# Morning run 2026-11-15

**MORNING: FAIL — 2026-11-15: step 'daily brief' failed (exit 1); later steps skipped; record report/briefs/morning_2026-11-15.json**

- **Schedule:** fired 12:40:57Z (scheduled 12:40Z). T0 2026-11-15T12:41:27Z. Path: `morning.py --since <T0>`. Sunday: next week forecasts ran.
- **Repos:** kit already attached; deck repo up to date. Tree clean, no stash. season/daily already up to date with origin/main.
- **Flaim:** tools present; league 478.l.36464. 12 of 12 rosters, matchups week 4, available players (100), standings, 12 of 12 dated lineups for 2026-11-14, transactions (99 rows; Flaim again could not interpret 1 Yahoo entry). No errors, no retries.
- **FantasyBot:** outlook only (1 call; Flaim was complete).

## Step lines (PASS before the failure)

- LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-15.json; 6 not in the deck pool (simulated once the season lines give an auto row, 3+ games): Sidy Cissoko (Looking Cool Joker!, UTIL), Nolan Traore (ANONG NANGIANNIS?!, BN), Tyrese Proctor (Podz save the league, SG), Meleek Thomas (MISSI ELLIOTT, BN), Mario Hezonja (KEL'EL YAXEL HALQUETA, BN), Danny Wolf (John's Cool Team, C)
- MATCHUP LIVE: PASS — week 4, games left 7 mine / 10 SNOWTIME WHITE WALKERS
- BOX PULL: PASS — 2026-11-14: 5 games, 132 player lines, 85 in the pool, 47 unpooled; single-source (ESPN only)
- MANAGER LOG: PASS — 2026-11-14: 12 lineups, 0 start(s) lost league-wide; outside IL, team played but no box line (inactive or unmatched name): Donovan Mitchell, Jalen Smith, Nic Claxton, Pelle Larsson, Ty Jerome; 3 new move(s), 168 on record. The prompt's separate manager_log run then recorded 0 new moves.
- TAG OUTCOMES: PASS — 2026-11-14: 33 flagged player(s) 21 no game, 2 played, 9 sat, 1 unresolved
- MINUTES LINE: PASS — 344 players, 298 with games; ratio >= 1.10 for 6, <= 0.90 for 25; candidate only. *A candidate, not the projection.*
- THREES LINE: PASS — candidate above the live line by 0.2+ for 22, below for 16; candidate only.
- SEASON LINES: PASS — 301 lines moved by 0.25+; 6 auto rows (Sidy Cissoko 12g, Nolan Traore 11g, Tyrese Proctor 13g, Meleek Thomas 11g, Mario Hezonja 14g, Danny Wolf 7g); 152 unpooled players with games.
- STATUS GATE: PASS — status_2026-11-15.json: 41 flagged row(s), each tiered with a dated receipt
- NEXT WEEK FORECASTS: WEEKLY PREVIEW: PASS — week 5
- IL RETURN: PASS

## The failure

- `scripts/daily_brief.py` line 298 raised StopIteration: it looks up the weakest player on your sim roster in your league_state player list and finds no match.
- Cause, from the records: your roster gained **Mario Hezonja** (added, Julian Champagnie dropped, Yahoo 2026-11-15). Hezonja is not in the pool; league_state carries him under `unpooled`, not in your team's player list, while the sim roster includes his auto row. He is the only player on your sim roster missing from that list, so the lookup has nothing to find. The engine was not changed.
- Not a fetch failure, so the retry rule does not apply and no re-check was scheduled.
- **Skipped:** decision log, title watch, week matchup, decision card, league table, form board, season deck. No title figure, waiver pair or lineup today.
- **Deck not published:** no deck_2026-11-15.html was built. The live page stays Version 85 (afternoon of 2026-11-14).

## League moves (league_moves_2026-11-15.json)

- **You** — added Mario Hezonja; dropped Julian Champagnie
- **SNOWTIME WHITE WALKERS** — to IL: James Harden; off IL: Luka Doncic
- **ANONG NANGIANNIS?!** — added Zaccharie Risacher; dropped Jamal Shead; to IL: Alex Sarr; off IL: Nolan Traore
- **Thompson Telepathy** — to IL: Austin Reaves; off IL: LeBron James
- **Podz save the league** — to IL: Nic Claxton; off IL: Brandon Miller, Klay Thompson
- **John's Cool Team** — added Bones Hyland; dropped Kyle Kuzma

## Decision for David (unattended run: options, not a card)

The brief fails every day while a player of yours sits outside the pool.
1. **Have main fix daily_brief.py so the streaming step handles an unpooled player on your roster (Recommended).** A small code fix; it restores the brief, title watch and deck tomorrow.
2. **Add Hezonja to the pool through the edit-CSV workflow.** Puts a projection line on him; it is a projection change, so it is your call.
3. **Leave it.** No brief, title figure or deck until Hezonja leaves your roster.

- **WROTE:** 41 path(s) (morning.py).
