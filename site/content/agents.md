---
title: Claude, MCP and other agents
lede: Punchcutter runs as a skill, an MCP server or a plain command line tool, so any capable AI can drive it.
---

## As a Claude skill

The skill is the most complete experience. It opens with the menu, runs each stage, looks at its own proofs, and finishes by publishing the Studio inside the chat. Install it from [Getting started](getting-started.html).

The skill's operating manual is [SKILL.md](https://github.com/byrishi/punchcutter/blob/main/skills/punchcutter/SKILL.md). It is plain markdown, so you can read exactly what Claude is told to do.

## As an MCP server

```bash
pip install "punchcutter[mcp] @ git+https://github.com/byrishi/punchcutter"
punchcutter mcp          # stdio server
```

| Tool | What it does |
| --- | --- |
| `menu` | the five routes and the working method |
| `presets` | all presets and design parameters |
| `new_font` | write a font spec from a brief |
| `update_design` | change parameters, weights or the custom glyph file |
| `build_font` | run the pipeline; returns the stage log and the proof image |
| `inspect_glyphs` | close-up image of letters at every weight |
| `handwriting_sheet` | write the printable sheets |
| `read_sheet_photos` | photos of filled sheets to a font project |
| `find_letters` | quick photo, step 1: numbered image of the characters |
| `label_letters` | quick photo, step 2: name them and make the project |

Tools that make images return them to the model, so a client with vision can check its proofs the same way the skill does.

### Client configs

**Claude Desktop** (`claude_desktop_config.json`), **Cursor** (`.cursor/mcp.json`), **Windsurf**, **VS Code** (`.vscode/mcp.json`):

```json
{
  "mcpServers": {
    "punchcutter": { "command": "punchcutter", "args": ["mcp"] }
  }
}
```

**Claude Code**:

```bash
claude mcp add punchcutter -- punchcutter mcp
```

If `punchcutter` is not on the client's path, use the full path to it, or `python` with `["/path/to/skills/punchcutter/scripts/punchcutter.py", "mcp"]`.

## ChatGPT

ChatGPT only talks to remote servers, so run Punchcutter over HTTP:

```bash
punchcutter mcp --http --port 8000 --public-url https://YOUR-PUBLIC-ADDRESS
```

| Option | What it does |
| --- | --- |
| `--http` | serve Streamable HTTP at `/mcp` instead of stdio |
| `--port`, `--host` | where to listen (use `--host 0.0.0.0` in a container) |
| `--public-url` | the address clients reach; used to build download links |
| `--workdir` | the one folder all files live in (default `./punchcutter-work`) |

In this mode the server keeps every file inside the work folder, accepts photos as `http(s)` URLs, and returns the proof, Studio and font zip as links it serves itself under `/files/`. Add it in ChatGPT under Settings, Apps & Connectors, Advanced, Developer mode, Create, with the address ending in `/mcp`. A `Dockerfile` is included for permanent hosting.

## Codex

Codex reads the same skill folder; `agents/openai.yaml` gives it a name, icon and default prompt. Install with `npx skills add byrishi/punchcutter --agent codex` or `$skill-installer`, or add the MCP server with `codex mcp add punchcutter -- punchcutter mcp`. See [Getting started](getting-started.html).

## Gemini CLI, Copilot, Aider

Open the agent in a clone of the repository. [AGENTS.md](https://github.com/byrishi/punchcutter/blob/main/AGENTS.md) points it at the skill manual and the commands. The one hard requirement is image input: the method depends on looking at proofs.

## Working method, for any agent

1. Offer the menu unless the route is clear.
2. Build a draft and look at `proof.png`.
3. Fix what the [critique checklist](critique.html) finds. Rebuild. At least two rounds.
4. Build the release and check that QA passed.
5. Hand over the proof, the Studio and the fonts.
