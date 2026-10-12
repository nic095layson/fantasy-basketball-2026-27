# After-report — 2026-10-12 data pull + deck v58

**Owner request (2026-10-12, verbatim):** "Good morning Claude, please run daily refresh pull" — WO-3's daily pull.

Pull window: 2026-10-11 → 2026-10-12 (from the decisions build's close, deck v57 published at 07:50 UTC on 10/11, to 14:42 UTC on 10/12: the four preseason games of 10/11 — Mavericks 132, Rockets 115 (Macao); Cavaliers 119, Magic 105 (Cleveland); Hornets 105, Bucks 90 (Charlotte); Nuggets 133, Bulls 128 (Denver) — all final. Today's five games — London Lions at Trail Blazers, Thunder at Hawks, Nets at Wizards, Timberwolves at Knicks, Spurs at Jazz — are the next pull's.)
Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07`, exit 0 (no kit row changed today).

**Method.** The four box scores read from ESPN's own feed (scoreboard and summary endpoints) before any search — starters, minutes, lines, DNP reasons and each summary's injury block — cross-referenced to both planes by script under `python3 -I` on the downloaded JSON (`scratchpad pull1012/boxscores.txt`, `box.json`, 154 player records). ESPN's league-wide injuries feed (130 rows, fetched 10/12 14:42 UTC) diffed against the deck's 51-row tag inventory in both directions by script (`injuries.txt`). The Basketball-Reference 2026-27 transactions page read directly (newest block still 10/8); NBA.com's news index and the 10/12 Starting 5 page egress-blocked at fetch time (369 and 414 bytes returned), the 10/11 Starting 5 ('Kyrie's return sparks Dallas in China') reached through the search as a link; ESPN's roster API for all 30 teams (the verifier, 335/335), ESPN's scoreboards 10/11–10/13. Then one sweep of 32 dated queries (26 standard, 6 extended): one recap query per game, a dedicated query for each of the ten flagged receipts, the ledger query, the league injury report, one team-shaped query for each of the seven teams in the watch set (CHI, GSW, LAC, MIL, NOP, POR, TOR), and the day's follow-ups (Raynaud's knee, Kessler, Miller's absence, Claxton's timeline, Suggs/Black, Holmgren/Hartenstein, Fox, Haliburton, Porziņģis). Egress-blocked as on every pull: Yahoo, SI, CBS, RotoWire, NBA.com's article pages and the other sports domains (their items rest on dated search summaries, labeled where they stand alone).

## 1. Roster changes

None. The ledger's newest block is 10/8 (Miami's two waivers); the transactions query found nothing dated 10/11 (its newest items are the Raptors' 10/5 waiver of Andre Jackson Jr. and Duren's 10/2 re-signing). No pool row changed team, entered or left; `report/projections-2026-27.csv` and `report/roster-provenance.csv` are byte-identical to yesterday's.

## 2. The box scores (ESPN's feed; the line is the evidence where no outlet named the row)

Four finals. Rows a dated outlet named (the recap queries): Kyrie Irving's return — 17 in 22 minutes, his first game since the March 3, 2025 ACL tear, a reverse layup on the first possession (ESPN, NBA.com Starting 5, Mavs Moneyball, Dallas Sports Journal, AP via KCBD); Cooper Flagg 14 and 7 assists and Marcus Smart 20 in his first Rockets appearance (AP, Mavs Moneyball); James Harden 24 on 7-of-10 in 26 minutes in his preseason debut after the ankle, Donovan Mitchell 11 (Yahoo, Fear the Sword); Brandon Miller 18 on four threes in his debut after the practice shin contusion and Tyler Herro 18 (Brew Hoop/Yahoo, CBS Sports, SI Hornets); Ryan Rollins 12 with a game-high three steals and two blocks, 'productive defensively' (RotoWire); Matas Buzelis back from the ankle with 13 and 6 in 23 minutes, Caleb Wilson 17 with five turnovers on a 'cold shooting night', Aaron Gordon 25 and Jokić a 22-point triple-double (Bleacher Report, Chicago Sun-Times, Bleacher Nation, Yahoo takeaways, On Tap Sports Net). Every other line below rests on the box score alone and is labeled so in the deck notes.

| game | player | team | plane | role | line (evidence: ESPN's box score) |
|---|---|---|---|---|---|
| Mavericks 132, Rockets 115 | Daniel Gafford | DAL | deck+kit | starter | 15 min, 9 pts, 4 reb, 0 ast, 0 stl, 0 blk, 1 to, FG 3-3, 3PT 0-0, FT 3-3 |
| Mavericks 132, Rockets 115 | P.J. Washington | DAL | deck+kit | starter | 16 min, 10 pts, 2 reb, 1 ast, 0 stl, 2 blk, 1 to, FG 3-7, 3PT 2-5, FT 2-2 |
| Mavericks 132, Rockets 115 | Cooper Flagg | DAL | deck+kit | starter | 25 min, 14 pts, 4 reb, 7 ast, 2 stl, 1 blk, 2 to, FG 3-10, 3PT 1-4, FT 7-8 |
| Mavericks 132, Rockets 115 | Zaccharie Risacher | DAL | deck+kit | starter | 24 min, 16 pts, 3 reb, 2 ast, 1 stl, 1 blk, 3 to, FG 7-13, 3PT 2-6, FT 0-0 |
| Mavericks 132, Rockets 115 | Kyrie Irving | DAL | deck+kit | starter | 22 min, 17 pts, 2 reb, 3 ast, 0 stl, 0 blk, 0 to, FG 6-13, 3PT 2-6, FT 3-3 |
| Mavericks 132, Rockets 115 | Naji Marshall | DAL | deck+kit | bench | 18 min, 14 pts, 2 reb, 0 ast, 3 stl, 2 blk, 1 to, FG 4-8, 3PT 1-3, FT 5-6 |
| Mavericks 132, Rockets 115 | Max Christie | DAL | deck+kit | bench | 22 min, 14 pts, 4 reb, 1 ast, 1 stl, 0 blk, 2 to, FG 4-7, 3PT 2-3, FT 4-4 |
| Mavericks 132, Rockets 115 | Santi Aldama | DAL | deck+kit | bench | did not play (coach's decision on the box score) |
| Mavericks 132, Rockets 115 | Morez Johnson Jr. | DAL | kit | bench | did not play (coach's decision on the box score) |
| Mavericks 132, Rockets 115 | Dereck Lively II | DAL | deck+kit | bench | did not play (coach's decision on the box score) |
| Mavericks 132, Rockets 115 | Jabari Smith Jr. | HOU | deck+kit | starter | 28 min, 14 pts, 9 reb, 4 ast, 1 stl, 0 blk, 2 to, FG 6-10, 3PT 2-6, FT 0-0 |
| Mavericks 132, Rockets 115 | Clint Capela | HOU | deck+kit | starter | 24 min, 5 pts, 9 reb, 0 ast, 0 stl, 1 blk, 3 to, FG 2-3, 3PT 0-0, FT 1-2 |
| Mavericks 132, Rockets 115 | Marcus Smart | HOU | deck+kit | starter | 24 min, 20 pts, 5 reb, 4 ast, 0 stl, 1 blk, 1 to, FG 7-13, 3PT 4-9, FT 2-3 |
| Mavericks 132, Rockets 115 | Amen Thompson | HOU | deck+kit | starter | 30 min, 14 pts, 7 reb, 6 ast, 1 stl, 1 blk, 2 to, FG 4-12, 3PT 1-4, FT 5-6 |
| Mavericks 132, Rockets 115 | Reed Sheppard | HOU | deck+kit | starter | 25 min, 17 pts, 1 reb, 1 ast, 1 stl, 2 blk, 5 to, FG 5-12, 3PT 4-10, FT 3-4 |
| Mavericks 132, Rockets 115 | Tari Eason | HOU | deck+kit | bench | 22 min, 9 pts, 6 reb, 0 ast, 1 stl, 1 blk, 1 to, FG 3-8, 3PT 0-3, FT 3-3 |
| Mavericks 132, Rockets 115 | Bogdan Bogdanovic | HOU | deck+kit | bench | 14 min, 7 pts, 4 reb, 0 ast, 1 stl, 0 blk, 4 to, FG 2-7, 3PT 2-6, FT 1-1 |
| Mavericks 132, Rockets 115 | Kevin Durant | HOU | deck+kit | bench | did not play (coach's decision on the box score) |
| Mavericks 132, Rockets 115 | Steven Adams | HOU | deck | bench | did not play (coach's decision on the box score) |
| Mavericks 132, Rockets 115 | Alperen Sengun | HOU | deck+kit | bench | did not play (coach's decision on the box score) |
| Mavericks 132, Rockets 115 | Fred VanVleet | HOU | deck+kit | bench | did not play (coach's decision on the box score) |
| Cavaliers 119, Magic 105 | Paolo Banchero | ORL | deck+kit | starter | 18 min, 10 pts, 7 reb, 2 ast, 0 stl, 1 blk, 3 to, FG 1-10, 3PT 1-3, FT 7-10 |
| Cavaliers 119, Magic 105 | Franz Wagner | ORL | deck+kit | starter | 15 min, 10 pts, 5 reb, 3 ast, 0 stl, 0 blk, 4 to, FG 4-7, 3PT 1-2, FT 1-1 |
| Cavaliers 119, Magic 105 | Tristan da Silva | ORL | deck+kit | starter | 24 min, 17 pts, 3 reb, 2 ast, 2 stl, 0 blk, 1 to, FG 6-14, 3PT 4-11, FT 1-2 |
| Cavaliers 119, Magic 105 | Wendell Carter Jr. | ORL | deck+kit | starter | 19 min, 4 pts, 5 reb, 2 ast, 1 stl, 1 blk, 1 to, FG 2-4, 3PT 0-0, FT 0-0 |
| Cavaliers 119, Magic 105 | Nikola Vucevic | ORL | deck+kit | bench | 11 min, 2 pts, 3 reb, 0 ast, 2 stl, 0 blk, 0 to, FG 1-6, 3PT 0-2, FT 0-0 |
| Cavaliers 119, Magic 105 | Goga Bitadze | ORL | deck+kit | bench | 12 min, 7 pts, 2 reb, 0 ast, 1 stl, 0 blk, 1 to, FG 3-3, 3PT 0-0, FT 1-2 |
| Cavaliers 119, Magic 105 | Desmond Bane | ORL | deck+kit | bench | did not play (coach's decision on the box score) |
| Cavaliers 119, Magic 105 | Jalen Suggs | ORL | deck+kit | bench | did not play (coach's decision on the box score) |
| Cavaliers 119, Magic 105 | Anthony Black | ORL | deck+kit | bench | did not play (coach's decision on the box score) |
| Cavaliers 119, Magic 105 | Jarrett Allen | CLE | deck+kit | starter | 25 min, 7 pts, 7 reb, 1 ast, 0 stl, 2 blk, 0 to, FG 3-8, 3PT 1-2, FT 0-0 |
| Cavaliers 119, Magic 105 | Evan Mobley | CLE | deck+kit | starter | 27 min, 14 pts, 7 reb, 2 ast, 0 stl, 2 blk, 2 to, FG 3-10, 3PT 0-1, FT 8-9 |
| Cavaliers 119, Magic 105 | James Harden | CLE | deck+kit | starter | 26 min, 24 pts, 4 reb, 2 ast, 1 stl, 0 blk, 2 to, FG 7-10, 3PT 3-5, FT 7-9 |
| Cavaliers 119, Magic 105 | Donovan Mitchell | CLE | deck+kit | starter | 26 min, 11 pts, 5 reb, 6 ast, 1 stl, 0 blk, 3 to, FG 3-9, 3PT 1-5, FT 4-5 |
| Cavaliers 119, Magic 105 | Peyton Watson | CLE | deck+kit | starter | 22 min, 6 pts, 4 reb, 1 ast, 2 stl, 0 blk, 1 to, FG 3-10, 3PT 0-3, FT 0-0 |
| Cavaliers 119, Magic 105 | Sam Merrill | CLE | deck+kit | bench | 18 min, 5 pts, 4 reb, 3 ast, 0 stl, 0 blk, 2 to, FG 1-2, 3PT 1-2, FT 2-2 |
| Cavaliers 119, Magic 105 | Jaylon Tyson | CLE | deck+kit | bench | 21 min, 13 pts, 2 reb, 1 ast, 0 stl, 0 blk, 1 to, FG 4-8, 3PT 3-5, FT 2-2 |
| Cavaliers 119, Magic 105 | Craig Porter Jr. | CLE | deck+kit | bench | 13 min, 0 pts, 1 reb, 4 ast, 1 stl, 0 blk, 1 to, FG 0-2, 3PT 0-0, FT 0-0 |
| Hornets 105, Bucks 90 | Kyle Kuzma | MIL | deck+kit | starter | 22 min, 12 pts, 4 reb, 2 ast, 2 stl, 0 blk, 2 to, FG 4-8, 3PT 2-5, FT 2-4 |
| Hornets 105, Bucks 90 | Jaime Jaquez Jr. | MIL | deck+kit | starter | 20 min, 9 pts, 7 reb, 4 ast, 0 stl, 0 blk, 0 to, FG 3-6, 3PT 2-3, FT 1-2 |
| Hornets 105, Bucks 90 | Myles Turner | MIL | deck+kit | starter | 24 min, 5 pts, 2 reb, 0 ast, 1 stl, 5 blk, 4 to, FG 2-7, 3PT 1-5, FT 0-0 |
| Hornets 105, Bucks 90 | Tyler Herro | MIL | deck+kit | starter | 23 min, 18 pts, 7 reb, 2 ast, 0 stl, 0 blk, 1 to, FG 6-13, 3PT 3-6, FT 3-3 |
| Hornets 105, Bucks 90 | Ryan Rollins | MIL | deck+kit | starter | 23 min, 12 pts, 4 reb, 2 ast, 3 stl, 2 blk, 0 to, FG 5-15, 3PT 2-8, FT 0-0 |
| Hornets 105, Bucks 90 | Kel'el Ware | MIL | deck+kit | bench | 24 min, 10 pts, 2 reb, 1 ast, 0 stl, 0 blk, 1 to, FG 4-9, 3PT 2-4, FT 0-0 |
| Hornets 105, Bucks 90 | Caris LeVert | MIL | deck+kit | bench | 18 min, 0 pts, 1 reb, 2 ast, 1 stl, 0 blk, 1 to, FG 0-3, 3PT 0-0, FT 0-2 |
| Hornets 105, Bucks 90 | Gary Trent Jr. | MIL | deck+kit | bench | 14 min, 0 pts, 2 reb, 0 ast, 1 stl, 0 blk, 1 to, FG 0-8, 3PT 0-5, FT 0-0 |
| Hornets 105, Bucks 90 | Kevin Porter Jr. | MIL | deck+kit | bench | 18 min, 6 pts, 4 reb, 4 ast, 2 stl, 0 blk, 1 to, FG 1-6, 3PT 0-2, FT 4-6 |
| Hornets 105, Bucks 90 | AJ Green | MIL | deck+kit | bench | 22 min, 6 pts, 2 reb, 4 ast, 0 stl, 0 blk, 1 to, FG 2-5, 3PT 2-4, FT 0-0 |
| Hornets 105, Bucks 90 | Johni Broome | MIL | deck+kit | bench | did not play (coach's decision on the box score) |
| Hornets 105, Bucks 90 | Moussa Diabate | CHA | deck+kit | starter | 20 min, 8 pts, 11 reb, 2 ast, 1 stl, 2 blk, 1 to, FG 3-5, 3PT 0-0, FT 2-4 |
| Hornets 105, Bucks 90 | Brandon Miller | CHA | deck+kit | starter | 23 min, 18 pts, 3 reb, 4 ast, 0 stl, 1 blk, 4 to, FG 6-15, 3PT 4-9, FT 2-2 |
| Hornets 105, Bucks 90 | Naz Reid | CHA | deck+kit | starter | 20 min, 16 pts, 2 reb, 1 ast, 0 stl, 1 blk, 0 to, FG 7-14, 3PT 2-6, FT 0-0 |
| Hornets 105, Bucks 90 | Dennis Schroder | CHA | deck+kit | starter | 17 min, 3 pts, 3 reb, 4 ast, 0 stl, 0 blk, 1 to, FG 1-2, 3PT 1-2, FT 0-0 |
| Hornets 105, Bucks 90 | Liam McNeeley | CHA | kit | starter | 27 min, 11 pts, 0 reb, 5 ast, 2 stl, 0 blk, 0 to, FG 4-11, 3PT 3-8, FT 0-0 |
| Hornets 105, Bucks 90 | Royce O'Neale | CHA | deck+kit | bench | 17 min, 9 pts, 1 reb, 1 ast, 1 stl, 0 blk, 1 to, FG 4-7, 3PT 1-4, FT 0-0 |
| Hornets 105, Bucks 90 | Hannes Steinbach | CHA | deck+kit | bench | 12 min, 8 pts, 5 reb, 1 ast, 0 stl, 0 blk, 1 to, FG 4-10, 3PT 0-0, FT 0-0 |
| Hornets 105, Bucks 90 | Ryan Kalkbrenner | CHA | deck+kit | bench | 12 min, 4 pts, 5 reb, 0 ast, 0 stl, 0 blk, 0 to, FG 2-2, 3PT 0-0, FT 0-0 |
| Hornets 105, Bucks 90 | Sion James | CHA | deck+kit | bench | 21 min, 11 pts, 5 reb, 4 ast, 0 stl, 0 blk, 2 to, FG 3-4, 3PT 3-4, FT 2-2 |
| Nuggets 133, Bulls 128 | Jalen Smith | CHI | deck+kit | starter | 14 min, 11 pts, 3 reb, 0 ast, 1 stl, 0 blk, 1 to, FG 4-6, 3PT 3-5, FT 0-0 |
| Nuggets 133, Bulls 128 | Isaac Okoro | CHI | deck+kit | starter | 13 min, 5 pts, 1 reb, 0 ast, 1 stl, 0 blk, 1 to, FG 2-2, 3PT 1-1, FT 0-0 |
| Nuggets 133, Bulls 128 | Matas Buzelis | CHI | deck+kit | starter | 23 min, 13 pts, 6 reb, 3 ast, 0 stl, 1 blk, 2 to, FG 5-10, 3PT 2-5, FT 1-2 |
| Nuggets 133, Bulls 128 | Caleb Wilson | CHI | deck+kit | starter | 25 min, 17 pts, 4 reb, 5 ast, 0 stl, 1 blk, 5 to, FG 6-10, 3PT 1-4, FT 4-7 |
| Nuggets 133, Bulls 128 | Josh Giddey | CHI | deck+kit | starter | 24 min, 7 pts, 1 reb, 8 ast, 1 stl, 1 blk, 1 to, FG 1-3, 3PT 1-2, FT 4-4 |
| Nuggets 133, Bulls 128 | Buddy Hield | CHI | deck | bench | 19 min, 15 pts, 3 reb, 1 ast, 2 stl, 0 blk, 1 to, FG 4-7, 3PT 4-6, FT 3-3 |
| Nuggets 133, Bulls 128 | Tre Jones | CHI | deck+kit | bench | 10 min, 0 pts, 1 reb, 5 ast, 1 stl, 0 blk, 0 to, FG 0-3, 3PT 0-0, FT 0-0 |
| Nuggets 133, Bulls 128 | Jordan Hawkins | CHI | deck | bench | 10 min, 6 pts, 0 reb, 0 ast, 0 stl, 0 blk, 1 to, FG 2-5, 3PT 2-3, FT 0-0 |
| Nuggets 133, Bulls 128 | Dailyn Swain | CHI | kit | bench | 15 min, 0 pts, 1 reb, 2 ast, 1 stl, 1 blk, 2 to, FG 0-4, 3PT 0-4, FT 0-0 |
| Nuggets 133, Bulls 128 | Zach Collins | CHI | deck+kit | bench | did not play (coach's decision on the box score) |
| Nuggets 133, Bulls 128 | Nic Claxton | CHI | deck+kit | bench | did not play (coach's decision on the box score) |
| Nuggets 133, Bulls 128 | Norman Powell | CHI | deck+kit | bench | did not play (coach's decision on the box score) |
| Nuggets 133, Bulls 128 | Aaron Gordon | DEN | deck+kit | starter | 23 min, 25 pts, 6 reb, 0 ast, 0 stl, 0 blk, 2 to, FG 9-12, 3PT 3-4, FT 4-5 |
| Nuggets 133, Bulls 128 | Cameron Johnson | DEN | deck | starter | 25 min, 15 pts, 3 reb, 1 ast, 2 stl, 0 blk, 1 to, FG 5-7, 3PT 4-5, FT 1-2 |
| Nuggets 133, Bulls 128 | Nikola Jokic | DEN | deck+kit | starter | 26 min, 22 pts, 11 reb, 10 ast, 0 stl, 1 blk, 4 to, FG 8-12, 3PT 1-2, FT 5-7 |
| Nuggets 133, Bulls 128 | Jamal Murray | DEN | deck+kit | starter | 26 min, 13 pts, 3 reb, 5 ast, 0 stl, 0 blk, 2 to, FG 4-11, 3PT 1-5, FT 4-4 |
| Nuggets 133, Bulls 128 | Christian Braun | DEN | deck+kit | starter | 23 min, 2 pts, 5 reb, 1 ast, 1 stl, 2 blk, 0 to, FG 1-6, 3PT 0-3, FT 0-0 |
| Nuggets 133, Bulls 128 | Cam Whitmore | DEN | kit | bench | 9 min, 4 pts, 0 reb, 1 ast, 0 stl, 0 blk, 0 to, FG 1-2, 3PT 0-0, FT 2-2 |
| Nuggets 133, Bulls 128 | DeMar DeRozan | DEN | deck+kit | bench | 9 min, 2 pts, 2 reb, 2 ast, 0 stl, 0 blk, 0 to, FG 0-4, 3PT 0-1, FT 2-2 |
| Nuggets 133, Bulls 128 | Julian Strawther | DEN | deck | bench | 17 min, 13 pts, 2 reb, 0 ast, 1 stl, 0 blk, 2 to, FG 5-12, 3PT 3-6, FT 0-0 |
| Nuggets 133, Bulls 128 | Marvin Bagley III | DEN | deck+kit | bench | did not play (coach's decision on the box score) |

Injury blocks of the four summaries (pool rows): Rockets — Adams, Şengün, VanVleet (rest, 10/15), Durant (not injury related, 10/15); Mavericks — Aldama (knee, 10/14), Lively (foot, 10/14); Magic — Black (right ankle sprain, 10/13), Bane (rest, 10/13), Suggs (illness, 10/13); Hornets — Grayson Allen (right knee soreness, 10/14), Coby White (calf, 10/21), Knueppel (hamstring, 10/21); Bucks — Jakucionis and Burries (coach's decision, 10/14); Bulls — Collins (toe, 10/14), Claxton (hamstring, 10/21).

## 3. Flagged-item receipts (F1) — verdicts

| player | query run (2026-10-12) | dated finding | verdict |
|---|---|---|---|
| Brandon Ingram | "Brandon Ingram Clippers Achilles update October 11 2026" | the 9/28 media-day items again (no timetable; re-evaluated when the season arrives); Out on ESPN's feed, 2026-11-01 | HELD; no October item |
| Kristaps Porzingis | "Kristaps Porzingis Warriors status update October 11 2026" + "… Slater NBA Today timetable indefinite" | the 9/28–10/6 items only; an undated 'timetable still indefinite' line attributed to NBA Today in the league injury summary could not be dated by a second query; ESPN's feed unchanged (10/21, Slater's 10/6 entry) | HELD; veto unchanged |
| Kawhi Leonard | "Kawhi Leonard Raptors Knicks preseason October 13 2026 status debut" + the TOR team query | no new item; the RotoBaller 'full practice Monday' item is the 10/5 one; Tuesday 10/13 vs the Knicks the first chance (TSN schedule), 10/13 estimate on the feed | HELD; re-check after 10/13 |
| Cam Thomas | "Cam Thomas signs free agent October 11 2026" | the February Bucks signing and the 2025 qualifying offer only; no signing on the ledger (10/8) | HELD, unsigned |
| Jaden Ivey | "Jaden Ivey signs free agent October 11 2026" | the March waiver items, RotoWire's free-agent listing; no signing on the ledger | HELD, unsigned |
| Jeremy Sochan | "Jeremy Sochan Trail Blazers London Lions October 12 2026 roster" + the POR team query | no dated item; on Portland's roster per ESPN's roster feed (335 of 335 verified today); the London Lions game is today at 20:00 UTC | HELD |
| Lonzo Ball | "Lonzo Ball signs free agent October 11 2026" | 2021 items only; no signing on the ledger | HELD, unsigned |
| Rob Dillingham | "Rob Dillingham signs free agent October 11 2026" | the 9/29 waiver items and ClutchPoints' landing-spot speculation; no signing on the ledger | HELD, unsigned |
| Bennedict Mathurin | "Bennedict Mathurin Pelicans October 11 2026 practice starting lineup" + the NOP team query | no dated item; no Pelicans game in the window (Wednesday vs Dallas next); the August signing items and summer projections | HELD; WO-5 decides |
| Ryan Rollins | "Ryan Rollins Bucks Hornets preseason October 11 2026 starting point guard" + the MIL team query + the Hornets recap | started at PG at Charlotte: 12 on 5-15, 3 steals, 2 blocks, 0 turnovers in 23 minutes (box score; RotoWire, Brew Hoop/Yahoo) — the starter question answered on the box | HELD; WO-5 decides the line |

## 4. The carried items

- **Maxime Raynaud** — the window's one new ruling. The Kings announced Sunday 10/11, after an MRI, a right patellar subluxation with no serious ligament damage, re-evaluated in approximately two weeks (ESPN, NBA.com, SI Kings, Yahoo, HoopsHype, all 10/11); he was taken off in a wheelchair in the 10/10 game; Out on ESPN's feed with a 10/25 estimate and 'will begin the regular season on the inactive list', Achiuwa and Cardwell the beneficiaries; one outlet counts the first three games missed if the timeline holds. Untagged on the deck (rank 230, below the draftable 156), kit GP 72 (board rank not on the 200-row board). The injury diff's one untagged Out row with an estimate past 10/21 → **D-1012-1** on the sheet, the Stewart shape (default (a): deck `inj-knee-risk` at 0.78 and kit GP 72 → 66, both planes at the next pull if silent; no board movement either way, since he sits below the pool mean on the deck and the kit never shrinks a negative).
- **The owed WO-5 projection pass.** The Sunday pass (Acuff, Lendeborg, Mathurin, Rollins, Daniels' steals, Flagg, the four LINE QUESTIONED names, Castle/Barrett's second step) did not run on 10/11 — the day went to the owner's decisions and their measurement. It is still owed before Wednesday's draft and is the next job after this pull; today's box scores add Rollins' start and Flagg's 14-and-7 to its evidence.
- **Kyrie Irving** — his first game in 587 days: 17 points in 22 minutes on 6-of-13, no turnovers; tag `inj-acl-risk` stays by the first-season-back convention (ESPN, NBA.com, Mavs Moneyball, Dallas Sports Journal, AP). **Cooper Flagg** 14/4/7 on 3-10 with 7-8 FT. **P.J. Washington** 10 in 16 minutes, **Gafford** 9 on 3-3 in 15 (both LINE QUESTIONED names for the WO-5 pass). **Marcus Smart** led Houston with 20 on four threes in his first Rockets appearance (tag `inj-risk` stays). **Reed Sheppard** 17 on 4-10 threes with 5 turnovers. **Durant, Şengün, VanVleet, Adams** rested (Durant by the plan announced 10/9).
- **James Harden** — 24 on 7-of-10 in 26 minutes in his debut after the ankle (Yahoo: 'no rust'); the 10/11 feed estimate is met. **Donovan Mitchell** 11 and 6 assists; **Mobley** 14 and 7 with 2 blocks on 8-9 FT; **Allen** 7 and 7. **Suggs, Black, Bane** sat in Cleveland — illness, right ankle sprain, rest; the feed names Tuesday 10/13 (Suggs) and Wednesday (Black) as the next chances; **Banchero** 1-of-10 for 10 in 18 minutes, **da Silva** 17 on 4-11 threes, **Vučević** 2 points in 11 minutes.
- **Brandon Miller** — his debut after the practice shin contusion (RotoBaller 10/7; the feed's 'leg bruise'): 18 on 6-15 with four threes, 4 turnovers, in 23 minutes; the contract-extension deadline is 10/19 per one report. **Ryan Rollins** — started at PG (the WO-5 starter question answered): 12 on 5-15, 3 steals, 2 blocks, 0 turnovers. **Myles Turner** 5 blocks and 4 turnovers; **Herro** 18; **Trent** 0-for-8; **Naz Reid** 16 for Charlotte; **Diabaté** 11 rebounds; **Grayson Allen** out with right knee soreness after 13 in 14 minutes in the opener; **Jakucionis, Burries** inactive (coach's decision).
- **Matas Buzelis** — back two days after the ankle, a start, 23 minutes, 13 and 6 (Bleacher Nation, Yahoo). **Caleb Wilson** 17/4/5 with 5 turnovers in 25 minutes (one recap says 17 minutes; the box score's 25 stands). **Nic Claxton** — out again; the two-week re-evaluation Splitter announced 10/5 lands right before the opener ('could cost a few regular-season games' — the Denver recap; Sun-Times 10/7); untagged, the feed's estimate 10/21 exactly. **Zach Collins** out (toe, 'will look to return before the regular season', RotoWire 10/12). **Tre Jones** 10 minutes, 5 assists. **Jokić** 22/11/10, **Gordon** 25, **Murray** 13 and 5, **DeRozan** 0-for-4 in 9 minutes.
- **Kessler** — no preseason minutes yet; questionable for Tuesday vs Golden State 'until the Lakers provide an update' (ESPN feed 10/11; the search returned the 10/8 items). **Holmgren, Hartenstein** — out tonight at Atlanta (carried from 10/10's feed entry); Tuesday vs Indiana is the last pre-draft look (D-1008-2 (a) holds). **Fox** — tonight at Utah the next chance after two missed games (10/12 estimate). **Haliburton** — 10/13 estimate, Tuesday at Oklahoma City. **Kawhi, Porziņģis, Ingram, Mathurin, Sochan, the four unsigned guards** — §3.
- **Stewart** (D-1010-2 applied 10/11; re-check about 10/22–10/23), **Coby White, Knueppel, Claxton** (the opener in question, re-evaluations about 10/19–10/21), **Strus, Lively, Nurkić** (exclusions stand) — no new item.
- **D-1011-4** (the owner's call on the judgment layer: veto, labels as they are, or a pre-registered engine change) — open; the default (b) holds, no change today.

## 5. Window sweep, team shadows, injury sweep

**Team shadows (7):** CHI — Buzelis back, Claxton and Collins out, the Denver box score; GSW — no dated item (Tuesday at the Lakers next; Porziņģis unchanged); LAC — no dated item (Beal's knee unchanged on the feed, 10/14; Ingram Out); MIL — the Charlotte box score, Rollins' start, Jakucionis and Burries inactive; NOP — no game, no item; POR — London Lions today, no cut news dated (Krejčí's $250K partial guarantee per Roundtable 9/28); TOR — Kawhi's Tuesday chance. No trade or signing touches a pool row.

**Injury sweep, both directions (mechanical).** ESPN's league injuries feed (130 rows, fetched 10/12 14:42 UTC) against the 51-row tag inventory (17 excluded, 34 risk):

| direction | evidence (the feed diff) |
|---|---|
| pool rows with status Out on the feed | 10: Isaiah Stewart (risk), Maxime Raynaud (UNTAGGED), Brandon Ingram (risk), Max Strus (excluded), Jusuf Nurkic (excluded), Moses Moody (excluded), Jimmy Butler III (excluded), Mark Williams (excluded), Shaedon Sharpe (excluded), Donte DiVincenzo (excluded) — Raynaud the one untagged Out row (10/25), D-1012-1 |
| tagged rows absent from the feed (candidates for 'cleared') | 30: the 9 `out-*` free agents and retirees and 21 risk rows (Davis, Lillard, Morant, Edey, Zion, Tatum, George, Robinson, Irving, Curry and the rest), all playing or practicing under their tags; none re-tagged (first-season-back convention) |
| untagged rows on the feed with Out or a return date after 10/21 | 1: Maxime Raynaud (Out, 10/25) → the owner's sheet |

Day-to-day items on the feed for untagged rows (not tier questions today): Dorian Finney-Smith, Nickeil Alexander-Walker, Mikel Brown Jr., Day'Ron Sharpe, Michael Porter Jr., Jaden McDaniels, Jonathan Kuminga, Ayo Dosunmu, Rudy Gobert, Anthony Edwards, LaMelo Ball, Tony Bradley, Ochai Agbaji, De'Aaron Fox, Lauri Markkanen, Khris Middleton, Tre Mann (10/12); T.J. McConnell, Ziaire Williams, Collin Sexton, Dalton Knecht, Chet Holmgren, Jaylin Williams, Alex Caruso, Jared McCain, Ajay Mitchell, Isaiah Hartenstein, Cason Wallace, Jalen Williams, Shai Gilgeous-Alexander, Anthony Black, Desmond Bane, Jalen Suggs, Dylan Cardwell, Domantas Sabonis, Malik Monk, Trayce Jackson-Davis, Allen Graves (10/13); Luka Garza, Grayson Allen, Zach Collins, Santi Aldama, Cade Cunningham, Jalen Duren, Kobe Sanders, Pelle Larsson, Bam Adebayo, Andrew Wiggins, Klay Thompson, Giannis Antetokounmpo, Davion Mitchell, Kasparas Jakucionis, Brayden Burries, Devin Booker, Miles Bridges (10/14); Alperen Sengun, Kevin Durant (10/15); Dru Smith, Kentavious Caldwell-Pope, Jaylen Brown, Dominick Barlow, Anfernee Simons, Adem Bona (10/16); Tobias Harris (10/20); Coby White, Kon Knueppel, Nic Claxton, Kyle Filipowski (10/21).

**Garbles caught (search summaries, logged, not used):** the Macao query's first Mavs Moneyball link was Friday's opener; the Hornets recap's SI item framed Miller's absence as the May shoulder surgery (the shin contusion is the dated cause); the Bulls recap disagreed with the box score on Wilson's minutes (17 vs 25); the Kawhi query's RotoBaller 'full practice Monday' is the 10/5 item and a 2017 Spurs piece surfaced; the Raptors team query returned 2019 items only; the Thunder–Hawks query returned 2024 Holmgren/Hartenstein injuries; the Fox query returned 2025 items; the Haliburton query returned the 2025 Finals; the Kessler query returned 10/8 items and a Jazz-era practice note; the Bucks team query returned 2023–25 injury reports; the Pelicans query returned the 2024 trade; the Thomas query's Fanatik item conflicts with the others; the Porziņģis 'NBA Today' line could not be dated and was not used.

## 6. Board effects (computed, never eyeballed)

- **Kit:** `rank_engine.py` re-run, 200 of 313 projected (12 held off: four unsigned, eight at GP ≤ 25); the diff against the morning snapshot is the generation-date line only — 0 entries, 0 exits, 0 moves.
- **Deck:** the draftable ordering recomputed before and after the edits (`scratchpad pull1012/deck_board_before.json`, `_after.json`): byte-identical, 318 live rows — notes only.

## 7. Deck build and publish

- `data/players.csv`: 93 notes appended on 93 rows (the four box scores on 75, the sweep on 18); no line, team or tag change; CRLF preserved, every other byte untouched; 0 notes violating D-1006-3 among the edits (Dylan Cardwell's pre-existing note still ends in `]`, untouched, the known trap).
- `scripts/verify_rosters.py` (no exemption): direct-complete, all 30 rosters, 335/335 matched, 0 mismatches, 0 unmatched; `roster_verification.json` and `rosters_official.json` dated today.
- `hoops.py freshness --stamp` with `--pool-changes` (gate 4): 2026-10-12; notes only asserted (32 dated queries in the note).
- `JUDGMENT` re-dated 2026-10-12 with the ten receipts (`judgment_open_items.py` flags the same ten; the three owner-note cards of 10/11 carry no lexicon marker); colophon Data paragraph rewritten for 10/12 (gate 6 accepted it).
- `build_deck.py`: planes 315 shared · team 0 · exclusion 0 · drift 0 · propagation 0 · waived 0; 170 line differences by design; market `yahoo-2026-10-09.csv`, 246/335 priced, 3 days old; built 335 players, pull 2026-10-12, pool 5e4acef794a2, injection round-trip OK, "safe to publish".
- `check_parity.py`: PARITY: EXACT MATCH. `test_card.py` CARD: all 99 cases passed; `test_draft.py` all 65 cases passed; `test_gates.py` all 54 cases passed. `full_dom_check.mjs` on `draft_state_54.json`: 143 assertions, 0 failed, [] page errors, pass true (`arena/results/full_dom_check_2026-10-12_v58.json`). `repeat_market_check.py`: 23 of 23 mocks replayed, 14 flagged (4 LINE QUESTIONED, 10 SOURCES SPLIT), 5 near misses (`arena/results/repeat_market_check_2026-10-12.json`).
- Published to the standing URL after a fresh read: Version 58, id 1791818861-878d, the standing URL; the served file carries the built page byte-for-byte inside the service's 364-byte wrapper; manifest built 2026-10-12

## 8. Gates (2026-10-12)

| gate | evidence |
|---|---|
| `report/check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07; exit 0 |
| `report/rank_engine.py` | exit 0; 200 of 313 projected (12 held off); board diff = the date line |
| `scripts/verify_rosters.py` (deck, no exemption) | direct-complete, all 30 rosters, 335/335, 0 mismatches, 0 unmatched; exit 0 |
| `hoops.py freshness --stamp --pool-changes` (deck) | 2026-10-12, notes only asserted |
| `scripts/build_deck.py` (deck) | gates 1–7 + F8 pass, no waiver; round-trip OK; "safe to publish" |
| `scripts/check_parity.py` (deck) | PARITY: EXACT MATCH; exit 0 |
| `scripts/test_card.py` / `test_gates.py` / `test_draft.py` (deck) | CARD: all 99 cases passed / all 54 cases passed / all 65 cases passed; exit 0 each |
| `arena/mocks/full_dom_check.mjs` (deck) | 143 assertions, 0 failed, [] page errors, pass true; exit 0 |
| `scripts/repeat_market_check.py` (deck) | 23 of 23 mocks replayed, 14 flagged (4 LINE QUESTIONED, 10 SOURCES SPLIT), 5 near misses; exit 0 |
| `report/check_report.py` | REPORT GATE: PASS — after-report-2026-10-12.md (structure, publication rule, pull-log row); exit 0 |
| `report/check_derived.py` | DERIVED: all 21 dated artifacts reproduce byte-for-byte from their pinned inputs; exit 0 |
| `scripts/judgment_open_items.py --check-report` (deck plane) | receipts check PASS — all 10 flagged names carry a receipts row in after-report-2026-10-12.md; exit 0 |
| `scripts/repeat_market_check.py --check-report` (deck plane) | REPEAT-NAME CHECK: PASS — after-report-2026-10-12.md: 14 flagged name(s), each with a row (23 of 23 mocks replayed); exit 0 |
| artifact publish | Version 58, id 1791818861-878d, the standing URL; the served file carries the built page byte-for-byte inside the service's 364-byte wrapper; manifest built 2026-10-12 |

## 9. Watchlist / open items

- **The WO-5 projection pass — owed, next.** Not run on Sunday; the draft is Wednesday. Acuff Jr. (D-1006-1), Lendeborg (D-1007-1), Mathurin, Rollins (started 10/11), Daniels' steals, Flagg, the LINE QUESTIONED names (PJ Washington, Gafford, Vassell, Herbert Jones), Castle/Barrett's second step; `range_check.py` and `identity_check.py` when lines move.
- **D-1012-1 (Raynaud)** — the default applies at the next pull if silent; re-check at the Kings' re-evaluation (about 10/25).
- **Tonight (10/12):** London Lions at Portland (Sochan, 20:00 UTC); Thunder at Hawks without Holmgren and Hartenstein; Nets at Wizards; Timberwolves at Knicks; Spurs at Jazz (Fox's next chance; Markkanen).
- **10/13 (the night before the draft):** Kawhi's first chance vs the Knicks; Thunder vs Pacers — the last pre-draft look at Holmgren and Hartenstein (D-1008-2) and Haliburton's next chance; Cavaliers at Magic (Suggs, Black); Warriors at Lakers (Kessler questionable; Lendeborg, Curry); Trail Blazers at Kings (Acuff, Simmons).
- **Claxton, Coby White, Knueppel, Harris, Stewart, Raynaud** — the opener in question for all six (re-evaluations about 10/19–10/25).
- **D-1011-4** — open (veto / labels / engine change); default (b) holds.
- **10/14 morning lock** — the fresh Yahoo ADP paste; the bigger-picture assessment on 10/13.

## Open-item receipts

| player | query run (2026-10-12) | dated finding |
|---|---|---|
| Brandon Ingram | "Brandon Ingram Clippers Achilles update October 11 2026" | no October item; the 9/28 media-day items; ESPN's feed 2026-11-01 — HELD |
| Kristaps Porzingis | "Kristaps Porzingis Warriors status update October 11 2026"; "… Slater NBA Today timetable indefinite October 2026" | the 9/28–10/6 items; the NBA Today line undated; feed unchanged (10/21) — HELD, veto unchanged |
| Kawhi Leonard | "Kawhi Leonard Raptors Knicks preseason October 13 2026 status debut"; the TOR team query | no new item; 10/13 vs the Knicks the first chance (TSN); the RotoBaller practice item is 10/5's — HELD |
| Cam Thomas | "Cam Thomas signs free agent October 11 2026" | the February signing items only; no signing on the ledger (newest block 10/8) — HELD, unsigned |
| Jaden Ivey | "Jaden Ivey signs free agent October 11 2026" | the March waiver items; RotoWire lists him a free agent; no signing on the ledger — HELD, unsigned |
| Jeremy Sochan | "Jeremy Sochan Trail Blazers London Lions October 12 2026 roster"; the POR team query | on Portland's roster per ESPN's roster feed; no waiver on the ledger; London Lions today — HELD |
| Lonzo Ball | "Lonzo Ball signs free agent October 11 2026" | 2021 items only; no signing on the ledger — HELD, unsigned |
| Rob Dillingham | "Rob Dillingham signs free agent October 11 2026" | the 9/29 waiver items; no signing on the ledger — HELD, unsigned |
| Bennedict Mathurin | "Bennedict Mathurin Pelicans October 11 2026 practice starting lineup"; the NOP team query | no game, no dated item; the August signing and summer projections — HELD, WO-5 |
| Ryan Rollins | "Ryan Rollins Bucks Hornets preseason October 11 2026 starting point guard"; the MIL team query; the Hornets recap | started at PG, 12 on 5-15, 3 stl, 2 blk (box score; RotoWire, Brew Hoop/Yahoo) — HELD, WO-5 decides the line |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 ca3fea1921d5), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 23 of 23 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-09.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-06.csv`, `hashtag-2026-10-09.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 5 players).

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

- Four finals in the window; today's five games are the next pull's. No line moved, so the range check and the points identity were not run (DATA-PULL §2); the owed WO-5 pass runs both when it moves a line.
- Raynaud's timeline rests on the Kings' Sunday announcement carried by ESPN, NBA.com, SI Kings, Yahoo and HoopsHype; 'misses the first three games' is one outlet's arithmetic on the two-week window, not a team statement; the inactive-list line is the feed's comment.
- Box-score lines not named by an outlet carry the [SINGLE-SOURCE: box score] label in the deck notes; the feed's day-to-day comments (Kessler, Şengün, VanVleet, Adams, Aldama, Jakucionis, Burries, Holmgren, Hartenstein, Fox) are labeled [SINGLE-SOURCE: ESPN feed] where no second outlet named them.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-1012-1 | Maxime Raynaud (SAC C, deck rank 230, kit GP 72, board rank not on the 200-row board): a right patellar subluxation per the Kings' 10/11 announcement, re-evaluated in approximately two weeks, Out on ESPN's feed with a 10/25 estimate and starting the season on the inactive list (ESPN, NBA.com, SI Kings, Yahoo, HoopsHype). Options: (a) deck `inj-knee-risk` (availability 0.78) and kit GP 72 → 66 (two weeks of the schedule), both planes at the next pull; (b) exclude on both planes, the Nurkić shape; (c) leave untagged. Either way no rank moves: he sits below the pool mean on the deck and the kit never shrinks a negative. | (a), applied at the next pull if silent — the Stewart precedent (D-1010-2): a two-week re-evaluation at the opener prices as a risk tier, not an exclusion |
| D-1011-4 | the judgment layer (veto / labels as they are / a pre-registered engine change) | (b) holds — carried |
| D-1010-2, D-1011-1..3, D-1010-1, D-RN-6, D73-1, D72-1, D71-1, D70-1, D69-1, D68-1..3, D61-4, D-RN-1..5, D67-1..6, D66-1, D-V4-1, D-CAST-1..4, D62-1..3, D-1008-1..3, D-1009-1..13 and earlier | carried | carried |

## Provenance

- Inputs: ESPN's scoreboards (10/11, 10/12, 10/13), the four summaries (401898400, 401898401, 401901821, 401908941), the league injuries feed and the 30 roster feeds (10/12 14:42–14:50 UTC, `scratchpad pull1012/dl/`); the Basketball-Reference 2026-27 transactions page fetched directly (NBA.com's pages egress-blocked); 32 dated search queries (`scratchpad pull1012/search_record.txt`).
- Scripts: `box_json.py`/`box.py` (the box records), `injdiff.py` (the two-way injury diff), `deck_edit.py` (93 notes; `deck_edit_record.json`), `judgment_colophon.py`, `deck_board.py` (before/after ordering), `chain.sh` (the deck chain; `chain.log`), `write_report.py` (this file).
- Deck results: `arena/results/full_dom_check_2026-10-12_v58.json`, `repeat_market_check_2026-10-12.json`; `data/roster_verification.json` and `data/freshness.json` dated 2026-10-12.
- Not verified: the Bucks', Raptors', Clippers', Warriors' and Pelicans' team-shaped queries returned nothing dated in the window (their items rest on the box scores, the feed and the schedule); the 10/12 Starting 5 (page blocked).

## In plain language

**What happened.** Four games. Kyrie Irving played his first game in 587 days and scored 17 in 22 minutes with no turnovers. James Harden made his preseason debut and led everyone with 24 on 7-of-10. Brandon Miller debuted with 18, and Ryan Rollins started at point guard for Milwaukee and had three steals and two blocks. Buzelis was back two days after the ankle, Caleb Wilson had a cold night with five turnovers, and Jokić posted a triple-double in 26 minutes.

**What moved.** Nothing on either board. The one new ruling is Maxime Raynaud: a kneecap subluxation, re-evaluated in two weeks, starting the season on the inactive list. He sits far below the draftable line on both boards, so the decision (D-1012-1, default: a risk tag and a six-game trim at the next pull) changes no rank; it is on the sheet because the rule is that every ruling past the opener gets your call.

**What is owed.** The Sunday projection pass did not happen yesterday; the day went to your three decisions and to proving what they do. It is the next job and the draft is Wednesday.

**The deck.** Rebuilt and republished as v58 with 93 dated notes and no line or tag change; every gate and the full page drive passed; the repeat-name check re-ran on the new page.

**Tonight and tomorrow.** Five games tonight, including Fox's next chance at Utah and the Thunder without Holmgren and Hartenstein. Tuesday is the night before your draft: Kawhi's first chance, the Thunder vs the Pacers for the only look at Holmgren and Hartenstein, the Warriors at the Lakers for Kessler and Lendeborg.
