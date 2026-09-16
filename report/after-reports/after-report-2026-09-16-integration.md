# After-report — Integration pass: role research + gap research into the board (2026-09-16)

**Owner request (2026-09-16, verbatim):** "Proceed with your recommendations" —
executing the recommended bundle from the two research reports: D-P1 (five line
re-derivations), D-R1 (Keaton Wallace row deletion), D-R2 (six ADD-tier pool
rows), D-R3 (engine reruns), as one pass. The AT-RISK names (Dyson Daniels, Naz
Reid) and the optional-tier adds (Wiggins, Kennard, Mara) were NOT touched, per
the recommendation's own scoping; a preseason recalibration pass follows when
the owner's data arrives.

Pull window: 2026-09-15 → 2026-09-15 (integration executed 2026-09-16 on the
research of the same date; not a news pull — the next pull's window still opens
at 2026-09-15 per the pull-log, and will re-sweep this period's news normally).

**Method.** Every line change derives from the sourced role findings in
`after-report-2026-09-16-role-research.md` and
`after-report-2026-09-16-gap-research.md` (receipts there); the board stays
first-principles — roles and availability came from sources, the 9-cat lines
are house-derived as always. Paired edits enforced: every touched player has a
refreshed or new `roster-provenance.csv` row (verified 2026-09-16), and the
Wallace deletion removed both rows. Edits were applied by an exact-match
script (old lines asserted verbatim before replacement).

**Headline.** The pool is now 240 rows. Butler's phantom value is gone (his 55
GP was the board's largest live error), the two stale-low breakout lines
(Keyonte George, Randle) now price their reported roles, the room's six most
draftable missing names can be priced, and Keaton Wallace is off the board.
All gates green: provenance PASS, build PASS (240 projected, top-200 written),
transcription/join gates PASS (220 matched, 0 unexplained, team mismatches
still ZERO), publication gate PASS on this report. Market alignment moved the
expected direction: ρ(our, XRank) 0.762 to 0.784, ρ(our, ADP) 0.701 to 0.712.

---

## 1. What changed

| player | change | board rank (old to new) | receipt |
|---|---|---|---|
| Jimmy Butler | GP 55 to 20, volume trimmed | 55 to 68 | ACL rehab, out for season start (role report §3) |
| Nikola Vučević | mpg 29 to 23, volume scaled | 49 to 134 | backup role behind Carter (role report §3) |
| Reed Sheppard | mpg 28 to 24, volume scaled | 50 to 107 | bench with VanVleet healthy (role report §3) |
| Keyonte George | line rebuilt: 20.5 pts, .445 FG%, 32 mpg | 181 to 116 | breakout + dilution (role report §2) |
| Julius Randle | usage bump: 22.5 pts, 5.5 ast, 34 mpg | 136 to 114 | BKN focal role (role report §4) |
| Keaton Wallace | row deleted (both files) | 230 to — | Maccabi two-year deal (gap report §3) |
| Keaton Wagler | ADDED: 16.5 pts rookie-starter line | new at 181 | No. 5 pick, projected starter (gap report §4) |
| Deandre Ayton | ADDED: 13.5/9.5 timeshare-C line | new at 141 | WAS center, role unsettled (gap report §4) |
| Adem Bona | ADDED: backup-C stocks line (1.3 blk) | new at 230 | top backup behind Embiid (gap report §4) |
| Duncan Robinson | ADDED: 3.0 3PM specialist line | new at 184 | probable DET starter (gap report §4) |
| Julian Champagnie | ADDED: 10.5 pts rotation-wing line | new at 173 | 3yr commitment, firm rotation (gap report §4) |
| Allen Graves | ADDED: rookie 3-and-D line | new at 224 | No. 19 pick, second unit (gap report §2) |

Ripple on untouched rows: at most 6 rank positions, all in the deep tail
(pool-relative z re-baselining plus six new rows) — no untouched top-150 player
moved more than 3 spots. Dyson Daniels holds #9 untouched.

## 2. The Butler surprise, diagnosed honestly

Prediction said Butler would fall out of the top ~100; he landed **#68**. The
cause is the kit's availability model working as designed, not a data error:
`avail(gp) = gp/82 + (1 − gp/82) × 0.20` — the streaming-credit floor the owner
ratified in the 2026-07-27 method change. At GP 20 he keeps a 0.395 weight, and
his per-game line is elite, so the board says "20 games of Butler are worth a
7th-round pick of streaming value." The DECK plane makes the opposite call by
design (an `out-*`/recovery tag zeroes him from draft boards), and the deck is
out of this session's reach — so the planes now deliberately disagree on Butler
until the next deck session tags him. If the owner wants long-absence returners
discounted harder on the KIT board too, that is a method change to the avail
curve (decision D-I1 below), not a data edit — flagged, not made.

## 3. Market layer after regeneration

- Matched 220 of 240 pool players; 20 verified absences; **zero team-code
  mismatches** (the six adds joined on their Yahoo-confirmed teams).
- Coverage gaps with ADP inside 140: **13 to 7** (all remaining are the
  deliberately skipped/optional tier: Horford, Kornet, Kennard, McConnell,
  Wiggins, Mara, Broome).
- ρ(our, XRank) 0.784 over 220; ρ(our, ADP) 0.712 over 182; band medians
  unchanged (20 picks, 46 of 131 at 25+).
- Consensus board: Butler consensus #101, Vučević #150, George #65, Randle #80,
  Wagler #165, Ayton #149 (full file regenerated in place; the pre-integration
  version remains in git history at `1940ae6`).

## 4. Gates run (all green, 2026-09-16)

Provenance gate PASS (240/240 sourced, verified through 2026-09-16, orphan
check clean after the Wallace pair-delete); rank_engine build PASS (240
projected, top-200 written); transcription gate PASS (unchanged raw);
join hard gate PASS (0 unexplained; Wallace's accepted-absence entry retired
with a dated comment); `market_stats.py` rerun reproduces the §3 figures;
this report passes `report/check_report.py`. The projections diff was verified
line-exact: 5 modified + 1 deleted + 6 added, nothing else; the provenance diff
shows exactly the 12 paired rows (a line-ending artifact from the first write
was caught and normalized so the diff stays honest).

## Watchlist (unchanged plus integration follow-ons)

Preseason recalibration pass when the owner's data lands (Daniels minutes,
Reid, Sheppard/VanVleet split, Butler rehab milestones, Vučević-vs-Carter,
George usage, Randle usage, Wagler camp role, WAS center rotation, Embiid camp
participation, Kawhi arrival Sept 30). Deck-plane sync items for the next deck
session: Butler ACL tag (out-recovery class), the five kit line changes'
context, Wallace's departure, and the six new kit names' deck counterparts.

## Open-item receipts

Receipts for this pass's checks (research receipts live in the two companion
reports):

| check | receipt |
|---|---|
| Exact-match edit script | 5 replacements + 1 delete asserted verbatim before write; 236 to 241 lines |
| Provenance pairing | gate PASS; 12-row diff verified; orphan check clean |
| Board regeneration | 240 projected, top-200 written; movement table §1 from old-vs-new CSV diff |
| Join regeneration | 220/20/80 exactly as predicted pre-run; mismatches 0 |
| Stats reproduction | market_stats.py rerun 2026-09-16 matches §3 figures |
| Publication gate | check_report.py PASS on this file |

## Bounds

**Out of scope by design:** deck plane (session GitHub scope is kit-only —
cross-plane divergence on Butler is deliberate and flagged); Daniels/Reid
edits (await preseason); optional-tier adds; avail-curve change (D-I1, owner's);
pull-log (not a pull — next pull re-sweeps from 2026-09-15 normally).

**In scope and unverified:** the six new lines and five re-derived lines are
house projections from sourced roles — their *numbers* are editorial derivations
(as all pool lines are), and the preseason pass is their first calibration
checkpoint; Wagler's line assumes the projected starter role holds through camp
(demotion trigger in the gap report).

## Decision sheet (owner disposes)

- **D-I1 — availability curve for long-absence returners:** keep the
  streaming-credit floor as-is (Butler #68 stands on the kit board), or adopt a
  harsher discount for players out past a date threshold. Method change; needs
  the board-header text update per the standing work-order rule.
- **D-I2 — optional-tier adds** (Wiggins, Kennard, Mara) remain one word away.
- **Preseason recalibration pass** on your data drop — standing plan.

## Provenance

Produced 2026-09-16 by the operating session
(`https://claude.ai/code/session_01QjgeRdpDaWgSJmGKRG8fTU`) on branch
`claude/market-data-workorder-mnfi2b` (PR #22). Inputs: the two 2026-09-16
research reports and their receipts. Rerun everything:
`python3 report/check_provenance.py && python3 report/rank_engine.py &&
python3 report/market/yahoo_market.py 2026-09-15 &&
python3 report/market/market_stats.py 2026-09-15 &&
python3 report/check_report.py`.
