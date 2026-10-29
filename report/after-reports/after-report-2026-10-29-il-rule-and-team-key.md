# The IL rule's effect on the title share, and league steps keyed on the Yahoo team key (owner picks, 2026-10-29)

Pull window: 2026-10-29 → 2026-10-29 (no pull: the 10-29 morning records on season/daily 934de05, read only; kit main deccaf2, deck main 55d8e3f).

**Method up front.** The Runner's 10-29 after-report raised two decisions. The owner picked "Measure it first" (A, assessment only) and "Key on Yahoo team key" (B, code). The method parameters below were stated to the owner before the runs. EVIDENCE marks what a run or read showed; INFERENCE marks what is derived.

**Verdict: the IL rule (D-IS-8) is the drop. On today's inputs, Haliburton counted as active on a legal 13-man roster gives 28.5%, against 15.6% with him on IL: −12.9 points. B is fixed: both league steps PASS on today's data.**

## 1. A: D-IS-8 measured (EVIDENCE: dis8.json, dis8_noportis.json)

Parameters: the 10-29 morning league state (`data/news/league_state_am_2026-10-29.json`) and the 10-29 season pool, seeds 2026 and 2027 × 10,000 seasons, real schedule, through the brief's own `co_gm.run_league_sim`. One change per run; Kawhi Leonard stays on IL throughout.

| roster for seat 10 | title (2026 / 2027) | mean | playoffs |
|---|---|---|---|
| as stored: Haliburton IL, Portis active (the brief) | 15.00 / 16.27 | **15.6** | 96.1 |
| Haliburton active, Portis dropped (legal 13) | 28.06 / 28.99 | **28.5** | 99.8 |
| Haliburton active and Portis kept (14 active: not a legal Yahoo roster) | 49.36 / 49.54 | 49.5 | 100.0 |

- Run 1 reproduces the brief's 15.0 / 16.27 to the digit, so the harness is the brief's.
- Sampling error: about ±0.4 per figure (one 10,000-season run); the two seeds agree within 1.3.
- INFERENCE: between the 10-28 brief's 32.6 and today's 28.5 (both Haliburton active, no Portis), about −4 comes from the 10-29 line moves and other rosters. The IL rule accounts for the rest of the overnight drop.
- **The honest range for "Haliburton out indefinitely" is 15.6 (never returns) to 28.5 (healthy all season).** The brief shows only the floor. Neither end is a forecast of his return.
- **A second finding, not asked:** with Haliburton active, keeping Portis as a 14th active player adds +21 points. The simulator rewards an extra body heavily, so any roster count above Yahoo's limit inflates the title share. INFERENCE: this cannot happen in a real state, since Yahoo enforces the limit, but a hand-built what-if roster can trip it. Recorded here, not acted on.
- D-IS-8 is not in the registry's swept set, so the brief's structural band (TEAM_WEEK_SHOCK, weekly_availability) does not bound this effect.

## 2. B: league steps keyed on the team, not the name (EVIDENCE)

| step | before | after |
|---|---|---|
| league_pairings | matched Yahoo's pinned week pins by team name: FAIL, "team 'Giavaris Jamal Javarison-Lamar' is not in the league state" | matches by Yahoo team key, mapped to today's name from the newest pinned pull, then to the seat; falls back to the name when a pin has no key |
| league_table | matched week_N.json scores by team name: FAIL, "no yahoo_score for ['ANONG NANGIANNIS?!']" | matches by seat |

- Tests: 3 new, red first (3 of 3 failed before the change), now pass; test_league_pairings, test_league_table and test_morning: 51 OK.
- Behavioral check (scratch copy of season/daily 934de05 with this diff): `LEAGUE PAIRINGS: PASS — 17 weeks of pairings for all 12 teams, owner opponents match, 1 week(s) played`; `LEAGUE TABLE: PASS — 2026-10-29: week 2 … Yahoo W-L-T matches the kit's finished weeks for 12 teams`. The rewritten schedule differs from the stored one only in its seat_map label: pairings and played records are identical.
- Why the pull: the league state carries no team key, and its seats come from roster overlap with the draft. The newest pinned pull's rosters carry key and name from the same morning pull the state was built from.

Runner impact: code-only (the morning's two existing steps PASS on the next run; no prompt changes).

## 3. Bands quoted

Every title share above carries the standing structural band (season sweep 2026-10-26, real schedule):
- **TEAM_WEEK_SHOCK is FRAGILE:** +2.7 (no shared games shock (0.0)) / -4.2 (shared games shock doubled (0.12)).
- **weekly_availability is FRAGILE:** -5.4 (no in-sim injury discount (risk 0.88 like healthy)) / +3.7 (harsher risk tier (0.65)) / +0.4 (healthy players play 0.95 of games) / -0.5 (healthy players play 0.80 of games).

## 4. Bounds and open decisions

**Out of scope by design.** No engine rule, tag, line or roster changed. Haliburton's timeline was not researched.

**In scope and unverified.** The deck's League tab under yesterday's FAIL (the Runner's NOT-ATTEMPTED) is moot once the step PASSes; not checked.

Open decisions for the owner: what to do with D-IS-8 now that it is measured (return on ESPN's date, show both ends, or keep the floor); whether the roster-count sensitivity needs a guard.

## Watchlist

- 10-30 morning: LEAGUE PAIRINGS and LEAGUE TABLE PASS.
- Haliburton news: a return date turns the 15.6–28.5 range into a figure.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| D-IS-8 effect on the title | **MEASURED**: −12.9 on a legal roster | §1 |
| Name-keyed league steps | **FIXED** in code | §2 |
| Roster-count sensitivity (+21 for a 14th active) | **NEW**, owner decision | §1 |

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
