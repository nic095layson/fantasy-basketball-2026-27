# Draft Kit Data Pull — After Report

**Run date:** 2026-08-21 · **Window swept:** 2026-08-20 → 2026-08-21 (1 day)
**Scope:** delta pull under DATA-PULL.md, both planes, ending in a deck republish. Not the October full re-verification.

```
📋 Freshness Check — 2026-08-21
✓ Verified: 1 signing (James Harden), 1 in-window roster-status report (Cam
  Whitmore waive-and-stretch), 4 FA statuses re-verified, Kawhi re-checked,
  3 out-of-window injury stories dated and dismissed — every claim carries a
  dated source from this run
⚠ Changes since 8/20: 2 rows edited in the draft-kit CSV, 1 row edited in the
  deck pool; 0 added, 0 removed on either plane
✗ Cannot verify: Cam Whitmore's medical clearance, second consecutive pull ·
  Jaden Ivey's FA status by dated news, fourth pull · Mark Williams' foot,
  FIFTH consecutive quiet pull · all claims rest on search results (see §0)
```

**Gate:** `check_provenance.py` → **PASS** (exit 0) — all rows sourced; verified 2026-07-13 .. 2026-08-21.
`--max-age-days 14` still **FAILS**, structural and expected, same as the last three pulls. The October full run clears it.

---

## 0. Window and method limits

**The window was 1 day** — the design case DATA-PULL.md was written for, and the pull ran fast.

**Research channel unchanged and re-tested.** Raw `curl` through the proxy to `basketball-reference.com`, `nba.com` and `site.api.espn.com` all returned no route; `verify_rosters.py`'s direct ESPN pull 403'd. Web search works. Fourth consecutive pull on search-derived evidence. The network-policy fix remains the highest-value change available to this system.

**The two planes were in sync at the start.** The live deck served `built: 2026-08-20`, pool hash `66dd70359323…`, byte-identical to git `HEAD`. Checked before overwriting (lesson 21). No orphan.

## 1. NBA roster changes

**One transaction: James Harden re-signs with Cleveland.**

| Player | Change | Date | Sources |
|---|---|---|---|
| **James Harden** | FA → **CLE**, 3yr/$97M with a 2028-29 player option and a trade kicker | agreed 8/20 | [ESPN](https://www.espn.com/nba/story/_/id/49671792/james-harden-agrees-3-year-97m-deal-remain-cavaliers), [Washington Post/AP](https://www.washingtonpost.com/sports/nba/2026/08/20/cavaliers-harden/ed3b8e6c-9cc4-11f1-9cc4-2dc9b46e2d5c_story.html), [Yahoo Sports](https://sports.yahoo.com/articles/james-hardens-contract-cavaliers-fully-184759346.html), [Eurohoops](https://www.eurohoops.net/en/nba-news/2000353/james-harden-agrees-to-three-year-97-million-deal-with-cavaliers/), [Blazer's Edge](https://www.blazersedge.com/nba-news-rumors/115280/james-harden-signs-contract-cleveland-cavaliers-2026-nba-free-agency-news-peyton-watson-nuggets) |

**This closes the highest-alert item carried from yesterday, in one day.** The 8/20 report recorded that his stated precondition was Cleveland landing a wing, that the Watson trade satisfied it on 8/19, and that the signing was reported imminent. He agreed the next day. The report also flagged it as "the first thing to check" next pull — it was, and it was the right call.

**One correction to the record.** The 8/20 reporting this system relayed said "at most two guaranteed years." **That was wrong — the deal is three years.** Recorded here and on the board rather than quietly dropped, because the board printed it.

Applied on **both** planes with provenance/evidence travelling in the same change. Harden was the only FA row shared across the two pools that moved, taking the kit's FA block from five rows to **four**.

**Checked, dated, and correctly NOT edited:** Alex Sarr's fractured right foot — surgery was **2026-06-16** ([Shams/ESPN](https://www.espn.com/nba/story/_/id/49073891/sources-wizards-alex-sarr-surgery-fracturing-foot), [NBA.com](https://www.nba.com/news/wizards-alex-sarr-broke-right-foot-in-offseason-workout-but-is-expected-to-recover-before-next-season)), two months outside the window, and already encoded on his deck row as `inj-foot-risk (June surgery, expected ready)`. The search surfaced it as though it were fresh. Brandon Ingram's heel and Josh Giddey's ankle are May 2026, dismissed for the third consecutive pull. Nikola Topić's lumbar microdiscectomy is not a pool row on either plane.

## 2. Projection changes (labeled per Operating Principle 3)

**James Harden — team label only, projection HELD, both planes.** No named mechanism exists to move it. His line was already priced as a Cavalier (the 8/18 judgment card said so explicitly), and the two candidate mechanisms point in opposite directions: Cleveland's guard room lost **both** Schröder (CHA, 8/15) and Tre Mann (WAS, 8/19), which raises his ball-handling load, while he **turns 37 on 8/26**, which argues for load management on a title team. Those offset. Holding is the honest answer, not the lazy one.

**Cam Whitmore — [ESTIMATED], kit plane, GP cut 68 → 30.** Per-game line **held** at yesterday's 9.5 pts; only availability moved. **Mechanism (in-window, and this is the point):** Cleveland is reportedly weighing a **waive-and-stretch** of his $5.4M contract across three years (~$1.8M/yr cap hold) to fit Harden under the first apron it became hard-capped at via the Watson sign-and-trade — [Chris Fedor (cleveland.com) and Bobby Marks (ESPN)](https://www.nbcsports.com/fantasy/basketball/player-news/2026-08-21/report-cavs-considering-waiving-cam-whitmore), relayed by [HoopsHype](https://www.hoopshype.com/story/sports/nba/rumors/2026/08/21/cavs-discussing-waive-and-stretch-for-cam-whitmore/91401003007/), [RealGM](https://basketball.realgm.com/wiretap/287067/Cavs-Weighing-Waiving-And-Stretching-Cam-Whitmore), [SI/Cavaliers](https://www.si.com/nba/cavaliers/onsi/cavs-likely-to-waive-the-forward-they-just-acquired-in-trade-from-washington-01m0exverm2g) and [Yahoo](https://sports.yahoo.com/articles/cavaliers-reportedly-waiving-15m-former-163539818.html). He is reported as **not expected to play a game in Cleveland**.

**Why this licenses an edit yesterday's pull could not make.** Yesterday I refused to discount his GP because the only availability evidence — a season-ending deep vein thrombosis — was dated December/January, far outside the window, and DATA-PULL §3 leaves rows without in-window news alone. Today there is an in-window, multiply-sourced **role** mechanism, and the arithmetic behind it (hard cap + Harden's $97M) is confirmed rather than speculative. That is a different kind of evidence, and it is inside the rule.

**On the number:** 30 GP is a probability-weighted guess and I want that stated plainly. The realistic range is 0 games (never cleared, or never signed after a waiver) to a partial season on a minimum deal somewhere. 30 sits near the middle, weighted toward the low end by the still-unresolved medical clearance. Direction **[LIKELY]**; magnitude **[SPECULATIVE]**. He was **not** deleted from the pool — §3 reserves deletion for retirement, overseas moves, or a lost season with no stash value, and a 22-year-old former first-rounder who may land elsewhere has stash value.

**No change (news checked, projection already consistent):** Kawhi Leonard 35 GP, Tyrese Haliburton 60 GP, Jalen Duren, Bennedict Mathurin, Mark Williams, Alex Sarr, Peyton Watson, Max Strus, Tre Mann.

## 3. Board movement (computed — engines re-run, baselines diffed by script)

**Draft-kit board.** Regenerated; **byte-identical on a second run** (determinism check). Script-computed diff vs the pre-pull snapshot:

- Entered top-200: **none**. Exited: **none**. Moves ≥3 ranks: **none**. Top 12 unchanged.
- One team-label change: **James Harden FA → CLE**. He holds **#36** — only the label moved, which is exactly right, because the kit's `team` column is a label and does not enter the z-computation.
- **Whitmore's GP cut moved nothing**, for the same reason his reprice moved nothing yesterday: he sits outside the top 200 both before and after. GP enters only the final availability multiplier, not the z-pool, so there was no ripple to look for. Real in the CSV, invisible on the published board.

**Engine header fix (§4 — the board must not contradict itself).** The FA caveat named Harden as one of five FA rows and said he was "still unsigned as of this build." **My own change falsified that**, so it was rewritten in the same pull: Harden is recorded as having left the FA block on 8/20 with his terms, the count is corrected to **four** FA rows, and the incorrect "at most two guaranteed years" is corrected on the board itself rather than quietly removed.

**Deck board: zero movement.** Script-computed against the pre-edit pool — no entries, no exits, **no moves ≥3 ranks, and not one unedited player moved even 1 rank**. A team-label-only edit cannot shift a z-score, and the diff confirms it did not. (Contrast yesterday, where a genuine reprice produced a 56-player 1–2 rank ripple. The check distinguishes the two cases, which is what it is for.)

## 4. Watchlist / open items

- **Cam Whitmore — the flag from yesterday resolved partway, in the direction the flag predicted.** Yesterday this report said his row was "lying" and needed an owner decision or a primary source. Twenty-four hours later, Cleveland is reported to be waiving him. **Still unresolved: his medical clearance.** No source in two pulls says he has been cleared from the DVT. The next concrete event to watch is the waiver actually being processed and where (or whether) he signs. If he is waived and unsigned by the October run, the row should be deleted, not discounted further.
- **The 8/20 decision NOT to add Whitmore to the deck pool was vindicated within a day.** It was taken on the reasoning that a fringe-rotation wing with an uncleared blood clot is not top-245 draftable — not on "I am blocked from sourcing him." Had the softer framing won, the deck would now carry a row for a player about to be waived.
- **James Harden — closed.** Off the watchlist entirely. His deck judgment card is **rebased, not carried**: the destination and signing-drag risks are gone, and the remaining −0.05 is now explicitly age-37 load management, which matters because his row carries **no availability tag at all**.
- **Cleveland's cap situation is now the live constraint on two other FA rows.** The first-apron hard cap plus Harden's $97M has effectively **closed the CLE route for both Kuminga and DeRozan** — the same squeeze that is costing Whitmore his roster spot. Kuminga's live routes are now MIN and the LAL sign-and-trade; DeRozan newly picks up **Washington** interest alongside Miami and Denver. Recorded on both cards.
- **Kawhi Leonard — HELD at 35 GP and −0.20 for the THIRD consecutive pull.** The only in-window item is the NBA publicly pushing back on the 8/17 ESPN report, which was already recorded on 8/18. Trade still frozen, still a Clipper, mid-September Board of Governors still the checkpoint.
- **Mark Williams' foot — FIFTH consecutive pull with no in-window news.** Every search result is still from the 2025-26 season and playoffs (a third-metatarsal stress reaction, March 2026, recurring in the April playoffs). His 58-GP kit discount and `inj-risk` deck tag have now stood unexamined since 7/27. **This has rolled forward four times with the same recommendation; it should be treated as an October must-do rather than a watchlist line.**
- **Cross-plane inconsistency noticed while dating Sarr's surgery, flagged not fixed:** the deck prices Alex Sarr at `inj-foot-risk` (×0.78 availability) while the kit carries him at 72 GP (≈0.90 under the streaming-credit model). Both encode the same June surgery, at materially different severities. Out of window and out of scope for a delta pull; worth reconciling in October.
- **Jaden Ivey** — fourth pull on contract-tracker evidence only. Still the board's weakest label, still says so on the board.
- **Four deck-draftable names still missing from the kit's 220-row pool** — D'Angelo Russell (MEM), Al Horford (GSW), Cedric Coward (MEM), Deandre Ayton (WAS), plus **Peyton Watson (CLE)**. Unchanged from 8/20, and **owner decision D1 from that report is still open**: does a committed, gate-verified projection on the deck plane count as a sourced base rate for the kit? Nothing this window bears on it.
- **PHI logjam** unchanged as the board's biggest projection-uncertainty cluster.

## 5. Deck plane (§7)

Deck-plane window 8/20 → 8/21. Applied: Harden FA → CLE (team label only); `data/rosters_official.json` **re-authored for 8/21** with Harden added to the Cleveland evidence list and the full window write-up; **JUDGMENT re-authored and re-dated 2026-08-21**:

- **Harden's card rewritten to SIGNED** and the residual **rebased** from signing-drag to age-37 load management (held at −0.05 — same number, different and now-stated reason).
- **Kuminga** — CLE route marked closed by the hard cap plus Harden's deal, leaving MIN and the LAL sign-and-trade.
- **DeRozan** — Washington added to the interest list; CLE route closed by the same squeeze.
- **Kawhi** — third consecutive hold, recorded on the card.
- FA re-verification dates advanced to 8/21 on Kuminga, DeRozan, Cam Thomas and Ivey; Ivey's carry count incremented to four pulls.

Gates: `verify_rosters.py` **245/245, zero mismatches, zero unmatched**, dated 2026-08-21 (fallback-partial — direct ESPN pull 403'd, reported not swallowed). `freshness --stamp` green with the pool-changes assertion recorded. `build_deck.py` green, injection round-trip OK, pool `8bbd5bf918b1…`. `check_parity.py` **EXACT MATCH**. `test_gates.py` **10/10**.

Deck **republished to the existing artifact URL** and verified live by re-fetching: `built: 2026-08-21`, `evidence_date: 2026-08-21`, pool hash `8bbd5bf918b1cb16e8b41f122c0d0145c1e59c2fb21182b5c77b5a38051d8d9d` matching the local build, 245 rows. `git status` run on both repos before committing (lesson 20) — only expected files modified.

## 6. Assumptions & deviations

- **A1 — Pushed to `claude/fantasy-basketball-data-pull-687jyp` on both repos, not `main`.** The 8/20 PRs (kit #7, deck #12) are **still open and unmerged**, so this pull's commit **stacks on that branch** rather than starting fresh — correct per the standing branch instruction, and it means the two PRs now each carry two days of pulls. `origin/main` remains at 8/18 on both repos until they merge. Done pending PR merge.
- **A2 — Harden's line was held, not repriced,** on a signing that is normally a repricing trigger. The two available mechanisms genuinely offset; inventing a number from that would be false precision.
- **A3 — Whitmore's 30 GP is a probability-weighted guess,** stated as such in §2 with its range. The alternative — leaving 68 GP on a player reported as never going to play for his team — was worse.
- **A4 — "Agreed" is treated as "signed"** for Harden's team label, consistent with how this system handled Beal (8/13), Draymond Green and Sochan. The formal signature had not been filed at build time.
- **D1 (carried from 8/20, still open)** — cross-plane sourcing for the missing kit rows. No new information this window.

## 7. Verification report (adversarial-verify)

**Criteria** — C1 dated sources from this run, 2+ outlets for tier-movers: **PASS** (Harden: 5 outlets incl. AP; Whitmore: 6 incl. two named reporters). · C2 CSV team edits paired with provenance, gate exits 0: **PASS**. · C3 board movement computed by script: **PASS** on both planes, kit board byte-identical on a determinism re-run. · C4 labels honest: **PASS** (§2). · C5 deck gates green, verification dated today: **PASS** (245/245, parity EXACT, gates 10/10). · C6 republished to the **existing** URL at `built: 2026-08-21`: **PASS**, verified by re-fetching. · C7 both repos pushed: **PASS** (designated branches — A1).

**Refutation — attacks that found something.**
- **Dating Alex Sarr's surgery** moved it from "August injury news" to 2026-06-16 and prevented an unjustified availability cut on a row that already encodes it. Third consecutive pull where the dating check stopped a bad edit (Ingram/Giddey 8/18, Watson's knee 8/20, Sarr today).
- **Re-reading yesterday's own Whitmore flag against today's news** found the in-window mechanism that made the edit legal — rather than either leaving a known-wrong row or reaching for the out-of-window medical story a second time.
- **Checking the deck diff for a ripple and finding literally zero** confirmed the label-only edit was label-only. A non-zero result here would have meant something was wrong with the edit.
- **Noticing the Sarr severity mismatch across planes** while doing the dating check surfaced a genuine inconsistency neither plane's gates can see, since each is internally consistent.
- **Checking whether the 8/20 board text survived the news** caught that the engine header still called Harden unsigned and still printed the wrong contract length.

**Attacks that found nothing.** Kit-board determinism (byte-identical). Deck injection round-trip. JS↔Python parity (EXACT, 6 states). Pre-republish orphan check (live matched `HEAD` exactly). Post-republish hash equality. `git status` on both repos. Gate suite 10/10.

**Regressions.** None. Both boards moved only where intended; both repos green at final state.

**Status** — delivered. The weakest parts of this report, in order: **Whitmore's 30-GP figure (§2, A3)** and his still-unverified medical clearance, the search-only evidence channel (§0), **Mark Williams' fifth unexamined pull (§4)**, and the Sarr cross-plane severity gap.
