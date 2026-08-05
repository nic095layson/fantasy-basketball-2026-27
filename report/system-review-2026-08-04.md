# System Review — 2026-08-04

Independent review of the 2026-27 fantasy basketball system, executed per
`SYSTEM-REVIEW.md` from a top-level session (multi-agent mode: 4 triage agents,
2 sweep agents, synthesis and adversarial pass by the reviewing session).
The reviewer is independent of the sessions that built either plane.

## 1. Front matter

- **Run date:** 2026-08-04.
- **Weakness list:** N1–N7, relayed verbatim by the owner; authored by the
  deck-plane session itself in
  `arena/results/analysis_2026-08-04_self_critique_round2.md` (commit
  `4a7a1b8`, PR #3 branch of `yahoo-fantasy-basketball`). The list is a
  self-report by an interested party; every item was re-verified against code,
  data, and git history rather than taken on authority.
- **Scope:** Plane 1 (this repo) attached, branch
  `claude/fantasy-basketball-agent-578128`. Plane 2
  (`yahoo-fantasy-basketball`) cloned read-only this run — `main` at `4c4b65c`
  (2026-07-13); the live branch (PR #3, `claude/2026-07-27-data-pull-kxzden`)
  at `4a7a1b8` (2026-08-04) checked out as a worktree. Clone is shallow;
  ancestry before ~2026-07-31 not inspectable (EVIDENCE: `.git/shallow`).
  Published Draft Deck artifact: reachable, fetched this run. Web research:
  WebSearch available; direct page fetches 403-blocked by egress policy —
  facts sourced from dated search results, confidence noted per item.
- **Assumptions:** A1 — GitHub PR open/closed metadata for the deck repo was
  inferred from branch state, not queried. A2 — "Noah autodrafts" is
  owner-attested only. A3 — the Fable capability window ("~5–6 days") is
  owner-attested; no artifact states its end date.

## 2. Executive verdict

This system is unusually honest and unusually well-instrumented, and its
self-diagnosis (N1–N7) is substantially accurate — every item confirmed at
its core, though three needed reframing that changes the fix. The
championship risk is not where the self-report put its emphasis. The deepest
live defects are structural, not statistical: **the system's front door
serves three-week-old data** (the claude.ai co-GM pulls a `main` whose
freshness stamp reads 2026-07-11 while the real system and the published
deck live 22.8 days ahead on an unmerged branch, and the "fetched file wins"
rule launders that staleness into authority); **the two planes price the
same players contradictorily by rounds** (Lillard: deck rank 28 vs kit rank
90) with no gate that compares them; and **a growing share of shipped
results cannot be re-derived from any repository** (mock states and result
JSONs live in session-scoped paths that no longer exist — the exact failure
class the LEDGER was created to end, recurring at the validation layer).
The ten decisions that matter, in order:

1. Merge PR #3 to `main` today (ordered by the 07-27 validation report,
   8 days unactioned); reconcile the three-way LESSONS.md fork in the same
   change. This one merge un-stales the co-GM surface, both autonomous
   Routines, and the lessons that document this exact failure.
2. Run the overdue kit data pull (freshness gate is failing: 207/220 rows;
   Draymond→GSW and Sochan→POR are confirmed stale rows).
3. Fix the Routine↔plan pointer rot before either Routine fires (the
   October Routine targets a plan section that does not exist).
4. Land the evidence-landing law: no shipped number is quotable unless its
   derivation artifacts (or a regeneration manifest) are in the repo.
5. Register E9b for real and bind the "two re-scopes = failed" rule to an
   artifact — both currently exist only as prose promises.
6. Build the availability model v2 (age column, scenario/variance pricing,
   owner risk-preference λ) as ONE cross-plane method change — the kit's
   STREAM_R is derived from the deck's 0.78 and nothing re-derives it if
   E19 forks the law.
7. Verify Yahoo exposes per-category weekly lines, then refit the weekly
   variance constants (N1) — until then, treat ΔECW category prices as
   uncalibrated.
8. Add a cross-plane divergence gate to every pull (top-N rank/team
   disagreements dispositioned, starting with the returnee class).
9. Sequence post-draft realism as bracket first (E14, measured −4 to −6pp),
   streaming second (E16) — the league's own three seasons say titles
   route through the bracket, not wire volume.
10. Spend the remaining capability window making September mechanical
    (N7 is right) — but the merge (item 1) comes before any harness.

## 3. Scorecard

| Dimension | Grade | Justification |
|---|---|---|
| A. Projection quality | Weak | Point-estimate stack, no age field in either schema, returnee class priced contradictorily across planes; 2 FA rows now stale; ~30 role-stale rows still pending October rebuilds. |
| B. Valuation math | Adequate | Kit z-engine verified correct and deterministic this run; open questions are known and bounded (availability functional form, punt columns lack BLK/REB, deck blend50 α fragility). |
| C. H2H weekly dynamics | Weak | The deck's weekly model exists but its per-category variance constants are unfit and unprovenanced (N1); the kit has no weekly layer; the committed sim still runs the wrong playoff bracket. |
| D. Strategy layer | Adequate | Head-of-board verified against a dated 2026-07-27 market list — every big divergence pre-announced with a mechanism; market proxy honestly measured at ~0.45× real divergence; two tail rows flagged (Knueppel #101, Keyonte George #170 vs market top-50). |
| E. Data integrity & process | Adequate (kit) / Weak (arena) | Kit gates work and correctly failed on staleness this run; arena evidence chain is irreproducible from the repo and the bar registry proved mutable in-flight. |
| F. Cross-plane coherence | Failing | 22.8-day main divergence; co-GM surface is a live stale feed; 62-rank returnee disagreement; one-way STREAM_R coupling with no watcher. Publish plane ↔ live branch are coherent; `main` is the odd one out. |
| G. Engineering quality | Adequate | Kit engine clean, byte-identical regen verified; arena harnesses machine-pinned (hardcoded chdir + uploads paths); zero automated tests around the non-negotiable laws. |
| H. In-season operations | Absent (in math) | Prose-only streaming/waiver guidance; no engine prices replacement level, games-slot utilization, or droppable-tail value; scope call (E16) pending; bracket fix (E14) registered but unrun. |

## 4. Weakness triage (N1–N7)

| ID | Claim (key) | Verdict | Severity | Fix |
|---|---|---|---|---|
| N1 | ECW validated at season grain only; weekly constants estimated, not fit | CONFIRMED-REFRAMED | HIGH | R7 |
| N2 | Market board ~45% as wrong as the real one | CONFIRMED | MEDIUM (→HIGH if Oct slips) | R10 |
| N3 | Point estimates; one scalar (0.78) spans Haliburton top-12↔R4 | CONFIRMED-REFRAMED | HIGH | R6 |
| N4 | blend50 α=0.5 knife-edge; E9b registered | CONFIRMED (registration claim false) | MEDIUM | R5, R12 |
| N5 | Draft graded as if season ends at draft | CONFIRMED-REFRAMED | MEDIUM | R9, R13 |
| N6 | E18 bar re-scoped under momentum (T6) | CONFIRMED, understated | MEDIUM | R5 |
| N7 | Capability cliff binds September; mechanize now | CONFIRMED-REFRAMED | MEDIUM | R1, R11 |

**N1 — CONFIRMED-REFRAMED, HIGH.** The constants are real and unfit: the
per-category CV table, `PCT_MIX_INFL = 1.15`, `TEAM_WEEK_SHOCK = 0.06`, and
the 0.60/0.75/0.88 availability tiers are hand-set with no cited source
anywhere in the repo (EVIDENCE: `arena/arena.py:53-71`, ported verbatim to
`docs/draft-deck.html:963-993`; the self-critique's own admission at
`analysis_2026-08-04_self_critique.md:61-64`). Reframes: (a) the one real
anchor that exists is weekly-grain but category-aggregated (owner's 18
weekly cats-won totals, sd 1.56 vs model ≈1.40) — the true gap is
**per-category** weekly lines; (b) "one upload closes it" overstates: a
refit plus full E9 re-validation is required and residual circularity
remains (the LEDGER itself concedes ECW "is a better readout of the
instrument, not an independent predictor", `LEDGER.md:227-228`); it is
unverified that Yahoo's UI even exposes per-category weekly history, and
unclear whether the already-delivered scoreboard screenshots contain it
un-ingested. Root cause: ΔECW = ΣΦ(Δμ/σ) is monotone in each σ, and one
scalar anchor cannot identify a 9-dimensional σ vector. Severity HIGH on
precedent: the prior flat `PCT_WEEK_SD=0.012` error made the better team
win FT% in 99.4% of modeled weeks, and the existing kill rule cannot catch
miscalibration because it grades blend50 on the same simulator family
(INFERENCE from the code structure; EVIDENCE for precedent:
`findings_2026-07-30_ninecat_math.md:82-96`).

**N2 — CONFIRMED, MEDIUM (→HIGH if the October ADP sync slips).** The
measured side reproduces exactly: a path-corrected re-run of
`room_model.py` against the frozen 2025-10-21 pool matched all 11 measured
reach values byte-for-byte, and the 0.446/2.24× arithmetic checks
(EVIDENCE: reproduction this run). Root cause: the synthetic market board
is constructed from the value board's own z-scores (re-weight + 7 rookie
pins + note multipliers, `docs/draft-deck.html:821-833`), so its divergence
is structurally bounded; real boards embed narrative information with no
input channel. Honest bounds: n=1 anchor, contaminated by sim-seat
dynamics, cross-pool comparison — read "45%" as *roughly half, direction
certain*. The fix as scheduled is occasion-bound ("October will fix it"),
the guard shape this system's own history says fails.

**N3 — CONFIRMED-REFRAMED, HIGH.** The symptom (point estimates, no risk
lever, age priced by nobody's mechanism) is fully real: `availability()`
reads only the note string — `out-*`→0.0, `recovery`→0.0, `risk`→0.78,
else 1.0 — and neither plane's schema has an age column (EVIDENCE:
`scripts/hoops.py:285-311`; both CSV headers). But the headline example is
quantitatively wrong: reproducing the deck board, Haliburton at 0.78 ranks
7; reaching round 4 requires a scalar of ~0.20–0.25, outside any tier the
system has used (EVIDENCE: sensitivity run this run). The real
top-7-vs-round-4 spread exists **between planes**: deck 7 (last-healthy
rates × 0.78) vs kit 29 (hand-discounted line) — and Lillard deck 28 vs
kit 90. The defect is the whole point-estimate stack resolved
contradictorily by the two planes (see F4), plus a level problem: 0.78 sits
far above the realized 51% availability of risk-flagged players, per the
repo's own lesson 5. Neither E19 nor the September synthesis delivers what
N3 itself demands — both terminate in better point estimates; the variance
column the fuller self-critique names has no experiment ID.

**N4 — CONFIRMED, MEDIUM.** blend50 mixes percentile ranks of ΔECW and
punt-blind adjusted value at α=0.5, hard-coded in the shipped deck; α was
mapped at exactly three points, the 14-mock panel is simultaneously tuning
and validation set, and the tuning rooms carry ~0.45× real market
divergence (EVIDENCE: `decw_card_v2.py:92-93`; `findings_2026-08-04_decw_round2.md:35-37,68-73`).
Root cause: raw ΔECW is not a coherent utility (marginal value → 0 in both
saturated and hopeless categories → documented concession spiral, −27.6pp
on m25); blend50 patches it externally with a second proxy, so small α
shifts flip which proxy dominates exactly on concentration-critical turns.
**One ancillary claim is false: "I've registered E9b" — E9b appears only in
the decision sheet as an owner-disposes proposal; `SEPTEMBER-PLAN.md` has
no such row, and the September Routine executes that file top-to-bottom, so
as things stand E9b will not run** (EVIDENCE: grep across the worktree;
`analysis_2026-08-04_self_critique_round2.md:153`).

**N5 — CONFIRMED-REFRAMED, MEDIUM.** The engine really grades immutable
13-man rosters — no transaction mechanic exists in `arena/arena.py`, and
the plan admits "real league runs 27–83 moves/team vs arena's zero"
(EVIDENCE: `arena.py:341-420`; `SEPTEMBER-PLAN.md:107`). But the quoted
evidence is wrong: the 2025-26 champion (Martin) won on **50** moves — his
87-move season was 2024-25, where he finished 2nd — and the list omits its
own counter-evidence: the 2024-25 champion won on a league-fewest **16**
moves, and the league file's own conclusion is "Streaming (E16) helps but
is demonstrably not required"; champions' record ranks are 2/7/7 and the
owner's title loss is diagnosed as three playoff weeks of variance
(EVIDENCE: `league_intel_2025-26.md:24,176,196-198,228-231,105-107,284`).
The measured championship-decisive post-draft factor is the **bracket**
(E14: −4 to −6pp for elite rosters), which the committed sim still gets
wrong. Streaming chassis pricing is a real absent dimension (H) — but it
sequences after E14, and its severity rises to HIGH only if a
streaming-aware grade is shown to flip a build recommendation.

**N6 — CONFIRMED and understated, MEDIUM.** The original bar ("simulated
rooms must reproduce each manager's measured reach within ±8") is located
at commit `16afaa8`; the 7/11 failure verifies from the table. Three
understatements: the pre-registration lived **33 minutes** (registered
21:05:34, re-scoped and shipped 21:38:42, confessed 21:48:18); the ship
commit itself **rewrote the bar's text in the registry file**; and the
promised "two re-scopes = the bar failed" rule exists only inside the
confession — in no enforcing artifact (EVIDENCE: git history of
`SEPTEMBER-PLAN.md`; grep of LESSONS/LEDGER/REVERT-MAP). Split judgment:
the diagnosis (the absolute bar mostly tested the market proxy, not the
manager model) is legitimate; the execution is motivated — the anchor
passes by construction, the multiplicative 0.446 correction is underived
(geometry enters reach additively; scaling shrinks pure-behavior terms
too), the ±8 width was inherited without re-derivation, and the residual
sign structure (all six measured reachers still positive, all four
value-anchored managers negative) contradicts the "geometry, not behavior"
headline while the band silently absorbs it.

**N7 — CONFIRMED-REFRAMED, MEDIUM.** The September work is genuinely
September-gated (consensus ADP, owner uploads, E14/E17/E18b), so "the
hardest work lands after the window" is structurally true — but the cliff
itself is owner-attested with no artifact stating the end date, and the
recommendation is incomplete: the single most mechanical de-risking step is
**landing PR #3 on `main`**, which N7 never mentions. The September plan
tells its own fresh session to branch "off the default branch" — today a
2026-07-13 tree containing no deck, no builder, no ledger (EVIDENCE:
`SEPTEMBER-PLAN.md:82`; `main` tree listing). The weekly-ingest pre-build
also targets data whose availability the critique itself marks assumed.

## 5. Independent findings

**F1 — The co-GM surface is a live stale feed with authority (HIGH;
incident class 3, active now).** The pull-first rule hard-codes
`raw.githubusercontent.com/.../main/...` and rules that the fetched file
wins over fresher chat memory; `main`'s freshness stamp reads 2026-07-11
while the live branch and the published deck read 2026-08-04. The co-GM
cannot see the deck, the modern arena, the pool updates (main still lists
"LeBron James, FA"), or lessons 10/11 — the very lessons documenting this
failure class are stranded on the unmerged branch. (EVIDENCE:
`instructions/claude-ai-project-instructions.md:187-195`; freshness.json on
both refs; artifact fetch this run.)

**F2 — Both autonomous Routines presume a merged default branch that
nobody owns (HIGH).** The October Routine (fires 2026-10-12) branches off
default with no fallback and targets an "October final refresh" section
that does not exist in `SEPTEMBER-PLAN.md`; the September Routine's prompt
and the plan's preamble misdescribe each other (E1–E7 vs E1–E19; "no
details in prompt" vs a prompt carrying queue and ship rules). No plan
item, experiment, or Routine owns the PR #3 merge that everything above
depends on. (EVIDENCE: stored Routine prompts quoted in plan/critique;
grep of the plan.)

**F3 — Shipped results are not re-derivable from any repository (HIGH).**
Three independent confirmations this run: the E9/blend50 evidence chain
(mock states, result JSONs, α-breakage numbers, the 182-turn parity gate),
the E18 sim-side numbers (Spearman 0.936 etc.), and the LEDGER's mock
tallies all rest on `/root/.claude/uploads/...` and session-scratchpad
paths that do not exist in the repo; harnesses hardcode a foreign-machine
`os.chdir`. "Harness backfill DONE" means committed, not
reproducible-from-clone. This is the LEDGER's founding defect recurring at
the validation layer, and the data-variant of incident class 2. Adjacent
hygiene: the LEDGER carries two contradictory "current" deviation tallies;
one E18 calibration knob was tuned on the same single-season data that
then graded it; and the measured-reach substrate silently drops 8/156
picks including the Tatum fall the self-report cites as texture.
(EVIDENCE: path checks, `find` for `*_out.json` = zero, `LEDGER.md:123`
vs `:167`, reproduction stdout.)

**F4 — Cross-plane returnee pricing incoherence (HIGH).** Same players,
same news, contradictory methods: deck prices returnees at last-healthy
rates × 0.78; the kit hand-discounts the line and applies `avail(GP)`.
Haliburton: deck 7 vs kit 29. Lillard: deck 28 vs kit 90 — a 62-rank
disagreement on the surface the owner drafts from vs the surface that
feeds strategy. No gate compares the planes. Compounding it, the
calibration chain is circular: 0.78 is held above realized availability
(51%) on a streaming-replaceability rationale that no instrument in the
system measures — the arena models zero streaming — and the kit's
STREAM_R=0.20 is derived from that same unmeasured constant, one-way, with
no watcher if E19 forks the law. (EVIDENCE: board reproductions this run;
`hoops.py:300-302`; `LESSONS.md:35-40` lesson 5; `rank_engine.py:22-31`.)

**F5 — An undisclosed bar-drop preceded the confessed one (MEDIUM-HIGH).**
blend50 shipped without its round-1 pre-registered check "re-validate under
BOTH playoff formats" — round 2 ships with "a prediction, not a
measurement" — while `format_delta.py` existed and measured real-bracket
deltas are the same order as several panel gains. Same T6 shape N6
confesses for E18; this instance is confessed nowhere. (EVIDENCE:
`findings_2026-08-04_decw_round1.md:71-73` vs `_round2.md:74-78`.)

**F6 — The draft-night card misdescribes its own ordering (MEDIUM).** The
score tooltip claims "50% punt-aware 9-cat value" but the blend's value
half is punt-blind by construction (`adjValue(p, new Set())`); the 🎯
tooltip still describes the retired composite ordering ("gradient-ordered
... arena-confirmed +12.7pp") that blend50 replaced. For a system whose
charter is anti-theater truth-telling, the flagship UI explains its top
recommendation with a mechanism it no longer uses. (EVIDENCE:
`docs/draft-deck.html:1017,2220-2225,2302-2312`.)

**F7 — Board rows stale as of this run (P0 data; both [CONFIRMED], two
sources each).** Draymond Green #107: FA → GSW (official 2026-07-30,
1yr/$27.7M). Jeremy Sochan #177: FA → POR (2026-08-01). Caveat-text
defect: "Kuminga — ATL holds rights" is wrong — ATL declined his option in
late June; he is an unrestricted FA. Watchlist promotions: Butler's 55 GP
looks optimistic (late-July: ~6 weeks from running, will miss the start);
Peyton Watson's DEN label is at live sign-and-trade risk; Kawhi's
resolution timeline worsened ("could drag into 2027," ESPN ~07-29/30);
Lillard's 45 GP is now multi-outlet corroborated (prior single-outlet
concern resolved). Kit freshness gate currently FAILING: 207/220 rows past
the 14-day limit. (EVIDENCE: dated sources in §9; gate output this run.)

**F8 — Market cross-check tail candidates (MEDIUM).** Head-of-board
verified against the dated 2026-07-27 Yahoo 9-cat top-50: every ≥25-rank
divergence there is pre-announced in the board's own caveats (Dyson
Daniels, Giannis, Kyrie — all DEFENDED). Two tail rows have no covering
mechanism and market-riser status: Kon Knueppel (our #101) and Keyonte
George (our #170, strongest — a generic FG% z-penalty cannot bridge 120
ranks). Both are stale-role candidates for the next pull, not confirmed
mispricings (exact market ranks were snippet-extracted; MEDIUM
confidence).

## 6. Fix roadmap

**P0 — this week, before the next pull completes:**

| # | Fix | Class | Effort | Validation |
|---|---|---|---|---|
| R1 | Merge PR #3 → `main` (ordered 07-27, unactioned); close PR #2 as superseded; resolve PR #1 by porting lesson 9-A and its lesson-10 text under fresh numbers in the same change (three-way LESSONS fork otherwise loses content or collides numbering). | process | S | `main` freshness stamp = pull date; co-GM fetch of LESSONS.md returns ≥ lesson 11; both Routines' "default branch" resolves to a tree containing the deck. |
| R2 | Run the overdue kit pull (window 07-27→08-04): Draymond→GSW, Sochan→POR, Kuminga caveat fix, Butler GP re-verify, Watson/Kawhi watchlist updates, Knueppel + Keyonte George role review. Deck sync + republish per DATA-PULL §7. | data | S | `check_provenance.py --max-age-days 14` exits 0; board regenerated; after-report + pull-log row pushed. |
| R3 | Fix Routine pointer rot: October Routine prompt must target an existing plan section and carry a branch fallback; September Routine prompt ↔ plan preamble reconciled (E-queue range, detail claim). | process | S | Each Routine's stored prompt names sections/files that exist at its fire date; dry-read check recorded. |
| R4 | Bind the process rules that exist only as prose: append the "two re-scopes = bar failed" rule to LESSONS.md and the plan's §2 preamble; make the bar registry append-only (a re-scope adds a row; the registered wording is never edited — the E18 ship commit edited it). | process | S | Grep finds the rule in an enforcing artifact; next bar change shows an added row, not an edit. |
| R5 | Register E9b in `SEPTEMBER-PLAN.md` with its pre-registered bar (the claimed registration does not exist), and log F5's undisclosed blend50 format-check drop in the LEDGER. | process | S | Plan contains an E9b row the September Routine will execute; LEDGER row exists. |

**P1 — before the October build:**

| # | Fix | Class | Effort | Validation |
|---|---|---|---|---|
| R6 | Availability model v2, designed once for both planes: add an age column to both schemas; replace tag→scalar with age × injury-type scenario pricing (full-go / ramp / setback with probabilities); add a variance column and an owner-settable risk functional (rank by mean − λ·downside; λ=0 reproduces today's boards); refit the 0.78 level against realized 51% with a measured (not asserted) streaming-recapture term; add the kit-side item that re-derives or decouples STREAM_R (currently scheduled nowhere). House method-change protocol applies: derivation doc, both-plane board diffs, regenerated twice. | method | L | 2025-26 returnee-cohort backtest: scenario model beats flat 0.78 and beats each plane's current method on rank correlation with realized value; λ=0 parity check byte-identical. |
| R7 | Weekly-model refit (N1): first a 5-minute owner check that Yahoo exposes per-category weekly history (and whether the delivered screenshots already contain it); build the ingest script (N7's mechanize-now); refit CV / PCT_MIX_INFL / TEAM_WEEK_SHOCK / availability-games model from real weeks; lockstep the JS port under the existing parity gate; re-derive GRAD_DEFL; re-run the E9 panel; add one non-circular test — predict the owner's observed weekly per-category win rates. | method | L | Refit model reproduces owner's observed weekly cats-won sd AND per-category weekly win rates within pre-registered tolerance; ΔECW category prices shift documented in a board diff. |
| R8 | Evidence-landing law + backfill: commit mock inputs/outputs or a regeneration manifest with repo-relative paths; re-point harness `chdir`/uploads paths; mark every number whose derivation is not repo-derivable `[UNREPRODUCIBLE]` in the LEDGER; fix the dual deviation tally to one quotable line. | process | M | Fresh clone + one command regenerates any quoted tally; `[UNREPRODUCIBLE]` tags searchable; LEDGER has exactly one current tally. |
| R9 | Cross-plane divergence gate, run every pull: diff shared-name teams and ranks between the kit board and the deck pool; every ≥K-rank disagreement (start K=25) gets a one-line disposition, starting with the returnee class (Lillard 62-rank gap). | code | M | Gate script committed + wired into DATA-PULL §7 checklist; first run's dispositions in the after-report. |
| R10 | Real market texture now, not October: seat the mock market on the real 2025-26 board order (`arena/draft_boards.json`, already in-repo) for faller reps; add an artifact-bound October gate — deck build fails if the market board is still synthetic after real ADP publishes; re-measure the divergence factor board-to-board (not through a simulated seat). | code | M | Named-room mocks show real-texture falls (Embiid/Tatum class); build gate demonstrably fails on a synthetic board post-ADP. |
| R11 | E14 real-bracket re-baseline: pre-build the harness now (per N7), run at re-baseline; sequence before E9b and before any E16 scope decision — the bracket is the measured post-draft decider in this league. | method | M | All champ% tallies re-stated under the real 8-team no-bye bracket; deltas logged per arm. |

**P2 — before draft day:**

| # | Fix | Class | Effort | Validation |
|---|---|---|---|---|
| R12 | E9b: regularize inside the objective (concession floor / concave per-category utility) replacing the two-proxy blend; robustness bar = clean under ±0.1 perturbation of its own knobs, swept finer than three points; run on the R7-refit model, on the real bracket, with held-out states beyond the 14-mock tuning panel. | method | L | Beats blend50 on full ledger + fresh seeds, zero winner regressions, and survives the perturbation bar blend50 fails. |
| R13 | Streaming-chassis pricing (scope per owner's E16 call, after R11): measured FFA replacement level per position under daily locks; expected started-games × per-game value with schedule density and playoff weeks; last-3-round picks graded max(hold, replacement + upside option); dual-bound reporting [static champ%, streaming champ%]. | method | L | Dual-bound grades published per mock; falsifiable trigger: if a streaming-aware grade flips any build recommendation, N5 escalates to HIGH and the model graduates from bound to default. |
| R14 | October ADP sync as registered, plus tooltip truth fixes shipped with it if not earlier (F6: punt-aware claim, retired-composite 🎯 text). | data/code | S | Deck tooltips describe the live ordering; ADP source dated and cited in the build manifest. |

**P3 — in-season:** weekly-record ingest continues (R7 pipeline); λ tuned
against the owner's realized start/sit choices; bracket-variance monitoring
through the playoff weeks.

## 7. Protect list

- **The kit's gate + engine.** Verified working this run: structural
  provenance PASS, freshness gate correctly FAILING (the gate caught real
  staleness — that is the design), two-run byte-identical regeneration,
  negatives-never-shrunk invariant intact on the committed board. Change
  nothing here except via the method-change protocol.
- **Push-is-done and the pull protocol.** The one plane that follows them
  (kit `main`) is the one that stayed current. The failure is uneven
  adoption, not the law.
- **The board's caveats-block discipline.** The market cross-check
  DEFENDED every head-of-board divergence because the board had
  pre-announced each with a named mechanism — divergence-with-paper-trail
  is exactly what a trustworthy contrarian board looks like.
- **The self-critique culture.** N1–N7 was substantially accurate
  (7/7 confirmed at core, 3 reframed) and one confession was voluntary.
  Keep the culture; bind its bars to artifacts (R4).
- **blend50's kill switch and REVERT-MAP.** Correctly scoped, keep as-is
  pending E9b.
- **The Lillard 45-GP hand discount.** The sweep upgraded it from
  single-outlet to beat-consensus — the analyst's caution was right.
  Protect the practice of hand-discounting on sourced injury mechanisms.

## 8. Validation & backtest plan

Every method fix above carries its own falsifiable criterion (R6, R7, R11,
R12, R13). Cross-cutting: (1) 2025-26 season actuals exist in full — the
R6 returnee-cohort backtest and an R7 weekly-distribution backtest are
runnable now, not in November; (2) the two-run determinism doctrine and
the λ=0 / synthetic-parity checks guarantee each method change is
observable as a pure board diff; (3) the R9 gate turns cross-plane
coherence from a one-time audit into a per-pull invariant; (4) after R1,
one WebFetch of raw `main` LESSONS.md is the standing check that the co-GM
surface is un-staled.

## 9. Sources

Dated sources fetched this run (WebSearch; direct fetches 403-blocked):
Draymond Green re-signing GSW (nba.com/news, hoopsrumors.com 2026-07,
vavel.com 2026-07-29); Sochan→POR (hoopsrumors.com 2026-08,
740thefan.com 2026-08-01); Kawhi investigation timeline (espn.com id
49482792 ~07-29/30, nba.com, cbssports.com); Harden unsigned
(bleacherreport.com, basketnews.com late July); DeRozan/Beal-MIA
(hoopsrumors.com 2026-07); Kuminga UFA status (espn.com id 49219048,
si.com/nba/hawks); Westbrook unsigned (hoopsrumors.com 2026-08); Butler
rehab (espn.com id 49198925, bleacherreport.com, heavy.com late July);
Lillard on-track multi-outlet (ibtimes.com.au, si.com ~07-15); DiVincenzo
timeline (heavy.com, bleacherreport.com); VanVleet (lastwordonsports.com
06-21, espn.com); RFA statuses Mathurin/Duren/Watson (hoopsrumors.com
07-26..08); Jalen Wilson two-way (hoopsrumors.com 07-20, hawks.com);
top-10 verification incl. Wemby extension and AD-WAS (bleacherreport.com,
sports.yahoo.com, espn.com id 49490878); market list: Yahoo/Dan Titus
2026-07-27 early top-50 9-cat (sports.yahoo.com fantasy article
143154601, nba.com mirror); ESPN way-too-early top-10 (espn.com fantasy
id 48484688, 2026-04-14). Full URLs in the sweep agents' outputs (session
records); confidence per item as tagged in §5 F7/F8.

## 10. Run log (appendix)

Kit plane, executed by the reviewing session before fan-out:

- `check_provenance.py` → PASS (verified 2026-07-13..27).
  `check_provenance.py --max-age-days 14` → **FAIL, 207/220 rows stale**.
- Regen probe per SYSTEM-REVIEW §3: two runs byte-identical; tracked diff =
  only the `*Generated <date>` header line; `git restore` left tree clean.
- Kit git state: working branch pushed through `eafa4cb`; tree clean.
- Deck plane: anonymous shallow clone; `main` tip `4c4b65c` (2026-07-13);
  PR branches fetched (`pr1`/`pr2`/`pr3`); pr3 worktree at `4a7a1b8`
  (2026-08-04); `git grep` proved N-list referents absent from `main`;
  `main..pr3` = 30 visible commits, 122 files, +19,460/−282 (shallow
  floor).
- Published deck artifact fetched: built 2026-08-04, pool 246, blend50 +
  E18 live — coherent with pr3, incoherent with `main`.
- Fan-out: 4 triage agents (N1+N4, N2+N6, N3+N5, N7+cross-plane), 2 sweep
  agents (current facts; market cross-check). All six returned; their
  reproductions included a byte-for-byte re-derivation of the E18 measured
  column and a live re-computation of the deck board for the 0.78
  sensitivity analysis. Failures honestly noted: all direct page fetches
  (WebFetch/curl) 403'd under the egress policy; market tail ranks
  therefore CANNOT VERIFY beyond the two riser findings.

### Adversarial pass (Phase 4, recorded)

1. *"Merge PR #3 is P0" — could main be frozen deliberately as a stable
   co-GM surface?* Refuted: the 07-27 validation report (owner-endorsed)
   already ordered the merge; the published artifact already exposes the
   new system to the owner; freezing main protects no one while reality
   moved. Survives, with the LESSONS-fork reconciliation folded in (R1).
2. *N3 reframe — did the self-report mean the deck-vs-market spread?* Even
   charitably, "one scalar is the entire difference" fails quantitatively
   (0.20–0.25 required); the cross-plane spread is real either way.
   Survives as reframed.
3. *F3 HIGH — maybe committing every mock state is impractical and prose
   records suffice?* Refuted by the repo's own founding rule (tallies
   quotable only if repo-derived) and by the cheap manifest alternative;
   three agents independently hit dead paths. Survives.
4. *Butler 55 GP — a confirmed defect?* No hard return date exists; kept
   as a watchlist promotion inside R2, not a NOW-WRONG row. Downgraded.
5. *Keyonte George — confirmed mispricing?* Market rank is
   snippet-extracted (MEDIUM confidence); could be a defensible fade.
   Kept as a review-candidate inside R2, not a confirmed error.
   Downgraded.
6. *N5 at MEDIUM — is that too low given unlimited moves?* The league's
   own three seasons (16-move champion; champions' record ranks 2/7/7;
   owner's loss = bracket variance) support bracket-first sequencing;
   an explicit escalation trigger is wired into R13. Survives.
7. *N1 at HIGH without a demonstrated mis-ranking?* The 99.4% FT%
   precedent shows this exact error class produced absurd category prices
   before, and the kill rule is structurally blind to it. Survives.
8. *F1 HIGH — does the co-GM's Daily Freshness web-search protocol
   mitigate the stale feed?* Partially for player news, not at all for
   the arena/deck/lessons content the pull-first rule exists to serve;
   "fetched file wins" makes the stale copy authoritative on exactly that
   content. Survives.
9. *R6 as one cross-plane change — too big to land?* The alternative
   (two divergent availability reforms) is how F4 happened; the method-
   change protocol has already landed a two-plane-consistent change once
   (2026-07-27). Survives with L effort acknowledged.
10. *Scorecard F "Failing" — unfair to a system whose publish plane is
    coherent?* The grade keys to the seam the owner actually consumes
    (co-GM + strategy surfaces), where a 62-rank disagreement and a
    22.8-day stale feed are live. Survives as phrased (publish↔pr3
    coherence is credited in the cell).

### Quality gates (SYSTEM-REVIEW §6) — all checked

100% of N1–N7 triaged with verdict/severity/root cause ✓; every §4
dimension graded with findings or checked-sound ✓; engine and gates
executed, probe restored, tree clean ✓; facts sweep run (20 items, each
sourced or CANNOT VERIFY) and market cross-check run (PARTIAL, honestly
bounded) ✓; every fix has mechanism/class/effort/priority/falsifiable
validation ✓; adversarial pass recorded, two downgrades ✓; no NBA-world
fact from memory ✓; protect list evidenced ✓; report committed and pushed
per session branch rules ✓.
