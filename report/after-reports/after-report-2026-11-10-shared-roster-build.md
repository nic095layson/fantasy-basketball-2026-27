# One roster build for the simulator, the Monday fit and the week card's season cost (audit 2026-11-10, fix F1; council ruling 4–1)

Pull window: 2026-11-10 → 2026-11-10 (no pull: data/weeks/week_1..3.json, report/accuracy/lines_week1..4.csv and state_week1..4.json, report/fits/fit_week3.json at be859ea on season/daily, read only; kit main 5841723, deck main 01483de).

**Method up front.** Order: the owner's 11-10 audit card, pick "F1 + F2 + F4 (Recommended)", with a council ruling first and red tests before building. The council ruled 4–1 that F1 goes in its own PR, because it changes the inputs of a graded fit, and that the fit record must say which roster build it used. Tests were written first and seen failing (6 tests: 5 failed or errored before the code; the IL and no-line guard passed before, as it should). No projection line, injury tag, roster or engine constant changes. EVIDENCE marks what a run or a read showed; INFERENCE what is derived.

**Verdict: the Monday fit and the week card's season cost now build rosters the simulator's way, so a rostered player on an auto season line counts in all three. Weeks 1–3 are untouched (their snapshots hold no such player; the shock estimate through week 3 reproduces the record exactly). Week 4 is the first week it changes: five teams' modeled weekly points rise 4.7% to 6.4%.**

## 1. What changed

| place | before | after | evidence |
|---|---|---|---|
| `co_gm.py` | `rosters()` held the build inline | `team_roster(t, by, include_il=False, strict=True)` is the one build; `rosters()` calls it. strict=True keeps the old KeyError on a listed player with no row | tests `test_daily_brief.TeamRoster`, `AutoRowsSimulated` (unchanged, still green) |
| `fit_constants.py` `team_week_rows` | its own list: active players with a line | `CG.team_roster(team, by, strict=False)`: the same, plus the team's unpooled players the week's lines carry | tests `test_fit_constants.SharedRosterBuild` |
| `fit_constants.py` `run` | no word on the roster build | the fit record's `method.rosters` names the build and its start date | same |
| `week_matchup.py` `this_week_block` | its own list for the season cost of a drop | `CG.team_roster(t, by, strict=False)` | test `test_week_matchup.SeasonCostRoster` |

## 2. Effect on the graded fits (EVIDENCE: runs on the season/daily records)

| check | evidence (run on the records) |
|---|---|
| Unpooled players with a row in the week's lines | week 1: none · week 2: none · week 3: none (Nolan Traore and Matisse Thybulle were unpooled with no row) · week 4: five |
| TEAM_WEEK_SHOCK through week 3, new build | 0.1117 ± 0.0153, equal to `fit_week3.json` (0.11166) |
| Week 4 modeled PTS, seat 1, with Meleek Thomas counted | 581.3 → 615.8 (+5.9%) |
| Week 4 modeled PTS, seat 5, with Nolan Traore counted | 563.5 → 599.9 (+6.4%) |
| Week 4 modeled PTS, seat 9, with Morez Johnson Jr. counted | 515.0 → 547.3 (+6.3%) |
| Week 4 modeled PTS, seat 11, with Mario Hezonja counted | 622.9 → 655.9 (+5.3%) |
| Week 4 modeled PTS, seat 7, with Kenrich Williams counted | 605.1 → 633.8 (+4.7%) |

INFERENCE: without this fix the week-4 fit would read those five teams' actual/mu about 5–6% too high, because the actual totals hold these players' box lines and the model did not. That pushes the measured shock up. The size of the effect on the week-4 shock figure is not known until week 4's actuals exist (2026-11-16).

## 3. Checks

- Red first: `test_daily_brief.TeamRoster` (2), `test_fit_constants.SharedRosterBuild` (3), `test_week_matchup.SeasonCostRoster` (1).
- Whole suite on this branch: 880 tests OK (2 skipped).

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds (season sweep 2026-11-09, engine 01483de). This fix changes no title figure: the title simulator already used this build (PR #246).

## 4. Bounds

- Out of scope by design: F2 and F4 (PR #250), F3, F5, F6.
- In scope and unverified: whether an auto-row player's modeled week (his line times a full week of games) overstates a deep-bench player. The title simulator has made the same assumption since 2026-11-09; grading it needs finished weeks (did not check).
- The fit's `_missing_lines` list still names only active listed players without a line, as before.

## 5. Next steps (owner decisions)

1. **Merge before the 2026-11-16 Monday fit (Recommended).** The week-4 fit, the first that can propose a constant, then runs on the simulator's rosters and says so in its record.
2. Hold until after the week-4 fit, and run that fit both ways for comparison (a scratch run and a short report, on your go).

Runner impact: code-only. The Monday `fit_constants.py` step and the morning week card run as before with no prompt change; the fit record gains `method.rosters`.

## Fired

plan-gate (loaded; compact plan table shown before the first edit) · council (loaded; ruling 4–1) · adversarial-verify (loaded before delivery).

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
