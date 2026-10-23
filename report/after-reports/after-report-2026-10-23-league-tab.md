# The League tab: every team's categories, sortable, with an all-play power ranking — 2026-10-23

Window: the kit at `main` `046ae2f` plus this branch; the records branch `season/daily` at `8fde7a2` for the replay (the Flaim pulls of 10/21–10/23, the league state, box scores). No projection line, tag, roster, ledger row or engine constant changed; one new script, three changed scripts, the deck, and their tests.

Pull window: 2026-10-23 → 2026-10-23. No pull: the table is built from the morning pulls already on disk (Yahoo's six matchups through Flaim), the league state and the box scores.

**Owner's request (2026-10-23).** "Build 1" of the League-tab options: the League tab as P2 of the 10/22 next-level proposal (the weekly intake of all six matchups from Yahoo into the team-weeks record, scoring the prediction ledger, plus the tab with cumulative nine-category totals per team), "and please add a dynamic (and computational) Power rankings, and also sortable columns for the 9-categories."

**Method (stated to the owner before the build).** M1, sources per week: a finished week from Yahoo's block in the latest pull dated after the week ended (the finals); failing that, the box-score rebuild of each team's active slots (pinned lineups, else today's roster), labeled; the week in progress from the day's pull. Cumulative FG% and FT% are total makes over total attempts. M2, the power ranking is the all-play record: each week every team against all eleven others on the nine categories (TO reversed, a tie half); power = the cumulative all-play win rate; beside it the actual matchup record from Yahoo's category scores and the luck gap (actual rate − all-play rate); recomputed every morning. Rejected: a z-score of cumulative totals (scale-dependent, double-counts games played). M3, the Monday problem: Yahoo's finals for a finished week reach the kit only when a pull requests that past week, which the Runner prompt (the owner's) does not do yet; until it does, finished weeks come from the rebuild. A1: sorting treats turnovers as fewest-first. A2: the League tab sits after Week in the tab rail.

## 1. What changed (EVIDENCE)

- `scripts/league_table.py` (new): `week_from_yahoo()`, `allplay()`, `ranks()`, `rebuild_week()`, `build()`; writes `report/league/league_<date>.json` (per week: status, source, pull, each team's totals, opponent, Yahoo score, games remaining, the week's all-play; cumulative: totals, cats, ranks, weeks; power: rank, all-play W–L–T and rate, actual W–L–T, luck). Records a standalone run-ledger row; silent under the morning run.
- `scripts/scoreboard_intake.py`: `--from-pull <pull> --week N` reads a finished week's six matchups from the Yahoo block (halts when the pull lacks the week, the week is not finished, or a team is not in the league state); `--state`, `--weeks-dir`; the CSV path stays.
- `scripts/morning.py`: step 5c "league table" after the week matchup, non-fatal.
- `scripts/season_deck.py`: the League tab — a Power rankings card (rank, all-play rate with a bar, W–L–T, actual, luck) and the League categories table (every column sortable by a click, TO ascending, a rank badge of 12 in every category cell, my row marked, a view selector: season to date / this week only); the record is an optional input (`league`); no record draws a zero-state. `scripts/deck_render_check.py`: the seventh tab and pane.
- Tests, red first, then green: `test_league_table` (10: no module, then 10 of 10; the all-play case is hand-computed for three teams, A 7–6–5, B 6–9–3, C 9–7–2), `test_scoreboard_intake.FromPull` (4: 3 errors + 1 failure, then 9 of 9 in the file), `test_morning.Steps` (the step list; red, then green), `test_season_deck.LeagueTab` (5: 5 errors, then 14 of 14 with the render-check tests; the browser clicks TO, PTS, PTS, REB and FG% and reads the first row each time). The League table's CLI test and the deck's run with a scratch ledger; the full suite leaves `report/run-ledger.jsonl` at 763 lines once `test_league_live` carries PR #183's scratch ledger (on this branch, which predates #183, the suite still appends its `league_live` rows; the rows were discarded, not committed).

## 2. The replay on the 10/23 records (EVIDENCE, `league-tab-2026-10-23/`)

Week 1 in progress from `pull_2026-10-23.json`, all 12 teams. My week-1 totals equal the Today board's (the week card's Yahoo column), and my all-play record recomputed by hand from the record's totals is 45–50–4, as the script says. The power table:

| # | team | manager | all-play W–L–T | rate | actual W–L–T | luck |
|---|---|---|---|---|---|---|
| 1 | Booker T Floppers | Robby | 77–19–3 | 0.793 | 6–3–0 | -0.126 |
| 2 | MAXEY-MUM OVERDRIVE | Cayas | 65–31–3 | 0.672 | 6–3–0 | -0.005 |
| 3 | Splash Mountain | JCo | 59–38–2 | 0.606 | 6–2–1 | +0.116 |
| 4 | Thompson Telepathy | Hegi | 56–41–2 | 0.576 | 3–6–0 | -0.242 |
| 5 | John's Cool Team | John | 51–42–6 | 0.545 | 5–2–2 | +0.121 |
| 6 | Looking Cool Joker! | Oblena | 48–48–3 | 0.500 | 6–3–0 | +0.167 |
| 7 | KEL'EL YAXEL HALQUETA | Me | 45–50–4 | 0.475 | 3–6–0 | -0.141 |
| 8 | ROOKS FTW | Noah | 44–52–3 | 0.460 | 5–4–0 | +0.096 |
| 9 | Cade n em | Martin | 42–55–2 | 0.434 | 3–6–0 | -0.101 |
| 10 | Podz save the league | Kevin | 36–60–3 | 0.379 | 2–5–2 | -0.045 |
| 11 | Lauri’s Prime Rib | Will | 35–61–3 | 0.369 | 4–5–0 | +0.076 |
| 12 | Giavaris Jamal Javarison-Lamar | Kyle | 17–78–4 | 0.192 | 2–6–1 | +0.086 |

My category ranks of 12: FG% 1, FT% 7, 3PTM 6, PTS 6, REB 12, AST 8, ST 5, BLK 10, TO 4. Renders `league_1280.png` and `league_400.png`; page overflow 0 px at both widths (the category table scrolls inside its card on a phone).

## 3. What refreshes it, and what still needs the owner (INFERENCE from §1)

The morning run builds the record after the week card and before the deck, so the tab refreshes every morning with no prompt change. The finished-week finals need one line in the Monday Runner prompt: call Flaim's get_matchups for the previous week as well as the current one; the pull then carries that week's block, the table reads it as the finals, and `scoreboard_intake.py --from-pull <that pull> --week N` scores the ledger. Until then a finished week is rebuilt from box scores and labeled.

## 4. Bounds

- **Not checked:** a live morning run with this code (the next is 12:03Z); a finished week on real data (none has finished; the finals path and the rebuild path are exercised on fixtures).
- **Pre-existing failures:** `test_matchup_live.Record` and `test_league_live.EndToEnd` (transcript-dependent) fail on `main` `046ae2f` too; 450 run, 2 failures, 2 skipped.
- **Out of scope by design:** standings and FAB balances (not in the pulls); per-player season accumulation as a table (the owner's earlier question; the data is in the actuals files).

**Bands.** This change computes no simulator figure; the standing sweep's bands (`redteam-2026-10-19/sweep.json`, engine 048efb6) are unchanged:
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

## Watchlist

- **The first morning run after merge:** `report/league/league_<date>.json` exists and the League tab draws from it.
- **Monday 10/26:** with the prompt line, the pull carries week 1's finals and the intake scores the week-1 prediction; without it, the table labels week 1 as rebuilt.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| the League tab, power rankings, sortable categories (Build 1) | **BUILT** on this draft PR | §1, §2 |
| Yahoo's finals for finished weeks | **OPEN**, needs the Monday prompt line (owner's) | §3 |
| `test_matchup_live` and `test_league_live` transcript dependence | **OPEN**, flagged (PR #172) | §4 |

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck 048efb6 and at 483482b, checked today, the same page the 10/22 day report replayed. Its table stands, carried here verbatim from the day report.

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
