# The scoring loop: every morning's P(win) graded against the finals — 2026-10-24

Window: the kit at `main` `330b2de` plus this branch; the 10/22 and 10/23 morning cards on `season/daily` (`report/briefs/week_matchup_<date>.json`). No projection line, tag, roster, engine constant or ledger row changed; one new script, one new record, two hooks.

Pull window: 2026-10-24 → 2026-10-24. No pull: the dry run reads the two morning cards already on disk against SYNTHETIC finals (illustrative; week 1 is not final until Sunday).

**Owner's decision (2026-10-24, Council verdict 5–0, step 2).** "Build the scoring loop now": without it, Monday's first finals go unscored and the calibration series starts a week late. The weekly PRE-WEEK prediction was already scored by `weekly_preview.score()` at the intake; this adds the DAILY card.

**Method (stated to the owner before the build).**
- Outcome: won 1, tied 0.5, lost 0; Brier = (p − outcome)², 0 perfect, 0.25 a coin flip. The weekly ledger counts a tie as a loss by its pre-registered rule of 2026-10-15 — left as it is (flagged, owner's call); the daily record uses 0.5, which is proper for a Brier score, and says so in its `method`.
- Baseline: that morning's lead to date as a forecast (1 led, 0 behind, 0.5 level); skill = baseline Brier − card Brier, positive when the card beats the scoreboard.
- Reliability: five bins of width 0.2 over every morning × category forecast — count, mean P, hit rate.
- Append-only: a week is scored once; a rerun on identical inputs is a no-op; on different inputs it halts and leaves the record. Mornings without a card are listed as missing, never filled.

## 1. What was built (EVIDENCE)

- `scripts/score_week.py`: `outcomes`, `score`, `load_cards`, `run`, `render`; record `report/calibration_daily.json` (+ `.md`); CLI `--week --weeks-dir --briefs-dir --out --ledger`; `WEEK SCORE: PASS — …`.
- `scripts/scoreboard_intake.py`: after the weekly ledger score, runs the daily scorer (non-fatal; its line names a failure); `--calibration`, `--briefs-dir`, `--daily-out` for tests; skipped under `--no-ledger`. The Runner's Monday prompt needs no change.
- `scripts/weekly_preview.py`: `--ledger PATH` (default unchanged), so a test can score a scratch ledger instead of the real one.
- `scripts/season_deck.py`: `default_paths` gains `scores`; the Week tab gains the Scorecard card (per week: result, mornings scored and missing, forecasts, Brier card vs lead, skill; reliability over all scored weeks); absent record → "first finals land at Monday's intake".
- Red first, then green: `test_score_week.py` (8: Brier by hand, tie 0.5, baseline and skill, per-category means, reliability bins, missing mornings listed, idempotent rerun, halt on changed inputs, CLI), `test_scoreboard_intake` (+1: the ledger-on CLI path scores from the morning cards into a scratch record), `test_season_deck.Scorecard` (2). One hand expectation of mine was wrong and corrected, not the code: 10/23's baseline in the fixture is 0 (every lead matched the final), not 1/9.
- Dry run (`score-week-2026-10-24/`): the two real morning cards against synthetic finals built from the 10/23 card's leaders (won FG%, FT%, TO; the rest lost): 18 forecasts, Brier 0.041 vs lead-to-date 0.181, skill +0.140 — ILLUSTRATIVE, the finals are made up to exercise the arithmetic. Hand check PTS 10/23: p 0.0278, lost → (0.0278 − 0)² = 0.000773, as the record says. Missing mornings listed: 10/20, 10/21 (the card first ran 10/22), 10/24, 10/25 (not yet).
- Suite bar the two pre-existing transcript failures (#172); the ledger unchanged across the suite.
- Roster changes: none (no pool row, tag, line or roster touched).

## 2. Bounds

- **Takes effect** Monday 10/26 at the intake (`scoreboard_intake --from-pull`), with 4 of 6 mornings scorable for week 1 (10/22–10/25); full weeks from week 2.
- **Flagged, not fixed:** the weekly ledger's tie-as-loss rule (pre-registered 2026-10-15); the two records score differently on a tied category and say so.
- **Out of scope by design:** scoring the pre-week `cat_p` per category beyond what `weekly_preview` already does; any change to how P(win) is computed.
- **Assumption A1:** Monday's `week_1.json` carries `owner.won/lost/tied` as `owner_result` writes them (the test fixtures mirror that function's output).

**Bands.** This change computes no engine figure; the standing sweep's bands (`redteam-2026-10-19/sweep.json`, engine 048efb6) are unchanged:
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

## Watchlist

- **Monday 10/26:** the intake line ends "week score scored, 4 mornings / 36 forecasts, Brier … vs lead-to-date …"; a `week score FAIL` names why, with the intake itself intact.
- **After 4–6 weeks:** the reliability table says whether the stated chances are honest; until then one week is one week.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| the scoring loop (Council step 2) | **BUILT** on this draft PR | §1 |
| the weekly ledger's tie-as-loss rule | **OPEN**, flagged | §2 |
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
