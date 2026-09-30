# After-report — 2026-09-30 data pull + deck v35, with the role pass

**Owner request (2026-09-30, verbatim):** "Please conduct daily deck pull, and
research players that you do not have roles for."

Pull window: 2026-09-29 → 2026-09-30 (1 day: day two of training camps; the
Knicks' first cuts). Gate: `check_provenance.py` → `PROVENANCE GATE: PASS —
all rows sourced; verified 2026-07-13 .. 2026-09-30`, exit 0.

**Method.** One search sweep of 58 dated queries: the ledger-shaped
transaction check (Spotrac, ESPN transactions, RealGM, Hoops Rumors), the
flagged receipts (Duren, Brunson, Ingram, Porziņģis, the four unsigned
guards, Sochan, Mathurin, Dillingham, Broome), the injury sweep against the
43-row tag inventory (Beal, Lively, Knueppel, Kessler, Edey, Butler, Paul
George, Jackson Jr., Kawhi, Mark Williams), the team shadows, and — the
owner's second ask — a role pass: every pool row whose note carried no role
text and whose best outside rank sat 40 or more places above the board (35
names) plus the seven-name role cluster from D-P3, researched team by team
(20 team-shaped camp queries) and then by name where a line was in play,
with Basketball-Reference's 2025-26 per-game pages fetched for each
re-derived line. Direct fetches to sports domains stay blocked by the
egress policy (Basketball-Reference is open), so every claim rests on dated
search results, two outlets minimum for anything that moved a row. Edits
applied by script with exact-match assertions (`scratchpad pull0930/
kit_edit.py`, `deck_edit.py`, `judgment_colophon.py`); both boards diffed by
script against the pre-pull snapshots; the deck built through gates 1–7/F8
and driven end to end by the step-5b browser gate.

**Headline.** Two placements moved and one row left the boards: the Knicks
waived John Konchar and signed Tony Bradley to a camp deal on 9/30, and
D'Angelo Russell agreed with the Shanghai Sharks. No trades. The role pass
found five rows whose line still carried a bench shape while two dated
outlets name a starting role — Nurkić, Clingan and Day'Ron Sharpe at center,
Davion Mitchell at point guard, Rollins in a starting-guard battle he won
last season — and re-derived each to last season's Basketball-Reference
line: on the deck Sharpe moves 199 → 78, Rollins 118 → 70, Clingan 75 → 54,
Mitchell 225 → 170; on the kit Rollins 175 → 61, Clingan 113 → 50. One
stale number surfaced on the kit alone: Kawhi's 35-game line was the July
suspension-limbo figure, and the league closed its investigation on 9/2
with a fine and no suspension while he opened Raptors camp healthy on a
ramp-up plan — the kit line goes to 60 games and he moves 25 → 12; the deck's
risk multiplier already priced him and does not move. Every flagged item
held: Duren is reportedly prepared to accept the qualifying offer by
tomorrow's deadline, Brunson practiced 9/29 and his card clears, Porziņģis is
out through the first camp week, Ingram is week-by-week, Lively is not
cleared. Deck v35 built and published.

## 1. Roster changes

| plane | change | count |
|---|---|---|
| both | John Konchar NYK → FA — placed on waivers by New York 2026-09-30, a personal matter and a mutual parting (Hoops Rumors, RealGM, BVM, HoopsHype, Heavy). Kit GP 42 → 30 for the missing team [LIKELY direction, SPECULATIVE magnitude]; deck note; kit provenance re-sourced to Hoops Rumors 9/30 | 1 |
| both | Tony Bradley ATL → NYK — non-guaranteed training-camp deal announced 2026-09-30 (RealGM, Hoops Wire, BVM, Heavy, Yardbarker). Kit GP 40 held; deck note; kit provenance re-sourced to RealGM 9/30 | 1 |
| deck | D'Angelo Russell FA → `out-china` (excluded) — agreed with the Shanghai Sharks of the CBA 2026-09-30 (HoopsHype, Sports Illustrated's Mavericks site). Card removed; not a kit row | 1 |
| both | Five lines re-derived to sourced starting roles (§3): Nurkić, Clingan, Davion Mitchell and Rollins on both planes; Day'Ron Sharpe's deck twin set to the kit's existing 28.2-minute starter line | 5 |
| kit | Kawhi Leonard GP 35 → 60 — the investigation closed 2026-09-02 with a $700K fine and no suspension (NBA.com release, ESPN); healthy at Raptors camp on a planned ramp-up with load management (TSN 9/29, Raptors Republic 9/30, HoopsHype 9/29); 65 games in 2025-26. Deck tag `inj-risk` (×0.78) unchanged | 1 |
| deck | Notes only, no tier change: 39 rows — the status refreshes in §2 and the role notes in §3 | 39 |

Two-source rule: every row edit above carries at least two outlets; the
Russell exclusion two; every note edit two (single-outlet role findings —
Alexander-Walker, Grayson Allen — were recorded here, not on the row).

## 2. Flagged-item receipts (F1) — verdicts

- **Duren — HELD −0.08.** Marc Stein: prepared to accept the one-year $9.6M
  qualifying offer by 11:59 pm Thursday 10/1 if no long-term deal arrives
  (Yahoo 9/29–30, Detroit Jock City, Roundtable); Detroit could extend the
  deadline as late as March 1 but has given no indication. Re-check 10/1.
- **Brunson — CLEARED to zero (card removed).** On the floor at the Knicks'
  first official practice 9/29 with Hart, Anunoby, Towns and Bridges (SNY
  9/29, BVM 9/29); the card's own rule was "clears on the first practice
  report".
- **Ingram — HELD −0.15.** Week-by-week; Redden: a partial tear runs about six
  months less rehab than a full one; on the floor "a little bit" in camp
  (ESPN, NBA.com, Washington Times 9/28–30). Tag unchanged.
- **Porziņģis — HELD −0.10, veto unchanged.** Ruled out through the first camp
  week — at least four practices and the 10/4 preseason opener; Kerr and
  Dunleavy give no timeline (NBC Sports, Yahoo, SI 9/29–30).
- **Cam Thomas, Ivey, Lonzo Ball — HELD, all unsigned** (Spotrac, Yahoo,
  heavy, Hoops Wire FA list). Thomas: no camp deal; the search's "Bucks sign
  Cam Thomas" item is the February 2026 signing, not new.
- **Russell — EXCLUDED** (§1); the −0.20 card is moot and removed.
- **Sochan — HELD −0.2.** Battling Cissoko for the backup-small-forward
  minutes behind Avdija on the non-guaranteed deal (Yahoo camp storylines,
  Rip City Project, KGW).
- **Mathurin — HELD −0.05.** Camp previews keep him as the bench scorer behind
  Herb Jones, in a second unit with Bey, Fears and Queen (Yahoo camp preview,
  SI Pelicans, Pelican Debrief).
- **Dillingham — HELD −0.10.** Cleared waivers; unrestricted free agent 9/30
  (Hoops Rumors, Yardbarker).
- **Rollins — NEW −0.05** with the reprice (§3): the starting job is a camp
  battle, not a decision; clears when Milwaukee names its starter.
- **Broome — unsigned** (waived by LAC 9/24 — Hoops Rumors, RotoWire, CBS).

## 3. The role pass — what the pool had no role for

Selection: deck rows whose note carried no role text (231 of 334) and whose
best rank across the five market files sat 40+ places above the board (35
names), plus the D-P3 cluster (Rollins, Harper, Dybantsa, Nurkić, Kevin
Porter Jr, Queta, Dёmin). Four of the 35 — Giannis, LeBron, Jaylen Brown,
Banchero — are the board's 9-cat-shape fades (D-P4), not role gaps, and were
excluded. The rest, with the dated finding and what was done:

| player | finding (dated) | outlets | action |
|---|---|---|---|
| Jusuf Nurkić (UTA) | starting center: camp day-one first unit with K. George, Peterson, Markkanen, Jackson Jr. | Hoops Rumors Jazz Notes; SLC Dunk 9/29; SI Jazz | **line re-derived** both planes to B-Ref 2025-26 (41 GP, 26.4 mpg, 10.9 / 10.4 / 4.8 / 1.3 stl / .549 FT); kit minutes from 18 to 26 |
| Donovan Clingan (POR) | starting center; Robert Williams the backup | SI Blazers; RotoWire; Blazer's Edge | **line re-derived** both planes to B-Ref 2025-26 (77 GP, 27.2 mpg, 12.1 / 11.6 / 1.1 3PM / 1.7 blk / .680 FT) |
| Day'Ron Sharpe (BKN) | starting center for Brooklyn | Yahoo Nets camp breakdown; TalkBasket; Fadeaway World | **deck twin** set to the kit's 28.2-mpg starter line (B-Ref per-36 16.8 / 12.8 / 4.5 / 2.1) |
| Davion Mitchell (MIA) | starting point guard next to Giannis and Bam | NBA.com season preview; SI Heat; Last Word 9/29 | **line re-derived** both planes to B-Ref 2025-26 (70 of 70 starts, 28.6 mpg, 9.3 / 6.5 ast / 1.3 3PM / .646 FT) |
| Ryan Rollins (MIL) | starting-PG battle with Kevin Porter Jr; took the job last season (17.3 / 4.6 / 5.6 / 1.5 in 32.1 mpg on 47/40) | SI Bucks; Yahoo camp preview; CBS | **line re-derived** both planes toward that season with a share haircut (30 mpg, 15.5 / 4.2 / 5.2 / 1.4); card −0.05 for the undecided battle. B-Ref page not reachable (two slug tries 404); the stat line rests on Yahoo and SI |
| Kevin Porter Jr (MIL) | the other half of that battle | SI Bucks; Yahoo | kit row only — **no deck row exists** (pool-completeness item, D-30-1) |
| Dylan Harper (SAS) | starter or first guard in; Johnson rotating lineups; Fox and Champagnie the likely opening-night five | Yahoo; CBS Sports; Air Alamo | note; line already a 29-minute shape |
| Neemias Queta (BOS) | starting-center favorite in a three-man platoon with Mitchell Robinson and Garza | Yahoo; SI Celtics | note; card note |
| Egor Dёmin (BKN) | projected starting guard; non-surgical plantar fasciitis procedure this offseason, monitored | Yahoo; TalkBasket; CBS | note |
| AJ Dybantsa (WAS) | projected starter | Bullets Forever; Washington Post 9/30 | note |
| Kyshawn George (WAS) | fifth-starter battle with Coulibaly and Tre Johnson | Bullets Forever; Yahoo | note |
| Keyonte George (UTA) | starter | SI Jazz; Hoops Rumors | note |
| Ace Bailey (UTA) | fifth-starter competition with Peterson; bench likely (Peterson with the first unit on day one) | SI Jazz; SLC Dunk 9/29 | note |
| Darryn Peterson (UTA) | first unit on day one | SLC Dunk 9/29; Hoops Rumors | no row change (rookie line already a starter shape) |
| Kel'el Ware (MIL) | about 25 mpg as Turner's primary backup | SI Bucks; Behind the Buck Pass; Brew Hoop | note (line already the backup role) |
| Peyton Watson (CLE) | presumed fifth starter; Atkinson: lineup not set | Yahoo; Hoops Wire; BVM 9/26–29 | note |
| Max Strus (LAC) | fifth-starter candidate among six, bench more likely; Ingram's absence opens early minutes | SI Clippers; Yardbarker | note |
| Rui Hachimura (LAC) | starter | SI Clippers; Yardbarker | note |
| Moussa Diabaté (CHA) | incumbent starting center vs rookie Steinbach | SI Hornets; QC News | note |
| Grayson Allen (CHA) | reserve | SI Hornets | single outlet — recorded here only |
| Coby White (CHA) | starter | SI Hornets; Yahoo | note |
| Kon Knueppel (CHA) | starter when healthy; three weeks since the hamstring strain on 9/30 | SI Hornets; Yahoo | existing note holds |
| Andrew Nembhard, Pascal Siakam, Ivica Zubac (IND) | starters, yellow jerseys on day one; McConnell and Huff their relief | Circle City Spin; SI Pacers | notes |
| Anthony Black (ORL) | sixth man, 20–25 mpg; first up if Suggs misses time | SI Magic; Orlando Magic Daily | note |
| Jalen Green (PHX) | starter, usage share down with Bridges added | SI Suns; Valley of the Suns; BVM 9/29 | note |
| Mark Williams (PHX) | torn labrum surgery 9/10, about five months, February targeted | ESPN; NBA.com; Yahoo; Hoops Wire | `shoulder-recovery` already on the row; note refreshed |
| RJ Barrett (TOR) | starter in the core five | SI Raptors; Yardbarker | note |
| Kawhi Leonard (TOR) | limited on day one by a planned ramp-up and load management; healthy; the investigation closed 9/2 | TSN; Raptors Republic; HoopsHype; NBA.com | kit GP 35 → 60 (§1); deck note |
| DeMar DeRozan (DEN) | bench unit projected; a possible starter over Cameron Johnson or Braun | Forbes 9/29; SI Nuggets | note |
| Naji Marshall (DAL) | rotation minutes, not a starter | Dallas Sports Journal; SI Mavericks | note |
| Ayo Dosunmu (MIN) | bench, the majority of minutes | Star Tribune; Dunking with Wolves | note |
| Nickeil Alexander-Walker (ATL) | starter in the McCollum–NAW–Daniels–Johnson–Okongwu five | SI Hawks (two pieces) | single outlet — recorded here only; the planes carry different lines (deck 19.5, kit 14.5 pts): D-30-2 |
| Andrew Wiggins (MIA) | starter | SI Heat; NBA.com preview | note |
| Bobby Portis (MIA) | bench | SI Heat; NBA.com preview | note |
| Tobias Harris (SAS) | fifth-starter battle with Champagnie, matchup-based | Air Alamo; Yahoo | note |
| Derik Queen (NOP) | bench unit with Mathurin, Bey and Fears | SI Pelicans; Pelican Debrief | note |
| Julius Randle, Michael Porter Jr. (BKN) | starters | Yahoo; Fadeaway World | notes |
| Bennedict Mathurin (NOP) | bench scorer behind Herb Jones | Yahoo; SI Pelicans | card HELD (§2) |
| Jeremy Sochan (POR) | backup-SF battle with Cissoko | Yahoo; Rip City Project | card HELD (§2) |

Forty-one names carry a dated finding. What the pass did not do: touch the
four shape fades, add the missing Porter row, or re-derive Nurkić's FT% (his
.549 is the line's biggest 9-cat cost and is last season's number, not a
projection choice).

## 4. Window sweep, team shadows, injury sweep

- **Transactions (F5 ledger check).** Spotrac, ESPN transactions, RealGM and
  Hoops Rumors via search: zero trades in the window (the "Morant traded 9/29"
  search summary is the July trade mis-dated; the pool has carried him in
  Portland since the baseline). Signings and waivers: the Knicks' 9/30 moves
  (Konchar and N'Faly Dante waived, Jaden Akins to a two-way, Tony Bradley to
  a camp deal, Toby Okani signed-and-waived — Hoops Rumors, RealGM, BVM,
  HoopsHype, Heavy); Russell to China. The MEM cut-down (Clayton, Hawkins,
  Kris Murray, with Russell now gone) is still reported-not-executed (SI
  Grizzlies, Yahoo, TalkBasket) — tenth pull; Hawkins "has a chance to stick".
- **Team shadows.** CHI (Giddey: no restrictions after the May ankle
  arthroscopy — Hoops Rumors, ESPN camp guide), DET (Duren — above), GSW
  (Hawaii camp without Porziņģis; Butler and Moody in individual rehab — NBC
  Sports Bay Area, SF Standard), LAC (Ingram and Beal — Beal's knee
  inflammation keeps him out of the camp start; Jordan Miller's rotator cuff
  and Niederhauser's foot, no pool rows — Sporting Tribune, Hoops Rumors),
  MEM (Edey practicing 9/30 without two-a-days, limited preseason reps,
  ready for the season per Kleiman — Yahoo, SI Grizzlies), NOP (Mathurin —
  above), NYK (first practice 9/29; the 9/30 cuts), POR (Sochan — above;
  Clingan the starting center), SAC (LaVine healthy per Perry; Sabonis ready
  after skipping Lithuania's qualifiers; Simmons the headline addition —
  Sactown Sports, SI Kings). Kawhi: Raptors camp opened 9/29 in Quebec City;
  limited day one by design (TSN, Raptors Republic).
- **Injury sweep vs the F6 tag inventory (43 tagged rows).** Cleared or
  progressing, tags kept by convention: Haliburton (fully healthy, no
  workload limits — ESPN camp guide, Roundtable), Luka (no restrictions —
  Yahoo), Kessler (healthy — Yahoo Lakers), Paul George ("body naturally
  healed" — Yahoo, NBA.com, CelticsBlog), Kawhi (ramp-up), Edey (above).
  Still out, tags kept: Butler (`acl-recovery`, "months away" — SF Standard,
  NBC Sports Bay Area), Moody, Porziņģis (out through the camp week), Lively
  (`risk`, not cleared for camp, opener undetermined — ESPN, CBS, Yahoo),
  Mark Williams (`shoulder-recovery`, February — ESPN, NBA.com), Ingram
  (`achilles-risk`, week-by-week), Knueppel (note: three weeks post-strain on
  9/30, aims for the 10/21 opener — Yahoo). Jaren Jackson Jr.: no dated
  camp item surfaced in two queries (the April "100%" update is the latest);
  tag unchanged. Returning-but-untagged: none found.
- **FA rows.** Kit: Cam Thomas, Ivey, Broome unsigned. Deck adds Lonzo,
  Dillingham (now cleared waivers), Konchar (new) and the retired/overseas
  rows (Westbrook, Brogdon, Valančiūnas, Batum, now Russell).

## 5. Board effects (computed, never eyeballed)

- **Kit.** `top-200-2026-27.md` regenerated against the pre-pull snapshot:
  entries Nurkić (176) and Davion Mitchell (182); exits Khaman Maluach and
  Jeremiah Fears; moves of three or more — Rollins 175 → 61, Clingan 113 →
  50, Kawhi 25 → 12; everything else displaced by at most six places
  (Murray-Boyles 86 → 92, Castle 91 → 97 the largest). Top 12 now ends
  Cunningham, Kawhi.
- **Deck.** By adjusted value over the draftable rows (325 → 324, Russell
  out): no entries; moves of three or more — Sharpe 199 → 78 (adjusted value
  −3.67 → −0.69), Davion Mitchell 225 → 170, Rollins 118 → 70, Clingan 75 →
  54; Nurkić 166 → 167 (the rebounds and assists gained are paid back by the
  .549 FT on 2.7 attempts); Kawhi 34, unchanged (the deck prices availability
  by tag, not games); displacement of three for Goodwin, Powell, Sheppard,
  Eason and Nesmith. Pool sha256 `3db2c63af0c3` (was `6efb01cd772b`).
- **Both planes on the same names.** Rollins and Clingan move together;
  Sharpe moves only on the deck because the kit already carried the starter
  line (a planes waiver by name, §6); Kawhi moves only on the kit because
  the deck's ×0.78 already priced him.

## 6. Deck build and publish

`build_deck.py` on 2026-09-30: roster verification 334/334, 0 mismatches,
evidence re-authored today (fallback-partial: direct ESPN still 403);
freshness stamped with the pool-changes note; JUDGMENT re-dated 2026-09-30
— Brunson and Russell cards removed, Rollins added, Duren, Porziņģis, Ingram,
Kawhi, Cam Thomas, Ivey, Lonzo, Dillingham, Sochan, Mathurin and Queta
re-authored; colophon Data paragraph rewritten for the window; planes 314
shared, team 0, exclusion 0, drift 0, propagation 0, waived 3 by name
(Sharpe: deck twin of an unchanged kit line; Konchar and Kawhi: kit GP
changes with no deck GP column); market `yahoo-2026-09-22.csv`, 296 of 334
priced, 8 days old (warning threshold 14). "safe to publish". Published to
the standing artifact URL as version 35; served bytes read back and matched.

## 7. Gates (2026-09-30)

| gate | result (evidence: the command's own output line) |
|---|---|
| kit `check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-09-30 |
| kit `check_derived.py` | all 11 dated artifacts reproduce byte-for-byte |
| kit `check_report.py` on this file | REPORT GATE: PASS (structure, publication rule, pull-log row) |
| deck `judgment_open_items.py --check-report` on this file | receipts check PASS — all 11 flagged names carry a receipts row |
| deck `verify_rosters.py` | 334/334, 0 mismatches, evidence authored 2026-09-30 |
| deck `check_planes.py` (in the build) | 314 shared · team 0 · exclusion 0 · drift 0 · propagation 0 (3 waived by name) |
| deck `build_deck.py` | all gates pass; safe to publish (pool `3db2c63af0c3`) |
| deck `check_parity.py` on the built page | PARITY: EXACT MATCH (market ranks 324) |
| deck `test_gates.py` / `test_draft.py` / `test_card.py` | all 34 cases passed / all 62 cases passed / CARD: all 61 cases passed |
| deck step-5b `full_dom_check.mjs` on the built page | 128 assertions, 0 failed, 0 page errors, exit 0 (`arena/results/full_dom_check_2026-09-30_v35.json`) |

## 8. Watchlist / open items

- **Duren** — qualifying-offer deadline 11:59 pm Thursday 10/1; Stein says he
  accepts absent a deal. Either branch resolves the card on 10/1.
- **Rollins vs Porter** — Milwaukee's starter call; the −0.05 clears when it
  is named. Porter has no deck row (D-30-1).
- **Nurkić** — 41 games last season; the row carries no availability tag
  because no current injury is reported; a camp setback would add one.
- **Ingram, Porziņģis, Lively** — first preseason week, as before.
- **Brunson** — cleared; no open item.
- **Kawhi** — the ramp-up plan; a load-management pattern in preseason would
  trim the kit's 60.
- **MEM cut-down** — tenth pull unexecuted.
- **Yahoo market paste** — eight days old; early October.
- **Owner decisions carried:** D-P1..D-P4 (9/29 profiles report), D57-1..D57-4
  (mock 57), D-F1..D-F3, D-R1/D-R2; new below.

## Open-item receipts

| player | query run | dated finding |
|---|---|---|
| Jalen Duren | Jalen Duren Pistons qualifying offer deadline October 1 2026 update | prepared to accept the $9.6M QO by 10/1 absent a deal (Stein) — Yahoo 9/29–30, Detroit Jock City, Roundtable |
| Jalen Brunson | Jalen Brunson Knicks first practice training camp September 30 2026 · Knicks first practice Brunson wrist full participant Mike Brown September 29 2026 | on the floor at the 9/29 first practice — SNY 9/29, BVM 9/29; card cleared |
| Brandon Ingram | Brandon Ingram Clippers Achilles timeline training camp September 30 2026 | week-by-week; partial tear about six months less rehab (Redden) — ESPN, NBA.com, Washington Times |
| Kristaps Porzingis | Kristaps Porzingis Warriors update September 30 2026 | out through the first camp week, misses the 10/4 opener — NBC Sports, Yahoo, SI, Heavy |
| Cam Thomas | Cam Thomas free agent signs September 30 2026 · Bucks sign Cam Thomas 2026 training camp contract | unsigned; the Bucks item is the February 2026 signing — Spotrac, Yahoo, Hoops Rumors |
| Jaden Ivey | Jaden Ivey free agent signs team September 2026 | unsigned — Spotrac, heavy |
| Jeremy Sochan | Jeremy Sochan Trail Blazers camp roster battle September 30 2026 | backup-SF battle with Cissoko — Yahoo, Rip City Project, KGW |
| Lonzo Ball | D'Angelo Russell OR Lonzo Ball free agent signs September 30 2026 | unsigned — Spotrac, Hoops Wire, the NBA.com 2026 free-agent list |
| Rob Dillingham | Rob Dillingham signs OR claimed waivers September 30 2026 | cleared waivers, UFA 9/30 — Hoops Rumors, Yardbarker |
| D'Angelo Russell | (same query) | agreed with the Shanghai Sharks 9/30 — HoopsHype, Sports Illustrated (Mavericks) |
| Bennedict Mathurin | Bennedict Mathurin Pelicans training camp role starter bench September 30 2026 | bench scorer behind Herb Jones — Yahoo camp preview, SI Pelicans, Pelican Debrief |
| Ryan Rollins | Milwaukee Bucks training camp 2026 starting lineup Ryan Rollins Kevin Porter Jr Herro Turner Ware role | starting-PG battle; 17.3/4.6/5.6/1.5 last season — SI Bucks, Yahoo, CBS |
| Kawhi Leonard | Kawhi Leonard Raptors training camp September 30 2026 status investigation · NBA announces Clippers Kawhi Leonard penalties September 2 2026 | investigation closed 9/2, fine, no suspension — NBA.com, ESPN; ramp-up at camp — TSN, Raptors Republic |
| John Konchar | NBA transactions September 30 2026 signed waived traded · Knicks practice Tuesday Brunson participated Konchar Dante waived Tony Bradley | waived 9/30 — Hoops Rumors, RealGM, BVM, HoopsHype |
| Tony Bradley | (same) | camp deal 9/30 — RealGM, Hoops Wire, BVM, Heavy |
| Johni Broome | Johni Broome signs free agent September 2026 | unsigned — Hoops Rumors, RotoWire, CBS |
| Dereck Lively | Dereck Lively Mavericks training camp cleared status September 30 2026 | not cleared for camp; opener undetermined — ESPN, CBS, Yahoo |
| Zach Edey | Zach Edey Grizzlies training camp status September 30 2026 | practicing 9/30, no two-a-days; limited preseason reps — Yahoo, SI Grizzlies |
| Jimmy Butler | Jimmy Butler Warriors ACL recovery Hawaii camp update September 30 2026 | individual rehab, "months away" — SF Standard 9/29, NBC Sports Bay Area |
| Paul George | Paul George Celtics training camp knee status September 30 2026 | "naturally healed" — Yahoo, NBA.com, CelticsBlog 9/28–29 |
| Jaren Jackson Jr. | Jaren Jackson Jr. Jazz training camp knee PVNS status September 2026 | no dated camp item; April "100%" update latest — Hoops Rumors, SI Jazz |
| Mark Williams | Mark Williams Suns shoulder surgery out months timeline September 2026 | surgery 9/10, about five months — ESPN, NBA.com, Yahoo, Hoops Wire |
| Egor Demin | Egor Demin plantar fasciitis procedure Nets training camp status September 2026 | non-surgical procedure; monitored at camp — Yahoo, CBS |
| (window ledger) | NBA transactions September 30 2026 · NBA trade September 29 OR September 30 2026 | zero trades; Knicks moves only — Spotrac, ESPN, RealGM, Hoops Rumors |
| (injury sweep) | NBA training camp injury news September 30 2026 · per-player queries above | §4 — Hoops Rumors, ESPN, Yahoo, Sporting Tribune |
| (MEM cut-down) | Grizzlies waive Jordan Hawkins OR Kris Murray OR Walter Clayton September 30 2026 roster | still reported-not-executed — Sports Illustrated (Grizzlies), Yahoo, TalkBasket |
| (role pass, 20 teams) | "<Team> training camp 2026 starting lineup rotation <names>" one each: UTA, MIL, BOS, MIA, SAS, WAS, BKN, POR, CHA, CLE, IND, LAC, ORL, PHX, TOR, DEN, DAL, MIN, ATL, SAC | §3 |
| (B-Ref lines) | basketball-reference.com player pages: Nurkić, Sharpe, Davion Mitchell, Clingan fetched; Rollins 404 on two slugs | §3 |

## Bounds

- Fallback-partial roster verification: the evidence file is authored by this
  pull, not an independent live source; ESPN's API stays 403.
- The five re-derived lines are last season's per-game production at last
  season's minutes with the sourced role; a camp battle lost (Rollins) or a
  platoon (Queta, unchanged) is the direction the residual cards cover.
- Rollins' stat line rests on two outlets' quotes of it, not the B-Ref page.
- Kawhi's 60 games is a judgment between 65 played last season and a stated
  load-management plan; the deck's multiplier is untouched.
- Single-outlet role findings (Alexander-Walker, Grayson Allen) changed no
  row and no note.
- Which Yahoo position display the league applies (D57-1) is still open; the
  pool positions used here are the 9/28 paste's.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-30-1 | Kevin Porter Jr has a kit row but no deck row while he battles Rollins for Milwaukee's starting job (SI Bucks, Yahoo; RotoBaller 126, Yahoo 131). Add the deck row as the kit's twin with Yahoo positions? | add at the next pull |
| D-30-2 | Nickeil Alexander-Walker's planes carry different lines (deck 19.5 pts, kit 14.5) — a drift the F7 gate does not check because neither row changed this window. Re-derive both to one line from his 2025-26 B-Ref page (20.8 ppg) with the starting-role reporting? | re-derive at the next pull; a second single-outlet finding today (SI Hawks) is not enough on its own |
| D-30-3 | Nurkić: 41 games last season on the .549 FT line; the row is untagged because no injury is current. Keep untagged, or carry `inj-risk` on the games history alone? | keep untagged; the kit's 62 games carries the history |
| D-30-4 | Extend the F7 planes gate to compare stat lines on shared rows (it compares team, exclusion, spelling and re-derivation propagation today)? Sharpe and Alexander-Walker show the gap it leaves | yes — a line-diff report, warning only, at the next tune-up |

## Provenance and bounds

- Inputs: 58 dated web-search summaries (2026-09-28 → 2026-09-30) and four
  Basketball-Reference player pages; the owner's request; the committed
  9/29 pool and boards as the pre-pull snapshots.
- Every number in §5 is a script diff (`scratchpad pull0930/`), every gate
  line is the command's own output; the counts in §3 are the table's rows.
- Not verified: nothing here rests on a direct read of a blocked sports
  domain.
