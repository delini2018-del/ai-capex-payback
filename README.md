# ai-capex-payback

Code and data for the Medium article **"Big Tech Spent More Than It Earned on AI This Quarter. I Did the Payback Math."** by Delini.

How much revenue a year do the AI data centres of Alphabet, Amazon, Meta and Microsoft need to bring in, just to earn back what they cost? And how close is the industry today?

## The model

```
required_revenue_per_year = capex * (1 / useful_life + cost_of_capital) / margin
```

Baseline: 6-year life, 8% cost of capital, 60% margin after running costs. All three are swept.

## Headline results (baseline)

| | $B per year |
|---|---|
| Revenue needed, 2026 capex only ($730B) | 300 |
| Revenue needed, 2024–2026 build-out ($1.39T) | 571 |
| New revenue added over the past year (AWS, Azure, Google Cloud, Meta; Q3 2026 vs Q3 2025, x4) | 211 |
| Whole cloud business of AWS + Azure + Google Cloud (Q3 2026 x4) | 440 |

## Files

- `data/epoch_capex.csv`: quarterly capex 2022–2025 from Epoch AI (https://epoch.ai/data/charts/hyperscaler-capex-trend/stacked_hyperscalers_trend.csv)
- `calc.py`: the payback model and sensitivity sweep. Writes `results/results.json`
- `make_charts.py`: draws the four figures into `charts/`
- `cover/cover.py`: draws the article cover (code-drawn, no AI image generation)
- `ai_capex_payback.ipynb`: the same steps as a Colab notebook

Q3 2026 company figures (capex, cash flow, revenue, guidance) are typed into `calc.py` from the earnings reports cited in the article.

## Run

```
pip install -r requirements.txt
python calc.py
python make_charts.py
```

## Limits

Treats all capex as AI capex, counts only cloud revenue plus Meta's revenue growth, annualises a single quarter, and uses company guidance for 2026. See the article for the full discussion.

MIT licence.
