# The box puller's index covers the season pool: ten players' games reach the blend — 2026-10-24

Window: the kit at `main` `e1f34a2` plus this branch; the 10/23 records on `season/daily` (box scores 10/20–10/22, `data/season/pool_season.csv`). No projection line, tag, roster, engine constant or ledger row changed; one function and one call site change.

Pull window: 2026-10-24 → 2026-10-24. No pull: the replay re-resolves the box rows already on disk.

**Finding (2026-10-23/24, the minutes-board build's adversarial pass; owner go "Fix next, own PR").** `box_pull` resolved every box-score name against the kit's `report/projections-2026-27.csv` (325 names). The season pool the board and simulator run on is the deck's 335 plus in-season additions, so ~20 season-pool players (Hield, Clarkson, Shamet, Westbrook, Brogdon, Valanciunas, Adams, Lonzo Ball, D'Angelo Russell, Batum, Vanderbilt, Kispert, Vincent, Hawkins, Strawther, Agbaji, Finney-Smith, Tre Mann, Hardy, Jackson-Davis) were unpooled in every box file, and `season_lines` blended none of their games: their board lines were preseason lines, unmoved. My first flag (2026-10-23, PR #186) blamed spellings; the diagnosis here corrected it — the spelling cases (Oubre, Herb Jones, Cam Johnson, Acuff, Mikel Brown) already resolve; the gap was membership.

**Method (stated before the fix).** `load_pool_names` returns the kit file's names, then every season-pool name whose suffix-free key the kit file lacks and whose spelling is not an alias variant of a kit name. The kit spelling wins a shared key, so `match_name`'s one-name-per-key rule holds and ESPN's spelling keeps landing on the kit row. The replay re-resolves the stored box rows (`name`, `team`) with `resolve_names`, the function the puller calls (assumption A1: that reproduces the live puller's matching).

## 1. What changed (EVIDENCE)

- `scripts/box_pull.py`: `SEASON_POOL_CSV`; `load_pool_names(path, season_csv, aliases)`; the pull passes the alias table to both.
- Red first: `test_box_pull.Resolve.test_pool_names_take_in_the_season_pool_with_the_kit_spelling_winning_a_shared_key` (a season-only name resolves; a shared key keeps the kit spelling; an absent season file is the old behaviour; an alias-variant spelling is not added and ESPN's spelling still lands on the kit row). The last case was added after replay 1 flipped Herb Jones and Cam Johnson off their kit rows (`players_with_games` 267 → 265) — the plan's branch rule, fired and fixed.
- Replay on 10/20–10/22: index 325 → 345 names; newly pooled with games: Hield, Kispert, Finney-Smith, Hardy, Vanderbilt, Clarkson, Shamet, Adams, Jackson-Davis, Tre Mann (10); previously pooled names changed: none; unpooled with games 81 → 73 (the remainder are outside the season pool). `season_lines` on the re-resolved files: PASS, 267 kit players with games (unchanged, a kit-file count), 212 lines moved (was 210); Hield's season line 7.6 → 7.0 pts, Clarkson's 8.6 → 8.2 — the games now count. `box-pool-membership-2026-10-24/season_lines_2026-10-23.replay.json`.
- Suite: `test_box_pull` 6 of 6 in `Resolve`; full suite bar the two pre-existing transcript failures (#172); the ledger unchanged across the suite.
- Roster changes: none (no pool row, tag, line or roster touched).

## 2. Bounds

- **Takes effect** at the next morning run's box pull (the step reads the season pool file committed on `season/daily`); earlier box files keep their stored `pool_name` until re-pulled — `box_pull --date` on 10/20–10/22 would re-resolve them, a separate decision.
- **Out of scope by design:** the 73 names outside the season pool (deep bench); the blend's weights.
- **Assumption A1:** re-resolving stored rows reproduces the live puller (same function, same inputs; not run against ESPN live).

**Bands.** This change computes no figure; the standing sweep's bands (`redteam-2026-10-19/sweep.json`, engine 048efb6) are unchanged:
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

## Watchlist

- **Tomorrow's season-lines line:** "unpooled players with games" should fall from the 80s toward the 70s once the day's box file is pulled on the wider index.
- **The three stored box files (10/20–10/22):** still carry the narrow index's `pool_name`; a re-pull decision if the ten players' first games should enter the blend.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| box index missing season-pool players (season_lines blends none of their games) | **FIXED** on this draft PR | §1 |
| re-pull 10/20–10/22 on the wider index | **OPEN**, owner decision | §2 |
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
