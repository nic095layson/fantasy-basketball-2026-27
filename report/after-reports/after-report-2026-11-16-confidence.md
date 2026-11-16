# Confidence by layer, week 5 re-run (2026-11-16)

Pull window: 2026-10-20 → 2026-11-16 (no pull: the records branch season/daily at 12964ec, this morning's run, read only; kit main 8ab1d8d; one re-run of the week engine in scratch, described in section 3).

**Owner's request, verbatim (2026-10-29):** "create after-report for repo, and run this report again on the Monday morning run of Week 5, 10 and 15". On 2026-11-05: "Nothing now, revisit on 11-16" (the two decisions in section 5).

**Method up front.** The layers and scoring of `after-report-2026-10-29-confidence.md`. Each score is a judgment anchored on the evidence beside it; only the evidence column is measured. Integrity and forecasting are scored separately and never averaged. The 11-05 and 11-13 columns are the chat updates of those days, quoted from this session's record of them; they were not written to the repository. EVIDENCE marks what a record shows; INFERENCE marks a reading of it.

**Verdict: the machinery holds at about 95%. The forecasts sit at about 60%: the player lines improved (week-4 bias +1.7%, from +9%) and the injury discounts got worse (healthy players played 0.74 of team games in week 4 against 0.88 assumed). This re-run also found that the week card counts neither a rostered player without a pool row nor a return date inside the week; its 57% for week 5 becomes 87% when it does.**

Runner impact: none (a report; nothing the morning or afternoon runs execute changes).

Pool rows touched: none

## 1. Machinery: is it computing and recording correctly?

| layer | 10-29 | 11-05 | 11-13 | 11-16 | EVIDENCE |
|---|---|---|---|---|---|
| Engine math | 99% | 99% | 98% | **98%** | `run_attacks.py --check` on main 8ab1d8d: PASS, CURRENT 10 of 11; `check_constants.py`: 52 registered = 52 live. No engine defect found since the 11-12 IL-list fix |
| Data pulls and records | 94% | 95% | 96% | **94%** | morning_2026-11-14 PASS (24 steps); morning_2026-11-15 FAIL at the daily brief (an owner player outside the pool), 7 steps and the deck skipped; fixed the same day (#271); morning_2026-11-16 PASS (28 steps) |
| Roster and injury status | 95% | 93% | 95% | **93%** | status_2026-11-16: every flagged row carries a dated receipt. A day's Out tag is applied to the whole week by the week card (section 3) |
| Process and integrity | 96% | 97% | 97% | **96%** | gates PASS on #269 and #270; #271 merged with no test of its own, against the kit's red-first rule |
| The deck page | 85% | 87% | 90% | **88%** | no deck built on 2026-11-15 (the brief failed); every other build renders with 0 page errors |

## 2. Forecasts: how far to trust what it predicts?

| layer | 10-29 | 11-05 | 11-13 | 11-16 | EVIDENCE |
|---|---|---|---|---|---|
| Player lines | 70% | 65% | 75% | **80%** | `accuracy.json` points per game, in-season line: bias +8.7% (wk 2), +9.1% (wk 3), +1.7% (wk 4); MAE 3.46, 3.39, 3.21; rank correlation 0.77 to 0.79. Threes: +3.3%, +9.1%, -4.6% |
| Injury and availability discounts | 50% | 45% | 45% | **40%** | `accuracy.json`: the 0.88 tier played 0.83, 0.79, 0.77, 0.74 of team games in weeks 1 to 4; the 0.75 tier 0.57, 0.53, 0.58, 0.55. `fit_week4.json` (48 team-weeks): 0.88 tier measured 0.779 ± 0.007 (n 3,694), 0.75 tier 0.559 ± 0.024 (n 438); neither live value is within two standard errors |
| Daily lineup card | 85% | 85% | 85% | **85%** | `calibration_daily.json`: Brier 0.034, 0.145, 0.124, 0.134 against the lead-to-date's 0.174, 0.294, 0.155, 0.176; skill positive all four weeks. Reliability: stated 0.8 to 1.0 hit 0.94 (n 77); stated 0.4 to 0.6 hit 0.63 (n 27) |
| Weekly matchup forecast | 50% | 55% | 60% | **55%** | `calibration.json`: pre-week P(win) 0.606 (L), 0.576 (W), 0.847 (W), 0.410 (L); category Brier 0.253, 0.214, 0.151, 0.206 against a coin flip's 0.25. Down for the two structural gaps in section 3 |
| Waiver pairs (relative) | 70% | 70% | 70% | **70%** | brief_2026-11-16: the top pair re-adds Julian Champagnie for Mario Hezonja (+3.0 title points, +0.107 cats/week); Hezonja's Saturday was 22 points and 7 rebounds on 9 of 12. The season and weekly views still weigh a streaming add differently |
| Title share as an absolute number | 35% | 30% | 40% | **35%** | brief_2026-11-16: 14.6% (seeds 14.69 / 14.52), 19.5% on 11-14, a move of -4.9 against a band of ±0.7 (title_watch_2026-11-16). One roster move is worth about 3 points by the kit's own pair score |

**weekly_availability is FRAGILE:** -3.2 (no in-sim injury discount (risk 0.88 like healthy)) / +2.8 (harsher risk tier (0.65)) / -0.1 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games); headline 14.6% within that band. Sweep of 2026-11-16 (`redteam-2026-11-16-season/sweep.json`); TEAM_WEEK_SHOCK is now ROBUST (+0.4 / -0.9).

INFERENCE on the title move: title_watch names three rival roster changes for 11-16 but compares against 11-14, so the owner's own Hezonja-for-Champagnie move of 11-15 is not on its list. The kit's pair score prices reversing that move at +3.0, which accounts for most of the -4.9; the week-4 loss and the rivals' moves the rest. Not split by a run.

## 3. The two structural gaps in the week card (found in this re-run)

`week_matchup_2026-11-16.json` gives week 5 a 57.0% chance. Re-run in scratch with the same engine (`remaining()`, `cat_chances()`, `win_week_chance()`), the figure reproduces exactly and then moves as follows:

| assumption | P(win week 5) | starts, mine v theirs |
|---|---|---|
| The card as built: today's Out tags for the whole week, owner players outside the pool not counted | 57.0% | 36 v 40 |
| plus Mario Hezonja (an auto-row player, on the roster since 11-15) | 67.7% | 38 v 40 |
| plus ESPN's return dates (Jerome and Irving back 2026-11-18, `espn_injuries_2026-11-16.json`) | 87.4% | 43 v 40 |

- Gap A: `week_matchup.active()` reads only a team's pooled players, so a rostered auto-row player counts nothing in the week card, while the season simulator does simulate him (#246). The same class of gap #271 closed in the daily brief.
- Gap B: the week card applies a player's status of the run's day to every remaining day. An Out with an ESPN return date inside the week counts as out all week.
- The kit's weekly preview (simulator, statuses not applied) gives 75.9% for the same week.

These are reported, not fixed: a fix is a build and waits for the owner's word.

## 4. The Monday fit's proposals for the two constants (week 4, `fit_week4.json`, proposes only)

| constant | live | measured (weeks 1 to 4) | live within two SE |
|---|---|---|---|
| availability, 0.88 tier | 0.88 | 0.779 ± 0.007 (n 3,694) | no |
| availability, 0.75 tier | 0.75 | 0.559 ± 0.024 (n 438) | no |
| availability, 0.79 tier | 0.79 | 0.885 ± 0.063 (n 26) | yes |
| TEAM_WEEK_SHOCK | 0.06 | 0.107 ± 0.013 (48 team-weeks) | no |

## 5. Decisions for the owner (assessment only; nothing changes without a pick)

1. Availability tiers: keep the live values, fit them to the four graded weeks, or fit with a floor. Section 4 holds the evidence.
2. Prior strength on points, rebounds and assists: the 11-05 recency backtest found halving the prior better on all three, intervals excluding zero (`after-report-2026-11-05-recency.md`). The scheduled recency re-run for 11-16 had not reported when this was written.
3. The two week-card gaps in section 3.

One line, as the owner asked on 11-05: the turn-gate fix (kit PR #238) is still not mirrored in claude-core-skills.

## 6. Bounds

Out of scope by design: no line, constant, roster or code change; no new simulation beyond the week engine re-run in section 3.

In scope and unverified:
- The 11-05 and 11-13 columns are chat figures, not repository records.
- The split of the title move between its causes was not run.
- Both re-run inputs (Hezonja's auto row, ESPN's return dates) were taken as given; ESPN's dates are graded on 11-25.

## 7. Provenance

Scheduled re-run, session of 2026-11-16 (session model B), branch `claude/market-data-workorder-mnfi2b`. Records: season/daily 12964ec (`accuracy.json`, `calibration.json`, `calibration_daily.json`, `fits/fit_week4.json`, `briefs/*_2026-11-16.json`, `after-reports/redteam-2026-11-16-season/sweep.json`). Re-verify: `python3 scripts/redteam/run_attacks.py --check`; the scratch re-run script is described in section 3 and is not committed.
