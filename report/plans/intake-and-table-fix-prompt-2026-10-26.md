# Prompt: fix the 2026-10-26 league-live halt and league-table failure

Written 2026-10-26 by the morning-runner session at the owner's request, to be pasted into the Fantasy Basketball session. Source records: report/briefs/morning_report_2026-10-26.md (commit a221c73).

```
Owner request (David, 2026-10-26): fix the two failures in this morning's run (2026-10-26) so they cannot freeze or break future runs. Ship this as an ordinary PR into main. Do not touch season/daily or PR #165, and merge nothing.

Governors: load anthropic-skills:plan-gate before the first change and adversarial-verify before you report. CLAUDE.md rule 4 applies: when a decision is mine, give me 2–4 options with the recommended one first, as AskUserQuestion cards. Do not build an option I have not chosen.

## Background (read these records; nothing here is from memory)
- report/briefs/morning_report_2026-10-26.md and report/briefs/morning_2026-10-26.json on season/daily (commit a221c73).
- Failure 1, league live HALT: "LEAGUE INTAKE: HALT — 1 name(s) not in the pool; nothing written: Trevon Brazile (Podz save the league, PF, DEN, status -)". scripts/league_intake.py run() refuses the whole pull when any rostered name outside an IL slot is missing from the pool (deck players.csv plus data/pool_additions.csv). Result: data/league_state.json stayed at 2026-10-25. The brief, waiver scan, title odds and deck ran on a stale roster. My own move (added Julian Champagnie, dropped Noah Clowney) and Kyrie Irving / Kawhi Leonard swapping IL status were invisible, and all three waiver pairs recommended dropping a player I had already dropped. This will happen again whenever any manager adds a player outside the frozen pool.
- Failure 2, league table FAIL: "LEAGUE TABLE: FAIL — unreadable makes/attempts value '/'". On day one of a week, Yahoo's FGM/A and FTM/A are "/" and the counting cells are "". flaim_live._pair() raises PullError, and league_table.py turns that into a fatal TableError. week_matchup.py already catches the same PullError and falls back to a rebuild. This will fail every Monday.

## Work item 1: get Trevon Brazile into the pool (today's unblock)
Follow the Andre Drummond precedent in data/pool_additions.csv (owner 2026-10-21; read its note column and commit e36596a):
- Fetch his data live from both sources the precedent used: Flaim's player data for the league, and FantasyBot's player value for him. Pin both responses under data/source/flaim/ and data/source/fantasybot/ with dated names.
- Build his line by the same 10/14 blend rule the Drummond note describes. If a source is missing or does not return him, stop and tell me what you tried. Never fill a line from memory.
- Add one row to data/pool_additions.csv with a full note column: sources, dates, rule, and "owner 2026-10-26".
- Prove it: run `python3 scripts/league_live.py --as-of <today> --since <now>` against the pinned 2026-10-26 pull or today's pull. LEAGUE LIVE must print PASS with "rosters from Flaim (Yahoo)". Leave the 13 FantasyBot roster calls out of this.
- Tell me in one line whether the simulator leaves him out the way it leaves out Drummond (absent_from_sim, D-IS-8).

## Work item 2: stop one unknown pickup from freezing the whole league (decision first)
Before building anything, present these options as AskUserQuestion cards with your recommendation first, then build only the chosen one.
(a) Partial intake with a loud flag. Write league_state.json with every resolvable player. Carry each unpooled non-IL name as an `unpooled` entry with no projection line, like the existing unpooled_il path. Print a named non-fatal warning line, and surface the names in the brief and on the deck's Today tab as "not in the pool, not simulated". The run continues on today's rosters, and the gap is visible every day until a pool_additions row lands.
(b) Keep the halt, but make it visible. Leave the intake rule as is, and add a top-of-brief and deck banner when league live halts: "rosters frozen at <date>; these moves are not seen: …", built from the pinned pull's roster diff.
(c) Halt only when the unknown name is on my roster or my current opponent's. Partial intake (as in a) for every other team.
Constraints for whichever I choose:
- The Council 2026-10-15 rule in data/unpooled_il.json stays intact for IL slots. Say plainly how the chosen option relates to it, because (a) and (c) widen it.
- Nothing silent. Every unpooled name appears in the LEAGUE LIVE line, the brief and the deck.
- The simulator never invents a line for an unpooled player.
- No engine constant, projection line or injury tag changes.

## Work item 3: make the league table survive an unplayed week
In scripts/league_table.py, a side whose FGM/A and FTM/A are "/" and whose counting cells are empty (a week with no games yet) must not be an error:
- Record that week as not started: zero games, totals None or zero, score 0-0-9 as Yahoo reports it. Follow week_matchup.py's handling as the precedent.
- Print a PASS line that says so, for example "wk2 not started (Yahoo shows no stats yet)".
- Any other unreadable value (such as "12/" or "abc") must still fail loudly. Do not loosen _pair() globally. scoreboard_intake.py and week_matchup.py depend on it failing.

## Tests and proof
- Add regression tests: test_league_table.py for a not-started week ('/' and '') and for a still-malformed value; test_league_intake.py (or test_league_live.py) for the chosen work-item-2 behaviour, with an unpooled bench player on a rival team and, if (c) is chosen, on my team.
- Run the full test suite and quote the counts.
- Rerun this morning's failing steps against the pinned data/source/flaim/pull_2026-10-26.json and quote the new LEAGUE LIVE and LEAGUE TABLE lines.
- Run `python3 scripts/morning.py --help` and confirm `--since` is still listed. The scheduled runner depends on it.

## Out of scope (flag, do not fix)
- The afternoon run overwriting the morning's data/news/league_moves_<date>.json.
- The morning prompt's commit list missing report/league, report/form and report/calibration*.
- Anything in the deck repo's engine.

## Report back
- The PR link.
- The option I chose and what it changes.
- Brazile's pool row and its sources.
- Before and after lines for both failures.
- Test counts.
- Anything the scheduled morning and afternoon prompts must change. Do not edit the scheduled prompts yourself; tell me the exact wording.
```
