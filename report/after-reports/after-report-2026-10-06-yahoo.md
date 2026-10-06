# After-report — 2026-10-06: Yahoo's 10/6 page as the price source (deck v45) and as a projection line

**Owner input (2026-10-06, verbatim):** "Here are Yahoo's ADP and projected stat TOTALS as of
10/6:" — followed by Yahoo's player list in its projected-stats view, 250 rows.

Pull window: 2026-10-06 → 2026-10-06 (owner input, WO-4; not a roster pull — the 10/06 pull's
report stands).

**What it is (parser output).** A tab-separated table: for each player an abbreviated name
("N. Jokić", twice — the copy artifact the parser uses as its transcription check), a
game-status letter on 48 rows (Q, O or P), positions, team, then XRank, Yahoo's own **Rank**,
ADP (184 rows carry one, 66 show "-"), games played and nine projected **season totals**
(FG%, FT%, 3PTM, PTS, REB, AST, ST, BLK, TO). Two things in it are new to this system: a
per-game projection from the totals (total / GP), which is a third projection outlet beside
the kit's own lines and Hashtag's 9/30 page, and the Rank column, which on the evidence is
Yahoo's rank of its own projected line (Giannis XRank 6 but Rank 50 on a .638 FT% and 223
turnovers; Cunningham 5 and 25 on 277 turnovers; LeBron 40 and 92) — assumption A1, the
owner can correct it.

**Method.** The paste kept verbatim as `report/market/yahoo-raw-2026-10-06.txt`. A third raw
format added to `yahoo_market.py` (the first two untouched; the 16-artifact derived gate
still reproduces): invariants I1, I4–I6 and a new I7 — every abbreviated name resolves to
exactly one pool row by first initial and surname, with team and then positions as the
tie-breakers (the two "J. Williams" on Oklahoma City, the two "M. Bridges", "D. Mitchell",
"A. Thompson" and "K. George" all resolved by those rules; the resolutions were checked by
eye against the raw). 249 of 250 resolved; the one Yahoo-only name is Jordan Clarkson
(NYK, XRank 246, no ADP, no pool row). The canonical `yahoo-2026-10-06.csv` carries the
resolved full names so the deck's F8 price join works; `yahoo-proj-2026-10-06.csv` carries
the per-game line, the totals, Yahoo's Rank and the status letters. Joined under the hard
gate (76 pool players outside Yahoo's 250, all accepted absences by the mechanical check;
no spelling trips); consensus, unmatched and disagreements files written; provenance row;
registry entry; both commits pinned. The deck rebuilt on the new file (verify, stamp with
`--no-pool-changes`, build), the chain run, Version 45 published. The comparisons in §4–§6
computed in scratch over the committed CSVs and the v44 and v45 pages. No pool row changed
(fix F2).

**Headline.** Yahoo's expert rank did not move at all between the 10/01 and 10/06 pastes
(249 names in both, zero XRank changes); the room's ADP drifted modestly (Gafford 14 picks
later, Hachimura 8 later, Knueppel 5 later; DeRozan 8 earlier). The deck's Mkt column now
carries the 10/6 price on 246 of 335 rows (183 by ADP, 63 by XRank). Because this paste is
250 rows where the 10/01 one was 300, **51 rows lost their Yahoo price** and fall back to the
internal model — four of them with an ADP last week (Bronny James, AJ Green, Kennard,
Aaron Wiggins) and ten of them inside the deck's top 120 by value (Capela, Bitadze, Cam
Thomas, Ivey, Keon Ellis, Hield, Trent Jr., Hawkins, Alvarado, Risacher). That is D-Y1.
Yahoo's projected line, set against both planes on 246 shared rows, is closer to the kit
than to the deck (78 rows to 56, with 112 even; on points 88 to 44) — the same lean
Hashtag's page showed on 10/01, and no new decision: D-WO1-1's default stays the WO-5
refresh. Yahoo's own Rank is a fourth outside signal, and it splits the morning's 25
two-plane divergences: it sides with the board on Giannis (50), Banchero (118), Keyonte
George (121), Nurkić (213), Lopez (200), Bey, Pippen Jr., Hart and Eason, and against it on
Maluach (86), Harper (88) and Knueppel (23). The status letters are game-day designations
for tonight's slate (the whole Thunder core is "Q" for the Tulsa game), not season tags.

## 1. Roster changes

No roster changes — an intake, not a pull. Yahoo's team codes agree with the pool's verified
placement on all 249 joined names (§C of the disagreements file: 0 mismatches). No pool
row changed.

## 2. What landed

| file | what |
|---|---|
| `report/market/yahoo-raw-2026-10-06.txt` | the paste verbatim (1,299 lines) |
| `report/market/yahoo_market.py` | the table format: header-detected; I7 name resolution; the projection file; the (surname, initial) absence key |
| `report/market/yahoo-2026-10-06.csv` | 250 rows, resolved names, XRank, ADP — the deck's price source from this commit (pin `fe42b70`) |
| `report/market/yahoo-proj-2026-10-06.csv` | per-game line = total / GP (one decimal), the totals, Yahoo's Rank, GP, the status letter |
| `report/market/consensus-2026-10-06.csv` | the averaged consolidation (our rank, XRank, ADP) re-ranked over the pool |
| `report/market/unmatched-yahoo-2026-10-06.md` | 76 pool players outside the 250, each with its reason; stamp |
| `report/market/disagreements-yahoo-2026-10-06.md` | consensus top 30, values 42 / fades 81 vs ADP, 0 team mismatches, 5 availability disagreements, 1 coverage gap, what Yahoo changed since 10/01 |
| `report/market/provenance.csv` | the yahoo row for 2026-10-06 |
| `report/check_derived.py` | the registry entry (16 artifacts now) |
| deck `data/freshness.json`, `docs/draft-deck.html`, `arena/results/full_dom_check_2026-10-06_v45.json` | v45: priced by the 10/6 file; colophon market sentence rewritten; the step-5b result |

## 3. The price (WO-4)

- **Same expert rank, a slightly moved room.** 249 names in both pastes; XRank identical
  on every one. ADP on 183 of them both times: earlier for DeRozan (115.4 to 107.4),
  Ausar Thompson (88.1 to 83.7), Dejounte Murray, Suggs, Garland, Keyonte George,
  Rollins (79.0 to 76.4); later for Gafford (109.0 to 123.4), Hachimura (109.4 to 117.9),
  Knueppel (42.4 to 47.5), Wendell Carter Jr., Ingram (62.8 to 67.1), Porziņģis, Kawhi
  (30.4 to 32.8), Lillard, Jaylen Brown (27.0 to 29.3), Kessler. Cam Johnson gained an
  ADP (112.5); Morez Johnson Jr. lost his (116.6).
- **The deck's Mkt column, v44 to v45.** 246 of 335 rows priced (was 297): 183 by ADP, 63
  by XRank. Two rows moved by ten or more (Cam Johnson, 135 XR to 112.5 ADP; Gafford
  +14.4). 51 rows lost their price because the 250-row page ends where the 300-row page
  did not: four with an ADP last week (Bronny James 103.5, AJ Green 106.8, Kennard 107.5,
  Aaron Wiggins 110.6) and 47 XRank-only rows (251–299). Ten of the 51 sit inside the
  deck's top 120 by adjusted value — Capela, Bitadze, Cam Thomas, Ivey, Keon Ellis, Hield,
  Trent Jr., Hawkins, Alvarado, Risacher — and are now ordered by the internal model, as
  the F8 design says, with `mktsrc` empty so nothing is silently priced. No top-board name
  stranded on a spelling (the build's F8 check). D-Y1 asks whether to leave it or to
  paste the 300-row view.
- **Values and fades vs the fresh ADP (the disagreements file, §B).** Values: Jerome (our
  50, ADP 115), Daniels (9 / 64), Porziņģis (48 / 101), Butler (68 / 116), Ajay Mitchell
  (73 / 117), Hart (53 / 96), VanVleet (75 / 118), Collins, PJ Washington, Garland (24 /
  63). Fades inside our 140: Jaylen Brown (135 / 29), LeBron (142 / 37), then the deep
  tail the room prices and we do not (Mara, Poole, Drummond, Mikel Brown, Queta, Kuminga,
  Jaquez, Barrett, Kuzma, Porter). Availability disagreements (§D): Mark Williams,
  Butler, Lively, Strus, Sharpe — the room still prices all five; the pool excludes or
  discounts them by the owner's rules.

## 4. Yahoo's projected line against both planes (the D-WO1-1 third line)

| measure | value |
|---|---|
| shared rows (Yahoo line, kit line, deck line) | 246 |
| category inputs: closer to the kit / to the deck / tie | 550 / 440 / 1,224 (ties are the rows where the two planes' lines are identical) |
| by rows: kit closer on more inputs / deck / even | 78 / 56 / 112 |
| points: kit closer / deck closer; mean absolute error | 88 / 44; kit 1.47, deck 1.69 |

The widest points rows, all three lines: Morant (Yahoo 16.9; kit 23.5; deck 23.5), Duren
(18.5; 13.5; 12.5), Fox (18.2; 22.5; 24.0), Knueppel (20.8; 15.5; 16.5), Filipowski
(10.3; 15.0; 15.0), LaVine (17.0; 20.5; 22.5), Vučević (8.6; 13.0; 13.0), Wagler (12.1;
16.5; 16.5), Kuminga (11.6; 15.5; 16.0), Carrington, Collier, McCain, GG Jackson. Yahoo
reads Morant's Portland usage far below both planes, Duren's scoring far above, Knueppel's
above, and the Jazz, Kings and Bulls bench scorers below. Hashtag's page on 10/01 leaned
the same way (kit closer on points 79 to 47); two outlets now say the deck's points
column runs high on a set of mid-board names. That is evidence for the WO-5 refresh, not
an edit (D-WO1-1's default; bound A2).

**Games played.** Yahoo's GP runs well above the kit's on exactly the rows the owner
discounted on purpose: LeBron 66 (kit 55), Lillard 62 (45), Ingram 68 (48), Lively 50
(25), Strus 63 (25), Butler 35 (20), Sharpe 30 (18), Zion 64 (50). Below the kit's on
Simmons 15 (55), Bagley 49 (68), Robert Williams III 45 (60), Jović, Edey 60 (70), Cam
Johnson 56 (66). The kit's availability discounts are owner decisions (D-RT1–3, D-BV1);
Yahoo's are generic.

**Acuff Jr.** Yahoo projects 76 games, 17.1 points, 3.6 rebounds, 4.5 assists, 0.8
steals, 2.1 threes, 2.1 turnovers on .409 and .794 — the same role as the pool's 29-minute
line (16.7 / 3.1 / 5.0 / 1.0 / 2.6 turnovers on .430 / .820), with the shooting read lower
and the games read higher. XRank 155, ADP 109.6, Yahoo's own Rank 158; our 190. Nothing
here moves D-1006-1 off its default.

## 5. Yahoo's own Rank — a fourth outside signal on the 25 two-plane divergences

| measure | value |
|---|---|
| rho, Yahoo Rank vs the kit board (191 shared) | 0.789 |
| rho, Yahoo Rank vs the deck board (241) | 0.807 |
| rho, Yahoo Rank vs Yahoo's XRank | 0.861 |
| rho, XRank vs the kit board | 0.808 |

So Yahoo's projection-based rank is a different ordering from its expert rank (0.861),
and it sits about as far from the board as the expert rank does. On the morning's 25
names (kit / deck / XRank / Yahoo Rank):

| it sides with the board | it sides with the market | in between |
|---|---|---|
| Giannis (59 / 42 / 6 / **50**), Banchero (131 / 102 / 52 / **118**), Keyonte George (117 / 107 / 43 / **121**), Nurkić (175 / 167 / 105 / **213**), Lopez (191 / 171 / 160 / **200**), Pippen Jr. (136 / 134 / 183 / **135**), Bey (102 / 95 / 132 / **109**), Hart (53 / 68 / 97 / **68**), Eason (115 / 111 / 163 / **132**), Daniels (9 / 11 / 61 / **20** — closer to us than to its own experts) | Maluach (199 / 226 / 118 / **86**), Harper (171 / 148 / 83 / **88**), Knueppel (106 / 94 / 64 / **23**), Grant (118 / 113 / 193 / **206**), Caruso (130 / 131 / 196 / **199**), Coulibaly (122 / 133 / 203 / **231**), Vučević (128 / 124 / 177 / **240**), PJ Washington (77 / 88 / 133 / **178**), Nesmith, Gordon, Herb Jones, Filipowski | Black (184 / 178 / 146 / **123**), Dybantsa (173 / 141 / 92 / **151**), Grimes (170 / 159 / 126 / **129**) |

Reading it: where our board is low on a veteran because of availability or fit (Giannis,
Nurkić, Lopez, Banchero, George), Yahoo's own projected line agrees with us and its experts
do not; where our board is high on a low-usage stat-stuffer (Grant, Caruso, Coulibaly,
Vučević, Washington), Yahoo's projected line agrees with the market against us. The three
the market and Yahoo's line both put far above us — Maluach, Harper, Knueppel — are the
cleanest WO-5 candidates in the set. D-Y3 asks whether this column should join the
consensus file's signals; the default keeps it reference only.

## 6. The status letters against the tag inventory

48 rows carry a letter. **O** (out): Ingram, Butler, Mark Williams, Strus, Sharpe — every
one excluded or risk-tagged on the deck already. **P**: Peyton Watson. **Q** (42): the
Thunder's whole core (Gilgeous-Alexander, Holmgren, Jalen Williams, Hartenstein, Wallace,
Caruso — the Tulsa game tonight), the Lakers held out on 10/5 (Reaves, Sexton, Kessler), the
Kings' trio (Simmons, Monk, Keegan Murray), the 76ers' healthy inactives (Maxey, LeBron,
Embiid, Simons), Duren, Edey, Kawhi, Porziņģis, Knueppel, White, Claxton, Harris, Lively,
Beal, Suggs, Black, Brown Jr., Dort, McCollum, Filipowski, Aldama, Stewart, Nurkić,
Graves, Sensabaugh, Zach Collins, McConnell, Morez Johnson Jr., Jamal Murray, Alex Sarr.
Every Q on a tagged row is consistent with the tag; every Q on an untagged row is a
game-day hold the pull already carries as a note (A2 confirmed by the Thunder pattern).
Nothing here asks for a tag. One pool oddity surfaced on the way: T.J. McConnell's deck note
opens with `rookie-proj` (the text is about the rookie behind him); harmless to the
engine, a wording to fix at the next pull.

## 7. Deck build and publish

`build_deck.py` on 2026-10-06 (v45): roster verification direct-complete 334/335, 0
mismatches, Broome exempted by name; freshness stamped `--no-pool-changes` with the
price-refresh note; colophon market sentence rewritten ("Yahoo's own 10/6 ADP … 246 of the
335 rows priced"); planes 315 shared, team 0, exclusion 0, drift 0, propagation 0, no
waiver; market `yahoo-2026-10-06.csv`, 246 of 335 priced, 0 days old; pool `48456b3b18ff`
unchanged from v44. No engine, card or pool change; v45 differs from v44 in the Mkt column
and the colophon only.

## 8. Gates (2026-10-06)

| gate | result (evidence: the command's own output line) |
|---|---|
| kit `yahoo_market.py` transcription + join | format table: parsed 250 players (184 with ADP, 66 XRank-only); XRank gaps NONE; I7: 249 of 250 resolved; JOIN 325 pool players, matched 249, unmatched 76, spelling variants 0; GATE PASS |
| kit `check_derived.py` | all 16 dated artifacts reproduce byte-for-byte from their pinned inputs |
| kit `check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-10-06 |
| kit `check_report.py` on this file | REPORT GATE: PASS (structure, publication rule, pull-log row) |
| deck `judgment_open_items.py --check-report` on this file | receipts check PASS — all 10 flagged names carry a receipts row |
| deck `verify_rosters.py --allow-unmatched` | direct-complete via site.api.espn.com (all 30 rosters): 334/335 checked, 0 mismatches, 1 unmatched exempted by name (Johni Broome) |
| deck `build_deck.py` | deck built: 335 players · pull 2026-10-06 · pool 48456b3b18ff · injection round-trip OK; market yahoo-2026-10-06.csv priced 246/335 (Yahoo ADP else XRank), 0 days old; safe to publish |
| deck `check_parity.py` on the built page | PARITY: EXACT MATCH |
| deck `test_card.py` / `test_draft.py` / `test_gates.py` | CARD: all 89 cases passed / all 65 cases passed / all 37 cases passed (no code change on the deck this intake, so no red-first case) |
| deck step-5b `full_dom_check.mjs` on the built page | 128 assertions, 0 failed, 0 page errors, exit 0 (`arena/results/full_dom_check_2026-10-06_v45.json`) |
| artifact publish | Version 45 (id `1791311913-9c3b`) at the standing URL; page 398,123 bytes, sha256 `3d33a6e086c259af…`, identical to the built file |

## 9. Watchlist / open items

- **D-Y1** — the 51 rows that lost a Yahoo price (ten inside the deck's top 120 by value);
  a 300-row paste restores them.
- **WO-5** — Yahoo's per-game line joins Hashtag's as the second outside line on the 184
  D-WO1-1 rows; the three names both the market and Yahoo's own line put far above us
  (Maluach, Harper, Knueppel) head the list.
- **Acuff Jr.** — D-1006-1 unchanged; game two 10/8.
- **T.J. McConnell's deck note** — the `rookie-proj` opener to reword at the next pull.
- **Jordan Clarkson** — Yahoo's one name without a pool row (XRank 246, no ADP); no action.
- **The next Yahoo paste** — the draft is 10/14; a paste the morning of the draft is the
  WO-4 plan.

## Open-item receipts

| player | query run | dated finding |
|---|---|---|
| Brandon Ingram | the 10/6 Yahoo paste (parsed 2026-10-06) | status O; XRank 66, ADP 67.1 (4.3 later than 10/01), Yahoo's Rank 91, 68 games projected — the owner's Yahoo paste; the card's HELD stands (ESPN, NBA.com) |
| Kristaps Porzingis | the 10/6 Yahoo paste | status Q; XRank 152, ADP 101.3 (2.7 later), Rank 148, 55 games — the owner's Yahoo paste; veto and HELD unchanged (NBA.com, NBC Sports) |
| Kawhi Leonard | the 10/6 Yahoo paste | status Q; XRank 37, ADP 32.8 (2.4 later), Rank 15, 59 games — the owner's Yahoo paste; HELD (NBA.com, RotoWire for the ramp) |
| Cam Thomas | the 10/6 Yahoo paste | absent from Yahoo's 250 — the owner's Yahoo paste; unsigned (Spotrac, NBC Sports) |
| Jaden Ivey | the 10/6 Yahoo paste | absent from the 250 — the owner's Yahoo paste; unsigned (Spotrac, Heavy) |
| Jeremy Sochan | the 10/6 Yahoo paste | absent from the 250 — the owner's Yahoo paste; camp deal (Blazer's Edge, Yahoo) |
| Lonzo Ball | the 10/6 Yahoo paste | absent from the 250 — the owner's Yahoo paste; unsigned (Spotrac, Yahoo) |
| Rob Dillingham | the 10/6 Yahoo paste | absent from the 250 — the owner's Yahoo paste; FA (Hoops Rumors, RotoBaller) |
| Bennedict Mathurin | the 10/6 Yahoo paste | XRank 156, ADP 115.8, Yahoo's own Rank 282 on an 11.2-point, 65-game projected line — the owner's Yahoo paste; HELD, the Pelicans' first game tonight (SI.com, NBA.com) |
| Ryan Rollins | the 10/6 Yahoo paste | XRank 62, ADP 76.4 (2.6 earlier), Rank 58, 69 games at 17.6 points — the owner's Yahoo paste; HELD, game two decides (ESPN's feed, Brew Hoop for the 10/5 start) |

## Bounds

- A1: the Rank column is read as Yahoo's rank of its own projected line; the page's label
  was not in the paste. A2: the status letters are game-day designations.
- Per-game lines are totals divided by projected games, rounded to one decimal; percentages
  as pasted. They are Yahoo's projection, one outlet (F2).
- The cross-source and projection comparisons are scratch computations over committed
  CSVs and the two pages; the board is the 10/06 kit and the v44/v45 deck pool.
- The deck's unpriced tail is ordered by the internal model by design; the ten top-120 names
  in it are a consequence of the paste's depth, not of a spelling.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-Y1 | 51 rows lost their Yahoo price on the 250-row paste, ten of them inside the deck's top 120 by value (Capela, Bitadze, Cam Thomas, Ivey, Keon Ellis, Hield, Trent Jr., Hawkins, Alvarado, Risacher); they are model-ordered now. Leave it (the room prices none of them inside 250), or paste the 300-row view so they carry XRank again? | leave it; a deeper paste any time restores them |
| D-Y2 | Yahoo's per-game line leans the way Hashtag's did (kit closer on points 88 to 44; by rows 78 to 56). Fold it into the D-WO1-1 evidence for WO-5 as the second outside line? No edit now | yes, WO-5 evidence; no edit |
| D-Y3 | Yahoo's own Rank as a signal: keep it reference only (the consensus file averages our rank, XRank and ADP), or add it as a fourth signal in `yahoo_market.py` (a code change, red-first)? | reference only |
| D-Y4 | Acuff Jr.: Yahoo's line (76 games, 17.1 points, 4.5 assists, .409) reads the same role as ours with lower shooting — does it change D-1006-1? | no; hold until game two |
| D-RW-1..4, D-1006-1..4, D-1005-1/3/4, D-1002-1/3, D60-1..4 | carried | carried |

## Provenance and bounds

- Inputs: the owner's 10/6 paste (`yahoo-raw-2026-10-06.txt`, sha256 `7fe94a08…`); the
  committed pool and boards; `yahoo-2026-10-01.csv`, `hashtag-2026-09-30.csv`,
  `rotoballer-2026-09-29.csv`, `rotoworld-2026-10-05.csv`; the v44 page (git HEAD) and the
  v45 page.
- Every number is a script's output (`yahoo_market.py` at its pin; the scratch
  comparisons); every gate line is the command's own output.

## In plain language

**What this did.** Your Yahoo paste is now the price the deck reads. Every row's "Mkt"
number is Yahoo's ADP from 10/6, or its expert rank where the room has no ADP, so the
survival chips, the wait chain and the TARGET shelf run on today's room. Version 45 is
live at the usual link. Nothing else on the deck changed.

**Two new things in this paste.** First, Yahoo's projected season totals, divided by
games, give Yahoo's own per-game projection for 250 players. I set it against both of our
boards: it sits closer to the kit than to the deck, especially on points (88 names to 44),
which is exactly what Hashtag's page said last week. Two outside projections now agree
the deck runs a little hot on points for a group of mid-round names (Morant, Fox, LaVine,
Filipowski, Kuzma among them). That stays evidence for the projection refresh after two
preseason games, not a change today. Second, Yahoo's "Rank" column looks like Yahoo's
rank of its own projection, which is a different list from its expert rank. On the 25
names I flagged this morning where both our boards disagree with every outside source,
Yahoo's own projection takes our side on ten (Giannis, Banchero, Keyonte George, Nurkić,
Lopez and others) and the market's side on twelve. The three where the market and Yahoo's
line both sit far above us, Maluach, Harper and Knueppel, are the first names to re-check at
the refresh.

**One thing to know.** This paste is 250 rows; the last one was 300. So 51 players lost
their Yahoo price and are now ordered by our internal model instead, and ten of them are
inside the deck's top 120 by value (Capela, Bitadze, Cam Thomas, Ivey, Keon Ellis, Hield,
Trent Jr., Hawkins, Alvarado, Risacher). The room does not draft them inside 250, so the
effect is small, but a 300-row paste any time restores them (D-Y1).

**Acuff.** Yahoo's projection has him at 76 games, 17 points and 4.5 assists on .409
shooting. Same role as our line, lower shooting, more games. No change to this morning's
default.

**Your decisions.** D-Y1 (the deeper paste, default: leave it). D-Y2 (fold Yahoo's line
into the refresh evidence, default: yes). D-Y3 (Yahoo's Rank as a consensus signal, default:
reference only). D-Y4 (Acuff, default: no change). Everything earlier is carried.
