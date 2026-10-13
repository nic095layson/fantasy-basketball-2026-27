# After-report — 2026-10-13 (market): Yahoo's 10/13 paste as the price source (deck Version 64) and as a projection line

**Owner input (2026-10-13, verbatim):** "Yahoo stats and ADP as of today:" — followed by Yahoo's player list in its projected-stats view, copied from the owner's draft room, 300 rows. The owner then said "Proceed with Yahoo intake".

Pull window: 2026-10-13 → 2026-10-13 (owner input, WO-4; not a roster pull — the day's pull report `after-report-2026-10-13.md` stands).
Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07`, exit 0 (no kit row changed).

**What it is (parser output).** The same page shape as the 10/06 paste — name twice, a status letter on some rows, positions, team, then XRank, Yahoo's own Rank, ADP, GP and nine projected season totals — but copied from the draft room: a leading "Queue" header column with no per-row value, and thirteen "Your Turn - Nth Pick" markers at the owner's slot-10 picks (10, 15, 34, 39, 58, 63, 82, 87, 106, 111, 130, 135, 154 of a 12-team snake). 300 rows; 187 carry an ADP, 113 show "-"; status letters Q on 82 rows, O on 10, NA on 4 (Westbrook, Konchar, Valančiūnas, Batum — on no roster; assumption A2, correctable).

**Method.** The paste kept verbatim as `report/market/yahoo-raw-2026-10-13.txt` (tabs intact, 1,910 lines). `yahoo_market.py` extended in three lines — the Queue header is accepted, the turn markers are dropped before parsing, NA joins the status set — and the earlier pastes re-parse unchanged (the derived gate reproduces all 24 registered artifacts, the 9/15, 9/22, 10/01 and 10/06 Yahoo intakes among them). Transcription gate PASS (I1–I5, I6, I7): 300 parsed, XRank 1..300 with no gap; I7 resolved 297 of 300 abbreviated names to a pool row; the three Yahoo-only names (R. Westbrook, J. Valančiūnas, N. Batum) are the retired and overseas rows the kit no longer carries (the deck keeps them as `out-retired` / `out-europe`). Absence gate PASS, mechanical: 28 pool players sit outside Yahoo's 300 (Hannes Steinbach, Taylor Hendricks, Obi Toppin, Bogdan Bogdanovic, Dailyn Swain, Zuby Ejiofor, Labaron Philon, Ben Sheppard, Kris Murray, Kasparas Jakucionis, Mike Conley, Cam Whitmore, Jaden Ivey, Kobe Sanders, Sion James, Gary Trent Jr, Ebuka Okorie, Moritz Wagner, Cam Thomas, Johni Broome, Rob Dillingham, Tony Bradley, Liam McNeeley, Jeremy Sochan, Jalen Wilson, Dalton Knecht, Bronny James, Yang Hansen), none sharing surname and initial with a Yahoo-only name; the three unsigned guards and Sochan carry their standing reasons. The run was pinned to the raw's commit (`0caec15`) and registered in `check_derived.py` (24 of 24 reproduce). Price moves computed against `yahoo-2026-10-12.csv` under the deck's own loader (ADP, else XRank); the line comparison against the kit's lines over Yahoo's top 150 by XRank.

**Headline.** Yahoo's projected lines did not move: on the 249 names shared with the 10/06 paste, the per-game line and the games figure are identical on every one (0 line changes, 0 GP changes). What moved is the market — XRank changed on 217 of 249 shared names, Yahoo's own Rank on 107 by 1 to 4 places as 51 new names slotted in (the list is 300 deep again, as on 10/01) — and the deck now prices 294 of 335 rows instead of 246: 48 rows newly priced, none lost, 152 of the 246 rows priced both days change market order (mean 3.48 places, max 101: Ben Simmons, who gained an ADP of 111.1 with 15 projected games; Tre Jones lost his ADP, Yves Missi gained one). The kit's lines sit closer to Yahoo's than they did on 10/06 in 9 of 10 categories — and since Yahoo's lines are unchanged, that movement is the WO-5 and MG passes', not Yahoo's.

## 1. Roster changes

None. One team-code flag (F2, single source): Yahoo lists John Konchar at NYK with the NA letter; the pool carries him FA. No pool row changed team, entered or left; `report/projections-2026-27.csv` is byte-identical to the morning's.

## 2. What landed

- `report/market/yahoo-raw-2026-10-13.txt` — the paste, verbatim.
- `report/market/yahoo-2026-10-13.csv` — the WO-4 price file (`player,team,pos,xrank,adp`; 300 names, 187 with ADP) — the deck's F8 price source from this build on.
- `report/market/yahoo-proj-2026-10-13.csv` — the per-game line (total / GP), the totals, Yahoo's Rank, the status letters.
- `report/market/consensus-2026-10-13.csv`, `unmatched-yahoo-2026-10-13.md` (the absence gate), `disagreements-yahoo-2026-10-13.md` (A–F), `provenance.csv` (the yahoo row).
- `report/market/yahoo_market.py` — the three-line format extension; `report/check_derived.py` — the registration.

## 3. The price (WO-4) — movers and fallers against the 10/12 file

Pool rows priced: 246 on the 10/12 file → 294 on 10/13 (186 by ADP, 108 by XRank). Newly priced (48): 'Isaiah Jackson', 'Tim Hardaway Jr.', 'Aaron Wiggins', 'Donte DiVincenzo', 'Max Christie', 'Luke Kornet', 'Isaiah Joe', 'Justin Champagnie', 'Keon Ellis', 'Javonte Green', 'Luke Kennard', 'Harrison Barnes', 'Moses Moody', 'AJ Green', 'Jordan Goodwin', 'Goga Bitadze', 'Gary Payton II', 'Bruce Brown', 'Jarace Walker', 'Ron Holland', 'Sam Merrill', 'Ziaire Williams', "Ja'Kobe Walter", 'Zaccharie Risacher', 'Dominick Barlow', 'John Konchar', 'Jose Alvarado', 'Dru Smith', 'Vit Krejci', 'Jaxson Hayes', 'Jock Landale', 'Dean Wade', 'Karlo Matkovic', 'Adem Bona', 'Isaac Okoro', 'Ryan Dunn', 'Brandon Williams', 'Simone Fontecchio', 'Mouhamed Gueye', 'Quinten Post', 'Terance Mann', 'Will Richard', 'Clint Capela', 'Baylor Scheierman', 'Luka Garza', 'Jordan Walsh', 'Craig Porter Jr.', 'Caris LeVert'. Lost: none. Source switches: 3 — [('Yves Missi', 'XR', 'ADP'), ('Tre Jones', 'ADP', 'XR'), ('Ben Simmons', 'XR', 'ADP')].

Market order among the rows priced both days (the deck's Mkt rank; price = ADP, else XRank):

| direction | player | market rank 10/12 to 10/13 | price 10/12 to 10/13 |
|---|---|---|---|
| riser | Ben Simmons | 231 to 130 | 232.0 XR to 111.1 ADP |
| riser | Yves Missi | 187 to 149 | 143.0 XR to 114.9 ADP |
| riser | Jalen Smith | 227 to 192 | 228.0 XR to 165.0 XR |
| riser | Jaylen Wells | 216 to 194 | 217.0 XR to 175.0 XR |
| riser | Terrence Shannon Jr | 221 to 210 | 222.0 XR to 199.0 XR |
| riser | Jamal Shead | 236 to 226 | 238.0 XR to 225.0 XR |
| riser | Nique Clifford | 226 to 217 | 227.0 XR to 215.0 XR |
| riser | Jonathan Kuminga | 156 to 148 | 116.1 ADP to 114.8 ADP |
| riser | John Collins | 125 to 119 | 111.3 ADP to 110.4 ADP |
| riser | Keegan Murray | 155 to 150 | 116.1 ADP to 115.2 ADP |
| riser | Cam Spencer | 232 to 227 | 233.0 XR to 226.0 XR |
| riser | Darius Acuff Jr. | 112 to 108 | 108.5 ADP to 108.3 ADP |
| faller | Kentavious Caldwell-Pope | 245 to 285 | 248.0 XR to 291.0 XR |
| faller | Santi Aldama | 195 to 234 | 176.0 XR to 234.0 XR |
| faller | Tre Jones | 153 to 187 | 115.9 ADP to 138.0 XR |
| faller | Bradley Beal | 211 to 238 | 212.0 XR to 239.0 XR |
| faller | Max Strus | 210 to 228 | 209.0 XR to 228.0 XR |
| faller | Ryan Kalkbrenner | 228 to 245 | 229.0 XR to 246.0 XR |
| faller | Zach Collins | 238 to 249 | 240.0 XR to 251.0 XR |
| faller | Jay Huff | 201 to 212 | 189.0 XR to 207.0 XR |
| faller | De'Andre Hunter | 193 to 203 | 172.0 XR to 191.0 XR |
| faller | Dennis Schroder | 192 to 201 | 171.0 XR to 188.0 XR |
| faller | Daniss Jenkins | 190 to 199 | 167.0 XR to 184.0 XR |
| faller | Dereck Lively II | 189 to 198 | 166.0 XR to 183.0 XR |

Yahoo's own re-pricing (XRank vs XRank, from `disagreements-yahoo-2026-10-13.md` §F; moves of 10+ places inside 150):

| move | player | XRank 10/12 to 10/13 | ADP 10/12 to 10/13 |
|---|---|---|---|
| +30 | Kevin Porter Jr | 158 to 128 | 119 to 119 |
| +28 | Darius Acuff | 155 to 127 | 108 to 108 |
| +26 | Ty Jerome | 114 to 88 | 110 to 109 |
| +19 | Ajay Mitchell | 145 to 126 | 118 to 118 |
| +17 | Keegan Murray | 116 to 99 | 116 to 115 |
| +15 | John Collins | 112 to 97 | 111 to 110 |
| +12 | Yves Missi | 143 to 131 | — to 115 |
| +12 | Brandin Podziemski | 117 to 105 | 116 to 115 |
| +12 | Ace Bailey | 159 to 147 | 117 to 117 |
| +11 | Yaxel Lendeborg | 144 to 133 | 114 to 114 |
| +10 | Tre Jones | 148 to 138 | 116 to — |
| +10 | Sandro Mamukelashvili | 139 to 129 | 119 to 119 |
| −40 | DeMar DeRozan | 102 to 142 | 108 to 108 |
| −28 | Herb Jones | 134 to 162 | — to — |
| −21 | Nic Claxton | 89 to 110 | 94 to 95 |
| −19 | Saddiq Bey | 132 to 151 | 120 to 120 |
| −17 | Brandon Ingram | 66 to 83 | 72 to 72 |
| −17 | Myles Turner | 101 to 118 | 103 to 104 |
| −15 | Draymond Green | 137 to 152 | 107 to 107 |
| −13 | Peyton Watson | 107 to 120 | 116 to 116 |
| −12 | Egor Demin | 131 to 143 | 118 to 118 |
| −11 | Cam Johnson | 135 to 146 | 113 to 114 |
| −10 | Daniel Gafford | 120 to 130 | 123 to 123 |
| −10 | Jusuf Nurkic | 105 to 115 | 113 to 114 |

The owner's turn markers sit at XRank 9/14, 33/38, 57/62, 81/86, 105/110, 129/134 and 153 — the paste's own map of who Yahoo's order puts on the board at each of the owner's picks ([(10, 9), (15, 14), (34, 33), (39, 38), (58, 57), (63, 62), (82, 81), (87, 86), (106, 105), (111, 110), (130, 129), (135, 134), (154, 153)]).

## 4. Yahoo's projected line against the kit (the D-WO1-1 third line)

Mean absolute gap per category over Yahoo's top 150 by XRank, every row joined (150 of 150):

| comparison | FG% | FT% | 3PM | PTS | REB | AST | STL | BLK | TOV | GP |
|---|---|---|---|---|---|---|---|---|---|---|
| 10/13 paste vs the kit now (WO-5 + MG) | 0.009 | 0.013 | 0.163 | 1.325 | 0.493 | 0.352 | 0.083 | 0.059 | 0.213 | 3.44 |
| 10/06 paste vs the kit now | 0.009 | 0.012 | 0.163 | 1.299 | 0.465 | 0.341 | 0.077 | 0.059 | 0.205 | 3.273 |
| 10/06 paste vs the kit as of 10/06 (pre-WO-5) | 0.015 | 0.024 | 0.237 | 1.407 | 0.578 | 0.483 | 0.113 | 0.124 | 0.254 | 3.24 |

closer on the 10/13 paste vs the current kit than the 10/06 paste vs the 10/06 kit: 9 of 10 categories (games the one exception — the MG pass moved five games figures on the kit, and the kit's GP sits a little further from Yahoo's than it did). Yahoo's lines are the same on both pastes, so the first two rows differ only by the top-150's membership; the third row is the pre-WO-5 kit. The method moved the lines toward the evidence, not away from it (the WO-5 report said the same against Rotoworld, RotoBaller and RotoWire).

## 5. Yahoo's own Rank (the projected-line rank)

Changed by 1 to 4 places on 107 shared names and on no projection — the displacement of 51 newly listed names (the 10/06 paste was 250 deep, this one 300). No new fourth-signal reading today; the 10/06 report's §5 stands.

## 6. The status letters against the tag inventory

- **O (10):** every one is tagged on the deck — seven excluded (Nurkić, Butler, Mark Williams, Sharpe, Strus, DiVincenzo, Moody at availability 0) and three risk rows (Ingram `inj-achilles-risk`, Raynaud `inj-knee-risk` from this morning's D-1012-1, Stewart `inj-ankle-risk`). Yahoo still prices three of the excluded rows with an ADP (Nurkić 113.9, Butler 115.8, Mark Williams 109.3) and all three risk rows (Ingram 72.5, Stewart 113.0, Raynaud 117.7) — disagreements §D lists the nine rows Yahoo prices against our GP ≤ 40.
- **NA (4):** Westbrook, Valančiūnas and Batum are the deck's `out-retired` / `out-europe` rows (no kit row); Konchar is the FA row (deck untagged, kit held off the board as unsigned).
- **Q (82):** 68 untagged rows (Yahoo's questionable letter is a preseason day-to-day marker — SGA, Cunningham, Giannis, Haliburton and the rest of the rested stars carry it), 12 risk rows (Haliburton, Kessler, LeBron, Davis, Embiid, Dejounte Murray, Lillard, VanVleet, Porziņģis, Robert Williams, Beal, Gueye), one excluded (Lively) and one name not in the pool. Untagged Q rows Yahoo projects at 62 games or fewer: Caruso 58, Horford 53, Jaylin Williams 60, Middleton 53, Zach Collins 55, Ziaire Williams 38, Barlow 53, Dru Smith 60, Garza 52 — none a top-150 row; no tag moves from a Yahoo letter (tags come from injury news, two outlets).
- **Blank:** Yahoo leaves 18 of the deck's risk rows unlettered (Tatum, Curry, Murphy, Kawhi, Jackson Jr., Irving, Sarr, Edey, George, Zion, Morant, Keegan Murray, Wells, Robinson, Hunter, Smart, Simmons, Melton) — the first-season-back and chronic tags Yahoo's letter does not express.

## 7. Deck build and publish

- Pool unchanged (Version 63's bytes, sha bf0914e594b3); `hoops.py freshness --stamp --no-pool-changes` re-stamped for the re-price; the colophon's Market sentence re-authored. Gate 6 refused the first wording — its count check read "300 rows" and "48 rows" as pool counts against the 335-row pool — reworded to "names"; the second build passed.
- `build_deck.py`: planes: 315 shared · kit-only 10 · deck-only 20 · team 0 · exclusion 0 · drift 0 · propagation 0; market: yahoo-2026-10-13.csv — priced 294/335 rows (Yahoo ADP else XRank), 0 days old; built 335 players, pool bf0914e594b3, injection round-trip OK, "safe to publish"; `data/market-snapshot.csv` refreshed with the build.
- `check_parity.py`: PARITY: EXACT MATCH. `test_card.py` CARD: all 99 cases passed; `test_draft.py` all 65 cases passed; `test_gates.py` all 54 cases passed. `full_dom_check.mjs` on `draft_state_54.json`: 145 assertions, 0 failed, 0 page errors, pass true (`arena/results/full_dom_check_2026-10-13_v64.json`). `repeat_market_check.py`: 25 of 25 mocks replayed, 8 flagged (2 LINE QUESTIONED, 6 SOURCES SPLIT), 4 near misses (`arena/results/repeat_market_check_2026-10-13_v64.json`).
- Published to the standing URL after a fresh read: Version 64, id 1791911410-a85b, the standing URL (fresh read of Version 63, id 1791903783-cda0, immediately before, itself byte-verified against d9916ce at offset 349); the served file (610226 bytes) carries the built page (609862 bytes, sha256 a88d83f4e2f8) byte-for-byte inside the service's 364-byte wrapper at offset 349; manifest built 2026-10-13, market yahoo-2026-10-13.csv priced 294/335, no waiver

## 8. Gates (2026-10-13, market)

| gate | evidence |
|---|---|
| `market/yahoo_market.py 2026-10-13 --as-of 0caec15` | TRANSCRIPTION GATE PASS (I1–I7); 300 parsed, 187 with ADP, XRank gaps NONE; I7 297 of 300; JOIN 325 pool players, 297 matched, 28 accepted absences, 0 possible spelling variants; GATE PASS |
| `report/check_derived.py` | DERIVED: all 24 dated artifacts reproduce byte-for-byte from their pinned inputs (the new entry pinned at 0caec15, 5 files identical); exit 0 |
| `report/check_provenance.py` | PASS — all rows sourced; exit 0 |
| `hoops.py freshness --stamp --no-pool-changes` (deck) | 2026-10-13, the re-price asserted, no pool change |
| `scripts/build_deck.py` (deck) | refused once on gate 6 (the "rows" wording), then gates 1–7 + F8 pass, no waiver; 294/335 priced on yahoo-2026-10-13.csv, 0 days old; "safe to publish" |
| `scripts/check_parity.py` (deck) | PARITY: EXACT MATCH; exit 0 |
| `scripts/test_card.py` / `test_gates.py` / `test_draft.py` (deck) | CARD: all 99 cases passed / all 54 cases passed / all 65 cases passed; exit 0 each |
| `arena/mocks/full_dom_check.mjs` (deck) | 145 assertions, 0 failed, 0 page errors, pass true; exit 0 |
| `scripts/repeat_market_check.py` (deck) | 25 of 25 mocks replayed, 8 flagged (2 LINE QUESTIONED, 6 SOURCES SPLIT), 4 near misses; exit 0 |
| typed figures in this report vs the pinned files (`yahoo-2026-10-13/verify_literals.py`) | 53 of 53 claims PASS (three typed sentences corrected first: Yahoo's own Rank moved 1 to 4 places, not one to three; three excluded rows carry an ADP, not four; the kit has Simmons at GP 55, not 15) |
| `report/check_report.py` | REPORT GATE: PASS — after-report-2026-10-13-yahoo.md (structure, publication rule, pull-log row); exit 0 |
| `scripts/judgment_open_items.py --check-report` (deck plane) | receipts check PASS — all 10 flagged names carry a receipts row in after-report-2026-10-13-yahoo.md; exit 0 |
| `scripts/repeat_market_check.py --check-report` (deck plane) | REPEAT-NAME CHECK: PASS — after-report-2026-10-13-yahoo.md: 8 flagged name(s), each with a row (25 of 25 mocks replayed); exit 0 |
| artifact publish | Version 64, id 1791911410-a85b, the standing URL (fresh read of Version 63, id 1791903783-cda0, immediately before, itself byte-verified against d9916ce at offset 349); the served file (610226 bytes) carries the built page (609862 bytes, sha256 a88d83f4e2f8) byte-for-byte inside the service's 364-byte wrapper at offset 349; manifest built 2026-10-13, market yahoo-2026-10-13.csv priced 294/335, no waiver |

## 9. Watchlist / open items

- **The 10/14 morning lock** — this paste is the morning-before price; if a fresh paste arrives before the draft it lands the same way (the parser now takes the draft-room copy as pasted).
- **Ben Simmons** — Yahoo prices him at ADP 111.1 with 15 projected games; on the deck he is `inj-back-risk` (availability 0.78, deeply negative value), on the kit GP 55 and outside the top 200; the price is Yahoo's, the row's value is ours — no action.
- **Tre Jones** — lost his ADP on the page (keeps XRank 138; priced by XRank now); **Yves Missi** gained one (114.9).
- **The nine rows Yahoo prices against our GP ≤ 40** (disagreements §D: Mark Williams, Nurkić, Butler, Lively, Sharpe, Strus, DiVincenzo, Moody, Konchar) — exclusions stand; Yahoo's letters agree on seven of them (O).
- **Tonight's games and Kawhi's debut** — the daily pull's watchlist stands; this report adds nothing to it.

## Open-item receipts

| player | query run (2026-10-13) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (`after-report-2026-10-13.md`, receipts dated 10/13) | all HELD or unsigned on 10/13; this paste adds Yahoo's letters only — Ingram O (ADP 72.5), Porziņģis Q (ADP 104.2), Kawhi unlettered (ADP 34.2), Rollins unlettered (ADP 74.3), Mathurin unlettered (ADP 115.9), Sochan absent from the 300, the four unsigned guards absent |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 a88d83f4e2f8), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 25 of 25 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-13.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 5 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 20 of 25 | 38 | 117 | 48 | 60 | 101 | 71 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Kel'el Ware | 19 of 25 | 27 | 77 | 51 | 51 | 63 | 65 | ft_pct .732 vs .714-.723 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 19 of 25 | 62 | 180 | 56 | 118 | 126 | 129 | tpm 2.8 vs 2.2-2.6 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Lauri Markkanen | 16 of 25 | 11 | 37 | 18 | 31 | 41 | 29 | pts 26.4 vs 20.2-23.8; ast 2.1 vs 1.8-1.9; fg_pct .471 vs .452-.463 | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Jrue Holiday | 14 of 25 | 88 | 148 | 161 | 129 | 128 | 145 | pts 16.4 vs 12-12.8; reb 4.6 vs 4-4.2; ast 6.1 vs 4.4-4.6; tpm 2.6 vs 1.9-2; tov 2.8 vs 1.8-2.1; ft_pct .822 vs .855-.867 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Yaxel Lendeborg | 11 of 25 | 70 | 143 | 93 | 121 | 137 | 98 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Ryan Rollins | 9 of 25 | 28 | 74 | 58 | 63 | 78 | 83 | stl 1.7 vs 1.3-1.5 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Kawhi Leonard | 6 of 25 | 6 | 32 | 15 | 16 | 15 | 20 | pts 27.8 vs 23.7-24.3; tpm 2.6 vs 2.2-2.3 | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (21 mocks, value 7, market 18); VJ Edgecombe (12 mocks, value 56, market 75); Tyrese Maxey (7 mocks, value 4, market 9); Derrick White (6 mocks, value 30, market 45).

## Bounds

- Out of scope by design: no pool line, tag, team or placement moved (a Yahoo letter is one outlet; tags come from injury news on two); the kit's lines are the WO-5 + MG lines of this morning.
- The line-gap table joins by name on Yahoo's top 150 by XRank; the membership differs by a few names between the two pastes, so the first two rows are not a controlled pair — the third row is the controlled pre/post comparison on the same paste.
- Did not check: Yahoo's page timestamp (the paste carries none; the date is the owner's "as of today"); whether the 51 newly listed names reflect roster moves or only a deeper list (the ledger showed no pool placement change this morning).

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-1013-1 | A fresh Yahoo paste at the 10/14 lock: land it the same way (parser, pin, re-price, republish) or draft on this one? | land it if it arrives before the draft; otherwise this paste is the draft's price |
| D-1012-1 (applied), D-C2, D-SF-1..4, D-1011-4, D-MG-1..3, D-1012-2..4, D-Y1..4 and earlier | carried | carried |

## Provenance

- Inputs: the owner's paste (chat, 2026-10-13; `report/market/yahoo-raw-2026-10-13.txt`), `yahoo-2026-10-12.csv` and `yahoo-proj-2026-10-06.csv` (the comparisons), `report/projections-2026-27.csv` at the working tree and at commit fe42b70 (the pre-WO-5 kit, for the line-gap table).
- Scripts: `report/market/yahoo_market.py` (the intake, pinned at 0caec15), `report/check_derived.py`; the session's record scripts in `scratchpad yahoo1013/` (moves, line gap, paste-vs-paste, status cross-check, this writer); the deck chain `chain.sh` (`chain.log`).
- Deck results: `arena/results/full_dom_check_2026-10-13_v64.json`, `repeat_market_check_2026-10-13_v64.json`; `data/freshness.json` re-stamped; `data/market-snapshot.csv` refreshed.

## In plain language

**What this did.** Your Yahoo paste is now the price the deck reads. Every row's "Mkt" number, the survival read behind BUY NOW, and the priced-only card from round 11 all come from today's ADP and XRank: 294 of the 335 rows carry a price now, up from 246, because Yahoo's list runs 300 deep again.

**What Yahoo changed.** Nothing in its projections — every per-game line and games figure on the 249 names both pastes share is identical to last week's. It re-ranked: Ty Jerome, Kevin Porter Jr., Darius Acuff, Ajay Mitchell, Keegan Murray and John Collins up; DeRozan, Herb Jones, Claxton, Bey, Ingram and Turner down. Ben Simmons picked up an ADP around 111 on a 15-game projection, which is a Yahoo quirk, not a reason to draft him.

**What it says about our lines.** Measured against Yahoo's projections, this morning's kit sits closer than the 10/06 kit did in nine categories of ten. Yahoo did not move; we did, through the re-derivation and the minutes pass.

**The deck.** Rebuilt on the new prices and republished; every gate, the full page drive and the repeat-name check passed on the published bytes. The lines, tags and placements are unchanged from this morning.
