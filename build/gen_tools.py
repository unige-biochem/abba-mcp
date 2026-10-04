"""Writes the definitions of the Fiji tools this bundle forwards, as Fiji serves them, and the manifest's tool list.

The server lists its tools before Fiji runs, so it needs a copy of Fiji's definitions; this makes the copy, so that
the Java code (fiji-modules, fiji-llm) stays their only source. Run it whenever a pinned version changes, against a
Fiji started from this bundle's environment (src/abba_fiji/env), from the bundle folder:
    uv run python build/gen_tools.py [http://127.0.0.1:9090/mcp]
Fails if Fiji lacks a forwarded tool, or if a note in the server refers to no forwarded tool.
"""
import asyncio
import json
import re
import sys
from pathlib import Path

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

import abba_fiji

ROOT = Path(__file__).resolve().parent.parent
URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:9090/mcp"


def first_sentence(text: str) -> str:
    return re.split(r"(?<!e\.g)(?<!i\.e)\.\s", text, maxsplit=1)[0].rstrip(".")


async def main():
    async with streamablehttp_client(URL) as (read, write, _), ClientSession(read, write) as session:
        await session.initialize()
        served = {t.name: t for t in (await session.list_tools()).tools}
    missing = [n for n in abba_fiji.FORWARDED if n not in served]
    orphans = [n for n in abba_fiji.NOTES if n not in abba_fiji.FORWARDED]
    if missing or orphans:
        sys.exit(f"Fiji at {URL} lacks {missing}; notes for tools not forwarded: {orphans}")

    tools = [{"name": n, "description": served[n].description, "inputSchema": served[n].inputSchema}
             for n in abba_fiji.FORWARDED]
    abba_fiji.FIJI_TOOLS_FILE.write_text(json.dumps(tools, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    listed = [(t["name"], first_sentence(t["description"])) for t in tools]
    listed += [(n, first_sentence(spec[0])) for n, spec in abba_fiji.BUNDLE_TOOLS.items()]
    block = ",\n".join(f'    {{ "name": {json.dumps(n)}, "description": {json.dumps(d, ensure_ascii=False)} }}' for n, d in listed)
    manifest = ROOT / "manifest.json"
    text, count = re.subn(r'"tools": \[.*?\n  \]', f'"tools": [\n{block}\n  ]', manifest.read_text(encoding="utf-8"),
                          flags=re.DOTALL)
    if count != 1:
        sys.exit("manifest.json: no tools list found")
    manifest.write_text(text, encoding="utf-8")
    print(f"{abba_fiji.FIJI_TOOLS_FILE.name}: {len(tools)} tools from {URL}; manifest.json: {len(listed)} tools")


asyncio.run(main())
