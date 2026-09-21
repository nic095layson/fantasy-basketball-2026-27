# Yahoo market consolidation — 2026-09-15

Owner ask (2026-09-16): consolidate and average Yahoo's rankings into the internal database. Consolidated per the standing work order: Yahoo lands as reference data (`yahoo-2026-09-15.csv`) and the average lands as the market-lens consensus board (`consensus-2026-09-15.csv`) — mean of the available rank signals (our board rank, Yahoo XRank capped at 300, Yahoo ADP), re-ranked over all pool players. The first-principles board itself is UNCHANGED (owner decision 2026-08-21: reference, not a blend; replacing marketRanks with real market data remains the work order's gated step 5).

Yahoo is a single outlet: per fix F2, nothing here changes a pool row. Team mismatches and coverage gaps below are flags for the next pull's watchlist.

---

## A. Consensus board top 30 (full file: consensus-2026-09-15.csv)

| cons # | player | avg | our # | XRank | ADP |
|---|---|---|---|---|---|
| 1 | Victor Wembanyama | 1.6 | 2 | 1 | 1.8 |
| 2 | Nikola Jokic | 2.57 | 3 | 2 | 2.7 |
| 3 | Shai Gilgeous-Alexander | 3.7 | 1 | 4 | 6.1 |
| 4 | Luka Doncic | 3.93 | 4 | 3 | 4.8 |
| 5 | Tyrese Maxey | 7.37 | 5 | 6 | 11.1 |
| 6 | Cade Cunningham | 8.17 | 11 | 5 | 8.5 |
| 7 | Anthony Edwards | 10.33 | 8 | 8 | 15.0 |
| 8 | Jayson Tatum | 12.13 | 17 | 7 | 12.4 |
| 9 | Karl-Anthony Towns | 12.4 | 6 | 16 | 15.2 |
| 10 | Cooper Flagg | 12.67 | 14 | 13 | 11.0 |
| 11 | Donovan Mitchell | 15.2 | 15 | 11 | 19.6 |
| 12 | Chet Holmgren | 16.7 | 10 | 19 | 21.1 |
| 13 | Jalen Johnson | 17.47 | 26 | 10 | 16.4 |
| 14 | Anthony Davis | 17.63 | 7 | 21 | 24.9 |
| 15 | Stephen Curry | 20.2 | 12 | 25 | 23.6 |
| 16 | Kevin Durant | 20.5 | 32 | 14 | 15.5 |
| 17 | Tyrese Haliburton | 20.73 | 28 | 12 | 22.2 |
| 18 | Kawhi Leonard | 21.0 | 25 | 18 | 20.0 |
| 19 | Scottie Barnes | 21.37 | 35 | 15 | 14.1 |
| 20 | Austin Reaves | 21.47 | 18 | 24 | 22.4 |
| 21 | Jamal Murray | 21.87 | 30 | 17 | 18.6 |
| 22 | Devin Booker | 25.87 | 13 | 33 | 31.6 |
| 23 | Giannis Antetokounmpo | 26.43 | 58 | 9 | 12.3 |
| 24 | Evan Mobley | 27.8 | 19 | 32 | 32.4 |
| 25 | LaMelo Ball | 27.83 | 41 | 20 | 22.5 |
| 26 | Trey Murphy III | 28.93 | 21 | 30 | 35.8 |
| 27 | Josh Giddey | 29.27 | 31 | 27 | 29.8 |
| 28 | Trae Young | 29.53 | 40 | 22 | 26.6 |
| 29 | Domantas Sabonis | 29.73 | 20 | 34 | 35.2 |
| 30 | Amen Thompson | 29.73 | 29 | 31 | 29.2 |

---

## B. Market arbitrage vs fresh Yahoo ADP (§5.3 / Pass E)
**Values** = our rank 15+ picks ahead of ADP; **Fades** = the reverse. z-lean = the two categories our board leans on most/least — the structural 'why', for the owner to accept or reject.

**Read the deep fades with care:** Yahoo publishes ADP only for its top 189 rows (max 125.2), so a player we rank ≥ ~140 shows a mechanical 15+ 'fade' merely by having an ADP at all. The real adjudication items are the fades among players we rank inside ~140; below that, read a fade as 'the room drafts him at all', not as a precise gap.

### Values (45) — we're higher than the room

| gap | player | our # | ADP | our z-lean |
|---|---|---|---|---|
| +54 | Kristaps Porzingis | 52 | 106 | +BLK, +REB / -AST, -STL |
| +54 | Dyson Daniels | 9 | 63 | +STL, +TOV / -PTS, -FT% |
| +53 | Myles Turner | 42 | 95 | +BLK, +TOV / -STL, -AST |
| +52 | Jimmy Butler | 68 | 120 | +FT%, +STL / -BLK, -3PM |
| +47 | Zach LaVine | 73 | 120 | +3PM, +PTS / -BLK, -REB |
| +47 | Cam Johnson | 61 | 108 | +3PM, +FT% / -BLK, -REB |
| +45 | Ty Jerome | 51 | 96 | +STL, +FT% / -BLK, -REB |
| +45 | Fred VanVleet | 76 | 121 | +STL, +AST / -REB, -FG% |
| +44 | Josh Hart | 53 | 97 | +REB, +STL / -BLK, -PTS |
| +42 | PJ Washington | 77 | 119 | +REB, +TOV / -FT%, -AST |
| +41 | John Collins | 78 | 119 | +FG%, +TOV / -AST, -STL |
| +38 | Ajay Mitchell | 72 | 110 | +STL, +FT% / -BLK, -REB |
| +36 | Kel'el Ware | 39 | 76 | +BLK, +REB / -STL, -AST |
| +36 | Christian Braun | 83 | 118 | +TOV, +FG% / -AST, -BLK |
| +35 | Darius Garland | 23 | 58 | +AST, +3PM / -REB, -TOV |
| +34 | Toumani Camara | 85 | 119 | +STL, +TOV / -AST, -PTS |
| +33 | Nic Claxton | 62 | 95 | +BLK, +FG% / -3PM, -FT% |
| +33 | Anfernee Simons | 84 | 117 | +3PM, +FT% / -FG%, -REB |
| +33 | Kyrie Irving | 16 | 49 | +FT%, +3PM / -BLK, -REB |
| +30 | Paul George | 50 | 80 | +STL, +3PM / -TOV, -FG% |
| +29 | Sandro Mamukelashvili | 86 | 115 | +TOV, +FG% / -PTS, -AST |
| +29 | Jalen Suggs | 79 | 108 | +STL, +3PM / -FG%, -REB |
| +28 | De'Aaron Fox | 54 | 82 | +STL, +AST / -FT%, -TOV |
| +26 | Collin Murray-Boyles | 95 | 121 | +FG%, +BLK / -FT%, -3PM |
| +26 | Joel Embiid | 22 | 48 | +FT%, +PTS / -STL, -TOV |

### Fades (91) — the room is higher than us

| gap | player | our # | ADP | our z-lean |
|---|---|---|---|---|
| -150 | Adem Bona | 235 | 85 | +TOV, +BLK / -3PM, -PTS |
| -148 | AJ Green | 221 | 73 | +TOV, +3PM / -REB, -STL |
| -130 | Allen Graves | 228 | 98 | +TOV, +FT% / -AST, -PTS |
| -120 | Jusuf Nurkic | 238 | 118 | +TOV, +FG% / -3PM, -PTS |
| -119 | Morez Johnson Jr. | 242 | 123 | +TOV, +FG% / -PTS, -STL |
| -118 | Neemias Queta | 223 | 105 | +FG%, +TOV / -PTS, -3PM |
| -118 | Mikel Brown | 240 | 122 | +AST, +TOV / -PTS, -REB |
| -113 | Jaime Jaquez Jr | 218 | 105 | +TOV, +FG% / -PTS, -3PM |
| -106 | Sam Hauser | 216 | 110 | +TOV, +3PM / -PTS, -STL |
| -103 | Jonathan Kuminga | 220 | 117 | +TOV, +REB / -STL, -FT% |
| -101 | Jaylen Brown | 133 | 32 | +PTS, +3PM / -TOV, -FT% |
| -100 | Davion Mitchell | 211 | 111 | +AST, +TOV / -PTS, -REB |
| -99 | LeBron James | 140 | 41 | +AST, +FG% / -FT%, -TOV |
| -98 | Kevin Porter Jr | 215 | 116 | +TOV, +FT% / -REB, -PTS |
| -98 | Darius Acuff | 208 | 110 | +AST, +FT% / -FG%, -REB |
| -97 | Ryan Rollins | 171 | 74 | +TOV, +STL / -PTS, -REB |
| -94 | Kyle Kuzma | 214 | 120 | +TOV, +REB / -FT%, -STL |
| -93 | AJ Dybantsa | 169 | 76 | +PTS, +REB / -TOV, -FG% |
| -92 | Paolo Banchero | 130 | 38 | +PTS, +REB / -FT%, -TOV |
| -90 | RJ Barrett | 201 | 111 | +PTS, +AST / -STL, -FT% |
| -90 | Duncan Robinson | 186 | 96 | +3PM, +TOV / -REB, -STL |
| -87 | Dylan Harper | 166 | 79 | +AST, +STL / -BLK, -REB |
| -86 | Dillon Brooks | 202 | 116 | +TOV, +3PM / -AST, -REB |
| -86 | Maxime Raynaud | 207 | 121 | +TOV, +FG% / -3PM, -STL |
| -82 | Derik Queen | 163 | 81 | +REB, +FG% / -PTS, -3PM |

---

## C. Team-code mismatches (0) — FLAGS ONLY (F2: single source)

| our # | player | our team | yahoo team |
|---|---|---|---|

---

## D. Availability disagreements (5) — our GP ≤ 40, market still pricing them

| our # | player | our GP | XRank | ADP |
|---|---|---|---|---|
| 25 | Kawhi Leonard | 35 | 18 | 20.0 |
| 126 | Mark Williams | 15 | 96 | 102.7 |
| 136 | Shaedon Sharpe | 18 | 146 | 114.2 |
| 68 | Jimmy Butler | 20 | 129 | 120.5 |
| 173 | Donte DiVincenzo | 15 | 251 | — |

---

## E. Coverage gaps — Yahoo names not in our pool (75; 7 carry an ADP inside 140)
Names the room is drafting that our database cannot price. Owner decides which enter the pool (each needs a sourced projection row).

| player | team | pos | XRank | ADP |
|---|---|---|---|---|
| Al Horford | GSW | PF,C | 248 | 86.6 |
| Luke Kornet | SAS | C | 220 | 87.5 |
| Luke Kennard | PHX | SG,SF | 255 | 87.5 |
| Aaron Wiggins | ATL | SG,SF | 271 | 88.4 |
| Aday Mara | OKC | C | 209 | 91.5 |
| T.J. McConnell | IND | PG | 247 | 93.5 |
| Johni Broome | LAC | C | 668 | 105.4 |
| Scotty Pippen Jr. | MEM | PG | 176 | — |
| Will Riley | WAS | SF,PF | 178 | — |
| Brayden Burries | MIL | SG | 180 | — |
| Ousmane Dieng | MIL | SF,PF | 182 | — |
| Tim Hardaway Jr. | MIA | SG,SF | 184 | — |
| Kingston Flemings | ATL | PG | 191 | — |
| Jaylon Tyson | CLE | SG,SF,PF | 192 | — |
| Jaylin Williams | OKC | PF,C | 193 | — |
| Ryan Kalkbrenner | CHA | C | 194 | — |
| Precious Achiuwa | SAC | PF,C | 198 | — |
| Gui Santos | GSW | SF,PF | 200 | — |
| Pelle Larsson | MIA | SG,SF | 201 | — |
| Dylan Cardwell | SAC | PF,C | 206 | — |
| Cam Spencer | MEM | PG,SG | 208 | — |
| Baylor Scheierman | BOS | SG,SF | 210 | — |
| Nique Clifford | SAC | SG,SF | 214 | — |
| Nate Ament | MIL | SF | 216 | — |
| Jalen Smith | CHI | PF,C | 217 | — |
| Moussa Cisse | DAL | C | 218 | — |
| Max Christie | DAL | SG,SF | 219 | — |
| Marvin Bagley III | DEN | PF,C | 221 | — |
| Sam Merrill | CLE | SG,SF | 222 | — |
| Daniss Jenkins | DET | PG,SG | 224 | — |
| Isaiah Jackson | LAC | C | 228 | — |
| Jock Landale | ATL | C | 229 | — |
| Hugo González | BOS | SG,SF | 232 | — |
| Jamal Shead | TOR | PG | 234 | — |
| Oso Ighodaro | PHX | C | 239 | — |
| Sergio De Larrea | DAL | PG | 244 | — |
| Carter Bryant | SAS | SF,PF | 245 | — |
| Jake LaRavia | LAL | SF,PF | 249 | — |
| Kris Dunn | LAC | PG,SG | 252 | — |
| Justin Champagnie | WAS | SF,PF | 253 | — |
| Javonte Green | DET | SG,SF | 254 | — |
| Harrison Barnes | SAS | PF | 256 | — |
| Kevin Huerter | DET | SG,SF | 257 | — |
| Moses Moody | GSW | SG,SF,PF | 259 | — |
| Jordan Goodwin | PHX | PG,SG | 261 | — |
| Russell Westbrook | SAC | PG,SG | 262 | — |
| Gary Payton II | GSW | SG,SF | 265 | — |
| Bruce Brown | DEN | PG,SG | 266 | — |
| Jarace Walker | IND | SF,PF | 267 | — |
| Dennis Schröder | CHA | PG,SG | 269 | — |
| Ziaire Williams | LAL | SG,SF | 270 | — |
| Ja'Kobe Walter | TOR | PG,SG | 272 | — |
| Dominick Barlow | PHI | PF,C | 274 | — |
| John Konchar | MIN | SG,SF | 275 | — |
| Jose Alvarado | NYK | PG | 276 | — |
| Jonas Valančiūnas | DEN | C | 277 | — |
| Noah Clowney | BKN | PF,C | 279 | — |
| Dru Smith | MIA | PG,SG | 280 | — |
| Vít Krejčí | POR | SG,SF | 281 | — |
| Jaxson Hayes | UTA | C | 283 | — |
| Karlo Matković | NOP | PF,C | 284 | — |
| Dean Wade | PHI | SF,PF | 285 | — |
| Isaac Okoro | CHI | SG,SF | 286 | — |
| Ryan Dunn | PHX | SF,PF | 287 | — |
| Brandon Williams | GSW | PG | 288 | — |
| Nicolas Batum | LAC | SF,PF | 289 | — |
| Mouhamed Gueye | ATL | PF,C | 290 | — |
| Simone Fontecchio | MIA | SF,PF | 291 | — |
| Kentavious Caldwell-Pope | PHI | SG,SF | 292 | — |
| Quinten Post | MEM | C | 293 | — |
| Miles McBride | NYK | PG,SG | 294 | — |
| Terance Mann | BKN | SG,SF | 295 | — |
| Will Richard | GSW | SG,SF | 297 | — |
| Luka Garza | BOS | C | 298 | — |
| Jordan Walsh | BOS | SF,PF | 299 | — |

