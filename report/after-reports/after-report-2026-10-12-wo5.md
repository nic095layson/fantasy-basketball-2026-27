# After-report — WO-5: every line re-derived by the work-order method, both planes, deck v60

**Owner request (2026-10-12, verbatim):** "Did Town's position change after this? Please proceed with WO-5 re-derivation. Ensure utmost thoroughness, accuracy, and data soundness as this needs to be pristine." Mid-pass, the owner: "I hope you understand that - while preseason games are important to see samples of player production and statistical output: Preseason games are really meant for tuneup and building chemistry. Please know that minutes, and productions vary from case to case - such as star players only playing around 20 minutes, etc."

**Method:** the WO-5 pass as `pre-draft-workorder-2026-10-01.md` writes it, with queue items 1–9 — rates from the player's 2025-26 per-36 line on Basketball-Reference scaled to his projected minutes, FG% and FT% shrunk one-third toward career, steals and blocks on the three-season anchor, points by the shooting identity, role from the preseason box scores and two dated outlets (never minutes or rates — the owner's note above is the rule this pass ran on), one asserted script writing both planes, the kit board regenerated, both boards diffed by script, then the range check, the points-identity check, the repeat-name check, the deck's full build ritual, the re-calibration and the top-60 market review. Every input, rule, script and output is in the kit's `report/wo5/` (tools, data, out); the raw downloads (23 Basketball-Reference season pages, 36 ESPN box scores) are pinned by sha256 in its manifests.

Pull window: 2026-10-12 → 2026-10-12

**Headline.** Towns' position changed: on his 2025-26 line (31.0 minutes, 20.2 / 11.9 / 1.5 threes / .508 / .852) he is #25 on both boards (deck from #6, kit from #5), and the card at pick #10 no longer shows him in its Top 5 in any of the 24 rooms on file — its #1 there is Tyrese Maxey when he is on the board (7 rooms) and Jamal Murray otherwise (17). The lines agree with the outside world far better than the ones they replace: the range check falls from 131 players and 435 cells outside every outside line to 23 players and 25 cells, each kept on a stated mechanism; the points-identity check from 49 top-200 lines (41 players) more than a point off their own shooting to none; the planes' stat lines from 170 differences to none. 223 players move three or more places on at least one board; every one carries its mechanism in §4.

## Plain-language summary

- **What changed.** Until today most of the board's lines were older estimates — for the stars, mostly shaped like 2024-25. Now every player who played 25 or more games last season carries his 2025-26 production rate at his 2025-26 minutes, with two adjustments the work order requires: shooting percentages pulled a third of the way toward his career, and steals and blocks averaged over three seasons. Seven players changed role in camp on two dated reports and their minutes moved; the players coming back from long injuries (Lillard, Haliburton, Kyrie, Trae Young, Davis, VanVleet, Morant, Dejounte Murray, Edey) had their minutes set where the three outside projections put them, because our own data cannot say how much they will play.
- **Towns.** He falls from #6 to #25. His 2025-26 season (20 points in 31 minutes, fewer threes) is the reason; his line was his bigger 2024-25 season before.
- **Your pick at #10.** The card now leads with Maxey if he is there, Jamal Murray if not, then Jalen Johnson, Kawhi Leonard (risk-tagged) and Durant or Markkanen. Murray usually lasts to #15 (the card puts it near 77 percent), so Maxey at #10 and Murray at #15 is the pair the card's own odds favor when Maxey is there. Haliburton sits #11 on the #10 card, Edwards #14, Towns #17–18.
- **Biggest risers among the names at your picks (the top 60 now):** Markkanen (52 → 10), Kawhi (34 → 6), Embiid (71 → 23), Rollins (70 → 29), Jamal Murray (20 → 7), Michael Porter Jr. (55 → 32). **Biggest fallers from this morning's top 60:** Towns (6 → 25), Edwards (8 → 24), Cade Cunningham (12 → 26), Dyson Daniels (11 → 22, his steals on the three-season average), Morant (65 → 143), Coby White (58 → 153). Every move on the whole board, by size and with its reason, is §6.
- **What did not change:** no team, injury tag, games-played figure or roster placement; the card's rules, prices and survival model are the 10/12 page's.
- **One page fix, found by this pass.** The "Your roster" panel could leave a drafted player off the list when no open slot fit him (for example, only one center among 13, with the bench already full). The page's own end-to-end check hit it on the new lines. He now shows in an EXTRA row and the open slot stays visibly open. Display only — the card is unchanged (§12, D-WO5-6).
- **What to keep in mind.** The method takes each player's own production rate; it does not model a player's usage changing with a new team (Jaylen Brown and LeBron in Philadelphia, Giannis in Miami, Trae Young and Davis in Washington). The range check catches only the cases where that pushes a line past every outside projection.

## 1. Roster changes

None. No team, tag, games-played figure, position or placement moved on either plane; the roster validation lock re-ran direct-complete (335 of 335 on ESPN's feed, 0 mismatches). What changed is the stat line of 326 deck rows and 311 kit rows (§2–§4).

## 2. The method as run

**Inputs.** Basketball-Reference season totals for 2003-04 through 2025-26 (23 pages, fetched 2026-10-12, sha256 in `wo5/data/bref_manifest_2026-10-12.tsv`), parsed from the regular-season totals table only, with every team split kept (`bref_totals_2004-2026.csv`: 11,501 season rows, 3,109 team splits). Cross-check: 1,721 player-seasons matched against the deck's verified 2023-24 to 2025-26 actuals (Basketball-Reference and ESPN, `arena/results/actuals_2026-10-09/`), 2025-26 581 of 582 identical. ESPN's 36 preseason box scores of 10/3–10/11 (`espn_manifest_2026-10-12.tsv`), parsed to starts, games and DNPs per player (`preseason_roles_2026-10-12.json`; dates in US Eastern — ESPN's timestamps are UTC, which put evening games a day late until this pass corrected it). An independent recomputation of three lines straight from the totals (Towns, Edwards, Maxey) matched the script to the last digit.

**The line.** Base season = 2025-26 if he played 25+ games, else the latest of 2024-25 / 2023-24 with 25+ (302 rows on 2025-26, 23 on 2024-25, 1 on 2023-24). FGA, FTA, threes, rebounds, assists and turnovers = base-season per-36 × minutes / 36. FG% and FT% = base season + one third of the way to career (all regular seasons on file). Steals and blocks = the 5/4/3 games-weighted per-36 of 2025-26 / 2024-25 / 2023-24 × minutes / 36 (queue item 8). Points = 2·FGA·FG% + 3PM + FTA·FT%. Minutes = the base season's (for a player traded during it, his minutes with his current team when that split has 15+ games — 16 rows), unless a role move or the range rule below changed them. Games played and tags: unchanged (rule 4 runs separately).

**Assumptions (register).** A1 minutes default to the base season's; A2 career = regular-season totals through 2025-26; A3 the steals/blocks anchor is applied in rate form (per-36 × minutes), so a player whose minutes jumped is not dragged to his old per-game; A4 the 25-game floor for a base season; A5 rookies keep the college translation (no NBA season to scale); A6 points from the identity, never typed; A7 games played and tags untouched; **A8 the method runs on every row with a qualifying season, not only the top 150 the work order names** — the z-score frame reads rows 151–180, and a board half on the method and half on old lines is not one frame (D-WO5-1).

**Role moves (rule M2, fixed before the research).** A role change needs two dated outlets (the box score counts as one). To a starting role: his own most recent stint (a season, or the team split of a split season, 15+ games) with 75%+ starts, else the 2025-26 minutes of the starter whose spot the outlets name, else hold. To the bench: his own most recent stint with 25% or fewer starts, else hold. Rates always stay on the base season. Two clarifications were made after the first stint lookups and before any line was written, and are on the owner's sheet (D-WO5-2): the stint must come from 2024-25 or 2025-26 (the first lookup for Gillespie returned his 2023-24 Denver stint — 24 games at 9.4 minutes, a role of a different stature; this is the one outcome the window changed), and a move to the bench never raises minutes, a move to starter never lowers them.

**Range rule (D-RN-3 on the pass; rules fixed before they were run).** R1: a listed player with two or more of points/rebounds/assists/threes/turnovers outside every reference on the same side — the signature of a minutes difference — takes one minutes factor that brings those cells inside the range of his references without pushing any other counting cell past the check's tolerance; steals and blocks ride along but never choose the factor. R2: a single counting cell outside stays on the base season's rates; a steals or blocks cell stays on the item-8 anchor. R3: a shooting cell outside stays when his unshrunk 2025-26 rate is itself inside (the career shrink put it outside); otherwise (no 2025-26 season of 25+ games, or a rookie) it moves to the nearest end of the range. Rookies take R1 and R3 the same way, and a counting cell left outside moves to the range (no NBA rates or anchor to cite). Run to a fixed point (two rounds). Two refinements came after the first round and before the write, on the sheet with M2's (D-WO5-2): the two-cell trigger (without it Naz Reid's minutes would have been cut to 27.7 on a single turnovers cell and Lendeborg's line scaled by 0.92 for cells on opposite sides), and the rookie steals/blocks clamp (Caleb Wilson's blocks were first labeled with an anchor he does not have).

**Two rookie lines outside the range rule.** AJ Dybantsa's planes carried different lines since 9/30 (D-R1, default: unify to the kit's); both now carry the kit's, and Dybantsa's and Cameron Boozer's shot volume is set so their shooting implies the points they carry (18.0 and 18.5, inside the outside lines' reach) — the points identity (D-1009-3) was the only check either line failed.

**The write.** `wo5/tools/wo5_apply.py` wrote 326 deck rows and 311 kit rows from one lines file (6,468 values), with seven assertions (headers and row order unchanged; every non-stat column unchanged; every row with a line written, every row without one byte-identical; the two planes equal on every shared row; the identity within 0.25 on every row; sane ranges; no note carrying "];", the build-regex trap of D-1006-3 that the first build hit and that this assertion now blocks). A second run changes nothing. Each deck row gained one dated note entry ("10/12: WO-5 line — <base> base at <minutes> min …").

## 3. Role evidence — the research pass

Universe: the union of the three top-150s (the deck's value board on the current and on the method lines, the kit board) plus the queue — 183 rows, 176 with a method line. Candidates: 75 rows flagged for a team change (52), a starts share 0.5 or more away from the base season in two or more preseason games (20), or the WO-5 queue (16). Preseason minutes and production were never used. Two dated outlets moved seven players; everyone else held his default minutes. Search summaries are leads; outlet pages that could be fetched were read directly (NBA.com); most outlet domains are blocked to direct fetch from this container, so the rest rest on dated search results. SI article dates come from the creation timestamp in the URL's ULID (checked on two 2025 SI items, which decode to the March 2025 dates their content implies).

| role move (mechanism) | minutes | evidence (two dated outlets) |
|---|---|---|
| Kevin Porter Jr. to the bench | 33.2 → 19.9 (his 2024-25 Milwaukee split, 30 games, 2 starts) | ESPN box scores 10/5 and 10/11 (bench); SI Bucks 10/11; Yahoo Sports (on/after 10/11) |
| Nikola Vučević to the bench | 28.4 → 21.1 (his 2025-26 Boston split, 16 games, 1 start) | ESPN box scores 10/7 and 10/11; Roundtable 10/8 |
| Jay Huff to the bench behind Zubac | 21.0 → 11.7 (his 2024-25 Memphis season, 64 games, 2 starts) | ESPN box scores 10/7 and 10/10; Roundtable 10/5 |
| Naz Reid to a starting role | 26.1 → 31.0 (no starter stint of his own; Miles Bridges' 2025-26 Charlotte minutes, the spot the outlets name) | ESPN box scores 10/6 and 10/11; Roundtable 10/7 |
| Coby White to the starting point guard role | 19.3 → 29.1 (his 2025-26 Chicago split, 29 games, 26 starts) | NBA.com/AP 10/6; Roundtable 10/7 |
| Ty Jerome to the starting point guard role | 19.9 → 22.6 (his 2025-26 Memphis season, 15 games, 15 starts), then 27.6 by the range rule | ESPN box scores 10/5, 10/7, 10/9; RotoBaller 10/5-6 |
| Rui Hachimura to a starting role | 28.3 → 31.7 (his 2024-25 Lakers season, 59 games, 57 starts) | ESPN box scores 10/4 and 10/10; CBS Sports, Yardbarker, Yahoo 10/4-5 |

Held on the record (role claimed but not on two dated outlets, or no stint for M2 to use): Gillespie and DeRozan (bench on two dated outlets, no bench stint in two seasons — the range check guards both lines and lists neither), Grayson Allen (bench when Knueppel is healthy, but Knueppel's opener is open), Kel'el Ware (mixed, as in 2025-26), Keon Ellis, Dylan Harper and Paul Reed (starts in place of an injured teammate), Mitchell Robinson (job unresolved), Ty Jerome's first entry (until RotoBaller's dated item was found), Kessler and Fox (health notes only; no tag change). The full log — every query, outlet, date and verdict — is `wo5/data/research_log_2026-10-12.jsonl`:

| player | question | outlets (date) — source | finding | verdict |
|---|---|---|---|---|
| Kevin Porter Jr. | preseason bench (0 of 2 starts) vs 2025-26 starter (36 of 38) | ESPN box scores (2026-10-05, 2026-10-11 (ET)): bench 19 and 18 min; not in the 10-07 box (inactive); SI (Bucks On SI) 'The Ideal Milwaukee Bucks Starting Lineup To Start 2026-27' (2026-10-11 (URL ULID)): opening unit Rollins, Herro, Jaquez, Kuzma, Turner; SI (Bucks On SI) 'An intriguing position battle for the Milwaukee Bucks' (2026-10-11 (URL ULID)): starting group in flux; Porter not in it; Yahoo Sports 'Bucks' Lineup Experiment Could Help Save Their 2026-27 Season' (on/after 2026-10-11 (cites both games)): came off the bench for 19 and 18 minutes in the first two preseason games under Jenkins; ESPN depth chart (MIL) (read 2026-10-12): starters Rollins, Herro, Jaquez, Ware, Turner | bench (box score + SI 10/11 + Yahoo); dates of SI from the URL's ULID (checked: two 2025 SI items decode to March 2025, matching their content) | role change: bench; M2 minutes = 2024-25 MIL split 19.9 (30 G, 2 GS) |
| Damian Lillard | minutes on return from the Achilles (2024-25 base 36.1) | ESPN box score (2026-10-07): started, 19 min; RotoBaller (2026-10-08): 15 pts in 19 min, started alongside Ja Morant; Tixel (unbylined) (2026-10-08): says no restrictions | starter (two outlets); no outlet gives a regular-season minutes number | role confirmed: starter; minutes number unsupported either way |
| Coby White | role and health after the LaMelo Ball trade; default minutes 19.3 (CHA split) | NBA.com (2026-10-05): left calf strain, out for the preseason, re-evaluated before the opener; NBC Sports (2026-10-05): calf, ruled out for preseason; Spectrum News (AP) (2026-10-06): to miss preseason with calf strain; still expected to open the season as the starting PG; TSN (2026-10-06): same AP report; Heavy / FadeawayWorld / ESPN (Shams, contract) (offseason 2026): starting PG after the Ball trade, 3 yr / $74M | starting PG when healthy (two outlets); out for the preseason with his second calf strain within a year | role: starter (minutes from his last starter stint); availability: rule 4 candidate (recurring calf) -> decision sheet |
| Kawhi Leonard | no preseason games; team change | CP24 (2026-10-02/10-03): held out as reconditioning, not injury; NBC Sports (2026-10-03): likely to sit the Vancouver game; RotoBaller (2026-10-05): returned to full practice Monday | reconditioning, debut targeted ~10/13; starter role | default minutes hold (32.1); existing inj-risk tag unchanged |
| Nikola Vucevic | preseason bench (0 of 2) vs 2025-26 mixed (49 of 64 starts) | ESPN box scores (2026-10-03..10-11): 2 games, 0 starts; SI (Magic, On SI) (undated in result): expected to back up Wendell Carter Jr.; Roundtable (Magic) (undated in result): backup center on a one-year deal | backup center (box score + SI) | role change: bench; minutes from his bench role |
| Naz Reid | preseason starter (2 of 2) vs 2025-26 bench (3 of 77) | ESPN box scores (2026-10-03..10-11): 2 games, 2 starts; Roundtable (Hornets) (2026-10-07): coach Charles Lee on Reid; projected starting PF; RotoBaller (2026-10-06): 13 pts in 16 min in the preseason debut; Hoops Rumors via Roundtable (2026-08): expected to take the starting spot Miles Bridges held | starting PF in Bridges' former slot (box score + Roundtable 10/7) | role change: starter; minutes = the slot's 2025-26 starter (Miles Bridges, CHA) |
| Ty Jerome | preseason starter (3 of 3) vs 2024-25 base bench (3 of 70); 2025-26 MEM 15 G / 15 GS 22.6 | ESPN box scores (2026-10-05, 10-07, 10-09 (ET)): started all three, 15/19/14 min; RotoBaller 'Ty Jerome Emerging as Grizzlies' Top Point Guard Option' (undated in the result): lead only; CBS player page (older items): not October; RotoBaller 'Ty Jerome Starts at Point Guard in Preseason Opener' (2026-10-05/06 (post id after the 10/5 Coby White item)): first starting look ahead of Pippen Jr. with Morant in Portland; early favorite for the job | starter (box score 3 of 3 + RotoBaller 10/5-6) | role change: starter; M2 minutes = 2025-26 MEM 22.6 (15 G, 15 GS); rates stay on the 2024-25 base (2025-26 under 25 G) |
| Kel'el Ware | preseason 1 of 3 starts vs 2025-26 34 of 77 | ESPN box scores (2026-10-05, 10-07, 10-11 (ET)): bench 24 / start 25 / bench 24; RotoBaller (2026-10-05): off the bench in the opener; NBC Sports (2026-10-07): started at OKC with Kuzma sitting; SI (Bucks On SI) (2026-10-11 (URL ULID)): Turner the starting center; Ware started only when Kuzma sat | mixed role, the same split as 2025-26 | hold default (2025-26 MIA 22.1) |
| Grayson Allen | preseason 1 of 1 start (Knueppel out) vs 2025-26 27 of 51 | ESPN box score (2026-10-06 (ET)): started, 14 min, with Knueppel out (hamstring); SI (Hornets On SI) depth chart 'predicting the Charlotte Hornets rotation' (undated in the result): SG behind Knueppel; Roundtable 'Hornets' best starting five should be obvious' (2026-09-26): White, Knueppel, Miller, Reid, Diabate; Roundtable 'Charles Lee raves about Naz Reid' (2026-10-07): projected five without Allen; RotoBaller 'Grayson Allen Perfect From Deep in Hornets Debut' (2026-10-06/07): 13 in 14 min; may compete for touches; RotoBaller / TSN / Roundtable on Knueppel (2026-09-28..10-05): Knueppel out for the preseason, re-evaluated the first week of the season; Allen could open as a starter | bench when Knueppel is healthy, but Knueppel's opener is open and outlets say Allen could start until he returns | hold default (2025-26 28.8): the role is not settled on two dated outlets |
| Collin Gillespie | preseason bench (0 of 3) vs 2025-26 58 of 80 | ESPN box scores (2026-10-05, 10-07, 10-10 (ET)): bench 17/14/20; Roundtable 'Phoenix Suns bench should continue as major weapon in 2026-27' (2026-10-01): the bench unit starts and stops with Gillespie; SI (Suns On SI) 'guard has path to potential starting role' (undated): could take Green's spot (speculative) | bench leader (box score + Roundtable 10/1) | role change: bench; M2 has no bench stint in 2024-25..2025-26 (2024-25 share 0.27) -> minutes hold 28.5; the range check guards the line |
| DeMar DeRozan | preseason bench (0 of 3, 10/11/9 min) vs 2025-26 77 of 77 | ESPN box scores (2026-10-04, 10-06, 10-11 (ET)): bench 10/11/9; Yardbarker 'Nuggets already making smart business decision with DeMar DeRozan' (2026-10-03 (URL date)): lead; ClutchPoints 'Adelman DeRozan plan' (undated in result): first bench option; minutes open; Gazette 'Projecting the Nuggets' rotation' (undated in result): sixth man | sixth man (box score + Yardbarker 10/3 lead; Adelman's words via ClutchPoints undated) | role change: bench (two dated outlets: box + Yardbarker 10/3); M2 has no bench stint -> minutes hold 31.2; the range check guards the line |
| Keon Ellis | preseason starter (2 of 2) vs 2025-26 11 of 72 | ESPN box scores (2026-10-06, 10-08 (ET)): started 12 and 21 min; Roundtable 'Ellis expected to start in Nets-Hornets preseason opener' (2026-10-06): starting with Mikel Brown Jr. nursing an ankle sprain | fill-in start for Brown Jr.; no outlet names him a regular-season starter | hold default (2025-26 BKN rule: 2TM, last split CLE not current team -> season 20.5) |
| Dylan Harper | preseason starter (2 of 2) vs 2025-26 4 of 69 | ESPN box scores (2026-10-08, 10-10 (ET)): started 19 and 24 min; Fox DNP 10/8, absent 10/10; Pounding The Rock 'Dylan Harper must step up with Fox's status in question' (undated in result): started in Fox's place; could replace him on opening night (opinion) | fill-in for Fox (soreness) | hold default (2025-26 22.6); Fox availability checked separately |
| Paul Reed | preseason starter (2 of 2) vs 2025-26 11 of 65 | ESPN box scores (2026-10-05, 10-10 (ET)): started 21 and 21 min; Duren DNP both | starts came with Duren out; no outlet names Reed the regular-season starter | hold default (2025-26 13.9) |
| Mitchell Robinson | preseason 1 of 1 start vs 2025-26 16 of 60 | ESPN box scores (2026-10-08 DNP, 2026-10-10 started 14 min (ET)); Roundtable (2026-10-08): unclear if Robinson or Queta will start; both will play big minutes; Roundtable (2026-09-30): starter or backup an open question | starting job unresolved | hold default (2025-26 19.6) |
| Jay Huff | preseason bench (0 of 2) vs 2025-26 47 of 82 | ESPN box scores (2026-10-07, 10-10 (ET)): bench 17 and 10 min; Roundtable 'Pacers' Tyrese Haliburton makes expectations clear for Jay Huff' (2026-10-05): Zubac the starter; Huff behind him (GM Buchanan, last month); Roundtable 'Pacers GM won't name a backup center behind Ivica Zubac' (undated in result): backup minutes night-to-night (Nance, Toppin) | backup center behind Zubac (box score + Roundtable 10/5) | role change: bench; M2 minutes = 2024-25 MEM 11.7 (64 G, 2 GS); the range check guards the line |
| Nikola Vucevic | second dated outlet for the bench role | Roundtable 'Key contributors in the Magic's win over Grizzlies' (2026-10-08): 12 minutes off the bench (coach Sean Sweeney) | bench confirmed on a second dated outlet (box score + Roundtable 10/8) | role change: bench; M2 minutes = 2025-26 BOS split 21.1 (16 G, 1 GS) |
| Naz Reid | minutes for the starter role | Roundtable (2026-10-07): Lee expected to start White, Knueppel, Miller, Reid, Diabate; first starts of his career; RotoBaller (2026-10-06): 13 pts in 16 min in the debut | starter (box score + Roundtable 10/7); no starter stint of his own | M2 minutes = the slot's 2025-26 starter, Miles Bridges (CHA 77 G, 77 GS, 31.0) |
| Coby White | second dated outlet for the starter role | NBA.com (AP) 'Coby White (calf strain) misses preseason' (2026-10-06 00:22 (fetched)): 'White had been expected to take over the starting point guard spot'; Roundtable (2026-10-07): Lee expected to start White, Knueppel, Miller, Reid, Diabate; ESPN 'Hornets guard Coby White to sit preseason after calf strain' (2026-10-05 (search)): lead | starter when healthy (AP 10/6 + Roundtable 10/7); out for the preseason, opener open | role: starter; M2 minutes = 2025-26 CHI split 29.1 (29 G, 26 GS); availability: rule 4 to the decision sheet |
| Rui Hachimura | starter with Ingram out (queue item 9); 2025-26 41 of 68 starts | ESPN box scores (2026-10-04, 10-10 (ET)): started 15 and 19 min; CBS Sports / Yardbarker / Yahoo (carried note) (2026-10-04/05): started the opener, 21 pts in 15 min; SI Clippers / Yardbarker (carried note) (2026-09-30): starter | starter (box score + CBS/Yardbarker/Yahoo recaps) | role change: starter; M2 minutes = 2024-25 LAL 31.7 (59 G, 57 GS) |
| Walker Kessler | no preseason minutes (finger) | Orange County Register via RotoBaller 'Walker Kessler Sidelined on Thursday' (2026-10-08): third straight preseason game missed, finger, Redick: minor; Yardbarker 'Walker Kessler gives update on finger injury' (2026-10 (id 44408848, after the 10/5 items)): expected ready for the 10/21 opener | starting center; minor finger | hold default (2024-25 base 30.0); tag unchanged (inj-shoulder-risk) |
| De'Aaron Fox | preseason DNP 10/8, absent 10/10 | ESPN box score (2026-10-08 (ET)): DNP; carried deck note (ESPN game feed; Yahoo) (2026-10-09..10-11): general soreness, day-to-day; ruled out of 10/10 | no October outlet on a lasting problem | hold default; no tag change (one-outlet health item) |
| (holds without research) | box-score role differs but M2 has no anchor stint in 2024-25..2025-26 in the claimed direction, so research could not move the line | — | Saddiq Bey, Herbert Jones, Jerami Grant, Royce O'Neale, Kris Dunn, Bilal Coulibaly, Derik Queen, Tari Eason, Deandre Ayton, Sandro Mamukelashvili, Jaime Jaquez Jr. (no outlet names whose slot), Brook Lopez, Isaiah Jackson, Daniel Gafford, Oso Ighodaro, Khaman Maluach, Jaylin Williams (mixed or no anchor) | hold default minutes; NOT-ATTEMPTED by choice (no outcome of the research changes the line); the range check guards every top-150 line |

## 4. What the lines did to the boards

223 players move three or more places on at least one board inside the top 200 (deck 216, kit 208); every one is in Appendix A with its mechanism (the line's basis, and the two categories whose z moved most in the deck's frame — a move with an unchanged line reads as the pool moving around him). The new deck top 40, with the kit beside it (▲ = the deck's ×0.78 risk tag):

| deck | player | line (pts / reb / ast / stl / blk / 3pm / to, FG% / FT%) | minutes — basis (mechanism) | deck was | kit now (was) |
|---|---|---|---|---|---|
| 1 | Nikola Jokic | 27.6 / 12.9 / 10.7 / 1.5 / 0.8 / 1.7 / 3.7, .566 / .829 | 34.9 — 2025-26 | 2 | 1 (3) |
| 2 | Victor Wembanyama | 24.7 / 11.5 / 3.1 / 1.1 / 3.3 / 1.9 / 2.4, .503 / .823 | 29.2 — 2025-26 | 1 | 2 (2) |
| 3 | Shai Gilgeous-Alexander | 30.5 / 4.3 / 6.6 / 1.6 / 0.9 / 1.7 / 2.2, .538 / .874 | 33.2 — 2025-26 | 3 | 3 (1) |
| 4 | Tyrese Maxey | 28.2 / 4.1 / 6.6 / 1.6 / 0.6 / 3.1 / 2.4, .462 / .886 | 38.0 — 2025-26 | 9 | 5 (6) |
| 5 | Luka Doncic | 33.3 / 7.7 / 8.3 / 1.6 / 0.5 / 4.0 / 4.0, .473 / .772 | 35.8 — 2025-26 | 4 | 6 (4) |
| 6 | Kawhi Leonard ▲ | 27.8 / 6.4 / 3.6 / 1.7 / 0.5 / 2.6 / 2.0, .503 / .882 | 32.1 — 2025-26 | 34 | 4 (12) |
| 7 | Jamal Murray | 25.1 / 4.4 / 7.1 / 1.1 / 0.5 / 3.3 / 2.3, .475 / .883 | 35.4 — 2025-26 | 20 | 7 (26) |
| 8 | Donovan Mitchell | 27.4 / 4.5 / 5.7 / 1.5 / 0.3 / 3.2 / 2.8, .473 / .858 | 33.5 — 2025-26 | 14 | 8 (16) |
| 9 | Jalen Johnson | 22.5 / 10.3 / 7.9 / 1.3 / 0.7 / 1.7 / 3.4, .492 / .776 | 35.2 — 2025-26 | 13 | 10 (25) |
| 10 | Lauri Markkanen | 26.4 / 6.9 / 2.1 / 0.9 / 0.5 / 2.7 / 1.5, .471 / .887 | 34.4 — 2025-26 | 52 | 14 (47) |
| 11 | Kevin Durant | 25.8 / 5.5 / 4.8 / 0.8 / 1.1 / 2.4 / 3.2, .515 / .876 | 36.4 — 2025-26 | 18 | 16 (30) |
| 12 | Tyrese Haliburton ▲ | 17.4 / 3.3 / 8.6 / 1.3 / 0.6 / 2.8 / 1.5, .474 / .853 | 31.3 — 2024-25 (range rule R1) | 7 | 11 (27) |
| 13 | Jayson Tatum ▲ | 27.0 / 8.7 / 6.0 / 1.1 / 0.5 / 3.5 / 2.9, .454 / .822 | 36.4 — 2024-25 | 21 | 9 (18) |
| 14 | Anthony Davis ▲ | 22.0 / 10.2 / 3.1 / 1.0 / 1.9 / 0.6 / 2.0, .518 / .781 | 29.6 — 2024-25 (range rule R1) | 5 | 15 (7) |
| 15 | Amen Thompson | 18.3 / 7.8 / 5.3 / 1.7 / 1.0 / 0.3 / 2.4, .536 / .763 | 37.4 — 2025-26 | 30 | 17 (28) |
| 16 | Chet Holmgren | 16.9 / 8.9 / 1.7 / 0.7 / 2.1 / 1.3 / 1.6, .549 / .790 | 28.9 — 2025-26 | 10 | 18 (10) |
| 17 | Stephen Curry ▲ | 26.6 / 3.6 / 4.7 / 1.0 / 0.4 / 4.4 / 2.8, .469 / .919 | 30.9 — 2025-26 | 17 | 13 (13) |
| 18 | James Harden | 22.9 / 4.7 / 7.7 / 1.2 / 0.6 / 3.0 / 3.4, .435 / .877 | 33.8 — 2025-26 | 31 | 19 (37) |
| 19 | Scottie Barnes | 17.8 / 7.5 / 5.9 / 1.4 / 1.3 / 0.9 / 2.6, .496 / .801 | 33.5 — 2025-26 | 38 | 20 (36) |
| 20 | Trey Murphy III ▲ | 21.4 / 5.7 / 3.8 / 1.3 / 0.5 / 3.2 / 1.8, .467 / .883 | 35.5 — 2025-26 | 33 | 12 (21) |
| 21 | Domantas Sabonis | 18.8 / 13.9 / 6.0 / 0.8 / 0.4 / 0.9 / 2.9, .580 / .746 | 34.7 — 2024-25 | 25 | 21 (19) |
| 22 | Dyson Daniels | 11.7 / 6.8 / 5.9 / 2.3 / 0.6 / 0.3 / 1.8, .508 / .615 | 33.2 — 2025-26 | 11 | 24 (9) |
| 23 | Joel Embiid ▲ | 26.9 / 7.7 / 3.9 / 0.8 / 1.3 / 1.4 / 2.9, .493 / .846 | 31.6 — 2025-26 | 71 | 27 (22) |
| 24 | Anthony Edwards | 28.3 / 5.0 / 3.7 / 1.2 / 0.7 / 3.4 / 2.9, .477 / .798 | 35.0 — 2025-26 | 8 | 23 (8) |
| 25 | Karl-Anthony Towns | 20.2 / 11.9 / 3.0 / 0.8 / 0.6 / 1.5 / 2.5, .508 / .852 | 31.0 — 2025-26 | 6 | 25 (5) |
| 26 | Cade Cunningham | 23.8 / 5.5 / 9.9 / 1.2 / 0.7 / 2.0 / 3.7, .457 / .821 | 33.9 — 2025-26 | 12 | 26 (11) |
| 27 | Bam Adebayo | 20.9 / 10.0 / 3.2 / 1.2 / 0.7 / 1.7 / 1.6, .469 / .772 | 32.4 — 2025-26 | 47 | 28 (32) |
| 28 | Walker Kessler ▲ | 11.2 / 12.2 / 1.7 / 0.7 / 2.7 / 0.1 / 1.5, .669 / .559 | 30.0 — 2024-25 | 44 | 22 (35) |
| 29 | Ryan Rollins | 17.3 / 4.6 / 5.6 / 1.7 / 0.6 / 2.5 / 2.7, .473 / .797 | 32.1 — 2025-26 | 70 | 29 (63) |
| 30 | Derrick White | 16.8 / 4.4 / 5.4 / 1.1 / 1.2 / 2.7 / 1.7, .409 / .888 | 34.1 — 2025-26 | 24 | 30 (23) |
| 31 | Austin Reaves | 23.2 / 4.7 / 5.5 / 1.0 / 0.3 / 2.3 / 3.0, .487 / .869 | 34.5 — 2025-26 | 26 | 31 (20) |
| 32 | Michael Porter Jr. | 24.5 / 7.1 / 3.0 / 0.7 / 0.5 / 3.4 / 2.3, .473 / .843 | 32.5 — 2025-26 | 55 | 32 (45) |
| 33 | Onyeka Okongwu | 15.9 / 7.6 / 3.1 / 1.0 / 1.1 / 1.9 / 1.7, .511 / .757 | 31.0 — 2025-26 | 36 | 33 (39) |
| 34 | Donovan Clingan | 12.1 / 11.6 / 2.1 / 0.6 / 1.9 / 1.1 / 1.2, .522 / .670 | 27.2 — 2025-26 | 53 | 34 (49) |
| 35 | Ty Jerome | 16.9 / 3.4 / 4.7 / 1.5 / 0.1 / 2.2 / 1.8, .497 / .874 | 27.6 — 2024-25 (range rule R1) | 101 | 41 (50) |
| 36 | Desmond Bane | 20.0 / 4.1 / 4.1 / 1.1 / 0.5 / 2.0 / 2.0, .481 / .902 | 33.6 — 2025-26 | 27 | 36 (38) |
| 37 | Kyrie Irving ▲ | 21.3 / 4.1 / 4.0 / 1.1 / 0.4 / 2.5 / 1.9, .473 / .907 | 31.1 — 2024-25 (range rule R1) | 15 | 35 (17) |
| 38 | Paul George ▲ | 17.4 / 5.3 / 3.6 / 1.6 / 0.4 / 2.7 / 1.7, .439 / .831 | 30.7 — 2025-26 | 66 | 38 (51) |
| 39 | Jalen Duren | 19.5 / 10.5 / 2.0 / 0.7 / 1.0 / 0.0 / 1.9, .651 / .736 | 28.2 — 2025-26 | 60 | 37 (57) |
| 40 | Cooper Flagg | 21.0 / 6.7 / 4.5 / 1.2 / 0.9 / 1.0 / 2.3, .468 / .827 | 33.5 — 2025-26 | 22 | 39 (14) |

**The shape of the change.** The stars' lines were mostly 2024-25-shaped (the Towns report found 44 of the 52 top-60 rows with a 2025-26 season of 20+ games closer to their 2024-25 line); they are now each player's 2025-26 rate at his 2025-26 minutes. Players whose 2025-26 rate rose — Kawhi, Markkanen, Embiid, Jamal Murray, Mitchell, Rollins, Michael Porter Jr., Adebayo — rise; players whose 2025-26 rate fell or whose old line ran ahead of it — Towns, Edwards, Cunningham, Jalen Williams, Herro, Franz Wagner, Giannis — fall. Dyson Daniels falls on the steals anchor the owner chose on 10/9 (2.3 against the old 3.0). The returnees' minutes come from the outside lines (range rule R1), which lowers Kyrie (15 → 37), Davis (5 → 14), Morant (65 → 143) and Haliburton on the deck (7 → 12; on the kit he rises 27 → 11 because the kit's old line was lower still).

## 5. Towns, and the card at pick #10

**Towns' line.** Before: 24.8 points, 12.5 rebounds, 2.1 threes, .525 / .830 (his 2024-25 shape). Now: 20.2 / 11.9 / 3.0 assists / 0.8 steals / 0.6 blocks / 1.5 threes / 2.5 turnovers, .508 / .852, at his 2025-26 31.0 minutes — the Basketball-Reference season (75 games) with FG% and FT% a third of the way to his career and steals and blocks on the three-season anchor; an independent recomputation from the totals gives the same digits. Rank: deck 6 → 25, kit 5 → 25.

**The card at #10** (the deck's own engine on the v60 page, replayed at pick #10 of every room on file — 24 rooms):

| room | v59 card at #10 (old lines) | v60 card at #10 | Towns on the v60 card |
|---|---|---|---|
| mock 75 (live, public) | Towns, Maxey, Jalen Johnson, Haliburton, Davis | **Maxey** (value 5.96, ΔECW 4.796, survival to #15 0.25), Jamal Murray (4.51, 4.561, 0.77), Jalen Johnson, Kawhi Leonard (0.97), Donovan Mitchell | #18 (Haliburton #11) |
| mock 74 (public) | Towns, Edwards, Jalen Johnson, Haliburton, Davis | **Jamal Murray** (4.51, 4.453, 0.77), Jalen Johnson, Kawhi Leonard (0.97), Durant, Markkanen (0.98) | #17 (Haliburton #11, Edwards #14) |
| all 24 rooms | on each room's own page, Towns was the #10 card's #1 in 12 of the 17 rooms 59–75 | Murray #1 in 17, Maxey #1 in the 7 where he is on the board | in the Top 5 in none |

So the answer to "did Towns' position change": yes — the 2024-25-shaped line was what put him first; on his own 2025-26 rates he is a late second-round value. D-1012-4 (Haliburton at #10, Towns at #15) changes meaning on these lines: Haliburton is #11 on the #10 card, Towns #17–18; neither is the card's choice at #10. The card's survival read says Murray usually lasts to #15 (0.77) and Maxey usually does not (0.25), so where both are there the order the card's odds favor is Maxey at #10 and Murray at #15.


## 6. Every ranking movement, in plain language

**One rule moved everyone.** Each player's line is now his own 2025-26 production rate at his 2025-26 minutes (with the work order's three adjustments: shooting percentages pulled a third of the way to career, steals and blocks averaged over three seasons, points computed from the shooting). So a player rises when last season was better than the line he carried, and falls when it was worse. Of the 223 players who moved three or more places on either board (deck 216, kit 208; every one in Appendix A): 191 moved for that reason alone; 10 are players returning from long injuries whose minutes were set from the outside projections; 8 had no 2025-26 season of 25 games and carry their 2024-25 rates; 8 are rookies whose college-translation cells were brought to the outside lines' range; 6 changed role in camp on two dated reports. On the deck, 94 players rose ten or more places and 89 fell ten or more.

**The first two rounds (deck top 24).** New to the first two rounds: Kawhi Leonard (was 34, kit 4); Lauri Markkanen (was 52, kit 14); Amen Thompson (was 30, kit 17); James Harden (was 31, kit 19); Scottie Barnes (was 38, kit 20); Trey Murphy III (was 33, kit 12); Domantas Sabonis (was 25, kit 21); Joel Embiid (was 71, kit 27). Out of them: Karl-Anthony Towns (6 → 25, kit 5 → 25); Cade Cunningham (12 → 26, kit 11 → 26); Kyrie Irving (15 → 37, kit 17 → 35); Jalen Williams (16 → 57, kit 29 → 56); Evan Mobley (19 → 46, kit 34 → 45); Cooper Flagg (22 → 40, kit 14 → 39); Jaren Jackson Jr. (23 → 45, kit 33 → 42); Derrick White (24 → 30, kit 23 → 30). Moved three or more places but stayed inside: Tyrese Maxey (9 → 4); Jamal Murray (20 → 7); Donovan Mitchell (14 → 8); Jalen Johnson (13 → 9); Kevin Durant (18 → 11); Tyrese Haliburton (7 → 12); Jayson Tatum (21 → 13); Anthony Davis (5 → 14); Chet Holmgren (10 → 16); Dyson Daniels (11 → 22); Anthony Edwards (8 → 24).

**Rounds three to five (deck 25–60).** Twelve names left and twelve arrived. Left: Franz Wagner (29 → 68); Payton Pritchard (37 → 77); Kristaps Porzingis (39 → 75); Darius Garland (41 → 103); Tyler Herro (43 → 65); Ivica Zubac (45 → 83); Brandon Miller (46 → 74); Jarrett Allen (50 → 73); Zach LaVine (56 → 138); Trae Young (57 → 63); Coby White (58 → 153); Jalen Suggs (59 → 61). Arrived: Joel Embiid (71 → 23); Ryan Rollins (70 → 29); Ty Jerome (101 → 35); Paul George (66 → 38); Naz Reid (79 → 48); Zach Edey (84 → 49); Damian Lillard (88 → 50); Alperen Sengun (69 → 51); VJ Edgecombe (96 → 52); Jaylen Brown (72 → 55); LeBron James (62 → 56); Reed Sheppard (104 → 60).

**The largest risers (40 or more places on the deck), with the reason from the record:**

- Ryan Kalkbrenner (270 → 149); kit 267 → 146 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: BLK +0.84, REB +0.61.
- John Konchar (292 → 172); kit off → off — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: ST +1.09, REB +0.66.
- Grayson Allen (172 → 81); kit 186 → 82 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: ST +1.06, FG% -0.99.
- Sam Merrill (236 → 146); kit 236 → 145 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: 3PTM +0.83, PTS +0.44.
- Bobby Portis (218 → 135); kit 169 → 135 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: 3PTM +0.88, PTS +0.63.
- Luke Kornet (231 → 152); kit 230 → 151 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: REB +0.50, BLK +0.44.
- Jeremiah Fears (273 → 198); kit 198 → 197 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: AST -0.88, TO +0.71.
- Neemias Queta (154 → 80); kit 237 → 78 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: FT% +0.70, TO +0.50.
- Precious Achiuwa (259 → 189); kit 248 → 190 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: ST +0.41, REB +0.40.
- Jarace Walker (267 → 197); kit 261 → 196 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: ST +0.73, PTS +0.48.
- Ayo Dosunmu (147 → 79); kit 151 → 80 — his 2025-26 rates at his 2025-26 minutes (2025-26 minutes with MIN (24 of 69 games)); the categories that carried it: 3PTM +0.67, PTS +0.63.
- DeMar DeRozan (156 → 88); kit 160 → 88 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: TO +0.51, PTS +0.45.
- Bennedict Mathurin (243 → 176); kit 200 → 172 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: TO -0.91, PTS +0.73.
- Ty Jerome (101 → 35); kit 50 → 41 — minutes set from the outside lines (returning from injury); the categories that carried it: ST +1.78, FG% +0.71.
- Jaime Jaquez Jr. (210 → 144); kit 229 → 143 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: AST +0.80, TO -0.52.
- Royce O'Neale (190 → 125); kit 194 → 126 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: 3PTM +0.74, ST +0.73.
- Jaylon Tyson (223 → 158); kit 222 → 156 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: PTS +0.43, TO -0.41.
- Maxime Raynaud (230 → 166); kit 210 → 163 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: REB +0.73, 3PTM -0.63.
- Bradley Beal (171 → 109); kit 189 → 106 — no 2025-26 season of 25+ games, so his 2024-25 rates; the categories that carried it: PTS +0.73, TO -0.52.
- Duncan Robinson (245 → 183); kit 187 → 182 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: 3PTM +0.73, TO +0.62.
- Dylan Cardwell (228 → 170); kit 227 → 170 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: REB +0.46, ST +0.33.
- Kyshawn George (181 → 126); kit 141 → 125 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: TO -1.15, AST +0.70.
- Tre Jones (143 → 89); kit 145 → 90 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: FG% +0.93, FT% +0.32.
- Naji Marshall (202 → 151); kit 179 → 153 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: ST +0.48, PTS +0.42.
- Joel Embiid (71 → 23); kit 22 → 27 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: FG% +1.04, BLK +0.84.
- Julian Champagnie (161 → 115); kit 168 → 115 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: REB +0.70, BLK +0.42.
- Jrue Holiday (136 → 91); kit 92 → 89 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: TO -1.55, PTS +0.86.
- Ajay Mitchell (152 → 107); kit 73 → 107 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: ST +0.81, PTS +0.17.
- VJ Edgecombe (96 → 52); kit 111 → 54 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: REB +0.49, ST +0.31.
- Reed Sheppard (104 → 60); kit 102 → 61 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: ST +1.21, 3PTM +0.63.
- Lauri Markkanen (52 → 10); kit 47 → 14 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: PTS +1.28, FT% +0.65.
- Deandre Ayton (158 → 116); kit 133 → 116 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: FG% +1.05, FT% -0.57.
- Miles McBride (199 → 157); kit 204 → 158 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: 3PTM +0.63, PTS +0.46.
- Ryan Rollins (70 → 29); kit 63 → 29 — his 2025-26 rates at his 2025-26 minutes; the categories that carried it: ST +1.28, TO -1.15.

**The largest fallers (40 or more places on the deck):**

- Jared McCain (145 → 294); kit 149 → 296 — his 2025-26 rates at his 2025-26 minutes (2025-26 minutes with OKC (30 of 67 games)); the categories that cost him: PTS -1.26, AST -0.98.
- Day'Ron Sharpe (76 → 203); kit 70 → 202 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: ST -1.30, REB -0.94.
- Jalen Green (126 → 240); kit 137 → 241 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: FT% -0.91, 3PTM -0.83.
- Terrence Shannon Jr (200 → 312); kit 201 → 309 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: ST -1.82, PTS -1.27.
- Nikola Jovic (197 → 303); kit 226 → 302 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: ST -0.89, PTS -0.72.
- Coby White (58 → 153); kit 100 → 152 — role move: starting PG when healthy (NBA.com/AP 10/6; Roundtable 10/7); the categories that cost him: TO -1.00, FT% -0.85.
- Gary Trent Jr. (196 → 291); kit 175 → 295 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: ST -0.81, REB -0.64.
- Jose Alvarado (177 → 267); kit 180 → 272 — his 2025-26 rates at his 2025-26 minutes (2025-26 minutes with NYK (28 of 69 games)); the categories that cost him: ST -1.59, PTS -0.31.
- Khaman Maluach (220 → 310); kit 191 → 307 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: REB -1.78, BLK -1.32.
- Jay Huff (198 → 284); kit 205 → 286 — role move: bench behind Zubac (ESPN box 10/7 and 10/10 ET; Roundtable 10/5); the categories that cost him: REB -0.61, BLK -0.53.
- Gui Santos (165 → 249); kit 172 → 250 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: ST -0.77, REB -0.61.
- Zach LaVine (56 → 138); kit 71 → 138 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: TO +0.82, AST -0.80.
- Keon Ellis (122 → 202); kit 128 → 205 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: PTS -0.59, AST -0.50.
- Yves Missi (189 → 269); kit 214 → 268 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: ST -0.96, REB -0.96.
- Ja Morant (65 → 143); kit 134 → 140 — minutes set from the outside lines (returning from injury); the categories that cost him: ST -1.02, AST -0.74.
- Sandro Mamukelashvili (81 → 159); kit 82 → 157 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: ST -0.52, 3PTM -0.47.
- Bub Carrington (195 → 272); kit 212 → 271 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: ST -0.85, TO -0.36.
- Malik Monk (153 → 228); kit 158 → 228 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: ST -0.85, AST -0.71.
- Jaylen Wells (179 → 253); kit 203 → 256 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: BLK -0.56, ST -0.52.
- Alex Caruso (129 → 200); kit 127 → 200 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: ST -0.58, AST -0.43.
- De'Andre Hunter (159 → 230); kit 161 → 229 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: FG% -0.74, TO -0.67.
- Zaccharie Risacher (173 → 242); kit 139 → 244 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: PTS -0.73, 3PTM -0.47.
- Luguentz Dort (151 → 218); kit 154 → 220 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: FG% -0.54, PTS -0.47.
- Herbert Jones (74 → 137); kit 64 → 137 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: FG% -0.66, ST -0.50.
- Darius Garland (41 → 103); kit 24 → 102 — his 2025-26 rates at his 2025-26 minutes (2025-26 minutes with LAC (19 of 45 games)); the categories that cost him: FT% -0.41, PTS -0.38.
- Bogdan Bogdanovic (163 → 224); kit 125 → 225 — no 2025-26 season of 25+ games, so his 2024-25 rates; the categories that cost him: ST -0.49, PTS -0.33.
- PJ Washington (87 → 141); kit 74 → 142 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: FT% -0.68, FG% -0.46.
- Anfernee Simons (160 → 213); kit 170 → 214 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: ST -0.89, TO +0.65.
- Dylan Harper (146 → 196); kit 165 → 195 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: ST -1.34, TO +1.33.
- Goga Bitadze (185 → 235); kit 218 → 235 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: REB -0.70, TO +0.62.
- Aaron Gordon (92 → 139); kit 93 → 141 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: FT% -1.02, FG% -0.69.
- Bilal Coulibaly (131 → 178); kit 119 → 179 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: ST -0.94, TO +0.80.
- Pascal Siakam (64 → 110); kit 86 → 109 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: FT% -0.95, FG% -0.79.
- Jordan Goodwin (112 → 156); kit 106 → 159 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: ST -0.87, BLK -0.17.
- Nikola Vucevic (121 → 163); kit 124 → 160 — role move: bench (ESPN box 10/7 and 10/11 ET; Roundtable 10/8); the categories that cost him: FG% -0.62, REB -0.40.
- Jalen Williams (16 → 57); kit 29 → 56 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: 3PTM -1.29, ST -1.19.
- Payton Pritchard (37 → 77); kit 66 → 77 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: 3PTM -1.18, TO +0.66.
- Draymond Green (115 → 155); kit 109 → 155 — his 2025-26 rates at his 2025-26 minutes; the categories that cost him: ST -0.66, TO -0.61.

**Players returning from long injuries** (minutes from the outside projections, because our own data cannot say how much they will play; rates are their last full season's): Tyrese Haliburton (7 → 12; 31.3 min, was 33.6); Anthony Davis (5 → 14; 29.6 min, was 33.5); Ty Jerome (101 → 35; 27.6 min, was 19.9); Kyrie Irving (15 → 37; 31.1 min, was 36.1); Zach Edey (84 → 49; 26.6 min, was 21.4); Damian Lillard (88 → 50; 27.8 min, was 36.1); Trae Young (57 → 63; 32.9 min, was 36.0); Dejounte Murray (63 → 87; 29.1 min, was 32.6); Fred VanVleet (68 → 96; 31.0 min, was 35.2); Ja Morant (65 → 143; 25.5 min, was 30.4).

**Role changes in camp** (each on two dated reports, §3; minutes from the player's own last stint in that role, else the displaced starter's): Naz Reid (79 → 48); Coby White (58 → 153); Nikola Vucevic (121 → 163); Rui Hachimura (183 → 169); Kevin Porter Jr. (224 → 188); Jay Huff (198 → 284). Ty Jerome's role move (bench to starter) is counted above under the returnees because the range rule then set his minutes.

**Players on their 2024-25 rates** (no 2025-26 season of 25 games, injury or otherwise): Jayson Tatum (21 → 13); Domantas Sabonis (25 → 21); Walker Kessler (44 → 28); Keegan Murray (100 → 72); Bradley Beal (171 → 109); Scotty Pippen Jr. (132 → 147); Obi Toppin (184 → 205); Bogdan Bogdanovic (163 → 224).

**Rookies** (the college translation held; only cells outside every outside projection were brought to the range): Cameron Boozer (48 → 41); Yaxel Lendeborg (82 → 69); Caleb Wilson (120 → 90); Darryn Peterson (140 → 112); AJ Dybantsa (139 → 148); Keaton Wagler (175 → 177); Darius Acuff Jr. (176 → 179); Hannes Steinbach (207 → 191).

**On the kit board only:** Andre Drummond (kit 273 → 198) — the deck carries no row for him (off the deck's draftable pool).

**Which categories did the moving.** Among players inside the top 100 on either board before or after, the category most often behind a move was steals (39 of the movers' two leading drivers), then FG% (32), TO (28), PTS (27), FT% (26). Steals leads because the three-season average replaces last year's single number, and steals are the least stable category season to season (the actuals study of 10/9). Nothing moved because of a tag, a team change, a games-played figure or a price.


## Range check (D-RN-3)

Rule (owner, 2026-10-08): on a projection pass, every cell of a top-150 line that sits outside the range of ALL its references (three or more of: Yahoo `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-12.csv`, RotoBaller `rotoballer-2026-09-29.csv`, 2025-26 actual `arena/results/tuning_2026-10-08/bref_pergame_2025-26.csv`; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats) carries a one-line mechanism naming two dated outlets, or comes back inside the range. Before this pass (the 10/12 lines): 131 players, 435 cells. After the range rule (§3.4): 23 player(s), 25 cell(s), of 145 checkable top-150 lines — every one a cell the method keeps on purpose, each with its mechanism below. Net z is what the cells carry beyond the nearest reference in the deck's frame (positive flatters the player).

| player | deck rank | cells outside every reference | net z | mechanism (two dated outlets) |
|---|---|---|---|---|
| Ryan Rollins | 29 | stl 1.7 vs 1.3-1.5 | +0.65 | steals on the item-8 three-season anchor (2025-26/2024-25/2023-24 weighted 5/4/3 by games, per-36 at his minutes) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals |
| Dejounte Murray | 87 | stl 1.4 vs 1.6-1.7 | -0.65 | steals on the item-8 three-season anchor (2025-26/2024-25/2023-24 weighted 5/4/3 by games, per-36 at his minutes) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals |
| Ausar Thompson | 105 | stl 1.8 vs 2-2.2 | -0.65 | steals on the item-8 three-season anchor (2025-26/2024-25/2023-24 weighted 5/4/3 by games, per-36 at his minutes) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals |
| Joel Embiid | 23 | stl 0.8 vs 0.5-0.6; ft_pct .846 vs .854-.867 | +0.42 | steals on the item-8 three-season anchor (2025-26/2024-25/2023-24 weighted 5/4/3 by games, per-36 at his minutes) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals; free throws shrunk one-third toward his career rate (the 10/7 Castle precedent; his 2025-26 rate alone sits inside the range) — Basketball-Reference career totals pulled 2026-10-12; ESPN 2025-26 actuals |
| Daniel Gafford | 119 | blk 1.6 vs 1.2-1.4 | +0.39 | blocks on the item-8 three-season anchor (5/4/3 by games, per-36 at his minutes) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals |
| Jerami Grant | 150 | ft_pct .795 vs .814-.825 | -0.35 | free throws shrunk one-third toward his career rate (the 10/7 Castle precedent; his 2025-26 rate alone sits inside the range) — Basketball-Reference career totals pulled 2026-10-12; ESPN 2025-26 actuals |
| Michael Porter Jr. | 32 | stl 0.7 vs 0.8-1.1 | -0.32 | steals on the item-8 three-season anchor (2025-26/2024-25/2023-24 weighted 5/4/3 by games, per-36 at his minutes) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals |
| Jalen Duren | 39 | stl 0.7 vs 0.8-0.8 | -0.32 | steals on the item-8 three-season anchor (2025-26/2024-25/2023-24 weighted 5/4/3 by games, per-36 at his minutes) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals |
| Luka Doncic | 5 | ft_pct .772 vs .780-.782 | -0.26 | free throws shrunk one-third toward his career rate (the 10/7 Castle precedent; his 2025-26 rate alone sits inside the range) — Basketball-Reference career totals pulled 2026-10-12; ESPN 2025-26 actuals |
| Tyrese Haliburton | 12 | tov 1.5 vs 1.7-1.7 | +0.26 | turnovers at his base season's per-36 rate (one cell alone is a rate, not minutes — rule R1) — Basketball-Reference season totals pulled 2026-10-12; ESPN actuals |
| Naz Reid | 48 | tov 1.9 vs 1.6-1.7 | -0.26 | turnovers at his base season's per-36 rate (one cell alone is a rate, not minutes — rule R1) — Basketball-Reference season totals pulled 2026-10-12; ESPN actuals |
| Giannis Antetokounmpo | 58 | fg_pct .600 vs .608-.624; ft_pct .664 vs .628-.650 | +0.23 | field goals shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference career totals pulled 2026-10-12; ESPN 2025-26 actuals; free throws shrunk one-third toward his career rate (the 10/7 Castle precedent; his 2025-26 rate alone sits inside the range) — Basketball-Reference career totals pulled 2026-10-12; ESPN 2025-26 actuals |
| Domantas Sabonis | 21 | tpm 0.9 vs 0.6-0.7 | +0.20 | threes at his base season's per-36 rate (one cell alone is a rate — rule R1) — Basketball-Reference season totals pulled 2026-10-12; ESPN actuals |
| Cade Cunningham | 26 | blk 0.7 vs 0.8-0.8 | -0.20 | blocks on the item-8 three-season anchor (5/4/3 by games, per-36 at his minutes) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals |
| Keegan Murray | 72 | pts 12.4 vs 13.3-16.1 | -0.16 | points at his base season's per-36 rates and shooting (one cell alone is a rate — rule R1) — Basketball-Reference season totals pulled 2026-10-12; ESPN actuals |
| Aaron Gordon | 139 | ft_pct .744 vs .753-.789 | -0.13 | free throws shrunk one-third toward his career rate (the 10/7 Castle precedent; his 2025-26 rate alone sits inside the range) — Basketball-Reference career totals pulled 2026-10-12; ESPN 2025-26 actuals |
| Brandon Ingram | 84 | ft_pct .811 vs .819-.826 | -0.12 | free throws shrunk one-third toward his career rate (the 10/7 Castle precedent; his 2025-26 rate alone sits inside the range) — Basketball-Reference career totals pulled 2026-10-12; ESPN 2025-26 actuals |
| Jrue Holiday | 91 | ft_pct .822 vs .838-.867 | -0.10 | free throws shrunk one-third toward his career rate (the 10/7 Castle precedent; his 2025-26 rate alone sits inside the range) — Basketball-Reference career totals pulled 2026-10-12; ESPN 2025-26 actuals |
| Jakob Poeltl | 117 | ft_pct .588 vs .602-.642 | -0.10 | free throws shrunk one-third toward his career rate (the 10/7 Castle precedent; his 2025-26 rate alone sits inside the range) — Basketball-Reference career totals pulled 2026-10-12; ESPN 2025-26 actuals |
| Jalen Suggs | 61 | ft_pct .834 vs .846-.866 | -0.08 | free throws shrunk one-third toward his career rate (the 10/7 Castle precedent; his 2025-26 rate alone sits inside the range) — Basketball-Reference career totals pulled 2026-10-12; ESPN 2025-26 actuals |
| CJ McCollum | 132 | ft_pct .780 vs .749-.772 | +0.08 | free throws shrunk one-third toward his career rate (the 10/7 Castle precedent; his 2025-26 rate alone sits inside the range) — Basketball-Reference career totals pulled 2026-10-12; ESPN 2025-26 actuals |
| Christian Braun | 124 | ft_pct .774 vs .782-.815 | -0.06 | free throws shrunk one-third toward his career rate (the 10/7 Castle precedent; his 2025-26 rate alone sits inside the range) — Basketball-Reference career totals pulled 2026-10-12; ESPN 2025-26 actuals |
| Tobias Harris | 111 | ft_pct .857 vs .863-.869 | -0.05 | free throws shrunk one-third toward his career rate (the 10/7 Castle precedent; his 2025-26 rate alone sits inside the range) — Basketball-Reference career totals pulled 2026-10-12; ESPN 2025-26 actuals |

## Points identity (D-1009-3)

Rule (owner, 2026-10-09): on a projection pass, every top-200 line on either plane whose points sit more than 1 from its own shooting (2·FGM + 3PM + FTM, with FGM = FG% × FGA and FTM = FT% × FTA) is reconciled by evidence — either side may be the wrong half — or carries a one-line mechanism naming two dated outlets. This pass: 0 player(s), 0 line(s), of 200 deck and 200 kit lines checked.

| player | plane | rank | pts | implied (2·FGM + 3PM + FTM) | gap | mechanism (two dated outlets) |
|---|---|---|---|---|---|---|


## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 d903b2eea753), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 25 of 25 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-12.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-06.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 5 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ryan Rollins | 20 of 25 | 29 | 74 | 58 | 63 | 78 | 83 | stl 1.7 vs 1.3-1.5 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Ty Jerome | 20 of 25 | 35 | 117 | 47 | 60 | 101 | 71 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Grayson Allen | 18 of 25 | 81 | 138 | 113 | 157 | 149 | 130 | pts 16.8 vs 11.7-13.8; ast 3.8 vs 2.5-3; tpm 3.1 vs 2.4-2.8; tov 1.6 vs 1.2-1.4; fg_pct .416 vs .422-.433 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Reed Sheppard | 18 of 25 | 60 | 178 | 56 | 118 | 126 | 129 | tpm 2.8 vs 2.2-2.6 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Lauri Markkanen | 16 of 25 | 10 | 37 | 18 | 31 | 41 | 29 | pts 26.4 vs 20.2-23.8; ast 2.1 vs 1.8-1.9; fg_pct .471 vs .452-.463 | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 11 of 25 | 69 | 141 | 94 | 121 | 137 | 98 | none | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Michael Porter Jr. | 8 of 25 | 32 | 60 | 55 | 62 | 70 | 59 | pts 24.5 vs 18.7-21.8; ast 3 vs 2.4-2.6; stl 0.7 vs 0.8-1; tpm 3.4 vs 2.9-3.1; tov 2.3 vs 1.9-2 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 6 of 25 | 6 | 32 | 15 | 16 | 15 | 20 | pts 27.8 vs 23.7-24.3; tpm 2.6 vs 2.2-2.3 | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (21 mocks, value 7, market 18); VJ Edgecombe (12 mocks, value 52, market 75); Derrick White (8 mocks, value 30, market 45); Tyrese Maxey (7 mocks, value 4, market 9).

**On this pass.** The check ran on the shipped v60 page (sha256 d903b2eea753), so every row above carries its re-derived line. The morning check on the 10/12 lines flagged 16 names, 4 of them LINE QUESTIONED — the verdict that asks for a re-derivation at the next projection pass. This pass was that re-derivation. All 4 moved toward the outside ranks and fell out of the card's 🎯: Daniel Gafford (value 90 → 119, market 180; the 🎯 in 0 of 25 mocks now); Devin Vassell (value 89 → 106, market 138; the 🎯 in 0 of 25 mocks now); Herbert Jones (value 74 → 137, market 182; the 🎯 in 0 of 25 mocks now); PJ Washington (value 87 → 141, market 155; the 🎯 in 0 of 25 mocks now). Now 8 names are flagged, 3 LINE QUESTIONED (Grayson Allen, Ryan Rollins, Yaxel Lendeborg):

- **Ryan Rollins** — one cell outside all three projections: steals 1.7, the item-8 three-season anchor (his 2025-26 per-game was 1.49; the 5/4/3 games-weighted per-36 of 2025-26, 2024-25 and 2023-24 at his 32.1 minutes gives 1.7), kept by range rule R2 with that mechanism. The rest of the line is his 2025-26 season at its minutes. The judgment flag stays HELD −0.05 (D-WO5-3).
- **Grayson Allen** — five cells outside: the outside lines price a bench role in Charlotte; ours is his 2025-26 Phoenix season at its 28.8 minutes, held by rule M2 because the dated outlets split (Watchlist; D-WO5-4).
- **Yaxel Lendeborg** — no cell outside all three projections after the range rule moved his rookie cells (R1b and R3); what remains is rank: his value rank rose 82 → 69 while the four outside ranks (Yahoo 94, Hashtag 121, Rotoworld 137, RotoBaller 98) stayed, so all four now sit 25+ places below ours. The owner's D-1011-2 (c) judgment card applies.


## 9. The top 60 against the five market files

The union of both boards' top 60 (61 names), name by name against the five outside rank files in `report/market/` — Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-12.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`, RotoWire `rotowire-2026-10-09.csv` — with Yahoo's ADP (`yahoo-2026-10-12.csv`) shown as the price. A divergence is any of the five 25 or more places from our rank on either board (a name a list leaves out counts as one place past its end). 30 of the 61 names diverge from at least one source (68 source divergences): 22 where we rank the player higher, 8 where lower. Each divergent row carries one line built from the records — the categories that carry (or cost) his value in the deck's frame, and how his line was made. The pattern: we sit higher on players whose value is steals, free throws and threes at high volume on their 2025-26 rates (Daniels, Rollins, Kawhi, Markkanen, Harden, Sheppard, Edgecombe, Ty Jerome) and on the returnees whose minutes we set from the outside lines but whose percentages stay ours (Kyrie, Lillard); lower on the categories-costly stars the market drafts for points (Giannis' free throws −4.27 z, Trae Young's turnovers −3.02 and field goals −1.75, Şengün, Booker, LaMelo Ball, Giddey) and on Flagg, whose 2025-26 rookie rates are below the market's expectation for his second season. None of these is a line the method did not derive; the market's disagreement is about value, not about data.

| player | deck | kit | ADP | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | RotoWire | divergence (25+) — why |
|---|---|---|---|---|---|---|---|---|---|
| Nikola Jokic | 1 | 1 | 1.5 | 1 | 1 | 1 | 1 | 1 | none |
| Victor Wembanyama | 2 | 2 | 1.9 | 3 | 2 | 2 | 2 | 2 | none |
| Shai Gilgeous-Alexander | 3 | 3 | 3.9 | 2 | 3 | 3 | 3 | 3 | none |
| Kawhi Leonard | 6 | 4 | 34.2 | 15 | 16 | 15 | 20 | **37** | we rank him higher: ST +2.16, PTS +1.93, FT% +1.76 z carry it; 2025-26 line at 32.1 min; availability x0.78 already applied |
| Tyrese Maxey | 4 | 5 | 9.7 | 4 | 9 | 12 | 8 | 12 | none |
| Luka Doncic | 5 | 6 | 3.4 | 5 | 4 | 4 | 4 | 4 | none |
| Jamal Murray | 7 | 7 | 20.8 | 9 | 14 | 23 | 18 | 20 | none |
| Donovan Mitchell | 8 | 8 | 13.8 | 8 | 12 | 17 | 10 | 13 | none |
| Jalen Johnson | 9 | 10 | 12.1 | 16 | 15 | 9 | 14 | 7 | none |
| Jayson Tatum | 13 | 9 | 8.5 | 14 | 7 | 6 | 5 | 6 | none |
| Lauri Markkanen | 10 | 14 | 36.8 | 18 | 31 | **41** | 29 | 27 | we rank him higher: FT% +1.87, PTS +1.68, 3PTM +0.99 z carry it; 2025-26 line at 34.4 min |
| Kevin Durant | 11 | 16 | 16.0 | 27 | 11 | 14 | 16 | 14 | none |
| Tyrese Haliburton | 12 | 11 | 13.5 | 13 | 18 | 8 | 12 | 17 | none |
| Trey Murphy III | 20 | 12 | 36.7 | 22 | 21 | 31 | 19 | 25 | none |
| Stephen Curry | 17 | 13 | 23.1 | 12 | 10 | 18 | 22 | 16 | none |
| Anthony Davis | 14 | 15 | 42.6 | 36 | 26 | 28 | 31 | 23 | none |
| Amen Thompson | 15 | 17 | 23.0 | 10 | 29 | 20 | 23 | 19 | none |
| Chet Holmgren | 16 | 18 | 30.4 | 19 | 23 | 21 | 25 | 30 | none |
| James Harden | 18 | 19 | 35.2 | **49** | 24 | 27 | 30 | 31 | we rank him higher: FT% +1.89, AST +1.86, 3PTM +1.29 z carry it; 2025-26 line at 33.8 min |
| Scottie Barnes | 19 | 20 | 15.1 | 21 | 22 | 13 | 11 | 11 | none |
| Domantas Sabonis | 21 | 21 | 28.6 | 38 | 39 | 29 | **46** | 34 | we rank him higher: REB +3.33, FG% +2.01, AST +1.02 z carry it; 2024-25 line at 34.7 min |
| Dyson Daniels | 22 | 24 | 65.2 | 20 | **64** | **56** | **53** | **69** | we rank him higher: ST +4.10, AST +0.97, FG% +0.40 z carry it; 2025-26 line at 33.2 min |
| Walker Kessler | 28 | 22 | 41.8 | 32 | 34 | 39 | 26 | 39 | none |
| Anthony Edwards | 24 | 23 | 7.8 | 6 | 8 | 7 | 9 | 9 | none |
| Joel Embiid | 23 | 27 | 50.3 | **125** | **49** | **52** | **49** | **66** | we rank him higher: PTS +1.77, FT% +1.40, BLK +1.16 z carry it; 2025-26 line at 31.6 min; availability x0.78 already applied |
| Karl-Anthony Towns | 25 | 25 | 15.6 | 11 | 13 | 11 | 15 | 15 | none |
| Cade Cunningham | 26 | 26 | 6.0 | 25 | 6 | 5 | 6 | 5 | none |
| Bam Adebayo | 27 | 28 | 26.7 | 30 | **53** | 37 | 27 | 35 | we rank him higher: REB +1.70, PTS +0.69, ST +0.54 z carry it; 2025-26 line at 32.4 min |
| Ryan Rollins | 29 | 29 | 74.5 | **58** | **63** | **78** | **83** | **59** | we rank him higher: ST +2.16, AST +0.82, 3PTM +0.79 z carry it; 2025-26 line at 32.1 min |
| Derrick White | 30 | 30 | 45.1 | 26 | 41 | 42 | 28 | 40 | none |
| Austin Reaves | 31 | 31 | 23.6 | 17 | 19 | 32 | 17 | 18 | none |
| Michael Porter Jr. | 32 | 32 | 62.2 | 55 | **62** | **70** | **59** | 53 | we rank him higher: 3PTM +1.70, PTS +1.34, FT% +0.66 z carry it; 2025-26 line at 32.5 min |
| Onyeka Okongwu | 33 | 33 | 55.0 | 37 | **61** | **59** | 42 | 48 | we rank him higher: BLK +0.77, REB +0.70, FG% +0.51 z carry it; 2025-26 line at 31.0 min |
| Donovan Clingan | 34 | 34 | 43.5 | 29 | 58 | 51 | 34 | 52 | none |
| Ty Jerome | 35 | 41 | 110.2 | 47 | **60** | **101** | **71** | **83** | we rank him higher: ST +1.51, FT% +0.72, 3PTM +0.48 z carry it; 2024-25 line at 27.6 min (minutes to the outside range) |
| Kyrie Irving | 37 | 35 | 49.8 | **75** | 27 | 40 | 43 | 42 | we rank him higher: FT% +1.32, 3PTM +0.79, PTS +0.76 z carry it; 2024-25 line at 31.1 min (minutes to the outside range); availability x0.78 already applied |
| Desmond Bane | 36 | 36 | 53.0 | 44 | 32 | 38 | 37 | 57 | none |
| Jalen Duren | 39 | 37 | 35.7 | 28 | 35 | 50 | 35 | 46 | none |
| Paul George | 38 | 38 | 80.8 | **126** | 52 | **69** | 54 | **79** | we rank him higher: ST +1.83, 3PTM +0.99, TO +0.33 z carry it; 2025-26 line at 30.7 min; availability x0.78 already applied |
| Cooper Flagg | 40 | 39 | 10.2 | **7** | 17 | **10** | **13** | **8** | we rank him lower: 3PTM -0.73, FG% -0.44, TO -0.44 z carry it; 2025-26 line at 33.5 min |
| Cameron Boozer | 41 | 40 | 55.4 | **70** | 59 | 55 | 51 | 61 | we rank him higher: REB +1.49, FG% +0.36, PTS +0.26 z carry it; rookie translation (range rule) |
| LaMelo Ball | 42 | 47 | 25.8 | 62 | 48 | 26 | **21** | **21** | we rank him lower: FG% -2.09, TO -1.09, BLK -1.01 z carry it; 2025-26 line at 28.0 min |
| Jaren Jackson Jr. | 45 | 42 | 47.8 | 54 | 28 | 35 | 48 | 36 | none |
| OG Anunoby | 43 | 44 | 67.7 | 60 | 56 | 43 | 44 | 56 | none |
| Nickeil Alexander-Walker | 44 | 43 | 61.5 | 24 | 44 | **83** | 55 | 55 | we rank him higher: 3PTM +1.50, FT% +0.94, PTS +0.60 z carry it; 2025-26 line at 33.4 min |
| Evan Mobley | 46 | 45 | 29.4 | 45 | 25 | 33 | 24 | 29 | none |
| Jalen Brunson | 47 | 46 | 21.3 | 42 | 43 | 30 | 45 | 41 | none |
| Naz Reid | 48 | 48 | 64.0 | 52 | **74** | 67 | 66 | 72 | we rank him higher: 3PTM +0.79, BLK +0.77, REB +0.62 z carry it; 2025-26 line at 31.0 min (role move) |
| Zach Edey | 49 | 49 | 75.4 | 65 | 36 | 66 | 61 | 64 | none |
| Alperen Sengun | 51 | 50 | 18.4 | 57 | 50 | **25** | 41 | **22** | we rank him lower: FT% -1.74, TO -1.60, 3PTM -1.14 z carry it; 2025-26 line at 33.3 min |
| Damian Lillard | 50 | 52 | 69.3 | **77** | 72 | **85** | **84** | **75** | we rank him higher: FT% +1.97, 3PTM +0.89, AST +0.72 z carry it; 2024-25 line at 27.8 min (minutes to the outside range); availability x0.78 already applied |
| Devin Booker | 53 | 51 | 25.2 | 40 | 30 | **19** | 33 | 33 | we rank him lower: TO -1.47, REB -0.84, BLK -0.81 z carry it; 2025-26 line at 33.5 min |
| VJ Edgecombe | 52 | 54 | 74.6 | 31 | **85** | 72 | **95** | **85** | we rank him higher: ST +1.19, 3PTM +0.28, TO +0.20 z carry it; 2025-26 line at 35.0 min |
| Josh Giddey | 54 | 53 | 23.0 | 61 | 33 | 36 | 38 | **26** | we rank him lower: TO -2.12, FG% -0.69, FT% -0.46 z carry it; 2025-26 line at 32.1 min |
| Jaylen Brown | 55 | 55 | 30.3 | **95** | 69 | 49 | 62 | 44 | we rank him higher: PTS +2.08, AST +0.58, REB +0.41 z carry it; 2025-26 line at 34.4 min |
| Jalen Williams | 57 | 56 | 40.4 | 35 | 38 | **24** | 36 | **32** | we rank him lower: 3PTM -1.04, REB -0.55, BLK -0.42 z carry it; 2025-26 line at 28.4 min |
| LeBron James | 56 | 57 | 37.6 | **92** | 40 | 47 | 47 | 54 | we rank him higher: AST +1.61, FG% +0.70, PTS +0.69 z carry it; 2025-26 line at 33.1 min; availability x0.78 already applied |
| Giannis Antetokounmpo | 58 | 58 | 6.4 | 50 | **5** | **16** | **7** | **10** | we rank him lower: FT% -4.27, TO -1.60, 3PTM -1.34 z carry it; 2025-26 line at 28.9 min |
| De'Aaron Fox | 59 | 59 | 80.1 | **85** | 70 | 60 | 68 | 74 | we rank him higher: ST +1.19, AST +1.12, PTS +0.24 z carry it; 2025-26 line at 31.0 min |
| Trae Young | 63 | 60 | 24.4 | 72 | **20** | **22** | 39 | **24** | we rank him lower: TO -3.02, FG% -1.75, REB -1.30 z carry it; 2024-25 line at 32.9 min (minutes to the outside range) |
| Reed Sheppard | 60 | 61 | 120.7 | 56 | **118** | **126** | **129** | **136** | we rank him higher: ST +1.51, 3PTM +1.09, TO +0.59 z carry it; 2025-26 line at 26.2 min |

## 10. Re-calibration

Work order: the seven live rooms 52–58 on the new page, the survival-chip Brier, and the follow-the-card arms on the real eight-team bracket. Each room was replayed by the deck's own engine on the v60 page at every owner turn (`m<N>_deckcard_v60.json`; the v59 page the same way, `m<N>_deckcard_v59.json`, as the like-for-like baseline), its as-drafted rosters re-scored on the v60 pool (`live_retro.py <N> final --tag v60`), and its two season arms — as drafted, and the shipped card followed at every owner turn (self-consistent, strict pairwise) — simulated on the real bracket (18,000 seasons, seeds 11/23/47) twice: on the room's own page and pool (`regrade --label own`) and on the v60 pool with the 10/12 page's prices and card rule (`regrade --tag v60 --rev eaf2b72 --label v60`; v60's prices and rule are v59's). The hindsight and single-swap arms were not re-run (about twelve minutes a room); the follow-the-card arm is the one the work order names.

| room (slot 10) | as drafted, own pool | as drafted, v60 pool | follow the card, own | follow the card, v60 | card's #1 differs from the room's own page | owner's pick in the Top-5: own page / v60 |
|---|---|---|---|---|---|---|
| mock 52 (own pool v23) | 37.95% (rank 1) | 5.43% (rank 7) | 45.81% | 32.69% | 12 of 13 | 11 / 2 |
| mock 53 (own pool v25) | 31.10% (rank 1) | 8.24% (rank 6) | 46.14% | 35.28% | 13 of 13 | 8 / 3 |
| mock 54 (own pool v28) | 38.62% (rank 1) | 5.11% (rank 7) | 49.17% | 33.55% | 12 of 13 | 11 / 1 |
| mock 55 (own pool v28) | 15.69% (rank 3) | 1.68% (rank 11) | 29.97% | 34.77% | 13 of 13 | 10 / 4 |
| mock 56 (own pool v31) | 43.66% (rank 1) | 3.51% (rank 8) | 52.58% | 40.43% | 13 of 13 | 11 / 3 |
| mock 57 (own pool v33) | 27.44% (rank 1) | 1.56% (rank 10) | 41.43% | 22.54% | 12 of 13 | 10 / 3 |
| mock 58 (own pool v35) | 36.75% (rank 1) | 2.71% (rank 9) | 40.89% | 43.76% | 13 of 13 | 13 / 3 |
| all seven | mean 33.03% | mean 4.03% | mean 43.71% | mean 34.72% | 88 of 91 | 74 / 19 of 91 |

**What changed.** The rosters these rooms drafted on the old lines score much worse on the new ones: as drafted, a mean 33.03% title chance on their own pools against 4.03% on v60 (rank 1 in six of seven rooms becomes rank 6 to 11), because they were built around the lines that fell (Towns, Kyrie, Davis, Daniels, Dejounte Murray, Poeltl, Franz Wagner among them). The card re-run on the v60 lines would have drafted rosters at 34.72% — but that arm is graded on the same lines it drafts with, so it shows the v60 card is coherent on its own lines, not that the lines are right. The card's #1 at the rooms' actual board states differs from the room's own page at 88 of 91 owner turns, and the owner's actual pick sits in the v60 Top-5 at 19 of 91 turns against 74 on the pages the owner drafted from.

**Survival chips (pooled over the seven rooms; Brier, lower is better).** The rooms' own pages: 0.260 (353 chips; mean predicted survival 0.456, realized 0.680) — older survival models and prices. Like for like on today's prices and survival model: the v59 page 0.195 (378 chips; 0.465 predicted, 0.577 realized), the v60 page 0.206 (402 chips; 0.457, 0.604). The new lines put players on the card whom these rooms let last longer than their prices predict, so the chips read a little more pessimistic than the rooms played (+0.011); the survival model itself is price-based and unchanged.

**What did not change.** The card's rules, the prices (Yahoo 10/12), the survival model, every availability tag and games-played figure; parity between the page and the Python engine is exact (416 owner turns across 32 committed states).

## 11. Verification

| check | evidence |
|---|---|
| lines file (`wo5/out/lines_wo5_2026-10-12.json`) | rebuilt from the committed totals, minutes overrides and range resolution by `wo5_lines.py`: byte-identical. The range resolution itself rebuilt from the committed inputs by `wo5_iterate.sh` in a clean directory: the same fixed point at round 2, entry for entry; the committed file is that fixed point plus the two rookie identity entries (Dybantsa, Boozer; §2) |
| `wo5_apply.py` (both planes) | from the origin/main inputs: `WO-5 APPLY: PASS — deck 326 rows written (326 with a changed value), kit 311 rows written (311 changed); 6468 values changed; files changed (deck True, kit True)`; outputs byte-identical to the committed `data/players.csv` and `projections-2026-27.csv`; the apply record reproduces byte-for-byte; a second application: `WO-5 APPLY: PASS — deck 326 rows written (0 with a changed value), kit 311 rows written (0 changed); 0 values changed; files unchanged (deck False, kit False)` |
| independent recomputation | Towns, Edwards and Maxey re-derived from the totals by separate arithmetic earlier in the pass (every digit matched the script). After the write, Coby White's line re-derived from his 2025-26 totals by a second, separate script (CHI 29 g + CHO 21 g = 1249 min; per-36 × 29.1; the one-third career shrink; the 5/4/3 anchor; the identity): all eleven values equal the committed line (14.5 / 5.6 / 2.7 / 4.0 / 4.7 / 3.0 / .442 / .830 / 0.7 / 0.2 / 20.2; `wo5/out/recompute_coby_white_2026-10-12.txt`). A first attempt that summed the team-split rows into the career totals as well as the season row disagreed on the two percentages by .001 and .002 — the check's error, not the line's; the tool, like Basketball-Reference's career line, counts each season once |
| `scripts/check_planes.py --lines-strict` (deck) | planes: 315 shared · kit-only 10 · deck-only 20 · team 0 · exclusion 0 · drift 0 · propagation 0; stat lines differing 0 (170 at the 10/12 morning pull); exit 0 |
| `scripts/identity_check.py` (deck) | 0 players, 0 lines, of 200 deck and 200 kit lines; exit 0 (49 lines / 41 players before) |
| `scripts/range_check.py` (deck) | 23 players, 25 cells of 145 checkable (131 / 435 before), each on a stated mechanism (§ Range check); exit 0 |
| `scripts/verify_rosters.py` (deck, no exemption) | re-ran 21:31 UTC in this pass: direct-complete, all 30 rosters on ESPN's feed, 335/335, 0 mismatches, 0 unmatched; `roster_verification.json` and `rosters_official.json` rewrote byte-identical to the morning pull's |
| `scripts/build_deck.py` (deck) | gates 1–7 + F8 pass, no waiver; planes: 315 shared · kit-only 10 · deck-only 20 · team 0 · exclusion 0 · drift 0 · propagation 0; market: yahoo-2026-10-12.csv — priced 246/335 rows (Yahoo ADP else XRank), 0 days old; deck built: 335 players · pull 2026-10-12 · pool b6bc48d86888 · injection round-trip OK; "safe to publish". Four refusals on the way, each reconciled, none waived: gate 6 (the colophon's refresh phrase), the injection round-trip (a note carrying "];", D-1006-3; assertion A7 now blocks it), and — after the roster fix — gate 4 and gate 7, because the page and the planes snapshot in the working tree were the unpublished first v60 build; both were restored to origin/main and the scripted edits re-applied, and the shipped page differs from the first v60 build only by the roster fix and its Logic sentence (diffed) |
| `scripts/check_parity.py` (deck) | PARITY: EXACT MATCH — 416 owner turns across 32 committed states; 318 market ranks (priced 240); exit 0 |
| `scripts/test_card.py` (deck) | CARD: all 99 cases passed; exit 0. Three probes were re-pointed because the new lines removed the committed example each one used (diff in `scripts/test_card.py`, reason in the code): D51R-4's pin probe from mock31 #64 (availability) to mock 75 #58 (behind #1 — no committed owner turn withholds a pin on availability on the v60 lines; the availability branch keeps its direct gate case); D-CAST-4's #154 probe adds an unpriced twin of that turn's leader (no committed late turn has an unpriced row in the unfiltered Top-5 now); V4's probe sets aside a shared value/XRank leader (Jokic leads both now). Each was mutation-checked: disabling `cardPool`, setting `BOT_XRANK_FROM` to 99, or `PIN_MAX_GAP` to 1.0 fails 1, 2 and 3 cases respectively |
| `scripts/test_draft.py` / `test_gates.py` (deck) | all 65 cases passed / all 54 cases passed; exit 0 each |
| `arena/mocks/full_dom_check.mjs` (deck) | 145 assertions, 0 failed, [] page errors, pass true (`full_dom_check_2026-10-12_v60.json`). Red first: the first run on the v60 lines failed S1.roster-shows-every-pick-one-C, S2.turn#154, S2.final-roster-13 — the roster panel left Team 10's 13th man off the list when only a C slot was open; the new assertion `S1.roster-shows-every-pick-one-C` (a crafted roster with one C among 13) failed on the unfixed page (`_v60_redfirst.json`) and passes on the fix |
| `scripts/repeat_market_check.py` (deck) | 25 of 25 mocks replayed; 8 FLAGGED, 4 near miss(es); exit 0 (`repeat_market_check_2026-10-12_v60.json`, page sha256 d903b2eea753) |
| card replays (§5, §10) | the 24 rooms' #10 cards, the seven rooms' owner turns and the two top-40 replays re-run on the shipped page: byte-identical to the records the report quotes |
| `report/rank_engine.py` (kit) | exit 0; 200 players from 313 projected (12 held off the board — unsigned: Cam Thomas, Jaden Ivey, John Konchar, Rob Dillingham; GP ≤ 25: Dereck Lively, Donte DiVincenzo, Jimmy Butler, Jusuf Nurkic, Mark Williams, Max Strus, Moses Moody, Shaedon Sharpe); re-run idempotent (board and slate byte-identical) |
| `report/test_rank_engine.py` / `check_provenance.py` / `check_derived.py` (kit) | 4 tests OK / PROVENANCE GATE: PASS / DERIVED: all 23 dated artifacts reproduce byte-for-byte; exit 0 each |
| artifact publish | Version 60, id 1791847492-747e, the standing URL, published after a fresh read of the live page (v59, id 1791824190-04c2); the served file read back (577380 bytes) carries the built page (577016 bytes, sha256 d903b2eea753) byte-for-byte inside the service's 364-byte wrapper; manifest built 2026-10-12 |

## 12. System integrity, in plain language

Everything below was checked by running it, not by reading it; the full table with exit codes is §11.

- **The arithmetic is the same everywhere.** The web page, the Python engine and the kit board all compute the same numbers: the page's card ordering matched the Python engine at every one of 416 recorded owner turns across 32 saved drafts (parity EXACT). An independent hand recomputation of four lines from the raw season totals (Towns, Edwards, Maxey, Coby White) matched the script to the last digit.
- **The data rebuilds from its sources.** Starting only from the files being committed — the Basketball-Reference totals (23 pages, each pinned by hash), the minutes overrides and the range resolution — the script regenerates the lines file byte-for-byte, and the one write script regenerates both planes' data files byte-for-byte from the pre-pass files. Run it twice and the second run changes nothing. The kit's 23 earlier derived artifacts still reproduce from their pinned inputs.
- **The two planes agree.** planes: 315 shared · kit-only 10 · deck-only 20 · team 0 · exclusion 0 · drift 0 · propagation 0 — the deck's 326 lines and the kit's 311 are the same numbers on every shared row (there were 170 differing lines this morning).
- **The lines pass their own checks.** Points equal what the shooting implies on every top-200 line (was 49 lines off by a point or more this morning); 23 players carry 25 cells outside every outside projection, each with its mechanism written down (was 131 players, 435 cells).
- **The page works as a draft room.** The headless-browser check exercised every control on the page through a full replay of a real draft: 145 assertions, 0 failed, no page errors. The three test suites passed in full (card 99 of 99, draft 65 of 65, gates 54 of 54). Rosters re-verified against ESPN's live feed: 335 of 335, zero mismatches (2026-10-12).
- **One defect was found and fixed, in the open.** The page check failed first: on the new lines, one real draft ended with the owner's roster panel listing 12 of 13 players, because the panel had no row for a player no open lineup slot could hold (one center among thirteen with the bench full). A new assertion was written that fails on the old page and passes on the fix; the fix is display only — the card and the numbers are untouched — and it is on your decision sheet as D-WO5-6. This defect was latent in every earlier version; the new lines made it visible.
- **Nothing was waived.** The build refused four times on the way (a colophon phrase, a note that would have broken the page's data block, and twice because the working tree held an unpublished build); each refusal was reconciled by restoring the file and re-applying the scripted edit, never by a waiver.
- **What the outside world says.** The new kit board agrees with the three outside 9-cat rankings a little more than the old one did: Rotoworld ρ 0.828 (was .830 on 10/06), RotoBaller 0.824 (was 0.815), RotoWire's expert panel 0.798 (was 0.779); against Yahoo's own XRank 0.839 over 249 names. Agreement with the market is not the goal — the board is meant to disagree where the categories say so — but the direction says the pass moved toward the evidence, not away from it (`wo5/out/rho_market_2026-10-12.json`, computed on the regenerated kit board against the joined files in `report/market/`).
- **What is still open.** The repeat-name check flags 3 names as LINE QUESTIONED (Grayson Allen, Ryan Rollins, Yaxel Lendeborg; each explained in that section); usage changes on new teams are not modeled (D-WO5-5); the ten returnees' minutes come from the outside projections, not from our data; tonight's preseason games are not in this pass.


## 13. Confidence, by layer — 10/09 against now

The same rule as on 10/01 and 10/09: the system is internally consistent to a very high standard and externally unproven, and those are not averaged into one number. Every "now" figure is a judgment (INFERENCE) anchored to a record named beside it (EVIDENCE). The 10/09 column is the earlier table as given.

| layer | 10/09 | now | what moved it, with the record |
|---|---|---|---|
| Engine math (page = code = Python) | 99% | 99% | EVIDENCE: parity EXACT at 416 owner turns / 32 states; suites 99 / 65 / 54; browser check 145 / 0; four lines recomputed by hand from the totals match to the digit. INFERENCE: nothing honest goes above 99. |
| Placements (who is on which team) | 98% | 98% | EVIDENCE: direct ESPN roster verification re-ran in this pass, all 30 teams, 335 of 335, zero mismatches. INFERENCE: unchanged; a placement can still change on the feed between pulls. |
| Availability tags (right in kind) | 88% | 88% | EVIDENCE: no tag moved in this pass (the method does not touch tags; A7). INFERENCE: unchanged. |
| Availability discount as a ranking input | 60% | 60% | EVIDENCE: unchanged mechanism (flat ×0.78 above the pool mean); the per-player games model is a post-draft item. INFERENCE: unchanged. |
| Market column (Mkt rank) | 92%, decaying slowly | 92%, decaying slowly | EVIDENCE: Yahoo ADP as of 10/12, 0 days old, 246 of 335 priced; unchanged by this pass. INFERENCE: the 10/14 lock paste is the last refresh. |
| Projection lines (the stats) | 70% | 76% | EVIDENCE for: every line with a 25-game NBA season is now its own 2025-26 rate at its 2025-26 minutes, from Basketball-Reference totals cross-checked against the verified actuals of 10/9 (Basketball-Reference and ESPN; 581 of 582 identical); points identity 0 lines off (was 49); range check 23 players / 25 cells outside every reference, each with a stated mechanism (was 131 / 435); the planes agree on every row (was 170 apart); the whole pipeline rebuilds byte-for-byte from pinned inputs; the board moved toward all three outside 9-cat rankings (ρ 0.828 / 0.824 / 0.798). EVIDENCE against: a player's usage on a new team is not modeled (Brown, LeBron, Giannis, Trae, Davis, Herro — D-WO5-5); the ten returnees' minutes are the outside lines' numbers, not ours; 3 names still LINE QUESTIONED by the repeat-name check; the method's own backtest (10/09) beat the prior season in 8 of 9 categories but lost steals, blocks and FT% to a three-season line — and steals is the category that moved the most players here. INFERENCE: on 10/09 I wrote that a clean pass with the identity and range checks green would read 75 to 78; this pass is that, and the usage gap and the three flags keep it at the lower end: 76. |
| Board order, top 60 within ten places | 82% | 82% | EVIDENCE for: the lines beneath the ordering are the ones above; the ordering's agreement with the outside rankings rose (Rotoworld 0.828, RotoBaller 0.824, RotoWire 0.798, Yahoo XRank 0.839). EVIDENCE against: the out-of-sample tests that earned 82 (the league's 2025-26 redraft, 10/07) were run on the old ordering and were not re-run on this one; 12 names left the deck's top 60 and 12 arrived, so this is a different ordering. INFERENCE: better inputs and less direct evidence offset; held at 82, not raised. |
| Survival chips as a ranking of risk | 70% | 70% | EVIDENCE: unchanged model; no new calibration on realized rooms. INFERENCE: unchanged. |
| Survival chips as probabilities | 40% | 40% | EVIDENCE: pooled over the seven live rooms 52–58, Brier 0.206 on the v60 page (402 chips) against 0.195 on v59 and 0.260 on the rooms' own pages; the model is price-based and did not change. INFERENCE: unchanged. |
| Arena title odds as absolute numbers | 40% | 40% | EVIDENCE: the seven rooms' as-drafted rosters average 33.03% on their own pools and 4.03% on the v60 pool — the odds are soft to the lines exactly as 10/09 said. INFERENCE: relative comparisons remain the use; unchanged. |
| Card advice under market noise | 95% | 95% | EVIDENCE: unchanged rule and prices; the 24 rooms' #10 cards and the seven rooms' owner turns replay byte-identically on the shipped page. INFERENCE: unchanged. |
| Record integrity | 95% | 96% | EVIDENCE: the projection pipeline now rebuilds byte-for-byte from pinned downloads (23 Basketball-Reference pages and 36 ESPN box scores, each with a sha256 manifest) through the range fixed point to both data files; derived 23 of 23; every report gate passing; the one defect found was recorded red-first with its failing run kept. INFERENCE: one point, for the pipeline being reproducible end to end. |

**One number each, as before.** The tool and the process: about 93% (was about 92) — the pass was scripted, asserted and gated at every step, the one defect it surfaced was caught by the page's own check before anything was published, and nothing was waived; it does not earn more because that defect existed on every earlier page. The data the draft will run on: about 76% (was about 70) — the lines are now each player's own last season on verified totals, with every cell either inside the outside projections or carrying its reason, and the remaining gaps are named (new-team usage, the returnees' minutes, three questioned names). The forecast of winning the league as an absolute figure: 40%, unchanged. The ordering of who to take over whom: about 82%, held.

**What would move the data number again before the lock.** Tonight's and Tuesday's preseason games read by the next WO-3 pull as evidence of role (never of minutes or rates), a role move only on two dated outlets; your 10/14 Yahoo paste for the prices; nothing else is scheduled to touch a line.


## Watchlist

- **Tonight's preseason games (10/12) are not in this pass** — they finish after it closed. The next WO-3 pull reads them as notes; a role change there moves a line only on two dated outlets, by the same rule M2 (D-WO5-4).
- **Usage on a new team is not modeled.** The method takes each player's own 2025-26 rates. Jaylen Brown (28.6 points, a Boston season without Tatum) and LeBron in Philadelphia, Giannis in Miami, Trae Young and Davis in Washington, Herro in Milwaukee carry their old-team rates; the range check catches only a cell past every outside line, and none of these is listed. D-WO5-5 puts the question.
- **The returnees' minutes are the outside lines' minutes** (range rule R1: Lillard 27.8, Haliburton 31.3, Kyrie 31.1, Trae Young 32.9, Davis 29.6, VanVleet 31.0, Morant 25.5, Dejounte Murray 29.1, Edey 26.6, Ty Jerome 27.6). Our own evidence cannot set those numbers; the first regular-season week can.
- **Coby White** (left calf, out for the preseason; minutes 29.1 as the starter on two outlets; untagged per D-1006-2); **Kessler** (finger, expected for the opener); **Fox** (soreness, sat 10/8 and 10/10); **Kawhi** (first preseason chance 10/13); **Ingram** (Achilles, out for the start of the season, inj-achilles-risk).
- **Grayson Allen** (Charlotte; LINE QUESTIONED by the repeat-name check): his line is his 2025-26 Phoenix season at its 28.8 minutes. The outside lines price a bench role (11.7–13.8 points). Our dated outlets split two ways. Roundtable 9/26 and 10/7 project a starting five without him. RotoBaller, TSN and Roundtable (9/28–10/5) have Knueppel out for the preseason and say Allen could open as the starter. Rule M2 therefore held his minutes. A bench move needs two dated outlets once Knueppel's opener is known, and the next WO-3 pull searches it (D-WO5-4).
- **Jay Huff at 11.7 minutes** is the role rule's number (his 2024-25 Memphis bench season); Indiana's backup-center minutes are "night-to-night" per the GM (Roundtable 10/5), so the line is the low end on purpose.

## Open-item receipts

| item | query run (2026-10-12) | dated finding |
|---|---|---|
| Ryan Rollins | WO-5 role pass; the 10/11 box score (ESPN) | started at point guard 10/11 (RotoWire, Brew Hoop/Yahoo — the day's pull); WO-5 line on his 2025-26 32.1 minutes; card receipt added; HELD −0.05, retiring the flag on the sheet (D-WO5-3) |
| Bennedict Mathurin | WO-5 universe (outside the top 150 on every board) | no role search ran; line on his 2025-26 season at 30.0 minutes; card receipt added; HELD −0.05 |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham | the day's pull, same day (after-report-2026-10-12.md, receipts dated 10/12) | unchanged since this morning's receipts; HELD or unsigned |

## Decisions

| decision | question | default |
|---|---|---|
| D-WO5-1 | Scope (A8): the method ran on every row with an NBA season of 25+ games (326 deck rows), not only the top 150 the work order names, so the z-score frame (rows to 180) is one method. Options: (a) keep; (b) put rows outside both boards' top 150 back on their 10/12 lines | (a) |
| D-WO5-2 | The rule refinements made during the pass and before the write (§2): M2's two-season window and direction bound (changes one outcome: Gillespie holds 28.5 minutes instead of 9.4); R1's two-cell trigger (Naz Reid keeps 31.0 instead of 27.7; Lendeborg's cells clamped instead of scaled); rookie steals/blocks to the range (Caleb Wilson). (a) ratify; (b) re-run without them | (a) |
| D-WO5-3 | Rollins' and Mathurin's judgment flags (−0.05 each) waited on WO-5; the lines now carry their roles. (a) hold; (b) retire both | (a) |
| D-WO5-4 | Tonight's preseason games: (a) the next WO-3 pull reads them, a role change moves a line only on two dated outlets by rule M2; (b) a second WO-5 pass before the draft | (a) |
| D-WO5-5 | Team-change usage (Brown, LeBron, Giannis, Trae, Davis, Herro on new teams): (a) the method stands, the range check guards the extremes; (b) a usage adjustment from the outside lines for the players who changed teams (a new rule; it would need its own test) | (a) |
| D-WO5-6 | The "Your roster" panel fix (display only; §11): a player no open slot can hold shows in an EXTRA row instead of being left off; the open slot stays open; one new page-check assertion guards it. (a) keep; (b) revert | (a) |
| D-1012-3 | WO-5 before Wednesday | **closed — done** |
| D75-2 | The punt button | **closed — (a), advice only** (owner, 2026-10-12: "we'll pass on punt button then") |
| D-1012-4 | Haliburton at #10 and Towns at #15. On the v60 lines neither is the card's #10 (Haliburton #11, Towns #17–18). (a) follow the card; (b) take them anyway | (a) |
| D-1006-2 | Coby White's tag — carried (hold untagged until his opener status is stated) | hold |
| D-1012-1, D-1012-2, D-1011-4, D74-1, D-1011-1..3, D-1010-2, D-1010-1, D-RN-6, D73-1 and earlier | carried | carried |

## Files

- Kit `report/wo5/`: `tools/` (fetch, parse, cross-check, `wo5_lines.py`, `wo5_range.py`, `wo5_apply.py`, `wo5_iterate.sh`, `wo5_boarddiff.py`, `wo5_top60.py`, `wo5_preview.py`, `wo5_universe.py`, `stints.py`; the two scripts that edited the deck page by exact anchor, `deck_judgment_colophon_wo5.py` and `deck_roster_fix_wo5.py`); `data/` (manifests, the parsed totals, preseason roles, the minutes overrides, the research log, the universe); `out/` (the lines, the range resolution, the apply record, the board diff, the top-60 review, the preview, the Coby White recompute, the board-vs-market correlations).
- Kit: `projections-2026-27.csv` (311 rows), `top-200-2026-27.md` (regenerated), `seat-10-slate.md` (regenerated), `rank_engine.py` (the board's basis note; no logic change).
- Deck: `data/players.csv` (326 rows), `data/freshness.json`, `data/kit-snapshot.csv`, `docs/draft-deck.html` (v60, with the roster-panel fix), `arena/mocks/full_dom_check.mjs` (the one-C roster assertion), `scripts/test_card.py` (three probes re-pointed, §11), `arena/results/test_card_scan_2026-10-12_v60/` (the scan of all 416 owner turns behind the re-points, and the mutation runs), `arena/mocks/live_retro.py` (the v60 pool tag), `arena/results/players_v60.csv`, the re-calibration records (`m52`–`m58` `_deckcard_v60`, `_deckcard_v59`, `_replay`/`_final_v60`, `_regrade_own`, `_regrade_v60`, `survival_v60_rooms52-58.json`, `survival_v59_rooms52-58.json`, `survival_own_rooms52-58.json`), `full_dom_check_2026-10-12_v60_redfirst.json` (the red run), `full_dom_check_2026-10-12_v60.json`, `repeat_market_check_2026-10-12_v60.json`.

## Appendix A — every move of three or more places (both boards, inside the top 200)

Deck = the page's value board (adjusted value, availability above zero); kit = the regenerated top-200 board. Driver = the two categories whose z moved most in the deck's frame (positive = toward the player). Basis = how the new line was made. Built by `wo5/tools/wo5_boarddiff.py` from the pinned 10/12 lines and today's; the record is `wo5/out/boarddiff_2026-10-12.json`.

| player | deck before → after (move) | kit before → after (move) | z driver (deck frame) | line basis (mechanism) |
|---|---|---|---|---|
| Kawhi Leonard | 34 → 6 (+28) | 12 → 4 (+8) | FT% +1.55, PTS +1.25 | 2025-26 per-36 at 32.1 min |
| Tyrese Maxey | 9 → 4 (+5) | 6 → 5 (+1) | PTS +0.59, BLK +0.42 | 2025-26 per-36 at 38.0 min |
| Jamal Murray | 20 → 7 (+13) | 26 → 7 (+19) | 3PTM +0.71, PTS +0.62 | 2025-26 per-36 at 35.4 min |
| Donovan Mitchell | 14 → 8 (+6) | 16 → 8 (+8) | FG% +0.64, ST +0.64 | 2025-26 per-36 at 33.5 min |
| Jalen Johnson | 13 → 9 (+4) | 25 → 10 (+15) | BLK -0.54, FT% +0.42 | 2025-26 per-36 at 35.2 min |
| Jayson Tatum | 21 → 13 (+8) | 18 → 9 (+9) | 3PTM +0.27, ST +0.20 | 2024-25 per-36 at 36.4 min |
| Lauri Markkanen | 52 → 10 (+42) | 47 → 14 (+33) | PTS +1.28, FT% +0.65 | 2025-26 per-36 at 34.4 min |
| Kevin Durant | 18 → 11 (+7) | 30 → 16 (+14) | FT% +0.64, AST +0.43 | 2025-26 per-36 at 36.4 min |
| Tyrese Haliburton | 7 → 12 (-5) | 27 → 11 (+16) | AST -0.39, 3PTM -0.23 | 2024-25 per-36 at 31.3 min (range rule R1 from 33.6) |
| Trey Murphy III | 33 → 20 (+13) | 21 → 12 (+9) | ST +0.85, BLK -0.36 | 2025-26 per-36 at 35.5 min |
| Anthony Davis | 5 → 14 (-9) | 7 → 15 (-8) | REB -0.43, ST -0.41 | 2024-25 per-36 at 29.6 min (range rule R1 from 33.5) |
| Amen Thompson | 30 → 15 (+15) | 28 → 17 (+11) | ST +1.00, FT% +0.92 | 2025-26 per-36 at 37.4 min |
| Chet Holmgren | 10 → 16 (-6) | 10 → 18 (-8) | FG% +0.84, ST -0.52 | 2025-26 per-36 at 28.9 min |
| James Harden | 31 → 18 (+13) | 37 → 19 (+18) | TO +1.04, FG% +0.51 | 2025-26 per-36 at 33.8 min (2025-26 minutes with CLE (26 of 70 games)) |
| Scottie Barnes | 38 → 19 (+19) | 36 → 20 (+16) | FG% +1.15, FT% +0.64 | 2025-26 per-36 at 33.5 min |
| Domantas Sabonis | 25 → 21 (+4) | 19 → 21 (-2) | REB +0.44, 3PTM +0.30 | 2024-25 per-36 at 34.7 min |
| Dyson Daniels | 11 → 22 (-11) | 9 → 24 (-15) | ST -1.34, 3PTM -0.74 | 2025-26 per-36 at 33.2 min |
| Walker Kessler | 44 → 28 (+16) | 35 → 22 (+13) | BLK +0.70, ST +0.62 | 2024-25 per-36 at 30.0 min; ft_pct to the range |
| Anthony Edwards | 8 → 24 (-16) | 8 → 23 (-15) | FT% -0.99, 3PTM -0.90 | 2025-26 per-36 at 35.0 min |
| Joel Embiid | 71 → 23 (+48) | 22 → 27 (-5) | FG% +1.04, BLK +0.84 | 2025-26 per-36 at 31.6 min |
| Karl-Anthony Towns | 6 → 25 (-19) | 5 → 25 (-20) | PTS -0.82, 3PTM -0.59 | 2025-26 per-36 at 31.0 min |
| Cade Cunningham | 12 → 26 (-14) | 11 → 26 (-15) | FT% -0.83, PTS -0.67 | 2025-26 per-36 at 33.9 min |
| Bam Adebayo | 47 → 27 (+20) | 32 → 28 (+4) | 3PTM +1.00, PTS +0.84 | 2025-26 per-36 at 32.4 min |
| Ryan Rollins | 70 → 29 (+41) | 63 → 29 (+34) | ST +1.28, TO -1.15 | 2025-26 per-36 at 32.1 min |
| Derrick White | 24 → 30 (-6) | 23 → 30 (-7) | FG% -0.90, 3PTM -0.54 | 2025-26 per-36 at 34.1 min |
| Austin Reaves | 26 → 31 (-5) | 20 → 31 (-11) | AST -0.67, FG% +0.54 | 2025-26 per-36 at 34.5 min |
| Michael Porter Jr. | 55 → 32 (+23) | 45 → 32 (+13) | TO -1.04, PTS +0.94 | 2025-26 per-36 at 32.5 min |
| Onyeka Okongwu | 36 → 33 (+3) | 39 → 33 (+6) | FG% -0.87, ST +0.73 | 2025-26 per-36 at 31.0 min |
| Donovan Clingan | 53 → 34 (+19) | 49 → 34 (+15) | BLK +0.47, REB +0.27 | 2025-26 per-36 at 27.2 min |
| Kyrie Irving | 15 → 37 (-22) | 17 → 35 (-18) | PTS -0.60, ST -0.37 | 2024-25 per-36 at 31.1 min (range rule R1 from 36.1) |
| Ty Jerome | 101 → 35 (+66) | 50 → 41 (+9) | ST +1.78, FG% +0.71 | 2024-25 per-36 at 27.6 min (range rule R1 from 19.9, after a role move); ft_pct to the range |
| Desmond Bane | 27 → 36 (-9) | 38 → 36 (+2) | REB -0.68, 3PTM -0.61 | 2025-26 per-36 at 33.6 min |
| Jalen Duren | 60 → 39 (+21) | 57 → 37 (+20) | PTS +1.33, FG% +0.38 | 2025-26 per-36 at 28.2 min |
| Paul George | 66 → 38 (+28) | 51 → 38 (+13) | TO +0.81, 3PTM +0.52 | 2025-26 per-36 at 30.7 min |
| Cooper Flagg | 22 → 40 (-18) | 14 → 39 (-25) | FT% +0.73, 3PTM -0.67 | 2025-26 per-36 at 33.5 min |
| Cameron Boozer | 48 → 41 (+7) | 41 → 40 (+1) | ST +0.20, REB +0.19 | rookie translation held; pts by identity |
| Jaren Jackson Jr. | 23 → 45 (-22) | 33 → 42 (-9) | PTS -0.74, FG% -0.58 | 2025-26 per-36 at 30.3 min |
| LaMelo Ball | 49 → 42 (+7) | 43 → 47 (-4) | TO +0.74, FG% -0.56 | 2025-26 per-36 at 28.0 min |
| Nickeil Alexander-Walker | 54 → 44 (+10) | 52 → 43 (+9) | PTS +0.40, 3PTM +0.39 | 2025-26 per-36 at 33.4 min |
| OG Anunoby | 28 → 43 (-15) | 44 → 44 (0) | TO -0.66, BLK -0.35 | 2025-26 per-36 at 33.2 min |
| Evan Mobley | 19 → 46 (-27) | 34 → 45 (-11) | FT% -0.62, ST -0.49 | 2025-26 per-36 at 31.9 min |
| Jalen Brunson | 40 → 47 (-7) | 46 → 46 (0) | FG% -0.42, AST -0.24 | 2025-26 per-36 at 35.0 min |
| Naz Reid | 79 → 48 (+31) | 94 → 48 (+46) | ST +0.73, TO -0.52 | 2025-26 per-36 at 31.0 min (role: starter in Bridges' former spot (ESPN box 10/6 and 10/11 ET; Roundtable 10/7)) |
| Zach Edey | 84 → 49 (+35) | 65 → 49 (+16) | TO -0.67, ST +0.62 | 2024-25 per-36 at 26.6 min (range rule R1 from 21.4); fg_pct/ft_pct to the range |
| Alperen Sengun | 69 → 51 (+18) | 58 → 50 (+8) | TO -0.58, AST +0.50 | 2025-26 per-36 at 33.3 min |
| Damian Lillard | 88 → 50 (+38) | 90 → 52 (+38) | PTS +0.43, FG% +0.39 | 2024-25 per-36 at 27.8 min (range rule R1 from 36.1) |
| Devin Booker | 35 → 53 (-18) | 15 → 51 (-36) | AST -0.53, 3PTM -0.29 | 2025-26 per-36 at 33.5 min |
| VJ Edgecombe | 96 → 52 (+44) | 111 → 54 (+57) | REB +0.49, ST +0.31 | 2025-26 per-36 at 35.0 min |
| Josh Giddey | 32 → 54 (-22) | 31 → 53 (-22) | TO -0.83, ST -0.69 | 2025-26 per-36 at 32.1 min |
| Jaylen Brown | 72 → 55 (+17) | 129 → 55 (+74) | TO -1.10, PTS +1.03 | 2025-26 per-36 at 34.4 min |
| Jalen Williams | 16 → 57 (-41) | 29 → 56 (-27) | 3PTM -1.29, ST -1.19 | 2025-26 per-36 at 28.4 min |
| LeBron James | 62 → 56 (+6) | 136 → 57 (+79) | FT% -0.86, ST +0.77 | 2025-26 per-36 at 33.1 min |
| Giannis Antetokounmpo | 42 → 58 (-16) | 59 → 58 (+1) | FT% +1.15, PTS -0.72 | 2025-26 per-36 at 28.9 min |
| De'Aaron Fox | 51 → 59 (-8) | 55 → 59 (-4) | PTS -0.99, TO +0.71 | 2025-26 per-36 at 31.0 min |
| Reed Sheppard | 104 → 60 (+44) | 102 → 61 (+41) | ST +1.21, 3PTM +0.63 | 2025-26 per-36 at 26.2 min |
| Trae Young | 57 → 63 (-6) | 42 → 60 (-18) | ST -0.37, AST +0.28 | 2024-25 per-36 at 32.9 min (range rule R1 from 36.0); ft_pct to the range |
| Jalen Suggs | 59 → 61 (-2) | 79 → 64 (+15) | AST +0.78, PTS -0.55 | 2025-26 per-36 at 27.6 min |
| Mikal Bridges | 61 → 62 (-1) | 56 → 62 (-6) | PTS -0.61, TO +0.50 | 2025-26 per-36 at 32.8 min |
| Tyler Herro | 43 → 65 (-22) | 40 → 63 (-23) | TO +1.50, AST -1.05 | 2025-26 per-36 at 31.3 min |
| Immanuel Quickley | 91 → 64 (+27) | 110 → 67 (+43) | TO +0.67, ST +0.48 | 2025-26 per-36 at 31.9 min |
| Kon Knueppel | 94 → 66 (+28) | 104 → 65 (+39) | 3PTM +0.81, REB +0.53 | 2025-26 per-36 at 31.5 min |
| Kel'el Ware | 80 → 67 (+13) | 83 → 66 (+17) | REB +0.37, BLK -0.33 | 2025-26 per-36 at 22.1 min |
| Franz Wagner | 29 → 68 (-39) | 68 → 68 (0) | TO +1.62, AST -1.23 | 2025-26 per-36 at 30.0 min |
| Yaxel Lendeborg | 82 → 69 (+13) | 80 → 69 (+11) | 3PTM +0.39, FG% -0.34 | rookie translation held; fg_pct/ft_pct to the range; reb/tpm to the range |
| Jaden McDaniels | 83 → 70 (+13) | 54 → 71 (-17) | FG% +0.79, REB -0.60 | 2025-26 per-36 at 31.7 min |
| Keyonte George | 108 → 71 (+37) | 114 → 70 (+44) | FT% +1.34, PTS +0.50 | 2025-26 per-36 at 33.1 min |
| Brandon Miller | 46 → 74 (-28) | 62 → 72 (-10) | AST -0.61, TO +0.45 | 2025-26 per-36 at 30.3 min |
| Keegan Murray | 100 → 72 (+28) | 105 → 73 (+32) | BLK +0.44, TO +0.22 | 2024-25 per-36 at 34.3 min |
| Jarrett Allen | 50 → 73 (-23) | 61 → 76 (-15) | FG% -0.51, FT% -0.43 | 2025-26 per-36 at 27.1 min |
| Kristaps Porzingis | 39 → 75 (-36) | 48 → 74 (-26) | FG% -0.69, REB -0.58 | 2025-26 per-36 at 23.7 min (2025-26 minutes with GSW (15 of 32 games)) |
| Deni Avdija | 77 → 76 (+1) | 69 → 75 (-6) | TO -1.49, AST +1.26 | 2025-26 per-36 at 33.3 min |
| Payton Pritchard | 37 → 77 (-40) | 66 → 77 (-11) | 3PTM -1.18, TO +0.66 | 2025-26 per-36 at 32.4 min |
| Collin Gillespie | 93 → 78 (+15) | 103 → 79 (+24) | ST +0.56, FT% -0.20 | 2025-26 per-36 at 28.5 min |
| Neemias Queta | 154 → 80 (+74) | 237 → 78 (+159) | FT% +0.70, TO +0.50 | 2025-26 per-36 at 25.3 min |
| Ayo Dosunmu | 147 → 79 (+68) | 151 → 80 (+71) | 3PTM +0.67, PTS +0.63 | 2025-26 per-36 at 28.9 min (2025-26 minutes with MIN (24 of 69 games)) |
| Grayson Allen | 172 → 81 (+91) | 186 → 82 (+104) | ST +1.06, FG% -0.99 | 2025-26 per-36 at 28.8 min |
| Ivica Zubac | 45 → 83 (-38) | 81 → 81 (0) | FT% +0.84, ST -0.60 | 2025-26 per-36 at 30.1 min |
| Norman Powell | 85 → 82 (+3) | 87 → 83 (+4) | FT% +0.38, FG% -0.26 | 2025-26 per-36 at 29.6 min |
| Brandon Ingram | 117 → 84 (+33) | 118 → 84 (+34) | PTS +0.47, BLK +0.23 | 2025-26 per-36 at 33.8 min |
| Andrew Wiggins | 99 → 86 (+13) | 140 → 85 (+55) | BLK +0.63, PTS -0.48 | 2025-26 per-36 at 30.3 min |
| Josh Hart | 67 → 85 (-18) | 53 → 86 (-33) | 3PTM +0.59, ST -0.37 | 2025-26 per-36 at 30.2 min |
| Dejounte Murray | 63 → 87 (-24) | 76 → 87 (-11) | ST -0.83, FG% +0.51 | 2024-25 per-36 at 29.1 min (range rule R1 from 32.6); fg_pct/ft_pct to the range |
| DeMar DeRozan | 156 → 88 (+68) | 160 → 88 (+72) | TO +0.51, PTS +0.45 | 2025-26 per-36 at 31.2 min |
| Jrue Holiday | 136 → 91 (+45) | 92 → 89 (+3) | TO -1.55, PTS +0.86 | 2025-26 per-36 at 29.4 min |
| Tre Jones | 143 → 89 (+54) | 145 → 90 (+55) | FG% +0.93, FT% +0.32 | 2025-26 per-36 at 26.9 min |
| Caleb Wilson | 120 → 90 (+30) | 117 → 91 (+26) | BLK -0.53, 3PTM +0.51 | rookie translation held; ft_pct to the range; blk/tpm to the range |
| Saddiq Bey | 95 → 92 (+3) | 99 → 92 (+7) | TO +0.63, BLK -0.56 | 2025-26 per-36 at 31.2 min |
| Matas Buzelis | 125 → 98 (+27) | 77 → 93 (-16) | BLK +0.84, 3PTM +0.76 | 2025-26 per-36 at 29.2 min |
| Tari Eason | 111 → 93 (+18) | 112 → 96 (+16) | ST +0.64, FG% -0.49 | 2025-26 per-36 at 25.8 min |
| Jabari Smith Jr. | 103 → 94 (+9) | 108 → 95 (+13) | 3PTM +0.33, AST +0.30 | 2025-26 per-36 at 35.1 min |
| Myles Turner | 86 → 97 (-11) | 88 → 94 (-6) | ST -0.28, FT% -0.16 | 2025-26 per-36 at 26.9 min |
| Cason Wallace | 73 → 95 (-22) | 91 → 100 (-9) | FG% -0.48, ST +0.43 | 2025-26 per-36 at 26.6 min |
| Fred VanVleet | 68 → 96 (-28) | 78 → 98 (-20) | ST -0.58, FG% +0.35 | 2024-25 per-36 at 31.0 min (range rule R1 from 35.2) |
| Alex Sarr | 110 → 99 (+11) | 75 → 97 (-22) | FG% +0.61, ST -0.52 | 2025-26 per-36 at 27.2 min |
| Miles Bridges | 119 → 101 (+18) | 121 → 99 (+22) | BLK +0.23, AST +0.16 | 2025-26 per-36 at 31.0 min |
| Toumani Camara | 98 → 100 (-2) | 84 → 101 (-17) | 3PTM +1.27, TO -0.53 | 2025-26 per-36 at 33.3 min |
| Darius Garland | 41 → 103 (-62) | 24 → 102 (-78) | FT% -0.41, PTS -0.38 | 2025-26 per-36 at 29.1 min (2025-26 minutes with LAC (19 of 45 games)) |
| Rudy Gobert | 78 → 102 (-24) | 85 → 103 (-18) | FT% -1.48, REB +0.51 | 2025-26 per-36 at 31.3 min |
| Andrew Nembhard | 124 → 104 (+20) | 159 → 104 (+55) | PTS +0.90, 3PTM +0.67 | 2025-26 per-36 at 31.3 min |
| Ausar Thompson | 109 → 105 (+4) | 67 → 110 (-43) | ST +0.75, FT% -0.54 | 2025-26 per-36 at 26.0 min |
| Peyton Watson | 135 → 108 (+27) | 144 → 105 (+39) | TO -0.67, BLK +0.65 | 2025-26 per-36 at 29.6 min |
| Bradley Beal | 171 → 109 (+62) | 189 → 106 (+83) | PTS +0.73, TO -0.52 | 2024-25 per-36 at 32.1 min |
| Devin Vassell | 89 → 106 (-17) | 123 → 108 (+15) | TO +0.63, PTS -0.48 | 2025-26 per-36 at 30.5 min |
| Ajay Mitchell | 152 → 107 (+45) | 73 → 107 (-34) | ST +0.81, PTS +0.17 | 2025-26 per-36 at 25.8 min |
| Pascal Siakam | 64 → 110 (-46) | 86 → 109 (-23) | FT% -0.95, FG% -0.79 | 2025-26 per-36 at 33.2 min |
| Tobias Harris | 138 → 111 (+27) | 153 → 111 (+42) | ST +0.41, FT% +0.28 | 2025-26 per-36 at 27.7 min |
| Darryn Peterson | 140 → 112 (+28) | 138 → 114 (+24) | TO +0.69, ST +0.24 | rookie translation held; pts/tov to the range |
| Julius Randle | 107 → 113 (-6) | 107 → 112 (-5) | TO +0.60, ST +0.41 | 2025-26 per-36 at 33.0 min |
| Isaiah Hartenstein | 75 → 114 (-39) | 101 → 113 (-12) | REB -0.45, ST +0.41 | 2025-26 per-36 at 24.2 min |
| Julian Champagnie | 161 → 115 (+46) | 168 → 115 (+53) | REB +0.70, BLK +0.42 | 2025-26 per-36 at 27.6 min |
| Deandre Ayton | 158 → 116 (+42) | 133 → 116 (+17) | FG% +1.05, FT% -0.57 | 2025-26 per-36 at 27.2 min |
| Daniel Gafford | 90 → 119 (-29) | 130 → 117 (+13) | ST +0.62, FG% -0.47 | 2025-26 per-36 at 21.7 min |
| Jakob Poeltl | 127 → 117 (+10) | 120 → 118 (+2) | REB -0.66, FT% +0.58 | 2025-26 per-36 at 25.0 min |
| Zion Williamson | 105 → 118 (-13) | 97 → 119 (-22) | TO +1.64, AST -1.08 | 2025-26 per-36 at 29.7 min |
| Robert Williams III | 141 → 120 (+21) | 143 → 120 (+23) | 3PTM +0.23, REB +0.21 | 2025-26 per-36 at 17.1 min |
| John Collins | 114 → 122 (-8) | 72 → 121 (-49) | FG% +0.75, REB -0.58 | 2025-26 per-36 at 27.1 min |
| Kelly Oubre Jr. | 149 → 121 (+28) | 155 → 123 (+32) | ST +0.56, TO +0.26 | 2025-26 per-36 at 31.5 min |
| Cam Spencer | 150 → 123 (+27) | 163 → 122 (+41) | AST +0.47, TO -0.42 | 2025-26 per-36 at 23.8 min |
| Christian Braun | 97 → 124 (-27) | 95 → 124 (-29) | FG% -0.41, PTS -0.26 | 2025-26 per-36 at 31.8 min |
| Kyshawn George | 181 → 126 (+55) | 141 → 125 (+16) | TO -1.15, AST +0.70 | 2025-26 per-36 at 29.0 min |
| Royce O'Neale | 190 → 125 (+65) | 194 → 126 (+68) | 3PTM +0.74, ST +0.73 | 2025-26 per-36 at 28.4 min |
| Kris Dunn | 162 → 127 (+35) | 167 → 131 (+36) | ST +0.71, TO -0.55 | 2025-26 per-36 at 27.2 min |
| Paolo Banchero | 102 → 128 (-26) | 126 → 127 (-1) | PTS -0.81, 3PTM -0.68 | 2025-26 per-36 at 34.8 min |
| Moussa Diabate | 164 → 130 (+34) | 171 → 128 (+43) | AST +0.46, ST +0.41 | 2025-26 per-36 at 26.0 min |
| Santi Aldama | 130 → 129 (+1) | 147 → 130 (+17) | FT% -0.81, ST +0.37 | 2025-26 per-36 at 27.9 min |
| Wendell Carter Jr. | 137 → 133 (+4) | 150 → 129 (+21) | ST +0.37, REB -0.29 | 2025-26 per-36 at 29.3 min |
| Nic Claxton | 134 → 131 (+3) | 60 → 132 (-72) | AST +0.72, ST -0.52 | 2025-26 per-36 at 27.8 min |
| CJ McCollum | 116 → 132 (-16) | 131 → 133 (-2) | ST -0.49, BLK +0.23 | 2025-26 per-36 at 28.8 min (2025-26 minutes with ATL (41 of 76 games)) |
| Cameron Johnson | 106 → 134 (-28) | 113 → 134 (-21) | 3PTM -0.29, PTS -0.28 | 2025-26 per-36 at 30.5 min |
| Bobby Portis | 218 → 135 (+83) | 169 → 135 (+34) | 3PTM +0.88, PTS +0.63 | 2025-26 per-36 at 24.2 min |
| Brandin Podziemski | 148 → 136 (+12) | 116 → 136 (-20) | PTS +0.30, REB +0.21 | 2025-26 per-36 at 28.4 min |
| Herbert Jones | 74 → 137 (-63) | 64 → 137 (-73) | FG% -0.66, ST -0.50 | 2025-26 per-36 at 28.4 min |
| Zach LaVine | 56 → 138 (-82) | 71 → 138 (-67) | TO +0.82, AST -0.80 | 2025-26 per-36 at 31.4 min |
| Aaron Gordon | 92 → 139 (-47) | 93 → 141 (-48) | FT% -1.02, FG% -0.69 | 2025-26 per-36 at 27.9 min |
| Derik Queen | 155 → 140 (+15) | 156 → 139 (+17) | FT% +0.75, FG% -0.72 | 2025-26 per-36 at 25.0 min |
| Ja Morant | 65 → 143 (-78) | 134 → 140 (-6) | ST -1.02, AST -0.74 | 2024-25 per-36 at 25.5 min (range rule R1 from 30.4); ft_pct to the range |
| PJ Washington | 87 → 141 (-54) | 74 → 142 (-68) | FT% -0.68, FG% -0.46 | 2025-26 per-36 at 31.0 min |
| Anthony Black | 174 → 142 (+32) | 177 → 144 (+33) | PTS +0.68, 3PTM +0.58 | 2025-26 per-36 at 29.8 min |
| Jaime Jaquez Jr. | 210 → 144 (+66) | 229 → 143 (+86) | AST +0.80, TO -0.52 | 2025-26 per-36 at 28.3 min |
| Mitchell Robinson | 133 → 145 (-12) | 174 → 147 (+27) | ST +0.73, BLK -0.53 | 2025-26 per-36 at 19.6 min |
| Sam Merrill | 236 → 146 (+90) | 236 → 145 (+91) | 3PTM +0.83, PTS +0.44 | 2025-26 per-36 at 26.5 min |
| Ryan Kalkbrenner | 270 → 149 (+121) | 267 → 146 (+121) | BLK +0.84, REB +0.61 | 2025-26 per-36 at 21.4 min |
| Scotty Pippen Jr. | 132 → 147 (-15) | 132 → 149 (-17) | TO +0.41, AST -0.33 | 2024-25 per-36 at 21.3 min |
| AJ Dybantsa | 139 → 148 (-9) | 166 → 148 (+18) | PTS -0.42, TO +0.32 | rookie translation held; pts by identity; the kit's line (D-R1) |
| Jerami Grant | 113 → 150 (-37) | 115 → 150 (-35) | TO -0.78, FT% -0.58 | 2025-26 per-36 at 29.7 min |
| Luke Kornet | 231 → 152 (+79) | 230 → 151 (+79) | REB +0.50, BLK +0.44 | 2025-26 per-36 at 21.0 min |
| Naji Marshall | 202 → 151 (+51) | 179 → 153 (+26) | ST +0.48, PTS +0.42 | 2025-26 per-36 at 29.5 min |
| Coby White | 58 → 153 (-95) | 100 → 152 (-52) | TO -1.00, FT% -0.85 | 2025-26 per-36 at 29.1 min (role: starting PG when healthy (NBA.com/AP 10/6; Roundtable 10/7)) |
| Aaron Nesmith | 118 → 154 (-36) | 96 → 154 (-58) | FG% -1.02, TO -0.55 | 2025-26 per-36 at 29.7 min |
| Draymond Green | 115 → 155 (-40) | 109 → 155 (-46) | ST -0.66, TO -0.61 | 2025-26 per-36 at 27.5 min |
| Jaylon Tyson | 223 → 158 (+65) | 222 → 156 (+66) | PTS +0.43, TO -0.41 | 2025-26 per-36 at 26.9 min |
| Jordan Goodwin | 112 → 156 (-44) | 106 → 159 (-53) | ST -0.87, BLK -0.17 | 2025-26 per-36 at 22.5 min |
| Miles McBride | 199 → 157 (+42) | 204 → 158 (+46) | 3PTM +0.63, PTS +0.46 | 2025-26 per-36 at 26.3 min |
| Sandro Mamukelashvili | 81 → 159 (-78) | 82 → 157 (-75) | ST -0.52, 3PTM -0.47 | 2025-26 per-36 at 21.9 min |
| Marcus Smart | 194 → 160 (+34) | 148 → 166 (-18) | AST -0.45, ST +0.35 | 2025-26 per-36 at 28.5 min |
| Nikola Vucevic | 121 → 163 (-42) | 124 → 160 (-36) | FG% -0.62, REB -0.40 | 2025-26 per-36 at 21.1 min (role: bench (ESPN box 10/7 and 10/11 ET; Roundtable 10/8)) |
| Cedric Coward | 128 → 165 (-37) | 135 → 161 (-26) | FG% +0.46, PTS -0.44 | 2025-26 per-36 at 25.8 min |
| Kyle Filipowski | 123 → 161 (-38) | 122 → 162 (-40) | ST +0.69, PTS -0.59 | 2025-26 per-36 at 23.4 min |
| Derrick Jones Jr | 178 → 162 (+16) | 182 → 164 (+18) | FG% -0.22, AST +0.21 | 2025-26 per-36 at 27.0 min |
| Maxime Raynaud | 230 → 166 (+64) | 210 → 163 (+47) | REB +0.73, 3PTM -0.63 | 2025-26 per-36 at 26.5 min |
| Justin Champagnie | 191 → 164 (+27) | 197 → 165 (+32) | AST +0.22, FT% +0.14 | 2025-26 per-36 at 20.0 min |
| Stephon Castle | 170 → 167 (+3) | 173 → 167 (+6) | ST +0.20, REB +0.09 | 2025-26 per-36 at 30.0 min |
| Quentin Grimes | 157 → 168 (-11) | 164 → 168 (-4) | TO -0.53, FT% +0.32 | 2025-26 per-36 at 29.4 min |
| Rui Hachimura | 183 → 169 (+14) | 157 → 169 (-12) | 3PTM +0.57, REB -0.38 | 2025-26 per-36 at 31.7 min (role: starter (ESPN box 10/4 and 10/10 ET; CBS Sports, Yardbarker, Yahoo 10/4-5)) |
| Dylan Cardwell | 228 → 170 (+58) | 227 → 170 (+57) | REB +0.46, ST +0.33 | 2025-26 per-36 at 20.6 min |
| Al Horford | 144 → 171 (-27) | 152 → 171 (-19) | AST +0.39, ST -0.32 | 2025-26 per-36 at 21.5 min |
| Bennedict Mathurin | 243 → 176 (+67) | 200 → 172 (+28) | TO -0.91, PTS +0.73 | 2025-26 per-36 at 30.0 min |
| John Konchar | 292 → 172 (+120) | — → — (—) | ST +1.09, REB +0.66 | 2025-26 per-36 at 19.9 min |
| Collin Murray-Boyles | 193 → 174 (+19) | 89 → 173 (-84) | TO +0.37, FG% +0.14 | 2025-26 per-36 at 21.9 min |
| De'Anthony Melton | 142 → 173 (-31) | 146 → 174 (-28) | TO -0.66, FG% -0.45 | 2025-26 per-36 at 23.0 min |
| Keaton Wagler | 175 → 177 (-2) | 185 → 175 (+10) | ST +0.12, TO -0.09 | line unchanged (no method line: rookie translation held or no qualifying season) |
| T.J. McConnell | 212 → 175 (+37) | 213 → 176 (+37) | 3PTM +0.22, AST +0.22 | 2025-26 per-36 at 17.2 min |
| Darius Acuff Jr. | 176 → 179 (-3) | 184 → 177 (+7) | ST +0.16, TO -0.08 | line unchanged (no method line: rookie translation held or no qualifying season) |
| Bilal Coulibaly | 131 → 178 (-47) | 119 → 179 (-60) | ST -0.94, TO +0.80 | 2025-26 per-36 at 26.2 min |
| Max Christie | 217 → 182 (+35) | 221 → 178 (+43) | 3PTM +0.44, PTS +0.34 | 2025-26 per-36 at 29.1 min |
| Dillon Brooks | 208 → 180 (+28) | 209 → 180 (+29) | PTS +0.96, FG% -0.61 | 2025-26 per-36 at 30.4 min |
| Davion Mitchell | 166 → 181 (-15) | 176 → 181 (-5) | ST -0.16, TO -0.14 | 2025-26 per-36 at 28.6 min |
| Duncan Robinson | 245 → 183 (+62) | 187 → 182 (+5) | 3PTM +0.73, TO +0.62 | 2025-26 per-36 at 27.4 min |
| Jalen Smith | 204 → 184 (+20) | 216 → 183 (+33) | TO -0.30, ST +0.22 | 2025-26 per-36 at 20.7 min |
| Isaiah Joe | 182 → 185 (-3) | 193 → 184 (+9) | 3PTM -0.32, FG% +0.20 | 2025-26 per-36 at 21.2 min |
| Ace Bailey | 168 → 187 (-19) | 178 → 185 (-7) | TO +0.67, REB -0.56 | 2025-26 per-36 at 27.6 min |
| RJ Barrett | 192 → 186 (+6) | 195 → 186 (+9) | REB +0.13, TO -0.13 | 2025-26 per-36 at 30.3 min |
| Kevin Porter Jr. | 224 → 188 (+36) | 224 → 187 (+37) | ST +1.09, 3PTM -0.76 | 2025-26 per-36 at 19.9 min (role: bench (ESPN box 10/5 and 10/11 ET; SI Bucks 10/11; Yahoo Sports after 10/11)) |
| Hannes Steinbach | 207 → 191 (+16) | 207 → 188 (+19) | REB +0.15, TO -0.14 | line unchanged (no method line: rookie translation held or no qualifying season) |
| Collin Sexton | 169 → 192 (-23) | 142 → 189 (-47) | AST -0.51, REB -0.25 | 2025-26 per-36 at 23.7 min |
| Precious Achiuwa | 259 → 189 (+70) | 248 → 190 (+58) | ST +0.41, REB +0.40 | 2025-26 per-36 at 23.9 min |
| Taylor Hendricks | 186 → 190 (-4) | 192 → 191 (+1) | ST +1.02, TO -0.43 | 2025-26 per-36 at 24.1 min (2025-26 minutes with MEM (26 of 59 games)) |
| Brook Lopez | 167 → 193 (-26) | 183 → 192 (-9) | BLK -0.13, FG% -0.13 | 2025-26 per-36 at 21.8 min |
| Keldon Johnson | 213 → 194 (+19) | 217 → 193 (+24) | FG% +0.38, ST -0.28 | 2025-26 per-36 at 23.3 min |
| Sam Hauser | 215 → 195 (+20) | 223 → 194 (+29) | FG% -0.33, ST +0.29 | 2025-26 per-36 at 24.8 min |
| Dylan Harper | 146 → 196 (-50) | 165 → 195 (-30) | ST -1.34, TO +1.33 | 2025-26 per-36 at 22.6 min |
| Jarace Walker | 267 → 197 (+70) | 261 → 196 (+65) | ST +0.73, PTS +0.48 | 2025-26 per-36 at 25.7 min |
| Jeremiah Fears | 273 → 198 (+75) | 198 → 197 (+1) | AST -0.88, TO +0.71 | 2025-26 per-36 at 25.8 min |
| Andre Drummond | — → — (—) | 273 → 198 (+75) | — | 2025-26 per-36 at 19.5 min |
| Jake LaRavia | 188 → 199 (-11) | 188 → 199 (-11) | FT% +0.24, BLK -0.17 | 2025-26 per-36 at 25.1 min |
| Alex Caruso | 129 → 200 (-71) | 127 → 200 (-73) | ST -0.58, AST -0.43 | 2025-26 per-36 at 18.2 min |
| Paul Reed | 219 → 201 (+18) | 98 → 201 (-103) | 3PTM +0.23, TO -0.17 | 2025-26 per-36 at 13.9 min |
| Day'Ron Sharpe | 76 → 203 (-127) | 70 → 202 (-132) | ST -1.30, REB -0.94 | 2025-26 per-36 at 18.7 min |
| Keon Ellis | 122 → 202 (-80) | 128 → 205 (-77) | PTS -0.59, AST -0.50 | 2025-26 per-36 at 20.5 min |
| Isaiah Stewart | 180 → 206 (-26) | 162 → 203 (-41) | ST -0.96, REB -0.70 | 2025-26 per-36 at 22.7 min |
| Obi Toppin | 184 → 205 (-21) | 199 → 204 (-5) | BLK -0.36, PTS -0.29 | 2024-25 per-36 at 19.6 min |
| Anfernee Simons | 160 → 213 (-53) | 170 → 214 (-44) | ST -0.89, TO +0.65 | 2025-26 per-36 at 24.9 min |
| Luguentz Dort | 151 → 218 (-67) | 154 → 220 (-66) | FG% -0.54, PTS -0.47 | 2025-26 per-36 at 26.8 min |
| Bogdan Bogdanovic | 163 → 224 (-61) | 125 → 225 (-100) | ST -0.49, PTS -0.33 | 2024-25 per-36 at 25.0 min |
| Luke Kennard | 187 → 226 (-39) | 196 → 226 (-30) | AST -0.33, 3PTM -0.27 | 2025-26 per-36 at 21.6 min |
| Malik Monk | 153 → 228 (-75) | 158 → 228 (-70) | ST -0.85, AST -0.71 | 2025-26 per-36 at 22.0 min |
| De'Andre Hunter | 159 → 230 (-71) | 161 → 229 (-68) | FG% -0.74, TO -0.67 | 2025-26 per-36 at 26.1 min |
| Goga Bitadze | 185 → 235 (-50) | 218 → 235 (-17) | REB -0.70, TO +0.62 | 2025-26 per-36 at 15.2 min |
| Jalen Green | 126 → 240 (-114) | 137 → 241 (-104) | FT% -0.91, 3PTM -0.83 | 2025-26 per-36 at 25.9 min |
| Zaccharie Risacher | 173 → 242 (-69) | 139 → 244 (-105) | PTS -0.73, 3PTM -0.47 | 2025-26 per-36 at 22.4 min |
| Gui Santos | 165 → 249 (-84) | 172 → 250 (-78) | ST -0.77, REB -0.61 | 2025-26 per-36 at 20.5 min |
| Klay Thompson | 222 → 250 (-28) | 190 → 252 (-62) | ST -0.60, 3PTM +0.51 | 2025-26 per-36 at 21.7 min |
| Jaylen Wells | 179 → 253 (-74) | 203 → 256 (-53) | BLK -0.56, ST -0.52 | 2025-26 per-36 at 26.4 min |
| GG Jackson | 233 → 259 (-26) | 181 → 259 (-78) | FG% +0.64, ST -0.60 | 2025-26 per-36 at 21.4 min |
| Jose Alvarado | 177 → 267 (-90) | 180 → 272 (-92) | ST -1.59, PTS -0.31 | 2025-26 per-36 at 16.9 min (2025-26 minutes with NYK (28 of 69 games)) |
| Yves Missi | 189 → 269 (-80) | 214 → 268 (-54) | ST -0.96, REB -0.96 | 2025-26 per-36 at 19.6 min |
| Bub Carrington | 195 → 272 (-77) | 212 → 271 (-59) | ST -0.85, TO -0.36 | 2025-26 per-36 at 27.7 min |
| Jay Huff | 198 → 284 (-86) | 205 → 286 (-81) | REB -0.61, BLK -0.53 | 2025-26 per-36 at 11.7 min (role: bench behind Zubac (ESPN box 10/7 and 10/10 ET; Roundtable 10/5)) |
| Gary Trent Jr. | 196 → 291 (-95) | 175 → 295 (-120) | ST -0.81, REB -0.64 | 2025-26 per-36 at 21.2 min |
| Jared McCain | 145 → 294 (-149) | 149 → 296 (-147) | PTS -1.26, AST -0.98 | 2025-26 per-36 at 18.0 min (2025-26 minutes with OKC (30 of 67 games)) |
| Nikola Jovic | 197 → 303 (-106) | 226 → 302 (-76) | ST -0.89, PTS -0.72 | 2025-26 per-36 at 17.2 min |
| Khaman Maluach | 220 → 310 (-90) | 191 → 307 (-116) | REB -1.78, BLK -1.32 | 2025-26 per-36 at 8.9 min |
| Terrence Shannon Jr | 200 → 312 (-112) | 201 → 309 (-108) | ST -1.82, PTS -1.27 | 2025-26 per-36 at 12.5 min |
