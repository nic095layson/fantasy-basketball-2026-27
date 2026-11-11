# Morning run 2026-11-11

**MORNING: FAIL — 2026-11-11: step 'box scores 2026-11-10' failed (exit 1); later steps skipped; record report/briefs/morning_2026-11-11.json**

No brief, no season lines, no deck today. The deck was not published, so the live page stands as it was. The artifact list at 13:1xZ shows it last updated 2026-11-10; my last publish was Version 72, yesterday afternoon. Nothing in the engine was changed.

- **T0:** 2026-11-11T13:03:53Z. Path: `morning.py --since <T0>` (`--help` lists `--since`). Wednesday: no Monday or Sunday steps.
- **Repos:** the kit was already attached (push rights to season/daily); the deck repo was up to date. Tree clean, no stash. season/daily merged origin/main 9b0a37f (#255 playoff games column and FAAB winning bids; #256 audit items F3, F5, F6, which add title_watch).
- **Flaim:** tools present.
  - 12 of 12 rosters (one at a time), matchups week 4, available players (100), standings, 12 of 12 dated lineups for 2026-11-10. No errors, no retries.
  - Transactions: 99 rows. Flaim warned that 1 Yahoo entry could not be interpreted (`omitted_unrecognized_rows: 1`).
- **FantasyBot:** tools present; outlook only (1 call; Flaim was complete).
- **LEAGUE LIVE:** PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-11.json; 5 not in the deck pool (simulated once the season lines give an auto row, 3+ games): Jamal Cain (SNOWTIME WHITE WALKERS, BN), Nolan Traore (ANONG NANGIANNIS?!, UTIL), Morez Johnson Jr. (Podz save the league, IL), Mario Hezonja (MAXEY-MUM OVERDRIVE, F), Danny Wolf (John's Cool Team, BN)
- **MATCHUP LIVE:** PASS — week 4, games left 29 mine / 30 SNOWTIME WHITE WALKERS; wrote data/news/matchup_live_2026-11-11.json
- **WEEK MATCHUP, TAG OUTCOMES, MINUTES LINE:** skipped (after the failed step). No line to quote.

## What failed

- **Box scores 2026-11-10:** `FAIL · box scores 2026-11-10 · Basketball-Reference /boxscores/202611100NYK.html HTTP 404: HTTP Error 404: Not Found | Basketball-Reference /boxscores/202611100PHI.html HTTP 404: HTTP Error 404: Not Found`
  - Diagnosis (read-only, 13:07Z):
    - ESPN's scoreboard for 20261110 lists 6 games, all STATUS_FINAL. That includes Bucks at Knicks (00:30Z) and Celtics at 76ers (01:00Z).
    - The same two Basketball-Reference pages still return 404.
    - box_pull.py fails when any fetch fails and then writes nothing, by design (its `--help`).
  - Steps skipped: tag outcomes, lineup log, accuracy render, season lines, minutes line, season board, status feed, transactions, league pairings, il return, daily brief, decision log, title watch, week matchup, decision card, league table, form board, season deck.
- **MANAGER LOG:** HALT — no box scores at data/actuals/2026-11-10.json; day not logged, profile stands at 18 day(s); 6 new move(s), 146 on record. 12 of 12 dated lineups and the transactions came back. The 6 moves were recorded.
- **WROTE:** 8 path(s) (morning.py), plus data/managers/ (manager_log) and report/briefs/morning_2026-11-11.json.

## League moves (league_moves_2026-11-11.json)

- **KEL'EL YAXEL HALQUETA (yours)** — added John Collins ($35 FAAB); dropped Alex Caruso
- **SNOWTIME WHITE WALKERS** (week-4 opponent) — added Jamal Cain; to IL: Josh Hart
- **Booker T Floppers** — to IL: Tristan da Silva; off IL: Keegan Murray
- **Looking Cool Joker!** — added Nique Clifford; dropped Meleek Thomas
- **Scottie’s Thotties** — to IL: Precious Achiuwa; off IL: Zion Williamson
- **Thompson Telepathy** — added Robert Williams III; dropped Karlo Matkovic; to IL: Devin Vassell; off IL: Egor Demin
- **ROOKS FTW** — dropped Ryan Rollins; off IL: Desmond Bane
- **MAXEY-MUM OVERDRIVE** — added Isaiah Collier; to IL: Keyonte George

## Decision for David (unattended run: options, not a card)

**Today's morning outputs are missing because one outlet has no page for two of last night's six games.**

1. **Re-run the same morning command later today, once Basketball-Reference posts the two pages (Recommended).** No method change; the afternoon runner or a session you start can do it. Until then the deck shows yesterday's numbers.
2. **Approve a single-outlet day for 11-10.** That means `box_pull.py --date 2026-11-10 --no-bref` (ESPN only, labelled single_source), then morning.py. ESPN has all 6 finals. It is a method choice for one day, so it waits for your word.
3. **Leave 11-10 unrecorded.** Tomorrow's run pulls 11-11. The 11-10 box scores, its tag outcomes and that day of the manager log stay missing.
