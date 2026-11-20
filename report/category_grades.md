# Category grades — every matchup's pre-week category forecast against the finals

Each recorded chance that a team wins a category, scored on the week's final line (`scripts/category_grade.py`; rebuilt from the forecast records and `data/weeks` on every run). Brier: 0 is perfect, 0.25 is a coin flip. Favourite right: of the forecasts that favoured a side in an untied category, how many that side won, beside the mean chance the kit gave it.

| category | flat: n | Brier | favourite right | stated | real games: n | Brier | favourite right | stated |
|---|---|---|---|---|---|---|---|---|
| FG% | 12 | 0.202 | 8 of 12 | 0.68 | 12 | 0.203 | 8 of 12 | 0.67 |
| FT% | 12 | 0.111 | 10 of 12 | 0.70 | 12 | 0.118 | 10 of 12 | 0.70 |
| 3PTM | 12 | 0.220 | 9 of 12 | 0.80 | 12 | 0.205 | 9 of 12 | 0.84 |
| PTS | 12 | 0.210 | 8 of 12 | 0.68 | 12 | 0.149 | 8 of 12 | 0.71 |
| REB | 12 | 0.232 | 7 of 12 | 0.71 | 12 | 0.211 | 9 of 12 | 0.70 |
| AST | 12 | 0.192 | 8 of 12 | 0.69 | 12 | 0.212 | 7 of 12 | 0.67 |
| ST | 12 | 0.227 | 9 of 12 | 0.69 | 12 | 0.220 | 9 of 12 | 0.71 |
| BLK | 12 | 0.130 | 11 of 12 | 0.67 | 12 | 0.113 | 10 of 12 | 0.72 |
| TO | 12 | 0.278 | 6 of 12 | 0.67 | 12 | 0.209 | 9 of 12 | 0.65 |
| **all** | 108 | 0.200 | 76 of 108 | 0.70 | 108 | 0.182 | 79 of 108 | 0.71 |

flat: weeks 3, 4.
real games: weeks 3, 4.

Small samples: one week is 54 forecasts, 6 per category. Read a category as weak only when it stays above the coin flip over several weeks.
