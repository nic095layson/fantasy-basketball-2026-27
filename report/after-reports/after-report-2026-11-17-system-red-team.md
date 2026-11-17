# System red team: operations, computations and the Runner (2026-11-17, evening)

Pull window: 2026-11-17 → 2026-11-17 (no pull: kit main 80b2be4, deck main 3551a15, the records branch season/daily at e971a0f, read only; one live Flaim read of the owner's roster; one season sweep run twice; one independent re-implementation by a separate agent).

**Owner's request, verbatim (2026-11-17).** "Red team system operations and ensure computations, logic are robust and with integrity. Ensure Top to Bottom, along with Runner session, are all calibrated and consolidated." Then, on the card: "Flag it and re-sweep (Recommended)"; "Draft the wording for me (Recommended)"; "Keep 28 days, 0.5, 10 games (Recommended)"; "Fix notes now, assess discount Monday (Recommended)".

**Method up front.** Read-only checks first, each named with its command below; then the four picks. The known-answer re-implementation was written by a separate agent given the written rules only, with the kit's own scripts and this day's reports forbidden to it; it read only `data/actuals`, `data/league_state.json` and `data/status/espn_injuries_*.json` on season/daily e971a0f. The sweep is the standing one (`scripts/redteam/sweep.py`, 6,000 seasons × seeds 2026 and 2027, real schedule) on the records of e971a0f with kit main merged, the inputs the Runner's Monday step uses.

**Verdict. The machinery and the Runner are consistent: every standing check passes, the Runner's two stored prompts match their repository copies, its morning run passed all 24 steps, and today's new code reproduces from its written rules. One integrity defect was live: the brief and the deck page printed the structural band of Monday morning's sweep, measured on an engine whose shock and availability constants changed that afternoon, with nothing to say so. This pull request makes a band from another engine say STALE (brief, deck page, report gate) and adds a sweep on today's configuration, on which no constant reaches the FRAGILE line.**

Runner impact: code-only (the brief's band line, the brief record's new key `band_check` and the deck page's band note read the sweep's engine against the live one; the report gate fails a report that names a stale sweep). No prompt, step or pass line changes. From the Runner's first run after a merge, the brief and the page quote the sweep of 2026-11-17 until the Monday step writes a newer one.

Pool rows touched: none

## 1. What was checked

| layer | result | EVIDENCE |
|---|---|---|
| Engine attacks | PASS | `python3 scripts/redteam/run_attacks.py --check`: 11 attacks CURRENT on engine 3551a15 (engine files last changed ecb60cb) |
| Constants registry | PASS | `python3 scripts/redteam/check_constants.py`: 53 registered = 53 live |
| Kit tests | PASS | full suite in the 20:08 UTC gate run of kit #290; the files changed here re-run below |
| Deck tests | PASS | `arena/test_*.py` 6 of 6 modules OK; `scripts/test_draft.py` 67 of 67 |
| Governance copies | PASS | 16 of 16 hook files identical in kit main, deck main and the core-governance plugin 0.1.6 (sha256 per file); `selftest-turn-gates.py W` 6 of 6; doctrine block identical in both CLAUDE.md files |
| Runner morning run of 2026-11-17 | PASS | `report/briefs/morning_2026-11-17.json`: 24 steps, each verdict PASS; `python3 scripts/run_watch.py --date 2026-11-17 --phase am --ref origin/season/daily`: "RUN WATCH: PASS — am 2026-11-17: morning PASS, 24 steps, no step failed" |
| Runner stored prompts | PASS | the scheduler's prompts (`list_triggers`, 2026-11-17) equal `report/runner/morning_prompt.txt` and `afternoon_prompt.txt` but for the files' final newline |
| Runner branch | in step | season/daily is 16 commits behind main (the day's merges); a trial merge of main into it is clean |
| Deck page | PASS | `report/season/deck_record_2026-11-17.json`: 21 inputs pinned, none changed since; 7 tabs, 0 page errors; the morning report's byte check (737,319 built bytes inside the 737,865-byte live page) |
| Records against Yahoo | PASS | Flaim `get_roster` for the owner's team, 2026-11-17 about 20:30 UTC: the same 15 players in the same slots as `data/league_state.json` |
| Schedules | PASS | the Runner's two runs and both watchdogs enabled, last runs SUCCEEDED |
| Today's title share | reproduces | 13.98 / 14.19 in the brief; the same in two separate re-runs of the day; 13.98 / 14.19 as the new sweep's 10k reference |

## 2. Known-answer re-implementation

Three computations built that day, rebuilt from their written rules by the separate agent and compared with the kit's code on the same records.

| computation | kit | separate agent | result |
|---|---|---|---|
| Starts watch, 2026-11-17 | 20 players | 21 players | the 20 match in every field (run length, minutes, new); the extra name is the owner's Cameron Johnson, whom the written rule could not tie to his box-score name "Cam Johnson" and the kit's name table does |
| Out since, 2026-11-17 | 51 pool players | 77 rows | the 51 pool players match in every field; the other 26 are not in the pool, which the kit's gate never reads; long absences 13 against 13 |
| Sampling error of a title change at 14.085%, 2 × 10,000 seasons | 0.6818 | 0.6818 | equal; the three-pick reading and the tie equal |

The agent ran its script twice with byte-identical output. INFERENCE: the one disagreement is the specification's, not the code's; the starts watch rests on the kit's name table to recognise a rostered player, so a missing alias would list a rostered player as free.

## 3. The stale band

| | sweep quoted on 2026-11-17 | the live engine |
|---|---|---|
| record | `redteam-2026-11-16-season` (season/daily), made at the Monday morning run | deck 3551a15 |
| engine files | 95ebade | ecb60cb |
| TEAM_WEEK_SHOCK | 0.06 | 0.11 (2026-11-16 afternoon) |
| availability, healthy / risk | 0.88 / 0.75 | 0.80 / 0.65 (2026-11-16 afternoon) |
| band printed | weekly_availability FRAGILE -3.2 / +2.8 | not measured on this engine with these lines until this report |

EVIDENCE: the record's `engine_commit` c933f07, whose last engine commit is 95ebade (`git log -1 -- scripts/hoops.py arena/arena.py`); the brief's line "Structural band (season sweep of 2026-11-16 (1 day old; ...), deck c933f07): weekly_availability is FRAGILE: -3.2 ... / +2.8 ..."; the deck page draws the same record (`sweep_record.latest`). The cause: the brief and the deck pick the newest season sweep by date and never compare its engine with the live one; the attack runner does that comparison and was not consulted. The reports of the session that day quoted the sweep of `shock-fit-2026-11-16`, which is on the live engine, so the brief and those reports disagreed on the same headline.

## 4. The new sweep

`report/after-reports/redteam-2026-11-17-season/sweep.json`: deck 3551a15, 2026-11-17 rosters and season lines (with the minutes switch), real schedule, inputs copied beside it and pinned by sha256. Baseline 14.00 / 14.33 against the 10k reference 13.98 / 14.19, within 3 SE on both seeds (MC SE 0.54). Run twice (once in a scratch worktree, once here): every title and every tier identical; only the stored paths differ.

| constant | variants (title share points) | tier |
|---|---|---|
| weekly_availability | -0.6 (healthy 0.88) / +0.2 (healthy 0.78) / -1.9 (risk 0.75) / +1.9 (risk 0.56) | SENSITIVE |
| TEAM_WEEK_SHOCK | +1.5 (no shock) / +0.6 (old 0.06) / 0.0 (0.13) | SENSITIVE |
| PCT_MIX_INFL | +0.7 / -0.5 | ROBUST |
| GAMES_PER_WEEK | -0.4 / +0.5 | ROBUST |
| BENCH_WEIGHT | 0.0 / 0.0 | ROBUST |

Two error bars on the owner's title share of the day, 14.1%: sampling ±0.5 (two runs of 10,000); structural, the largest single constant, weekly_availability, -1.9 / +1.9. The risk variants sit 0.07 and 0.10 points under the 2-point FRAGILE line, inside one MC SE of it, and the same constant read FRAGILE (-2.6 / +1.4) on the live engine with the lines before the minutes switch. INFERENCE: the tier is a coin flip at this threshold; the band, about ±2 points, is the figure that matters.

## 5. What was built

| change | file | checks |
|---|---|---|
| `stale(rec, deck)`: CURRENT when the engine files at the record's commit are the live ones (the attack runner's rule), STALE when not, UNKNOWN when it cannot tell; `stale_note` the words printed | `scripts/sweep_record.py` | `test_sweep_record.py` Stale, 6 tests on a fixture git history; on the real records: the 11-16 Runner sweep STALE ("measured on engine 95ebade, the live engine is ecb60cb"), the 11-17 and shock-fit sweeps CURRENT |
| The brief's band line says STALE; the brief record gains `band_check` | `scripts/daily_brief.py` | `test_daily_brief.py` Band, 2 tests (one moved off the live sweep onto a fixture: it asserted a FRAGILE constant exists, a property of the day's data) |
| The deck page: "Model bands: STALE, ..." and the reason in the hover; "Model bands: no FRAGILE constant" instead of an empty line when none is | `scripts/season_deck.py` | `test_season_deck.py` BandStale, 2 rendered-page tests |
| The report gate fails a report that names a stale sweep | `scripts/redteam/check_bands.py` (`--deck`, default the sibling checkout) | `test_redteam_sweep.py`, 1 test |
| The sweep of section 4 | `report/after-reports/redteam-2026-11-17-season/` | run twice, identical |
| Registry notes: TEAM_WEEK_SHOCK and weekly_availability gain the 11-17 tiers beside the post-mortem history; hoops.availability's comparison updated to the 11-16 tiers and the week-4 measurement; the owner's pick of the grader settings recorded on the three D-DL-1 rows (no value changes) | `scripts/redteam/constants_registry.json` | `check_constants.py` PASS, 53 = 53 |

Each new test failed on the code before this change (brief 1 error, gate 1 error, sweep record 6 errors, deck page 1 failure and 1 error) and passes after.

## 6. Decisions for the owner (nothing changes without a pick)

1. Done on the owner's card click ("Merge #291 now"): merged as kit #291 (main 7950fba), before the Runner's 04:40 PT run of 2026-11-18.
2. Done on the owner's card click ("Show the largest band anyway"): section 8.
3. The Runner's morning prompt (the owner edits it from the Runner's conversation): the wording is drafted in the session's message of 2026-11-17; the repository copy is refreshed after the edit.
4. The kit board's risk discount (assumed ratio 0.904 against 0.718 measured, SE 0.031, weeks 1-4): assessment at the Monday review of 2026-11-23 (owner pick).

## 7. Bounds

Out of scope by design: no constant value, line, roster or pool row was changed; the Runner's prompts and branch were not touched; no trade was scored (owner veto 2026-10-20).

In scope and unverified:
- The deck's `scripts/test_gates.py`: NOT-ATTEMPTED today (it stalled twice on 2026-11-16 after 32 passing cases).
- The week card against the simulator, re-run: NOT-ATTEMPTED (last measured 2026-11-16, within 0.004 per category).
- The live deck page itself was not opened; its check is the Runner's byte comparison.
- The afternoon run of 2026-11-17 had not run when this was written.
- Three regular-season box-score days rest on one outlet (10-27, 11-03, 11-14; the files say so).
- One run of the full kit suite inside the gate runner failed one test (1,312 run, 1 failure) after the deck wording fix; which test was not recorded (the gate keeps the last lines only). ATTEMPTED-FAILED to reproduce: two later full runs, one direct and one inside the gate runner with the whole output saved, passed 1,312 of 1,312 (2 skipped).
- `stale()` sees the engine only: a sweep made before a change to how the season lines are made (the minutes switch of 2026-11-16) reads CURRENT. The configuration it ran on is named beside it (`describe`).
- 17 hand-set constants await calibration, each with a named decision in the registry; 7 more are draft-day only.

## 8. Follow-up the same evening: the largest band

With no FRAGILE constant, the brief and the deck printed no band at all while the availability tiers moved the title share by 1.9 points. On the owner's pick, both now fall back to the SENSITIVE constant with the largest shift, labelled as such (`sweep_record.shown_bands`; a sweep with any FRAGILE constant prints exactly what it printed before). The report gate (`check_bands.py`) still owes FRAGILE bands only.

Tomorrow's band line from the sweep of 2026-11-17, printed by the merged code plus this change: "no FRAGILE constant; the largest band, weekly_availability is SENSITIVE: -0.6 (healthy at the old 0.88) / +0.2 (healthy at the unfloored fit (0.78)) / -1.9 (risk at the old 0.75) / +1.9 (risk at the unfloored fit (0.56))". The deck's note: "Model bands: weekly_availability (SENSITIVE, the largest) -0.6/+0.2/-1.9/+1.9 title pts".

Tests: `test_sweep_record.py` ShownBands (4), `test_daily_brief.py` (1), `test_season_deck.py` BandStale (2, one rewritten from "no FRAGILE constant" to the fallback, one new for an all-ROBUST sweep). On the code before the change: 4 errors, 1 failure, 1 failure.

## 9. Provenance

Session of 2026-11-17 (session models A and B), the Main session; branch `claude/stale-band-flag`. Records: kit main 80b2be4, deck main 3551a15, season/daily e971a0f. Re-verify: `python3 scripts/test_sweep_record.py`; `python3 -m unittest scripts.test_season_deck.BandStale`; `python3 scripts/redteam/check_bands.py --report <report> --sweep report/after-reports/redteam-2026-11-16-season/sweep.json` from a season/daily checkout (expect FAIL, STALE); the sweep: `python3 scripts/redteam/sweep.py --season <state> <pool> --real-schedule <schedule> --out <dir>/sweep.json` on season/daily e971a0f with main merged.
