# Morning run 2026-11-23

**MORNING: PASS — 2026-11-23: 28 steps; brief report/briefs/brief_2026-11-23.md; record report/briefs/morning_2026-11-23.json**

- **Schedule:** T0 2026-11-23T12:41:44Z. Path: `morning.py --since <T0>`. Monday, so the season sweep ran and the scoreboard intake was run for week 5.
- **Repos:** kit already attached; deck repo pulled. season/daily already up to date at 3c3ce35. Tree clean, no stash.
- **Flaim:** league 478.l.36464.
  - Returned: 12 of 12 rosters (one call at a time), matchups for week 6, week 5 finals, 100 available players, standings, 12 of 12 dated lineups for 2026-11-22, transactions (99 rows).
  - Flaim again could not interpret 1 Yahoo entry. No errors, no retries.
- **FantasyBot:** outlook only (1 call; Flaim was complete).

## Step lines

- LEAGUE LIVE: PASS — pinned data/source/flaim/pull_2026-11-23.json; 4 not in the deck pool: Nolan Traore (ANONG NANGIANNIS?!, G), Charles Bassey (Podz save the league, C), Caleb Martin (Podz save the league, UTIL), Matisse Thybulle (John's Cool Team, SG)
- MATCHUP LIVE: PASS — week 6, games left 37 mine / 34 Booker T Floppers
- BOX PULL: PASS — 2026-11-22: 7 games, 179 player lines, 125 in the pool, 54 unpooled; two outlets: 172 matched, 7 cells differ
- MANAGER LOG: PASS — 2026-11-22: 12 lineups, 0 starts lost league-wide; 4 new moves, 206 on record; Flaim could not read 1 row
- TAG OUTCOMES: PASS — 2026-11-22: 39 flagged: 16 no game, 6 played, 16 sat, 1 unresolved
- SEASON LINES: PASS — 303 lines moved by 0.25+; 4 auto rows (Traore 14g, Bassey 15g, Martin 13g, Thybulle 17g); 157 unpooled players with games; 1 tag override
- MINUTES LINE: PASS — 342 players, 297 with games; ≥1.10 for 6, ≤0.90 for 22; 37 unscaled
- THREES LINE: PASS — above the live line by 0.2+ for 19, below for 12; candidate only
- STATUS GATE: PASS — status_2026-11-23.json: 39 flagged rows
- SEASON SWEEP: `SWEEP: 6,000 seasons x seeds [2026, 2027] on deck 3551a15; MC SE 0.54; baseline within 3 SE of the 10k reference: {'2026': True, '2027': True}`
- DECISION LOG: PASS — R-2026-11-23-01 add_drop Cameron Johnson for Andrew Wiggins; moves: nothing new
- DECISION GRADE: PASS — 44 rows, 4 new final, 33 pending
- DRAFT CHECK: PASS — rank agreement 0.735; ranked 1 on draft day, stand 3 (27-18-0)
- TITLE WATCH: PASS — title 13.2% (was 13.1%), +0.2 against a band of ±0.7: within the band
- WEEK MATCHUP: PASS — week 6 vs Booker T Floppers; to date from Yahoo (rebuild agrees); 0 days, 0 missing; projected 6-3-0
- DECISION CARD: PASS — 3 pairs; order changes between the worlds; top pair holds in 4 of 4
- LEAGUE TABLE: PASS — power #1 ROOKS FTW (0.629), you #6 (0.520); Yahoo W-L-T matches the kit's finished weeks
- SEASON DECK: PASS — report/season/deck_2026-11-23.html (7 panes, 316 board rows, 39 status rows; render: 7 tabs, 0 page errors)

## Scoreboard intake (week 5)

- `SCOREBOARD INTAKE: PASS — week 5: 6 matchups, 12 team lines; you 6-3-0 vs Thompson Telepathy (won FT%, 3PTM, PTS, AST, BLK, TO)`
- Accuracy: "accuracy week 5: 242 players, points 12.82 projected / 12.18 actual; 6 league matchup(s) scored (Brier 0.162)"
- Fit (proposal only): "fit through week 5, weeks [1, 2, 3, 4, 5], 60 team-weeks; shock 0.1166 ± 0.0134, level-relative 0.1049 (live 0.11); level (actual/model) 1.112; in-week factor F 1.68 (df 11, 48); … board comparison mild 1.18 ± 0.07 vs deck 0.85 / sim 0.9875 / kit 0.8249, risk 0.72 ± 0.03 vs deck 0.78 / sim 0.8125 / kit 0.9036; proposal; proposes only"

## League moves (league_moves_2026-11-23.json)

- **ANONG NANGIANNIS?!** — to IL: Giannis Antetokounmpo, OG Anunoby; off IL: Collin Murray-Boyles, Nolan Traore
- **Podz save the league** — added Caleb Martin, Charles Bassey; to IL: Aday Mara, Brandon Miller
- **John's Cool Team** — added Sam Hauser; dropped Danny Wolf, Max Strus; off IL: Brandon Ingram

## Brief

- **Week 5 final:** won 6-3 over Thompson Telepathy. Standings 27-18-0, 3rd.
- **Week 6:** vs Booker T Floppers; games left 37 / 34.
- **Lineup today (daily-fill rule):** PG Spencer, SG Jerome, G Durant, SF McDaniels, PF Bridges, C Ware. No game: White, Queta, Irving, Washington, Wiggins, Lendeborg, Collins.
- **Waiver scan:** 6 of 520 pairs raise expected weekly category wins (base 4.855).
  - Top pair: add **Cameron Johnson**, drop Andrew Wiggins: +0.030 cats/week; title 14.0% (+0.8).
  - Then Collin Gillespie (+1.1) and Jordan Goodwin (+0.0).
- **Decision card:** Johnson +0.8 if IL players never return, +0.3 if they return on time, +0.04 categories this week. Gillespie +1.1 / −0.7. The order changes between the two worlds.
- **Waiver scan status:** "Set aside as Out: Jalen Williams, Cason Wallace, Tobias Harris, Kevin Porter Jr., Justin Champagnie" (receipts in the brief).
- **Title:** 13.2% ± 0.5 (2 runs × 10,000 seasons). Playoffs 98.1%.
  - Structural band (today's sweep): no FRAGILE constant; weekly_availability SENSITIVE −1.1 / +0.5 (healthy), −1.5 / +1.2 (risk).
  - With no move: ≈21.7% if IL players return on ESPN's dates (scenario, not a forecast; ROOM_RULE_ON now ROBUST).

## Deck

- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 100 (1795438082-823d). Before: Version 99.
- The 763,437 built bytes are contained in the 763,983-byte live page, which renders 7 tabs with 0 page errors.
- **WROTE:** 57 path(s) (morning.py).

## Decision for David

1. **Add Cameron Johnson, drop Andrew Wiggins (Recommended)** — the only pair positive in both IL worlds (+0.8 / +0.3) and +0.04 categories this week.
2. **Add Collin Gillespie, drop Andrew Wiggins** — larger if IL players stay out (+1.1), but −0.7 if they return on time.
3. **Hold; no roster move.**
