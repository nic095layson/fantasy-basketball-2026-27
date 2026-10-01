# After-report — 2026-10-01: deck v40 — the history box keeps up with inserts (D59-1) and the two-pick 🎯 (D59-2), the second behind a pre-registered experiment

**Owner decision (2026-10-01, verbatim):** "Proceed with recommended steps,
forget about the ESPN projections as they are stale data."

**What this is.** The two proposals the owner raised after mock 59, built
red-first on both planes and shipped as deck v40. (1) After an Insert-at-#,
the history box re-numbers and re-seats every earlier line from the state,
marks the picks the shift moved onto the owner's seat and gives them the
card echo they never got, and renames a standing UNKNOWN to its new number
in the state and the log. (2) The 🎯 is chosen on the expected value of the
next two owner turns, not the next one, so a deep #1 the room will not take
for rounds yields the marker to a near-equal scarce row — with the deep row
named as next turn. The second is a change to the card's primary signal, so
it carried the D58-3 bar first: a pre-registered replay of the eight public
live rooms, written up before the numbers landed
(`arena/results/pair_experiment_2026-10-01_design.md`), and the switch that
turns the marker on follows that document's decision rule.

**Method.** Red tests first (card suite, draft suite, a new browser drive of
the mock-59 tool log), then the code on both planes (page engine and app;
`hoops.py` twins for the insert rename and the pair rule, parity pinned by
the card suite on five fixtures), then the experiment, then the build and
its gates, parity, the three suites, the 128-assertion browser drive, the
publish. ESPN's projection page is dropped as stale at the owner's word.
Verification: this file passes `report/check_report.py`.

Pull window: 2026-10-01 → 2026-10-01 (deck change; not a roster pull).

**Headline.** Deck v40: the history box re-numbers, re-seats and marks (YOU) after an insert and renames a shifted UNKNOWN (mock 59's three stale lines now read right in the browser drive); the two-pick 🎯 is built on both planes and was put behind a pre-registered replay of eight live rooms before it could move the marker — mean title odds 45.83 / 46.21 following the blend 🎯 against 45.69 / 45.89 following the two-pick 🎯 on the two seed sets, the marker moving at 6 turns; the bar fails and v40 ships with the marker off (advice only). All gates, parity and suites green; Version 40 published.

## 1. D59-1 — the history box after an insert

[EVIDENCE: `docs/draft-deck.html` `insertPick` / `relabelLog` / `applyShift`;
`scripts/hoops.py` `insert_pick`; `scripts/test_card.py`, `scripts/test_draft.py`;
`arena/mocks/history_dom_check.mjs` → `arena/results/history_dom_check_2026-10-01_v40.json`]

What was wrong, measured on the room (mock 59, 161 events, four inserts): the
history lines were plain text written when each pick was fed, so after the
#97 insert Queta's line kept "#105 → Seat 9" and after the #121 insert
Washington's kept "#128 → Seat 8" — both were the owner's picks by then and
neither read as such nor got the card echo; the standing UNKNOWN (Hansen)
kept "#125" in its name at #126. The browser drive of those 161 events on
v39 failed exactly those three lines; on v40 it passes all nineteen checks
with zero page errors.

What changed, both planes:

- Pick lines in the history carry their pick index and kind. After an
  insert the earlier lines are re-rendered from the state: number, round,
  seat, "(YOU)". A pick the shift moved onto the owner's seat gets one
  warning line with its card rank and gap against the card as it stands
  now, labelled "(card as of now)"; a pick moved off the seat is noted.
- A standing UNKNOWN the shift moves is renamed to its new number in the
  state (page and `hoops.py`), so the roster list, the status strip and the
  history agree. A fixed UNKNOWN's original line is history and stays as
  written.
- The insert echo's wording is unchanged ("✎ inserted X at #P → Seat S;
  #P–#N → #P+1–#N+1 (k shifted, slots recomputed)") so the 161 recorded
  expectations of the mock-59 tool log still hold; the owner's proposed
  re-wording was not adopted (A6 in the plan, stated here).
- Not built: undo of an insert. The page's Undo pops the last pick only and
  keeps no pre-insert snapshot; §9a's point 5 assumed one. It is a separate
  item (D40-3).

Tests: the draft suite gained three cases (the shifted UNKNOWN is renamed
#3 to #4), the card suite nine (the engine's `relabelLog` on a fixture with a
pick moved onto the owner's seat and a renamed UNKNOWN; the app consumes it
and echoes the card as of now), and the browser drive is the room itself.

## 2. D59-2 — the two-pick 🎯

[EVIDENCE: `docs/draft-deck.html` `pairDecision` / `PAIR_MIN_GAIN` /
`PAIR_WAIT_MIN` / `PAIR_MARKER`; `scripts/hoops.py` `pair_decision`;
`arena/mocks/live_retro.py` `stage_pairarms`; `arena/mocks/pair_experiment.py`;
`arena/results/pair_experiment_2026-10-01_design.md` (written first);
`arena/results/pair_experiment_2026-10-01.json`; `arena/results/m<NN>_pairarms.json`]

**The rule.** For the five rows of the card in blend order, with s_j the
price-only survival of row j to the look-through next owner turn and
ΔECW(j | i) the marginal weekly categories of row j with row i already on
the roster (the same weekly model the card scores with):

```
pair_i = ΔECW_i + Σ_j  s_j · Π_{k before j} (1 − s_k) · ΔECW(j | i)   (j ≠ i, by ΔECW(j | i) desc)
       + Π_j (1 − s_j) · ΔECW(last | i)
```

The marker moves to the best pair only when the gain over row 1 is at least
0.01 categories a week and row 1's own survival is at least 0.60 (the band
where the refit survival model has been right: rows at 0.60 or better
survived 40 of 43). The Top-5 order never changes, so the parity key and the
value ranking stand; an urgent structural pin still outranks it. The advice
line says who to take now, who likely waits and by how much, and the deep
row carries a "⏭ next turn ~N%" tag. `PAIR_MARKER` is the switch between
the marker moving and the read being advice only.

**What the rule says about mock 59's #82, honestly.** On the card the owner
saw (Poeltl 0.940 at 0.83 survival; LaVine, Suggs, Bridges, Hart at 0.62 to
0.77), the pair arithmetic prefers Bridges-now by 0.007 — under the bar, no
move. All five rows were deep; the cost at that turn came from taking none
of them, which is what §9b of the mock-59 report found. The fixture in the
card suite pins that arithmetic rather than a wished-for move; the cases
that exercise the move use a deep #1 against a genuinely scarce near-equal
row.

**The experiment (pre-registered, then run).** Eight public live rooms,
each graded on the pool it was drafted against, two self-consistent
follow-the-🎯 chains built on the same code path (strict pairwise swaps with
a pick that went later to a non-owner seat; the owner veto where the room
had it): the shipped blend 🎯 and the two-pick 🎯. Title odds on the real
eight-team bracket, 6,000 seasons per seed, seed sets S1 = (11, 23, 47) and
S2 = (5, 17, 29). Validity check: the blend chain reproduced every room's
recorded `follow_card_selfconsistent` swaps where the record exists.

| room | pool | survival price | as drafted S1 / S2 | blend 🎯 chain S1 / S2 | two-pick 🎯 chain S1 / S2 | marker moved | blend chain = recorded arms |
|---|---|---|---|---|---|---|---|
| 51 | v23 | market position (pre-F8) | 42.79 / 43.27 | 51.44 / 52.79 | 51.44 / 52.79 | 0 | yes |
| 52 | v23 | market position (pre-F8) | 37.95 / 37.78 | 45.81 / 46.18 | 45.81 / 46.18 | 0 | yes |
| 53 | v25 | Yahoo price (page) | 31.10 / 31.67 | 46.14 / 47.08 | 43.11 / 42.91 | 2 | yes |
| 54 | v28 | Yahoo price (page) | 38.62 / 39.49 | 49.17 / 49.39 | 49.17 / 49.39 | 1 | yes |
| 56 | v31 | Yahoo price (page) | 43.66 / 44.07 | 52.58 / 52.50 | 52.58 / 52.50 | 1 | yes |
| 57 | v33 | Yahoo price (page) | 27.44 / 27.30 | 41.43 / 41.76 | 41.43 / 41.76 | 0 | yes |
| 58 | v35 | Yahoo price (page) | 36.75 / 36.74 | 40.89 / 40.29 | 40.89 / 40.29 | 0 | yes |
| 59 | v37 | Yahoo price (page) | 20.38 / 21.08 | 39.18 / 39.70 | 41.09 / 41.31 | 2 | yes |
| **mean** | | | 34.84 / 35.17 | **45.83 / 46.21** | **45.69 / 45.89** | 6 | |

Per room the two-pick chain was better in 1 and worse in 1 on
S1, better in 1 and worse in 1 on S2; the chains were identical
in 5 of eight rooms. The turns where the marker moved: mock 53 #15: Austin Reaves now instead of Jalen Williams (+0.045); mock 53 #58: OG Anunoby now instead of Payton Pritchard (+0.010); mock 54 #34: Derrick White now instead of Jalen Williams (+0.015); mock 56 #82: Jakob Poeltl now instead of Tari Eason (+0.061); mock 59 #34: Derrick White now instead of Jalen Williams (+0.024); mock 59 #63: Payton Pritchard now instead of Jakob Poeltl (+0.031).

**Verdict against the bar (mean two-pick ≥ mean blend on both seed sets):**
FAILS — S1 45.69 vs 45.83, S2 45.89 vs
46.21; the marker moved at 6 turns. By the design
document's decision rule: **BAR FAILED — PAIR_MARKER false, advice only** — v40 ships with `PAIR_MARKER = false`.

**Where the two-pick chain lost, and where it won.** Mock 53 is the whole
deficit: at #15 the rule took Austin Reaves (survival 0.07 to #34) over
Jalen Williams (0.76) and Derrick White (0.82), expecting Bane (0.89) next —
and the roster that followed was worth 3.0 and 4.2 title-odds points less
on the two seed sets than the blend chain, which took White at #15 and then
Karl-Anthony Towns, fallen to #34, at the next turn. A two-turn horizon
cannot see a star falling to the next pick; the blend chain's #1 at #34 did.
Mock 59 is the gain: White at #34 with Jalen Williams next, Pritchard at #63
with Jarrett Allen next — 1.9 and 1.6 points better. In mocks 54 and 56 the
marker moved (White over Jalen Williams at #34; Poeltl over Tari Eason at
#82) but the owner's actual pick or the swap rule produced the same roster
either way; in mocks 51, 52, 57 and 58 the guard never let it move, the two
pre-F8 rooms because the internal market positions make every Top-5 row look
scarce. The verdict stands as pre-registered: one room up, one down, the
mean down by 0.14 and 0.32 points, so the marker does not move in v40. The
read itself ships: when it fires, the advice line says who likely waits,
who is the scarcer row and what the pair would gain, and the owner decides.

## 3. Integration — the build and its gates

| gate | result |
|---|---|
| red tests before the code | card suite 17 new cases FAIL, draft suite 1 new case FAIL, the mock-59 history drive 4 of 19 FAIL (the three stale lines plus one over-broad check, narrowed) |
| deck `check_planes.py` | 314 shared · team 0 · exclusion 0 · drift 0 · propagation 0 (no waivers) · lines 171 |
| deck freshness stamp | quiet-day stamp: no pool change asserted; gate 4 holds the pool to the v39 manifest hash `1ecfb66bdcef` |
| deck `build_deck.py` gates 1–7 (v40) | all pass; market `yahoo-2026-10-01.csv` priced 297 of 334; injection round-trip OK; "safe to publish" |
| deck `check_parity.py` on the built page | PARITY: EXACT MATCH (208 owner turns across 16 states; 324 market ranks; 12 survival probabilities bit-identical) |
| deck `test_card.py` / `test_draft.py` / `test_gates.py` on the built page | all 88 / all 65 / all 37 cases passed |
| deck `full_dom_check.mjs` on the built page | 128 assertions, 0 failed, 0 page errors (`arena/results/full_dom_check_2026-10-01_v40.json`) |
| deck `history_dom_check.mjs`, mock 59's 161 events on the built page | 19 checks, 0 failed, 0 page errors (`arena/results/history_dom_check_2026-10-01_v40.json`) |
| experiment validity | the blend chain reproduced every room's recorded `follow_card_selfconsistent` swaps (8 of 8) |
| kit `check_report.py` | PASS (this file) |
| kit `check_provenance.py` / `check_derived.py` | PASS / 13 of 13 (no kit data changed) |
| artifact publish | Version 40 (id `1790898430-fba4`) at the standing URL; page 379,701 bytes, sha256 `1d8be64c7a691996…` |

## 4. Integrity

| check | result |
|---|---|
| planes gate | 314 shared · team 0 · exclusion 0 · drift 0 · propagation 0 (no waivers needed: the thirteen reconciled lines now match on both planes) · lines 171 |
| pool | unchanged from v39 (sha `1ecfb66bdcef`); the stamp asserts no pool change and gate 4 holds it to the manifest hash |
| roster verification | the 2026-10-01 evening direct-complete run (333 of 334, 0 mismatches) stands; nothing on a roster moved in this change |
| kit `check_provenance.py` / `check_derived.py` | PASS / 13 of 13 reproduce (no kit data changed) |
| git state at merge | both mains fast-forwarded, working trees clean |

## Watchlist

- **Mock 60 on v40**: the first live room with the two-pick 🎯 on the card.
  Each turn where the marker moves is logged in the advice line; the retro
  (`live_retro.py 60 pairarms`) grades the chain it would have produced.
- **The thresholds**: 0.01 and 0.60 were set before the experiment and not
  tuned to it. Revisit only with a pre-registered bar, after mock 60.
- **Survival on your own league**: the price-only model is calibrated on
  public Yahoo rooms. Last year's draft (156 picks) is in the deck repo but
  carries no pre-draft ADP; a Yahoo export of that season's pre-draft ranks
  is the one upload that would let the model be refit on your eleven
  opponents (D40-2).
- Carried: D-ADP-1/2 (next pull), the league settings screenshot, the
  preseason refresh after 10/5 (WO-5) for the other 171 differing lines.

## Open-item receipts

| item | query run (2026-10-01) | dated finding |
|---|---|---|
| (this change) | machine joins, replays and gates only — no web research | the 10/01 daily pull's receipts cover the window |
| Jalen Duren, Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the daily pull's dedicated queries, same day (after-report-2026-10-01.md) | all HELD on 2026-10-01; no roster row changed in this deck version |

## Bounds

- The experiment replays finished rooms with strict pairwise swaps: the
  other eleven seats draft exactly as they did, so a chain never changes
  what opponents do in reaction. It measures the owner's roster under two
  rules on the same rooms, not a new truth about the rooms.
- Survival prices for mocks 51 and 52 are the internal market positions the
  pre-F8 page used; the rule almost never fires there by its own guard.
- The thresholds and the independence assumption inside the pair sum are
  the rule's two modelling choices; both are named in the engine comment and
  the design document.
- The history re-render changes no state and no ordering; an undo of an
  insert remains unbuilt (D40-3).

## Decision sheet (owner disposes)

| id | decision | default if silent |
|---|---|---|
| D40-1 | The marker switch (`PAIR_MARKER`) follows the pre-registered rule's verdict as shipped in v40. Override? | keep the verdict |
| D40-2 | Export last season's pre-draft ADP from Yahoo (the draft results page's pre-draft rank column, or the draft-analysis list from that October) so survival can be refit on the league's own eleven managers. | wait on the upload; public-room calibration stands |
| D40-3 | Undo of an Insert-at-# on the page (a pre-insert snapshot and a one-click reverse, as `hoops.py` keeps on disk). | after mock 60 |

## Provenance

Every number in §1 and §2 is read from the named result files; the suites'
counts are the suites' own summary lines; no web research in this report.
