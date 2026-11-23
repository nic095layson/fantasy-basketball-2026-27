# Confidence by layer after week 5 (2026-11-23)

Pull window: 2026-11-18 → 2026-11-23 (no pull: kit main b804c66, deck main 4fcd92b, the records branch season/daily read only; no new simulation).

**Owner's request, verbatim (2026-11-23).** "Can you provide me updated confidence % report", then "File it as a report".

**Method up front.** Stated to the owner before the checks: the baseline is `after-report-2026-11-18-state-of-system.md`, with the same layers and scoring. Each score is a judgment anchored on the evidence beside it; only the evidence column is measured. Week 5 is the first graded week since that report, so forecast scores may move for outcomes this time. Checks re-run today on kit main b804c66 with the deck at 4fcd92b: standing attacks, constants registry, hook parity. Bands are today's Monday sweep (`redteam-2026-11-23-season/sweep.json`, copied here from the records branch).

**Verdict. Machinery holds at about 94% and governance at 95%. The forecasts move to about 63% (from 62%): the first graded week since 11-18 lifted the player lines, the daily card and the weekly odds, and lowered the waiver advice after its first grades.**

Runner impact: none.

Pool rows touched: none

## 1. Machinery

| Layer | 11-18 | 11-23 | EVIDENCE |
|---|---|---|---|
| Engine math | 98% | **98%** | `run_attacks.py --check`: 11 attacks CURRENT on engine 4fcd92b; `check_constants.py`: 54 registered = 54 live (the kit-row games rule added, #300); full suite OK in each of today's gate runs |
| Data pulls and records | 95% | **95%** | mornings 11-17 to 11-23 all PASS in their final records; 11-20 failed first at the season deck (a rival's pickup with no board row) and was re-run PASS the same day after #298 and #299 |
| Roster and injury status | 94% | **95%** | #290 merged: the waiver scan treats a short Out as a short absence and no longer repeats names it cannot tell apart |
| Process and integrity | 94% | **93%** | 2 corrections-log rows dated 2026-11-20; the stop gate caught two outward actions taken before a plan was shown (11-20, 11-23); #298 merged without its own gates, now a written rule (#302) |
| The deck page | 90% | **91%** | Board position dropdown live (#296, #297); the morning build names a pooled player with no board row instead of stopping (#299); published daily (version 99 on 11-22) |

Machinery, simple mean of five layers: **94.4%** (11-18: 94.2%).

## 2. Governance

| Item | Status | EVIDENCE |
|---|---|---|
| Hook copies | PASS | 16 of 16 identical: kit main, deck main, plugin (re-checked 2026-11-23) |
| Merge law | PASS | every merge of the week on the owner's own word; the scheduled-run hook refused one merge inside a reminder's turn (#290), merged on his typed word |
| Lessons | added | deck LESSONS.md 25 (board rank vs value to this roster; a drop call inside the sampling error is said to be a coin flip) |
| Score | **95%** | unchanged |

## 3. Forecasts (week 5 graded)

| Layer | 11-18 | 11-23 | EVIDENCE |
|---|---|---|---|
| Player lines | 78% | **80%** | `accuracy.json` week 5, in-season line, 250 players: points bias +0.9% (wk 2 +8.7%), MAE 3.18, rank correlation 0.81 (best so far); REB +3.4% (wk 4 +7.0%), STL +2.6% (+13.9%), TO -1.2% (+6.7%); BLK +12.2% (new high) |
| Injury and availability discounts | 50% | **50%** | `report/fits.md` through week 5: risk tier 0.721 ± 0.028 (n 553) against deck 0.78, simulator 0.81, kit board 0.90; today's sweep: weekly_availability the one SENSITIVE constant |
| Daily lineup card | 85% | **87%** | `calibration_daily.json`: skill positive all 5 weeks; week 5 Brier 0.123 against 0.230 (+0.108) |
| Weekly matchup forecast | 60% | **65%** | `calibration.json` pre-week P(win), weeks 1-5: 0.61 L, 0.58 W, 0.85 W, 0.41 L, 0.76 W; favorite won 4 of 5; mean Brier 0.159 against a coin's 0.25 (n 5); league matchups week 5 Brier 0.162 (n 6) |
| Waiver pairs (relative) | 65% | **60%** | `report/decisions/scorecard.md` as of 11-23: 4 graded, KIT RIGHT 1, KIT WRONG 3 (the Braun drop calls of 10-20 to 10-22) |
| Title share as an absolute number | 35% | **35%** | brief 2026-11-23: 13.2% ± 0.5; the band moved with rosters between 11-17 and 11-19 (the shock's no-shock variant +1.66 then +0.24 on six seeds) |

Forecasts, simple mean of six layers: **62.8%** (11-18: 62.2%).

## 4. Today's headline with both error bars

Title share 13.2% ± 0.5 (2 runs × 10,000 seasons). weekly_availability is SENSITIVE: -1.38 / -0.90 (healthy at the old 0.88), +0.49 / +0.40 (healthy at the unfloored fit), -2.11 / -0.85 (risk at the old 0.75), +1.44 / +0.91 (risk at the unfloored fit), per seed; no FRAGILE constant (sweep of 2026-11-23, deck 3551a15). Playoffs 98.1%.

## 5. Bounds

Out of scope by design: no simulation, line, constant or roster changed.

In scope and unverified:
- The live season page: not read; the Runner's byte check relied on.
- The Runner session's own health beyond its run records: did not check.
- Weekly scores rest on 5 graded weeks; the week-10 re-score (2026-12-28) is the next full one.

## 6. Provenance

Session of 2026-11-23 (session model B, continuing the Main session; branch `claude/confidence-2026-11-23`). Re-verify: `python3 scripts/redteam/run_attacks.py --check`; `python3 scripts/redteam/check_constants.py`; `git show origin/season/daily:report/accuracy.json`.
