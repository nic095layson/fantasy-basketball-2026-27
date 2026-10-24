# The 10/20–10/22 box scores re-pulled on the season-pool index — 2026-10-24

Window: the records branch `season/daily` at `b52818c` (the files as committed) and this re-pull (draft PR into `season/daily`); the kit at `main` `330b2de` (PR #187, the box puller's index covers the season pool). No projection line, tag, roster, ledger row or engine constant changed; three record files change on the records branch.

Pull window: 2026-10-24 → 2026-10-24. Three live box-score pulls at ~00:20Z: ESPN's scoreboard and summary API and Basketball-Reference's game pages for 2026-10-20 (3 games), 2026-10-21 (11 games) and 2026-10-22 (2 games), two-outlet, through `scripts/box_pull.py`.

**Owner's decision (2026-10-24, on PR #187).** "Re-pull after merge (Recommended)": the three stored box files carried the narrow index's `pool_name`, so the ten season-pool players #187 newly pools (Hield, Clarkson, Shamet, Adams, Kispert, Finney-Smith, Hardy, Vanderbilt, Jackson-Davis, Tre Mann) had their first games outside the blend.

**Method (stated before the run).** The same script and outlets as the morning run, on the merged kit; the committed files compared to the re-pulled ones player by player; any box cell that differs is listed, not averaged (the script's own rule), and disclosed here.

## 1. What changed (EVIDENCE, `box-repull-pool-2026-10-24/repull_diff.json`)

- Pool names: 10/20 — Jordan Clarkson and Landry Shamet newly pooled (23 unpooled, was 25); 10/21 — Buddy Hield, Corey Kispert, Dorian Finney-Smith, Jaden Hardy, Jarred Vanderbilt, Steven Adams, Trayce Jackson-Davis, Tre Mann newly pooled (86, was 94); 10/22 — none (20). No previously pooled name changed. Player rows: 84 / 301 / 55, the same counts as before.
- Box cells: two differ, both 10/21 CHI steals — Norman Powell 1 → 2, Tobe Awaka 1 → 0 — an ESPN correction since the morning pull (the two outlets agree today: 300 matched, 1 cell differs on another line, as the PASS line says). Nothing else moved.
- `season_lines` on the re-pulled files (dry run, scratch): PASS; 267 kit players with games (a kit-file count, unchanged); unpooled with games 81 → 73. The ten players' lines now move with their games (Hield 7.6 → 7.0 pts, Clarkson 8.6 → 8.2 at the previous replay).
- Roster changes: none (no pool row, tag, line or roster touched).

## 2. Bounds

- **Out of scope by design:** the 73 names still unpooled (outside the season pool); 10/23's games (pulled by this morning's run on the merged index).
- **In scope and unverified:** nothing — every cell is compared mechanically.

**Bands.** This change computes no figure; the standing sweep's bands (`redteam-2026-10-19/sweep.json`, engine 048efb6) are unchanged:
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

## Watchlist

- **This morning's season-lines line:** "unpooled players with games" in the 70s, not the 80s, once the run reads these files.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| the three stored box files on the narrow index | **FIXED** on this draft PR | §1 |
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
