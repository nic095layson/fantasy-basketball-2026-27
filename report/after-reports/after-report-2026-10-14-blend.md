# After-report — 2026-10-14 (night of 10/13): the owner's calls (Version 66), an audit of the 200 projection lines, and the six-way blend (Version 67)

**Owner requests (verbatim).** First, the calls: "Chet - untag / Tyrese - healthy, untag / Kawhi - keep at .85 (But I am very bullish on him) / Damian - keep at .85 / Kyrie - .85 / Davis - .85 / leave the other 3 as default / Kessler - healthy / Lendeborg, I may take with my 7th or 8th pick, I'm very bullish on him. Knowing my draft mates, I don't think he survives past 105", with "New 0.85 tier for these four", "Now, tonight" and "If you believe .88 is better than .85, please use that." Then, while that was building: "Now, once that is complute. Run a thorough and expertise audit of the 200 player projections. Are these realistic and accurate, or do you have 95% confidence in your kit's projections, based on the outside data that you have aggregated. Run a Gauntlet and Council debate to tighten up and dial in all the numbers so that we have a sound and realistic projection. Provide after report in plain language"

**What was analyzed and changed.** Kit `main` 29d3d26 and deck `main` 6064cc2 (Version 65) as the start. Version 66 (deck PR #114, main c1065c5) carries the calls. Version 67 (deck PR #115, main 43ca6bf; this kit PR) carries the blend. The five outside projections, all already pinned in `report/market/`: Yahoo `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, RotoBaller `rotoballer-2026-10-13.csv`, FantasyPros `fantasypros-2026-10-13.csv`, the Basketball Monster cards `cards-2026-10-13.csv`.

**Method.** The Gauntlet sequence (plan gate → work → adversarial pass → this report), with a Council on the method. The plan went to the owner before any line moved, with assumptions A1–A5 and criteria C1–C9 (§7). Tools in `report/blend/tools/`: `audit_measure.py` (the audit, read-only), `blend_lines.py` (the blended lines, writes nothing), `blend_apply.py` (writes both planes with assertions), `board_diff.py`, `card_compare.py`. Every one that produces a record was run twice with identical output.

Pull window: 2026-10-14 → 2026-10-14 (no roster pull beyond Version 66's verification; the stat lines of the 10/13 outside projections, already pinned).

## The short answer, in plain language

**Were our numbers realistic?** Yes. I compared our 200 lines with the five outside projection sets, and our lines turned out to be the closest of the six to the group. Each source's average distance from the median of the other five, in category-spread units: ours 0.134, the other five 0.135 to 0.141. On average we ran a little high on points (+0.20 a game against the outside median) and matched the group everywhere else.

**Could you have 95% confidence in them?** No, and no projection can give you that. Two facts settle it.
- *The experts disagree with each other.* I asked how often each source's number lands between the highest and lowest of four others. RotoBaller, the best of them, did so 77.2% of the time, Hashtag 68.5%, and our lines 72.1%.
- *The season itself is noisy.* In last season's test our pre-season points line missed a player's real average by 2.78 points a game on average (`after-report-2026-10-09-market.md`), and that was one of the better methods tested.

So no single source deserves 95% confidence, ours included.

**What we did about it (Council 4–1).** The most reliable way to get a sounder number is to average several good forecasts. Every line that has at least three outside projections — 241 on the kit, 238 of them on the page — is now the plain average of our line and the outside lines, category by category, with ours counting as one vote of up to six. Games, minutes, injury tags (including tonight's calls) and teams did not change.

- *Why averaging helps.* The average of several forecasts can never do worse than those forecasts do on average; that is arithmetic. It usually beats most of them, because their misses partly cancel (INFERENCE: the general forecasting result, not measured on these six). Last season's test showed the same on our own data: a half-and-half blend of two forecasts beat each of them in all nine categories.
- *What it costs.* The blend pulls our lines toward the market. Where we were higher than everyone on a player, he drops.

**What changed on your draft board.**
- The page's top 12 is the same twelve names, slightly reordered.
- The middle rounds moved more. In the page's top 100, 85 players changed rank, by 8.41 places on average; 8 moved more than 20 places. In each of those, our line had sat at or past the edge of the outside range in several categories.
- The 🎯 (the card's single pick) changes at **152 of the 364** turns where you picked in the 28 practice drafts I replayed. That is a big change in what the card will tell you today, so read §5 before the draft.

**Three names you asked about.**
- *Kawhi* stays #5 on the page.
- *Lendeborg* falls from value #70 to #102: the outside average sits below our line in 8 of his 9 categories. Your plan to take him in round 7 or 8 is still yours to make; the card simply won't point at him there (decision D-1014-1).
- *Kel'el Ware*, the 🎯 in 45 of your practice turns before, falls from #27 to #58. All five outside sources project him for fewer points, rebounds and threes than we did.

**How confident I am now.** In the system (arithmetic, plumbing, the page) as before: every gate and test passed on Version 67, and the 🎯 the page shows is the engine's own. In the numbers, more than last night: they now sit inside the professional range in 99.7% of cells, and the main thing the audit worried about — lines we alone believed — is gone. That number is by construction, not proof of accuracy.

One weak spot stays open, and nobody can close it before tonight. Whether equal weights are better than, say, trusting our line a little more could only be settled with last season's outside projections, and those are not on file. I did not search for them tonight (time); the choice is on the decision sheet.

## 1. Roster changes

No placement or team changed on either plane, and no row was added or dropped. Two passes changed the pool tonight.

- **Version 66 (availability tags only).**
  - Tyrese Haliburton and Walker Kessler are untagged and healthy, by your call.
  - Kawhi Leonard, Anthony Davis, Kyrie Irving and Damian Lillard sit on a new lighter risk tier. It counts ×0.85 on value instead of ×0.78, and 0.79 instead of 0.75 in the weekly model, in all three copies of the engine.
  - Holmgren stays untagged. Black, Merrill and Hartenstein keep their defaults.
  - On your ".88" question I kept 0.85. The outside projections put these four at 0.842–0.870 of a healthy season's games.
  - Checks: the four new card tests failed before the code and passed after (103 of 103). Build: 7 gates PASS. Chain: parity EXACT (455 owner turns across 35 committed states), test_card 103, test_draft 65, test_gates 54, full DOM 145/0, repeat-name 28 of 28 mocks replayed; 9 FLAGGED.
  - Published as Version 66 (1791957366-babb), byte-verified (page 7d4bab2d61bf).
- **Version 67 (stat lines only):** the blend, §3.

## 2. The audit: how our 200 lines compared with the five outside projections

EVIDENCE: `blend/out/audit_v66_lines.txt` (our lines before the blend, on the board's 200), `audit_v67_lines_new200.txt` (the blended lines, on the new board's 200), both by `audit_measure.py` with two identical runs each. Outside lines per player in the top 200 before the blend: {0: 1, 1: 1, 2: 7, 3: 8, 4: 26, 5: 157} (number of outside sources: players). The 191 with three or more are the ones the tables below read.

**Category by category.** "Lean" is our line minus the median of the outside sources, averaged over the 191 (+ means we were higher). "Outside every source" counts players whose number sat above all five or below all five.

| category | lean before | lean after | outside every source, before | after |
|---|---|---|---|---|
| points | +0.20 | +0.01 | 56 of 191 (29%) | 0 of 191 (0%) |
| rebounds | +0.03 | -0.00 | 42 of 191 (22%) | 0 of 191 (0%) |
| assists | +0.07 | +0.00 | 63 of 191 (33%) | 1 of 191 (1%) |
| steals | -0.00 | +0.00 | 25 of 191 (13%) | 0 of 191 (0%) |
| blocks | +0.01 | +0.00 | 18 of 191 (9%) | 1 of 191 (1%) |
| threes | +0.03 | +0.00 | 45 of 191 (24%) | 1 of 191 (1%) |
| turnovers | +0.03 | +0.01 | 52 of 191 (27%) | 0 of 191 (0%) |
| FG% | -0.0003 | +0.0001 | 50 of 191 (26%) | 3 of 191 (2%) |
| FT% | -0.0028 | -0.0005 | 76 of 191 (40%) | 0 of 191 (0%) |

**Each forecaster against the others** (the 157 players all five sources cover). "Inside" is how often a source's number lands between the highest and lowest of four others. "Distance" is the average gap to the median of the other five, in units of the category's spread across the 200.

| forecaster | inside, before | distance, before | inside, after | distance, after |
|---|---|---|---|---|
| RotoBaller | 77.2% | 0.135 | 71.2% | 0.127 |
| FantasyPros | 73.9% | 0.137 | 70.6% | 0.126 |
| Yahoo | 73.0% | 0.141 | 66.0% | 0.139 |
| **ours** | 72.1% | 0.134 | 98.3% | 0.046 |
| BBM cards | 71.9% | 0.140 | 65.6% | 0.132 |
| Hashtag | 68.5% | 0.137 | 63.2% | 0.131 |

Reading:
- **EVIDENCE.** Before the blend our lines were the closest of the six to the rest and sat in the middle of the pack on the "inside" test. No outside source reaches 80% on it.
- **INFERENCE.** "95% confidence" in single numbers isn't on offer from anyone. The useful question is whether our lines were an outlier, and they were not.

After the blend our line is, by construction, close to the middle of the six, which is why its own "after" figures look so much better than anyone else's. That is a property of averaging, not new evidence of accuracy.

## 3. The blend

**The Council (4–1).**
- The Contrarian voted to change nothing, or to cap our line's move at half the gap: our lines were already the closest to the group, so nothing was broken.
- First Principles carried the vote. The average of good forecasts beats them on average whether or not any one of them is broken, and our own 2025-26 test agreed (a half-and-half blend beat both of its parts in 9 of 9 categories, `after-report-2026-10-09-market.md`).
- Equal weights won over 50/50 because the six distances above sit within 0.007 of each other: no forecaster looks more reliable than the rest.
- The Contrarian's vote would flip if last season's outside projections showed equal weights doing worse than our lines alone (D-1014-2).

**The rule as shipped (A1–A5).**
- Each of the nine categories is the plain average of our line and every outside line on file.
- It applies to rows with three or more outside projections: 241 kit rows (238 on the page).
- FGA and FTA scale by one factor per row, so points still add up from the shooting.
- Games, minutes, tags, teams and placements stay. So do the rows with fewer than three outside projections, including Marcus Smart, whose line is on two (RotoBaller, Yahoo).

**One rule changed mid-run, and why.** The plan said that a row needing its shot attempts scaled by more than ±15% would keep its old shooting.
- That rule fired on 23 rows, and they were the widest disagreements. Khaman Maluach is the clearest: our 3.0 points against 5.0–10.4 from the outside sources. Holding his shooting would have blended his rebounds and blocks but not his points, which makes the line contradict itself.
- Minutes feed neither ranking engine; the page has no minutes column. So I changed the rule to always rescale and list the wide factors instead.
- The 23: Bennedict Mathurin (0.817), Egor Demin (1.158), Kevin Porter Jr (1.199), Yves Missi (1.211), Jordan Poole (0.816), Jared McCain (1.382), Khaman Maluach (2.338), Dylan Harper (1.282), Isaiah Collier (0.836), Brice Sensabaugh (0.825), Bub Carrington (0.846), Day'Ron Sharpe (1.245), Morez Johnson Jr. (1.318), Keaton Wagler (0.777), Tre Jones (0.836), Joan Beringer (1.766), Naji Marshall (0.821), Jay Huff (1.325), Noah Clowney (0.811), Jaxson Hayes (0.793), Moses Moody (0.818), Marvin Bagley III (0.837), Bradley Beal (0.789).
- One consequence: for these rows the kit's minutes column no longer matches the shot volume. That column feeds no value.

**What the writer checked** (`blend_apply.py`, record `apply_record_2026-10-14.json`).
- Headers, row counts and every non-stat column are unchanged.
- The two planes agree on every blended row.
- Points add up within 0.25.
- Values are sane.
- No note carries the `];` trap.
- Every blended value equals the six-way mean recomputed inside the writer from the pinned files, and three of the sources agree with the deck's own loader.
- Nothing beyond the nine categories and FGA/FTA moved.
- Result: PASS — 238 deck rows and 241 kit rows; 4026 values (2029 on the kit, 1997 on the deck). A second run changes nothing, and the written files equal the dry run byte for byte. Three planted errors (a wrong mean, a broken points identity, a `];` note) were each caught.

**The named players** (`blend/out/named_players_2026-10-14.txt`, from the lines file):

- Jamal Murray (5 outside): pts 25.1→23.4, reb 4.4→4.2, ast 7.1→6.6, tpm 3.3→2.9, tov 2.3→2.2, fg_pct .475→.476, ft_pct .883→.885
- Collin Gillespie (5 outside): pts 12.7→11.2, reb 4.1→3.7, ast 4.6→4.2, stl 1.3→1.2, tpm 2.9→2.5, tov 1.6→1.3, ft_pct .866→.867
- Bradley Beal (3 outside): pts 16.7→13.2, reb 3.3→2.7, ast 3.7→3.0, stl 1.0→0.8, blk 0.5→0.4, tpm 1.9→1.5, tov 1.9→1.5, ft_pct .809→.803
- Deandre Ayton (3 outside): pts 12.1→10.8, reb 8.0→7.3, ast 0.8→0.9, stl 0.7→0.6, blk 0.9→0.8, tov 1.2→1.1, fg_pct .647→.617, ft_pct .677→.678
- Aaron Nesmith (5 outside): pts 14.1→13.3, ast 1.9→1.7, blk 0.6→0.5, tpm 2.3→2.2, tov 1.4→1.2, fg_pct .427→.456, ft_pct .829→.848
- Sandro Mamukelashvili (3 outside): pts 11.0→12.2, reb 4.9→5.7, ast 1.9→2.0, stl 0.7→0.8, tpm 1.4→1.7, tov 0.8→1.0, fg_pct .513→.505, ft_pct .744→.745
- Marcus Smart: not blended (two outside projections: RotoBaller, Yahoo — under the three-projection rule)

The 12 players aged 34 and older whose lines carried no age decline (last night's audit, T6) now carry the outside sources' view of them:

- Kawhi Leonard (5 outside): pts 24.3→24.4, reb 6.1→5.9, ast 3.6→3.4, ft_pct .881→.877
- Kevin Durant (5 outside): pts 25.8→25.0, ast 4.8→4.3, blk 1.1→1.0, tpm 2.4→2.3, tov 3.2→3.0, fg_pct .515→.521, ft_pct .876→.863
- Kyrie Irving (5 outside): pts 21.3→22.3, reb 4.1→4.3, ast 4.0→4.5, stl 1.1→1.2, tpm 2.5→2.6, fg_pct .473→.479, ft_pct .907→.908
- Paul George (5 outside): pts 17.4→17.5, reb 5.3→5.2, ast 3.6→3.7, stl 1.6→1.5, blk 0.4→0.5, tov 1.7→2.0, fg_pct .439→.443, ft_pct .831→.840
- Damian Lillard (5 outside): pts 19.1→19.6, reb 3.6→4.1, ast 5.4→5.5, stl 0.9→1.0, tpm 2.6→2.8, tov 2.2→2.3, fg_pct .445→.439, ft_pct .914→.913
- LeBron James (5 outside): pts 20.3→20.2, reb 6.1→6.3, ast 7.2→7.0, tpm 1.4→1.5, fg_pct .513→.515, ft_pct .752→.755
- Rudy Gobert (5 outside): pts 10.9→11.2, reb 11.5→11.1, ast 1.7→1.6, stl 0.7→0.8, tov 1.4→1.3, fg_pct .674→.673, ft_pct .562→.588
- Jrue Holiday (5 outside): pts 12.8→12.2, reb 4.2→4.1, ast 4.6→4.4, stl 1.0→0.9, tpm 2.0→1.9, tov 2.1→1.9, fg_pct .455→.453, ft_pct .855→.858
- Tobias Harris (5 outside): pts 12.0→12.7, reb 4.6→5.1, stl 0.8→0.9, tov 0.9→1.0, fg_pct .472→.474, ft_pct .857→.864
- Nikola Vucevic (5 outside): pts 11.2→11.3, reb 6.2→6.4, ast 2.5→2.3, tpm 1.2→1.1, fg_pct .494→.499, ft_pct .810→.815
- Al Horford (3 outside): pts 8.6→7.5, reb 4.9→4.7, ast 2.6→2.2, stl 0.5→0.6, blk 0.9→0.8, tpm 1.6→1.5, tov 0.9→0.8, fg_pct .453→.440, ft_pct .819→.857
- T.J. McConnell (4 outside): pts 9.3→8.9, ast 5.1→4.6, stl 1.0→0.9, tpm 0.3→0.2, tov 1.1→1.2, fg_pct .531→.532, ft_pct .836→.796

## 4. What moved on the boards

EVIDENCE: `blend/out/board_diff_2026-10-14.txt` (`board_diff.py`, two runs identical): the kit board before (kit HEAD) and after, and the page's value ranks on Version 66's pool and on Version 67's.

| board | players | changed rank | mean move | moved more than 20 | left the range |
|---|---|---|---|---|---|
| page, top 100 | 100 | 85 | 8.41 | 8 | 5 |
| page, top 156 (the draftable pool) | 156 | 139 | 12.66 | 27 | 12 |
| kit board, top 100 | 100 | 88 | 8.45 | 7 | 6 |
| kit board, top 200 | 190 | 176 | 13.10 | 34 | 10 |

- Page top 12 before: ['Nikola Jokic', 'Victor Wembanyama', 'Shai Gilgeous-Alexander', 'Luka Doncic', 'Kawhi Leonard', 'Tyrese Maxey', 'Jamal Murray', 'Donovan Mitchell', 'Tyrese Haliburton', 'Jayson Tatum', 'Anthony Davis', 'Stephen Curry'].
- After: ['Nikola Jokic', 'Victor Wembanyama', 'Shai Gilgeous-Alexander', 'Luka Doncic', 'Kawhi Leonard', 'Tyrese Maxey', 'Tyrese Haliburton', 'Donovan Mitchell', 'Jayson Tatum', 'Stephen Curry', 'Anthony Davis', 'Jamal Murray'].
- Largest moves in the page's top 100: Tre Jones 89→128; Yaxel Lendeborg 70→102; Kel'el Ware 27→58; Saddiq Bey 90→120; Ryan Rollins 47→75; Reed Sheppard 63→89; Brandon Miller 74→52; Cameron Boozer 45→66; Cooper Flagg 44→24; Collin Gillespie 79→99; Ayo Dosunmu 81→101; Caleb Wilson 92→73; Tari Eason 98→117; OG Anunoby 51→33; Jarrett Allen 80→62.
- In the top 156: Bradley Beal 105→186; Ryan Kalkbrenner 146→213; Deandre Ayton 113→173; Cam Spencer 115→174; Naji Marshall 147→204; Julian Champagnie 110→159; Luke Kornet 148→196; Moussa Diabate 128→169; Tre Jones 89→128; Coby White 145→106; Kris Dunn 123→161; Sandro Mamukelashvili 155→121; Yaxel Lendeborg 70→102; Kel'el Ware 27→58; Santi Aldama 149→180.

**Your players and questions** (kit board, then page value rank):

| player | kit board, before / after | page value, before / after |
|---|---|---|
| Kawhi Leonard | 6 / 6 | 5 / 5 |
| Tyrese Haliburton | 11 / 8 | 9 / 7 |
| Walker Kessler | 22 / 26 | 22 / 28 |
| Kyrie Irving | 34 / 21 | 31 / 18 |
| Anthony Davis | 16 / 14 | 11 / 11 |
| Damian Lillard | 55 / 49 | 53 / 46 |
| Chet Holmgren | 18 / 24 | 17 / 23 |
| Yaxel Lendeborg | 72 / 102 | 70 / 102 |
| Kel'el Ware | 27 / 55 | 27 / 58 |
| Jalen Duren | 43 / 33 | 43 / 39 |
| Donovan Clingan | 35 / 48 | 38 / 50 |
| Zach Edey | 53 / 50 | 54 / 54 |

Every move of more than 20 places in the top 100 was inspected before publishing. None was a data error. In each one, our line had sat at or past the edge of the outside range in several of the nine categories: Tre Jones, Saddiq Bey, Ryan Rollins, Reed Sheppard and Lendeborg high; Brandon Miller low. Small moves in many categories add up in ranks 60–120, where one z point is about 30 places.

**The team budget did not improve.** 6 teams' pools still claim more possessions a game than any team used last season: ['WAS', 'MIL', 'PHI', 'MEM', 'NOP', 'MIA'] (`blend/out/team_budget_after.txt`, the 10/13 usage report's own script). The outside projections overload the same rosters about as much as we did. Fixing that needs the usage model on the sheet for after the draft (D-C2).

## 5. Test 7 — the card's 🎯 at your picks, Version 66 against Version 67

EVIDENCE: `blend/out/card_compare_2026-10-14.txt` (`card_compare.py`, two runs identical), from the deck's repeat-name replays of the same 28 graded mocks on each page (`arena/results/repeat_market_check_2026-10-14_v66.json` and `_v67.json`). The page is the only input that differs.

- **Turns compared:** 364. **The 🎯 changed at 152.**
- **By round** (changed / turns): R1 10/28, R2 8/28, R3 3/28, R4 9/28, R5 26/28, R6 17/28, R7 8/28, R8 11/28, R9 12/28, R10 14/28, R11 6/28, R12 13/28, R13 15/28.
- **Count of 🎯 across all turns, the 15 largest changes:** Kel'el Ware 45 to 8, Ty Jerome 58 to 86, Reed Sheppard 53 to 37, OG Anunoby 0 to 14, Yaxel Lendeborg 13 to 0, Tyrese Haliburton 1 to 12, VJ Edgecombe 18 to 7, Cameron Johnson 0 to 10, Jamal Murray 39 to 29, John Collins 2 to 12, Saddiq Bey 10 to 1, Michael Porter Jr. 7 to 1, Myles Turner 0 to 6, Derrick White 10 to 15, Julian Champagnie 5 to 0.
- **What it means for today (INFERENCE).** The card now points less often at the men only we liked (Ware, Sheppard, Lendeborg, Bey) and more often at men every source likes but the market prices late:
  - Ty Jerome: value #41, market #117.
  - OG Anunoby: value #33, market #65.
  - John Collins: value #74, market #118.
- **What this test cannot tell you.** Whether the new 🎯 wins more. The practice rooms are graded on our own lines, so regrading them on the blended lines would grade the blend by itself.

## 6. Publication

| step | result |
|---|---|
| deck build (7 gates) | refused once at gate 6: the colophon said "the other 97 rows", a count the gate rejects against the 335-row pool. The refused build had not touched the page (checked by comparison). Reworded, then PASS |
| chain on Version 67 | parity EXACT (455 owner turns across 35 committed states); test_card 103; test_draft 65; test_gates 54; full DOM 145 assertions, 0 failed; repeat-name 28 of 28 mocks replayed; 8 FLAGGED; 0 player(s), 0 line(s) more than 1 from their own shooting (200 deck and 200 kit lines checked); 4 player(s) with 4 cell(s) outside every reference (147 of the top 150 checkable) |
| kit | provenance PASS; board 200 from 313; tests OK; derived 27 of 27; the seat-10 slate regenerated (it still carried Version 65's pool) |
| publish | Version 67, version id 1791960484-154b, on the standing artifact; the served page equals the local file (sha256 16bb03665e93) inside the publisher's wrapper |
| PRs | deck #114 (Version 66) and #115 (Version 67) merged; this kit PR carries the tools, the lines and this report |

## 7. The plan against the outcome

The plan as sent to the owner before any line moved, graded binary:

| criterion | grade | evidence |
|---|---|---|
| C1 the audit and the 95% answer from files | PASS | §2, both audit records, two runs identical |
| C2 blended lines, two identical runs | PASS | `blend_lines.py` twice, `cmp` identical |
| C3 writer assertions, planted errors, no-op second run | PASS | §3 |
| C4 every blended value recomputed at the source | PASS | A8 in `blend_apply.py`, recomputed from the pinned files |
| C5 kit rebuild and tests | PASS | §6 |
| C6 deck build and full chain | PASS | §6 (one refusal on a prose count, fixed before publishing) |
| C7 test 7 count | PASS | §5, 152 of 364 |
| C8 Version 67 published, byte-verified; PRs merged | PASS | §6 |
| C9 this report through the gates | PASS | the gate runs are in the kit PR |

Predictions against outcomes:
- "About 241 rows change": 241. ✓
- "Envelope from 75% to above 95%": 75.2% → 99.7%. ✓
- "The top 12 barely moves": the same 12 names, reordered. ✓
- "No top-100 player moves more than about 20 places": **missed**. 8 on the page did, the largest 39; each was inspected (§4).
- The ±15% shot rule: **fired 23 times and was changed** (§3).

## Range check (D-RN-3)

Rule (owner, 2026-10-08): on a projection pass, every cell of a top-150 line that sits outside ALL its references either carries a one-line mechanism naming two dated outlets, or comes back inside. The references are Yahoo `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, RotoBaller `rotoballer-2026-10-13.csv` and the 2025-26 actual line. This page: 4 player(s) with 4 cell(s) outside every reference (147 of the top 150 checkable). Each one sits outside because the blend also reads FantasyPros and the BBM cards, which the deck's range check does not yet read (D-1013-14).

| player | deck rank | cells outside every reference | net z | mechanism (two dated outlets) |
|---|---|---|---|---|
| Yaxel Lendeborg | 102 | tpm 1 vs 1.2-1.3 | -0.21 | the six-way blend: FantasyPros 10/13 (0.6) and the BBM cards 10/13 (0.3) sit below the three references the check reads (Yahoo 10/13 1.3, Hashtag 10/12 1.2, RotoBaller 10/13 1.3); the equal-weight mean of the six is 1.0 |
| Caleb Wilson | 73 | ft_pct .735 vs .720-.728 | +0.09 | the six-way blend: FantasyPros 10/13 (.752) and the BBM cards 10/13 (.770) sit above the three references (Yahoo 10/13 .720, Hashtag 10/12 .720, RotoBaller 10/13 .728); the mean of the six is .735 |
| Collin Murray-Boyles | 132 | fg_pct .586 vs .579-.580 | +0.06 | the six-way blend: FantasyPros 10/13 (.600) and the BBM cards 10/13 (.599) sit above the three references (Yahoo 10/13 .580, Hashtag 10/12 .579, RotoBaller 10/13 .579); the mean of the six is .586 |
| Dylan Harper | 104 | ft_pct .765 vs .754-.758 | +0.05 | the six-way blend: FantasyPros 10/13 (.785) and the BBM cards 10/13 (.785) sit above the three references (Yahoo 10/13 .758, Hashtag 10/12 .754, RotoBaller 10/13 .755); the mean of the six is .765 |

## Points identity (D-1009-3)

0 player(s), 0 line(s) more than 1 from their own shooting (200 deck and 200 kit lines checked) (`blend/out/identity_v67.txt`; the deck's `identity_check.py` on Version 67, both planes). No line needs a mechanism.

## Watchlist

- **This morning's final pull and the Yahoo lock paste** (D-1013-1) build Version 68 on top of Version 67. If the lock paste brings new Yahoo projected lines (not only prices), the blend can be re-run on them mechanically with the same two scripts (D-1014-3).
- **The publish freeze during the draft** (D-1013-5) and **no RESYNC during the draft** (D-1013-2) stand.
- **Ty Jerome** is now the 🎯 in 28 of 28 replayed mocks (value #41, market #117). His line sits inside all three projections the check reads, and three of the four outside ranks put him at 48–65.

## Open-item receipts

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| (this pass) | records only; no web research and no roster pull beyond Version 66's verification (direct-complete 335/335, 2026-10-14) | the blend reads the five outside projections pinned 10/12–10/13; no tag or placement moved |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the 10/13 pull (`after-report-2026-10-13.md`, receipts dated 10/13); Kawhi's debut read from ESPN's 10/13 box score for Version 66 | held or unsigned on 2026-10-13 per those receipts; not re-queried tonight (did not check); this morning's final pull re-queries them |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 16bb03665e93), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 28 of 28 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-13.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 28 of 28 | 41 | 117 | 48 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 19 of 28 | 89 | 180 | 56 | 118 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 11 of 28 | 33 | 65 | 60 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 9 of 28 | 105 | 138 | 181 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| John Collins | 9 of 28 | 74 | 118 | 102 | 71 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 8 of 28 | 99 | 183 | 100 | 126 | 148 | 155 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 8 of 28 | 6 | 32 | 15 | 16 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 7 of 28 | 112 | 141 | 120 | 131 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (19 mocks, value 9, market 18); Derrick White (15 mocks, value 25, market 45); Lauri Markkanen (15 mocks, value 20, market 37); Tyrese Haliburton (12 mocks, value 7, market 12); Tyrese Maxey (7 mocks, value 5, market 9); Kel'el Ware (6 mocks, value 58, market 77); VJ Edgecombe (6 mocks, value 60, market 75).

## Bounds

**Out of scope by design.**
- Games, minutes and availability (your calls and the 10/13 minutes-and-games pass stand).
- The usage model and team scaling (D-C2, after the draft).
- Adding FantasyPros and the cards to the deck's own range check (D-1013-14).
- Any change to the engine, the card or the page beyond its Data paragraph.

**In scope and unverified.**
- **Whether equal weights beat our line alone, or a 50/50 split, on real outcomes:** `NOT-ATTEMPTED`. It needs last season's pre-season projections from the outside sources. None are on file, and I did not search for archived copies tonight (time). The choice rests on the measured fact that the six forecasters sit equally close to each other (§2) and on general forecasting practice. It is a **candidate**, decision D-1014-2.
- **Whether the new 🎯 wins more often than the old one:** `UNVERIFIABLE` before the season. Every practice room is graded on our own projected lines (§5).
- **The players with fewer than three outside projections** (9 in the top 200 before the blend) keep our lines unchecked against a consensus: `NOT-ATTEMPTED` by rule (A4).

## Decision sheet (owner disposes)

| id | decision | options | recommendation |
|---|---|---|---|
| D-1014-1 | Lendeborg's line | (a) keep the blend (value #102); (b) take his line out of the blend, back to ours (value #70); (c) keep the blend and add a judgment note (a tooltip flag, it moves no rank) | (a). Your plan to take him in round 7 or 8 does not need the card's agreement, and the outside average sits below our line in 8 of his 9 categories |
| D-1014-2 | the blend's weights | (a) keep equal weights (ours one of six); (b) 50/50 ours against the outside average; (c) revert to Version 66's lines | (a). (b) or (c) is a rerun of the same scripts and the chain, about 50 minutes |
| D-1014-3 | the lock paste | (a) if Yahoo's lock paste changes projected lines, re-run the blend on them before the lock; (b) keep the 10/13 lines regardless | (a) |
| D-1014-4 | the six teams over budget | (a) leave for after the draft with D-C2; (b) scale those pools tonight | (a) |

## Provenance

- **Session:** this cloud session, the night of 10/13 (UTC 2026-10-14). Plan, Council and adversarial pass as described above.
- **Governors loaded for this task:** gauntlet, plan-gate, adversarial-verify and after-report. The plan block was emitted before the work; council and scope-fence were applied in-session.
- **Kit:** branch `claude/market-data-workorder-mnfi2b`; commits 440bb9e (tools and audit), e2cc9db (lines, board, slate), and this report's commit.
- **Deck:** PR #114 → c1065c5 (Version 66), PR #115 → 43ca6bf (Version 67).
- **Artifact:** https://claude.ai/code/artifact/190e2c13-a19c-4239-8085-73230ef4eae0, versions 1791957366-babb (66) and 1791960484-154b (67).
- **Re-verify:**
  - `python3 report/blend/tools/blend_lines.py --deck <deck>/data/players.csv --kit report/projections-2026-27.csv --out x.json` on the pre-blend files reproduces `lines_blend_2026-10-14.json`.
  - `python3 report/blend/tools/blend_apply.py report/blend/out/lines_blend_2026-10-14.json --deck … --kit …` on the shipped files changes nothing.
  - `python3 report/blend/tools/audit_measure.py` reproduces `audit_v67_lines_new200.txt`.
