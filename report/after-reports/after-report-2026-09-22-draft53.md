# After-Report — draft_53: third live-human mock from the REAL slot 10, plus the Insert-at-# integrity test

**Owner request (2026-09-22, verbatim):** "One more live mock draft recap for
you. I noticed when: I use the 'insert at # pick' tool, the Deck tool breaks
and continues to say (YOURE ON THE CLOCK). Additionally, can you please
conduct an integrity test where: When I use the insert at # function, the
tool is operating correct - as in assigning the players to the right team,
and that categorical computation is still accurate?" Two inputs again: the
deck tool's pick-by-pick feed, then Yahoo's recap — the authoritative record.

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (the real league slot;
opponents are random humans — a practice rep, not opponent intel). Two
"David"s in the room: seat 6 is the other one. **Deck used:** one of the two
same-day builds (v24 or v25 — identical Yahoo 9/22 prices, identical engine;
v25 carries 66 more pool rows). **Method:** the recap was reconciled against
the feed pick-by-pick; the insert test replays the owner's whole tool log two
ways — through the deck engine headlessly and through the real page in
headless Chromium; the grade is the deck plane's machine-derived retro
(`yahoo-fantasy-basketball` `arena/results/m53_*.json`, debrief
`debrief_2026-09-22_mock53_slot10.md`). Every figure below is read from those
files; none is eyeballed. Verification: this file passes
`report/check_report.py`; receipts in §8.

Pull window: 2026-09-22 → 2026-09-22 (analysis run 2026-09-22 against the
9/22 pool and market files; not a roster pull — the 9/22 pull-log row covers
the window).

**Headline.** The insert tool placed every shifted pick on the right seat
and the deck's category math is unaffected — proven, not eyeballed (§4). The
"you're on the clock" message was a real defect, reproduced in the real page:
it fires after your 13th pick, whatever came before, and is fixed (§4). The
draft itself: ECW **5.563** cats/week, rank **1 of 12**, favored in **11 of
11** head-to-heads, championship rate **38.53%** over 18,000 simulated seasons
(next seat: MichaelH, 5.274) [EVIDENCE: `m53_final.json`, `m53_arms.json`].
Mocks 51 and 52 from the same seat read 5.610 / 55.03% and 5.634 / 47.94%.
The survival chips met their first out-of-sample room and under-predicted
survival (§5).

---

## 1. Validation vs the Yahoo recap

| check | result |
|---|---|
| recap picks | 156, a clean snake; the manager at each seat consistent across all 13 rounds |
| feed events | 169: 163 feeds (2 halts, 2 UNKNOWN placeholders and their fixes), 3 undos, 3 Insert-at-# uses (1 refused as ambiguous "White") |
| final board | the feed's board equals Yahoo's on all 156 picks and seats after both inserts |
| your roster | Tatum, Towns, Mobley, Jalen Williams, Lillard, Anunoby, Quickley, Myles Turner (#87, moved there by the Coby White insert), Poeltl, Reed Sheppard, Tre Jones, Cameron Johnson, P.J. Washington — 13/13 as Yahoo lists them |
| poolless names | none (the 330-row pool covers every pick in this room) |

## 2. The team, replayed

Category ranks by the weekly model: FG% 8 · FT% 3 · 3PTM 3 · PTS 3 · REB 5 ·
AST 6 · ST 2 · BLK 4 · TO **1**. Board rank 1 by kept-total z-sum (+12.78;
next +8.37). Season-shape head-to-head wins 10 of 11 (MichaelH the exception,
4 of 9 categories). No punt declared; the room-relative advisor never
advised — an AST lean showed at #58 and #82 and cleared.

## 3. Pick by pick — card vs owner vs hindsight

Card #1 taken at 7 of 13 turns (#15 Towns, #34 Mobley, #39 Jalen Williams,
#63 Anunoby, #87 Turner, #106 Poeltl, #135 Cameron Johnson); hindsight found
no better legal pick at five of them. The three departures that cost the
most, in ECW gain of the best legal alternative on current lines:

| pick | owner | card rank | hindsight best | gain |
|---|---|---|---|---|
| #130 | Tre Jones | 33 | Christian Braun (went #145) | +0.141 |
| #10 | Jayson Tatum (`inj-achilles-risk`, 0.78) | 17 | Chet Holmgren (went #23) | +0.129 |
| #111 | Reed Sheppard | 16 | Christian Braun | +0.109 |

Tatum at #10 is the third room in a row where the owner took him against the
card (52.82% vs 47.94% swap in mock 52; 46.26% vs 38.53% here). Christian
Braun was card-available and passed at #111, #130 and #135 again (mock 52:
passed three times). Follow-card arm 55.59%.

## 4. Insert-at-# — the defect and the integrity test

**The defect, reproduced.** `live_replay_dom.mjs` drove the published page in
headless Chromium through all 169 events. Zero page errors, every echo line
reproduced. The countdown under the feed title was wrong at exactly two
events: after picks #154 and #155 it read "(YOU'RE ON THE CLOCK)" while the
status strip beside it correctly read "Seat 11 on the clock" and "Seat 12 on
the clock". Root cause: once your 13th pick is in, the engine's next-pick
lookup returns null and the countdown treated null as "0 until your pick".
It fires after your LAST pick, whatever came before; the second insert
episode in this room ended at your #154, which is why it looked like the
insert broke the deck. At both inserts the clock was right ("18 until your
pick" after Coby White; "7 until your pick" after Portis).

**The fix (D-M53).** One engine function, `clockRead`, is now the single read
of the clock (phases done / you / none-left / wait); the countdown says
"your roster is full — N picks left in the draft" in the none-left phase and
the strip says "no picks left for you". A refused insert now shows its
warning immediately (it used to surface on the next action). Written red
first: 8 new `test_card` cases on this room's board (35/35), a Python twin
with parity item 8 (EXACT), and the Chromium replay re-run on the fixed page:
0 clock mismatches, 0 echo misses, 0 page errors.

**Placement and computation.** `insert_integrity.py` replayed the same 169
events through the engine and built the same board from scratch in Yahoo's
order:

| check | result |
|---|---|
| final board (156 picks with seats) | identical |
| every roster | identical |
| category ranks, all 12 seats | identical |
| category matrix, 9 × 12 | identical |
| ΔECW card ordering at all 13 owner turns | identical |
| Python `insert_pick` on the exact pre-insert boards | refuses the ambiguous name; reproduces both inserts |
| Python rosters vs the deck's | identical |

After each successful insert the board returned to an exact prefix of
Yahoo's order; the only non-prefix moments were your own mid-course states
(Turner typed at #86 before the insert, the two UNKNOWN placeholders before
their fixes, Herbert Jones before the undo, the four picks logged before the
Portis insert). One precision note, not an insert defect: the Python rank
helper and the deck split a 3PTM tie (seats 10 and 2 at 2.49269) differently
because the deck carries z-scores to six decimals. Record:
`arena/results/m53_insert_integrity.md`.

## 5. Survival chips — first out-of-sample room for the refit

| room | rows | mean predicted | realized | Brier | constant base rate |
|---|---|---|---|---|---|
| mock 53 (out of sample) | 53 | 0.501 | 0.755 | **0.217** | 0.185 |
| pooled with mocks 51 + 52 | 152 | 0.511 | 0.717 | 0.197 | 0.203 |

The refit did NOT beat this room's constant base rate: players survived more
than the price model expects (BUY NOW 4 of 8 gone; TOSS-UP 5 of 12 gone; quiet
rows 29 of 33 survived). Pooled over three rooms it still edges the base
rate. The quiet side ("safe to wait") keeps holding; BUY NOW is now 14 of 23
across the three rooms. Decision D53-2.

## 6. What this run answers and asks

- **Answered:** the insert tool is correct on placement and math; the clock
  message was a display defect with a one-function root cause, fixed and
  shipped.
- **Answered:** the deck's grade is stable across three live rooms from the
  real seat (ECW 5.56–5.63, rank 1 each time); the follow-card arm is 55–63%.
- **Asks:** the survival chips' out-of-sample miss (D53-2); Tatum at #10 a
  third time (D53-3); the feed resolver does not match Yahoo's dotted
  spelling "P.J. Washington" (the owner typed "PJ") — D53-4.

## Watchlist

| item | detail |
|---|---|
| survival model | third-room data in hand (152 rows); refit with all three before the real draft, or keep the chips advisory as stated on the tooltip |
| dotted spellings in the feed | "P.J. Washington" does not resolve; "PJ Washington" does — add dot-folding to the resolver at the next tune-up |
| deck build used in this room | v24 or v25 (same prices); unknowable from the log |
| standing | Duren camp open 9/29; camp bodies (Brown, Konchar, Krejčí, Sochan); Gueye return timeline |

## Open-item receipts

| check | receipt |
|---|---|
| Recap-vs-feed reconciliation | 156/156 mapped after both inserts; the ambiguous insert, two UNKNOWN fixes, three undos and two halted re-sends all match |
| Defect reproduction | Chromium replay on the unfixed page: wrong countdown at events 166 and 167 only, 0 page errors (`m53_dom_replay_unfixed.json`) |
| Fix verification | Chromium replay on the fixed page: 0 mismatches (`m53_dom_replay.json`); test_card 35/35; parity EXACT incl. item 8; test_gates 34/34; test_draft 57/57 |
| Insert integrity | engine replay vs from-scratch board identical on picks, rosters, ranks, matrix, cards; Python inserts equal (`m53_insert_integrity.json`) |
| Harness fidelity | mock 52's final and hindsight regenerate byte-identical on the pinned v23 pool after the pool grew to 330 rows |
| Category/H2H/championship figures | computed 2026-09-22 on current lines, deck plane; 18,000 CRN seasons per arm |
| Publication gate | `report/check_report.py` PASS on this file |

## Bounds

**Out of scope by design:** opponent-intel conclusions (random public room);
roster or projection edits; a survival re-fit (data recorded, decision the
owner's). **Model bounds:** the championship rate carries the room's weakness
in its denominator; hindsight is single-swap on current lines, an upper
bound; which of the two same-day builds the room ran on is not recoverable
from the log (identical prices and engine, so no figure above depends on it).

## Decision sheet (owner disposes)

| # | decision | default if silent |
|---|---|---|
| D53-1 | The clock fix and the integrity harnesses: merged and published as Version 26 of the standing deck | shipped |
| D53-2 | Survival chips after the out-of-sample miss: keep on (rates stated on the tooltip), re-fit on 152 rows, or suspend again | keep on; re-fit before the real draft |
| D53-3 | Tatum at #10 against the card a third time: keep the 0.78 multiplier and the card's read, or set a judgment override | keep |
| D53-4 | Dot-folding in the feed resolver ("P.J." → "PJ") | queued for the next tune-up |

## Provenance

Deck plane: `yahoo-fantasy-basketball` `claude/mock53-insert-integrity`
(two commits: the fix + harnesses, then the grading outputs) — state,
`arena/results/m53_*.json`, `m53_insert_integrity.{json,md}`,
`debrief_2026-09-22_mock53_slot10.md`, LEDGER row 53. Kit: this report.
