# Structural bands on the season configuration, and same-day re-runs that keep earlier finals — 2026-10-26

Pull window: 2026-10-26 → 2026-10-26 (no new pull: the rosters and the season pool are the records branch `season/daily` at 5f95841, pinned beside the sweep as `league_state_2026-10-26.json` and `pool_season_2026-10-26.csv`; no web search, no market pull).

**Method up front.** Owner 2026-10-26: "re-measure the uncertainty ranges shown with the title odds now that they use the updated stats" and "same-day re-runs to keep earlier final results instead of replacing them". The sweep's method choices were stated before the run: M1 the 2026-10-26 rosters (IL excluded, as the brief) on the season pool (337 rows) with the season per-game variation; M2 the sweep's simulator draws pairings at random and starts each season 0-0, while the brief's odds use the real schedule with week 1 played — so the bands measure how far the odds move per constant on these rosters and lines, not the brief's exact level; M3 6,000 seasons × seeds 2026/2027 against 10,000-season `league_sim --verify --pool` references on the same state and pool, the baseline within 3 SE or the sweep fails; M4 the registry's declared bands and the 1/2-point tiers unchanged. EVIDENCE marks what a run or file showed; INFERENCE what is derived.

## 1. The season sweep (EVIDENCE, `redteam-2026-10-26-season/sweep.json`, deck f3e1d27)

Baseline title share 25.10 / 25.32 (seeds 2026 / 2027) against the 10k references 24.96 / 25.47: within 3 SE (0.54 points) on both seeds.

| constant | variant | shift, draft sweep (10-19, deck 048efb6) | shift, season sweep |
|---|---|---|---|
| BENCH_WEIGHT | bench weight 0.50 | +0.00 | +0.00 |
| BENCH_WEIGHT | bench weight 1.00 (F07's flip) | +0.00 | +0.00 |
| **BENCH_WEIGHT tier** | | **ROBUST** | **ROBUST** |
| PCT_MIX_INFL | binomial floor only (1.0) | +0.82 | +0.88 |
| PCT_MIX_INFL | inflation 1.30 | -1.28 | -0.68 |
| **PCT_MIX_INFL tier** | | **SENSITIVE** | **ROBUST** |
| TEAM_WEEK_SHOCK | no shared games shock (0.0) | +2.29 | +2.69 |
| TEAM_WEEK_SHOCK | shared games shock doubled (0.12) | -3.35 | -3.71 |
| **TEAM_WEEK_SHOCK tier** | | **FRAGILE** | **FRAGILE** |
| weekly_availability | no in-sim injury discount (risk 0.88 like healthy) | -2.00 | -5.12 |
| weekly_availability | harsher risk tier (0.65) | +0.75 | +3.69 |
| weekly_availability | healthy players play 0.95 of games | -1.46 | +1.00 |
| weekly_availability | healthy players play 0.80 of games | +0.95 | -1.48 |
| **weekly_availability tier** | | **FRAGILE** | **FRAGILE** |
| GAMES_PER_WEEK | 3.0 games per healthy week | -0.69 | -1.03 |
| GAMES_PER_WEEK | 4.0 games per healthy week | +0.63 | +1.01 |
| **GAMES_PER_WEEK tier** | | **ROBUST** | **SENSITIVE** |

The line the brief and the deck now quote, verbatim from `daily_brief.band_line()`:

> Structural band (season sweep (current rosters, season pool), deck f3e1d27): TEAM_WEEK_SHOCK is FRAGILE: +2.7 (no shared games shock (0.0)) / -3.7 (shared games shock doubled (0.12)); weekly_availability is FRAGILE: -5.1 (no in-sim injury discount (risk 0.88 like healthy)) / +3.7 (harsher risk tier (0.65)) / +1.0 (healthy players play 0.95 of games) / -1.5 (healthy players play 0.80 of games).

INFERENCE, not tested here: the availability constant moved most (−2.0 / +0.8 to −5.1 / +3.7, and the healthy-share variants changed sign), which is what a roster set with more players on the risk tiers would do; the draft sweep was on draft-day rosters before any injury. Which rosters carry them was not broken down (did not check). Nothing was tuned.

## 2. Same-day re-runs keep earlier finals (EVIDENCE)

`flaim_live.keep_daily`: a re-pin that carries some weeks keeps every week the earlier pin had and it lacks; a week both carry takes the newer copy; `carried_forward` names it ("matchups week 1"). Replayed on today's two real files (`season/daily` a221c73 then 5f95841): weeks 1 and 2 both kept, week 2 equal to the re-run's.

## 3. What was built (EVIDENCE)

- `scripts/redteam/sweep.py`: `--season LEAGUE_STATE POOL` builds the picks file and each seed's 10k reference beside `--out`; the record names the state and pool with their sha256; a missing reference is an error. Without it, the draft configuration as before.
- `daily_brief.SWEEP` and the deck's default sweep → `redteam-2026-10-26-season/sweep.json`; the band line names the configuration ("season sweep (current rosters, season pool)"). The draft record stays at `redteam-2026-10-19`.
- Tests, red first: `test_flaim_live` (1), `test_redteam_sweep.SeasonConfiguration` (3), `test_daily_brief.SeasonBand` (2), `test_season_deck.SeasonBandDeck` (2). Full kit suite: every file OK.

## 4. Bounds

**Out of scope by design.** No projection line, injury tag, roster or engine constant changed. **In scope and unverified.** The real schedule and the played week are not in the sweep (M2). The bands belong to the 2026-10-26 rosters; rosters change daily, and when to rerun the sweep is the owner's call (§5).

## 5. Next steps (owner decisions)

1. Merge this PR; tomorrow's brief and deck quote the season bands.
2. When to rerun the season sweep: on demand, weekly (Monday after the intake), or on a roster change.
3. Whether to build the sweep through the real-schedule simulator (M2), so the bands sit on the brief's exact configuration.

## Watchlist

- **Tomorrow's brief:** "Structural band (season sweep (current rosters, season pool), deck …)".
- **Next same-day re-run:** its pin lists `carried_forward: ["matchups week N"]` when the re-run lacks a week the first run had.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| bands measured on the draft configuration | **FIXED**, season sweep | §1 |
| same-day re-run dropping week 1's finals | **FIXED** | §2 |
| brief header "lines v69" | **OPEN**, owner decision (from #201) | — |

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
