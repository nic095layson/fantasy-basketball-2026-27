# Fits of the hand-set constants — proposals only

Each Monday the finished weeks are fitted (`scripts/fit_constants.py`); a record is never rewritten. A proposal needs 4 finished weeks. Nothing here changes the engine or the registry: the owner decides any swap.

## TEAM_WEEK_SHOCK (shared weekly games swing)

| through week | weeks | team-weeks | live | measured | SE | status |
|---|---|---|---|---|---|---|
| 1 | 1 | 12 | 0.06 | no shock detectable at this sample (excess variance 0.00438 ± 0.00226, not 2 SE clear of 0) | – | too few weeks to propose (1 of 4) |
| 2 | 1,2 | 24 | 0.06 | 0.0973 | 0.0134 | too few weeks to propose (2 of 4) |
| 3 | 1,2,3 | 36 | 0.06 | 0.1117 | 0.0153 | too few weeks to propose (3 of 4) |

## weekly_availability (share of team games played, by assumed tier)

| through week | tier (live) | measured | SE | n | live within 2 SE |
|---|---|---|---|---|---|
| 1 | 0.00 | 0.000 | 0.000 | 22 | yes |
| 1 | 0.75 | 0.573 | 0.050 | 96 | no |
| 1 | 0.79 | 0.800 | 0.179 | 5 | yes |
| 1 | 0.88 | 0.828 | 0.013 | 809 | no |
| 2 | 0.00 | 0.000 | 0.000 | 48 | yes |
| 2 | 0.75 | 0.551 | 0.035 | 207 | no |
| 2 | 0.79 | 0.909 | 0.087 | 11 | yes |
| 2 | 0.88 | 0.809 | 0.009 | 1727 | no |
| 3 | 0.00 | 0.039 | 0.022 | 77 | yes |
| 3 | 0.75 | 0.561 | 0.027 | 326 | no |
| 3 | 0.79 | 0.895 | 0.070 | 19 | yes |
| 3 | 0.88 | 0.793 | 0.008 | 2736 | no |

## board comparison (realized ratio to healthy, beside each instrument's discount)

| through week | tier | measured | SE | n | deck board | simulator | kit board | within 2 SE (deck / sim / kit) |
|---|---|---|---|---|---|---|---|---|
| 2 | mild | 1.124 | 0.108 | 11 | 0.85 | 0.898 | 0.825 | no / no / no |
| 2 | risk | 0.681 | 0.043 | 207 | 0.78 | 0.852 | 0.904 | no / no / no |
| 3 | mild | 1.128 | 0.089 | 19 | 0.85 | 0.898 | 0.825 | no / no / no |
| 3 | risk | 0.707 | 0.035 | 326 | 0.78 | 0.852 | 0.904 | no / no / no |
