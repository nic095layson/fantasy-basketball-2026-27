# The structural bands on the real schedule, re-measured every Monday — 2026-10-26

Pull window: 2026-10-26 → 2026-10-26 (no new pull: the rosters and season pool are the ones pinned in `redteam-2026-10-26-season/` from the records branch at 5f95841; the schedule is kit main's `data/league_schedule.json`, pairings for weeks 1–17 and week 1 played; no web search, no market pull).

**Method up front.** Owner 2026-10-26: "Build it" for the real-schedule re-measurement and for re-measuring every Monday. Stated before the run: the same pinned rosters and pool as the morning's season record, plus the league schedule; 6,000 seasons × seeds 2026/2027; the reference a plain 10,000-season `league_sim` run on the same inputs (its `--verify` cannot run with a schedule), the baseline within 3 SE or the run fails. EVIDENCE marks what a run showed; INFERENCE what is derived.

## 1. The real-schedule sweep (EVIDENCE, `redteam-2026-10-26-season-real/sweep.json`, deck cbfb422)

Baseline title share 25.55 / 24.63 against the 10k references 25.46 / 25.19: within 3 SE (0.54) on both seeds. Ran in about one minute (21:39:32 → 21:40:33 UTC, 4 workers).

| constant | variant | shift, practice schedule (this morning) | shift, real schedule |
|---|---|---|---|
| BENCH_WEIGHT | bench weight 0.50 | +0.00 | +0.00 |
| BENCH_WEIGHT | bench weight 1.00 (F07's flip) | +0.00 | +0.00 |
| **BENCH_WEIGHT tier** | | **ROBUST** | **ROBUST** |
| PCT_MIX_INFL | binomial floor only (1.0) | +0.88 | +0.73 |
| PCT_MIX_INFL | inflation 1.30 | -0.68 | -0.24 |
| **PCT_MIX_INFL tier** | | **ROBUST** | **ROBUST** |
| TEAM_WEEK_SHOCK | no shared games shock (0.0) | +2.69 | +2.68 |
| TEAM_WEEK_SHOCK | shared games shock doubled (0.12) | -3.71 | -4.22 |
| **TEAM_WEEK_SHOCK tier** | | **FRAGILE** | **FRAGILE** |
| weekly_availability | no in-sim injury discount (risk 0.88 like healthy) | -5.12 | -5.39 |
| weekly_availability | harsher risk tier (0.65) | +3.69 | +3.72 |
| weekly_availability | healthy players play 0.95 of games | +1.00 | +0.42 |
| weekly_availability | healthy players play 0.80 of games | -1.48 | -0.45 |
| **weekly_availability tier** | | **FRAGILE** | **FRAGILE** |
| GAMES_PER_WEEK | 3.0 games per healthy week | -1.03 | -0.81 |
| GAMES_PER_WEEK | 4.0 games per healthy week | +1.01 | +0.98 |
| **GAMES_PER_WEEK tier** | | **SENSITIVE** | **ROBUST** |

The line the brief and the deck quote from tomorrow, verbatim from `daily_brief.band_line(date="2026-10-27")`:

> Structural band (season sweep of 2026-10-26 (current rosters, season pool, real schedule), deck cbfb422): TEAM_WEEK_SHOCK is FRAGILE: +2.7 (no shared games shock (0.0)) / -4.2 (shared games shock doubled (0.12)); weekly_availability is FRAGILE: -5.4 (no in-sim injury discount (risk 0.88 like healthy)) / +3.7 (harsher risk tier (0.65)) / +0.4 (healthy players play 0.95 of games) / -0.5 (healthy players play 0.80 of games).

INFERENCE: the two FRAGILE constants and their size hold on the real schedule (the shared shock's downside −3.7 → −4.2; the injury discount −5.1 → −5.4); the healthy-share variants shrink to under half a point and games-per-week returns to ROBUST.

## 2. What was built (EVIDENCE)

- **Deck** (`yahoo-fantasy-basketball`, branch `claude/sim-patches-2026-10-26`): `arena/patches.py` holds the four patch kinds, moved verbatim from the kit's sweep; `league_sim --patch FILE` applies one before SEASON_CV is read and names it in the record; `--verify` checks a patched run against `arena.simulate_seasons` patched the same way. Without `--patch` the output is byte-identical to main's (`cmp`). `arena/test_patches.py` (8, red first; one assertion widened from one seat's share to every team's season after a 200-season tie).
- **Kit sweep:** patches come from the deck module — the 13 draft variants are identical before and after at seed 2026, 300 seasons. `--real-schedule SCHEDULE` (with `--season`) runs every variant through `league_sim`; inputs (league state, pool, schedule) are pinned beside the record and read from there. `test_redteam_sweep.RealSchedule` (3) was written **after** the code, then shown failing on the old code (3 errors) and passing on the new — not red-first, said so.
- **Monday step:** `morning.py` adds a non-fatal "season sweep" on Mondays after league pairings and before the brief, writing `redteam-<date>-season/` on the real schedule (`test_morning.MondaySweep`, 2, red first).
- **Newest record:** `scripts/sweep_record.py` — the newest season record on or before the day (a same-day `-season-real` record wins; a Monday with no record keeps the last; before the first, the draft sweep). `daily_brief.band_line` and the deck read it and name date and configuration (`test_sweep_record`, 6, red first; its tie test caught a real ordering bug, fixed).
- Suites: kit every file OK; deck every `arena/test_*.py` OK.

## 3. Bounds

**Out of scope by design.** No projection line, injury tag, roster or engine constant changed. **In scope and unverified.** The Monday step has not run in the real morning yet (first: 2026-11-02); its command was exercised here with the pinned inputs, not the records branch's live files. The runner's core count is unknown (did not check); at one core the run would take roughly four times as long.

## 4. Next steps (owner decisions)

1. Merge the deck PR, then the kit PR (the kit's real-schedule mode calls `league_sim --patch`).

## Watchlist

- **Tomorrow's brief:** "Structural band (season sweep of 2026-10-26 (current rosters, season pool, real schedule), …)".
- **Monday 2026-11-02:** a `season sweep` step line `SWEEP: … baseline within 3 SE …: {'2026': True, '2027': True}` and a new `redteam-2026-11-02-season/` folder; the brief names 2026-11-02.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| real-schedule re-measurement | **BUILT**, run | §1, §2 |
| Monday re-measurement | **BUILT**, first run 2026-11-02 | §2, §3 |
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
