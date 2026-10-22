# Week 2's prediction recorded before the week — 2026-10-22

Window: the kit at `main` `d2f2f0f`, the league state of the 10/22 morning run (`season/daily` `e7b69bb`, rosters from Flaim 12 of 12), the deck at `048efb6`. Lines v69, the same as week 1. No projection line, tag, roster or engine constant changed.

Pull window: 2026-10-22 → 2026-10-22. No new pull: the rosters are the 10/22 morning run's Flaim pull, already logged; the state file is pinned beside this report (`week2-record-2026-10-22/league_state_e7b69bb.json`, sha256 64eaafe93e13).

**Owner's decision (2026-10-22, decision 5 on PR #171).** "Record it now (Recommended)": record week 2's prediction with `weekly_preview.py --week 2 --record` before Monday 10/26, so the ledger has no hole.

**What was run.** The weekly preview, recorded once, then re-run without recording to check it reproduces. Method, stated to the owner before the run: the same as week 1, so the ledger compares like with like — v69 lines, the season per-game CV (`arena.SEASON_CV`), the house weekly draw with the shared shock, 10,000 simulated weeks for each of seeds 2026 and 2027, non-IL rosters as of 10/22. The opponent is the league schedule's seat 1, Looking Cool Joker! (Oblena), which matches Flaim's pinned week-2 pairings (PR #171, `next-level-2026-10-22/flaim_samples.json`).

## 1. What happened (EVIDENCE)

- **The first run stopped before writing anything.** `CG.rosters` raised `KeyError: 'Andre Drummond'`: he is on seat 9's roster in the 10/22 state and has no v69 line (the open D-DR-1 item). The preview built a model for all twelve rosters but simulates only the owner against one opponent (`scripts/weekly_preview.py:59`), so a third team's player could stop the record without touching the prediction.
- **The fix, red-first.** The preview now models only the two teams in the matchup, and a player without a line on either of them stops it by name (`scripts/weekly_preview.py:64`). Two new tests (`scripts/test_weekly.py:44`, `MatchupOnly`): a third team carrying a player with no line neither stops nor moves the preview (identical by-seed results), and a matchup player with no line stops it with his name. Both failed on `main` (`KeyError`, 2 errors of 5), then passed twice (5 of 5).
- **The record.** `report/calibration.json` week 2: recorded 2026-10-22T17:09:13Z, week starts 2026-10-26; P(win) 0.576 (seeds 0.570 / 0.582); expected categories 4.82 of 9; lines v69; rosters as of 2026-10-22. Week 1's row is byte-identical to before (`week2-record-2026-10-22/calibration_before.json`). The ledger refuses a rewrite and a record after the week starts (`test_weekly.py`, the existing ledger tests).
- **Reproduces.** Re-running the preview on the same state gives identical by-seed results (`week2-record-2026-10-22/commands.txt`; the record run's output is `record.txt`).

| category | P(you win), week 2 |
|---|---|
| FG% | 0.655 |
| FT% | 0.648 |
| 3PTM | 0.474 |
| PTS | 0.312 |
| REB | 0.399 |
| AST | 0.063 |
| ST | 0.544 |
| BLK | 0.762 |
| TO | 0.961 |

The full preview is `report/previews/week_02.md`. These are the kit's own figures; no FantasyBot or Yahoo projection is quoted.

## 2. Tests

- `scripts/test_weekly.py`: 5 of 5, twice; `scripts/test_season_cv.py` (the preview runs on the season CV): OK.
- Full suite: 356 run, 1 failure, 1 skipped. The failure is `test_matchup_live.Record.test_todays_transcript_yields_todays_outlook`, which reads the newest session transcript in the container and expects week 1's opponent; it fails identically on unchanged `main` `d2f2f0f` (run the same day), so it is not this change's. Not skipped or changed here; recorded below.

## 3. Bounds

- **Out of scope by design:** the method itself. Week 2 runs on the preseason v69 lines and the 3.5-games-per-player weekly model, as week 1 did; P3 (owner's decision 3) moves the title odds to the season lines, and the ledger records the lines each week used.
- **In scope and unverified:** none open. The prediction cannot be graded until week 2 ends (11/01) and its result is entered.

## Watchlist

- **Week 1 ends Sunday 10/25:** its result can be scored (`weekly_preview.py --score 1 --won ...`); P2 (owner's decision 2) automates the intake.
- **The records branch** (`season/daily`) still carries the ledger without week 2 until this PR reaches `main` and the branch next syncs.
- **`test_matchup_live`** depends on the newest session transcript in the container, so it fails in any session whose latest FantasyBot outlook is not week 1's (flagged, not fixed).

## Open-item receipts

| item | status | receipt |
|---|---|---|
| the weekly prediction ledger | **OPEN**: week 1 recorded 2026-10-15 and not yet scored; week 2 recorded 2026-10-22 | §1 |
| D-DR-1 (Drummond has no v69 line) | **OPEN**; no longer stops the weekly record unless he is in the matchup | §1 |
| `test_matchup_live` transcript dependence | **OPEN**, flagged here | §2 |

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
