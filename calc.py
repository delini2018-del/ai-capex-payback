"""Payback math for Big Tech's AI build-out.

Question: how much revenue per year would the data centres need to bring in, just to earn back what they cost?

For a pile of capital spending C, the yearly amount that must be recovered is
    depreciation (C / L, useful life L years) + a return on the money tied up (C * r, cost of capital r).
That is a cost, so the revenue needed is that cost divided by the share of each revenue dollar
that is left after running costs (power, staff, networking, software): the margin m.
    required_revenue = C * (1/L + r) / m
Defaults: L = 6 years (Microsoft and Alphabet depreciate servers over 6 years, Meta over 5.5, Amazon over 5),
r = 8%, m = 60%. All three are swept below.
Inputs are reported company figures (see README and the article's references).
"""
import json, csv
import numpy as np

# ---- capex history (Epoch AI, broad capex incl. finance leases, $M, calendar quarters) ----
rows = list(csv.DictReader(open("data/epoch_capex.csv")))
cos = ["MSFT", "AMZN", "GOOG", "META"]
quarters = [r["Calendar Quarter"] for r in rows]
hist = {c: [float(r[f"{c} Broad CapEx ($M)"]) / 1000 for r in rows] for c in cos}
annual = {}
for y in ("2022", "2023", "2024", "2025"):
    annual[y] = round(sum(hist[c][i] for c in cos for i, q in enumerate(quarters) if q.startswith("CY" + y)), 1)

# ---- latest quarter (calendar Q3 2026), $B, as reported this week ----
q3 = {  # capex, operating cash flow, free cash flow
    "Alphabet":  dict(capex=51.4, ocf=42.3, fcf=-9.1, basis="Q3 2026"),
    "Microsoft": dict(capex=39.4, capex_incl_leases=45.2, ocf=58.0, fcf=18.6, basis="Jul-Sep 2026 (cash capex; $45.2B incl. leases)"),
    "Meta":      dict(capex=34.9, ocf=32.8, fcf=-2.1, basis="Q3 2026 (incl. finance-lease principal)"),
    "Amazon":    dict(capex=77.3, ocf=None, fcf=-42.4, basis="trailing 12 months to Sep 2026 (OCF 168.3, capex 215.2)"),
}
# ---- 2026 full-year capex plans, $B (midpoint of guidance) ----
plan26 = {"Amazon": 220, "Alphabet": 200, "Microsoft": 170, "Meta": 140}
C26 = sum(plan26.values())
C_cum = annual["2024"] + annual["2025"] + C26          # the 2024-2026 build-out

# ---- revenue the build-out is meant to earn, $B per quarter, Jul-Sep 2026 vs a year earlier ----
rev = {"AWS": (46.0, 33.0), "Azure": (33.2, 33.2 / 1.48), "Google Cloud": (30.7, 30.7 / 2.03), "Meta (whole company)": (64.6, 64.6 / 1.26)}
run_rate = {k: round(4 * v[0], 1) for k, v in rev.items()}
new_rev = {k: round(4 * (v[0] - v[1]), 1) for k, v in rev.items()}
cloud_run = sum(run_rate[k] for k in ("AWS", "Azure", "Google Cloud"))
new_total = sum(new_rev.values())

def need(C, L=6, r=0.08, m=0.6):
    return C * (1 / L + r) / m

base = dict(L=6, r=0.08, m=0.6)
req26, req_cum = need(C26), need(C_cum)
# margin at which this year's new revenue would cover this year's capex
m_be = C26 * (1 / 6 + 0.08) / new_total

Ls = [4, 5, 6, 7, 8]; Ms = [0.4, 0.5, 0.6, 0.7, 0.8]
grid = [[round(need(C_cum, L, 0.08, m), 0) for m in Ms] for L in Ls]
grid26 = [[round(need(C26, L, 0.08, m), 0) for m in Ms] for L in Ls]
rs = {f"{int(r*100)}%": round(need(C_cum, 6, r, 0.6), 0) for r in (0.0, 0.04, 0.08, 0.12)}

# Sequoia-style check (David Cahn, 2024): data-centre spend x2 for gross margin -> revenue needed
seq_style = round(C26 * 2, 0)

R = dict(quarters=quarters, hist=hist, annual=annual, q3=q3, plan26=plan26, C26=C26, C_cum=round(C_cum, 1),
         run_rate=run_rate, new_rev=new_rev, cloud_run=round(cloud_run, 1), new_total=round(new_total, 1),
         req26=round(req26, 1), req_cum=round(req_cum, 1), m_breakeven=round(m_be, 3),
         Ls=Ls, Ms=Ms, grid_cum=grid, grid26=grid26, r_sweep=rs, sequoia_style=seq_style,
         cover26=round(new_total / req26, 3), cover_cum=round(new_total / req_cum, 3), cloud_cover_cum=round(cloud_run / req_cum, 3))
json.dump(R, open("results/results.json", "w"), indent=1)
for k in ("annual", "C26", "C_cum", "run_rate", "new_rev", "cloud_run", "new_total", "req26", "req_cum", "m_breakeven",
          "cover26", "cover_cum", "cloud_cover_cum", "r_sweep", "sequoia_style"):
    print(k, R[k])
print("grid_cum (rows L=4..8, cols m=.4..0.8)"); [print(L, g) for L, g in zip(Ls, grid)]
