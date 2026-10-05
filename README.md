# 🌊 rheopy/canvas

An interactive map of the [rheopy](https://github.com/rheopy) ecosystem, drawn as a
[JSON Canvas](https://jsoncanvas.org) (the open Obsidian standard) and rendered in
the browser with the open-source
[json-canvas-viewer](https://github.com/hesprs/json-canvas-viewer) (MIT).

**Live site:** https://rheopy.github.io/canvas/

## What's here

| File | What it is |
|---|---|
| `ecosystem.canvas` | The map itself — plain JSON, opens in Obsidian too |
| `walkthrough-carreau-carreau.canvas` | A second canvas: the rheofit carreau–carreau walkthrough as an interactive narrative |
| `index.html` | The GitHub Pages site embedding the viewer |
| `viewer/chimp.js` | The viewer, vendored from `json-canvas-viewer@4.3.2` (npm) — no CDN needed |
| `assets/test_clip.mp4` | CaBER test clip, played inline as a video node |
| `assets/snapshots/*.png` | Page snapshots backing the clickable preview nodes |
| `assets/walkthrough/*` | Walkthrough figures + mermaid diagram used by the walkthrough canvas |
| `build_walkthrough.py` | Generator script for the walkthrough canvas (run it, commit the `.canvas` output) |

## The map

- **Center:** the rheopy vision — complete expert workflows, not disconnected tools
- **The loop:** measure → data → model → fit → explore
  (`rheomeasurement` → `rheodata` → `rheomodel` → `rheofit` → `rheolite`)
- **Bundles:** flow curves, CaBER/extensional, oscillatory, engineering flows —
  each wired to the repos that deliver it
- Nodes link out to the repos; the CaBER bundle embeds the filament-thinning
  video right on the canvas

## Multiple canvases

The site serves more than one canvas. Pick one with the `?canvas=` query
parameter — it defaults to the ecosystem map:

- `https://rheopy.github.io/canvas/` — the ecosystem map
- `https://rheopy.github.io/canvas/?canvas=walkthrough-carreau-carreau` —
  the carreau–carreau walkthrough, linked from the rheofit node on the map

To add another canvas: drop a `<name>.canvas` file next to the others,
register it in the `CANVASES` table at the top of `index.html`, and link to
it as `?canvas=<name>`. The header title, subtitle, and `.canvas` download
button follow the active canvas automatically.

## Editing the canvas

`ecosystem.canvas` is just JSON (`nodes` + `edges`, per the
[1.0 spec](https://jsoncanvas.org/spec/1.0/)). Edit it by hand, generate it with a
script, or open it in Obsidian and drag nodes around — the site picks up the
change on the next push to `main`.

To upgrade the vendored viewer: download the tarball from
`https://registry.npmjs.org/json-canvas-viewer/-/json-canvas-viewer-<version>.tgz`
and replace `viewer/chimp.js` with `package/dist/chimp.js`.
