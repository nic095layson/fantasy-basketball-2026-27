Harness run: 2026-09-29T00:28:39.372Z on `docs/draft-deck.html` — 127 assertions, 2 failed, 0 page errors, crash: False.

| control | assertions | verdict | failing assertion (detail) |
|---|---|---|---|
| Teams / Rounds / Your slot inputs (echo) | 2 | PASS |  |
| Start draft — invalid config refused | 4 | PASS |  |
| Start draft — LIVE | 6 | PASS |  |
| Start draft — MOCK (cast seated, AI advances to your pick) | 3 | PASS |  |
| LIVE / MOCK mode buttons | 2 | PASS |  |
| Punt chips (9) at setup | 5 | PASS |  |
| ⟳ Daily sweep panel | 3 | PASS |  |
| Import draft_state.json (chooser, invalid JSON, missing keys, valid) | 4 | PASS |  |
| Export draft_state.json (download) | 4 | PASS |  |
| Copy state JSON (clipboard) | 1 | PASS |  |
| Reset draft (two-click confirm) | 3 | PASS |  |
| Pick feed — Log button and Enter | 2 | PASS |  |
| Pick feed — numbered correction (24- Name) | 2 | PASS |  |
| Pick feed — live hint under the box (D54-1) | 1 | PASS |  |
| Undo last pick | 4 | PASS |  |
| Insert at #… (toggle, empty input, insert) | 4 | FAIL | S2.insert-empty-warns: [] |
| Resync (toggle, empty paste, rebuild) | 4 | FAIL | S2.resync-empty-refused: null |
| Advance AI picks (MOCK) | 1 | PASS |  |
| Stage pick / Draft them buttons on the card | 3 | PASS |  |
| TARGET / BOARD LEAN button on the card | 1 | PASS |  |
| Tabs (Best available, Draft board, Rosters, Matrix, Head-to-head) | 5 | PASS |  |
| Best available — Pos filter | 1 | PASS |  |
| Best available — Find box and Enter (drafted lookup) | 2 | PASS |  |
| Best available — Show N | 1 | PASS |  |
| Best available — Lens select (val / ΔECW / fit / mkt) | 4 | PASS |  |
| Best available — category header clicks, 3-cat cap, drill, × chip | 5 | PASS |  |
| Best available — Reset | 1 | PASS |  |
| Best available — row click stages the pick | 1 | PASS |  |
| Best available — ⛔ DO NOT DRAFT marker | 1 | PASS |  |
| Head-to-head opponent select | 2 | PASS |  |
| Tooltip (data-tip hover) | 1 | PASS |  |
| Draft-complete state (strip, countdown, placeholder, card) | 9 | PASS |  |

| displayed number / computation | assertions | verdict | failing assertion (detail) |
|---|---|---|---|
| Status strip: pick #, round, seat on the clock, your next, roster n/13, N available (= availablePool) | 7 | PASS |  |
| Decision card top-5 = rankCard(decwScores) over the owner pool, every owner turn | 2 | PASS |  |
| Exactly one 🎯 on the card; veto never on the card | 1 | PASS |  |
| Draft board grid: 13 rounds × 12 seats, snake placement | 3 | PASS |  |
| Rosters tab: 12 rosters, kept-cat value = Σ totalValue | 2 | PASS |  |
| Matrix: every cell = categoryRanks totals, Kept column, rank note; punted column struck | 2 | PASS |  |
| Head-to-head: You/Them = rosterTotals, lead flags, W–L note, consistent with the matrix; punted label | 2 | PASS |  |
| Mkt column = marketRanks over the baked Yahoo prices | 1 | PASS |  |
| Lens orderings monotone (val, ΔECW, fit, mkt, cat lens, drill) | 6 | PASS |  |
| Your roster list and my-pick logging at all 13 owner turns | 13 | PASS |  |
| MOCK: typed my: pick logs, D54-1 gap warning, input memory across Undo | 3 | PASS |  |

Assertions not in either table (2): S1.setup-visible PASS, S1.advance-hidden-in-live PASS
Live replay notes: substitutions 5 (a mock-54 opponent name already taken by the card's earlier pick, replaced by the cheapest available), TARGET button present at 11 of 13 owner turns, LAST CALL rows 0; clipboard grant: granted; copy path: clipboard write + read-back verified.
