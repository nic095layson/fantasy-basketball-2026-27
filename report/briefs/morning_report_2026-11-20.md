# Morning run 2026-11-20

**MORNING: FAIL — 2026-11-20: step 'season deck' failed (exit 1); later steps skipped; record report/briefs/morning_2026-11-20.json**

- **Failed step:** `SEASON DECK: FAIL — 2026-11-20: rostered player(s) with no season-board or held row: ['Landry Shamet']`.
  - ANONG NANGIANNIS?! added Landry Shamet this morning.
  - He has a row in data/season/pool_season.csv but no row in data/season/projections_season.csv.
  - LEAGUE LIVE did not list him as unpooled.
  - Season deck is morning.py's last step, so nothing else was skipped.
  - This is not a fetch step, so the 2-hour re-check rule does not apply. Nothing in the engine was changed.
- **Schedule:** fired 12:41:27Z. T0 2026-11-20T12:41:47Z. Path: `morning.py --since <T0>`. Friday, so no Monday or Sunday extras.
- **Repos:** kit already attached; deck repo pulled. Tree clean, no stash. origin/main (4fe235c, through #297) merged into season/daily.
- **Flaim:** league 478.l.36464.
  - Returned: 12 of 12 rosters (one call at a time), matchups for week 5, 100 available players, standings, 12 of 12 dated lineups for 2026-11-19, transactions (99 rows).
  - Flaim again could not interpret 1 Yahoo entry. No errors, no retries.
- **FantasyBot:** outlook only (1 call; Flaim was complete).

## Step lines

- LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-20.json; 6 not in the deck pool: Nolan Traore, Javon Small, Tyrese Proctor, Y. Konan Niederhäuser, Matisse Thybulle, Danny Wolf
- MATCHUP LIVE: PASS — week 5, games left 16 mine / 15 Thompson Telepathy
- WEEK MATCHUP: PASS — 2026-11-20: week 5 vs Thompson Telepathy; to date from Yahoo (rebuild differs on 2 stat(s)); to date 4 day(s), 0 missing; projected 8-1-0
- BOX PULL: PASS — 2026-11-19: 4 games, 105 player lines, 68 in the pool, 37 unpooled; single-source (ESPN only)
- MANAGER LOG: PASS — 2026-11-19: 12 lineups, 0 start(s) lost league-wide; outside IL, team played but no box line: Draymond Green, Myles Turner, Ty Jerome, Yanic Konan Niederhäuser, Zach Edey; 7 new move(s), 196 on record; Flaim could not read 1 row
- TAG OUTCOMES: PASS — 2026-11-19: 37 flagged player(s) 25 no game, 3 played, 8 sat, 1 unresolved
- MINUTES LINE: PASS — 2026-11-20: 343 players, 298 with games; ratio >= 1.10 for 6, <= 0.90 for 21; 38 unscaled (no preseason mpg); full candidate from the blend (PTS/REB/AST switched in season lines)
- THREES LINE: PASS — candidate above the live line by 0.2+ for 18, below for 12; candidate only
- SEASON LINES: PASS — 303 lines moved by 0.25+; 5 auto rows; 156 unpooled players with games; 1 tag override
- STATUS GATE: PASS — status_2026-11-20.json: 36 flagged row(s), each tiered with a dated receipt
- TITLE WATCH: PASS — title 14.2% (was 13.6% on 2026-11-19), +0.6 against a band of ±0.7: within the band
- DECISION LOG: PASS — R-2026-11-20-01 add_drop Cameron Johnson for Andrew Wiggins; moves: nothing new
- DECISION CARD: PASS — 3 pair(s); order changes between the worlds; top pair holds in 4 of 4
- LEAGUE TABLE: PASS — power #1 ROOKS FTW (0.634), you #6 (0.547); Yahoo W-L-T matches the kit's finished weeks
- SEASON DECK: **FAIL** (above)

## League moves (league_moves_2026-11-20.json)

- **Thompson Telepathy (your opponent)** — added Javon Small
- **ANONG NANGIANNIS?!** — added Landry Shamet; dropped Brice Sensabaugh; to IL: Collin Murray-Boyles; off IL: Toumani Camara
- **MISSI ELLIOTT** — added Jordan Poole; dropped Meleek Thomas
- **Podz save the league** — added Y. Konan Niederhäuser; to IL: Alperen Sengun, Deni Avdija
- **ROOKS FTW** — added Jaxson Hayes; dropped Mo Bamba
- **SNOWTIME WHITE WALKERS** — added Julian Champagnie; dropped Kevin Huerter

## Brief

- **Week 5 live (Yahoo):** you lead Thompson Telepathy 8-1 after four days; games left 16 / 15. Standings 21-15-0, 3rd.
- **Lineup today (daily-fill rule):** SG Durant, PF Collins, F Bridges. The other 10 have no game today. Ty Jerome (O) is still in your active SG slot on Yahoo; Memphis has no game today.
- **Waiver scan:** 4 of 520 pairs raise expected weekly category wins (base 4.960).
  - Top pair: add **Cameron Johnson**, drop Andrew Wiggins: +0.010 cats/week; title 14.7% (+0.5). You dropped him 2026-11-18.
  - Then Kevin Huerter (+0.1; on waivers until 2026-11-21) and Alex Caruso (+0.2; Q today).
- **Decision card:** if IL players return on ESPN's dates, all three pairs are worth +0.0 to +0.1. Under the weekly_availability band the top pair holds in 4 of 4 settings (+0.1 to +0.6). The order of the pairs changes between the two worlds.
- **Waiver scan status:** "Status from Yahoo and ESPN. Set aside as Out: Jalen Williams (Out, espn, ESPN's earliest return 2027-03-02), Cason Wallace (O, yahoo, ESPN's earliest return 2027-03-02), Tobias Harris (O, yahoo, ESPN's earliest return 2026-12-03), Kevin Porter Jr. (NA, yahoo), Justin Champagnie (O, yahoo, ESPN's earliest return 2027-02-25), Bradley Beal (Out, espn, ESPN's earliest return 2026-11-29)."
- **Title:** 14.2% ± 0.5 (2 runs × 10,000 seasons). Playoffs: 98.4%.
  - Structural band (season sweep of 2026-11-17): no FRAGILE constant. The largest, weekly_availability, is SENSITIVE: −0.6 / +0.2 (healthy) and −1.9 / +1.9 (risk tier).
  - With no move: 22.2% if IL players return on ESPN's dates (scenario, not a forecast).
- **Season lines:** 303 movers (report/season/board_2026-11-20.md). 5 auto rows; 156 unpooled players with games.

## Deck

- **Not published.** The deck step failed, so no deck_2026-11-20.html was built.
- The live page stays at Version 93 (yesterday afternoon): https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe
- **WROTE:** 44 path(s) (morning.py).

## Decision for David

1. **Hold; no roster move today (Recommended)** — you lead 8-1, and the best pair is worth +0.5 if IL players never return and +0.0 if they return on time.
2. **Add Cameron Johnson, drop Andrew Wiggins** — +0.5 title if IL players never return. You dropped him two days ago.
3. **For the deck failure:** have a kit session add Landry Shamet's season line, or decide how the deck should treat a pooled player without a line. While he stays rostered without a line, the afternoon deck rebuild runs the same check (not tested).
