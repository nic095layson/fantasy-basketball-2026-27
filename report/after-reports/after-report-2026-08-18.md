# Draft Kit Data Pull — After Report

**Run date:** 2026-08-18 · **Window swept:** 2026-08-13 → 2026-08-18 (5 days)
**Scope:** delta pull under DATA-PULL.md, both planes, ending in a deck republish. Not the October full re-verification.

```
📋 Freshness Check — 2026-08-18
✓ Verified: 1 trade (2 players), 1 free-agent signing, 5 FA statuses re-verified,
  6 targeted injury/status checks, Kawhi probe status — every claim carries a
  dated source from this run
⚠ Changes since 8/13: 0 rows edited in the draft-kit CSV (none of the moved
  players are in its 220-row pool); 3 rows edited in the deck pool; 0 added,
  0 removed on either plane
✗ Cannot verify: Jaden Ivey's free-agent status by dated news (contract-tracker
  evidence only — see §4) · Mark Williams' foot, third consecutive quiet pull ·
  all claims this run rest on search results, not fetched pages (see §0)
```

**Gate:** `check_provenance.py` → **PASS** (exit 0) — all rows sourced; verified 2026-07-13 .. 2026-08-18.
`--max-age-days 14` still **FAILS**, expected and structural for the same reason as 8/13: a delta pull does not re-verify rows without news, and the bulk of the pool still carries 7/13–7/27 verification. The October full run clears it. Flagged, not worked around.

---

## 0. Window and method limits — read before the findings

**The window was 5 days.** Normal delta pull, no widening required.

**Research channel is still degraded, and I re-tested rather than assuming.** `WebFetch` to `hoopsrumors.com` and `nba.com` both returned `EGRESS_BLOCKED` this run, as did `espn.com`; `verify_rosters.py`'s direct pull to `site.api.espn.com` failed with a 403 through the proxy tunnel. Web **search** works. So every claim below rests on dated search results (headline, dated summary, outlet URL) rather than fetched article bodies — the same reduction in evidence quality flagged on 8/13, now confirmed as persistent rather than transient.

Consequences, stated plainly:

- Where I cite two outlets, I saw two independent search results, not two articles read end to end.
- I could not fetch Basketball-Reference, which is the sourcing route DATA-PULL §3 requires for adding a player to the pool. That directly blocks the five-name pool gap carried since 7/27 (§4).
- **Allowing the sports domains — or at minimum `site.api.espn.com` — in the environment network policy is now the single highest-value fix available to this system.** It would restore the complete roster-verification guarantee, unblock pool additions, and raise every claim in these reports from search-summary to primary-source.

**The two planes were in sync at the start of this pull**, unlike the last two runs. The 8/13 pull landed both planes and the deck's published build matched git (pool hash `306d144c…` on the live page, identical to `HEAD`). No orphaned artifact this time — the 8/10 incident's work was re-landed with its Python half in that pull's PR #10, and the parity check confirms it (§5).

## 1. NBA roster changes

**Applied to the deck pool. None of them touch the draft-kit's 220-row pool** — this is the expected asymmetry: the deck pool carries 245 rows including deeper rotation players.

| Player | Change | Date | Sources |
|---|---|---|---|
| **Dennis Schröder** | CLE → **CHA** (with cash, for Tre Mann) | reported 8/15 | [ESPN](https://www.espn.com/nba/story/_/id/49611835/sources-cavaliers-trading-schroder-cash-hornets-mann), [NBA.com](https://www.nba.com/news/charlotte-cleveland-trade-schroder-mann), [CBS Sports](https://www.cbssports.com/nba/news/dennis-schroder-trade-grades-cavaliers-hornets-tre-mann/), [Spectrum News](https://spectrumlocalnews.com/nc/charlotte/sports/2026/08/15/hornets-cavs-trade-dennis-schroder) |
| **Tre Mann** | CHA → **CLE** (same trade) | reported 8/15 | same |
| **Bradley Beal** | FA → **LAC**, 2yr/$13.2M with a player option | reported 8/13 | [ESPN](https://www.espn.com/nba/story/_/id/49604287/beal-stays-clippers-2-year-deal-worth-132-million-deal), [NBC Sports](https://www.nbcsports.com/nba/news/bradley-beal-re-signs-with-clippers-for-reported-two-years-13-2-million), [RealGM](https://basketball.realgm.com/wiretap/286994/Bradley-Beal-Clippers-Agree-To-Two-Year-$132M-Deal), [Last Word](https://lastwordonsports.com/basketball/2026/08/13/beal-agrees-to-return/) |

Every deck team edit travelled with its `data/rosters_official.json` evidence entry.

**FA rows re-verified still unsigned** (team stays FA, provenance refreshed to 2026-08-18 on both planes):

- **James Harden** — still unsigned. Cleveland is in "constant communication" and expects a resolution soon, but the reporting adds a detail that matters: Harden told the Cavs he would sign once they landed a wing, and they landed none — LeBron chose Philadelphia, and Kuminga, Watson and DeRozan are all still open ([HoopsHype 8/14](https://www.hoopshype.com/story/sports/nba/2026/08/14/cavaliers-remain-constant-communication-harden-strongly-pursuing-peyton-watson-jonathan-kuminga/91310471007/)). The 8/13 report's "framework and terms agreed" framing was softer than this week's reporting supports; corrected.
- **DeMar DeRozan** — still unsigned, still on the remaining-FA lists ([HoopsHype FA rankings 8/16](https://www.hoopshype.com/story/sports/nba/2026/08/16/2026-nba-free-agent-rankings-best-players-available/88589278007/)). Denver is effectively out after signing Lonnie Walker IV; SAS/TOR/GSW are the named interest.
- **Jonathan Kuminga** — still unsigned. A Lakers sign-and-trade (~$45M, Vanderbilt plus picks to Atlanta) is reported as the leading route, with Minnesota and Cleveland also in.
- **Cam Thomas** — still unsigned, **confirmed by dated reporting this window** ([Yardbarker](https://www.yardbarker.com/nba/articles/why_cam_thomas_is_still_unsigned_as_nba_free_agency_drags_on/s1_17776_44164367), [SI/Yahoo](https://sports.yahoo.com/articles/free-agency-again-showing-brooklyn-170006959.html)). **This closes the 8/13 cannot-verify flag** — the item the last report named as "first thing to settle next pull."
- **Jaden Ivey** — still FA, but only half-closed. See §4.

**Checked and correctly absent from both pools — no edit:** Trendon Watford (NOP, 1yr/$2.9M, 8/17), Haywood Highsmith (re-signed PHX, 8/17). Brandon Ingram's heel surgery and Josh Giddey's ankle surgery both surfaced in the injury sweep and both date to **May 2026**, outside the window — checked precisely because a search summary presented them as August news. No edit on either.

## 2. Projection changes (labeled per Operating Principle 3)

All three are deck-plane edits; the draft-kit CSV has **zero** projection changes this window.

- **Dennis Schröder** — [ESTIMATED]. 13.0 pts / 5.4 ast on 10.5 fga → **10.5 pts / 4.5 ast on 8.5 fga** (2.3 reb, 1.3 3pm, 2.1 fta, 0.8 stl, 1.9 tov). Percentages unchanged — no efficiency mechanism. **Mechanism (>20% fga swing, §4.4):** in Cleveland he was the lead ball-handler alongside Mitchell, and the Cavaliers carry no other true point guard; the reporting explicitly frames his Charlotte role as *backup point guard behind Coby White*, on a rebuilding roster that also carries Brandon Miller, Kon Knueppel and Grayson Allen. Direction **[LIKELY]**; magnitude **[SPECULATIVE]** — a rebuilding team could also hand a 32-year-old veteran fewer minutes than the depth chart implies, which would make this too kind.
- **Bradley Beal** — [ESTIMATED]. 16.5 pts on 13.0 fga → **13.0 pts on 10.0 fga** (3.0 reb, 3.2 ast, 1.6 3pm, 2.0 fta, 0.9 stl, 1.6 tov). Percentages unchanged. **Mechanism (>20% swing):** he was priced as an unsigned free agent assuming a starter's role; $6.6M AAV is a bench-veteran contract, the Clippers' guard room is Garland and Mathurin ahead of him, and he played six games in 2025-26. Direction **[LIKELY]**; magnitude **[SPECULATIVE]**. His `inj-hip-risk` tag (×0.78 availability) is unchanged and carries the health half — the note prose was updated from "unsigned" to the signing.
- **Tre Mann** — direction-only edit: assists 4.2 → **4.6**, nothing else. **Mechanism:** the trade removes Cleveland's only true backup point guard and he is the replacement (Strus and Merrill are off-guards). I deliberately did **not** raise his scoring: the standing 12.5 pts already runs well ahead of last season's 5.5 ppg on 36% shooting across 53 games, so the honest read is that his line is generous, not conservative, and the opportunity bump does not license inflating it further.

- **No change** (news checked, projection already consistent): **Tyrese Haliburton** 60 GP. This is the **third consecutive pull holding him**, and it deserves a straight answer rather than another deferral. The evidence this window is genuinely strong — he says he is "100% cleared," he is playing 5-on-5, and Indiana's opener is set for 10/21 vs New Orleans. It is still *pre-camp* evidence, and a 60-GP line for a first season back from an Achilles tear does not price "will he be ready for opening night"; it prices load management and second-half attrition across 82 games, which no August quote can speak to. **The trigger to raise him is camp and preseason participation without a setback — late September.** If that lands, it moves a top-15 player and should be acted on immediately, not held a fourth time.
- **No change:** **Kawhi Leonard** 35 GP (see §4), **Damian Lillard**, **Joel Embiid**, **Mark Williams** — no in-window news on any.

## 3. Board movement (computed — engines re-run, baselines diffed by script)

**Draft-kit board: unchanged.** Regenerated with `rank_engine.py`; **byte-identical on a second run** (determinism check). Diff computed by script against the pre-pull snapshot:

- Entered top-200: **none**. Exited: **none**. Moves ≥3 ranks: **none**. Team-label changes: **none**. Top 12 unchanged.
- The only diff in `top-200-2026-27.md` is the generation date, the provenance date span (now `2026-07-13 – 2026-08-18`), and the two header bullets rewritten below.

**Engine header fixes (§4 — the board must not contradict itself).** Two hard-coded caveats in `rank_engine.py` were contradicted by this window's findings and were rewritten in this pull:

1. The FA bullet still said *"Cam Thomas and Jaden Ivey could NOT be re-verified in the 2026-08-13 window."* Both were re-verified as unsigned this run, so the bullet now names all five FA rows with a 2026-08-18 verification date — and states outright that Ivey's is the weakest label on the board rather than burying that in a report.
2. The Kawhi bullet was dated 2026-08-10 and framed around the arbitrator tail. Rewritten to the 8/17 state, including the mid-September Board of Governors checkpoint.

**Deck board: three moves, all isolated to the three edited rows.** Computed by script against `HEAD`'s pool:

| Player | Move | Cause |
|---|---|---|
| Bradley Beal | #129 → **#165** (−36) | the reprice |
| Dennis Schröder | #208 → **#235** (−27) | the reprice |
| Tre Mann | #212 → **#201** (+11) | the assist bump plus pool-composition effect |

No entries, no exits, top 12 unchanged, and **no unedited player moved 3 ranks or more** — which is the check that the edits did what they were supposed to and nothing else.

## 4. Watchlist / open items

- **Jaden Ivey — half-closed, and I want to be exact about which half.** His free-agent status is corroborated: Chicago waived him on **2026-03-30 for conduct detrimental to the team** (not the knee injury the deck's judgment card had blamed — that was a factual defect, now corrected), he was paid his full $10.1M, and no signing has surfaced across four searches this run and several last run. What I do **not** have is a dated in-window news item affirming "still unsigned"; the evidence is a contract-tracker page and the absence of a signing. I bumped his `verified_on` because that is more than the last pull had, and labelled the weakness on the board itself rather than silently upgrading it. If the sports domains open up, verify him from a primary source first.
- **Tyrese Haliburton** — held at 60 GP for the third pull, with the raise trigger now stated as a date and a condition (§2) rather than a vague "if camp reporting confirms."
- **Kawhi Leonard** — still LAC, trade **still on hold**, 35-GP placeholder stands. New this window (8/17): ESPN reported the investigation found **no evidence** that Steve Ballmer funneled money to him through team sponsors; the NBA publicly disputed that report as containing "numerous and significant inaccuracies" without saying which parts; and the inquiry narrowed to whether the Clippers' *introductions* of Leonard to sponsors were themselves circumvention. A mid-September Board of Governors meeting is the named next checkpoint. **I held the deck's −0.20 judgment adj rather than softening it** — the news is favorable and contested at the same time, and manufacturing a delta out of reporting the league is publicly disputing would be a guess dressed as an update. Mathurin's RFA remains frozen by the same probe.
- **The three RFA standoffs are now all reported at an impasse**, which is a change in kind from "unresolved":
  - **Jalen Duren** (DET) — pushing for a five-year rookie max (~$287M) off an All-NBA Third Team season; Detroit will not offer it; both sides dug in past mid-August; he is reportedly weighing the $9.6M qualifying offer. Deck adj widened −0.10 → **−0.15**.
  - **Bennedict Mathurin** (LAC) — negotiations at a standstill, seeking $20–25M, LAC open to a sign-and-trade, the $8.8M qualifying offer now openly floated.
  - **Peyton Watson** (DEN) — declined Denver's five-year/$70M against a stated ask north of $25M/yr; CLE, MIL, ATL and LAC all pursuing sign-and-trades, which may be his only route out.
- **Mark Williams' foot** — **third consecutive pull with no in-window news**; every search result is still from the 2025-26 season and playoffs. His 58-GP discount has now stood unexamined since 7/27. This should not keep rolling forward silently: either a primary-source check clears it in the October run, or the discount should be re-derived from the 2025-26 game log rather than carried on inertia.
- **Five deck-draftable names still missing from this repo's 220-row pool** — D'Angelo Russell (MEM), Al Horford (GSW), Cedric Coward (MEM), Deandre Ayton (WAS), Peyton Watson (DEN). **Carried unresolved for the third consecutive pull, and this time with a concrete blocker rather than an omission:** DATA-PULL §3 requires base rates for a new row to come from a stats source *fetched this run*, and Basketball-Reference is egress-blocked. I will not synthesise projections from search summaries into a board the owner drafts off. This is now formally blocked on the network-policy fix in §0, or on the October full run.
- **PHI logjam** unchanged as the board's biggest projection-uncertainty cluster.

## 5. Deck plane (§7)

Deck-plane window was 8/13 → 8/18. Applied: the three pool edits above, `data/rosters_official.json` re-authored for 8/18 with dated evidence for every changed placement, and the **JUDGMENT layer re-authored and re-dated 2026-08-18**:

- **Bradley Beal moved off the unsigned-free-agent block** (−0.25 → −0.05). The destination discount is gone because he has a destination; the residual is camp-rotation risk only. Deliberately small to avoid double-counting: the role is already in the repriced line and the health is already in the `inj-hip-risk` availability tag.
- **Jaden Ivey's card corrected** — it claimed he was waived for a knee. He was waived for conduct.
- **Cam Thomas's card** now records that the 8/13 cannot-verify flag is closed.
- **Jalen Duren widened to −0.15**; Kuminga, DeRozan, Harden, Mathurin and Watson re-authored against this week's reporting; **Kawhi held at −0.20** with the reasoning stated on the card itself.
- **New cards for Dennis Schröder and Tre Mann**, each carrying the trade and the honest caveat on its own reprice.
- The footer Data paragraph was rewritten for this window — it still described Beal as a true free agent and Kawhi's status as of 8/10.

Gates: `verify_rosters.py` **245/245, zero mismatches**, dated 2026-08-18 (fallback-partial mode — the direct ESPN pull 403'd through the proxy, reported not swallowed). `build_deck.py` green with injection round-trip OK. `check_parity.py` **EXACT MATCH** (2205 z-cells, 45 name fixtures, 72 df_hash vectors bit-identical, 78 card orderings across 6 committed states). `test_gates.py` **10/10**.

Deck **republished to the existing artifact URL** and verified live by re-fetching the page: `built: 2026-08-18`, `evidence_date: 2026-08-18`, pool hash `f09492c7a625…` matching the local build, 245 rows.

**No orphan this time.** I checked the published page before overwriting it (the 8/13 report's hard-won lesson) and it matched git exactly — pool hash `306d144c…`, built 8/13. The 8/10 orphaned build's work was properly re-landed with its Python half in that pull's PR, and parity is exact, so the ΔECW column and daily-fill model are now canonical rather than artifact-only. That failure mode has been closed, not just survived.

## 6. Assumptions & deviations

- **A1 — Pushed to `claude/fresh-deck-pull-report-ebqheg`, not `main`.** DATA-PULL §0 defines done as "pushed to `main`"; this session is under standing instructions to develop on a designated branch. The branch instruction wins, so this pull is **done pending PR merge** and I am not claiming a `main` landing. Same for the deck repo. Merging the two PRs completes §0 items 1–4.
- **A2 — Schröder's and Beal's magnitudes are my judgment, not computations.** Both directions are well sourced; both magnitudes are arguable and labelled as such.
- **A3 — Tre Mann got an assist bump and nothing else,** where a fuller reprice was defensible in either direction. His projection is generous relative to his actual production and his opportunity just improved; those pull opposite ways, and a minimal edit is the honest resolution of that rather than a confident number.
- **A4 — Ivey's `verified_on` was bumped on partial evidence.** Argue with this one; the alternative was leaving it at 7/27 and pretending I learned nothing, which is also wrong. The label is flagged as the board's weakest in the board's own header.
- **A5 — Kawhi's judgment adj was held rather than softened** on news that arguably favors him. Stated in §4.

## 7. Verification report (adversarial-verify)

**Criteria** — C1 every change carries a dated source from this run, 2+ outlets for tier-movers: **PASS**, with the §0 channel caveat stated up front rather than buried. · C2 CSV team edits paired with provenance edits, `check_provenance.py` exits 0: **PASS**. · C3 board movement computed by script, not eyeballed: **PASS** on both planes (determinism re-run byte-identical on the kit board). · C4 computed/estimated/speculative labeled: **PASS** (§2). · C5 deck plane updated, `verify_rosters` clean and dated today, build gates green: **PASS** (245/245, parity EXACT, gates 10/10). · C6 deck republished to the **existing** URL at `built: 2026-08-18`: **PASS**, verified by re-fetching the live page after publishing. · C7 both repos pushed with PRs: **PASS** (on designated branches — see A1).

**Refutation — attacks that found something.**
- Checking the *dates* on the Ingram and Giddey surgery stories moved both out of the window and prevented two unjustified GP cuts on stories a search summary had presented as August news.
- Reading the deck's existing Ivey card against this run's research found it blamed a knee injury for a conduct waiver — a factual defect that had been rendering to the owner as a stated reason to fade him.
- Diffing the deck board by script confirmed that **no unedited player moved ≥3 ranks**, which is the check that catches a reprice with unintended pool-wide side effects.
- Checking the published artifact before overwriting it confirmed no orphan — the check that found the entire 8/10 incident last time, run again precisely because it paid off then.
- Re-testing `WebFetch` against two sports domains rather than assuming the 8/13 block still held turned "probably still blocked" into a stated, reproducible finding with a named fix.
- Tracing the five missing pool names to a *specific blocked requirement* (DATA-PULL §3's fetched-stats rule vs. the Basketball-Reference block) turned a third silent carry-forward into an actionable blocker.

**Attacks that found nothing.** Kit-board determinism on re-run (byte-identical). Deck injection round-trip. JS↔Python parity (EXACT across 5 states). Published-page-vs-local pool hash equality. Cross-plane consistency of the five shared FA labels. Gate suite 10/10.

**Regressions.** None. No unintended movement on either board; both repos' gates are green at final state.

**Status** — delivered. The weakest parts of this report, in order: the search-only evidence channel and what it blocks (§0), Jaden Ivey's half-verified FA status (§4), the Schröder and Beal magnitudes (§2), and Mark Williams' 58-GP discount now standing unexamined for a third pull (§4).
