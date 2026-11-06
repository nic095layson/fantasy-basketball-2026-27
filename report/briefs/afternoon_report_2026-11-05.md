# Afternoon check 2026-11-05

- **T0:** 2026-11-05T23:04:14Z. No stash (tree clean). season/daily merged origin/main 6b30551 cleanly. That brought in #239 (an after-report) and #240 (start/sit ledger, start/sit heat map, auto pool rows).
- **Flaim:** 12 of 12 roster calls returned data, no retries. FantasyBot not needed.
- **LEAGUE LIVE:** PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-05_pm.json; 4 not in the pool, not simulated: Meleek Thomas (Looking Cool Joker!, G), Nolan Traore (ANONG NANGIANNIS?!, PG), Matisse Thybulle (MAXEY-MUM OVERDRIVE, BN), Quenton Jackson (John's Cool Team, UTIL)
  - LEAGUE MOVES: PASS — 3 team(s) changed, 6 move(s), 2026-11-05 to 2026-11-05 (pm); wrote data/news/league_moves_2026-11-05_pm.json
- **Morning records untouched** (sha256 checked before and after): league_moves_2026-11-05.json, status_2026-11-05.json, espn_injuries_2026-11-05.json, data/source/flaim/pull_2026-11-05.json.

## League moves since the morning state (league_moves_2026-11-05_pm.json)

- **KEL'EL YAXEL HALQUETA (yours)** — added Ziaire Williams; dropped Karlo Matkovic
- **ANONG NANGIANNIS?!** — added Oso Ighodaro; dropped Zaccharie Risacher
- **MAXEY-MUM OVERDRIVE** — added Jalen Green; to IL: Kon Knueppel

## Injury status since the morning (status_2026-11-05_pm.json vs status_2026-11-05.json)

- **Your players:** no injury-status change (Kawhi Leonard and Tyrese Haliburton still Out). Roster moves are in the league-moves section above.
- **Opponent's players (Podz save the league):** no injury-status change (Nic Claxton still Out).
- **Elsewhere:**
  - Out → questionable: DeMar DeRozan, Jalen Johnson, Josh Hart, Peyton Watson.
  - Out → probable: Trey Murphy III.
  - Newly questionable: Anthony Davis, Moussa Diabate.
  - Flag cleared: Jayson Tatum (was out).
- **STATUS GATE:** PASS — status_2026-11-05_pm.json: 27 flagged row(s), each tiered with a dated receipt

## Deck

- **SEASON DECK:** PASS — 2026-11-05 (afternoon refresh): report/season/deck_2026-11-05_pm.html (7 panes, 315 board rows, 27 status rows; record deck_record_2026-11-05_pm.json pins 16 inputs; render: 7 tabs, 0 page errors). Lineup, waiver pairs and title odds are the 5 AM run's. That run's waiver pairs dropped Karlo Matkovic, who is no longer on your roster.
- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 60 (1793920011-293f). The 565,063 built bytes are contained in the 565,609-byte live page.

## Nothing failed

- Flag, not fixed: the `out` field in deck_record_2026-11-05_pm.json names report/season/deck_2026-11-05.html (the morning file), not the _pm file. deck_record_2026-11-04_pm.json has the same mislabel. The morning deck file is unchanged in git, so only the record's label is wrong.
