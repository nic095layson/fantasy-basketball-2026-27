# System-wide red team and audit — 2026-10-21

Pull window: 2026-10-21 → 2026-10-21 (audit only; no roster pull, no box scores, no plane change).

**Owner's request.** "We've built and changed a lot today, and we've also encountered
a lot of errors and mis-truths. Please conduct a system wide red team and audit,
including the tool's and arithmetic computational integrity. Provide plain language,
thorough afterreport."

**What was audited.** Kit `main` **ec803bb**, deck `main` **d33942f** — the post-merge
heads, read with `git rev-parse`, not assumed. Both engines' arithmetic, all 31
registered judgment constants, every gate and tool in both repos, the two scheduled
tasks, and an inventory of today's errors assembled from `git log` and this session's
tool output rather than from memory.

**Headline, in one paragraph.** The arithmetic is clean — not "passed its own tests"
clean, but *an independent implementation written from the spec by an agent that never
saw the source reproduces it to the digit*, 1,800 of 1,800 cells, same rank order. The
constants have not drifted. What is wrong is somewhere else entirely, and it is the
same thing that was wrong all day: **the system is reliable at computing and unreliable
at knowing what actually runs.** Every error today was a confident statement about a
mechanism nobody had exercised. Three of them were in checkers I wrote to catch errors.

---

## 1. Arithmetic — the strongest result in this report

A subagent was given the written spec (PROMPT.md §2 and §4.2) and the input data, and
explicitly forbidden from reading `rank_engine.py`, `season_board.py`, `season_lines.py`,
`hoops.py`, `arena.py`, or any existing board output. It wrote its own implementation
and reported three interpretation choices it had to make. Then both were run on the same
180-player pool.

| | result |
|---|---|
| cells compared (9 categories + total × 180 players) | **1,800** |
| disagreements at the attacker's reporting precision | **0** |
| largest raw difference | 5.0 × 10⁻⁷ (its 6-decimal rounding) |
| rank order of the top 180 by total | **identical** |

Its three independent choices — population SD, volume-weighted pool percentages
(`Σ pct×att / Σ att`), TOV negated — all match the engine, which was written separately.
Reading the engine afterwards confirms the same three.

**In plain language:** somebody who had never seen your code, working only from your
written description of the method, built the same calculator and got the same answers
to six decimal places on every player in every category. That is the real test, and it
passed.

**One finding the attacker volunteered, which is worth having.** The spec says the pool
"iterates once". It is not a fixed point after one iteration: re-selecting with the
second-pass parameters would swap four fringe players (Konchar and Dunn in, Spencer and
Joe out). This affects the bottom of the pool and nothing in the top 100. It is a
definitional loose end, not an error — the spec says once, the engine does once.

## 2. Constants and engine state

- **Registry: PASS — 31 registered = 31 live**, no unregistered constant, no drift.
  Breakdown: 7 settings, 6 measured, 6 declared_band, 4 structural, **8 uncalibrated**.
- **Today's merges touched no engine code, no projection line, no roster, no tag.** The
  only data added was three pinned raw FantasyBot JSON files. Verified by diff, not asserted.
- Of the 8 uncalibrated constants, **6 are legitimately scoped out** — they are
  draft-time or mock-room only (`GRAD_K`, `GRAD_SCALE`, `MKT_W`, `MKT_PIN`,
  `PAIR_MIN_GAIN`, `PAIR_WAIT_MIN`) and have no in-season effect. The two that matter
  in-season are `availability` (§4 below) and `SEASON_GAMES = 65` (D-IS-1, open).

## 3. The red team's own gate is RED — and it is right to be

`run_attacks.py` **FAILS**: all four attack records (A-1, A-5, A-7, A-8) are STALE,
made on engine `259c630` while the live deck is `d33942f`. The fixture caught its own
staleness, which is the fixture working.

But the honest reading needs the next step, which the gate cannot take:

- 6 commits separate the sweep from today, dated 2026-10-15 → 2026-10-19.
- Those commits are governance hooks, CLAUDE.md, LESSONS.md, settings, and last night's
  weekly-matchups CSV.
- **`arena/arena.py` and `scripts/hoops.py` are byte-identical** at both commits
  (sha256 `7b84edc16f2c30f9` and `6eb3e0320befdd03` at each).

So: **formally stale, substantively sound.** The bands measure an object that has not
changed. I am not quoting them as current numbers, because the rule exists precisely to
stop that reasoning from becoming a habit — but you should know the difference between
"stale and probably wrong" and "stale and provably measuring the same code." This is the
second.

## 4. New finding — the two instruments price injury differently

The board haircut (`hoops.availability`) and the simulator's weekly availability
(`arena.weekly_availability`) are different scales by design: one is a relative ranking
multiplier (healthy = 1.00), the other an absolute weekly probability (healthy = 0.88,
because healthy players miss games too). So the raw gap on all 168 rostered players is
expected, not a bug.

The real test is whether they agree **relative to their own healthy baseline**:

| tier | board | simulator | board ÷ healthy | sim ÷ healthy | **relative gap** |
|---|---|---|---|---|---|
| healthy | 1.00 | 0.88 | 1.000 | 1.000 | 0.000 |
| mild | 0.85 | 0.79 | 0.850 | 0.898 | **−0.048** |
| risk | 0.78 | 0.75 | 0.780 | 0.852 | **−0.072** |

**The board punishes injury risk harder than the simulator does** — about 7 points
harder at the risk tier. Both cannot be right. Exposure today: **27 rostered players on
a risk tier, 5 on mild**, including Kawhi Leonard and Kyrie Irving on your own team.

This is already on the sheet as **D-PM-4** ("reconcile 0.78 vs 0.75, 1.0 vs 0.88"). What
this audit adds is the relative framing, which makes it a real inconsistency rather than
a cosmetic one, and the count of players it currently touches. It is a judgment call
which number is right — that is yours, not mine.

There is also a separate divergence at the recovery tier: the board **excludes**
recovery players (0.0), the simulator **prices** them at 0.60. Five rostered players are
on a recovery/out tag right now (Strus, Mark Williams, Suggs, Butler, Nurkić). Since the
board excludes them they never reach a board ranking, but the league simulator reads
real league rosters — so it does see them, at 0.60.

## 5. Every tool and gate, pass or fail

| check | result |
|---|---|
| kit test suite | **204/204**, run twice |
| `check_derived` | **PASS** — all 29 dated artifacts reproduce byte-for-byte from pinned inputs |
| `check_provenance` (structural) | **PASS** — every row sourced |
| `check_provenance --max-age-days 14` | **FAIL** — 322 of 325 rows stale, oldest 100 days (D-INT-1, known) |
| `check_claims` | **FAIL by design** — 3 rows FALSIFIED as expected, 2 controls SUPPORTED |
| `run_attacks` | **FAIL** — 4 records stale (§3) |
| constants registry | **PASS** — 31 = 31 |
| deck `check_planes` | **PASS** — 315 shared, team 0, exclusion 0, drift 0, propagation 0 |
| deck `identity_check` | **PASS** — no rows off the points identity |
| deck `range_check` | 1 row flagged (Dylan Harper FT% .765 vs .754–.758, +0.05) |
| deck `repeat_market_check` | ran; 9 near-misses listed, no new collision |

Two of the three reds are known and tracked; the third (`check_claims`) is the intended
output of a checker built last night to report exactly those three falsified claims.

## 6. The errors — what actually went wrong today, and the pattern

Assembled from commits and tool output, not recollection.

| # | what was said or done | what was true | caught by |
|---|---|---|---|
| 1 | Scheduled-task prompts: "the kit is this session's own repository" | a fresh session has no checkout; the 10/20 evening run did nothing | the owner, from the failed run |
| 2 | First fix assumed `add_repo` would work unattended | present but **denied by the permission classifier**; would have stalled at 5:53am | my own probe |
| 3 | D-INT-1 option (c) recommended **twice**: "live ESPN verification supersedes the age flag" | nothing verifies team labels in-season at all | closing the Council's unknown |
| 4 | Self-audit A2: "the weekly in-season pull keeps it green" | **no script writes that file**, and none ever has | grep |
| 5 | D-INT-1 (a): "run the re-dating pass (mechanical)" | no such pass was ever built | grep |
| 6 | "Still only yours: attach the FantasyBot connector" | the owner had already attached it; the evidence was in a tool result I had read one minute earlier | the owner |
| 7 | `check_claims` detector | blind to writers routed through an argparse default — would have under-reported writers repo-wide | its own known-answer control |
| 8 | tonight's roster join | read field `name`; the field is `player` → 0 of 168 matched [SINGLE-SOURCE] (this session's own tool output) | implausible result |
| 9 | tonight's tier classifier | substring-matched whole notes → Haliburton scored "mild" off his injury history [SINGLE-SOURCE] (this session's own tool output) | implausible result |

**The pattern.** Nine errors, and not one is arithmetic. Every single one is a confident
claim about **whether a mechanism runs** — a script, a tool, a control, a connector, a
checkout. The part of this system that is exercised daily (the maths, the gates, the
byte-for-byte reproduction) is flawless. The part that is *described* rather than
exercised is where everything went wrong.

**The second-order pattern is worse and more useful.** Items 7, 8 and 9 are checkers I
wrote *to catch errors*, and each was broken before the thing it was checking. Three
times in one night, adversarial-verify's rule 9 — *a broadly-failing check indicts the
checker* — was the thing that saved the finding. A detector nobody validates is a
confident wrong answer with a script behind it.

**Why `check_claims` is the right response to this and is currently unwired.** It was
built last night precisely to test the "does it actually run" class of claim
mechanically. It sits in the repo running nothing (D-CLAIM-1, decide by 2026-10-24).
That is the single highest-value thing on the decision sheet, because it is the only
item that attacks the pattern rather than one instance of it.

## 7. What I could not establish

- **Whether the 10/19 structural bands are numerically current.** The simulator is
  byte-identical, so they very probably are, but only a re-run proves it. `NOT-ATTEMPTED`
  — hours of compute, and a decision for you, not a limit I hit.
- **Whether the `note_tag` extraction is robust.** It takes the leading token of a
  free-text research note. It works today because non-injury notes (dates, "role",
  "repriced") fall through to healthy, which is correct. A note that happened to begin
  with "risk" or "mild" would mis-tier. I did not find one; I also did not enumerate
  every possible future note. `INFERENCE` on the mechanism, not a measured failure rate.
- **Whether any projection line is *wrong*.** This audit tested reproducibility and
  consistency, not accuracy. The engine computes exactly what it says it computes; that
  is a different claim from "the projections are good."

## Watchlist

- **`availability` tier mismatch (§4)** — 27 risk + 5 mild rostered players priced
  differently by the two instruments. D-PM-4.
- **Red team stale** — every band quoted anywhere is formally stale until the sweep
  re-runs. D-RT-STALE (new).
- **`roster-provenance.csv`** — all 325 rows past the limit from 2026-10-22. D-INT-1.
- **`check_claims` unwired** — the one check aimed at the actual failure pattern runs
  on nothing. D-CLAIM-1, dated 2026-10-24.
- **Pool not a fixed point after one iteration** — 4 fringe players; cosmetic today.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| arithmetic integrity | **CLEAN** | 1,800/1,800 cells, independent spec implementation, rank order identical |
| constants drift | **CLEAN** | 31 registered = 31 live on d33942f |
| engine untouched today | **CONFIRMED** | diff of ec803bb vs 7c6a05a over engine paths: 3 pinned JSON only |
| D-PM-4 availability | **re-put with new evidence** | relative gap −0.072 risk / −0.048 mild; 32 rostered players exposed |
| D-RT-STALE | **new** | run_attacks FAIL, 4 records on 259c630; arena.py and hoops.py byte-identical |
| D-INT-1 | carried | 322/325 stale, no writer exists |
| D-CLAIM-1 | carried, dated | decide by 2026-10-24 |

## Repeat-name market check

Not applicable: this audit pulled no market source and changed no pool row, so no new
name can collide. The standing check ran clean tonight (9 near-misses, none new).

## Decision sheet

1. **D-PM-4 — reconcile the two availability scales.** (a) move the simulator to match
   the board's relative penalty; (b) move the board to match the simulator's; (c) declare
   them deliberately different and document why. *Recommended: (c) first — write down
   which is which — then decide (a) or (b) with a sweep, because this moves title odds.*
2. **D-RT-STALE — re-run the assumption sweep** to un-stale the bands. *Recommended: yes,
   but scheduled, not now; the simulator hasn't moved, so nothing is urgent.*
3. **D-CLAIM-1 — wire `check_claims` into `gates.py`.** *Recommended: yes. It is the only
   item here that addresses the pattern rather than an instance.*
4. **D-INT-1 — the provenance writer.** Unchanged from last night; still yours.

## Provenance

Session `session_01QjgeRdpDaWgSJmGKRG8fTU`, 2026-10-21. Governors loaded: red-team,
plan-gate (full block, pre-work), adversarial-verify. Separate attacker: one subagent,
spec-only, 64k tokens, 7 tool calls. Kit ec803bb, deck d33942f. No projection line, tag,
roster or engine constant was changed by this audit; `git diff` over both planes is empty
but for this report and its pull-log row.
