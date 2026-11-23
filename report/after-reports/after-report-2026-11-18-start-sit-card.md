# The start/sit card: one to three swaps that help, or keep the lineup (2026-11-18)

Pull window: 2026-11-18 → 2026-11-18 (no pull: kit main a40cf46, deck main 3551a15, the records branch season/daily at 2a61d547, read only; one deck page built in a throwaway worktree).

**Owner's request, verbatim (2026-11-18), with a screenshot of the Today tab.** "Hi Claude, can you please fine-tune this on the season page? It is recommending I swap in PJ Washington for all of these players-- But the tool should be dynamic and intuitive with: calculating who would be the best plug and play based on both team's remaining players' games, and forecasting; should be dialed down to top 1-3 player suggestions; more concise with its decision".

**Method up front.** Stated to the owner before the change: the model is unchanged (each swap is valued by `week_matchup.today_swap_cats`: the change in categories expected to be won this week if the bench player starts today, both teams' remaining games and the Week card's forecast counted). Only the selection and the wording change: a swap is suggested only when it adds expected categories (above 0); each bench player once, with his best starter to sit; at most three; under 0.05 categories (`week_matchup.LINEUP_D_EXP`, the kit's existing alert bar) is marked "small"; when nothing helps, the card says to keep the lineup and names the closest swap and its cost.

**Verdict. The card the owner photographed listed six pairs, PJ Washington for each starter, every one costing categories (−0.010 to −0.075). The model was right and the card read like a recommendation. It now reads "Keep your lineup" on that morning's records, and on a day when swaps help it lists at most three, one line each.**

Runner impact: code-only (the deck page's start/sit card and two record keys, `swap_keep` and `swap_small`; `swap_grid` keeps its key, now holding helpful swaps only). No prompt, step or pass line changes.

Pool rows touched: none

## 1. What changed

| | before | after |
|---|---|---|
| Rows | every bench-to-starter pair, top 6, gains and losses alike | only swaps that add expected categories; one per bench player; at most 3 |
| Nothing helps | the six losing pairs, in a heat map | "Keep your lineup. No bench swap adds categories this week; the closest, start X for Y, costs Z." |
| Each suggestion | a heat-map row | "1. Start X for Y (slot): +0.060 categories this week — helps REB +4.0, BLK +3.0 · costs PTS -1.0"; "(small)" under 0.05 |
| Heat map | the card's body | folded under "Category detail" |
| Card title | "Start/sit for today — by this week's needs" | "Start/sit today" |

Files: `scripts/season_deck.py` (`_swap_pairs`, `swap_grid`, `swap_keep`, `SWAP_SMALL`, the card), `scripts/test_season_deck.py` (SwapGrid: one new test, one rewritten).

## 2. Checks

| check | result |
|---|---|
| The owner's case | on season/daily 2a61d547 (the morning of the screenshot), the built page reads: "Keep your lineup. No bench swap adds categories this week; the closest, start PJ Washington for John Collins, costs 0.010." EVIDENCE: `swap_grid` [], `swap_keep` PJ Washington for John Collins, −0.01 |
| Page | SEASON DECK: PASS, 7 tabs, 0 page errors; no sideways scroll at 390 px or 1200 px |
| Tests | SwapGrid 3 of 3 pass; on the card before this change, 1 failure and 1 error |
| Full suite and gates | below, from gates.py |

## 3. Bounds

Out of scope by design: the valuation itself (the replacement table of `week_matchup.py`) is unchanged; the Out-today card is unchanged; free agents are not "plug and play" candidates here (the Week card's "Best adds this week" carries them); the brief's text has no start/sit section.

In scope and unverified:
- A day on which swaps help, on real records: NOT-ATTEMPTED (the morning of 2026-11-18 had none); covered by the fixture test's text.
- The figures are the 5 AM model's; the 3 PM page refreshes who plays and who is Out, as before.

## 4. Decisions for the owner

1. This pull request: merge (the page changes from the Runner's next build) or keep it as a draft.

## 5. Provenance

Session of 2026-11-18 (session model B), the Main session; branch `claude/start-sit-card`. Re-verify: `python3 -m unittest scripts.test_season_deck.SwapGrid`; build the page from season/daily 2a61d547 with this branch's `scripts/season_deck.py` and read the Today tab.
