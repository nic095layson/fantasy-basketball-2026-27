# The league table matches Yahoo teams by team key (owner pick A1, 2026-11-09)

Pull window: 2026-11-09 → 2026-11-09 (no pull: the records on season/daily read only at 85556cc — pull_2026-10-21 … pull_2026-11-09, data/league_state.json, report/league/league_2026-11-08.json, data/weeks/; kit main 8f252a2, deck main e14cc42).

**Method up front.** Order: runner after-report `after-report-2026-11-09-runner-window.md`, pick A1. The 11-09 morning step failed `LEAGUE TABLE: FAIL — Yahoo team 'Lauri’s Prime Rib' is not in the league state`: seat 3 renamed itself to SNOWTIME WHITE WALKERS, and every pull through 11-08 pins its matchup blocks under the old name. Method parameters, stated before the build: a Yahoo side is matched by its team key (`teamKey`) against the newest pinned pull that carries rosters (key → today's name, the same rule `league_pairings.names_by_key` has used since the 10-29 pick "Key on Yahoo team key"), and falls back to the name it carries when the key is unknown; the team is shown under the league state's name. The week records (`data/weeks/week_1.json`, `week_2.json`) and `team_weeks.csv` are not touched. EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: fixed and tested. `league_table.py --date 2026-11-09` PASSes on the live records and lists seat 3 once, as SNOWTIME WHITE WALKERS, Yahoo 20-7-0, W-L-T matching the kit's finished weeks for 12 teams. One more fix rides along, which the same key match brings: the week-1 rebuild had been silently dropping the pinned lineups of three renamed teams.**

## 1. What changed (EVIDENCE: the diff, the suite)

- `scripts/league_table.py` — `key_names(pulls)`: team key → today's name from the newest pull with rosters. `week_from_yahoo(block, state, keys=None)` matches a side by key first (with no `keys`, it behaves as before, so `scoreboard_intake.py` is unchanged). `build()` passes the key map. In the same file, two more lookups by name now go by key first: the rebuild's pinned daily lineups (`rebuild_week`) and the Yahoo standings rows (`standings_of`).
- `scripts/test_league_table.py` — class `Renamed`. Week 1's finals are pinned under the old name and the state and newest rosters carry the new one: the team is found by key, shown once under the new name, and its opponent names the new name. Standings pinned under the old name also find their seat. With no key map, an unknown name still halts.

Red first (EVIDENCE): with main's `league_table.py`, `test_league_table.Renamed` gave 3 errors (`TableError: Yahoo team 'Team 3' is not in the league state`, and a `TypeError` on the new argument). With the fix, `test_league_table` passes 24 tests.

## 2. The known answer (EVIDENCE: scratch worktree of season/daily at 85556cc, removed after; the records tree untouched)

| | before (main) | after |
|---|---|---|
| `league_table.py --date 2026-11-09` | `LEAGUE TABLE: FAIL — Yahoo team 'Lauri’s Prime Rib' is not in the league state` | `LEAGUE TABLE: PASS — 2026-11-09: week 4; wk1 finished (rebuild), wk2 finished (yahoo), wk3 finished (yahoo), wk4 not started …; power #1 SNOWTIME WHITE WALKERS (0.641), you #6 (0.537); … Yahoo W-L-T matches the kit's finished weeks for 12 teams` |
| seat 3 in weeks 1–4 and cumulative | — | SNOWTIME WHITE WALKERS, once each |
| seat 3 standings | — | 20-7-0 |
| week 2 totals vs the 11-08 record | — | all 12 seats equal |

## 3. A ride-along correction: renamed teams' pinned lineups in the week-1 rebuild (EVIDENCE: rebuild_week run with and without the key map on the same inputs)

Three Yahoo keys pinned their week-1 lineups (10-20 … 10-25) under names they no longer carry:

| key | name pinned in week 1 | name now | seat |
|---|---|---|---|
| t.1 | Lauri’s Prime Rib | SNOWTIME WHITE WALKERS | 3 |
| t.4 | Splash Mountain | Scottie’s Thotties | 8 |
| t.5 | Giavaris Jamal Javarison-Lamar | ANONG NANGIANNIS?! | 5 |

On main, `rebuild_week` matched pins by the name the pin carries. The pins of seats 5 and 8 have been missed since their renames, and those days fell back to today's roster, with no message. With the key match, week-1 totals change for exactly seats 3, 5 and 8. INFERENCE: the new figures are the right ones, because they are the lineups those teams actually set. Week 1's W-L-T comes from `data/weeks/week_1.json` and does not move, so standings and the record check are unaffected. The all-play power ranking reads week 1's totals and can shift slightly.

Not caused by this change (EVIDENCE: 11-08 vs 11-09 records): week-1 rebuild totals also drift from day to day for every seat. On unpinned days the rebuild uses the current roster, and that roster changes. This is pre-existing behaviour, named here and not touched.

## 4. Other scripts that match teams by name — reported, not changed (order: "stop and report the caller rather than guessing")

| caller | what it matches by name | exposure to a rename |
|---|---|---|
| `scoreboard_intake.py:95` | calls `week_from_yahoo(block, state)` with no key map | reads the day's own pull, whose names are current. INFERENCE: low exposure |
| `flaim_live.py:211` | matchup sides by `teamName` | same-pull lookups. INFERENCE: low exposure |
| `league_live.py:106` | rosters by `teamName` | same-pull. INFERENCE: low exposure |
| `week_matchup.py:186`, `:507-510` | daily pins by `teamName`; the owner's team found by name | an older pin of a renamed team is missed |
| `lineup_log.py:78` | the owner's own team by name | only the owner's rename would break it |
| `manager_log.py:193-204` | manager by folded team name | a rename loses the manager label |

None of these failed on 11-09. Each is a candidate for the same key match on the owner's word. None was changed.

## 5. Bands quoted

This report quotes no new title share. The standing structural band for any title figure is the season sweep of 2026-11-02 (deck e14cc42): **weekly_availability is FRAGILE:** -2.6 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.2 (healthy players play 0.95 of games) / +0.0 (healthy players play 0.80 of games), mean of the two seeds.

Runner impact: code-only. After merge, the morning's league-table step stops failing on the rename. No step or prompt change.

## 6. Bounds

- Out of scope by design: the week records and `team_weeks.csv` (not rewritten); the callers in §4.
- In scope and unverified: the first live morning run after merge.
## Watchlist

- 2026-11-09: week 3 on the accuracy card, the candidate's second graded week under D-ML-1.
- 2026-11-16: the week-5 confidence re-run; re-run `backtest.py` on about 20 games per player.

## Open-item receipts

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck 366d3ca (this PR changes no deck file), checked today, the same page the 10/22 day report replayed. Its table stands, carried here verbatim from the day report.

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
