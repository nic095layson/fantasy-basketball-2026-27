# Independent-audit adoption: morning preflight, claim receipts on every report, deck replay on real mornings — 2026-10-21

Pull window: 2026-10-21 → 2026-10-21 (build only; no roster pull, no box scores, no projection line, tag or roster changed).

**Owner's request.** "Can you audit the several errors and failures from the past 2 days … are there meaningful fixes and safeguards we can build?", then "Build all the recommended, then red team to confirm the integrity and effectiveness", and mid-build: "This is not just for Fantasy Basketball, but Claude Global." The safeguards were therefore built as a library skill, `independent-audit`, in `nic095layson/claude-core-skills`; this kit is its first project instance. "Build" means build: merging stays the owner's word.

**What was analyzed.** Kit `main` `55f950c`; the kit's 15 after-reports of 10/19–10/21, its run ledger and git history (the 21-failure inventory); the real 10/20 and 10/21 deck records.

**Method.** Stated to the owner before the build:
- the three recommended safeguards (independent auditor, real-input replay, unattended-run preflight); the nice-to-have (a known-answer rule for every new checker) is not built;
- each piece red-first against a recorded incident, then a red team (library `results/2026-10-21/independent-audit/REPORT.md`).

**Headline.**
- **The morning run now checks its own preconditions first.** Step 0 is a preflight (`scripts/independent_audit/morning_preflight.json`): kit checkout, the deck repo beside the kit, the render browser, writable briefs, a reachable remote. A missing one prints one FAIL line and stops the run, instead of a half-run that publishes no deck (the 10/21 runner reported "deck still missing").
- **Every after-report's claims are linted (advisory).** `gates.py` adds a `claim receipts` gate that lists sentences saying something runs or changes nothing with no receipt beside them. It never fails the build: its precision on this kit's own reports was 3 of 7 when first measured, under the 0.5 bar set beforehand.
- **`gates.py --replay` rebuilds the Season Deck on the last 3 real mornings** and opens each in a headless browser. On the real 10/21 morning the deck code from before #152 crashes (no matchup file) and the code from before #154 builds a page with no tabs; today's code passes both mornings.
- **Not covered by anything here:** the 10/20 no-checkout failure itself. A run with no checkout cannot run `morning.py`, so its guard belongs in the scheduled task's prompt (decision 2).

---

## 1. Roster changes

None. This build changes no roster, line, tag or engine constant.

## 2. What was built

| piece | file | red-first evidence |
|---|---|---|
| preflight step 0 | `scripts/morning.py`, `scripts/independent_audit/morning_preflight.json` | `test_independent_audit_adoption.py` 4 of 6 failing before the build; the first spec looked for `hoops.py` at the deck root and FAILED this correctly set-up kit — the checker was wrong, fixed, and a pass control now pins it |
| claim receipts gate | `scripts/gates.py` `audit_gates()` | gate list test red then green |
| deck replay | `scripts/gates.py --replay`, `scripts/replay_deck.sh` | replay of three deck versions on the real 10/20 and 10/21 records: before #152 1 of 2 FAIL, before #154 1 of 2 FAIL, current 2 of 2 PASS |
| vendored scripts | `scripts/independent_audit/{claim_receipts,replay_gate,preflight}.py` | byte-identical to the library copies; a test fails on drift when the library sits beside the kit |

Two existing tests in `test_morning.py` pinned the step order; they were updated, with a dated note, because step 0 moved every index by one.

## Watchlist

- **Tomorrow's 05:53 PT runner fire** runs the preflight first once this merges. If its container lacks the deck repo or playwright, the run now stops at step 0 with a named FAIL instead of publishing no deck.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| morning preflight (step 0, fatal) | **BUILT**, this PR; not merged | `scripts/test_independent_audit_adoption.py` red then green; PASS in this kit, FAIL outside it and with the deck missing |
| claim receipts on every report (advisory) | **BUILT**, this PR; not merged | gate `claim receipts` in `gates.json` |
| deck replay (`gates.py --replay`) | **BUILT**, this PR; not merged | pre-#152 and pre-#154 deck code FAIL on the real 10/21 morning; current code PASS 2 of 2 |
| Movers fix, render check (#154) | **MERGED** | `55f950c` |
| 7 risk rows, calibration date, evening routine, old routine | open, the owner's | GAUNTLET report decisions 2, 3, 5, 6 |

The flagged-name receipts are carried forward from the lock report. This build pulled nothing and researched no player, so they were not re-queried (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this build (did not check) |

## Repeat-name market check

This build did not change the deck page, which is still deck `80eecdf`, page sha256 6a5cefea4921. The GAUNTLET report replayed it today. Its table stands, carried here verbatim.

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 6a5cefea4921), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 33 of 33 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 32 of 33 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 23 of 33 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 14 of 33 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 33 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| John Collins | 11 of 33 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 10 of 33 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 10 of 33 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 9 of 33 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 7 of 33 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 7 of 33 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 33 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 33 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (17 mocks, value 27, market 45); Lauri Markkanen (15 mocks, value 21, market 37); Tyrese Haliburton (13 mocks, value 7, market 12); Tyrese Maxey (11 mocks, value 5, market 9); Kel'el Ware (10 mocks, value 57, market 77); Tyler Herro (9 mocks, value 51, market 69); Karl-Anthony Towns (8 mocks, value 12, market 15); Miles Bridges (5 mocks, value 96, market 98).

## Decision sheet

1. **Merge this PR** (the kit's adoption). Merging is your word.
2. **The no-checkout guard belongs in the scheduled task's prompt**, not in `morning.py`. Proposed first line of the runner's stored prompt: `test -f fantasy-basketball-2026-27/scripts/morning.py || { echo "PREFLIGHT: FAIL — no kit checkout; attach nic095layson/fantasy-basketball-2026-27"; exit 1; }`. Changing a scheduled task is yours to approve; nothing was changed.
3. **Claim receipts stays advisory** until a fresh precision measurement on reports it has not seen clears 0.5; then it can become a blocking gate. Your call when.
4. **Use the independent auditor before the next large merge** (library skill, `auditor-brief.md`).

## Bounds

**Out of scope by design.**
- The nice-to-have checker rule; any engine, line, tag or roster change.
- The deck repo, which this build does not touch.

**In scope and unverified.**
- **The preflight inside the runner's own container:** NOT-ATTEMPTED, it cannot run there before this merges; tomorrow's fire shows it.
- **Replay over more than two mornings:** only 2 mornings have produced a deck so far (10/20, 10/21); the gate replays the last 3 as they accumulate.

## Provenance

- **Session:** Claude Code (cloud) "Claude Global Operations", 2026-10-21, after the failure audit of the same day.
- **Library:** `nic095layson/claude-core-skills`, skill `independent-audit`, report `results/2026-10-21/independent-audit/REPORT.md`.
