# The Monday intake reads Flaim's "final", not a string Flaim never sends — 2026-10-23

Window: the kit at `main` `3ca1150` plus this branch. No projection line, tag, roster, engine constant or ledger row changed; one script and its test file change.

Pull window: 2026-10-23 → 2026-10-23. No pull: a contract fix found by reading the live pull and the tool's own description.

**Finding (2026-10-23, the Runner session, editing the Monday step into the morning prompt).** `scoreboard_intake.from_pull` (Build 1, PR #184) accepted a week only when every matchup's `status` read `"finished"`. Flaim's `get_matchups` description, read today, says the status is `upcoming`, `in_progress` or `final`, and that Yahoo's winner appears only when it is `final`. Today's pull (`pull_2026-10-23.json` on `season/daily` `8fde7a2`) carries 18 matchup statuses, all `in_progress`, consistent with that contract. The string `"finished"` was written from recall, and the test fixture used the same string, so the tests passed against themselves and not against the source. Unfixed, every Monday's intake would have halted with "week N is not finished … are 'final'" and the pull path would never have recorded a week; the League tab was unaffected (it dates a finished week by the pull's date, not the status).

**Method (stated before the fix, owner go 2026-10-23: "Fix now: accept final").** The check requires `status == "final"` exactly; `upcoming`, `in_progress` and any other string (the old `"finished"` included) halt as before. Red first: the fixture moved to `"final"` and a new test asserts that `"finished"` halts.

## 1. What changed (EVIDENCE)

- `scripts/scoreboard_intake.py`: the status check and its halt message read `final`; the docstring and the `--from-pull` help name the contract and the Runner's flag.
- `scripts/test_scoreboard_intake.py`: the FromPull fixture is built with `"final"`; new test `test_a_week_marked_finished_is_not_final_and_halts`.
- Red then green: on the unpatched script, 3 of the 5 FromPull tests failed, the CLI one printing exactly Monday's failure (`SCOREBOARD INTAKE: FAIL — week 1 is not finished in pull_2026-10-26.json (matchups [1, 2, 3, 4, 5, 6] are 'final')`); after the patch, `test_scoreboard_intake.py` 10 of 10 and `test_league_table.py` 10 of 10 pass, and the full suite (30 files) fails only the two pre-existing transcript tests (`test_league_live`, `test_matchup_live`; PR #172). `report/run-ledger.jsonl` stayed at 808 lines across the suite.
- Roster changes: none (no pool row, tag, line or roster touched).

## 2. Bounds

- **In scope and unverified:** no pull has yet observed a completed Yahoo week, so `"final"` rests on Flaim's documented contract, not an observed record; the first observation is Monday 2026-10-26's run. If the wire differs from the contract, the intake halts non-fatally and names the string it saw.
- **Flagged, not fixed (the Runner's second point):** the morning prompt derives last week as Yahoo's `currentWeek − 1`; if Yahoo has not rolled by 12:00Z Monday, the run reports "no week N matchups" and records nothing. The kit's own calendar (`week_of(date)`, as `league_table.py` uses) would not depend on the rollover; the prompt is the owner's to change.
- **Out of scope by design:** the two pre-existing transcript-dependent failures (PR #172).

**Bands.** This change computes no figure; the standing sweep's bands (`redteam-2026-10-19/sweep.json`, engine 048efb6) are unchanged:
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

## Watchlist

- **Monday 2026-10-26, the morning run:** its `SCOREBOARD INTAKE` line is the first observation of a completed week's status string; a HALT naming any value but `final` is a contract change to report, not a fixture to patch.
- **Any string a script expects from a connector:** it is read from the tool's description or an observed pull, never written from recall; the fixture and the script agreeing is not evidence.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| `from_pull` rejecting Flaim's `final` | **FIXED** on this draft PR | §1 |
| `currentWeek − 1` rollover dependence in the morning prompt | **OPEN**, flagged to the owner | §2 |
| `test_matchup_live` and `test_league_live` transcript dependence | **OPEN**, flagged (PR #172) | §2 |

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
