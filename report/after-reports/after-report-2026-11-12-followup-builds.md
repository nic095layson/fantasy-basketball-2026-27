# Three follow-up builds from the evening's tests (owner 2026-11-12, on the council's verdicts)

Pull window: 2026-10-20 → 2026-11-12 (no pull: kit main f6d49f5; the records branch season/daily at 0e21df1 with box scores through 2026-11-11 and the 21:03 rosters of 2026-11-12, read only; simulation and backtest runs in scratch).

**Owner's request, verbatim:** "I've just reset my Fable usage for the week. What tests and computations can you do to help improve the system at this time? Please conduct what is helpful and let me know any findings you bring". Then, on the card offering four follow-up builds: "Council deliberates and proceed with their verdicts".

**Method up front.** The tests ran read-only in scratch and were reported in chat first. The council (five roles, one vote each) took the four builds after the facts each turned on had been read from the code and the published deck's data. The plan table, with each parameter, was shown before any file was written. Tests were written first and seen failing. The deck was then rebuilt from today's records in a throwaway copy and the new button clicked in a browser.

**Verdict: three of the four were built and one was declined. Trending Up now lists a free agent on a minutes rise only; the filed drop-order check uses the corrected IL list and carries tonight's re-run; a "Full health" button sits beside "My build". The one-sided threes candidate was not built, because the kit already saves both lines each week and the idea can be graded from them later.**

Runner impact: code-only — the morning and afternoon decks pick up the Trending Up rule and the new button from `season_deck.py`; no step, record field or prompt changes.

Pool rows touched: none

## 1. The council's verdicts

| Build | Vote | Verdict | Deciding point |
|---|---|---|---|
| Trending Up on minutes only | 5 to 0 | Built | The backtest caps any usage-only edge at about 0.6 points a game, with worse availability; usage stays as a column, so the rule is one line to restore |
| Refresh the drop-order record | 5 to 0 | Built | A filed record its author knows to be wrong; the corrected run already existed |
| "My build" at full health | 4 to 1 | Built as one button | "My build" reads a roster missing two stars while the owner weighs moving a player it ranks last; IL stints recur all season. Dissent: the window is ten days and the read depends on the method |
| One-sided threes candidate | 0 to 5 | Not built | Found by slicing three weeks after the fact; the smaller of the live and candidate lines is that candidate, computable from saved lines at any later date |

## 2. Trending Up: what the backtest showed

Box scores 2026-10-20 to 2026-11-11; every player-date with three later games for his team (1,536, 370 players); a game he missed counts as zero. Flags as the deck drew them before this change. "Edge" is against unflagged players, with a player-level bootstrap interval. Script and output: `followups-2026-11-12/trend_backtest.py`, `trend_backtest.txt` (two runs, identical output).

| Trigger | Flags | Appeared in his team's next 3 | Minutes edge per team game | Points edge per team game |
|---|---|---|---|---|
| Minutes up 6 or more | 126 | 88% | +0.96 (95% -0.38 to +2.41) | +0.24 (-0.66 to +1.15) |
| Usage up 4 or more, minutes not up | 160 | 84% | +0.19 (-0.95 to +1.29) | -0.10 (-0.88 to +0.62) |
| Not flagged | 1,043 | 90% | | |

- The usage-only players appeared in fewer of their team's next games: -5.7 points of appearance rate (95% -10.1 to -1.3).
- The minutes flags with five later games (71) ran 16.2 minutes before, 25.0 in the flagged three, 24.1 over the next three and 23.3 over the two after. The rise lasts; the edge over a season average is about one minute and its interval includes zero.
- A first pass counted only the games a player appeared in and overstated the minutes edge (0.4 to 2.4). The table is the corrected pass.

The change: the card lists a free agent when `trend` is "up"; `usg_trend` no longer lists anyone. The two usage columns and their mark stay. `form_board.py` and the form record are unchanged.

## 3. The drop-order record (attack A-11)

`findings-fix-2026-11-12/drop_band.py` built its IL list without the pool, so two rivals' unpooled IL-slot players were simulated as playing every week (the defect fixed in `il_return.py` this afternoon). One line changes (`by=by`). The record was re-made on the 21:03 rosters: 6,000 seasons, seeds 2026 and 2027, baseline plus 10 variants. The first record is kept as `drop_band_2026-11-12_pre-il-fix.json`.

Share of simulated seasons won by the owner, mean of the two seeds:

| Pair leaving for the two returns | First record | Re-made | Rise |
|---|---|---|---|
| Queta, then Washington (the room rule's pick) | 25.12 | 26.34 | +1.22 |
| Queta, then Cam Johnson | 27.09 | 28.10 | +1.01 |
| Champagnie, then Queta | 26.49 | 27.93 | +1.44 |
| Champagnie, then Cam Johnson | 26.23 | 27.34 | +1.11 |

- Across all 11 configurations the rise is 0.4 to 1.9. It mixes the fix with one rival roster move between the two rosters.
- The rule's pair is last in 22 of 22 seed-runs, behind Queta and Cam Johnson by 1.2 to 3.3 on the two-seed mean.
- The other three pairs are within 0.8 of each other at baseline and change places in 3 of 11 configurations.
- The two seeds differ by 1.4 to 2.2 at baseline, so read each level as about plus or minus 1.

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds. That is the 2026-11-09 sweep the brief quotes, for the headline title odds; the record applies the same variants to the drop pairs.

A second run, baseline only, 10,000 seasons, same seeds, asked whether "keep Washington" was really "keep two centers" (`followups-2026-11-12/centers.py`, `centers.json`, `centers.log`):

| Pair leaving | Seasons won, % | By seed |
|---|---|---|
| Queta, then Cam Johnson | 27.98 | 28.53 / 27.44 |
| Champagnie, then Queta | 27.63 | 28.07 / 27.20 |
| Champagnie, then Cam Johnson | 27.38 | 27.98 / 26.77 |
| Queta, then Ware | 26.79 | 27.32 / 26.25 |
| Queta, then Washington | 26.38 | 27.16 / 25.59 |
| Cam Johnson, then Washington | 26.20 | 26.94 / 25.46 |
| Champagnie, then Washington | 25.71 | 26.37 / 25.06 |

Every pair that includes Washington is at the bottom, including the one that keeps Queta. The two-centers reading is not supported.

## 4. "Full health"

"My build" ranks the owner's categories with IL players counting nothing (the owner's rule D-IS-8 for the build strip) and switches off those ranked 10th or worse. "Full health" does the same with every team's IL players counted as active and no cuts applied. It is drawn only when some roster has an IL player on the board. A player the board does not rank counts nothing in either view; today two rostered players are off the board (Jimmy Butler, Jusuf Nurkic). Display only: the build strip, the board's order and the simulator are unchanged.

On the deck rebuilt from today's records:

| Button | Switched off | Derrick White's fit |
|---|---|---|
| My build | AST, STL | -0.37 |
| Full health | AST | +0.18 |

The owner's ranks behind it (of 12), from the published deck's data:

| Basis | REB | AST | STL |
|---|---|---|---|
| Today, IL counting nothing | 7 | 12 | 11 |
| Every team's IL players active, no cuts (the button) | 8 | 12 | 7 |
| Only the owner's IL players active, no cuts | 10 | 12 | 6 |
| Every team's IL active; Queta and Cam Johnson cut | 8 | 11 | 4 |
| Every team's IL active; Champagnie and Cam Johnson cut | 5 | 10 | 6 |

A correction to what was said in chat before the council: rebounds was called weak (10th) once Queta is cut. That counted only the owner's IL players. With every team's counted it is 8th. Assists and steals read the same on either basis. The row is in `report/corrections-log.md`.

## 5. Checks

| Check | Result |
|---|---|
| New tests seen failing first | Trending: the usage-only free agent was still listed. Full health: the button did not exist |
| New tests after | 3 pass (one changed, two new); the no-IL test is a guard and passed before the change too. The Full health test clicks the button on the Board and on the analyzer tab |
| Attack list | PASS: 11 attacks, CURRENT 10, UNFINGERPRINTED 1; A-11's record carries the changed script's hash |
| Deck on today's records | PASS, 7 tabs, 0 page errors; six trending names, the same six as this afternoon's deck |
| Full suite | 1,200 tests OK, 2 skipped (was 1,198) |

## 6. Bounds

Out of scope by design: the usage threshold and formula (kept; only what lists a player changed); the build strip's IL rule; any projection line, constant or roster; the threes candidate.

In scope and unverified:
- Whether tomorrow's 5 AM form record, the first made with the usage code, would have listed usage-only names: did not check; the afternoon record predates that code.
- The backtest covers 23 days. A usage edge under about 0.6 points a game cannot be ruled out, nor one that appears later in the season.

## 7. Next steps (owner decisions)

1. Merge this PR, or not. Merged before 5 AM Pacific, tomorrow's deck uses the minutes-only rule.
2. The one-sided threes idea is graded from saved lines on 2026-11-23 and reported in chat; nothing to decide until then.

## 8. Provenance

Session of 2026-11-12 (session model A), branch `claude/market-data-workorder-mnfi2b`. Records: `findings-fix-2026-11-12/drop_band.json` (deck 01483de, records 0e21df1, state, pool and schedule hashes inside), `followups-2026-11-12/`. Re-verify: `python3 scripts/redteam/run_attacks.py --check`; `python3 -m unittest test_season_deck.TrendingUp test_season_deck.FullHealthBuild` in `scripts/`; `python3 report/after-reports/followups-2026-11-12/trend_backtest.py` against the records checkout.
