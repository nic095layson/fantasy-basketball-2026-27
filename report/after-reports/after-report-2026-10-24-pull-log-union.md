# report/pull-log.md gets the union merge driver — 2026-10-24

Window: the kit at `main` `0869566` plus this branch. No projection line, tag, roster, engine constant or ledger row changed; one line in `.gitattributes` and one new test file.

Pull window: 2026-10-24 → 2026-10-24. No pull.

**Incident (the Runner's record, `season/daily` `169da89`, read and checked against git this session).** The 12:03Z morning fire stopped at step 2: `git merge origin/main` into `season/daily` conflicted on `gates.json` and `report/pull-log.md`, both regenerated on both branches the same day — PR #188 into `season/daily` (box re-pull, 00:21Z) and PR #189 into `main` (scoring loop, 00:40Z), both merged by this session. The runner stopped per its rule, the owner answered at 16:35Z, the merge was resolved mechanically (`3f42157`) and the run completed at 16:49Z (`4be1760`). Cost: a 4.5-hour stall and a blocked afternoon slot. The cause was this session's: two same-day PRs onto the two branches, each carrying its own whole-file `gates.json` and its own `pull-log.md` row.

**Owner's decisions (2026-10-24, on the incident record).** Decision 1 "Add it now, own PR": the union merge driver for `pull-log.md`. Decision 2 "Prompt rule now, per-report later": a Runner-prompt line for `gates.json` today (given to the owner), per-report gate verdicts next week. Decisions 3–5: prompt lines, given to the owner.

**Method (stated before the change).** `report/pull-log.md merge=union` in `.gitattributes`, the same driver `report/run-ledger.jsonl` already carries. The file is an append-only table, so union is safe; two rows appended at the same spot keep whichever order git produces, and the date column orders them for the reader. The test builds a throwaway repository with the kit's `.gitattributes`, appends a different row on two branches, merges, and reads the file — git's behaviour, not the kit's code.

## 1. What changed (EVIDENCE)

- `.gitattributes`: `report/pull-log.md merge=union`.
- `scripts/test_merge_drivers.py` (new, 3): pull-log — two rows appended on two branches merge with exit 0, no conflicted path, both rows present, no markers (red before the line, green after); run-ledger — the existing driver still merges two appended rows; a file with no driver (`gates.json`) still conflicts the way the morning merge did (the control; decision 2 covers it).
- Takes effect for any merge run from a checkout whose tree carries the new `.gitattributes`: `season/daily` gets it at its next `git merge origin/main`. Tomorrow's merge is clean by construction either way — since `3f42157`, `season/daily` has changed neither file, so main's new versions of both merge as one-sided changes.
- Roster changes: none (no pool row, tag, line or roster touched).

## 2. Bounds

- **Out of scope by design:** `gates.json` (decision 2: prompt rule today, per-report verdicts as a later PR); the Runner prompt's step-2 failure branch, Monday formula, AskUserQuestion rule and commit list (decisions 2–5, lines given to the owner to paste).
- **Standing correction for this session:** after merging a PR into `season/daily` on a day `main` also moved, open the merge-main-into-season/daily PR at once, so the morning fire fast-forwards; never leave a conflict for the runner to meet.

**Bands.** This change computes no figure; the standing sweep's bands (`redteam-2026-10-19/sweep.json`, engine 048efb6) are unchanged:
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

## Watchlist

- **Tomorrow's step 2:** `Auto-merging report/pull-log.md` with no conflict line is the driver at work; a `CONFLICT` naming `gates.json` alone is decision 2's case, resolved by the prompt rule once pasted.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| pull-log.md union merge driver (decision 1) | **FIXED** on this draft PR | §1 |
| gates.json shared across branches (decision 2) | **OPEN**: prompt rule given; per-report verdicts next week | §2 |
| Runner prompt lines (decisions 2–5, Monday formula, commit list incl. report/calibration_daily.*) | **OPEN**, owner's prompt; lines given | §2 |
| `test_matchup_live` and `test_league_live` transcript dependence | **OPEN**, flagged (PR #172) | — |

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
