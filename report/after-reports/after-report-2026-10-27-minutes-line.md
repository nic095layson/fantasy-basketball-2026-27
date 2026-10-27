# The minutes-trend candidate line — 2026-10-27

Pull window: 2026-10-27 → 2026-10-27 (no pull: the records branch's box records through 2026-10-26, its Sunday-morning pools of 10-19 and 10-25, and the never-edited preseason file; no web search, no market pull).

**Method up front.** Owner 2026-10-27: build 2 of the five chosen ("let's build"), the first that touches a forecast — as a **candidate only**: written beside the live line every morning, snapshotted each Sunday, graded each Monday by the accuracy card as a third column; nothing on the board, in the brief or in the simulator reads it. The rule, stated before any run: candidate = live line × (forecast minutes ÷ implicit minutes) on counting stats and attempts, FG%/FT% untouched; forecast minutes = the preseason mpg as a 3-game prior plus the regular-season minutes weighted 0.5^(age/5 games); implicit minutes = the preseason mpg moved at the blend's own points prior (11.7 games, read live from `season_lines`). Switch rule, pre-committed (D-ML-1): the candidate replaces nothing until its MAE beats the in-season line's on PTS, REB and AST in 3 of 4 consecutive graded weeks, on the owner's word. EVIDENCE marks what a run showed; INFERENCE what is derived.

## 1. Two corrections to the plan, found by the build (EVIDENCE)

- **One prior in both places graded the blend against itself.** The plan said a 10-game minutes prior. The red test (four 36-minute games on a 30-minute prior came out *below* 1, because recency weighting shrinks the effective sample) and a smoke run on today's records (every ratio within 0.976–1.026, no player moved 10%) showed that with the minutes prior next to the blend's 11.7-game points prior the ratio is ~1 by construction. The rule above is the fix: minutes are trusted at 3 games, stats stay at the blend's prior, and the ratio carries exactly that difference. A regression test pins the flaw (`test_one_prior_in_both_places_would_grade_the_blend_against_itself`).
- **The constants are registered `uncalibrated`, not `declared_band`.** The standing sweep turns every `declared_band` entry into an arena patch with no module filter; a band on these two would have broken it. `uncalibrated` with the decision named is the status the red-team doctrine defines for a hand-set number whose calibration is pending — here D-ML-1, the weekly grading. Registry check: 34 registered = 34 live (uncalibrated 9 → 11).

## 2. What the candidate says today (EVIDENCE, scratch run on the records branch at a7d7283, not published)

337 players, 281 with games; ratio median 1.000, mean 0.986, range 0.733–1.342; 8 players scaled up 10%+ and 29 down; 33 unscaled (no preseason mpg on file, left equal to the blend and named). Biggest moves: Khaman Maluach 1.34, Will Riley 0.73, Harrison Barnes 0.76, Simone Fontecchio 0.78, Joan Beringer 1.20, Kyle Filipowski 0.80, Terrence Shannon Jr 1.18, Nikola Vucevic 0.82. INFERENCE: the league-wide mean below 1 is the week-1 minutes shortfall the audit measured (24.7 played vs 26.3 projected), and the largest downs (Barnes, Vucevic) are names the audit listed as below projection — the signal is the one intended; whether it forecasts better is what the card will say.

## 3. What was built (EVIDENCE)

- `minutes_line.py` (new): the rule above; writes `data/season/pool_season_mt.csv`, `projections_season_mt.csv` and a dated `minutes_line_<date>.json` (ratios, forecasts, the unscaled, the biggest moves). `test_minutes_line` (8, red first; the Build test's hand numbers re-derived for the two-prior rule).
- `morning.py`: a non-fatal "minutes line" step right after season lines (`test_morning.MinutesLine`, the exact-order tests gained the step). `weekly_preview.snapshot`: copies the candidate beside the live pool as `lines_week<N>_mt.csv`, never overwriting (`test_weekly_preview.Snapshot`, 3). `accuracy_week.grade_snapshots`: the card's third column with MAE, and the switch rule printed under the table (`test_accuracy_week.Snapshots`, 2). Registry: `minutes_line.HALF_LIFE` 5.0 and `MIN_PRIOR_GAMES` 3.0; `check_constants` imports the module.
- **Back-fill (this PR, `report/accuracy/`):** week 1's snapshots from the 10-19 Sunday pool (0344518; 335 rows, equal to the preseason line on every stat column, candidate byte-identical — no games yet, as it must be) and week 2's from the 10-25 Sunday pool (d887553, blending through 10-24; candidate differs for 244 of 336 players, FG%/FT% identical). Week 1's card row, written before these existed, stays as written: the record is append-only. The first three-column grade is week 2 on 2026-11-02.
- Kit suite: every file OK; no stray writes.

## 4. Bounds

**Out of scope by design.** The live line, the board, the brief and the simulator are unchanged; the candidate's only consumers are the Sunday snapshot and the Monday card. **In scope and unverified.** Whether the candidate forecasts better — that is the point of the card, and no graded week exists yet. HALF_LIFE and MIN_PRIOR_GAMES are hand-set; if the candidate wins, a sweep over them belongs before any switch. Minutes for a player the pool lacks a preseason mpg for (33 today) are not forecast.

## 5. Next steps (owner decisions)

1. Merge this PR; the morning writes the candidate from 10-28 and Nov 2 grades week 2 three ways.
2. Build 3 (fit the two fragile constants), then 5, as ordered.

## Watchlist

- **2026-10-28 morning:** `MINUTES LINE: PASS — 2026-10-28: … ratio >= 1.10 for N, <= 0.90 for M`.
- **Sunday 2026-11-01:** `snapshot: report/accuracy/lines_week3.csv, report/accuracy/lines_week3_mt.csv`.
- **Monday 2026-11-02:** the week-2 row of `report/accuracy.md` with all three line columns.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| minutes-trend candidate line (build 2) | **BUILT**, candidate only, graded from 11-02 | §2, §3 |
| one-prior flaw | **FIXED**, regression test | §1 |
| builds 3, 5 | **OPEN**, owner-ordered next | §5 |

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck e0722cf (this change's deck commit), checked today, the same page the 10/22 day report replayed. Its table stands, carried here verbatim from the day report.

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 6a5cefea4921), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 33 of 33 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 32 of 33 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 23 of 33 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 14 of 33 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 33 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| John Collins | 11 of 33 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 10 of 33 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 10 of 33 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 9 of 33 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 7 of 33 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 7 of 33 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 33 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 33 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (17 mocks, value 27, market 45); Lauri Markkanen (15 mocks, value 21, market 37); Tyrese Haliburton (13 mocks, value 7, market 12); Tyrese Maxey (11 mocks, value 5, market 9); Kel'el Ware (10 mocks, value 57, market 77); Tyler Herro (9 mocks, value 51, market 69); Karl-Anthony Towns (8 mocks, value 12, market 15); Miles Bridges (5 mocks, value 96, market 98).
