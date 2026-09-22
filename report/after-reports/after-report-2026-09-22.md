# After-report — 2026-09-22 data pull + pool completion + deck v24 / v25

**Owner request (2026-09-22, verbatim):** "Proceed with all actions, in order of
your recommendation. Research and Add all missing players to your internal
database." The recommended order, executed in full: merge the eleven open
PRs from the 9/21–9/22 work; build and publish deck v24 (the 9/22 pull, Yahoo
prices baked, advice-only punt advisor); refit the survival chips on the two
live rooms; research and add every Yahoo top-300 name the pools lacked;
rebuild and publish v25; verify.

Pull window: 2026-09-21 → 2026-09-22 (1 day). Gate: `check_provenance.py`
PASS — all rows sourced; verified 2026-07-13 .. 2026-09-22.

**Method.** The deck's freshness gate refused any rebuild on 9/21 evidence,
so the day opened with a full F1–F6 pull (7 flagged receipts, team-shadow set
CHI/DET/NOP/NYK/POR/SAC, ledger-shaped transaction sweep, injury sweep against
the F6 tag inventory) — 22 dated WebSearch passes on the summary channel
(direct sports fetches egress-blocked; two-outlet rule per claim; two
fact-checked fakes logged). Then the pool-completion research: 78 names
(76 Yahoo-only names plus the Tre Mann and Whitmore checks), two dated
outlets each, in the session scratch ledger `adds/research.jsonl`. Every
edit below was applied by script with exact-match assertions and every gate
re-run. This file passes `report/check_report.py` and the deck's
`judgment_open_items.py --check-report`.

## 1. Roster changes

| plane | change | count |
|---|---|---|
| kit | Cam Whitmore CLE → DEN — Nuggets two-way 9/18 (Hoops Rumors, SI.com Nuggets); stats held | 1 |
| kit | rows added — Yahoo top-300 names the pool lacked (§4) | 73 |
| kit | not added, left the NBA: Batum retired 9/21 (Hoops Rumors, ESPN); Valančiūnas waived by DEN in July and signed Žalgiris (RealGM, Hoops Rumors); Westbrook retired 8/12 (NBA.com, PFN) — kit rule §3 | 3 |
| deck | rows added — the 66 of those names the deck also lacked, incl. Batum and Valančiūnas as FA `out-*` rows for resolver coverage (§4) | 66 |
| deck | placements moved among the 264 incumbent rows | 0 |
| both | lines changed on incumbent rows | 0 |

## 2. Flagged-item receipts (F1) — verdicts

| player | verdict | evidence (dated 2026-09-20 to 09-22) |
|---|---|---|
| Jalen Duren | HELD −0.08; holdout branch named | Detroit raised its offer Monday 9/21 to a fully guaranteed 5yr/$200M, no options; reported rejected, may skip media day or the start of camp — Shams/ESPN via Yahoo ×3, HoopsHype 9/21, CBS Sports, Yardbarker, ClutchPoints; $9.6M QO branch stands, Oct 1 nine days out |
| Jeremy Sochan | HELD −0.20 | POR one-year non-guaranteed; camp battle now framed as Sochan vs Micah Potter for the last spot — Rip City Project ×2, KGW |
| Cam Thomas | HELD FA | still unsigned; no dated signing surfaced — SI Nets, Yardbarker |
| Jaden Ivey | HELD FA; garble logged | "Lakers sign Jaden Ivey" ($4M / $6.5M variants) is a fact-checked FAKE — heavy.com, EssentiallySports: no reporter, no team, satire/social accounts |
| Lonzo Ball | HELD FA; garble logged | social posts claiming vet-min deals with MIN / PHI carry no outlet; still unsigned — Yahoo, SI Kings |
| Jalen Brunson | HELD −0.05 | ready for camp with no restrictions (ESPN's Goodwill via RotoWire; Eastern Herald 9/20; nyknicksnews); camp 9/29 |
| Bennedict Mathurin | HELD −0.05; checkpoint stands | SI Pelicans counts six rotation players who need the ball; bench line holds — SI, Yahoo, FanSided |

## 3. Window sweep, team shadows, injury sweep

Ledger-shaped query (Spotrac / ESPN transactions): 9/21 Jaden Bradley TOR
(two-way converted to a 4yr/$9.26M standard deal), D.J. Armstrong CHA
(Exhibit 10); 9/20 Ogi Agbim GSW (Exhibit 10), Bez Mbeng waived by CHA. None
is a row on either plane. Zero trades in the one-day window — the F5
zero-trade rule applies to multi-day windows; the ledger query is cited
regardless. Team shadows CHI / DET / NOP / NYK / POR / SAC returned nothing
that touches a row (DET: Duren unsigned; NYK: Sochan no longer an option,
Tyler Nickel camp item; SAC: Ben Simmons SAC re-confirmed). Kawhi: TOR
extension talks "advanced" per Fischer/Stein Line, now multi-outlet (Hoops
Rumors, RotoWire, RealGM, CBS, NBC Sports, Yardbarker) — card unchanged.
MEM cut-down (Hawkins / DLo / Clayton / Kris Murray) still reported, not
executed — seventh pull; rows hold (Yahoo, SI Grizzlies, HoopsHype).

Injury sweep vs the F6 inventory (8 excluded, 31 risk-tagged): no new
returner and no new setback on a row. Returning-player coverage found only
already-tagged names (Embiid on track, Ingram heel spur removed in May —
both carried). The Kuzma-China MRI item resurfaced again (2019 story;
garble logged 9/21).

**Garble log** — instances 7 and 8 (the Ivey and Lonzo social fakes; see
§2). Both were caught because the sweep treats an undated social snippet as
a claim to fact-check, not a finding.

## 4. Pool completion — the adds

**Scope.** The 9/22 Yahoo top-300 paste (`report/market/yahoo-2026-09-22.csv`)
listed 76 names absent from the kit pool (disagreements report §E), 66 of
them absent from the deck too. Every name was researched with two dated
outlets (role, minutes, games, contract status), plus dedicated stat lookups
for the six with no Hashtag or Statdunk line.

**Lines (kit `projections-2026-27.csv`, 73 rows).** The Hashtag 8/24
per-game line scaled to the researched 2026-27 role — the minutes ratio,
capped ×0.5–1.5, applied to the volume categories; percentages held; GP the
midpoint of the researched range — labeled **[ESTIMATED]** with that
mechanism (DATA-PULL §3). The nine names the deck already carried (Horford,
Hardaway Jr., Merrill, Post, Schröder, Moody, Ziaire Williams, Alvarado,
LeVert) take the deck's existing researched line, so the planes do not
diverge on the day both gain the row. No Hashtag/Statdunk line (5): Broome
(2026 Summer League 14.7/9.0 in 27.4 mpg translated to a ~10-mpg fringe role
at a rookie discount), Tony Bradley (2025-26 IND 4.1/2.9 in 11.2 mpg held),
Brandon Williams (2025-26 DAL 13.0/2.9/3.9 scaled to the GSW bench role),
Bruce Brown and John Konchar (NYK Exhibit 9 camp bodies — bench-guard shapes,
GP discounted for the roster battle). Moody GP 20 (torn patellar tendon, 9–12
months — exclusion class, matching the deck's `patellar-recovery` tag); Gueye
GP 52 (fractured left foot, out to start). Provenance: one row per name,
first outlet URL, `verified_on` 2026-09-22.

**Deck rows (`data/players.csv`, 66 rows; PR #40 merged).** Same lines,
Yahoo's team and positions, notes carrying the role class with the
mechanism: `bench-role` / `starter-watch` / `rookie-proj` (Mara, Burries,
Broome) / `camp-deal` (Brown, Konchar) / `camp-battle` (Krejčí) /
`inj-foot-risk` (Gueye → 0.78) / `out-retired` (Batum, FA) / `out-europe`
(Valančiūnas, FA). The two non-NBA names are kept as rows, like Westbrook and
Brogdon, so the live resolver logs a room's pick of them instead of refusing.
Evidence ledger: 66 placements added under their teams.

**Not added to the kit (3).** Batum, Valančiūnas, Westbrook — the kit rule
(DATA-PULL §3) removes players who leave the NBA. Yahoo still lists Westbrook
at SAC and Valančiūnas at DEN; both labels are stale (retired 8/12; waived in
July). They remain the only three Yahoo-only names.

**Board effects (kit `top-200-2026-27.md`, 318 projected).** Nine entries /
nine exits, all at the tail: in — Jordan Goodwin (109), Scotty Pippen Jr.
(138), Al Horford (161), Cam Spencer (167), Kris Dunn (173), Gui Santos
(181), Jose Alvarado (186), Jake LaRavia (194), Luke Kennard (198); out —
Maluach, Dillingham, Toppin, Mathurin, Shannon Jr., Demin, Wells, Jakučionis,
Tre Johnson (192–200 before). 43 moves of ≥3 ranks, every one inside 125–200
and every one a slide of 3–12 places from the wider z-score pool (Fears
188 → 200 the largest); the top 120 is unchanged. No incumbent line moved.

**Yahoo intake re-run (`yahoo_market.py 2026-09-22`).** 318 pool players,
297 matched to Yahoo, 21 accepted absences (unchanged list), Yahoo-only
names 76 → 3. Transcription gate PASS (I1–I5).

## 5. Deck builds and publishes

| build | what | record |
|---|---|---|
| v24 | 9/22 pull; first build on `main` with the 9/22 Yahoo paste baked — Mkt rank = Yahoo ADP else XRank on 230 of 264 rows (F8); advice-only punt advisor (D51R-3); judgment re-authored 2026-09-22 | deck PR #39 merged (592ae42); published to the standing artifact URL, Version 24 |
| refit | survival chips back on the price-only model (D51R-1R): P(alive at N) = Φ((price − N)/max(8, 0.30·price)) on the baked Yahoo price; Brier 0.192 on the 98 pooled live rows vs 0.651 shipped (constant base rate 0.212; leave-one-room-out 0.180 / 0.207 vs 0.210 / 0.215); quiet rows survived 40 of 43, BUY NOW gone 10 of 15, TOSS-UP a coin flip — the measured rates are stated on the chip tooltip and colophon | deck PR #41 merged (b7c0825) |
| v25 | pool 264 to 330 with the 66 adds (PR #40 merged, 1e4e663) + the refit; Yahoo prices on 296 of 330 rows | deck PR #42 merged (175f8e4); published to the standing artifact URL, Version 25 — the deck the owner opens now |

## 6. Gates (2026-09-22)

| gate | result |
|---|---|
| kit `check_provenance.py` | PASS — 318/318 sourced |
| kit `check_report.py` + deck `judgment_open_items.py --check-report` | PASS on this file |
| kit `yahoo_market.py` transcription gate | PASS (I1–I5); join 297/318 |
| deck build gates 1–7 (v24) | green — verify 264/264, planes 235 shared / 0 mismatches, market 230/264 |
| deck build gates 1–7 (v25) | green — verify 330/330, planes 308 shared / 0 mismatches, market 296/330, injection round-trip OK |
| deck `test_gates` / `test_card` / `test_draft` / `check_parity` | 34/34 · 27/27 (6 new refit cases, red-first) · 57/57 · EXACT (new item 7: survival probabilities bit-identical) |
| deck `check_planes.py` vs this branch | 308 shared · 0 team / exclusion / drift / propagation |

## 7. Watchlist / open items

- **Duren** — camp opens 9/29; if he sits, widen the card (holdout branch now
  named). Oct 1 QO deadline.
- **Survival chips** — re-fit after the next live room; n=98 is two rooms.
  BUY NOW is two-in-three, not a certainty; the quiet side (safe to wait)
  is the reliable signal.
- **Whitmore** — kit GP 30 on a two-way (50-game NBA limit); no sourced role
  mechanism yet; the deck has no row (never in a live room).
- **Yahoo team labels** — Westbrook (SAC) and Valančiūnas (DEN) are stale
  on Yahoo's page; both planes keep the researched status.
- **MEM cuts** — still reported-not-executed; Hawkins and DLo are deck rows.
- **Kawhi extension** — advanced, multi-outlet, no deal yet; card unchanged.
- **Gueye** — return timeline unsourced beyond "out to start"; re-check at
  camp.
- **Camp bodies** — Bruce Brown, Konchar (NYK), Krejčí (POR), Sochan (POR):
  non-guaranteed; a cut returns each to FA with no line.

## 8. Open-item receipts

| player | query run (2026-09-22) | dated finding |
|---|---|---|
| Jalen Duren | Jalen Duren Pistons qualifying offer contract September 22 2026 · Pistons increase Jalen Duren offer five years $200 million | offer raised 9/21 to 5yr/$200M fully guaranteed, rejected; Yahoo ×3, HoopsHype, CBS, Yardbarker, ClutchPoints |
| Jeremy Sochan | Jeremy Sochan Trail Blazers roster camp September 22 2026 | non-guaranteed; Potter battle; Rip City Project, KGW |
| Cam Thomas | Cam Thomas signs free agent September 2026 · still unsigned training camp | still unsigned; SI Nets, Yardbarker |
| Jaden Ivey | Jaden Ivey signs free agent September 2026 · Jaden Ivey Lakers one-year deal | Lakers signing = fact-checked fake; still unsigned; heavy, EssentiallySports |
| Lonzo Ball | Lonzo Ball free agent signs retire September 2026 · agrees one-year veteran minimum | social-only MIN/PHI claims, no outlet; still unsigned; Yahoo, SI |
| Jalen Brunson | Jalen Brunson wrist Knicks training camp September 22 2026 | camp-ready, no restrictions; RotoWire, Eastern Herald, nyknicksnews |
| Bennedict Mathurin | Bennedict Mathurin Pelicans rotation role September 22 2026 | bench line holds; SI Pelicans, Yahoo, FanSided |
| (window sweep) | NBA transactions September 21 2026 signed waived traded · NBA news September 22 2026 | Bradley TOR conversion, Armstrong CHA E10, Agbim GSW E10, Mbeng waived; Spotrac, ESPN |
| (injury sweep) | NBA injury news September 22 2026 surgery out training camp | nothing new on a row; NBA.com, ESPN, covers |
| (CHI/DET/NOP/NYK/POR/SAC) | team-shaped news queries, one each | consistent with pools; Yahoo, ESPN, SI, CBS |
| (MEM shadow) | Grizzlies waive Jordan Hawkins D'Angelo Russell roster cuts September 22 2026 | reported-not-executed; Yahoo, SI, HoopsHype |
| (Kawhi) | Kawhi Leonard Raptors extension talks September 22 2026 | advanced, multi-outlet; Hoops Rumors, RotoWire, RealGM, CBS, NBC |
| Russell Westbrook | Russell Westbrook retirement announcement August 2026 OR unsigned free agent September 2026 | retired 8/12; NBA.com, PFN — Yahoo's SAC label stale |

## Provenance and bounds

- Research channel: WebSearch summaries only; every claim above is dated
  and carries the outlets named in its row. Two fakes were detected by
  fact-check outlets, not by this sweep's own judgment — the rule that an
  undated social snippet is a claim to check, never a finding, held.
- The 73 kit lines are role-scaled Hashtag lines, not observed production;
  they rank at the tail (highest new entry #109) and move nothing in the
  top 120. Each carries [ESTIMATED] by construction.
- The survival refit is fit on 98 rows from two rooms; leave-one-room-out
  beats each room's base rate by 0.008–0.030 Brier — real but thin.
- Not verified by direct fetch: any roster page (egress policy). The
  evidence ledger remains fallback-partial.
