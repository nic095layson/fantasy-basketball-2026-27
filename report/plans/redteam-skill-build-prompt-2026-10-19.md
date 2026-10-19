# Build prompt — the `red-team` governor for all Claude operations

Paste everything below the line into a Claude Code session opened on `nic095layson/claude-core-skills`.
Written 2026-10-19 by the fantasy-basketball kit session that authored the candidate skill (claude-core-skills PR #25)
and the reference implementation (fantasy-basketball-2026-27 PR #128, `scripts/redteam/`).

---

You are working in `nic095layson/claude-core-skills`, the governance library whose skills shape how every Claude session
of mine plans, verifies, scopes and learns. Your task: take the **candidate** `red-team` skill on branch
`claude/red-team-skill-2026-10-19` (draft PR #25) from candidate to a governor that fires on its own across my Claude
operations, with the measurements the library requires before anything becomes always-on. Read this whole prompt, then
`CLAUDE.md`, `README.md`, and the skills `architecture-contract`, `skill-authoring`, `research-methodology`,
`adversarial-verify`, `plan-gate` and `scope-fence` before you act. Emit your plan-gate to me before the first
consequential action. Do not merge anything; I merge.

## Why this skill exists (the incident, so you build for the failure and not the description)

In `nic095layson/fantasy-basketball-2026-27`, a 9-category fantasy-basketball engine passed three months of audits:
z-scores re-derived to the last digit, two implementations in exact parity, every projection fact-checked against two
outlets, gates on every report. The draft post-mortem of 2026-10-19 (`report/after-reports/after-report-2026-10-19-draft-postmortem.md`)
then found that one hand-set simulator constant (`TEAM_WEEK_SHOCK = 0.06`, a shared games-played shock, never fit to
anything) moved the owner's quoted title share by **+3.4 / −2.3 points**, while every report had quoted that share as
**±0.4**. Second finding: the engine had changed between the report's records and the report (18-week fixed bracket to
17-week reseeded) and nothing said so. Why it went undiscovered: every audit tested *implementation against
specification*; a judgment constant cannot fail a test of itself; two copies of the same model agree whatever the model
is worth; "we checked" was true of the arithmetic and false of the assumptions. `adversarial-verify` grades a
deliverable against its criteria. The red team attacks the thing the deliverable is computed *from*, and keeps attacking
it as a standing fixture.

## What already exists (read it; do not rewrite it from memory)

1. The candidate skill: `.claude/skills/red-team/SKILL.md` on branch `claude/red-team-skill-2026-10-19` (lints PASS,
   description 997 chars / 147 words, guard PASS before and after). Its law: a registry of judgment constants with a
   calibration status (`settings | structural | measured | declared_band | uncalibrated`); a known-answer
   re-implementation by a **separate attacker** who has not read the code; a one-at-a-time assumption sweep with
   **structural bands** and tiers (ROBUST / SENSITIVE / FRAGILE); decision robustness under the sweep; an **engine
   fingerprint** on every record (STALE fails); an **append-only numbered attack list**; every headline figure carries
   **two error bars** and quotes every FRAGILE band or fails its gate; a proportionality valve.
2. Its pre-registered evals and hypothesis: `evals/red-team.json` (ids 1, 2, 3, 6 should-fire; 4, 5 should-not;
   gate ≥5/6 fire, 4/4 silent, N≥2) and `experiments/hypothesis-2026-10-19-red-team.md` (NOT YET RUN).
   README candidate section and `evals/model-capability-register.md` row 13 are in place.
3. The reference implementation, in the kit repo `nic095layson/fantasy-basketball-2026-27`, branch
   `claude/market-data-workorder-mnfi2b`, folder `scripts/redteam/`: `constants_registry.json`, `check_constants.py`
   (registry vs live engine, fingerprint), `sweep.py` (bands one at a time, tiers), `check_bands.py` (report must quote
   FRAGILE bands), `attacks.json` + `run_attacks.py` (numbered, STALE/MISSING fail), and `scripts/gates.py --redteam`
   which makes the three checks gates; 29 red-first tests in `scripts/test_constants_registry.py`,
   `test_redteam_sweep.py`, `test_redteam_attacks.py`, `test_gates_runner.py`. Reports:
   `after-report-2026-10-19-redteam-standing.md` (what was built, D-RT-1..5) and
   `after-report-2026-10-19-retro-redteam.md` (the skill used once: the findings changed the odds, not the names).
   Attach that repo read-only if you need to read these; do not change it.

## What to build (the scope; flag anything beyond it, do not absorb it)

**A. Measure the candidate before touching its wording.** Run the trigger evals as pre-registered
(`experiments/hypothesis-2026-10-19-red-team.md`): Claude Code headless (`claude -p`), fresh session per run, the skill in
the loaded list, N≥2 per prompt, record FIRED/SILENT by the Skill-tool invocation in the stream-json transcript, results
to `results/2026-<date>/red-team-trigger-evals/` with the raw transcripts beside the summary. If the gate fails, the fix
is a `description:` edit under `research-methodology` (pre-register, A/B, N=2 floor, any-regression-blocks), never a
body edit for a trigger miss. Report the measured rates as rates.

**B. The general-purpose tooling, so the skill is executable outside fantasy basketball.** A small, dependency-free
Python toolkit under `.claude/skills/red-team/scripts/` (the library ships scripts this way; see
`diagnostics-and-tooling/scripts/`), generalized from the kit's `scripts/redteam/` with every fantasy-basketball
specific name removed:
- `registry_check.py`: reads a project's `redteam/constants_registry.json` and a project-supplied `live.py` (or a
  `--live JSON`) that reports the live values; fails on drift, unregistered live constant, registered-but-gone, a
  status outside the five, a `measured`/`declared_band`/`settings` entry with no record, an `uncalibrated` entry with no
  decision id. Prints `CONSTANTS CHECK: PASS — …` / `FAIL` + problems. Exit 0 / 1.
- `attacks_check.py`: reads `redteam/attacks.json` (id, name, question, script, record, commit_field, added, retired);
  fails on MISSING record or script, STALE (record's commit ≠ live fingerprint from `git rev-parse --short HEAD` or a
  `--fingerprint` value), DUPLICATE id; UNFINGERPRINTED allowed and counted; `--out` writes the numbered artifact.
- `bands_check.py`: reads a sweep record (`constants.<name>.{tier, variants[].{label, shift_mean}}`, `fragile[]`) and a
  report; fails unless every FRAGILE constant is named, the word FRAGILE sits within 400 characters of it, and each
  variant's signed one-decimal shift appears (unicode minus accepted). The sweep itself stays project-specific: ship a
  `sweep_template.py` that shows the contract (reload the module per job, patch one constant, assert the baseline
  within 3 SE of the published reference before any tier is read, two seeds, tiers on the unrounded mean, record the
  fingerprint and the tier rule), not a runner that pretends to know the project's simulator.
- `redteam_init.py`: scaffolds `redteam/constants_registry.json`, `redteam/attacks.json` and a `redteam/README.md` in
  a project, with the five statuses documented and an example entry per status.
- Red-first tests beside them (`tests/test_redteam_scripts.py` or the library's convention): stale value fails,
  unregistered fails, uncalibrated without decision fails, STALE record fails, report missing a FRAGILE band fails, good
  cases pass. Each test must be seen red before green; say so in the PR body with the output.

**C. The enforcement layer, per surface** (`install-and-surfaces` and `hooks/README.md` decide what is possible).
- Claude Code: a hook under `hooks/` that fires when a session is about to deliver a report containing a headline
  figure from a model and no band sentence, modeled on `hooks/plan-gate-first-write-reminder.sh` (a reminder, not a
  block, unless the library's hook doctrine says otherwise). Pipe-test it like the existing hooks; pre-register its A/B
  in `experiments/`.
- claude.ai: add the red-team law to `instructions/claude-ai-custom-instructions.md` in the carrier's existing shape (the
  owner re-pastes it; say so in the PR). Keep the paste block within whatever size the carrier already respects.
- Both: the skill's "Proportionality" section is the anti-ceremony valve; a hook that fires on every number is a
  regression (architecture-contract invariant 5).

**D. Library bookkeeping.** README: move `red-team` from "Candidate" to whatever status the measurements earn (the
README's own words, not a new tier); `evals/model-capability-register.md` row 13 superseded by a dated row with the
measured rates (append, never rewrite); `.claude/LESSONS.md` gets the incident as `INC-2026-10-19-nn` (symptom → root
cause → evidence → status; cite the kit after-reports by path); the skill's "Volatile facts" status line updated with
the eval date. Run `bash .claude/skills/diagnostics-and-tooling/scripts/guard_essentials.sh` before and after; both
outputs in the PR body. `lint_skill.sh` on the skill after any edit.

## Rules that bind you here

- **Do not edit the skill body to fix a trigger result**, and do not edit the description without the research-
  methodology protocol. The candidate's wording is the pre-registered variant; measure it first.
- **No repo-specific facts in the governor's procedure** (architecture-contract Decision 2 corollary). The kit is
  lineage in Provenance, not a step in the procedure.
- **Red-first for every script and hook**: the test or pipe-test fails before the code exists and passes after.
- **Two runs where cheap**; aggregates from records never from recall; every "couldn't" names what was attempted.
- **Nothing becomes always-on by your decision.** Your PR proposes; the README's Decision-5 review and I dispose.
- **Deletions** are declared in `.guard-acknowledged-deletions` or the guard fails; never renumber a ledger entry.
- Keep the PR to this scope. Anything else you notice (and you will) goes in the PR body under "Out of scope, flagging".

## Deliverable

One draft PR on `nic095layson/claude-core-skills` built on top of branch `claude/red-team-skill-2026-10-19` (merge
`main` into it first; do not rebase it). PR body: the plan-gate you emitted; the eval results as rates with the results
directory; the scripts and their red-then-green test output; the hook's pipe-test; the guard before/after; the lint;
what you changed in the README, register and ledger; the "Out of scope, flagging" list; and an honest status line per
adversarial-verify's delivery shape (criteria, refutation, regressions, gaps, status). I merge only on my word.

## Acceptance (I will grade against exactly these)

1. Trigger evals run as pre-registered, N≥2, raw transcripts committed, rates reported; gate met or a pre-registered
   description edit proposed with its own A/B.
2. The four scripts exist, lint, and their red-first tests pass; a fresh session given only the skill and
   `redteam_init.py` can scaffold a project and run the three checks without reading the kit.
3. The Claude Code hook pipe-tests; the claude.ai carrier carries the law; neither fires on a conversational answer with
   no model behind it (one negative case each, recorded).
4. README, register, ledger and the skill's volatile-facts line agree with each other and with the results directory.
5. Guard PASS before and after; lint PASS; no deletions outside `.guard-acknowledged-deletions`.
6. Nothing in the kit repo changed; nothing merged.
