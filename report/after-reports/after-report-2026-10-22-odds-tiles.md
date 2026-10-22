# The Odds card: the pre-week forecast labelled, and a live week tile beside it — 2026-10-22

Window: the kit at `main` `bac6882` plus this branch; the 10/22 morning records (`season/daily` `e7b69bb`); the deck at `048efb6`. No projection line, tag, roster, ledger row or engine constant changed.

Pull window: 2026-10-22 → 2026-10-22. No new pull: the render reads the 10/22 morning run's records, already logged.

**Owner's question (2026-10-22).** "The categorical breakdown regarding my Week 1 matchup shows a projection of 3 - 6 (me losing). However below that, it shows my Odds 60% to win Week 1? Are these synced and can these two display more precise projections?" Assessment given first (not synced by design: the 60.6% is the ledger's week-1 prediction, recorded 2026-10-15 before the week and frozen so it can be graded; the 3–6–0 is this morning's live card). **Decision: "Live + pre-week (Recommended)".**

**Method (stated before the build).** The live tile's main figure is the expected categories won this week, the sum of the card's nine chances (exact, and it is what the each-category standings count). Its second figure is the chance of 5 or more of 9, from those chances with the categories taken as **independent** (a simplification: counting categories move together; the tile says so). The pre-week tile keeps the ledger's figure and shows its recorded date.

## 1. What changed (EVIDENCE)

- `scripts/week_matchup.py`: `win_week_chance` (line 233), the distribution of category wins built one category at a time; the record carries `p_5plus` (line 627).
- `scripts/season_deck.py`: the Odds card's first tile reads "week N pre-week forecast · recorded <date>" (line 400); `liveTile` (line 384) shows "week N now: expected categories of 9" and "5+ of 9", or "no live record this morning" when the week card is missing or for another week. The FantasyBot "This week — live" card showed the same frozen figure as "P(win week) — our simulator"; it now reads "pre-week forecast" (line 604).
- Tests: `test_week_matchup.py` class `WinWeek` (line 293, hand figures with `math.comb`) and the record test; `test_season_deck.py` from line 606 (three page tests).

## 2. Tests

- Red first: 4 errors in `test_week_matchup.py`, 3 failures in `test_season_deck.py` on main's code; then green twice.
- Full suite: 374 run, 1 failure (`test_matchup_live`, the known transcript-dependent test, failing identically on main), 1 skipped.

## 3. On today's records (EVIDENCE; two runs byte-identical)

The pre-week tile: 60.6%, recorded 2026-10-15. The live tile: 3.44 expected categories of 9; 5+ of 9: 14.0%. Rendered with no page error (`odds-tiles-2026-10-22/odds_tiles_real_2026-10-22.png`). Why they differ: the pre-week prediction counted REB (0.75) and BLK (0.95) as likely wins; two days in, you trail 52–71 and 7–11 and the projected finals favour them.

## 4. Bounds

- **Assumption A1 (unconfirmed):** the league scores each category separately, so expected categories is the figure that maps onto the standings; confirmed when week 1's standings show W+L+T = 9 per team.
- **INFERENCE:** the 5+ figure is approximate because of the independence simplification; not measured against a simulation (did not check).
- **Out of scope by design:** the ledger and its method (frozen for grading).

**Bands.** The live tile's chances use neither FRAGILE constant of the standing sweep (`redteam-2026-10-19/sweep.json`, engine 048efb6): the shared shock is left out and availability is the day's status. The pre-week tile is the ledger's prediction, which runs on both (`weekly_preview.py`); the sweep measured them on the title share, and their effect on the week's figures was not measured (did not check):
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).


## Watchlist

- **Week 1's final standings (after 10/25):** W+L+T = 9 confirms A1.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| the Odds card's frozen figure read as live | **FIXED** on this draft PR | §1 |
| `test_matchup_live` transcript dependence | **OPEN**, flagged (PR #172) | §2 |

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward as the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck 048efb6, checked today, the same page the 10/22 day report and the GAUNTLET report replayed. Its table stands, carried here verbatim from the day report.

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
