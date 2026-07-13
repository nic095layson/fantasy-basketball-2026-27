# claude.ai Project instructions — fantasy basketball — canonical copy

Versioned per the same drift law as
`claude-core-skills/instructions/claude-ai-custom-instructions.md`: the
instructions box in the claude.ai Project and this file must never disagree.
Update this file and re-paste on any change.

**Paste everything between the markers into the claude.ai fantasy basketball
Project → Project instructions.** These ADD to the general custom instructions
in Settings → Personalization (both fire in every project conversation; the
governors — plan-gate, adversarial-verify, scope-fence — still apply here).

---- BEGIN PASTE ----

**Source of truth: the GitHub repos, not project knowledge.** Project
knowledge synced from GitHub is a manual snapshot — it updates only when
David clicks "Sync now" — so treat it as stale by default.

1. **Pull first.** At the start of any conversation that touches draft prep,
   the arena, rankings, lessons, or repo content, fetch the LIVE files before
   answering (the repos are public — plain web fetch works, no connector):
   - Always: `https://raw.githubusercontent.com/nic095layson/yahoo-fantasy-basketball/main/LESSONS.md`
   - Kit index: `https://raw.githubusercontent.com/nic095layson/fantasy-basketball-2026-27/main/README.md`
   - Then fetch whatever specific files the task needs, same URL pattern:
     `https://raw.githubusercontent.com/nic095layson/<repo>/main/<path>`
     (repos: `fantasy-basketball-2026-27`, `yahoo-fantasy-basketball`,
     `claude-core-skills`, `claude`).

2. **If a fetch fails, say so.** Fall back to project knowledge only with an
   explicit label ("from the project snapshot, may be stale") — never present
   snapshot content as current repo state.

3. **No write-back from here.** claude.ai cannot commit, push, or PR — reads
   only (verified 2026-07-13). When work produces anything worth keeping:
   output the COMPLETE updated file in chat so David can save and commit via
   GitHub Desktop, or end with a one-line handoff task for Claude Code. Never
   claim something was "saved to the repo" from this project.

4. **Conflicts resolve toward live state.** If a fetched file contradicts
   project knowledge or chat memory, the fetched file wins; flag the
   discrepancy in one line.

---- END PASTE ----

## Provenance and maintenance

Authored 2026-07-13 (Claude Code session, GitHub-404 follow-up). Grounded in:

- **All four repos made public 2026-07-13.** Anonymous reads verified the
  same day: `raw.githubusercontent.com` returned HTTP 200 for all four repos
  with no auth. This is what makes the pull-first rule executable from
  claude.ai at all.
- **Project GitHub sync is manual.** Files sync only on "Sync now"; no
  refresh at conversation start or on a schedule
  (support.claude.com article 10167454, checked 2026-07-13).
- **claude.ai is read-only toward GitHub** — built-in Projects integration
  and the GitHub connector both; no plan tier unlocks write. Writes require
  Claude Code (any surface) or the Cowork → repo folder → GitHub Desktop
  relay (yahoo-fantasy-basketball LESSONS.md, lesson 9).
- **The pull-first rule is compliance-based, not mechanical.** claude.ai has
  no hook that forces a fetch; the instruction relies on Claude following it.
  That is the strongest mechanism the surface offers today.

Cross-reference: LESSONS.md lesson 9 (Cowork connector token sees zero
repos) predates the repos going public. Public repos likely un-break the
READ half of that failure (anonymous fetch now works); the WRITE half stands.
Retest per the lesson's own protocol in a fresh Cowork conversation.

Re-verify / update when: a repo is renamed or made private again, the GitHub
connector auth is fixed (retest per lesson 9), claude.ai gains write-back or
auto-sync, or a file named in the paste block moves.
