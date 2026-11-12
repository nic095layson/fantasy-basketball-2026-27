# System-wide calibration, validation, red team and integrity test, with Runner adoption (owner 2026-11-12)

Pull window: 2026-10-17 → 2026-11-12 (no pull: kit main 94117d8, the records branch season/daily at db51bfb, the published deck page and the scheduler's task list, read only; one season sweep and one morning dry run in a scratch copy, nothing written to the records).

**Owner's request, verbatim:** "Conduct system wide calibration, validation, red team and integrity test, along with Runner adoption and comparability. Provide after report".

**What was analyzed.** The kit at main 94117d8, after the five merges of 2026-11-11 and 11-12 (#261 Draft Check, #262 council fixes, #263 playbook, #264 header alignment, #265 punt view, trending-up card and threes candidate); the records branch at db51bfb (this morning's Runner commit c14c1ec plus the session's afternoon refresh); the deck engine at 01483de; the published deck (Version 78).

**Method up front.** Five phases, parameters stated to the owner before the runs. (1) Validation: the full suite and the gates on main. (2) Calibration: the records as they stand, no refitting. (3) Red team: the constants registry against live code, the attack list against the live engine, the bands on today's brief, and a fresh season sweep on today's rosters with the 2026-11-09 sweep's settings (6,000 seasons, seeds 2026 and 2027, one constant at a time, tiers read only with the baseline inside 3 standard errors of the 10,000-season reference). (4) Integrity: every checksum pinned in today's two deck records against the committed file, the run ledger, the published page against the built file. (5) Runner adoption: a scratch copy of season/daily merged with main, `morning.py --date 2026-11-12 --no-fetch`, the Sunday snapshot and the Monday card render, and the scheduler's last-run records. EVIDENCE marks what a run or a read showed; INFERENCE what is derived.

**Verdict: the system is sound and the Runner will adopt the last five merges without a prompt change. 1,174 tests pass, the gates pass, the registry and attack list match the live engine, the published deck is the built file, and every morning step passes on main in a dry run. Three findings need the owner's eye, none of them a failure: the per-manager moves file is rewritten after the morning deck has pinned it; the sweep printed on the brief is three days old and one constant has since moved a tier; and the attack list's fingerprint does not cover the kit's own scripts.**

Runner impact: none — this report adds documents only. The five merges were each code-only or documents; section 5 confirms them together on the Runner's sequence.

## 1. Validation

| check | result (EVIDENCE) |
|---|---|
| Full suite on main 94117d8 | 1,174 tests, OK, 2 skipped, 164 s |
| `gates.py --verify` on main | PASS, inputs unchanged |
| Records branch against main | no script differs once main is merged (`git diff origin/main...origin/season/daily -- scripts` is empty; the scratch merge was automatic) |

## 2. Calibration (records as they stand)

**Player lines, bias and typical miss per game** (`report/accuracy.json`, players with 2+ games in the week):

| week | players | line | PTS bias / miss | REB | AST | 3PM |
|---|---|---|---|---|---|---|
| 1 | 261 | draft-day | +13.0% / 3.50 | +7.1% / 1.29 | +12.6% / 1.09 | +15.0% / 0.63 |
| 2 | 253 | in-season | +8.7% / 3.46 | +3.8% / 1.35 | +2.9% / 1.02 | +3.3% / 0.67 |
| 2 | 253 | minutes candidate | +7.6% / 3.34 | +2.7% / 1.31 | +1.7% / 1.00 | +2.0% / 0.66 |
| 3 | 258 | in-season | +9.1% / 3.39 | +6.4% / 1.27 | +4.8% / 0.98 | +9.1% / 0.61 |
| 3 | 258 | minutes candidate | +8.2% / 3.30 | +5.3% / 1.23 | +3.7% / 0.96 | +7.7% / 0.61 |

- The lines still run high: about 9% on points. The minutes candidate has beaten the in-season line on points, rebounds and assists in both graded weeks (2 of 2; its switch rule needs 3 of 4).
- **Availability** (share of team games played, weeks 1 to 3 pooled): the 0.88 tier played 2,171 of 2,736, **0.79**; the 0.75 tier 183 of 326, **0.56**. Both below what the simulator assumes. The decision is on the 11-16 agenda.
- **Daily win chances** (`calibration_daily.json`): miss score 0.034, 0.145, 0.124 in weeks 1 to 3 against the scoreboard's 0.174, 0.294, 0.155; better than the scoreboard in all three, by 0.140, 0.149 and 0.030 (36, 63 and 63 forecasts).
- **League matchups** (week 3, 6 matchups): flat-games forecast 0.222, real-games forecast 0.191. One week; the switch rule needs four.
- **Advice against the owner's moves:** no add/drop call has closed its window (first on 11-17). Lineup ledger: 7 days, 6 agreed, 1 graded pair.
- **Title watch, this morning:** 20.2% against 16.1% on 11-11, +4.2 against a band of ±0.75, flagged MOVED by the step built to flag it.

## 3. Red team

| check | result (EVIDENCE) |
|---|---|
| Constants registry against live code | PASS: 51 registered = 51 live; declared band 5, measured 7, settings 8, structural 6, uncalibrated 25 |
| Attack list against the live engine | PASS: 10 attacks on engine 01483de, simulator aa470f8; 9 CURRENT, 1 UNFINGERPRINTED (A-6, allowed and named) |
| Bands on today's brief | quoted, from the 2026-11-09 sweep |
| Fresh season sweep, today's rosters | baseline 19.52 / 19.60, inside 3 standard errors of the 10,000-season reference (19.30 / 19.44) on both seeds; record `audit-2026-11-12/sweep_2026-11-12.json` |

**The fresh sweep beside the one on the brief** (mean shift in title points over the two seeds; Monte-Carlo error 0.54):

| constant | variant | 11-09 (on the brief) | 11-12 (fresh) | tier 11-09 to 11-12 |
|---|---|---|---|---|
| weekly_availability | no injury discount | −4.8 | −4.34 | FRAGILE to FRAGILE |
| weekly_availability | harsher risk tier (0.65) | +2.9 | +2.34 | |
| TEAM_WEEK_SHOCK | none / doubled | — | +1.12 / −1.51 | SENSITIVE to SENSITIVE |
| GAMES_PER_WEEK | 3.0 / 4.0 a week | — | −1.14 / +0.32 | ROBUST to **SENSITIVE** |
| PCT_MIX_INFL | 1.0 / 1.30 | — | +0.96 / −0.79 | ROBUST to ROBUST (0.04 under the line) |
| BENCH_WEIGHT | 0.50 / 1.00 | — | 0.00 / 0.00 | ROBUST to ROBUST |

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds. That is the 2026-11-09 sweep the brief quotes; on today's rosters the same constant reads −4.34 / +2.34 around a baseline of 19.56%.

**Decision robustness.** Today's recommendation is "no pair today", so there is no verdict to flip. Yesterday's and today's session findings on who leaves when the injured players return (dropping PJ Washington costs 2 to 3 title points) were not re-run under the sweep's variants: NOT-ATTEMPTED, by choice; it would be about 26 more simulator runs. It is the one figure the owner is likely to act on that has no structural band.

## 4. Integrity

| check | result (EVIDENCE) |
|---|---|
| Afternoon deck record's pinned inputs against the committed files | 21 of 21 match |
| Morning deck record's pinned inputs | 20 of 21 match; `data/managers/transactions.json` does not (finding F1) |
| Published page against the built file | the 670,747 built bytes of `deck_2026-11-12_pm.html` (sha256 c318ea963bea) are inside the live page, Version 78 |
| Run ledger, 11-12 | the 22 morning steps and one sub-step row, all PASS, 13:06:04 to 13:09:08 UTC; 2 afternoon rows PASS |

A first pass of the pin check reported four mismatches. It had read the scratch folder two seconds after the dry run began rewriting it; the check was the faulty part. Re-run against the committed objects, it gives the table above.

## 5. Runner adoption

EVIDENCE, scratch copy of season/daily merged with main (record `audit-2026-11-12/morning_dry_run.json`):

- `morning.py --date 2026-11-12 --no-fetch`: **MORNING: PASS, 19 steps** (the four fetch steps are skipped by `--no-fetch`; with them the sequence is 23, one more than this morning's 22). The new step reads `THREES LINE: PASS — 342 players, 233 split, 109 unsplit`. Ledger steps re-run cleanly: "already recorded".
- Sunday snapshot: writes `lines_week5.csv`, `lines_week5_mt.csv` and `lines_week5_3s.csv`. Monday card: renders with the threes table.
- The deck built in the dry run: 0 page errors, 7 tabs (Today, Trade Analyzer, Free Agents, Board, Draft Check, Week, League), 9 chips on the Board and on the Trade Analyzer, 16 free agents on the Trending Up card.
- Scheduler: the afternoon runner last ran 2026-11-11 23:03 UTC, SUCCEEDED; the morning watchdog 2026-11-12 14:40 UTC and the afternoon watchdog 2026-11-11 23:45 UTC, both SUCCEEDED. The afternoon runner's stored prompt merges main before it builds, so today's 23:03 UTC run is the first to publish the new deck.
- The dry run's title figure is 19.4% against this morning's 20.2%: it ran on the afternoon's rosters (one league move since the morning), same seeds.

One open item on the Runner's side, unchanged: the owner has the text to rename "Movers" to "Draft Check" in the Runner prompt's tab list (given 11-11). The prompt lives in the Runner's conversation and was not readable from here beyond the afternoon task's stored text, which names no tabs.

## 6. Findings

| # | finding | evidence | effect | tier |
|---|---|---|---|---|
| F1 | The per-manager moves file is rewritten after the morning deck has pinned it. `manager_log.py` runs outside `morning.py` and leaves no ledger row. | The morning record's `league_tx` pin does not match the file in the same commit (c14c1ec); the ledger has no manager-log row on 11-12; this is the first morning the pin exists. | The morning deck, brief and week card read yesterday's moves file. This morning's adds count was still right (3). | HIGHLY RECOMMEND a fix |
| F2 | The brief's structural band is three days old and one constant has moved a tier since. | Section 3's table: GAMES_PER_WEEK ROBUST to SENSITIVE; the FRAGILE band −4.8 / +2.9 to −4.34 / +2.34. The brief labels the 11-09 sweep "current rosters". | The quoted band is slightly wide today; the label overstates its freshness. | NICE TO HAVE |
| F3 | The attack list's fingerprint follows the deck engine, not the kit's scripts. | A-10 (IL-return known answers) is dated 10-31 and reads CURRENT; `il_return.py` changed on 11-11 (two worlds retired). Its unit tests were updated then and pass. | An attack record can read CURRENT after the kit script it attacked has changed. | NICE TO HAVE |
| F4 | The drop-order finding has no structural band. | Section 3, decision robustness. | The figure most likely to drive a roster decision carries sampling error only. | NICE TO HAVE, before the first cut |

What would demote F1: a ledger row or a record showing the moves file is written before the brief. None was found.

## 7. Bounds

**Out of scope by design:** refitting any constant; the deck repository's own draft tools; the Solo-Leveling and briefing tasks that share the scheduler; trade evaluation (owner veto 2026-10-20).

**In scope and unverified:**
- The Runner's morning prompt text: NOT-ATTEMPTED from here; it lives in the Runner's own conversation. The dry run tests the code path it calls, not its wording.
- The four fetch steps on today's main: NOT-ATTEMPTED in the dry run (`--no-fetch`); they are unchanged by the five merges (`git diff 47a094e 94117d8 -- scripts` names none of `league_live.py`, `box_pull.py`, the matchup or the transactions scripts).
- F4's band: NOT-ATTEMPTED, by choice.
- Calibration rests on three graded weeks; every rate above is on that sample.

## 8. Next steps (owner decisions)

1. F1: move the manager-log step into `morning.py` ahead of the brief, with a ledger row (recommended), or leave it and drop the pin.
2. F2: re-run the season sweep in the Monday run each week (it ran on 11-02 and 11-09), or on every roster change.
3. F3: add the kit scripts' commit to the attack fingerprint.
4. F4: run the drop pairs under the sweep's variants before Haliburton is activated.
5. Already scheduled, unchanged: availability and prior-strength decisions on 11-16; the Monday upkeep review.

## 9. Provenance

Produced in the owner's working session on 2026-11-12 (session model A). Supporting records in `report/after-reports/audit-2026-11-12/`: `sweep_2026-11-12.json`, `attacks.json`, `morning_dry_run.json`. Re-verify: `python3 scripts/redteam/check_constants.py`; `python3 scripts/redteam/run_attacks.py --check`; `python3 scripts/gates.py --verify`; the pin check is `git show origin/season/daily:<path> | sha256sum` against `report/season/deck_record_2026-11-12.json`.
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
