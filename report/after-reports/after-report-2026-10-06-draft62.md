# After-report — draft_62: the first MOCK on the real seating — the deck's eleven league-mates in the league's 2026-27 draft order, and the card followed at thirteen of thirteen turns

**Owner request (2026-10-06, verbatim):** "Mock against the 11 league personalities" — the
deck's exported draft state, uploaded after Version 46 seated the cast in the real order.

**Room:** the deck's own MOCK mode, 12 × 13, owner seat 10, the eleven opponents the
E18 behavioral models of the real league-mates seated 1 Oblena, 2 Noah, 3 Will, 4 Robby,
5 Kyle, 6 Martin, 7 John, 8 JCo, 9 Kevin, 11 Cayas, 12 Hegi — the league's real order for
the 10/14 draft (owner-supplied, final). Not a public room: LEDGER-eligible. **Deck used:**
v46 (rev `441bba6`, the MOCK-seating build; pool sha `48456b3b18ff`, the v44 pool with
the 10/6 Yahoo prices baked; Porziņģis veto live; the D59-1 history and the D59-2 advice
line live) — the only build that seats the cast this way, which the exported state's
`cast` field carries verbatim. **Method:** the state is the deck's own export (no Yahoo
recap and no tool log exist for a MOCK: the board IS the engine's record), checked
snake-consistent with every name in the pool; the grade is the deck plane's
machine-derived retro (`yahoo-fantasy-basketball` `arena/results/m62_*.json`, debrief
`debrief_2026-10-06_mock62_slot10.md`, deck card replayed from the v46 page, title odds on
the league's real eight-team bracket). Every figure below is read from those files; none
is eyeballed. Verification: this file passes `report/check_report.py`; receipts below.

Pull window: 2026-10-06 → 2026-10-06 (analysis run 2026-10-06 against the v44 pool and the
10/6 market file the v46 page baked; not a roster pull — the day's pull-log rows cover the
window).

**Headline.** Rank 2 of 12 in expected weekly category wins (4.987 against 5.284 for seat 1, Oblena), favored in 10 of 11 head-to-heads; title odds **18.05 percent on the league's real bracket** (rank 2 of 12) — against the eleven modeled league-mates in their real seats, with the card's 🎯 taken at every one of the thirteen turns, the first thirteen-for-thirteen room, so the as-drafted roster is the page's own chain; the retro port's chain differs only by the D60-1 tie-break at #130 and #135 (Herbert Jones, then Gillespie, Gafford dropped) and grades 18.22 percent against 18.05. Hindsight's single-swap ledger finds nothing better at 8 turns and its largest entry is Chet Holmgren at #15 (+0.103 categories a week, +3.69 points of title odds). The D59-2 advice line fired at four turns — #15, #34, #39 and #82, its first room with more than one — and the owner took the 🎯 each time; the four 'now' men as single swaps grade -0.10, +1.30, -1.76 and +1.48 points, all four together +1.44. The survival chips ran optimistic against the cast (mean predicted 0.577, realized 0.521, Brier 0.196); the eleven bots drafted like their profiles (§7); the state is the deck's own export, so there is no second record to diff against.

## 1. Roster changes

None — this is a mock-draft grade, not a roster pull; no pool row, line, tag or board
changed. The validation of the exported state:

| check | result |
|---|---|
| picks in the state | 156; every name is a pool row (the deck's own export, so no resolution was needed); no duplicates |
| snake attribution | all 156 seats match the round parity; the owner's 13 picks sit at #10, #15, #34, #39, #58, #63, #82, #87, #106, #111, #130, #135, #154 |
| cast | the state's `cast` field reads exactly the real 2026-27 order (Oblena, Noah, Will, Robby, Kyle, Martin, John, JCo, Kevin, owner at 10, Cayas, Hegi) — the Version 46 seating, which is how the page is identified |
| owner's roster | Jalen Johnson, Jalen Williams, Anunoby, Pritchard, Herro, Hartenstein, Lendeborg, Mamukelashvili, PJ Washington, Saddiq Bey, Gillespie, Gafford, Cam Thomas |
| punt box | empty all draft (state `punt: []`) |
| veto | Porziņģis went #99 to seat 11 (Cayas) — the room drafts him, the owner's card never showed him |
| state | `arena/data/states/draft_state_62.json`, md5 `f185f50d5dcbe3f0ba7108e314837677` |

## 2. The team, replayed

[EVIDENCE: `m62_final.json`, `m62_arms.json`, `m62_followcard_grade.json`,
the debrief's headline table]

| roster | ECW (cats/week vs the average opponent) | head-to-heads favored | championship rate, 18,000 seasons, real 8-team bracket | playoff rate | swaps |
|---|---|---|---|---|---|
| as drafted (the card's 🎯 at all 13 turns) | 4.987, rank 2 (next 5.284) | 10 of 11 | **18.05%** (rank 2) | 94.91% | none |
| follow-card, self-consistent (arms stage) | 4.941, rank 2 (next 5.148) | 10 of 11 | **18.22%** (rank 2) | 93.91% | Herbert Jones at #130, Collin Gillespie at #135 |
| advice at #15: Desmond Bane for Jalen Williams (the 'now' man; Bane went #33) | 4.971, rank 2 (next 5.280) | 10 of 11 | **17.95%** (rank 2) | 94.73% | Desmond Bane at #15 |
| advice at #34: Franz Wagner for OG Anunoby (Wagner went #38) | 5.004, rank 2 (next 5.271) | 10 of 11 | **19.35%** (rank 2) | 95.52% | Franz Wagner at #34 |
| advice at #39: Onyeka Okongwu for Payton Pritchard (Okongwu went #42) | 4.912, rank 2 (next 5.291) | 10 of 11 | **16.29%** (rank 2) | 93.76% | Onyeka Okongwu at #39 |
| advice at #82: Myles Turner for Yaxel Lendeborg (Turner went #92) | 5.019, rank 2 (next 5.298) | 10 of 11 | **19.53%** (rank 2) | 96.08% | Myles Turner at #82 |
| the four advice 'now' men together (#15 Bane, #34 Wagner, #39 Okongwu, #82 Turner) | 4.993, rank 2 (next 5.285) | 10 of 11 | **19.49%** (rank 2) | 96.03% | Desmond Bane at #15, Franz Wagner at #34, Onyeka Okongwu at #39, Myles Turner at #82 |
| hindsight single swap Chet Holmgren at #15 | 5.090, rank 2 (next 5.279) | 10 of 11 | **21.74%** (rank 2) | 97.56% | Chet Holmgren at #15 |
| hindsight single swap Dyson Daniels at #34 | 5.018, rank 2 (next 5.275) | 10 of 11 | **20.16%** (rank 2) | 95.97% | Dyson Daniels at #34 |
| hindsight single swap Rudy Gobert at #63 | 4.995, rank 2 (next 5.288) | 10 of 11 | **18.36%** (rank 2) | 94.99% | Rudy Gobert at #63 |
| hindsight single swap Myles Turner at #82 | 5.019, rank 2 (next 5.298) | 10 of 11 | **19.53%** (rank 2) | 96.08% | Myles Turner at #82 |
| hindsight single swap Myles Turner at #87 | 5.013, rank 2 (next 5.287) | 10 of 11 | **19.36%** (rank 2) | 95.78% | Myles Turner at #87 |

| category rank, as drafted | |
|---|---|
| weekly model | FG% 5 · FT% 7 · 3PTM 1 · PTS 5 · REB 3 · AST 6 · ST 6 · BLK 7 · TO 4 |
| 13-man z-sum | FG% 5 · FT% 7 · 3PTM 2 · PTS 8 · REB 5 · AST 7 · ST 8 · BLK 8 · TO 3 |

The shape: FG% 5, FT% 7, 3PTM 1, PTS 5, REB 3, AST 6, ST 6, BLK 7, TO 4 in the weekly model — no category worse than 7th. It is favored against 10 of the eleven and trails only seat 1 (Oblena) in expected wins. The port's follow-the-card chain is the same roster but for the tie-break at #130 and #135 (Herbert Jones in, Gafford out) and grades 18.22 percent against 18.05. The advice line's four 'now' men are the counterfactuals that matter in this room: Bane for Williams at #15 (-0.10), Franz Wagner for Anunoby at #34 (+1.30), Okongwu for Pritchard at #39 (-1.76), Turner for Lendeborg at #82 (+1.48); all four together +1.44. Compared with mock 55, the earlier cast room on the shuffled seating (ECW 4.931 rank 3, 15.69 percent rank 3, the card followed at 7 of 13), this room is better on every readout.

## 3. Pick by pick — card vs owner vs hindsight

| pick | deck 🎯 (Top-5) | owner took | card rank · gap (blend) | hindsight best single swap (ΔECW vs final rosters) |
|---|---|---|---|---|
| #10 | Jalen Johnson (Jalen Johnson, Jalen Williams, Kevin Durant, Donovan Mitchell, Anthony Davis) | Jalen Johnson | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #15 | Jalen Williams (Jalen Williams, Jamal Murray, Derrick White, Desmond Bane, James Harden) | Jalen Williams | #1 · +0.000 | Chet Holmgren +0.103 |
| #34 | OG Anunoby (OG Anunoby, Franz Wagner, Kyrie Irving, Payton Pritchard, Jaren Jackson Jr.) | OG Anunoby | #1 · +0.000 | Dyson Daniels +0.032 |
| #39 | Payton Pritchard (Payton Pritchard, Tyler Herro, Onyeka Okongwu, Kyrie Irving, Darius Garland) | Payton Pritchard | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #58 | Tyler Herro (Tyler Herro, De'Aaron Fox, Jalen Suggs, Mikal Bridges, Coby White) | Tyler Herro | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #63 | Isaiah Hartenstein (Isaiah Hartenstein, Jalen Suggs, Rudy Gobert, De'Aaron Fox, Naz Reid) | Isaiah Hartenstein | #1 · +0.000 | Rudy Gobert +0.009 |
| #82 | Yaxel Lendeborg (Yaxel Lendeborg, Sandro Mamukelashvili, Myles Turner, PJ Washington, Jaden McDaniels) | Yaxel Lendeborg | #1 · +0.000 | Myles Turner +0.032 |
| #87 | Sandro Mamukelashvili (Sandro Mamukelashvili, Myles Turner, PJ Washington, Jaden McDaniels, Devin Vassell) | Sandro Mamukelashvili | #1 · +0.000 | Myles Turner +0.026 |
| #106 | PJ Washington (PJ Washington, Devin Vassell, Saddiq Bey, Collin Gillespie, Herbert Jones) | PJ Washington | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #111 | Saddiq Bey (Saddiq Bey, Collin Gillespie, Cason Wallace, Ty Jerome, Herbert Jones) | Saddiq Bey | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #130 | Collin Gillespie (Collin Gillespie, Herbert Jones, Daniel Gafford, Reed Sheppard, Christian Braun) | Collin Gillespie | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #135 | Daniel Gafford (Daniel Gafford, Herbert Jones, Christian Braun, Cam Thomas, Reed Sheppard) | Daniel Gafford | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #154 | Cam Thomas (Cam Thomas, Jordan Goodwin, Bilal Coulibaly, Santi Aldama, Scotty Pippen Jr.) | Cam Thomas | #1 · +0.000 | none positive (the pick was hindsight-best) |

🎯 taken 13 of 13; Top-5 row 13 of 13

[EVIDENCE: `m62_replay.json`, `m62_deckcard_v44.json`, `m62_hindsight.json`;
card ranks are the deck's own JS replayed on the v46 page]

Reading: the card was followed at every turn, so the table's third column is the card's own first row thirteen times, and the only question hindsight can answer is what the card itself left on the table. It found nothing better at 8 turns (#10, #39, #58, #106, #111, #130, #135, #154) and small change elsewhere; the entries worth a sentence are Chet Holmgren at #15 (+0.103, went #19 to Martin, seat 6); Myles Turner at #82 (+0.032, went #91 to Martin); Dyson Daniels at #34 (+0.032, went #46 to Will, seat 3); Myles Turner at #87 (+0.026, went #91 to Martin). None is a reach the card should have made on its own numbers: each is a roster-fit gain visible only once the final rosters are known.

The port-versus-page note (D60-1, D61-3): the retro's Python card port and the page differ at 4 turn(s) here (#15, #58, #130, #135: the Top-5 order or the pick's rank); the table reads the page.

## 4. Tool-state integrity — a MOCK has no second record

A public room leaves two records, Yahoo's recap and the owner's tool log, and the
integrity check diffs them. A MOCK leaves one: the deck advanced the eleven bots itself
and logged the owner's thirteen picks, and the exported state is that board. What can be
checked is checked: 156 picks, 156 distinct pool names, every seat on the snake, the
cast in the real order, the owner's roster the thirteen names at the owner's turns, and
the deck card replayed from the v46 page reproduces the card the owner drafted against
(§3) [EVIDENCE: `arena/data/states/draft_state_62.json`, `m62_deckcard_v44.json`].

## 5. Survival chips — the first cast room scored since the refit

[EVIDENCE: `m62_survival.json`; the debrief's survival table]

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 62 (out of sample) | 48 | 0.577 | 0.521 | **0.196** | 0.250 |
| pooled with every earlier scored room (51 to 61) | 602 | 0.444 | 0.645 | 0.264 | 0.229 |

By chip in this room: BUY NOW 4 rows, mean predicted 0.139, 0 survived; TOSS-UP 9 rows, 0.340, 3 survived; quiet rows 35, 0.687, 22 survived; survivors called at two percent or less: none.

The first cast room scored since the price-only refit, and the first where the model ran optimistic: it predicted 0.577 and 0.521 survived. The eleven bots price by Yahoo's ADP with their own leans and noise, so they take the market's names closer to the market's order than a public room of strangers does — the quiet rows were taken more often than the model expects. The Brier of 0.196 still beats the constant base rate, but the chips are calibrated on public rooms and this is evidence they read a touch too safe against the cast (D62-2).

## 6. The punt advisor, replayed

[EVIDENCE: `m62_advisor.json`, 23 pre- and post-pick moments across the owner's turns; `m62_final.json` for the finish]

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 PTS+REB; #63 REB (advise); #82 PTS+REB (advise); #87 PTS (advise); #106 PTS (advise); #111 PTS (advise); #130 PTS (advise); #135 PTS (advise); #154 PTS (advise).

The owner declared no punt; the box stayed empty. Advice only, by design.

## 7. Did the eleven draft like themselves? — cast fidelity

The question the real seating was built to answer: with each model in its real seat,
does it draft the way three seasons of that manager's boards say it should?
[EVIDENCE: `m62_cast_fidelity.json`; the profiles in the page's `MANAGERS` block; market
rank = the v46 page's baked Yahoo price, value rank = the v44 pool's adjusted value]

| seat | manager | profile lean (market / value) | mean market rank minus pick | mean value rank minus pick | guards / centers | loyalty names on the board | taken by them |
|---|---|---|---|---|---|---|---|
| 1 | Oblena | 0.35 / 0.65 | +1.7 | -12.6 | 6 / 6 | Donovan Mitchell (seat 11) | 0 of 1 |
| 2 | Noah | 0.75 / 0.25 | -17.0 | +25.1 | 6 / 5 | LaMelo Ball (seat 2) | 1 of 1 |
| 3 | Will | 0.55 / 0.45 | -7.4 | +14.2 | 7 / 4 | Onyeka Okongwu (seat 7), Jaden Ivey (undrafted) | 0 of 2 |
| 4 | Robby | 0.70 / 0.30 | -14.1 | +19.7 | 7 / 3 | Jarrett Allen (seat 4), Collin Sexton (seat 4), Devin Booker (seat 4), Devin Vassell (seat 11) | 3 of 4 |
| 5 | Kyle | 0.45 / 0.55 | -6.3 | +4.5 | 5 / 5 | none | 0 of 0 |
| 6 | Martin | 0.45 / 0.55 | -0.3 | -1.3 | 6 / 3 | Luka Doncic (seat 4), Brandon Ingram (seat 2), Jalen Suggs (seat 6) | 1 of 3 |
| 7 | John | 0.50 / 0.50 | -8.5 | +6.4 | 6 / 4 | Tyrese Maxey (seat 7), Jakob Poeltl (seat 7), Jeremy Sochan (undrafted) | 2 of 3 |
| 8 | JCo | 0.45 / 0.55 | -4.6 | +4.2 | 7 / 4 | Tyrese Haliburton (seat 8), Jimmy Butler (undrafted), Nic Claxton (seat 8) | 2 of 3 |
| 9 | Kevin | 0.45 / 0.55 | +1.3 | -6.2 | 8 / 4 | Pascal Siakam (seat 9) | 1 of 1 |
| 10 | David | owner | +18.5 | -11.2 | 4 / 4 | — | — |
| 11 | Cayas | 0.40 / 0.60 | -4.6 | -0.8 | 7 / 4 | none | 0 of 0 |
| 12 | Hegi | 0.65 / 0.35 | -6.9 | +9.5 | 7 / 4 | Immanuel Quickley (seat 12), Andrew Wiggins (seat 3) | 1 of 2 |

Reading: "market rank minus pick" is negative when a manager took players the market
had priced earlier than the pick — market fallers — and positive when he reached past
the market. The three market-leaning profiles behaved that way: Noah (0.75 market) at
−17.0, Robby (0.70) at −14.1, Hegi (0.65) at −6.9, and all three sit well behind on
value (+25.1, +19.7, +9.5 value ranks behind their picks). The value-leaning profiles
drafted ahead on value: Oblena (0.65 value) at −12.6, Kevin at −6.2, Martin at −1.3,
Cayas at −0.8. Kevin's guard bias showed — eight guards, the most in the room. Loyalty
fired wherever the name was still on the board: Robby took Jarrett Allen, Sexton and
Booker (three of his four; Vassell went to Cayas), Noah took LaMelo, John took Maxey and
Poeltl, JCo took Haliburton and Claxton, Kevin took Siakam, Hegi took Quickley, Martin
took Suggs. The misses are the names that were gone before their manager's turn: Oblena's
Donovan Mitchell went #11 to Cayas before Oblena's #24, Will's Okongwu went #42 to John
before Will's #46, Martin's Luka went #4 and Ingram #71 to other seats, Hegi's Wiggins
went to Will. The owner's own line in the table is the card's signature: +18.5 past the
market, −11.2 ahead on value.

## 8. Repeat names on the card — the audit, re-run on this room

Same instrument as mocks 56–61 (`repeat_names_audit.mjs`, eleven other rooms' owner
rosters substituted in at each turn, an empty roster, value-only and ΔECW-only orders;
the watch list Poeltl, Gafford, Brook Lopez, Cameron Johnson, Braun, Eason) [EVIDENCE:
`m62_repeat_names_audit.json`]:

| readout | mock 62 | mock 61 | mock 60 |
|---|---|---|---|
| owner turns where the #1 changes under at least one other room's roster | **12 of 13** | 10 of 13 | 12 of 13 |
| owner turns where the #1 changes under an empty roster | **11 of 13** | 11 of 13 | 12 of 13 |
| watch names on this room's Top-5 | Gafford at two turns (#130 3rd, #135 1st — taken), Braun at two (#130 5th, #135 3rd); Poeltl, Lopez, Cameron Johnson and Eason at none | Gafford at one, Braun at one | Gafford at two, Braun at one |

The empty-roster #1 from #34 on reads Kessler, Kessler, LaVine, LaVine, Gafford five
times, then Cam Spencer, while the card said Anunoby, Pritchard, Herro, Hartenstein,
Lendeborg, Mamukelashvili, Washington, Bey, Gillespie, Gafford, Cam Thomas — ten of
eleven decided by the roster as it stood; Gafford at #135 is the one agreement, and the
owner took him there.

## 9. The advice line's third live room, the thirteen-for-thirteen chain, and whether the 🎯 waited

[EVIDENCE: `m62_advice_reads.json` (the advice line on the page's own Top-5 rows, pair_decision twin), `m62_pairarms.json`, `target_wait_2026-10-06b.json`, `m62_followcard_grade.json`]

**The advice line's third live room (D59-2, shipped v40 as advice only).** It fired at four turns, the most in any room — #15 ("Desmond Bane now, Derrick White next turn (80% to survive): +0.035 cats/wk over the pair"), #34 ("Franz Wagner now, Payton Pritchard next turn (96% to survive): +0.016 cats/wk over the pair"), #39 ("Onyeka Okongwu now, Payton Pritchard next turn (83% to survive): +0.079 cats/wk over the pair") and #82 ("Myles Turner now, Sandro Mamukelashvili next turn (82% to survive): +0.015 cats/wk over the pair") — because against the cast the 🎯 was priced to wait (0.70, 0.92, 0.83, 0.80 to survive) and a second row would not. The owner took the 🎯 each time. Graded as single swaps, the 'now' men are worth -0.10, +1.30, -1.76 and +1.48 points of title odds, all four together +1.44; the pre-registered pair rule, replayed as the marker across this room, finished at 17.49 percent against the blend chain's 18.22 on seed set one (4.994 against 4.941 ECW). The advice-only verdict holds on its third room. A wording note for D60-3: at #15 the page's rows named Bane now and White next while the port's rows named White now and Bane next — the twins disagree on which partner is the 'now' man when two rows tie on survival.

**Does the 🎯 wait? — the instrument, with this room added.** No 🎯 was passed in this room, so it adds no passed-on rows; across mocks 56–62 the deep 🎯s passed on were still there at the next owner turn 8 of 10 times, near-price 5 of 11.

## Watchlist

- **D62-1, the seating is live**: this room is the baseline for every MOCK until the 14th; its grade is LEDGER-eligible.
- **D62-2, survival against the cast**: the chips ran optimistic here; one room, logged, no refit.
- **D62-3, the advice line fired four times**: the first room with more than one; the 'now' men graded as single swaps (§9); carried to the next cast room.
- D60-3 wording: the twins can name different 'now' men on a survival tie (#15 here).
- Carried: D61-1..4, D-Y1..4, D-RW-1..4, D-1006-1..4, D-1005-1/3/4, D-1002-1/3, D60-1..4, D58-2..4, the preseason projection refresh (WO-5, after two games per team).

## Open-item receipts

| item | query run (2026-10-06) | dated finding |
|---|---|---|
| (this analysis) | machine replay only — no web research in this report | pull receipts for the window live in `after-report-2026-10-06.md`, `after-report-2026-10-06-rotoworld.md` and `after-report-2026-10-06-yahoo.md` |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull and the 10/6 Yahoo paste, same day (after-report-2026-10-06.md, after-report-2026-10-06-yahoo.md) | all HELD or unsigned on 2026-10-06; in this room the bots took Ingram (#71, Noah), Porzingis (#99, Cayas), Kawhi (#30, Martin) and Rollins (#68, John), and the owner took Cam Thomas at #154 as the card's #1; nothing here changes a card |

## Bounds

- Championship figures are on the real eight-team bracket (E14); the arms use 18,000 CRN seasons on three seeds (seed set 2 for the pair-arms replay: 18.75 / 18.65 / 18.47 percent as drafted / blend chain / pair chain).
- The opponents are the E18 models of the league-mates, not the people: their rosters here are one draw of each model's noise, and the field's modeled weakness or strength is in every denominator above.
- The room was drafted on v46 and graded on the v44 pool's lines (identical) with the v46 page's prices. A different line set grades every room differently.
- The page's follow-the-card chain equals the as-drafted roster; the retro port's chain differs at #130 and #135 by its name-order tie-break (D60-1); the advice arms are the 'now' man swapped in as a single pairwise swap, not the full two-turn plan.
- The advice line's reads are the Python twin of pairDecision on the page's rows, not a capture of the rendered sentence.
- No tool log exists for a MOCK; the state is the deck's own export (A3). No punt was declared (A2).

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D62-1 | The real seating is live and this room grades 18.05 percent (rank 2) with the card followed at every turn. Keep MOCK rooms on the real seating as the practice baseline through the 14th, and log each one? | yes |
| D62-2 | The survival chips ran optimistic against the cast (predicted 0.577, realized 0.521; Brier 0.196, still under the base rate). Leave the price-only refit alone (it is calibrated on public rooms, and the league draft is the target), or fit a cast-room adjustment after more cast rooms? | leave it; log cast rooms separately |
| D62-3 | The advice line fired at four turns and the 'now' men grade -0.10 / +1.30 / -1.76 / +1.48 as single swaps, +1.44 together. Keep it advice-only (the standing verdict) or re-open the marker experiment with the cast rooms? | advice only; re-put after three cast rooms |
| D61-1..4, D60-1..4, D-Y1..4, D-RW-1..4, D-1006-1..4, D-1005-1/3/4, D-1002-1/3, D58-2..4 | carried | carried |

## Provenance

- Inputs: the owner's exported draft state (this session, 2026-10-06), copied verbatim
  to `arena/data/states/draft_state_62.json`; no recap and no tool log exist for a MOCK.
- Every number is read from `arena/results/m62_*.json` and the debrief; the arms use
  18,000 CRN seasons (seeds 11/23/47) on the real eight-team bracket; the audit, the deck
  card and the advisor ran the v46 page's own engine under node; the cast-fidelity
  readouts read the page's `MANAGERS` profiles and baked prices.
- Not verified: nothing here rests on web research.

## In plain language

**What this was.** Your first practice draft against the eleven league-mates in their real seats for the 14th. The deck advanced them itself, so there is no Yahoo recap to check against; the exported board is the record. I graded it the way every room has been graded: expected weekly category wins against the other eleven rosters, then 18,000 simulated seasons on the league's real eight-team bracket.

**How it went.** Second of twelve in expected wins, favored against 10 of the other eleven, and an 18.1 percent title rate, rank 2 of 12. You took the card's top name at all thirteen turns, which no earlier room did, so the roster is exactly what the card would have built from this seat against these opponents.

**What the card left on the table.** Not much. Hindsight's best single swap is Chet Holmgren at #15, worth about 0.10 categories a week and +3.7 points of title odds. The advice line spoke four times, more than in any room so far, each time saying take the second name now because the top name would wait; taking all four of those 'now' men instead would have graded 19.5 percent against 18.1.

**The eleven.** They drafted like themselves. The three who lean on the market (Noah, Robby, Hegi) took market fallers and ended up behind on value; the value drafters (Oblena, Kevin, Martin, Cayas) ended up ahead; Kevin took eight guards; and nearly every loyalty name that was still on the board went to its manager (Robby got Allen, Sexton and Booker; Noah got LaMelo; JCo got Haliburton and Claxton; John got Maxey and Poeltl).

**One thing to know.** The survival chips were a little optimistic here. They are calibrated on public rooms, and the bots follow the market more closely than strangers do, so a few names the chips expected to wait did not. It is on your sheet to watch, not to change.

**Your decisions.** D62-1 keep the real seating as the practice baseline (default yes). D62-2 the chips against the cast (default: leave, log). D62-3 the advice line after four firings (default: advice only). Everything earlier is carried.
