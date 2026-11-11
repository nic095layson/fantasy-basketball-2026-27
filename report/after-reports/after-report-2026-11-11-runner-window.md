# After-report: runner window 2026-11-09 PM to 2026-11-11 AM

**Request (David, 2026-11-11):** "Create afterreport for main session."

**Analyzed:** five scheduled runs by the persistent runner on season/daily. Each run, with its report, its commit and the code it ran on:

| Run | Report | Commit | Kit code at run |
|---|---|---|---|
| 11-09 afternoon | `report/briefs/afternoon_report_2026-11-09.md` | 4b24a83 | 5807833 |
| 11-10 morning | `morning_report_2026-11-10.md` | 6da518c | (same as 11-09 PM) |
| 11-10 afternoon | `afternoon_report_2026-11-10.md` | 6223c50 | d15f6e7, main through #254 |
| 11-11 morning | `morning_report_2026-11-11.md` | c051fac | d70be1e, main through #256 |
| 11-11 owner edit | the morning scheduled task's prompt (retry rule) | — | 17:46Z |

**Method:**
- I read the runner's own logs (scratchpad `morning_1110.log`, `pm_1110.log`, `morning_1111.log`, `ml_1111.log`) and the committed records.
- I re-ran read-only checks at the dates given: curl of the Basketball-Reference and ESPN pages, `data/league_state.json`, and `git show origin/main:scripts/title_watch.py`.
- No engine code was run beyond the scheduled steps. Nothing was edited except the scheduled task's prompt, at David's request.

**Headline:** the window's one real failure was 11-11's morning.
- The box-score step is all-or-nothing. Two Basketball-Reference pages for 11-10 were missing, even though ESPN had all six finals. That skipped 18 steps and left the day without a brief or deck.
- **Since resolved:** another session re-ran the day at 16:25Z (8473ce7, "box scores 11-10 and the 18 skipped steps PASS", deck v73), and `report/briefs/morning_2026-11-11.json` now reads PASS. The manager log for 11-10 was filled in separately (53ec31a, owner pick "Cancel it, I fill the gap"). The runner's 17:00Z re-check task no longer exists (`get_trigger` returned not found at about 17:50Z); INFERENCE: that session cancelled it.
- David added a standing retry rule. It relies on `--resume`, which is on main. Whether the box-score step should accept a single outlet when one is late is a design question for main (decision D1).
- Everything else either worked or main has already handled it:
  - The A1 league-table fix holds.
  - The B1 label wording is live.
  - The 11-10 title drop was traced by main's `title_watch`.

## Findings

### F1. The box-score step fails a whole day when one outlet is late (11-11)

- EVIDENCE, `morning_1111.log` line 4: `FAIL · box scores 2026-11-10 · Basketball-Reference /boxscores/202611100NYK.html HTTP 404 … | … /boxscores/202611100PHI.html HTTP 404`. The run then went to `MORNING: FAIL`, with 18 steps skipped.
- EVIDENCE: ESPN's scoreboard (curl 13:07Z, `scratchpad/espn_sb_1110.json`) listed 6 games for 20261110, all `STATUS_FINAL`.
- EVIDENCE: the same two Basketball-Reference pages returned 404 at 13:07Z and again at 15:08Z. At 17:47Z all six pages for the date returned 200. Those are the NYK and PHI pages plus PHO, UTA, SAC and POR, which I had not checked before.
- EVIDENCE, `box_pull.py --help`: it fails when a fetch failed or an event has no box score, "in which case nothing is written".
  - A `--no-bref` flag exists, and the docstring labels a date as `single_source` only when one outlet *has no games* (preseason).
  - So a late second outlet is treated the same as a broken primary.
- INFERENCE: the two early Eastern games (7:30 and 8 PM ET) were posted later than the four Western ones. A 13:05Z morning run is about 10 hours after those finals. I did not check Basketball-Reference's posting times.
- Cost: no brief, waiver pairs or title line for 11-11 until a re-run. The manager log HALTed on the missing `data/actuals/2026-11-10.json`, and 11-10 tag outcomes were skipped.

### F2. The retry rule is in the morning prompt; it relies on `--resume` on main

- EVIDENCE: `update_trigger` at 17:46:02Z. The prompt now carries David's bullet word for word after "If a fatal step FAILS…". The schedule is unchanged, with the next run at 2026-11-12T13:01:54Z.
- EVIDENCE: `git show origin/main:scripts/morning.py` has `--resume` at line 281. The runner's checkout at 15:08Z (d70be1e) did not, because main merged it later.
- INFERENCE: tomorrow's run merges main at step 2, so `--resume` will be present. A plain `--since` re-run would also keep the day's moves record, because league_live's `am_baseline` diffs against the previous day's morning state (`league_live.py:320-328`, lookback starts at 1).
- One overlap to note: the runner's 11-11 morning report (c051fac) and the session's re-run both touch `morning_report_2026-11-11.md` (the re-run added an addendum, 6f40cf6). With the retry rule, the runner and a human-started session could both re-run the same day. The rule's "already PASS on origin, do nothing" guard is what prevents a double run; it has not been exercised live.
- Not yet exercised live: the rule's "fetch origin/season/daily and stop if the day's record already says PASS" guard.

### F3. The 11-10 title drop (18.1% to 12.3%) was traced by main

- EVIDENCE: `brief_2026-11-10.md` has "Title: 12.3% ± 0.5" and playoffs 96.4%, against 18.1% and 99.3% in the 11-09 brief. The runner flagged it as untraced (INFERENCE then: "Caruso move and league moves are candidates").
- EVIDENCE, the `origin/main:scripts/title_watch.py` docstring: "the reasons (a kit merge that put auto-row players in the simulator, a pool change and one IL return on another team) had to be traced by hand". The new step now names what changed between two briefs.
- So the runner's candidate causes were wrong: the main driver was the kit merge, not David's move. Nothing open, except that title_watch has not yet run in a morning (it was skipped on 11-11).

### F4. Two publishers write the same deck page

- EVIDENCE, from the publish results:
  - On 11-09 the runner read 1794258525-8eac (deck data generated 21:08Z), not its own v67, and overwrote it with v69.
  - On 11-10 it read 1794338269-dc9b (generated 19:17Z), not its own v70, and overwrote it with v72.
- INFERENCE: both newer versions are main's rebuilds after merges (2686e73 on 11-09; the #250 to #254 merges on 11-10). I did not check who published them.
- Risk: the afternoon run's page replaces main's mid-day rebuild. That is harmless while both build from the same merged code, but a runner page built *before* a merge could replace a newer main page. The afternoon runs merge main first, so it has not happened yet.

### F5. Decision card has not appeared in a live deck yet

- EVIDENCE: the 11-10 PM deck reported `absent: decision_card`. `report/briefs/decision_card_2026-11-10.json` did not exist, because #252 merged at 22:34Z, after that morning's 13:11Z run.
- On 11-11 the decision-card step was skipped (F1), so the card has still never appeared in a published deck.

### F6. The pool still has Nique Clifford on SAC

- EVIDENCE: `data/league_state.json` `nba_team_disagreements` (read 17:47Z) is `[{'player': 'Nique Clifford', 'yahoo': 'OKC', 'pool': 'SAC'}]`.
- The ESPN transactions feed recorded the SAC-to-OKC trade on 2026-11-08 (11-10 brief, transactions hit).
- He is rostered (Looking Cool Joker!), so the simulator schedules him on SAC's games. INFERENCE: this skews his games-left and team context; the size was not measured.

### F7. Smaller items

- **Unreadable Yahoo transaction:** on 11-11 Flaim returned 99 of 100 transactions. Its warning was "1 entry Flaim could not interpret" (`omitted_unrecognized_rows: 1`). Which move it was is UNVERIFIABLE from the response: Flaim drops it before returning.
- **Manager log on a HALT day:** on 11-11 manager_log HALTed but still updated `data/managers/profile.json` and `transactions.json` (6 new moves). That is consistent with its line ("day not logged … 6 new move(s), 146 on record"), but a HALT that writes files is worth a glance.

### F8. Verified working this window

| Item | Evidence |
|---|---|
| A1 league table on team keys | 11-10 morning `LEAGUE TABLE: PASS … Yahoo W-L-T matches the kit's finished weeks for 12 teams` |
| B1 label | LEAGUE LIVE now reads "not in the deck pool (simulated once the season lines give an auto row, 3+ games)" from 11-09 PM onward |
| Flaim one-at-a-time rule | 0 parallel roster calls and 0 retries across all 4 runs (each report says "no retries") (the 11-07 miss has not recurred) |
| Afternoon morning-record hashes | `sha256sum -c` passed for all four records on 11-09 and 11-10 |
| Afternoon deck "lineup side refreshed" | Present in both afternoon SEASON DECK lines |

## Bounds

**Out of scope by design:** the simulator's math; the FantasyBot outlook's projection (never quoted); trades.

**In scope and unverified:**
- Who published the two deck versions in F4: NOT-ATTEMPTED (the artifact service shows versions, not publishers, in what I read).
- Basketball-Reference's usual posting delay: NOT-ATTEMPTED.
- How much F6 skews Clifford's games-left and team context: NOT-ATTEMPTED.
- Which Yahoo row Flaim dropped (F7): UNVERIFIABLE, as stated.

I cannot see main's own session history; what main did is read only from commits and docstrings.

## Decisions for David

**D1. What should a late second outlet do to the morning?**
1. **Keep the strict two-outlet rule and rely on the new retry rule (Recommended).** Nothing to build; at most a re-run hours later, as today.
2. **Have main make box_pull accept ESPN alone when it has every final but Basketball-Reference 404s, labelled `single_source`, with a re-pull at the next run.** The morning would never be lost to a late page, but it is a method change for main to build and test.
3. **Move the morning trigger later.** Basketball-Reference is more likely to be posted, but the brief arrives later in your day.

**D2. Two deck publishers (F4)**
1. **Leave it; the afternoon run merges main before building (Recommended).** No change.
2. **Have main's rebuilds write a dated note the afternoon run checks before overwriting.** Safer, but it is one more step.

**D3. Clifford's pool team (F6)**
1. **Have main add a pool team-update path, or a rule like "Yahoo team wins when ESPN transactions confirm a trade" (Recommended).**
2. Leave it as a flagged disagreement.

## Provenance

- Produced by the persistent runner session (session model A) on 2026-11-11.
- Sources: the runner logs named above (scratchpad); the committed records at 4b24a83, 6da518c, 6223c50 and c051fac; `origin/main` at 9b0a37f plus the `--resume` and `title_watch.py` reads at 15:08Z and 17:47Z; curl of the ESPN and Basketball-Reference pages at 13:07Z, 15:08Z and 17:47Z.
- Re-verify:
  - `curl -s -o /dev/null -w "%{http_code}" https://www.basketball-reference.com/boxscores/202611100NYK.html`
  - `python3 scripts/morning.py --help | grep resume`
  - `python3 -c "import json;print(json.load(open('data/league_state.json'))['nba_team_disagreements'])"`

## Owner picks (2026-11-11, decision cards)

- **D1:** "Keep strict + retry (Recommended)". No build: the two-outlet rule stands, and the new retry rule covers a late outlet.
- **D2:** "Leave it (Recommended)". No build.
- **D3:** "Team-update path (Recommended)". Main adds a way to update a pooled player's NBA team when Yahoo and ESPN's transactions feed agree on a trade, with a test on Nique Clifford (SAC to OKC, 2026-11-08).
