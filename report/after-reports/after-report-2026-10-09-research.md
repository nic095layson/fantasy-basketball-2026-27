# After-report — 2026-10-09 (research): the owner's role-and-health items checked against October-2026 outlets, two or three per item

**Owner request (2026-10-09, verbatim):** "If any of these real life opportunities interest you and may have an impact on
your system rankings (and categorical projections), please go ahead and research on the internet to find more and
strengthen your calculations. I ask that you limit any source findings to October 2026, and if you can find at least 2-3
sources affirming any roles, opportunities, and relevant research that only strengthen your arithmetic."

Pull window: 2026-10-09 → 2026-10-09 — a research pass, not a scheduled pull, plus the Macao box score (the morning
pull closed its window with that game in progress). Every item below was checked two ways: (1) dated October-2026
outlets found by search, two or three per claim, the queries and every returned URL pinned in
`research-2026-10-09/receipts.md` (30 queries); (2) the 24 preseason box scores of 10/3–10/9 read from ESPN's own
feed (`research-2026-10-09/sweep.tsv`, 58 target lines; `starters.txt`, `injuries.txt`). Verdicts: CONFIRMED (two or
more dated October outlets agree, the box score counting as one), SINGLE-SOURCE (one outlet), CONTRADICTED (the
record says otherwise), NOT FOUND (no October outlet on the point), ANSWERED (a panel lead that the October record
closes). What moves a row is the system's own rule, not the verdict: tags by the injury defaults (D-RT3, D-1005-2,
D-1008-1), lines by the WO-5 method after two games per team on Sunday's pass (rates from the 2025-26 per-36 line
times the projected minutes, two dated outlets for every role claim). This pass therefore changed the evidence under
the rows, not the rows: no line, tag, team or placement moved on either plane. Gate: `check_provenance.py` → PASS
(verified 2026-07-13 .. 2026-10-07), exit 0.

## 1. Roster changes

None. No line, tag, team or placement changed on either plane. The deck carries 44 dated notes on 39 rows
(the research receipts on 28 rows, the Macao box score on 16 rows); the kit's record is this report and WO-5
item (9).

## 2. The verdict table

| # | item (owner's note or the panel's lead) | what the October record says (outlets, dates) | verdict | effect on the arithmetic |
|---|---|---|---|---|
| 1 | Flagg + Irving synergy (owner) | Irving sat the 10/9 Macao game (left-knee rest) and plays Sunday 10/11, cleared for Macao with no restrictions per ANTA (Dallas Sports Journal 10/9; SI Mavericks; Yahoo Sports; Yardbarker); Flagg 19 pts in 19 min, 17 in the second quarter, sat the second half (ESPN box; Dallas Morning News 10/9, Dallas Sports Journal, Smoking Cuban); Flagg: Irving's gravity gets him easier shots (Dallas Sports Journal, Bleacher Report) | CONFIRMED (Irving's return); NOT YET OBSERVED (the pairing — Sunday is the first shared floor) | none today; Flagg's D-RN-2 re-derivation runs Sunday with both Macao boxes; Irving's tag stays by the first-season-back convention |
| 2 | Davis health (owner) | healthy and a full camp participant per the Wizards beat (Finberg via RotoWire 10/1); 16 pts / 7 reb in 17 min in the 10/8 debut at New York (ESPN box; CBS Sports, Bullets Forever/Yahoo); no minutes restriction or availability note found in October | CONFIRMED | none; inj-risk (0.78) stays — 20 games last season; his expected games belong to the post-draft availability model (D-1009-7) |
| 3 | Irving health (owner) | as row 1: cleared with no restrictions, first game since the 3/3/2025 ACL tear on Sunday (Dallas Sports Journal, SI Mavericks, Yahoo Sports) | CONFIRMED | none; tag stays for the first season back |
| 4 | Daniels usage vs Alexander-Walker and Dort (owner) | two starts, 18 and 21 min, 6 and 13 pts, one steal in 39 min (ESPN boxes; SI Hawks grades 10/6 and 10/9; CBS Sports); Alexander-Walker started both (CBS Sports 10/6, SI Hawks); Dort out of both with a right knee contusion (ESPN injuries page citing the Hawks' Chouinard; RotoWire, CBS Sports); ESPN's fantasy roundup warns the minutes may shrink with Dort, Wiggins and Flemings; the summer depth charts list Dort as a reserve (SI Hawks; AJC, July — outside the window) | CONFIRMED (Daniels starts; the competition exists); NOT FOUND (any October minute for Dort) | none today; steals 3.0 go to Sunday's three-season anchor (WO-5 items (5) and (8)); the Dort question has no preseason minute to answer it yet |
| 5 | Holmgren's weight and regression (owner) | 215 lb, two more than last year (OKC Thunder Wire via Bleacher Report, HoopsHype, Basketnews — all 9/28, outside the window); no preseason minutes: rest 10/6 (USA Today's Almanza via CBS Sports), a precautionary quad contusion 10/7 per Daigneault (CBS Sports 10/7, Yahoo Sports 10/8, RotoWire); next chance 10/12 at Atlanta | CONFIRMED (both absences precautionary); the weight item is September-dated and not arithmetic | none; the line holds (kit 17.5 / 8.5 / 2.4 blk at 30 mpg) |
| 6 | Mara's emergence (owner) | two starts, 18 and 25 min, 34 pts on 15-15, 15 reb, 4 blk (ESPN boxes; SLAM, News9, CBS Sports, Roundtable) — both with Holmgren, Hartenstein and Jaylin Williams out (Yahoo Sports 10/8, CBS Sports); the coverage expects significant competition for minutes when the regulars return | CONFIRMED (the production); CONTEXT: not a Holmgren signal — Mara has not shared a floor with him | none; the backup-C line (12 mpg) holds, WO-5 decides the Mara / Jaylin Williams battle |
| 7 | Jackson Jr.'s role and a late-season shutdown (owner) | a lock at the four (Yahoo Sports 10/2, Deseret 10/2); started both games, 18 and 16 min (ESPN boxes; RotoWire — Roundtable's 10/7 recap says 27 min, ESPN's box 16); summer surgery removed a growth from the left knee; more center time with Nurkić out (NBA.com release 10/8, SI Jazz) | CONFIRMED (role); NOT FOUND (shutdown — a late-season question no October outlet addresses) | none; the knee tag stays for the first season back |
| 8 | Porziņģis (owner: a grenade) | not with the team 10/4, did not play 10/7, out indefinitely (ESPN feed; Bleacher Report, Newsweek — the morning pull's receipts) | CONFIRMED (out) | none; vetoed since 9/28 |
| 9 | Bane, Herro, LaVine (owner's distrust) | box lines only: Bane 13 min / 9 pts 10/7; Herro 19 and 23 min, 11 and 13 pts; LaVine 15 and 23 min, 4 stl on 10/8 (ESPN boxes) | NOT RESEARCHED by design — the owner asked for consideration, not a check | none |
| 10 | Gafford starts at center with Lively out (panel lead) | Lively still not practicing, likely not back for 10/21 (SI Mavericks, Smoking Cuban); the beat expects Gafford to start (CBS Sports, Smoking Cuban); but Dallas opened small in Macao with Morez Johnson Jr. at the five and Gafford off the bench, 8 min / 7 pts (ESPN box; CBS Sports, SI Mavericks) | CONTRADICTED by the one box so far; the role is unsettled | none; the line (10.5 / 7.5 / 1.7 blk) is already LINE QUESTIONED by the repeat-name check and re-derives Sunday with both Macao boxes |
| 11 | Isaiah Jackson starting at center (panel lead, carried) | started the 10/4 opener over Lopez, first half by plan, 17 min / 4 / 4 / 3 ast / 2 blk (ESPN box; RotoWire 10/4, RotoBaller, SI Clippers); "I think I'm going to be in the starting role" to ESPN's Youngmisuk (Yahoo fantasy roundup); Lopez still competing, Lue says the lineup can change; Niederhauser (foot) out to start the year | CONFIRMED (one game) | none today; the 14-mpg line is Sunday's question after the 10/10 game at Toronto |
| 12 | Maluach's minutes (panel lead, carried) | Ighodaro started both games (SI Suns 10/7 lineup, Bright Side 10/6 and 10/8, Arizona Sports); Maluach 17 and 25 min off the bench (ESPN boxes), 21 mpg to Ighodaro's 16 (Arizona Sports); Ott: not settled, three games left, a third big wanted (Arizona Sports, Yahoo, BVM); Mark Williams about five months per Gambadoro (Arizona Sports; NBC Sports: likely until February) | CONFIRMED | none; the lines already split the minutes (kit Maluach 24 mpg, Ighodaro 20); Sunday decides |
| 13 | Knueppel (carried) | out for the whole preseason, re-evaluated the week of 10/19, the 10/21 opener in doubt, Peterson "doesn't know" (NBC Sports, NBA.com, Yahoo, Fox Sports, Roundtable) | CONFIRMED | none; D-1002-1 holds (kit 70 GP) |
| 14 | Coby White (carried) | left calf strain 10/5, out for the preseason, the opener uncertain (ESPN 10/5, Hoops Rumors, SI Hornets, ClutchPoints, Yahoo) | CONFIRMED | none; D-1006-2 carried (kit 68 GP) |
| 15 | Claxton (carried) | hamstring strain 10/5, out at least two weeks and all five preseason games, the opener in jeopardy, no grade released (Hoops Rumors, ClutchPoints, BVM Sports 10/5, Yahoo) | CONFIRMED | none; D-1005-3 carried (kit 68 GP) |
| 16 | Hachimura the second option with Ingram out (panel lead) | 21 pts in 15 min in the 10/4 opener (ESPN box; CBS Sports, Yardbarker, Yahoo); Ingram misses at least the 10/21 opener (Basketnews, CBS Sports); expected to start and carry more scoring (CBS Sports, Yardbarker) | CONFIRMED (one game) | none today; the 28-mpg / 13.5-pt line is Sunday's question after the 10/10 game |
| 17 | Garland's "recent injury issues" (panel lead) | the toe "100 percent" and the conditioning good, to Andscape (Basketnews 10/5); started 10/4, first half, 15 min / 15 pts / 6 ast on 4-4 (ESPN box; Fox Sports); Lue impressed with the offseason | ANSWERED — healthy | none; no tag; the kit's 70 GP holds |
| 18 | Poeltl's back (panel lead) | healthy this preseason after the back cost him last preseason and held him to 46 games, the regimen changed; started 10/3, 18 min / 9 pts / 2 stl / 1 blk on 3-3 (ESPN box; NBC Sports 10/3, Yahoo Sports Canada) | ANSWERED — healthy | none; the kit's 66 GP holds |
| 19 | Durant's rest days (panel lead) | 23 min / 15 pts in Macao, asked for more than the planned half to build chemistry with VanVleet per Udoka (ESPN box; CBS Sports, RotoWire, Houston Chronicle); sits the 10/11 rematch, a planned precaution, not an injury (CBS Sports, RotoWire, Houston Chronicle; ESPN's feed: not injury related); the team has discussed trimming his minutes and he has pushed back, 36.4 mpg last season (Newsweek, RotoBaller, Houston Chronicle) | CONFIRMED (a rest plan exists; no number attached) | none; the kit's 62 GP / 33 mpg already prices rest; item (9) closes this lead |
| 20 | Sengun (owner: an impressive line) | 16 / 10 / 10 with a steal in 22 min, +22, in the preseason opener (ESPN box; Eurohoops, RotoWire, Yahoo Sports, TalkBasket, Macau Business); no October item on a role change beyond the game | CONFIRMED (the line); NOT FOUND (any role change) | none |
| 21 | DeRozan's role (panel role word; the sweep) | off the bench in both Denver games, 10 and 11 min, behind Johnson and Braun (ESPN boxes); no October outlet on his regular-season role — the September signing coverage framed a bench scorer (NBA.com 9/8, Roundtable 8/5, outside the window) | NOT FOUND (October); the box score alone | none today; the kit's 27-mpg line is Sunday's question |
| 22 | Lively, Mark Williams, Ingram (the exclusions and the Achilles tag) | Lively not practicing, likely not back for 10/21 (SI Mavericks, Smoking Cuban; ESPN's feed carries a 10/11 placeholder); Williams' labrum surgery 9/10, no team timetable, five months per Gambadoro (Arizona Sports, NBC Sports, SI Suns); Ingram misses at least the opener (Basketnews, CBS Sports, Yahoo) | CONFIRMED | none; the exclusions (D-RT3, D-1009-1) and Ingram's tag and 48 GP stand |

## 3. The owner's notes, answered one by one

| owner's note (2026-10-09 evening) | what the record says | effect |
|---|---|---|
| "AD can win your season, but it fully depends on his health … I want to monitor news reporting and preseason results" | healthy, full camp, 16 in 17 minutes in the debut; nothing in October says otherwise (row 2) | the 0.78 haircut already prices the history; the monitor continues at every pull |
| "Irving is also insanely good (and self-reported fully healthy). A healthy Irving along with Flagg only optimizes Flagg's output" | cleared with no restrictions, plays Sunday; Flagg credits Irving's gravity already (rows 1, 3) | the pairing is unobserved until Sunday; Flagg's line re-derives on Sunday's pass with both boxes (D-RN-2) |
| "Daniels, I agree with on steals. I am concerned with NAW, and now with Dort, taking away his production and opportunities" | Daniels starts, one steal in 39 preseason minutes; Alexander-Walker starts beside him; Dort has not played (knee contusion); ESPN's fantasy desk shares the minutes concern (row 4) | the steals cell is Sunday's first item (three-season anchor 2.0 / outside median 2.2 against our 3.0); the opportunity concern is real and still unmeasured — no Dort minute exists |
| "Holmgren … scared of regression as he did not improve physically … his 2lb weight gain, and the emergence of Aday Mara" | the two-pound item is September-dated; Holmgren has not played (rest, then a precautionary quad contusion); Mara's two starts came with all three centers out (rows 5, 6) | nothing in the October record moves Holmgren's line; Mara's production is not evidence about Holmgren's minutes |
| "JJJ I also love, but him being on the Jazz … may be shut down towards fantasy playoffs" | a starter lock at the four, two starts, more center time with Nurkić out; no October outlet on a shutdown (row 7) | none now; the shutdown risk is a late-season availability question, the post-draft model's (D-1009-7) |
| "Porzingis … a fantasy grenade" | out indefinitely, not with the team (row 8) | vetoed since 9/28; nothing to change |
| "Bane, Herro and Lavine. I honestly just don't trust them" | box lines only (row 9); no research requested | none; their lines stand on the method |

## 4. The RotoWire leads (WO-5 item (9)) after this pass

| lead | status after the October check |
|---|---|
| Garland's "recent injury issues" | ANSWERED: healthy, toe 100 percent, started the opener; no tag, no change (row 17) |
| Poeltl's back (46 games last season) | ANSWERED: healthy this preseason, started the opener; the 66 GP holds (row 18) |
| Gafford as Dallas's starting center with Lively out | CONTRADICTED by the Macao box (bench, 8 min); unsettled; the line re-derives Sunday (row 10) |
| Hachimura as the Clippers' second option with Ingram out | CONFIRMED on one game (21 in 15); the line is Sunday's question (row 16) |
| Durant's rest days against his 62 | CONFIRMED that a rest plan exists, no number attached; 62 GP already prices it; closed with no change (row 19) |

## 5. The preseason box-score sweep (ESPN's feed, 24 games, 10/3–10/9)

Built from `research-2026-10-09/sweep.tsv` by `sweep_table.py` — the record, not a transcription. Dates are the
Eastern game dates. Lines are pts / reb / ast / stl / blk and the field-goal line.

| player | team | games (date: role, min) | lines (pts / reb / ast / stl / blk, FG) |
|---|---|---|---|
| Aday Mara | OKC | 10/6: start, 18 min; 10/7: start, 25 min | 12 / 9 / 3 / 0 / 3, 5-5; 22 / 6 / 2 / 0 / 1, 10-10 |
| Alperen Sengun | HOU | 10/9: start, 22 min | 16 / 10 / 10 / 1 / 0, 6-9 |
| Anthony Davis | WSH | 10/8: start, 17 min | 16 / 7 / 2 / 0 / 1, 6-11 |
| Brandon Ingram | LAC | 10/4: DNP (coach's decision) | — |
| Brook Lopez | LAC | 10/4: bench, 7 min | 1 / 3 / 0 / 0 / 0, 0-4 |
| CJ McCollum | ATL | 10/8: start, 19 min | 14 / 5 / 4 / 0 / 0, 5-11 |
| Clint Capela | HOU | 10/9: DNP (coach's decision) | — |
| Cooper Flagg | DAL | 10/9: start, 19 min | 19 / 6 / 3 / 1 / 1, 7-14 |
| Daniel Gafford | DAL | 10/9: bench, 8 min | 7 / 3 / 0 / 1 / 0, 3-4 |
| Darius Garland | LAC | 10/4: start, 15 min | 15 / 3 / 6 / 0 / 0, 4-4 |
| DeMar DeRozan | DEN | 10/4: bench, 10 min; 10/6: bench, 11 min | 5 / 1 / 1 / 0 / 1, 2-5; 7 / 1 / 1 / 0 / 0, 2-5 |
| Dereck Lively II | DAL | 10/9: DNP (coach's decision) | — |
| Desmond Bane | ORL | 10/7: start, 13 min | 9 / 1 / 1 / 0 / 0, 3-3 |
| Dyson Daniels | ATL | 10/5: start, 18 min; 10/8: start, 21 min | 6 / 4 / 2 / 0 / 0, 2-6; 13 / 11 / 1 / 1 / 0, 6-16 |
| Fred VanVleet | HOU | 10/9: start, 24 min | 17 / 2 / 7 / 2 / 0, 5-12 |
| Isaiah Jackson | LAC | 10/4: start, 17 min | 4 / 4 / 3 / 1 / 2, 2-3 |
| Jabari Smith Jr. | HOU | 10/9: start, 22 min | 12 / 4 / 1 / 1 / 0, 4-8 |
| Jakob Poeltl | TOR | 10/3: start, 18 min | 9 / 1 / 1 / 2 / 1, 3-3 |
| Jalen Johnson | ATL | 10/5: start, 18 min; 10/8: DNP (coach's decision) | 8 / 5 / 3 / 1 / 0, 1-7 |
| Jalen Williams | OKC | 10/7: start, 19 min | 16 / 3 / 6 / 2 / 0, 8-11 |
| Jaren Jackson Jr. | UTAH | 10/4: start, 18 min; 10/6: start, 16 min | 11 / 4 / 2 / 0 / 0, 4-7; 7 / 1 / 0 / 0 / 1, 2-3 |
| Kevin Durant | HOU | 10/9: start, 23 min | 15 / 0 / 2 / 0 / 1, 7-12 |
| Khaman Maluach | PHX | 10/5: bench, 17 min; 10/7: bench, 25 min | 6 / 2 / 0 / 0 / 1, 3-5; 8 / 7 / 4 / 0 / 0, 2-3 |
| Kristaps Porzingis | GS | 10/4: DNP (not with team); 10/6: DNP (coach's decision) | — |
| Kyrie Irving | DAL | 10/9: DNP (coach's decision) | — |
| Luguentz Dort | ATL | 10/8: DNP (coach's decision) | — |
| Mark Williams | PHX | 10/5: DNP (coach's decision); 10/7: DNP (coach's decision) | — |
| Michael Porter Jr. | BKN | 10/6: start, 17 min | 16 / 5 / 2 / 1 / 0, 6-9 |
| Mitchell Robinson | BOS | 10/8: DNP (coach's decision) | — |
| Naji Marshall | DAL | 10/9: start, 24 min | 16 / 2 / 3 / 0 / 0, 7-14 |
| Neemias Queta | BOS | 10/8: DNP (coach's decision) | — |
| Nic Claxton | CHI | 10/7: DNP (coach's decision) | — |
| Nickeil Alexander-Walker | ATL | 10/5: start, 16 min; 10/8: start, 23 min | 14 / 1 / 0 / 1 / 0, 6-9; 7 / 3 / 2 / 0 / 0, 2-8 |
| Onyeka Okongwu | ATL | 10/5: start, 14 min; 10/8: start, 22 min | 8 / 4 / 2 / 0 / 1, 3-4; 13 / 4 / 5 / 0 / 0, 5-11 |
| Oso Ighodaro | PHX | 10/5: start, 14 min; 10/7: start, 18 min | 3 / 5 / 2 / 1 / 0, 1-1; 8 / 2 / 2 / 1 / 0, 4-6 |
| P.J. Washington | DAL | 10/9: DNP (coach's decision) | — |
| Rui Hachimura | LAC | 10/4: start, 15 min | 21 / 5 / 0 / 0 / 1, 8-11 |
| Ryan Rollins | MIL | 10/5: start, 14 min; 10/7: start, 21 min | 15 / 4 / 1 / 1 / 1, 6-12; 12 / 3 / 7 / 1 / 1, 5-7 |
| Steven Adams | HOU | 10/9: bench, 14 min | 2 / 3 / 1 / 1 / 0, 1-1 |
| Ty Jerome | MEM | 10/5: start, 15 min; 10/7: start, 19 min | 12 / 0 / 5 / 0 / 1, 4-8; 17 / 1 / 4 / 0 / 0, 7-14 |
| Tyler Herro | MIL | 10/5: start, 19 min; 10/7: start, 23 min | 11 / 3 / 3 / 0 / 0, 3-9; 13 / 3 / 3 / 0 / 1, 5-9 |
| Victor Wembanyama | SA | 10/8: start, 17 min | 9 / 6 / 1 / 0 / 1, 3-6 |
| Zach LaVine | SAC | 10/5: start, 15 min; 10/8: start, 23 min | 9 / 1 / 0 / 0 / 0, 4-6; 11 / 1 / 4 / 4 / 0, 3-8 |

Starters per game for the teams in question are in `starters.txt`; the feed's injury rows for the target names
(status, body part, the feed's return estimate) in `injuries.txt`. Three reads from the starters file matter above:
Dallas opened Marshall, Morez Johnson Jr., Flagg, Risacher, Christie (Gafford bench); Phoenix opened Ighodaro both
games (Maluach bench); Oklahoma City opened Mara both games (Holmgren, Hartenstein, Jaylin Williams out).

## 6. What moved, and why nothing more

- **Lines:** none. The WO-5 method moves a line only after two games per team, on Sunday's pass, from the 2025-26
  per-36 rates times projected minutes with two dated outlets on the role. Four names from this pass are already on
  that pass with their boxes pre-loaded: Isaiah Jackson and Hachimura (one Clippers game so far; the second is 10/10),
  Gafford (one Dallas game; the second is 10/11), DeRozan (two Denver games, no October outlet on the role). Daniels'
  steals go to the three-season anchor (item (8)). Maluach / Ighodaro are two games in and the lines already split
  the minutes the way the box scores do.
- **Tags:** none. Every health item is already carried (Knueppel, White, Claxton, Lively, Mark Williams, Ingram,
  Nurkić, Porziņģis) or is precautionary by the team's own word (Holmgren, Hartenstein, Durant's Sunday, Dort's
  contusion, Irving's Friday rest). Irving's, Davis's and Jackson Jr.'s risk tags stay by the first-season-back
  convention the owner has seen on every pull.
- **Deck notes:** 44 dated fragments on 39 rows — the research receipts on 28 rows (four [SINGLE-SOURCE] markers
  from the morning pull lifted to two or more outlets: Holmgren's contusion, Daniels' and Alexander-Walker's 10/8
  lines, Maluach's 10/7 line) and the Macao box score on 16 rows (named outlets on Sengün, Flagg, Durant, VanVleet,
  Gafford; the rest [SINGLE-SOURCE: box score]); Ingram's judgment card re-dated with the Clippers' opener ruling.
- **Rankings:** identical to v53 on both planes by construction (no stat, tag, team or GP cell changed; the deck's
  non-note columns diffed against the v53 pool: 0 differences). The board file is unchanged.

## 7. Gates (2026-10-09, the research pass)

| gate | result |
|---|---|
| deck `check_parity.py` | PARITY: EXACT MATCH — 364 owner turns across 28 committed states, 318 market ranks compared (240 priced) |
| deck `test_card.py` | CARD: all 99 cases passed |
| deck `test_draft.py` | all 65 cases passed |
| deck `test_gates.py` | all 52 cases passed (gates_v54.log; the five PI cases included) |
| deck `identity_check.py` | POINTS IDENTITY: 41 player(s), 49 line(s) more than 1 from their own shooting (200 deck and 200 kit lines checked); exit 0 |
| deck `range_check.py` | RANGE CHECK: 131 player(s) with 436 cell(s) outside every reference (145 of the top 150 checkable); exit 0 |
| deck `full_dom_check.mjs` (state 54, v54 page) | pass: true — 143 assertions, 0 failed, 0 page errors (`arena/results/full_dom_check_2026-10-09_v54.json`) |
| deck `repeat_market_check.py` (v54 page) | 21 of 21 mocks replayed; 12 flagged, 5 near misses — the same 12 as v53 (`arena/results/repeat_market_check_2026-10-09_v54.json`) |
| deck `build_deck.py` | gates 1–7 pass, planes clean (315 shared, drift 0, propagation 0, 170 line warnings as before), 335 players, injection round-trip OK, safe to publish; exit 0 |
| kit `report/check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07; exit 0 |
| kit `report/check_derived.py` | DERIVED: all 21 dated artifacts reproduce byte-for-byte from their pinned inputs (nothing derived changed on this pass); exit 0 |
| kit `report/check_report.py` | REPORT GATE: PASS (structure, publication rule, pull-log row); exit 0 |
| deck `judgment_open_items.py --check-report` (this file) | receipts check PASS — all 10 flagged names carry a receipts row; exit 0 |
| deck `repeat_market_check.py --check-report` (this file) | REPEAT-NAME CHECK: PASS — 12 flagged names, each with a row (21 of 21 mocks replayed on the v54 page); exit 0 |

## 8. Watchlist / open items

- **Sunday 10/11** — the WO-5 pass, with this pass's boxes and receipts pre-loaded: Daniels' steals (item (5), anchor
  (8)); Flagg (D-RN-2) with both Macao boxes; Isaiah Jackson, Hachimura, Lopez after the Clippers' 10/10 game; Gafford
  and Morez Johnson Jr. after the 10/11 rematch; Maluach / Ighodaro; DeRozan; Mara / Jaylin Williams. Also 10/11:
  Irving's first game beside Flagg, Durant's planned rest.
- **10/12** — Holmgren, Hartenstein and Jaylin Williams' first chance (at Atlanta); Dort's knee (10/10 estimate).
- **Week of 10/19** — Knueppel, White, Claxton re-evaluations against the 10/21 openers.
- **10/13** — the bigger-picture assessment the owner asked for; this table is its health-and-role half.
- Everything carried from the day's earlier reports stands.

## Open-item receipts

| player | query run (2026-10-09) | dated finding |
|---|---|---|
| Brandon Ingram | the Clippers' opener ruling (query 13 in `receipts.md`) | out for at least the 10/21 opener per the Clippers; partial Achilles repair at the May procedure; Hachimura the second option meanwhile (Basketnews, CBS Sports, Yahoo) — HELD -0.15, re-check |
| Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (`after-report-2026-10-09.md`, receipts dated 10/9); Porziņģis re-read in this pass (row 8), the rest not in the owner's list | all HELD or unsigned on 2026-10-09; this pass did no roster research on them |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 a771018d8dd3), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 21 of 21 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-09.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-06.csv`, `hashtag-2026-10-09.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| PJ Washington | 17 of 21 | 87 | 151 | 178 | 144 | 141 | 121 | ast 2.4 vs 1.9-2; tov 1.5 vs 1.7-1.8; fg_pct .470 vs .448-.451; ft_pct .750 vs .698-.703 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Payton Pritchard | 16 of 21 | 37 | 83 | 33 | 90 | 92 | 72 | stl 1 vs 0.7-0.8; tpm 3.8 vs 3-3.2; tov 2 vs 1.3-1.3; ft_pct .850 vs .873-.875 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 15 of 21 | 28 | 65 | 60 | 56 | 43 | 44 | pts 18.5 vs 16.4-17; ast 2.3 vs 2.1-2.1; ft_pct .805 vs .813-.819 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Sandro Mamukelashvili | 15 of 21 | 81 | 169 | 138 | 105 | 153 | 120 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Daniel Gafford | 10 of 21 | 90 | 181 | 188 | 180 | 161 | 155 | pts 10.5 vs 9.1-9.8; reb 7.5 vs 5.8-6.5; ast 1.5 vs 1.1-1.2; blk 1.7 vs 1.2-1.4; fg_pct .700 vs .648-.689; ft_pct .700 vs .671-.687 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Jalen Suggs | 10 of 21 | 59 | 105 | 89 | 54 | 84 | 99 | pts 17 vs 14.1-15.1; ast 4 vs 4.8-5 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 9 of 21 | 82 | 144 | 94 | 121 | 137 | 98 | reb 7.5 vs 5.5-6.9; tpm 0.9 vs 1.2-1.3; fg_pct .520 vs .447-.498; ft_pct .740 vs .765-.828 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Isaiah Hartenstein | 7 of 21 | 75 | 104 | 141 | 92 | 100 | 102 | pts 11.5 vs 9.1-10.5; reb 11 vs 9.2-10.3; fg_pct .585 vs .597-.611; ft_pct .680 vs .642-.656 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Zach LaVine | 6 of 21 | 56 | 100 | 162 | 68 | 77 | 118 | pts 22.5 vs 17-21.1; reb 4.5 vs 3.1-3.6; ast 4 vs 2.8-3.4; tov 2.6 vs 2-2.4 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 5 of 21 | 89 | 142 | 122 | 131 | 125 | 123 | pts 16.8 vs 13.4-15.1; tov 1.5 vs 1-1.2; fg_pct .465 vs .432-.443 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Dyson Daniels | 5 of 21 | 11 | 62 | 20 | 64 | 56 | 53 | pts 14.5 vs 11.3-11.8; stl 3 vs 2-2.4; tpm 1.1 vs 0.5-0.6; fg_pct .495 vs .501-.513 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Saddiq Bey | 5 of 21 | 95 | 176 | 109 | 132 | 169 | 143 | blk 0.4 vs 0.1-0.1; tpm 2.4 vs 1.8-2; tov 1.5 vs 0.8-0.9 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Karl-Anthony Towns (16 mocks, value 6, market 15); Jalen Williams (15 mocks, value 16, market 39); Derrick White (11 mocks, value 24, market 44); Jalen Johnson (6 mocks, value 13, market 11); Mikal Bridges (6 mocks, value 61, market 82).

## Bounds

**Out of scope by design:** Bane, Herro and LaVine were not researched (the owner named them as distrust, not as a
question); no line or tag moved outside the WO-5 method, which runs Sunday; the panel's prose beyond the five leads
was not re-checked.

**Attempted and failed:** direct fetches of the game recaps and beat pages (macaubusiness.com, lastwordonsports.com,
eurohoops.net refused by the egress proxy tonight, as cbssports, sports.yahoo, rotowire, si.com and the rest were
earlier in the session); every dated outlet above is therefore the search tool's digest of the page, the URL pinned
in `receipts.md`, with two or more outlets required before a row calls anything confirmed and the ESPN box score as
the one primary record. Two digests conflicted with that record and lost to it: Roundtable's 27 minutes for Jackson
Jr. on 10/6 (ESPN's box: 16) and CBS's 17-point headline for Davis (ESPN's box: 16).

**Not found (named as limits, not choices):** any October minute or role report for Dort (he has not played); any
October outlet on a Jackson Jr. shutdown, on a Sengün role change, or on DeRozan's regular-season role; the Sunday
Macao game, which had not been played.

**September-dated items named but not used:** Holmgren's 215 lb (9/28), DeRozan's signing framing (9/8), the AJC's
July depth chart, Last Word's 9/29 Ingram piece.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-1009-11 | Holmgren: the October record (two precautionary absences, no minutes) says nothing about regression and Mara's starts came without him; (a) hold the line and the 30-mpg assumption to Sunday's pass, where his own first box joins; (b) apply an owner haircut now | (a) |
| D-1009-12 | Gafford: the panel's starting-center lead is contradicted by one box; (a) hold the line to Sunday with both Macao boxes (the repeat-name check already questions it); (b) re-derive him now on one game | (a) |
| D-1009-13 | Durant: a rest plan exists with no number; (a) keep 62 GP; (b) the owner names a lower number | (a) |

**Owner disposition (2026-10-09, later the same evening, verbatim: "Keep three defaults and finish the chain"):**
D-1009-11 (a), D-1009-12 (a), D-1009-13 (a). Holmgren's line and 30-mpg assumption, Gafford's line and Durant's 62 GP
all hold to Sunday's WO-5 pass. No row changes on either plane, so the deck stays at v54 and no rebuild follows; the
kit's record is this note, the WO-5 item (9) paragraph and the pull-log row.

## Provenance and bounds

- Inputs: the owner's message (verbatim above); ESPN's summary feed for the 24 games (ids in `sweep.tsv`); the 30
  search queries and their returned URLs (`receipts.md`); the deck pool before and after (`deck_edit_record.json`).
- Records: `report/after-reports/research-2026-10-09/{sweep.tsv, sweep_table.md, starters.txt, injuries.txt,
  receipts.md, deck_edit_record.json}`; the deck's `data/players.csv` notes (the fragments begin "10/9 (research):" or
  carry the Macao box); the deck's `arena/results/full_dom_check_2026-10-09_v54.json` and
  `repeat_market_check_2026-10-09_v54.json`; the page published as Version 54 (id 1791578089-d0fd) after a fresh read of
  Version 53 (its body equal to the deck's main, so no outside republish since).
- Every number in §5 is the sweep script's output; every count in §1 and §6 is the edit script's record; every
  outlet in §2 is in `receipts.md` under its query.

## In plain language

**What you asked.** Chase the real-life items — roles, health, opportunity — on October sources only, two or three
agreeing, and let them strengthen the arithmetic.

**What I found.** Almost everything the record says agrees with what the rows already carry. Irving is cleared and
plays Sunday, his first game beside Flagg. Davis is healthy and played. Daniels starts, but he has one steal in 39
preseason minutes and Dort has not played yet, so your opportunity worry is real and still unmeasured. Holmgren has
not played at all — rest, then a bruised quad the team calls precautionary — which means Mara's two big games came
with all three Thunder centers out; they say nothing about Holmgren's minutes. Jackson Jr. is a locked starter. The
Suns start Ighodaro and play Maluach more. Isaiah Jackson and Hachimura each had one strong Clippers game. Garland and
Poeltl are healthy. Durant sits Sunday on purpose. Knueppel, White and Claxton are out through the preseason. The one
lead the record contradicts is the panel's "Gafford starts with Lively out": Dallas opened small and Gafford played
eight minutes off the bench.

**What changed.** Nothing in the rankings — on purpose. The system moves a line only after two games per team, from
rates times minutes with two outlets on the role, and that pass is Sunday. What this pass did is put the receipts
under the rows (44 dated notes on the deck) and pre-load Sunday's work: Daniels' steals, Flagg with both Macao
games, the two Clippers bigs and Hachimura after Saturday's game, Gafford after Sunday's rematch. The deck was rebuilt
and verified so the notes travel with the card.
