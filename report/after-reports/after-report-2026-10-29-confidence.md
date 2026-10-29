# Confidence by layer, in season — 2026-10-29 (baseline for the week 5, 10 and 15 re-runs)

Pull window: 2026-10-20 → 2026-10-29 (no new pull: week 1 graded records and this week's runs on season/daily 934de05, kit main 14b27d4, deck main 55d8e3f, all read only).

**Method up front.** Owner 2026-10-29: "Before you've given me a confidence % report on the state of this system and tool. Can you provide me an update as of today?", then "create after-report for repo, and run this report again on the Monday morning run of Week 5, 10 and 15".
- Same shape as `after-report-2026-10-09-confidence.md`: one score per layer, each beside the record behind it.
- Integrity (is it computing and recording correctly) and forecasting (how far to trust what it predicts) are scored separately and never averaged, as on 10-14.
- The scores are judgments anchored on the evidence column. Only the evidence column is measured.
- EVIDENCE marks what a record shows; INFERENCE marks the score drawn from it.

**Verdict: the machinery is sound (about 95%); the forecasts are soft (about 55%) after one graded week, mostly from generous preseason lines and generous injury discounts.**

## 1. Machinery: is it computing and recording correctly?

| layer | 10-14 (draft lock) | 10-29 | EVIDENCE |
|---|---|---|---|
| Engine math | 99% | **99%** | A-1 re-run on deck 55d8e3f: z and availability diffs 0.0; A-9 separate-attacker match on record; attack check CURRENT 8 of 9; constants registry 39 = 39 live (`after-report-2026-10-29-redteam-followups.md` §2, `after-report-2026-10-28-redteam-system-audit.md` §1) |
| Data pulls and records | 97% | **94%** | 10-29 morning: Flaim 31 of 31 calls, no retries; 16-step MORNING PASS. LEAGUE PAIRINGS and LEAGUE TABLE failed on team 5's rename (fixed, #226); the afternoon `_pm` path runs for the first time 10-29 (`after-report-2026-10-29-morning-run.md` on season/daily) |
| Roster and injury status | 88% | **95%** | STATUS GATE PASS, 26 flagged rows each with a dated receipt; the waiver gate set aside 5 Out players with Yahoo and ESPN both read; one runner misstatement on 10-29 caught and corrected the same morning |
| Process and integrity | 97% | **96%** | gates PASS on every merge (#224 to #228); both runner prompts read back byte-equal (afternoon pm_v4, 6,648 bytes); the 3 PM overwrite of morning-hashed files fixed (#225) |
| The deck page | — | **85%** | every build renders, 0 page errors; two display defects found by the owner this week (#227, #228), fixed; the League tab is empty on 10-29 until the next morning run |

## 2. Forecasts: how far to trust what it predicts?

| layer | 10-14 | 10-29 | EVIDENCE |
|---|---|---|---|
| Player lines | 97.8%* | **70%** | week 1, 261 players with 2+ games (`report/accuracy.json`): points per game projected 13.50 against 11.95 actual (+13.0% high), rank correlation 0.77; assists +12.6%, threes +15.0%, rebounds +7.1%; steals and turnovers low |
| Injury and availability discounts | — | **50%** | healthy tier: 0.83 of 809 team games played against 0.88 assumed; risk tier: 0.57 of 96 against 0.75; the IL rule (D-IS-8) alone moves the owner's title share 15.6% to 28.5% (`after-report-2026-10-29-il-rule-and-team-key.md`) |
| Daily lineup card | — | **85%** | Brier 0.034 against a baseline 0.174 over 36 daily forecasts (`report/calibration_daily.json`, week 1) |
| Weekly matchup forecast | — | **50%** | category Brier 0.253 against a coin flip's 0.25 (week 1, nine categories, one matchup); P(win) 0.61 and the week was lost, 3 categories to 6 |
| Waiver pairs (relative) | — | **70%** | the top pair (Cameron Johnson for Collin Gillespie) positive under all 13 sweep configurations; cats/week and the season simulator disagreed on two other adds (Tobias Harris, Jalen Smith) (`after-report-2026-10-29-redteam-followups.md` §1) |
| Title share as an absolute number | 40% | **35%** | two FRAGILE constants (bands below); the IL rule's 12.9-point range; a 14th active player adds about +21 in the simulator (`after-report-2026-10-29-il-rule-and-team-key.md` §1) |

\*The 10-14 figure measured agreement with five outside projections, not accuracy (`after-report-2026-10-14-integrity.md` §6). 10-29's 70% is the first score with real games behind it.

INFERENCE: the integrity layers moved little and stay high; the forecast layers are new or fell, because the season now grades them. A near-uniform high bias moves every player together, so rankings hold better than totals.

## 3. Bands quoted

Every title share above carries the standing structural band (season sweep 2026-10-26, real schedule):
- **TEAM_WEEK_SHOCK is FRAGILE:** +2.7 (no shared games shock (0.0)) / -4.2 (shared games shock doubled (0.12)).
- **weekly_availability is FRAGILE:** -5.4 (no in-sim injury discount (risk 0.88 like healthy)) / +3.7 (harsher risk tier (0.65)) / +0.4 (healthy players play 0.95 of games) / -0.5 (healthy players play 0.80 of games).

## 4. The re-runs (owner 2026-10-29)

| re-run | Monday | data by then | what should move |
|---|---|---|---|
| Week 5 | 2026-11-16 | 4 graded weeks | the Monday fit's first proposals for the two FRAGILE constants; the lines' high bias, as the blend weights games more |
| Week 10 | 2026-12-28 | 9 graded weeks | the weekly matchup forecast's skill (enough weeks to read a Brier against chance) |
| Week 15 | 2027-02-01 | 14 graded weeks | every layer on a full half-season; the title share against the standings |

Each re-run uses this report's layers and scoring, puts the new score beside 10-29 and the previous re-run, and cites the records added since.

Runner impact: none (a report; the re-runs fire into the main session, not the runner).

## Bounds

**Out of scope by design.** No line, tag, constant or roster change; no new simulation for this report.

**In scope and unverified.** One graded week is a small sample for every forecast layer; the scores are the starting point the re-runs are measured against, not a verdict.

## Watchlist

- 2026-11-16, 2026-12-28, 2027-02-01: the three re-runs.
- The week-4 Monday fit (2026-11-16): the largest expected lift to the forecast layers.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| Confidence by layer, in season | **BASELINE** recorded | §1–2 |
| Re-runs at weeks 5, 10, 15 | **SCHEDULED** | §4 |

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
