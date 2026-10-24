# Daily calibration — the morning card's P(win) against the finals

Each morning the Today card states, per category, the chance of winning it; at the week's intake every stated chance is
scored against the final (won 1, tied 0.5, lost 0; Brier = (p − outcome)², 0 perfect, 0.25 a coin flip). Baseline = the
lead to date as a forecast; skill = baseline − card, positive when the card beats the scoreboard. `scripts/score_week.py`;
`report/calibration_daily.json` is the record and is append-only.

| week | opponent | result | mornings | forecasts | Brier (card) | Brier (lead to date) | skill |
|---|---|---|---|---|---|---|---|
| 1 | MAXEY-MUM OVERDRIVE | 3-6-0 | 2 (+4 missing) | 18 | 0.041 | 0.181 | +0.140 |

Reliability, all weeks (a calibrated card has hit rate ≈ mean P in every bin):

| stated P | forecasts | mean P | hit rate |
|---|---|---|---|
| 0.0-0.2 | 9 | 0.08 | 0.00 |
| 0.2-0.4 | 2 | 0.30 | 0.00 |
| 0.4-0.6 | 1 | 0.49 | 0.00 |
| 0.6-0.8 | 2 | 0.73 | 1.00 |
| 0.8-1.0 | 4 | 0.91 | 1.00 |
