# After-report — draft_59: the eighth live-human room from the REAL slot 10, the third on the concise card, the first with four Insert-at-# corrections — and the owner's two card proposals answered on it

**Owner request (2026-10-01, verbatim):** "Here is latest pick by pick mock
draft for your analysis:" — the deck tool's pick-by-pick feed and Yahoo's
round-by-round recap; then, mid-grade, two proposals: (1) "After I use the
'Insert at #' function, can the history box say '(player) inserted at #',
and then re-number each pick following (so that I can track that each pick
is in order)" and (2) "The tool suggested Poeltl, who did not get selected
for at least 3+ rounds. My worry is that the tool is suggesting players that
are way down the board, when I could be drafting higher valued players
available at that point in the draft."

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (the real league slot;
random humans — a practice rep, not opponent intel; none of the eleven seat
names is a modeled league-mate). **Deck used:** v37 (rev `b3986f8`, the
10/01 daily-pull build; pool sha `09fe6d433264`, 334 rows; Porziņģis veto
live; the D-R5 advice wording live) — proved by replay: the owner's own
echo at #39, "0.164 behind 🎯 Derrick White", reproduces on the v37 page as
a 0.1637 gap. **Method:** the recap was resolved to pool names by the
tracker's own resolver (155 of 156; the one unresolved name, Yang Hansen,
has no pool row on either plane) and the state checked snake-consistent;
the grade is the deck plane's machine-derived retro (`yahoo-fantasy-
basketball` `arena/results/m59_*.json`, debrief
`debrief_2026-10-01_mock59_slot10.md`, deck card replayed from the v37 page
the owner drafted against, title odds on the league's real eight-team
bracket). Every figure below is read from those files; none is eyeballed.
Verification: this file passes `report/check_report.py`; receipts below.

Pull window: 2026-10-01 → 2026-10-01 (analysis run 2026-10-01 against the
v37 pool and the 9/22 market file; not a roster pull — the 10/01 pull-log
rows cover the window).

**Headline.** Rank 2 of 12 in expected weekly category wins (5.092 against 5.260 for seat 2, Giordano), favored in 10 of 11 head-to-heads; title odds **20.38 percent on the league's real bracket** (rank 2 of 12) — the first live room from the real seat that did not finish first, and the first where the card was left at more than one turn that mattered. The 🎯 was taken at 5 of 13 turns and four picks sat off the Top-5 (Kessler #39, Sharpe #82, Edgecombe #87, Queta #106); hindsight prices those four at +0.237, +0.112, +0.107 and +0.215 categories a week. Following the card at every turn would have been 39.18 percent; Derrick White at #39 alone 27.14. Tool state was clean (161 events, four inserts, a halt and an undo, zero drift) but the history box did not keep up with the inserts — the owner's proposal (1), answered in §9a. The survival chips scored a Brier of 0.183 against a 0.241 base rate in their sixth out-of-sample room, and the owner's proposal (2) — the card names men the room will not take for rounds — is measured in §9b: the survival-aware roster (LaVine at #82, Poeltl at #87) grades 26.36 percent.

## 1. Validation vs the Yahoo recap

| check | result |
|---|---|
| picks in the recap | 156; 155 "Last, First" lines resolved to a pool name by the tracker's resolver (diacritics, suffixes, "P.J." included); one UNKNOWN — #126 "Hansen, Yang" (Portland's center, no pool row on either plane; D59-3) |
| snake attribution | all 156 seats match the round parity; the owner's 13 picks sit at #10, #15, #34, #39, #58, #63, #82, #87, #106, #111, #130, #135, #154 |
| owner's roster | Haliburton, Towns, Jalen Williams, Kessler, Anunoby, Lillard, Day'Ron Sharpe, Edgecombe, Queta, Gillespie, PJ Washington, Lendeborg, Vassell — identical to the recap's "My Team" |
| cast | seats 1–12: Kobe, Giordano, Christian, Antonio, Benjamin, Gabe, Tiger, Kross, Nate, **David (10)**, William, shiny |
| positions shown by the draft room vs the pool | **28 of 155 differ**, every one the pool listing MORE positions than the room (see §7) |
| state | `arena/data/states/draft_state_59.json`, md5 `0bfcbba343380d83e2436ed1125695d3` |

## 2. The team, replayed

[EVIDENCE: `m59_final.json`, `m59_arms.json`, `m59_followcard_grade.json`,
the debrief's headline table]

| roster | ECW (cats/week vs the average opponent) | head-to-heads favored | championship rate, 18,000 seasons, real 8-team bracket | playoff rate | swaps |
|---|---|---|---|---|---|
| as drafted | 5.092, rank 2 (next 5.260) | 10 of 11 | **20.38%** (rank 2) | 98.50% | none |
| follow the card (self-consistent) | 5.660, rank 1 (next 5.252) | 11 of 11 | **39.18%** (rank 1) | 99.97% | Tyrese Maxey at #10, Derrick White at #39, Jakob Poeltl at #63, Damian Lillard at #82, Miles Bridges at #87, Day'Ron Sharpe at #106 |
| card's #1 at #39 only (Derrick White) | 5.329, rank 1 (next 5.260) | 11 of 11 | **27.14%** (rank 2) | 99.67% | Derrick White at #39 |
| card's #1 at #82 only (Poeltl) | 5.177, rank 2 (next 5.260) | 10 of 11 | **23.06%** (rank 2) | 99.17% | Jakob Poeltl at #82 |
| card's #1 at #87 only (LaVine) | 5.199, rank 2 (next 5.263) | 10 of 11 | **23.32%** (rank 2) | 99.18% | Zach LaVine at #87 |
| survival-aware: LaVine #82, Poeltl #87 | 5.296, rank 1 (next 5.273) | 10 of 11 | **26.36%** (rank 2) | 99.61% | Zach LaVine at #82, Jakob Poeltl at #87 |

| category rank, as drafted | |
|---|---|
| weekly model | FG% 2 · FT% 7 · 3PTM 7 · PTS 11 · REB 3 · AST 11 · ST 2 · BLK 3 · TO 1 |
| 13-man z-sum | FG% 2 · FT% 7 · 3PTM 7 · PTS 10 · REB 2 · AST 10 · ST 3 · BLK 3 · TO 1 |

The shape is new for this seat: steals, blocks, turnovers and FG% locked
(1st to 3rd), rebounds 3rd, and two conceded categories instead of one —
points and assists both 11th weekly. The earlier rooms conceded assists
alone and finished first; this one conceded points as well (Haliburton,
Towns and Jalen Williams are the only three 20-point men on it) and
finished second to Giordano's seat. Hindsight's single-swap ledger
is the story of §3: White at #39 is worth +6.76 points of title odds on
its own, and the full follow-card chain (Tyrese Maxey at #10, Derrick White at #39, Jakob Poeltl at #63, Damian Lillard at #82, Miles Bridges at #87, Day'Ron Sharpe at #106) +18.80.

## 3. Pick by pick — card vs owner vs hindsight

| pick | deck 🎯 (Top-5) | owner took | card rank · gap (blend) | hindsight best single swap (ΔECW vs final rosters) |
|---|---|---|---|---|
| #10 | Karl-Anthony Towns (Karl-Anthony Towns, Tyrese Maxey, Tyrese Haliburton, Anthony Davis, Chet Holmgren) | Tyrese Haliburton | #3 · +0.006 | Tyrese Maxey +0.029 |
| #15 | Karl-Anthony Towns (Karl-Anthony Towns, Anthony Davis, Chet Holmgren, Evan Mobley, Tyrese Maxey) | Karl-Anthony Towns | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #34 | Jalen Williams (Jalen Williams, Derrick White, Dyson Daniels, Kyrie Irving, OG Anunoby) | Jalen Williams | #1 · +0.000 | Derrick White +0.019 |
| #39 | Derrick White (Derrick White, Desmond Bane, Kyrie Irving, OG Anunoby, Franz Wagner) | Walker Kessler | #47 · +0.164 | Derrick White +0.237 |
| #58 | OG Anunoby (OG Anunoby, Dyson Daniels, Payton Pritchard, Tyler Herro, Damian Lillard) | OG Anunoby | #1 · +0.000 | Payton Pritchard +0.014 |
| #63 | Payton Pritchard (Payton Pritchard, Damian Lillard, De'Aaron Fox, Zach LaVine, Michael Porter Jr.) | Damian Lillard | #2 · +0.000 | Payton Pritchard +0.047 |
| #82 | Jakob Poeltl (Jakob Poeltl, Zach LaVine, Jalen Suggs, Miles Bridges, Josh Hart) | Day'Ron Sharpe | #12 · +0.048 | Miles Bridges +0.112 |
| #87 | Zach LaVine (Zach LaVine, Jalen Suggs, Miles Bridges, Josh Hart, Collin Gillespie) | VJ Edgecombe | #20 · +0.078 | Zach LaVine +0.107 |
| #106 | Jakob Poeltl (Jakob Poeltl, PJ Washington, Yaxel Lendeborg, Collin Gillespie, Cason Wallace) | Neemias Queta | #52 · +0.244 | Jakob Poeltl +0.215 |
| #111 | Collin Gillespie (Collin Gillespie, Devin Vassell, Jakob Poeltl, Cason Wallace, Quentin Grimes) | Collin Gillespie | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #130 | Devin Vassell (Devin Vassell, PJ Washington, Yaxel Lendeborg, Saddiq Bey, Herbert Jones) | PJ Washington | #2 · +0.003 | none positive (the pick was hindsight-best) |
| #135 | Devin Vassell (Devin Vassell, Saddiq Bey, Fred VanVleet, Malik Monk, Yaxel Lendeborg) | Yaxel Lendeborg | #5 · +0.016 | Saddiq Bey +0.013 |
| #154 | Devin Vassell (Devin Vassell, Fred VanVleet, Malik Monk, Reed Sheppard, Christian Braun) | Devin Vassell | #1 · +0.000 | Malik Monk +0.007 |

🎯 taken 5 of 13; Top-5 row 9 of 13

[EVIDENCE: `m59_replay.json`, `m59_deckcard_v37.json`, `m59_hindsight.json`;
card ranks are the deck's own JS replayed on the v37 page; the live echo at
#39 ("0.164 behind 🎯 Derrick White") matches the replay's 0.1637]

Reading: the first live room where the owner left the card at more than one
turn that mattered. Eight of thirteen picks were off the 🎯 and four of
those were off the Top-5 altogether: Kessler at #39 (card #47, 0.164
behind), Sharpe at #82 (#12, 0.048), Edgecombe at #87 (#20, 0.078) and
Queta at #106 (#52, 0.244). Hindsight's single-swap ledger, which re-scores
each turn against the rosters as they finished, puts the cost where the
card put it: Derrick White at #39 (+0.237 categories a week, 31 legal
alternatives better than Kessler), Poeltl at #106 (+0.215, 44 better than
Queta), Bridges or LaVine at #82 (+0.112 / +0.101) and LaVine at #87
(+0.107). Those four turns are the whole gap between this roster's rank 2
and the rank-1 finish of the earlier rooms; the other nine picks were
within 0.05 of hindsight-best, five of them hindsight-best outright. The
round-9+ rule (D54-1, take the 🎯) was followed at two of the five turns
from #106 on (Gillespie at #111, Vassell at #154); the three deviations
were Queta at #106 (the costly one), Washington at #130 (0.003 behind the
🎯, hindsight-best outright) and Lendeborg at #135 (0.016 behind; Bey
+0.013). The two late ones cost 0.000 and 0.013; the first cost 0.215.

## 4. Tool-state integrity — the deck's board vs the recap, on the v37 page

The owner's tool log was rebuilt as an event list (161 events: 156 feeds,
sixteen of them the shared token wherever the echo said "assumed over" or
"only X left" — Jalen, Barnes, Mitchell, Murray, Ball, Williams, Brown,
White, Wagner, Allen, Sharpe, Wilson, Wiggins, Bridges, Collins, Reed; three
UNKNOWN feeds, "Keytone" and "Posz" fixed by number, "Hansen" left standing;
four Insert-at-# corrections — Jalen Green at #97, Keegan Murray at #118, RJ
Barrett at #121, Rui Hachimura at #128; the HALTED "Johnson" feed; and the
undo that turned Reed Sheppard into Paul Reed at #156) and replayed through
the real v37 page in headless Chromium [EVIDENCE: `m59_tool_vs_truth.json`,
`arena/data/events/m59_tool_events.json`]:

| finding | detail |
|---|---|
| positions differing from the recap | **0 of 156**; owner's roster identical; the one UNKNOWN sits at #126 on both |
| echo lines asserted | 161 of 161 (each feed's resolved name, the three UNKNOWNs, the two fixes, the four inserts, the HALTED refusal, the undo) |
| clock text under the feed title | correct after all 161 events |
| page errors | 0 |
| the inserts, live | each one shifted the right range and recomputed the seats ("#97–#105 to #98–#106 (9 shifted)"); the final state matches the recap pick for pick |
| the halt, live | "Johnson" before #143 stopped the feed with the fuller-name instruction; "Cameron Johnson" logged — the D51 surname guard working as designed |
| **what the log did NOT do** | two of the owner's own picks were logged under another seat at the time — #106 Neemias Queta as "#105 to Seat 9" and #130 PJ Washington as "#128 to Seat 8" — because the inserts that moved them to the owner's slot came later; neither got the card echo (rank, gap, round-9+ reminder) that every other owner pick got. And the standing UNKNOWN keeps its pre-shift label, "UNKNOWN #125", while it sits at #126. Both are the owner's proposal (1) — see §9 and D59-1 |

Fourth clean public room in a row on the concise card's page family
(mocks 56–59 drifted none). The inserts and the standing UNKNOWN are the
new mechanics exercised here, and the state behaved; the log's narration
did not keep up with it.

## 5. Survival chips — sixth out-of-sample room for the refit

[EVIDENCE: `m59_survival.json`; the debrief's survival table]

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 59 (out of sample) | 52 | 0.514 | 0.596 | **0.183** | 0.241 |
| pooled with every earlier scored room (51 to 58) | 454 | 0.418 | 0.672 | 0.294 | 0.220 |

By chip in this room: BUY NOW 6 rows, mean predicted 0.134, 2 survived;
TOSS-UP 13 rows, 0.333, 5 survived; quiet rows 33, 0.655, 24 survived; no
survivor was called at two percent or less. Sixth straight out-of-sample
room under the base rate for the price-only refit (0.178, 0.189, 0.183 in
the last three). The pooled row still carries the pre-refit rooms and is a
history, not a grade. The chips' calibration is what §9's second answer
rests on: the model that said Poeltl would wait (0.829) was right in every
room it said so, and the model that said LaVine was a coin flip (0.506) was
right too.

## 6. The punt advisor, replayed

[EVIDENCE: `m59_advisor.json`, 25 pre- and post-pick moments across the
owner's turns; `m59_final.json` for the finish]

The advisor spoke in this room, and it was reading the roster that was
being built. Points and assists leaned on two consecutive turns by #63
(the two-turn hysteresis satisfied at the #63 pre-pick moment), so from
#63 on the strip read ADVISE PTS·AST at every owner turn but #87's and
#111's post-pick moments, where the lean briefly dropped to points alone
or to nothing after a guard was taken. The "clear" flag (a winnable path
through at least 70 percent of the kept categories) came on at #87, #106,
#111, #130, #135 and #154. The owner declared no punt and took the picks
that the lean describes anyway: Sharpe, Queta, Washington and Lendeborg
are rebounds-blocks-FG% men, and the roster finished ranked 11th weekly in
both points and assists while winning the other seven. Advice only, box
left empty by design (D51R-3); the read and the finish agree.

## 7. Two Yahoo position displays disagree — 28 of 155 drafted men

The 9/29 and 9/30 rooms showed 29 of 156 drafted men with fewer positions
than the pool carries; this room shows 28 of 155, and again the pool is a
superset in every case: 10 extra SF listings, 10 SG, 5 PF, 3 PG [EVIDENCE:
`scratchpad m59/positions_check.json`; the recap as pasted]. On the owner's
roster: Jalen Williams (room PF,SF; pool adds SG), PJ Washington (room C,PF;
pool adds SF), Lendeborg (room PF; pool adds SF). Three rooms agreeing is
one more data point for D-G3 (set both planes' positions from the draft
room before Oct 14); nothing new to decide here.

## 8. Repeat names on the card — the audit, re-run on this room

Same instrument as mocks 56–58 (`repeat_names_audit.mjs`, eight other
rooms' owner rosters substituted in at each turn, an empty roster,
value-only and ΔECW-only orders; Poeltl and Gafford added to the watch list
this time) [EVIDENCE: `m59_repeat_names_audit.json`]:

| readout | mock 59 | mock 58 | mock 57 |
|---|---|---|---|
| owner turns where the #1 changes under at least one other room's roster | **10 of 13** | 10 of 13 | 10 of 13 |
| owner turns where the #1 changes under an empty roster | **10 of 13** | 8 of 13 | 11 of 13 |
| the mock-56 repeat names (Brook Lopez, Cameron Johnson, Braun, Eason) on this room's Top-5 | Braun at one turn (#154); the other three at none | at no turn | 7, 3, 5 and 4 turns |
| Poeltl on the Top-5 | three turns (#82, #106, #111) — the #1 at two of them | — | — |

The empty-roster #1 from #82 on reads LaVine, LaVine, Gafford, Gafford,
Gordon, Braun, Braun; the card said Poeltl, LaVine, Poeltl, Gillespie,
Vassell, Vassell, Vassell — the roster as it stood decided five of those
seven, which is the card doing its job (the empty-roster read is a
value-only read).

## 9. The owner's two proposals, answered on this room

### 9a. "After Insert at #, say '(player) inserted at #' and re-number every pick after it" (D59-1)

What the tracker does today, on both planes [EVIDENCE: `docs/draft-deck.html`
`insertPick`, `scripts/hoops.py` `insert_pick`, the tool log as pasted,
`m59_tool_vs_truth.json`]: the insert splices the pick into the state,
recomputes the snake seat of every pick after it, and writes ONE log line,
"✎ inserted Jalen Green at #97 → Seat 1; #97–#105 → #98–#106 (9 shifted,
slots recomputed)". The state is right from that moment (the replay proved
it: every roster matches the recap). The history box is not: its earlier
lines are plain text written when the picks were fed, so they keep their
old numbers and old seats. Three consequences showed up in this room, all
owner-visible:

- **Two of the owner's own picks never read as the owner's.** Queta was fed
  before the #97 insert and logged as "✓ (R9) #105: Neemias Queta → Seat
  9"; Washington was fed before the #121 insert and logged as "#128 → Seat
  8". Both moved to seat 10 when the inserts landed, and the log never said
  so. Neither got "(YOU)", neither got the card echo (rank, gap, the
  round-9+ reminder) that every other owner pick got — and those were the
  two picks the card disagreed with most (Queta: card #52, 0.244 behind
  Poeltl).
- **The standing UNKNOWN keeps its old number in its name.** "Hansen" was
  logged as "UNKNOWN #125" and sits at #126 after the #121 insert. The
  status strip computes its fix instruction from position, so "126- Name"
  is what it says and that is correct; the roster list and the history
  line still say #125.
- **Nothing in the box says which lines moved.** The owner's request is
  exactly the missing sentence: which player went in, at which number, and
  the new numbering of everything after it.

The change, red-first, both planes (page and `hoops.py`, parity held by
`check_parity.py`):

1. The insert line becomes "✎ Jalen Green inserted at #97 → Seat 1; #98–#106
   re-numbered (9 picks shifted)".
2. Every earlier history line that names a pick number at or after the
   insert point is re-numbered and re-seated from the state (the log keeps a
   pick index on each pick line, so the re-render is mechanical: "#105 →
   Seat 9" becomes "#106 → Seat 10 (YOU)" for Queta).
3. A pick that the shift moves onto the owner's seat gets the "(YOU)" mark
   and a fresh card echo against the card as it stands now, labelled "(card
   as of now)" because the card at the time of the pick is gone; a pick the
   shift moves off the owner's seat loses its mark.
4. A standing UNKNOWN is renamed to its new number in the state and in the
   log ("UNKNOWN #126"), so the three places that name it agree.
5. Undo of an insert reverses all of the above (the page already keeps the
   pre-insert state).

Tests before code: `test_draft.py` cases for the re-numbered lines, the
re-seated owner pick and the renamed UNKNOWN; `live_replay_dom.mjs` on this
room's 161 events asserting the two Queta/Washington lines read "(YOU)"
after the inserts and the UNKNOWN reads #126; `full_dom_check.mjs` S2
extended. Ships as deck v38 with no board change (no pool edit, no
ordering change), so the artifact republishes on the page's own diff.

### 9b. "The tool suggested Poeltl, who was not taken for three more rounds; was it costing me higher-valued players that would not last?" (D59-2)

The worry is a real property of the card and the room measured it. The 🎯
is the top blend score and it is price-blind by design: it does not know
where the room will take a man, only what he is worth to this roster. The
survival chips know the first thing and sit on the same card, but they do
not touch the 🎯. So when the best-value row is a man the room prices far
below his value, the card says "take him now" even when he would wait, and
it says nothing about the row one line down that will not.

What happened at #82, from the card the owner saw [EVIDENCE:
`m59_deckcard_v37.json` turn 82, `arena/data/states/draft_state_59.json`]:

| Top-5 at #82 | blend | gap to 🎯 | survival to #87 | chip | went |
|---|---|---|---|---|---|
| Jakob Poeltl 🎯 | 0.998 | — | 0.829 | quiet | #129 |
| Zach LaVine | 0.994 | 0.004 | 0.729 | quiet | #94 |
| Jalen Suggs | 0.990 | 0.008 | 0.765 | quiet | #95 |
| Miles Bridges | 0.988 | 0.010 | 0.645 | quiet | #102 |
| Josh Hart | 0.981 | 0.017 | 0.623 | quiet | #101 |

Every one of the five was quiet (no BUY NOW, no TOSS-UP) and every one of
the five was still there at #87, so at this particular turn the card's
pick cost nothing by waiting: the owner could have taken any of the five at
#82 and the other four were available at #87. The cost came from taking
none of them (Sharpe, card #12, and then Edgecombe, card #20): hindsight
prices the two turns at +0.112 and +0.107 categories a week. At #106 the
card said Poeltl again, 0.244 ahead of Queta, and he was still there at
#111 (survival 0.614) and went at #129. Poeltl's price on the pool is
Yahoo ADP 121.6, XRank 114, market rank 187 on the card; he went #82, #82
and #87 in the three rooms before this one, so "three rounds early" is this
room, not the pattern.

Across the last four live rooms, every owner turn where the owner passed on
the 🎯, by how far the 🎯's market rank sat below the pick [EVIDENCE:
`arena/mocks/target_wait.py` → `arena/results/target_wait_2026-10-01.json`]:

| the 🎯's market rank vs the pick | turns passed on | 🎯 still there at the next owner turn | still there two turns on |
|---|---|---|---|
| deep (24+ slots below the pick) | 5 | 4 | 1 of 5 |
| mid (12 to 23) | 4 | 2 | 1 of 3 |
| near (under 12) | 10 | 5 | 0 of 9 |

The deep 🎯s wait one turn (Poeltl ×3, Braun; LaVine at +31 did not) and
rarely two; the near ones survive the five-pick turn and never the next.
That is the owner's intuition, measured, and it is the shape the survival
model already encodes (0.829 for Poeltl at #82 against 0.213 for Derrick
White at #39). What the measurement does not say is that passing on the
🎯 paid: the survival-aware roster for this room — LaVine at #82 and Poeltl
at #87, the two rows the card would have named in that order if it read
its own chips — grades 26.36 percent (ECW 5.296), against 39.18 percent for the self-consistent follow-card chain and 20.38 as drafted for the card as it is
and the as-drafted roster in §2. The order matters less than taking one
of the rows at all.

What to change, in two sizes, both red-first, the owner picks (D59-2):

- **The small one (advice line, no ordering change).** When the 🎯's
  modeled survival to the next owner turn is 0.75 or higher and a Top-5 row
  within 0.01 of it in blend has survival at or below 0.50, the advice line
  says so: "🎯 Poeltl likely waits (83%); LaVine (0.004 behind) is a coin
  flip (51%) — LaVine now, Poeltl next turn". Display-only, same bar as
  every other advice feature; measured on the next live rooms.
- **The large one (a two-turn 🎯).** Order the card by the expected value
  of the pair of turns: the row now plus the best row the survival model
  expects at the next turn, so a deep 🎯 drops to second when a near-equal
  scarce row would be lost. A ranking change to the card's primary signal,
  so it carries the D58-3 bar first: title odds not below the current
  card's on two seed sets across the eight live rooms, pre-registered,
  before it ships.

Default if silent: the small one for v38, the large one as a
pre-registered arena experiment after the preseason refresh. On this room
the small line would have fired at #82 (LaVine) and #106 (Washington 0.014
behind at 0.576, no) — once, and the one time was the turn the room is
about.

## Watchlist

- **D59-1 and the v38 build**: the insert re-numbering is the next deck
  change; this room's 161-event log is its regression case.
- **D59-2's advice line**: fires at #82 of this room and nowhere else;
  the next live room is its first out-of-sample test.
- **Yang Hansen** (D59-3): poolless and drafted #126 in a public room; two
  outlets on his role and a line at the next pull.
- **The #39 pattern**: Derrick White has been the card's 🎯 at #39 in
  three of the four rooms and the owner has taken someone else each time
  (Kyrie, Kessler; hindsight +0.119 and +0.237). Not a card question; it
  is on the sheet as D59-4 so the owner can say whether the card is
  missing something about White.
- Carried: Morant's deck tag (D58-1, shipped today), the UPSIDE chip
  (D58-2), the ceiling experiment (D58-3), the league settings screenshot
  (D-G5), the draft room's positions (D-G3), the fresh Yahoo ADP paste,
  the preseason projection refresh (WO-5).

## Open-item receipts

| item | query run (2026-10-01) | dated finding |
|---|---|---|
| (this analysis) | machine replay only — no web research in this report | pull receipts for the window live in `after-report-2026-10-01.md` |
| Jalen Duren, Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the daily pull's dedicated queries, same day (after-report-2026-10-01.md) | all HELD on 2026-10-01; nothing in this room touches them |
| Yang Hansen | none this report — poolless, drafted #126 by seat 6 | pool-completeness item for the next pull (D59-3) |

## Bounds

- Championship figures are on the real eight-team bracket (E14); the
  arms use 18,000 CRN seasons on three seeds.
- The room was drafted on v37 and graded on v37's lines. The 184
  cross-plane line differences found today (WO-1) are the deck's lines
  here; a different line set grades every room differently.
- The follow-the-card chain is the retro's Python port of the card, not the
  deck's JS. Measured here: the two agree on the 🎯 at 12 of 13 turns; at
  #111 they tie exactly on blend (0.9835) and the page breaks the tie by
  ΔECW (Gillespie, the D51R-4 rule) while the port keeps the older
  name-order rule (Vassell). §3 reads the page; the owner took Gillespie,
  hindsight-best. The port's tie-break is a harness item (D59-5).
- The target-wait table pools four rooms of random public opponents; it
  says how the public prices the card's deep names, not how the eleven
  league-mates will.
- The survival-aware arm is one counterfactual on one room; it is evidence
  for the advice line's wording, not for the two-turn 🎯.
- The advisor's "spoke" is the replay's read of the engine at each
  owner turn; the owner's screen at the time is not recorded.
- §9a describes code not yet written; the numbers it rests on are this
  room's replay.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D59-1 | Insert at #: the history box gets "(player) inserted at #N to Seat S; #N+1–#M re-numbered", every earlier pick line after the insert point is re-numbered and re-seated from the state, a pick moved onto your seat gets "(YOU)" and a card echo marked "card as of now", a standing UNKNOWN is renamed to its new number, undo reverses it all; both planes, red-first, deck v38, no board change. Build it now? | yes, next deck change |
| D59-2 | Survival-aware 🎯: (small) an advice line when the 🎯 likely waits (≥0.75) and a Top-5 row within 0.01 likely does not (≤0.50), display-only, in v38; (large) a two-turn 🎯 that re-orders the card, behind the D58-3 bar (title odds not below the current card's on two seed sets across the eight live rooms) as a pre-registered arena experiment. | small in v38; large after the preseason refresh, bar first |
| D59-3 | Yang Hansen (POR, C): no row on either plane, drafted #126 here. Add a row at the next pull with two outlets on his role and a line from his 2025-26 numbers? | yes, next pull, two outlets |
| D59-4 | Derrick White at #39: the card's 🎯 there in three of four rooms, passed on each time (Kyrie, Kyrie, Kessler), hindsight +0.119 / +0.237. Is there a reason about White the card is missing (role, health, the Boston rotation) that belongs in his row or his tag, or does the round-9 rule extend to "take the 🎯 at #39 when the gap is under 0.01"? | nothing changes on the card; the owner says what he sees in White |
| D59-5 | `live_retro.py`'s card port breaks exact blend ties by name order (its pre-D51R-4 rule) while the page breaks them by ΔECW; one turn here (#111). Align the port with the page's rule for rooms drafted on v33 or later, keeping the old rule by pool tag for the earlier rooms, and re-run mocks 56 to 59's chains for a byte-identical check? | yes, with the next harness change; this room's numbers stand (§3 reads the page) |
| D58-1 | Ja Morant's deck tag | shipped today (v37, `inj-risk`); closed |
| D58-2 | UPSIDE chip from round 9 | carried: at the final pre-draft refresh |
| D58-3 | the ceiling experiment | carried: design doc first; the D59-2 large option shares its bar |
| D58-4 | NBA-team stack ⚠ at three or more | carried: next deck build, red-first |

## Provenance

- Inputs: the owner's tool log and Yahoo recap (this session, 2026-10-01),
  transcribed verbatim into `arena/data/events/m59_tool_events.json` and the
  recap into the state by the tracker's resolver (`hoops.py draft resync`).
- Every number is read from `arena/results/m59_*.json` and the debrief; the
  arms use 18,000 CRN seasons (seeds 11/23/47) on the real eight-team bracket;
  the audit and the advisor replay ran the v37 page's own engine under node.
- Not verified: nothing here rests on web research.
