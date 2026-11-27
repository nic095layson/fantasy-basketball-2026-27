# Afternoon check 2026-11-21

- **T0:** 2026-11-21T23:03:58Z.
  - The morning records were hashed before the run; all 4 were still OK after it (`sha256sum -c`).
  - Baseline check passed: the league state at HEAD matches `league_state_am_2026-11-21.json`.
- **Repo:** season/daily was at 5279000 and already up to date with origin/main. Tree clean; no stash.
- **Flaim:** 12 of 12 rosters returned, called one at a time, with no errors and no retries. FantasyBot was not needed.

## Lines

- LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-21_pm.json; 3 not in the deck pool (simulated once the season lines give an auto row, 3+ games): Nolan Traore (ANONG NANGIANNIS?!, IL), Matisse Thybulle (John's Cool Team, SG), Danny Wolf (John's Cool Team, BN)
- STATUS GATE: PASS — status_2026-11-21_pm.json: 38 flagged row(s), each tiered with a dated receipt
- SEASON DECK: PASS — 2026-11-21 (afternoon refresh): report/season/deck_2026-11-21_pm.html (7 panes, 316 board rows, 38 status rows; record deck_record_2026-11-21_pm.json pins 21 inputs; render: 7 tabs, 0 page errors; lineup side refreshed (week_matchup_2026-11-21_pm.json))

## League moves since the morning state (league_moves_2026-11-21_pm.json)

- **Thompson Telepathy (your opponent)** — added Kris Dunn; dropped Javon Small
- **Looking Cool Joker!** — added Naji Marshall; dropped Pelle Larsson
- **ANONG NANGIANNIS?!** — to IL: Nolan Traore; off IL: Trey Murphy III
- **Podz save the league** — off IL: Deni Avdija
- **John's Cool Team** — to IL: Jayson Tatum

## Injury status (status_2026-11-21_pm.json vs the morning's status_2026-11-21.json)

- **Yours:**
  - Derrick White: Q → **O**, still in your active G slot.
  - PJ Washington: Q → **D** (doubtful), still in your active Util slot.
  - Ty Jerome: O this morning → no designation now, in your active SG slot.
- **Thompson Telepathy:** no injury-status change.
- Across the league, 16 players' status tiers differ from the morning file.

## Deck

- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 97 (1795302306-353c). Before: Version 96 (this morning).
- The 743,363 built bytes are contained in the 743,909-byte live page, which renders 7 tabs with 0 page errors.
- The page's waiver pairs and title odds are the morning run's.

## Nothing failed
