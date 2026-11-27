# Category grades — every matchup's pre-week category forecast against the finals

Each recorded chance that a team wins a category, scored on the week's final line (`scripts/category_grade.py`; rebuilt from the forecast records and `data/weeks` on every run). Brier: 0 is perfect, 0.25 is a coin flip. Favourite right: of the forecasts that favoured a side in an untied category, how many that side won, beside the mean chance the kit gave it.

| category | flat: n | Brier | favourite right | stated | real games: n | Brier | favourite right | stated |
|---|---|---|---|---|---|---|---|---|
| FG% | 18 | 0.241 | 12 of 18 | 0.65 | 18 | 0.239 | 12 of 18 | 0.65 |
| FT% | 18 | 0.153 | 13 of 18 | 0.71 | 18 | 0.150 | 13 of 18 | 0.70 |
| 3PTM | 18 | 0.187 | 14 of 18 | 0.78 | 18 | 0.183 | 14 of 18 | 0.82 |
| PTS | 18 | 0.190 | 14 of 18 | 0.66 | 18 | 0.143 | 13 of 18 | 0.71 |
| REB | 18 | 0.231 | 11 of 18 | 0.69 | 18 | 0.218 | 13 of 18 | 0.68 |
| AST | 18 | 0.203 | 11 of 18 | 0.70 | 18 | 0.182 | 13 of 18 | 0.68 |
| ST | 18 | 0.202 | 14 of 18 | 0.68 | 18 | 0.209 | 13 of 18 | 0.71 |
| BLK | 18 | 0.214 | 13 of 18 | 0.68 | 18 | 0.195 | 12 of 18 | 0.72 |
| TO | 18 | 0.247 | 11 of 18 | 0.67 | 18 | 0.229 | 11 of 18 | 0.67 |
| **all** | 162 | 0.208 | 113 of 162 | 0.69 | 162 | 0.194 | 114 of 162 | 0.70 |

flat: weeks 3, 4, 5.
real games: weeks 3, 4, 5.

Small samples: one week is 54 forecasts, 6 per category. Read a category as weak only when it stays above the coin flip over several weeks.
