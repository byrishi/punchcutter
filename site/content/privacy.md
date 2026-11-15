---
title: Privacy and usage stats
lede: What Punchcutter counts, why, and how to turn it off in one line.
---

Punchcutter is free and open source. To know whether people actually use it (not just star it), it sends a few **anonymous** events. They never contain your fonts, text, images, file names, prompts or location.

## What is counted

| Event | When |
| --- | --- |
| `installed` | the first time Punchcutter runs on a machine |
| `build_started`, `build_completed`, `build_failed` | a font build, with the route, draft or release, duration and error type |
| `tool_called`, `mcp_started` | the MCP server is used, with the AI client's name (for example Claude Desktop or Cursor) |
| `studio_opened`, `studio_download`, `lab_copy`, `mockup_download` | someone opens or uses a font's Studio app |

Each event carries a random install id made on your machine, the Punchcutter version, your OS family and Python version. There are no person profiles and no IP-based location.

The documentation site counts page views without cookies.

## Turn it off

Any one of these switches it off for good:

```
punchcutter telemetry off
export PUNCHCUTTER_TELEMETRY=0
export DO_NOT_TRACK=1
```

It is already off in CI and in the test suite. Add `"telemetry": false` to a spec to build a Studio with no tracking at all. The code is in [`telemetry.py`](https://github.com/byrishi/punchcutter/blob/main/skills/punchcutter/scripts/pc/telemetry.py).

## Referral codes

Links shared on launch platforms carry `?ref=` (for example `?ref=producthunt`). To credit an install to a source, set `PUNCHCUTTER_REF` once:

```
PUNCHCUTTER_REF=producthunt punchcutter menu
```
