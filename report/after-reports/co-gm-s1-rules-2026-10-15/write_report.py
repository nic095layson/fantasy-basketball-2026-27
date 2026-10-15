#!/usr/bin/env python3
"""Writer for after-report-2026-10-15-co-gm-rules.md — every figure read from this folder's
records (RULES.md rule 6). Run from the kit root: python3 report/after-reports/co-gm-s1-rules-2026-10-15/write_report.py"""
import hashlib
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DECK = os.path.join(KIT, "..", "yahoo-fantasy-basketball")
OUT = os.path.join(KIT, "report", "after-reports", "after-report-2026-10-15-co-gm-rules.md")


def rd(name):
    return open(os.path.join(HERE, name), encoding="utf-8").read()


def unittest_counts(text):
    ran = int(re.search(r"Ran (\d+) tests?", text).group(1))
    m = re.search(r"FAILED \((?:failures=(\d+))?(?:, )?(?:errors=(\d+))?\)", text)
    bad = (int(m.group(1) or 0) + int(m.group(2) or 0)) if m else 0
    return ran, bad


red_ran, red_bad = unittest_counts(rd("test_gates_runner_red.txt"))
green_ran, green_bad = unittest_counts(rd("test_gates_runner_green.txt"))
red_fails = re.findall(r"^FAIL: (\w+)", rd("test_gates_runner_red.txt"), re.M)
cli = rd("gates_cli_red.txt")
cli_fail_gates = len(re.findall(r"^- FAIL · ", cli, re.M))
cli_exit = re.search(r"^exit=(\d+)", cli, re.M).group(1)
verify_exit = re.search(r"^verify exit=(\d+)", cli, re.M).group(1)
page_sha = hashlib.sha256(open(os.path.join(DECK, "docs", "draft-deck.html"), "rb").read()).hexdigest()[:12]
rules_lines = len(open(os.path.join(KIT, "RULES.md"), encoding="utf-8").read().splitlines())
open_md = open(os.path.join(KIT, "OPEN.md"), encoding="utf-8").read()
n_disputed = len(re.findall(r"^\| X-\d+ ", open_md, re.M))
n_rules = len(re.findall(r"^\d+\. \*\*", open(os.path.join(KIT, "RULES.md"), encoding="utf-8").read(), re.M))
n_cli = len(re.findall(r"^- (?:PASS|FAIL) · ", cli, re.M))
rn = rd("rn_section.md").rstrip() + "\n"
assert green_bad == 0 and red_bad > 0 and cli_exit == "1" and verify_exit == "1"

text = f"""# After-report — 2026-10-15: Session 1 item 1 — RULES.md and OPEN.md in both repos; one gate runner writing gates.json

**Owner request (2026-10-15, the Session 1 prompt, item 1):** "RULES.md + OPEN.md (both repos); scripts/gates.py writing gates.json." Plan: `report/plans/co-gm-self-audit-2026-10-15.md` §4 D2, D3; §6 item 1.

**What changed.** Kit: `RULES.md` ({rules_lines} lines, the {n_rules} rules of the Session 1 prompt plus the L1 urgency rule), `OPEN.md` (master: {n_disputed} DISPUTED results, the open owner decisions, the two owner inputs requested today), `scripts/gates.py`, `scripts/test_gates_runner.py`, `gates.json`. Deck: the same `RULES.md`, and an `OPEN.md` that points to the kit's master. No line, tag, team, price or placement changed on either plane; nothing published.

**Method (stated before the run).** Red-first against a naive runner that trusts the exit code and never re-checks its inputs — the habit behind the 10/15 empty-log near-miss (plan §1). No sample, window or seed: these are deterministic tests.

Pull window: 2026-10-15 → 2026-10-15 (governance files and a gate runner; no roster pull, no web research).

## 1. Roster changes

None. No roster pull in this item.

## 2. What the gate runner refuses

| case | naive runner (red) | `gates.py` (green) |
|---|---|---|
| exit 0, empty log | PASS | FAIL — "exit 0 but no PASS line" |
| PASS text, exit 1 | FAIL | FAIL |
| gates.json older than the report it vouches for | accepted | refused — "changed since the gates ran" |
| gates.json with a failing gate | accepted | refused |
| no gates.json | refused | refused |

EVIDENCE: `test_gates_runner_red.txt` — {red_ran} tests, {red_bad} failing on the naive runner ({", ".join(red_fails)}); `test_gates_runner_green.txt` — {green_ran} tests, {green_bad} failing. The real CLI was driven red on a stub report (`gates_cli_red.txt`): {cli_fail_gates} of {n_cli} report gates FAIL, runner exit {cli_exit}, `--verify` exit {verify_exit}. This PR's own `gates.json` (green) is quoted in the PR body.

## Watchlist

- `gates.json` binds to the report's sha256; any edit after the gates run makes `--verify` refuse it, so gates run last, after the final edit.
- The merge refusal is procedural until the stop hook lands (P1, D1/D-SA-6): today it is `gates.py --verify` run before each merge.

## Open-item receipts

| item | query run (2026-10-15) | dated finding |
|---|---|---|
| (this item) | records only; no web research and no roster pull | governance files and a gate runner; the pool is unchanged |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this item (did not check) |

{rn}
The section above is today's output of the deck's `repeat_market_check.py` on the page (sha256 {page_sha}), pasted unedited (`rn_section.md`; run record `rn_run.json`).

## Bounds

**Out of scope by design.** The SessionStart hook and the stop-hook merge refusal (P1, D-SA-6). No change to any existing gate.

**In scope and unverified.** None. Every claim above comes from a log in `co-gm-s1-rules-2026-10-15/`.

**What this cannot see.** `gates.py` checks that each gate ran and passed on these bytes. It does not check that a gate is the *right* one. That stays a judgment, made in each item's plan-gate.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-S1-1 | Merge policy: I mark each Session 1 PR ready and merge it once `gates.py --verify` passes on its head (your acceptance list says "PR merged"), or you merge | I merge |
| D-SA-6 | SessionStart hook: P1, or pull into Session 1 | P1 |
| earlier rows | carried in `OPEN.md` | carried |

## Provenance

- This folder: `test_gates_runner_red.txt`, `test_gates_runner_green.txt`, `gates_cli_red.txt`, `rn_section.md`, `rn_run.json`, this writer.
- No line, tag or placement changed on either plane; nothing published.

## In plain language

The house rules now live in a file both repos read at the start of every session, instead of only in my memory. The one gate runner will not call a check passed unless the check both exits cleanly and prints its PASS line. It also refuses a pass record once the report it vouched for has been edited. That closes the empty-log near-miss from this morning.
"""
open(OUT, "w", encoding="utf-8").write(text)
print(f"wrote {os.path.relpath(OUT, KIT)}")
