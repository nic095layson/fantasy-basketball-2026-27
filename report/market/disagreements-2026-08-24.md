# Market disagreement & arbitrage tables — 2026-08-24

Reference layer for owner adjudication (work order §3.4, §5.3). Built from committed raw snapshots; our board = rank_engine.py over projections-2026-27.csv, unchanged. The board stays built from first principles — these are consulted as a sanity reference, not blended (owner decision 2026-08-21).

- **Statdunk** = category value reconstructed from the freshest projections (`Projections V4.10`, asOf **2026-08-23T20:12:48.000Z**) via statdunk's own `attempt-weighted-nine-category-zscore-v1` method — validated to reproduce statdunk's published category block exactly (Spearman 1.0000). The pre-computed board itself sits behind statdunk's off-allowlist Supabase backend. Ranks compared = games-inclusive `totals` (structural analog of our availability-adjusted board); per-game `averages` rank shown alongside.
- **Hashtag** = 2026-27 Rest-of-Season, Yahoo ADP + eligibility.

---

## A. Biggest per-game line (and games) differences vs Hashtag (§3.4)
Our projection minus Hashtag's, for matched players with at least one category past threshold (pts 3.0, reb 1.5, ast 1.5, stl 0.4, blk 0.4, tpm 0.6, gp 8, fg_pct 0.03, ft_pct 0.04, tov 0.8); `gp` is season games. Sorted by total divergence. `+` = we project higher than Hashtag.

| our # | player | flagged diffs (our − hashtag) |
|---|---|---|
| 212 | Zuby Ejiofor | pts +5.7, reb +4.2, stl +0.4, blk +0.8, fg_pct +0.070, gp +42.0 |
| 117 | Bogdan Bogdanovic | pts +8.5, reb +1.8, ast +1.9, stl +0.7, tpm +1.5, tov +1.0, gp +22.0 |
| 188 | Hannes Steinbach | pts +6.3, reb +5.3, blk +0.6, ft_pct -0.056, tov +1.0, gp +18.0 |
| 165 | GG Jackson | pts +7.0, reb +2.4, stl +0.4, tpm +1.0, ft_pct +0.044, gp +28.0 |
| 161 | Gary Trent Jr | pts +7.1, reb +2.0, stl +0.5, tpm +1.1, gp +28.0 |
| 214 | Jusuf Nurkic | pts -3.7, reb -4.2, ast -1.9, stl -0.5, ft_pct +0.088, tov -1.2 |
| 181 | Kasparas Jakucionis | pts +7.0, ast +3.3, ft_pct -0.077, tov +1.6, gp +10.0 |
| 176 | Rob Dillingham | pts +6.6, ast +2.6, tpm +0.9, fg_pct +0.040, ft_pct +0.116 |
| 174 | Khaman Maluach | pts +3.7, reb +2.9, fg_pct +0.087, ft_pct -0.070, gp +10.0 |
| 204 | Dalton Knecht | pts +7.3, reb +1.5, tpm +1.3, ft_pct +0.045, gp +18.0 |
| 78 | Jordan Poole | pts +6.3, ast +1.6, stl +0.5, tpm +0.7, tov +0.9, gp +15.0 |
| 208 | Dailyn Swain | pts +3.2, blk +0.4, ft_pct -0.086, gp +15.0 |
| 93 | Brook Lopez | pts +3.7, reb +1.7, blk +0.6, fg_pct +0.035, gp +8.0 |
| 154 | Derik Queen | fg_pct +0.046, ft_pct -0.076, tov -0.8, gp -12.0 |
| 173 | Taylor Hendricks | pts +4.4, reb +2.3, blk +0.4, ft_pct +0.064 |
| 113 | Yaxel Lendeborg | pts +3.2, reb +1.9, stl +0.4, ft_pct -0.088 |
| 178 | Egor Demin | ast +2.1, tpm -1.2, ft_pct -0.081 |
| 209 | Clint Capela | reb +2.6, fg_pct +0.077, gp +9.0 |
| 51 | Nikola Vucevic | pts +5.5, reb +3.2, fg_pct +0.037 |
| 213 | Andre Drummond | fg_pct +0.067, ft_pct -0.076, gp -8.0 |
| 54 | Jimmy Butler | fg_pct -0.040, gp +30.0 |
| 100 | Nickeil Alexander-Walker | pts -5.1, tpm -0.8, ft_pct -0.081 |
| 215 | Labaron Philon | pts +3.0, ast +1.5, stl +0.4, gp +14.0 |
| 185 | Khris Middleton | pts +3.7, tpm +0.7, gp +18.0 |
| 119 | Kyle Filipowski | pts +7.0, reb +3.4 |
| 65 | Nic Claxton | reb +2.0, blk +0.6, fg_pct +0.052 |
| 33 | Bam Adebayo | blk +0.4, tpm -0.8, fg_pct +0.067 |
| 112 | Donovan Clingan | reb -1.9, tpm -1.1, ft_pct -0.054 |
| 157 | Ryan Rollins | pts -5.0, tpm -0.9, tov -1.0 |
| 9 | Dyson Daniels | stl +0.7, tpm +0.6, ft_pct +0.058 |
| 41 | LaMelo Ball | pts +5.7, tpm +0.7, tov +0.8 |
| 133 | Bennedict Mathurin | pts +4.7, tpm +0.7, gp +10.0 |
| 201 | Gradey Dick | pts +6.0, tpm +1.1 |
| 110 | Jerami Grant | reb +1.5, fg_pct +0.032, gp +14.0 |
| 192 | Kyle Kuzma | pts +4.5, reb +1.9, ft_pct +0.042 |
| 26 | Kawhi Leonard | gp -30.0 |
| 196 | Nikola Jovic | pts +3.2, fg_pct +0.044, ft_pct +0.047 |
| 155 | AJ Dybantsa | reb +1.8, tpm +0.8, fg_pct -0.035 |
| 103 | DeMar DeRozan | pts +4.3, ast +1.7, tov +0.8 |
| 193 | Kevin Porter Jr | stl -0.6, tpm +0.6, ft_pct -0.042 |

_138 matched players show a material line divergence._

---

## B. Biggest ordering differences vs Statdunk value (§3.4)
Δ = Statdunk totals rank − our board rank. **Δ>0 = we rank him higher than Statdunk** (a relative value on our board); Δ<0 = Statdunk higher (a relative fade). `sd_avg#` = Statdunk per-game rank.

**Read with care:** Statdunk `totals` weights games proportionally (full season totals) — a harsher availability model than our streaming-credit `z_adj`. For injury-discounted stars a large Δ is mostly that model gap, not a valuation disagreement: compare `sd_avg#` (per-game) instead. E.g. Embiid sits at sd_tot#≈117 but sd_avg#≈23 ≈ our #22 — we agree on his per-game value and differ only on how hard to dock the missed games.

| |Δ| | player | our # | sd_tot# | sd_avg# | our zAdj |
|---|---|---|---|---|---|
| -140 | Neemias Queta | 202 | 62 | 86 | -4.31 |
| +131 | Bogdan Bogdanovic | 117 | 248 | 244 | -1.35 |
| +130 | Herb Jones | 66 | 196 | 136 | +0.28 |
| +124 | Jordan Poole | 78 | 202 | 173 | -0.07 |
| -124 | Ryan Rollins | 157 | 33 | 54 | -2.44 |
| +111 | Fred VanVleet | 75 | 186 | 77 | +0.00 |
| -107 | Kevin Porter Jr | 193 | 86 | 71 | -3.76 |
| -97 | Derik Queen | 154 | 57 | 91 | -2.37 |
| +96 | Zach Edey | 73 | 169 | 95 | +0.07 |
| +95 | Joel Embiid | 22 | 117 | 23 | +2.38 |
| +94 | De'Anthony Melton | 138 | 232 | 177 | -2.05 |
| -90 | Donovan Clingan | 112 | 22 | 36 | -1.12 |
| +89 | Kyrie Irving | 16 | 105 | 16 | +2.92 |
| +87 | Anfernee Simons | 81 | 168 | 170 | -0.13 |
| +87 | Alex Caruso | 121 | 208 | 197 | -1.40 |
| +86 | Walker Kessler | 37 | 123 | 38 | +1.48 |
| +83 | Marcus Smart | 140 | 223 | 203 | -2.12 |
| +82 | PJ Washington | 77 | 159 | 148 | -0.07 |
| +81 | Aaron Gordon | 97 | 178 | 129 | -0.74 |
| -81 | Jusuf Nurkic | 214 | 133 | 118 | -5.34 |
| +80 | Jerami Grant | 110 | 190 | 159 | -1.10 |
| -80 | Nickeil Alexander-Walker | 100 | 20 | 40 | -0.81 |
| -80 | Kon Knueppel | 101 | 21 | 50 | -0.84 |
| -75 | Ayo Dosunmu | 143 | 68 | 65 | -2.19 |
| +74 | Kristaps Porzingis | 53 | 127 | 68 | +0.79 |
| -74 | Jaylen Brown | 123 | 49 | 55 | -1.42 |
| -72 | Julius Randle | 130 | 58 | 84 | -1.59 |
| -72 | Donte DiVincenzo | 159 | 87 | 114 | -2.56 |
| +69 | Jalen Green | 129 | 198 | 172 | -1.57 |
| -68 | LeBron James | 131 | 63 | 53 | -1.66 |
| +67 | Tari Eason | 68 | 135 | 131 | +0.20 |
| +64 | Max Strus | 186 | 250 | 237 | -3.55 |
| +63 | Zaccharie Risacher | 134 | 197 | 207 | -1.88 |
| -61 | Keyonte George | 170 | 109 | 106 | -2.99 |
| -60 | Naz Reid | 96 | 36 | 63 | -0.72 |
| +59 | Domantas Sabonis | 21 | 80 | 32 | +2.53 |
| +59 | Bilal Coulibaly | 114 | 173 | 158 | -1.26 |
| +57 | Zach LaVine | 72 | 129 | 105 | +0.10 |
| +57 | Khris Middleton | 185 | 242 | 242 | -3.51 |
| -56 | Matas Buzelis | 80 | 24 | 49 | -0.10 |

---

## C. Market arbitrage vs Yahoo ADP (§5.3 / Pass E)
Designed-but-never-populated Pass E output. **Values** = our rank 15+ picks ahead of ADP; **Fades** = ADP 15+ picks ahead of our rank. z-profile names the two categories our board leans on most (+) and least (−) for that player — the structural 'why', for the owner to accept or reject. Mechanisms are the owner's call; nothing here is blended into the board.

### Values (42) — we're higher than the room

| gap | player | our # | Yahoo ADP | our board z-lean |
|---|---|---|---|---|
| +68 | Reed Sheppard | 50 | 118 | +STL, +3PM / -FG%, -REB |
| +64 | Jimmy Butler | 54 | 118 | +FT%, +STL / -BLK, -3PM |
| +62 | Tari Eason | 68 | 130 | +STL, +TOV / -PTS, -AST |
| +58 | Nikola Vucevic | 51 | 109 | +REB, +FG% / -AST, -STL |
| +53 | Myles Turner | 42 | 95 | +BLK, +TOV / -STL, -AST |
| +52 | Cam Johnson | 63 | 115 | +3PM, +FT% / -BLK, -REB |
| +52 | Kristaps Porzingis | 53 | 104 | +BLK, +REB / -AST, -STL |
| +51 | Dyson Daniels | 9 | 60 | +STL, +TOV / -PTS, -FT% |
| +48 | Zach LaVine | 72 | 120 | +3PM, +PTS / -BLK, -REB |
| +47 | PJ Washington | 77 | 124 | +REB, +TOV / -AST, -FT% |
| +45 | Fred VanVleet | 75 | 120 | +STL, +AST / -REB, -FG% |
| +44 | Anfernee Simons | 81 | 125 | +3PM, +FT% / -FG%, -REB |
| +41 | John Collins | 76 | 117 | +FG%, +TOV / -AST, -STL |
| +39 | Josh Hart | 57 | 96 | +REB, +STL / -BLK, -PTS |
| +36 | Christian Braun | 82 | 118 | +TOV, +FG% / -AST, -BLK |
| +35 | Kel'el Ware | 39 | 74 | +BLK, +REB / -3PM, -AST |
| +34 | Toumani Camara | 84 | 118 | +STL, +TOV / -AST, -PTS |
| +33 | Darius Garland | 23 | 56 | +AST, +3PM / -REB, -TOV |
| +30 | Brook Lopez | 93 | 123 | +BLK, +TOV / -AST, -STL |
| +29 | Kyrie Irving | 16 | 45 | +FT%, +3PM / -BLK, -REB |
| +28 | Nic Claxton | 65 | 93 | +BLK, +FG% / -3PM, -FT% |
| +28 | Jalen Suggs | 79 | 107 | +STL, +3PM / -FG%, -REB |
| +26 | Paul George | 52 | 78 | +STL, +3PM / -TOV, -FG% |
| +25 | Anthony Edwards | 7 | 32 | +3PM, +PTS / -FG%, -TOV |
| +25 | De'Aaron Fox | 56 | 81 | +STL, +AST / -FT%, -TOV |
| +24 | Jrue Holiday | 91 | 115 | +AST, +STL / -REB, -PTS |
| +24 | Joel Embiid | 22 | 46 | +FT%, +PTS / -3PM, -TOV |
| +24 | Cason Wallace | 89 | 113 | +STL, +TOV / -REB, -PTS |
| +24 | Donovan Mitchell | 14 | 38 | +3PM, +PTS / -BLK, -TOV |
| +22 | Jaden McDaniels | 55 | 77 | +TOV, +STL / -PTS, -AST |

### Fades (73) — the room is higher than us

| gap | player | our # | Yahoo ADP | our board z-lean |
|---|---|---|---|---|
| -120 | Keyonte George | 170 | 50 | +AST, +3PM / -BLK, -FG% |
| -99 | Jusuf Nurkic | 214 | 115 | +TOV, +FG% / -3PM, -PTS |
| -98 | Neemias Queta | 202 | 104 | +FG%, +TOV / -PTS, -3PM |
| -97 | Jaime Jaquez Jr | 197 | 100 | +TOV, +FG% / -PTS, -3PM |
| -95 | Zuby Ejiofor | 212 | 117 | +TOV, +BLK / -3PM, -PTS |
| -93 | Jaylen Brown | 123 | 30 | +PTS, +3PM / -TOV, -FT% |
| -92 | LeBron James | 131 | 39 | +AST, +FG% / -FT%, -TOV |
| -92 | Mikel Brown | 216 | 124 | +AST, +TOV / -PTS, -REB |
| -86 | Ryan Rollins | 157 | 71 | +TOV, +STL / -REB, -PTS |
| -85 | Isaiah Collier | 205 | 120 | +AST, +STL / -PTS, -REB |
| -85 | Paolo Banchero | 122 | 37 | +PTS, +REB / -FT%, -TOV |
| -79 | AJ Dybantsa | 155 | 76 | +PTS, +REB / -TOV, -FG% |
| -79 | Scoot Henderson | 207 | 128 | +AST, +FT% / -FG%, -REB |
| -77 | Kevin Porter Jr | 193 | 116 | +TOV, +FT% / -FG%, -PTS |
| -76 | Darius Acuff | 187 | 111 | +AST, +FT% / -FG%, -REB |
| -74 | Dylan Harper | 153 | 79 | +AST, +STL / -BLK, -REB |
| -74 | Donovan Clingan | 112 | 38 | +BLK, +REB / -PTS, -3PM |
| -73 | Sam Hauser | 195 | 122 | +TOV, +3PM / -PTS, -STL |
| -73 | RJ Barrett | 183 | 110 | +PTS, +AST / -STL, -FT% |
| -72 | Davion Mitchell | 190 | 118 | +AST, +TOV / -PTS, -REB |
| -72 | Derik Queen | 154 | 82 | +REB, +FG% / -PTS, -3PM |
| -70 | Kyle Kuzma | 192 | 122 | +TOV, +REB / -FT%, -STL |
| -68 | Julius Randle | 130 | 62 | +REB, +PTS / -STL, -TOV |
| -67 | Kon Knueppel | 101 | 34 | +3PM, +FT% / -FG%, -BLK |
| -65 | Darryn Peterson | 156 | 91 | +STL, +FT% / -REB, -FG% |
| -62 | Dillon Brooks | 182 | 120 | +TOV, +3PM / -AST, -REB |
| -59 | Keldon Johnson | 189 | 130 | +TOV, +FG% / -STL, -AST |
| -59 | Hannes Steinbach | 188 | 129 | +FG%, +REB / -STL, -3PM |
| -57 | Caleb Wilson | 137 | 80 | +BLK, +REB / -FT%, -3PM |
| -57 | Egor Demin | 178 | 121 | +AST, +STL / -PTS, -FG% |

