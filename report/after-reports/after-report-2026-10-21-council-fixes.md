# The Council's fixes, built — 2026-10-21

Pull window: 2026-10-21 → 2026-10-21 (build only; no roster pull, no box scores, no projection line or tag changed).

**Owner's request.** "Merge and build council's fixes", 2026-10-21, after the Council's 4–1
verdict on the red-team audit. That verdict proposed one structural fix and two near-term items:
- the structural fix: a **run-ledger** — every gate writes `{name, ran_at, engine_commit, verdict}`
  to one append-only file, `check_claims` consumes it, and the red-team fingerprint check becomes
  a query on it;
- near-term: **pick the recovery number** (D-PM-4) and **wire `check_claims`** (D-CLAIM-1);
- separately: a **separate-attacker re-implementation of the simulator** from its spec.

**What was analyzed.** Kit `main` at **09acd70** (after the #147 merge) and deck `main` at
**d33942f**. The audit report as merged, `arena.weekly_availability` and its JS twin,
`hoops.availability`, `co_gm.rosters` (the IL rule), `league_state.json` of 2026-10-20, the
season pool of 10/21, `scripts/gates.py`, `scripts/check_claims.py`, `scripts/morning.py`,
`scripts/redteam/*`, and the morning scheduled task's stored prompt.

**Method choices, stated to the owner before the runs that used them:**
- M1: the recovery number is **0.0**. The runner-up was 0.09.
- M2: D-CLAIM-1 is option (b). A claim fails the gate only when it changes.
- M3: the ledger fingerprints the last engine-file commit and the deck HEAD.
- M4: the attack's scope is the simulator's deterministic layer, compared exactly, plus the
  season Monte Carlo, compared within |z| ≤ 3. Tolerances were committed before the attacker's
  output was read.

**Headline.** ⟨HEADLINE⟩

---

## 1. Roster changes and the merge

No roster moved and no line or tag changed. **PR #147 is merged** (`09acd70`), but only after
re-measuring turned up three more false passages in it, which were corrected first:

| passage in the audit report | what was true | fixed |
|---|---|---|
| §4 follow-on, receipt row, decision sheet and pull-log still argued from the withdrawn "relative gap" | the withdrawal had been applied to the headline paragraph only | all four rewritten |
| "27 risk / 5 mild / 5 recovery/out (… Suggs …)" | **22 / 2 / 4**, the same on both pools; Suggs carries no injury tag; 27 / 5 / 5 could not be reproduced from any pool | yes |
| "the league simulator reads real league rosters — so it does see them, at 0.60" | all four recovery players are in **IL slots**, and the owner's D-IS-8 rule (2026-10-20) already counts IL as zero; the 0.60 reached **no** rostered player in-season | yes |

The PR's title and body still stated the withdrawn finding as fact. Both were rewritten before
the squash, so the commit message on `main` is accurate. These are errors **#11 and #12** in the
audit's inventory.

## 2. D-PM-4, recovery: 0.60 → 0.0 in the simulator

**What changed.** In `arena.weekly_availability` (deck), a `-recovery` tag now returns
**0.0** instead of 0.60, and so does a tag containing `recovery`. The JS twin `weeklyAvail` in
`docs/draft-deck.html` changed identically. The board's `hoops.availability` was already 0.0
and is untouched.

**Why 0.0 (M1).** Three sources point the same way. The owner's ruling of 2026-07-12 took
the board to exclusion and retired 0.60 there. The deck `LESSONS.md` item 5 records that real
2025-26 recovery players played **~9% of games against 60% assumed** (EVIDENCE: the file).
And a returning player is re-tagged `-risk`, which prices him at 0.75, so a recovery tag means
"not playing now", the same meaning D-IS-8 gives an IL slot. The runner-up, 0.09, was rejected
because it would count a player's return twice: once in the 0.09 and again when the re-tag
lifts him to 0.75.

**Effect today: none on any in-season number.** All four recovery-tagged rostered players
(Strus, M. Williams, Butler, Nurkić) are in IL slots, and the simulator already drops them
(measured with `co_gm.rosters` on league_state 2026-10-20). The change governs the draft and
arena simulations, and any future recovery-tagged player stashed on a bench instead of IL.

**Verification.** Red-first: two recovery tags were added to `test_card.py`'s three-engine
twin case, and **2 of 103 cases failed** on the old engine (Python and page both returned
0.6). After the change: test_card **103/103**, test_draft **67/67**, test_gates ⟨GATES⟩,
check_parity ⟨PARITY⟩. The constants registry caught the change on its own (`CONSTANTS CHECK:
FAIL … recovery 0.6 != 0.0`), proving the drift detector works. The registry entry now carries
the new value, its basis and its in-season effect; check is **PASS 31 = 31**.

**Not changed, and flagged.** `out-*` tags score **0.88** in the simulator, the healthy
rate, because `weekly_availability` has no `out-*` branch. The board excludes them at 0.0.
None is rostered (they are unsigned, retired or overseas), so no current number moves, but a
future `out-*` player on a roster would be simulated as healthy. **Out of scope, flagging:
`arena.weekly_availability` lacks the `out-*` → 0.0 branch its own comment says it mirrors —
one line plus its JS twin. Not touched.** The separate attacker's spec followed the
documented intent here, and its divergence on exactly these tags is predicted (§5).

## 3. D-CLAIM-1 (b): `check_claims` is a gate

`check_claims.py --gate` passes only when **every claim's verdict equals its recorded
`expected`**. A claim known to be false (CL-1..CL-3) does not block a build. A claim whose
truth *changes*, in either direction, does block it until the registry is updated to say so.
`scripts/gates.py` now runs it as its **last gate on every invocation**, unless `--no-claims`
is passed.

- Live: `CLAIM GATE: 7 claim(s), 7 as expected` ⟨confirm at gate time⟩.
- Tests: `gate_code` returns 0 when all rows are as expected, 1 when one has changed, and 1 on
  an empty registry.

## 4. The run-ledger

`scripts/run_ledger.py` writes `report/run-ledger.jsonl`, one JSON object per line:
`name, ran_at, verdict, kit_head, deck_head, engine_commit, detail`. The file is only ever
opened in append mode, and `.gitattributes` merges it with git's built-in `union` driver, so
appends on two branches (the morning run's `season/daily` and `main`) never conflict.

**Producers.**
- `gates.py`: each gate, as it finishes. It records before the next gate starts, so
  `check_claims` sees this run's rows.
- `morning.py`: each step, as `morning: <step>`. Non-fatal: an unwritable ledger never fails
  the morning run. A SKIPPED step writes no row, because it did not run.
- `run_attacks.py --check`: one row named `run_attacks`.

**Consumer.** `check_claims` has a new kind, `ledger_pass`. It returns SUPPORTED only if the
named gate's latest row PASSED, optionally within `max_age_hours` and on the live engine
commit. It is the only check kind that tests "it ran" rather than "it is wired".

**Two seeded claims.**
- **CL-6**, "the red team's attack records describe the live engine". This is the fingerprint
  check as a ledger query. Expected FALSIFIED: the records predate today's engine change, and
  re-running the sweep is D-RT-STALE.
- **CL-7**, "the kit report gate has run and passed". The known-answer SUPPORTED control.

**The fingerprint (M3), and why it matters.** On first run the ledger showed deck HEAD
`d33942f` but the last engine-file commit as **`7a43a25`**. So the audit's "stale: 259c630 vs
d33942f" compared two HEADs that ran the *same* engine. The ledger records both values; the
attack runner's stricter HEAD rule is unchanged. While I built this, the first row ever
written exposed a defect: it was recorded while the engine file had uncommitted edits, and
claimed the old commit. The fingerprint now appends **`+dirty`** in that case, a test pins
it, and that row was discarded before the file's first commit.

**Verification.**
- Red-first: against `main`'s `gates.py`, `morning.py` and `check_claims.py`, the new tests
  give 6 errors (plus one environment failure from running outside the repo). Green: 16/16.
- Kit suite **⟨SUITE⟩**. The suite never touches the real ledger: tests pass a temp path, and
  `report/run-ledger.jsonl` did not exist after a full run.

**Bound.** A scheduled run cloned without a push credential (the documented fallback) leaves
its ledger rows in its container. They reach `main` only through the `season/daily` PR. That
gap is named in `check_claims`'s docstring.

## 5. A-9: a separate attacker re-implements the simulator

⟨A9⟩

## 6. Every gate, pass or fail

⟨GATES-TABLE⟩

## Watchlist

- **`out-*` → 0.88 in the simulator** (§2). No rostered player today. One-line fix, flagged.
- **CL-6 FALSIFIED by design** until the sweep is re-run (D-RT-STALE). The gate then fails
  until CL-6's `expected` is updated, which is the intended signal.
- **Morning-run ledger rows** reach `main` only by the `season/daily` PR (§4 bound).
- **Arena mock scripts** (`arena/mocks/decw_third.py`, `injured_rivals_cf.py`) keep their own
  historical copies of the 0.60 tier. They are dated research records, not the engine, and
  were deliberately not edited.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| PR #147 | **MERGED** | `09acd70`, after three passages were corrected (§1) |
| D-PM-4 recovery | **BUILT** | 0.60 → 0.0, Python and JS; red-first 2/103 → 103/103; registry PASS |
| D-PM-4 risk/mild | carried | needs the composed per-player comparison (tier × `avail(gp)` vs simulator) |
| D-CLAIM-1 | **BUILT (b)** | `check_claims --gate` is the last gate in `gates.py` |
| run-ledger | **BUILT** | `scripts/run_ledger.py`; three producers; `ledger_pass` consumer; 16 tests |
| A-9 simulator attack | ⟨A9-RECEIPT⟩ | `report/after-reports/redteam-sim-2026-10-21/rt_sim.json` |
| D-RT-STALE | carried | the sweep is not re-run (owner's call); CL-6 now tracks it |
| D-INT-1 | carried | provenance writer not built (owner's call) |

## Repeat-name market check

Not applicable: no market source was pulled and no pool row changed, so no new name can
collide.

## Decision sheet

1. **Merge the two PRs** (kit and deck). Merging is your word.
2. **The `out-*` branch** (§2): add `out-*` → 0.0 to the simulator and its JS twin, so it
   matches its own comment and the board. *Recommended: yes, one line each; zero effect on
   today's numbers.*
3. **Morning prompt:** after the kit PR merges, add `report/run-ledger.jsonl` to the list of
   paths the morning run commits. Without that, its ledger rows are never saved.
   *Recommended: yes, the same day as the merge.*
4. **D-RT-STALE:** re-run the assumption sweep on the new engine. That is what turns CL-6 and
   the four attack records current. *Recommended: yes, scheduled; hours of compute.*
5. **D-PM-4 risk/mild:** run the composed per-player comparison before touching 0.78/0.75 or
   0.85/0.79. *Recommended: yes, as a measurement first.*

## Bounds

**Out of scope by design.** The sweep re-run, the provenance writer (D-INT-1), the `out-*`
branch, and any change to risk or mild values. No new scheduled task was created, and the
morning task's prompt was not edited before the kit PR is merged.

**In scope and unverified.** ⟨BOUNDS⟩

## Provenance

Session `session_01QjgeRdpDaWgSJmGKRG8fTU`, 2026-10-21. Governors: plan-gate **loaded for this
task** (full block emitted before the first change); adversarial-verify ⟨AV⟩. Separate
attacker: one subagent, spec and fixture only, ⟨A9-COST⟩. Kit base `09acd70`, deck base
`d33942f`.
