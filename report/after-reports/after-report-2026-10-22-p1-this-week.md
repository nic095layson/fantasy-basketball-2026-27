# P1 built: free agents judged on this week's matchup — 2026-10-22

Window: the kit at `main` `d2f2f0f` plus this branch; the 10/22 morning records (`season/daily` `e7b69bb`: league state, Flaim pull with Yahoo's available-player list, box scores, status file); the deck at `048efb6`. No projection line, tag, roster or engine constant changed.

Pull window: 2026-10-22 → 2026-10-22. No new pull: the run reads the 10/22 morning run's records, already logged.

**Owner's decision (2026-10-22, decision 1 on PR #171).** "Full build (Recommended)": upgrade the week card's pickup scan and add a "This week" view to the Free Agents tab — categories won per add — red-first, on its own draft PR. The question behind it (2026-10-22): "instead of solely relying on zscore gscore, can this tool also analyze what categorical contributions the free agents can provide (plus remaining games for the week) to help win my weekly matchup?"

**Method (stated to the owner before the build, M8 in `week_matchup.py`).**
- Each category's chance: the normal approximation on the final totals (`co_gm._pcat`). To date is fixed; each remaining started game adds a·(x·cv)² + a·(1−a)·x² to a counting category's variance (season per-game CV, `arena.SEASON_CV`; a = that day's availability); FG% and FT%: the binomial floor on the remaining makes × `PCT_MIX_INFL`², over the total attempts. The shared weekly shock (`TEAM_WEEK_SHOCK`) is left out because the games come from the real schedule.
- A free agent's worth this week: the change in expected categories won, the sum of the nine changes in P(win) (exact by linearity), in place of the drop candidate that helps most. Candidates: the active players below the active roster's median value, finished or not. The swap starts tomorrow (assumption A2: waiver players cannot be told apart, so the conservative day).
- The season cost of that drop: the change in expected weekly categories against the other eleven teams (the waiver scan's measure, `co_gm.waiver_pairs`).
- Pool: Yahoo's available-player list from the morning pull (up to 100), with every exclusion named as before (M7).

## 1. What was built (EVIDENCE)

- `scripts/week_matchup.py`: `remaining()` carries the variance of what it projects (line 203); `cat_chances` (line 208); `swap_candidates` (line 233); `scan_drop_alone` (line 247); `scan_this_week` (line 261); `this_week_block` (line 366); the card's categories carry `p_win` and the record `exp_cats` (line 554). The old M7 scan (a finished player only, point flips) is unchanged and still runs.
- `scripts/season_deck.py`: the Today card shows each category's chance and the expected categories, then "This week's adds" (`thisWeek`, line 302): the move, Δ expected categories, games, the drop's own part, the season cost, the categories moved; the drops' own effects; the free agents with no playable game. The Free Agents tab sorts by this week by default when the scan ran, and back to season z (`#fa-sort`, line 495); each free agent shows "this week +x (n g, for <drop>)".
- Tests: `scripts/test_week_matchup.py` class `ThisWeek` (line 184) and the card-level test (line 359); `scripts/test_season_deck.py` lines 574 and 591 onward.

## 2. Tests, and what the first green run taught

- Red first: 8 errors of 39 in `test_week_matchup.py` and 3 failures of 69 in `test_season_deck.py` on main's code.
- **Two of my tests were wrong, and the model was right.** In the fixture, dropping "Scorer" (25 points on .45 shooting, 2 turnovers) helped with nobody added, because points were already safe and his shooting and turnovers cost categories. So the best drop for a free agent with no games was Scorer, and that free agent showed a positive change he did nothing to earn. Two changes followed, both within the stated method: each row now reports the drop's own part beside the total (the add's part is the rest), and free agents with no playable game after today are listed apart, not ranked. Two tests were corrected (their premise, not their tolerance) and one added for the split.
- One tolerance corrected: the card rounds each P(win) to 4 places, so the card's expected categories is checked against their sum to 3 places.
- One existing test held a promise in place: the Free Agents tab still contains the owner's 10/20 z-sort; the this-week order is a stable second sort on top of it.
- Green twice: 40 of 40 and 69 of 69. Full suite: 366 run, 1 failure, 1 skipped. The failure is `test_matchup_live.Record.test_todays_transcript_yields_todays_outlook`, which reads the newest session transcript and fails identically on unchanged `main` `d2f2f0f` (PR #172 §2); not skipped, not changed.

## 3. The real run on today's records (EVIDENCE; `p1-this-week-2026-10-22/week_matchup_2026-10-22.json`, two runs byte-identical)

Week 1 against MAXEY-MUM OVERDRIVE, four days left (10/22–10/25). The card's chances sum to the expected categories (3.444 of 9); on every scored row the nine changes sum to the total (largest difference 0.0).

| category | you, projected final | them | P(you win) |
|---|---|---|---|
| FG% | 0.507 | 0.448 | 0.973 |
| FT% | 0.811 | 0.795 | 0.656 |
| 3PTM | 58.8 | 72.0 | 0.101 |
| PTS | 588.2 | 669.4 | 0.061 |
| REB | 170.9 | 209.0 | 0.018 |
| AST | 123.2 | 141.5 | 0.113 |
| ST | 39.1 | 40.3 | 0.433 |
| BLK | 22.7 | 27.4 | 0.208 |
| TO | 62.0 | 72.8 | 0.880 |

Pool: Yahoo's list (100 listed), 90 scored, 86 ranked, 4 with no playable game after today. Drop candidates: PJ Washington, Miles Bridges, Yaxel Lendeborg, Christian Braun, Neemias Queta, Kel'el Ware.

| move | games | Δ expected cats | drop's part | season cost | categories moved |
|---|---|---|---|---|---|
| Anfernee Simons (PHI) for Neemias Queta | 2 | +0.342 | -0.001 | -0.1664 | 3PTM +0.16, PTS +0.12, TO -0.10, AST +0.09, ST +0.07, FG% -0.02, REB +0.01, BLK -0.01, FT% +0.01 |
| Keon Ellis (BKN) for Neemias Queta | 2 | +0.293 | -0.001 | -0.2020 | ST +0.14, 3PTM +0.09, TO -0.05, PTS +0.05, BLK +0.05, AST +0.04, FT% -0.02, FG% -0.01, REB +0.01 |
| Noah Clowney (BKN) for Neemias Queta | 2 | +0.281 | -0.001 | -0.1915 | 3PTM +0.10, ST +0.09, PTS +0.08, TO -0.08, BLK +0.05, AST +0.04, REB +0.02, FG% -0.02, FT% -0.01 |
| Brook Lopez (LAC) for Neemias Queta | 2 | +0.206 | -0.001 | -0.0608 | BLK +0.09, 3PTM +0.06, PTS +0.03, TO -0.02, FT% +0.02, ST +0.02, AST +0.01, FG% -0.01 |
| Julian Champagnie (SAS) for Neemias Queta | 1 | +0.182 | -0.001 | -0.0582 | 3PTM +0.08, ST +0.06, PTS +0.04, TO -0.04, AST +0.02, BLK +0.02, REB +0.01, FG% -0.01, FT% -0.01 |

What it says (INFERENCE from the figures above): the best adds this week are worth about a third of a category against this opponent, almost all from the add (the drop's part is −0.001), and every one of the 86 ranked moves costs season value (negative season figure in 86 of 86). The card puts both numbers side by side; whether a third of a category this week is worth a season cost is the owner's call, and the card makes no recommendation.

Page: built from these records, `deck_render_check` PASS, no page error in Chromium at 420 px, no sideways page scroll; screenshots in the folder (the first render clipped the Δ column at phone width; the column order and cell wrapping were fixed and re-rendered).

## 4. Validation plan and bounds

- **How it will be checked:** each morning's card records each category's chance; once weekly results are scored (P2), the per-category Brier score of these chances against what happened is the calibration test, beside the ledger's preseason-style prediction. Not yet possible: no week has been scored.
- **Assumptions (unconfirmed):** A1, every add needs a drop (the 15 spots include the IL slots; 13 players fill the non-IL ones); A2, the swap counts from tomorrow.
- **INFERENCE, not tested:** the normal approximation is coarse for small weekly counts (a category decided by a few blocks); a simulation for playoff weeks was fenced out of this build (PR #171 §2).
- **Out of scope by design:** trades, lineups, the shared weekly shock, any change to lines or engine constants.

**Bands.** The category chances use neither FRAGILE constant of the standing sweep (`redteam-2026-10-19/sweep.json`, engine 048efb6): the shared shock is left out, and availability is the day's status, not the weekly discount. The season cost does run on `arena.team_week_model`, which carries the weekly availability discount; the sweep measured both constants on the title share:
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

Their effect on the season-cost column was not measured (did not check).

## Watchlist

- **The morning runner** runs `week_matchup.py` already (`morning.py`), so the card and the Free Agents view refresh each morning once this is merged; the runner's stored prompt needs no change.
- **Week 2 starts 10/26:** the first Monday the scan has a full week of games to judge.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| P1, matchup-aware free agents | **BUILT** on this draft PR; not merged | §1–§3 |
| the drop-alone effect (a drop that helps on its own) | **SHOWN** on the card, not credited to the add | §2 |
| `test_matchup_live` transcript dependence | **OPEN**, flagged (PR #172) | §2 |

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward as the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck 048efb6, checked today, the same page the 10/22 day report and the GAUNTLET report replayed. Its table stands, carried here verbatim from the day report.

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
