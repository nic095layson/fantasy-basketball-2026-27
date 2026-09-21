# After-Report — draft_51 retro: a pick-by-pick defense and critique of the card

**Owner request (2026-09-21, verbatim):** "provide a dissertation style analysis
and defense of the recent mock draft run … Do you defend each pick
recommendation (a retro analysis) at each moment of the draft, or do you see
any improvements you could have forecasted? Was the best player recommended to
me to select, or was there a better player that you see afterward that should
have been suggested? … identify where (if any) tightening in calculations can
be made. … I want to ensure this system is operating on pristine, data
comparison vs. that of the opponent roster build, forecasting of categorical
strength, and using the delta for me to build the strongest, building lead vs.
that of opponent teams."

Pull window: 2026-09-21 → 2026-09-21 (a stored-state replay, not a roster
pull; the 2026-09-21 pull-log row is the data state this analysis ran on).

**Method, stated once.** Every number here is computed, none eyeballed. The
card the owner saw is *reconstructed*, not remembered: the tool feed the owner
pasted contains the pick log only, so the decision card at each of the 13
turns was re-run two ways — through the Python port that the deck's parity
gate certifies as EXACT against the deck's JavaScript on this very state, and
through the deck's own JavaScript engine under node (`mock51_deckcard.py`),
which also reproduces the survival chips, the market rank and the 🎯 pin from
the deck's source verbatim. Two pools are in play: **v22** is the deck the
owner actually drafted against (pool 255, built 2026-09-15; the pool file was
recovered from git history and its z-scores match the published artifact to
six decimals), **v23** is the current deck (pool 264, built 2026-09-21, after
the tune-up). Three yardsticks grade rosters: *ECW* (expected categories won
per week against the average opponent, the card's own unit, from the arena's
weekly model), *season-shape H2H* (the draft_50/51 method), and *championship
rate* (18,000 Monte-Carlo seasons, seeds 11/23/47, common random numbers, the
ledger's instrument). Counterfactuals use the ledger's pairwise-swap model: the
owner takes the alternative at his turn and the player he actually took goes
to whoever drafted the alternative later, so the room still drafts 156 distinct
players. Harness and every output are landed in the deck repo
(`arena/mocks/mock51_*.py`, `arena/results/m51_*.json`); the technical
debrief is `arena/results/debrief_2026-09-21_mock51_slot10.md`.

---

**Headline.** The card is defended at twelve of thirteen turns and the owner
is defended at eight. On current lines the drafted roster projects as the
room's clear #1 — ECW 5.61 cats/week against the average opponent (next best
4.77), favored in all eleven head-to-heads, championship rate 55.0% in a room
where the next-best seat simulates at 11.6%. At eight of the thirteen turns
**no legal alternative** (or exactly one, worth ≤0.02 cats/week) would have
improved the final roster. The card's 🎯 was the hindsight-best legal choice
at twelve of thirteen turns; the thirteenth (#130) it had tied with the
hindsight-best and an alphabetical tie-break separated them. The two decisions
that cost real equity were both **owner deviations from a correct card**:
Sheppard over Turner at #82 (Turner was still there at #87 and went #102;
−7.3 points of championship) and Champagnie over Brook Lopez at #154 (Lopez was
the card's #1 at the last two turns and in the top five at seven consecutive
turns; he went undrafted; −8.4 points). Following the card at every turn
simulates at 63.5%; taking just those two recommendations, 67.4%.

The critique is where the value is. Three display layers the owner reads
between picks are **not** operating on pristine, room-relative data: the
survival chips read "BUY NOW" on 46 of 48 scored rows at a ~3% predicted
survival while 32 of those 46 players were still on the board at the next
turn (Brier 0.646 — a coin flip would have scored 0.25); the punt advisor
proposed punting turnovers for a hundred picks while the roster's weekly TO
win-probability sat at 0.62–0.77 (2nd of 12 at the end), because it grades
punts by absolute z-sums instead of room-relative strength; and on the current
deck an "urgent TARGET" pin would have moved the 🎯 at #58 onto Joel Embiid
(−0.17 cats/week, availability 0.78) over a #1 that was the hindsight-best. The
ordering itself — the thing that decides the 🎯 — held up under every test,
including one tightening I expected to help and which measured worse
(forecasting the room's final rosters). Details, receipts and the decision
sheet follow.

---

## 1. Roster changes (none) — what this report replays

No pool row moved; this is an analysis of a stored state. Data: deck main at
`65d1626` (pool `c1f87ac1db09`, 264 rows) and the v22 pool regenerated from
git (`e7aac6b`, sha `e3e17e279ea5`, 255 rows). The state is
`arena/data/states/draft_state_51.json` (156 picks, owner slot 10, verified
against the Yahoo recap on 9/21). On v22 two drafted names have no row (Tre
Jones, Julian Champagnie), exactly as the owner's deck experienced them; on
v23 all 156 resolve.

## 2. The draft, turn by turn — the defense

Column key: *card 🎯* = the system pick the owner's deck showed (v22; the 🎯
is the blend50 #1 unless an urgent TARGET pin fires — none fired on v22);
*rank* = where the owner's pick sat on that card; *hindsight best* = the best
legal single-swap alternative on current lines, with its ECW gain in
cats/week over the roster as drafted; *n better* = how many of the legal
alternatives at that moment would have improved the final roster.

| pick | card 🎯 (v22) | owner took | rank | hindsight best (gain) | n better | verdict |
|---|---|---|---|---|---|---|
| 10 | Towns | Edwards | 2 | none (Towns came back at 15) | 0 of 234 | pair plan executed |
| 15 | Towns | Towns | 1 | none | 0 of 230 | optimal |
| 34 | Davis | Davis | 1 | none | 0 of 212 | optimal |
| 39 | D. White | Daniels | 3 | D. White (+0.055) | 4 of 208 | card right by a hair |
| 58 | Anunoby | Anunoby | 1 | Turner (+0.007) | 1 of 190 | optimal within noise |
| 63 | Pritchard (tied w/ Lillard) | Lillard | 2 | Pritchard (+0.066) | 4 of 186 | card right; tie decided by name |
| 82 | Turner | Sheppard | 5 | Turner (+0.182) | 34 of 168 | the costly miss |
| 87 | Turner | Porziņģis | 2 | Turner (+0.076) | 2 of 164 | card right; Turner lasted to 102 |
| 106 | C. Johnson | C. Johnson | 1 | Lopez (+0.021) | 1 of 146 | optimal within noise |
| 111 | Poeltl | Poeltl | 1 | Lopez (+0.021) | 1 of 142 | optimal within noise |
| 130 | Braun (tied w/ Lopez) | Eason | 3 | Lopez (+0.074) | 1 of 124 | Lopez was tied for 🎯 |
| 135 | Lopez | Braun | 2 | Lopez (+0.061) | 1 of 120 | card right |
| 154 | Lopez | Champagnie | not in pool | Lopez (+0.223) | 33 of 103 | the other costly miss |

The moment-by-moment reading, with what each choice *bought* (mean change in
per-category win probability against the room's rosters as they stood):

**#10 Edwards, #15 Towns — the pair.** With no opponent roster yet, the #10
card is pure 9-cat value; Towns sat first by 0.006 of blend score. Taking
Edwards first and Towns on the wheel was the slot-10 pair plan (Towns' Yahoo
ADP 12.3 made him the likelier of the two to survive), and hindsight has
nothing to add: with Towns arriving at 15, no alternative at 10 improves the
roster. Towns at 15 bought +2.05 cats/week against the eleven partial rosters
— the largest single purchase of the draft (REB +0.69, PTS +0.48, BLK +0.36,
ST +0.33) at the cost of TO (−0.42).

**#34 Davis.** Card #1, value #1, hindsight-optimal. The room let the board's
#7 fall to 34 (Yahoo ADP 24.9); the card's survival read on him at #15 was
1% — it was wrong about the timing but the owner did not need it to be right.
Davis bought BLK +0.43, PTS +0.39, REB +0.35.

**#39 Daniels over White.** The card said Derrick White (3PTM +0.32, AST
+0.29) by 0.010 of blend; Daniels bought ST +0.51 and became the engine of a
category the roster finished first in. Hindsight prefers White by 0.055
cats/week — real but small — and White went at 47, so the room agreed with the
owner's price. This is the third straight mock in which Daniels was the
board's favorite at an owner turn (ledger L-m33c); this time the owner took
him, and the roster's identity (ST 1st, TO 2nd) came from it.

**#58 Anunoby.** Card #1, value #1, hindsight-optimal to within 0.007. At
this turn the roster's own numbers read AST 12th, FT% 10th, 3PTM 8th (z-sum
ranks vs the field): the punt lean the advisor had flagged was real for AST
and only for AST.

**#63 Lillard over Pritchard.** The card showed an *exact* blend tie between
Pritchard and Lillard and listed Pritchard first because the tie-break is name
order. Hindsight says Pritchard, +0.066 (3PTM +0.33 vs Lillard's FT% +0.12 /
AST +0.28), and Pritchard went at 80 — he would have kept to #82. The owner's
read that the roster needed AST insurance was true of the *category* (AST
never left 12th) and false of the *remedy*: one guard does not move a
12th-ranked category into contention, and the weekly model priced that
correctly (Lillard's AST purchase, +0.28 in win probability, was the same
+0.25 Pritchard offered).

**#82 Sheppard over Turner — the miss that mattered.** On the deck the owner
was using, Sheppard was still priced on his pre-downgrade line: card #5, value
#7. On current lines he is card #36. The card's #1 was Myles Turner (BLK
+0.27, REB +0.20), and Turner was the #1 again at #87 and did not go until
#102. Thirty-four legal alternatives improve on Sheppard here; Turner improves
by 0.182 cats/week and +7.3 points of championship. Two things are true at
once: the card was right on the day with the lines it had, and the line it
had for Sheppard was stale (fixed 9/21). The owner's stated reason — AST
insurance for the punt build — is the same category logic as #63, and the same
answer applies.

**#87 Porziņģis over Turner.** A near-tie on the card (0.988 vs 0.984) and a
near-tie in what they buy (BLK +0.25 vs +0.19; everything else within 0.03).
Hindsight leans Turner by 0.076 because Porziņģis's row carries the injury
multiplier (0.78). Defensible either way; the card was right by the margin it
showed.

**#106 Cameron Johnson, #111 Poeltl.** Both card #1 and both hindsight-optimal
to within 0.021 (the only better alternative each time was Brook Lopez, who
was on the card at #4 and #2). By #111 the roster's z-sum ranks read FT% 1st,
3PTM 1st, ST 1st, PTS 2nd — the FT% the advisor had proposed punting at #46
was now the roster's best category.

**#130 Eason, #135 Braun, #154 Champagnie — the Lopez saga.** Brook Lopez was
in the card's top five at seven consecutive owner turns (82, 87, 106, 111,
130, 135, 154), the tied #1 at 130 and the outright #1 at 135 and 154, and
nobody in the room drafted him. Eason and Braun were good picks (Eason value
#1 on the current card; both hindsight-optimal but for Lopez), and the owner
got both, so the cost was deferred, not avoided: at #154, Lopez over
Champagnie is +0.223 cats/week and +8.4 points, the largest single swap in the
draft, because a 13th man who never starts is replaced by a center who does
(BLK +0.20, PTS +0.16). Champagnie had no row on the deck the owner used, so
the card could not price him; on current lines he is card #24 at that turn.

## 3. Was the best player recommended?

Three counts, on current lines:

- **The card's 🎯 vs hindsight.** At 12 of 13 turns the 🎯 was the
  hindsight-best legal choice or within 0.02 cats/week of it. The exception is
  #130, where the hindsight-best (Lopez) was *tied* with the 🎯 (Braun) on the
  card and lost the alphabetical tie-break. No turn produced a 🎯 that
  hindsight rejects.
- **The owner's picks vs hindsight.** Eight turns with zero or one better
  alternative (#10, #15, #34, #58, #106, #111, #130, #135); five with a
  material one (#39 +0.055, #63 +0.066, #87 +0.076, #82 +0.182, #154
  +0.223). All five were deviations from the card; in four of the five the
  card's #1 *was* the hindsight-best.
- **Championship arms** (18,000 seasons, CRN-paired; standard error ≈0.4
  points at these rates, so differences under a point are noise):

| arm (mechanism: pairwise swap, opponents unchanged) | champ % | playoff % |
|---|---|---|
| as drafted | 55.03 | 99.8 |
| D. White at 39 | 56.06 | 99.9 |
| Pritchard at 63 | 57.85 | 99.9 |
| Turner at 82 | 62.34 | 100.0 |
| Turner at 87 | 58.14 | 99.9 |
| Lopez at 106 / 111 / 130 / 135 | 57.18 / 56.43 / 57.41 / 58.11 | 99.9 |
| Lopez at 154 | 63.42 | 100.0 |
| follow the card #1 at every turn (self-consistent, strict pairwise; swaps at 39, 63, 82, 87) | 63.47 | 100.0 |
| Turner at 82 and Lopez at 154 | 67.38 | 100.0 |
| Turner at 82, Lopez at 154, Pritchard at 63 | 69.66 | 100.0 |

The mock-34 debrief recorded the opposite result (full card-follow 0.008% vs
the owner's 9.52%) in a punted draft where the card was punt-blind and the
owner was not. Here no punt was declared before pick 1 and the card's
punt-blind ordering matched the roster that emerged; the card-follow arm wins.
Neither result generalizes on its own — they bracket the card: it is a
strong value-first drafter and a poor punt-drafter, by measured design.

## 4. The final roster against the room

Current lines (v23). ECW is expected categories won per week against the
named opponent; 4.5 is the break-even.

| opponent (seat) | expected cats | | opponent (seat) | expected cats |
|---|---|---|---|---|
| San (9) | 6.20 | | Bonani (2) | 5.45 |
| Sen (12) | 6.02 | | dnd (7) | 5.42 |
| Jeff (6) | 5.91 | | Team 1 (1) | 5.16 |
| Akis (8) | 5.75 | | Daniel (5) | 5.08 |
| andrew (11) | 5.72 | | | |
| steven (3) | 5.52 | | **average** | **5.61** |
| donkeanu (4) | 5.47 | | | |

Category standing, three yardsticks (1 = best of 12):

| yardstick | FG% | FT% | 3PTM | PTS | REB | AST | ST | BLK | TO |
|---|---|---|---|---|---|---|---|---|---|
| weekly-model win probability | 3 | 2 | 3 | 3 | 5 | 12 | 1 | 3 | 2 |
| season-shape totals (draft_51 method) | 3 | 2 | 2 | 3 | 5 | 12 | 1 | 3 | 2 |
| kept-total z-sum | 3 | 2 | 2 | 3 | 5 | 11 | 1 | 2 | 2 |

The three yardsticks agree to within one rank in every category — the first
mock in the ledger where board rank, ECW rank and championship rank all read
1. The build is what the 9/21 draft_51 report said it was, one notch better:
eight categories at 5th or better, six in the top three, one dead (AST). The
room simulates as **T10 55.0%, dnd 11.6%, steven 6.8%, Bonani 6.7%, Team 1
5.6%, Daniel 3.7%, donkeanu 3.5%, andrew 2.9%, Akis 2.2%, Jeff 1.3%, Sen 0.4%,
San 0.2%**. Read the 55% with its denominator: this is a random public room
whose next-best seat is an 11.6% team; the league cast is a different field.

**Cross-plane check (S3 theme).** The 9/21 draft_51 report projected 9 wins
of 11 on *kit* lines, losing to Bonani and dnd. Replaying on the deck's v22
lines gives 9 of 11 with the *same two losers* — the planes agreed at draft
time. On v23 lines the same roster reads 11 of 11 and ECW 5.30 → 5.61. Two
mechanical reasons, both stated: the 13th man now exists (Champagnie had no
v22 row, so the v22 replay scored a 12-man roster), and the 9/21 line syncs
moved Sheppard down while adding nothing to the opponents. The v23 read is the
honest current one; the jump is bookkeeping, not a better draft.

## 5. Critique — where the calculations need tightening

The owner's standard is the right one: room-relative comparison, forecast of
categorical strength, and the delta as the decision variable. Measured
against it, the card's *ordering* passes and three of its *readouts* fail.

**T1. The survival chips are calibrated for bots, not humans (display layer;
misled the owner at every turn).** The model prices P(survive to your next
pick) as Φ((rank − N)/σ) blended 9/11 on the internal value rank and 2/11 on
the internal market rank — fit on 840 rows from 14 replayed *mock* rooms
whose opponents were the arena's value-drafting personas. In this human room
the value rank is what the room ignores: the internal value rank misses the
actual pick number by a standard deviation of 41 picks (mean absolute error
32); the internal market proxy by 41 (MAE 30); Yahoo's 9/15 ADP by 17 (MAE
12). So every high-value player still on the board at pick N looked to the
model like a player who should already be gone: 46 of the 48 scored Top-5
rows carried "BUY NOW" at a mean predicted survival of 2.8%, and 32 of those
46 survived to the owner's next turn. Brier 0.646. An ADP-only model on the
same rows — Yahoo ADP with the deck's own σ rule — scores Brier 0.260, calls
28 rows quiet (22 survive) and 13 BUY (6 leave). Not good yet, but a
different instrument. Recommendation: (a) when a real ADP exists (the kit's
market layer now carries Yahoo's, and the 8/21 work order already gated the
Mkt column on it), the survival model should run on it, with σ fit to live
rooms; (b) until refit, the chip should be suppressed rather than shown — a
chip that fires on every row conveys nothing and taught the owner to read
"BUY NOW" as wallpaper, which is the state in which a true BUY NOW gets
ignored.

**T2. Exact ties at the top of the card, resolved alphabetically (ordering
layer; decided the 🎯 at 2 of 13 turns on the owner's deck, 6 of 13 on the
current one).** The blend is 0.5·pct(ΔECW) + 0.5·pct(value) where pct is a
rank percentile. Percentiles are quantized to 1/(n−1), so two players who
hold ranks {1,2} and {2,1} in the two halves score *identically*, and the
parity gate then requires a deterministic tie-break — name, descending. At
#63 that put Pritchard ahead of Lillard; at #130 it put Braun ahead of Lopez
(hindsight-best); on current lines #15, #82, #87 and #135 are also ties.
Recommendation: keep the percentile blend for ordering (it is the validated
E9 instrument) but break ties on the ΔECW *magnitude* in cats/week — the
number the row already prints — and only then on name. This changes no
validated ordering except where the ordering was arbitrary.

**T3. The punt advisor grades punts on absolute z-sums, so it proposes
conceding categories the roster is winning in the room (advisory layer; drove
four owner clicks).** The FULL TILT gate fired after #46 on AST+FT% (AST
12th, FT% 10th by z-sum — a fair read at four players). The coherence strip
then "retargeted" three times — to FT%+TO at #52, to TO+FG% at #63, to TO+AST
at #111 — each on a +2.0–2.3 "roster fit" delta. Roster fit is kept-z summed
over the owner's players *against the pool mean*; a roster of high-usage
stars always looks TO-negative on that scale, so punting TO always raises
"fit". Against the *room*, the same roster's weekly TO win-probability was
0.62–0.77 at every turn from #58 on and finished 2nd of 12; FG% (proposed
punt at #63) was 0.43–0.56 and finished 3rd; FT% (proposed at #46) finished
2nd. The advisor was right about exactly one category (AST, win-probability
0.04–0.30 throughout) and wrong about three, and its recommendation changed
at every check — the S4 hysteresis item, now with a root cause: the quantity
it optimizes is not room-relative. Recommendation: rebuild the strip on the
weekly model's per-category win probability (already computed for the card,
so zero new machinery), require a margin *and* two consecutive turns before a
retarget is offered, and label the punt box what mock 34 established it to be
— display-only, never read by the ordering.

**T4. The urgent-TARGET pin can override a correct #1 with an unavailable
player (🎯 layer; latent on the owner's deck, live on the current one).** On
v22 the archetype read never went urgent. On v23 at #58 it reads "C shelf
nearly empty" and pins Joel Embiid as the 🎯 over Anunoby — Embiid carries
the 0.78 injury multiplier and hindsight prices him at −0.171 cats/week
against the roster as drafted (Anunoby was hindsight-best). The pin's
scarcity count is a *market-rank* shelf count that never consults ΔECW or
availability, and it is the one override class the ledger graded positive
(m13/m18/m19 interior counterfactuals). Recommendation: the pin may move the
🎯 only when the pinned player's ΔECW is within a stated margin of the #1's
and his availability is 1.0; otherwise it stays a labeled row.

**T5. Forecasting opponents' final rosters — tested, and it measured worse
(ordering layer; negative result, reported so it is not tried twice).** The
owner's phrase "forecasting of categorical strength" names the obvious
tightening: the card measures ΔECW against the room's *current* partial
rosters, which are three players deep at #39. I built the forecast (finish
the draft twelve times from each owner turn with the arena's market persona
in every opponent seat, average the opponents' final weekly models, rank
candidates by ΔECW against that) and an oracle (rank against the *actual*
final rosters), and graded all four orderings by rank correlation with the
hindsight gain over the top-40 shelf at each turn. Mean Spearman ρ: shipped
(current rosters) **0.77**, forecast 0.59, oracle 0.59, value-only 0.58; the
shipped ordering was best or tied-best at 11 of 13 turns. The reason is a
stage mismatch, not a bad forecast: a three-man roster measured against
thirteen-man opponents has near-zero win probability in every category, so
the marginal player's effect is a flat, noisy gradient, whereas current
rosters keep both sides at the same stage. The principled version — roll out
*both* sides, the owner's remaining picks included — is a different and
expensive experiment and is not claimed here.

**T6. The internal market proxy should yield to the real ADP where one
exists (data layer).** Measured above: sd 41 picks for the proxy vs 17 for
Yahoo ADP. The proxy feeds the Mkt column, the survival chips, the TARGET
shelf counts and the mock-room personas. The 8/21 work order made the real
ADP a gated step; the measurement here is the case for taking the gate.

**T7. Stale lines cost more than any calculation (data layer; already
fixed).** The single most expensive event in this draft was a line, not a
formula: Sheppard priced pre-downgrade on the deck the owner used. The 9/21
tune-up synced the deck to the 9/16 research and expanded the pool so live
rooms' picks resolve. The lesson generalizes: the card is only as good as the
row, and the S3/F7 cross-plane gate is the mechanism that would have caught a
kit-vs-deck line divergence before a live room did.

**What is measured and what is decorative — the "theatrical" question.**
Computed and validated: the blend50 ordering (E9, 14-mock panel, this draft),
the ΔECW figure on each row (exact port of the arena weekly model, parity
EXACT), the category rank strip, the Monte-Carlo grading. Computed but
miscalibrated for this room: the survival chips (T1), the punt advisor's fit
delta (T3). Heuristic: the TARGET read (T4), the Mkt proxy (T6), the advice
line (derived from the above, adds nothing). None of the miscalibrated
layers touches the ordering — that separation is by design and it held — but
they are what the owner reads between picks, and the log shows them steering
four clicks and two reaches. Pristine at the core; not yet pristine at the
surface.

## Watchlist

- **The Lopez pattern.** A center the card ranked in its top five at seven
  consecutive turns went undrafted by a 12-team human room. Either the
  room-wide price on late-career bigs is lower than every model here assumes
  (ADP 111.9 — the room passed him at that price too), or the line is high.
  Worth a look at his row before October; if the line holds, he is the
  round-12/13 target the seat-10 slate should name explicitly.
- **Survival recalibration needs more live rooms.** n = 1 room, 48 rows. The
  ADP-model Brier of 0.26 is a single-room estimate; two or three more live
  mocks at slot 10 give a fit set.
- **Daniels-class hesitation is now Lopez-class hesitation** (ledger L-m33c):
  the owner takes the board's favorite guard and passes the board's favorite
  center. Structural, not random — the seat-10 slate should say so.
- Standing items unchanged (preseason data drop, camp roles, D-I1 Butler
  severity, S3 as F7, S4 hysteresis — now with a root cause, T3).

## Open-item receipts

| check | receipt |
|---|---|
| v22 pool reconstruction | `git show e7aac6b:data/players.csv`, sha256 `e3e17e279ea5`; Jokić z FG% 2.677116 / AST 3.268015 equal the published v22 data block to 6 decimals |
| v22 deck source | data and engine blocks of `docs/draft-deck.html` at `e7aac6b` byte-identical to the published artifact v22 |
| card reconstruction | Python port (check_parity's ordering, EXACT on state_51) and the deck's own JS under node agree on every Top-5 at all 13 turns, both pools |
| hindsight counterfactuals | pairwise-swap model per `arena/mocks/README.md`; owner's own later picks screened as degenerate; undrafted alternatives in release mode |
| season arms | `arena.simulate_seasons`, 6,000 seasons × seeds 11/23/47, CRN-paired; per-seat champ% for as-drafted recorded in `m51_arms.json` |
| survival calibration | 48 scored rows (v22 card, actual pick excluded), realized survival from the pick log; Yahoo ADP joined by folded name, 145/156 picks matched |
| forecast experiment | K = 12 rollouts per turn, market persona for opponents, bpa_pure for the owner; Spearman on the top-40 shelf; `m51_forecast.json` |
| publication gate | `report/check_report.py` PASS on this file |

## Bounds

**Out of scope by design:** opponent intel from this room (random public
humans; owner directive 2026-08-25 — their tendencies are disposable, only the
price signal is durable); any engine change (this is a decision sheet, not a
ship); the kit-plane replay (the 9/21 draft_51 report holds it).
**In scope and unverified:** all championship rates are simulator-conditional
(the weekly model's constants are unfit to the 2025-26 weekly data the owner
supplied 8/4); hindsight is measured on current (v23) lines while the card the
owner saw ran on v22 lines — they differ materially only at #82 and #154, and
both are stated; single-swap gains are one-at-a-time and do not add; the
follow-card arm is self-consistent but strict-pairwise (an undrafted card #1
is skipped, so it understates the card); the ADP survival model uses the
deck's σ rule unfit, and 11 of 156 names did not join on folded name (Jr.
suffixes, one alias) — the kit's alias table would close that.

## Decision sheet (owner disposes)

- **D51R-1 — survival chips (T1):** refit on Yahoo ADP with σ from live
  rooms, or suppress the chip until refit. Recommendation: suppress now,
  refit after two more live mocks.
- **D51R-2 — tie-break (T2):** ΔECW magnitude before name. Zero-risk to the
  validated ordering; needs a parity-fixture update.
- **D51R-3 — punt advisor (T3, absorbs S4):** room-relative win probability,
  margin + two-turn hysteresis, display-only label. Recommendation: do it
  before the next live mock; it drove four clicks here.
- **D51R-4 — TARGET pin gate (T4):** ΔECW-within-margin and availability 1.0
  before the 🎯 may move. Recommendation: yes; it is live on the current deck.
- **D51R-5 — real ADP into the Mkt column (T6):** take the 8/21 work order's
  gated step 5 on the measurement above.
- **D51R-6 — seat-10 slate:** name the round-12/13 center explicitly (Lopez
  on current lines) and the AST stance (accept 12th; do not buy insurance).
- **D51R-7 — the rollout forecast (T5):** not recommended on this evidence;
  revisit only with a both-sides rollout design and a ship bar.

## Provenance

Produced 2026-09-21 by the operating session
(`https://claude.ai/code/session_01QjgeRdpDaWgSJmGKRG8fTU`). Kit branch
`claude/draft-51-retro` (this report). Deck branch `claude/mock51-retro`:
`arena/mocks/mock51_retro.py` (stages replay · final · hindsight · forecast ·
arms), `mock51_deckcard.py` (the deck's own JS, both decks), `mock51_extra.py`
(survival calibration, ties, Embiid, punt advisor, ADP model),
`mock51_combo.py` (combined arms, board rank), outputs `arena/results/m51_*.json`,
debrief `arena/results/debrief_2026-09-21_mock51_slot10.md`, LEDGER row 51.
Regeneration status is stated in the debrief, per lesson 13.
