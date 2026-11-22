# Morning run 2026-11-22

**MORNING: PASS — 2026-11-22: 25 steps; brief report/briefs/brief_2026-11-22.md; record report/briefs/morning_2026-11-22.json**

- **Schedule:** T0 2026-11-22T12:41:30Z. Path: `morning.py --since <T0>`. Sunday, so the next week forecasts step ran (below).
- **Repos:** kit already attached; deck repo pulled. season/daily already up to date at d8af78c. Tree clean, no stash.
- **Flaim:** league 478.l.36464.
  - Returned: 12 of 12 rosters (one call at a time), matchups for week 5, 100 available players, standings, 12 of 12 dated lineups for 2026-11-21, transactions (99 rows).
  - Flaim again could not interpret 1 Yahoo entry. No errors, no retries.
- **FantasyBot:** outlook only (1 call; Flaim was complete).

## Step lines

- LEAGUE LIVE: PASS — pinned data/source/flaim/pull_2026-11-22.json; 3 not in the deck pool: Nolan Traore (ANONG NANGIANNIS?!, IL), Matisse Thybulle (John's Cool Team, SG), Danny Wolf (John's Cool Team, BN)
- MATCHUP LIVE: PASS — week 5, games left 5 mine / 2 Thompson Telepathy
- BOX PULL: PASS — 2026-11-21: 6 games, 150 player lines, 105 in the pool, 45 unpooled; single-source (ESPN only)
- MANAGER LOG: PASS — 2026-11-21: 12 lineups, 0 starts lost league-wide; team played but no box line: Cameron Boozer, Jaylen Brown, Karl-Anthony Towns, OG Anunoby, P.J. Washington, Trey Murphy III; 3 new moves, 202 on record; Flaim could not read 1 row
- TAG OUTCOMES: PASS — 2026-11-21: 35 flagged: 20 no game, 3 played, 11 sat, 1 unresolved
- SEASON LINES: PASS — 303 lines moved by 0.25+; 3 auto rows (Traore 14g, Thybulle 17g, Wolf 10g); 158 unpooled players with games; 1 tag override
- MINUTES LINE: PASS — 341 players, 298 with games; ≥1.10 for 6, ≤0.90 for 23; 36 unscaled
- THREES LINE: PASS — above the live line by 0.2+ for 19, below for 13; candidate only
- STATUS GATE: PASS — status_2026-11-22.json: 39 flagged rows
- NEXT WEEK FORECASTS: `WEEKLY PREVIEW: PASS — week 6`
- DECISION LOG: PASS — R-2026-11-22-01 add_drop Collin Gillespie for Andrew Wiggins; moves: nothing new
- TITLE WATCH: PASS — title 13.1% (was 13.9% on 2026-11-21), −0.8 against a band of ±0.7: **MOVED**. 5 teams changed rosters (moves below).
- WEEK MATCHUP: PASS — to date from Yahoo (rebuild differs on 2 stats); 6 days, 0 missing; projected 5-4-0
- DECISION CARD: PASS — 3 pairs; order changes between the worlds; top pair holds in 4 of 4
- LEAGUE TABLE: PASS — power #1 ROOKS FTW (0.631), you #6 (0.505); Yahoo W-L-T matches the kit's finished weeks
- SEASON DECK: PASS — report/season/deck_2026-11-22.html (7 panes, 316 board rows, 39 status rows; render: 7 tabs, 0 page errors)

## League moves (league_moves_2026-11-22.json)

- **Thompson Telepathy (your opponent)** — added Kris Dunn; dropped Javon Small
- **Looking Cool Joker!** — added Naji Marshall; dropped Pelle Larsson
- **ANONG NANGIANNIS?!** — to IL: Nolan Traore; off IL: Trey Murphy III
- **Podz save the league** — off IL: Deni Avdija
- **John's Cool Team** — added Max Strus; to IL: Jayson Tatum

## Brief

- **Week 5 (Yahoo):** you lead Thompson Telepathy 5-4 on the last day; games left 5 / 2. Standings 21-15-0, 3rd.
- **Lineup today (daily-fill rule):** PG Irving, SG Wiggins, SF Lendeborg, PF Collins, C Queta. No game: Spencer, Bridges, Ware, Jerome, McDaniels, Durant.
  - On Yahoo, Derrick White (O) is in your active G slot and PJ Washington (O) in Util.
- **Waiver scan:** 6 of 520 pairs raise expected weekly category wins (base 4.845).
  - Top pair: add **Collin Gillespie**, drop Andrew Wiggins: +0.029 cats/week; title 13.9% (+0.9). Flaim now lists him as a free agent.
  - Then Cameron Johnson (+0.4) and Kevin Huerter (+0.3).
- **Decision card:** Gillespie +0.9 if IL players never return, −0.3 if they return on time, +0.00 categories this week. Johnson +0.4 / +0.0. The top pair holds in 4 of 4 weekly_availability settings (+0.7 to +1.0). The order changes between the two worlds.
- **Waiver scan status:** "Set aside as Out: Jalen Williams, Cason Wallace, Tobias Harris, Kevin Porter Jr., Justin Champagnie" (receipts in the brief).
- **Title:** 13.1% ± 0.5 (2 runs × 10,000 seasons). Playoffs 98.1%.
  - Structural band (sweep of 2026-11-17): no FRAGILE constant; weekly_availability SENSITIVE −0.6 / +0.2 (healthy), −1.9 / +1.9 (risk).
  - With no move: ≈21.9% if IL players return on ESPN's dates (scenario, not a forecast; ROOM_RULE_ON SENSITIVE +1.0).

## Deck

- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 98 (1795351593-df51). Before: Version 97.
- The 739,633 built bytes are contained in the 740,179-byte live page, which renders 7 tabs with 0 page errors.
- **WROTE:** 56 path(s) (morning.py).

## Decision for David

1. **Bench White and Washington (both O) before tonight's lock (Recommended)** — today's last-day lineup has only five players with games; the 5-4 lead rides on them.
2. **Add Collin Gillespie, drop Andrew Wiggins** — +0.9 title if IL players never return, −0.3 if they return on time; Wiggins has a game today, so the swap is better made after tonight.
3. **Hold; no roster move** — the best pair's value flips sign between the two IL worlds.
