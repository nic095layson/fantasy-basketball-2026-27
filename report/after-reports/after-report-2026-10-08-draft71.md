# After-report — draft_71: the third MOCK of the evening, the first on v51, against the league-mates' models — the card followed at 0 of 13 turns

**Owner request (2026-10-08):** a third exported draft state, pasted into the chat as JSON without comment while the D-RN-3 range check was being built — graded as mock 71, the standing practice-room protocol. The room ran on v51 (the card-row display change published after mock 70; no engine, value or pool change).

**Room:** the deck's own MOCK mode, 12 × 13, owner seat 10, the eleven opponents the E18 behavioral models of the real league-mates in the league's real order (1 Oblena, 2 Noah, 3 Will, 4 Robby, 5 Kyle, 6 Martin, 7 John, 8 JCo, 9 Kevin, 11 Cayas, 12 Hegi). Not a public room: LEDGER-eligible. **Deck used:** v51 (rev `1026558`, live at the standing URL since its publish this evening; the card-row display change over v50 — research notes behind a muted †; engine, values and pool identical to v50; Porziņģis veto live) (A1). **Method:** the state is the deck's own export (no Yahoo recap and no tool log exist for a MOCK), checked snake-consistent with every name in the v51 pool (identical to v50's) and the `cast` field equal to the real order; the grade is the deck plane's machine-derived retro (`arena/results/m71_*.json`; deck card replayed from the v51 page; title odds on the league's real eight-team bracket). Every figure below is read from those files. Verification: this file passes `report/check_report.py` and the deck's `judgment_open_items.py --check-report` and `repeat_market_check.py --check-report`.

Pull window: 2026-10-08 → 2026-10-08 (analysis only, the sixth report of the day; no roster pull).

**Headline.** As drafted **3.48 percent** on the real bracket (rank 9 of 12), expected weekly category wins 4.316, rank 9 of 12 (next 5.346), favored in 4 of 11 head-to-heads; the card's 🎯 taken at 0 of 13 turns, a Top-5 row at 3 of 13 (off the card: #10 Jayson Tatum (card #19), #15 Giannis Antetokounmpo (card #23), #34 Trae Young (card #24), #39 Jaylen Brown (card #20), #58 Damian Lillard (card #72), #63 Deni Avdija (card #6), #82 Zion Williamson (card #41), #87 Day'Ron Sharpe (card #3), #106 Draymond Green (card #11), #111 Yaxel Lendeborg (card #3), #130 Herbert Jones (card #3), #135 Tari Eason (card #11), #154 Bilal Coulibaly (card #11)); the self-consistent follow-card chain from the same seat grades 27.13 percent. Category shape: REB, AST, ST in the top three of the weekly model, FT%, 3PTM, TO ninth or lower. Hindsight's best single swap is Tyler Herro at #58 (+0.299 a week).

## 1. Roster changes

None — a MOCK room; no pull, no row moved on either plane.

## 2. The team, replayed

| arm | ECW (rank; next) | favored | title odds (rank) |
|---|---|---|---|
| as drafted (the card's 🎯 at 0 of 13 turns) | 4.316 (rank 9; next 5.346) | 4 of 11 | 3.48% (rank 9) |
| follow-card, self-consistent (arms stage) | 5.323 (rank 2; next 5.347) | 10 of 11 | 27.13% (rank 2) |
| 🎯 at #10: Karl-Anthony Towns for Jayson Tatum (card #19; Karl-Anthony Towns went #11) | 4.518 (rank 5; next 5.333) | 6 of 11 | 7.08% (rank 6) |
| 🎯 at #15: Jalen Williams for Giannis Antetokounmpo (card #23; Jalen Williams went #25) | 4.130 (rank 11; next 5.336) | 2 of 11 | 1.79% (rank 11) |
| 🎯 at #34: Dyson Daniels for Trae Young (card #24; Dyson Daniels went #48) | 4.339 (rank 8; next 5.288) | 5 of 11 | 3.39% (rank 9) |
| 🎯 at #39: Dyson Daniels for Jaylen Brown (card #20; Dyson Daniels went #48) | 4.342 (rank 8; next 5.236) | 4 of 11 | 3.57% (rank 9) |
| 🎯 at #58: Payton Pritchard for Damian Lillard (card #72; Payton Pritchard went #61) | 4.587 (rank 4; next 5.355) | 7 of 11 | 8.59% (rank 5) |
| 🎯 at #63: Jalen Suggs for Deni Avdija (card #6; Jalen Suggs went #102) | 4.265 (rank 9; next 5.349) | 2 of 11 | 2.73% (rank 9) |
| 🎯 at #82: Jalen Suggs for Zion Williamson (card #41; Jalen Suggs went #102) | 4.379 (rank 8; next 5.348) | 4 of 11 | 4.46% (rank 8) |
| 🎯 at #87: Jalen Suggs for Day'Ron Sharpe (card #3; Jalen Suggs went #102) | 4.302 (rank 9; next 5.342) | 2 of 11 | 3.20% (rank 9) |
| 🎯 at #106: Yaxel Lendeborg for Draymond Green (card #11; Yaxel Lendeborg went #111) | 4.316 (rank 9; next 5.346) | 4 of 11 | 3.48% (rank 9) |
| 🎯 at #111: PJ Washington for Yaxel Lendeborg (card #3; PJ Washington went #125) | 4.328 (rank 8; next 5.350) | 4 of 11 | 3.81% (rank 9) |
| 🎯 at #130: Daniel Gafford for Herbert Jones (card #3; Daniel Gafford went #150) | 4.401 (rank 8; next 5.341) | 6 of 11 | 4.63% (rank 8) |
| 🎯 at #135: Daniel Gafford for Tari Eason (card #11; Daniel Gafford went #150) | 4.440 (rank 7; next 5.344) | 6 of 11 | 5.16% (rank 8) |
| 🎯 at #154: Saddiq Bey for Bilal Coulibaly (card #11; Saddiq Bey went #155) | 4.372 (rank 7; next 5.353) | 4 of 11 | 4.51% (rank 7) |
| advice at #15: Chet Holmgren for Jalen Williams (the 'now' man; Chet Holmgren went #18) | 4.315 (rank 9; next 5.362) | 4 of 11 | 3.91% (rank 9) |
| advice at #34: Desmond Bane for Dyson Daniels (the 'now' man; Desmond Bane went #41) | 4.374 (rank 8; next 5.345) | 4 of 11 | 4.38% (rank 8) |
| advice at #39: Onyeka Okongwu for Dyson Daniels (the 'now' man; Onyeka Okongwu went #43) | 4.409 (rank 8; next 5.350) | 6 of 11 | 4.78% (rank 8) |
| advice at #58: Rudy Gobert for Payton Pritchard (the 'now' man; Rudy Gobert went #68) | 4.562 (rank 5; next 5.316) | 7 of 11 | 7.99% (rank 5) |
| advice at #63: Rudy Gobert for Jalen Suggs (the 'now' man; Rudy Gobert went #68) | 4.395 (rank 8; next 5.330) | 5 of 11 | 4.54% (rank 8) |
| advice at #82: Myles Turner for Jalen Suggs (the 'now' man; Myles Turner went #99) | 4.411 (rank 8; next 5.352) | 5 of 11 | 5.06% (rank 8) |
| the 6 advice 'now' men together (#15 Holmgren, #34 Bane, #39 Okongwu, #58 Gobert, #63 Gobert, #82 Turner) | 4.589 (rank 4; next 5.331) | 9 of 11 | 10.23% (rank 3) |
| hindsight single swap Karl-Anthony Towns at #10 | 4.518 (rank 5; next 5.333) | 6 of 11 | 7.08% (rank 6) |
| hindsight single swap Franz Wagner at #34 | 4.414 (rank 8; next 5.330) | 5 of 11 | 5.00% (rank 8) |
| hindsight single swap Ivica Zubac at #39 | 4.473 (rank 6; next 5.324) | 6 of 11 | 6.30% (rank 6) |
| hindsight single swap Tyler Herro at #58 | 4.615 (rank 4; next 5.347) | 8 of 11 | 9.63% (rank 3) |
| hindsight single swap Paolo Banchero at #63 | 4.399 (rank 8; next 5.300) | 4 of 11 | 4.48% (rank 8) |
| hindsight single swap Zach LaVine at #82 | 4.459 (rank 6; next 5.360) | 5 of 11 | 6.13% (rank 6) |
| hindsight single swap Zach LaVine at #87 | 4.369 (rank 8; next 5.357) | 4 of 11 | 4.35% (rank 9) |
| hindsight single swap Daniel Gafford at #106 | 4.372 (rank 8; next 5.339) | 4 of 11 | 4.09% (rank 8) |
| hindsight single swap Daniel Gafford at #111 | 4.341 (rank 8; next 5.346) | 5 of 11 | 3.66% (rank 9) |
| hindsight single swap Daniel Gafford at #130 | 4.401 (rank 8; next 5.341) | 6 of 11 | 4.63% (rank 8) |
| hindsight single swap Daniel Gafford at #135 | 4.440 (rank 7; next 5.344) | 6 of 11 | 5.16% (rank 8) |
| hindsight single swap Kyle Filipowski at #154 | 4.385 (rank 8; next 5.338) | 4 of 11 | 4.63% (rank 8) |

Category ranks (weekly model): FG% 6 · FT% 12 · 3PTM 12 · PTS 6 · REB 2 · AST 2 · ST 1 · BLK 8 · TO 12.

## 3. Pick by pick — card vs owner vs hindsight

| pick | deck 🎯 (Top-5) | owner took | card rank · gap (blend) | hindsight best single swap (ΔECW vs final rosters) |
|---|---|---|---|---|
| #10 | Karl-Anthony Towns (Karl-Anthony Towns, Jalen Johnson, Jalen Williams, Anthony Davis, Kevin Durant) | Jayson Tatum | #19 · +0.047 | Karl-Anthony Towns +0.202 |
| #15 | Jalen Williams (Jalen Williams, Derrick White, Jamal Murray, Chet Holmgren, Evan Mobley) | Giannis Antetokounmpo | #23 · +0.063 | none positive (the pick was hindsight-best) |
| #34 | Dyson Daniels (Dyson Daniels, OG Anunoby, Desmond Bane, Jaren Jackson Jr., Franz Wagner) | Trae Young | #24 · +0.091 | Franz Wagner +0.098 |
| #39 | Dyson Daniels (Dyson Daniels, OG Anunoby, Desmond Bane, Onyeka Okongwu, Franz Wagner) | Jaylen Brown | #20 · +0.075 | Ivica Zubac +0.157 |
| #58 | Payton Pritchard (Payton Pritchard, De'Aaron Fox, Tyler Herro, Jalen Suggs, Rudy Gobert) | Damian Lillard | #72 · +0.262 | Tyler Herro +0.299 |
| #63 | Jalen Suggs (Jalen Suggs, De'Aaron Fox, Rudy Gobert, Day'Ron Sharpe, Naz Reid) | Deni Avdija | #6 · +0.033 | Paolo Banchero +0.083 |
| #82 | Jalen Suggs (Jalen Suggs, Zach LaVine, Day'Ron Sharpe, Isaiah Hartenstein, Myles Turner) | Zion Williamson | #41 · +0.157 | Zach LaVine +0.142 |
| #87 | Jalen Suggs (Jalen Suggs, Zach LaVine, Day'Ron Sharpe, Isaiah Hartenstein, Myles Turner) | Day'Ron Sharpe | #3 · +0.015 | Zach LaVine +0.053 |
| #106 | Yaxel Lendeborg (Yaxel Lendeborg, PJ Washington, Daniel Gafford, Sandro Mamukelashvili, Herbert Jones) | Draymond Green | #11 · +0.052 | Daniel Gafford +0.056 |
| #111 | PJ Washington (PJ Washington, Sandro Mamukelashvili, Yaxel Lendeborg, Daniel Gafford, Herbert Jones) | Yaxel Lendeborg | #3 · +0.002 | Daniel Gafford +0.025 |
| #130 | Daniel Gafford (Daniel Gafford, Sandro Mamukelashvili, Herbert Jones, Saddiq Bey, Collin Gillespie) | Herbert Jones | #3 · +0.009 | Daniel Gafford +0.085 |
| #135 | Daniel Gafford (Daniel Gafford, Sandro Mamukelashvili, Saddiq Bey, Collin Gillespie, Jerami Grant) | Tari Eason | #11 · +0.080 | Daniel Gafford +0.124 |
| #154 | Saddiq Bey (Saddiq Bey, Collin Gillespie, Kyle Filipowski, Jerami Grant, Christian Braun) | Bilal Coulibaly | #11 · +0.092 | Kyle Filipowski +0.068 |

Advice line (page reading): fired at #15 (Chet Holmgren now, Jamal Murray next turn (5% to survive): +0.024 cats/wk over the pair); #34 (Desmond Bane now, OG Anunoby next turn (92% to survive): +0.031 cats/wk over the pair); #39 (Onyeka Okongwu now, OG Anunoby next turn (68% to survive): +0.078 cats/wk over the pair); #58 (Rudy Gobert now, Payton Pritchard next turn (77% to survive): +0.034 cats/wk over the pair); #63 (Rudy Gobert now, Jalen Suggs next turn (79% to survive): +0.038 cats/wk over the pair); #82 (Myles Turner now, Jalen Suggs next turn (74% to survive): +0.013 cats/wk over the pair).

## 4. Where the league-mates' models took the preseason standouts

The owner asked today which preseason performers stood out. The cast prices players from the 10/06 Yahoo file and the board's values, so it has not seen the preseason; a real league-mate who reacts to the box scores would take these men earlier than the models do here. The public rooms of 10/07 and 10/08 are humans who could see the games.

| player | deck rank (v50) | Yahoo ADP 10/06 | this room (cast) | mock 67, public, 10/07 | mock 68, public, 10/08 |
|---|---|---|---|---|---|
| Yaxel Lendeborg | 82 | 115.7 | #111 (David) | #126 | #127 |
| Ty Jerome | 101 | 115.1 | #121 (Oblena) | #107 | #82 (you) |
| Sandro Mamukelashvili | 81 | 119.3 | #152 (JCo) | #135 (you) | #133 |
| Ryan Rollins | 70 | 76.4 | #71 (Noah) | #68 | #67 |
| Darryn Peterson | 140 | 103.2 | #107 (Cayas) | #108 | #111 (you) |
| Kel'el Ware | 80 | 75.6 | #81 (Kevin) | #65 | #65 |
| Cameron Boozer | 48 | 55.9 | #52 (Robby) | #49 | #61 |
| Aday Mara | 316 | 107.7 | undrafted | undrafted | undrafted |
| Jalen Williams | 16 | 40.4 | #25 (Oblena) | #34 (you) | #39 (you) |
| Tyrese Haliburton | 7 | 14.2 | #6 (Martin) | #15 (you) | #9 |
| Damian Lillard | 88 | 68.3 | #58 (David) | #82 (you) | #56 |
| Deni Avdija | 77 | 40.8 | #63 (David) | #43 | #40 |

Late card: 0 unpriced rows across the owner's three turns in rounds 11–13. Repeat-name audit (`m71_repeat_names_audit.json`): the #1 changes at 12 of 13 turns under other rooms' rosters (10 of 13 against an empty roster); Gafford on the Top-5 at 4, Braun 1, Poeltl 0.

## 5. Survival chips and the cast

Survival (`m71_survival.json`): this room 57 rows, predicted 0.539 vs realized 0.544, Brier 0.222; BUY NOW 3 of 6 survived, TOSS-UP 5 of 13, quiet 23 of 38. Pooled 51–71: 1068 rows, Brier 0.239.

| seat | manager | profile lean (market / value) | mean market rank minus pick | mean value rank minus pick | guards / centers | loyalty names on the board | taken by them |
|---|---|---|---|---|---|---|---|
| 1 | Oblena | 0.35 / 0.65 | -2.9 | +9.8 | 5 / 5 | Donovan Mitchell (seat 9) | 0 of 1 |
| 2 | Noah | 0.75 / 0.25 | -12.0 | +18.5 | 5 / 6 | LaMelo Ball (seat 2) | 1 of 1 |
| 3 | Will | 0.55 / 0.45 | -7.9 | -2.8 | 7 / 4 | Onyeka Okongwu (seat 6), Jaden Ivey (undrafted) | 0 of 1 |
| 4 | Robby | 0.70 / 0.30 | -4.0 | +17.9 | 8 / 3 | Jarrett Allen (seat 4), Collin Sexton (seat 4), Devin Booker (seat 4), Devin Vassell (seat 4) | 4 of 4 |
| 5 | Kyle | 0.45 / 0.55 | -5.0 | +12.7 | 6 / 3 | none | 0 of 0 |
| 6 | Martin | 0.45 / 0.55 | -3.2 | +11.8 | 5 / 5 | Luka Doncic (seat 4), Brandon Ingram (seat 3), Jalen Suggs (seat 6) | 1 of 3 |
| 7 | John | 0.50 / 0.50 | -4.5 | +11.5 | 3 / 6 | Tyrese Maxey (seat 7), Jakob Poeltl (seat 7), Jeremy Sochan (undrafted) | 2 of 2 |
| 8 | JCo | 0.45 / 0.55 | -1.3 | +7.5 | 7 / 4 | Tyrese Haliburton (seat 6), Jimmy Butler (undrafted), Nic Claxton (seat 8) | 1 of 2 |
| 9 | Kevin | 0.45 / 0.55 | -1.6 | +16.5 | 9 / 2 | Pascal Siakam (seat 6) | 0 of 1 |
| 10 | David | owner | -0.4 | +4.1 | 7 / 4 | none | — |
| 11 | Cayas | 0.40 / 0.60 | -3.8 | +11.2 | 6 / 4 | none | 0 of 0 |
| 12 | Hegi | 0.65 / 0.35 | -3.6 | +23.2 | 7 / 4 | Immanuel Quickley (seat 12), Andrew Wiggins (seat 12) | 2 of 2 |

loyalty fired on 11 of the 17 loyalty names that were drafted by anyone (undrafted names excluded)

Target-wait (`target_wait_2026-10-08d.json`, mocks 56–71): deep (mkt − pick ≥ 24) — 🎯s passed on 40, still there at the next owner turn 25, at the turn after 7 of 36; mid (12–23) — 🎯s passed on 9, still there at the next owner turn 2, at the turn after 1 of 8; near (< 12) — 🎯s passed on 23, still there at the next owner turn 8, at the turn after 0 of 22.

## 6. Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 3e594b9dc16b), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 21 of 21 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-06.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-06.csv`, `hashtag-2026-10-06.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| PJ Washington | 17 of 21 | 87 | 149 | 178 | 144 | 141 | 121 | ast 2.4 vs 1.9-2; tov 1.5 vs 1.7-1.8; fg_pct .470 vs .448-.451; ft_pct .750 vs .698-.703 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Payton Pritchard | 16 of 21 | 37 | 82 | 33 | 90 | 92 | 72 | stl 1 vs 0.7-0.8; tpm 3.8 vs 3-3.2; tov 2 vs 1.3-1.3; ft_pct .850 vs .873-.875 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Sandro Mamukelashvili | 16 of 21 | 81 | 170 | 138 | 105 | 153 | 120 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 15 of 21 | 28 | 65 | 60 | 56 | 43 | 44 | pts 18.5 vs 16.4-17; ast 2.3 vs 2.1-2.1; ft_pct .805 vs .813-.819 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Daniel Gafford | 10 of 21 | 90 | 181 | 188 | 180 | 161 | 155 | pts 10.5 vs 9.1-9.8; reb 7.5 vs 5.8-6.5; ast 1.5 vs 1.1-1.2; blk 1.7 vs 1.2-1.4; fg_pct .700 vs .648-.689; ft_pct .700 vs .671-.687 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Jalen Suggs | 10 of 21 | 59 | 108 | 89 | 54 | 84 | 99 | pts 17 vs 14.1-15.1; ast 4 vs 4.8-5 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 9 of 21 | 82 | 144 | 94 | 121 | 137 | 98 | reb 7.5 vs 5.5-6.9; tpm 0.9 vs 1.2-1.3; fg_pct .520 vs .447-.498; ft_pct .740 vs .765-.828 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Isaiah Hartenstein | 7 of 21 | 75 | 104 | 141 | 92 | 100 | 102 | pts 11.5 vs 9.1-10.5; reb 11 vs 9.2-10.3; fg_pct .585 vs .597-.611; ft_pct .680 vs .642-.656 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Zach LaVine | 6 of 21 | 56 | 101 | 162 | 68 | 77 | 118 | pts 22.5 vs 17-21.1; reb 4.5 vs 3.1-3.6; ast 4 vs 2.8-3.4; tov 2.6 vs 2-2.4 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 5 of 21 | 89 | 142 | 122 | 131 | 125 | 123 | pts 16.8 vs 13.4-15.1; tov 1.5 vs 1-1.2; fg_pct .465 vs .432-.443 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Dyson Daniels | 5 of 21 | 11 | 62 | 20 | 65 | 56 | 53 | pts 14.5 vs 11.3-11.8; stl 3 vs 2-2.4; tpm 1.1 vs 0.5-0.6; fg_pct .495 vs .501-.513 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Saddiq Bey | 5 of 21 | 95 | 175 | 109 | 132 | 169 | 143 | blk 0.4 vs 0.1-0.1; tpm 2.4 vs 1.8-2; tov 1.5 vs 0.8-0.9 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Karl-Anthony Towns (16 mocks, value 6, market 15); Jalen Williams (15 mocks, value 16, market 39); Derrick White (11 mocks, value 24, market 45); Jalen Johnson (6 mocks, value 13, market 11); Mikal Bridges (6 mocks, value 61, market 83).

What this room changed (the check re-run with mock 71 registered, `arena/results/repeat_market_check_2026-10-08_m71.json`; this evening's first run on 20 mocks is `repeat_market_check_2026-10-08.json`): 21 of 21 mocks replayed; 12 flagged against 10. Two names crossed the five-mock bar here — Dyson Daniels (the card's 🎯 at #34 and #39 in this room; value rank 11 against market 62, three of the four outside lists 25+ places below ours, and four cells above every outside projection: points, steals, threes, field-goal percentage) and Saddiq Bey (the 🎯 at #154). The three LINE QUESTIONED lines are unchanged (PJ Washington now the 🎯 in 17 mocks, Gafford 10, Vassell 5); all three, Daniels and Bey sit inside WO-5's top-150 re-derivation, where the D-RN-3 range check now also requires a mechanism for each of their outlier cells.

## Watchlist

- The 13 off-card turns: #10 Jayson Tatum (card #19), #15 Giannis Antetokounmpo (card #23), #34 Trae Young (card #24), #39 Jaylen Brown (card #20), #58 Damian Lillard (card #72), #63 Deni Avdija (card #6), #82 Zion Williamson (card #41), #87 Day'Ron Sharpe (card #3), #106 Draymond Green (card #11), #111 Yaxel Lendeborg (card #3), #130 Herbert Jones (card #3), #135 Tari Eason (card #11), #154 Bilal Coulibaly (card #11). The card's man alone at each, with every other pick as drafted: #10 +3.60, #15 -1.69, #34 -0.09, #39 +0.09, #58 +5.11, #63 -0.75, #82 +0.98, #87 -0.28, #106 +0.00, #111 +0.33, #130 +1.15, #135 +1.68, #154 +1.03 title points; the whole follow-card chain +23.65.
- The preseason standouts (§4): the WO-5 passes on 10/11 and 10/13 (D-1008-3) re-derive their lines; the cast will then price them on the new values.
- The survival chips against the cast (D62-2: leave, log).

## Open-item receipts

| item | query run (2026-10-08) | dated finding |
|---|---|---|
| (this analysis) | machine replay only — no web research in this report | pull receipts for the window live in `after-report-2026-10-08.md` (the morning's pull, same day) |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (after-report-2026-10-08.md, receipts dated 10/8) | all HELD or unsigned on 2026-10-08; nothing changed since |

## Bounds

- A1: the room ran on v51, the version live at the standing URL when it was exported; v50 and v51 share engine, values and pool, so the grade reads the same on either.
- Grades are on the v50/v51 lines; the WO-5 refresh will move them.
- A MOCK has no second record; only the owner's picks are an outside input.
- One room is one draw of the bots' seeded noise; the fidelity read is a single sample.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D71-1 | The third cast room tonight (the first on v51) grades 3.48 percent with the card followed at 0 of 13 turns (off the card: #10 Jayson Tatum (card #19), #15 Giannis Antetokounmpo (card #23), #34 Trae Young (card #24), #39 Jaylen Brown (card #20), #58 Damian Lillard (card #72), #63 Deni Avdija (card #6), #82 Zion Williamson (card #41), #87 Day'Ron Sharpe (card #3), #106 Draymond Green (card #11), #111 Yaxel Lendeborg (card #3), #130 Herbert Jones (card #3), #135 Tari Eason (card #11), #154 Bilal Coulibaly (card #11)); the follow-card chain grades 27.13 percent. Log it? | log it; no card change |
| D70-1, D69-1, D68-1..3, D61-4, D-RN-1..5, D67-1..6, D66-1, D-V4-1, D-CAST-1..4, D62-1..3, D-1008-1..3 and earlier | carried | carried |

## Provenance

- Inputs: the owner's exported draft state (pasted 2026-10-08), written in the export's own JSON format to `arena/data/states/draft_state_71.json` (md5 `0fb234a092690b115e61cdf0c24bcd89`); the pool is main `1026558`'s data/players.csv, byte-identical to `arena/results/m68_players_v50.csv`.
- Every figure from `arena/results/m71_*.json` and `target_wait_2026-10-08d.json`; the arms use 18,000 CRN seasons (seeds 11/23/47) on the real eight-team bracket; the deck card and the audit ran the v51 page's own engine under node; §4's prices from `report/market/yahoo-2026-10-06.csv` and the deck board snapshot of the 10/08 pull.
- Not verified: nothing here rests on web research.

## In plain language

**What this was.** Your third practice room tonight against the models of your eleven league-mates, on today's page. It grades 3.5 percent on the real bracket, ninth of twelve, ninth in expected weekly category wins, and you took the card's name at 0 of 13 turns.

**What the card left on the table.** Hindsight's best single swap is Tyler Herro at #58, worth about 0.30 categories a week. The advice line spoke at 6 turn(s).

**Following the card.** You took the card's name at 0 of 13 turns. Following it all the way grades 27.1 percent against 3.5 as drafted.

**The preseason names.** The league-mate models haven't seen the preseason, so §4 shows where they took the standouts against where real people took them in the last two public rooms.

**Your decision.** D71-1 log the room (default yes). Everything earlier is carried.
