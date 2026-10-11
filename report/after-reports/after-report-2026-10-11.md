# After-report — 2026-10-11 data pull (early: the seven 10/10 finals) + deck v56

**Owner request (2026-10-11, verbatim):** "Please conduct pull with tonight's slate of games completed. Notes: I'm bullish on Acuff, but especially Lendeborg. I really may target Yaxel if he fits my build. I want to tell you now - not a fan of LaVine. Has let me down before in fantasy and I believe he will regress this season" — WO-3's pull on the completed 10/10 slate, plus three owner notes recorded on the record (§4, the decision sheet).

Pull window: 2026-10-10 → 2026-10-11 (from the 10/10 pull's close, deck v55 published at 15:33 UTC on 10/10, to 05:06 UTC on 10/11: the seven preseason games of 10/10 — Raptors 114, Clippers 106 (Vancouver); Hawks 119, Pacers 117 (Indianapolis); Wizards 114, Pistons 108, OT (Washington); Timberwolves 125, Heat 124 (Miami); Celtics 144, 76ers 106 (Boston); Warriors 111, Kings 106 (San Francisco); Suns 102, Spurs 98 (Phoenix) — all final. Today's four games — the Macao rematch Mavericks–Rockets at 10:00 UTC, Magic at Cavaliers, Bucks at Hornets, Bulls at Nuggets — are the next pull's.)
Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07`, exit 0 (one kit cell changed today — Stewart's GP, §4 — games, not team, so no provenance row moves).

**Method.** The seven box scores read from ESPN's own feed (scoreboard and summary endpoints) before any search — starters, minutes, lines, DNP reasons and each summary's injury block — cross-referenced to both planes by script under `python3 -I` on the downloaded JSON (`scratchpad pull1011/boxscores.txt`, `box.json`, 248 player records). ESPN's league-wide injuries feed (131 rows, fetched 10/11 05:07 UTC) diffed against the deck's 50-row tag inventory in both directions by script (`injuries.txt`). The Basketball-Reference 2026-27 transactions page read directly (newest block still 10/8), NBA.com's news index read directly (the 10/11 Starting 5 not yet published at fetch time; the article pages themselves egress-blocked), ESPN's roster API for all 30 teams (the verifier, 335/335), ESPN's scoreboards 10/10–10/12 and the Thunder's schedule endpoint. Then one sweep of 32 dated queries (22 standard, 10 extended): one recap query per game (a second for the Suns–Spurs and Hawks–Pacers games and for Sarr's return, when the first returned previews only), a dedicated query for each of the ten flagged receipts, the ledger query, the league injury report, and the day's follow-ups (Haliburton's MRI, Brown's absence, Sabonis, Buzelis, the Pelicans, the Blazers, the Bucks, Podziemski's extension). Egress-blocked as on every pull: Yahoo, SI, CBS, RotoWire, NBA.com's article pages and the other sports domains (their items rest on dated search summaries, labeled where they stand alone).

## 1. Roster changes

None. The ledger's newest block is 10/8; the transactions query found nothing dated 10/10 (its newest items: the Raptors' 10/5 waiver of Andre Jackson Jr. and Jamal Shead's 10/1 extension; an undated Nets waiver of Malachi Smith, who played 13 minutes for Toronto in the Vancouver box score, so the item is stale). One contract item: NBA.com's news index headlines "Warriors sign Brandin Podziemski to 5-year rookie scale contract extension" (the article page is egress-blocked; the search returned only the 9/18 extension-talks items with an Oct. 19 deadline — SF Standard, NBC Sports Bay Area) [SINGLE-SOURCE: NBA.com index headline] — a contract, not a placement, so no pool row changes. No pool row changed team, entered or left; `report/roster-provenance.csv` is byte-identical to yesterday's.

## 2. The box scores (ESPN's feed; the line is the evidence where no outlet named the row)

Seven finals. Rows a dated outlet named (the recap queries): Scottie Barnes 12/10/3 (CBS Sports, NBC Sports, Raptors Republic), RJ Barrett 20 and Immanuel Quickley 18 on five threes (Raptors Republic — Kawhi sat, Yahoo), Jalen Johnson 20 and 7 with Luguentz Dort's Hawks debut (CBS Sports, SportsEthos; Pascal Siakam 13 in 22 workload-limited minutes — RotoWire, SI Pacers), Will Riley and Tre Johnson 15 each and AJ Dybantsa 14 and 7 in the overtime win (Bullets Forever), Payton Pritchard 25 and Jayson Tatum 23 in 27 minutes with Paul George's and Mitchell Robinson's Celtics debuts and a 144-point preseason team record (NBC Sports Boston, Boston Globe, CelticsBlog), VJ Edgecombe 19 for Philadelphia (Newsweek), Yaxel Lendeborg 23/10/6 on 10-14 — the game's only double-double — and Darius Acuff Jr. 25 and 8 in 27 minutes with Ben Simmons' Kings debut (Yahoo/NBC Sports Bay Area, Yahoo, SI Kings; Precious Achiuwa started at C). The Suns–Spurs game drew previews only (Arizona Sports' recap surfaced as a link without text), so every Phoenix and San Antonio line below rests on the box score alone, Stephon Castle's 21 minutes included. Alex Sarr's first game of the preseason (20 minutes, a start) likewise: no outlet in two queries named the return. Every other line rests on the box score and is labeled so in the deck notes.

| game | player | team | plane | role | line (evidence: ESPN's box score) |
|---|---|---|---|---|---|
| Raptors 114, Clippers 106 | Derrick Jones Jr. | LAC | deck+kit | starter | 17 min, 5 pts, 2 reb, 0 ast, 0 stl, 0 blk, 0 to, FG 2-3, 3PT 1-1, FT 0-2 |
| Raptors 114, Clippers 106 | Rui Hachimura | LAC | deck+kit | starter | 19 min, 14 pts, 3 reb, 1 ast, 1 stl, 0 blk, 3 to, FG 3-8, 3PT 1-3, FT 7-7 |
| Raptors 114, Clippers 106 | Brook Lopez | LAC | deck+kit | starter | 15 min, 6 pts, 7 reb, 1 ast, 0 stl, 1 blk, 0 to, FG 3-6, 3PT 0-1, FT 0-0 |
| Raptors 114, Clippers 106 | Darius Garland | LAC | deck+kit | starter | 19 min, 11 pts, 0 reb, 4 ast, 0 stl, 0 blk, 1 to, FG 4-11, 3PT 1-4, FT 2-2 |
| Raptors 114, Clippers 106 | Isaiah Jackson | LAC | deck+kit | bench | 15 min, 8 pts, 4 reb, 0 ast, 0 stl, 0 blk, 5 to, FG 2-4, 3PT 0-0, FT 4-4 |
| Raptors 114, Clippers 106 | Kris Dunn | LAC | deck+kit | bench | 15 min, 1 pts, 1 reb, 6 ast, 2 stl, 1 blk, 1 to, FG 0-1, 3PT 0-1, FT 1-2 |
| Raptors 114, Clippers 106 | Gradey Dick | LAC | deck+kit | bench | 13 min, 4 pts, 1 reb, 0 ast, 0 stl, 0 blk, 0 to, FG 1-3, 3PT 0-1, FT 2-2 |
| Raptors 114, Clippers 106 | Keaton Wagler | LAC | deck+kit | bench | 23 min, 9 pts, 1 reb, 2 ast, 0 stl, 0 blk, 1 to, FG 3-9, 3PT 2-6, FT 1-2 |
| Raptors 114, Clippers 106 | RJ Barrett | TOR | deck+kit | starter | 23 min, 20 pts, 5 reb, 5 ast, 1 stl, 0 blk, 1 to, FG 7-11, 3PT 3-5, FT 3-5 |
| Raptors 114, Clippers 106 | Scottie Barnes | TOR | deck+kit | starter | 22 min, 12 pts, 10 reb, 3 ast, 0 stl, 0 blk, 2 to, FG 4-10, 3PT 1-3, FT 3-4 |
| Raptors 114, Clippers 106 | Jakob Poeltl | TOR | deck+kit | starter | 22 min, 9 pts, 4 reb, 1 ast, 2 stl, 0 blk, 1 to, FG 3-4, 3PT 0-0, FT 3-6 |
| Raptors 114, Clippers 106 | Immanuel Quickley | TOR | deck+kit | starter | 19 min, 18 pts, 4 reb, 4 ast, 1 stl, 0 blk, 0 to, FG 6-8, 3PT 5-6, FT 1-2 |
| Raptors 114, Clippers 106 | Ja'Kobe Walter | TOR | deck+kit | starter | 19 min, 3 pts, 0 reb, 1 ast, 1 stl, 0 blk, 1 to, FG 1-4, 3PT 1-4, FT 0-0 |
| Raptors 114, Clippers 106 | Collin Murray-Boyles | TOR | deck+kit | bench | 22 min, 13 pts, 9 reb, 3 ast, 0 stl, 2 blk, 4 to, FG 4-9, 3PT 0-1, FT 5-7 |
| Raptors 114, Clippers 106 | Jamal Shead | TOR | deck+kit | bench | 19 min, 13 pts, 1 reb, 2 ast, 2 stl, 0 blk, 4 to, FG 5-9, 3PT 0-3, FT 3-3 |
| Hawks 119, Pacers 117 | Onyeka Okongwu | ATL | deck+kit | starter | 23 min, 18 pts, 3 reb, 3 ast, 0 stl, 0 blk, 1 to, FG 5-10, 3PT 2-7, FT 6-6 |
| Hawks 119, Pacers 117 | Jalen Johnson | ATL | deck+kit | starter | 25 min, 20 pts, 7 reb, 3 ast, 0 stl, 0 blk, 3 to, FG 8-12, 3PT 2-2, FT 2-3 |
| Hawks 119, Pacers 117 | CJ McCollum | ATL | deck+kit | starter | 19 min, 12 pts, 5 reb, 0 ast, 0 stl, 0 blk, 2 to, FG 2-4, 3PT 1-2, FT 7-7 |
| Hawks 119, Pacers 117 | Luguentz Dort | ATL | deck+kit | starter | 24 min, 7 pts, 6 reb, 2 ast, 0 stl, 0 blk, 0 to, FG 2-7, 3PT 1-4, FT 2-2 |
| Hawks 119, Pacers 117 | Dyson Daniels | ATL | deck+kit | starter | 24 min, 7 pts, 4 reb, 4 ast, 2 stl, 0 blk, 3 to, FG 3-8, 3PT 1-4, FT 0-0 |
| Hawks 119, Pacers 117 | Corey Kispert | ATL | deck | bench | 18 min, 5 pts, 3 reb, 3 ast, 0 stl, 0 blk, 0 to, FG 2-6, 3PT 1-4, FT 0-0 |
| Hawks 119, Pacers 117 | Jalen Wilson | ATL | deck+kit | bench | 9 min, 8 pts, 3 reb, 0 ast, 0 stl, 0 blk, 0 to, FG 2-3, 3PT 2-3, FT 2-2 |
| Hawks 119, Pacers 117 | Zuby Ejiofor | ATL | kit | bench | 12 min, 4 pts, 4 reb, 0 ast, 2 stl, 1 blk, 1 to, FG 1-4, 3PT 0-2, FT 2-2 |
| Hawks 119, Pacers 117 | Jock Landale | ATL | deck+kit | bench | 9 min, 2 pts, 3 reb, 1 ast, 1 stl, 0 blk, 1 to, FG 0-3, 3PT 0-1, FT 2-2 |
| Hawks 119, Pacers 117 | Aaron Wiggins | ATL | deck+kit | bench | 20 min, 13 pts, 2 reb, 1 ast, 2 stl, 0 blk, 0 to, FG 4-9, 3PT 3-6, FT 2-2 |
| Hawks 119, Pacers 117 | Kingston Flemings | ATL | deck+kit | bench | 18 min, 8 pts, 1 reb, 1 ast, 1 stl, 0 blk, 1 to, FG 4-7, 3PT 0-2, FT 0-0 |
| Hawks 119, Pacers 117 | Pascal Siakam | IND | deck+kit | starter | 22 min, 13 pts, 2 reb, 4 ast, 0 stl, 2 blk, 0 to, FG 3-7, 3PT 1-3, FT 6-6 |
| Hawks 119, Pacers 117 | Ivica Zubac | IND | deck+kit | starter | 21 min, 11 pts, 5 reb, 2 ast, 1 stl, 1 blk, 1 to, FG 4-6, 3PT 0-0, FT 3-6 |
| Hawks 119, Pacers 117 | Kelly Oubre Jr. | IND | deck+kit | starter | 20 min, 13 pts, 1 reb, 0 ast, 0 stl, 0 blk, 2 to, FG 5-8, 3PT 3-5, FT 0-0 |
| Hawks 119, Pacers 117 | Andrew Nembhard | IND | deck+kit | starter | 22 min, 10 pts, 1 reb, 3 ast, 0 stl, 0 blk, 2 to, FG 3-5, 3PT 2-3, FT 2-2 |
| Hawks 119, Pacers 117 | Aaron Nesmith | IND | deck+kit | starter | 20 min, 7 pts, 1 reb, 5 ast, 1 stl, 0 blk, 1 to, FG 2-6, 3PT 1-4, FT 2-2 |
| Hawks 119, Pacers 117 | Obi Toppin | IND | deck+kit | bench | 15 min, 11 pts, 3 reb, 1 ast, 1 stl, 0 blk, 2 to, FG 5-8, 3PT 1-2, FT 0-0 |
| Hawks 119, Pacers 117 | Jarace Walker | IND | deck+kit | bench | 20 min, 10 pts, 7 reb, 3 ast, 0 stl, 0 blk, 2 to, FG 3-7, 3PT 2-5, FT 2-2 |
| Hawks 119, Pacers 117 | Jay Huff | IND | deck+kit | bench | 10 min, 5 pts, 0 reb, 1 ast, 0 stl, 0 blk, 0 to, FG 2-6, 3PT 1-4, FT 0-0 |
| Hawks 119, Pacers 117 | Ben Sheppard | IND | deck+kit | bench | 16 min, 2 pts, 1 reb, 1 ast, 1 stl, 0 blk, 2 to, FG 1-3, 3PT 0-1, FT 0-0 |
| Wizards 114, Pistons 108, OT | Duncan Robinson | DET | deck+kit | starter | 19 min, 12 pts, 2 reb, 4 ast, 0 stl, 0 blk, 1 to, FG 4-9, 3PT 2-6, FT 2-3 |
| Wizards 114, Pistons 108, OT | John Collins | DET | deck+kit | starter | 17 min, 2 pts, 2 reb, 0 ast, 0 stl, 0 blk, 2 to, FG 1-5, 3PT 0-3, FT 0-0 |
| Wizards 114, Pistons 108, OT | Paul Reed | DET | deck+kit | starter | 21 min, 11 pts, 9 reb, 3 ast, 2 stl, 0 blk, 2 to, FG 4-8, 3PT 0-0, FT 3-4 |
| Wizards 114, Pistons 108, OT | Ausar Thompson | DET | deck+kit | starter | 15 min, 2 pts, 1 reb, 2 ast, 3 stl, 1 blk, 1 to, FG 1-7, 3PT 0-1, FT 0-0 |
| Wizards 114, Pistons 108, OT | Daniss Jenkins | DET | deck+kit | starter | 18 min, 12 pts, 0 reb, 4 ast, 0 stl, 0 blk, 1 to, FG 4-6, 3PT 3-5, FT 1-2 |
| Wizards 114, Pistons 108, OT | Javonte Green | DET | deck+kit | bench | 14 min, 7 pts, 6 reb, 1 ast, 2 stl, 0 blk, 0 to, FG 2-4, 3PT 1-3, FT 2-2 |
| Wizards 114, Pistons 108, OT | Kevin Huerter | DET | deck+kit | bench | 18 min, 11 pts, 2 reb, 3 ast, 1 stl, 0 blk, 0 to, FG 3-7, 3PT 3-6, FT 2-2 |
| Wizards 114, Pistons 108, OT | Isaiah Joe | DET | deck+kit | bench | 17 min, 5 pts, 2 reb, 1 ast, 0 stl, 1 blk, 3 to, FG 2-11, 3PT 0-7, FT 1-1 |
| Wizards 114, Pistons 108, OT | Ebuka Okorie | DET | kit | bench | 27 min, 14 pts, 1 reb, 6 ast, 1 stl, 0 blk, 3 to, FG 6-15, 3PT 0-4, FT 2-2 |
| Wizards 114, Pistons 108, OT | Jalen Duren | DET | deck+kit | bench | did not play (coach's decision on the box score) |
| Wizards 114, Pistons 108, OT | Cade Cunningham | DET | deck+kit | bench | did not play (coach's decision on the box score) |
| Wizards 114, Pistons 108, OT | Anthony Davis | WSH | deck+kit | starter | 22 min, 10 pts, 11 reb, 4 ast, 1 stl, 2 blk, 5 to, FG 3-8, 3PT 0-1, FT 4-6 |
| Wizards 114, Pistons 108, OT | AJ Dybantsa | WSH | deck+kit | starter | 23 min, 14 pts, 7 reb, 2 ast, 1 stl, 0 blk, 0 to, FG 4-10, 3PT 0-2, FT 6-10 |
| Wizards 114, Pistons 108, OT | Kyshawn George | WSH | deck+kit | starter | 23 min, 14 pts, 3 reb, 0 ast, 1 stl, 3 blk, 3 to, FG 3-4, 3PT 0-1, FT 8-8 |
| Wizards 114, Pistons 108, OT | Alex Sarr | WSH | deck+kit | starter | 20 min, 8 pts, 1 reb, 0 ast, 0 stl, 1 blk, 2 to, FG 3-5, 3PT 1-3, FT 1-2 |
| Wizards 114, Pistons 108, OT | Trae Young | WSH | deck+kit | starter | 23 min, 2 pts, 2 reb, 8 ast, 0 stl, 0 blk, 5 to, FG 1-4, 3PT 0-2, FT 0-0 |
| Wizards 114, Pistons 108, OT | Justin Champagnie | WSH | deck+kit | bench | 17 min, 12 pts, 3 reb, 1 ast, 3 stl, 0 blk, 3 to, FG 4-8, 3PT 2-6, FT 2-4 |
| Wizards 114, Pistons 108, OT | Deandre Ayton | WSH | deck+kit | bench | 15 min, 4 pts, 6 reb, 1 ast, 0 stl, 0 blk, 2 to, FG 0-1, 3PT 0-0, FT 4-6 |
| Wizards 114, Pistons 108, OT | Bub Carrington | WSH | deck+kit | bench | 18 min, 5 pts, 0 reb, 1 ast, 0 stl, 1 blk, 2 to, FG 2-8, 3PT 1-6, FT 0-0 |
| Wizards 114, Pistons 108, OT | Bilal Coulibaly | WSH | deck+kit | bench | 20 min, 3 pts, 4 reb, 1 ast, 1 stl, 0 blk, 2 to, FG 0-0, 3PT 0-0, FT 3-4 |
| Wizards 114, Pistons 108, OT | Will Riley | WSH | deck+kit | bench | 24 min, 15 pts, 4 reb, 3 ast, 1 stl, 1 blk, 1 to, FG 3-7, 3PT 1-3, FT 8-8 |
| Wizards 114, Pistons 108, OT | Tre Johnson | WSH | deck+kit | bench | 19 min, 15 pts, 2 reb, 1 ast, 0 stl, 0 blk, 0 to, FG 5-9, 3PT 4-6, FT 1-1 |
| Wizards 114, Pistons 108, OT | Khris Middleton | WSH | deck+kit | bench | did not play (coach's decision on the box score) |
| Wizards 114, Pistons 108, OT | Tre Mann | WSH | deck | bench | did not play (coach's decision on the box score) |
| Timberwolves 125, Heat 124 | Joan Beringer | MIN | deck+kit | starter | 24 min, 10 pts, 7 reb, 1 ast, 1 stl, 4 blk, 1 to, FG 5-6, 3PT 0-0, FT 0-0 |
| Timberwolves 125, Heat 124 | Terrence Shannon Jr. | MIN | deck+kit | starter | 22 min, 19 pts, 6 reb, 4 ast, 0 stl, 0 blk, 1 to, FG 8-16, 3PT 3-6, FT 0-0 |
| Timberwolves 125, Heat 124 | Bones Hyland | MIN | deck+kit | starter | 21 min, 23 pts, 4 reb, 4 ast, 3 stl, 0 blk, 0 to, FG 6-9, 3PT 5-6, FT 6-6 |
| Timberwolves 125, Heat 124 | Jonathan Kuminga | MIN | deck+kit | bench | did not play (coach's decision on the box score) |
| Timberwolves 125, Heat 124 | Donte DiVincenzo | MIN | deck+kit | bench | did not play (coach's decision on the box score) |
| Timberwolves 125, Heat 124 | Simone Fontecchio | MIA | deck+kit | starter | 24 min, 14 pts, 1 reb, 0 ast, 0 stl, 0 blk, 0 to, FG 4-12, 3PT 4-7, FT 2-2 |
| Timberwolves 125, Heat 124 | Nikola Jovic | MIA | deck+kit | starter | 25 min, 16 pts, 6 reb, 3 ast, 3 stl, 0 blk, 3 to, FG 7-11, 3PT 2-2, FT 0-1 |
| Timberwolves 125, Heat 124 | Pelle Larsson | MIA | deck+kit | starter | 25 min, 14 pts, 3 reb, 5 ast, 0 stl, 0 blk, 4 to, FG 4-15, 3PT 0-2, FT 6-7 |
| Timberwolves 125, Heat 124 | Bobby Portis | MIA | deck+kit | bench | did not play (coach's decision on the box score) |
| Timberwolves 125, Heat 124 | Bam Adebayo | MIA | deck+kit | bench | did not play (coach's decision on the box score) |
| Timberwolves 125, Heat 124 | Dru Smith | MIA | deck+kit | bench | did not play (coach's decision on the box score) |
| Celtics 144, 76ers 106 | Dean Wade | PHI | deck+kit | starter | 20 min, 5 pts, 3 reb, 1 ast, 0 stl, 0 blk, 1 to, FG 2-4, 3PT 1-3, FT 0-0 |
| Celtics 144, 76ers 106 | Tyrese Maxey | PHI | deck+kit | starter | 18 min, 8 pts, 3 reb, 4 ast, 1 stl, 1 blk, 2 to, FG 2-10, 3PT 1-6, FT 3-3 |
| Celtics 144, 76ers 106 | VJ Edgecombe | PHI | deck+kit | starter | 26 min, 19 pts, 3 reb, 4 ast, 4 stl, 0 blk, 3 to, FG 6-11, 3PT 2-5, FT 5-6 |
| Celtics 144, 76ers 106 | Labaron Philon Jr. | PHI | kit | bench | 25 min, 14 pts, 2 reb, 7 ast, 1 stl, 0 blk, 2 to, FG 5-13, 3PT 4-8, FT 0-0 |
| Celtics 144, 76ers 106 | LeBron James | PHI | deck+kit | bench | did not play (did not dress on the box score) |
| Celtics 144, 76ers 106 | Dominick Barlow | PHI | deck+kit | bench | did not play (did not dress on the box score) |
| Celtics 144, 76ers 106 | Joel Embiid | PHI | deck+kit | bench | did not play (did not dress on the box score) |
| Celtics 144, 76ers 106 | Adem Bona | PHI | deck+kit | bench | did not play (did not dress on the box score) |
| Celtics 144, 76ers 106 | Kentavious Caldwell-Pope | PHI | deck+kit | bench | did not play (did not dress on the box score) |
| Celtics 144, 76ers 106 | Jaylen Brown | PHI | deck+kit | bench | did not play (did not dress on the box score) |
| Celtics 144, 76ers 106 | Anfernee Simons | PHI | deck+kit | bench | did not play (did not dress on the box score) |
| Celtics 144, 76ers 106 | Paul George | BOS | deck+kit | starter | 25 min, 13 pts, 5 reb, 4 ast, 5 stl, 0 blk, 3 to, FG 3-10, 3PT 2-7, FT 5-6 |
| Celtics 144, 76ers 106 | Jayson Tatum | BOS | deck+kit | starter | 27 min, 23 pts, 5 reb, 4 ast, 1 stl, 0 blk, 1 to, FG 9-19, 3PT 4-10, FT 1-1 |
| Celtics 144, 76ers 106 | Mitchell Robinson | BOS | deck+kit | starter | 14 min, 6 pts, 5 reb, 1 ast, 0 stl, 0 blk, 0 to, FG 3-5, 3PT 0-0, FT 0-3 |
| Celtics 144, 76ers 106 | Derrick White | BOS | deck+kit | starter | 26 min, 15 pts, 4 reb, 2 ast, 1 stl, 0 blk, 2 to, FG 5-11, 3PT 1-5, FT 4-4 |
| Celtics 144, 76ers 106 | Jordan Walsh | BOS | deck+kit | starter | 11 min, 6 pts, 5 reb, 0 ast, 1 stl, 1 blk, 0 to, FG 2-3, 3PT 2-3, FT 0-0 |
| Celtics 144, 76ers 106 | Sam Hauser | BOS | deck+kit | bench | 21 min, 11 pts, 1 reb, 2 ast, 1 stl, 0 blk, 0 to, FG 4-6, 3PT 3-5, FT 0-0 |
| Celtics 144, 76ers 106 | Luka Garza | BOS | deck+kit | bench | 11 min, 8 pts, 7 reb, 0 ast, 1 stl, 1 blk, 1 to, FG 4-8, 3PT 0-0, FT 0-0 |
| Celtics 144, 76ers 106 | Neemias Queta | BOS | deck+kit | bench | 19 min, 6 pts, 10 reb, 1 ast, 0 stl, 0 blk, 1 to, FG 2-5, 3PT 0-1, FT 2-4 |
| Celtics 144, 76ers 106 | Payton Pritchard | BOS | deck+kit | bench | 24 min, 25 pts, 4 reb, 7 ast, 0 stl, 0 blk, 4 to, FG 7-12, 3PT 5-8, FT 6-6 |
| Celtics 144, 76ers 106 | Baylor Scheierman | BOS | deck+kit | bench | 19 min, 3 pts, 3 reb, 8 ast, 5 stl, 0 blk, 3 to, FG 1-3, 3PT 1-3, FT 0-0 |
| Celtics 144, 76ers 106 | Mike Conley | BOS | deck+kit | bench | did not play (coach's decision on the box score) |
| Warriors 111, Kings 106 | Precious Achiuwa | SAC | deck+kit | starter | 27 min, 8 pts, 8 reb, 1 ast, 0 stl, 0 blk, 1 to, FG 3-8, 3PT 0-2, FT 2-2 |
| Warriors 111, Kings 106 | Keegan Murray | SAC | deck+kit | starter | 8 min, 5 pts, 0 reb, 0 ast, 0 stl, 0 blk, 0 to, FG 2-3, 3PT 0-1, FT 1-2 |
| Warriors 111, Kings 106 | Zach LaVine | SAC | deck+kit | starter | 23 min, 11 pts, 1 reb, 2 ast, 3 stl, 0 blk, 0 to, FG 5-13, 3PT 1-4, FT 0-0 |
| Warriors 111, Kings 106 | Ben Simmons | SAC | deck+kit | starter | 9 min, 7 pts, 0 reb, 1 ast, 0 stl, 0 blk, 2 to, FG 2-4, 3PT 0-0, FT 3-4 |
| Warriors 111, Kings 106 | Darius Acuff Jr. | SAC | deck+kit | starter | 27 min, 25 pts, 4 reb, 8 ast, 0 stl, 0 blk, 4 to, FG 8-15, 3PT 4-6, FT 5-5 |
| Warriors 111, Kings 106 | De'Andre Hunter | SAC | deck+kit | bench | 19 min, 4 pts, 3 reb, 1 ast, 0 stl, 0 blk, 2 to, FG 2-8, 3PT 0-3, FT 0-0 |
| Warriors 111, Kings 106 | Maxime Raynaud | SAC | deck+kit | bench | 9 min, 10 pts, 5 reb, 1 ast, 0 stl, 1 blk, 0 to, FG 3-3, 3PT 1-1, FT 3-4 |
| Warriors 111, Kings 106 | Nique Clifford | SAC | deck+kit | bench | 23 min, 3 pts, 1 reb, 3 ast, 2 stl, 0 blk, 4 to, FG 1-10, 3PT 0-3, FT 1-2 |
| Warriors 111, Kings 106 | Draymond Green | GS | deck+kit | starter | 23 min, 3 pts, 7 reb, 5 ast, 1 stl, 0 blk, 1 to, FG 1-1, 3PT 0-0, FT 1-3 |
| Warriors 111, Kings 106 | Gui Santos | GS | deck+kit | starter | 24 min, 15 pts, 6 reb, 1 ast, 0 stl, 0 blk, 5 to, FG 6-9, 3PT 0-2, FT 3-4 |
| Warriors 111, Kings 106 | Yaxel Lendeborg | GS | deck+kit | starter | 24 min, 23 pts, 10 reb, 6 ast, 2 stl, 1 blk, 2 to, FG 10-14, 3PT 1-3, FT 2-2 |
| Warriors 111, Kings 106 | Stephen Curry | GS | deck+kit | starter | 14 min, 8 pts, 0 reb, 2 ast, 0 stl, 0 blk, 1 to, FG 3-6, 3PT 2-4, FT 0-0 |
| Warriors 111, Kings 106 | Brandin Podziemski | GS | deck+kit | starter | 26 min, 14 pts, 7 reb, 4 ast, 1 stl, 0 blk, 1 to, FG 4-9, 3PT 3-7, FT 3-4 |
| Warriors 111, Kings 106 | Al Horford | GS | deck+kit | bench | 21 min, 4 pts, 5 reb, 3 ast, 0 stl, 1 blk, 2 to, FG 1-9, 3PT 0-4, FT 2-2 |
| Warriors 111, Kings 106 | Gary Payton II | GS | deck+kit | bench | 19 min, 0 pts, 2 reb, 0 ast, 1 stl, 0 blk, 0 to, FG 0-1, 3PT 0-1, FT 0-0 |
| Warriors 111, Kings 106 | De'Anthony Melton | GS | deck+kit | bench | 18 min, 0 pts, 2 reb, 1 ast, 1 stl, 3 blk, 1 to, FG 0-6, 3PT 0-1, FT 0-0 |
| Warriors 111, Kings 106 | Brandon Williams | GS | deck+kit | bench | 17 min, 19 pts, 0 reb, 1 ast, 1 stl, 0 blk, 5 to, FG 7-8, 3PT 2-2, FT 3-4 |
| Warriors 111, Kings 106 | Will Richard | GS | deck+kit | bench | 14 min, 7 pts, 3 reb, 1 ast, 2 stl, 0 blk, 0 to, FG 1-5, 3PT 1-4, FT 4-4 |
| Suns 102, Spurs 98 | Julian Champagnie | SA | deck+kit | starter | 25 min, 10 pts, 1 reb, 2 ast, 0 stl, 0 blk, 0 to, FG 2-7, 3PT 2-6, FT 4-4 |
| Suns 102, Spurs 98 | Victor Wembanyama | SA | deck+kit | starter | 22 min, 13 pts, 7 reb, 6 ast, 1 stl, 2 blk, 2 to, FG 6-14, 3PT 0-5, FT 1-2 |
| Suns 102, Spurs 98 | Devin Vassell | SA | deck+kit | starter | 23 min, 6 pts, 2 reb, 1 ast, 0 stl, 0 blk, 2 to, FG 2-9, 3PT 1-4, FT 1-1 |
| Suns 102, Spurs 98 | Stephon Castle | SA | deck+kit | starter | 21 min, 13 pts, 7 reb, 5 ast, 1 stl, 0 blk, 2 to, FG 5-10, 3PT 1-3, FT 2-2 |
| Suns 102, Spurs 98 | Dylan Harper | SA | deck+kit | starter | 24 min, 15 pts, 3 reb, 4 ast, 1 stl, 1 blk, 1 to, FG 6-9, 3PT 1-1, FT 2-2 |
| Suns 102, Spurs 98 | Harrison Barnes | SA | deck+kit | bench | 17 min, 6 pts, 0 reb, 0 ast, 1 stl, 0 blk, 1 to, FG 2-5, 3PT 2-5, FT 0-0 |
| Suns 102, Spurs 98 | Keldon Johnson | SA | deck+kit | bench | 16 min, 6 pts, 3 reb, 1 ast, 0 stl, 0 blk, 1 to, FG 3-4, 3PT 0-0, FT 0-0 |
| Suns 102, Spurs 98 | Luke Kornet | SA | deck+kit | bench | 17 min, 4 pts, 10 reb, 2 ast, 0 stl, 2 blk, 1 to, FG 2-7, 3PT 0-0, FT 0-0 |
| Suns 102, Spurs 98 | Dillon Brooks | PHX | deck+kit | starter | 24 min, 15 pts, 2 reb, 2 ast, 1 stl, 0 blk, 2 to, FG 4-11, 3PT 1-4, FT 6-7 |
| Suns 102, Spurs 98 | Ryan Dunn | PHX | deck+kit | starter | 19 min, 6 pts, 4 reb, 1 ast, 1 stl, 1 blk, 1 to, FG 2-5, 3PT 0-1, FT 2-2 |
| Suns 102, Spurs 98 | Khaman Maluach | PHX | deck+kit | starter | 23 min, 10 pts, 15 reb, 3 ast, 1 stl, 1 blk, 2 to, FG 4-9, 3PT 1-2, FT 1-1 |
| Suns 102, Spurs 98 | Luke Kennard | PHX | deck+kit | starter | 25 min, 20 pts, 5 reb, 4 ast, 0 stl, 0 blk, 1 to, FG 8-15, 3PT 4-10, FT 0-0 |
| Suns 102, Spurs 98 | Jalen Green | PHX | deck+kit | starter | 29 min, 18 pts, 3 reb, 5 ast, 1 stl, 0 blk, 3 to, FG 7-12, 3PT 3-5, FT 1-2 |
| Suns 102, Spurs 98 | Oso Ighodaro | PHX | deck+kit | bench | 21 min, 8 pts, 5 reb, 5 ast, 2 stl, 2 blk, 0 to, FG 4-7, 3PT 0-0, FT 0-0 |
| Suns 102, Spurs 98 | Jordan Goodwin | PHX | deck+kit | bench | 17 min, 8 pts, 2 reb, 0 ast, 0 stl, 1 blk, 0 to, FG 3-7, 3PT 2-5, FT 0-0 |
| Suns 102, Spurs 98 | Collin Gillespie | PHX | deck+kit | bench | 20 min, 2 pts, 2 reb, 0 ast, 3 stl, 0 blk, 2 to, FG 1-5, 3PT 0-4, FT 0-0 |

Injury blocks of the seven summaries (pool rows): Raptors — Jackson-Davis (dental, 10/13), Graves (groin, 10/13); Clippers — Sanders (hip, 10/14), Beal (knee inflammation, 10/14), Strus (Out, 11/2), Ingram (Out, 11/1); Pacers — McConnell (undisclosed, 10/13), Haliburton (right ankle, 10/13); Hawks — Finney-Smith and Alexander-Walker (rest, 10/12), Gueye (foot, 10/21); Wizards — Middleton and Mann (rest, 10/12); Pistons — Cunningham and Duren (rest, 10/14); Heat — Larsson (illness), Adebayo, Wiggins, Thompson (rest, 10/14); Timberwolves — McDaniels, Kuminga, Dosunmu, Gobert, Edwards (rest, 10/12); Celtics — Garza (nose, 10/14); 76ers — James, Caldwell-Pope, Brown, Embiid (rest), Barlow (back), all 10/16; Warriors — Porziņģis (undisclosed, 10/21), Butler (Out, 1/2/27), Moody (Out, 12/1); Kings — Raynaud (knee), Cardwell, Monk (rest), Sabonis (undisclosed), all 10/13; Suns — Booker (rest), Bridges (ankle), both 10/14, Mark Williams (Out, 2/3/27); Spurs — Fox (soreness, 10/12), Harris (calf, 10/20).

## 3. Flagged-item receipts (F1) — verdicts

| player | query run (2026-10-11) | dated finding | verdict |
|---|---|---|---|
| Brandon Ingram | "Brandon Ingram Clippers update October 10 2026" | the late-September media-day items only (no timetable; re-evaluated when the season begins, per Redden); Out on ESPN's feed with the 2026-11-01 estimate, on the Vancouver summary's injury block | HELD; no October item |
| Kristaps Porzingis | "Kristaps Porzingis Warriors update October 10 2026 Kings game" | not on the 10/10 box score vs Sacramento; the summary's injury block carries him day-to-day, undisclosed, 10/21 estimate (Slater's 10/6 entry); the search returned older games and an undated AP 'out indefinitely' item | HELD; veto unchanged |
| Kawhi Leonard | "Kawhi Leonard Raptors debut Knicks October 13 2026" + the Vancouver recap query | sat the 10/10 Vancouver game, his second straight, not injury related (ESPN feed 10/13 estimate; Yahoo, Raptors Republic); the Knicks games Tuesday 10/13 and Thursday 10/15 per TSN's 10/6 note, 'a chance he gets into game action the following week' (Lewenberg) | HELD; re-check after 10/13 |
| Cam Thomas | "Cam Thomas unsigned October 10 2026" | Roundtable's 9/28 'free agency limbo' piece the newest; the ledger's newest block (10/8) carries no signing | HELD, unsigned |
| Jaden Ivey | "Jaden Ivey free agent workout October 2026" | the March waiver items only; no signing on the ledger | HELD, unsigned |
| Jeremy Sochan | "Jeremy Sochan Trail Blazers roster October 10 2026" + "Portland Trail Blazers news October 10 2026 roster cuts Sochan Potter" | on Portland's roster per ESPN's roster feed (335 of 335 verified today); no waiver on the ledger; the signing and camp-battle items only (Roundtable 9/28, SI Blazers); London Lions 10/12 | HELD |
| Lonzo Ball | "Lonzo Ball unsigned October 10 2026" | nothing past February; no signing on the ledger | HELD, unsigned |
| Rob Dillingham | "Rob Dillingham free agent October 10 2026" | the 9/29 waiver items; no signing on the ledger | HELD, unsigned |
| Bennedict Mathurin | "Bennedict Mathurin Pelicans October 10 2026" + "New Orleans Pelicans news October 10 2026 Mathurin Murray practice" | no dated item; the Pelicans did not play in the window (Wednesday vs Dallas next); the August signing items and the summer lineup projections (FanSided: starting SG; one outlet: sixth man) | HELD; WO-5 decides today |
| Ryan Rollins | "Ryan Rollins Bucks October 10 2026 Hornets preseason" + "Milwaukee Bucks Hornets preseason October 11 2026 Rollins Turner injury report" | nothing dated (2023–25 previews and game logs); the Bucks play today at Charlotte — the next pull's box score | HELD; WO-5 decides |

## 4. The carried items and the owner's notes

- **Isaiah Stewart — D-1010-2's default applied (the owner silent).** Deck: re-tagged `inj-ankle-risk` (availability 0.78; the tag's parenthetical records the ruling and the re-evaluation); kit: GP 70 → 64 in `report/projections-2026-27.csv`. Board effect on both planes: none — his value sits below the pool mean, where the deck's multiplier does not bite (audit 2026-10-09) and the kit never shrinks a negative by absence; deck rank 180 → 180, kit rank 162 → 162 (§6). The build's plane check (gate 7) read the kit's GP change as a re-derivation with no deck line change and refused; the twin was waived by name as on 10/9 for Nurkić — `--planes-waive "Isaiah Stewart: the D-1010-2 twin — the kit's GP 70→64 propagates to the deck as the inj-ankle-risk tag, not a stat-line change"`, recorded in the page manifest. Feed unchanged: Out, left ankle, 10/23. Re-check at the Grizzlies' re-evaluation (about 10/22–10/23).
- **The owner's three notes (10/11)** — recorded in three places each: the deck pool note (the player's row), a JUDGMENT note card (adj 0, the owner's words verbatim), and the decision sheet. **Lendeborg** (deck rank 82, value −0.77 on the committed 12.9/7.5/2.7 line; 23/10/6 on 10-14 last night, three starts in three games played): "bullish… I really may target Yaxel if he fits my build" — no adjustment today; the line is on today's WO-5 pass (D-1007-1), and a preference enters the board only through the judgment layer by the owner's call (D-1011-2). **Acuff Jr.** (deck rank 176, below the draftable 156, Yahoo-priced; 25 and 8 assists in 27 minutes last night, three starts at PG): "bullish" — same handling, D-1006-1 (a) already put the line on today's pass. **LaVine** (deck rank 56, value +0.15; kit GP 64 on 20.5/4.0/3.5 at 47.0%; 11 points on 5-13 with 3 steals last night): "not a fan… has let me down before in fantasy and I believe he will regress this season" — **D-1011-1** on the sheet: (a) a judgment adjustment of −0.10 carrying the owner's rationale, (b) the `doNotDraft` veto (the Porziņģis shape), (c) no change; default (a) at the next pull if silent. The note card is on the page today so the room's read and the owner's read sit side by side on his card row.
- **Tyrese Haliburton** — sat the Hawks game with a 'mild tweak of the right ankle' from the 10/7 game, the MRI 'positive' per Carlisle (Yahoo 10/10; ESPN feed 10/13 estimate, Forbes' East). Tag `inj-achilles-risk` stays by the first-season-back convention; the 10/21 opener vs New Orleans the target.
- **Holmgren and Hartenstein** — both ruled out of Monday's 10/12 game at Atlanta (quadriceps; ankle — Almanza, USA Today via ESPN's feed), with SGA, Jalen Williams, Caruso, Wallace, Mitchell, McCain resting and Jaylin Williams (heel) out. The Thunder's remaining preseason per ESPN's schedule endpoint: 10/13 vs Indiana (00:00 UTC 10/14), 10/15 at Houston — so the pre-draft look at both is 10/13 at the earliest, the night before the draft. D-1008-2 (a) holds.
- **De'Aaron Fox** — out again (undisclosed soreness per Guzman, SI, via the feed), two of two preseason games missed; 10/12 at Utah the next chance (10/12 estimate). **Stephon Castle** — 21 minutes, 13/7/5 on 5-10 (18 then 21 in the two games: the D-CAST-2a re-check reads a normal starter's preseason load; no recap named him). **Dylan Harper** 15 in 24 minutes; **Wembanyama** 13/7/6 with 2 blocks on 6-14, 0-5 from three.
- **Ben Simmons** — the Kings debut, started: 7 points in 9 minutes on 2-4 (Yahoo, SI Kings; RotoWire via the search). **Sabonis, Monk, Cardwell** out on the Kings' availability report (Sacramento Bee via the feed); Achiuwa started at C. **Keegan Murray** 8 minutes, his first of the preseason. **Maxime Raynaud** left in the second quarter with a right knee injury after 10 points in 9 minutes (Spears via the feed; 10/13 estimate).
- **Alex Sarr** — his first game of the preseason: a start, 20 minutes, 8 points on 3-5 with a block (box score only; two queries found no outlet naming the return). Tag kept by convention. **Cade Cunningham** rested (feed) and **Jalen Duren** sat a second straight game (reconditioning — Robbins via the feed; shootaround per Bullets Forever); both 10/14 estimates. **Anthony Davis** 10/11/4 with 2 blocks and 5 turnovers in 22 minutes; **Trae Young** 2 points, 8 assists, 5 turnovers.
- **Celtics–76ers** — Jaylen Brown, LeBron and Embiid rested (Tony Jones via the feed; NBC Sports Philadelphia, Boston Globe); Caldwell-Pope rest, Simons (right hamstring), Barlow (back), Bona (left foot) did not dress; all 10/16 estimates. **Luka Garza** left late with a nose injury after 8 and 7 in 11 minutes (CLNS via the feed, 10/14). **Paul George** 13/5/4 with 5 steals in 25 minutes in his debut; **Mitchell Robinson** 6 and 5 in 14 as the starting C; **Pritchard** 25 on five threes; **Tatum** 23 in 27.
- **Wolves–Heat** — both teams rested their regulars: Edwards, Gobert, McDaniels, Ball, Dosunmu, Kuminga (feed); Giannis, Adebayo, Wiggins, Thompson, Davion Mitchell (Nehm via the feed; Hot Hot Hoops). **Joan Beringer** 10/7 with 4 blocks on 5-6; **Bones Hyland** 23 on 5-6 from three; **Terrence Shannon Jr.** 19; **Pelle Larsson** 14 and 5 assists on 4-15, then out with an illness (feed, 10/14). **DiVincenzo** DNP; exclusion stands.
- **Hawks–Pacers** — Dort's Hawks debut (24 minutes, 7 points); **Dyson Daniels** 7/4/4 with 2 steals and 3 turnovers; **Okongwu** 18; **Zubac** 11 and 5 in 21 minutes; **Nembhard** 10; **Toppin** 11; Finney-Smith and Alexander-Walker rested; McConnell did not play (undisclosed, 10/13).
- **Raptors–Clippers** — Kawhi sat (§3); **Garland** 11 and 4 assists in 19 minutes; **Hachimura** 14 in 19; **Isaiah Jackson** 5 turnovers in 15 minutes; **Kris Dunn** 6 assists; **Jakob Poeltl** 9 and 4; **Collin Murray-Boyles** 13 and 9 with 2 blocks and 4 turnovers.
- **Kessler** (practiced Saturday without live work per Redick; 10/13 estimate, Tuesday vs Golden State the next game), **Sexton** (lower leg, day-to-day — Buha via the feed), **Suggs** (increased activity Saturday, 'looked more like himself' — Sweeney via the feed; today at Cleveland the next chance), **Filipowski** (progressing, no return date — Hardy via the feed), **Booker** (rest) and **Bridges** (right ankle) — the feed's new entries, all noted.
- **Kawhi, Porziņģis, Ingram, Mathurin, Rollins, Sochan, the four unsigned guards** — §3. **Durant** sits today's Macao rematch by plan (carried from 10/10); **Buzelis, Tre Jones, Jalen Smith, Collins** — today at Denver; **Harden, Suggs, Black** — today at Cleveland; **Rollins** — today at Charlotte; **Irving, P.J. Washington, Aldama, Lively** — today in Macao: all the next pull's.
- **Strus, Lively, Nurkić** — exclusions stand (Strus and Lively on the feed as Out; Nurkić Out, 11/4).

## 5. Window sweep, team shadows, injury sweep

**Team shadows (7):** CHI — no item in the window (Denver tonight); GSW — Lendeborg's third start, Simmons' debut on the other bench, Porziņģis not on the box score, the Podziemski extension headline (§1); LAC — Vancouver played without Kawhi on the other side, Beal's knee unchanged (10/14), Ingram and Strus Out on the summary's block; MIL — Charlotte today, no dated item; NOP — no game, no item (Wednesday vs Dallas next); POR — London Lions 10/12, no cut news dated; TOR — the Vancouver win, Kawhi's Knicks-week chance. No trade or signing touches a pool row.

**Injury sweep, both directions (mechanical).** ESPN's league injuries feed (131 rows, fetched 10/11 05:07 UTC) against the 50-row tag inventory as it stood before today's edit (17 excluded, 33 risk; 34 risk after Stewart's tag):

| direction | evidence (the feed diff) |
|---|---|
| pool rows with status Out on the feed | 9: Isaiah Stewart (UNTAGGED), Brandon Ingram (risk), Max Strus (excluded), Jusuf Nurkic (excluded), Moses Moody (excluded), Jimmy Butler III (excluded), Mark Williams (excluded), Shaedon Sharpe (excluded), Donte DiVincenzo (excluded) — Stewart, the one untagged Out row yesterday, carries the D-1010-2 tag today |
| tagged rows absent from the feed (candidates for 'cleared') | 32: the 9 `out-*` free agents and retirees and 23 risk rows (Davis, Lillard, Morant, Edey, Zion, Tatum, George, Robinson, Irving, VanVleet, Curry and the rest), all playing or practicing under their tags; none re-tagged (first-season-back convention) |
| untagged rows on the feed with Out or a return date after 10/21 | 1 before today's edit (Isaiah Stewart, Out, 10/23), 0 after |

Day-to-day items on the feed for untagged rows (not tier questions today): Brandon Miller, Matas Buzelis, Tre Jones, Jalen Smith, Zach Collins, James Harden, P.J. Washington, Santi Aldama, Jalen Suggs, Anthony Black (10/11); Dorian Finney-Smith, Nickeil Alexander-Walker, Mikel Brown Jr., Day'Ron Sharpe, Michael Porter Jr., Jaden McDaniels, Jonathan Kuminga, Ayo Dosunmu, Rudy Gobert, Anthony Edwards, LaMelo Ball, Tony Bradley, Ochai Agbaji, De'Aaron Fox, Lauri Markkanen, Khris Middleton, Tre Mann (10/12); T.J. McConnell, Ziaire Williams, Collin Sexton, Dalton Knecht, Chet Holmgren, Jaylin Williams, Alex Caruso, Jared McCain, Ajay Mitchell, Isaiah Hartenstein, Cason Wallace, Jalen Williams, Shai Gilgeous-Alexander, Maxime Raynaud, Dylan Cardwell, Domantas Sabonis, Malik Monk, Trayce Jackson-Davis, Allen Graves (10/13); Luka Garza, Cade Cunningham, Jalen Duren, Kobe Sanders, Pelle Larsson, Bam Adebayo, Andrew Wiggins, Klay Thompson, Giannis Antetokounmpo, Davion Mitchell, Devin Booker, Miles Bridges (10/14); Kevin Durant (10/15); Dru Smith, Kentavious Caldwell-Pope, Jaylen Brown, Dominick Barlow, Anfernee Simons, Adem Bona (10/16); Tobias Harris (10/20); Coby White, Kon Knueppel, Nic Claxton, Kyle Filipowski (10/21).

**Garbles caught (search summaries, logged, not used):** the Vancouver query's ESPN recap was an older Clippers–Raptors game with Harden; the Celtics query's NBC Sports item had Brown and Tatum 'out Sunday vs the Magic'; the Suns–Spurs queries returned a 2025 ESPN recap (gameId 401705361, Wembanyama's blood clot, Paul, Durant) and 2023 items; the Pistons query's ESPN recap was an earlier 129-125 game; the Pacers query returned a February 2022 SI item (Young 34 and 11) and a 2024 Hawks note; the transactions query's RealGM tracker stopped in July; the Porziņģis query returned the April 10 Kings–Warriors game; the Kawhi query offered his 2018 Raptors debut; the Haliburton MRI query returned the June 2025 Finals items only; the Sabonis query returned 2024–25 injuries; the Buzelis query returned ESPN's June injury page and April items; the Bucks queries returned 2023–25 previews and 2025-26 game logs; the Sarr queries returned his 2024 and 2025 preseason debuts; the Ivey query returned the March waiver and 2022–25 items. One search caveat that is not a garble: the Brown query called a Brown-to-Philadelphia trade 'unconfirmed' — the deck has carried him at PHI since the summer intake and last night's box score lists him on Philadelphia's bench.

## 6. Board effects (computed, never eyeballed)

- **Kit:** `rank_engine.py` re-run, 200 of 313 projected (12 held off: four unsigned, eight at GP ≤ 25); the diff against the morning snapshot is the generation-date line and Stewart's GP cell (70 → 64 at #162, rank unchanged) — 0 entries, 0 exits, 0 moves.
- **Deck:** the draftable ordering recomputed before and after the edits (`scratchpad pull1011/deck_board_before.json`, `_after.json`): 318 live rows, 0 entries, 0 exits, 0 moves; Stewart 180 → 180 (below the zero of the pool, the 0.78 multiplier leaves his adjusted value where it was).

## 7. Deck build and publish

- `data/players.csv`: 165 notes appended on 165 rows (the seven box scores on 123, the sweep on 42); one tag change (Isaiah Stewart → `inj-ankle-risk`, prepended with D-1010-2's ruling in the parenthetical); no line or team change; CRLF preserved, every other byte untouched; 0 notes violating D-1006-3 among the edits (Dylan Cardwell's pre-existing note still ends in `]`, untouched, the known trap; skipped rows: none).
- `scripts/verify_rosters.py` (no exemption): direct-complete, all 30 rosters, 335/335 matched, 0 mismatches, 0 unmatched; `roster_verification.json` and `rosters_official.json` dated today.
- `hoops.py freshness --stamp` with `--pool-changes` (gate 4): 2026-10-11; one tag + notes asserted (32 dated queries in the note).
- `JUDGMENT` re-dated 2026-10-11 with the ten receipts (`judgment_open_items.py` flags the same ten — the three new owner-note cards carry no lexicon marker, so they are notes, not open items); colophon Data paragraph rewritten for 10/11 (gate 6 accepted it).
- `build_deck.py --planes-waive "Isaiah Stewart: …"`: planes 315 shared · team 0 · exclusion 0 · drift 0 · propagation 0 · waived 1 (the first unwaived attempt was refused on the Stewart propagation, as designed); 170 line differences by design; market `yahoo-2026-10-09.csv`, 246/335 priced, 2 days old; built 335 players, pull 2026-10-11, pool 3294e3cb7512, injection round-trip OK, "safe to publish".
- `check_parity.py`: PARITY: EXACT MATCH. `test_card.py` CARD: all 99 cases passed; `test_draft.py` all 65 cases passed; `test_gates.py` all 54 cases passed. `full_dom_check.mjs` on `draft_state_54.json`: 143 assertions, 0 failed, [] page errors, pass true (`arena/results/full_dom_check_2026-10-11_v56.json`). `repeat_market_check.py`: 23 of 23 mocks replayed, 14 flagged (4 LINE QUESTIONED, 10 SOURCES SPLIT), 5 near misses (`arena/results/repeat_market_check_2026-10-11.json`).
- Published to the standing URL after a fresh read: Version 56, id 1791698352-d333, the standing URL; the served file carries the built page byte-for-byte inside the service's 364-byte wrapper; manifest built 2026-10-11

## 8. Gates (2026-10-11)

| gate | evidence |
|---|---|
| `report/check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07; exit 0 |
| `report/rank_engine.py` | exit 0; 200 of 313 projected (12 held off); board diff = the date line + Stewart's GP cell, 0 moves |
| `scripts/verify_rosters.py` (deck, no exemption) | direct-complete, all 30 rosters, 335/335, 0 mismatches, 0 unmatched; exit 0 |
| `hoops.py freshness --stamp --pool-changes` (deck) | 2026-10-11, one tag + notes asserted |
| `scripts/build_deck.py --planes-waive` (deck) | gates 1–7 + F8 pass, one named waiver (Stewart, the D-1010-2 twin) in the manifest; round-trip OK; "safe to publish" |
| `scripts/check_parity.py` (deck) | PARITY: EXACT MATCH; exit 0 |
| `scripts/test_card.py` / `test_gates.py` / `test_draft.py` (deck) | CARD: all 99 cases passed / all 54 cases passed / all 65 cases passed; exit 0 each |
| `arena/mocks/full_dom_check.mjs` (deck) | 143 assertions, 0 failed, [] page errors, pass true; exit 0 |
| `scripts/repeat_market_check.py` (deck) | 23 of 23 mocks replayed, 14 flagged (4 LINE QUESTIONED, 10 SOURCES SPLIT), 5 near misses; exit 0 |
| `report/check_report.py` | REPORT GATE: PASS — after-report-2026-10-11.md (structure, publication rule, pull-log row); exit 0 |
| `report/check_derived.py` | DERIVED: all 21 dated artifacts reproduce byte-for-byte from their pinned inputs; exit 0 |
| `scripts/judgment_open_items.py --check-report` (deck plane) | receipts check PASS — all 10 flagged names carry a receipts row in after-report-2026-10-11.md; exit 0 |
| `scripts/repeat_market_check.py --check-report` (deck plane) | REPEAT-NAME CHECK: PASS — after-report-2026-10-11.md: 14 flagged name(s), each with a row (23 of 23 mocks replayed); exit 0 |
| artifact publish | Version 56, id 1791698352-d333, the standing URL; the served file carries the built page byte-for-byte inside the service's 364-byte wrapper; manifest built 2026-10-11 |

## 9. Watchlist / open items

- **Today (Sunday 10/11): the WO-5 projection pass** per the work order — Acuff Jr. (D-1006-1), Lendeborg (D-1007-1), Mathurin, Rollins, Daniels' steals, Flagg, the LINE QUESTIONED names (PJ Washington, Gafford, Vassell, Herbert Jones), Castle/Barrett's second step; `range_check.py` and `identity_check.py` when lines move. The owner's Lendeborg and Acuff notes are on the record for it (the preference stays in the judgment layer, D-1011-2).
- **D-1011-1 (LaVine)** — the owner's call; default (a) at the next pull.
- **Today's games** (the next pull): Mavericks–Rockets in Macao 10:00 UTC (Irving's first game, P.J. Washington, Aldama, Lively out, Durant resting by plan); Magic at Cavaliers 22:30 (Harden, Suggs, Black); Bucks at Hornets 23:00 (Rollins, Miller); Bulls at Nuggets 01:00 (Buzelis, Tre Jones, Jalen Smith, Collins).
- **10/12:** London Lions at Portland (Sochan); Thunder at Hawks without Holmgren and Hartenstein; Nets at Wizards; Timberwolves at Knicks; Spurs at Jazz (Fox's next chance; Markkanen).
- **10/13 (the night before the draft):** Kawhi's first chance vs the Knicks; Thunder vs Pacers — the only pre-draft look at Holmgren and Hartenstein (D-1008-2); Haliburton's and Raynaud's estimates land.
- **Claxton, Coby White, Knueppel, Harris, Stewart** — the opener in question for all five (re-evaluations about 10/19–10/23).
- **10/14 morning lock** — the fresh Yahoo ADP paste, the bigger-picture assessment on 10/13.

## Open-item receipts

| player | query run (2026-10-11) | dated finding |
|---|---|---|
| Brandon Ingram | "Brandon Ingram Clippers update October 10 2026" | no October item; the 9/28 media-day items (no timetable, re-evaluated when the season begins); ESPN's feed 2026-11-01 — HELD |
| Kristaps Porzingis | "Kristaps Porzingis Warriors update October 10 2026 Kings game" | not on the 10/10 box score; day-to-day on the summary's block (10/21, Slater's 10/6 entry); AP 'out indefinitely' undated — HELD, veto unchanged |
| Kawhi Leonard | "Kawhi Leonard Raptors debut Knicks October 13 2026"; the Vancouver recap query | sat Vancouver 10/10, not injury related, 10/13 estimate (ESPN feed; Yahoo, Raptors Republic); Knicks games 10/13 and 10/15 (TSN) — HELD |
| Cam Thomas | "Cam Thomas unsigned October 10 2026" | Roundtable 9/28 'limbo' the newest; no signing on the ledger (newest block 10/8) — HELD, unsigned |
| Jaden Ivey | "Jaden Ivey free agent workout October 2026" | the March waiver items only; no signing on the ledger — HELD, unsigned |
| Jeremy Sochan | "Jeremy Sochan Trail Blazers roster October 10 2026"; the POR team query | on Portland's roster per ESPN's roster feed; no waiver on the ledger; London Lions 10/12 — HELD |
| Lonzo Ball | "Lonzo Ball unsigned October 10 2026" | nothing past February; no signing on the ledger — HELD, unsigned |
| Rob Dillingham | "Rob Dillingham free agent October 10 2026" | the 9/29 waiver items only; no signing on the ledger — HELD, unsigned |
| Bennedict Mathurin | "Bennedict Mathurin Pelicans October 10 2026"; the NOP team query | no game in the window, no dated item; the August signing and summer lineup items — HELD, WO-5 today |
| Ryan Rollins | "Ryan Rollins Bucks October 10 2026 Hornets preseason"; the MIL team query | nothing dated; Charlotte today — HELD, WO-5 |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 7aa1253bfb59), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 23 of 23 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-09.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-06.csv`, `hashtag-2026-10-09.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 5 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| PJ Washington | 19 of 23 | 87 | 151 | 178 | 144 | 141 | 121 | ast 2.4 vs 1.9-2; tov 1.5 vs 1.7-1.8; fg_pct .470 vs .448-.451; ft_pct .750 vs .698-.703 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Payton Pritchard | 18 of 23 | 37 | 83 | 33 | 90 | 92 | 72 | stl 1 vs 0.7-0.8; tpm 3.8 vs 3-3.2; tov 2 vs 1.3-1.3; ft_pct .850 vs .873-.875 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 17 of 23 | 28 | 65 | 60 | 56 | 43 | 44 | pts 18.5 vs 16.4-17; ast 2.3 vs 2.1-2.1; ft_pct .805 vs .813-.819 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Sandro Mamukelashvili | 17 of 23 | 81 | 169 | 138 | 105 | 153 | 120 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Daniel Gafford | 11 of 23 | 90 | 181 | 188 | 180 | 161 | 155 | pts 10.5 vs 9.1-9.8; reb 7.5 vs 5.8-6.5; ast 1.5 vs 1.1-1.2; blk 1.7 vs 1.2-1.4; fg_pct .700 vs .648-.689; ft_pct .700 vs .671-.687 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Jalen Suggs | 11 of 23 | 59 | 105 | 89 | 54 | 84 | 99 | pts 17 vs 14.1-15.1; ast 4 vs 4.8-5 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 10 of 23 | 82 | 144 | 94 | 121 | 137 | 98 | reb 7.5 vs 5.5-6.9; tpm 0.9 vs 1.2-1.3; fg_pct .520 vs .447-.498; ft_pct .740 vs .765-.828 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Isaiah Hartenstein | 7 of 23 | 75 | 104 | 141 | 92 | 100 | 102 | pts 11.5 vs 9.1-10.5; reb 11 vs 9.2-10.3; fg_pct .585 vs .597-.611; ft_pct .680 vs .642-.656 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Zach LaVine | 7 of 23 | 56 | 100 | 162 | 68 | 77 | 118 | pts 22.5 vs 17-21.1; reb 4.5 vs 3.1-3.6; ast 4 vs 2.8-3.4; tov 2.6 vs 2-2.4 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 5 of 23 | 89 | 142 | 122 | 131 | 125 | 123 | pts 16.8 vs 13.4-15.1; tov 1.5 vs 1-1.2; fg_pct .465 vs .432-.443 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Dyson Daniels | 5 of 23 | 11 | 62 | 20 | 64 | 56 | 53 | pts 14.5 vs 11.3-11.8; stl 3 vs 2-2.4; tpm 1.1 vs 0.5-0.6; fg_pct .495 vs .501-.513 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Herbert Jones | 5 of 23 | 74 | 182 | 147 | 169 | 134 | >250 | — | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Josh Hart | 5 of 23 | 67 | 96 | 68 | 84 | 91 | 94 | pts 13.5 vs 11.9-12.2; tpm 1 vs 1.2-1.5; fg_pct .520 vs .498-.503; ft_pct .780 vs .751-.759 | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Saddiq Bey | 5 of 23 | 95 | 176 | 109 | 132 | 169 | 143 | blk 0.4 vs 0.1-0.1; tpm 2.4 vs 1.8-2; tov 1.5 vs 0.8-0.9 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Karl-Anthony Towns (18 mocks, value 6, market 15); Jalen Williams (15 mocks, value 16, market 39); Derrick White (12 mocks, value 24, market 44); Jalen Johnson (6 mocks, value 13, market 11); Mikal Bridges (6 mocks, value 61, market 82).

## Bounds

- Seven finals in the window; today's four games are the next pull's. No stat line moved, so the range check and the points identity were not run (DATA-PULL §2); the WO-5 pass that follows today runs both if it moves a line.
- The Suns–Spurs game and Sarr's return rest on the box score alone (two queries each returned previews or older seasons); the Wolves' rest list rests on the feed plus one recap sentence; every such note carries its [SINGLE-SOURCE] label.
- The Podziemski extension is a headline on NBA.com's index with the article egress-blocked and no second outlet yet — labeled, and not a pool-row fact.
- The owner-note cards carry adj 0: they change no value anywhere; the owner's preferences move the board only through D-1011-1/D-1011-2 by the owner's call or the stated default.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-1011-1 | Zach LaVine (SAC, deck rank 56, value +0.15; kit 20.5/4.0/3.5 at 47.0% on 64 GP): the owner's 10/11 note — "not a fan of LaVine. Has let me down before in fantasy and I believe he will regress this season." Options: (a) a judgment adjustment of −0.10 on his card carrying this rationale (the Maxey/Edgecombe size) — **corrected the same day (after-report-2026-10-11-decisions.md): since the 2026-08-04 blend50 ship a judgment adjustment labels the card row and moves no rank, so (a) is a visible flag, not a demotion**; (b) the `doNotDraft` veto (the Porziņģis shape — he leaves YOUR candidate pool only); (c) no change, the note card alone. | (a), applied at the next pull if silent — a stated belief about regression is what the judgment layer prices; a veto is the owner's to say in so many words |
| D-1011-2 | Yaxel Lendeborg (GSW, deck rank 82) and Darius Acuff Jr. (SAC, deck rank 176): the owner's 10/11 note — "bullish on Acuff, but especially Lendeborg. I really may target Yaxel if he fits my build." Options: (a) no adjustment — today's WO-5 pass re-derives both lines from the evidence (D-1007-1, D-1006-1) and the card follows the line; (b) a +0.10 judgment adjustment on each carrying the note; (c) Lendeborg only. | (a) — the owner's words are a preference and a line question, and the line question is already on today's pass; a judgment plus is the owner's to add after the WO-5 numbers land |
| D-1010-2 | Isaiah Stewart — default (a) applied today (deck `inj-ankle-risk`, kit GP 64); re-check at the Grizzlies' re-evaluation (about 10/22–10/23) | applied; closed unless the owner picks (b) or (c) |
| D-1010-1, D-RN-6, D73-1, D72-1, D71-1, D70-1, D69-1, D68-1..3, D61-4, D-RN-1..5, D67-1..6, D66-1, D-V4-1, D-CAST-1..4, D62-1..3, D-1008-1..3, D-1009-1..13 and earlier | carried | carried |

## Provenance

- Inputs: ESPN's scoreboards (10/10, 10/11, 10/12), the seven summaries (401898396, 401898397, 401898398, 401898399, 401898720, 401902645, 401906510), the league injuries feed, the 30 roster feeds and the Thunder schedule endpoint (10/11 05:06–05:17 UTC, `scratchpad pull1011/dl/`); the Basketball-Reference 2026-27 transactions page and NBA.com's news index, fetched directly; 32 dated search queries (`scratchpad pull1011/search_record.txt`; results in `search_results.txt`).
- Scripts: `box_json.py`/`box.py` (the box records), `injdiff.py` (the two-way injury diff), `deck_edit.py` (165 notes + the Stewart tag; `deck_edit_record.json`), `judgment_colophon.py` (ten receipts, three owner-note cards, the colophon), `deck_board.py` (before/after ordering), `chain.sh` (the deck chain; `chain.log`), `write_report.py` (this file).
- Deck results: `arena/results/full_dom_check_2026-10-11_v56.json`, `repeat_market_check_2026-10-11.json`; `data/roster_verification.json` and `data/freshness.json` dated 2026-10-11; the page manifest carries the Stewart waiver.
- Not verified: the Suns–Spurs and Sarr items beyond the box score (two queries each); the Podziemski extension beyond NBA.com's index headline; the 10/11 Starting 5 (not yet published at fetch time).

## In plain language

**What happened.** All seven Saturday games are in. The two names you flagged both had the night of the preseason: Lendeborg went 23 points, 10 rebounds and 6 assists on 10-of-14 in his third start, and Acuff put up 25 and 8 assists in 27 minutes on the other bench. Ben Simmons made his Kings debut (7 points in 9 minutes). Paul George and Mitchell Robinson debuted for Boston in a 144-point rout; Jaylen Brown, LeBron and Embiid all sat. Haliburton sat with a mild ankle tweak and a clean MRI. The Thunder have already ruled Holmgren and Hartenstein out of Monday, so the only look at them before your draft is Tuesday night.

**Your notes.** All three are on the record: the player rows, a note card on each man's card line with your words, and the decision sheet. Nothing moved on the board because of them — that is yours to decide. For LaVine the sheet offers a modest negative judgment adjustment (the default if you say nothing by the next pull), a veto, or nothing. For Lendeborg and Acuff the lines themselves get re-derived in today's projection pass, and a positive adjustment is there if you want it after the numbers land.

**What moved.** One thing, by yesterday's default: Isaiah Stewart now carries the ankle-risk tag on the deck and 64 games on the kit. It changed no rank on either board.

**The deck.** Rebuilt and republished as v56 with 165 dated notes; every gate and the full page drive passed; the repeat-name check re-ran on the new page.

**Today.** The Macao rematch (Irving's first game) is already under way; the Magic, Bucks and Bulls play tonight. Then the Sunday projection pass.
