# After-Report — Data Pull 2026-09-08

**Pull window: 2026-09-02 → 2026-09-08 (6 days — wider than the design case, sweep widened accordingly).**
Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows sourced;
verified 2026-07-13 .. 2026-09-02`, exit 0.

> **Headline: a quiet window with one loud non-event.** Six days after the NBA
> lifted the hold, **the Kawhi Leonard trade to Toronto still has not been
> formally executed.** The 9/2 report predicted these rows would move this
> pull. They did not, and that prediction is marked wrong below rather than
> quietly dropped.

## 1. NBA roster changes

**Zero placements moved on either plane. `data/players.csv` is byte-identical**
(sha `9b2316a313de`, stamped `--no-pool-changes`). Board diff **0 entries /
0 exits / 0 rank moves of any size**; regenerated board differs from the
snapshot by its generation-date line alone. `verify_rosters` **255/255, 0
mismatches, 0 unmatched**, dated 2026-09-08.

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
| **Ben Simmons → LAC**, 1yr/$3.52M | 9/4 | **Watchlisted, NOT added.** On no row in either plane, no consensus-top-120 or live-room draft evidence — the same standard applied to Brandon Williams on 8/26 |
| **Paul Reed** (DET) money fully guaranteed, $5.6M | 9/4 | Already a DET row. Same team, no *sourced* role mechanism → no projection edit (§3) |
| Tacko Fall → PHI | 9/1 | no row |
| John Butler Jr. → MIL · Kobe Stewart → CHA (Exhibit 10) · Grant Nelson → BKN (two-way) | 9/4 | no rows |

### Injury / camp sweep — no exclusion changes

The standing rule removes `*-recovery` players from the pool and re-admits them
only on confirmed return, so every "biggest injury returns" item was checked
against the tag list:

- **Jamal Murray** (ruptured Achilles) and **Domantas Sabonis** (Feb meniscus)
  are reported **full go for camp** — and neither was ever tagged here, so
  nothing changes. Worth stating plainly: the board was already correct.
- **Jimmy Butler** — limited to individual court/strength work at camp, not yet
  cleared for contact. `acl-recovery-jan26 (return ~2027)` **exclusion stands.**
- **Haliburton** and **Irving** already carry `inj-*-risk (first season back)`;
  correctly re-admitted in earlier pulls.
- Adams, Moody, Sharpe, DiVincenzo exclusions unchanged.

### Other open items

| item | finding | action |
|---|---|---|
| **Jalen Duren** | Unsigned. Still the **top remaining RFA**; DET at 5yr/~$35M per vs a $40M+ ask — the same ~$5M/yr gap as 9/1. One softer single-sourced item (Yardbarker: "closer than expected"), uncorroborated | hold −0.08; **Oct 1 QO deadline now 23 days out** |
| **Cam Thomas / Jaden Ivey / Lonzo Ball** | still unsigned, no dated event in window | hold |
| **Cam Whitmore** | confirmed UFA by a **third** independent source; on no row | correctly absent |
| **Mark Williams** | **11th quiet pull** | hold — see §4 |
| **Sochan / Brunson / Mathurin** | nothing in window | hold |

## 2. Significant fantasy analysis changes

**None to the numbers. Both live cards HELD, both rationales rebased.**

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
- **Ben Simmons (LAC)** — watchlisted, not added. Re-check if camp reporting
  gives him a rotation role.
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
  a bound, not waved off: five weekdays of transactions were swept by aggregator
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
| **D-S7** | **New. Merge the stack.** Four data-pull PRs are open and unmerged (#24/#15, #25/#16, plus today's), and `main` has not moved since 9/1. DATA-PULL §0 says a pull not pushed to `main` did not happen | merge in order, or say the word and I will consolidate them |

## 7. Gates

`verify_rosters` **255/255, 0 mismatches, 0 unmatched**, dated 2026-09-08 ·
`check_provenance` exit **0** · `freshness --stamp` green with an explicit
`--no-pool-changes` assertion (correct — the CSV is byte-identical) ·
`build_deck.py` all gates pass, 255 players, pull 2026-09-08, pool
`9b2316a313de`, injection round-trip byte-identical · `check_parity`
**EXACT MATCH** (2295 z-cells, 64 name fixtures, 72 df_hash vectors, 78 card
orderings) · `test_draft` **53/53** · `test_gates` **12/12** · board diff
**0/0/0** · artifact republished at `built: 2026-09-08`.
