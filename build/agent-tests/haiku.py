"""Talk to a Haiku agent that has only the ABBA (Fiji) MCP bundle, as a Claude Desktop user would.

    python haiku.py send <pair_dir> "<message>"   starts a turn, then waits for Haiku's answer (up to WAIT_S)
    python haiku.py wait <pair_dir>               keeps waiting for a turn still running
    python haiku.py stop <pair_dir>               ends the test: stops Haiku and the pair's Fiji

<pair_dir>/pair.json: {"port": 9201, "bundle": "<unzipped bundle>", "headless": false}
Each pair has its own Fiji (ABBA_MCP_HOME=<pair_dir>/abba-home, ABBA_MCP_PORT=port) and Claude session.
Prints Haiku's messages, a compact log of its tool calls, and the paths of the pictures it was shown.
Everything is also appended to <pair_dir>/transcript.md.
"""
import base64
import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path

WAIT_S = 540
MODEL = "claude-haiku-5-5"
SYSTEM = ("You are Claude, an AI assistant made by Anthropic, chatting with a user in the Claude desktop app. "
          "The user installed the extension 'ABBA (Fiji)': its tools are your only way to act. You cannot read or "
          "write files on the user's computer and have no shell. Be helpful and concise; answer in the user's language.")


def load(pair: Path) -> dict:
    return json.loads((pair / "pair.json").read_text(encoding="utf-8"))


def state(pair: Path) -> dict:
    f = pair / "state.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {"session": None, "turn": 0, "pid": None}


def save_state(pair: Path, s: dict):
    (pair / "state.json").write_text(json.dumps(s), encoding="utf-8")


def mcp_config(pair: Path, cfg: dict) -> Path:
    env = {"ABBA_MCP_HOME": str(pair / "abba-home"), "ABBA_MCP_PORT": str(cfg["port"])}
    if cfg.get("headless"):
        env["ABBA_MCP_HEADLESS"] = "true"
    conf = {"mcpServers": {"abba": {"command": "uv", "args": ["run", "--directory", cfg["bundle"], "abba-mcp"], "env": env}}}
    f = pair / "mcp.json"
    f.write_text(json.dumps(conf, indent=1), encoding="utf-8")
    return f


def alive(pid) -> bool:
    if not pid:
        return False
    out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout
    return str(pid) in out


def send(pair: Path, message: str):
    cfg, s = load(pair), state(pair)
    if alive(s.get("pid")):
        sys.exit("A turn is still running: use 'wait', or 'stop'.")
    s["turn"] += 1
    n = s["turn"]
    turns = pair / "turns"
    turns.mkdir(exist_ok=True)
    (turns / f"{n}_user.md").write_text(message, encoding="utf-8")
    cwd = pair / "cwd"
    cwd.mkdir(exist_ok=True)
    args = ["claude", "-p", message, "--model", MODEL, "--tools", "", "--mcp-config", str(mcp_config(pair, cfg)),
            "--strict-mcp-config", "--setting-sources", "", "--disable-slash-commands", "--permission-mode",
            "bypassPermissions", "--output-format", "stream-json", "--verbose", "--system-prompt", SYSTEM]
    if s["session"]:
        args += ["--resume", s["session"]]
    else:
        s["session"] = str(uuid.uuid4())
        args += ["--session-id", s["session"]]
    env = dict(os.environ, MCP_TOOL_TIMEOUT="60000")  # as Claude Desktop: a tool call is abandoned after about 60 s
    env.pop("CLAUDECODE", None)
    out = open(turns / f"{n}_stream.jsonl", "w", encoding="utf-8")
    err = open(turns / f"{n}_stderr.txt", "w", encoding="utf-8")
    args[0] = shutil.which("claude")  # no shell: the message goes through as it is
    p = subprocess.Popen(args, cwd=cwd, env=env, stdout=out, stderr=err, stdin=subprocess.DEVNULL,
                         creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    s["pid"] = p.pid
    save_state(pair, s)
    with open(pair / "transcript.md", "a", encoding="utf-8") as t:
        t.write(f"\n\n## Turn {n}\n\n**USER:** {message}\n")
    wait(pair)


def wait(pair: Path):
    s = state(pair)
    n = s["turn"]
    stream = pair / "turns" / f"{n}_stream.jsonl"
    t0 = time.time()
    while time.time() - t0 < WAIT_S:
        if has_result(stream) or not alive(s.get("pid")):
            time.sleep(1)
            report(pair, n)
            s["pid"] = None
            save_state(pair, s)
            return
        time.sleep(3)
    print(f"Turn {n} still running after another {WAIT_S} s (Haiku is working). Progress so far:\n")
    print(summarize(pair, n, final=False))
    print("\nCall: python haiku.py wait <pair_dir>")


def has_result(stream: Path) -> bool:
    try:
        return any('"type":"result"' in line for line in stream.read_text(encoding="utf-8", errors="replace").splitlines())
    except OSError:
        return False


def summarize(pair: Path, n: int, final: bool) -> str:
    stream = pair / "turns" / f"{n}_stream.jsonl"
    images = pair / "images"
    images.mkdir(exist_ok=True)
    lines, names, k = [], {}, 0
    for raw in stream.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            ev = json.loads(raw)
        except ValueError:
            continue
        if ev.get("type") == "assistant":
            for c in ev["message"].get("content", []):
                if c.get("type") == "text" and c["text"].strip():
                    lines.append(f"HAIKU: {c['text'].strip()}")
                elif c.get("type") == "tool_use":
                    names[c["id"]] = c["name"].split("__")[-1]
                    lines.append(f"  -> {names[c['id']]} {json.dumps(c.get('input', {}), ensure_ascii=False)[:400]}")
        elif ev.get("type") == "user":
            content = ev.get("message", {}).get("content", [])
            for c in content if isinstance(content, list) else []:
                if c.get("type") != "tool_result":
                    continue
                parts = c.get("content")
                parts = parts if isinstance(parts, list) else [{"type": "text", "text": str(parts)}]
                texts = []
                for part in parts:
                    if part.get("type") == "image":
                        k += 1
                        f = images / f"t{n}_{k}.png"
                        f.write_bytes(base64.b64decode(part["source"]["data"]))
                        texts.append(f"[picture shown to Haiku: {f}]")
                    elif part.get("type") == "text":
                        texts.append(part["text"])
                body = " ".join(" ".join(texts).split())
                flag = "ERROR " if c.get("is_error") else ""
                lines.append(f"  <- {flag}{body[:600]}{' ...' if len(body) > 600 else ''}")
        elif ev.get("type") == "result" and final:
            lines.append(f"[turn {n} ended: {ev.get('subtype')}, {ev.get('duration_ms', 0) / 1000:.0f} s, "
                         f"{ev.get('num_turns')} steps]")
    return "\n".join(lines) if lines else "(no output yet)"


def report(pair: Path, n: int):
    text = summarize(pair, n, final=True)
    err = (pair / "turns" / f"{n}_stderr.txt").read_text(encoding="utf-8", errors="replace").strip()
    if err:
        text += "\n[stderr] " + err[-800:]
    with open(pair / "transcript.md", "a", encoding="utf-8") as t:
        t.write("\n```\n" + text + "\n```\n")
    print(text)


def stop(pair: Path):
    s, cfg = state(pair), load(pair)
    if alive(s.get("pid")):
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(s["pid"])], capture_output=True)
    # The pair's Fiji: the process listening on its port, if its command line is this pair's
    ps = ("$c = Get-NetTCPConnection -LocalPort %d -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1; "
          "if ($c) { $p = Get-CimInstance Win32_Process -Filter \"ProcessId=$($c.OwningProcess)\"; "
          "if ($p.CommandLine -like '*%s*') { Stop-Process -Id $p.ProcessId -Force; 'Fiji stopped' } else { 'not this pair''s Fiji' } } "
          "else { 'no Fiji on the port' }") % (cfg["port"], pair.name)
    print(subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True).stdout.strip())
    s["pid"] = None
    save_state(pair, s)


if __name__ == "__main__":
    cmd, pair = sys.argv[1], Path(sys.argv[2]).resolve()
    sys.stdout.reconfigure(encoding="utf-8")
    {"send": lambda: send(pair, sys.argv[3]), "wait": lambda: wait(pair), "stop": lambda: stop(pair)}[cmd]()
