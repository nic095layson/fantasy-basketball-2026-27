# The 10/20 and 10/21 box scores re-pulled on the Jr.-suffix matcher — 2026-10-23

Window: the records branch `season/daily` at `b74ed6f` (the files as committed) and this re-pull (`ec36b0c`, draft PR #178 into `season/daily`); the kit at `main` `679fc8b`. No projection line, tag, roster, ledger row or engine constant changed; two record files change on the records branch.

Pull window: 2026-10-23 → 2026-10-23. Two live box-score pulls at 15:05Z: ESPN's scoreboard and summary API and Basketball-Reference's game pages for 2026-10-20 (3 games) and 2026-10-21 (11 games), both two-outlet, through `scripts/box_pull.py`.

**Owner's decision (2026-10-23, D4 of the system audit, re-put on corrected facts).** "Re-pull 10/20 and 10/21 box scores (Recommended)". The audit's first version said three rostered players had no projection line; that was wrong (erratum in `after-report-2026-10-23-system-audit.md` §2). The actual defect: the two files were matched before the Jr.-suffix fix (#174) merged, so "Darius Acuff Jr.", "Mikel Brown Jr." and other Jr. names carried no `pool_name` and their games never blended into their season lines.

**Method (stated before the run).** The same script and outlets as the morning run, on today's matcher; the committed files compared to the re-pulled ones player by player; any cell that differs is listed, not averaged (the script's own rule), and disclosed here.

## 1. What changed (EVIDENCE, `box-repull-2026-10-23/repull_diff.json`)

| date | games | players | same players | newly matched to the pool | pooled | evidence: cells that differ |
|---|---|---|---|---|---|---|
| 2026-10-20 | 3 | 84 | yes | Labaron Philon Jr. → Labaron Philon | 58 → 59 | none |
| 2026-10-21 | 11 | 301 | yes | Mikel Brown Jr. → Mikel Brown; Kelly Oubre Jr. → Kelly Oubre; Darius Acuff Jr. → Darius Acuff | 204 → 207 | two unrostered players (§2) |

Both pulls: two outlets, 0 ESPN-only, 0 bref-only lines (`BOX PULL: PASS` lines in the records' `sources`).

## 2. Disclosed side effect: outlet corrections since 10/22 (EVIDENCE)

Two players' 10/21 cells differ from the committed file because the outlets changed between the first pull (10/22 14:48Z) and this one, not because of the matcher:
- **Isaiah Collier (UTA, pooled, unrostered):** FGA 8 → 7, 3PA 2 → 1. On 10/22 ESPN and Basketball-Reference disagreed on both cells and the file carried ESPN's figure with the disagreement listed; today the outlets agree on 7 and 1.
- **Rasheer Fleming (PHX, unpooled, unrostered):** 3PA 3 → 4; the outlets now disagree on that cell and the file lists it in `reconciliation.mismatched`.

Neither is on a league roster; 3PA is not a scored category; Collier's FGA moves his FG% line by one attempt. Norman Powell (STL 1 vs 2) and Tobe Awaka stay listed as before.

## 3. What follows (INFERENCE)

The next morning run re-derives `season_lines_<date>.json` from these files: Acuff Jr. (35 min, 5-24 FG, 12 pts, 3 stl on 10/21) and Brown Jr. blend their first games into their lines, which the week card and the board then carry. Drummond is unaffected: he is out of the title simulation by the owner's 10/21 rule (in-season pickups stay out of the frozen pool), not for lack of a line.

## 4. Bounds

- **Records branch, not main.** The two files live on `season/daily`; #178 targets that branch so the runner's daily `merge origin/main` cannot conflict on `gates.json` or `pull-log.md`. This report and its pull-log row ride `main`.
- **Not checked:** the re-derived season lines (the morning run is the writer; running `season_lines.py` by hand here would produce a record the run then overwrites).
- **Out of scope by design:** the other eleven unpooled "Jr." names in those files are genuinely outside the pool (no line), and stay unpooled with their lines kept, as the script's rule says.

**Bands.** This change computes no figure; the standing sweep's bands (`redteam-2026-10-19/sweep.json`, engine 048efb6) are unchanged:
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

## Watchlist

- **The morning run after #178 merges:** `season_lines_<date>.json` lists Acuff Jr. and Brown Jr. among the movers with games 2 and 1 (Acuff: 10/21 and whatever he plays next), and `unpooled_with_games` no longer names them.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| 10/20 and 10/21 box-score files matched before the Jr.-suffix fix | **FIXED** on draft PR #178 (records branch) | §1 |
| outlet corrections for Collier and Fleming on 10/21 | **DISCLOSED**, carried as the outlets report them | §2 |
| `test_matchup_live` transcript dependence | **OPEN**, flagged (PR #172) | — |

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
