# Morning report 2026-10-22 (run at T0 2026-10-22T03:43:33Z)

- MORNING: PASS — 2026-10-22: 11 steps; brief report/briefs/brief_2026-10-22.md; record report/briefs/morning_2026-10-22.json
- Date flag: the routine's Pacific "today" was 2026-10-21 (20:43 PDT); morning.py defaults --date to the container's date (UTC, 2026-10-22), so every record and the deck carry 2026-10-22.
- Step 4 path: `--since 2026-10-22T03:43:33Z` (morning.py lists --since).
- Repos: kit already attached; deck repo already present (pull up to date). Branch: origin/season/daily merged with origin/main (af625a8); no stash.
- Flaim: tools present; league 478.l.36464 (matches). 4 of 12 roster calls returned data (teams 6, 7, 9, 11); 7 failed with "YAHOO_AUTH_UNAVAILABLE: refresh_temporarily_unavailable: Yahoo token refresh is already in progress", team 12 with a Cloudflare 502; get_league_info and get_free_agents failed with the same auth error; get_matchups returned. Flaim not complete; no retry (rule: stop calling Flaim).
- FantasyBot: tools present; 14 of 14 calls returned data (outlook + my roster + team list + 11 rivals).
- LEAGUE LIVE: PASS — rosters from FantasyBot, pinned data/source/fantasybot/pull_2026-10-22.json
- WEEK MATCHUP: PASS — 2026-10-22: week 1 vs MAXEY-MUM OVERDRIVE; to date from Yahoo (rebuild differs on 21 stat(s)); to date 2 day(s), 0 missing; projected 3-6-0; pickups: no finished low-value player
- League moves (2026-10-20 to 2026-10-22): Cade n em added Moussa Diabate, dropped Mitchell Robinson; John's Cool Team added Yves Missi; Podz save the league added Andre Drummond, Brandin Podziemski to IL; Splash Mountain added Ace Bailey, dropped Collin Sexton.
- MATCHUP LIVE: PASS — week 1, games left 21 mine / 27 MAXEY-MUM OVERDRIVE
- AVAILABILITY CALIBRATION: INSUFFICIENT — median team games 1 < 15 (population 156: healthy 138, mild 2, risk 16; regular-season team-games on file 22); first verdict expected near 2026-11-17. No value changed.
- Deck: SEASON DECK: PASS — report/season/deck_2026-10-22.html (6 panes, 313 board rows, 15 status rows; render: 6 tabs, 0 page errors). Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe (version 1792640745-5b2e); built bytes confirmed inside the live page; tabs Today, Trade Analyzer, Free Agents, Board, Movers, Week.
- Brief: lineup today SG Christian Braun only; no game today for the other twelve. Waiver scan: no add/drop pair raises expected weekly category wins (520 scored); stand pat. Title 23.8% ± 0.6 (2 runs x 10,000); structural band: TEAM_WEEK_SHOCK FRAGILE +2.3/-3.4, weekly_availability FRAGILE -2.0/+0.8/-1.5/+0.9.
- Box pull 2026-10-21: single-source (ESPN only), labelled in data/actuals/2026-10-21.json.
- Movers: 152 lines moved by 0.25+. Unpooled with games: 48 (listed in data/season/season_lines_2026-10-22.json).
- Scoreboard intake: no weekly CSV in data/weeks (TEMPLATE.csv only).
