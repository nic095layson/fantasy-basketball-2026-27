# Runner findings 1 to 6 (2026-11-02): sweep crash, emptied accuracy card, IL band, Monday "/", trailers (owner picks: the recommended option on each)

Pull window: 2026-11-02 → 2026-11-02 (no pull: the records on season/daily 2ed19d2 read only, the 11-02 morning run f6db119 among them; kit main 8ce0a75, deck main e14cc42).

**Method up front.** The runner's after-report of 11-02 (`after-report-2026-11-02-runner-window.md`, on season/daily) raised six findings. Each claim was re-verified on the records branch before the council sat; the council's verdict and the red-team pass on the band machinery were given to the owner with options, and the owner picked the recommended option on all four questions and excluded the waiver own-drop fix. Finding 1 was caused by this session's own #232 registry entries. EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: all five fixes built and tested; the 11-02 Monday sweep re-runs and PASSes on the fixed registry; the IL section now carries its FRAGILE room-rule band (+13.2 today) and reads as one range line; the accuracy card can no longer empty its own file; nothing merged.**

## 1. What was verified (EVIDENCE: the records branch at 2ed19d2)

| finding | the runner's claim | verified |
|---|---|---|
| 1 sweep crash | `ValueError: il_return.SLIPS is declared_band with no band` | yes: `morning_2026-11-02.json` step "season sweep" FAIL (non-fatal); the registry's two IL-return entries carried no band; `sweep.py:58` is the only reader of `band`; `check_constants.py` never asked for it |
| 2 accuracy.md emptied | 998 to 0 bytes, committed in f6db119 | yes: `wc -c` 0; `accuracy_week.py` opened the file for writing before `render()` raised on week 1's missing `candidate_minutes` |
| 3 IL band missing | the section names the rule, not the band | yes: brief and deck named the rule only |
| 4 waiver re-adds | three days running | yes; not built, the owner's word |
| 5 trailers | 41 / 6 model-named since 10-28 | yes: 41 / 6 / 1 neutral |
| 6 "/" on Monday, league ledger 0 rows | | yes; the ledgers (`calibration_league*.json`) hold week 3 only: they were created 10-27, after week 2's Sunday, so week 2 had no forecast to score. Not a bug; reported |

## 2. What was built (EVIDENCE: the suite, every file OK; the re-runs below)

| finding | change | test |
|---|---|---|
| 1 | `SLIPS` re-registered structural (a reporting grid); `ROOM_RULE_ON` uncalibrated under D-ILR-2 with its measured band in the record (the engine sweep cannot move a kit constant); `check_constants` now refuses a declared_band entry without a labelled band, so the gate asks what the Monday sweep will | `test_constants_registry.DeclaredBand` (2): the checker refuses a bandless entry; the live registry loads through `sweep.variants_from_registry` |
| 2 | `render()` tolerates a week without a snapshot column ("no snapshot"); the md is rendered to a string before the file is opened; `accuracy_week.py --render` regenerates the md from the record; a daily non-fatal "accuracy render" morning step restores it from the next run | `test_accuracy_week.RenderSafety` (2): week-1-shaped row renders; a failed render leaves the file untouched; `test_morning` order list |
| 3 | `il_return.py` measures the room rule's band every run (on time with the rule flipped, two more simulator runs); the section reads "if they return ≈30% (lo to hi across on time / +2 wk / +4 wk) · never = headline" with "**ROOM_RULE_ON is FRAGILE: +13.2 (rule off)**"; the deck's table collapses to the same two rows and quotes the band; the full grid stays in the record | `test_il_return` (lines, band, tiers, "band not measured") |
| 6a | `flaim_live.not_started` / `side_totals(empty_ok=True)`: a side with "/" and empty counts reads as zeros for the week card only; the strict read for the scoreboard intake is unchanged | `test_flaim_live.NotStarted` |
| 6b | `run_attacks` names the simulator's last commit beside the engine fingerprint ("simulator aa470f8"); `league_sim.py` is **not** added to the engine files: that would mark all nine standing attack records STALE and fail the gates | attacks check PASS, 10 attacks |
| 5 | this session's trailers switch to "Claude (session model A)" from this PR's commits; history untouched (rule 6) | |

## 3. Re-runs on the 11-02 records (EVIDENCE: `runner-fixes-2026-11-02/`)

- **Season sweep** (`sweep_2026-11-02.json`; 11-02 state, pool and real schedule; 6,000 seasons × seeds 2026/2027): PASS. Tiers today: TEAM_WEEK_SHOCK ROBUST (−0.05 / −0.35 and −0.03 / +0.29 by seed), weekly_availability FRAGILE (−2.4 / −3.9 with no injury discount; +2.2 / +1.3 harsher risk tier), BENCH_WEIGHT, PCT_MIX_INFL, GAMES_PER_WEEK ROBUST. INFERENCE: with week 1 final and the rosters of 11-02 the shared-games shock no longer moves the title share; the 10-26 band (+2.7 / −4.2) that the brief has quoted for a week was made on a different configuration.
- **IL-return** (`il_return_2026-11-02.json`): if they return 30.1 to 30.5 across the slip grid, never 13.6; **ROOM_RULE_ON is FRAGILE: +13.2 (rule off)**; the deck rendered the two-row table and the band (Playwright read-back).

## 4. Bands quoted

Title shares above carry the standing structural band. From the sweep of 2026-11-02 (this report's configuration): **weekly_availability is FRAGILE:** -3.2 (no in-sim injury discount (risk 0.88 like healthy)) / +1.8 (harsher risk tier (0.65)) / -0.4 (healthy players play 0.95 of games) / +0.1 (healthy players play 0.80 of games), mean of the two seeds. **TEAM_WEEK_SHOCK is ROBUST** on this configuration (it was FRAGILE on the 10-26 sweep: +2.7 / -4.2). The IL section's own: **ROOM_RULE_ON is FRAGILE:** +13.2 (rule off).

Runner impact: code-only (two new non-fatal morning steps: "accuracy render" daily, and the existing "il return" step now runs two more simulations; the Monday sweep runs again from the next Monday). No prompt change. The runner's own trailer label is the runner's to set; this session's is set here.

## 5. Bounds and open items

- Out of scope by design: the waiver own-drop logic (owner: not built); rewriting commit history; regenerating `accuracy.md` on main (main's copy is intact; the records branch's is restored by the first morning run after merge).
- In scope and unverified: the first live "accuracy render" and Monday sweep on the records branch (11-03 and 11-09); the Monday "/" rule has not seen a live Monday yet (unit-tested only).
- Open to the owner, not decided here: whether the brief should quote the 11-02 sweep's bands at once (it will from the next Monday run, when the sweep record is written by the run) or keep the 10-26 band until then.

## Watchlist

- 2026-11-03 morning: "accuracy render" PASS and `report/accuracy.md` back at its full length on season/daily; the IL section in its new shape with the band.
- 2026-11-09 Monday: the season sweep PASS and the brief's band line refreshed.

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
