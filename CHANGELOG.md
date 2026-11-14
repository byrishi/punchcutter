# Changelog

All notable changes to Punchcutter. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions follow [Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-11-14

### Added
- Handwriting route: printable sheet with corner markers and drop-out guides; photo is squared up, traced, measured and turned into a complete font.
- Quick photo route: find, number and trace characters from a photo of any writing, including plain paper.
- Studio: a self-contained HTML app shipped with every font (tester, glyph inspector, install guide, download).
- MCP server for Claude Desktop, Claude Code, Cursor, Windsurf, VS Code and Codex (stdio), and for ChatGPT developer mode (Streamable HTTP with download links).
- Codex skill metadata, Claude Code plugin manifest and `/punchcutter` command, `AGENTS.md` for other agents.
- Docs site with guides, gallery and live Studios.
- `pip install` packaging with `punchcutter` and `punchcutter-mcp` commands, and a `Dockerfile` for hosting.

### Changed
- Brand moved to one token source shared by every output; meadow palette.

## [1.0.0] - 2026-11-13

### Added
- Parametric font engine: stroke-based drawing, eight presets, about 300 Latin glyphs.
- Automatic spacing, 2D class kerning, OpenType features (kern, case, tnum, zero, ss01).
- Variable, TTF, OTF and WOFF2 output with QA checks, proof sheets and UFO sources.
- Claude skill with critique loop and five example families.

[1.1.0]: https://github.com/byrishi/punchcutter/releases/tag/v1.1.0
[1.0.0]: https://github.com/byrishi/punchcutter/commits/main
