# Yahoo market consolidation — 2026-10-01

Owner ask (2026-09-16): consolidate and average Yahoo's rankings into the internal database. Consolidated per the standing work order: Yahoo lands as reference data (`yahoo-2026-10-01.csv`) and the average lands as the market-lens consensus board (`consensus-2026-10-01.csv`) — mean of the available rank signals (our board rank, Yahoo XRank capped at 300, Yahoo ADP), re-ranked over all pool players. The first-principles board itself is UNCHANGED (owner decision 2026-08-21: reference, not a blend; replacing marketRanks with real market data remains the work order's gated step 5).

Yahoo is a single outlet: per fix F2, nothing here changes a pool row. Team mismatches and coverage gaps below are flags for the next pull's watchlist.

---

## A. Consensus board top 30 (full file: consensus-2026-10-01.csv)

| cons # | player | avg | our # | XRank | ADP |
|---|---|---|---|---|---|
| 1 | Victor Wembanyama | 1.87 | 2 | 2 | 1.6 |
| 2 | Nikola Jokic | 1.97 | 3 | 1 | 1.9 |
| 3 | Shai Gilgeous-Alexander | 3.0 | 1 | 4 | 4.0 |
| 4 | Luka Doncic | 3.5 | 4 | 3 | 3.5 |
| 5 | Cade Cunningham | 7.33 | 11 | 5 | 6.0 |
| 6 | Tyrese Maxey | 7.87 | 6 | 9 | 8.6 |
| 7 | Anthony Edwards | 7.93 | 8 | 8 | 7.8 |
| 8 | Jayson Tatum | 11.43 | 18 | 7 | 9.3 |
| 9 | Karl-Anthony Towns | 12.1 | 5 | 16 | 15.3 |
| 10 | Cooper Flagg | 12.43 | 14 | 13 | 10.3 |
| 11 | Donovan Mitchell | 13.77 | 16 | 12 | 13.3 |
| 12 | Jalen Johnson | 15.87 | 25 | 11 | 11.6 |
| 13 | Tyrese Haliburton | 17.23 | 26 | 10 | 15.7 |
| 14 | Kevin Durant | 20.2 | 30 | 14 | 16.6 |
| 15 | Stephen Curry | 20.53 | 13 | 25 | 23.6 |
| 16 | Austin Reaves | 20.87 | 19 | 21 | 22.6 |
| 17 | Devin Booker | 21.4 | 15 | 23 | 26.2 |
| 18 | Scottie Barnes | 21.43 | 35 | 15 | 14.3 |
| 19 | Jamal Murray | 21.53 | 27 | 17 | 20.6 |
| 20 | Chet Holmgren | 22.1 | 10 | 28 | 28.3 |
| 21 | Amen Thompson | 23.87 | 28 | 20 | 23.6 |
| 22 | Giannis Antetokounmpo | 24.17 | 59 | 6 | 7.5 |
| 23 | Josh Giddey | 24.33 | 31 | 19 | 23.0 |
| 24 | Kawhi Leonard | 26.47 | 12 | 37 | 30.4 |
| 25 | Domantas Sabonis | 26.8 | 20 | 35 | 25.4 |
| 26 | Trae Young | 27.87 | 39 | 18 | 26.6 |
| 27 | Bam Adebayo | 29.37 | 32 | 26 | 30.1 |
| 28 | LaMelo Ball | 30.1 | 40 | 24 | 26.3 |
| 29 | Evan Mobley | 30.37 | 34 | 27 | 30.1 |
| 30 | Trey Murphy III | 30.43 | 21 | 30 | 40.3 |

---

## B. Market arbitrage vs fresh Yahoo ADP (§5.3 / Pass E)
**Values** = our rank 15+ picks ahead of ADP; **Fades** = the reverse. z-lean = the two categories our board leans on most/least — the structural 'why', for the owner to accept or reject.

**Read the deep fades with care:** Yahoo publishes ADP only for its top 188 rows (max 121.7), so a player we rank ≥ ~140 shows a mechanical 15+ 'fade' merely by having an ADP at all. The real adjudication items are the fades among players we rank inside ~140; below that, read a fade as 'the room drafts him at all', not as a precise gap.

### Values (43) — we're higher than the room

| gap | player | our # | ADP | our z-lean |
|---|---|---|---|---|
| +62 | Ty Jerome | 51 | 114 | +STL, +FT% / -BLK, -REB |
| +55 | Dyson Daniels | 9 | 64 | +STL, +TOV / -PTS, -FT% |
| +51 | Kristaps Porzingis | 48 | 99 | +BLK, +REB / -AST, -STL |
| +48 | Jimmy Butler | 68 | 116 | +FT%, +STL / -BLK, -3PM |
| +45 | Ajay Mitchell | 73 | 118 | +STL, +FT% / -BLK, -REB |
| +43 | Josh Hart | 53 | 96 | +REB, +STL / -PTS, -BLK |
| +42 | Fred VanVleet | 76 | 118 | +STL, +AST / -REB, -FG% |
| +42 | Darius Garland | 24 | 66 | +AST, +3PM / -REB, -TOV |
| +42 | John Collins | 74 | 116 | +FG%, +TOV / -AST, -STL |
| +38 | PJ Washington | 77 | 116 | +REB, +TOV / -FT%, -AST |
| +36 | Sandro Mamukelashvili | 84 | 120 | +TOV, +FG% / -PTS, -AST |
| +36 | Jaden McDaniels | 54 | 90 | +TOV, +STL / -PTS, -AST |
| +35 | Anthony Davis | 7 | 42 | +BLK, +REB / -TOV, -3PM |
| +35 | Kyrie Irving | 17 | 52 | +FT%, +3PM / -BLK, -REB |
| +35 | Yaxel Lendeborg | 81 | 116 | +TOV, +REB / -PTS, -3PM |
| +31 | Zach LaVine | 71 | 102 | +3PM, +PTS / -BLK, -REB |
| +31 | Jalen Suggs | 80 | 111 | +STL, +3PM / -FG%, -REB |
| +30 | Paul George | 50 | 80 | +STL, +3PM / -TOV, -FG% |
| +29 | Nic Claxton | 60 | 89 | +BLK, +FG% / -3PM, -FT% |
| +29 | Joel Embiid | 22 | 51 | +FT%, +PTS / -STL, -TOV |
| +28 | Tyler Herro | 41 | 70 | +3PM, +PTS / -FG%, -TOV |
| +28 | Anfernee Simons | 82 | 110 | +3PM, +FT% / -FG%, -REB |
| +25 | Cason Wallace | 93 | 118 | +STL, +TOV / -REB, -PTS |
| +25 | De'Aaron Fox | 55 | 80 | +STL, +AST / -FT%, -TOV |
| +24 | Collin Murray-Boyles | 91 | 115 | +FG%, +BLK / -FT%, -3PM |

### Fades (88) — the room is higher than us

| gap | player | our # | ADP | our z-lean |
|---|---|---|---|---|
| -220 | Bronny James | 324 | 104 | +TOV, +FT% / -STL, -PTS |
| -213 | Aday Mara | 322 | 109 | +TOV, +BLK / -PTS, -STL |
| -191 | Morez Johnson Jr. | 308 | 117 | +TOV, +FG% / -PTS, -STL |
| -179 | Andre Drummond | 284 | 105 | +TOV, +REB / -3PM, -PTS |
| -177 | Jordan Poole | 289 | 112 | +TOV, +FT% / -STL, -REB |
| -138 | AJ Green | 245 | 107 | +TOV, +3PM / -REB, -STL |
| -135 | Mikel Brown | 253 | 118 | +AST, +FT% / -REB, -FG% |
| -132 | Jonathan Kuminga | 246 | 114 | +TOV, +PTS / -STL, -FT% |
| -132 | Neemias Queta | 249 | 117 | +FG%, +TOV / -PTS, -3PM |
| -128 | Jaime Jaquez Jr | 238 | 110 | +TOV, +FG% / -PTS, -3PM |
| -119 | Aaron Wiggins | 230 | 111 | +TOV, +FT% / -AST, -PTS |
| -113 | Kyle Kuzma | 231 | 118 | +TOV, +REB / -FT%, -STL |
| -113 | Kevin Porter Jr | 233 | 120 | +TOV, +FT% / -FG%, -PTS |
| -107 | Jaylen Brown | 134 | 27 | +PTS, +3PM / -TOV, -FT% |
| -106 | LeBron James | 143 | 37 | +AST, +FG% / -FT%, -TOV |
| -104 | Maxime Raynaud | 222 | 118 | +TOV, +FG% / -3PM, -STL |
| -103 | RJ Barrett | 215 | 112 | +PTS, +AST / -STL, -FT% |
| -103 | Dillon Brooks | 217 | 114 | +TOV, +3PM / -FG%, -REB |
| -97 | Paolo Banchero | 131 | 34 | +PTS, +REB / -FT%, -TOV |
| -96 | Luke Kennard | 203 | 108 | +TOV, +FT% / -REB, -PTS |
| -95 | AJ Dybantsa | 174 | 79 | +PTS, +REB / -TOV, -FG% |
| -92 | Klay Thompson | 198 | 106 | +TOV, +3PM / -STL, -REB |
| -91 | Bennedict Mathurin | 208 | 117 | +FT%, +TOV / -AST, -STL |
| -90 | Egor Demin | 209 | 119 | +AST, +3PM / -PTS, -FG% |
| -87 | Dylan Harper | 171 | 84 | +AST, +STL / -BLK, -REB |

---

## C. Team-code mismatches (1) — FLAGS ONLY (F2: single source)

| our # | player | our team | yahoo team |
|---|---|---|---|
| 294 | John Konchar | FA | NYK |

---

## D. Availability disagreements (6) — our GP ≤ 40, market still pricing them

| our # | player | our GP | XRank | ADP |
|---|---|---|---|---|
| 124 | Mark Williams | 15 | 201 | 108.6 |
| 68 | Jimmy Butler | 20 | 154 | 115.9 |
| 137 | Shaedon Sharpe | 18 | 214 | — |
| 179 | Donte DiVincenzo | 15 | 251 | — |
| 225 | Moses Moody | 20 | 261 | — |
| 294 | John Konchar | 30 | 276 | — |

---

## E. Coverage gaps — Yahoo names not in our pool (4; 0 carry an ADP inside 140)
Names the room is drafting that our database cannot price. Owner decides which enter the pool (each needs a sourced projection row).

| player | team | pos | XRank | ADP |
|---|---|---|---|---|
| Jordan Clarkson | NYK | SG,SF | 246 | — |
| Russell Westbrook | SAC | PG,SG | 264 | — |
| Jonas Valančiūnas | DEN | C | 278 | — |
| Nicolas Batum | LAC | SF,PF | 289 | — |

---

## F. What Yahoo changed since `yahoo-2026-09-22.csv`
Same-outlet comparison (287 names in both files, 284 expert-ranked in both). Moves are XRank vs XRank; ADP before and after are shown beside them. A rank move is Yahoo re-pricing a player; a team change here is Yahoo's own roster data moving between the two pastes — still ONE outlet, so it flags a transaction to verify at the next pull, never a row edit.

### Risers (20 shown; XRank move ≥ 10 places, inside 150 on either side)

| move | player | XRank before | XRank after | ADP before | ADP after |
|---|---|---|---|---|---|
| +149 | DeMar DeRozan | 251 | 102 | 117 | 115 |
| +126 | Pelle Larsson | 273 | 147 | — | — |
| +109 | Gui Santos | 250 | 141 | — | — |
| +65 | Rui Hachimura | 186 | 121 | 105 | 109 |
| +50 | Daniel Gafford | 170 | 120 | 107 | 109 |
| +37 | Cameron Johnson | 172 | 135 | 113 | — |
| +33 | Egor Dëmin | 164 | 131 | 120 | 119 |
| +32 | Quentin Grimes | 158 | 126 | 122 | 119 |
| +23 | Yves Missi | 166 | 143 | — | — |
| +19 | Ty Jerome | 133 | 114 | 107 | 114 |
| +18 | Wendell Carter Jr. | 141 | 123 | 112 | 115 |
| +18 | P.J. Washington | 151 | 133 | 118 | 116 |
| +15 | Herbert Jones | 149 | 134 | — | — |
| +14 | Saddiq Bey | 146 | 132 | 122 | 120 |
| +13 | Ausar Thompson | 90 | 77 | 90 | 88 |
| +12 | Keegan Murray | 128 | 116 | 121 | 120 |
| +12 | Collin Gillespie | 137 | 125 | 121 | 119 |
| +11 | Matas Buzelis | 80 | 69 | 59 | 65 |
| +10 | Jalen Suggs | 104 | 94 | 111 | 111 |
| +10 | Ja Morant | 103 | 93 | 92 | 92 |

### Fallers (20 shown)

| move | player | XRank before | XRank after | ADP before | ADP after |
|---|---|---|---|---|---|
| -55 | Kristaps Porziņģis | 97 | 152 | 101 | 99 |
| -37 | Kevin Porter Jr. | 121 | 158 | 117 | 120 |
| -35 | Devin Vassell | 122 | 157 | 117 | 116 |
| -33 | Nikola Vučević | 144 | 177 | 115 | 114 |
| -32 | Reed Sheppard | 117 | 149 | 120 | 122 |
| -30 | Christian Braun | 143 | 173 | 121 | 120 |
| -27 | Maxime Raynaud | 135 | 162 | 119 | 118 |
| -27 | Paul Reed | 138 | 165 | 120 | 114 |
| -24 | Tari Eason | 139 | 163 | 121 | 119 |
| -21 | Bobby Portis Jr. | 140 | 161 | 115 | 111 |
| -20 | Jimmy Butler III | 134 | 154 | 117 | 116 |
| -20 | Yaxel Lendeborg | 124 | 144 | 116 | 116 |
| -19 | Kon Knueppel | 45 | 64 | 39 | 42 |
| -19 | Tre Jones | 129 | 148 | — | 118 |
| -17 | Fred VanVleet | 136 | 153 | 120 | 118 |
| -16 | Sandro Mamukelashvili | 123 | 139 | 118 | 120 |
| -15 | Ajay Mitchell | 130 | 145 | 114 | 118 |
| -13 | Domantas Sabonis | 22 | 35 | 30 | 25 |
| -13 | Jaime Jaquez Jr. | 127 | 140 | 104 | 110 |
| -13 | Jaylen Brown | 31 | 44 | 28 | 27 |

### Newly expert-ranked (3) — placeholder tier before, ranked now

| XRank now | player | ADP before |
|---|---|---|
| 129 | Jonathan Kuminga | 117 |
| 250 | Aday Mara | 102 |
| 467 | Bronny James | 100 |

### Yahoo team changes (0) — transaction flags for the next pull

| XRank | player | before | after |
|---|---|---|---|

### Entered Yahoo's list inside the draftable 156 (0)

| XRank | player | team |
|---|---|---|

### Left Yahoo's list from inside the draftable 156 (0)

| XRank before | player | team | ADP before |
|---|---|---|---|

_Inputs: yahoo-raw-2026-10-01.txt sha256 ca3033cc88dd43bf 2774 lines · projections-2026-27.csv sha256 f319c07f160f96bd 324 rows · yahoo-2026-09-22.csv sha256 b1f3cb53ca82a7de 300 rows · as of commit 020771c (2026-10-01) · by yahoo_market.py_
