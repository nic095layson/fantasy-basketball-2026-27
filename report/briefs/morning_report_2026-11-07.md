# Morning run 2026-11-07

**MORNING: PASS — 2026-11-07: 20 steps; brief report/briefs/brief_2026-11-07.md; record report/briefs/morning_2026-11-07.json**

- **T0:** 2026-11-07T13:03:05Z. Path: `morning.py --since <T0>` (`--help` lists `--since`).
- **Repos:** the kit was already attached (push rights to season/daily); the deck repo was up to date. Tree clean, no stash. season/daily was already up to date with origin/main.
- **Flaim:** tools present. 12 of 12 rosters, matchups (week 3), available players (100), standings, 12 of 12 dated lineups for 2026-11-06, transactions (100 rows). No errors, no retries.
- **FantasyBot:** tools present; outlook only (1 call; Flaim was complete).
- **LEAGUE LIVE:** PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-07.json; 5 not in the pool, not simulated: Meleek Thomas (Looking Cool Joker!, G), Nolan Traore (ANONG NANGIANNIS?!, PG), Mario Hezonja (MAXEY-MUM OVERDRIVE, PF), Matisse Thybulle (MAXEY-MUM OVERDRIVE, F), Kenrich Williams (John's Cool Team, BN)
- **WEEK MATCHUP:** PASS — 2026-11-07: week 3 vs Podz save the league; to date from Yahoo (rebuild differs on 4 stat(s)); to date 5 day(s), 0 missing; projected 8-1-0; pickups: no finished low-value player; pool pool_season.csv; wrote report/briefs/week_matchup_2026-11-07.json
- **Live matchup:** week 3, games left 11 mine / 11 Podz save the league.

## League moves (league_moves_2026-11-07.json, 2026-11-06 → 2026-11-07)

- **Looking Cool Joker!** — added Naji Marshall; dropped Obi Toppin
- **Scottie’s Thotties** — added Mikel Brown Jr.; dropped Bobby Portis; to IL: Scottie Barnes; off IL: DeMar DeRozan
- **ANONG NANGIANNIS?!** — dropped Sandro Mamukelashvili; off IL: Trey Murphy III
- **MAXEY-MUM OVERDRIVE** — added Mario Hezonja, Santi Aldama; dropped Bradley Beal, Jalen Green; to IL: Immanuel Quickley
- **John's Cool Team** — added Kenrich Williams; dropped Quenton Jackson; to IL: De'Andre Hunter; off IL: Ivica Zubac

## Step lines

- **TAG OUTCOMES:** PASS — 2026-11-06: 29 flagged player(s) 11 no game, 4 played, 13 sat, 1 unresolved; data/status/tag_outcomes.jsonl
- **MINUTES LINE:** PASS — 2026-11-07: 343 players, 293 with games; ratio >= 1.10 for 8, <= 0.90 for 33; 38 unscaled (no preseason mpg); candidate only, wrote pool_season_mt.csv, projections_season_mt.csv. *A candidate, not the projection.*
- **MANAGER LOG:** PASS — 2026-11-06: 12 lineups, 2 start(s) lost league-wide; outside IL, team played but no box line (inactive or unmatched name): Chet Holmgren, Jalen Johnson, Jarrett Allen, Moussa Diabaté, Scottie Barnes; profile 2026-10-22..2026-11-06 (15 day(s)); 10 new move(s), 117 on record. 12 of 12 dated lineups; transactions came back.
- **STATUS GATE:** PASS — status_2026-11-07.json: 28 flagged row(s), each tiered with a dated receipt

## Brief

- **Lineup today:** PG Collin Gillespie, SG Kevin Durant, SF Yaxel Lendeborg, PF Miles Bridges. The other 9 active players have no game today.
- **Top waiver pair:** add Tobias Harris (SAS), drop Ziaire Williams: +0.127 cats/week; title 14.6% (+3.0). He is "O today (yahoo), ESPN expects back 2026-11-09, check before claiming".
- **Waiver scan status:** "Status from Yahoo and ESPN. Set aside as Out: Jalen Williams (Out, espn, ESPN expects back 2027-03-02), Cason Wallace (O, yahoo, ESPN expects back 2027-03-02), Kevin Porter Jr. (NA, yahoo), Justin Champagnie (O, yahoo, ESPN expects back 2027-02-25), Bradley Beal (Out, espn, ESPN expects back 2026-11-29)."
- **Title:** 11.6% ± 0.4 (2 runs × 10,000 seasons). Playoffs: 98.8%. Structural band: weekly_availability is FRAGILE, −2.6 / +2.2. IL-return scenario: ≈29%, not a forecast.
- **Season lines:** 298 lines moved by 0.25+ (report/season/board_2026-11-07.md lists them). 143 unpooled players have games. 5 auto rows for rostered players the pool lacked (Meleek Thomas 6g, Nolan Traore 8g, Mario Hezonja 9g, Matisse Thybulle 10g, Kenrich Williams 9g).
- **Unpooled rostered players:** the 5 named in LEAGUE LIVE. Mario Hezonja and Kenrich Williams are new today; Quenton Jackson left (dropped).
- **Flag, carried from 11-06:** the brief and LEAGUE LIVE still call these 5 "not in the pool, not simulated", although season lines gave all 5 an auto row. LEAGUE LIVE runs before season lines. Whether the simulator reads the auto rows was not traced (INFERENCE).

## Deck

- **SEASON DECK:** PASS — 2026-11-07: report/season/deck_2026-11-07.html (7 panes, 315 board rows, 28 status rows; record deck_record_2026-11-07.json pins 16 inputs; render: 7 tabs, 0 page errors)
- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 63 (1794057061-f3c2). The 573,519 built bytes are contained in the 574,065-byte live page. The 7 tabs are Today, Trade Analyzer, Free Agents, Board, Movers, Week and League.
- **WROTE:** 34 path(s) (morning.py). manager_log adds data/managers/.

## Nothing failed
