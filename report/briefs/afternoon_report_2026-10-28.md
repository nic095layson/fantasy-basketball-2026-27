# Afternoon check 2026-10-28

First afternoon run on prompt pm_v2 (retry rule for retryable errors).

- **T0:** 2026-10-28T22:04:47Z. No stash (tree clean); season/daily merged with origin/main cleanly.
- **Flaim:** 12 of 12 roster calls returned data. No retries were needed: no YAHOO_AUTH_UNAVAILABLE, no retryable error. FantasyBot not needed.
- **LEAGUE LIVE:** PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-10-28.json; 1 not in the pool, not simulated: Matisse Thybulle (MAXEY-MUM OVERDRIVE, BN)
  - LEAGUE INTAKE: PASS — 12 teams, 176 players, 176 of 176 resolved; 1 unpooled. Mo Bamba resolved, now in the pool (kit #218).
  - LEAGUE MOVES: PASS — 4 team(s) changed, 9 move(s), 2026-10-28 to 2026-10-28 (pm); wrote data/news/league_moves_2026-10-28_pm.json
- **Morning record untouched:** data/news/league_moves_2026-10-28.json sha256 `1c60130d…`, equal to the committed morning version.
- **ESPN injuries pin:** data/status/espn_injuries_2026-10-28.json written by status_feed (kit #216).

## League moves since the morning state (league_moves_2026-10-28_pm.json)

- **KEL'EL YAXEL HALQUETA (yours)** — added Bobby Portis; to IL: Tyrese Haliburton
- **Looking Cool Joker!** — added Keldon Johnson, Mo Bamba; dropped Precious Achiuwa
- **Lauri's Prime Rib** — to IL: Luka Doncic; off IL: Maxime Raynaud
- **Splash Mountain** — added Robert Williams III; to IL: Ziaire Williams

## Status since the morning status file (diff against morning commit 2beeb16)

- **Your roster:** Tyrese Haliburton Q (SG) → **O** (IL). Kyrie Irving and Yaxel Lendeborg are still Q; Kawhi Leonard still O (IL).
- **Opponent (Looking Cool Joker!):** Pelle Larsson's P flag is gone (no status row now).
- **STATUS GATE:** PASS — status_2026-10-28.json: 33 flagged row(s), each tiered with a dated receipt
