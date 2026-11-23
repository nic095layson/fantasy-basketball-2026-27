# The Runner's prompt copy is current, and Runner-built changes go through the gates (2026-11-23)

Pull window: 2026-11-23 → 2026-11-23 (no pull: kit main 1c6eaa0; the Runner's scheduled task read with `get_trigger` on 2026-11-23).

**Owner's request, verbatim (2026-11-23).** On the Monday ranked list's card of small fixes: "For the remaining 3 decisions on this card, invoke Council to deliberate and proceed with their vote." The Council voted 4-1 to build all three, this one as a single documents pull request (the Contrarian dissented on the rule line: words do not enforce; a checker would).

**Method up front.** Stated to the owner before the change: (B) copy the Runner's live morning prompt into `report/runner/morning_prompt.txt`, extracted mechanically from this session's `get_trigger` result of 2026-11-23 (never retyped), and update the README's `updated_at` and sha256; (C) one sentence each in RULES.md rule 7 and RUNBOOK.md's "What only the owner does". No code changes.

**Verdict. The copy now equals the live prompt (sha256 5f0553d0…, scheduler `updated_at` 2026-11-17T22:12:25Z); its only difference from the old copy is the owner's own edit of 2026-11-17 (two lines on the minutes line).**

Runner impact: none (documents only; the stored prompts are unchanged, as they are edited only from the Runner's own conversation).

Pool rows touched: none

## 1. Checks

| check | result |
|---|---|
| `git diff` of the copy | 2 lines changed, both the 2026-11-17 minutes-line wording; nothing else |
| `sha256sum report/runner/*.txt` | morning 5f0553d0d623abe92e5e66ab9927ffe683ebc3e140a8a89471d652270ddba4ea (README updated); afternoon f7186373… unchanged |

The full suite and gates: below, from gates.py.

## 2. Bounds

Out of scope by design: a checker that refuses a merged change with no gate record (the dissent's ask; a feature for after the owner's fixes-only window).

## 3. Provenance

Session of 2026-11-23 (session model B, continuing the Main session; branch `claude/runner-copy-and-gates-rule`). Re-verify: `sha256sum report/runner/*.txt` against the README table.
