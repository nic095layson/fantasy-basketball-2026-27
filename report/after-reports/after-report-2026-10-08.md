# After-report — 2026-10-08 data pull + deck v50

**Owner request (2026-10-08, verbatim):** "Good morning Claude! Please conduct refresh pull and
provide after report" — WO-3's daily pull.

Pull window: 2026-10-07 → 2026-10-08 (from Wednesday's pull, about 14:30 UTC on 10/7, to 14:17
UTC on 10/8: five preseason games played in it — Pacers–Timberwolves in Ames, Magic–Grizzlies,
Bucks–Thunder, Suns–Bulls and Warriors–Trail Blazers, all 10/7 — and six more tip tonight).
Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13
.. 2026-10-07`, exit 0 (no provenance row changed today, so the range end stands).

**Method.** The five box scores read from ESPN's own feed (scoreboard and summary endpoints,
the same host the verifier uses) before any search: starters, minutes, lines and DNP reasons
for every pool row that dressed, plus the summaries' own injury blocks (status, body part, the
feed's return estimate), cross-referenced to both planes by script (`scratchpad
pull1008/boxscores.txt`, `injuries.txt`). New today, the injury sweep's mechanical half: ESPN's
league-wide injuries feed (99 rows) diffed against the 49-row tag inventory in both directions
by script (`injuries_league.json`). Then one search sweep of 52 dated queries (34 standard, 8
extended for the five recaps and the four open questions, 10 standard for the carried items):
the ledger-shaped transaction check (Basketball-Reference's 2026-27 transactions page read
directly — 84 date blocks parsed, newest 10/6 — plus one search ledger), a dedicated query
for each of the ten flagged receipts, one team-shaped query for each of the seven teams in the
watch set (CHI, GSW, LAC, MIL, NOP, POR, TOR), the injury sweep in both directions, the
free-agent rows, the carried items (Strus, Harris, Lively, Beal, Knueppel, Bona, Brown Jr.,
Duren, Simmons, Monk, Keegan Murray, Acuff, Alexander-Walker, Dort, McCollum, Queta, Vincent,
Konchar, Steinbach vs Diabaté, Miller, White, Castle, the Lakers' four, Jerome vs Pippen Jr.,
Stewart, McConnell, Claxton, Collins). Direct fetches, all open: the Jazz's medical release on
NBA.com, NBA.com's 10/8 Starting 5 column and its 10/6 Coby White item, NBA.com's news index,
ESPN's roster API for all 30 teams (the verifier) and three rosters by hand (MEM, MIL, CHI),
ESPN's scoreboards 10/3–10/17 (the WO-5 count), ESPN's league injuries feed. Egress-blocked
today as on every pull: Yahoo, SI, CBS, RotoWire, Blazer's Edge, Golden State of Mind and the
other sports domains (their items rest on dated search summaries, labeled where they stand
alone).

## 1. Roster changes

One placement moved on the deck, by the lock's own rule; no tier or line moved on either plane.

| player | change | date | sources | applied? |
|---|---|---|---|---|
| Jordan Hawkins | MEM → CHI (two-way contract signed 10/6; ESPN's official roster feed now lists him on Chicago, 22 names, and no longer on Memphis, 20) | 2026-10-08 (feed) | ESPN roster feed (direct, 10/8); the 10/6 signing per NBA.com's release, SI Bulls, Bleacher Nation, Yahoo | **Yes** — deck `team` MEM → CHI by script; the D-1005-4 lock releases on the feed's own move, no owner input needed. Deck rank 250 of 319 draftable (unchanged), no kit row |
| Johni Broome | now on ESPN's Milwaukee feed (21 names) | 2026-10-08 (feed) | ESPN roster feed (direct); the Basketball-Reference ledger lists the 10/5 deal as an Exhibit 10 [SINGLE-SOURCE on the contract type: the ledger; Hoops Rumors and Yardbarker say the terms were not announced] | The by-name exemption ends: the verifier runs without `--allow-unmatched`, 335/335, 0 mismatches. DNP the 10/7 game, coach's decision |

Zero trades in the window: the ledger's 10/6 block is five camp moves (Pritchard signed and
McCray waived in Oklahoma City, Johnell Davis waived in Orlando, Terrell Brown in Utah,
Fletcher Loyer by the Clippers), its 10/5 block the Broome and Hawkins signings and the John
Butler waiver; the search ledger (ESPN's team transaction pages, Spotrac) carries nothing
dated 10/7 or 10/8. One injury with a pool effect, §4: Jusuf Nurkić's four-week
re-evaluation.

## 2. The five box scores (ESPN's feed; the lines rest on the box score where no outlet named them)

**Pacers 123, Timberwolves 112 (Hilton Coliseum, Ames).** Indiana started Siakam (19 min, 10),
Zubac (18 min, 6 / 3, 3 to), Nembhard, Nesmith (16 min, 19, 4-6 from three, all before
halftime) and **Haliburton** — his first game in 472 days since the Finals Achilles tear: 16
min, 7 pts / 6 ast / 2 blk, Indiana's first points (Yahoo, Star Tribune, AP, NBA.com Starting
5); Walker 28 min / 7 / 5 / 10 ast off the bench (team highs in minutes and assists), Huff 17
min / 16, Sheppard 22 / 13, Toppin 11 / 10, Oubre 10 / 5. T.J. McConnell did not dress —
"undisclosed, day-to-day" on the feed with a 10/10 estimate [SINGLE-SOURCE: ESPN feed].
Minnesota started McDaniels (21 min, 16, 4-6 from three), Kuminga (19 min, 2 on 1-9), Gobert
(19 min, 7 / 9), **LaMelo Ball** (20 min, 14 with four threes, 7 ast, 5 to; his second
Minnesota game after 11 / 4 / 3 on 10/5) and Edwards (20 min, 19, 4-5 from three, all in the
first half); Beringer 19 min / 8 reb, Dosunmu 17 / 10, Hyland 11 / 10 off the bench.

**Magic 122, Grizzlies 118.** Orlando's opener: Banchero (15 min, 11 / 5 ast), F. Wagner (14
min, 6 / 7 ast), W. Carter Jr. at C (15 min, 13, 3-4 from three), Bane (13 min, 9, 3-3) and
Jase Richardson (not a pool row, starting for Black) started; da Silva 25 min / 19 (the game
high) / 5 reb, 4-10 from three off the bench; **Vučević** 12 min / 9 off the bench behind
Carter; Bitadze 13 / 7. **Suggs** (illness, several days) and **Black** (the workout ankle
sprain) did not dress, both day-to-day on the feed with 10/11 estimates. Memphis started
Coward (22 min, 8 / 4 / 3), **Boozer** (22 min, 16 / 6, 6-7 FT), Wells (22 min, 6 on 2-10),
**Edey** at C — his first game since the ankle surgery, 10 minutes all in the first half, 2 /
4 / 1 stl / 1 blk; "short on wind", Iisalo's "best-case scenario" (Yahoo, SI Grizzlies, AP) —
and **Jerome** at the point (19 min, 17, the team high, 4 ast), with **Pippen Jr.** 14 min / 1
/ 3 stl off the bench: two starts in two games for Jerome. Hendricks 11 min / 12, GG Jackson 14
/ 15 / 6, Post 15 / 5 / 4 ast, Spencer 16 / 7 / 5 ast, Grant 20 / 3 off the bench; Stewart DNP
(the 10/5 fall, left ankle, day-to-day, 10/9 estimate).

**Bucks 128, Thunder 126.** Milwaukee started Jaquez (22 min, 13), **Turner** (22 min, 19, the
team high, 5 reb, 2 blk), **Ware** in Kuzma's spot (25 min, 18 / 12), Herro (23 min, 13, 3-6
from three) and **Rollins** (21 min, 12 / 3 / 7 ast on 5-7) — two starts in two games at the
point; **Porter Jr., Kuzma, LeVert, Trent Jr. and AJ Green were inactive with no injury
designation** (Yahoo/Brew Hoop; RotoWire and CBS on Kuzma); Burries 21 min / 16 / 5 / 2 stl
and on the floor for the finish, Jakučionis 18 / 10 / 4 / 4 off the bench; Broome DNP,
coach's decision. Oklahoma City started **Mara** at C again (25 min, 22 on 10-10, 6 reb, 1
blk, the only starter still playing after halftime), Caruso (17 min, 12, 4-6 from three),
**Gilgeous-Alexander** (18 first-half min, 17 on 5-5, 5 ast), **Jalen Williams** (19 first-half
min, 16 on 8-11, 6 ast, 2 stl — his first game back; Daigneault: "awesome") and Wallace (18
min, 7 / 6 ast); McCain 17 / 11 and Mitchell 17 / 3 / 5 ast / 4 to off the bench. Out:
**Holmgren** (rest on the feed, a quadriceps contusion per RotoWire alone, "likely
precautionary"), **Hartenstein** (ankle soreness — both exhibitions missed; the ankle that
kept him out of Germany's August qualifiers; next chance 10/12 at Atlanta) and Jaylin
Williams (heel), all day-to-day with 10/12 estimates.

**Bulls 124, Suns 117.** Chicago's opener: Jalen Smith at C with Claxton and Collins out (20
min, 13 / 8 / 2 stl), Buzelis (26 min, 14 / 2 stl / 2 blk, 0-6 from three), **Caleb Wilson** at
PF (29 min, the team high; 15 on 6-15, 0-4 from three, 3 / 2 — Bleacher Report, SI Bulls,
NBA.com), Powell (14 min, 14, 3-4 from three) and Giddey (23 min, 7 / 3 / 7 ast) started;
Okoro 17 / 2, Hield 15 / 8 off the bench; Hawkins DNP (coach's decision) in his first game on
the Chicago roster. Out: Claxton (as announced; the feed's estimate now 10/21), Collins (the
feed: right toe surgery, day-to-day, 10/9; one summary says quad — labeled), Tre Jones (left
hip soreness, 10/9). Phoenix started Brooks (23 min, 24 on 7-9, 7-8 FT, 5 to), **Bridges** —
left after 8 minutes (3 pts) with a right ankle injury from a loose-ball collision with
Powell, ruled out for the game; day-to-day on the feed with a 10/10 estimate, Ott: Saturday
vs San Antonio in play (CBS, Arizona Sports, Yahoo, Bright Side) — Ighodaro at C again (18
min, 8; Maluach 25 min / 8 / 7 / 4 off the bench, two games each), Booker (23 min, 11 on 3-14,
0-8 from three) and Jalen Green (22 min, 12 / 4 / 2 stl / 4 to); Dunn 23 / 4 / 5 / 2 stl,
Kennard 13 / 8 / 4, Goodwin 16 / 5 / 6 stl, Gillespie 14 / 12 off the bench; Mark Williams DNP
(out, 2027-02-03 on the feed).

**Trail Blazers 123, Warriors 118.** Portland's opener: Camara (19 min, 5), **Avdija** (21 min,
23 on 9-13, the game high), Clingan at C (20 min, 3 on 1-7, 10 reb), **Lillard** — his first
game since the Achilles tear: 19 min, 15, 3-8 from three, 2 stl — and **Morant** (19 min, 8
on 3-8, 5 ast, 4 to) in his Portland debut; the pair 8-19 with five turnovers, minus-9, Nori:
rough around the edges (Blazer's Edge, SI Blazers, Yahoo, KATU). **Holiday** off the bench as
flagged pregame (19 min, 5 / 7 / 5), **Sochan** 9 min / 10 on 4-6, all ten in the fourth
quarter from 90-90 (Yahoo, Golden State of Mind), Robert Williams III 14 min / 8 / 5 / 5 blk,
Yang Hansen 12 min / 6 / 4 ast (third center), Henderson 17 / 9, Krejci 14 / 3; Sharpe DNP
(out, 2027-03-02 on the feed). Golden State dressed nine on the second night of a
back-to-back: **Curry, Green, Lendeborg, Horford, Podziemski, Melton, Santos, Payton and Niang
all held out** (Yahoo, Golden State of Mind, Press Democrat, Roundtable), so Lendeborg's count
stays at two starts in two games; Brandon Williams (18 min, 17 on 7-11, 4 ast) and Will
Richard (33 min, 15, 3-3 from three, 6-6 FT) started with Leons, Bassey and Terry (23 / 8 / 9 /
4 stl in 43 min, not a pool row), Miles Kelly 24 off the bench (not a pool row); Butler and
Moody DNP, coach's decision; Porziņģis not with the travel group.

## 3. Flagged-item receipts (F1) — verdicts

| card | 10/8 finding | verdict |
|---|---|---|
| Brandon Ingram | no new item; out on ESPN's league feed with a 2026-11-01 estimate that is the feed's (the 9/28 items) | HELD −0.15 |
| Kristaps Porziņģis | not with the nine-man travel group at Portland; no new team statement; Kerr's 10/3 "day-to-day" framing in one outlet only | HELD, veto unchanged |
| Kawhi Leonard | no new item; sits 10/10 in Vancouver, could see action the week after (RotoBaller 10/2, NBC Sports 10/3, TSN) | HELD |
| Cam Thomas | unsigned, no dated item (Spotrac, RotoWire) | HELD |
| Jaden Ivey | unsigned, no dated item (Spotrac, SalarySwish) | HELD |
| Jeremy Sochan | first game: 9 min off the bench, 10 pts on 4-6, the fourth-quarter closer; the non-guaranteed deal still competes with Cissoko, Krejci and Potter (box score; Yahoo, Golden State of Mind, Sports Illustrated's Blazers site 9/28) | HELD −0.2, next box score |
| Lonzo Ball | unsigned, no dated item (RotoWire, Eurohoops) | HELD |
| Rob Dillingham | unsigned, no dated item (Spotrac, RotoBaller) | HELD |
| Bennedict Mathurin | game two tonight at Miami; no new item | HELD, WO-5 after game two |
| Ryan Rollins | started at the point again at Oklahoma City, 21 min / 12 / 7 ast on 5-7; Porter Jr. inactive with no injury designation; two starts in two games (box score; Yahoo/Brew Hoop, RotoWire, CBS) | HELD, WO-5 |

`judgment_open_items.py` on the re-authored page: 10 flagged, the same ten.

## 4. The carried items

- **Nurkić** — the Jazz's medical update (official release on NBA.com, 10/8 01:55 UTC): a
  partial plantar plate tear of the second toe of the right foot, sustained in the 10/4
  opener vs Denver, re-evaluated in four weeks; Haynes: a minimum of four weeks, a return
  around early November, the start of the season missed (CBS, SI Jazz, Bleacher Report,
  ClutchPoints, Yardbarker). The same shape as Strus on 10/5 (a four-week re-evaluation,
  the start of the season missed), which the owner's sheet carried as D-1005-2 with the
  exclusion as the default and the next pull applied. On the sheet as **D-1008-1**; the row's
  tier is unchanged today (deck rank 165 of 319, kit 172 — outside any 156-pick room either
  way), the note carries the finding. Hayes (deck 282), Filipowski (123, no return date on
  the back) and Jackson Jr. (23, tagged) are the center minutes.
- **Hawkins** — moved to Chicago on the feed (§1); D-1005-4 closed.
- **Broome** — on the feed; the exemption ends (§1).
- **Hartenstein** — ankle soreness has kept him out of both exhibitions; the ankle first kept
  him out of Germany's August qualifiers (RotoWire, Yahoo, SI Thunder, the feed); next chance
  10/12 at Atlanta. Untagged (deck 75, kit 102). On the sheet as **D-1008-2** (the White/Harris
  treatment by default).
- **Strus** — no new item; exclusion stands (D-1006-4 carried).
- **Claxton** — out for all five preseason games, re-evaluated two weeks from 10/5 (about
  10/19), the 10/21 opener in question (Hoops Rumors, RotoBaller, ClutchPoints); the feed's
  estimate moved to 10/21. D-1005-3 carried.
- **Tobias Harris** — out for the whole preseason with the left calf strain; Johnson: "totally
  questionable" for the 10/20 opener, reassessed after the five exhibitions (KSAT, RotoBaller,
  Spectrum News). D-1005-1 carried; first Spurs game tonight.
- **Lively** — no new item; Macao games 10/9 and 10/11; exclusion stands.
- **Beal** — no new item; the search returned the November 2025 hip fracture (garble).
- **Knueppel** — "a little more on-court work each day" (the coach, 10/4); re-check the week of
  10/19, his target the 10/21 opener; D-1002-1 holds.
- **Bona** — no new item before tonight's game at Brooklyn (the September items only).
- **Brown Jr.** — no new item before tonight; some contact work added 10/4, ruled out 10/6,
  "at some point in the preseason" per Fernández.
- **Suggs, Black** — sat Orlando's opener (illness; the workout ankle sprain), 10/11 estimates.
- **Edey** — played (§2); the tag stays by convention for the first season back.
- **Duren** — no new item; the ramp stands.
- **Simmons, Monk, Keegan Murray, Acuff** — tonight at the Lakers (Acuff's game two, D-1006-1's
  checkpoint); no new item before it.
- **Alexander-Walker, Dort, McCollum** — tonight at San Antonio; Dort (right knee contusion)
  and McCollum (nose contusion) game-time decisions on ESPN's injury page.
- **Queta vs Mitchell Robinson** — tonight at Cleveland; the Globe sees the minutes shared, NBC
  Sports has Robinson the reserve.
- **Steinbach vs Diabaté, Brandon Miller, Coby White** — no new item; Charlotte's next game
  10/11. White's calf strain is the 10/6 NBA.com/AP item (out for the preseason, the 10/21
  opener unclear); D-1006-2 carried.
- **Castle** — San Antonio's first game is tonight, the second 10/10 at Phoenix; the minutes
  re-check (D-CAST-2a) follows the second.
- **Vincent, Konchar** — unsigned; Konchar's "signs with the Knicks" items are the 9/15–16
  signing (waived 9/30, the ledger).
- **Jerome vs Pippen Jr.** — Jerome started both games (§2); WO-5 decides.
- **The Lakers' four** — tonight vs Sacramento; no new item before it.

## 5. Window sweep, team shadows, injury sweep

**Team shadows (7):** CHI — Hawkins on the roster, Claxton's timeline, Collins and Tre Jones
sidelined for the opener; GSW — the nine-man trip to Portland; MIL — the five inactive
regulars; POR — the opener; LAC, NOP, TOR — nothing beyond the items above.

**Injury sweep, both directions — now mechanical.** ESPN's league injuries feed (99 rows,
fetched 10/8) diffed against the 49-row tag inventory (16 excluded, 33 risk):

| direction | result |
|---|---|
| pool rows with status Out on the feed | 7: Ingram (tagged risk, carded), Strus, Moody, Mark Williams, Sharpe, DiVincenzo (all excluded) — and **Nurkić, the one untagged row with an Out status and a return date past opening night** (§4, D-1008-1) |
| tagged rows absent from the feed (candidates for "cleared") | 29: the nine `out-*` free agents and retirees (no team, not on any feed) and 20 risk rows — Morant, Jackson Jr., Edey, Haliburton, Lillard, Dejounte Murray, Zion, Murphy, Wells, Vanderbilt and the rest played or practice under their tags; none is re-tagged (the risk tag is kept by convention for the first season back) |
| untagged rows on the feed with Out or a return date after 10/21 | 1: Nurkić |

Day-to-day items on the feed for untagged rows (not tier questions): Hartenstein (10/12),
Holmgren (10/12), Bridges (10/10), Suggs and Black (10/11), Collins and Tre Jones (10/9),
Stewart (10/9), McConnell (10/10), Markkanen (expected back 10/12 per SI Jazz and Yardbarker),
Filipowski (no date).

**Garbles caught (search summaries and one fetch, logged, not used):** NBA.com's column at the
`starting-5-oct-8-ja-takes-flight…` slug is the **2025** 10/8 column (Morant "for the first
time in nine months" for Memphis, Castle fouling out in his debut, Hawkins 18 for the
Pelicans) — the 2026 column lives at `starting-5-october-8-2026` and was fetched instead; the
2022 Nurkić plantar fasciitis (the standard pass returned it before the 10/8 release); the
2025 Warriors–Blazers rest story and the 10/14/2025 Bucks–Thunder game; "LaMelo Ball's
Timberwolves debut" for the 10/7 game (the debut was 10/5); Edey's 2024 preseason debut vs
Dallas; Brandon Miller's May shoulder surgery and 2023 ankle; Beal's November 2025 hip
fracture; the 10/7/2025 McConnell hamstring; Konchar "signed with the Knicks" (the 9/15–16
signing, waived 9/30); "Kuminga landed in Atlanta" (he started for Minnesota, per the box
score); the 2025 Rollins recap (Cole Anthony, Giannis); Sofascore's "Gainbridge Fieldhouse"
for the Ames game; the "121-117" Bulls headline (the body and the box say 124-117); Dieng's
six vs seven assists; Collins' quad vs the feed's toe.

## 6. Board effects (computed, never eyeballed)

- **Kit:** `rank_engine.py` re-run, 200 of 321 projected (the four unsigned rows held off the
  board by the D-CAST-1 engine rule); the diff against the morning snapshot is the
  generation-date line only (2 lines of 206 differ, both the `*Generated …*` stamp). No rank
  moved. No kit row changed today (Hawkins has no kit row; Nurkić's kit row waits on
  D-1008-1).
- **Deck:** the draftable ordering recomputed from `data/players.csv` after the edits and
  diffed against this morning's snapshot (`scratchpad pull1008/deck_board_diff.json`): 319
  draftable before and after, 0 entries, 0 exits, 0 moves of three or more places, 0 value
  changes, 1 team change (Hawkins MEM → CHI). Notes do not move value; nothing else changed.

## 7. Deck build and publish

- `data/players.csv`: 151 notes appended (no row rewritten; every bracketed label sits ahead of its
  source parenthetical, so no note ends in `]` and the script asserts no note contains `];`,
  D-1006-3); one placement change, Hawkins MEM → CHI; no tag or line change; CRLF preserved
  (the committed file is CRLF; the first write was LF and showed as a full-file diff, 151 rows
  once the endings were restored).
- `scripts/verify_rosters.py` (no `--allow-unmatched`, the first run without an exemption since
  10/1): direct-complete, all 30 rosters, 335/335 matched, 0 mismatches, 0 unmatched.
- `hoops.py freshness --stamp`: 2026-10-08; the pool change described (one placement, 151
  notes); rosters verified direct-complete with no exemption.
- `JUDGMENT` re-dated 2026-10-08 with the ten receipts; colophon Data paragraph rewritten for
  the 10/8 window (gate 6 accepted it on the first build).
- `build_deck.py`: planes 315 shared · kit-only 10 · deck-only 20 · team 0 · exclusion 0 ·
  drift 0 · propagation 0, no waiver (the manifest's `waived` list is empty); 170 line
  differences by design; market `yahoo-2026-10-06.csv`, 246/335 priced, 2 days old; built 335
  players, pull 2026-10-08, pool `e03190d62399`, injection round-trip OK, "safe to publish".
- `check_parity.py`: PARITY: EXACT MATCH (312 owner turns across 24 committed states; 319
  market ranks compared, 241 priced). `test_card.py` 99/99, `test_gates.py` 37/37,
  `test_draft.py` 65/65. `full_dom_check.mjs` on `draft_state_54.json`: 130 assertions, 0
  failed, 0 page errors, pass true (`arena/results/full_dom_check_2026-10-08_v50.json`,
  committed).
- Published to the standing artifact URL as **Version 50** (version id 1791472393-27d5); the
  page's manifest reads built 2026-10-08, unmatched 0.

## 8. Gates (2026-10-08)

| gate | result |
|---|---|
| `report/check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07; exit 0 |
| `report/rank_engine.py` | exit 0; 200 of 321 projected (4 unsigned held off the board); board unchanged (date line only) |
| `scripts/verify_rosters.py` (deck, no exemption) | direct-complete, all 30 rosters, 335/335, 0 mismatches, 0 unmatched; exit 0 |
| `hoops.py freshness --stamp` (deck) | 2026-10-08, pool change described (one placement, 151 notes), rosters verified direct-complete |
| `scripts/build_deck.py` (deck) | gates 1–7 + F8 pass on the first run; planes 315 shared · team 0 · exclusion 0 · drift 0 · propagation 0 · no gate-7 exemption needed; round-trip OK; "safe to publish" |
| `scripts/check_parity.py` (deck) | PARITY: EXACT MATCH (312 owner turns, 24 states; 319 market ranks, 241 priced); exit 0 |
| `scripts/test_card.py` / `test_gates.py` / `test_draft.py` (deck) | 99 / 37 / 65 cases passed; exit 0 each |
| `arena/mocks/full_dom_check.mjs` (deck) | 130 assertions, 0 failed, 0 page errors, pass true; exit 0 |
| `report/check_report.py` | PASS — structure, publication rule, pull-log row; exit 0 (two rows reworded first: the gate's transaction heuristic matched a plane-exemption word in the build row and counted one lexicon outlet in the Sochan receipt) |
| `report/check_derived.py` | PASS — all 17 dated artifacts reproduce byte-for-byte; exit 0 |
| `scripts/judgment_open_items.py --check-report` (deck plane) | PASS — all 10 flagged names carry a receipts row; exit 0 |
| artifact publish | Version 50, id 1791472393-27d5, the standing URL |

## 9. Watchlist / open items

- **Tonight's six games** — CLE vs BOS (Queta vs Robinson; Tatum), MIA vs NOP (Mathurin's game
  two; Giannis), BKN vs PHI (Brown Jr.; Bona), WAS vs NYK, SAS vs ATL (Castle's and Harris'
  team's first game; Dort, McCollum, Alexander-Walker), LAL vs SAC (Acuff's game two; Simmons,
  Monk, Keegan Murray; Dončić, Reaves, Kessler, Sexton). Friday: DAL–HOU in Macao (Lively),
  MEM at CHI (Hawkins in his new building; Wilson vs Boozer).
- **WO-5, the projection refresh** — the trigger ("every team has played twice") lands later
  than the 10/9–10/10 estimate: on ESPN's schedule 9 teams have two completed games now, 16
  after tonight, 17 after Friday, 24 after Saturday 10/10, 29 after Sunday 10/11 and all 30
  only after Portland's 10/12 game vs the London Lions — one day before the 10/14 draft. On
  the sheet as **D-1008-3** (two passes by default: 10/11 and 10/13).
- **Nurkić** — D-1008-1; the Jazz's four-week re-evaluation lands about 11/4.
- **Hartenstein** — D-1008-2; next chance 10/12 at Atlanta.
- **Bridges** — right ankle, day-to-day; Saturday vs San Antonio the named chance.
- **Holmgren** — rest vs quad contusion; re-check on the 10/12 game.
- **Rollins, Jerome** — two starts in two games each; Porter Jr. and Pippen Jr. the losers so
  far; WO-5 decides the lines.
- **Lendeborg** — two starts in two games (held out in Portland); next game 10/10 vs
  Sacramento (D-1007-1 default: hold until WO-5).
- **Claxton, Harris, Knueppel** — re-evaluations about 10/19; the opener in question for all
  three.
- **Kawhi** — re-check after 10/10; the Knicks games the next named chance.
- **Strus, Lively** — exclusions stand; re-entry on two outlets reporting a cleared return.
- **The build regex trap** — D-1006-3; today's notes routed around it (no note ends in `]`,
  the script asserts it; Cardwell's note was not touched and still ends in `]`).
- **Market** — the Yahoo paste is two days old; the next is the owner's input.
- **Owner decisions carried:** D-BV1 (Butler), D-30-3, D58-2..D58-5, D-R1..D-R4, D-G2,
  D-G4..D-G7, D-P1..D-P4, D-1001-1/3, D-ADP-1/2, D40-1/3, D-LS-1/3, D-1002-1, D-1002-3,
  D60-1..D60-4, D61-1..D61-4, D62-1..D62-3, D-1005-1, D-1005-3, D-1006-1..D-1006-4, D-Y1..D-Y4,
  D-RW-1..D-RW-4, D-1007-1, D-CAST-2a/2b, D66-1, D67-1..D67-6, D-WI-1..D-WI-3.

## Open-item receipts

| player | query run | dated finding |
|---|---|---|
| Brandon Ingram | Brandon Ingram Clippers Achilles update October 8 2026 · ESPN league injuries feed (fetched) | no new item; the 9/28 partial-tear coverage only — NBC Sports, TSN, ABC30; the feed's 2026-11-01 estimate; HELD |
| Kristaps Porzingis | Kristaps Porzingis Warriors status update October 8 2026 · ESPN box score 10/7 (fetched) | not with the nine-man group at Portland; no new team statement; Kerr "day-to-day" 10/3 per Roundtable alone — box score, Yahoo, Roundtable; HELD |
| Kawhi Leonard | Kawhi Leonard Raptors preseason status October 8 2026 · Toronto Raptors news October 8 2026 | no new item; sits 10/10 in Vancouver, possible action the week after — RotoBaller 10/2, NBC Sports 10/3, TSN; HELD |
| Cam Thomas | Cam Thomas OR Jaden Ivey OR Lonzo Ball OR Rob Dillingham free agent signs October 8 2026 · NBA transactions October 8 2026 signed waived traded two-way · basketball-reference.com NBA_2027_transactions (fetched) | unsigned, no dated item — Spotrac, RotoWire |
| Jaden Ivey | (same queries) | unsigned, no dated item — Spotrac, SalarySwish |
| Jeremy Sochan | Jeremy Sochan Trail Blazers debut preseason October 7 2026 Warriors · Trail Blazers beat Warriors 123-118 … (extended) · ESPN box score 10/7 (fetched) | 9 min off the bench, 10 pts on 4-6, all in the fourth quarter — box score, Yahoo, Golden State of Mind; the roster math per SI Blazers 9/28; HELD |
| Lonzo Ball | (same free-agent queries) | unsigned, no dated item — RotoWire, Eurohoops |
| Rob Dillingham | (same free-agent queries) · ledger (fetched) | unsigned, no dated item — Spotrac, RotoBaller |
| Bennedict Mathurin | Bennedict Mathurin Pelicans Heat preseason October 8 2026 bench role · New Orleans Pelicans news October 8 2026 | game two tonight at Miami; the bench projections only — Yardbarker, Roundtable; HELD |
| Ryan Rollins | Ryan Rollins starting point guard Bucks Thunder preseason October 7 2026 · Bucks beat Thunder 128-126 … (extended) · Milwaukee Bucks news October 8 2026 · ESPN box score 10/7 (fetched) | started again, 21 min / 12 / 7 ast; Porter Jr. inactive, no designation — box score, Yahoo/Brew Hoop, RotoWire, CBS; HELD, WO-5 |
| Jordan Hawkins | Bulls beat Suns 124-117 … Hawkins (extended) · ESPN CHI + MEM + MIL rosters (fetched, direct) · verify_rosters.py direct-complete | on Chicago's feed (22), off Memphis' (20); DNP coach's decision 10/7 — ESPN roster feed, box score, SI Bulls, Bleacher Nation; moved |
| Johni Broome | Johni Broome Bucks Exhibit 10 contract October 2026 · ledger (fetched) · ESPN MIL roster (fetched) | on Milwaukee's feed (21); Exhibit 10 per the ledger, terms unannounced per Hoops Rumors/Yardbarker; DNP 10/7 — exemption ended |
| Jusuf Nurkić | Jusuf Nurkic foot injury re-evaluated four weeks Jazz October 2026 · Jusuf Nurkic re-evaluated in four weeks … Filipowski Markkanen update (extended) · nba.com/news/jazz-jusuf-nurkic-foot-injury (fetched) · ESPN league injuries feed (fetched) | partial plantar plate tear, right second toe, from the 10/4 opener; re-evaluated in four weeks — NBA.com release 10/8, CBS, SI Jazz, Bleacher Report, ClutchPoints, Yardbarker; D-1008-1 |
| Isaiah Hartenstein / Chet Holmgren / Jaylin Williams | Isaiah Hartenstein ankle Thunder Bucks preseason October 7 2026 … · Thunder Hartenstein ankle Holmgren sat out … (extended) · ESPN game feed 10/7 (fetched) | Hartenstein out both games, ankle soreness, 10/12 next; Holmgren rest (feed) vs quad contusion (RotoWire); Jaylin Williams heel — RotoWire, Yahoo, SI Thunder, ESPN feed; D-1008-2 |
| Kyle Kuzma / Kevin Porter Jr. / Caris LeVert / Gary Trent Jr. / AJ Green | Bucks Thunder preseason October 7 2026 recap … · Bucks beat Thunder 128-126 … (extended) | all five inactive, no injury designation; Ware in Kuzma's spot — Yahoo/Brew Hoop, RotoWire, CBS |
| Miles Bridges | Miles Bridges ankle Suns Bulls preseason October 7 2026 · Bulls beat Suns 124-117 … (extended) · ESPN game feed 10/7 (fetched) | right ankle after a loose-ball collision, 8 min, out for the game; Saturday in play per Ott — CBS, Arizona Sports, Yahoo, Bright Side, FantasyPros |
| Nic Claxton / Zach Collins / Tre Jones | Nic Claxton Bulls hamstring two weeks re-evaluated October 19 2026 · Zach Collins quad Bulls preseason October 7 2026 toe · Chicago Bulls news October 8 2026 · ESPN game feed 10/7 (fetched) | Claxton out for the preseason, re-check about 10/19, the opener in question — Hoops Rumors, RotoBaller, ClutchPoints; Collins toe (feed) vs quad (one summary); Jones hip — SI Bulls |
| Jalen Suggs / Anthony Black / Zach Edey / Ty Jerome / Isaiah Stewart | Magic Grizzlies preseason October 7 2026 recap … · Magic beat Grizzlies 122-118 … (extended) · Grizzlies Magic preseason Ty Jerome Scotty Pippen Jr. … Isaiah Stewart ankle · ESPN box score + game feed 10/7 (fetched) | Suggs illness, Black ankle, both 10/11; Edey's first game, 10 min; Jerome started again; Stewart DNP after the 10/5 fall — Yahoo, SI Grizzlies, CBS, AP via WREG, Yardbarker |
| Tyrese Haliburton / LaMelo Ball / T.J. McConnell | Pacers Timberwolves preseason October 7 2026 recap … · Pacers beat Timberwolves 123-112 … (extended) · T.J. McConnell Pacers undisclosed … · ESPN box score + game feed 10/7 (fetched) · nba.com Starting 5 10/8 (fetched) | Haliburton 16 min / 7 / 6 after 472 days; LaMelo 14 / 7 with four threes; McConnell undisclosed on the feed — Yahoo, Star Tribune, AP, NBA.com, Sofascore |
| Damian Lillard / Ja Morant / Jrue Holiday / Yang Hansen | Trail Blazers Warriors preseason October 7 2026 recap … · Trail Blazers beat Warriors 123-118 … (extended) · Portland Trail Blazers news October 8 2026 · ESPN box score 10/7 (fetched) | Lillard 15 in 19 min, Morant 8 / 5 with 4 to, Holiday off the bench, Hansen 12 min (box score only) — Blazer's Edge, SI Blazers, Yahoo, KATU, RotoWire, NBC Sports, NBA.com |
| Stephen Curry / Draymond Green / Yaxel Lendeborg / Al Horford / Brandin Podziemski | Warriors rest Curry Green Lendeborg Horford … · Warriors Trail Blazers preseason Wednesday … skeleton lineup (extended) · Golden State Warriors news October 8 2026 · ESPN game feed 10/7 (fetched) | all held out, nine dressed, the second night of a back-to-back — Yahoo, Golden State of Mind, Press Democrat, Roundtable; the feed: rest, 10/10 |
| Caleb Wilson / Devin Booker / Dillon Brooks | Bulls Suns preseason October 7 2026 recap … · Bulls beat Suns 124-117 … (extended) · nba.com Starting 5 10/8 (fetched) | Wilson 15 on 6-15; Booker 3-14; Brooks 24 on 7-9 — Bleacher Report, SI Bulls, Bleacher Nation, Sofascore, Bright Side, NBA.com |
| Max Strus | Max Strus Clippers foot update October 8 2026 · Los Angeles Clippers news October 8 2026 | no new item; the four-week re-evaluation a checkpoint — TSN, RotoBaller, ClutchPoints 10/5-6; exclusion stands |
| Tobias Harris / Stephon Castle | Tobias Harris Spurs calf Hawks preseason October 8 2026 Castle Wembanyama lineup | Harris out for the preseason, "totally questionable" for the opener — KSAT 10/5, RotoBaller, Spectrum News; Castle's first game tonight |
| Dereck Lively II | Dereck Lively Mavericks update October 8 2026 Macao | no new item; Macao 10/9 and 10/11 — TSN, RotoBaller, Roundtable; exclusion stands |
| Bradley Beal | Bradley Beal Clippers knee update October 8 2026 | no new item; the November 2025 hip coverage resurfaced (garble logged) |
| Kon Knueppel | Kon Knueppel hamstring update Hornets October 8 2026 | more on-court work each day (10/4); re-check the week of 10/19 — Roundtable, ClutchPoints, NBC Sports; D-1002-1 holds |
| Adem Bona | Adem Bona 76ers foot cleared update October 8 2026 Nets preseason | no new item; the September items — Eurohoops, NBC Sports Philadelphia, Inquirer |
| Mikel Brown Jr. | Mikel Brown Jr. Nets ankle 76ers preseason October 8 2026 | some contact 10/4, ruled out 10/6, "at some point in the preseason" — RotoBaller, Roundtable, ClutchPoints |
| Jalen Duren | Jalen Duren Pistons return timeline update October 8 2026 | no new item — RotoBaller, Field Level Media |
| Ben Simmons / Malik Monk / Keegan Murray / Darius Acuff Jr. / Luka Dončić / Austin Reaves / Walker Kessler / Collin Sexton | Kings Lakers preseason October 8 2026 Simmons Monk Keegan Murray Acuff Doncic Reaves Kessler Sexton status | nothing new before tonight's game — SI Kings, SI Lakers, RotoWire |
| Nickeil Alexander-Walker / Luguentz Dort / CJ McCollum | Hawks Spurs preseason October 8 2026 Alexander-Walker Dort McCollum status | Dort (knee contusion) and McCollum (nose) game-time decisions on ESPN's page — SI Hawks, Locked On |
| Neemias Queta / Mitchell Robinson | Celtics Cavaliers preseason October 8 2026 Queta Mitchell Robinson starting center Tatum | first game tonight; the Globe sees shared minutes, NBC Sports has Robinson the reserve — Boston Globe 10/5, NBC Sports 9/28, Hoodline |
| Gabe Vincent / John Konchar | Gabe Vincent OR John Konchar signs OR workout October 8 2026 · ledger (fetched) | both unsigned; Konchar's "signing" items are 9/15-16 (waived 9/30 per the ledger) — Heavy, Bleacher Report, RotoBaller |
| Hannes Steinbach / Moussa Diabaté / Brandon Miller / Coby White | Hornets Brandon Miller leg Steinbach Diabate Coby White update October 8 2026 · nba.com/news/coby-white-preseason-calf-strain (fetched) | no new item on the three; White's calf strain the 10/6 NBA.com/AP item — NBA.com, TSN, Spectrum News |
| (window ledger) | NBA transactions October 8 2026 signed waived traded two-way · basketball-reference.com NBA_2027_transactions (fetched, 84 date blocks) · nba.com/news (fetched) | 10/6 camp moves only (Pritchard, McCray, Davis, Brown, Loyer); 10/5 Broome (Exhibit 10), Hawkins (two-way), Butler waived; zero trades since 9/27 |
| (injury sweep) | NBA injury news October 8 2026 preseason · NBA injury report October 7 2026 preseason RotoWire CBS out day-to-day · NBA "cleared" OR "full participant" OR "returns to practice" OR "preseason debut" October 8 2026 · ESPN league injuries feed (fetched, 99 rows) | §5; the "cleared" query returned the September Haliburton/Brunson items; the feed diff found the one untagged Out row (Nurkić) |
| (preseason) | ESPN scoreboards 10/3–10/17 (fetched, direct) · five ESPN summaries (fetched) | five games in the window, six tonight, two Friday; the second-game dates per team in §9 |
| (team watch, 7) | "<Team> news October 8 2026" one each: CHI, GSW, LAC, MIL, NOP, POR, TOR | §5 |

## Bounds

- Direct-complete roster verification proves membership, not role; today it has no exemption
  (335/335, 0 mismatches after the Hawkins move).
- A preseason box score is a dated primary record, not a reprice mechanism (A1); the lines
  move at the WO-5 refresh after two games per team (D-1008-3 on the timing).
- Nurkić's tier is unchanged today by the sheet's precedent (D-1005-2: sheet one day, apply the
  default the next if silent); the row is outside any 156-pick room on both planes, so the
  one-day lag moves no draft board.
- Starting lineups and bench minutes for Indiana, Minnesota, Orlando, Memphis, Phoenix, Chicago,
  Portland and Golden State rest on the box score alone where no outlet named the lineup; every
  such row carries the `[SINGLE-SOURCE: box score]` label in the pool. Collins' quad (one
  summary) and Holmgren's quad (RotoWire alone) are labeled.
- The mechanical injury sweep reads ESPN's feed, which lists active designations only; a
  tagged row absent from the feed is a candidate for "cleared", not a finding — all 20 such
  risk rows were checked against the box scores and the sweep, and none is re-tagged.
- Yahoo, SI, CBS, RotoWire and most sports domains are egress-blocked; their items rest on
  dated search summaries, as on every prior pull; twenty garbles were caught (§5). NBA.com's
  pages and ESPN's API endpoints answer; one NBA.com slug served the 2025 column.
- The build's PLAYERS regex trap (D-1006-3) was routed around in data again, not fixed in code.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-1008-1 | Nurkić: a partial plantar plate tear of the right second toe, re-evaluated in four weeks per the Jazz's release (NBA.com 10/8; CBS, SI, Bleacher Report, ClutchPoints), the start of the season missed. The Strus shape: (a) re-tag `foot-recovery` on the deck (excluded, availability 0) and set the kit's GP to 25 (the exclusion twin, off the board), re-entry on two outlets reporting him cleared and playing; (b) a risk tier instead (`inj-foot-risk`, 0.78, kit GP cut to ~60); (c) hold untagged. Deck 165 of 319, kit 172 today — outside a 156-pick room either way | (a), applied at the next pull if silent |
| D-1008-2 | Hartenstein: ankle soreness has cost him both exhibitions and the August qualifiers (RotoWire, Yahoo, SI Thunder; the feed day-to-day, 10/12). Untagged, deck 75 / kit 102. (a) hold untagged until the 10/12 game, the White/Harris treatment; (b) `inj-ankle-risk` now (0.78; kit GP 66 → ~60) | (a) hold until 10/12 |
| D-1008-3 | WO-5 timing: "every team has played twice" lands 10/12 on ESPN's schedule (9 teams now, 16 tonight, 17 Friday, 24 Saturday, 29 Sunday, Portland last on 10/12), the day before the draft. (a) one pass on the 10/13 pull; (b) two passes — the first on the 10/11 pull for the 24 teams with two games after Saturday, the second on the 10/13 pull for the last six (HOU, DAL, CLE, ORL, CHA, POR), each with the diff table on both planes and the mock-67 room re-graded on the new lines | (b) two passes, 10/11 and 10/13 |
| D-1005-4 | Hawkins — **closed**: the feed moved him, the placement followed (no owner input needed) | — |
| D-1007-1 | Lendeborg's line: still two starts in two games (held out in Portland); carried | (a) hold until WO-5 |
| D-1006-1 | Acuff Jr.: game two tonight; carried | (a) hold until game two |
| D-1006-2 / D-1006-3 / D-1006-4 | Coby White tag; the build regex patch; Strus exclusion | carried: hold untagged / patch before WO-7 in a separate PR / keep the exclusion |
| D-1005-1 / D-1005-3 | Harris, Claxton tags — both now "the opener in question" with re-evaluations about 10/19 | carried: hold until ruled out of the opener / the 10/19 re-evaluation |
| D-1002-1 | Knueppel's tag | carried: hold until ruled out of the opener |
| D-1002-3 | camp first-unit signals: Rollins and Jerome now two starts each (Porter Jr. inactive, Pippen Jr. off the bench twice), Ware in Kuzma's spot once, Mara two starts with the bigs out, Ighodaro two starts over Maluach, Mathurin one game | carried: hold for WO-5 |
| D-CAST-2a / D-CAST-2b | Castle's minutes after San Antonio's second game (10/10); WO-5 proper per D-1008-3 | carried |
| D60-1..D60-4, D61-1..D61-4, D62-1..D62-3, D66-1, D67-1..D67-6, D-WI-1..D-WI-3 | the port's tie-break, Murray-Boyles, the advice-line wording, closing D-G3; the Lillard conviction, the Lendeborg passes, the advisor's lean; the real-seating baseline, the chips vs the cast; the v49 practice baseline; the mock-67 items; the what-if harness, the availability refit, the line date on repeat names | carried, owner silent |

## Provenance and bounds

- Inputs: ESPN's scoreboards (10/3–10/17) and five summary feeds (fetched 2026-10-08), ESPN's
  roster API for all 30 teams (fetched by the verifier) and three rosters by hand, ESPN's
  league injuries feed (99 rows); Basketball-Reference's 2026-27 transactions page (fetched
  2026-10-08, 84 date blocks); NBA.com's news index, the Jazz's Nurkić release, the 10/8
  Starting 5 column and the 10/6 Coby White item (fetched); 52 dated web-search summaries
  (2026-10-04 → 2026-10-08); the owner's request; the committed 10/07 pools and boards as the
  pre-pull snapshots.
- Every number in §2, §5 and §6 is a script run or a box-score read (`scratchpad pull1008/`),
  every gate line is the command's own output.
- Not verified: the Yahoo, SI, CBS, RotoWire, Blazer's Edge and Golden State of Mind articles
  (egress-blocked; headlines and search summaries only); nothing here rests on a direct read
  of a blocked sports domain.

## In plain language

**What this pull did.** One day since Wednesday's pull, and five more preseason games in it.
Before any news search I read all five box scores straight from ESPN's feed, including the
feed's own injury notes for each game, then swept the news, checked every player's team
against ESPN's live rosters for all 30 clubs, and rebuilt and republished the deck. New
today: I also pulled ESPN's league-wide injury list and had a script compare it against every
tag in the pool in both directions, so a player who is hurt but untagged, or tagged but
healthy, gets caught by the machine rather than by me remembering to look.

**The comebacks.** Haliburton played his first game in 472 days: 16 minutes, 7 points, 6
assists, two blocks, and Indiana's first basket. Lillard played his first game since his
Achilles tear: 19 minutes, 15 points, three threes, next to Ja Morant in Morant's first
Portland game. Edey started his first game since the ankle surgery and played 10 careful
minutes. Jalen Williams came back for Oklahoma City and scored 16 in a half. All of them keep
their risk tags for now, which is the pool's standing rule for a first season back.

**The one real injury.** Jusuf Nurkić has a torn plantar plate in a toe on his right foot. The
Jazz will look again in four weeks, which means he misses the start of the season. That is
exactly what happened to Max Strus last week, and the rule you set then was to take him off
the board until he is cleared. I have put the same question on your sheet (D-1008-1); if you
say nothing, he comes off both boards at tomorrow's pull. He sits at 165 on the deck and 172 in
the kit, so he was not going to be drafted in a 13-round room either way.

**What changed in the data.** One thing: Jordan Hawkins moved from Memphis to Chicago. The
deck follows ESPN's roster feed, the feed caught up with his two-way signing overnight, so
his row moved on its own rule. Johni Broome is on the feed now too, which means the roster
check passed with no exceptions for the first time in a week. No line moved, no tag moved.

**What the games said.** Rollins started at point guard for Milwaukee for the second game
running and Porter was inactive with no injury listed, so that battle is leaning Rollins. The
same for Ty Jerome over Pippen in Memphis. Milwaukee also held out Kuzma, LeVert, Trent and
Green, which put Kel'el Ware in the starting five and he had 18 and 12. Aday Mara went
10-for-10 for Oklahoma City with Holmgren and Hartenstein out. Hartenstein has now missed
both exhibitions with ankle soreness, the same ankle that kept him out of Germany's games in
August; that question is on your sheet too (D-1008-2), with the default to wait for Monday's
game before tagging him. Miles Bridges turned an ankle after eight minutes for Phoenix and
may be back Saturday. Golden State took nine players to Portland and rested everyone who
matters, so Lendeborg still has two starts in two games, not three.

**The projection refresh.** It starts when every team has played twice. On ESPN's schedule
that is later than I estimated: 24 teams will have two games after Saturday, and the last one,
Portland, plays its second game on Monday the 12th, one day before your draft. My suggestion
on the sheet (D-1008-3) is to run it in two passes, Sunday and Tuesday, so you have a
refreshed deck three days out and a final one the day before.

**What broke and what I did.** Nothing broke. The build passed on the first run and the
roster check needed no exception. One trap I caught: NBA.com's web address for the Oct 8
"Starting 5" column served last year's column, so I fetched the right one by its dated slug.
Nineteen other stale search results were caught and logged, none used.

**Verification.** The rebuilt deck passed every gate: the page and the Python agree exactly across 312 owner turns in 24 saved rooms, all 201 test cases pass, the browser robot drafted a full room with 130 checks and zero failures, the roster check matched all 335 players with no exception, and Version 50 is live at the usual link.

**Your decisions.** D-1008-1 Nurkić (default: off the board at the next pull). D-1008-2
Hartenstein (default: wait for Monday). D-1008-3 the refresh in two passes (default: yes).
D-1005-4 Hawkins is closed. Lendeborg, Acuff, Claxton, Harris, Knueppel, Coby White and the
regex patch are carried.

**Next.** Six games tonight, including Castle's and Harris' Spurs, Mathurin's second game,
Acuff's second game and the Lakers' regulars. Two on Friday. The first refresh pass on
Sunday if you agree.
