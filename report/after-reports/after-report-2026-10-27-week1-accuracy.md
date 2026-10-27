# Week 1 audit and the weekly accuracy card — 2026-10-27

Pull window: 2026-10-27 → 2026-10-27 (no new pull: the data are week 1's regular-season box scores, 2026-10-20 to 2026-10-25, already pinned in `season/daily` `data/actuals/` at a7d7283; no web search, no market pull).

**Method up front.** Owner 2026-10-27: "audit and report back ... where our system data projections and calculations hit the mark, missed", then "Weekly accuracy card ... build all four parts". Stated before the run: regular-season week 1 only (Oct 16 preseason and Oct 26 week 2 excluded); the frozen preseason lines graded (`players_v69.csv`; the season pool already blends week 1's games, so grading it would be circular); every pool player with 2+ games (261), not only rostered ones; per category the average, bias, mean absolute error and rank correlation, FG%/FT% pooled as makes over attempts; availability as games played over the player's NBA team's games, by the tier the simulator assumes. The era check (`league_per36.py`) does not apply: one week of one season. EVIDENCE marks what a run showed; INFERENCE what is derived.

## 1. Where the numbers hit (EVIDENCE, `report/accuracy.json` week 1)

- **Ordering players.** Rank correlation, projected vs actual per game: points 0.77, rebounds 0.75, assists 0.74, threes 0.68, turnovers 0.64, blocks 0.59, steals 0.53.
- **Against Yahoo's preseason line** (pinned 2026-10-14), same 255 players, mean absolute error per game: ours equal or lower in 6 of 7 categories (assists 1.11 vs 1.09 the exception). Not independent: Yahoo is one of the six sources blended into our line (the line's note).
- **The in-week Today card:** Brier 0.034 against 0.174 for "the leader to date wins"; its 12 calls of 60%+ all came true, its 20 calls under 20% all did not (4 mornings, 36 forecasts; later-week calls are easier).
- **Players tagged out:** 0 of 22 team games played, as assumed.

## 2. Where they missed (EVIDENCE)

- **Every line ran high.** Points 13.50 projected vs 11.95 actual (+13.0%), threes +15.0%, assists +12.6%, rebounds +7.1%; steals −5.5% and turnovers −6.3% (more than projected). FG% 0.478 vs 0.460, FT% 0.792 vs 0.777. About half the points gap is minutes (26.3 projected vs 24.7 played, kit `report/projections-2026-27.csv`, 257 players) and half per-minute output (18.6 vs 17.6 points per 36). Yahoo's line is high by the same amount (13.66 vs 12.09 on its 255). INFERENCE: a league-wide gap moves every team alike, so it changes category matchups little; its cause (early-season minutes, sample) was not checked.
- **Injury-risk players played less than assumed:** the 0.75 tier played 55 of 96 team games (0.57); the healthy 0.88 tier played 670 of 809 (0.83). This is the FRAGILE constant `arena.weekly_availability` (structural band −5.4 / +3.7 title points on the real schedule); 96 team games is a small sample.
- **The pre-week forecast:** 60.6% to win; lost 3–6. Brier over the nine categories 0.253 (a coin flip is 0.25); blocks (95%) and rebounds (75%) the big misses. One matchup cannot grade a 61% call.

## 3. What was built (EVIDENCE)

- `scripts/accuracy_week.py`: each finished week graded on the four parts above plus every matchup's pre-week forecast; appended to `report/accuracy.json` (append-only), `report/accuracy.md` regenerated. Week 1 back-filled; it reproduces this audit exactly.
- `weekly_preview.py --league --record --snapshot`: every pairing forecast and recorded in `report/calibration_league.json` before the week; the in-season lines copied to `report/accuracy/lines_week<N>.csv`. Exercised on the records branch for week 3 without writing: 6 of 6 pairings, none skipped, about a second at 2,000 draws.
- `morning.py`: the Sunday before a week runs it (non-fatal). `scoreboard_intake.py`: the Monday intake grades the week (non-fatal, on the PASS line).
- Tests, red first: `test_accuracy_week` (8, one of them the real week-1 numbers), `test_weekly_preview` (4), `test_morning.SundayForecasts` (2), `test_scoreboard_intake` (1). Kit suite: every file OK.
- **A defect caught in the build:** the pre-existing intake CLI test ran the new grading step against the kit's real `report/` and wrote a junk `report/accuracy.json` during the suite. The stray files were removed and the test now passes `--accuracy-out` to scratch.

## 4. Bounds

**Out of scope by design.** No projection line, injury tag, roster or engine constant changed; nothing is tuned on one week. **In scope and unverified.** Week 2 (Oct 26 – Nov 1) has no league-wide forecast and no line snapshot (its week had started); the first fully graded week is week 3 (forecast Sunday Nov 1, graded Monday Nov 9). The weekly matchup model does not apply Q/O statuses (its own note).

## 5. What 1 month and 3 months buy (INFERENCE from the sample sizes)

- **~1 month (4 weeks):** 12–15 games a player — points, rebounds, assists and minutes settle, steals and blocks still noisy; preseason vs in-season line, week on week; ~3,000 player-games on the availability tiers, enough to measure them; ~36 weekly and ~180 daily category forecasts for a first calibration check; ~12 league matchups scored (weeks 3–4).
- **~3 months (12 weeks):** ~144 team-weeks to fit the shared weekly shock (`TEAM_WEEK_SHOCK`, the other FRAGILE constant); this season's game logs to refit the category spreads (`SEASON_CV`); ~60 league matchups to check whether a 60% call wins about 6 in 10; projected seeds against standings. Title odds stay ungradeable within one season (one champion).

## 6. Next steps (owner decisions)

1. Merge this PR; the first Sunday step runs Nov 1, the first full grade lands Nov 9.
2. Whether to show the scorecard on the deck's Week tab (a small follow-up).

## Watchlist

- **Sunday 2026-11-01 morning:** a `next week forecasts` step line `WEEKLY PREVIEW: PASS — week 3`; new `report/calibration_league.json` week 3 (6 pairs) and `report/accuracy/lines_week3.csv`.
- **Monday 2026-11-02:** `SCOREBOARD INTAKE … accuracy week 2: … players … 0 league matchup(s) scored` (no week-2 forecast exists).

## Open-item receipts

| item | status | receipt |
|---|---|---|
| week 1 audit | **DONE** | §1, §2 |
| weekly accuracy card | **BUILT**, week 1 back-filled | §3 |
| calibration ledger rows labelled v69 | **OPEN**, owner decision (from #205) | — |

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck e0722cf (this change's deck commit), checked today, the same page the 10/22 day report replayed. Its table stands, carried here verbatim from the day report.

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
