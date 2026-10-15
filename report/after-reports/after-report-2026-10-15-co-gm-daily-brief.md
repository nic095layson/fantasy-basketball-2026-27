# After-report — 2026-10-15: Session 1 item 6 — the daily brief, run for 2026-10-21

**Owner request:** Session 1 item 6: "scripts/daily_brief.py: for today — the owner's players with games, the lineup by the daily-fill rule, the waiver scan (waiver_moves.py against league_state.json), streaming candidates by games remaining this week, title odds on the real schedule (10,000 seasons, two seeds, error stated). One markdown note. Run it for 10/21 and show the owner the note." The owner set the date as 10/21.

**What changed.**
- Kit: `scripts/co_gm.py` (the library: league-state rosters, the daily lineup, games left, the waiver scan lifted from `waiver_moves.py`, the simulator bridge), `scripts/daily_brief.py`, `scripts/test_daily_brief.py`, `report/briefs/brief_2026-10-21.md` and `.json`.
- No line, tag, team, price or placement changed. Nothing published.

**Method (stated to the owner before the run).**
- **Inputs:** NBA games from `games-2026-27.csv` (Basketball-Reference, built 9/30); lines v69; availability from `status_2026-10-15.json`.
- **Waiver scan:** the top 40 free agents by board value (inherited from `waiver_moves.py`, stated) × the owner's non-IL players. The top 3 distinct adds go to the simulator on seed 2026, 10,000 seasons, real schedule.
- **Title odds:** 10,000 seasons × seeds 2026 / 2027.

Pull window: 2026-10-15 → 2026-10-15 (the brief for 2026-10-21, built on the 2026-10-15 records; no web research — the sports hosts are denied).

## 1. Roster changes

None.

## 2. The note

# Daily brief — 2026-10-21 (week 1, 2026-10-20 to 2026-10-25)

Opponent this week: **DEVIN ELEVEN DOUBLES**. Rosters as of 2026-10-15 (owner's Yahoo page); statuses from `status_2026-10-15.json`; lines v69.

## Your players today

| player | NBA | game | status | availability | games left this week |
|---|---|---|---|---|---|
| Tyrese Haliburton | IND | @ NOP | — | 1.00 | 3 |
| Kevin Durant | HOU | vs DAL | Q | 0.50 | 3 |
| Kawhi Leonard | TOR | vs CHI | — | 1.00 | 3 |
| Jaden McDaniels | MIN | @ MIA | — | 1.00 | 3 |
| Miles Bridges | PHX | @ POR | Q | 0.50 | 2 |
| Yaxel Lendeborg | GSW | @ LAL | — | 1.00 | 3 |
| Kel'el Ware | MIL | @ WAS | — | 1.00 | 3 |
| Neemias Queta | BOS | — | — | 1.00 | 1 |
| Derrick White | BOS | — | — | 1.00 | 1 |
| Kyrie Irving | DAL | @ HOU | Q | 0.50 | 3 |
| Ty Jerome | MEM | vs UTA | — | 1.00 | 3 |
| PJ Washington | DAL | @ HOU | — | 1.00 | 3 |
| Christian Braun | DEN | — | — | 1.00 | 2 |

## Lineup (daily-fill rule)

- **PG** Ty Jerome
- **SG** Kevin Durant — Q, check before lock
- **G** Kawhi Leonard
- **SF** Jaden McDaniels
- **PF** Yaxel Lendeborg
- **F** Miles Bridges — Q, check before lock
- **C** PJ Washington
- **C** Kel'el Ware
- **Util** Tyrese Haliburton
- **Util** Kyrie Irving — Q, check before lock
- No game today: Neemias Queta, Derrick White, Christian Braun

## Waiver scan

8 of 520 add/drop pairs raise expected weekly category wins (base 5.147). Best three, checked in the simulator (seed 2026, 10,000 seasons, real schedule):
- Add **Draymond Green** (GSW), drop Christian Braun: +0.060 cats/week; title 24.75% (+2.57 vs 22.18%)
- Add **Bobby Portis** (MIA), drop Christian Braun: +0.027 cats/week; title 22.76% (+0.58 vs 22.18%)
- Add **Jrue Holiday** (POR), drop Christian Braun: +0.012 cats/week; title 23.25% (+1.07 vs 22.18%)

## Streaming (2026-10-21 to 2026-10-25)

Your weakest active player by board value is PJ Washington (-2.43 per game, 3 games left). Free agents with more games left, best per game first:
- none

## Title odds (real schedule)

- Title: 22.0% ± 0.6 (seeds 2026 / 2027: 22.18% / 21.90%; 10,000 seasons each)
- Playoffs: 98.9%

_Cannot see: news after the rosters/status paste; ESPN injuries (network-denied); minutes limits; other managers' pending claims. Q counts as a coin flip._


## 3. Verification

- **Tests, red first:**
  - `test_daily_brief_red.txt`: the module was missing.
  - `test_streaming_red.txt`: 7 tests, 1 error.
  - `test_daily_brief_green.txt`: 7 tests, 0 failing.
- **The lineup test was sharpened before any code existed:** the case is one that slot-order greedy loses (a PG/SG star plus four pure PGs: greedy starts 4, the matching starts 5).
- **Caught in my own review of the first run** (`brief_2026-10-21_first_run.md`):
  - **What was wrong:** the streaming list ranked by a value clamped at zero. Every free agent sits below the pool mean, so the list was in arbitrary order.
  - **Fix:** rank free agents with more games left than the owner's weakest active player by per-game value. Red-first.
  - **Result for 10/21:** no free agent has more games left this week than the weakest player, so the section correctly says "none".
- **Lineup:** 10 of the owner's non-IL players play on 2026-10-21, and 10 start.
- **Title odds:** 22.0% ± 0.6 (seeds 22.18% / 21.90%).

## Watchlist

- **The waiver result is the brief's one actionable item:**
  - **The pairs:** add Draymond Green for Christian Braun (+0.060 cats/week; title +2.57 points on one seed), add Bobby Portis for Christian Braun (+0.027 cats/week; title +0.58 points on one seed), add Jrue Holiday for Christian Braun (+0.012 cats/week; title +1.07 points on one seed).
  - **This is an open decision:** draft-night D-LD-2, defaulting to watching Green's first week.
  - **The +2.57-point figure is one seed;** a second seed confirms or shrinks it before anyone acts.
- The schedule file predates the Cup knockout dating (week 7); week 1 is unaffected.

## Open-item receipts

| item | query run (2026-10-15) | dated finding |
|---|---|---|
| (this item) | records only (league state, status file, schedule file); no web research (network-denied) | brief written |
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
- Automating the run at 9am ET (P1).
- Trades.

**In scope and unverified.**
- The brief runs on the 10/15 rosters and statuses. On 10/21 itself it needs a fresh paste to be current.

**What this cannot see.**
- News after the paste.
- ESPN injuries.
- Minutes limits.
- Other managers' pending claims.
- FAB budgets.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-LD-2 (carried) | Add Draymond Green for Christian Braun now, or watch week 1 | watch week 1; the brief re-scores it daily |
| D-S1-9 | Re-run the brief on 10/21 morning after a fresh rosters/status paste | yes, if you paste |
| earlier rows | carried in `OPEN.md` | carried |

## Provenance

This folder: `test_daily_brief_red.txt`, `test_streaming_red.txt`, `test_daily_brief_green.txt`, `brief_2026-10-21_first_run.md`, `rn_section.md`, this writer. Kit: `report/briefs/brief_2026-10-21.md`, `.json`.

## In plain language

The daily note works. For 10/21 it starts your ten players who have games. It flags Durant, Irving and Bridges as questionable to check before tip-off.

The waiver scan's best move is Draymond Green in for Christian Braun, worth about +2.6 points of title odds on one simulation run. That's still your call from draft night.

Your title odds on today's rosters are about 22%.
