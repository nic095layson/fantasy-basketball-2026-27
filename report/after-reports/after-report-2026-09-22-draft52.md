# After-Report — draft_52: second live-human mock from the REAL slot 10

**Owner request (2026-09-22, verbatim):** "I just completed another live mock
draft with live humans. Please see copied draft recap from TOOL; Message
following this will provide draft recap from yahoo." Two inputs again: the
deck tool's pick-by-pick feed, then Yahoo's recap — the authoritative record.

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (the real league slot;
opponents are random humans, not the league cast — a practice rep, not
opponent intel). Two "David"s in the room: seat 8 is the other one.
**Deck used:** the published v23 artifact (pool 264), proven by the feed's
FULL TILT / Retarget lines — only the pre-2026-09-21 advisor renders them —
and by two live-drafted names the pool lacks. **Method:** the recap was
reconciled against the feed pick-by-pick; the grade is the deck plane's
machine-derived retro (`yahoo-fantasy-basketball` PR #38: `live_retro.py`,
`live_deckcard.py`, `live_advisor.py`, `live_survival.py`, `live_debrief.py`,
outputs `arena/results/m52_*.json`), whose harness first regenerated mock 51's
landed outputs byte-for-byte. Every figure below is read from those files;
none is eyeballed. Verification: this file passes `report/check_report.py`;
receipts in §8.

Pull window: 2026-09-21 → 2026-09-21 (analysis run 2026-09-22 against the
9/21 pool and the 9/22 Yahoo market files; not a roster pull — the 9/21
pull-log row covers the window).

**Headline.** ECW **5.634** cats/week, rank **1 of 12**, favored in **11 of
11** head-to-heads, championship rate **47.94%** over 18,000 simulated seasons
(next seat: the other David, 5.195 / 11.6%) [EVIDENCE: `m52_final.json`,
`m52_arms.json`]. Mock 51 from the same seat read 5.610 / 11 of 11 / 55.03%.
The card's #1 was hindsight-best or within 0.013 of it wherever the owner took
it; the two departures that cost the most were the two injury-tagged picks
the owner made against the card, Tatum at #10 and Kyrie at #39. Two of the
9/21 tune-ups were tested live in this room and both held.

---

## 1. Validation vs the Yahoo recap

| check | result |
|---|---|
| picks mapped | 156 of 156; every seat, every round |
| tool corrections reconciled | the #27 Harden insert (#27–#29 shifted), unknown-name fixes at #62 (Edey), #65 (Keyonte George), #141 (Daniss Jenkins), #155 (Gui Santos), the #125/#126 Jaquez / Davion Mitchell order, two halted "Mitchell" re-sends — all match the recap |
| names outside the deck pool | 2, both opponents: Daniss Jenkins (#141, seat 4), Gui Santos (#155, seat 11). Those seats simulate with 12 men; both were already the room's weakest by ECW |
| state landed | `arena/data/states/draft_state_52.json`, md5 `ba6c2a94fa41b02d7871fb42d13cc923`, cast recorded |

No roster row changed anywhere in this analysis (not a pull). The two
poolless names are now priced by Yahoo (XRank 154 and 250 on the 9/22
draft-analysis page) and sit in the market coverage gaps for the owner's
disposition (§7).

## 2. The team, replayed

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **47.94%** (rank 1 of 12) |
| Playoff rate | 99.81% |
| ECW | **5.634** cats/week (rank 1; next 5.195, David (seat 8)) — favored in 11/11 head-to-heads |
| Season-shape H2H | wins 11/11 |
| Board rank (kept-total z-sum) | **1** (+20.84; next +3.78) |
| Category rank, weekly model | FG% **9** · FT% 4 · 3PTM 3 · PTS **1** · REB 5 · AST **10** · ST **1** · BLK 4 · TO 6 |

[EVIDENCE: `debrief_2026-09-22_mock52_slot10.md` headline, generated from the
JSON]. The shape is the slot-10 pair plan again: PTS and ST first, 3PM third,
FG% and AST conceded. TO finished sixth by the weekly model after the late
picks stopped protecting it — see §4.

## 3. Pick by pick — card vs owner vs hindsight

Card 🎯 = what the v23 deck showed (blend50 #1, or the urgent TARGET pin when
it took the 🎯). Tuned 🎯 = the same turn on the tuned deck (PRs #34 + #37).
Hindsight = the best legal single-swap alternative, ECW gain in cats/week
(pairwise-swap model; the owner's own later picks screened). [EVIDENCE:
`m52_deckcard_v23.json`, `m52_deckcard_tuned.json`, `m52_hindsight.json`]

| pick | card 🎯 | tuned 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | = | Jayson Tatum | 15 | Jalen Johnson (+0.154) | 18/234 | +0.105 |
| 15 | Karl-Anthony Towns | Evan Mobley | Donovan Mitchell | 8 | Derrick White (+0.029) | 3/230 | -0.010 |
| 34 | Anthony Davis | = | Anthony Davis | 1 | Derrick White (+0.013) | 1/212 | owner's own later pick |
| 39 | Jalen Williams | = | Kyrie Irving | 5 | Derrick White (+0.139) | 8/208 | +0.049 |
| 58 | Kristaps Porzingis | Franz Wagner | Franz Wagner | 1 | Tyler Herro (+0.001) | 1/190 | owner's own later pick |
| 63 | OG Anunoby | = | Dyson Daniels | 2 | none | 0/186 | -0.041 |
| 82 | Jakob Poeltl | = | Jakob Poeltl | 1 | Isaiah Hartenstein (+0.010) | 1/168 | owner's own later pick |
| 87 | Cameron Johnson | = | Myles Turner | 2 | none | 0/164 | owner's own later pick |
| 106 | Cameron Johnson | = | Miles Bridges | 4 | Brook Lopez (+0.002) | 1/146 | owner's own later pick |
| 111 | Cameron Johnson | = | Cameron Johnson | 1 | none | 0/142 | owner's own later pick |
| 130 | Christian Braun | = | Jordan Poole | 3 | Christian Braun (+0.053) | 4/125 | +0.053 |
| 135 | Christian Braun | = | Tari Eason | 3 | Christian Braun (+0.053) | 4/121 | +0.053 |
| 154 | Christian Braun | = | PJ Washington | 2 | Christian Braun (+0.033) | 1/104 | +0.033 |

**Where it was won.** No better legal pick existed at #63 (Daniels), #87
(Turner) and #111 (Cam Johnson); exactly one at #34, #58, #82, #106 and #154.
The owner took the card's #1 at four turns and a Top-5 row at 11 of 13.

**Where it cost something** [EVIDENCE: hindsight and arms JSON]:

- **#10 Jayson Tatum** (card #15; pool availability 0.78, `inj-achilles-risk`):
  18 of 234 alternatives grade higher — Jalen Johnson +0.154 (went #11), Tyrese
  Haliburton +0.144 (#14), Towns +0.105 (#17). Swapping in Johnson alone lifts
  the championship rate from 47.94% to 52.82%.
- **#39 Kyrie Irving** (card #5; availability 0.78, `inj-acl-risk`): 8 of 208
  grade higher — Derrick White +0.139 (went #43), Pritchard +0.065, Bane +0.060.
  White alone: 52.44%.
- **Christian Braun, passed three times** (#130, #135, #154; the card's 🎯 each
  time, +0.053 / +0.053 / +0.033): he went #156, the last pick of the draft.
- Following the card's #1 at every turn, pairwise-legal, simulates at 56.92%.

The verdict on the two injury picks is the same as the retro's Butler
verdict: the card was not wrong to rank them lower, and the owner's judgment
on Tatum's Achilles and Kyrie's ACL year is the owner's to keep or revise
(§Decision sheet). [INFERENCE: the ECW gap is entirely the 0.78 multiplier;
at availability 1.0 both picks grade inside the card's top three.]

## 4. The 9/21 tune-ups, tested live

**D51R-4 (urgent pin gate) held.** At #58 the v23 deck moved the 🎯 off Franz
Wagner onto an urgent "Shot-block C" pin, Kristaps Porziņģis (availability
0.78) — LAST CALL. The owner ignored it and took Franz: card #1, and
hindsight-best within 0.001 cats/week. The tuned deck withholds that pin
(`availability 0.78`) and keeps the 🎯 on Franz. [EVIDENCE: `m52_deckcard_*.json`]

**D51R-3 (punt advisor advice-only, room-relative) held — and the box this
time was the old advisor's own product.** `live_advisor.py` reproduces both
feed lines from the engine: right after #39 the old advisor showed FULL TILT
FG%+AST "clear path 6/7"; on that box the old coherence strip offered
Retarget to FG%+TO "+2.9 fit". The owner clicked both. What the two strips
then said at every owner turn the FG%+TO box stood:

| owner turn | box | TO beats | old strip | new strip |
|---|---|---|---|---|
| #58 | FG%+TO | 90% | aligned | inverted: punt AST for TO (+0.80 cats/wk) |
| #63 | FG%+TO | 66% | aligned | inverted: punt REB for TO (+0.34 cats/wk) |
| #82 | FG%+TO | 80% | aligned | inverted: punt REB for TO (+0.58 cats/wk) |
| #87 | FG%+TO | 68% | aligned | inverted: drop TO (+0.68 cats/wk) |
| #106 | FG%+TO | 81% | aligned | inverted: punt AST for TO (+0.65 cats/wk) |
| #111 | FG%+TO | 67% | aligned | inverted: punt AST for TO (+0.38 cats/wk) |
| #130 | FG%+TO | 74% | aligned | inverted: punt AST for TO (+0.53 cats/wk) |
| #135 | FG%+TO | 52% | aligned | inverted: drop TO (+0.52 cats/wk) |
| #154 | FG%+TO | 62% | aligned | inverted: punt AST for TO (+0.37 cats/wk) |

"TO beats" = the share of the room this roster beats in turnovers in a
typical week, from the same weekly model the card scores with. The old strip
read *aligned* at all nine turns while the roster was punting its second-best
category; the room-relative read calls it *inverted* at all nine. At the
moment of the FULL TILT click (roster 4, box empty) the new advisor would
have shown nothing — AST beat 46% of the room with Kyrie aboard — and on the
FG%+AST box it would have read "drifting: punting AST though this roster beats
46% of the room in it; smaller box". [EVIDENCE: `m52_advisor.json`]

**D51R-2 (ΔECW tie-break):** the #15 🎯 flips from Towns to Mobley on the tuned
deck (ΔECW 2.236 vs 2.179); the owner took Mitchell, within 0.03 of the best
alternative either way.

**D51R-1 (survival chips, suspended on the tuned deck, still live on v23):**

| room | rows | mean predicted survival | realized | Brier |
|---|---|---|---|---|
| mock 52 (v23 deck, chips still live) | 50 | 0.043 | 0.700 | 0.655 |
| pooled with mock 51 | 98 | 0.044 | 0.694 | 0.651 |

BUY NOW on 47 of 50 scored rows at a mean 0.028 predicted survival; 33 of
those players were still there at the owner's next turn. This is the second
live room of the two the owner set as the refit threshold. [EVIDENCE:
`m52_survival.json`]

## 5. Market context — the 9/22 Yahoo draft-analysis page

Prices from `report/market/yahoo-2026-09-22.csv` (ADP where Yahoo lists one).
Reach = pick number minus ADP (positive = taken earlier than the room takes
him). [EVIDENCE: the CSV; INFERENCE on what the reach cost, since our model
grades by ECW, not by price]

| pick | player | ADP | XRank | reach | our read |
|---|---|---|---|---|---|
| 10 | Jayson Tatum | 10.4 | 8 | 0 | at price; the cost was the multiplier, not the pick number |
| 15 | Donovan Mitchell | 14.8 | 11 | 0 | at price |
| 34 | Anthony Davis | 37.2 | 44 | −3 | at price; card #1 |
| 39 | Kyrie Irving | 52.1 | 48 | −13 | 13 picks early by the room; White (ADP 46.8) went #43 |
| 58 | Franz Wagner | 53.5 | 49 | +4 | value; card #1 |
| 63 | Dyson Daniels | 61.6 | 60 | +1 | at price; hindsight-best |
| 82 | Jakob Poeltl | 121.6 | 114 | −40 | 40 early by the room; by ECW still the best legal pick (one alternative +0.010) |
| 87 | Myles Turner | 99.0 | 99 | −12 | 12 early; hindsight-best |
| 106 | Miles Bridges | 97.9 | 98 | +8 | value |
| 111 | Cameron Johnson | 113.2 | 172 | −2 | at price; card #1 |
| 130 | Jordan Poole | — | 174 | — | no ADP; card #3 |
| 135 | Tari Eason | 120.8 | 139 | +14 | value |
| 154 | PJ Washington | 117.8 | 151 | +36 | value |

The Poeltl and Turner reaches are the pair plan's price of insisting on
centers before the room does; the model says both were the right players,
and the 9/22 ADP says the room would probably have let Poeltl reach #87
(ADP 121.6). That is a sequencing question for the next live room, not a
correction. [INFERENCE]

## 6. What this run answers and asks

- **Answered:** the seat-10 build repeats under a second random room (ECW
  rank 1 twice, 11 of 11 twice); the card's #1 was hindsight-best or within
  0.013 at every turn the owner took it; both retro tune-ups behaved as
  designed on live data; the survival model failed the same way twice.
- **Asks:** the owner's judgment on the two injury multipliers (Tatum, Kyrie);
  whether to refit the survival model now that two rooms are in hand; and the
  merge-and-publish order below, so the next live room runs on the tuned deck
  and on Yahoo's price.

## Watchlist

Flags from the 9/22 market files, for the next pull's process (Yahoo is one
outlet; no row changes flow from it):

| item | detail |
|---|---|
| Cam Whitmore team | our pool says CLE; Yahoo's 9/22 page says DEN [SINGLE-SOURCE] — verify at the next pull |
| Yahoo's own team data moved since 9/15 | Bruce Brown DEN to NYK and John Konchar MIN to NYK on Yahoo's page [SINGLE-SOURCE]; neither is in our pool |
| coverage gaps the room drafts (ADP inside 140, no pool row) | Bronny James 100.3, Al Horford 101.2, Aday Mara 101.8, Luke Kennard 102.7, Johni Broome 104.2, Aaron Wiggins 106.8, Brayden Burries 116.2 |
| poolless live picks | Daniss Jenkins (XRank 154), Gui Santos (XRank 250) — a projection row each if the owner wants them priced |
| standing | preseason data drop; camp roles; Butler severity; Wagler / WAS-center / Daniels-minutes watches |

## Open-item receipts

| check | receipt |
|---|---|
| Recap-vs-feed reconciliation | 156/156 mapped; the insert, four unknown-name corrections and two halted re-sends all match |
| Harness fidelity | `live_retro.py 51 final/replay/hindsight` regenerated the tracked mock-51 JSON byte-for-byte before grading 52 |
| Card parity | Python port vs the deck's own JS: Top-5 names and blend scores identical at 13/13 owner turns |
| Category/H2H/championship figures | computed 2026-09-22 on current lines, deck plane; 18,000 CRN seasons per arm |
| Market prices quoted | `report/market/yahoo-2026-09-22.csv` (draft-analysis page, ADP + XRank), landed on PR #29 |
| Publication gate | `report/check_report.py` PASS on this file |

## Bounds

**Out of scope by design:** opponent-intel conclusions (random public room);
any roster or projection edit; the survival refit itself (data now in hand,
decision the owner's). **Model bounds:** seats 4 and 11 are one man short in
every simulation, which flatters the owner against those two seats only; the
championship rate carries the room's weakness in its denominator; the punt box
after #39 is read from the feed (no later Retarget was logged).

## Decision sheet (owner disposes)

| # | decision | default if silent |
|---|---|---|
| D52-1 | Merge and publish so the next live room runs on the tuned deck and Yahoo's price: deck #34 then #37, #35 then #36, #33 then #38; kit #29 then this report | nothing merges; the next room repeats v23 |
| D52-2 | Tatum (`inj-achilles-risk`) and Kyrie (`inj-acl-risk`) multipliers: keep 0.78, or revise on your read of their camps | keep 0.78 |
| D52-3 | Survival-chip refit on the two live rooms (98 rows) | chips stay suspended |
| D52-4 | The seven ADP-inside-140 names without a pool row, plus Jenkins and Santos: research and add, or ignore as room noise | ignored until a third room shows them again |
| D52-5 | Cam Whitmore CLE vs DEN: verify at the next pull | flagged only |

## Provenance

Deck plane: `yahoo-fantasy-basketball` PR #38 (`claude/mock52-live`, stacked
on #33) — state, harnesses, `arena/results/m52_*.json`,
`debrief_2026-09-22_mock52_slot10.md`, LEDGER row 52. Market: PR #29
(`claude/market-data-workorder-mnfi2b`). This report: PR stacked on #29.
