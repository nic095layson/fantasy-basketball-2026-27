# After-report — 2026-10-15: Session 1 item 7 — the weekly preview and the calibration ledger, week 1 recorded before the week

**Owner request:** Session 1 item 7: "scripts/weekly_preview.py (the real opponent, category by category) and calibration.md/calibration.json with week 1's predicted category-win probabilities recorded before the week." The owner said "Proceed".

**What changed.**
- Kit: `scripts/weekly_preview.py`, `scripts/test_weekly.py`, `report/previews/week_01.md`, `report/calibration.json`, `report/calibration.md`.
- No line, tag, team, price or placement changed. Nothing published.

**Method (stated to the owner before the run, as the 2026-10-15 assessment).**
- Non-IL rosters from the league state, on lines v69.
- `arena.team_week_model` with the house simulator's weekly draw.
- 10,000 matchups × seeds 2026 / 2027.

Pull window: 2026-10-15 → 2026-10-15 (records only; no web research).

## 1. Roster changes

None.

## 2. Week 1, recorded 2026-10-15T20:26:51Z (the week starts 2026-10-20)

# Week 1 preview — vs DEVIN ELEVEN DOUBLES (Cayas), 2026-10-20 to 2026-10-25

P(win the week): **60.6%** (seeds 2026 / 2027: 0.605 / 0.607; ±0.7 points). Expected categories: 4.94 of 9.

| category | you (weekly mean) | them | P(you win) |
|---|---|---|---|
| FG% | 0.491 | 0.463 | 78% |
| FT% | 0.830 | 0.844 | 40% |
| 3PTM | 69.8 | 77.3 | 29% |
| PTS | 648.6 | 705.4 | 28% |
| REB | 220.4 | 199.6 | 75% |
| AST | 142.5 | 165.7 | 18% |
| ST | 41.0 | 42.3 | 44% |
| BLK | 30.4 | 20.6 | 95% |
| TO | 64.3 | 78.8 | 88% |

_Rosters as of 2026-10-15; lines v69; Q/O statuses not applied to the weekly model; a two-week matchup (weeks 7, 17) is modelled as one week._


## 3. Verification

- **Tests, red first:** `test_weekly_red.txt` (module missing), then `test_weekly_green.txt` (3 tests, OK).
- **What the tests prove:** a recorded week cannot be rewritten; a prediction dated on or after the week's start is refused; the Brier arithmetic is checked against a hand-written formula.
- **The real ledger, driven red:** recording week 1 a second time returns `LedgerError: week 1 is already recorded (2026-10-15T20:26:51Z); the ledger is append-only` (`record_week1_again_refused.txt`).
- **Agreement with the owner's earlier assessment:** week 1's per-seed P(win) equals `h2h_assessment_2026-10-15.json` exactly: True. Same method, same seeds.

## Watchlist

- **Score week 1 after Sunday 10/25:** `weekly_preview.py --score 1 --won "<the categories won>"` from the owner's scoreboard paste.
- **Week 1 is six days (Oct 20–25), but the model's weekly means are a standard week.** Category win probabilities depend on both sides alike, so the effect is second-order. The ledger will show it.

## Open-item receipts

| item | query run (2026-10-15) | dated finding |
|---|---|---|
| (this item) | records only | week 1 recorded |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried (network blocked) |

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

The section above is carried from item 1's run today; the page is unchanged, and the gate replays it.

## Bounds

**Out of scope by design.**
- Player-level projected-vs-actual lines (plan B6's second half, P1).
- Monthly reports.

**In scope and unverified.**
- Q/O statuses are not applied to the weekly model.
- The short week 1 is modelled as a full week.

**What this cannot see.**
- Lineup moves.
- Streaming.
- Injuries during the week.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-S1-10 | Paste week 1's final scoreboard on 10/26 so the ledger can score it | requested |
| D-S1-11 | Apply status tiers to the weekly model (P1, with B3) | P1 |
| earlier rows | carried in `OPEN.md` | carried |

## Provenance

This folder: `test_weekly_red.txt`, `test_weekly_green.txt`, `record_week1.txt`, `record_week1_again_refused.txt`, `rn_section.md`, this writer.

## In plain language

Before week 1 begins, the system has written down its prediction: a 61% chance you beat Cayas, winning blocks, turnovers, field-goal % and rebounds and losing assists, points and threes. That record is locked, so it can't be changed after the fact.

When you send the final scoreboard, it grades itself. That's the first test of the model against real games rather than against itself.
