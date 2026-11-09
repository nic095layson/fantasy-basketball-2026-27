# After-report 2026-11-09: runner window 11-05 evening → 11-09 morning

**For:** the main session. **From:** the persistent runner (records branch season/daily).
**Owner's request (2026-11-09):** "Create after report to feed into Main for these additions and improvements."
**Window:** 2026-11-05 23:54Z (end of the addendum to `after-report-2026-11-05-runner-window.md`) → 2026-11-09 13:13Z (morning commit 85c8f06). Seven scheduled runs: mornings 11-06, 11-07, 11-08, 11-09; afternoons 11-06, 11-07, 11-08.

**Analyzed:** the seven run reports in `report/briefs/`; `brief_2026-11-0{3..9}.json`; `deck_record_2026-11-0{6,7,8}_pm.json` and `deck_record_2026-11-09.json`; `report/previews/week_0{3,4}.md`; `report/briefs/week_matchup_2026-11-09.json`; `data/decisions/{moves,recommendations,session}.jsonl`; `data/weeks/`; and the code lines cited below at season/daily 85c8f06 (= main 8f252a2 for `scripts/`).
**Method:** records only. Nothing re-run, nothing changed. EVIDENCE = a file, line or log shows it; INFERENCE = derived. One instrument was checked against a known answer before use (Finding 3).

**Headline.**
- All seven runs completed. Flaim returned 12 of 12 rosters every time, with no retries, so the `YAHOO_TRANSIENT_ERROR` retry rule still has not run live.
- #241 and #243 hold in live runs (Finding 6).
- **One real break:** seat 3 renamed itself on Yahoo (Lauri’s Prime Rib → SNOWTIME WHITE WALKERS) and `league_table.py` failed on 11-09. The League tab has no standings/power table until it is fixed, and the deck still reported PASS.
- Four improvements, each small: the deck's PASS hides a missing input; a stale "not simulated" label; the decision log missing alternative-pair matches; and two week-4 numbers that disagree.

## 1. Findings

| # | Finding | Severity | Basis |
|---|---|---|---|
| 1 | `league_table.py` fails when a team renames itself | **Medium: tab empty, recurs on any rename** | EVIDENCE |
| 2 | SEASON DECK passes while a named input is absent; nothing on the page or in the PASS line says so | Low-medium: silent degrade | EVIDENCE |
| 3 | "Not in the pool, not simulated" is stale for players with auto rows; `absent_from_sim` does not detect unpooled players | Low: label + instrument | EVIDENCE + INFERENCE |
| 4 | Decision log matches a move only to a brief's top pair, not its listed alternatives | Low: grading attribution | EVIDENCE |
| 5 | Week-4 preview (41.0%, 4.22 cats) and the 11-09 week projection (5-4, Σp ≈ 5.53) disagree; the preview has no structural band | Medium: two model figures point opposite ways | EVIDENCE (numbers) + INFERENCE (cause) |
| 6 | Verified live: #241, #243, and the week-3 intake | Info | EVIDENCE |
| 7 | Runner process miss 11-07 pm: two roster calls sent together | Info: runner-side, no build | EVIDENCE |

### Finding 1: team rename breaks the league table (EVIDENCE)

- 11-09 morning, step "league table": `LEAGUE TABLE: FAIL — Yahoo team 'Lauri’s Prime Rib' is not in the league state` (`report/briefs/morning_2026-11-09.json`, step tail; exit 1). Non-fatal; no `report/league/league_2026-11-09.json` was written.
- Cause, in code: `scripts/league_table.py:139` (`week_from_yahoo`) looks up each Yahoo matchup block's `teamName` via `_seats(state)` (`:108-109`, keyed by folded name) and raises at `:141` on a miss. Earlier pinned pulls still carry the old name.
- The same file already follows the owner's 2026-10-29 pick "Key on Yahoo team key" for week files: `:291-293` matches `week_N.json` scores by seat. `week_from_yahoo` was not brought under that rule.
- Other steps handled the rename. LEAGUE LIVE, WEEK MATCHUP and the brief all name SNOWTIME WHITE WALKERS as seat 3. `league_moves_2026-11-09.json` lists its moves under the new name.
- Records now split the name: in `data/weeks/team_weeks.csv` seat 3 is "Lauri’s Prime Rib" for weeks 1-2 and "SNOWTIME WHITE WALKERS" for week 3; `week_1.json` and `week_2.json` carry the old name. Nothing was edited.
- **Known answer for a fix:** with the 11-09 state and pulls, `league_table.py --date 2026-11-09` should PASS and list seat 3 once, under SNOWTIME WHITE WALKERS, with its weeks 1-3 record (Yahoo standings 11-09: 20-7-0).

### Finding 2: the deck passes with an input missing (EVIDENCE)

- `deck_record_2026-11-09.json → inputs.league = {path: report/league/league_2026-11-09.json, present: false, sha256: null}`. The embedded deck data has `league_table: null`.
- The SEASON DECK line still reads PASS with "7 tabs, 0 page errors", and nothing marks the League tab as missing its table.
- `season_deck.py:392-395` records absent inputs on purpose. The comment there says an optional input is "recorded as absent, not hashed", per GAUNTLET decision 4. So the behaviour is designed; the gap is that it is silent.
- INFERENCE: a reader of the 11-09 deck sees an empty League tab with no reason given.

### Finding 3: stale "not simulated" label; a field that cannot detect it (EVIDENCE + INFERENCE)

- EVIDENCE: since #240, `season_lines.py` writes an auto row for each rostered player with 3+ games. On 11-09: Meleek Thomas, Nolan Traore, Morez Johnson Jr., Mario Hezonja, Danny Wolf.
  - Each appears in `data/season/pool_season.csv`. Example: line 340, Meleek Thomas, note "auto: rostered, no pool row; 7-game box line…".
  - The brief runs on that file: `morning.py:18` `SEASON_POOL=data/season/pool_season.csv scripts/daily_brief.py`.
- EVIDENCE: the same five are still printed as "Not in the pool, not simulated" in three places:
  - the LEAGUE LIVE line (`league_live.py:301`);
  - the brief (`daily_brief.py:167`);
  - the deck note (`season_deck.py:812`).
  
  LEAGUE LIVE runs before season lines, so its list is computed before the auto rows exist.
- INFERENCE: the simulator counts these players, because it reads `pool_season.csv` after the auto rows are written. Whether `run_league_sim` filters them was not traced.
- **Instrument check (known answer):** `brief_*.json → absent_from_sim` was `[]` on 11-03, 11-04 and 11-05, when 2, 3 and 4 rostered players had no pool row at all. So that field does not report unpooled players, and it cannot be used to settle this question. Gap: NOT-ATTEMPTED (what the field does count was not read).

### Finding 4: the decision log misses alternative pairs (EVIDENCE)

- The owner's 11-08 move: +Cameron Johnson, −Ziaire Williams (`moves.jsonl` M-2026-11-08-01).
- That pair is listed word for word as alternative 2 of R-2026-11-07-01 and of R-2026-11-06-01 (`recommendations.jsonl` rows 18-19, `alternatives[1]`).
- The log recorded it as `add_match_drop_differs` against S-2026-10-30-01, a 10-30 session row whose drop was Collin Gillespie.
- Cause: `decision_log.py:126-136` (`join`) compares the move's add with each row's top `add` only. The 11-06 and 11-07 rows' top add was Tobias Harris, so they were skipped. `decision_grade.py:121` then grades the move against the 10-30 row.
- M-2026-10-31-01 has the same pattern. Whether that one was also an alternative was not checked (NOT-ATTEMPTED).

### Finding 5: two week-4 figures disagree (EVIDENCE numbers, INFERENCE cause)

- EVIDENCE: Sunday's preview `report/previews/week_04.md` (rosters 11-08) says "P(win the week): 41.0% (… ±0.7 points). Expected categories: 4.22 of 9". It notes "Q/O statuses not applied to the weekly model" and gives no structural band.
- EVIDENCE: Monday's `week_matchup_2026-11-09.json` projects 5-4-0. Its nine category p_win values sum to 5.53 (by hand from the file: FG% .466, FT% .866, 3PTM .861, PTS .874, REB .403, AST .433, ST .725, BLK .521, TO .380). PTS alone is 0.874 here against 23% in the preview.
- INFERENCE, not diagnosed: possible causes include
  - between the two runs, seat 3 moved Dončić and Markkanen to IL (`league_moves_2026-11-09.json`);
  - the preview ignores Q/O status;
  - the two use different models.

  Which of these drives the gap was not checked (NOT-ATTEMPTED).
- Calibration context (EVIDENCE): the week-3 preview said 84.7% and the week was won 7-2. The week-3 intake scored 7 mornings and 63 forecasts at Brier 0.124 against 0.155 for "leader to date" (SCOREBOARD INTAKE line, 11-09).

### Finding 6: verified live (EVIDENCE)

- **#241:** `deck_record_2026-11-0{6,7,8}_pm.json → out` names `deck_<date>_pm.html` (3 of 3).
- **#243:** the three afternoon SEASON DECK lines (11-06, 11-07, 11-08) end "lineup side refreshed (week_matchup_<date>_pm.json)" (3 of 3).
- **Monday steps on 11-09:** SEASON SWEEP PASS (6,000 seasons × 2 seeds, MC SE 0.54, baseline within 3 SE). SCOREBOARD INTAKE PASS for week 3; the fit says "too few weeks to propose (3 of 4)".
- **Retry rule:** all 7 run reports say "no retries" (4 × "No errors, no retries", 3 × "…returned data, no retries"). It is still untested live.

### Finding 7: runner process miss (EVIDENCE)

- 11-07 afternoon: the roster calls for teams 11 and 12 went out in one message, against the stored "ONE AT A TIME" rule. Both returned data.
- This was disclosed in `afternoon_report_2026-11-07.md`. Every later run sent them one at a time. Nothing to build.

## 2. Bounds

**Out of scope by design**
- Any fix, re-run or data edit (read-only report).
- Title-odds movement this window (11.6% ± 0.4 → 16.3% ± 0.5 → 18.1% ± 0.5) beyond quoting it.
- Main's own after-reports of 11-06.

**In scope and unverified**
- Finding 3: whether `run_league_sim` includes auto-row players, and what `absent_from_sim` actually counts. NOT-ATTEMPTED.
- Finding 4: whether M-2026-10-31-01 was also an alternative-pair match. NOT-ATTEMPTED.
- Finding 5: the cause of the preview/projection gap. NOT-ATTEMPTED. This is load-bearing only for how urgent decision D is, not for whether to look.

## 3. Decisions for the owner (main builds only on the owner's go)

**A. Team rename (Finding 1)**
1. **Extend the 2026-10-29 "Key on Yahoo team key" rule to `week_from_yahoo`: match on team key/seat, not name, with a test that uses this rename (Recommended).** No data rewrite.
2. A one-time name alias for weeks 1-2. This is a data change, and the next rename breaks it again.
3. Leave it. The League tab stays without its table.

**B. Silent missing inputs and the stale label (Findings 2-3)**
1. **Both, one PR: (a) SEASON DECK names any absent input in its PASS line, and the affected tab says why it is empty; (b) the "not simulated" label drops players that have an auto row (or reads "auto row, blended"). Plus a note on what `absent_from_sim` really reports (Recommended).**
2. Only (a).
3. Leave as is.

**C. Decision-log matching (Finding 4)**
1. **Match a move against each row's alternatives as well as its top pair, and record which pair matched. Re-derive M-2026-11-08-01 in the PR's test as the known answer: it should match R-2026-11-07-01, alternative 2, exact (Recommended).**
2. Leave as is. Grading keeps attributing such moves to older rows.

**D. Week-4 figures disagree (Finding 5)**
1. **Ask main for a diagnosis first (an after-report, no build): which input or model difference drives 41% vs about 5.5 categories, and whether the preview should carry a structural band like the title odds do (Recommended).**
2. Add the structural band to the preview now; diagnose later.
3. Leave as is.

## 4. Provenance

- Persistent runner session (claude.ai/code/session_01BsJA4wttu98TKVNoh6HBz1), 2026-11-09, after morning commit 85c8f06.
- Re-verify:
  - `sed -n 105,145p scripts/league_table.py; sed -n 288,295p scripts/league_table.py`
  - `python3 -c "import json;print(json.load(open('report/season/deck_record_2026-11-09.json'))['inputs']['league'])"`
  - `python3 -c "import json;[print(d,json.load(open(f'report/briefs/brief_2026-11-{d}.json'))['absent_from_sim']) for d in ['03','04','05']]"`
  - `grep -n "Meleek Thomas" data/season/pool_season.csv`
  - `sed -n 126,140p scripts/decision_log.py; grep -n "M-2026-11-08-01" data/decisions/moves.jsonl`
  - `sed -n 3p report/previews/week_04.md`
- Earlier runner report: `after-report-2026-11-05-runner-window.md`.
