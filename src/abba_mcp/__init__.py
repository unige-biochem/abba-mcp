"""abba-mcp (codename sextant): ABBA in Fiji, for AI assistants.

A thin stdio MCP server. It owns no image-analysis logic:
- it starts the pinned ABBA Fiji (jgo, env/jgo.toml) the first time a Fiji tool is called;
- it forwards the generic module tools to Fiji's own MCP server (fiji-llm + fiji-modules);
- it serves the bundled, version-matched docs (data/) as instructions and files.
"""

__all__ = ("main",)

import argparse
import asyncio
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

# The Fiji tools, forwarded as they are. Defined here so that the assistant sees them before Fiji runs.
FIJI_TOOLS = {
    "fiji_module_search": ("Find ABBA and Fiji commands and scripts whose title, menu path or description contain all the words "
                           "of the query, titles first. Every ABBA action is a command: search here, or grep the command docs.",
                           {"query": "words to look for, e.g. 'ABBA register'"}, ["query"]),
    "fiji_module_describe": ("Describe a command or script: its inputs (types, defaults, choices, descriptions, after its "
                             "initializers ran), its outputs, its messages, the live objects that fit its object inputs, "
                             "and the artifact and version providing it.",
                             {"id": "command title (e.g. 'ABBA - Snapshot'), class name, or script file path"}, ["id"]),
    "fiji_module_run": ("Run a command or script file with inputs as a JSON object string. Never opens a dialog: inputs not "
                        "given keep their default; an object input (ABBA session, atlas) with one live instance is bound to it. "
                        "Returns status, outputs (objects by name, pictures as images), new objects, logged warnings and errors. "
                        "Waits up to wait_seconds (default 60); longer runs return a job for fiji_module_status. "
                        "Starts Fiji first if it is not running (the first start takes minutes).",
                        {"id": "command title, class name, or script file path",
                         "inputs": "JSON object, e.g. {\"slices_csv\": \"0,3\"}", "wait_seconds": "seconds to wait"}, ["id"]),
    "fiji_module_status": ("Follow a run started by fiji_module_run: waits up to wait_seconds and returns its result or 'running'.",
                           {"job": "the job id", "wait_seconds": "seconds to wait"}, ["job"]),
    "fiji_objects": ("The live objects Fiji holds (ABBA sessions, atlases, windows, images...): without a type, the number "
                     "of objects per type; with a type, its objects by the names command inputs accept.",
                     {"type": "simple or full class name, e.g. MultiSlicePositioner"}, []),
    "fiji_module_script": ("The successful fiji_module_run calls of this session as a Groovy script that replays them, every "
                           "input explicit. Save it (path) next to the data once a result is right: it is the pipeline.",
                           {"path": "file to write; empty returns the script"}, []),
    # fiji-llm's window tools: what the user sees, in window mode (screen pixels: nothing headless or on a locked screen)
    "fiji_ui_windows_read": ("List the visible Fiji windows and dialogs: title, class, bounds, active state. The ABBA "
                             "window's title starts with its atlas; there may be several ABBA windows.", {}, []),
    "fiji_ui_screenshot": ("Picture of one visible window, as the user sees it: give its exact title (fiji_ui_windows_read). "
                           "Windows on top of it show too.",
                           {"window_title": "exact window title",
                            "window_class_name": "class name, only to tell apart windows with the same title",
                            "activate_and_restore": ("boolean", "bring the window to the front for the capture, then restore")},
                           ["window_title"]),
    "fiji_ui_dialogs_read": ("List the open dialogs: title, messages, buttons, modality. A command that opened a dialog for "
                             "the user (interactive registrations) waits until it is closed.", {}, []),
    "fiji_ui_dialog_respond": ("Click a button of an open dialog, by exact dialog title and button text (fiji_ui_dialogs_read "
                               "first). Only for dialogs the user asked you to answer.",
                               {"dialog_title": "exact dialog title", "button_text": "exact button text"},
                               ["dialog_title", "button_text"]),
}
# Arguments fiji-llm's tools expect even when not given
UI_DEFAULTS = {"fiji_ui_screenshot": {"window_class_name": "", "component_path": "", "activate_and_restore": False}}

DOC_TOOLS = {
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
        "properties": {k: ({"type": v[0], "description": v[1]} if isinstance(v, tuple) else {"type": "string", "description": v})
                       for k, v in props.items()},
        "required": required})


def _arguments(name: str, arguments: dict) -> dict:
    """The module tools take strings only; fiji-llm's own tools take typed values, some of them always."""
    if name.startswith("fiji_ui_"):
        return {**UI_DEFAULTS.get(name, {}), **(arguments or {})}
    return {k: str(v) for k, v in (arguments or {}).items()}


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
                result = await session.call_tool(name, _arguments(name, arguments))
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
          "`fiji_ui_screenshot` (`guides/window.md`).",
    False: "**Mode: headless.** Fiji runs without any window, and the user cannot see it: start sessions with "
           "`ABBA - Align Big Brains and Atlases (no GUI)`. Commands that need a window fail or do nothing "
           "(`ABBA - ABBA Start`, manual and BigWarp registrations), and so do the `fiji_ui_` tools. Show the user "
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
        return [tool(n, s) for n, s in {**FIJI_TOOLS, **DOC_TOOLS}.items()]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == "abba_docs_search":
            return [types.TextContent(type="text", text=_docs_search(arguments["pattern"]))]
        if name == "abba_docs_read":
            return [types.TextContent(type="text", text=_docs_read(arguments["path"]))]
        if name in FIJI_TOOLS:
            return await _forward(name, arguments, gui)
        raise ValueError(f"Unknown tool {name}")

    async def run():
        async with stdio_server() as (read, write):
            await server.run(read, write, server.create_initialization_options())

    asyncio.run(run())
    return 0
