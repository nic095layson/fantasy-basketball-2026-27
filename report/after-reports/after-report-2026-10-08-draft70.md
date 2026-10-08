# After-report — draft_70: the second MOCK on v50 against the league-mates' models — the card followed at 4 of 13 turns

**Owner request (2026-10-08):** a second exported draft state, pasted into the chat as JSON without comment while the card-row change was being built — graded as mock 70, the standing practice-room protocol. The room ran on v50: Version 51 (the card-row display change, no engine change) was published after the paste.

**Room:** the deck's own MOCK mode, 12 × 13, owner seat 10, the eleven opponents the E18 behavioral models of the real league-mates in the league's real order (1 Oblena, 2 Noah, 3 Will, 4 Robby, 5 Kyle, 6 Martin, 7 John, 8 JCo, 9 Kevin, 11 Cayas, 12 Hegi). Not a public room: LEDGER-eligible. **Deck used:** v50 (rev `9f54e99`, live at the standing URL from 15:15 UTC; the 10/08 pull's build — notes and Hawkins's team, no line, tag or card change; engine identical to v49; Porziņģis veto live) (A1). **Method:** the state is the deck's own export (no Yahoo recap and no tool log exist for a MOCK), checked snake-consistent with every name in the v50 pool and the `cast` field equal to the real order; the grade is the deck plane's machine-derived retro (`arena/results/m70_*.json`; deck card replayed from the v50 page; title odds on the league's real eight-team bracket). Every figure below is read from those files. Verification: this file passes `report/check_report.py` and the deck's `judgment_open_items.py --check-report`.

Pull window: 2026-10-08 → 2026-10-08 (analysis only, the fourth report of the day; no roster pull).

**Headline.** As drafted **20.68 percent** on the real bracket (rank 2 of 12), expected weekly category wins 5.092, rank 2 of 12 (next 5.144), favored in 10 of 11 head-to-heads; the card's 🎯 taken at 4 of 13 turns, a Top-5 row at 7 of 13 (off the card: #10 Giannis Antetokounmpo (card #16), #15 Cooper Flagg (card #8), #34 Trae Young (card #16), #63 Kon Knueppel (card #29), #82 Day'Ron Sharpe (card #6), #87 Myles Turner (card #3), #106 Yaxel Lendeborg (card #3), #111 Ty Jerome (card #10), #154 Saddiq Bey (card #2)); the self-consistent follow-card chain from the same seat grades 30.77 percent. Category shape: 3PTM, ST in the top three of the weekly model, FT% ninth or lower. Hindsight's best single swap is Desmond Bane at #34 (+0.107 a week).

## 1. Roster changes

None — a MOCK room; no pull, no row moved on either plane.

## 2. The team, replayed

| arm | ECW (rank; next) | favored | title odds (rank) |
|---|---|---|---|
| as drafted (the card's 🎯 at 4 of 13 turns) | 5.092 (rank 2; next 5.144) | 10 of 11 | 20.68% (rank 2) |
| follow-card, self-consistent (arms stage) | 5.359 (rank 1; next 5.148) | 11 of 11 | 30.77% (rank 1) |
| 🎯 at #10: Karl-Anthony Towns for Giannis Antetokounmpo (card #16; Karl-Anthony Towns went #11) | 5.127 (rank 2; next 5.142) | 11 of 11 | 23.25% (rank 1) |
| 🎯 at #15: Jalen Williams for Cooper Flagg (card #8; Jalen Williams went #25) | 5.013 (rank 2; next 5.227) | 10 of 11 | 18.31% (rank 2) |
| 🎯 at #34: Dyson Daniels for Trae Young (card #16; Dyson Daniels went #44) | 5.155 (rank 1; next 5.154) | 11 of 11 | 23.76% (rank 1) |
| 🎯 at #63: Jalen Suggs for Kon Knueppel (card #29; Jalen Suggs went #91) | 5.141 (rank 2; next 5.141) | 10 of 11 | 22.50% (rank 2) |
| 🎯 at #82: Jalen Suggs for Day'Ron Sharpe (card #6; Jalen Suggs went #91) | 5.028 (rank 2; next 5.135) | 10 of 11 | 20.31% (rank 2) |
| 🎯 at #87: Jalen Suggs for Myles Turner (card #3; Jalen Suggs went #91) | 5.021 (rank 2; next 5.144) | 10 of 11 | 19.90% (rank 2) |
| 🎯 at #106: Sandro Mamukelashvili for Yaxel Lendeborg (card #3; Sandro Mamukelashvili went #135) | 5.092 (rank 2; next 5.144) | 10 of 11 | 20.68% (rank 2) |
| 🎯 at #111: Sandro Mamukelashvili for Ty Jerome (card #10; Sandro Mamukelashvili went #135) | 5.092 (rank 2; next 5.144) | 10 of 11 | 20.68% (rank 2) |
| 🎯 at #154: Daniel Gafford for Saddiq Bey (card #2; Daniel Gafford went #undrafted) | 5.077 (rank 2; next 5.151) | 10 of 11 | 19.92% (rank 2) |
| advice at #34: Payton Pritchard for Dyson Daniels (the 'now' man; Payton Pritchard went #58) | 5.092 (rank 2; next 5.144) | 10 of 11 | 20.68% (rank 2) |
| advice at #39: Onyeka Okongwu for OG Anunoby (the 'now' man; Onyeka Okongwu went #42) | 5.096 (rank 2; next 5.146) | 10 of 11 | 20.19% (rank 2) |
| advice at #63: Rudy Gobert for Jalen Suggs (the 'now' man; Rudy Gobert went #69) | 5.119 (rank 2; next 5.155) | 10 of 11 | 21.94% (rank 2) |
| advice at #82: Isaiah Hartenstein for Jalen Suggs (the 'now' man; Isaiah Hartenstein went #103) | 5.144 (rank 1; next 5.143) | 10 of 11 | 21.81% (rank 2) |
| the 4 advice 'now' men together (#34 Pritchard, #39 Okongwu, #63 Gobert, #82 Hartenstein) | 5.018 (rank 2; next 5.169) | 10 of 11 | 18.99% (rank 2) |
| hindsight single swap Karl-Anthony Towns at #10 | 5.127 (rank 2; next 5.142) | 11 of 11 | 23.25% (rank 1) |
| hindsight single swap Chet Holmgren at #15 | 5.166 (rank 1; next 5.146) | 11 of 11 | 22.72% (rank 2) |
| hindsight single swap Desmond Bane at #34 | 5.199 (rank 1; next 5.132) | 11 of 11 | 24.11% (rank 1) |
| hindsight single swap Franz Wagner at #39 | 5.103 (rank 2; next 5.140) | 10 of 11 | 21.40% (rank 2) |
| hindsight single swap Paolo Banchero at #63 | 5.182 (rank 1; next 5.072) | 11 of 11 | 24.33% (rank 1) |
| hindsight single swap Isaiah Hartenstein at #82 | 5.144 (rank 1; next 5.143) | 10 of 11 | 21.81% (rank 2) |
| hindsight single swap Isaiah Hartenstein at #87 | 5.093 (rank 2; next 5.154) | 10 of 11 | 20.79% (rank 2) |
| hindsight single swap Collin Gillespie at #111 | 5.128 (rank 2; next 5.139) | 10 of 11 | 22.31% (rank 2) |
| hindsight single swap Kyle Filipowski at #154 | 5.104 (rank 2; next 5.147) | 10 of 11 | 21.01% (rank 2) |

Category ranks (weekly model): FG% 4 · FT% 11 · 3PTM 1 · PTS 4 · REB 5 · AST 6 · ST 3 · BLK 6 · TO 5.

## 3. Pick by pick — card vs owner vs hindsight

| pick | deck 🎯 (Top-5) | owner took | card rank · gap (blend) | hindsight best single swap (ΔECW vs final rosters) |
|---|---|---|---|---|
| #10 | Karl-Anthony Towns (Karl-Anthony Towns, Anthony Davis, Kevin Durant, Jalen Williams, Chet Holmgren) | Giannis Antetokounmpo | #16 · +0.050 | Karl-Anthony Towns +0.035 |
| #15 | Jalen Williams (Jalen Williams, Derrick White, Jamal Murray, Stephen Curry, James Harden) | Cooper Flagg | #8 · +0.018 | Chet Holmgren +0.075 |
| #34 | Dyson Daniels (Dyson Daniels, OG Anunoby, Desmond Bane, Payton Pritchard, Franz Wagner) | Trae Young | #16 · +0.058 | Desmond Bane +0.107 |
| #39 | OG Anunoby (OG Anunoby, Desmond Bane, Dyson Daniels, Payton Pritchard, Onyeka Okongwu) | OG Anunoby | #1 · +0.000 | Franz Wagner +0.011 |
| #58 | Payton Pritchard (Payton Pritchard, De'Aaron Fox, Zach LaVine, Coby White, Jalen Suggs) | Payton Pritchard | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #63 | Jalen Suggs (Jalen Suggs, Naz Reid, Rudy Gobert, Zach LaVine, Isaiah Hartenstein) | Kon Knueppel | #29 · +0.114 | Paolo Banchero +0.090 |
| #82 | Jalen Suggs (Jalen Suggs, Isaiah Hartenstein, Mikal Bridges, Josh Hart, Zach LaVine) | Day'Ron Sharpe | #6 · +0.021 | Isaiah Hartenstein +0.052 |
| #87 | Jalen Suggs (Jalen Suggs, Zach LaVine, Myles Turner, Isaiah Hartenstein, Josh Hart) | Myles Turner | #3 · +0.022 | Isaiah Hartenstein +0.001 |
| #106 | Sandro Mamukelashvili (Sandro Mamukelashvili, PJ Washington, Yaxel Lendeborg, Devin Vassell, Cason Wallace) | Yaxel Lendeborg | #3 · +0.005 | none positive (the pick was hindsight-best) |
| #111 | Sandro Mamukelashvili (Sandro Mamukelashvili, PJ Washington, Devin Vassell, Saddiq Bey, Collin Gillespie) | Ty Jerome | #10 · +0.039 | Collin Gillespie +0.036 |
| #130 | PJ Washington (PJ Washington, Sandro Mamukelashvili, Devin Vassell, Herbert Jones, Saddiq Bey) | PJ Washington | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #135 | Sandro Mamukelashvili (Sandro Mamukelashvili, Devin Vassell, Saddiq Bey, Herbert Jones, Collin Gillespie) | Sandro Mamukelashvili | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #154 | Daniel Gafford (Daniel Gafford, Saddiq Bey, Collin Gillespie, Kyle Filipowski, Christian Braun) | Saddiq Bey | #2 · +0.006 | Kyle Filipowski +0.013 |

Advice line (page reading): fired at #34 (Payton Pritchard now, Desmond Bane next turn (81% to survive): +0.057 cats/wk over the pair); #39 (Onyeka Okongwu now, Desmond Bane next turn (37% to survive): +0.012 cats/wk over the pair); #63 (Rudy Gobert now, Zach LaVine next turn (74% to survive): +0.032 cats/wk over the pair); #82 (Isaiah Hartenstein now, Jalen Suggs next turn (74% to survive): +0.033 cats/wk over the pair).

## 4. Where the league-mates' models took the preseason standouts

The owner asked today which preseason performers stood out. The cast prices players from the 10/06 Yahoo file and the board's values, so it has not seen the preseason; a real league-mate who reacts to the box scores would take these men earlier than the models do here. The public rooms of 10/07 and 10/08 are humans who could see the games.

| player | deck rank (v50) | Yahoo ADP 10/06 | this room (cast) | mock 67, public, 10/07 | mock 68, public, 10/08 |
|---|---|---|---|---|---|
| Yaxel Lendeborg | 82 | 115.7 | #106 (David) | #126 | #127 |
| Ty Jerome | 101 | 115.1 | #111 (David) | #107 | #82 (you) |
| Sandro Mamukelashvili | 81 | 119.3 | #135 (David) | #135 (you) | #133 |
| Ryan Rollins | 70 | 76.4 | #64 (Kevin) | #68 | #67 |
| Darryn Peterson | 140 | 103.2 | #105 (Kevin) | #108 | #111 (you) |
| Kel'el Ware | 80 | 75.6 | #68 (Kyle) | #65 | #65 |
| Cameron Boozer | 48 | 55.9 | #46 (Will) | #49 | #61 |
| Aday Mara | 316 | 107.7 | undrafted | undrafted | undrafted |
| Jalen Williams | 16 | 40.4 | #25 (Oblena) | #34 (you) | #39 (you) |
| Tyrese Haliburton | 7 | 14.2 | #8 (JCo) | #15 (you) | #9 |
| Damian Lillard | 88 | 68.3 | #78 (Martin) | #82 (you) | #56 |
| Deni Avdija | 77 | 40.8 | #61 (Hegi) | #43 | #40 |

Late card: 0 unpriced rows across the owner's three turns in rounds 11–13. Repeat-name audit (`m70_repeat_names_audit.json`): the #1 changes at 12 of 13 turns under other rooms' rosters (11 of 13 against an empty roster); Gafford on the Top-5 at 1, Braun 1, Poeltl 0.

## 5. Survival chips and the cast

Survival (`m70_survival.json`): this room 54 rows, predicted 0.562 vs realized 0.630, Brier 0.203; BUY NOW 2 of 6 survived, TOSS-UP 7 of 11, quiet 25 of 37. Pooled 51–70: 1011 rows, Brier 0.240.

| seat | manager | profile lean (market / value) | mean market rank minus pick | mean value rank minus pick | guards / centers | loyalty names on the board | taken by them |
|---|---|---|---|---|---|---|---|
| 1 | Oblena | 0.35 / 0.65 | -4.8 | +13.5 | 7 / 3 | Donovan Mitchell (seat 12) | 0 of 1 |
| 2 | Noah | 0.75 / 0.25 | -13.4 | +14.8 | 4 / 6 | LaMelo Ball (seat 2) | 1 of 1 |
| 3 | Will | 0.55 / 0.45 | -6.6 | +10.1 | 7 / 2 | Onyeka Okongwu (seat 7), Jaden Ivey (undrafted) | 0 of 1 |
| 4 | Robby | 0.70 / 0.30 | -8.9 | +21.8 | 6 / 4 | Jarrett Allen (seat 4), Collin Sexton (undrafted), Devin Booker (seat 4), Devin Vassell (seat 4) | 3 of 3 |
| 5 | Kyle | 0.45 / 0.55 | -2.6 | +14.8 | 7 / 4 | none | 0 of 0 |
| 6 | Martin | 0.45 / 0.55 | -0.4 | +23.3 | 6 / 4 | Luka Doncic (seat 4), Brandon Ingram (seat 3), Jalen Suggs (seat 6) | 1 of 3 |
| 7 | John | 0.50 / 0.50 | -4.3 | +12.5 | 5 / 5 | Tyrese Maxey (seat 7), Jakob Poeltl (seat 7), Jeremy Sochan (undrafted) | 2 of 2 |
| 8 | JCo | 0.45 / 0.55 | -2.4 | +20.4 | 5 / 4 | Tyrese Haliburton (seat 8), Jimmy Butler (undrafted), Nic Claxton (seat 8) | 2 of 2 |
| 9 | Kevin | 0.45 / 0.55 | -2.0 | +9.5 | 9 / 3 | Pascal Siakam (seat 9) | 1 of 1 |
| 10 | David | owner | -0.3 | -9.2 | 5 / 5 | none | — |
| 11 | Cayas | 0.40 / 0.60 | -3.4 | +7.8 | 6 / 5 | none | 0 of 0 |
| 12 | Hegi | 0.65 / 0.35 | -8.2 | +23.0 | 5 / 7 | Immanuel Quickley (seat 12), Andrew Wiggins (seat 12) | 2 of 2 |

loyalty fired on 12 of the 16 loyalty names that were drafted by anyone (undrafted names excluded)

Target-wait (`target_wait_2026-10-08c.json`, mocks 56–70): deep (mkt − pick ≥ 24) — 🎯s passed on 31, still there at the next owner turn 20, at the turn after 6 of 28; mid (12–23) — 🎯s passed on 7, still there at the next owner turn 2, at the turn after 1 of 6; near (< 12) — 🎯s passed on 22, still there at the next owner turn 8, at the turn after 0 of 21.

## Watchlist

- The 9 off-card turns: #10 Giannis Antetokounmpo (card #16), #15 Cooper Flagg (card #8), #34 Trae Young (card #16), #63 Kon Knueppel (card #29), #82 Day'Ron Sharpe (card #6), #87 Myles Turner (card #3), #106 Yaxel Lendeborg (card #3), #111 Ty Jerome (card #10), #154 Saddiq Bey (card #2). The card's man alone at each, with every other pick as drafted: #10 +2.57, #15 -2.37, #34 +3.08, #63 +1.82, #82 -0.37, #87 -0.78, #106 +0.00, #111 +0.00, #154 -0.76 title points; the whole follow-card chain +10.09.
- The preseason standouts (§4): the WO-5 passes on 10/11 and 10/13 (D-1008-3) re-derive their lines; the cast will then price them on the new values.
- The survival chips against the cast (D62-2: leave, log).

## Open-item receipts

| item | query run (2026-10-08) | dated finding |
|---|---|---|
| (this analysis) | machine replay only — no web research in this report | pull receipts for the window live in `after-report-2026-10-08.md` (the morning's pull, same day) |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (after-report-2026-10-08.md, receipts dated 10/8) | all HELD or unsigned on 2026-10-08; nothing changed since |

## Bounds

- A1: the room ran on v50, the version live at the standing URL when it was exported; v49 and v50 share the engine, so the grade reads the same on either.
- Grades are on the v50 lines; the WO-5 refresh will move them.
- A MOCK has no second record; only the owner's picks are an outside input.
- One room is one draw of the bots' seeded noise; the fidelity read is a single sample.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D70-1 | The second cast room on v50 grades 20.68 percent with the card followed at 4 of 13 turns (off the card: #10 Giannis Antetokounmpo (card #16), #15 Cooper Flagg (card #8), #34 Trae Young (card #16), #63 Kon Knueppel (card #29), #82 Day'Ron Sharpe (card #6), #87 Myles Turner (card #3), #106 Yaxel Lendeborg (card #3), #111 Ty Jerome (card #10), #154 Saddiq Bey (card #2)); the follow-card chain grades 30.77 percent. Log it? | log it; no card change |
| D69-1, D68-1..3, D61-4, D67-1..6, D66-1, D-V4-1, D-CAST-1..4, D62-1..3, D-1008-1..3 and earlier | carried | carried |

## Provenance

- Inputs: the owner's exported draft state (pasted 2026-10-08), written in the export's own JSON format to `arena/data/states/draft_state_70.json` (md5 `e55be4f72a1f354c7ad42935f48a551d`); the pool is main `9f54e99`'s data/players.csv, frozen as `arena/results/m68_players_v50.csv`.
- Every figure from `arena/results/m70_*.json` and `target_wait_2026-10-08c.json`; the arms use 18,000 CRN seasons (seeds 11/23/47) on the real eight-team bracket; the deck card and the audit ran the v50 page's own engine under node; §4's prices from `report/market/yahoo-2026-10-06.csv` and the deck board snapshot of the 10/08 pull.
- Not verified: nothing here rests on web research.

## In plain language

**What this was.** Your second practice room tonight against the models of your eleven league-mates, on today's page. It grades 20.7 percent on the real bracket, second of twelve, second in expected weekly category wins, and you took the card's name at 4 of 13 turns.

**What the card left on the table.** Hindsight's best single swap is Desmond Bane at #34, worth about 0.11 categories a week. The advice line spoke at 4 turn(s).

**Following the card.** You took the card's name at 4 of 13 turns. Following it all the way grades 30.8 percent against 20.7 as drafted.

**The preseason names.** The league-mate models haven't seen the preseason, so §4 shows where they took the standouts against where real people took them in the last two public rooms.

**Your decision.** D70-1 log the room (default yes). Everything earlier is carried.
