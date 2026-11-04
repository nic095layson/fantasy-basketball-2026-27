# Prompt for the main session: the turn gate treats a scheduled run as a turn of its own

Paste everything below the line into the main session.

---

**Build order from David (owner pick 2026-11-03, decision A option 1 of `after-report-2026-11-03-runner-window.md`): make the governance turn gate treat each scheduled-trigger run as the start of a new turn, so it judges that run on its own. Today it judges a scheduled run against the owner's previous message.**

Read first, on season/daily: `report/after-reports/after-report-2026-11-03-runner-window.md` (Finding 1 and the owner's picks at the bottom).

Governance: load plan-gate before your first edit and adversarial-verify before you report. Show David the compact plan (Goal · Method / parameters · Done when · If it breaks) before building. Build on a claude/ branch off main and open a PR. Do not merge it, and do not touch season/daily.

## The defect (EVIDENCE, code at season/daily 27f4fee)

- `hooks/turngate.py:65-77` `owner_index()` returns the latest owner row. It skips rows whose text contains a `HARNESS_MARKERS` string (`hooks/govclass.py:65`), and that list includes `"[SYSTEM NOTIFICATION"`.
- Every caller then treats "everything after `owner_index`" as the turn:
  - `hooks/governance-enforce.py:76` (F1, the Stop gate)
  - `hooks/turn-gates-pretool.py:40` (F2/F3)
  - `hooks/governance-trigger.py:57,62`
- A scheduled run never moves that index, so a scheduled run plus the owner's previous turn are judged as one span. Two failures follow:
  - **False block, observed 2026-11-03 23:06Z.** The afternoon run loaded plan-gate before step 1, but the Stop gate still blocked. The span began at the owner's earlier "Commit the prompt to the repo too" turn, whose push (709a15f) came before that turn's plan-gate.
  - **False pass, by the same logic, not yet observed.** If the owner's previous turn loaded both governors before its outward action, a scheduled run that skips both still passes.

## What a scheduled run looks like in the transcript (EVIDENCE, this session's transcript, checked 2026-11-04)

This is how the 11-03 and 11-04 runs arrived:
1. Harness rows of `"type": "attachment"` (deferred-tool deltas, date changes, file notices). These are not owner text.
2. An assistant row that calls `ReadNotifications`.
3. A `user` row holding that call's `tool_result`. Its text starts with `[SYSTEM NOTIFICATION - NOT USER INPUT]` and contains one header line per notification, for example:
   `--- Notification 1 of 1 · id: dfc64dcd-… · origin: scheduled trigger (the stored prompt of a routine or task on this account) · queued at: 2026-11-04T13:04:18Z · reached this session 3s before this read ---`

**Trap (EVIDENCE):** the same tool_result also has a fixed explanatory paragraph that contains the words *"A scheduled trigger is a stored prompt"*. A plain `"scheduled trigger"` substring match would therefore fire on every ReadNotifications result, including GitHub-only ones. Match the header form only: a line starting `--- Notification ` that contains `· origin: scheduled trigger`.

**Known-answer check, run by the runner on 2026-11-04 over this session's 40 ReadNotifications results:**
- The header regex `^--- Notification .*· origin: scheduled trigger` (multiline) matched 33.
- The 7 it did not match are all `origin: GitHub activity on a subscribed PR`.
- The plain substring `scheduled trigger` matched all 40, so it would have marked 7 false boundaries.

## What to build

1. A `turngate.turn_start(rows)` function that returns the larger of:
   - `owner_index(rows)`
   - the index of the last `tool_result` row (any tool) whose text has a `--- Notification … · origin: scheduled trigger` header line
2. Callers that need "this turn" (`governance-enforce.py` F1, `turn-gates-pretool.py` F2/F3) use `turn_start`.
   - `governance-trigger.py` classifies the owner's *prompt text*, which a scheduled run does not have. Decide whether it should classify the stored-prompt body, or stay as it is, and say which and why in one line to David before building.
3. Fixtures in `hooks/selftest-turn-gates.py`, red first: run them against the current code and show they fail before the fix.
   - **Replay of 2026-11-03 23:06Z:** owner turn with push before plan-gate → scheduled notification → plan-gate → commit → adversarial-verify. Expect PASS (today: BLOCK).
   - **Crafted skip:** owner turn with plan-gate, verify, then push → scheduled notification → commit with no governor. Expect BLOCK (today: PASS).
   - **GitHub-only notification** (origin not "scheduled trigger") → no boundary; the owner's turn span is unchanged.
   - **Explanatory paragraph present but no scheduled header** → no boundary (this guards the trap above).
4. **Where the hooks come from.** These hooks are ported from the library (`nic095layson/claude-core-skills`; see commits 4e883f9, 1d3a40e, 9dbbc3d).
   - If the session has the library attached, make the fix there first and port it with a "Sync … from the library" commit, as before.
   - If it does not, build in the kit, and say in the PR and to David that the kit's `hooks/` now differs from the library and the library needs the same patch. Do not claim the library was updated.

## Done when

- The four fixtures pass with the fix, and the first two fail on the old code (red-first output shown).
- The existing hook selftests all pass: `selftest-turn-gates.py`, `selftest-governance-classify.py`, `selftest-reminders.sh`, `selftest-receipt-law.sh`.
- No change to the governor list, the outward-action list, or the trigger classifier, apart from item 2's stated decision.
- The PR is open and unmerged, with an after-report in `report/after-reports/`.

## If it breaks

- If a real transcript row differs from the shape above (another field, or the header text changed), stop and report the row shape. Do not widen the match beyond the header form.
- If the library is not reachable, follow the kit-only path in item 4 and flag the divergence.

## Report back

One bold outcome line, then:
- a before→after table of the four fixture verdicts
- the selftest results
- the PR link
- whether the library was patched or the divergence was flagged
- item 2's decision

Commits use the neutral label "Claude (session model A)". No model names.
