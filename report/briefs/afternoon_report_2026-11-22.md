# Afternoon check 2026-11-22

- **T0:** 2026-11-22T23:04:21Z.
  - The morning records were hashed before the run; all 4 were still OK after it (`sha256sum -c`).
  - Baseline check passed: the league state at HEAD matches `league_state_am_2026-11-22.json`.
- **Repo:** season/daily was at 314312d and already up to date with origin/main. Tree clean; no stash.
- **Flaim:** 12 of 12 rosters returned, called one at a time, with no errors and no retries. FantasyBot was not needed.

## Lines

- LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-22_pm.json; 4 not in the deck pool (simulated once the season lines give an auto row, 3+ games): Nolan Traore (ANONG NANGIANNIS?!, IL), Charles Bassey (Podz save the league, C), Caleb Martin (Podz save the league, UTIL), Matisse Thybulle (John's Cool Team, SG)
- STATUS GATE: PASS — status_2026-11-22_pm.json: 39 flagged row(s), each tiered with a dated receipt
- SEASON DECK: PASS — 2026-11-22 (afternoon refresh): report/season/deck_2026-11-22_pm.html (7 panes, 316 board rows, 39 status rows; record deck_record_2026-11-22_pm.json pins 21 inputs; render: 7 tabs, 0 page errors; lineup side refreshed (week_matchup_2026-11-22_pm.json))

## League moves since the morning state (league_moves_2026-11-22_pm.json)

- **Podz save the league** — added Caleb Martin, Charles Bassey; to IL: Aday Mara, Brandon Miller
- **John's Cool Team** — added Sam Hauser; dropped Danny Wolf, Max Strus; off IL: Brandon Ingram

## Injury status (status_2026-11-22_pm.json vs the morning's status_2026-11-22.json)

- **Yours:** Derrick White: O this morning → no designation now, in your active G slot. PJ Washington stays O in your active Util slot.
- **Thompson Telepathy:** no injury-status change.
- Across the league, 17 players' status tiers differ from the morning file.

## Deck

- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 99 (1795388725-8e95). Before: Version 98 (this morning).
- The 739,409 built bytes are contained in the 739,955-byte live page, which renders 7 tabs with 0 page errors.
- The page's waiver pairs and title odds are the morning run's.

## Nothing failed
