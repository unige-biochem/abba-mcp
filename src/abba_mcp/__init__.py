"""abba-mcp (codename sextant): ABBA in Fiji, for AI assistants.

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
PORT = 9090
URL = f"http://127.0.0.1:{PORT}/mcp"
STATE = Path(os.environ.get("ABBA_MCP_HOME", Path.home() / ".abba-mcp"))
START_TIMEOUT_S = 1800  # the first start downloads Java, Fiji and ABBA


def _pinned(artifact: str) -> str:
    """The version of an artifact pinned in env/jgo.toml."""
    m = re.search(rf'"[^":]+:{artifact}:([^"]+)"', (ENV / "jgo.toml").read_text(encoding="utf-8"))
    return m.group(1) if m else "unknown"


# The bundle's version is ABBA's (build/check_env.sh checks it): the docs and examples are for this ABBA only.
ABBA_VERSION = _pinned("ImageToAtlasRegister")
FIJI_VERSION = _pinned("fiji")
try:  # in Maven's spelling, as ABBA's: Python spells 0.24.1-SNAPSHOT 0.24.1.dev0
    BUNDLE_VERSION = metadata.version("abba-fiji-mcp").replace(".dev0", "-SNAPSHOT")
except metadata.PackageNotFoundError:
    BUNDLE_VERSION = "unknown"

# The Fiji tools this bundle forwards: fiji-modules' module tools, and fiji-llm's window tools for window mode. Not
# fiji-llm's screenshot: it copies screen pixels, so it shows whatever covers the window, possibly another application
# of the user (abba_window_picture instead).
FORWARDED = ["fiji_module_search", "fiji_module_describe", "fiji_module_run", "fiji_module_status", "fiji_objects",
             "fiji_module_script", "fiji_ui_windows_read", "fiji_ui_dialogs_read", "fiji_ui_dialog_respond"]

# Their definitions as Fiji serves them, written by build/gen_tools.py: the assistant must see the tools before Fiji
# runs, and the Java code stays their only source. The bundle only adds a sentence about ABBA to some of them.
FIJI_TOOLS_FILE = HERE / "fiji_tools.json"
NOTES = {
    "fiji_module_search": "Every ABBA action is a command: search here, or grep the command docs.",
    "fiji_module_run": "Starts Fiji first if it is not running: the first start downloads Fiji and ABBA and takes minutes.",
    "fiji_objects": "An ABBA session is a MultiSlicePositioner.",
    "fiji_ui_windows_read": "The ABBA window's title starts with its atlas; there may be several ABBA windows.",
    "fiji_ui_dialogs_read": "A command that opened a dialog for the user (interactive registrations) waits until it is closed.",
    "fiji_ui_dialog_respond": "Only for dialogs the user asked you to answer.",
}


@functools.cache
def fiji_tools() -> dict:
    return {t["name"]: types.Tool(name=t["name"], description=" ".join(filter(None, [t["description"], NOTES.get(t["name"])])),
                                  inputSchema=t["inputSchema"])
            for t in json.loads(FIJI_TOOLS_FILE.read_text(encoding="utf-8"))}

PICTURE_SCRIPT = DATA / "scripting" / "window_picture.groovy"

# Served by this bundle
BUNDLE_TOOLS = {
    "abba_window_picture": ("Picture of one Fiji window as it is drawn, what the user sees in it: right even when the window "
                            "is covered or the screen is locked, and never another application. Window mode only. Not "
                            "recorded in fiji_module_script.",
                            {"window_title": "the window title, or its start (fiji_ui_windows_read); default: the first "
                                             "ABBA window"}, []),
    "abba_docs_search": ("Search the bundled ABBA documentation (guides, one file per command, scripting, examples) with a "
                         "regular expression; returns matching lines with their file. For assistants without file access: "
                         "with file access, grep the docs folder named in the instructions instead.",
                         {"pattern": "case-insensitive regular expression"}, ["pattern"]),
    "abba_docs_read": ("Read one bundled documentation file, by its path relative to the docs folder (as abba_docs_search gives it).",
                       {"path": "e.g. guides/abba.md"}, ["path"]),
}


def tool(name, spec):
    description, props, required = spec
    return types.Tool(name=name, description=description, inputSchema={
        "type": "object",
        "properties": {k: {"type": "string", "description": v} for k, v in props.items()},
        "required": required})


# -- Fiji lifecycle --

def _port_open() -> bool:
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", PORT)) == 0


def _jgo() -> list:
    exe = shutil.which("jgo", path=str(Path(sys.executable).parent)) or shutil.which("jgo")
    return [exe] if exe else [sys.executable, "-m", "jgo"]


def _start_fiji(gui: bool):
    STATE.mkdir(parents=True, exist_ok=True)
    work = STATE / "env"
    work.mkdir(exist_ok=True)
    for f in ("jgo.toml", "startmcp.groovy", "logback.xml"):  # jgo keeps its cache next to jgo.toml
        shutil.copy(ENV / f, work / f)
    here = work.as_posix()
    env = dict(os.environ)
    opts = f"--add-opens=java.base/java.lang=ALL-UNNAMED -Dlogback.configurationFile={here}/logback.xml"
    if not gui:
        opts += " -Djava.awt.headless=true"
    env["JAVA_TOOL_OPTIONS"] = opts
    args = _jgo() + ["--lenient", "--class-path-only", "run", "--local", "--", "--"]
    args += (["--headless"] if not gui else []) + ["--run", f"{here}/startmcp.groovy"]
    log = open(STATE / "fiji.log", "w", encoding="utf-8")
    flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS if os.name == "nt" else 0
    return subprocess.Popen(args, cwd=work, env=env, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                            creationflags=flags, start_new_session=os.name != "nt")


_verified = False  # the Fiji on PORT runs the ABBA version of this bundle


async def _ensure_fiji(gui: bool):
    global _verified
    if _port_open():
        return
    _verified = False
    process = _start_fiji(gui)
    t0 = time.time()
    while time.time() - t0 < START_TIMEOUT_S:
        await asyncio.sleep(2)
        if process.poll() is not None:  # it died: say why, now
            tail = (STATE / "fiji.log").read_text(encoding="utf-8", errors="replace")[-1500:]
            raise RuntimeError(f"Fiji stopped while starting (exit {process.returncode}). "
                               f"Log {STATE / 'fiji.log'}:\n{tail}")
        if _port_open():
            await asyncio.sleep(2)
            return
    raise RuntimeError(f"Fiji did not start within {START_TIMEOUT_S} s, see {STATE / 'fiji.log'}")


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
          "`abba_window_picture` (`guides/window.md`).",
    False: "**Mode: headless.** Fiji runs without any window, and the user cannot see it: start sessions with "
           "`ABBA - Align Big Brains and Atlases (no GUI)`. Commands that need a window fail or do nothing "
           "(`ABBA - ABBA Start`, manual and BigWarp registrations), and so do the window tools. Show the user "
           "snapshots instead.",
}


def instructions(gui: bool = True) -> str:
    text = (DATA / "instructions.md").read_text(encoding="utf-8")
    return (text.replace("{DOCS}", DATA.as_posix()).replace("{MODE}", MODES[gui])
            .replace("{ABBA_VERSION}", ABBA_VERSION).replace("{BUNDLE_VERSION}", BUNDLE_VERSION)
            .replace("{FIJI_VERSION}", FIJI_VERSION))


def main() -> int:
    parser = argparse.ArgumentParser(description="ABBA in Fiji, for AI assistants (MCP, stdio).")
    parser.add_argument("--headless", action="store_true", help="start Fiji without a window")
    parser.add_argument("--print-instructions", action="store_true")
    parser.add_argument("--version", action="version",
                        version=f"abba-fiji {BUNDLE_VERSION} (ABBA {ABBA_VERSION}, Fiji {FIJI_VERSION})")
    args = parser.parse_args()
    gui = not (args.headless or os.environ.get("ABBA_MCP_HEADLESS", "").lower() in ("1", "true", "yes"))
    if args.print_instructions:
        print(instructions(gui))
        return 0

    server = Server("abba-fiji", version=BUNDLE_VERSION, instructions=instructions(gui))

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
        if name in fiji_tools():
            return await _forward(name, arguments, gui)
        raise ValueError(f"Unknown tool {name}")

    async def run():
        async with stdio_server() as (read, write):
            await server.run(read, write, server.create_initialization_options())

    asyncio.run(run())
    return 0
