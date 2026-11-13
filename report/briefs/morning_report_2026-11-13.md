# Morning run 2026-11-13

**MORNING: PASS — 2026-11-13: 24 steps; brief report/briefs/brief_2026-11-13.md; record report/briefs/morning_2026-11-13.json**

- **Late fire:** the scheduled task was set for 13:01:54Z but fired at 15:17:16Z. The cause was not traced. The container had restarted, and the Flaim tools reconnected first.
- **T0:** 2026-11-13T15:17:37Z. Path: `morning.py --since <T0>` (`--help` lists `--since`). Friday: no Monday or Sunday steps.
- **Repos:** the kit was already attached (push rights to season/daily); the deck repo pulled (4 files changed). Tree clean, no stash. season/daily was already up to date with origin/main (8dc596d).
- **Flaim:** tools present; league 478.l.36464.
  - 12 of 12 rosters (one at a time), matchups week 4, available players (100), standings, 12 of 12 dated lineups for 2026-11-12. No errors, no retries.
  - Transactions: 99 rows. Flaim again warned that 1 Yahoo entry could not be interpreted (`omitted_unrecognized_rows: 1`).
- **FantasyBot:** tools present; outlook only (1 call; Flaim was complete).
- **LEAGUE LIVE:** PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-13.json; 4 not in the deck pool (simulated once the season lines give an auto row, 3+ games): Nolan Traore (ANONG NANGIANNIS?!, IL), Morez Johnson Jr. (Podz save the league, PF), Meleek Thomas (MAXEY-MUM OVERDRIVE, SG), Danny Wolf (John's Cool Team, BN)
- **MATCHUP LIVE:** PASS — week 4, games left 18 mine / 20 SNOWTIME WHITE WALKERS.
- **WEEK MATCHUP:** PASS — 2026-11-13: week 4 vs SNOWTIME WHITE WALKERS; to date from Yahoo (rebuild agrees); to date 4 day(s), 0 missing; projected 5-4-0; pickups: no finished low-value player; pool pool_season.csv
- **BOX PULL:** PASS — 2026-11-12: 4 games, 104 player lines; two outlets: 104 matched, 0 cells differ. No retry needed.

## League moves (league_moves_2026-11-13.json)

Your roster and SNOWTIME's: no move.
- **Looking Cool Joker!** — added Sion James; dropped Nique Clifford
- **Scottie’s Thotties** — to IL: Stephen Curry; off IL: Precious Achiuwa
- **ANONG NANGIANNIS?!** — added Tre Jones; dropped Jalen Green
- **Cade n em** — to IL: Caleb Wilson; off IL: Ajay Mitchell
- **Thompson Telepathy** — added Oso Ighodaro; dropped Robert Williams III; to IL: LeBron James; off IL: Devin Vassell
- **Podz save the league** — to IL: Klay Thompson; off IL: Morez Johnson Jr.
- **ROOKS FTW** — added De'Anthony Melton; dropped Ryan Kalkbrenner; to IL: Evan Mobley; off IL: Paul George
- **MAXEY-MUM OVERDRIVE** — added Ja'Kobe Walter; dropped Isaiah Collier

## Step lines

- **TAG OUTCOMES:** PASS — 2026-11-12: 33 flagged player(s) 23 no game, 2 played, 7 sat, 1 unresolved; data/status/tag_outcomes.jsonl
- **MINUTES LINE:** PASS — 2026-11-13: 342 players, 297 with games; ratio >= 1.10 for 7, <= 0.90 for 28; 36 unscaled (no preseason mpg); candidate only. *A candidate, not the projection.*
- **THREES LINE (new step, #267):** PASS — 2026-11-13: 342 players, 233 split, 109 unsplit; candidate above the live line by 0.2+ for 25, below for 19; candidate only. *A candidate, not the projection.*
- **TITLE WATCH:** PASS — title 20.6% (was 20.2% on 2026-11-12), +0.3 against a band of ±0.8: within the band.
- **DECISION CARD:** PASS — 1 pair(s); same order in both worlds; top pair holds in 2 of 4.
- **LEAGUE TABLE:** PASS — power #1 ROOKS FTW (0.611), you #5 (0.535); Yahoo W-L-T matches the kit's finished weeks for 12 teams.
- **STATUS GATE:** PASS — status_2026-11-13.json: 36 flagged row(s), each tiered with a dated receipt
- **MANAGER LOG:** PASS — 2026-11-12: 12 lineups, 0 start(s) lost league-wide; outside IL, team played but no box line (inactive or unmatched name): LeBron James, Scottie Barnes; profile 2026-10-22..2026-11-12 (21 day(s)); 5 new move(s), 161 on record; Flaim could not read 1 row(s) on Yahoo's page (the moves on record may be short). 12 of 12 dated lineups; transactions came back.
  - morning.py now runs the manager log as its own step. The prompt's separate manager_log.py run then re-ran it: same day, "0 new move(s), 161 on record". Nothing was double-counted.

## Brief

- **Lineup today (players with a game):** PG Ty Jerome, SG Kevin Durant, SF Julian Champagnie, PF Yaxel Lendeborg, C Kel'el Ware. No game: White, Irving, Cameron Johnson, Collins, Washington, McDaniels, Bridges, Queta.
- **Top waiver pair:** add Tobias Harris (SAS), drop Cameron Johnson. It is worth +0.002 cats/week; title 20.4% (-0.2).
  - Harris is "O today (yahoo), ESPN's earliest return 2026-11-19, check before claiming".
  - Decision card: −0.2 if IL players never return, +0.1 if they return on time. Under the weekly_availability band it holds in 2 of 4 settings (−0.5 to +0.2). In short, a near-zero pair.
- **Waiver scan status:** "Status from Yahoo and ESPN. Set aside as Out: Jalen Williams (Out, espn, ESPN's earliest return 2027-03-02), Cason Wallace (O, yahoo, ESPN's earliest return 2027-03-02), Kevin Porter Jr. (NA, yahoo), Justin Champagnie (O, yahoo, ESPN's earliest return 2027-02-25), Bradley Beal (Out, espn, ESPN's earliest return 2026-11-29), Scotty Pippen Jr. (O, yahoo, ESPN's earliest return 2026-11-21)."
- **Title:** 20.6% ± 0.6 (2 runs × 10,000 seasons). Playoffs: 98.9%. Structural band (season sweep of 2026-11-09, 4 days old): weekly_availability is FRAGILE, −4.8 / +2.9.
- **Season lines:** 302 lines moved by 0.25+ (report/season/board_2026-11-13.md). 151 unpooled players have games. 4 auto rows (Nolan Traore 10g, Morez Johnson Jr. 11g, Meleek Thomas 9g, Danny Wolf 6g).

## Deck

- **SEASON DECK:** PASS — 2026-11-13: report/season/deck_2026-11-13.html (7 panes, 315 board rows, 36 status rows; record deck_record_2026-11-13.json pins 21 inputs; render: 7 tabs, 0 page errors)
- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 81 (1794583430-db8c). The 699,475 built bytes are contained in the 700,021-byte live page. All 7 tab names (Today, Trade Analyzer, Free Agents, Board, Draft Check, Week, League) are present.
- The live page before this publish was Version 80 (1794524785-ee34), yesterday afternoon's runner page.
- **WROTE:** 45 path(s) (morning.py).

## Nothing failed
