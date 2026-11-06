# The afternoon deck record and page footer name their own page; the replay gate replays mornings only (runner finding 3, owner picks 2026-11-05/06)

Pull window: 2026-11-04 → 2026-11-05 (no pull: the records on season/daily read only at 3f85584 — deck_record_2026-11-05{,_pm}.json and the runner's after-report-2026-11-05-runner-window.md; kit main 6b30551, deck main e14cc42).

**Method up front.** Build order: the runner's `after-report-2026-11-05-runner-window.md` Finding 3 and its build prompt `prompt-2026-11-05-main-deck-record-label.md` (owner pick A1, 2026-11-05: "put the phase in the record's out path, plus a test"; B1: leave the afternoon waiver pairs). The prompt's two adjacent observations were put to the owner as cards on 2026-11-06: the page footer's same mislabel **rides this PR** (owner pick), and the replay gate **skips `_pm` records** (owner pick; the prompt had said "do not change the gate under this order", so this is the owner's own later word). Method: red-first — the new assertions were run on main's code and failed before the fix; both 11-05 records were rebuilt in a scratch worktree of season/daily and compared key by key with the committed ones. EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: three one-line fixes, each with a test; the afternoon record now names `deck_<date>_pm.html`, the afternoon page's footer names `deck_record_<date>_pm.json`, the morning record and page are unchanged, and the replay gate's input glob takes morning records only (17 of 25 on season/daily). Suite 798 OK (2 pre-existing skips); nothing merged; the 8 committed afternoon records stay as written.**

## 1. What was built (EVIDENCE: the diff, the suites)

| Fix | Where | Before → after |
|---|---|---|
| Record `out` carries the phase | `scripts/season_deck.py` `build()` record line | afternoon: `report/season/deck_2026-11-05.html` → `report/season/deck_2026-11-05_pm.html`; morning: unchanged |
| Page footer names its own record | `scripts/season_deck.py` footer JS | afternoon page: `Record: report/season/deck_record_2026-11-05.json` → `…_pm.json`; morning page: unchanged |
| Replay gate inputs | `scripts/gates.py` replay spec | glob `deck_record_*.json` → `deck_record_????-??-??.json` (morning records only; `--last 3` now replays three distinct mornings) |

Tests: `test_season_deck.AfternoonRefresh` asserts the `_pm` record's `out` and the rendered footer text of the `_pm` page; the morning `main()` test asserts the morning record's `out` and footer. Red first: on main's code `test_the_afternoon_page_is_written_beside_the_mornings` FAILED (`Ran 175 tests … FAILED (failures=1)`); with the fix `OK`. Whole suite 798 OK.

## 2. Re-runs on the records (EVIDENCE: scratch worktree at season/daily, removed after; the records tree untouched)

`season_deck.py --date 2026-11-05` and `--phase pm` with the new code: both `SEASON DECK: PASS`. Record comparison against the committed files (keys other than `generated_utc`, `render`, `inputs`, `out`): morning equal, afternoon equal; `out` morning `deck_2026-11-05.html` → same; afternoon `deck_2026-11-05.html` → `deck_2026-11-05_pm.html`. On season/daily the glob `deck_record_????-??-??.json` selects 17 of the 25 records, the last three `2026-11-03`, `2026-11-04`, `2026-11-05`.

INFERENCE: the replay gate was not run end to end here (it rebuilds three mornings through `replay_deck.sh`); its input change is a glob, covered by the listing above.

## 3. Bands quoted

No title share is quoted as a new figure in this report. The standing structural band for any title figure is the season sweep of 2026-11-02 (deck e14cc42): **weekly_availability is FRAGILE:** -2.6 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.2 (healthy players play 0.95 of games) / +0.0 (healthy players play 0.80 of games), mean of the two seeds.

Runner impact: code-only. The 3 PM run's deck step writes the corrected record and footer from the next afternoon; no step, flag or prompt change.

## 4. Bounds and open items

- Out of scope by design: rewriting the 8 committed afternoon records (they stay as written; the fix applies from the next afternoon run); B1 — the afternoon page's morning waiver pairs stay as they are (owner pick); replaying afternoon builds (the owner chose "skip", not "replay afternoons too").
- In scope and unverified: the first live afternoon run after merge (2026-11-06 ~23:03Z): its record's `out` and its footer end in `_pm`.

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
