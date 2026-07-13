# Fantasy Basketball 2026-27 — 9-Cat Draft Kit

A ready-to-fire analysis system for the 2026-27 NBA fantasy season. Authored July
2026; designed to be executed in October 2026, once rosters are final and the draft
slot is known.

## What's here

| File | Purpose |
|---|---|
| [PROMPT.md](PROMPT.md) | The master analysis prompt — research protocol, 9-cat z-score valuation, punt-build math, draft-slot playbook, full deliverables spec. Methodology only; contains no player data that can go stale. |
| [INPUTS.md](INPUTS.md) | Fill-in template. Four ⭐ fields are the only things the prompt can't research itself: injury/news notes, final-roster caveats, **your draft slot**, and league team names. Everything else has defaults. |
| [report/baseline-2026-07.md](report/baseline-2026-07.md) | **The July 2026 baseline analysis** — offseason ledger (Giannis→MIA, Brown→PHI, Ja→POR, the record deadline), early 9-cat tiers, breakouts/fades with mechanisms, all-30-team capsules, punt sketches, and the October verification list. The October run reads this as priors and patches what changed. |
| `report/` | Final kit lands here. The run also writes intermediate research artifacts here, so an interrupted session can resume. |

## How to run it in October

1. **Fill in [INPUTS.md](INPUTS.md)** — at minimum the ⭐ fields (draft slot, league
   team names, any injury/roster news you want verified first). Commit or don't;
   the agent reads the working tree.
2. **Open Claude Code in this repo** and say:

   > Read PROMPT.md and INPUTS.md in full, then execute the mission end to end.
   > Web research is required; do not use training-data rosters.

3. **Wait.** It's a long run (research across all 30 teams, then valuation, then the
   playbook). The kit lands at `report/2026-27-draft-kit.md`, ending with a one-page
   draft-day cheat sheet.
4. **Skim the front matter first** — it lists every assumption the run made where
   INPUTS.md was blank, so you can correct and re-run cheaply.

Best timing: within a week of your draft, after opening-night rosters firm up
(late-camp cuts happen ~Oct 18-20; NBA opening night is typically the third week of
October). Running earlier is fine — the prompt forces fresh research either way —
but you'd want a quick re-run for late injury news.

## Re-running / updating

The prompt is idempotent by design: every run re-verifies rosters and injuries as of
its own run date. To refresh after news breaks, just run it again — or ask for a
targeted update ("re-run Pass C and update the injury ledger and cheat sheet").
