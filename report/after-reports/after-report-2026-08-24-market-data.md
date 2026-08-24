# External Market Data → Pass E — After Report

**Run date:** 2026-08-24 · **Scope:** the market-data work order (`report/market-data-workorder.md`),
§3 **steps 1–4 only** — fetch, normalize, join behind the hard unmatched-name gate, and produce the
disagreement + Pass-E arbitrage tables for owner adjudication. **Step 5 (`marketRanks`) was NOT
touched** — it is owner-gated and lives in the deck repo, out of this session's scope (§5 below).

**This is NOT a routine data pull.** No news was swept, no projection or team label was edited, the
board was not regenerated, and **no `pull-log.md` row was added** — deliberately: adding one would
advance the staleness window to 8/24 and hide 8/22–8/24 news from the next real pull. The next
routine pull's window still correctly starts **2026-08-21** (the last logged pull).

**Gate:** `report/check_provenance.py` → **PASS** (exit 0) — untouched; I edited nothing under the
provenance gate's scope. The market files carry their own provenance in `report/market/provenance.csv`.
`report/market/build_market.py` → **GATE PASS** (exit 0) — every one of the 220 pool players is
matched or a documented absence.

---

## 0. Channel verification (work order §0 — verified, not assumed)

Ran the §0 probe. **The channel the owner opened on 8/21 is live for what this job needs:**

```
statdunk.com                     200
hashtagbasketball.com            200
www.basketball-reference.com     200
site.api.espn.com                403
www.nba.com                      403
```

statdunk and hashtag both resolve — the two sources this work order asked for. ESPN/NBA remain 403
(the four-pull-old degradation), but neither is a source here, so this job is unblocked. **No
artifact/orphan check was needed** (§0's second paragraph) because nothing is republished this
session — the deck plane is untouched.

**One egress finding worth the owner's attention.** statdunk.com is allowlisted, but statdunk's data
backend is **not**: its SPA reads projections directly from `uajisozzfvtqfselbfri.supabase.co`, and
the proxy rejects that host (`connect_rejected`, gateway 403). I reached statdunk's numbers through
its **same-origin** API routes on the allowlisted domain instead (`/api/statdunk-nba-projections*`).
The consequence is in §2: statdunk's *pre-computed* category board is only served from Supabase, so
it could not be pulled directly — only reconstructed. **If the owner adds
`uajisozzfvtqfselbfri.supabase.co` (or `*.supabase.co`) to the allowlist, a future pull can take
statdunk's published category ranks verbatim instead of reconstructing them.**

## 1. What was landed (`report/market/`)

| File | Rows | What it is |
|---|---|---|
| `hashtag-2026-08-24.csv` | 429 | Normalized §4 schema + `adp,htag_rank,htag_total` (Yahoo ADP) |
| `statdunk-2026-08-24.csv` | 250 | Normalized §4 schema + per-category z-scores + `rank_avg/value_avg` |
| `provenance.csv` | 2 | `source,url,fetched_on,rows,notes` per §4 |
| `unmatched-2026-08-24.md` | — | **Hard gate** (§3.3): every unmatched pool player, with team + reason |
| `disagreements-2026-08-24.md` | — | Owner-adjudication tables (§3.4 lines + ordering; §5.3 values/fades) |
| `hashtag-raw-2026-08-24.html` | — | Raw snapshot (dated, §3.1) |
| `statdunk-raw / -v2-raw / -v3-raw-2026-08-24.json` | — | Raw snapshots (three statdunk releases; §2) |
| `fetch_market.py`, `build_market.py` | — | Reproducible fetch (network) + deterministic build (offline) |

## 2. Schema adjustments and the statdunk reconstruction (§4 requires I say so)

**Hashtag — added columns, none dropped.** The live table exposes exactly the §4 line
(`gp,mpg,fg_pct,fga,ft_pct,fta,tpm,pts,reb,ast,stl,blk,tov`), where FG%/FT% cells carry `pct
(makes/attempts)` so `fga`/`fta` come straight from the parenthetical. I **added** `adp`
(Yahoo — `DDPOSFROM=1`, the client's platform per INPUTS default and PROMPT.md Pass E),
`htag_rank` (their R#), and `htag_total` (their value). ADP is the whole point of Pass E, so it is
kept, not dropped. Two live-page mechanics had to be handled: the full list is an ASP.NET postback
(`DDSHOW=All`), and the nine category **display checkboxes must be submitted as `on`** — an empty
value silently collapses the table to 8 columns and zeroes every value (found and fixed;
`fetch_market.py`). 241 of 429 rows have blank ADP — genuinely undrafted in the Yahoo consensus
(verified against the raw), correctly excluded from the arbitrage.

**Statdunk — the reachable published board is stale and broken; the fresh board has no category
values; so category value is reconstructed and validated.** This is the one real complication:

- The **only** statdunk endpoint that ships a pre-computed category block
  (`/api/statdunk-nba-projections`) is a **stale "provisional" artifact** (`asOf 2026-08-11`) whose
  player universe is broken — it omits most stars (Kessler, DeRozan, Dejounte Murray, Smart,
  Robinson, Strus…) and ranks obscure rookies absurdly high (Bez Mbeng #41). Unusable as "statdunk's
  board."
- The **freshest** full-coverage release (`/api/statdunk-nba-projections-v2`, "Projections V4.10",
  `asOf 2026-08-23`) has the stars and correct ranks but exposes **no** category block — that lives
  only in the off-allowlist Supabase backend (§0).
- So I reconstruct statdunk's category value from the V4.10 projections using statdunk's **own stated
  method** (`attempt-weighted-nine-category-zscore-v1`), and **validate** it: reconstructing the
  8/11 artifact's published z-scores from its own projections reproduces them **exactly (Spearman =
  Pearson = 1.0000 over 250 players)**. The method is statdunk's engine; applying it to the fresh
  projections yields statdunk's board as its own code would compute it today. `build_market.py`
  asserts this ρ ≥ 0.999 on every run or refuses to build. Provenance says all of this plainly.

Both `totals` (season, games-inclusive) and `averages` (per-game) value/rank are emitted; the
comparison uses `totals` as the structural analog of our availability-adjusted board (§4 note).

## 3. Join and the hard unmatched-name gate (§3.3)

Joined to the committed 220-row pool. **Our board is `rank_engine.py` over
`projections-2026-27.csv`, reproduced with 0 rank mismatches against the committed
`top-200-2026-27.md`** — the real board, not a re-derivation. Name matching folds accents,
punctuation and generational suffixes (an equivalent of the deck plane's `hoops.norm()`, which lives
out-of-repo).

- **Zero normalized-name collisions** in any of the three sets — no two distinct players fold to one
  key, so the 18-shared-surname hazard (Johnson ×4, Williams/Thompson/Murray/George ×3) produces **no
  false matches**. The join is provably 1:1.
- **4 spelling aliases**, each verified to resolve to exactly one source player: Herb/Herbert Jones,
  Cam/Cameron Johnson, Nic/Nicolas Claxton, Alex/Alexandre Sarr.
- **Coverage:** Hashtag matches **212/220** (8 absent); Statdunk matches **187/220** (33 absent).
  **Every absence is deep-tail or an unsigned FA** — both sources cover our entire top ~108
  (statdunk's shallowest gap is Dereck Lively #109). All 41 are enumerated with team + reason in
  `unmatched-2026-08-24.md`; the gate refuses to proceed on any *undocumented* miss.
- **One absence worth a flag:** **Donte DiVincenzo (MIN, our #159)** is genuinely missing from
  Hashtag's full 429-row set — not a spelling variant (surname absent from the raw). A rotation guard
  absent from a consensus source is a data-quality note, not our error.

## 4. Disagreement & arbitrage highlights (owner adjudicates — nothing blended)

Full tables in `report/market/disagreements-2026-08-24.md`. The board stays built from first
principles; these are a sanity/arbitrage reference only (owner decision 2026-08-21).

- **Pass-E arbitrage vs Yahoo ADP (§5.3) — the designed prize.** Top **values** (we rank ≥15 picks
  ahead of the room): Reed Sheppard (+68, STL/3PM), Jimmy Butler (+64, FT%/STL), Tari Eason (+62,
  STL/TOV), **Dyson Daniels (+51, STL — exactly the archetype the board header calls out)**, Anthony
  Edwards (+25), Donovan Mitchell (+24). Top **fades** (room ≥15 ahead of us): Keyonte George (−120),
  Jaylen Brown (−93, TOV/FT%), LeBron James (−92, age/availability), Paolo Banchero (−85, FT%/TOV),
  Donovan Clingan (−74, one-cat). Each carries our board's own z-lean as the "why."
- **Ordering vs Statdunk (§3.4).** Biggest genuine value gaps where we rank higher: Herb Jones (+130,
  we pay his steals), Bogdan Bogdanović (+131), Walker Kessler (+86), Domantas Sabonis (+59). Where
  Statdunk ranks higher: Neemias Queta (−140), Ryan Rollins (−124), Donovan Clingan (−90). **Read the
  totals-Δ with care** for injury-discounted stars — Statdunk `totals` docks missed games harder than
  our streaming-credit `z_adj`, so e.g. Embiid's sd_tot#≈117 vs our #22 is almost entirely the
  availability model (his sd_avg#≈23 ≈ our #22). The per-game column isolates real disagreement; the
  report says so inline.
- **Lines vs Hashtag (§3.4).** The largest divergences are deep rookies and our higher GP projections
  (Bogdanović +22 GP, Gary Trent Jr +28 GP); among draftables, Jordan Poole (+6.3 pts), Nikola
  Vučević (+5.5 pts/+3.2 reb), LaMelo Ball (+5.7 pts) stand out. All for owner adjudication.

## 5. What was deliberately NOT done (scope)

- **`marketRanks` untouched.** Step 5 is explicitly gated ("ONLY THEN") behind owner adjudication of
  the tables above, and it is a cross-language change (`docs/draft-deck.html` JS + `arena.market_ranks`
  + `check_parity.py` fixtures) that lives in the **deck repo** (`yahoo-fantasy-basketball`), which is
  not in this session's scope. Not started.
- **No projections, team labels, board, or engine edits.** `git status` shows only new files under
  `report/market/` plus this report. `check_provenance.py` passes; the board is byte-for-byte the
  committed one.
- **Deck plane untouched**, so no republish, so the §0 orphan check does not apply.

## 6. Carried open items

New, from this session:
- **Allowlist statdunk's Supabase host** (`uajisozzfvtqfselbfri.supabase.co`) to pull statdunk's
  *published* category board directly instead of reconstructing it (§0, §2). Reconstruction is
  validated-exact, so this is an improvement, not a blocker.
- **`marketRanks` decision is now teed up.** The tables the design always wanted exist. Whether to
  replace the circular `Mkt` proxy (0.88–0.90 self-correlated by construction, per the work order §2)
  with real consensus is the owner's call; the disagreement table is the input to it. That change,
  when taken, is a deck-repo cross-language edit driven red first (work order §3 step 5).
- **Donte DiVincenzo** absent from Hashtag's 429-row set (§3) — recheck next market pull.
- **Statdunk's 250-cap** leaves 33 of our deep-tail/FA rows uncovered; fine for the top-108 arbitrage,
  a limitation for full-pool work — the Supabase route would also widen coverage.

Still open from the 8/21 after-report (unchanged — no news swept this session, by design):
- **Cam Whitmore** — waive-and-stretch + unverified DVT clearance; delete if waived and unsigned by October.
- **Mark Williams** — fifth-pull-quiet 58-GP discount; October must-do.
- **Alex Sarr** — cross-plane severity mismatch (deck `inj-foot-risk` ×0.78 vs kit 72 GP).
- **D1** — does a gate-verified deck projection count as a sourced base rate for the kit (Peyton Watson gap)?

## 7. Verification (adversarial-verify)

**Criteria.** C1 §0 channel verified before work, not assumed: **PASS**. C2 both sources landed raw +
dated: **PASS**. C3 normalized to §4, additions documented, nothing silently dropped: **PASS**. C4
hard unmatched gate — every pool player matched or documented, no silent partial join: **PASS** (0
unexplained). C5 disagreement + Pass-E tables produced for adjudication: **PASS**. C6 no
projections/board/`marketRanks` edits; `check_provenance` exit 0; board byte-identical: **PASS**. C7
pushed to the designated branch with a draft PR: see final state.

**Refutation — attacks that found something.**
- **Auditing statdunk's base endpoint** caught that the reachable pre-computed board is a stale,
  star-less "provisional" build — using it as-is would have shipped Bez Mbeng #41 as market truth.
  Forced the fresh-projections + validated-reconstruction path.
- **Spot-checking the first hashtag postback** caught the category-checkbox `on` bug — the initial
  full-list pull had silently returned 8 columns with TOTAL=0.
- **Collision-checking every normalized name** proved the shared-surname hazard produces no false
  matches (0 collisions), rather than assuming full-name matching was safe.
- **Verifying blank ADPs against the raw** confirmed they are genuinely undrafted, not dropped numbers.

**Attacks that found nothing.** Board reproduction (0/200 rank mismatches vs the committed md).
Reconstruction faithfulness (ρ=1.0000 vs statdunk's own published block). Alias uniqueness (each →
exactly 1 source row). `git status` (only `report/market/` touched). Provenance gate (exit 0).

**Status — delivered for adjudication.** Weakest parts, in order: statdunk's category value is
*reconstructed* not pulled (validated-exact, but the direct Supabase route is better and now flagged);
statdunk's 250-cap under-covers our deep tail; and the ADP arbitrage rests on Yahoo consensus that is
blank for 56% of rows (all undrafted, so out of the arbitrage by definition).
