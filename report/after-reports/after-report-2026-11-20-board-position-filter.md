# The Board tab filters by position (2026-11-20)

Pull window: 2026-11-20 → 2026-11-20 (no pull: kit main 2ab5346, then 2f77312 for the same-day change of section 2, deck main 3551a15, the records branch season/daily at b0d0e9b0, read only; the deck page rebuilt in a throwaway worktree).

**Owner's request, verbatim (2026-11-20).** "On the "Board" tab, can you please give me the option to also filter by POSITION? Similar to on the Draft deck tool PG, SG, G, SF, PF, F, C". Told first that this is a new feature under his standing pick of 2026-11-18 ("Fixes only until wk 8"), he chose on a card: "Build it, display-only (Recommended)".

**Method up front.** Stated to the owner before the build: display only, in `scripts/season_deck.py`; eligibility is the pos column the Board already shows (Yahoo's); G is PG or SG and F is SF or PF, the league's slots (`hoops.POSITIONAL_SLOTS`); one position at a time, "All" by default; it combines with the search box, "free agents only" and the category switches; the # and z adj columns keep their overall values.

**Verdict. The Board has a position dropdown with the Draft deck's list (All, PG, SG, G, SF, PF, F, G/F, F/C, C). On the 2026-11-19 afternoon records each choice shows exactly the players eligible there, and no figure on the page changes.** It was first built as a row of eight buttons (kit #296, merged on the owner's card click) and changed to the dropdown the same day on his request (section 2).

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

## 2. Same-day change: a dropdown, as on the Draft deck

**Owner, 2026-11-20, after #296 merged:** "Looks great Claude, but sorry to ask- can you make it a drop down select, like the Draft deck tool?", with a picture of the Draft deck's list. Stated before the change: the list is matched to the Draft deck's exactly (deck `docs/draft-deck.html`, `#bestPos`), which adds two choices his first request did not name. G/F is a player eligible at a guard spot and a forward spot; F/C at a forward spot and center (the Draft deck's rule for both).

| choice | players shown | players eligible by the pos column | rows at a wrong position |
|---|---|---|---|
| PG, SG, G, SF, PF, F, C | 89, 129, 158, 121, 114, 173, 90 | the same | 0 |
| G/F | 68 | 68 | 0 |
| F/C | 38 | 38 | 0 |

EVIDENCE: the 2026-11-19 afternoon page rebuilt with the change (SEASON DECK PASS, 0 page errors), each choice selected in a browser and compared with a count from the page's own board data; no overflow at phone width.

- "All" or Reset returns to every position.
- The line under the row says how many of the ranked players are eligible ("68 of 315 players are eligible at G/F (a guard spot and a forward spot)").
- The table still shows at most 200 rows at a time, as before.

## 3. Checks

`scripts/test_season_deck.py`, class `BoardPositionFilter`: five tests written first for the buttons (1 failure and 4 errors before, all pass after). For the dropdown the class was rewritten first, now six tests: on the button version 1 failure and 5 errors; after: all pass. The full suite and gates: below, from gates.py.

## 4. Bounds

Out of scope by design: no projection, rank, simulation or record changes; the other tabs are untouched.

In scope and unverified: the published page. The Runner's next run builds and publishes it after the merge; did not publish it from this session (the deck page is published only by the Runner or on the owner's word).

## 5. Provenance

Session of 2026-11-20 (session model C, continuing the Main session; branches `claude/board-position-filter` and `claude/board-position-select`). Re-verify: `python3 -m unittest scripts.test_season_deck.BoardPositionFilter`.
