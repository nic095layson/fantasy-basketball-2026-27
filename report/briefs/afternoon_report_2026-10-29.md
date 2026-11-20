# Afternoon check 2026-10-29

First afternoon run on the `_pm` path (#225 on main; `league_live.py`, `status_feed.py` and `season_deck.py` all list `--phase`).

- **T0:** 2026-10-29T22:04:31Z. No stash (tree clean); season/daily merged with origin/main cleanly.
- **Flaim:** 12 of 12 roster calls returned data. No retries were needed: no YAHOO_AUTH_UNAVAILABLE, no retryable error. FantasyBot not needed.
- **LEAGUE LIVE:** PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-10-29.json; 1 not in the pool, not simulated: Matisse Thybulle (MAXEY-MUM OVERDRIVE, F)
  - LEAGUE INTAKE: PASS — 12 teams, 175 players, 175 of 175 resolved; 1 unpooled
  - LEAGUE MOVES: PASS — 4 team(s) changed, 10 move(s), 2026-10-29 to 2026-10-29 (pm); wrote data/news/league_moves_2026-10-29_pm.json
- **Morning records untouched** (sha256 checked before and after): data/news/league_moves_2026-10-29.json, data/status/status_2026-10-29.json, data/status/espn_injuries_2026-10-29.json.

## League moves since the morning state (league_moves_2026-10-29_pm.json)

- **ANONG NANGIANNIS?!** — added Sandro Mamukelashvili; dropped Mitchell Robinson
- **Thompson Telepathy** — to IL: Alex Caruso; off IL: Jimmy Butler
- **MAXEY-MUM OVERDRIVE** — added Mikel Brown Jr.; dropped Daniss Jenkins
- **John's Cool Team** — added De'Andre Hunter; dropped Jakob Poeltl, Jay Huff; off IL: Ivica Zubac

## Status since the morning (status_2026-10-29_pm.json vs status_2026-10-29.json)

- **Your roster:** no change.
- **Opponent (Looking Cool Joker!):** no change.
- Elsewhere: Egor Demin Q → O; Ivica Zubac D → O; new flags on Jaylen Brown (Q), Reed Sheppard (O), Robert Williams III (D) and Andrew Nembhard (P).
- **STATUS GATE:** PASS — status_2026-10-29_pm.json: 30 flagged row(s), each tiered with a dated receipt

## Deck

- **SEASON DECK:** PASS — 2026-10-29 (afternoon refresh): report/season/deck_2026-10-29_pm.html (7 panes, 315 board rows, 30 status rows; 7 tabs, 0 page errors). Lineup, waiver pairs and title odds are the 5 AM run's.
- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 43 (1793311558-7390). The 502,034 built bytes are contained in the 502,580-byte live page.

## Finding: the afternoon still rewrites the morning's pinned Flaim pull

- `league_live.py --phase pm` rewrote `data/source/flaim/pull_2026-10-29.json` (and `rosters_2026-10-29.transcribed.csv`).
  - It went from sha256 a409ab3e… to 841c2ca4…; `rosters` changed and a `carried_forward` key was added.
- The morning's `status_2026-10-29.json` and `deck_record_2026-10-29.json` pin a409ab3e…. After this commit the branch tip no longer holds that file; the morning version stays in history at 62cfdc6.
- This is the same overwrite class #225 fixed for the status and injury files.
- Recorded only; nothing changed.
