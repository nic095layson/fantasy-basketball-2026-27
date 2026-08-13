# Draft Kit Data Pull — After Report

**Run date:** 2026-08-13 · **Window swept:** 2026-07-27 → 2026-08-13 (17 days — last logged pull was the 7/27 validation sweep)
**Scope:** delta pull under DATA-PULL.md, both planes, ending in a deck republish. Not the October full re-verification.

```
📋 Freshness Check — 2026-08-13
✓ Verified: 2 team changes, 1 retirement, 3 FA statuses re-verified, 5 targeted
  injury checks, Kawhi probe status — every claim below carries a dated source
⚠ Changes since 7/27: 2 rows edited in projections CSV; 0 added, 0 removed
✗ Cannot verify: Cam Thomas and Jaden Ivey FA status (absent from every remaining-FA
  list found; no signing found either) · Mark Williams' foot (no in-window news, second
  pull running) · all claims this run rest on search results, not fetched pages (see §0)
```

**Gate:** `check_provenance.py` → **PASS** (exit 0) — all rows sourced; verified 2026-07-13 .. 2026-08-13.
`--max-age-days 14` → **FAIL**, expected and structural: a delta pull does not re-verify rows without news, and the bulk of the pool still carries 7/13–7/27 verification. The October full run clears it. Flagged, not worked around.

---

## 0. Window and method limits — read before the findings

**The window was 17 days, not 1.** DATA-PULL §1 requires saying so and widening the sweep; I did (13 searches across transactions, FA trackers, injuries, retirements, overseas moves, and every open item from the 7/27 report).

**Research channel was degraded.** `WebFetch` to every sports domain — nba.com, ESPN, RealGM, Spotrac, HoopsRumors, Yahoo, CBS, RotoWire, basketball-reference — returned `EGRESS_BLOCKED` from the environment's network policy. Web **search** worked. So every claim below rests on dated search results (headline, dated summary, outlet URL) rather than fetched article bodies. Consequences, stated plainly:

- The two-source rule was satisfiable by outlet count, not by reading two articles. Where I cite two outlets, I saw two independent search results, not two pages.
- Search summaries were actively unreliable this run: one asserted Kawhi Leonard "returned to the Toronto Raptors" (false — his trade is still on hold) and another asserted Denver was waiving Jonas Valančiūnas (stale by a month). **Every candidate change below was re-checked with a targeted query before it was applied**, and the two conflations above were caught and discarded.
- This is a real reduction in evidence quality versus prior pulls. Allowing the sports domains (or at least `site.api.espn.com`) in the environment network policy would restore it.

**The two planes had drifted apart in the opposite direction from 7/27.** This repo sat at 7/27 while the deck plane had been refreshed on 8/9 and republished on 8/10. The 7/27 incident was the deck lagging the kit; this time the kit lagged the deck. Cross-plane team-label diff at start: 208 shared names, **2 disagreements** (both resolved below).

## 1. NBA roster changes applied to the CSV

| Player | Change | Date | Sources |
|---|---|---|---|
| **Draymond Green** | FA → **GSW**, re-signed 1yr/$27.7M — team label only | agreed 7/28 | [NBA.com](https://www.nba.com/news/draymond-green-warriors-free-agency-2026), [AP via ClickOnDetroit](https://www.clickondetroit.com/sports/2026/07/28/draymond-green-agrees-to-a-1-year-277m-contract-to-remain-with-the-warriors-ap-source-says/), [Golden State of Mind](https://www.goldenstateofmind.com/general/111804/warriors-re-sign-draymond-green-to-one-year-27-7-million-deal) |
| **Jeremy Sochan** | FA → **POR**, 1yr veteran-minimum, **non-guaranteed camp deal** — team + projection | ~8/1 | [Hoops Rumors](https://www.hoopsrumors.com/2026/08/trail-blazers-jeremy-sochan-agree-to-one-year-deal.html), [Blazer's Edge](https://www.blazersedge.com/trail-blazers-free-agency-rumors-news/114847/portland-trail-blazers-sign-jeremy-sochan-nba-free-agency-news-new-york-knicks-san-antonio-spurs), [Yahoo](https://sports.yahoo.com/articles/jeremy-sochan-signs-portland-trail-161838789.html) |

Both were already correct in the deck plane (applied 7/28 and 8/1 there) — this pull closed the gap in the draft-kit plane. Every CSV team edit travelled with its `roster-provenance.csv` row; the gate enforces it.

**Russell Westbrook retired** — announced 8/12 after 18 seasons ([NBA.com](https://www.nba.com/news/russell-westbrook-retires-nba-after-18-seasons), [NBC Sports](https://www.nbcsports.com/nba/news/after-18-seasons-russell-westbrook-announces-retirement-from-nba), [Chicago Sun-Times 8/12](https://chicago.suntimes.com/nba/2026/08/12/russell-westbrook-retires-after-18-seasons-in-nba), [Al Jazeera](https://www.aljazeera.com/sports/2026/8/13/russell-westbrook-announces-nba-retirement-after-18-seasons), [KGOU 8/13](https://www.kgou.org/sports/2026-08-13/former-thunder-star-nba-mvp-russell-westbrook-retires-after-18-seasons)). He was **not** in this repo's 220-row pool, so no row changed here — but `rank_engine.py`'s header still named him as the example of an excluded unsigned FA, and the deck plane still carried him as a draftable free agent. Both fixed (§3, §5).

**FA rows re-verified still unsigned** (team stays FA, provenance refreshed to 2026-08-13): **James Harden** — CLE framework and financial terms now reported agreed (~2yr/$75M with a player option) but **unsigned**, so consistent FA treatment holds; **DeMar DeRozan** — still unsigned, MIA the market favorite, 44 of the top 50 FAs have signed and he has not; **Jonathan Kuminga** — still unsigned, August reporting calls his market "a mess". ATL declining his $24.3M option also **closes the 7/27 open item**: the GSW-vs-ATL rights discrepancy resolves to ATL.

**Checked and correctly absent / unchanged — no edit:** Kentavious Caldwell-Pope (PHI 1yr/$3.88M, 8/5), Lonnie Walker IV (DEN, 8/5), Andre Jackson Jr. (TOR, 8/4), Naji Marshall (DAL extension, 8/2), Dillon Brooks (PHX extension, 8/8), Johni Broome (PHI→LAC, 7/28), Sean Pedulla (waived LAC, 8/7) — none are in the 220-row pool. Wembanyama's rookie-max extension is not a team change. Xavier Tillman and Boban Marjanović left for Turkey; neither is in the pool.

## 2. Projection changes (labeled per Operating Principle 3)

- **Jeremy Sochan** — [ESTIMATED]. 66 GP / 24 mpg / 9.5 pts → **58 GP / 16 mpg / 6.3 pts** (5.0 fga, 1.3 fta, 0.3 3pm, 4.3 reb, 1.7 ast, 0.7 stl, 0.3 blk, 0.9 tov). Percentages unchanged — no efficiency mechanism. **Mechanism (>20% swing, §4.4):** he signed a *non-guaranteed* veteran-minimum camp deal, not a rotation contract, into a crowded Portland frontcourt (Avdija, Camara, Grant, Clingan) on a team that also added Ja Morant; the standing row was priced as a San Antonio starter, which no longer describes any job he holds. Direction **[LIKELY]**; magnitude **[SPECULATIVE]** — if he wins a rotation spot outright this is too harsh, and if he is cut in camp it is far too kind. GP 58 blends make-the-roster against camp-cut risk.
- **Draymond Green** — no projection change. Same franchise, same role, and §3 says stats stay absent a sourced role mechanism.
- **No change** (news checked, projection already consistent): **Tyrese Haliburton** 60 GP — the strongest positive signal in the window ("I'm playing five-on-five... I can pretty much say I'm back"; Pacers reportedly "extremely optimistic" for opening night) and I still **held**, because incremental rehab optimism is not a discrete event and the 7/27 session held at 60 on the same class of evidence. Raising him would be a magnitude guess dressed as news. Watchlisted instead — see §4. **Damian Lillard** 45 GP (on track, no new timeline), **Joel Embiid** 45 GP (camp-ready reporting, team explicitly not expecting 82 — the existing discount already says that), **Josh Giddey** 72 GP — his ankle surgery is dated **2026-05-13**, outside the window, expected ready for camp; no edit.

## 3. Board movement (computed — engine re-run, baseline diffed by script)

Board regenerated with `rank_engine.py`; **byte-identical on a second run** (determinism check). Diff computed by script against the pre-pull snapshot, not by eye.

- **Entered top-200:** Jonathan Kuminga #200.
- **Exited top-200:** Jeremy Sochan (was #177 — the reprice).
- **Moves ≥3 ranks:** Cam Thomas #121 → #118 (−3; pool-composition side effect, not a projection change). That is the only one.
- **Team-label changes on the board:** Draymond Green FA → GSW.
- **Top 12 unchanged.**

**Engine header fixes (§4 — the board must not contradict itself).** `rank_engine.py`'s hard-coded caveats had gone stale in three ways and were rewritten in this pull: it named **Russell Westbrook** as the standing example of an unsigned FA (he retired 8/12); it listed **Draymond Green** and **Sochan** among rows "still labeled FA" (both now have teams); and its Kawhi bullet was dated 7/24. The FA bullet now also records honestly that Cam Thomas and Jaden Ivey could not be re-verified.

## 4. Watchlist / open items

- **Cam Thomas and Jaden Ivey — CANNOT VERIFY.** Neither appears on any remaining-free-agent list I found (which named Harden, Westbrook, DeRozan, Kevin Love, Beal, and the three RFAs), and no signing turned up for either. Absence from a list is not evidence of a signing. Their rows and provenance are **unchanged from 7/27** — I did not bump `verified_on`, because I did not verify them. First thing to settle next pull.
- **Tyrese Haliburton** — held at 60 GP against genuinely positive news (§2). If camp reporting confirms a full opening-night role, that is the mechanism to raise him, and it would move a top-15 player.
- **Kawhi Leonard** — still LAC, trade **still on hold**, his 35-GP placeholder stands. As of 8/10 the outside law firm's fact-finding is complete and Leonard expects to be a Raptor before camp, but a sanction may route through an arbitrator with the NBPA intervening, so the "could run into 2027" tail has not closed. Bennedict Mathurin's RFA remains frozen by the same probe.
- **RFAs still unsigned mid-August:** Jalen Duren (DET, no max offer), Bennedict Mathurin (LAC), Peyton Watson (DEN, sign-and-trade interest from LAC/MIL). Duren and Mathurin are in the pool; Watson still is **not** (see below).
- **Mark Williams' foot** — no in-window news found; every result was from the 2025-26 season and playoffs. His 58-GP discount stands unexamined for a second consecutive pull.
- **Five deck-draftable names still missing from this repo's 220-row pool** — D'Angelo Russell, Al Horford, Cedric Coward, Deandre Ayton, Peyton Watson. Carried from the 7/27 report **unresolved**; still recommended for the next pull with sourced base rates.
- **PHI logjam** unchanged as the board's biggest projection-uncertainty cluster; KCP's signing is now official (1yr/$3.88M, 8/5), which confirms the mechanism behind the 7/27 Simons trim.

## 5. Deck plane (§7) — and the orphaned 8/10 build

Deck-plane window was 8/9 → 8/13. Applied there: **Westbrook** tagged `out-retired` (the documented convention at `hoops.py:151` keeps the row at availability 0.0, excluded from every board — so I did *not* delete it), and **Sochan repriced** — the deck had landed his POR placement on 8/1 but never the role-reprice, leaving a starter's line under a `camp-deal` note tag that the availability function does not discount. Evidence file re-authored for 8/13; `verify_rosters` **245/245, zero mismatches**; `build_deck.py` green with injection round-trip OK; `check_parity.py` **EXACT MATCH**; `test_gates.py` **10/10**. The footer Data paragraph was rewritten — it still claimed Westbrook was "still a true free agent". Deck **republished to the existing artifact URL**, verified live at `built: 2026-08-13`, `evidence_date: 2026-08-13`, matching pool hash, JUDGMENT dated 8/13, Westbrook absent from the judgment layer.

**The finding that stopped this pull mid-flight.** The published artifact was serving a **2026-08-10 build that exists nowhere in git**. It carried real work: a Monte-Carlo daily-fill lineup model (`dailyFillWeights`, 32 trials, day-of-week weights, hashed game-count draw) replacing `lineupWeights`, plus an owner-requested **Fit → ΔECW** column swap. Its matching `scripts/hoops.py` change was never committed either, so that JavaScript **disagrees with the canonical engine by 20 card orderings** (z-scores and name fixtures still match — the divergence is purely the recommendation ordering), while the same page's Logic paragraph still claims it is "verified against engine output at build time".

Rebuilding on the repo's committed code would have silently discarded the owner's 8/10 work; publishing the 8/10 code would have shipped an unverifiable recommendation ordering into a live draft tool. I stopped and asked. **Owner decision: publish the parity-clean committed code.** The orphaned build is preserved verbatim at `docs/recovered/draft-deck-2026-08-10-published.html` in the deck repo with a README explaining exactly what it contains and how to land it properly. The published page has therefore **reverted to the Fit column** and the older lineup model until that work is re-landed with its Python half — a visible, deliberate regression, recorded here rather than left to be discovered.

This is the **third** instance of the same failure mode in this system's short history: 7/24 (a pull that never landed), 7/27 (the deck serving a stale pool), and now 8/10 (a republish whose source never reached git). The first two produced protocol amendments. This one is a stronger signal: the artifact can be edited and published without the repo ever seeing it, so the repo is not actually the only persistent layer — it is only the *intended* one.

## 6. Assumptions & deviations

- **A1 — Pushed to `claude/fresh-deck-pull-report-s20noc`, not `main`.** DATA-PULL §0 defines done as "pushed to `main`"; this session is under standing instructions to develop on a designated branch and never push elsewhere without permission. The branch instruction wins, so this pull is **done pending PR merge**, and I am not claiming a `main` landing. Same for the deck repo. Merging the two PRs completes §0 items 1–4.
- **A2 — Sochan's magnitude is my judgment, not a computation.** Argue with it; the direction is the defensible half.
- **A3 — Westbrook kept as a tagged row rather than deleted** in the deck pool, following the documented convention (`hoops.py:151`) rather than the Valančiūnas precedent of removal. Retirement and departure-for-Europe are handled differently by design; availability 0.0 achieves the same fantasy outcome.
- **A4 — Malcolm Brogdon is NOT a defect.** He sits in the deck pool as an FA tagged `out-retired`; he retired 2025-10-15. I checked this specifically because it resembled the retired-Chris-Paul defect found on 7/13. It is correct handling, not a miss.

## 7. Verification report (adversarial-verify)

**Criteria** — C1 every change carries a dated source from this run, 2+ outlets for tier-movers: **PASS**, with the §0 channel caveat stated rather than buried. · C2 CSV team edits paired with provenance edits, `check_provenance.py` exits 0: **PASS**. · C3 board movement computed by script, not eyeballed: **PASS** (diff script; determinism re-run byte-identical). · C4 computed/estimated/speculative labeled: **PASS** (§2). · C5 deck plane updated, `verify_rosters` clean and dated today, build gates green: **PASS** (245/245, parity EXACT, gates 10/10). · C6 deck republished to the **existing** URL at `built: 2026-08-13`: **PASS** (verified by fetching the live page after publishing). · C7 both repos pushed with PRs: **PASS** (on designated branches — see A1).

**Refutation — attacks that found something.** Checking the published page before overwriting it (required by the publish tool's conflict guard, and the right thing regardless) exposed the entire 8/10 orphan; had I published blind, I would have destroyed it and never known. Re-checking Brogdon rather than assuming a Chris-Paul repeat found correct handling and avoided a wrong "fix". Re-querying each candidate change caught two false search summaries (Kawhi "returned to Toronto", Valančiūnas being waived by Denver). Reading `hoops.py` before touching Westbrook's row found the `out-retired` convention and prevented a wrong deletion. Checking Giddey's surgery date moved it out of the window and prevented an unjustified GP cut.

**Attacks that found nothing.** Cross-plane team-label diff after the edits (0 disagreements). Board determinism on re-run. Deck injection round-trip. JS↔Python parity on the published build. Published-page-vs-local-build pool hash equality.

**Regressions.** One, deliberate and owner-approved: the published deck reverts to the Fit column and the pre-8/10 lineup model (§5). No unintended regressions — unchanged players' ranks are stable across the baseline diff, the top 12 is unchanged, and both repos' gates are green at final state.

**Status** — delivered. The weakest parts of this report, in order: the search-only evidence channel (§0), Sochan's magnitude (§2), and the two FA rows I could not verify at all (§4).
