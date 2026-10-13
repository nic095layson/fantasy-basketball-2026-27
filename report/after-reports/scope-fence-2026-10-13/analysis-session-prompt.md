# Prompt for the analysis session — fortifying Gauntlet and operational excellence

Written 2026-10-13 at the owner's request ("prompt for another Code session to analyze where Gauntlet and operational
excellence can be fortified"). Paste everything between the markers into a new Claude Code session. It is written
for a session that starts cold.

---- BEGIN PROMPT ----

GAUNTLET — governance analysis: where can Gauntlet and operational excellence be fortified, so that the process catches the 2026-10-12 class of failure instead of the owner?

## Context (read before planning)

- **The owner** runs a fantasy-basketball draft project across two repos:
  - `nic095layson/fantasy-basketball-2026-27`, "the kit";
  - `nic095layson/yahoo-fantasy-basketball`, "the deck".
- **The doctrine.** The governance lives in `nic095layson/claude-core-skills`, the source of truth for plan-gate, scope-fence, adversarial-verify, gauntlet and after-report. Those skills cite lessons-ledger, live-state-truth and research-methodology. The project's lessons ledger is the deck repo's `LESSONS.md`. `nic095layson/claude` is the older lineage repo the skills' provenance cites.
- **What the kit binds every session to:**
  - The kit's `CLAUDE.md`: "The core governors run on every session here — plan-gate → scope-fence → adversarial-verify".
  - `report/pre-draft-workorder-2026-10-01.md` §1 adds: "Emit the plan gate … before the first consequential action."
- **The incident.** Read `report/after-reports/after-report-2026-10-13-scope-fence.md` in the kit (`main`), and its evidence folder `report/after-reports/scope-fence-2026-10-13/`. In short:
  1. **A data window chosen silently.** Answering an owner question, a session used a 20-season data window (2006-07 to 2025-26). It was never stated as a choice or opened for objection; in the log it appears only as one tool-call label. The window was set by the first season of a data file, and the league's per-36 numbers show the era is not stable over it.
  2. **A fix built without being asked.** The same session built an unrequested, fix-shaped "WO-5b" candidate (326 re-derived lines). The owner caught both; the process did not.
  3. **Governors never loaded.** In the three-week log, up to the owner's 10/13 request, no Skill-tool load of plan-gate, scope-fence, adversarial-verify or gauntlet exists. plan-gate and adversarial-verify text sat in context only as 28 re-attachments after compactions, each carrying an older task's arguments. scope-fence's text was never in context until the owner asked about it.
  4. **Doctrine and skills missing.** `~/.claude/CLAUDE.md` does not exist in the cloud container. lessons-ledger, live-state-truth and research-methodology are not synced there.
  5. **Compaction promoted a disputed result.** One compaction summary carried a disputed result forward as an established finding.
  6. **An unwritten house rule.** "A question gets an assessment, not a fix" exists only in session memory, not in any committed file.
  7. **An incomplete log.** The session log keeps text for only a minority of assistant messages (2 of 22 and 5 of 32 in the measured windows), so log-based audits of "what the owner was told" are limited.

## Your task

Analyze, and propose. Change nothing.

Answer each question below with dated evidence. Use tiered recommendations: MUST ADD / HIGHLY RECOMMEND / NICE TO HAVE / NOT NEEDED / fold-don't-add. Each high tier states what evidence would demote it, and gives the exact proposed text or diff, written in your report and not applied.

1. **Loading without the keyword.** Gauntlet loads the governors only when "GAUNTLET" is typed, and the kit's promise that the governors "run on every session" has no mechanism behind it. Compare the options: a `CLAUDE.md` instruction to load (not recall) the governors on every owner request that is not trivial; a UserPromptSubmit or SessionStart hook in the kit's `.claude/settings.json`; changes to the trigger descriptions; a per-turn "Fired" line. Give each one's cost, including over-firing on trivia (Gauntlet rule 3, plan-gate's triage rule).
2. **Doctrine on the cloud surface.** `~/.claude/CLAUDE.md` is absent in Claude Code on the web containers, and three cited skills are not synced. Where should the doctrine live so that a cloud session receives it: the repo's own `CLAUDE.md`, the skills sync, a SessionStart hook, or something else? Check the claude.ai / Claude Code documentation for how each surface loads `CLAUDE.md` and skills, and quote it with dates.
3. **Compaction.** Re-attachment after compaction keeps old task arguments, and summaries can promote disputed results to findings. What should survive a compaction? For example: a per-task gate record; an "open objections / disputed results" list; marking unvetted results as unvetted; dropping stale skill arguments. What is in the owner's control (instructions, hooks) and what is not?
4. **Method choices inside the fence.** The data window was an in-scope method choice, not an "adjacent problem", so scope-fence's trigger does not obviously cover it. Where does "state the window, sample and assumptions before running an analysis the owner will rely on" belong: plan-gate §3, a domain rule in the kit's `CLAUDE.md` (for example, "historical analyses state their seasons and an era check first"), or both?
5. **Dry runs and stated requirements.** Is a "dry-run candidate" built in scratch a fix under scope-fence? Is an owner message stating a requirement mid-turn ("X is critical") authorization to build? Propose wording for scope-fence and for the kit, and say where "a question gets an assessment, not a fix" should be written down.
6. **Long silent stretches.** 14 tool calls in 6.4 minutes carried method choices with nothing to the owner except tool labels. Would a phase-boundary rule ("state the choice in one line before running it") pay for itself? How would anyone check it, given the log's text gaps?
7. **Gauntlet's own gaps.** Its trigger evals are authored but not run (UNMEASURED), its named-firing line reports loads but cannot catch a skipped load on an un-keyworded task, and it depends on governors being present. What would a measurable fortification look like? Pre-register any experiment the way research-methodology requires; read that skill from the repo, since it is not synced on the web surface.
8. **Operational excellence beyond the governors.** Look for anything else in the record:
   - the lessons ledger lives in the deck repo while the skills point to `.claude/LESSONS.md`;
   - session-only rules;
   - the incomplete session log as an audit source;
   - anything you find yourself.

## How to work

- **Run the full Gauntlet.** Load plan-gate, scope-fence, adversarial-verify and after-report through the Skill tool. Load, do not recall. Emit the full plan-gate block, with a branch rule for every phase that depends on a repo or doc you have not read, as its own message before any work. End with the `Fired` line, saying honestly what loaded.
- **Access first.** Your first step is to confirm you can read all three repos (`claude-core-skills`, the kit, the deck). If one is missing, add it. If that fails, say so with the error and narrow the analysis. Don't guess its contents.
- **Verify the incident's claims yourself before relying on them.** At minimum, spot-check:
  - `out/timeline.json`'s census;
  - `out/integrity_check.txt`;
  - one re-run from §6 of the after-report.

  Mark EVIDENCE vs INFERENCE, and give every unknown its gap provenance (NOT-ATTEMPTED / ATTEMPTED-FAILED / UNVERIFIABLE).
- **The fence:**
  - Read-only across all three repos, except your one report. Do not edit any skill, `CLAUDE.md`, hook, settings file, data file, deck page or published artifact.
  - Do not merge anything.
  - Adjacent problems you find get a one-line flag in the report, not a fix.
- **The deliverable.** One report in after-report shape at `results/2026-10-13/gauntlet-fortification/REPORT.md` on a new branch in `nic095layson/claude-core-skills` (the governing repo's results convention), opened as a draft PR.
  - If you cannot push there, put the report at `report/after-reports/gauntlet-fortification-2026-10-13.md` in the kit instead, and say why.
  - Put the raw outputs beside the report.
  - End with a decision sheet: one row per proposal, with its default if the owner is silent. Defaults change nothing.
- **Owner preferences:**
  - Plain language, and a short "In plain language" section at the end.
  - Use they/them for the owner.
  - Decisions belong to the owner.
  - Every count comes from a record, never from recall.
  - No model identifiers in commits or PRs.

---- END PROMPT ----
