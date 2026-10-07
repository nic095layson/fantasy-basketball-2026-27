# After-report — draft_67: the eleventh live-human room from the REAL slot 10, the first on deck v49 — the card followed at nine of thirteen turns, the 4 misses in rounds 6 to 10

**Owner request (2026-10-07, verbatim):** "Here is a live pick by pick draft for your analysis." — the deck tool's pick-by-pick feed (LIVE mode) and Yahoo's recap, pasted after the mock 66 grade the same evening.

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (the real league slot; random humans — a practice rep, not opponent intel; the twelve display names — 1 Deniz, 2 Sammy, 3 Danny W., 4 Gon, 5 Deki, 6 Alfonso Luis, 7 Jeff, 8 Dino, 9 Gerren, 10 David, 11 Jai, 12 Ben — are not the league's). **Deck used:** v49 (rev `269c522`, the fixes build: the round-11 priced-only card, the re-derived Castle/Barrett lines, the four unsigned men excluded; Porziņģis veto live) — proved by the replay itself: the v49 page's own echo code re-emitted the owner's four "off the card" lines identically (#63 Zubac rank 2, 0.008 behind OG Anunoby; #82 Lillard rank 41, 0.163 behind De'Aaron Fox; #87 Harper rank 58, 0.255 behind De'Aaron Fox; #111 DeRozan rank 48, 0.232 behind PJ Washington), rank, three-decimal gap and 🎯 alike. **Method:** the recap was resolved to pool names by the tracker's own resolver (156 of 156), the state checked snake-consistent and against the tool log's board (simulated from its 167 events); the tool log replayed through the real page in headless Chromium; the grade is the deck plane's machine-derived retro (`yahoo-fantasy-basketball` `arena/results/m67_*.json`, debrief `debrief_2026-10-07_mock67_slot10.md`, deck card replayed from the v49 page, title odds on the league's real eight-team bracket). Every figure below is read from those files; none is eyeballed. Verification: this file passes `report/check_report.py` and the deck's `judgment_open_items.py --check-report`.

Pull window: 2026-10-07 → 2026-10-07 (analysis only, the fifth report of the day; not a roster pull — the morning's pull-log row covers the window).

**Headline.** Rank 2 of 12 in expected weekly category wins (5.015 against 5.129 for seat 4, Gon), favored in 9 of 11 head-to-heads; title odds **17.51 percent on the league's real bracket** (rank 2 of 12), with the card followed at 9 of 13 turns (mock 61's count). The 4 misses: Ivica Zubac at #63 (card #2, 0.008 behind OG Anunoby, who went #69 to seat 4 (Gon); the 🎯 alone +1.14 title points); Damian Lillard at #82 (card #41, 0.163 behind De'Aaron Fox, who went #92 to seat 5 (Deki); the 🎯 alone +6.53 title points); Dylan Harper at #87 (card #58, 0.255 behind De'Aaron Fox, who went #92 to seat 5 (Deki); the 🎯 alone +6.44 title points); DeMar DeRozan at #111 (card #48, 0.232 behind PJ Washington, who went #130 to seat 10 (David); the 🎯 alone +0.00 title points). Following the card's chain self-consistently grades 37.51 percent (OG Anunoby at #63, De'Aaron Fox at #82, Isaiah Hartenstein at #87, Yaxel Lendeborg at #111). The D59-2 advice line stayed silent at every turn, for the stated reasons. The survival chips scored a Brier of 0.186 against a 0.242 base rate; the draft room's positions matched the pool on all 156 picks for the third room running; the tool log — three inserts, two namesake halts, four undos and an UNKNOWN fix among its 167 events — replayed on the real page with zero drift. Two findings on the instruments: the deck-card replayer did not apply the page's round-11 priced-only rule (fixed here, red-first; mock 66's record corrected), and the history box re-renders an undone pick's line as its replacement after a later insert (display only, D67-4).

## 1. Roster changes

None — this is a mock-draft grade, not a roster pull; no pool row, line, tag or board changed. The validation of the room against Yahoo's recap:

| check | result |
|---|---|
| picks in the recap | 156; all 156 "Last, First" lines resolved to a pool name by the tracker's resolver (diacritics, suffixes, "P.J." included); no UNKNOWN |
| snake attribution | all 156 seats match the round parity; the owner's 13 picks sit at #10, #15, #34, #39, #58, #63, #82, #87, #106, #111, #130, #135, #154 |
| owner's roster | Karl-Anthony Towns, Tyrese Haliburton, Jalen Williams, Derrick White, Desmond Bane, Ivica Zubac, Damian Lillard, Dylan Harper, Zach LaVine, DeMar DeRozan, PJ Washington, Sandro Mamukelashvili, Devin Vassell — identical to the recap's "My Team" |
| cast | seats 1–12: Deniz, Sammy, Danny W., Gon, Deki, Alfonso Luis, Jeff, Dino, Gerren, **David (10)**, Jai, Ben |
| tool board vs recap | the tracker's final board (after three inserts, four undos and the UNKNOWN fix) matches the recap pick for pick, 156 of 156 |
| positions shown by the draft room vs the pool | **0 of 156 differ**, teams 0 of 156 — the third room in a row where the room and the pool match on every drafted man (see §7) |
| state | `arena/data/states/draft_state_67.json`, md5 `c18bae2654100c24ae9fe17b4d99ebd7` |

## 2. The team, replayed

[EVIDENCE: `m67_final.json`, `m67_arms.json`, `m67_followcard_grade.json`, the debrief's headline table]

| roster | ECW (cats/week vs the average opponent) | head-to-heads favored | championship rate, 18,000 seasons, real 8-team bracket | playoff rate | swaps |
|---|---|---|---|---|---|
| as drafted (the card's 🎯 at 9 of 13 turns) | 5.015, rank 2 (next 5.129) | 9 of 11 | **17.51%** (rank 2) | 97.12% | none |
| follow-card, self-consistent (arms stage) | 5.669, rank 1 (next 5.067) | 11 of 11 | **37.51%** (rank 1) | 99.98% | OG Anunoby at #63, De'Aaron Fox at #82, Isaiah Hartenstein at #87, Yaxel Lendeborg at #111 |
| 🎯 at #63: OG Anunoby for Ivica Zubac (card #2; OG Anunoby went #69) | 4.980, rank 2 (next 5.079) | 9 of 11 | **18.65%** (rank 2) | 97.44% | OG Anunoby at #63 |
| 🎯 at #82: De'Aaron Fox for Damian Lillard (card #41; De'Aaron Fox went #92) | 5.255, rank 1 (next 5.131) | 11 of 11 | **24.04%** (rank 1) | 99.34% | De'Aaron Fox at #82 |
| 🎯 at #87: De'Aaron Fox for Dylan Harper (card #58; De'Aaron Fox went #92) | 5.249, rank 1 (next 5.129) | 10 of 11 | **23.95%** (rank 1) | 99.33% | De'Aaron Fox at #87 |
| 🎯 at #111: PJ Washington for DeMar DeRozan (card #48; PJ Washington went #130) | 5.015, rank 2 (next 5.129) | 9 of 11 | **17.51%** (rank 2) | 97.12% | PJ Washington at #111 |
| hindsight single swap Chet Holmgren at #10 | 5.037, rank 2 (next 5.041) | 10 of 11 | **18.78%** (rank 2) | 97.69% | Chet Holmgren at #10 |
| hindsight single swap Chet Holmgren at #15 | 5.178, rank 1 (next 5.102) | 10 of 11 | **22.16%** (rank 2) | 98.94% | Chet Holmgren at #15 |
| hindsight single swap Domantas Sabonis at #34 | 5.069, rank 2 (next 5.136) | 10 of 11 | **18.82%** (rank 2) | 97.92% | Domantas Sabonis at #34 |
| hindsight single swap OG Anunoby at #58 | 5.021, rank 2 (next 5.103) | 9 of 11 | **17.78%** (rank 2) | 97.03% | OG Anunoby at #58 |
| hindsight single swap De'Aaron Fox at #82 | 5.255, rank 1 (next 5.131) | 11 of 11 | **24.04%** (rank 1) | 99.34% | De'Aaron Fox at #82 |
| hindsight single swap De'Aaron Fox at #87 | 5.249, rank 1 (next 5.129) | 10 of 11 | **23.95%** (rank 1) | 99.33% | De'Aaron Fox at #87 |
| hindsight single swap Yaxel Lendeborg at #106 | 5.023, rank 2 (next 5.141) | 10 of 11 | **17.13%** (rank 2) | 96.74% | Yaxel Lendeborg at #106 |
| hindsight single swap Daniel Gafford at #111 | 5.219, rank 1 (next 5.138) | 10 of 11 | **22.58%** (rank 2) | 99.16% | Daniel Gafford at #111 |
| hindsight single swap Draymond Green at #135 | 5.027, rank 2 (next 5.124) | 9 of 11 | **18.56%** (rank 2) | 97.33% | Draymond Green at #135 |
| hindsight single swap Kyle Filipowski at #154 | 5.067, rank 2 (next 5.137) | 9 of 11 | **18.25%** (rank 2) | 97.71% | Kyle Filipowski at #154 |

| category rank, as drafted | |
|---|---|
| weekly model | FG% 3 · FT% 2 · 3PTM 2 · PTS 5 · REB 9 · AST 5 · ST 8 · BLK 10 · TO 3 |
| 13-man z-sum | FG% 3 · FT% 2 · 3PTM 2 · PTS 4 · REB 9 · AST 5 · ST 7 · BLK 10 · TO 3 |

The shape: FG%, FT%, 3PTM, TO inside the top three of the weekly model, REB, BLK at 9, 10 — the opposite silhouette to mock 66's points-assists-steals roster (there FG%, FT% and turnovers sat 11th, 12th and 12th). It is favored against 9 of the eleven and trails only seat 4 (Gon: Shai Gilgeous-Alexander, Austin Reaves, Chet Holmgren, Jaren Jackson Jr., Darius Garland, OG Anunoby, Zion Williamson, Mikal Bridges, Miles Bridges, Brandin Podziemski, Jalen Green, Quentin Grimes, Kristaps Porzingis) in expected wins. The follow-the-card chain adds +20.00 title points; the card's own man at each off-card turn, with every other pick as drafted, is worth +6.53 at #82, +6.44 at #87, +1.14 at #63, +0.00 at #111.

## 3. Pick by pick — card vs owner vs hindsight

| pick | deck 🎯 (Top-5) | owner took | card rank · gap (blend) | hindsight best single swap (ΔECW vs final rosters) |
|---|---|---|---|---|
| #10 | Karl-Anthony Towns (Karl-Anthony Towns, Tyrese Maxey, Jalen Johnson, Tyrese Haliburton, Anthony Davis) | Karl-Anthony Towns | #1 · +0.000 | Chet Holmgren +0.022 |
| #15 | Tyrese Haliburton (Tyrese Haliburton, Jalen Williams, Jamal Murray, Derrick White, Kevin Durant) | Tyrese Haliburton | #1 · +0.000 | Chet Holmgren +0.163 |
| #34 | Jalen Williams (Jalen Williams, Derrick White, Dyson Daniels, Desmond Bane, Kyrie Irving) | Jalen Williams | #1 · +0.000 | Domantas Sabonis +0.054 |
| #39 | Derrick White (Derrick White, Desmond Bane, OG Anunoby, Jaren Jackson Jr., Onyeka Okongwu) | Derrick White | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #58 | Desmond Bane (Desmond Bane, OG Anunoby, Payton Pritchard, Ivica Zubac, Tyler Herro) | Desmond Bane | #1 · +0.000 | OG Anunoby +0.006 |
| #63 | OG Anunoby (OG Anunoby, Ivica Zubac, Payton Pritchard, Michael Porter Jr., Tyler Herro) | Ivica Zubac | #2 · +0.008 | none positive (the pick was hindsight-best) |
| #82 | De'Aaron Fox (De'Aaron Fox, Jalen Suggs, Coby White, Zach LaVine, Mikal Bridges) | Damian Lillard | #41 · +0.163 | De'Aaron Fox +0.240 |
| #87 | De'Aaron Fox (De'Aaron Fox, Jalen Suggs, Coby White, Zach LaVine, Mikal Bridges) | Dylan Harper | #58 · +0.255 | De'Aaron Fox +0.234 |
| #106 | Zach LaVine (Zach LaVine, Yaxel Lendeborg, PJ Washington, Sandro Mamukelashvili, Herbert Jones) | Zach LaVine | #1 · +0.000 | Yaxel Lendeborg +0.008 |
| #111 | PJ Washington (PJ Washington, Yaxel Lendeborg, Sandro Mamukelashvili, Herbert Jones, Daniel Gafford) | DeMar DeRozan | #48 · +0.232 | Daniel Gafford +0.204 |
| #130 | PJ Washington (PJ Washington, Sandro Mamukelashvili, Daniel Gafford, Devin Vassell, Saddiq Bey) | PJ Washington | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #135 | Sandro Mamukelashvili (Sandro Mamukelashvili, Saddiq Bey, Devin Vassell, Draymond Green, Tari Eason) | Sandro Mamukelashvili | #1 · +0.000 | Draymond Green +0.012 |
| #154 | Devin Vassell (Devin Vassell, Kyle Filipowski, Nikola Vucevic, Jerami Grant, Aaron Nesmith) | Devin Vassell | #1 · +0.000 | Kyle Filipowski +0.052 |

🎯 taken 9 of 13; Top-5 row 10 of 13

[EVIDENCE: `m67_replay.json`, `m67_deckcard_v49.json`, `m67_hindsight.json`; card ranks are the deck's own JS replayed on the v49 page with the page's round-11 priced-only candidate list; the live echoes at #63 (0.008 behind Anunoby, rank #2), #82 (0.163 behind Fox, rank #41), #87 (0.255 behind Fox, rank #58), #111 (0.232 behind Washington, rank #48) match the replay]

Reading: the card was followed at 9 of thirteen turns; hindsight has nothing to add at #39 and #130; the other followed turns grade +0.022 at #10 (Chet Holmgren), +0.163 at #15 (Chet Holmgren — the one followed turn worth more than a point, +4.65 title points; he went #28 to seat 4), +0.054 at #34 (Domantas Sabonis), +0.006 at #58 (OG Anunoby), +0.008 at #106 (Yaxel Lendeborg), +0.012 at #135 (Draymond Green), +0.052 at #154 (Kyle Filipowski). At #63 the owner took Zubac, card #2 and 0.008 behind Anunoby — a coin-flip row (the first off-card pick inside the Top-5 in a human room since mock 61's Herbert Jones); Anunoby went #69, six picks later, so the chip that gave him 0.24 to survive to #82 was right; the 🎯 alone is worth +1.14 title points in the simulated seasons, while on expected category wins hindsight sides with the owner (Zubac the better man by 0.035 a week; 0 of 248 legal picks grade higher) — a coin flip on either ruler. At #82 the owner took Lillard, card #41 and 0.163 behind Fox — the achilles-risk row (availability 0.78) for the second room running (mock 61, #63, card #65); his market rank is 68, so the price called him value fourteen slots late while the card priced the tag; Fox went #92 and the 🎯 alone is worth +6.53 points; hindsight's best is De'Aaron Fox +0.240 a week (went #92), +6.53 title points. At #87 the owner took Harper, card #58 and 0.255 behind the same Fox, passed a second time with the chip now at 0.14 to survive to #106 — he lasted to #92 only, five picks on; the 🎯 alone is worth +6.44 points; hindsight's best is De'Aaron Fox +0.234 a week (went #92), +6.44 title points. At #111 the owner took DeRozan, card #48 and 0.232 behind Washington, with the round-9+ reminder on the echo; Washington lasted to #130 (the chip said 0.35), where the owner took him, so the single swap is a reorder of the same roster (17.51 percent, as drafted) and what the turn cost is DeRozan's slot: hindsight's best is Daniel Gafford +0.204 a week (went #132), +5.07 title points.

## 4. Tool-state integrity — the deck's board vs the recap, on the v49 page

The owner's tool log was rebuilt as an event list (167 events: 160 feeds, fifteen of them the shared token wherever the echo said "assumed over", "only X left" or "skipped" — fourteen surnames and one first name, Miles; two feeds that halted on the page's namesake guard ("Murray" after #49 with Jamal gone, "Jones" after #135 with Herbert gone — nothing logged by either, the fuller name resent); one UNKNOWN feed, "CMB" at #88, fixed with "88- Collin Murray-Boyles"; three Insert-at-# — Cameron Boozer at #49, Paul George at #70, Quentin Grimes at #141 — each after the next names had already been logged; four undos, each a skipped-pick correction at #62, #75, #89 and #93) and replayed through the real v49 page in headless Chromium [EVIDENCE: `m67_tool_vs_truth.json`, `arena/data/events/m67_tool_events.json`]:

| finding | detail |
|---|---|
| positions differing from the recap | **0 of 156**; owner's roster identical; nothing missing, nothing extra |
| echo lines asserted | 167 of 167 (each feed's resolved name, the fifteen shared-token resolutions, the two halts, the UNKNOWN warning, the fix, the three inserts, the four undos) |
| the page's own off-card echoes | re-emitted at #63, #82, #87 and #111 identical to the owner's paste — the page identification |
| clock text under the feed title | correct after all 167 events |
| page errors | 0 |
| the UNKNOWN at #88 | "CMB" logged the placeholder with the fix hint; the next feed, "Collin Murray-Boyles", did not auto-fix it (the D54-2 matcher compares letters, not initials) and logged him at #89 with the "still UNKNOWN" reminder; an undo and "88- Collin Murray-Boyles" put him at #88 and Derik Queen at #89 — the recap's order |
| the three inserts | Boozer at #49 after Jaylen Brown had been logged there (1 shifted); Paul George at #70 after Reid and Castle (2 shifted); Grimes at #141 after Cameron Johnson, Demin and Acuff (3 shifted); no owner pick moved seats |
| the four undos | each a missed-pick correction: Zubac logged for Seat 11 at #62, taken back, Buzelis #62, Zubac #63 (YOU); Zion for Seat 3 at #75, Herro #75, Zion #76; Murray-Boyles for Seat 8 at #89 (see above); Hartenstein for Seat 4 at #93, Mikal Bridges #93, Hartenstein #94 |
| the history box after the inserts | the four undone picks' lines were re-rendered from the state by the later inserts (D59-1 relabelLog re-renders every pick line), so the log shows the replacement's line twice, e.g. "#62: Matas Buzelis" before and after "undid: Ivica Zubac"; the state was right throughout — a display quirk, D67-4 |
| the resume marker | the log opens with "— resumed: 0 picks logged —" (a page load before pick 1); nothing to replay |

Seventh clean public room in a row on the concise card's page family (mocks 56–61 and 67 drifted none). The halts are the first in a public room since the guard was written: both resolved by the fuller name on the next feed, as designed.

## 5. Survival chips — the fourteenth out-of-sample room for the refit, the eighth human one

[EVIDENCE: `m67_survival.json`; the debrief's survival table]

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 67 (out of sample) | 51 | 0.445 | 0.588 | **0.186** | 0.242 |
| pooled with every earlier scored room (51 to 66) | 858 | 0.477 | 0.624 | 0.247 | 0.235 |

By chip in this room: BUY NOW 9 rows, mean predicted 0.111, 1 survived; TOSS-UP 15 rows, 0.319, 7 survived; quiet rows 27, 0.626, 22 survived; survivors called at two percent or less: none.

Under the constant base rate for this room (0.186 against 0.242); the pooled figure stays over its base. On the 🎯s the owner passed: Anunoby at #63 (0.24, TOSS-UP) went #69, before #82; Fox at #82 (0.39, TOSS-UP) lasted to the next turn; Fox at #87 (0.14, BUY NOW) went #92, before #106; Washington at #111 (0.35, TOSS-UP) lasted to the next turn, #130, where the owner took him. By chip the pattern holds its shape: BUY NOW rows survived 1 of 9 (the model said 0.11), TOSS-UP 7 of 15 (0.32), quiet rows 22 of 27 (0.63).

## 6. The punt advisor, replayed

[EVIDENCE: `m67_advisor.json`; `m67_final.json` for the finish]

Box empty all draft. Room-relative lean at 4 of 11 owner turns: #58 PTS+REB; #130 REB+BLK; #135 BLK (advise); #154 BLK (advise).

The room-relative advisor (D51R-3) read a lean at 4 of the eleven owner turns with a next turn and cleared the two-turn hysteresis at 2 of them — PTS, REB, BLK named — and the owner left the box empty, which is the design (advice only, no button pressed). The finish: REB 9th, BLK 10th in the weekly model; the lean the strip read is the shape the roster took. D61-4 (declare the punt the strip advises, or keep it advice-only) carries.

## 7. The draft room's positions match the pool — 0 of 156, third room running

Mocks 60 and 61 were the first two rooms after the 10/01 position sync (D-ADP-3) where the room's display matched the pool on every drafted man; this room is the third, on both positions and teams [EVIDENCE: `scratchpad m67/positions_check.json`; the recap as pasted]. D60-4 (close D-G3) stands.

## 8. Repeat names on the card — the audit, re-run on this room

Same instrument as mocks 56–66 (`repeat_names_audit.mjs`, sixteen other rooms' owner rosters substituted in at each turn, an empty roster, value-only and ΔECW-only orders; the watch list Gafford, Braun, Poeltl) [EVIDENCE: `m67_repeat_names_audit.json`]:

| readout | mock 67 | mock 66 | mock 61 |
|---|---|---|---|
| owner turns where the #1 changes under at least one other room's roster | **12 of 13** | 12 of 13 | 10 of 13 |
| owner turns where the #1 changes under an empty roster | **10 of 13** | 12 of 13 | 11 of 13 |
| watch names on this room's Top-5 | Gafford at 2 turn(s) (#111, #130); Braun at 0 turn(s); Poeltl at 0 turn(s) | Gafford at one, Braun at none, Poeltl at none | Gafford at one, Braun at one, Poeltl at none |

## 9. The off-card turns, the advice line's third human room, and whether the 🎯 waited

[EVIDENCE: `m67_advice_reads.json` (the advice line on the page's own Top-5 rows, pair_decision twin), `m67_pairarms.json`, `target_wait_2026-10-07e.json`, `m67_followcard_grade.json`]

**The 4 turns.** The grades in §2 say what each one cost on its own: De'Aaron Fox for Damian Lillard at #82 +6.53 points (24.04 percent); De'Aaron Fox for Dylan Harper at #87 +6.44 points (23.95 percent); OG Anunoby for Ivica Zubac at #63 +1.14 points (18.65 percent); PJ Washington for DeMar DeRozan at #111 +0.00 points (17.51 percent). 1 of the 4 🎯s was recovered later by the owner (Washington at #130); Fox was passed twice and went #92, five picks after the second pass; Anunoby went #69, six after the first. The pattern differs from mock 61 (four different men on the roster, none recovered) and from mock 60 (two reorders): here one reorder, one coin flip and two picks at the market's price against the card's.

**The advice line (D59-2, shipped v40 as advice only).** It fired at no turn, on the page's rows or the port's: the 🎯 sat under the 0.60 wait floor at 7 turns (#10, #34, #63, #82, #87, #111, #130 — 'take him now'), and was the best pair at 5 (#15, #39, #58, #106, #135); #154 has no next turn. The pre-registered pair rule, replayed as the marker across this room, finished at 37.51 percent against the blend chain's 37.51 on seed set one (5.669 against 5.669 ECW).

**Does the 🎯 wait? — the instrument, with this room added.** Across mocks 56–67 the 🎯s passed on with a market rank 24 or more slots below the pick were still there at the owner's next turn 14 of 24 times, and two turns on 3 of 21; mid-band (12–23 slots) 2 of 6; near-price 🎯s (under 12 slots) 7 of 17 and 0 of 16. This room added #111 PJ Washington (+38, surv 0.347), went #130; #63 OG Anunoby (+2, surv 0.241), went #69; #82 De'Aaron Fox (−2, surv 0.389), went #92; #87 De'Aaron Fox (−7, surv 0.142), went #92. The deep-band read (the 🎯 usually waits one turn, rarely two) held: Washington at #111, 38 slots under his price, waited to #130; the near-price 🎯s were a mixed read — Anunoby went six picks after the pass; Fox lasted to the next turn, then went five picks after the second pass.

## 10. The fixes in a human room, and the harness gap they exposed

| player | human rooms (of 10) and range | this room | rule in play |
|---|---|---|---|
| Stephon Castle | 10 · 62–84 | #72 (Deniz) | re-derived line (D-CAST-2) |
| RJ Barrett | 10 · 117–140 | #128 (Dino) | re-derived line (D-CAST-2) |
| Davion Mitchell | 10 · 102–129 | #102 (Alfonso Luis) | priced; value axis only |
| Rui Hachimura | 3 · 123–129 | #140 (Deki) | priced; value axis only |
| Dillon Brooks | 8 · 120–153 | undrafted | priced; value axis only |
| Saddiq Bey | 8 · 136–149 | #146 (Sammy) | priced; value axis only |
| Cam Thomas | 0 · — | undrafted | D-CAST-1 (unsigned, excluded) |

Late card on the page: 0 unpriced rows across the owner's three turns in rounds 11–13 (the v49 rule). **The harness gap.** The first replay of this room put Jordan Goodwin on the #154 card — an unpriced man the page could not have shown, because the page ranks the card over `cardPool(pool, round)` from round 11 and the replayer (`live_deckcard.py`) ranked the whole pool. Red-first: the pre-fix replay is kept (`scratchpad m67/m67_deckcard_before.json`, Goodwin second at #154); the fixed replayer removes him, changes no 🎯, and now throws if an unpriced row ever reaches a round-11+ card while the candidate list is all priced. Mock 66 was replayed on the same harness, so its record moved with the fix: VanVleet at #135 is card #19, not #24, and the DEPTH WATCH pin at #135 named him; the room's survival Brier is 0.218 (was 0.205), pooled 0.251 (was 0.250); no arm, no 🎯 and no decision changed. Both records were regenerated and the mock 66 README entry, debrief and report corrected in this PR pair.

## Watchlist

- **D67-1, Lillard at #82 (again)**: card #41 with the achilles-risk tag (availability 0.78), the second room running; the 🎯 alone +6.53 points, hindsight's best De'Aaron Fox +0.240 a week (went #92). D61-1's default (log it; review the tag at the WO-5 refresh with his preseason minutes) carries — this room adds a second data point to the same question.
- **D67-2, Fox passed twice**: the 🎯 at #82 and #87 (0.163 and 0.255 ahead), went #92; the chips read 0.39 then 0.14. The second room where this seat passed the same 🎯 twice (Lendeborg in mock 61).
- **D67-3, DeRozan at #111 over Washington with the round-9+ reminder**: Washington waited to #130 and was taken there; the cost is DeRozan's slot (hindsight's best Daniel Gafford +0.204 a week (went #132)).
- **D67-4, the history box after an undo and a later insert**: an undone pick's line is re-rendered from the state as the replacement's line, so it shows twice (four cases here). Display only; the state, the strip and the recap agreed throughout.
- **D67-5, the "CMB" shorthand**: the D54-2 auto-fix matches letters of a typed name, not initials, so "Collin Murray-Boyles" typed after "CMB" logged a new pick instead of fixing #88; the owner's undo and "88- Name" fixed it in two feeds.
- **D67-6, the deck-card replayer and mock 66's record**: `live_deckcard.py` now ranks the card over the page's `cardPool` (round 11+, priced rows only) with a loud guard; mock 66's deck card, survival, advice reads, follow-card grade and debrief were regenerated and its README entry and report corrected (VanVleet #135 card #19; Brier 0.218 / pooled 0.251). Red-first evidence kept in the scratch (`m67_deckcard_before.json`).
- The D59-4 pattern (White the 🎯 at #39) stayed broken: taken, hindsight best.
- Carried: D66-1 (v49 the practice baseline through the 14th), D-V4-1 and D-CAST-1/2a/2b/3/4, D-C64-1, D62-1..3, D61-1..4 (D61-3 the port's tie-break — the chain in §2 reads the port), D60-2/3/4, D-Y1..4, D-RW-1..4, D-1006-1..4, D-1005-1/3/4, D-1002-1/3, D58-2..4, the league settings screenshot (D-G5), the preseason projection refresh (WO-5, after two games per team).

## Open-item receipts

| item | query run (2026-10-07) | dated finding |
|---|---|---|
| (this analysis) | machine replay only — no web research in this report | pull receipts for the window live in `after-report-2026-10-07.md` (the morning's pull, same day) |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (after-report-2026-10-07.md, ten receipts dated 10/7) | all HELD or unsigned on 2026-10-07; Ingram (#74, seat 2), Porzingis (#148, seat 4), Kawhi (#36, seat 12) and Rollins (#68, seat 5) were drafted by opponents in this room; the four unsigned men were drafted by no one; nothing here changes a card |

## Bounds

- Championship figures are on the real eight-team bracket (E14); the arms use 18,000 CRN seasons on three seeds (seed set 2 for the pair-arms replay: 17.52 / 37.72 / 37.72 percent as drafted / blend chain / pair chain).
- The room was drafted and graded on v49's lines (the two re-derived rows included); the WO-5 refresh will move them.
- The follow-the-card chain is the retro's Python port of the card (name-order tie-break, D61-3); the page's reads are in §3 and §9.
- The advice line's reads are the Python twin of pairDecision on the page's rows, not a capture of the rendered sentence.
- The owner's typed tokens are inferred from the echoes (the shared token where the echo said 'assumed over', 'only X left' or 'skipped'; the halting token from the halt line; the undone feeds from the undo lines; the full name elsewhere) — A1; the replay reproduces every echo, which is the only check the log allows.
- The target-wait table pools seven human rooms and five cast rooms; it says how rooms price the card's deep names, not how the eleven league-mates will.
- The advisor's reads are the replay's read of the engine at each owner turn; the owner's screen at the time is not recorded. No punt was declared (A2).

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D67-1 | Lillard at #82: card #41, 0.163 behind Fox, the achilles-risk row (availability 0.78) taken for the second room running, fourteen slots under his market rank; the 🎯 alone +6.53 title points, hindsight's best De'Aaron Fox +0.240 a week (went #92). Conviction on the return, or should the risk tag move before the 14th? | carried with D61-1: log it as a conviction pick; review the tag at the WO-5 refresh with his preseason minutes |
| D67-2 | Fox: the 🎯 at #82 and #87, passed twice, went #92; the chips read 0.39 then 0.14 to survive. A reason about his line (the Spurs' guard rotation with Harper and Castle) the card is missing, or conviction against him at that slot? | no card change; log the two picks as conviction picks; his minutes are a WO-5 item with the Spurs' preseason box scores |
| D67-3 | DeRozan at #111: card #48, 0.232 behind Washington with the round-9+ reminder; Washington waited to #130 and was taken there, so the turn cost DeRozan's slot (hindsight's best Daniel Gafford +0.204 a week (went #132)). Log it? | log it; no card change |
| D67-4 | The history box re-renders an undone pick's line as its replacement after a later Insert-at-# (four cases in this log). Drop or mark the undone line at undo time so the log reads as it happened? | yes — next deck build, red-first (a test_card fixture on relabelLog after an undo); display only, no grade depends on it |
| D67-5 | "CMB" at #88: the auto-fix matches typed letters, not initials, so the re-typed full name logged a new pick. Add an initials rule to the D54-2 matcher (three capitals matching the three name tokens), or leave the "N- Name" fix as the path? | leave as shipped; the fix path worked in two feeds and an initials rule invites namesake collisions |
| D67-6 | The deck-card replayer ranked the card over the whole pool, not the page's round-11 priced-only list; fixed with a loud guard, mock 66's record regenerated and corrected (no arm, 🎯 or decision moved). Accept the corrected record? | yes — accept; rooms before v48 replay unchanged by construction |
| D66-1, D-V4-1, D-CAST-1..4, D-C64-1, D62-1..3, D61-1..4, D60-2..4, D-Y1..4, D-RW-1..4, D-1006-1..4, D-1005-1/3/4, D-1002-1/3, D58-2..4 | carried | carried |

## Provenance

- Inputs: the owner's tool log and Yahoo recap (this session, 2026-10-07 evening), transcribed verbatim into `arena/data/events/m67_tool_events.json` and the recap into the state by the tracker's resolver (`hoops.py draft resync`); state md5 `c18bae2654100c24ae9fe17b4d99ebd7`.
- Every number is read from `arena/results/m67_*.json`, `target_wait_2026-10-07e.json` and the debrief; the arms use 18,000 CRN seasons (seeds 11/23/47) on the real eight-team bracket; the audit, the deck card, the advisor and the tool replay ran the v49 page's own engine under node and headless Chromium; the human ranges from `dcast_realism_picks_2026-10-07.json`.
- Not verified: nothing here rests on web research.

## In plain language

**What this was.** Your eleventh practice draft from the real seat, the first live one on the page with today's fixes. I rebuilt the room from Yahoo's recap, replayed your tool log through the real page, and graded the roster the way every room has been graded: expected weekly category wins against the eleven other rosters, then 18,000 simulated seasons on the league's real eight-team bracket.

**How it went.** Second of twelve in expected wins, behind Gon's roster at seat 4. The roster is favored against 9 of the other eleven and wins the title in 17.5 percent of seasons, rank 2 of 12, with a 97.1 percent playoff rate. The shape is the mirror image of last night's mock 66 team: FG%, FT%, 3PTM, TO are the strengths, REB, BLK the weakness.

**What you did with the card.** You took the card's top name at 9 of thirteen turns. The four exceptions, in order of what the card's man alone was worth:

- **#82, Damian Lillard.** The card had Fox first and Lillard forty-first, and Lillard's row carries the achilles-risk tag — the same pick you made in mock 61. Fox went #92. The card's man alone: +6.5 points of title odds.
- **#87, Dylan Harper.** Fox again, passed a second time; the chip gave him 0.14 to last to your next turn and he did not. Harper was card #58. The card's man alone: +6.4 points of title odds.
- **#63, Ivica Zubac.** A coin flip against Anunoby (0.008 apart): the simulated seasons give Anunoby a small edge, expected category wins give it to Zubac. Nearly free either way. The card's man alone: +1.1 points of title odds.
- **#111, DeMar DeRozan.** The card had Washington first with the round-9 reminder; he waited to #130 and you took him there, so this one is a reorder that cost DeRozan's slot. The card's man alone: +0.0 points of title odds.

Following the card's whole chain self-consistently grades 37.5 percent against 17.5.

**The advice line.** Silent at every turn, each time for the stated reason (the top name would not wait, or the top name was already the best pair). Nothing to grade. The punt advisor read a lean and you left the box empty, which is how it is built.

**The tool itself.** Your 167 events — three inserts, two halts on a bare surname, four undos and the "CMB" fix — replayed on the real page with zero mismatches, and the page's own echo lines came back identical, which is how I know this was v49. Two things to know: the history box shows an undone pick's line twice after a later insert (display only, D67-4), and typing initials does not fix an UNKNOWN (D67-5). The draft room's positions matched the deck on all 156 players for the third room running.

**One correction.** Grading this room exposed a gap in my replayer, not in your page: it ranked the late card over every player instead of the priced ones the page uses from round 11. Fixed, with a guard that fails loudly. Last night's mock 66 was replayed on the same instrument, so three of its figures moved (VanVleet was card #19 at #135, not #24, and the survival Brier is 0.218, not 0.205); nothing you decided on changes.

**Your decisions.** D67-1 Lillard again (default: carried with D61-1). D67-2 Fox passed twice (default: log, no change). D67-3 DeRozan over Washington (default: log). D67-4 fix the double line in the history box (default: yes, next build). D67-5 an initials rule for UNKNOWN fixes (default: leave as shipped). D67-6 accept the corrected mock 66 record (default: yes). Everything earlier is carried.
