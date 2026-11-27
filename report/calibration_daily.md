# Daily calibration — the morning card's P(win) against the finals

Each morning the Today card states, per category, the chance of winning it; at the week's intake every stated chance is
scored against the final (won 1, tied 0.5, lost 0; Brier = (p − outcome)², 0 perfect, 0.25 a coin flip). Baseline = the
lead to date as a forecast; skill = baseline − card, positive when the card beats the scoreboard. `scripts/score_week.py`;
`report/calibration_daily.json` is the record and is append-only.

| week | opponent | result | mornings | forecasts | Brier (card) | Brier (lead to date) | skill |
|---|---|---|---|---|---|---|---|
| 1 | MAXEY-MUM OVERDRIVE | 3-6-0 | 4 (+2 missing) | 36 | 0.034 | 0.174 | +0.140 |
| 2 | Looking Cool Joker! | 7-2-0 | 7 | 63 | 0.145 | 0.294 | +0.149 |
| 3 | Podz save the league | 7-2-0 | 7 | 63 | 0.124 | 0.155 | +0.030 |
| 4 | SNOWTIME WHITE WALKERS | 4-5-0 | 6 (+1 missing) | 54 | 0.134 | 0.176 | +0.042 |
| 5 | Thompson Telepathy | 6-3-0 | 7 | 63 | 0.123 | 0.230 | +0.108 |

Reliability, all weeks (a calibrated card has hit rate ≈ mean P in every bin):

| stated P | forecasts | mean P | hit rate |
|---|---|---|---|
| 0.0-0.2 | 56 | 0.07 | 0.07 |
| 0.2-0.4 | 18 | 0.30 | 0.39 |
| 0.4-0.6 | 38 | 0.51 | 0.55 |
| 0.6-0.8 | 58 | 0.71 | 0.69 |
| 0.8-1.0 | 109 | 0.95 | 0.95 |
