# Morning run — 2026-10-25 (Sunday, week 1, last day of the scoring week)

T0 2026-10-25T12:03:14Z (fire 12:02:41Z). Step-4 path: `morning.py --since T0` (the flag is listed). Repos already attached; kit head at start 01215bc, origin/main ec6264c already contained (merge "Already up to date"); tree clean, no stash. Deck repo pulled (already up to date).

## Result lines
- PREFLIGHT: PASS — kit morning run: 4 checks
- LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-10-25.json
- MATCHUP LIVE: PASS — week 1, games left 5 mine / 9 MAXEY-MUM OVERDRIVE
- BOX PULL: PASS — 2026-10-24: 8 games, 219 player lines, 151 in the pool, 68 unpooled; two outlets: 209 matched, 9 cells differ, 1 ESPN-only, 0 bref-only
- SEASON LINES: PASS — 2026-10-25: 7 box-score records, 283 pool players with regular-season games, 261 lines moved by 0.25+; 96 unpooled players with games; 1 tag override(s)
- SEASON BOARD: PASS — report/season/board_2026-10-25.md (261 movers listed)
- STATUS GATE: PASS — status_2026-10-25.json: 26 flagged row(s), each tiered with a dated receipt
- TRANSACTIONS: PASS — 2 feed item(s) 2026-10-23 to 2026-10-25; 0 name a pool player
- DAILY BRIEF: PASS — report/briefs/brief_2026-10-25.md
- WEEK MATCHUP: PASS — 2026-10-25: week 1 vs MAXEY-MUM OVERDRIVE; to date from Yahoo (rebuild differs on 18 stat(s)); to date 5 day(s), 0 missing; projected 3-6-0; pickups ran (drop PJ Washington, 82 free agents scored from the Yahoo list)
- LEAGUE TABLE: PASS — week 1 in progress; power #1 Booker T Floppers (0.768), you #4 (0.551)
- FORM BOARD: PASS — 170 rostered + 100 free agents, 248 with games over 5 box days (2026-10-20 to 2026-10-24)
- SEASON DECK: PASS — report/season/deck_2026-10-25.html (7 panes, 313 board rows, 26 status rows; record pins 12 inputs; render 7 tabs, 0 page errors)
- MORNING: PASS — 2026-10-25: 13 steps; brief report/briefs/brief_2026-10-25.md; record report/briefs/morning_2026-10-25.json
- AVAILABILITY CALIBRATION: INSUFFICIENT — median team games 2 < 15 (population 154: healthy 138, mild 1, risk 15; regular-season team-games on file 72); first verdict expected near 2026-11-17. No value changed.
- MANAGER LOG: PASS — 2026-10-24: 12 lineups, 0 start(s) lost league-wide; outside IL, team played but no box line (inactive or unmatched name): Fred VanVleet, LeBron James, Yves Missi; profile 2026-10-22..2026-10-24 (3 day(s)); 7 new move(s), 43 on record
- SCOREBOARD INTAKE: not run (Sunday; the Monday rule applies tomorrow for week 1)

## Source pull
- Flaim: tools present; get_user_session (league 478.l.36464), get_league_info (currentWeek 1), 12 current rosters one at a time (12 of 12, no retries), get_matchups (week 1, all six in_progress), get_free_agents (100 returned), 12 dated lineups for 2026-10-24 one at a time (12 of 12, no retries), get_transactions (43 rows in the 30-day window; Flaim excluded 6 malformed rows). Flaim complete.
- FantasyBot: tools present; get_matchup_outlook once (live scoring, 5 left to play mine / 9 opponent). The 13 roster calls were not needed. Its verdict and win figure are not quoted.

## Yahoo week 1 to date (Sunday morning, from get_matchups)
KEL'EL YAXEL HALQUETA 6-3 vs MAXEY-MUM OVERDRIVE (winning FG%, FT%, 3PTM, REB, BLK, TO; losing PTS, AST, ST), 5 games left mine / 9 theirs. The kit's pre-week projection stands at 3-6-0. Week 1 closes tonight; Monday's run records the finals.

## League moves since the 2026-10-24 morning state (league_moves_2026-10-25.json)
- KEL'EL YAXEL HALQUETA (yours): added Noah Clowney; Kyrie Irving to IL (Yahoo status O).
- Lauri's Prime Rib: added Jaxson Hayes, dropped Keon Ellis.
- Looking Cool Joker!: added Brandon Williams, dropped Jeremiah Fears.
- ROOKS FTW: added Isaiah Jackson (FAAB 10), dropped Bilal Coulibaly.
- Booker T Floppers: Paolo Banchero to IL.

## Status changes since the 2026-10-24 afternoon file (commit 9c07606)
- Yours: Kyrie Irving D → O, moved to IL.
- Opponent: Joel Embiid newly D (Util slot). Kon Knueppel and Bradley Beal unchanged (O, IL).
- League-wide, 11 rows differ: Draymond Green D → O (now in a C slot), Zach Edey newly O, Keegan Murray newly Q, Reed Sheppard cleared, Paolo Banchero to IL, and slot moves for Podziemski, Coward, VanVleet, LeBron James.

## Brief: lineup, waiver scan, odds
- Lineup today (daily-fill rule): PG Ty Jerome, SG Tyrese Haliburton, G Kawhi Leonard, SF Jaden McDaniels, PF Noah Clowney. No game today for the other eight.
- Waiver scan: 40 of 520 pairs raise expected weekly category wins (base 5.109). Top pair: add Bobby Portis (MIA), drop Noah Clowney: +0.197 cats/week; title 25.6% (+5.1). Then Julian Champagnie (+3.2) and Tobias Harris (+4.5), both for Clowney. Record only, no proposal.
- Title odds (real schedule): 20.5% ± 0.6 (avg of 2 runs × 10,000 seasons), down from 27.0% ± 0.6 yesterday; playoffs 99.1%. Structural band unchanged from the standing sweep (deck 048efb6): TEAM_WEEK_SHOCK FRAGILE +2.3 / −3.4; weekly_availability FRAGILE −2.0 / +0.8 / −1.5 / +0.9. What changed in the inputs between the two runs: Kyrie Irving O and on IL, Noah Clowney (board value −4.94 per game) added, and 261 lines moved on the 10-24 box scores; the brief does not decompose the drop and this runner does not compute one.
- Movers: 261 lines moved by 0.25+ on 7 box-score records (season_lines_2026-10-25.json). Unpooled players with games: 96.

## Manager log, 2026-10-24
All 12 teams started their best available lineup (0 starts lost). A light slate: starts ranged from 5 (Lauri's Prime Rib, Podz save the league, MAXEY-MUM OVERDRIVE, John's Cool Team) to 8. Fred VanVleet, LeBron James and Yves Missi were in active slots with their team playing but no box line (all three carried O/Q tags). Profile now spans 3 days; 43 moves on Flaim's 30-day record.

## Deck publish
https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe republished as version 37 (id 1792930241-97e8). Read before: the 2026-10-24 deck. Read after: 438,222 bytes live, built file 437,676 bytes, built content found inside the live page, seven-tab list present once, data stamp 2026-10-25T12:09:36Z.

## Notes for the owner
1. The deck record pins report/calibration_daily.json as its 12th input and that file does not exist in the repo (present: false in deck_record_2026-10-25.json). It is written by main's scoring loop (score_week.py / calibration_daily), which has not run against a finished week yet. The record's input list will resolve after Monday's intake. Not fixed by me.
2. report/league and report/form are committed again (pinned by the record), as on 10-24; the prompt's commit list still omits them.
3. Title odds fell 6.5 points day over day. That is a model output (simulator with FRAGILE constants); the brief's own error bar is ±0.6 and the structural band is ±2–3.4, so the move is outside the sampling noise but inside what the standing sweep calls fragile. Decision for you whether to ask for a decomposition (a run, not done here).
4. Flaim's transactions carry 6 malformed rows Flaim excluded; the 43-row record is what Flaim returned.
