# Resilience builds A, C and D: a morning that can be finished, a package scan, and integrity checks (owner card 2026-11-11)

Pull window: 2026-11-10 → 2026-11-11 (one Flaim get_matchups and one get_roster read on the evening of 11-10 for the owner's question, not written; the 24 morning records, the run ledger, the 11-11 pull, week card, decision card and il_return record at 6f40cf6 on season/daily, read only; the account's scheduled-task list, read 2026-11-11; a scratch copy of season/daily for one trial of the package scan, nothing written back; kit main 9b0a37f).

**Method up front.** Order: the owner's audit card of 2026-11-11, picks "A. Self-healing morning", "C. Package and what-if tool" and "D. Data-integrity checks". Tests were written first and seen failing for each piece. Two display thresholds are hand-set and named below. No projection line, roster, injury tag or engine constant changes. EVIDENCE marks what a run or a read showed.

**Verdict: a failed morning can now be finished with one command that keeps both attempts on record; packages of one or two moves are scored on demand with the same models the card uses; the watchdog names a missing day; the week card warns when Yahoo counts far fewer games than the best lineup. Two audit items were examined and need no code. One finding is left as an owner decision: the manager log's code lives only on the records branch.**

## 1. What happened on 2026-11-11 (EVIDENCE: morning record, scheduled-task list)

The 05:07 PT run failed at box scores: two Basketball-Reference pages returned 404 for games ESPN already listed as final. Nineteen steps were skipped. The watchdog alerted the owner at 06:30. Recovery was then improvised twice: a session re-ran the skipped steps by hand at the owner's word, and the Runner had scheduled its own full re-run for 17:00Z, cancelled at the owner's word before it fired.

Run history: 24 morning records since 2026-10-17, 2 hard failures (10-17 and 11-11), 5 mornings with a non-fatal step failure.

## 2. A: `morning.py --resume`

| before | after |
|---|---|
| A failed morning could only be re-run whole, from a session whose transcript holds the day's roster pull | `--resume` runs only the steps the day's record does not show as PASS, in order |
| A re-run replaced the record | The record keeps the first run's time, a `resumed_at_utc`, and each earlier attempt under `attempts` with the steps that had not passed |
| | Nothing left to do: nothing runs. No record yet: a full run. A non-fatal failure is retried too |

The watchdog's ALERT for a failed morning now ends with the command that finishes it.

Proposed Runner prompt edit (not applied; the owner approves prompt edits): "On MORNING: FAIL at a fetch step, schedule one re-check two hours later that runs `morning.py --date <date> --resume` and the manager log, at most three times, and say so in the report. A session that finishes the run by hand deletes that re-check first."

## 3. C: `package_scan.py` and the return-world note

- Every available free agent with a pool line against the seven lowest-value active players (`DROP_POOL = 7`, hand-set scan width), in packages of one or two moves.
- Week: the week card's model, the moves counted from tomorrow as the decision card counts a pair (`--from-today` for a free agent added before tip-off).
- Season: the brief's weekly-categories screen for every package; the title simulation (IL players never return) for the top six by each measure (`SHORTLIST = 6`, hand-set) and every `--named` package.
- An add that would be the lowest-value active player is flagged as the next cut when the owner's first IL player returns.

The decision card and the deck's pickup table now add "(X leaves when Y returns)" to the return-on-time figure when the room rule removes the pair's own add. On 2026-11-10 several different second adds showed identical return-world figures for this reason.

EVIDENCE (trial on a scratch copy of season/daily 6f40cf6): 546 single-move packages in 99 seconds. "Julian Champagnie for Kris Dunn: 60.0% (+2.4), title +1.5", equal to the day's decision card (+2.4 points, +1.5). Counting from today instead, the same pair reads +8.7; the default was set to match the card after that mismatch was seen.

## 4. D: integrity checks

| item | result |
|---|---|
| Games-left disagreement (29/30, 22/32, 31/31 on 11-11) | Traced, no bug: three definitions. Yahoo counts players in active slots on the coming days; FantasyBot counts current starters; the card counts the best daily fill. The week card now records `lineup_gap` when Yahoo is 3 or more below the card (`LINEUP_GAP_GAMES = 3`, hand-set) and the deck says to check the lineup |
| Missing days | `run_watch.py` am: when the schedule on record shows games the day before, that day's box scores and manager-log day must exist |
| Status function "crash" | No code needed: `co_gm.fa_status` raises by design when both sources are missing; the brief catches it and the deck only calls it when one source exists |
| Transaction rows Flaim could not read (1 on 11-11) | Not built: the intake is `manager_log.py`, which is not on main (next row) |
| **Code only on the records branch** | `scripts/manager_log.py` and its tests exist on season/daily and not on main. They are outside the gates and the suite. Owner decision, section 7 |

## 5. Checks

- Red first: `Resume` (6), `MissingDays` (4), `LineupGap` (2), `LineupGapLine` (2), `test_package_scan` (9), `CaptureInputs` (2), `FirstCut` (1), `DecisionCardFirstCut` (1).
- Whole suite on this branch: 1057 tests OK (2 skipped).

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds (season sweep 2026-11-09, engine 01483de). The package scan's title figures are differences under the live constants; the band was not run on them.

## 6. Bounds

- Out of scope by design: `--resume` does not redo the roster pull. If league live itself failed, a resume from another session cannot recover it.
- Out of scope by design: the package scan gives no return-world figure; it flags the next cut instead. Which player should leave on an IL return is the owner's choice, not the room rule's.
- In scope and unverified: `--resume` inside the Runner's own session (did not check: no failed morning to resume since it was written). The 11-11 hand re-run used the same step list.
- Two-move scan, EVIDENCE: with `--must-add` 1,617 packages ran in 84 seconds on the same scratch copy. Without `--must-add` the two-move pool is about 63,000 packages; that run was not timed (did not check).
- The three hand-set numbers (7, 6, 3) are display and scan widths, not engine constants; they are not in the constants registry.

## 7. Next steps (owner decisions)

1. **Merge, and approve the Runner prompt edit in section 2 (Recommended).** The resume then has one owner: the Runner retries, a session only steps in at your word.
2. Merge without the prompt edit: the command exists; recovery stays by hand.
3. Separately: bring `manager_log.py` and its tests onto main (code only, not the records), so they are tested and gated. Recommended, as its own small PR.

Runner impact: prompt edit (proposed in section 2, not applied; without it the change is code-only and the Runner's runs are unchanged).

## Fired

plan-gate (loaded; compact plan table shown before the first edit) · adversarial-verify (loaded for the audit and again before the push) · scope-fence: not loaded.

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
