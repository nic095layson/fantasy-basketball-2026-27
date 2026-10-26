# Runner prompt edits for the run-records fix — before/after, 2026-10-26

Companion to `after-report-2026-10-26-run-records.md` (PR #193). Nothing here is applied: the owner applies each
edit with `update_trigger` on an explicit go, and nothing else in either prompt changes. Scheduled tasks:
morning `trig_01V43JtVvW6teWGmwt17dPVw` (step 6), afternoon `trig_015cHK6ECUvXA9TX1UNTT53r` (steps 3–5).
Text under BEFORE is quoted verbatim from the live prompts (list_triggers, 2026-10-26). Lines not shown are unchanged.

The afternoon edit depends on PR #193 being on `main` first: the afternoon runner merges `origin/main` into
`season/daily` before it runs, and `--phase` does not exist before that merge (the AFTER text says what to do if it
is missing, so applying early is safe, just ineffective until the merge).

---

## Morning prompt — step 6

### BEFORE

```
6. Save the records. Skip the commit and push only if step 1b left you without a push credential, and quote the refusal.
   - Write the step-7 report, without its commit and PR lines, to report/briefs/morning_report_<date>.md.
   - Commit everything the run wrote as "Morning run <date>: <one line from the MORNING line>". That covers data/actuals, data/season, data/status, data/news, data/source/fantasybot, data/source/flaim, data/managers, data/weeks, data/league_state.json, report/season, report/briefs, and report/run-ledger.jsonl.
   - Push with `git push -u origin season/daily`, retrying up to 3 times (2s, 4s, 8s) on network errors only. If it still fails, quote the exact git error.
```

### AFTER

```
6. Save the records. Skip the commit and push only if step 1b left you without a push credential, and quote the refusal.
   - Write the step-7 report, without its commit and PR lines, to report/briefs/morning_report_<date>.md.
   - Commit what the run wrote as "Morning run <date>: <one line from the MORNING line>": every path in morning.py's WROTE block (the lines printed after `WROTE: n path(s)`; report/briefs/morning_<date>.json records the same list under "wrote"), plus report/briefs/morning_report_<date>.md, plus anything else `git status --porcelain --untracked-files=all` lists under data/ or report/ (the step-4 scripts that run outside morning.py — availability_calibration, manager_log, scoreboard_intake — write there too). The WROTE block is measured from the tree, so a path it names that no list in this prompt mentions is still the run's: commit it. If the block reads `WROTE: unattributed (not a git checkout)`, commit everything under data/ and report/ and say so in the report.
   - Then run `python3 scripts/commit_check.py` and keep its one COMMIT CHECK line. On FAIL, commit the paths it names as "Morning run <date> (part 2): <the paths>" and run it again; a second FAIL goes in the report with the paths. Never stash or discard a path it names.
   - Push with `git push -u origin season/daily`, retrying up to 3 times (2s, 4s, 8s) on network errors only. If it still fails, quote the exact git error.
```

Only the "Commit everything" bullet is replaced and one bullet is added after it; the first, second and last bullets
and everything after them in step 6 are unchanged.

Not changed, by the owner's instruction (step 7 is outside the edit): the step-7 report does not yet ask for the
COMMIT CHECK line. Listed in the after-report §4 as an option.

---

## Afternoon prompt — step 3

### BEFORE

```
3. In KIT, each non-fatal (report a HALT, fix nothing in the engine):
   - `python3 scripts/league_live.py --as-of <date> --since <T0>` (roster validation: refreshes data/league_state.json and writes data/news/league_moves_<date>.json; its PASS line names the source).
   - `python3 scripts/status_feed.py --date <date>` then `python3 scripts/status_feed.py --check data/status/status_<date>.json` (game status and injury designations).
```

### AFTER

```
3. In KIT, each non-fatal (report a HALT, fix nothing in the engine):
   - `python3 scripts/league_live.py --as-of <date> --since <T0> --phase pm` (roster validation: refreshes data/league_state.json and writes data/news/league_moves_<date>_pm.json, the moves since the morning's state; the morning's league_moves_<date>.json is the overnight record and this run never touches it. Its PASS line names the source and the phase). If `python3 scripts/league_live.py --help` does not list `--phase`, run it without `--phase` and say in the report that the afternoon record overwrote the morning's.
   - `python3 scripts/status_feed.py --date <date>` then `python3 scripts/status_feed.py --check data/status/status_<date>.json` (game status and injury designations).
```

## Afternoon prompt — step 4

### BEFORE

```
4. Save: write the step-5 report (without commit/PR lines) to report/briefs/afternoon_report_<date>.md; commit data/league_state.json, data/news, data/source/flaim, data/source/fantasybot, data/status and report/briefs as "Afternoon check <date>: <one line>"; `git push -u origin season/daily` (retry 3x on network errors only, else quote the error); confirm `git ls-remote origin refs/heads/season/daily` equals `git rev-parse HEAD`; make sure an open draft PR "Season: daily records" exists for season/daily into main (create it as the morning prompt's step 6 does if none is open); never merge.
```

### AFTER

```
4. Save: write the step-5 report (without commit/PR lines) to report/briefs/afternoon_report_<date>.md; commit everything `git status --porcelain --untracked-files=all` lists under data/ and report/ as "Afternoon check <date>: <one line>" (this run writes data/league_state.json, data/news, data/source/flaim, data/source/fantasybot, data/status, report/briefs and report/run-ledger.jsonl; a script may gain an output this list does not name — commit it too); then run `python3 scripts/commit_check.py` and keep its one COMMIT CHECK line — on FAIL, commit the paths it names as "Afternoon check <date> (part 2): <the paths>" and run it again, a second FAIL goes in the report with the paths, and never stash or discard a path it names; `git push -u origin season/daily` (retry 3x on network errors only, else quote the error); confirm `git ls-remote origin refs/heads/season/daily` equals `git rev-parse HEAD`; make sure an open draft PR "Season: daily records" exists for season/daily into main (create it as the morning prompt's step 6 does if none is open); never merge.
```

## Afternoon prompt — step 5

### BEFORE

```
5. Report to David briefly: T0; Flaim roster calls returned (n of 12) and whether FantasyBot was needed; the LEAGUE LIVE line (or halt line with names); league moves since the morning state (or "no record"); status changes on David's roster and his current opponent's roster since the morning status file (diff data/status/status_<date>.json against the morning commit's version), or "no change"; the STATUS GATE line; the pushed commit and PR link; anything that failed and any stash.
```

### AFTER

```
5. Report to David briefly: T0; Flaim roster calls returned (n of 12) and whether FantasyBot was needed; the LEAGUE LIVE line (or halt line with names); league moves since the morning state, read from data/news/league_moves_<date>_pm.json (or "no record"); status changes on David's roster and his current opponent's roster since the morning status file (diff data/status/status_<date>.json against the morning commit's version), or "no change"; the STATUS GATE line; the COMMIT CHECK line; the pushed commit and PR link; anything that failed and any stash.
```

---

## What the edits do not cover (open, for the owner)

- The morning step-7 report does not ask for the COMMIT CHECK line or the WROTE count (step 7 was outside the edit).
- The disabled "fresh session" morning and evening prompts still carry the old step 3/6 text; they do not fire.
- `scripts/commit_check.py` runs after the commit and before the push, so a FAIL is caught before anything leaves the
  container; it does not check that the push carried the commit — the existing `git ls-remote` confirmation does.
