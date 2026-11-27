# Morning run 2026-11-09

**MORNING: PASS — 2026-11-09: 22 steps; brief report/briefs/brief_2026-11-09.md; record report/briefs/morning_2026-11-09.json**

One non-fatal step failed: **league table** (`LEAGUE TABLE: FAIL — Yahoo team 'Lauri’s Prime Rib' is not in the league state`). Seat 3 renamed itself on Yahoo to SNOWTIME WHITE WALKERS; see "Decision for David" below.

- **T0:** 2026-11-09T13:04:58Z. Path: `morning.py --since <T0>` (`--help` lists `--since`). Monday: last week's matchups pulled, season sweep and scoreboard intake ran.
- **Repos:** the kit was already attached (push rights to season/daily); the deck repo was up to date. Tree clean, no stash. season/daily was already up to date with origin/main.
- **Flaim:** tools present. 12 of 12 rosters (one at a time), matchups week 4 and week 3 finals, available players (100), standings, 12 of 12 dated lineups for 2026-11-08, transactions (100 rows). No errors, no retries.
- **FantasyBot:** tools present; outlook only (1 call; Flaim was complete).
- **LEAGUE LIVE:** PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-09.json; 5 not in the pool, not simulated: Meleek Thomas (Looking Cool Joker!, G), Nolan Traore (ANONG NANGIANNIS?!, BN), Morez Johnson Jr. (Podz save the league, UTIL), Mario Hezonja (MAXEY-MUM OVERDRIVE, SF), Danny Wolf (John's Cool Team, C)
- **WEEK MATCHUP:** PASS — 2026-11-09: week 4 vs SNOWTIME WHITE WALKERS; to date from Yahoo (rebuild agrees); to date 0 day(s), 0 missing; projected 5-4-0; pickups: no finished low-value player; pool pool_season.csv; wrote report/briefs/week_matchup_2026-11-09.json
- **Live matchup:** week 4, games left 41 mine / 42 SNOWTIME WHITE WALKERS.

## League moves (league_moves_2026-11-09.json, 2026-11-08 → 2026-11-09)

- **John's Cool Team** — added Danny Wolf; dropped Kenrich Williams
- **Podz save the league** — added Klay Thompson; dropped John Collins; to IL: Brandon Miller; off IL: Nic Claxton
- **SNOWTIME WHITE WALKERS** (seat 3, formerly Lauri’s Prime Rib) — added Jake LaRavia, Jaxson Hayes; dropped Luguentz Dort, Maxime Raynaud; to IL: Lauri Markkanen, Luka Doncic; off IL: Josh Hart
- **Scottie’s Thotties** — to IL: Norman Powell; off IL: Jarrett Allen

## Step lines

- **TAG OUTCOMES:** PASS — 2026-11-08: 29 flagged player(s) 16 no game, 4 played, 8 sat, 1 unresolved; data/status/tag_outcomes.jsonl
- **MINUTES LINE:** PASS — 2026-11-09: 343 players, 297 with games; ratio >= 1.10 for 8, <= 0.90 for 34; 37 unscaled (no preseason mpg); candidate only, wrote pool_season_mt.csv, projections_season_mt.csv. *A candidate, not the projection.*
- **SEASON SWEEP (Monday):** SWEEP: 6,000 seasons x seeds [2026, 2027] on deck 01483de; MC SE 0.54; baseline within 3 SE of the 10k reference: {'2026': True, '2027': True}
- **LEAGUE TABLE:** FAIL (non-fatal) — LEAGUE TABLE: FAIL — Yahoo team 'Lauri’s Prime Rib' is not in the league state. No report/league/league_2026-11-09.json was written; the deck record shows that input `present: False`, and the deck's embedded `league_table` is null, so today's League tab has no standings/power table.
- **MANAGER LOG:** PASS — 2026-11-08: 12 lineups, 5 start(s) lost league-wide; outside IL, team played but no box line (inactive or unmatched name): Domantas Sabonis; profile 2026-10-22..2026-11-08 (17 day(s)); 4 new move(s), 133 on record. 12 of 12 dated lineups; transactions came back.
- **SCOREBOARD INTAKE (week 3):** SCOREBOARD INTAKE: PASS — week 3: 6 matchups, 12 team lines; you 7-2-0 vs Podz save the league (won FG%, FT%, 3PTM, PTS, REB, ST, BLK); team_weeks.csv updated; ledger exit 0: scored week 3: {'won': ['3PTM', 'BLK', 'FG%', 'FT%', 'PTS', 'REB', 'ST'], 'cats_won': 7, 'brier_cats': 0.15080588944444445, 'brier_matchup': 0.023378410000000013}; week score scored, 7 mornings / 63 forecasts, Brier 0.124 vs lead-to-date 0.155; accuracy week 3: 255 players, points 13.06 projected / 11.63 actual; 6 league matchup(s) scored (Brier 0.222); fit through week 3, weeks [1, 2, 3], 36 team-weeks; shock 0.1117 ± 0.0153 (live 0.06); availability 0.00: 0.04 ± 0.02 (n 77), 0.75: 0.56 ± 0.03 (n 326), 0.79: 0.89 ± 0.07 (n 19), 0.88: 0.79 ± 0.01 (n 2736); board comparison mild 1.13 ± 0.09 vs deck 0.85 / sim 0.8977 / kit 0.8249, risk 0.71 ± 0.04 vs deck 0.78 / sim 0.8523 / kit 0.9036; too few weeks to propose (3 of 4); proposes only
  - The intake recorded seat 3 for week 3 as "SNOWTIME WHITE WALKERS"; weeks 1-2 in data/weeks/ still carry "Lauri’s Prime Rib". Nothing was edited.
- **STATUS GATE:** PASS — status_2026-11-09.json: 34 flagged row(s), each tiered with a dated receipt

## Brief

- **Lineup today:** PG Kyrie Irving, SG Ty Jerome, G Kevin Durant, SF Cameron Johnson (Q, check before lock), PF Yaxel Lendeborg, F PJ Washington, Util Miles Bridges, Util Collin Gillespie. No game today: Queta, Ware, White, Dunn, McDaniels.
- **Top waiver pair:** add John Collins (DET), drop Kris Dunn: +0.054 cats/week; title 20.2% (+2.1) — on waivers until 2026-11-11 (Podz dropped him this morning).
- **Waiver scan status:** "Status from Yahoo and ESPN. Set aside as Out: Jalen Williams (Out, espn, ESPN expects back 2027-03-02), Cason Wallace (O, yahoo, ESPN expects back 2027-03-02), Kevin Porter Jr. (NA, yahoo), Justin Champagnie (O, yahoo, ESPN expects back 2027-02-25), Bradley Beal (Out, espn, ESPN expects back 2026-11-29)."
- **Title:** 18.1% ± 0.5 (2 runs × 10,000 seasons). Playoffs: 99.3%. Structural band (today's re-measured season sweep): weekly_availability is FRAGILE, −4.8 / +2.9. IL-return scenario: ≈26% (26.0 to 26.9), not a forecast; ROOM_RULE_ON is FRAGILE (+11.1).
- **Season lines:** 301 lines moved by 0.25+ (report/season/board_2026-11-09.md). 146 unpooled players have games. 5 auto rows (Meleek Thomas 7g, Nolan Traore 10g, Morez Johnson Jr. 10g, Mario Hezonja 10g, Danny Wolf 5g).
- **Unpooled rostered players:** the 5 named in LEAGUE LIVE; Danny Wolf is new, Kenrich Williams left (dropped). The 11-06 flag stands: these are still called "not simulated" though each has an auto row (simulator input not traced).

## Deck

- **SEASON DECK:** PASS — 2026-11-09: report/season/deck_2026-11-09.html (7 panes, 315 board rows, 34 status rows; record deck_record_2026-11-09.json pins 16 inputs; render: 7 tabs, 0 page errors)
- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 67 (1794229963-8aa6). The 571,735 built bytes are contained in the 572,281-byte live page. 7 tabs present. The League tab's table is missing today (see LEAGUE TABLE).
- **WROTE:** 41 path(s) (morning.py). manager_log and scoreboard_intake add data/managers/ and data/weeks/.

## Decision for David (unattended run: options, not a card)

**League table broken by seat 3's rename** (Lauri’s Prime Rib → SNOWTIME WHITE WALKERS). EVIDENCE: `scripts/league_table.py:139` (`week_from_yahoo`) looks up each Yahoo matchup block's `teamName` in today's league state and raises on a miss; earlier pinned pulls still carry the old name. The week-file path at `:291` already keys on seat per your 2026-10-29 pick ("Key on Yahoo team key"); `week_from_yahoo` does not. league_live and week matchup handled the rename.

1. **Have main extend the 2026-10-29 "Key on Yahoo team key" rule to `week_from_yahoo` (match on the Yahoo team key/seat, not the name), with a test using this rename (Recommended).** Fixes future renames too; no data rewrite.
2. Approve a one-time name alias (old → new) for weeks 1-2. Faster, but it is a data change and the next rename breaks it again.
3. Leave it. The League tab stays without its standings/power table until a fix lands.

## Failed

- league table (non-fatal), above. Nothing else failed. No stash.
