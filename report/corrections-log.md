# Corrections log

Statements a session made to the owner that the records later showed to be wrong, each with how it was caught and the
check that would have prevented it. Append-only; a row is never edited or removed. The Monday review reads this file
and reports any pattern (owner's card, 2026-11-12). A session adds a row in the same pull request as its next change,
or proposes it in the Monday report.

| Date | What was said | What the records showed | How it was caught | The check that prevents it |
|---|---|---|---|---|
| 2026-11-11 | The team-rename step failures "will recur whenever a manager renames" | The fix was already merged (95cf5a3 on 10-29, 7a974cf on 11-09); both days replay PASS | `git log -S` on the two scripts, then a replay | Before calling a failure open, search the history for its fix and replay the failing day |
| 2026-11-11 | The IL-return step runs four worlds | It ran six | Reading `run_scenarios` | Count from the code or the record, not from memory of the design |
| 2026-11-11 | The owner "didn't" follow the kit's Portis-for-Braun call and was right to ignore it | The move ledger shows he dropped Braun on 10-24 and added Portis on 10-28 | Reading the league move ledger | Any claim about what the owner did is read from the move ledger first |
| 2026-11-11 | The roster is "guard-heavy" | The deck's positional counter: 7 guards, 8 forwards, 4 centers | The owner's screenshot | Use the positional counter before describing roster balance |
| 2026-11-11 | Lean "keep Dunn for steals" | The leave-one-out run ranked Dunn the cheapest player to lose | The session's own run, after the lean was stated | Run the comparison before stating a lean, or label it as unrun |
| 2026-11-12 | Leaned "wait for the bounce" on Derrick White as possible cold shooting | 11 box scores: full role in close games, reduced minutes in six blowouts, three-point rate unchanged from last season | The box-score split, run at the owner's request | State the lean as unexamined until the game log has been read |
