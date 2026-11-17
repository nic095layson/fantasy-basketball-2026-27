# Five gaps, one trace, and the fixes that can be built (2026-11-17)

Pull window: 2026-11-16 → 2026-11-17 (no pull: kit main 5de73b6, deck main 1a47f81, the records branch season/daily at 92d0034 and e971a0f, read only; six simulator runs in a throwaway worktree, section 1).

**Owner's request, verbatim (2026-11-17):** "Analyze what meaningful fixes and improvements can be built, the method of how you would build to strengthen these gaps, and proceed. Provide me a full analysis report and your proposed actions", with the picks "Trace the overnight drop", "Assess a change window" and "Assess the playoff weeks". It followed five gaps this session named the same day: decisions ungraded, the instrument moving more than the game, the playoff weeks, one Runner session, rivals frozen.

**Method up front.** Stated to the owner before the first run. "Proceed" was read as: proceed with the analysis and this report; nothing is built until the owner picks from section 6. The trace: the kit's league simulator on one engine (deck 1a47f81: tiers 0.80 / 0.65, shock 0.11), 10,000 seasons x seeds 2026 and 2027, weeks 1 to 4 played, IL players never returning; one input swapped at a time between the 2026-11-16 afternoon records (92d0034) and the 2026-11-17 morning records (e971a0f): rosters (`data/league_state.json`), then lines (`data/season/pool_season.csv`), then the owner's lines against the rivals'. Playoff weeks: NBA games per rostered player in Yahoo weeks 18 to 20, from `report/schedule/games-2026-27.csv` and the 11-17 rosters. The rest is read from code and records, quoted beside each claim. Records: `gaps-2026-11-17/trace.json` and `trace.py`.

**Verdict: the "overnight drop" from 16.9% to 14.1% was not an event. It is the minutes-based line reaching the daily lines file for the first time. The figure this session gave on 11-16 evening (16.9%, and the page it published) mixed the new constants with lines built before that switch; on the live method the owner's share is 14.1%, second of twelve behind ROOKS FTW (14.6%). Of the five gaps, two are worth building now (a like-for-like title watch; a method stamp with a change window), one needs only a document (a Runner rebuild guide), one is already built and simply not due yet (decision grades start arriving this week), and one is small on the evidence (the playoff weeks).**

Runner impact: none (a report; the proposals in section 6 state their own impact).

Pool rows touched: none

## 1. The trace: where 16.9% went

Both corners reproduce their sources exactly: the 11-16 evening run (16.93; seeds 16.89 / 16.96) and the 11-17 brief (14.09; seeds 13.98 / 14.19, the brief's own figures).

| rosters | lines | owner's title share | seeds |
|---|---|---|---|
| 11-16 afternoon | 11-16 (built 12:51 UTC, before the minutes switch merged) | 16.93 | 16.89 / 16.96 |
| 11-17 morning | 11-16 | 18.39 | 18.31 / 18.47 |
| 11-16 afternoon | 11-17 | 13.37 | 13.33 / 13.41 |
| 11-17 morning | 11-17 | 14.09 | 13.98 / 14.19 |
| 11-17 morning | 11-17 for the owner's players only | 15.57 | 15.57 / 15.58 |
| 11-17 morning | 11-17 for everyone else only | 16.73 | 16.36 / 17.10 |

Sampling error on a difference of two rows is about ±0.7.

| step | effect on the owner's share | EVIDENCE |
|---|---|---|
| Roster changes, 11-16 afternoon to 11-17 morning (among them SNOWTIME putting Walker Kessler on IL) | +1.5 at the old lines, +0.7 at the new | rows 1 to 4; `league_moves_2026-11-17.json` |
| The lines file of 11-17 | -4.3 at the 11-17 rosters, -3.6 at the 11-16 rosters | rows 1 to 4 |
| of which the owner's own players | -2.8 | row 5 against row 2 |
| of which everyone else's players | -1.7 | row 6 against row 2 |

EVIDENCE that the lines change is the minutes switch and not one day of games: Kawhi Leonard has not played, his minutes ratio is 0.9552 in both days' `minutes_line` records, and his points line went from 23.9 to 22.8 (23.9 x 0.9552 = 22.8). Kevin Durant: 23.0 to 22.3 at ratio 0.9751. The 11-16 lines file was written by the 5 AM run; the switch (kit #274) merged at 16:53 UTC the same day, so 11-17 is the first lines file that carries it. `after-report-2026-11-16-state-of-system.md` had measured the same switch at about -3.0 on that morning's rosters.

Why it costs this roster: 7 of the owner's 12 active players with a ratio carry one below 1 on 11-17 (Ware 0.954, Washington 0.955, Bridges 0.957, Collins 0.971, White 0.973, Durant 0.975, Queta 0.982; Cam Johnson has no ratio; Kawhi on IL 0.955). INFERENCE: the kit reads this roster as playing fewer minutes than its lines assumed. The minutes line beat the blend on points in all three graded weeks (`accuracy.json`: MAE 3.34 / 3.30 / 3.12 against 3.46 / 3.39 / 3.21), so 14.1% is the better-founded figure.

The whole walk from the 11-16 brief to the 11-17 brief:

| from | to | change | cause |
|---|---|---|---|
| 14.6 (11-16 brief) | 16.5 | +1.9 | tiers 0.80 / 0.65 and shock 0.11 (sweep of 2026-11-16, 6,000 seasons) |
| 16.5 | 16.9 | +0.4 | week 4 counted, the afternoon rosters (Spencer for Hezonja) |
| 16.9 | 18.4 | +1.5 | overnight roster changes |
| 18.4 | 14.1 (11-17 brief) | -4.3 | the minutes switch reaching the lines file |

The 11-17 title watch printed "14.6% to 14.1%, change -0.5 (band ±0.7) … within the band", under a METHOD CHANGE heading that names the switch and both constants. It is correct and it names the changes; it cannot say that +1.9 (constants), +1.9 (rosters and week 4) and -4.3 (lines) sit inside that -0.5, because it "does not split the move between the causes" (its own docstring).

**weekly_availability is FRAGILE:** -0.8 (healthy at the old 0.88) / -0.3 (healthy at the unfloored fit (0.78)) / -2.6 (risk at the old 0.75) / +1.4 (risk at the unfloored fit (0.56)); headline title share 14.1% ± 0.5 (MC) within that band. Sweep of 2026-11-16, made on the lines before the minutes switch; no sweep has run on the switched lines with the new constants.

## 2. Change window: what the record shows

| fact | EVIDENCE |
|---|---|
| 48 pull requests merged into the kit from 11-09 to 11-16; 12 on 11-16 | `git log --merges --since=2026-11-07` on main |
| 10 of the 19 corrections-log rows are dated 2026-11-16 | `report/corrections-log.md` on main |
| Three method changes merged on 11-16 reached live figures at three different moments: the constants at the next run after their merge; the minutes switch a day later, at the next lines build | section 1 |
| A session quoted a figure as "tonight's engine" that was new constants on old lines | this session, 11-16 evening; section 5 |
| Each brief records its title share; nothing on the brief names the method it was made with | `title_watch.py` rebuilds that from git history and the registry (`line_method_changes`, `registry_changes`) |

INFERENCE: the cost is not the changes, each of which was measured and gated; it is that a figure cannot be read without knowing which of them it contains, and nothing printed beside the figure says so.

## 3. Playoff weeks

| fact | EVIDENCE |
|---|---|
| The simulator plays three one-week rounds, 8 seeds, reseeded after round 1, with each team's final regular-season roster and the same weekly model as any week | `arena.playoff_champion`; `league_sim.py` ("the playoffs play the final week's roster") |
| The kit holds the NBA schedule through week 20 (2027-03-01 to 2027-03-21) | `report/schedule/games-2026-27.csv`; `co_gm.week_of` |
| NBA teams play 3.27, 3.53 and 3.47 games on average in weeks 18, 19 and 20 (range 2 to 4) | same file |
| Games per rostered player over the three weeks, by fantasy team: 9.92 to 10.73; the owner 10.20 (eighth of twelve) | 11-17 rosters, the owner's IL players counted |
| Week 18 is the owner's thin week: 3.00 games per player, the league's lowest with Cade n em; Dallas plays twice (Irving, Washington) | same |

The spread between teams is about 8% over the three weeks and about 12% in a single week, and it is measured on rosters that will change for four months. The owner's playoff probability is 98% or higher in every run of this report, so the title is decided in these weeks; the schedule itself is a small part of that on today's evidence.

## 4. The other three gaps, re-read against the code

| gap as first stated | what the code and records show | revised reading |
|---|---|---|
| "Decision value is ungraded" | `decision_grade.py` runs every morning. 28 recommendations and 14 owner moves are on the ledger; `grades.jsonl` is empty because the window is 28 days and a verdict needs 10 games: `scorecard.md` (as of 11-16) lists the first window closing 2026-11-17. Running gaps so far: Portis for Braun -2.78, Champagnie for Clowney +3.38 | Built, not yet due. Two real limits: the grade is the kit's own board value (the same lines that made the advice, with the box scores blended in), and this session's advice of 11-17 is not on the ledger (last row S-2026-11-16-01) |
| "One session carries the daily operation" | Usage on the Runner session: about $660 since 2026-10-21 (session record, 11-17). Its context was 775,056 of 1,000,000 tokens on 11-16 and 299,975 on 11-17 after an automatic compaction; the 11-17 run passed, 24 steps. `flaim_live.py` reads the day's Yahoo responses from the session transcript, filtered by the run's start time. The two stored prompts carry fresh-container steps. A search of the kit for a rebuild guide (file names and the phrases "runbook", "rebuild the runner", "new runner session") found `RULES.md` only | One clean run after one compaction. The prompts live only in the scheduler, not in the repository |
| "Rivals are frozen" | The simulator holds the other eleven rosters as they stand; the manager log is recorded daily and, by the Runner prompt's own words, "nothing in the engine reads it" | True, and unmeasured: nothing yet shows that a manager's behaviour predicts his roster's change |

## 5. Corrections this report makes to this session's own statements

| said | the record |
|---|---|
| 11-16 evening: "You're the 2nd favourite to win the league at 16.9% … tonight's engine", and the published page "Title Odds 11-16" | The lines file predated the minutes switch. On the live method: 14.1%, second behind ROOKS FTW 14.6%; SNOWTIME 12.6%, not 20.6% |
| 11-16 evening: 23.7% if every IL player returns, 30.9% if only the owner's | Same lines. The kit's own 11-17 figure for the on-time world is 20.5% |
| 11-17: the share fell overnight because "the morning run counted week 4 and refreshed the lines" | The 16.9% already counted week 4. The cause is section 1 |
| 11-17: "a real drop of roughly 2.5 points was hidden by a method gain" | The drop is itself a method change; two method changes offset, with a roster gain of about +1.5 |
| 11-16: Wiggins for Cam Johnson -1.17 title points | Run on the same pre-switch lines; not re-run. The 11-17 runs (drop pairs, Claxton, the Wiggins and Claxton build) used the 11-17 lines and stand |

## 6. Decision sheet (assessment and proposals; nothing is built without a pick)

| # | proposal | tier | what would be built, and how | Runner impact | what would demote it |
|---|---|---|---|---|---|
| F1 | Like-for-like title watch | MUST ADD | `title_watch.py` gains two re-runs when a method change is named: yesterday's pinned state and lines on today's engine, and today's rosters on yesterday's lines (both read with `git show` from the records branch). It prints the walk of section 1 instead of one net figure. Red first: a fixture where a method gain hides an input loss must fail today's output. Display only | code-only: the morning step grows by about 30 seconds on a method-change day, nothing otherwise | a change window (F2) that makes method changes rare |
| F2 | Method stamp and a change window | HIGHLY RECOMMEND | (a) the brief record gains a `method` block (deck commit, line-method flags, registry sha256), which the deck page and any session quote beside a title share; `title_watch` already derives all three. (b) one rule in `RULES.md`: a change to a constant or a line method merges on Monday after grading, unless the owner says otherwise. Tests red first for (a); (b) is a document | (a) code-only; (b) none | the owner preferring speed over like-for-like days |
| F3 | Runner rebuild guide, prompts in the repository | HIGHLY RECOMMEND | `RUNBOOK.md`: how to stand up a new Runner (repository, push right to season/daily, the two schedules), and the two stored prompts copied word for word under `report/runner/` with their dates. Documents only; no prompt is edited | none | a second Runner or a scripted run replacing the session |
| F4 | Session advice on the ledger the day it is given | HIGHLY RECOMMEND | no build: `decision_log.py --session` exists. The owner's word per day, or a Monday back-fill as on 11-16. Today's rows: keep Cam Johnson over Wiggins; pass on Claxton; the return drops (Spencer, Cam Johnson); Wiggins and Claxton gated on minutes | none (the Runner owns the branch; a session writes on the owner's word) | - |
| F5 | Playoff-weeks line in the Monday review | NICE TO HAVE | from late January, the review prints games per player in weeks 18 to 20 for the owner and his likely opponents. No engine change | none | the spread staying under about 10% |
| F6 | Rivals' behaviour in the simulator | NOT NEEDED now | first a read-only check, at week 8, of whether the manager log predicts roster change at all | none | - |
| F7 | A sweep on the switched lines | HIGHLY RECOMMEND | no build: the next Monday sweep (11-23) runs on switched lines and the new constants; until then every band quoted is the 11-16 sweep's and says so | none | - |

Also for the owner: the published page "Title Odds 11-16" shows the superseded figures (update it to 11-17, or mark it superseded); three rows for `report/corrections-log.md` (section 5).

## 7. Bounds

Out of scope by design: no line, constant, roster, prompt or code change; no trade computation; the library repository was not read.

In scope and unverified:
- Decision robustness of the 11-17 drop-pair and build figures under the swept constants: NOT-ATTEMPTED.
- Whether a compaction can ever drop the current run's Yahoo responses from the transcript the scripts read: NOT-ATTEMPTED (one passing run after one compaction is the only evidence).
- Whether the $660 is billed or is usage inside a subscription: did not check.
- The Wiggins for Cam Johnson swap on the 11-17 lines: NOT-ATTEMPTED.
- The +1.9 step for the constants is the 6,000-season sweep's figure on the 11-16 5 AM inputs, not a run of this report.

## 8. Provenance

Session of 2026-11-17 (session model A until about 17:00 UTC, session model C after), the Main session; branch `claude/new-session-koi1jp`. Records: kit main 5de73b6, deck main 1a47f81, season/daily 92d0034 and e971a0f. Re-verify: `python3 report/after-reports/gaps-2026-11-17/trace.py <state.json> <pool.csv> <out.json>` from a worktree of season/daily with the deck beside it, for each pair in `trace.json`; `git show e971a0f:report/briefs/title_watch_2026-11-17.md`; `git show e971a0f:report/decisions/scorecard.md`.
