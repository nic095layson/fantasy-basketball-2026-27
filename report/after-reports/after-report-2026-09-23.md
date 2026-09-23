# After-report — 2026-09-23 data pull + deck v27

**Owner request (2026-09-23, verbatim):** "Conduct fresh data pull, provide
after report and update tool."

Pull window: 2026-09-22 → 2026-09-23 (1 day). Gate: `check_provenance.py`
PASS — all rows sourced; verified 2026-07-13 .. 2026-09-22 (no kit row was
edited this pull, so the newest `verified_on` stays 9/22).

**Method.** Full F1–F6 sweep on the summary channel: 37 dated WebSearch
passes — the 7 flagged receipts, the six-team shadow set (CHI / DET / NOP /
NYK / POR / SAC), a ledger-shaped transaction query (Spotrac / ESPN), the
injury sweep diffed against the F6 tag inventory (10 excluded, 32 risk)
in both directions, the 9/22 watchlist (MEM cuts, Kawhi extension, Gueye,
camp bodies), the FA rows, and dedicated follow-ups on everything the
sweep surfaced (the Hawks–Hornets trade, Veesaar, Ingram, Adams, the
Rockets' media day). Four direct article fetches (Newsweek, ClutchPoints,
Yardbarker, TSN) were egress-blocked; every claim below rests on dated
search results with the outlets named in its row, two per claim. Kit edits:
none. Deck edits: four rows, applied by script with exact-match assertions;
every gate and suite re-run. This file passes `report/check_report.py` and
the deck's `judgment_open_items.py --check-report`.

## 1. Roster changes

| plane | change | count |
|---|---|---|
| deck | Buddy Hield ATL → CHA — the one trade of the window, announced by both teams Tuesday 9/22: Atlanta sent Hield, Ryan Nembhard and cash to Charlotte for Dorian Finney-Smith (ESPN, NBA.com, AP via ABC News, RealGM, Yahoo, HoopsHype, BVM); bench shooting role in Charlotte, line held | 1 |
| deck | Dorian Finney-Smith CHA → ATL — same trade (ESPN, NBA.com, RealGM, SI.com Hawks depth chart, RotoWire, CBS); competes for a reserve forward spot after rookie C Henri Veesaar's torn ACL, line held | 1 |
| deck | Steven Adams HOU — availability tag `ankle-recovery` (excluded, ×0.0) → `inj-ankle-risk` (×0.78): a full camp participant per Ime Udoka, on the podium at the Rockets' 9/22 media day ("good just to be back out there on the court") — Yahoo ("tracking well"), SI.com Rockets, Houston Chronicle media-day takeaways; F6 returner-vs-tag catch; team and line held (backup C) | 1 |
| deck | Brandon Ingram LAC — note only: heel status UNCLEAR per ESPN's Windhorst, no Clippers update on the May surgery, answer expected at media day 9/28 (Yahoo/ClutchPoints, heavy, Yardbarker, Newsweek); no multiplier, card held at −0.05 | 1 |
| kit | rows edited | 0 |
| both | lines changed on any row | 0 |
| neither | not a row on either plane: Ryan Nembhard (CHA, expected to be waived — Hoops Rumors, CBS, RotoWire, BVM 9/23); Henri Veesaar (ATL rookie C, torn right ACL 9/15, announced 9/21, out for the season — ESPN, Hoops Rumors, NBC, CBS); Exhibit 10 camp bodies below | — |

## 2. Flagged-item receipts (F1) — verdicts

| player | verdict | evidence (dated 2026-09-22 to 09-23) |
|---|---|---|
| Jalen Duren | HELD −0.08 | increasingly prepared to take the $9.6M qualifying offer and reach 2027 unrestricted free agency; sides about $5M a year apart on the five-year framework; Oct 1 deadline, camp 9/29 — Yahoo ×2, ESPN ("staring contest"), CBS Sports, Hoops Rumors (DET) |
| Jalen Brunson | HELD −0.05 | 80-85% after the July wrist surgery, no restrictions expected when camp opens 9/29 — Yahoo, heavy, nyknicksnews |
| Brandon Ingram | HELD −0.05; now an open item | heel status unclear — Windhorst: "we're gonna hear at media day"; Clippers camp in Hawaii 9/29–10/3 — Yahoo/ClutchPoints, heavy, Fadeaway World/Yardbarker, Newsweek |
| Cam Thomas | HELD FA | still unsigned with camps a week out — Yahoo ("From 40-Point Scorer to Free Agent"), SI.com Nets |
| Jaden Ivey | HELD FA | still unsigned since the March waiver — RotoWire, heavy; the "Lakers" Instagram post resurfaced in results and remains the logged fake (garble 7) |
| Jeremy Sochan | HELD −0.20 | Exhibit 9, non-guaranteed; SI.com Blazers lists him among three Blazers fighting for a job (with Krejčí and Cissoko); Rip City Project, KGW |
| Lonzo Ball | HELD FA | still an unrestricted free agent training on his own; no outlet carries a signing — Yahoo, heavy |
| Bennedict Mathurin | HELD −0.05; checkpoint stands | bench scoring punch behind the Murphy / Zion wing room — SI.com Pelicans, Yahoo |

## 3. Window sweep, team shadows, injury sweep

**Ledger-shaped query (Spotrac / ESPN transactions, 9/22):** the
Hawks–Hornets trade (§1); Pelle Larsson's 4yr/$60M rookie-scale extension
made official by Miami (Yahoo, NBA.com, Hoops Rumors, HoopsHype — his deck
note already carried it); Miami claimed Bez Mbeng off waivers; New Orleans
waived Solomon Washington; Exhibit 10s in Denver (Reese Dixon-Waters, Keonte
Jones), Detroit (Drake Allen; Jordan Riley per Hoops Rumors), Minnesota
(Jalen Crutcher), Charlotte (Tre Carroll) and Portland (Mark Armstrong,
Keylan Boone, Samson — Blazer's Edge). One trade in a one-day window; the
F5 zero-trade rule is satisfied by the finding itself and the ledger is
cited regardless.

**Kawhi Leonard:** the 9/22 watch item closed — a two-year / $115M
extension with Toronto agreed 9/22, 2028-29 player option, $11M under his
max (Shams/ESPN via TSN; AP via Washington Times, US News, Japan Times;
Yahoo, NBC Sports). Row and card unchanged: the card prices integration,
not contract.

**Team shadows (one query each):** CHI — season-preview coverage only;
DET — Riley camp contract 9/22, Duren "$5M annually" apart (Hoops Rumors),
Ausar Thompson and Reed already recorded; NOP — rotation-crunch previews,
nothing on a row; NYK — second-rounder Tyler Nickel still unsigned (Posting
and Toasting), no row; POR — the three Exhibit 10s, Sharpe out most of the
season (consistent with his knee-recovery tag); SAC — quiet, Achiuwa already
a SAC row. ATL and CHA were not in the watch set; the trade was caught by
the ledger query, which is the F3 design working as intended.

**MEM cut-down:** still reported-not-executed — eighth pull. No dated
9/22–9/23 item surfaced; every result (Yahoo, SI.com Grizzlies, HoopsHype)
predates the window. Hawkins and DLo rows hold.

**Injury sweep vs the F6 inventory, both directions.** Excluded-but-now-
cleared: **Steven Adams — caught.** His deck row had carried
`ankle-recovery (out indefinitely)` since the January surgery; the Rockets'
9/22 media day put him on the podium and Udoka named him a full camp
participant. Retagged to the first-season-back risk class (Kessler / Edey
convention), so he is draftable again on the deck. He is not a kit row.
Returning-but-untagged: none new — VanVleet is "full go" for camp but not
100% (already `inj-acl-risk`); Nikola Topić ready for camp after June back
surgery (not a row on either plane); Alex Sarr's fractured right foot is the
June surgery his tag already names; Gueye's 3–4-month re-evaluation from
the mid-July surgery matches "misses camp, preseason and the start";
Sharpe consistent. Ingram is the one genuine unknown (note + open item).

**Garble log:** no new instance. The Ivey "Lakers" Instagram post
resurfaced in search results and stays logged as instance 7.

**Rockets media day (9/22)** was the first of the season (HOU and DAL early
for the China games; the other 28 teams on 9/28). It produced the Adams
catch. The next pull lands on the league-wide media day: expect the
densest injury-status day of the preseason and widen the F6 sweep
accordingly.

## 4. Board effects (computed, never eyeballed)

**Kit:** zero row edits. `rank_engine.py` re-run; the board content is
byte-identical to the 9/22 board — the only diff is the generation-date
line. Top 12 unchanged.

**Deck:** scripted diff of the ranked board between HEAD's pool and the
edited pool — draftable set 320 → 321 (Adams enters at 284 of 321 with an
adjusted value of −5.51, a backup center behind Şengün); top-200 entries 0,
exits 0, moves ≥3 ranks 0, maximum value delta among incumbents 0.000
(Adams sits far outside the top-156 z-score base, so no incumbent's z
moved). Hield (245) and Finney-Smith (249) keep their ranks; only the team
label changed. Pool hash c6d6b4fc → 4d0f202f.

## 5. Deck build and publish

| build | what | record |
|---|---|---|
| v27 | 9/23 pull: two placements moved (Hield, Finney-Smith), Adams retagged from excluded to risk, Ingram note, JUDGMENT re-authored and dated 2026-09-23 (8 open items incl. Ingram), colophon rewritten for this window; Yahoo 9/22 prices re-baked at one day old (296 of 330) | deck PR #44 merged (a5b2c91); published to the standing artifact URL as Version 27, byte-identical to deck main (md5 2629781b) |

## 6. Gates (2026-09-23)

| gate | result |
|---|---|
| kit `check_provenance.py` | PASS — 318/318 sourced |
| kit `check_report.py` + deck `judgment_open_items.py --check-report` | PASS on this file |
| deck `verify_rosters.py` | 330/330 checked, 0 unmatched, 0 mismatches, evidence dated 2026-09-23 (fallback-partial) |
| deck `hoops.py freshness --stamp` | stamped 2026-09-23, pool_changes asserted (2 placements, 1 retag, 1 note) |
| deck build gates 1–7 + F8 | green — planes 308 shared / kit-only 10 / deck-only 22 / 0 team / 0 exclusion / 0 drift / 0 propagation; market yahoo-2026-09-22.csv 296/330 priced, 1 day old; injection round-trip OK; "safe to publish" |
| deck `test_gates` / `test_card` / `test_draft` / `check_parity` | 34/34 · 35/35 · 57/57 · EXACT (330 rows, 2970 z cells, 130 owner turns across 10 committed states; survival probs bit-identical, clock reads field-identical) |
| deck `check_planes.py --kit` standalone | 308 shared · kit-only 10 · deck-only 22 · 0 team / 0 exclusion / 0 drift / 0 propagation |

## 7. Watchlist / open items

- **Ingram (LAC)** — media day 9/28 is the tell. If he opens camp limited,
  the deck row takes a heel risk tag (×0.78) and the kit GP (64) comes
  down; if full-go, the card clears to zero as written on 9/15.
- **Duren** — Oct 1 QO deadline, camp 9/29; widen the card if he sits.
- **Adams** — first camp reps; the line (6.5 / 8.5 on 4.5 FGA) is the
  backup-center shape and was not repriced. Re-check after the first
  preseason game.
- **Nembhard** — CHA waiver expected; no row. **Veesaar** — no row; his
  absence is why Finney-Smith has a rotation path in Atlanta.
- **League-wide media day 9/28** — the next pull should treat every
  risk-tagged and excluded row as due for a status check (F6 widened).
- **MEM cuts** — eighth pull reported-not-executed; Hawkins and DLo rows.
- **Cam Thomas / Ivey / Lonzo** — unsigned; a signing repriced on the day.
- **Camp bodies** — Sochan, Krejčí (POR); Bruce Brown, Konchar (NYK):
  non-guaranteed; a cut returns each to FA with no line.
- **Survival chips (D53-2)**, **Tatum at #10 (D53-3)**, **resolver
  dot-folding (D53-4)** — owner decisions carried from the mock-53 report.
- **Whitmore** — kit GP 30 on a two-way; no deck row.
- **Yahoo team labels** — Westbrook (SAC) and Valančiūnas (DEN) stale on
  Yahoo's page; the researched status stands on both planes.

## 8. Open-item receipts

| player | query run (2026-09-23) | dated finding |
|---|---|---|
| Jalen Duren | Jalen Duren Pistons contract qualifying offer September 23 2026 · Detroit Pistons news September 23 2026 | increasingly prepared to take the $9.6M QO; ~$5M/yr apart; Oct 1 — Yahoo ×2, ESPN, CBS, Hoops Rumors |
| Jalen Brunson | Jalen Brunson Knicks wrist training camp September 23 2026 | 80-85%, no restrictions for camp 9/29 — Yahoo, heavy, nyknicksnews |
| Brandon Ingram | Brandon Ingram heel injury update Clippers September 2026 · Brandon Ingram heel Windhorst media day Clippers Hawaii camp | status unclear; update at media day 9/28 — Yahoo/ClutchPoints, heavy, Fadeaway World, Yardbarker, Newsweek (article dates not fetchable — egress; dated to the camp-eve week by the media-day framing and absence from the 9/22 sweep) |
| Cam Thomas | Cam Thomas free agent signs September 23 2026 · Cam Thomas unsigned free agent training camp Nets September 2026 | still unsigned — Yahoo, SI.com Nets |
| Jaden Ivey | Jaden Ivey free agent signs September 23 2026 · Jaden Ivey still unsigned September 22 2026 | still unsigned — RotoWire, heavy; Lakers post = logged fake |
| Jeremy Sochan | Jeremy Sochan Trail Blazers roster training camp September 23 2026 | Exhibit 9 camp battle, non-guaranteed — SI.com Blazers, Rip City Project, KGW |
| Lonzo Ball | Lonzo Ball free agent signs September 2026 · Lonzo Ball unsigned September 22 2026 training camp | still unsigned — Yahoo, heavy |
| Bennedict Mathurin | Bennedict Mathurin Pelicans rotation role September 23 2026 | bench scoring punch; line holds — SI.com Pelicans, Yahoo |
| (window sweep) | NBA transactions September 23 2026 signed waived traded · NBA trade September 22 2026 · NBA news September 23 2026 | Hawks–Hornets trade; Larsson extension official; Mbeng claim; Exhibit 10s — Spotrac, ESPN, NBA.com |
| (trade) | Hornets trade Dorian Finney-Smith Hawks Buddy Hield Ryan Nembhard · HoopsRumors September 22 2026 trade Hawks Hornets Finney-Smith · Atlanta Hawks news September 23 2026 Finney-Smith role · Charlotte Hornets Buddy Hield role Nembhard waived September 23 2026 | both teams announced 9/22; roles as in §1; Nembhard waiver expected — ESPN, NBA.com, AP, RealGM, SI.com, HoopsHype, BVM, RotoWire, CBS, Hoops Rumors |
| (injury sweep) | NBA injury news September 23 2026 surgery out training camp · Rockets media day September 22 2026 Steven Adams Fred VanVleet injury update · Steven Adams ankle status training camp 2026-27 Rockets media day cleared · Steven Adams ankle surgery January 2026 return timeline · Alex Sarr fractured right foot surgery · Nikola Topic lumbar microdiscectomy · Henri Veesaar torn ACL · Mouhamed Gueye foot injury timeline | Adams cleared (retagged); VanVleet full go, tagged; Sarr/Gueye/Sharpe consistent; Topić and Veesaar not rows — Yahoo, SI.com, Houston Chronicle, ESPN, NBA.com, Hoops Rumors, CBS, RotoWire |
| (CHI/DET/NOP/NYK/POR/SAC) | team-shaped news queries, one each | consistent with the pools; DET Riley camp deal; POR Exhibit 10s — Hoops Rumors, Blazer's Edge, Yahoo, SI.com |
| (MEM shadow) | Grizzlies waive Jordan Hawkins D'Angelo Russell roster cuts September 23 2026 · Grizzlies roster waive September 23 2026 Russell Clayton Hawkins Murray | reported-not-executed, nothing dated in window — Yahoo, SI.com, HoopsHype |
| (Kawhi) | Kawhi Leonard Raptors extension September 23 2026 | 2yr/$115M agreed 9/22, player option 2028-29 — TSN, AP (Washington Times / US News / Japan Times), Yahoo, NBC |
| (Larsson) | Pelle Larsson Heat rookie scale extension September 22 2026 | official 9/22; note already carried — Yahoo, NBA.com, Hoops Rumors, HoopsHype |

## Provenance and bounds

- Research channel: WebSearch summaries only; four direct fetches
  egress-blocked (Newsweek, ClutchPoints, Yardbarker, TSN). Every claim is
  dated and carries the outlets named in its row; the one date not directly
  verified is the Ingram item's article date (stated in its receipt).
- The Adams retag is a classification change, not a reprice: his line was
  never touched and he ranks 284th. The catch matters for the resolver and
  the live room (he can now be logged as a draftable pick) more than for
  the card.
- The Hield / Finney-Smith lines are held on bench roles at both ends; no
  source gave minutes to reprice against.
- Not verified by direct fetch: any roster page (egress policy). The
  evidence ledger remains fallback-partial.
