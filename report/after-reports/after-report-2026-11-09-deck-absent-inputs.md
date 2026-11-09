# Silent missing inputs, and what "not simulated" really means (owner pick B1, 2026-11-09)

Pull window: 2026-11-09 → 2026-11-09 (no pull: data/league_state.json, data/season/pool_season.csv, data/season/season_lines_2026-11-09.json and report/season/deck_record_2026-11-0*.json on season/daily read only at 85556cc; kit main 8f252a2, deck main e14cc42).

**Method up front.** Order: runner after-report `after-report-2026-11-09-runner-window.md`, pick B1, three parts. (1) The SEASON DECK PASS line names absent inputs, and an empty card whose input was absent says why. (2) Auto-row players are no longer called "not simulated", but only after tracing whether `run_league_sim` includes them; if it does not, stop and report before changing any label. (3) A one-line comment on what `absent_from_sim` counts, with no change in behaviour. Method parameters: an input is absent when the build names its path and the file does not exist (the record's existing `present: false`). EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: parts 1 and 3 built and tested. Part 2 STOPPED as the order directs: the trace shows `run_league_sim` does not include auto-row players, so "not simulated" is still true of them. Only "not in the pool" is stale. No label was changed. The decision is the owner's (§3).**

## 1. Part 1: absent inputs are named (EVIDENCE: the diff, the suite)

| | before | after |
|---|---|---|
| PASS line, 11-09 morning (league record absent) | `SEASON DECK: PASS — … pins N inputs; render: 7 tabs, 0 page errors` | `… render: 7 tabs, 0 page errors; absent: league` |
| Week tab Scorecard / Forecast accuracy / Start-sit cards with their record absent | "No week scored yet …" / "No week graded yet …" / "No start/sit day on the ledger yet …" (the same text as a real empty week) | "Empty: calibration_daily.json was absent this morning (the step that writes it did not run, or failed)." and the same for accuracy.json and lineup_scorecard.json |
| League, Movers, Week-categories cards with their record absent | already say "(… did not run, or failed, this morning)" | unchanged |

- `scripts/season_deck.py` — page data `absent_inputs`, `absentWhy(k, file)` for the three cards above, and the PASS line suffix `; absent: <keys>` from the record's `present: false` inputs.
- How often it fires (EVIDENCE: deck records 11-01 … 11-09, am and pm): absent inputs on 3 of 17 builds — `yahoo_pull` 11-04, `lineup` 11-05 pm, `league` 11-09.
- `scripts/test_season_deck.py` — class `AbsentInputs`: absent `league` and `scores` show in the PASS line, nothing absent adds nothing, and three absent records give three "was absent this morning" cards.

Red first (EVIDENCE): before the change, `AbsentInputs` gave 1 failure (`'; absent: league, scores' not found in 'SEASON DECK: PASS — …'`) and 1 error (`KeyError: 'absent_inputs'`). After, 3 OK.

## 2. Part 2: the trace (EVIDENCE: the code and the 11-09 records)

```
league_live → league_intake.run(pool = deck pool + data/pool_additions.csv)
   ├─ teams[].players   ← every rostered player that pool has
   └─ teams[].unpooled  ← the rest: Meleek Thomas, Nolan Traore, Morez Johnson Jr., Mario Hezonja, Danny Wolf
season_lines.auto_rows → data/season/pool_season.csv gains a row for all five (season_lines_2026-11-09.json auto_rows ×5)
daily_brief.py:199  ros = co_gm.rosters(state, by)       ← co_gm.py:53-58 reads teams[].players only
daily_brief.py:256  co_gm.run_league_sim(ros, …)        ← the five never reach ros, so they are not simulated
```

Read on the 11-09 records: each of the five has a `pool_season.csv` row (True ×5) and none is in any `teams[].players` (False ×5).

So of the label "Not in the pool, not simulated", the first half is stale (each has an auto pool row on the board), and the second half is true (no title figure counts them). INFERENCE: the 11-05 build expected the auto row to drain this list (the comment at `season_deck.py:814-815` says so), but the intake that fills `teams[].players` reads the deck pool plus additions, not `pool_season.csv`. So nothing drains it.

Readers of the exact wording (EVIDENCE: grep): `test_season_deck.UnpooledAndNotStarted` asserts "Not in the pool, not simulated: Trevon Brazile (THEM, BN)". No production reader parses it.

## 3. Open decision for the owner: the five auto-row players

1. **Put auto-row players in the simulation (Recommended).** `co_gm.rosters` (or the intake) also takes a rostered "unpooled" player whose name has a row in the season pool. The simulator then counts the five, and the label drops them, which is what the 11-05 "auto season line" pick meant to achieve. This changes an engine input: title odds and waiver pairs move, for 5 players across 5 teams. It needs your pick, and a calibration note in the after-report.
2. **Keep them out, fix the words.** The label becomes "auto row on the board (blended), not in the simulation", which is true today. Display-only, three places.
3. **Leave it.** The label stays half stale.

## 3a. Owner's picks (2026-11-09): "Simulate them", then "Push it" after seeing the shift — built

- `co_gm.rosters` also takes a team's `unpooled` player whose name the pool in use has: the season pool's auto season line. An IL slot still counts 0, and a name with no row anywhere stays out. All callers share it: the brief's title odds and waiver pairs, `il_return`, and `weekly_preview`.
- Labels: the brief and the deck's Today tab split the list into "Not in the pool, not simulated" (no row anywhere) and "Auto row (blended), simulated". The intake and league-live lines now say "not in the deck pool (simulated once the season lines give an auto row, 3+ games)", because they run before the season lines. No prompt or production reader parses the old wording (EVIDENCE: grep across the kit and season/daily). The two tests that pinned it were updated with it.
- Tests: `test_daily_brief.AutoRowsSimulated` (+2) and `test_season_deck.AutoRowLabel` (+1). Red first: 2 failures (`Lists differ: ['A'] != ['A', 'Auto Guy']` and the deck still saying "not simulated" for the auto-row player) and 1 error (`TypeError: unpooled_line() takes 1 positional argument but 2 were given`). Suite 831 OK (2 skips).

**What it does to the title odds** (EVIDENCE: `run_league_sim` on the 11-09 state and season pool, 10,000 seasons, seeds 2026/2027, before = `teams[].players` only, after = `rosters()` as built; scratch worktree at 85556cc, removed after):

| seat (player added) | before (mean of seeds) | after | change |
|---|---|---|---|
| 1 (Meleek Thomas) | 0.74% | 4.22% | +3.48 |
| 5 (Nolan Traore) | 0.75% | 4.12% | +3.38 |
| 7 (Danny Wolf) | 0.83% | 4.80% | +3.97 |
| 9 (Morez Johnson Jr.) | 0.00% | 0.00% | 0.00 |
| 11 (Mario Hezonja) | 3.12% | 10.76% | +7.64 |
| 10 (owner) | 18.06% | 15.19% | **−2.87** |

The owner's shift is outside the season band below. The plan's branch rule (shift larger than the band → stop and report) fired; it was reported, and the owner chose to push. INFERENCE: the four teams that gain had been simulated a man short, so the new figures are closer to the rosters as they stand. How large the shift is rests on the auto line's replacement prior (deck rows 146–166 by z, `AUTO_PRIOR_LO`/`AUTO_PRIOR_HI`, uncalibrated, D-AP-1). That decision stays open.

## 4. Part 3: what `absent_from_sim` counts (EVIDENCE: `co_gm.py:315-333`)

It counts rostered active players who reached `ros` (state `teams[].players`) but whose names the simulator's pool (SEASON_POOL, else frozen v69) lacks. A state "unpooled" player never reaches `ros`, so it can never be counted there. That is why the field read `[]` on 11-03 … 11-05 while 2–4 players were unpooled (runner finding 3). There are comments to that effect at `co_gm.py` (above `rec["absent_from_sim"]`) and `daily_brief.py:258`. Behaviour is unchanged.

## 5. Bands quoted

This report quotes no new title share. The standing structural band for any title figure is the season sweep of 2026-11-02 (deck e14cc42): **weekly_availability is FRAGILE:** -2.6 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.2 (healthy players play 0.95 of games) / +0.0 (healthy players play 0.80 of games), mean of the two seeds.

Runner impact: code-only. The deck step's PASS line may now end `; absent: …`, and the runner's pass pattern (`^SEASON DECK: PASS`) still matches. The intake and league-live lines changed wording; their pass patterns are unchanged. From the first morning after merge, the brief's title odds count the auto-row players. No step or prompt change.

## 6. Bounds

- Out of scope by design: any label change (§3, stopped); the simulator's roster input.
- In scope and unverified: the first live build with an absent input after merge.
## Watchlist

- 2026-11-09: week 3 on the accuracy card, the candidate's second graded week under D-ML-1.
- 2026-11-16: the week-5 confidence re-run; re-run `backtest.py` on about 20 games per player.

## Open-item receipts

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
