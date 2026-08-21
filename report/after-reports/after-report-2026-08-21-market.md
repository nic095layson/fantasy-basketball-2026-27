# Draft Kit Data Pull — After Report (later 2026-08-21)

**Run date:** 2026-08-21 · **Window swept:** 2026-08-21 (later same day) → 2026-08-21
**Scope:** delta pull under DATA-PULL.md **plus** execution of
`report/market-data-workorder.md`, which was opened earlier today and blocked on
session start. Not the October full re-verification.

```
📋 Freshness Check — 2026-08-21 (later)
✓ Verified: 1 signing (DeRozan→DEN, 2 outlets), channel re-tested by raw curl,
  4 carried pool gaps closed from Basketball-Reference lines fetched this run,
  2 market feeds fetched and normalized, join gate clean
⚠ Changes since this morning's pull: 1 row edited + 4 rows added (kit),
  1 row edited (deck); 0 removed on either plane
✗ Cannot verify: D'Angelo Russell's 2026-27 team (contested across sources —
  held OUT of the pool) · Kuminga and Cam Thomas rest on absence-of-signing,
  freshest dated items predate the window
```

**Gate:** `check_provenance.py` → **PASS** (exit 0) — all 224 rows sourced;
verified 2026-07-13 .. 2026-08-21. `--max-age-days 14` still fails, structural
and expected: a delta pull does not re-verify rows without news.

---

## 0. Baseline correction — read this first

**This session started from the wrong baseline and corrected it mid-run.** That
correction is the most important thing in this report, because a naive version
of this pull would have silently reverted a teammate's work.

`origin/main` is still at **2026-08-18**. The pull-log on `main` therefore dated
my window as 8/18 → 8/21. That was wrong: two further pulls (**8/20** and
**8/21**) already exist on `claude/fantasy-basketball-data-pull-687jyp`, with
open PRs (kit #7, deck #12) that have not been merged.

I did not discover this from git. I discovered it from the **published
artifact**: the live deck already read `built: 2026-08-21` while the repo's last
commit was 8/18. Checking the published page before overwriting it is the
pre-republish orphan check (LESSONS.md lesson 21), and it paid for itself again
here — it turned an invisible divergence into a visible one **before** I
published over someone else's build.

I rebased both repos onto that branch and re-applied only my net-new work.
Concretely, the earlier pull was **ahead of my first attempt** on two points and
I discarded mine in favour of theirs:

- **Cam Whitmore** — they cut GP 68 → 30 on an in-window report that Cleveland is
  weighing a waive-and-stretch and that he is not expected to play a game there.
  I had repriced him as a Cleveland bench wing, which was wrong. Theirs stands.
- **Max Strus** — I had trimmed his line for a crowded Clippers wing room. They
  left it alone. **Theirs is more correct**: DATA-PULL §3 says stats stay unless
  there is a *sourced* role mechanism, and I had a plausible inference, not a
  source. My trim is gone.

## 1. Channel change — the blocker lifted, and it was verified, not assumed

The work order's §0 says to verify the channel by raw `curl` and not to report it
fixed without running the check. Run this session:

| domain | status |
|---|---|
| `statdunk.com` | **200** (newly reachable) |
| `hashtagbasketball.com` | **200** (newly reachable) |
| `www.basketball-reference.com` | **200** (newly reachable) |
| `site.api.espn.com` | 403 (unchanged) |
| `www.nba.com` | 403 at root; player pages fetch |
| `basketball.realgm.com`, `www.hoopsrumors.com` | unreachable (unchanged) |

The owner's 2026-08-21 network reconfiguration reached this session, exactly as
the work order predicted ("a fresh session picks it up"). Two consequences, and
the second one matters more than the market data:

1. The market-data work order is unblocked and executed (§4).
2. **Basketball-Reference is open**, which is the requirement DATA-PULL §3 puts
   on adding a player to the pool. The four-pull pool gap is closed on the
   protocol's own terms (§3) — no workaround, and open decision **D1 is now
   moot** rather than answered: nothing needs to count deck-plane projections as
   a base rate, because the real base rates are fetchable again.

`verify_rosters.py` stays **fallback-partial** — ESPN's API is still 403.

## 2. NBA roster changes

| Player | Change | Date | Sources |
|---|---|---|---|
| **DeMar DeRozan** | FA → **DEN**, 1yr/$3.9M | reported 8/21 | [ESPN](https://www.espn.com/nba/story/_/id/49684447/nuggets-signing-6-all-star-demar-derozan-1-year-deal), [HoopsHype](https://www.hoopshype.com/story/sports/nba/rumors/2026/08/21/demar-derozan-signs-with-denver/91410912007/), [Yahoo](https://sports.yahoo.com/nba/article/demar-derozan-reportedly-signing-with-the-nuggets-on-1-year-39-million-deal-204045448.html) |

This broke **after** the morning pull ran, which is why that pull correctly
recorded him as FA. He chose Denver over Miami, Washington and New Orleans for a
stated significant role next to Jokić and Murray — on wing minutes the Peyton
Watson trade had opened two days earlier.

Everything else in the 8/19–8/21 window (the five-team CLE/DEN/LAC/WAS/CHA
trade, the Harden signing) was already landed by the 8/20 and 8/21 pulls and is
**not** re-applied here. I re-verified each independently and found no
disagreement.

**Corrections to earlier cards, stated plainly.** The 8/18 card said Denver was
"effectively out" on DeRozan after signing Lonnie Walker IV; the 8/21 card had
him gaining Washington interest. Both were wrong. The reporting moved, and the
deck's judgment card now says so rather than quietly overwriting it.

## 3. Projection changes (labeled per Operating Principle 3)

**DeMar DeRozan** — [ESTIMATED], both planes. Kit: 20.5 pts on 15.5 fga in 32
mpg → **15.5 pts on 12.0 fga in 28 mpg** (3.5 reb, 3.5 ast, 0.8 3pm, 4.0 fta,
1.6 tov). Deck: 21.5/16.5 fga → **16.0/12.5 fga**. **Mechanism (>20% fga
swing):** he was priced as an unsigned free agent assuming a starter's role.
$3.9M is minimum-scale money, he turns 37 this season, and third-option usage
next to Jokić and Murray is not the usage he carried in Sacramento. Direction
**[LIKELY]**; magnitude **[SPECULATIVE]** — "significant role" is the reporting's
word, and a healthy Denver bench could support more than this.

**Four pool additions** — all [ESTIMATED], base rates from Basketball-Reference
2025-26 per-game lines **fetched this run**, scaled for role and age, each
cross-checked against both market feeds:

| Player | Tm | line | mechanism |
|---|---|---|---|
| **Peyton Watson** | CLE | 62 GP, 13.8/4.9/2.1, 0.9 stl, 1.2 blk | B-Ref base 14.6 pts on 10.8 fga in 29.6 mpg (54 GP, 40 starts). Trimmed slightly: Cleveland's hierarchy (Mitchell, Harden, Mobley, Allen) absorbs usage Denver did not. GP 62 sits between his 54 played and the feeds' 62–70. |
| **Cedric Coward** | MEM | 68 GP, 15.0/6.2/2.9 | B-Ref rookie base 13.6/5.9/2.8 in 62 games, scaled up modestly for a year-two role on a rebuilding Memphis team. |
| **Deandre Ayton** | WAS | 66 GP, 11.5/7.6/0.9 | B-Ref base 12.5/8.0 in 27.2 mpg across 72 starts. Minutes trimmed for a three-big Washington frontcourt (Davis, Sarr) and FG% regressed off a .671 outlier. |
| **Al Horford** | GSW | 52 GP, 7.8/4.7/2.4, 1.5 3pm | B-Ref base 8.3/4.9/2.6 in 45 games. Age-40 season on a 2yr/$14M re-sign behind Green and Porziņģis; GP cut to 52. |

**D'Angelo Russell stays OUT, deliberately.** He was the fifth carried name. His
2026-27 team is contested across sources this run — one report has him traded to
Memphis in a six-team deal, another places him in Washington, and Memphis buyout
rumors are live; B-Ref shows him on Dallas for 26 games in 2025-26. A contested
team label is precisely what this board refuses to ship, so he is not added. This
is the fourth pull carrying him and the first with a *stated* reason rather than
a blocker.

## 4. Market data — Pass E executed (the work order)

New: `report/market/` (raw + normalized + provenance), `report/market_join.py`,
`report/market-2026-27.md`.

**Owner decision honored, not re-litigated.** Work order §1.2 is that these feeds
are a **sanity check and arbitrage input, not a blend**. `market_join.py` never
writes `projections-2026-27.csv`, and its docstring says so. The board is still
built from first principles and its header still truthfully claims that.

**Both feeds needed real work to retrieve, and the method is recorded** in
`report/market/provenance.csv` so the next session does not rediscover it:

- **Hashtag** 403s without a browser UA, and its default view is the top 30. The
  full table needs an ASP.NET postback carrying `__VIEWSTATE`, each `<select>`'s
  *selected* value, **and the nine checked category checkboxes**. Omitting the
  checkboxes returns HTTP 200 with the stat columns silently dropped and
  `TOTAL` = 0.00 — a failure that looks like success. `DDSHOW=900` ("All") also
  drops them; 200 is the usable ceiling.
- **statdunk** is a React SPA whose HTML carries no data. Its JS bundle exposes a
  public JSON API. The release is stamped `asOf 2026-08-21T02:40Z`, model
  `statmaxers-nba-preseason-lock-in-v4.7`, 20 000 Monte Carlo draws, 250 players.

**The two feeds' native ranks are not comparable** — Hashtag ranks on a 9-cat
z-sum, statdunk on **points-league** fantasy points. Comparing them directly
would have been a category error. `market_join.py` re-ranks both through this
repo's own engine first, so only the projected stat lines differ.

**Join gate (work order §3.3: a silent partial join is a defect).** It fired
three times and each time it caught a real defect:

1. 14 Hashtag names arrived as `"Trey Murphy III T.Murphy III"`. My first
   normalizer stripped only the simple `N.Lastname` form and silently failed on
   suffixed names, producing 14 bogus "unmatched" rows.
2. A surname+team near-miss detector then surfaced five genuine alias misses —
   Cameron/Cam Johnson, Alexandre/Alex Sarr, Herbert/Herb Jones,
   Nicolas/Nic Claxton, and `P.J.`/`PJ` Washington. Each was verified on
   surname **and** team before being aliased; none is auto-joined, because a
   wrong merge is worse than a missing row.
3. After the fixes: **0 near-misses, 0 ambiguous names**, ADP coverage up from
   150 → **166** pool rows.

**Output** (`report/market-2026-27.md`): the Pass E ADP table, **58 values** (our
rank 15+ picks ahead of ADP) and **52 fades**, per-game line disagreements
against each feed, and 23 remaining pool-completeness candidates. The largest
single gap is **Ty Jerome (MEM)**, ranked #41 by statdunk and absent from the
pool — the strongest October addition candidate.

**The one team-label conflict is worth the owner's attention:** Hashtag prices
the frozen Kawhi trade as **done** (Kawhi on TOR, Brandon Ingram on LAC) while
statdunk agrees with this board that Kawhi is still a Clipper. The market is
split on whether to price a transaction the league has frozen, so his ADP will be
unusually noisy. The deck's −0.20 judgment adj is **held** for a fourth pull and
its card now records the split.

## 5. Board movement (computed — engines re-run, diffed by script)

**Kit board.** Regenerated; **byte-identical on a second run** (determinism).

- **Entered top-200:** Cedric Coward **131**, Peyton Watson **133**, Deandre
  Ayton **160**, Al Horford **174**.
- **Exited:** Jaime Jaquez Jr (197), Ron Holland (198), AJ Green (199), Jonathan
  Kuminga (200) — all displaced off the bottom.
- **Moves ≥3:** DeMar DeRozan **103 → 172 (+69)**, the reprice. 35 others, all
  in the 140–200 band.

**Those 35 are not a valuation change and I checked rather than assuming.**
Subtracting mechanical displacement (insertions ranked above a player, minus
exits), the maximum *genuine* reordering among unedited players is **4 ranks**,
concentrated entirely in centers (Mark Williams, Poeltl, Zubac, Hartenstein,
Clingan). Cause: inserting two centers into the iterated top-180 valuation pool
shifts the pool's REB/BLK moments. Underlying value changes are **0.02–0.03
z-units** — the mid-board is simply packed tightly enough that 0.03 moves a
player four spots. Nothing above rank 40 moved more than 2.

**Deck board.** DeRozan **107 → 152 (+45)**. Entries 0, exits 0, and **no
unedited player moved ≥3 ranks** — the check that a reprice had no pool-wide
side effects.

## 6. Deck plane (§7)

Applied: the DeRozan row + reprice, `rosters_official.json` re-authored to
2026-08-21 with dated evidence and the channel status, and the DeRozan judgment
card rewritten to record that two earlier cards had his market wrong.

Gates: `verify_rosters.py` **245/245, zero mismatches**, dated 2026-08-21
(fallback-partial — ESPN 403, reported not swallowed). `build_deck.py` green,
injection round-trip OK. `check_parity.py` **EXACT MATCH**. `test_gates.py`
**10/10**.

**Republished to the existing artifact URL** and verified by re-fetching the live
page: pool hash `cebffc969c94c237…` **identical** to the local build, `built:
2026-08-21`, DeRozan rendering as `DEN`, new judgment card present. No orphan.

## 7. Watchlist / open items

- **D'Angelo Russell** — contested team (§3). Resolve from a primary source
  before he is ever added.
- **Ty Jerome (MEM)** — statdunk #41, absent from the pool. Now that B-Ref is
  open, the blocker is gone; this is an October must-add along with the other 22
  candidates in `market-2026-27.md`.
- **Mark Williams** — the discount has now stood unexamined since 7/27 across
  **six** pulls. B-Ref is open, so the honest fix is available: re-derive the
  58-GP discount from the 2025-26 game log instead of carrying it on inertia.
- **Cam Whitmore** — carried from the morning pull: if waived and unsigned by
  October, delete the row rather than discount it again.
- **Kawhi Leonard** — held at −0.20 for a fourth pull; mid-September Board of
  Governors meeting is the checkpoint. New: the feeds disagree about him (§4).
- **Kuminga / Cam Thomas** — no signing reported, but the freshest dated items
  predate the window; both labels rest on absence. Cleveland is now out on both
  (hard cap, after Harden and Watson).
- **`marketRanks` is circular** — the work order's §2 finding stands and is
  untouched by design: the deck's `Mkt` column is computed from our own z-scores
  (ρ ≈ 0.88–0.90) plus seven hand-typed rookie pins. Real ADP now exists in
  `report/market/`, so the substitution is finally possible. **Deliberately not
  attempted here** — work order §3 sequences data before integration, and any
  change is a cross-language edit to JS + `arena.market_ranks` +
  `check_parity.py` fixtures, driven red first. That is the next session's job.
- **Two open PRs are still unmerged** (kit #7, deck #12) and `main` is four pulls
  stale on both repos. This pull stacks on that branch rather than on `main`.

## 8. Assumptions & deviations

- **A1 — Pushed to `claude/pull-rankings-3tc18h`, based on
  `claude/fantasy-basketball-data-pull-687jyp`, not on `main`.** DATA-PULL §0
  defines done as pushed to `main`; the standing branch instruction wins, and
  basing on `main` would have silently reverted the 8/20 and 8/21 pulls. Done
  pending PR merge.
- **A2 — I discarded my own Whitmore and Strus edits** in favour of the earlier
  pull's (§0). Deliberate: theirs was better sourced.
- **A3 — The four added lines are my scaling of B-Ref base rates**, not
  computations. Directions are defensible; magnitudes are arguable and labeled.
- **A4 — Peyton Watson's line is the most speculative of the four.** He has a
  new team, a new contract and no beat-reported Cleveland role yet; the two feeds
  disagree with each other about him by 2.7 ppg.
- **A5 — ADP is from one platform, not two.** PROMPT.md Pass E asks for "at
  least two platforms (prefer the client's platform from INPUTS.md, plus one
  aggregator)". INPUTS.md's ⭐ fields are still blank, so the client's platform
  is unknown and only the aggregator half is satisfied. Flagged, not worked
  around.

## 9. Verification report (adversarial-verify)

**Criteria** — C1 every change carries a dated source from this run, 2+ outlets
for tier-movers: **PASS** (DeRozan on three). · C2 CSV team edits paired with
provenance, gate exits 0: **PASS** (224/224). · C3 board movement computed by
script: **PASS** on both planes, including the displacement-vs-genuine
decomposition. · C4 estimates labeled with mechanisms: **PASS** (§3). · C5 deck
gates green: **PASS** (245/245, parity EXACT, 10/10). · C6 republished to the
existing URL, verified live: **PASS** (hash-identical). · C7 both repos pushed
with PRs: **PASS** (on designated branches — A1).

**Refutation — attacks that found something.**

- Reading the **published artifact before overwriting it** found the entire
  parallel-branch divergence. Without it this pull would have reverted two days
  of a teammate's work while reporting success.
- Re-running the **baseline board diff after noticing zero movement** caught that
  `HOOPS_DATA`, not `DATA_PATH`, is the deck engine's env override — my first
  "no movement" result was two identical runs of the *same* pool.
- **Decomposing board moves into displacement vs. genuine reordering** turned an
  alarming "35 unedited players moved" into a bounded, explained 4-rank ceiling.
- The **join gate** caught 14 malformed names and 5 alias misses that would
  otherwise have silently dropped 19 players from the market comparison.
- **Re-testing the channel by raw curl** rather than trusting four prior reports
  of "blocked" is what revealed B-Ref had opened — which is what actually closed
  the pool gap.
- Checking **D'Angelo Russell's team** instead of taking the deck's placement
  found a live three-way conflict and stopped a bad row from shipping.
- Verifying the **live page after publishing** confirmed hash equality rather
  than assuming the publish took.

**Attacks that found nothing.** Kit-board determinism (byte-identical on re-run).
Deck injection round-trip. JS↔Python parity (EXACT). Ambiguous-name collision
check across all three sources. Deck board side-effects (zero unedited movement).
Gate suite 10/10.

**Regressions.** None. Both repos' gates are green at final state, and the two
edits I dropped (§0) were dropped in favour of better-sourced existing work, not
lost.

**Status** — delivered. Weakest parts, in order: Peyton Watson's new-team line
(A4), ADP from a single platform (A5), the four added rows being my scaling
rather than a model, and Mark Williams' six-pull-stale discount, which is now
fixable and was not fixed.
