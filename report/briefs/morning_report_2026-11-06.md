# Morning run 2026-11-06

**MORNING: PASS — 2026-11-06: 20 steps; brief report/briefs/brief_2026-11-06.md; record report/briefs/morning_2026-11-06.json**

- **T0:** 2026-11-06T13:06:58Z. Path: `morning.py --since <T0>` (`--help` lists `--since`).
- **Repos:** the kit was already attached (push rights to season/daily); the deck repo was up to date. Tree clean, no stash. season/daily merged origin/main 8f252a2 cleanly. That brought in #241 (the afternoon deck record and footer name their own page; the replay gate takes morning records only), #242 and #243.
- **Flaim:** tools present. 12 of 12 rosters, matchups (week 3), available players (100), standings, 12 of 12 dated lineups for 2026-11-05, transactions (100 rows). No errors, no retries.
- **FantasyBot:** tools present; outlook only (1 call; Flaim was complete).
- **LEAGUE LIVE:** LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-06.json; 4 not in the pool, not simulated: Meleek Thomas (Looking Cool Joker!, G), Nolan Traore (ANONG NANGIANNIS?!, PG), Matisse Thybulle (MAXEY-MUM OVERDRIVE, F), Quenton Jackson (John's Cool Team, BN)
- **WEEK MATCHUP:** WEEK MATCHUP: PASS — 2026-11-06: week 3 vs Podz save the league; to date from Yahoo (rebuild differs on 2 stat(s)); to date 4 day(s), 0 missing; projected 8-1-0; pickups: no finished low-value player; pool pool_season.csv; wrote report/briefs/week_matchup_2026-11-06.json
- **Live matchup:** week 3, games left 19 mine / 17 Podz save the league.

## League moves (league_moves_2026-11-06.json, 2026-11-05 → 2026-11-06)

- **KEL'EL YAXEL HALQUETA (yours)** — added Ziaire Williams; dropped Karlo Matkovic
- **ANONG NANGIANNIS?!** — added Oso Ighodaro; dropped Zaccharie Risacher
- **Cade n em** — added Kingston Flemings; dropped Andrew Wiggins
- **MAXEY-MUM OVERDRIVE** — added Jalen Green; to IL: Kon Knueppel
- **ROOKS FTW** — dropped Isaiah Jackson; off IL: Anthony Black

## Step lines

- **TAG OUTCOMES:** TAG OUTCOMES: PASS — 2026-11-05: 26 flagged player(s) 22 no game, 3 sat, 1 unresolved; data/status/tag_outcomes.jsonl
- **MINUTES LINE:** MINUTES LINE: PASS — 2026-11-06: 342 players, 290 with games; ratio >= 1.10 for 9, <= 0.90 for 33; 37 unscaled (no preseason mpg); candidate only, wrote pool_season_mt.csv, projections_season_mt.csv *A candidate, not the projection.*
- **LINEUP LOG** (new, #240): LINEUP LOG: PASS — 2026-11-05: agreed; ledger 1 days, 0 pairs, start followed 0/0, night kit 0 / against 0
- **MANAGER LOG:** MANAGER LOG: PASS — 2026-11-05: 12 lineups, 0 start(s) lost league-wide; profile 2026-10-22..2026-11-05 (14 day(s)); 5 new move(s), 107 on record. 12 of 12 dated lineups; transactions came back.
- **STATUS GATE:** STATUS GATE: PASS — status_2026-11-06.json: 29 flagged row(s), each tiered with a dated receipt

## Brief

- **Lineup today:** PG Ty Jerome, SG Ziaire Williams, G Derrick White, SF Jaden McDaniels, PF PJ Washington, C Neemias Queta, C Kel'el Ware, Util Kyrie Irving. No game today: Lendeborg, Bridges, Gillespie, Durant, Dunn.
- **Top waiver pair:** add Tobias Harris (SAS), drop Ziaire Williams: +0.133 cats/week; title 12.6% (+2.3). He is "O today (yahoo), ESPN expects back 2026-11-09, check before claiming".
- **Waiver scan status:** "Status from Yahoo and ESPN. Set aside as Out: Jalen Williams (Out, espn, ESPN expects back 2027-03-02), Cason Wallace (O, yahoo, ESPN expects back 2027-03-02), Kevin Porter Jr. (NA, yahoo), Justin Champagnie (O, yahoo, ESPN expects back 2027-02-25)."
- **Title:** 10.4% ± 0.4 (2 runs × 10,000 seasons). Playoffs: 98.0%. Structural band: weekly_availability is FRAGILE, −2.6 / +2.2.
- **Season lines:** 294 lines moved by 0.25+ (report/season/board_2026-11-06.md). 140 unpooled players have games.
- **Auto pool rows (#240, first live run):** SEASON LINES made 4 auto rows: Meleek Thomas 5g, Nolan Traore 8g, Matisse Thybulle 9g, Quenton Jackson 9g. This matches the known answer in after-report-2026-11-05 (all 4 clear the 3-game bar). All 4 are now in data/season/pool_season.csv, and the brief's absent_from_sim list is empty.
- **Flag (not fixed):** the brief and LEAGUE LIVE still list those 4 as "Not in the pool, not simulated", each needing a pool_additions.csv row. LEAGUE LIVE builds that list before SEASON LINES adds the rows, so the line is likely stale. INFERENCE; I did not trace which pool file the simulator read.

## Deck

- **SEASON DECK:** SEASON DECK: PASS — 2026-11-06: report/season/deck_2026-11-06.html (7 panes, 315 board rows, 29 status rows; record deck_record_2026-11-06.json pins 16 inputs; render: 7 tabs, 0 page errors)
- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 61 (1793970849-2294). The 586,519 built bytes are contained in the 587,065-byte live page. The 7 tabs are Today, Trade Analyzer, Free Agents, Board, Movers, Week and League.
- **WROTE:** 35 path(s) (morning.py). manager_log adds data/managers/.

## Nothing failed
