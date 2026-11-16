# Morning run 2026-11-16

**MORNING: PASS — 2026-11-16: 28 steps; brief report/briefs/brief_2026-11-16.md; record report/briefs/morning_2026-11-16.json**

- **Schedule:** fired 12:41:48Z. T0 2026-11-16T12:42:10Z. Path: `morning.py --since <T0>`. Monday: season sweep and scoreboard intake ran.
- **Repos:** kit already attached; deck repo up to date. Tree clean, no stash. season/daily already up to date with origin/main (the #271 fix came in at the 11-15 afternoon merge).
- **Fix check:** the daily brief step that failed on 11-15 passed today with Mario Hezonja on the roster (#271).
- **Flaim:** tools present; league 478.l.36464. 12 of 12 rosters, matchups week 5, week 4 finals, available players (100), standings, 12 of 12 dated lineups for 2026-11-15, transactions (99 rows; Flaim again could not interpret 1 Yahoo entry). No errors, no retries.
- **FantasyBot:** outlook only (1 call; Flaim was complete).

## Step lines

- LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-16.json; 6 not in the deck pool (simulated once the season lines give an auto row, 3+ games): Sidy Cissoko, Nolan Traore, Tyrese Proctor, Meleek Thomas, Mario Hezonja, Danny Wolf
- MATCHUP LIVE: PASS — week 5, games left 36 mine / 37 Thompson Telepathy
- WEEK MATCHUP: PASS — 2026-11-16: week 5 vs Thompson Telepathy; to date from Yahoo (rebuild agrees); to date 0 day(s), 0 missing; projected 5-4-0; pickups: no finished low-value player
- BOX PULL: PASS — 2026-11-15: 9 games, 231 player lines; two outlets: 231 matched, 0 cells differ
- TAG OUTCOMES: PASS — 2026-11-15: 41 flagged player(s) 20 no game, 6 played, 13 sat, 2 unresolved
- MINUTES LINE: PASS — 344 players, 298 with games; ratio >= 1.10 for 5, <= 0.90 for 22; candidate only. *A candidate, not the projection.*
- THREES LINE: PASS — candidate above the live line by 0.2+ for 24, below for 13; candidate only.
- SEASON SWEEP: PASS — 6,000 seasons x seeds [2026, 2027] on deck c933f07; MC SE 0.54; baseline within 3 SE of the 10k reference: {'2026': True, '2027': True}
- MANAGER LOG: PASS — 2026-11-15: 12 lineups, 0 start(s) lost league-wide; outside IL, team played but no box line: Andrew Nembhard, Chet Holmgren, De'Aaron Fox, Joel Embiid, Kyrie Irving, Ryan Rollins; 3 new move(s), 171 on record. 12 of 12 dated lineups; transactions came back. The prompt's separate run recorded 0 new moves.
- SCOREBOARD INTAKE: PASS — week 4: 6 matchups, 12 team lines; you 4-5-0 vs SNOWTIME WHITE WALKERS (won FT%, 3PTM, BLK, TO); team_weeks.csv updated; week score scored, 6 mornings / 54 forecasts, Brier 0.134 vs lead-to-date 0.176; accuracy week 4: 240 players, points 13.26 projected / 12.55 actual; 6 league matchup(s) scored (Brier 0.217); fit through week 4, weeks [1, 2, 3, 4], 48 team-weeks; shock 0.1069 ± 0.0132 (live 0.06); availability 0.00: 0.06 ± 0.02 (n 103), 0.75: 0.56 ± 0.02 (n 438), 0.79: 0.88 ± 0.06 (n 26), 0.88: 0.78 ± 0.01 (n 3694); board comparison mild 1.14 ± 0.08 vs deck 0.85 / sim 0.8977 / kit 0.8249, risk 0.72 ± 0.03 vs deck 0.78 / sim 0.8523 / kit 0.9036; proposal; proposes only. *Accuracy and fit are proposals only.*
- TITLE WATCH: PASS — title 14.6% (was 19.5% on 2026-11-14), −4.9 against a band of ±0.7: MOVED. Names 1 kit merge (#271) and 3 teams' roster changes.
- DECISION CARD: PASS — 3 pair(s); order changes between the worlds; top pair holds in 4 of 4.
- LEAGUE TABLE: PASS — power #1 SNOWTIME WHITE WALKERS (0.633), you #6 (0.527); Yahoo W-L-T matches the kit's finished weeks.
- STATUS GATE: PASS — status_2026-11-16.json: 34 flagged row(s), each tiered with a dated receipt
- DRAFT CHECK: PASS — 13 picks, rank agreement 0.713; ranked 1 on draft day, stand 3 (21-15-0).

## League moves (league_moves_2026-11-16.json)

- **Scottie’s Thotties** — added Alex Caruso; dropped Precious Achiuwa
- **ANONG NANGIANNIS?!** — dropped Tre Jones; off IL: Alex Sarr
- **John's Cool Team** — added De'Andre Hunter; dropped Bones Hyland
- Your roster and Thompson Telepathy's: no move.

## Brief

- **Week 4 final:** lost 4-5 to SNOWTIME WHITE WALKERS. Standings 21-15-0, 3rd.
- **Lineup today:** PG White, SG Durant, SF Cam Johnson, PF Lendeborg, F Bridges, C Queta, Util McDaniels. No game: Ware, Irving, Washington, Collins. Ty Jerome (O) is in Yahoo's PG slot, Irving (O) on the bench.
- **Waiver scan:** 18 of 520 pairs raise expected weekly category wins (base 4.759). Top pair: add **Julian Champagnie**, drop Mario Hezonja: +0.107 cats/week; title 17.7% (+3.0); "you dropped him 2026-11-15". Decision card: under the weekly_availability band it holds in 4 of 4 settings (+2.5 to +3.6); if IL players return on ESPN's dates it is −1.0, and the order changes between the two worlds.
- **Waiver scan status:** "Status from Yahoo and ESPN. Set aside as Out: Jalen Williams (Out, espn, ESPN's earliest return 2027-03-02), Cason Wallace (O, yahoo, ESPN's earliest return 2027-03-02), Kevin Porter Jr. (NA, yahoo), Justin Champagnie (O, yahoo, ESPN's earliest return 2027-02-25), Bradley Beal (Out, espn, ESPN's earliest return 2026-11-29)."
- **Title:** 14.6% ± 0.5 (2 runs × 10,000 seasons). Playoffs: 97.0%. Structural band (season sweep of today): weekly_availability is FRAGILE, −3.2 / +2.8. If IL players return on ESPN's dates ≈26.3% (scenario, not a forecast; room rule FRAGILE +5.2).
- **Season lines:** 302 lines moved by 0.25+ (report/season/board_2026-11-16.md). 6 auto rows.

## Flag (not acted on)

- The waiver scan's third pair, "add Meleek Thomas", names a player rostered by MISSI ELLIOTT (Yahoo roster today, BN); he is not in the available-player pull. The decision card notes "add not in today's free-agent pool". The scan appears to treat an unpooled rostered player as available. Recorded only; nothing changed.

## Deck

- **SEASON DECK:** PASS — 2026-11-16: report/season/deck_2026-11-16.html (7 panes, 315 board rows, 34 status rows; record deck_record_2026-11-16.json pins 21 inputs; render: 7 tabs, 0 page errors)
- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 86 (1794833419-7ece). The 703,252 built bytes are contained in the 703,798-byte live page; all 7 tab names are present. Before: Version 85 (afternoon of 2026-11-14).
- **WROTE:** 52 path(s) (morning.py).

## Decision for David (unattended run: options, not a card)

The waiver scan proposed a rostered player (Meleek Thomas) as an add.
1. **Have main fix the scan so rostered unpooled players are never offered as adds (Recommended).** Small; the other two pairs are real free agents.
2. **Leave it;** read pairs against Yahoo before acting.
