# Morning run 2026-11-25

**MORNING: PASS — 2026-11-25: 24 steps; brief report/briefs/brief_2026-11-25.md; record report/briefs/morning_2026-11-25.json**

- **Schedule:** T0 2026-11-25T12:41:00Z. Path: `morning.py --since <T0>` (`--help` lists `--since`). Wednesday: no sweep, no forecasts, no scoreboard intake.
- **Repos:** kit already attached; deck repo pulled. season/daily checked out at 8fd8c60 from origin; origin/main had nothing new. Tree clean, no stash.
- **Flaim:** league 478.l.36464.
  - Returned: 12 of 12 rosters (one call at a time), matchups for week 6, 100 available players, standings, 12 of 12 dated lineups for 2026-11-24, transactions (99 rows).
  - Flaim again could not interpret 1 Yahoo entry. No errors, no retries.
- **FantasyBot:** outlook only (1 call; Flaim was complete).

## Step lines

- LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-25.json; 3 not in the deck pool (simulated once the season lines give an auto row, 3+ games): Charles Bassey (Podz save the league, C), Kenrich Williams (ROOKS FTW, UTIL), Matisse Thybulle (John's Cool Team, SG)
- MATCHUP LIVE: PASS — week 6, games left 27 mine / 28 Booker T Floppers
- BOX PULL: PASS — 2026-11-24: 3 games, 78 player lines, 57 in the pool, 21 unpooled; two outlets: 78 matched, 0 cells differ
- MANAGER LOG: PASS — 2026-11-24: 12 lineups, 0 start(s) lost league-wide; 5 new move(s), 220 on record; Flaim could not read 1 row (the separate `manager_log.py` re-run found 0 new, as expected)
- TAG OUTCOMES: PASS — 2026-11-24: 32 flagged player(s) 26 no game, 1 played, 4 sat, 1 unresolved
- SEASON LINES: PASS — 305 lines moved by 0.25+; 3 auto rows (Bassey 15g, Kenrich Williams 18g, Thybulle 18g); 162 unpooled players with games; 1 tag override
- MINUTES LINE: PASS — 2026-11-25: 341 players, 300 with games; ratio >= 1.10 for 6, <= 0.90 for 26; 36 unscaled (no preseason mpg)
- THREES LINE: PASS — above the live line by 0.2+ for 19, below for 12; candidate only
- STATUS GATE: PASS — status_2026-11-25.json: 36 flagged rows
- DECISION LOG: PASS — R-2026-11-25-01 hold; moves: nothing new
- TITLE WATCH: PASS — title 14.6% (was 14.8%), −0.2 against a band of ±0.7: within the band
- WEEK MATCHUP: PASS — week 6 vs Booker T Floppers; to date from Yahoo (rebuild agrees); 2 days, 0 missing; projected 6-3-0
- DECISION CARD: PASS — no pair today
- LEAGUE TABLE: PASS — power #1 SNOWTIME WHITE WALKERS (0.578), you #2 (0.566); Yahoo W-L-T matches the kit's finished weeks
- SEASON DECK: PASS — report/season/deck_2026-11-25.html (7 panes, 317 board rows, 36 status rows; render: 7 tabs, 0 page errors)

## League moves (league_moves_2026-11-25.json, since the 11-24 morning state)

- **SNOWTIME WHITE WALKERS** — added Isaiah Joe; dropped Kelly Oubre Jr.
- **Thompson Telepathy** — added Mike Conley; dropped Kris Dunn
- **ROOKS FTW** — added Kenrich Williams; dropped Svi Mykhailiuk (Kevin Huerter came and went in between)
- **Looking Cool Joker!** — added Brandon Williams; dropped Anfernee Simons
- **ANONG NANGIANNIS?!** — to IL: De'Aaron Fox; off IL: Giannis Antetokounmpo

## Brief

- **Week 6 (Yahoo):** you lead Booker T Floppers 6-2-1 after 2 days; games left 27 / 28. Standings 27-18-0, 3rd.
- **Lineup today (daily-fill rule):** PG Gillespie, SG Spencer, G Jerome, SF Durant, PF Lendeborg (Q, check before lock), F Bridges, C Ware, Util McDaniels. No game: Queta, Washington, White, Collins, Irving.
- **Waiver scan:** no add/drop pair raises expected weekly category wins (520 scored). Stand pat.
- **Waiver scan status:** "Status from Yahoo and ESPN. Set aside as Out: Jalen Williams, Cason Wallace, Tobias Harris, Kevin Porter Jr., Maxime Raynaud, Justin Champagnie, Bradley Beal" (receipts in the brief).
- **Title:** 14.6% ± 0.5 (2 runs × 10,000 seasons). Playoffs 98.8%.
  - Structural band (sweep of 2026-11-23): no FRAGILE constant in the headline; weekly_availability SENSITIVE −1.1 / +0.5 (healthy), −1.5 / +1.2 (risk).
  - If IL players return on ESPN's dates: ≈22.0% (scenario, not a forecast; ± 0.49). **ROOM_RULE_ON is FRAGILE in that scenario: +2.7 with the rule off.**

## Deck

- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 104 (1795610654-2b03). Before: Version 103.
- The 784,271 built bytes are contained in the 784,817-byte live page, which renders 7 tabs with 0 page errors.
- **WROTE:** 46 path(s) (morning.py).

## Decision for David

None today: the scan finds no positive pair. Lineup only: Yaxel Lendeborg (Q) is in the active PF slot; check his status before lock.
