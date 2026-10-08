# After-report — draft_68: the twelfth live-human room from the REAL slot 10, the first on deck v50 — the card followed at nine of thirteen turns; with the owner's two questions answered (why no punt lately; injured men on rival rosters)

**Owner requests (2026-10-08, verbatim):** "Live draft for your analysis:" — the deck tool's pick-by-pick feed (LIVE mode) and Yahoo's recap. Then, during the grade: "How come earlier in September/August, the tool was able to Declare Punts pretty frequently, but now we've gone in a drought since the tool has declared a punt to steer towards. What do you think has changed?" and "Even with Butler, Porzingis, Ingram etc. injured, when an OPPONENT roster drafts them, you still somewhat use them in your categorical calculations correct?"

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (random humans — a practice rep, not opponent intel; display names 1 sean, 2 Alejandro, 3 Sahil, 4 Dody, 5 Charles, 6 Hugo, 7 PJ, 8 GoodWillPunting, 9 Ed, 10 David, 11 alvin, 12 Giannis are not the league's). **Deck used:** v50 (rev `9f54e99`, the 10/08 pull's build: notes and Hawkins's team only — no line, tag or card change; Porziņģis veto live). The page's own echo code re-emitted the owner's four "off the card" lines identically in the replay (#34 White rank 3, 0.011 behind Anthony Davis; #82 Jerome rank 28, 0.117 behind Coby White; #87 McDaniels rank 12, 0.045 behind Mikal Bridges; #111 Peterson rank 33, 0.145 behind Sandro Mamukelashvili); the same log replays identically on v49, which shares the engine, so v50 is graded as the version live at the standing URL when the room ran (A1). **Method:** the recap resolved to pool names by the tracker's own resolver (156 of 156); the tool log replayed through the real page in headless Chromium; the grade is the deck plane's machine-derived retro (`yahoo-fantasy-basketball` `arena/results/m68_*.json`, debrief `debrief_2026-10-08_mock68_slot10.md`), title odds on the league's real eight-team bracket. Every figure below is read from those files. Verification: this file passes `report/check_report.py` and the deck's `judgment_open_items.py --check-report`.

Pull window: 2026-10-08 → 2026-10-08 (analysis only, the second report of the day; not a roster pull — the morning's pull-log row covers the window).

**Headline.** Rank 1 of 12 in expected weekly category wins (5.371 against 5.096 for seat 1, sean), favored in 11 of 11 head-to-heads; title odds **28.36 percent on the league's real bracket** (rank 1 of 12), with the card followed at 9 of 13 turns. The 4 misses: Derrick White at #34 (card #3, 0.011 behind Anthony Davis, who went #38 to seat 11; the 🎯 alone +0.80 title points; the advice line's 'now' man — it read "Derrick White now, Jalen Williams next turn (55% to survive)" and the owner did both); Ty Jerome at #82 (card #28, 0.117 behind Coby White, who went #90 to seat 7; the 🎯 alone +3.51 title points); Jaden McDaniels at #87 (card #12, 0.045 behind Mikal Bridges, who went #88 to seat 9; the 🎯 alone +0.80 title points); Darryn Peterson at #111 (card #33, 0.145 behind Sandro Mamukelashvili, who went #133 to seat 12; the 🎯 alone +2.67 title points). Following the card's chain self-consistently grades 35.00 percent. The advice line fired at #34, and the owner took its pair — White there, Jalen Williams at #39. The survival chips scored a Brier of 0.181 against a 0.242 base rate; positions matched the pool on all 156 picks; the tool log (159 events: an UNKNOWN fix, two refused inserts and one applied, the Butler heads-up) replayed on the real page with zero drift. **The punt drought (§10)** is by design: since 9/22 the tool has no button that declares a punt, and its room-relative read found a clear path at 7 of 275 owner turns across 25 rooms — one of them this room's #135. **Injured rivals (§11):** yes — every rival's injured man counts at his tag's weekly availability, every week; counted at zero instead, this roster's expected wins rise from 5.371 to 5.549.

## 1. Roster changes

None — this is a mock-draft grade, not a roster pull; no pool row, line, tag or board changed. The validation of the room against Yahoo's recap:

| check | result |
|---|---|
| picks in the recap | 156; all 156 "Last, First" lines resolved to a pool name by the tracker's resolver; no UNKNOWN |
| snake attribution | all 156 seats match the round parity; the owner's 13 picks sit at #10, #15, #34, #39, #58, #63, #82, #87, #106, #111, #130, #135, #154 |
| owner's roster | Karl-Anthony Towns, Tyrese Maxey, Derrick White, Jalen Williams, OG Anunoby, Ivica Zubac, Ty Jerome, Jaden McDaniels, Isaiah Hartenstein, Darryn Peterson, PJ Washington, Devin Vassell, Herbert Jones — identical to the recap's "My Team" |
| cast | seats 1–12: sean, Alejandro, Sahil, Dody, Charles, Hugo, PJ, GoodWillPunting, Ed, **David (10)**, alvin, Giannis |
| tool board vs recap | the tracker's final board (after the insert at #50 and the UNKNOWN fix at #119) matches the recap pick for pick, 156 of 156 |
| positions shown by the draft room vs the pool | **0 of 156 differ**, teams 0 of 156 — the fourth room in a row (§7) |
| state | `arena/data/states/draft_state_68.json`, md5 `cd08323137a56fa7a31609d1c28f6447` |

## 2. The team, replayed

[EVIDENCE: `m68_final.json`, `m68_arms.json`, `m68_followcard_grade.json`, the debrief's headline table]

| roster | ECW (cats/week vs the average opponent) | head-to-heads favored | championship rate, 18,000 seasons, real 8-team bracket | playoff rate | swaps |
|---|---|---|---|---|---|
| as drafted (the card's 🎯 at 9 of 13 turns) | 5.371, rank 1 (next 5.096) | 11 of 11 | **28.36%** (rank 1) | 99.73% | none |
| follow-card, self-consistent (arms stage) | 5.635, rank 1 (next 5.112) | 11 of 11 | **35.00%** (rank 1) | 99.96% | Anthony Davis at #34, Payton Pritchard at #63, Mikal Bridges at #82, Josh Hart at #87, Sandro Mamukelashvili at #111, Fred VanVleet at #135 |
| 🎯 at #34: Anthony Davis for Derrick White (card #3; Anthony Davis went #38) | 5.361, rank 1 (next 5.104) | 11 of 11 | **29.16%** (rank 1) | 99.78% | Anthony Davis at #34 |
| 🎯 at #82: Coby White for Ty Jerome (card #28; Coby White went #90) | 5.480, rank 1 (next 5.092) | 11 of 11 | **31.87%** (rank 1) | 99.90% | Coby White at #82 |
| 🎯 at #87: Mikal Bridges for Jaden McDaniels (card #12; Mikal Bridges went #88) | 5.436, rank 1 (next 5.089) | 11 of 11 | **29.16%** (rank 1) | 99.83% | Mikal Bridges at #87 |
| 🎯 at #111: Sandro Mamukelashvili for Darryn Peterson (card #33; Sandro Mamukelashvili went #133) | 5.470, rank 1 (next 5.103) | 11 of 11 | **31.03%** (rank 1) | 99.92% | Sandro Mamukelashvili at #111 |
| advice at #34: Derrick White for Anthony Davis (the 'now' man; Derrick White went #34) | 5.371, rank 1 (next 5.096) | 11 of 11 | **28.36%** (rank 1) | 99.73% | Derrick White at #34 |
| hindsight single swap Payton Pritchard at #58 | 5.387, rank 1 (next 5.081) | 11 of 11 | **27.99%** (rank 1) | 99.76% | Payton Pritchard at #58 |
| hindsight single swap Coby White at #82 | 5.480, rank 1 (next 5.092) | 11 of 11 | **31.87%** (rank 1) | 99.90% | Coby White at #82 |
| hindsight single swap Coby White at #87 | 5.449, rank 1 (next 5.093) | 11 of 11 | **30.06%** (rank 1) | 99.86% | Coby White at #87 |
| hindsight single swap Sandro Mamukelashvili at #111 | 5.470, rank 1 (next 5.103) | 11 of 11 | **31.03%** (rank 1) | 99.92% | Sandro Mamukelashvili at #111 |
| hindsight single swap Saddiq Bey at #135 | 5.380, rank 1 (next 5.092) | 11 of 11 | **28.71%** (rank 1) | 99.73% | Saddiq Bey at #135 |
| hindsight single swap Draymond Green at #154 | 5.401, rank 1 (next 5.101) | 11 of 11 | **28.10%** (rank 1) | 99.79% | Draymond Green at #154 |

| category rank, as drafted | |
|---|---|
| weekly model | FG% 3 · FT% 3 · 3PTM 5 · PTS 4 · REB 3 · AST 10 · ST 1 · BLK 3 · TO 1 |
| 13-man z-sum | FG% 3 · FT% 3 · 3PTM 6 · PTS 7 · REB 5 · AST 11 · ST 1 · BLK 5 · TO 1 |

The shape: FG%, FT%, REB, ST, BLK, TO inside the top three of the weekly model, AST at 10. It is favored against all eleven and leads the room in expected wins, ahead of seat 1 (sean: Nikola Jokic, Alperen Sengun, LaMelo Ball, Desmond Bane, Onyeka Okongwu, Tyler Herro, De'Aaron Fox, Ja Morant, Jabari Smith Jr., Jakob Poeltl, Collin Gillespie, Jrue Holiday, Dillon Brooks). The follow-the-card chain adds +6.64 title points; the card's own man at each off-card turn, with every other pick as drafted, is worth +3.51 at #82, +2.67 at #111, +0.80 at #34, +0.80 at #87.

## 3. Pick by pick — card vs owner vs hindsight

| pick | deck 🎯 (Top-5) | owner took | card rank · gap (blend) | hindsight best single swap (ΔECW vs final rosters) |
|---|---|---|---|---|
| #10 | Karl-Anthony Towns (Karl-Anthony Towns, Tyrese Maxey, Jalen Johnson, Anthony Davis, Chet Holmgren) | Karl-Anthony Towns | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #15 | Tyrese Maxey (Tyrese Maxey, Jalen Williams, Jamal Murray, Donovan Mitchell, Derrick White) | Tyrese Maxey | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #34 | Anthony Davis (Anthony Davis, Jalen Williams, Derrick White, OG Anunoby, Dyson Daniels) | Derrick White | #3 · +0.011 | none positive (the pick was hindsight-best) |
| #39 | Jalen Williams (Jalen Williams, Desmond Bane, Dyson Daniels, Franz Wagner, OG Anunoby) | Jalen Williams | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #58 | OG Anunoby (OG Anunoby, Dyson Daniels, Ivica Zubac, Payton Pritchard, Cameron Boozer) | OG Anunoby | #1 · +0.000 | Payton Pritchard +0.016 |
| #63 | Ivica Zubac (Ivica Zubac, Payton Pritchard, Tyler Herro, Jarrett Allen, Dyson Daniels) | Ivica Zubac | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #82 | Coby White (Coby White, Zach LaVine, Mikal Bridges, Jalen Suggs, Josh Hart) | Ty Jerome | #28 · +0.117 | Coby White +0.109 |
| #87 | Mikal Bridges (Mikal Bridges, Josh Hart, Coby White, Jalen Suggs, Isaiah Hartenstein) | Jaden McDaniels | #12 · +0.045 | Coby White +0.078 |
| #106 | Isaiah Hartenstein (Isaiah Hartenstein, Yaxel Lendeborg, PJ Washington, Sandro Mamukelashvili, Daniel Gafford) | Isaiah Hartenstein | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #111 | Sandro Mamukelashvili (Sandro Mamukelashvili, Devin Vassell, Cason Wallace, Collin Gillespie, PJ Washington) | Darryn Peterson | #33 · +0.145 | Sandro Mamukelashvili +0.099 |
| #130 | PJ Washington (PJ Washington, Sandro Mamukelashvili, Daniel Gafford, Herbert Jones, Devin Vassell) | PJ Washington | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #135 | Devin Vassell (Devin Vassell, Fred VanVleet, Saddiq Bey, Herbert Jones, Cameron Johnson) | Devin Vassell | #1 · +0.000 | Saddiq Bey +0.009 |
| #154 | Herbert Jones (Herbert Jones, Draymond Green, Cameron Johnson, Jerami Grant, Kyle Filipowski) | Herbert Jones | #1 · +0.000 | Draymond Green +0.031 |

🎯 taken 9 of 13; Top-5 row 10 of 13

[EVIDENCE: `m68_replay.json`, `m68_deckcard_v50.json`, `m68_hindsight.json`; card ranks are the deck's own JS replayed on the v50 page; the blend gap is the Python port's (at #130 and #135 the port's name-order tie-break puts the owner's man second at a 0.000 gap, the page's ΔECW tie-break first — D61-3); the live echoes at #34 (0.011 behind Davis, rank #3), #82 (0.117 behind White, rank #28), #87 (0.045 behind Bridges, rank #12), #111 (0.145 behind Mamukelashvili, rank #33) match the replay]

Reading: the card was followed at 9 of thirteen turns; hindsight has nothing to add at #10, #15, #39, #63, #106, #130 and only +0.016 at #58 (Payton Pritchard), +0.009 at #135 (Saddiq Bey), +0.031 at #154 (Draymond Green). At #34 the owner took Derrick White, card #3 and 0.011 behind Anthony Davis; the advice line's 'now' man — it read "Derrick White now, Jalen Williams next turn (55% to survive)" and the owner did both; Anthony Davis went #38 to seat 11; the 🎯 alone is worth +0.80 title points; hindsight has nothing better at this turn. At #82 the owner took Ty Jerome, card #28 and 0.117 behind Coby White; Coby White went #90 to seat 7; the 🎯 alone is worth +3.51 title points; hindsight's best single swap at this turn is Coby White +0.109 a week. At #87 the owner took Jaden McDaniels, card #12 and 0.045 behind Mikal Bridges; Mikal Bridges went #88 to seat 9; the 🎯 alone is worth +0.80 title points; hindsight's best single swap at this turn is Coby White +0.078 a week. At #111 the owner took Darryn Peterson, card #33 and 0.145 behind Sandro Mamukelashvili with the round-9+ reminder on the echo; Sandro Mamukelashvili went #133 to seat 12; the 🎯 alone is worth +2.67 title points; hindsight's best single swap at this turn is Sandro Mamukelashvili +0.099 a week.

## 4. Tool-state integrity — the deck's board vs the recap, on the v50 page

The owner's tool log was rebuilt as an event list (159 events) and replayed through the real v50 page in headless Chromium [EVIDENCE: `m68_tool_vs_truth.json`, `arena/data/events/m68_tool_events.json`]:

| finding | detail |
|---|---|
| positions differing from the recap | **0 of 156**; owner's roster identical; nothing missing, nothing extra |
| echo lines asserted | 159 of 159 (each feed's resolved name, the seventeen shared-token resolutions, the heads-up, the UNKNOWN warning and its fix, the two refused inserts, the applied insert) |
| the page's own off-card echoes | re-emitted at #34, #82, #87 and #111 identical to the owner's paste (rank, three-decimal gap, 🎯) |
| clock text under the feed title | correct after all 159 events |
| page errors | 0 |
| the UNKNOWN at #119 | "Jurkic" logged the placeholder with the fix hint; the next feed, "119- Jusuf Nurkic", replaced it before #120 — the recap's order |
| the insert at #50 | "Wagner" twice as Insert-at-# — refused both times as ambiguous (Franz Wagner or Moritz Wagner; the page logs nothing and asks for more); then "Franz Wagner" inserted at #50 after Banchero to Dejounte Murray had been logged at #50 to #56 (7 shifted); no owner pick moved seats |
| the heads-up at #149 | "Butler" resolved to Jimmy Butler with the heads-up that he is injury-excluded on this board (acl-recovery-jan26); the room drafted him and the tool logged him as asked |
| undos, halts | none |

The eighth clean public room on the concise card's page family. The refused-insert path is new in a live log and behaved as written: an ambiguous surname never logs.

## 5. Survival chips — the fifteenth out-of-sample room for the refit, the ninth human one

[EVIDENCE: `m68_survival.json`; the debrief's survival table]

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 68 (out of sample) | 51 | 0.463 | 0.588 | **0.181** | 0.242 |
| pooled with every earlier scored room (51 to 67) | 909 | 0.476 | 0.622 | 0.243 | 0.235 |

By chip in this room: BUY NOW 7 rows, mean predicted 0.118, 1 survived; TOSS-UP 17 rows, 0.326, 6 survived; quiet rows 27, 0.638, 23 survived; survivors called at two percent or less: none.

Under the constant base rate for this room (0.181 against 0.242); the pooled figure is 0.243 against its base 0.235. On the 🎯s the owner passed: Davis at #34 (0.61) went #38, before #39; White at #82 (0.52) lasted to the next turn; Bridges at #87 (0.15, BUY NOW) went #88, before #106; Mamukelashvili at #111 (0.38, TOSS-UP) lasted to the next turn.

## 6. The punt advisor, replayed

[EVIDENCE: `m68_advisor.json`; `punt_advice_effect_2026-10-08.json` rows for this state]

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 AST+REB; #63 AST+REB (advise); #82 AST (advise); #87 AST (advise); #106 AST (advise); #111 AST (advise); #130 AST (advise); #135 AST (advise); #154 AST (advise).

Turn by turn on the v50 engine [EVIDENCE: `punt_advice_effect_2026-10-08.json`, this state's rows]: #58 AST+REB (watch, 3/7 kept winnable); #63 AST+REB (advise, 4/7 kept winnable); #82 AST (advise, 2/8 kept winnable); #87 AST (advise, 5/8 kept winnable); #106 AST (advise, 3/8 kept winnable); #111 AST (advise, 5/8 kept winnable); #130 AST (advise, 3/8 kept winnable); #135 AST (advise, 6/8 kept winnable); #154 AST (advise, 5/8 kept winnable). In the page's words: from #58 the strip read "Watching …"; from #63 it advised; at every advised turn but #135 the verdict was "Don't punt them … Keep taking the best player" (kept categories winnable short of the 70 percent bar); at #135 it read "Punting them works: you'd be winning 6 of the other 8 categories … Your call — set the punt box" — advice only, no button, two picks from the end of the draft. The box stayed empty; the finish has assists 10th of 12 in the weekly model.

## 7. The draft room's positions match the pool — 0 of 156, fourth room running

Mocks 60, 61 and 67 matched on every drafted man; this room is the fourth, on both positions and teams [EVIDENCE: `scratchpad m68/positions_check.json`; the recap as pasted]. D60-4 (close D-G3) stands.

## 8. Repeat names on the card — the audit, re-run on this room

Same instrument as mocks 56–67 (`repeat_names_audit.mjs`, seventeen other rooms' owner rosters substituted at each turn, an empty roster; the watch list Gafford, Braun, Poeltl) [EVIDENCE: `m68_repeat_names_audit.json`]:

| readout (mock 67 and 66 columns from `after-report-2026-10-07-draft67.md` §8) | mock 68 | mock 67 | mock 66 |
|---|---|---|---|
| owner turns where the #1 changes under at least one other room's roster | **12 of 13** | 12 of 13 | 12 of 13 |
| owner turns where the #1 changes under an empty roster | **10 of 13** | 10 of 13 | 12 of 13 |
| watch names on this room's Top-5 | Gafford at 2 turn(s) (#106, #130); Braun at 1 turn(s) (#154); Poeltl at 0 turn(s) | see mock 67's report | see mock 66's report |

## 9. The off-card turns, the advice line, and whether the 🎯 waited

[EVIDENCE: `m68_advice_reads.json`, `m68_pairarms.json`, `target_wait_2026-10-08.json`, `m68_followcard_grade.json`]

**The 4 turns.** Coby White for Ty Jerome at #82 +3.51 points (31.87 percent); Sandro Mamukelashvili for Darryn Peterson at #111 +2.67 points (31.03 percent); Anthony Davis for Derrick White at #34 +0.80 points (29.16 percent); Mikal Bridges for Jaden McDaniels at #87 +0.80 points (29.16 percent).

**The advice line (D59-2, advice only).** It fired at #34 (Derrick White now, Jalen Williams next turn (55% to survive): +0.030 cats/wk over the pair). The owner took the 'now' man and the next-turn man as it said, so its arm is the roster as drafted (+0.00 title points). The pre-registered pair rule, replayed as the marker across this room, finished at 36.06 percent against the blend chain's 35.00 on seed set one (5.635 against 5.635 ECW).

**Does the 🎯 wait?** Across mocks 56–68 the 🎯s passed on with a market rank 24 or more slots below the pick were still there at the owner's next turn 15 of 25 times, two turns on 3 of 22; mid-band (12–23 slots) 2 of 6; near-price (under 12) 8 of 20 and 0 of 19.

## 10. The owner's question: why the tool stopped declaring punts

**Short answer: the tool was changed on 2026-09-22 so it cannot declare a punt, and the read that replaced it almost never finds one worth taking.** Nothing broke; the drought is the shipped behavior.

**What changed.** Deck commit `0560c77` (2026-09-22, the mock 51 retro, D51R-3) did two things:

1. **It removed the buttons that wrote the punt box.** Before it, three controls set or rewrote a punt with one click: the FULL TILT pivot on the decision card, the Build read's Adopt, and the coherence strip's Retarget. Mock 51's box changed four times mid-draft (#46, #52, #63, #111) and mock 52's was set at #39. Since then `PUNT_BUTTONS = false`: the strip still reads, but only as a sentence, and the box changes only if the owner types into it [EVIDENCE: `live_deckcard.py` PUNT_TIMELINES, mocks 51–68].
2. **It changed what the read measures.** The old read ranked each category by the 13-man z-sum; mock 51 showed the flaw — it called turnovers 11th while that roster beat 76 percent of the room in them, and proposed punting a category the team was winning. The new read uses the share of the room the roster beats in a typical week (the same weekly model the card's ΔECW half uses), and adds gates: a category must sit at or below 25 percent for two owner picks running, and a punt is called workable only when 70 percent of the kept categories beat at least 55 percent of the room.

**Where the earlier punts came from.** The committed rooms that carry a punt are mocks 31, 32 and 34 (August, three-category boxes), 41 and 50 (two- and three-category), all set before pick 1, plus 51 and 52, set mid-draft by the buttons. No room after mock 52 has had a box set either way. So the drought has two halves: the one-click path was removed, and the pre-draft box has not been used since 9/22.

**The record across every committed room** [EVIDENCE: `arena/results/punt_advice_effect_2026-10-08.json` — the D51R-3 effect harness (`arena/mocks/punt_advice_effect.py`) re-run over all 25 committed states, 275 owner turns, on the v50 engine]:

| readout | old z-sum rule (to 9/21) | room-relative rule (since 9/22) |
|---|---|---|
| owner turns with a punt offer (old: FULL TILT or Adopt; new: "Punting them works") | 6 (FULL TILT 5, Adopt 6) | **7** |
| owner turns where it named a losing category and said "Don't punt them" | — (the old rule had no such verdict) | 113 |
| category-level proposals, all kinds (pivots plus coherence retargets of a box already set) | 58 (33 retargets) | 214 (30 retargets; the rest are the advised turns' categories, mostly "Don't punt") |
| proposals on a category the roster was winning against most of the room | **9** | **0** |
| proposals on a top-4 z-sum category | 1 | 0 |
| one-click button to set the box | yes | no |

The clear-path turns, all of them: mock 54 #154 AST (6/8); mock 56 #111 AST+PTS+REB (5/6); mock 56 #135 AST+PTS+REB (5/6); mock 59 #135 PTS+AST (5/7); mock 65 #63 REB+PTS (5/7); mock 68 #135 AST (6/8); mock 42 #138 FT%+3PTM (5/7). In the sixteen live rooms 53–68 the old rule itself would have offered FULL TILT or Adopt at only 4 turn(s) in mock 59, 1 turn(s) in mock 67 — the old pivot offers were rare everywhere (6 turns in all 25 rooms); its frequent proposals (33 of 58) were coherence retargets, which only run once a box is already set.

**Why clear paths are rare now.** The card has ranked by the ΔECW blend since 2026-08-04: it adds whoever raises expected weekly wins the most against the rosters already in the room. That builds rosters that are good-to-middling almost everywhere, which is what wins weeks, but a punt only pays when the kept categories are strong enough to carry the week. A roster built to win six or seven categories narrowly rarely has 70 percent of its kept categories above 55 percent of the room — so the read says "Don't punt them" at most turns where it sees a weak category.

**The evidence that declaring punts costs title odds** (the reason the change shipped and the reason it has not been reverted):

| study | finding |
|---|---|
| gap study, 2026-07-30 (`findings_2026-07-30_gap_study.md`) | every punt policy loses championship odds against not punting: adaptive punt-the-worst-at-round-4 −4.87 points (t −3.0), punt FT% −5.93, punt TO −6.49, punt AST −7.82, the guard build −8.25, the big-man build −11.22 (t −8.0) |
| pivot gate, 2026-07-27 (`findings_2026-07-27_punt_pivot_gate.md`) | mid-draft pivots measured net-negative in the paired test (two-gate rank −3.16 points, static ≥0.5 −1.42); the "champ% when pivoted" glow was selection — gates fire on drafts already strong |
| mock 54 punt arms (`m54_punt_arms.json`, `m54_punt_arms_veto.json`) | from #63, following the card 48.74 percent vs following it with assists punted 42.49 (veto version 46.29 vs 38.54); 0 of 3 seeds met the steered-wins bar |
| the declared-punt rooms (`LEDGER.md`, old bracket) | title odds and finish: mock 22 0.22 percent, 11th; mock 31 6.16, 5th; mock 32 4.11, 9th; mock 34 9.52, 4th — mock 33, balanced with no punt, 11.37, 3rd |

**What would bring declarations back** is an owner call, already on the sheet as D61-4: turn the buttons back on (`PUNT_BUTTONS = true` restores all three), or declare by hand when the strip says "Punting them works". The default stays advice-only as shipped; nothing in this room argues for changing it (§6: the one clear-path turn was #135, two picks from the end).

## 11. The owner's question: injured men on rival rosters

**Short answer: yes.** Every roster in the category math — yours and all eleven rivals' — runs through one weekly model (`teamWeekModel` on the page, `arena.team_week_model` in the grade). It scales each player's weekly games by an availability read from the first tag of his note, and nothing removes a drafted man from a rival's roster. So Butler on a rival roster still counts, at a discount.

| tag on the note (first word) | weekly availability | share of a healthy man's weekly games | examples in this room |
|---|---|---|---|
| untagged | 0.88 | 100 percent | Nurkić (out about four weeks, untagged today — D-1008-1) |
| `*-risk` | 0.75 | 85 percent | Porziņģis (`inj-risk`), Ingram (`inj-achilles-risk`), Tatum, Haliburton, Lillard, Irving |
| `*-recovery` | 0.60 | 68 percent | Butler (`acl-recovery-jan26`) |

Two different numbers are in play, and they do different jobs. The **card's value half** uses the board multiplier (`av`): Butler 0.0, the risk tier 0.78 — that is why the page warned "heads-up … injury-excluded" when Butler was logged at #149. The **weekly model** uses the tiers above for everyone, rivals included, so Butler on seat 5 still adds 60 percent of a healthy man's games to that roster every week. The model is a season average with no calendar: it charges seat 5 with Butler's 0.60 in October, when he will not play, and in March, when he may.

**What it moves, in this room** [EVIDENCE: `arena/results/m68_injured_rivals.json`, `arena/mocks/injured_rivals_cf.py` — the final rosters re-graded with the four men's availability changed and nothing else]:

| rival | man (pick) | your expected categories won vs that rival, as shipped | with him at 0 | with him healthy (0.88) |
|---|---|---|---|---|
| seat 5 (Charles) | Jimmy Butler (#149) | 5.295 | 5.813 | 5.052 |
| seat 9 (Ed) | Kristaps Porzingis (#136) | 5.046 | 5.540 | 4.958 |
| seat 6 (Hugo) | Brandon Ingram (#91) | 6.086 | 6.520 | 5.997 |
| seat 2 (Alejandro) | Jusuf Nurkic (#119) | 4.765 | 5.283 | 4.765 |
| the room (your ECW, rank) | all four | 5.371, rank 1 | 5.549, rank 1 | 5.332, rank 1 |

Reading: in a week when the man sits, the shipped model overstates that rival by 0.43 to 0.52 categories against you; across the room it is 0.178 categories a week, and it changes no rank here. The direction matters for the draft: discounting rather than zeroing a rival's injured man makes his roster look a little stronger than it will be early in the season, and the card's ΔECW half then values your picks against slightly stiffer opponents. Nurkić is the one gap of kind, not degree — out about four weeks with no tag, he counts as fully healthy; D-1008-1's default (re-tag `foot-recovery` at the next pull) would put him at 0.60. Counting a man at zero still lets that rival's bench fill his lineup slot on game days (the daily-fill weights do that), so the zero column is the fair picture of a week he sits; a rival who replaces him from free agency would be a little stronger than that. Assessment only — no change made (D68-3 asks).

## Watchlist

- **D68-1, Jerome at #82**: card #28, 0.117 behind Coby White (went #90 to seat 7); the 🎯 alone +3.51 points; hindsight's best Coby White +0.109 a week.
- **D68-2, Peterson at #111 with the round-9+ reminder**: card #33, 0.145 behind Sandro Mamukelashvili (went #133 to seat 12); the 🎯 alone +2.67 points.
- **White at #34, McDaniels at #87**: coin-flip and near-coin-flip rows (card #3 at 0.011, #12 at 0.045); +0.80 and +0.80 points.
- **Hartenstein (#106, yours)**: ankle soreness, both exhibitions missed, untagged (D-1008-2, hold until 10/12).
- **Nurkić (#119, seat 2)**: out about four weeks, untagged; D-1008-1's default re-tags him at the next pull (§11).
- Carried: D67-1..6, D66-1, D-V4-1, D-CAST-1..4, D62-1..3, D61-1..4 (D61-4 the punt question, §10), D60-2..4, D-Y1..4, D-RW-1..4, D-1008-1..3.

## Open-item receipts

| item | query run (2026-10-08) | dated finding |
|---|---|---|
| (this analysis) | machine replay only — no web research in this report | pull receipts for the window live in `after-report-2026-10-08.md` (the morning's pull, same day) |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (after-report-2026-10-08.md, receipts dated 10/8) | all HELD or unsigned on 2026-10-08; Ingram (#91, seat 6), Porzingis (#136, seat 9), Leonard (#37, seat 12), Rollins (#67, seat 6) were drafted by opponents in this room; Thomas, Ivey, Sochan, Ball, Dillingham, Mathurin by no one; nothing here changes a card |

## Bounds

- Championship figures are on the real eight-team bracket (E14); the arms use 18,000 CRN seasons on three seeds (seed set 2 for the pair-arms replay: 28.38 / 35.20 / 35.60 percent as drafted / blend chain / pair chain).
- A1: the room ran on v50, the version live at the standing URL from 15:15 UTC; the echoes cannot tell it from v49, and the grade would read the same on v49's lines except for Hawkins's team.
- The follow-the-card chain is the retro's Python port of the card (name-order tie-break, D61-3); the page's reads are in §3 and §9.
- The owner's typed tokens are inferred from the echoes (the shared token where the echo said 'assumed over', 'only X left' or 'skipped'; the refused token from the ambiguity line); the replay reproduces every echo, which is the only check the log allows.
- §10's counts replay the advisor on every committed state with the v50 engine; rooms before 9/22 were drafted on the old advisor, so their 'new' column is what the current page would have said, not what the owner saw.
- §11 re-grades one room's final rosters; the draft-time effect on the card (rival rosters a little stronger in the ΔECW half) is not measured here.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D68-1 | Jerome at #82: card #28, 0.117 behind Coby White; the 🎯 alone +3.51 title points. Log it? | log it; no card change |
| D68-2 | Peterson at #111: card #33, 0.145 behind Sandro Mamukelashvili with the round-9+ reminder; the 🎯 alone +2.67 points. Log it? | log it; no card change |
| D68-3 | Injured men on rival rosters count at their tag's season-average weekly availability every week (0.60 recovery, 0.75 risk, 0.88 untagged); zeroing the four out-now men here moves your ECW 5.371 to 5.549, no rank. (a) keep the season-average tiers; (b) count rivals' out-now men at 0 in the card's ΔECW half for draft night only; (c) keep the tiers and rely on the pull's tagging (D-1008-1) for untagged out-now men | (a) keep, with D-1008-1's default applied at the next pull |
| D61-4 (re-put with §10) | Declaring punts: turn `PUNT_BUTTONS` back on, declare by hand when the strip says "Punting them works", or keep advice-only? The record: 7 clear-path turns in 275; every punt policy measured negative | advice only as shipped |
| D67-1..6, D66-1, D-V4-1, D-CAST-1..4, D62-1..3, D61-1..3, D60-2..4, D-Y1..4, D-RW-1..4, D-1008-1..3 | carried | carried |

## Provenance

- Inputs: the owner's tool log and Yahoo recap (this session, 2026-10-08), transcribed into `arena/data/events/m68_tool_events.json` and the recap into the state by the tracker's resolver (`hoops.py draft resync`); state md5 `cd08323137a56fa7a31609d1c28f6447`.
- Every number is read from `arena/results/m68_*.json`, `target_wait_2026-10-08.json`, `punt_advice_effect_2026-10-08.json` and the debrief; the arms use 18,000 CRN seasons (seeds 11/23/47) on the real eight-team bracket; the audit, the deck card, the advisor and the tool replay ran the v50 page's own engine under node and headless Chromium. §10's study figures are quoted from the named files in the deck repo.
- Not verified: nothing here rests on web research.

## In plain language

**How it went.** First of twelve in expected weekly wins, favored against all eleven others, title odds 28.4 percent on the real bracket (rank 1). You took the card's top name at 9 of thirteen turns. The four exceptions: #34 Derrick White (the advice line's pick; +0.80 points for the card's man); #82 Ty Jerome (+3.51 points for the card's man); #87 Jaden McDaniels (+0.80 points for the card's man); #111 Darryn Peterson (+2.67 points for the card's man). Following the card all the way grades 35.0 percent.

**The tool.** Your 159 events replayed on the real page with zero mismatches: the "Jurkic" fix, the two "Wagner" inserts the page refused as ambiguous, then "Franz Wagner" at #50, and the Butler heads-up.

**Why no punts lately.** On September 22 the buttons that set a punt were removed, after mock 51 showed the old read proposing to punt a category your roster was winning. The tool now only advises in words, and it calls a punt workable only when the rest of your roster is strong enough. With the card building balanced rosters, that happened at 7 of 275 turns across 25 rooms — once here, at #135. Every punt study on file says declaring costs title odds. Turning the buttons back on is your call (D61-4).

**Injured rivals.** Yes, they count. A rival's injured man counts at a discount every week: 60 percent of a healthy man's games for a recovery tag like Butler's, 85 percent for a risk tag like Porziņģis's or Ingram's, and 100 percent if he has no tag, which is Nurkić today. Counting the four at zero would lift your expected wins from 5.37 to 5.55 a week; it changes no rank. D68-3 asks whether to keep it that way.
