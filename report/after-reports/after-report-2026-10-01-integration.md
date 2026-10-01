# After-report — 2026-10-01: D-WO1-1 (a)+(d) applied, then a full integration, calibration and integrity check (deck v39)

**Owner decision (2026-10-01, verbatim):** "(a) and (d) go ahead. Afterwards,
conduct a full system integration, calibration, and integrity check please.
If all green, merge."

**What (a) and (d) are.** (a): the preseason refresh (WO-5, after 10/5)
re-derives every top-150 line from box scores and writes one line to both
planes; the tail takes the kit's line. Nothing to do today beyond the
schedule. (d): the thirteen rows on which the two planes differed by three
or more points become one line now — the plane whose points sit nearer
Hashtag's 9/30 projection is adopted on both, RotoBaller's 9/29 projection
the second outlet; Gradey Dick, outside Hashtag's top 200, takes the kit's
line.

**Method.** The thirteen lines copied by script across the eleven shared
per-game columns with assertions on every row (a second run changes
nothing; `report/lines_sync_2026-10-01.json` carries every before/after);
GP, minutes, tags and notes untouched. Kit board and slate regenerated.
Deck re-stamped, colophon extended, built as v39 with the thirteen
propagation waivers named in the manifest, then the full verification set:
planes gate, parity, the three suites, the 128-assertion browser drive, a
fresh direct roster verification against ESPN, the kit's provenance and
reproduction gates. Calibration: mock 59 (the latest live room, drafted on
v37) re-graded on the v39 pool with the `--tag` re-grade the 9/29 final
check used, so the change's effect on a real room is measured, not argued.
Verification: this file passes `report/check_report.py`.

Pull window: 2026-10-01 → 2026-10-01 (owner decision; not a roster pull).

**Headline.** Thirteen wide lines are one line on both planes; deck v39 built, every gate and suite green (one data-pinned test fixture re-pointed), Version 39 published. Mock 59 re-graded on the reconciled pool: as drafted 15.21% (20.38% on v37), four of thirteen 🎯s change — both Poeltl turns among them — and the owner's #63 Lillard pick reads as a reach (card #2 to #32; hindsight 2nd to 43rd); the v37 card's #82 🎯 (Poeltl) grades below the owner's pick on the reconciled line (13.28% against 15.21%). All green; merged.

## 1. The thirteen lines

[EVIDENCE: `report/lines_sync_2026-10-01.json`; `hashtag-2026-09-30.csv`;
`rotoballer-2026-09-29.csv`]

| player | points kit / deck | Hashtag 9/30 | RotoBaller 9/29 | line adopted | plane that changed | columns changed |
|---|---|---|---|---|---|---|
| Damian Lillard | 17.0 / 24.0 | 19.1 | 16.6 | kit | deck | 11 |
| Anfernee Simons | 19.5 / 14.5 | 15.1 | — | deck | kit | 9 |
| Luka Dončić | 30.0 / 33.5 | 32.7 | 32.4 | deck | kit | 9 |
| Cooper Flagg | 21.0 / 17.8 | 23.3 | 22.4 | kit | deck | 10 |
| Quentin Grimes | 14.0 / 17.5 | 15.5 | — | kit | deck | 9 |
| Cedric Coward | 16.3 / 13.0 | 16.3 | 14.2 | kit | deck | 10 |
| Sandro Mamukelashvili | 13.7 / 10.5 | 13.7 | 12.0 | kit | deck | 10 |
| Gradey Dick | 12.0 / 15.0 | — | — | kit | deck | 9 |
| Jakob Poeltl | 11.5 / 14.5 | 12.4 | 11.8 | kit | deck | 10 |
| Kevin Porter Jr. | 11.5 / 14.5 | 12.9 | 11.8 | kit | deck | 10 |
| Malik Monk | 14.5 / 17.5 | 14.6 | — | kit | deck | 9 |
| Miles Bridges | 17.0 / 20.0 | 18.0 | 17.1 | kit | deck | 11 |
| RJ Barrett | 17.5 / 20.5 | 20.5 | 19.6 | deck | kit | 9 |

Two outlets per row, as promised: Hashtag decides, RotoBaller is written
up beside it. RotoBaller agrees with the verdict on seven of the nine rows
it covers and sits nearer the deck's line on two (Coward 14.2, between the
two; Mamukelashvili 12.0, marginally nearer 10.5 than 13.7). Both of those
kit lines are Hashtag's own 8/24 line inherited when the rows were added,
so the agreement there is inheritance; averaged over the two outlets the
kit's line is still the nearer one on both (15.25 and 12.85). The rule the
owner approved was applied as stated; these two are the weakest of the
thirteen and the refresh re-derives them from box scores anyway. 126
column values changed in all; 171 shared rows still carry differing lines
(184 before).

## 2. Board effects (computed, never eyeballed)

[EVIDENCE: `report/top-200-2026-27.md` before and after; `hoops.adj_value`
order on `data/players.csv` v38 vs v39]

- **Kit.** Three rows changed. Simons 82 → 179 (the deck's 14.5-point line
  adopted); Dončić and Barrett moved within noise; 113 other rows displaced
  by one or two places from re-standardising; Taylor Hendricks re-enters the
  top 200, Royce O'Neale leaves. Top 12 unchanged.
- **Deck.** Ten rows changed, and these are the card's reads that moved:
  Lillard 28 → 89 (value +1.92 → −0.96), Poeltl 46 → 132 (+0.66 → −1.96),
  Flagg 38 → 22 (+1.15 → +2.45), Bridges 75 → 122, Grimes 98 → 164, Monk
  113 → 160, Porter Jr. 159 → 235, Dick 195 → 255, Mamukelashvili 217 → 83,
  Coward 164 → 133; 191 other rows displaced by a place or two. Simons,
  Dončić and Barrett unchanged on the deck (the kit adopted their lines).
- **What this says about the last four rooms.** Poeltl was the card's 🎯
  at #82 in all of mocks 56 to 59 and the subject of the owner's second
  proposal (D59-2). On the reconciled line he is a round-11 value, not a
  round-7 one: part of "the card names men the room will not take for
  rounds" was the deck's own points, not only the price-blind 🎯. The
  survival-aware advice line (D59-2 small) still stands on its own evidence;
  the deep-🎯 pattern it addresses should be rarer on v39.

## 3. Integration — the build and its gates

| gate | result |
|---|---|
| line sync script (both planes, 13 rows, assertions on every row) | 126 column values changed; a second run changes 0 |
| deck `check_planes.py` after the sync | 314 shared · team 0 · exclusion 0 · drift 0 · propagation 0 (13 named waivers, D-WO1-1) · lines 171 (was 184) |
| deck `build_deck.py` gates 1–7 + F8 (v39) | all pass; market `yahoo-2026-10-01.csv` priced 297/334; pool `1ecfb66bdcef`; injection round-trip OK; waivers recorded in the manifest |
| deck `verify_rosters.py` direct-complete, fresh run this evening | 30 rosters, 333 of 334 matched, 0 mismatches, 1 exemption (Tony Bradley) |
| deck `check_parity.py` | PARITY: EXACT MATCH (324 market ranks compared) |
| deck `test_card.py` / `test_draft.py` / `test_gates.py` | CARD all 68 cases passed — after re-pointing one data-pinned fixture: the D51R-4 availability-branch probe (state_54 #34) stopped producing an urgent read on the reconciled lines, the 9/29 scan repeated on the v39 page (16 states × 208 owner turns) found four urgent reads, three withheld on availability, and the probe now measures on the un-vetoed one (mock31 #64, Zion 0.78); the four synthetic gate cases never moved / all 62 cases passed / all 37 cases passed |
| deck `full_dom_check.mjs` on the built page | 128 assertions, 0 failed, 0 page errors, pass (`arena/results/full_dom_check_2026-10-01_v39.json`) |
| kit `rank_engine.py` provenance gate | PASS — board regenerated, 200 of 324 |
| kit `slate.py` | regenerated (ADP 2026-10-01) |
| kit `check_report.py` | PASS (this file) |
| kit `check_provenance.py` | PASS — all rows sourced |
| kit `check_derived.py` | PASS — all 13 dated artifacts reproduce byte-for-byte at their pins |
| artifact publish | Version 39 (id `1790890616-1e8d`) at the standing URL; page 369,616 bytes, sha256 `f294b73383413752…` |

## 4. Calibration — mock 59 re-graded on v39

[EVIDENCE: `arena/results/m59_deckcard_v39.json` against `m59_deckcard_v37.json`;
`m59_*_v39.json` from `live_retro.py 59 <stage> --tag v39`;
`m59_followcard_grade_v39.json`]

The card, replayed on the v39 page at the owner's thirteen turns of mock 59
(the room was drafted on v37; its grade on the record stays v37's):

| pick | 🎯 on v37 | 🎯 on v39 | owner took | card rank v37 to v39 |
|---|---|---|---|---|
| #10 | Towns | Towns | Haliburton | 3 to 3 |
| #15 | Towns | Towns | Towns | 1 to 1 |
| #34 | Jalen Williams | Jalen Williams | Jalen Williams | 1 to 1 |
| #39 | Derrick White | Derrick White | Kessler | 47 to 39 |
| #58 | Anunoby | **Pritchard** | Anunoby | 1 to 2 |
| #63 | Pritchard | Pritchard | Lillard | 2 to **32** |
| #82 | **Poeltl** | **LaVine** | Day'Ron Sharpe | 12 to 5 |
| #87 | LaVine | LaVine | Edgecombe | 20 to 17 |
| #106 | **Poeltl** | **Lendeborg** | Queta | 52 to 46 |
| #111 | Gillespie | Gillespie | Gillespie | 1 to 1 |
| #130 | Vassell | **Mamukelashvili** | PJ Washington | 2 to 3 |
| #135 | Vassell | Vassell | Lendeborg | 5 to 5 |
| #154 | Vassell | Vassell | Vassell | 1 to 1 |

Four of thirteen 🎯s change. The two that matter are the Poeltl turns: on
the reconciled line the card names LaVine at #82 and Lendeborg at #106, so
the "deep 🎯 the room will not take for rounds" of D59-2 was, in this
room, partly the deck's own 14.5-point Poeltl line. Lillard, the owner's
#63 pick, falls from the card's #2 to #32 on his reconciled 17.0-point
line: the pick that read as a near-🎯 on v37 reads as a reach on v39.

The as-drafted grade moves with the pool, as it must — the pool a
finished room is scored on changed, not the picks:

| roster (mock 59, slot 10; real eight-team bracket) | on v37 | on v39 |
|---|---|---|
| as drafted | 20.38% · ECW 5.092 rank 2 · favored 10 of 11 | 15.21% (rank 2) · ECW 4.877 rank 2 (next 5.272) · favored 10 of 11 |
| follow the card, self-consistent | 39.18% (Maxey at #10, White at #39, Poeltl at #63, Lillard at #82, Bridges at #87, Sharpe at #106) | 37.13% · ECW 5.548 rank 1 (Tyrese Maxey at #10, Derrick White at #39, Jarrett Allen at #63, Zach LaVine at #82, Josh Hart at #87, Sandro Mamukelashvili at #106, Cason Wallace at #111) |
| Derrick White at #39 only | 27.14% | 21.26% |
| Zach LaVine at #87 only | 23.32% | 17.82% |
| survival-aware: LaVine at #82, Poeltl at #87 | 26.36% | 15.54% |
| Jakob Poeltl at #82 only | 23.06% | 13.28% |

Hindsight on v39 (the legal choice at each owner turn, graded against the
finished room): the owner's #63 pick, Lillard, falls from the 2nd-best
legal choice to the 43rd — the card's Pritchard is worth +0.265
categories a week there (+0.047 on v37); Kessler at #39 stays the
largest miss (White +0.251, was +0.237); Edgecombe at #87 improves from
11th to 5th; Queta at #106 goes 45th to 49th. Forecast
calibration (the card's Top-5 against hindsight, Spearman ρ averaged over
the thirteen turns): shipped card 0.815 on v37, 0.838 on v39; value-only
0.620 and 0.663. Two arms change meaning on the reconciled lines: Poeltl
at #82 alone now grades below the owner's own pick (13.28% against
15.21%, rank 3) — the v37 card's 🎯 at that turn was, on the line
both planes now carry, a worse choice than Sharpe; and the survival-aware
pair (LaVine at #82, Poeltl at #87) is a wash (15.54% against 15.21%)
because Poeltl at #87 no longer adds anything. The D59-2 advice line rests
on `target_wait.py`'s survival counts, not on that roster's grade, so it
stands; the roster that illustrated it does not. The v37 grade stays the
room's record (D-INT-1); this section is the calibration row.

**Decisions.**
- **D-INT-1** — mock 59's grade on the record stays v37's (the pool it was
  drafted on); the v39 re-grade is a calibration row, not a re-score.
  Default: yes.
- **D-INT-2** — re-grade mocks 56 to 58 on v39 as well? They were drafted on
  v31 to v35 and each carried the old Poeltl and Lillard lines. Default: no —
  mock 60 on v39 is the cheaper and cleaner test.

## 5. Integrity

| check | result |
|---|---|
| roster verification, fresh direct run against ESPN's thirty rosters | 333 of 334 matched, 0 mismatches, 1 exemption (Tony Bradley, NYK camp deal not yet on the feed) |
| planes gate (after the sync) | 314 shared · team 0 · exclusion 0 · drift 0 · propagation 0 with 13 named waivers · lines 171 |
| kit `check_provenance.py` | PASS — all rows sourced |
| kit `check_derived.py` | PASS — all 13 dated artifacts reproduce byte-for-byte at their pins |
| line sync idempotence | a second run changes 0 columns on either plane |
| git state at merge | both mains fast-forwarded, working trees clean |

## Watchlist

- **Mock 60 on v39**: the first room with Lillard, Poeltl and Flagg on the
  reconciled lines; the card's reads at the owner's round-5 to round-7
  turns are the thing to watch.
- **The other 171 differing lines**: the refresh after 10/5 (WO-5);
  `--planes-lines-strict` at the final build on 10/14 is what proves it.
- Carried: D59-1 (insert re-numbering), D59-2 (advice line), D-ADP-1/2
  (next pull), the ESPN page as a PDF, the league settings screenshot.

## Open-item receipts

| item | query run (2026-10-01) | dated finding |
|---|---|---|
| (this change) | machine joins and gates only — no web research | the 10/01 daily pull's receipts cover the window |
| Jalen Duren, Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the daily pull's dedicated queries, same day (after-report-2026-10-01.md) | all HELD on 2026-10-01; none of the thirteen rows is a flagged name |

## Bounds

- The thirteen lines are projections chosen by proximity to one outlet
  with a second written up; they are not box-score derivations. The refresh
  overwrites most of them.
- The calibration re-grade changes the pool a finished room is scored on;
  it measures the change's effect on that room's grade, not a new truth
  about the room.
- The deck board movement counts rank displacement among all 334 rows; a
  one-place move from re-standardising is counted the same as a real one,
  which is why the ten changed rows are listed by name.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-WO1-1 | Closed for the thirteen rows by (d); (a) stands for the rest at the refresh. | — |
| D-INT-1 | Mock 59's grade on the record stays the v37 grade (the deck the owner drafted against); the v39 re-grade is a calibration row in the ledger, not a replacement. Keep it that way? | yes |
| D-INT-2 | Re-grade mocks 56 to 58 on v39 as well (about 25 minutes of compute each), or let mock 60 be the next data point? | mock 60; the three re-grades only if the owner wants the full restatement |

## Provenance

- Inputs: the owner's decision in chat (2026-10-01); `hashtag-2026-09-30.csv`
  and `rotoballer-2026-09-29.csv` (committed); both planes' pools at the
  10/01 evening state.
- Every number is a command's output or a field of the files named; the
  board diffs were computed from the committed board before and after.
- Not verified: nothing here rests on web research.
