# The Board tab filters by position (2026-11-20)

Pull window: 2026-11-20 → 2026-11-20 (no pull: kit main 2ab5346, deck main 3551a15, the records branch season/daily at b0d0e9b0, read only; the deck page rebuilt in a throwaway worktree).

**Owner's request, verbatim (2026-11-20).** "On the "Board" tab, can you please give me the option to also filter by POSITION? Similar to on the Draft deck tool PG, SG, G, SF, PF, F, C". Told first that this is a new feature under his standing pick of 2026-11-18 ("Fixes only until wk 8"), he chose on a card: "Build it, display-only (Recommended)".

**Method up front.** Stated to the owner before the build: display only, in `scripts/season_deck.py`; eligibility is the pos column the Board already shows (Yahoo's); G is PG or SG and F is SF or PF, the league's slots (`hoops.POSITIONAL_SLOTS`); one position at a time, "All" by default; it combines with the search box, "free agents only" and the category switches; the # and z adj columns keep their overall values.

**Verdict. The Board has a row of eight buttons (All, PG, SG, G, SF, PF, F, C). On the 2026-11-19 afternoon records each one shows exactly the players eligible there, and no figure on the page changes.**

Runner impact: code-only (the built page gains the button row; no step, record, prompt or pass line changes).

Pool rows touched: none

## 1. On the 2026-11-19 afternoon records

| button | players shown | players eligible by the pos column | rows at a wrong position |
|---|---|---|---|
| PG | 89 | 89 | 0 |
| SG | 129 | 129 | 0 |
| G (PG or SG) | 158 | 158 | 0 |
| SF | 121 | 121 | 0 |
| PF | 114 | 114 | 0 |
| F (SF or PF) | 173 | 173 | 0 |
| C | 90 | 90 | 0 |

EVIDENCE: `scripts/season_deck.py --date 2026-11-19 --phase pm` on season/daily b0d0e9b0 with this branch's `season_deck.py`: SEASON DECK PASS, 7 tabs, 0 page errors, 315 board rows. A browser run clicked each button and compared the rows shown with a count made from the page's own board data; no page error; no sideways overflow at phone width (390 px). With G on, the first rows keep their overall ranks (3, 4, 5, 6, 7, 8, 10).

## 2. Behaviour

- A second click on the active button, "All", or Reset returns to every position.
- The line beside the buttons says how many of the ranked players are eligible ("158 of 315 players are eligible at G (PG or SG)").
- The table still shows at most 200 rows at a time, as before.

## 3. Checks

`scripts/test_season_deck.py`, class `BoardPositionFilter`: five tests written first. On the code before the change: 1 failure and 4 errors; after: all pass. The full suite and gates: below, from gates.py.

## 4. Bounds

Out of scope by design: no projection, rank, simulation or record changes; the other tabs are untouched.

In scope and unverified: the published page. The Runner's next run builds and publishes it after the merge; did not publish it from this session (the deck page is published only by the Runner or on the owner's word).

## 5. Provenance

Session of 2026-11-20 (session model C, continuing the Main session; branch `claude/board-position-filter`). Re-verify: `python3 -m unittest scripts.test_season_deck.BoardPositionFilter`.
