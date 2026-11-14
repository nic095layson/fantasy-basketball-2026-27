# Forecast accuracy — week by week

Each finished week graded against the box scores and the final scores (`scripts/accuracy_week.py`; `report/accuracy.json` is the record, one row per week, never rewritten). Players with 2+ games in the week.

## Player lines: points per game (projected / actual, bias, MAE, rank correlation)

| week | players | preseason | bias | MAE | rank | in-season | bias | MAE | rank | minutes candidate | bias | MAE | rank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 261 | 13.50 / 11.95 | 13.0% | 3.50 | 0.77 | no snapshot | | |  | no snapshot | | |  |
| 2 | 252 | 13.14 / 11.88 | 10.6% | 3.60 | 0.77 | 12.89 / 11.86 | 8.7% | 3.46 | 0.79 | 12.76 / 11.86 | 7.6% | 3.34 | 0.81 |
| 3 | 255 | 13.06 / 11.63 | 12.3% | 3.77 | 0.73 | 12.61 / 11.55 | 9.1% | 3.39 | 0.79 | 12.50 / 11.55 | 8.2% | 3.30 | 0.80 |

Switch rule (D-ML-1, pre-committed 2026-10-27): the minutes candidate replaces nothing until its MAE beats the in-season line's on PTS, REB and AST in 3 of 4 consecutive graded weeks, on the owner's word.

## Player lines: threes made per game (projected / actual, bias, MAE, rank correlation)

| week | players | in-season | bias | MAE | rank | threes-split candidate | bias | MAE | rank |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 261 | no snapshot | | |  | no snapshot | | |  |
| 2 | 252 | 1.42 / 1.37 | 3.3% | 0.67 | 0.68 | no snapshot | | |  |
| 3 | 255 | 1.39 / 1.28 | 9.1% | 0.61 | 0.76 | no snapshot | | |  |

Switch rule (D-TS-1, pre-committed 2026-11-12): the threes-split candidate replaces nothing until its MAE on threes made beats the in-season line's in 3 of 4 consecutive graded weeks, on the owner's word.

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
| 3 | 0.00 | 0.00 | 3 / 29 | 0.10 |
| 3 | 0.75 | 0.75 | 69 / 119 | 0.58 |
| 3 | 0.79 | 0.79 | 7 / 8 | 0.88 |
| 3 | 0.88 | 0.88 | 774 / 1009 | 0.77 |

## Forecasts

| week | your P(win) | result | daily card Brier vs lead | league matchups scored | league Brier (flat 3.5) | league Brier (real games) |
|---|---|---|---|---|---|---|
| 1 | 0.606 | 3 cats | 0.034 vs 0.174 | 0 | – | – |
| 2 | 0.576 | 7 cats | 0.145 vs 0.294 | 0 | – | – |
| 3 | 0.847 | 7 cats | 0.124 vs 0.155 | 6 | 0.222 | 0.191 |

Switch rule (D-RG-1, pre-committed 2026-10-27): the real-games forecast replaces the flat one only after a lower Brier over at least 4 consecutive graded weeks, on the owner's word.
