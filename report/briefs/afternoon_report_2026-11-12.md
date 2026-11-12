# Afternoon check 2026-11-12

- **T0:** 2026-11-12T23:04:25Z. No stash (tree clean). season/daily merged origin/main 8dc596d (through #269); merge 124930c.
- **Flaim:** 12 of 12 roster calls returned data, one at a time, no retries. FantasyBot not needed.
- **LEAGUE LIVE:** PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-12_pm.json; 4 not in the deck pool (simulated once the season lines give an auto row, 3+ games): Nolan Traore (ANONG NANGIANNIS?!, IL), Morez Johnson Jr. (Podz save the league, F), Meleek Thomas (MAXEY-MUM OVERDRIVE, BN), Danny Wolf (John's Cool Team, BN)
  - LEAGUE MOVES: PASS — 0 team(s) changed, 0 move(s), 2026-11-12 to 2026-11-12 (pm); wrote data/news/league_moves_2026-11-12_pm.json
  - LEAGUE INTAKE: 0 NBA-team disagreement(s) with the pool.
- **Morning records untouched** (sha256 checked before and after): league_moves_2026-11-12.json, status_2026-11-12.json, espn_injuries_2026-11-12.json, data/source/flaim/pull_2026-11-12.json.

## A second afternoon writer today

- Another session ran two afternoon refreshes on season/daily before this run: db51bfb and 0e21df1 ("Afternoon refresh 2 2026-11-12 … 1 team changed … deck v79"; its pull was taken at 21:03Z).
- So this run's baseline was that 21:03Z state, not the morning's. The "0 moves" above means **no moves since 21:03Z**.
- This run rewrote the `_pm` files that session had committed: league_moves_2026-11-12_pm.json, the pm pull, status and ESPN files, week_matchup_pm and deck_pm. Their versions remain in git history (0e21df1). Its pm moves record held one team: Podz save the league, to IL Klay Thompson, off IL Morez Johnson Jr.

## League moves since the morning state

These were computed read-only, with league_moves.write_record, from league_state_am_2026-11-12.json to this run's league_state.json. The output is in the scratchpad, not committed.
- **Podz save the league** — to IL: Klay Thompson; off IL: Morez Johnson Jr.
- **MAXEY-MUM OVERDRIVE** — added Ja'Kobe Walter; dropped Isaiah Collier
- Your roster and SNOWTIME's: no move.

## Injury status since the morning (status_2026-11-12_pm.json vs status_2026-11-12.json)

- **Your players:** no injury-status change (Kawhi Leonard and Tyrese Haliburton still Out).
- **Opponent's players (SNOWTIME WHITE WALKERS):** no injury-status change (Luka Doncic Q on IL, Lauri Markkanen Out).
- **Elsewhere:**
  - Newly Out: Evan Mobley.
  - Questionable → Out: Caleb Wilson, LeBron James, Stephen Curry.
  - Out → questionable: Ajay Mitchell, Devin Vassell, Norman Powell, Tristan da Silva.
  - Out → doubtful: Trey Murphy III.
  - Newly questionable: Klay Thompson, Pelle Larsson. Newly probable: Giannis Antetokounmpo.
  - Flag cleared: Myles Turner (was Out), Moussa Diabate (was probable), Ryan Rollins (was questionable).
- **STATUS GATE:** PASS — status_2026-11-12_pm.json: 34 flagged row(s), each tiered with a dated receipt

## Deck

- **SEASON DECK:** PASS — 2026-11-12 (afternoon refresh): report/season/deck_2026-11-12_pm.html (7 panes, 315 board rows, 34 status rows; record deck_record_2026-11-12_pm.json pins 21 inputs; render: 7 tabs, 0 page errors; lineup side refreshed (week_matchup_2026-11-12_pm.json))
- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 80 (1794524785-ee34). The 678,603 built bytes are contained in the 679,149-byte live page; all 7 tab names are present.
- The live page before this publish was 1794517471-ae78 (deck data generated 21:04Z), the other session's refresh. This page replaces it and is built on main through #269.

## Decision for David (unattended run: options, not a card)

**Two afternoon writers touched the same `_pm` records today. The last one to run wins the file.**
1. **Leave it (Recommended).** History keeps both versions, and this report lists the full moves since the morning. Nothing to build.
2. **Have main make a second afternoon run write `_pm2` (or append) instead of overwriting.** This keeps every afternoon record as a file, but it is a change for main to build.
3. **Pause the scheduled afternoon run on days a session has already refreshed.** This needs a check before step 3, which is also a build.

## Nothing failed
