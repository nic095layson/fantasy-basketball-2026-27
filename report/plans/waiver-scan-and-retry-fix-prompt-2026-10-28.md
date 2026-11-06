# Prompt for the main session — waiver-scan availability and Flaim retry (2026-10-28)

Written by the runner session at the owner's request. Paste the text below into the main Fantasy Basketball session.

---

Diagnose, research and fix two findings from the persistent runner session (owner 2026-10-28). Governors: load anthropic-skills:plan-gate before acting, anthropic-skills:adversarial-verify before delivering, and anthropic-skills:red-team before quoting any title or win figure that a fix moves. The doctrine applies:
- No projection line, injury tag or engine constant changes without my explicit pick.
- Method parameters are stated to me before the run that uses them.
- Decisions come to me as 2–4 clickable options, recommended first.
- Never merge PR #165 "Season: daily records". Work on a branch off main and open a draft PR.

READ FIRST, IN THIS ORDER (on origin/season/daily, at 4559da0 or later)
1. report/after-reports/after-report-2026-10-28-morning-run-v3.md — the runner's report. It is your starting point, not your evidence: re-verify every EVIDENCE line yourself and treat every INFERENCE line as a hypothesis to test.
2. report/briefs/morning_report_2026-10-28.md and report/briefs/brief_2026-10-28.json (waiver_top, streaming).
3. data/source/flaim/pull_2026-10-28.json (the pinned Yahoo responses: rosters, the 100-player available list with status letters, transactions).
4. scripts/co_gm.py (free_agents, waiver_pairs, streaming), scripts/daily_brief.py (around lines 160–205), scripts/week_matchup.py (yahoo_free_agents, around line 510), scripts/status_feed.py (TIERS), and hoops.availability in the deck repo.

THE FINDINGS AS REPORTED (verify them; do not assume them)

A. The waiver scan and the streaming list can recommend players who cannot be claimed or cannot play.
- co_gm.free_agents() builds candidates as: every pool player not on a league roster, with hoops.availability(p) > 0 (the kit's tag), and not on the do-not-draft list.
- It never consults Yahoo's available-player list or Yahoo's status for unrostered players.
- On 10-28 the brief's top pair was "add Jalen Williams, drop Gillespie: +0.144 cats/week, title 37.3% (+4.7)":
  - Yahoo showed him O in the 10-27 pulls, the day MAXEY-MUM dropped him (transaction tr.85).
  - He is absent from the 10-28 Flaim available list.
  - He has no kit tag change since 10/14.
- The 2nd pair's add, Cameron Johnson, shows D on Yahoo's list.
- daily_brief.py:199 builds the streaming list from the same fa, so streaming has the same exposure.
- week_matchup.yahoo_free_agents() already maps Yahoo's list against the pool and sets Out players aside. It is a precedent you may reuse, not a mandate.

B. One transient Flaim error halts the manager log.
- The 10-28 dated get_roster for team 5 (as_of 2026-10-27) returned a Cloudflare 502 marked retryable (retry_after 60).
- The morning prompt v3 allows one retry only on YAHOO_AUTH_UNAVAILABLE, so the runner did not retry.
- MANAGER LOG: HALT — 11 of 12 locked lineups for 2026-10-27; the day is not in the profile.

BE SELF-CRITICAL: WHAT THE RUNNER GOT WRONG OR LEFT OPEN (check each)
- The runner reported the brief's top waiver pair every morning since 10-24 without checking that the add was on Yahoo's available list or healthy. 10-28 is the first day it flagged one. Treat every earlier reported pair as unaudited.
- Its claim that "no kit tag means full availability" is read from co_gm.py and has not been tested. Confirm how hoops.availability treats an untagged player before building on it.
- In the 10-27 run it issued get_standings and a dated get_roster in the same tool block. The one-at-a-time rule names get_roster calls, so this probably complied, but say whether you agree.
- Its first after-report draft miscounted the run's calls (49 instead of 31), and its morning report carried an unsupported line until a follow-up commit. Re-derive any count you quote from the files.
- The owner said in the runner conversation on 10-26 that Jalen Williams is out for the season. That statement is not a run input and nobody verified it. Do not treat it as evidence; research it.
- It did not check whether Yahoo still serves the 10-27 dated lineup for team 5, or whether a failed day can be back-filled.

PHASE 1 — DIAGNOSE AND RESEARCH (read-only; write nothing to the repo)
1. Reproduce A from the pinned 10-28 inputs. Rebuild fa exactly as daily_brief does, show Jalen Williams in it with his availability value, and show he is absent from the Flaim available list. Quote file:line for every step.
2. Map the blast radius: every reader of co_gm.free_agents or a fa built the same way (brief waiver scan, streaming, the deck's Free Agents and Today tabs, Trade Analyzer inputs, anything else). For each, say whether it is affected.
3. Audit history: for each morning brief since 10-20, check whether the top-3 waiver adds and the streaming list were on that day's pinned Flaim available list, and what Yahoo status they had. Build the table from the pinned files, not recall.
4. Research Jalen Williams's current status from primary sources (team or league injury report, reputable outlets). Date every source. If you have no web access, say so and mark it NOT-ATTEMPTED with the reason.
5. For B, check:
   - Flaim's error shape for 5xx versus YAHOO_AUTH_UNAVAILABLE.
   - Whether a dated as_of_date roster can be pulled days later (test one past date read-only if allowed).
   - What manager_log.py does with an 11-of-12 day.
6. State, before Phase 2, every method parameter a fix would introduce (for example: which Yahoo status letters map to which availability, whether D or Q candidates stay in the scan with a discount, the retry wait and count). Give each one's basis.

PHASE 2 — OPTIONS (AskUserQuestion; stop here until I pick)
For A, at least:
  1. (likely recommended) Restrict candidates to the day's Flaim available list and apply Yahoo status through status_feed.TIERS, reusing yahoo_free_agents. One mechanism covers the waiver scan and streaming. Show the fallback when the pull is missing or incomplete (the kit must never invent availability).
  2. Keep pool-based candidates, but drop any player not on the Flaim list and apply status. Same effect, different code path.
  3. Leave the scan as is and add a brief/deck flag on any pair whose add is not on Yahoo's list.
For B, at least:
  1. (likely recommended) One retry for retryable 5xx after retry_after (cap ~60s), never parallel. This is a morning and afternoon prompt edit; show the exact text diff.
  2. Keep the rule and accept HALT days.
  3. Add a next-morning back-fill of missing dated lineups (only if Phase 1 shows Yahoo still serves them).
Give each option its tests and its cost.

PHASE 3 — BUILD (only the options I pick)
- Red-first tests:
  - A Yahoo-Out unrostered player never appears in waiver_top or streaming.
  - A player absent from the available list never appears.
  - A D/Q player is handled as the picked option says.
  - A missing pull halts loudly instead of silently falling back to the pool.
  - All existing tests stay green.
- Re-run the 10-28 brief from the pinned inputs, before and after the fix. Report how the top-3 pairs, the streaming list and title odds change. Quote title shares with their sampling error and the structural band (red-team: name any FRAGILE constant).
- If B option 1 is picked: draft the exact new step-3a text for both runner prompts and show me before/after. Applying it is a separate owner go, done in the runner conversation, which is the one the tasks post into.
- Write one after-report in report/after-reports/: what changed, what it fixes, what it does not fix, and each gap with its provenance.
- Then report back in short: the findings confirmed or refuted, the audit table, the options built, test output, the before/after on the 10-28 brief, the PR link, and anything left open.
