# After-report — 2026-10-07 data pull + deck v47, with the Lendeborg read

**Owner request (2026-10-07, verbatim):** "Good morning Claude! Please conduct daily refresh
pull and provide after report. I am bullish on Lendeborg and see him as a potential draft
target should he fit my build" — WO-3's daily pull plus a dedicated read on one player (§2).

Pull window: 2026-10-06 → 2026-10-07 (from the Tuesday pull's run time, 19:30 UTC on 10/6,
to the morning of 10/7: four preseason games played in it — Hornets–Nets, Thunder–Pelicans
in Tulsa, Jazz–Nuggets and Warriors–Lakers, all 10/6 — and five more tip after this pull).
Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13
.. 2026-10-06`, exit 0 (no provenance row changed today, so the range end stands).

**Method.** The four box scores read from ESPN's own feed (scoreboard and summary endpoints,
the same host the verifier uses) before any search: starters, minutes, lines and DNP reasons
for every pool row that dressed, plus the summaries' own injury blocks (status, body part,
the feed's return estimate), cross-referenced to both planes by script (`scratchpad
pull1007/boxscores.txt`). Then one search sweep of 54 dated queries: the ledger-shaped
transaction check (Basketball-Reference's 2026-27 transactions page read directly — 114
dated entries parsed, newest 10/5 — plus one search ledger), a dedicated query for each of
the ten flagged receipts, one team-shaped query for each of the seven teams in the watch set
(CHI, GSW, LAC, MIL, NOP, POR, TOR), the injury sweep in both directions against the 46-row
tag inventory, the free-agent rows, the carried items (Strus, Claxton, Harris, Hawkins,
Lively, Beal, Knueppel, Bona, Brown Jr., Black, Suggs, Edey, Duren, Simmons, Monk, Keegan
Murray, Acuff, Alexander-Walker, Dort, McCollum, Queta, Steinbach vs Diabaté, Vincent,
Konchar, Broome), four game recaps re-run in extended mode after the first pass returned
2013, 2015 and 2025 games, and three queries on Lendeborg. Direct fetches: NBA.com's news
index, its 10/7 Starting 5 column and its Hawkins release (all open); ESPN's roster API for
all 30 teams (the verifier) and four rosters by hand (MEM, MIL, CHI, CHA). Egress-blocked
today: NBC Sports Bay Area, Deseret News, the Gazette and the Hornets Substack (their items
rest on dated search summaries, labeled where they stand alone).

## 1. Roster changes

No row changed team, tier or line on either plane. One transaction in the window touches a
pool row and is held by the deck's rule:

| player | change | date | sources | applied? |
|---|---|---|---|---|
| Jordan Hawkins | waived by MEM 10/2, cleared waivers 10/5, signed a two-way contract with CHI (Isaiah Stevens waived) | 2026-10-06 | NBA.com release (fetched, 20:12 UTC), ESPN/Shams, Yahoo, Hoops Rumors, Heavy | **No** — ESPN's official roster feed still lists him on Memphis (21 names) and not on Chicago (19) at the 10/7 direct-complete check; placement follows the feed (D-1005-4 re-put). Deck rank 252 of 323 draftable, no kit row. |
| Johni Broome | signed MIL 10/6 (applied yesterday) | 2026-10-06 | NBA.com, RotoWire, Hoops Rumors | Still not on ESPN's Milwaukee feed (Butler Jr. still listed); the by-name exemption continues |

Zero trades in the window: the Basketball-Reference ledger's October entries are Exhibit 10
signings and waivers only (10/1–10/5), and the search ledger (Hoops Rumors' transactions
index, "Minor Roster Moves: Magic, Raptors, Jazz, Kings", "Bucks Sign Johni Broome") agrees.
The NBA.com headline "Hornets send Buddy Hield to Bulls for Rob Dillingham" is the 9/27 trade
already in both pools (index date 2026-09-27T00:51Z), not a new one. One injury with a pool
effect: Ariel Hukporti's right Achilles tear is season-ending (NBA.com 10/6, Yahoo, PhillyVoice
10/6) — not a pool row; it clears the backup-center path for Adem Bona once he is cleared (§4).

## 2. Lendeborg — the owner's note

**The role evidence, two games.** Both from ESPN's feed, both starts:

| date | opponent | lineup | min | line | notes |
|---|---|---|---|---|---|
| 10/4 | LAC (L 101–104) | Curry, Podziemski, Lendeborg, Green, Horford | 19 | 4 pts (1-6), 9 reb, 3 ast | Kerr: "we need him to be more aggressive" (Yahoo, Heavy, SI) |
| 10/6 | LAL (W 124–98) | Green, Santos, Lendeborg, Curry, Podziemski | 21 | 17 pts (7-11, 2-3 3PT, 1-2 FT), 9 reb, 2 ast, 1 blk, 2 to | team's top scorer; Horford rested; NBC Sports Bay Area: "dominates in Chase Center debut" |

The standing role claim — Kerr's "clearly going to play a ton", starter or not (Yahoo rookie
targets, NBA.com media day) — now has two starts behind it, with the second coming with
Horford held out (rest on ESPN's feed) and Santos at the other forward. Porziņģis did not play
either game and Butler is out until at least January. That is the minutes case. The rates case
is two games old.

**Where both planes have him today** (committed, unchanged this pull):

| plane | line | rank | price |
|---|---|---|---|
| kit | 70 GP, 28 mpg, 12.9 / 7.5 / 2.7, 1.1 stl, 0.9 blk, 0.9 3PM, .520 / .740, 1.5 to | **81** (z_adj −0.31) | — |
| deck | same line (twinned 9/30) | **82** of 323 draftable (adj value −0.806) | Yahoo ADP 115.7 (10/6 paste); 10/6 consensus 114; RotoBaller 98; Hashtag 121; Rotoworld 9-cat 137 |

**His shape in the league's nine categories** (deck z on the v46 page): FG% +0.59, REB +0.54,
TO +0.75 (few turnovers), BLK +0.34, ST 0.00; against that, 3PTM −0.98, PTS −0.83, AST −0.70,
FT% −0.52. He is a four-category contributor who costs three counting categories and FT%.

**Does he fit the build?** The build to measure against is the owner's own mock-62 roster
(13 of 13 on the card, drafted 2026-10-06 on the real seating), where the deck's BUILD strip
read FG% 5 · FT% 7 · 3PTM 2 · PTS 8 · REB 5 · AST 7 · ST 10 · BLK 8 · TO 3, and the weekly
model's win rate against the field sat below a coin flip in exactly two categories: BLK (.47)
and AST (.49). Lendeborg's positives land on the build's soft side (BLK) and on three
strengths it keeps (FG%, REB, TO); his negatives land on 3PTM, the build's second-best
category and the one it can most afford to tax, and on PTS/AST/FT%, which are already soft.
That is the pattern of a complementary big, not a star.

The card already made this judgment, because its ΔECW term is build-aware (marginal weekly
categories won against the room, given the roster as drafted):

| room | owner turn | card | taken? | survival to the next turn |
|---|---|---|---|---|
| mock 62 (cast, real seating) | #82 | **#1**, 🎯 TARGET (blend 0.9854, a tie with Mamukelashvili broken on ΔECW 0.9369 vs 0.9368; Turner #3) | yes | 0.796 |
| mock 61 (Yahoo public room) | #106 | **#1**, 🎯 TARGET | no — Murray-Boyles | 0.557 |
| mock 61 | #111 | **#1**, 🎯 TARGET, TOSS-UP chip | no — Davion Mitchell | 0.344 |
| mock 61 | #130 | #2 (Washington #1) | gone at #133 to seat 12 | — |

Hindsight on the mock-62 pick (every legal alternative at #82 re-scored on the final rosters,
`m62_hindsight.json`): Lendeborg ranks **4th of 234** legal picks at that turn; the three
above him are Myles Turner (+0.032 cats/week), Day'Ron Sharpe (+0.017) and Jabari Smith Jr.
(+0.002) — all within the noise of one roster. In the mock-61 room the card wanted him at #106
and again at #111 and he went at #133; the debrief's cost of passing him twice sits on D61-2.

**So the system's answer is yes, on two conditions.** He fits this build, and the card will
pin him when he is the best marginal add — it did so three times in the last two rooms. The
conditions: take him when the 🎯 says so, which in a cast room was round 8 (#82) and in a
public room was round 9–10 (#106–#111, where he survived to #133); and do not reach a round
early for him, because at the committed line he is a value-rank-82 player and the market
prices him at 116, so he is usually there at the turn the card names.

**What the preseason would change, if it carries.** Research only, nothing committed — the
pool's rule is that lines move at WO-5 after two games per team, and Golden State has now
played twice while the league threshold lands about 10/9–10/10. Both planes, per-minute
scaling of the committed line (`scratchpad pull1007/lendeborg_sens.py`):

| scenario | line (pts / reb / ast / 3PM) | kit rank (z_adj) | deck rank (of 323) |
|---|---|---|---|
| S0 committed, 28 mpg | 12.9 / 7.5 / 2.7 / 0.9 | 81 (−0.31) | 82 |
| S1 30 mpg, same rates | 13.8 / 8.0 / 2.9 / 1.0 | 53 (+0.57) | 57 |
| S2 32 mpg, same rates | 14.7 / 8.6 / 3.1 / 1.0 | 39 (+1.19) | 45 |
| S3 30 mpg, 1.3 3PM | 13.8 / 8.0 / 2.9 / 1.3 | 45 (+0.86) | 50 |
| S4 32 mpg, 1.4 3PM, .530 FG | 14.7 / 8.6 / 3.1 / 1.4 | 34 (+1.73) | 37 |
| S5 24 mpg (bench), same rates | 11.1 / 6.4 / 2.3 / 0.8 | 144 (−1.97) | 141 |

Two more minutes a night is worth about 25 places on both boards; a starter's 32 minutes puts
him in the top 40 at a round-10 price. The bench case is the risk the 28-minute line already
hedges: Kerr has said only Curry and Green are entrenched starters, Horford was rested rather
than benched, and a healthy Porziņģis takes frontcourt minutes. The owner's sheet carries the
reprice as D-1007-1 (default: hold until WO-5, two games per team).

## 3. Flagged-item receipts (F1) — verdicts

| card | 10/7 finding | verdict |
|---|---|---|
| Brandon Ingram | no new item; only the 9/28 items surfaced (ESPN, Bleacher Report) | HELD −0.15 |
| Kristaps Porziņģis | DNP 10/6; ESPN's feed "undisclosed, day-to-day" with a 10/13 estimate that is the feed's, not the team's; no new statement | HELD, veto unchanged |
| Kawhi Leonard | likely sits 10/10 in Vancouver too (NBC Sports 10/3, CP24); 10/13 vs the Knicks named as a possible first appearance (SI Raptors, Yahoo) | HELD |
| Cam Thomas | unsigned; the February Bucks signing and the later Bucks waiver resurfaced, not new (AOL/ESPN, Eurohoops; Spotrac) | HELD |
| Jaden Ivey | unsigned; the "Bulls waive Ivey" item is the March waiver (NBC Sports FA list, Spotrac) | HELD |
| Jeremy Sochan | Portland's first game tips tonight vs Golden State, no lineup published (Yahoo, Blazer's Edge) | HELD, box score tonight |
| Lonzo Ball | unsigned, no dated item (Spotrac, ESPN player page) | HELD |
| Rob Dillingham | unsigned; RotoBaller dates the Charlotte waiver 9/29 where the ledger says 9/28 (ledger read directly) | HELD |
| Bennedict Mathurin | the reprice checkpoint: off the bench at OKC, 17 min, team-high 13 pts with 5 ast; the bench role the row carries (box score; NBA.com Starting 5) | HELD, WO-5 after game two |
| Ryan Rollins | Milwaukee's second game tips tonight at OKC; no new item | HELD, WO-5 after game two |

`judgment_open_items.py` on the re-authored page: 10 flagged, the same ten.

## 4. The carried items

- **Hawkins** — a Bull on a two-way contract per five outlets and the team's own release;
  ESPN's feed says Memphis. The lock holds by design (D-1005-4 re-put with the new fact).
- **Hukporti / Bona** — the tear is season-ending (NBA.com, Yahoo, PhillyVoice); Bona is the
  backup-center path once cleared; no Bona update in the window (the Sept items only).
- **Strus** — no new item; exclusion stands (D-1006-4 carried).
- **Claxton** — day-to-day on ESPN's feed; Chicago plays Phoenix tonight; no new item.
- **Tobias Harris** — the 10/5 NBA.com note stands (questionable for the opener, left calf
  strain); first game 10/8 vs Atlanta; no new item.
- **Lively** — no new item; exclusion stands.
- **Beal** — no new item; the search returned the February hip-fracture coverage (garble).
- **Knueppel** — out as announced; ESPN's feed carries a 10/21 estimate; D-1002-1 holds.
- **Coby White** — out as announced; Schröder started at the point; D-1006-2 carried.
- **Brandon Miller** — missed the opener with a leg bruise, day-to-day on ESPN's feed with a
  10/11 estimate; no team statement found [SINGLE-SOURCE: ESPN feed]; untagged (the
  White/Harris treatment).
- **Brown Jr.** — out 10/6 (ankle); Dёmin started at the point; ESPN's estimate 10/8.
- **Suggs, Black, Edey** — tonight (ORL at MEM); Edey day-to-day on the feed.
- **Duren** — no new item; the ramp to 10/20 stands.
- **Simmons, Monk, Keegan Murray, Acuff** — tomorrow (SAC at LAL), Acuff's game two.
- **Alexander-Walker, Dort, McCollum** — tomorrow (ATL at SAS).
- **Queta vs Mitchell Robinson** — tomorrow (BOS at CLE).
- **Steinbach vs Diabaté** — Diabaté started (20 min, 4 / 4 / 1, 2 stl, 2 blk, 4 to), Steinbach
  14 min off the bench (7 / 4), Kalkbrenner third [SINGLE-SOURCE: box score]; one game.
- **Vincent, Konchar** — unsigned; **Broome** — not yet on ESPN's feed.

## 5. Window sweep, box scores, team shadows, injury sweep

**Hornets 90, Nets 124.** Charlotte: Diabaté (C), Reid, Schröder, Allen and McNeeley started
(McNeeley a kit-only row, 14 pts); Allen 13 on 3-3 from three, Reid 13; O'Neale 17 min,
Steinbach 14, Kalkbrenner 15, James 17 off the bench. Out: Miller (leg bruise), Knueppel and
White (as announced), Grant Williams (hamstring, 9/25 — not a pool row). Brooklyn: Randle (18
min, 13 / 2 / 3), Porter Jr. (16 pts, 4-6 from three), Sharpe at C (18 min, 8 / 7 / 3, 2 blk),
Ellis and Dёmin (18 min, 6 / 1 / 5) started; Clowney 19, Wagner 18, Mann 20 off the bench;
Brown Jr. out (ankle). Sources: box score; NBA.com Starting 5 (Porter Jr., Randle, McNeeley,
Reid, Allen); the lineup itself rests on the box score.

**Thunder 110, Pelicans 116 (Tulsa).** New Orleans started Herbert Jones, Williamson (16 min,
11), Murphy (19 min, 11, 2 stl), Missi (19 min, 6 / 7) and Dejounte Murray (19 min, 6 / 4 / 6);
Mathurin 17 min off the bench with the team-high 13 and 5 ast, Fears 17 min / 12, Queen 17 min
/ 10 / 9 / 3 stl, Poole 16 / 9, Bey 20 / 5, Matković 12. Mosley's first game; a comeback from
24 down (NBA.com). Oklahoma City held out Gilgeous-Alexander, Jalen Williams, Holmgren, Caruso
and Hartenstein on the back-to-back (Yahoo, Hoodline; Caruso and Wallace "rest" on the feed,
Jaylin Williams heel); Mara started at C (18 min, 12 on 5-5, 9 reb, 3 blk), McCain (16 min,
12, 4-8 from three) and Mitchell (18 min, 11 / 4) started, Stirtz 15 / 6.

**Jazz 106, Nuggets 117.** Utah started Jackson Jr. (16 min, 7), Hayes at C (14 min, 7 / 4),
George (13 min, 6 / 4 ast), Bailey (27 min, 10 / 7 / 3) and Peterson (30 min, team high, 23 on
10-18, the game high); Collier 17 off the bench. Out: Markkanen (neck soreness), Nurkić (right
foot), Filipowski (back), Sensabaugh (left hip, kit-only) — the feed's estimates all 10/12
(ESPN game feed; Deseret, Yahoo, KSL, Salt Lake Tribune on Peterson and Markkanen). Denver
started Gordon (15 min, 18 / 5), Cam Johnson (15 min, 10), Jokić (16 min, 6 / 4 / 5), Jamal
Murray (16 min, 4 / 2 / 3 — his first game after missing the opener for personal reasons) and
Braun; Strawther 18 min / 15 with three threes, Bagley 15 / 10 / 5, DeRozan 11 / 7, Whitmore
(kit-only) 14.

**Warriors 124, Lakers 98.** Golden State started Green (15 min, 3 / 2 / 8), Santos (21 min,
7), Lendeborg (§2), Curry (14 min, 16 / 5, 3-6 from three) and Podziemski (19 min, 16);
Melton 18 min / 9, Payton 16, Brandon Williams 18 / 10 (5 to), Richard 15 off the bench.
Horford rested; Porziņģis, Moody and Butler did not play. Los Angeles started Mamukelashvili
at C (18 min, 15, 3-4 from three), LaRavia (22 min, 9 / 3, 3 stl), Thiero, Grimes (23 min, 12)
and Bronny James at the point (21 min, 4 / 1 / 5); Knecht 22 / 11, Vanderbilt 16 (3 stl),
Hardy 19 / 13 (5 to) off the bench. Redick ruled out Dončić, Thybulle, Ziaire Williams,
Reaves, Sexton and Kessler (Yardbarker, SI Warriors; the feed: Dončić "undisclosed", Reaves
ankle, Kessler finger, Sexton lower body, Williams rest); one outlet says Dončić left the 10/5
opener holding his right hamstring and sat as a precaution [SINGLE-SOURCE: Yardbarker].

**Tonight (10/7):** IND at MIN, MEM vs ORL, OKC vs MIL (Rollins; the Thunder regulars'
return), CHI at PHX (Claxton), POR vs GSW (Sochan; Morant and Lillard; Lendeborg's third
game). **Tomorrow (10/8):** CLE vs BOS (Queta), MIA at NOP, BKN at PHI, NYK at WAS, SAS vs ATL
(Harris; Dort, McCollum), LAL vs SAC (Acuff's game two; Simmons, Monk, Keegan Murray;
Dončić, Reaves, Kessler, Sexton).

**Team shadows (7):** CHI — the Hawkins two-way and Stevens waiver; GSW, LAC, MIL, NOP, POR,
TOR — nothing beyond the items above. **Injury sweep, both directions:** no tagged row cleared
in the window (Jackson Jr. and Herro played again under their tags; Kessler, Keegan Murray,
Simmons, Edey, Beal still waiting); no returning-but-untagged name surfaced (Jamal Murray
played and is untagged by design; Miller's bruise is day-to-day, untagged). The 46-row tag
inventory (12 excluded, 34 risk) is unchanged.

**Garbles caught (search summaries, logged, not used):** a 2013 Pelicans–Thunder Tulsa game
(Brian Roberts, Anthony Davis); a 2015 Jazz–Nuggets preseason finale (Trey Burke, Gobert);
the 2025 Warriors–Lakers opener (Horford's debut); "the Bulls beat Cleveland 118–117 on
October 7" (the 2025-26 season page; Chicago plays Phoenix tonight); "Brandon Miller 25 points
vs the Nets on opening night" (2025); Lendeborg "19 points on 6-of-6" (the July California
Classic, not the 10/6 game); "Porter started at point guard in preseason" for Rollins (the
2025-26 preseason); the February Bucks signing and waiver for Cam Thomas; the March Bulls
waiver for Ivey; Beal's February hip fracture; the Cavaliers-era Strus items; an older Duren
"day-to-day, ankle" item; a Kawhi "preseason assist percentage 22.7" line with no year.

## 6. Board effects (computed, never eyeballed)

- **Kit:** `rank_engine.py` re-run, 200 of 325 projected; the diff against the pre-pull
  snapshot is the generation-date line only (2 lines of 206 differ, both the `*Generated …*`
  stamp). No rank moved. Lendeborg 81.
- **Deck:** the draftable ordering recomputed from `data/players.csv` after the edits and
  diffed against this morning's snapshot (`scratchpad pull1007/deck_board_diff.json`): 323
  draftable before and after, 0 entries, 0 exits, 0 moves of three or more places, 0 value
  changes. Notes do not move value; nothing else changed.

## 7. Deck build and publish

- `data/players.csv`: 89 notes written (2 rows rewritten — Filipowski and Bona, whose notes
  ended in a bracketed label that the `; ` join would have turned into the build's `];`
  anchor (D-1006-3), so the label is parenthesized; 87 appended); no tag, team or line change.
  Every bracketed label written today sits ahead of its source parenthetical so no note ends
  in `]` (the script asserts it; Cardwell's 10/6 note is the one remaining row that does).
- `scripts/verify_rosters.py --allow-unmatched`: direct-complete, all 30 rosters, 334/335
  matched, 0 mismatches, Broome the one unmatched (exempted in the stamp note).
- `hoops.py freshness --stamp`: 2026-10-07; the first stamp said `--no-pool-changes` and the
  build refused (the notes change the pool hash), re-stamped with the change described.
- `JUDGMENT` re-dated 2026-10-07 with the ten receipts; colophon Data paragraph rewritten;
  gate 6 refused once on `334/335` (it wants the N/N form with the exemption named) — fixed.
- `build_deck.py`: planes 315 shared · kit-only 10 · deck-only 20 · team 0 · exclusion 0 ·
  drift 0 · propagation 0 (no waiver needed today); 171 line differences by design; market
  `yahoo-2026-10-06.csv`, 246/335 priced, 1 day old; built 335 players, pull 2026-10-07,
  injection round-trip OK, "safe to publish".
- `check_parity.py`: PARITY: EXACT MATCH (323 market ranks compared, 241 priced). `test_card.py` 89/89, `test_draft.py`
  65/65, `test_gates.py` 37/37. `full_dom_check.mjs` on `draft_state_54.json`: 130 assertions, 0 failed, 0 page
  errors, pass true (`arena/results/full_dom_check_2026-10-07_v47.json`, committed).
- Published to the standing artifact URL as **Version 47** (version id 1791385324-3067); the page header reads
  pull 2026-10-07.

## 8. Gates (2026-10-07)

| gate | result |
|---|---|
| `report/check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-10-06; exit 0 |
| `report/rank_engine.py` | exit 0; 200 of 325; board unchanged (date line only) |
| `scripts/verify_rosters.py --allow-unmatched` (deck) | direct-complete, all 30 rosters, 334/335, 0 mismatches, Broome exempted; exit 0 |
| `hoops.py freshness --stamp` (deck) | 2026-10-07, pool change described (notes only), rosters verified direct-complete |
| `scripts/build_deck.py` (deck) | gates 1–7 + F8 pass; planes 315 shared · team 0 · exclusion 0 · drift 0 · propagation 0; round-trip OK; "safe to publish" (two refusals first: a `--no-pool-changes` stamp, then the colophon count wording) |
| `scripts/check_parity.py` (deck) | PARITY: EXACT MATCH; exit 0 |
| `scripts/test_card.py` / `test_draft.py` / `test_gates.py` (deck) | 89 / 65 / 37 cases passed; exit 0 each |
| `arena/mocks/full_dom_check.mjs` (deck) | 130 assertions, 0 failed, 0 page errors, pass true; exit 0 |
| `report/check_report.py` | PASS — structure, publication rule, pull-log row; exit 0 |
| `report/check_derived.py` | PASS — all 16 dated artifacts reproduce byte-for-byte; exit 0 |
| `scripts/judgment_open_items.py --check-report` (deck plane) | PASS — all 10 flagged names carry a receipts row; exit 0 |
| artifact publish | Version 47, id 1791385324-3067, the standing URL |

## 9. Watchlist / open items

- **Tonight's five games** — POR–GSW (Sochan's first game; Morant and Lillard; Lendeborg's
  third start or not), OKC–MIL (Rollins vs Porter; the Thunder regulars back), MEM–ORL
  (Suggs, Black, Edey), CHI–PHX (Claxton; Hawkins on a two-way), IND–MIN. 10/8: SAC at LAL
  (Acuff's game two, D-1006-1's checkpoint; Simmons, Monk, Keegan Murray; the Lakers' four),
  ATL at SAS (Harris; Dort, McCollum), BOS at CLE (Queta).
- **WO-5, the projection refresh** — starts when every team has played twice; after tonight
  eleven teams have two games; the threshold still lands about 10/9–10/10. Lendeborg's line
  is the first named candidate (D-1007-1); Mathurin, Diabaté/Steinbach, Rollins/Porter and
  Jerome/Pippen Jr. are the role battles with one game each.
- **Hawkins** — moves to CHI the pull ESPN's feed reflects the two-way (D-1005-4).
- **Broome** — the by-name exemption ends when ESPN's Milwaukee feed lists him.
- **Porziņģis** — the feed's 10/13 estimate is not a team statement; re-check daily.
- **Brandon Miller** — leg bruise, untagged; re-check against the 10/9 Bucks game.
- **Kawhi** — re-check after 10/10; 10/13 vs the Knicks the next named date.
- **Strus, Lively** — exclusions stand; re-entry on two outlets reporting a cleared return.
- **Claxton, Tobias Harris** — re-evaluation about 10/19 and after 10/16.
- **Knueppel** — D-1002-1 stands; the trigger is a ruling-out for the 10/21 opener.
- **The build regex trap** — D-1006-3; today's notes routed around it by placing labels
  before their parentheticals; Cardwell's note still ends in `]`.
- **Market** — the Yahoo paste is one day old; the next is the owner's input.
- **Owner decisions carried:** D-BV1 (Butler), D-30-3, D58-2..D58-5, D-R1..D-R4, D-G2,
  D-G4..D-G7, D-P1..D-P4, D-1001-1/3, D-ADP-1/2, D40-1/3, D-LS-1/3, D-1002-1, D-1002-3,
  D60-1..D60-4, D61-1..D61-4, D62-1..D62-3, D-1005-1, D-1005-3, D-1005-4, D-1006-1..D-1006-4,
  D-Y1..D-Y4, D-RW-1..D-RW-4.

## Open-item receipts

| player | query run | dated finding |
|---|---|---|
| Brandon Ingram | Brandon Ingram Clippers Achilles update October 7 2026 | no new item; the 9/28 partial-tear coverage only — ESPN, Bleacher Report, TSN; HELD |
| Kristaps Porzingis | Kristaps Porzingis Warriors status update October 7 2026 · Porzingis Horford Warriors did not play Lakers preseason October 6 2026 · ESPN game feed 10/6 (fetched) | DNP 10/6; the feed says undisclosed, day-to-day, 10/13 estimate; no new team statement — box score, ESPN feed; NBC Sports, Bleacher Report (9/28 items); HELD |
| Kawhi Leonard | Kawhi Leonard Raptors preseason status October 7 2026 · Kawhi Leonard Raptors update October 6 2026 OR October 7 2026 · Toronto Raptors news October 7 2026 | likely sits the 10/10 Vancouver game too; 10/13 vs the Knicks a possible first appearance — NBC Sports 10/3, CP24, SI Raptors, Yahoo, Raptors Republic; HELD |
| Cam Thomas | Cam Thomas OR Jaden Ivey free agent signs October 7 2026 | unsigned; the February Bucks signing and the Bucks waiver resurfaced (garble logged) — AOL/ESPN, Eurohoops, Spotrac |
| Jaden Ivey | (same query) | unsigned; the March Bulls waiver resurfaced (garble logged) — NBC Sports FA list, Spotrac |
| Jeremy Sochan | Jeremy Sochan Trail Blazers Warriors preseason October 7 2026 Morant Lillard starting lineup · Portland Trail Blazers news October 7 2026 | first game tonight vs Golden State, no lineup published — Yahoo, Blazer's Edge, KATU; HELD |
| Lonzo Ball | Lonzo Ball OR Rob Dillingham free agent signs workout October 7 2026 | unsigned, no dated item — Spotrac, ESPN player page |
| Rob Dillingham | (same query) · basketball-reference.com NBA_2027_transactions (fetched) | unsigned; RotoBaller dates the waiver 9/29, the ledger 9/28 — RotoBaller, Saturday Down South, ledger |
| Bennedict Mathurin | Pelicans Thunder preseason October 6 2026 recap … · Pelicans Thunder Tulsa preseason October 6 2026 recap Fears Queen Mathurin Zion Mosley · ESPN box score 10/6 (fetched) · nba.com Starting 5 10/7 (fetched) | off the bench, 17 min, team-high 13 pts, 5 ast; starters Jones, Williamson, Murphy, Missi, Murray — box score, NBA.com, Yahoo, Hoodline; HELD, one game |
| Ryan Rollins | Ryan Rollins Bucks Thunder preseason October 7 2026 starting point guard Porter · Milwaukee Bucks news October 7 2026 | second game tonight at OKC; the "Porter started" summary is the 2025-26 preseason (garble logged) — ESPN schedule, Brew Hoop; HELD |
| Jordan Hawkins | Jordan Hawkins Bulls two-way contract October 6 2026 · Jordan Hawkins Bulls two-way contract signed · nba.com release (fetched) · ESPN MEM + CHI rosters (fetched, direct) | two-way with Chicago 10/6, Stevens waived; cleared waivers 10/5 — NBA.com, ESPN/Shams, Yahoo, Hoops Rumors, Heavy; feed still MEM; held (D-1005-4) |
| Ariel Hukporti / Adem Bona | Ariel Hukporti Achilles tear 76ers October 6 2026 · Adem Bona 76ers foot update October 7 2026 · nba.com news index (fetched) | Hukporti: right Achilles tear, season-ending — NBA.com 10/6, Yahoo, PhillyVoice; Bona: no new item (Sept items) |
| Nic Claxton | Nic Claxton Bulls hamstring update October 7 2026 · ESPN CHI roster (fetched, direct) | day-to-day on the feed; no new item; CHI plays PHX 10/7 |
| Tobias Harris | Tobias Harris Spurs calf strain update October 7 2026 · nba.com news index (fetched) | no new item; the 10/5 NBA.com note stands (questionable for the opener) |
| Dereck Lively II | Dereck Lively Mavericks update October 7 2026 | no new item; not cleared, status undetermined — TSN, Fadeaway World (older); exclusion stands |
| Bradley Beal | Bradley Beal Clippers knee update October 7 2026 | no new item; the February hip coverage resurfaced (garble logged) — 213hoops, SI Clippers |
| Kon Knueppel | Kon Knueppel hamstring update October 7 2026 Hornets · ESPN game feed 10/6 (fetched) | out as announced, re-evaluated the first week of the season; the feed's estimate 10/21 — TSN, NBC Sports, WSOC; D-1002-1 holds |
| Mikel Brown Jr. | Mikel Brown Jr. Nets ankle preseason October 7 2026 · ESPN game feed 10/6 (fetched) | out 10/6, ankle, the feed's estimate 10/8; non-contact work 9/30 — NBC Sports; Dёmin started |
| Jalen Suggs / Anthony Black / Zach Edey | Magic Grizzlies preseason October 7 2026 Suggs Black Edey status · ESPN MEM roster (fetched, direct) | game tonight; Edey day-to-day on the feed; Suggs "trending in the right direction" (CBS, undated) |
| Jalen Duren | Jalen Duren Pistons return timeline update October 7 2026 | no new item; an older "day-to-day, ankle" item resurfaced (garble logged) — RotoBaller, Field Level Media (contract items) |
| Ben Simmons / Malik Monk / Keegan Murray / Darius Acuff Jr. | Kings Lakers preseason October 8 2026 Simmons Monk Keegan Murray Acuff status | nothing new before tomorrow's game — ESPN injuries page, SI Kings |
| Nickeil Alexander-Walker / Luguentz Dort / CJ McCollum | Hawks Spurs preseason October 8 2026 Dort McCollum Alexander-Walker status | nothing new before tomorrow's game — SI Hawks, NBA.com |
| Neemias Queta / Mitchell Robinson | Celtics Cavaliers preseason October 8 2026 Queta Mitchell Robinson starting center | nothing new before tomorrow's game — Boston 25, NBC Boston |
| Gabe Vincent / John Konchar / Johni Broome | Gabe Vincent OR John Konchar OR Johni Broome signs OR update October 7 2026 · ESPN MIL roster (fetched, direct) | Vincent and Konchar unsigned; Broome not on the feed — Spotrac, RealGM offseason page, salaryswish |
| Max Strus | Max Strus Clippers foot update October 7 2026 | no new item; Cavaliers-era items resurfaced (garble logged) — exclusion stands |
| Hannes Steinbach / Moussa Diabaté / Brandon Miller | Hornets Nets preseason October 6 2026 recap … · Hornets Nets preseason opener October 6 2026 recap Steinbach Diabate … · Brandon Miller Hornets out preseason opener Nets October 6 2026 reason · Brandon Miller Grant Williams Hornets inactive … · ESPN box score + game feed 10/6 (fetched) · nba.com Starting 5 10/7 (fetched) | Diabaté started, Steinbach 14 min off the bench [SINGLE-SOURCE: box score]; Miller out, leg bruise [SINGLE-SOURCE: ESPN feed]; Grant Williams hamstring (9/25, WSOC) — NBA.com on the Nets' lines |
| Lauri Markkanen / Jusuf Nurkić / Kyle Filipowski / Darryn Peterson / Jamal Murray | Jazz Nuggets preseason October 6 2026 recap … (twice) · ESPN box score + game feed 10/6 (fetched) · nba.com Starting 5 10/7 (fetched) | Markkanen neck soreness, Nurkić right foot, Filipowski back, all out; Peterson 23 in 30 min; Murray started — box score, ESPN feed, Deseret, Yahoo, KSL, Salt Lake Tribune, NBA.com |
| Yaxel Lendeborg | Yaxel Lendeborg Warriors starter Kerr role minutes preseason October 2026 · Warriors Lakers preseason October 6 2026 recap … (twice) · Lendeborg 17 points 9 rebounds … · ESPN box score 10/6 (fetched) · nba.com Starting 5 10/7 (fetched) | §2 — started, 21 min, 17 / 9 on 7-11; Kerr's role quotes — box score, NBA.com, NBC Sports Bay Area (headline), Yahoo, SI, Heavy, Blue Man Hoop, VAVEL |
| Luka Dončić / Austin Reaves / Walker Kessler / Collin Sexton | Lakers Doncic Reaves Kessler Sexton out Warriors preseason October 6 2026 reason · Lakers at Warriors preseason October 6 2026 Doncic Reaves Kessler Sexton sit out Redick · ESPN game feed 10/6 (fetched) | all four out, with Thybulle and Ziaire Williams; Dončić's hamstring detail [SINGLE-SOURCE: Yardbarker] — Yardbarker, SI Warriors, ESPN feed |
| Shai Gilgeous-Alexander / Jalen Williams / Chet Holmgren / Isaiah Hartenstein / Alex Caruso | Thunder Pelicans preseason October 6 2026 Gilgeous-Alexander Holmgren Williams rest Mara start · Thunder Pelicans Tulsa October 6 2026 Stirtz Mara … · ESPN game feed 10/6 (fetched) | held out on the back-to-back — Yahoo, Hoodline, SI Thunder, Daily Thunder; Caruso and Wallace "rest" on the feed |
| (window ledger) | NBA transactions October 7 2026 signed waived traded · basketball-reference.com NBA_2027_transactions (fetched, 114 entries parsed) · nba.com/news (fetched) | 10/5 Exhibit 10 moves (Magic, Wizards, Jazz, Raptors, Bulls); 10/6 Broome signed MIL, Hawkins two-way CHI, Stevens waived — ledger, Hoops Rumors, NBA.com; zero trades since 9/27 |
| (injury sweep) | NBA injury news October 7 2026 preseason · NBA injury report news October 6 2026 preseason RotoWire CBS · NBA "cleared" OR "full participant" OR "returns to practice" October 7 2026 | Hukporti season-ending; White; Porziņģis; the Lakers' four; Jamal Murray's opener absence (personal) — Yahoo, NBA.com, Yardbarker; the "cleared" query returned 2020–2024 items only |
| (preseason) | ESPN scoreboard 10/6, 10/7, 10/8 (fetched, direct) · four ESPN summaries (fetched) | four games in the window, five tonight, six tomorrow; box scores in §5 |
| (team watch, 7) | "<Team> news October 7 2026" one each: CHI, GSW, LAC, MIL, NOP, POR, TOR | §5 |

## Bounds

- Direct-complete roster verification proves membership, not role; the one exempted row rests
  on three outlets and the team's own release for a 10/6 signing the feed has not caught up to.
- A preseason box score is a dated primary record, not a reprice mechanism (A1); the lines
  move at the WO-5 refresh after two games per team. The Lendeborg sensitivity in §2 is a
  what-if computed in scratch, not a change; its per-minute scaling holds rates fixed, which
  is a convention, not a projection of his rates.
- The "fit" read in §2 is against the mock-62 roster, one draft of one noise draw; a different
  room produces a different build, and the card re-judges the fit at every turn.
- The Hawkins hold follows the feed by design; five outlets and the team's release now say
  Chicago. Overriding needs the by-name mismatch exemption (D-1005-4).
- Starting lineups and bench minutes for Charlotte, Brooklyn, Utah, Denver, Los Angeles and
  Golden State rest on the box score alone where no outlet named the lineup; every such row
  carries the `[SINGLE-SOURCE: box score]` label in the pool.
- The kit and deck boards did not move; no line changed.
- NBC Sports Bay Area, Deseret, the Gazette, the Hornets Substack, Yahoo, SI.com, Hoops Rumors
  and most sports domains are egress-blocked; their items rest on dated search summaries, as on
  every prior pull; thirteen summary garbles were caught (§5). NBA.com's pages and ESPN's API
  endpoints answer.
- The build's PLAYERS regex trap (D-1006-3) was routed around in data again, not fixed in code.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-1007-1 | Lendeborg's line: two preseason starts (19 and 21 minutes per the ESPN box scores, Horford rested in the second per ESPN's feed), Kerr's "clearly going to play a ton" (Yahoo, SI Warriors, Heavy), a value-rank-82 line priced at Yahoo's ADP 116. (a) Hold 28 minutes until WO-5 after two games per team, the pool's own rule; (b) reprice minutes now to 30 (kit 81 → 53, deck 82 → 57); (c) reprice to a starter's 32 (kit 39, deck 45). Either reprice moves both planes in one script with the diff in the next report; rates stay until a two-outlet role claim moves them | (a) hold until WO-5 |
| D-1005-4 | Hawkins: now a Bull on a two-way per NBA.com's release, ESPN/Shams, Yahoo, Hoops Rumors and Heavy; ESPN's feed still says Memphis. Keep the lock (move when the feed catches up) or override with a by-name mismatch exemption in `verify_rosters.py`, a small code change? Deck rank 252, outside any 156-pick room either way | keep the lock |
| D-1006-1 | Acuff Jr.: game two is tomorrow; carried | (a) hold until game two |
| D-1006-2 / D-1006-3 / D-1006-4 | Coby White tag; the build regex patch; Strus exclusion | carried: hold untagged / patch before WO-7 in a separate PR / keep the exclusion |
| D-1005-1 / D-1005-3 | Harris, Claxton tags | carried: hold until ruled out of the opener / the 10/19 re-evaluation |
| D-1002-1 | Knueppel's tag | carried: hold until ruled out of the opener |
| D-1002-3 | camp first-unit signals, now two games for Lendeborg and one each for Jackson over Lopez, Rollins, Jerome over Pippen Jr., Reed with Duren out, Diabaté over Steinbach, Mathurin off the bench | carried: hold for WO-5 after two games per team |
| D60-1..D60-4, D61-1..D61-4, D62-1..D62-3 | the port's tie-break, Murray-Boyles, the advice-line wording, closing D-G3; the Lillard conviction, the Lendeborg passes, the port tie-break, the advisor's lean; the real-seating baseline, the chips vs the cast, the advice line after four firings | carried, owner silent |

## Provenance and bounds

- Inputs: ESPN's scoreboard (10/6–10/8) and four summary feeds (fetched 2026-10-07), ESPN's
  roster API for all 30 teams (fetched by the verifier) and four rosters by hand;
  Basketball-Reference's 2026-27 transactions page (fetched 2026-10-07, 114 entries); NBA.com's
  news index, its 10/7 Starting 5 and its Hawkins release (fetched); 54 dated web-search
  summaries (2026-10-03 → 2026-10-07); the owner's request; the committed 10/06 pools and boards
  as the pre-pull snapshots; `arena/results/m62_*` and `m61_*` for §2's card history.
- Every number in §2's tables and §6 is a script run (`scratchpad pull1007/`), every gate line
  is the command's own output.
- Not verified: the NBC Sports Bay Area, Deseret, Gazette and Hornets Substack articles
  (egress-blocked; headlines and search summaries only); nothing here rests on a direct read
  of a blocked sports domain.

## In plain language

**What this pull did.** One day since Tuesday's pull, and four more preseason games in it.
Before any news search I read all four box scores straight from ESPN's feed, including the
feed's own injury notes for each game, then swept the news, checked every player's team
against ESPN's live rosters for all 30 clubs, and rebuilt and republished the deck.

**Your Lendeborg question, short version.** He fits, and the system already knows it. Last
night he started again for Golden State with Horford rested and had his best game yet: 17
points on 7-of-11 with 9 rebounds in 21 minutes. The card had him as the number-one pick at
your turn in both of the last two mock rooms: you took him at pick 82 in Tuesday's cast
room, and in the Yahoo room it wanted him at 106 and 111 before he went at 133. Re-scoring
that pick 82 against every other player available, he was the fourth-best of 234 options,
within three hundredths of a category per week of the best. His strengths are field-goal
percentage, rebounds, blocks and low turnovers, which is exactly the side of your build that
was soft on Tuesday; his weaknesses are threes, points, assists and free throws, and threes
are the category your build can most afford to give.

**The one caution.** He is a round-eight to round-ten player at today's line, and the market
prices him at pick 116. Take him when the card names him; do not reach two rounds early for
him. If the preseason minutes carry into the season, the line moves at the projection refresh
later this week and he becomes a much better value: two more minutes a night is worth about
25 places on both boards, and a true starter's 32 minutes puts him in the top 40. That reprice
is on your sheet as D-1007-1 if you want it now; the default is to wait for the refresh.

**What else the games said.** Mathurin came off the bench for New Orleans and led the team in
scoring, which is the role his line already assumes. Diabaté started at center for Charlotte
over the rookie Steinbach. Darryn Peterson scored 23 in 30 minutes for Utah with Markkanen,
Nurkić and Filipowski out. Jamal Murray played for Denver after missing the opener. Oklahoma
City rested its regulars on a back-to-back; the Lakers sat Dončić, Reaves, Kessler and Sexton
again. Brandon Miller missed Charlotte's opener with a leg bruise.

**What changed in the data.** Nothing on either board: no line, no tag, no team. Jordan
Hawkins signed a two-way contract with Chicago, but the deck follows ESPN's roster feed and
the feed still lists him in Memphis, so his row waits one more day. Hukporti's Achilles tear
is season-ending; he is not in the pool, but it clears the path for Adem Bona as
Philadelphia's backup center once Bona is cleared.

**What broke and what I did.** The build refused twice, both my own doing. The first stamp
said the pool had no changes, but the notes change the file, so I re-stamped with the change
described. The second was the colophon count wording the gate wants a certain way. The
bracket trap from Tuesday did not bite: my script now checks every note before writing and
puts labels ahead of their sources.

**What I caught.** Thirteen stale or wrong items in the search summaries, including a 2013
Pelicans game, a 2015 Jazz game, last year's Warriors opener, and a summer-league line
presented as Lendeborg's Tuesday game.

**Verification.** The rebuilt deck passed every gate: the page and the Python agree exactly, all 191 test cases
pass, the browser robot drafted a full room with 130 checks and zero failures, and Version 47 is live at the usual
link.

**Your decisions.** D-1007-1 Lendeborg reprice (default: hold until the refresh). D-1005-4
Hawkins (default: keep the lock). Acuff, Coby White, the regex patch, Strus, Harris, Claxton,
Knueppel and the camp-signal question are carried.

**Next.** Five games tonight, six tomorrow including Acuff's second game and the Lakers'
regulars. The projection refresh starts once every team has played twice, likely 10/9 to
10/10, and Lendeborg's line is first on that list.
