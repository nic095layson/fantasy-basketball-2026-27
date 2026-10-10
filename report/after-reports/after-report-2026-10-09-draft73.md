# After-report — draft_73: the thirteenth live-human room from the real slot 10, the first on deck v54 — the card followed at 6 of 13 turns

**Owner request (2026-10-09, verbatim):** "Live mock draft for your review, I am very impressed with this round. Please let me know your analysis:" — the deck tool's pick-by-pick feed (LIVE mode) and Yahoo's recap, pasted after the research pass published v54. Graded as mock 73, the standing live-room protocol.

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (random humans — a practice rep, not opponent intel; display names 1 sean, 2 Elliot, 3 selvin, 4 Cheater, 5 Herro ball, 6 Jeff, 7 Gundy, 8 Mark, 9 Angelbert, 10 David, 11 Nikes, 12 David Mandem are not the league's). **Deck used:** v54 (rev `03cba0a`, live at the standing URL since 20:29 UTC; the research-pass notes and the Macao box score over v53; engine, values, prices and pool identical to v53; Porziņģis veto live). The page's own echo code re-emitted the owner's 7 "off the card" lines identically in the replay (#34 Davis rank 2, 0.002 behind Chet Holmgren; #58 Daniels rank 2, 0.000 behind OG Anunoby; #63 Anunoby rank 2, 0.002 behind Payton Pritchard; #87 Harper rank 59, 0.246 behind Josh Hart; #111 Gordon rank 2, 0.010 behind Sandro Mamukelashvili; #130 Mamukelashvili rank 2, 0.000 behind PJ Washington; #154 Eason rank 9, 0.057 behind Christian Braun); v53 would replay the same, so v54 is graded as the version live when the room ran (A1). **Method:** the recap resolved to pool names by the tracker's own resolver (`hoops.py draft resync`, 156 of 156); the tool log replayed through the real page in headless Chromium and reconciled against the recap; the grade is the deck plane's machine-derived retro (`arena/results/m73_*.json`, debrief `debrief_2026-10-09_mock73_slot10.md`; title odds on the league's real eight-team bracket). Every figure below is read from those files. Verification: this file passes `report/check_report.py` and the deck's `judgment_open_items.py --check-report` and `repeat_market_check.py --check-report`.

Pull window: 2026-10-09 → 2026-10-09 (analysis only, the eighth report of the day; no roster pull).

**Headline.** As drafted **34.17 percent** on the real bracket (rank 1 of 12), expected weekly category wins 5.498, rank 1 of 12 (next 5.080), favored in 11 of 11 head-to-heads; the card's 🎯 taken at 6 of 13 turns, a Top-5 row at 11 of 13 (off the card: #34 Anthony Davis (card #2), #58 Dyson Daniels (card #2), #63 OG Anunoby (card #2), #87 Dylan Harper (card #59), #111 Aaron Gordon (card #2), #130 Sandro Mamukelashvili (card #2), #154 Tari Eason (card #9)); the self-consistent follow-card chain from the same seat grades 40.44 percent. Category shape: 3PTM, ST, TO in the top three of the weekly model, AST ninth or lower. Hindsight's best single swap is Immanuel Quickley at #87 (+0.131 a week). The tool log (159 events, one halt, one undo) replayed on the real page with zero drift; positions matched the pool on 156 of 156 picks.

## 1. Roster changes

None — a public practice room; no pull, no row moved on either plane.

## 2. The team, replayed

| arm | ECW (rank; next) | favored | title odds (rank) |
|---|---|---|---|
| as drafted (the card's 🎯 at 6 of 13 turns) | 5.498 (rank 1; next 5.080) | 11 of 11 | 34.17% (rank 1) |
| follow-card, self-consistent (arms stage) | 5.690 (rank 1; next 5.082) | 11 of 11 | 40.44% (rank 1) |
| 🎯 at #34: Chet Holmgren for Anthony Davis (card #2; Chet Holmgren went #36) | 5.511 (rank 1; next 5.083) | 11 of 11 | 35.43% (rank 1) |
| 🎯 at #58: OG Anunoby for Dyson Daniels (card #2; OG Anunoby went #63) | 5.498 (rank 1; next 5.080) | 11 of 11 | 34.17% (rank 1) |
| 🎯 at #63: Payton Pritchard for OG Anunoby (card #2; Payton Pritchard went #82) | 5.498 (rank 1; next 5.080) | 11 of 11 | 34.17% (rank 1) |
| 🎯 at #87: Josh Hart for Dylan Harper (card #59; Josh Hart went #88) | 5.624 (rank 1; next 5.073) | 11 of 11 | 38.67% (rank 1) |
| 🎯 at #111: Sandro Mamukelashvili for Aaron Gordon (card #2; Sandro Mamukelashvili went #130) | 5.498 (rank 1; next 5.080) | 11 of 11 | 34.17% (rank 1) |
| 🎯 at #130: PJ Washington for Sandro Mamukelashvili (card #2; PJ Washington went #135) | 5.498 (rank 1; next 5.080) | 11 of 11 | 34.17% (rank 1) |
| 🎯 at #154: Christian Braun for Tari Eason (card #9; Christian Braun went undrafted) | 5.547 (rank 1; next 5.078) | 11 of 11 | 34.84% (rank 1) |
| hindsight single swap Chet Holmgren at #34 | 5.511 (rank 1; next 5.083) | 11 of 11 | 35.43% (rank 1) |
| hindsight single swap Tyler Herro at #58 | 5.504 (rank 1; next 5.081) | 11 of 11 | 31.82% (rank 1) |
| hindsight single swap Immanuel Quickley at #87 | 5.628 (rank 1; next 4.932) | 11 of 11 | 37.78% (rank 1) |
| hindsight single swap Myles Turner at #106 | 5.502 (rank 1; next 5.084) | 11 of 11 | 35.11% (rank 1) |
| hindsight single swap Myles Turner at #111 | 5.499 (rank 1; next 5.072) | 11 of 11 | 36.25% (rank 1) |
| hindsight single swap Kyle Filipowski at #135 | 5.503 (rank 1; next 5.078) | 11 of 11 | 33.69% (rank 1) |
| hindsight single swap Kyle Filipowski at #154 | 5.583 (rank 1; next 5.071) | 11 of 11 | 36.21% (rank 1) |

Category ranks (weekly model): FG% 5 · FT% 6 · 3PTM 2 · PTS 7 · REB 4 · AST 11 · ST 1 · BLK 4 · TO 1.

## 3. Pick by pick — card vs owner vs hindsight

| pick | deck 🎯 (Top-5) | owner took | card rank · gap (blend) | hindsight best single swap (ΔECW vs final rosters) |
|---|---|---|---|---|
| #10 | Karl-Anthony Towns (Karl-Anthony Towns, Jalen Johnson, Tyrese Haliburton, Anthony Davis, Chet Holmgren) | Karl-Anthony Towns | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #15 | Donovan Mitchell (Donovan Mitchell, Jalen Williams, Jamal Murray, Derrick White, Kevin Durant) | Donovan Mitchell | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #34 | Chet Holmgren (Chet Holmgren, Anthony Davis, Derrick White, Dyson Daniels, OG Anunoby) | Anthony Davis | #2 · +0.002 | Chet Holmgren +0.014 |
| #39 | Derrick White (Derrick White, Desmond Bane, OG Anunoby, Kyrie Irving, Dyson Daniels) | Derrick White | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #58 | OG Anunoby (OG Anunoby, Dyson Daniels, Onyeka Okongwu, Payton Pritchard, Darius Garland) | Dyson Daniels | #2 · +0.000 | Tyler Herro +0.007 |
| #63 | Payton Pritchard (Payton Pritchard, OG Anunoby, Darius Garland, De'Aaron Fox, Coby White) | OG Anunoby | #2 · +0.002 | none positive (the pick was hindsight-best) |
| #82 | Payton Pritchard (Payton Pritchard, Coby White, Josh Hart, Isaiah Hartenstein, Jalen Suggs) | Payton Pritchard | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #87 | Josh Hart (Josh Hart, Isaiah Hartenstein, Yaxel Lendeborg, Sandro Mamukelashvili, Jalen Suggs) | Dylan Harper | #59 · +0.246 | Immanuel Quickley +0.131 |
| #106 | Yaxel Lendeborg (Yaxel Lendeborg, Myles Turner, Sandro Mamukelashvili, PJ Washington, Daniel Gafford) | Yaxel Lendeborg | #1 · +0.000 | Myles Turner +0.004 |
| #111 | Sandro Mamukelashvili (Sandro Mamukelashvili, Aaron Gordon, PJ Washington, Myles Turner, Saddiq Bey) | Aaron Gordon | #2 · +0.010 | Myles Turner +0.001 |
| #130 | PJ Washington (PJ Washington, Sandro Mamukelashvili, Saddiq Bey, Cason Wallace, Devin Vassell) | Sandro Mamukelashvili | #2 · +0.000 | none positive (the pick was hindsight-best) |
| #135 | PJ Washington (PJ Washington, Saddiq Bey, Christian Braun, Devin Vassell, Draymond Green) | PJ Washington | #1 · +0.000 | Kyle Filipowski +0.005 |
| #154 | Christian Braun (Christian Braun, Draymond Green, Cameron Johnson, Kyle Filipowski, Herbert Jones) | Tari Eason | #9 · +0.057 | Kyle Filipowski +0.086 |

[EVIDENCE: `m73_replay.json`, `m73_deckcard_v53.json`, `m73_hindsight.json`; card ranks are the deck's own JS replayed on the v54 page; the live echoes at #34 (0.002 behind Holmgren, rank #2), #58 (0.000 behind Anunoby, rank #2), #63 (0.002 behind Pritchard, rank #2), #87 (0.246 behind Hart, rank #59), #111 (0.010 behind Mamukelashvili, rank #2), #130 (0.000 behind Washington, rank #2), #154 (0.057 behind Braun, rank #9) match the replay]

Advice line (page reading): silent at every turn.

## 4. Tool-state integrity — the deck's board vs the recap, on the v54 page

| check | result |
|---|---|
| picks differing from the recap | **0 of 156**; owner's roster identical; nothing missing, nothing extra |
| events replayed | 159 (158 feeds incl. 19 shared-token feeds resolved by the 'assumed over' / 'only X left' / 'skipped' rule and 2 heads-up feeds; 1 halt; 1 undo; 0 inserts; 0 UNKNOWN feeds) |
| the halt | the feed "Jalen" after pick #30 halted on Jalen Johnson (already drafted) with the fuller-name hint (Jalen Williams, Jalen Duren, Jalen Green); the owner resent the full name and the log continued with nothing lost |
| the undo | Aaron Gordon at #111 was logged to seat 11, undone, Collin Gillespie logged there instead, and Gordon then taken by the owner at the next pick — the room's order per the recap |
| the page's own off-card echoes | re-emitted at #34, #58, #63, #87, #111, #130, #154 identical to the owner's paste (rank, three-decimal gap, 🎯) |
| echo lines asserted / clock text / page errors | 159 of 159 / 0 mismatches / 0 errors |

[EVIDENCE: `arena/results/m73_tool_vs_truth.json`, `arena/data/events/m73_tool_events.json`; harness `live_replay_dom.mjs` on `page_v54.html`]

## 5. Survival chips

Survival (`m73_survival.json`): this room 49 rows, predicted 0.474 vs realized 0.612, Brier 0.193; BUY NOW 2 of 9 survived, TOSS-UP 7 of 13, quiet 21 of 27. Pooled 51–73: 1167 rows, Brier 0.237.

Target-wait (`target_wait_2026-10-09b.json`, mocks 56–73): deep (mkt − pick ≥ 24) — 🎯s passed on 45, still there at the next owner turn 29, at the turn after 8 of 40; mid (12–23) — 🎯s passed on 13, still there at the next owner turn 5, at the turn after 1 of 12; near (< 12) — 🎯s passed on 27, still there at the next owner turn 9, at the turn after 0 of 26.

## 6. The draft room's positions vs the pool

0 of 156 positions differ, teams 0 of 156 [EVIDENCE: `scratchpad m73/positions_check.json`; the recap as pasted].

## 7. Where this human room took the preseason standouts

The standing comparison. These humans could see the box scores; the cast rooms could not. The deck rank is the v52–v54 board (identical values), the ADP the 10/09 Yahoo file (Hashtag's column).

| player | deck rank (v52–v54) | Yahoo ADP 10/09 | this room (humans) | mock 72, cast, 10/09 | mock 68, public, 10/08 |
|---|---|---|---|---|---|
| Yaxel Lendeborg | 82 | 115.1 | #106 (David) | #106 (you) | #127 |
| Ty Jerome | 101 | 113.7 | #83 (Nikes) | #118 | #82 (you) |
| Sandro Mamukelashvili | 81 | 119.1 | #130 (David) | #154 (you) | #133 |
| Ryan Rollins | 70 | 75.3 | #69 (Cheater) | #70 | #67 |
| Darryn Peterson | 140 | 103.3 | #97 (sean) | #105 | #111 (you) |
| Kel'el Ware | 80 | 76.0 | #64 (Angelbert) | #85 | #65 |
| Cameron Boozer | 48 | 55.4 | #71 (Elliot) | #49 | #61 |
| Aday Mara | 315 | 107.7 | undrafted | undrafted | undrafted |
| Jalen Williams | 16 | 40.2 | #31 (Gundy) | #29 | #39 (you) |
| Tyrese Haliburton | 7 | 13.8 | #12 (David Mandem) | #8 | #9 |
| Damian Lillard | 88 | 69.1 | #55 (Gundy) | #76 | #56 |
| Deni Avdija | 77 | 40.8 | #50 (Elliot) | #63 (you) | #40 |

Late card: 0 unpriced rows across the owner's three turns in rounds 11–13. Repeat-name audit (`m73_repeat_names_audit.json`): the #1 changes at 12 of 13 turns under other rooms' rosters (10 of 13 against an empty roster); Gafford on the Top-5 at 1, Braun 2, Poeltl 0.

## 8. Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 a771018d8dd3), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 23 of 23 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-09.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-06.csv`, `hashtag-2026-10-09.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| PJ Washington | 19 of 23 | 87 | 151 | 178 | 144 | 141 | 121 | ast 2.4 vs 1.9-2; tov 1.5 vs 1.7-1.8; fg_pct .470 vs .448-.451; ft_pct .750 vs .698-.703 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Payton Pritchard | 18 of 23 | 37 | 83 | 33 | 90 | 92 | 72 | stl 1 vs 0.7-0.8; tpm 3.8 vs 3-3.2; tov 2 vs 1.3-1.3; ft_pct .850 vs .873-.875 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 17 of 23 | 28 | 65 | 60 | 56 | 43 | 44 | pts 18.5 vs 16.4-17; ast 2.3 vs 2.1-2.1; ft_pct .805 vs .813-.819 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Sandro Mamukelashvili | 17 of 23 | 81 | 169 | 138 | 105 | 153 | 120 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Daniel Gafford | 11 of 23 | 90 | 181 | 188 | 180 | 161 | 155 | pts 10.5 vs 9.1-9.8; reb 7.5 vs 5.8-6.5; ast 1.5 vs 1.1-1.2; blk 1.7 vs 1.2-1.4; fg_pct .700 vs .648-.689; ft_pct .700 vs .671-.687 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Jalen Suggs | 11 of 23 | 59 | 105 | 89 | 54 | 84 | 99 | pts 17 vs 14.1-15.1; ast 4 vs 4.8-5 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 10 of 23 | 82 | 144 | 94 | 121 | 137 | 98 | reb 7.5 vs 5.5-6.9; tpm 0.9 vs 1.2-1.3; fg_pct .520 vs .447-.498; ft_pct .740 vs .765-.828 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Isaiah Hartenstein | 7 of 23 | 75 | 104 | 141 | 92 | 100 | 102 | pts 11.5 vs 9.1-10.5; reb 11 vs 9.2-10.3; fg_pct .585 vs .597-.611; ft_pct .680 vs .642-.656 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Zach LaVine | 7 of 23 | 56 | 100 | 162 | 68 | 77 | 118 | pts 22.5 vs 17-21.1; reb 4.5 vs 3.1-3.6; ast 4 vs 2.8-3.4; tov 2.6 vs 2-2.4 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 5 of 23 | 89 | 142 | 122 | 131 | 125 | 123 | pts 16.8 vs 13.4-15.1; tov 1.5 vs 1-1.2; fg_pct .465 vs .432-.443 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Dyson Daniels | 5 of 23 | 11 | 62 | 20 | 64 | 56 | 53 | pts 14.5 vs 11.3-11.8; stl 3 vs 2-2.4; tpm 1.1 vs 0.5-0.6; fg_pct .495 vs .501-.513 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Herbert Jones | 5 of 23 | 74 | 182 | >490 | 169 | >200 | >250 | — | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Josh Hart | 5 of 23 | 67 | 96 | 68 | 84 | 91 | 94 | pts 13.5 vs 11.9-12.2; tpm 1 vs 1.2-1.5; fg_pct .520 vs .498-.503; ft_pct .780 vs .751-.759 | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Saddiq Bey | 5 of 23 | 95 | 176 | 109 | 132 | 169 | 143 | blk 0.4 vs 0.1-0.1; tpm 2.4 vs 1.8-2; tov 1.5 vs 0.8-0.9 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Karl-Anthony Towns (18 mocks, value 6, market 15); Jalen Williams (15 mocks, value 16, market 39); Derrick White (12 mocks, value 24, market 44); Jalen Johnson (6 mocks, value 13, market 11); Mikal Bridges (6 mocks, value 61, market 82).

What this room changed (the check re-run with mock 73 registered, `arena/results/repeat_market_check_2026-10-09_m73.json`; the previous run, with mock 72 registered, on 22 mocks is `repeat_market_check_2026-10-09_m72.json`): 23 of 23 mocks replayed; 14 flagged against 13. Newly across the five-mock bar: Josh Hart (the 🎯 in 5 mocks, value 67 against market 96). LINE QUESTIONED lines: PJ Washington, Daniel Gafford, Devin Vassell, Herbert Jones (unchanged). Every flagged line sits inside Sunday's WO-5 top-150 re-derivation, where the D-RN-3 range check requires a mechanism for each outlier cell.

*Correction (2026-10-10, D-RN-6).* The Yahoo Rank and Rotoworld receipts for Herbert Jones in the table above read `>490` and `>200` because the check folded names without the kit's spelling-alias table (`report/market/build_market.py` ALIASES: Herb Jones = Herbert Jones); both files list him as Herb Jones: Yahoo ranks him 147 (`yahoo-proj-2026-10-06.csv`, yrank; his XRank in the same file, the card's market column, is 134) and Rotoworld 134 (`rotoworld-9cat-2026-10-05.csv`). RotoBaller's `>250` is real (he is not in its 250). The verdict stands: 147 and 134 are 73 and 60 places below our 74, so all four outside ranks still sit 25+ places below ours. The check reads the alias table since 2026-10-10 (deck `scripts/repeat_market_check.py`, two red-first gate cases); the corrected run on the same page is `arena/results/repeat_market_check_2026-10-10_alias.json` (`after-report-2026-10-10-alias-fix.md`).

## 9. The off-card turns, read one by one

- **#34 Anthony Davis** (card #2, 0.002 behind Chet Holmgren, who went #36 to David Mandem): the 🎯 alone +1.26 title points; hindsight's best single swap here is Chet Holmgren +0.014 a week.
- **#58 Dyson Daniels** (card #2, 0.000 behind OG Anunoby, who went #63 to David): the 🎯 alone +0.00 title points; hindsight's best single swap here is Tyler Herro +0.007 a week.
- **#63 OG Anunoby** (card #2, 0.002 behind Payton Pritchard, who went #82 to David): the 🎯 alone +0.00 title points; hindsight has nothing better at this turn.
- **#87 Dylan Harper** (card #59, 0.246 behind Josh Hart, who went #88 to Angelbert): the 🎯 alone +4.50 title points; hindsight's best single swap here is Immanuel Quickley +0.131 a week.
- **#111 Aaron Gordon** (card #2, 0.010 behind Sandro Mamukelashvili, who went #130 to David): the 🎯 alone +0.00 title points; hindsight's best single swap here is Myles Turner +0.001 a week.
- **#130 Sandro Mamukelashvili** (card #2, 0.000 behind PJ Washington, who went #135 to David): the 🎯 alone +0.00 title points; hindsight has nothing better at this turn.
- **#154 Tari Eason** (card #9, 0.057 behind Christian Braun, who went undrafted): the 🎯 alone +0.67 title points; hindsight's best single swap here is Kyle Filipowski +0.086 a week.

## Watchlist

- The 7 off-card turns: #34 Anthony Davis (card #2), #58 Dyson Daniels (card #2), #63 OG Anunoby (card #2), #87 Dylan Harper (card #59), #111 Aaron Gordon (card #2), #130 Sandro Mamukelashvili (card #2), #154 Tari Eason (card #9). The card's man alone at each, with every other pick as drafted: #34 +1.26, #58 +0.00, #63 +0.00, #87 +4.50, #111 +0.00, #130 +0.00, #154 +0.67 title points; the whole follow-card chain +6.27.
- The preseason standouts (§7): Sunday's WO-5 pass re-derives their lines; the next human room then prices them on the new values.
- The survival chips against humans (D62-2: leave, log).

## Open-item receipts

| item | query run (2026-10-09) | dated finding |
|---|---|---|
| (this analysis) | machine replay only — no web research in this report | pull receipts for the window live in `after-report-2026-10-09.md` (the morning's pull) and `after-report-2026-10-09-research.md` (the evening's research pass), same day |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull and research pass, same day (after-report-2026-10-09.md, after-report-2026-10-09-research.md, receipts dated 10/9) | all HELD or unsigned on 2026-10-09; nothing changed since |

## Bounds

- A1: the room ran on the v53/v54 card (v54 published 20:29 UTC; the paste arrived after mock 72's grade); the two share engine, values, prices and pool, so the grade and the echoes read the same on either.
- Grades are on the v53/v54 lines; Sunday's WO-5 refresh will move them.
- A public room is a practice rep against strangers: the title odds are against the league's real bracket with these twelve rosters, not a forecast of the league.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D73-1 | The first human room on v54 grades 34.17 percent with the card followed at 6 of 13 turns (off the card: #34 Anthony Davis (card #2), #58 Dyson Daniels (card #2), #63 OG Anunoby (card #2), #87 Dylan Harper (card #59), #111 Aaron Gordon (card #2), #130 Sandro Mamukelashvili (card #2), #154 Tari Eason (card #9)); the follow-card chain grades 40.44 percent. Log it? | log it; no card change |
| D72-1, D71-1, D70-1, D69-1, D68-1..3, D61-4, D-RN-1..5, D67-1..6, D66-1, D-V4-1, D-CAST-1..4, D62-1..3, D-1008-1..3, D-1009-1..13 and earlier | carried | carried |

## Provenance

- Inputs: the owner's paste (the deck tool's LIVE feed and Yahoo's recap, 2026-10-09), pinned as `scratchpad m73/paste.txt`; the recap resolved by `hoops.py draft resync` to `arena/data/states/draft_state_73.json` (md5 `69a8c03ee2c922c9a14b5d6aea8bed1d`); the tool events pinned as `arena/data/events/m73_tool_events.json`; the pool is rev `03cba0a`'s data/players.csv, whose non-note columns equal `arena/results/players_v53.csv`.
- Every figure from `arena/results/m73_*.json` and `target_wait_2026-10-09b.json`; the arms use 18,000 CRN seasons (seeds 11/23/47) on the real eight-team bracket; the deck card, the DOM replay and the audit ran the v54 page's own engine under node; §7's prices from `report/market/yahoo-2026-10-09.csv` and the deck board snapshot of the 10/09 pull (v52; values unchanged through v54).
- Not verified: nothing here rests on web research.

## In plain language

**What this was.** A live room against twelve strangers on tonight's page. It grades 34.2 percent on the real bracket, first of twelve, first in expected weekly category wins, and you took the card's name at 6 of 13 turns and a Top-5 name at 11.

**What the card left on the table.** Hindsight's best single swap is Immanuel Quickley at #87, worth about 0.13 categories a week. The advice line was silent.

**Following the card.** Following it all the way grades 40.4 percent against 34.2 as drafted.

**The tool.** The log replayed on the real page with zero drift: one halt (the bare "Jalen" with three Jalens on the board, resent as the full name), one undo, 19 shared-surname feeds resolved as the page said, and the 7 off-card lines you saw are the page's own, re-emitted to the third decimal.

**Your decision.** D73-1 log the room (default yes). Everything earlier is carried.
