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
| `index.html` | The GitHub Pages site embedding the viewer |
| `viewer/chimp.js` | The viewer, vendored from `json-canvas-viewer@4.3.2` (npm) — no CDN needed |
| `assets/test_clip.mp4` | CaBER test clip, played inline as a video node |

## The map

- **Center:** the rheopy vision — complete expert workflows, not disconnected tools
- **The loop:** measure → data → model → fit → explore
  (`rheomeasurement` → `rheodata` → `rheomodel` → `rheofit` → `rheolite`)
- **Bundles:** flow curves, CaBER/extensional, oscillatory, engineering flows —
  each wired to the repos that deliver it
- Nodes link out to the repos; the CaBER bundle embeds the filament-thinning
  video right on the canvas

## Editing the canvas

`ecosystem.canvas` is just JSON (`nodes` + `edges`, per the
[1.0 spec](https://jsoncanvas.org/spec/1.0/)). Edit it by hand, generate it with a
script, or open it in Obsidian and drag nodes around — the site picks up the
change on the next push to `main`.

To upgrade the vendored viewer: download the tarball from
`https://registry.npmjs.org/json-canvas-viewer/-/json-canvas-viewer-<version>.tgz`
and replace `viewer/chimp.js` with `package/dist/chimp.js`.
