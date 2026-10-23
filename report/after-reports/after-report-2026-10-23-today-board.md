# The Today tab as a matchup board — 2026-10-23

Window: the kit at `main` `046ae2f` plus this branch; the records branch `season/daily` at `8fde7a2` for the replay (league state, status, box scores and the Flaim pull of 2026-10-23). No projection line, tag, roster, ledger row or engine constant changed; two scripts and their tests change, and the week card record gains a `board` block.

Pull window: 2026-10-23 → 2026-10-23. No pull: the board is drawn from records the morning run already writes (the Yahoo pull through Flaim, the ESPN and Basketball-Reference box scores, the league state, the status file, the schedule file).

**Owner's request (2026-10-23).** "Can you please take this inspiration [Yahoo's matchup page] to build into our tool? Let's make this the today page, which should update with each morning refresh. Same data being pulled, just build differently visually." The owner's screenshot: a team header with the category score, a category totals row per team with the leader shaded, and both rosters side by side by slot, each player with his week to date and today's game.

**Method (stated before the build).** M1: each player's week line is the sum of his box scores on the days he sat in an active slot, the week card's existing rebuild rule (a day with a pinned Yahoo lineup counts its active slots; any earlier day falls back to today's roster). M2: the totals row stays Yahoo's own figure where the pull carries the matchup; where the rebuilt rows do not add up to it the board says so stat by stat. M3: today's game reads "vs OPP" or "@ OPP" with no tip-off time, since the schedule file carries dates only. A1: the rest of the Today tab (the lineup notice, "Worth a look", the week card's chances and pickups, the odds tiles) stays below the board. A2: the layout follows the screenshot; the look stays the deck's own (no logos, avatars or Yahoo styling).

## 1. What changed (EVIDENCE)

- `scripts/week_matchup.py`: `to_date()` keeps each counted player's own sum and games (`players`); `todays_games()` and `board_side()`; the record carries `board` = the score (categories each side leads to date), and per side the name, manager, rows in Yahoo's slot order (slot, player, NBA team, positions, status letter, today's game, week line, games counted), `departed` (counted this week, no longer rostered), `totals` and `rows_match_totals`.
- `scripts/season_deck.py`: `matchupBoard()` draws the card first on the Today tab from that block: header, category row with the leader cell shaded (`td.lead`), the players table with the slot column in the middle, the TOTAL row, the difference note, the departed note. CSS tokens: one new color `--lead` in all three theme blocks.
- Tests, red first: `test_week_matchup.MatchupBoard` (5: KeyError `board` on the unchanged code, then 25 of 25 in the file's Record classes) and `test_season_deck.MatchupBoard` (7: 3 failures and 2 errors on the unchanged page, then 7 of 7 twice; the browser reads the rendered card, including a 400-px viewport with no sideways page scroll).

## 2. The replay on the 10/23 records (EVIDENCE, `today-board-2026-10-23/`)

Score 3–6–0 on the categories led to date, the same 3–6 as the owner's Yahoo screenshot; the category row equals the week card record's `cats` (`me_to_date`, `opp_to_date`), which is Yahoo's scoreboard at the morning pull. My rows add up to Yahoo's totals (`rows_match_totals` true, 217 points); the opponent's rows add to 264 against Yahoo's 276, the same 8-stat difference the week card already reports (10/20 and 10/21 have no pinned opponent lineup and are read from today's roster; Gui Santos' 10/21 game was Yahoo-counted and he has since been dropped), and the board says so under the table.

| slot | my player | NBA | today | games | PTS | REB | AST |
|---|---|---|---|---|---|---|---|
| PG | Tyrese Haliburton | IND | vs DAL | 1 | 23 | 2 | 12 |
| SG | Christian Braun | DEN | no game | 1 | 7 | 6 | 1 |
| G | Kawhi Leonard | TOR | @ WAS | 1 | 23 | 6 | 2 |
| SF | Jaden McDaniels | MIN | @ ORL | 1 | 17 | 8 | 1 |
| PF | Miles Bridges | PHX | no game | 1 | 8 | 4 | 0 |
| F | Yaxel Lendeborg | GSW | vs MEM | 1 | 12 | 3 | 2 |
| C | Kel'el Ware | MIL | vs CHI | 1 | 7 | 3 | 1 |
| C | PJ Washington | DAL | @ IND | 1 | 10 | 4 | 2 |
| UTIL | Kyrie Irving | DAL | @ IND | 1 | 15 | 4 | 2 |
| UTIL | Ty Jerome | MEM | @ GSW | 1 | 45 | 7 | 6 |
| BN | Kevin Durant | HOU | @ SAS | 1 | 30 | 6 | 3 |
| BN | Neemias Queta | BOS | vs NYK | 1 | 3 | 4 | 2 |
| BN | Derrick White | BOS | vs NYK | 1 | 17 | 1 | 8 |
| IL | Anthony Black | ORL | vs MIN | 0 | – | – | – |

| slot | opponent | NBA | today | games | PTS | REB | AST |
|---|---|---|---|---|---|---|---|
| PG | Tyrese Maxey | PHI | no game | 2 | 60 | 7 | 11 |
| SG | Immanuel Quickley | TOR | @ WAS | 1 | 23 | 4 | 7 |
| G | Keyonte George | UTA | vs NOP | 1 | 22 | 3 | 5 |
| SF | Devin Vassell | SAS | vs HOU | 1 | 7 | 3 | 1 |
| PF | Karl-Anthony Towns | NYK | @ BOS | 1 | 19 | 12 | 1 |
| F | Franz Wagner | ORL | vs MIN | 1 | 22 | 6 | 5 |
| C | Jalen Smith | CHI | @ MIL | 1 | 15 | 8 | 1 |
| C | Myles Turner | MIL | vs CHI | 1 | 11 | 5 | 3 |
| UTIL | Darius Acuff Jr. | SAC | vs POR | 1 | 12 | 3 | 3 |
| BN | Jalen Williams | OKC | no game | 2 | 33 | 12 | 5 |
| BN | Jaylon Tyson | CLE | no game | 1 | 3 | 6 | 2 |
| BN | Joel Embiid | PHI | no game | 2 | 37 | 18 | 7 |
| IL | Kon Knueppel | CHA | vs ATL | 0 | – | – | – |
| IL | Bradley Beal | LAC | @ LAL | 0 | – | – | – |

Renders: `board_1280.png` (desktop), `board_400.png` (phone), `page_1280.png` (the page top with the sticky tab rail). Page overflow 0 px at both widths; the players table is 1026 px inside a 1058-px card on desktop.

## 3. What refreshes it (INFERENCE from §1)

Steps 5b (week matchup) and 6 (season deck) of the morning run already produce both records, so the board updates with every morning refresh and the runner prompt needs no change. A morning without a Yahoo pull draws the board from the rebuilt totals and says so in the card's first line; a morning without a week card record draws no board (the tab falls back to its previous first card).

## 4. Bounds

- **Not checked:** a live morning run with this code (the next is 12:03Z tomorrow). The suite's end-to-end tests run both scripts on fixture records.
- **Pre-existing failures:** `test_matchup_live.Record.test_todays_transcript_yields_todays_outlook` and `test_league_live.EndToEnd.test_todays_transcript_builds_a_passing_state_without_overwriting` fail on `main` `046ae2f` too (both read a FantasyBot transcript the container lacks); 463 run, 2 failures, 2 skipped.
- **Out of scope by design:** tip-off times (not in any record); the opponent's injury letters beyond Q/O (the status file carries only the two teams' listed statuses); a League tab of cumulative team totals (the owner's next idea, not yet ordered).

**Bands.** This change computes no figure; the standing sweep's bands (`redteam-2026-10-19/sweep.json`, engine 048efb6) are unchanged:
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

## Watchlist

- **The first morning run after merge:** `report/briefs/week_matchup_<date>.json` carries `board`, and the Today tab opens on the matchup card.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| the Today tab as a matchup board | **BUILT** on this draft PR | §1, §2 |
| `test_matchup_live` and `test_league_live` transcript dependence | **OPEN**, flagged (PR #172) | §4 |


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
