# Morning run 2026-11-08

**MORNING: PASS — 2026-11-08: 21 steps; brief report/briefs/brief_2026-11-08.md; record report/briefs/morning_2026-11-08.json**

- **T0:** 2026-11-08T13:05:14Z. Path: `morning.py --since <T0>` (`--help` lists `--since`). Sunday: the next-week forecasts step ran.
- **Repos:** the kit was already attached (push rights to season/daily); the deck repo was up to date. Tree clean, no stash. season/daily was already up to date with origin/main.
- **Flaim:** tools present. 12 of 12 rosters (one at a time), matchups (week 3), available players (100), standings, 12 of 12 dated lineups for 2026-11-07, transactions (100 rows). No errors, no retries.
- **FantasyBot:** tools present; outlook only (1 call; Flaim was complete).
- **LEAGUE LIVE:** PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-08.json; 5 not in the pool, not simulated: Meleek Thomas (Looking Cool Joker!, G), Nolan Traore (ANONG NANGIANNIS?!, PG), Morez Johnson Jr. (Podz save the league, UTIL), Mario Hezonja (MAXEY-MUM OVERDRIVE, BN), Kenrich Williams (John's Cool Team, UTIL)
- **WEEK MATCHUP:** PASS — 2026-11-08: week 3 vs Podz save the league; to date from Yahoo (rebuild differs on 4 stat(s)); to date 6 day(s), 0 missing; projected 8-1-0; pickups ran (drop Cameron Johnson, 74 free agents scored from the Yahoo list); pool pool_season.csv; wrote report/briefs/week_matchup_2026-11-08.json
- **Live matchup:** week 3, games left 7 mine / 6 Podz save the league.

## League moves (league_moves_2026-11-08.json, 2026-11-07 → 2026-11-08)

- **KEL'EL YAXEL HALQUETA (yours)** — added Cameron Johnson; dropped Ziaire Williams
- **ANONG NANGIANNIS?!** — added Malik Monk; dropped Oso Ighodaro
- **John's Cool Team** — dropped De'Andre Hunter
- **Lauri’s Prime Rib** — added Luguentz Dort; dropped Klay Thompson
- **Looking Cool Joker!** — added Rui Hachimura; dropped Naji Marshall
- **MAXEY-MUM OVERDRIVE** — added Brayden Burries; dropped Ja'Kobe Walter, Matisse Thybulle; off IL: Immanuel Quickley
- **Podz save the league** — added Max Strus, Morez Johnson Jr.; dropped Anfernee Simons, De'Anthony Melton
- **ROOKS FTW** — added Jared McCain; to IL: Desmond Bane
- **Scottie’s Thotties** — added Jalen Smith; dropped Mikel Brown Jr.; to IL: Jarrett Allen; off IL: Scottie Barnes
- **Thompson Telepathy** — added Karlo Matkovic; dropped Alex Caruso

## Step lines

- **TAG OUTCOMES:** PASS — 2026-11-07: 28 flagged player(s) 14 no game, 3 played, 10 sat, 1 unresolved; data/status/tag_outcomes.jsonl
- **MINUTES LINE:** PASS — 2026-11-08: 343 players, 297 with games; ratio >= 1.10 for 9, <= 0.90 for 33; 37 unscaled (no preseason mpg); candidate only, wrote pool_season_mt.csv, projections_season_mt.csv. *A candidate, not the projection.*
- **NEXT WEEK FORECASTS (Sunday):** WEEKLY PREVIEW: PASS — week 4. report/previews/week_04.md: week 4 vs Lauri’s Prime Rib, P(win the week) 41.0% (±0.7 points, 2 seeds; the preview states no structural band, and Q/O statuses are not applied to the weekly model).
- **DECISION LOG:** PASS R-2026-11-08-01 add_drop Tobias Harris for Kris Dunn; M-2026-11-08-01 am +Cameron Johnson -Ziaire Williams -> add_match_drop_differs S-2026-10-30-01
- **MANAGER LOG:** PASS — 2026-11-07: 12 lineups, 1 start(s) lost league-wide; outside IL, team played but no box line (inactive or unmatched name): Anthony Davis, Chet Holmgren, Jarrett Allen; profile 2026-10-22..2026-11-07 (16 day(s)); 12 new move(s), 129 on record. 12 of 12 dated lineups; transactions came back.
- **STATUS GATE:** PASS — status_2026-11-08.json: 29 flagged row(s), each tiered with a dated receipt

## Brief

- **Lineup today:** PG Kris Dunn, SG Derrick White, G Kyrie Irving, SF Jaden McDaniels, PF PJ Washington, C Neemias Queta, C Kel'el Ware. No game today: Lendeborg, Bridges, Cameron Johnson, Gillespie, Durant, Jerome.
- **Top waiver pair:** add Tobias Harris (SAS), drop Kris Dunn: +0.058 cats/week; title 18.1% (+1.8). He is "O today (yahoo), ESPN expects back 2026-11-09, check before claiming". Only 11 of 520 pairs are positive today (40 yesterday).
- **Waiver scan status:** "Status from Yahoo and ESPN. Set aside as Out: Jalen Williams (Out, espn, ESPN expects back 2027-03-02), Cason Wallace (O, yahoo, ESPN expects back 2027-03-02), Kevin Porter Jr. (NA, yahoo), Justin Champagnie (O, yahoo, ESPN expects back 2027-02-25), Bradley Beal (Out, espn, ESPN expects back 2026-11-29)."
- **Title:** 16.3% ± 0.5 (2 runs × 10,000 seasons). Playoffs: 99.5%. Structural band: weekly_availability is FRAGILE, −2.6 / +2.2. IL-return scenario: ≈31% (30.7 to 31.1), not a forecast; ROOM_RULE_ON is FRAGILE (+7.5).
- **Season lines:** 301 lines moved by 0.25+ (report/season/board_2026-11-08.md lists them). 145 unpooled players have games. 5 auto rows for rostered players the pool lacked (Meleek Thomas 7g, Nolan Traore 9g, Morez Johnson Jr. 9g, Mario Hezonja 10g, Kenrich Williams 10g).
- **Unpooled rostered players:** the 5 named in LEAGUE LIVE. Morez Johnson Jr. is new today; Matisse Thybulle left (dropped).
- **Flag, carried from 11-06:** the brief and LEAGUE LIVE still call these 5 "not in the pool, not simulated", although season lines gave all 5 an auto row. Whether the simulator reads the auto rows was not traced (INFERENCE).

## Deck

- **SEASON DECK:** PASS — 2026-11-08: report/season/deck_2026-11-08.html (7 panes, 315 board rows, 29 status rows; record deck_record_2026-11-08.json pins 16 inputs; render: 7 tabs, 0 page errors)
- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 65 (1794143540-68b3). The 558,209 built bytes are contained in the 558,755-byte live page. The 7 tabs are Today, Trade Analyzer, Free Agents, Board, Movers, Week and League.
- **WROTE:** 44 path(s) (morning.py). manager_log adds data/managers/.

## Nothing failed
