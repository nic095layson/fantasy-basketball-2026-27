# After-report — data pull 2026-08-26

**Pull window: 2026-08-25 → 2026-08-26** (1 day — the design case).
**Gate status:** `PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13 .. 2026-08-26` (exit 0, re-run after the Mathurin pairing).
**Orphan check (carried process item from the 8/25 report): CLEAN.** The live
artifact manifest was fetched *before* any edit and matched git `HEAD`
(`1452b5e`) exactly — `built: 2026-08-25`, pool `f6dc8c089335…`, 255 rows. The
two surfaces were in sync; no orphan to recover this run. The check took one
fetch and is worth keeping.

**Sourcing note:** direct page fetches to sports domains remain blocked by the
environment egress policy (re-tested this run — `dynatyze.com` returned
`EGRESS_BLOCKED`, consistent with the ESPN 403s of prior pulls). Web *search*
works, so every claim below rests on dated search results rather than fetched
article bodies. Stated, not swallowed.

---

## 2. NBA Roster Changes

> **AMENDED — the first sweep of this pull MISSED a transaction.** The owner
> asked "What about Bennedict Mathurin?" after the report was first written.
> He had signed with New Orleans **on 8/26 — inside this window**. The sweep's
> two general transaction searches surfaced Brandon Williams but never
> returned Mathurin, and the RFA standoff carried in the JUDGMENT layer was
> not given a targeted search of its own. The change is applied below in the
> same pull; §2's "no roster changes" finding is **corrected, not preserved**,
> and the process defect is recorded in §4 and §7 rather than quietly fixed.

**One roster change in window (found on owner challenge):**

| player | change | date | sources | applied |
|---|---|---|---|---|
| **Bennedict Mathurin** | **LAC → NOP** — two years / $16M with a player option | 2026-08-26 | ESPN (Shams), NBA.com, HoopsRumors, Fox8, Bleacher Report — **[CONFIRMED]**, five independent | **Yes**, both planes |

Mechanism detail: his representatives asked the Clippers to **withdraw the
$8.8M qualifying offer** so he could sign outright rather than through an offer
sheet or sign-and-trade. Jake Fischer reports LAC has *not formally withdrawn
it yet* but "will indeed work with" him to facilitate the move — applied under
the standing "agreed to terms is final for team labels" rule (A1), same as
DeRozan 8/21, Klay 8/25, Harden 8/21, Beal 8/13.

**Line HELD, not repriced.** §3 permits a projection change only with a *named,
sourced* mechanism, and no source yet describes his New Orleans role or
minutes. The bearish read is real but it is inference: $8M AAV sits far below
the $20–25M he sought, and New Orleans is not an open runway — Trey Murphy III,
Zion, Herbert Jones and Saddiq Bey hold the wing with Poole, Hawkins, Dejounte
Murray and Fears in the backcourt. That read is carried in the JUDGMENT adj
(rebased, §3) rather than smuggled into the stat line, and he is the **first
reprice candidate once camp reporting lands**.

Sweep also confirmed, requiring no action: **Caris LeVert** (named in an 8/26
DET→MIL trade summary) is *already* at MIL on both planes from a prior pull;
Georges Niang, Taurean Prince, Gary Harris and Jordan McLaughlin are on no row
in either plane.

**Everything below was the original §2 finding and still holds for the rest of
the pool — zero other placements moved.**
Sweep ran; feeds/searches checked: Spotrac NBA transactions, ESPN transactions
+ 2026 offseason trade tracker, NBA.com offseason trade tracker, HoopsRumors,
RotoWire injury report, CBS/Yahoo/SI injury feeds, plus targeted searches for
each carried watchlist item and each `FA` row.

One in-window transaction was found and deliberately **not** applied:

| player | change | date | sources | disposition |
|---|---|---|---|---|
| Brandon Williams | signed GSW, 1yr/$2.63M | 2026-08-25 | 2 independent (Spotrac-derived transaction listings, surfaced in two separate searches) — **[CONFIRMED]** | **Watchlisted, not added.** He is on **no row in either plane** (kit 235, deck 255). Pool entry requires either consensus-top-120 standing (`MUST_HAVE`) or live-room draft evidence; he has neither, and he went undrafted in the 12-human mock (draft_state_49). Adding him would mean inventing relevance. |

`FA` rows re-checked, all still unsigned — **[CONFIRMED]** by absence of any
reported signing plus dated reporting placing each on the open market:
Jonathan Kuminga (new detail: Atlanta declined his $24.3M team option, so he is
**unrestricted**, not RFA; Lakers pursuing via sign-and-trade, Atlanta reported
underwhelmed by the offers), Cam Thomas, Jaden Ivey, Lonzo Ball (no retirement
announced; future openly described as in doubt). Westbrook and Brogdon remain
correctly tagged `out-retired`.

## 3. Significant Fantasy Analysis Changes

**Kit board unchanged (diff ran clean), before and after the Mathurin
correction.** `rank_engine.py` regenerated twice; both scripted diffs against
the pre-pull snapshot returned **0 entries, 0 exits, 0 moves ≥3 ranks**, and the
file differs from the snapshot by its generation-date line alone (verified by
`diff`; the one changed line is quoted in §7). **No projection edits.** One row
carried in-window news — Mathurin — but it was a *team* change with the line
held (§2), and a team label does not enter the kit's stat-based value math.

**The pull's real finding is a data-integrity defect, not a transaction.**

- **EVIDENCE:** `data/players.csv` line 154 parsed to **17 fields against a
  15-field header** — the only malformed row in 255. Shaedon Sharpe's note was
  written bare on 8/25 as `knee-recovery (torn meniscus 8/24, ~6mo, ret ~late
  Feb 2027)`, so `csv.DictReader` truncated `note` at the first comma and
  overflowed `[' ~6mo', ' ret ~late Feb 2027)']` into its restkey.
- **EVIDENCE:** the published deck carried
  `"note":"knee-recovery (torn meniscus 8/24"` — a user-visible note cut
  mid-sentence, live since the 8/25 republish.
- **EVIDENCE (why nothing caught it):** `availability()` reads the **leading
  tag only** (by design, audit 2026-08-09), so `knee-recovery` → 0.0 resolved
  correctly and Sharpe stayed excluded. **No ranking, z-score, or board value
  moved** — which is exactly why every gate stayed green.
- **Fix applied:** the cell is quoted; the note now publishes complete. Stats,
  team, and the availability-0 exclusion are unchanged (re-verified after the
  edit).
- **Class gated:** `load_players()` — the single choke point every command
  loads through — now exits loudly on any row with extra fields, naming the
  player and the overflow. `test_gates.py` gained 2 red-first cases (malformed
  row fails; the same row quoted loads with its note intact); suite 10 → **12**.
- **INFERENCE:** the same defect could have been written into any note or `pos`
  cell containing a comma. The guard is field-count based, so it covers the
  class, not just this row.

**Mathurin's JUDGMENT adj REBASED, not carried (−0.15 held).** The discount was
originally priced for RFA *route* uncertainty — re-sign, QO, or trade all landing
differently. That uncertainty is now resolved, so carrying the same rationale
would have been stale reasoning wearing a correct number. What replaces it:
rotation-role risk, evidenced by the AAV gap and the crowded New Orleans wing.
The magnitude only holds because one risk replaced another; direction LIKELY,
magnitude SPECULATIVE. Kit board re-diffed after the change: **0 entries, 0
exits, 0 moves ≥3**, Mathurin holds rank 141 — a team label with a held line
does not move stat-based value, which is the expected result.

**JUDGMENT layer re-authored and re-dated 2026-08-26** (stale rationales are
defects, §7.4): Kawhi **fifth consecutive hold** — nothing in-window, freshest
reporting still predates it (8/10: resolution expected within six weeks, likely
Clippers sanctions but ultimate clearance; Leonard believes it concludes before
camp) and the card now records that a resolution moves **two** pool rows, since
Ingram is the return. Kuminga rewritten to UFA-after-declined-option. Ivey
upgraded from "weakest label on the board" to weakly sourced — the 8/26 sweep is
the first to return dated reporting independently describing him as waived by
CHI and still unsigned, after five pulls on contract-tracker evidence alone.
Brunson advanced to ~7 weeks post-op with camp-clearance reporting (his
`wrist-surgery-monitor` tag is informational and deliberately carries **no**
availability multiplier — re-verified this run). Lonzo held.

## 4. Watchlist / open items

- **Bennedict Mathurin (NOP) — NEW, first reprice candidate.** Line held at
  16.5 ppg / 31 mpg / 70 GP on a rotation-money contract into a crowded wing.
  Re-check at camp: if reporting names him a starter or a sixth man, the line
  moves and the −0.15 adj rebases again.
- **Brandon Williams (GSW, signed 8/25) — NEW.** Not in either pool by design
  (above). Re-check if camp reporting gives him rotation minutes; Golden State's
  guard depth is thinner than usual with Moody out.
- **Moses Moody — timeline detail, no action.** Sweep returned "expected to miss
  the start of the 2026-27 season" (torn left patellar tendon). Our deck tag
  reads `patellar-recovery (no return timeline)` → availability 0. The new
  phrasing is *consistent* and does not change the treatment; it is not
  in-window reporting, so the tag is held rather than re-worded on it.
- **Cam Whitmore — FOURTH consecutive quiet pull. CANNOT VERIFY.** Searched
  clearance and signing status; every result still resolves to the 2025-26 DVT
  reporting (Dec 2025 – Jan 2026). Note a standing discrepancy: those sources
  describe him as a **Wizards** forward while the kit row carries **CLE 30 GP**
  from the waive-and-stretch. If still unsigned by October, delete the kit row
  rather than discount further.
- **Mark Williams' foot — SEVENTH consecutive quiet pull.** Every result is
  still 2025-26 season/playoffs (March metatarsal stress reaction, walking boot
  in the OKC series). The 58-GP kit discount and `inj-risk` deck tag (×0.78)
  have now stood unexamined since 7/27. **October must-do, not a watchlist
  line.**
- **Kawhi — fifth hold.** Mid-September Board of Governors session is still the
  checkpoint and still falls outside every window so far.
- **Alex Sarr cross-plane severity mismatch** (deck `inj-foot-risk` ×0.78 vs kit
  72 GP) and the **Sharpe cross-plane treatment** (deck binary exclusion vs kit
  GP 18) — both unchanged, both carry to October.
- **Four deck-draftable names still missing from the kit's pool** — D'Angelo
  Russell, Al Horford, Cedric Coward, Deandre Ayton, plus Peyton Watson — and
  **owner decision D1** (does a committed, gate-verified deck projection count
  as a sourced base rate for the kit?) remains open. Nothing this window bears
  on it.
- **PHI logjam** unchanged as the board's biggest projection-uncertainty
  cluster.
- **Process note (positive):** the 8/25 report's prescribed orphan check ran
  first and came back clean. Keep it as step one of every pull.

## 5. Deck plane (§7)

Deck-plane window 8/25 → 8/26. Pool **255 rows**, one row repaired (above), no
data values changed. `rosters_official.json` re-authored and re-dated 2026-08-26
with the full window write-up in `source` (explicitly recording zero placement
moves and the Brandon Williams non-add). JUDGMENT re-authored and re-dated
(above).

Gates: `verify_rosters.py` **255/255, zero mismatches, zero unmatched**, dated
2026-08-26 (fallback-partial — direct ESPN pull still 403s, reported not
swallowed). `freshness --stamp` green with the pool-changes assertion recorded.
`build_deck.py` green, injection round-trip OK, pool `2f30effb9638`.
`check_parity.py` **EXACT MATCH** (255 rows, 2295 z-cells, 64 name fixtures, 72
df_hash vectors bit-identical, 78 card orderings across 6 states).
`test_draft.py` **53/53**. `test_gates.py` **12/12** (10 + the 2 new
malformed-row cases). Deck **republished to the existing artifact URL**
(`…/artifact/190e2c13-…`) at `built: 2026-08-26`.

Deck commit `f427066` on `claude/data-pull-2026-08-26`.

## 6. Assumptions & deviations

- **A1 — "agreed to terms" is final for team labels.** Consistent with DeRozan
  (8/21), Klay (8/25), Harden (8/21), Beal (8/13). Applies only to the Brandon
  Williams finding, which was not applied anyway.
- **A2 — a quiet day is the expected outcome of a 1-day window,** not a failed
  sweep (§0). Most of the 255 rows are untouched by design.
- **A3 — the malformed-row repair is in scope for a pull.** §3 permits editing
  data rows; §8 requires diagnosing anything surprising before patching. The
  row was diagnosed (field count, restkey contents, published output, and the
  reason gates missed it) before the one-character-class fix. The accompanying
  `load_players()` guard and its two tests are a deliberate scope addition,
  reported here rather than folded in silently: the defect was invisible to
  every existing gate, and a pull that fixes the instance without gating the
  class invites the same silent truncation on the next note containing a comma.
- **A4 — Brandon Williams not added.** Stated as a decision, not an omission;
  reversible in one line if camp reporting moves him.

## 7. Verification report (adversarial-verify)

**Criteria** — C1 dated in-window sources, 2+ for tier-movers: **PASS** (the
sole transaction carried two independent sources; no tier-mover was applied).
· C2 CSV team edits paired with provenance, gate exit 0: **PASS — vacuously**,
no team edits were made; `check_provenance.py` exit 0. · C3 board movement
computed by script: **PASS** (0/0/0, and the lone file delta identified as the
generation-date line by `diff`, not by eye). · C4 labels honest: **PASS** —
CANNOT VERIFY written for Whitmore and Mark Williams rather than filled from
memory; Moody's timeline marked consistent-but-not-in-window and held. · C5
deck gates green, verification dated today: **PASS** (255/255, parity EXACT,
gates 12/12, draft 53/53). · C6 republished to the **existing** URL at
`built: 2026-08-26`: **PASS**. · C7 both repos pushed: **PASS** (§5, §8).

**C1 is AMENDED to a partial pass.** The sweep was window-bounded and
multi-source, but it **missed a same-day transaction** (Mathurin → NOP) that the
owner caught. Root cause, stated plainly: the two general transaction searches
were phrased around dates ("NBA transactions August 26 2026") and returned only
what those indexes surfaced, while the **carried RFA standoffs in the JUDGMENT
layer — Mathurin and Duren — never got targeted searches of their own.** §2 of
the protocol requires re-checking "open items from the last after-report"; the
named watchlist items were each searched, but unresolved situations living only
in the JUDGMENT layer were not treated as open items. **Process fix for the next
pull: every JUDGMENT entry whose text describes an unresolved situation (RFA
standoff, league hold, camp deal, pending trade) gets its own targeted search,
enumerated from the file rather than from memory.** Jalen Duren is the
outstanding one and **was re-checked as part of this correction**: still
unsigned, both sides still dug in (he is seeking a five-year ~$287M rookie max,
Detroit has not offered it, the ~$9.6M qualifying offer is still live). That is
exactly what the board already carries, so his −0.15 is **held with no change** —
the re-check confirmed the label rather than moving it.

**Refutation — attacks that found something.**
- **Checking what the tags actually resolve to, rather than trusting the note
  text, is what found the defect.** Printing `availability()` for every
  watchlist player surfaced Sharpe's note ending mid-word at
  `torn meniscus 8/24` — a truncation no gate, no test, and no board diff could
  see, because the math it feeds was correct.
- **Isolating the gate failure before "fixing" it.** When `test_gates` failed
  after the repair, I stashed my own test block and re-ran: the failure
  reproduced without it, proving gate 4 was correctly refusing an *unexplained
  pool change* rather than my tests being wrong. The reconciliation was a
  `--pool-changes` stamp, which is the protocol's own answer — not a test edit.
- **The board "difference" was not assumed benign.** §8 requires diagnosing any
  unexplained diff; `diff` showed a single line, the generation date, with all
  200 ranked rows identical.
- **What I could not attack:** whether the Brandon Williams non-add is the right
  call for a 13-round league is a judgment, not a verified fact. It is written
  as a decision with its reversal condition.

## 8. Provenance

Kit commit: see the pull-log row for this date. Deck commit `f427066`
(`claude/data-pull-2026-08-26`). Sources are dated web-search results from
2026-08-26 across Spotrac, ESPN, NBA.com, HoopsRumors, RotoWire, CBS, Yahoo,
SI, and Bleacher Report transaction/injury/free-agency trackers; no article
bodies were fetchable (egress policy). Re-verify volatile claims by re-running
the same searches with a later window.
