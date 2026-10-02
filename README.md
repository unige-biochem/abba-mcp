# ABBA (Fiji) for AI assistants (experimental, codename sextant)

An MCP bundle: your assistant can drive ABBA (Aligning Big Brains and Atlases) to register brain sections to an
atlas, look at the result, and save the session as a replayable Groovy pipeline.

- Install: double-click the `.mcpb` (Claude Desktop), or unzip it and run
  `claude mcp add abba -- uv run --directory <folder> abba-mcp` (Claude Code). Needs `uv`.
- The first Fiji tool call starts a pinned Fiji with ABBA (downloaded by jgo on first use, several minutes).
  Fiji's MCP server listens on 127.0.0.1:9090 only.
- Docs for the assistant: `src/abba_mcp/data/` (instructions, guides, one file per command, examples).
- What the assistant sees (snapshots, slice state) goes to your AI provider.
- Versions: the bundle's version is the ABBA version it runs. The server reports it (MCP server info,
  `abba-mcp --version`, the instructions), and refuses a Fiji already running on the port with another ABBA.

**Works only where `sc.fiji:fiji-llm` and `ch.unige.biochem:fiji-modules` are in the local Maven repository**:
neither is published yet. Everything else in `env/jgo.toml` is a release.

## Releasing for a new ABBA version

1. Set the ABBA version in `src/abba_mcp/env/jgo.toml`, then check that the environment resolves what ABBA
   declares: `build/check_env.sh src/abba_mcp/env <ABBA pom.xml>`.
2. Regenerate the command docs: run `build/gen_commands.groovy` in that environment's Fiji (for instance through
   `fiji_module_run`) with `outDir` an empty folder, and copy the result over `src/abba_mcp/data/commands/`.
   Mention new commands in the guides where they belong.
3. Update `src/abba_mcp/data/environment.md`, and the version in `manifest.json` and `pyproject.toml`: **the
   bundle's version is ABBA's** (`0.24.0`), plus `+N` for a re-release of the bundle alone (`0.24.0+1`).
   `check_env.sh` fails otherwise.
4. Run the example pipeline (`src/abba_mcp/data/examples/abba_demo_pipeline.groovy`), then
   `npx @anthropic-ai/mcpb validate manifest.json` and `npx @anthropic-ai/mcpb pack . abba-fiji-<version>.mcpb`.
