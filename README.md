# abba-mcp: ABBA for AI assistants (experimental)

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

### Claude

- **Claude Desktop**: download `abba-mcp-<version>.mcpb` from the
  [releases](https://github.com/unige-biochem/abba-mcp/releases) and double-click it.
- **Claude Code**:
  ```
  claude mcp add abba -- uvx abba-mcp
  ```

### VS Code (GitHub Copilot)

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_ABBA_MCP-0098FF?logo=visualstudiocode)](https://vscode.dev/redirect/mcp/install?name=abba&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22abba-mcp%22%5D%7D)

Or, from a terminal: `code --add-mcp '{"name":"abba","command":"uvx","args":["abba-mcp"]}'`.

### OpenAI

- **Codex** (CLI, IDE extension), and the **ChatGPT desktop app**, which shares Codex's configuration:
  ```
  codex mcp add abba -- uvx abba-mcp
  ```
- **ChatGPT on the web** connects to remote MCP servers only: it cannot start this one.

### Any other MCP client

The server talks MCP over stdio (protocol versions 2024-11-05 to 2025-11-25): command `uvx`, arguments
`abba-mcp`. Most applications (Cursor, Gemini CLI...) take this JSON in their MCP settings:

```json
{
  "mcpServers": {
    "abba": {
      "command": "uvx",
      "args": ["abba-mcp"]
    }
  }
}
```

`uvx abba-mcp` runs the latest release; `uvx abba-mcp@0.25.0` a given one (the version is the ABBA it runs).

The server gives the assistant its rules and points it to its documentation through the MCP *instructions*.
Some applications do not pass them on: if the assistant seems not to know how to proceed, ask it to read
`guides/abba.md` with the `abba_docs_read` tool first.

## First run

The first time the assistant uses Fiji, the server downloads Java, Fiji and ABBA, then starts them: allow several
minutes; later starts are much faster. Meanwhile the assistant is told that Fiji is starting, and tries again. DeepSlice, Elastix and atlases are also downloaded the first time they are
needed.

## With or without a window

- **Window** (default): ABBA opens its window on your screen. You see what the assistant does, can select slices
  for it, and can take over.
- **Headless**: no window, for servers and remote machines. The assistant shows you snapshots instead, and
  manual registrations are not available. Set the environment variable `ABBA_MCP_HEADLESS=true` for the server:
  `"env": {"ABBA_MCP_HEADLESS": "true"}` next to `"args"` in the JSON, `-e ABBA_MCP_HEADLESS=true` before `--`
  for `claude mcp add`, `--env ABBA_MCP_HEADLESS=true` for `codex mcp add`. In Claude Desktop, turn on
  *Run Fiji without a window* in the extension's settings.

## Privacy

What the assistant looks at (snapshots of your slices, the session state, file names) is sent to your AI
provider, as for anything else you show it. Fiji itself is only reachable from your own computer (port 9090 on
127.0.0.1).

## Versions

The version is the ABBA version it runs (`0.25.0`), with `.post1`, `.post2`... for a fix of this server alone.
Every machine gets the same Fiji, ABBA and plugins, and the assistant's documentation is written for exactly that
version. Your own Fiji installation is not used or modified.

## Troubleshooting

- **"The Fiji on port 9090 runs ..."**: another Fiji with an MCP server is already running (your own, or one
  started by another version of this bundle). Close it and ask again.
- **Fiji does not start**: its log is `fiji.log` in `~/.abba-mcp` (set `ABBA_MCP_HOME` to use another folder).
- Questions about ABBA itself: the [ABBA documentation](https://abba-documentation.readthedocs.io/en/v0.25.0/) of this version and the
  [image.sc forum](https://forum.image.sc/tag/abba).

Developing or releasing this bundle: see [DEVELOPMENT.md](DEVELOPMENT.md).
