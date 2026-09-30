# After-report — Rookie intake: Yahoo's ten first-round targets, checked and taken into the pool (2026-09-30)

**Owner request (2026-09-30, verbatim):** "Here is some rookie role context and
projections for your internal database:" — followed by Yahoo Sports' piece on
ten 2026 first-round picks to target (Dybantsa, Peterson, Boozer, Wilson,
Wagler, Brown, Acuff, Flemings, Lendeborg, Steinbach), each with a role claim,
a college line and the teammates around him.

**Scope.** The ten claims, checked against both planes and against a second
named outlet per claim (the two-outlet rule, F2: Yahoo's piece is one outlet
and never edits a row on its own). The article's thirty-odd teammate
placements were also read against the pool, since every one of them is a
free consistency check. **What changed:** five rookie lines moved to the
starter minutes a second outlet supports (per-minute rates kept, the 9/30
role-pass method), one deck line joined its kit twin, and three rows carry
notes only. **What did not change:** the rookie translation method, every
non-rookie row, the Mkt column.

**Method.** The paste transcribed verbatim to
`report/market/rookies-raw-2026-09-30.csv` (ten rows: pick, player, team,
role claim, college line, context, outlet); eight dated WebSearch passes on
2026-09-30, one per claim that could move a row (Dybantsa and Wagler already
carried two-outlet starter notes); every board number below is a script
diff of the committed boards before and after. Verification: this file
passes `report/check_report.py`; receipts in the section below.

Pull window: 2026-09-30 → 2026-09-30 (same-evening intake after the 9/30
daily pull; not a roster pull — the 9/30 pull-log rows cover the window).

**Headline.** The article agrees with the pool on every placement it makes
and disagrees with the board on how much the rookies will play. Four of its
ten "starter" claims survive a second outlet (Wilson, Brown, Acuff, and
Peterson with a caveat), Lendeborg's heavy minutes are confirmed by Kerr's
own words and Porziņģis' indefinite absence, Boozer's role was already
priced on the kit, and Steinbach's "job to lose" is contradicted by SI
Hornets and ESPN's depth chart. The five re-derivations move **Lendeborg
120 → 81, Peterson 174 → 145 and Wilson 147 → 122** on the kit and bring
Acuff onto the board at 190; on the deck Boozer's twin jumps him **127 → 51**
and Acuff **293 → 181**. Brown stays outside the top 200 on both planes even
at 29 minutes, because a .410 shooter with rookie-guard turnovers is a
9-cat drag whatever his minutes.

---

## 1. The ten claims, checked

| pick | player | Yahoo's claim | second outlet (2026-09-30) | verdict | action |
|---|---|---|---|---|---|
| 1 | AJ Dybantsa (WAS) | sizable impact from the gate, starting group | already on the row: Bullets Forever, Washington Post (9/30) | confirmed | note appended, no line change |
| 2 | Darryn Peterson (UTA) | backcourt starter next to Keyonte George | Hoops Rumors Jazz Notes: day-one first unit in purple, the fifth spot contested with Bailey, Sensabaugh, Mykhailiuk | starter-likely, contested | minutes 28 to 30 on both planes |
| 3 | Cameron Boozer (MEM) | primary scoring option from the opening tip | SI Grizzlies: starting PF next to Edey, offensive hub per Iisalo | confirmed | kit line already the 32-minute starter line; deck line set to it |
| 4 | Caleb Wilson (CHI) | starting power forward | Heavy, Sun-Times: starting frontcourt with Claxton and Buzelis; Patrick Williams to the bench | confirmed (as a starting forward) | minutes 28 to 30 on both planes |
| 5 | Keaton Wagler (LAC) | key piece, starter | already on the row (9/16 research, two outlets) | confirmed | none |
| 6 | Mikel Brown Jr. (BKN) | starting point guard, primary ball handler | ClutchPoints rotation projection: starting PG next to Dёmin; ankle sprain in camp, minor per Marks (Yahoo) | confirmed | minutes 24 to 29 on both planes; games held at 65 |
| 7 | Darius Acuff Jr. (SAC) | starting point guard from day one | CBS Sports "projected to start"; Sactown Sports on the GM's expectations | confirmed | minutes 26 to 29 on both planes |
| 8 | Kingston Flemings (ATL) | backup point guard behind McCollum | SI Hawks, HoopsHype (McCollum: "ahead of his time") | confirmed | note only; bench line unchanged |
| 11 | Yaxel Lendeborg (GSW) | "clearly going to play a ton" (Kerr); can fill at C with Porziņģis out | NBA.com media day (the Kerr quote); CBS Sports, SI Warriors (Porziņģis out indefinitely, undisclosed) | confirmed | minutes 26 to 28 on both planes |
| 14 | Hannes Steinbach (CHA) | starting center, his job to lose | SI Hornets and ESPN's depth chart lean Diabaté starting, Steinbach off the bench | contested, not a lock | note only; 24-minute line unchanged |

## 2. The re-derivations

Method (plan-gate A1): the pool's per-minute rates are kept, the shooting
percentages are untouched, and the counting stats scale with minutes. No
college-to-NBA re-translation, so a rookie's line stays the baseline's
translation of his college profile, only at more minutes.

| player | minutes | kit line before | kit line after | kit rank | deck rank |
|---|---|---|---|---|---|
| Darryn Peterson | 28 to 30 | 17.0 / 3.8 / 3.5, 1.7 3PM, 1.1 stl | 18.2 / 4.1 / 3.8, 1.8 3PM, 1.2 stl | 174 to 145 | 155 to 142 |
| Caleb Wilson | 28 to 30 | 13.5 / 7.5 / 2.0, 1.0 stl, 1.3 blk | 14.5 / 8.0 / 2.1, 1.1 stl, 1.4 blk | 147 to 122 | 204 to 123 |
| Mikel Brown Jr. | 24 to 29 | 10.5 / 2.5 / 4.0 | 12.7 / 3.0 / 4.8 | outside 200, unchanged | 265 to 259 |
| Darius Acuff Jr. | 26 to 29 | 15.0 / 2.8 / 4.5, 1.9 3PM | 16.7 / 3.1 / 5.0, 2.1 3PM | outside 200 to 190 | 293 to 181 |
| Yaxel Lendeborg | 26 to 28 | 12.0 / 7.0 / 2.5, 1.0 stl, 0.8 blk | 12.9 / 7.5 / 2.7, 1.1 stl, 0.9 blk | 120 to 81 | 120 to 85 |
| Cameron Boozer | 32 (kit, unchanged) | deck carried 15.0 / 8.5 / 2.5 | deck set to the kit's 18.5 / 9.5 / 3.8 | 43 to 42 | 127 to 51 |

The deck lines for Wilson and Acuff were bench-shaped copies that had
drifted from the kit's (Wilson 11.5 points against the kit's 13.5 before
today; Acuff 12.0 against 15.0), which is why their deck moves are larger
than their kit moves: the twin closes the plane gap D-30-4 named as well as
adding the minutes.

## 3. What did not move, and why

- **Boozer's kit line** already carried the starter role (32 minutes, 72
  games; rank 43). The article confirms it; only the deck moved.
- **Dybantsa and Wagler** already carried two-outlet starter notes. Their
  planes still differ on Dybantsa's line (deck 20.5 / 5.5 / 3.0, kit 18.0 /
  6.0 / 2.8, neither with a dated derivation): D-R1.
- **Flemings** is a backup on every outlet; the 20-minute line is right.
- **Steinbach** is contested: SI Hornets' own preview and ESPN's depth chart
  put Diabaté first. If he wins the job in preseason, the re-derivation is
  27 minutes (D-R2).
- **Brown** moves five minutes and stays outside the top 200 on both planes.
  A .410 field-goal line on 11.5 attempts with 2.3 turnovers is a 9-cat drag
  that more minutes deepen; the market's 117 ADP is buying the role, not the
  categories. The board is first-principles and stays there.
- **Lendeborg's jump to 81** is the largest and deserves a sentence: his
  per-minute line (rebounds, steals, blocks, .520 shooting, low turnovers)
  is the 9-cat shape the engine pays for, so two more minutes is a lot of
  value. It rests on Kerr's quote and an indefinite Porziņģis absence; if
  Porziņģis returns healthy before the draft, 26 minutes is the honest
  number again (watchlist).

## 4. Board effects (computed, never eyeballed)

Kit (`report/top-200-2026-27.md`, before and after): moves of three places
or more are exactly the three re-derived men inside the top 200 (Lendeborg
120 → 81, Peterson 174 → 145, Wilson 147 → 122); Acuff enters at 190 and
Taylor Hendricks exits at the tail; Boozer 43 → 42, Wagler 190 → 191,
Dybantsa 173 unchanged. Deck (`hoops.adj_value` order on `data/players.csv`,
before and after): Boozer 127 → 51, Acuff 293 → 181, Wilson 204 → 123,
Lendeborg 120 → 85, Peterson 155 → 142, Brown 265 → 259; no other row moved
five places or more.

## 5. The free consistency check

Every team the article places a player on matches the pool: Young, Kyshawn
George, Davis and Sarr in Washington; Keyonte George, Markkanen, Jackson Jr.
and Nurkić in Utah; Morant in Portland and Jackson Jr. gone from Memphis;
Pippen Jr., Coward, Grant and Edey in Memphis; Giddey, Powell and Buzelis in
Chicago; Leonard in Toronto and Ingram, Garland, Jones Jr. and Lopez with
the Clippers; Porter Jr. and Randle in Brooklyn; LaVine, Hunter, Murray and
Sabonis in Sacramento; McCollum, Alexander-Walker, Johnson and Daniels in
Atlanta; Porziņģis in Golden State (the pool's note already carries the
indefinite absence); Ball in Minnesota and Bridges in Phoenix. Patrick
Williams is the one name the pool does not carry, and he is the bench
player Wilson displaces. Nothing in the article moved a placement.

## 6. Deck build and publish

- Verify: 334 of 334 rows against the 9/30 evidence file
  (fallback-partial); freshness re-stamped 2026-09-30 with the rookie
  pool-changes note; JUDGMENT date unchanged at 2026-09-30 (gate 5).
- Build: planes 314 shared, drift 0, propagation 0, one waiver (Boozer:
  deck line set to the kit's existing starter line, the kit row already
  carried it); pool sha `bdb40833a6ac`; injection round-trip OK; safe to
  publish. Parity: EXACT MATCH.
- Colophon: one sentence added to the Data paragraph describing this pass.
- Suites: test_draft 62 of 62, test_card 61 of 61, test_gates PENDING_GATES.
- DOM drive (full_dom_check, state 54): PENDING_DOM.
- Publish: PENDING_PUBLISH.

## 7. Gates (2026-09-30)

- Kit: `check_provenance.py` PASS (no team labels changed); `check_derived.py`
  11 of 11; `check_report.py` PASS on this file; pull-log row added.
- Deck: build gates 1 to 7 and F8 as above.

## Watchlist / open items

- **Peterson's fifth starting spot** (Bailey, Sensabaugh, Mykhailiuk): the
  first preseason lineup decides whether 30 minutes holds.
- **Steinbach vs Diabaté**: re-derive to 27 minutes if he starts the
  preseason opener (D-R2).
- **Brown's ankle**: minor per the GM; a missed opener moves the games line.
- **Lendeborg and Porziņģis**: a healthy Porziņģis return before Oct 14
  puts Lendeborg back at 26 minutes.
- Carried: Duren's qualifying-offer deadline (Oct 1), the fresh Yahoo ADP
  paste (early October), the league settings screenshot (D-G5).

## Open-item receipts

| item | query run (2026-09-30) | dated finding |
|---|---|---|
| Peterson starter | WebSearch, Jazz camp starting five | Yahoo camp footage: George, Peterson, Markkanen, Jackson Jr., Nurkić in purple on day one; Hoops Rumors: Peterson, Bailey, Sensabaugh, Mykhailiuk in the mix for the fifth spot; Deseret on camp day one |
| Boozer role | WebSearch, Grizzlies camp | SI Grizzlies forwards preview: starting PF next to Edey; Iisalo on his post scoring, range and passing; TSN camp storylines |
| Wilson starter | WebSearch, Bulls camp roster | Heavy and the Sun-Times: starting frontcourt Claxton, Buzelis, Wilson; Williams battles for bench minutes; Bleacher Nation camp roster |
| Brown starter | WebSearch, Nets ball-handler | ClutchPoints rotation projection: starting PG with Dёmin; Yahoo: left ankle sprain, "not considerable time" per Marks |
| Acuff starter | WebSearch, Kings camp | CBS Sports fantasy news: projected to start; Sactown Sports: GM expectations; NBA.com media day |
| Flemings role | WebSearch, Hawks backup PG | SI Hawks: assumed backup PG; HoopsHype: McCollum working out with him, "ahead of his time" |
| Lendeborg minutes | WebSearch, Kerr quote and Porziņģis | NBA.com media day takeaways and Yahoo: Kerr, "clearly going to play a ton"; CBS Sports and SI Warriors: Porziņģis out indefinitely, undisclosed health issue |
| Steinbach starter | WebSearch, Hornets center | SI Hornets "Starting Center Dilemma": Diabaté the incumbent, most projections and ESPN's depth chart lean Diabaté; Yahoo: Steinbach's to lose |

## Bounds

- The lines are minutes-scaled, not re-translated; a rookie's per-minute
  rates remain the July baseline's estimate of his college profile.
- Peterson's starter status is the least settled of the five; the 30-minute
  figure is a midpoint between a contested fifth spot and a No. 2 pick's
  usual load.
- Boozer's deck change is a deck-only twin, recorded as a build waiver.
- Search summaries are the channel for every outlet named here (Yahoo,
  SI, CBS, Hoops Rumors and the rest are egress-blocked for direct reads);
  each claim rests on two independently named outlets or is marked
  contested.
- No claim here rests on a direct read of a blocked sports domain.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-R1 | Dybantsa's planes carry different lines (deck 20.5 / 5.5 / 3.0, kit 18.0 / 6.0 / 2.8) with no dated derivation on either. Unify to one line at the next pull, and which? | unify to the kit's line at the next pull (the kit is the report card; the deck is its twin) unless a dated outlet supports the higher scoring number |
| D-R2 | Steinbach: if he starts the preseason opener over Diabaté, re-derive to 27 minutes on both planes? | yes, on the first preseason start, two outlets |
| D-R3 | Lendeborg at 28 minutes rests on Porziņģis' absence; if Porziņģis is cleared before Oct 14, return him to 26? | yes, with the clearance report |
| D-R5 | Card wording (owner-reported 2026-09-30, mid-intake): the advice line quotes the ΔECW gap between the 🎯 and the #2 as the reason for the pick, so when the 🎯 wins on value and trails on ΔECW it reads "Take Chet Holmgren — −0.017 expected categories per week over Jalen Williams". Change the sentence, when the gap is negative, to name the real reason: "Take Chet Holmgren — the best value left (Mkt 25); Jalen Williams fits this week's roster slightly better (+0.034 cats/wk) but ranks lower on value; only ~6% chance Chet survives to your next turn." Ordering unchanged; red-first case in test_card.py; separate deck PR. | yes, next deck build |
| D-R4 | The rookie translation itself (per-minute rates from the July baseline) has now been scaled three times without a re-check; audit the five re-derived rookies' per-minute lines against their college per-36 before the final pre-draft build? | yes, at the final pre-draft refresh, as a report before any edit |

## Provenance

- Inputs: the owner's paste (transcribed to `report/market/rookies-raw-2026-09-30.csv`);
  eight dated WebSearch summaries on 2026-09-30; the committed 9/30 boards as
  the before-state (scratchpad `rookies0930/`).
- Every board number is a script diff (`kit_edit.py`, `deck_edit.py`, the
  rank-diff one-liners in the session log); every gate line is the
  command's own output.
- Not verified: nothing here rests on a direct read of a blocked sports
  domain.
