#!/usr/bin/env python3
"""Build a single-file offline viewer for a .canvas file.

The offline file embeds the EXACT same viewer JavaScript the online site uses
(viewer/chimp.js, byte-identical), so online and offline render identically --
no separate viewer codebase to drift out of sync. The canvas JSON,
markdown-referenced images, and the video attachment are inlined as well, so
the output needs no network at all: open it from disk, from SharePoint, or
anywhere a browser runs.

Usage:
    python3 build_offline.py using-rheopy.canvas [-o using-rheopy-offline.html]
    python3 build_offline.py walkthrough-carreau-carreau.canvas --title "custom"

Title/subtitle default to the CANVASES registry in index.html (single source
of truth); override with --title / --sub.
"""
import base64
import json
import mimetypes
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
CHIMP = ROOT / "viewer" / "chimp.js"
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")
WARN_BYTES = 8 * 1024 * 1024


def registry_meta(name):
    """Read title/sub for a canvas from the CANVASES table in index.html."""
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    m = re.search(r"'" + re.escape(name) + r"':\s*\{\s*file:\s*'[^']*',\s*"
                  r"title:\s*'([^']*)',\s*sub:\s*'([^']*)',", html)
    if m:
        return m.group(1), m.group(2)
    return name, ""


def data_uri(path):
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def inline_images(data, base):
    inlined = []

    def as_data_uri(src):
        if src.startswith(("data:", "http://", "https://", "#")):
            return src
        p = (base / src).resolve()
        if p.is_file():
            uri = data_uri(p)
            inlined.append((src, len(uri)))
            return uri
        return src

    for node in data.get("nodes", []):
        if node.get("type") == "text" and node.get("text"):
            node["text"] = IMG_RE.sub(
                lambda m: m.group(0).replace(m.group(1), as_data_uri(m.group(1)), 1),
                node["text"],
            )
    return inlined


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<style>
  html, body {{ margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden;
               font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
  #viewer {{ width: 100%; height: 100%; }}
  #brand {{
    position: fixed; top: 16px; left: 16px; z-index: 10;
    background: rgba(255,255,255,.88); backdrop-filter: blur(6px);
    border: 1px solid #e2e2e2; border-radius: 12px; padding: 10px 14px;
    box-shadow: 0 2px 12px rgba(0,0,0,.08); max-width: 320px;
  }}
  #brand h1 {{ margin: 0; font-size: 17px; font-weight: 700; }}
  #brand p  {{ margin: 4px 0 0; font-size: 12.5px; color: #555; }}
  #brand .row {{ display: flex; gap: 8px; margin-top: 8px; }}
  #brand button, #brand a.btn {{
    font-size: 12.5px; padding: 5px 10px; border-radius: 8px;
    border: 1px solid #d5d5d5; background: #fff; cursor: pointer;
    color: #222; text-decoration: none;
  }}
  #brand button:hover, #brand a.btn:hover {{ background: #f4f4f4; }}
  body.dark #brand {{ background: rgba(30,30,34,.88); border-color: #3a3a3f; }}
  body.dark #brand h1 {{ color: #f0f0f0; }}
  body.dark #brand p {{ color: #aaa; }}
  body.dark #brand button, body.dark #brand a.btn {{
    background: #2a2a2e; border-color: #444; color: #eee;
  }}
  body.dark #brand button:hover, body.dark #brand a.btn:hover {{ background: #35353b; }}
  /* hand-colored code blocks (same classes as the online site) */
  #viewer .codeblock {{ position: relative; margin: 10px 0; }}
  #viewer .codeblock pre {{ margin: 0; }}
  #viewer .codelang {{
    position: absolute; top: 6px; right: 10px; font-size: 10px; color: #9ca3af;
    text-transform: uppercase; letter-spacing: .08em; pointer-events: none;
  }}
  #viewer .ck {{ color: #7c3aed; font-weight: 600; }}
  #viewer .cs {{ color: #047857; }}
  #viewer .cc {{ color: #9ca3af; font-style: italic; }}
  #viewer .cn {{ color: #b45309; }}
  #viewer .cd {{ color: #2563eb; }}
  #viewer .cb {{ color: #0e7490; }}
  body.dark #viewer .ck {{ color: #c4b5fd; }}
  body.dark #viewer .cs {{ color: #6ee7b7; }}
  body.dark #viewer .cc {{ color: #7d8590; }}
  body.dark #viewer .cn {{ color: #fbbf24; }}
  body.dark #viewer .cd {{ color: #93c5fd; }}
  body.dark #viewer .cb {{ color: #67e8f9; }}
</style>
</head>
<body>
<div id="brand">
  <h1>{title}</h1>
  <p>{sub}</p>
  <div class="row">
    <button id="themeBtn" title="Toggle light / dark">&#x1F319; dark</button>
    <a class="btn" href="https://github.com/rheopy/canvas" target="_blank" rel="noopener">&#x2B22; repo</a>
    <button id="dlBtn" title="Download the .canvas file">&#x2913; .canvas</button>
  </div>
</div>
<div id="viewer"></div>
<script id="chimp-src" type="text/plain">{chimp}</script>
<script id="canvas-json" type="application/json">{canvas}</script>
<script type="module">
// The viewer below is byte-identical to the online site's viewer/chimp.js,
// loaded from the embedded copy above: same code, same experience, no network.
const chimpSrc = document.getElementById('chimp-src').textContent;
const chimp = await import(URL.createObjectURL(
  new Blob([chimpSrc], {{ type: 'text/javascript' }})));
const {{ JSONCanvasViewer, parser, Minimap, Controls }} = chimp;
const canvasData = JSON.parse(document.getElementById('canvas-json').textContent);

const viewer = new JSONCanvasViewer(
  {{
    container: document.getElementById('viewer'),
    canvas: canvasData,
    parser,
    attachments: {{ 'assets/test_clip.mp4': '{video}' }},
    theme: 'light',
  }},
  [Minimap, Controls]
);

const btn = document.getElementById('themeBtn');
btn.addEventListener('click', () => {{
  const next = viewer.options.theme === 'dark' ? 'light' : 'dark';
  viewer.changeTheme(next);
  document.body.classList.toggle('dark', next === 'dark');
  btn.innerHTML = next === 'dark' ? '&#x2600;&#xFE0F; light' : '&#x1F319; dark';
}});
document.getElementById('dlBtn').addEventListener('click', () => {{
  const blob = new Blob([JSON.stringify(canvasData, null, 2)],
    {{ type: 'application/json' }});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = '{name}.canvas';
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 5000);
}});
</script>
</body>
</html>
"""


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    canvas_path = pathlib.Path(args[0])
    if not canvas_path.is_file():
        print(f"not found: {canvas_path}", file=sys.stderr)
        return 1
    rest = args[1:]
    out = None
    title = sub = None
    i = 0
    while i < len(rest):
        if rest[i] == "-o" and i + 1 < len(rest):
            out, i = pathlib.Path(rest[i + 1]), i + 2
        elif rest[i] == "--title" and i + 1 < len(rest):
            title, i = rest[i + 1], i + 2
        elif rest[i] == "--sub" and i + 1 < len(rest):
            sub, i = rest[i + 1], i + 2
        else:
            i += 1
    if out is None:
        out = canvas_path.with_name(canvas_path.stem + "-offline.html")

    name = canvas_path.stem
    if title is None or sub is None:
        reg_title, reg_sub = registry_meta(name)
        title = title or reg_title
        sub = sub if sub is not None else reg_sub

    if not CHIMP.is_file():
        print(f"viewer not found: {CHIMP}", file=sys.stderr)
        return 1
    chimp = CHIMP.read_text(encoding="utf-8")
    assert "</script" not in chimp, "chimp.js contains </script -- cannot inline safely"
    assert "<script" not in chimp, "chimp.js contains <script -- cannot inline safely"

    data = json.loads(canvas_path.read_text(encoding="utf-8"))
    inlined = inline_images(data, canvas_path.parent)

    video = ""
    clip = ROOT / "assets" / "test_clip.mp4"
    if clip.is_file():
        video = data_uri(clip)
        print(f"  inlined assets/test_clip.mp4 (+{len(video) // 1024} KB base64)")

    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    payload = payload.replace("</script", "<\\/script")  # keep the JSON script tag intact

    def esc(s):
        return (s.replace("&", "&amp;").replace("<", "&lt;")
                 .replace(">", "&gt;").replace('"', "&quot;"))

    page = TEMPLATE.format(
        title=esc(title), sub=esc(sub), name=name,
        chimp=chimp, canvas=payload, video=video,
    )
    out.write_text(page, encoding="utf-8")

    size = out.stat().st_size
    print(f"wrote {out} ({size / 1024:.0f} KB, "
          f"{len(data.get('nodes', []))} cards, {len(data.get('edges', []))} links)")
    for src, n in inlined:
        print(f"  inlined {src} (+{n // 1024} KB base64)")
    if size > WARN_BYTES:
        print("  NOTE: over ~8 MB -- consider hosted image URLs instead.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
