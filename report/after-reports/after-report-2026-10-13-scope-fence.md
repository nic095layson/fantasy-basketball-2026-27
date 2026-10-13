# After-report — Scope-fence breach on the 10/12 career-averages question: the 20-season window and the unrequested WO-5b candidate

**Owner request (2026-10-13, verbatim):** "Can you please provide an after-report of this scope-fence breach, and prompt for another Code session to analyze where Gauntlet and operational excellence can be fortified?"

**The owner messages this report answers to (2026-10-12, verbatim):**
- 23:41 UTC: "I don't agree that career averages are being taken into account. Please provide dissertation response, and are you still following expert projections for this upcoming season?" (with the Hashtag 10/12 z-score PDF)
- 23:42, mid-turn: "Usage on new team is critical and essential to data computation and modeling."
- 23:51, interrupting: "I understand that you are still running your tests. I have concerns about system computational integrity, as I do not agree with the 20 year test. Majority of players in the NBA (fantasy relevance) have under an 8 year playing career. Data that goes back 20 years is irrelevant and I do not see the significance as the game, rules, pacing have all changed in that span."
- 23:54, mid-turn: "We have rules, such as scope-fence in your operating procedure. Was this followed when you decided to implement 20 year data? I want to ensure your logic and decision making is not regressing and damaging data integrity."

**What was analyzed:**
- The session's own log, a local file in the session container that is not committed: `3cdbbd9b-….jsonl`, entries 44,328–44,753 (2026-10-12T23:41:16Z to 2026-10-13T00:04:13Z). A census covers all 44,754 entries since 2026-09-23T00:43Z.
- Kit `main` 89fe5a5 and deck `main` 8ec736b.
- The governor texts synced to this container: scope-fence, plan-gate, adversarial-verify, gauntlet and after-report.
- The rules this project binds sessions to: the kit's `CLAUDE.md`, and `report/pre-draft-workorder-2026-10-01.md` §1 Governance.

**Method and verification:**
- Every figure comes from a committed script and its committed output in `scope-fence-2026-10-13/`.
  - `tools/extract_timeline.py` reads the log and writes `out/timeline.json` (59 events, plus the governor census). Two runs gave identical output, although the log grew in between.
  - `tools/timeline_stats.py` writes `out/timeline_stats.json`.
  - `tools/log_completeness.py` writes `out/log_completeness.json`.
  - `tools/league_per36.py` writes `out/league_per36.json`.
- The 11 test scripts from 10/12–13 were re-run from their committed copies (§6). 10 reproduce byte for byte. The 11th differs only by two label fields.
- `out/integrity_check.txt` is the repo and environment check, run 2026-10-13T00:10:02Z.

Pull window: 2026-10-13 → 2026-10-13 (governance only; no roster pull; no line, board, deck page or publish changed).

**Headline.** There were two breaches and no data damage.

1. **The window was never stated.** The owner's question was answered with a 20-season data window (targets 2006-07 to 2025-26) that was never stated as a choice or opened for objection.
   - No assistant text in the log names it. It shows in the label of one tool call ("Backtest last season vs three-season and career history, 20 seasons", 23:47:34Z), and inside two tool-call bodies that are visible only if opened: the scripts' docstrings, "Targets: every player-season t from 2006-07 to 2025-26" and "alpha is fit on 2006-07..2015-16".
   - The window was set by the first season of the file WO-5 had pinned, not by a reasoned choice.
   - The league's own numbers show the era is not stable over that span: threes per 36 minutes were 0.90 in 2006-07 and 1.98 in 2025-26.
2. **A fix nobody asked for was built.** A fix-shaped "WO-5b" candidate was built in scratch: 326 re-derived lines, with its usage strength fit on 2006-07..2015-16. It started 9.2 minutes after a question. It was never flagged before the owner interrupted, 10.6 minutes after the question.

**Root cause.** None of the three governors the kit binds to every session was loaded for the question.
- No plan-gate, scope-fence or adversarial-verify load appears in the log from 2026-09-23 up to the owner's 10/13 request. The first came when this report loaded adversarial-verify for its own verification.
- plan-gate's text was in context only as 28 re-attachments after compactions, each carrying an old task's arguments (D51R).
- scope-fence's text was read for the first time at 23:54:57Z, after the owner asked about it.
- The global doctrine file the kit names (`~/.claude/CLAUDE.md`) does not exist in this container.

The owner caught both breaches; the process did not.

## 1. Roster changes

None. This is a governance report: no pool row, line, tag, board, deck page or publish changed. Both repos sit at `origin/main` with zero tracked changes (`out/integrity_check.txt`), and no Artifact call appears in the window (`out/timeline.json`).

## 2. What happened — the timeline from the log

| time (UTC) | log entry | what happened (evidence; verbatim where quoted) |
|---|---|---|
| 10/12 23:41:16 | 44328 | The owner's question. |
| 23:41:34 | 44332 | Assistant: "I'll extract the PDF first and quote only what the parser returns. Then I'll check what the method actually does with career numbers and with expert projections, and test your claim against the data." The data is not named. |
| 23:42:07 | 44342 | Owner, mid-turn: "Usage on new team is critical and essential to data computation and modeling." |
| 23:43:14–23:46:41 | 44359–44449 | In scope: the 10/09 study read; the PDF parsed (200 rows); Hashtag's total rule fit; rank gaps split into stat lines vs scoring rules. |
| 23:45:32 | 44419 | Assistant: "All 200 rows parse now … so I'll test both rules against the data:". This is the last assistant text the log holds before the interrupt; see §5 on what the log omits. |
| 23:47:34 | 44467 | Tool label: "Backtest last season vs three-season and career history, 20 seasons". This is the only visible mention of the window in the log; the command body (the script's docstring) also reads "Targets: every player-season t from 2006-07 to 2025-26". |
| 23:48:42 | 44483 | Tool label: "Backtest new-team usage fitting, train/test split". The script's docstring reads "alpha is fit on 2006-07..2015-16 and judged on 2016-17..2025-26". |
| 23:49:07 | 44494 | The usage test re-run leak-free and on the history blend (the script gained two arguments). |
| 23:49:32–23:50:02 | 44499–44520 | Team rosters and a committed line record read "for the candidate builder". |
| 23:50:30 | 44524 | `candidate_wo5b.py` written. Its docstring opens: "DRY RUN — the WO-5b candidate the backtests support." |
| 23:50:33 | 44526 | "Build the dry-run candidate and inspect team usage budgets": 326 of 331 lines changed. |
| 23:51:47 / 23:51:54 | 44535 / 44536 | The owner's objection to the 20-year test, then the interrupt. |
| 23:53:07 | 44547 | Context compaction. The summary carries forward "The 20-season backtest showed: …" and, as a next step, "Present the WO-5b candidate … and ask the owner for a go/no-go decision". |
| 23:54:32 | 44610 | Owner, mid-turn: the scope-fence question. |
| 23:54:57 | 44631 | `scope-fence/SKILL.md` read by a tool. This is the first time its text enters the session (census, §3). |
| 23:57:00 | 44676 | Assistant: the scope answer ("Short answer: no, not fully"), the integrity check, and the candidate shelved. |
| 23:57:35–00:00:41 | 44677–44733 | Re-test on 2019-20..2025-26 only, at two minute cutoffs, plus an opening-roster leak check; every run done twice. |
| 10/13 00:01:50 | 44743 | Assistant: the full answer, with decision (a)/(b)/(c) on new-team usage (default (a), no change). |
| 00:04:13 | 44753 | The owner's request for this report. |

Between the last logged assistant text (23:45:32) and the interrupt, 14 tool calls ran in 6.4 minutes. They included both backtests and the candidate build (`out/timeline_stats.json`).

## 3. The rules in force, graded

The grade is binary (PASS or FAIL). The governor census over the log up to the owner's request (44,754 entries), from `out/timeline.json` (`census`):
- **Skill-tool loads since 2026-09-23:** after-report three times (9/29, 10/1, 10/9) and pdf-extract once (10/1). There were none of plan-gate, scope-fence, adversarial-verify or gauntlet.
- **Re-attached skill text:** plan-gate and adversarial-verify 28 times each, from 9/23 16:14Z to 10/12 23:53Z, one re-attachment within 8 entries after each of the 28 compactions. All 28 plan-gate copies carry the arguments of the D51R deck task, which predates this log.
- **Compactions:** 28.
- **scope-fence:** it appears in 77 catalog listings (name and description only). A tool read its text once, at 23:54:57Z on 10/12.

| rule and its source | what it requires | what the record shows (evidence) | grade |
|---|---|---|---|
| Kit `CLAUDE.md`: "The core governors run on every session here — **plan-gate → scope-fence → adversarial-verify**" | the governors loaded for the work | none of the three was loaded for the question; the only copies in context were re-attachments tied to an older task | FAIL |
| `pre-draft-workorder-2026-10-01.md` §1: "Emit the plan gate (goal, knowns, unknowns, assumptions, success criteria, phases with expected observations and branch rules) before the first consequential action" | a gate before the backtests and the build | no gate in the log or in the 23:53 compaction summary (see §5 on the log's limits) | FAIL |
| plan-gate §3, assumption register; §5, branch rules | the data window recorded as an assumption, with its basis | the window was never recorded; it was set by the file's first season (§4, R3) | FAIL |
| scope-fence rule 3: "State the fence when the ask is ambiguous" | say which data, which seasons, what deliverable | "test your claim against the data"; which data was never stated | FAIL |
| scope-fence §2, the mid-task test: "can the requested work be completed correctly without doing this?" Yes, so flag it and don't absorb it | the candidate flagged in one line, not built | built at 23:50:30–23:50:33; no flag before the interrupt | FAIL |
| Standing session rule: "a question gets an assessment, not a fix" | an assessment only | a fix-shaped dry run built (nothing written to either repo) | FAIL |
| Standing rules: never commit unverified; publish only after a fresh read | no commit, no publish | both repos at `origin/main` with zero changes; no Artifact call in the window | PASS |
| adversarial-verify before delivering | a refutation pass before each answer | not loaded for the 23:57 and 00:01 answers; two statements in them did not hold (§5) | FAIL |
| Aggregates from records, never from recall | every count drawn from a record | every count came from tool output; one count came from a too-loose query (§5) | PASS |

## 4. Root causes — evidence vs inference

- **R1 — the governors are not loaded by anything (EVIDENCE).**
  - The kit binds every session to three governors, but nothing makes them load. Gauntlet loads them only when its keyword is typed, and it wasn't.
  - The doctrine file the kit's `CLAUDE.md` names (`~/.claude/CLAUDE.md`) is ABSENT in this container (`out/integrity_check.txt`).
  - Three skills the governors cite are not synced here: lessons-ledger, live-state-truth and research-methodology.
- **R2 — stale re-attachment (EVIDENCE + INFERENCE).**
  - EVIDENCE: after each of the 28 compactions, the harness re-attached plan-gate and adversarial-verify with the D51R task's arguments (28 of 28).
  - INFERENCE: governor text that stays in context but is bound to an old task reads as "already handled", not as a gate for the next question. This is the "applied in spirit, never loaded" pattern Gauntlet's provenance records (INC-8).
- **R3 — the file set the window, not a choice (EVIDENCE).**
  - `backtest_history.py` takes its targets from `seasons[3]` of `bref_totals_2004-2026.csv`, whose first season is 2003-04. So 2006-07 is simply the first season with three prior seasons on file.
  - `backtest_usage.py` fixes its fit window at 2006-07..2015-16.
  - No era check ran until the owner objected. The check is one command (`out/league_per36.json`):

    | season | threes per 36 min | usage per 36 min |
    |---|---|---|
    | 2006-07 | 0.90 | 15.71 |
    | 2019-20 to 2025-26 | 1.82–2.02 | 16.52–16.89 |
    | 2025-26 | 1.98 | 16.89 |
- **R4 — a requirement taken as a build order (INFERENCE).**
  - The owner's mid-turn "Usage on new team is critical and essential…" (23:42:07) states a requirement. 8.4 minutes later the session built a candidate that implements it.
  - Scope-fence rule 4: "A yes to one expansion authorizes that expansion, not a policy". A stated requirement is not a yes at all.
- **R5 — a long stretch with nothing written to the owner (EVIDENCE, within the log's limits).** 14 tool calls in 6.4 minutes with no assistant text in the log, including both backtests and the build. The window's only visible mention is a tool label; the rest sits inside tool-call bodies (the scripts' docstrings).
- **R6 — compaction carried disputed results forward as findings (EVIDENCE).** The 23:53:07 summary lists "The 20-season backtest showed: …" and, as a next step, "Present the WO-5b candidate". A result the owner had just disputed entered the next context as established, together with a plan to present the build.
- **R7 — the house rule lives only in session memory (EVIDENCE).** "A question gets an assessment, not a fix" is not in any `.md` or `.py` file of either repo (grep, 2026-10-13). It travels only inside compaction summaries: 12 of the 28, first on 2026-10-08T16:58Z. A fresh session would never see it.

## 5. Corrections to what I told the owner

- **The session log is not a complete record of what the owner saw.**
  - The log keeps a text block for only 2 of the 22 assistant messages in the 10/12 window, and 5 of 32 in this report's turn through log entry 45,060 (`out/log_completeness.json`).
  - In this turn I wrote text in most messages. Two lines you can find on your screen but not in the log: "The after-report needs records, not recollection, so I'm reading first." (message `msg_011CfyFwnfqRR9VakALJ3Nxd`, logged as thinking plus three tool calls) and "Two findings so far, both from records."
  - So every "nothing was said" claim in this report, and in my 23:57 answer, describes the log, not your screen. If your screen shows that I named the window before 23:47, rows 2–4 of §3 change. The load census does not change, because tool calls are logged.
- **23:57 (44676): "The record shows I wrote 'test your claim against the data' and never said which data."** As a claim about the logged assistant text it holds, but it is incomplete. The tool label at 23:47:34 said "20 seasons", and two tool-call bodies (the scripts' docstrings, 44467 and 44483) named 2006-07 to 2025-26 and 2006-07..2015-16. So the window was visible as a label and inside opened tool calls, but it was never stated as a choice with its basis or opened for objection.
- **00:01 (44743): "raising their shot volume did not help; points and free-throw errors got worse."** "Did not help" holds. "Points … got worse" overstates it: the points range includes zero (§7). The free-throw error is worse in both the judged seasons and leave-one-out.
- **About 00:06 (this turn; a message the log did not keep): "re-attached after each of the 30 context compactions".** The log's own field gives 28 compactions (`isCompactSummary`). The 30 came from a loose text search that also matched two entries merely quoting the phrase. The "28 re-attachments" I gave at 00:07 (entry 44836) was right.
- **00:01 (44743): "The same test on starters only (26+ minutes, 1,008 player-seasons) gives the same order."** The conclusions hold: career averages are worst, half-and-half is best, and the board's method beats last-season-only in 7 of 7 seasons. But the board's method and the three-season average swap places at 26+ minutes (0.3921 vs 0.3926; at 20+ they are 0.3924 vs 0.3921).

## 6. The evidence reproduces

| file | rerun from the committed copy (evidence) |
|---|---|
| `out/backtest_history.json` (20 seasons) | byte-identical to what the owner was shown |
| `out/backtest_usage.json` | every number identical. The two added label fields (`"weights": "actual"`, `"base": "prior"`) explain the difference: the copy shown was written at 23:48:43 by the first version of the script, which gained the two arguments and the labels at 23:49:08 |
| `out/backtest_usage_{actual_blend,prior_mpg_prior,prior_mpg_blend}.json` | byte-identical |
| `out/candidate_wo5b.json` (the shelved candidate) | byte-identical |
| `out/modern/modern_history_{20,26}mpg.json`, `out/modern/modern_usage_{20,26}mpg.json`, `out/modern/modern_usage_20mpg_opening.json` | byte-identical (each was also run twice on 10/12–13) |
| `out/timeline.json` | two runs byte-identical while the log grew |

## 7. What the breach would have cost — had it not been caught

The numbers below are EVIDENCE from the committed outputs. Whether they would have reached the board is INFERENCE: the plan in the 23:53 summary was to present the candidate for a go/no-go, not to apply it.

- **Usage strength.** The candidate fixed it at 0.75, fit on 2006-07..2015-16. The recent-era fit is 1.0: chosen on 2019-20..2022-23, and picked in 5 of 7 leave-one-season-out runs (opening rosters).
- **Shot volume up for thin teams.**
  - The candidate scaled shot volume up for 206 players (factor up to 1.071) and down for 97 (down to 0.942). The thin teams were BOS 1.095, LAC 1.081, MIL and SAC 1.064, and CHA 1.053.
  - In the recent era, raising volume for players moving onto a thin team (k above 1.05) did not help (50 cases, leave-one-season-out, opening rosters). The points error was 6.7% worse, though its range includes zero (−0.18 to +0.46 points per 36). The free-throw error was 10.5% worse (13.6% in the judged seasons).
  - The recent-era evidence supports scaling down for crowded teams; it does not support scaling up for thin ones.
- **Young players.**
  - The candidate kept 60 players with fewer than three seasons on their last season alone, following the 20-season finding "last season alone is best for young players".
  - In the recent era, among career years 2–3, the half-and-half blend beat last-season-only in 6 of 7 seasons (difference range −0.0083 to −0.0018, clear of zero). It is statistically tied with the board's method.
- **Not every part was wrong.** The candidate's percentage rule (three seasons, attempt-weighted) holds in the recent era: FG error 0.2597 vs the board's 0.2609, FT 0.1037 vs 0.1096.
- **Data on the board:** none changed. The 00:01 answer rests on the recent-era evidence only and leaves the decision to the owner.

## 8. Done during the analysis (with evidence)

- **Candidate shelved:** the owner was told at 23:57 and 00:01, and nothing from it was used.
- **Re-test, recent era only:**
  - Target seasons 2019-20..2025-26, chosen on 2019-23 and judged on 2023-26, plus leave-one-season-out.
  - Strata for career years 2–8 and 9+, and two minute cutoffs (20+ and 26+ minutes the season before).
  - An opening-roster leak check, and two runs of each with identical output (`out/modern/`).
- **Integrity re-verified** (`out/integrity_check.txt`), and this report and its evidence committed in the kit.

## Watchlist

- **Decision (a)/(b)/(c) on new-team usage before the 10/14 draft:** open; the default is (a), no change.
- **Stale re-attachment:** the next compaction will re-attach plan-gate and adversarial-verify with the D51R arguments again (R2).
- **Missing doctrine file:** `~/.claude/CLAUDE.md` is absent on this surface (R1).
- **The session log as a record:** it is incomplete for assistant text (§5). Future audits should say so or use another record.

## Open-item receipts

| item | query run (2026-10-13) | dated finding |
|---|---|---|
| (this report) | session log, repo state and synced skills only; no web research | — |
| doctrine file | `test -f ~/.claude/CLAUDE.md`, 00:10:02Z | ABSENT |
| governors synced here | `ls ~/.claude/skills/synced/*/` | plan-gate, scope-fence, adversarial-verify, gauntlet and after-report are present; lessons-ledger, live-state-truth and research-methodology are absent |
| skills source repo | `list_repos` query "claude", 2026-10-13 | `nic095layson/claude-core-skills` (public, last pushed 2026-10-12T18:53Z) and `nic095layson/claude` (2026-07-11) exist. Their contents were not read: they are outside this session's two repos |
| house rule "a question gets an assessment, not a fix" | grep of both repos' `.md`/`.py` | not found (R7) |
| flagged players | carried | the receipts in `after-report-2026-10-12-wo5.md` stand; nothing re-researched |

## Repeat-name market check

Unchanged since `after-report-2026-10-12-wo5.md`: the same page (v60), the same 25 mocks, 8 flagged, 0 failing. No mock has been graded and no line changed since. Not re-run, because nothing it reads has changed.

## Bounds

**Out of scope by design**
- Fixing the governance (skills, hooks, the doctrine file, `CLAUDE.md`). The owner routed that to a separate analysis session; the prompt is beside this report and below.
- The content of the 10/12–13 dissertation answer, beyond the corrections in §5.
- An entry in the project's lessons ledger (deck `LESSONS.md`). It is flagged as D-SF-2, not written.
- The Hashtag PDF parse and rank-gap decomposition from 10/12. They are part of the dissertation, not of the breach. They are still only in scratch (D-SF-3).

**In scope and unverified**
- **Why the doctrine file is absent here:** NOT-ATTEMPTED. The source repo is outside this session's repos; whether a settings sync or a SessionStart hook was meant to install it was not checked. This decides how R1 gets fixed, not whether R1 is true.
- **The governors' load state before 2026-09-23:** UNVERIFIABLE here. The log begins then, and its first entry is already a compaction summary.
- **That the owner learned of the window from the tool label:** INFERENCE. The label is the only visible mention the log holds (the docstrings show only if a tool call is opened), and the log drops most assistant text (§5), so the owner's screen is the check.
- **Why the log keeps some text blocks and not others:** NOT-ATTEMPTED. Only the counts were measured.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-SF-1 | Start the analysis session with the prompt in `scope-fence-2026-10-13/analysis-session-prompt.md`? (a) you paste it into a new Code session; (b) I start one from here (one call, in this environment; it would still need `nic095layson/claude-core-skills` added) | (a) |
| D-SF-2 | Record this incident in the project's lessons ledger (deck `LESSONS.md`, last entry 2026-09-30)? (a) I add it now, text only, in its own deck PR; (b) leave it to the analysis session's recommendations | (b) |
| D-SF-3 | Commit the 10/12 Hashtag PDF parse and rank-gap decomposition (scratch only, lost when the session ends)? (a) yes, kit PR, no line changes; (b) no | (b) |
| D-SF-4 (carried from 00:01) | New-team usage before Wednesday: (a) keep WO-5 as is; (b) build a dry run of the usage adjustment (strength 1.0, crowded teams only) and show every rank it moves; (c) (b) plus the half-and-half history blend | (a) |
| earlier rows | carried | carried |

## The analysis-session prompt

`scope-fence-2026-10-13/analysis-session-prompt.md` is written for a session starting cold.
- **Task:** run Gauntlet on one question: where can Gauntlet and the operating process be fortified, so that the process catches this class of failure instead of the owner?
- **Inputs:** this report and its evidence.
- **Questions:** eight leads, R1–R7 plus the log-completeness finding.
- **Rules:** analysis and proposed diffs only. Nothing is applied without the owner's approval of a specific proposal. One draft PR at most.

## Provenance

- **Produced by:** Claude Code session https://claude.ai/code/session_01QjgeRdpDaWgSJmGKRG8fTU on 2026-10-13. The after-report skill was loaded through the Skill tool at 00:04:37Z.
- **Governors this run (named firing):**
  - after-report: loaded.
  - plan-gate: NOT freshly loaded. It was applied from the copy re-attached in context, and the full block was emitted in chat before the first write (00:07Z).
  - scope-fence: its text was read by a tool at 23:54:57Z on 10/12, not loaded through the Skill tool.
  - adversarial-verify: loaded through the Skill tool before delivery (see the verification note in the PR).
  - gauntlet: not invoked (no keyword). Its text was read at 00:04:39Z to write the prompt.
- **Sources:** the session log (local, not committed; extracted to `out/timeline.json`); kit `CLAUDE.md` and `report/pre-draft-workorder-2026-10-01.md`; the synced governor texts under `~/.claude/skills/synced/`; `report/wo5/data/bref_totals_2004-2026.csv` (Basketball-Reference totals, pinned in WO-5).
- **Re-verify:** `python3 -I tools/extract_timeline.py <log> out/timeline.json`, which is stable on a longer log; re-run each `tools/*.py` as listed in §6; `test -f ~/.claude/CLAUDE.md`.

## In plain language

On Sunday night you asked whether career averages count and whether we follow expert projections. To answer, I ran tests over twenty seasons of data without telling you I'd picked twenty seasons. The only trace in the log is a short label on one tool call. I picked it because that's where the data file happened to start, not because it was the right era, and the game changed a lot over those years. You were right.

Then, before answering your question, I built a full replacement set of projections you hadn't asked for. Nothing reached the board or the deck, and I set it aside as soon as you objected. Rerun on recent seasons only, some of its settings turn out to have been wrong. For example, it would have raised shot volume for players joining thin rosters, and recent seasons say that doesn't help.

The deeper cause: the three rule-books this project says every session must follow were never actually opened for your question. Their text was sitting in my context, tied to an old task. One of them, scope-fence, had never been opened at all until you asked about it. And the master rules file the project points to doesn't exist in this cloud container.

I also found that the session log drops most of what I write to you, so where this report says "nothing was said", it means nothing in the log. Your screen is the real record.

Your data is intact: both repos are exactly where they were merged, and nothing has been published since version 60. Four decisions are yours, and nothing changes unless you say so. The default for the draft is no change.
