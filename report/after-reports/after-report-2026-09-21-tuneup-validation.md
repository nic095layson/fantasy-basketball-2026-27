# After-report — Pre-implementation validation & integrity test (2026-09-21)

**Owner request (2026-09-21, verbatim):** "Conduct a thorough validation and
integrity test before implementing these permanent fixes to system."

**Scope.** Three things, all before any change: (1) a green baseline of every
existing gate on both planes, so post-fix regressions are attributable; (2)
mechanical verification of every tune-up premise against primary artifacts —
the cross-plane diff (S3's prototype run), line-drift measurement, and the
resolver source read; (3) per-fix GO/NO-GO with the exact implementation
lists. **Nothing was changed** — working trees verified clean after every
check (two regenerated-artifact touches restored: the board's embedded
generation date, the verifier's checked_at stamp).

Pull window: 2026-09-15 → 2026-09-15 (validation run 2026-09-21; no roster
state change).

**Headline.** Every gate on both planes is green; every fix premise survives
contact with the primary artifacts except two of my own framings, which this
test corrects: **D-I1 is not a data conflict** (across 224 shared names there
are ZERO team mismatches and ZERO exclusion-class severity mismatches —
Butler's deck tag and kit GP 20 agree in class; the only question is the
ratified streaming-credit curve, genuinely optional), and **S1's scope
narrows** (the resolver source shows bare-surname ambiguity is irreducible
without a pool row; the implementable fix is verbatim logging on the fix-path
and full-name no-match inputs, which recovers every draft_51 failure). The
deck build's freshness gate REFUSES on 6-day-old evidence — by design — so
the deck implementation must ride an evidence-re-authoring pool-maintenance
pass (precedent: 2026-08-25). Verdict: **GO on S1 (narrowed), S2 (lists
below), S5, S6; S3 validated by its own prototype; S4 and the avail-curve
remain owner options.**

---

## 1. Baseline gate battery — all green (2026-09-21)

| plane | gate | result |
|---|---|---|
| kit | provenance gate | PASS (240/240 sourced, orphan-clean) |
| kit | rank_engine build | PASS (200 from 240; regenerated board byte-identical except embedded date) |
| kit | yahoo_market transcription + join | PASS (220/20/80, 0 unexplained) |
| kit | market_stats reproduction | PASS (ρ 0.7839 / 0.7124 reproduce) |
| kit | report publication gate | PASS |
| deck | verify_rosters (fallback-partial) | PASS (255/255 vs 9/15 official, 0 mismatches) — PARTIAL by egress design |
| deck | build_deck | **REFUSED — freshness gate working as designed** (evidence dated 9/15; re-author required before rebuild) |
| deck | check_parity | EXACT MATCH (72 vectors, 91 turns, 7 states) |
| deck | test_draft / test_gates | 53/53 · 15/15 |
| deck | judgment enumerator | 7 flagged from the 9/15 JUDGMENT, parses clean |

## 2. Premise verification (the integrity test proper)

**Cross-plane diff — first mechanical run (S3 prototype).** kit 240 vs deck
255, 224 shared after normalization/aliases. **Team mismatches: 0. Exclusion-
class severity mismatches: 0** (deck tag class vs kit GP class agree
everywhere, Butler and Sharpe included). The premise "planes drift" is TRUE
for membership and lines, FALSE for placements and severity — a stronger
system than the tune-up report implied, and S3 remains worth adopting
precisely because this run took one script to prove it.

- **KIT-ONLY (16)** — deck lacks: Wagler, Ayton, Bona, Robinson, Champagnie,
  Graves (the 9/16 adds), plus AJ Green, Robert Williams III, Drummond,
  Sensabaugh, Whitmore, Swain, Okorie, Kris Murray, Philon, McNeeley,
  Morez Johnson [16 incl. both lists' overlap].
- **DECK-ONLY (31)** — incl. the stale **Keaton Wallace row (delete)**, plus
  Naji Marshall and Tim Hardaway Jr. (so those two need KIT rows only), and
  veteran depth the kit's value floor dropped (Beal, Hield, LeVert, DLo,
  Moody, Adams, …) — no action; different pool philosophies, now documented.
- **Line drift, the 9/16 re-derivations** (deck vs kit per-game): Sheppard
  15.5/5.4 vs 12.5/3.9 ast; George 17.5 vs 20.5 pts; Randle 19.0 vs 22.5
  pts; Vučević 13.5 vs 13.0 (deck was already bench-shaped — partial credit);
  Butler moot (excluded on deck). Reconciliation list confirmed at four
  names.

**Resolver source read (S1 premise).** `hoops.py match_player`: pipeline is
nickname > exact word > substring > fuzzy (surname-only, first-letter guard,
F22-audited), with draft-context auto-resolution for ambiguous surnames and a
hard exit on already-drafted. The draft_51 #134 failure is confirmed as
out-of-candidate-set, NOT a pipeline bug: no resolver can infer "Tre Jones"
from "Jones" when Tre has no row. Narrowed S1 spec: (a) the fix/insert path
accepts a full name (2+ tokens) with no pool match and logs it VERBATIM with
a not-in-pool marker — this recovers #134 ("38- Tre Jones" was refused),
#152, and #154; (b) bare-surname UNKNOWNs keep today's behavior (typo inputs
like "Markenan" must stay UNKNOWN, not verbatim-logged). Cross-language:
`hoops.py` + `docs/draft-deck.html` (one "assumed over" site each;
`arena.py` clean), tests driven red first.

**Freshness constraint (real, by design).** `build_deck` refuses on evidence
older than today; re-authoring evidence requires a sweep. Precedent: the
2026-08-25 pool-completion pass. The deck implementation therefore rides a
pool-maintenance pass with a same-day verification sweep — which is also
where the 12 deck adds get current sourcing.

## 3. GO/NO-GO

| fix | verdict | note |
|---|---|---|
| S1 resolver | **GO, narrowed** | verbatim fix-path spec above; red-first tests both languages |
| S2 pool adds | **GO** | deck: the 6 kit-integration names + Tre Jones + RWIII + AJ Green + Beringer + Joe + Huff, and delete Wallace; kit: Tre Jones + Beringer + Joe + Marshall + Huff |
| S3 gate | **VALIDATED by prototype** | adopt as F7: this run's script becomes the per-pull check |
| S4 punt hysteresis | owner option | no premise defect found; behavioral tuning |
| S5 annotation | GO | wording only |
| S6 state tolerance | GO | rides S1's verbatim marker |
| S7 / D-I1 | **REFRAMED** | data already harmonized; only the avail-curve philosophy question remains — owner's, not urgent |

## Watchlist

Unchanged from the gap-research-2 report; adds pending implementation.

## Open-item receipts

| check | receipt |
|---|---|
| Kit battery | 5 gates run 2026-09-21, outputs above, tree clean after restore |
| Deck battery | 6 gates run 2026-09-21; build refusal text quoted; parity EXACT |
| Cross-plane diff | script run 2026-09-21: 224 shared, 0 team, 0 severity-class mismatches; 16/31 one-plane lists |
| Line drift | 5 names diffed deck-vs-kit per-game, table above |
| Resolver read | hoops.py match pipeline + F22 audit note located; draft-deck.html 1 site, arena.py 0 |
| Publication gate | check_report.py PASS on this file |

## Bounds

**Out of scope by design:** the implementation itself (follows this report on
its GO verdicts, on branches, with artifact republish and all merges held for
the owner); S4 and the avail-curve (owner options).
**In scope and unverified:** deck verification remains PARTIAL by egress
policy (vs the 9/15 official file, not an independent live source — its own
output says so); the deck-side add lines will be derived from kit rows at
implementation and get their sourcing re-checked in the maintenance pass.

## Decision sheet

Implementation proceeds on the GO verdicts (branches + draft PRs only).
Still yours: S4 adopt/skip; avail-curve keep/harshen; republish timing; and
the merges.

## Provenance

Produced 2026-09-21 by the operating session
(`https://claude.ai/code/session_01QjgeRdpDaWgSJmGKRG8fTU`), branch
`claude/draft-51-mock-analysis` (PR #23). Every figure from commands run this
session against both repos at main; companions:
`after-report-2026-09-21-draft51.md`, `after-report-2026-09-21-gap-research-2.md`.
