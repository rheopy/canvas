#!/usr/bin/env python3
"""Build using-rheopy.canvas — the rheopy API in one picture.

A communication canvas: measure -> data -> model -> fit -> explore.
Each package does one job; this canvas shows the calls that connect them.
All code snippets are verified against the package READMEs / walkthroughs.

Code samples are emitted as hand-colored HTML (spans), not fenced blocks,
so they look right in any viewer without relying on automatic syntax
highlighting. The span classes (ck/cs/cc/cn/cd/cb) are styled by the
.codeblock CSS in index.html.
"""
import html
import json
import re
import secrets

def nid():
    return secrets.token_hex(8)

# --- tiny Python tokenizer -> colored spans (mirrors the prototype viewer) ---
PY_KW = set("False None True and as assert async await break class continue def "
            "del elif else except finally for from global if import in is lambda "
            "nonlocal not or pass raise return try while with yield".split())
PY_BI = set("print len range str int float bool list dict set tuple abs min max "
            "sum sorted enumerate zip map filter isinstance type repr input open "
            "super round".split())
TOKEN_RE = re.compile(
    r"(#[^\n]*)"
    r"|([fFrRbB]{0,2}'''(?:[^\\]|\\.)*?'''"
    r"|[fFrRbB]{0,2}\"\"\"(?:[^\\]|\\.)*?\"\"\""
    r"|[fFrRbB]{0,2}'(?:[^'\\\n]|\\.)*'"
    r"|[fFrRbB]{0,2}\"(?:[^\"\\\n]|\\.)*\")"
    r"|(&[a-zA-Z]+;|&#[0-9]+;)"
    r"|(@[A-Za-z_]\w*)"
    r"|\b(\d[\d_]*(?:\.\d+)?(?:[eE][+-]?\d+)?j?)\b"
    r"|\b([A-Za-z_]\w*)"
)

def hl_py(src):
    src = html.escape(src, quote=False)
    out, last = [], 0
    for m in TOKEN_RE.finditer(src):
        out.append(src[last:m.start()])
        tok = m.group(0)
        if m.group(1):
            out.append('<span class="cc">' + tok + "</span>")
        elif m.group(2):
            out.append('<span class="cs">' + tok + "</span>")
        elif m.group(3):
            out.append(tok)
        elif m.group(4):
            out.append('<span class="cd">' + tok + "</span>")
        elif m.group(5):
            out.append('<span class="cn">' + tok + "</span>")
        elif m.group(6):
            w = m.group(6)
            if w in PY_KW:
                out.append('<span class="ck">' + w + "</span>")
            elif w in PY_BI:
                out.append('<span class="cb">' + w + "</span>")
            else:
                out.append(w)
        else:
            out.append(tok)
        last = m.end()
    out.append(src[last:])
    return "".join(out)

def codeblock(src, lang="python"):
    return ('<div class="codeblock"><span class="codelang">' + lang + "</span>\n"
            "<pre><code>" + hl_py(src) + "</code></pre>\n</div>")

# --- card texts ---
hero = """# 🗺️ Using rheopy — the API in one picture

The rheopy way: **measure → data → model → fit → explore**.

Each package does exactly one job, and they snap together: **rheodata** serves
curated datasets, **rheomodel** holds the constitutive equations, **rheofit** runs
the nonlinear regression, **rheolite** is the notebook + browser playground."""

install = """## 📦 Install

```bash
pip install rheopy-rheodata rheopy-rheomodel rheofit
```"""

rheodata = ("""## 🗃️ rheodata — data in

Curated rheology datasets with provenance, measurement records, and citations.

"""
+ codeblock('''import rheodata

rheodata.list()                             # every dataset, one row each
rheodata.search(material="carbopol")        # substring filters
rheodata.info("caggioni_pg_carbopol_2pct")  # summary + DOI link

ds = rheodata.load("caggioni_pg_carbopol_2pct")
ds.df.head()                                # tidy DataFrame
rheodata.plot("caggioni_pg_carbopol_2pct")   # figure''')
+ "\n")

bridge = ("""## 🔧 The bridge — data → fit

"""
+ codeblock('''df = rheodata.to_rheofit("caggioni_pg_carbopol_2pct",
                         sample="carbopol_2pct")
# -> "Shear rate / 1/s" and "Stress / Pa",
#    exactly what rheofit.fit expects''')
+ "\n")

rheomodel = ("""## 🧮 rheomodel — pick a model

Nine flow-curve models as pure functions — equations, bounds, verified citations.

- **Yield stress:** `herschel_bulkley`, `bingham`, `casson`
- **Microstructure-informed:** `tc`, `tc_carreau`, `tccc`
- **No yield stress:** `power_law`, `carreau`, `carreau_carreau`

"""
+ codeblock('''import rheomodel

hb = rheomodel.get_model("herschel_bulkley")
sigma = hb.equation(gamma_dot, sigma_y=20.0, K=10.0, n=0.6)
# hb.CITATION - hb.PARAM_INFO - hb.get_equation_latex()''')
+ "\n")

rheofit = ("""## 🎯 rheofit — fit

Nonlinear regression: physics-informed starts, ladder seeding, multi-start
global search (`effort`: fast / normal / thorough).

"""
+ codeblock('''import rheofit

res = rheofit.fit(df, "carreau_carreau", effort="thorough", seed=0)
# res.params - fitted values with uncertainties''')
+ "\n")

explore = """## 🔬 Explore — rheolite

Notebooks, the browser fit app, and the interactive model explorers.

🌊 [Fit app](https://rheopy.github.io/rheofit/) — upload data or pick a rheodata
dataset, choose a model, fit in the browser · 📓 [rheolite](https://github.com/rheopy/rheolite)"""

back = """[← back to the rheopy ecosystem](https://rheopy.github.io/canvas/)"""

# (key, text, x, y, w, h)
specs = [
    ("hero", hero, -660, 0, 1280, 220),
    ("install", install, -660, 260, 1280, 180),
    ("rheodata", rheodata, -660, 480, 600, 360),
    ("rheomodel", rheomodel, -20, 480, 600, 360),
    ("bridge", bridge, -660, 880, 600, 240),
    ("rheofit", rheofit, -660, 1160, 1280, 300),
    ("explore", explore, -660, 1500, 1280, 200),
    ("back", back, -660, 1740, 600, 100),
]

nodes = []
ids = {}
for key, text, x, y, w, h in specs:
    i = nid()
    ids[key] = i
    nodes.append({"id": i, "x": x, "y": y, "width": w, "height": h,
                  "type": "text", "text": text})

edges = []
def edge(a, b, a_side="bottom", b_side="top", label=None):
    e = {"id": nid(), "fromNode": ids[a], "fromSide": a_side,
         "toNode": ids[b], "toSide": b_side}
    if label:
        e["label"] = label
    edges.append(e)

edge("hero", "install")
edge("install", "rheodata", label="data path")
edge("install", "rheomodel", label="model path")
edge("rheodata", "bridge")
edge("bridge", "rheofit", label="data in")
edge("rheomodel", "rheofit", label="model in")
edge("rheofit", "explore")
edge("explore", "back")

nodes.append({
    "id": nid(), "x": -760, "y": -120, "width": 1440, "height": 2080,
    "type": "group", "label": "using rheopy", "color": "6",
})

canvas = {"nodes": nodes, "edges": edges}
with open("using-rheopy.canvas", "w") as f:
    json.dump(canvas, f, indent=2, ensure_ascii=False)
print("wrote using-rheopy.canvas:", len(nodes), "nodes,", len(edges), "edges")
