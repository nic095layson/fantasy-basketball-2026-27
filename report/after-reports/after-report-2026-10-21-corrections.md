# Corrections to the system — 2026-10-21 (GAUNTLET, Council 4–1)

Pull window: 2026-10-21 → 2026-10-21 (corrections only; no roster pull, no box scores, no plane change).

**Owner's request.** "Invoke council, then initiate Gauntlet corrections to system",
2026-10-21, following three defects surfaced earlier the same evening.

**What was analyzed.** The kit at `claude/market-data-workorder-mnfi2b` (head
`ed0db79`) and the deck repo beside it; `report/roster-provenance.csv`,
`report/check_provenance.py`, `report/rank_engine.py`, `scripts/season_board.py`,
`scripts/morning.py`, `report/plans/co-gm-self-audit-2026-10-15.md`,
`arena/data/weekly_matchups_2025-26.csv` and its README, and the two scheduled
tasks (`trig_015cdR…`, `trig_0192N7…`).

**Method.** Council (4–1) set the order; plan-gate block emitted before the first
edit; every claim below is either a command run tonight (EVIDENCE) or marked
INFERENCE. The Council's one open unknown was closed by lookup before any
recommendation was written.

**Headline.** The three defects are one pattern: **statements the system makes
about itself, with no live counterpart.** Closing the open unknown also
*withdrew* the recommendation this session had been carrying — in-season team
labels are verified by nothing, so "retire the age flag, live verification
supersedes it" was wrong. Two zero-risk corrections landed; the gate decision is
rebuilt and returned to the owner; a claim-vs-reality checker is built and
deliberately unwired.

---

## 1. The closed unknown — nothing verifies team labels in-season

**EVIDENCE (2026-10-21).**

| Check | Result |
|---|---|
| `grep -rn "verify_roster" scripts/` | only `verify_rosters.norm` imported — the **name fold**, by `league_live.py`, `transactions.py`, `league_intake.py` |
| `grep -n "build_deck" scripts/morning.py scripts/season_deck.py` | no match — the deck's verification gate is **not** in the in-season path |
| `grep -rn "roster-provenance" scripts/ report/*.py` | `check_provenance.py`, `rank_engine.py` — **both read-only** |
| writes to the pool's `team` column in-season | none found |
| `python3 report/check_provenance.py --max-age-days 14` | FAIL — **322 of 325** rows over the limit, oldest **100 days** |
| rows still inside the limit | **3** [SINGLE-SOURCE] (`check_provenance.py` output, this session) |

**Refinement found by the refutation pass, 2026-10-21.** "No script writes it" is
true but could be misread as "it never changes." `git log --follow` shows
**26 commits** have touched `roster-provenance.csv` — it was maintained **by
hand**, by sessions, and the last such commit was `52c590b` (2026-10-07,
D-CAST-1), which is exactly why the only 3 rows inside the 14-day window are
dated 2026-10-07. So the accurate statement is: **the file has never had an
automated writer, and hand-maintenance stopped on 2026-10-07.** An independent
repo-wide grep (all file types, not just `.py`) found no shell script, notebook
or other writer either — the only `.py` files naming it are `rank_engine.py`,
`check_provenance.py`, this session's test, and one archived report writer, all
read-only.

Those 3 surviving rows all carry the same verification date, one week before this
report, so every row in the file is past the limit the day after it.

**INFERENCE.** Exposure is low now and grows: team labels drive schedule and
games-per-week, and a wrong label needs an in-season transaction to arise. One
week into the season that is rare; by the February trade deadline it is not.

**This withdraws D-INT-1 option (c)**, which this session recommended twice today.
It rested on a control that does not run.

## 2. Corrections landed

- **(C) `report/plans/co-gm-self-audit-2026-10-15.md`** — three passages carried
  false claims, each now marked `[CORRECTED 2026-10-21]` with the evidence
  inline: A2's "the weekly in-season pull keeps it green" (nothing writes the
  file), A2/§4's "re-dating pass … (mechanical)" (no such pass exists — the item
  means *build a writer*), and the stale 318 count.
- **(D) `arena/data/weekly_matchups_2025-26.csv`** — week 1, Kyle, `gp` **29 → 28**.
  Receipt: the owner's Yahoo week-1 matchup screenshot (2026-10-21) reading
  `32/32` and `28/28`. The other 20 week-1 values reproduce it exactly, and
  recomputing the nine categories from the stored totals returns David
  **8-0-1** with the TO 68–68 tie, matching the recorded `cats_won`. `gp` is not
  a scoring category, so no result moved. **The other 43 rows' `gp` is unchecked** —
  only week 1 has a screenshot, so an isolated slip and a systematic one are not
  yet distinguishable. Recorded in the README.

## 3. Built, deliberately NOT wired — `scripts/check_claims.py`

A registry (`report/claims.json`) of claims the system makes about itself, each
with a mechanical check; `writer_exists` and `invoked_by`. Red-first: tests
written and failing before the script existed, **8/8 green** after.

**The checker failed its own known-answer control on first run**, and that is the
most useful thing in this report. CL-5 ("gates.json is written by gates.py")
came back FALSIFIED. Two causes, both real: the registry pointed at
`report/gates.json` (the file is at the kit root), and the detector could not see
a writer whose path arrives through an **argparse default** — `gates.py` writes
`open(a.out, "w")` where `--out`'s default carries the name. That idiom is common
here, so the detector would have under-reported writers across the repo. Per
adversarial-verify rule 9 the checker was re-diagnosed rather than its threshold
tuned; the fix is a generalization (follow argparse defaults to `a.<dest>`), and
a regression test pins the exact case. Both known-answer controls now return
SUPPORTED, so the detector is validated in both directions.

First run: **5 claims, 3 FALSIFIED as expected, 2 SUPPORTED controls.**

Not added to `scripts/gates.py` — Council/Executor: no new gate surface inside
12 hours of a scheduled run. Wiring it is **D-CLAIM-1**.

## 4. Scheduled-task class defect (context, fixed earlier this session)

Both fresh-session tasks assumed a repo checkout that does not exist.
**EVIDENCE:** a probe session showed `add_repo` **is** present in a fresh cloud
session's tool list but was **denied by the auto-mode permission classifier,
"awaiting approval"** — so unattended it blocks. Both repos are public
(`private: false`), so both prompts now carry a credential-free `git clone`
fallback and report which path they took. The class defect — nothing verifies a
scheduled task's assumptions before it fires — is **D-CLAIM-2**.

---

## Watchlist

- `roster-provenance.csv` — **all 325 rows past the freshness limit from 2026-10-22.**
  Dormant today (the gate does not fire in-season), live if `rank_engine.main()`
  is ever run again. D-INT-1.
- In-season NBA team labels — unverified by anything. Bites on the first
  in-season transaction affecting a rostered player; materially at the February
  deadline. D-INT-1.
- `report/claims.json` — 3 rows FALSIFIED by design. If a row's verdict ever
  stops matching its `expected`, something changed and nobody said so; that is
  the signal the registry exists for. D-CLAIM-1.
- `gp` in `weekly_matchups_2025-26.csv` — 43 of 44 rows unchecked against a
  source. D-CLAIM-3.

## Open-item receipts

| Item | Status | Receipt |
|---|---|---|
| D-INT-1 | **re-put, options rebuilt** | option (c) withdrawn 2026-10-21; `morning.py` names neither `build_deck.py` nor `check_provenance.py` (grep, this session) |
| D-CLAIM-1 | **new, dated** | `check_claims.py` + `claims.json` committed, wired into nothing; decide by 2026-10-24 |
| D-CLAIM-2 | **new** | scheduled-task prompts carry the public-clone fallback; probe session showed `add_repo` present but denied by the auto-mode classifier |
| D-CLAIM-3 | **new** | week-1 Kyle `gp` corrected against the owner's screenshot; 43 rows unchecked |
| D-TW-1..3 | carried | unchanged — owner decision outstanding since 2026-10-20 |
| D-TF-1 (trade veto) | **closed** | Trade Finder removed; guard test asserts the card never renders |

## Repeat-name market check

Not run and not applicable: this item pulled no market source and changed no
pool row, so there is no new name to collide. The standing check's last run is
the 2026-10-14 lock refresh (32/32, 12 flagged), unchanged by anything here.

## Bounds

**Out of scope by design.** Building the re-dating writer (needs an ESPN fetch
and touches the preseason path); wiring the claim check into `gates.py`; any
change to a projection line, tag, roster or engine constant; anything
`morning.py` calls.

**In scope and unverified.**
- `gp` on the other 43 rows of `weekly_matchups_2025-26.csv` — `NOT-ATTEMPTED`
  (only week 1 has a screenshot). Not load-bearing tonight; load-bearing for any
  future games/shock fit, and flagged in the README for that reason.
- Whether `add_repo` would also be denied in a *scheduled* session specifically,
  as opposed to the interactive probe — `ATTEMPTED-FAILED` (the probe blocked on
  approval and was archived). Not load-bearing: the clone fallback makes the run
  work either way.
- Whether the deck's `verify_rosters.py` can reach ESPN from this environment in
  `direct-complete` mode — `NOT-ATTEMPTED`. **Load-bearing for option (b) below**,
  so (b) is marked `candidate` until a dry run settles it.

## Decision sheet

**D-INT-1 (re-put; the old option set is withdrawn).** In-season team labels are
verified by nothing.
- **(a)** Build the re-dating writer and wire it into the morning run. Real work:
  ESPN fetch, tests, a new in-season step.
- **(b)** Wire the deck's existing `verify_rosters.py` into the in-season path.
  Cheaper — the verifier is already written. **Caveat:** the 2026-08-09 finding
  F01 showed `fallback-partial` mode compares the pool against a mirror of
  itself, so only `direct-complete` is real verification. `candidate` until a dry
  run proves ESPN is reachable here.
- **(c)** ~~Retire the age flag; live verification supersedes it.~~ **WITHDRAWN
  2026-10-21** — the premise is false.
- **(d)** Accept the exposure explicitly: stamp the board and deck "team labels
  unverified in-season" and re-check by hand at a stated cadence.
- *Recommended:* **(b), falling back to (a) if the dry run shows ESPN unreachable.**
  Not urgent tonight; wanted well before the February deadline.

**D-CLAIM-1.** Wire `check_claims.py` into `scripts/gates.py`? (a) yes, after
tomorrow's run · (b) yes, and fail the build on any FALSIFIED row whose
`expected` is SUPPORTED · (c) leave it manual. *Recommended:* **(b)** — a
registry nobody runs is the defect it was built for. The Council's Expansionist
dissented at 4–1 precisely because deferral is how this dies, so it carries a
date: **decide by 2026-10-24.**

**D-CLAIM-3.** Re-check `gp` on the remaining 43 rows of the 2025-26 matchup file?
(a) yes, when the weekly screenshots are captured · (b) no, treat `gp` as
error-bearing and stop using it in any fit. *Recommended:* **(a)**, folded into
the scoreboard capture if that goes ahead.

## Provenance

Session `session_01QjgeRdpDaWgSJmGKRG8fTU`, 2026-10-21 00:30–01:00Z. Governors
loaded this task: council, gauntlet, plan-gate (full block, pre-work),
adversarial-verify. Kit suite 196/196 twice before the work; claim-check tests
8/8. Nothing merged; nothing published; no plane changed.
