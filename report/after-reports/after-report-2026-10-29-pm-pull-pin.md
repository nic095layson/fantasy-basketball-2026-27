# The 3 PM run pins its own Flaim pull (owner, 2026-10-29)

Pull window: 2026-10-29 → 2026-10-29 (no new pull: the 10-29 morning and afternoon pins on season/daily ced738c and 62cfdc6, read only).

**Method up front.** The Runner's 10-29 afternoon report found the 3 PM roster step still rewrote the morning's pinned Flaim pull, the same overwrite class #225 fixed for the status files. The owner picked "Fix like #225". EVIDENCE marks what a run showed.

**Verdict: fixed. The afternoon writes `pull_<date>_pm.json` and `rosters_<date>_pm.transcribed.csv`; the morning's pin stays byte-identical.**

## 1. Fix (EVIDENCE)

| file | before | after |
|---|---|---|
| Flaim pull pin | 3 PM rewrote `pull_<date>.json` (10-29: sha256 a409ab3e… to 841c2ca4…) | 3 PM writes `pull_<date>_pm.json`, built from the morning pin (lineups, matchups and the available list carried forward as before) |
| roster transcription | 3 PM rewrote `rosters_<date>.transcribed.csv` | 3 PM writes `rosters_<date>_pm.transcribed.csv` |
| 3 PM deck's pull input | the rewritten morning file | `pull_<date>_pm.json` |

- `league_live.pin_paths()` names the files by phase; the command line is unchanged (`--phase pm` already runs), so the Runner prompt does not change.
- Readers that glob `pull_????-??-??.json` (league_table, league_pairings, form_board, week_matchup) skip `_pm` names by construction; the morning readers (brief, lineup check, week card) keep reading the morning pin.
- Tests: 2 new, red first (1 error, 1 failure), now pass; test_league_live 28 OK with test_season_deck.PhasePaths.
- Behavioral check (scratch copy of season/daily, the morning pull and transcription restored from 62cfdc6, an afternoon run on the branch-tip pull): `LEAGUE LIVE: PASS … pinned data/source/flaim/pull_2026-10-29_pm.json`; the morning pull and transcription re-hash unchanged; the `_pm` pin carries daily, matchups, free_agents and standings; the league state's sources name the `_pm` files; `SEASON DECK: PASS … (afternoon refresh)`, its pull input re-checks.

Runner impact: code-only (the afternoon command line is unchanged; the next 3 PM run writes the `_pm` pin).

## Bounds

Out of scope by design: records already made are unchanged; 10-29's morning pull survives in git history at 62cfdc6.

## Watchlist

- The 10-30 3 PM run: `pull_2026-10-30_pm.json` written, `pull_2026-10-30.json` unchanged from the morning commit.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| 3 PM rewrites the morning's Flaim pin | **FIXED** in code | §1 |

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
