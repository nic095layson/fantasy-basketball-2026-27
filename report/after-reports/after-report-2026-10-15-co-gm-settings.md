# After-report — 2026-10-15: Session 1 item 2 — the league's settings and schedule, read from the league; the simulator corrected to 17 weeks and a reseeded bracket

**Owner request (2026-10-15):** Session 1 item 2 — settings and schedule from the owner, `league_settings.json` / `league_schedule.json`, `test_settings.py` failing on any divergence, `league_sim.py --schedule`. Owner inputs: the settings PDF and the rosters PDF (uploaded 2026-10-15, pinned in `data/source/`), then in chat, verbatim: "Correct, weeks 18-20 and ends March 21, 2027." with the 17-opponent list and "Merge" (`data/source/owner-matchup-schedule-2026-10-15.md`).

**What changed.**
- Kit: `data/league_settings.json`, `data/league_schedule.json`, `scripts/test_settings.py`, `scripts/test_schedule.py`.
- Kit: `report/schedule/build_schedule.py` gets playoff weeks (18, 19, 20), plus a `--games` re-bucket mode with no fetch. Its per-week file changes only the two playoff-window columns: 28 shared columns, 0 rows differ.
- Deck: `arena.WEEKS` 17, `arena.playoff_champion` reseeded (new `arena.reseed`), `league_sim.py` reseeded plus `--schedule`, and the `test_bracket.py` docstring.
- No line, tag, team, price or placement changed. Nothing published.

**Method (stated to the owner before the run).**
- A1: reseeding means the best remaining seed meets the worst. This is assumed; the owner has not confirmed it.
- A2: only the owner's 17 opponents are known. The other ten teams are paired at random each week.
- A3: weeks 7 and 17 are 14-day matchups on Yahoo's calendar. The simulator treats them as single weeks.
- A4: the re-grade uses the rosters as drafted (state `draft_state_100.json`, tag v69), so it is comparable with draft night.
- Runs: 10,000 seasons each, seeds 2026 and 2027 (draft night's seeds).

Pull window: 2026-10-15 → 2026-10-15 (owner settings, rosters and schedule; no roster pull, no web research).

## 1. Roster changes

None applied. The rosters PDF is pinned for item 5 and has not been parsed here.

## 2. What the league's page said that the model had wrong

| setting | league page | model before | test |
|---|---|---|---|
| regular-season weeks | 17 (playoffs weeks 18, 19, 20, end 2027-03-21) | 18 | `test_regular_season_weeks` |
| playoff window in the schedule builder | weeks 18, 19, 20 | weeks 19, 20, 21 (D-G5, "confirm on the settings page") | `test_playoff_weeks_in_the_schedule_builder` |
| playoff reseeding | yes | fixed bracket | `test_playoff_reseeding` |

EVIDENCE:
- `test_settings_red.txt`: 8 tests, 3 failing (test_playoff_reseeding, test_playoff_weeks_in_the_schedule_builder, test_regular_season_weeks).
- `test_settings_green.txt`: 8 tests, 0 failing.
- `test_schedule_red.txt`: 3 tests, 1 failing. `league_sim` ignored `--schedule` and wrote no schedule record.
- `test_schedule_green.txt`: 3 tests, 0 failing.

Settings that already matched: 12 teams, 8 playoff teams, the nine categories, the ten starting slots, and 13 active roster spots.

## 3. The schedule

The owner's opponents by week, with managers resolved to draft seats through the draft board: 1 Cayas, 2 Oblena, 3 Kevin, 4 Will, 5 Hegi, 6 Robby, 7 Noah, 8 John, 9 Martin, 10 JCo, 11 Kyle, 12 Cayas, 13 Oblena, 14 Kevin, 15 Will, 16 Hegi, 17 Robby. Weeks 18, 19, 20 are playoffs. Every other team appears, and the owner's seat never plays itself (`test_schedule.py`).

## 4. The league grade, re-stated

Seat 10, rosters as drafted on 10/14, 10,000 seasons per seed. Error is the 95% binomial interval on the two-seed mean.

| model | weeks | title s2026 / s2027 | title, mean | playoffs s2026 / s2027 | playoffs, mean | title rank |
|---|---|---|---|---|---|---|
| 18 weeks, fixed bracket (draft night, on file) | 18 | 22.50 / 21.84 | 22.17 ± 0.58 | 98.87 / 98.82 | 98.84 ± 0.15 | 1 / 1 |
| 17 weeks, reseeded, random pairings | 17 | 21.10 / 21.33 | 21.21 ± 0.57 | 98.67 / 98.73 | 98.70 ± 0.16 | 1 / 1 |
| 17 weeks, reseeded, the real schedule | 17 | 21.81 / 21.60 | 21.70 ± 0.57 | 98.99 / 98.92 | 98.95 ± 0.14 | 1 / 1 |

`--verify` on the corrected model, both seeds: "verify: champions and playoff counts equal arena.simulate_seasons on seed 2026 for all 12 teams" and "2027 for all 12 teams". In plain terms, the reseeded `league_sim` equals `arena.simulate_seasons` draw for draw. The schedule runs change the draw order, so they cannot be verified that way. Their check is that the owner met the listed opponent in all 340,000 simulated weeks (`honored` in each record).

**Reading.**
- Correcting the season shape moves the title share from 22.17% to 21.21%.
- The real schedule moves it to 21.70%.
- Each shift is about the size of the ±0.57-point error, so the honest reading is that the title share is still about 21–22%, and still rank 1.
- INFERENCE: one week fewer gives the regular season less room for the stronger roster to separate. The schedule's random pairings for the other ten teams (A2) limit what its arm can say.

## Watchlist

- A1 (reseed semantics) and A2 (others' pairings) are on `OPEN.md`. If the owner can share the full league schedule, A2 goes away.
- D-S1-2: the two 14-day matchups (weeks 7 and 17) are not modelled as double-length.

## Open-item receipts

| item | query run (2026-10-15) | dated finding |
|---|---|---|
| (this item) | owner inputs only; no web research and no roster pull | settings and schedule pinned; pool unchanged |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this item (did not check) |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 beb243ef57af), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 33 of 33 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 32 of 33 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 23 of 33 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 14 of 33 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 33 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| John Collins | 12 of 33 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 11 of 33 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 10 of 33 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 10 of 33 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 7 of 33 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 6 of 33 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 33 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 33 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (17 mocks, value 27, market 45); Lauri Markkanen (15 mocks, value 21, market 37); Tyrese Haliburton (13 mocks, value 7, market 12); Tyrese Maxey (11 mocks, value 5, market 9); Kel'el Ware (10 mocks, value 57, market 77); Tyler Herro (9 mocks, value 51, market 69); Karl-Anthony Towns (8 mocks, value 12, market 15); Miles Bridges (5 mocks, value 96, market 98).

The section above is item 1's pasted output of the deck's `repeat_market_check.py` from earlier today, carried over. The page and the lines are unchanged since then; the arena changes do not touch the page engine. The gate replays it again.

## Bounds

**Out of scope by design.**
- No change to projections, the page, or the in-season dynamics (B3).
- The schedule's 14-day weeks (D-S1-2).

**In scope and unverified.**
- A1, the reseed rule: assumed, not confirmed by the owner.
- The settings transcription beyond the confirmed playoff fields: read from the page images, not individually confirmed.

**What this cannot see.**
- Every pick, add and drop since the draft (item 5).
- The other teams' real pairings.
- Whether the season model is calibrated. It is verified against itself, not against outcomes; item 7 starts that.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-S1-2 | Model weeks 7 and 17 as double-length matchups | not modelled; P1 with B3 |
| D-S1-3 | Send the full league schedule, so that all 12 teams' pairings are real | random pairings for the other ten |
| D-G5 | Playoff window | CLOSED: weeks 18–20 per the settings page and the owner |
| earlier rows | carried in `OPEN.md` | carried |

## Provenance

- This folder: `test_settings_red.txt`, `test_settings_green.txt`, `test_schedule_red.txt`, `test_schedule_green.txt`, `sim_w17r_s2026.log`, `sim_w17r_s2027.log`, `sim_w17r_sched_s2026.log`, `sim_w17r_sched_s2027.log`, `rn_section.md`, this writer.
- Deck: `arena/results/m100_league_sim_10k_s{2026,2027}{_w17r,_w17r_sched}.json` (new) and the draft-night `m100_league_sim_10k_s{2026,2027}.json` (unchanged).
- Owner inputs: `data/source/yahoo-league-settings-2026-10-15.pdf`, `data/source/yahoo-starting-rosters-2026-10-20-view.pdf`, `data/source/owner-matchup-schedule-2026-10-15.md`.

## In plain language

Your league's settings page caught two mistakes in the simulator. It was playing 18 regular-season weeks instead of 17, and it ignored the reseeding after round one. Both are fixed, each with a test that failed before the fix and passes now.

The simulator now also plays your actual opponent each week. With all of that, your title chance on the roster you drafted is about 22% (was 22%), still the best in the league on this model.
