# After-report — 2026-09-29 data pull + deck v31

**Owner request (2026-09-29, verbatim):** "Pull and merge. What fix do you
propose for the drift?" (The drift proposal is §9; it is a proposal, not a
change.)

Pull window: 2026-09-28 → 2026-09-29 (1 day: league media day into the first
day of training camps). Gate: `check_provenance.py` → `PROVENANCE GATE: PASS —
all rows sourced; verified 2026-07-13 .. 2026-09-29`, exit 0.

**Method.** One search sweep of 47 dated queries: a ledger-shaped transaction
check (Spotrac and ESPN transaction pages, RealGM; F5), the 11 flagged
receipts (10 carried plus the new Dillingham card), the eight team shadows
(CHI, DET, GSW, LAC, NOP, NYK, POR, SAC), an F6 diff of media-day injury
coverage against the 41-row tag inventory in both directions (every excluded
and risk row with a media-day item was checked by name), and the FA rows on
both planes. Direct fetches to sports domains stay blocked by the egress
policy (Yahoo and BVM returned EGRESS_BLOCKED this run), so every claim rests
on dated search results, two outlets minimum for anything that moved a row.
Edits applied by script with exact-match assertions; both boards diffed by
script against the pre-pull snapshot; the deck built through gates 1–7/F8
and driven end to end by the step-5b browser gate.

**Headline.** One placement moved: Charlotte waived Rob Dillingham on 9/28,
two days after taking him in the Hield trade. One availability tier moved:
the Clippers disclosed at media day that Brandon Ingram had a partially torn
Achilles found and repaired during his May heel surgery; he is out for the
start of the season with no team timetable, so his deck row now carries the
×0.78 risk multiplier and a wider card, and his kit GP drops to 48. Neither
change moves a board rank: Ingram's nine-category total is slightly negative
on both planes and the availability model never shrinks a non-positive
total, and Dillingham sits outside both top-200s. Every flagged open item
held — Duren skipped the camp opening with the qualifying-offer deadline on
Thursday 10/1, Brunson is fully cleared, Porzingis is still out indefinitely
with the GM hoping for a quick return. No trades in the window. Deck v31 built
and published; the D1/D2 button fixes from the validation ride this build.

## 1. Roster changes

| plane | change | count |
|---|---|---|
| both | Rob Dillingham CHA → FA — waived by Charlotte 2026-09-28, two days after arriving in the Hield trade; a crowded point-guard room (Yahoo ×2, NBC Sports, Hoops Rumors, HoopsHype, ClutchPoints, BVM). Kit GP 66 → 50 for the missing team [LIKELY direction, SPECULATIVE magnitude], per-game line held; deck note plus a −0.10 destination-discount card; kit provenance re-sourced to NBC Sports 9/28 | 1 |
| deck | Brandon Ingram availability tag: none → `inj-achilles-risk` (×0.78) — partially torn left Achilles found and repaired at the 2026-05 heel surgery, disclosed at the 9/28 media day; out for the start of the season, no team timetable, "week-by-week", not participating in camp much; reporting points at November to early December (ESPN, NBA.com, NBC Los Angeles, Last Word on Sports, Bleacher Report, Yahoo). Team unchanged (LAC); line held; card widened −0.05 → −0.15. Kit GP 64 → 48 [LIKELY direction, SPECULATIVE magnitude] | 1 |
| deck | Notes only, no tier change: Bradley Beal (right-knee inflammation, misses the start of camp — Hoops Rumors, SI); Dereck Lively II (running and shooting, still not cleared — NBA.com recap, Yardbarker); Walker Kessler (fully cleared per Pelinka — NBC Sports, CBS); Zach Edey (cleared for full-speed work, expected ready for the season per Kleiman — SI Grizzlies, Yahoo); Kristaps Porziņģis (Dunleavy: informed Sunday, "hopefully back soon", not ruled out for the season start — NBC Sports, NBA.com); Jimmy Butler (light on-court work at three-quarter speed, Warriors hope for early 2027 — NBC Sports Bay Area, SF Chronicle) | 6 |

Two-source rule: the Dillingham waiver carries six outlets, the Ingram
disclosure six; every note edit carries two.

## 2. Flagged-item receipts (F1) — verdicts

- **Duren — HELD −0.08.** Skipped media day 9/28 and the camp opening 9/29;
  not on Detroit's 20-man camp roster; barred from practice while unsigned;
  declined the fully guaranteed 5yr/$200M; qualifying-offer deadline Thursday
  10/1 (Yahoo, NBC Sports, SI, Detroit Sports Nation; Langdon on record 9/29).
- **Brunson — HELD −0.05.** "Fully cleared" (his own show 9/24; Hoops Rumors,
  Yahoo, BVM); camp opened 9/29; no first-practice report by run time.
- **Ingram — WIDENED −0.05 → −0.15** and tagged (§1).
- **Porziņģis — HELD −0.10, veto unchanged.** Out indefinitely; Dunleavy not
  marking him out for the season start (NBC Sports, NBA.com, Hoops Rumors).
- **Russell, Cam Thomas, Ivey, Lonzo Ball — HELD, all unsigned** as camps
  open (Hoops Rumors, ClutchPoints, NBC Sports, Spotrac, heavy). The "Lakers
  sign Ivey 1yr/$4M" Instagram post resurfaced in this sweep; it was
  fact-checked fake on 9/22 and no outlet carries it (garble log, 9th
  sighting).
- **Sochan — HELD −0.2.** In camp on the Exhibit 9 non-guaranteed deal; camp
  9/29–10/2; fighting for the backup power-forward spot (NBC Sports, SI
  Blazers, Rip City Project, Yahoo).
- **Mathurin — HELD −0.05.** On the 21-man camp roster under Mosley; camp
  previews still project bench scoring punch behind Herb Jones (Yahoo camp
  preview, NBA.com).
- **Dillingham — NEW card −0.10** (§1).

## 3. Window sweep, team shadows, injury sweep

- **Transactions (F5 ledger check).** Spotrac and ESPN transaction pages, RealGM
  and Hoops Rumors via search: zero trades in the window. Signings and
  waivers on no row: Knicks two-ways Tyler Nickel and Kevin McCullar Jr.
  (9/28 — ClutchPoints, Yahoo); Exhibit 10 churn 9/25–9/27 (GSW Nick Boyd
  waived, Miles Kelly signed; BKN Nick Pringle waived; WAS KeShawn Murphy
  waived, Settle and Livingston signed; UTA Terrell Brown Jr.; MEM Lewis,
  Dixon, Collins, Lovering; SAS R.J. Davis; DET Romeo Weems; SAC Leaky Black
  and Tristen Newton; MIN Kennedy Chandler; CHI Dwayne Sutton; LAC Jamarion
  Sharp waived) — Spotrac, RealGM. Nembhard: no row. The MEM cut-down (Hawkins,
  Clayton, Kris Murray) is still reported-not-executed (Yahoo, TalkBasket,
  SI Grizzlies) — ninth pull; Hawkins' row holds.
- **Team shadows.** CHI (camp opened 9/29 in Chicago; 21-man roster; Buzelis
  listed at 196 lb — SI Bulls, Yahoo, Bleacher Nation), DET (Duren absent —
  above), GSW (camp at BYU-Hawaii 9/29–10/3; Curry's knee healthy, extension
  signed; Butler and Moody travelling; Porziņģis not — NBA.com, KNBR, NBC
  Sports Bay Area), LAC (camp in Hawaii 9/29–10/3; Ingram and Beal — above;
  preseason vs GSW 10/4), NOP (21-man camp roster under Mosley; Zion at 271 lb
  — NBA.com, Crescent City Sports, WWL), NYK (camp opened 9/29; two-ways
  above), POR (camp 9/29–10/2 under Nori; Lillard and Morant both spoke at
  media day — OPB, KATU, SI Blazers), SAC (19 in camp for 18 spots; Newton
  camp deal 9/26 — NBA.com Kings, RotoWire, Sactown Sports). Anthony Davis
  (WAS) said he will decide after the season whether to stay; not a trade
  request (Washington Times, Bleacher Report) — no change.
- **Injury sweep vs the F6 tag inventory (41 tagged rows).** Cleared or
  progressing with tags kept by convention (first season back): Haliburton
  (100%, no restrictions), Kyrie Irving (no restrictions), Kessler (fully
  cleared), Edey (full speed), Kawhi (feels good, 65 games last year), Embiid
  (knee "behind him", leaner), Lillard (rehab complete, media day), Dejounte
  Murray and Trey Murphy (spoke at media day, no status detail), Jalen
  Williams (untagged, "totally healthy" — correct). Still out, tags kept:
  Butler (acl-recovery), Moody (patellar-recovery), Porziņģis (risk, out
  indefinitely), Lively (risk, not cleared), Knueppel (note; aims for the
  10/21 opener, re-evaluated in week one — Yahoo, BVM). New: Ingram (tagged),
  Beal (note). Paul George and Jaren Jackson Jr.: no dated 9/28 item surfaced
  in three queries each; tags unchanged, receipts below say so. Returning-
  but-untagged: none found.
- **FA rows.** Kit: Cam Thomas, Ivey, Broome — all unsigned (Broome: RotoWire,
  CBS, Hoops Wire). Deck adds Russell, Lonzo, Dillingham (unsigned) and the
  retired/overseas rows (Westbrook, Brogdon, Valančiūnas, Batum) — unchanged.

## 4. Board effects (computed, never eyeballed)

- **Kit.** `top-200-2026-27.md` regenerated: no entries, no exits, no moves of
  three or more ranks. Ingram stays #88 (zPG −0.49 → the availability model
  never shrinks a non-positive total, so the GP cut is recorded but rankless
  by design). Dillingham is not in the top 200 on either GP. The header's
  stale Kawhi caveat (investigation limbo; flagged 9/28) was rewritten to the
  executed trade and the 9/22 extension.
- **Deck.** By adjusted value over the 321 draftable rows: no entries, no
  exits, no moves of three or more. Ingram stays #68 at −0.195 (same reason);
  Dillingham #201 unchanged; Beal #174 unchanged. Pool sha256 `c0bf82bf4d39`
  (was `9d11cb45`): the notes and the FA relabel changed the file, not the
  math.

## 5. Deck build and publish

`build_deck.py` on 2026-09-29: roster verification 330/330, 0 mismatches,
dated today (fallback-partial: direct ESPN still 403); freshness stamped with
the pool-changes note; JUDGMENT re-dated 2026-09-29 with eleven cards
re-authored (Brunson, Ingram, Porziņģis, Cam Thomas, Ivey, Sochan, Lonzo,
Russell, Mathurin, Duren, new Dillingham); colophon Data paragraph rewritten
for the window; planes 308 shared, team 0, exclusion 0, drift 0, propagation
0, waived 2 by name (Ingram and Dillingham kit-GP cuts — no deck GP column,
carried as the multiplier and the note); market `yahoo-2026-09-22.csv`, 296
of 330 priced, 7 days old (warning threshold 14). "safe to publish". This
build is the first to carry the V-D1/V-D2 fixes (empty-input Insert/Resync
warnings render immediately; the sweep panel counts the pool) and the first
under step 5b of §7.

## 6. Gates (2026-09-29)

| gate | result (evidence: the command's own output line) |
|---|---|
| kit `check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-09-29 |
| kit `check_report.py` on this file | see the commit: run after this file was written |
| deck `judgment_open_items.py --check-report` on this file | see the commit: 11 flagged names, one receipts row each |
| deck `verify_rosters.py` | 330/330, 0 mismatches, evidence dated 2026-09-29 |
| deck `check_planes.py` | 308 shared · team 0 · exclusion 0 · drift 0 · propagation 0 (2 waived) |
| deck `build_deck.py` | all gates pass; safe to publish |
| deck `check_parity.py`, `test_card.py`, `test_draft.py`, step-5b `full_dom_check.mjs` | recorded in the commit message and §Provenance below |

## 7. Watchlist / open items

- **Duren** — QO deadline Thursday 10/1. Either signature resolves the card
  (re-check 10/1); a holdout into the regular season widens it.
- **Ingram** — first preseason week: a setback or a December-plus timeline
  converts the risk tag to an exclusion (owner decision D-P1 below).
- **Porziņģis** — first preseason week; a sourced regular-season absence
  would make this an exclusion (veto already keeps him off the card).
- **Brunson** — clears to zero on the first practice report.
- **Beal** — knee; the first practice report either clears the note or dates
  a longer absence.
- **Lively, Knueppel** — opener status; both re-evaluated in the season's
  first week.
- **Russell, Dillingham, Cam Thomas, Ivey, Lonzo, Broome** — a signing
  reprices the row that day.
- **Sochan** — Portland's 15-man decision after the first preseason game.
- **MEM cut-down** — ninth pull unexecuted; Hawkins' row holds.
- **Yahoo market paste** — seven days old; a fresh paste in early October
  re-prices the Mkt column before the 10/14 draft.
- **Owner decisions carried:** D-P1 Ingram exclusion vs risk (this pull chose
  the risk tier on the Lively precedent and the Nov–Dec reporting; the
  owner may prefer the exclusion class given the Achilles); D4 drift fix
  (§9); survival chips (D53-2), Tatum at #10 (D53-3), resolver dot-folding
  (D53-4); the five stale pre-session draft PRs.

## 8. Open-item receipts

| player | query run | dated finding |
|---|---|---|
| Jalen Brunson | Jalen Brunson wrist Knicks training camp first practice September 2026 | fully cleared 9/24; camp opened 9/29; no practice report yet — Hoops Rumors, Yahoo, BVM 9/24 |
| Brandon Ingram | Brandon Ingram heel Clippers media day status September 28 2026 · Brandon Ingram partially torn Achilles Clippers timeline return | partial Achilles disclosed 9/28, out for the start of the season, Nov–early Dec — ESPN, NBA.com, NBC LA, Last Word, B/R 9/28 |
| Kristaps Porzingis | Kristaps Porzingis Warriors health update indefinitely September 2026 · Warriors media day Curry Porzingis | out indefinitely, GM hopes soon — NBC Sports, NBA.com, Hoops Rumors 9/28; KNBR 9/28 |
| Cam Thomas | Cam Thomas signs free agent training camp September 2026 | unsigned, waiting for an offer — NBC Sports, Yahoo |
| Jaden Ivey | Jaden Ivey signs free agent September 2026 | unsigned — Spotrac, heavy; Instagram "Lakers 1yr/$4M" is the 9/22 fake, resurfaced |
| Jeremy Sochan | Jeremy Sochan Trail Blazers roster training camp September 29 2026 | in camp, Exhibit 9, backup-PF battle — SI Blazers, Rip City Project, Yahoo, NBC Sports |
| Lonzo Ball | Lonzo Ball signs free agent September 2026 | unsigned; retirement report denied — Spotrac, heavy, uSports |
| Rob Dillingham | Hornets waive Rob Dillingham September 28 2026 | waived 9/28 — Yahoo ×2, NBC Sports, Hoops Rumors, HoopsHype, ClutchPoints, BVM |
| D'Angelo Russell | D'Angelo Russell signs free agent September 2026 | unsigned as of late September — Hoops Rumors, ClutchPoints, Yahoo |
| Bennedict Mathurin | Bennedict Mathurin Pelicans training camp role September 2026 · New Orleans Pelicans training camp news September 29 2026 | camp roster, bench role projected — Yahoo camp preview, NBA.com, Crescent City Sports |
| Jalen Duren | Jalen Duren qualifying offer Pistons September 29 2026 · Detroit Pistons training camp news September 29 2026 | skipped camp opening, declined 5yr/$200M, QO deadline 10/1 — Yahoo, NBC Sports, SI, Detroit Sports Nation |
| (window ledger) | NBA transactions September 29 2026 · NBA trade September 28 OR 29 2026 · RealGM NBA transactions September 2026 signed waived | zero trades; two-ways and Exhibit 10s only — Spotrac, ESPN, RealGM, Hoops Rumors |
| (injury sweep) | NBA training camp injury news September 29 2026 · NBA media day injury update September 28 2026 · per-player queries: Lillard, Lively/Irving, Butler/Moody, Embiid/George, Jackson Jr., Murray/Murphy, Edey, Knueppel, Kawhi, Morant, Kessler, Curry, Bulls, Lakers | §3 — Hoops Rumors/Yardbarker/BVM, NBA.com, SI, Yahoo, NBC Sports, ESPN |
| (Paul George, Jaren Jackson Jr.) | three media-day queries each | no dated 9/28 item surfaced; tags unchanged |
| (Anthony Davis) | Anthony Davis Wizards trade request media day September 28 2026 | will decide after the season; no request — Washington Times, B/R 9/28 |
| (MEM cut-down) | Grizzlies waive Jordan Hawkins OR Kris Murray OR Walter Clayton September 2026 | still reported-not-executed — Yahoo, TalkBasket, SI Grizzlies |
| (Johni Broome) | Johni Broome signs September 2026 free agent | unsigned — RotoWire, CBS, Hoops Wire |
| (CHI/DET/GSW/LAC/NOP/NYK/POR/SAC) | team-shaped camp-news queries, one each | §3 |

## 9. The drift fix — proposal (owner question, not executed)

The 9/29 validation found four derived kit artifacts that read the *current*
pool when re-run, so their numbers change as the pool grows, and one script
that overwrites a shared ledger. Proposed fix, in three parts:

1. **Stamp inputs into every output.** Each generating script (`slate.py`,
   `mock_draft_league_projection.py`, `market/market_stats.py`,
   `market/yahoo_market.py`, `market/build_market.py`) writes a one-line
   provenance header into what it produces: the input files it read, each
   file's sha256, its row count, and the generation date. A reader can then
   see at a glance which pool a number came from. Cost: a shared helper of
   ~15 lines; no number changes.
2. **An as-of mode plus a gate.** Scripts that analyse a moment (the 8/24
   league projection, the 9/16 market statistics) gain `--as-of <date>`,
   which reads their inputs from git at that date instead of the working
   tree. A new `report/check_derived.py` re-runs every committed dated
   analysis in as-of mode and fails on any diff, the way `check_parity.py`
   fails on engine drift. Re-running today then reproduces the committed
   numbers exactly, and a report can never silently mean something else.
   Cost: ~45 minutes; DATA-PULL §0 gains "check_derived passes".
3. **Merge, never overwrite.** `build_market.py` merges `provenance.csv` rows
   by (source, fetched_on) instead of rewriting the file, so the Yahoo rows
   survive a re-run; `yahoo_market.py` scopes its unmatched-absence ledger to
   the pool snapshot of the paste's date, so the 9/15 intake stops tripping
   its own gate against a pool that grew later. Cost: ~20 minutes.

Nothing in the proposal touches a projection, a board or the deck; the
slate was already regenerated on 9/29 and points at the newest paste.

## Provenance and bounds

- Research channel: WebSearch summaries only; direct fetches of Yahoo and
  BVM returned EGRESS_BLOCKED this run. Every row edit rests on two or more
  independent outlets named in its row.
- Media day was 9/28 and camps opened 9/29 the same morning as the sweep;
  first-practice reports (Brunson, Beal, Lively) land next pull.
- Lines were not repriced for Dillingham or Ingram: no source gave minutes
  to reprice against; only GP moved, labeled.
- Ingram's tier choice (risk, not exclusion) is a judgment call recorded as
  owner decision D-P1 above.
- Research effort: 47 searches and 2 blocked fetches, all this session.
