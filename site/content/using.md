---
title: Use your font
lede: What is in the box, how to install it on every system, and how to use it in design apps and on the web.
---

Every route ends with the same release folder and its Studio. In the Claude app the Studio opens in the chat and the font downloads as a zip. In a terminal it lands in `build/<Family>/`.

## What you get

Inside `build/<Family>/`:

| File | What it is |
| --- | --- |
| `fonts/studio.html` | the font's own app; open it in any browser, works offline |
| `fonts/otf/`, `fonts/ttf/` | desktop fonts, one file per weight |
| `fonts/variable/` | one file with every weight (drawn families only) |
| `fonts/webfonts/`, `fonts/<Family>.css` | WOFF2 files and ready `@font-face` rules |
| `fonts/README.md` | how to use it, with the license you chose |
| `proof.png` | the proof sheet |
| `report.md` | every stage and every quality check |
| `sources/` | UFO masters and a designspace for Glyphs, FontLab or RoboFont |
| `design.json` | the exact settings used, to rebuild or remix |

The zip from the Studio's Download button holds the fonts, CSS and README in one folder named after the family. The install steps below use that folder.

## The Studio

Open `studio.html`, or [try one now](fonts/PomeloRound/studio.html). It has:

- **Tester**: type anything, change size, weight, tracking, line height, case and colours, switch OpenType features, and compare against Helvetica, Georgia or Times.
- **Design lab**: sliders for weight, width, softness and more, live in the browser. Copy the settings back to Punchcutter to bake them into a new release.
- **Waterfall and weights**: every size and every weight at once.
- **Glyphs**: every character; click one to inspect it.
- **Kerning and languages**: the pairs that were kerned, and the languages it covers.
- **Specs**: files, quality checks and features.
- **Install**: step-by-step guides for each system and app, and the download button.

## Install on your computer

**Mac**: open the `otf` folder, select every file, double-click and choose Install. The font appears in every app after a restart of that app.

**Windows**: open the `otf` or `ttf` folder, select every file, right-click and choose Install (or "Install for all users").

**Linux**:

```bash
mkdir -p ~/.local/share/fonts
cp MyFont/ttf/*.ttf ~/.local/share/fonts/
fc-cache -f
```

Install either the static files or the variable file, not both, so apps do not show the font twice.

## Design apps

| App | How |
| --- | --- |
| Figma | install on your computer, then restart Figma (desktop app, or the font helper in the browser). Org plans can upload it as a shared font. |
| Canva | Brand Kit, then Brand fonts, then Upload a font, and choose the `otf` files (Canva Pro, Teams or Education). |
| Word, Pages, Keynote | install on your computer; it appears in the font menu. |
| Photoshop, Illustrator, Affinity | install on your computer; the variable file gives a live weight slider. |
| Google Docs | cannot load your own font files. Use it in Word or on the web instead. |

## On the web

Copy the `webfonts` folder and `<Family>.css` into your site, then:

```html
<link rel="stylesheet" href="/fonts/MyFont.css">
<style>
  body { font-family: "My Font", system-ui, sans-serif; }
  h1   { font-weight: 700; }
</style>
```

Variable families take any weight from the lightest to the heaviest: `font-weight: 560` works.

In Next.js, use `next/font/local`:

```js
import localFont from "next/font/local";
export const myFont = localFont({ src: "./fonts/MyFont[wght].woff2", weight: "300 800" });
```

Turn features on with CSS, for example tabular figures in a table:

```css
td { font-variant-numeric: tabular-nums; }
.alt { font-feature-settings: "ss01"; }   /* the other form of a */
```

## Change it later

Go back to the same chat, or the same folder, and say what you want: "bolder", "a bit wider", "tighter spacing", "redo the g", "add a 900 weight", or for handwriting "cleaner" or "keep it messy". Punchcutter changes the spec and builds a new release. The version number goes up, so you can tell the files apart.

In a terminal, edit the spec and run `punchcutter build` again. [Design parameters](parameters.html) lists every setting.

## Share it

You own fonts you make. The license in the spec is written into every file: Punchcutter suggests the SIL Open Font License if you want others to use it freely, or "All rights reserved" to keep it to yourself. Send the zip, or host the `studio.html` page so people can try the font before they download it.
