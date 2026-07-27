# Full-System Validation — After Report

**Run date:** 2026-07-27 (second session of the day) · **Trigger:** owner found the published Draft Deck serving the 2026-07-24 pool ("aging pull, 3 days old") hours after the morning's fresh pull landed on this repo's `main`.
**Scope:** root-cause the stale artifact, fix it and the protocol so it cannot recur, then validate the whole system (both repos + published artifact) for other silent errors.

---

## 1. Root cause of the stale artifact (three surfaces, three truths)

The system has **two data planes** that share news but not files:

| Surface | What it said on 7/27 ~11AM | Why |
|---|---|---|
| This repo (`main`) | fresh through 2026-07-27 | the morning pull landed (`e439169`..`af25c1b`) |
| Published Draft Deck | built 2026-07-24, pool 227 | renders only what `build_deck.py` baked in at the last republish |
| `yahoo-fantasy-basketball` `main` | data plane fresh-as-of 2026-07-11 | the deck source, builder, verifier, and the 7/22–24 refreshes were stranded on the unmerged PR #2 branch (50 commits ahead) |

No single surface showed an error; the drift was only visible by comparing all three. The morning pull was correct and complete under the protocol as written — the protocol itself lacked the republish duty.

## 2. Fixes implemented

1. **Deck rebuilt and republished to the same URL** — pool refreshed to 246 rows for 2026-07-27, `verify_rosters` 246/246 clean (fallback-partial), `build_deck.py` gates green, injection round-trip OK, JS-vs-Python rank parity EXACT (241 available rows), JUDGMENT layer re-authored for 7/27. Header stamp now reads fresh-today.
2. **Protocol amended (both surfaces):** `DATA-PULL.md` §0 items 5–6 + new §7 (deck sync + republish are definition-of-done for every pull; pushed to this repo's `main` at `950fb86`); the fantasy-basketball skill's publish-gate law now names republish staleness a live defect; LESSONS.md lesson 11 records the incident.
3. **Stranded branch consolidated:** PR #2's branch merged into PR #3's branch (`d046ff5`), so one merge lands the deck source, builder, verifier, all daily pulls, and today's refresh on yahoo `main`. PR #3 title/body updated; PR #2 is superseded (close after PR #3 merges). PR #1 (lesson-9 addendum) has been open since 7/13 — owner decision.

## 3. Silent errors found and fixed during validation

All sourced per the two-source rule; details in the yahoo repo commit `83f05d4` and freshness note.

| # | Defect | Where | Fix |
|---|---|---|---|
| 1 | **Harden carried as CLE while unsigned** (option declined 6/29; his provenance row even cited the decline story) — inconsistent with Draymond's FA treatment in the same file | both planes | FA in both planes + judgment entry (re-sign framework agreed, paperwork gap); board regenerated, only the Tm cell changes (#36) |
| 2 | **Draymond labeled GSW in deck plane** while unsigned (7/25–27 reporting) | yahoo pool + evidence file | FA + judgment discount (destination near-certain) |
| 3 | **Cole Anthony stale as unsigned FA** — he signed with MIL after a ~7/12 MEM buyout (2 sources) | yahoo pool + JUDGMENT | team MIL + backup-PG role reprice; stale "waived July 20, unsigned" judgment entry retired |
| 4 | **Valančiūnas still in deck pool as NBA FA** — left for EuroLeague Žalgiris 7/15 | yahoo pool | row removed (matches this repo's morning fix) |
| 5 | **20 board-ranked players missing from the deck pool** (#110–#198: Grant, Caruso, Dort, McCain, rookie tail) — pool-completeness law gap | yahoo pool | ported from this repo's verified projections (per-row dated provenance); MUST_HAVE +8 (all names inside the 156-pick universe) |
| 6 | **4 malformed CSV rows** — unquoted commas in note fields silently truncated notes and created a phantom column on every parse | yahoo `data/players.csv` | notes reconstructed and properly quoted |
| 7 | **"Jamie Jaquez Jr." misspelling** (correct: Jaime) | yahoo pool + evidence | renamed both places |
| 8 | **Deck footer still claimed "LeBron is an unsigned FA"** in the same build whose manifest announced his PHI signing — the builder soft-syncs only the date, not the prose | `docs/draft-deck.html` | Data paragraph rewritten for 7/27; garbled duplicated sentence in the Logic paragraph fixed |
| 9 | **Kuminga rights discrepancy resolved** — ATL holds his rights (2 late-July sources), not GSW; morning report had flagged it single-source | JUDGMENT + this report | judgment entry updated; watchlist item closed |
| 10 | **CRLF artifact introduced by this session's own tooling** (csv.writer default) — caught and normalized back to LF in both repos | both repos | `b314e85` + included in `83f05d4` |

## 4. Verified-clean (checks that found nothing)

- Cross-plane team labels: 187 shared names, **zero disagreements** after fixes (Draymond/Harden were the only two).
- Ripple placements from the sweep all already correct in the pool: Ayton WAS, Hardy LAL, Kessler LAL, Trae Young WAS, Allen/O'Neale CHA, McCollum/Kispert ATL, DLo MEM (the 7/23 "AD/DLo to WAS" note was corrected to MEM by the 7/24 grind — verified right).
- Provenance gate PASS (this repo), `--max-age-days 14` PASS; board regeneration deterministic (byte-identical on re-run).
- JS engine ↔ `hoops.py` rank parity exact before AND after the rebuild.
- All MKT_PIN names exist in the pool (no dead market pins).
- No scheduled Routine conflicts: no automated daily refresh exists (see §6).

## 5. Watchlist / open items (flagged, not edited)

- **Harden/Draymond/DeRozan/Beal signings expected imminently** — MIA reported "huge progress" on DeRozan+Beal (7/26); next pull re-labels them the moment deals are official.
- **Fringe in-window moves, no pool rows:** Hezonja→CLE (NBA return, 7/26), Dalen Terry waived by PHI, Bufkin/Phillips camp deals, Spencer Jones offer sheet matched by DEN.
- **This repo's 220-pool lacks five deck-draftable names** (deck ranks in parens): D'Angelo Russell (#137), Al Horford (#138), Cedric Coward (#147), Deandre Ayton (#148), Peyton Watson (#154). Same defect class as the Miles Bridges miss (A3, morning report) — recommend adding in the next pull with sourced base rates.
- **Morez Johnson** (DAL #9 pick, strong SL) — single source, not in either pool; October candidate.
- **ESPN direct roster verification remains proxy-blocked** — verification runs fallback-partial off the evidence file; allowing `site.api.espn.com` in the environment network policy upgrades it to the complete direct guarantee.

## 6. Recommendations (owner decisions, not defects)

1. **Merge PR #3** (`yahoo-fantasy-basketball`) — until it merges, yahoo `main` still misreports the data plane as 7/11-fresh. Close PR #2 as superseded afterward; PR #1 is a one-file lesson-9 correction also still open.
2. Consider a **scheduled Routine for the daily pull** (the "daily refresh" law currently relies on someone opening a session) — the artifact drift happened precisely on days nobody ran one.

## 7. Multi-agent validation workflow results

Ran post-fix as a 16-agent workflow: 5 parallel auditors (deck internal
consistency, fantasy board integrity, repo hygiene, deck runtime sanity,
published-page-vs-repo equality) followed by one adversarial verifier per
finding, each instructed to refute by re-running the underlying check.

**43 checks passed. 11 findings confirmed (10 LOW, 1 MEDIUM), 0 refuted.
All 11 fixed the same session:**

| Sev | Finding | Fix |
|---|---|---|
| MED | This validation report was itself untracked/unpushed (lesson-10 violation in flight) | committed in this push |
| LOW | Deck judgment comment still said "grounded in 7/22 research" beside `date: 2026-07-27` | re-dated, now tied to JUDGMENT.date |
| LOW | Kuminga carried FA while judgment says ATL holds rights — convention split vs rostered RFAs (Mathurin/Duren/Watson) unexplained | convention documented in his judgment entry (rights-held ≠ rostered) |
| LOW | `build_deck.py` truncated the manifest freshness note mid-word at 160 chars, no marker | builder now truncates at word boundary + ellipsis (both defect and fix visible in repo + published page) |
| LOW | Board header bullet listed Kuminga among FA rows but he ranks outside the top 200 | bullet annotated, board regenerated |
| LOW | Morning after-report banner said "10 rows edited" vs 8 in its own detail | corrected with correction note |
| LOW | DATA-PULL.md §7 hard-coded "227-row deck pool", stale within hours (found twice by independent auditors) | count removed — non-brittle phrasing |
| LOW | Harden post-pull edit absent from pull-log accounting | validation row added to pull-log (this push) |
| LOW | Yahoo README said "~210 players" twice vs 246-row pool | non-brittle "~250-player pool" phrasing |

The published page was re-verified equal to the repo deck after the fix
republish (manifest, BUILD_PULL, JUDGMENT date, pool, footer).

## 8. Verification report (adversarial-verify)

**Criteria** — C1 artifact republished to the existing URL, `built: 2026-07-27`: PASS (WebFetch-verified twice — after the refresh publish and after the fix publish; manifest, pool 246, footer all current). · C2 builder gates: PASS (`verify_rosters` 246/246 clean dated today; `build_deck.py` green on all three builds; injection round-trip OK each time). · C3 JS↔Python rank parity: PASS (exact, 241 available rows, run before AND after the rebuild — two-run doctrine). · C4 DATA-PULL.md amended on `main`: PASS (`950fb86`, §7 count made non-brittle in this push). · C5 yahoo work only on the designated branch, PR #3 updated: PASS. · C6 validation ≥6 dimensions with every confirmed finding fixed: PASS (news sweep 5 agents, audit+verify 16 agents, plus inline mechanical diffs; 21 total defects fixed across §3 and §7). · C7 gates green post-fix: PASS (provenance, board regen, build gates re-run after every fix batch).

**Refutation** — attacks that found something: the audit pass itself (11 confirmed findings, §7 — all fixed and re-verified); the CRLF artifact was this session attacking its own tooling output. Attacks that found nothing: cross-plane label diff after fixes; published-page-vs-repo equality; determinism re-runs; MKT_PIN dead-code check.

**Regressions** — none found: board order unchanged except documented moves; unchanged players byte-identical across regens; deck parity exact post-rebuild; both repos' gates green at final state.

**Status** — delivered. Open items live in §5 (watchlist) and are labeled; the arena punt-pivot gate study runs separately in the yahoo repo (arena lab) and its findings doc will carry its own verification.
