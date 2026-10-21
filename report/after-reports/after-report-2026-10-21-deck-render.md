# Season Deck: the Movers crash fixed, and a render check before any page is written — 2026-10-21

Pull window: 2026-10-21 → 2026-10-21 (build only; no roster pull, no box scores, no projection line or tag changed).

**Owner's request.** "Build fixes, A and B", 2026-10-21. A and B are decision 2 of `after-report-2026-10-21-board-test.md`:
- (a) fix the Movers rows;
- (b) add a render check to the deck build.

"Build" means build. Merging stays the owner's word.

**What was analyzed.**
- Kit `main` `e318657` (after #150 and #153), branch `claude/market-data-workorder-mnfi2b`.
- The live Season Deck page, version `1792587540-e153` (broken).
- The committed 10/20 build `report/season/deck_2026-10-20.html` (good).
- Today's real records on `main` for 2026-10-21.

**Method.** The choices below were stated to the owner before the build:
- **The render check's pass rule:** no uncaught script error, on load or on clicking any tab; exactly the six tabs in order; every pane present with content; each tab showing its own pane.
  - The page is opened offline, with every web request blocked, so a blocked font is not an error.
- **It fails closed:** if no browser can start, the deck step fails and no page is written.
- **Movers show stats as recorded,** for example "PTS 25.6 → 24.5" and "FG% 0.503 → 0.491".

**Headline.**
- **Today's real 10/21 records now build a page that draws itself:** 6 tabs, 0 page errors, every pane drawn. The Movers rows read "Victor Wembanyama · PTS 25.6 → 24.5 · FG% 0.503 → 0.491".
- **A page that cannot draw itself is no longer written under its published name.** It is kept as `deck_<date>.failed.html` and the deck step FAILs, so the morning run has nothing broken to publish.
- **This reaches the runner only once this PR merges,** before 2026-10-22 12:53Z for tomorrow's run.

---

## 1. Merges

No roster moved and no projection line or tag changed. Nothing was merged: this PR is open for the owner's word.

## 2. Fix A: the Movers rows

**The cause** (from the board-test report §3, EVIDENCE). `season_lines.py` records each moved stat as `[preseason, season]` strings under its kit column. The page formatted that pair as one signed number (`zv(v, true)` → `x.toFixed`) and threw. The tab bar is drawn after the Movers pane, so it never appeared.

**The fix** (`scripts/season_deck.py`, the page's Movers code):
- Each moved stat now prints as its category name, then preseason → season (`fgp` → "FG%", `fga` → "FGA", and so on).
- The pane's header said "±0.25 z". It now states the real threshold: a per-game line moved 0.25 or more, or FG%/FT% 0.01 or more (`season_lines.py` line 140).
- The data stays embedded as recorded, so the page still draws every figure from the record.

**Red-first** (EVIDENCE). `test_the_page_draws_itself_with_real_movers` builds its movers by running `season_lines.run` on three big games for a fixture player, so the record has the producer's real shape.
- **Before the fix:** FAIL with `page error: x.toFixed is not a function; tabs []; pane-movers empty; pane-week empty`. That is the production failure exactly.
- **After the fix:** PASS. The pane reads "PTS … → …", "FG% … → …", "REB", "AST" and "TOV" from the record.

**Today's real records** (EVIDENCE, `season_deck.py --date 2026-10-21 --out <scratch>` on `main` `e318657`). It printed `SEASON DECK: PASS — 2026-10-21: … (6 panes, 313 board rows, 16 status rows; record … pins 8 inputs; render: 6 tabs, 0 page errors)`.
- The Movers pane lists the 10/21 movers.
- The Week pane also draws on real game data. The board-test report had left that untested.

## 3. Fix B: the render check

**The checker** (`scripts/deck_render_check.py`). It opens a page in headless Chromium and reports:
- the tab labels;
- every uncaught page error, on load and on clicking each tab;
- each pane's text;
- which pane each tab shows.

A page that cannot be opened or driven FAILs with "render error". When no browser starts, the result is UNAVAILABLE, which counts as a failure.

**Proven on known answers before use** (EVIDENCE):

| page | expected | result |
|---|---|---|
| live page `1792587540-e153` | FAIL | FAIL: `x.toFixed is not a function`; tabs []; pane-movers empty; pane-week empty |
| `deck_2026-10-20.html` | PASS | PASS: 6 tabs, 0 page errors, every pane drawn |
| synthetic page that draws itself | PASS | PASS |
| script error before the tab bar | FAIL | FAIL |
| five tabs | FAIL | FAIL |
| an empty pane | FAIL | FAIL |
| a tab showing the wrong pane | FAIL | FAIL |
| an error on clicking a tab | FAIL | FAIL |
| a page that cannot be opened | FAIL | FAIL ("render error") |
| empty browser folder | UNAVAILABLE | UNAVAILABLE |

**The browser it uses.** The installed Playwright for Python (1.64) asks for browser build 1248, but `/opt/pw-browsers` holds build 1194. The checker therefore names the installed builds itself: `DECK_CHROMIUM` first, then Playwright's default, then the installed builds, newest first. Here it runs Chromium 141.0.7390.37 headless, in about 1 second.

**Wired into the deck build** (`season_deck.py` `main()`):
- The page is written to `deck_<date>.check.html` and checked.
- Only on PASS is it renamed `deck_<date>.html`, and the record gains a `render` entry.
- On FAIL or UNAVAILABLE it is renamed `deck_<date>.failed.html`, the step prints `SEASON DECK: FAIL — … render …` and exits 1.
- `morning.py` treats the deck step as fatal, so the run reports it and has no page to publish.

**Red-first** (EVIDENCE):
- `test_a_page_that_cannot_draw_itself_is_never_written_as_the_deck` failed before the wiring ("SystemExit not raised": the broken page was written). It passes after.
- `test_a_page_that_draws_itself_is_written_and_its_render_recorded` failed before (no `render` in the record) and passes after.

**Kit suite:** 250/250, twice (238 before, plus 12 new).

**Bands, unchanged:** sweep on `80eecdf`, `redteam-2026-10-19/sweep.json`.
- **TEAM_WEEK_SHOCK is FRAGILE:** +2.7 (no shock) / −3.6 (shock doubled).
- **weekly_availability is FRAGILE:** −2.7 (no in-sim injury discount) / +0.5 (harsher risk tier 0.65) / −1.5 (healthy plays 0.95) / +1.0 (healthy plays 0.80).
- This report quotes no title share.

## Watchlist

- **The live page stays the broken 10/21 build** until a fixed page is published (decision 2).
- **The first daily cron fire into the runner is 2026-10-22 12:53Z;** a check-in is armed for 13:10Z. It renders the published page and reports its tabs and errors.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| Movers crash (board-test decision 2, option a) | **BUILT**, this PR; not merged | red-first on the producer's real movers shape; today's 10/21 records render 6 tabs, 0 errors |
| render check before a page is written (option b) | **BUILT**, this PR; not merged | known answers 10 of 10; publish-gate tests red then green; 250/250 twice |
| kit #150, #153 | **MERGED** | `e318657`, `eee277d` |
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

1. **Merge this PR** before 2026-10-22 12:53Z, so tomorrow's 05:53 PT run builds with both fixes. Merging is your word.
2. **The live page is still the broken 10/21 build** until a fixed page is published. Options:
   - **(a)** publish today's fixed build now. It is built from `main`'s 10/21 records and renders 6 tabs with 0 errors.
   - **(b)** wait for tomorrow's run.
3. **Option (c) from the board-test report,** drawing the tab bar first so one pane cannot hide the others, is not built. It is not needed for B: B already refuses any page with fewer than six working tabs.
4. Carried, still open:
   - the 7 risk rows (GAUNTLET decision 2);
   - the calibration check date (decision 3);
   - the evening status routine (decision 5);
   - deleting the old routine (decision 6).

## Bounds

**Out of scope by design.**
- Option (c).
- The draft-room deck (the deck repo), which this check does not touch.
- Any projection line, tag, roster or engine constant.

**In scope and unverified.**
- **The render check inside the runner's own container:** NOT-ATTEMPTED. It cannot run there before this PR merges.
  - The runner was created from this session's environment, which has the browser and `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`.
  - If its container lacks them, the deck step fails with "render UNAVAILABLE" and publishes nothing. The 13:10Z check-in reports which happened.

## Provenance

- **Session:** Claude Code (cloud), 2026-10-21, about 16:30Z–17:30Z.
- **Governors:** plan-gate, loaded for this request with its block shown before the first write; adversarial-verify, before delivery.
- **Re-verify:**
  - `SEASON_POOL=1 python3 -m unittest discover -s scripts -p 'test_*.py'` (expect 250 OK);
  - `python3 scripts/deck_render_check.py report/season/deck_2026-10-20.html` (expect PASS);
  - `python3 scripts/season_deck.py --date 2026-10-21 --out /tmp/deck` (expect `SEASON DECK: PASS … render: 6 tabs, 0 page errors`).
