# After-report — 2026-10-06 data pull + deck v44, with the Acuff Jr. research

**Owner request (2026-10-06, verbatim):** "Good morning, please conduct daily refresh
pull and provide after report. Acuff Jr. looks like he will have a sizeable role and
contributions, please see if you can research this on your end." — WO-3's daily pull
plus a dedicated research item (§2).

Pull window: 2026-10-05 → 2026-10-06 (from the Monday pull's run time, 18:35 UTC on
10/5, to 19:30 UTC on 10/6: one day; five preseason games played in it — Hawks–
Grizzlies, Pistons–Suns, 76ers–Knicks, Bucks–Timberwolves and Kings–Lakers, all 10/5 —
and four more tip after this pull). Gate: `check_provenance.py` → `PROVENANCE GATE:
PASS — all rows sourced; verified 2026-07-13 .. 2026-10-06`, exit 0.

**Method.** The five box scores read from ESPN's own feed (scoreboard and summary
endpoints, the same host the verifier uses) before any search: starters, minutes,
lines and DNP reasons for every pool row that dressed, cross-referenced to the pool by
script (`scratchpad pull1006/boxscores.txt`). Then one search sweep of 46 dated
queries: the ledger-shaped transaction check (Basketball-Reference's 2026-27
transactions page read directly — 81 dated entries parsed — plus one search ledger),
a dedicated query for each of the ten flagged receipts, one team-shaped query for each
of the seven teams in the watch set (CHI, GSW, LAC, MIL, NOP, POR, TOR), the injury
sweep in both directions against the 45-row tag inventory, the free-agent rows, the
carried items (Strus, Claxton, Harris, Hawkins, Lively, Beal, Knueppel, Bona, Brown
Jr., Black, Dru Smith, the MEM cut-down, Alexander-Walker vs Dort, Queta, Steinbach vs
Diabaté, Konchar/Vincent/Broome/Bradley, Edey, Duren, Simmons), and seven queries on
Acuff Jr. Direct fetches: Basketball-Reference (the ledger and Acuff's player page with
his Arkansas line, both open), NBA.com's news index (open), ESPN's roster API for all
30 teams (the verifier) plus Sacramento, Memphis, New York, the Lakers, Atlanta,
Milwaukee and Charlotte read by hand with their injury entries, and ESPN's Kings
schedule. Wikipedia is egress-blocked to this session (two fetches refused). Edits
applied by script with exact-match assertions (`scratchpad pull1006/deck_edit.py`,
`kit_edit.py`), both boards diffed by script against the committed v43 pools, the
deck built through gates 1–7/F8 and driven end to end by the step-5b browser gate.
Four search-summary garbles and one query error of mine caught and logged (§5).

**Headline.** Two rows moved on both planes, the owner's own defaults applied as the
10/5 sheet said. Max Strus has a partial tear of the right plantar fascia, is
re-evaluated in four weeks and misses the start of the season (ESPN, NBA.com, Hoops
Rumors), so the D-1005-2 default — apply the convention once the diagnosis came —
makes him a recovery exclusion (deck `foot-recovery`, kit GP 25). Johni Broome signed
with Milwaukee (RotoWire, CBS Sports, Hoops Rumors) and moves from FA to MIL,
exempted by name until ESPN's feed lists him. Basketball-Reference's ledger now
carries Memphis's 10/2 waiver of Jordan Hawkins, but ESPN's feed still lists him, so
his row stays under the lock (D-1005-4 carried). The box scores: Darius Acuff Jr.
started at the point and played 27 minutes, the most of any Kings starter — the
research the owner asked for is §2, and the line holds at 29 minutes until the
projection refresh after game two (D-1006-1). Ryan Rollins started at the point for
Milwaukee with Porter the first sub; Ty Jerome started over Pippen Jr.; Paul Reed
started at center with Duren held out; Edgecombe, Boozer and Flemings started. Coby
White is out for the preseason with a calf strain (D-1006-2). The build refused once
on a data trap in its own regex, diagnosed and routed around (D-1006-3). No line
changed. Deck v44 built and published.

## 1. Roster changes

| plane | change | count |
|---|---|---|
| both | **Max Strus → recovery exclusion** (deck tag `fifth-starter candidate…` → `foot-recovery`, availability 0.0; kit GP 68 → 25, the exclusion twin). Diagnosis 10/5: partial tear of the right plantar fascia, re-evaluated in four weeks, out for the rest of the preseason and the start of the regular season (ESPN, NBA.com, Hoops Rumors, HoopsHype, CBS Sports). The 10/5 sheet's D-1005-2 default was "hold until the diagnosis; apply the convention then" — applied: a weeks-long recovery with no cleared return is a recovery exclusion (the Lively and Adams precedents; `hoops.availability`). Re-entry when two outlets report him cleared and playing. The planes gate's propagation check flagged the kit-only GP move and was waived by name, recorded in the manifest (the Lively mechanism) | 1 |
| both | **Johni Broome FA → MIL** — signed by the Bucks 10/6 (reported Exhibit 10, competing for a roster spot; John Butler Jr. waived to make room — RotoWire, CBS Sports, Hoops Rumors, Yahoo, Heavy). Not yet on ESPN's Milwaukee feed at the 10/6 direct check (21 names, no Broome), so the verifier ran `--allow-unmatched` with the reason in the stamp note — the Tony Bradley mechanism, whose own exemption lapsed today because ESPN's Knicks feed now lists him. Line unchanged (rookie-proj, 10 minutes). Kit provenance row rewritten (RotoWire, 2026-10-06) | 1 |
| deck | **Jordan Hawkins — still held.** Basketball-Reference's 2026-27 transactions ledger, read directly, now carries "October 2, 2026: The Memphis Grizzlies waived Jordan Hawkins" (with ESPN/Shams, NBC Sports, Hoops Rumors from 10/5); he was not on the 10/5 box score; ESPN's official roster feed still listed him on Memphis at the 10/6 direct check (21 names). The verifier treats an FA row that appears on a feed as a mismatch, so the placement stays MEM under the lock with the ledger receipt in his note (D-1005-4 carried, with the override cost named) | 0 |
| deck | Notes only, no tier change (52 rows): the five box scores on every pool row that started, sat, or carried a role question (§5), plus Coby White (calf strain, out for the preseason — NBA.com 10/5, RealGM, Heavy), Suggs (illness), Kawhi (misses 10/10 too), Knueppel, Lively, Beal, Dru Smith, Brown Jr., Black, Bona and Edey | 52 |

Two-source rule: every note carries two or more dated outlets or the box score as the
primary record plus one; the two box-score-only fragments (Cardwell's 29 minutes;
Duncan Robinson's start was left unnoted) and the one single-outlet claim (PhillyVoice
on Hukporti's Achilles tear) are labeled `[SINGLE-SOURCE]` in the rows. The roster
evidence file was rewritten by the direct verifier (all 30 rosters).

## 2. Acuff Jr. — the owner's question

**The claim.** "Sizeable role and contributions." Split in two, because the evidence
answers them differently.

**Role — SUPPORTED, [CONFIRMED] starter, [LIKELY] 29–32 minutes.**

- Primary record (ESPN box score, 10/5 vs the Lakers): started at point guard; 27
  minutes, the most of any Kings starter — Sabonis 10, LaVine 15, Hunter 13, Achiuwa
  13 — and within two of the team's most (Sharp 30, Cardwell 29, Clifford 28). The
  staff left him on the floor with the second unit after the starters sat, which is
  how a team treats a rookie it is developing, not one it is protecting.
- Depth chart and plan (dated outlets): SI.com's Kings depth chart lists Acuff as the
  starter with Monk and Simmons behind him; CBS Sports "projected to start" (9/30);
  RotoWire's guard sleepers piece calls his "the best opportunity spot out of the top
  10 draftees" with "30-plus minutes right away"; FantasyAlarm's season preview says
  Sacramento "enters 2026-27 by handing the keys" to him; Yahoo's camp item has
  Christie calling him "first one in, last one out … the kid is a machine."
- Postgame (dated 10/5–6): Christie — "his poise is at a really high level. He's not
  ducking the smoke" (Sactown Sports, SI.com); Yahoo's debut story: 17 of his 19
  points came in his first 19 minutes, "handled pressure … without appearing
  rattled"; Heavy: "erases Summer League doubts."
- Both planes already price this: the 9/30 role pass moved him from 26 to 29 minutes
  as the starting point guard (kit and deck twins), the fifth-highest minutes line of
  any 2026 rookie in the pool (Boozer 32, Dybantsa 31, Peterson 30, Wilson 30, Acuff
  29, Brown 29, Lendeborg 28).

**Contributions — CATEGORY-DEPENDENT; in this league's 9-cat format the role is
priced and the rates are the question.**

- The line (both planes): 68 GP, 29 mpg, 16.7 pts / 3.1 reb / 5.0 ast / 1.0 stl /
  0.2 blk, 2.1 3PM, .430 FG on 13.4 FGA, .820 FT, 2.6 TOV.
- The college base (Basketball-Reference, read directly): Arkansas 2025-26, 36 GP,
  35.1 mpg, 23.5 pts / 3.1 reb / 6.4 ast / 0.8 stl / 0.3 blk, 2.5 3PM on 5.8 3PA
  (.440), .484 FG, .809 FT on 6.1 FTA, 2.2 TOV.
- The Summer League (Yahoo, NBC Sports Bay Area): five games, 20.8 pts on .350 FG
  and .278 3P, 4.6 ast, 3.8 TOV — the shooting did not carry over there.
- The debut: 8-17 FG, 1-4 3P, 2-2 FT, 5 turnovers in 27 minutes — volume and poise,
  with the turnover rate the Summer League showed.
- The market: Yahoo ADP 155 / XRank 109.7 (the owner's 10/01 paste); Hashtag 29.1
  mpg, 14.5 / 1.9 / 5.0 on .454 (9/30); RotoBaller 15.0 / 3.2 / 4.9 / 1.1 stl, .452,
  9-cat rank 224 (9/29); the five-source consensus rank 163 (10/01). Kit rank 190;
  deck adjusted-value rank 179 of 323.

**Sensitivity (computed in scratch, nothing committed — `scratchpad
pull1006/acuff_sens.py`).** The kit engine and the deck's value function re-run with
his row rewritten; everyone else unchanged.

| scenario | kit rank (z) | deck rank (of 323) |
|---|---|---|
| S0 as priced: 29 mpg, .430 FG, 2.1 3PM, 2.6 TOV | 190 (−2.97) | 179 |
| S1 32 mpg, same per-minute rates | 153 (−2.23) | 148 |
| S2 32 mpg, the Arkansas shooting carries (.455 FG, 2.7 3PM, .810 FT) | 118 (−1.20) | 114 |
| S3 34 mpg, the Arkansas shooting carries | 81 (−0.29) | 79 |
| S4 29 mpg, Summer League efficiency (.410 FG, 3.0 TOV) | outside 200 | 265 |

Reading it: three more minutes buy about 35 places; the shooting carrying over buys
another 35; both together make him a round-10 value in a 156-pick room, and the
Summer League version of him is undraftable. Half the gap between him and the
market's ADP 155 is the minutes question, half is the shooting question, and one
preseason game — 8-17, 1-4, five turnovers — answers neither. In 9-cat the mechanism
is specific: a volume scorer at .430 with 2.6 turnovers is negative in two
categories before his points and assists count, so his value swings on FG% and TOV
more than on usage. In a points league the same evidence would already argue for
a reprice.

**What this pull did with it.** The role evidence is two-outlet and dated, and the
box score agrees with it, but the pool's own rule (WO-5; bound A2 since 10/5) is that
one preseason box score is evidence of role, never of rates, and lines move at the
refresh after two games per team — Sacramento's second game is 10/8 at the Lakers
(ESPN schedule). So the line holds at 29 minutes today, the deck note carries the
debut, and the choice is the owner's on the sheet (D-1006-1) with the numbers above
beside it. Draft-day consequence either way: at Yahoo ADP 155 in a 156-pick room he
is a last-round name or undrafted, so the cost of waiting for game two is nil; if
the owner wants the S2 line now, both planes move in one script with assertions and
the board diff goes in the next report.

## 3. Flagged-item receipts (F1) — verdicts

- **Ingram — HELD −0.15.** No new item; light on-court work, no timetable (Bleacher
  Report, ESPN).
- **Porziņģis — HELD −0.10, veto unchanged.** No new team statement; out
  indefinitely, did not travel to Hawaii (NBA.com, Bleacher Report); the trade-
  candidate item (Yahoo/Siegel) is speculation, logged as such.
- **Kawhi — HELD −0.05.** Expected to miss the 10/10 Vancouver game too; a week of
  workouts before a possible late-preseason appearance (NBA.com Starting 5, RotoWire,
  SI.com).
- **Cam Thomas, Ivey, Lonzo Ball — HELD, all unsigned** (Spotrac, NBC Sports, Yahoo,
  Heavy); the summaries surfaced only the 2025 qualifying-offer and Jazz-trade items
  again (garbles, §5).
- **Dillingham — HELD −0.10.** Unsigned, any team but Chicago (Hoops Rumors,
  RotoBaller, Spotrac).
- **Sochan — HELD −0.2.** Still on the Exhibit 9 camp deal; Portland's first game is
  10/7 vs Golden State, where Nori "probably" starts Morant and Lillard (Blazer's
  Edge, Yahoo, SI.com).
- **Mathurin — HELD −0.05.** The Pelicans' first game tips tonight at Oklahoma City
  in Tulsa, no lineup published before this pull (SI.com, NBA.com).
- **Rollins — HELD −0.05, one game.** Started the 10/5 opener at the point (Rollins,
  Herro, Jaquez, Kuzma, Turner), 15 points in 14 minutes before fouling out; a cut
  above the right eye needing stitches, returned the same quarter; Porter the first
  sub, 19 minutes off the bench (box score; Brew Hoop, Yahoo, Bucks PR via Eric
  Nehm). The card's "undecided" marker stays until game two, per WO-5.

## 4. The carried items

| item | finding (dated) | outlets | action |
|---|---|---|---|
| Strus (D-1005-2) | partial plantar fascia tear, re-evaluated in four weeks, out for the start of the season | ESPN, NBA.com, Hoops Rumors, HoopsHype, CBS Sports | default applied: recovery exclusion, both planes (§1) |
| Hawkins (D-1005-4) | the ledger now carries the 10/2 waiver; ESPN's feed still lists him; not on the box score | ESPN/Shams, NBC Sports, Hoops Rumors; Basketball-Reference ledger (direct) | held under the lock; carried |
| Claxton (D-1005-3) | no new item | Yardbarker NBA notes | note stands; carried |
| Tobias Harris (D-1005-1) | no new item; the Hawks visit 10/8 | NBA.com, ESPN (10/4–5) | carried |
| Coby White (new) | left calf strain in camp, out for the entire preseason, regular-season status not stated | NBA.com 10/5, RealGM, Heavy, SI.com | note; D-1006-2 |
| Lively (excluded) | progressed to shooting, working toward running, no setbacks; misses Macao; 10/21 undetermined | Yahoo, Mavs Moneyball | exclusion stands |
| Beal | still out, right knee inflammation | Hoops Rumors Clippers Notes, Yahoo | note; `inj-hip-risk` stays |
| Knueppel (D-1002-1) | "iffy for opening night"; no change from Lee's 10/4 update | RotoBaller 10/6, NBC Sports | note; the sheet's default holds |
| Bona | not cleared, DNP 10/5; Hukporti (the other backup-C candidate) left the game with a right Achilles injury, imaging Tuesday | Inquirer, Hoops Rumors; the tear [SINGLE-SOURCE] PhillyVoice | note |
| Mikel Brown Jr. | out for the 10/6 opener; Fernández expects him to play in the preseason; contact drills | ClutchPoints, Yahoo | note |
| Anthony Black | not confirmed for the 10/7 opener; full-speed non-contact work | ClutchPoints, Yahoo | note |
| Dru Smith | right calf strain, at least a couple of weeks, could make 10/21 | Hoops Rumors injury notes, HoopsHype | note |
| MEM cut-down | Hawkins (above); Edey held out after a full workout Monday; Jerome started at the point over Pippen Jr.; Post started at C; Stewart 2 minutes | box score; RotoWire, Yahoo, SI.com | notes; carried |
| Alexander-Walker vs Dort | Alexander-Walker started with McCollum (nose contusion) and Dort (right knee contusion) out; both back 10/8 at San Antonio | box score; RotoWire, CBS Sports | notes; one game |
| Queta vs Robinson (BOS) | Queta expected to remain the starter; opener 10/8 at Cleveland | Yahoo, SI.com | no change |
| Steinbach vs Diabaté (CHA) | Charlotte's first game is tonight vs Brooklyn; White out, Knueppel out | Yahoo preview, SI.com | no change; box score next pull |
| Konchar, Vincent, Broome, Bradley | Broome signed MIL (§1); Vincent unsigned, no Heat offer; Konchar still unsigned since the 9/30 waiver; Bradley now on ESPN's Knicks feed and played 6 minutes | RotoWire, CBS Sports, Hoops Rumors, Yahoo; ESPN roster (direct) | Broome moved; Bradley's exemption lapsed; FA rows stand |
| Edey | held out 10/5 after a full on-court workout; opening night trending, preseason appearances unclear | RotoWire, Yahoo, SI.com | note; tag kept |
| Herro | started, 19 minutes, 11 points, first game since the April foot procedure | box score; RotoWire, Yahoo | note; no tag needed |
| Duren | DNP 10/5; back at practice Monday; the plan is a ramp to the 10/20 opener, no preseason date | Detroit News, Yahoo/SI.com, CBS Sports | note |
| Simmons | ruled out 10/5 as planned, no injury; next chance 10/8 or 10/10 | Heavy, Yahoo | note |
| Jaren Jackson Jr. | plays Denver again tonight | ESPN schedule | tag kept; box score next pull |

## 5. Window sweep, box scores, team shadows, injury sweep

- **Transactions (F5 ledger check).** Basketball-Reference's 2026-27 transactions
  page, read directly and parsed (81 dated entries): the newest are 10/2 — Memphis
  waived Jordan Hawkins, Detroit signed Jalen Duren to the multi-year contract,
  Washington signed Jazian Gortman (Exhibit 10). Zero trades since the 9/27
  Charlotte trade-exception entry. The one move in the window on a pool row is
  Broome's signing (10/6, Hoops Rumors, RotoWire); Milwaukee waived John Butler Jr.
  to make room (Hoops Rumors, Heavy) — not a pool row. **Garbles logged:** (1) one
  summary put Monk's and Keegan Murray's next chance at "Thursday (October 10)" —
  Thursday is 10/8 and ESPN's schedule has the Kings at the Lakers that night; (2)
  "Lonzo Ball is with the Utah Jazz, a free agent in 2027" is the 2025 trade item
  again; (3) the Suggs query surfaced "cleared for opener" and "exits preseason game
  vs Mavericks" items from 2025 — the 10/6 RotoWire item (illness, ran at practice)
  is the current one; (4) the Cam Thomas / Ivey summaries recycled the 2025
  qualifying-offer stories with no 10/6 item. (5) My own error, caught by the
  summary: I queried "Chicago Bulls … Coby White" — White is a Hornet (signed there
  in the offseason; the pool has had him on CHA since the 9/30 role pass).
- **Box scores (ESPN summary feed, primary).** 10/5 ATL–MEM (MEM 132–123): Memphis
  started Coward, Boozer (18 min / 11 / 5 / 4 / 2 stl), Wells (17 min / 12, 4-6 from
  three), Post (12 min / 8) and Jerome (15 min / 12 / 5 ast); Grant 14 min / 10,
  Hendricks 19 min / 7 / 6, GG Jackson 16 min / 14, Pippen Jr. 16 min / 10 / 4, Kris
  Murray 13 min / 3, Clayton 13 min / 7, Stewart 2 min; Edey and Hawkins not listed.
  Atlanta started Okongwu, Jalen Johnson (18 min / 8 / 5 / 3), Alexander-Walker (16
  min / 14), Daniels (18 min / 6) and Flemings (25 min / 11); Kispert 20 min / 19,
  Newell 22 min / 12 / 12, Landale 16 min / 4 / 6; McCollum, Dort, Gueye not listed.
  10/5 DET–PHX (DET 109–107): Detroit started Robinson (13 min / 9, 3-3 from three),
  Collins (17 min / 10), Reed (21 min / 10 / 7), Cunningham (16 min / 10), Ausar
  Thompson (18 min / 10 / 3 stl); Holland 24 min / 14 / 5 stl / 2 blk, Huerter 18,
  Joe 18, Jenkins 18, Duren DNP (coach's decision). Phoenix started Brooks, Bridges,
  Ighodaro (14 min / 3 / 5), Booker (16 min / 13), Green (15 min / 11); Maluach 17 min
  / 6, Kennard 15, Goodwin 11, Gillespie 17; Mark Williams DNP. 10/5 PHI–NYK (PHI
  120–97): New York's five starters played 13–15 minutes (Towns 15 / 5 / 5, Brunson 15
  / 12, Anunoby 14 / 12 / 6, Hart 13, Bridges 15); Clarkson 14, Shamet 11 / 10,
  McBride 12 / 0, Bradley 6 / 2, Drummond 12 / 6 / 5 / 3 blk, Wiseman 9 / 8; Alvarado
  DNP. Philadelphia started Wade, Hukporti (5 min, left injured), Caldwell-Pope,
  Jaylen Brown (17 min / 22) and Edgecombe (20 min / 12 / 4 / 7); Embiid, Maxey,
  LeBron, Simons, Bona, Barlow DNP. 10/5 MIL–MIN (MIN 116–97): Milwaukee started
  Kuzma (20 min / 1, 0-6), Jaquez (18 / 5), Turner (19 / 7 / 5 / 1 blk), Herro (19 /
  11 / 3 / 3) and Rollins (14 / 15, fouled out); Ware 24 min / 14 / 12, Trent 18 / 11,
  Porter 19 / 7, AJ Green 22 / 6, Burries 16 / 7 / 5 ast, LeVert 11 / 0; Jakučionis
  DNP. Minnesota started McDaniels, Kuminga, Gobert, LaMelo Ball (17 min / 11) and
  Edwards (18 min / 14); Beringer 15 / 12 / 7, Dosunmu 13, Shannon 16, Hyland 9.
  10/5 SAC–LAL (LAL 127–103): Sacramento started Sabonis (10 min / 4), Hunter (13 /
  3), Achiuwa (13 / 2), LaVine (15 / 9) and Acuff (27 / 19 / 2 / 4 / 1 / 1, 5 TO);
  Clifford 28 min / 23 / 9, Cardwell 29 / 9 / 10 / 3 stl, Raynaud 24 / 12 / 8, Sharp
  30 / 7, Plowden 25 / 12, Karaban 16, Payton 7; Monk, Keegan Murray, Simmons not
  listed. The Lakers started Looney, Ziaire Williams (21 / 13), Thybulle, Dončić (16
  min / 21 / 3 ast / 5 TO) and Grimes (19 / 16); LaRavia 21 / 12, Mamukelashvili 19 /
  8 / 5 ast, Bronny James 16 / 3, Hardy 14 / 8, Knecht 12 / 0; Reaves, Kessler,
  Sexton not listed.
- **Roster verification went direct again.** ESPN's roster API answered for all 30
  teams: 334 of 335 pool rows matched, zero mismatches; Johni Broome the one
  unmatched row, exempted by name (signed 10/6, five outlets, not yet on the feed).
  Tony Bradley now matches (ESPN's Knicks feed, 21 names), ending his exemption.
- **Team shadows.** CHI (Claxton out for the preseason, no new item; first game 10/7
  — Yardbarker), GSW (home preseason opener tonight vs the Lakers, Nellie Night; no
  Porziņģis or Butler item — NBA.com), LAC (Strus four weeks, Beal out, Ingram out —
  Hoops Rumors, Yahoo), MIL (Broome signed, Butler Jr. waived — Hoops Rumors, Heavy),
  NOP (opener tonight at OKC in Tulsa; Mosley's first game — SI.com, NBA.com), POR
  (opener 10/7 vs GSW; Nori "probably" starts Morant and Lillard; Fan Fest scrimmage
  — Blazer's Edge, Yahoo, SI.com), TOR (Kawhi's two-game ramp; Kyle Anderson back to
  full practice — RotoWire, CBS Sports, Yahoo).
- **Injury sweep vs the F6 tag inventory (11 excluded, 34 risk).** Tagged and
  progressing, tags kept by convention: Jaren Jackson Jr. (plays again tonight),
  Edey (full workout, held out), Simmons (held out as planned), Herro untagged and
  played, Kessler (jammed finger, day-to-day), Keegan Murray (held out as a
  precaution), Embiid (healthy inactive), LeBron (healthy inactive), Wells (started,
  12 points), Beal (still out). Still out, tags kept: Butler, Moody, Porziņģis, Mark
  Williams (DNP), Sharpe, Ingram, Lively. Returning-but-untagged: Reaves (ankle
  tweak, "fine"), Sexton ("very light lower-body"), Monk (precaution), Maxey (healthy
  inactive), Suggs (illness) — none needs a tag. New on pool rows: Strus (exclusion,
  §1), Coby White (D-1006-2), Dru Smith (calf, a couple of weeks), Rollins (stitches,
  returned). Not pool rows: Hukporti (Achilles), Kaluma, Isaac (personal), Josh
  Green (knee), Sensabaugh (hip), Grant Williams (hamstring).
- **FA rows.** Kit: Cam Thomas, Ivey, Dillingham, Konchar unsigned; Broome moved.
  Deck adds Lonzo, Vincent and the retired/overseas rows; all on no ESPN roster.
- **Market (F8).** The newest Yahoo paste is 10/01, five days old; 297 of 335 rows
  priced. A fresh paste sharpens the Mkt column and the TARGET shelf counts.

## 6. Board effects (computed, never eyeballed)

- **Kit.** `top-200-2026-27.md` regenerated against the pre-pull snapshot: no
  entries, no exits, no move of three or more, zero one- or two-place
  displacements, no team change on the board — Strus (GP 25) and Broome (MIL) both
  sat outside the top 200 before and after; the only changed line is the generation
  date. 325 projected rows, unchanged.
- **Deck.** By adjusted value over the draftable rows (324 → 323): Max Strus exits
  (was 194, excluded); no entries; no move of three or more; 130 one-place shifts,
  all of them the rows below 194 moving up one as his row left. Acuff Jr. 179 → 179,
  Coby White 57 → 57, Broome 319 → 318. Pool sha256 `48456b3b18ff` (was
  `7729dd246981`); 335 rows.

## 7. Deck build and publish

`build_deck.py` on 2026-10-06: roster verification direct-complete, 334/335 against
all 30 official rosters, 0 mismatches, 1 exemption by name (Broome); freshness
stamped with the pool-changes note; JUDGMENT re-dated 2026-10-06 — the ten open cards
re-authored with this pull's receipts, none added or removed, all ten still flagged
by the enumerator; colophon Data paragraph rewritten for the window; planes 315
shared, team 0, exclusion 0, drift 0, propagation 0, waived 1 (Strus, the exclusion
twin, recorded in the manifest); market `yahoo-2026-10-01.csv`, 297 of 335 priced, 5
days old. No engine or card change this pull; v44 differs from v43 in data and prose
only.

**The build refused twice before it passed, both my doing, both diagnosed before
patching (surprise rule).** (a) Gate 6 refused a colophon that said "334/335" — the
gate wants the pool count on both sides of the slash, so the exemption is prose, not
arithmetic; fixed in the script. (b) The post-write integrity check reported that the
injected data did not round-trip. Cause, found by diffing the injected and read-back
strings: the Rollins row's existing `[SINGLE-SOURCE: SI Bucks]` label, followed by
this pull's standard `; 10/6:` join, formed the two characters `];` inside the JSON —
exactly the end anchor of the build's non-greedy `const PLAYERS = [...];` regex, so
the read-back stopped 2,000 characters early. The failed write also left today's pool
hash in the page's manifest, which made the next attempt refuse for "pool changes
asserted but CSV byte-identical to the last published build". Route-around: the label
wrapped in parentheses (no note in the pool now ends `]` before a `;`), the page
restored from v43 and re-authored, the build re-run clean. The trap is latent for any
future note ending in `]` (Filipowski's 10/5 note does) and belongs to the build
script, not the data — on the sheet as D-1006-3 with the patch.

## 8. Gates (2026-10-06)

| gate | result (evidence: the command's own output line) |
|---|---|
| kit `check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-10-06 |
| kit `check_derived.py` | all 13 dated artifacts reproduce byte-for-byte from their pinned inputs |
| kit `check_report.py` on this file | REPORT GATE: PASS (structure, publication rule, pull-log row) |
| deck `judgment_open_items.py --check-report` on this file | receipts check PASS — all 10 flagged names carry a receipts row |
| deck `verify_rosters.py --allow-unmatched` | direct-complete via site.api.espn.com (all 30 rosters): 334/335 checked, 0 mismatches, 1 unmatched exempted by name (Johni Broome, signed 10/6) |
| deck `check_planes.py` (in the build) | 315 shared · team 0 · exclusion 0 · drift 0 · propagation 0 · waived 1 (Max Strus, the exclusion twin) · lines 171 (warning by design) |
| deck `build_deck.py` | deck built: 335 players · pull 2026-10-06 · pool 48456b3b18ff · injection round-trip OK; safe to publish (market `yahoo-2026-10-01.csv`, 297 of 335 priced, 5 days old) |
| deck `check_parity.py` on the built page | PARITY: EXACT MATCH |
| deck `test_card.py` / `test_draft.py` / `test_gates.py` | CARD: all 89 cases passed / all 65 cases passed / all 37 cases passed (no code change this pull, so no red-first case) |
| deck step-5b `full_dom_check.mjs` on the built page | 128 assertions, 0 failed, 0 page errors, exit 0 (`arena/results/full_dom_check_2026-10-06_v44.json`) |
| artifact publish | Version 44 (id `1791304560-ccae`) at the standing URL; page 398,264 bytes, sha256 `6997f2adc5dac644…`, identical to the built file |

## 9. Watchlist / open items

- **Tonight's four games** — CHA–BKN (Steinbach vs Diabaté at center; White and
  Knueppel out; Brown Jr. out for Brooklyn), OKC–NOP in Tulsa (Mathurin's rotation,
  the reprice checkpoint), UTA–DEN again (Jaren Jackson Jr., Filipowski, Jamal
  Murray), GSW–LAL (Reaves and Kessler day-to-day; Porziņģis, Butler out). 10/7:
  POR–GSW (Sochan; Morant and Lillard together), ORL–MEM (Suggs, Black, Edey). 10/8:
  SAC at LAL (Acuff's game two — D-1006-1's checkpoint; Monk, Keegan Murray,
  Simmons), ATL at SAS (McCollum, Dort, Tobias Harris), BOS at CLE (Queta).
- **WO-5, the projection refresh** — starts when every team has played twice; ten
  teams have one game after tonight's slate, the earliest the threshold lands is
  still about 10/9–10/10.
- **Acuff Jr.** — D-1006-1; game two 10/8.
- **Strus** — excluded; re-entry needs two outlets on a cleared return (re-evaluation
  about 11/2).
- **Hawkins** — moves to FA the pull ESPN's feed reflects the waiver, or the pull the
  owner overrides the lock (D-1005-4).
- **Broome** — the by-name exemption ends when ESPN's Milwaukee feed lists him.
- **Coby White** — D-1006-2; the regular-season status is the next item.
- **The build regex trap** — D-1006-3; the Filipowski note already ends in `]`.
- **Claxton, Tobias Harris** — re-evaluation dates about 10/19 and after 10/16
  (D-1005-3, D-1005-1).
- **Lively** — back to the draftable pool when two outlets report him cleared.
- **Knueppel** — D-1002-1 stands; the trigger is a ruling-out for the 10/21 opener.
- **Market** — the Yahoo paste is five days old; a fresh one is the owner's input.
- **Owner decisions carried:** D-BV1 (Butler), D-30-3, D58-2..D58-5, D-R1..D-R4,
  D-G2, D-G4..D-G7, D-P1..D-P4, D-1001-1/3, D-ADP-1/2, D40-1/3, D-LS-1/3, D-1002-1,
  D-1002-3, D60-1..D60-4, D-1005-1, D-1005-3, D-1005-4; D-1005-2 closed today
  (default applied).

## Open-item receipts

| player | query run | dated finding |
|---|---|---|
| Brandon Ingram | Brandon Ingram Clippers Achilles update October 6 2026 | out for the start of the season, light on-court work, no timetable — Bleacher Report, ESPN; HELD |
| Kristaps Porzingis | Kristaps Porzingis Warriors status update October 6 2026 | out indefinitely, did not travel to Hawaii, no new statement; trade chatter is speculation — NBA.com, Bleacher Report, Yahoo; HELD |
| Kawhi Leonard | Kawhi Leonard Raptors preseason ramp up October 6 2026 · Toronto Raptors news October 6 2026 Kawhi | misses the 10/10 Vancouver game too, workouts this week — NBA.com Starting 5, RotoWire, SI.com; HELD |
| Cam Thomas | Cam Thomas OR Jaden Ivey free agent signs October 6 2026 | unsigned; only the 2025 qualifying-offer item surfaced — Spotrac, NBC Sports (garble logged) |
| Jaden Ivey | (same query) | unsigned — Spotrac, Heavy |
| Jeremy Sochan | Jeremy Sochan Trail Blazers roster camp deal October 6 2026 · Portland Trail Blazers news October 6 2026 preseason opener Sochan Morant | Exhibit 9 camp deal; first game 10/7 vs GSW, Nori "probably" starts Morant and Lillard — Blazer's Edge, Yahoo, SI.com; HELD |
| Lonzo Ball | Lonzo Ball OR Rob Dillingham free agent workout signs October 6 2026 | unsigned — Spotrac, Yahoo; the Jazz item is 2025 (garble) |
| Rob Dillingham | (same query) | unsigned, any team but Chicago — Hoops Rumors, RotoBaller, Spotrac |
| Bennedict Mathurin | Pelicans Thunder preseason opener October 6 2026 Mathurin starting lineup rotation · New Orleans Pelicans news October 6 2026 | first game tonight at OKC in Tulsa, no lineup published — SI.com, NBA.com; HELD |
| Ryan Rollins | Bucks Timberwolves preseason October 5 2026 recap Rollins Herro Porter · Ryan Rollins elbow eye injury Bucks status October 6 2026 · ESPN box score 10/5 (fetched) | started at PG, 15 pts in 14 min, fouled out; stitches above the right eye, returned; Porter the first sub — box score, Brew Hoop, Yahoo, Bucks PR/Nehm; HELD, one game |
| Darius Acuff Jr. | Darius Acuff Jr. Kings Lakers preseason October 5 2026 · Darius Acuff Kings starting point guard role minutes Doug Christie October 2026 · Kings Lakers preseason recap October 5 2026 · Darius Acuff fantasy basketball rookie 2026-27 draft value sleeper · Kings depth chart 2026-27 point guard Acuff Simmons Monk · Darius Acuff summer league Kings expectations · Kings Acuff Christie postgame comments · basketball-reference.com/players/a/acuffda01.html (fetched) · ESPN box score 10/5 (fetched) | §2 — started at PG, 27 min, 19 pts, 5 TO; starter on every depth chart, "30-plus minutes" per RotoWire; Arkansas line read directly; Summer League .350 FG — Yahoo, Sactown Sports, SI.com, Heavy, RotoWire, CBS Sports, FantasyAlarm, NBC Sports Bay Area; D-1006-1 |
| Max Strus | Max Strus foot injury MRI results Clippers October 6 2026 · Los Angeles Clippers news October 6 2026 Beal Ingram Strus | partial plantar fascia tear, four weeks, out for the start of the season — ESPN, NBA.com, Hoops Rumors, HoopsHype, CBS Sports; exclusion (D-1005-2 default) |
| Johni Broome | NBA transactions October 6 2026 signed waived traded · Milwaukee Bucks sign Johni Broome October 6 2026 · ESPN MIL roster (fetched, direct) | signed by the Bucks 10/6, Butler Jr. waived — RotoWire, CBS Sports, Hoops Rumors, Yahoo, Heavy; not yet on ESPN's feed; FA → MIL, exempted by name |
| Jordan Hawkins | Jordan Hawkins waived Grizzlies clears waivers signs October 2026 · basketball-reference.com NBA_2027_transactions (fetched) · ESPN MEM roster (fetched, direct) | waived 10/2 on the ledger and per ESPN/Shams, NBC Sports, Hoops Rumors; still on ESPN's feed; held (D-1005-4) |
| Coby White | Chicago Bulls news October 6 2026 Coby White calf strain · nba.com/news index (fetched) | left calf strain, out for the entire preseason — NBA.com 10/5, RealGM, Heavy, SI.com; note (D-1006-2) |
| Dereck Lively II | Dereck Lively Mavericks update October 6 2026 | shooting, working toward running, no setbacks; misses Macao; 10/21 undetermined — Yahoo, Mavs Moneyball; exclusion stands |
| Bradley Beal | Los Angeles Clippers news October 6 2026 Beal Ingram Strus | still out, right knee inflammation — Hoops Rumors Clippers Notes, Yahoo |
| Kon Knueppel | Kon Knueppel hamstring update October 6 2026 Hornets | "iffy for opening night"; no change — RotoBaller, NBC Sports; D-1002-1 holds |
| Adem Bona / Ariel Hukporti | Adem Bona 76ers foot OR Ariel Hukporti injury update October 6 2026 · ESPN box score 10/5 (fetched) | Bona not cleared, DNP; Hukporti left after 5 min, right Achilles imaging — Inquirer, Hoops Rumors; tear [SINGLE-SOURCE] PhillyVoice |
| Mikel Brown Jr. | Mikel Brown Jr. Nets ankle update October 6 2026 preseason opener Hornets | out 10/6; expected to play in the preseason, contact drills — ClutchPoints, Yahoo |
| Anthony Black | Anthony Black Magic ankle status preseason opener October 7 2026 | not confirmed for 10/7; full-speed non-contact — ClutchPoints, Yahoo |
| Dru Smith / Gabe Vincent / John Konchar | Gabe Vincent OR John Konchar OR Dru Smith signs OR update October 6 2026 | Smith calf, a couple of weeks — Hoops Rumors, HoopsHype; Vincent and Konchar unsigned — Yahoo, Hoops Rumors |
| Jalen Suggs | Jalen Suggs Magic illness status preseason opener Grizzlies October 7 2026 · NBA injury news October 6 2026 preseason | illness, ran at Tuesday's practice, uncertain for 10/7 — RotoWire 10/6, Yahoo; the 2025 items logged as garbles |
| Zach Edey | Zach Edey Grizzlies status Magic preseason October 7 2026 · Hawks Grizzlies preseason October 5 2026 recap | held out 10/5 after a full workout; opening night trending — RotoWire, Yahoo, SI.com |
| Jalen Duren | Pistons Suns preseason October 5 2026 recap Duren Mark Williams · Jalen Duren Pistons return preseason timeline Bickerstaff October 6 2026 · ESPN box score 10/5 (fetched) | DNP; back at practice Monday, ramp to 10/20 — Detroit News, Yahoo/SI.com, CBS Sports |
| Ben Simmons / Malik Monk / Keegan Murray | Malik Monk Keegan Murray Kings preseason opener out October 5 2026 · ESPN SAC roster + schedule (fetched, direct) | all three held out 10/5 as precautions, no injuries; next game 10/8 at LAL — Heavy, Yahoo; the "October 10" summary logged as a garble |
| Austin Reaves / Walker Kessler / Collin Sexton | Lakers Kings preseason Austin Reaves Collin Sexton Walker Kessler out October 5 2026 · ESPN LAL roster (fetched, direct) | ankle tweak, jammed finger, light lower-body; all day-to-day, "fine" per Redick — Silver Screen and Roll, Yahoo, SI.com, Heavy |
| Nickeil Alexander-Walker / Luguentz Dort / CJ McCollum | Hawks McCollum Dort out Grizzlies preseason reason October 5 2026 · ESPN ATL roster (fetched, direct) | NAW started; Dort right knee contusion, McCollum nose contusion, both back 10/8 — RotoWire, CBS Sports |
| Tyler Herro / Kel'el Ware / Myles Turner / Kevin Porter Jr. | Bucks Timberwolves preseason October 5 2026 recap · ESPN box score 10/5 (fetched) | Herro started 19 min / 11; Turner started, Ware 24 min / 14 / 12 off the bench; Porter the first sub — box score, Brew Hoop, RotoWire, Yahoo |
| VJ Edgecombe / Joel Embiid / Tyrese Maxey / LeBron James | 76ers Knicks preseason October 5 2026 recap · ESPN box score 10/5 (fetched) | Edgecombe started 20 min / 12 / 7 ast; Embiid, Maxey, LeBron healthy inactives — NBC Sports Philadelphia, CBS Philadelphia, Inquirer |
| Ty Jerome / Scotty Pippen Jr. / Quinten Post / Cameron Boozer / Jaylen Wells | Hawks Grizzlies preseason October 5 2026 recap · ESPN box score 10/5 (fetched) | Jerome started at PG over Pippen Jr.; Post started at C; Boozer and Wells started — box score, SI.com, Yahoo, Fox 5 Atlanta |
| Neemias Queta / Mitchell Robinson | Celtics Queta Mitchell Robinson starting center preseason opener October 2026 | Queta expected to remain the starter; opener 10/8 — Yahoo, SI.com |
| Hannes Steinbach / Moussa Diabaté | Hornets Nets preseason October 6 2026 preview Steinbach Diabate Knueppel White | first game tonight; no decision — Yahoo, SI.com |
| Tony Bradley | ESPN NYK roster (fetched, direct) · ESPN box score 10/5 (fetched) | on the feed now, 21 names; 6 min / 2 pts — exemption lapsed |
| (window ledger) | NBA transactions October 6 2026 signed waived traded · basketball-reference.com NBA_2027_transactions (fetched, 81 entries parsed) · nba.com/news (fetched) | 10/2 Hawkins waived, Duren signed, Gortman signed; 10/6 Broome signed MIL — Hoops Rumors, RotoWire; zero trades since 9/27 |
| (injury sweep) | NBA injury news October 6 2026 preseason · NBA "cleared" OR "full participant" OR "returns to practice" October 6 2026 · Jazz Nuggets preseason October 6 2026 … status | §5 — Hukporti, Isaac, Suggs; Kyle Anderson full practice; Green, Sensabaugh, Filipowski out 10/4 — RotoWire, CBS Sports, Yahoo |
| (preseason) | ESPN scoreboard 10/5, 10/6 (fetched, direct) · five ESPN summaries (fetched) | five games in the window, four tonight; box scores in §5 |
| (team watch, 7) | "<Team> news October 6 2026" one each: CHI, GSW, LAC, MIL, NOP, POR, TOR | §5 |

## Bounds

- Direct-complete roster verification proves membership, not role; the one exempted
  row rests on five outlets for a same-day signing.
- A single preseason box score is a dated primary record, not a reprice mechanism
  (A2); the lines move at the WO-5 refresh after two games per team. The Acuff
  sensitivity in §2 is a what-if computed in scratch, not a change.
- The Strus exclusion is the owner's 10/5 default applied, a convention and not a
  medical read; if the owner prefers the Knueppel treatment (risk tier, draftable),
  D-1006-4 reverses it in one script.
- The Hawkins hold follows the feed by design; the ledger and four outlets now say
  waived. Overriding needs a verifier exemption for mismatches, a code change.
- The kit and deck boards did not move beyond the Strus exit; no line changed.
- Hoops Rumors, Yahoo, SI.com, Wikipedia and most sports domains are egress-blocked;
  their items rest on dated search summaries, as on every prior pull; four summary
  garbles and one query error of mine were caught (§5). ESPN's article pages return
  empty bodies to this session; its API endpoints answer.
- The build's PLAYERS regex trap (§7) was routed around in data, not fixed in code.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-1006-1 | Acuff Jr.: the role is confirmed (starter, 27 minutes in the opener, "30-plus" per RotoWire); the rates are not. (a) Hold the 29-minute line until WO-5 after game two on 10/8, per the pool's own rule; (b) reprice minutes now to 32 (kit 190 to 153, deck 179 to 148); (c) reprice minutes and shooting now (32 min, .455 FG, 2.7 3PM: kit 118, deck 114). Either reprice moves both planes in one script with the diff in the next report | (a) hold until game two |
| D-1006-2 | Coby White: left calf strain, out for the entire preseason, regular-season status not stated (NBA.com, RealGM, Heavy). Tag `inj-calf-risk` (0.78) now, or hold untagged until the Hornets state his opener status? | hold untagged (the Harris treatment, D-1005-1) |
| D-1006-3 | The build's PLAYERS regex ends at the first `];` — a note ending in `]` followed by the `; ` join breaks the round-trip (today's Rollins case; Filipowski's note already ends in `]`). Patch: anchor on `];\n` with a sentinel comment after the block, red-first in `test_gates.py`, parity and DOM re-run. Patch now in a separate deck PR, or at the next deck code change before WO-7 (10/13)? | patch before WO-7, separate PR, red-first |
| D-1006-4 | Strus: keep the recovery exclusion (convention: no cleared return) or re-tag `inj-foot-risk` (0.78) so he stays a late stash with a mid-November return in view? He was deck rank 194, outside a 156-pick room either way | keep the exclusion |
| D-1005-4 | Hawkins: the Basketball-Reference ledger and four outlets (ESPN/Shams, NBC Sports, Hoops Rumors, Yahoo) say waived; ESPN's feed still lists him. Keep the lock (move when the feed catches up) or override — which needs a by-name mismatch exemption in `verify_rosters.py`, a small code change? | keep the lock |
| D-1005-1 / D-1005-3 | Harris, Claxton tags | carried: hold until ruled out of the opener / the 10/19 re-evaluation |
| D-1002-1 | Knueppel's tag | carried: hold until ruled out of the opener |
| D-1002-3 | camp first-unit signals, now one game each (Lendeborg, Jackson over Lopez, Rollins, Jerome over Pippen Jr., Reed with Duren out) | carried: hold for WO-5 after two games |
| D60-1..D60-4 | the port's tie-break, Murray-Boyles, the advice-line wording, closing D-G3 | carried, owner silent |

## Provenance and bounds

- Inputs: ESPN's scoreboard and summary feeds for 10/5–10/6 (fetched 2026-10-06),
  ESPN's roster API for all 30 teams (fetched by the verifier) and seven rosters plus
  the Kings' schedule by hand; Basketball-Reference's 2026-27 transactions page and
  Acuff's player page (fetched 2026-10-06); NBA.com's news index (fetched); 46 dated
  web-search summaries (2026-10-04 → 2026-10-06); the owner's request; the committed
  10/05 pools and boards as the pre-pull snapshots.
- Every number in §2's table and §6 is a script run (`scratchpad pull1006/`), every
  gate line is the command's own output.
- Not verified: Wikipedia's Acuff and Kings-season pages (egress-blocked); nothing
  here rests on a direct read of a blocked sports domain.

## In plain language

**What this pull did.** One day since Monday's pull, and five more preseason games
in it. Before any news search I read all five box scores straight from ESPN's feed,
then swept the news, checked every player's team against ESPN's live rosters for all
30 clubs, and rebuilt and republished the deck.

**Your Acuff question, short version.** The role part is real. He started at point
guard, played 27 minutes (more than any other Kings starter; Sabonis played 10,
LaVine 15), scored 19, and every depth chart and beat writer has him as the starter
with "30-plus minutes" expected. Both boards already pay for that: his line has been a
29-minute starter line since the 9/30 role pass, the fifth-highest minutes of any
rookie in the pool.

The contributions part is where your league's scoring bites. In nine categories a
volume scorer who shoots .430 with 2.6 turnovers is negative in two categories before
his points and assists count. His Arkansas year says the shooting can be much better
(.484 overall, .440 from three); his Summer League (.350, .278) and last night (8 of
17, five turnovers) say it has not carried over yet. I ran the what-ifs on both
boards: three more minutes lift him about 35 places; the shooting carrying over lifts
him another 35; both together make him a round-10 value; the Summer League version of
him is undraftable. One preseason game answers none of that, and the pool's own rule
is that lines move at the projection refresh after game two (Thursday at the Lakers).
So the line holds today, with the numbers on your sheet as D-1006-1 if you want the
reprice now. Either way he is a last-round name at Yahoo's ADP of 155, so waiting
costs nothing.

**Two rows moved, both your own defaults from Monday.** Max Strus has a partial tear
of the plantar fascia in his right foot, is re-evaluated in four weeks and misses the
start of the season; your D-1005-2 default was to apply the convention once the
diagnosis came, so he is a recovery exclusion on both boards (he was deck rank 194,
outside a 13-round draft anyway; D-1006-4 lets you keep him draftable instead). Johni
Broome signed with Milwaukee and moves from free agent to the Bucks; ESPN's feed does
not list him yet, so he carries a by-name exemption until it does.

**One row still waiting.** Basketball-Reference's transaction ledger now records that
Memphis waived Jordan Hawkins on 10/2, and he was not on last night's box score, but
ESPN's roster feed still lists him. The deck's rule follows the feed, so his row stays
on Memphis one more day (D-1005-4 if you want to override).

**What the other games said.** Ryan Rollins started at the point for Milwaukee and
scored 15 in 14 minutes before fouling out, with Porter the first sub. Ty Jerome
started over Pippen Jr. in Memphis; Paul Reed started at center with Duren held out;
Edgecombe, Boozer and Flemings started. Herro played 19 minutes in his first game
back. Embiid, Maxey, LeBron, Simmons, Monk, Keegan Murray, Reaves, Kessler and Edey
all sat as precautions. New injury: Coby White is out for the preseason with a calf
strain, untagged for now with the choice on your sheet (D-1006-2).

**What broke and what I did.** The deck build refused twice. Once was a colophon
wording the gate wants a certain way. The other was a real trap: a note that ended in
a square bracket, followed by the usual "; 10/6:" join, produced the two characters
the build uses to find the end of its data block, so the page read back short. I
found it by diffing the written and read-back data, routed around it in the data
(parentheses around the label), restored the page and rebuilt clean. The proper fix is
in the build script and is on your sheet as D-1006-3, because another note already
ends the same way.

**What I did not change.** No line, no existing player's tag except Strus, no team
except Broome. The kit board did not move at all; the deck board only lost Strus.

**What I caught.** Four stale or wrong items in the search summaries (a 2025 Lonzo
item, 2025 Suggs items, recycled Cam Thomas and Ivey stories, and "Thursday October
10" where Thursday is the 8th), plus one mistake of mine: I queried Coby White as a
Bull. He is a Hornet, and the summary corrected me.

**Verification.** The rebuilt deck passed every gate: the page and the Python agree
exactly, all 191 test cases pass, the browser robot drafted a full room with 128
checks and zero failures, and Version 44 is live at the usual link.

**Your decisions.** D-1006-1 Acuff reprice (default: hold until Thursday's game).
D-1006-2 Coby White tag (default: hold). D-1006-3 the build regex patch (default: a
separate PR before 10/13). D-1006-4 Strus exclusion vs risk tier (default: keep the
exclusion). D-1005-4 Hawkins (default: keep the lock). Harris, Claxton, Knueppel and
the camp-signal question are carried.

**Next.** Four games tonight (Hornets, Pelicans, Jazz, Warriors) and Acuff's second
game Thursday. The projection refresh starts once every team has played twice,
likely 10/9 to 10/10. A fresh Yahoo paste would sharpen the price column; the current
one is five days old.
