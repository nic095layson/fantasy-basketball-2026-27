# Why the title share fell 18.1% → 12.3% overnight (11-09 → 11-10), and the 11-10 confidence read (owner card "After-report PR"; report only, no code)

Pull window: 2026-11-09 → 2026-11-10 (no pull: data/league_state.json and data/season/pool_season.csv at 85c8f06 (11-09 morning) and 6da518c (11-10 morning), report/briefs/brief_2026-11-09.json and brief_2026-11-10.json, report/accuracy.json, report/calibration_daily.md, report/calibration.md, report/fits.md, report/league/league_2026-11-10.json, report/briefs/week_matchup_2026-11-10.json, report/after-reports/redteam-2026-11-09-season/sweep.json, all on season/daily, read only; kit main a417ee9, deck main 01483de).

**Method up front.** The 11-10 morning brief flagged "yesterday's brief said 18.1% ± 0.5 … a 5.8-point overnight drop is larger than the band. The cause is not traced." Method parameters, stated to the owner before the runs: the kit's own title simulator (`co_gm.rosters` + `co_gm.run_league_sim`, 10,000 seasons, seeds 2026 and 2027, owner seat 10), one input changed at a time, starting from the 11-09 morning inputs. The steps are: the roster build before and after the 11-09 change that simulates auto-row players (owner pick "Simulate them", PR #246); the 11-09 vs 11-10 season pool; the 11-09 vs 11-10 league state; and, inside the 11-10 state, Luka Dončić back on IL and Collin Gillespie back in place of Alex Caruso. Scratch scripts only; nothing written to the records. EVIDENCE marks what a run or a read showed; INFERENCE what is derived.

**Verdict: the drop is traced and neither half is an error. About half (−2.7) is the method change the owner picked on 11-09: five rival players on auto season lines are now simulated. About half (−2.6) is a rival getting healthier: Dončić came off IL on seat 3. The overnight line update (−0.4) and the owner's Caruso-for-Gillespie move (+0.1) are inside sampling noise. The brief's figure is reproducible to the hundredth on the 11-10 inputs.**

## 1. The decomposition (EVIDENCE: the runs)

| step | seed 2026 | seed 2027 | mean | change | evidence |
|---|---|---|---|---|---|
| 11-09 brief as published | 17.84 | 18.27 | 18.06 | | brief_2026-11-09.json |
| 11-09 state, 11-09 pool, roster build before B2 | 18.40 | 17.66 | 18.03 | reproduces the brief (within MC) | run |
| same, roster build after B2 (5 auto-row players simulated: Meleek Thomas seat 1, Nolan Traore seat 5, Danny Wolf seat 7, Morez Johnson Jr. seat 9, Mario Hezonja seat 11) | 15.25 | 15.43 | 15.34 | **−2.69** (−2.87 was measured before the merge) | run |
| + 11-10 season pool | 14.63 | 15.21 | 14.92 | −0.42 (noise: SE of a difference ≈ 0.7) | run |
| + 11-10 league state = the 11-10 brief | 12.32 | 12.23 | 12.28 | **−2.64** | run; brief_2026-11-10.json 12.32 / 12.23 |
| 11-10 state with Dončić set back to IL | 14.82 | 15.36 | 15.09 | Dončić alone: **−2.81** | run |
| 11-10 state with Gillespie back for Caruso | 12.41 | 12.28 | 12.34 | owner's move: +0.06 (noise) | run |

The sum is −2.69 − 0.42 − 2.64 = −5.75, matching 18.03 → 12.28. Seat 3 had Dončić on IL in the 11-09 morning state, on PG in the 11-09 afternoon state, and on BN on 11-10 (data/league_state.json at 85c8f06, 4b24a83 and 6da518c).

One instrument note (EVIDENCE): `run_league_sim` reads `SEASON_POOL` from the environment when it runs, not from the pool loaded earlier. A first pass of this trace set the variable twice before running, so two of its rows ran on the same pool. Those rows were discarded and re-run one pool per process. The table holds only the re-runs.

## 2. Two checks on the brief's waiver figure (EVIDENCE: the runs)

| pair on the 11-10 rosters | change in title points | evidence |
|---|---|---|
| add John Collins, drop Alex Caruso | +3.35 (brief: +3.36) | run; brief waiver_top |
| add John Collins, drop Kris Dunn (the owner's planned second move) | +3.44 | run |

Both sit inside the FRAGILE band below.

## 3. The 11-10 confidence read, by layer (EVIDENCE: the records named)

| layer | evidence | read |
|---|---|---|
| Engine integrity | Kit suite 854 OK (2 skipped); CONSTANTS CHECK PASS (49 = 49 live, deck 01483de); ATTACKS CHECK PASS (9 current, 1 unfingerprinted); morning PASS, 20 steps; the brief reproduced in §1–2 | high |
| Daily week card | Brier 0.034 / 0.145 / 0.124 vs the lead to date 0.174 / 0.294 / 0.155 (skill +0.140 / +0.149 / +0.030). Reliability bin 0.4–0.6: mean P 0.51, hit rate 0.88 (16 forecasts) | high; cautious on close categories |
| Pre-week P(win) | Our matchups, Brier: 0.367 / 0.180 / 0.023. League, week 3 only: flat 0.222, real games 0.191 | medium-low (small sample) |
| Player lines | In-season line, week 3: PTS +9.1%, REB +6.4%, STL +12.5%, BLK +8.0%; PTS rank correlation 0.79. Minutes candidate PTS +8.2%, MAE 3.30 vs 3.39 | medium: order right, level high |
| Availability | Through week 3: healthy tier live 0.88, measured 0.793 ± 0.008 (n 2,736); risk tier live 0.75, measured 0.561 ± 0.027 (n 326). Live is outside 2 SE for both, every week | low |
| Shared weekly shock | Live 0.06, measured 0.1117 ± 0.0153 through week 3 | low-medium |
| Title share | 12.3% ± 0.5 (MC); band below; playoffs 96.4% | low as a point |
| League table | Yahoo W-L-T matches the kit's finished weeks for 12 teams; seat 10 all-play 0.542 (#6), standings 17-10 (#2) | high |
| Decision grading | 0 graded; first window closes 2026-11-17 | not yet measured |

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds (season sweep 2026-11-09, engine 01483de, 6,000 seasons × 2 seeds). TEAM_WEEK_SHOCK is SENSITIVE (−1.4 at 0.12).

INFERENCE, not a forecast: the measured risk-tier share (0.56) sits beyond the sweep's harsh variant (0.65, +2.9 for seat 10), and the measured shock (0.11) sits near the doubled variant (0.12, −1.4). The two point in opposite directions on seat 10's title share. The constants fit (`fit_constants.py`) needs 4 finished weeks, and week 4 ends 2026-11-15.

## 4. Bounds

- Out of scope by design: no code, constant, line, tag or roster changed. Whether the brief's overnight flag should name code merges as a candidate cause is an owner decision (below).
- In scope and unverified: the auto-row lines behind the −2.69 rest on 5–11 games each (11-10 morning report: Meleek Thomas 8, Nolan Traore 10, Morez Johnson Jr. 10, Mario Hezonja 11, Danny Wolf 5 games). How small-sample lines behave was not graded here (did not check). Three sources disagree on week-4 games left (kit 38/37, live matchup 36/34, Yahoo games_remaining 26/37); not traced (did not check).
- The Dončić effect assumes the simulator's season-long availability for him. His health is unverifiable ahead of time.

## 5. Next steps (owner decisions)

1. **Leave the brief as is (Recommended).** The trace is on record here, and the flag did its job: it named a drop larger than the band.
2. A one-line addition to the overnight flag naming kit merges since the last brief as a candidate cause (code, a test and an after-report, on your go).

Runner impact: none. No script, step or prompt the Runner uses changed. The Runner prompt stays the owner's paste.

## Fired

plan-gate (loaded; compact plan table shown before the runs) · adversarial-verify (loaded before delivery).

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
