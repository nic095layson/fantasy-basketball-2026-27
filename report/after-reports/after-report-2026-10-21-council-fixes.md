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

**Headline.** All four of the Council's fixes are built and tested, and #147 is merged. Making the
first fix exposed three more false passages in #147, all corrected before the merge.
- **The recovery number is now 0.0 in the simulator.** It changes no current in-season
  number, because all four recovery players are on IL, which your D-IS-8 rule already zeroes.
- **`check_claims` is a gate.** A claim fails the build only when its truth changes.
- **The run-ledger exists.** "Ran and passed" is now a recorded fact rather than a
  recollection, and on its first run it showed that today's "stale engine" was the same
  engine under a different deck HEAD.
- **The simulator survived its first separate-attacker test.** An agent that never saw the
  code rebuilt it from a written spec. It agrees bit-for-bit on every deterministic number
  (2,174 of them: hashes, start weights, team models, category probabilities, expected wins), and within noise on title and playoff odds (max |z| 2.06 over 24).
- **It diverged in exactly the one place I predicted beforehand:** the 9 `out-*` tags,
  which the simulator prices as healthy, contrary to its own comment. That is flagged, not
  fixed.

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
(measured with `co_gm.rosters` on league_state 2026-10-20). Checked behaviourally, not
argued: all 12 in-season team models were built under 0.60 and under 0.0, and **0 of 216**
numbers differ. No caller passes `include_il=True`, and the free-agent scan filters on the
board's availability, which is unchanged. The change governs the draft and
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

- Live: see §6. The gate runs last in `gates.py`, after the report gate has written its ledger row (CL-7).
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
- Kit suite ****219/219****. The suite never touches the real ledger: tests pass a temp path, and
  `report/run-ledger.jsonl` did not exist after a full run.

**Bound.** A scheduled run cloned without a push credential (the documented fallback) leaves
its ledger rows in its container. They reach `main` only through the `season/daily` PR. That
gap is named in `check_claims`'s docstring.

## 5. A-9: a separate attacker re-implements the simulator

**What it is.** The board engine's arithmetic was verified this way on 2026-10-21 (1,800 of
1,800 cells). The simulator, the part that produces title odds and the weekly matchup
probabilities, had never been attacked like that. I wrote `SPEC.md` from the simulator's
docstrings and comments, and `fixture.json` from the real inputs. One subagent was given those
two files only and forbidden the source. It reports opening only them (EVIDENCE: its hand-back
lists every file it opened). It wrote `attacker.py` (stdlib only), and `compare.py` runs the live
engine on the same fixture. All four artifacts sit beside the record in
`report/after-reports/redteam-sim-2026-10-21/`.

**Inputs (M4, stated before the run).** The 12 real league rosters as the in-season simulator
sees them: league_state 2026-10-20, IL slots excluded per D-IS-8, 155 players, lines from the
10/21 season pool, `z_sum` from the verified board engine. Plus all 335 distinct pool notes and
603 hash vectors.

**Result, engine `bcf9ed9` (EVIDENCE: `rt_sim.json`).**

| layer | compared | result |
|---|---|---|
| weekly availability tiers | 335 notes | **326 exact**; the 9 `out-*` notes differ, **as pre-registered** (below) |
| daily-fill hash | 603 vectors | **603 bit-identical** |
| daily-fill start weights | 155 players | **155 exact** |
| team weekly model (mean, variance) | 216 numbers | **216 bit-identical** (max difference 0) |
| head-to-head category probability | 1,188 | **1,188 identical** (max difference 0) |
| expected categories won (`pwins`) | 12 | **12 identical** |
| season title and playoff shares, independent streams | 24 (12 seats × 2) | **max \|z\| 2.06, none above 3** (20,000 seasons each side); a second engine seed (2027): **max \|z\| 2.40, none above 3** |
| season, shared stream (same seed) | 12 playoff shares | **12 of 12 identical to the digit** |

**The predicted divergence happened exactly where predicted, and nowhere else.** The
simulator's own comment says its tiers "mirror hoops.availability", and hoops excludes `out-*`
at 0.0. The code has no `out-*` branch and returns 0.88. The spec followed the documented
intent, so I predicted a divergence on exactly the `out-*` tags. That is what happened: 9 notes,
all `out-*` (EVIDENCE: `diff_out_predicted`). It confirms the §2 flag, and it is behavioural
evidence of independence: an attacker who had read the code would have reproduced the 0.88.

**A surprise, handled without moving a tolerance.** On the first run, both sides happened to
seed Python's generator with 20261021. The attacker had also independently chosen the same draw
order through the regular season and seeding. So the two samples shared one random stream:
**all 12 playoff shares were identical**. That is not the independent sampling the |z| test
assumes, and under shared streams the test is too lenient. The pre-registered method said
"different random streams", so the engine side was re-run on an independent seed (1021). That
gives the |z| row above. Switching made the result look *worse* (max |z| 1.15 → 2.06, and
2.40 on a second seed), and no tolerance moved, so this was not tuning. The shared-stream
result is kept as a separate and stronger check:
with one stream, 20,000 seasons of standings and seedings matched exactly on both sides. Title
shares still differ under the shared stream because the two sides list the final's teams in a
different order. `SPEC.md` left that open; the outcome is distributionally equivalent.

**The comparator was itself tested.** A broadly passing checker is suspect too
(adversarial-verify rule 9). One error was planted per section, for example a model mean off by
one part in a million, a hash value off by 1e-12, or a title share off by 0.03. All seven
sections FAILed, the season at |z| 7.25.

**Registered.** This is attack **A-9** on the standing list (`scripts/redteam/attacks.json`),
CURRENT on `bcf9ed9`.

**What the attacker's notes add** (its six spec gaps, none impossible):
- 137 of 335 notes begin with a date, so their tag is the date and they score healthy. Three
  rostered notes carry injury words after the tag (Kessler, Murray, Haliburton), and all three
  record that the tag was removed. So the healthy reading is intended there.
- Bare tags like `unsigned` and `waived` do not start with `out-`, and score 0.88 even under
  the intended rule.
- §3's "last available day" fallback can never fire, because the hash is always below 1.
- §6 never says whether the 0.06 shock is a standard deviation or a variance. It is a standard
  deviation in the engine, and the attacker read it that way.

None of these changes a number. The `unsigned` and `waived` point joins the §2 flag.

**Bound.** I wrote the spec, and I had read the code. So A-9 tests the code against its *own
documented intent*. It does not test that intent against the world. It is the right test for
implementation bugs, and it says nothing about whether 0.06, 3.5 games a week, or the CV values
are right. That is the sweep's job (D-RT-STALE).

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
| A-9 simulator attack | **PASS, registered** | `report/after-reports/redteam-sim-2026-10-21/rt_sim.json` |
| D-RT-STALE | carried | the sweep is not re-run (owner's call); CL-6 now tracks it |
| D-INT-1 | carried | provenance writer not built (owner's call) |

The flagged-name receipts are carried forward from the lock report. This build pulled
nothing and researched no player, so they were not re-queried (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this build (did not check) |

## Repeat-name market check

Not applicable: no market source was pulled and no pool row changed, so no new name can
collide.

## Decision sheet

1. **Merge the two PRs** (kit and deck). Merging is your word.
   - **Veto line on M1:** if you prefer the measured 0.09 to 0.0 for recovery, it is a
     one-value change in both engines and the registry. Today it changes nothing either way,
     because all four recovery players are on IL.
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

**In scope and unverified.** - **Deck page not republished.** The JS twin changed in `docs/draft-deck.html`, but the draft
  deck artifact was not rebuilt or republished: the draft is over, and nobody asked for it.
  The page's next build will carry it.
- **The 155 players are today's active rosters.** A-9 compares on this fixture only. A layer
  these rosters never reach (an `out-*` or recovery player on an active roster, a five-game
  week drawn on every day) is exercised by the 335-note tier check and the hash vectors, not
  by a roster.
- **The morning task was not run end to end with the ledger.** `test_morning` covers
  `run_steps` writing rows, and the real morning run at 5:53am PT is the first live exercise.
  It runs on `season/daily`, built from `main`, which does not carry this code until the PR is
  merged. So tomorrow's run is unaffected either way.

## Provenance

Session `session_01QjgeRdpDaWgSJmGKRG8fTU`, 2026-10-21. Governors: plan-gate **loaded for this
task** (full block emitted before the first change); adversarial-verify ⟨AV⟩. Separate
attacker: one subagent, spec and fixture only, about 106k tokens, 17 tool calls, 6 minutes. Kit base `09acd70`, deck base
`d33942f`.
