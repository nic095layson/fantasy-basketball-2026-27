# The board test that read live data, fixed; #150 merged; why the Season Deck lost its tabs — 2026-10-21

Pull window: 2026-10-21 → 2026-10-21 (build and diagnosis only; no roster pull, no box scores, no projection line or tag changed).

**Owner's request.** "Merge. Why did the Season Deck lose a lot of it's tabs and funcionality?", 2026-10-21. "Merge" is PR #150, the only PR waiting on the owner's word. Merging it would have turned one kit test red, so the owner was asked and chose "Fix test, then merge" (2026-10-21). The deck question is answered as an assessment: nothing in the deck was changed.

**What was analyzed.**
- Kit `main` `d5c5d0d` (after #152), branch `claude/market-data-workorder-mnfi2b`.
- The runner's 10/21 records, `season/daily` `8ba6534` (PR #150).
- The live Season Deck page, artifact version `1792587540-e153` (published 2026-10-21 12:59:00Z), and the committed 10/20 build `report/season/deck_2026-10-20.html`.
- Deck repo unchanged.

**Method.**
- Both deck pages were rendered in headless Chromium (Playwright, fonts blocked), recording the tab buttons, each pane's text length and every page error with its stack.
- The test fix is red-first: the old test fails on the 10/21 records, the new one passes on both trees, and a mutant that breaks the zero-games identity is caught.

**Headline.**
- **The Season Deck lost its tabs because the page's script crashes in the Movers tab.** The crash happens before the tab bar is drawn, so only the Today pane shows. 10/21 was the first morning with real season-line movers, and the Movers code had never run on real movers before.
- **Every in-season morning will crash the same way until the Movers code is fixed.** Tomorrow's runner build will publish a page with the same fault. A fix is proposed below and not built.
- **The board test now checks what it was written for**, without reading live data. #150 merges after this PR.

---

## 1. Merges

No roster moved and no projection line or tag changed.

| PR | state | commit | note |
|---|---|---|---|
| kit #152 (deck missing-input fix) | **MERGED** | `d5c5d0d` | merge commit; main's tree equals its head `9031c39` (checked) |
| kit (this PR, board test) | open | — | merges on the owner's word ("Fix test, then merge") |
| kit #150 (daily records 10/21) | merges after this PR | — | GitHub refused it as conflicted (405); see §2 |

## 2. PR #150 and the board test

**Why GitHub refused #150** (EVIDENCE, `merge_pull_request` 2026-10-21: "405 Pull Request has merge conflicts"). Both sides appended rows to `report/run-ledger.jsonl`. The repository sets `merge=union` for that file (`.gitattributes`), and GitHub's merge check does not apply it. In git the merge is clean.
- The ledger after the merge has 43 rows: `main`'s 38 and the runner's 5. Every row from both sides is present, none duplicated, none from neither side (checked by sorting and comparing).
- My plan predicted 35 rows. That figure used `main`'s count before #152, which added 8; corrected here.

**The test that went red** (EVIDENCE, two runs on the merged tree: `FAILED (failures=1)`). `test_identity_board_matches_the_preseason_order` built the board from the committed `data/season/projections_season.csv` and asserted it equals the preseason board.
- That held only while no regular-season game had been played. The 10/21 records carry the first real season lines: Wembanyama's points and FG% moved down, so Shai Gilgeous-Alexander is #2 and the assertion fails.
- The data is right and the test was wrong: it would fail on every in-season record.

**The fix** (`scripts/test_season_board.py`). The test now builds zero-game season lines in a temporary folder with `season_lines.run(actuals=[])` and asserts that board equals the preseason board. That is the property the test was written for, and it no longer depends on the day's data.

**Red-first and the mutation check** (EVIDENCE):
- Old test on the merged #150 tree: FAILED.
- New test on `main` and on the merged #150 tree: OK on both.
- A mutant that changes one zero-game line (Wembanyama's points) is caught: 1 failure, 0 errors, on the board assertion.
- Kit suite on the branch: 238/238, twice.

## 3. Why the Season Deck lost its tabs

**What the live page does** (EVIDENCE, Chromium render of version `1792587540-e153`):
- Tab buttons drawn: none.
- Page error: `TypeError: x.toFixed is not a function`, at `sgn` ← `zv` ← the Movers renderer.
- Panes: Today, Trade, Free Agents and Board hold their content but have no tab to reach them; Movers and Week are empty.

**The 10/20 page, same check** (EVIDENCE): six tabs (Today, Trade Analyzer, Free Agents, Board, Movers, Week) and no page error.

**The cause** (EVIDENCE, the code on `main`):
- `scripts/season_lines.py` line 139 records each mover's change as the old and new stat text: `moved = {c: (r[c], b[c]) ...}`, for example `"pts": ["25.6", "24.5"]`.
- The deck's Movers code formats each value as a signed number: `zv(v, true)` → `x.toFixed(...)`. A pair of strings has no `toFixed`, so the script throws.
- The tab bar is built after the Movers pane (page line 346, Movers at 306), so the throw also stops the tab bar and the Week pane.

**Why it first broke on 10/21** (EVIDENCE):
- The 10/20 build had 0 movers and 0 players with games, so the Movers rows were never drawn.
- 10/21 is the first build with real games: 56 players with games, and movers.
- The deck tests only ever build with `movers=[]` (`test_season_deck.py` line 42), so the movers path was never exercised.

**Who published it** (EVIDENCE, `get_trigger`): the old morning routine's last scheduled run, 2026-10-21 12:54:22Z to 12:59:36Z, session `cse_011gyxrUQHo8CPYDhPE3oYEq`. The page's data says generated 12:58:50Z; the version is stamped 12:59:00Z. That routine has since been disabled.

**Why no check caught it.** The publish step's "six tabs" check reads the page's text (INFERENCE: the six pane ids are all in the HTML, so a text check passes). The tabs are drawn by the script at runtime, so only a render shows them missing. `SEASON DECK: PASS` means the HTML was written, not that it runs.

**What happens next** (INFERENCE from the above): from now on every morning has movers. Tomorrow's runner run (05:53 PT) can build the deck since #152, and will publish a page with the same crash unless the Movers code is fixed first.

**Bands, unchanged:** sweep on `80eecdf`, `redteam-2026-10-19/sweep.json`.
- **TEAM_WEEK_SHOCK is FRAGILE:** +2.7 (no shock) / −3.6 (shock doubled).
- **weekly_availability is FRAGILE:** −2.7 (no in-sim injury discount) / +0.5 (harsher risk tier 0.65) / −1.5 (healthy plays 0.95) / +1.0 (healthy plays 0.80).
- This report quotes no title share.

## Watchlist

- **The live page stays tab-less** until a fixed deck is published.
- **The first daily cron fire into the runner is 2026-10-22 12:53Z.** A check-in is armed for 13:10Z.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| kit #152 | **MERGED** | `d5c5d0d` |
| board test reading live data | **BUILT**, this PR | red on #150's tree, green on both; mutant caught; 238/238 twice |
| kit #150 | open, merges after this PR | GitHub 405 (union-merged ledger) |
| Season Deck Movers crash | **open, the owner's** | §3; fix not built |
| 7 risk rows, calibration date, evening routine, old routine | open, the owner's | GAUNTLET report decisions 2, 3, 5, 6 |

The flagged-name receipts are carried forward from the lock report. This build pulled nothing and researched no player, so they were not re-queried (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this build (did not check) |

## Repeat-name market check

This build did not change the deck page, which is still deck `80eecdf`, page sha256 6a5cefea4921. The GAUNTLET report replayed it today. Its table stands, carried here verbatim.

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 6a5cefea4921), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 33 of 33 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 32 of 33 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 23 of 33 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 14 of 33 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 33 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| John Collins | 11 of 33 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 10 of 33 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 10 of 33 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 9 of 33 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 7 of 33 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 7 of 33 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 33 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 33 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (17 mocks, value 27, market 45); Lauri Markkanen (15 mocks, value 21, market 37); Tyrese Haliburton (13 mocks, value 7, market 12); Tyrese Maxey (11 mocks, value 5, market 9); Kel'el Ware (10 mocks, value 57, market 77); Tyler Herro (9 mocks, value 51, market 69); Karl-Anthony Towns (8 mocks, value 12, market 15); Miles Bridges (5 mocks, value 96, market 98).

## Decision sheet

1. **Merge this PR**, then #150. Both are your word, given as "Fix test, then merge".
2. **The Season Deck Movers crash.** Not built; your call. Options:
   - **(a) Fix the Movers rows (recommended, with b).** Show each moved stat as old → new (for example "PTS 25.6 → 24.5") with the kit's category names, instead of formatting the pair as a number. Red-first test with a fixture in the real `season_lines` shape.
   - **(b) Add a render check to the deck build (recommended, with a).** Open the built page in headless Chromium and fail the step on any page error or fewer than six tab buttons, so a page that cannot draw itself is never published.
   - **(c) Isolate the panes.** Draw the tab bar first and wrap each pane, so one pane's failure leaves the others usable. Optional on top of a and b.
   - **(d) Stopgap:** republish the 10/20 page. Not recommended: its data is a day old and tomorrow's run would overwrite it with the broken build anyway.
   - Timing: to keep tomorrow's page whole, a fix must be merged before 2026-10-22 12:53Z.
3. Carried from the GAUNTLET report, still open: the 7 risk rows (decision 2), the calibration check date (decision 3), the evening status routine (decision 5), deleting the old routine (decision 6).

## Bounds

**Out of scope by design.**
- Any change to the deck page or its builder: the deck question was a question, answered as an assessment.
- Any projection line, tag, roster or engine constant.

**In scope and unverified.**
- **How the old routine checked "six tabs" before publishing:** NOT-ATTEMPTED (its session transcript was not read). The inference in §3 rests on the page text containing all six pane ids.
- **Whether other panes have the same kind of fault on in-season data:** the render shows Today, Trade, Free Agents and Board drawn before the throw. The Week pane never ran on 10/21 data, so it is untested on real games (NOT-ATTEMPTED).

## Provenance

- **Session:** Claude Code (cloud), 2026-10-21, about 16:10Z–17:10Z.
- **Governors:** plan-gate, loaded for this request with its block shown before the merge; adversarial-verify, before delivery.
- **Re-verify:**
  - `SEASON_POOL=1 python3 -m unittest discover -s scripts -p 'test_*.py'` (expect 238 OK);
  - render the live page (Artifact read of `Az6vPGzG6TLWrPjdAWL2pe`) in Chromium and list `#tabs button` (expect none until fixed) and page errors (expect `x.toFixed is not a function`).
