---
title: Getting started
lede: Install Punchcutter in the tool you already use. Then ask for a font.
---

Every route needs Python 3.10 or newer. Punchcutter installs its own font libraries; nothing else is required.

## Claude Code

As a plugin, which adds the skill and the `/punchcutter` command:

```
/plugin marketplace add byrishi/punchcutter
/plugin install punchcutter@punchcutter
```

As a plain skill:

```bash
npx skills add byrishi/punchcutter
```

By hand:

```bash
git clone https://github.com/byrishi/punchcutter
mkdir -p ~/.claude/skills && cp -r punchcutter/skills/punchcutter ~/.claude/skills/
pip install -r ~/.claude/skills/punchcutter/scripts/requirements.txt
```

Then type `/punchcutter`, or just say "make me a font".

## Claude app (web, desktop, mobile)

1. Download [punchcutter.skill](https://github.com/byrishi/punchcutter/releases/latest/download/punchcutter.skill).
2. In Claude, open Settings, then Skills, and upload the file. Code execution must be turned on.
3. Start a chat: "make me a font".

Claude installs the libraries on first use. When the font is done, the Studio opens right inside the chat.

## Claude Desktop, Cursor, Windsurf, VS Code

These connect through MCP. Install the package with the MCP extra:

```bash
pip install "punchcutter[mcp] @ git+https://github.com/byrishi/punchcutter"
```

Add it to the client's MCP config (`claude_desktop_config.json`, `.cursor/mcp.json`, `.vscode/mcp.json` and so on):

```json
{
  "mcpServers": {
    "punchcutter": { "command": "punchcutter", "args": ["mcp"] }
  }
}
```

Claude Code can add the same server in one line:

```bash
claude mcp add punchcutter -- punchcutter mcp
```

See [Claude, MCP and other agents](agents.html) for the tool list.

## ChatGPT

ChatGPT connects to remote MCP servers in developer mode (paid plans, on the web). Run Punchcutter as a web server and give ChatGPT its address.

Start the server and open a tunnel to it:

```bash
pip install "punchcutter[mcp] @ git+https://github.com/byrishi/punchcutter"
cloudflared tunnel --url http://localhost:8000      # or: ngrok http 8000
punchcutter mcp --http --public-url https://YOUR-TUNNEL-ADDRESS
```

To host it permanently instead, deploy the repository's `Dockerfile` to Render, Railway or Fly and set `PUNCHCUTTER_PUBLIC_URL` to the app's address.

Then connect ChatGPT:

1. Open Settings, then Apps & Connectors, then Advanced, and turn on Developer mode.
2. Choose Create, paste `https://YOUR-TUNNEL-ADDRESS/mcp`, and set authentication to none.
3. In a chat, pick Punchcutter from the Developer mode tools and say "make me a font".

ChatGPT gets the proof as an image and the Studio and font zip as download links. For the photo routes, give it a link to the photo. Anyone with the address can use the server, so keep the tunnel address to yourself.

## Codex

As a skill, from your terminal:

```bash
npx skills add byrishi/punchcutter --agent codex
pip install -r ~/.codex/skills/punchcutter/scripts/requirements.txt
```

Or inside Codex: `$skill-installer install https://github.com/byrishi/punchcutter/tree/main/skills/punchcutter`. Restart Codex, then type `$punchcutter`.

As an MCP server:

```bash
codex mcp add punchcutter -- punchcutter mcp
```

or in `~/.codex/config.toml`:

```toml
[mcp_servers.punchcutter]
command = "punchcutter"
args = ["mcp"]
```

## Gemini CLI, Copilot, Aider

Clone the repository and open your agent in it. The [AGENTS.md](https://github.com/byrishi/punchcutter/blob/main/AGENTS.md) file tells it how to run the foundry.

```bash
git clone https://github.com/byrishi/punchcutter && cd punchcutter
pip install -r skills/punchcutter/scripts/requirements.txt
```

Then ask: "Follow AGENTS.md and make me a rounded friendly font called Pomelo." The agent must be able to view images, because it checks its own proofs.

## No AI at all

The engine is a normal command line tool.

```bash
pip install "git+https://github.com/byrishi/punchcutter"
punchcutter new "My Sans" --preset humanist --weights 300,400,700
punchcutter build MySans.json
```

The [CLI reference](cli.html) lists every command.

## Platform notes

| System | Note |
| --- | --- |
| macOS | Proof images and sheets need Cairo: `brew install cairo` |
| Windows | Use Python from python.org; everything installs with pip |
| Linux | Install `libcairo2` from your package manager if proofs fail |
| Claude app | Code execution must be on in Settings |

## Your first font

```
> a calm grotesque for a fintech app, three weights, call it Ledger
```

Punchcutter answers with its stages, shows you a proof, revises it, and ends with the Studio, the font files and a short list of next moves. That is the whole loop.
