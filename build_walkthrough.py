#!/usr/bin/env python3
"""Build walkthrough-carreau-carreau.canvas — an interactive canvas presentation
of the rheofit carreau_carreau walkthrough."""
import json
import secrets

def nid():
    return secrets.token_hex(8)

W = 920
X = -460

hero = """# 🧭 Two microstructures, two relaxation times

**`carreau_carreau` on a wormlike-micelle + polymer system** — a rheofit case study.

When a formulation mixes microstructures, the model should too. A temperature-series
story of why one Carreau mode fails on a mixed WLM/polymer surfactant system — and
how the microstructure-informed sum succeeds, with parameters that track temperature
like they mean it.

📖 [Full walkthrough](https://rheofit.readthedocs.io/en/latest/walkthrough-carreau-carreau.html) · 📦 [rheofit](https://github.com/rheopy/rheofit) · 🗃️ [rheodata](https://github.com/rheopy/rheodata)"""

dataset = """## 🧪 The dataset

`caggioni_wlm_polymer_temp_series` from **rheodata** — equilibrium flow curves of a
mixed surfactant system: **wormlike micelles (WLM) + a polymer solution**.

- 7 sweeps: **18, 20, 22, 24, 26, 28 °C — plus a repeat at 18 °C**
- 41 points each, 0.01 → 100 1/s
- the curves carry **at least two distinct relaxation times** — that is exactly what makes them interesting

```python
df18 = rheodata.to_rheofit("caggioni_wlm_polymer_temp_series", "T_18")
res = rheofit.fit(df18, "carreau_carreau", effort="thorough", seed=0)
```"""

model = """## 🤔 The modeling assumption

Decouple the WLM contribution from the polymer contribution — one Carreau mode each,
with **fixed** exponents:

- **WLM → stress plateau** at high shear → Carreau with **n = 0**
- **polymer → shear-thinning**, no plateau → Carreau with **n = 0.5**

`σ = η₀,₁·γ̇·[1+(λ₁·γ̇)²]^(−¼) + η₀,₂·γ̇·[1+(λ₂·γ̇)²]^(−½)`

![WLM and polymer modes feeding the carreau–carreau model](assets/walkthrough/walkthrough_cc_mermaid.svg)"""

fails = """## 📉 One Carreau is not enough — 18 °C

A single Carreau does its honest best: **η₀ = 15.2 Pa·s, λ = 1.50 s, n = 0.61** —
a compromise exponent stuck halfway between the plateau mode (n = 0) and the polymer
mode (n = 0.5).

Reduced χ² = **1.29e-2**, and the residuals trace a systematic S-shape: the model
cannot bend twice.

![Single Carreau vs carreau–carreau at 18 °C, with relative residuals](assets/walkthrough/fig5_cc_vs_carreau_18C.png)"""

wins = """## ✅ `carreau_carreau` at 18 °C

| parameter | value | ± stderr |
|---|---|---|
| η₀,₁ (polymer) | 11.01 Pa·s | 1.7% |
| λ₁ (polymer) | 3.97 s | 6.7% |
| η₀,₂ (WLM) | 5.08 Pa·s | 2.9% |
| λ₂ (WLM) | 0.0454 s | 3.0% |

Reduced χ² = **8.28e-4** — about **15× better** than one Carreau — condition number
11.6: every parameter identified, no degeneracy. The two relaxation times sit ~90×
apart, exactly the separation the data demanded.

![Decomposition into polymer and WLM terms, with viscosity on a twin axis](assets/walkthrough/fig4_cc_decomposition_18C.png)

A slow polymer mode (λ ≈ 4 s) carries the low-shear viscosity; a fast WLM mode
(λ ≈ 0.05 s) flattens into its stress plateau (σ → η₀,₂/λ₂ ≈ 112 Pa) at high shear."""

temperature = """## 🌡️ Across temperatures: the parameters behave

| T / °C | η₀,₁ / Pa·s | λ₁ / s | η₀,₂ / Pa·s | λ₂ / s | Red. χ² (cc) | Red. χ² (1× C.) |
|---|---|---|---|---|---|---|
| 18 | 11.01 | 3.97 | 5.08 | 0.0454 | 8.3e-4 | 1.29e-2 |
| 20 | 9.05 | 3.17 | 3.84 | 0.0316 | 9.8e-4 | 8.2e-3 |
| 22 | 7.54 | 2.37 | 2.78 | 0.0210 | 1.0e-3 | 2.9e-3 |
| 24 | 6.29 | 2.07 | 2.17 | 0.0166 | 1.3e-3 | 1.5e-3 |
| 26 | 5.09 | 1.64 | 1.71 | 0.0136 | 1.0e-3 | 6.8e-4 |
| 28 | 4.16 | 1.33 | 1.37 | 0.0116 | 8.1e-4 | 3.3e-4 |
| 18 ↺ | 10.49 | 3.33 | 4.60 | 0.0405 | 9.6e-4 | 1.0e-2 |

![Carreau–Carreau parameters vs temperature](assets/walkthrough/fig6_cc_params_vs_T.png)

Both relaxation times shorten and both viscosities fall with temperature — clean
thermal softening, separated per microstructure. The 18 °C repeat lands on top of
the first run. Bonus insight: as the WLM contribution weakens, one Carreau becomes
competitive — **the data itself tells you when the second mode stops mattering.**"""

takeaway = """## 💡 Takeaway

Formulations are mixtures of microstructures; their flow curves are mixtures of
relaxation modes. A single-mode model returns a compromise — n = 0.61 describing
neither the micelles nor the polymer. The microstructure-informed sum fits the
physics instead of averaging it, and its parameters move with temperature the way
real material parameters should.

*Dataset: `rheodata:caggioni_wlm_polymer_temp_series` · Fits: `rheofit.fit(..., "carreau_carreau", effort="thorough", seed=0)` · rheofit 1.0.2*"""

back = """[← back to the rheopy ecosystem](https://rheopy.github.io/canvas/)"""

specs = [
    ("hero", hero, 0, 400, "6"),
    ("dataset", dataset, 470, 380, None),
    ("model", model, 920, 640, None),
    ("fails", fails, 1630, 1020, "1"),
    ("wins", wins, 2720, 1040, "4"),
    ("temperature", temperature, 3830, 1180, None),
    ("takeaway", takeaway, 5080, 400, "3"),
    ("back", back, 5550, 120, None),
]

nodes = []
ids = {}
y = 0
for key, text, dy, h, color in specs:
    i = nid()
    ids[key] = i
    node = {"id": i, "x": X, "y": dy, "width": W, "height": h, "type": "text", "text": text}
    if color:
        node["color"] = color
    nodes.append(node)

order = ["hero", "dataset", "model", "fails", "wins", "temperature", "takeaway", "back"]
edges = []
for a, b in zip(order, order[1:]):
    edges.append({
        "id": nid(),
        "fromNode": ids[a], "fromSide": "bottom",
        "toNode": ids[b], "toSide": "top",
    })

nodes.append({
    "id": nid(), "x": X - 100, "y": -120, "width": W + 200, "height": 5920,
    "type": "group", "label": "carreau_carreau walkthrough", "color": "6",
})

canvas = {"nodes": nodes, "edges": edges}
with open("walkthrough-carreau-carreau.canvas", "w") as f:
    json.dump(canvas, f, indent=2, ensure_ascii=False)
print("wrote walkthrough-carreau-carreau.canvas:", len(nodes), "nodes,", len(edges), "edges")
