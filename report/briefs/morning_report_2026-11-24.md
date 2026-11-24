# Morning run 2026-11-24

**MORNING: PASS — 2026-11-24: 24 steps; brief report/briefs/brief_2026-11-24.md; record report/briefs/morning_2026-11-24.json**

- **Schedule:** T0 2026-11-24T12:41:23Z. Path: `morning.py --since <T0>` (`--help` lists `--since`). Tuesday: no sweep, no forecasts, no scoreboard intake.
- **Repos:** kit already attached; deck repo pulled. season/daily checked out at 8a91038 from origin; origin/main had nothing new. Tree clean, no stash.
- **Flaim:** league 478.l.36464.
  - Returned: 12 of 12 rosters (one call at a time), matchups for week 6, 100 available players, standings, 12 of 12 dated lineups for 2026-11-23, transactions (99 rows).
  - Flaim again could not interpret 1 Yahoo entry. No errors, no retries.
- **FantasyBot:** outlook only (1 call; Flaim was complete).

## Step lines

- LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-24.json; 3 not in the deck pool (simulated once the season lines give an auto row, 3+ games): Charles Bassey (Podz save the league, C), Svi Mykhailiuk (ROOKS FTW, UTIL), Matisse Thybulle (John's Cool Team, SG)
- MATCHUP LIVE: PASS — week 6, games left 32 mine / 29 Booker T Floppers
- BOX PULL: PASS — 2026-11-23: 10 games, 269 player lines, 182 in the pool, 87 unpooled; two outlets: 268 matched, 1 cells differ
- MANAGER LOG: PASS — 2026-11-23: 12 lineups, 0 start(s) lost league-wide; outside IL, team played but no box line: Cameron Boozer, Chet Holmgren, De'Aaron Fox, Evan Mobley, Grayson Allen, Joel Embiid, Norman Powell, RJ Barrett, Victor Wembanyama; 9 new move(s), 215 on record; Flaim could not read 1 row (the separate `manager_log.py` re-run found 0 new, as expected)
- TAG OUTCOMES: PASS — 2026-11-23: 39 flagged player(s) 10 no game, 7 played, 21 sat, 1 unresolved
- SEASON LINES: PASS — 305 lines moved by 0.25+; 3 auto rows (Bassey 15g, Mykhailiuk 19g, Thybulle 18g); 162 unpooled players with games; 1 tag override
- MINUTES LINE: PASS — 2026-11-24: 341 players, 299 with games; ratio >= 1.10 for 6, <= 0.90 for 23; 36 unscaled (no preseason mpg)
- THREES LINE: PASS — above the live line by 0.2+ for 21, below for 12; candidate only
- STATUS GATE: PASS — status_2026-11-24.json: 32 flagged rows
- DECISION LOG: PASS — R-2026-11-24-01 hold; M-2026-11-23-01 pm +Collin Gillespie −Andrew Wiggins → exact S-2026-11-23-01
- TITLE WATCH: PASS — title 14.8% (was 13.2%), +1.6 against a band of ±0.7: **MOVED**. Flags a METHOD CHANGE (constant `season_lines.KIT_ROW_GP_QUANTILE` added to the register); its walk puts +0.0 on the engine, +1.1 on rosters and results, +0.6 on lines. The code sets it at 0.5 with the comment "0.5 is the median, as before".
- WEEK MATCHUP: PASS — week 6 vs Booker T Floppers; to date from Yahoo (rebuild agrees); 1 day, 0 missing; projected 5-4-0
- DECISION CARD: PASS — no pair today
- LEAGUE TABLE: PASS — power #1 SNOWTIME WHITE WALKERS (0.592), you #5 (0.544); Yahoo W-L-T matches the kit's finished weeks
- SEASON DECK: PASS — report/season/deck_2026-11-24.html (7 panes, 317 board rows, 32 status rows; render: 7 tabs, 0 page errors)

## League moves (league_moves_2026-11-24.json)

- **KEL'EL YAXEL HALQUETA (you)** — added Collin Gillespie; dropped Andrew Wiggins
- **Podz save the league** — added Buddy Hield, Cameron Johnson; dropped Caleb Martin, Ja'Kobe Walter, Keaton Wagler; off IL: Brandon Miller
- **ANONG NANGIANNIS?!** — added Terrence Shannon Jr; dropped Nolan Traore
- **Thompson Telepathy** — added De'Andre Hunter; dropped Collin Sexton
- **Looking Cool Joker!** — added Anfernee Simons; dropped Aaron Nesmith
- **ROOKS FTW** — added Svi Mykhailiuk; dropped Jaxson Hayes
- **John's Cool Team** — dropped Sam Hauser; off IL: Jayson Tatum

## Brief

- **Week 6 (Yahoo):** you lead Booker T Floppers 5-4 after day 1; games left 32 / 29. Standings 27-18-0, 3rd.
- **Lineup today (daily-fill rule):** PG White, SG Irving, PF Washington (Q, check before lock), F Collins, C Queta. No game: Jerome, Gillespie, McDaniels, Bridges, Ware, Spencer, Durant, Lendeborg.
- **Waiver scan:** no add/drop pair raises expected weekly category wins (520 scored). Stand pat.
- **Waiver scan status:** "Status from Yahoo and ESPN. Set aside as Out: Jalen Williams, Cason Wallace, Tobias Harris, Kevin Porter Jr., Maxime Raynaud, Justin Champagnie, Bradley Beal" (receipts in the brief).
- **Title:** 14.8% ± 0.5 (2 runs × 10,000 seasons). Playoffs 98.9%.
  - Structural band (sweep of 2026-11-23): no FRAGILE constant in the headline; weekly_availability SENSITIVE −1.1 / +0.5 (healthy), −1.5 / +1.2 (risk).
  - If IL players return on ESPN's dates: ≈22.0% (scenario, not a forecast; ± 0.49). **ROOM_RULE_ON is FRAGILE in that scenario: +2.8 with the rule off.**

## Deck

- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 102 (1795524370-8fe2). Before: Version 101.
- The 779,332 built bytes are contained in the 779,878-byte live page, which renders 7 tabs (Today, Trade Analyzer, Free Agents, Board, Draft Check, Week, League) with 0 page errors.
- **WROTE:** 48 path(s) (morning.py).

## Decision for David

None today: the scan finds no positive pair. Lineup only: PJ Washington (Q) sits in the active lineup for DAL @ DEN; check his status before lock.
