# ABBA (Fiji) for AI assistants (experimental)

Lets an AI assistant drive [ABBA](https://abba-documentation.readthedocs.io) (Aligning Big Brains and Atlases) to
register brain sections to an atlas. The assistant runs ABBA's commands, looks at what they produced, and once the
result is right saves the session (`.abba` state file) and a Groovy script that replays every step.

You can follow along and take over at any time: by default, ABBA's window opens on your screen as usual.

It is an [MCP](https://modelcontextprotocol.io) server, so it is not tied to one assistant: it works with any
application (MCP client) that can start a local MCP server, and any model it offers that calls tools and reads
images (the assistant looks at pictures of your slices).

## Install

You need [uv](https://docs.astral.sh/uv/getting-started/installation/) and an internet connection for the first
run. Java, Fiji and ABBA are downloaded for you.

Get `abba-fiji-<version>.mcpb` and unzip it (it is a zip file) into a folder of your choice, then add the server to
your application.

### Any MCP client

The server talks MCP over stdio (protocol versions 2024-11-05 to 2025-11-25). Register it with:

| | |
|---|---|
| command | `uv` |
| arguments | `run --directory <unzipped folder> abba-fiji` |
| environment (optional) | `ABBA_FIJI_HEADLESS=true` for no window (see below) |

Most applications take this JSON, in their own settings file:

```json
{
  "mcpServers": {
    "abba": {
      "command": "uv",
      "args": ["run", "--directory", "<unzipped folder>", "abba-fiji"]
    }
  }
}
```

On Windows, write the folder with forward slashes (`C:/Users/me/abba-fiji`) or doubled backslashes.

The server gives the assistant its rules and points it to its documentation through the MCP *instructions*.
Some applications do not pass them on: if the assistant seems not to know how to proceed, ask it to read
`guides/abba.md` with the `abba_docs_read` tool first.

### Claude

- **Claude Desktop**: no need to unzip, double-click the `.mcpb`.
- **Claude Code**:
  ```
  claude mcp add abba -- uv run --directory <unzipped folder> abba-fiji
  ```

### OpenAI

- **Codex** (CLI, IDE extension), and the **ChatGPT desktop app**, which shares Codex's configuration:
  ```
  codex mcp add abba -- uv run --directory <unzipped folder> abba-fiji
  ```
  or, in `~/.codex/config.toml`:
  ```toml
  [mcp_servers.abba]
  command = "uv"
  args = ["run", "--directory", "<unzipped folder>", "abba-fiji"]
  ```
- **ChatGPT on the web** connects to remote MCP servers only: it cannot start this one.

### Others

- **VS Code** (GitHub Copilot): in `.vscode/mcp.json`, the JSON above with `"servers"` instead of `"mcpServers"`.
- **Cursor**, **Gemini CLI**, and most others: the JSON above, in their MCP settings.

## First run

The first time the assistant uses Fiji, the server downloads Java, Fiji and ABBA, then starts them: allow several
minutes; later starts are much faster. DeepSlice, Elastix and atlases are also downloaded the first time they are
needed.

## With or without a window

- **Window** (default): ABBA opens its window on your screen. You see what the assistant does, can select slices
  for it, and can take over.
- **Headless**: no window, for servers and remote machines. The assistant shows you snapshots instead, and
  manual registrations are not available. Set the environment variable `ABBA_FIJI_HEADLESS=true` for the server:
  `"env": {"ABBA_FIJI_HEADLESS": "true"}` next to `"args"` in the JSON, `-e ABBA_FIJI_HEADLESS=true` before `--`
  for `claude mcp add`, `--env ABBA_FIJI_HEADLESS=true` for `codex mcp add`. In Claude Desktop, turn on
  *Run Fiji without a window* in the extension's settings.

## Privacy

What the assistant looks at (snapshots of your slices, the session state, file names) is sent to your AI
provider, as for anything else you show it. Fiji itself is only reachable from your own computer (port 9090 on
127.0.0.1).

## Versions

The bundle's version is the ABBA version it runs (`0.24.1`), with `+1`, `+2`... for a fix of the bundle alone.
Every machine gets the same Fiji, ABBA and plugins, and the assistant's documentation is written for exactly that
version. Your own Fiji installation is not used or modified.

## Troubleshooting

- **"The Fiji on port 9090 runs ..."**: another Fiji with an MCP server is already running (your own, or one
  started by another version of this bundle). Close it and ask again.
- **Fiji does not start**: its log is `fiji.log` in `~/.abba-fiji` (set `ABBA_FIJI_HOME` to use another folder).
- Questions about ABBA itself: the [ABBA documentation](https://abba-documentation.readthedocs.io/en/v0.24.1/) of this version and the
  [image.sc forum](https://forum.image.sc/tag/abba).

Developing or releasing this bundle: see [DEVELOPMENT.md](DEVELOPMENT.md).
