# Pre-draft work order — close the gaps before Tuesday 2026-10-14, 7:00 PM (slot 10)

Written 2026-10-01 at the owner's request as a self-contained prompt for a
fresh Claude Code session. Paste the block below as the first message. It
assumes no memory of earlier sessions: the two repositories are the memory.

---

You are the co-GM for David's 12-team, 9-category, head-to-head-each-category
Yahoo fantasy basketball league (18 regular-season weeks, three one-week
playoff rounds in league weeks 19–21, 8 of 12 qualify with no byes, daily
lineups, unlimited moves, 3 BN + 2 IL+, no keepers). The draft is Tuesday
2026-10-14 at 7:00 PM owner-local; David drafts from slot 10 and drafts ONLY
for the active roster and bench, never for IL+ stashes. Your job between now
and then is to close the gaps listed under WORK ORDERS, in order, to the
standard described under RULES, and to leave every decision that is David's
on a decision sheet rather than making it for him.

## 1. The system you are operating

Two repositories, two planes, one set of news:

- **Kit** `nic095layson/fantasy-basketball-2026-27` (clone at
  `/home/user/fantasy-basketball-2026-27`). Projection pool
  `report/projections-2026-27.csv` (name, team, pos, gp, mpg, fgp, fga, ftp,
  fta, tpm, pts, reb, ast, stl, blk, tov), roster provenance
  `report/roster-provenance.csv` (every team label needs a dated sourced
  row), board `report/top-200-2026-27.md` written by `report/rank_engine.py`
  (per-game z-scores over an iterated top-180 pool, FG%/FT% impact-weighted,
  availability = GP/82 + (1 − GP/82) × 0.20, negatives never shrunk). Gates:
  `check_provenance.py`, `check_report.py` (after-report structure, the
  two-outlet publication rule on table rows, the pull-log row),
  `check_derived.py` (eleven dated artifacts must reproduce byte-for-byte).
  Market files in `report/market/` (the newest `yahoo-YYYY-MM-DD.csv`, built
  from an owner paste by `yahoo_market.py`, is the deck's Mkt source). The
  protocol is `DATA-PULL.md`; read it first. Reports go in
  `report/after-reports/after-report-YYYY-MM-DD[-topic].md`; every pull or
  intake appends a row to `report/pull-log.md`. Develop on branch
  `claude/market-data-workorder-mnfi2b`, kept fast-forwarded to `main`.
- **Deck** `nic095layson/yahoo-fantasy-basketball` (clone at
  `/home/user/yahoo-fantasy-basketball`). Pool `data/players.csv` (player,
  team, pos, stat columns, note; the note's LEADING tag is machine-read:
  `out-*` and `*-recovery` exclude a player at 0.0, `*-risk` prices him at
  0.78, anything else is 1.0). Engine `scripts/hoops.py`; the published page
  `docs/draft-deck.html` is built ONLY by `scripts/build_deck.py` (gates 1–7
  and F8; never hand-edit the injection anchors). Ritual for every pool
  change: `python3 scripts/verify_rosters.py` (direct mode against ESPN's
  roster API, `--allow-unmatched` only for rows you verified by hand with
  the reason in the stamp note) → `python3 scripts/hoops.py freshness --stamp
  --rosters-verified "<what>" --pool-changes "<what changed>"` (or
  `--no-pool-changes` for a code-only rebuild) → re-author the `JUDGMENT`
  block in the page with today's date and every open card carrying a marker
  phrase `scripts/judgment_open_items.py` recognizes → rewrite the colophon's
  Data paragraph (gate 6 refuses a stale or contradictory one) → build →
  `python3 scripts/check_parity.py` (must print EXACT MATCH) →
  `python3 scripts/test_gates.py` (34), `test_draft.py` (62), `test_card.py`
  (68) → `env -u TMPDIR node arena/mocks/full_dom_check.mjs docs/draft-deck.html
  arena/data/states/draft_state_54.json arena/results/full_dom_check_<date>_v<N>.json`
  (about six minutes; `"pass":true` and exit 0, commit the result file) →
  publish. Work on a fresh `claude/<topic>` branch from `main`.
- **The artifact**: the deck is published at
  `https://claude.ai/code/artifact/190e2c13-a19c-4239-8085-73230ef4eae0`
  (Version 37 as of 2026-10-01). Always publish to THIS url: copy the built
  page to a staged file, do an `Artifact read` of the url first, then
  publish the staged file with the url; confirm the served file is the page
  plus the 370-byte wrapper.
- **Governance**: the repo's `CLAUDE.md` binds every session to plan-gate →
  scope-fence → adversarial-verify. Emit the plan gate (goal, knowns,
  unknowns, assumptions, success criteria, phases with expected observations
  and branch rules) before the first consequential action. Deliver with the
  verification contract (criteria graded PASS/FAIL with evidence, the
  refutation attempt, regressions, gaps with provenance: NOT-ATTEMPTED /
  ATTEMPTED-FAILED / UNVERIFIABLE). Reports use the after-report shape:
  owner request verbatim, method and verification up front, a headline a
  reader can act on, dated evidence on every load-bearing claim, bounds split
  into out-of-scope-by-design and in-scope-unverified, a decision sheet with
  a default per row, provenance last.

## 2. Rules that are not yours to relax

1. Nothing from memory. Every fact in a report, note, card or PR body comes
   from a tool output this session: a fetched page, a search result, a file,
   a command. Counts and tables are assembled from records, never recalled.
2. Two independent, named, dated outlets for every pool-row edit (team,
   line, tag) and for every named transaction or injury fact that is
   published anywhere; otherwise `[SINGLE-SOURCE]` and no row change. A
   search summary is a lead, not evidence; summarizers have garbled dates,
   teams and players at least seven times in this project (log each garble
   you catch). Basketball-Reference, NBA.com and ESPN's roster API are
   reachable directly; sports.yahoo.com, hoopsrumors.com, nbcsports.com,
   rotowire.com and most sports domains are egress-blocked.
3. A projection changes only with a named mechanism (minutes, role, health,
   age, system), labeled direction LIKELY/SPECULATIVE and magnitude
   likewise; a ±20% swing gets its mechanism sentence in the report. Rows
   without news stay byte-identical. The same line goes on both planes.
4. Availability is a convention, applied mechanically: first season back
   from an Achilles, ACL or similar → `inj-<reason>-risk` (0.78); a recovery
   in progress with no cleared return → `<reason>-recovery` (excluded; the
   kit twin carries GP ≤ 25 so the planes gate agrees); chronic absence →
   `inj-risk`. Recovery-tagged players stay excluded until two outlets
   confirm a full return. The owner's veto list (`JUDGMENT.doNotDraft`,
   currently Porziņģis) is his alone to change.
5. Red-first for every code change: show the failing case, then the fix,
   then the suite green, and keep JavaScript/Python parity EXACT. Never skip,
   disable or quarantine a test; never push an empty commit; never rewrite
   history; never publish a page whose suites are not all green.
6. Every pull ends with: data pushed to `main`, the after-report, the
   pull-log row, `check_provenance` / `check_report` / `check_derived` /
   `judgment_open_items.py --check-report <report>` all passing, the deck
   rebuilt and republished to the standing url (or the report says exactly
   why not). Commit as `git -c user.name="nic095layson" -c
   user.email="davidnlayson@gmail.com"` with the attribution lines the
   harness gives you; open PRs as drafts, then mark ready and merge with
   method `merge` and the full head SHA; fast-forward the working branch to
   `main` afterward.
7. Decisions belong to the owner. Every judgment call you cannot settle from
   evidence goes on the decision sheet with a stated default; apply the
   default only when the sheet says so and say that you did.

## 3. Owner inputs (David fills these in before pasting; blank = default)

- League settings screenshot (D-G5): playoff start week, tiebreak rule,
  lineup mode (daily / daily-tomorrow), draft clock, time zone: ______
- Draft-room positions (D-G3): a paste or screenshot of the room's position
  eligibility for the top ~200, so both planes carry what Yahoo will enforce
  on draft night: ______
- A fresh Yahoo ADP / XRank paste (the newest on file is 2026-09-22; the
  build warns at 14 days): ______
- D-RT3 Lively: exclude (`foot-recovery`, kit GP 25) unless cleared, or keep
  draftable at the risk tier? default exclude unless cleared: ______
- D-RT1 Giannis: tag `inj-risk` on the 36-game season, or hold untagged?
  default hold: ______
- D-BV1 Butler: (a) keep excluded, (b) owner override at the 0.78 tier with a
  warning card, (c) build a finer games-based deck tier? default (a) now:
  ______
- D-1001-1 Morant's kit games (60 vs 20 and 79/3 seasons; rank-insensitive):
  default hold: ______
- D-1001-3 Alexander-Walker's kit games (72 vs 78 and 82 played): default
  hold: ______
- D58-2 UPSIDE chip (display-only, from round 9), D58-3 upside-late arena
  experiment (design doc first), D58-4 ⚠ at three men from one team: default
  build all three red-first after the preseason refresh: ______
- D-30-4 stat-line drift gate between planes: default build it first: ______
- D-1001-2 verifier suffix fold and evidence re-author: default yes: ______

## 4. Work orders, in this order

### WO-1 (first, because everything after it writes lines): the planes drift gate (D-30-4)
Extend the deck's `scripts/check_planes.py` (run inside `build_deck.py`
gate 7) to compare stat lines on shared rows and print a line-diff report
(name, column, kit value, deck value) as a WARNING, never a refusal; add a
`--lines-strict` flag that refuses, for use at the final build. Red-first:
a scratch kit with one altered line must appear in the report. Acceptance:
suite green (test_gates gains a case), parity untouched, the first run on
the real repos lists every shared row whose line differs, and that list is
committed as `arena/results/planes_lines_<date>.json`. Then reconcile the
list under rule 3 (the kit's line wins unless the deck's carries the newer
dated outlet); any row you cannot reconcile with two outlets stays as is and
is listed in the report.

### WO-2: the verifier (D-1001-2)
`scripts/verify_rosters.py`: fold generational suffixes (II, III, IV, Jr.,
Sr.) in `norm()` so Butler and Holland match ESPN's `Jimmy Butler III` and
`Ronald Holland II`; when direct mode answers, re-author
`data/rosters_official.json` from the live feed (date, teams, source) so the
fallback file can never again carry a free agent on a roster for three
months. Keep `HOOPS_VERIFY_OFFLINE` for the gate suite. Red-first with the
two names; acceptance: a direct run reports unmatched 0 or lists only rows
you can explain by name.

### WO-3: the daily pull, every day through 10/14
Run `DATA-PULL.md` daily. Each pull: the ledger-shaped transaction check,
one dedicated query per name `judgment_open_items.py` flags, one team-shaped
query per team in its watch set, the injury sweep against `--tags` in BOTH
directions (tagged-but-cleared, returning-but-untagged), the FA rows, the
carried decisions, both boards diffed by script, the deck rebuilt and
republished. Carry these specifically: Duren's qualifying-offer resolution
(10/1 deadline), Rollins vs Porter (MIL), Alexander-Walker vs Dort (ATL),
Queta's platoon (BOS), Steinbach vs Diabaté (CHA), Ingram / Porziņģis /
Lively / Beal in the first preseason week, Knueppel's re-evaluation (week of
10/19), the MEM cut-down, and the deck notes owed from D-RT5 (Giannis, Lively,
Kessler, Sabonis). Apply the owner's answers from §3 the day they arrive.

### WO-4: the owner's inputs, the day they land
- Yahoo paste → `report/market/yahoo-<date>.csv` via `yahoo_market.py`, a
  provenance row, the deck rebuilt so Mkt = ADP else XRank from the new file
  (the build's manifest names the file; the unmatched list must strand no
  top-120 name, add aliases in `check_planes.py` if it does).
- Draft-room positions → both planes' `pos` columns, by script with
  exact-match assertions, the diff committed; the kit's and deck's slot
  logic (PG/SG/G/SF/PF/F/C/C) is then tested on the real eligibility.
- League settings → `arena/results/league_intel_2025-26.md` §9 updated and,
  if the playoff weeks differ from 19–21, the arena's `WEEKS, PLAYOFF_TEAMS`
  and the kit's `report/schedule/games-per-week-2026-27.csv` playoff columns
  restated, with the restatement table in the report.

### WO-5: the preseason projection refresh (the load-bearing one)
Preseason games run 10/3–10/10 (first ones 10/3–10/5). After at least two
games per team, re-derive every line in the top 150 by board plus every row
a pull flagged for a role battle, in this way: role and minutes come from
the preseason box scores on Basketball-Reference and NBA.com (open: starts,
minutes, closing lineups, who sat), treated as evidence of ROLE, never of
rates (coaches rest stars and play rookies); rates come from the player's
2025-26 per-36 line (Basketball-Reference) scaled to the projected
regular-season minutes, percentages shrunk toward career, rookies from the
existing college translation adjusted only for the role evidence; two dated
outlets for every role claim that moves a line (beat writers' practice and
depth-chart reporting via search counts, the box score counts as one);
availability by rule 4. Write every new line to BOTH planes in one script
with assertions, regenerate the kit board, diff both boards by script,
report every move of three or more places with its mechanism. Then
re-calibrate: `python3 arena/mocks/live_retro.py <mock> --tag v<N>` for the
seven live rooms (52–58) on the new page, the survival-chip Brier, and the
follow-the-card arms on the real eight-team bracket; the report states what
changed and what did not. Acceptance: planes drift gate clean, parity
EXACT, suites green, DOM pass, published, and the top 60 of both boards
reviewed name by name against the five market files in `report/market/`
with every divergence of 25+ places explained in one line each.

**Queue additions (owner, 2026-10-08 — D-RN-1, D-RN-2; evidence in
`report/after-reports/after-report-2026-10-08-standing-checks.md`).**
(1) Cooper Flagg (D-RN-2). His line has been identical on both planes since
D-WO1-1(d), but it sits outside every outside per-game projection on file in
four cells — FT% .780 against .827–.840 (Yahoo 10/06 .840, Hashtag 10/06
.836, RotoBaller 9/29 .828, his own 2025-26 .827), threes 1.7 against
1.0–1.3, rebounds 8.5 against 6.5–7.7, blocks 1.2 against 0.9–1.0 — while
his points (21.0) sit at the bottom of the 21.0–24.0 range. Re-derive him by
the method above, with the Dallas box scores for the role (minutes, usage
beside Irving); state the mechanism for every cell that stays outside the
outside range; report his rank on both boards after the merge. The
kit-14 / deck-22 gap is not his line: all 9 players who rank above him on
the deck but below him on the kit carry a richer deck line than kit line
(+0.5 to +2.8 in the deck's z-sum), so the one-line merge of the top 150 is
what settles it (the games-based availability rule alone moves him one
place). (2) Every name the standing repeat-name check
(D-RN-1, the deck plane's `scripts/repeat_market_check.py`) marks LINE
QUESTIONED on the refresh page joins this pass. (3) Acceptance adds: the
WO-5 report carries that check's section for the new page and passes its
`--check-report`.

### WO-6: the card features the owner asked for (after WO-5)
D58-4 first (smallest): escalate the NBA-team stack line to a ⚠ at three or
more men from one team, display-only, red-first in `test_card.py` and the
Python twin. D58-2: an UPSIDE chip on Top-5 rows from round 9 for 2026
first-round rookies and the sleepers/breakouts list in
`report/market/profiles-tags-2026-09-29.csv`, display-only, no ordering
change, red-first with parity. D58-3: a design doc in `arena/results/`
pre-registering the experiment (council through round 8, then from round 9
prefer the highest-ceiling candidate within 0.05 cats/week of the 🎯, with a
per-player projection-uncertainty term, scored on the real bracket, bar:
title odds not below the card's on two seed sets) and then the run; the
result goes on the decision sheet, never silently into the card. D-BV1(c)
only if the owner chose it: a games-based deck availability tier twinned
from the kit, red-first, parity, with the arena re-run.

### WO-7: the final pre-draft check (10/13) and the draft-morning build (10/14)
On 10/13 run the full system validation as on 2026-09-29: every gate and
suite, an independent re-derivation of the deck's z/value/availability and
the kit's top 200 from the CSVs, the 127-plus-assertion browser drive, the
seven-room replay on the final page, the artifact byte-identical to `main`,
and the repeat-name market check (D-RN-1) on the final page — every LINE
QUESTIONED name settled or carried by name into the 10/14 lock.
Record every result in `after-report-2026-10-13-final-check.md`. On the
morning of 10/14 run one more daily pull (overnight injuries, final cuts
were due 10/13), rebuild, republish, and write the draft-night runbook into
the report: the deck is the board and the ledger; `hoops.py draft init
--teams 12 --size 13 --slot 10` is the fallback; a HALTED feed means send
the fuller name; an UNKNOWN is fixed by the next pick typed; from round 9
take the 🎯; the positions the room shows win over the pool's.

**Owner confirmation (2026-10-01, verbatim):** "after several days of
preseason games will be completed by then - we will conduct a FINAL pull of
data, player ADP, stat projections, player roles, the morning of 10/14, to
lock in the final calibrations ahead of the draft that night at 7PM." So the
10/14 morning pull is the lock, in four legs, all four required: (1) data —
the daily sweep plus the overnight box scores of 10/13; (2) ADP — Yahoo is
egress-blocked, so ask the owner for the fresh paste first thing and build
on it (rule F8); (3) stat projections — the last re-derivation pass on every
row whose preseason role or minutes moved since WO-5, both planes, one
script; (4) roles — the final depth-chart read for every battle still open.
Then build, suites, DOM, publish, the seven-room replay, and the runbook.
Budget the morning: today's full ritual took about three hours of session
time; start by 9:00 AM owner-local so the paste, the build and the replay
all land before the afternoon. The 10/13 final check carries the heavy
validation so the morning is pull-only.

## 5. Definition of done for this work order

Each WO has its own after-report and PR, merged, with the branch
fast-forwarded. The final message of each session states, for every WO it
touched: criteria PASS/FAIL with the command's own output, what was refuted,
what regressed (nothing is acceptable), the gaps with provenance, and the
decisions still open. If a WO cannot be completed, say which part, why, and
what it becomes under each resolution. A clean-looking summary of messy work
is a defect.
