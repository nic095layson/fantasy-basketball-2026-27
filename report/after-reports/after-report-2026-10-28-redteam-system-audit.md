# System red-team audit: operations, integrity, data sourcing, forecasting — 2026-10-28

Pull window: 2026-10-28 → 2026-10-28 (no pull: read-only audit of kit main 848a4ef, deck main 55d8e3f, season/daily 2f80fb0, and the runner's two stored prompts read 23:5xZ).

**Method up front.** Owner 2026-10-28: "conduct a critical red team audit of system operations, procedural and integrity checks … data sourcing validation … computations effective/competitive. Provide after report and confirmation all systems calibrated."
- Every standing instrument was run on the current heads.
- Every pinned receipt the newest records cite was re-hashed against its file.
- The runner's stored prompts were read back.
- Forecasts and lines were graded on every week on file (week 1; week 2 is in progress).
- No new simulation was run, and nothing was fixed. Findings go to the owner as options.

EVIDENCE marks what a run or read showed; INFERENCE marks what is derived.

**Verdict: operations and integrity checks all PASS. "All systems calibrated" does not hold yet, and is not expected to.** Two constants that move the title odds most are still hand-set and FRAGILE, and their measured fit proposes from week 4. Four findings below are open.

## 1. Standing checks (EVIDENCE)

| check | result |
|---|---|
| constants registry vs live engine | PASS — 39 registered = 39 live (deck 55d8e3f); declared_band 5, measured 7, settings 8, structural 4, uncalibrated 15 |
| attack list vs records and engine | PASS — 9 attacks; CURRENT 5, UNFINGERPRINTED 4 (§3 F2) |
| season sweep (bands) currency | CURRENT — sweep engine cbfb422 = the last engine change (arena/patches.py) |
| kit test suite | 693 tests OK (2 skipped) |
| gates.json on main | GATES VERIFY: PASS |
| turn-gate hooks (merged by another session, #222/#223; deck #137/#138) | selftest 33 passed, 0 failed; they touch hooks, settings and CLAUDE.md only, no engine or data |
| runner prompts | both byte-equal to their verified files (morning 15,081 bytes, updated 18:53Z; afternoon 6,231 bytes, updated 23:07Z) |
| last runs | morning 10-28: 16 of 16 steps PASS (MANAGER LOG HALT from team 5's 502, back-filled 264d0b6); afternoon 10-28: Flaim 12/12, no retries, STATUS GATE PASS |

## 2. Data sourcing (EVIDENCE)

| record | check | result |
|---|---|---|
| league_state.json (10-28 pm) | sha256 of its two cited sources (pull_2026-10-28.json, rosters_2026-10-28.transcribed.csv) | both match |
| status files 10-27, 10-28 | status_feed --check | PASS (32 and 33 flagged rows, each with a dated receipt) |
| ESPN injury pin | data/status/espn_injuries_2026-10-28.json | present (the afternoon run, first day of the #216 pin) |
| records tree | commit_check | PASS — clean under data/, report/ |
| deck records 10-26..10-28 | re-hash every input | 10 of 12 match; status and league_state differ (§3 F3) |

## 3. Findings (open, owner decisions)

- **F1. Decision robustness is a draft-day record (EVIDENCE).**
  - A-6 last ran on engine 259c630 against draft-day rosters.
  - No in-season recommendation (the waiver pairs, today's Portis add) has been re-run under the sweep's variants.
  - The brief quotes the FRAGILE bands beside each title figure, but it does not check whether a recommendation flips under them. INFERENCE: a pair whose gain is smaller than the band could reverse.
- **F2. Four attack records carry no engine fingerprint (EVIDENCE).**
  - A-1 to A-4 (10-19: category math, kit/deck join, card vs simulator, integer ties).
  - The checker passes them as UNFINGERPRINTED, so nothing proves they still hold on today's engine.
- **F3. The 3 PM run overwrites two files the 5 AM deck record fingerprints (EVIDENCE).**
  - `status_<date>.json` and `league_state.json` are rewritten in place by the afternoon run.
  - The morning deck's input hashes for those two no longer match the branch tip on 10-26, 10-27 and 10-28.
  - The morning bytes survive in git history at the morning commit, so nothing is lost, but the record cannot be re-checked from the tip alone.
- **F4. Week-1 accuracy: preseason lines ran high, and two hand-set tiers ran generous (EVIDENCE, report/accuracy.json week 1, 261 players with 2+ games).**

| measure | projected | actual | note |
|---|---|---|---|
| PTS per game | 13.50 | 11.95 | +13.0% high; rank correlation 0.77 |
| AST | 3.07 | 2.73 | +12.6% high |
| 3PM | 1.49 | 1.29 | +15.0% high |
| REB | 4.89 | 4.57 | +7.1% high |
| STL / TO | 0.90 / 1.57 | 0.96 / 1.68 | −5.5% / −6.3% (low) |
| FG% / FT% | .478 / .792 | .460 / .777 | high |
| healthy tier (sim) | 0.88 | 0.83 of 809 team games | generous |
| risk tier (sim) | 0.75 | 0.57 of 96 team games | generous |
| owner matchup, week 1 | P(win) 0.61, 4.94 expected categories | 3 categories won | one matchup |
| category forecast Brier | — | 0.253 vs coin flip 0.25 | no skill shown yet (9 categories, one week) |
| daily forecasts | — | Brier 0.034 vs baseline 0.174 (36 forecasts) | skill |

INFERENCE: a near-uniform high bias moves every player together, so rankings (and z-scores) hold better than raw totals, as the 0.73–0.77 rank correlations on PTS/REB/AST show. The in-season blend already pulls each line toward his games: PTS is 56% his own after 15 games. One week is a small sample. The Monday fit proposes the two FRAGILE constants from week 4.

## 4. Calibration status (EVIDENCE: the registry)

| class | constants | status |
|---|---|---|
| FRAGILE, hand-set, banded | TEAM_WEEK_SHOCK, weekly_availability | the Monday fit proposes from week 4 (D-PM-1, D-PM-4) |
| banded, not fragile | BENCH_WEIGHT, PCT_MIX_INFL, GAMES_PER_WEEK | deck N1 refit |
| uncalibrated, in-season effect | hoops.availability (D-PM-4), status tiers and 7-day line (D-WS-1/2), SEASON_GAMES (D-IS-1), minutes-line knobs (D-ML-1) | each carries its decision |
| uncalibrated, draft-only | CV, GRAD_K/SCALE, MKT_W/PIN, PAIR_* | none needed in-season |

Every title share the system quotes carries the standing structural band (season sweep 2026-10-26, real schedule):
- **TEAM_WEEK_SHOCK is FRAGILE:** +2.7 (no shared games shock (0.0)) / -4.2 (shared games shock doubled (0.12)).
- **weekly_availability is FRAGILE:** -5.4 (no in-sim injury discount (risk 0.88 like healthy)) / +3.7 (harsher risk tier (0.65)) / +0.4 (healthy players play 0.95 of games) / -0.5 (healthy players play 0.80 of games).

## 5. Bounds

**Out of scope by design.**
- No simulation was re-run, and no fix was made.
- calibration_league*.json are absent on season/daily (INFERENCE: expected; the Sunday forecast step's first run since build 5 is 11-01).

**In scope and unverified.**
- F1 and F2 are not re-run (owner decisions).
- The 10-29 runs are not yet seen: the morning at 12:02Z, the afternoon refresh at 22:03Z, both with scheduled checks.

Runner impact: none (read-only audit; a fix to F3 would be a prompt edit and would follow rule 11).

## Watchlist

- 10-29 14:30Z and 22:45Z check-ins (Bamba role; the first afternoon refresh).
- The week-4 Monday fit (about 11-16): its proposals for the two FRAGILE constants.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| F1 decision robustness in-season | **OPEN**, owner decision | §3 |
| F2 unfingerprinted attacks | **OPEN**, owner decision | §3 |
| F3 afternoon overwrites morning-pinned files | **OPEN**, owner decision | §3 |
| F4 week-1 bias and generous tiers | **WATCH**, the week-4 fit | §3, §4 |

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
