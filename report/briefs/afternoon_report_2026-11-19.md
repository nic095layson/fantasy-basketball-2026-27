# Afternoon check 2026-11-19

- **T0:** 2026-11-19T23:04:17Z. The morning records were hashed before the run, and all 4 hashes were still OK after it (`sha256sum -c`). The baseline check passed: the league state committed at HEAD matches `league_state_am_2026-11-19.json`.
- **Repo:** season/daily was at 24c4b24 and already up to date with origin/main. Tree clean; no stash.
- **Flaim:** returned 12 of 12 rosters, with no errors and no retries. FantasyBot was not needed. **Process note:** the calls for teams 4 and 5 went out together in one batch, against the one-at-a-time rule. Both returned data. Every other call went out alone.

## Lines

- LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-19_pm.json; 7 not in the deck pool (simulated once the season lines give an auto row, 3+ games): Nolan Traore (ANONG NANGIANNIS?!, G), Brice Sensabaugh (ANONG NANGIANNIS?!, UTIL), Javon Small (Thompson Telepathy, PG), Tyrese Proctor (Podz save the league, BN), Meleek Thomas (MISSI ELLIOTT, SG), Matisse Thybulle (John's Cool Team, SG), Danny Wolf (John's Cool Team, BN)
- STATUS GATE: PASS — status_2026-11-19_pm.json: 38 flagged row(s), each tiered with a dated receipt
- SEASON DECK: PASS — 2026-11-19 (afternoon refresh): report/season/deck_2026-11-19_pm.html (7 panes, 315 board rows, 38 status rows; record deck_record_2026-11-19_pm.json pins 21 inputs; render: 7 tabs, 0 page errors; lineup side refreshed (week_matchup_2026-11-19_pm.json))

## League moves since the morning state (league_moves_2026-11-19_pm.json)

- **SNOWTIME WHITE WALKERS** — added Julian Champagnie (this morning's top waiver add for you); dropped Kevin Huerter
- **Thompson Telepathy (your opponent)** — added Javon Small, starting him at PG
- **ROOKS FTW** — added Kasparas Jakucionis; dropped Mo Bamba

## Injury status (status_2026-11-19_pm.json vs the morning's status_2026-11-19.json)

- **Thompson Telepathy:** Myles Turner is new on the list, as O. He sits in their active C slot.
- **Your players:** no injury-status change. Ty Jerome is still O in your active SG slot. Haliburton and Leonard are still O on IL.
- Across the league, 11 players' status tiers differ from the morning file.

## Deck

- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 93 (1795129538-b7a9). The 752,425 built bytes are contained in the 752,971-byte live page. The live copy renders 7 tabs with 0 page errors. Before: Version 92 (this morning).

## Nothing failed
