# Punchcutter for AI agents

Punchcutter is a type foundry: it makes original font families from a text
brief, a filled-in handwriting sheet, a photo of writing, or a mood image.
This file tells any coding agent (Codex, Cursor, Gemini CLI, Copilot, Aider,
Claude Code and others) how to run it.

Codex users can also install it as a skill (`npx skills add byrishi/punchcutter --agent codex`)
and call it with `$punchcutter`.

## Use it

1. Install once: `pip install -r skills/punchcutter/scripts/requirements.txt`
2. Read `skills/punchcutter/SKILL.md` and follow it. It is the full operating
   manual: the menu, the six routes, the commands, the critique loop.
3. Commands are `python skills/punchcutter/scripts/punchcutter.py <command>`:
   `menu`, `presets`, `bases`, `new`, `build`, `glyph`, `sheet`, `read-sheet`, `segment`, `label`, `mcp`, `telemetry`.

If your client supports MCP, run the server instead and use its tools:
`python skills/punchcutter/scripts/punchcutter.py mcp` (stdio), or add `--http` for remote
clients such as ChatGPT. See the README for client configs.

## Rules that matter

- Look at `proof.png` after every build. You need image input for this; if you
  have none, say so and ask the user to check the proof.
- Original designs only. Do not copy commercial typefaces or logos.
- Do not edit files under `build/`; change the spec and rebuild.

## Working on Punchcutter itself

- Engine: `skills/punchcutter/scripts/pc/`. Glyph drawings are in `glyphs_latin.py` and `glyphs_extra.py`.
- Every glyph must produce the same point structure at every weight (variable font compatibility). The tests check this.
- Run `python tests/test_build.py` before committing. Conventional commit messages.
