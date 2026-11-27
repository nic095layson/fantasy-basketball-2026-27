# Morning run — 2026-10-26 (Monday, week 2 day 1)

The 05:00 Pacific fire (12:09Z) reached this session at 14:29Z after a worker restart; the run started then. T0 2026-10-26T14:29:50Z. Step-4 path: `morning.py --since T0`. Repos already attached; kit head at start 13597a2; origin/main ec6264c already contained; tree clean, no stash.

## Result lines
- MORNING: PASS — 2026-10-26: 13 steps; brief report/briefs/brief_2026-10-26.md; record report/briefs/morning_2026-10-26.json
- LEAGUE LIVE: HALT (non-fatal) — "LEAGUE INTAKE: HALT — 1 name(s) not in the pool; nothing written: Trevon Brazile (Podz save the league, PF, DEN, status -)"; "intake refused the pull; league_state.json not touched (last paste stands)". The pull itself is pinned at data/source/flaim/pull_2026-10-26.json.
- MATCHUP LIVE: PASS — week 2, games left 39 mine / 39 Looking Cool Joker!
- BOX PULL: PASS — 2026-10-25: 7 games, 196 player lines, 132 in the pool, 64 unpooled; two outlets: 193 matched, 0 cells differ
- SEASON LINES: PASS — 8 box-score records, 286 pool players with games, 275 lines moved by 0.25+; 103 unpooled players with games
- SEASON BOARD: PASS — 275 movers listed
- STATUS GATE: PASS — status_2026-10-26.json: 22 flagged row(s), each tiered with a dated receipt
- TRANSACTIONS: PASS — 0 feed items 2026-10-24 to 2026-10-26
- WEEK MATCHUP: PASS — week 2 vs Looking Cool Joker!; to date rebuilt (Yahoo's week 2 totals could not be read: unreadable makes/attempts value '/'); to date 0 days; projected 6-3-0; pickups: no finished low-value player
- LEAGUE TABLE: FAIL (non-fatal) — "LEAGUE TABLE: FAIL — unreadable makes/attempts value '/'" (week 2 has no stats on day one)
- FORM BOARD: PASS — 172 rostered + 93 free agents, 244 with games over 6 box days
- SEASON DECK: PASS — 7 panes, 313 board rows, 22 status rows; record pins 12 inputs; render 7 tabs, 0 page errors
- AVAILABILITY CALIBRATION: INSUFFICIENT — median team games 3 < 15; first verdict near 2026-11-17. No value changed.
- MANAGER LOG: PASS — 2026-10-25: 12 lineups, 1 start lost league-wide (Looking Cool Joker!, Precious Achiuwa benched while playing); no box line outside IL: Ausar Thompson, Joel Embiid, Keegan Murray; profile 4 days; 11 new moves, 54 on record
- SCOREBOARD INTAKE: PASS — week 1: 6 matchups, 12 team lines; you 3-6-0 vs MAXEY-MUM OVERDRIVE (won FG%, FT%, TO); team_weeks.csv updated; week score scored, 4 mornings / 36 forecasts, Brier 0.034 vs lead-to-date 0.174

## Source pull
- Flaim: tools present. get_user_session (478.l.36464), get_league_info (currentWeek 2), 12 current rosters one at a time (12/12, no retries), get_matchups week 2 (current, all 0-0-9) and week 1 (all six "final"), get_free_agents (100), 12 dated lineups for 2026-10-25 one at a time (12/12), get_transactions (54 rows; Flaim excluded 6 malformed). Flaim complete.
- FantasyBot: outlook only (1 call). Its verdict is not quoted.

## What the halt means for today's outputs
The brief, waiver scan, title odds and deck were computed on the 2026-10-25 afternoon roster, not today's. Differences on your roster that they do not see (from today's Flaim pull):
- You added Julian Champagnie and dropped Noah Clowney (Yahoo tr.66). The brief's lineup omits Champagnie, and all three waiver pairs read "drop Noah Clowney".
- Kyrie Irving is now active (bench, no tag) and Kawhi Leonard is in your IL slot tagged Q. The brief still treats Kyrie as IL.
League moves file: not written today (the halt writes nothing).

## Brief (stale roster, as written)
- Lineup: PG Collin Gillespie, SG Ty Jerome, G Kevin Durant, SF Jaden McDaniels, PF Miles Bridges, F Yaxel Lendeborg, C Neemias Queta, C Kel'el Ware, Util Derrick White, Util Tyrese Haliburton; bench PJ Washington.
- Top waiver pair: add Bobby Portis, drop Noah Clowney, +0.202 cats/week, title 24.8% (+4.9). Not actionable as written: Clowney is already gone.
- Title odds 20.0% ± 0.6 (2 × 10,000 seasons); playoffs 98.8%. Structural band unchanged: TEAM_WEEK_SHOCK FRAGILE +2.3 / −3.4; weekly_availability FRAGILE −2.0 / +0.8 / −1.5 / +0.9. Computed on the stale roster.

## Week 1 final (Yahoo, recorded in data/weeks/week_1.json)
You lost 3-6 to MAXEY-MUM OVERDRIVE, winning FG%, FT% and TO. The kit had projected 3-6-0 all week.

## Deck
Republished as version 38 (id 1793025305-e4a8). Read after: 460,948 bytes live, 460,402 built, built content inside the live page, seven tabs present once, stamp 2026-10-26T14:34:32Z.

## Decisions for the owner (nothing changed by me)
1. Trevon Brazile is not in the projection pool, so every run halts league live until the pool or the intake rule changes. Options: add him to the pool by your usual pool process; or let the intake carry unpooled names through (an engine change). Until then each morning's roster stays frozen at 2026-10-25.
2. league_table.py fails on day one of every week ("/" values). week_matchup.py already falls back to a rebuild in the same case; the table needs the same handling (a code change).
