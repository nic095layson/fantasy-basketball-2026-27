# After-report — 2026-10-15: Session 1 item 5 — the league's current state from the owner's rosters page; data/league_state.json

**Owner request:** Session 1 item 5 (rosters, standings, scoreboard → `data/league_state.json`, names resolved 100% to the pool, halt on any miss). Owner input: the rosters PDF uploaded 2026-10-15. On the halt, the owner said: "Convene council to decide and proceed with their recommendations." Then "Proceed".

**What changed.**
- Kit: `data/source/yahoo-starting-rosters-2026-10-20-view.transcribed.csv` (164 rows), `scripts/league_intake.py`, `scripts/test_league_intake.py`, `data/unpooled_il.json`, `data/league_state.json`.
- No line, tag, team, price or placement changed. Nothing published.

**Method (stated before the run).**
- **Transcription.** The PDF has no text layer and no OCR engine is installed. Each page was rendered at 250 dpi, and every team column was read from the image.
- **Resolution, in order:**
  1. The deck's name fold.
  2. Yahoo's abbreviations as recorded on the 10/14 draft board.
  3. Nothing else: any other miss halts the intake.
- **Seats.** Each team gets the draft seat whose 13 picks overlap its roster most, and the match must be unique.
- **Standings and scoreboard.** None exist before week 1, which starts 2026-10-20.

Pull window: 2026-10-15 → 2026-10-15 (the owner's rosters page as of its Tue Oct 20 view; no web research — the environment denies the sports hosts, see item 3).

## 1. Roster changes

No pool row changed. League-roster moves since the draft, read from the page:

| seat | manager | fantasy team | draft picks still rostered | added since draft | dropped | empty slots |
|---|---|---|---|---|---|---|
| 1 | Oblena | Itsy Bitsy Spida | 13 of 13 | none | none | none |
| 2 | Noah | Devin Minutes in Heaven | 13 of 13 | Zaccharie Risacher | none | C |
| 3 | Will | Lauri's Prime Rib | 13 of 13 | Mark Williams, Maxime Raynaud | none | none |
| 4 | Robby | Booker T Floppers | 13 of 13 | none | none | none |
| 5 | Kyle | Giavaris Jamal Javarison-Lamar | 13 of 13 | none | none | none |
| 6 | Martin | Cade n em | 13 of 13 | Y. Konan Niederhäuser (unpooled IL) | none | none |
| 7 | John | John's Cool Team | 13 of 13 | none | none | none |
| 8 | JCo | Splash Mountain | 13 of 13 | none | none | none |
| 9 | Kevin | Podz save the league | 13 of 13 | none | none | none |
| 10 | Me | JAMAL AL-QUETA | 13 of 13 | Max Strus | none | none |
| 11 | Cayas | DEVIN ELEVEN DOUBLES | 13 of 13 | Bradley Beal | none | none |
| 12 | Hegi | Thompson Telepathy | 13 of 13 | Wendell Carter Jr. | none | none |

## 2. The halt and the Council's decision

- **First run:** `Y. Konan Niederhäuser (Cade n em, IL, LAC, status O)`. The intake halted and wrote nothing (`intake_run_1.txt`).
- **Council (owner-convened, 4–1):** carry the player as an IL-only exception in `data/unpooled_il.json`, with no projection line, rather than writing a pool row from memory or with no source. He is on IL, so he contributes nothing to the lineup.
- **Red first:**
  - `test_league_intake_red.txt`: ModuleNotFoundError — the intake module did not exist.
  - `test_unpooled_red.txt`: 6 tests, 2 errors.
  - `test_league_intake_green.txt`: 6 tests, 0 failing. This includes the test that the same name in a BN slot still halts.
- **Second run:** `LEAGUE INTAKE: PASS — 12 teams, 162 players, 162 of 162 resolved; 0 NBA-team disagreement(s) with the pool; wrote data/league_state.json`

**Cross-checks that came free (EVIDENCE):**
- Every team keeps all 13 of its draft picks, so each maps to exactly one seat.
- Yahoo's NBA team equals the pool's team for all 162 pooled players (0 disagreements). This also checks the transcription.

**Status letters on the page:** {'Q': 46, 'O': 7}. The owner's flagged players: Kevin Durant Q, Miles Bridges Q, Kyrie Irving Q, Max Strus O.

## 3. The owner's question: the predicted head-to-head (an assessment, not a build)

- **Asked:** "what is my predicted head to head result each week, based on your rosters and calculations as of today?"
- **Method (stated before the run):**
  - non-IL players from this league state, on the v69 lines;
  - `arena.team_week_model` and the house simulator's weekly draw;
  - 10,000 matchups per week on seeds 2026 and 2027, against the owner's real schedule.
- **Records:** `h2h_assessment.py`, `h2h_assessment_2026-10-15.json`.
- **Result:** favored in all 17 weeks, P(win) from 54% to 79%. Expected regular-season wins: 11.1 of 17.
- **Not modelled:** Q statuses, streaming, injuries after today, and the two 14-day weeks. Item 7 records week 1's prediction formally before the week.

## Watchlist

- Niederhäuser's exception ends when he gets a sourced pool row; the file says so.
- The standings and scoreboard fields stay `null` until week 1 has results to read.

## Open-item receipts

| item | query run (2026-10-15) | dated finding |
|---|---|---|
| (this item) | owner rosters page only; no web research (sports hosts denied by the environment) | league state written; pool unchanged |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried (did not check; the network is blocked) |

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

The section above is today's output of the deck's `repeat_market_check.py`, carried from item 1; the page is unchanged. The gate replays it again.

## Bounds

**Out of scope by design.**
- No pool rows were added.
- The other teams' standings are not modelled.

**In scope and unverified.**
- The transcription is the agent's reading of page images. It agrees with the pool on every NBA team and every draft pick, but statuses and slots have no second reader.

**What this cannot see.**
- Anything on Yahoo after the page was captured.
- FAB budgets.
- Pending waiver claims.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-S1-4 | Add a sourced pool row for Yanic Konan Niederhäuser once the network allows | keep the IL-only exception |
| D-S1-5 | Paste the rosters again before each Monday preview (weekly), or only on change | weekly |
| earlier rows | carried in `OPEN.md` | carried |

## Provenance

- This folder: `test_league_intake_red.txt`, `test_unpooled_red.txt`, `test_league_intake_green.txt`, `intake_run_1.txt`, `intake_run_2.txt`, `preview_state_without_niederhauser.json`, `h2h_assessment.py`, `h2h_assessment_2026-10-15.json`, `rn_section.md`, this writer.
- Item 3's blocker receipts are in `co-gm-s1-provenance-2026-10-15/`.

## In plain language

Every team's roster is now on file. All 162 players match our database, except one injured rookie who is parked as an exception.

Everyone still has all the players they drafted. The only pickups so far are bench and injured-list adds; yours is Max Strus.

On today's rosters you're favored every week, with an expected record of about 11–6.
