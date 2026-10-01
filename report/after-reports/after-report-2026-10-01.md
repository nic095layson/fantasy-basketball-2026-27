# After-report — 2026-10-01 data pull + deck v37

**Owner request (2026-10-01, verbatim):** "Good morning Claude, please conduct
daily pull and provide after report of findings."

Pull window: 2026-09-30 → 2026-10-01 (1 day: day three of training camps; the
qualifying-offer deadline). Gate: `check_provenance.py` → `PROVENANCE GATE:
PASS — all rows sourced; verified 2026-07-13 .. 2026-09-30`, exit 0.

**Method.** One search sweep of 41 dated queries: the ledger-shaped
transaction check (Spotrac, ESPN transactions, RealGM, Hoops Rumors), a
dedicated query for each of the eleven flagged receipts, one team-shaped
query for each of the eight teams in the watch set (CHI, DET, GSW, LAC, MIL,
NOP, POR, TOR), the injury sweep against the 43-row tag inventory, the free
agents, and the four items carried from yesterday's sheets (Morant's games,
Alexander-Walker's role, VanVleet's clearance, the Porter row). Direct fetches:
Basketball-Reference's game logs for Morant and Alexander-Walker and NBA.com's
Hawks season preview (open); Hoops Rumors blocked on three tries, so its items
rest on dated search summaries. New this pull: ESPN's public roster API
(`site.api.espn.com`) answered the deck's verifier for the first time, so
roster verification ran in **direct-complete** mode against all 30 live
rosters instead of the pull-authored fallback file. Edits applied by script
with exact-match assertions (`scratchpad pull1001/kit_edit.py`,
`deck_edit.py`, `deck_edit2.py`, `judgment_colophon.py`); both boards diffed
by script against the pre-pull snapshots; the deck built through gates 1–7/F8
and driven end to end by the step-5b browser gate.

**Headline.** No trades and no window signing on a pool row, but the live
roster check caught a placement the fallback evidence had carried wrong for
three months: Gabe Vincent is on none of ESPN's 30 rosters and has been an
unsigned free agent since his contract expired on June 30 — his deck row moves
Atlanta → FA. Two carried decisions landed: Ja Morant's deck row now carries
the risk tier on his 20-of-82 2025-26 (the kit's 60-game line already priced
him, and his kit rank is insensitive to the number because his composite is
negative), and Nickeil Alexander-Walker's line was re-derived on both planes
to his 20.8-point Most Improved Player season at 31 minutes now that two
outlets name him Atlanta's starter — kit 103 → 52, deck 68 → 56. Duren is
unsigned on deadline day; the qualifying-offer decision lands tonight and
resolves his card either way at the next pull. Every other flagged item held.
Deck v37 built and published.

## 1. Roster changes

| plane | change | count |
|---|---|---|
| deck | Gabe Vincent ATL → FA — on none of ESPN's 30 live rosters (605 names; `site.api.espn.com`, direct check 2026-10-01); unsigned since his contract expired 2026-06-30, turned down a Knicks camp offer while waiting for a guaranteed deal (Yahoo, Heavy, Soaring Down South; Spotrac free-agent list). The pool had carried him on ATL since the February trade; not a kit row | 1 |
| both | Nickeil Alexander-Walker line re-derived (D-30-2) — starting shooting guard per NBA.com's season preview (Zillgitt, 9/22: McCollum, Alexander-Walker, Daniels, Johnson, Okongwu) and SI Hawks' projected lineup; 2025-26 Basketball-Reference game-log totals 78 GP, 33.3 mpg, 20.8 pts, 3.2 3PM, 3.4 reb, 3.7 ast, 1.3 stl, 0.5 blk, 2.1 tov, .459 FG on 15.3 FGA, .902 FT on 3.9 FTA; set at 31 minutes with a share haircut for McCollum, Dort and Wiggins (×0.885): 18.4 / 3.0 / 3.3 / 1.2 / 0.5 / 2.8 3PM, .455 / .890. [LIKELY] direction, [SPECULATIVE] magnitude; kit GP 72 held. The planes had carried different lines (deck 19.5 pts, kit 14.5) since the baseline | 1 |
| deck | Ja Morant availability tag `inj-risk` (D58-1) — 20 of 82 games in 2025-26 (calf, elbow, a suspension; 19.5 / 3.3 / 8.1 in 28.4 mpg — Basketball-Reference game log), 79 appearances over the last three seasons (Hoops Rumors Trail Blazers Notes, SI Blazers); says he hopes to play every game; day-two practice 10/1 (Blazer's Edge). Adjusted value unchanged — the multiplier never shrinks a negative composite — but the weekly model now expects 0.75 × games instead of 0.88 ×, which is the term the card's ΔECW blends on | 1 |
| deck | Notes only, no tier change: VanVleet (D-BV2), Kevin Porter Jr (D-30-1 closed, see §3), Duren, Rollins, Anthony Black, Curry, Knueppel, Embiid, Jamal Shead — the status refreshes in §2 and §4 | 9 |

Two-source rule: every row edit above carries at least two outlets; the
Vincent move three plus the direct roster feed; every note edit two.

## 2. Flagged-item receipts (F1) — verdicts

- **Duren — HELD −0.08; deadline day.** Unsigned at run time, left off
  Detroit's 20-man camp roster, the fully guaranteed 5yr/$200M offer reported
  rejected; the $9.6M qualifying-offer decision is due 11:59 pm ET tonight
  (NBC Sports, Yahoo, Hoops Rumors 9/30–10/1). Stein's 9/29 read — he accepts
  absent a deal — stands. Either branch resolves the card tomorrow.
- **Ingram — HELD −0.15.** No new item: out for the 10/21 opener, week-by-week,
  limited camp involvement (ESPN, SI Clippers depth chart, The Sporting
  Tribune). Tag unchanged.
- **Porziņģis — HELD −0.10, veto unchanged.** Out at the Hawaii camp, no
  timeline (Yardbarker 9/30, SF Chronicle); re-check after the 10/4 opener.
- **Kawhi — HELD −0.05.** Through the second camp practice on the planned
  ramp-up, drills without live contact, confirmed by him (HoopsHype 9/29,
  Yahoo 9/30).
- **Cam Thomas, Ivey, Lonzo Ball — HELD, all unsigned** (Spotrac, RotoWire,
  Hoops Wire list; Yahoo 9/30 on Lonzo: a month from tip-off, no indication
  of a change). The "Bucks sign Cam Thomas" items are the February 2026 deal.
- **Dillingham — HELD −0.10.** Unrestricted free agent, eligible for any team
  but Chicago (Hoops Rumors, Spotrac).
- **Sochan — HELD −0.2.** The Sochan–Cissoko battle for the backup-small-forward
  minutes is still the camp storyline (Yahoo, Rip City Project).
- **Mathurin — HELD −0.05.** Presumptive sixth man behind Herb Jones in a bench
  unit with Bey, Fears and Queen (SI Pelicans, FanSided/Yahoo).
- **Rollins — HELD −0.05.** Undecided; listed first on the camp depth chart
  (RealGM) while SI Bucks runs the starter debate. The "Doc Rivers names
  Porter starter" item that surfaced is the 2025 camp.

## 3. The carried items

| item | finding (dated) | outlets | action |
|---|---|---|---|
| D58-1 Morant deck tag | 20 GP in 2025-26, 79 in three seasons; healthy at camp | B-Ref game log (direct); Hoops Rumors; SI Blazers; Blazer's Edge 10/1 | **tag added** (§1). Kit 60 GP held: scratch engine runs at 60, 50 and 40 games all leave him at kit rank 139 (negative composite), so the number is cosmetic there — D-1001-1 |
| D-30-2 Alexander-Walker | projected starter, two independent outlets; 2025-26 line fetched | NBA.com preview 9/22; SI Hawks; B-Ref (direct) | **line re-derived both planes** (§1). SI Hawks' position-battle piece says Dort could take the spot — watchlist |
| D-BV2 VanVleet | fully cleared, scrimmaging five-on-five for weeks, practiced Wednesday; no back-to-backs to open the season, minutes limit set by camp progress per Udoka | CBS Sports; The Dream Shake; Yahoo; RotoWire | note appended; tag `inj-acl-risk` and line unchanged (kit 75 / deck 69) |
| D-30-1 Porter deck row | **the premise was wrong**: the deck has carried `Kevin Porter Jr.` since the baseline commit (`git log -S`), under the dotted spelling the planes gate folds (314 shared); yesterday's role pass searched the undotted kit spelling and reported "no deck row exists" | repo history | correction recorded; a role note added (the Rollins battle — SI Bucks, Yahoo); decision closed |

## 4. Window sweep, team shadows, injury sweep

- **Transactions (F5 ledger check).** Spotrac, ESPN transactions, RealGM and
  Hoops Rumors via search: zero trades in the window. The ledger summary's
  "Timberwolves trade Josh Green to Utah for Cody Williams and Konchar" is
  the 2026-08-29 deal (Star Tribune, ESPN, Deseret, Hoops Rumors all date it
  there) — garble logged, no row involved. Window moves, none a pool row:
  the Bulls waived Marquel Sutton and signed Jalen Bridges, the Nuggets
  signed Ryan Nembhard to a two-way deal, the Heat signed Lester Quinones
  (Exhibit 10), the Thunder waived Mason Plumlee (Hoops Rumors, Spotrac).
  Jamal Shead agreed a three-year, $24M extension 10/1 (ESPN/Shams, TSN, NBC
  Sports) — contract only, note added. The MEM cut-down (Clayton, Hawkins,
  Kris Murray) is still reported-not-executed (SI Grizzlies, TalkBasket) —
  eleventh pull.
- **Roster verification went direct.** ESPN's public roster JSON answered
  the deck's `verify_rosters.py` for the first time (every prior pull: 403,
  fallback-partial). All 30 rosters, 605 names, zero mismatches on the 331 of
  334 pool rows it could match by name. The three unmatched were each
  verified by hand: Jimmy Butler is `Jimmy Butler III` on ESPN's Warriors
  list and Ron Holland is `Ronald Holland II` on Detroit's (the verifier's
  name fold keeps generational suffixes), and Tony Bradley's 9/30 camp deal
  (RealGM, Hoops Wire, BVM) is not yet on ESPN's Knicks feed — exemptions
  recorded in the verification artifact and the freshness note. The one true
  absence was Vincent (§1). The same scan confirms every FA row: Konchar,
  Dillingham, Cam Thomas, Ivey, Lonzo, Broome and Westbrook are on no roster.
- **Team shadows.** CHI (Sutton waived, Bridges added; Giddey a full
  participant — CBS, SI Bulls), DET (Duren — above; Holland on the camp
  roster — Yahoo, RealGM), GSW (Hawaii camp; Curry "knee feeling great" with
  select back-to-backs off — NBC Sports Bay Area, Heavy; Porziņģis out), LAC
  (Beal's knee inflammation keeps him out of the camp start — RotoBaller,
  HoopsHype, SI Clippers; Ingram above), MIL (camp under Jenkins; the Rollins
  battle; the Gary Trent Jr. contract investigation still open — Yahoo, SI
  Bucks), NOP (21-man camp roster, full health per Dumars — WWL, Yahoo;
  Mathurin above), POR (day two 10/1: Morant's catch-and-shoot work, Clingan
  the starting center — Blazer's Edge; Sochan above), TOR (Shead extension;
  Kawhi above).
- **Injury sweep vs the F6 tag inventory (43 tagged rows).** Cleared or
  progressing, tags kept by convention: Embiid (full participant at the
  opening practice, no restrictions per Nurse — NBC Sports Philadelphia,
  Heavy, SI 76ers), Curry (above), Jaren Jackson Jr. (Deseret 9/28:
  recovered from the PVNS removal, fully healthy — single dated outlet, note
  not changed), VanVleet (above), Edey (cleared for full-speed work, on pace
  for 10/21, no two-a-days — NBC Sports, SI Grizzlies), Kessler and Paul
  George (no new item). Still out, tags kept: Butler (`acl-recovery`,
  January–February "optimistic", individual work only — Yahoo, Heavy, NBC
  Sports Bay Area; D-BV1 unchanged), Moody, Porziņģis, Lively (`risk`, not
  cleared, opener undetermined — Mavs Moneyball/ESPN, CBS), Mark Williams,
  Ingram, Shaedon Sharpe (about six months — SI Blazers media day). New
  minor: Anthony Black, a minor ankle sprain from the voluntary workouts,
  day-to-day, limited at camp (Sweeney via HoopsHype 9/30, SI Magic,
  RotoBaller) — note, no tag; Knueppel's hamstring pain is gone, no
  five-on-five yet, re-evaluation the week of 10/19 (Yahoo, NBC Sports) —
  note refreshed. Returning-but-untagged: none found (Giddey and Brunson
  cleared, neither tagged, both already noted). The "76ers' Embiid and Paul
  George both sidelined" item is the 2025 camp — garble logged.
- **FA rows.** Kit: Cam Thomas, Ivey, Dillingham, Broome, Konchar unsigned.
  Deck adds Lonzo, Vincent (new) and the retired/overseas rows.

## 5. Board effects (computed, never eyeballed)

- **Kit.** `top-200-2026-27.md` regenerated against the pre-pull snapshot:
  Nickeil Alexander-Walker 103 → 52; one entry (Khaman Maluach, 199) for
  one exit (Isaiah Joe, 199); the re-standardized pool displaces Jrue
  Holiday 91 → 94 and Dereck Lively 118 → 114; 98 further displacements of
  one or two places (Amen Thompson 30 → 28 the largest upward, Ty Jerome
  49 → 51 downward). Top 12 unchanged.
- **Deck.** By adjusted value over the draftable rows (324 → 324): no
  entries or exits; Alexander-Walker 68 → 56 (adjusted value −0.19 → +0.20);
  Morant 66 → 68 by displacement only (value −0.18 → −0.19 from the
  re-standardization; the new tag does not shrink a negative composite);
  VanVleet 69, Porter 155, Duren 64 → 65. Vincent's value is unchanged by the
  team label. Pool sha256 `09fe6d433264` (was `bdb40833a6ac`).
- **Both planes on the same name.** Alexander-Walker moves together; Morant
  moves on the deck's weekly model only, by design (the kit's 60 games
  already priced him).

## 6. Deck build and publish

`build_deck.py` on 2026-10-01: roster verification **direct-complete**,
331/334 against all 30 official rosters, 0 mismatches, 3 unmatched exemptions
by name (§4); freshness stamped with the pool-changes note; JUDGMENT re-dated
2026-10-01 — eleven open cards re-authored with today's receipts, none added
or removed, all eleven still flagged by the enumerator after re-authoring;
colophon Data paragraph rewritten for the window (gate 6 refused the first
draft over the phrase "330 rows" and the paragraph was re-phrased — the gate
working as designed); planes 314 shared, team 0, exclusion 0, drift 0,
propagation 0, **no waivers**; market `yahoo-2026-09-22.csv`, 296 of 334
priced, 9 days old (warning threshold 14). "safe to publish". Published to the
standing artifact URL as version 37; served bytes read back and matched.

**Harness finding (the day ESPN answered).** The deck's gate suite
(`test_gates.py`) went red twice before it went green, both times because of
the new direct mode, never because of the page: its first run died priming
on the three suffix-form rows the live feed cannot match (the suite's
docstring assumed ESPN blocked, so its cases mutate the evidence file to make
the gates fire — a file the live feed ignores); its second run died on a TLS
handshake timeout inside the verifier's per-team loop, which escaped as a
traceback because only the first fetch was guarded. Two fixes, both
red-first with the failing runs as the red (`scratchpad pull1001/
test_gates.log`, `test_gates_run2.log`, `red_midloop.py`): the suite now pins
itself to the evidence-file mode through `HOOPS_VERIFY_OFFLINE`, honored by
`verify_rosters.py` with a stderr line saying so, and the verifier's per-team
fetch retries three times with backoff and then reports and falls back
instead of crashing (the scratch case raised `TimeoutError` before the fix
and returned the reported fallback after it). Third run: all 34 cases passed,
offline. The real pull's verification stays direct-complete; the offline
check I ran in the real checkout rewrote the verification artifact with the
fallback result, so the direct run was repeated (direct-complete, 331/334, 3
exempted) and a rebuild attempted — gate 4 refused it because the pool is
byte-identical to the build already recorded, and the page on disk is that
build's output: sha `502eaf2d8797e457`, the same as the staged copy, its
manifest reading direct-complete 331/334.

## 7. Gates (2026-10-01)

| gate | result (evidence: the command's own output line) |
|---|---|
| kit `check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-09-30 |
| kit `check_derived.py` | all 11 dated artifacts reproduce byte-for-byte |
| kit `check_report.py` on this file | REPORT GATE: PASS (structure, publication rule, pull-log row) |
| deck `judgment_open_items.py --check-report` on this file | receipts check PASS — all 11 flagged names carry a receipts row |
| deck `verify_rosters.py` | direct-complete via site.api.espn.com (all 30 rosters): 331/334 checked, 0 mismatches, 3 unmatched exempted by name |
| deck `check_planes.py` (in the build) | 314 shared · team 0 · exclusion 0 · drift 0 · propagation 0 (no waivers) |
| deck `build_deck.py` | all gates pass; safe to publish (pool `09fe6d433264`) |
| deck `check_parity.py` on the built page | PARITY: EXACT MATCH |
| deck `test_gates.py` / `test_draft.py` / `test_card.py` | all 34 cases passed (third run, suite pinned offline — §6) / all 62 cases passed / CARD: all 68 cases passed |
| deck step-5b `full_dom_check.mjs` on the built page | 128 assertions, 0 failed, 0 page errors, exit 0 (`arena/results/full_dom_check_2026-10-01_v37.json`) |

## 8. Watchlist / open items

- **Duren** — the qualifying-offer decision is due 11:59 pm ET tonight; the
  10/2 pull applies whichever branch lands (QO: card cleared, de facto
  no-trade clause, unrestricted in 2027; long-term deal: card cleared).
- **Rollins vs Porter** — Milwaukee's starter call; the −0.05 clears when it
  is named; both rows now carry the battle.
- **Alexander-Walker vs Dort** — SI Hawks' position-battle piece names Dort
  as the alternative at the fifth spot; a Dort start in preseason would trim
  the new line.
- **Anthony Black** — day-to-day ankle; a tag only if he misses preseason.
- **Knueppel** — re-evaluation the week of 10/19; the 10/21 opener undecided.
- **Ingram, Porziņģis, Lively, Beal** — the first preseason week (the Hawaii
  game 10/4 for the Warriors and Clippers).
- **Vincent** — a signing reprices the row that day (Konchar precedent: no
  judgment card for a deep-bench free agent).
- **MEM cut-down** — eleventh pull unexecuted.
- **Yahoo market paste** — nine days old; the build warns at 14. Early October.
- **Owner decisions carried:** D-BV1 (Butler), D-30-3/D-30-4, D58-2..D58-5,
  D-R1..D-R4, D-G2..D-G7, D-P1..D-P4; D-30-1, D-30-2, D-BV2 and D58-1 closed
  today.

## Open-item receipts

| player | query run | dated finding |
|---|---|---|
| Jalen Duren | Jalen Duren Pistons qualifying offer deadline decision October 1 2026 · Detroit Pistons news October 1 2026 Duren Cunningham training camp | unsigned on deadline day, off the camp roster, decision due 11:59 pm ET — NBC Sports, Yahoo, Hoops Rumors 9/30–10/1 |
| Brandon Ingram | Brandon Ingram Clippers Achilles update October 1 2026 · Los Angeles Clippers training camp news October 1 2026 Beal Ingram | out for the 10/21 opener, week-by-week — ESPN, SI Clippers, The Sporting Tribune |
| Kristaps Porzingis | Kristaps Porzingis Warriors update October 1 2026 · Golden State Warriors Hawaii training camp news October 1 2026 | out at the Hawaii camp, no timeline — Yardbarker 9/30, SF Chronicle, Golden State of Mind |
| Kawhi Leonard | Kawhi Leonard Raptors training camp practice October 1 2026 · Toronto Raptors training camp news October 1 2026 | ramp-up through the second practice, no live contact — HoopsHype 9/29, Yahoo 9/30 |
| Cam Thomas | Cam Thomas free agent signs October 1 2026 | unsigned; the Bucks items are the February 2026 deal — Spotrac, ESPN, NBC Sports |
| Jaden Ivey | Jaden Ivey free agent signs team October 2026 | unsigned — Spotrac, RotoWire |
| Jeremy Sochan | Jeremy Sochan Trail Blazers camp roster battle October 1 2026 | the Sochan–Cissoko backup-SF battle — Yahoo, Rip City Project |
| Lonzo Ball | Lonzo Ball OR Rob Dillingham free agent signs October 1 2026 | unsigned, a month from tip-off — Yahoo 9/30, Hoops Wire FA list |
| Rob Dillingham | (same query) | unrestricted free agent, any team but Chicago — Hoops Rumors, Spotrac |
| Bennedict Mathurin | Bennedict Mathurin Pelicans training camp rotation October 1 2026 · New Orleans Pelicans training camp news October 1 2026 | presumptive sixth man behind Herb Jones — SI Pelicans, FanSided/Yahoo |
| Ryan Rollins | Bucks training camp starting point guard Ryan Rollins Kevin Porter Jr October 1 2026 · Milwaukee Bucks training camp news October 1 2026 | undecided; listed first on the camp depth chart (RealGM), debate live (SI Bucks); the Rivers item is 2025 |
| Ja Morant | Ja Morant games played 2025-26 season injuries Trail Blazers training camp October 2026 · basketball-reference.com game log 2026 (fetched) · Portland Trail Blazers training camp news October 1 2026 | 20 GP (B-Ref); 79 in three seasons (Hoops Rumors, SI Blazers); day-two practice 10/1 (Blazer's Edge) |
| Nickeil Alexander-Walker | Nickeil Alexander-Walker Hawks training camp starting lineup October 2026 · nba.com 2026-27 season preview ATL (fetched) · basketball-reference.com game log 2026 (fetched) | projected starter — NBA.com (Zillgitt 9/22), SI Hawks; Dort the alternative (SI Hawks); 2025-26 line from B-Ref totals |
| Fred VanVleet | Fred VanVleet Rockets practice scrimmage status October 1 2026 | cleared, scrimmaging, practiced Wednesday; no back-to-backs to open — CBS Sports, The Dream Shake, Yahoo, RotoWire |
| Gabe Vincent | Gabe Vincent Hawks roster status waived OR traded September 2026 · Gabe Vincent free agent signs 2026 unsigned guard October · ESPN roster API, 30 teams (fetched) · basketball-reference.com ATL 2026-27 transactions (fetched) | on no ESPN roster; unsigned since 6/30, turned down a Knicks camp offer — Yahoo, Heavy, Soaring Down South, Spotrac |
| Tony Bradley | ESPN roster API NYK (fetched) | not on ESPN's Knicks feed; camp deal 9/30 stands — RealGM, Hoops Wire, BVM |
| Ron Holland | Ron Holland Pistons training camp 2026 roster · ESPN roster API DET (fetched) | `Ronald Holland II` on Detroit's roster — ESPN API, Yahoo, RealGM |
| Jimmy Butler | Jimmy Butler Warriors return timeline update October 1 2026 · ESPN roster API GSW (fetched) | `Jimmy Butler III` on the Warriors' roster — ESPN API; January–February optimistic, individual work — Yahoo, Heavy, NBC Sports Bay Area |
| Dereck Lively | Dereck Lively Mavericks cleared training camp October 1 2026 | not cleared, opener undetermined — Mavs Moneyball/ESPN, CBS |
| Zach Edey | Zach Edey Grizzlies practice status October 1 2026 | cleared for full-speed work, on pace for 10/21 — NBC Sports 9/29, SI Grizzlies |
| Kon Knueppel | Kon Knueppel hamstring Hornets training camp update October 2026 | pain gone, re-evaluation the week of 10/19 — Yahoo, NBC Sports |
| Stephen Curry | Stephen Curry injury update training camp Hawaii October 2026 | knee "feeling great", select back-to-backs off — NBC Sports Bay Area, Heavy, Yahoo |
| Anthony Black | Anthony Black ankle sprain Magic training camp October 2026 | minor ankle sprain, day-to-day — HoopsHype 9/30, SI Magic, RotoBaller |
| Bradley Beal | Bradley Beal knee Clippers training camp status October 2026 | knee inflammation, misses the camp start — RotoBaller, HoopsHype, SI Clippers |
| Joel Embiid | Joel Embiid 76ers training camp practice status September 30 2026 | full participant at the opening practice — NBC Sports Philadelphia, Heavy, SI 76ers |
| Jaren Jackson Jr. | Jaren Jackson Jr. Jazz training camp practice knee September 30 2026 | recovered from the PVNS removal, fully healthy — Deseret 9/28 [SINGLE-SOURCE]; note unchanged |
| Jamal Shead | Jamal Shead Raptors extension three-year $24 million October 1 2026 | extension agreed 10/1 — ESPN/Shams, TSN, NBC Sports |
| (window ledger) | NBA transactions October 1 2026 signed waived traded · NBA trade September 30 OR October 1 2026 · Josh Green Jazz Timberwolves trade Cody Williams Konchar | zero trades; the Green deal is 8/29 — Star Tribune, ESPN, Deseret, Hoops Rumors; window moves touch no pool row — Hoops Rumors, Spotrac |
| (injury sweep) | NBA training camp injury news October 1 2026 · "cleared" OR "full participant" returns training camp practice first time since surgery NBA October 1 2026 · NBA players returning from injury limited training camp October 1 2026 Embiid Paul George Jaren Jackson | §4 — Hoops Rumors injury updates, ESPN, CBS, Yahoo |
| (MEM cut-down) | Grizzlies waive Jordan Hawkins OR Kris Murray OR Walter Clayton roster cut October 2026 | still reported-not-executed — SI Grizzlies, TalkBasket |
| (team watch, 8) | "<Team> training camp news October 1 2026" one each: CHI, DET, GSW, LAC, MIL, NOP, POR, TOR | §4 |
| (Johni Broome) | Johni Broome signs October 2026 | unsigned — Hoops Rumors, Spotrac |

## Bounds

- Direct-complete roster verification proves membership, not role; the three
  exempted rows were verified by hand (name forms on ESPN's own lists, and
  three outlets for Bradley's day-old camp deal).
- Alexander-Walker's share haircut is a judgment on top of a fetched line; a
  Dort start would be the first signal against it. His kit games (72) were
  not re-derived.
- Morant's tag changes the weekly model only; the value board cannot price
  his games because his composite is negative on both planes.
- Hoops Rumors was fetched three times and blocked each time; its items rest
  on dated search summaries, as on every prior pull. The first
  Basketball-Reference per-game fetch for Alexander-Walker returned two
  identical rows (a summarizer merge) and was discarded for the game-log
  totals, which reconcile to the 20.8-point season reported by NBA.com.
- No preseason box score exists yet; the first-week items (Lively, Ingram,
  Porziņģis, Beal, Rollins) wait on 10/4–10/7.
- Jaren Jackson Jr.'s "fully healthy" rests on one dated outlet and changed no
  row.
- Which Yahoo position display the league applies (D-G3) is still open.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-1001-1 | Morant's kit games: 60 against a record of 20 (2025-26) and 79 over three seasons. The kit rank is 139 at 60, 50 or 40 games (scratch runs), so the number changes no draft order there; the deck now prices his games in the weekly model. Lower the kit line to 50 for honesty, or hold 60 and revisit with the preseason minutes? | hold 60; revisit at the final pre-draft refresh |
| D-1001-2 | The verifier's name fold keeps generational suffixes, so Butler and Holland need a by-hand exemption every direct-mode pull; and the fallback evidence file carried Vincent on ATL for three months. Teach `verify_rosters.py` to fold II/III/Jr/Sr (red-first) and re-author `rosters_official.json` from the live feed whenever direct mode answers? (The per-team retry and the suite's offline pin shipped today — §6.) | yes, at the next tune-up |
| D-1001-3 | Alexander-Walker's kit games: 72 against 78 and 82 played the last two seasons. Raise to 76 with the reprice? | hold 72 |
| D-1001-4 | The Yahoo market paste is nine days old; the build warns at 14. Paste a fresh ADP list this week? | owner action |

## Provenance and bounds

- Inputs: 41 dated web-search summaries (2026-09-28 → 2026-10-01), three
  Basketball-Reference pages, NBA.com's Hawks preview, ESPN's roster JSON for
  all 30 teams (fetched 2026-10-01 by the verifier and by hand); the owner's
  request; the committed 9/30 pool and boards as the pre-pull snapshots.
- Every number in §5 is a script diff (`scratchpad pull1001/`), every gate
  line is the command's own output.
- Not verified: nothing here rests on a direct read of a blocked sports
  domain.
