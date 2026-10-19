# After-report — the standing red team: a constants registry with drift check, an assumption sweep whose FRAGILE bands every report must quote, and a numbered attack list, all as gates

**Owner request (2026-10-19):** after the post-mortem's explanation of what the red team caught and why it went undiscovered, the owner wrote "Proceed" to the two-PR proposal: PR 1, make the red team standing in the kit (this report); PR 2, a red-team skill for the skills library (separate).

**What was built.** `scripts/redteam/`: a registry of every judgment constant the engine runs on (`constants_registry.json`, 28 entries) with a drift check against the live deck (`check_constants.py`); an assumption sweep that reads the registry's declared bands and runs them one at a time on the league's final rosters (`sweep.py`), tiering each constant by the post-mortem rule; a bands check that refuses any report that does not quote every FRAGILE band (`check_bands.py`); and a numbered attack list (`attacks.json`, 8 attacks) with a runner that refuses a missing record or one made on a different engine than the live deck (`run_attacks.py`). `scripts/gates.py` gained `--redteam SWEEP_JSON`, which adds the three as gates to `gates.json`. Every piece landed red-first: `test_constants_registry.py` 10 tests OK, `test_redteam_sweep.py` 10 tests OK, `test_redteam_attacks.py` 7 tests OK, `test_gates_runner.py` 12 tests OK. Engine: deck `259c630`. No engine constant, line, tag or price changed.

**Headline.** The sweep on the shipped engine (6,000 seasons per variant on seeds 2026 and 2027, Monte-Carlo SE 0.54 points) finds 1 FRAGILE constant (TEAM_WEEK_SHOCK), 2 SENSITIVE (PCT_MIX_INFL, weekly_availability) and 3 ROBUST (BENCH_WEIGHT, CV, GAMES_PER_WEEK) among the 6 constants with a declared band. The baseline title share is 21.43 / 21.68 against the 10,000-season reference 21.10 / 21.33 (within 3 SE on 2 of 2 seeds). The registry check passes: 28 registered equals 28 live, 7 constants uncalibrated and each named with its decision, 6 with a band, 4 measured, 7 from the league settings, 4 structural. The attack list carries the post-mortem's six attacks and the two new ones: 4 CURRENT on the live engine, 4 UNFINGERPRINTED (their records carry no engine commit; named on the watchlist), 0 STALE, 0 MISSING. From this PR on, a title figure in a report that does not quote the FRAGILE bands fails its gates.

Pull window: 2026-10-19 → 2026-10-19 (build only; no roster pull, no line change).

## 1. Roster changes

None. No pull was made today and no line, tag, price or engine constant changed; the registry records the live values and the sweep patches them only inside its own worker processes.

## 2. The constants registry and the drift check

EVIDENCE: `scripts/redteam/constants_registry.json`, `scripts/redteam/check_constants.py --json` → `constants.json` (verdict PASS, engine `259c630`). The checker imports the live deck modules, reads every module-level constant of `arena.py` and `hoops.py` that the engine uses (path, alias and persona tables excluded by name), probes the two availability-tier functions with one note per tier, and reads the 3.5 games-per-week literal out of `team_week_model`'s source; a constant that is live but unregistered, registered but gone, or whose value differs, fails. Each entry states what the constant is for and what vouches for it.

| status | meaning | count | constants |
|---|---|---|---|
| settings | read from the league settings page (`data/league_settings.json`) | 7 | TEAMS, ROUNDS, WEEKS, PLAYOFF_TEAMS, LINEUP_SLOTS, CATS, DRAFTABLE |
| structural | no judgment in it (parity hash, reporting band, legacy cap) | 4 | STARTERS, DF_K, DF_DAY_W, TIERS |
| measured | fit to a committed record | 4 | GRAD_DEFL, GRAD_SLOTS, SURV_K, SURV_FLOOR |
| declared_band | hand-set; the sweep publishes its title band (§3) | 6 | BENCH_WEIGHT, CV, PCT_MIX_INFL, TEAM_WEEK_SHOCK, weekly_availability, GAMES_PER_WEEK |
| uncalibrated | hand-set, no band; carries the decision id where its calibration is decided | 7 | GRAD_K, GRAD_SCALE, MKT_W, MKT_PIN, PAIR_MIN_GAIN, PAIR_WAIT_MIN, availability |

The uncalibrated entries and where each is decided:

| constant | role | what vouches for it today | decided at |
|---|---|---|---|
| arena.GRAD_K | gradient gain (draft-time only) | arena.py comment 2026-07-30 council 5-0; no fit | none needed: draft-time only, no in-season effect |
| arena.GRAD_SCALE | gradient scale (draft-time only) | arena.py 2026-07-30; no fit | none needed: draft-time only, no in-season effect |
| arena.MKT_W | market-persona category weights (mock-room opponents only) | arena.py strategy personalities block; no fit | none needed: mock rooms only, not the league simulator |
| arena.MKT_PIN | hand-set market pins for named rookies (mock rooms only) | deck analysis_2026-08-09_findings_table.md (MKT_PIN finding): hand-set July pins, no eligibility guard | none needed for the league simulator; mock rooms only |
| hoops.PAIR_MIN_GAIN | minimum gain for a pair recommendation (draft-time) | hoops.py; no fit | none needed: draft-time only |
| hoops.PAIR_WAIT_MIN | minimum survival to wait on a pair (draft-time) | hoops.py; no fit | none needed: draft-time only |
| hoops.availability | board haircut by injury tier (applies above the pool mean only) | hoops.py docstring: 0.78 'arena-calibrated vs real 2025-26 games played'; deck LESSONS.md item 5 (2026-07-12): risk-flagged played 51% of games vs 75% assumed, 0.78 kept above the realized ratio for streaming; 0.85 from outside projections' games 0.84-0.87 (2026-10-13); not used by the simulator (weekly_availability is), so no title band | D-PM-4 reconcile with arena.weekly_availability (0.78 vs 0.75, 1.0 vs 0.88); D-RN-4 review |

## 3. The assumption sweep

EVIDENCE: `scripts/redteam/sweep.py --seasons 6000 --seeds 2026 2027 --workers 4` → `sweep.json` on deck `259c630`; rosters `arena/data/states/draft_state_100.json` (the league's final rosters), pool `arena/results/players_v69.csv`, owner seat 10; registry sha `6ac4c0733f3a`. One constant changed per row, everything else held. **Tier rule:** mean shift over seeds: ROBUST < 1, SENSITIVE 1-2, FRAGILE >= 2 title points. The baseline is asserted within 3 SE of the 10,000-season reference on each seed before any tier is read. Tiers are taken on the unrounded mean shift, so a shown +1.0 can be 0.99 and ROBUST.

| constant | variant | title share (seed 2026 / 2027) | shift (mean) | tier |
|---|---|---|---|---|
| — | baseline (shipped) | 21.43 / 21.68 | — | — |
| arena.BENCH_WEIGHT | bench weight 0.50 | 21.43 / 21.68 | +0.00 / +0.00 (+0.0) | ROBUST |
| arena.BENCH_WEIGHT | bench weight 1.00 (F07's flip) | 21.43 / 21.68 | +0.00 / +0.00 (+0.0) | ROBUST |
| arena.CV | per-game variance x0.8 | 21.30 / 21.97 | -0.13 / +0.29 (+0.1) | ROBUST |
| arena.CV | per-game variance x1.2 | 21.98 / 22.67 | +0.55 / +0.99 (+0.8) | ROBUST |
| arena.PCT_MIX_INFL | binomial floor only (1.0) | 22.42 / 23.72 | +0.99 / +2.04 (+1.5) | SENSITIVE |
| arena.PCT_MIX_INFL | inflation 1.30 | 20.52 / 21.45 | -0.91 / -0.23 (-0.6) | ROBUST |
| arena.TEAM_WEEK_SHOCK | no shared games shock (0.0) | 24.42 / 25.43 | +2.99 / +3.75 (+3.4) | FRAGILE |
| arena.TEAM_WEEK_SHOCK | shared games shock doubled (0.12) | 19.40 / 19.02 | -2.03 / -2.66 (-2.3) | FRAGILE |
| arena.weekly_availability | no in-sim injury discount (risk 0.88 like healthy) | 20.17 / 20.22 | -1.26 / -1.46 (-1.4) | SENSITIVE |
| arena.weekly_availability | harsher risk tier (0.65) | 22.58 / 22.80 | +1.15 / +1.12 (+1.1) | SENSITIVE |
| arena.weekly_availability | healthy players play 0.95 of games | 20.68 / 20.87 | -0.75 / -0.81 (-0.8) | ROBUST |
| arena.weekly_availability | healthy players play 0.80 of games | 22.83 / 23.42 | +1.40 / +1.74 (+1.6) | SENSITIVE |
| arena.GAMES_PER_WEEK | 3.0 games per healthy week | 20.87 / 22.53 | -0.56 / +0.85 (+0.1) | ROBUST |
| arena.GAMES_PER_WEEK | 4.0 games per healthy week | 22.30 / 22.78 | +0.87 / +1.10 (+1.0) | ROBUST |

Per constant, the tier is its worst variant:

| constant | tier | largest mean shift | band to quote |
|---|---|---|---|
| arena.BENCH_WEIGHT | **ROBUST** | 0.00 | +0.0 (bench weight 0.50), +0.0 (bench weight 1.00 (F07's flip)) |
| arena.CV | **ROBUST** | 0.77 | +0.1 (per-game variance x0.8), +0.8 (per-game variance x1.2) |
| arena.PCT_MIX_INFL | **SENSITIVE** | 1.52 | +1.5 (binomial floor only (1.0)), -0.6 (inflation 1.30) |
| arena.TEAM_WEEK_SHOCK | **FRAGILE** | 3.37 | +3.4 (no shared games shock (0.0)), -2.3 (shared games shock doubled (0.12)) |
| arena.weekly_availability | **SENSITIVE** | 1.57 | -1.4 (no in-sim injury discount (risk 0.88 like healthy)), +1.1 (harsher risk tier (0.65)), -0.8 (healthy players play 0.95 of games), +1.6 (healthy players play 0.80 of games) |
| arena.GAMES_PER_WEEK | **ROBUST** | 0.99 | +0.1 (3.0 games per healthy week), +1.0 (4.0 games per healthy week) |

**The FRAGILE bands, as every report quoting a title share must now quote them:** TEAM_WEEK_SHOCK is FRAGILE, +3.4 (no shared games shock (0.0)) / -2.3 (shared games shock doubled (0.12)).

The shock rows reproduce the post-mortem's rows exactly (same engine, same seeds, same draw order, so the harness is the same harness): the post-mortem (6,000 seasons) had no shock at 24.42 / 25.43 and doubled at 19.40 / 19.02 against its baseline 21.43 / 21.68; this sweep's rows are in the table above. The new rows (PCT_MIX_INFL, games per week, bench weight) had never been swept. BENCH_WEIGHT's zero is structural: `team_week_model` reads the daily-fill weights, not the pick engine's bench weight (deck `arena.py`, 2026-07-23 note), and the sweep records the zero rather than asserting it.

## 4. The attack list

EVIDENCE: `scripts/redteam/attacks.json`, `run_attacks.py --check --out` → `attacks.json` (verdict PASS, live engine `259c630`; CURRENT 4, UNFINGERPRINTED 4). A row is never deleted, only retired with a date. Status CURRENT = record present and made on the live engine; STALE = made on another engine (fails); UNFINGERPRINTED = the record carries no engine commit (allowed, named); MISSING fails.

| id | attack | the question it tries to break | record | status |
|---|---|---|---|---|
| A-1 | known-answer re-implementation of the category math | Does a from-scratch z-score, availability, board and weekly FG%/PTS model reproduce the engine to the last digit? | `report/after-reports/postmortem-2026-10-19/rt_math.json` | CURRENT |
| A-2 | kit vs deck line join | Do the two planes carry the same lines for the same players, with no alias or surname false pairing? | `report/after-reports/postmortem-2026-10-19/rt_join.json` | UNFINGERPRINTED |
| A-3 | card measure vs simulator realized rates | Does the card's ECW rank the same as the seasons' title share, and are the category edges it quotes the ones the seasons realize? | `report/after-reports/postmortem-2026-10-19/rt_consistency.json` | UNFINGERPRINTED |
| A-4 | integer ties the simulator cannot produce | How often does a real weekly category tie, and does the continuous model see any of it? | `report/after-reports/postmortem-2026-10-19/rt_ties.json` | UNFINGERPRINTED |
| A-5 | structural sensitivity (format and tiers) | Does the title share survive the format assumptions one at a time: weeks, bracket, standings rule, tiers, shock, variance, category independence? | `report/after-reports/postmortem-2026-10-19/rt_sensitivity.json` | CURRENT |
| A-6 | decision robustness | Do the two headline swap verdicts stay positive under every A-5 variant? | `report/after-reports/postmortem-2026-10-19/rt_decisions.json` | UNFINGERPRINTED |
| A-7 | constants registry vs live engine | Does every judgment constant the engine runs on still equal its registered value, carry a calibration status, and name what vouches for it? | `report/after-reports/redteam-2026-10-19/constants.json` | CURRENT |
| A-8 | assumption sweep from the registry | Which hand-set constants move the title share by 2 points or more, and does every report quote those bands? | `report/after-reports/redteam-2026-10-19/sweep.json` | CURRENT |

## 5. The gates

EVIDENCE: `scripts/gates.py --report R --redteam SWEEP` runs, after the three report gates, `redteam constants` (`CONSTANTS CHECK: PASS`), `redteam bands` (`BANDS CHECK: PASS`, the report against the sweep record) and `redteam attacks` (`ATTACKS CHECK: PASS`), and records the sweep file's sha256 among the inputs so `--verify` refuses a report whose sweep moved. `test_gates_runner.py` gained two cases: the three gates are the three checks, and the bands gate goes red on a report missing a FRAGILE band and green when it quotes it. Each new check was seen red before green: the registry tests failed on a missing module, the attacks check failed live on the two records that did not yet exist (A-7, A-8), and the bands gate failed on the report without the band.

## 6. What this closes from the post-mortem, and what it does not

- Finding 1 (an uncalibrated constant quoted as ±0.4 where the band was ±3): closed for reporting (D-PM-6 made mechanical by the bands gate); open for calibration (D-PM-1, the registry names it).
- Finding 2 (the engine changed under the report): closed for every record that carries an engine commit (4 of 8 today): the attack runner fails on a mismatch. The 4 older records without a commit are named UNFINGERPRINTED until their scripts write one (D-RT-3).
- Findings 3 to 5 (card edges, retro noise line, ties): not touched; they are attacks A-3 and A-4, standing, and decisions D-PM-2 and D-PM-6.
- Finding 6 (two availability scales): the registry carries both scales side by side with D-PM-4; not reconciled here (no engine change without the owner's decision).
- Why it went undiscovered (every audit tested implementation against specification): the sweep is the first standing test of the specification itself, and the registry is the first list of what the specification's judgment calls are.

## Watchlist

- The sweep's bands are for the final rosters of 10/14 at seat 10; a roster move changes them. Re-run the sweep (about two minutes at 6,000 seasons) after any roster change that a report quotes a title share for.
- A new engine constant fails the registry check until it is registered with a status; that is the point, not a nuisance.
- Attacks A-1 to A-6 are fingerprinted where their records carry a commit (A-1, A-5) and UNFINGERPRINTED otherwise; a future run of those scripts should write `engine_commit`.

## Open-item receipts

Carried from the post-mortem report of the same day (no pull today; the rows are that report's):

Carried verbatim from the 10/14 league report (gated there on 10/15); not re-queried for this post-mortem (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| (this draft) | records only; no web research and no roster pull | Yahoo's 156 names resolve to the lock pool 156 of 156; Yahoo's NBA team agrees with the pool's at all 156 |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this grade (did not check) |

## Repeat-name market check

Carried from the post-mortem report of the same day (no refresh today):

Carried verbatim from the 10/14 league report; the same 33 rooms, not replayed again here (did not check).

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 beb243ef57af), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 33 of 33 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 32 of 33 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 23 of 33 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 14 of 33 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 33 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| John Collins | 12 of 33 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 11 of 33 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 10 of 33 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 10 of 33 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 7 of 33 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 6 of 33 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 33 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 33 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (17 mocks, value 27, market 45); Lauri Markkanen (15 mocks, value 21, market 37); Tyrese Haliburton (13 mocks, value 7, market 12); Tyrese Maxey (11 mocks, value 5, market 9); Kel'el Ware (10 mocks, value 57, market 77); Tyler Herro (9 mocks, value 51, market 69); Karl-Anthony Towns (8 mocks, value 12, market 15); Miles Bridges (5 mocks, value 96, market 98).

## Bounds

**Out of scope by design.**
- No constant was calibrated or changed; the registry records, the sweep measures. Calibration is D-PM-1 / D-PM-4 / the deck's N1 refit, each the owner's decision.
- The board-side haircut `hoops.availability` has no title band: the simulator does not read it. Its band would be a ranking band (board order under 0.70 / 0.85), not built here.
- The sweep moves one constant at a time; joint moves (shock and variance together) are not run.
- PR 2 (the skill) is separate.

**In scope and unverified.**
- The registry's calibration statuses are read from the deck's own records (findings tables, refit JSONs, LESSONS) and the module comments; where a record says 'hand-set' the status is uncalibrated or declared_band. A constant whose fit exists in a record this session did not find would be mislabelled uncalibrated: `NOT-ATTEMPTED` as a full search of the deck's results folder beyond the files named in each entry; not load-bearing (a mislabel in that direction over-reports doubt).
- The tier thresholds (1 and 2 points) are the post-mortem's and are a convention, not a fit; at 6,000 seasons the FRAGILE line sits at about 3.7 SE.

## Decision sheet (owner disposes)

| id | decision | recommended |
|---|---|---|
| D-RT-1 | adopt `--redteam` on every after-report that quotes a title share (the three red-team gates in `gates.json`): (a) yes, from this PR; (b) only on engine or roster changes | (a) |
| D-RT-2 | the registry's uncalibrated entries: (a) each gets a band at the next sweep that can reach it (hoops.availability as a ranking band), or a dated 'no in-season effect' note as now; (b) leave | (a) |
| D-RT-3 | the attack list: (a) every future red-team script registers a row and writes `engine_commit`; (b) leave the six as history | (a) |
| D-RT-4 | re-run the sweep after each roster change a report quotes odds for (two minutes): (a) yes, the record goes beside that report; (b) once a month | (a) |
| D-RT-5 | noticed, not touched (RULES 10): `scripts/weekly_preview.py` line 110 nests double quotes inside an f-string, a SyntaxError on Python 3.11 (this container) and legal only on 3.12+; `scripts/test_weekly.py` cannot import it here. Every other kit test file passes (9 of 10). (a) fix red-first in its own PR with the interpreter version pinned in the test header; (b) leave until the week-1 preview runs | (a) |

## Provenance

- Session: Claude Code (claude.ai/code), 2026-10-19, kit branch `claude/market-data-workorder-mnfi2b`; deck `259c630` read-only.
- Records: `report/after-reports/redteam-2026-10-19/constants.json`, `sweep.json`, `attacks.json`; this report by `write_redteam.py` in the same folder.
- Tools: `scripts/redteam/check_constants.py`, `sweep.py`, `check_bands.py`, `run_attacks.py`; `scripts/gates.py --redteam`; tests `scripts/test_constants_registry.py`, `test_redteam_sweep.py`, `test_redteam_attacks.py`, `test_gates_runner.py`.
- Re-verify: `python3 scripts/redteam/check_constants.py`; `python3 scripts/redteam/run_attacks.py --check`; `python3 scripts/gates.py --verify --report report/after-reports/after-report-2026-10-19-redteam-standing.md`.

## In plain language

The post-mortem found that a few numbers inside the simulator were set by hand and never tested against anything, and that one of them moved your title odds by about three points either way while the report quoted less than half a point. This PR makes that impossible to miss again. There is now a list of every such number with what it is for and what, if anything, backs it up; a script that checks the list against the live engine every time; a sweep that moves each hand-set number through its plausible range and says which ones matter (TEAM_WEEK_SHOCK are the ones that move your odds by two points or more); a rule that any report quoting your odds must also quote those bands, or it fails its gates; and a numbered list of every attack the engine has faced, which fails if the engine changes underneath it. Nothing in the engine changed: the numbers are the same as yesterday; what changed is that they are now written down, watched, and quoted with their doubt.
