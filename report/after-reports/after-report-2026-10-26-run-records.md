# The afternoon run stops overwriting the morning's league moves, and the runs say what they wrote — 2026-10-26

Window: the kit at `main` `d04523d` plus this branch; the records branch `season/daily` at `5f95841` for the evidence. No projection line, injury tag, roster or engine constant changed.

Pull window: 2026-10-26 → 2026-10-26. No pull: both findings come from the code and from git history.

**Owner's decisions (2026-10-26, clicked).** Problem 1: "A. Afternoon writes its own _pm file", then "Include the am baseline". Problem 2: "A. WROTE manifest + clean-tree check".

## 1. What was wrong (EVIDENCE, re-verified this session)

- **The overwrite.** `league_live.py:291` calls `league_moves.write_record(old, new, a.as_of)`; `write_record` (`league_moves.py:45`) opens `data/news/league_moves_<date>.json` with mode `"w"` (`:49`). Both runs date by UTC and both fall on the same UTC date — the morning cron is `0 5 * * *` Pacific (last fired 2026-10-26T12:09:39Z), the afternoon `0 15 * * *` Pacific (last fired 2026-10-25T22:04:02Z). Reproduced on `data/news/league_moves_2026-10-25.json`: at morning commit `d887553` it reads `old_as_of 2026-10-24 → new_as_of 2026-10-25`, five teams; at afternoon commit `13597a2`, `2026-10-25 → 2026-10-25`, two teams. The overnight record survived only in git.
- **The blast radius is one reader.** A repo-wide search finds `daily_brief.league_moves_for` (`daily_brief.py:63-65`, used at `:195` and `:225`) and nothing else; `season_deck` does not render the brief's `league_moves` field, and no other script reads the file. So the live damage was: the brief was built each morning from the morning record, and by 22:00Z the file behind it said something else.
- **The commit lists drift.** The morning prompt's step 6 names twelve paths; the run also writes `report/league/league_<date>.json` (`league_table.py:320`), `report/form/form_<date>.{json,csv}` (`form_board.py:175,180`) and, on Mondays, `report/calibration.json/.md` (`weekly_preview.py:94,152-153`) and `report/calibration_daily.json/.md` (`score_week.py:181`). The 10/26 re-run commit `5f95841` carries all of `report/league` and `report/form`, committed by the runner's judgment outside the prompt; `21995bf` is a separate sweep-up commit for the four calibration files. The afternoon prompt's step 4 omits `report/run-ledger.jsonl`, which `league_live` and `status_feed` both append to (`run_ledger.py:79`).
- **Correction to my own first pass:** I listed `manager_log.py` among the scripts whose write sites I read. It does not exist on `main` — it is on `season/daily` only, and the morning prompt guards it with "if it exists". The manifest built by reading `main` was therefore incomplete by one script. Option 2A removes that class of error: it measures the tree instead of enumerating scripts.

## 2. What was built (EVIDENCE)

**Problem 1 — the phase split with an am baseline.**
- `league_moves.record_path(date, phase, outdir)`: `am` keeps `league_moves_<date>.json`, `pm` writes `league_moves_<date>_pm.json`. `write_record(..., phase="am")` records the phase in the file and defaults to `am`, so nothing changes until a caller asks for `pm`.
- `league_live.py` gains `--phase am|pm` (default `am`) and `--news-dir`. `record_moves()` writes the phase's record and, on the morning, a copy of the state it produced as `data/news/league_state_am_<date>.json`. `am_baseline()` reads the most recent such copy within `BASELINE_LOOKBACK_DAYS` (7, hand-set and declared), falling back to `league_state.json` when none exists — so a morning re-run made after that day's afternoon run still diffs overnight.
- `daily_brief` is untouched: it reads the unsuffixed name, which is now always the morning's.

**Problem 2 — the WROTE manifest and the clean-tree check.**
- `morning.py` snapshots `git status --porcelain --untracked-files=all` before and after each step and attributes the difference to that step. Each step's `wrote` list and the run's union land in `report/briefs/morning_<date>.json`, and `print_manifest()` prints a `WROTE: n path(s)` block after the MORNING line. Outside a git checkout the manifest reads `unattributed (not a git checkout)` rather than a confident empty list.
- `scripts/commit_check.py` (new): after the commit, any change still in the tree under `data/` or `report/` fails loudly and is named; `--expected` additionally names a path the run reported writing that never reached a commit. `--untracked-files=all` is deliberate — git otherwise collapses a new directory to `report/` and hides which file was left behind.

**Tests, red first.** `test_league_moves.Phase` (2), `test_league_live.Phases` (3: the pm file leaves the morning record byte-identical, a morning re-run after the afternoon still diffs overnight, no baseline falls back to disk), `test_morning.Manifest` (4, including the unattributed case), `test_commit_check` (5, new file). All nine failed before the code.

**Behavioural check (twice, scratch repo):** a two-step run reported `['report/form/form_2026-10-26.csv', 'report/league/league_2026-10-26.json']` — the two paths that have drifted out of the prompt's list — and `commit_check` failed before the commit and passed after. A second run writing new content to a tracked file reported it; a run writing byte-identical content reported nothing.

**Suite:** 34 files, 502 tests; the only failures are the two pre-existing transcript-dependent ones (`test_league_live` 1, `test_matchup_live` 1; PR #172). `report/run-ledger.jsonl` unchanged across the suite (871 lines).

## 3. Bounds

- **The afternoon keeps writing the morning file until the prompt changes.** `--phase` defaults to `am`, which is the safe default (unchanged behaviour), so Problem 1 is only *fixed in production* once the owner applies the afternoon prompt's `--phase pm`. The replacement text is drafted, not applied.
- **The manifest is a changed-paths manifest, not a touched-paths manifest.** A run that rewrites a file with identical bytes reports nothing for it. That is the right answer for committing (there is nothing to commit), but it is not a record of every file the run opened.
- **`--untracked-files=all` costs a full worktree scan per step.** On this repo that is milliseconds; on a much larger tree it would not be free.
- **Not fixed, by decision:** the historical records the afternoon overwrote. They remain recoverable from git (`d887553` and earlier morning commits). Back-filling them is listed in §4 as an option, not done.
- **Assumption A1:** the morning run is the one that writes the baseline. If a day ever runs the afternoon first, that day has no baseline and the next morning falls back to the state on disk — the old behaviour, not a new failure.

**Bands.** This change computes no engine figure; the standing sweep's bands (`redteam-2026-10-19/sweep.json`, engine 048efb6) are unchanged:
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

## 4. Open for the owner

- **Apply the two prompt edits** (before/after in full in `prompt-diff-2026-10-26-run-records.md`, beside this report). Until then the afternoon still overwrites.
- **Back-fill the overwritten overnight records** from git history into `league_moves_<date>.json`, or leave history as the record. Not done either way.

## Watchlist

- **The first afternoon run after the prompt edit:** its LEAGUE MOVES line should name `league_moves_<date>_pm.json`, and the morning file's mtime should not move.
- **Any morning WROTE block naming a path outside the commit list:** that is the drift this was built to catch; the commit check turns it into a failure rather than a leftover.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| afternoon overwrites the morning's league-moves record | **FIXED** in code on this draft PR; needs the prompt edit to take effect | §2, §3 |
| morning re-run diffing against the afternoon state | **FIXED** (am baseline) | §2 |
| prompts' commit lists drift from what the runs write | **FIXED** (manifest + check); needs the prompt edits | §2, §3 |
| back-filling the overwritten historical records | **OPEN**, owner decision | §4 |
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
