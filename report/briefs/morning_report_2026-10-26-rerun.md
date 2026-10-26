# Morning re-run report — 2026-10-26 (on main d04523d)

Owner-ordered re-run of today's morning run after PR #192's fixes. This morning's
report (`morning_report_2026-10-26.md`) stays as it was. **The re-run overwrote the
day's brief (`brief_2026-10-26.md/.json`), deck (`report/season/deck_2026-10-26.html`)
and `report/briefs/morning_2026-10-26.json`; git history keeps the originals (commit a221c73).**

- **T0:** 2026-10-26T15:06:55Z
- **Base:** d04523d confirmed on origin/main; merged into season/daily cleanly (da09128). No stash (tree was clean).
- **Pull:** Flaim session + league info, 12 rosters one at a time (no retries), current matchups (week 2, all 0-0-9), 100 free agents, FantasyBot outlook once. Skipped as ordered: last-week matchups, dated rosters, transactions. Not run as ordered: scoreboard_intake.py, manager_log.py, availability_calibration.py.

## Lines, this morning vs re-run

| Check | This morning (a221c73) | Re-run |
|---|---|---|
| LEAGUE LIVE | HALT — Trevon Brazile not in the pool | PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-10-26.json; no unpooled names |
| LEAGUE TABLE | FAIL — unreadable '/' value | PASS — week 2; wk1 finished (rebuild), wk2 not started (Yahoo shows no stats yet); power #1 MAXEY-MUM OVERDRIVE (0.626), you #10 (0.429) |
| MORNING | — | PASS — 2026-10-26: 13 steps; brief report/briefs/brief_2026-10-26.md; record report/briefs/morning_2026-10-26.json |

- **Unpooled names:** none. Brazile is now pooled (owner's `data/pool_additions.csv` row from PR #192, which the season build appended to `projections_season.csv`; no existing line changed). He is still **left out of the season simulation** (frozen v69 sim pool, D-IS-8 rule); the waiver scan counts him.

## Roster (league_state as_of 2026-10-26)

PG Haliburton · SG White · G Gillespie · SF McDaniels · PF Durant · F Lendeborg · C Ware · C Queta · UTIL PJ Washington · UTIL Kyrie Irving · BN Ty Jerome · BN Miles Bridges · BN Julian Champagnie · IL Kawhi Leonard (Q).
Expected facts hold: Champagnie on, Clowney off; Kyrie off IL; Kawhi on IL.

## Brief

- **Lineup:** PG Jerome, SG Durant, G White, SF McDaniels, PF Bridges, F Lendeborg, C Queta, C Ware, Util Haliburton, Util Irving. Bench: Gillespie, Washington. No game: Champagnie.
- **Waiver scan:** 5 of 520 pairs positive (base ECW 5.258). Top: Bobby Portis for PJ Washington (+0.006 ECW, title 22.0%, −0.6); Jrue Holiday for Gillespie (+0.003, 21.5%, −1.1); Christian Braun for Champagnie (+0.002, 23.6%, +1.0). Every drop in these pairs is a current player; none drops Clowney or anyone no longer owned.
- **Title** 22.6% ± 0.6 sampling; playoffs 99.1%. Structural band: TEAM_WEEK_SHOCK FRAGILE (+2.3/−3.4), weekly_availability FRAGILE (−2.0/+0.8, −1.5/+0.9). Pair deltas of ±1 point sit inside both bands.

## Week matchup

WEEK MATCHUP: PASS — week 2 vs Looking Cool Joker!; to date rebuilt (Yahoo's week 2 totals could not be read: unreadable makes/attempts value '/'); to date 0 day(s); projected 6-3-0; pickups: no finished low-value player.

## Deck

Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as version 1793027463-3979 (before: 1793025305-e4a8, the stale-run deck). Post-publish read: the 491,911 built bytes are contained in the live page (492,457 bytes with the host wrapper), the seven-tab list appears exactly once, and the stamp is generated_utc 2026-10-26T15:10:46Z. STATUS GATE PASS (26 rows); SEASON DECK PASS (7 panes, 314 board rows, 0 page errors).

## Failures

None in the re-run. Standing flags (unchanged, not fixed): the afternoon run overwrites the morning league_moves file; the morning prompt's commit list omits report/league, report/form, report/calibration*.
