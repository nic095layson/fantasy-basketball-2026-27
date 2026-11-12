# Trimming ceremony that verified nothing (owner 2026-11-12, on the council's verdicts)

Pull window: 2026-10-17 → 2026-11-12 (no pull: the kit at main 1613629, the 25 morning records and the report folder on the records branch at 0e21df1, this session's own record and the account's scheduled-task list, read only).

**Owner's request, verbatim:** "can you please conduct system wide check for any operations or system churn that has proved to be theatrical only and non-essential, non-contributional? Flag them to me and suggest what is no longer needed / can be terminated". Then, on the options card: "Have council deliberate on all these, and proceed with their verdicts."

**Method up front.** The test for "theatrical", stated before the check: nothing reads the output, or the output has been empty or identical every time, or it repeats a check made elsewhere. Counts come from the morning records, the report folder and this session's record, not from memory. The council (five roles, one vote each) then ruled on four groups of findings.

**Verdict: the kit's core path is not theatrical. Two things were: report text copied forward to satisfy a gate, and a band sentence required of reports that quote no title odds. Both gates now ask for that text only where the report's content calls for it. One scheduled task was cancelled and two were slimmed. The daily steps were left alone.**

Runner impact: none — the change is to the report gates a main session runs before a merge; no morning or afternoon step, script the Runner runs, or prompt is touched.

Pool rows touched: none

## 1. What was measured

| Finding | Evidence |
|---|---|
| A copied report tail | 196 after-reports since October; 33 carry an identical 4,624-character tail: a watch item dated 2026-11-09 and receipt tables from 2026-10-14 marked "did not check" |
| The band sentence where no title odds are quoted | 51 reports carry the bold sentence; 13 of them quote a title share anywhere else |
| Governance loads on fixed procedures | 50 skill loads in this session on 2026-11-12, 705,662 characters of the same rule text re-sent |
| Daily steps redoing unchanged work | accuracy render wrote the same 2,189-character file each morning; league pairings the same line; both run in under a second |
| ESPN transactions feed | 23 mornings, 3 naming a rostered player; the script already records an unreachable feed and lets the morning go on |
| Tag outcomes | 487 rows, no reader yet; the season-end calibration task is written to read them |

## 2. The council's verdicts and what was done

| Item | Verdict | Vote | Done |
|---|---|---|---|
| Scheduled tasks | Cancel the 2026-11-28 Runner-impact review; keep the week-10 and week-15 confidence re-runs but deliver them in chat with no report or PR; leave the two disabled October tasks (deleting one also deletes the sessions it started, for no saving) | 4 to 1 | Done on the account: one task cancelled, two prompts replaced |
| Report boilerplate | Require the tail and the band sentence only where the content calls for them | 4 to 1 | This PR, section 3 |
| Daily steps | No action: the two repeat steps cost under a second and repair a past fault by themselves; the transactions step already survives an outage | 4 to 1 | Nothing changed |
| Governance loads | A proposal only, three named procedures, no hook changed | 4 to 1 | Section 4 |

A correction to the assessment given in chat before the council: it suggested making the transactions step non-fatal. The script's own text shows an unreachable feed is recorded and the morning continues, so there was nothing to fix.

## 3. The gate change

`report/check_report.py`: a report that states `Pool rows touched: none` on a line of its own does not owe the Watchlist, Open-item receipts and Repeat-name sections, provided the claim holds: neither `report/projections-2026-27.csv` nor `data/pool_additions.csv` differs from origin/main or is modified in the working tree. A false claim fails and names the file; a claim that cannot be checked against main fails. Without the line, the three sections are owed as before. The pull window, the first section, the Runner impact line, the publication rule and the pull-log row are unchanged.

`scripts/gates.py`: for such a report the deck's two receipt gates are not run, since they check the content of sections the report does not owe. Every other report runs all three.

`scripts/redteam/check_bands.py`: the bands are owed when the report quotes a title share ("title" or "championship" within 120 characters of a percentage on one line) or names a FRAGILE constant. A report that does neither passes and says so. This is the rule the script's own first line has always stated. A half-quoted band still fails.

This report is the first written under the new rule: it carries the line above, no copied tail, and no band sentence.

## 4. Proposal for the core-skills repository (not built; the owner decides)

The enforcement hooks require a plan-gate load before, and an adversarial-verify load after, every governed request. On three kinds of request the procedure is fixed and carries its own checks, so the load adds text and no decision:

| Request | The checks the procedure already makes |
|---|---|
| "merge N" on the owner's typed word | head unchanged since the gates ran; `gates.py --verify` PASS; the merge pinned to that commit |
| A deck rebuild after the owner's card pick | each step's PASS line; the published page compared byte for byte with the built file |
| A status read from a record that already exists ("week N update") | every figure read from the named record in the same turn |

Options: (1) exempt these three by name in the hook, keeping the procedure's own checks mandatory (recommended); (2) keep the load and shorten what is re-sent to a one-line reminder; (3) leave as is. What would argue against (1): the three ungoverned weeks of October (INC-2026-10-13-01), which is why the list is three named procedures and not a class.

## 5. Checks

| Check | Result |
|---|---|
| New tests | 6 for the pool line, 3 for the bands rule, 1 for the gate runner; written in the same step as the code, so not seen failing first, except one that caught a fault in the exempt path (a passing claim was reported as a problem) |
| Existing band tests | 3 failed against the first version (they spell "percent", and one tests a half-quoted band); the rule was widened to cover both, and they pass unchanged |
| Full suite | 1,198 tests OK, 2 skipped (was 1,188) |
| Gates | PASS and verified (see the commit) |

## 6. Bounds

Out of scope by design: the deck repository's two receipt scripts (not changed; skipped by the gate runner for exempt reports); the enforcement hooks; the other projects' scheduled tasks.

In scope and unverified:
- Which deck cards and tabs the owner opens: did not check; there is no usage record.
- Whether the run watches have ever sent a real alert: did not check.

## 7. Next steps (owner decisions)

1. Merge this PR, or not.
2. The section 4 proposal: pick an option; it is applied in `nic095layson/claude-core-skills`, which this session cannot write to.

## 8. Provenance

Session of 2026-11-12 (session model A), branch `claude/market-data-workorder-mnfi2b`. Re-verify: `python3 -m unittest test_check_report test_gates_runner test_redteam_sweep` in `scripts/`.
