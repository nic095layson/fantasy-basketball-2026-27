# Forecast accuracy — week by week

Each finished week graded against the box scores and the final scores (`scripts/accuracy_week.py`; `report/accuracy.json` is the record, one row per week, never rewritten). Players with 2+ games in the week.

## Player lines: points per game (projected / actual, bias, MAE, rank correlation)

| week | players | preseason | bias | MAE | rank | in-season | bias | MAE | rank | minutes candidate | bias | MAE | rank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 261 | 13.50 / 11.95 | 13.0% | 3.50 | 0.77 | no snapshot | | |  | no snapshot | | |  |
| 2 | 252 | 13.14 / 11.88 | 10.6% | 3.60 | 0.77 | 12.89 / 11.86 | 8.7% | 3.46 | 0.79 | 12.76 / 11.86 | 7.6% | 3.34 | 0.81 |

Switch rule (D-ML-1, pre-committed 2026-10-27): the minutes candidate replaces nothing until its MAE beats the in-season line's on PTS, REB and AST in 3 of 4 consecutive graded weeks, on the owner's word.

## Availability: share of team games played, by the tier the simulator assumes

| week | tier | assumed | played / team games | share |
|---|---|---|---|---|
| 1 | 0.00 | 0.00 | 0 / 22 | 0.00 |
| 1 | 0.75 | 0.75 | 55 / 96 | 0.57 |
| 1 | 0.79 | 0.79 | 4 / 5 | 0.80 |
| 1 | 0.88 | 0.88 | 670 / 809 | 0.83 |
| 2 | 0.00 | 0.00 | 0 / 26 | 0.00 |
| 2 | 0.75 | 0.75 | 59 / 111 | 0.53 |
| 2 | 0.79 | 0.79 | 6 / 6 | 1.00 |
| 2 | 0.88 | 0.88 | 727 / 918 | 0.79 |

## Forecasts

| week | your P(win) | result | daily card Brier vs lead | league matchups scored | league Brier (flat 3.5) | league Brier (real games) |
|---|---|---|---|---|---|---|
| 1 | 0.606 | 3 cats | 0.034 vs 0.174 | 0 | – | – |
| 2 | 0.576 | 7 cats | 0.145 vs 0.294 | 0 | – | – |

Switch rule (D-RG-1, pre-committed 2026-10-27): the real-games forecast replaces the flat one only after a lower Brier over at least 4 consecutive graded weeks, on the owner's word.
