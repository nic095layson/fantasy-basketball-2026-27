# The pre-week matchup forecast on each NBA team's real games — 2026-10-27 (build 5, first slice)

Pull window: 2026-10-27 → 2026-10-27 (no pull: `report/schedule/games-2026-27.csv`, the records branch's rosters and season pool as of 10-27; no web search, no market pull).

**Method up front.** Owner 2026-10-27: build 5's first slice, the part that needs no accrued data ("first slice now"). **Candidate only**: a second league-wide pre-week forecast is recorded each Sunday beside the flat one and graded each Monday as a second matchup column; nothing live reads it. Stated before the run: the model is the simulator's `team_week_model` with one substitution — a player's expected games are his NBA team's games in the fantasy week's window times his availability, not 3.5 × availability; the engine's daily-fill weights, availability tiers, category list and percentage-mix constant are imported, never copied. Switch rule, pre-committed (D-RG-1): a lower Brier than the flat forecast over at least 4 consecutive graded weeks, on the owner's word. EVIDENCE marks what a run showed; INFERENCE what is derived.

## 1. The drift check (EVIDENCE)

With every NBA team set to exactly 3.5 games, the candidate's `(mu, var)` on the owner's real roster equal the engine's to nine decimal places in every category (`test_real_games.DriftCheck`); a team at 4 games scales its counting means by 4/3.5 and at 3 by 3/3.5 exactly. A team code the schedule lacks falls back to 3.5 and is named in the record, never dropped. So the only thing the candidate changes is the games count.

## 2. Week 3, forecast both ways (EVIDENCE, scratch run on the records branch at a7d7283, 4,000 draws per seed, not recorded)

Window 2026-11-02 → 11-08: 18 NBA teams play 4 games, 12 play 3; no team unscheduled, no pair skipped.

| matchup (seat a v b) | P(a wins), flat 3.5 | P(a wins), real games | change |
|---|---|---|---|
| 3 v 6 | 0.544 | 0.703 | +0.159 |
| 4 v 2 | 0.393 | 0.369 | -0.024 |
| 1 v 5 | 0.524 | 0.450 | -0.074 |
| 8 v 11 | 0.470 | 0.601 | +0.131 |
| 12 v 7 | 0.499 | 0.489 | -0.010 |
| 9 v 10 | 0.097 | 0.032 | -0.065 |

INFERENCE: a one-game edge in a 3–4 game week moves a close matchup by 10–16 points of win chance (seats 3 v 6, 4 v 2); the flat model cannot see it. Which forecast is better is for the card: the first graded week is week 3 on 2026-11-09.

## 3. What was built (EVIDENCE)

- `real_games.py` (new): `team_week_model_games`, `week_games` (each NBA team's games in a fantasy week's window from the schedule file, which carries all 1,200 games through 2027-04-11). `test_real_games` (4, red first).
- `weekly_preview.py`: `preview_league(..., real_games=True)`; the Sunday `--league` step records the real-games forecast in `report/calibration_league_real.json` (append-only, its own method line) beside the flat one (`test_weekly_preview.RealGamesLedger`, 2). `accuracy_week.grade_matchup_ledgers`: the `matchups_real` column and the switch rule under the table (`test_accuracy_week.RealGamesColumn`, 2).
- Kit suite: every file OK; no stray writes (the intake tests already pass every output path to scratch).

## 4. Bounds

**Out of scope by design.** The owner's own pre-week ledger (`calibration.json`, the deck's Week tab) stays on the flat model until the card decides; the in-week Today card already uses real remaining games and is untouched. The rest of build 5 (game context — rest days, home/away, margins — and real-schedule variance) waits for the context now accruing since build 1, as assessed. **In scope and unverified.** Whether real games forecast better: no graded week yet. Weeks 7 and 17 (two-week matchups) take the real count over the whole window, the flat model's known wrong spot; the first such grade is 2026-12-14.

## 5. Next steps (owner decisions)

1. Merge this PR; Sunday 11-01 records week 3 both ways, Monday 11-09 grades them.
2. The context-aware rest of build 5 after 11-09, as assessed.

## Watchlist

- **Sunday 2026-11-01:** `league (real games): 6 matchup(s) recorded` beside `league: 6 matchup(s) recorded`.
- **Monday 2026-11-09:** the week-3 row of `report/accuracy.md` with both league Brier columns.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| real-games pre-week forecast (build 5, first slice) | **BUILT**, candidate only, first grade 11-09 | §1–§3 |
| build 5, context-aware remainder | **OPEN**, after 11-09 | §4 |

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
