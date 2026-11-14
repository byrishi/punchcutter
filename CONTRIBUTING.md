# Contributing

Thanks for helping. Punchcutter is small on purpose, so a short note before a big change saves everyone time: open an issue first.

## Set up

```bash
git clone https://github.com/byrishi/punchcutter && cd punchcutter
pip install -r skills/punchcutter/scripts/requirements.txt mcp
python tests/test_build.py
```

## Where things live

| Path | What |
| --- | --- |
| `skills/punchcutter/SKILL.md` | the skill's instructions |
| `skills/punchcutter/scripts/pc/` | the engine |
| `glyphs_latin.py`, `glyphs_extra.py` | letter drawings |
| `brand.py` | colours, type and the mark used by every output |
| `site/content/` | docs pages; `python tools/build_site.py` rebuilds `docs/` |

## Rules

- Every glyph must have the same point structure at every weight. The tests check this.
- Look at the proof after changing a drawing: `python skills/punchcutter/scripts/punchcutter.py glyph examples/burin-grotesk.json a g R`.
- Use colours from `brand.py`, never new ones.
- Conventional commit messages (`feat:`, `fix:`, `docs:`).
- Original designs only. No traced or copied typefaces.
