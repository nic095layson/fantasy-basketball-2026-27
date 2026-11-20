# Afternoon check 2026-11-20

- **T0:** 2026-11-20T23:04:11Z.
  - The morning records were hashed before the run; all 4 were still OK after it (`sha256sum -c`).
  - Baseline check passed: the league state at HEAD matches `league_state_am_2026-11-20.json`.
- **Repo:** season/daily was at 4c08827 and already up to date with origin/main. Tree clean; no stash.
- **Flaim:** 12 of 12 rosters returned, called one at a time, with no errors and no retries. FantasyBot was not needed.

## Lines

- LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-20_pm.json; 5 not in the deck pool (simulated once the season lines give an auto row, 3+ games): Nolan Traore (ANONG NANGIANNIS?!, G), Javon Small (Thompson Telepathy, BN), Tyrese Proctor (Podz save the league, SG), Matisse Thybulle (John's Cool Team, SG), Danny Wolf (John's Cool Team, C)
- STATUS GATE: PASS — status_2026-11-20_pm.json: 38 flagged row(s), each tiered with a dated receipt
- SEASON DECK: PASS — 2026-11-20 (afternoon refresh): report/season/deck_2026-11-20_pm.html (7 panes, 316 board rows, 38 status rows; record deck_record_2026-11-20_pm.json pins 21 inputs; render: 7 tabs, 0 page errors; lineup side refreshed (week_matchup_2026-11-20_pm.json))

## League moves since the morning state (league_moves_2026-11-20_pm.json)

- **Podz save the league** — added Ja'Kobe Walter; dropped Y. Konan Niederhäuser
- **ROOKS FTW** — to IL: CJ McCollum; off IL: Evan Mobley

## Injury status (status_2026-11-20_pm.json vs the morning's status_2026-11-20.json)

- **Yours:** PJ Washington is newly Q, in your active Util slot.
- **Thompson Telepathy:** Myles Turner no longer carries a designation (he was Q on their bench this morning).
- Across the league, 4 players' status tiers differ from the morning file.

## Deck

- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 95 (1795215917-f888).
- The 762,638 built bytes are contained in the 763,184-byte live page, which renders 7 tabs with 0 page errors.
- Before: Version 94 (this morning's rebuild).

## Nothing failed
