# After-report — 2026-10-13 (audit): validation and integrity audit of the top-180 lines on the kit board

**Owner request (2026-10-13, verbatim):** "With the board now rebuilt, I'd like for you to conduct a validation and integrity audit on the top 180 players 9cat projection lines. Do you agree with the kit's projections, or do they seem unrealistic? Provide a report of who you have question marks on, and let me know what I can upload to you to help confidence reach near certain levels."

**What was analyzed:** the kit board's ranks 1 to 180 (`report/top-200-2026-27.md` at kit `main` a98a37f, Version 65's lines) and each player's line in `report/projections-2026-27.csv`. Nothing on either plane changed: both files are byte-identical before and after the audit. References: Yahoo `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, RotoBaller `rotoballer-2026-09-29.csv`; the player's own Basketball-Reference seasons 2003-04 to 2025-26 (`report/wo5/data/bref_totals_2004-2026.csv`, pinned at WO-5); outside ranks from Hashtag, RotoBaller, RotoWire, Rotoworld, Yahoo.

**Method (A1 to A6, stated to the owner before the run):** A1 the universe is the kit board's top 180. A2 history is the player's own per-36 rates over his last three seasons of 25+ games; a cell is questioned beyond that band by more than 10% (0.1 floor), a percentage beyond the career band by more than .010. A3 minutes are questioned 2+ above the three-season high or 4+ from Hashtag's; games 10+ above the three-season average after a season under 60, or 6+ above both Yahoo's and Hashtag's projected games. A4 age: 32 and older projecting more per 36 than last season, 23 and younger projecting less, and 34 and older above the outside average in two of points, rebounds and assists. A5 market: every outside rank 25+ places on one side of ours. A6 tiers: HIGH when three or more tests fire or the cells outside the outside range carry more than 0.5 z; MEDIUM two tests; LOW one; UNANCHORED when fewer than two qualifying NBA seasons exist; CLEAN none. Seven tests, T1 to T7, in `audit180-2026-10-13/audit180.py`; two runs identical.

Pull window: 2026-10-13 → 2026-10-13 (no roster pull; the lines as merged in kit PR #109).

**Headline.** The lines are internally sound and history-shaped: every one of the 180 passes the points identity, and none departs from the player's own three-season per-36 band by more than the tolerance (T2 fired 0 times). That is the strength and the limit of the method: a line built from a player's own rates cannot be wrong about his arithmetic, and cannot see a role change. The real question marks are therefore where the outside projections disagree with that history. 110 of the 180 have a category outside all three outside projections, but after this evening's clamp the disagreements are small and balanced: the cells beyond the range carry +30.28 z on the flattering side and -27.15 on the other, and only 13 lines carry more than 0.5 z net. I agree with the top 100 as a whole; my question marks concentrate on 12 HIGH lines (10 of them past rank 100, 8 with only two outside projections), on 12 players aged 34 and older whose lines carry no age decline, on the 18 rookies and returners with fewer than two NBA seasons, and on the 6 team pools still above last season's league maximum of possessions. Games played are not a systematic lean: over the 165 players both Yahoo and Hashtag project, our games sum to 11198 against their average 11255.

## 1. Roster changes

None. No line, tag, placement, games or minutes figure changed on either plane; this is an assessment.

## 2. The verdict, test by test

EVIDENCE: `audit180-2026-10-13/audit180.json` (one record per player), `audit180.txt` (the flagged lines), `range_no_actual_v65.json`, `team_budget_v65.txt`.

| test | what it asks | fired | reading |
|---|---|---|---|
| T1 outside range | is a cell outside all three outside projections, and by how much in the deck's z frame | 110 of 180 | small and two-sided after the clamp: 255 cells, +30.28 z flattering against -27.15; 13 lines over 0.5 z net, all but 1 of them ranked past 100. 24 of the 180 have only two outside projections and 3 have none (Deandre Ayton, Herb Jones, Marcus Smart) |
| T2 own history | does the per-36 line sit inside the player's own three-season band | 0 | the method builds each line from that band, so it cannot fail here; the test confirms no transcription or scaling error in the 162 anchored lines |
| T3 career shooting | FG% or FT% outside the career band | 1 | Ja Morant: FT% .845 against a career band of .728 to .824 |
| T4 minutes and games | minutes above the career high or far from Hashtag; games above the player's own history or above both outside projections | 35 | 25 games flags rest on the player's injury history; only 6 lines sit 6+ games above both Yahoo and Hashtag (Cam Johnson, Miles McBride, Jordan Goodwin, Justin Champagnie, Al Horford, Bilal Coulibaly). Our games are not optimistic in aggregate (11198 against 11255 over 165 players) |
| T5 points identity | points equal to 2·FG%·FGA + 3PM + FT%·FTA within 1 | 0 | every line reconciles |
| T6 age | 32+ projected up, 23 and under projected down, 34+ above the outside average | 12 | no line projects an old player up or a young player down against his own last season; 12 players aged 34 and older sit above the outside average in two or more of points, rebounds and assists because the method carries no age decline: Kawhi Leonard (35), Kevin Durant (38), Kyrie Irving (34), Paul George (36), Damian Lillard (36), LeBron James (42), Rudy Gobert (34), Jrue Holiday (36), Tobias Harris (34), Nikola Vucevic (36), Al Horford (40), T.J. McConnell (34) |
| T7 market | every outside rank 25+ places on one side of ours | 15 | we are high on 10 (Dyson Daniels, Reed Sheppard, Kristaps Porzingis, Yaxel Lendeborg, Collin Gillespie, Saddiq Bey, Julian Champagnie, Kris Dunn, Luke Kornet, Derrick Jones Jr) and low on 5 (Zion Williamson, AJ Dybantsa, Coby White, Cedric Coward, Collin Murray-Boyles) |
| team budget | a team's pool above the league maximum of possessions used | 6 teams | WAS, MIL, PHI, NOP, MEM, MIA; 8 teams above their own 2025-26 total; Philadelphia 121.4 against 117.7 (`team_budget_v65.txt`, the dial pass's run on these same lines) |

Tiers: HIGH 12, MEDIUM 27, LOW 84, UNANCHORED 18, CLEAN 39. Of the 180, 39 lines pass every test and 84 carry one flag; apart from the age-decline question in T6, which is a property of the method rather than of any one line, I agree with those 123 as they stand.

## 3. The question marks

EVIDENCE: `audit180-2026-10-13/audit180.json`; z figures in the deck's own frame, flattering positive.

### HIGH

| rank | player | age | net z beyond the range | why |
|---|---|---|---|---|
| 7 | Jamal Murray (DEN) | 29 | +0.51 | outside all three projections: ast 7.1 vs 6.5 to 6.7 (+0.20 z); 3PM 3.3 vs 2.8 to 3 (+0.31 z) |
| 79 | Collin Gillespie (PHX) | 27 | +0.18 | outside all three projections: pts 12.7 vs 9.5 to 11.9 (+0.15 z); reb 4.1 vs 3.3 to 3.9 (+0.08 z); 3PM 2.9 vs 2.1 to 2.7 (+0.21 z); TO 1.6 vs 1.1 to 1.4 (-0.26 z); gp 75 vs three-season average 56 with a season under 60; every outside rank 25+ places below ours (we are high): Yahoo 116, Hashtag 126, RotoBaller 156, RotoWire 135, Rotoworld 148 |
| 103 | Bradley Beal (LAC) | 33 | +1.10 | outside all three projections: pts 16.7 vs 9.8 to 13.9 (+0.52 z); reb 3.3 vs 2 to 2.8 (+0.21 z); ast 3.7 vs 2.3 to 3 (+0.35 z); 3PM 1.9 vs 1.1 to 1.7 (+0.21 z); TO 1.9 vs 1.2 to 1.7 (-0.26 z); FT% .809 vs .795 to .801 (+0.07 z); mpg 32.1 vs Hashtag 27.5 |
| 149 | Aaron Nesmith (IND) | 27 | -0.53 | outside all three projections: FG% .427 vs .450 to .456 (-0.42 z); FT% .829 vs .843 to .862 (-0.11 z); gp 68 vs three-season average 54 with a season under 60 |
| 153 | Jaylon Tyson (CLE) | 24 | +0.74 | outside all three projections: pts 13.1 vs 10.6 to 11.3 (+0.33 z); reb 5.1 vs 4.5 to 4.7 (+0.16 z); 3PM 2 vs 1.5 to 1.7 (+0.31 z); TO 1.5 vs 0.8 to 1.3 (-0.26 z); FG% .489 vs .471 to .477 (+0.20 z); gp 72 vs three-season average 56 with a season under 60 |
| 154 | Sandro Mamukelashvili (LAL) | 27 | -1.00 | outside all three projections: pts 11 vs 12 to 13.7 (-0.18 z); reb 4.9 vs 5.6 to 6.2 (-0.29 z); stl 0.7 vs 0.8 to 0.9 (-0.32 z); 3PM 1.4 vs 1.6 to 1.9 (-0.21 z); gp 74 vs three-season average 62 with a season under 60 |
| 155 | Jordan Goodwin (PHX) | 28 | +0.57 | outside all three projections: pts 8.7 vs 6.9 to 7.7 (+0.18 z); reb 4.9 vs 4.1 to 4.6 (+0.12 z); 3PM 1.6 vs 1.2 to 1.3 (+0.31 z); FT% .712 vs .726 to .740 (-0.04 z); gp 75 vs three-season average 52 with a season under 60; gp 75 vs outside 65 (Yahoo/Hashtag) |
| 158 | Kyle Filipowski (UTA) | 23 | +0.77 | outside all three projections: pts 11.4 vs 9.6 to 10.3 (+0.20 z); reb 7.2 vs 6 to 6.5 (+0.29 z); ast 2.6 vs 2.1 to 2.3 (+0.15 z); FT% .737 vs .719 to .723 (+0.13 z) |
| 165 | Quentin Grimes (LAL) | 26 | -0.69 | outside all three projections: pts 13.3 vs 15.5 to 15.6 (-0.41 z); reb 3.6 vs 3.9 to 4.4 (-0.12 z); blk 0.3 vs 0.4 to 0.4 (-0.20 z); 3PM 1.7 vs 2.1 to 2.4 (-0.41 z); TO 1.8 vs 2 to 2 (+0.26 z); FT% .824 vs .799 to .806 (+0.19 z) |
| 167 | Al Horford (GSW) | 40 | +0.47 | outside all three projections: pts 8.6 vs 5.8 to 7.7 (+0.17 z); ast 2.6 vs 1.6 to 2.2 (+0.20 z); FG% .453 vs .435 to .438 (+0.17 z); FT% .819 vs .857 to .867 (-0.07 z); gp 62 vs outside 53 (Yahoo/Hashtag); age 40: above the outside average in pts, reb, ast (no decline in the method) |
| 168 | Bennedict Mathurin (NOP) | 24 | +1.22 | outside all three projections: pts 17.6 vs 11.2 to 13.2 (+0.81 z); reb 5.4 vs 3.5 to 4.2 (+0.49 z); ast 2.4 vs 1.4 to 1.6 (+0.40 z); 3PM 1.4 vs 0.9 to 1 (+0.41 z); TO 2.2 vs 1.3 to 1.6 (-0.77 z); FG% .434 vs .440 to .443 (-0.12 z) |
| 174 | T.J. McConnell (IND) | 34 | +0.52 | outside all three projections: pts 9.3 vs 8.6 to 8.6 (+0.13 z); ast 5.1 vs 4.4 to 4.4 (+0.35 z); FT% .836 vs .796 to .814 (+0.04 z); age 34: above the outside average in pts, reb, ast (no decline in the method) |

### MEDIUM

| rank | player | age | net z | why |
|---|---|---|---|---|
| 14 | Kevin Durant (HOU) | 38 | -0.11 | outside all three projections: ast 4.8 vs 3.8 to 4.3 (+0.25 z); TO 3.2 vs 2.9 to 2.9 (-0.38 z); FG% .515 vs .523 to .524 (-0.23 z); FT% .876 vs .860 to .863 (+0.25 z); age 38: above the outside average in pts, reb, ast (no decline in the method) |
| 20 | Domantas Sabonis (SAC) | 30 | +0.21 | outside all three projections: 3PM 0.9 vs 0.6 to 0.7 (+0.21 z); mpg 34.7 vs Hashtag 30.7 |
| 23 | Dyson Daniels (ATL) | 23 | +0.15 | outside all three projections: reb 6.8 vs 5.8 to 6.4 (+0.16 z); ast 5.9 vs 4.7 to 5.5 (+0.20 z); 3PM 0.3 vs 0.5 to 0.6 (-0.21 z); every outside rank 25+ places below ours (we are high): Yahoo 62, Hashtag 64, RotoBaller 53, RotoWire 69, Rotoworld 56 |
| 27 | Kel'el Ware (MIL) | 22 | +0.04 | outside all three projections: FT% .732 vs .714 to .723 (+0.04 z); mpg 26.8 vs three-season high 22.2 |
| 32 | Franz Wagner (ORL) | 25 | -0.34 | outside all three projections: reb 6 vs 5.4 to 5.7 (+0.12 z); ast 3.8 vs 4.1 to 4.3 (-0.15 z); FT% .832 vs .846 to .852 (-0.31 z); gp 66 vs three-season average 55 with a season under 60 |
| 42 | Jalen Williams (OKC) | 25 | +0.02 | outside all three projections: ast 6 vs 5 to 5.3 (+0.35 z); 3PM 0.8 vs 1.3 to 1.5 (-0.51 z); FT% .828 vs .805 to .815 (+0.18 z); gp 68 vs three-season average 58 with a season under 60 |
| 52 | Naz Reid (CHA) | 27 | -0.35 | outside all three projections: TO 1.9 vs 1.6 to 1.7 (-0.26 z); FT% .731 vs .746 to .756 (-0.09 z); mpg 31 vs three-season high 27.5 |
| 63 | Reed Sheppard (HOU) | 22 | +0.21 | outside all three projections: 3PM 2.8 vs 2.2 to 2.6 (+0.21 z); every outside rank 25+ places below ours (we are high): Yahoo 141, Hashtag 118, RotoBaller 129, RotoWire 136, Rotoworld 126 |
| 64 | Tyler Herro (MIL) | 27 | -0.17 | outside all three projections: ast 4.1 vs 4.6 to 4.9 (-0.25 z); 3PM 2.5 vs 2.9 to 3.2 (-0.41 z); TO 1.9 vs 2.2 to 2.3 (+0.38 z); FT% .904 vs .886 to .894 (+0.11 z); gp 70 vs three-season average 51 with a season under 60 |
| 68 | Kristaps Porzingis (GSW) | 31 | +0.00 | gp 54 vs three-season average 44 with a season under 60; every outside rank 25+ places below ours (we are high): Yahoo 154, Hashtag 96, RotoBaller 189, RotoWire 128, Rotoworld 115 |
| 83 | Neemias Queta (BOS) | 27 | -0.08 | outside all three projections: FT% .704 vs .714 to .719 (-0.08 z); gp 68 vs three-season average 55 with a season under 60 |
| 107 | Rudy Gobert (MIN) | 34 | -0.27 | outside all three projections: FT% .562 vs .583 to .596 (-0.27 z); age 34: above the outside average in reb, ast (no decline in the method) |
| 110 | Julian Champagnie (SAS) | 25 | +0.28 | outside all three projections: reb 5.8 vs 4.4 to 5 (+0.33 z); FT% .847 vs .856 to .870 (-0.05 z); every outside rank 25+ places below ours (we are high): Yahoo 173, Hashtag 165, RotoBaller 186, Rotoworld 194 |
| 113 | Zion Williamson (NOP) | 26 | +0.08 | outside all three projections: ast 3.2 vs 3.9 to 4.1 (-0.35 z); TO 2 vs 2.2 to 2.4 (+0.26 z); FT% .709 vs .696 to .702 (+0.17 z); every outside rank 25+ places above ours (we are low): Yahoo 81, Hashtag 78, RotoBaller 80, RotoWire 82, Rotoworld 71 |
| 115 | Cam Spencer (MEM) | 26 | +0.22 | outside all three projections: ast 5.6 vs 3 to 5.3 (+0.15 z); FG% .471 vs .452 to .465 (+0.07 z); gp 68 vs three-season average 48 with a season under 60 |
| 118 | Kyshawn George (WAS) | 23 | +0.25 | outside all three projections: pts 14.5 vs 11.9 to 12.5 (+0.37 z); ast 4.5 vs 3.5 to 3.9 (+0.30 z); TO 2.6 vs 2 to 2.2 (-0.51 z); FT% .795 vs .782 to .785 (+0.09 z); gp 68 vs three-season average 58 with a season under 60 |
| 122 | Cam Johnson (DEN) | 30 | -0.12 | outside all three projections: pts 12.1 vs 12.9 to 14.2 (-0.15 z); ast 2.4 vs 2.7 to 2.7 (-0.15 z); TO 0.9 vs 1.1 to 1.2 (+0.26 z); FT% .843 vs .854 to .862 (-0.08 z); gp 66 vs outside 56/60 (Yahoo/Hashtag) |
| 126 | Kris Dunn (LAC) | 32 | -0.03 | outside all three projections: pts 7.1 vs 6.3 to 6.6 (+0.09 z); ast 3.6 vs 3.1 to 3.2 (+0.20 z); TO 1.4 vs 1.1 to 1.1 (-0.38 z); FT% .757 vs .734 to .739 (+0.06 z); every outside rank 25+ places below ours (we are high): Yahoo 189, Hashtag 193, Rotoworld 184 |
| 133 | Ja Morant (POR) | 27 | +0.00 | FT% .845 outside his career band .728 to .824; mpg 25.5 vs Hashtag 30.4 |
| 136 | Tobias Harris (SAS) | 34 | -0.04 | outside all three projections: FT% .857 vs .863 to .869 (-0.04 z); age 34: above the outside average in pts, ast (no decline in the method) |
| 142 | Coby White (CHA) | 26 | -0.40 | outside all three projections: FG% .442 vs .449 to .451 (-0.16 z); FT% .830 vs .843 to .864 (-0.24 z); every outside rank 25+ places above ours (we are low): Yahoo 86, Hashtag 86, RotoBaller 77, RotoWire 68, Rotoworld 76 |
| 146 | Mitchell Robinson (BOS) | 28 | +0.04 | outside all three projections: FG% .716 vs .685 to .709 (+0.04 z); gp 64 vs three-season average 50 with a season under 60 |
| 147 | Luke Kornet (SAS) | 31 | -0.12 | outside all three projections: reb 6.1 vs 5 to 5.8 (+0.12 z); FG% .613 vs .656 to .662 (-0.28 z); FT% .812 vs .765 to .804 (+0.04 z); every outside rank 25+ places below ours (we are high): Yahoo 254, Hashtag 189, RotoBaller 211 |
| 152 | Miles McBride (NYK) | 26 | +0.40 | outside all three projections: pts 11.9 vs 9.1 to 10.9 (+0.18 z); 3PM 2.7 vs 2 to 2.3 (+0.41 z); TO 0.8 vs 0.6 to 0.7 (-0.13 z); FT% .785 vs .803 to .803 (-0.06 z); gp 72 vs three-season average 58 with a season under 60; gp 72 vs outside 66 (Yahoo/Hashtag) |
| 160 | Derrick Jones Jr (LAC) | 29 | +0.15 | outside all three projections: ast 1.4 vs 1 to 1.1 (+0.15 z); every outside rank 25+ places below ours (we are high): Yahoo 223, Hashtag 199, RotoBaller 185 |
| 163 | Justin Champagnie (WAS) | 25 | +0.30 | outside all three projections: pts 8.6 vs 7.6 to 8.1 (+0.09 z); reb 5.6 vs 4.9 to 5.2 (+0.16 z); FT% .776 vs .754 to .766 (+0.05 z); gp 73 vs three-season average 56 with a season under 60; gp 73 vs outside 58 (Yahoo/Hashtag) |
| 178 | Bilal Coulibaly (WAS) | 22 | +0.18 | outside all three projections: pts 11.7 vs 10.4 to 10.7 (+0.18 z); gp 68 vs outside 58 (Yahoo/Hashtag) |

### UNANCHORED (fewer than two NBA seasons of 25+ games: college or one-season translations)

| rank | player | NBA seasons on file | net z | what the outside projections say |
|---|---|---|---|---|
| 41 | Cooper Flagg (DAL) | 2025-26 | -0.46 | outside all three projections: pts 21 vs 22.4 to 23.3 (-0.26 z); ast 4.5 vs 4.9 to 5.1 (-0.20 z) |
| 44 | Cameron Boozer (MEM) | none | +0.00 | inside all three projections; no NBA history at all |
| 53 | Zach Edey (MEM) | 2024-25 | +0.00 | inside all three projections; one season |
| 59 | VJ Edgecombe (PHI) | 2025-26 | +0.00 | inside all three projections; one season |
| 66 | Kon Knueppel (CHA) | 2025-26 | +0.00 | inside all three projections; one season |
| 72 | Yaxel Lendeborg (GSW) | none | +0.00 | every outside rank 25+ places below ours (we are high): Yahoo 133, Hashtag 121, RotoBaller 98, RotoWire 134, Rotoworld 137 |
| 92 | Caleb Wilson (CHI) | none | +0.00 | inside all three projections; no NBA history at all |
| 109 | Darryn Peterson (UTA) | none | +0.00 | inside all three projections; no NBA history at all |
| 135 | Derik Queen (NOP) | 2025-26 | -0.16 | outside all three projections: reb 7.1 vs 7.5 to 7.8 (-0.16 z) |
| 140 | AJ Dybantsa (WAS) | none | -0.17 | outside all three projections: ast 2.8 vs 3 to 3.1 (-0.10 z); 3PM 1.6 vs 1.2 to 1.4 (+0.21 z); FG% .450 vs .462 to .463 (-0.28 z); every outside rank 25+ places above ours (we are low): Yahoo 93, RotoBaller 103, RotoWire 101, Rotoworld 89 |
| 144 | Ryan Kalkbrenner (CHA) | 2025-26 | +0.84 | outside all three projections: pts 7.6 vs 6.5 to 6.8 (+0.15 z); reb 5.5 vs 4.7 to 4.9 (+0.25 z); ast 0.8 vs 0.7 to 0.7 (+0.05 z); blk 1.5 vs 1.3 to 1.3 (+0.39 z) |
| 145 | Scotty Pippen Jr. (MEM) | 2024-25 | +0.00 | inside all three projections; one season |
| 156 | Cedric Coward (MEM) | 2025-26 | +0.00 | every outside rank 25+ places above ours (we are low): Yahoo 75, Hashtag 117, RotoBaller 91, RotoWire 90, Rotoworld 117 |
| 161 | Maxime Raynaud (SAC) | 2025-26 | +0.00 | inside all three projections; one season |
| 170 | Dylan Cardwell (SAC) | 2025-26 | +0.95 | outside all three projections: pts 5.4 vs 3.1 to 4.7 (+0.13 z); reb 7.5 vs 4.3 to 6.7 (+0.33 z); ast 1.4 vs 0.8 to 1.2 (+0.10 z); blk 1.5 vs 0.9 to 1.3 (+0.39 z) |
| 171 | Keaton Wagler (LAC) | none | +0.38 | outside all three projections: pts 16.5 vs 11.6 to 12.1 (+0.81 z); ast 3.8 vs 3.2 to 3.6 (+0.10 z); 3PM 2.3 vs 1.4 to 1.5 (+0.82 z); TO 2.4 vs 1.5 to 1.7 (-0.90 z); FG% .430 vs .462 to .508 (-0.70 z); FT% .820 vs .697 to .798 (+0.25 z) |
| 173 | Darius Acuff (SAC) | none | -0.47 | outside all three projections: TO 2.6 vs 1.4 to 2.1 (-0.64 z); FT% .820 vs .772 to .804 (+0.17 z) |
| 175 | Collin Murray-Boyles (TOR) | 2025-26 | -0.64 | outside all three projections: pts 8.5 vs 10.4 to 11 (-0.35 z); reb 5 vs 6.1 to 6.5 (-0.45 z); ast 1.9 vs 2.1 to 2.4 (-0.10 z); TO 1 vs 1.2 to 1.4 (+0.26 z); mpg 21.9 vs Hashtag 28; every outside rank 25+ places above ours (we are low): Yahoo 102, Hashtag 108, RotoBaller 97, RotoWire 109, Rotoworld 88 |

### LOW (one small disagreement each; I agree with these lines)

Nikola Jokic (outside all three projections: TO 3.7 vs 3.3 to 3.5 (-0.26 z); FG% .566 vs .573 to .574 (-0.20 z); FT% .829 vs .816 to .822 (+0.17 z)); Shai Gilgeous-Alexander (outside all three projections: FT% .874 vs .885 to .889 (-0.32 z)); Victor Wembanyama (outside all three projections: ast 3.1 vs 3.3 to 3.6 (-0.10 z); TO 2.4 vs 2.6 to 2.9 (+0.26 z)); Luka Doncic (outside all three projections: FT% .772 vs .781 to .782 (-0.30 z)); Kawhi Leonard (age 35: above the outside average in pts, reb, ast (no decline in the method)); Donovan Mitchell (outside all three projections: TO 2.8 vs 2.6 to 2.6 (-0.26 z)); Stephen Curry (outside all three projections: ast 4.7 vs 5 to 5.2 (-0.15 z); FG% .469 vs .453 to .459 (+0.30 z); FT% .919 vs .926 to .929 (-0.12 z)); Tyrese Haliburton (outside all three projections: TO 1.5 vs 1.7 to 1.7 (+0.26 z)); Trey Murphy III (gp 70 vs three-season average 59 with a season under 60); Jalen Johnson (gp 65 vs three-season average 55 with a season under 60); Amen Thompson (outside all three projections: ast 5.3 vs 4 to 5 (+0.15 z); TO 2.4 vs 2.1 to 2.2 (-0.26 z)); Chet Holmgren (outside all three projections: FG% .549 vs .535 to .538 (+0.20 z); FT% .790 vs .780 to .784 (+0.08 z)); Scottie Barnes (outside all three projections: FG% .496 vs .477 to .484 (+0.27 z); FT% .801 vs .784 to .791 (+0.12 z)); Lauri Markkanen (gp 66 vs three-season average 48 with a season under 60); Cade Cunningham (outside all three projections: blk 0.7 vs 0.8 to 0.8 (-0.20 z); TO 3.7 vs 4 to 4.1 (+0.38 z)); Bam Adebayo (outside all three projections: ast 3.2 vs 3.6 to 3.8 (-0.20 z); TO 1.6 vs 1.8 to 1.9 (+0.26 z)); Derrick White (outside all three projections: 3PM 2.7 vs 2.9 to 3.1 (-0.21 z); FG% .409 vs .416 to .440 (-0.16 z)); Austin Reaves (outside all three projections: FG% .487 vs .470 to .481 (+0.14 z)); Michael Porter Jr (outside all three projections: pts 24.5 vs 18.7 to 21.8 (+0.50 z); ast 3 vs 2.4 to 2.6 (+0.20 z); stl 0.7 vs 0.8 to 1 (-0.32 z); 3PM 3.4 vs 2.9 to 3.1 (+0.31 z); TO 2.3 vs 1.9 to 2 (-0.38 z)); Onyeka Okongwu (outside all three projections: ast 3.1 vs 2.7 to 2.9 (+0.10 z)); Kyrie Irving (age 34: above the outside average in pts, reb (no decline in the method)); Evan Mobley (gp 74 vs three-season average 62 with a season under 60); Paul George (age 36: above the outside average in pts, reb (no decline in the method)); Giannis Antetokounmpo (outside all three projections: TO 3.6 vs 3.1 to 3.3 (-0.38 z); FG% .600 vs .608 to .613 (-0.24 z); FT% .664 vs .628 to .639 (+0.91 z)); Jalen Duren (outside all three projections: pts 19.5 vs 17.2 to 18.5 (+0.18 z); ast 2 vs 2.3 to 2.5 (-0.15 z); stl 0.7 vs 0.8 to 0.8 (-0.32 z)); Ty Jerome (mpg 27.6 vs three-season high 19.9); Nickeil Alexander-Walker (outside all three projections: 3PM 3.2 vs 2.6 to 3 (+0.21 z); TO 2.1 vs 1.7 to 1.9 (-0.26 z)); OG Anunoby (outside all three projections: TO 1.8 vs 1.5 to 1.6 (-0.26 z)); LaMelo Ball (outside all three projections: FT% .882 vs .866 to .874 (+0.07 z)); Devin Booker (outside all three projections: FT% .873 vs .881 to .884 (-0.21 z)); Damian Lillard (age 36: above the outside average in pts, ast (no decline in the method)); Alperen Sengun (outside all three projections: TO 3.2 vs 3 to 3 (-0.26 z)); LeBron James (age 42: above the outside average in pts, ast (no decline in the method)); Josh Giddey (outside all three projections: FT% .763 vs .771 to .776 (-0.11 z)); Darius Garland (gp 70 vs three-season average 59 with a season under 60); De'Aaron Fox (outside all three projections: FT% .756 vs .777 to .799 (-0.23 z)); Mikal Bridges (outside all three projections: TO 1 vs 1.2 to 1.3 (+0.26 z); FT% .832 vs .815 to .824 (+0.03 z)); Jalen Suggs (outside all three projections: ast 5.5 vs 4.8 to 5 (+0.25 z); blk 0.7 vs 0.8 to 0.8 (-0.20 z); FT% .834 vs .846 to .866 (-0.08 z)); Brandon Miller (outside all three projections: 3PM 3.1 vs 3.4 to 3.5 (-0.31 z)); John Collins (outside all three projections: FG% .550 vs .541 to .542 (+0.14 z); FT% .774 vs .799 to .810 (-0.20 z)); Jaden McDaniels (outside all three projections: reb 4.2 vs 4.8 to 5.8 (-0.25 z)); Keegan Murray (outside all three projections: pts 12.4 vs 13.3 to 16.1 (-0.17 z)); Payton Pritchard (outside all three projections: 3PM 2.7 vs 3 to 3.2 (-0.31 z); FG% .461 vs .467 to .467 (-0.13 z); FT% .883 vs .873 to .875 (+0.04 z)); Jarrett Allen (outside all three projections: FG% .639 vs .656 to .676 (-0.26 z)); Ayo Dosunmu (outside all three projections: 3PM 1.9 vs 1.5 to 1.7 (+0.21 z)); Norman Powell (outside all three projections: reb 3.5 vs 3.2 to 3.2 (+0.12 z); ast 2.5 vs 2.1 to 2.3 (+0.10 z)); Brandon Ingram (outside all three projections: TO 2.4 vs 2.6 to 2.7 (+0.26 z); FT% .811 vs .819 to .826 (-0.12 z)); Ivica Zubac (outside all three projections: TO 1.8 vs 1.6 to 1.6 (-0.26 z); FG% .603 vs .615 to .618 (-0.19 z); FT% .716 vs .681 to .700 (+0.16 z)); Josh Hart (outside all three projections: reb 7.4 vs 7.9 to 8.3 (-0.21 z); FT% .730 vs .751 to .759 (-0.13 z)); Tre Jones (outside all three projections: pts 13.7 vs 11.4 to 12.3 (+0.26 z)); Saddiq Bey (every outside rank 25+ places below ours (we are high): Yahoo 151, Hashtag 132, RotoBaller 143, RotoWire 131, Rotoworld 169); Matas Buzelis (outside all three projections: pts 16.2 vs 17.2 to 18.6 (-0.18 z)); Jabari Smith Jr (outside all three projections: ast 1.9 vs 1.6 to 1.7 (+0.10 z); FT% .782 vs .791 to .796 (-0.08 z)); Myles Turner (outside all three projections: FT% .750 vs .757 to .759 (-0.06 z)); Tari Eason (outside all three projections: 3PM 1.6 vs 1.3 to 1.4 (+0.21 z); FG% .427 vs .441 to .450 (-0.22 z)); Miles Bridges (outside all three projections: FG% .460 vs .444 to .451 (+0.20 z); FT% .823 vs .838 to .845 (-0.16 z)); Toumani Camara (outside all three projections: pts 13.5 vs 12.3 to 12.6 (+0.17 z); 3PM 2.7 vs 2.2 to 2.3 (+0.41 z); TO 1.8 vs 1.6 to 1.6 (-0.26 z)); Cason Wallace (outside all three projections: FG% .442 vs .449 to .453 (-0.09 z)); Alex Sarr (gp 72 vs three-season average 58 with a season under 60); Peyton Watson (outside all three projections: pts 14.5 vs 12.2 to 12.5 (+0.37 z); 3PM 1.5 vs 1.2 to 1.3 (+0.21 z); TO 1.7 vs 1.3 to 1.4 (-0.38 z)); Ajay Mitchell (mpg 25.8 vs Hashtag 30.1; gp 68 vs three-season average 46 with a season under 60); Isaiah Hartenstein (outside all three projections: FT% .631 vs .642 to .656 (-0.08 z)); Jakob Poeltl (outside all three projections: FG% .679 vs .653 to .668 (+0.12 z); FT% .588 vs .618 to .642 (-0.21 z)); Robert Williams III (outside all three projections: FG% .712 vs .687 to .697 (+0.10 z); FT% .618 vs .651 to .692 (-0.11 z)); Zach LaVine (gp 64 vs three-season average 46 with a season under 60); Christian Braun (outside all three projections: FG% .522 vs .531 to .560 (-0.13 z); FT% .774 vs .786 to .815 (-0.09 z)); Paolo Banchero (outside all three projections: pts 22 vs 23.6 to 24.3 (-0.30 z); 3PM 1.2 vs 1.4 to 1.5 (-0.21 z); FT% .764 vs .753 to .756 (+0.21 z)); CJ McCollum (outside all three projections: FT% .780 vs .749 to .765 (+0.15 z)); Aaron Gordon (gp 66 vs three-season average 53 with a season under 60); Jrue Holiday (age 36: above the outside average in pts, reb, ast (no decline in the method)); Wendell Carter Jr (outside all three projections: FG% .511 vs .490 to .504 (+0.09 z); FT% .775 vs .754 to .768 (+0.07 z)); Nic Claxton (outside all three projections: reb 6.9 vs 7.4 to 8 (-0.21 z); ast 3.7 vs 3.1 to 3.5 (+0.10 z); stl 0.7 vs 0.8 to 0.8 (-0.32 z); FT% .596 vs .581 to .583 (+0.14 z)); Bobby Portis (outside all three projections: 3PM 2 vs 1.6 to 1.8 (+0.21 z); FT% .724 vs .765 to .776 (-0.13 z)); Moussa Diabate (outside all three projections: FG% .623 vs .607 to .616 (+0.06 z)); Grayson Allen (outside all three projections: ast 3.3 vs 2.5 to 3 (+0.15 z); FG% .416 vs .422 to .433 (-0.11 z)); Naji Marshall (outside all three projections: pts 15 vs 11.4 to 14.1 (+0.17 z); ast 3.3 vs 2.6 to 3.1 (+0.10 z); FG% .497 vs .505 to .506 (-0.14 z); FT% .766 vs .775 to .778 (-0.12 z)); Santi Aldama (gp 68 vs three-season average 56 with a season under 60); Nikola Vucevic (age 36: above the outside average in pts, reb, ast (no decline in the method)); Stephon Castle (outside all three projections: ast 7.4 vs 6.2 to 6.9 (+0.25 z)); Kelly Oubre (outside all three projections: 3PM 1.5 vs 1.2 to 1.3 (+0.21 z)); Rui Hachimura (outside all three projections: FT% .716 vs .728 to .743 (-0.05 z)); Dillon Brooks (outside all three projections: pts 20 vs 15.9 to 18.3 (+0.31 z); TO 1.8 vs 1.3 to 1.5 (-0.38 z)); Max Christie (outside all three projections: reb 3.2 vs 3.4 to 3.6 (-0.08 z); FT% .888 vs .869 to .878 (+0.06 z)); Duncan Robinson (outside all three projections: TO 0.7 vs 0.9 to 1.4 (+0.26 z); FT% .786 vs .798 to .808 (-0.05 z)).

## 4. What you can upload, and what it would settle

Near-certainty is not available for a forecast: a projection is right or wrong in April. What an upload can make near-certain tonight is narrower and still worth having: that every line sits inside the band of independent projections, that minutes and games match what the people closest to each team expect, and that the 18 unanchored lines rest on more than one translation. Each item below names the test it feeds.

| upload | feeds | what it settles |
|---|---|---|
| A fresh RotoBaller projection export, or any third full-stat projection dated this week (Basketball Monster, ESPN, FantasyPros, Hashtag's paid sheet) | T1, the clamp's references | the RotoBaller file on hand is dated 9/29, before camp cuts and the preseason; a current third source tightens the range for all 180 and gives the 24 two-reference players a real band |
| A projected-minutes or depth-chart export per team (RotoWire depth charts, Hashtag's minutes column for the full pool, a Lineups-style minutes sheet) | T4, the team budget | minutes are the largest single lever in every line; an outside minutes sheet for all 180 settles the 35 T4 flags and lets the team budget be read per player, Philadelphia first |
| The latest injury report and games-played projections (Yahoo's projected GP page for the full pool, or Hashtag's) | T4 games | our games are consensus-shaped in aggregate; a full-pool games file closes the 25 injury-history flags one by one |
| A rookie projection source with per-game lines (Hashtag rookie sheet, a draft-guide translation, summer-league and preseason box scores) | the 18 unanchored lines | Keaton Wagler, Collin Murray-Boyles, Dylan Cardwell, Ryan Kalkbrenner, Darius Acuff carry the largest cell-by-cell disagreements with the outside projections among the unanchored lines; two more translations per rookie would say whether ours or the outside's is the outlier |
| Any source that projects decline for players 34 and older (an aging-curve table, or simply a second projection's lines for the 12 named in T6) | T6 | the method carries last season's per-36 forward unchanged; an outside view with decline built in says how much the 12 old lines overstate |
| Your league's final Yahoo draft order and roster settings (already on file for 10/14) and tonight's Yahoo projected-stats paste at the lock | T7, prices | the lock paste re-prices the card; it does not change a line unless you say so (D-1013-1) |

What an upload cannot settle: whether the three outside sources share a blind spot on a roster (a line inside their range is still a guess if they all guessed together), and anything that happens after the draft. Those are bounded below.

## Range check (D-RN-3, without last season as a reference)

The deck's own range check re-run on the live page with no last-season file: 80 of 139 checkable top-150 lines have a category outside all three outside projections, 154 cells; identical to the dial pass's after-run (`range_no_actual_v65.json`). None of the 24 clamped lines is among them. This is not a projection pass, so the owner's D-RN-3 mechanism rule does not apply to this report; the 19 lines the rule flags with last season as a reference carry their mechanisms in `after-report-2026-10-13-dial.md`.

## Watchlist

- The 12 HIGH lines above; none is changed by this report (D-1013-10).
- The 12 players aged 34 and older with no decline in the method (D-1013-11).
- The 18 unanchored lines, 3 with net z beyond 0.5 either way: Ryan Kalkbrenner +0.84, Dylan Cardwell +0.95, Collin Murray-Boyles -0.64 (D-1013-12).
- Philadelphia's pool at 121.4 possessions against 117.7; the usage model is D-C2, after the draft.
- The 10/14 lock paste (D-1013-1) and the publish freeze during the draft (D-1013-5); no RESYNC during the draft (D-1013-2).

## Open-item receipts

| item | query run (2026-10-13) | dated finding |
|---|---|---|
| (this audit) | records only; no web research and no roster pull | the lines audited are the ones merged in kit PR #109 this evening; pull receipts for the window live in `after-report-2026-10-13.md` (the morning's pull), same day |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (`after-report-2026-10-13.md`, receipts dated 10/13) | all HELD or unsigned on 2026-10-13 per those receipts; not re-queried in this audit (did not check) |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 09a889d4baa5), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 25 of 25 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-13.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 5 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Kel'el Ware | 21 of 25 | 26 | 77 | 51 | 51 | 63 | 65 | ft_pct .732 vs .714-.723 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Reed Sheppard | 20 of 25 | 63 | 180 | 56 | 118 | 126 | 129 | tpm 2.8 vs 2.2-2.6 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Ty Jerome | 20 of 25 | 39 | 117 | 48 | 60 | 101 | 71 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 11 of 25 | 70 | 143 | 93 | 121 | 137 | 98 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 7 of 25 | 79 | 183 | 100 | 126 | 148 | 156 | pts 12.7 vs 9.5-11.9; reb 4.1 vs 3.3-3.9; tpm 2.9 vs 2.1-2.7; tov 1.6 vs 1.1-1.4 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Saddiq Bey | 7 of 25 | 90 | 177 | 108 | 132 | 169 | 143 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Dyson Daniels | 6 of 25 | 22 | 62 | 20 | 64 | 56 | 53 | reb 6.8 vs 5.8-6.4; ast 5.9 vs 4.7-5.5; tpm 0.3 vs 0.5-0.6 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Michael Porter Jr. | 5 of 25 | 32 | 60 | 55 | 62 | 70 | 59 | pts 24.5 vs 18.7-21.8; ast 3 vs 2.4-2.6; stl 0.7 vs 0.8-1; tpm 3.4 vs 2.9-3.1; tov 2.3 vs 1.9-2 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (21 mocks, value 6, market 18); Lauri Markkanen (14 mocks, value 21, market 37); VJ Edgecombe (12 mocks, value 58, market 75); Derrick White (10 mocks, value 29, market 45); Tyrese Maxey (7 mocks, value 5, market 9).


## Bounds

**Out of scope by design.**
- No line was changed, built or dry-run; this is the assessment the owner asked for. The option, if asked: a line-by-line review of the 12 HIGH rows with two dated outlets each, the way WO-5 researched its candidates.
- Ranks 181 to 200 of the kit board and the deck-only rows were not audited.
- The tests use the files on hand; no new outside source was fetched.

**In scope and unverified.**
- Whether the three outside sources share a blind spot on a roster: `NOT-ATTEMPTED`; a line inside their range cannot show one.
- The 24 lines with only two outside projections and the 3 with none: their T1 verdicts rest on a narrower or absent band: `ATTEMPTED-FAILED`, no third source on file for them (the RotoBaller file covers 242 names, Hashtag 200, Yahoo 300).
- Whether the clamped and history-shaped lines are closer to what will happen than the outside projections: `UNVERIFIABLE` until games are played; the one-season record (`after-report-2026-10-09-market.md` §4) favours pre-season projections over a copy of the prior season in 8 of 9 categories.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-1013-10 | The 12 HIGH lines: (a) hold for the draft; (b) clamp the ones with two or more outside references to the edge of their range at the lock, the dial method; (c) review line by line with two dated outlets each | (a) for tonight: Jamal Murray, Collin Gillespie sit in the top 100 and the rest sit past rank 100 |
| D-1013-11 | Age decline for the 12 players 34 and older: (a) none, as now; (b) a flat per-36 haircut by age band, after the draft with D-C2 | (b) after the draft |
| D-1013-12 | The 3 unanchored lines beyond 0.5 z net (Ryan Kalkbrenner, Dylan Cardwell, Collin Murray-Boyles): (a) hold; (b) move to the outside average at the lock | (a) |
| D-1013-8, D-1013-9 | Murray and Nesmith just past the cut; Ware LINE QUESTIONED | as set in the dial report |
| D-1013-1..7, D-C2, D-SF-1..4 and earlier | carried | carried |

## Provenance

- Inputs: kit `main` a98a37f (board, lines), deck `main` dd6b719 (page sha256 09a889d4baa5, the z frame), the three projection files and 5 rank files named above, the pinned Basketball-Reference totals.
- Tools: `audit180-2026-10-13/audit180.py` (two runs identical), the deck's `scripts/range_check.py` with no last-season file, the dial pass's `team_budget_after.txt` copied as `team_budget_v65.txt`, `write_audit_report.py` (this file's writer).
- Known-answer checks on the tool: a planted doubling of Holiday's points fires T2 (session record); `reproduce_check.py` confirms the T1 cells and their z equal the deck's own range check cell for cell on every player both records cover.
- No line, tag or placement changed; both planes' hashes equal before and after (e821ec1ddc67 kit, bd2b983876a8 deck).

## In plain language

**Do I agree with the lines?** For the most part, yes. Every line adds up, and every line follows from the player's own last three seasons. 123 of the 180 pass everything or carry one small flag. The method's weakness is the opposite of a transcription error: it trusts last season. Where a player's role is changing, the outside projections see it and the history does not, and that is where my question marks sit.

**Who I have question marks on.** 12 players, listed in §3. In the top 100: Jamal Murray at #7 (ast, 3PM above every outside projection, +0.51 z net); Collin Gillespie at #79 (pts, reb, 3PM above every outside projection, +0.18 z net). Kel'el Ware at #27 is MEDIUM here rather than HIGH only because Hashtag ranks him 51, 24 places from ours, one short of the market test; the repeat-name check still calls his line questioned (D-1013-9). Further down, Bennedict Mathurin (+1.22 z net, 2 outside projections) and Bradley Beal (+1.10 z net, 2 outside projections) carry the largest disagreements on the board. Add the 12 players aged 34 and older, whose lines carry no decline, and the 18 rookies and returners whose lines rest on a translation rather than NBA seasons.

**What to upload.** The single most useful file is a current third projection with full stats (RotoBaller's is two weeks old). After that, a projected-minutes sheet per team, a full-pool games projection, and a rookie projection source. Each closes a named test above. None makes a forecast certain; together they make the lines consensus-checked in every category for every player, which is as far as pre-season certainty goes.

**Your decisions.** D-1013-10 on the HIGH lines tonight; D-1013-11 and D-1013-12 can wait for the lock or the draft's aftermath.
