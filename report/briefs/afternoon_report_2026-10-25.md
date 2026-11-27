# Afternoon check — 2026-10-25 (Sunday, week 1 closes tonight)

T0 2026-10-25T22:04:29Z (fire 22:04:02Z). Kit head at run start d887553 (this morning's record); origin/main ec6264c already contained ("Already up to date"); tree clean, no stash.

## Pull
- Flaim (Yahoo): get_user_session once, then 12 rosters one at a time — 12 of 12 on the first call, no YAHOO_AUTH_UNAVAILABLE, no retries. FantasyBot not needed, not called.
- The re-pin of data/source/flaim/pull_2026-10-25.json kept the morning's matchups, free agents and 12 dated lineups (carried_forward block present).

## Lines
- LEAGUE INTAKE: PASS — 12 teams, 172 players, 172 of 172 resolved; 0 NBA-team disagreement(s) with the pool
- LEAGUE MOVES: PASS — 2 team(s) changed, 5 move(s), 2026-10-25 to 2026-10-25
- LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-10-25.json
- STATUS GATE: PASS — status_2026-10-25.json: 22 flagged row(s), each tiered with a dated receipt

## League moves since the morning state (rosters 12:0xZ to 22:0xZ)
- Booker T Floppers: added Derrick Jones Jr. and Tristan da Silva; Zach Edey to IL (roster now 15 with two IL).
- Looking Cool Joker!: added Obi Toppin, dropped Brandon Williams (Williams was added only yesterday).
- Your roster and your opponent's: no change.
Note: league_moves_2026-10-25.json now holds this afternoon diff and no longer the morning's 10-24 → 10-25 diff (5 teams), which survives in commit d887553 and in brief_2026-10-25.md. Same overwrite as noted on 10-22 and 10-24; not fixed by me.

## Status changes since the morning status file (commit d887553)
- Yours: Kyrie Irving's row is gone — Yahoo no longer shows a status tag on him; he is still in your IL slot. No other change on your roster.
- Opponent (MAXEY-MUM OVERDRIVE): Joel Embiid D → O (Util slot). Knueppel and Beal unchanged (O, IL).
- League-wide, 26 rows → 22: tags cleared on Brandin Podziemski, Draymond Green, Fred VanVleet, LeBron James, Stephen Curry (Curry stays on IL); Cameron Johnson O → Q (on IL); Keegan Murray Q → D; Zach Edey moved to IL; new rows Naji Marshall O and VJ Edgecombe Q.

## Nothing failed. No stash.
