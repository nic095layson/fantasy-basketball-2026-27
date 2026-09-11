# After-Report — Data Pull 2026-09-11

**Pull window: 2026-09-08 → 2026-09-11 (3 days).** The **first pull run under
the F1–F6 protocol** — receipts contract, team-shadow sweep, publication
gate, returner-vs-tag diff, colophon gate all exercised below.
Gate: `check_provenance.py` exit 0 (verified 2026-07-13 .. 2026-09-02).

> **Headline: Mark Williams' eleven-pull quiet streak broke, the wrong way.**
> Torn left shoulder labrum in an offseason workout, surgery **9/10**, out an
> extended period with **no timetable** — he is now excluded from all boards
> under the recovery ruling. Second headline: **the Kawhi trade is unexecuted
> a THIRD straight pull**, and the delay finally has a sourced cause.
> Per owner instruction this report is delivered **before** the artifact
> republish; the deck is built and gate-green locally, publish held for your go.

## 1. NBA roster changes

**Zero placements moved.** Two rows changed without team edits (both under
§3 sourced-mechanism rules): `verify_rosters` **255/255, 0 mismatches**,
dated 2026-09-11.

| change | mechanism + sources | disposition |
|---|---|---|
| **Mark Williams (PHX)** — `inj-risk` → `shoulder-recovery` (availability 0.78 → **0.0**, excluded); kit GP **58 → 15** | Torn left labrum in an offseason workout, **surgery 2026-09-10**, "extended period," no timetable — wire/AOL, ESPN's injury ledger, Valley of the Suns, Bright Side of the Sun (independent) | Excluded per the owner ruling on serious recoveries (Sharpe precedent). GP 15 is probability-weighted: labrum repairs run ~6+ months → earliest ~March; range 0–30, magnitude `[SPECULATIVE]` |
| **Bennedict Mathurin (NOP)** — volume rescaled to a bench shape (deck 16.5 → 13.9 pts; kit mpg 31 → 26); judgment −0.10 → −0.05 | His registered **reprice checkpoint arrived**: NOP rotation coverage (SI Pelicans, Yahoo, FanSided, 9/9–9/11) casts him as the bench scoring punch behind Murphy/Zion/Jones/Bey | Role and line now agree; residual −0.05 prices the six-ball-handler logjam. `[LIKELY]` direction, `[SPECULATIVE]` magnitude |

In-window transactions touching no row: **Taj Gibson waived by NOP 9/9**
(Spotrac ledger + BVM — and it **confirms the 9/8 NOP–MEM trade formally
processed**, corroborating the Hawkins row move) · **DeRozan's DEN deal
formally signed 9/8** (Spotrac; agreed 8/21, row already DEN — the
agreed-then-official pattern again) · Exhibit 10s: Keyshawn Bryant, Devon
Higgs, Bez Mbeng, Dillon Jones `[SINGLE-SOURCE]`.

**Garble log:** the ledger row "Ben Simmons signed 1yr/$3.52M with the LA
Clippers (9/8)" resurfaced — the **sixth** documented garble, second for this
item. Refuted again: he is a **King** on a non-guaranteed deal (NBA.com,
HoopsRumors, B/R workout detail, SI Kings). The F2 publication gate exists
for exactly this row shape; no surface carried it.

## 2. Significant fantasy analysis changes

- **Mark Williams excluded** — the board's only C-eligible PHX starter row
  goes to 0.0. **Khaman Maluach and Oso Ighodaro are the named beneficiaries**
  (Valley of the Suns: "obvious solution"; Bright Side depth pieces) —
  **watched, not repriced**: no minutes reporting exists yet. Kit board:
  Williams was already sub-top-200, so the visible move is **Mathurin
  141 → 188** (+47); 49 one-to-two-slot ripples, no entries/exits.
- **Kawhi Leonard held −0.08 through a third hold** — the 9/8 card's
  "third hold = signal" clause fired, and the signal is now identified:
  the **Clippers' front-office leadership vacuum** (Ballmer suspended a year,
  Lawrence Frank six months; nobody empowered to execute) — Raptors Republic
  9/8, Yahoo, Yardbarker ×2, BlogTO. All parties "remain very confident" it
  closes before camp. Administrative cause with a camp deadline ≠ new
  player-value risk; the row stays LAC, right for the third time.
- **Jalen Duren held −0.08, rationale rebased**: BVM **9/10** — increasingly
  prepared to **play on the $9.6M qualifying offer**; DET's offer now framed
  near $190M/5yr vs his $40M+/yr ask (HoopsRumors, SI). The likely branch
  flipped extension → QO year: availability-neutral, arguably usage-positive.
  Oct 1 is 20 days out.
- **Jeremy Sochan widened −0.15 → −0.20**: SI Trail Blazers names him the
  **likeliest opening-night cut** on his non-guaranteed Exhibit 9 deal.

## Open-item receipts (F1 — all 8 flagged, each searched this pull)

| player | query run | dated finding |
|---|---|---|
| Kawhi Leonard | "Kawhi Leonard Raptors trade officially completed finalized" + delay-cause query | Unexecuted, third pull; Friday-dated status "still officially a Clipper, timing undetermined"; cause sourced (front-office vacuum, Raptors Republic 9/8 + 4 outlets) — HELD −0.08 |
| Jalen Duren | "Jalen Duren Pistons extension agreement signed September 10 2026" | No deal; **BVM 9/10**: leaning to the $9.6M QO; offer ~$190M/5yr vs $40M+/yr ask — HELD −0.08, card rebased |
| Bennedict Mathurin | "Bennedict Mathurin Pelicans role rotation news September 2026" | Bench-role coverage (SI/Yahoo/FanSided 9/9–9/11) → line repriced, adj −0.10 → −0.05 |
| Jeremy Sochan | "Trail Blazers roster news Sochan September 2026" | SI: likeliest opening-night cut; Exhibit 9 non-guaranteed (KGW, Blazer's Edge) — WIDENED to −0.20 |
| Jalen Brunson | "Knicks Jalen Brunson wrist camp ready September 2026" | On-timeline (6–8wk from 7/7); expected fully cleared for camp (Yahoo, NY Post via Yahoo, Yardbarker) — HELD, informational tag |
| Cam Thomas | remaining-FA sweep 9/10 query | Still unsigned (Yardbarker, hoopswire list, B/R) — HELD |
| Jaden Ivey | remaining-FA sweep 9/10 query | Still unsigned; CHI-waiver history stands (Wikipedia/hoopswire) — HELD |
| Lonzo Ball | remaining-FA sweep 9/10 query | Still unsigned (hoopswire list) — HELD |

**Team-shadow sweep (F3)** — one team-shaped query each over
CHI/DET/LAC/MEM/NOP/NYK/POR. Yield: the **MEM roster crunch** (below), the
Kawhi delay cause (LAC), the Mathurin role reporting (NOP), CHI quiet
(Powell/Wilson/Claxton all already correct rows). **F5:** no in-window trade
existed to find; the ledger-shaped Spotrac query is the receipt (only the
Gibson waiver and Exhibit 10s). **F6:** `--tags` diff run; the only
returner-class story in window was Williams — inbound, not returning.

## 4. Watchlist / open items

- **MEM roster crunch — two rows exposed.** Fischer: four of **Jordan
  Hawkins**, Micah Peavy, **D'Angelo Russell**, Walter Clayton Jr., **Kris
  Murray** (kit row) must be waived to reach 15; "Hawkins has a chance to
  stick." Hawkins and DLo are deck rows. Nothing executed — next pull
  likely moves rows here.
- **Kawhi/Ingram/Dick** — third hold; execution expected before camp, cause
  identified. Still the largest pending three-row move.
- **Maluach (and Ighodaro)** — sourced beneficiaries of the Williams
  exclusion; reprice on the first minutes reporting.
- **Duren** — Oct 1 is 20 days out; QO branch now reported likely.
- **Camp opens in ~2 weeks** — Kuminga usage, Mathurin minutes (verify the
  bench-shape), Simmons (SAC, non-guaranteed) roster fate, Sochan cut watch.
- Carried: Cam Thomas / Ivey / Lonzo unsigned · Ingram heel monitor-tag
  queued for his row's trade rewrite · PHI logjam · Sarr/Sharpe cross-plane
  severity mismatches · D-S1/D-S2 (September plan inputs) still blocked ·
  D-S4 October Routine de-risk · D-S8 Sabonis tag.

## 5. Verification (adversarial pass)

- **C1 — the new protocol caught its first live regression.** The Williams
  exclusion broke `test_draft`'s surname-collision fixture — the injury-aware
  resolver *correctly* auto-resolved where the fixture assumed two draftable
  namesakes. Diagnosed as stale-premise, not code; the fixture now selects
  its collision surname at runtime (currently "Johnson ×4", suffix-aware),
  immune to future pool-health changes. **53/53**, no test skipped or
  weakened.
- **C2 — the tier-mover carries three independent source clusters** (wire/
  AOL, ESPN ledger, two Suns outlets) before any edit; the GP figure is
  labeled probability-weighted with its range, not presented as a timetable
  the sources don't contain.
- **C3 — receipts honesty**: all 8 receipts above were run *this* pull; the
  F1 table is the enforcement the 9/8 miss bought.
- **Bounds:** every direct fetch remains egress-blocked; claims rest on
  dated search results across independent outlets. "As of Friday" phrasing
  in one Kawhi summary is treated as summarizer-dated; the third-hold
  finding rests on the not-yet-executed reporting cluster, not that stamp.
  Roster verification remains `fallback-partial`.

## 6. Gates

`verify_rosters` 255/255 dated 2026-09-11 · `check_provenance` exit 0 ·
`freshness --stamp` with explicit `--pool-changes` (2 rows, zero team edits) ·
`build_deck.py` **all six gates** green (255 players, pull 2026-09-11, pool
`cfe14ff9ab26`, round-trip byte-identical, colophon gate 6 passing on the
rewritten paragraph) · `check_parity` **EXACT MATCH** · `test_gates` **15/15**
· `test_draft` **53/53** (fixture repair above) · `check_report.py` PASS ·
`judgment_open_items --check-report` PASS (8/8 receipts) · kit board diff:
Mathurin 141→188, no entries/exits · **artifact republish HELD at owner
instruction** — deck is built and safe-to-publish; will publish on your go.
