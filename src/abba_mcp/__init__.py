"""abba-mcp: ABBA in Fiji, for AI assistants.

A thin stdio MCP server. It owns no image-analysis logic:
- it starts the pinned ABBA Fiji (jgo, env/jgo.toml) the first time a Fiji tool is called;
- it forwards the generic module tools to Fiji's own MCP server (fiji-llm + fiji-modules);
- it serves the bundled, version-matched docs (data/) as instructions and files.
"""

__all__ = ("main",)

import argparse
import asyncio
import functools
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
from importlib import metadata
from pathlib import Path

import mcp.types as types
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
ENV = HERE / "env"
# fiji-llm's default; ABBA_MCP_PORT runs several bundles side by side (tests), each with its own ABBA_MCP_HOME
PORT = int(os.environ.get("ABBA_MCP_PORT", "9090"))
URL = f"http://127.0.0.1:{PORT}/mcp"
STATE = Path(os.environ.get("ABBA_MCP_HOME", Path.home() / ".abba-mcp"))
START_TIMEOUT_S = 1800  # the first start downloads Java, Fiji and ABBA
# MCP clients abort a request after about 60 s (the TypeScript SDK's default): a tool call waits for Fiji's start at
# most this long. fiji-modules caps its own waits (wait_seconds) the same way.
MAX_WAIT_S = 40


def _pinned(artifact: str) -> str:
    """The version of an artifact pinned in env/jgo.toml."""
    m = re.search(rf'"[^":]+:{artifact}:([^"]+)"', (ENV / "jgo.toml").read_text(encoding="utf-8"))
    return m.group(1) if m else "unknown"


# The bundle's version is ABBA's (build/check_env.sh checks it): the docs and examples are for this ABBA only.
ABBA_VERSION = _pinned("ImageToAtlasRegister")
FIJI_VERSION = _pinned("fiji")
# The user documentation is tagged per ABBA release (v<version>); a SNAPSHOT has none yet
USER_DOCS = ("https://abba-documentation.readthedocs.io/en/"
             + ("latest/" if ABBA_VERSION.endswith("-SNAPSHOT") else f"v{ABBA_VERSION}/"))
try:  # in Maven's spelling, as ABBA's: Python spells 0.24.1-SNAPSHOT 0.24.1.dev0
    BUNDLE_VERSION = metadata.version("abba-mcp").replace(".dev0", "-SNAPSHOT")
except metadata.PackageNotFoundError:
    BUNDLE_VERSION = "unknown"

# The Fiji tools this bundle forwards: fiji-modules' module tools, and fiji-llm's window tools for window mode. Not
# fiji-llm's screenshot: it copies screen pixels, so it shows whatever covers the window, possibly another application
# of the user (abba_window_picture instead).
FORWARDED = ["fiji_module_search", "fiji_module_describe", "fiji_module_run", "fiji_module_run_script", "fiji_module_status", "fiji_objects",
             "fiji_module_script", "fiji_ui_windows_read", "fiji_ui_dialogs_read", "fiji_ui_dialog_respond",
             "fiji_ui_dialog_close"]

# Their definitions as Fiji serves them, written by build/gen_tools.py: the assistant must see the tools before Fiji
# runs, and the Java code stays their only source. The bundle only adds a sentence about ABBA to some of them.
FIJI_TOOLS_FILE = HERE / "fiji_tools.json"
NOTES = {
    "fiji_module_search": "Every ABBA action is a command: search here, or grep the command docs.",
    "fiji_module_run": "Starts Fiji first if it is not running: the first start downloads Fiji and ABBA and takes minutes.",
    "fiji_module_run_script": "Write Groovy, as ABBA's docs and examples: 'python' here is Jython 2.7, not CPython. Read scripting/groovy-steps.md before the first script: a line starting with #@ is a parameter even inside a string. The ABBA window is a ch.epfl.biop.atlas.aligner.gui.bdv.BdvMultislicePositionerView, the session a ch.epfl.biop.atlas.aligner.MultiSlicePositioner (guides/window.md, scripting/).",
    "fiji_objects": "An ABBA session is a MultiSlicePositioner.",
    "fiji_ui_windows_read": "The ABBA window's title starts with its atlas; there may be several ABBA windows.",
    "fiji_ui_dialogs_read": "A command that opened a dialog for the user (interactive registrations) waits until it is closed.",
    "fiji_ui_dialog_respond": "Only for dialogs the user asked you to answer.",
    "fiji_ui_dialog_close": "Only for dialogs the user asked you to close.",
}


# What each tool may do, for clients deciding which calls the user confirms: the ones that only look are read-only;
# stopping Fiji is destructive (unsaved work is lost); running a module may be (deleting slices, say), so it keeps
# MCP's default. All act on this computer only.
READ_ONLY = {"fiji_module_search", "fiji_module_describe", "fiji_module_status", "fiji_objects", "fiji_ui_windows_read",
             "fiji_ui_dialogs_read", "abba_window_picture", "abba_docs_search", "abba_docs_read"}
DESTRUCTIVE = {"abba_fiji_stop"}


def annotations(name: str) -> types.ToolAnnotations:
    if name in READ_ONLY:
        return types.ToolAnnotations(readOnlyHint=True, openWorldHint=False)
    if name in DESTRUCTIVE:
        return types.ToolAnnotations(title="Stop Fiji (closes ABBA; unsaved work is lost)", readOnlyHint=False,
                                     destructiveHint=True, openWorldHint=False)
    if name == "abba_window_view":  # changes the view only
        return types.ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=True, openWorldHint=False)
    return types.ToolAnnotations(readOnlyHint=False, openWorldHint=False)


@functools.cache
def fiji_tools() -> dict:
    return {t["name"]: types.Tool(name=t["name"], description=" ".join(filter(None, [t["description"], NOTES.get(t["name"])])),
                                  inputSchema=t["inputSchema"], annotations=annotations(t["name"]))
            for t in json.loads(FIJI_TOOLS_FILE.read_text(encoding="utf-8"))}

PICTURE_SCRIPT = DATA / "scripting" / "window_picture.groovy"
VIEW_SCRIPT = DATA / "scripting" / "window_view.groovy"

# Served by this bundle
BUNDLE_TOOLS = {
    "abba_window_picture": ("Picture of one Fiji window, or dialog, as it is drawn, what the user sees in it: right even when the window "
                            "is covered or the screen is locked, and never another application. Window mode only. Not "
                            "recorded in fiji_module_script.",
                            {"window_title": "the window title, or its start (fiji_ui_windows_read); default: the first "
                                             "ABBA window"}, []),
    "abba_window_view": ("Sets what an ABBA window shows the user: its mode, its current slice, the channels shown, and "
                         "what is framed. Review mode: the atlas section of the current slice, whole or a region of it. "
                         "Positioning mode: the current slice and its neighbours with the atlas above, or all the "
                         "slices. Window mode only. Changes the view, not the session; not recorded in "
                         "fiji_module_script. A session started without a window gets one. Then look with abba_window_picture. The window has no region names: to "
                         "name what it shows, use ABBA - Snapshot with labels on the same region_mm.",
                         {"window_title": "the window title, or its start; default: the first ABBA window",
                          "mode": "'positioning' or 'review' (the current slice alone over the atlas); empty keeps it",
                          "slice_index": "0-based index of the slice to make current, as in ABBA - Get State; empty "
                                         "keeps the current slice",
                          "region_mm": "region to zoom on, 'x,y,width,height' in mm, as ABBA - Snapshot's region_mm "
                                       "(x, y: top left, as read on a snapshot's rulers); 'all' frames all the slices "
                                       "in positioning mode; empty: see above",
                          "slice_channels": "slice channels to show on every slice, e.g. '0' for the first alone, "
                                            "'*' for all, 'none'; empty keeps them",
                          "atlas_channels": "atlas channels to show, in the order of 'atlas_channels' in ABBA - Get "
                                            "State, e.g. '0,2' (Allen: Nissl and borders), 'none'; empty keeps them"}, []),
    "abba_fiji_stop": ("Stops the Fiji this extension started: the ABBA window closes and unsaved work is lost. Only "
                       "when the user explicitly asks to stop or restart Fiji. Never to check, wait for or speed up a "
                       "start: a start taking minutes is normal, and stopping it starts it all over again. To look at "
                       "Fiji, use fiji_ui_windows_read or abba_window_picture.",
                       {"user_request": "the user's own words asking to stop or restart Fiji, quoted"}, ["user_request"]),
    "abba_docs_search": ("Search the bundled ABBA documentation (guides, one file per command, scripting, examples) with a "
                         "regular expression; returns matching lines with their file. For assistants without file access: "
                         "with file access, grep the docs folder named in the instructions instead. This server: bundle "
                         f"abba-mcp {BUNDLE_VERSION}, for ABBA {ABBA_VERSION} only.",
                         {"pattern": "case-insensitive regular expression"}, ["pattern"]),
    "abba_docs_read": ("Read one bundled documentation file, by its path relative to the docs folder (as abba_docs_search gives it).",
                       {"path": "e.g. guides/abba.md"}, ["path"]),
}


def tool(name, spec):
    description, props, required = spec
    return types.Tool(name=name, description=description, annotations=annotations(name), inputSchema={
        "type": "object",
        "properties": {k: {"type": "string", "description": v} for k, v in props.items()},
        "required": required})


# -- Fiji lifecycle --

def _port_open() -> bool:
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", PORT)) == 0


def _section(name: str) -> dict:
    """The `key = "value"` lines of one [section] of env/jgo.toml."""
    section = re.search(rf"^\[{name}\]\n(.*?)(?=^\[|\Z)", (ENV / "jgo.toml").read_text(encoding="utf-8"), re.M | re.S)
    return dict(re.findall(r'^(\w[\w.-]*)\s*=\s*"([^"]+)"', section.group(1) if section else "", re.M))


def _repositories() -> list:
    """jgo options for the [repositories] of env/jgo.toml: jgo 3.1 reads that section but resolves from Maven Central
    only, so ABBA resolved only where the local Maven repository already held it."""
    return [o for name, url in _section("repositories").items() for o in ("-r", f"{name}:{url}")]


def _java_home() -> Path:
    """The JDK of [java] in env/jgo.toml, downloaded on first use. jgo would run any Java already installed (JAVA_HOME,
    PATH) that is at least that version, whatever its vendor: the server puts this one first instead."""
    import cjdk  # a dependency of jgo, which uses the same cache

    java = _section("java")
    return Path(cjdk.java_home(vendor=java["vendor"], version=java["version"]))


def _jgo() -> list:
    exe = shutil.which("jgo", path=str(Path(sys.executable).parent)) or shutil.which("jgo")
    return ([exe] if exe else [sys.executable, "-m", "jgo"]) + _repositories()


def _start_fiji(gui: bool, java_home: Path):
    STATE.mkdir(parents=True, exist_ok=True)
    work = STATE / "env"
    work.mkdir(exist_ok=True)
    for f in ("jgo.toml", "startmcp.groovy", "logback.xml"):  # jgo keeps its cache next to jgo.toml
        shutil.copy(ENV / f, work / f)
    here = work.as_posix()
    env = dict(os.environ)
    # jgo looks at JAVA_HOME, then PATH; on Windows only PATH counts (it looks for bin/java, not bin/java.exe)
    env["JAVA_HOME"] = str(java_home)
    env["PATH"] = str(java_home / "bin") + os.pathsep + env.get("PATH", "")
    opts = f"--add-opens=java.base/java.lang=ALL-UNNAMED -Dlogback.configurationFile={here}/logback.xml"
    if not gui:
        opts += " -Djava.awt.headless=true"
    if "ABBA_MCP_PORT" in os.environ:  # read by startmcp.groovy
        opts += f" -Dabba.mcp.port={PORT}"
    env["JAVA_TOOL_OPTIONS"] = opts
    args = _jgo() + ["--lenient", "--class-path-only", "run", "--local", "--", "--"]
    # Not single instance: otherwise, with another Fiji open (the user's own), ImageJ passes the arguments to it, and
    # the startup script opens in that Fiji while this one waits with no MCP server
    args += (["--headless"] if not gui else ["--forbid-single-instance"]) + ["--run", f"{here}/startmcp.groovy"]
    log = open(STATE / "fiji.log", "w", encoding="utf-8")
    log.write(f"abba-mcp {BUNDLE_VERSION}, Java: {java_home}\n")
    log.flush()
    flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS if os.name == "nt" else 0
    process = subprocess.Popen(args, cwd=work, env=env, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                               creationflags=flags, start_new_session=os.name != "nt")
    PID_FILE.write_text(str(process.pid))
    return process.pid


# The Fiji this bundle started (the jgo process, Fiji's parent), for a later server to wait for it rather than start
# another (a client restarting its servers), and to stop it
PID_FILE = STATE / "fiji.pid"


def _is_ours(pid: int, written: float) -> bool:
    """Whether pid still runs and is the process started when the pid file was written, not a reuse of its number."""
    if os.name == "nt":  # os.kill(pid, 0) would terminate it on Windows
        import ctypes
        k32 = ctypes.windll.kernel32
        handle = k32.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not handle:
            return False
        code, times = ctypes.c_ulong(), (ctypes.c_ulonglong * 4)()
        ok = k32.GetExitCodeProcess(handle, ctypes.byref(code)) and k32.GetProcessTimes(
            handle, ctypes.byref(times, 0), ctypes.byref(times, 8), ctypes.byref(times, 16), ctypes.byref(times, 24))
        k32.CloseHandle(handle)
        created = (times[0] - 116444736000000000) / 1e7  # FILETIME: 100 ns since 1601
        return bool(ok) and code.value == 259 and abs(created - written) < 60  # 259: STILL_ACTIVE
    out = subprocess.run(["ps", "-p", str(pid), "-o", "command="], capture_output=True, text=True).stdout
    return "jgo" in out


def _our_fiji():
    """The pid of the Fiji this bundle started, if it still runs."""
    try:
        pid = int(PID_FILE.read_text())
        return pid if _is_ours(pid, PID_FILE.stat().st_mtime) else None
    except (OSError, ValueError):
        return None


def _stop_requested(user_request: str) -> str:
    """abba_fiji_stop: refused while Fiji starts, and without the user's request."""
    if not user_request.strip():
        raise ValueError("Not stopped: abba_fiji_stop needs the user's own words asking to stop or restart Fiji.")
    if (_starting is not None and not _starting.done()) or (not _port_open() and _our_fiji() is not None):
        raise ValueError("Not stopped: Fiji is starting, which takes minutes the first time. Stopping it would start it "
                         "all over again: call a Fiji tool again to wait, or fiji_ui_windows_read to look.")
    return _stop_fiji()


def _stop_fiji() -> str:
    global _verified
    _verified = False  # the next Fiji is checked again
    pid = _our_fiji()
    if pid is None:
        return "No Fiji started by this extension is running."
    if os.name == "nt":
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(pid)], capture_output=True)
    else:
        os.killpg(pid, 15)
    PID_FILE.unlink(missing_ok=True)
    return (f"Fiji is stopped (process {pid}): it no longer runs, and its windows are closed. A new Fiji starts at the "
            "next Fiji tool call (slices, if any, come back only from a saved state).")


_verified = False  # the Fiji on PORT runs the ABBA version of this bundle
_starting = None  # the task starting Fiji: it outlives the tool calls that wait for it
_started_at = 0.0


async def _start(gui: bool):
    global _started_at
    if _our_fiji() is not None:  # started by an earlier server process (the client restarted it): wait for that one
        _started_at = PID_FILE.stat().st_mtime
    else:
        try:  # a download on first use: off the event loop
            java_home = await asyncio.to_thread(_java_home)
        except Exception as e:
            raise RuntimeError(f"Could not get Java {_section('java')} (downloaded on first use): {e}") from e
        _start_fiji(gui, java_home)
    while time.time() - _started_at < START_TIMEOUT_S:
        await asyncio.sleep(2)
        if _port_open():
            await asyncio.sleep(2)
            return
        if _our_fiji() is None:  # it died: say why
            raise RuntimeError(f"Fiji stopped while starting. Log {STATE / 'fiji.log'}:\n{_log_tail(1500)}")
        if "Detected existing ImageJ" in _log_tail(5000):  # it handed its arguments to another Fiji, and idles
            _stop_fiji()
            raise RuntimeError("Fiji did not start: another Fiji took its startup script (ImageJ's single instance "
                               "mode). Ask the user to close the other Fiji, then call the tool again.")
    raise RuntimeError(f"Fiji did not start within {START_TIMEOUT_S} s, see {STATE / 'fiji.log'}")


def _log_tail(chars: int) -> str:
    try:
        return (STATE / "fiji.log").read_text(encoding="utf-8", errors="replace")[-chars:]
    except OSError:
        return ""


async def _ensure_fiji(gui: bool):
    """Returns once Fiji answers. A start takes minutes the first time, longer than clients wait for a tool call: it
    goes on in the background, and the call says so after MAX_WAIT_S, for the assistant to call again."""
    global _verified, _starting, _started_at
    if _port_open():
        return
    if _starting is None:
        _verified = False
        _started_at = time.time()
        _starting = asyncio.create_task(_start(gui))
    task = _starting
    try:
        await asyncio.wait_for(asyncio.shield(task), MAX_WAIT_S)
    except asyncio.TimeoutError:
        last = (_log_tail(300).strip().splitlines() or ["(nothing yet)"])[-1]
        raise RuntimeError(f"Not run: Fiji is starting ({time.time() - _started_at:.0f} s so far; the first start "
                           f"downloads Java, Fiji and ABBA and takes minutes). Tell the user, then call the tool "
                           f"again. Last line of {STATE / 'fiji.log'}: {last}") from None
    finally:
        if task.done() and _starting is task:  # started, or failed: a later call starts afresh
            _starting = None


async def _forward(name: str, arguments: dict, gui: bool):
    await _ensure_fiji(gui)
    # Refusals are raised after the connection closes: raised inside it, they reach the client as a bare TaskGroup error
    problem = None
    async with streamablehttp_client(URL, timeout=30, sse_read_timeout=3600) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            listed = {t.name for t in (await session.list_tools()).tools}
            if name not in listed:
                problem = (f"Port {PORT} answers but it is not ABBA's Fiji (no {name}): "
                           "close the other Fiji that uses its MCP server, then retry.")
            else:
                problem = await _version_problem(session)
            if problem is None:
                result = await session.call_tool(name, {k: str(v) for k, v in (arguments or {}).items()})
                return result.content
    raise RuntimeError(problem)


async def _version_problem(session):
    """Why the Fiji on PORT is not this bundle's ABBA version (such as the user's own Fiji), or None."""
    global _verified
    if _verified:
        return None
    result = await session.call_tool("fiji_module_describe", {"id": "ABBA - Save State"})
    text = "".join(c.text for c in result.content if getattr(c, "type", "") == "text")
    try:
        running = json.loads(text).get("provided_by") or "an unknown ABBA version"
    except ValueError:
        running = "no ABBA"
    if running != f"ch.epfl.biop:ImageToAtlasRegister:{ABBA_VERSION}":
        return (f"The Fiji on port {PORT} runs {running}, but this server and its docs are for ABBA {ABBA_VERSION}. "
                f"Ask the user to close that Fiji, then retry: this server then starts ABBA {ABBA_VERSION}.")
    _verified = True
    return None


# -- docs --

def _docs_search(pattern: str) -> str:
    rx = re.compile(pattern, re.IGNORECASE)
    hits = []
    for f in sorted(DATA.rglob("*")):
        if not f.is_file() or f.suffix not in (".md", ".groovy", ".txt"):
            continue
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if rx.search(line):
                hits.append(f"{f.relative_to(DATA).as_posix()}:{i}: {line.strip()[:200]}")
                if len(hits) >= 60:
                    return "\n".join(hits) + "\n... (more: refine the pattern)"
    return "\n".join(hits) or "no match"


def _docs_read(path: str) -> str:
    f = (DATA / path).resolve()
    if DATA not in f.parents or not f.is_file():
        raise ValueError(f"No doc file {path!r}: use abba_docs_search, or read INDEX.md")
    return f.read_text(encoding="utf-8")


MODES = {
    True: "**Mode: window.** Fiji shows its windows on the user's screen: start sessions with `ABBA - ABBA Start`. "
          "The user can act in the ABBA window too: share slices through the selection, see what they see with "
          "`abba_window_picture`, and show them a mode, a slice or a region with `abba_window_view` (`guides/window.md`).",
    False: "**Mode: headless.** Fiji runs without any window, and the user cannot see it: start sessions with "
           "`ABBA - Align Big Brains and Atlases (no GUI)`. Commands that need a window fail or do nothing "
           "(`ABBA - ABBA Start`, manual and BigWarp registrations), and so do the window tools. Show the user "
           "snapshots instead.",
}


def instructions(gui: bool = True) -> str:
    text = (DATA / "instructions.md").read_text(encoding="utf-8")
    return (text.replace("{DOCS}", DATA.as_posix()).replace("{MODE}", MODES[gui])
            .replace("{ABBA_VERSION}", ABBA_VERSION).replace("{BUNDLE_VERSION}", BUNDLE_VERSION)
            .replace("{FIJI_VERSION}", FIJI_VERSION).replace("{USER_DOCS}", USER_DOCS))


def main() -> int:
    parser = argparse.ArgumentParser(description="ABBA in Fiji, for AI assistants (MCP, stdio).")
    parser.add_argument("--headless", action="store_true", help="start Fiji without a window")
    parser.add_argument("--print-instructions", action="store_true")
    parser.add_argument("--version", action="version",
                        version=f"abba-mcp {BUNDLE_VERSION} (ABBA {ABBA_VERSION}, Fiji {FIJI_VERSION})")
    args = parser.parse_args()
    gui = not (args.headless or os.environ.get("ABBA_MCP_HEADLESS", "").lower() in ("1", "true", "yes"))
    if args.print_instructions:
        print(instructions(gui))
        return 0

    server = Server("abba-mcp", version=BUNDLE_VERSION, instructions=instructions(gui))

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return list(fiji_tools().values()) + [tool(n, s) for n, s in BUNDLE_TOOLS.items()]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == "abba_docs_search":
            return [types.TextContent(type="text", text=_docs_search(arguments["pattern"]))]
        if name == "abba_docs_read":
            return [types.TextContent(type="text", text=_docs_read(arguments["path"]))]
        if name == "abba_window_picture":
            inputs = {"window_title": arguments["window_title"]} if (arguments or {}).get("window_title") else {}
            return await _forward("fiji_module_run", {"id": PICTURE_SCRIPT.as_posix(), "inputs": json.dumps(inputs),
                                                      "wait_seconds": "30"}, gui)
        if name == "abba_fiji_stop":
            return [types.TextContent(type="text", text=_stop_requested((arguments or {}).get("user_request", "")))]
        if name == "abba_window_view":
            inputs = {k: v for k, v in (arguments or {}).items() if v not in (None, "")}
            return await _forward("fiji_module_run", {"id": VIEW_SCRIPT.as_posix(), "inputs": json.dumps(inputs),
                                                      "wait_seconds": "30"}, gui)
        if name in fiji_tools():
            return await _forward(name, arguments, gui)
        raise ValueError(f"Unknown tool {name}")

    async def run():
        async with stdio_server() as (read, write):
            await server.run(read, write, server.create_initialization_options())

    asyncio.run(run())
    return 0
