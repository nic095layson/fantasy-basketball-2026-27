# After-Report — draft_54: fourth live-human mock from the REAL slot 10, and the Porziņģis veto

**Owner request (2026-09-28, verbatim):** "Please standby for following
message with Yahoo live mock draft results. Here is the draft tool's log:"
— then the deck tool's pick-by-pick feed and Yahoo's recap (the
authoritative record) in one message. The same message carried the
executive decision that Porziņģis is DO NOT DRAFT (recorded in
`after-report-2026-09-28.md` §9; the owner chose the contained veto over a
manual skip).

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (the real league slot;
opponents are random humans — a practice rep, not opponent intel). Two
"David"s in the room again: seat 9 is "David M". **Deck used:** v28, the
9/28 pull build (Hield/Dillingham trade, DLo and Broome waived, Jamal
Murray's tag corrected; Yahoo 9/22 prices), before the veto landed.
**Method:** the recap was resolved to pool names by script (156 of 156, no
unresolved name) and the state was checked snake-consistent; the grade is
the deck plane's machine-derived retro (`yahoo-fantasy-basketball`
`arena/results/m54_*.json`, debrief `debrief_2026-09-28_mock54_slot10.md`,
deck card replayed from the deck he drafted against, `rev b150541`). Every
figure below is read from those files; none is eyeballed. Verification:
this file passes `report/check_report.py`; receipts in the section below.

Pull window: 2026-09-28 → 2026-09-28 (analysis run 2026-09-28 against the
9/28 pool and the 9/22 market file; not a roster pull — the 9/28 pull-log
row covers the window).

**Headline.** The best live room yet from the real seat: ECW **5.552**
cats/week, rank **1 of 12**, favored in **11 of 11** head-to-heads,
season-shape 11 of 11, championship rate **49.36%** over 18,000 simulated
seasons (next seat: gaby, 4.912) [EVIDENCE: `m54_final.json`,
`m54_arms.json`]. Mocks 51, 52 and 53 from the same seat read 5.610 /
55.03%, 5.634 / 47.94% and 5.563 / 38.53%. The owner took the card's 🎯 at
8 of 13 turns and a Top-5 row at 11 of 13. The survival chips beat their
base rate in a second out-of-sample room (§5). The tool board drifted one
slot for eleven picks after an UNKNOWN was followed by a fresh feed (§4) —
the owner's own roster was untouched.

---

## 1. Validation vs the Yahoo recap

| check | result |
|---|---|
| picks in the recap | 156; every "Last, First" line resolved to a pool name by script (dot and suffix retries; zero unresolved) |
| snake attribution | all 156 seats match the round parity; the owner's 13 picks sit at #10, #15, #34, #39, #58, #63, #82, #87, #106, #111, #130, #135, #154 |
| poolless names | none — every pick in this room is a v28 row |
| cast | seats 1–12: gaby, CJ, Isaiah, Justin, Team 5, Rogelio, ben, Bonani, David M, **David (10)**, JB, Ali Ege |
| state | `arena/data/states/draft_state_54.json`, md5 `c576efd303176ee0e884fbc1e9050cc8` |

## 2. The team, replayed

| readout | value | evidence |
|---|---|---|
| ECW (cats/week vs the average opponent) | **5.552**, rank 1 of 12 (next 4.912) | `m54_final.json` |
| head-to-heads favored | 11 of 11 (per-opponent expected cats 5.11–6.03) | `m54_final.json` |
| season-shape H2H | wins 11 of 11 | `m54_final.json` |
| board rank (kept-total z-sum) | 1 (+13.81; next +1.43) | `m54_final.json` |
| category ranks, weekly model | FG% 4 · FT% 6 · 3PTM 4 · PTS 8 · REB 3 · **AST 10** · **ST 1** · BLK 3 · TO 4 | `m54_final.json` |
| championship rate, as drafted | **49.36%**, playoff 99.73%, rank 1 | `m54_arms.json` |
| follow-card arm | 60.11% (swaps #39 Derrick White, #135 Christian Braun) | `m54_arms.json` |
| best single swap | #135 Christian Braun → 56.93% | `m54_arms.json` |

The roster is a steals-and-bigs build with a dead assists column (rank 10):
Towns, Jalen Johnson, Jalen Williams, Kyrie, OG, Pritchard, McDaniels,
Turner, Cameron Johnson, Poeltl, Eason, Ajay Mitchell, PJ Washington.

## 3. Pick by pick — card vs owner vs hindsight

| pick | card 🎯 | owner | card rank | hindsight best (gain, ECW) |
|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Towns | 1 | none |
| 15 | Jalen Johnson | Jalen Johnson | 1 | none |
| 34 | Jalen Williams | Jalen Williams | 1 | Derrick White +0.028 |
| 39 | Derrick White | Kyrie Irving | 4 | Derrick White +0.101 |
| 58 | OG Anunoby | OG Anunoby | 1 | Tyler Herro +0.046 |
| 63 | Payton Pritchard | Pritchard | 1 | Tyler Herro +0.004 |
| 82 | Myles Turner | Jaden McDaniels | 16 | Coby White +0.124 |
| 87 | Myles Turner | Myles Turner | 1 | none |
| 106 | Cameron Johnson | Cameron Johnson | 1 | none |
| 111 | Jakob Poeltl | Jakob Poeltl | 1 | none |
| 130 | Christian Braun | Tari Eason | 2 | Christian Braun +0.015 |
| 135 | Christian Braun | Ajay Mitchell | 33 | Christian Braun +0.165 |
| 154 | Brook Lopez | PJ Washington | 3 | Brook Lopez +0.065 |

Costliest departures from the card: **#135 Ajay Mitchell** (card #33;
Braun +0.165, drafted #145 by gaby), **#82 Jaden McDaniels** (card #16; Coby
White +0.124, drafted #89), **#39 Kyrie** (card #4, availability 0.78;
Derrick White +0.101, drafted #45). The 🎯 was the blend50 #1 at every turn;
no LAST CALL pin fired and none was withheld [EVIDENCE:
`m54_deckcard_v28.json`]. The advisor leaned AST from #58 and advised it
from #63 on; no button exists to take it and the box stayed empty (D51R-3).

**Porziņģis on the card this room:** 6th row at #63, 4th at #82, 3rd at
#87, never the 🎯; the room took him at #101 (seat 5). With the veto now
live (Version 29) those rows go to the next name down — the Chromium check
on mock 51's equivalent turn shows exactly that promotion.

## 4. Tool-state integrity — the deck's board vs the recap

The owner's tool log was replayed into its final board and diffed against
the recap position by position [EVIDENCE: `m54_tool_vs_truth.json`]:

| finding | detail |
|---|---|
| owner's roster | identical to the recap, all 13 |
| positions differing | 13 of 156 |
| #97 | logged as UNKNOWN ("LavineWiggins") and never fixed — Andrew Wiggins (seat 1) is absent from the tool board |
| #118 through #129 | UNKNOWN ("mamy") was followed by a fresh feed of "Sandro Mamukelashvili", which logged as pick #119 instead of fixing #118 — every pick through #129 sits one slot late on the wrong seat until the owner's own #130 correction (Vassell to Eason) re-synced the board; Devin Vassell (seat 9) is absent from the tool board |
| inserts | Giddey at #19 and Suggs at #105 both match the recap |
| assumed-over resolutions | all 12 correct against the recap |

The seat math was right throughout; the drift is a usage pattern, not a
placement defect: after an UNKNOWN line the next entry must be `118- Name`
(a fix), not a new pick. Decision D54-2 below asks whether the tool should
catch this itself.

## 5. Survival chips — second out-of-sample room for the refit

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 54 (out of sample) | 50 | 0.534 | 0.780 | **0.168** | 0.172 |
| pooled, four rooms | 202 | 0.517 | 0.733 | 0.190 | 0.196 |

BUY NOW: 9 rows, 6 gone. TOSS-UP: 10 rows, 4 gone. Quiet: 31 rows, 30
survived. After mock 53's miss (0.217 vs 0.185) the model is back ahead of
the base rate out of sample, and the pooled margin stands at 0.006
[EVIDENCE: `m54_survival.json`].

## 6. What this run answers and asks

- **Answers:** the seat-10 process holds in a fourth random room (four rooms,
  four first-place ECW reads; championship 38–55%). The card's #1 was taken
  at 8 turns and was hindsight-unbeatable at 5 of them. The survival refit
  survived a second out-of-sample test.
- **Asks:** the late-round departures (#135 Ajay Mitchell over Braun,
  −0.165; #82 McDaniels over Coby White, −0.124) are the whole gap between
  49% and the 60% follow-card arm (D54-1); the UNKNOWN-then-fresh-feed drift
  (D54-2); and whether the AST advice, now nine turns running across two
  rooms, should be tested as a declared frame in the arena before the real
  draft (D54-3).

## Watchlist

- Ajay Mitchell (#135) and McDaniels (#82): both card-off picks; re-check
  the lines at the next pull (Mitchell's OKC role, McDaniels' usage).
- Porziņģis veto: live on Version 29; the retro harness applies it only to
  rooms drafted on v29 or later (`MOCKS[...]['veto']`).
- Survival chips: four rooms, 202 rows, +0.006 over base pooled — thin but
  positive; re-fit not needed before the real draft unless a fifth room
  misses.
- Yahoo market paste: six days old; early-October paste before 10/14.

## Open-item receipts

| item | query run (2026-09-28) | dated finding |
|---|---|---|
| (this analysis) | machine replay only — no web research in this report | pull receipts for the window live in `after-report-2026-09-28.md` §8 (10 of 10 flagged names) |

## Bounds

- Random public room: the field's weakness is in every denominator; the
  championship rate is not a league forecast.
- Hindsight is single-swap on current lines: an upper bound on a pick's
  cost, not a strategy.
- The Python replay port breaks exact blend ties by name (older rule) while
  the deck breaks them by ΔECW: at #106 the deck showed Cameron Johnson 🎯
  and the port lists Poeltl first; the card table above follows the deck.
- Lines are the v28 pool; the veto build (v29) shares it.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D54-1 | Late-round card-off picks (#82, #135) cost ~11 points of championship vs following the card; keep drafting on feel late, or commit to the 🎯 from round 8 on? | keep; record again next room |
| D54-2 | After an UNKNOWN line the next feed is logged as a new pick; should the tool prompt "fix #N?" when the previous pick is UNKNOWN and the new name resolves? | build it before 10/14 (small, deck app only) |
| D54-3 | AST advised at nine straight turns across mocks 53–54; run the declared-AST-punt arm in the arena before the real draft? | run it |

## Provenance

- Inputs: the owner's tool log and Yahoo recap (this session, 2026-09-28),
  transcribed verbatim into the scratch ledger and resolved by script.
- Every number is read from `arena/results/m54_*.json` and the debrief;
  the arms use 18,000 CRN seasons (seeds 11/23/47).
- Not verified: nothing here rests on web research.
