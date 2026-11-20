# The morning deck build names a rostered player with no board row (2026-11-20)

Pull window: 2026-11-20 → 2026-11-20 (no pull: kit main 4fe235c, deck main 3551a15, the records branch season/daily at c318ebd2, read only; the deck page rebuilt in a throwaway worktree).

**Owner's request, verbatim (2026-11-20).** Card pick "Build anyway, name him (Recommended)", after the session reported that this morning's run failed at the season deck step: "SEASON DECK: FAIL — 2026-11-20: rostered player(s) with no season-board or held row: ['Landry Shamet']".

**Method up front.** Stated to the owner before the change: one change in `scripts/season_deck.py`, tests first; the morning build does what the 3 PM rebuild has done since 2026-10-28 (owner, "Rebuild, flag morning parts"): it carries the player as off the board and names him. Checked on this morning's records, where the step failed. Narrowed during the build and told to the owner: the morning carries only a player the league intake matched to a pool row (`pool_team` in the league state, as Shamet has); a rostered name with no pool row still halts the morning, because that halt is the 2026-10-19 guard against a mis-joined name showing a rostered player as a free agent (an older test, `test_unresolvable_rostered_name_halts`, failed on the first version of this change and now passes unchanged).

**Verdict. On the 2026-11-20 morning records the deck step fails before the change and passes after it; the page names Landry Shamet and nothing else on it changes.**

Runner impact: code-only (the morning SEASON DECK step passes where it halted; its PASS line ends "; rostered with no board row: <names>" when there are any; the deck record's `join.not_on_board` is now always present). No prompt or step changes.

Pool rows touched: none

## 1. What happened

ANONG NANGIANNIS?! added Landry Shamet between the 11-19 afternoon and the 11-20 morning records. He has a row in the deck pool (`data/season/pool_season.csv`) and none on the kit's board (`report/season/board_2026-11-20.json`: 315 rows, 12 held, his name in neither), because the kit's projections list has no line for him. The morning build raised on that by design (a test said so: "the morning build still halts on it"); the afternoon build has carried such a player since 2026-10-28. Every other morning step passed (24 steps, the brief, the week card, the title share); the page was not built or published, so the owner's page stayed on the 11-19 afternoon version.

## 2. On this morning's records

| build of 2026-11-20 (morning) | result |
|---|---|
| before the change (season/daily c318ebd2 as run) | SEASON DECK: FAIL, the same line the Runner recorded |
| after the change | SEASON DECK: PASS, 7 panes, 315 board rows, 36 status rows, 7 tabs, 0 page errors; "rostered with no board row: Landry Shamet" |

EVIDENCE: both builds run in a worktree at c318ebd2. The Today tab carries one new note: "Rostered with no row on the board (no season line on this page): Landry Shamet, on ANONG NANGIANNIS?! (Kyle)." The record's join reads rostered 172, on the board 169, off the board 3, `not_on_board` ["Landry Shamet"]. He is not on the Board tab (no line to rank), and the simulator's treatment of him is unchanged (it plays the deck pool's row, as this morning's brief did).

## 3. Checks

`scripts/test_season_deck.py`, class `AfternoonRefresh`: the test that required the halt was rewritten first to require the name, with one added for a morning with everyone on the board and one for a name with no pool row (still a halt). On the code before the change: 2 errors; after: all pass. The first version of the change failed one older test in the full suite (1,329 tests, 1 failure); the narrowed version is the one gated below. The full suite and gates: below, from gates.py.

## 4. Bounds

Out of scope by design: no projection line was added for Shamet (the owner's other option, not picked); the afternoon note's wording ("Added since the 5 AM board") is unchanged.

In scope and unverified: the Runner's own next morning run on this code (2026-11-21); did not re-run today's morning from this session (the Runner owns the records branch).

## 5. Provenance

Session of 2026-11-20 (session model C, continuing the Main session; branch `claude/deck-morning-off-board`). Re-verify: `python3 -m unittest scripts.test_season_deck.AfternoonRefresh`.
