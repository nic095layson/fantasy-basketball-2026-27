# Standalone step runs leave a run-ledger row — 2026-10-23

Window: the kit at `main` `679fc8b` plus this branch. No projection line, tag, roster, engine constant or existing ledger row changed; the change adds rows for runs that had none.

Pull window: 2026-10-23 → 2026-10-23. No pull: the change is to three scripts and their tests.

**Owner's decision (2026-10-23, D5 of the system audit).** "Append rows on standalone runs (Recommended)": the 3 PM afternoon runs (`league_live.py`, `status_feed.py --check`) left no rows in `report/run-ledger.jsonl`; only `morning.py` wrote rows, as `morning: <step>`.

**Method (stated before the build).** A step script run on its own records one row under its own name (`league_live`, `status_feed`, `status_feed --check`) with PASS on exit 0 and FAIL on a HALT or gate failure. Under `morning.py`, which records `morning: <step>` itself, the environment carries `KIT_LEDGER_PARENT=morning` and the step scripts stay silent, so no step is counted twice. The ledger stays append-only; a row that cannot be written never fails the run.

## 1. What changed (EVIDENCE)

- `scripts/run_ledger.py`: `standalone_record()` — `safe_record()` that returns None under `KIT_LEDGER_PARENT`.
- `scripts/morning.py` `run_steps`: every step's environment carries `KIT_LEDGER_PARENT=morning`.
- `scripts/status_feed.py`: `--ledger` (default the kit ledger, `''` to skip); the `--check` path records `status_feed --check` PASS/FAIL.
- `scripts/league_live.py`: `--ledger`; `main()` wraps the former body and records `league_live` PASS on exit 0, FAIL otherwise.
- Tests, red first (one each failing on the unchanged code: 2 errors, 1 failure, 1 failure, 1 error), then green: `test_run_ledger.StandaloneRows` (2), `test_morning.LedgerParent` (1), `test_status_feed.LedgerRow` (1, end to end by subprocess, with and without the parent variable), `test_league_live.LedgerRow` (1, a HALT on a missing pull records FAIL).

## 2. What the afternoon run will now leave (INFERENCE from §1)

Two rows per 3 PM run: `league_live` (PASS, or FAIL on a HALT) and `status_feed --check` (PASS/FAIL), plus `status_feed` for the feed itself. The morning run's 11 `morning: <step>` rows are unchanged (the parent variable keeps the step scripts silent). The afternoon prompt needs no change: both scripts default to the kit ledger.

## 3. Bounds

- **Not checked:** a live afternoon run with this code (the next is 22:03Z today, after merge). The subprocess tests exercise the same code paths with a temp ledger.
- **Out of scope by design:** rows for the other scripts the prompts run by hand (`lineup_check.py` after #176 merges; it could take the same two lines later).

**Bands.** This change computes no figure; the standing sweep's bands (`redteam-2026-10-19/sweep.json`, engine 048efb6) are unchanged:
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

## Watchlist

- **The first 3 PM run after merge:** two or three new rows dated that run in `report/run-ledger.jsonl`, none named `morning:`.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| afternoon runs leave no ledger rows | **FIXED** on this draft PR | §1 |
| `test_matchup_live` transcript dependence | **OPEN**, flagged (PR #172) | — |

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
