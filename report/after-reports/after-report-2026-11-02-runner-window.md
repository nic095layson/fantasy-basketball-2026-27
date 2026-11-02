# After-report — runner window 2026-10-31 → 2026-11-02 (5 runs)

**Request (owner, 2026-11-02):** "Please create comprehensive after report and next steps for Main session."

**What was covered:**
- Five runner runs on season/daily: morning 10-31 (44841fe), afternoon 10-31 (4d5ac5f), morning 11-01 (d9d84c6), afternoon 11-01 (05a024c) and morning 11-02 (f6db119).
- The main-session merge that landed in between: #232, IL-return title odds (9208733, 67d1532; merge 8ce0a75).
- The window starts where the last after-report (`after-report-2026-10-29-morning-run.md`) ended.

**Method:**
- Read-only, from committed files, the runner's step logs (`morning_1031.log`, `morning_1101.log`, `morning_1102.log` in the runner's scratchpad) and the pinned Flaim pulls.
- Two code paths were traced to a line.
- One rerun of `accuracy_week.run(2)` with every output redirected to scratch, to separate a code fault from a data fault. Its outputs were deleted, and `git status` was clean after it.
- `python3 -m unittest scripts.test_constants_registry scripts.test_redteam_sweep` was run: 30 tests, OK.
- No simulator run, no engine or data change. Every EVIDENCE line was re-read on 2026-11-02, ~14:00–14:30Z.

**Headline:**

| # | Finding | Severity | Status |
|---|---|---|---|
| 1 | **The Monday season sweep crashes** on two IL-return registry entries that are `declared_band` with no `band`. The structural band in the brief stays frozen at 10-26. | High: the brief's uncertainty band stops refreshing | EVIDENCE, root-caused |
| 2 | **The week-2 accuracy card crashed, and the crash emptied `report/accuracy.md`** (998 → 0 bytes, committed in f6db119). `render()` indexes `candidate_minutes` on week 1's row, which predates that key. | High: a record file was destroyed | EVIDENCE, root-caused |
| 3 | **The IL-return section is printed without its FRAGILE room-rule band** (+13.4 title points). Main's own report quotes that band. | Medium: a red-team quoting rule is missed in the brief | EVIDENCE |
| 4 | **The waiver scan re-proposes a player you just dropped who is still on waivers, three days running.** | Medium: an advice-quality defect, recurring | EVIDENCE |
| 5 | **Commit trailers carry model names** in breach of the repository's CLAUDE.md rule 6: 41 runner commits and 6 main-session commits since 10-28. | Process | EVIDENCE |
| 6 | Minor items: Yahoo's "/" makes/attempts on a week's first morning; a start lost on 11-01; team 4's rename handled cleanly. | Low | EVIDENCE |

## 1. Season sweep crash (Monday 11-02)

**EVIDENCE:**
- `report/briefs/morning_2026-11-02.json`, step "season sweep": exit 1, tail `ValueError: il_return.SLIPS is declared_band with no band`.
- `scripts/redteam/sweep.py:55-59`: every `declared_band` constant must carry `band`, or the sweep raises.
- `scripts/redteam/constants_registry.json`: of the 7 `declared_band` entries, 5 carry `band`. The two that don't are:
  - `il_return.SLIPS`, record text "the grid is its own band: the section shows every row";
  - `il_return.ROOM_RULE_ON`, record text "FRAGILE, +13.4 title points with the rule off".
- `python3 scripts/redteam/check_constants.py` → `CONSTANTS CHECK: PASS — 45 registered = 45 live … declared_band 7`. The checker requires a record for `declared_band` but not a `band`.
- So the two validators disagree, and the registry passes the one that ran at merge time.
- `scripts/test_redteam_sweep.py:37` (`test_declared_band_without_band_is_an_error`) pins the sweep's behaviour. No test runs the sweep on the live registry.

**Effect:**
- No sweep was written for 11-02.
- The brief's structural band ("season sweep of 2026-10-26 … deck cbfb422") is now 7 days old and will not refresh on any Monday until this is fixed.
- Even if only `SLIPS` were fixed, the sweep would fail next on `ROOM_RULE_ON`. Both lack `band`. (INFERENCE: the loop raises on the first entry it meets.)

**Fix shape (proposal; the main session decides):**
- Either give both entries a `band` the sweep can patch:
  - `ROOM_RULE_ON`: `[{"label": "rule off", "ROOM_RULE_ON": false}]`;
  - `SLIPS`: is a grid, not a point value, so it may belong under a different status.
- Or teach `check_constants.py` the sweep's rule, so the two agree, and register `SLIPS` as `structural` or `settings`.
- Add a test that loads the live registry through `variants_from_registry`.

## 2. Accuracy card crash emptied `report/accuracy.md`

**EVIDENCE:**
- SCOREBOARD INTAKE (11-02) printed `accuracy FAIL — 'candidate_minutes'`. The intake itself passed.
- `report/accuracy.json`: week 1 row keys `['preseason', 'in_season']`; week 2 row keys `['preseason', 'in_season', 'candidate_minutes']`. Week 2 *was* appended.
- `scripts/accuracy_week.py:196-197` opens `report/accuracy.md` with mode `"w"` **before** calling `render(rec)`.
- `:213` in `render` indexes `r[x]` for `x` in `("preseason", "in_season", "candidate_minutes")`, which raises `KeyError` on week 1.
- `wc -c report/accuracy.md` → 0. `git show d9d84c6:report/accuracy.md | wc -c` → 998. The empty file is in f6db119; the runner committed it as part of the run's output, per its prompt.
- Scratch rerun with a fresh output file (week 2 only): `summary` returned "week 2: 252 players, points 13.14 projected / 11.88 actual; 0 league matchup(s) scored". So the fault is the mixed-schema history, not week 2's data.

**Effect:**
- The human-readable accuracy table is gone from the branch tip; history keeps it at d9d84c6.
- `accuracy.json` is intact.
- Every later week will crash the same way until `render` tolerates week 1's row.

**Fix shape (proposal):**
- `r.get(x)` with a "no snapshot" cell (the `cell` helper already handles a falsy value).
- Render to a string first, then write.
- A test with a week-1-shaped row.
- Regenerate `accuracy.md` from `accuracy.json`.

**Also seen, not root-caused:** the same summary says "0 league matchup(s) scored". Whether the league-matchup ledger should have had week 2 rows: did not check.

## 3. IL-return section shown without its FRAGILE band

**EVIDENCE:**
- `after-report-2026-10-31-il-return.md` §3 and §5: "ROOM_RULE_ON is FRAGILE: +13.4 (rule off)", listed under "Bands quoted" as "The section's own".
- `report/briefs/brief_2026-11-02.md`, section "If IL players return": "on time 30.1% · +2 wk 30.5% · +4 wk 30.1% · never = headline 13.6%. Error ± 0.47 each … Room rule: lowest adj_value active player leaves from the return week."
- It names the rule but not its +13.4 band or the word FRAGILE.

**INFERENCE:**
- The owner sees "≈ 30% if they return" with only the sampling error.
- The room rule alone can move that figure by more than the gap between "return" and "never" is wide on the other side.
- The red-team quoting rule (two error bars, FRAGILE constant named) is met in main's report but not on the surface the owner reads daily.

**Not checked:** whether the deck's Today-tab IL table shows the band (did not check).

**Also observed (assessment only):** across three days the slip rows stay within one error bar of each other:
- 10-31: 29.9 / 29.9 / 29.6;
- 11-02: 30.1 / 30.5 / 30.1.

This matches main's inference that "whether" matters and "when within a month" does not. A display with three near-equal rows may read as more precision than exists. The main session can judge whether one row plus the range says it better.

## 4. Waiver scan re-proposes your own fresh drops

**EVIDENCE** (pinned pulls `data/source/flaim/pull_<date>.json`, Yahoo transactions tr.102, tr.107):

| Day | Your move | Scan's top pair that morning | That player's Yahoo state |
|---|---|---|---|
| 10-31 | +Cameron Johnson −Julian Champagnie | add Champagnie, drop Queta | waivers, waiverDate 2026-11-01 |
| 11-01 | +Champagnie −Bobby Portis | add Portis, drop Cameron Johnson | waivers, waiverDate 2026-11-03 |
| 11-02 | (no move) | add Portis, drop Cameron Johnson | waivers, waiverDate 2026-11-03 |

- The streaming list's first name on 11-01 (Kris Dunn) was also on waivers (waiverDate 2026-11-02).
- The pull already carries `ownershipType` and `waiverDate` for every available player; the brief prints neither.
- The decision log records each pair as a recommendation (R-2026-10-31-01, R-2026-11-01-01, R-2026-11-02-01). The 11-01 move is graded `add_match_drop_differs` against the 10-31 pick.
- **INFERENCE:** the scorecard will grade advice that was unactionable on the day it was given.

## 5. Model names in commit trailers

**EVIDENCE:**
- Repository CLAUDE.md, rule 6: "Commits … name a model by a neutral label ('session model A') … Existing history is not rewritten."
- `git log origin/season/daily --since=2026-10-28` trailers: 41 `Co-Authored-By: Claude Opus 5.5`, 6 `Co-Authored-By: Claude Fable 5.1`.

**Cause:**
- The runner followed the platform's attribution reminder over CLAUDE.md. The reminder itself says the user's own instructions take precedence. My error.
- From this report's commit on, the runner uses a neutral label in the trailer.

**Open to the owner:** confirm the label (proposal below). History stays as is per rule 6.

## 6. Minor items

- **Yahoo "/" on a new week's first morning.**
  - WEEK MATCHUP 11-02: "to date rebuilt (Yahoo's week 3 totals could not be read: unreadable makes/attempts value '/')".
  - The step passed on the rebuild, which had 0 days.
  - INFERENCE: this recurs every Monday morning. Treating "/" as 0/0 before the first game would keep the line quiet.
- **A start lost on 11-01:**
  - `data/managers/day_2026-11-01.json`, seat 10: `starts 2, best_starts 3, starts_lost 1, benched_played ['Yaxel Lendeborg']`.
  - The 11-01 brief's lineup had Lendeborg at PF; Yahoo's locked lineup had him on BN.
  - Scottie’s Thotties lost 2 the same day.
- **Team-4 rename** ("Splash Mountain" → "Scottie’s Thotties", 11-01): LEAGUE PAIRINGS and LEAGUE TABLE both PASS. The 95cf5a3 team-key fix works in production.
- **Week 2 result:** 7-2-0 vs Looking Cool Joker!. Record 10-8, seed 4 (Yahoo standings 11-02).
  - Forecast: 7 mornings / 63 forecasts, Brier 0.145 vs lead-to-date 0.294.
  - Constants fit: shock 0.0973 ± 0.0134 vs live 0.06. "Too few weeks to propose (2 of 4)".

## 7. Run results (EVIDENCE: step logs and run reports)

| Run | Verdict | Deck | Pushed | Notes |
|---|---|---|---|---|
| 10-31 am | PASS, 17 steps | v46 | 44841fe | Finding 4 first seen |
| 10-31 pm | all PASS | v47 | 4d5ac5f | morning hashes unchanged |
| 11-01 am | PASS, 18 steps (+ WEEKLY PREVIEW week 3) | v48 | d9d84c6 | rename handled |
| 11-01 pm | all PASS | v49 | 05a024c | Kyrie newly Q |
| 11-02 am | PASS, 20 steps; season sweep FAIL (non-fatal) | v50 | f6db119 | Findings 1, 2, 3 |

- Flaim returned every call on first try across all five runs: no YAHOO_AUTH_UNAVAILABLE and no retryable error. The v5 retry rule has still not been exercised.
- The publish byte check passed on every run.
- PR #165 stays open as a draft, untouched.

## Bounds

**Out of scope by design:**
- Any code, registry, data or engine change.
- Re-running the sweep or the IL-return simulator.
- Regenerating `accuracy.md`.

**In scope and unverified:**
- Whether the deck's IL table shows the room-rule band: NOT-ATTEMPTED.
- Why the week-2 summary scored 0 league matchups: NOT-ATTEMPTED.
- Whether any other `declared_band` consumer besides the sweep assumes `band`: NOT-ATTEMPTED (only `sweep.py` and `check_constants.py` were read).
- That the sweep fails next on `ROOM_RULE_ON` once `SLIPS` is fixed: INFERENCE from the loop, not run.

## Next steps for the main session (owner decides each)

**A. Season sweep (Finding 1)**
1. **Give `SLIPS` and `ROOM_RULE_ON` sweep-readable bands, or re-register `SLIPS` under a non-band status; make `check_constants.py` require `band` for `declared_band`; add a live-registry sweep test; re-run the 11-02 sweep (Recommended).**
2. Skip IL-return constants in the sweep until their bands are written.
3. Leave it; the Monday step fails non-fatally and the band stays at 10-26.

**B. Accuracy card (Finding 2)**
1. **Make `render` tolerate missing snapshot keys, write only after a successful render, add the test, and regenerate `report/accuracy.md` from `accuracy.json` (Recommended).**
2. Backfill week 1's row with an explicit "no snapshot" `candidate_minutes` entry (rewrites an append-only record; not recommended).

**C. IL-return display (Finding 3)**
1. **Print the room-rule band beside the section in the brief and deck: "ROOM_RULE_ON FRAGILE +13.4 (rule off)" (Recommended).**
2. Collapse the three near-equal rows to one "if they return" row plus the band.
3. Leave as is.

**D. Waiver scan (Finding 4)**
1. **Mark `waivers` players with Yahoo's `waiverDate` in the scan, the streaming list and the decision log (Recommended).**
2. Also hold back a pair that re-adds a player the owner dropped in the last 2 days.
3. Leave it; the runner flags it daily.

**E. Commit trailers (Finding 5)**
1. **Neutral label "Claude (session model A)" in all trailers from now on; the label-to-model map stays outside the repository (Recommended).**
2. A different label the owner names.

**F. Small items (bundle with any of the above)**
- Treat Yahoo's "/" as 0/0 before a week's first game.
- Add `league_sim.py` to the engine fingerprint (carried from main's IL-return report).

## Provenance

- Runner session `session_01BsJA4wttu98TKVNoh6HBz1`, 2026-11-02.
- Sources:
  - `report/briefs/morning_2026-11-0{1,2}.json`
  - `report/briefs/brief_2026-11-02.md`
  - `report/briefs/morning_report_2026-1{0-31,1-01,1-02}.md`
  - `scripts/redteam/sweep.py:55-59`
  - `scripts/redteam/constants_registry.json` (il_return entries)
  - `scripts/redteam/check_constants.py`
  - `scripts/accuracy_week.py:196-213`
  - `report/accuracy.json`
  - `data/managers/day_2026-11-01.json`
  - `data/source/flaim/pull_2026-1{0-31,1-01,1-02}.json`
  - `report/after-reports/after-report-2026-10-31-il-return.md`
- Re-verify:
  - `wc -c report/accuracy.md` (expect 0 until fixed)
  - `python3 scripts/redteam/sweep.py --season data/league_state.json data/season/pool_season.csv --real-schedule data/league_schedule.json --out /tmp/x/sweep.json` (expect the ValueError until fixed)
  - `python3 -c "import json;print([(e['name'],'band' in e) for e in json.load(open('scripts/redteam/constants_registry.json'))['constants'] if e['status']=='declared_band'])"`
