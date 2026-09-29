# After-Report — 2026-09-29 re-derivation pass: Yahoo's official positions on both planes, nine projection lines re-derived from last season and camp reporting, six pool rows added — and what moved on each board

**Owner request (2026-09-29, verbatim):** "Proceed with all recommended
actions, then merge. Provide after report of major ranking movements after
these data reads" — on the decision sheet of the same-day market intake
(`after-report-2026-09-29-market.md`): D-M1 sync position eligibility to
Yahoo's official list on both planes; D-M2 and D-M5 add the Yahoo-top-250
names the pool lacks; D-M4 re-derive the nine projection lines the kit held
high on its own. D-M3 (no consensus blend) is a no-action decision and
stands.

**Method:** every re-derived line rests on two inputs fetched this pass — the
player's 2025-26 per-game row opened directly on Basketball-Reference, and
dated camp-role reporting from at least two named outlets (search-summary
reports; the environment's egress policy blocks direct fetches of most sports
domains, see Bounds). Positions are Yahoo's own 9/28 eligibility strings
(`report/market/yahoo-9cat-rankings-2026-09-28.csv`), applied by script to
every row the intake's join matched (244 kit rows, 243 deck rows); the
platform's rule needs no second outlet. Board movement on both planes was
computed by a diff script over the pre-edit and post-edit boards, never
eyeballed. Verification: this file passes `report/check_report.py`; the
deck's `judgment_open_items.py --check-report` result is recorded in §5.

Pull window: 2026-09-29 → 2026-09-29 (same-day re-derivation pass; no news
sweep — the 9/29 pull's transaction sweep, team shadows and 11 receipts stand,
`after-report-2026-09-29.md` §3 and §8).

**Gates (kit):** `PROVENANCE GATE: PASS — all rows sourced; verified
2026-07-13 .. 2026-09-29` · `rank_engine.py`: 200 players from 324 projected
· `REPORT GATE: PASS` (this file) · `DERIVED: all 10 dated artifacts
reproduce byte-for-byte from their pinned inputs`.

**Headline.** The nine lines the market intake singled out all moved, and
they moved a lot: on the kit board Jordan Poole leaves the top 200 (81 →
out), Brook Lopez falls 94 places (96 → 190), Cameron Johnson 54 (61 → 115),
Myles Turner 47 (40 → 87), Tari Eason 44 (67 → 111), Kel'el Ware 43 (39 →
82), Brandon Ingram 32 (88 → 120), Evan Mobley 15 (19 → 34, on his free-throw
percentage alone) and Christian Braun 11 (83 → 94). The deck agrees in
direction and size (Poole 79 → 293, Lopez 58 → 171, Eason 44 → 109, Cameron
Johnson 50 → 103, Ingram 68 → 117, Braun 54 → 95, Turner 52 → 84, Ware 59 →
80, Mobley 12 → 21). Every one of those names was on the owner's mock-56
card in the middle and late rounds; the repeat-name question the draft-56
report answered mechanically is now closed on the evidence too — the rows
were high, and they are not any more. Nothing touched the point-guard plan:
Haliburton, Lillard and Irving hold their lines, though Irving is now
**PG-only** on Yahoo's official list (he loses SG). Positions changed on 82
kit rows and 104 deck rows; six names entered the kit pool (Beal, Clifford,
Simmons, Riley, Flemings, Zach Collins) and four the deck (the latter four —
the deck already carried Beal and Clifford). No placement moved.

---

## 1. Roster changes

No roster changes applied. This pass ran no transaction sweep: it is a
same-day re-derivation on the pool the 9/29 pull verified (sweep, team
shadows and the 11 flagged receipts in `after-report-2026-09-29.md` §3, §8).
Ten rows entered the two pools at placements the Yahoo 9/28 list and the
dated reporting agree on — §3b. Roster verification on the deck plane:
334/334 rows checked against the evidence ledger, zero mismatches
(fallback-partial mode; ESPN's roster API still returns 403).

## 2. Position eligibility synced to Yahoo (D-M1)

| plane | matched to Yahoo | strings changed | gained a listing | lost or swapped one (evidence: the joined files) |
|---|---|---|---|---|
| kit `report/projections-2026-27.csv` | 244 of 318 | **82** | 81 | Max Strus SG → PF,SF |
| deck `data/players.csv` | 243 of 330 | **104** | 98 | Kyrie Irving PG,SG → **PG**; Nickeil Alexander-Walker SG,SF → PG,SG; Santi Aldama PF,C → PF,SF; Max Strus SG,SF → PF,SF; Nikola Jović PF,SF → C,PF; Lauri Markkanen PF,C → SF,PF |

Yahoo never lists fewer positions than the kit did (the intake's finding
holds: 81 strict widenings and one outright change), but the deck had six
rows Yahoo narrows or swaps, because the deck's strings were authored
independently. The platform's eligibility is the league's rule for the
October draft, so both planes now read Yahoo's string verbatim. On the kit
the column is display-only (the z-score engine does not read it), so no rank
moved for a position; on the deck the PG/SG/G/SF/PF/F/C slots, the family
reads and the mock opponents' positional need all read it — 40 draftable
players the deck under-counted (the intake's §4 tables name them) now count
what Yahoo counts. Irving's PG-only listing still fills PG, G and Util; it
no longer fills SG.

## 3. Significant fantasy analysis changes

### 3a. Nine lines re-derived (D-M4)

Kit line before → after (GP / mpg / pts / reb / ast / stl / blk / 3PM ·
FG% / FT%); the deck row moved to the same line on the same evidence (the
plane check reports zero propagation mismatches, no waivers). Swing is on
points unless stated; direction and magnitude labeled honestly.

| player | before → after | 2025-26 per-game (Basketball-Reference, opened 2026-09-29) | role mechanism, two dated outlets | swing / label | kit # before → after | deck # before → after |
|---|---|---|---|---|---|---|
| Jordan Poole (NOP) | 65 / 30 / 19.5 / 3.0 / 4.5 / 1.2 / 0.3 / 3.0 · .440/.880 → **58 / 19 / 10.5 / 1.7 / 2.5 / 0.6 / 0.2 / 1.9 · .410/.870** | 39 GP, 8 GS, 23.9 mpg, 13.4 / 2.0 / 3.1 / 0.6 / 0.4, 2.5 3PM, .372 on 11.4 FGA, .860 FT | third point guard behind Dejounte Murray and Jeremiah Fears, with Mathurin at SG squeezing the bench wing minutes; out of the rotation by the end of 2025-26 (SI Pelicans "Rotation Crunch"; Yahoo camp preview 9/28; Pelican Debrief) | −46% · direction [LIKELY], magnitude [SPECULATIVE] — the standing row was his 2024-25 Washington starter line | 81 → **out of the top 200** | 79 → 293 |
| Myles Turner (MIL) | 68 / 30 / 15.0 / 7.0 / 1.6 / 0.7 / 2.0 / 1.9 · .490/.800 → **68 / 27 / 12.5 / 5.8 / 1.5 / 0.7 / 1.7 / 2.0 · .460/.770** | 71 GP, 71 GS, 26.9 mpg, 11.9 / 5.3 / 1.5 / 0.7 / 1.6, 2.1 3PM, .440 on 9.1 FGA, .740 FT | starter entering camp, but Ware is "right on his heels" with "no guarantees"; last season's points and blocks were the second-lowest of his career (SI Bucks centers preview; Behind the Buck Pass) | −17% · [LIKELY] / [SPECULATIVE] — the row was the Indiana-era shape | 40 → 87 | 52 → 84 |
| Tari Eason (HOU) | 66 / 26 / 12.0 / 6.5 / 1.8 / 1.6 / 0.8 / 1.1 · .480/.760 → **64 / 26 / 11.0 / 6.2 / 1.6 / 1.4 / 0.7 / 1.4 · .455/.770** | 60 GP, 34 GS, 25.8 mpg, 10.5 / 6.3 / 1.5 / 1.2 / 0.5, 1.6 3PM, .416 on 9.7 FGA (2024-25: .487, 1.7 stl, 0.9 blk) | bench role behind Durant, Smith and Amen Thompson, minutes trending up each season; re-signed 5yr/$81.5M 7/2 (The Dream Shake camp breakdown; CBS Sports) | −8% pts, FG% and stocks to the two-year blend · [LIKELY] / [LIKELY] | 67 → 111 | 44 → 109 |
| Cam Johnson (DEN) | 68 / 31 / 17.0 / 4.5 / 3.0 / 0.9 / 0.4 / 2.7 · .470/.870 → **66 / 30 / 14.0 / 4.0 / 2.6 / 0.8 / 0.4 / 2.3 · .475/.860** | 54 GP, 54 GS, 30.5 mpg, 12.2 / 3.8 / 2.4 / 0.7 / 0.4, 2.0 3PM, .480 on 8.8 FGA (2024-25 BKN: 18.8 on 13.1 FGA) | starting small forward in Denver's five with DeRozan on the bench; fourth-option usage, double figures in 13 of the last 15 after a slow start and a knee (SI Nuggets lineup projection; Colorado Springs Gazette 9/20) | −18% pts, −22% attempts · [LIKELY] / [SPECULATIVE] | 61 → 115 | 50 → 103 |
| Christian Braun (DEN) | 74 / 32 / 15.0 / 5.0 / 2.8 / 1.1 / 0.4 / 1.6 · .520/.800 → **72 / 31 / 13.8 / 4.9 / 2.6 / 1.0 / 0.4 / 1.1 · .545/.800** | 44 GP (ankle), 31.8 mpg, 12.0 / 4.8 / 2.7 / 0.7 / 0.3, 1.0 3PM, .519 (2024-25: 79 GP, 15.4, 1.1 3PM, .580) | cemented starter after the Watson trade, "explosiveness back" for camp (Gazette Nuggets notebook 9/28; SI Nuggets) | −8% pts; the 1.6 3PM had no season behind it · [LIKELY] / [LIKELY] | 83 → 94 | 54 → 95 |
| Brook Lopez (LAC) | 68 / 26 / 12.0 / 5.0 / 1.6 / 0.6 / 1.8 / 1.4 · .510/.800 → **70 / 23 / 9.5 / 4.0 / 1.3 / 0.5 / 1.4 / 1.5 · .460/.780** | 75 GP, 40 GS, 21.8 mpg, 8.5 / 3.6 / 1.3 / 0.6 / 1.2, 1.5 3PM, .428 on 7.2 FGA | one of two healthy centers with Isaiah Jackson (Niederhäuser out, Lisfranc), likely starter at 38 in a 22-minute platoon (SI Clippers position battle; NBA.com season preview 9/22; Clipperholics) | −21% · [LIKELY] / [SPECULATIVE] — the row was the Milwaukee 2024-25 line | 96 → 190 | 58 → 171 |
| Kel'el Ware (MIL) | 72 / 30 / 14.5 / 10.5 / 1.5 / 0.7 / 1.8 / 0.7 · .570/.700 → **74 / 24 / 11.5 / 8.5 / 0.9 / 0.7 / 1.3 / 1.0 · .545/.720** | 77 GP, 34 GS, 22.1 mpg, 11.1 / 9.0 / 0.7 / 0.8 / 1.1, 1.2 3PM, .530 on 8.4 FGA, .740 FT | "clear No. 2 center behind Myles Turner" entering camp (SI Bucks; Behind the Buck Pass) | −21% · [LIKELY] / [SPECULATIVE] — the row priced a 30-minute starter | 39 → 82 | 59 → 80 |
| Brandon Ingram (LAC) | 48 / 32 / 20.0 / 5.5 / 4.5 / 0.8 / 0.6 / 1.8 · .470/.830 → **48 / 31 / 19.0 / 5.3 / 3.9 / 0.8 / 0.6 / 1.7 · .465/.820** | 77 GP, 33.8 mpg, 21.5 / 5.6 / 3.7 / 0.8 / 0.7, 1.8 3PM, .477 on 16.7 FGA (TOR) | out for the start of the season after the partial Achilles found at the May heel surgery, "week-by-week", reporting points at November–early December; GP 48 already carried it (ESPN 9/28; NBA.com; RealGM). The per-game trim is the ramp and a Garland-led offense; assists to the Toronto level | −5% · [LIKELY] / [SPECULATIVE]. RotoBaller's 15.0 is a season blend; the kit keeps per-game plus GP | 88 → 120 | 68 → 117 |
| Evan Mobley (CLE) | FT% .740 on 4.5 FTA → **.680** (line otherwise held) | 65 GP, .606 on 4.6 FTA in 2025-26 after .725 and .719; career .674 | no role change; the free-throw assumption had no recent season behind it (Basketball-Reference; StatMuse) | FT impact only · [LIKELY] / [SPECULATIVE] on where between .606 and .725 he lands | 19 → 34 | 12 → 21 |

Two things to read off the table. First, the kit's own after-the-fact
check: for eight of the nine the standing row was a prior-team or prior-role
line (Poole's Washington year, Turner's Indiana shape, Lopez's Milwaukee
year, Cameron Johnson's Brooklyn usage, Ware's Miami starter minutes) — the
July baseline carried them forward and nothing re-derived them because no
transaction moved them. That is the failure class the market intake was
built to catch, and it caught it. Second, the moves land the kit inside the
pack: Poole (RotoBaller 230, Yahoo 211), Lopez (144 / 156), Turner (104 /
108), Ware (65 / 77), Cameron Johnson (105 / 158), Eason (140 / 150) are
now within a round of where the market has them.

### 3b. Ten rows added (D-M2, D-M5)

Six kit rows and four deck rows (the deck already carried Beal and
Clifford; Clifford's deck row was still his rookie projection and is
repriced here off his actual rookie season). Every line is **[ESTIMATED]**:
base rates from Basketball-Reference opened this pass, scaled for the
researched role. The provenance row carries the first outlet's URL; the
second is named here.

| player | kit row (GP / mpg / pts / reb / ast / stl / blk / 3PM · FG% / FT%) | base rates (Basketball-Reference) | placement and role, two dated outlets (evidence) | kit # | deck # |
|---|---|---|---|---|---|
| Bradley Beal (LAC, SF,SG) | 55 / 24 / 13.0 / 2.8 / 3.0 / 0.9 / 0.4 / 1.6 · .470/.810 | 2024-25 PHO 53 GP, 32.1 mpg, 17.0 / 3.3 / 3.7 / 1.1 / 0.5, 1.9 3PM, .497; 2025-26 LAC 6 GP (hip surgery) | re-signed LAC 2yr/$13.2M 8/13; right-knee inflammation while ramping up from the hip surgery, out for the start of camp, preseason opener in doubt, regular season "doesn't sound to be in serious danger" (HoopsHype 9/28; RotoWire; SI Clippers). Matches the deck row's line and inj-hip-risk tag | 194 (enters) | 218 → 214 |
| Nique Clifford (SAC, SF,SG) | 74 / 24 / 9.0 / 3.8 / 2.4 / 0.9 / 0.3 / 1.1 · .430/.740 | 2025-26 SAC 75 GP, 28 GS, 25.1 mpg, 8.6 / 3.8 / 2.4 / 0.9 / 0.3, 1.0 3PM, .418 | second-year wing in a three-guard bench rotation with Monk and Simmons, consistent minutes but few starts (SI Kings position battles; Sactown Sports; Fanrecap) | outside the 200 | 185 → 284 (deck rookie projection 11.5 pts retired) |
| Ben Simmons (SAC, PG) | 55 / 20 / 5.0 / 4.5 / 4.8 / 0.9 / 0.5 / 0.0 · .520/.650 | sat out all of 2025-26 (back and leg); 2024-25 BKN 33 GP, 25.0 mpg, 6.2 / 5.2 / 6.9 / 0.8 / 0.5, .547 | signed SAC 1yr/$3.5M, announced 9/8, as the backup point guard behind rookie Darius Acuff Jr.; "no limitations" entering camp (ESPN; NBA.com; CBS Sports; Sactown Sports). Deck tag inj-back-risk (×0.78) | outside the 200 | 276 (enters) |
| Will Riley (WAS, PF,SF) | 74 / 24 / 11.8 / 3.2 / 2.3 / 0.7 / 0.2 / 1.4 · .445/.800 | 2025-26 WAS 74 GP, 18 GS, 22.1 mpg, 10.3 / 2.9 / 2.0 / 0.7 / 0.1, 1.1 3PM, .439 | on the 2026 camp roster; the primary perimeter weapon off the bench, competing with Middleton and Coulibaly for second-unit minutes (Bullets Forever camp roster; SI Wizards; Yardbarker) | outside the 200 | 277 (enters) |
| Kingston Flemings (ATL, PG,SG) | 68 / 20 / 8.0 / 2.5 / 3.0 / 0.8 / 0.2 / 1.0 · .420/.760 | rookie — Houston 2025-26: 37 GP, 31.6 mpg, 16.1 / 4.1 / 5.2 / 1.5 stl, 38.7% from three (NBA.com draft profile; Yahoo) | No. 8 pick on a rookie-scale deal; expected backup point guard, competing with Nembhard and Carter (SI Hawks position battles; Soaring Down South). Deck tag rookie-proj | outside the 200 | 311 (enters) |
| Zach Collins (CHI, C) | 62 / 17 / 7.0 / 4.6 / 1.6 / 0.4 / 0.5 / 0.6 · .520/.800 | 2025-26 CHI 10 GP, 18.4 mpg, 9.7 / 5.6 / 1.5; 2024-25 (SAS+CHI) 64 GP, 15.3 mpg, 6.4 / 4.5 / 1.7, .507 | on the 21-man camp roster 9/25 on a standard deal; re-signed 2yr/$17M with a team option as the backup big behind Claxton, platooning with Jalen Smith (Bleacher Nation; Pippen Ain't Easy; On Tap Sports Net) | outside the 200 | 292 (enters) |

RotoBaller's six rookies without a pool row (Ament, De Larrea, Cissé,
González, Bryant, Wolf) are not added: Yahoo's 250 does not carry them
(D-M5 as decided).

### 3c. Board movement, computed (both planes)

Diff script over the pre-edit and post-edit boards (`kit-diff.json`,
`deck-diff.json` in the session scratchpad; the numbers below are read from
them).

| plane | rows (evidence: `board_diff.py` output, kit-diff.json / deck-diff.json) | entries | exits | moves ≥ 3 | moves ≥ 5 | position strings changed on the board |
|---|---|---|---|---|---|---|
| kit top-200 | 200 → 200 (pool 318 → 324) | Bradley Beal #194, Khaman Maluach #196 | Jordan Poole (was #81), Luke Kennard (was #198) | 88 | 43 | 58 |
| deck ranked board (availability > 0) | 319 → 323 (pool 330 → 334) | Simmons #276, Riley #277, Zach Collins #292, Flemings #311 | none | 130 | 62 | 101 |

The nine named moves are the story (§3a). Everything else is
re-standardization: the z-scores standardize over the top-180 (kit) and
top-156 (deck) pools, and when six mid-board rows fall out of that pool the
means shift and the rows around them move a few places in the other
direction. On the kit the largest secondary moves are all bigs and stocks
players, up: Isaiah Hartenstein 112 → 102, Rudy Gobert 93 → 84, Collin
Murray-Boyles 95 → 86, Paul Reed 106 → 97, Zach Edey 70 → 63, Zubac 86 → 79,
Naz Reid 99 → 92, Aaron Gordon 100 → 93, Zion 103 → 96, Draymond 114 → 107;
no secondary move exceeds 10 places and none crosses a tier line. On the
deck the same class: Ja Morant 74 → 64, Jaylen Brown 81 → 72, Avdija 86 →
77, Gobert 88 → 79, Duren 71 → 63, Siakam 73 → 65, Embiid 78 → 70, Herbert
Jones 82 → 74, Clingan 83 → 75, Hartenstein 84 → 76; none exceeds 10. Top-12
on both planes: unchanged.

### 3d. What it means for the draft

- **The mock-56 late-round set is repriced.** Turner (card #1 at #106),
  Eason (#111), Cameron Johnson (#87), Braun (#130/#135), Lopez (#154) and
  Poole (hindsight's #130 alternative) were the names the owner asked the
  system to defend against bias. The draft-56 report showed the card was
  computing them honestly from the rows; the market intake showed the rows
  were high; this pass fixed the rows. Those cards will not surface at the
  same turns in the next mock, and the +7.6-point follow-the-card
  counterfactual's Poole leg is withdrawn, not caveated: Poole is no longer
  a top-200 kit row.
- **The point-guard plan stands.** Haliburton, Lillard and Irving were not
  re-derived (every source sits at or above the kit on their production;
  the kit's discount is games played). Irving's Yahoo listing is PG-only —
  he fills PG, G and Util, not SG — which the deck's slot feasibility now
  reads.
- **Centers move up as a class** on both planes (Hartenstein, Gobert, Edey,
  Zubac, Reid, Gordon on the kit; Duren, Clingan, Hartenstein on the deck):
  four of the six repriced rows were centers or bigs whose blocks had been
  inflating the pool mean. Expect the deck's BLK-family shelf to read a
  little deeper at the same turns.
- **Mobley's fall (19 → 34 kit, 12 → 21 deck) is a single assumption.** His
  free-throw percentage at .680 on 4.5 attempts costs about half a
  standard deviation of FT impact. If he shoots .72 again the row belongs
  back in the top 20; if he repeats .606 it belongs lower. Watch the first
  preseason week.

## 4. Deck build and publish

- Positions, lines and rows landed in `data/players.csv` (334 rows); roster
  evidence entries added for the four new placements
  (`data/rosters_official.json`); `verify_rosters.py` 334/334, zero
  mismatches, fallback-partial; freshness stamped 2026-09-29 with the
  pool-changes assertion.
- `build_deck.py`: all seven gates pass — planes 314 shared, team 0,
  exclusion 0, drift 0, **propagation 0, no waivers** (the nine deck lines
  moved with the kit's); market yahoo-2026-09-22.csv priced 296/334 (the four
  added rows are in the unpriced tail); pool sha `6efb01cd772b`; injection
  round-trip OK; colophon rewritten for this window (gate 6 checked locally
  before the build).
- Parity and suites: `check_parity.py` **EXACT MATCH** (169 owner turns
  across 13 committed states; 325 market ranks, 288 priced);
  `test_gates.py` 34/34; `test_draft.py` 62/62; `test_card.py` **61/61
  after a fixture repoint** — three D51R-4 cases replayed committed turns
  (state 51 #58, mock 32 #34 and #63) expecting an urgent structural
  TARGET read there; with Yahoo's wider eligibility the family shelves are
  fuller and no urgency fires at those turns any more (a scan of all 13
  committed states × owner turns finds three urgent reads, all withheld on
  availability). The gate itself is unchanged; the availability branch is
  now measured on state 54 #34 (Jaren Jackson Jr. at 0.78) and the behind,
  kept and non-urgent branches are pinned by calling the gate directly.
  Recorded in the suite's own docstring.
- DOM drive (`full_dom_check.mjs`, default TMPDIR, against
  `draft_state_54.json`): 127 assertions, 0 failed, 0 page errors, no
  crash, `"pass": true` —
  `arena/results/full_dom_check_2026-09-29_v33.json`.
- Publish: republished to the standing artifact URL after a fresh read of
  the live page (which was still v32, 330 rows) — **Version 33**, version
  id 1790707729-3a0f; the served page contains `docs/draft-deck.html`
  byte-for-byte inside the host's 355-byte head and 15-byte tail wrapper
  (checked on disk against the read-back). Deck record: branch
  `claude/rederive-0929`, commit 4f24423.

## 5. Gates (2026-09-29)

- Kit: `check_provenance.py` PASS · `rank_engine.py` 200 from 324 ·
  `check_report.py` PASS on this file · `check_derived.py` 10/10 (every
  dated artifact stays pinned to its own commit; this pass re-scopes nothing).
- Deck: `judgment_open_items.py --check-report` on this file: `receipts
  check PASS — all 11 flagged names carry a receipts row`.
- Cross-plane: `check_planes.py` 0/0/0/0 with the kit at
  `a5041cfc963b`; kit-only rows 10 (Drummond, Sensabaugh, Whitmore, Swain,
  Okorie, Kris Murray, Philon, McNeeley, Morez Johnson Jr., Ejiofor — the
  kit's deep rookies and camp bodies), deck-only 20 (Hield, Kispert,
  Russell, Finney-Smith, Vincent, Hardy, Vanderbilt, Valančiūnas, Clarkson,
  Hawkins, Strawther, Shamet, Lonzo Ball, Brogdon, Batum, Agbaji, Westbrook,
  Adams, Jackson-Davis, Tre Mann — resolver coverage for names the room
  drafts), both by design.

## Watchlist

- **Turner vs Ware (MIL).** Both rows now price Turner as the starter and
  Ware as the No. 2; the camp reporting says the job is open. The first
  preseason rotation decides which row is wrong; re-check after the first
  preseason game.
- **Poole (NOP).** Now priced as the third guard. If Fears or Murray sits
  in preseason and Poole starts, the row is too low; the next pull re-reads
  it. Either way he is no longer a card name.
- **Mobley's free throws.** .680 is a blend; the first preseason week
  moves it.
- **Beal (LAC, new kit row).** Knee inflammation on top of the hip; regular
  season not in doubt per reporting, preseason opener is. Re-check next
  pull.
- **Simmons (SAC, new rows).** First games since 2024-25; the ×0.78 tag is
  the availability read. A preseason DNP streak turns it into an exclusion.
- **Flemings (ATL, new rows).** Rookie backup point guard; the line is a
  tail estimate. Re-derive after the first two preseason games.
- **Trae Young and Tyler Herro.** The market intake's headline listed both
  among the rows the kit holds high on its own (kit 23.5 pts / 10.8 ast for
  Young vs RotoBaller 19.1 / 8.4; kit 24.5 / 5.5 for Herro vs 20.5 / 4.6),
  but D-M4 as written named neither, so neither was re-derived here —
  decision D-R1.
- **Yahoo price paste.** The deck's Mkt rank still runs on the 9/22 ADP
  file (7 days old at build); a fresh draft-analysis paste in early October
  re-prices the room and the survival chips.

## Open-item receipts

| item | query run (2026-09-29) | dated finding |
|---|---|---|
| (this pass) | no transaction sweep — same-day re-derivation on the 9/29 pull's verified pool; role research for the fifteen names above, plus one dedicated re-check per flagged name below (F1) | every flagged item quiet or unchanged; the 9/29 pull's verdicts stand (`after-report-2026-09-29.md` §8) |
| Jalen Duren | "Jalen Duren Pistons qualifying offer decision September 29" | HELD −0.08. Decision due Thursday 10/1; Detroit says it has "offered market value" and will not trade him (HoopsHype 9/29; NBC Sports; Yahoo); reported now expected to take the $9.6M qualifying offer (Yahoo; ESPN's McMenamin via Yahoo) — either branch resolves the card on 10/1 |
| Jalen Brunson | "Jalen Brunson Knicks first practice training camp September 29" | HELD −0.05. "Fully cleared", no restrictions as camp opened 9/29; 80–85 percent per ESPN's Goodwill (Hoops Rumors; Yahoo; ClutchPoints) — no first-practice report by run time |
| Brandon Ingram | "Brandon Ingram Clippers Achilles update September 29" | line re-derived here (§3a), tag and card unchanged: partial Achilles, out for the start, no timetable, "week-by-week" (NBC Sports; Washington Times 9/28; NBA.com) |
| Kristaps Porzingis | "Kristaps Porzingis Warriors out indefinitely update September 29" | veto unchanged. Out indefinitely, not on the Hawaii trip, Dunleavy not marking him out for the season start (NBC Sports; NBA.com; Hoops Rumors; CBS); one outlet quotes him naming the condition as POTS (boston.com 9/29) [SINGLE-SOURCE] |
| D'Angelo Russell | "D'Angelo Russell free agent signing September 29" | unsigned; waived 9/25, cleared 9/27, reported to prefer a contender (ESPN; NBC Sports; Hoops Rumors; ClutchPoints) |
| Cam Thomas | "Cam Thomas free agent unsigned September 29 training camp" | unsigned unrestricted free agent, "still waiting for an offer" (SI Nets; Yahoo; Yardbarker) |
| Jaden Ivey | "Jaden Ivey free agent signing news September 29" | unsigned; no signing reported; the fake "Lakers sign Ivey" post persists (EssentiallySports fact-check; RealGM; Spotrac) |
| Lonzo Ball | "Lonzo Ball free agent signing news September 29" | unsigned unrestricted free agent, no confirmed signing (Yahoo; heavy; Spotrac) |
| Jeremy Sochan | "Jeremy Sochan Trail Blazers training camp September 29 roster spot" | HELD −0.2. Camp opened 9/29 with him on the non-guaranteed minimum, fighting for the backup power-forward spot (SI Blazers; KGW; Rip City Project; Fanrecap) |
| Bennedict Mathurin | "Bennedict Mathurin Pelicans training camp September 29 role" | bench scoring behind Herbert Jones, media day 9/28; a starting spot "not out of the realm" (SI Pelicans; Yahoo camp preview; BVM 9/28) — line and card unchanged |
| Rob Dillingham | "Rob Dillingham waived Hornets signing claimed September 29" | waived 9/28, an unrestricted free agent Wednesday if unclaimed; no claim reported (RealGM; Hoops Rumors; NBC Sports 9/28; HoopsHype) — FA row and −0.10 card unchanged |

## Decision sheet (owner disposes)

| # | question | recommendation |
|---|---|---|
| D-R1 | Re-derive Trae Young and Tyler Herro the same way (the two names the market headline flagged that D-M4 did not list)? | yes, at the next pull; both are early-round rows where a 4-point gap moves a tier |
| D-R2 | Paste a fresh Yahoo draft-analysis page (ADP) in early October so the deck's Mkt rank, TARGET shelves and survival chips price the room the owner will actually draft in? | yes — the 9/22 file is the last price the deck has seen |
| D-R3 | Re-run a mock from seat 10 on v33 before the 10/14 draft to see which names the card now reaches at #87–#154? | yes — the late-round card will differ from mock 56's |

## Provenance and bounds

- Stat lines: Basketball-Reference player pages, opened directly this pass
  (`basketball-reference.com/players/…`: poolejo01, turnemy01, easonta01,
  johnsca02, braunch01, lopezbr01, wareke01, ingrabr01, mobleev01,
  cliffni01, simmobe01, rileywi01, colliza01, bealbr01). Flemings has no
  NBA line; his Houston line is from the NBA.com draft profile and Yahoo's
  signing report (sports-reference.com is blocked by the egress policy).
- Role reporting: search-summary reports from the named outlets, dated
  where the outlet dates them (Gazette 9/28, HoopsHype 9/28, NBA.com preview
  9/22, Bleacher Nation 9/25, ESPN 9/28, NBA.com 9/8). The environment's
  egress policy blocked direct fetches of sports.yahoo.com, si.com,
  gazette.com, cbssports.com, thedreamshake.com, behindthebuckpass.com,
  roundtable.io and crescentcitysports.com this pass; Basketball-Reference,
  NBA.com and ESPN opened. The pull protocol's garble caveat applies to the
  summaries; every line here rests on the directly-opened stat row plus at
  least two outlets agreeing on the role.
- Magnitudes are the author's ([SPECULATIVE] where labeled): the rows blend
  last season's actual line toward the reported role; they are not a
  computation. Argue with them.
- The deck's lines were set equal to the kit's re-derived lines on the same
  evidence (assumption A3 of the plan: the planes may differ by design, but a
  re-derivation from one evidence set yields one line).
- Board diffs: `board_diff.py` over `kit-top200-before.md` /
  `report/top-200-2026-27.md` and `hoops.py rank --top 340` before / after;
  the JSONs live in the session scratchpad, the counts above are copied
  from its output.
