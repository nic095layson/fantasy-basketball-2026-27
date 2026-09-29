# After-Report — 2026-09-29 final system integration, validation and integrity check on both mains, with re-calibration of the live-room instruments on the new rankings

**Owner request (2026-09-29, verbatim):** "Conduct one final system
integration, validation, integrity and full systems check. Merge, thank
you." and, mid-run: "Please conduct re-calibration testing as well with
these new player rankings."

**Method.** Same shape as the morning's validation sweep
(`after-report-2026-09-29-validation.md`), run on the merged mains — kit
`3bedd45` (PR #44) and deck `a3b4d31` (PR #53), the state the live artifact
Version 33 was built from: (P0) every gate and suite on both planes; (P1/P2)
the independent re-derivations of the deck's and the kit's computations
(`rederive_deck.py`, `rederive_kit.py` from the morning sweep, unchanged),
diffed against the page and the board; (P3) a fresh headless-Chromium drive of
every control on the published page; (P4) build reproducibility — the deck
rebuilt in a scratch copy of main and compared byte for byte; (P5)
integration assertions specific to the re-derivation pass — Yahoo position
parity on both planes, kit-deck line equality on the touched names,
provenance and roster-evidence coverage of every row; (P6) the live artifact
read back and compared to deck main; (P7) **re-calibration**: every live room
the deck has drafted in (mocks 51–56) re-graded on the v33 pool with the same
harnesses that graded it on the pool it was drafted against — the card
replay, the final standing, hindsight, the championship arms, the price-only
survival model pooled across all six rooms, and the mock-56 repeat-name
audit. No constant was re-fit: the re-calibration measures whether the
calibrated instruments still read true on the new rankings; a re-fit is a
model change and is the owner's call (Decision sheet).

Pull window: 2026-09-29 → 2026-09-29 (validation and re-calibration run; no
roster state change; no pool edit on either plane).

**Headline.** Every gate, suite and independent re-derivation is green on
both mains, the page drives clean, the build reproduces itself, and the live
artifact is byte-identical to deck main. Three integrity defects were found
and fixed in this pass, none of them in a computation: a sentence in the
re-derivation report that overstated how closely Beal's new kit row matches
the deck's; two stale counts in the kit README (the projections row count and
the derived-artifact count); and the seat-10 slate, which was still
generated from the 330-row pool and has been regenerated on v33. The
re-calibration says the instruments still read true — the pooled survival
model scores Brier 0.198 on v33 against 0.196 on the rooms' own pools, with
BUY NOW rows surviving 11 of 43 — and that the new rankings change what the
card would have said in every past room: on the corrected lines every
drafted roster loses title odds (mock 56's as-drafted roster from 55% to
26%, still first in expected category wins but by a third of the old
margin), while following the card on v33 recovers most of it in every room
(45–57%). The card's advice still produces a top roster on the new
rankings; what changed is which names it reaches for late — Suggs, PJ
Washington, Grimes and Gafford where Turner, Eason, Braun and Lopez stood.

---

## 1. Roster changes

None — validation and re-calibration only. Roster verification on the deck
plane re-run on main: 334/334 rows checked against the evidence ledger,
zero mismatches, fallback-partial (ESPN's roster API still returns 403);
`data/roster_verification.json` unchanged by the run.

## 2. Baseline gate battery — both mains (P0)

| plane | gate / suite | result |
|---|---|---|
| kit | `check_provenance.py` | PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13 .. 2026-09-29 |
| kit | `check_report.py` on all five 9/29 after-reports (pull, validation, market, draft-56, re-derivation) | REPORT GATE: PASS ×5 |
| kit | `rank_engine.py` re-run on main | 200 players from 324 projected; `top-200-2026-27.md` byte-identical after the rerun |
| kit | `check_derived.py` | DERIVED: all 10 dated artifacts reproduce byte-for-byte from their pinned inputs |
| deck | `hoops.py validate` | pool complete: all 120 consensus names present |
| deck | `check_planes.py --kit …` (F7) | 314 shared · kit-only 10 · deck-only 20 · team 0 · exclusion 0 · drift 0 · propagation 0 |
| deck | `check_parity.py` | PARITY: EXACT MATCH |
| deck | `test_gates.py` | all 34 cases passed |
| deck | `test_draft.py` | all 62 cases passed |
| deck | `test_card.py` | all 61 cases passed (the re-pointed D51R-4 cases included) |
| deck | `verify_rosters.py` | 334/334, 0 mismatches, fallback-partial |
| deck | `judgment_open_items.py` | 11 flagged names enumerated; `--check-report` PASS on the re-derivation report |
| deck | `build_deck.py` on main as-is | **BUILD REFUSED** by gate 4, as designed: the stamp asserts pool changes but `data/players.csv` is byte-identical to the last published build — a re-run on an unchanged pool must be restamped `--no-pool-changes` (see P4) |

## 3. Independent re-derivations (P1, P2)

| quantity | compared against | result |
|---|---|---|
| deck per-category z, 334 rows × 9 | `PLAYERS` baked into the page | max abs diff 4.99e-07 (6-dp rounding bound) |
| deck z | `hoops.zscores` | 0 |
| deck adjusted value | `hoops.adj_value` | 0 |
| deck availability multiplier, raw rows, team, position, note | baked page | 0 mismatches over 334 |
| deck market price (Yahoo 9/22 ADP else XRank) | baked `mkt` | 296 priced; the same two alias gaps as the morning (P.J. Washington, Ronald Holland II — both priced in the page, my naive matcher lacks the aliases) |
| deck top-10 by value | mine vs hoops vs page | identical: Wembanyama, Jokić, Gilgeous-Alexander, Dončić, Davis, Towns, Haliburton, Edwards, Maxey, Holmgren |
| fixed-point iterations to the top-156 set | — | 4 (2 in the morning: six mid-board rows crossing the replacement line take two more passes to settle) |
| kit top-200: rank, name, team, GP on every row | committed table | 0 mismatches over 200 of 324 |
| kit zPG / zAdj | committed table (2 dp) | max abs diff 0.005, rounding only |
| kit top 12 | — | Gilgeous-Alexander, Wembanyama, Jokić, Dončić, Towns, Maxey, Davis, Edwards, Daniels, Holmgren, Cunningham, Curry |

## 4. Integration assertions for the re-derivation pass (P5)

| assertion | result |
|---|---|
| every Yahoo-matched kit row's position set equals Yahoo's | 250 matched of 324, **0 differences** |
| every Yahoo-matched deck row's position set equals Yahoo's | 247 matched of 334, **0 differences** |
| the nine re-derived lines plus Clifford: kit line equals deck line | equal on all 11 stats for all ten; Mobley differs on everything but FT% by design (only his FT% was re-derived) |
| Beal's new kit row vs the deck's existing row | points, threes, attempts, FT% equal; FG%, rebounds, assists, turnovers differ by 0.1–0.2 — the re-derivation report said "matches the deck row's line"; **corrected** in this pass |
| every kit projection row has a provenance row | 324/324 |
| every non-FA deck row is on a team's evidence list | 334/334 |
| seat-10 slate generated from the current pool | **stale** — stamped on the 330-row pool (c0bf82bf4d39); regenerated on v33 (6efb01cd772b): 34 lines change, the likely names at #82–#111 are now Porziņģis, Poeltl, LaVine, Suggs, VanVleet and Wallace where Eason, Cameron Johnson, Turner, Braun and Poole stood, and Poole leaves the #130–#154 bands |
| kit README counts | "220 players" and "all six committed artifacts" were stale (324 rows, 10 artifacts); **corrected** |

## 5. The page and the build (P3, P4)

- Fresh DOM drive of `docs/draft-deck.html` on main (`full_dom_check.mjs`,
  `draft_state_54.json`, default TMPDIR): **127 assertions, 0 failed, 0 page
  errors, no crash, pass: true** — `arena/results/full_dom_check_2026-09-29_final.json`.
- Build reproducibility: main exported to a scratch copy, restamped
  `--no-pool-changes`, rebuilt with the kit checkout beside it — seven gates
  pass, pool sha `6efb01cd772b`, market 296/334 — and the page differs from
  main in exactly two strings, the freshness note in the manifest comment and
  in `BUILD_NOTE`, both of which carry the stamp text by design. Every other
  byte, the injected pool included, reproduces.

## 6. Live artifact (P6)

Read back from the standing URL after everything else: still Version 33
(id 1790707729-3a0f, 352,889 bytes); the served page contains deck main's
`docs/draft-deck.html` byte for byte inside the host's 355-byte head and
15-byte tail wrapper. No republish was needed or made.

## 7. Re-calibration on the new rankings (P7)

Every live room was re-graded on v33 by the harnesses that graded it on the
pool it was drafted against; the room's own record is untouched and the v33
results sit beside it as `m<mock>_<stage>_v33.json`
(`live_retro.py <mock> <stage> --tag v33`, new this pass; the tag pins the
pool to deck rev a3b4d31).

### 7.1 Survival chips — the calibrated instrument, re-measured

`live_survival.py` pooled over the six rooms' cards replayed on the v33 page
(`m5x_deckcard_v33.json`). Predicted survival comes from Yahoo's price alone,
so a re-ranking changes only which rows the card shows, not the model.

| pool | scored rows | mean predicted | realized alive | Brier | BUY NOW alive | TOSS-UP alive | quiet alive |
|---|---|---|---|---|---|---|---|
| rooms' own pools (m56_survival.json) | 303 | 0.535 | 0.713 | 0.196 | 17 of 45 | 31 of 59 | 168 of 199 |
| v33 (m56_survival_v33.json) | 323 | 0.502 | 0.616 | **0.198** | 11 of 43 | 43 of 90 | 145 of 190 |

Reading: the instrument holds. Brier moves by 0.002; BUY NOW still means
"more likely gone than not" (26% survived on v33, 38% before); TOSS-UP is
still a coin flip (48%); quiet rows still mostly survive (76%). The model
under-predicts survival by about 0.1 on both pools, the same direction as
the refit's own fit set — a candidate for the next refit, not a defect of
the re-ranking.

### 7.2 The rooms re-graded

Own pool = the pool the room was drafted against (its committed record);
v33 = the same room re-graded on the new rankings, opponents' picks held
fixed. "Card-#1 hits" = owner turns where the actual pick was the card's
#1; "card rank" = the card's rank of the actual pick, mean over 13 turns;
ECW = expected weekly category wins of the owner's roster vs the room and
its rank of 12; title odds from the arms stage (`as_drafted`); "follow the
card" = the self-consistent follow-the-card arm and its swap count.

| room (evidence: `arena/results/m<room>_{replay,final,arms}.json` and their `_v33` twins) | card-#1 hits, own → v33 | mean card rank, own → v33 | ECW, own → v33 | ECW rank | title odds as drafted, own → v33 | follow the card, own → v33 |
|---|---|---|---|---|---|---|
| 51 (live, seat 10) | 7 → 5 | 5.9 → 8.5 | 5.61 → 5.31 | 1 → 1 | 55.0% → 39.8% | 63.5% (4 swaps) → 54.2% (7) |
| 52 (live, seat 10) | 4 → 3 | 3.7 → 18.3 | 5.63 → 5.09 | 1 → 2 | 47.9% → 23.7% | 56.9% (7) → 49.7% (9) |
| 53 (live, seat 10) | 6 → 5 | 7.9 → 8.5 | 5.56 → 5.34 | 1 → 1 | 38.5% → 29.3% | 55.6% (9) → 45.0% (8) |
| 54 (live, seat 10) | 7 → 7 | 5.1 → 7.2 | 5.55 → 5.30 | 1 → 1 | 49.4% → 38.3% | 60.1% (2) → 53.9% (6) |
| 55 (deck MOCK room, seat 10) | 7 → 3 | 4.9 → 20.2 | 4.93 → 4.29 | 3 → 8 | 16.1% → 1.6% (playoff 86% → 34%) | 37.3% (7) → 26.4% (9) |
| 56 (live, seat 10 — the owner's plan) | 9 → 4 | 2.9 → 9.1 | 5.76 → 5.09 | 1 → 1 | 54.9% → 25.5% | 62.6% (3) → 57.0% (9) |

Three readings. (1) The instruments are stable: replay, final, hindsight
and arms all run on v33 without a missing name, and the rooms keep their
order (the four live rooms stay first or second in expected category wins;
the MOCK-mode room, which leaned hardest on the repriced names, falls to
eighth). (2) The re-ranking is large enough to change every past verdict's
numbers: mean card rank of the actual picks rises in all six rooms because
the owner's late picks were the names the intake repriced. (3) Following
the card on v33 still lands a top roster in every live room, at 45–57%
title odds, from a different set of late names — so the card's method
survives the re-ranking; its old late-round picks do not.

Survival on v33 is in 7.1. The mock-56 arms on v33 name the same late
alternatives the audit does: Miles Bridges at #87–#111, PJ Washington at
#130–#135, Filipowski or Gafford at #154.

### 7.3 Mock 56 — the owner's plan, re-graded

The Haliburton / Lillard / Irving roster re-graded on the lines the
re-derivation produced (opponents' rosters as drafted):

| measure | v31 (drafted against) | v33 |
|---|---|---|
| expected weekly category wins | 5.76, rank 1 of 12 | 5.09, rank 1 of 12 |
| season-shape H2H weeks won | 11 of 11 | 9 of 11 |
| category ranks (z-sum): FG% / FT% / 3PTM / PTS / REB / AST / ST / BLK / TO | 2 / 1 / 3 / 5 / 7 / 9 / 3 / 2 / 1 | 3 / 1 / 4 / **9** / 8 / 9 / **5** / 2 / 1 |
| title odds as drafted (arms) | 54.9% (playoff 100%) | 25.5% (playoff 94%) |
| follow the card self-consistently | 62.6%, 3 swaps (White #39, Pritchard #63, Poole #130) | 57.0%, 9 swaps (Holmgren #34, Bane #39, Pritchard #63, LaVine #87, Suggs #106, Bridges #111, PJ Washington #130, Wallace #135, Gafford #154) |
| card-#1 hits at the 13 owner turns | 9 | 4 |

What moved and what did not. The point-guard core is untouched: the three
guards carry the same lines on both pools and FT%, turnovers and blocks stay
first or second. The losses are exactly the repriced late picks — Turner
(#106), Eason (#111), Cameron Johnson (#87), Braun (#135), Lopez (#154) —
which take points from 5th to 9th and steals from 3rd to 5th and cost the
roster the margin that made it a 55% title favorite. The roster is still
the room's best by expected category wins; it is no longer a favorite by
season simulation, because the corrected lines give the field back the
categories those five were winning. The follow-the-card arm on v33 (57%)
says the same seat, drafting the new card's late names, recovers it.

The +7.6-point follow-the-card counterfactual the draft-56 report priced
on v31 is superseded by this table: on v33 the gap between as-drafted and
follow-the-card is 31.5 points of title odds, and none of the v31 arm's
three legs survive as the best swap at their pick.

### 7.4 Repeat-name audit on v33

`repeat_names_audit.mjs` re-run on the v33 page with the same seven watch
names (Anunoby, Lopez, Cameron Johnson, Braun, Eason, Poeltl, Turner):
at the owner's late turns the card's #1 is now Jalen Suggs at #106 and #111
(it was Turner, then Eason), PJ Washington at #130 and #135 (Braun) and
Quentin Grimes at #154 (Lopez). The set the owner asked the system to
defend no longer surfaces at those turns; the names that replaced them are
rows the re-derivation did not touch. `m56_repeat_names_audit_v33.json`.

## Watchlist

- **Survival under-prediction.** Mean predicted 0.50 vs realized 0.62 on
  v33 (0.54 vs 0.71 on the rooms' own pools): the price-only model is
  conservative about survival on both. A refit on the six-room set would
  move the chip thresholds; owner decision D-F2.
- **Mock 56's standing on v33** — see 7.3; the plan's roster is graded on
  lines it was not drafted against.
- **Fresh Yahoo ADP paste** (D-R2 stands): every survival prediction here
  runs on the 9/22 price file.
- Carried unchanged: Turner vs Ware, Poole, Mobley's free throws, Beal's
  knee, Simmons, Flemings, Trae Young and Herro (D-R1) — see the
  re-derivation report's watchlist.

## Open-item receipts

| item | query run (2026-09-29) | dated finding |
|---|---|---|
| (this run) | validation and re-calibration only — no news sweep; the day's 11 flagged receipts were re-run in the re-derivation pass (`after-report-2026-09-29-rederive.md`, receipts table, all quiet) | no roster state change; nothing new to receipt |

## Bounds

- The re-calibration re-grades past rooms on lines they were not drafted
  against: it measures the instruments and how the card would have read,
  not what the rooms would have done. Opponents' picks are held fixed.
- The survival pooled set changed size (303 → 323 rows) because the v33
  card shows different Top-5 rows at each turn; Brier is compared across
  sets, not on identical rows.
- No constant was re-fit (STREAM_R, the 0.78 multiplier, the survival
  σ-floor and K, PIN_MAX_GAP, the value-board knobs). The ΔECW weekly model
  still rests on the JS-vs-Python parity check alone (unchanged from the
  morning sweep).
- Direct fetches to most sports domains remain blocked; nothing in this
  run needed the web.

## Decision sheet (owner disposes)

| # | question | recommendation |
|---|---|---|
| D-F1 | Treat the v33 re-grades as the record for the mock rooms going forward (the debriefs and arms quoted in past reports were graded on the rooms' own pools)? | no — keep both; the room's own record is what the owner saw, the v33 re-grade is what the card would say now |
| D-F2 | Refit the survival model on the six-room v33 set (323 rows)? | not before the October price paste: the refit would learn 9/22 prices the room will not be drafting at |
| D-F3 | Run a fresh mock from seat 10 on v33 before 10/14 (D-R3 restated)? | yes — the only measurement of the new card that is not a re-grade of an old room |

## Provenance

- Kit main `3bedd45`, deck main `a3b4d31`, artifact Version 33
  (1790707729-3a0f). Every number above is read from a gate's or harness's
  output in this session; the re-derivation scripts and the comparison
  script are the session's, their JSON outputs are quoted, not recalled.
- Files added or changed by this pass: kit — this report, the pull-log row,
  `README.md` (two counts), `report/after-reports/after-report-2026-09-29-rederive.md`
  (the Beal sentence), `report/seat-10-slate.md` (regenerated on v33); deck —
  `arena/mocks/live_retro.py` (`--tag`, `POOLS["v33"]`, `V33_REV`),
  `arena/mocks/README.md` (the re-calibration entry),
  `arena/results/full_dom_check_2026-09-29_final.json`, `players_v33.csv`,
  and the `m5x_*_v33.json` result files.
