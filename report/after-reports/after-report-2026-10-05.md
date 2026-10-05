# After-report — 2026-10-05 data pull + deck v43

**Owner request (2026-10-05, verbatim):** "Good morning Claude! Please conduct daily
refresh pull, and provide after report in plain language" — WO-3's daily pull, the
first with preseason box scores in the window.

Pull window: 2026-10-02 → 2026-10-05 (from the Friday-morning pull's run time, 16:00
UTC on 10/2, to 18:35 UTC on 10/5: three days; three preseason games played in it —
Raptors–Heat 10/3, Jazz–Nuggets and Clippers–Warriors 10/4 — and five more tip after
this pull). Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows sourced;
verified 2026-07-13 .. 2026-10-05`, exit 0.

**Method.** The three box scores read from ESPN's own feed (scoreboard and summary
endpoints, the same host the verifier uses) before any search: starters, minutes
and DNP reasons for every pool row that dressed. Then one search sweep of 48 dated
queries (four re-run after a rate limit): the ledger-shaped transaction check
(Basketball-Reference's 2026-27 transactions page read directly, plus two search
ledgers), a dedicated query for each of the ten flagged receipts, one team-shaped
query for each of the seven teams in the watch set (CHI, GSW, LAC, MIL, NOP, POR,
TOR), the injury sweep in both directions against the 45-row tag inventory, the
free-agent rows, and the carried items (Lively, Beal, Knueppel, Bona, Brown Jr.,
Black, Dru Smith, the MEM cut-down, Alexander-Walker vs Dort, Queta's platoon,
Steinbach vs Diabaté, Konchar/Vincent/Broome/Bradley, Yang Hansen, Herro, Edey,
Duren, Simmons, Tobias Harris, Strus, Claxton). Direct fetches: Basketball-Reference
(the ledger and Yang Hansen's player page, both open), NBA.com's news index (open),
ESPN's roster API for all 30 teams (the verifier) plus Memphis, the Clippers and
Portland read by hand; ESPN's Hawkins article returned an empty body — CANNOT VERIFY
through it. Edits applied by script with exact-match assertions (`scratchpad
pull1005/deck_edit.py`, the kit rows appended by script), both boards diffed by
script against the pre-pull snapshots, the deck built through gates 1–7/F8 and driven
end to end by the step-5b browser gate. Four search-summary garbles caught and logged
(§4).

**Headline.** The first box scores say what the camp reads said. Yaxel Lendeborg
started Golden State's opener at small forward (19 minutes); Isaiah Jackson started
at center for the Clippers with Brook Lopez playing seven minutes off the bench;
Jaren Jackson Jr. started his first game since the knee surgery; Kawhi, Porziņģis
and Jamal Murray sat; Beal did not dress. The window's two injuries on pool rows are
Max Strus (left the opener after five minutes, right foot, testing pending) and Nic
Claxton (hamstring, out for the preseason); Tobias Harris is out for the preseason
with a calf strain and questionable for the opener. One reported move on a pool row,
Memphis waiving Jordan Hawkins, is not yet on ESPN's official roster feed, so his row
stays on MEM under the roster validation lock with the report on it. One row was
added on both planes: Yang Hansen, the D59-3 default. No placement, tag or line
changed on an existing row. Deck v43 built and published.

## 1. Roster changes

| plane | change | count |
|---|---|---|
| both | **Yang Hansen added** (POR, C) — the D59-3 default from the 10/01 sheet, applied as that sheet said (a public room drafted him at #126 with no pool row; two outlets on his role). Role: third-string center behind Clingan and Robert Williams III per the GM, "developmental reserve", G League minutes likely (Yahoo, Rip City Project). Line **[ESTIMATED]** from his 2025-26 base (43 GP, 7.0 mpg, 2.2 / 1.5 / 0.5 on .310 — Basketball-Reference) at about 8 minutes: 40 GP, 2.5 pts / 1.8 reb / 0.6 ast / 0.1 stl / 0.3 blk / 0.7 tov on .420 and .750; LIKELY direction, SPECULATIVE magnitude; identical on both planes. ESPN's Portland roster lists him (direct check) | 1 |
| deck | **Jordan Hawkins — reported waived, placement held.** ESPN/Shams, NBC Sports, Hoops Rumors and Yahoo report Memphis waived him in its roster crunch (10/4–5, $7M guaranteed). ESPN's official roster feed still listed him on Memphis at the 18:42 UTC direct check, and the verifier refuses an FA row that sits on an official roster, so his team stays MEM with the report in his note; he moves to FA the pull the feed or the ledger reflects it (D-1005-4) | 0 |
| deck | Notes only, no tier change (twenty rows): Strus (left the 10/4 opener after 5 minutes, non-contact right foot injury, further testing in Los Angeles, no diagnosis — box score; Hoops Wire, RotoWire, Yahoo, BVM 10/4); Claxton (hamstring, re-evaluated in two weeks, out for the preseason — CBS Sports, RotoWire, Yahoo); Tobias Harris (left calf strain, out for the preseason, questionable for the 10/20 opener — NBA.com 10/4, ESPN, KSAT 10/5, Yahoo); Lendeborg, Isaiah Jackson, Lopez, Beal, Kawhi, Porziņģis, Jamal Murray, Jaren Jackson Jr., Filipowski (the 10/3–10/4 box scores, with dated outlets on each); Edey (held out of the opener, on track for 10/21 — RotoBaller, RotoWire, CBS Sports); Duren (game-time decision, undisclosed; missed Saturday's open practice — SI Pistons, RotoWire); Simmons (cautious ramp-up, targeting 10/8 or 10/10 — RotoWire, Bleacher Report); Bona (not cleared — RotoWire, CBS Sports); Brown Jr. (taking contact, next chance 10/8 — RotoWire, Hoops Rumors); Knueppel (trending positively per Lee 10/4 — Yahoo, SI Hornets); Black (practiced Sunday, "pretty close" — RotoWire, CBS Sports, Hoops Rumors) | 20 |

Two-source rule: every note carries two or more dated outlets or the box score as the
primary record plus one; the one single-outlet fragment (Filipowski's "lower back")
is labeled `[SINGLE-SOURCE]` in the row. The roster evidence file was rewritten by
the direct verifier (all 30 rosters).

## 2. Flagged-item receipts (F1) — verdicts

- **Ingram — HELD −0.15.** No new item; "Out" on ESPN's feed (ESPN, NBA.com,
  Bleacher Report).
- **Porziņģis — HELD −0.10, veto unchanged.** DNP "not with team" on the 10/4 box
  score; Dunleavy's "not marking him down as out to start the season" is the last
  team statement (box score; Yardbarker, Golden State of Mind).
- **Kawhi — HELD −0.05.** Held out of the 10/3 opener, no contact work yet, expected
  to miss the 10/10 Vancouver game too (box score; HoopsHype 10/3, CTV News, Yahoo).
- **Cam Thomas, Ivey, Lonzo Ball — HELD, all unsigned** (NBC Sports, Spotrac, Hoops
  Wire, Yahoo; the "Bucks sign Cam Thomas" item is February 2026 again, the Lonzo
  "traded to the Jazz" item is 2025).
- **Dillingham — HELD −0.10.** Unsigned, any team but Chicago (Fox Sports, Spotrac).
- **Sochan — HELD −0.2.** Still on the camp deal, in the roster bubble watch;
  Portland's first game 10/7 (SI Blazers, Yahoo).
- **Mathurin — HELD −0.05.** Presumptive sixth man; the Pelicans' first game is 10/6
  at Oklahoma City (SI Pelicans, Fox 8).
- **Rollins — HELD −0.05.** Projected to start tonight's opener vs Minnesota with
  Porter not in the projected five (Canis Hoopus, Yahoo primer); the game tips after
  this pull — the box score decides at the next pull.

## 3. The carried items

| item | finding (dated) | outlets | action |
|---|---|---|---|
| Lively (excluded) | not cleared, no setbacks, misses Macao (10/9), 10/21 undetermined | Yahoo, Mavs Moneyball/ESPN, CBS Sports | exclusion stands |
| Beal | did not play 10/4 (knee); day-to-day on ESPN's feed; spoke about the hip recovery | box score; Yahoo, Hoops Rumors Clippers Notes | note; `inj-hip-risk` stays |
| Knueppel (D-1002-1) | "trending positively", more on the court each day per Lee 10/4; out for the preseason; not ruled out of the opener | Yahoo, SI Hornets | note; the sheet's default holds |
| Bona | not cleared, out tonight; Nurse optimistic for some preseason | RotoWire, CBS Sports | note |
| Mikel Brown Jr. | taking contact; out 10/6, next chance 10/8 | RotoWire, Hoops Rumors | note |
| Anthony Black | practiced Sunday, "pretty close"; opener 10/7 | RotoWire, CBS Sports, Hoops Rumors | note |
| Dru Smith | unchanged, "a couple of weeks" | NBC Sports, HoopsHype | no change |
| MEM cut-down | Hawkins waived per the outlets (placement held, §1); Clayton, Kris Murray and Peavy all still on ESPN's 21-man feed | ESPN/Shams, NBC Sports, Hoops Rumors; ESPN roster (direct) | fourteenth pull carried; Kris Murray's kit row stands |
| Alexander-Walker vs Dort | Dort and McCollum both to get preseason starts for Snyder to assess; ATL–MEM tonight | SI Hawks [SINGLE-SOURCE] | no change |
| Queta vs Robinson (BOS) | Queta expected to remain the starter; opener 10/8 | Yahoo/Keith Smith, SI Celtics | no change |
| Steinbach vs Diabaté (CHA) | no decision; Charlotte's first game is 10/6 — the "Diabaté logs 11 in a preseason start" item is 2025 (garble) | SI Hornets, Last Word | no change |
| Konchar, Vincent, Broome, Bradley | Konchar unsigned since the 9/30 waiver; no Heat offer for Vincent; Broome unsigned; Bradley still not on ESPN's feed, exempted again | Hoops Rumors, SNY / Yahoo / Spotrac / Hoops Rumors, Yardbarker | FA rows stand |
| Edey | unlikely to play tonight, precaution; on track for 10/21 | RotoBaller, RotoWire, CBS Sports | note; tag kept |
| Herro | full camp participant; first game tonight | RotoWire, CBS Sports | no change |
| Duren | game-time decision (undisclosed) tonight; missed Saturday's open practice | SI Pistons 10/5, RotoWire injury report | note |
| Jaren Jackson Jr. | started 10/4, 18 minutes, 11 points — first game since the PVNS surgery | box score; Deseret, Salt Lake Tribune | note; `inj-knee-risk` kept by the first-season-back convention |

## 4. Window sweep, box scores, team shadows, injury sweep

- **Transactions (F5 ledger check).** Basketball-Reference's 2026-27 transactions
  page, read directly: nothing dated 10/2–10/5; the newest entries are three 10/1
  waivers (Utah, Houston, Chicago). Zero trades in the window. Minor moves on no pool
  row: Washington signed Gortman and waived Settle (10/3), Orlando signed
  Sharavjamts, Toronto signed Degenhart and waived Andre Jackson Jr. (10/5 — Hoops
  Rumors). The Hawkins waiver (§1) is the one reported move on a pool row.
  **Garbles logged:** (1) one summary said Beal "played and drove to the basket" on
  10/4 — the box score has him not dressed, and Yahoo and Hoops Rumors say he did not
  play; (2) "Hornets' Diabaté logs 11 in a preseason start" (CBS) is October 2025 —
  Charlotte has not played; (3) "Bucks sign Cam Thomas" is the February 2026 deal, a
  fourth time; (4) "Lonzo Ball traded to the Jazz, to be waived" is a 2025 item.
- **Box scores (ESPN summary feed, primary).** 10/3 TOR–MIA (MIA 129–105): Poeltl
  started, 18 min, 9 pts; Murray-Boyles 20 min, 6 pts / 9 reb; Shead 28 min; Kawhi
  did not dress; for Miami, Giannis, Wiggins, Adebayo and Davion Mitchell started,
  Larsson 11 min / 13 pts, Jović 17 min / 11 pts. 10/4 UTA–DEN (UTA 109–97):
  Markkanen 14 min / 17 pts, Jaren Jackson Jr. started 18 min / 11, Keyonte George
  21 min / 15, Peterson started 19 min / 3, Nurkić started; Ace Bailey 20 min / 10;
  Filipowski and Sensabaugh DNP; Jokić 15 min / 3 pts / 7 ast; Jamal Murray DNP
  (personal); Strawther 20 min / 14. 10/4 LAC–GSW (LAC 104–101): Lendeborg started
  19 min / 4 pts / 9 reb / 3 ast; Curry 13 min / 10; Podziemski, Horford, Green
  started; Butler, Moody, Porziņģis DNP; for the Clippers Garland, Hachimura (21
  pts), Jones Jr., Strus (5 min, left) and Isaiah Jackson started, Lopez 7 min off
  the bench, Wagler 30 min / 15 pts (the game-winner), Beal not dressed.
- **Roster verification went direct again.** ESPN's roster API answered for all 30
  teams: 334 of 335 pool rows matched (the new row included), zero mismatches; Tony
  Bradley the one unmatched row, exempted by name with the same three outlets.
- **Team shadows.** CHI (Claxton out for the preseason; Stevens signed, Suder waived,
  not pool rows; first game 10/7 — Bleacher Nation, Sun-Times), GSW (the Honolulu
  loss; Kerr on Lendeborg's aggression — NBC Sports Bay Area, Yahoo), LAC (Strus
  testing; Beal out; Jackson over Lopez — Hoops Rumors Clippers Notes, SI Clippers),
  MIL (opener tonight; Rollins projected to start — SI Bucks, Canis Hoopus), NOP
  (opener 10/6 at OKC; Murray, Zion, Murphy locks to start — WWL, Fox 8), POR (Fan
  Fest; first game 10/7; the guard logjam — SI Blazers, KPTV), TOR (the Quebec City
  loss; Kawhi's two-game ramp — TSN, Raptors Republic).
- **Injury sweep vs the F6 tag inventory (11 excluded, 34 risk).** Tagged and
  progressing, tags kept by convention: Jaren Jackson Jr. (played), Edey (held out
  as a precaution), Simmons (ramp-up), Haliburton, Embiid, VanVleet, Adams, Curry
  (played 13 min), Paul George, Kessler. Still out, tags kept: Butler, Moody,
  Porziņģis, Mark Williams, Sharpe, Ingram, Lively. Returning-but-untagged: Herro
  (full participant), Giddey, Brunson, Sabonis — none needs a tag. New items on pool
  rows: Strus, Claxton, Tobias Harris (§1); Filipowski (DNP, lower back per one
  outlet); SGA sat Tuesday's opener as rest (RotoWire) — no tag. Not pool rows: Tacko
  Fall, Thomas Sorber, Spencer Jones, Grant Williams.
- **FA rows.** Kit: Cam Thomas, Ivey, Dillingham, Broome, Konchar unsigned. Deck adds
  Lonzo, Vincent and the retired/overseas rows; all on no ESPN roster.

## 5. Board effects (computed, never eyeballed)

- **Kit.** `top-200-2026-27.md` regenerated against the pre-pull snapshot after the
  one added row: Royce O'Neale enters at 200, Taylor Hendricks exits; one move of
  three or more (Cam Thomas 136 to 133); 75 one- or two-place displacements, among
  them the exact tie at ranks 5 and 6 (Towns and Maxey, both +4.56 / +4.02) flipping
  to Towns first. Mechanism: the engine's z-scores run over an iterated top-180
  pool, so one added row shifts the means and spreads by a hair and re-breaks ties;
  no line changed. Yang Hansen himself ranks outside the top 200.
- **Deck.** By adjusted value over the draftable rows (323 to 324): Yang Hansen enters
  at 324, the last draftable row; no exits, no moves, no one- or two-place
  displacements. Pool sha256 `7729dd246981` (was `75a4994b4a59`); 335 rows.

## 6. Deck build and publish

`build_deck.py` on 2026-10-05: roster verification direct-complete, 334/335 against
all 30 official rosters, 0 mismatches, 1 exemption by name; freshness stamped with
the pool-changes note; JUDGMENT re-dated 2026-10-05 — the ten open cards re-authored
with this pull's receipts, none added or removed, all ten still flagged by the
enumerator; colophon Data paragraph rewritten for the window; planes 315 shared,
team 0, exclusion 0, drift 0, propagation 0, no waiver; market
`yahoo-2026-10-01.csv`, 297 of 335 priced, 4 days old. No engine or card change this
pull; v43 differs from v42 in data and prose only.

## 7. Gates (2026-10-05)

| gate | result (evidence: the command's own output line) |
|---|---|
| kit `check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-10-05 |
| kit `check_derived.py` | all 13 dated artifacts reproduce byte-for-byte from their pinned inputs |
| kit `check_report.py` on this file | REPORT GATE: PASS (structure, publication rule, pull-log row) |
| deck `judgment_open_items.py --check-report` on this file | receipts check PASS — all 10 flagged names carry a receipts row |
| deck `verify_rosters.py` | direct-complete via site.api.espn.com (all 30 rosters): 334/335 checked, 0 mismatches, 1 unmatched exempted by name (Tony Bradley) |
| deck `check_planes.py` (in the build) | 315 shared · team 0 · exclusion 0 · drift 0 · propagation 0 · no waiver · lines 171 (warning by design) |
| deck `build_deck.py` | deck built: 335 players · pull 2026-10-05 · pool 7729dd246981 · injection round-trip OK; safe to publish (market `yahoo-2026-10-01.csv`, 297 of 335 priced, 4 days old) |
| deck `check_parity.py` on the built page | PARITY: EXACT MATCH |
| deck `test_card.py` / `test_draft.py` / `test_gates.py` | CARD: all 89 cases passed / all 65 cases passed / all 37 cases passed (no code change this pull, so no red-first case) |
| deck step-5b `full_dom_check.mjs` on the built page | 128 assertions, 0 failed, 0 page errors, exit 0 (`arena/results/full_dom_check_2026-10-05_v43.json`) |
| artifact publish | Version 43 (id `1791227061-5465`) at the standing URL; page 388,368 bytes, sha256 `1fea555fcbfcd292…`, identical to the built file |

## 8. Watchlist / open items

- **Tonight's five games** — ATL–MEM (Alexander-Walker vs Dort; Edey held out; the
  Memphis cut-down), DET–PHX (Duren a game-time decision), PHI–NYK (Bona out; Tony
  Bradley's camp fight), MIL–MIN (Rollins vs Porter; Herro's first game), SAC–LAL
  (Simmons held out). The next pull reads their box scores.
- **WO-5, the projection refresh** — starts when every team has played twice; six
  teams have one game, sixteen play their first tonight or tomorrow; the earliest
  that threshold lands is about 10/9–10/10.
- **Strus** — a diagnosis is the next item (D-1005-2).
- **Hawkins** — moves to FA the pull ESPN's feed or the ledger reflects the waiver
  (D-1005-4).
- **Claxton, Tobias Harris** — re-evaluation dates about 10/19 and after 10/16
  (D-1005-3, D-1005-1).
- **Lively** — back to the draftable pool when two outlets report him cleared.
- **Knueppel** — D-1002-1 stands; the trigger is a ruling-out for the 10/21 opener.
- **Owner decisions carried:** D-BV1 (Butler), D-30-3, D58-2..D58-5, D-R1..D-R4,
  D-G2, D-G4..D-G7, D-P1..D-P4, D-1001-1/3, D-ADP-1/2, D40-1/3, D-LS-1/3, D-1002-1,
  D-1002-3, D60-1..D60-4; D59-3 closed today (default applied).

## Open-item receipts

| player | query run | dated finding |
|---|---|---|
| Brandon Ingram | Brandon Ingram Clippers update October 5 2026 | out for the start of the season, no timetable; "Out" on ESPN's feed — ESPN, NBA.com, Bleacher Report; HELD |
| Kristaps Porzingis | Kristaps Porzingis Warriors health update October 5 2026 · ESPN box score 10/4 (fetched) | DNP "not with team" 10/4; out indefinitely, no new statement — box score, Yardbarker, Golden State of Mind; HELD |
| Kawhi Leonard | Kawhi Leonard Raptors Heat preseason October 3 2026 played minutes · ESPN box score 10/3 (fetched) | did not dress 10/3; expected to miss 10/10 too — box score, HoopsHype 10/3, CTV News, Yahoo; HELD |
| Cam Thomas | Cam Thomas free agent signs October 2026 | unsigned; the Bucks item is February 2026 — NBC Sports, Spotrac |
| Jaden Ivey | Jaden Ivey free agent signs October 2026 | unsigned — Spotrac, Hoops Wire FA list |
| Jeremy Sochan | Jeremy Sochan Trail Blazers roster October 5 2026 | on the camp deal, roster bubble watch; first game 10/7 — SI Blazers, Yahoo; HELD |
| Lonzo Ball | Lonzo Ball OR Rob Dillingham free agent signs October 5 2026 | unsigned — Yahoo, Spotrac; the Jazz trade item is 2025 (garble) |
| Rob Dillingham | (same query) | unsigned, any team but Chicago — Fox Sports, Spotrac |
| Bennedict Mathurin | Bennedict Mathurin Pelicans preseason rotation October 5 2026 | presumptive sixth man; first game 10/6 at OKC — SI Pelicans, Fox 8; HELD |
| Ryan Rollins | Bucks Timberwolves preseason October 5 2026 starting lineup Ryan Rollins Kevin Porter Jr. · Milwaukee Bucks news October 5 2026 | projected starter tonight, Porter not in the projected five — Canis Hoopus, Yahoo primer; the game tips after the pull; HELD |
| Jalen Duren | Jalen Duren Pistons preseason opener Suns October 5 2026 status | game-time decision (undisclosed), missed Saturday's open practice — SI Pistons 10/5, RotoWire injury report; note |
| Dereck Lively II | Dereck Lively Mavericks update October 5 2026 | not cleared, no setbacks, misses Macao — Yahoo, Mavs Moneyball/ESPN, CBS Sports; exclusion stands |
| Bradley Beal | Bradley Beal Clippers preseason Warriors October 4 2026 played status · Bradley Beal ruled out Clippers Warriors Hawaii knee October 4 2026 · ESPN box score 10/4 (fetched) | did not play 10/4, knee, day-to-day — box score, Yahoo, Hoops Rumors Clippers Notes; one summary's "played" logged as a garble |
| Kon Knueppel | Kon Knueppel Hornets hamstring update October 5 2026 | trending positively per Lee 10/4, out for the preseason — Yahoo, SI Hornets; D-1002-1 holds |
| Adem Bona | Adem Bona 76ers foot update October 5 2026 | not cleared, out tonight — RotoWire, CBS Sports |
| Mikel Brown Jr. | Mikel Brown Jr. Nets ankle update October 5 2026 | taking contact, out 10/6, next chance 10/8 — RotoWire, Hoops Rumors |
| Anthony Black | Anthony Black Magic ankle update October 5 2026 | practiced Sunday, "pretty close" — RotoWire, CBS Sports, Hoops Rumors |
| Dru Smith | Dru Smith Heat calf update October 2026 | unchanged, "a couple of weeks" — NBC Sports, HoopsHype |
| Max Strus | NBA preseason injury October 4 2026 left game · Max Strus foot injury MRI Clippers October 5 2026 · ESPN box score 10/4 (fetched) | left after 5 min, right foot, testing in Los Angeles, no diagnosis — box score, Hoops Wire, RotoWire, Yahoo, BVM; note (D-1005-2) |
| Nic Claxton | NBA injury news October 5 2026 preseason · Nic Claxton hamstring Bulls out preseason re-evaluated two weeks | hamstring, re-evaluated in two weeks, out for the preseason — CBS Sports, RotoWire, Yahoo; note (D-1005-3) |
| Tobias Harris | Tobias Harris Spurs calf strain questionable opener October 2026 · nba.com/news index (fetched) | left calf strain, out for the preseason, questionable for 10/20 — NBA.com 10/4, ESPN, KSAT 10/5, Yahoo; note (D-1005-1) |
| Jordan Hawkins | Grizzlies waive Jordan Hawkins Kris Murray Walter Clayton roster October 2026 · ESPN MEM roster (fetched, direct) · espn.com Hawkins story (fetched, empty) | waived per ESPN/Shams, NBC Sports, Hoops Rumors, Yahoo; still on ESPN's roster feed at the direct check; placement held (D-1005-4) |
| Yang Hansen | Yang Hansen Trail Blazers preseason role October 2026 · basketball-reference.com/players/y/yangha01.html (fetched) · ESPN POR roster (fetched, direct) | third-string C per the GM, developmental reserve — Yahoo, Rip City Project; 2025-26 line from Basketball-Reference; row added (D59-3) |
| Yaxel Lendeborg / Isaiah Jackson / Brook Lopez | Golden State Warriors Clippers Honolulu preseason October 4 2026 recap · Los Angeles Clippers preseason Warriors October 4 2026 recap · ESPN box score 10/4 (fetched) | Lendeborg started at SF 19 min; Jackson started at C 17 min, Lopez 7 min off the bench — box score, NBC Sports Bay Area, Yahoo, Hoops Rumors Clippers Notes; notes (D-1002-3 carried) |
| Jaren Jackson Jr. / Zach Edey | Jazz Nuggets preseason October 4 2026 recap · Zach Edey Grizzlies preseason opener Hawks October 5 status ankle · ESPN box score 10/4 (fetched) | Jackson started 18 min / 11 pts — box score, Deseret, SL Tribune; Edey held out tonight, on track for 10/21 — RotoBaller, RotoWire, CBS Sports |
| Ben Simmons | Ben Simmons Kings preseason debut ramp up October 8 October 10 | held out tonight, targeting 10/8 or 10/10 — RotoWire, Bleacher Report; note |
| Tyler Herro | Tyler Herro Bucks preseason opener Timberwolves October 5 status | full participant, first game tonight — RotoWire, CBS Sports |
| John Konchar / Gabe Vincent / Johni Broome / Tony Bradley | Gabe Vincent OR Johni Broome OR John Konchar signs October 2026 · ESPN NYK roster (verifier) | all unsigned; Bradley not on ESPN's feed, camp deal stands — Hoops Rumors, SNY, Yahoo, Spotrac, Yardbarker |
| Nickeil Alexander-Walker | Hawks preseason Alexander-Walker Dort starting lineup October 2026 | Dort and McCollum both to get preseason starts — SI Hawks [SINGLE-SOURCE] |
| Neemias Queta / Mitchell Robinson | Celtics Queta Mitchell Robinson starting center preseason October 2026 | Queta expected to remain the starter — Yahoo/Keith Smith, SI Celtics |
| Hannes Steinbach / Moussa Diabaté | Hornets Steinbach Diabate starting center preseason October 2026 | no decision; the "logs 11" item is 2025 (garble) — SI Hornets, Last Word |
| (window ledger) | NBA transactions October 3 2026 signed waived traded · NBA transactions October 5 2026 waived roster cuts · NBA trade agreed October 4 2026 · basketball-reference.com NBA_2027_transactions (fetched) · nba.com/news (fetched) | nothing dated 10/2–10/5 on the direct ledger; zero trades; minor Exhibit-10 moves on no pool row |
| (injury sweep) | NBA injury news October 5 2026 preseason · NBA preseason injury October 4 2026 left game · NBA "cleared" OR "full participant" OR "return to practice" October 5 2026 | §4 — Strus, Claxton, Harris new; SGA rest; Simmons ramp; Duren day-to-day |
| (preseason) | ESPN scoreboard 10/3, 10/4, 10/5 (fetched, direct) · Toronto Raptors Heat preseason October 3 2026 recap · Jazz Nuggets preseason October 4 2026 recap | three games played in the window, five tonight; box scores in §4 |
| (team watch, 7) | "<Team> news October 5 2026" one each: CHI, GSW, LAC, MIL, NOP, POR, TOR | §4 |

## Bounds

- Direct-complete roster verification proves membership, not role; the one exempted
  row rests on three outlets for a five-day-old camp deal.
- A single preseason box score is a dated primary record, not a reprice mechanism
  (A2); the lines move at the WO-5 refresh after two games per team.
- The Hawkins waiver is reported by four outlets but not reflected on the official
  feed at run time; the placement follows the feed by design (roster validation
  lock). If the feed never reflects it before the next pull, D-1005-4 asks whether
  to override.
- Yang Hansen's line is an estimate from a seven-minute season; it sits at the bottom
  of both boards and changes no draft decision.
- The kit's 75 small displacements are re-standardization from one added row, not
  line changes; the deck's standardization did not move.
- Hoops Rumors, Yahoo and most sports domains are egress-blocked; their items rest
  on dated search summaries, as on every prior pull; four summary garbles were caught
  by date or by the box score this pull (§4). ESPN's article pages return empty
  bodies to this session.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-1005-1 | Tobias Harris: left calf strain, out for the preseason, re-evaluated after it, questionable for the 10/20 opener. Tag `inj-calf-risk` (0.78) now, or hold untagged until the post-preseason re-evaluation? | hold untagged; tag if he is ruled out of the opener |
| D-1005-2 | Max Strus: non-contact right foot injury five minutes into the opener, testing pending (Hoops Wire, RotoWire, Yahoo). Hold until the diagnosis, then apply the convention (a weeks-long recovery → exclusion; a short absence → note)? | hold until the diagnosis; apply the convention then |
| D-1005-3 | Nic Claxton: hamstring, re-evaluated in two weeks (about 10/19), out for the preseason, questionable for the opener. Tag `hamstring-risk` now or hold? | hold until the re-evaluation |
| D-1005-4 | Jordan Hawkins: waived per four outlets (ESPN/Shams, NBC Sports, Hoops Rumors, Yahoo), still on ESPN's official feed. Keep the roster validation lock (move to FA when the feed reflects it) or override the lock on the outlets now? | keep the lock; move at the next pull if the feed has caught up |
| D-1002-1 | Knueppel's tag | carried: hold until ruled out of the opener (trending positively) |
| D-1002-3 | camp first-unit signals, now one game each (Lendeborg started; Jackson over Lopez) | carried: hold for WO-5 after two games |
| D60-1..D60-4 | the port's tie-break, Murray-Boyles, the advice-line wording, closing D-G3 | carried, owner silent |

## Provenance and bounds

- Inputs: ESPN's scoreboard and summary feeds for 10/3–10/5 (fetched 2026-10-05),
  ESPN's roster API for all 30 teams (fetched by the verifier) and three rosters by
  hand; Basketball-Reference's 2026-27 transactions page and Yang Hansen's player page
  (fetched 2026-10-05); NBA.com's news index (fetched); 48 dated web-search summaries
  (2026-10-01 → 2026-10-05); the owner's request; the committed 10/02 pool and boards
  as the pre-pull snapshots.
- Every number in §5 is a script diff (`scratchpad pull1005/`), every gate line is
  the command's own output.
- Not verified: ESPN's article page for the Hawkins story (empty body); nothing here
  rests on a direct read of a blocked sports domain.

## In plain language

**What this pull did.** Three days since Friday's pull, and the first with real
games in it. Before any news search I read the three preseason box scores straight
from ESPN's feed, then swept the news, checked every player's team against ESPN's
live rosters for all 30 clubs, and rebuilt and republished the deck.

**What the games said.** The camp reads from Friday held up on the floor:

- Golden State's rookie Yaxel Lendeborg started at small forward and played 19
  minutes. Kerr wants him shooting more.
- The Clippers started Isaiah Jackson at center; Brook Lopez played seven minutes
  off the bench. Both lines stay where they are until the second game, as your
  D-1002-3 default says.
- Jaren Jackson Jr. started and played 18 minutes, his first game since the knee
  surgery. His risk tag stays for now by the first-season-back convention.
- Kawhi, Porziņģis and Jamal Murray all sat. Beal did not dress.

**The injuries.** Max Strus left the Clippers' game after five minutes with a
non-contact foot injury and is being tested; no diagnosis yet. Nic Claxton tweaked a
hamstring and is out for the preseason. Tobias Harris strained a calf, is out for the
preseason, and is questionable for the opener. None of the three is tagged yet; each
is on your sheet with a default.

**One roster move, held.** Four outlets report Memphis waived Jordan Hawkins. ESPN's
official roster feed still listed him when I checked, and the deck's rule is that a
player's team follows the official feed, so his row stays on Memphis with the
report attached. He moves to free agent the day the feed catches up.

**One row added.** Yang Hansen, Portland's third-string center, is now on both
boards at the very bottom. You asked for that after mock 59 drafted him with no row
on the deck. He changes no draft decision.

**What I did not change.** No tag, no line, no existing player's team. The kit board
shuffled by a place or two in 75 spots because adding one row re-centers the
scoring, including the exact tie between Towns and Maxey at five and six. The deck
board did not move.

**What I caught.** Four stale or wrong items: a summary that said Beal played (the
box score says he did not dress), a 2025 Hornets box score, the February Cam Thomas
signing again, and a 2025 Lonzo Ball trade item.

**Verification.** The rebuilt deck passed every gate: the page and the Python agree
exactly, all 191 test cases pass, the browser robot drafted a full room with 128
checks and zero failures, and Version 43 is live at the usual link.

**Your decisions.** D-1005-1 Harris (default: hold the tag until he is ruled out of
the opener). D-1005-2 Strus (default: hold until the diagnosis). D-1005-3 Claxton
(default: hold until the two-week re-evaluation). D-1005-4 Hawkins (default: keep the
official-feed rule and move him at the next pull). Knueppel and the camp-signal
question are carried.

**Next.** Five games tonight, including Milwaukee's opener with Rollins projected to
start and Detroit's with Duren a game-time decision. The projection refresh starts
once every team has played twice, likely around 10/9 to 10/10.
