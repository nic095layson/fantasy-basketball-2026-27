# Confidence, integrity and robustness after the session handoff (2026-11-16, evening)

Pull window: 2026-11-16 → 2026-11-16 (no pull: kit main 9cb7e23, deck main 1a47f81, the records branch season/daily at 92d0034, read only; no new simulation).

**Owner's request, verbatim (2026-11-16):** "Can you please conduct system and tool wide confidence %, integrity and robustness report after our session handoff?"

**Method up front.** Stated to the owner before any check ran. The baseline is `after-report-2026-11-16-confidence.md` (the week-5 re-run of that morning: main 8ab1d8d, records 12964ec), and the layers and scoring are the same: each score is a judgment anchored on the evidence beside it, only the evidence column is measured, and integrity and forecasting are never averaged. One layer is new: governance and the handoff itself. Only weeks 1 to 4 are graded (week 5 is graded on 2026-11-23), so a forecast score moves here only for a structural change made on 11-16, never for a new outcome. Checks run this evening, each on the commits named above:

| Check | Command | Result |
|---|---|---|
| Standing attacks | `python3 scripts/redteam/run_attacks.py --check` | PASS, 11 attacks on engine 1a47f81, CURRENT 11 |
| Constants registry | `python3 scripts/redteam/check_constants.py` | PASS, 53 registered = 53 live (declared_band 5, measured 10, settings 8, structural 6, uncalibrated 24) |
| Kit test suite | `python3 -m unittest discover -s scripts -p 'test_*.py'` | 1,259 tests OK (2 skipped), 163 s |
| Deck tests | each `arena/test_*.py` alone; `scripts/test_draft.py` | 6 of 6 modules OK; 67 of 67 cases |
| Hook parity | sha256 of every file in `hooks/`, kit main vs deck main vs the core-governance plugin | 16 of 16 identical in all three; doctrine block identical in both CLAUDE.md files |
| Plugin | version, `selftest-turn-gates.py W` from /tmp | 0.1.6; 6 of 6 |

A first run of the two red-team checks failed (STALE 11; registry 0.11 and 0.80 / 0.65 against live 0.06 and 0.88 / 0.75). Cause: the session's local deck checkout was still at c933f07, so the kit read the old engine through the sibling path. With the checkout at deck main 1a47f81 both pass. EVIDENCE of a checker fault, not an engine fault; the two rows that run wrote to `report/run-ledger.jsonl` were discarded, not committed.

**Verdict: the handoff left the system whole. The machinery holds at about 94% (simple mean of its five layers; 93.8 this morning), and every governance copy is identical. The forecasts rise from about 61% to about 63% (simple mean of six layers), for structural reasons only: the injury tiers moved toward the measured rates, and both week-card gaps of this morning are closed. The robustness picture is one FRAGILE constant (the risk tier: -2.6 / +1.4 points of title share) and one SENSITIVE one (the games shock: +1.6 / -1.1).**

Runner impact: none (a report; nothing the morning or afternoon runs execute changes).

Pool rows touched: none

## 1. Machinery: is it computing and recording correctly?

| layer | 11-16 am | now | EVIDENCE |
|---|---|---|---|
| Engine math | 98% | **98%** | attacks CURRENT 11 of 11 (10 of 11 this morning); 53 = 53 constants; kit 1,259 tests OK; deck modules 6 of 6, draft 67 of 67. A-3 was re-run on the old engine's reference file by mistake earlier in the day and corrected the same day (corrections log, 2026-11-16) |
| Data pulls and records | 94% | **94%** | `morning_2026-11-16.json`: PASS, 28 steps. `afternoon_report_2026-11-16.md`: 12 of 12 Flaim rosters, no retries, morning records sha256-checked untouched, "Nothing failed". One reporting slip: that report says it merged main "32af665 (through #278)", but its merge commit daef1c3 has parent 9cb7e23 (#282), so the run did use the tiers, the shock and the new hooks |
| Roster and injury status | 93% | **94%** | STATUS GATE PASS on the afternoon file (32 flagged rows, each with a dated receipt). The week card now applies ESPN return dates by day (#274, #275), which closes this morning's gap B. ESPN's dates themselves are graded on 2026-11-25 |
| Process and integrity | 96% | **95%** | 11 kit and 3 deck pull requests merged on 2026-11-16 (`git log --merges` on both mains); 7 corrections-log rows dated 2026-11-16, all caught before a decision rested on them. Three more rows were added in this pull request (section 5) |
| The deck page | 88% | **90%** | afternoon deck v87 built and published: 7 tabs, 0 page errors; its 723,576 built bytes are contained in the 724,122-byte live page |

## 2. Governance and the handoff (new layer)

| item | status | EVIDENCE |
|---|---|---|
| Plugin governs the session | PASS | core-governance 0.1.6; selftest 6 of 6; `turngate.cpython-313.pyc` written at session start, before the selftest |
| Hook copies | PASS | 16 of 16 files identical: kit main, deck main (#142 merged at pinned head 6bc7412), plugin |
| Scheduled tasks | PASS | `list_triggers`, both pages: the five old-Main tasks were recreated on this session (four one-shot reminders, the Monday review) and the old ones deleted; the Runner's two tasks unchanged; none left on the old Main or the archived tiers session |
| Open pull requests | PASS | kit: only #165 (never merge); deck: only #5 (July draft). #142, #143, #144, #279 to #282 merged |
| Runner under the new hooks | PASS | the afternoon run's checkout held the gate-fix hook files (its merge daef1c3 contains 4235127); its report shows no Stop block and no denied command. INFERENCE: whether the Runner's session reloaded the hook wiring, not only the scripts, was not checked |
| Disputed results | unchanged | `OPEN.md` unchanged since 4235127; X-1 to X-4 still DISPUTED |
| Score | **95%** | INFERENCE: the one blemish is a mislabel in a report, not a wrong record |

## 3. Forecasts: how far to trust what it predicts?

| layer | 11-16 am | now | EVIDENCE |
|---|---|---|---|
| Player lines | 80% | **80%** | unchanged records (`accuracy.json` weeks 1 to 4: points bias +8.7%, +9.1%, +1.7%). The minutes line went live on PTS, REB and AST on 11-16 and is ungraded until week 5 |
| Injury and availability discounts | 40% | **50%** | live tiers now 0.80 / 0.65 (#143, #279) against the measured 0.779 ± 0.007 and 0.559 ± 0.024 (`fit_week4.json`). Healthy is now 3 SE from the measurement (was 14); risk is 3.8 SE above it, by the owner's floor. Still the one FRAGILE constant |
| Daily lineup card | 85% | **85%** | unchanged records (`calibration_daily.json`: Brier skill positive all four weeks) |
| Weekly matchup forecast | 55% | **60%** | both gaps of this morning are closed (auto-row players counted, return dates by day: #274, #275), and the card's season edges now carry the shock's variance: card against simulator within 0.004 per category, was 0.08 (`after-report-2026-11-16-level-and-card.md`). No graded week yet, so held at 11-13's 60% until one is |
| Waiver pairs (relative) | 70% | **70%** | the pickup scan now prices a same-day swap (#275) and never offers a rostered player outside the pool (#278); not yet graded against outcomes |
| Title share as an absolute number | 35% | **35%** | three method changes in one day (minutes line, tiers, shock) moved the level; the model's weekly level runs 10% low (measured 1.103, left in the engine and measured every Monday). The sweep's baseline is 16.78 / 16.15 |

## 4. Robustness: the structural bands on the live engine

Sweep of 2026-11-16 (`report/after-reports/shock-fit-2026-11-16/sweep.json`): 6,000 seasons x seeds 2026 and 2027, MC SE 0.54, baseline within 3 SE of its 10k reference on both seeds; the attack runner reports it CURRENT on deck 1a47f81.

| constant | worst variants (title share points) | tier |
|---|---|---|
| weekly_availability | -2.6 (risk at the old 0.75) / +1.4 (risk at the unfloored fit 0.56) / -0.8 (healthy at the old 0.88) / -0.3 (healthy at the fit 0.78) | **FRAGILE** |
| TEAM_WEEK_SHOCK | +1.6 (no shock) / +0.7 (old 0.06) / -1.1 (0.13) | SENSITIVE |
| PCT_MIX_INFL | +0.5 / -0.8 | ROBUST |
| GAMES_PER_WEEK | -0.4 / +0.4 | ROBUST |
| BENCH_WEIGHT | 0.0 / 0.0 | ROBUST |

**weekly_availability is FRAGILE:** -2.6 (risk at the old 0.75) / +1.4 (risk at the unfloored fit 0.56); headline title share 16.5% ± 0.5 (MC) within that band. Sweep of 2026-11-16, engine 56230e9, CURRENT on 1a47f81.

24 of 53 registered constants are uncalibrated (each names the decision that will calibrate it in `scripts/redteam/constants_registry.json`).

## 5. Decisions for the owner (assessment only; nothing changes without a pick)

1. Done on the owner's pick ("With the report's PR"): three rows added to `report/corrections-log.md` in this pull request: the 14.0% title share (record: 13.84%), the "257th" rank quoted without saying it is this week's rank (season rank 14th), and the afternoon report's merge line.
2. The afternoon report's merge line: note only, or ask the Runner (from its own conversation) to quote its merge commit's parent instead of a cached name.
3. This report: merge the pull request or keep it as a draft.

## 6. Bounds

Out of scope by design: no line, constant, roster or code change; no simulation (the bands are the last sweep's, which the attack runner reports CURRENT); the library repository (claude-core-skills) was not read.

In scope and unverified:
- The deck's `scripts/test_gates.py`: ATTEMPTED-FAILED. Run twice this evening on deck main 1a47f81; both times it printed 32 passing cases, the last "F8 snapshot written with the 200 priced rows", and then produced nothing for more than 10 minutes, so it was stopped. No case failed; the remaining cases did not run. Deck PR #143 reported 54 of 54 on 9a009af. Other deck script tests: NOT-ATTEMPTED.
- Every score is a judgment; only its evidence column is measured. The "11-16 am" column is the morning report's.
- The week-card fixes (#274, #275, #282) are scored as fixed from their reports and merged tests; no week has been graded on them.

## 7. Provenance

Session of 2026-11-16 evening (session model A), the new Main session after the handoff; branch `claude/new-session-koi1jp`. Records: kit main 9cb7e23, deck main 1a47f81, season/daily 92d0034. Re-verify: `python3 scripts/redteam/run_attacks.py --check` and `python3 scripts/redteam/check_constants.py` with the deck checkout at its main; `python3 -m unittest discover -s scripts -p 'test_*.py'`; the hook parity loop compares `git show origin/main:hooks/<f> | sha256sum` in both repositories with the plugin's `scripts/<f>`.
