# Developing and releasing abba-mcp

Users read [README.md](README.md), which ships in the bundle. This file does not (`.mcpbignore`).

## How it works

`src/abba_mcp/__init__.py` is a thin stdio MCP server with no image-analysis logic:

- the first time a Fiji tool is called, it starts the pinned Fiji with jgo (`src/abba_mcp/env/`), detached,
  in `~/.abba-mcp/env` (`ABBA_MCP_HOME`), logging to `~/.abba-mcp/fiji.log`. `startmcp.groovy` starts
  fiji-llm's MCP server on `127.0.0.1:9090`. The start goes on in the background: a call that would wait longer than
  `MAX_WAIT_S` (40 s) fails with "Fiji is starting", and the assistant calls again;
- no call blocks longer than about 40 s: MCP clients abort a request after about 60 s (the TypeScript SDK's
  default), losing the job id it would have returned. fiji-modules caps `wait_seconds` itself;
- it forwards the Fiji tools (`FORWARDED`: fiji-modules' module tools, fiji-llm's window and dialog tools) to
  that server. Before the first call it checks that the Fiji there runs this bundle's ABBA version, and refuses
  otherwise;
- it serves `abba_window_picture` (a Groovy script run through `fiji_module_run`) and the bundled docs
  (`abba_docs_search`, `abba_docs_read`), and builds its MCP instructions from `data/instructions.md`.

The server lists its tools before Fiji runs, so it keeps a copy of the forwarded tools' definitions in
`fiji_tools.json`, generated from Fiji (`build/gen_tools.py`): the Java code (fiji-llm, fiji-modules) stays their
only source. The server only appends one sentence about ABBA to some of them (`NOTES`).

| Path | What |
|---|---|
| `src/abba_mcp/env/jgo.toml` | the pinned environment: ABBA, Fiji, fiji-llm, fiji-modules, overrides, repositories |
| `src/abba_mcp/data/instructions.md` | the MCP instructions (placeholders: version, mode, docs folder) |
| `src/abba_mcp/data/guides/`, `scripting/`, `examples/` | docs written for the assistant |
| `src/abba_mcp/data/commands/` | **generated**: one file per ABBA command (`build/gen_commands.groovy`) |
| `src/abba_mcp/data/environment.md` | what the environment runs, for the assistant |
| `src/abba_mcp/fiji_tools.json`, the `tools` of `manifest.json` | **generated** (`build/gen_tools.py`) |
| `build/check_env.sh` | checks the resolved versions against ABBA's pom, and the bundle version |

Handy: `uv run abba-mcp --version`, `uv run abba-mcp --print-instructions [--headless]`.

## The environment

Everything in `jgo.toml` is a release. ABBA, fiji-llm and fiji-modules are on the SciJava repository only, listed
under `[repositories]`. jgo 3.1 reads that section but resolves from Maven Central only, so the server and
`check_env.sh` pass the repositories to jgo as `-r` options. Without them the environment resolves only on a
machine whose local Maven repository already holds ABBA.

Java is pinned too, in `[java]` (Zulu 21). On its own, jgo runs any Java already installed (`JAVA_HOME`, then
`PATH`) that is at least the version asked, whatever its vendor: a machine with Java 25 on its `PATH` ran Fiji on
it. So the server fetches the pinned JDK itself through cjdk (the cache jgo uses too) and puts it first in
`JAVA_HOME` and `PATH` for jgo. `fiji.log` starts with the Java it chose.

Order matters in `coordinates`: it decides, silently, which version of a shared dependency wins (see the comments
in `jgo.toml`). `check_env.sh` catches the case that matters, ABBA's pins (atlas, biop-tools, image-loaders,
bigdataviewer-playground) losing.

To check that nothing comes from this machine only, resolve with an empty Maven cache:
`jgo --repo-cache <empty folder> -r scijava:https://maven.scijava.org/content/groups/public info deplist`
in a folder holding a copy of `jgo.toml`.

## Versions

The version is ABBA's (`0.25.0`), plus `+N` for a re-release of this server alone (`0.25.0+1`): the docs are for
that ABBA only. It is set in `manifest.json` (`version`, and `display_name`: `ABBA (Fiji) - 0.25.0`, which names the
server and its tools, so that the assistant and the user can tell bundles apart) and `pyproject.toml`, where Python
spells `+1` `.post1` (PyPI refuses local versions) and `-SNAPSHOT` `.dev0`; `check_env.sh` fails if they disagree
with the ABBA pinned in `jgo.toml`.

## Releasing

For a new ABBA version, or new fiji-llm / fiji-modules versions:

1. Set the versions in `src/abba_mcp/env/jgo.toml`, then check that the environment resolves what ABBA declares:
   `build/check_env.sh src/abba_mcp/env <ABBA pom.xml>`.
2. Start that environment's Fiji (for instance through the server's first Fiji call), then:
   - regenerate the command docs: run `build/gen_commands.groovy` (for instance through `fiji_module_run`) with
     `outDir` an empty folder, and copy the result over `src/abba_mcp/data/commands/`. Mention new commands in
     the guides where they belong;
   - regenerate the forwarded tools' definitions and the manifest's tool list: `uv run python build/gen_tools.py`.
3. Update `src/abba_mcp/data/environment.md`, and the version in `manifest.json` and `pyproject.toml`.
   The instructions link the user documentation of the pinned ABBA (`USER_DOCS`,
   `https://abba-documentation.readthedocs.io/en/v<version>/`): check that this version is published there, and
   that the pages `instructions.md` names still exist. The README's link names the version too.
4. Run the example pipeline (`src/abba_mcp/data/examples/abba_demo_pipeline.groovy`).
5. `npx @anthropic-ai/mcpb validate manifest.json`; `npx @anthropic-ai/mcpb pack . abba-mcp-<version>.mcpb` to try
   the bundle locally.
6. Commit, then publish a GitHub release tagged `v<version>` (`gh release create v<version> --generate-notes`): the
   workflow `.github/workflows/release.yml` publishes the package to PyPI (trusted publishing, environment `pypi`)
   and attaches `abba-mcp-<version>.mcpb` to the release. A version reaches PyPI once: a fix is a new version.

Several servers side by side (tests, `build/agent-tests/`): each needs its own `ABBA_MCP_HOME` and `ABBA_MCP_PORT`.
