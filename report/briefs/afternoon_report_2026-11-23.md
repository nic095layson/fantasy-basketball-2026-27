# Afternoon check 2026-11-23

- **T0:** 2026-11-23T23:04:14Z.
  - The morning records were hashed before the run; all 4 were still OK after it (`sha256sum -c`).
  - Baseline check passed: the league state at HEAD matches `league_state_am_2026-11-23.json`.
- **Repo:** season/daily was at 0e053c4; origin/main had two new merges (#304 playbook lesson, #305 confidence report), merged in as 5ee1f73 with no conflict. Tree clean; no stash.
- **Flaim:** 12 of 12 rosters returned, called one at a time, with no errors and no retries. FantasyBot was not needed.

## Lines

- LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-23_pm.json; 4 not in the deck pool: Nolan Traore (ANONG NANGIANNIS?!, G), Charles Bassey (Podz save the league, C), Svi Mykhailiuk (ROOKS FTW, UTIL), Matisse Thybulle (John's Cool Team, SG)
- STATUS GATE: PASS — status_2026-11-23_pm.json: 36 flagged row(s), each tiered with a dated receipt
- SEASON DECK: PASS — 2026-11-23 (afternoon refresh): report/season/deck_2026-11-23_pm.html (7 panes, 316 board rows, 36 status rows; record deck_record_2026-11-23_pm.json pins 21 inputs; render: 7 tabs, 0 page errors; lineup side refreshed (week_matchup_2026-11-23_pm.json)); rostered with no board row: Buddy Hield

## League moves since the morning state (league_moves_2026-11-23_pm.json)

- **KEL'EL YAXEL HALQUETA (you)** — added Collin Gillespie; dropped Andrew Wiggins (David's own move; this morning's recommended pair was Cameron Johnson for Wiggins)
- **Podz save the league** — added Buddy Hield, Cameron Johnson; dropped Caleb Martin, Ja'Kobe Walter, Keaton Wagler; off IL: Brandon Miller
- **Thompson Telepathy** — added De'Andre Hunter; dropped Collin Sexton
- **Looking Cool Joker!** — added Anfernee Simons; dropped Aaron Nesmith
- **ROOKS FTW** — added Svi Mykhailiuk; dropped Jaxson Hayes

## Injury status (status_2026-11-23_pm.json vs the morning's status_2026-11-23.json)

- **Yours:** PJ Washington: O this morning → **Q** now, in your active Util slot.
- **Booker T Floppers (your opponent):** Shai Gilgeous-Alexander: O this morning → no designation now.
- Across the league, 13 players' status tiers differ from the morning file.

## Deck

- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 101 (1795475135-3ce1). Before: Version 100 (this morning).
- The 776,086 built bytes are contained in the 776,632-byte live page, which renders 7 tabs with 0 page errors.
- The page's waiver pairs and title odds are the morning run's; they were scored before the Gillespie move and before Johnson left the pool.

## Nothing failed
