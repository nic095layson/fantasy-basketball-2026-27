# Afternoon check 2026-11-24

- **T0:** 2026-11-24T23:03:43Z.
  - The morning records were hashed before the run; all 4 were still OK after it (`sha256sum -c`).
  - Baseline check passed: the league state at HEAD matches `league_state_am_2026-11-24.json`.
- **Repo:** season/daily was at 6f2058b; origin/main had one new merge (#306), merged in as 60c17f2 with no conflict. Tree clean; no stash.
- **Flaim:** 12 of 12 rosters returned, called one at a time, with no errors and no retries. FantasyBot was not needed.

## Lines

- LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-24_pm.json; 2 not in the deck pool (simulated once the season lines give an auto row, 3+ games): Charles Bassey (Podz save the league, C), Matisse Thybulle (John's Cool Team, SG)
- STATUS GATE: PASS — status_2026-11-24_pm.json: 35 flagged row(s), each tiered with a dated receipt
- SEASON DECK: PASS — 2026-11-24 (afternoon refresh): report/season/deck_2026-11-24_pm.html (7 panes, 317 board rows, 35 status rows; record deck_record_2026-11-24_pm.json pins 21 inputs; render: 7 tabs, 0 page errors; lineup side refreshed (week_matchup_2026-11-24_pm.json))

## League moves since the morning state (league_moves_2026-11-24_pm.json)

- **SNOWTIME WHITE WALKERS** — added Isaiah Joe; dropped Kelly Oubre Jr.
- **Thompson Telepathy** — added Mike Conley; dropped Kris Dunn
- **ROOKS FTW** — added Kevin Huerter; dropped Svi Mykhailiuk

## Injury status (status_2026-11-24_pm.json vs the morning's status_2026-11-24.json)

- **Yours:** no injury-status change. PJ Washington stays Q in your active Util slot.
- **Booker T Floppers (your opponent):** no injury-status change.
- Across the league, 5 players' status tiers differ from the morning file (Joel Embiid Q → D and Karl-Anthony Towns → Q, both MISSI ELLIOTT; OG Anunoby Q → O; Jalen Smith and Josh Hart → Q).

## Deck

- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 103 (1795561510-3a62). Before: Version 102 (this morning).
- The 780,321 built bytes are contained in the 780,867-byte live page, which renders 7 tabs with 0 page errors.
- The page's waiver pairs and title odds are the morning run's.

## Nothing failed
