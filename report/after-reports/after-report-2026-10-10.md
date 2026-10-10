# After-report — 2026-10-10 data pull + deck v55

**Owner request (2026-10-10, verbatim):** "Good morning! Please conduct daily refresh" — WO-3's daily pull.

Pull window: 2026-10-09 → 2026-10-10 (from the research pass's close on 10/9 evening, deck v54 published at 20:29 UTC, to 14:53 UTC on 10/10: one preseason game played in it — Grizzlies 104, Bulls 100 in Chicago, 10/9, tip 00:00 UTC 10/10. Tonight's seven games — Raptors–Clippers in Vancouver, Pacers–Hawks, Wizards–Pistons, Heat–Timberwolves, 76ers–Celtics, Kings–Warriors and Spurs–Suns — tip from 22:30 UTC and are the next pull's.)
Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07`, exit 0 (no kit row changed today).

**Method.** The box score read from ESPN's own feed (scoreboard and summary endpoints) before any search — starters, minutes, lines, DNP reasons and the summary's injury block — cross-referenced to both planes by script under `python3 -I` on the downloaded JSON (`scratchpad pull1010/boxscores.txt`, `box.json`). ESPN's league-wide injuries feed (120 rows) diffed against the deck's 50-row tag inventory in both directions by script (`injuries.txt`). The Basketball-Reference 2026-27 transactions page read directly (86 date blocks, newest 10/8), NBA.com's news index and its 10/9 and 10/10 Starting 5 columns, the Grizzlies' Stewart release on NBA.com and the Bulls' own game story fetched directly, ESPN's roster API for all 30 teams (the verifier), ESPN's scoreboards 10/9–10/11. Then one sweep of 30 dated queries (23 standard, 7 extended): a dedicated query for each of the ten flagged receipts, one team-shaped query for each of the seven teams in the watch set (CHI, GSW, LAC, MIL, NOP, POR, TOR), the ledger query, the game's recap, the league injury report, the day's pregame items (Kings–Warriors, Celtics–76ers, Spurs–Suns, Wizards–Pistons, Kessler, Harden, Buzelis) and Stewart's timeline. Egress-blocked as on every pull: Yahoo, SI, CBS, RotoWire and the other sports domains (their items rest on dated search summaries, labeled where they stand alone).

## 1. Roster changes

None. The ledger's newest block is 10/8 (Miami waived Lester Quinones and J'Vonne Hadley); the search found 10/9 minor moves only — the Lakers' Exhibit 10 for Rafael Castro with William Kyle III waived, the Pelicans waiving Christian Koloko, Miami's Exhibit 10 for Kylor Kelley (Hoops Rumors, Spotrac) — none a pool row on either plane. No pool row changed team, entered or left; `report/projections-2026-27.csv` and `report/roster-provenance.csv` are byte-identical to yesterday's.

## 2. The box score (ESPN's feed; the line is the evidence where no outlet named the row)

Grizzlies 104, Bulls 100 at the United Center, 10/9. Memphis started Coward, Boozer, Wells, Edey and Jerome; Chicago started Buzelis, Wilson, Awaka, Powell and Giddey. Rows named by a dated outlet: Caleb Wilson (21 on five threes in 32 minutes, a missed step-back for the lead — NBA.com Starting 5 10/10, Bulls.com, RotoBaller, Bleacher Report), Cameron Boozer (10 in 12 first-half minutes — NBA.com Starting 5, Bleacher Report), Matas Buzelis (out after 12 minutes with a right ankle sprain, 'sore' per Splitter, further evaluation expected — the Bulls on X, ClutchPoints, Heavy), Isaiah Stewart (§4). Every other line below rests on the box score alone and is labeled so in the deck notes.

| player | team | plane | role | line (evidence: ESPN's box score) |
|---|---|---|---|---|
| Cedric Coward | MEM | deck+kit | starter | 12 min, 2 pts, 2 reb, 0 ast, 0 stl, 0 blk, 0 to, FG 1-4, 3PT 0-2, FT 0-0 |
| Cameron Boozer | MEM | deck+kit | starter | 12 min, 10 pts, 4 reb, 3 ast, 0 stl, 0 blk, 0 to, FG 3-5, 3PT 0-1, FT 4-4 |
| Jaylen Wells | MEM | deck+kit | starter | 14 min, 8 pts, 2 reb, 1 ast, 1 stl, 0 blk, 1 to, FG 3-5, 3PT 2-2, FT 0-0 |
| Zach Edey | MEM | deck+kit | starter | 16 min, 10 pts, 5 reb, 0 ast, 2 stl, 1 blk, 3 to, FG 3-3, 3PT 0-0, FT 4-6 |
| Ty Jerome | MEM | deck+kit | starter | 14 min, 16 pts, 1 reb, 4 ast, 0 stl, 0 blk, 0 to, FG 5-8, 3PT 4-6, FT 2-2 |
| Jerami Grant | MEM | deck+kit | bench | 12 min, 9 pts, 1 reb, 0 ast, 0 stl, 0 blk, 0 to, FG 1-1, 3PT 0-0, FT 7-8 |
| Kris Murray | MEM | kit | bench | 16 min, 3 pts, 3 reb, 3 ast, 0 stl, 0 blk, 0 to, FG 1-1, 3PT 1-1, FT 0-0 |
| Taylor Hendricks | MEM | deck+kit | bench | 11 min, 5 pts, 2 reb, 1 ast, 0 stl, 0 blk, 1 to, FG 2-2, 3PT 1-1, FT 0-0 |
| GG Jackson | MEM | deck+kit | bench | 17 min, 14 pts, 4 reb, 1 ast, 0 stl, 1 blk, 1 to, FG 5-9, 3PT 1-3, FT 3-4 |
| Quinten Post | MEM | deck+kit | bench | 17 min, 4 pts, 1 reb, 0 ast, 1 stl, 0 blk, 0 to, FG 2-3, 3PT 0-0, FT 0-0 |
| Scotty Pippen Jr. | MEM | deck+kit | bench | 12 min, 2 pts, 0 reb, 0 ast, 3 stl, 0 blk, 1 to, FG 1-6, 3PT 0-1, FT 0-0 |
| Cam Spencer | MEM | deck+kit | bench | 16 min, 4 pts, 2 reb, 4 ast, 0 stl, 0 blk, 1 to, FG 2-5, 3PT 0-1, FT 0-0 |
| Isaiah Stewart | MEM | deck+kit | bench | did not play (coach's decision on the box score) |
| Matas Buzelis | CHI | deck+kit | starter | 12 min, 6 pts, 0 reb, 0 ast, 0 stl, 1 blk, 1 to, FG 3-6, 3PT 0-2, FT 0-0 |
| Caleb Wilson | CHI | deck+kit | starter | 32 min, 21 pts, 4 reb, 0 ast, 1 stl, 0 blk, 4 to, FG 7-17, 3PT 5-11, FT 2-6 |
| Norman Powell | CHI | deck+kit | starter | 19 min, 17 pts, 3 reb, 2 ast, 1 stl, 0 blk, 0 to, FG 3-6, 3PT 1-2, FT 10-12 |
| Josh Giddey | CHI | deck+kit | starter | 23 min, 13 pts, 3 reb, 3 ast, 0 stl, 1 blk, 2 to, FG 3-7, 3PT 1-3, FT 6-7 |
| Isaac Okoro | CHI | deck+kit | bench | 23 min, 5 pts, 3 reb, 3 ast, 1 stl, 0 blk, 1 to, FG 1-4, 3PT 0-0, FT 3-4 |
| Buddy Hield | CHI | deck | bench | 17 min, 5 pts, 2 reb, 2 ast, 0 stl, 0 blk, 1 to, FG 2-7, 3PT 1-4, FT 0-0 |
| Dailyn Swain | CHI | kit | bench | 18 min, 6 pts, 2 reb, 4 ast, 2 stl, 0 blk, 2 to, FG 2-6, 3PT 0-2, FT 2-2 |
| Zach Collins | CHI | deck+kit | bench | did not play (coach's decision on the box score) |
| Jalen Smith | CHI | deck+kit | bench | did not play (coach's decision on the box score) |
| Nic Claxton | CHI | deck+kit | bench | did not play (coach's decision on the box score) |
| Tre Jones | CHI | deck+kit | bench | did not play (coach's decision on the box score) |
| Jordan Hawkins | CHI | deck | bench | did not play (coach's decision on the box score) |

Injury block of the summary: Buzelis (right ankle, day-to-day, 10/11), Tre Jones (left hip, 10/11), Jalen Smith (left foot soreness, 10/11), Zach Collins (right toe, 'nearing a return', 10/11), Jaylin Sellers (back, 10/11); Micah Peavy (ankle, 10/16); Isaiah Stewart (Out, left ankle, 10/23).

## 3. Flagged-item receipts (F1) — verdicts

| player | query run (2026-10-10) | dated finding | verdict |
|---|---|---|---|
| Brandon Ingram | "Brandon Ingram Clippers Achilles update October 2026" | only the 9/28 items (NBC Sports, abc30, TSN); ESPN's feed Out with a 2026-11-01 estimate | HELD; no October item |
| Kristaps Porzingis | "Kristaps Porzingis Warriors status October 9 2026" + the GSW team query | out indefinitely per Slater on ESPN's feed (10/6 entry); no team timeline; misses tonight vs Sacramento (NBC Sports Bay Area, Blue Man Hoop) | HELD; veto unchanged |
| Kawhi Leonard | "Kawhi Leonard Raptors Vancouver preseason October 10 2026 status" | sits tonight's Vancouver game, his second straight, not injury related; ESPN's feed 10/13 estimate, Tuesday vs the Knicks the next chance (ESPN injuries feed 10/9; TSN, Daily Hive, NBC Sports 10/3) | HELD; re-check after 10/13 |
| Cam Thomas | "Cam Thomas free agent signing October 2026" | nothing past February; the ledger's newest block (10/8) carries no signing | HELD, unsigned |
| Jaden Ivey | "Jaden Ivey free agent October 2026 signs" | RotoWire lists him a free agent; no signing on the ledger | HELD, unsigned |
| Jeremy Sochan | "Jeremy Sochan Spurs non-guaranteed contract October 2026" + the POR team query | on Portland's roster per ESPN's roster feed (335 of 335 verified today); no waiver on the ledger; the August signing items only | HELD |
| Lonzo Ball | "Lonzo Ball free agent October 2026" | nothing past February; no signing on the ledger | HELD, unsigned |
| Rob Dillingham | "Rob Dillingham signs October 2026" | the 9/29 waiver items (RotoBaller, Saturday Down South); no signing on the ledger | HELD, unsigned |
| Bennedict Mathurin | "Bennedict Mathurin Pelicans starting lineup October 2026" | Roundtable 10/7: the Murray–Jones–Murphy–Williamson–Missi first unit 'likely' to open the season, Mathurin off the bench; he started 10/8 with Murray out (box score) | HELD; WO-5 decides |
| Ryan Rollins | "Ryan Rollins Bucks starter October 2026 preseason" | Bleacher Report's lineup piece lists him the starting PG with Burries the challenger; Roundtable 10/6: the opener's only plus-net-rating starter; RotoWire's stale 10/1 thumb estimate logged as a garble | HELD; WO-5 decides |

## 4. The carried items

- **Isaiah Stewart** — the window's one new ruling. The Grizzlies' update (NBA.com, 10/10 05:00 UTC): a moderate left ankle sprain from the 10/5 opener, re-evaluated in two weeks; likely to miss the 10/21 opener per NBC Sports (10/9) and Yahoo; Out on ESPN's league feed with a 10/23 estimate; Quinten Post the backup-C option behind Edey meanwhile (ESPN feed). Untagged on the deck (rank 180, below the draftable 156), kit GP 70. The injury diff's one untagged row with an estimate past 10/21 → **D-1010-2** on the sheet (default (a): deck `inj-ankle-risk` at 0.78 and kit GP 70 → 64, applied at the next pull if silent; the Nurkić exclusion shape does not fit a two-week re-evaluation that lands at the opener). DNP the 10/9 game.
- **Matas Buzelis** — right ankle sprain, out after 12 minutes of the 10/9 game, precautionary per the Bulls, 'sore' per Splitter; day-to-day with a 10/11 estimate, Sunday at Denver the next chance. Untagged (deck 125); a tier question only if Sunday's update names a timeline.
- **Nic Claxton** — DNP (coach's decision on the box; the hamstring per the feed): out for the preseason, re-evaluated about 10/19, questionable for the 10/21 opener; 'could return right when the regular season begins' per ClutchPoints/Yahoo. Untagged, the feed's estimate is 10/21 exactly (not past it); carried, the opener in question.
- **Kevin Durant** — sits Sunday's Macao rematch, a planned precaution per Udoka after he asked for extra minutes on 10/9 (ESPN feed; Houston Chronicle via the feed); 10/15 estimate. D-1009-13's default holds.
- **Miles Bridges** — right ankle X-rays negative per Ott (10/9); questionable for tonight vs San Antonio, the team to 'be smart' with him (ESPN feed).
- **Alex Sarr** — Keefe (10/9): trending in a positive direction, a decision on tonight vs Detroit made Saturday (ESPN feed). Tag stays by the first-season-back convention.
- **Ben Simmons** — in line for his Kings preseason debut tonight vs Golden State (Spears via ESPN's feed; NBC Sports Bay Area preview). **Sabonis, Keegan Murray, Monk** — tonight the named chance; no new item.
- **Anthony Black** — a full practice participant 10/9, a preseason debut possible Sunday at Cleveland (ESPN feed; Orlando Sentinel via the feed). **Suggs** — illness, Sunday the first chance.
- **Kawhi, Porziņģis, Ingram, Mathurin, Rollins, Sochan, the four unsigned guards** — §3.
- **Harden** (10/11 estimate, Sunday vs Orlando), **P.J. Washington, Irving, Aldama** (Sunday's Macao rematch), **Fox, Castle** (tonight at Phoenix — the D-CAST-2a minutes re-check), **Kessler** (Tuesday vs Golden State), **Hartenstein, Holmgren** (10/12 at Atlanta, D-1008-2 holds), **Lendeborg** (tonight vs Sacramento, D-1007-1 holds), **Tre Jones, Jalen Smith, Collins** (Sunday at Denver), **Acuff Jr.** (WO-5) — no new item beyond the feed's estimates.
- **Strus, Lively, Nurkić** — exclusions stand; Lively out of Macao again Sunday per the feed.

## 5. Window sweep, team shadows, injury sweep

**Team shadows (7):** CHI — Buzelis's ankle and Claxton's hamstring (above); GSW — Porziņģis out indefinitely, Lendeborg's center minutes, Sacramento tonight; LAC — Vancouver tonight, no Harden item found, Beal's knee unchanged; MIL — Charlotte 10/11, no dated item (the query returned nothing current); NOP — Koloko waived (not a pool row), Murray's toe (10/14 estimate); POR — no dated item, London Lions 10/12; TOR — Kawhi sits tonight. No trade or signing touches a pool row.

**Injury sweep, both directions (mechanical).** ESPN's league injuries feed (120 rows, fetched 10/10 14:55 UTC) against the 50-row tag inventory (17 excluded, 33 risk):

| direction | evidence (the feed diff) |
|---|---|
| pool rows with status Out on the feed | 8: Ingram (risk), Strus, Nurkić, Moody, Butler, Mark Williams, Shaedon Sharpe, DiVincenzo (excluded) — and Isaiah Stewart, the one untagged Out row (10/23 estimate), D-1010-2 |
| tagged rows absent from the feed (candidates for 'cleared') | 27: the nine `out-*` free agents and retirees and 18 risk rows (Davis, Lillard, Morant, Haliburton, Edey, Zion, Embiid, LeBron, Irving, VanVleet and the rest), all playing or practicing under their tags; none re-tagged (first-season-back convention) |
| untagged rows on the feed with Out or a return date after 10/21 | 1: Isaiah Stewart (Out, 10/23) → the owner's sheet |

Day-to-day items on the feed for untagged rows (not tier questions today): Luguentz Dort, Jalen Johnson, Sam Hauser, Payton Pritchard, Neemias Queta, Derrick White, Jalen Duren, Gui Santos, Brandin Podziemski, Gary Payton II, Yaxel Lendeborg, Draymond Green, T.J. McConnell, Kobe Sanders, Pelle Larsson, Miles Bridges, Domantas Sabonis, Malik Monk, De'Aaron Fox, Trayce Jackson-Davis, Allen Graves, Khris Middleton (10/10); Brandon Miller, Matas Buzelis, Tre Jones, Jalen Smith, Zach Collins, James Harden, P.J. Washington, Santi Aldama, Anthony Black, Jalen Suggs (10/11); Mikel Brown Jr., Day'Ron Sharpe, Michael Porter Jr., Tony Bradley, Ochai Agbaji, Chet Holmgren, Isaiah Hartenstein, Jaylin Williams, Lauri Markkanen, Kyle Filipowski (10/12); Dalton Knecht, Collin Sexton, Ziaire Williams (10/13); Kevin Durant (10/15); Dru Smith, Dominick Barlow, Anfernee Simons, Adem Bona (10/16); Tobias Harris (10/20); Coby White, Kon Knueppel, Nic Claxton (10/21).

**Garbles caught (search summaries, logged, not used):** NBC Sports' Stewart item places the injury against the Pistons (the Grizzlies' release and ESPN's feed say the 10/5 game at Atlanta); the Harden query returned 2013 Rockets items and an undated 'sat Friday vs the Warriors' line; the Kings–Warriors query returned 2013–2025 games; the Bucks queries returned nothing dated and a podcast feed's AI-produced 'Giannis trade' claim; the Raptors query returned 2024-25 injury reports and called the Vancouver game non-existent; the Buzelis query returned April 2026 items; the Lonzo Ball query returned 2019–2021 items; the Sochan query returned the August signing; Rollins' RotoWire page carries a stale 10/1 thumb estimate; the Celtics–76ers query returned a 2025 preview.

## 6. Board effects (computed, never eyeballed)

- **Kit:** `rank_engine.py` re-run, 200 of 313 projected (12 held off: four unsigned, eight at GP ≤ 25); the diff against the morning snapshot is the generation-date line only — 0 entries, 0 exits, 0 moves of three places or more.
- **Deck:** the draftable ordering recomputed before and after the edits (`scratchpad pull1010/deck_board_before.json`, `_after.json`): byte-identical, 318 live rows — notes only.

## 7. Deck build and publish

- `data/players.csv`: 38 notes appended on 38 rows (the box score on 23, the sweep on 15); no line, team or tag change; CRLF preserved, every other byte untouched; 0 notes violating D-1006-3 among the edits (Dylan Cardwell's pre-existing note still ends in `]`, untouched, the known trap).
- `scripts/verify_rosters.py` (no exemption): direct-complete, all 30 rosters, 335/335 matched, 0 mismatches, 0 unmatched; `roster_verification.json` and `rosters_official.json` dated today.
- `hoops.py freshness --stamp` with `--pool-changes` (gate 4): 2026-10-10; notes only. The first build of the day consumed that assertion, so a corrected stamp (the query count, 28 → 30) was applied to the committed v54 page restored from git, the JUDGMENT and colophon edits re-applied, and the page rebuilt — gate 4 refused the intermediate rebuild exactly as designed.
- `JUDGMENT` re-dated 2026-10-10 with the ten receipts (`judgment_open_items.py` flags all ten); colophon Data paragraph rewritten for 10/10 (gate 6 accepted it).
- `build_deck.py`: planes 315 shared · team 0 · exclusion 0 · drift 0 · propagation 0 · waived 0; 170 line differences by design; market `yahoo-2026-10-09.csv`, 246/335 priced, 1 day old; built 335 players, pull 2026-10-10, pool ea2762e6e262, injection round-trip OK, "safe to publish".
- `check_parity.py`: PARITY: EXACT MATCH. `test_card.py` CARD: all 99 cases passed; `test_draft.py` all 65 cases passed; `test_gates.py` all 54 cases passed. `full_dom_check.mjs` on `draft_state_54.json`: 143 assertions, 0 failed, [] page errors, pass true (`arena/results/full_dom_check_2026-10-10_v55.json`). `repeat_market_check.py`: 23 of 23 mocks replayed, 14 flagged (4 LINE QUESTIONED, 10 SOURCES SPLIT), 5 near misses (`arena/results/repeat_market_check_2026-10-10.json`).
- Published to the standing URL after a fresh read: Version 55, id 1791646358-9ba4, the standing URL; the served file carries the built page byte-for-byte inside the service's 364-byte wrapper; manifest built 2026-10-10

## 8. Gates (2026-10-10)

| gate | evidence |
|---|---|
| `report/check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07; exit 0 |
| `report/rank_engine.py` | exit 0; 200 of 313 projected (12 held off); board diff = the date line |
| `scripts/verify_rosters.py` (deck, no exemption) | direct-complete, all 30 rosters, 335/335, 0 mismatches, 0 unmatched; exit 0 |
| `hoops.py freshness --stamp --pool-changes` (deck) | 2026-10-10, notes only asserted |
| `scripts/build_deck.py` (deck) | gates 1–7 + F8 pass, no waiver; round-trip OK; "safe to publish" |
| `scripts/check_parity.py` (deck) | PARITY: EXACT MATCH; exit 0 |
| `scripts/test_card.py` / `test_gates.py` / `test_draft.py` (deck) | CARD: all 99 cases passed / all 54 cases passed / all 65 cases passed; exit 0 each |
| `arena/mocks/full_dom_check.mjs` (deck) | 143 assertions, 0 failed, [] page errors, pass true; exit 0 |
| `scripts/repeat_market_check.py` (deck) | 23 of 23 mocks replayed, 14 flagged (4 LINE QUESTIONED, 10 SOURCES SPLIT), 5 near misses; exit 0 |
| `report/check_report.py` | REPORT GATE: PASS — after-report-2026-10-10.md (structure, publication rule, pull-log row); exit 0 |
| `report/check_derived.py` | DERIVED: all 21 dated artifacts reproduce byte-for-byte from their pinned inputs; exit 0 |
| `scripts/judgment_open_items.py --check-report` (deck plane) | receipts check PASS — all 10 flagged names carry a receipts row in after-report-2026-10-10.md; exit 0 |
| `scripts/repeat_market_check.py --check-report` (deck plane) | REPEAT-NAME CHECK: PASS — after-report-2026-10-10.md: 14 flagged name(s), each with a row (23 of 23 mocks replayed); exit 0 |
| artifact publish | Version 55, id 1791646358-9ba4, the standing URL; the served file carries the built page byte-for-byte inside the service's 364-byte wrapper; manifest built 2026-10-10 |

## 9. Watchlist / open items

- **D-1010-2 (Stewart)** — the default applies at the next pull if silent; re-check the Grizzlies' two-week re-evaluation (about 10/22–10/23).
- **Buzelis** — Sunday's update on the ankle; a timeline past 10/21 would make him the next sheet item.
- **Tonight's seven games** — Simmons' debut, Sabonis/Murray/Monk, Fox and Castle at Phoenix (D-CAST-2a), Lendeborg vs Sacramento, Kawhi out, Sarr's decision, Bridges' ankle, Tatum/George/White after Thursday's rest — the next pull's box scores.
- **Sunday's Macao rematch** — Irving's first game (D-1009-11..13 context), P.J. Washington and Aldama, Durant resting by plan, Lively out.
- **Claxton, Coby White, Knueppel, Harris** — the opener in question for all four (re-evaluations about 10/19–10/20).
- **WO-5 (Sunday)** — Acuff Jr., Mathurin, Rollins, Daniels' steals, Flagg, the LINE QUESTIONED names (PJ Washington, Gafford, Vassell, Herbert Jones) per the work order.

## Open-item receipts

| player | query run (2026-10-10) | dated finding |
|---|---|---|
| Brandon Ingram | "Brandon Ingram Clippers Achilles update October 2026" | no October item; the 9/28 items stand (NBC Sports, abc30, TSN); ESPN's feed 2026-11-01 estimate — HELD |
| Kristaps Porzingis | "Kristaps Porzingis Warriors status October 9 2026"; GSW team query | out indefinitely per Slater (ESPN feed 10/6), misses tonight (NBC Sports Bay Area, Blue Man Hoop) — HELD, veto unchanged |
| Kawhi Leonard | "Kawhi Leonard Raptors Vancouver preseason October 10 2026 status" | sits tonight, not injury related, 10/13 estimate (ESPN feed 10/9; TSN, Daily Hive, NBC Sports) — HELD |
| Cam Thomas | "Cam Thomas free agent signing October 2026" | nothing past February; no signing on the ledger (newest block 10/8) — HELD, unsigned |
| Jaden Ivey | "Jaden Ivey free agent October 2026 signs" | RotoWire lists him a free agent; no signing on the ledger — HELD, unsigned |
| Jeremy Sochan | "Jeremy Sochan Spurs non-guaranteed contract October 2026"; POR team query | on Portland's roster per ESPN's roster feed; no waiver on the ledger — HELD |
| Lonzo Ball | "Lonzo Ball free agent October 2026" | nothing past February; no signing on the ledger — HELD, unsigned |
| Rob Dillingham | "Rob Dillingham signs October 2026" | the 9/29 waiver items only (RotoBaller, Saturday Down South); no signing on the ledger — HELD, unsigned |
| Bennedict Mathurin | "Bennedict Mathurin Pelicans starting lineup October 2026" | Roundtable 10/7: bench to open the season behind Jones and Murphy; started 10/8 with Murray out (box score) — HELD, WO-5 |
| Ryan Rollins | "Ryan Rollins Bucks starter October 2026 preseason" | the starting PG per Bleacher Report's lineup piece and Roundtable 10/6 — HELD, WO-5 |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 f17f55ea920c), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 23 of 23 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-09.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-06.csv`, `hashtag-2026-10-09.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 5 players).

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

- One box score in the window; tonight's seven games and Sunday's Macao rematch are the next pull's. No line moved, so the range check and the points identity were not run (DATA-PULL §2).
- Stewart's timeline rests on the team's release (NBA.com) with NBC Sports, Yahoo and SI Grizzlies alongside; 'likely to miss the opener' is the outlets' reading of a two-week re-evaluation, not a team statement.
- Box-score lines not named by an outlet carry the [SINGLE-SOURCE: box score] label in the deck notes; the feed's day-to-day comments (Durant, Bridges, Sarr, Black, the Bulls' three) are labeled [SINGLE-SOURCE: ESPN feed] where no second outlet named them.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-1010-2 | Isaiah Stewart (MEM C, deck rank 180, kit GP 70): a moderate left ankle sprain, re-evaluated in two weeks per the Grizzlies' release (NBA.com 10/10), Out on ESPN's feed with a 10/23 estimate, likely to miss the 10/21 opener per NBC Sports (10/9), Yahoo and SI Grizzlies. Options: (a) deck `inj-ankle-risk` (availability 0.78) and kit GP 70 → 64 (two weeks of the schedule), both planes at the next pull; (b) exclude on both planes, the Nurkić shape; (c) leave untagged. | (a), applied at the next pull if silent — a two-week re-evaluation lands at the opener, so a risk tier, not an exclusion, prices it; re-check when the Grizzlies re-evaluate |
| D-1010-1, D-RN-6, D73-1, D72-1, D71-1, D70-1, D69-1, D68-1..3, D61-4, D-RN-1..5, D67-1..6, D66-1, D-V4-1, D-CAST-1..4, D62-1..3, D-1008-1..3, D-1009-1..13 and earlier | carried | carried |

## Provenance

- Inputs: ESPN's scoreboard (10/9, 10/10, 10/11), summary 401908940, the league injuries feed and the 30 roster feeds (all 10/10 14:53–14:58 UTC, `scratchpad pull1010/dl/`); the Basketball-Reference 2026-27 transactions page, NBA.com's news index, its 10/9 and 10/10 Starting 5 columns, the Grizzlies' Stewart release and the Bulls' game story, fetched directly; 30 dated search queries (`search_record` in the session transcript).
- Scripts: `box_json.py`/`box.py` (the box records), `injdiff.py` (the two-way injury diff), `deck_edit.py` (38 notes; `deck_edit_record.json`), `judgment_colophon.py`, `deck_board.py` (before/after ordering), `chain.sh` (the deck chain; `chain.log`), `write_report.py` (this file).
- Deck results: `arena/results/full_dom_check_2026-10-10_v55.json`, `repeat_market_check_2026-10-10.json`; `data/roster_verification.json` and `data/freshness.json` dated 2026-10-10.
- Not verified: the Bucks' and Raptors' team-shaped queries returned nothing dated in the window (their items rest on the schedule, the roster feed and the Kawhi query).

## In plain language

**What happened.** One game in the window: the Grizzlies beat the Bulls in Chicago. Caleb Wilson scored 21 on five threes in 32 minutes, Boozer had 10 in 12, Edey started again and played 16, Ty Jerome hit four threes, and Matas Buzelis left after 12 minutes with a sprained ankle that the Bulls call day-to-day.

**What moved.** Nothing on either board. Isaiah Stewart is the one new ruling: a moderate ankle sprain, re-evaluated in two weeks, so he likely misses opening night. He sits outside the draftable 156, and the question of how to price it is yours as D-1010-2 (default: a risk tag and a games trim at the next pull).

**The deck.** Rebuilt and republished as v55 with 38 dated notes and no line or tag change; every gate and the full page drive passed; the repeat-name check re-ran on the new page.

**Tonight.** Seven games, including Simmons' debut, Fox and Castle at Phoenix, and the Celtics' regulars back. Sunday brings Irving's first game in Macao. Both are tomorrow's pull.
