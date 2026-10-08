# After-report — draft_69: the first MOCK on v50 against the league-mates' models — the card followed at 12 of 13 turns

**Owner request (2026-10-08):** an exported draft state (`draft_state_56.json`) uploaded without comment, after the preseason-standouts questions — graded as mock 69, the standing practice-room protocol.

**Room:** the deck's own MOCK mode, 12 × 13, owner seat 10, the eleven opponents the E18 behavioral models of the real league-mates in the league's real order (1 Oblena, 2 Noah, 3 Will, 4 Robby, 5 Kyle, 6 Martin, 7 John, 8 JCo, 9 Kevin, 11 Cayas, 12 Hegi). Not a public room: LEDGER-eligible. **Deck used:** v50 (rev `9f54e99`, live at the standing URL from 15:15 UTC; the 10/08 pull's build — notes and Hawkins's team, no line, tag or card change; engine identical to v49; Porziņģis veto live) (A1). **Method:** the state is the deck's own export (no Yahoo recap and no tool log exist for a MOCK), checked snake-consistent with every name in the v50 pool and the `cast` field equal to the real order; the grade is the deck plane's machine-derived retro (`arena/results/m69_*.json`; deck card replayed from the v50 page; title odds on the league's real eight-team bracket). Every figure below is read from those files. Verification: this file passes `report/check_report.py` and the deck's `judgment_open_items.py --check-report`.

Pull window: 2026-10-08 → 2026-10-08 (analysis only, the third report of the day; no roster pull).

**Headline.** As drafted **27.51 percent** on the real bracket (rank 1 of 12), expected weekly category wins 5.228, rank 1 of 12 (next 5.058), favored in 10 of 11 head-to-heads; the card's 🎯 taken at 12 of 13 turns, a Top-5 row at 13 of 13 (off the card: #15 James Harden (card #5)); the self-consistent follow-card chain from the same seat grades 26.58 percent. Category shape: FT%, 3PTM, ST, TO in the top three of the weekly model, PTS, AST ninth or lower. Hindsight's best single swap is Franz Wagner at #34 (+0.071 a week).

## 1. Roster changes

None — a MOCK room; no pull, no row moved on either plane.

## 2. The team, replayed

| arm | ECW (rank; next) | favored | title odds (rank) |
|---|---|---|---|
| as drafted (the card's 🎯 at 12 of 13 turns) | 5.228 (rank 1; next 5.058) | 10 of 11 | 27.51% (rank 1) |
| follow-card, self-consistent (arms stage) | 5.179 (rank 1; next 5.077) | 10 of 11 | 26.58% (rank 1) |
| 🎯 at #15: Jamal Murray for James Harden (card #5; Jamal Murray went #16) | 5.179 (rank 1; next 5.077) | 10 of 11 | 26.58% (rank 1) |
| advice at #34: Desmond Bane for OG Anunoby (the 'now' man; Desmond Bane went #38) | 5.284 (rank 1; next 5.059) | 11 of 11 | 29.73% (rank 1) |
| advice at #63: Mikal Bridges for Jalen Suggs (the 'now' man; Mikal Bridges went #82) | 5.228 (rank 1; next 5.058) | 10 of 11 | 27.51% (rank 1) |
| the 2 advice 'now' men together (#34 Bane, #63 Bridges) | 5.284 (rank 1; next 5.059) | 11 of 11 | 29.73% (rank 1) |
| hindsight single swap Chet Holmgren at #15 | 5.242 (rank 1; next 5.063) | 10 of 11 | 30.66% (rank 1) |
| hindsight single swap Franz Wagner at #34 | 5.299 (rank 1; next 5.056) | 11 of 11 | 29.99% (rank 1) |
| hindsight single swap Dyson Daniels at #39 | 5.238 (rank 1; next 4.864) | 11 of 11 | 30.36% (rank 1) |
| hindsight single swap Paolo Banchero at #63 | 5.247 (rank 1; next 5.055) | 11 of 11 | 27.69% (rank 1) |
| hindsight single swap Draymond Green at #106 | 5.230 (rank 1; next 5.064) | 10 of 11 | 28.98% (rank 1) |
| hindsight single swap Draymond Green at #111 | 5.241 (rank 1; next 5.063) | 11 of 11 | 28.88% (rank 1) |
| hindsight single swap Cason Wallace at #130 | 5.240 (rank 1; next 5.065) | 11 of 11 | 29.04% (rank 1) |

Category ranks (weekly model): FG% 5 · FT% 3 · 3PTM 3 · PTS 10 · REB 5 · AST 11 · ST 2 · BLK 5 · TO 3.

## 3. Pick by pick — card vs owner vs hindsight

| pick | deck 🎯 (Top-5) | owner took | card rank · gap (blend) | hindsight best single swap (ΔECW vs final rosters) |
|---|---|---|---|---|
| #10 | Karl-Anthony Towns (Karl-Anthony Towns, Anthony Davis, Kevin Durant, Jalen Williams, Chet Holmgren) | Karl-Anthony Towns | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #15 | Jamal Murray (Jamal Murray, Jalen Williams, Derrick White, Austin Reaves, James Harden) | James Harden | #5 · +0.013 | Chet Holmgren +0.014 |
| #34 | OG Anunoby (OG Anunoby, Desmond Bane, Franz Wagner, Dyson Daniels, Kyrie Irving) | OG Anunoby | #1 · +0.000 | Franz Wagner +0.071 |
| #39 | Onyeka Okongwu (Onyeka Okongwu, Kyrie Irving, Tyler Herro, Payton Pritchard, Brandon Miller) | Onyeka Okongwu | #1 · +0.000 | Dyson Daniels +0.009 |
| #58 | Payton Pritchard (Payton Pritchard, De'Aaron Fox, Mikal Bridges, Jalen Suggs, Coby White) | Payton Pritchard | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #63 | Jalen Suggs (Jalen Suggs, Mikal Bridges, Coby White, Ryan Rollins, Josh Hart) | Jalen Suggs | #1 · +0.000 | Paolo Banchero +0.019 |
| #82 | Mikal Bridges (Mikal Bridges, Josh Hart, Isaiah Hartenstein, Yaxel Lendeborg, Day'Ron Sharpe) | Mikal Bridges | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #87 | Josh Hart (Josh Hart, Isaiah Hartenstein, Day'Ron Sharpe, Yaxel Lendeborg, PJ Washington) | Josh Hart | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #106 | Yaxel Lendeborg (Yaxel Lendeborg, Daniel Gafford, PJ Washington, Sandro Mamukelashvili, Herbert Jones) | Yaxel Lendeborg | #1 · +0.000 | Draymond Green +0.002 |
| #111 | PJ Washington (PJ Washington, Daniel Gafford, Sandro Mamukelashvili, Herbert Jones, Aaron Gordon) | PJ Washington | #1 · +0.000 | Draymond Green +0.013 |
| #130 | Sandro Mamukelashvili (Sandro Mamukelashvili, Cason Wallace, Daniel Gafford, Herbert Jones, Devin Vassell) | Sandro Mamukelashvili | #1 · +0.000 | Cason Wallace +0.012 |
| #135 | Daniel Gafford (Daniel Gafford, Herbert Jones, Devin Vassell, Cason Wallace, Saddiq Bey) | Daniel Gafford | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #154 | Collin Gillespie (Collin Gillespie, Herbert Jones, Saddiq Bey, Reed Sheppard, Christian Braun) | Collin Gillespie | #1 · +0.000 | none positive (the pick was hindsight-best) |

Advice line (page reading): fired at #34 (Desmond Bane now, Franz Wagner next turn (80% to survive): +0.017 cats/wk over the pair); #63 (Mikal Bridges now, Josh Hart next turn (69% to survive): +0.012 cats/wk over the pair).

## 4. Where the league-mates' models took the preseason standouts

The owner asked today which preseason performers stood out. The cast prices players from the 10/06 Yahoo file and the board's values, so it has not seen the preseason; a real league-mate who reacts to the box scores would take these men earlier than the models do here. The public rooms of 10/07 and 10/08 are humans who could see the games.

| player | deck rank (v50) | Yahoo ADP 10/06 | this room (cast) | mock 67, public, 10/07 | mock 68, public, 10/08 |
|---|---|---|---|---|---|
| Yaxel Lendeborg | 82 | 115.7 | #106 (David) | #126 | #127 |
| Ty Jerome | 101 | 115.1 | #120 (Oblena) | #107 | #82 (you) |
| Sandro Mamukelashvili | 81 | 119.3 | #130 (David) | #135 (you) | #133 |
| Ryan Rollins | 70 | 76.4 | #81 (Kevin) | #68 | #67 |
| Darryn Peterson | 140 | 103.2 | #108 (Hegi) | #108 | #111 (you) |
| Kel'el Ware | 80 | 75.6 | #80 (JCo) | #65 | #65 |
| Cameron Boozer | 48 | 55.9 | #48 (Oblena) | #49 | #61 |
| Aday Mara | 316 | 107.7 | undrafted | undrafted | undrafted |
| Jalen Williams | 16 | 40.4 | #20 (Kyle) | #34 (you) | #39 (you) |
| Tyrese Haliburton | 7 | 14.2 | #8 (JCo) | #15 (you) | #9 |
| Damian Lillard | 88 | 68.3 | #77 (Kyle) | #82 (you) | #56 |
| Deni Avdija | 77 | 40.8 | #65 (JCo) | #43 | #40 |

Late card: 0 unpriced rows across the owner's three turns in rounds 11–13. Repeat-name audit (`m69_repeat_names_audit.json`): the #1 changes at 12 of 13 turns under other rooms' rosters (10 of 13 against an empty roster); Gafford on the Top-5 at 4, Braun 1, Poeltl 0.

## 5. Survival chips and the cast

Survival (`m69_survival.json`): this room 48 rows, predicted 0.564 vs realized 0.625, Brier 0.219; BUY NOW 1 of 6 survived, TOSS-UP 5 of 8, quiet 24 of 34. Pooled 51–69: 957 rows, Brier 0.242.

| seat | manager | profile lean (market / value) | mean market rank minus pick | mean value rank minus pick | guards / centers | loyalty names on the board | taken by them |
|---|---|---|---|---|---|---|---|
| 1 | Oblena | 0.35 / 0.65 | -2.3 | +7.2 | 6 / 6 | Donovan Mitchell (seat 11) | 0 of 1 |
| 2 | Noah | 0.75 / 0.25 | -15.1 | +25.3 | 3 / 8 | LaMelo Ball (seat 2) | 1 of 1 |
| 3 | Will | 0.55 / 0.45 | -7.7 | +26.5 | 7 / 4 | Onyeka Okongwu (seat 10), Jaden Ivey (undrafted) | 0 of 1 |
| 4 | Robby | 0.70 / 0.30 | -10.6 | +11.0 | 7 / 4 | Jarrett Allen (seat 4), Collin Sexton (seat 4), Devin Booker (seat 4), Devin Vassell (seat 4) | 4 of 4 |
| 5 | Kyle | 0.45 / 0.55 | -1.6 | +0.0 | 6 / 3 | none | 0 of 0 |
| 6 | Martin | 0.45 / 0.55 | -5.8 | +11.5 | 6 / 3 | Luka Doncic (seat 4), Brandon Ingram (seat 2), Jalen Suggs (seat 10) | 0 of 3 |
| 7 | John | 0.50 / 0.50 | -5.6 | +9.5 | 6 / 4 | Tyrese Maxey (seat 6), Jakob Poeltl (seat 7), Jeremy Sochan (undrafted) | 1 of 2 |
| 8 | JCo | 0.45 / 0.55 | -4.4 | +19.9 | 5 / 6 | Tyrese Haliburton (seat 8), Jimmy Butler (undrafted), Nic Claxton (seat 8) | 2 of 2 |
| 9 | Kevin | 0.45 / 0.55 | -3.4 | +3.2 | 8 / 2 | Pascal Siakam (seat 3) | 0 of 1 |
| 10 | David | owner | +8.6 | -19.5 | 5 / 5 | none | — |
| 11 | Cayas | 0.40 / 0.60 | -0.9 | +24.5 | 8 / 3 | none | 0 of 0 |
| 12 | Hegi | 0.65 / 0.35 | -8.4 | +24.2 | 7 / 4 | Immanuel Quickley (seat 12), Andrew Wiggins (seat 1) | 1 of 2 |

loyalty fired on 9 of the 17 loyalty names that were drafted by anyone (undrafted names excluded)

Target-wait (`target_wait_2026-10-08b.json`, mocks 56–69): deep (mkt − pick ≥ 24) — 🎯s passed on 25, still there at the next owner turn 15, at the turn after 3 of 22; mid (12–23) — 🎯s passed on 6, still there at the next owner turn 2, at the turn after 1 of 5; near (< 12) — 🎯s passed on 21, still there at the next owner turn 8, at the turn after 0 of 20.

## Watchlist

- Harden at #15 off the card (card #5); one turn, logged.
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
| D69-1 | The first cast room on v50 grades 27.51 percent with the card followed at 12 of 13 turns (#15 James Harden (card #5) the exception). Log it? | log it; no card change |
| D68-1..3, D61-4, D67-1..6, D66-1, D-V4-1, D-CAST-1..4, D62-1..3, D-1008-1..3 and earlier | carried | carried |

## Provenance

- Inputs: the owner's exported draft state (uploaded 2026-10-08), copied verbatim to `arena/data/states/draft_state_69.json` (md5 `899ff83b23b415fee14e7c282096f029`); the pool is main `9f54e99`'s data/players.csv, frozen as `arena/results/m68_players_v50.csv`.
- Every figure from `arena/results/m69_*.json` and `target_wait_2026-10-08b.json`; the arms use 18,000 CRN seasons (seeds 11/23/47) on the real eight-team bracket; the deck card and the audit ran the v50 page's own engine under node; §4's prices from `report/market/yahoo-2026-10-06.csv` and the deck board snapshot of the 10/08 pull.
- Not verified: nothing here rests on web research.

## In plain language

**What this was.** A practice room against the models of your eleven league-mates, on today's page. It grades 27.5 percent on the real bracket, first of twelve, first in expected weekly category wins, and you took the card's name at 12 of 13 turns.

**What the card left on the table.** Hindsight's best single swap is Franz Wagner at #34, worth about 0.07 categories a week. The advice line spoke at 2 turn(s).

**The preseason names.** The league-mate models haven't seen the preseason, so §4 shows where they took the standouts against where real people took them in the last two public rooms.

**Your decision.** D69-1 log the room (default yes). Everything earlier is carried.
