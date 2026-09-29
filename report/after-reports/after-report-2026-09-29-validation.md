# After-report — Top-to-bottom system validation and integrity test (2026-09-29)

**Owner request (2026-09-29, verbatim):** "Conduct a top to bottom, thorough
system validation and integrity test. Provide after report of findings , and
ensure every feature, button on the tool, and calculations / computations are
accurate and working."

**What was analyzed.** Both planes at their merged heads on 2026-09-29:
the deck repo `nic095layson/yahoo-fantasy-basketball` at main `d79847f`
(`docs/draft-deck.html` md5 `9f0aa0665b4e75a2a881b3eb420db219`, build v30 of
2026-09-28, pool sha256 `9d11cb45…`, 330 rows, Yahoo prices of 2026-09-22 baked
for 296 rows); the kit repo `nic095layson/fantasy-basketball-2026-27` at main
`2963d3b` (`report/projections-2026-27.csv` 318 rows; `top-200-2026-27.md`
generated 2026-09-28); and the live artifact at the standing URL, version
`1790626156-6db4` (Version 30). Nothing in either pool was edited. Every
regenerated file was restored with `git checkout` after its diff was recorded;
both working trees were clean apart from the artifacts this report adds.

**Method.** Six passes, each with its output committed under
`report/validation-2026-09-29/` (kit) or `arena/results/` (deck):
(P0) every existing gate and suite on both planes;
(P1) an independent re-derivation of the deck's z-scores, values, availability
multipliers, raw stat rows and market prices from `data/players.csv`, written
from the documented method without calling `hoops.py`, diffed against the
`PLAYERS` array baked into the page and against `hoops.py`;
(P2) the same for the kit board, written from PROMPT.md §4.2 without importing
`rank_engine.py`, diffed row by row against the committed top-200 table;
(P3/P4) a new headless-Chromium harness (`arena/mocks/full_dom_check.mjs`)
that drives every interactive control on the real page in LIVE, punt-declared
and MOCK rooms and cross-checks every displayed number against the engine
functions the page itself carries;
(P5) reproducibility runs of every kit script that can run offline;
(P6) a byte comparison of the live artifact against deck main.
Verification ran three times where cheap (the harness ran three times; the
first two runs' failures were harness bugs, listed in §4 so the reader can see
what changed between runs).

**Headline.** No computation is wrong anywhere I could measure. The deck's
baked z-scores match an independent derivation from the CSV to 5e-7 (the
6-decimal rounding bound) and match `hoops.py` exactly; values, availability,
raw rows and prices match on all 330 rows; JS and Python agree bit-for-bit on
survival and on the card ordering at 143 owner turns; the kit's 200-row board
re-derives identically, name for name, and regenerates with only its date line
changing; the card the browser shows equals the engine's ordering at all 13
owner turns of a replayed room; every strip count, matrix cell, roster total,
head-to-head cell and Mkt rank on the page equals the engine's number. All
127 harness assertions pass except two, which are the same small defect: with
an empty input, **Insert at #** and **Resync** log their warning but neither
re-render the log nor save, so the user sees nothing until the next action
(EVIDENCE §4.2). One cosmetic stale number: the Daily-sweep panel says the
sweep "re-verifies all 246 placements" while the pool is 330 rows. On the kit
side the engine is clean but four derived artifacts are not pinned to the
input snapshot they were generated from, so re-running their scripts today
produces different numbers (the seat-10 slate is eight days stale; the 8/24
league projection and the 9/16 market statistics regenerate against the grown
pool; the 9/15 Yahoo intake now trips its own gate), and one script
(`build_market.py`) overwrites `provenance.csv`, dropping the three Yahoo
provenance rows. Verdicts and the exact patches are in §7. Nothing was fixed
in this pass; the owner disposes.

Pull window: 2026-09-28 → 2026-09-29 (validation run; no roster state change,
no pool edit on either plane).

---

## 1. Baseline gate battery — all green (2026-09-29, both mains)

Roster changes in window: none (validation only). EVIDENCE:
`report/validation-2026-09-29/deck_suites_2026-09-29.txt` and the kit gate
output quoted below.

| plane | gate / suite | result (2026-09-29) |
|---|---|---|
| deck | `scripts/test_gates.py` (build gates 1–7, F8) | all 34 cases passed |
| deck | `scripts/test_card.py` | all 53 cases passed |
| deck | `scripts/test_draft.py` | all 62 cases passed |
| deck | `scripts/check_parity.py` | PARITY: EXACT MATCH — survival 12 vectors bit-identical, clock reads 12 field-identical, card orderings 143 owner turns across 11 committed states, market ranks 321 (priced 288), name-matching fixture and dfHash vectors identical on both sides |
| deck | `scripts/check_planes.py --kit …` (F7) | 308 shared, kit-only 10, deck-only 22, team 0, exclusion 0, drift 0, propagation 0 |
| deck | `scripts/hoops.py validate` | pool complete: all 120 consensus names present |
| deck | `scripts/verify_rosters.py` | 330/330 rows checked, 30 teams, 0 mismatches, mode fallback-partial (direct ESPN pull 403, as on every pull since 8/25); it correctly reports the 9/28 evidence as stale for a 9/29 build |
| deck | `scripts/judgment_open_items.py --check-report` on `after-report-2026-09-28.md` | receipts check PASS — all 10 flagged names carry a receipts row |
| kit | `report/check_provenance.py` | PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13 .. 2026-09-28 |
| kit | `report/check_report.py` (newest report) | REPORT GATE: PASS — after-report-2026-09-28.md |
| kit | `report/rank_engine.py` regeneration | 200 players from 318 projected; diff against the committed board is the "Generated …" date line only |

Two notes on the battery itself, both behaviour-as-designed: `verify_rosters.py`
rewrites `data/roster_verification.json` even when only reading (restored
after the run), and `judgment_open_items.py --check-report` against the
draft-54 room report fails by construction (a room report carries no pull
receipts; the gate is for the day's pull report, which passes).

## 2. Deck computations — independent re-derivation (P1)

Script: `report/validation-2026-09-29/rederive_deck.py` (mine; reads the CSV,
implements the documented top-156 fixed point, impact-weighted percentages,
inverted turnovers, the note-tag availability tiers and the ADP-else-XRank
price rule; never calls `hoops.py`). Result file: `deck_rederive.json`.

| quantity | compared against | result | grade |
|---|---|---|---|
| per-category z, 330 rows × 9 cats | `PLAYERS` baked into the page | max abs diff 4.997e-07 (the build rounds z to 6 dp; bound 5e-07) | EVIDENCE |
| per-category z, 330 × 9 | `hoops.zscores` | max abs diff 0 | EVIDENCE |
| adjusted value (availability applied to positive totals only) | `hoops.adj_value` | max abs diff 0 | EVIDENCE |
| availability multiplier (1.0 / 0.78 / 0.0 by note tag) | baked `av` | 0 mismatches over 330 | EVIDENCE |
| raw per-game rows (11 columns) + team, position, note | baked `r`, `t`, `p`, `note` | 0 mismatches over 330 | EVIDENCE |
| market price (Yahoo ADP else XRank, 2026-09-22 file) | baked `mkt` | 296 priced in the page vs 294 by my naive name match; the two gaps are aliases my matcher lacks — P.J. Washington (ADP 117.8) and Ronald Holland II (XRank 227) are in the Yahoo file at those values | EVIDENCE |
| fixed-point iterations to the top-156 set | — | 2 (the engine's own comment says it converges in one step; the second pass confirms the set) | EVIDENCE |
| top-10 by value | mine vs hoops vs page | identical: Wembanyama, Jokic, Gilgeous-Alexander, Doncic, Davis, Towns, Haliburton, Maxey, Edwards, Daniels | EVIDENCE |

Third-implementation checks that do not depend on either engine: the
survival law Φ((price − N)/max(8, 0.30·price)) re-implemented with `math.erf`
agrees with `hoops.survival_prob` (Abramowitz–Stegun polynomial) to 6.8e-08 on
the 12 parity vectors, inside the polynomial's stated 1.5e-07 bound, and both
clamps and both None cases agree; the snake order re-implemented from the
definition matches `hoops.team_of_pick` on all 156 picks. EVIDENCE (command
output in this session, 2026-09-29).

INFERENCE: with z, value, availability, prices, survival, clock and the card
ordering each verified by two or three implementations, the only computation
on the deck that rests on a single cross-check (JS vs Python, via
`check_parity`) rather than an independent derivation is the weekly
category-win model behind ΔECW (`teamWeekModel` / `decwScores`). It is listed
under Bounds.

## 3. Kit computations — independent re-derivation (P2)

Script: `report/validation-2026-09-29/rederive_kit.py` (mine; two-pass
top-180 pool as PROMPT.md §4.2 specifies "iterated once", impact-weighted
percentages, negative turnovers, zAdj = z × (GP/82 + (1 − GP/82) × 0.20) for
positive z, punt shifts for the six builds). Result: `kit_rederive.json`.

| check | result | grade |
|---|---|---|
| rows in the committed table | 200 of 318 projected | EVIDENCE |
| rank, name, team, GP on every row | 0 mismatches | EVIDENCE |
| zPG and zAdj (table shows 2 dp) | max abs diff 0.005, i.e. rounding only | EVIDENCE |
| punt column (+best / −worst build) | 0 mismatches | EVIDENCE |
| top 12 | Gilgeous-Alexander, Wembanyama, Jokic, Doncic, Maxey, Towns, Davis, Edwards, Daniels, Holmgren, Cunningham, Curry | EVIDENCE |
| `rank_engine.py` re-run on the same CSV | board byte-identical except the "Generated 2026-09-29" line | EVIDENCE |

The two planes rank the same names differently at the top (Wembanyama first
on the deck, Gilgeous-Alexander first on the kit) because they carry different
projection lines and different pool anchors by design (F7 compares only what
must agree: team, exclusion class, spelling, propagation — all 0 mismatches
today). INFERENCE, consistent with `check_planes.py`'s stated scope.

## 4. The tool — every control exercised in headless Chromium (P3/P4)

Harness: `arena/mocks/full_dom_check.mjs` (deck repo, new). Result:
`arena/results/full_dom_check_2026-09-29.json`, copied to
`report/validation-2026-09-29/full_dom_check_2026-09-29.json`; the tables
below are generated from that file by `coverage_table.py` (same folder).

Harness run: 2026-09-29T00:28:39Z on `docs/draft-deck.html` — 127 assertions,
2 failed, 0 page errors, 0 console errors, no crash. Three runs were needed:
run 1 crashed on my own selector (I selected the head-to-head opponent while
that tab was hidden); run 2 reported 29 failures of which 26 were harness
bugs (case-sensitive comparison against CSS-uppercased text, the ▲ risk glyph
the card appends to a name, an off-by-one in my strip expectation, a read of
the sweep panel before its awaited clipboard write finished) and 3 were the
page; run 3 is the record. EVIDENCE: the three run logs are in this session
and the diagnosis of each harness bug is in the harness source comments.

### 4.1 Controls

| control | assertions | verdict (evidence: assertion ids in the result file) |
|---|---|---|
| Teams / Rounds / Your slot inputs (echo) | 2 | PASS |
| Start draft — invalid config refused (teams < 2, rounds < 1, slot out of range) | 4 | PASS |
| Start draft — LIVE | 6 | PASS |
| Start draft — MOCK (cast seated, AI advances to your pick) | 3 | PASS |
| LIVE / MOCK mode buttons | 2 | PASS |
| Punt chips (9) at setup, and the declared punt on the strip, matrix, head-to-head and rosters | 5 | PASS |
| ⟳ Daily sweep panel (opens, names the last sweep, closes) | 3 | PASS |
| Import draft_state.json (file chooser opens; invalid JSON and missing keys refused with the right message; a 156-pick state enters the draft) | 4 | PASS |
| Export draft_state.json (real browser download; 156- and 24-pick states; MOCK export carries the cast) | 4 | PASS |
| Copy state JSON (clipboard write verified by reading the clipboard back) | 1 | PASS |
| Reset draft (two-click confirm; clears state and log; remembers the slot) | 3 | PASS |
| Pick feed — Log button and Enter (156-pick replay) | 2 | PASS |
| Pick feed — numbered correction (`24- Name`) | 2 | PASS |
| Pick feed — live hint under the box (D54-1; round-9+ wording from pick 97 on) | 1 | PASS |
| Undo last pick (LIVE and MOCK; MOCK input memory restored across 19 undos) | 4 | PASS |
| Insert at #… — toggle and a real insert (shifts the board) | 2 of 4 | PASS |
| Insert at #… — empty input | 2 of 4 | FAIL — warning not shown until the next action (§4.2) |
| Resync — toggle and a full 24-name rebuild (prior board saved under `draftdeck.v1:preresync`) | 2 of 4 | PASS |
| Resync — empty paste | 2 of 4 | FAIL — refusal not shown until the next action (§4.2) |
| Advance AI picks (MOCK) | 1 | PASS |
| Stage pick / Draft them buttons on the card (LIVE stages `my:`; MOCK drafts and advances) | 3 | PASS |
| TARGET / BOARD LEAN button (present at 11 of 13 owner turns; click sets the Fit lens and the family filter) | 1 | PASS |
| Tabs: Best available, Draft board, Rosters, Matrix, Head-to-head | 5 | PASS |
| Best available — Pos filter | 1 | PASS |
| Best available — Find box, and Enter on a drafted name ("Drafted #1 (R1) by Team 1") | 2 | PASS |
| Best available — Show N | 1 | PASS |
| Best available — Lens select (Balanced val, ΔECW, Fit, Mkt) | 4 | PASS |
| Best available — category header clicks, 3-cat cap warning, drill, × chip | 5 | PASS |
| Best available — Reset | 1 | PASS |
| Best available — row click stages the pick for the seat on the clock | 1 | PASS |
| Best available — ⛔ DO NOT DRAFT marker on the vetoed row | 1 | PASS |
| Head-to-head opponent select (11 options, the owner's seat excluded) | 2 | PASS |
| Tooltip on hover (data-tip) | 1 | PASS |
| Draft-complete state (strip, countdown, placeholder, card, 13-man roster, completion log line) | 9 | PASS |

Not exercised, by design: the FULL TILT / Adopt / Retarget buttons sit behind
`PUNT_BUTTONS = false` and do not render (page source line 1491); the Daily
sweep's clipboard copy of the sweep request was allowed to succeed or fail
(the panel's wording covers both).

### 4.2 The two defects

Both are the same two-line omission. In `runInsert`, the empty-input guard is
`if (!name || !Number.isInteger(P)) { log("Insert needs a pick # and a player name.", "warn"); return; }`
and in `runResync` the empty-paste guard is
`if (!segs.length) { log("RESYNC refused: paste is empty — …", "warn"); return; }`.
Neither path calls `renderMirror()` or `save()`. Probe
(`report/validation-2026-09-29/probe_empty_input_and_sweep.json`, 2026-09-29):
after clicking Insert with both fields empty, the log gained 0 visible lines
and the saved state carried no warning; after the next action (an Undo) the
warning was visible. Identical for Resync. EVIDENCE. The M53 fix of
2026-09-22 added the re-render for a *refused* insert (ambiguous name, out of
range) but not for the empty-input guard above it. Severity: minor — nothing
is lost, the button just looks dead until the next click.

Proposed patch (two lines; not applied):

```
-    if (!name || !Number.isInteger(P)) { log("Insert needs a pick # and a player name.", "warn"); return; }
+    if (!name || !Number.isInteger(P)) { log("Insert needs a pick # and a player name.", "warn"); save(); renderMirror(); return; }
…
-      log("RESYNC refused: paste is empty — nothing cleared, the board is untouched.", "warn");
-      return;
+      log("RESYNC refused: paste is empty — nothing cleared, the board is untouched.", "warn");
+      save(); renderMirror();
+      return;
```

### 4.3 Displayed numbers vs the engine

| displayed number / computation | assertions | verdict |
|---|---|---|
| Status strip: pick #, round, seat on the clock, your next, roster n/13, "N available" = `availablePool` — at pick 1 and every 24 picks | 7 | PASS |
| Decision card top-5 = `rankCard(decwScores)` over the owner pool (veto removed), at all 13 owner turns of the replayed mock-54 room | 2 | PASS |
| Exactly one 🎯 on the card; the vetoed name never on the card or the pin | 1 | PASS |
| Draft board grid: 13 rounds × 12 seats, snake placement (round 2 reversed) | 3 | PASS |
| Rosters tab: 12 rosters, kept-cat value = Σ `totalValue` (punt-aware) | 2 | PASS |
| Matrix: every cell = `categoryRanks` totals, Kept column, "Your rank" note; punted column struck | 2 | PASS |
| Head-to-head: You/Them = `rosterTotals`, lead flags, W–L note, cells consistent with the matrix row; "(punted)" label | 2 | PASS |
| Mkt column = `marketRanks` over the baked Yahoo prices | 1 | PASS |
| Lens orderings monotone (val, ΔECW, Fit, Mkt, cat lens, drill) | 6 | PASS |
| Your roster list and my-pick logging at all 13 owner turns (no D54-1 gap warning when the 🎯 is taken) | 13 | PASS |
| MOCK: typed `my:` pick logs and advances, D54-1 gap warning fires on an off-card pick, input memory across Undo | 3 | PASS |

Card-vs-engine detail (EVIDENCE, result file `notes.live.ownerTurns`): the
browser's top-5 equalled the engine's at #10, #15, #34, #39, #58, #63, #82,
#87, #106, #111, #130, #135 and #154; the gap the hint printed between #1 and
#2 was 0.000–0.013 blend points; the hint carried the round-9+ rule from #106
on and not before. The Python twin of that same ordering is what
`check_parity` compares (143 turns, EXACT), which closes the chain browser →
JS engine → Python.

### 4.4 Cosmetic

The Daily-sweep panel's step text reads "Cowork sweeps the news, re-verifies
all 246 placements, …" (page source line 1860) while the build carries 330
rows (build manifest). EVIDENCE. The number is a literal from the July pool;
`PLAYERS.length` is available in the same scope.

## 5. Kit scripts — reproducibility (P5)

Record: `report/validation-2026-09-29/kit_script_reproducibility.md` (every
regenerated file restored).

| script | evidence of the re-run | grade |
|---|---|---|
| `rank_engine.py` | board identical except the date line | EVIDENCE — clean |
| `slate.py` (default ADP file `consensus-2026-09-15.csv`) | 38 diff lines against the committed `seat-10-slate.md`, whose header says "board 2026-09-21 · Yahoo ADP 2026-09-15"; ranks moved (e.g. Holmgren/Mobley swap at #11/#12, Jalen Williams #17 to #18) because the deck pool changed on 9/22 and 9/28 | EVIDENCE — the committed slate is stale, and the script's default still points at the 9/15 file although 9/22 prices exist |
| `mock_draft_league_projection.py` | rewrites the 8/24 analysis with different numbers (cat wins 65 to 64, Σz +15.2 to +15.0 for the owner's seat) because it values the 8/24 rosters with today's 318-row CSV | EVIDENCE — a dated historical record regenerates against a moved input |
| `market/market_stats.py 2026-09-15` | ρ(our, XRank) 0.7842 on n=225 today vs 0.762 on n=214 in the 9/16 after-report (pool then 235 rows, now 318) | EVIDENCE — the report's figures are not reproducible from today's tree; the script has no snapshot argument |
| `market/yahoo_market.py 2026-09-22` | transcription gate PASS; `yahoo-2026-09-22.csv` (the file the deck bakes) byte-identical; `consensus`, `disagreements`, `unmatched` regenerate differently against the 318-row pool | EVIDENCE — the price file is stable; the joined artifacts are pool-dependent |
| `market/yahoo_market.py 2026-09-15` | HARD GATE TRIP — 10 unexplained unmatched pool players (rows added after 9/15 that the 9/15 paste never listed); no files written | EVIDENCE — the 9/15 intake can no longer be re-run without recording those absences |
| `market/build_market.py 2026-08-24` | regenerates from the committed raw snapshots but rewrites `provenance.csv` with only its two sources, dropping the three Yahoo rows that `yahoo_market.py` appended (9/16, 9/22 rankings, 9/22) | EVIDENCE — a data-loss footgun on any re-run; restored here |
| `market/fetch_market.py` | not run: network fetch of allow-listed sports hosts, out of scope by design | not run |
| `validate_49.py` | not run: hard-codes a state path under a session uploads directory that no longer exists (line 12); historical, single-use | not run |

INFERENCE: none of these is an arithmetic error. All five non-clean rows are
one design gap — derived reports read the *current* projections and pool
rather than the snapshot they were generated from, so their numbers drift
silently as the pools grow, and one of them overwrites a shared ledger.

## 6. Live artifact

The served page at the standing URL (version `1790626156-6db4`, read fresh
2026-09-29) contains deck main's `docs/draft-deck.html` byte-for-byte
(md5 `9f0aa066…`) inside the service's 355-byte head and 15-byte tail wrapper;
its manifest reads build 2026-09-28, pool sha256 `9d11cb45…`, market
`yahoo-2026-09-22.csv` priced 296 of 330. EVIDENCE (mechanical substring
compare, this session).

## Watchlist

- The two empty-input paths (§4.2) until patched — a user who clicks Insert or
  Rebuild with nothing typed sees no response.
- The seat-10 slate: regenerate on the October Yahoo paste, as its own
  docstring says; until then it reflects the 9/21 board.
- `verify_rosters.py` remains fallback-partial while `site.api.espn.com`
  returns 403 (every pull since 8/25); the direct guarantee needs the
  network-policy allow.
- The ΔECW weekly model has no third implementation (Bounds).

## Open-item receipts

None searched this run — this is a validation pass with no pull. The ten
flagged names (Brunson, Ingram, Porzingis, Cam Thomas, Ivey, Sochan, Lonzo
Ball, D'Angelo Russell, Mathurin, Duren) carry their receipts in
`after-report-2026-09-28.md`, which the deck's
`judgment_open_items.py --check-report` passes (10 of 10, re-run
2026-09-29); the same check against this file is not applicable and fails by
construction.

## Bounds

**Out of scope by design.** The arena's historical measurements (punt-arm,
tie-break, survival refit, season simulations) were not re-run — they are
recorded findings, not live features. The second page in `docs/`
(`cowork-vs-artifact.html`) was not exercised (assumption A1: "the tool" is the
draft deck). Network-fetching scripts (`fetch_market.py`, the direct ESPN pull
inside `verify_rosters.py`) were not run. Visual layout, dark mode, mobile
widths and accessibility were not checked — the harness asserts DOM state and
numbers, not rendering. The hidden punt buttons (`PUNT_BUTTONS = false`) do
not render and were not forced on. Projection lines themselves are inputs and
were not judged for accuracy against external sources.

**In scope and unverified.**
- ΔECW / weekly category-win model (`teamWeekModel`, `pwinsTotal`,
  `decwScores`): NOT-ATTEMPTED as an independent third derivation; verified
  only as JS-equals-Python by `check_parity` on 143 turns and as
  browser-equals-JS by the harness on 13 turns. Not load-bearing for the
  verdict "the tool shows what its engine computes"; load-bearing for the
  stronger claim "the engine computes the documented model", which this
  report therefore does not make for that one layer (decision D5).
- The LAST CALL pinned row and its 🎯 hand-off: ATTEMPTED-FAILED — the
  replayed mock-54 room produced 0 LAST CALL reads in 13 owner turns, so the
  path was exercised only by `test_card.py`'s cases, not in the browser.
- The UNKNOWN badge and D54-2 auto-fix in the browser: verified 2026-09-28 by
  `d54_dom_check.mjs` on the same page bytes (md5 identical), not re-run today.
- Survival chips (⏱ BUY NOW / TOSS-UP) and the 🚌 wait-chain text on the card:
  rendered during the replay but their wording was NOT-ATTEMPTED as an
  assertion; the probabilities behind them are verified (§2).
- The pick feed's name resolver on adversarial spellings: covered by the
  parity fixture (accents, suffixes, nicknames, typos, "Last, First") and by
  `test_draft.py`, not by new browser cases today.

## 7. Verdicts

| finding | tier | what would demote it |
|---|---|---|
| Empty-input Insert / Resync show no response until the next action (§4.2) | SHOULD FIX — two lines, patch above | a reproduction where the warning does render (the probe shows it does not) |
| Daily-sweep panel says 246 placements (§4.4) | NICE TO HAVE — one literal | none; it is a literal |
| Derived kit reports drift with the pool (slate, league projection, market stats, 9/15 intake) (§5) | SHOULD FIX — stamp the pool hash and date into each output and add a snapshot argument, or mark the historical ones frozen | evidence that the owner reads these as living documents rather than dated records |
| `build_market.py` overwrites `provenance.csv` (§5) | SHOULD FIX before its next run — merge by source instead of rewrite | none; the diff shows the three rows dropped |
| Deck engine, kit engine, parity, planes, gates, artifact | NO ACTION — all verified | any of the diffs in §2, §3 or §6 becoming non-zero on a re-run |
| ΔECW third derivation | NICE TO HAVE (decision D5) | — |

## Decision sheet (owner disposes; nothing here was executed)

| decision | proposal | cost |
|---|---|---|
| D1 | Apply the §4.2 two-line patch to `runInsert` and `runResync`; rebuild as v31 with a `--no-pool-changes` stamp; add a `test_card` case that the empty-input warning is in the saved log | 15 minutes; one deck PR and a republish |
| D2 | Replace the literal "246 placements" in the sweep panel with `PLAYERS.length` | ride D1's build |
| D3 | Regenerate `seat-10-slate.md` on the October Yahoo paste (or on `consensus-2026-09-22.csv` now) and point `slate.py`'s default at the newest consensus file | 5 minutes now; October's paste later |
| D4 | Make `build_market.py` merge `provenance.csv` rows by source rather than rewrite the file; stamp the pool hash and generation date into the outputs of `slate.py`, `mock_draft_league_projection.py` and `market_stats.py`, and either freeze the 8/24 and 9/16 artifacts as dated records or add a `--projections <snapshot>` argument | 30–45 minutes, kit PR |
| D5 | A third implementation of the weekly category-win model (from the arena's method notes, not from either port) compared on the 143 parity turns | 1–2 hours; closes the last single-cross-check layer |
| D6 | Add `full_dom_check.mjs` to the post-build ritual in DATA-PULL.md so every republished page is driven end to end (runs in about six minutes) | 5 minutes of doc |

Done during the analysis, reported as done: the harness and its result file
were added to the deck repo (`arena/mocks/full_dom_check.mjs`,
`arena/results/full_dom_check_2026-09-29.json`, README entry); this report
and its raw artifacts were added to the kit under
`report/validation-2026-09-29/`; a pull-log row for 2026-09-29 was added.
No pool, engine, page or board file was changed.

## Provenance

Produced 2026-09-29 by the Claude Code session
`session_01QjgeRdpDaWgSJmGKRG8fTU` on deck main `d79847f` and kit main
`2963d3b`. Raw artifacts: `report/validation-2026-09-29/` (suite log,
re-derivation scripts and their JSON, the Python card output at mock-54 pick
10, market-stats re-runs, the kit reproducibility record, the harness result
and the empty-input probe, `coverage_table.py` and its output). Harness
source: deck `arena/mocks/full_dom_check.mjs`. Re-verify the volatile claims:
`python3 scripts/check_parity.py` and `node arena/mocks/full_dom_check.mjs docs/draft-deck.html arena/data/states/draft_state_54.json /tmp/out.json`
in the deck repo; `python3 report/validation-2026-09-29/rederive_kit.py` and
`python3 report/validation-2026-09-29/rederive_deck.py` in the kit (the deck
one needs both checkouts side by side). The live-artifact comparison needs a
fresh read of the standing URL. Token cost of the session: not measured.
