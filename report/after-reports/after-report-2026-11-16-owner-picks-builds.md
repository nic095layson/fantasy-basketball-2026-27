# Owner picks of 2026-11-16: week card, decision grader, minutes line, records (availability floor blocked)

Pull window: 2026-11-16 → 2026-11-16 (no pull: kit main 88faf9b; the records branch season/daily at 12964ec, read only, re-run in a throwaway worktree).

**Owner's picks, verbatim (clickable cards, 2026-11-16):** "Build both fixes (Recommended)" (week card); "Fit with a floor (Recommended)" then "Band edge: 0.80 / 0.65 (Recommended)" (availability tiers); "Wait for today's re-run (Recommended)" (prior strength: no change); "Switch now (Recommended)" (minutes line); "All three (Recommended)" (records); "Grade from box scores (Recommended)" (decision grader).

**Method up front.** Each build's rule was stated to the owner before any file was written (plan table in the session). Tests first, seen failing, then the code; each change re-run on the 2026-11-16 records in a throwaway worktree of season/daily.

**Verdict: four of five built. The availability floor is not built: the tiers live in the deck repository, which this session could not attach (the attach request was refused by the session's permission check).**

Runner impact: code-only — the morning run's season-lines step now also writes `projections_season_blend.csv` and `pool_season_blend.csv` and puts the minutes ratio on the live line's PTS, REB and AST; the minutes-line step reads the blend; the board JSON gains a `scale` key; the week card reads `espn_injuries_<date>.json` beside the status file. No step added or removed; no Runner prompt change.

Pool rows touched: none

## 1. What changed

| Build | Rule | Where |
|---|---|---|
| Week card: auto-row players | A team's `unpooled` rows count through their pool line; an IL-slot unpooled row counts 0 | `week_matchup.py` `active()`, slot map |
| Week card: return dates by day | Today keeps today's tag. On a later day, a player whose ESPN return date is on or before that day counts 1.0. No return date keeps today's tag all week | `week_matchup.py` `day_avail()`, `_return_dates()`; record key `return_dates` |
| Decision grader: off-board players | A player the window-end board does not carry is scored from his box-score games in the window on that board's own z scale; total times the board's availability factor at gp = 82 × games / team games. A board written before today has no scale: the row stays pending and says so | `season_board.py` `scale_of()`, `score_line()`; `decision_grade.py` `box_value()`; a box row with no pool name matches on its box-score name |
| Minutes line on PTS, REB, AST | Live line = blend × minutes ratio (forecast / implicit minutes) on those three columns only; every other column is the blend's. The deck plane takes the same player's ratio by folded name, the box pull's name-to-pool bridge, or the alias table | `season_lines.py` `minutes_switch()`, `SWITCH_CATS` (registered, 53 = 53); `minutes_line.py` reads the blend; accuracy card and deck wording |
| Records | Three corrections (11-14, 11-16 twice) and three owner statements (11-14) | `report/corrections-log.md`, `OWNER-PLAYBOOK.md` |

## 2. Checks

| Check | Result |
|---|---|
| New tests seen failing first | Week card 5 (also run by the 7 subclasses of its end-to-end fixture), grader 3, board scale 1, season lines 2 |
| Week 5 on today's records, fixed card | P(5+ categories) 0.8743 on two runs (the card as published: 0.570); starts 43 v 40; Hezonja 2 starts, Jerome and Irving 3 each (from 11-18) |
| Minutes switch on today's records | PTS/REB/AST differ from the blend on 276 of 327 kit rows and equal the candidate's on all 327; every other column equals the blend; kit and deck planes match on every shared name |
| Grader on today's records | Hezonja scores −4.634 from 14 games on the 11-16 board's scale (built in the worktree). His live row R-2026-11-16-01 stays pending: its window opens today and he has no game in it yet |
| Constants registry | PASS, 53 registered = 53 live |
| Full suite | 1,236 tests: 1 failure, the deck test that pinned both switch rules as undecided; updated to the decided wording, then green (see the gates record) |

A side effect to know: the grader's interim gaps move with the switch, because the board's values change (R-2026-10-31-01: −0.07 → −0.13 as of today).

## 3. Not built: the availability floor

The owner picked healthy 0.80 and injury-risk 0.65 (minor knock stays 0.79: measured 0.885, n 26). The constant is `weekly_availability` in the deck repository's `arena/arena.py`. This session's GitHub scope is this repository only, and the request to attach the deck repository was refused. What the change needs, once that repository is reachable: the two return values in `arena.weekly_availability`; the kit registry's value and band (proposed band: healthy 0.88 / 0.78, risk 0.75 / 0.56, the old values and the unfloored fit); the deck page's tier labels (`season_deck.py`, keyed by value); and a fresh season sweep on the new engine. Nothing on the kit side was changed for it, so the tiers stay 0.88 / 0.75 until then.

**weekly_availability is FRAGILE:** -3.2 (no in-sim injury discount (risk 0.88 like healthy)) / +2.8 (harsher risk tier (0.65)) / -0.1 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), on the 2026-11-16 sweep (`redteam-2026-11-16-season/sweep.json`). The owner's two values sit on two of these variants, each swept alone (+2.8 and -0.4 points of title share); together they were not run. This report quotes no title share.

## 4. Prior strength: re-run and the combination test (owner: "Test with the switch first", then "Keep; re-test at week 10")

The scheduled week-5 re-run of the recency backtest (`recency-2026-11-05/backtest.py` from main, box scores through 11-15, min games 6 and 8; records in `recency-2026-11-16/backtest_min*_all.json`) again finds halving the PTS/REB/AST prior better than the blend: PTS −0.067, REB −0.023, AST −0.018 (6+ games, 2,177 player-games), every interval excluding zero at both cutoffs. Run again with today's minutes switch in both arms (`recency-2026-11-16/backtest_switch.py`, records `switch_min*_all.json`):

| | switch vs blend | prior /2 on top of the switch | interval of that extra gain (6+ / 8+) |
|---|---|---|---|
| PTS | −0.069 | −0.020 | −0.043 to +0.002 / −0.044 to +0.003 |
| REB | −0.030 | −0.004 / −0.003 | −0.015 to +0.004 / −0.014 to +0.006 |
| AST | −0.017 | −0.006 | −0.014 to +0.001 / −0.013 to +0.001 |

The switch's gain over the blend is confirmed on this backtest (intervals excluding zero). Halving the prior adds a gain whose interval includes zero on all three; the owner kept the prior and asked for this test again at week 10.

## 5. Bounds

Out of scope by design: a change to the prior strength (section 4: kept, re-tested at week 10); a blend column on the weekly accuracy card from week 6 (week 5's snapshots were taken on 11-15, before the switch, so week 5 grades both lines as they stand).

In scope and unverified:
- The advice back-fill into `data/decisions/session.jsonl` is on the records branch season/daily, which takes the owner's explicit word; not written.
- The ESPN return dates are ESPN's own estimates; their accuracy is graded on 2026-11-25 (scheduled).
