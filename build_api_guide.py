#!/usr/bin/env python3
"""Build using-rheopy.canvas — the rheopy API in one picture.

A communication canvas: measure -> data -> model -> fit -> explore.
Each package does one job; this canvas shows the calls that connect them.
All code snippets are verified against the package READMEs / walkthroughs.
"""
import json
import secrets

def nid():
    return secrets.token_hex(8)

hero = """# 🗺️ Using rheopy — the API in one picture

The rheopy way: **measure → data → model → fit → explore**.

Each package does exactly one job, and they snap together: **rheodata** serves
curated datasets, **rheomodel** holds the constitutive equations, **rheofit** runs
the nonlinear regression, **rheolite** is the notebook + browser playground."""

install = """## 📦 Install

```bash
pip install rheopy-rheodata rheopy-rheomodel rheofit
```"""

rheodata = """## 🗃️ rheodata — data in

Curated rheology datasets with provenance, measurement records, and citations.

```python
import rheodata

rheodata.list()                               # every dataset, one row each
rheodata.search(material="carbopol")          # substring filters
rheodata.info("caggioni_pg_carbopol_2pct")    # summary + DOI link

ds = rheodata.load("caggioni_pg_carbopol_2pct")
ds.df.head()                                  # tidy DataFrame
rheodata.plot("caggioni_pg_carbopol_2pct")     # experiment-appropriate figure
```"""

bridge = """## 🔧 The bridge — data → fit

```python
df = rheodata.to_rheofit("caggioni_pg_carbopol_2pct",
                         sample="carbopol_2pct")
# → DataFrame with "Shear rate / 1/s" and "Stress / Pa",
#   exactly the shape rheofit.fit expects
```"""

rheomodel = """## 🧮 rheomodel — pick a model

Nine flow-curve models as pure functions — equations, bounds, verified citations.

- **Yield stress:** `herschel_bulkley`, `bingham`, `casson`
- **Microstructure-informed:** `tc`, `tc_carreau`, `tccc`
- **No yield stress:** `power_law`, `carreau`, `carreau_carreau`

```python
import rheomodel

hb = rheomodel.get_model("herschel_bulkley")
sigma = hb.equation(gamma_dot, sigma_y=20.0, K=10.0, n=0.6)
# hb.CITATION, hb.PARAM_INFO, hb.get_equation_latex()
```"""

rheofit = """## 🎯 rheofit — fit

Nonlinear regression with physics-informed starts, ladder seeding, and
multi-start global search (`effort`: fast / normal / thorough).

```python
import rheofit

res = rheofit.fit(df, "carreau_carreau", effort="thorough", seed=0)
# res.params — fitted values with uncertainties
```"""

explore = """## 🔬 Explore — rheolite

Notebooks, the browser fit app, and the interactive model explorers.

🌊 [Fit app](https://rheopy.github.io/rheofit/) — upload data or pick a rheodata
dataset, choose a model, fit in the browser · 📓 [rheolite](https://github.com/rheopy/rheolite)"""

back = """[← back to the rheopy ecosystem](https://rheopy.github.io/canvas/)"""

# (key, text, x, y, w, h)
specs = [
    ("hero", hero, -1010, 0, 1920, 380),
    ("install", install, -1010, 450, 1920, 220),
    ("rheodata", rheodata, -1010, 740, 920, 680),
    ("rheomodel", rheomodel, 0, 740, 920, 680),
    ("bridge", bridge, -1010, 1490, 920, 400),
    ("rheofit", rheofit, -1010, 1960, 1920, 480),
    ("explore", explore, -1010, 2510, 1920, 340),
    ("back", back, -1010, 2920, 920, 120),
]

nodes = []
ids = {}
for key, text, x, y, w, h in specs:
    i = nid()
    ids[key] = i
    nodes.append({"id": i, "x": x, "y": y, "width": w, "height": h,
                  "type": "text", "text": text})

def edge(a, b, a_side="bottom", b_side="top", label=None):
    e = {"id": nid(), "fromNode": ids[a], "fromSide": a_side,
         "toNode": ids[b], "toSide": b_side}
    if label:
        e["label"] = label
    edges.append(e)

edges = []
edge("hero", "install")
edge("install", "rheodata", label="data path")
edge("install", "rheomodel", label="model path")
edge("rheodata", "bridge")
edge("bridge", "rheofit", label="data in")
edge("rheomodel", "rheofit", label="model in")
edge("rheofit", "explore")
edge("explore", "back")

nodes.append({
    "id": nid(), "x": -1110, "y": -120, "width": 2120, "height": 3230,
    "type": "group", "label": "using rheopy", "color": "6",
})

canvas = {"nodes": nodes, "edges": edges}
with open("using-rheopy.canvas", "w") as f:
    json.dump(canvas, f, indent=2, ensure_ascii=False)
print("wrote using-rheopy.canvas:", len(nodes), "nodes,", len(edges), "edges")
