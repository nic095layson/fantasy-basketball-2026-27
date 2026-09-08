# After-Report — Data Pull 2026-09-08 — **AMENDED same day**

> **AMENDED TWICE 2026-09-08, on owner integrity challenge.** Round 1 (before
> being told): the pass found and fixed the **Jamal Murray certification error**
> (§1a) plus three smaller report defects. Round 2 (owner supplied the answers):
> the error the owner saw was **Ben Simmons' team — SACRAMENTO, not the
> Clippers** (§1b), and the missed trade was the **9/8 four-player NOP–MEM deal
> with direct Mathurin implications** (§1b) — which ten trade-shaped queries
> failed to surface but a single team-shaped query found immediately once the
> teams were known. §1c analyzes how both failures happened and proposes the
> fixes the owner asked for.

**Pull window: 2026-09-02 → 2026-09-08 (6 days — wider than the design case, sweep widened accordingly).**
Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows sourced;
verified 2026-07-13 .. 2026-09-02`, exit 0.

> **Headline: a quiet window with one loud non-event.** Six days after the NBA
> lifted the hold, **the Kawhi Leonard trade to Toronto still has not been
> formally executed.** The 9/2 report predicted these rows would move this
> pull. They did not, and that prediction is marked wrong below rather than
> quietly dropped.

## 1. NBA roster changes

**Zero placements moved on either plane** — no player changed teams. *(Original
text claimed `players.csv` byte-identical and board diff 0/0/0; true when
written, superseded by the §1a amendment: the Murray tag is a 1-row note-cell
edit — pool `3f51e273c42a`, restamped `--pool-changes` — and the kit board
moved Murray 27 → 30.)* `verify_rosters` **255/255, 0 mismatches, 0
unmatched**, dated 2026-09-08.

Sweep: transaction aggregators (Spotrac, NBA.com offseason tracker, HoopsRumors
via dated search), general weekly transaction searches, an injury/camp sweep,
the FA and RFA rows, every open item from the 9/2 after-report, and the
scripted JUDGMENT enumeration (8 flagged open, each searched). Direct page
fetches to every sports and news domain re-tested were blocked by the egress
policy (ESPN, NBA.com, CBS Sports, CNN, **HoopsRumors**, CP24, The Globe and
Mail) — claims rest on dated search results corroborated across independent
outlets.

### The Kawhi trade: still not executed `[CONFIRMED as of 2026-09-07]`

| source | dated | says |
|---|---|---|
| HoopsRumors, "Significant Transactions That Have Yet To Be Finalized" | Sept 2026 | the trade is on the not-yet-finalized list |
| transaction sweep | **2026-09-07** | still "expected to be finalized **in the next couple of days**" — the same phrasing carried on 9/3 |
| CBS Sports player note (Ingram) | Sept 2026 | "**although the trade isn't yet finalized**, it sounds like Ingram is heading to Los Angeles" |

**Leonard stays LAC; Ingram and Dick stay TOR — a second consecutive hold.**
Their note cells (`league hold LIFTED 2026-09-02, awaiting execution`) remain
accurate and were deliberately **not churned**.

Read carefully, this is not new trouble. The 9/2 ruling is final and
non-appealable, Leonard was neither suspended nor his contract voided, and
**nothing in the window reports a snag** — a six-team-asset trade routinely
sits days awaiting paperwork. What it *is* is a direct vindication of the 9/2
judgment call: the lone aggregator post claiming the deal was "OFFICIALLY
completed" would, if believed, have put the **wrong team on three rows for six
days and counting.**

### In-window transactions — checked, none touches a pool row

| transaction | date | disposition |
|---|---|---|
| **Ben Simmons → SAC** *(CORRECTED — original said LAC off one garbled summary)*, 1yr/~$3.5M, announced 9/4 (AP, NBA.com, ABC, Kings Herald); sat out all of 2025-26 (back/leg) | 9/4 | **Watchlisted, NOT added.** On no row in either plane, no consensus-top-120 or live-room draft evidence, and no 2025-26 statistical base |
| **Paul Reed** (DET) money fully guaranteed, $5.6M | *date not stated by source* | Already a DET row. Same team, no *sourced* role mechanism → no projection edit (§3) |
| Tacko Fall → PHI | 9/1 — **pre-window** (window opened 9/2) | no row |
| John Butler Jr. → MIL · Kobe Stewart → CHA (Exhibit 10) · Grant Nelson → BKN (two-way) | 9/4 | no rows |

### Injury / camp sweep — CORRECTED in the amendment

**§1a — The error (found on integrity challenge, before being told).** The
original version of this section read:

> *"**Jamal Murray** (ruptured Achilles) and **Domantas Sabonis** (Feb meniscus)
> are reported full go for camp — and neither was ever tagged here, so nothing
> changes. Worth stating plainly: the board was already correct."*

That certification was **wrong**, and wrong in the worst way — affirmatively.
The sweep item itself said Murray is returning from a **ruptured right
Achilles** (2025-26; returned a few games after the All-Star break, ~14 games,
per TSN's and ESPN's 2026-27 injury-returns coverage — two independent
summaries). This board's own convention tags **every** Achilles returnee
`inj-achilles-risk` at 0.78 — Haliburton, Lillard, and **Dejounte Murray,
whose tag literally cites the identical profile** ("14 games last season").
Jamal Murray alone stood untagged at availability 1.0, and the report graded
the headline ("full go") instead of the row. **Fixed both planes:**

- **Deck:** `inj-achilles-risk (first season back; ruptured right Achilles
  2025-26; returned post-ASB)` → availability **0.78**, matching the Dejounte
  anchor. Gates, parity (EXACT), and both suites re-run green; artifact
  republished.
- **Kit:** GP **66 → 62** (mechanism: first-season-back Achilles availability,
  anchored to Dejounte Murray's 62; comparables Haliburton/Irving 60, Lillard
  45). Board move: **Jamal Murray 27 → 30**; Jalen Williams, Haliburton and
  Amen Thompson each rise one slot. Scripted diff, no other movement.
- **Domantas Sabonis deliberately NOT tagged** — February meniscus arthroscopy,
  seven months post-op, full go: a routine-recovery class, not the
  rupture/reconstruction class this board tags. Stated for **owner overrule**
  rather than silently decided (D-S8).

Three smaller defects corrected in this same amendment:

1. **Paul Reed's "9/4" date was unsourced** — the sweep summary dated Simmons
   (9/4), Fall (9/1) and the Butler Jr./Stewart/Nelson trio (9/4), but gave
   **no date** for Reed's guarantee; the table inherited 9/4 by adjacency.
   It now reads *date not stated by source*.
2. **Tacko Fall (9/1) was listed as in-window** — the window opened 9/2. His
   signing belongs to the 9/2 pull's window (it touches no row either way).
3. **§5-C4 said "five weekdays" — the window holds four** (Thu 9/3, Fri 9/4,
   Mon 9/7, Tue 9/8).

And one receipt downgraded: the Kawhi table's "**as of 2026-09-07**" line came
from a search summary whose phrasing ("As of September 7, 2026…") may echo the
query date rather than an article date. The claim it supports (trade still
pending) is independently carried by the HoopsRumors not-yet-finalized listing
and the CBS Ingram note, so the conclusion stands — but that cell is now
labeled *summarizer-dated*, not treated as a primary receipt.

The rest of the sweep stands as originally reported:

- **Jimmy Butler** — limited to individual court/strength work at camp, not yet
  cleared for contact. `acl-recovery-jan26 (return ~2027)` **exclusion stands.**
- **Haliburton** and **Irving** already carry `inj-*-risk (first season back)`;
  correctly re-admitted in earlier pulls.
- Adams, Moody, Sharpe, DiVincenzo exclusions unchanged.

**§1b — The owner-reported missed trade: hunted, not recovered.**
`ATTEMPTED-FAILED`, receipts as follows. Ten query shapes were run
(trade-specific weekly sweeps, day-specific 9/5–9/7 queries, HoopsRumors
"in exchange for", ESPN/B-R trade-grade and live-blog content queries, RealGM
day and ledger queries, plus targeted checks on the PHI logjam and the
executed-Kawhi hypothesis). Every trade they surfaced was checked against both
pools and is **already applied**: Morant→POR (Grant + Kris Murray back),
Kessler→LAL, Ayton→WAS (Hardy back), Finney-Smith→CHA, Bogdanović→HOU,
Claxton→CHI, Randle→BKN, Giannis→MIA, LaMelo→MIN, Jaylen Brown→PHI, the
Watson/Whitmore/Strus/Schröder/Tre-Mann chain, Middleton→WAS (sign-and-trade)
— or row-neutral and out of window: Broome→LAC (dated **7/28–7/30** by three
URL slugs; enabled PHI's KCP signing; none of the three touches a row),
Konchar/Cody Williams/Josh Green→UTA (8/29, no rows), J.D. Davison (9/3, no
row). Bound stated plainly: every transaction ledger is egress-blocked to
direct fetch, so this hunt ran entirely on search summaries, which demonstrably
blend eras.

**CLOSED by the owner's answer, and applied.** The missed trade is the
**four-player NOP–MEM deal reported 2026-09-08**: Pelicans send **Jordan
Hawkins**, Micah Peavy, a future second and a second-round swap to Memphis for
**AJ Johnson and Taj Gibson** — executed, per the reporting, to clear ~$5.7M so
New Orleans could **officially complete Bennedict Mathurin's 2yr/$16M
signing** (HoopsRumors "Pelicans, Grizzlies Complete Four-Player Trade"; ESPN
La Crosse 9/8; Daily Memphian; BVM Sports 9/8; Yahoo and Yardbarker trade
grades — multi-source, dated). Applied:

- **Jordan Hawkins NOP → MEM** (deck row + evidence ledger in the same change;
  he has no kit row). `verify_rosters` re-run: 255/255, 0 mismatches.
- **Mathurin narrowed −0.15 → −0.10** — the first *sourced role mechanism*
  since the signing: Hawkins is one of the four backcourt names his discount
  explicitly counted against him, subtracted specifically to fit him in, and
  the signing itself is now cap-final rather than merely agreed. Line still
  held (no minutes source yet).
- Peavy, AJ Johnson and Taj Gibson are on no row in either plane.
- The **Ben Simmons error is also closed**: Sacramento, 1yr/~$3.5M, announced
  9/4, multi-sourced; he sat out all of 2025-26. The original "LAC" came from
  one garbled sweep summary relayed without a second source because he wasn't
  a pool row — see §1c.

**§1c — How these failures happened, and the fixes proposed (owner asked).**

*Failure A — Simmons "LAC": an unverified fact reached the report because
verification is gated on row impact, publication is not.* The
two-independent-sources rule fires only for edits that move a pool row.
Simmons touches no row, so the claim skipped every gate — yet it was still
**published** as fact in the after-report, the colophon, and the PR bodies.
This is the fifth documented search-summary garble (NOP-withdrew-the-QO ×3
refutations, Sochan-to-the-Knicks, stale Hornets Mark Williams, now
Simmons-LAC). The channel is known-noisy; the rule's scope was too narrow.

*Failure B — the NOP–MEM trade: two independent misses stacked.* (1) **Query
shape**: the general sweep was signing-shaped and the open-item checks were
player-name-shaped. This trade is *about* a flagged player's cap room without
being *about* him — "Bennedict Mathurin traded" never matches it, and no
query contained "Pelicans" or "Grizzlies." A team-shaped query finds it
instantly (demonstrated today). (2) **Checklist execution decayed**: the
scripted enumeration flagged 8 open names, but only 5 got dedicated searches;
Mathurin, Sochan and Brunson were bundled into one "nothing in window" line
with **no per-name receipt**. That is the exact discipline created by the
8/26 Mathurin post-mortem — run faithfully on 8/27, 9/1 and 9/2, then
partially skipped on 9/8 — and nothing audits execution, so the skip was
invisible. The same failure recurred on the same player within two weeks.
(A timing caveat is owed: some 9/8 trade coverage may postdate the 16:2xZ
sweep. It does not excuse the miss — the checklist skip is real either way,
and the amendment ran the same day.)

*Failure C — Jamal Murray (found by this audit): the sweep graded headlines,
not rows.* "Full go for camp" was read as "no action" without asking what he
was returning *from*, against a tag inventory where every comparable
returnee is priced at 0.78.

*Common root:* the egress policy makes every fact single-channel (search
summaries), the summaries demonstrably garble, and the system's defenses —
two-source rule, refute-before-apply, per-name enumeration — are each scoped
narrowly (rows, tier-movers, player names) and enforced by session
discipline rather than by anything mechanical.

**Proposed fixes (adopt via D-S9; each is small and checkable):**

| # | fix | mechanism | failure it kills |
|---|---|---|---|
| **F1** | **Receipts contract for open items.** Promote the scan to `scripts/judgment_open_items.py` (D-S5, already validated 18→8) and extend DATA-PULL §2: the after-report MUST carry one receipts row per flagged name (name → query run → dated finding). A flagged name with no receipt = the pull is incomplete | script emits the flag list; a report linter verifies every name appears in the receipts table | B2 — the silent checklist skip |
| **F2** | **Publication gate.** Any named transaction/team/injury fact entering the after-report, colophon, or PR body needs two independent sources **or** an explicit `[SINGLE-SOURCE]` label — regardless of row impact | extend DATA-PULL §5; `scripts/check_report.py` flags transaction lines lacking either | A — Simmons-class garbles shipping as fact |
| **F3** | **Team-shadow sweep.** The open-items list implies a team watch set (each flagged player's team + counterparties of pending deals). Run one team-shaped news query per team in the set, every pull | derived mechanically from the flag list (~6–8 queries) | B1 — trades *about* a player's situation that never name him |
| **F4** | Prose gate on the deck colophon (row count + narrated pull date vs manifest) | = D-S6, already on the sheet | stale hand-authored prose |
| **F5** | **Zero-trade anomaly rule.** A multi-day window returning zero league-wide trades is a sweep-failure signal, not a finding: one ledger-shaped query (RealGM month page / HoopsRumors trades index) is mandatory before writing "no trades in window" | one required query + its receipt in §2 | B1 — quiet-window false negatives |
| **F6** | **Returner-vs-tag two-way diff.** The injury sweep must diff "returning players" coverage against the pool tag inventory both directions: tagged-but-now-cleared AND returning-but-untagged | `judgment_open_items.py` already parses notes; add the tag-side pass | C — Murray-class certification errors |

### Other open items

| item | finding | action |
|---|---|---|
| **Jalen Duren** | Unsigned. Still the **top remaining RFA**; DET at 5yr/~$35M per vs a $40M+ ask — the same ~$5M/yr gap as 9/1. One softer single-sourced item (Yardbarker: "closer than expected"), uncorroborated | hold −0.08; **Oct 1 QO deadline now 23 days out** |
| **Cam Thomas / Jaden Ivey / Lonzo Ball** | still unsigned, no dated event in window | hold |
| **Cam Whitmore** | confirmed UFA by a **third** independent source; on no row | correctly absent |
| **Mark Williams** | **11th quiet pull** | hold — see §4 |
| **Sochan / Brunson / Mathurin** | nothing in window | hold |

## 2. Significant fantasy analysis changes

**Post-amendment: two number changes, both sourced.** *(The original text here
said "none to the numbers"; superseded.)*

- **Bennedict Mathurin −0.15 → −0.10** (§1b mechanism — a named backcourt
  competitor subtracted to complete his signing).
- **Jamal Murray**: deck availability 1.0 → **0.78**, kit GP 66 → **62**
  (§1a); kit board **27 → 30**.

The two cards below were the original pull's holds and stand as written:

- **Kawhi Leonard — held −0.08.** The discount prices last-mile execution plus
  Toronto role integration, and that is *exactly* what is still outstanding —
  neither more nor less than a week ago. Re-widening on delay alone would be
  pricing impatience, not evidence. The card now records the second hold and
  the dated 9/7 status.
- **Jalen Duren — held −0.08.** Nothing moved; the clock did. The card records
  that Oct 1 now falls **inside** the October refresh window rather than beyond
  it, which matters for §6 sequencing.

No projection edits, no line changes, no structural-knob changes, no pool
changes. Board unchanged (diff ran clean).

## 3. A prediction from the last report, marked wrong

The 9/2 after-report and both 9/2 PRs said: *"Expect all three placements to
move next pull."* **They did not move.** The direction of that call is still
supported by every source in this window; only the timing was wrong. It is
recorded here because a system that quietly drops its own forecasts cannot be
calibrated — the same reason the Kawhi card retracts theses by name.

The deck colophon was rewritten for this window (second consecutive pull it has
needed hand-editing), which is the standing argument for **D-S6**.

## 4. Watchlist / open items

- **Kawhi + Ingram + Dick — still the highest-probability pending change.**
  Three rows move on execution, and Ingram's Toronto line, Dick's role and
  Leonard's Toronto role all need repricing when they do. Second pull carrying
  this; if it is still open at the **third**, that is worth treating as signal
  rather than paperwork, and the card should say so.
- **Duren — Oct 1, now 23 days out**, and inside the October refresh window.
  Either an extension or the $9.6M QO; both keep him in Detroit.
- **NEW — Brandon Ingram's heel.** He had **right-heel surgery on 2026-05-08**
  (spur removal; expected ready for camp). His row carries **no monitor tag**.
  Outside this window and availability-neutral, so nothing was edited — but it
  is a genuine coverage gap, flagged for the pull that rewrites his row on
  trade execution (precedent: Brunson's informational `wrist-surgery-monitor`,
  which carries no multiplier).
- **Ben Simmons (SAC — corrected)** — watchlisted, not added; sat out all of
  2025-26. Re-check if camp reporting gives him a rotation role.
- **Jordan Hawkins (MEM — new)** and Mathurin's now-final NOP fit — camp
  reporting reprices both; AJ Johnson (NOP) stays a non-row.
- **Mark Williams — 11th quiet pull.** Diagnosis unchanged and now firmer:
  every hit resolves to 2025-26 Phoenix or Charlotte-era content because camps
  have not opened. On the §6 October must-do list.
- **Camps open late September** — the next pull inside camp week should expect
  real role news (Kuminga usage, Mathurin's NOP role, Ingram, Simmons).
- **September trigger: unchanged, still blocked on owner input** (D-S1, D-S2).
  §1.4 and all §2 experiments held; **zero append-only bars consumed.**
- Carried: Cam Thomas / Ivey / Lonzo unsigned · Sarr/Sharpe cross-plane severity
  mismatches · four deck-draftable names missing from the kit pool + decision D1
  · PHI logjam · Brunson wrist (informational).

## 5. Verification (adversarial pass)

- **C1 — the tempting error this pull was impatience.** After predicting three
  rows would move, the pull that finds them unmoved is under quiet pressure to
  "find" the execution or to re-widen Kawhi to show responsiveness. Neither
  happened: the rows held on dated evidence, the number held because what it
  prices is unchanged, and the failed prediction is written up in §3.
- **C2 — absence of evidence was checked, not assumed.** "No completion news"
  could mean the trade did not close *or* that search recency buried it. That
  is why the finding rests on **positive** dated statements that it is still
  pending (a 9/7 "next couple of days", a not-yet-finalized list, a CBS player
  note) rather than on the absence of a completion story. **Bound:** if the
  deal closed on 9/8 itself, this sweep would not see it.
- **C3 — the injury-return story was checked against the tag list, not the
  headline.** "Biggest injury returns" named Murray and Sabonis; the correct
  action was *nothing*, because neither was tagged. Reading only the headline
  would have produced two pointless edits and a false claim of re-admission.
- **C4 — a six-day window is thinner per-day than a one-day window.** Stated as
  a bound, not waved off: four weekdays of transactions were swept by aggregator
  search rather than day-by-day. Fringe moves (Exhibit 10s, two-ways) are the
  most likely miss class, and none of them reach a 255-row 9-cat pool.
- **C5 — pool-completeness pressure was resisted once.** Ben Simmons is the
  most recognizable name to sign in the window. He was watchlisted under the
  standard already applied to Brandon Williams; adding him because the name is
  familiar would be exactly the ad-hoc pool growth the MUST_HAVE gate exists to
  prevent.
- **Not claimed:** roster verification remains `fallback-partial` against an
  owner-authored ledger (egress policy). Every claim here rests on dated search
  summaries; every direct fetch attempted today was blocked.

## 6. Decision sheet (owner disposes)

| # | decision | recommendation |
|---|---|---|
| **D-S1** | Upload the 2026-27 **projection/ranking datasets** (§1.2b) | unchanged — the input the September plan waits on |
| **D-S2** | Provide **September consensus ADP** (§1.2) | unchanged; a pasted table is enough |
| **D-S4** | **October Routine** (`trig_0146xxp4wAt4uHQypXLxjNZ1`, 2026-10-12 14:00Z) — exists and is armed; its one forced test run aborted | do not recreate; decide between leaving it armed with a manual prompt in reserve, or one more forced test run |
| **D-S5** | Promote the JUDGMENT scan to `scripts/judgment_open_items.py` | yes — validated 9/2, hand-retyped again today |
| **D-S6** | Gate hand-authored deck prose against the current pull (colophon row count + narrated pull date) | **strengthened** — the colophon has now needed manual rewriting two pulls running |
| **D-S9** | **Adopt fixes F1–F3, F5, F6** (§1c) — the receipts contract, the publication gate, the team-shadow sweep, the zero-trade anomaly rule, and the returner-vs-tag diff. F1/F2 add one script each; F3/F5/F6 are DATA-PULL.md text | adopt all five; today produced one shipped false fact and one missed row-moving trade in a single report |
| **D-S8** | **Sabonis tag** — Feb meniscus, full go, deliberately left untagged (routine-recovery class vs the rupture class this board tags). Overrule to `inj-knee-risk` (0.78) if you want surgical recency priced regardless of class | leave untagged |
| **D-S7** | **New. Merge the stack.** Four data-pull PRs are open and unmerged (#24/#15, #25/#16, plus today's), and `main` has not moved since 9/1. DATA-PULL §0 says a pull not pushed to `main` did not happen | merge in order, or say the word and I will consolidate them |

## 7. Gates

All re-run after BOTH amendments: `verify_rosters` **255/255, 0 mismatches, 0
unmatched**, dated 2026-09-08 (Hawkins moved in CSV + evidence as a pair) ·
`check_provenance` exit **0** · `freshness --stamp` green with an explicit
`--pool-changes` assertion (2 rows: Murray note cell, Hawkins team) ·
`build_deck.py` all gates pass, 255 players, pull 2026-09-08, pool
`c98cf4f39840`, injection round-trip byte-identical · `check_parity`
**EXACT MATCH** (2295 z-cells, 64 name fixtures, 72 df_hash vectors, 78 card
orderings) · `test_draft` **53/53** · `test_gates` **12/12** · kit board diff:
**Jamal Murray 27 → 30**, three 1-slot risers, nothing else (Hawkins has no
kit row; Mathurin's line held) · artifact republished at `built: 2026-09-08`
(amended ×2).
