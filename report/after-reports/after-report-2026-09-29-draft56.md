# After-Report — draft_56: fifth live-human mock from the REAL slot 10, the point-guard trio, and the repeat-name audit

**Owner request (2026-09-29, verbatim):** "I have another live mock draft
results for you. I want to say- this was the smoothest draft, using the tool
wise, and - if everything goes according to plan - how I would actually want
to draft my team. I like the idea of strong PGs with Hali, Dame and Kyrie.
Please analyze:" — then the deck tool's pick-by-pick feed and Yahoo's recap
(the authoritative record). Mid-analysis, a second ask: "Although this is
the first time I've assembled a trio of star point guards, the same fantasy
suggested players were on my card this draft as previous drafts, such as OG,
Brook Lopez, Cam Johnson, Braun, etc. I just want to ensure that the system
does not have a bias to continue suggesting these players unless actually,
statistically and categorically warranted." — answered in §7.

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (the real league slot;
random humans — a practice rep, not opponent intel). **Deck used:** v31 or
v32 — the 9/29 pull build either way (`data/players.csv` sha `c0bf82bf4d39`
on both, same engine; only the resolver's dot-folding differs), Porziņģis
veto live. **Method:** the recap was resolved to pool names by the deck's
own resolver (156 of 156, no unresolved name) and the state checked
snake-consistent; the grade is the deck plane's machine-derived retro
(`yahoo-fantasy-basketball` `arena/results/m56_*.json`, debrief
`debrief_2026-09-29_mock56_slot10.md`, deck card replayed from the deck he
drafted against, `rev e2b45ed`). Every figure below is read from those
files; none is eyeballed. Verification: this file passes
`report/check_report.py`; receipts in the section below.

Pull window: 2026-09-29 → 2026-09-29 (analysis run 2026-09-29 against the
9/29 pool and the 9/22 market file; not a roster pull — the 9/29 pull-log
rows cover the window).

**Headline.** The strongest room yet from the real seat on every readout:
ECW **5.760** cats/week, rank **1 of 12** (next seat 4.850), favored in
**11 of 11** head-to-heads, season-shape 11 of 11, board rank 1 by a margin
of 17.7 z, championship rate **54.94%** over 18,000 simulated seasons
[EVIDENCE: `m56_final.json`, `m56_arms.json`]. Mocks 51–54 from the same
seat read 5.610 / 55.03%, 5.634 / 47.94%, 5.563 / 38.53% and 5.552 / 49.36%.
The owner took the card's 🎯 at **10 of 13** turns (mock 54: 8) and a Top-5
row at 11 of 13; the round-9+ rule from D54-1 was broken once (#130) against
three times in mock 54. The tool board finished **identical to Yahoo's
recap at all 156 positions** (§4). The point-guard trio did not buy
assists — the roster ranks 10th of 12 there — it bought the room's best
free-throw and turnover columns (§6). The repeat-name audit found no bias in
the card's mechanism and a real question in three projection lines (§7).

---

## 1. Validation vs the Yahoo recap

| check | result |
|---|---|
| picks in the recap | 156; every "Last, First" line resolved to a pool name by the deck's own resolver (diacritics and suffixes included; zero unresolved, zero surname mismatches) |
| snake attribution | all 156 seats match the round parity; the owner's 13 picks sit at #10, #15, #34, #39, #58, #63, #82, #87, #106, #111, #130, #135, #154 |
| owner's roster | Towns, Haliburton, Mobley, Kyrie, OG Anunoby, Lillard, Poeltl, Cameron Johnson, Turner, Eason, Sheppard, Braun, Brook Lopez — identical to the recap |
| poolless names | none — every pick in this room is a v31 row |
| cast | seats 1–12: Mathew, Cholo, Matthew, İlhan Engin, Shawn, Tom Cruise, Boogie, john, Alonzo, **David (10)**, Bob, shiny |
| state | `arena/data/states/draft_state_56.json`, md5 `e5305ff3b4a1b5c04a18c65e2d67e56c` |

## 2. The team, replayed

| readout | value | evidence |
|---|---|---|
| ECW (cats/week vs the average opponent) | **5.760**, rank 1 of 12 (next 4.850, seat 7) | `m56_final.json` |
| head-to-heads favored | 11 of 11 (per-opponent expected cats 5.25–6.86) | `m56_final.json` |
| season-shape H2H | wins 11 of 11 (cats won per opponent 5–9) | `m56_final.json` |
| board rank (kept-total z-sum) | 1 (+21.52; next +3.83) | debrief |
| category ranks, weekly model | FG% 2 · **FT% 1** · 3PTM 4 · PTS 5 · REB 6 · **AST 10** · ST 3 · **BLK 1** · **TO 1** | `m56_final.json` |
| championship rate, as drafted | **54.94%**, playoff 99.95%, rank 1 | `m56_arms.json` |
| follow-card arm | 62.56% (swaps #39 Derrick White, #63 Payton Pritchard, #130 Jordan Poole); ECW 5.942 | `m56_arms.json`, `m56_followcard_grade.json` |
| best single swap | #15 Tyrese Maxey for Haliburton, 59.96%; then #130 Jordan Poole 58.59%, #39 Desmond Bane 58.01%, #63 Tyler Herro 57.71% | `m56_arms.json` |

## 3. Pick by pick — card vs owner vs hindsight

| pick | card 🎯 | owner | card rank | hindsight best (gain, ECW) |
|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Towns | 1 | none |
| 15 | Tyrese Haliburton | Haliburton | 1 | Tyrese Maxey +0.108 |
| 34 | Evan Mobley | Mobley | 1 | none |
| 39 | Derrick White | Kyrie Irving | 3 | Desmond Bane +0.094 |
| 58 | OG Anunoby | OG Anunoby | 1 | none |
| 63 | Payton Pritchard | Damian Lillard | 7 | Tyler Herro +0.074 |
| 82 | Jakob Poeltl | Poeltl | 1 | none |
| 87 | Cameron Johnson | Cameron Johnson | 1 | Miles Bridges +0.019 |
| 106 | Myles Turner | Turner | 1 | Miles Bridges +0.002 |
| 111 | Tari Eason | Eason | 1 | none |
| 130 | Christian Braun | Reed Sheppard | 16 | Jordan Poole +0.101 |
| 135 | Christian Braun | Braun | 1 | none |
| 154 | Brook Lopez | Brook Lopez | 1 | none |

Hindsight found no better legal pick at 7 of 13 turns. The three
departures from the card: **#39 Kyrie** (card #3, 0.005 behind White;
availability 0.78, first season back from the ACL), **#63 Lillard** (card
#7, 0.021 behind Pritchard) and **#130 Sheppard** (card #16, 0.076 behind
Braun — the round-9+ hint fired and was overridden; Braun was still there
at #135 and the owner took him, so the cost is Sheppard against the best
alternative at #130, Poole, +0.101). The costliest turn by hindsight is a
card pick: **#15 Haliburton** (card #1, availability 0.78, Achilles return)
where Maxey graded +0.108 — the card weighs the 0.78 in and still ranked
him first; the arm says the swap is worth five points of championship. No
LAST CALL pin fired and none was withheld [EVIDENCE: `m56_deckcard_v31.json`].

**The D54-1 test.** Mock 54's report said the next room would count round-9+
deviations against that room's five card-off picks. This room: three
card-off picks in all (5 before), and **one** in rounds 9–13 (#130) against
three in mock 54 (#130, #135, #154). The hint under the feed read "off the
card: Reed Sheppard ranks #16 (0.076 behind 🎯 Christian Braun) — round-9+
rule (D54-1): take the 🎯" and the owner took Sheppard anyway; the arm
prices that turn at 3.65 points of championship (54.94 as drafted, 58.59
with Poole).

**Follow the card — how much better (owner question, 2026-09-29).** The
same weekly model and 18,000-season arms as the as-drafted grade, swaps
pairwise (the displaced man goes to the seat that took the alternative);
as drafted reproduced at 54.94% on the re-run [EVIDENCE:
`m56_followcard_grade.json`]:

| arm | ECW | championship | category ranks that move |
|---|---|---|---|
| as drafted | 5.760 | 54.94% | — |
| card at #39 (White for Kyrie) | 5.806 (+0.046) | 57.67% (+2.7) | PTS 5 to 8, 3PTM 4 to 3, AST 10 to 9 |
| card at #63 (Pritchard for Lillard) | 5.787 (+0.027) | 57.01% (+2.1) | FT% 1 to 2, FG% 2 to 1, 3PTM 4 to 2 |
| card at #130 (Poole for Sheppard) | 5.861 (+0.101) | 58.59% (+3.7) | 3PTM 4 to 3, PTS 5 to 4, AST 10 to 9 |
| both point-guard turns (#39 and #63) | 5.826 (+0.066) | 59.73% (+4.8) | FT% 1 to 2, 3PTM 4 to 1, PTS 5 to 8 |
| all three (self-consistent follow-card) | 5.942 (+0.182) | 62.56% (+7.6) | FT% 1 to 2, 3PTM 4 to 1, PTS 5 to 4, AST 10 to 9 |

Rank 1 and 11 of 11 favored in every arm. The bar the arena registers for a
real difference is two points on two of three seeds (the D54-3 test); the
full follow-card clears it by nearly four times, and the single biggest
item is the #130 turn the round-9+ rule flagged. At #130 the follow-card
arm takes Poole rather than Braun because, with White and Pritchard on the
roster, the card re-ranks and Braun still arrives at #135. The roster's
identity survives every arm: the FT% column drops one place, the threes
column rises to first, assists stay ninth or tenth.

## 4. Tool-state integrity — the deck's board vs the recap

The owner's tool log was rebuilt as an event list (162 feeds and one undo:
bare surnames wherever the echo said "assumed over", "only X left" or
"skipped"; the four raw UNKNOWN texts "Heyonte", "WCJ", "Yendeborg" and
"Brooke Lopez" with their `N- Name` fixes; the #120 "Reed" undo; the
"Mitchell" HALT) and replayed through the real page in headless Chromium on
BOTH the v31 and the v32 page [EVIDENCE: `m56_tool_vs_truth.json`,
`arena/data/events/m56_tool_events.json`]:

| finding | detail |
|---|---|
| positions differing from the recap | **0 of 156** on v31 and on v32 (identical boards) |
| owner's roster | identical |
| echo lines asserted | 163 of 163 (each feed's resolved name, each UNKNOWN, each fix, the undo, the HALT) |
| clock text under the feed title | correct after all 163 events |
| page errors | 0 |
| what the owner did right | every UNKNOWN fixed with the numbered syntax before the next pick; the HALT at #148 answered with the fuller name; the #120 "Reed" ambiguity undone and re-fed as "Paul Reed" |

The "smoothest draft" is measurable: mock 54 drifted 13 positions from an
UNKNOWN followed by a fresh feed; this room drifted none. One harness
finding, not a tool defect: the Chromium harnesses die at launch (SIGTRAP)
when `TMPDIR` points at the session scratchpad path, because the browser's
socket paths exceed the Unix limit — three of three attempts; with the
default temp dir four of four passed. Recorded in `arena/mocks/README.md`.

## 5. Survival chips — third out-of-sample room for the refit

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 56 (out of sample) | 50 | 0.496 | 0.720 | **0.232** | 0.202 |
| pooled, six rooms | 303 | 0.535 | 0.713 | 0.196 | 0.205 |

BUY NOW: 9 rows, 4 gone. TOSS-UP: 11 rows, 5 gone. Quiet: 30 rows, 25
survived. The refit missed this room (0.232 vs a 0.202 base rate) after
beating the base in mocks 54 and 55; pooled over six rooms it stays ahead by
0.009 [EVIDENCE: `m56_survival.json`, pooled the same way as mock 55: the
51/52 refit cards, 53, 54, 55 — 253 rows reproduced exactly before this
room was added].

## 6. The point-guard trio — what "strong PGs" bought, categorically

The owner's frame: Haliburton (#15), Kyrie (#39), Lillard (#63). Read off the
13-man z-sums of the final roster against the room [EVIDENCE:
`m56_players_v31.csv` through `hoops.zscores`, `m56_final.json`]:

| category | owner z-sum | rank of 12 | who carries it |
|---|---|---|---|
| FT% | +4.79 | **1** | Lillard +2.72, Kyrie +1.62, Cameron Johnson +1.04 |
| TO | +5.15 | **1** | Lopez +1.20, Braun +1.06, OG +0.93, Turner +0.93 (Lillard −1.10 and Towns −1.10 are the only drags) |
| BLK | +4.59 | 2 | Turner, Mobley, Lopez, Poeltl, Towns |
| FG% | +4.49 | 2 | the five centers |
| 3PTM | +2.60 | 3 | Haliburton +1.25, Lillard +1.25, Cameron Johnson +1.04, Kyrie +0.93 |
| ST | +1.61 | 3 | Eason +1.98, OG +1.41 |
| PTS | +0.72 | 5 | — |
| REB | +0.32 | 7 | — |
| AST | −2.75 | **9** (10 on the weekly model) | the three guards +4.37; the other ten −7.12 |

So the trio is not an assists build. Kyrie's assists z is +0.26 — he is a
scorer with elite free throws — and Lillard's +1.49 cannot cover five
centers and four wings who sum to −7.12. What the three guards actually
deliver is the room's best free-throw column, a top-3 threes column and the
volume that lets the bigs' FG%/BLK/TO stand — the same shape mock 54 reached
by a different route (AST 10 there too). Measured against the slate's own
assists rule ("the casualty is earned only when the roster is top-4 in at
least five of the other eight at #63"): at #63 the strip read top-4 in
**four** of the other eight (FG% 4, 3PTM 4, ST 3, TO 1), so the rule was not
yet met when Lillard was taken; by the end of the draft it was (six of
eight). The category shape wins anyway — 11 of 11 head-to-heads — because
the room-relative model prices eight strong columns over one dead one, and
the advisor said so at every turn from #63 on ("ADVISE AST", box left empty
by design, D51R-3).

## 7. Repeat names on the card — the bias audit (owner's question)

**The claim to defend:** the card recommends OG Anunoby, Brook Lopez,
Cameron Johnson, Christian Braun (and Eason, Poeltl, Turner) draft after
draft because the arithmetic warrants it, not because the system remembers
them. **Tested four ways, all mechanical** [EVIDENCE:
`arena/mocks/repeat_names_audit.mjs`, `m56_repeat_names_audit.json`,
`m56_repeat_names_history.json`; the kit's market files].

**1. Mechanism.** The card's order is blend50: half availability-adjusted
9-cat value (a per-player number from the projection line), half ΔECW (the
marginal weekly category wins this roster gains against these eleven
rosters). No draft history enters either half: the engine reads the pool,
the state of THIS draft and nothing else; the arena results never feed the
page; the price column is display-only and the survival chips never move a
rank. Name-keyed inputs exist in exactly one place, the judgment layer, and
none of the seven names has a card there (the 29 adjustments are listed in
the deck; the only mention of any of them in code is Poeltl in a
mock-opponent loyalty table that the owner's card never reads).

**2. Roster sensitivity.** At each of the 13 owner turns the deck's own
engine re-ranked the same available pool with the owner's roster from
mocks 51, 52, 53, 54 and 55 substituted in, and with an empty roster:

| turn | actual 🎯 | #1 under the five other rosters | #1 under an empty roster |
|---|---|---|---|
| 10 | Towns | Towns ×5 | Towns |
| 15 | Haliburton | Anthony Davis ×4, Haliburton ×1 | Maxey |
| 34 | Mobley | Mobley ×4, Derrick White ×1 | Holmgren |
| 39 | Derrick White | White ×5 | Holmgren (White #15) |
| 58 | OG Anunoby | OG ×4, Pritchard ×1 | Braun (OG #23) |
| 63 | Pritchard | Pritchard ×4, Poeltl ×1 | Braun |
| 82 | Poeltl | Turner ×4, Poeltl ×1 | Braun |
| 87 | Cameron Johnson | Turner ×4, Cameron Johnson ×1 | Braun |
| 106 | Turner | Turner ×2, Braun ×2, Eason ×1 | Braun |
| 111 | Eason | Lopez ×3, Braun ×2 | Braun |
| 130 | Braun | Braun ×2, Lopez ×3 | Braun |
| 135 | Braun | Braun ×1, Lopez ×4 | Braun |
| 154 | Lopez | Lopez ×5 | Gafford |

The #1 changes at 9 of 13 turns when the roster changes, and at 11 of 13
against an empty roster. The half of the card that reads the roster is
doing real work: Poeltl at #82 and Cameron Johnson at #87 are this
roster's picks (four of five other rosters wanted Turner there), Eason at
#111 is this roster's pick alone. What does not change is the SET of names
the card chooses among from #82 on — Turner, Poeltl, Cameron Johnson,
Eason, Braun, Lopez — because on the deck's value column they are the best
men left at those picks under any roster.

**3. Why they are left.** Seat 10's turns fall at the same picks in every
room, and rooms price these men well below the deck's value for them —
measured, not assumed, over the six live rooms:

| player | deck value # | kit board # | Yahoo XRank / ADP | Hashtag # | Statdunk # (avg) | drafted at (rooms 51–56) | mean |
|---|---|---|---|---|---|---|---|
| OG Anunoby | 27 | 44 | 71 / 66 | 58 | 39 (48) | 58, 74, 63, 58, 47, 58 | 60 |
| Brook Lopez | 58 | 96 | 165 / 101 | 205 | 99 (139) | 116, 81, 154; undrafted in three rooms | 117 |
| Cameron Johnson | 50 | 61 | 172 / 113 | 97 | 102 (92) | 106, 111, 135, 106, 87, 87 | 105 |
| Christian Braun | 54 | 83 | 143 / 121 | 110 | 107 (103) | 135, 156, 145, 145, 111, 135 | 138 |
| Tari Eason | 44 | 67 | 139 / 121 | 145 | 135 (131) | 130, 135, 137, 130, 106, 111 | 125 |
| Jakob Poeltl | 47 | 128 | 114 / 122 | 94 | 121 (98) | 111, 82, 106, 111, 82, 82 | 96 |
| Myles Turner | 52 | 40 | 99 / 99 | 99 | 77 (99) | 102, 87, 87, 87, 71, 106 | 90 |

The card is price-blind, so it is not "targeting values"; it ranks what is
left, and what is left at #82–#154 for seat 10 is this set every time
because eleven strangers keep passing on them. The kit's own 9/22 market
report already lists Cameron Johnson (+52), Braun (+38), Eason (+54) and
Turner (+59) as the board's biggest disagreements with the room, under the
standing owner rule that the board is first-principles and the market a
reference layer (work order, 2026-08-21).

**4. Where the question is real.** An independent 9-cat model (Statdunk)
sides with the deck on OG Anunoby (39 vs 27), Brook Lopez (99 vs 58's
kit-rank 96) and, closer, Turner (77). It does not on **Cameron Johnson**
(102 vs 50/61), **Christian Braun** (107 vs 54/83) and **Tari Eason** (135
vs 44/67); Hashtag agrees with Statdunk on all three. Those three lines were
authored in July–August, re-verified by every news pull since, and never
re-derived; none carries an injury multiplier. If the card has a "bias", it
is inherited from those three projection rows, not generated by the card —
and it is exactly the kind of disagreement the 9/16 integration pass
resolved for five other lines by re-deriving them from current role
research. Separately, Poeltl's two plane ranks differ by 81 places (deck 47,
kit 128) because the deck standardizes over the draftable 156 with
replacement anchoring, which rewards his low-volume FG%/BLK/TO profile;
the market sits with the kit. Both are owner decisions below (D56-1, D56-2).

**Verdict.** No bias in the mechanism: nothing remembers a past draft, no
name is favored by code or judgment, and the roster half of the card
changes the pick at most turns. The recurrence is a property of the room
(seat 10's fixed turns and eleven random drafters who price these men 30–80
slots below the deck) and of three projection lines that deserve the
re-derivation ritual before 10/14. If those lines hold, the card is right
and the rooms are wrong; if they move, the card moves with them the same
day, mechanically.

## 8. What this run answers and asks

- **Answers:** the seat-10 process holds in a fifth random room and set its
  best marks (ECW 5.760, 54.94%); the round-9+ rule cut round-9+
  deviations from three to one; the UNKNOWN fix syntax, the HALT recovery
  and the undo left the tool board identical to the recap; the point-guard
  frame is an FT%/3PTM/TO build with assists conceded, and it wins on that
  shape; the card has no name memory.
- **Asks:** re-derive the Cameron Johnson, Braun and Eason lines (D56-1);
  decide on the Poeltl plane gap (D56-2); the survival chips' third
  out-of-sample miss (D56-3); #15 Haliburton at 0.78 availability as the
  costliest turn by hindsight (D56-4).

## Watchlist

- Haliburton (#15): card #1 at 0.78 availability; the Achilles return
  timeline is the single biggest lever on this build (Maxey swap +5.0 pts).
- Cameron Johnson, Braun, Eason: lines to re-derive (D56-1); re-check the
  Denver and Houston role reporting at the next pull.
- Kyrie (#39, 0.78): first season back from the ACL; the card's #3 with
  the 0.78 already priced.
- Survival chips: three of six rooms now beat the base rate; pooled margin
  0.009 — thin; re-fit if a seventh room misses.
- Yahoo market paste: seven days old; early-October paste before 10/14.

## Open-item receipts

| item | query run (2026-09-29) | dated finding |
|---|---|---|
| (this analysis) | machine replay only — no web research in this report | pull receipts for the window live in `after-report-2026-09-29.md` §8 (11 flagged names) |

## Bounds

- Random public room: the field's weakness is in every denominator; the
  championship rate is not a league forecast.
- Hindsight is single-swap on current lines: an upper bound on a pick's
  cost, not a strategy.
- The championship and ECW figures use the same projection lines the card
  ranks by; they cannot certify those lines. §7's external comparison is
  the only line-independent evidence in this report, and it is two dated
  snapshots (Yahoo 9/22, Hashtag and Statdunk 8/24).
- The Python replay port breaks exact blend ties by name while the deck
  breaks them by ΔECW: at #106 the port lists Eason first and the deck
  showed Turner 🎯 (the tool log carries no off-card note there); the
  table in §3 follows the deck.
- Addendum (2026-09-29, later the same day): the #130 leg of the follow-the-
  card arm (Poole for Sheppard, +3.7 points) and hindsight's "Poole +0.101"
  rest on the kit's Poole line (19.5 points as a starter), which RotoBaller
  (rank 230), Yahoo (211) and a projected top 150 (absent) all reject —
  `after-report-2026-09-29-market.md` §6–§7. Treat that leg as unproven
  until the line is re-derived (D-M4); the White and Pritchard legs stand
  on lines every source agrees with.
- Which of v31/v32 the owner had open is not recorded; both carry the same
  pool and engine, and the tool log replays identically on both (§4).

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D56-1 | Re-derive the Cameron Johnson, Braun and Eason projection lines from current role research (the 9/16 ritual), since Statdunk and Hashtag both rank them 25–90 places below the kit? | re-derive before the next pull; the card follows whatever the lines say |
| D56-2 | Poeltl: deck value #47 vs kit board #128 (standardization difference) — reconcile the two planes' methods, or accept the deck's read for the draft? | accept for now; measure the gap across the pool at the next tune-up |
| D56-3 | Survival chips missed a third room out of sample (0.232 vs 0.202); keep them on with the pooled +0.009 margin, or suspend until re-fit? | keep on; read BUY NOW as two-in-three |
| D56-4 | Haliburton at #15 at 0.78 availability was the card's #1 and hindsight's costliest turn; keep the risk tier or raise his multiplier until camp reporting settles? | keep; re-check at the first preseason report |

## Provenance

- Inputs: the owner's tool log and Yahoo recap (this session, 2026-09-29),
  transcribed verbatim into `arena/data/events/m56_tool_events.json` and the
  recap into the state by the deck's resolver.
- Every number is read from `arena/results/m56_*.json` and the debrief; the
  arms use 18,000 CRN seasons (seeds 11/23/47); the audit ran the deck's own
  engine under node against `docs/draft-deck.html` (main, v32 engine —
  identical to v31 for the card).
- Not verified: nothing here rests on web research.
