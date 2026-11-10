# Category grades for every matchup, and the weekly adds counter (owner pick 2026-11-10, "P5 + P7")

Pull window: 2026-11-10 → 2026-11-10 (one Flaim get_league_info call at 2026-11-10 for the settings' shape, read only, not written to the records; no other pull: report/calibration_league.json, calibration_league_real.json, data/weeks/week_1..3.json, data/managers/transactions.json, data/news/league_moves_2026-11-10.json and data/source/flaim/pull_2026-11-10.json at be859ea on season/daily, read only; kit main a1c91ca, deck main 01483de).

**Method up front.** Order: the owner's card pick "P5 + P7: grade the sim, track moves". Method parameters, stated before the build: the graded forecasts are the pre-week category chances the kit already records for all six matchups (flat schedule and real games), against the week's final lines; a tie scores 0.5 and turnovers count low; no forecast is recomputed after the fact. The adds counter counts the owner's adds from the league transaction record and the day's move records, by UTC date, against Yahoo's `maxWeeklyAdds` as pinned with the pull. Tests were written first and seen failing. No projection line, injury tag, roster or engine constant changes. EVIDENCE marks what a run or a read showed.

**Verdict: the Monday intake now grades every matchup's category forecasts by category (54 a week against the owner's 9), and the week card and deck now show adds used against the league's weekly limit. The limit appears from the first morning pull after this merges; until then the card shows the count and says the limit is not on record.**

## 1. Category grades (P5)

| piece | what it does | evidence |
|---|---|---|
| `scripts/category_grade.py` (new) | For each recorded pair and category: the pre-week chance against the final line. Per category and in total: n, Brier, how often the favoured side won, and the mean chance the kit gave it. Writes `report/category_grades.json` and `.md`, rebuilt from the records on each run | tests `test_category_grade` (6) |
| `scoreboard_intake.py` | Runs it after the constants fit, non-fatal; the PASS line gains `; categories …` | test `test_scoreboard_intake.FromPull.test_cli_grades_the_category_forecasts_after_the_fit` |

First reading on the records (EVIDENCE: run; week 3 is the only week with both forecasts and finals):

| category | flat: Brier | favoured side won | stated | real games: Brier | favoured side won | stated |
|---|---|---|---|---|---|---|
| FG% | 0.241 | 4 of 6 | 0.66 | 0.237 | 4 of 6 | 0.67 |
| FT% | 0.079 | 5 of 6 | 0.77 | 0.078 | 5 of 6 | 0.78 |
| 3PTM | 0.202 | 5 of 6 | 0.82 | 0.191 | 5 of 6 | 0.84 |
| PTS | 0.247 | 3 of 6 | 0.66 | 0.183 | 3 of 6 | 0.67 |
| REB | 0.211 | 4 of 6 | 0.69 | 0.199 | 5 of 6 | 0.77 |
| AST | 0.202 | 4 of 6 | 0.67 | 0.266 | 3 of 6 | 0.69 |
| ST | 0.199 | 5 of 6 | 0.67 | 0.203 | 5 of 6 | 0.70 |
| BLK | 0.095 | 6 of 6 | 0.70 | 0.062 | 6 of 6 | 0.76 |
| TO | 0.328 | 3 of 6 | 0.69 | 0.252 | 4 of 6 | 0.66 |
| all | 0.200 | 39 of 54 | 0.71 | 0.186 | 40 of 54 | 0.73 |

Read with care: one week is six forecasts per category. In total the favoured side won 72% of the time against a stated 71% (flat). Turnovers scored worse than a coin flip on the flat forecast in this one week. No conclusion rests on it yet.

## 2. Adds counter (P7)

| piece | what it does | evidence |
|---|---|---|
| `flaim_live.py` | The league-settings response the morning run already makes is pinned with the pull as `league_info` (maxWeeklyAdds, usesFaab, waiverType, waiverTime, startWeek, endWeek, currentWeek); a later pin without it keeps the earlier | tests `test_flaim_live.LeagueInfo` |
| `week_matchup.adds_this_week` | The owner's adds from the week's first day: the league transaction record (complete through the last morning) plus the day's move records, a name counted once across accents; the limit from the pull, or said to be not on record | tests `test_week_matchup.AddsThisWeek`, `AddsOnTheCard` |
| `season_deck.py` | The live week tile adds "Adds this week: 1 of 4 used (Alex Caruso); 3 left." | tests `test_season_deck.AddsLine` |

Behavioral check on the 11-10 records (EVIDENCE: run in a scratch copy): used 1 (Alex Caruso), limit not on record (no pull carries the settings yet). Flaim's settings response of 2026-11-10 reads `maxWeeklyAdds: 4`.

## 3. Checks

- Red first: `test_category_grade` (6), the intake test (1), `LeagueInfo` (2), `AddsThisWeek` (5), `AddsOnTheCard` (1), `AddsLine` (4, of which 3 failed before the code).
- A side effect found and fixed before the commit: the intake's older tests wrote `category_grades.*` into the repository's report folder. A run pointed at its own accuracy output now keeps the grades beside it.
- Whole suite on this branch: 949 tests OK (2 skipped).

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds (season sweep 2026-11-09, engine 01483de). Nothing here touches a title figure.

## 4. Bounds

- Out of scope by design: the grades propose nothing and no rule reads them. The counter counts adds, not Yahoo's own tally, and cannot see a pending waiver claim.
- In scope and unverified: a move in the hours around the week's boundary can land a day off Yahoo's count, because the records carry UTC dates (did not check against Yahoo's own figure). A player added, dropped and added again in one week counts once.
- This branch and PR #252 both edit one line of `season_deck.py`; the second to merge needs main merged in first.

## 5. Next steps (owner decisions)

1. **Merge (Recommended).** The first category grades land with Monday's intake of week 4; the limit shows on the deck from the next morning pull.
2. After four graded weeks, decide whether a category that stays above the coin flip needs its own look (assessment, on your go).

Runner impact: code-only. The Monday SCOREBOARD INTAKE line gains a third part (`; categories …`) after the accuracy card and the fit; the morning pull gains `league_info`. No prompt change.

## Fired

plan-gate (loaded; compact plan table shown before the first edit) · council (loaded; ruling 4–1) · adversarial-verify (loaded this turn).

## Watchlist

- 2026-11-09: week 3 on the accuracy card, the candidate's second graded week under D-ML-1.
- 2026-11-16: the week-5 confidence re-run; re-run `backtest.py` on about 20 games per player.

## Open-item receipts

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck 366d3ca (this PR changes no deck file), checked today, the same page the 10/22 day report replayed. Its table stands, carried here verbatim from the day report.

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
