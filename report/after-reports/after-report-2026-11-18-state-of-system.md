# State of the system and confidence by layer, 2026-11-18

Pull window: 2026-11-16 → 2026-11-18 (no pull: kit main 471244d, deck main 3551a15, the records branch season/daily at 2a61d547, read only; no new simulation).

**Owner's request, verbatim (2026-11-18):** "Please provide full state of system report, and confidence %"

**Method up front.** Stated to the owner before any check ran. The baseline is the last scored record, `after-report-2026-11-16-post-handoff.md` (2026-11-16 evening: kit main 9cb7e23, records 92d0034), with the same layers and the same scoring: each score is a judgment anchored on the evidence beside it, only the evidence column is measured, and machinery, governance and forecasts are never averaged together. No week has been graded since 11-16 (week 5 is graded on Monday 2026-11-23), so a forecast score moves here only for a structural finding made on 11-17 or 11-18, never for a new outcome. Structural bands are the season sweep of 2026-11-17 (`redteam-2026-11-17-season/sweep.json`, deck 3551a15, the one the morning brief quotes). Checks run today, each on the commits named above:

| Check | Command | Result |
|---|---|---|
| Standing attacks | `python3 scripts/redteam/run_attacks.py --check` | PASS, 11 attacks CURRENT on deck 3551a15 (engine files at ecb60cb) |
| Constants registry | `python3 scripts/redteam/check_constants.py` | PASS, 53 registered = 53 live (declared_band 5, measured 10, settings 8, structural 6, uncalibrated 24) |
| Kit test suite | `python3 -m unittest discover -s scripts -p 'test_*.py'` | 1,322 tests OK (2 skipped), 176 s |
| Deck engine and draft tests | `arena/test_*.py`, `scripts/test_draft.py` in the deck checkout | engine modules 6 of 6 exit 0; draft 67 of 67 |
| Hook parity | sha256 of every file in `hooks/`, kit main vs deck main vs the core-governance plugin | 16 of 16 identical in all three; plugin 0.1.6, selftest 6 of 6; doctrine block identical in both CLAUDE.md files |
| Daily runs | `report/briefs/morning_<date>.json`, `afternoon_report_<date>.md` on season/daily | mornings 11-16 PASS (28 steps), 11-17 PASS (24), 11-18 PASS (24), 0 failed steps; afternoons 11-16 and 11-17 "Nothing failed" (11-18's runs at 23:00 UTC, after this report) |
| Run watch | the two scheduled watchdogs' last runs | PASS am 11-18, PASS pm 11-17 |
| Deck page | morning SEASON DECK step, 11-18 | PASS, 7 tabs, 0 page errors; published version 90 |
| Open pull requests | GitHub, both repositories | kit: #290 (draft, held to Monday 11-23 on the owner's pick), #165 (never merge); deck: #5 (July draft) |

**Verdict: the machinery holds at about 94% and governance at 95%, both unchanged within a point. The forecasts slip from about 63% to about 62%: two structural findings (turnovers and FG% lines run high; the waiver scan's first pick lands at the 64th percentile of what was free) outweigh one improvement (the availability constant is now SENSITIVE, not FRAGILE). The title share, 12.3% this morning, is still the least trustworthy number the kit prints.**

Runner impact: none — this report changes no step, record, prompt or code.

Pool rows touched: none

## 1. What changed since 2026-11-16 evening (11 pull requests, #283 to #289 and #291 to #294)

| Area | Pull requests | What it does now |
|---|---|---|
| Records and method stamps | #283, #286, #287 | confidence re-run record; the title watch walks a method-change day like for like; every title share carries its method stamp (RULES.md rule 12) |
| Runner | #285 | runbook for rebuilding the Runner; both stored prompts copied into the repository |
| Gaps and traces | #284 | five gaps from the 11-17 audit, the overnight title trace, and the fixes that could be built |
| Missed pickups | #288, #289 | starts watch (a free player who starts 2 straight games) and hold check (a recent drop who then plays) in the brief and on the deck's Free Agents tab |
| Model bands | #291, #292 | a sweep older than the engine it describes prints STALE; when no constant is FRAGILE, the largest SENSITIVE band is still shown |
| Start/sit card | #293 | top 1 to 3 swaps only, each with its cost, "Keep your lineup" when none clears 0.05; category heat map folded under "Category detail" |
| Waiver timing | #294 | a player on waivers is priced from his claim date, not today (Alex Caruso, on waivers until 11-19) |

Held, not merged: #290 (the waiver scan treats a short Out as a short absence; the list says which repeats it can tell apart), on the owner's card "Merge Monday 11-23".

## 2. Machinery: does it run and compute right?

| Layer | 11-16 eve | 11-18 | EVIDENCE for the change |
|---|---|---|---|
| Engine math | 98% | **98%** | attacks CURRENT 11 of 11, constants 53 = 53 (table above). Kit 1,322 tests OK; deck modules 6 of 6, draft 67 of 67 |
| Data pulls and records | 94% | **95%** | three mornings PASS with 0 failed steps and two afternoons "Nothing failed" (table above); 12 of 12 Flaim rosters each morning. The 11-17 box scores are single-source (ESPN only), which the run allows and labels |
| Roster and injury status | 94% | **94%** | one timing defect found by the owner and fixed (#294: a player on waivers was priced as a same-day add); one repeat-listing defect found by the 11-17 audit and fixed on a branch still held (#290). Status gate PASS each morning, 33 flagged rows on 11-18, each with a dated receipt |
| Process and integrity | 95% | **94%** | 6 corrections-log rows dated 11-17, none dated 11-18 (12 dated 11-16). The red team of 11-17 found that the brief had quoted a week-old sweep as current without saying so (fixed, #291). This session's Stop gate fired once (a merge before the plan was shown in that turn), caught and corrected. One full-suite failure seen once on 11-17 inside the gate runner was not reproduced in two later runs and is not explained |
| The deck page | 90% | **90%** | version 90 built and published with 7 tabs and 0 page errors; its 753,089 built bytes sit inside the 753,635-byte live page. The start/sit card's over-listing (one bench player offered for every starter) was caught by the owner, not by a check, and fixed (#293) |

Machinery, simple mean of five layers: **94.2%** (11-16 evening 94.2%).

## 3. Governance

| Item | Status | EVIDENCE |
|---|---|---|
| Plugin governs the session | PASS | core-governance 0.1.6; selftest 6 of 6 |
| Hook copies | PASS | 16 of 16 identical: kit main, deck main, plugin |
| Merge law | PASS | each of the 11 merges was on the owner's own card click naming the pull request, pinned to its head sha; #290 held as he chose |
| Scheduled tasks | PASS | `list_triggers`, both pages: the Runner's morning and afternoon tasks enabled and untouched by this session; the run watches enabled; this session's reminders listed in section 7 |
| Runner prompt | owner edited | the live morning prompt (updated 2026-11-17 22:12 UTC) carries the owner's minutes-line wording; the repository copy `report/runner/morning_prompt.txt` still has the old "minutes-trend CANDIDATE" wording. Monday review item 9 proposes the refresh |
| Disputed results | unchanged | `OPEN.md` (last changed 7aa18a3): X-1 to X-4 still DISPUTED, none cited here |
| Score | **95%** | INFERENCE: one Stop-gate catch is the mechanism working; the stale repository copy of the prompt is a record lag, not a wrong run |

## 4. Forecasts: how far to trust what it predicts?

| Layer | 11-16 eve | 11-18 | EVIDENCE for the change |
|---|---|---|---|
| Player lines | 80% | **78%** | red team of 11-17 (`after-report-2026-11-17-system-red-team.md`), weeks 1 to 4, player-clustered: REB +6.7% (t 4.2), STL +10.1% (t 3.6), and two not known on 11-16: TO +4.1% (t 2.0, rising +0.5 / +4.3 / +6.7% in weeks 2 to 4) and FG% lines about 1 point high with FGA +6.9%. The minutes line is ungraded until 11-23 |
| Injury and availability discounts | 50% | **50%** | the constant moved from FRAGILE (11-16: -2.6 / +1.4) to SENSITIVE (11-17 sweep: -0.6 / +0.2 healthy, -1.9 / +1.9 risk tier). Against it: the kit board's risk discount is 0.904 against a measured 0.718 (SE 0.031), 6 SE apart (`report/fits.md`); assessment set for Monday on the owner's pick |
| Daily lineup card | 85% | **85%** | no new grade (`calibration_daily.json` weeks 1 to 4, skill +0.140, +0.149, +0.030, +0.042, n 36 / 63 / 63 / 54). The card now names at most 3 swaps (#293) |
| Weekly matchup forecast | 60% | **60%** | week 5 is ungraded: the card said 6-3-0 on 11-18; Yahoo has the owner up 5-3-1 after two days. League matchups through week 4: Brier 0.222 and 0.217 against a coin's 0.25 (n 6 a week, weeks 3 and 4) |
| Waiver pairs (relative) | 70% | **65%** | missed-pickup audit (`after-report-2026-11-17-missed-pickups.md`): the scan's first pick landed at the median 64th percentile of free players over the next 7 days, and 5 of 22 first picks then played no game; 5 of the 9 adds the kit flagged played at top-100 level. The 11-18 scan's top three all drop Ziaire Williams, the repeat pattern #290 addresses |
| Title share as an absolute number | 35% | **35%** | 14.1% to 12.3% overnight, -1.8 against a band of ±0.7 (`title_watch_2026-11-18.md`); split on 6 seeds: the owner's swap about -1.2, Walker Kessler off IL -0.8, Cade n em -0.4, two others +0.1 each. Every part is an event, none a method change |

Forecasts, simple mean of six layers: **62.2%** (11-16 evening 63.3%).

## 5. Today's headline figures with both error bars

| Figure | Value | Sampling error | Structural band (sweep of 2026-11-17) |
|---|---|---|---|
| Title share | 12.3% | ±0.5 (2 runs × 10,000 seasons) | weekly_availability SENSITIVE, the largest: -0.6 / +0.2 (healthy tier), -1.9 / +1.9 (risk tier); TEAM_WEEK_SHOCK SENSITIVE +1.5 / +0.6 / 0.0 |
| Reach the final | about 25% | about ±0.7 on a difference of two picks | the same constants; no FRAGILE constant |
| Playoffs | 96.2% | brief | not swept separately |
| Title if IL players return on ESPN's dates | about 21.2% | brief | a scenario, not a forecast |

The sweep's baseline was 14.00 / 14.33 against its own reference 13.98 / 14.19 (MC SE 0.54); PCT_MIX_INFL and GAMES_PER_WEEK ROBUST; BENCH_WEIGHT 0 / 0. The sweep ran on 11-17's rosters, before the owner's swap and Kessler's return.

## 6. Findings and decisions for the owner

| # | Finding | Evidence | Proposed |
|---|---|---|---|
| 1 | #290 (waiver scan repeats) is ready but held | GitHub: draft, head 9afc749 | merge on Monday 11-23 as already chosen (reminder set) |
| 2 | The Runner prompt's repository copy is behind the live prompt | section 3 | refresh the copy in a small pull request (Monday item 9) |
| 3 | Lines run high on turnovers and FG% as well as rebounds and steals | section 4 | re-measure with week 5 on Monday, then decide (already on the Monday notes, items 2 to 4) |
| 4 | The kit board's risk discount is 6 SE off the measurement | section 4 | assess on Monday as chosen (item 8) |
| 5 | The waiver scan's first pick is middling against what was free | section 4 | none new: the starts watch (#288) and #290 are the owner's chosen answers; re-audit one week on (Monday item 7) |

No new decision is open today: each finding already has the owner's pick and a scheduled check.

## 7. Scheduled checks this session holds

| When (UTC) | What |
|---|---|
| daily 13:37 to 11-30 | minutes watch: Andrew Wiggins, Nic Claxton |
| 11-20 14:05 | plan the second gate-fix pull request (another session's reminder) |
| 11-22 14:00 | return day: Williams re-score against Champagnie and Caruso; the drop pair |
| 11-23 16:10 to 17:20 | Monday upkeep review, its notes, the #290 merge ask, the one-sided threes grade |
| 11-25 17:00 | ESPN return dates re-graded on four weeks |
| 12-28, 2027-02-01 | confidence re-runs, weeks 10 and 15 |

## 8. Bounds

Out of scope by design: no simulation, sweep or line was re-run; no roster, constant, prompt or scheduled task changed; hypothetical trades (standing owner veto).

In scope and unverified:
- The 11-18 afternoon run had not fired when this report was written (23:00 UTC); did not check it.
- Week 5 is ungraded, so no forecast score moved for an outcome; the 11-23 grade can move any of them.
- The intermittent test failure of 11-17: ATTEMPTED-FAILED (two later full runs passed; the failing test was not captured).
- "Reach the final about 25%" is from this session's 6-seed runs of 11-18, not a brief record.

## 9. Provenance

Session of 2026-11-18 (session model B, continuing the Main session; branch `claude/state-2026-11-18`). Records: kit main 471244d, deck main 3551a15, season/daily 2a61d547. Earlier evidence cited from this session's reports of 11-17 and 11-18 (session models A and B). Re-verify: `python3 scripts/redteam/run_attacks.py --check` and `python3 scripts/redteam/check_constants.py` with the deck checkout at its main; `python3 -m unittest discover -s scripts -p 'test_*.py'`; `git show origin/season/daily:report/briefs/morning_report_2026-11-18.md`; the hook parity loop compares `git show origin/main:hooks/<f> | sha256sum` in both repositories with the plugin's `scripts/<f>`.
