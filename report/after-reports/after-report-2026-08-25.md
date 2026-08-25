# Draft Kit Data Pull — After Report

**Run date:** 2026-08-25 · **Window swept:** 2026-08-21 → 2026-08-25 (4 days)
**Scope:** delta pull under DATA-PULL.md, both planes, ending in a deck republish. Not the October full re-verification. This run also **recovered an orphaned later-8/21 deck build** and **shipped the merged Insert-at-# / RESYNC UI to the live deck for the first time** (see §5).

```
📋 Freshness Check — 2026-08-25
✓ Verified: 3 in-window transactions (DeRozan → DEN 8/21, Klay Thompson
  DAL → MIA 8/23, Shaedon Sharpe torn meniscus 8/24), each with 2+ dated
  outlets from this run; 3 FA statuses re-verified unsigned (Kuminga, Cam
  Thomas, Ivey); Kawhi re-checked (fourth hold); Mark Williams dated out of
  window a sixth time
⚠ Changes since 8/21: kit 3 rows edited (2 team, 1 GP, 1 of them also a
  reprice); deck 3 rows edited + rosters_official re-authored; 0 added,
  0 removed on either plane. ORPHAN RECOVERED: the live deck was a
  later-8/21 build (DeRozan repriced) that never reached git AND predated
  the Insert-# merge; both are reconciled here.
✗ Cannot verify: Cam Whitmore's medical clearance (third quiet pull) ·
  Ivey's FA status by dated news (fifth pull) · Mark Williams' foot (SIXTH
  quiet pull) · all claims rest on search results — sports domains still
  egress-blocked / ESPN 403 (see §0)
```

**Gate:** `check_provenance.py` → **PASS** (exit 0) — all rows sourced; verified 2026-07-13 .. 2026-08-25.
`--max-age-days 14` still **FAILS**, structural and expected (oldest row 2026-07-13); the October full run clears it.

---

## 0. Window and method limits

**The window was 4 days** (8/21 → 8/25). A quiet late-August stretch — three transactions, no trades.

**Research channel unchanged and re-tested.** Sports domains (`basketball-reference.com`, `nba.com`, `site.api.espn.com`) still return no route / EGRESS_BLOCKED; `verify_rosters.py`'s direct ESPN pull 403'd. Web search works. **Fifth consecutive pull on search-derived evidence.** The network-policy fix remains the highest-value change available to this system.

**The two planes were NOT in sync at the start — an orphan was found.** Before overwriting the live deck (lesson 21), I fetched it and compared against git `HEAD`. They had **diverged**:
- git `origin/main` (kit #9 / deck #14): the **morning-8/21** data (DeRozan **FA**), plus the merged **Insert-at-#** feature.
- the **live** artifact: a **later-8/21** build (pool `cebffc96…`) that had **repriced DeRozan down for the Denver signing** — but was published **before** the Insert-# merge, so it **lacked that feature**.

Neither was a superset. This run is the reconciliation point (§5).

## 1. NBA roster changes

**Three transactions, all confirmed with 2+ dated outlets from this run.**

| Player | Change | Date | Sources |
|---|---|---|---|
| **DeMar DeRozan** | FA → **DEN**, 1yr / $3.88M minimum (wing depth) | reported 8/21 | [ESPN](https://www.espn.com/nba/story/_/id/49684447/nuggets-signing-6-all-star-demar-derozan-1-year-deal), NBA.com, NBC Sports, Hoops Rumors, HoopsHype, SI |
| **Klay Thompson** | DAL → **MIA**; waived via buyout 8/21, cleared waivers, 2yr / $11.48M (2027-28 player option) | signed 8/23 | [NBA.com](https://www.nba.com/news/klay-thompson-heat-2026-free-agency), ESPN, Yahoo Sports, Bleacher Report, NBC Sports Bay Area |
| **Shaedon Sharpe** | **torn meniscus, ~6-month timeline**, expected back ~late Feb 2027 (stays POR) | reported 8/24 | [NBC Sports](https://www.nbcsports.com/nba/news/portlands-shaedon-sharpe-tears-meniscus-out-six-months), Yahoo Sports, Bleacher Report, SI, Blazer's Edge |

**FA rows re-verified unsigned this window (no in-window signing):** Kuminga, Cam Thomas, Jaden Ivey. The kit's FA block goes from **four to three**. These were carefully documented as active unsigned free agents in the 8/21 report; a broad search this run surfaced older, pre-window items (a Kuminga rights-transfer, an Ivey waiver) that the disciplined 8/21 record already accounts for — none is an in-window signing, so **no edit**. Their re-verification dates advance to 8/25.

**Checked, dated, correctly NOT edited:** Mark Williams (sixth consecutive quiet pull — every result still 2025-26 season/playoffs); Alex Sarr's foot (June surgery, already `inj-foot-risk`); Kawhi (mid-September Board of Governors still the next checkpoint, before this window's end).

## 2. Projection changes (labeled per Operating Principle 3)

- **DeMar DeRozan — repriced DOWN, both planes.** Kit: PTS 20.5 → 16.0, MPG 32 → 27, FGA 15.5 → 12.5, FTA 5.5 → 4.5, AST 4.0 → 3.6, REB 4.0 → 3.5, TOV 1.8 → 1.7, 3PM 0.9 → 0.8 (efficiency, STL, BLK, GP held). Deck: adopted the recovered later-8/21 line verbatim (21.5 → 16.0 ppg with shots/boards). **Mechanism:** he chose Denver as a **third option next to Jokic and Murray** on minimum-scale money at age 37 — usage well below his Sacramento featured-scorer line. Direction **[LIKELY]**, magnitude **[SPECULATIVE]**. This *replaces* the "hold + reprice-at-preseason" I first drafted, after the orphan recovery surfaced a better, already-published analysis of the same event (§5).
- **Klay Thompson — team label only, line HELD, both planes.** His line was already the reduced floor-spacer profile (kit 12.5 pts / 2.7 3PM), and Miami's role — spacing next to Giannis — is the same role that line assumes. No named mechanism to move it.
- **Shaedon Sharpe — availability only, per-game HELD.** Kit: GP 70 → 18 (a probability-weighted guess: a ~6-month timeline lands ~late Feb, ramp and knee-setback risk pull it toward the low end; realistic range ~0 to ~30). Deck: tagged `knee-recovery`, which zeroes availability and **removes him from the draftable board** — the deck's binary treatment of a serious-injury recovery, more aggressive than the kit's z-model (§3).

## 3. Board movement (computed — engines re-run, baselines diffed by script)

**Draft-kit board.** Regenerated; **byte-identical on a second run** (determinism check). Script-computed diff vs the pre-pull snapshot:
- Entered top-200: **none**. Exited: **none**.
- Moves ≥3 ranks: **one — DeMar DeRozan #112 → #163**, the repriced player himself, exactly as intended. No other player moved ≥3 (the reprice's pool-stat cascade is sub-3-rank everywhere else).
- Klay Thompson **#181 → #181** (team-label edit cannot move a z). Shaedon Sharpe **#135 → #134** (a benign one-rank re-index as DeRozan fell past him).
- **Sharpe's GP cut moved nothing on its own:** his z-total is **negative (−1.65)**, and the availability model does not shrink negatives by absence (documented rule). Recorded in the CSV, invisible on the ranked board — the same pattern as Whitmore's 8/21 GP cut. The deck handles the same player differently (below).

**Deck board.** Script-computed against the pre-edit (git `origin/main`) pool:
- **Exited: Shaedon Sharpe** (was #186 pre-reprice / #152-region context; `knee-recovery` → availability 0 → excluded). Entered: none.
- Moves ≥3 ranks: **one — DeMar DeRozan #107 → #152** (the reprice). No other player moved ≥3.
- Ranked pool 238 → 237 (Sharpe removed); the players below him shift up one — a pure re-index, no z changed.

**Cross-plane note (flagged, not "fixed"):** the two planes now treat Sharpe at different severities — the kit keeps a negative-z row at GP 18, the deck excludes him entirely. Both are internally consistent with their own models (z-with-negative-invariance vs. binary availability tags). This is the same class of gap flagged for Alex Sarr on 8/21; worth reconciling in October, out of scope for a delta pull.

**Engine header (§4 — the board must not contradict itself).** The kit engine's FA caveat named DeRozan as still-FA; my change falsified it, so it was rewritten in the same pull: DeRozan recorded as leaving the FA block 8/21 with his terms and the down-reprice, the FA count corrected to **three**, and a new line added for Klay's DAL → MIA move and Sharpe's GP cut. Kawhi's note incremented to a fourth consecutive hold.

## 4. Watchlist / open items

- **Cam Whitmore — medical clearance still unresolved,** third quiet pull. No source says he has been cleared from the DVT, or where (or whether) he has signed since the Cleveland waive-and-stretch. If waived-and-unsigned by October, delete the kit row rather than discount further.
- **Kawhi Leonard — HELD at 35 GP / −0.20 for the FOURTH consecutive pull.** Nothing new in-window; the mid-September Board of Governors meeting remains the checkpoint — it falls *after* this window, so the next pull is the first that can move it.
- **Mark Williams' foot — SIXTH consecutive quiet pull.** Every result is still 2025-26 season/playoffs. His 58-GP kit discount and `inj-risk` deck tag have stood unexamined since 7/27. **This is an October must-do, not a watchlist line.**
- **Alex Sarr cross-plane severity mismatch** (deck `inj-foot-risk` ×0.78 vs kit 72 GP) — unchanged, carry to October. **New sibling: the Sharpe cross-plane treatment** (§3) joins it.
- **Four deck-draftable names still missing from the kit's 220-row pool** — D'Angelo Russell, Al Horford, Cedric Coward, Deandre Ayton, plus Peyton Watson — and **owner decision D1** (does a committed, gate-verified deck projection count as a sourced base rate for the kit?) remains open. Nothing this window bears on it.
- **Jaden Ivey** — fifth pull on contract-tracker evidence only; still the board's weakest label, still says so on the board.
- **PHI logjam** unchanged as the board's biggest projection-uncertainty cluster.
- **Process scar (new): the later-8/21 orphan.** A pull that republishes the live deck without committing to git leaves the two surfaces diverged and invisible to the next session — exactly lesson 10 + lesson 21. This run recovered it, but the recovery cost a full orphan diff. **The next data pull should first `git show`-diff the live manifest against `HEAD` before doing anything else.**

## 5. Deck plane (§7) + orphan recovery

Deck-plane window 8/21 → 8/25. **The orphan is the headline.** The live deck (`built: 2026-08-21`, pool `cebffc96…`) was a *later-8/21* build that had repriced DeRozan for the Denver signing but **was published before the Insert-# / RESYNC merge** (deck #14), so it lacked that feature. git `origin/main`, conversely, **had** the feature but carried the morning-8/21 DeRozan-FA data and had never been republished. A structured per-player diff proved the **only** uncommitted data change in the live build was DeRozan (team + repriced line); every other player differed only by the sub-3-rank pool-stat cascade, and the engine diff was exactly the absent Insert-# code.

**Reconciliation applied here:**
- **Recovered** DeRozan's repriced line verbatim into the deck pool (16.0 ppg with shots/boards) and his judgment card (adj −0.05, reasoning adopting the reprice), so the owner's live surface keeps the analysis it has shown since 8/21 rather than snapping back to a stale FA-priced line.
- **Ported** the same reprice to the kit plane for cross-plane consistency (§2).
- The republish therefore ships a true **superset**: the Insert-# / RESYNC UI (new to the live deck) **+** the recovered DeRozan reprice **+** this window's Klay → MIA and Sharpe-out.

Other deck edits this window: `data/players.csv` — Klay DAL → MIA (label), Sharpe `knee-recovery` note. `data/rosters_official.json` re-authored for 8/25 (DeRozan added to Denver, Klay moved Dallas → Miami, full window write-up in `source`). JUDGMENT re-authored and re-dated 2026-08-25: DeRozan rebased to the recovered reprice (−0.05); Klay rebased from a team-unsettled discount to age/bench residual (−0.10); Kuminga / Cam Thomas / Ivey FA re-verification advanced to 8/25 (three FA rows, not four); Kawhi fourth consecutive hold recorded.

Gates: `verify_rosters.py` **245/245, zero mismatches, zero unmatched**, dated 2026-08-25 (fallback-partial — direct ESPN pull 403'd, reported not swallowed). `freshness --stamp` green with the pool-changes assertion recorded. `build_deck.py` green, injection round-trip OK, pool `e63457ae39d9…`. `check_parity.py` **EXACT MATCH** (245 rows, 2205 z-cells, 72 df_hash vectors bit-identical, 78 card orderings across 6 states). `test_gates.py` **10/10**. `test_draft.py` **39/39** (Insert-# feature regression intact).

Deck **republished to the existing artifact URL** (`…/artifact/190e2c13-…`) and verified live by re-fetching: `built: 2026-08-25`, `evidence_date: 2026-08-25`, pool hash `e63457ae39d9…` matching the local build, and the Insert-at-# control + `108+` token + RESYNC button all present in the served HTML. `git status` checked on both repos before committing (lesson 20).

## 6. Assumptions & deviations

- **A1 — Branches restarted from `origin/main`.** The kit PR #9 and deck PR #14 are both **merged**, so per the standing branch instruction this follow-up work starts fresh: the kit branch `claude/market-data-workorder-mnfi2b` was reset to `origin/main` (its prior content was byte-identical to the squash-merge — nothing lost), and the deck work is on a new branch `claude/data-pull-2026-08-25` off `origin/main`. New PRs, not the merged ones.
- **A2 — DeRozan repriced, not held.** I first drafted a held-line + reprice-at-preseason treatment; the orphan recovery surfaced a better, already-published down-reprice for the same event, and preserving live work (lesson 21) plus the stronger analysis both point to adopting it. Stated in §2/§5.
- **A3 — Sharpe's 18 GP is a probability-weighted guess,** stated with its range in §2. The deck's binary `knee-recovery` exclusion and the kit's GP 18 encode the same injury at different resolutions (§3).
- **A4 — "Signed/agreed" treated as final** for team labels (DeRozan, Klay), consistent with prior pulls (Harden 8/21, Beal 8/13).

## 7. Verification report (adversarial-verify)

**Criteria** — C1 dated sources from this run, 2+ outlets for tier-movers: **PASS** (DeRozan 6, Klay 5, Sharpe 5). · C2 CSV team edits paired with provenance, gate exit 0: **PASS**. · C3 board movement computed by script on both planes, kit board byte-identical on a determinism re-run: **PASS**. · C4 labels honest (direction vs magnitude): **PASS** (§2). · C5 deck gates green, verification dated today: **PASS** (245/245, parity EXACT, gates 10/10, draft 39/39). · C6 republished to the **existing** URL at `built: 2026-08-25` and verified by re-fetching, Insert-# UI confirmed live: **PASS**. · C7 both repos pushed: **PASS** (§6, A1).

**Refutation — attacks that found something.**
- **The orphan check earned its keep.** Fetching the live deck before overwriting caught that it was a divergent later-8/21 build — a silent republish would have either destroyed the DeRozan reprice or shipped the Insert feature without the current data. The structured per-player diff (not an eyeball) is what proved the recovery scope was exactly one player.
- **Re-checking the engine caveat against my own edit** caught that it still named DeRozan as FA — fixed in the same pull.
- **Reading the 8/21 watchlist before trusting a broad FA search** stopped me from acting on pre-window Kuminga/Ivey items the summarizer conflated as fresh.

**Attacks that found nothing.** Kit-board determinism (byte-identical). Deck injection round-trip. JS↔Python parity (EXACT, 6 states). Post-republish manifest + hash equality against the local build. Insert-# regression (39/39). `git status` on both repos.

**Regressions.** None. Both boards moved only where intended; both repos green at final state.

**Status — delivered.** The weakest parts of this report, in order: **the later-8/21 orphan** and the process gap that created it (§4, §5); **Sharpe's 18-GP figure and its cross-plane split** (§2, §3, A3); the **search-only evidence channel** (§0); and **Mark Williams' sixth unexamined pull** (§4).
