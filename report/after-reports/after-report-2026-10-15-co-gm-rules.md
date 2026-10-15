# After-report — 2026-10-15: Session 1 item 1 — RULES.md and OPEN.md in both repos; one gate runner writing gates.json

**Owner request (2026-10-15, the Session 1 prompt, item 1):** "RULES.md + OPEN.md (both repos); scripts/gates.py writing gates.json." Plan: `report/plans/co-gm-self-audit-2026-10-15.md` §4 D2, D3; §6 item 1.

**What changed.** Kit: `RULES.md` (37 lines, the 10 rules of the Session 1 prompt plus the L1 urgency rule), `OPEN.md` (master: 3 DISPUTED results, the open owner decisions, the two owner inputs requested today), `scripts/gates.py`, `scripts/test_gates_runner.py`, `gates.json`. Deck: the same `RULES.md`, and an `OPEN.md` that points to the kit's master. No line, tag, team, price or placement changed on either plane; nothing published.

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

EVIDENCE: `test_gates_runner_red.txt` — 9 tests, 4 failing on the naive runner (test_exit0_with_empty_log_is_fail, test_overall_verdict_fails_if_any_gate_fails, test_changed_input_is_refused, test_failing_record_is_refused); `test_gates_runner_green.txt` — 9 tests, 0 failing. The real CLI was driven red on a stub report (`gates_cli_red.txt`): 3 of 3 report gates FAIL, runner exit 1, `--verify` exit 1. This PR's own `gates.json` (green) is quoted in the PR body.

## Watchlist

- `gates.json` binds to the report's sha256; any edit after the gates run makes `--verify` refuse it, so gates run last, after the final edit.
- The merge refusal is procedural until the stop hook lands (P1, D1/D-SA-6): today it is `gates.py --verify` run before each merge.

## Open-item receipts

| item | query run (2026-10-15) | dated finding |
|---|---|---|
| (this item) | records only; no web research and no roster pull | governance files and a gate runner; the pool is unchanged |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this item (did not check) |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 beb243ef57af), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 33 of 33 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 32 of 33 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 23 of 33 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 14 of 33 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 33 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| John Collins | 12 of 33 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 11 of 33 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 10 of 33 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 10 of 33 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 7 of 33 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 6 of 33 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 33 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 33 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (17 mocks, value 27, market 45); Lauri Markkanen (15 mocks, value 21, market 37); Tyrese Haliburton (13 mocks, value 7, market 12); Tyrese Maxey (11 mocks, value 5, market 9); Kel'el Ware (10 mocks, value 57, market 77); Tyler Herro (9 mocks, value 51, market 69); Karl-Anthony Towns (8 mocks, value 12, market 15); Miles Bridges (5 mocks, value 96, market 98).

The section above is today's output of the deck's `repeat_market_check.py` on the page (sha256 beb243ef57af), pasted unedited (`rn_section.md`; run record `rn_run.json`).

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
