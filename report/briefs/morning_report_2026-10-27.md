# Morning report — 2026-10-27

First morning run on the updated prompt (get_standings, WROTE block, commit check).

- **MORNING:** PASS — 2026-10-27: 14 steps; brief report/briefs/brief_2026-10-27.md; record report/briefs/morning_2026-10-27.json
- **T0:** 2026-10-27T12:20:26Z. Step-4 path: `--since` (morning.py lists it). Tuesday, so no last-week matchups and no scoreboard intake.
- **Repos:** kit already attached (origin nic095layson/fantasy-basketball-2026-27); deck repo pulled fast-forward. season/daily merged with origin/main cleanly ("Already up to date"). No stash (tree clean).
- **Flaim:** tools present; 12 of 12 current rosters, current matchups (week 2), 100 available players, standings: all returned data, no retries. Manager log: 12 of 12 dated lineups (2026-10-26) and transactions (65 rows; Flaim notes 6 unrecognized Yahoo entries omitted) returned.
- **FantasyBot:** tools present; outlook once (rosters not needed).
- **LEAGUE LIVE:** PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-10-27.json
- **WEEK MATCHUP:** PASS — 2026-10-27: week 2 vs Looking Cool Joker!; to date from Yahoo (rebuild agrees); to date 1 day(s), 0 missing; projected 7-2-0; pickups: no finished low-value player
- **LEAGUE TABLE:** PASS — 2026-10-27: week 2; wk1 finished (rebuild), wk2 in_progress (yahoo); power #1 Cade n em (0.636), you #2 (0.636); Yahoo W-L-T matches the kit's finished weeks for 12 teams

## League moves 2026-10-26 → 2026-10-27 (data/news/league_moves_2026-10-27.json)

- **Lauri's Prime Rib** — added Jrue Holiday; dropped Mark Williams; to IL: Jaxson Hayes
- **Looking Cool Joker!** — added Pelle Larsson; to IL: Chet Holmgren
- **MAXEY-MUM OVERDRIVE** — added Daniss Jenkins; dropped Devin Vassell
- **Splash Mountain** — added Ziaire Williams; to IL: Andrew Nembhard

Yours: no change. (Diff is against the afternoon state of 10-26, so it is the overnight record.)

## Matchup, calibration, manager log

- **Games left (matchup_live):** week 2, 29 mine / 32 Looking Cool Joker!
- **AVAILABILITY CALIBRATION:** INSUFFICIENT — median team games 3.5 < 15 (population 155: healthy 137, mild 2, risk 16; regular-season team-games on file 104); first verdict expected near 2026-11-17. No value changed.
- **MANAGER LOG:** PASS — 2026-10-26: 12 lineups, 0 start(s) lost league-wide; outside IL, team played but no box line (inactive or unmatched name): Jalen Williams, Naji Marshall; profile 2026-10-22..2026-10-26 (5 day(s)); 11 new move(s), 65 on record

## Deck

Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 40 (id 1793103914-ff31). Re-read: the 509,237 built bytes are contained in the live page (509,783 with the host wrapper); the seven-tab list appears once; generated_utc 2026-10-27T12:24:25Z. SEASON DECK: PASS (7 panes, 314 board rows, 26 status rows, 7 tabs, 0 page errors).

- **WROTE:** 24 path(s) from morning.py.

## Brief

- **Lineup today (daily-fill):** PG Derrick White, SF Julian Champagnie, C Neemias Queta. No game today: Jerome, Gillespie, Durant, Lendeborg, Ware, Washington, Bridges, Haliburton, McDaniels, Irving.
- **Top waiver pair:** add Bobby Portis (MIA), drop Collin Gillespie: +0.015 cats/week; title 30.1% (+0.1). Next: Cameron Johnson for Champagnie (+0.009, 30.7%, +0.7); Tobias Harris for Champagnie (+0.002, 29.6%, −0.3). 5 of 520 pairs positive (base 5.408).
- **Title:** 30.0% ± 0.6 (avg of 2 runs × 10,000 seasons); playoffs 99.6%. Structural band: TEAM_WEEK_SHOCK FRAGILE +2.7 / −4.2; weekly_availability FRAGILE −5.4 / +3.7 / +0.4 / −0.5. Every pair delta sits inside both bands.

## Season lines movers (data/season/season_lines_2026-10-27.json)

282 lines moved by 0.25+ league-wide. On your roster: Ty Jerome pts 17.5→20.6, fga 12.7→13.6; Yaxel Lendeborg pts 11.7→14.3, reb 5.9→6.7, ast 2.4→3.0, 3PM 1.0→1.4; Haliburton pts 17.9→18.9; Washington pts 13.7→14.2; McDaniels reb 4.8→5.2; Durant pts 25.0→24.6; Irving pts 22.7→21.9; White pts 16.8→15.7; Gillespie pts 11.2→10.3, FT% .867→.808; Queta reb 7.9→7.3; Bridges pts 17.7→16.9; Champagnie pts 10.2→9.9, blk 0.5→0.8; Ware pts 12.1→12.4; Kawhi pts 24.6→23.9. One tag override: De'Andre Hunter inj-eye-risk → tag-cleared.

## Unpooled

No rostered unpooled player (league_state unpooled lists empty). League-wide, 109 unpooled players had games (none rostered).

## Failures

None.
