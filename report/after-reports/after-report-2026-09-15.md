# After-Report — Data Pull 2026-09-15

**Pull window: 2026-09-11 → 2026-09-15 (4 days).**
Gate: `check_provenance.py` exit 0 (verified 2026-07-13 .. 2026-09-15).

> **Headline: the Kawhi trade EXECUTED.** Official Monday **9/14**, announced
> by the Raptors (CBC with GM Bobby Webster's statement; SI, HoopsRumors,
> BVM 9/14, The Sporting Tribune 9/14, Yardbarker/heavy). Owner reported it
> settled; verified across six independent outlets before any edit. **Three
> rows moved** — the largest placement change since the pull system began.
> Second headline: **the real draft is set — Tuesday, October 14, 7 PM**
> (owner-local), recorded in league intel.

## 1. NBA roster changes

**Three placements moved**, all from the executed 9/14 trade; `verify_rosters`
**255/255, 0 mismatches**, dated 2026-09-15; CSV + evidence ledger + kit
provenance edited as pairs (source: the Raptors' announcement via CBC,
source_date 9/14, verified_on 9/15).

| row | move | line handling |
|---|---|---|
| **Kawhi Leonard** | LAC → **TOR** | HELD — acquired as the primary option, same shape as his LA usage (CBC announcement; HoopsRumors). Judgment −0.08 → **−0.05** (execution risk dissolved; integration residual only; availability stays in the `inj-risk` 0.78 tag) |
| **Brandon Ingram** | TOR → **LAC** | HELD — LA cast him as the one-for-one wing replacement (SI.com; Yardbarker). His row gains the **queued heel-monitor note** (right heel spur removed 5/8, expected ready for camp — informational, no multiplier, Brunson convention). New card at −0.05 |
| **Gradey Dick** | TOR → **LAC** | HELD — bench wing both places (CBC; Sporting Tribune full-package coverage); no card |

Seventy-six days elapsed between agreement (June 30) and execution (Sept 14).
This board held all three rows through three pulls of "done any day now"
reporting and one false "officially completed" aggregator post — **the
hold-until-executed discipline was right all three times**, and the rows
moved within one pull of the real event.

Also checked, nothing applied: the **Memphis cut-down remains
reported-not-executed** (still "could waive" coverage on Hawkins / Peavy /
D'Angelo Russell / Clayton / Kris Murray — all rows hold) · no in-window
injury-tag changes (Mark Williams stays excluded post-labrum) · Exhibit-10
churn touches no row.

## 2. Significant fantasy analysis changes

**Board diff: zero rank moves** — the trade moved labels, not values (no stat
edits; lines held pending camp roles). Kit top-200: Kawhi's and Ingram's team
columns flip; Dick is sub-200. Deck: same three notes now read
`traded … 2026-09-14 (executed)`.

- **Kawhi −0.08 → −0.05** (resolved; integration residual).
- **Ingram card added at −0.05** (integration + heel informational; clears to
  zero if camp opens full-go).
- **Duren held −0.08, card refreshed**: the QO branch keeps firming —
  Forbes (**9/12**) argues Detroit should call the bluff; Last Word (**9/14**)
  games the rotation with Duren on the $9.6M QO; ask now **$200M+** vs ~$190M
  offered. **Oct 1 is 16 days out.** A Piston on every branch.

## Open-item receipts (F1 — 7 flagged after Kawhi's card closed)

| player | query run | dated finding |
|---|---|---|
| Kawhi Leonard *(closed this pull)* | "Kawhi Leonard trade completed official Raptors announce" | **EXECUTED 9/14** (CBC/SI/HoopsRumors/BVM/Sporting Tribune) — rows moved, card resolved, drops off the open list |
| Jalen Duren | "Jalen Duren Pistons qualifying offer extension news September 14 2026" | No deal; Forbes 9/12 + Last Word 9/14; $200M+ ask; QO branch firming — HELD −0.08 |
| Bennedict Mathurin | NOP/S-B-M combined check | No new role reporting since the 9/11 bench reprice; camp minutes are the checkpoint — HELD −0.05 |
| Jeremy Sochan | S-B-M combined check + POR shadow | No cut executed; still listed as a Blazers addition; cut-watch stands — HELD −0.20 |
| Jalen Brunson | S-B-M combined check + NYK shadow | Nothing new in window; recovery on-timeline — HELD |
| Cam Thomas | FA-trio query | Still unsigned (hoopswire list; personality-cited coverage) — HELD |
| Jaden Ivey | FA-trio query | Still unsigned (hoopswire list) — HELD |
| Lonzo Ball | FA-trio query | Still unsigned (hoopswire; 8/31 workout video the only signal) — HELD |

**Team-shadow sweep (F3):** MEM query yielded the cut-down status (pending);
LAC/TOR covered by the execution cluster; DET by the Duren queries; CHI/NOP/
NYK/POR quiet. **F5:** the only in-window transaction of consequence IS the
executed trade; ledger check clean otherwise. **F6:** `--tags` diff run — no
returner-class stories in window.

## 4. Watchlist / open items

- **Camp roles for the three moved rows** — Kawhi's TOR usage, Ingram's LAC
  usage, Dick's rotation spot. First reprice checkpoint: camp/preseason
  reporting (~2 weeks).
- **MEM cut-down** — still the likeliest next row-mover (two deck rows + one
  kit row exposed).
- **Duren — Oct 1, 16 days.** QO branch now the reported-likely outcome.
- **DRAFT DATE SET: Tuesday 2026-10-14, 7 PM owner-local** (timezone
  unconfirmed — worth stating once). Recorded in `league_intel_2025-26.md`
  §9 item 8. The Oct-12 Routine fires two days before, inside its designed
  threshold; per SEPTEMBER-PLAN §8.5 the October session creates the T-1
  draft-eve Routine (targeting **Oct 13**) before it closes. **D-S4 is now
  sharper**: that Routine's only test fire aborted, and its real fire is
  draft-minus-two — the de-risk decision (leave armed + manual backup, or
  one more test fire) deserves an answer before October.
- **Slot still TBD** — send it the moment Yahoo assigns it (league intel
  notes this).
- Carried: Maluach/Ighodaro minutes watch (Williams out) · Kuminga usage ·
  Simmons (SAC, non-guaranteed) camp fate · D-S1/D-S2 (September-plan
  inputs) still the standing blockers · D-S8 Sabonis tag.

## 5. Verification (adversarial pass)

- **C1 — owner report verified, not assumed.** "Settled" was confirmed
  against six independent outlets including the acquiring team's own
  announcement before any row moved — the same bar that held these rows
  through three false dawns.
- **C2 — paired edits everywhere**: pool CSV + evidence ledger teams arrays
  (deck) and projections CSV + provenance rows (kit) moved together;
  `verify_rosters` and `check_provenance` both re-ran green after.
- **C3 — the enumerator's resolved-card behavior worked as designed**: the
  rewritten Kawhi card initially re-flagged on the word "investigation"
  (used historically); reworded so a *closed* situation doesn't demand
  receipts forever. 8 flagged → 7.
- **Bounds:** all direct fetches remain egress-blocked; sourcing is dated
  search results across independent outlets. Draft-time timezone is
  unconfirmed. Lines on all three moved rows are deliberately unrepriced
  until camp reporting exists — direction of any future reprice unknown.

## 6. Gates

`verify_rosters` 255/255 dated 2026-09-15 · `check_provenance` exit 0
(range now .. 2026-09-15) · `freshness --stamp` with `--pool-changes`
(3 team rows) · `build_deck.py` all six gates green (pool `e3e17e279ea5`,
round-trip byte-identical) · `check_parity` **EXACT MATCH** · `test_gates`
**15/15** · `test_draft` **53/53** · board diff **0 rank moves / 2 visible
team-label flips** · `check_report` PASS · receipts check PASS · artifact
republished at `built: 2026-09-15`.
