# Morning run 2026-11-26

**MORNING: PASS — 2026-11-26: 24 steps; brief report/briefs/brief_2026-11-26.md; record report/briefs/morning_2026-11-26.json**

- **Schedule:** T0 2026-11-26T12:42:06Z. Path: `morning.py --since <T0>` (`--help` lists `--since`). Thursday: no sweep, no forecasts, no scoreboard intake.
- **Repos:** kit already attached; deck repo pulled. season/daily checked out at 813cdde from origin; origin/main had nothing new. Tree clean, no stash.
- **Flaim:** league 478.l.36464.
  - Returned: 12 of 12 rosters (one call at a time), matchups for week 6, 100 available players, standings, 12 of 12 dated lineups for 2026-11-25, transactions (99 rows).
  - Flaim again could not interpret 1 Yahoo entry. No errors, no retries.
- **FantasyBot:** outlook only (1 call; Flaim was complete).

## Step lines

- LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-26.json; 3 not in the deck pool (simulated once the season lines give an auto row, 3+ games): Charles Bassey (Podz save the league, C), Kenrich Williams (ROOKS FTW, UTIL), Matisse Thybulle (John's Cool Team, SG)
- MATCHUP LIVE: PASS — week 6, games left 20 mine / 17 Booker T Floppers
- BOX PULL: PASS — 2026-11-25: 9 games, 235 player lines, 165 in the pool, 70 unpooled; two outlets: 232 matched, 2 cells differ, 1 ESPN-only, 0 bref-only
- MANAGER LOG: PASS — 2026-11-25: 12 lineups, 0 start(s) lost league-wide; 6 new move(s), 226 on record; Flaim could not read 1 row (the separate `manager_log.py` re-run found 0 new, as expected)
- TAG OUTCOMES: PASS — 2026-11-25: 36 flagged player(s) 12 no game, 6 played, 17 sat, 1 unresolved
- SEASON LINES: PASS — 305 lines moved by 0.25+; 3 auto rows (Bassey 16g, Kenrich Williams 19g, Thybulle 18g); 163 unpooled players with games
- MINUTES LINE: PASS — 2026-11-26: 341 players, 301 with games; ratio >= 1.10 for 5, <= 0.90 for 27; 36 unscaled (no preseason mpg)
- THREES LINE: PASS — above the live line by 0.2+ for 22, below for 14; candidate only
- STATUS GATE: PASS — status_2026-11-26.json: 34 flagged rows
- DECISION LOG: PASS — R-2026-11-26-01 add_drop Alex Caruso for Collin Gillespie; moves: nothing new
- TITLE WATCH: PASS — title 14.7% (was 14.6%), +0.1 against a band of ±0.7: within the band
- WEEK MATCHUP: PASS — week 6 vs Booker T Floppers; to date from Yahoo (rebuild agrees); 3 days, 0 missing; projected 8-1-0
- DECISION CARD: PASS — 1 pair; same order in both worlds; top pair holds in 2 of 4
- LEAGUE TABLE: PASS — power #1 ROOKS FTW (0.582), you #2 (0.575); Yahoo W-L-T matches the kit's finished weeks
- SEASON DECK: PASS — report/season/deck_2026-11-26.html (7 panes, 317 board rows, 34 status rows; render: 7 tabs, 0 page errors)

## League moves (league_moves_2026-11-26.json, since the 11-25 morning state)

- **SNOWTIME WHITE WALKERS** — added Kelly Oubre Jr.; dropped Isaiah Joe (Mikel Brown Jr. came and went in between)
- **Scottie's Thotties** — added Ja'Kobe Walter; dropped Ryan Rollins
- **ANONG NANGIANNIS?!** — dropped Zaccharie Risacher; off IL: De'Aaron Fox
- **Thompson Telepathy** — added Kevin Porter Jr.; dropped Mike Conley
- **John's Cool Team** — added Jalen Green; to IL: Zach LaVine

## Brief

- **Week 6 (Yahoo):** you lead Booker T Floppers 8-1-0 after 3 days; games left 20 / 17. Standings 27-18-0, 3rd.
- **Lineup today:** no NBA games for any of your players today (Thanksgiving).
- **Waiver scan:** 1 of 520 pairs positive — add **Alex Caruso** (OKC), drop Collin Gillespie: +0.007 cats/week; title 14.9% (+0.1), inside the ±0.7 sampling error. Decision card: top pair holds in 2 of 4 worlds.
- **Waiver scan status:** "Status from Yahoo and ESPN. Set aside as Out: Jalen Williams, Cason Wallace, Tobias Harris, Maxime Raynaud, Justin Champagnie, Bradley Beal" (receipts in the brief).
- **Title:** 14.7% ± 0.5 (2 runs × 10,000 seasons). Playoffs 98.9%.
  - Structural band (sweep of 2026-11-23): no FRAGILE constant in the headline; weekly_availability SENSITIVE −1.1 / +0.5 (healthy), −1.5 / +1.2 (risk).
  - If IL players return on ESPN's dates: ≈22.9% (scenario, not a forecast; ± 0.49). **ROOM_RULE_ON is FRAGILE in that scenario: +2.6 with the rule off.**

## Deck

- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 109 (1795697295-c00f). Before: Version 108 (last night's afternoon refresh).
- The 782,122 built bytes are contained in the 782,668-byte live page, which renders 7 tabs with 0 page errors.
- **WROTE:** 46 path(s) (morning.py).

## Decision for David

The scan's one positive pair is too small to act on: +0.007 categories a week, and its title change (+0.1) is inside sampling error.
1. **Hold (Recommended)** — Gillespie stays; the gain is noise-level and he has 2 games left this week.
2. Make the swap (Caruso for Gillespie) — only if you want the steals/defence profile; the kit sees no measurable edge.
