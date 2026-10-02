# After-report — 2026-10-02 data pull + deck v41

**Owner request (2026-10-02, verbatim):** "What are your logical recommended next
actions? Proceed with that." — the recommended action being WO-3's daily pull with
the deck rebuilt as v41 carrying D-LS-2.

Pull window: 2026-10-01 → 2026-10-02 (1 day: the last day of most training camps;
the first preseason games are 10/3 and 10/4, none in the window). Gate:
`check_provenance.py` → `PROVENANCE GATE: PASS — all rows sourced; verified
2026-07-13 .. 2026-09-30`, exit 0.

**Method.** One search sweep of 38 dated queries: the ledger-shaped transaction
check (Basketball-Reference's 2026-27 transactions page read directly, plus two
search ledgers), a dedicated query for each of the eleven flagged receipts, one
team-shaped query for each of the eight teams in the watch set (CHI, DET, GSW,
LAC, MIL, NOP, POR, TOR), the injury sweep in both directions against the 45-row
tag inventory, the free-agent rows, and the carried items (Duren's deadline, the
MEM cut-down, Broome, Vincent, Black, Knueppel, Lively, Beal, Alexander-Walker vs
Dort). Direct fetches: Basketball-Reference (open), NBA.com's news index (open,
nothing dated 10/1–10/2), ESPN's transactions page and NBA.com's Pistons page
(both returned empty bodies — CANNOT VERIFY through them), ESPN's roster API for
all 30 teams (the verifier). Edits applied by script with exact-match assertions
(`scratchpad pull1002/deck_edit.py`, the kit edit inline), both boards diffed by
script against the pre-pull snapshots, the deck built through gates 1–7/F8 and
driven end to end by the step-5b browser gate. Five search-summary garbles caught
and logged (§4).

**Headline.** A quiet window with one carried decision landed: Dereck Lively II is
now a recovery exclusion on both planes (deck `foot-recovery`, kit GP 25) — the
10/01 sheet's D-RT3 default, applied as that sheet said because he is still not
cleared for camp, will miss the Macao preseason games and has no opener status.
No trade and no window signing on a pool row (Basketball-Reference's ledger, read
directly, has no 10/1–10/2 entry). Jalen Duren's qualifying-offer deadline passed
at midnight and no reachable outlet reports the outcome, so his card holds one
more day. Seven rows took dated notes. Deck v41 built and published, carrying
D-LS-2: the survival chips' tooltip now says how those bands played out in your
own league last season.

## 1. Roster changes

| plane | change | count |
|---|---|---|
| both | Dereck Lively II → recovery exclusion (D-RT3 default from the 10/01 sheet, "re-tag at the next pull unless cleared"): deck tag `inj-risk` → `foot-recovery` (availability 0.0), kit GP 56 → 25 (the planes-gate twin). Mechanism: not cleared for camp, gradually increasing basketball activity with no setbacks, will miss the Macao preseason games from 10/9, 10/21 opener undetermined; Gafford the favorite to start while he heals (Mavs Moneyball/ESPN, CBS Sports, Yahoo 10/1–2). He returns to the draftable pool the day two outlets report him cleared | 1 |
| deck | Notes only, no tier change: Duren (deadline passed, outcome unreported), Konchar (Knicks camp deal 9/15, waived 9/30 — Hoops Rumors, HoopsHype/Begley, Yardbarker; FA again), Herro (full camp participant after an April foot procedure — CBS Sports, RotoWire), Bona (foot re-evaluation in days — Liberty Ballers, Metro Philadelphia), Mikel Brown Jr. (rolled ankle, likely misses the 10/6 preseason opener — NetsDaily, Yahoo, ClutchPoints), Beal (knee inflammation, 10/4 opener in doubt — RotoWire, HoopsHype/Law Murray, SI Clippers), Knueppel (misses the preseason, re-evaluation the week of 10/19 — NBA.com, Yahoo, WBTV) | 7 |

Two-source rule: the Lively re-tag carries three outlets; every note edit two or
more. No placement moved; the roster evidence file is untouched.

## 2. Flagged-item receipts (F1) — verdicts

- **Duren — HELD −0.08; outcome unreported.** The 11:59 pm ET 10/1 deadline has
  passed. NBC Sports' latest is "still awaiting"; CBS Sports and NBC Sports
  carry the weight clause removed from the $200M offer (9/30); ESPN/Shams has him
  skipping media day; NBA.com's news index, read directly, has nothing dated
  10/1 or 10/2. Either branch — the qualifying offer or a long-term deal —
  resolves the card at the next pull. Unsigned at run time, not on the camp roster.
- **Ingram — HELD −0.15.** No new item: partial Achilles tear found at the May heel
  surgery, out for the start of the season, no timetable, re-evaluated at the
  opener (NBA.com, Bleacher Report, NBC Philadelphia).
- **Porziņģis — HELD −0.10, veto unchanged.** Out indefinitely with the undisclosed
  issue, "day to day" per Kerr, not in Hawaii, misses the 10/4 opener
  (Yahoo/Kerr, Golden State of Mind, Newsweek).
- **Kawhi — HELD −0.05.** Quebec City camp, drills without live contact on the
  planned ramp-up (HoopsHype 9/29, SI Raptors, Yahoo); first preseason game 10/3.
- **Cam Thomas, Ivey, Lonzo Ball — HELD, all unsigned** (Spotrac, Hoops Wire FA
  list, Heavy; the "Bucks sign Cam Thomas" items are the February 2026 deal).
- **Dillingham — HELD −0.10.** Unrestricted free agent, any team but Chicago
  (Hoops Rumors 9/28, Spotrac, ClutchPoints).
- **Sochan — HELD −0.2.** On Portland's 18-man camp roster on the non-guaranteed
  deal, fighting for a spot through the camp's last day (SI Blazers, Yahoo,
  Blazer's Edge).
- **Mathurin — HELD −0.05.** Camp runs through 10/5; still the presumptive sixth
  man behind Herb Jones (SI Pelicans, Yahoo).
- **Rollins — HELD −0.05.** Undecided; listed first on the camp depth chart
  (RealGM), the debate still running (SI Bucks, Behind the Buck Pass); first
  preseason game 10/5. The "Doc Rivers names Porter starter" item is 2025 again.

## 3. The carried items

| item | finding (dated) | outlets | action |
|---|---|---|---|
| D-RT3 Lively | not cleared for camp, no setbacks, misses Macao (10/9), opener undetermined | Mavs Moneyball/ESPN, CBS Sports, Yahoo | **default applied** — re-tagged both planes (§1) |
| Konchar (FA row) | Knicks camp deal 9/15, waived 9/30 (personal matter), unsigned again | Hoops Rumors, HoopsHype/Begley, Yardbarker | note; row stays FA (the 10/01 direct check already had him on no roster) |
| Alexander-Walker vs Dort | projected starter at the two, Dort off the bench with a chance to work in | SI Hawks, FanSided | no change; watch the first preseason start |
| Anthony Black | minor sprain, day-to-day, limited | RotoWire, Yahoo/Sweeney | note stands, no tag |
| Knueppel | misses the entire preseason; opener in doubt; re-evaluation week of 10/19 | NBA.com, Yahoo, WBTV | note refreshed; tag question D-1002-1 |
| Beal | hip "95% there", knee inflammation, 10/4 opener in doubt, season not in serious danger | RotoWire, HoopsHype/Law Murray, SI Clippers | note; `inj-hip-risk` stays |
| MEM cut-down | latest read: Clayton stays; Hawkins, Murray and Peavy the likely cuts — not yet executed | SI Grizzlies, Yardbarker, TalkBasket | twelfth pull carried; Kris Murray's kit row (MEM) waits on the execution |
| Vincent, Broome | unsigned | Heavy, Spotrac / Hoops Rumors, Spotrac | FA rows stand |

## 4. Window sweep, team shadows, injury sweep

- **Transactions (F5 ledger check).** Basketball-Reference's 2026-27 transactions
  page, read directly: no entry dated 10/1 or 10/2; the newest are 9/28
  (Memphis waived Lovering; Charlotte waived Dillingham; Atlanta, Sacramento and
  Memphis Exhibit-10 and two-way signings). Zero trades in the window. **Garbles
  logged:** (1) a search ledger offered "October 2, 2026" signings — Mamukelashvili
  to Toronto, Dickinson and Trey Alexander two-ways, Kelly and Nembhard to Dallas,
  Sears to Milwaukee, Reeves and Landale waived — every one a 2025 move (the
  direct ledger has none of them this window; Nembhard's current deal is Denver's,
  per the 10/01 pull); (2) "Jaren Jackson Jr. doubtful, knee" is the March 2026
  item (SI Jazz and Deseret have him expecting to be fully ready); (3) "Tyler Herro
  to miss the first month after surgery" is the 2025 item (CBS Sports and RotoWire
  9/29–30 have him a full participant); (4) one summary gave Beal's absence to
  his hip, the dated outlets to knee inflammation with the hip recovered; (5) the
  Rivers/Porter item (2025) resurfaced a third time. ESPN's transactions page
  returned an empty body on fetch — CANNOT VERIFY through it; the direct
  Basketball-Reference read is the ledger cited.
- **Roster verification went direct again.** ESPN's roster API answered for all
  30 teams: 333 of 334 pool rows matched, zero mismatches; the one unmatched row is
  Tony Bradley's 9/30 Knicks camp deal, hand-verified again (Hoops Rumors,
  Yardbarker, Daily Knicks: the Konchar waiver made his room) and exempted in the
  stamp.
- **Team shadows.** CHI (open practice at Horner Park 10/2; Essengue praised by
  Splitter; Giddey a full participant — Yahoo/SI Bulls, On Tap, Bleacher Nation),
  DET (Duren absent; 20-man camp; Collins, Prince, Joe, Okorie the additions —
  Yahoo, NBC Sports, NBA.com), GSW (Oahu camp, 10/4 vs the Clippers; Porziņģis
  out — KHON, KITV, Star-Advertiser), LAC (Hawaii through 10/3; Ingram limited, Beal
  out at the start; Jamarion Sharp waived from a two-way, not a pool row — KTLA,
  Yahoo, SI Clippers), MIL (Jenkins on depth; Herro participating; Rollins/Porter
  undecided — SI Bucks, Yahoo, NBA.com preview), NOP (camp through 10/5; Shumate
  released, not a pool row — NBA.com/Pelicans, WWL), POR (camp's last day 10/2,
  Fan Fest 10/4, preseason 10/7 vs Golden State; Morant's catch-and-shoot work —
  Blazer's Edge, Yahoo, BVM), TOR (Quebec City camp day two; Poeltl "moving well,
  looks good" per Webster; preseason 10/3 vs Miami — SI Raptors, Raptors Republic).
- **Injury sweep vs the F6 tag inventory (10 excluded, 35 risk).** Tagged and
  progressing, tags kept by convention: Embiid, Curry, Jaren Jackson Jr.
  (expects to be fully ready — SI Jazz, Deseret), VanVleet, Edey, Adams (fully
  cleared — Yahoo), Simmons (fully cleared — theScore), Kessler, Paul George.
  Still out, tags kept: Butler, Moody, Porziņģis, Mark Williams, Sharpe, Ingram;
  Lively now excluded (§1). Returning-but-untagged: Herro (foot procedure in
  April, full participant — no tag, note added), Giddey and Brunson (cleared,
  already noted). New minor items on pool rows: Bona (§1), Mikel Brown Jr. (§1).
  Not pool rows: Grant Williams (CHA, hamstring, misses the preseason), Jamarion
  Sharp, Yanic Konan Niederhauser.
- **FA rows.** Kit: Cam Thomas, Ivey, Dillingham, Broome, Konchar unsigned. Deck
  adds Lonzo, Vincent and the retired/overseas rows; all on no ESPN roster.

## 5. Board effects (computed, never eyeballed)

- **Kit.** `top-200-2026-27.md` regenerated against the pre-pull snapshot: no
  entries, no exits, no move of three or more, no one- or two-place
  displacement. Lively stays 111: his composite is negative, so the 56 → 25 games
  change cannot move him (the D-RT3 row said so). Top 12 unchanged.
- **Deck.** By adjusted value over the draftable rows (324 → 323): Lively (131)
  exits as a recovery exclusion; no entries; RJ Barrett 245 → 242 and Stephon
  Castle 255 → 252 by re-standardisation; 201 further displacements of one or two
  places. Pool sha256 `c3b23060522c` (was `1ecfb66bdcef`).

## 6. Deck build and publish

`build_deck.py` on 2026-10-02: roster verification direct-complete, 333/334
against all 30 official rosters, 0 mismatches, 1 exemption by name; freshness
stamped with the pool-changes note; JUDGMENT re-dated 2026-10-02 — eleven open
cards re-authored with today's receipts, none added or removed, all eleven still
flagged by the enumerator; colophon Data paragraph rewritten for the window;
planes 314 shared, team 0, exclusion 0, drift 0, propagation 1 waived by name
(Lively: the kit's GP 25 is the twin of the deck's exclusion tag; the gate's own
exclusion check agrees — the waiver is recorded in the manifest); market
`yahoo-2026-10-01.csv`, 297 of 334 priced, 1 day old. **D-LS-2 shipped:** the
survival chips' tooltip now reads, after the public-room rates, "In your league
last season (156 picks scored at your seat, 2026-10-01): BUY NOW rows survived 21
of 53, TOSS-UP 36 of 69, quiet rows 447 of 481 — your room waits longer than the
public ones." Red-first: the card suite's new case failed on the unchanged page
(1 of 89) and passes on v41. Display only; no ordering change.

## 7. Gates (2026-10-02)

| gate | result (evidence: the command's own output line) |
|---|---|
| kit `check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-09-30 |
| kit `check_derived.py` | all 13 dated artifacts reproduce byte-for-byte from their pinned inputs |
| kit `check_report.py` on this file | REPORT GATE: PASS (structure, publication rule, pull-log row) |
| deck `judgment_open_items.py --check-report` on this file | receipts check PASS — all 11 flagged names carry a receipts row |
| deck `verify_rosters.py` | direct-complete via site.api.espn.com (all 30 rosters): 333/334 checked, 0 mismatches, 1 unmatched exempted by name (Tony Bradley) |
| deck `check_planes.py` (in the build) | 314 shared · team 0 · exclusion 0 · drift 0 · propagation 0 · waived 1 (Lively, the exclusion twin) · lines 171 |
| deck `build_deck.py` | all gates pass; safe to publish (pool `c3b23060522c`; market `yahoo-2026-10-01.csv`, 297 of 334 priced, 1 day old) |
| deck `check_parity.py` on the built page | PARITY: EXACT MATCH |
| deck `test_card.py` / `test_draft.py` / `test_gates.py` | CARD: all 89 cases passed (the D-LS-2 case failed red on the unchanged page, 1 of 89; its first run on v41 failed on the case's own lower-case string, corrected to the sentence's text, then passed) / all 65 cases passed / all 37 cases passed |
| deck step-5b `full_dom_check.mjs` on the built page | 128 assertions, 0 failed, 0 page errors, exit 0 (`arena/results/full_dom_check_2026-10-02_v41.json`) |
| artifact publish | Version 41 (id `1790901055-9661`) at the standing URL; page 381,649 bytes, sha256 `212afb42da9eb772…` |

## 8. Watchlist / open items

- **Duren** — the deadline passed last night; the first outlet to report the
  outcome resolves the card (qualifying offer: cleared, unrestricted in 2027;
  long-term deal: cleared).
- **The first preseason games** — 10/3 TOR–MIA (Kawhi, Poeltl), 10/4 GSW–LAC in
  Honolulu (Porziņģis out, Beal in doubt, Ingram out), 10/5 MIL–MIN (Rollins vs
  Porter), 10/5 DET preseason opener (Duren), 10/6 BKN–CHA (Brown Jr.), 10/7 CHI,
  POR; WO-5's refresh starts after two games per team.
- **Lively** — back to the draftable pool when two outlets report him cleared.
- **Knueppel** — re-evaluation the week of 10/19 (D-1002-1).
- **MEM cut-down** — twelfth pull unexecuted; Kris Murray's kit row waits on it.
- **Owner decisions carried:** D-BV1 (Butler), D-30-3, D58-2..D58-5, D-R1..D-R4,
  D-G2..D-G7, D-P1..D-P4, D-1001-1/3, D-ADP-1/2, D40-1/3, D-LS-1/3; D-RT3 closed
  today (default applied); D-LS-2 shipped (default applied).

## Open-item receipts

| player | query run | dated finding |
|---|---|---|
| Jalen Duren | Jalen Duren Pistons qualifying offer decision signed October 2026 · Jalen Duren accepts qualifying offer Pistons October 2 2026 · Jalen Duren Pistons agree contract extension deadline night · "Duren" Pistons signs OR "qualifying offer" news October 2 2026 · Jalen Duren Pistons decision (espn.com, nba.com, cbssports.com, nbcsports.com) · nba.com/news index (fetched) · nba.com/pistons/news (fetched, empty) | deadline passed, outcome unreported — NBC Sports "still awaiting", CBS/NBC (weight clause removed 9/30), ESPN/Shams (skipped media day); HELD |
| Brandon Ingram | Brandon Ingram Clippers Achilles update October 2 2026 | out for the start of the season, no timetable — NBA.com, Bleacher Report, NBC Philadelphia; HELD |
| Kristaps Porzingis | Kristaps Porzingis Warriors health update October 2 2026 | out indefinitely, "day to day" per Kerr, misses the 10/4 opener — Yahoo/Kerr, Golden State of Mind, Newsweek; HELD |
| Kawhi Leonard | Kawhi Leonard Raptors training camp practice October 2 2026 | ramp-up, no live contact — HoopsHype 9/29, SI Raptors, Yahoo; HELD |
| Cam Thomas | Cam Thomas free agent signs team October 2026 | unsigned; the Bucks items are February 2026 — ESPN, NBC Sports, Spotrac |
| Jaden Ivey | Jaden Ivey free agent signs October 2026 | unsigned — Spotrac, Hoops Wire, Heavy |
| Jeremy Sochan | Jeremy Sochan Trail Blazers training camp roster October 2 2026 | 18-man camp roster, non-guaranteed, fighting for a spot — SI Blazers, Yahoo, Blazer's Edge; HELD |
| Lonzo Ball | Lonzo Ball OR Rob Dillingham free agent signs October 2026 | unsigned, no indication of a change — Yahoo, Hoops Wire, Spotrac |
| Rob Dillingham | (same query) | unrestricted free agent, any team but Chicago — Hoops Rumors 9/28, Spotrac, ClutchPoints |
| Bennedict Mathurin | Bennedict Mathurin Pelicans rotation training camp October 2 2026 | presumptive sixth man behind Herb Jones — SI Pelicans, Yahoo; HELD |
| Ryan Rollins | Bucks starting point guard Ryan Rollins Kevin Porter Jr training camp October 2 2026 | undecided; first on the camp depth chart (RealGM), debate live (SI Bucks, Behind the Buck Pass); the Rivers item is 2025 |
| Dereck Lively II | Dereck Lively Mavericks cleared practice update October 2 2026 | not cleared, misses Macao, no setbacks — Mavs Moneyball/ESPN, CBS Sports, Yahoo; D-RT3 default applied (§1) |
| John Konchar | John Konchar signs free agent October 2026 · Knicks part ways John Konchar personal matter September 30 2026 | Knicks deal 9/15, waived 9/30, unsigned again — Hoops Rumors, HoopsHype/Begley, Yardbarker |
| Tyler Herro | Tyler Herro injury status Bucks training camp October 2026 | full participant after an April foot procedure — CBS Sports, RotoWire; the "miss a month" item is 2025 |
| Jaren Jackson Jr. | Jaren Jackson Jr. knee doubtful Jazz training camp October 2026 | the "doubtful" item is March 2026; expects to be fully ready — SI Jazz, Deseret; tag kept by convention |
| Adem Bona | Adem Bona sprained foot 76ers training camp October 2026 | re-evaluation in the next few days, "hopeful" for part of the preseason — Liberty Ballers, Metro Philadelphia |
| Mikel Brown Jr. | Mikel Brown Jr. Nets ankle preseason opener October 2026 | rolled ankle, likely misses 10/6, not expected to miss considerable time — NetsDaily, Yahoo, ClutchPoints |
| Bradley Beal | Bradley Beal Clippers injury status training camp Hawaii October 2 2026 | knee inflammation, hip 95%, 10/4 in doubt — RotoWire, HoopsHype/Law Murray, SI Clippers |
| Kon Knueppel | Kon Knueppel hamstring Hornets update October 2 2026 · Grant Williams hamstring Hornets training camp October 2026 | misses the preseason, re-evaluation the week of 10/19 — NBA.com, Yahoo, WBTV |
| Anthony Black | Anthony Black ankle Magic training camp update October 2 2026 | day-to-day, limited — RotoWire, Yahoo/Sweeney |
| Nickeil Alexander-Walker | Hawks starting lineup Nickeil Alexander-Walker Luguentz Dort training camp October 2026 | projected starter, Dort off the bench — SI Hawks, FanSided |
| Gabe Vincent | Gabe Vincent signs free agent guard October 2026 | unsigned — Heavy, Spotrac |
| Johni Broome | Johni Broome signs October 2026 | unsigned since the 9/24 LAC waiver — Hoops Rumors, Spotrac |
| Tony Bradley | ESPN roster API NYK (fetched by the verifier) | not on ESPN's feed; the 9/30 camp deal stands — Hoops Rumors, Yardbarker, Daily Knicks |
| (window ledger) | NBA transactions October 2 2026 signed waived traded · NBA trade October 1 2026 OR October 2 2026 agreed deal · basketball-reference.com NBA_2027_transactions (fetched) · espn.com/nba/transactions (fetched, empty) | no 10/1–10/2 entry on the direct ledger; zero trades; the "October 2" signings a summary offered are 2025 moves (garble logged) |
| (injury sweep) | NBA training camp injury news October 2 2026 · "cleared" OR "full participant" returns training camp practice NBA October 2 2026 · NBA player ruled out preseason opener injury October 2 2026 | §4 — Giddey, Brunson, Simmons, Adams cleared; Knueppel, Ingram, Brown Jr. out for openers; Grant Williams not a pool row |
| (MEM cut-down) | Grizzlies waive Walter Clayton OR Jordan Hawkins OR Kris Murray roster cut October 2026 | still not executed; latest read keeps Clayton — SI Grizzlies, Yardbarker |
| (team watch, 8) | "<Team> training camp news October 2 2026" one each: CHI, DET, GSW, LAC, MIL, NOP, POR, TOR | §4 |

## Bounds

- Direct-complete roster verification proves membership, not role; the one
  exempted row rests on three outlets for a three-day-old camp deal.
- Duren's outcome is a CANNOT VERIFY today, not a finding: the deadline passed in
  the window and the reachable outlets had not reported by run time; ESPN's
  transactions page and NBA.com's Pistons page returned empty bodies.
- The Lively exclusion is a convention applied, not a medical read: it reverses
  the day two outlets report him cleared.
- No preseason box score exists yet; the first-week items wait on 10/3–10/7.
- Hoops Rumors, Yahoo and most sports domains are egress-blocked; their items rest
  on dated search summaries, as on every prior pull, and five summary garbles were
  caught by date this pull (§4).

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-1002-1 | Knueppel: out for the whole preseason with the opener in doubt and a re-evaluation the week of 10/19. Rule 4 reads a recovery with no cleared return as an exclusion, but three pulls have kept him untagged on the strength of "pain gone". Tag `hamstring-risk` (0.78) now, exclude, or hold untagged until the 10/19 re-evaluation? | tag `hamstring-risk` if he is ruled out for the 10/21 opener; hold until then |
| D-1002-2 | Duren: when the outcome lands, the card clears either way; if he took the qualifying offer, keep a one-line "contract-year" note on the row or nothing? | nothing — the card clears |

## Provenance and bounds

- Inputs: 38 dated web-search summaries (2026-09-28 → 2026-10-02), Basketball-
  Reference's 2026-27 transactions page and NBA.com's news index (fetched
  2026-10-02), ESPN's roster JSON for all 30 teams (fetched by the verifier);
  the owner's request; the committed 10/01 pool and boards as the pre-pull
  snapshots.
- Every number in §5 is a script diff (`scratchpad pull1002/`), every gate line is
  the command's own output.
- Not verified: nothing here rests on a direct read of a blocked sports domain.
