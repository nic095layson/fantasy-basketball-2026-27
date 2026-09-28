# After-report — 2026-09-28 data pull + deck v28

**Owner request (2026-09-28, verbatim):** "Daily sweep for the Draft Deck: run
the daily refresh per the freshness rule and pool-completeness law (rosters,
trades, injuries, signings, rookie class; two-source rule for team moves),
verify rosters, stamp freshness, rebuild through scripts/build_deck.py with
all gates, re-verify engine parity, and republish the Draft Deck artifact to
the same URL."

Pull window: 2026-09-23 → 2026-09-28 (5 days, ending on league-wide media
day). Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows
sourced; verified 2026-07-13 .. 2026-09-28`, exit 0.

**Method.** Three parallel research passes (flagged receipts + the team-shadow
set; a day-by-day transaction ledger 9/23–9/28 with the F5 zero-trade check;
a media-day injury sweep diffed against the F6 tag inventory in both
directions, rookie class included), then my own re-verification of every
claim that moved a row: the Bulls–Hornets trade, both waivers, Porzingis,
Knueppel, and the Jamal Murray tag (by direct fetch of his 2025-26 game log
and the Nuggets' season page). Edits applied by script with exact-match
assertions and a byte-identical CSV round-trip check. Board diffs computed by
script on both planes. Media day was still in progress at run time
(~10 AM PT); anything announced after the sweep lands next pull.

## 1. Roster changes

| plane | change | count |
|---|---|---|
| deck | Buddy Hield CHA → CHI — Chicago sent Rob Dillingham to Charlotte for Hield and cash, reported 9/26–9/27 (ESPN, NBA.com, CBS, Washington Post 9/27, Hoops Rumors, Last Word on Sports, RealGM ledger); his second trade in five days after ATL → CHA on 9/22; line held, bench shooter | 1 |
| both | Rob Dillingham CHI → CHA — same trade (ESPN, NBA.com, CBS, Washington Post, Hoops Rumors); line held, bench guard; kit provenance re-sourced to NBA.com 9/26 | 1 |
| deck | D'Angelo Russell MEM → FA — waived by Memphis 9/25, cleared waivers 9/27, unsigned (ESPN, NBA.com, NBC Sports 9/25, theScore, Yahoo, Hoops Rumors); new −0.20 destination card; not a kit row | 1 |
| both | Johni Broome LAC → FA — waived by the Clippers 9/24 (NBC Sports/Fischer 9/24, SI, Hoops Rumors, Yardbarker, TalkBasket); fringe row (deck 317th), line held; kit provenance re-sourced to NBC 9/24 | 1 |
| both | Jamal Murray — **tag correction, not news**: the `inj-achilles-risk` tag and kit GP 66 → 62 added in the 9/8 amendment are reverted. He played **75 games in 2025-26** (landofbasketball game log: every month October–April, longest absence two games; Wikipedia's 2025-26 Nuggets season page: 75 GP / 75 GS, 25.4 ppg, franchise single-season 3PM record 3/27). The "ruptured right Achilles, ~14 games, returned post-ASB" profile is Dejounte Murray's — his tag cites the identical profile. Deck availability 0.78 → 1.0; kit GP 62 → 66 | 1 |
| kit | Kon Knueppel GP 74 → 70 [ESTIMATED; direction LIKELY, magnitude SPECULATIVE] — left hamstring strain 9/25, out for the preseason, likely misses the start of the season, re-evaluated in week one (NBA.com, NBC Sports, ESPN, Yahoo); deck note `hamstring-monitor`, no multiplier (Bona precedent) | 1 |
| kit | Kristaps Porzingis GP 58 → 54 [ESTIMATED; direction LIKELY, magnitude SPECULATIVE] — out indefinitely with an undisclosed health issue, will not travel to the Hawaii camp, no timeline (CBS, NBC Sports, theScore, AP via myMotherLode, 9/28); deck keeps ×0.78, adds note + −0.10 card | 1 |
| kit | Dereck Lively GP 60 → 56 [ESTIMATED; direction LIKELY, magnitude SPECULATIVE] — not cleared for camp, could miss the start of the season (NBC Sports 9/25, Yardbarker, NBA.com Mavs media-day recap); deck keeps ×0.78, adds note | 1 |
| deck | Santi Aldama — note only: limited in practice after arthroscopic right-knee surgery (Yardbarker, RotoWire, CBS, Yahoo, 9/25–9/27) | 1 |
| deck | Brunson (says fully cleared) and Ingram (no status yet) — note cells updated | 2 |
| neither | Ryan Nembhard waived by CHA 9/27 (RealGM, Yahoo); Grant Williams (CHA) hamstring, misses preseason (NBC Sports, RotoWire); Gary Harris waived by DET 9/27 (ClutchPoints, RealGM); Stephen Curry signed a 2yr/$116M extension with GSW 9/25 (NBA.com, NBC, Yahoo, HoopsHype) — no row moves | — |

Rows edited: kit 6 data rows (2 team, 4 GP) + 2 provenance rows; deck 11
rows (4 placements, 1 retag, 6 notes). No rows added or removed on either plane.

## 2. Flagged-item receipts (F1) — verdicts

| player | verdict | evidence (dated 2026-09-23 to 09-28) |
|---|---|---|
| Jalen Duren | HELD −0.08 | skipped media day, cannot practice while unsigned; Detroit's offer 5yr/$200M; his camp frames it as respect, not money; Pistons not pursuing a sign-and-trade; QO deadline Oct 1 — The Athletic via Bleacher Report 9/27, Detroit Free Press via Yahoo 9/28, CBS Sports 9/28 |
| Jalen Brunson | HELD −0.05 | says he is fully cleared after the July wrist surgery (his own show 9/24) — Field Level Media, Yahoo 9/25; a player statement, not a team release; clears to zero on the first practice report |
| Brandon Ingram | HELD −0.05; still open | no heel status surfaced from media day by run time; Yahoo's 9/28 preview still lists it as open question #1; every dated item is 9/22–9/23 (Newsweek, Yahoo/heavy, Yardbarker) |
| Kristaps Porzingis | NEW card −0.10 | out indefinitely, undisclosed health issue, no timeline, won't travel to Hawaii — CBS, NBC Sports, theScore, AP 9/28 |
| D'Angelo Russell | NEW card −0.20 | waived 9/25, unsigned free agent since 9/27 — ESPN, NBA.com, NBC Sports |
| Cam Thomas | HELD FA | no dated signing in window — RotoWire, transaction ledgers (RealGM) |
| Jaden Ivey | HELD FA | no dated signing in window — RotoWire, RealGM ledger; Lakers posts remain the logged fake (garble 7) |
| Jeremy Sochan | HELD −0.20 | on Portland's official 18-man camp roster, non-guaranteed; Yahoo names Potter and Krejčí as the rivals — SI 9/28, Yahoo |
| Lonzo Ball | HELD FA | NBC reported a retirement 9/23; he denied it the same day, open to a mid-season opportunity — NBC Sports ×2 9/23, Bleacher Nation 9/24 |
| Bennedict Mathurin | HELD −0.05 | on the 21-man camp roster; bench-scorer framing holds (opinion) — Crescent City Sports 9/25, SI/Yahoo 9/24 |

## 3. Window sweep, team shadows, injury sweep

**Ledger (F5).** RealGM's transaction ledger read day by day for 9/23–9/28,
plus three trade-shaped queries: exactly one trade in the window
(Dillingham–Hield). Everything else is camp-body churn — Exhibit 10 deals and
waive-and-re-sign conversions across DEN, MIN, TOR, SAC, DAL, PHX, CHI, OKC,
MEM, DET, LAC, ORL, CLE, BKN, BOS, ATL — none on a row [SINGLE-SOURCE,
RealGM per item]. Spotrac returned 2017 data and the ESPN transactions page
came back empty; Hoops Rumors and HoopsHype story pages are robots-blocked
from this environment.

**MEM cut-down: half executed after eight pulls.** Russell waived 9/25
(§1). Jordan Hawkins was NOT waived; SI's camp preview has him, Walter
Clayton Jr. and Kris Murray competing for a place. Hawkins row holds.

**Team shadows (one query each):** CHI — the Dillingham trade, camp deals
(Boston Jr., O. Robinson, Sutton), Mallette waived; DET — Gary Harris waived
9/27, Duren absent; GSW — Porzingis, Curry extension; LAC — Broome waived,
Jamarion Sharp's two-way cut, Garland says his toe is fine; NOP — 21-man camp
roster, no injuries; NYK — five non-guaranteed players (Bruce Brown,
Konchar, Wiseman, Eubanks, Agbaji) for about one spot, no cuts yet
[SINGLE-SOURCE, TalkBasket]; POR — official camp roster 9/28; SAC — no
transactions.

**Injury sweep vs F6, both directions.**
Tagged-but-changed: **Jamal Murray** (tag was wrong — §1); **Porzingis**
(worse, card); **Lively** (worse, note). Consistent with existing tags:
Haliburton "100%, no restrictions" (Yahoo, WSB-TV/AP, WISH-TV 9/28), Irving
"not under any restrictions" (NBC, NBA.com), Lillard without limitations
(RotoWire, Bleacher Report), Kessler fully cleared (NBC, RotoWire), Sarr a
"partial participant" (NBC), Adams no back-to-backs early (RotoWire, CBS),
Curry to sit select back-to-backs, Kawhi "feeling healthy" (CP24). First-
season-back tags hold when a player is cleared — that is what the risk class
prices (Adams convention). No news in window on the other risk rows; the
exclusions (Butler, Mark Williams, Moody, Sharpe, DiVincenzo) are unchanged.
Returning-or-injured-but-untagged: **Knueppel** (note + kit GP), **Aldama**
(note); Grant Williams and Veesaar are not rows; Brandon Miller's shoulder
reads "ready to roll" [SINGLE-SOURCE, RotoWire 9/28] against an older WBTV
"sidelined" line — no action.

**Rookie class:** no 2026 first-rounder unsigned (six unsigned picks are all
second-rounders, Yardbarker 8/29); no new injury for Dybantsa, Peterson,
Boozer, Wilson, Acuff, Wagler, Burries, Steinbach or Mara. Mikel Brown Jr.
rolled an ankle last week and will ramp up at camp [SINGLE-SOURCE,
RotoWire 9/28] — no action. Pool completeness: all 120 consensus names present.

**CANNOT VERIFY:** Giannis Antetokounmpo "knee, GTD, 9/24" appears only as a
CBS injury-tracker line with no article behind it, and Miami's 9/28 media-day
coverage mentions no health concern — no action.

**Garble log — ninth instance, and the first one to ship as a row change.**
The Jamal Murray tag came from two search summaries on 9/8 ("TSN's and ESPN's
injury-returns coverage") that merged the two Murrays; it moved a top-30
player three kit slots and eight deck slots for twenty days. Also seen this
window and discarded: a Yahoo/heavy line saying Ingram would update at "the
Raptors' media day," an NBA.com line with the Hawks–Hornets trade reversed,
resurfaced 2025 media-day stories (Embiid, Zion, Tatum), and fake Lonzo-to-MIN
posts.

## 4. Board effects (computed, never eyeballed)

**Kit:** scripted diff of `top-200-2026-27.md` against the pre-edit
snapshot — 0 entries, 0 exits; one move ≥3: **Jamal Murray 29 → 26**; five
1–2-slot shifts; top 12 unchanged. Knueppel (108), Lively (118) held and
Porzingis moved 51 → 52 — GP has a damped effect under the streaming-credit
availability model. Engine header fixed in the same pull: it said "the TWO
rows still labeled FA", and Broome makes three.

**Deck:** scripted diff of `hoops.py rank` over all 319 ranked rows — 0
top-200 entries or exits; one move ≥3: **Jamal Murray 27 → 19** (value
+1.92 → +2.46); eight 1–2-slot shifts; four team labels changed; top 12
unchanged; no other value moved. Pool hash 4d0f202f → 9d11cb45.

## 5. Deck build and publish

| build | what | record |
|---|---|---|
| v28 | this pull: 4 placements, Murray retag, 6 notes, JUDGMENT re-authored and dated 2026-09-28 (10 open items, +Porzingis, +Russell), colophon rewritten for this window; Yahoo 9/22 prices re-baked (296 of 330, 6 days old) | published to the standing artifact URL as Version 28 (read back: manifest built 2026-09-28, pool 9d11cb45, host wrapper the only diff from the committed file); deck PR below |

Gate 7 refused the first build on four propagation items — the kit GP edits
for Murray, Porzingis, Knueppel and Lively have no deck stat column to land
in. Each was waived by name with its reason (recorded in the build manifest):
the deck carries the same news as availability — Murray's tag removed,
Porzingis's card and note, Knueppel's and Lively's notes.

## 6. Gates (2026-09-28)

| gate | result |
|---|---|
| kit `check_provenance.py` | PASS — verified 2026-07-13 .. 2026-09-28 |
| kit `check_report.py` + deck `judgment_open_items.py --check-report` | PASS on this file |
| deck `verify_rosters.py` | 330/330 checked, 0 unmatched, 0 mismatches, evidence dated 2026-09-28 (fallback-partial; ESPN API still egress-blocked) |
| deck `hoops.py freshness --stamp` | stamped 2026-09-28, pool_changes asserted |
| deck build gates 1–7 + F8 | green — planes 308 shared / 0 team / 0 exclusion / 0 drift / 0 propagation / 4 named exemptions recorded in the manifest; market 296/330, 6 days old; injection round-trip OK; "safe to publish" |
| deck `test_gates` / `test_card` / `test_draft` / `check_parity` | 34/34 · 35/35 · 57/57 · PARITY_RESULT |

## 7. Watchlist / open items

- **Duren** — QO deadline Thursday Oct 1; he is barred from practice while
  unsigned. A signing on either branch resolves the card; a holdout into the
  regular season widens it.
- **Ingram** — no heel status by run time; Clippers camp in Hawaii 9/29–10/3.
  A limitation → heel risk tag; full go → card clears to zero.
- **Porzingis** — no timeline; watch the first preseason week. An exclusion
  needs sourced regular-season absence, which nothing yet says.
- **Knueppel** — re-evaluated in week one of the season.
- **Lively** — not running as of 9/27; a missed-opener report is the next tell.
- **Brunson** — clears to zero on the first practice report.
- **Russell** — unsigned; a signing reprices the row that day.
- **Hawkins** — MEM camp battle with Clayton and Kris Murray; a waiver moves
  the row to FA.
- **Nembhard** — clears waivers 9/29; Denver reportedly interested in a
  two-way [SINGLE-SOURCE, Stein via Nugglove]; no row.
- **Camp bodies** — Sochan/Krejčí/Potter (POR); five non-guaranteed Knicks.
- **Yahoo market paste** — six days old; a fresh paste in early October
  re-prices the Mkt column before the 10/14 draft.
- **Stale kit engine caveat (found, not fixed — pre-existing):** the kit
  board's header still describes Kawhi Leonard's 35-GP projection as sitting
  in "league-investigation limbo"; the trade executed 9/14 and his kit row
  already reads TOR. Needs a text rewrite; out of this pull's scope.
- **Owner decisions carried:** survival chips (D53-2), Tatum at #10 (D53-3),
  resolver dot-folding (D53-4).

## 8. Open-item receipts

| player | query run | dated finding |
|---|---|---|
| Jalen Duren | Jalen Duren Pistons qualifying offer extension media day · Jalen Duren qualifying offer October 1 deadline sign · Pistons Duren agree deal OR signs qualifying offer today | skipped media day, barred from practice unsigned, Oct 1 — The Athletic/B/R 9/27, Detroit Free Press/Yahoo 9/28, CBS 9/28 |
| Jalen Brunson | Jalen Brunson wrist media day Knicks | "fully cleared" (own show 9/24) — Field Level Media, Yahoo 9/25 |
| Brandon Ingram | Brandon Ingram heel Clippers media day September 28 (+13 variants) | no status by run time — Yahoo 9/28 preview; latest dated items Newsweek, Yahoo/heavy 9/23 |
| Kristaps Porzingis | Porzingis out indefinitely Warriors media day illness · Golden State Warriors news September 28 2026 | out indefinitely, no timeline — CBS, NBC Sports, theScore, AP 9/28 |
| D'Angelo Russell | Grizzlies waive D'Angelo Russell · D'Angelo Russell clears waivers signs with | waived 9/25, unsigned — ESPN, NBA.com, NBC Sports 9/25 |
| Cam Thomas | Cam Thomas signs free agent September 2026 · "Cam Thomas" free agent unsigned training camp | no dated signing in window — RotoWire, RealGM ledger |
| Jaden Ivey | Jaden Ivey signs free agent · Jaden Ivey free agent news September 2026 | no dated signing in window — RotoWire, RealGM ledger |
| Jeremy Sochan | Jeremy Sochan Trail Blazers training camp roster spot · Sochan Krejci Cissoko Blazers final roster spot | official camp roster, non-guaranteed — SI 9/28, Yahoo |
| Lonzo Ball | Lonzo Ball signs free agent · Lonzo Ball September 2026 | retirement report denied 9/23; unsigned — NBC Sports, Bleacher Nation 9/24 |
| Bennedict Mathurin | Bennedict Mathurin Pelicans role media day · Mathurin Pelicans training camp bench Trey Murphy Zion | camp roster, bench role — Crescent City Sports 9/25, SI/Yahoo 9/24 |
| (window ledger) | NBA transactions September 2026 · NBA trade September 28 2026 · acquired trade NBA September 24 OR September 25 2026 · RealGM ledger 9/23–9/28 | one trade (Dillingham–Hield); two waivers on rows; camp churn — RealGM, NBA.com, ESPN |
| (trade) | Bulls trade Rob Dillingham Hornets Buddy Hield | ESPN, CBS, Washington Post 9/27, NBA.com, Hoops Rumors, Last Word on Sports 9/27 |
| (Broome) | Clippers waive Johni Broome | waived 9/24 — NBC Sports/Fischer 9/24, SI, Hoops Rumors, Yardbarker, TalkBasket |
| (Jamal Murray) | Jamal Murray Achilles 2025-26 season · direct fetch: landofbasketball 2025-26 game log; Wikipedia 2025-26 Nuggets season | 75 GP, no Achilles injury; the profile is Dejounte Murray's |
| (injury sweep) | NBA media day injury update September 28 2026 · will miss start of training camp 2026 · surgery September 2026 · limited in training camp · per-player queries on all 42 tagged rows | §3 — NBC, Yahoo, NBA.com, CBS, RotoWire, ESPN, AP |
| (CHI/DET/GSW/LAC/NOP/NYK/POR/SAC) | team-shaped news queries, one each | §3 — Bleacher Nation, ClutchPoints, Yahoo, NBC, SI, Crescent City Sports, TalkBasket |

## Provenance and bounds

- Research channel: WebSearch summaries plus direct fetches where the
  environment allowed; Hoops Rumors, HoopsHype, ESPN story pages and several
  team blogs were blocked or empty. Every row edit rests on two or more
  independent outlets; the Murray correction rests on two primary data pages.
- Media day was still running at sweep time. Absence of an Ingram status is a
  timing fact, not a finding about his heel.
- Lines were not repriced for any traded or waived player: no source gave
  minutes to reprice against.
- Research effort: three delegated search passes (≈350 tool calls combined)
  plus ~10 of my own verification searches and fetches.
