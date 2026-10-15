# Co-GM self-audit, 2026-10-15 — what went wrong through draft preparation, why, and the plan to fix it

**Owner request (2026-10-15, verbatim):** "I'd like for you to self-audit yourself, critically, with all the learnings (such as not knowing bench clearly thinking they played a .%, rather than most games played in a week and switching players through positions, accidentally using Towns' wrong season stats, e.g.). What are all the lessons that you learned, and what are actionable steps for an agent to greatly improve the operation and efficacy / success of this tool moving forward? Use Fable to draft a comprehensive plan and resolution action steps - then I will refeed the prompt to Code to execute."

**What was analyzed.** The records, not recollection: the deck's `LESSONS.md` (23 numbered lessons, 2026-07-12 to 2026-09-30), the kit's 119 after-reports (2026-07-27 to 2026-10-14), the postmortems (`postmortem-2026-07-13-roster-audit.md`, deck `postmortem_2026-07-12_draft_sim.md`), the decision sheets still open at the draft (D-INT-1/2, D-LD-1/2, D82-1, D83-1, D-1013-2, D-1009-2), and the code comments that record each model change (`arena/arena.py`, `scripts/hoops.py`). Every incident below cites its record. Where a cause is my judgment rather than a record, it is marked INFERENCE.

**Method.** Three passes: (1) every incident on file, dated, with what caught it and what it cost; (2) the incidents grouped by root cause into lessons; (3) a work plan a fresh Code session can execute, each package with a red-first test, a gate, a report and the owner decision it needs. Section 6 is the prompt to re-feed.

**Headline.** The system's arithmetic was never the problem: both engines reproduce to 0.0, the page equals the Python at 481 of 481 owner turns, and the final league board matched Yahoo 156 of 156. The failures were upstream and sideways of the arithmetic — **data written from memory and labelled as fact** (July rosters, July stat lines that were 2024-25-shaped and said 2025-26), **league mechanics modelled from assumption rather than from the league's settings** (a 0.15 bench weight for a daily-lineup league; a 6-team bracket for an 8-team league), **prose and display logic that no audit tested** (the LEAN line, the shift line, RESYNC), and **process habits of mine** (deferring an urgent finding into a queue, building a candidate to answer a question, grading my own checklist, letting a 97.8% "confidence" stand for more than it measured). Eleven of the thirteen incidents in §1 were found by you or by a later session, not by a gate at the time. The plan's first principle follows from that: **every class of failure that happened gets a mechanical check that can fail**, and the agent's judgment is the last line, never the first.

---

## 1. The incidents, from the records

| # | date | what happened | how it was found | what it cost | record |
|---|---|---|---|---|---|
| I1 | 7/12 | 220 kit projections and the deck's lines were written from model memory, labelled "2025-26 production"; sources were 403-blocked and the file said so. | Roster audit 7/13 (39 of 220 team values stale); the stat-line vintage not until 10/12. | Every mock before 10/12 (51–75) was drafted and graded on lines that were mostly 2024-25-shaped; Towns ranked first at #10 on a line that was his 2024-25 season. | `data/RESEARCH.md` @ `dc18de2`; `postmortem-2026-07-13-roster-audit.md`; `after-report-2026-10-13-usage.md` §2 |
| I2 | 7/12–8/05 | The weekly model weighted 10 starters × 1.0 + 3 bench × **0.15** ("BENCH_WEIGHT"). Yahoo lineups are set daily; bench players backfill any open slot on their game days. Measured: ~99.4% of a 13-man roster's played games start. The static model underweighted the bench ~6.5×. | Measurement in the daily-fill study (8/05–8/10); the orphaned build carrying it was found 8/13. | A mis-shaped star inflated against the card; mocks 51–54 graded on the old weighting. The pick engine's `lineup_weights`/`bench_bound` still use the static 0.15 (unverified whether that matters — §4 B5). | `arena/arena.py` lines 138–186; `LESSONS.md` 21 |
| I3 | 7/12–9/30 | The arena simulated a 6-team playoff with byes; the league plays 8 of 12, no byes. Found 8/04 from your screenshots, registered as E14, shipped 9/30. | Owner screenshots 8/04. | Every title share before 9/30 was for the wrong bracket (−4 to −6 pp on elite rosters); E14 sat registered eight weeks. | `league_intel_2025-26.md` §4; `LESSONS.md` 23 |
| I4 | 7/30 | Standings accumulated weekly binary wins instead of the category record; playoff% shifted up to ±29 pp on identical rosters. | The 9-cat math audit. | Pre-7/30 odds unreliable. | `arena/arena.py` comment at `simulate_seasons` |
| I5 | 8/09 | `verify_rosters.py` wrote `date.today()` and the gates checked that self-written date; a fabricated row (`Bronny James,ZZZ`) passed every gate. | Round-3 audit. | "Safe to publish" with zero research. | `LESSONS.md` 15 |
| I6 | 8/10 | The fix batch that closed 20 findings introduced 13, incl. RESYNC's backup holding the wiped board, and two-letter first names (CJ, PJ, AJ…) silently unmatched. | Round-4 audit. | — (caught before the draft) | `LESSONS.md` 19 |
| I7 | 8/13 | The live artifact served a build that existed in no repo; its JS disagreed with the Python at 20 card orderings while the page said "verified". | The 8/13 pull. | Three unlanded-work incidents in total. | `LESSONS.md` 10, 11, 21 |
| I8 | 10/08 → 10/12 | The range check found **131 of 145** top lines outside every outside reference. I queued it for Sunday's pass instead of raising it. Your Towns question four days later exposed the vintage (44 of 52 top-60 rows closer to 2024-25). | Owner question. | Four more days of practice on the wrong lines; the WO-5 re-derivation then changed the 🎯 at 12 of 13 turns of your practice room. | `after-report-2026-10-13-usage.md` §2; `-live-mock.md` |
| I9 | 10/09 | The availability discount reaches only positive totals and its zero sits at the pool mean: 19 of 29 risk-tagged rows in the top 200 carried **no discount**; the kit kept GP ≤ 25 rows on its board (Butler #68); 41 lines failed the points identity. | Category audit (mine). | D-1009-1 fixed; D-1009-2 still open; identity made a check. | `after-report-2026-10-09.md` §8 |
| I10 | 10/12–13 | Answering "is usage on the new team taken into account?" I built a 326-line replacement candidate in scratch within 9 minutes; the backtest window (2006-07 onward) was chosen by the data file's extent and never stated. The governors were not loaded; the house rule lived only in compaction summaries. | Owner objection. | A scope breach; a disputed result carried into the next context as a finding. | `after-report-2026-10-13-scope-fence.md` §4 |
| I11 | 10/13 | RESYNC wiped a 141-pick live board: the box expected a semicolon list, the paste was the page's own history, and RESYNC cleared the board before validating. | Owner, mid-draft. | A practice room lost; a console restore written. D-1013-2 chose the procedure (b), not the fix. | `after-report-2026-10-13-live-mock.md` |
| I12 | 10/14 | The ⚠ LEAN line counted position tokens, not players: your roster read "7G vs 2F" with four guards. The full integrity audit that same evening (34 of 35 green) did not catch it — it audited arithmetic, not sentences. | Owner screenshot. | Display only; fixed as Version 70. | `after-report-2026-10-14-lean.md`; `-integrity.md` |
| I13 | 10/14 | Live-room resolver and history defects: "Green" → Draymond when Jalen was taken (D82-1); the shift line says "X is the 🎯" when X is merely absent from the card (D83-1); undone entries re-render under the later occupant and a stale "no longer your pick" line (D-LD-1). The board was right every time; the words were not. | Grading replays in Chromium. | Confusion in the real draft (Keyonte George line). | `after-report-2026-10-14-draft82/83/league-draft.md` |

**Self-reporting incidents (the agent's, not the tool's).**
- 10/14 integrity report: my first pass read 91.7% because my own parser compared the wrong record; the 97.8% "projection confidence" measured agreement with the consensus the lines had been blended toward — near-tautological, as I said the same night; I graded my own checklist (`after-report-2026-10-14-integrity.md` §6; chat 10/14).
- Mock grades are circular: the grader (ECW on the house weekly model) is the same engine that produced the card, so "following the 🎯 grades higher" is self-agreement. Stated in every report's Bounds, never fixed.
- 10/15: the repeat-name gate's log came back empty and I nearly reported it as a pass; re-run with the exit code captured before merging (`scratchpad/league/gate3b.log`). Caught, but by habit, not by a gate.
- Version 61 (10/13) shipped with a colophon sentence that contradicted the build; caught and republished as 62.

---

## 2. The lessons, by root cause

### L1 — Data written from memory is the original sin; it was caught for teams and not for stat lines
EVIDENCE: I1, I8. The July files said their limit out loud ("knowledge-based, not scraped — spot-check when access allows"), and the gate built after the roster audit checked **team placements only**. The same failure in the per-game lines got no gate for 92 days. The first instrument that could see it (the 10/08 range check) saw it, and I queued the finding. **Lesson:** a limit written in a docstring is not a control; every data class an agent can author from memory (teams, positions, stat lines, minutes, games, injury status) needs its own provenance column and its own gate that fails on an unsourced row — and a finding that touches most of the top 150 within a week of the draft is an owner alert, not a queue item.

### L2 — League mechanics must be read from the league, never assumed
EVIDENCE: I2, I3, I4. Three settings — daily lineups, the bracket, the standings rule — were modelled from fantasy-basketball convention and corrected only when measured or when you showed screenshots. Each correction moved odds by whole points. **Lesson:** a single `league_settings.json`, verified from the league's own pages, that every constant reads from; a test that fails when any simulator constant diverges from it; and a settings review as the first item of every season.

### L3 — Audits test arithmetic; failures live in sentences and in state transitions
EVIDENCE: I11, I12, I13. The 34-of-35 audit, parity EXACT, 145 DOM assertions — all green the evening the LEAN line was wrong. Undo/insert/resync bugs are state-transition bugs; the LEAN and shift lines are prose-claim bugs. **Lesson:** every log line and warning that makes a claim about state gets a test that asserts the claim against the state; every state-mutating control (undo, insert, resync, numbered fix) gets a property test — "after any sequence of operations, the board equals the recap" — in the DOM harness, not only in Python.

### L4 — Gates are untested until seen red; evidence must carry its own date; artifacts need overwrite guards
EVIDENCE: I5, I6, I7, and the empty-log near-miss on 10/15. **Lesson** (already law in `LESSONS.md` 15, 19, 20, 21, extended): a merge is blocked unless each gate's log shows its PASS line *and* exit 0, captured by the gate runner itself, not read off a terminal; the three-gate run is one script with one JSON verdict file the PR body quotes.

### L5 — The agent's judgment calls were the costliest errors
EVIDENCE: I8 (deferral), I10 (built to answer a question; parameter chosen by a file), the circular grader, the 97.8%. INFERENCE: each had the same shape — a locally reasonable choice made silently, discovered by you from its consequences. **Lesson:** the governors have to be loaded by the harness, not by a keyword; house rules live in a repo file the session reads at start; any parameter a run depends on is stated to you in one line *before* the run; a question gets an assessment, never a build; disputed results are marked DISPUTED in any summary that carries them forward.

### L6 — A grade is only as independent as its grader
EVIDENCE: 33 mock grades and the league grade all use the house weekly model to score rosters the house card built. **Lesson:** keep the house grade (it measures internal consistency) and add two independent graders — the outside consensus lines (Yahoo/Hashtag/RotoBaller medians) and, from the first week on, actuals — and report all three. A "confidence %" is reported with the sentence that says what it measures, every time.

### L7 — Frozen rosters and random schedules are the model's largest unmodelled risks in-season
EVIDENCE: `after-report-2026-10-14-league-draft.md` §9; the in-season grinders (Will 83 moves, Martin 50 and the title). **Lesson:** the draft tool is finished; the in-season tool does not exist yet. Streaming, IL+, waivers, trades and the real matchup schedule are where the next 18 weeks are won, and the simulator sees none of them.

### L8 — What worked, and must be kept
Red-first fixes with gates (`test_gates.py` drives each gate to refusal and acceptance); the lock pool pinned by git revision; Chromium replays of every live room; the planes gate (kit = deck); the two-run rule for Monte-Carlo figures; the after-report contract with Bounds and decision sheets; the verified league simulator (`league_sim.py --verify`); the owner's veto and judgment layers as data, not code.

---

## 3. Self-grade (honest)

| area | grade | why |
|---|---|---|
| Arithmetic and engine parity | A | 0.0 in nine categories on both planes; JS = Python at 481/481 turns. |
| Tool state integrity in live rooms | A− | 156/156 on the real draft after 4 undos, 3 inserts, 1 halt; the words were wrong three times. |
| Data provenance | C | Teams fixed in July; stat-line vintage not until 10/12; 318 provenance rows still July-dated at the draft. |
| League-mechanics realism | B− | Three convention-based assumptions corrected late; schedule and in-season dynamics unmodelled. |
| Process discipline (mine) | C+ | Two scope breaches, one deferral that cost four days, one near-miss on an empty gate log. |
| Reporting honesty | B | Bounds and decision sheets every time; but a near-tautological confidence figure and a circular grader were disclosed rather than fixed. |
| Draft outcome | — | 22.5% title share, rank 1 of 12 on the model; your picks beat the card's at 4 of 6 disputed turns. Real grade: the season. |

---

## 4. The plan — work packages

Priority: **P0** this week (in-season operation starts 10/21), **P1** before week 3, **P2** by the All-Star break. Every package ships red-first (a test that fails before the fix), behind the existing gates, with an after-report and a decision-sheet row. No package changes a projection line without a dated fetched source.

### A. Data truth
- **A1 (P0) Line provenance per row.** Add `line_source, line_season, line_method, line_date` to both planes' pools. Gate: any top-200 row whose `line_source` is empty or `memory` fails the build. Test: a row with `line_source=memory` → refusal. Deliverable: `check_provenance.py` extended; both planes backfilled from WO-5/MG/blend records (every top-180 row has one; the tail is `UNANCHORED` and says so on the card).
- **A2 (P0) D-INT-1 re-dating pass.** Re-verify the 318 July-dated roster rows against ESPN live; `--max-age-days 14` passes on its own file; the weekly in-season pull keeps it green.
- **A3 (P0) Status feed.** Daily in-season pull reads Yahoo's status letters (Q/O/IL) and the ESPN injury feed; a row flagged by either carries a dated receipt or the availability tier it implies; "Q at 1.00 with no receipt" fails the build (Durant and Bridges were there on draft night).
- **A4 (P1) Range check as a gate, not a queue.** `range_check.py` runs at every build; a top-150 row with a cell outside all references needs either a dated receipt (`[SINGLE-SOURCE]`-style) or a waiver named in the build log. Owner alert rule: >25% of the top 150 flagged → an owner-facing report that day.
- **A5 (P1) Points identity as a hard gate** (D-1009-3): top-200 rows beyond max(1.0, 8%) fail; current offenders re-derived from fetched lines.

### B. Model realism
- **B1 (P0) `league_settings.json`.** Lineup slots, bench, IL+ count, daily lineups, 18 weeks, the fixed schedule rotation, 8-team no-bye bracket, tiebreak rules, roster limits, waiver rules — verified from the league's settings page (owner screenshot pinned). `arena.py`, `hoops.py` and the page read every constant from it; `test_settings.py` fails on any divergence.
- **B2 (P0) Real schedule.** Ingest the league's week-by-week matchups; `league_sim.py --schedule` simulates the real pairings; report random-pairing and real-schedule odds side by side.
- **B3 (P1) In-season roster dynamics.** Streaming model (games-per-week maximization with the daily-fill rule), IL+ slots (an IL player frees a roster spot), waiver replacement at replacement level when a player is out. Validate against last season's weekly scoreboard (your 18 weekly category counts are on file: mean 5.72, sd 1.56).
- **B4 (P1) D-1009-2.** Move the availability discount's zero to replacement level on both planes (or decide not to, on the record); red-first; re-grade the 33 rooms to show the effect.
- **B5 (P1) Pick engine bench weights.** `lineup_weights`/`bench_bound` still use the static 0.15 in `slots_left`/trial; measure whether the card's ordering changes under daily-fill weights there too; ship or document the reason not to.
- **B6 (P0) Calibration ledger.** `calibration.md` + `calibration.json`: each week, the model's predicted category-win probabilities vs the actual scoreboard (Brier), each player's projected vs actual per-game line, the title-odds trajectory. Scored weekly, reported monthly. This is the only grade that is not circular.

### C. Tool integrity (deck)
- **C1 (P0) D-LD-1 + D83-1.** History re-render shows undone entries as undone (or drops them); the shift line reports the card rank on the board before the pick or says nothing; red-first DOM tests on the real draft's event file (`m100_tool_events.json`).
- **C2 (P0) D-1013-2 RESYNC hardening.** Preview what the paste resolves to and ask before any wipe; refuse a paste whose pieces do not all resolve or that is the page's own history; keep every replaced board behind an Undo. Red-first with the exact 10/13 paste.
- **C3 (P1) D82-1 resolver.** In LIVE mode, a bare surname with 2+ available namesakes shows a one-key disambiguation line instead of silently choosing (the pre-9/29 halt buried the owner at "George"; the fix is a choice, not a halt). Test with "Green", "George", "Williams".
- **C4 (P0) Prose-claim tests.** For every ⚠/· line the page emits, a test asserts the sentence's claim against the state that produced it (LEAN, shift, "no longer your pick", "assumed over", "injury-excluded"). Harness: extend `lean_dom_check.mjs` into `claims_dom_check.mjs`.
- **C5 (P1) State-transition property test.** Random sequences of feed/insert/undo/numbered-fix/resync over recorded rooms; invariant: the board equals the recap after the sequence that the recap implies. Runs in the DOM harness.
- **C6 (P1) In-season page mode.** The deck grows a "season" mode: my roster, this week's opponent, category win probabilities, the streaming/pickup card, trade evaluator entry. Same engine, same gates, same publish procedure.

### D. Agent process (the part that failed most)
- **D1 (P0) Governors loaded by the harness.** SessionStart hook loads plan-gate, scope-fence, adversarial-verify from the synced skills on every session in both repos; verify with a startup check that fails loudly if a governor is missing (I10/R1).
- **D2 (P0) `RULES.md` in both repos**, read at session start: a question gets an assessment, not a build; a stated requirement is not a build order; every run parameter (window, sample, threshold, seed) is stated to the owner in one line before the run; a finding touching >25% of the top 150 within 7 days of a lock is raised the same day; disputed results are carried forward only as DISPUTED; no figure is typed by hand (writers read records).
- **D3 (P0) One gate runner.** `scripts/gates.py` runs check_report, judgment_open_items, repeat_market_check (and the deck chain for a build), writes `gates.json` with each gate's PASS line and exit code, and the PR body quotes it; a merge without `gates.json` on the head commit is refused by the stop hook.
- **D4 (P1) Independent graders.** `grade_room.py --grader house|consensus|actuals`: the consensus grader scores rosters on the outside-line medians; the actuals grader scores on the season to date. Every room report shows all available graders.
- **D5 (P1) Confidence sentences.** Any percentage labelled confidence/integrity/odds carries, in the same cell, what it measures and its error (Monte-Carlo SE, or "agreement with consensus, not foresight").
- **D6 (P1) Compaction ledger.** `OPEN.md` lists disputed results and unanswered owner questions; the session re-reads it after every compaction; a summary may not promote an OPEN item to a finding.

### E. In-season operating cadence (what the tool does from 10/21)
- **Daily (automated, before 9am ET):** status pull (A3) → availability re-derive → waiver scan (every add/drop pair through the verified sim, as `waiver_moves.py`) → streaming suggestions for the day → one short owner note with any item that moves the title share by ≥0.5 points.
- **Weekly (Monday):** matchup preview vs the real opponent (category by category, with their roster as of that morning), lineup recommendation, the previous week's scoreboard ingested into the calibration ledger (B6), title-odds update on the real schedule (B2).
- **On request:** trade evaluator (two-for-one and multi-player, both rosters re-simulated), injury what-ifs (the §6 stress method), "should I pick up X" (the §7b method).
- **Monthly:** projection re-derivation (rolling 2025-26 + 2026-27 actuals, fetched, with provenance), the after-report with the calibration scores, the decision sheet.

---

## 5. Bounds

**Out of scope by design.** No projection line changes in this plan; no re-grade of past mocks except where a package names one (B4, D4).

**In scope and unverified.**
- Whether B5 (the pick engine's static bench weights) matters: did not measure; the package measures it.
- Whether the league exposes the schedule and settings in a form the daily pull can read without a login: `NOT-ATTEMPTED`; owner screenshots are the fallback (as on 8/04).
- The size of the circular-grader effect: `UNVERIFIABLE` until D4's consensus and actuals graders run.

---

## 6. The prompt to re-feed to Code

Paste the block below as the opening message of a fresh Code session in `fantasy-basketball-2026-27` (the deck repo `yahoo-fantasy-basketball` is cloned alongside, as in every session).

```
You are the Co-GM agent for the 2026-27 fantasy basketball season. The draft is done (seat 10, locked lines v69; league grade in report/after-reports/after-report-2026-10-14-league-draft.md). Read, in this order, before acting:
1. report/plans/co-gm-self-audit-2026-10-15.md (this plan) — the incidents, lessons and work packages.
2. yahoo-fantasy-basketball/LESSONS.md (23 lessons) and report/after-reports/after-report-2026-10-13-scope-fence.md §4.
3. The open decision sheet: D-INT-1, D-INT-2, D-LD-1, D-LD-2, D82-1, D83-1, D-1013-2, D-1009-2.

Rules in force (write them into RULES.md in both repos as package D2's first step):
- Plan-gate before any consequential action; the gate's output is emitted to the owner before the work.
- A question gets an assessment, not a build. A stated requirement is not a build order.
- Every run parameter (window, sample, threshold, seed, source) is stated to the owner in one line before the run.
- No data is written from memory: a team, position, stat line, minutes, games or status value needs a dated fetched record pinned in the repo.
- Every fix lands red-first: a test that fails before the fix, passes after, and a gate that has been seen red.
- No figure in a report is typed by hand; writers read records. Monte-Carlo figures are run twice.
- Every gate run writes a PASS line and exit code to gates.json; no merge without it on the head commit.
- Disputed results are carried only as DISPUTED; OPEN.md is re-read after every compaction.
- Publish only after a fresh read of the artifact, byte-verify the served page, and never during a live room.

Execute the packages in this order, each as its own PR pair (deck + kit) with an after-report gated by check_report.py and the two deck --check-report gates, and stop for the owner's decision where a package names one:
P0: D1 (governor hook + startup check), D2 (RULES.md, OPEN.md), D3 (gates.py + gates.json + stop-hook refusal), B1 (league_settings.json from the owner's settings screenshots — ask for them first), A1 (line provenance columns + gate), A2 (D-INT-1 re-dating), A3 (status feed + Q-at-1.00 gate), C1 (D-LD-1/D83-1 red-first), C2 (D-1013-2 RESYNC hardening), C4 (prose-claim tests), B2 (real schedule — ask the owner for the matchup schedule), B6 (calibration ledger, first entry = week 1), E daily/weekly cadence scripts (waiver scan reusing draft-league-2026-10-14/waiver_moves.py, matchup preview, lineup recommendation).
P1: A4, A5, B3, B4, B5, C3, C5, C6, D4, D5, D6.
P2: anything the P0/P1 after-reports put on the decision sheet.

Acceptance for each package is the red-first test, the gate verdict in gates.json, the after-report's Bounds and decision sheet, and both PRs merged with branches synced. Report to the owner in plain language at the end of each package: what changed, what it was tested against, what it cannot see.
```

---

## 7. Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-SA-1 | Execute the plan as ordered (P0 first), or re-order (e.g. the in-season cadence E before the integrity packages)? | as ordered: D1–D3 and B1 first, because every later package depends on the settings file and the gate runner |
| D-SA-2 | D-1013-2 RESYNC: harden (C2) or hide the button for the season? | harden (C2) |
| D-SA-3 | D82-1 resolver: disambiguation line (C3) or keep the bare-surname rule? | C3 |
| D-SA-4 | The independent graders (D4): add both consensus and actuals, or actuals only? | both |
| D-SA-5 | The league settings and schedule: owner screenshots, or does the league expose them to a daily fetch? | screenshots, pinned like the 8/04 intel |

## Provenance
- Written 2026-10-15 from the records named in the header; no figure here is from recall except the self-grades in §3, which are judgments and say so.
- No line, tag, placement or price changed; nothing was published.
