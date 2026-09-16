# After-report — Yahoo player rankings vs the internal board (2026-09-16)

**Owner request (2026-09-16, verbatim):** "Provide an after report of your analysis
of yahoo player rankings against your internal one."

**Analyzed:** `report/market/yahoo-2026-09-15.csv` (300 players, XRank + ADP as of
2026-09-15 per the owner's paste, landed at commit `b0c9f48`) against the
first-principles board — `rank_engine.py` over `projections-2026-27.csv` at the
2026-09-15 pull head (`3c30933`, PR #21 lineage). Derived artifacts:
`consensus-2026-09-15.csv`, `disagreements-yahoo-2026-09-15.md`,
`unmatched-yahoo-2026-09-15.md`. Statistics computed 2026-09-16 by
`report/market/market_stats.py` (committed beside this report; two runs,
identical output).

Pull window: 2026-09-15 → 2026-09-15 (market snapshot date; this is an analysis
report, not a roster pull — the 9/15 pull-log row covers the window and the
flagged-name receipts of record live in `after-report-2026-09-15.md`).

**Method.** Owner paste transcribed verbatim and parsed under invariants I1–I5
(XRank coverage verified as the complete 1..299 plus one placeholder 668; ADP
non-decreasing over a strict 189-row prefix; duplicate name lines used as a
transcription check). Joined to all 235 pool players under the work order's hard
unmatched gate (214 matched, 21 verified genuine absences — every surname grepped
against the raw). Divergence measured by Spearman rank correlation, gap medians,
§5.3 arbitrage at ±15 picks, and a 9-cat z-lean aggregation over the value and
fade sets. Verification: transcription gate PASS, join gate PASS (0 unexplained),
consensus averages recomputed independently with zero mismatches, this file
passes `report/check_report.py`.

**Headline.** Yahoo's market data is genuinely exogenous — ρ(our rank, XRank) =
0.76 and ρ(our rank, ADP) = 0.70, well below the ~0.88 the deck's synthetic
`Mkt` column achieves with our own board *by construction* — and the disagreement
has a clean structure: the room pays for points, rebounds, and name recognition;
our 9-cat engine pays for steals, FT%, and turnover discipline. Median gap in the
adjudicable band (our top-140) is 20 picks; 47 of 131 players diverge by 25+.
Zero team mismatches across all 214 matched players — the roster state passed an
external audit. The market's biggest gift at our draft slot: Dyson Daniels (our
#9, room ADP 62.9). The three fades big enough to also be *our* problem: Jaylen
Brown, LeBron James, Keyonte George — each a top-52 room pick our board prices
90+ picks lower, flagged for line re-derivation next pull.

---

## 1. What was compared

| quantity | value |
|---|---|
| Yahoo list | 300 players; XRank 1..299 complete + one placeholder 668; ADP on top 189 rows (max 125.2) |
| Our pool | 235 projection rows; board = availability-adjusted 9-cat z-scores |
| Matched | 214 of 235 (aliases applied; 21 verified absences, see `unmatched-yahoo-2026-09-15.md`) |
| Both rank signals + ADP | 176 players |
| Team agreement | 214 of 214 — zero mismatches (EVIDENCE: join output, 2026-09-16) |

The 2026 rookie class is fully covered on both sides (Boozer, Dybantsa, Peterson,
Acuff, et al. all matched); the pool's gaps against Yahoo are veterans — see §8.

## 2. How much outside information the market adds

The 8/21 work order (§2) measured that the deck's `Mkt` column correlates ~0.88
with our own board because it is *derived from* our z-scores; it structurally
cannot say the room disagrees with us. Against real Yahoo data (EVIDENCE,
`market_stats.py` 2026-09-16):

| pair | n | Spearman ρ | median abs gap |
|---|---|---|---|
| our rank vs Yahoo XRank | 214 | 0.762 | 30 picks |
| our rank vs Yahoo ADP | 176 | 0.701 | 27 picks |
| our rank vs ADP, our top-140 band | 131 | — | 20 picks (47 of 131 at 25+) |

INFERENCE: at ρ ≈ 0.70–0.76 the market is broadly sane (no sign our board or
their list is broken) while carrying real independent signal — exactly the
regime where an arbitrage table earns its keep. This also confirms the work
order's premise: replacing the synthetic `Mkt` with this data (gated step 5)
would change what the draft-day survival model believes.

## 3. The category signature — why we diverge

Mean 9-cat z-scores on our board, for band-limited values (our rank 15+ picks
ahead of ADP, n=47) vs fades (the reverse, n=39) (EVIDENCE, `market_stats.py`):

| category | value set | fade set | value minus fade |
|---|---|---|---|
| STL | +0.45 | −0.43 | +0.88 |
| FT% | +0.20 | −0.42 | +0.62 |
| TOV | +0.14 | −0.27 | +0.41 |
| 3PM | +0.14 | −0.22 | +0.36 |
| BLK | +0.03 | +0.04 | −0.01 |
| AST | −0.03 | +0.08 | −0.12 |
| FG% | +0.00 | +0.15 | −0.15 |
| PTS | +0.03 | +0.19 | −0.16 |
| REB | −0.08 | +0.19 | −0.26 |

INFERENCE: the room drafts scoring volume, boards, and interior efficiency; it
systematically underpays steals, FT%, and low turnovers — the quiet categories a
9-cat league scores just the same. Draft-night consequence at slot 5: our value
targets should still be on the board a round or two past where we rate them,
while our fades will leave early without costing us anything. One structural
caveat: the board is punt-agnostic — a Giannis (our #61 on FT% drag, room 12.3)
is correctly cheap on a neutral board and elite in a punt-FT% build, so §4/§5
reads assume no punt is locked.

## 4. Where we are higher than the room (values)

47 players at 15+ picks; the largest, with our board's structural reason
(EVIDENCE: `disagreements-yahoo-2026-09-15.md` §B):

| gap | player | our # | ADP | our z-lean |
|---|---|---|---|---|
| +66 | Reed Sheppard | 50 | 115.8 | +STL, +3PM |
| +66 | Jimmy Butler | 55 | 120.5 | +FT%, +STL |
| +63 | Nikola Vučević | 49 | 111.9 | +REB, +FG% |
| +54 | Dyson Daniels | 9 | 62.9 | +STL, +TOV |
| +53 | Myles Turner | 42 | 95.4 | +BLK, +TOV |
| +52 | Kristaps Porziņģis | 54 | 106.0 | +BLK, +REB |
| +46 | Zach LaVine | 74 | 120.3 | +3PM, +PTS |
| +44 | Cam Johnson | 64 | 107.9 | +3PM, +FT% |
| +44 | Ty Jerome | 52 | 95.7 | +STL, +FT% |
| +43 | Fred VanVleet | 78 | 120.6 | +STL, +AST |

Also notable inside the top 60: Anthony Davis (our 7, ADP 24.9), Devin Booker
(our 13, ADP 31.6), Joel Embiid (our 22, ADP 47.9 — the room now discounts his
availability *harder* than our streaming-credit model does), and rookie Cameron
Boozer (our 45, ADP 62.6). Dyson Daniels is the headline: a top-10 player on our
board that the room lets sit to pick ~63.

## 5. Where the room is higher than us (fades)

39 band-limited players at 15+ picks. The room's end of the top of that list
(EVIDENCE: consensus CSV, extracted 2026-09-16):

| gap | player | our # | ADP | read |
|---|---|---|---|---|
| −100 | Jaylen Brown | 132 | 32.2 | re-derivation flag |
| −98 | LeBron James | 139 | 40.8 | re-derivation flag |
| −92 | Paolo Banchero | 129 | 37.5 | re-derivation flag |
| −76 | Donovan Clingan | 117 | 40.7 | room prices year-2 leap |
| −72 | Julius Randle | 136 | 64.1 | PTS/REB profile, our engine cool |
| −72 | Kon Knueppel | 109 | 37.2 | room prices year-2 leap |
| −49 | Giannis Antetokounmpo | 61 | 12.3 | FT% drag; punt-build elite |
| −42 | Alperen Şengün | 60 | 18.4 | FT%/TOV drag on our board |
| −33 | Zion Williamson | 103 | 70.1 | availability history priced by us |

Two honest readings and both go in: (a) for draft night, fades cost nothing —
let the room take them early; (b) a 90+ pick gap on a top-52 room pick can also
mean *our* line is stale. Jaylen Brown, LeBron, and Banchero (plus Keyonte
George, our 181 vs ADP 52.4, just outside the band) carry a re-derivation flag:
next pull, re-source their 2026-27 role assumptions before trusting our number.
Caveat repeated from the disagreements doc: Yahoo publishes ADP only to 125.2,
so "fades" among players we rank 140+ are partly an ADP-truncation artifact and
were excluded from the band statistics above.

## 6. Availability pricing — market vs our GP discounts

Four matched players carry our GP ≤ 40 while the market still prices them
(EVIDENCE: disagreements §D):

| player | our GP | our # | XRank | ADP |
|---|---|---|---|---|
| Kawhi Leonard | 35 | 25 | 18 | 20.0 |
| Mark Williams | 15 | 124 | 96 | 102.7 |
| Shaedon Sharpe | 18 | 134 | 146 | 114.2 |
| Donte DiVincenzo | 15 | 170 | 251 | — |

INFERENCE: the market believes Mark Williams returns meaningfully this season
(ADP 102.7 vs our 15 GP from the 9/10 surgery reporting); Yahoo is one outlet,
so the 15 GP stands until the standing October must-do re-sources it. Kawhi at
ADP 20 vs our #25 is *agreement* on value and a mild disagreement on games.

## 7. The room vs Yahoo's own experts

Inside Yahoo's own data, the room reaches 120–190 picks above Yahoo's expert
rank on a distinct cluster (EVIDENCE: `market_stats.py`): Caruso (OKC), AJ Green
(MIL), Aaron Wiggins (ATL), Kennard (PHX), Klay Thompson (MIA), Horford (GSW),
T.J. McConnell (IND), Allen Graves (TOR), Hauser (BOS), Kornet (SAS), Nesmith
(IND), Broome (LAC). INFERENCE: veteran role players on strong or beloved teams
— name-brand drafting. Our board agrees with Yahoo's experts on every one of
these it can see (e.g., AJ Green our 212, Hauser 208, Klay matched deep), so no
action — except **Allen Graves**, a name neither our pool nor any prior pull has
ever carried, whom the room drafts at 98.4 against expert rank 250. Identity
UNVERIFIABLE this session (all sports/news egress blocked by environment policy;
no fetch possible) — top of the next pull's watchlist.

## 8. Coverage gaps — Yahoo names our database cannot price

86 Yahoo names are not in the pool; 13 carry an ADP inside 140. Tiered verdicts
on pool adds (each add requires a sourced projection row; the tier states what
would demote it):

| tier | player | XRank | ADP | demoted if |
|---|---|---|---|---|
| HIGHLY RECOMMEND | Deandre Ayton (WAS C) | 160 | 118.3 | sourced projection puts him below streaming replacement |
| HIGHLY RECOMMEND | Adem Bona (PHI C) | 189 | 85.4 | role reporting shows backup minutes behind Embiid |
| HIGHLY RECOMMEND | Julian Champagnie (SAS F) | 151 | 114.0 | SAS wing rotation crowds his minutes |
| INVESTIGATE FIRST | Keaton Wagler (LAC SG) | 149 | 121.5 | identity vs pool's Keaton Wallace unresolved — see Watchlist |
| INVESTIGATE FIRST | Allen Graves (TOR PF) | 250 | 98.4 | identity unknown to the system entirely |
| NICE TO HAVE | Aday Mara (OKC C), Duncan Robinson (DET) | 209 / 205 | 91.5 / 96.3 | expert rank ~205+ says thin margins |
| NOT NEEDED | Horford, Kornet, Kennard, McConnell, Wiggins, Broome | 220–668 | 86–105 | room-only reaches; both the experts and our engine rate them late-round names |

## 9. Watchlist (next pull)

| item | evidence / receipt |
|---|---|
| Allen Graves (TOR) identity + why the room pays 98.4 | Yahoo row XRank 250 / ADP 98.4, 2026-09-15; name absent from all prior pulls |
| Keaton Wagler vs pool's Keaton Wallace (both LAC guards) | Yahoo lists Wagler ADP 121.5; pool row is Wallace; surnames differ, not aliased per verification rule |
| Jaylen Brown, LeBron James, Banchero, Keyonte George line re-derivation | gaps −100/−98/−92/−129 vs room ADP, this report §5 |
| Mark Williams return timetable vs market's ADP 102.7 | standing October must-do; our GP 15 from 9/10 surgery reporting |
| Gradey Dick absent from Yahoo's entire 300 | unmatched report 2026-09-15; camp-role check due |
| Pool-add candidates from §8 pending owner decision | this report §8 tiers |

## 10. Open-item receipts

Analysis receipts for this report (the 9/15 pull's flagged-name receipts of
record are in `after-report-2026-09-15.md` §receipts, unchanged):

| check | receipt |
|---|---|
| Transcription gate I1–I5 | PASS 2026-09-16; XRank gaps in 1..299: NONE; 189-row monotone ADP prefix |
| Hard unmatched gate | PASS 2026-09-16; 235/235 matched or accepted (0 unexplained) |
| 21 absences surname-verified | grep battery vs raw, 2026-09-16: 19 absent; Wallace only as Cason; Murray only as Keegan/Dejounte/Jamal |
| Consensus averages | independently recomputed over all 235 rows, zero mismatches, clean 1..235 permutation |
| Statistics reproducibility | `market_stats.py` run twice 2026-09-16, byte-identical output |
| This file vs publication gate | `report/check_report.py` PASS 2026-09-16 |

## 11. Bounds

**Out of scope by design:** no pool row was edited (Yahoo is a single outlet —
fix F2); the first-principles board method is untouched (owner decision
2026-08-21); the deck plane and `marketRanks` are untouched (work-order gated
step 5, and the deck repo is outside this session's GitHub scope); fades beyond
our rank ~140 were excluded from statistics (ADP truncation); Yahoo position
eligibility is stored in `yahoo-2026-09-15.csv` but not compared against pool
positions.

**In scope and unverified:** team codes and ADP digits on the ~80 deep
Yahoo-only rows beyond the 6 spot-checked — NOT-ATTEMPTED (bounded impact: no
conclusion in this report rests on any single such row). Allen Graves and
Wagler-vs-Wallace identities — UNVERIFIABLE this session (sports/news egress
blocked by environment network policy; no lookup channel available). The meaning
of Yahoo's 668 placeholder tier — INFERENCE from list structure (asserted
nowhere in the paste).

## 12. Decision sheet (owner disposes; nothing below was executed)

- **D-M1 — pool adds.** Approve §8 tiers? Each HIGHLY RECOMMEND needs a sourced
  projection row (same process as D1/D-S1 inputs).
- **D-M2 — line re-derivations.** Authorize re-sourcing Jaylen Brown, LeBron,
  Banchero, Keyonte George role assumptions next pull (no board edit until
  two-source evidence).
- **D-M3 — consensus role.** Keep `consensus-2026-09-15.csv` as a reference
  lens, or promote real market data into the deck's `Mkt`/survival model —
  the work order's gated step 5, a cross-plane, parity-locked change.
- **D-M4 — second ADP source** to complete D-S2 (Yahoo now in hand,
  single-outlet).

## 13. Provenance

Produced 2026-09-16 by the operating session
(`https://claude.ai/code/session_01QjgeRdpDaWgSJmGKRG8fTU`) on branch
`claude/market-data-workorder-mnfi2b` (PR #22, stacked on #21 ← #20). Sources:
the owner's 2026-09-15 Yahoo paste (raw at `report/market/yahoo-raw-2026-09-15.txt`);
committed artifacts at `b0c9f48`; board state at `3c30933`. Re-verify any figure:
`python3 report/market/yahoo_market.py 2026-09-15` (gates + artifacts) and
`python3 report/market/market_stats.py 2026-09-15` (statistics).
