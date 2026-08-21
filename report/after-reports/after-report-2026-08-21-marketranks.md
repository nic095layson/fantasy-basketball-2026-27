# Work-order execution — marketRanks → real ADP (2026-08-21, step 5)

**Run date:** 2026-08-21 (later same day, third session) · **Scope:** execute
`report/market-data-workorder.md` **step 5** — replace the deck's circular
`marketRanks` proxy with real ADP. Cross-language change in the deck repo
(`yahoo-fantasy-basketball`), driven red-first. Not a data pull.

```
📋 What changed
✓ Deck marketRanks (JS) + arena.market_ranks (py) now lead with real Hashtag
  ADP; z-derived proxy is the fallback for the 73 pool players the feed misses
✓ check_parity.py EXTENDED to cover marketRanks — it never did; the mirror was
  unverified. Proven red-first (224 disagreements when only JS changed), then GREEN
✓ ADP shipped as data/market_adp.json (172 players) + a committed generator;
  the feeds are now bundled in the deck repo (data/market/)
✗ Live artifact deliberately NOT republished — engine change under review; the
  live board keeps the reviewed 943d675 build until this PR is approved
```

**Gates at final state:** `check_parity.py` **EXACT MATCH** (now including 239
market ranks), `test_gates.py` **10/10**, `build_deck.py` green with round-trip OK.

---

## 0. Why this session could do it

The work order was opened blocked-on-session-start; the two prior sessions
executed steps 1–4. This is step 5. The owner's 2026-08-21 network change is
confirmed still in effect (`statdunk`, `hashtagbasketball`, `basketball-reference`
all 200 via the §0 curl check; ESPN API and nba.com root still 403).

## 1. The finding that changed the plan

The work order states `marketRanks` is "locked by check_parity.py". **It was
not.** `check_parity`'s driver compares the pool fields, name-matching, `dfHash`,
and `decwScores` orderings — none of which invoke `marketRanks`, and it wasn't in
the exported `api`. A JS↔Python divergence in the market model would have shipped
silently. So step 5 grew a step 0: **extend the parity harness to cover
`marketRanks`**, which then served as the red-first net for the change itself.

This is the whole reason for plan-gate: the doc's stated mechanism was wrong, and
finding that before coding changed what got built.

## 2. What was built

**The model.** `marketRanks(pool)` / `market_ranks(pool)` now:
1. compute the **same** z-derived proxy as before (mscore + rookie/risk
   sign-multipliers + `MKT_PIN`) — unchanged, byte-for-byte in logic;
2. **lead** the ranking with players that have a real ADP, ordered by ADP;
3. append the proxy order for players the feed doesn't cover.

Real ADP overrides `MKT_PIN` (a measured room price beats a hand-entered rookie
pin); pins still apply within the no-ADP tail. Ties broken by proxy rank so the
two languages order identically. **Empty ADP reproduces the old proxy verbatim** —
the change is inert until data is present, which made the wiring step safe.

**The data.** `data/market_adp.json` — 172 deck-pool players keyed to their deck
names, from Hashtag consensus ADP, built by `scripts/build_market_adp.py` from
`data/market/hashtag-2026-08-21.csv` (feeds now bundled in the deck repo with
provenance). Name matching reuses the accent/alias normalizer the kit join
settled on. `build_deck.py` injects it as `const ADP` (new anchor, round-trip
verified); `arena.py` loads it module-level (read-only — honors the isolation
contract).

**Files:** `docs/draft-deck.html` (marketRanks + ADP const), `arena/arena.py`
(loader + market_ranks), `scripts/build_deck.py` (inject + round-trip),
`scripts/check_parity.py` (marketRanks coverage), `scripts/build_market_adp.py`
(new), `data/market_adp.json` (new), `data/market/*` (new),
`data/freshness.json` + `data/roster_verification.json` (re-stamped no-pool-change).

## 3. Red-first, as the work order requires

1. Extended `check_parity` to compare `marketRanks` across the 6 states' pools →
   **GREEN** (proved the new comparison runs; both sides still proxy).
2. Wired ADP data in, unused → **GREEN** (data present, model unchanged).
3. Rewrote **JS** `marketRanks` to ADP-primary, left `arena` on the proxy →
   **RED, 224 disagreements** (`AJ Dybantsa deck172/py32`, `Cam Thomas
   deck173/py70`, …). This is the proof the harness now catches the change.
4. Mirrored the rewrite into `arena.market_ranks` → **GREEN** (239 ranks EXACT).

## 4. Impact (the owner-adjudication artifact)

**Circularity fell as intended.** Spearman ρ of the market rank against our own
punt-aware value board:

| | ρ vs our val board |
|---|---|
| old proxy | **0.886** (≈ the 0.88 the work order measured) |
| real ADP | **0.777** |

The market signal is now genuinely exogenous rather than a re-skin of our board.
Match rate: **172 / 245** pool rows get real ADP; 73 (deep bench, some rookies)
fall back to the proxy.

**Biggest `MKT_RANK` moves, proxy → real ADP** (the room's price we couldn't see):

| player | proxy | ADP | note |
|---|---:|---:|---|
| LeBron James | 66 | 10 | room pays name-value; we priced him on the 9-cat line |
| Jalen Duren | 113 | 52 | room pays up |
| Nikola Vučević | 111 | 42 | " |
| Jarrett Allen | 110 | 53 | " |
| Rudy Gobert | 127 | 70 | " |
| Cameron Johnson | 64 | 153 | we over-priced his draft cost |
| Fred VanVleet | 80 | 142 | " |
| Dejounte Murray | 55 | 117 | " |
| Quentin Grimes | 84 | 146 | " |

**Live-draft effect, on the owner's own `draft_state_44`.** The upload is a
complete 12×13 draft, so there are no live picks left — but truncated to the
owner's round-4 turn (pick #42) it replays a real board. **17 of 198** available
players change their survival ("will he last?") call, all in the right direction:
Vučević, Stephon Castle and Myles Turner stop being promised as "quiet" (the room
takes them earlier than our value board assumed); Cam Thomas (unsigned FA,
ADP #131) and Zach LaVine correctly read as lasting. The flip count is small **by
design** — `survivalP` weights market only 2/11 (the room drafts 9/11 by value,
per the 2026-08-03 recalibration). The **mkt-lens Best-available board and the
card price badges**, which read `MKT_RANK` directly, change much more.

## 5. What was deliberately NOT done

- **`survivalP`'s 9/11–2/11 blend weights were not re-fit.** They were calibrated
  against the old proxy on 840 observations; re-fitting needs a paired-mock study
  and is out of scope. The change makes the 2/11 market term *more honest*, not
  differently weighted — but the weights now sit against a different signal, and
  a future calibration pass should confirm them. **Flagged, not silently shipped.**
- **The live artifact was not republished.** This is an engine change to live
  draft advice, under review — not a data pull. The live board keeps the reviewed
  build until the PR is approved; the pool on it is already current.
- **`draft_state_44` was not added as a committed parity fixture.** Adding a state
  to the locked set could surface an unrelated `decwScores` regression and couple
  it to this PR. Used for validation only; offered as a clean follow-up.
- **arena's own tournament seats now see real ADP** for their market persona
  (same module-level map). A minor anachronism against arena's frozen 2025-10-21
  dataset; most frozen names still match. If the owner wants arena kept
  pure-proxy, one guard (`ADP={}` in arena's internal callers) does it — flagged.

## 6. Verification (adversarial-verify)

**Criteria** — C1 parity covers marketRanks, fails one-sided: **PASS** (224-diff
red proven). C2 ADP-primary + proxy fallback, JS==py: **PASS** (239 EXACT). C3
ADP committed with generator + provenance, build round-trips: **PASS**. C4 full
parity EXACT + gates 10/10: **PASS**. C5 impact quantified (ρ 0.886→0.777 + flip
list): **PASS**. C6 both repos pushed, PRs updated, live artifact not republished,
after-report written: **PASS**.

**Refutation — attacks that found something.**
- Reading the parity harness instead of trusting the work order found that
  `marketRanks` was **uncovered** — the change would otherwise have had no net.
- The empty-ADP-equals-old-proxy property was verified, which is what let the
  data-wiring step land GREEN before the behavior change (clean red-first).
- Running the change against the owner's real draft (not a synthetic pool)
  confirmed the survival flips are directional and sensible, not noise.

**Attacks that found nothing.** Cross-language equivalence (239 ranks EXACT across
6 states). Build round-trip incl. the new ADP anchor. Gate suite 10/10. arena
market persona smoke test. df_hash still bit-identical.

**Status** — delivered to a draft PR. Weakest parts, in order: the un-refit
survival weights (§5), ADP from one platform only (Pass E wants two), and the
73-player proxy tail where the board still can't see the room.
