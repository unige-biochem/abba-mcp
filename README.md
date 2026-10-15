# abba-mcp: ABBA for AI assistants (experimental)

Lets an AI assistant drive [ABBA](https://abba-documentation.readthedocs.io) (Aligning Big Brains and Atlases) to
register brain sections to an atlas. The assistant runs ABBA's commands, looks at what they produced, and once the
result is right saves the session (`.abba` state file) and a Groovy script that replays every step.

You can follow along and take over at any time: by default, ABBA's window opens on your screen as usual.

It is an [MCP](https://modelcontextprotocol.io) server, so it is not tied to one assistant: it works with any
application (MCP client) that can start a local MCP server, and any model it offers that calls tools and reads
images (the assistant looks at pictures of your slices).

## Install

Follow the [installation page](https://abba-documentation.readthedocs.io/en/stable/installation/installation.html#install-assistant)
of the ABBA documentation: VS Code (one click), Claude Desktop and Claude Code, Codex, and any other MCP client;
the first run, running without a window, privacy, and what to do if something goes wrong.

In short: install [uv](https://docs.astral.sh/uv/getting-started/installation/), then register the command
`uvx abba-mcp` as a local (stdio) MCP server in your application, or click:

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_ABBA_MCP-0098FF?logo=visualstudiocode)](https://vscode.dev/redirect/mcp/install?name=abba&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22abba-mcp%22%5D%7D)

The version is the ABBA version it runs (`0.25.0`), with `.post1`, `.post2`... for a fix of this server alone.
Questions about ABBA itself: the [ABBA documentation](https://abba-documentation.readthedocs.io/en/v0.25.0/) of this
version and the [image.sc forum](https://forum.image.sc/tag/abba).

Developing or releasing this bundle: see [DEVELOPMENT.md](DEVELOPMENT.md).
