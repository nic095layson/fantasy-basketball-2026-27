# Afternoon check 2026-11-11

- **T0:** 2026-11-11T23:04:21Z. No stash (tree clean). season/daily merged origin/main 383bb07 (through #262, which includes #260 "team-update path (D3)" and #261 Draft Check); merge b87952b.
- **Flaim:** 12 of 12 roster calls returned data, one at a time, no retries. FantasyBot not needed.
- **LEAGUE LIVE:** PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-11_pm.json; 4 not in the deck pool (simulated once the season lines give an auto row, 3+ games): Nolan Traore (ANONG NANGIANNIS?!, IL), Morez Johnson Jr. (Podz save the league, IL), Mario Hezonja (MAXEY-MUM OVERDRIVE, F), Danny Wolf (John's Cool Team, BN)
  - LEAGUE MOVES: PASS — 4 team(s) changed, 8 move(s), 2026-11-11 to 2026-11-11 (pm); wrote data/news/league_moves_2026-11-11_pm.json
  - LEAGUE INTAKE: "0 NBA-team disagreement(s) with the pool". Yesterday's Nique Clifford mismatch (Yahoo OKC, pool SAC) is gone. INFERENCE: #260, the D3 team-update path, resolved it; `pool_season.csv` itself still reads SAC, so the update lives elsewhere (not traced).
- **Morning records untouched** (sha256 checked before and after): league_moves_2026-11-11.json, status_2026-11-11.json, espn_injuries_2026-11-11.json, data/source/flaim/pull_2026-11-11.json. These are the session re-run's morning files (8473ce7).

## League moves since the morning state (league_moves_2026-11-11_pm.json)

- **SNOWTIME WHITE WALKERS** (your week-4 opponent) — dropped Jamal Cain; off IL: Josh Hart
- **ANONG NANGIANNIS?!** — to IL: Nolan Traore; off IL: Trey Murphy III
- **Thompson Telepathy** — to IL: LeBron James; off IL: Devin Vassell
- **ROOKS FTW** — added Andre Drummond; to IL: Paul George
- Your roster: no move.

## Injury status since the morning (status_2026-11-11_pm.json vs status_2026-11-11.json)

- **Your players:** no injury-status change (Kawhi Leonard and Tyrese Haliburton still Out).
- **Opponent's players (SNOWTIME WHITE WALKERS):** Josh Hart's Out flag cleared (now in the F slot). Lauri Markkanen still Out.
- **Elsewhere:**
  - Newly Out: Ajay Mitchell, Myles Turner, Paul George.
  - Newly questionable: Caleb Wilson, Joel Embiid, LeBron James.
  - Out → questionable: Keyonte George, Precious Achiuwa, Tristan da Silva, Tyler Herro.
  - Probable → doubtful: Trey Murphy III.
  - Flag cleared: Collin Murray-Boyles and Immanuel Quickley (were questionable), Egor Demin (was out).
- **STATUS GATE:** PASS — status_2026-11-11_pm.json: 30 flagged row(s), each tiered with a dated receipt

## Deck

- **SEASON DECK:** PASS — 2026-11-11 (afternoon refresh): report/season/deck_2026-11-11_pm.html (7 panes, 315 board rows, 30 status rows; record deck_record_2026-11-11_pm.json pins 21 inputs; render: 7 tabs, 0 page errors; lineup side refreshed (week_matchup_2026-11-11_pm.json))
- All 21 inputs are present, the decision card included. It was already present in the session re-run's morning deck (deck_record_2026-11-11.json).
- The tabs are Today, Trade Analyzer, Free Agents, Board, Draft Check, Week, League. Movers is gone (#261).
- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 76 (1794438332-45bb). The 669,897 built bytes are contained in the 670,443-byte live page. All 7 tab names are present in the live page.
- The live page before this publish was 1794430419-c921 (deck data generated 20:53Z). It was not this runner's; its publisher was not checked. The afternoon page replaces it.

## Nothing failed
