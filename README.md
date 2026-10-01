# ABBA (Fiji) for AI assistants (experimental, codename sextant)

An MCP bundle: your assistant can drive ABBA (Aligning Big Brains and Atlases) to register brain sections to an
atlas, look at the result, and save the session as a replayable Groovy pipeline.

- Install: double-click the `.mcpb` (Claude Desktop), or unzip it and run
  `claude mcp add abba -- uv run --directory <folder> abba-mcp` (Claude Code). Needs `uv`.
- The first Fiji tool call starts a pinned Fiji with ABBA (downloaded by jgo on first use, several minutes).
  Fiji's MCP server listens on 127.0.0.1:9090 only.
- Docs for the assistant: `src/abba_mcp/data/` (instructions, guides, one file per command, examples).
- What the assistant sees (snapshots, slice state) goes to your AI provider.
