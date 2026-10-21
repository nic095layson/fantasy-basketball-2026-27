# Morning report 2026-10-21 (catch-up run)

- MORNING: FAIL — 2026-10-21: step 'season deck' failed (exit 1); later steps skipped; record report/briefs/morning_2026-10-21.json
- T0: 2026-10-21T14:56:43Z. Step 4 path: no-fetch fallback (morning.py has no --since; step 3 skipped by the catch-up instruction). Rosters and matchup are the last saved state (brief line 1: "Rosters as of 2026-10-20 (FantasyBot live pull)").
- Repos: kit already attached (origin https://github.com/nic095layson/fantasy-basketball-2026-27); deck repo cloned fresh to /home/user/yahoo-fantasy-basketball.
- FantasyBot: no call made (step 3 skipped). Tools present only under UUID prefix mcp__fc659f00-abbe-421b-bbf7-230cf9e631c7__*, not mcp__FantasyBot__*. 0 of 14 calls.
- League moves: no record (live pull did not run).
- Matchup live games-left: no record for 2026-10-21 (matchup_live not run). Brief shows games left this week per player (3 for most of the lineup).
- AVAILABILITY CALIBRATION: INSUFFICIENT — median team games 1 < 15; 5 risk-tagged with games < 10 (population 155: healthy 136, mild 2, risk 17; regular-season team-games on file 6); first verdict expected near 2026-11-17. No value changed.
- Deck: NOT built, NOT published. season_deck.py treats data/news/matchup_live_<date>.json as optional when loading it but hashes every input path unconditionally (scripts/season_deck.py line 142), so with no matchup_live file it raises FileNotFoundError. Engine not touched, per rules. The artifact still holds the 12:54Z publish.
- Brief: lineup PG Ty Jerome, SG Kevin Durant, G Kawhi Leonard, SF Jaden McDaniels, PF Yaxel Lendeborg, F Miles Bridges, C PJ Washington, C Kel'el Ware, Util Haliburton, Util Irving. Top waiver pair: add Bobby Portis, drop Christian Braun, +0.029 cats/week; title 24.8% (+0.7). Title odds 24.1% ± 0.6 (sampling); structural band: TEAM_WEEK_SHOCK and weekly_availability are FRAGILE (see brief).
- Movers: 43 lines moved by 0.25+ (e.g. Wembanyama pts 25.6→24.5, Tatum pts 27.5→26.4).
- Unpooled with games (12): Bennett Stirtz, Brooks Barnhizer, Carter Bryant, David Jones Garcia, Hugo Gonzalez, Ja'Kobi Gillespie, Jabari Walker, Jordan Clarkson, Kenrich Williams, Landry Shamet, Maliq Brown, Tarris Reed Jr.
- Passing steps: box pull (2026-10-20: 3 games, 84 lines), transactions (9 items), season lines, season board, status feed, daily brief.
- Stash: none.
