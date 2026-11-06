# The 3 PM run refreshes the lineup side (owner pick 2026-11-06: "refresh the lineup side only")

Pull window: 2026-11-05 → 2026-11-05 (no pull: the records on season/daily read only at 1e6652a — pull_2026-11-05_pm.json, status_2026-11-05_pm.json, league_state.json (PM), brief_2026-11-05.json; kit main 02c26d6, deck main e14cc42).

**Method up front.** Owner's question: "Would it be more efficient to have both morning and afternoon runs conduct the same information pull?" Assessment given in chat: a full second run would double-count every graded forecast (one per day feeds calibration, the decision log and the start/sit ledger) and move the odds by noise; what goes stale by 3 PM is the lineup side. Owner's pick on the card: refresh the lineup side only. Method parameters, stated before the build: on the afternoon deck build, `week_matchup.build` re-runs with the afternoon roster (`data/league_state.json` as the 3 PM pull left it), the 3 PM status file (`status_<date>_pm.json`, else the morning's) and the 3 PM Yahoo pull (`pull_<date>_pm.json`, else the morning's), written as `report/briefs/week_matchup_<date>_pm.json` with `phase: "pm"` and `refreshed_from`; no simulator, so the title odds, waiver pairs and every graded ledger stay the morning's; a refresh that cannot run is named in the step line and the morning record stands. EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: built and tested (suite 825 OK, 2 pre-existing skips) and run on the live 11-05 afternoon records: the refreshed record reads status_2026-11-05_pm.json and pull_2026-11-05_pm.json, its slots carry Ziaire Williams and not Matković, the page's Lineup card shows the 3 PM slots, the morning's Matkovic today-row carries the "no longer on your roster" chip, and the afternoon note says which parts are the 3 PM run's. Nothing merged. The companion build of the same day (the chip, `after-report-2026-11-06-gone-since-morning.md`) rides the same PR.**

## 1. What was built (EVIDENCE: the diff, the suites)

- `scripts/week_matchup.py` — `build()` reads `paths["status_file"]` when given (an afternoon run names its status file; the morning's newest-dated rule is unchanged).
- `scripts/season_deck.py` — `afternoon_lineup_refresh(date)`; `main()` on `--phase pm` runs it before the build, points the `week_matchup` input at the `_pm` record (pinned in the deck record) and appends to the PASS line "lineup side refreshed (…)" or "lineup refresh did not run (<why>), the 5 AM record stands"; page data `refresh.lineup_refreshed`; the Lineup card is the 3 PM slots on a refreshed page (active slots in Yahoo order), the brief's lineup otherwise; the afternoon note and the start/sit card say what the 3 PM run recomputed.
- Tests: `test_week_matchup.StatusFileOverride` (the named file is read; the morning rule unchanged); `test_season_deck.AfternoonLineupRefresh` (a refreshed record is read, pinned and announced; the Lineup card from the afternoon slots; a failed refresh keeps the morning record and says so). Every test that runs the afternoon `main()` mocks the refresh so no test writes into the kit's `report/briefs` (a first run did — caught by `git status`, restored).

## 2. Re-runs on the records (EVIDENCE: scratch worktree at 1e6652a, removed after; the records tree untouched)

`season_deck.py --date 2026-11-05 --phase pm`: `SEASON DECK: PASS — … pins 16 inputs; render: 7 tabs, 0 page errors; lineup side refreshed (week_matchup_2026-11-05_pm.json)`. The record: `phase: pm`, `refreshed_from` {status_2026-11-05_pm.json, pull_2026-11-05_pm.json, data/league_state.json}; `lineup_today.slots` has Ziaire Williams, no Matković; `moves: []`. Page: `refresh` {gone: [Karlo Matkovic], lineup_refreshed: true}; Lineup card PG Ty Jerome · SG Derrick White · G Collin Gillespie · SF Yaxel Lendeborg · PF Miles Bridges · F Ziaire Williams · C Kel'el Ware · C Neemias Queta · UTIL Jaden McDaniels; Today's games: "Karlo Matkovic (NOP) no longer on your roster".

INFERENCE: the afternoon week-matchup record is a second record per day in `report/briefs`; no grader reads `week_matchup_*_pm.json` (the accuracy and calibration graders read the dated morning files by exact name), so nothing is double-counted.

## 3. Bands quoted

No title share is quoted as a new figure in this report. The standing structural band for any title figure is the season sweep of 2026-11-02 (deck e14cc42): **weekly_availability is FRAGILE:** -2.6 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.2 (healthy players play 0.95 of games) / +0.0 (healthy players play 0.80 of games), mean of the two seeds.

Runner impact: code-only. The 3 PM run's deck step does the refresh itself; the new `week_matchup_<date>_pm.json` lands under `report/briefs`, which the afternoon commit already sweeps. No step or prompt change.

## 4. Bounds and open items

- Out of scope by design: afternoon title odds, waiver pairs, ledgers (the owner's pick); the brief Markdown.
- In scope and unverified: the first live afternoon run after merge (the PASS line carries "lineup side refreshed"; the `_pm` record is committed by the run).

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
