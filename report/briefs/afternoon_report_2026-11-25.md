# Afternoon check 2026-11-25 (pm)

Runner: session model A. Clean-start container (after kit PR #307).

| Item | Result |
|---|---|
| T0 | 2026-11-25T21:39:51Z |
| Flaim roster calls | 12 of 12 returned data (get_user_session: ANTI MARTIN MARTIN CLUB, 478.l.36464). No retries. FantasyBot not needed. |
| LEAGUE LIVE | **HALT** — `scripts/league_live.py` crashes at import: `ModuleNotFoundError: No module named 'verify_rosters'` (league_live.py:40 → league_intake.py:44). `scripts/verify_rosters.py` is not tracked in git and is not on this container. `--phase` support could not be checked (`--help` crashes too). data/league_state.json NOT refreshed; no league_moves_2026-11-25_pm.json written. |
| League moves since morning | **no record** (league_live HALT). Unrecorded observation, this afternoon's Flaim reads vs data/source/flaim/pull_2026-11-25.json: SNOWTIME WHITE WALKERS — Isaiah Joe gone, Mikel Brown Jr. added; ANONG NANGIANNIS?! — Zaccharie Risacher gone (14 players); Thompson Telepathy — Mike Conley gone, Kevin Porter Jr. added. No script verified these. |
| Injury status (David + opponent Booker T Floppers) | **no injury-status change** in status_2026-11-25_pm.json vs status_2026-11-25.json (36 rows each, 0 changed). Caveat: the pm file's Yahoo tags cite the MORNING pull (league_live did not refresh), so only its ESPN read is fresh. This afternoon's Flaim tags for both teams match the morning pull: David — Lendeborg Q, Haliburton O, Leonard O; Booker T Floppers — Grayson Allen O, Banchero O, Dejounte Murray O. |
| STATUS GATE | STATUS GATE: PASS — status_2026-11-25_pm.json: 36 flagged row(s), each tiered with a dated receipt (ESPN injuries read 21:40:56Z) |
| SEASON DECK | **FAIL (crash, no SEASON DECK line)** — `season_deck.py --date 2026-11-25 --phase pm` → `ModuleNotFoundError: No module named 'hoops'` (season_deck.py:106 → week_matchup.py:70 → co_gm.py:20). `scripts/hoops.py` is not tracked in git. Not published; the morning deck page stands. |

Both crashes come from modules (verify_rosters, hoops) that are not in the repo, so the afternoon pipeline cannot run in a clean clone. Nothing in the engine was changed. Decision for the owner: commit the two missing modules from wherever the earlier runs had them.
