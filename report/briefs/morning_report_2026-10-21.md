# Morning report 2026-10-21 (scheduled run, T0 2026-10-21T18:33:05Z)

- MORNING: FAIL — 2026-10-21: step 'season deck' failed (exit 1); later steps skipped; record report/briefs/morning_2026-10-21.json
- Step 4 path: `--since 2026-10-21T18:33:05Z` (morning.py lists --since).
- Repos: kit already attached; deck repo already present (pull: up to date). Branch: origin/season/daily, merged origin/main (55f950c, fast-forward), no stash.
- Flaim: tools present; league ANTI MARTIN MARTIN CLUB = 478.l.36464 (matches). 12 of 12 roster calls returned data; matchups returned (week 1); available-player list returned (100). scripts/flaim_live.py is not in the kit, so nothing reads the Flaim pull yet.
- FantasyBot: tools present; 14 of 14 calls returned data (outlook + my roster + team list + 11 rivals).
- LEAGUE LIVE: HALT — unknown FantasyBot injury label 'Questionable' on Deni Avdija: add it to STATUS_OF, do not guess; league_state.json not touched (last paste stands)
- WEEK MATCHUP: no line — morning.py has no week-matchup step yet.
- League moves: no record (league live halted).
- MATCHUP LIVE: PASS — week 1, games left 30 mine / 34 MAXEY-MUM OVERDRIVE
- AVAILABILITY CALIBRATION: INSUFFICIENT — median team games 1 < 15; 5 risk-tagged with games < 10 (population 155: healthy 136, mild 2, risk 17; regular-season team-games on file 6); first verdict expected near 2026-11-17. No value changed.
- Deck: NOT published. SEASON DECK: FAIL — render UNAVAILABLE: playwright not importable: No module named 'playwright' (page kept as deck_2026-10-21.failed.html; deck_2026-10-21.html not written). The deck_2026-10-21.html on disk is the earlier run's file and was not republished. Python playwright is not installed in this container (Chromium is, at /opt/pw-browsers); nothing installed, per the rules.
- Brief (rosters are the last saved state, as of 2026-10-20): lineup PG Ty Jerome, SG Kevin Durant, G Kawhi Leonard, SF Jaden McDaniels, PF Yaxel Lendeborg, F Miles Bridges, C PJ Washington, C Kel'el Ware, Util Tyrese Haliburton, Util Kyrie Irving. Top waiver pair: add Bobby Portis, drop Christian Braun, +0.029 cats/week; title 24.8% (+0.7). Title 24.1% ± 0.6; TEAM_WEEK_SHOCK and weekly_availability FRAGILE (bands in the brief).
- Stale-state flag: the brief names the opponent KEVIN ELEVEN DOUBLES; today's Yahoo matchup and FantasyBot both name team 10 MAXEY-MUM OVERDRIVE.
- Movers: 43 lines moved by 0.25+. Unpooled with games (12): Bennett Stirtz, Brooks Barnhizer, Carter Bryant, David Jones Garcia, Hugo Gonzalez, Ja'Kobi Gillespie, Jabari Walker, Jordan Clarkson, Kenrich Williams, Landry Shamet, Maliq Brown, Tarris Reed Jr.
- Scoreboard intake: no weekly CSV in data/weeks (TEMPLATE.csv only).
