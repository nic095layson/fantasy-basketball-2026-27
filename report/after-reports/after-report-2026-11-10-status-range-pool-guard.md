# Week card status range and the simulator pool guard (audit 2026-11-10, fixes F2 and F4; council ruling 4–1)

Pull window: 2026-11-10 → 2026-11-10 (no pull: data/status/status_2026-11-10_pm.json, data/source/flaim/pull_2026-11-10_pm.json, data/league_state.json and data/season/pool_season.csv at be859ea on season/daily, read only; kit main 5841723, deck main 01483de).

**Method up front.** Order: the owner's 11-10 audit card, pick "F1 + F2 + F4 (Recommended)", with "have council deliberate … conduct red tests before building, and if all green, proceed on Council recommendations". The council ruled 4–1 to build F4 and F2 together (neither changes a graded input) and F1 alone in its own PR. Each fix had its test written first and seen failing (10 tests: 7 failed or errored before the code, 1 passed trivially, 2 deck tests failed), then the code, then the whole suite. No projection line, injury tag, roster or engine constant changes. EVIDENCE marks what a run or a read showed.

**Verdict: both fixes are in and green. The week card now records, and the deck's live week tile now says, both ends when one of the owner's players is Questionable with a game left. The simulator now refuses to run on a pool other than the one loaded.**

## 1. F2: the week card's status range

| before | after | evidence |
|---|---|---|
| On 11-10 one Questionable tag (Kel'el Ware, availability 0.50) took the card from 82.4% to 69.3% with no word why | `week_matchup.build` adds `status_range`: the players of mine tagged between out and healthy with a projected game left, and the card's 5+ chance and expected categories with every such player at 1.0 ("plays") and at 0.0 ("sits"). None when there is no such player. The card's own figure does not move | `week_matchup._status_range`; tests `test_week_matchup.StatusRange` |
| The live week tile showed one figure | The tile adds one line: "Kel'el Ware is Questionable. If he plays every game: 82.4% · if he sits all week: 54.0%." Two players: "A and B are Questionable. If both play …". No line on a record without a range, so older records draw as before | `season_deck.py` `statusRangeLine`; tests `test_season_deck.StatusRangeLine` |

Behavioral check on the 11-10 afternoon records (EVIDENCE: run): card 69.3%; plays 82.4% (5.64 categories), which equals the counterfactual run in the audit with the tag removed; sits 54.0% (4.61 categories).

Scope, by the council's ruling: the range covers the owner's players only. The opponent's Questionable players are counted at their tag's availability, as before. Covering them too is an owner decision (below).

## 2. F4: the pool guard

| before | after | evidence |
|---|---|---|
| `co_gm.run_league_sim` read `SEASON_POOL` when it ran. The rosters it was handed carried the lines `load_pool` had read earlier. A variable changed in between made the simulator play a different pool, silently | `load_pool` records the file it read. `run_league_sim` calls `pool_guard()` first, which raises a RuntimeError naming both files when they differ. No load yet, or the same file: nothing changes | `co_gm.pool_guard`; tests `test_daily_brief.PoolGuard` (the simulator is never started in the refused case) |

No script in the kit sets `SEASON_POOL` between a load and a simulation (EVIDENCE: a search of `scripts/*.py`; the morning run passes it per step). The guard changes no run that works today.

## 3. Checks

- Red first: `test_daily_brief.PoolGuard` (3), `test_week_matchup.StatusRange` (4), `test_season_deck.StatusRangeLine` (3, of which 2 failed; the "no line" test passed before the code, as it should).
- One test expectation of mine was wrong and was corrected before the build was called green: the fixture's own morning status tags Jokić Questionable, so the morning card carries a range too.
- Whole suite: 884 tests OK (2 skipped).

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds (season sweep 2026-11-09, engine 01483de). Neither fix touches a title figure.

## 4. Bounds

- Out of scope by design: F1 (its own PR), F3, F5, F6; the opponent's side of the range.
- In scope and unverified: the tile line was read in the test browser, not on a phone (did not check).

## 5. Next steps (owner decisions)

1. **Merge as is (Recommended).** The next morning run writes the range and the deck shows the line.
2. Add the opponent's Questionable players to the range (a second line; code, a test and an after-report, on your go).

Runner impact: code-only. The morning and afternoon runs need no prompt change. `week_matchup_<date>.json` gains one field (`status_range`), and the deck's live week tile gains one line when the field is set. `daily_brief.py` and `il_return.py` now stop with a named error if the pool changes between load and simulation; no current step does that.

## Fired

plan-gate (loaded; compact plan table shown before the first edit) · council (loaded; ruling 4–1) · adversarial-verify (loaded before delivery).

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
