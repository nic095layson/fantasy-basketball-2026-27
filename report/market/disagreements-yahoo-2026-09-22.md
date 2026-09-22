# Yahoo market consolidation — 2026-09-22

Owner paste (2026-09-22): Yahoo's current 9-cat RANKINGS as of 2026-09-22 — rank order only, no ADP column. Landed per the standing work order: Yahoo lands as reference data (`yahoo-2026-09-22.csv`, XRank = the rank, ADP empty) and the average lands as the market-lens consensus board (`consensus-2026-09-22.csv`) — mean of our board rank and Yahoo XRank, re-ranked over all pool players. The first-principles board itself is UNCHANGED (owner decision 2026-08-21: reference, not a blend). Downstream, the deck's F8 price loader (yahoo-fantasy-basketball PR #36) prices by ADP where Yahoo lists one, else XRank — this file prices every matched player by XRank, labelled XR.

Yahoo is a single outlet: per fix F2, nothing here changes a pool row. Team mismatches, Yahoo's own team changes since the previous paste, and coverage gaps below are flags for the next pull's watchlist.

---

## A. Consensus board top 30 (full file: consensus-2026-09-22.csv)

| cons # | player | avg | our # | XRank | ADP |
|---|---|---|---|---|---|
| 1 | Victor Wembanyama | 2.0 | 2 | 2 |  |
| 2 | Nikola Jokic | 2.0 | 3 | 1 |  |
| 3 | Shai Gilgeous-Alexander | 2.5 | 1 | 4 |  |
| 4 | Luka Doncic | 3.5 | 4 | 3 |  |
| 5 | Tyrese Maxey | 5.5 | 5 | 6 |  |
| 6 | Anthony Edwards | 7.5 | 8 | 7 |  |
| 7 | Cade Cunningham | 8.0 | 11 | 5 |  |
| 8 | Karl-Anthony Towns | 11.0 | 6 | 16 |  |
| 9 | Jayson Tatum | 12.5 | 17 | 8 |  |
| 10 | Donovan Mitchell | 13.0 | 15 | 11 |  |
| 11 | Cooper Flagg | 13.5 | 14 | 13 |  |
| 12 | Stephen Curry | 17.0 | 12 | 22 |  |
| 13 | Austin Reaves | 18.0 | 18 | 18 |  |
| 14 | Jalen Johnson | 18.0 | 26 | 10 |  |
| 15 | Devin Booker | 19.5 | 13 | 26 |  |
| 16 | Tyrese Haliburton | 20.0 | 28 | 12 |  |
| 17 | Chet Holmgren | 20.5 | 10 | 31 |  |
| 18 | Trey Murphy III | 22.5 | 21 | 24 |  |
| 19 | Jamal Murray | 22.5 | 30 | 15 |  |
| 20 | Kevin Durant | 23.0 | 32 | 14 |  |
| 21 | Evan Mobley | 24.0 | 19 | 29 |  |
| 22 | Josh Giddey | 25.0 | 31 | 19 |  |
| 23 | Anthony Davis | 25.5 | 7 | 44 |  |
| 24 | Scottie Barnes | 26.0 | 35 | 17 |  |
| 25 | Kyrie Irving | 26.5 | 16 | 37 |  |
| 26 | Amen Thompson | 28.5 | 29 | 28 |  |
| 27 | James Harden | 29.5 | 36 | 23 |  |
| 28 | Kawhi Leonard | 30.5 | 25 | 36 |  |
| 29 | Trae Young | 30.5 | 40 | 21 |  |
| 30 | LaMelo Ball | 30.5 | 41 | 20 |  |

---

## B. Market arbitrage vs Yahoo XRank (§5.3 / Pass E)
**Values** = our rank 15+ picks ahead of Yahoo's rank; **Fades** = the reverse. z-lean = the two categories our board leans on most/least — the structural 'why', for the owner to accept or reject.

**Read with care:** this paste is Yahoo's expert RANK, not the room's ADP. It covers 250 names, so a player we rank inside 250 but absent from it appears in section E (coverage), not here.

### Values (80) — we're higher than the room

| gap | player | our # | XRank | our z-lean |
|---|---|---|---|---|
| +130 | Jordan Poole | 80 | 210 | +3PM, +FT% / -TOV, -REB |
| +110 | Anfernee Simons | 84 | 194 | +3PM, +FT% / -FG%, -REB |
| +92 | PJ Washington | 77 | 169 | +REB, +TOV / -FT%, -AST |
| +92 | De'Anthony Melton | 149 | 241 | +STL, +TOV / -REB, -PTS |
| +89 | Cam Johnson | 61 | 150 | +3PM, +FT% / -BLK, -REB |
| +87 | Kyle Filipowski | 129 | 216 | +REB, +TOV / -FT%, -STL |
| +87 | Bilal Coulibaly | 122 | 209 | +STL, +TOV / -FG%, -PTS |
| +82 | Christian Braun | 83 | 165 | +TOV, +FG% / -AST, -BLK |
| +79 | Marcus Smart | 150 | 229 | +STL, +AST / -REB, -PTS |
| +75 | Brook Lopez | 96 | 171 | +BLK, +TOV / -AST, -STL |
| +74 | Herb Jones | 64 | 138 | +STL, +TOV / -REB, -PTS |
| +74 | Alex Caruso | 125 | 199 | +STL, +TOV / -REB, -PTS |
| +72 | Tari Eason | 65 | 137 | +STL, +TOV / -PTS, -AST |
| +68 | Jared McCain | 154 | 222 | +3PM, +FT% / -BLK, -REB |
| +64 | Shaedon Sharpe | 136 | 200 | +3PM, +PTS / -FG%, -REB |
| +62 | Aaron Nesmith | 98 | 160 | +TOV, +FT% / -PTS, -AST |
| +61 | Malik Monk | 162 | 223 | +FT%, +AST / -FG%, -REB |
| +60 | Dyson Daniels | 9 | 69 | +STL, +TOV / -PTS, -FT% |
| +57 | Ajay Mitchell | 72 | 129 | +STL, +FT% / -BLK, -REB |
| +56 | Jimmy Butler | 68 | 124 | +FT%, +STL / -BLK, -3PM |
| +55 | Paul Reed | 104 | 159 | +TOV, +FG% / -3PM, -PTS |
| +55 | Keaton Wagler | 183 | 238 | +3PM, +FT% / -REB, -FG% |
| +54 | Myles Turner | 42 | 96 | +BLK, +TOV / -STL, -AST |
| +54 | Luguentz Dort | 157 | 211 | +TOV, +3PM / -PTS, -AST |
| +53 | Josh Hart | 53 | 106 | +REB, +STL / -BLK, -PTS |

### Fades (80) — the room is higher than us

| gap | player | our # | XRank | our z-lean |
|---|---|---|---|---|
| -128 | Jusuf Nurkic | 238 | 110 | +TOV, +FG% / -3PM, -PTS |
| -126 | Neemias Queta | 223 | 97 | +FG%, +TOV / -PTS, -3PM |
| -110 | Ryan Rollins | 171 | 61 | +TOV, +STL / -PTS, -REB |
| -110 | Davion Mitchell | 211 | 101 | +AST, +TOV / -PTS, -REB |
| -95 | LeBron James | 140 | 45 | +AST, +FG% / -FT%, -TOV |
| -93 | Kevin Porter Jr | 215 | 122 | +TOV, +FT% / -REB, -PTS |
| -87 | Jaylen Brown | 133 | 46 | +PTS, +3PM / -TOV, -FT% |
| -85 | Jaime Jaquez Jr | 218 | 133 | +TOV, +FG% / -PTS, -3PM |
| -78 | Khaman Maluach | 192 | 114 | +BLK, +FG% / -3PM, -STL |
| -76 | Keyonte George | 115 | 39 | +3PM, +AST / -BLK, -TOV |
| -74 | Dylan Harper | 166 | 92 | +AST, +STL / -BLK, -REB |
| -73 | Kon Knueppel | 108 | 35 | +3PM, +FT% / -FG%, -BLK |
| -72 | Jonathan Kuminga | 220 | 148 | +TOV, +REB / -STL, -FT% |
| -70 | Derik Queen | 163 | 93 | +REB, +FG% / -PTS, -3PM |
| -68 | Paolo Banchero | 130 | 62 | +PTS, +REB / -FT%, -TOV |
| -63 | Donovan Clingan | 118 | 55 | +BLK, +REB / -PTS, -3PM |
| -60 | Caleb Wilson | 147 | 87 | +BLK, +REB / -FT%, -3PM |
| -58 | RJ Barrett | 201 | 143 | +PTS, +AST / -STL, -FT% |
| -58 | AJ Dybantsa | 169 | 111 | +PTS, +REB / -TOV, -FG% |
| -56 | Darius Acuff | 208 | 152 | +AST, +FT% / -FG%, -REB |
| -54 | Nickeil Alexander-Walker | 105 | 51 | +3PM, +STL / -FG%, -REB |
| -53 | Cedric Coward | 139 | 86 | +FT%, +REB / -FG%, -STL |
| -51 | Mikel Brown | 240 | 189 | +AST, +TOV / -PTS, -REB |
| -51 | Anthony Black | 177 | 126 | +TOV, +STL / -PTS, -REB |
| -49 | Giannis Antetokounmpo | 58 | 9 | +FG%, +PTS / -TOV, -FT% |

---

## C. Team-code mismatches (0) — FLAGS ONLY (F2: single source)

| our # | player | our team | yahoo team |
|---|---|---|---|

---

## D. Availability disagreements (4) — our GP ≤ 40, market still pricing them

| our # | player | our GP | XRank | ADP |
|---|---|---|---|---|
| 25 | Kawhi Leonard | 35 | 36 | — |
| 68 | Jimmy Butler | 20 | 124 | — |
| 126 | Mark Williams | 15 | 166 | — |
| 136 | Shaedon Sharpe | 18 | 200 | — |

---

## E. Coverage gaps — Yahoo names not in our pool (32; 1 ranked inside the draftable 156)
Names the room is drafting that our database cannot price. Owner decides which enter the pool (each needs a sourced projection row).

| player | team | pos | XRank | ADP |
|---|---|---|---|---|
| Pelle Larsson | MIA | SG,SF | 154 | — |
| Scotty Pippen Jr. | MEM | PG,SG | 158 | — |
| Al Horford | GSW | PF,C | 161 | — |
| Bradley Beal | LAC | SF,SG | 172 | — |
| Daniss Jenkins | DET | PG,SG | 175 | — |
| Jake LaRavia | LAL | SF,PF | 180 | — |
| Oso Ighodaro | PHX | C,PF | 182 | — |
| Kris Dunn | LAC | PG,SG | 190 | — |
| Dylan Cardwell | SAC | C,PF | 197 | — |
| Precious Achiuwa | SAC | PF,C | 198 | — |
| T.J. McConnell | IND | PG | 202 | — |
| Jaylon Tyson | CLE | PF,SF,SG | 205 | — |
| Dennis Schroder | CHA | PG,SG | 206 | — |
| Gui Santos | GSW | SF,PF | 207 | — |
| Miles McBride | NYK | PG,SG | 208 | — |
| Jalen Smith | CHI | PF,C | 214 | — |
| Kevin Huerter | DET | SG,SF | 215 | — |
| Nique Clifford | SAC | SF,SG | 217 | — |
| Jaylin Williams | OKC | PF,C | 220 | — |
| Cam Spencer | MEM | PG,SG | 225 | — |
| Noah Clowney | BKN | C,PF | 228 | — |
| Ben Simmons | SAC | PG | 230 | — |
| Marvin Bagley III | DEN | PF,C | 231 | — |
| Will Riley | WAS | PF,SF | 234 | — |
| Jamal Shead | TOR | PG | 236 | — |
| Bones Hyland | MIN | PG,SG | 237 | — |
| Ryan Kalkbrenner | CHA | C | 239 | — |
| Kentavious Caldwell-Pope | PHI | SG,SF | 243 | — |
| Brayden Burries | MIL | SG | 244 | — |
| Kingston Flemings | ATL | PG,SG | 247 | — |
| Aday Mara | OKC | C | 249 | — |
| Zach Collins | CHI | C | 250 | — |

---

## F. What Yahoo changed since `yahoo-2026-09-15.csv`
Same-outlet comparison (242 names in both files, 242 expert-ranked in both). Moves are XRank vs XRank — the previous file's ADP is shown for reference only, because this paste carries none. A rank move is Yahoo re-pricing a player; a team change here is Yahoo's own roster data moving between the two pastes — still ONE outlet, so it flags a transaction to verify at the next pull, never a row edit.

### Risers (20 shown; XRank move ≥ 10 places, inside 150 on either side)

| move | player | XRank before | XRank after | ADP before |
|---|---|---|---|---|
| +70 | Rui Hachimura | 195 | 125 | 106 |
| +65 | Dereck Lively II | 211 | 146 | — |
| +59 | Jonathan Kuminga | 207 | 148 | 117 |
| +55 | Tre Jones | 173 | 118 | — |
| +54 | Khaman Maluach | 168 | 114 | 121 |
| +41 | Herbert Jones | 179 | 138 | — |
| +36 | Tobias Harris | 183 | 147 | — |
| +36 | Davion Mitchell | 137 | 101 | 111 |
| +35 | Cason Wallace | 154 | 119 | 114 |
| +33 | Moussa Diabate | 177 | 144 | 99 |
| +30 | Zach LaVine | 125 | 95 | 120 |
| +27 | Keegan Murray | 118 | 91 | 122 |
| +26 | Bennedict Mathurin | 175 | 149 | 122 |
| +22 | Cedric Coward | 108 | 86 | 100 |
| +21 | Tari Eason | 158 | 137 | — |
| +20 | Devin Vassell | 161 | 141 | 117 |
| +19 | John Collins | 121 | 102 | 119 |
| +18 | Andrew Nembhard | 130 | 112 | 121 |
| +17 | Michael Porter Jr. | 67 | 50 | 68 |
| +17 | Kelly Oubre Jr. | 145 | 128 | 111 |

### Fallers (20 shown)

| move | player | XRank before | XRank after | ADP before |
|---|---|---|---|---|
| -89 | Keaton Wagler | 149 | 238 | 122 |
| -70 | Mark Williams | 96 | 166 | 103 |
| -54 | Shaedon Sharpe | 146 | 200 | 114 |
| -50 | Wendell Carter Jr. | 103 | 153 | 110 |
| -45 | Kyshawn George | 106 | 151 | 112 |
| -45 | Quentin Grimes | 140 | 185 | 122 |
| -41 | Darryn Peterson | 93 | 134 | 93 |
| -37 | Maxime Raynaud | 127 | 164 | 121 |
| -36 | Darius Acuff Jr. | 116 | 152 | 110 |
| -32 | Brook Lopez | 139 | 171 | 78 |
| -25 | AJ Dybantsa | 86 | 111 | 76 |
| -25 | P.J. Washington Jr. | 144 | 169 | 119 |
| -24 | Sandro Mamukelashvili | 112 | 136 | 115 |
| -23 | Anthony Davis | 21 | 44 | 25 |
| -20 | Egor Demin | 135 | 155 | 121 |
| -20 | Naz Reid | 61 | 81 | 65 |
| -20 | RJ Barrett | 123 | 143 | 111 |
| -18 | Kawhi Leonard | 18 | 36 | 20 |
| -18 | Paul Reed | 141 | 159 | 124 |
| -17 | CJ McCollum | 115 | 132 | 111 |

### Newly expert-ranked (0) — placeholder tier before, ranked now

| XRank now | player | ADP before |
|---|---|---|

### Yahoo team changes (0) — transaction flags for the next pull

| XRank | player | before | after |
|---|---|---|---|

### Entered Yahoo's list inside the draftable 156 (0)

| XRank | player | team |
|---|---|---|

### Left Yahoo's list from inside the draftable 156 (0)

| XRank before | player | team | ADP before |
|---|---|---|---|

