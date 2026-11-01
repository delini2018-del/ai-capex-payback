"""Figures for the AI capex payback article, from results/results.json."""
import json
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.text as mtext
mtext.Text._preprocess_math = lambda self, s: (s, False)   # dollar signs are money, not maths

R = json.load(open("results/results.json"))
INK, INK2, GRID, BG = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": INK2, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "figure.facecolor": BG, "axes.facecolor": BG})
def title(fig, t, sub):
    fig.text(0.02, 0.965, t, ha="left", va="top", fontsize=15, color=INK, weight="bold")
    fig.text(0.02, 0.905, sub, ha="left", va="top", fontsize=11, color=INK2)

COL = {"MSFT": BLUE, "AMZN": ORANGE, "GOOG": AQUA, "META": YELLOW}
NAME = {"MSFT": "Microsoft", "AMZN": "Amazon", "GOOG": "Alphabet", "META": "Meta"}

# ---------- 1: quarterly capex ----------
Q = R["quarters"]; n = len(Q); x = list(range(n)) + [n + 2]
fig, ax = plt.subplots(figsize=(11, 5.8))
bottom = np.zeros(n + 1)
q3 = R["q3"]; latest = {"MSFT": q3["Microsoft"]["capex_incl_leases"], "AMZN": q3["Amazon"]["capex"], "GOOG": q3["Alphabet"]["capex"], "META": q3["Meta"]["capex"]}
for c in ("AMZN", "MSFT", "GOOG", "META"):
    v = np.array(R["hist"][c] + [latest[c]])
    ax.bar(x, v, bottom=bottom, color=COL[c], width=0.75, label=NAME[c], edgecolor=BG, lw=0.6)
    bottom += v
for i in (0, n - 1, n):
    ax.text(x[i], bottom[i] + 4, f"${bottom[i]:.0f}B", ha="center", fontsize=10.5, color=INK, weight="bold" if i == n else None)
ax.text(n + 0.5, 105, "2026 Q1–Q2\nnot shown", ha="center", fontsize=9, color=INK2)
lab = [q.replace("CY", "").replace(" Q1", "\nQ1") if q.endswith("Q1") else "" for q in Q] + ["2026\nQ3"]
ax.set_xticks(x, lab); ax.set_ylim(0, 235); ax.set_xlim(-0.8, n + 2.8)
ax.set_ylabel("Capital spending per quarter ($ billion)"); ax.grid(axis="y", color=GRID); ax.set_axisbelow(True)
ax.legend(frameon=False, loc="upper left", fontsize=10.5, ncol=4)
title(fig, "Four companies now spend about $200 billion a quarter on buildings and chips",
      "Capital spending incl. finance leases, 2022–2025 from Epoch AI; July–September 2026 from this week's earnings reports")
fig.subplots_adjust(top=0.84, left=0.08, right=0.98, bottom=0.12)
fig.savefig("charts/01_quarterly_capex.png", dpi=200); plt.close(fig)

# ---------- 2: free cash flow ----------
order = ["Microsoft", "Meta", "Alphabet", "Amazon"]
fig, ax = plt.subplots(figsize=(11, 5.2))
vals = [q3[k]["fcf"] for k in order]
cols = [AQUA if v > 0 else ORANGE for v in vals]
y = np.arange(len(order))
ax.barh(y, vals, color=cols, height=0.6)
notes = {"Microsoft": "Jul–Sep 2026 · still positive", "Meta": "Q3 2026 · capex $34.9B > cash from operations $32.8B",
         "Alphabet": "Q3 2026 · second negative quarter in a row", "Amazon": "12 months to Sep 2026 · capex $215.2B > cash from ops $168.3B"}
for yi, k, v in zip(y, order, vals):
    ax.text(v + (0.8 if v > 0 else -0.8), yi, f"{'+' if v > 0 else '−'}${abs(v):.1f}B", va="center", ha="left" if v > 0 else "right", fontsize=11, color=INK, weight="bold")
    ax.text(1.5 if v < 0 else 33, yi, notes[k], va="center", ha="left", fontsize=10, color=INK2)
ax.axvline(0, color=INK2, lw=1)
ax.set_yticks(y, order); ax.invert_yaxis(); ax.set_xlim(-55, 70)
ax.set_xlabel("Free cash flow: cash from operations minus capital spending ($ billion)")
ax.grid(axis="x", color=GRID); ax.set_axisbelow(True)
for s in ("left",): ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
title(fig, "Three of the four spent more cash than their businesses produced",
      "Free cash flow in the latest reported period (Amazon reports it only on a trailing 12-month basis)")
fig.subplots_adjust(top=0.84, left=0.11, right=0.98, bottom=0.13)
fig.savefig("charts/02_free_cash_flow.png", dpi=200); plt.close(fig)

# ---------- 3: required vs actual revenue ----------
fig, ax = plt.subplots(figsize=(11, 5.8))
nr = R["new_rev"]
labels = ["Revenue needed:\n2026 spending only", "Revenue needed:\n2024–2026 build-out", "New revenue this year\n(annualised growth)", "Whole cloud business\n(AWS + Azure + Google Cloud)"]
xs = np.array([0, 1, 2, 3.25])
ax.bar(0, R["req26"], color=INK2, width=0.62); ax.bar(1, R["req_cum"], color=INK, width=0.62)
b = 0
for (k, v), c in zip(nr.items(), (ORANGE, BLUE, AQUA, YELLOW)):
    ax.bar(2, v, bottom=b, color=c, width=0.62, edgecolor=BG, lw=0.6); ax.text(2.34, b + v / 2, k.replace(" (whole company)", " (all ads)"), va="center", fontsize=9.5, color=INK2); b += v
b = 0
for k, c in zip(("AWS", "Azure", "Google Cloud"), (ORANGE, BLUE, AQUA)):
    v = R["run_rate"][k]; ax.bar(3.25, v, bottom=b, color=c, width=0.62, edgecolor=BG, lw=0.6, alpha=0.55); b += v
for xi, v in zip(xs, (R["req26"], R["req_cum"], R["new_total"], R["cloud_run"])):
    ax.text(xi, v + 10, f"${v:.0f}B / yr", ha="center", fontsize=11.5, color=INK, weight="bold")
ax.axhline(R["req_cum"], color=INK, lw=1, ls=":")
ax.set_xticks(xs, labels, fontsize=10.5); ax.set_ylim(0, 660); ax.set_xlim(-0.5, 3.75)
ax.set_ylabel("$ billion per year"); ax.grid(axis="y", color=GRID); ax.set_axisbelow(True)
title(fig, "The build-out needs about $570 billion a year. New revenue is about $210 billion",
      "Revenue needed to cover depreciation (6 years) and an 8% cost of capital at a 60% margin, against Jul–Sep 2026 revenue ×4")
fig.subplots_adjust(top=0.84, left=0.08, right=0.98, bottom=0.15)
fig.savefig("charts/03_required_vs_actual.png", dpi=200); plt.close(fig)

# ---------- 4: sensitivity heatmap (coverage) ----------
G = np.array(R["grid_cum"]); cov = R["new_total"] / G
fig, ax = plt.subplots(figsize=(10, 6))
im = ax.imshow(cov, cmap="Blues", vmin=0, vmax=0.7, aspect="auto")
for i in range(G.shape[0]):
    for j in range(G.shape[1]):
        ax.text(j, i, f"${G[i, j]:.0f}B\n{100 * cov[i, j]:.0f}% covered", ha="center", va="center", fontsize=10,
                color="white" if cov[i, j] > 0.4 else INK)
ax.set_xticks(range(len(R["Ms"])), [f"{int(100 * m)}%" for m in R["Ms"]]); ax.set_yticks(range(len(R["Ls"])), [f"{L} years" for L in R["Ls"]])
ax.set_xlabel("Margin left after running costs (power, staff, networking)"); ax.set_ylabel("How long the chips and servers last")
for s in ax.spines.values(): s.set_visible(False)
ax.add_patch(plt.Rectangle((1.5, 1.5), 1, 1, fill=False, ec=ORANGE, lw=2.5))
title(fig, "Even generous assumptions leave most of the gap open today",
      "Yearly revenue the $1.39T 2024–2026 build-out needs (8% cost of capital), and how much ~$211B of new revenue covers")
fig.subplots_adjust(top=0.84, left=0.15, right=0.97, bottom=0.12)
fig.savefig("charts/04_sensitivity.png", dpi=200); plt.close(fig)
print("ok")
