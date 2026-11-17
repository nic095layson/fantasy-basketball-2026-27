# Missed pickups, the blind spots behind them, and two display builds (2026-11-17)

Pull window: 2026-11-17 → 2026-11-17 (no pull: kit main a90bdbf, deck main 3551a15, the records branch season/daily at e971a0f, read only; 52 simulator runs, three package scans and one brief run in a throwaway worktree, sections 5 and 6).

**Owner's requests, verbatim (2026-11-17).** The card pick "Missed-pickup audit", then: "I'd like for you to continue auditing and finding cases where there was a case of missed-pick up player that was in my blind spot. You are my co-GM and truly, I do not want an echo chamber back to me, or blindly taking option "B", when there was truly a better "X, Y, Z" option that I hadn't even thought to consider. You are not only my devil's advocate, but also exploring all possible avenues to winning even if I do not see that potential". Then, on the card: build "Starts watch", "Hold check on drops" and "Open the pool"; "Score them properly" for three free players; "Quote both" for title and reach-the-final odds.

**Method up front.** Each choice was stated to the owner before the run that used it.

- Window: 2026-10-20 (the first brief) to 2026-11-16 (the last box score). The session's choice, not a file's extent.
- Adds: Yahoo's transaction feed on the records branch (`data/managers/transactions.json`, 179 rows from 10-15 to 11-17; Yahoo returned 1 entry the feed could not interpret).
- "Flagged": named in a brief's `waiver_top`, or separately its `streaming` list, on or before the add date. 28 briefs; there is none for 11-15.
- Value: a plain nine-category per-game z-sum from the window's box scores. It is not the kit's value: no category fit, no positions, no opponent. "Roster level" is the 156th best of the window (-2.09), "top 100" the 100th (+0.07).
- Signals: checked on the morning of each day, from games before that day, on players who were on no roster.
- Known answers: Poeltl's timeline against the raw feed; three players' lines recomputed by hand from the box-score files (Anthony Black 16.6 points over 9 games, Christian Braun 12.9 points and 2.3 steals over 10, Jalen Smith 13.75 points and 8.4 rebounds over 8); the committed script re-run against the scratch result (identical).
- A first pass used Yahoo team 10 as the owner. Team 10 is MISSI ELLIOTT; the owner is team 11. The owner's roster in the state file was the known answer that caught it, before any figure was delivered. Everything below is the re-run.

**Verdict: the best pickups of the last four weeks were mostly players the owner or the kit already had in hand. The kit's gap is coverage, not accuracy: it named 2 of the 16 rival pickups that then played at top-100 level, and its own flagged names did well (5 of 9 top-100). A pool-wide minutes watch as set for Wiggins and Claxton (30+ minutes, three straight) would have named none of the misses; "started his last two games" named 8 of 14. Two display lists are built from that: a starts watch and a hold check. The third pick, opening the pool, is not built: only 4 of the 24 unlined free players have a position on file, which a line needs, so the choice goes back to the owner.**

Runner impact: code-only (the morning brief gains two sections and one record key, `role_watch`). Display only; a failure inside it is printed in the brief and the brief still passes. No prompt, step, pass line or other output changes; the deck page is unchanged.

Pool rows touched: none

## 1. The count

EVIDENCE: `missed-pickups-2026-11-17/audit.json`, made by `audit.py` beside it.

| rival adds, 10-20 to 11-16 | all | with 3+ games since | top-100 level since | roster level since |
|---|---|---|---|---|
| never flagged | 90 | 72 | 12 | 29 |
| streaming list only | 17 | 12 | 2 | 7 |
| in `waiver_top` | 7 | 5 | 2 | 3 |
| total | 114 | 89 | 16 | 39 |

The kit's own flagged adds: 16 distinct names over the window, 9 with three or more games since the first flag; 5 of the 9 played at top-100 level and 7 at roster level. The owner's own adds: 17, 13 with three or more games since; 3 at top-100 level, 7 at roster level.

## 2. The cases

| # | player | what happened (feed timestamps, UTC) | since | the kit | visible before |
|---|---|---|---|---|---|
| 1 | Anthony Black | Owner added 10-22 20:20, before any rival, and dropped 10-24 08:05 for Collin Gillespie; Black had no game in between. ROOKS FTW added 10-26 | 17/5/6, 1.9 stl, 33 min, 9 starts in 9 | never flagged; line ranked 160th of 336 | 18 points and 5 threes on 10-25, after the drop |
| 2 | Christian Braun | The brief named him as the drop of every listed pair from 10-20 to 10-23, on title edges of -0.8 to +0.7. Owner dropped 10-24 01:26. John's Cool Team added 10-30 | 13/4/2, 2.3 stl, 33 min | flagged as an add 10-26, 10-29, 10-30 | a 33-minute start on 10-22 |
| 3 | Jalen Smith | Free 10-27 to 11-08. The owner made six other adds in that span | 15/7/2, 1.2 blk, 2.2 threes while free; 18/9/3 in 3 games since; day-to-day on 11-17 | flagged once, 10-31, second on the list | started every game |
| 4 | Klay Thompson | Free 10-20 to 11-04 and 11-07 to 11-09 | 18 pts, 4.4 threes in 5 games after the first add | never; line ranked 253rd of 338 | two straight starts; 25 points and 7 threes on 10-30 |
| 5 | Darryn Peterson | Free 10-26 to 11-02 | 21/4/4, 32 min | streaming list once, 10-31 | 30-minute starts from 10-21 |
| 6 | Daniss Jenkins | Free 10-29 to 11-09 | 21/4/4, 2.2 stl, 36 min over 4 games | never; ranked 243rd | none in the box scores |
| 7 | Duncan Robinson | Free to 10-23 | 17 pts, 3.7 threes, 31 min | never | two straight starts |
| 8 | Kevin Huerter | Free until 11-17 | 15 pts at 30 min over 5 games | streaming list once, 11-16 | none of the six signals |
| 9 | Jakob Poeltl | Free 10-29 to 11-01, 11-02 to 11-06, 11-07 to 11-09 | 12/7, 1.0 blk | streaming list | two straight starts |

INFERENCE: whether the owner dropped Braun because the brief named him. The records hold the brief's pairs and the drop, not the reason.

## 3. The patterns

| blind spot | EVIDENCE |
|---|---|
| Finding a riser, then renting him | Black, Ziaire Williams and Alex Caruso were the owner's three adds that then played at top-100 level; he held them for 0, 2 and 1 games. The playbook (section 3) has a rule for snagging a player trending up and none for keeping one |
| The same veterans every morning | `waiver_top` over 28 briefs: Julian Champagnie on 16 days, Bobby Portis 9, Cam Johnson 9, Jrue Holiday 4. Tobias Harris on 17 days; he has no box-score row in the window, and ESPN's 11-16 note has him out until early December |
| A role change is ranked late | Each of the 12 never-flagged top-100 pickups had a kit line below top-100 level on the add date (the best was -0.3 on the audit's scale, where +0.07 is the cut). INFERENCE: a projection is narrower than a box-score average, so the two scales are not the same; the ranks in section 2 are the cleaner evidence |
| No line, no score | 77 free players averaged 18+ minutes over 4+ games from 11-03 to 11-16; 24 have no pool row (25 by the audit's name fold; the kit's fold matches Herb Jones to his row). Nolan Traore and Matisse Thybulle had none on the day rivals took them |
| The two weakest lines are the two centres | 11-03 to 11-16: Kel'el Ware 6/5 in 17 minutes, Neemias Queta 8/8 in 22. Both kit lines sit above that. Section 5 shows the simulator still prefers both to a wing |

## 4. Would a watch have caught them?

The 14 add events (13 players) that the kit had not put in `waiver_top` and that played at top-100 level afterwards.

| signal | named before the add | players it fired on in four weeks | of those with 3+ games after: roster level | top-100 |
|---|---|---|---|---|
| 30+ minutes, 3 straight | 0 of 14 | 7 | 3 of 5 | 2 |
| 30+ minutes in 2 of the last 3 | 3 | 29 | 8 of 17 | 6 |
| last 2 games 6+ minutes over his average | 2 | 68 | 12 of 47 | 5 |
| **started his last two games** | **8** | 66 | 26 of 54 | 14 |
| last 3 games at roster-level value | 6 | 108 | 35 of 84 | 12 |
| last 3 games at top-100 value | 4 | 68 | 25 of 48 | 10 |

Two straight starts is the best screen and no more than a screen: 28 of its 54 graded names did not play at roster level afterwards.

## 5. Three free players, scored (owner's pick)

Kelly Oubre Jr., Ziaire Williams and Jerami Grant against Ware, Queta, PJ Washington and Cameron Johnson. 10,000 seasons × seeds 2026 and 2027, injured players never returning (the brief's world), records e971a0f, the live lines (minutes ratio on PTS, REB, AST). No move: title 14.1% (13.98 / 14.19), final 27.1%. Each swap was run twice: on the kit's line, and with the added player's line replaced by his own box-score average for 11-03 to 11-16 (the session's window; 5, 6 and 6 games). EVIDENCE: `missed-pickups-2026-11-17/swap_scores.json`. The kit's own package scan gave the same kit-line figures within 0.1.

| add, for the drop | kit's line: title / final | last-14-day line: title / final |
|---|---|---|
| Ziaire Williams for Queta | -0.8 / -1.3 | +2.0 / +2.2 |
| Ziaire Williams for Cameron Johnson | -1.1 / -1.1 | +1.8 / +2.3 |
| Ziaire Williams for PJ Washington | -0.9 / -1.1 | +1.3 / +1.5 |
| Ziaire Williams for Ware | -1.4 / -2.4 | +1.2 / +1.3 |
| Jerami Grant for Cameron Johnson | -1.4 / -1.8 | +1.0 / +1.2 |
| Jerami Grant for Queta | -1.7 / -2.5 | +1.0 / +1.1 |
| Jerami Grant for PJ Washington | -1.7 / -2.3 | +0.6 / +1.3 |
| Jerami Grant for Ware | -2.3 / -3.3 | 0.0 / -0.1 |
| Kelly Oubre Jr. for Queta | -1.5 / -2.1 | +0.7 / +0.7 |
| Kelly Oubre Jr. for Cameron Johnson | -1.7 / -2.4 | +0.6 / +0.6 |
| Kelly Oubre Jr. for PJ Washington | -1.4 / -2.2 | +0.4 / +0.5 |
| Kelly Oubre Jr. for Ware | -2.3 / -3.3 | 0.0 / -0.2 |

Two error bars. Sampling: about ±0.7 on a difference. Structural: the line choice moves every swap by 2.3 to 2.9 points of title share and flips its sign, so no row is a verdict. The recent lines carry shooting that will not hold (Williams and Grant both 57% from the field over six games).

**weekly_availability is FRAGILE:** -0.8 (healthy at the old 0.88) / -0.3 (healthy at the unfloored fit (0.78)) / -2.6 (risk at the old 0.75) / +1.4 (risk at the unfloored fit (0.56)); headline title share 14.1% ± 0.5 (MC) within that band. Sweep of 2026-11-16, made on the lines before the minutes switch; no sweep has run on the switched lines with the new constants.

What holds on both lines: Williams is the best of the three, and Ware is the worst drop in every row.

## 6. What was built

| build | what it is | checks |
|---|---|---|
| Starts watch | `scripts/role_watch.py`, a new "Starts watch (free players)" section in the brief: every player on no roster who started his last two games, with the last three games' minutes and line, the length of the run, whether the pool has a line for him, ESPN's injury line, and the day a team dropped him. New runs and fresh drops are always printed; the rest fill the list to eight by minutes | `scripts/test_role_watch.py`, 23 tests |
| Hold check | The same module, a "Hold check (before you drop)" section: the owner's active players added in the last seven days or named as a drop by the day's pairs or streaming line; the last three games, games since the add, "nothing to judge yet" when he has not played since, and "HOLD?" when a free player with his run would be on the starts watch | the same file; two tests in `scripts/test_daily_brief.py` |

Run on the real records (scratch worktree of e971a0f, `python3 scripts/daily_brief.py --date 2026-11-17 --seasons 10000`): every key of this morning's brief record is unchanged; the new record lists 20 free players on a run of starts (9 printed) and three hold lines.

Known answers on the real records, graded pass or fail:

| case | result |
|---|---|
| Jalen Smith on the starts watch while free | PASS: listed on 11-03, seven starts in a row |
| Darryn Peterson on the starts watch | PASS: listed on 10-28, "dropped 2026-10-26 by ROOKS FTW" |
| Christian Braun, named as the drop on 10-24 | PASS: "HOLD? he started his only game" |
| Anthony Black, added 10-22 | FAIL on the real records: the league-moves records of 10-22 and 10-23 do not hold the owner's add, so no hold line would have printed. The same case passes on a fixture. The moves records have carried the owner's adds since 10-24 |
| Ziaire Williams and Alex Caruso | Not caught by design: both came off the bench. The hold check prints their line without a HOLD |

The four thresholds (2 starts, 7 days stale, 3 days for "dropped", 7 days for a pickup) are display thresholds, hand-set and declared in the module; nothing downstream reads them, and none is an engine constant (`scripts/redteam/check_constants.py` passes unchanged).

## 7. What was not built: open the pool

A pool row needs a position; the lineup and the waiver scan place a player by it. Of the 24 free players with real minutes and no line, 4 have a position anywhere on disk (Yahoo's free-agent list of 100: Jase Richardson, Morez Johnson Jr., Brice Sensabaugh, Bennett Stirtz). EVIDENCE: `data/source/flaim/pull_2026-11-17.json`, `report/projections-2026-27.csv`. The other 20 would need a new source of positions, and the morning pull is the Runner's.

It is also a change to how the season line is made, with new constants to register, so under RULES.md rule 12 it lands on a Monday. The starts watch already prints "no line in the pool" beside such a player, so he is no longer invisible.

## 8. Decisions for the owner (nothing changes without a pick)

1. This pull request (the report, the two lists, three corrections rows): merge or keep as a draft.
2. Open the pool: the narrow version (the four with a position, for Monday 11-23), the wide version (a positions source, which means a change to the morning pull from the Runner's own conversation), or leave it to the starts watch.
3. The two lists reach the brief only. Showing them on the deck's Waivers tab is a separate change to `season_deck.py`.
4. The waiver scan's repeated names (Tobias Harris 17 days without a game; Portis 9 days): assess the scan's ranking, or leave it.
5. A keep rule for the playbook: the owner's own words, at Monday's review, if he wants one.
6. Ziaire Williams: section 5 is conditional on the line. The call is his.

## 9. Bounds

Out of scope by design: no line, constant, roster or pool row was changed; no trade was scored (owner veto 2026-10-20); positions, category fit and the weekly opponent are outside the audit's value score; the deck page; the Runner's prompts.

In scope and unverified:
- Every "since" line is 3 to 13 games. NOT-ATTEMPTED: no test of whether these lines persist; week 5 is graded on 2026-11-23.
- Section 5 changed only the added player's line. NOT-ATTEMPTED: the dropped players' recent lines, though Queta and Ware have played below their kit lines.
- Bids and waiver priority behind each add: did not check; the feed's `faab_bid` field is empty on the rows read.
- One Yahoo entry the feed could not interpret: ATTEMPTED-FAILED, the feed's own warning names it and gives no content, so one move in the window may be missing.
- The sweep quoted in section 5 predates the minutes switch; the season sweep's next run is the Runner's.
- The signal table counts a signal as "before the add" by date, not by hour.

## 10. Provenance

Session of 2026-11-17 (session model A), the Main session; branch `claude/new-session-koi1jp`. Records: kit main a90bdbf, deck main 3551a15, season/daily e971a0f. Re-verify: `python3 report/after-reports/missed-pickups-2026-11-17/audit.py --records <checkout of season/daily at e971a0f>` rewrites `audit.json`; `python3 scripts/test_role_watch.py`; `python3 scripts/test_daily_brief.py`. Corrections logged with this report: Poeltl's free window, the count of unlined free players, and the range of the brief's Braun edges.
