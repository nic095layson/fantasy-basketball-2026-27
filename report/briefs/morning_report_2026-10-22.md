# Morning report 2026-10-22 (on-demand run in the owner's session, T0 2026-10-22T14:44:17Z)

- MORNING: PASS — 2026-10-22: 11 steps; brief report/briefs/brief_2026-10-22.md; record report/briefs/morning_2026-10-22.json
- Why this run: the owner's third "Please run this morning" (~14:44Z). Built on the scheduled runner's run of 14:31:49Z (21d815d, owner "Run now" in the persistent runner session); that run's report is in history at 21d815d. This run is later and picks up a roster move the runner's did not see (below).
- Step 4 path: `--since 2026-10-22T14:44:17Z` (only pulls made after T0 are read from this session's transcript).
- Flaim (Yahoo), all successful: get_roster for all 12 teams (every snapshot "current"), get_matchups (week 1), get_free_agents (100). FantasyBot: get_matchup_outlook only (its projection is not used or quoted).
- LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-10-22.json (sha256 47d1e6583bcd…).
- League moves: MAXEY-MUM OVERDRIVE dropped Gui Santos (now in the free-agent list) and moved Kon Knueppel off IL (to the bench). Yahoo's games-remaining for them went from 26 to 22.
- WEEK MATCHUP: PASS — week 1 vs MAXEY-MUM OVERDRIVE; to date from Yahoo (the 14:44Z pin); projected 3-6-0 (the kit's week card).
  - Your side: Yahoo and the box-score rebuild agree on all 11 stats.
  - Opponent: the rebuild differs on 10 stats, lower on every one (FGA 129 vs Yahoo's 163, PTS 172 vs 196). The gap is exactly two player-games: Darius Acuff Jr.'s 10/21 game (his box score is left unmatched: the box pull spells the kit's pool name "Darius Acuff", without "Jr.") and Gui Santos's 10/21 game (5-10 FG, 12 PTS; the rebuild uses today's roster, and Santos was dropped this morning after playing). The displayed to-date column is Yahoo's own totals, so the card's figures are right; the rebuild is the cross-check.
  - Yahoo's category state: 4–4–1. Games left: Yahoo 19 yours / 22 theirs.
- MATCHUP LIVE: PASS — week 1, games left 21 mine / 26 MAXEY-MUM OVERDRIVE (FantasyBot's count; Yahoo's is 19 / 22).
- AVAILABILITY CALIBRATION: INSUFFICIENT — median team games 1 < 15 (population 156: healthy 138, mild 2, risk 16; regular-season team-games on file 28); first verdict expected near 2026-11-17. No value changed.
- Box pull 2026-10-21: ESPN 11 events, 11 final; two outlets, 298 matched, 3 cells differ.
- Deck: SEASON DECK: PASS (6 tabs, 0 page errors). Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe (version 1792680635-8c8b, generated 2026-10-22T14:50:17Z), on top of the runner's version 1792679671-9758; built bytes found inside the live page (offset 531); the served copy rendered twice in headless Chromium, 6 tabs, 0 page errors, every pane drawn.
- Brief: lineup today SG Christian Braun only. Top waiver pair: add Julian Champagnie, drop Christian Braun, +0.001 cats/week; title 22.7% (+0.1) — the only positive pair of 520. Title 22.6% ± 0.6 (22.94 / 22.29 by seed; the 14:20Z and 14:31Z runs had 23.8%, before MAXEY-MUM's moves); TEAM_WEEK_SHOCK and weekly_availability FRAGILE (bands in the brief).
- Brief label (recorded, not changed): line 1 reads "Rosters as of 2026-10-22 (owner's Yahoo page)"; the rosters came from Flaim. scripts/daily_brief.py:200 names every source other than FantasyBot "owner's Yahoo page".
- Movers: 194. Unpooled with games: 73 (data/season/season_lines_2026-10-22.json).
- Scoreboard intake: no weekly CSV in data/weeks.
