# After-report — draft_61: the tenth live-human room from the REAL slot 10, the fifth on the concise card — the card followed at nine of thirteen turns, the four misses all in rounds 6 to 12

**Owner request (2026-10-06, verbatim):** "Here is a pick by pick mock draft for you
to review:" — the deck tool's pick-by-pick feed and Yahoo's round-by-round recap,
pasted after the day's Rotoworld and Yahoo intakes.

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (the real league slot; random
humans — a practice rep, not opponent intel; seat 6's display name "martin"
coincides with a modeled league-mate's first name, and a public room cannot say
whether it is the same person, so it is treated as a stranger). **Deck used:** v44
(rev `583435c`, the 2026-10-06 daily-pull build; pool sha `48456b3b18ff`, 335 rows;
Porziņģis veto live; the D59-1 re-numbered history and the D59-2 advice line live)
— proved by replay: the owner's four "off the card" echoes (#63 Lillard rank 65,
0.237 behind Jarrett Allen; #106 Murray-Boyles rank 79, 0.363 behind Lendeborg;
#111 Davion Mitchell rank 48, 0.227 behind Lendeborg; #135 Herbert Jones rank 4,
0.019 behind Mamukelashvili) reproduce on the v44 pool at three decimals, while
the v43 pool (Strus still in it) gives 0.364 and 0.226 at #106 and #111; v45
carries the same pool with the 10/6 prices and was published at 18:38 UTC, after
this room closed, so the chips the owner saw were v44's. **Method:** the recap was
resolved to pool names by the tracker's own resolver (156 of 156) and the state
checked snake-consistent; the grade is the deck plane's machine-derived retro
(`yahoo-fantasy-basketball` `arena/results/m61_*.json`, debrief
`debrief_2026-10-06_mock61_slot10.md`, deck card replayed from the v44 page, title
odds on the league's real eight-team bracket). Every figure below is read from
those files; none is eyeballed. Verification: this file passes
`report/check_report.py`; receipts below.

Pull window: 2026-10-06 → 2026-10-06 (analysis run 2026-10-06 against the v44 pool
and the 10/01 market file the v44 page baked; not a roster pull — the day's four
pull-log rows cover the window).

**Headline.** Rank 2 of 12 in expected weekly category wins (4.940 against 5.366 for seat 4, Jesse), favored in 10 of 11 head-to-heads; title odds **16.66 percent on the league's real bracket** (rank 2 of 12) — the first room from this seat since mock 59 to finish behind another roster in expected wins, with the card followed at 9 of 13 turns (mock 58's count; mock 59 was five, mock 60 eleven). The four misses all came after round five and none of them recovered the 🎯 later. Lillard at #63 (card #65, 0.237 behind Jarrett Allen, with the achilles-risk tag on his row) is the room's large cost: 67 of 252 legal picks grade better, the best of them Tyler Herro by +0.329 categories a week and +9.07 points of title odds (25.73 percent), and the 🎯 himself by +0.174 (+4.35 points, 21.01 percent). Murray-Boyles at #106 (card #79, 0.363 behind Lendeborg, after the round-9+ reminder) and Davion Mitchell at #111 (card #48, 0.227 behind the same Lendeborg, same reminder) are the second and third: Lendeborg waited to #133 as the chips said he would, and taking him at either turn is worth +0.205 or +0.176 a week (+4.81 and +4.03 points). Herbert Jones at #135 (card #4, 0.019 behind Mamukelashvili) is worth +0.23 points the other way. Following the card's chain self-consistently grades 34.49 percent (Jarrett Allen at #63, Zach LaVine at #82, Isaiah Hartenstein at #87, Sandro Mamukelashvili at #106, Cason Wallace at #111, Yaxel Lendeborg at #130, Saddiq Bey at #135); the card at all four off-card turns alone grades 30.99 percent. The D59-2 advice line stayed silent at every turn, for the stated reasons. The survival chips posted their best out-of-sample Brier yet (0.168 against a 0.248 base rate); the draft room's positions matched the pool on all 156 picks for the second room running; the tool log — an UNKNOWN fix and an undo among its 159 events — replayed on the real page with zero drift.

## 1. Roster changes

None — this is a mock-draft grade, not a roster pull; no pool row, line, tag or
board changed. The validation of the room against Yahoo's recap:

| check | result |
|---|---|
| picks in the recap | 156; all 156 "Last, First" lines resolved to a pool name by the tracker's resolver (diacritics, suffixes, "P.J." included); no UNKNOWN |
| snake attribution | all 156 seats match the round parity; the owner's 13 picks sit at #10, #15, #34, #39, #58, #63, #82, #87, #106, #111, #130, #135, #154 |
| owner's roster | Towns, Donovan Mitchell, Jalen Williams, Derrick White, Anunoby, Lillard, Hartenstein, Mikal Bridges, Murray-Boyles, Davion Mitchell, PJ Washington, Herbert Jones, Vassell — identical to the recap's "My Team" |
| cast | seats 1–12: Jp, Neil, Carl, Jesse, Geovanny, martin, Max, Michael, Isam, **David (10)**, fred, A.V |
| tool board vs recap | the tracker's final board (after the UNKNOWN fix and the undo) matches the recap pick for pick, 156 of 156 |
| positions shown by the draft room vs the pool | **0 of 156 differ**, teams 0 of 156 — the second room in a row where the room and the pool match on every drafted man (see §7) |
| state | `arena/data/states/draft_state_61.json`, md5 `051fee6c1160f7fc75452b08fc3826dc` |

## 2. The team, replayed

[EVIDENCE: `m61_final.json`, `m61_arms.json`, `m61_followcard_grade.json`,
the debrief's headline table]

| roster | ECW (cats/week vs the average opponent) | head-to-heads favored | championship rate, 18,000 seasons, real 8-team bracket | playoff rate | swaps |
|---|---|---|---|---|---|
| as drafted | 4.940, rank 2 (next 5.366) | 10 of 11 | **16.66%** (rank 2) | 95.97% | none |
| follow-card, self-consistent (arms stage) | 5.513, rank 1 (next 5.326) | 11 of 11 | **34.49%** (rank 1) | 99.91% | Jarrett Allen at #63, Zach LaVine at #82, Isaiah Hartenstein at #87, Sandro Mamukelashvili at #106, Cason Wallace at #111, Yaxel Lendeborg at #130, Saddiq Bey at #135 |
| card at #63 only (Jarrett Allen for Lillard; Allen went #72) | 5.114, rank 2 (next 5.374) | 10 of 11 | **21.01%** (rank 2) | 98.47% | Jarrett Allen at #63 |
| card at #106 only (Yaxel Lendeborg for Murray-Boyles; Lendeborg went #133) | 5.145, rank 2 (next 5.368) | 10 of 11 | **21.47%** (rank 2) | 98.53% | Yaxel Lendeborg at #106 |
| card at #111 only (Yaxel Lendeborg for Davion Mitchell; Lendeborg went #133) | 5.116, rank 2 (next 5.371) | 10 of 11 | **20.69%** (rank 2) | 98.35% | Yaxel Lendeborg at #111 |
| card at #135 only (Sandro Mamukelashvili for Herbert Jones; Mamukelashvili went #142) | 4.973, rank 2 (next 5.365) | 10 of 11 | **16.89%** (rank 2) | 96.37% | Sandro Mamukelashvili at #135 |
| card at all four off-card turns (#63 Allen, #106 Lendeborg, #111 Draymond Green, #135 Mamukelashvili) | 5.436, rank 1 (next 5.251) | 11 of 11 | **30.99%** (rank 1) | 99.88% | Jarrett Allen at #63, Yaxel Lendeborg at #106, Draymond Green at #111, Sandro Mamukelashvili at #135 |
| hindsight single swap Jalen Johnson at #10 | 4.953, rank 2 (next 5.381) | 10 of 11 | **16.46%** (rank 2) | 96.29% | Jalen Johnson at #10 |
| hindsight single swap Chet Holmgren at #15 | 4.965, rank 2 (next 5.249) | 10 of 11 | **18.06%** (rank 2) | 96.71% | Chet Holmgren at #15 |
| hindsight single swap Tyler Herro at #58 | 4.956, rank 2 (next 5.366) | 10 of 11 | **16.72%** (rank 2) | 95.69% | Tyler Herro at #58 |
| hindsight single swap Tyler Herro at #63 | 5.269, rank 2 (next 5.362) | 10 of 11 | **25.73%** (rank 2) | 99.26% | Tyler Herro at #63 |
| hindsight single swap Zach LaVine at #87 | 4.963, rank 2 (next 5.316) | 10 of 11 | **17.60%** (rank 2) | 95.95% | Zach LaVine at #87 |
| hindsight single swap Draymond Green at #106 | 5.147, rank 2 (next 5.153) | 10 of 11 | **22.92%** (rank 2) | 98.60% | Draymond Green at #106 |
| hindsight single swap Yaxel Lendeborg at #111 | 5.116, rank 2 (next 5.371) | 10 of 11 | **20.69%** (rank 2) | 98.35% | Yaxel Lendeborg at #111 |
| hindsight single swap Draymond Green at #135 | 4.999, rank 2 (next 5.352) | 10 of 11 | **17.11%** (rank 2) | 96.67% | Draymond Green at #135 |
| hindsight single swap Kyle Filipowski at #154 | 4.965, rank 2 (next 5.364) | 10 of 11 | **16.66%** (rank 2) | 95.94% | Kyle Filipowski at #154 |

| category rank, as drafted | |
|---|---|
| weekly model | FG% 6 · FT% 2 · 3PTM 1 · PTS 11 · REB 11 · AST 8 · ST 1 · BLK 7 · TO 1 |
| 13-man z-sum | FG% 6 · FT% 2 · 3PTM 1 · PTS 9 · REB 11 · AST 9 · ST 2 · BLK 7 · TO 1 |

The shape is the second from this seat to concede two counting categories outright (mock 59 gave up points and assists): points and rebounds both sit 11th of 12 in the weekly model, while threes, steals and turnovers are 1st and free throws 2nd — a guard-and-wing roster (Mitchell, White, Lillard, Davion Mitchell, Bridges, Anunoby, Jones, Vassell) with Towns and Hartenstein the only two bigs. It is favored against 10 of the eleven and trails only seat 4 (Jesse: Gilgeous-Alexander, Jamal Murray, Holmgren, Markkanen, Okongwu, Porter Jr., Fox, Powell, LaVine, Maluach, Poeltl, Draymond Green, Anthony Black) in expected wins. Hindsight's single-swap ledger finds nothing at four turns and small change at five more; its large entries are the four off-card turns, and the largest is #63 (Herro +0.329 a week, +9.07 title points). The follow-the-card chain (Jarrett Allen at #63, Zach LaVine at #82, Isaiah Hartenstein at #87, Sandro Mamukelashvili at #106, Cason Wallace at #111, Yaxel Lendeborg at #130, Saddiq Bey at #135) adds +17.83 points; the card at the four off-card turns alone, with every other pick as drafted, adds +14.33.

## 3. Pick by pick — card vs owner vs hindsight

| pick | deck 🎯 (Top-5) | owner took | card rank · gap (blend) | hindsight best single swap (ΔECW vs final rosters) |
|---|---|---|---|---|
| #10 | Karl-Anthony Towns (Karl-Anthony Towns, Jalen Johnson, Tyrese Haliburton, Anthony Davis, Chet Holmgren) | Karl-Anthony Towns | #1 · +0.000 | Jalen Johnson +0.013 |
| #15 | Donovan Mitchell (Donovan Mitchell, Jalen Williams, Jamal Murray, Derrick White, Kevin Durant) | Donovan Mitchell | #1 · +0.000 | Chet Holmgren +0.025 |
| #34 | Jalen Williams (Jalen Williams, Derrick White, Dyson Daniels, OG Anunoby, Jaren Jackson Jr.) | Jalen Williams | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #39 | Derrick White (Derrick White, Desmond Bane, Dyson Daniels, Onyeka Okongwu, Franz Wagner) | Derrick White | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #58 | OG Anunoby (OG Anunoby, Ivica Zubac, Tyler Herro, Payton Pritchard, De'Aaron Fox) | OG Anunoby | #1 · +0.000 | Tyler Herro +0.017 |
| #63 | Jarrett Allen (Jarrett Allen, Payton Pritchard, De'Aaron Fox, Tyler Herro, Pascal Siakam) | Damian Lillard | #65 · +0.237 | Tyler Herro +0.329 |
| #82 | Isaiah Hartenstein (Isaiah Hartenstein, Jalen Suggs, Day'Ron Sharpe, Mikal Bridges, Yaxel Lendeborg) | Isaiah Hartenstein | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #87 | Mikal Bridges (Mikal Bridges, Jalen Suggs, Zach LaVine, Yaxel Lendeborg, Sandro Mamukelashvili) | Mikal Bridges | #1 · +0.000 | Zach LaVine +0.023 |
| #106 | Yaxel Lendeborg (Yaxel Lendeborg, PJ Washington, Sandro Mamukelashvili, Daniel Gafford, Herbert Jones) | Collin Murray-Boyles | #79 · +0.363 | Draymond Green +0.207 |
| #111 | Yaxel Lendeborg (Yaxel Lendeborg, PJ Washington, Sandro Mamukelashvili, Cason Wallace, Aaron Gordon) | Davion Mitchell | #48 · +0.228 | Yaxel Lendeborg +0.176 |
| #130 | PJ Washington (PJ Washington, Yaxel Lendeborg, Sandro Mamukelashvili, Herbert Jones, Cason Wallace) | PJ Washington | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #135 | Sandro Mamukelashvili (Sandro Mamukelashvili, Saddiq Bey, Devin Vassell, Herbert Jones, Fred VanVleet) | Herbert Jones | #4 · +0.019 | Draymond Green +0.059 |
| #154 | Devin Vassell (Devin Vassell, Jerami Grant, Christian Braun, Kyle Filipowski, Nikola Vucevic) | Devin Vassell | #1 · +0.000 | Kyle Filipowski +0.025 |

🎯 taken 9 of 13; Top-5 row 10 of 13

[EVIDENCE: `m61_replay.json`, `m61_deckcard_v44.json`, `m61_hindsight.json`;
card ranks are the deck's own JS replayed on the v44 page; the live echoes at #63
(0.237 behind Jarrett Allen, rank #65), #106 (0.363 behind Lendeborg, rank #79),
#111 (0.227 behind Lendeborg, rank #48) and #135 (0.019 behind Mamukelashvili,
rank #4) match the replay's 0.237, 0.363, 0.228 and 0.019]

Reading: the card was followed at nine of thirteen turns, and at eight of them hindsight has nothing or next to nothing to add (none at #34, #39, #82, #130; +0.013 at #10, +0.017 at #58, +0.023 at #87, +0.025 at #154); the ninth, #15, is Holmgren at +0.025 — he went #28 to seat 4. The four deviations are of three kinds. At #63 the owner took Lillard, card #65 and 0.237 behind Allen, with the card's other four rows grading +0.22 to +0.33 better in hindsight, the 🎯 himself +0.174, and the man taken carrying the achilles-risk availability; Allen went #72 to seat 1, Herro #65 to seat 8. At #106 and #111 the owner twice passed the same 🎯, Lendeborg (0.363 and 0.227 ahead, the round-9+ reminder on both echoes), for Murray-Boyles and Davion Mitchell; Lendeborg lasted to #133, two picks before the owner's #135, so the chip that said he would wait (0.56, then 0.34) was right twice and the roster never got him. At #135 the owner took Herbert Jones over Mamukelashvili by 0.019 — a coin-flip row, and hindsight agrees it was nearly free (+0.033 for the 🎯, +0.059 for Draymond Green, who went #141). The D59-4 pattern (White the 🎯 at #39, passed on) stayed broken: taken, hindsight-best.

Six turns carry a port-versus-page note (D60-1, re-put as D61-3): the retro's
Python card port breaks exact blend ties by name order while the page breaks
them by ΔECW, so the port ranks Lillard #66 at #63 where the page said #65,
Davion Mitchell #47 at #111 where the page said #48, and names Lendeborg the 🎯
at #130 where the page said Washington (the owner took Washington, the page's
#1); the Top-5 order differs at #39, #106 and #154 with the same #1. The table
above reads the page; the owner's echoes agree with the page; the follow-card
chain in §2 reads the port.

## 4. Tool-state integrity — the deck's board vs the recap, on the v44 page

The owner's tool log was rebuilt as an event list (159 events: 158 feeds, sixteen
of them the shared token wherever the echo said "assumed over", "only X left" or
"skipped" — thirteen surnames (Barnes, Murray twice, Ball, Brown, Wagner, Allen,
White, Sharpe, Wilson, Wiggins, Collins, Sheppard) and three first names (Jalen,
Miles, Tre); one UNKNOWN feed, "Gianis" at #5, fixed with "5- Giannis
Antetokounmpo"; one undo at #137 — Egor Demin logged for Seat 8, taken back,
Jrue Holiday logged at #137, Demin re-logged at #138 for Seat 7; no Insert-at-#,
no halt) and replayed through the real v44 page in headless Chromium [EVIDENCE:
`m61_tool_vs_truth.json`, `arena/data/events/m61_tool_events.json`]:

| finding | detail |
|---|---|
| positions differing from the recap | **0 of 156**; owner's roster identical; nothing missing, nothing extra |
| echo lines asserted | 159 of 159 (each feed's resolved name, the sixteen shared-token resolutions, the UNKNOWN warning, the fix, the undo) |
| clock text under the feed title | correct after all 159 events |
| page errors | 0 |
| the UNKNOWN at #5 | "Gianis" logged the UNKNOWN placeholder with the fix hint; "5- Giannis Antetokounmpo" corrected it in place; the seat and the clock never moved |
| the undo at #137 | the echo took Demin back and the next feed logged Holiday at #137 for Seat 8; Demin landed at #138 for Seat 7 — the recap's order |
| the injury-excluded guard | "Shaedon Sharpe skipped: injury-excluded" at #85 resolved the shared token past the excluded man to Day'Ron Sharpe |
| the resume marker | the owner's log ends with "— resumed: 156 picks logged —" (a page reload after the draft completed; the state persisted); nothing to replay |

Sixth clean public room in a row on the concise card's page family (mocks 56–61
drifted none). The three first-name tokens (Jalen, Miles, Tre) are a first: the
resolver's "assumed over" rule handled them the way it handles surnames.

## 5. Survival chips — eighth out-of-sample room for the refit

[EVIDENCE: `m61_survival.json`; the debrief's survival table]

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 61 (out of sample) | 51 | 0.494 | 0.549 | **0.168** | 0.248 |
| pooled with every earlier scored room (51 to 60) | 554 | 0.432 | 0.655 | 0.270 | 0.226 |

By chip in this room: BUY NOW 7 rows, mean predicted 0.103, 1 survived; TOSS-UP 14 rows, 0.335, 6 survived; quiet rows 30, 0.660, 21 survived; survivors called at two percent or less: none.

Eighth straight out-of-sample room under the base rate for the price-only refit
(0.178, 0.189, 0.183, 0.175, 0.168 in the last five), and the best so far. By chip
the pattern is the one your league's own draft showed (D-LS-2) only in part: BUY
NOW rows survived once in seven here (the model said 0.10), TOSS-UP rows six of
fourteen (0.34), quiet rows twenty-one of thirty (0.66). In this room the model
said Lendeborg would wait at #106 (0.56) and at #111 (0.34); he waited both times,
to #133. It said Allen would not wait at #63 (0.27) and Mamukelashvili would not at
#135 (0.18); neither did.

## 6. The punt advisor, replayed

[EVIDENCE: `m61_advisor.json`, 23 pre- and post-pick moments across the owner's turns; `m61_final.json` for the finish]

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 AST+REB; #63 AST+REB (advise); #82 REB+AST (advise); #87 AST (advise); #106 REB+AST (advise); #111 AST+REB (advise); #130 REB+PTS (advise); #135 PTS+REB (advise); #154 REB+PTS (advise).

The room-relative advisor (D51R-3) read a lean at nine of the eleven owner turns with a next turn and cleared the two-turn hysteresis at eight of them — assists and rebounds from #63, rebounds and points from #130 — and the owner left the box empty, which is the design (advice only, no button pressed). The assists lean is this seat's recurring read — mocks 54, 56, 57 and 59 drew the same advise at eight of the last nine turns, mocks 58 and 60 at four and two — and this room adds rebounds throughout and points from #130. The finish is the shape it read: points and rebounds 11th of 12 in the weekly model, assists 8th, with threes, steals and turnovers 1st. Whether a declared two-category concession from this seat is something the card should build toward is on the sheet as D61-4.

## 7. The draft room's positions match the pool again — 0 of 156

Mock 60 was the first room after the 10/01 position sync (D-ADP-3) where the
room's display matched the pool on every drafted man; this room is the second,
on both positions and teams [EVIDENCE: `scratchpad m61/positions_check.json`; the
recap as pasted]. The owner's roster reads the same in the room and on the deck
(Jalen Williams SF,PF; Murray-Boyles PF,C; PJ Washington PF,C; Herbert Jones
SG,SF). D60-4 (close D-G3) stands.

## 8. Repeat names on the card — the audit, re-run on this room

Same instrument as mocks 56–60 (`repeat_names_audit.mjs`, ten other rooms'
owner rosters substituted in at each turn, an empty roster, value-only and
ΔECW-only orders; the watch list Poeltl, Gafford, Brook Lopez, Cameron Johnson,
Braun, Eason) [EVIDENCE: `m61_repeat_names_audit.json`]:

| readout | mock 61 | mock 60 | mock 59 |
|---|---|---|---|
| owner turns where the #1 changes under at least one other room's roster | **10 of 13** | 12 of 13 | 10 of 13 |
| owner turns where the #1 changes under an empty roster | **11 of 13** | 12 of 13 | 10 of 13 |
| watch names on this room's Top-5 | Gafford at one turn (#106, 4th), Braun at one (#154, 3rd); Poeltl, Lopez, Cameron Johnson and Eason at none | Gafford at two turns, Braun at one | Poeltl at three turns, Braun at one |

The three turns where the #1 held under every other room's roster were #10 (the
first pick, roster-blind by construction), #34 and #39 (Jalen Williams and
Derrick White, the #1 under all ten substituted rosters — the two names the deck
has put first at those turns in every room from this seat). The empty-roster #1
from #58 on reads Allen, Allen, LaVine, LaVine, Gafford, Gafford, Braun, Braun,
Braun while the card said Anunoby, Allen, Hartenstein, Bridges, Lendeborg,
Lendeborg, Washington, Mamukelashvili, Vassell — eight of nine decided by the
roster as it stood (Allen at #63 is the one agreement). The value-only #1 was
Anthony Davis at the first two turns, Dyson Daniels at #34 and #39, and Fred
VanVleet from #106 on; the card never put either first.

## 9. The four off-card turns, the advice line's second live room, and whether the 🎯 waited

[EVIDENCE: `m61_advice_reads.json` (the advice line on the page's own Top-5 rows, pair_decision twin), `m61_pairarms.json`, `target_wait_2026-10-06.json`, `m61_followcard_grade.json`]

**The four turns.** The grades in §2 say what each one cost on its own: Allen for Lillard at #63 +4.35 points (21.01 percent), Lendeborg for Murray-Boyles at #106 +4.81 (21.47), Lendeborg for Davion Mitchell at #111 +4.03 (20.69), Mamukelashvili for Jones at #135 +0.23 (16.89); all four together, 30.99 percent (+14.33). None of the four 🎯s was taken later by the owner, which is the difference from mock 60: there the two misses were reorders and cost one slot; here they are four different men on the roster.

**The advice line's second live room (D59-2, shipped v40 as advice only).** It fired at no turn, on the page's rows or the port's: the 🎯 sat under the 0.60 wait floor at 5 turns (#10, #15, #34, #58, #130 — 'take him now'), and was the best pair at 7 (#39, #63, #82, #87, #106, #111, #135); #154 has no next turn. Nothing to grade against, and nothing the D60-3 wording defect could touch. The pre-registered pair rule, replayed as the marker across this room, moved it at one turn of the chain's own path (#82) and finished at 34.49 percent against the blend chain's 34.49 on seed set one (5.513 against 5.513 ECW) — the advice-only verdict holds on its second out-of-sample room.

**Does the 🎯 wait? — the instrument, with this room added.** Across mocks 56–61 the 🎯s passed on with a market rank 24 or more slots below the pick were still there at the owner's next turn 8 of 10 times (this room added Lendeborg at #106, +45, and at #111, +40 — there both times — and Mamukelashvili at #135, +46, gone at #142), and two turns on 3 of 9; near-price 🎯s (under 12 slots) 5 of 11 and 0 of 10 (this room added Allen at #63, +6, gone at #72). The card's survival read is the number to trust on a deep 🎯; this room passed one twice and lost him by two picks.

## Watchlist

- **D61-1, Lillard at #63**: card #65 with the achilles-risk tag; the room's large cost. Conviction pick or a tag question — his preseason minutes decide (WO-5).
- **D61-2, Lendeborg passed twice**: the 🎯 at #106 and #111, lasted to #133. His rookie-proj line is a WO-5 item; nothing on the card changes today.
- **D61-3 (D60-1 re-put), the port's tie-break**: six turns in this room after four in mock 60; align the retro's card port with the page's ΔECW rule and re-run mocks 56–61's chains.
- **D61-4, the roster shape**: points and rebounds both 11th from this seat; the room-relative advisor advised a two-category lean at eight of the last nine turns and the box stayed empty. On the sheet.
- The D59-4 pattern (White passed at #39) stayed broken: taken, hindsight-best.
- Carried: D-Y1..4 (the price file, Yahoo's line, Yahoo's Rank, Acuff), D-RW-1..4, D-1006-1..4 (Acuff, Coby White, the build regex, Strus), D-1005-1/3/4, D-1002-1/3, D60-2 (Murray-Boyles — taken again here, at #106 again), D60-3 (the advice-line wording), D60-4 (close D-G3), D58-2..4, the league settings screenshot (D-G5), the preseason projection refresh (WO-5, after two games per team).

## Open-item receipts

| item | query run (2026-10-06) | dated finding |
|---|---|---|
| (this analysis) | machine replay only — no web research in this report | pull receipts for the window live in `after-report-2026-10-06.md`, `after-report-2026-10-06-rotoworld.md` and `after-report-2026-10-06-yahoo.md` |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull and the 10/6 Yahoo paste, same day (after-report-2026-10-06.md, after-report-2026-10-06-yahoo.md) | all HELD or unsigned on 2026-10-06; Ingram (#74, seat 2), Porzingis (#128, seat 8), Kawhi (#31, seat 7) and Rollins (#70, seat 3) were drafted by opponents in this room; nothing here changes a card |

## Bounds

- Championship figures are on the real eight-team bracket (E14); the arms use 18,000 CRN seasons on three seeds (seed set 2 for the pair-arms replay: 17.01 / 34.27 / 34.27 percent as drafted / blend chain / pair chain).
- The room was drafted on v44 and graded on v44's lines; v45 (published after the room) carries the same lines with the 10/6 prices, so its chips would have read differently at the margins. A different line set grades every room differently.
- The follow-the-card chain is the retro's Python port of the card; at six turns its order differs from the page's (§3). The page's reads are in §3 and §9.
- The advice line's reads are the Python twin of pairDecision on the page's rows, not a capture of the rendered sentence; the two are bit-identical by the card suite's fixtures.
- The owner's typed tokens are inferred from the echoes (the shared token where the echo said 'assumed over', 'only X left' or 'skipped'; the full name elsewhere) — A1; the replay reproduces every echo, which is the only check the log allows.
- The reload after #156 has nothing to replay; the state persisted.
- The target-wait table pools six rooms of random public opponents; it says how the public prices the card's deep names, not how the eleven league-mates will.
- The advisor's reads are the replay's read of the engine at each owner turn; the owner's screen at the time is not recorded. No punt was declared (A2).

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D61-1 | Lillard at #63: card #65, 0.237 behind Allen, with `inj-achilles-risk (first season back)` on his row (availability 0.78); hindsight 68th of 252, Herro +0.329 a week and +9.07 title points, the 🎯 +4.35. A conviction pick on the return (log it, no card change), or a case that the risk tag should move once his preseason minutes are in? | log it as a conviction pick; review the tag at the WO-5 refresh with his preseason minutes |
| D61-2 | Lendeborg: the 🎯 at #106 and #111 (0.363 and 0.227 ahead, the round-9+ reminder on both echoes), passed twice, lasted to #133; the card's chips said he would wait and he did. Is there a reason about his line (rookie-proj; Kerr: "clearly going to play a ton"; started at SF 10/3) the card is missing, or a conviction against a rookie forward at that slot? | no card change; his line is a WO-5 item with the preseason box scores; log the two picks as conviction picks |
| D61-3 | D60-1 re-put with the evidence: the port's name-order tie-break differs from the page at six turns here (#63 rank 66 vs 65, #111 47 vs 48, the 🎯 at #130, the Top-5 order at #39, #106, #154) after four in mock 60. Align the port with the page's ΔECW rule for rooms drafted on v33 or later and re-run mocks 56 to 61's chains before the next live room? | yes — next harness change, red-first |
| D61-4 | The room-relative advisor (D51R-3) advised a lean at eight of the last nine turns — assists and rebounds from #63, rebounds and points from #130 — and the box stayed empty; the finish concedes points and rebounds (11th of 12 weekly), assists 8th. When the strip advises a two-category lean from this seat, do you want to declare the punt so the card builds toward it, or does the advisor stay advice-only as shipped? | advice only as shipped; no change; the lean is logged for the WO-5 review of the seat-10 shape |
| D60-2 | Murray-Boyles — taken at #106 again, card #79 again | carried: review his line at the WO-5 refresh |
| D60-3 | the advice line's partner wording | carried: next deck build, red-first |
| D60-4 | close D-G3 (positions matched 156 of 156 twice running) | carried: close |
| D-Y1..4, D-RW-1..4, D-1006-1..4, D-1005-1/3/4, D-1002-1/3, D58-2..4 | carried | carried |

## Provenance

- Inputs: the owner's tool log and Yahoo recap (this session, 2026-10-06),
  transcribed verbatim into `arena/data/events/m61_tool_events.json` and the
  recap into the state by the tracker's resolver (`hoops.py draft resync`).
- Every number is read from `arena/results/m61_*.json` and the debrief; the arms
  use 18,000 CRN seasons (seeds 11/23/47) on the real eight-team bracket; the
  audit, the deck card, the advisor and the tool replay ran the v44 page's own
  engine under node and headless Chromium.
- Not verified: nothing here rests on web research.

## In plain language

**What this was.** Your tenth practice draft from the real seat, on the deck as it stood after this morning's pull. I rebuilt the room from Yahoo's recap, replayed your tool log through the real page, and graded the roster the way every room has been graded: expected weekly category wins against the eleven other rosters, then 18,000 simulated seasons on the league's real eight-team bracket.

**How it went.** Second of twelve in expected wins, behind Jesse's roster at seat 4. The roster is favored against 10 of the other eleven and wins the title in 16.7 percent, rank 2 of 12, with a 96.0 percent playoff rate. It is the second team you have drafted from this seat that gives up two counting categories outright (mock 59 gave up points and assists): points and rebounds are both eleventh of twelve. Threes, steals and turnovers are first, free throws second.

**What you did with the card.** You took the card's top name at nine of thirteen turns. The four exceptions, in order of cost:

- **#63, Lillard.** The card had Jarrett Allen first and Lillard sixty-fifth, and Lillard's row carries the achilles-risk tag. Every one of the card's five names graded better in hindsight; the best, Herro, went two picks later and is worth about +9.1 points of title odds. This is the room's one large cost.
- **#106 and #111, passing Lendeborg twice.** The card had him first at both turns, by a wide margin, with the round-9 reminder on both echoes. You took Murray-Boyles and then Davion Mitchell. Lendeborg lasted to #133, two picks before your next turn, so the chip that said he would wait was right both times and you never got him. Taking him at either turn is worth about +4.8 or +4.0 points.
- **#135, Herbert Jones.** A coin flip against Mamukelashvili (0.019 apart). Nearly free in hindsight.

Taking the card at all four turns, everything else as drafted, grades 31.0 percent against 16.7.

**The advice line.** Its second live room, and it stayed silent at every turn, each time for the stated reason (the top name would not wait, or the top name was already the best pair). Nothing to grade. The punt advisor did speak: from #63 on it read a lean away from assists and rebounds, later rebounds and points, and you left the box empty, which is how it is built.

**The tool itself.** Your 159 events — including the 'Gianis' fix at #5 and the undo at #137 — replayed on the real page with zero mismatches. The draft room's positions matched the deck on all 156 players for the second room running. The survival chips had their best room yet.

**Your decisions.** D61-1 Lillard: conviction pick, or a tag question (default: log it; review the tag after the preseason games). D61-2 Lendeborg passed twice: a reason the card is missing, or conviction (default: no change; his line is a refresh item). D61-3 fix the retro's tie-break (default yes). D61-4 whether to declare the punt when the advisor flags a two-category lean (default: advice only, as shipped). Everything earlier is carried.
