# Agent tests: a user-simulating agent drives Haiku with this bundle

Not shipped (`build/` is in `.mcpbignore`). Used on 2026-10-14 for 3 rounds of 3 pairs.

- `haiku.py`: one Claude Code session per pair, with the Haiku model, no built-in tools, only this bundle's MCP
  server (as a Claude Desktop session), a Desktop-like system prompt and a 60 s tool timeout. Each pair has its own
  Fiji: `pair.json` gives `port` (ABBA_MCP_PORT), `bundle` (an unzipped `.mcpb`) and `headless`.
- `BRIEF.md`: what the user-simulating agent (Opus) is told; replace `<harness folder>` with the folder holding
  `haiku.py` and `pairs/`. Each run gets its own scenario on top.

Do not install new SNAPSHOTs while pairs run: jgo environments hardlink the jars of the local Maven repository,
so a reinstall rewrites them under the running Fijis (NoClassDefFoundError mid-session).
