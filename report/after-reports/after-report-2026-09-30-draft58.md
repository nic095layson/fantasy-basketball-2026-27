# After-report — draft_58: seventh live-human mock from the REAL slot 10, the second room on the concise card, and the first graded on the league's real bracket

**Owner request (2026-09-30, verbatim):** "Live pick by pick mock draft for
your analysis:" — the deck tool's pick-by-pick feed and Yahoo's round-by-round
recap (the authoritative record), pasted while the rookie intake and the D-R5
wording change were being finished.

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (the real league slot;
random humans — a practice rep, not opponent intel; none of the eleven seat
names is a modeled league-mate). **Deck used:** v35 (rev `6426a59`, the 9/30
daily-pull build with the role pass; pool sha `3db2c63af0c3`, 334 rows;
Porziņģis veto live; the advice line still in its pre-D-R5 wording). **Method:**
the recap was resolved to pool names by the tracker's own resolver (156 of 156,
no unresolved name) and the state checked snake-consistent; the grade is the
deck plane's machine-derived retro (`yahoo-fantasy-basketball`
`arena/results/m58_*.json`, debrief `debrief_2026-09-30_mock58_slot10.md`, deck
card replayed from the v35 page the owner drafted against). **This is the
first room graded on the league's real playoff bracket** (E14 shipped
2026-09-30: 8 of 12, no byes), so its championship figures are not comparable
to the mock-57 debrief's headline (35.23 percent on the old bracket; 27.44
restated) except through the restatement table. Every figure below is read
from those files; none is eyeballed. Verification: this file passes
`report/check_report.py`; receipts in the section below.

Pull window: 2026-09-30 → 2026-09-30 (analysis run 2026-09-30 against the
v35 pool and the 9/22 market file; not a roster pull — the 9/30 pull-log rows
cover the window).

**Headline.** Rank 1 of 12 in expected weekly category wins by the widest margin
of the seven live rooms (5.667 against the next seat's 4.932) and favored in
all eleven head-to-heads; title odds **36.75 percent on the league's real
bracket**, the first room graded on it. The card's 🎯 was taken at 9 of 13
turns, every pick sat on the Top-5, and exactly one turn cost anything:
#39, Kyrie Irving over Jalen Williams, where hindsight's best swap (Derrick
White, +0.119 categories a week) is worth four points of title odds. Following
the card at every turn would have been 40.89 percent. Tool state was clean
(zero drift across 158 events, a HALT and four page reloads handled), and
the survival chips scored a Brier of 0.189 against a 0.246 base rate in
their fifth out-of-sample room. The owner's late-round pitch (upside over
floor from round 9) is taken up in §9 with what the instruments can and
cannot say about it.

## 1. Validation vs the Yahoo recap

| check | result |
|---|---|
| picks in the recap | 156; every "Last, First" line resolved to a pool name by the tracker's resolver (diacritics, suffixes and "P.J." included; zero unresolved, zero surname mismatches) |
| snake attribution | all 156 seats match the round parity; the owner's 13 picks sit at #10, #15, #34, #39, #58, #63, #82, #87, #106, #111, #130, #135, #154 |
| owner's roster | Haliburton, Towns, Anthony Davis, Kyrie, Anunoby, Pritchard, Miles Bridges, Poeltl, Morant, PJ Washington, Gillespie, Herbert Jones, Gafford — identical to the recap's "My Team" |
| poolless names | none — every pick in this room is a pool row |
| cast | seats 1–12: Alonzo, Elie, Noel, Art, Michael, Gabe, Brandon, Mindaugas, Cyril, **David (10)**, Gamze, Alan |
| positions shown by the draft room vs the pool | **29 of 156 differ**, every one the pool listing MORE positions than the room (see §7) |
| state | `arena/data/states/draft_state_58.json`, md5 `84547309be00afd40ed15adcd72ff367` |

## 2. The team, replayed

[EVIDENCE: `m58_final.json`, `m58_arms.json`, `m58_followcard_grade.json`,
the debrief's headline table]

| readout | as drafted | follow the card (self-consistent) | card's #1 at #39 only |
|---|---|---|---|
| ECW (cats/week vs the average opponent) | **5.667**, rank 1 (next 4.932, Elie) | 5.744, rank 1 | 5.764, rank 1 |
| head-to-heads favored | 11 of 11 | 11 of 11 | 11 of 11 |
| championship rate, 18,000 seasons, real 8-team bracket | **36.75%** (rank 1) | **40.89%** | 40.17% |
| playoff rate | 99.99% | 100.00% | 99.99% |
| swaps | none | Maxey at #10, Jalen Williams at #39, LaVine at #82 | Jalen Williams at #39 |
| category rank, weekly model | FG% 4 · FT% 5 · 3PTM 4 · PTS 5 · REB 5 · AST 8 · ST 2 · BLK 3 · TO 2 | | |
| category rank, 13-man z-sum | FG% 4 · FT% 5 · 3PTM 4 · PTS 2 · REB 3 · AST 6 · ST 2 · BLK 3 · TO 3 | | |
| board rank (kept-total z-sum) | 1 (+17.62; next +6.25) | | |

The shape is the one the owner has drafted in every live room: steals,
blocks and turnovers locked, points and rebounds top-five, assists the
conceded category (8th weekly). Hindsight's single-swap ledger names one
turn: Derrick White at #39 (+0.119 cats/week, 40.81 percent alone); the
next-best legs are Maxey at #10 (+0.007), Grimes at #135 (+0.033) and
Filipowski at #154 (+0.001), all inside noise. On the same bracket, mock 57's
roster restates to 27.44 percent as drafted and 41.43 following the card,
so this draft is about nine points stronger as drafted with the same seat
and the same instrument.

## 3. Pick by pick — card vs owner vs hindsight

| pick | deck 🎯 (Top-5) | owner took | card rank · gap (blend) | hindsight best single swap (ΔECW vs final rosters) |
|---|---|---|---|---|
| #10 | Karl-Anthony Towns (Karl-Anthony Towns, Tyrese Maxey, Jalen Johnson, Tyrese Haliburton, Anthony Davis) | Tyrese Haliburton | #4 · +0.006 | Tyrese Maxey +0.007 |
| #15 | Karl-Anthony Towns (Karl-Anthony Towns, Chet Holmgren, Anthony Davis, Evan Mobley, Kevin Durant) | Karl-Anthony Towns | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #34 | Anthony Davis (Anthony Davis, Jalen Williams, Derrick White, Dyson Daniels, Desmond Bane) | Anthony Davis | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #39 | Jalen Williams (Jalen Williams, Derrick White, Desmond Bane, Kyrie Irving, Dyson Daniels) | Kyrie Irving | #4 · +0.009 | Derrick White +0.119 |
| #58 | OG Anunoby (OG Anunoby, Payton Pritchard, Tyler Herro, Darius Garland, Damian Lillard) | OG Anunoby | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #63 | Payton Pritchard (Payton Pritchard, Tyler Herro, Darius Garland, De'Aaron Fox, Coby White) | Payton Pritchard | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #82 | Jakob Poeltl (Jakob Poeltl, Ja Morant, Coby White, Zach LaVine, Miles Bridges) | Miles Bridges | #5 · +0.017 | none positive (the pick was hindsight-best) |
| #87 | Jakob Poeltl (Jakob Poeltl, Ja Morant, Jalen Suggs, Josh Hart, Coby White) | Jakob Poeltl | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #106 | Ja Morant (Ja Morant, Josh Hart, Collin Gillespie, Devin Vassell, Quentin Grimes) | Ja Morant | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #111 | PJ Washington (PJ Washington, Daniel Gafford, Cason Wallace, Aaron Gordon, Collin Gillespie) | PJ Washington | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #130 | Collin Gillespie (Collin Gillespie, Quentin Grimes, Herbert Jones, Fred VanVleet, Saddiq Bey) | Collin Gillespie | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #135 | Daniel Gafford (Daniel Gafford, Herbert Jones, Quentin Grimes, Christian Braun, Saddiq Bey) | Herbert Jones | #2 · +0.005 | Quentin Grimes +0.033 |
| #154 | Daniel Gafford (Daniel Gafford, Malik Monk, Saddiq Bey, Jerami Grant, Kyle Filipowski) | Daniel Gafford | #1 · +0.000 | Kyle Filipowski +0.001 |

🎯 taken 9 of 13; Top-5 row 13 of 13

[EVIDENCE: `m58_replay.json`, `m58_deckcard_v35.json`, `m58_hindsight.json`;
card ranks are the deck's own JS replayed on the v35 page — the live echoes
in the tool log match them at all four off-card turns]

Reading: the four off-card picks were all Top-5 rows a hair behind the 🎯
(0.006, 0.009, 0.017, 0.005 in blend score), and three of the four were
hindsight-neutral or better — Haliburton at #10 cost 0.007 against Maxey,
Miles Bridges at #82 was hindsight-best outright, Herbert Jones at #135
trailed Grimes by 0.033. The one that mattered was #39: the card said Jalen
Williams (+0.097 by hindsight), the hindsight-best was Derrick White
(+0.119), the owner took Kyrie (a top-two value that fit this roster worst
of the four, because assists were already the conceded category and Kyrie's
percentages sit where the roster was already strong). From round 9 on the
owner took the 🎯 at four of five turns (the fifth off by 0.005), which is
the round-9 rule (D54-1) working as the debriefs said it would.

## 4. Tool-state integrity — the deck's board vs the recap, on the v35 page

The owner's tool log was rebuilt as an event list (158 events: 155 direct
feeds, the shared token wherever the echo said "assumed over" or "only X
left" — fifteen of them, Barnes, Mitchell, Jalen, Murray, Ball, Brown,
Williams, White twice, Wagner, Allen, Wiggins, Collins, Sheppard, Reed; the
raw UNKNOWN "Gianis" and its `6- Giannis Antetokounmpo` fix; and the HALTED
"Murray" feed the deck refused because its best match, Jamal Murray, was
already drafted) and replayed through the real v35 page in headless Chromium
[EVIDENCE: `m58_tool_vs_truth.json`, `arena/data/events/m58_tool_events.json`]:

| finding | detail |
|---|---|
| positions differing from the recap | **0 of 156**; owner's roster identical |
| echo lines asserted | 158 of 158 (each feed's resolved name, the UNKNOWN, the fix, the HALTED refusal) |
| clock text under the feed title | correct after all 158 events |
| page errors | 0 |
| the halt, live | "Murray" before #68 stopped the feed with the fuller-name instruction; the owner resent "Dejounte Murray" and #68 to #70 logged in order — the D51 surname guard working as designed |
| page reloads | four ("resumed" at 26, 63, 70 and 156 picks) — the autosave restored the board each time with no drift |
| off-card echoes reproduced | #10 Haliburton (card #4, 0.006 behind 🎯 Towns), #39 Kyrie (#4, 0.009 behind 🎯 Jalen Williams), #82 Miles Bridges (#5, 0.017 behind 🎯 Poeltl), #135 Herbert Jones (#2, 0.005 behind 🎯 Gafford, with the round-9+ reminder) |

Third clean public room in a row on the concise card's page family
(mocks 56, 57 and 58 drifted none; mock 54 drifted 13). The HALT and the four
reloads are the new mechanics exercised here, and both behaved.

## 5. Survival chips — fifth out-of-sample room for the refit

[EVIDENCE: `m58_survival.json`; the debrief's survival table]

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 58 (out of sample) | 48 | 0.444 | 0.562 | **0.189** | 0.246 |
| pooled with every earlier scored room (51 to 57) | 401 | 0.407 | 0.681 | 0.306 | 0.217 |

By chip in this room: BUY NOW 8 rows, mean predicted 0.139, 2 survived;
TOSS-UP 16 rows, 0.309, 5 survived; quiet rows 24, 0.636, 20 survived; no
survivor was called at two percent or less. The price-only refit beats the
base rate in its fifth straight out-of-sample room (0.178 in mock 57, 0.189
here). The pooled row still carries the pre-refit rooms and is a history,
not a grade.

## 6. The punt advisor, replayed

[EVIDENCE: `m58_advisor.json`, 23 pre- and post-pick moments across the
owner's turns]

The advisor never spoke. At #58 the strip watched assists and points
("losing them to most of the room this pick", the owner beating 17 and 18
percent of the room in them) and the two-turn hysteresis held, so no punt
was ever advised and no category was ever called dead; the final roster
ranks assists 8th weekly, the same conceded category as mocks 56 and 57.
The build strip read the same roster the card was scoring: strong in
points, rebounds and turnovers, winnable in the percentages, steals and
blocks, assists soft.

## 7. Two Yahoo position displays disagree — 29 of 156 drafted men, again

The 9/29 room (mock 57) showed 29 of 156 drafted men with fewer positions
than the pool carries; this room shows the same count, and again the pool is
a superset in every case: 11 extra SG listings, 10 SF, 6 PF, 2 PG [EVIDENCE:
`scratchpad m58/positions_check.json`; the recap as pasted]. On the owner's
roster: Payton Pritchard (room PG; pool adds SG), Miles Bridges (room PF; pool
adds SF), PJ Washington (room PF,C; pool adds SF), Herbert Jones (room SG,SF;
pool adds PF). Two rooms a day apart agreeing is what turned D57-1 into the
gap audit's D-G3 (set both planes' positions from the draft room before Oct
14); nothing new to decide here, one more data point that the room's display
is stable.

## 8. Repeat names on the card — the audit, re-run on this room

Same instrument as mocks 56 and 57 (`repeat_names_audit.mjs`, seven other
rooms' owner rosters substituted in at each turn, an empty roster, value-only
and ΔECW-only orders) [EVIDENCE: `m58_repeat_names_audit.json`]:

| readout | mock 58 | mock 57 | mock 56 |
|---|---|---|---|
| owner turns where the #1 changes under at least one other room's roster | **10 of 13** | 10 of 13 | 9 of 13 |
| owner turns where the #1 changes under an empty roster | **8 of 13** | 11 of 13 | 11 of 13 |
| the mock-56 repeat names (Brook Lopez, Cameron Johnson, Braun, Eason) on this room's Top-5 | Braun at one turn (#4 once); Lopez, Cameron Johnson and Eason at no turn | at no turn | on the Top-5 at 7, 3, 5 and 4 turns |

The empty-roster #1 from #106 on is Daniel Gafford at every turn; the card
said Morant, PJ Washington, Gillespie, Gafford and Gafford — the roster as it
stood decided three of those five, and the owner took the card's man at four.

## 9. The owner's late-round pitch: upside over floor from round 9

The owner's pitch, verbatim in spirit: from round 9 the card's "safe" 🎯
(Gafford, a third Dallas man; Morant over a rookie such as Darryn Peterson)
should give way to high-upside picks, because a late bust costs a waiver
move and a hit is a season-long edge, and this can be tightened once
preseason projections land.

What the instruments can say today [EVIDENCE: the deck's engine block,
`arena/arena.py` `STRATEGIES`, `arena/README.md` baseline, this room's
files, the v36 boards]:

- **The card has no ceiling column.** Every line is a point projection and
  the weekly model's only spread is per-game noise plus availability. A
  rookie's ceiling is not in his row, so "safe beats upside" in every sim
  and every debrief is partly the instrument talking. The round-9 rule
  (D54-1: 15 of 16 across four rooms) was measured on that model and is a
  statement about means, not about distributions.
- **The arena's existing "upside" persona is not this pitch.** It draws at
  full value through injury discounts (`risk="upside"`) and scored 2.8
  percent championships against `safe_floor`'s 14.9 in the baseline
  tournament. That measures ignoring injury risk, not chasing young
  ceilings; nothing in the ledger has measured the owner's idea yet.
- **The "safe" pick was not priced as safe.** Ja Morant carries no
  availability tag on the deck (value at 1.00, rank 66 on v36) while the kit
  prices him at 60 games (rank 139). The card's #106 🎯 was a risk pick the
  deck did not call a risk; Darryn Peterson sits at 142 on the deck and 145
  on the kit after today's intake (155 and 174 on the v35 pool the room
  used). The gap between them on the board is mean production (23.5 / 7.5
  against 18.2 / 3.8), and a ceiling case is exactly what the mean cannot
  carry.
- **Late slots are churn slots in this league** (unlimited moves, daily
  lineups, two IL+ slots; 16 to 87 moves a season — gap audit §5), which is
  the structural argument for the pitch: the downside of a late miss is
  one waiver claim. The weekly model does not know this (E16).
- **The Dallas stack was flagged, not priced.** The card shows "NBA-team
  stacks: DAL:2" as a display line and never penalises the order; the arena's
  council persona carries a stack penalty the deck does not. Three men from
  one team share a schedule (a two-game week hits all three) and a
  frontcourt rotation.

What would settle it, in order: a display-only UPSIDE chip from round 9
built from the 9/29 sleepers and breakouts tags and the rookie rows
(D58-2), a pre-registered arena experiment with a projection-uncertainty
term per player (D58-3), and a Morant availability twin (D58-1). The owner's
timing is right: the ceiling inputs are the preseason projections, so the
build belongs at the final pre-draft refresh.

## Watchlist

- **Morant's availability on the deck** (D58-1): untagged at 1.00 while the
  kit carries 60 games; two outlets on his 2025-26 games at the next pull.
- **v36 is the next room's page**: Peterson 142, Wilson 123, Lendeborg 85
  and Boozer 51 on the deck after the rookie intake, and the D-R5 advice
  wording live; the first room on it re-checks the wording under a
  negative gap.
- **D-G3 positions** before Oct 14: the room's display differed from the
  pool on 29 of 156 men in both of the last two rooms.
- **The preseason projections** (owner): the trigger for the ceiling chip
  and the upside experiment (D58-2, D58-3).
- Carried: the league settings screenshot (D-G5), Duren's deadline, the
  fresh Yahoo ADP paste.

## Open-item receipts

| item | query run (2026-09-30) | dated finding |
|---|---|---|
| (this analysis) | machine replay only — no web research in this report | pull receipts for the window live in `after-report-2026-09-30.md` §8 and the rookie intake's receipts |

## Bounds

- Championship figures are on the real eight-team bracket (E14, shipped
  today); earlier debrief headlines are on the six-team bracket and compare
  only through `report_2026-09-30_bracket_restate.md`.
- The room was drafted on v35; the grade is on v35's lines. Today's rookie
  intake moved five of those lines, so the next room grades differently on
  Peterson, Wilson, Brown, Acuff, Lendeborg and Boozer.
- The follow-the-card chain is the retro's Python port of the card, not the
  deck's JS; the two agree on the 🎯 at every turn here, and the arms stage
  now applies the owner veto (a harness defect found and fixed in this
  grading — the earlier rooms' chains carried no vetoed name).
- The survival pool's 401-row Brier includes the pre-refit rooms.
- §9 states what the instruments cannot see; it measures nothing new.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D58-1 | Ja Morant: the deck row is untagged (availability 1.00, rank 66) while the kit prices 60 games (rank 139). Twin the kit's view onto the deck — an `inj-risk` tag at 0.78 with two outlets on his 2025-26 games — so the card stops calling him a safe late pick? | yes, at the next pull, two outlets |
| D58-2 | An UPSIDE chip on the card from round 9, display-only like LEAN and LINEUP CAP: a row carries it when its man is a 2026 first-round rookie or on the 9/29 sleepers/breakouts list, with no ordering change. Build it red-first at the final pre-draft refresh, when the preseason projections give the ceilings something to stand on? | yes, at the final pre-draft refresh |
| D58-3 | A pre-registered arena experiment for the owner's pitch: council through round 8, then from round 9 prefer the highest-ceiling candidate within 0.05 cats/week of the 🎯, scored on the real bracket under a weekly model with a per-player projection-uncertainty term (rookies and breakouts wider). Bar: title odds not below the card's on two seed sets. | design doc first; run after the preseason projections land |
| D58-4 | NBA-team stacks: escalate the display line to a ⚠ at three or more men from one team, with the reason (one schedule, one rotation), no ordering change. | yes, next deck build, red-first |
| D58-5 | The arms-stage veto fix is shipped with this grading; mocks 55 to 57's chains carried no vetoed name, so their numbers stand. Re-run them anyway for a byte-identical proof? | no; the check on the swap lists is the proof |

## Provenance

- Inputs: the owner's tool log and Yahoo recap (this session, 2026-09-30),
  transcribed verbatim into `arena/data/events/m58_tool_events.json` and the
  recap into the state by the tracker's resolver (`hoops.py draft resync`).
- Every number is read from `arena/results/m58_*.json` and the debrief; the
  arms use 18,000 CRN seasons (seeds 11/23/47) on the real eight-team bracket;
  the audit and the advisor replay ran the v35 page's own engine under node.
- Not verified: nothing here rests on web research.
