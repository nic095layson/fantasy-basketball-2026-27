# Yahoo market consolidation — 2026-09-22

Owner ask (2026-09-16): consolidate and average Yahoo's rankings into the internal database. Consolidated per the standing work order: Yahoo lands as reference data (`yahoo-2026-09-22.csv`) and the average lands as the market-lens consensus board (`consensus-2026-09-22.csv`) — mean of the available rank signals (our board rank, Yahoo XRank capped at 300, Yahoo ADP), re-ranked over all pool players. The first-principles board itself is UNCHANGED (owner decision 2026-08-21: reference, not a blend; replacing marketRanks with real market data remains the work order's gated step 5).

Yahoo is a single outlet: per fix F2, nothing here changes a pool row. Team mismatches and coverage gaps below are flags for the next pull's watchlist.

---

## A. Consensus board top 30 (full file: consensus-2026-09-22.csv)

| cons # | player | avg | our # | XRank | ADP |
|---|---|---|---|---|---|
| 1 | Victor Wembanyama | 1.53 | 2 | 1 | 1.6 |
| 2 | Nikola Jokic | 2.33 | 3 | 2 | 2.0 |
| 3 | Shai Gilgeous-Alexander | 3.13 | 1 | 4 | 4.4 |
| 4 | Luka Doncic | 3.57 | 4 | 3 | 3.7 |
| 5 | Tyrese Maxey | 6.73 | 5 | 6 | 9.2 |
| 6 | Cade Cunningham | 7.5 | 11 | 5 | 6.5 |
| 7 | Anthony Edwards | 8.17 | 8 | 7 | 9.5 |
| 8 | Jayson Tatum | 11.8 | 17 | 8 | 10.4 |
| 9 | Karl-Anthony Towns | 12.33 | 6 | 16 | 15.0 |
| 10 | Cooper Flagg | 12.33 | 14 | 13 | 10.0 |
| 11 | Donovan Mitchell | 13.6 | 15 | 11 | 14.8 |
| 12 | Jalen Johnson | 16.17 | 26 | 10 | 12.5 |
| 13 | Tyrese Haliburton | 19.27 | 28 | 12 | 17.8 |
| 14 | Austin Reaves | 19.97 | 18 | 20 | 21.9 |
| 15 | Stephen Curry | 20.83 | 12 | 26 | 24.5 |
| 16 | Scottie Barnes | 20.97 | 35 | 14 | 13.9 |
| 17 | Chet Holmgren | 21.1 | 10 | 27 | 26.3 |
| 18 | Kevin Durant | 21.43 | 32 | 15 | 17.3 |
| 19 | Devin Booker | 21.6 | 13 | 24 | 27.8 |
| 20 | Jamal Murray | 22.4 | 30 | 17 | 20.2 |
| 21 | Domantas Sabonis | 23.83 | 20 | 22 | 29.5 |
| 22 | Josh Giddey | 24.53 | 31 | 18 | 24.6 |
| 23 | Amen Thompson | 24.7 | 29 | 21 | 24.1 |
| 24 | Giannis Antetokounmpo | 25.17 | 58 | 9 | 8.5 |
| 25 | Evan Mobley | 25.73 | 19 | 28 | 30.2 |
| 26 | Kawhi Leonard | 28.43 | 25 | 33 | 27.3 |
| 27 | Trae Young | 28.6 | 40 | 19 | 26.8 |
| 28 | Anthony Davis | 29.4 | 7 | 44 | 37.2 |
| 29 | LaMelo Ball | 29.67 | 41 | 23 | 25.0 |
| 30 | Trey Murphy III | 31.83 | 21 | 35 | 39.5 |

---

## B. Market arbitrage vs fresh Yahoo ADP (§5.3 / Pass E)
**Values** = our rank 15+ picks ahead of ADP; **Fades** = the reverse. z-lean = the two categories our board leans on most/least — the structural 'why', for the owner to accept or reject.

**Read the deep fades with care:** Yahoo publishes ADP only for its top 193 rows (max 122.0), so a player we rank well below that shows a mechanical 15+ 'fade' merely by having an ADP at all. The real adjudication items are the fades among players we rank inside ~140; below that, read a fade as 'the room drafts him at all', not as a precise gap.

### Values (44) — we're higher than the room

| gap | player | our # | ADP | our z-lean |
|---|---|---|---|---|
| +57 | Myles Turner | 42 | 99 | +BLK, +TOV / -STL, -AST |
| +56 | Ty Jerome | 51 | 107 | +STL, +FT% / -BLK, -REB |
| +56 | Tari Eason | 65 | 121 | +STL, +TOV / -PTS, -AST |
| +53 | Dyson Daniels | 9 | 62 | +STL, +TOV / -PTS, -FT% |
| +52 | Cam Johnson | 61 | 113 | +3PM, +FT% / -BLK, -REB |
| +49 | Jimmy Butler | 68 | 117 | +FT%, +STL / -BLK, -3PM |
| +49 | Kristaps Porzingis | 52 | 101 | +BLK, +REB / -AST, -STL |
| +44 | Fred VanVleet | 76 | 120 | +STL, +AST / -REB, -FG% |
| +43 | Josh Hart | 53 | 96 | +REB, +STL / -BLK, -PTS |
| +42 | Ajay Mitchell | 72 | 114 | +STL, +FT% / -BLK, -REB |
| +41 | Darius Garland | 23 | 64 | +AST, +3PM / -REB, -TOV |
| +41 | PJ Washington | 77 | 118 | +REB, +TOV / -FT%, -AST |
| +39 | John Collins | 78 | 117 | +FG%, +TOV / -AST, -STL |
| +38 | Christian Braun | 83 | 121 | +TOV, +FG% / -AST, -BLK |
| +36 | Kyrie Irving | 16 | 52 | +FT%, +3PM / -BLK, -REB |
| +34 | Zach LaVine | 73 | 106 | +3PM, +PTS / -BLK, -REB |
| +33 | Kel'el Ware | 39 | 72 | +BLK, +REB / -STL, -AST |
| +32 | Jaden McDaniels | 55 | 87 | +TOV, +STL / -PTS, -AST |
| +32 | Jalen Suggs | 79 | 111 | +STL, +3PM / -FG%, -REB |
| +32 | Sandro Mamukelashvili | 86 | 118 | +TOV, +FG% / -PTS, -AST |
| +31 | Paul George | 50 | 81 | +STL, +3PM / -TOV, -FG% |
| +30 | Anthony Davis | 7 | 37 | +BLK, +REB / -TOV, -3PM |
| +29 | Nic Claxton | 62 | 91 | +BLK, +FG% / -3PM, -FT% |
| +29 | Joel Embiid | 22 | 51 | +FT%, +PTS / -STL, -TOV |
| +27 | Toumani Camara | 85 | 112 | +STL, +TOV / -AST, -PTS |

### Fades (90) — the room is higher than us

| gap | player | our # | ADP | our z-lean |
|---|---|---|---|---|
| -133 | Adem Bona | 235 | 102 | +TOV, +BLK / -3PM, -PTS |
| -128 | Andre Drummond | 236 | 108 | +TOV, +REB / -3PM, -PTS |
| -125 | Morez Johnson Jr. | 242 | 117 | +TOV, +FG% / -PTS, -STL |
| -124 | Jusuf Nurkic | 238 | 114 | +TOV, +FG% / -3PM, -PTS |
| -123 | Mikel Brown | 240 | 117 | +AST, +TOV / -PTS, -REB |
| -122 | AJ Green | 221 | 99 | +TOV, +3PM / -REB, -STL |
| -114 | Jaime Jaquez Jr | 218 | 104 | +TOV, +FG% / -PTS, -3PM |
| -110 | Neemias Queta | 223 | 113 | +FG%, +TOV / -PTS, -3PM |
| -104 | Jaylen Brown | 133 | 28 | +PTS, +3PM / -TOV, -FT% |
| -103 | Jonathan Kuminga | 220 | 117 | +TOV, +REB / -STL, -FT% |
| -100 | LeBron James | 140 | 40 | +AST, +FG% / -FT%, -TOV |
| -98 | Darius Acuff | 208 | 110 | +AST, +FT% / -FG%, -REB |
| -98 | Kevin Porter Jr | 215 | 117 | +TOV, +FT% / -REB, -PTS |
| -96 | Paolo Banchero | 130 | 34 | +PTS, +REB / -FT%, -TOV |
| -96 | Kyle Kuzma | 214 | 118 | +TOV, +REB / -FT%, -STL |
| -95 | Ryan Rollins | 171 | 76 | +TOV, +STL / -PTS, -REB |
| -92 | Davion Mitchell | 211 | 119 | +AST, +TOV / -PTS, -REB |
| -92 | AJ Dybantsa | 169 | 77 | +PTS, +REB / -TOV, -FG% |
| -90 | RJ Barrett | 201 | 111 | +PTS, +AST / -STL, -FT% |
| -88 | Maxime Raynaud | 207 | 119 | +TOV, +FG% / -3PM, -STL |
| -87 | Dillon Brooks | 202 | 115 | +TOV, +3PM / -AST, -REB |
| -85 | Derik Queen | 163 | 78 | +REB, +FG% / -PTS, -3PM |
| -82 | Dylan Harper | 166 | 84 | +AST, +STL / -BLK, -REB |
| -80 | Duncan Robinson | 186 | 106 | +3PM, +TOV / -REB, -STL |
| -77 | Donovan Clingan | 118 | 41 | +BLK, +REB / -PTS, -3PM |

---

## C. Team-code mismatches (1) — FLAGS ONLY (F2: single source)

| our # | player | our team | yahoo team |
|---|---|---|---|
| 243 | Cam Whitmore | CLE | DEN |

---

## D. Availability disagreements (6) — our GP ≤ 40, market still pricing them

| our # | player | our GP | XRank | ADP |
|---|---|---|---|---|
| 25 | Kawhi Leonard | 35 | 33 | 27.3 |
| 126 | Mark Williams | 15 | 252 | 106.2 |
| 68 | Jimmy Butler | 20 | 134 | 117.4 |
| 136 | Shaedon Sharpe | 18 | 213 | 117.6 |
| 243 | Cam Whitmore | 30 | 193 | — |
| 173 | Donte DiVincenzo | 15 | 216 | — |

---

## E. Coverage gaps — Yahoo names not in our pool (76; 7 carry an ADP inside 140)
Names the room is drafting that our database cannot price. Owner decides which enter the pool (each needs a sourced projection row).

| player | team | pos | XRank | ADP |
|---|---|---|---|---|
| Bronny James | LAL | PG,SG | 464 | 100.3 |
| Al Horford | GSW | PF,C | 200 | 101.2 |
| Aday Mara | OKC | C | 622 | 101.8 |
| Luke Kennard | PHX | SG,SF | 238 | 102.7 |
| Johni Broome | LAC | C | 676 | 104.2 |
| Aaron Wiggins | ATL | SG,SF | 187 | 106.8 |
| Brayden Burries | MIL | SG | 188 | 116.2 |
| Daniss Jenkins | DET | PG,SG | 154 | — |
| Oso Ighodaro | PHX | C | 171 | — |
| Scotty Pippen Jr. | MEM | PG | 191 | — |
| Miles McBride | NYK | PG,SG | 195 | — |
| T.J. McConnell | IND | PG | 197 | — |
| Jalen Smith | CHI | PF,C | 199 | — |
| Kris Dunn | LAC | PG,SG | 211 | — |
| Max Christie | DAL | SG,SF | 212 | — |
| Ryan Kalkbrenner | CHA | C | 214 | — |
| Noah Clowney | BKN | PF,C | 217 | — |
| Luke Kornet | SAS | C | 219 | — |
| Tim Hardaway Jr. | MIA | SG,SF | 221 | — |
| Jake LaRavia | LAL | SF,PF | 223 | — |
| Dylan Cardwell | SAC | PF,C | 224 | — |
| Jaxson Hayes | UTA | C | 225 | — |
| Kevin Huerter | DET | SG,SF | 228 | — |
| Sam Merrill | CLE | SG,SF | 229 | — |
| Tony Bradley | ATL | C | 230 | — |
| Isaiah Jackson | LAC | C | 231 | — |
| Jaylon Tyson | CLE | SG,SF,PF | 232 | — |
| Jarace Walker | IND | SF,PF | 233 | — |
| Ja'Kobe Walter | TOR | PG,SG | 234 | — |
| Jordan Goodwin | PHX | PG,SG | 235 | — |
| Jaylin Williams | OKC | PF,C | 236 | — |
| Quinten Post | MEM | C | 239 | — |
| Moritz Wagner | BKN | C | 241 | — |
| Kobe Sanders | LAC | SG,SF | 242 | — |
| Dennis Schröder | CHA | PG,SG | 245 | — |
| Cam Spencer | MEM | PG,SG | 246 | — |
| Karlo Matković | NOP | PF,C | 247 | — |
| Baylor Scheierman | BOS | SG,SF | 249 | — |
| Gui Santos | GSW | SF,PF | 250 | — |
| Justin Champagnie | WAS | SF,PF | 253 | — |
| Javonte Green | DET | SG,SF | 254 | — |
| Harrison Barnes | SAS | PF | 255 | — |
| Moses Moody | GSW | SG,SF,PF | 257 | — |
| Russell Westbrook | SAC | PG,SG | 259 | — |
| Precious Achiuwa | SAC | PF,C | 261 | — |
| Gary Payton II | GSW | SG,SF | 263 | — |
| Bruce Brown | NYK | PG,SG | 264 | — |
| Ziaire Williams | LAL | SG,SF | 265 | — |
| Dominick Barlow | PHI | PF,C | 266 | — |
| Jamal Shead | TOR | PG | 267 | — |
| John Konchar | NYK | SG,SF | 268 | — |
| Jose Alvarado | NYK | PG | 269 | — |
| Jonas Valančiūnas | DEN | C | 270 | — |
| Dru Smith | MIA | PG,SG | 272 | — |
| Pelle Larsson | MIA | SG,SF | 273 | — |
| Vít Krejčí | POR | SG,SF | 274 | — |
| Jock Landale | ATL | C | 275 | — |
| Dean Wade | PHI | SF,PF | 276 | — |
| Isaac Okoro | CHI | SG,SF | 277 | — |
| Brandon Williams | GSW | PG | 278 | — |
| Ryan Dunn | PHX | SF,PF | 279 | — |
| Nicolas Batum | LAC | SF,PF | 280 | — |
| Mouhamed Gueye | ATL | PF,C | 282 | — |
| Simone Fontecchio | MIA | SF,PF | 283 | — |
| Kentavious Caldwell-Pope | PHI | SG,SF | 284 | — |
| Marvin Bagley III | DEN | PF,C | 285 | — |
| Terance Mann | BKN | SG,SF | 286 | — |
| Will Richard | GSW | SG,SF | 288 | — |
| Luka Garza | BOS | C | 289 | — |
| Jordan Walsh | BOS | SF,PF | 290 | — |
| Bones Hyland | MIN | PG,SG | 291 | — |
| Craig Porter Jr. | CLE | PG,SG | 292 | — |
| Caris LeVert | MIL | SG,SF | 293 | — |
| Sion James | CHA | SG,SF | 294 | — |
| Mike Conley | BOS | PG | 295 | — |
| Ben Sheppard | IND | SG,SF | 296 | — |

---

## F. What Yahoo changed since `yahoo-2026-09-15.csv`
Same-outlet comparison (287 names in both files, 286 expert-ranked in both). Moves are XRank vs XRank; ADP before and after are shown beside them. A rank move is Yahoo re-pricing a player; a team change here is Yahoo's own roster data moving between the two pastes — still ONE outlet, so it flags a transaction to verify at the next pull, never a row edit.

### Risers (20 shown; XRank move ≥ 10 places, inside 150 on either side)

| move | player | XRank before | XRank after | ADP before | ADP after |
|---|---|---|---|---|---|
| +53 | Khaman Maluach | 168 | 115 | 121 | 120 |
| +52 | Aaron Nesmith | 199 | 147 | 75 | 104 |
| +44 | Tre Jones | 173 | 129 | — | — |
| +39 | Devin Vassell | 161 | 122 | 117 | 117 |
| +37 | Aaron Gordon | 156 | 119 | 112 | 113 |
| +35 | Tobias Harris | 183 | 148 | — | 115 |
| +32 | Moussa Diabaté | 177 | 145 | 99 | 110 |
| +30 | Nikola Vučević | 174 | 144 | 112 | 115 |
| +30 | Herbert Jones | 179 | 149 | — | — |
| +29 | Zach LaVine | 125 | 96 | 120 | 106 |
| +28 | Davion Mitchell | 137 | 109 | 111 | 119 |
| +28 | Cason Wallace | 154 | 126 | 114 | 118 |
| +27 | Cedric Coward | 108 | 81 | 100 | 91 |
| +25 | Andrew Nembhard | 130 | 105 | 121 | 116 |
| +24 | Christian Braun | 167 | 143 | 118 | 121 |
| +22 | Jakob Poeltl | 136 | 114 | 122 | 122 |
| +22 | Brandon Ingram | 77 | 55 | 75 | 65 |
| +21 | Reed Sheppard | 138 | 117 | 116 | 120 |
| +19 | Toumani Camara | 120 | 101 | 119 | 112 |
| +19 | Tari Eason | 158 | 139 | — | 121 |

### Fallers (20 shown)

| move | player | XRank before | XRank after | ADP before | ADP after |
|---|---|---|---|---|---|
| -156 | Mark Williams | 96 | 252 | 103 | 106 |
| -129 | DeMar DeRozan | 122 | 251 | 117 | 117 |
| -67 | Shaedon Sharpe | 146 | 213 | 114 | 118 |
| -57 | Keaton Wagler | 149 | 206 | 122 | 119 |
| -46 | Ty Jerome | 87 | 133 | 96 | 107 |
| -40 | Darius Acuff Jr. | 116 | 156 | 110 | 110 |
| -38 | Wendell Carter Jr. | 103 | 141 | 110 | 112 |
| -36 | Daniel Gafford | 134 | 170 | 98 | 107 |
| -29 | Egor Dëmin | 135 | 164 | 121 | 120 |
| -26 | Brook Lopez | 139 | 165 | 78 | 101 |
| -24 | Cameron Johnson | 148 | 172 | 108 | 113 |
| -23 | Anthony Davis | 21 | 44 | 25 | 37 |
| -20 | Darryn Peterson | 93 | 113 | 93 | 98 |
| -20 | Saddiq Bey | 126 | 146 | 123 | 122 |
| -18 | Neemias Queta | 100 | 118 | 105 | 113 |
| -18 | Quentin Grimes | 140 | 158 | 122 | 122 |
| -17 | Fred VanVleet | 119 | 136 | 121 | 120 |
| -15 | Jaden McDaniels | 74 | 89 | 78 | 87 |
| -15 | Kawhi Leonard | 18 | 33 | 20 | 27 |
| -14 | Ja Morant | 89 | 103 | 91 | 92 |

### Newly expert-ranked (1) — placeholder tier before, ranked now

| XRank now | player | ADP before |
|---|---|---|
| 676 | Johni Broome | 105 |

### Yahoo team changes (2) — transaction flags for the next pull

| XRank | player | before | after |
|---|---|---|---|
| 264 | Bruce Brown | DEN | NYK |
| 268 | John Konchar | MIN | NYK |

### Entered Yahoo's list inside the draftable 156 (0)

| XRank | player | team |
|---|---|---|

### Left Yahoo's list from inside the draftable 156 (0)

| XRank before | player | team | ADP before |
|---|---|---|---|

---

## G. Yahoo's two pages on 2026-09-22: this file (draft-analysis XRank + ADP) vs the 9-cat RANKINGS page
237 players on both pages. The 9-cat rankings page (reference file `yahoo-9cat-rankings-2026-09-22.csv`) is a different expert ordering from this page's XRank; the deck prices by ADP where present, else this page's XRank (F8). Differences here are Yahoo disagreeing with Yahoo — read them as the width of the expert band, not as a price.

### 9-cat page ranks him higher than this page (top 15)

| 9-cat rank | XRank here | ADP | player | our # |
|---|---|---|---|---|
| 116 | 251 | 116.6 | DeMar DeRozan | 165 |
| 154 | 273 | — | Pelle Larsson | — |
| 166 | 252 | 106.2 | Mark Williams | 126 |
| 198 | 261 | — | Precious Achiuwa | — |
| 125 | 186 | 105.1 | Rui Hachimura | 164 |
| 224 | 281 | — | Isaiah Collier | 225 |
| 231 | 285 | — | Marvin Bagley III | — |
| 237 | 291 | — | Bones Hyland | — |
| 180 | 223 | — | Jake LaRavia | — |
| 207 | 250 | — | Gui Santos | — |
| 229 | 271 | — | Marcus Smart | 150 |
| 243 | 284 | — | Kentavious Caldwell-Pope | — |
| 161 | 200 | 101.2 | Al Horford | — |
| 206 | 245 | — | Dennis Schröder | — |
| 91 | 128 | 120.7 | Keegan Murray | 110 |

### 9-cat page ranks him lower than this page (top 15)

| 9-cat rank | XRank here | ADP | player | our # |
|---|---|---|---|---|
| 244 | 188 | 116.2 | Brayden Burries | — |
| 241 | 189 | — | De'Anthony Melton | 149 |
| 201 | 159 | 117.3 | Morez Johnson Jr. | 242 |
| 216 | 176 | 116.1 | Kyle Filipowski | 129 |
| 193 | 155 | 117.4 | Jeremiah Fears | 188 |
| 210 | 174 | — | Jordan Poole | 80 |
| 218 | 185 | — | Jaylen Wells | 198 |
| 238 | 206 | 119.0 | Keaton Wagler | 183 |
| 213 | 182 | 107.9 | Andre Drummond | 236 |
| 151 | 120 | 116.3 | Kyshawn George | 146 |
| 130 | 101 | 112.0 | Toumani Camara | 85 |
| 164 | 135 | 118.7 | Maxime Raynaud | 207 |
| 196 | 167 | — | Sam Hauser | 216 |
| 195 | 168 | 115.7 | Isaiah Stewart | 172 |
| 185 | 158 | 122.0 | Quentin Grimes | 167 |

### The room vs the 9-cat page: biggest reaches (ADP well ahead of the 9-cat rank)

| ADP | 9-cat rank | player | our # |
|---|---|---|---|
| 101.8 | 249 | Aday Mara | — |
| 116.2 | 244 | Brayden Burries | — |
| 119.0 | 238 | Keaton Wagler | 183 |
| 107.9 | 222 | Jared McCain | 154 |
| 107.9 | 213 | Andre Drummond | 236 |
| 98.4 | 199 | Alex Caruso | 125 |
| 116.1 | 216 | Kyle Filipowski | 129 |
| 105.7 | 203 | Duncan Robinson | 186 |
| 102.2 | 194 | Anfernee Simons | 84 |
| 117.3 | 201 | Morez Johnson Jr. | 242 |
| 117.6 | 200 | Shaedon Sharpe | 136 |
| 115.7 | 195 | Isaiah Stewart | 172 |

### The room vs the 9-cat page: biggest fades (ADP well behind the 9-cat rank)

| ADP | 9-cat rank | player | our # |
|---|---|---|---|
| 120.7 | 91 | Keegan Murray | 110 |
| 111.1 | 90 | Jalen Suggs | 79 |
| 53.1 | 34 | Desmond Bane | 38 |
| 119.1 | 101 | Davion Mitchell | 211 |
| 88.0 | 70 | Coby White | 103 |
| 56.0 | 39 | Keyonte George | 115 |
| 79.3 | 63 | Mikal Bridges | 56 |
| 112.6 | 97 | Neemias Queta | 223 |
| 39.5 | 24 | Trey Murphy III | 21 |
| 47.2 | 32 | Brandon Miller | 60 |
| 52.1 | 37 | Kyrie Irving | 16 |
| 117.1 | 102 | John Collins | 78 |

