# Proceed with all: merges, the out-* branch, current attack records, and the D-PM-4 measurement — 2026-10-21

Pull window: 2026-10-21 → 2026-10-21 (build and measurement only; no roster pull, no box scores, no projection line or tag changed).

**Owner's request.** "Proceed with all", 2026-10-21. These are the five items on the council-fixes decision sheet:
1. merge kit #148 and deck #127;
2. add the `out-*` → 0.0 branch to the simulator and its page twin;
3. after #148, add `report/run-ledger.jsonl` to the morning run's commit list;
4. D-RT-STALE: re-run the assumption sweep on the new engine, so the stale attack records become current;
5. D-PM-4 risk/mild: run the per-player comparison, as a measurement only, with no value change.

The 0.09 veto line was not taken, so recovery stays at 0.0.

**What was analyzed.**
- Kit `main` `f7db616` (after #148). The kit branch is `claude/market-data-workorder-mnfi2b`, restarted from it.
- Deck `main` `ac2c554` (after #127), then `80eecdf` (after #128, this report's engine).
- Code read: `arena.weekly_availability` and `weeklyAvail`, `hoops.availability` and `hoops.adj_value`, `rank_engine.avail` and `exclude_held`.
- Inputs: the in-season pool (`data/season/pool_season.csv`), the kit's season lines (`data/season/projections_season.csv`), and `data/league_state.json` of 2026-10-21.
- Tools: the red-team scripts, `league_sim.py`, and the morning task's stored prompt.

**Method choices, stated to the owner in the plan before the runs that used them:**
- M1. `out-*` → 0.0, first in the tier order, exactly as in `hoops.availability`.
- M2. The 10k references were regenerated on the final engine.
  - How: `league_sim.py --verify`, 10,000 seasons × seeds 2026 and 2027.
  - Where: new files, `m100_league_sim_10k_s{seed}_w17r_av0.json`, inside the deck PR, so no later deck commit makes the records stale. The old `_w17r` files are kept, because earlier reports cite them.
  - Then the sweep: 6,000 seasons × seeds 2026 and 2027, on `draft_state_100`, pool v69, seat 10, tiers 1 and 2 points.
  - Basis: the sweep's 3-SE self-check means nothing against a reference made on a different engine.
- M3. D-PM-4 is measured on what actually exists.
  - The three numbers per player: the deck tier, the kit `avail(gp)` and the simulator's `a`.
  - Each is shown relative to its own healthy reference: deck ÷ 1.00, simulator ÷ 0.88, kit ÷ the median `avail(gp)` of healthy players the kit prices.
  - Population: the in-season pool joined to the kit lines by the planes gate's name fold, plus the active-roster subset (IL excluded, D-IS-8).
- A1, stated in the plan as an assumption: your go on item 2 includes merging the deck PR. Item 4 means nothing unless the sweep runs on the engine that stands.

**Headline.** All five items are done. Only this kit PR waits for your word.
- **Merged:** kit #148 (`f7db616`), deck #127 (`ac2c554`), and deck #128, the `out-*` branch (`80eecdf`).
- **The morning run now commits the ledger.**
- **The attack records are current.** `run_attacks` passes with 5 CURRENT and 0 STALE (it failed in the 10/21 audit), and the claims gate passes 7 of 7 with CL-6 flipped to SUPPORTED.
- **Two findings change numbers you have seen:**
  - **The preseason title share moved.** The recovery change you approved tonight was not, as I had written, "nothing either way". It moves seat 10's draft-day title share from **21.1 % → 23.3 %** and **21.3 % → 24.1 %** on the two 10k reference seeds. All of that is Nurkić (seat 2) and Butler (seat 12) leaving the simulation (§3).
  - **The board's own injury discount is now a FRAGILE constant.** `weekly_availability` crossed the 2-point line, so title shares now carry **two** structural bands.
- **D-PM-4 measured.** For an injury-risk player, the three instruments disagree. The deck board discounts hardest (×0.78), the simulator sits in between (×0.852), and the kit board discounts least, on average ×0.918. The kit prices 7 risk-tagged players at or above the healthy median (§4).
- **I found a 13th error in my own record.** The audit's correction paragraph said "the board" applies both the tier and `avail(gp)`. No board does. That error also withdrew a finding for the wrong reason (§4).

---

## 1. Roster changes and the merges

No roster moved and no projection line or tag changed.

| PR | state | commit | note |
|---|---|---|---|
| kit #148 (council fixes) | **MERGED** | `f7db616` | one row corrected before the merge (§4): its "tier × `avail(gp)`" wording repeated the false premise; kit gates 4/4 PASS on the corrected bytes |
| deck #127 (recovery 0.0) | **MERGED** | `ac2c554` | as approved |
| deck #128 (`out-*` 0.0, 10k references) | **MERGED** | `80eecdf` | under A1; red-first 2/103 then 103/103, test_draft 67/67, test_gates 54/54, parity EXACT (520 owner turns, 40 states) |

**Morning task** (`trig_015cdR1nKmi2ZgqTcVZQBSgf`), after #148 merged:
- Step 6's commit list now ends with `report/run-ledger.jsonl`.
- Step 4 gained one clause saying that each step appends a ledger row.
- EVIDENCE: `update_trigger` returned the new prompt (`updated_at` 2026-10-21T05:27:25Z).
- The first run on it is 12:53Z today. Whether that run commits its rows is not yet observed (Bounds).

## 2. The `out-*` branch

`arena.weekly_availability` and the page's `weeklyAvail` now return **0.0** for a tag beginning `out-`. The check comes first, as in `hoops.availability`.
- Before, those tags fell through to the healthy 0.88. That contradicted the function's own comment ("mirrors hoops.availability").
- The A-9 separate attacker had predicted exactly this divergence beforehand: 9 notes.

| check | before the change | after |
|---|---|---|
| test_card, the two new `out-*` tags | **2 of 103 FAIL** (Python 0.88, page 0.88) | 103/103 |
| kit `check_constants`, now probing `out` (it skipped it) | **FAIL** on deck `ac2c554`: registry `out` 0.0, live 0.88 | PASS, 31 = 31 on `80eecdf` |
| A-9 availability, all 335 notes | 326 exact; the 9 `out-*` differ | **335 of 335 exact**; the 9 predicted diffs are now 0 |
| graded mocks replayed on the changed page | — | the 🎯 is identical at **429 of 429** owner turns; 33 of 33 card files equal |

The `check_constants` probe change is a **stated dependency, not a request**. The checker had skipped `out` for the simulator, so a PASS said nothing about the new branch. It is one line, and your veto can drop it.

**Effect on every current number: none.** No `out-*` player is on a league roster or on any roster in the 33 graded rooms. EVIDENCE: `proceed-2026-10-21/repeat_name_compare.out`, and the A-9 record.

## 3. D-RT-STALE: the attack records on the live engine

The new 10k references were built on `80eecdf` with `league_sim.py --verify`, which asserts draw-for-draw equality with `arena.simulate_seasons`. They passed on both seeds.

**Surprise, and its diagnosis.** I predicted that seat 10's baseline would move by less than a point. It moved +2.2 and +2.7. I stopped and decomposed it:
- The current engine with recovery patched back to 0.60 reproduces the old `_w17r` files seat for seat (0 of 12 differ, on both seeds).
- With recovery at 0.0, it reproduces the new files the same way.
- So the whole shift is the 10/21 recovery change. Two drafted recovery players leave the simulation: Nurkić on seat 2 and Butler on seat 12.
- EVIDENCE: `proceed-2026-10-21/decompose_ref.py` and `decompose_ref.out`.

| 10k reference, seed 2026 / 2027 | recovery 0.60 (old `_w17r`) | recovery 0.0 (`_w17r_av0`) |
|---|---|---|
| seat 10 (you), title % | 21.10 / 21.33 | **23.27 / 24.07** |
| seat 2 (Nurkić), title % | 11.23 / 10.57 | 2.62 / 2.95 |
| seat 12 (Butler), title % | 0.34 / 0.38 | 0.01 / 0.00 |

**What this corrects.** On 10/21 I wrote that the recovery choice "changes nothing either way, because all four recovery players are on IL". That holds for the in-season rosters only. The preseason grade and every sweep made on draft-day rosters move by more than 2 points.

**The re-runs, all on deck `80eecdf`:**

| attack | record | result |
|---|---|---|
| A-1 known-answer math | `postmortem-2026-10-19/rt_math.json` | z and availability max abs diff **0.0** over 335 rows; owner-week FG% and PTS identical; kit vs deck lines 0.0 on 302 common |
| A-5 sensitivity | `postmortem-2026-10-19/rt_sensitivity.json` | baseline 23.77 / 24.20; within 3 SE of the new reference on both seeds |
| A-7 constants | `redteam-2026-10-19/constants.json` | PASS, 31 = 31 |
| A-8 sweep | `redteam-2026-10-19/sweep.json` | baseline 23.77 / 24.20 (MC SE 0.54); within 3 SE on both seeds; **two FRAGILE** |
| A-9 simulator, separate attacker | `redteam-sim-2026-10-21/rt_sim.json` | PASS; all deterministic sections exact; season max abs z 2.06 |
| runner | `proceed-2026-10-21/attacks.json` | **ATTACKS CHECK: PASS** — 9 attacks; 5 CURRENT, 4 UNFINGERPRINTED, 0 STALE |

**The sweep's tiers moved with the engine** (mean shift over the two seeds, in title points):

| constant | variant | 10/19 (`259c630`) | now (`80eecdf`) |
|---|---|---|---|
| TEAM_WEEK_SHOCK | no shared shock / shock doubled | +3.37 / −2.34, FRAGILE | +2.71 / −3.62, FRAGILE |
| weekly_availability | no in-sim injury discount | −1.36 | **−2.68** |
| weekly_availability | harsher risk 0.65 / healthy 0.95 / healthy 0.80 | +1.14 / −0.78 / +1.57 | +0.47 / −1.54 / +1.01 |
| weekly_availability | tier | SENSITIVE | **FRAGILE** |
| PCT_MIX_INFL | binomial floor / inflation 1.30 | +1.52 / −0.57 | +0.99 / −1.06, still SENSITIVE |

The baseline title share, **23.8 % / 24.2 %** (sweep, 6,000 seasons, MC SE ±0.5), comes with two structural bands:
- **TEAM_WEEK_SHOCK is FRAGILE:** +2.7 (no shock) / −3.6 (shock doubled). The headline sits within that band.
- **weekly_availability is FRAGILE:** −2.7 (no in-sim injury discount) / +0.5 (harsher risk tier 0.65) / −1.5 (healthy plays 0.95) / +1.0 (healthy plays 0.80). This is the same table D-PM-4 is about.

**CL-6** ("the red team's attack records describe the live engine") is SUPPORTED. Its expected value is updated, so `check_claims --gate` passes 7 of 7. Two consequences:
- It returns to FALSIFIED at the next deck commit, because `run_attacks` keys on the deck HEAD.
- The gate then fails until the attacks are re-run. That is the design.

## 4. D-PM-4 risk/mild: the measurement, and an error in my own record

**The error (#13 of today's inventory).** The red-team audit's correction paragraph (`after-report-2026-10-21-redteam-audit.md`, on `main`) says "the board applies two separate factors: the injury-tier multiplier and, independently, an expected-games factor `avail(gp)`". The code says otherwise. EVIDENCE, read 2026-10-21:
- The **deck** board is tier only: `hoops.adj_value` returns `tv * availability(p)`, and `hoops.py` has no games term.
- The **kit** board is games only: `rank_engine` uses `z_total * avail(gp)` and has no notes column.

No instrument multiplies the tier by `avail(gp)`. Two consequences followed:
- That paragraph withdrew the "relative gap" finding (risk −0.072, mild −0.048) **for a reason that is false**.
- Decision item 5 then asked for a composition nothing computes.

The #148 row that repeated the premise was corrected before the merge. The audit report on `main` is not edited here (decision 4).

**The measurement.** Population: the in-season pool, 335 rows, joined to the kit lines by the planes gate's name fold, with **315 matched**.
- The 20 unmatched rows are deck-only: out-, traded, unsigned and deep-bench rows. Two of them carry risk tags (Steven Adams, Jarred Vanderbilt).
- That is under the 95 % I set as a branch rule, so the unmatched rows are named here and the table runs on the matched.
- EVIDENCE: `proceed-2026-10-21/dpm4.json` (engine `80eecdf`) and `dpm4_compare.py`.
- Relative = the multiplier for this player against an otherwise identical healthy player, read on each instrument's own scale.

| tier (pool / active rosters) | n | deck board | simulator | kit board: mean [min, max] | kit ≥ healthy median |
|---|---|---|---|---|---|
| healthy | 271 / 136 | 1.00 | 1.000 | 0.997 [0.571, 1.124] / 0.990 [0.868, 1.089] | 184 / 78 |
| mild | 2 / 2 | **0.85** | **0.898** | 0.825 [0.740, 0.910] / 0.807 [0.724, 0.890] | 0 / 0 |
| risk | 31 / 17 | **0.78** | **0.852** | **0.918** [0.740, 1.045] / 0.906 [0.724, 1.022] | **7 / 4** |
| recovery | 8 / — | 0.0 | 0.0 | held off the kit board (GP ≤ 25), 8 of 8 | — |
| out | 3 / — | 0.0 | 0.0 (since #128) | held, 3 of 3 | — |

Kit healthy median `avail(gp)`: 0.8634 (pool) and 0.8829 (active). One healthy-tagged row is kit-held: John Konchar, FA.

What the table establishes (EVIDENCE, read from the record):
- For a risk-tagged player the three instruments give **three different discounts**: deck ×0.78, simulator ×0.852, kit ×0.918 on average. The kit's is per player, from GP, and ranges ×0.74–1.05.
- **The deck board is the harshest and the kit board the mildest.**
- On recovery and `out`, all three now agree: excluded.
- **Seven risk-tagged players carry kit GP at or above the healthy median**, so the kit plane prices them as healthy or better: Alex Sarr, Jaylen Wells and Keegan Murray (72 GP); Zach Edey, Trey Murphy III and De'Andre Hunter (70); Jaren Jackson Jr. (68).

What it suggests (INFERENCE):
- The withdrawn deck-vs-simulator gap is a like-for-like comparison after all: 0.78 vs 0.852 at risk, and 0.85 vs 0.898 at mild, so the deck multiplier is 0.072 and 0.048 lower. Both numbers mean "an otherwise identical healthy player = 1".
- So on the **deck plane** the risk discount is harsher than the simulator's. That plane is `hoops`, which ranks the draft board, the waiver scan (`co_gm`) and the brief's per-game values.
- It does *not* hold for the kit plane's board, which is the in-season Board tab. That one discounts less.
- Three caveats:
  - The deck's tier applies only above the pool-mean zero (D-1009-2).
  - The simulator's figure is its mean-games scaling. Its start-rate weights and variance terms are not part of this ratio.
  - The kit's figure is per player.

What it does not establish: which number is right. That needs realized games for tagged players (decision 3). No value changed.

## 5. Every gate, pass or fail

| gate | result |
|---|---|
| kit suite (`SEASON_POOL=1 … unittest`) | 219/219, twice (before and after the records changed) |
| deck test_card / test_draft / test_gates | 103/103, 67/67, 54/54 |
| deck check_parity | EXACT: 520 owner turns, 40 states |
| redteam constants / attacks | PASS 31 = 31 / PASS, 0 STALE |
| check_claims --gate | PASS, 7 of 7 as expected |
| report gates and bands | in `gates.json` (this report) |

## Watchlist

- **The in-season page shows one of two FRAGILE bands once this PR merges.** `scripts/season_deck.py` hardcodes `TEAM_WEEK_SHOCK` for the Odds tile. `daily_brief.py` reads every FRAGILE constant, so the brief carries both. Flagged, not fixed (decision 2).
- **CL-6 goes FALSIFIED at the next deck commit.** That is by design. Re-run the five attacks after any deck merge.
- **Older scripts still read the 0.60-recovery references:** `rt_consistency.py` and `retro_redteam.py`. Both are dated or unfingerprinted research scripts, and they were not repointed.
- **The draft deck was not republished.** The page changed only in `weeklyAvail`, and the draft is over.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| kit #148 | **MERGED** | `f7db616` |
| deck #127 | **MERGED** | `ac2c554` |
| `out-*` branch | **BUILT, MERGED** | deck #128 `80eecdf`; red-first 2/103 then 103/103 |
| morning ledger path | **DONE** | trigger prompt step 6, updated 05:27Z |
| D-RT-STALE | **DONE** | 5 records CURRENT on `80eecdf`; `run_attacks` PASS; CL-6 SUPPORTED |
| D-PM-4 risk/mild | **MEASURED**, no value changed | `proceed-2026-10-21/dpm4.json` |
| D-INT-1 | carried | provenance writer not built (owner's call) |

The flagged-name receipts are carried forward from the lock report. This build pulled nothing and researched no player, so they were not re-queried (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this build (did not check) |

## Repeat-name market check

Re-run fresh, because this build changed the page (`weeklyAvail`, §2). The 33 graded mocks were replayed on the changed page (sha256 6a5cefea4921, deck `80eecdf`) and, for comparison, on the page before it (`ac2c554`, sha256 a7185d96286f, the page the council-fixes report replayed).

**What the page change did to the card: nothing.**
- The 🎯 is identical at 429 of 429 owner turns, and all 33 saved card files are equal.
- The flagged list and counts are unchanged from the council-fixes report.
- EVIDENCE: `proceed-2026-10-21/repeat_name_compare.out`.

The tool's output, pasted:

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

## Decision sheet

1. **Merge this kit PR.** Merging is your word.
   - It carries the current attack records, CL-6 SUPPORTED, the `out` registry row and probe, the new reference path, and the D-PM-4 record.
   - Until it merges, `main`'s `sweep.json` is the 10/19 record: one FRAGILE band, engine `259c630`. The morning brief keeps quoting that.
2. **The in-season page's band line** (flagged, not built). `season_deck.py` hardcodes `TEAM_WEEK_SHOCK`. With `weekly_availability` now FRAGILE, the Odds tile would quote one of two bands.
   - Option (a): read every FRAGILE constant from the record, as `daily_brief.py` does. That is one function plus a red-first test.
   - Option (b): leave it.
   - *Recommended: (a), merged with or before this PR.*
3. **D-PM-4 risk/mild values.** Options:
   - (a) leave all three instruments as they are;
   - (b) align the simulator to the deck: risk ×0.78 relative, i.e. 0.686;
   - (c) align the deck to the simulator: risk 0.852, mild 0.898;
   - (d) calibrate all three against realized games for tagged players once the season has enough of them.
   - *Recommended: (d), with a check date you pick.* Separately, the 7 risk-tagged kit rows carrying healthy-level GP need a look (each is a line or tag question, so yours).
4. **Correct the audit report on `main`** (flagged, not edited). Add a dated note at its "two separate factors" paragraph saying the premise is false, and that the withdrawn deck-vs-simulator gap stands as measured here. *Recommended: yes; docs only.*
5. **Older scripts on the old references.** `rt_consistency.py` and `retro_redteam.py` still read the 0.60-recovery `_w17r` files. Option (a): leave them as dated research. Option (b): repoint them. *Recommended: (a).*
6. **The A1 reading.** I merged deck #128 on your item-2 go, and said so in the plan beforehand. If you meant build-only, a revert PR restores `ac2c554`'s engine. The attack records would then go stale again.

## Bounds

**Out of scope by design.**
- Any change to risk or mild values, and any line, tag or roster.
- The four unfingerprinted attacks (A-2, A-3, A-4, A-6). They are not re-run, and the runner allows them as UNFINGERPRINTED.
- The draft deck republish, the `season_deck.py` fix, the audit-report note, and repointing older scripts.

**In scope and unverified.**
- **Whether the 12:53Z morning run commits its ledger rows.** `NOT-ATTEMPTED`, because it has not run yet. A check-in is armed for after it. Not load-bearing for anything above.
- **The deck's DOM check.** `full_dom_check`, which earlier builds ran, was not run for #128: `NOT-ATTEMPTED`. Not load-bearing: test_card executes the page's `weeklyAvail` on the two new tags, and parity is EXACT.
- **The two risk-tagged players outside the D-PM-4 join** (Adams, Vanderbilt). Not in the kit's figures. Not load-bearing: two of 33.
- **The sweep's tier boundaries.** They rest on two seeds at 6,000 seasons. A tier near a line (`PCT_MIX_INFL` at 1.06) could flip on a third seed. Did not check.

## Provenance

- **Session:** Claude Code (cloud), 2026-10-21, 05:04Z–06:40Z.
- **Governors, all loaded with the Skill tool for this task:**
  - plan-gate, before the first action; its block was shown to you before any merge;
  - after-report, before this report was written;
  - adversarial-verify, before delivery;
  - scope-fence, **late**: at the delivery step, after the three flags above had been decided from re-attached text, which by the house rule does not count as loaded.
- **Records:** `proceed-2026-10-21/`. It holds `dpm4_compare.py`, `dpm4.json`, `decompose_ref.py`, `decompose_ref.out`, `attacks.json`, and `repeat_name_{out_page,main_page}.json` with `repeat_name_compare.out`.
- **The five attack records** sit at the paths in §3.
- **Re-verify:**
  - `python3 scripts/redteam/run_attacks.py --check` (expect PASS, 0 STALE while deck HEAD is `80eecdf`);
  - `python3 scripts/check_claims.py --gate`;
  - `python3 scripts/run_ledger.py --stale`;
  - `python3 report/after-reports/proceed-2026-10-21/dpm4_compare.py`.
