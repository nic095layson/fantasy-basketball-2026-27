# Morning run 2026-11-05

**MORNING: PASS — 2026-11-05: 19 steps; brief report/briefs/brief_2026-11-05.md; record report/briefs/morning_2026-11-05.json**

- **T0:** 2026-11-05T13:05:06Z. Path: `morning.py --since <T0>` (`--help` lists `--since`).
- **Repos:** the kit was already attached (push rights to season/daily); the deck repo was up to date. Tree clean, no stash. season/daily was already up to date with origin/main.
- **Flaim:** tools present. 12 of 12 rosters, matchups (week 3), available players (100), standings, 12 of 12 dated lineups for 2026-11-04, transactions (100 rows). No errors, no retries.
- **FantasyBot:** tools present; outlook only (1 call; Flaim was complete).
- **LEAGUE LIVE:** PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-05.json; 4 not in the pool, not simulated: Meleek Thomas (Looking Cool Joker!, G), Nolan Traore (ANONG NANGIANNIS?!, PG), Matisse Thybulle (MAXEY-MUM OVERDRIVE, BN), Quenton Jackson (John's Cool Team, UTIL)
- **WEEK MATCHUP:** PASS — 2026-11-05: week 3 vs Podz save the league; to date from Yahoo (rebuild differs on 2 stat(s)); to date 3 day(s), 0 missing; projected 8-1-0; pickups: no finished low-value player; pool pool_season.csv; wrote report/briefs/week_matchup_2026-11-05.json
- **Live matchup:** week 3, games left 22 mine / 19 Podz save the league.

## League moves (league_moves_2026-11-05.json, 2026-11-04 → 2026-11-05)

- **Lauri’s Prime Rib** — added Klay Thompson; to IL: Josh Hart
- **Scottie’s Thotties** — added Bobby Portis; to IL: DeMar DeRozan
- **ANONG NANGIANNIS?!** — to IL: Trey Murphy III; off IL: Alex Sarr
- **MAXEY-MUM OVERDRIVE** — dropped Mikel Brown Jr.; off IL: Kon Knueppel
- **John's Cool Team** — added Quenton Jackson

## Step lines

- **TAG OUTCOMES:** PASS — 2026-11-04: 31 flagged player(s) 4 no game, 8 played, 18 sat, 1 unresolved; data/status/tag_outcomes.jsonl
- **MINUTES LINE:** PASS — 2026-11-05: 338 players, 290 with games; ratio >= 1.10 for 9, <= 0.90 for 33; 33 unscaled (no preseason mpg); candidate only, wrote pool_season_mt.csv, projections_season_mt.csv. *A candidate, not the projection.*
- **MANAGER LOG:** PASS — 2026-11-04: 12 lineups, 0 start(s) lost league-wide; outside IL, team played but no box line (inactive or unmatched name): Chet Holmgren, Jalen Johnson, Jayson Tatum, Peyton Watson; profile 2026-10-22..2026-11-04 (13 day(s)); 6 new move(s), 102 on record. 12 of 12 dated lineups; transactions came back.
- **STATUS GATE:** PASS — status_2026-11-05.json: 26 flagged row(s), each tiered with a dated receipt

## Brief

- **Lineup today:** PG Collin Gillespie, SF Yaxel Lendeborg, PF Miles Bridges. The other 10 have no game today.
- **Top waiver pair:** add Tobias Harris (SAS), drop Karlo Matkovic: +0.166 cats/week; title 11.8% (+3.0). He is "O today (yahoo), ESPN expects back 2026-11-09, check before claiming".
- **Waiver scan status:** "Status from Yahoo and ESPN. Set aside as Out: Jalen Williams (Out, espn, ESPN expects back 2027-03-02), Cason Wallace (O, yahoo, ESPN expects back 2027-03-02), Kevin Porter Jr. (NA, yahoo), Justin Champagnie (O, yahoo, ESPN expects back 2027-02-25), Dominick Barlow (Out, espn, ESPN expects back 2026-11-18)."
- **Waiver-date notes, first run with a Yahoo list pinned:** the notes read the list (`read: true`). Mikel Brown Jr. has waiver date 2026-11-06, which matches the pull. The top 3 adds are free agents, so they show no waiver date. Their own-drop notes held: Champagnie and Johnson show "you dropped him 2026-11-03".
- **Title:** 8.7% ± 0.4 (2 runs × 10,000 seasons). Playoffs: 96.8%. Structural band: weekly_availability is FRAGILE, −2.6 / +2.2. IL-return scenario: ≈26%, not a forecast; ROOM_RULE_ON is FRAGILE (+6.3).
- **Season lines:** 293 lines moved by 0.25+ (report/season/board_2026-11-05.md lists them). 144 unpooled players have games.
- **Unpooled rostered players:** the 4 named in LEAGUE LIVE. Quenton Jackson is new today.

## Deck

- **SEASON DECK:** PASS — 2026-11-05: report/season/deck_2026-11-05.html (7 panes, 315 board rows, 26 status rows; record deck_record_2026-11-05.json pins 15 inputs; render: 7 tabs, 0 page errors)
- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 59 (1793884343-7442). The 558,295 built bytes are contained in the 558,841-byte live page. The 7 tabs are Today, Trade Analyzer, Free Agents, Board, Movers, Week and League.
- **WROTE:** 31 path(s) (morning.py). manager_log adds data/managers/.

## Nothing failed
