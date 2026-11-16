# State of the system, week of 2026-11-09 to 2026-11-16

Pull window: 2026-11-09 → 2026-11-16 (no pull: kit main b7d8a10; the records branch season/daily at b35ad98, read only; one season sweep run in a throwaway worktree on today's switched lines, section 4).

**Owner's request, verbatim (2026-11-16):** "Can you please conduct state-of-system wide report, with additions from last week and confidence/robustness auditing and findings. Thank you"

**Method up front.** Stated to the owner before any run: window 11-09 to 11-16; sources are the merged pull requests on main, the run ledger and morning records on season/daily, the weekly accuracy and calibration records, the constants registry check, the standing attack list, and one fresh season sweep (`scripts/redteam/sweep.py`, 6,000 seasons x seeds 2026 and 2027, real schedule, baseline asserted within 3 SE of its own 10k reference) on today's minutes-switched lines, because the switch changed the simulator's input and the 5 AM sweep ran on the old lines. Confidence scores are judgments anchored on the evidence beside them, as in `after-report-2026-10-29-confidence.md`; only the evidence column is measured.

**Verdict: the machinery is sound and grew a lot this week (32 pull requests); the forecasts are a little better than a week ago. The largest finding is today's: the minutes-based line moves the owner's title share from about 14.8% to about 11.8% on the same rosters, a method change, not an event, and tomorrow's title watch will show it as a drop.**

Runner impact: code-only — the morning title-watch step now names method changes (section 7); no step, record or prompt changes.

Pool rows touched: none

## 1. What was added (pull requests #244 to #275, 2026-11-09 to 2026-11-16)

| Area | Pull requests | What it does now |
|---|---|---|
| Daily run resilience | #253, #257, #271 | run watch alerts at 6:30 AM and 3:45 PM; `morning.py --resume` re-runs only what was skipped; package scan; integrity checks; the brief no longer stops on an owner player outside the pool |
| Decision log and grading | #245, #252, #274 | alternative pairs and a re-join file; the decision card; players outside the pool scored from box scores on the board's scale |
| Week card | #250, #251, #274, #275 | status range; one roster build shared with the simulator; auto-row players counted; ESPN return dates applied by day; same-day swaps priced when the add's team plays today |
| Lines and forecasts | #247, #265, #267, #274 | week preview carries its structural band and a Monday staleness line; threes-split candidate (graded, not live); minutes line live on PTS, REB and AST since 11-16 |
| Deck page | #248, #254, #255, #261, #264, #265, #269, #270 | Week tab in plain language, category grades, weekly adds counter, playoff games, FAAB bids, Draft Check tab, season totals, punt-aware view, trending-up free agents on minutes, Full health button, Board category filter |
| Records and rosters | #244, #246, #258, #259, #260, #263 | league table by team key, auto-row players in the simulator, manager log, ESPN dates graded and worded as the earliest return, team-update path, owner playbook and corrections log |
| Audits and gates | #249, #256, #262, #266, #268, #272 | title-drop trace, audit findings F1 to F6 fixed, council fixes, report gates tightened, confidence re-run for week 5 |
| Waiver scan | #273 | never offers a rostered player who sits outside the pool |

## 2. Health of the daily runs (2026-11-10 to 2026-11-16)

| Morning | Result | Notes |
|---|---|---|
| 11-10, 11-12, 11-13, 11-14, 11-16 | PASS | 20 to 28 steps |
| 11-11 | FAIL, then PASS on re-run | two Basketball-Reference pages missing; fixed by #257 and re-run the same morning |
| 11-15 | FAIL at the daily brief | an owner player outside the pool (Hezonja); fixed by #271; that morning is missing from week 4's daily calibration (`calibration_daily.json`, days_missing 2026-11-15) |

Afternoon checks ran all seven days; the 11-15 afternoon deck was not built because the morning brief was missing.

## 3. Confidence by layer, this morning and now

| Layer | 11-16 am | 11-16 now | EVIDENCE for the change |
|---|---|---|---|
| Engine math | 98% | **98%** | constants 53 registered = 53 live; attacks CURRENT 10 of 11 (section 4) |
| Data pulls and records | 94% | **94%** | section 2; no change today |
| Roster and injury status | 93% | **95%** | the week card now reads ESPN return dates by day (#274) |
| Process and integrity | 96% | **95%** | four session statements corrected since 11-14 (`corrections-log.md`, one row of 11-14 and three of 11-16), each caught and logged; the availability build could not reach the deck repository |
| The deck page | 88% | **90%** | Week tab carries the fixes from the 3 PM build on (#274, #275) |
| Player lines | 80% | **80%** | minutes line live on PTS/REB/AST: lower MAE than the blend in weeks 2, 3 and 4 (`accuracy.json`); not yet graded live |
| Injury and availability discounts | 40% | **40%** | measured 0.78 and 0.56 against 0.88 and 0.75 (`fit_week4.json`); the owner's floor (0.80 / 0.65) is not built |
| Daily lineup card | 85% | **85%** | unchanged (`calibration_daily.json`, skill positive in weeks 1 to 4) |
| Weekly matchup forecast | 55% | **65%** | both week-card gaps closed (57.0% became 87.4% on the same records); pickups priced with the right timing |
| Waiver pairs (relative) | 70% | **70%** | unchanged |
| Title share as an absolute number | 35% | **30%** | one method change moved it about 3 points in a day (section 4), on top of the FRAGILE availability band |

## 4. Robustness audit

| Check | Result |
|---|---|
| Constants registry against the live engine (`check_constants.py`) | PASS, 53 registered = 53 live, deck 01483de |
| Standing attack list (`run_attacks.py --check`, record `state-of-system-2026-11-16/attacks.json`) | PASS: CURRENT 10 of 11 at the start of this audit; A-6 (decision robustness) read UNFINGERPRINTED since October. After the owner's pick, CURRENT 11 of 11 (section 7) |
| Deck engine between this morning's sweep (c933f07) and this one (01483de) | the two commits differ only in hook files; no engine file differs |
| Season sweep on the switched lines (`state-of-system-2026-11-16/sweep.json`) | baseline within 3 SE of its 10k reference on both seeds; MC SE 0.54 |

Same rosters (state sha a12ecf58 in both), same schedule, the only input difference is the pool: the switched pool's blend file is byte-identical to this morning's pool (sha dbe05f8d).

| Figure | 5 AM, blend lines | Now, minutes-switched lines |
|---|---|---|
| Title share, 10k reference (seed 2026 / 2027) | 14.69 / 14.52 | 11.23 / 12.29 |
| Sweep baseline (seed 2026 / 2027) | 14.95 / 14.60 | 11.30 / 12.23 |
| FRAGILE constants | weekly_availability | weekly_availability |
| SENSITIVE constants | none | none |

**weekly_availability is FRAGILE:** -3.2 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.3 (healthy players play 0.95 of games) / -0.2 (healthy players play 0.80 of games); headline 11.8% within that band. Sweep of 2026-11-16 on the switched lines (`state-of-system-2026-11-16/sweep.json`); every other constant ROBUST.

Where the switch lands, summing each active player's per-game change (minutes line less blend): the owner's team PTS -2.4, REB -1.2, AST -0.4; the opponent this week -2.4 / -0.2 / -0.7; four rivals gain 1.8 to 4.3 points (MISSI ELLIOTT +4.3, Scottie's Thotties +3.2, Cade n em +2.0, Podz save the league +1.8). The owner's lines that fall most are Miles Bridges (16.1 to 15.3 points), Kel'el Ware, PJ Washington, John Collins and Derrick White: players whose recent minutes run below what the blend implied.

INFERENCE: the minutes line was more accurate on PTS, REB and AST in each graded week, so the lower figure is the better-supported one; it is still one method's figure inside a band of about 5.5 points.

## 5. Forecast accuracy, weeks 1 to 4 (`accuracy.json`, `calibration.json`, `calibration_daily.json`)

| Measure | Week 1 | Week 2 | Week 3 | Week 4 |
|---|---|---|---|---|
| In-season line, points bias | n/a | +8.7% | +9.1% | +1.7% |
| Rebounds bias | n/a | +3.8% | +6.4% | +7.0% |
| Steals bias | n/a | +0.9% | +12.5% | +13.9% |
| Healthy-tier games played (assumed 0.88) | 0.83 | 0.79 | 0.77 | 0.74 |
| Pre-week P(win), result | 0.606, L | 0.576, W | 0.847, W | 0.410, L |
| Daily card skill over the scoreboard | +0.140 | +0.149 | +0.030 | +0.042 |

Players graded: 246 to 261 a week. Decision grades at 5 AM: 34 rows, none final yet; five session rows were added today (two of them later superseded); the first 28-day window closes 11-17.

## 6. Findings and decisions for the owner

| # | Finding | Evidence | Proposed |
|---|---|---|---|
| 1 | Title share falls about 3 points tomorrow from the line switch alone; the title watch compares day to day and will read it as a loss | section 4 | a method-change marker on the title watch, or a note here only |
| 2 | The availability floor (0.80 / 0.65) the owner picked is not built | the deck repository could not be attached from this session | a session with the deck repository attached |
| 3 | Rebounds and steals projections run high and rising | section 5 | watch through the week-5 grade |
| 4 | Attack A-6 (decision robustness) has no engine fingerprint | `attacks.json` | re-run A-6 and fingerprint it |
| 5 | Four session statements corrected since 11-14, each caught by the owner or the gates | `corrections-log.md` | none beyond the rules already logged |

## 7. Built on the owner's picks (2026-11-16, cards after section 6)

| Pick | What was done | Check |
|---|---|---|
| "Mark method changes (Recommended)" | `title_watch.py` names a METHOD CHANGE first among the causes when the season line's minutes switch differs between the two days' `season_lines_<date>.json`, or when a registered constant was added, removed or changed between the earlier run's commit and now | 5 tests written first and seen failing; on the real records the step reads "line method: the minutes ratio now applies to PTS, REB, AST (before: none)" and "constant season_lines.SWITCH_CATS added", which is what tomorrow's run will compare |
| "Re-run and stamp it (Recommended)" | A-6 re-run on engine 01483de; `attacks.json` reads its `engine_commit`; the 10-19 record kept as `rt_decisions_2026-10-19.json` | both swap verdicts stay positive under every variant (smallest +0.42 title points); attack list CURRENT 11 of 11 |
| "New session with deck repo (Recommended)" | not built here: the availability floor needs the deck repository, which this session cannot attach; the hand-off is in the chat answer of 2026-11-16 | none |

## 8. Bounds

Out of scope by design: no line, constant, roster or code changed; the decision card and the brief were not re-run on the switched lines; hypothetical trades (standing owner veto).

In scope and unverified:
- The sweep ran once on the switched lines (two seeds); the morning run will sweep again on Monday next week.
- The 11-05 and 11-13 confidence columns in `after-report-2026-11-16-confidence.md` are chat figures; this report's two columns are both from records.
