# fantasy-basketball-2026-27 — a domain-layer project

Governed by the operating doctrine of `nic095layson/claude-core-skills`. The block
below is that doctrine's cloud-safe copy (`instructions/project-doctrine-block.md`
there); `~/.claude/CLAUDE.md` does not exist in cloud containers, so nothing here
depends on it.

Within the governed process, this project's domain rules apply: the 9-cat z-score
engine, the July-2026 projections baseline, and the edit-CSV → rerun →
board-regenerates workflow. Core on top, domain within.

Three domain instances of the general rules (architecture-contract Decision 2 —
these win here):
- Historical analyses state their seasons and run the era check
  (`league_per36.py`) before any conclusion rests on a multi-season window; a
  window inherited from a file's first season is an assumption, named as such.
- Every method choice that will reach the board, the deck, or a work order is
  stated to the owner in one line before the run that uses it.
- A question about the board's method gets an assessment and the decision
  options; a candidate (WO-5b class) is built only on an owner go.

---- BEGIN BLOCK ----

## Operating doctrine (every session, every surface)

The core governors run on every non-trivial request here — **plan-gate** before the
first consequential action, **scope-fence** during the work, **adversarial-verify**
before delivering — and they are **loaded with the Skill tool, never applied from
memory**. Governor text already in context from an earlier task or from a compaction
does not count as loaded. Source of truth: `nic095layson/claude-core-skills`.

Four rules this project binds every session to, in addition to the governors:

1. **A question gets an assessment, not a fix.** When the owner asks whether something
   is right, or disagrees with a result, the deliverable is the assessment. A fix,
   candidate, rewrite, or dry run — even in scratch — waits until the owner asks for it.
2. **Method parameters are stated before the run.** Any data window, sample, cutoff,
   era, or baseline an analysis runs on is named to the owner in one line before the run
   that uses it, with its basis. A parameter inherited from a file's extent or a script's
   default is an assumption, not a choice.
3. **A stated requirement is not a build order.** "X is critical" says what the work
   must respect; it authorizes nothing new.
4. **Decisions come as options.** When there is a decision for the owner to make, offer
   2–4 options, each with a brief plain-language explanation, the recommended one listed
   first and marked "(Recommended)". Where the surface has clickable choices (Claude Code:
   the AskUserQuestion tool, with a preview card when comparing options helps), use them;
   otherwise a numbered list. Not for trivial choices or ones with an obvious default (state
   the default in one line), and never in an unattended run, where nobody is there to click:
   record the open decision in the report instead.

After a compaction: list the owner's open objections in one line before continuing;
a result the owner disputed stays disputed; reload the governors before the next
consequential action.

Enforcement: this repository's `.claude/settings.json` wires the governance hooks
(prompt trigger, Stop gate, first-write reminders, compaction protocol). They run in
Claude Code sessions that start inside this one repository, on the web included. A
cloud session with several repositories attached reads only plugin keys from each
repository's settings, not hooks (Claude Code settings documentation, read 2026-10-13);
there, this file and the plugin route carry the doctrine.

---- END BLOCK ----
