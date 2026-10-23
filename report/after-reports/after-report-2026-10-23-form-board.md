# Minutes & role board: the signal that stabilizes first, on the Movers tab — 2026-10-23

Window: the kit at `main` `16b1059` plus this branch; the 10/23 morning records on `season/daily` (box scores 10/20–10/22, league state, the Flaim pull); the deck at `048efb6`. No projection line, tag, roster, engine constant or ledger row changed.

Pull window: 2026-10-23 → 2026-10-23. No pull: the record is built from the box scores and the pull already on disk.

**Owner's ask (2026-10-23).** "Perform a self-critical analysis and audit, see where we can make meaningful strides in building competitive and winning potential … What can we do today, and let's do it." The audit (in session) named five weaknesses; the owner picked the first build: the minutes & role board. Then: "add a time stamp at the top right of when the tool was last updated" and "a lot of words and data … make more concise and precise, as with the Draft Deck".

**Method (stated to the owner before the build).**
- Window: every regular-season box score on disk (`season_type == 2`, DNPs excluded — `season_lines.totals`' rules, kept per game). Today that is 10/20–10/22: every NBA team has played once, so every row is a one-game row and says so. The trend (last 3 games' minutes against the games before them, ±6 min) draws only from 4 games on; nothing downstream reads it.
- Rates per 36 minutes on the minutes actually played; role from the box score's starter flag (S started every game / B none / M some, with starts/games).
- Scope: the 12 rosters (league state) plus Yahoo's available list from the pull, Yahoo spellings resolved against the season pool CSV and the box-score names (`league_intake.resolve`); a name in neither is listed, never guessed.
- Not a projection: the season line stays the per-game line the board and the simulator run on. The pool CSV carries no minutes, so there is no preseason minutes expectation; the trend is within-season only.

## 1. What was built (EVIDENCE)

- `scripts/form_board.py`: `game_log`, `summarize`, `build`, CLI (`--date --actuals --state --pull --pool --out-dir --ledger`), record `report/form/form_<date>.json` (+ `.csv`), prints `FORM BOARD: PASS — …`; a standalone run records a run-ledger row (D5), the morning run's child does not.
- `scripts/season_deck.py`: `default_paths` gains `form`; the Movers tab leads with the "Minutes & role" card — view select (all / my roster / free agents), every column sortable, my rows marked, "How to read it" folded under the table; the Free Agents list shows each free agent's `min/g (g, starts|bench)`; the header carries "Updated <build time>" top right in the viewer's own clock (the morning run's `generated_utc`).
- `scripts/morning.py`: step "form board" after "league table", non-fatal.
- Red first, then green: `test_form_board.py` (9: regular season only, per-36 by hand, trend null under 4 games and signed at 4, role flags, owner/slot/mine, Yahoo spelling resolved, a no-game free agent as a 0-game row, totals equal `season_lines.totals` on the same files, CLI), `test_season_deck.py` `FormCard` (4: absent record builds, order and marking, header sorts and view filter, the free-agent minutes note and the stamp), `test_morning.py` step list. Two of my own expectations were wrong and corrected, not the code: a "down" fixture that was −5.7 (inside the ±6 band) and a stamp assertion that assumed the fixture date.
- Replay on the 10/23 records (`form-board-2026-10-23/form_2026-10-23.json`): 168 rostered + 100 free agents (all of Yahoo's list resolved), 238 with a game over 3 box days, 30 without one yet (17 of them on Yahoo's list: Porter Jr., Harris, Nesmith, Sexton, Stewart, Sharpe, Lively, Strus, DiVincenzo, Cardwell, Huff, Monk, Moody, McConnell, Kennard, Westbrook, Riley — every NBA team has played once, so these are inactives), 77 played-not-in-pool. Hand check: Jarrett Allen's 10/22 box 28 min, 14 pts, 7 reb, 2 blk → per-36 18.0 / 9.0 / 2.571, as the record says. My roster's minutes: Durant 37, White 36, Haliburton 34, Braun 33, Jerome 32, Washington 31, McDaniels 29, Bridges 29, Lendeborg 29, Leonard 24, Irving 24, Queta 22 (bench), Ware 14 (bench), Black 0 (IL) — one game each.
- The adversarial pass caught my first replay: it resolved Yahoo names against box-score names only, so 17 injured free agents read "unresolved" and ten players whose box spelling differs from the pool's (Jabari Smith Jr., Michael Porter Jr., Jaren Jackson Jr., Jaime Jaquez Jr., Wendell Carter Jr., Darius Acuff Jr., Mikel Brown Jr., Cameron Johnson, Kelly Oubre Jr., Herbert Jones) had no games. The record now resolves against the pool CSV first and looks the box log up by the folded name (`box_name` on each row); a red test covers the Oubre case.
- Renders: `form-board-2026-10-23/minutes-mine.png`, `minutes-fa.png`, `minutes-phone.png` (400 px, no horizontal page scroll), `header.png` (the stamp). `deck_render_check` PASS; full suite bar the two pre-existing transcript failures; `report/run-ledger.jsonl` unchanged across the suite (817 lines).
- Roster changes: none (no pool row, tag, line or roster touched).

## 2. Bounds

- **In scope and thin by the data:** one game per player today; the board shows the games count on every row and no trend until 4 games. The 10/23 games reach it with tomorrow's pull.
- **Out of scope by design:** a minutes-based projection or a change to the blend; a preseason minutes baseline (none in the pool); the four other audit items (title odds from real standings and pairings, the P(win) scoring loop, transactions/standings pinning, the opponent model) — owner decisions, listed in session.
- **Flagged, not fixed (scope-fence):** the owner's "a lot of words" reads naturally against the whole page (the week card's red reconciliation line, the long notes); this build tightened the new card and the header only. Tightening the rest is a separate decision.
- **Flagged, not fixed (scope-fence) — a defect in the existing pipeline, found by this build:** the box puller leaves pool players unpooled under another spelling (Kelly Oubre / Herb Jones / Cam Johnson / Darius Acuff / Mikel Brown, and five same-spelling names it still misses: Buddy Hield, Jaden Hardy, Jordan Clarkson, Landry Shamet, Trayce Jackson-Davis), so `season_lines` blends none of their games: 81 "unpooled with games" in today's `season_lines_2026-10-23.json`. This card reads through the gap; the blend, the season board and the week card's box-score rebuild do not. A `box_pull.match_name` alias fix is a separate decision.
- **Assumption A1:** the box score's starter flag is reliable (not checked against a second source).

**Bands.** This change computes no figure; the standing sweep's bands (`redteam-2026-10-19/sweep.json`, engine 048efb6) are unchanged:
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

## Watchlist

- **From 4 games on (≈10/28):** the first ▲/▼ trends; a flag on a rostered player is the cue for the owner's "pivot after ~3 games" check, read with the games count.
- **Unpooled with games (78 today):** deep-bench names outside the pool; if one becomes a Yahoo pickup candidate, the pool is what needs the row, not this card.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| minutes & role board (owner, 2026-10-23) | **BUILT** on this draft PR | §1 |
| last-updated stamp, top right | **BUILT** | §1, `header.png` |
| the rest of the page's wording | **OPEN**, flagged | §2 |
| box puller's unpooled pool players (season_lines blends none of their games) | **OPEN**, flagged | §2 |
| audit items 1, 3, 4 (title odds, scoring loop, league activity record) | **OPEN**, owner decisions | §2 |
| `test_matchup_live` and `test_league_live` transcript dependence | **OPEN**, flagged (PR #172) | — |

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck 048efb6 and at 483482b, checked today, the same page the 10/22 day report replayed. Its table stands, carried here verbatim from the day report.

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
