# After-report — 2026-10-02 second pull (Friday morning) + deck v42

**Owner request (2026-10-02, verbatim):** "Good morning Claude, happy Friday! Please
conduct daily refresh pull, and provide after report with plain language following."

Pull window: 2026-10-02 → 2026-10-02 (the second pull of the date: from the overnight
pull's run time, 00:31 UTC, to 16:00 UTC; the first ran Thursday evening in the
owner's time, this one Friday morning). The first preseason game is tomorrow (10/3
TOR–MIA), none in the window. Gate: `check_provenance.py` → `PROVENANCE GATE: PASS —
all rows sourced; verified 2026-07-13 .. 2026-09-30`, exit 0.

**Method.** One search sweep of 42 dated queries: the ledger-shaped transaction check
(Basketball-Reference's 2026-27 transactions page read directly, plus two search
ledgers), a dedicated query for each of the eleven names the enumerator flagged at
run start, one team-shaped query for each of the eight teams in the watch set (CHI,
DET, GSW, LAC, MIL, NOP, POR, TOR), the injury sweep in both directions against the
45-row tag inventory (11 excluded, 34 risk), the free-agent rows, and the carried
items (Duren's deadline, the MEM cut-down, Lively, Beal, Knueppel, Bona, Brown Jr.,
Black, Herro, Edey, Alexander-Walker vs Dort, Queta's platoon, Steinbach vs Diabaté,
Konchar, Vincent, Broome, Bradley). Direct fetches: Basketball-Reference (open),
NBA.com's news index and its Duren article (open, dated 10/2), ESPN's transactions
page (empty body again — CANNOT VERIFY through it), ESPN's roster API for all 30
teams (the verifier). Edits applied by script with exact-match assertions
(`scratchpad pull1002b/deck_edit.py`, `judgment_colophon.py`), both boards diffed by
script against pre-pull snapshots, the deck built through gates 1–7/F8 and driven end
to end by the step-5b browser gate. Six search-summary garbles caught and logged (§4).

**Headline.** Jalen Duren's holdout is over: about 90 minutes before Thursday's
11:59 pm ET qualifying-offer deadline he agreed to the fully guaranteed five-year,
$200M deal (Shams Charania and Chris Haynes via NBA.com 10/2, Yahoo, Hoops Rumors,
ClickOnDetroit 10/2). The card that had held him at −0.08 since 9/29 is retired —
contract only, no role change, so neither board moves. Nothing else moved a tier:
zero trades on the direct ledger, no placement change, Lively still excluded. Seven
rows took dated camp notes, the loudest being the Clippers' first unit (Isaiah Jackson
at center with Brook Lopez on the second group "for now") and Yaxel Lendeborg named
the starter at small forward for Golden State's 10/4 preseason opener; both lines
hold until the WO-5 refresh after two preseason games. Deck v42 built and published.

## 1. Roster changes

| plane | change | count |
|---|---|---|
| both | No placement, tag or line change. The window's one transaction on a pool row is a contract: Jalen Duren agreed to the 5yr/$200M deal with Detroit (NBA.com 10/2 citing Shams Charania and Chris Haynes, Yahoo, Hoops Rumors, ClickOnDetroit 10/2); team DET unchanged, kit GP 72 unchanged, deck note rewritten from `rfa-holdout` to `re-signed` | 0 |
| deck | Notes only: Duren (above); Lendeborg (starts the 10/4 preseason opener at SF — SI Warriors, Yahoo, Heavy, Golden State of Mind); Isaiah Jackson, Brook Lopez, Max Strus (the Clippers' camp first unit Garland, Strus, Jones Jr., Hachimura, Jackson, Lopez on the second group — HoopsHype/Lue 10/1, SI Clippers, Clipperholics); Dru Smith (right calf strain, "a couple of weeks", minor per Spoelstra — NBC Sports 10/1, HoopsHype 10/1, SI Heat, ClutchPoints); Mikel Brown Jr. (not yet cleared for contact, no timetable — RotoWire, Yahoo/NetsDaily); Rollins (Jenkins may rotate starting groups through the preseason — SI Bucks, Yahoo) | 8 |

Two-source rule: every note carries two or more dated outlets; the one single-outlet
fragment (the Bucks camp photo's first five) is labeled `[SINGLE-SOURCE]` in the row
and changes nothing. The roster evidence file is untouched.

## 2. Flagged-item receipts (F1) — verdicts

- **Duren — CLEARED, card retired.** Agreed to the fully guaranteed 5yr/$200M deal
  about 90 minutes before the deadline; joins camp (NBA.com 10/2 quoting Shams
  Charania and Chris Haynes, Yahoo, Hoops Rumors, SI Pistons live updates,
  ClickOnDetroit 10/2). The 10/01 sheet said the card clears on either branch; it
  did. D-1002-2 (a contract-year note if he had taken the qualifying offer) is moot.
- **Ingram — HELD −0.15.** No new item: out for the start of the season, no
  timetable, "week-by-week" (ESPN, Bleacher Report, Yahoo).
- **Porziņģis — HELD −0.10, veto unchanged.** Still out indefinitely; Dunleavy "not
  marking him down as being out to start the season," Kerr day-to-day, not in Hawaii
  (NBC Sports Bay Area, Yahoo, Golden State of Mind).
- **Kawhi — HELD −0.05.** No contact drills yet; unlikely to play the 10/3 opener vs
  Miami though Rajaković said the team would consider it (CBS Sports, HoopsHype 10/1,
  Yahoo).
- **Cam Thomas, Ivey, Lonzo Ball — HELD, all unsigned** (Spotrac, Hoops Wire FA
  list, Yahoo; the "Bucks sign Cam Thomas" item is the February 2026 deal again).
- **Dillingham — HELD −0.10.** Unsigned, any team but Chicago (Hoops Rumors, Spotrac,
  ClutchPoints).
- **Sochan — HELD −0.2.** Camp's last day, no cut reported, non-guaranteed deal
  (Yahoo, Blazer's Edge, SI Blazers).
- **Mathurin — HELD −0.05.** No new item; the sixth-man read stands (SI Pelicans,
  Yahoo, FanSided).
- **Rollins — HELD −0.05.** Still undecided. Jenkins may use multiple starting groups
  through the preseason (SI Bucks, Yahoo); the camp photo's first five had Rollins at
  the point [SINGLE-SOURCE: SI Bucks]; the 2025 Rivers/Porter item resurfaced again;
  first preseason game 10/5.

## 3. The carried items

| item | finding (dated) | outlets | action |
|---|---|---|---|
| Lively (D-RT3 applied overnight) | not cleared for camp, no setbacks, shooting, misses Macao (10/9), 10/21 undetermined | Yahoo, Mavs Moneyball/ESPN, CBS Sports | exclusion stands on both planes |
| Beal | knee inflammation, doubtful for the 10/4 opener; the "preseason debut Friday vs the Warriors" items are October 2025 | CBS Sports, SI Clippers | no change; `inj-hip-risk` stays |
| Knueppel (D-1002-1) | out for all four preseason games, re-evaluated the first week of the regular season; not ruled out of the 10/21 opener | Yahoo, ESPN, NBA.com | no change; the sheet's default (tag only if ruled out of the opener) holds |
| Bona | re-evaluation in the next couple of days, could play part of the preseason | Hoops Rumors injury notes, Metro Philadelphia, Inquirer 10/2 | no change |
| Mikel Brown Jr. | not yet cleared for contact, no timetable, light on-court work | RotoWire, Yahoo/NetsDaily | note refreshed; no tag |
| Anthony Black | minor ankle sprain, day-to-day, limited | NBC Sports 10/1, RotoBaller | no change |
| MEM cut-down | 19 on the roster, cuts not yet executed; Clayton now expected to survive; Hawkins, Kris Murray and Peavy the vulnerable three | Yahoo, SI Grizzlies, BVM Sports 10/1 | thirteenth pull carried; Kris Murray's kit row waits on the execution |
| Alexander-Walker vs Dort | Alexander-Walker the projected starter, Dort off the bench with in-game experiments planned | SI Hawks, FanSided, Yahoo | no change |
| Queta vs Robinson (BOS) | competing for the starting spot, Queta with the inside track | CelticsBlog, Yahoo, SI Celtics | no change; Robinson's `inj-risk (timeshare)` stays |
| Steinbach vs Diabaté (CHA) | Diabaté the incumbent, no decision | SI Hornets, Yahoo | no change |
| Herro, Edey, Jaren Jackson Jr. | Herro a full camp participant; Edey cleared for on-court work, on pace for 10/21; no new Jackson item | RotoWire, CBS Sports / CBS Sports, Hoops Rumors / SI Jazz | tags kept by convention |
| Konchar, Vincent, Broome | unsigned; the Heat have made Vincent no offer | Hoops Rumors, SNY / Hoops Rumors, Yahoo / Hoops Rumors, Spotrac | FA rows stand |
| Tony Bradley | still not on ESPN's feed; the 9/30 Knicks camp deal stands | Hoops Rumors, Yardbarker, Yahoo | exempted again in the stamp |
| Jamal Shead | 3yr/$24M extension agreed 10/1, contract only | ESPN, NBC Sports 10/1, HoopsHype 10/1 | already noted at the overnight pull; nothing to change |

## 4. Window sweep, team shadows, injury sweep

- **Transactions (F5 ledger check).** Basketball-Reference's 2026-27 transactions
  page, read directly: still no entry dated 10/1 or 10/2; the newest remains 9/28.
  Zero trades in the window. NBA.com's news index, read directly: the only 10/2 item
  is the preseason preview ("preseason action begins Saturday"); the Duren article
  sits on the index and is dated 10/2. The Duren agreement is the window's one
  transaction on a pool row and is not yet on the ledger (an agreement, reported by
  the insiders). **Garbles logged:** (1) a search ledger offered an "October 2, 2026"
  transaction list — Ausar Thompson's extension (mid-September per ESPN and NBA.com),
  D'Angelo Russell's waiver (9/25), Buddy Hield's Atlanta trade (before the 9/27
  Bulls deal), Larsson, Powell, Reese, Weems, Mbeng — an undated aggregate of
  September moves, none dated in the window; (2) "Bucks sign Cam Thomas" is the
  February 2026 deal, a third time; (3) "Doc Rivers names Porter starter" and
  "Rollins has stolen Porter's spot" are 2025-26 items, a fourth time; (4) "Beal to
  make his preseason debut Friday vs the Warriors, 12 points" is October 2025; (5)
  "LeBron ruled out for the Lakers' preseason opener" is 2025 (he is a 76er; Metro
  Philadelphia 10/2 has him at the point in camp); (6) one summary dated the TOR–MIA
  opener "Saturday, October 2" — Saturday is 10/3, as NBA.com's own 10/2 preview says.
  ESPN's transactions page returned an empty body — CANNOT VERIFY through it.
- **Roster verification went direct again.** ESPN's roster API answered for all 30
  teams: 333 of 334 pool rows matched, zero mismatches; Tony Bradley the one unmatched
  row, exempted by name in the stamp with the same three outlets.
- **Team shadows.** CHI (open practice at Horner Park 10/2; Isaiah Stevens signed to a
  camp deal, not a pool row — SI Bulls, Hoops Rumors), DET (Duren agreed Thursday
  night, joins camp — ClickOnDetroit, NBC Sports, Newsweek), GSW (day three in Laie;
  Kerr's 10/4 starters Curry, Podziemski, Lendeborg, Green, Horford — SI Warriors,
  Yahoo, Heavy), LAC (first unit Garland, Strus, Jones Jr., Hachimura, Isaiah Jackson;
  Lopez second group, "things will change" — HoopsHype/Lue, SI Clippers,
  Clipperholics; Beal doubtful 10/4), MIL (Jenkins rotating groups; a likely opening
  five of Rollins, Herro, Jaquez, Kuzma, Turner [SINGLE-SOURCE: SI Bucks]; first
  preseason game 10/5 — SI Bucks, Yahoo), NOP (camp through 10/5; nothing new —
  NBA.com/Pelicans, WWL), POR (camp's last day; Lillard, Morant, Avdija, Camara,
  Clingan the expected opening five — Blazer's Edge, Yahoo; Fan Fest 10/4), TOR
  (camp's last day in Quebec City; Kawhi unlikely 10/3; Shead's extension — CBS
  Sports, HoopsHype, ESPN).
- **Injury sweep vs the F6 tag inventory (11 excluded, 34 risk).** Tagged and
  progressing, tags kept by convention: Haliburton ("fully healthy" — ESPN), Embiid
  (full participant — Bleacher Report, NBC Sports Philadelphia), Edey (cleared for
  on-court work — CBS Sports, Hoops Rumors), Herro, Adams, Simmons, VanVleet, Curry,
  Paul George, Kessler, Jaren Jackson Jr. Still out, tags kept: Butler, Moody,
  Porziņģis, Mark Williams, Sharpe, Ingram, Lively. Returning-but-untagged: Sabonis
  ("100%" — SI Kings), Luka (no restrictions — NBC Sports), Brandon Miller (full
  participant — Hoops Rumors): none carries a tag and none needs one. New items on
  pool rows: Dru Smith (§1). Not pool rows: Tacko Fall (hip strain, two weeks), Grant
  Williams (hamstring, misses the preseason), Isaiah Stevens, Micah Peavy.
- **FA rows.** Kit: Cam Thomas, Ivey, Dillingham, Broome, Konchar unsigned. Deck adds
  Lonzo, Vincent and the retired/overseas rows; all on no ESPN roster.

## 5. Board effects (computed, never eyeballed)

- **Kit.** `check_provenance.py` PASS; `rank_engine.py` re-run against the pre-pull
  snapshot: byte-identical (`diff` empty). No row changed — a contract agreement is
  not a projection mechanism. Top 12 unchanged.
- **Deck.** The adjusted-value order over the 323 draftable rows is identical to the
  pre-pull order (script diff: no entries, no exits, no moves). Notes carry no value.
  Pool sha256 `75a4994b4a59` (was `c3b23060522c`); 334 rows, none added or removed.

## 6. Deck build and publish

`build_deck.py` on 2026-10-02 (second build of the date): roster verification
direct-complete, 333/334 against all 30 official rosters, 0 mismatches, 1 exemption by
name; freshness stamped with the pool-changes note; JUDGMENT dated 2026-10-02 — the
Duren card retired, the ten open cards re-authored with this pull's receipts, all ten
still flagged by the enumerator; colophon Data paragraph rewritten for the second
refresh; planes 314 shared, team 0, exclusion 0, drift 0, propagation 0, **no waiver**
(the overnight Lively waiver is absorbed: the kit snapshot now carries GP 25); market
`yahoo-2026-10-01.csv`, 297 of 334 priced, 1 day old. No engine or card change this
pull; v42 differs from v41 in data and prose only.

## 7. Gates (2026-10-02, second pull)

| gate | result (evidence: the command's own output line) |
|---|---|
| kit `check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-09-30 |
| kit `check_derived.py` | all 13 dated artifacts reproduce byte-for-byte from their pinned inputs |
| kit `check_report.py` on this file | REPORT GATE: PASS (structure, publication rule, pull-log row) |
| deck `judgment_open_items.py --check-report` on this file | receipts check PASS — all 10 flagged names carry a receipts row |
| deck `verify_rosters.py` | direct-complete via site.api.espn.com (all 30 rosters): 333/334 checked, 0 mismatches, 1 unmatched exempted by name (Tony Bradley) |
| deck `check_planes.py` (in the build) | 314 shared · kit-only 10 · deck-only 20 · team 0 · exclusion 0 · drift 0 · propagation 0 · lines 171 (warning by design) |
| deck `build_deck.py` | deck built: 334 players · pull 2026-10-02 · pool 75a4994b4a59 · injection round-trip OK; safe to publish (market `yahoo-2026-10-01.csv`, 297 of 334 priced, 1 day old) |
| deck `check_parity.py` on the built page | PARITY: EXACT MATCH |
| deck `test_card.py` / `test_draft.py` / `test_gates.py` | CARD: all 89 cases passed / all 65 cases passed / all 37 cases passed (no code change this pull, so no red-first case) |
| deck step-5b `full_dom_check.mjs` on the built page | 128 assertions, 0 failed, 0 page errors, exit 0 (`arena/results/full_dom_check_2026-10-02_v42.json`) |
| artifact publish | Version 42 (id `1790958391-0e23`) at the standing URL; page 383,066 bytes, sha256 `82f3a19b08a3f2f6…`, identical to the built file |

## 8. Watchlist / open items

- **The first preseason games** — 10/3 TOR–MIA in Quebec City (Kawhi unlikely,
  Poeltl), 10/4 GSW–LAC in Honolulu (Lendeborg starting; Porziņģis out, Beal
  doubtful, Ingram out; Isaiah Jackson vs Lopez at center), 10/5 MIL–MIN (Rollins vs
  Porter, Herro), 10/5 DET (Duren's first camp week), 10/6 BKN–CHA (Brown Jr.,
  Knueppel out), 10/7 CHI, POR (Sochan). WO-5's refresh starts after two games per
  team; the next pull reads the 10/3 box score.
- **Lively** — back to the draftable pool when two outlets report him cleared.
- **Knueppel** — D-1002-1 stands; the trigger is a ruling-out for the 10/21 opener.
- **MEM cut-down** — thirteenth pull unexecuted; Kris Murray's kit row waits on it.
- **Camp first-unit signals** — Lendeborg (GSW), Isaiah Jackson over Lopez (LAC):
  notes only; D-1002-3 asks whether to reprice before WO-5.
- **Owner decisions carried:** D-BV1 (Butler), D-30-3, D58-2..D58-5, D-R1..D-R4,
  D-G2..D-G7, D-P1..D-P4, D-1001-1/3, D-ADP-1/2, D40-1/3, D-LS-1/3, D-1002-1;
  D-1002-2 moot (closed by the long-term deal).

## Open-item receipts

| player | query run | dated finding |
|---|---|---|
| Jalen Duren | Jalen Duren Pistons qualifying offer decision October 2 2026 · Detroit Pistons training camp news October 2 2026 Duren · nba.com/news index (fetched) · nba.com/news/pistons-jalen-duren-rookie-extension (fetched, dated 10/2) | agreed to the fully guaranteed 5yr/$200M deal about 90 minutes before the 11:59 pm ET deadline, joins camp — NBA.com 10/2 (Shams Charania, Chris Haynes), Yahoo, Hoops Rumors, SI Pistons, ClickOnDetroit 10/2; CLEARED, card retired |
| Brandon Ingram | Brandon Ingram Clippers Achilles update October 2 2026 | out for the start of the season, no timetable, "week-by-week" — ESPN, Bleacher Report, Yahoo; HELD |
| Kristaps Porzingis | Kristaps Porzingis Warriors health update Hawaii October 2 2026 | out indefinitely, Dunleavy not marking him out for the season start, Kerr day-to-day — NBC Sports Bay Area, Yahoo, Golden State of Mind; HELD |
| Kawhi Leonard | Kawhi Leonard Raptors preseason opener Miami October 3 2026 status | no contact drills, unlikely 10/3 though the team would consider it — CBS Sports, HoopsHype 10/1, Yahoo; HELD |
| Cam Thomas | Cam Thomas free agent signs October 2026 | unsigned; the Bucks item is February 2026 — ESPN, Spotrac |
| Jaden Ivey | Jaden Ivey free agent signs October 2026 | unsigned — Spotrac, Hoops Wire FA list |
| Jeremy Sochan | Jeremy Sochan Trail Blazers roster spot October 2 2026 | non-guaranteed deal, competing for a spot, no cut reported on the camp's last day — Yahoo, Blazer's Edge, SI Blazers; HELD |
| Lonzo Ball | Lonzo Ball OR Rob Dillingham free agent signs October 2 2026 | unsigned — Yahoo, Hoops Wire FA list, Spotrac |
| Rob Dillingham | (same query) | unsigned, any team but Chicago — Hoops Rumors, Spotrac, ClutchPoints |
| Bennedict Mathurin | Bennedict Mathurin Pelicans rotation sixth man October 2 2026 | sixth-man read stands — SI Pelicans, Yahoo, FanSided; HELD |
| Ryan Rollins | Bucks starting point guard Ryan Rollins Kevin Porter Jr. October 2 2026 · Milwaukee Bucks training camp news October 2 2026 | undecided; Jenkins rotating starting groups (SI Bucks, Yahoo); the camp photo's first five [SINGLE-SOURCE: SI Bucks]; the 2025 Rivers/Porter items logged as garbles; HELD |
| Dereck Lively II | Dereck Lively Mavericks cleared update October 2 2026 | not cleared, no setbacks, misses Macao — Yahoo, Mavs Moneyball/ESPN, CBS Sports; exclusion stands |
| Bradley Beal | Bradley Beal Clippers knee preseason opener Warriors October 4 status | doubtful for 10/4, knee inflammation — CBS Sports, SI Clippers; the "debut Friday" items are 2025 (garble) |
| Kon Knueppel | Kon Knueppel hamstring Hornets update October 2 2026 | out all four preseason games, re-evaluated the first week of the season, not ruled out of 10/21 — Yahoo, ESPN, NBA.com; D-1002-1 holds |
| Adem Bona | Adem Bona foot 76ers update October 2 2026 | re-evaluation in days, could play part of the preseason — Hoops Rumors, Metro Philadelphia, Inquirer 10/2 |
| Mikel Brown Jr. | Mikel Brown Jr. Nets ankle update October 2 2026 | not cleared for contact, no timetable — RotoWire, Yahoo/NetsDaily; note refreshed |
| Anthony Black | Anthony Black Magic ankle update October 2 2026 | day-to-day, limited — NBC Sports 10/1, RotoBaller |
| Dru Smith | Dru Smith Heat calf strain training camp October 2026 · NBA injury news October 2 2026 training camp | right calf strain Thursday, "a couple of weeks", minor per Spoelstra — NBC Sports 10/1, HoopsHype 10/1, SI Heat, ClutchPoints; note added |
| Yaxel Lendeborg | Steve Kerr names Warriors starters preseason opener Clippers Lendeborg October 2026 | starts the 10/4 opener at SF — SI Warriors, Yahoo, Heavy, Golden State of Mind; note added |
| Isaiah Jackson / Brook Lopez / Max Strus | Ty Lue Clippers starting lineup training camp Isaiah Jackson Brook Lopez Garland Strus October 2026 · Los Angeles Clippers training camp news October 2 2026 Beal Ingram | first unit Garland, Strus, Jones Jr., Hachimura, Jackson; Lopez second group, "things will change" — HoopsHype/Lue 10/1, SI Clippers, Clipperholics; notes added |
| Tyler Herro | Tyler Herro Bucks preseason status October 2 2026 | full camp participant — RotoWire, CBS Sports |
| Jaren Jackson Jr. / Zach Edey | Jaren Jackson Jr. Jazz OR Zach Edey Grizzlies preseason status October 2 2026 | no new Jackson item (SI Jazz); Edey cleared for on-court work, on pace for 10/21 — CBS Sports, Hoops Rumors |
| Nickeil Alexander-Walker | Hawks starting lineup Alexander-Walker Dort preseason October 2026 | projected starter, Dort off the bench — SI Hawks, FanSided, Yahoo |
| Neemias Queta / Mitchell Robinson | Celtics center rotation Neemias Queta Mitchell Robinson training camp October 2026 | competing, Queta the inside track — CelticsBlog, Yahoo, SI Celtics |
| Hannes Steinbach / Moussa Diabaté | Hornets starting center Steinbach Diabaté training camp October 2026 | Diabaté the incumbent, no decision — SI Hornets, Yahoo |
| John Konchar / Gabe Vincent / Johni Broome | John Konchar OR Gabe Vincent OR Johni Broome signs October 2026 | all unsigned — Hoops Rumors, SNY, Yahoo, Spotrac |
| Ausar Thompson | Ausar Thompson Pistons rookie scale extension October 2026 | 5yr/$155M extension is mid-September, not in the window — ESPN, NBA.com (garble logged) |
| Jamal Shead | Jamal Shead Raptors three-year extension agreed October 2026 | 3yr/$24M agreed 10/1 — ESPN, NBC Sports 10/1, HoopsHype 10/1; already noted overnight |
| Tony Bradley | ESPN roster API NYK (fetched by the verifier) | not on ESPN's feed; the 9/30 camp deal stands — Hoops Rumors, Yardbarker, Yahoo |
| (window ledger) | NBA transactions October 2 2026 signed waived traded · NBA trade agreed October 2 2026 · basketball-reference.com NBA_2027_transactions (fetched) · espn.com/nba/transactions (fetched, empty) · nba.com/news (fetched) | no 10/1–10/2 entry on the direct ledger; zero trades; the "October 2" list is an undated aggregate of September moves (garble logged) |
| (injury sweep) | NBA injury news October 2 2026 training camp · NBA "cleared" OR "full participant" practice training camp October 2 2026 · NBA player ruled out preseason opener injury October 2 2026 | §4 — Dru Smith new; Haliburton, Embiid, Sabonis, Luka, Miller cleared; Knueppel, Ingram, Brown Jr. out for openers; the LeBron item is 2025 (garble) |
| (preseason check) | NBA preseason game October 2 2026 result | no game in the window; the opener is Saturday 10/3 per NBA.com's 10/2 preview (one summary's "Saturday, October 2" logged as a garble) |
| (MEM cut-down) | Grizzlies roster cuts Walter Clayton Jordan Hawkins Kris Murray October 2026 | not executed; Clayton expected to survive; Hawkins, Murray, Peavy vulnerable — Yahoo, SI Grizzlies, BVM Sports 10/1 |
| (team watch, 8) | "<Team> training camp news October 2 2026" one each: CHI, DET, GSW, LAC, MIL, NOP, POR, TOR | §4 |

## Bounds

- Direct-complete roster verification proves membership, not role; the one exempted
  row rests on three outlets for a three-day-old camp deal.
- The Duren agreement is insider-reported (Charania, Haynes) and carried by NBA.com's
  own dated article; the signing itself is not yet on Basketball-Reference's ledger.
  The card is retired on the agreement; a reversal would re-open it.
- Camp first-unit reads (Lendeborg, Isaiah Jackson over Lopez) are two-day signals
  that the coaches themselves called fluid; they are notes, not reprices.
- No preseason box score exists yet; the first-week items wait on 10/3–10/7.
- Hoops Rumors, Yahoo and most sports domains are egress-blocked; their items rest
  on dated search summaries, as on every prior pull, and six summary garbles were
  caught by date this pull (§4).

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-1002-1 | (carried) Knueppel: out for all four preseason games, re-evaluated the first week of the season, not yet ruled out of the 10/21 opener. Tag `hamstring-risk` now, exclude, or hold untagged? | tag only if he is ruled out for the opener; hold until then |
| D-1002-3 | Camp first-unit signals before any preseason game: Lendeborg named the 10/4 starter at SF (28-minute line); Isaiah Jackson on the Clippers' first unit over Brook Lopez (Lopez's line was repriced 9/29 as the likely starter). Reprice either line now, or hold both for the WO-5 refresh after two preseason games? | hold for WO-5; the notes carry the signal and the refresh re-derives from box scores |

## Provenance and bounds

- Inputs: 42 dated web-search summaries (2026-09-28 → 2026-10-02), Basketball-
  Reference's 2026-27 transactions page, NBA.com's news index and its Duren article
  (fetched 2026-10-02), ESPN's roster JSON for all 30 teams (fetched by the
  verifier); the owner's request; the overnight pull's committed pool and boards as
  the pre-pull snapshots.
- Every number in §5 is a script diff (`scratchpad pull1002b/`), every gate line is
  the command's own output.
- Not verified: nothing here rests on a direct read of a blocked sports domain.

## In plain language

**What this pull did.** The overnight run was Thursday's pull; this is Friday
morning's. I checked every news source I can reach for anything that happened in
the fifteen hours between the two runs, verified every player's team against ESPN's
live rosters for all 30 clubs, and rebuilt and republished the draft deck.

**The one real event.** Jalen Duren signed. About an hour and a half before his
Thursday-night deadline he agreed to the five-year, $200 million deal Detroit had on
the table. Since September 29 his card had carried a small penalty because he was
holding out and barred from practice. That penalty is gone and the card is retired.
His projection does not change: a contract tells us where he plays, and it is the
same team, so neither board moved by a single place.

**What else came in.** Nothing that changes a ranking. The notes worth knowing for
draft night:

- Golden State starts the rookie Yaxel Lendeborg at small forward in Sunday's
  preseason opener. Kerr says only Curry and Green are locked in as regular-season
  starters.
- The Clippers' first unit in camp has Isaiah Jackson at center with Brook Lopez on
  the second group. Lue says that will change. Both lines stay where they are until
  real games are played; whether to move them sooner is your D-1002-3.
- Miami's Dru Smith strained a calf and is out a couple of weeks. Minor, no tag.
- Brooklyn's rookie Mikel Brown Jr. is still not cleared for contact and has no
  timetable.
- Kawhi probably sits Saturday's opener, Beal is doubtful for Sunday, Lively is
  still not cleared and stays excluded, and Knueppel is still out for the whole
  preseason, so your D-1002-1 question stands.

**What I did not change.** No player changed teams, no injury tag was added or
removed, and no stat line moved. Both boards are byte-for-byte what they were after
the overnight pull.

**What I caught.** Six times a search summary served an old story dressed as
today's: last year's Beal preseason debut, a 2025 LeBron-as-a-Laker item, the
February Cam Thomas signing, two 2025 Bucks point-guard items, and a transaction
list labeled "October 2" that was really September's moves. Each was checked
against a dated source and thrown out. That is the two-outlet rule doing its job.

**Verification.** The rebuilt deck passed every gate: the page and the Python agree
exactly, all 191 test cases pass, the browser robot drafted a full room with 128
checks and zero failures, and Version 42 is live at the usual link.

**Your decisions.** D-1002-1, Knueppel: the default is to hold until he is ruled out
of the opener. D-1002-3, the two camp signals: the default is to wait for the
preseason refresh. D-1002-2 is closed by the deal itself.

**Next.** Saturday's Raptors–Heat game is the first box score of the preseason.
From here each pull reads the box scores, and the WO-5 refresh starts once every
team has played twice.
