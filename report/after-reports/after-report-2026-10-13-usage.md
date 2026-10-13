# After-report — why the practice lines were 2024-25-shaped despite the checks, and how far the shipped lines hold on re-shaped rosters (Maxey and Philadelphia, Holiday and Portland)

**Owner request (2026-10-13, verbatim):** "\"The old lines were mostly shaped by the 2024-25 season for the stars.\" How is this possible? After we've conducted many system integrity checks, why was data not confirmed to be based off 2025-2026 recent data? I understand you are trying to implement role and opportunity for this upcoming season. One case study: Tyrese Maxey. Last year, Embiid and Paul George were hurt majority of the season. This year, Embiid is healthy, along with additions of LeBron and Jaylen Brown. I am very hesitant to trust Maxey's projection as it very logically could go down with more mouths to feed. Again, I ask you how confident are you with the new NBA roster in real life builds this year, and the projections we have in the tool?"

**Owner follow-up (2026-10-13, mid-turn, verbatim):** "For Jrue Holiday, with the discrepancy of your rank vs Yahoo, did you consider that they have 4 point guards? Damian Lillard, Morant, Scoot Henderson and Jrue Holiday. This ties into the same scope of opportunity and real life roster build. I want to ensure your computations have real life context taken into account for this upcoming season projections as they are critical."

**Owner permission (2026-10-13, mid-turn, verbatim):** "I allow for you to utilize internet search for verification and validation."

**Method:** an assessment from records; no line, page or engine changed. (1) The July files that built the lines (deck `data/RESEARCH.md` at `dc18de2`, 2026-07-11; kit `report/projections-2026-27.csv` at `29f2276`, 2026-07-12) and every later report that checked them. (2) Maxey's and four teammates' last three seasons (Basketball-Reference totals, pinned in `report/wo5/data/`), the kit line behind the practice page (`89fe5a5^1`, the main commit before the WO-5 merge) and today's, and the three outside projections on file: Yahoo 10/13, Hashtag 10/12, RotoBaller 9/29. Rotoworld's sheet and the 9/26 projected-150 carry last season's actuals, not projections, so only their ranks are used. (3) A team usage budget for all 30 teams (`usage-2026-10-13/team_budget.py`). For each team it sums the shipped lines weighted by projected games (line × GP ÷ 82). It compares that claim of shots and possessions used (shots + 0.44 × free-throw attempts + turnovers) with the team's own 2025-26 per-game totals and the league range. The pool omits deep benches, so each team's sum is a lower bound. Known-answer check first: every team's 2025-26 minutes come to 240.3–243.1 a game. (4) For the follow-up, Portland's four guards and its two incumbent forwards from the same sources (`usage-2026-10-13/por_lines.py`). (5) One board-wide test that needs no team total: the deck's own range check (`scripts/range_check.py` at `f6fb476`, owner rule D-RN-3) re-run with no file for its last-season reference, so every top-150 line is set against the three outside projections only; `context_check.py` then lists the lines whose points sit above all three, with each line's team, budget status and live-page ranks. (6) For the real-life context of the two named cases, the preseason box scores already on file (ESPN, pinned by WO-5 in `report/wo5/data/preseason_roles_2026-10-12.json`, and the 10/12 Portland game in the 10/13 morning report; printed by `usage-2026-10-13/preseason_roles.py`) and, with your permission, eight web searches for October-2026 reporting on Portland's and Philadelphia's rotations (`usage-2026-10-13/web_checks_2026-10-13.md`). The article pages could not be opened from this environment (WebFetch: host not resolved; curl through the proxy: CONNECT 403), so the web claims rest on the search tool's digests of those pages and are marked as such. Each script ran twice with byte-identical output.

**Assumptions (stated before the runs).** A1: each team's own 2025-26 per-game totals are the benchmark for what a team uses. A2: a team pool's claim is the sum of line × GP ÷ 82 over its rows, a lower bound because deep benches are missing. A3: possessions used = shots + 0.44 × free-throw attempts + turnovers. A4: where all three outside projections sit below our line, the analysts have priced a role we have not; they also regress career years, so §6's count is an upper bound on context misses. A5: §6 uses the range check's own rule (top 150 by deck value; a cell counts when it misses all three projections by more than 5% of the highest, at least 0.1), on points only; an arrival is a pool teammate of 20+ projected minutes who was on another team in 2025-26 or had no 2025-26 games, a return one who played fewer than 41 games.

Pull window: 2026-10-13 → 2026-10-13 (analysis only; no roster pull; no line changed).

**Headline.** The July lines were never built from 2025-26 statistics. The file that built them says they came "from assistant season knowledge through Jan 2026" because the stat sites were blocked, and asked for a top-50 spot-check "when access allows". That spot-check never ran as a step of its own. Every integrity check since July tested the machinery: page against Python, kit against deck, the arithmetic of each category, team placements. A wrong line computed consistently passes all of them. The first comparison with real 2025-26 seasons came on 10/08: the range check found 131 of 145 top lines with a category outside every reference. It was queued into the WO-5 pass rather than raised with you as urgent. Your Towns question on 10/12 measured the vintage (44 of 52 top-60 rows closer to 2024-25) and WO-5 ran that day. On Maxey your instinct is right, and the problem is wider. WO-5 gave every player his own 2025-26 line, including the usage he had on last season's team. Philadelphia's shipped lines now claim 100.3 shots and 127.6 possessions a game. The most any team used in 2025-26 was 93.3 shots and 117.7 possessions; Philadelphia itself used 114.2. Maxey is shipped at his career-best 28.2 points; all three outside projections have him at 24.2–26.1. Brown is shipped at his Boston peak of 28.6 against 22.6–24.0 outside. Six other teams' pools also claim more possessions than any team used last season.

**Headline, the Holiday follow-up.** No: nothing in the build accounted for Portland's four point guards. Holiday is shipped at his own 2025-26 line, 16.4 points, 6.1 assists and 13.4 shots a game. He played that season with Lillard out all year, Morant in Memphis and Henderson limited to 30 games; in his two Boston seasons he took 9 to 10 shots a game. All three outside projections have him at 12.0–12.8 points and 4.4–4.6 assists. His practice-era line, 12.5 points, sat inside that range; WO-5 moved it up, value rank 136 to 88 against a market rank of 148. WO-5 set the returning Lillard and Morant at the outside projections' minutes, 27.8 and 25.5, and left Holiday, Avdija, Camara and Henderson at exactly their 2025-26 minutes, so nothing connected the arrivals to the incumbents. The team budget passes Portland, because Lillard's 45 projected games and Sharpe's 18 leave room in the season total. The repeat-name check has flagged Holiday's line since the MG pass, and nothing has settled the flag. A board-wide test without last season as a reference finds 18 top-150 lines scoring more points than all three outside projections. Three are Portland's: Holiday, Avdija and Camara. Only 4 of the 18 sit on the teams over the league maximum, and 14 rank above their market price on the live page, so the board values them above the room's price. The real-life record on file agrees with the outside projections in both named cases: in Portland's opener on 10/07 Lillard and Morant started and Holiday came off the bench, and on 10/08 Philadelphia started Maxey, Edgecombe, Brown, LeBron and Embiid together.

## 1. Roster changes

None — analysis only; no row moved on either plane.

## 2. How the practice lines came to be 2024-25-shaped

| date | what happened | what it tested | record |
|---|---|---|---|
| 7/11 | The deck's lines were written "from assistant season knowledge through Jan 2026" and labelled 2025-26 production. Basketball-Reference, NBA.com, ESPN and Yahoo were 403-blocked; the file says "per-game lines are knowledge-based, not scraped — spot-check the top 50 when access allows". | nothing; the limit was written down | deck `data/RESEARCH.md` at `dc18de2` |
| 7/12 | The kit's projections (220 players) were authored the next day with no method note; the audit of 7/13 found their team values "sourced from memory instead of research". | nothing | kit `29f2276`; `report/baseline-2026-07.md` |
| 7/13 | The roster audit found 39 team values "sourced from memory instead of research"; the provenance gate was built for them. | team placements only, never stat lines | `report/check_provenance.py` docstring; `postmortem-2026-07-13-roster-audit.md` |
| 9/29 | Nine lines the kit held high were re-derived from fetched 2025-26 data. | 9 rows, none of the stars | `after-report-2026-09-29-rederive.md` |
| 10/01 | The work order defined WO-5: every top-150 line from the 2025-26 per-36 rate, scheduled after the preseason games. | planned, not run | `report/pre-draft-workorder-2026-10-01.md` |
| 10/07 | Basketball-Reference's 2025-26 per-game tables were downloaded, for the 2025-26 what-if. | the data to catch it was on hand | `after-report-2026-10-08-standing-checks.md` §5 |
| 10/08 | The range check set each top-150 line against Yahoo, Hashtag, RotoBaller and the player's own 2025-26 line: 131 of 145 had a cell outside all of them, leaning flattering. It went into WO-5's queue. | lines against outside projections, first time | same, §5 C |
| 10/09 | The category audit found the arithmetic exact on both planes; the actuals for 2022-23 to 2025-26 were ingested; the confidence report put the data at about 70%, "both wait on Sunday's pass". | computation; the data | `after-report-2026-10-09.md` §8; `-market.md` §3; `-confidence.md` |
| 10/12 | Your Towns question: 44 of the 52 top-60 rows were closer to their 2024-25 line than to 2025-26. WO-5 ran the same day. | the vintage itself, first time | `after-report-2026-10-12-towns-haliburton.md` §2; `-wo5.md` |

**Why the checks did not catch it (EVIDENCE for the checks, INFERENCE for the judgment).**
- Every check took the lines as given. Parity tests that the page computes what the Python computes; the planes gate tests that the kit and the deck hold the same numbers; the category audit tests the arithmetic; the roster lock tests placements. None asks which season a line came from.
- The one gate built against memory-sourced data checks team placements, because that is where the July failure was first found. The same failure in the stat lines got no gate.
- The first check that could see it (10/08) did see it, and its finding was queued for a pass planned to wait for preseason role evidence. That deferral was my judgment, and the wrong one: with 131 of 145 top lines outside every reference six days before the draft, it should have come to you as an urgent finding.

## 3. Maxey and Philadelphia's other stars

EVIDENCE: `usage-2026-10-13/phi_lines.txt` (per game).

| Maxey | GP | min | shots | points | threes | assists |
|---|---|---|---|---|---|---|
| 2023-24 actual | 70 | 37.5 | 20.3 | 25.9 | 3.0 | 6.2 |
| 2024-25 actual | 52 | 37.7 | 21.0 | 26.3 | 3.1 | 6.1 |
| 2025-26 actual | 70 | 38.0 | 21.4 | 28.3 | 3.1 | 6.6 |
| practice-era line | 70 | 36 | 20.0 | 26.0 | 3.4 | 6.0 |
| **shipped today** | 70 | 38.0 | 21.4 | **28.2** | 3.1 | 6.6 |
| Yahoo 10/13 projection | 69 | — | — | 26.1 | 3.1 | 5.8 |
| Hashtag 10/12 projection | 70 | 36.1 | 18.2 | 24.2 | 2.8 | 5.8 |
| RotoBaller 9/29 projection | — | — | — | 25.7 | 2.8 | 6.0 |

RotoWire's panel (10/09) ranks him 12th with the note "the concern is that Jaylen Brown and LeBron James arriving trims the usage, and possibly minutes". Embiid played 38 games and Paul George 37 in 2025-26 (Basketball-Reference), so your premise holds: Maxey's best season came with both mostly out.

| points per game | practice-era line | shipped today | outside projections | 2025-26 actual | value rank, practice / today |
|---|---|---|---|---|---|
| Tyrese Maxey | 26.0 | 28.2 | 24.2 – 26.1 | 28.3 (PHI) | 9 / 4 |
| Jaylen Brown | 22.0 | 28.6 | 22.6 – 24.0 | 28.7 (BOS) | 72 / 59 |
| LeBron James | 16.0 | 20.9 | 19.1 – 20.3 | 20.9 (LAL) | 62 / 60 |
| Joel Embiid | 25.0 | 25.1 | 22.2 – 24.6 | 26.9 (PHI, 38 games) | 71 / 32 |
| VJ Edgecombe | 14.5 | 16.0 | 13.1 – 15.9 | 16.0 (PHI) | 96 / 56 |

Value ranks from `live-mock-2026-10-13/val_v59.json` and `val_v63.json`.

**What happened to them.** The July lines carried a usage haircut for Philadelphia; the July baseline's own words were "Brown joins Maxey/Embiid — three mouths, one ball; mild haircut for all". WO-5 replaced every line with the player's own 2025-26 line and, by its own report, "does not model a player's usage changing with a new team" (D-WO5-5, Brown and LeBron named). The minutes-and-games pass moved minutes and games, not rates, and D-C2 put the usage adjustment after the draft. So Brown arrived with his Boston usage from a season Tatum mostly missed, LeBron with his Lakers usage, and Maxey kept the usage of a season Embiid and George mostly missed. The incumbent's side of the problem, Maxey losing shots because others arrived, was never named.

**Why the range check does not flag them (EVIDENCE: `scripts/range_check.py` docstring).** Its references include "the player's own 2025-26 line". A line equal to last season is always inside the range, however much the team changed. Brown's 28.6 against 22.6–24.0 outside passes by construction.

**Real-life context, checked 10/13.** EVIDENCE: ESPN box scores on file (`usage-2026-10-13/preseason_roles.txt`); leads: `web_checks_2026-10-13.md`.

| game | Maxey | Edgecombe | Brown | LeBron | Embiid |
|---|---|---|---|---|---|
| 10/05 vs New York | did not play, coach's decision | started, 20 min | started, 17 min | did not play, coach's decision | did not play, coach's decision |
| 10/08 vs Brooklyn | started, 19 min | started, 23 min | started, 24 min | started, 18 min | started, 24 min |
| 10/10 vs Boston | started, 18 min | started, 26 min | did not dress | did not dress | did not dress |

- The new five started together once, on 10/08; Embiid played 24 minutes that night.
- Search digests, pages not opened: PhillyVoice's media-day piece of 2026-09-28 lists the same five as the starters; RotoWire's Maxey outlook expects a slight hit to his usage from the arrivals of LeBron and Brown, a lighter playmaking load and less need for 37-plus minutes.
- Embiid's 2026 health: the search found only October 2024 items on his knee (`ATTEMPTED-FAILED`); the record on file is the 10/08 start above.

## 4. Holiday and Portland's four point guards

EVIDENCE: `usage-2026-10-13/por_lines.txt` (per game).

| Holiday | GP | min | shots | points | threes | assists | turnovers |
|---|---|---|---|---|---|---|---|
| 2023-24 actual (BOS) | 69 | 32.8 | 10.0 | 12.5 | 2.0 | 4.8 | 1.8 |
| 2024-25 actual (BOS) | 62 | 30.6 | 9.2 | 11.1 | 1.7 | 3.9 | 1.2 |
| 2025-26 actual (POR) | 53 | 29.4 | 13.4 | 16.3 | 2.6 | 6.1 | 2.8 |
| practice-era line | 62 | 28 | 10.0 | 12.5 | 1.8 | 5.5 | 1.8 |
| **shipped today** | 62 | 29.4 | 13.4 | **16.4** | 2.6 | 6.1 | 2.8 |
| Yahoo 10/13 projection | 65 | — | — | 12.0 | 1.9 | 4.4 | 1.8 |
| Hashtag 10/12 projection | 54 | 28.2 | 10.6 | 12.8 | 2.0 | 4.6 | 1.8 |
| RotoBaller 9/29 projection | — | — | — | 12.6 | 1.9 | 4.6 | 2.1 |

RotoWire's panel (10/09) ranks him 148th: "Age 36 with Ja Morant and Damian Lillard added ahead of him."

| points per game | 2025-26 | how WO-5 built the line | practice-era line | shipped today | outside projections | value / market rank, practice page | value / market rank, live page |
|---|---|---|---|---|---|---|---|
| Jrue Holiday | 16.3 (POR, 53 games) | his 2025-26 rate at his 2025-26 minutes, 29.4 | 12.5 | 16.4 | 12.0 – 12.8 | 136 / 144 | 88 / 148 |
| Damian Lillard | no games | his 2024-25 rate (MIL) at the outside minutes, 27.8 | 17.0 | 19.1 | 16.6 – 19.1 | 88 / 70 | 53 / 70 |
| Ja Morant | 19.4 (MEM, 20 games) | his 2024-25 rate (MEM) at the outside minutes, 25.5 | 23.5 | 19.7 | 16.9 – 19.5 | 65 / 88 | 139 / 88 |
| Scoot Henderson | 14.2 (POR, 30 games) | his 2025-26 rate at his 2025-26 minutes, 24.9 | 13.0 | 14.1 | 11.5 – 13.6 | 256 / 195 | 243 / 193 |
| Deni Avdija | 24.2 (POR, 66 games) | his 2025-26 rate at his 2025-26 minutes, 33.3 | 19.5 | 24.1 | 18.9 – 20.7 | 77 / 39 | 76 / 39 |
| Toumani Camara | 13.4 (POR, 82 games) | his 2025-26 rate at his 2025-26 minutes, 33.3 | 12.0 | 13.5 | 12.3 – 12.6 | 98 / 131 | 99 / 134 |

How each line was built: the per-player tables of `after-report-2026-10-12-wo5.md` and `-mg.md` ("2025-26 per-36 at 29.4 min" for Holiday; "2024-25 per-36 at 27.8 min (range rule R1 from 36.1)" for Lillard; "2024-25 per-36 at 25.5 min (range rule R1 from 30.4)" for Morant). Henderson is not in those tables; WO-5's general rule covers him ("every player who played 25 or more games last season carries his 2025-26 production rate at his 2025-26 minutes"), and his shipped minutes equal his 2025-26 minutes. Ranks from `live-mock-2026-10-13/val_v59.json` and `val_v64.json`.

**What happened.**
- WO-5 treated Portland as two groups. The returning Lillard and Morant got their last full season's rates at the outside projections' minutes, so their points sit at the top of the outside range or just above it, inside the check's tolerance: Lillard 19.1 against a top of 19.1, Morant 19.7 against 19.5. The four incumbents kept their own 2025-26 rates at exactly their 2025-26 minutes. Nothing connected the two groups: adding Lillard's 27.8 minutes and Morant's 25.5 took no minutes or shots from Holiday, Avdija, Camara or Henderson.
- Holiday's 2025-26 was his biggest role in three seasons: 13.4 shots a game against 9.2–10.0 in Boston, in a season Lillard did not play, Morant was in Memphis and Henderson played 30 games. That role is what the shipped line carries. His practice-era line, 12.5 points on 10.0 shots, sat inside the outside range; for him, the July line was closer to the outside view than today's.
- Avdija is the same case at a larger size: his 2025-26 breakout, 24.2 points and 6.7 assists, ships as 24.1 and 6.7 against 18.9–20.7 and 4.9–5.5 outside. RotoWire: "the Ja Morant and Damian Lillard additions threaten his touches." His value rank sits below his market price, 76 against 39, so the board values him below the room's price, but his line still inflates Portland. Camara is above the range by less: 13.5 points against 12.3–12.6, and 2.7 threes against 2.2–2.3.

**Why no check stopped it (EVIDENCE for the checks).**
- WO-5 does not model a player's usage changing with a new team, and it never named the other side of that: incumbents losing usage to arrivals (§3).
- The range check counts the player's own 2025-26 line as a reference. On 10/12 it flagged only Holiday's free-throw percentage (`after-report-2026-10-12-wo5.md`: "ft_pct .822 vs .838-.867"); his points and assists were inside the range by construction (the check has no shots column).
- The team budget passes Portland: 111.0 possessions against its own 117.7 (§5). Lillard's 45 projected games and Sharpe's 18 leave room in the season total. The budget sees a season total, not who has the ball on a night all four guards play.
- The repeat-name check did catch it. Since the MG pass (`after-report-2026-10-13-mg.md`) it has marked Holiday LINE QUESTIONED: all four outside ranks sit 25+ places below ours, and six of his nine categories sit outside all three projections. Its rule says "re-derive at the next projection pass (two dated outlets)", and the work order's WO-7 requires every LINE QUESTIONED name to be "settled or carried by name into the 10/14 lock". Nothing has settled it yet; D-1013-6 is where it gets settled.

**Real-life context, checked 10/13.** EVIDENCE: ESPN box scores on file (`usage-2026-10-13/preseason_roles.txt`); leads: `web_checks_2026-10-13.md`.

| game | Lillard | Morant | Holiday | Henderson |
|---|---|---|---|---|
| 10/07 vs Golden State | started, 19 min | started, 19 min | bench, 19 min | bench, 17 min |
| 10/12 vs London Lions | did not play, coach's decision | started, 14 min | started, 15 min | bench, 16 min |

- When Lillard and Morant both played, Holiday came off the bench. He started only in the exhibition Lillard sat out.
- Search digests, pages not opened: a roundtable.io headline of 2026-10-04 reads "Micah Nori admits Damian Lillard, Ja Morant starting backcourt doesn't make sense", and Nori then started them in the opener; RotoWire's outlook has Holiday "in danger of handling a lesser role" after Morant's arrival; RotoBaller (2026-08-04) reports no buyout planned, so he stays on the roster.
- The real-life record agrees with the outside projections, not with the shipped line. The role Holiday's line carries, Portland's lead guard on 13.4 shots, is not the role he has had this preseason.

## 5. The team usage budget — do the shipped lines fit a team?

EVIDENCE: `usage-2026-10-13/team_budget.txt`. Possessions used per game; the pool's claim is a lower bound because deep benches are missing.

| team | pool minutes today (practice-era) | shots today (practice-era) | 2025-26 shots | possessions today (practice-era) | 2025-26 possessions |
|---|---|---|---|---|---|
| WAS | 262 (274) | 109.8 (115.1) | 90.4 | 142.2 (148.4) | 114.8 |
| PHI | 236 (219) | 100.3 (88.7) | 90.3 | 127.6 (114.4) | 114.2 |
| MIL | 257 (263) | 95.8 (107.4) | 85.5 | 119.1 (133.5) | 108.4 |
| NOP | 233 (231) | 94.4 (96.2) | 90.5 | 122.2 (124.8) | 115.2 |
| MEM | 260 (276) | 94.5 (107.1) | 90.6 | 121.5 (136.3) | 115.3 |
| UTA | 211 (212) | 92.5 (92.0) | 91.1 | 119.7 (118.5) | 117.2 |
| MIA | 230 (237) | 93.5 (91.5) | 93.3 | 118.1 (116.8) | 117.4 |

The 2025-26 league range was 83.6–93.3 shots and 108.0–117.7 possessions used per game.

| board-wide | today | practice-era |
|---|---|---|
| teams whose pool alone exceeds the team's own 2025-26 possessions | 10 | 14 |
| teams whose pool alone exceeds the 2025-26 league maximum | 7 | 7 |
| share of league minutes the pools cover | 91.6% | 92.5% |
| share of league possessions the pools claim | 97.2% | 99.9% |

- **Philadelphia is the clearest usage case.** Its minutes fit, 236 of 240, but its shots do not: 100.3 against a league maximum of 93.3. WO-5 added about 13 possessions a game to Philadelphia; by player, Brown +5.2, Caldwell-Pope +3.3, LeBron +3.0, Edgecombe +1.8 and Maxey +1.1.
- **Washington, Milwaukee, Memphis and Charlotte have a minutes problem.** Their pools claim 252–262 minutes a game, which no team can play; the practice-era lines claimed 250–276 for the same four.
- **Board-wide, WO-5 did not make this worse.** It moved the excess: Philadelphia up, Milwaukee, Memphis, San Antonio and others down. The lines are built player by player, and no step ever checked them against a team total.
- **A pool under budget can still be wrong player by player.** Portland passes, 111.0 against its own 117.7, with three lines above every outside projection (§4, §6).

## 6. Board-wide — lines that score above every outside projection

EVIDENCE: `usage-2026-10-13/range_check_no_actual.txt` and `.json` (the deck's `scripts/range_check.py` at `f6fb476`, run with no last-season file, twice, identical) and `context_check.txt` (twice, identical).

With last season removed as a reference, 102 of the 139 checkable top-150 lines have at least one category outside all three outside projections, 214 cells in all. That is too broad to read as a context signal, since any of nine categories counts. Points alone, the category that carries opportunity, is the narrower test: 18 lines score above all three projections and 5 below. A line counts only when it misses the range by more than the check's tolerance, 5% of the highest projection, so LeBron's 20.9 against a top of 20.3 is not counted.

| player | team | 2025-26 team, games | our points | outside projections | value / market rank, live page | team budget |
|---|---|---|---|---|---|---|
| Tyrese Maxey | PHI | PHI, 70 | 28.2 | 24.2 – 26.1 | 4 / 9 | over the league max |
| Kawhi Leonard | TOR | LAC, 65 | 27.8 | 23.7 – 24.3 | 6 / 32 | under both |
| Lauri Markkanen | UTA | UTA, 42 | 26.4 | 20.2 – 23.8 | 11 / 37 | over the league max |
| James Harden | CLE | CLE and LAC, 70 | 22.9 | 18.9 – 20.8 | 17 / 33 | under both |
| Michael Porter Jr. | BKN | BKN, 52 | 24.5 | 18.7 – 21.8 | 34 / 60 | under both |
| Jalen Duren | DET | DET, 70 | 19.5 | 17.2 – 18.5 | 43 / 34 | over its own total |
| Jaylen Brown | PHI | BOS, 71 | 28.6 | 22.6 – 24.0 | 59 / 30 | over the league max |
| Keyonte George | UTA | UTA, 54 | 23.1 | 17.7 – 20.3 | 73 / 53 | over the league max |
| Deni Avdija | POR | POR, 66 | 24.1 | 18.9 – 20.7 | 76 / 39 | under both |
| Collin Gillespie | PHX | PHX, 80 | 12.7 | 9.5 – 11.9 | 79 / 183 | under both |
| Jrue Holiday | POR | POR, 53 | 16.4 | 12.0 – 12.8 | 88 / 148 | under both |
| Tre Jones | CHI | CHI, 65 | 13.7 | 11.4 – 12.3 | 89 / 184 | under both |
| Toumani Camara | POR | POR, 82 | 13.5 | 12.3 – 12.6 | 99 / 134 | under both |
| Andrew Nembhard | IND | IND, 57 | 17.1 | 13.1 – 14.7 | 101 / 152 | over its own total |
| Peyton Watson | CLE | DEN, 54 | 14.5 | 12.2 – 12.5 | 106 / 155 | under both |
| Santi Aldama | DAL | MEM, 43 | 13.9 | 10.1 – 13.2 | 124 / 228 | under both |
| Sam Merrill | CLE | CLE, 52 | 12.5 | 10.0 – 10.8 | 142 / 258 | under both |
| Naji Marshall | DAL | DAL, 74 | 15.0 | 11.4 – 14.1 | 148 / 204 | under both |

The five below all three: Cooper Flagg, Keegan Murray, Matas Buzelis, Ausar Thompson and Paolo Banchero.

- **By team:** Cleveland 3, Portland 3, Dallas 2, Philadelphia 2, Utah 2, and one each on six other teams.
- **The team budget sees few of them.** 4 of the 18 sit on teams over the league maximum and 2 on teams over their own 2025-26 total; 12 are on teams under both.
- **The board values most of them above the room's price.** On the live page 14 of the 18 rank above their market price, 12 of them by 25 or more places; the card's suggestions are computed from the same lines. Holiday is one; Kawhi, Markkanen, Gillespie and Tre Jones are others.
- **What this test cannot tell.** A line can sit above every projection because the roster changed around the player, or because he had a career year that will not repeat. I tried to separate the two with a label: did a teammate of 20+ projected minutes arrive or return? Every team in the pool has one (30 of 30 teams; 29 of 30 at 25+ minutes), so the label separates nothing. Telling them apart would take a usage model, which this report does not build. Both readings point the same way for the draft: three independent projections expect less.

## 7. How confident, by layer

Anchored to the WO-5 report's table of 10/12 (§13 there); "now" is a judgment (INFERENCE) on the records named.

| layer | 10/12 | now | basis |
|---|---|---|---|
| Engine math | 99% | 99% | parity EXACT on the 10/13 chain |
| Placements, who is on which team | 98% | 98% | 335 of 335 against ESPN's feed at the 10/13 build |
| The 18 lines above every outside projection in points | not split out | low | §6: three independent projections all expect less; 14 rank above their market price |
| The pools of the seven over-budget teams | not split out | low | §5: each claims more possessions than any team used in 2025-26; Philadelphia's five sit at or above the top of every outside projection |
| Other lines | 76% | 76% | 2025-26 rates, backtested; the WO-5 checks. A blind spot shared by all three outside sources would not show here (A4) |
| Board order | 82% | 82% outside those lines and teams | the out-of-sample test behind 82% still ran on the old ordering |

## Watchlist

- Philadelphia's five (Maxey, Brown, LeBron, Embiid, Edgecombe) and the other six over-budget teams (§5) until D-1013-6 is decided.
- Portland's Holiday, Avdija and Camara, and the other 13 lines of §6, until D-1013-6 is decided.
- Holiday's LINE QUESTIONED flag: WO-7 carries it by name into the 10/14 lock unless D-1013-6 settles it.
- Embiid's availability: his projected 45 games are what keep Philadelphia's total from being higher still.
- The 10/14 lock paste (D-1013-1) and the publish freeze (D-1013-5).

## Open-item receipts

| item | query run (2026-10-13) | dated finding |
|---|---|---|
| (this analysis) | records, plus eight web searches on Portland's and Philadelphia's rotations (2026-10-13; queries, result links and digests in `usage-2026-10-13/web_checks_2026-10-13.md`) | the real-life rows of §3 and §4 rest on ESPN box scores on file; pull receipts for the window live in `after-report-2026-10-13.md` (the morning's pull), same day |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (`after-report-2026-10-13.md`, receipts dated 10/13) | all HELD or unsigned on 2026-10-13; nothing changed since |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 a88d83f4e2f8), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 25 of 25 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-13.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 5 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 20 of 25 | 38 | 117 | 48 | 60 | 101 | 71 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Kel'el Ware | 19 of 25 | 27 | 77 | 51 | 51 | 63 | 65 | ft_pct .732 vs .714-.723 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 19 of 25 | 62 | 180 | 56 | 118 | 126 | 129 | tpm 2.8 vs 2.2-2.6 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Lauri Markkanen | 16 of 25 | 11 | 37 | 18 | 31 | 41 | 29 | pts 26.4 vs 20.2-23.8; ast 2.1 vs 1.8-1.9; fg_pct .471 vs .452-.463 | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Jrue Holiday | 14 of 25 | 88 | 148 | 161 | 129 | 128 | 145 | pts 16.4 vs 12-12.8; reb 4.6 vs 4-4.2; ast 6.1 vs 4.4-4.6; tpm 2.6 vs 1.9-2; tov 2.8 vs 1.8-2.1; ft_pct .822 vs .855-.867 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Yaxel Lendeborg | 11 of 25 | 70 | 143 | 93 | 121 | 137 | 98 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Ryan Rollins | 9 of 25 | 28 | 74 | 58 | 63 | 78 | 83 | stl 1.7 vs 1.3-1.5 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Kawhi Leonard | 6 of 25 | 6 | 32 | 15 | 16 | 15 | 20 | pts 27.8 vs 23.7-24.3; tpm 2.6 vs 2.2-2.3 | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (21 mocks, value 7, market 18); VJ Edgecombe (12 mocks, value 56, market 75); Tyrese Maxey (7 mocks, value 4, market 9); Derrick White (6 mocks, value 30, market 45).

The check as the 10/13 chain ran it on the page now live (Version 64). Holiday and Rollins are the two LINE QUESTIONED rows; Holiday's is the line your follow-up asks about (§4). The Philadelphia five are not flagged, because the check counts 🎯 repeats against the market price, not lines against a team total (§5).

## Bounds

**Out of scope by design.**
- No candidate lines: a usage-adjusted Maxey or Holiday, or a rescaled team, is what D-1013-6 would build, not this report.
- No dry run of any D-1013-6 option: what each would change on the board, the card or a graded room is measured only once you choose one.
- Web research covers the two named cases only, Portland and Philadelphia. The other 16 lines of §6 were not searched; the decision on them rests on the three outside projections either way.
- Pace: the budget compares with each team's 2025-26 totals and the league range; a few percent of pace cannot close Philadelphia's gap to the league maximum.
- The other eight categories are not tallied board-wide; points is tallied because it carries opportunity. Every line's full list of cells outside all three projections is in `range_check_no_actual.txt`.

**In scope and unverified.**
- Why the July recall came out 2024-25-shaped — `UNVERIFIABLE`: the July session's reasoning is not on file; the July file states the method and the 10/12 measurement states the result.
- Which of the 18 lines in §6 are context misses and which are career years that will not repeat — `ATTEMPTED-FAILED`: the arrival-or-return label put every team in one class (30 of 30 at 20+ minutes, 29 of 30 at 25+), so it separates nothing. The decision does not turn on it: both readings put the lines above three independent projections.
- The 11 top-150 lines without all three outside projections — `NOT-ATTEMPTED`: the range check skips them, so §6's 18 covers the 139 checkable lines only.
- Whether all three outside sources share a blind spot on some roster — `NOT-ATTEMPTED`: A4 assumes they price the rosters; a line inside their range would not show in §6.
- The web claims in §3 and §4 — `ATTEMPTED-FAILED` at the page level: WebFetch could not resolve bleacherreport.com, www.rotowire.com or www.phillyvoice.com, and curl through the proxy got CONNECT 403 for the same pages (2026-10-13). They rest on the search tool's digests and are used only beside the ESPN box scores on file, which carry the finding.
- Embiid's 2026 health — `ATTEMPTED-FAILED`: the search returned only October 2024 items.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-1013-6 | Lines before the lock. Every option but (a) sets the named lines' counting categories to the average of the three outside projections on both planes, sets the shot attempts so each line still passes the points identity check, keeps the percentages and games, runs the full chain and publishes. (a) No line change; you discount these players yourself at the card. (b) The two cases raised: Philadelphia's five and Holiday. (c) One rule for the board: the 18 lines of §6 whose points sit above all three outside projections, Maxey, Brown, Holiday, Avdija and Camara among them, plus Philadelphia's other three for the team budget. (d) (c) plus the other over-budget teams scaled to their own 2025-26 totals | (a); I recommend (c), because it applies one test to every line instead of to the names someone happened to question, and it reaches Kawhi and Markkanen, whom the live page values at 6 and 11 against market ranks of 32 and 37 |
| D-1013-7 | Two checks in the build: the team budget, so no pool claims more possessions than any team used; and the range check without last season as a reference, so a copy of last season can no longer pass by construction. Both would refuse today's build, so they go in with D-C2 | after the draft |
| D-1013-2..5, D-1013-1, D-C2, D-SF-1..4 and earlier | carried | carried |

## Provenance

- Inputs: deck `data/RESEARCH.md` at `dc18de2`; kit `report/projections-2026-27.csv` at `29f2276`, at `89fe5a5^1` and at `cd9ecd9`; `report/wo5/data/bref_totals_2004-2026.csv`; `report/market/yahoo-proj-2026-10-13.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-09-29.csv`, `rotoworld-2026-10-05.csv`, `rotowire-2026-10-09.csv`; the reports named in §2.
- Scripts and outputs in `usage-2026-10-13/`: `team_budget.py` → `team_budget.txt` (two runs identical), `phi_lines.py` → `phi_lines.txt`, `por_lines.py` → `por_lines.txt` (two runs identical), `range_check_no_actual.json` and `.txt` (the deck's `scripts/range_check.py` at `f6fb476` with `--actual` naming no file; two runs identical), `context_check.py` → `context_check.txt` (two runs identical; reads the range-check record, `team_budget.txt` and `live-mock-2026-10-13/val_v64.json`), `rn_section_v64.md` (the repeat-name section as the 10/13 chain printed it), `preseason_roles.py` → `preseason_roles.txt` (two runs identical), `web_checks_2026-10-13.md` (the eight searches), `verify_usage_literals.py` → `verify_usage_literals.txt` (every figure in the tables and the two headlines checked against the outputs above: 438 of 438, two runs identical; six planted errors each caught).
- Web: the eight searches of 2026-10-13 returned result links and the search tool's digests; no article page could be opened from this environment. Every web claim is marked as a digest and sits beside an ESPN box score on file.

## In plain language

**How the old numbers happened.** In July the stat websites were blocked, so the projections were written from memory and labelled as last season's numbers. The file even said to spot-check the top 50 once the sites opened. That check never happened on its own. All the integrity checks since then tested whether the tool calculates correctly and whether players are on the right teams. None of them asked which season a player's numbers came from. The real 2025-26 numbers arrived on 10/07 and 10/09, a check on 10/08 showed most top lines were off, and I filed it for the Sunday refresh instead of telling you it was urgent. That was my mistake.

**Maxey.** You are right. His line is his best season, played while Embiid and George were mostly out. All three outside projections have him 2 to 4 points lower. Brown is worse: we carry his Boston career year, about 5 points above every outside projection. Taken together, Philadelphia's numbers ask for more shots than any NBA team took last season, so they cannot all come true.

**Holiday and Portland.** You are right again, and it is the same mistake. Holiday's numbers are his numbers from last season, when Lillard was hurt all year, Morant was still in Memphis and Henderson played 30 games. The rebuild on 10/12 added Lillard and Morant to Portland without taking anything from the players already there. All three outside projections have Holiday about 4 points lower. The team check from this afternoon missed it, because Portland's total still fits. So I ran a second check across the whole board: 18 top players are projected for more points than all three outside projections give them. Three are Portland's. Two others are Kawhi and Markkanen, whom the tool ranks far above their draft price. I also checked the real games. In Portland's first preseason game Lillard and Morant started and Holiday came off the bench. Philadelphia started Maxey, Edgecombe, Brown, LeBron and Embiid together on 10/08. Real life matches the outside projections here, not our lines.

**How confident I am.** Very confident about who is on which team, and in the math. Reasonably confident in the numbers for players whose points sit inside the outside projections. Not confident in those 18 lines, or in the totals for Philadelphia and six other teams whose players, added up, claim more of the ball than any team uses.

**Your decisions.** D-1013-6: before the lock, move those 18 lines and Philadelphia's other three to the outside projections' average; that is my recommendation. Or fix only the two cases you raised, Philadelphia and Holiday, or change nothing and discount those players yourself. D-1013-7: after the draft, build two checks so this cannot ship again.
