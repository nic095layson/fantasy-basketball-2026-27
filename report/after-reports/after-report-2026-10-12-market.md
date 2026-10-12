# After-report — 2026-10-12 (market): the Hashtag ADP of 10/12 — movers and fallers, and the deck it rebuilt

**Owner request (2026-10-12, verbatim, with the upload `Hashtag_ADP_10.12.26.pdf`):** "ADP update for you: PLease let me know movers and fallers"

Pull window: 2026-10-12 → 2026-10-12 — not a roster pull: the day's pull is `after-report-2026-10-12.md` (deck v58). This report records the 10/12 page's intake (parsed, pinned, registered), the movers and fallers against the 10/9 page (the owner's question), the price file it re-priced and the deck rebuilt on it (v59, the published page). No projection line moved; the Sunday WO-5 pass still keeps that work. Gate: `check_provenance.py` → see §5.

**Method.** The owner's upload read with pdfplumber page by page (parser output is the raw layer, `report/market/hashtag-raw-2026-10-12.txt`); two dumps byte-identical; the same registered parser as the 9/30, 10/6 and 10/9 pages; every number below is a script's output on a committed record (`work/movers.json`, `market_rank_moves_2026-10-12.json`, the refresh note); two runs of every derivation, byte-identical; nothing below is recalled.

## 1. Roster changes

None — not a pull. The pool on both planes is byte-identical to the morning's (deck pool `5e4acef794a2`, the v58 pool; kit `bdcba46ae4a5`).

## 2. The page

| item | result |
|---|---|
| the page | Hashtag "Fantasy Basketball Projections", updated 12 October 2026, Top 200, positions and ADP from Yahoo (the same settings line as 10/9, byte-identical scaffolding apart from the date); 10 pages, 238 lines, 200 projection rows, parsed by `hashtag_pdf_market.py 2026-10-12 --as-of 2f19b5d` (TRANSCRIPTION GATE PASS, GATE PASS; two runs identical); 199 of 200 names join the pool (Yanic Konan Niederhauser (LAC, R# 182) Hashtag-only) |
| ADP coverage | 169 of 200 rows carry a Yahoo ADP (10/9: 170); Tre Jones (R# 109) lost his ADP (115.9 on 10/9); no name gained one |
| names | 1 entry: Jerami Grant (MEM, R# 170, ADP 116.5); 1 exit: Maxime Raynaud (SAC, was R# 199, ADP 117.7) — the knee (D-1012-1) |
| Hashtag's lines vs 10/9 | no per-game cell moved on any of the 199 shared rows (0 stat-cell changes, 0 games changes); 22 rows' TOTAL recalculated by ±0.01 (rounding) — Sunday's outside median is unchanged |
| Hashtag's injury glyph | 64 rows flagged (10/9: 46): 31 gained the glyph (Shai Gilgeous-Alexander, Giannis Antetokounmpo, Cade Cunningham, Anthony Edwards, Kevin Durant, Tyrese Haliburton, James Harden, Devin Booker, Jalen Williams, Domantas Sabonis, Dejounte Murray, Nickeil Alexander-Walker, Matas Buzelis, LaMelo Ball, Alperen Sengün, Bam Adebayo, Michael Porter Jr., Jaden McDaniels, Jaylen Brown, De'Aaron Fox, Rudy Gobert, Day'Ron Sharpe, Ajay Mitchell, Cason Wallace, Miles Bridges, Fred VanVleet, Ayo Dosunmu, Jalen Smith, Davion Mitchell, Jared McCain, Alex Caruso); 13 lost it (Luka Doncic, Tyrese Maxey, Stephen Curry, Austin Reaves, Keegan Murray, Brandin Podziemski, Alexandre Sarr, Yaxel Lendeborg, Draymond Green, Gui Santos, CJ McCollum, Peyton Watson, De'Anthony Melton). The glyph is Hashtag's own flag, not a status read: it is cross-checked against tonight's pull, not acted on here |
| Hashtag's own R# | 37 rows moved, every one by a single place: 4 adjacent swaps (John Collins 72 to 71 with Damian Lillard 71 to 72; Rudy Gobert 77 to 76 with Deni Avdija 76 to 77; Bobby Portis 149 to 148 with Malik Monk 148 to 149; Moussa Diabaté 168 to 167 with Collin Sexton 167 to 168) and the 29 rows from R# 170 to 198 one place down after Jerami Grant's entry at 170 and Raynaud's exit at 199 |

## 3. Movers and fallers (the owner's question)

Yahoo's ADP as Hashtag compiles it, 10/9 page → 10/12 page, over the 168 names priced on both: mean move 0.48 places, median 0.30, largest 3.5; 0 of 5 or more places, 7 of 2 or more; 78 names are drafted earlier (ADP fell), 66 later (ADP rose), 24 unchanged. Three days of Yahoo drafts moved nobody more than a third of a round; the biggest movers are all late-round names, where a few drafts swing an average.

**Risers — drafted earlier (ADP fell)**

| player | 10/9 ADP | 10/12 ADP | move | Hashtag R# |
|---|---|---|---|---|
| Ty Jerome (MEM) | 113.7 | 110.2 | -3.5 | 60 to 60 |
| John Collins (DET) | 114.5 | 111.3 | -3.2 | 72 to 71 |
| Keegan Murray (SAC) | 119.0 | 116.1 | -2.9 | 94 to 94 |
| Collin Murray-Boyles (TOR) | 113.7 | 111.7 | -2.0 | 108 to 108 |
| Alexandre Sarr (WAS) | 70.3 | 68.8 | -1.5 | 112 to 112 |
| Aaron Nesmith (IND) | 111.9 | 110.4 | -1.5 | 135 to 135 |
| Brandin Podziemski (GS) | 117.3 | 115.9 | -1.4 | 111 to 111 |
| Ausar Thompson (DET) | 82.0 | 80.7 | -1.3 | 87 to 87 |
| Cameron Johnson (DEN) | 114.5 | 113.3 | -1.2 | 93 to 93 |
| Kyrie Irving (DAL) | 50.8 | 49.8 | -1.0 | 27 to 27 |
| Neemias Queta (BOS) | 117.0 | 116.0 | -1.0 | 99 to 99 |
| Cedric Coward (MEM) | 86.8 | 85.9 | -0.9 | 117 to 117 |
| Alex Caruso (OKC) | 108.7 | 107.8 | -0.9 | 190 to 191 |
| Mikel Brown Jr. (BKN) | 118.0 | 117.1 | -0.9 | 196 to 197 |
| Trey Murphy III (NO) | 37.5 | 36.7 | -0.8 | 21 to 21 |

**Fallers — drafted later (ADP rose)**

| player | 10/9 ADP | 10/12 ADP | move | Hashtag R# |
|---|---|---|---|---|
| Nicolas Claxton (CHI) | 91.5 | 94.5 | +3.0 | 124 to 124 |
| Brandon Ingram (LAC) | 69.2 | 71.8 | +2.6 | 82 to 82 |
| Myles Turner (MIL) | 101.1 | 103.1 | +2.0 | 95 to 95 |
| Jusuf Nurkic (UTA) | 111.9 | 113.4 | +1.5 | 134 to 134 |
| Kristaps Porzingis (GS) | 102.7 | 103.8 | +1.1 | 96 to 96 |
| Toumani Camara (POR) | 111.6 | 112.7 | +1.1 | 125 to 125 |
| DeMar DeRozan (DEN) | 107.0 | 108.1 | +1.1 | 130 to 130 |
| Michael Porter Jr. (BKN) | 61.2 | 62.2 | +1.0 | 62 to 62 |
| Coby White (CHA) | 89.2 | 90.2 | +1.0 | 86 to 86 |
| Kon Knueppel (CHA) | 48.9 | 49.8 | +0.9 | 57 to 57 |
| Naz Reid (CHA) | 63.1 | 64.0 | +0.9 | 74 to 74 |
| Donovan Clingan (POR) | 42.7 | 43.5 | +0.8 | 58 to 58 |
| Jarrett Allen (CLE) | 69.3 | 70.1 | +0.8 | 80 to 80 |
| Ajay Mitchell (OKC) | 117.2 | 118.0 | +0.8 | 89 to 89 |
| Miles Bridges (PHO) | 99.3 | 100.1 | +0.8 | 107 to 107 |

**The names on the owner's sheet and the standing checks**

| player | 10/9 ADP | 10/12 ADP | move | Hashtag R# | the decision or check he sits under |
|---|---|---|---|---|---|
| Zach LaVine (SAC) | 101.2 | 101.8 | +0.6 | 68 to 68 | the owner's 10/11 note (D-1011-1, judgment −0.10) |
| De'Aaron Fox (SA) | 80.0 | 80.1 | +0.1 | 70 to 70 | the owner's 10/11 call (D-1011-3, judgment −0.10); Hashtag's injury glyph on since 10/12 |
| Yaxel Lendeborg (GS) | 115.1 | 114.5 | -0.6 | 121 to 121 | the owner's 10/11 note (D-1011-2 c, judgment +0.10); Hashtag's injury glyph off since 10/12 |
| Darius Acuff Jr. (SAC) | 108.9 | 108.5 | -0.4 | 197 to 198 | the owner's 10/11 note (unchanged, D-1011-2) |
| Ryan Rollins (MIL) | 75.3 | 74.5 | -0.8 | 63 to 63 | WO-5 (started at PG 10/11) |
| Dyson Daniels (ATL) | 65.0 | 65.2 | +0.2 | 64 to 64 | WO-5 (steals) |
| Cooper Flagg (DAL) | 10.3 | 10.2 | -0.1 | 17 to 17 | WO-5 (D-RN-2) |
| P.J. Washington (DAL) | 116.4 | 116.5 | +0.1 | 144 to 144 | LINE QUESTIONED (D-RN-1) |
| Daniel Gafford (DAL) | 123.5 | 123.0 | -0.5 | 180 to 181 | LINE QUESTIONED (D-RN-1) |
| Devin Vassell (SA) | 114.8 | 114.1 | -0.7 | 131 to 131 | LINE QUESTIONED (D-RN-1) |
| Stephon Castle (SA) | 53.9 | 54.0 | +0.1 | 151 to 151 | D-CAST-2 second step |
| RJ Barrett (TOR) | 112.3 | 112.4 | +0.1 | 153 to 153 | D-CAST-2 second step |
| Kawhi Leonard (TOR) | 33.7 | 34.2 | +0.5 | 16 to 16 | judgment card (10/13 vs NYK the first chance) |
| Kristaps Porzingis (GS) | 102.7 | 103.8 | +1.1 | 96 to 96 | DO NOT DRAFT (veto) |
| Brandon Ingram (LAC) | 69.2 | 71.8 | +2.6 | 82 to 82 | judgment card (Achilles, HELD) |
| Isaiah Stewart (MEM) | 113.2 | 113.2 | +0.0 | 159 to 159 | D-1010-2 (inj-ankle-risk) |
| Herbert Jones (NO) | — | — | no Yahoo ADP on either page (R# 169) | 169 to 169 | LINE QUESTIONED (D-RN-1) |
| Bennedict Mathurin (NO) | — | — | not on either page's top 200 (keeps the 10/6 paste's ADP in the price file) | — | WO-5 |
| Maxime Raynaud (SAC) | 117.7 | — | off the 10/12 page (was R# 199) | 199 to none | D-1012-1 (knee; keeps the 10/9 ADP in the price file) |

## 4. The price file and the deck it rebuilt

| item | result |
|---|---|
| the price file | `yahoo-2026-10-12.csv` by `report/market/adp_refresh.py 2026-10-12 --as-of 3979017` (registered; derived gate 23 of 23): the 10/9 file's 250 rows with 169 ADPs replaced from the page, 81 keeping the 10/9 ADP (outside the page's top 200, or on it without an ADP — Tre Jones; or off the page — Raynaud), 0 appended, XRank unchanged; two runs byte-identical |
| moves in the file | among the 169 re-priced rows: mean move 0.48 places, largest 3.5; 0 of 5 or more (`adp-refresh-2026-10-12.md` lists the fifteen largest) |
| the deck | rebuilt on the new file (`build_deck.py`, gates 1–7, no waiver, pool identical to v58): priced 246 of 335 (184 by ADP, 62 by XRank — unchanged), 0 days old; prices changed on 142 rows, market-rank order changed for 112 of the 246 priced rows; largest shift 16 places (John Collins 140 to 124; Keegan Murray 168 to 152; Ty Jerome 133 to 117); 90 of the moves are three places or fewer; the unpriced tail's order unchanged; 6 priced names sit off the board (availability 0: Dereck Lively II, Jimmy Butler, Jusuf Nurkic, Mark Williams, Max Strus, Shaedon Sharpe); no pool row, line or placement changed; the colophon's market sentence names the 10/12 ADP; freshness restamped `--no-pool-changes` (`arena/results/market_rank_moves_2026-10-12.json`) |
| shift histogram | 1 place: 51, 2 places: 25, 3 places: 14, 4 places: 11, 5 places: 4, 7 places: 2, 8 places: 1, 11 places: 1, 16 places: 3 |

## 5. Gates (2026-10-12, market)

| gate | result |
|---|---|
| kit `report/check_derived.py` | DERIVED: all 23 dated artifacts reproduce byte-for-byte from their pinned inputs (the two new ones at pins 2f19b5d and 3979017); exit 0 |
| kit `report/check_provenance.py` | PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07; exit 0 |
| deck `scripts/build_deck.py` | gates 1–7 + F8 pass, no waiver; market `yahoo-2026-10-12.csv` priced 246/335, 0 days old; pool `5e4acef794a2` identical to v58; freshness restamped `--no-pool-changes`; injection round-trip OK; "safe to publish" |
| deck `scripts/check_parity.py` | PARITY: EXACT MATCH — 390 owner turns across 30 committed states; market ranks 318 (priced 240); exit 0 |
| deck `test_card.py` / `test_gates.py` / `test_draft.py` | CARD: all 99 cases passed; all 54 cases passed; all 65 cases passed; exit 0/0/0 |
| deck `arena/mocks/full_dom_check.mjs` | 143 assertions, 0 failed, 0 page errors, pass true (`arena/results/full_dom_check_2026-10-12_v59.json`) |
| deck `scripts/repeat_market_check.py` | 23 of 23 mocks replayed on the v59 page, 14 flagged (4 LINE QUESTIONED, 10 SOURCES SPLIT), 5 near misses (`arena/results/repeat_market_check_2026-10-12_v59.json`); the card's 🎯 at 299 of 299 owner turns identical to the v58 replay (`repeat_market_check_2026-10-12.json`); flagged names whose market rank moved: 9 (PJ Washington 151 to 155, Payton Pritchard 83 to 85, OG Anunoby 65 to 64, Daniel Gafford 181 to 180, Yaxel Lendeborg 144 to 141, Zach LaVine 100 to 99, Devin Vassell 142 to 138, Josh Hart 96 to 95, Saddiq Bey 176 to 175) |
| kit `report/check_report.py` | REPORT GATE: PASS — after-report-2026-10-12-market.md (structure, publication rule, pull-log row); exit 0 |
| deck `judgment_open_items.py --check-report` | receipts check PASS — all 10 flagged names carry a receipts row in after-report-2026-10-12-market.md; exit 0 |
| deck `repeat_market_check.py --check-report` | REPEAT-NAME CHECK: PASS — after-report-2026-10-12-market.md: 14 flagged name(s), each with a row (23 of 23 mocks replayed); exit 0 |
| artifact publish | Version 59, id 1791824190-04c2, the standing URL; the served file carries the built page byte-for-byte inside the service's 364-byte wrapper; manifest built 2026-10-12; the live version read before publishing was 1791818861-878d (v58) (the page's sha256 ca032b2697c5) |

## 6. Watchlist / open items

- **10/14 lock** — the owner's fresh Yahoo paste replaces `yahoo-2026-10-12.csv` as the price file (WO-4, D-1009-8); until then this file stands (D-1012-2 below).
- **WO-5, the owed projection pass** — still owed before Wednesday's draft (Acuff, Lendeborg, Mathurin, Rollins, Daniels' steals, Flagg, the LINE QUESTIONED names, Castle/Barrett's second step); the 10/12 page's lines are the same as 10/9's, so the outside median is unchanged.
- **Hashtag's glyph set as a cross-check for tonight's pull** — the 31 names that gained the glyph include men playing tonight (Fox at Utah) and men the feed lists day-to-day; the pull reads the feed and the box scores, not the glyph.
- **D-1012-1** (Raynaud: deck `inj-knee-risk`, kit GP 72 → 66) applies at the next pull if silent; D-1011-4 open (default (b)); D-1010-2 re-check ~10/22–23.

## Open-item receipts

| player | query run (2026-10-12) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (`after-report-2026-10-12.md`, receipts dated 10/12) | all HELD or unsigned on 2026-10-12; this report did no roster research |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 ca032b2697c5), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 23 of 23 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-12.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-06.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 5 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| PJ Washington | 19 of 23 | 87 | 155 | 178 | 144 | 141 | 121 | ast 2.4 vs 1.9-2; tov 1.5 vs 1.7-1.8; fg_pct .470 vs .448-.451; ft_pct .750 vs .698-.703 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Payton Pritchard | 18 of 23 | 37 | 85 | 33 | 90 | 92 | 72 | stl 1 vs 0.7-0.8; tpm 3.8 vs 3-3.2; tov 2 vs 1.3-1.3; ft_pct .850 vs .873-.875 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 17 of 23 | 28 | 64 | 60 | 56 | 43 | 44 | pts 18.5 vs 16.4-17; ast 2.3 vs 2.1-2.1; ft_pct .805 vs .813-.819 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Sandro Mamukelashvili | 17 of 23 | 81 | 169 | 138 | 105 | 153 | 120 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Daniel Gafford | 11 of 23 | 90 | 180 | 188 | 181 | 161 | 155 | pts 10.5 vs 9.1-9.8; reb 7.5 vs 5.8-6.5; ast 1.5 vs 1.1-1.2; blk 1.7 vs 1.2-1.4; fg_pct .700 vs .648-.689; ft_pct .700 vs .671-.687 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Jalen Suggs | 11 of 23 | 59 | 105 | 89 | 54 | 84 | 99 | pts 17 vs 14.1-15.1; ast 4 vs 4.8-5 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 10 of 23 | 82 | 141 | 94 | 121 | 137 | 98 | reb 7.5 vs 5.5-6.9; tpm 0.9 vs 1.2-1.3; fg_pct .520 vs .447-.498; ft_pct .740 vs .765-.828 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Isaiah Hartenstein | 7 of 23 | 75 | 104 | 141 | 92 | 100 | 102 | pts 11.5 vs 9.1-10.5; reb 11 vs 9.2-10.3; fg_pct .585 vs .597-.611; ft_pct .680 vs .642-.656 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Zach LaVine | 7 of 23 | 56 | 99 | 162 | 68 | 77 | 118 | pts 22.5 vs 17-21.1; reb 4.5 vs 3.1-3.6; ast 4 vs 2.8-3.4; tov 2.6 vs 2-2.4 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 5 of 23 | 89 | 138 | 122 | 131 | 125 | 123 | pts 16.8 vs 13.4-15.1; tov 1.5 vs 1-1.2; fg_pct .465 vs .432-.443 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Dyson Daniels | 5 of 23 | 11 | 62 | 20 | 64 | 56 | 53 | pts 14.5 vs 11.3-11.8; stl 3 vs 2-2.4; tpm 1.1 vs 0.5-0.6; fg_pct .495 vs .501-.513 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Herbert Jones | 5 of 23 | 74 | 182 | 147 | 169 | 134 | >250 | — | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Josh Hart | 5 of 23 | 67 | 95 | 68 | 84 | 91 | 94 | pts 13.5 vs 11.9-12.2; tpm 1 vs 1.2-1.5; fg_pct .520 vs .498-.503; ft_pct .780 vs .751-.759 | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Saddiq Bey | 5 of 23 | 95 | 175 | 109 | 132 | 169 | 143 | blk 0.4 vs 0.1-0.1; tpm 2.4 vs 1.8-2; tov 1.5 vs 0.8-0.9 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Karl-Anthony Towns (18 mocks, value 6, market 15); Jalen Williams (15 mocks, value 16, market 40); Derrick White (12 mocks, value 24, market 45); Jalen Johnson (6 mocks, value 13, market 11); Mikal Bridges (6 mocks, value 61, market 84).

## Bounds

- The 10/12 ADP is Yahoo's as compiled by Hashtag (the owner's 10/9 verification, assumed to hold for the same page three days later — assumption A1); the page's settings line is byte-identical to 10/9's.
- 81 of the 250 priced names keep an older ADP (79 outside the page's top 200 from the 10/6 paste via 10/9, Tre Jones and Raynaud from 10/9).
- 'Movers and fallers' is read as ADP movement between the two pages (assumption A2); Hashtag's own R# moved nobody more than one place, so the ranking view carries no separate story.
- The movers are measured against the 10/9 page, three days of drafts; against the 10/6 paste the drift is the 10/9 report's drift plus today's.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-1012-2 | the price file until the lock: (a) `yahoo-2026-10-12.csv` (the 10/9 file re-priced from the 10/12 page) stands until the owner's 10/14 Yahoo paste, which replaces it (D-1009-8 carried to the newer page); (b) revert to `yahoo-2026-10-09.csv` | (a) |
| D-1012-1, D-1011-4, D-1011-1..3, D-1010-2, D-1010-1, D-RN-6, D73-1, D72-1, D71-1, D70-1, D69-1, D68-1..3, D61-4, D-RN-1..5, D67-1..6, D66-1, D-V4-1, D-CAST-1..4, D62-1..3, D-1008-1..3, D-1009-1..13 and earlier | carried | carried |

## Provenance and bounds

- Inputs: the owner's `Hashtag_ADP_10.12.26.pdf` (sha256 f3fb7d4146d2f92e…, raw layer `report/market/hashtag-raw-2026-10-12.txt`, pinned at 2f19b5d); `report/market/hashtag-2026-10-09.csv` and `yahoo-2026-10-09.csv` (the comparison and the base); the deck's `data/players.csv` (unchanged) and `data/market-snapshot.csv` before and after the build.
- Records: `report/market/hashtag-2026-10-12.csv`, `unmatched-hashtag-2026-10-12.md` (pin 2f19b5d), `yahoo-2026-10-12.csv`, `adp-refresh-2026-10-12.md` (pin 3979017); the deck's `arena/results/market_rank_moves_2026-10-12.json`, `full_dom_check_2026-10-12_v59.json`, `repeat_market_check_2026-10-12_v59.json`; the movers record `scratchpad adp1012/work/movers.json` (the parser's rows joined to the 10/9 CSV by the kit's name rules).
- Scripts: `report/market/hashtag_pdf_market.py`, `report/market/adp_refresh.py` (both registered), `scratchpad adp1012/work/movers.py` (the movers record), `work/market_moves.py` (the market-rank twin, `arena.market_ranks` over the two snapshots as `check_parity.py` item 6), `chain.sh` (the deck chain; `chain.log`), `write_report.py` (this file).
- Every number in §2, §3 and §4 is a script's output; every gate line is the command's own output.

## In plain language

**What you asked.** Who moved up and who moved down in Yahoo's ADP since the last Hashtag page (10/9), and the page taken into the system.

**The short answer.** Almost nobody moved much. Across the 168 players priced on both pages the average move is half a place, and the largest is three and a half places. Nobody moved five places or more. 78 players are being drafted a little earlier, 66 a little later, 24 exactly the same.

**Risers (drafted earlier).** Ty Jerome 113.7 to 110.2 (-3.5); John Collins 114.5 to 111.3 (-3.2); Keegan Murray 119.0 to 116.1 (-2.9); Collin Murray-Boyles 113.7 to 111.7 (-2.0); Alexandre Sarr 70.3 to 68.8 (-1.5); Aaron Nesmith 111.9 to 110.4 (-1.5); Brandin Podziemski 117.3 to 115.9 (-1.4); Ausar Thompson 82.0 to 80.7 (-1.3). Mostly late-round names, where a few drafts move the average; Irving and Murphy are the two inside the top 50.

**Fallers (drafted later).** Nicolas Claxton 91.5 to 94.5 (+3.0); Brandon Ingram 69.2 to 71.8 (+2.6); Myles Turner 101.1 to 103.1 (+2.0); Jusuf Nurkic 111.9 to 113.4 (+1.5); Kristaps Porzingis 102.7 to 103.8 (+1.1); Toumani Camara 111.6 to 112.7 (+1.1); DeMar DeRozan 107.0 to 108.1 (+1.1); Michael Porter Jr. 61.2 to 62.2 (+1.0). Every one of them a move of three places or fewer; Ingram and Porziņģis keep sliding on their injuries.

**Your names.** Zach LaVine 101.2 to 101.8 (+0.6); De'Aaron Fox 80.0 to 80.1 (+0.1); Yaxel Lendeborg 115.1 to 114.5 (-0.6); Darius Acuff Jr. 108.9 to 108.5 (-0.4); Ryan Rollins 75.3 to 74.5 (-0.8); Cooper Flagg 10.3 to 10.2 (-0.1). Nothing there changes where any of them sits on the card.

**Two names left and entered.** Maxime Raynaud dropped off the top 200 (the kneecap, D-1012-1 on your sheet); Jerami Grant came on at 170. Tre Jones lost his ADP on the page (keeps his 10/9 price in our file). Hashtag's injury glyph switched on for 31 players and off for 13 — that is Hashtag's own flag, read as a cross-check for tonight's pull, not as news.

**What changed on the deck.** The board was rebuilt on the new prices and republished as v59. The projections, tiers and the card's recommendations are untouched; only the market column moved, by a place or two for most priced players and by at most 16 places for three late-round names (Collins, Keegan Murray, Jerome). The one assumption is the same as on 10/9: that Hashtag's ADP column is Yahoo's current ADP, as you verified then.

**Verification.** The page was parsed by the same registered script as the 9/30, 10/6 and 10/9 pages (two runs identical), both new price artifacts carry commit pins and reproduce byte-for-byte (derived gate 23 of 23), the re-priced deck passed the full chain (parity exact at 390 owner turns across 30 committed states, 99/54/65 cases, 143 browser assertions, the 23-mock replay with the card's pick compared turn by turn against the v58 replay), and it was published after a fresh read of the live version.

**Your decision.** D-1012-2: this price file stands until your 10/14 Yahoo paste replaces it (default yes). Wednesday morning's paste is still the one that matters.
