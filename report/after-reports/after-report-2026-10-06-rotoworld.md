# After-report — 2026-10-06: NBC Sports' Rotoworld draft kit v2 as a reference source

**Owner input (2026-10-06, verbatim):** "Excellent data for your system. Please analyze and
provide after report of any new findings that you intake for projections or calculations" —
with the PDF `rotoworld-2026-27-fantasy-basketball-kit-v2.pdf` (1.9 MB, 53 pages).

Pull window: 2026-10-06 → 2026-10-06 (owner input; not a roster pull — the 10/06 pull's
report stands on its own).

**What it is (parser output, not memory).** NBC Sports' Rotoworld 2026-27 Fantasy
Basketball Draft Kit, "v2": created 2026-09-25, modified 2026-10-05 (the PDF's own
metadata). Editor-in-chief D.J. Short; staff writers Raphielle Johnson, Zak Hanshew, Noah
Rubin, Cole Huff; the offseason recap by Kurt Helin. Four parts: the recap (pages 3–5), 141
player profiles (50 guards, 50 forwards, 41 centers; each with age, height, weight, the
player's 2025-26 per-game line where he has one, and three prose fields — "2025-26",
"What's Changed", "Outlook"), and four cheat sheets — points leagues (200), 8-category
(200), 9-category (200) and dynasty (300). **It carries no projected stat lines**: the
numbers in it are last season's actuals. Its signal for this system is the 9-category
ranking (our format), the 8-cat and points rankings as cross-checks, and the prose on
roles.

**Method.** The PDF read with pdfplumber page by page; the two-column profile pages
cropped into a left and a right column so each profile's lines stay together; the text
kept verbatim as the raw layer (`report/market/rotoworld-raw-2026-10-05.txt`, PDF sha256
`0ccd0086…`). Parsed deterministically by `rotoworld_pdf_market.py` under invariants (every
sheet's ranks contiguous 1..N; profile ranks contiguous per section; every profile with an
age line; a stat line parses in full or is absent); three transcription traps caught and
handled in the parser (a team code split as "I ND" on the points sheet; Kessler's
five-game percentages printed without the leading dot; a "2TM" team code for traded
players). The 9-cat sheet joined to the pool under the hard gate by
`third_party_market.py rotoworld 2026-10-05` (the same machinery as the RotoBaller,
expert-consensus and projected-150 intakes): Spearman agreement, both disagreement
tables with the board's own z-lean on each row, the kit's projection against each
profiled player's 2025-26 actual line, team mismatches. Both artifacts pinned to their
input commits and registered in `check_derived.py` — 15 of 15 dated artifacts reproduce
byte-for-byte. The cross-source test (every outside source on file against both planes)
computed in scratch from the committed CSVs. No pool row changed: a ranking outlet is
one line of evidence, never an edit (owner decision 2026-08-21; fix F2).

**Headline.** The kit agrees with Yahoo's own ranking far more than with ours (rho 0.950
against Yahoo's XRank, 0.830 against the board), which is the pattern every outside source
has shown: the market ranks by volume and name, the board by nine-category z-scores. 175
of its 200 are in our top 200; zero team mismatches, so its placements match the pool's
verified ledger on all 199 joined names. The useful product is the cross-source list:
**25 names where both planes sit 25 or more places from every outside source on file, in
the same direction** — 14 the board likes more than anyone else (Dyson Daniels at 9 and 11
against 53–69 is the largest at the top of the board), 11 it likes less (Banchero, Keyonte
George, Harper, Dybantsa, Maluach, Nurkić, Anthony Black among them). Those are the WO-5
re-derivation candidates (D-RW-1), to be reviewed name by name against the role evidence
when the lines move after two preseason games. The kit also ranks Acuff Jr. 143rd in 9-cat
(we 190) and its recap says "the Kings are going to hand him the keys" — two more dated
voices on the role, none on the rates (D-1006-1 unchanged). One pool-completeness item
(Hugo Gonzalez, Boston, 180th). And the kit's prose predates late-September news on
several rows, which bounds how far its ranks should be trusted on the injured.

## 1. Roster changes

No roster changes — this is an intake, not a pull. The kit's 9-cat sheet names a team for
all 200 rows and disagrees with the pool's verified placement on none of the 199 it joins
(§D of the disagreements file: 0). Its dynasty sheet carries three stale placements
(§6).

## 2. What landed

| file | what |
|---|---|
| `report/market/rotoworld-raw-2026-10-05.txt` | the PDF's text, 53 pages, profile pages in two columns (3,955 lines) |
| `report/market/rotoworld_pdf_market.py` | the parser (`--extract` once; `<date>` reproducibly) |
| `report/market/rotoworld-sheets-2026-10-05.csv` | 315 names across the four sheets with each sheet's rank, the 9-cat position and team |
| `report/market/rotoworld-profiles-2026-10-05.csv` | 141 profiles: section, rank, age, height, weight, the 2025-26 line (131 have one), the three prose fields |
| `report/market/rotoworld-9cat-2026-10-05.csv` | the 9-cat sheet in the third-party raw shape, with the other sheets' ranks and the profile's 2025-26 line |
| `report/market/rotoworld-parse-2026-10-05.md` | the parse invariants and the input stamp (pin `cfbdf02`) |
| `report/market/rotoworld-2026-10-05.csv` | the join: 199 of 200 rows with our rank, z, Yahoo XRank and ADP, the extra ranks |
| `report/market/unmatched-rotoworld-2026-10-05.md` | the hard-gate report: one name without a pool row (Hugo Gonzalez), no spelling trips; stamp (pin `6001d17`) |
| `report/market/disagreements-rotoworld-2026-10-05.md` | agreement, the two 20-place tables (51 and 72 rows), 0 team mismatches, 59 projection-vs-actual rows, every row |
| `report/market/provenance.csv` | one row, source `rotoworld`, 2026-10-05 |
| `report/check_derived.py` | two registry entries |

## 3. Agreement and the disagreements (computed)

| measure | value |
|---|---|
| 9-cat rows joined | 199 of 200 |
| Spearman rho, our rank vs the kit's 9-cat rank | 0.830 |
| Spearman rho, our rank vs Yahoo XRank (9/28 file), same rows | 0.821 (192 rows) |
| Spearman rho, the kit's rank vs Yahoo XRank, same rows | 0.950 (192 rows) |
| median absolute gap, our rank vs the kit's | 25 places |
| the kit's top 200 inside our top 200 | 175 of 200 |
| our top-200 names the kit leaves out | 25 (Goodwin, Mark Williams, Bogdanović, Keon Ellis, Cam Thomas, Ayton, Risacher, Smart, Ivey, Horford, Dort …) |
| we are higher by 20+ places | 51 rows (largest: Butler +83, Grant +73, Mamukelashvili +71, Herb Jones +70, Caruso +68, Porziņģis +67) |
| the kit is higher by 20+ places | 72 rows (largest: Morez Johnson −148, Queta −138, Flemings −128, Beringer −109, Jaquez −106, Drummond −106, Porter −101) |

For comparison, RotoBaller's 9-cat projections on 9/29 scored rho 0.815 against the board
and 0.941 against Yahoo; the market sources agree with each other more than any agrees
with us, by design.

**The cross-source test.** For every name in the kit's 200 that the board ranks, the four
outside sources on file (this kit's 9-cat, RotoBaller 9/29, Hashtag 9/30, Yahoo's 10/01
XRank) were set against the kit rank and the deck's adjusted-value rank (v44). A name
counts when at least three sources exist and every one sits 25 or more places from the
kit in the same direction; 33 names qualify. Where the two planes disagree with each
other the deck already prices the market's view on eight of them (LeBron 142/61, Jaylen
Brown 135/72, Embiid 22/71, Claxton 60/136, Holiday 93/137 — the deck sits with the
market; the kit is the outlier), so those are kit-line questions for WO-5, not
two-plane questions. The 25 where **both planes** sit 25+ places from every source:

| direction | names (kit rank / deck rank vs the four sources) |
|---|---|
| we are higher | Dyson Daniels (9 / 11 vs 56, 53, 68, 61); Herb Jones (64 / 74 vs 134, —, 169, 134); Jerami Grant (118 / 113 vs 191, 183, 186, 193); Alex Caruso (130 / 131 vs 198, —, 191, 196); Bilal Coulibaly (122 / 133 vs 167, 177, —, 203); PJ Washington (77 / 88 vs 141, 121, 144, 133); Kyle Filipowski (126 / 125 vs 164, 172, —, 198); Aaron Nesmith (97 / 118 vs 152, 154, 135, 150); Nikola Vučević (128 / 124 vs 181, 161, 178, 177); Scotty Pippen Jr. (136 / 134 vs 176, 178, 177, 183); Saddiq Bey (102 / 95 vs 169, 143, 132, 132); Aaron Gordon (96 / 93 vs 132, 147, 145, 127); Josh Hart (53 / 68 vs 91, 94, 85, 97); Tari Eason (115 / 111 vs 147, 140, 147, 163) |
| we are lower | Khaman Maluach (199 / 226 vs 118, 92, 104, 118); Dylan Harper (171 / 148 vs 81, 76, 106, 83); AJ Dybantsa (173 / 141 vs 89, 103, —, 92); Paolo Banchero (131 / 102 vs 65, 60, 101, 52); Keyonte George (117 / 107 vs 61, 63, 83, 43); Jusuf Nurkić (175 / 167 vs 116, 136, 133, 105); Anthony Black (184 / 178 vs 112, 131, 143, 146); Giannis (59 / 42 vs 16, 7, 5, 6); Kon Knueppel (106 / 94 vs 48, 74, 58, 64); Brook Lopez (191 / 171 vs 136, 144, —, 160); Quentin Grimes (170 / 159 vs 145, —, 122, 126) |

The mechanism is visible in the z-leans the disagreements file prints: the names the
board likes more are low-usage stat-stuffers whose steals, blocks, field-goal percentage
and low turnovers score in nine categories (Daniels +STL, Herb Jones +STL, Caruso +STL,
Filipowski +REB, Vučević +FG%); the names it likes less are young volume scorers whose
points and usage the lines price conservatively (Harper, Dybantsa, George, Banchero),
two bigs whose role the lines read as shared (Maluach behind Ighodaro on the 10/5 box
score, Nurkić), and the two availability discounts the owner already set (Giannis D-RT1,
Knueppel D-1002-1). Four of the 14 "higher" names also carry the kit's own warning in
§5 of the disagreements file: Daniels's line has 2.8 steals against 2.0 last season,
Claxton 9.5 rebounds against 6.9, Sabonis 6.8 assists against 4.1, Trae Young 23.5
points against 17.9 — projection-versus-actual gaps that are either a role call or a
stretch, and WO-5 is where each gets its mechanism sentence.

**The kit's own sheets against each other.** Its 8-cat list lifts the turnover-heavy
(Butler 151 → 65, DeRozan 172 → 123, Alexander-Walker 83 → 45, Lillard 85 → 49) and
drops the low-turnover role players (Castle 80 → 107, Watson 109 → 136, Acuff 143 → 176);
its points list lifts the volume names (Porziņģis 115 → 67, Siakam 57 → 22, Zion 71 →
39) and buries the specialists (Knueppel 48 → 84, Anunoby 43 → 82, Mikal Bridges 68 →
111). That is the same lesson as the cross-source test from the other side: the owner's
league is nine categories, and a points-shaped rank is the wrong yardstick for it.

## 4. The role prose against the open items

The kit's profile text is a late-September read (see the bounds), so each line below is a
dated outlet on a role, weighed with the others on the sheet, never a reprice.

| item | the kit (9-cat rank; profile) | bearing |
|---|---|---|
| Acuff Jr. (D-1006-1) | 143rd in 9-cat, 150th points, 61st dynasty; no profile; the recap: "Darius Acuff has an outside shot at winning ROY because he's certainly going to get the opportunity, the Kings are going to hand him the keys" | a fourth and fifth dated outlet on the ROLE; nothing on the rates; D-1006-1's default (hold until game two) stands |
| Rollins vs Porter (MIL) | Rollins 78th (G30: "top 50 value last season … should be a top 75 pick, but a safer option just outside"); Porter 131st (G50: "his role may not align with the one he enjoyed in 2025-26", "younger players like Burries and Rollins may be the focus") | matches the 10/5 box score (Rollins started, Porter the first sub; ESPN's feed, Brew Hoop); the card's HELD stands until game two |
| Jerome vs Pippen Jr. (MEM) | Jerome 101st (G42: Morant's exit "likely puts the keys to the offense in Jerome's hands", "worthy of the first 100 picks", "hit 70 games once"); Pippen Jr. 176th | matches the 10/5 box score (Jerome started; ESPN's feed, SI.com); we have Jerome 50th and Pippen 136th — both higher than the kit |
| Queta vs Robinson (BOS) | Queta 111th yet the profile says "can be left undrafted outside of deep leagues"; Robinson 120th ("inside track to earn the starting gig … a sneaky later-round selection") | the kit's sheet and its prose disagree on Queta; our 249 sits with the prose, the market (Yahoo 103) with the sheet; the opener is 10/8 |
| Steinbach vs Diabaté (CHA) | Steinbach 156th ("upside is capped in this crowded rotation"); Diabaté 122nd ("wait-and-see" on all three centers); Naz Reid 67th | in line with the pool's hold; Charlotte plays tonight |
| Kessler (D-RT2) | 39th (C7: "early-round upside", health and FT% the questions) | next to our 37 |
| Duren | 50th (C8, written before the 10/1 extension: "three major red flags") | the kit's text is stale on the contract; the rank is close to our 58 |
| Edey | 66th (C15: "availability is a major concern") | matches our 66 and the tag |
| Ware vs Turner (MIL) | Ware 63rd ("a chance to end the season as the starting center"); Turner 98th ("a trade candidate" — the kit's read alone [SINGLE-SOURCE]) | our 84 and 89 sit between; the 10/5 box score had Turner starting, Ware 24 minutes off the bench |
| Knueppel (D-1002-1) | 48th (G22: "top 50 value should represent his floor", written before the hamstring) | the kit does not price the injury; our 106 does; the sheet's default holds |
| Coby White (D-1006-2) | 76th (G29: "should be selected outside the first 75 picks", written before the calf strain) | our 101; no bearing on the tag question |
| Strus (D-1005-2, closed) | 154th, no profile — ranked before the 10/5 diagnosis | stale; the exclusion stands |
| Ingram, Porziņģis, Kawhi (receipts) | 64th (F24, written before the 9/14 trade execution and the Achilles disclosure), 115th (C24, no mention of the health issue), 15th (F6) | the first two predate the news the cards carry (ESPN, NBA.com, NBC Sports); Kawhi's 15 sits next to our 12 |
| Morant and Lillard (POR) | 74th and 85th; both profiles call the point-guard room "crowded" and leave the minutes to Nori | our 139 and 92; the first game is 10/7 |

## 5. Pool completeness and spelling

- **Hugo Gonzalez (BOS)** — 180th in 9-cat, 128th in dynasty, absent from the points and
  8-cat sheets; no pool row; no spelling variant in the pool, so the hard gate passed. One
  outlet at 180 is below the pool's MUST_HAVE bar; on the sheet as D-RW-2.
- The dynasty sheet's 51 names outside the pool are rookies, two-way and camp bodies
  (Stirtz, Sorber, Carr, Topić, Ament, Clayton Jr., Essengue …) plus one spelling of a pool
  row — "Ronald Holland II" for the pool's Ron Holland — and is not joined under the gate
  (dynasty is not the league's format). No alias needed for the 9-cat join.
- Names the kit spells differently across its own sheets (Porziņģis with and without
  the second diacritic; "Jimmy Butler" and "Jimmy Butler III"; "Hugo Gonzalez" and
  "Hugo González") fold to one key under the planes gate's normalisation.

## 6. What is stale in the kit (bounds on trusting it)

The cheat sheets were edited after the profiles. Evidence in the parser output:

| item | the kit | the ledger |
|---|---|---|
| Konchar | dynasty 264th as NYK | the Knicks let him go 9/30 (RealGM, Hoops Rumors); FA on both planes |
| Dillingham | dynasty 268th as CHI | Charlotte parted with him 9/28 (Hoops Rumors, RotoBaller); FA on both planes |
| Day'Ron Sharpe | dynasty says CHI, the 9-cat / points / 8-cat sheets say BKN | BKN on both planes (ESPN's feed, direct) |
| Strus | 154th, no injury note | partial plantar fascia tear 10/5 (ESPN, NBA.com) — excluded 10/6 |
| Ingram's profile | "barring an agreed-upon deal … falling through" | the trade executed 9/14 and the Achilles disclosure came 9/28 (ESPN, NBA.com) |
| Porziņģis's profile | no health item | out indefinitely since 9/28 (NBA.com, NBC Sports) |
| Duren's profile | contract talks unresolved | the extension agreed 10/1 (NBA.com, ESPN) |
| Hawkins, Broome | on no sheet | — |

So the kit's 9-cat ranks on injured or recently moved players carry the pre-news view;
its ranks elsewhere are a late-September to early-October market read.

## 7. Watchlist / open items

- **WO-5** — the 25 two-plane names in §3 join the re-derivation list; each gets its
  mechanism sentence or a "line stands" with the reason.
- **Acuff Jr.** — D-1006-1 unchanged; game two on 10/8.
- **Queta** — the kit's own sheet-versus-prose split; Boston's opener 10/8 decides more
  than any ranking.
- **Hugo Gonzalez** — D-RW-2.
- The deck is untouched by this intake (it reads the kit's Yahoo paste only, F8); nothing
  to republish.

## Open-item receipts

| player | query run | dated finding |
|---|---|---|
| Brandon Ingram | the kit's 9-cat sheet and profile F24 (parsed 2026-10-06) | 64th; the profile predates the 9/14 trade execution and the 9/28 Achilles disclosure — NBC Sports' Rotoworld v2; the card's HELD stands (ESPN, NBA.com for the news) |
| Kristaps Porzingis | the kit's 9-cat sheet and profile C24 | 115th in 9-cat, 67th in points; no health item in the profile — NBC Sports' Rotoworld v2; veto and HELD unchanged (NBA.com, NBC Sports for the absence) |
| Kawhi Leonard | the kit's 9-cat sheet and profile F6 | 15th (we 12); "is it realistic to expect both his level of play and the number of games" — NBC Sports' Rotoworld v2; HELD |
| Cam Thomas | the kit's four sheets | not in the 9-cat 200 (one of our 25 top-200 names it leaves out) — NBC Sports' Rotoworld v2; unsigned (Spotrac) |
| Jaden Ivey | the kit's four sheets | not in the 9-cat 200 (left out) — NBC Sports' Rotoworld v2; unsigned (Spotrac) |
| Jeremy Sochan | the kit's four sheets | not in the 9-cat 200 — NBC Sports' Rotoworld v2; camp deal (Blazer's Edge, Yahoo) |
| Lonzo Ball | the kit's four sheets | not in the 9-cat 200 — NBC Sports' Rotoworld v2; unsigned (Spotrac, Yahoo) |
| Rob Dillingham | the kit's four sheets | not in the 9-cat 200; dynasty 268th listed as CHI, stale — NBC Sports' Rotoworld v2; FA (Hoops Rumors, RotoBaller) |
| Bennedict Mathurin | the kit's four sheets and the recap | not in the 9-cat 200; the recap's aside "(sorry, Bennedict Mathurin)" on the Pelicans' summer — NBC Sports' Rotoworld v2; the Pelicans' first game is tonight |
| Ryan Rollins | the kit's 9-cat sheet and profile G30 | 78th (we 63; Yahoo 60); "should be a top 75 pick … a safer option just outside" — NBC Sports' Rotoworld v2; HELD, game two decides |

## Bounds

- A ranking outlet is one line of evidence; nothing here moves a pool row (F2). The
  cross-source list is a review list for WO-5, not a verdict on either side.
- The kit's numbers are last season's actuals; its "projection" content is prose and rank
  order. The 59 projection-versus-actual rows in the disagreements file flag role calls
  and stretches alike (Kessler's row is a five-game sample).
- The profiles were written in late September and the sheets edited by 10/5; §6 lists
  where that shows. Ranks on injured or moved players carry the pre-news view.
- The cross-source test uses Yahoo's 10/01 XRank, RotoBaller's 9/29 and Hashtag's 9/30
  files as they sit in the repo; the board is the 10/06 kit and the v44 deck.
- The dynasty sheet was parsed and kept but not joined under the gate; its 51 non-pool
  names are listed in the sheets file, not vetted.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-RW-1 | The 25 two-plane divergences in §3 (both planes 25+ places from every outside source, same direction): add them to the WO-5 re-derivation list, each to get a mechanism sentence or a "line stands" with the reason? No edit now | yes, WO-5 candidates; no edit now |
| D-RW-2 | Hugo Gonzalez (BOS): 180th on one outlet's 9-cat sheet, 128th dynasty, no pool row. Add a sourced row on both planes (Basketball-Reference base, [ESTIMATED]) or accept the absence? | accept the absence; add if a second outlet ranks him inside 150 |
| D-RW-3 | Dyson Daniels: the largest two-plane gap at the top of the board (9 / 11 against 53–69), driven by a 2.8-steal line against 2.0 last season. Hold for WO-5 or re-derive the steals now from the 2025-26 game log? | hold for WO-5 |
| D-RW-4 | Acuff Jr.: the kit's 143rd and "hand him the keys" line — does the owner want them counted toward D-1006-1 (b), a 32-minute reprice now? They speak to the role, which was already priced, not the rates | no change; D-1006-1's default stands |
| D-1006-1..4, D-1005-1/3/4, D-1002-1/3, D60-1..4 | carried | carried |

## Provenance and bounds

- Inputs: the owner's PDF (sha256 `0ccd0086…`, md5 `acb2e264…`, 1,894,449 bytes, 53
  pages, metadata CreationDate 2026-09-25, ModDate 2026-10-05), read with pdfplumber
  0.11.10; the committed pool and boards; the committed market files named above.
- Every number is a script's output (`rotoworld_pdf_market.py`, `third_party_market.py`,
  the scratch cross-source script over committed CSVs); gates: `check_derived.py` 15 of 15,
  `check_report.py` and the receipts check on this file (below).
- Not verified: the kit's 2025-26 lines against Basketball-Reference row by row (they are
  the outlet's transcription of last season; the pool's own bases came from
  Basketball-Reference directly).
