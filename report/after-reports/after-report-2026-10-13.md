# After-report — 2026-10-13 data pull + deck v62 (the daily pull on top of the morning's MG pass)

**Owner request (2026-10-13, verbatim):** "Daily refresh pull and after report please" — WO-3's daily pull.

Pull window: 2026-10-12 → 2026-10-13 (from the 10/12 pull's fetch at 14:42 UTC to this pull's fetch at 13:58 UTC on 10/13: the five preseason games of 10/12 — Trail Blazers 119, London Lions 66 (Portland); Hawks 113, Thunder 110 (Atlanta); Nets 131, Wizards 122 (Washington); Timberwolves 122, Knicks 104 (New York); Jazz 119, Spurs 109 (Salt Lake City) — all final. Tonight's five games — Cavaliers at Magic, Knicks at Raptors (Kawhi's debut), Pacers at Thunder, Warriors vs Lakers in Las Vegas, Trail Blazers at Kings — are the next pull's.)
Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07`, exit 0 (one kit cell changed today: Raynaud's GP, D-1012-1).

**Method.** The five box scores read from ESPN's own feed (scoreboard and summary endpoints) before any search — starters, minutes, lines, DNP reasons and each summary's injury block — cross-referenced to both planes by script under `python3 -I` on the downloaded JSON (`scratchpad pull1013/boxscores.txt`, `box.json`, 84 pool-row lines). ESPN's league-wide injuries feed (137 rows, fetched 10/13 13:58 UTC) diffed against the deck's 51-row tag inventory in both directions by script (`feed_diff.json`), and every feed item dated inside the window on a pool row (34) written to the deck. The Basketball-Reference 2026-27 transactions page read directly (the 10/9–10/11 blocks; the 10/12 pull's newest was 10/8); ESPN's roster API for all 30 teams (the verifier, 335/335); ESPN's scoreboards 10/12–10/13. Then one sweep of 32 dated queries (5 standard, 27 extended; the five standard recap queries returned old games and were re-run extended): one recap query per game, one team-shaped query for each of the seven teams in the watch set (CHI, GSW, LAC, MIL, NOP, POR, TOR), a dedicated query for each of the ten flagged receipts, and five narrowed follow-ups where the first query returned stale items (Thomas, Ivey, Ball, Mathurin, Dillingham). Egress-blocked as on every pull: Yahoo, SI, CBS, RotoWire, NBA.com's article pages and the other sports domains (their items rest on dated search summaries, labeled where they stand alone; the query list and every result are pinned in `scratchpad pull1013/search_results_1013.txt`).

## 1. Roster changes

None on a pool row. The ledger's blocks newer than 10/8: 10/11 — the Warriors waived Miles Kelly, the Wizards waived Skal Labissière; 10/10 — the Pelicans waived Christian Koloko (HoopsHype 10/9 via the Pelicans shadow query; Jalon Moore signed in his place), the Warriors signed Brandin Podziemski to a contract extension (a pool row; a contract, not a placement — no cell changes); 10/9 — four Exhibit 10 signings (Moore NOP, Castro LAL, Robinson and Yaacov CLE), none a pool row. Rob Dillingham's 9/26–27 trade to Charlotte and 9/28 release surfaced in his receipt query (Yahoo, Fox Sports) — already reflected: he is `out-unsigned` on the deck and an unsigned row on the kit. No pool row changed team, entered or left; `report/roster-provenance.csv` is byte-identical to yesterday's.

## 2. The box scores (ESPN's feed; the line is the evidence where no outlet named the row)

Five finals. Rows a dated outlet named (the recap queries): Anthony Edwards 26 and Jaden McDaniels 22 at the Garden, 9-of-13 from three between them on 18 Minnesota threes (Star Tribune, Canis Hoopus, TalkBasket, Yahoo); Michael Porter Jr. 22 on 8-of-13 and Julius Randle 14 with 9 assists for Brooklyn, Kyshawn George 21 with 3 steals, AJ Dybantsa 14 and Bub Carrington 14 for Washington (NetsDaily/Yahoo, Bullets Forever, TalkBasket, sofascore); Aday Mara 17/10/6 in 33 minutes starting at center — CBS Sports says five blocks, TalkBasket four, the box score four — with Jock Landale 17/6/5, Nickeil Alexander-Walker 16/6/5 and Jalen Wilson 12 and 8 for Atlanta (CBS Sports, TalkBasket, Atlanta News First); Scoot Henderson 14 on 4-of-5 threes, Yang Hansen 13 (SI, Yahoo, Blazer's Edge, Sky Sports, TalkBasket) and Jeremy Sochan 8 and 8 off the bench (the Polish outlets: weszło, TVP Sport, Polsat Sport, Eurosport PL); Darryn Peterson 14 with 5 assists, Lauri Markkanen 11, Ace Bailey's defense, five Jazz starters in double figures (TalkBasket, Bleacher Report, SLC Dunk/Yahoo, Deseret News, KSL); Brunson and Towns 'missing badly from deep' (Posting and Toasting/Yahoo). Every other line below rests on the box score alone and is labeled so in the deck notes.

| game | player | team | plane | role | line (evidence: ESPN's box score) |
|---|---|---|---|---|---|
| Trail Blazers 119, London Lions 66 | Toumani Camara | POR | deck+kit | starter | 15 min, 14 pts, 2 reb, 3 ast, 1 stl, 0 blk, 1 to, FG 4-7, 3PT 2-5, FT 4-4 |
| Trail Blazers 119, London Lions 66 | Deni Avdija | POR | deck+kit | starter | 17 min, 9 pts, 5 reb, 4 ast, 0 stl, 0 blk, 2 to, FG 3-4, 3PT 1-1, FT 2-3 |
| Trail Blazers 119, London Lions 66 | Donovan Clingan | POR | deck+kit | starter | 15 min, 11 pts, 6 reb, 1 ast, 0 stl, 1 blk, 3 to, FG 5-7, 3PT 0-1, FT 1-1 |
| Trail Blazers 119, London Lions 66 | Jrue Holiday | POR | deck+kit | starter | 15 min, 6 pts, 5 reb, 3 ast, 0 stl, 0 blk, 0 to, FG 3-5, 3PT 0-2, FT 0-0 |
| Trail Blazers 119, London Lions 66 | Ja Morant | POR | deck+kit | starter | 14 min, 5 pts, 0 reb, 5 ast, 3 stl, 0 blk, 1 to, FG 2-6, 3PT 1-2, FT 0-0 |
| Trail Blazers 119, London Lions 66 | Jeremy Sochan | POR | deck+kit | bench | 21 min, 8 pts, 8 reb, 2 ast, 1 stl, 0 blk, 1 to, FG 4-6, 3PT 0-0, FT 0-0 |
| Trail Blazers 119, London Lions 66 | Yang Hansen | POR | deck+kit | bench | 21 min, 13 pts, 4 reb, 4 ast, 0 stl, 0 blk, 2 to, FG 6-8, 3PT 1-1, FT 0-0 |
| Trail Blazers 119, London Lions 66 | Vit Krejci | POR | deck+kit | bench | 21 min, 10 pts, 5 reb, 2 ast, 3 stl, 0 blk, 1 to, FG 3-6, 3PT 2-4, FT 2-2 |
| Trail Blazers 119, London Lions 66 | Scoot Henderson | POR | deck+kit | bench | 16 min, 14 pts, 0 reb, 3 ast, 2 stl, 0 blk, 1 to, FG 4-7, 3PT 4-5, FT 2-3 |
| Trail Blazers 119, London Lions 66 | Robert Williams III | POR | deck+kit | bench | did not play (coach's decision on the box score) |
| Trail Blazers 119, London Lions 66 | Damian Lillard | POR | deck+kit | bench | did not play (coach's decision on the box score) |
| Trail Blazers 119, London Lions 66 | Shaedon Sharpe | POR | deck+kit | bench | did not play (coach's decision on the box score) |
| Hawks 113, Thunder 110 | Aday Mara | OKC | deck+kit | starter | 33 min, 17 pts, 10 reb, 6 ast, 0 stl, 4 blk, 5 to, FG 4-9, 3PT 0-1, FT 9-12 |
| Hawks 113, Thunder 110 | Corey Kispert | ATL | deck | starter | 26 min, 6 pts, 1 reb, 2 ast, 0 stl, 2 blk, 0 to, FG 2-11, 3PT 2-9, FT 0-0 |
| Hawks 113, Thunder 110 | Jock Landale | ATL | deck+kit | starter | 21 min, 17 pts, 6 reb, 5 ast, 3 stl, 2 blk, 0 to, FG 7-11, 3PT 1-3, FT 2-2 |
| Hawks 113, Thunder 110 | Nickeil Alexander-Walker | ATL | deck+kit | starter | 25 min, 16 pts, 6 reb, 5 ast, 1 stl, 0 blk, 3 to, FG 4-10, 3PT 4-7, FT 4-4 |
| Hawks 113, Thunder 110 | Kingston Flemings | ATL | deck+kit | starter | 28 min, 7 pts, 2 reb, 7 ast, 1 stl, 0 blk, 0 to, FG 3-11, 3PT 0-0, FT 1-2 |
| Hawks 113, Thunder 110 | Dorian Finney-Smith | ATL | deck | bench | 17 min, 8 pts, 1 reb, 0 ast, 0 stl, 0 blk, 0 to, FG 3-6, 3PT 2-4, FT 0-0 |
| Hawks 113, Thunder 110 | Jalen Wilson | ATL | deck+kit | bench | 30 min, 12 pts, 8 reb, 1 ast, 1 stl, 0 blk, 2 to, FG 4-13, 3PT 4-9, FT 0-0 |
| Hawks 113, Thunder 110 | Zuby Ejiofor | ATL | kit | bench | 23 min, 15 pts, 9 reb, 3 ast, 0 stl, 1 blk, 3 to, FG 5-9, 3PT 1-2, FT 4-4 |
| Nets 131, Wizards 122 | Julius Randle | BKN | deck+kit | starter | 23 min, 14 pts, 4 reb, 9 ast, 1 stl, 0 blk, 3 to, FG 5-8, 3PT 2-4, FT 2-4 |
| Nets 131, Wizards 122 | Michael Porter Jr. | BKN | deck+kit | starter | 24 min, 22 pts, 4 reb, 0 ast, 2 stl, 1 blk, 3 to, FG 8-13, 3PT 2-7, FT 4-5 |
| Nets 131, Wizards 122 | Day'Ron Sharpe | BKN | deck+kit | starter | 21 min, 4 pts, 2 reb, 3 ast, 3 stl, 1 blk, 1 to, FG 1-1, 3PT 1-1, FT 1-4 |
| Nets 131, Wizards 122 | Keon Ellis | BKN | deck+kit | starter | 21 min, 15 pts, 1 reb, 0 ast, 0 stl, 0 blk, 0 to, FG 4-7, 3PT 3-4, FT 4-5 |
| Nets 131, Wizards 122 | Egor Demin | BKN | deck+kit | starter | 22 min, 4 pts, 0 reb, 3 ast, 1 stl, 0 blk, 1 to, FG 2-8, 3PT 0-5, FT 0-0 |
| Nets 131, Wizards 122 | Noah Clowney | BKN | deck+kit | bench | 22 min, 15 pts, 3 reb, 4 ast, 1 stl, 0 blk, 0 to, FG 5-8, 3PT 4-6, FT 1-1 |
| Nets 131, Wizards 122 | Moritz Wagner | BKN | deck+kit | bench | 18 min, 13 pts, 5 reb, 1 ast, 2 stl, 0 blk, 1 to, FG 4-8, 3PT 0-3, FT 5-6 |
| Nets 131, Wizards 122 | Terance Mann | BKN | deck+kit | bench | 9 min, 3 pts, 2 reb, 0 ast, 0 stl, 0 blk, 1 to, FG 1-2, 3PT 1-1, FT 0-0 |
| Nets 131, Wizards 122 | AJ Dybantsa | WSH | deck+kit | starter | 25 min, 14 pts, 4 reb, 3 ast, 1 stl, 1 blk, 3 to, FG 5-12, 3PT 1-3, FT 3-4 |
| Nets 131, Wizards 122 | Kyshawn George | WSH | deck+kit | starter | 25 min, 21 pts, 1 reb, 4 ast, 3 stl, 0 blk, 0 to, FG 6-7, 3PT 3-3, FT 6-6 |
| Nets 131, Wizards 122 | Deandre Ayton | WSH | deck+kit | starter | 25 min, 4 pts, 7 reb, 4 ast, 0 stl, 0 blk, 1 to, FG 2-4, 3PT 0-0, FT 0-0 |
| Nets 131, Wizards 122 | Alex Sarr | WSH | deck+kit | starter | 23 min, 6 pts, 9 reb, 0 ast, 0 stl, 0 blk, 3 to, FG 3-10, 3PT 0-3, FT 0-0 |
| Nets 131, Wizards 122 | Trae Young | WSH | deck+kit | starter | 28 min, 11 pts, 3 reb, 11 ast, 1 stl, 0 blk, 8 to, FG 1-5, 3PT 1-4, FT 8-8 |
| Nets 131, Wizards 122 | Justin Champagnie | WSH | deck+kit | bench | 16 min, 7 pts, 3 reb, 0 ast, 1 stl, 0 blk, 0 to, FG 3-7, 3PT 1-3, FT 0-0 |
| Nets 131, Wizards 122 | Tre Mann | WSH | deck | bench | 12 min, 3 pts, 0 reb, 1 ast, 0 stl, 0 blk, 0 to, FG 1-3, 3PT 1-2, FT 0-0 |
| Nets 131, Wizards 122 | Bub Carrington | WSH | deck+kit | bench | 13 min, 14 pts, 0 reb, 1 ast, 0 stl, 0 blk, 2 to, FG 3-5, 3PT 3-4, FT 5-6 |
| Nets 131, Wizards 122 | Bilal Coulibaly | WSH | deck+kit | bench | 24 min, 19 pts, 2 reb, 1 ast, 3 stl, 1 blk, 0 to, FG 7-11, 3PT 3-5, FT 2-2 |
| Nets 131, Wizards 122 | Will Riley | WSH | deck+kit | bench | 7 min, 3 pts, 1 reb, 1 ast, 0 stl, 0 blk, 1 to, FG 1-1, 3PT 1-1, FT 0-0 |
| Nets 131, Wizards 122 | Tre Johnson | WSH | deck+kit | bench | 20 min, 13 pts, 0 reb, 3 ast, 2 stl, 0 blk, 1 to, FG 5-9, 3PT 3-7, FT 0-0 |
| Nets 131, Wizards 122 | Anthony Davis | WSH | deck+kit | bench | did not play (coach's decision on the box score) |
| Nets 131, Wizards 122 | Khris Middleton | WSH | deck+kit | bench | did not play (coach's decision on the box score) |
| Timberwolves 122, Knicks 104 | Jaden McDaniels | MIN | deck+kit | starter | 24 min, 22 pts, 5 reb, 2 ast, 0 stl, 0 blk, 4 to, FG 8-12, 3PT 4-5, FT 2-2 |
| Timberwolves 122, Knicks 104 | Rudy Gobert | MIN | deck+kit | starter | 22 min, 2 pts, 3 reb, 3 ast, 1 stl, 1 blk, 1 to, FG 1-2, 3PT 0-0, FT 0-0 |
| Timberwolves 122, Knicks 104 | LaMelo Ball | MIN | deck+kit | starter | 22 min, 10 pts, 3 reb, 7 ast, 0 stl, 1 blk, 5 to, FG 3-7, 3PT 1-3, FT 3-3 |
| Timberwolves 122, Knicks 104 | Anthony Edwards | MIN | deck+kit | starter | 25 min, 26 pts, 3 reb, 3 ast, 1 stl, 0 blk, 2 to, FG 8-16, 3PT 5-8, FT 5-7 |
| Timberwolves 122, Knicks 104 | Joan Beringer | MIN | deck+kit | bench | 14 min, 5 pts, 4 reb, 0 ast, 1 stl, 1 blk, 0 to, FG 1-3, 3PT 0-0, FT 3-6 |
| Timberwolves 122, Knicks 104 | Ayo Dosunmu | MIN | deck+kit | bench | 20 min, 11 pts, 4 reb, 2 ast, 3 stl, 1 blk, 2 to, FG 3-6, 3PT 3-5, FT 2-2 |
| Timberwolves 122, Knicks 104 | Bones Hyland | MIN | deck+kit | bench | 14 min, 6 pts, 2 reb, 2 ast, 0 stl, 0 blk, 1 to, FG 3-9, 3PT 0-3, FT 0-0 |
| Timberwolves 122, Knicks 104 | Jonathan Kuminga | MIN | deck+kit | bench | did not play (coach's decision on the box score) |
| Timberwolves 122, Knicks 104 | Donte DiVincenzo | MIN | deck+kit | bench | did not play (coach's decision on the box score) |
| Timberwolves 122, Knicks 104 | Terrence Shannon Jr. | MIN | deck+kit | bench | did not play (coach's decision on the box score) |
| Timberwolves 122, Knicks 104 | OG Anunoby | NY | deck+kit | starter | 22 min, 15 pts, 2 reb, 1 ast, 3 stl, 0 blk, 0 to, FG 4-8, 3PT 1-3, FT 6-6 |
| Timberwolves 122, Knicks 104 | Karl-Anthony Towns | NY | deck+kit | starter | 22 min, 11 pts, 2 reb, 4 ast, 1 stl, 0 blk, 3 to, FG 3-6, 3PT 1-4, FT 4-4 |
| Timberwolves 122, Knicks 104 | Josh Hart | NY | deck+kit | starter | 22 min, 2 pts, 3 reb, 3 ast, 1 stl, 0 blk, 2 to, FG 1-2, 3PT 0-1, FT 0-0 |
| Timberwolves 122, Knicks 104 | Mikal Bridges | NY | deck+kit | starter | 22 min, 9 pts, 2 reb, 2 ast, 0 stl, 0 blk, 1 to, FG 3-6, 3PT 1-2, FT 2-2 |
| Timberwolves 122, Knicks 104 | Jalen Brunson | NY | deck+kit | starter | 22 min, 20 pts, 5 reb, 3 ast, 3 stl, 0 blk, 2 to, FG 6-13, 3PT 1-4, FT 7-8 |
| Timberwolves 122, Knicks 104 | Andre Drummond | NY | kit | bench | 12 min, 4 pts, 4 reb, 0 ast, 1 stl, 3 blk, 0 to, FG 1-2, 3PT 0-0, FT 2-2 |
| Timberwolves 122, Knicks 104 | Tony Bradley | NY | deck+kit | bench | 7 min, 10 pts, 2 reb, 0 ast, 0 stl, 0 blk, 0 to, FG 5-5, 3PT 0-0, FT 0-0 |
| Timberwolves 122, Knicks 104 | Jordan Clarkson | NY | deck | bench | 10 min, 5 pts, 0 reb, 0 ast, 0 stl, 1 blk, 1 to, FG 2-3, 3PT 1-1, FT 0-0 |
| Timberwolves 122, Knicks 104 | Landry Shamet | NY | deck | bench | 12 min, 2 pts, 0 reb, 1 ast, 0 stl, 0 blk, 1 to, FG 0-2, 3PT 0-2, FT 2-2 |
| Timberwolves 122, Knicks 104 | Jose Alvarado | NY | deck+kit | bench | 15 min, 4 pts, 2 reb, 2 ast, 1 stl, 0 blk, 3 to, FG 2-8, 3PT 0-2, FT 0-0 |
| Timberwolves 122, Knicks 104 | Ochai Agbaji | NY | deck | bench | 10 min, 2 pts, 2 reb, 1 ast, 0 stl, 0 blk, 0 to, FG 0-3, 3PT 0-3, FT 2-2 |
| Timberwolves 122, Knicks 104 | Miles McBride | NY | deck+kit | bench | 13 min, 3 pts, 0 reb, 0 ast, 1 stl, 0 blk, 1 to, FG 1-5, 3PT 1-4, FT 0-0 |
| Timberwolves 122, Knicks 104 | Bruce Brown | NY | deck+kit | bench | did not play (coach's decision on the box score) |
| Jazz 119, Spurs 109 | Harrison Barnes | SA | deck+kit | starter | 23 min, 19 pts, 2 reb, 1 ast, 0 stl, 0 blk, 3 to, FG 3-8, 3PT 3-7, FT 10-12 |
| Jazz 119, Spurs 109 | Keldon Johnson | SA | deck+kit | starter | 24 min, 15 pts, 4 reb, 4 ast, 2 stl, 0 blk, 1 to, FG 4-10, 3PT 0-2, FT 7-9 |
| Jazz 119, Spurs 109 | Julian Champagnie | SA | deck+kit | starter | 26 min, 14 pts, 4 reb, 0 ast, 1 stl, 1 blk, 5 to, FG 5-13, 3PT 3-9, FT 1-1 |
| Jazz 119, Spurs 109 | Luke Kornet | SA | deck+kit | starter | 22 min, 0 pts, 3 reb, 1 ast, 0 stl, 1 blk, 3 to, FG 0-2, 3PT 0-0, FT 0-0 |
| Jazz 119, Spurs 109 | Tobias Harris | SA | deck+kit | bench | did not play (coach's decision on the box score) |
| Jazz 119, Spurs 109 | Victor Wembanyama | SA | deck+kit | bench | did not play (coach's decision on the box score) |
| Jazz 119, Spurs 109 | De'Aaron Fox | SA | deck+kit | bench | did not play (coach's decision on the box score) |
| Jazz 119, Spurs 109 | Devin Vassell | SA | deck+kit | bench | did not play (coach's decision on the box score) |
| Jazz 119, Spurs 109 | Stephon Castle | SA | deck+kit | bench | did not play (coach's decision on the box score) |
| Jazz 119, Spurs 109 | Dylan Harper | SA | deck+kit | bench | did not play (coach's decision on the box score) |
| Jazz 119, Spurs 109 | Lauri Markkanen | UTAH | deck+kit | starter | 19 min, 11 pts, 1 reb, 2 ast, 2 stl, 0 blk, 3 to, FG 3-7, 3PT 1-2, FT 4-4 |
| Jazz 119, Spurs 109 | Jaren Jackson Jr. | UTAH | deck+kit | starter | 18 min, 13 pts, 3 reb, 1 ast, 1 stl, 0 blk, 2 to, FG 6-8, 3PT 1-2, FT 0-0 |
| Jazz 119, Spurs 109 | Jaxson Hayes | UTAH | deck+kit | starter | 15 min, 11 pts, 2 reb, 0 ast, 0 stl, 0 blk, 1 to, FG 4-5, 3PT 0-0, FT 3-4 |
| Jazz 119, Spurs 109 | Keyonte George | UTAH | deck+kit | starter | 16 min, 13 pts, 2 reb, 1 ast, 3 stl, 0 blk, 0 to, FG 5-7, 3PT 0-1, FT 3-4 |
| Jazz 119, Spurs 109 | Darryn Peterson | UTAH | deck+kit | starter | 24 min, 14 pts, 2 reb, 5 ast, 1 stl, 0 blk, 1 to, FG 5-10, 3PT 1-2, FT 3-3 |
| Jazz 119, Spurs 109 | Brice Sensabaugh | UTAH | kit | bench | 15 min, 11 pts, 2 reb, 2 ast, 1 stl, 0 blk, 3 to, FG 3-7, 3PT 2-5, FT 3-4 |
| Jazz 119, Spurs 109 | Isaiah Collier | UTAH | deck+kit | bench | 22 min, 11 pts, 3 reb, 5 ast, 5 stl, 0 blk, 3 to, FG 4-7, 3PT 1-2, FT 2-4 |
| Jazz 119, Spurs 109 | Ace Bailey | UTAH | deck+kit | bench | 24 min, 6 pts, 6 reb, 3 ast, 3 stl, 0 blk, 1 to, FG 3-8, 3PT 0-2, FT 0-0 |
| Jazz 119, Spurs 109 | Kyle Filipowski | UTAH | deck+kit | bench | did not play (coach's decision on the box score) |
| Jazz 119, Spurs 109 | Jusuf Nurkic | UTAH | deck+kit | bench | did not play (coach's decision on the box score) |

Injury blocks of the five summaries (pool rows): Trail Blazers 119, London Lions 66 — Robert Williams III (day-to-day, 2026-10-13); Damian Lillard (day-to-day, 2026-10-13); Shaedon Sharpe (out, 2027-03-02); Hawks 113, Thunder 110 — Aaron Wiggins (day-to-day, 2026-10-16); Onyeka Okongwu (day-to-day, 2026-10-16); CJ McCollum (day-to-day, 2026-10-16); Luguentz Dort (day-to-day, 2026-10-16); Chet Holmgren (day-to-day, 2026-10-13); Jaylin Williams (day-to-day, 2026-10-13); Nets 131, Wizards 122 — Khris Middleton (day-to-day, 2026-10-16); Anthony Davis (day-to-day, 2026-10-16); Mikel Brown Jr. (day-to-day, 2026-10-14); Timberwolves 122, Knicks 104 — Karl-Anthony Towns (day-to-day, 2026-10-15); Mikal Bridges (day-to-day, 2026-10-15); Josh Hart (day-to-day, 2026-10-15); OG Anunoby (day-to-day, 2026-10-15); Jalen Brunson (day-to-day, 2026-10-15); Terrence Shannon Jr. (day-to-day, 2026-10-14); Jonathan Kuminga (day-to-day, 2026-10-14); Donte DiVincenzo (out, 2027-04-01); Jazz 119, Spurs 109 — Kyle Filipowski (day-to-day, 2026-10-21); Jusuf Nurkic (out, 2026-11-04); Stephon Castle (day-to-day, 2026-10-14); Devin Vassell (day-to-day, 2026-10-14); De'Aaron Fox (day-to-day, 2026-10-14).

## 3. Flagged-item receipts (F1) — verdicts

| player | query run (2026-10-13) | dated finding | verdict |
|---|---|---|---|
| Brandon Ingram | "Brandon Ingram Clippers Achilles injury update October 13 2026" + the LAC shadow | the 9/28–29 items again (the partial Achilles tear found at the heel surgery; 'won't be ready for the start of the season'; no timetable); ESPN's buzz page 10/12 says the same; Out on ESPN's feed, 2026-11-01 | HELD; no October medical item |
| Kristaps Porzingis | "Kristaps Porzingis Warriors return practice opener October 13 2026" + the GSW shadow | expected at Chase Center today to meet Celebrini and the performance staff per Kerr (ESPN 10/12); no return-to-court timeline (RotoBaller); Kerr unsure for the 10/21 opener, leaning Green at center with Lendeborg (Yahoo, Heavy); 'remains away from the team' per Slater on the feed 10/12, 10/21 estimate | HELD; veto unchanged |
| Kawhi Leonard | "Kawhi Leonard Raptors preseason debut Knicks October 13 2026" + the TOR shadow | cleared to debut tonight 10/13 vs the Knicks per Rajakovic — a full practice Monday, the two absences not injury-related (The Athletic via NBC Sports), a limited role expected (CBS Sports, NBC Sports, TSN, HoopsHype, Sportando, Heavy 10/12) | HELD; the box score is the next pull's |
| Cam Thomas | "Cam Thomas injury status news October 2026"; "\"Cam Thomas\" free agent October 2026" | the Nets' waiver, the February Bucks signing and the March waiver only (Yahoo's 'remains unsigned' about 67 days old); no signing on the ledger (10/9–10/11 blocks) | HELD, unsigned |
| Jaden Ivey | "Jaden Ivey injury update October 2026 preseason"; "\"Jaden Ivey\" Bulls October 2026" | the Bulls' 3/30 waiver (ESPN, Bulls.com, Yahoo); nothing dated in October; no signing on the ledger | HELD, unsigned |
| Jeremy Sochan | "Jeremy Sochan Trail Blazers debut Kings October 13 2026" + the POR shadow | 8 and 8 in 21 minutes vs the Lions (box score; weszło, TVP Sport, Polsat Sport, Eurosport PL); on Portland's roster per ESPN's feed (335/335 verified); one outlet names an Exhibit 9 clause; no waiver on the ledger; at Sacramento tonight | HELD |
| Lonzo Ball | "Lonzo Ball injury status October 2026 preseason"; "\"Lonzo Ball\" Cavaliers preseason October 2026" | 2024–25 items only (the Cavaliers' 2025 preseason; a 2026-27 team option noted by NBA.com in 2025, its exercise unconfirmed); no signing on the ledger | HELD, unsigned |
| Rob Dillingham | "Rob Dillingham Timberwolves preseason October 2026 minutes role"; "\"Dillingham\" Bulls preseason October 2026" | the 9/26–27 Bulls-to-Hornets trade for Hield and the 9/28 release (Yahoo, Fox Sports, Wikipedia); the April wrist ganglion-cyst surgery; no signing on the ledger | HELD, unsigned |
| Bennedict Mathurin | "Bennedict Mathurin Pacers preseason injury October 2026"; "\"Mathurin\" Pacers preseason October 2026 Carlisle" + the NOP shadow | no Pelicans game in the window (Wednesday vs Dallas next); the 2025–26 Pacers items, the February trade to the Clippers, the two-year $16M Pelicans deal, an undated Hoops Wire note on his Pelicans opener (13 in 17 minutes off the bench) | HELD |
| Ryan Rollins | "Ryan Rollins Bucks preseason October 2026 starting role" + the MIL shadow | no Bucks game in the window; CBS's 'bigger role incoming?', Yahoo's panel (Rollins 'for now'), SI's potential starting five (Rollins with Herro), FantasySP 'fully cleared' after the eye laceration; Jenkins has not settled the frontcourt (Ware/Kuzma) | HELD; retiring the flag stays on the sheet |

## 4. The carried items

- **Maxime Raynaud — D-1012-1's default (a) applied (the owner silent since 10/12).** Deck: re-tagged `inj-knee-risk` (availability 0.78; the tag's parenthetical records the ruling and the re-evaluation); kit: GP 72 → 66 in `report/projections-2026-27.csv`. Board effect on both planes: none — his value sits below the pool mean, where the deck's multiplier does not bite (audit 2026-10-09) and the kit never shrinks a negative by absence; deck rank 165 → 165 (adjusted value -2.9703 → -2.9703, availability 1.0 → 0.78), kit rank 162 → 162 (§6). The feed is unchanged since the Kings' 10/11 announcement (Out, 10/25). Re-check at the re-evaluation (about 10/25).
- **Kawhi Leonard** — cleared to debut tonight vs the Knicks (Rajakovic, Monday; CBS Sports, NBC Sports, TSN, HoopsHype, Sportando, Heavy), a limited role expected; Thursday at MSG and Friday at Detroit close the preseason. The next pull reads the box score; the tag stays by the first-season-back convention.
- **Kristaps Porziņģis** — at the facility today to meet the performance staff (Kerr via ESPN 10/12); no timeline; Kerr unsure for the opener and leaning Green at center with Lendeborg (Yahoo, Heavy). Veto unchanged. **Curry** ramps to second-half minutes tonight vs the Lakers; **Horford** not traveling (rest).
- **Tyrese Haliburton** — practiced Monday without restrictions after the ankle tweak (Carlisle to Forbes, on the feed 10/12); tonight at Oklahoma City the next chance — the same game is the last pre-draft look at **Holmgren** and **Hartenstein** (both sat Monday at Atlanta as announced 10/10; D-1008-2 (a) holds). **SGA, J. Williams, Caruso, Wallace, Mitchell, McCain, Jaylin Williams** rested the same game.
- **De'Aaron Fox** — a third straight missed preseason game ('undisclosed' soreness per Orsborn/Express-News on the feed 10/12, 10/14 estimate); Friday vs Sacramento closes the Spurs' preseason. **Wembanyama, Castle, Vassell, Harper, Harris** rested with him (nine Spurs sat per the recaps).
- **The Knicks' starters** — Brunson 20, Anunoby 15 with 3 steals, Towns 11, Bridges 9, Hart 2 in 22 minutes each; all five rest tonight in Toronto (Bondy/NY Post on the feed; 10/15 estimate). **Edwards** 26 and **McDaniels** 22; **LaMelo Ball** 10 and 7 with 5 turnovers; **Kuminga** (general soreness) and **Shannon** sat; **DiVincenzo** Out (Achilles, April).
- **Sabonis** — a full participant Monday after two straight missed games ('a minor issue'), questionable tonight vs Portland (KHTK on the feed); **Cardwell** (calf) did not practice; **Monk** practiced. **Lillard** and **Robert Williams III** rested vs the Lions (maintenance; Sacramento tonight). **Davis** and **Middleton** rested vs Brooklyn (Friday next; Middleton has yet to play). **Trae Young** 11 and 11 assists with 8 turnovers; **Ayton** 4 and 7; **Sarr** 6 and 9 on 3-10.
- **Aday Mara** — a start at center with Holmgren, Hartenstein and Jaylin Williams out: 33 minutes, 17/10/6, 4 blocks (CBS says five), 5 turnovers, 9-12 FT. **Jock Landale** 17/6/5 with 3 steals in 21 minutes with Okongwu resting. **Jalen Wilson** 12 and 8 in 30.
- **Ingram, Thomas, Ivey, Ball, Dillingham, Mathurin, Rollins, Sochan** — §3. **Stewart** (D-1010-2, re-check ~10/22–23), **Coby White, Knueppel, Claxton** (re-evaluations ~10/19–21), **Strus, Lively, Nurkić** (exclusions stand), **Dru Smith** (calf, a couple of weeks from 10/1) — no new item.
- **D-C2** (the post-draft projection review) and **D-SF-1..4** (the governance items) — carried; **D-1011-4** — carried, default (b).

## 5. Window sweep, team shadows, injury sweep

**Team shadows (7):** CHI — nothing dated 10/13; Bleacher Nation (~10/10) says Claxton will effectively miss the entire preseason; the Sun-Times' projected starters (Giddey, Powell, Buzelis, Wilson, Claxton); the White and Collins items returned were 2025–26's; GSW — Porziņģis at the facility Tuesday, Curry ramping up tonight, Horford not traveling, the Kerr starting five (ESPN, Yahoo, Heavy); LAC — Ingram Out (the Achilles), Beal no five-on-five (inflammation managed), Strus' foot, Sanders day-to-day; Wednesday vs Denver next; MIL — nothing dated 10/13; the Sunday loss to Charlotte (Herro 18, Turner 5 blocks), Rollins the most consistent early performer, Ware 18 and 12 vs the Thunder then −22 off the bench, Jenkins' frontcourt unsettled; NOP — Koloko waived 10/9 (Exhibit 9, HoopsHype), Jalon Moore signed 10/10; the summary mis-joined 'Mathurin Koloko' (a garble, logged); POR — a 10/13 preview (Kings 0-3, Blazers 2-0), Sochan's roster case, Lillard's return 'solving the shooting woes' (Fox Sports), Sharpe out six months (Fubo, from the 8/24 announcement); TOR — Kawhi cleared for tonight (Rajakovic), Thursday at MSG, Friday at Detroit, the opener 10/21 vs Chicago. No trade or signing touches a pool row.

**Injury sweep, both directions (mechanical).** ESPN's league injuries feed (137 rows, fetched 10/13 13:58 UTC) against the 51-row tag inventory (17 excluded, 34 risk):

| direction | evidence (the feed diff) |
|---|---|
| pool rows with status Out on the feed | 10: Jimmy Butler III (1/2), Moses Moody (12/1), Max Strus (11/2), Brandon Ingram (11/1), Isaiah Stewart (10/23), Donte DiVincenzo (4/1), Mark Williams (2/3), Shaedon Sharpe (3/2), Maxime Raynaud (10/25), Jusuf Nurkic (11/4) — Raynaud the one untagged Out row at fetch time, tagged today (D-1012-1) |
| tagged rows absent from the feed (candidates for 'cleared') | 28: the 9 `out-*` free agents, retirees and overseas rows and 19 risk rows (Morant, Jackson Jr., Curry, Zion, Kawhi, Edey, Robinson, Sarr, Tatum, Irving, George, Melton, Murphy, Wells, Keegan Murray, Vanderbilt, Hunter, Smart, Simmons), all playing or practicing under their tags; none re-tagged (first-season-back convention) |
| untagged rows on the feed with Out or a return date after 10/21 | 1: Maxime Raynaud (Out, 10/25) → D-1012-1 applied today |
| feed items dated inside the window on pool rows | 34, every one written to the deck: Mikel Brown Jr., Tyrese Haliburton, Kristaps Porzingis, Anfernee Simons, Adem Bona, Dylan Harper, Victor Wembanyama, De'Aaron Fox, Devin Vassell, Stephon Castle, Damian Lillard, Robert Williams III, Al Horford, Dylan Cardwell, Domantas Sabonis, Pelle Larsson, Malik Monk, Allen Graves, Trayce Jackson-Davis, Anthony Davis, Dyson Daniels, Jalen Johnson, Luguentz Dort, CJ McCollum, Aaron Wiggins, Onyeka Okongwu, Jonathan Kuminga, Terrence Shannon Jr., Khris Middleton, Jalen Brunson, Josh Hart, OG Anunoby, Karl-Anthony Towns, Mikal Bridges |

Day-to-day items on the feed for untagged rows (not tier questions today): T.J. McConnell, Ziaire Williams, Collin Sexton, Dalton Knecht, Chet Holmgren, Jaylin Williams, Alex Caruso, Jared McCain, Ajay Mitchell, Isaiah Hartenstein, Cason Wallace, Jalen Williams, Shai Gilgeous-Alexander, Anthony Black, Desmond Bane, Jalen Suggs, Malik Monk, Domantas Sabonis, Dylan Cardwell, Trayce Jackson-Davis, Allen Graves (10/13); Luka Garza, Mikel Brown Jr., Grayson Allen, Zach Collins, Santi Aldama, Cade Cunningham, Jalen Duren, Kobe Sanders, Pelle Larsson, Bam Adebayo, Andrew Wiggins, Klay Thompson, Giannis Antetokounmpo, Davion Mitchell, Kasparas Jakucionis, Brayden Burries, Terrence Shannon Jr., Jonathan Kuminga, Devin Booker, Miles Bridges, Stephon Castle, Devin Vassell, De'Aaron Fox, Dylan Harper, Victor Wembanyama (10/14); Alperen Sengun, Kevin Durant, Karl-Anthony Towns, Mikal Bridges, Josh Hart, OG Anunoby, Jalen Brunson (10/15); Aaron Wiggins, Onyeka Okongwu, CJ McCollum, Luguentz Dort, Jalen Johnson, Dyson Daniels, Al Horford, Dru Smith, Adem Bona, Anfernee Simons, Kentavious Caldwell-Pope, Jaylen Brown, Dominick Barlow, Khris Middleton (10/16); Tobias Harris (10/20); Coby White, Kon Knueppel, Nic Claxton, Kyle Filipowski (10/21).

**Garbles caught (search summaries, logged, not used):** the Blazers recap summary said it found no mention of Sochan while the Polish outlets in his receipt query had his 8 and 8; the Hawks recap's block count conflicts (CBS five, TalkBasket four — the box score's four stands); the Wolves recap's date (10/12 local, 10/13 UTC); the Jazz query surfaced a CBS item from an earlier 128-115 Spurs win; the CHI shadow returned 2025–26 White and Collins items; the LAC shadow mixed dated and undated items; the MIL, TOR and POR shadows returned nothing dated 10/13 itself (their items are 10/12's); the Pelicans summary mis-joined 'Mathurin Koloko'; the first Dillingham query named his old team and returned Minnesota items; the Thomas, Ivey, Ball and Mathurin first queries returned 2025–26 items (the narrowed follow-ups ran); the Sochan query reported 'no Kings game found' — it is tonight; the Porziņģis summary conflates the Tuesday facility visit with practice (no on-court item exists).

## 6. Board effects (computed, never eyeballed)

- **Kit:** `rank_engine.py` re-run after Raynaud's GP 72 → 66, 200 of 313 projected (12 held off: four unsigned, eight at GP ≤ 25); the diff against the morning snapshot (`top200_baseline.md`, taken after the MG merge) is Raynaud's GP cell on his row only — rank 162 before and after; 0 entries, 0 exits, 0 moves.
- **Deck:** the draftable ordering recomputed before and after the edits under the deck's own math (`deck_board_before.json`, `_after.json`): identical, 318 draftable rows of 335; Raynaud rank 165 → 165 with availability 1.0 → 0.78 (adjusted value -2.9703 unchanged — below the pool mean the multiplier has nothing to bite).

## 7. Deck build and publish

- `data/players.csv`: 117 notes appended on 117 rows (the five box scores on 81, the sweep and receipts on 36); one tag change (Maxime Raynaud → `inj-knee-risk`, prepended with D-1012-1's ruling in the parenthetical); no line or team change; the LF endings the morning's MG pass left are preserved (0 CRLF), every other byte untouched; 0 notes violating D-1006-3 among the edits; skipped rows: none.
- `scripts/verify_rosters.py` (no exemption): direct-complete, all 30 rosters, 335/335 matched, 0 mismatches, 0 unmatched; `roster_verification.json` and `rosters_official.json` dated today.
- `hoops.py freshness --stamp` with `--pool-changes` (gate 4): 2026-10-13; notes plus one tag asserted (32 dated queries in the note).
- `JUDGMENT` (already dated 2026-10-13 by the MG pass) carries the ten 10/13 receipts (`judgment_open_items.py` flags the same ten); colophon Data paragraph rewritten for the daily refresh on top of the MG pass (gate 6 accepted it).
- `build_deck.py`, red-first: without a waiver the build refused on gate 7 — `propagation 1: Maxime Raynaud: kit re-derived (GP 72->66) but the deck row is unchanged` (the deck has no games column; its row changed by tag). With the named waiver: planes: 315 shared · kit-only 10 · deck-only 20 · team 0 · exclusion 0 · drift 0 · propagation 0 · waived 1; market: yahoo-2026-10-12.csv — priced 246/335 rows (Yahoo ADP else XRank), 1 days old; deck built: 335 players · pull 2026-10-13 · pool bf0914e594b3 · injection round-trip OK; "safe to publish".
- `check_parity.py`: PARITY: EXACT MATCH. `test_card.py` CARD: all 99 cases passed; `test_draft.py` all 65 cases passed; `test_gates.py` all 54 cases passed. `full_dom_check.mjs` on `draft_state_54.json`: 145 assertions, 0 failed, [] page errors, pass true (`arena/results/full_dom_check_2026-10-13_v62.json`). `repeat_market_check.py`: 25 of 25 mocks replayed, 8 flagged (2 LINE QUESTIONED, 6 SOURCES SPLIT), 4 near misses (`arena/results/repeat_market_check_2026-10-13_v62.json`). `identity_check.py`: POINTS IDENTITY: 0 player(s), 0 line(s) more than 1 from their own shooting (200 deck and 200 kit lines checked). `range_check.py`: RANGE CHECK: 26 player(s) with 28 cell(s) outside every reference (145 of the top 150 checkable).
- Published to the standing URL after a fresh read: Version 63, id 1791903783-cda0, the standing URL (fresh read of Version 62, id 1791870667-7ce2, immediately before); the served file (610350 bytes) carries the built page (609986 bytes, sha256 1ec428cd372a) byte-for-byte inside the service's 364-byte wrapper at offset 349; manifest built 2026-10-13 with the one Raynaud waiver

## 8. Gates (2026-10-13)

| gate | evidence |
|---|---|
| `report/check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07; exit 0 |
| `report/rank_engine.py` | exit 0; 200 of 313 projected (12 held off); board diff = Raynaud's GP cell, rank 162 unchanged |
| `scripts/verify_rosters.py` (deck, no exemption) | direct-complete, all 30 rosters, 335/335, 0 mismatches, 0 unmatched; exit 0 |
| `hoops.py freshness --stamp --pool-changes` (deck) | 2026-10-13, notes plus one tag asserted |
| `scripts/build_deck.py --planes-waive` (deck) | red-first refused on gate 7 (propagation 1: Raynaud); gates 1–7 + F8 pass with the one named waiver (Raynaud, the D-1012-1 twin) in the manifest; round-trip OK; "safe to publish" |
| `scripts/check_parity.py` (deck) | PARITY: EXACT MATCH; exit 0 |
| `scripts/test_card.py` / `test_gates.py` / `test_draft.py` (deck) | CARD: all 99 cases passed / all 54 cases passed / all 65 cases passed; exit 0 each |
| `arena/mocks/full_dom_check.mjs` (deck) | 145 assertions, 0 failed, [] page errors, pass true; exit 0 |
| `scripts/repeat_market_check.py` (deck) | 25 of 25 mocks replayed, 8 flagged (2 LINE QUESTIONED, 6 SOURCES SPLIT), 4 near misses; exit 0 |
| `scripts/identity_check.py` / `range_check.py` (deck) | POINTS IDENTITY: 0 player(s), 0 line(s) more than 1 from their own shooting (200 deck and 200 kit lines checked) / RANGE CHECK: 26 player(s) with 28 cell(s) outside every reference (145 of the top 150 checkable); exit 0 each |
| `report/check_report.py` | REPORT GATE: PASS — after-report-2026-10-13.md (structure, publication rule, pull-log row); exit 0 |
| `report/check_derived.py` | DERIVED: all 23 dated artifacts reproduce byte-for-byte from their pinned inputs; exit 0 |
| `scripts/judgment_open_items.py --check-report` (deck plane) | receipts check PASS — all 10 flagged names carry a receipts row; exit 0 |
| `scripts/repeat_market_check.py --check-report` (deck plane) | REPEAT-NAME CHECK: PASS — 8 flagged name(s), each with a row (25 of 25 mocks replayed); exit 0 |
| artifact publish | Version 63, id 1791903783-cda0, the standing URL (fresh read of Version 62, id 1791870667-7ce2, immediately before); the served file (610350 bytes) carries the built page (609986 bytes, sha256 1ec428cd372a) byte-for-byte inside the service's 364-byte wrapper at offset 349; manifest built 2026-10-13 with the one Raynaud waiver |

## 9. Watchlist / open items

- **Tonight (10/13), the night before the draft:** Kawhi's debut vs the Knicks (the Knicks' starters rest); Pacers at Thunder — Haliburton's next chance and the last pre-draft look at Holmgren and Hartenstein (D-1008-2); Cavaliers at Magic (Suggs, Black); Warriors vs Lakers in Las Vegas (Curry's second-half minutes, Lendeborg; Porziņģis at the facility, not the game); Trail Blazers at Kings (Sabonis questionable, Lillard and Robert Williams back, Sochan, Acuff, Simmons).
- **D-1012-1 (Raynaud)** — applied today; re-check at the Kings' re-evaluation (about 10/25); the owner may still pick (b) exclude or (c) untag.
- **Claxton, Coby White, Knueppel, Harris, Stewart, Raynaud** — the opener in question for all six (re-evaluations about 10/19–10/25).
- **Porziņģis** — the facility visit today; any on-court item is the next pull's; the veto holds.
- **Fox** — three straight misses, 'undisclosed'; Friday vs Sacramento the last preseason chance.
- **D-C2** (the post-draft projection review), **D-SF-1..4**, **D-1011-4** — carried.
- **10/14 morning lock** — the fresh Yahoo ADP paste; the draft is tomorrow.

## Open-item receipts

| player | query run (2026-10-13) | dated finding |
|---|---|---|
| Brandon Ingram | "Brandon Ingram Clippers Achilles injury update October 13 2026"; the LAC shadow | no October medical item; the 9/28–29 announcement items and ESPN's 10/12 buzz line; ESPN's feed 2026-11-01 — HELD |
| Kristaps Porzingis | "Kristaps Porzingis Warriors return practice opener October 13 2026"; the GSW shadow | at the facility today per Kerr (ESPN 10/12); no timeline (RotoBaller); opener uncertain (Yahoo, Heavy); feed 'remains away' 10/12, 10/21 — HELD, veto unchanged |
| Kawhi Leonard | "Kawhi Leonard Raptors preseason debut Knicks October 13 2026"; the TOR shadow | cleared to debut tonight per Rajakovic (CBS Sports, NBC Sports, TSN, HoopsHype 10/12); limited role expected — HELD |
| Cam Thomas | "Cam Thomas injury status news October 2026"; "\"Cam Thomas\" free agent October 2026" | the Nets/Bucks 2025–26 items only; no signing on the ledger (10/9–10/11 blocks) — HELD, unsigned |
| Jaden Ivey | "Jaden Ivey injury update October 2026 preseason"; "\"Jaden Ivey\" Bulls October 2026" | the Bulls' 3/30 waiver items; nothing in October; no signing on the ledger — HELD, unsigned |
| Jeremy Sochan | "Jeremy Sochan Trail Blazers debut Kings October 13 2026"; the POR shadow | 8 and 8 vs the Lions (box score; weszło, TVP Sport, Polsat Sport, Eurosport PL); on Portland's roster per ESPN's feed; no waiver on the ledger — HELD |
| Lonzo Ball | "Lonzo Ball injury status October 2026 preseason"; "\"Lonzo Ball\" Cavaliers preseason October 2026" | 2024–25 items only; no signing on the ledger — HELD, unsigned |
| Rob Dillingham | "Rob Dillingham Timberwolves preseason October 2026 minutes role"; "\"Dillingham\" Bulls preseason October 2026" | the 9/26–28 trade-and-release items (Yahoo, Fox Sports); no signing on the ledger — HELD, unsigned |
| Bennedict Mathurin | "Bennedict Mathurin Pacers preseason injury October 2026"; "\"Mathurin\" Pacers preseason October 2026 Carlisle"; the NOP shadow | no game in the window; the 2025–26 items and the Pelicans signing; an undated opener note — HELD |
| Ryan Rollins | "Ryan Rollins Bucks preseason October 2026 starting role"; the MIL shadow | no game in the window; CBS, Yahoo, SI and FantasySP role items; Jenkins' frontcourt unsettled — HELD |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 1ec428cd372a), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 25 of 25 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-12.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-06.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 5 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 20 of 25 | 38 | 117 | 47 | 60 | 101 | 71 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Kel'el Ware | 19 of 25 | 27 | 77 | 51 | 51 | 63 | 65 | ft_pct .732 vs .714-.723 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 19 of 25 | 62 | 178 | 56 | 118 | 126 | 129 | tpm 2.8 vs 2.2-2.6 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Lauri Markkanen | 16 of 25 | 11 | 37 | 18 | 31 | 41 | 29 | pts 26.4 vs 20.2-23.8; ast 2.1 vs 1.8-1.9; fg_pct .471 vs .452-.463 | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Jrue Holiday | 14 of 25 | 88 | 144 | 161 | 129 | 128 | 145 | pts 16.4 vs 12-12.8; reb 4.6 vs 4-4.2; ast 6.1 vs 4.4-4.6; tpm 2.6 vs 1.9-2; tov 2.8 vs 1.8-2.1; ft_pct .822 vs .855-.867 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Yaxel Lendeborg | 11 of 25 | 70 | 141 | 94 | 121 | 137 | 98 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Ryan Rollins | 9 of 25 | 28 | 74 | 58 | 63 | 78 | 83 | stl 1.7 vs 1.3-1.5 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Kawhi Leonard | 6 of 25 | 6 | 32 | 15 | 16 | 15 | 20 | pts 27.8 vs 23.7-24.3; tpm 2.6 vs 2.2-2.3 | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (21 mocks, value 7, market 18); VJ Edgecombe (12 mocks, value 56, market 75); Tyrese Maxey (7 mocks, value 4, market 9); Derrick White (6 mocks, value 30, market 45).

## Bounds

- Five finals in the window; tonight's five games are the next pull's. No line moved, so the range check and the points identity ran as regression only (both green on the unchanged lines).
- Out of scope by design: the WO-5 method and the MG consensus (D-C2 is after the draft); the Hashtag/Yahoo price files (no new paste today); Kawhi's debut (after the window).
- In scope and single-source: box-score lines not named by an outlet carry the [SINGLE-SOURCE: box score] label in the deck notes; the feed's items (the Thunder and Hawks rest groups, the Kings' practice, the Knicks' rest, Davis, Middleton, Kuminga, Shannon, Filipowski, Brown Jr., Simons, Bona, Larsson, Jackson-Davis, Graves, Haliburton's practice) are labeled [SINGLE-SOURCE: ESPN feed] where no second outlet named them — ATTEMPTED (the recap and shadow queries) and not found, not unverifiable.
- Mara's block count: CBS Sports five, TalkBasket and the box score four; the deck note records the conflict and the box score's figure.
- Mathurin's Pelicans-opener line (13 in 17 minutes) is an undated Hoops Wire note in a search summary — recorded as such, not used for any cell.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-1012-1 | Maxime Raynaud — default (a) applied today (deck `inj-knee-risk` at 0.78, kit GP 66); no rank moves on either plane (deck 165 → 165, kit 162 → 162); re-check at the Kings' re-evaluation (about 10/25) | applied; closed unless the owner picks (b) exclude or (c) untag |
| D-C2, D-SF-1..4, D-1011-4, D-MG-1..3 (decided a/a/a), D-1012-2..4, D-1010-2, D-1011-1..3, D-1010-1, D-RN-6, D75-1..2, D74-1, D73-1 and earlier | carried | carried |

## Provenance

- Inputs: ESPN's scoreboards (10/12, 10/13), the five summaries (401914130, 401898402, 401901824, 401914124, 401898721), the league injuries feed and the 30 roster feeds (10/13 13:58–14:0x UTC, `scratchpad pull1013/dl/`, fetched_at 2026-10-13T13:58:37Z); the Basketball-Reference 2026-27 transactions page fetched directly; 32 dated search queries (`scratchpad pull1013/search_record.txt`; every result pinned in `search_results_1013.txt`, extracted from the session transcript).
- Scripts: `tools/parse_box.py` (the box records), `tools/feed_diff.py` (the two-way injury diff), `tools/deck_edit.py` (117 notes + 1 tag; `deck_edit_record.json`), `tools/deck_board.py` (before/after ordering), `tools/judgment_colophon.py`, `chain.sh` (the deck chain; `chain.log`), `tools/write_report.py` (this file).
- Deck results: `arena/results/full_dom_check_2026-10-13_v62.json`, `repeat_market_check_2026-10-13_v62.json`; `data/roster_verification.json` and `data/freshness.json` dated 2026-10-13; the build manifest carries the Raynaud waiver.
- Did not check: the Spanish-league pursuit of Koloko (Baskonia, per one summary) — not a pool row; Sochan's Exhibit 9 clause beyond the one outlet naming it.

## In plain language

**What happened.** Five games. Edwards and McDaniels combined for 48 at the Garden on 18 Minnesota threes while the Knicks' starters played 22 minutes each and rest tonight. Porter Jr. 22 and Randle 14 and 9 in Washington, where Trae Young had 11 assists and 8 turnovers. Aday Mara started at center for the Thunder with Holmgren and Hartenstein sitting and put up 17, 10 and 6 with four blocks. The Spurs rested nine, including Wembanyama and Fox, who has now missed three straight. Portland beat the London Lions by 53 with Lillard resting; Sochan had 8 and 8.

**What moved.** One thing, by your standing rule: Maxime Raynaud's kneecap ruling from Sunday (D-1012-1) was on your sheet with a default that applies at the next pull if you are silent, and you were, so he now carries the risk tag on the deck and six fewer games on the kit, exactly as Stewart did on 10/11. It changes no rank on either board: he sits at 165 on the deck and 162 on the kit, far below the draftable line, where neither engine moves a player for missing games. Nothing else changed — no line, no team, no other tag.

**Tonight.** The night before your draft: Kawhi's first game as a Raptor (cleared, limited minutes), the Pacers at the Thunder for Haliburton's next look and the only remaining look at Holmgren and Hartenstein, the Warriors and Lakers in Las Vegas (Curry ramping up; Porziņģis is at the facility, not the game, with no timeline), and Portland at Sacramento with Sabonis questionable.

**The deck.** Rebuilt and republished with 117 dated notes and the one tag; the build refused once on purpose (the kit's games column moved and the deck has none) and passed with that one difference named in the manifest; every gate, the full page drive and the repeat-name check passed on the published bytes.
