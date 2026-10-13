# After-report — 2026-10-13 (uploads): the three uploads taken in, and the top-180 audit re-run on five outside projections

**Owner request (2026-10-13 evening):** three uploads with no words, answering the audit report's §4 ("what you can upload"): a RotoBaller 9-cat projected-rankings CSV, a FantasyPros rest-of-season projections CSV, and a pasted set of player cards given with the URL basketballmonster.com/projections.aspx. Then: "Are you able to view and read this link? https://bleacherreport.com/articles/25507731-ranking-99-best-nba-players-ahead-2026-27 — If so, you can also use player role and real life context to integrate to this data projection."

**What was analyzed:** the three uploads, pinned verbatim and joined to the pool under the hard gate; then the same seven tests as `after-report-2026-10-13-audit180.md` on the same 180 lines (`report/top-200-2026-27.md` at kit `main` 7c44327, Version 65's lines) with the outside-projection set widened from three to five. Nothing on either plane changed: both files are byte-identical before and after. References: Yahoo `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, RotoBaller `rotoballer-2026-10-13.csv`, FantasyPros `fantasypros-2026-10-13.csv`, cards `cards-2026-10-13.csv`; history and ranks as in the first audit.

**Method:** A1 to A6 as stated in the first audit, with A3 generalized to the wider set: minutes are questioned 2+ above the three-season high or 4+ beyond every outside minutes projection on the same side (Hashtag, FantasyPros, the cards); games 10+ above the three-season average after a season under 60, or 6+ above every outside games projection (Yahoo, Hashtag, FantasyPros, the cards). The intake assumptions stated before the run: the card paste's origin is recorded as the owner gave it (the URL) with the observed layout (ESPN-style player cards), unconfirmed because the host cannot be reached from here; the RotoBaller file is dated by its upload day; FantasyPros' rest-of-season games are read as full-season games. Tool: `audit180-2026-10-13/audit180_v2.py`; two runs identical.

Pull window: 2026-10-13 → 2026-10-13 (no roster pull; three owner uploads).

**Headline.** With five outside projections instead of three, the question marks shrink and sharpen. 78 of the 180 now have a cell outside every outside projection (was 110), the cells beyond the range carry +19.71 z on the flattering side against -15.12 (was +30.28 / -27.15), and the tiers move from HIGH 12 / MEDIUM 27 / LOW 84 / CLEAN 39 to HIGH 7 / MEDIUM 21 / LOW 69 / CLEAN 65. 149 of the 180 lines now have all five projections and 174 have three or more; 6 still have fewer than three (Miles McBride, Jordan Goodwin, Marcus Smart, Maxime Raynaud, Justin Champagnie, Dylan Cardwell). Two lines that had no second projection before now have one and fail it: Marcus Smart (+1.95 z net) and Deandre Ayton (+1.01). One line left HIGH because it lost a projection, not because it was vindicated: Jordan Goodwin, dropped from the RotoBaller re-export. The RotoBaller upload is the 9/29 projection re-ranked, not a new one: the same stat line on all 238 shared names, 200 ranks moved, 12 names added and 11 dropped (the 9/29 file lists Aaron Gordon twice). 16 of the 18 unanchored lines now have three or more outside projections (was 13); 1 line among them still beyond 0.5 z (Dylan Cardwell +0.95). Minutes and games: over the 174 lines with an outside minutes projection ours sum to 5157 against their average 5162; over the 180 with an outside games projection, 12229 against 12546. The Bleacher Report link cannot be read from this container (DNS fails and the proxy refuses the host, the same wall as every sports host on file); pasted text would be taken in the way the cards were.

## 1. Roster changes

None. No line, tag, placement, games or minutes figure changed on either plane; this is an intake and an assessment.

## 2. The three uploads

EVIDENCE: `report/market/rotoballer-raw-2026-10-13.csv`, `fantasypros-raw-2026-10-13.csv`, `cards-raw-2026-10-13.csv` (raw, verbatim; the card paste transcribed), the joins `rotoballer-2026-10-13.csv`, `fantasypros-2026-10-13.csv`, `cards-2026-10-13.csv` with their `unmatched-` and `disagreements-` files, `provenance.csv`, `check_derived.py` (27 of 27 reproduce at pin d08ac74).

| upload | what it is | rows | joined | without a pool row | note |
|---|---|---|---|---|---|
| RotoBaller overall 9-cat projected rankings | the owner's re-export of the file pinned 9/29 | 250 | 243 | 7: Leonard Miller, Nate Ament, Sergio De Larrea, Moussa Cisse, Hugo Gonzalez, Carter Bryant, Danny Wolf | the same stat line as 9/29 on all 238 shared names; 200 of 238 ranks moved; added Kyshawn George, Jaxson Hayes, Yves Missi, Quentin Grimes, Ben Simmons, Ryan Kalkbrenner, Leonard Miller, Precious Achiuwa, Marcus Smart, Ziaire Williams, Aaron Wiggins, Noah Clowney; dropped Jusuf Nurkic, Kristaps Porzingis, Brandon Ingram, Will Riley, Taylor Hendricks, De'Andre Hunter, Kyle Kuzma, Jimmy Butler III, Donte DiVincenzo, Jordan Goodwin, Goga Bitadze. It is a fourth ranking of the same projection, not a fresh projection |
| FantasyPros rest-of-season projections | a full 9-cat line with games and minutes | 322 (57 with no projection, all zeros, left out) | 250 | 15: Danny Wolf, Nate Ament, Tristan Vukcevic, Patrick Williams, Grant Williams, Matisse Thybulle, Trayce Jackson-Davis, Kyle Anderson, Thomas Bryant, Jarred Vanderbilt, Kevon Looney, Jericho Sims, Steven Adams, Jonathan Isaac, Jonathan Mogbo | one new alias: Ron Holland = Ronald Holland II (verified: DET on both). Team codes NOR/PHO/UTH mapped. Covers rookies |
| The card paste | one card per player: last season's line, a 2027 projection with games and minutes, an outlook paragraph | 200 cards (4 with no 2027 line: Russell Westbrook, Cam Spencer, Vince Williams Jr., Gary Payton II) | 195 | 1: Danny Wolf | the 2027 projection rows transcribed; assists over turnovers reproduces the pasted A/TO within 0.06 on every projected row (0 mismatches). Origin: given with the Basketball Monster URL; the layout (Headshot, Day-To-Day and Out tags, 2026 STATISTICS / 2027 PROJECTIONS / 2027 Outlook) matches ESPN's player pages. `UNVERIFIABLE` from here: basketballmonster.com does not resolve (ENOTFOUND). The outlook prose was read in-session and not stored |

The Bleacher Report article: `ATTEMPTED-FAILED`. The fetch fails at DNS (ENOTFOUND bleacherreport.com) and a direct request through the session proxy is refused (CONNECT 403), the same wall recorded for 17 sports hosts at the actuals intake on 10/09. If the owner pastes the article, it goes in as a role-context source the way the RotoWire panel and the profiles pieces did: names, ranks and the role or health words kept verbatim, joined under the hard gate, used as leads for the per-line reading, never as a line edit.

## 3. The verdict, test by test, three references against five

EVIDENCE: `audit180-2026-10-13/audit180.json` (three references), `audit180_v2.json` (five), `audit180_v2.txt`.

| test | fired, 3 refs | fired, 5 refs | reading on five |
|---|---|---|---|
| T1 outside range | 110 | 78 | 161 cells (was 255), +19.71 z flattering against -15.12; 7 lines over 0.5 z net (was 13): Marcus Smart +1.95, Bradley Beal +1.03, Deandre Ayton +1.01, Sandro Mamukelashvili -1.00, Dylan Cardwell +0.95, Aaron Nesmith -0.53, Jamal Murray +0.51. Lines per reference count: five 149, four 19, three 6, two 5, one 1 |
| T2 own history | 0 | 0 | unchanged by construction |
| T3 career shooting | 1 | 1 | Ja Morant's FT% .845 against his career band, as before |
| T4 minutes and games | 35 | 30 | 25 games flags rest on injury history; 3 lines sit 6+ games above every outside games projection (Miles McBride, Jordan Goodwin, Justin Champagnie); 3 minutes flags against the career high (Kel'el Ware, Ty Jerome, Naz Reid); 2 lines 4+ minutes beyond every outside minutes projection (Bradley Beal mpg 32.1 vs outside 27.5/23.9 (Hashtag/FantasyPros), Ja Morant mpg 25.5 vs outside 30.4/29.5/29.5 (Hashtag/FantasyPros/cards)). Aggregate minutes 5157 against 5162 over 174; games 12229 against 12546 over 180 |
| T5 points identity | 0 | 0 | every line reconciles |
| T6 age | 12 | 7 | 7 players 34 and older above the five-source average in two or more of points, rebounds and assists: Kawhi Leonard (35), Kevin Durant (38), LeBron James (42), Rudy Gobert (34), Jrue Holiday (36), Al Horford (40), T.J. McConnell (34). Kyrie Irving, Paul George, Damian Lillard, Tobias Harris, Nikola Vucevic no longer sit above the five-source average in two of the three; the method still carries no decline |
| T7 market | 15 | 15 | the same 15 names (RotoBaller's re-ranking moves no verdict): high on 10, low on 5 |
| team budget | 6 teams | 6 teams | unchanged: the lines did not move; Philadelphia 121.4 against 117.7 |

Tiers on five references: HIGH 7, MEDIUM 21, LOW 69, UNANCHORED 18, CLEAN 65. 45 lines changed tier: 43 down and 2 up.

### Lines that changed tier

| rank | player | 3 refs | 5 refs | net z before | net z after | why |
|---|---|---|---|---|---|---|
| 17 | Amen Thompson | LOW | CLEAN | -0.11 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 20 | Domantas Sabonis | MEDIUM | LOW | +0.21 | +0.21 | no longer T4 |
| 26 | Bam Adebayo | LOW | CLEAN | +0.06 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 27 | Kel'el Ware | MEDIUM | LOW | +0.04 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 30 | Austin Reaves | LOW | CLEAN | +0.14 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 33 | Onyeka Okongwu | LOW | CLEAN | +0.10 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 34 | Kyrie Irving | LOW | CLEAN | +0.00 | +0.00 | no longer T6 |
| 38 | Paul George | LOW | CLEAN | +0.00 | +0.00 | no longer T6 |
| 50 | OG Anunoby | LOW | CLEAN | -0.26 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 51 | LaMelo Ball | LOW | CLEAN | +0.07 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 55 | Damian Lillard | LOW | CLEAN | +0.00 | +0.00 | no longer T6 |
| 58 | Josh Giddey | LOW | CLEAN | -0.11 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 63 | Reed Sheppard | MEDIUM | LOW | +0.21 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 73 | Jaden McDaniels | LOW | CLEAN | -0.25 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 75 | Keegan Murray | LOW | CLEAN | -0.17 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 76 | Payton Pritchard | LOW | CLEAN | -0.40 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 81 | Ayo Dosunmu | LOW | CLEAN | +0.21 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 82 | Norman Powell | LOW | CLEAN | +0.22 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 88 | Josh Hart | LOW | CLEAN | -0.34 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 94 | Matas Buzelis | LOW | CLEAN | -0.18 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 96 | Myles Turner | LOW | CLEAN | -0.06 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 101 | Cason Wallace | LOW | CLEAN | -0.09 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 104 | Peyton Watson | LOW | CLEAN | +0.20 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 111 | Isaiah Hartenstein | LOW | CLEAN | -0.08 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 112 | Deandre Ayton | CLEAN | HIGH | +0.00 | +1.01 | gained a second outside projection (now 3); the range test ran for the first time |
| 118 | Kyshawn George | MEDIUM | LOW | +0.25 | +0.00 | inside the five-source band (the three-source band was narrower); 2 to 5 projections |
| 122 | Cam Johnson | MEDIUM | LOW | -0.12 | -0.22 | no longer T4 |
| 128 | Bobby Portis | LOW | CLEAN | +0.08 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 131 | Moussa Diabate | LOW | CLEAN | +0.06 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 134 | Grayson Allen | LOW | CLEAN | +0.04 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 136 | Tobias Harris | MEDIUM | LOW | -0.04 | -0.04 | no longer T6 |
| 146 | Mitchell Robinson | MEDIUM | LOW | +0.04 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 153 | Jaylon Tyson | HIGH | LOW | +0.74 | +0.00 | inside the five-source band (the three-source band was narrower); 2 to 4 projections |
| 155 | Jordan Goodwin | HIGH | LOW | +0.57 | +0.00 | lost its second outside projection (now 1: Yahoo); the range test cannot run |
| 157 | Nikola Vucevic | LOW | CLEAN | +0.00 | +0.00 | no longer T6 |
| 158 | Kyle Filipowski | HIGH | LOW | +0.77 | +0.44 | band widened: net z +0.77 to +0.44 |
| 159 | Marcus Smart | CLEAN | HIGH | +0.00 | +1.95 | gained a second outside projection (now 2); the range test ran for the first time |
| 162 | Stephon Castle | LOW | CLEAN | +0.25 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 165 | Quentin Grimes | HIGH | LOW | -0.69 | +0.14 | band widened: net z -0.69 to +0.14 |
| 166 | Rui Hachimura | LOW | CLEAN | -0.05 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 167 | Al Horford | HIGH | MEDIUM | +0.47 | +0.34 | band widened: net z +0.47 to +0.34 |
| 168 | Bennedict Mathurin | HIGH | LOW | +1.22 | +0.09 | band widened: net z +1.22 to +0.09 |
| 174 | T.J. McConnell | HIGH | MEDIUM | +0.52 | +0.04 | band widened: net z +0.52 to +0.04 |
| 177 | Max Christie | LOW | CLEAN | -0.02 | +0.00 | inside the five-source band (the three-source band was narrower); 3 to 5 projections |
| 178 | Bilal Coulibaly | MEDIUM | LOW | +0.18 | +0.18 | no longer T4 |

## 4. The question marks on five references

EVIDENCE: `audit180_v2.json`; z figures in the deck's own frame, flattering positive.

### HIGH

| rank | player | age | refs | net z | why |
|---|---|---|---|---|---|
| 7 | Jamal Murray (DEN) | 29 | 5 | +0.51 | outside all 5 outside projections: ast 7.1 vs 6.3 to 6.7 (+0.20 z); 3PM 3.3 vs 2.6 to 3 (+0.31 z) |
| 79 | Collin Gillespie (PHX) | 27 | 5 | +0.18 | outside all 5 outside projections: pts 12.7 vs 9.5 to 11.9 (+0.15 z); reb 4.1 vs 3.3 to 3.9 (+0.08 z); 3PM 2.9 vs 2.1 to 2.7 (+0.21 z); TO 1.6 vs 1.1 to 1.4 (-0.26 z); gp 75 vs three-season average 56 with a season under 60; every outside rank 25+ places below ours (we are high): Yahoo 116, Hashtag 126, RotoBaller 155, RotoWire 135, Rotoworld 148 |
| 103 | Bradley Beal (LAC) | 33 | 3 | +1.03 | outside all 3 outside projections: pts 16.7 vs 9.8 to 13.9 (+0.52 z); reb 3.3 vs 2 to 2.8 (+0.21 z); ast 3.7 vs 2.3 to 3 (+0.35 z); 3PM 1.9 vs 1.1 to 1.7 (+0.21 z); TO 1.9 vs 1.2 to 1.7 (-0.26 z); mpg 32.1 vs outside 27.5/23.9 (Hashtag/FantasyPros) |
| 112 | Deandre Ayton (WAS) | 28 | 3 | +1.01 | outside all 3 outside projections: pts 12.1 vs 9.4 to 11.5 (+0.11 z); reb 8 vs 6.9 to 7.6 (+0.16 z); blk 0.9 vs 0.7 to 0.7 (+0.39 z); FG% .647 vs .592 to .621 (+0.35 z) |
| 149 | Aaron Nesmith (IND) | 27 | 5 | -0.53 | outside all 5 outside projections: FG% .427 vs .450 to .474 (-0.42 z); FT% .829 vs .843 to .862 (-0.11 z); gp 68 vs three-season average 54 with a season under 60 |
| 154 | Sandro Mamukelashvili (LAL) | 27 | 3 | -1.00 | outside all 3 outside projections: pts 11 vs 12 to 13.7 (-0.18 z); reb 4.9 vs 5.6 to 6.2 (-0.29 z); stl 0.7 vs 0.8 to 0.9 (-0.32 z); 3PM 1.4 vs 1.6 to 1.9 (-0.21 z); gp 74 vs three-season average 62 with a season under 60 |
| 159 | Marcus Smart (HOU) | 32 | 2 | +1.95 | outside all 2 outside projections: pts 9.3 vs 7.8 to 7.8 (+0.28 z); reb 2.8 vs 2.1 to 2.3 (+0.21 z); ast 3 vs 2.5 to 2.7 (+0.15 z); stl 1.5 vs 0.6 to 1.1 (+1.26 z); 3PM 1.6 vs 1.2 to 1.3 (+0.31 z); TO 1.5 vs 1.1 to 1.3 (-0.26 z) |

### MEDIUM

| rank | player | age | refs | net z | why |
|---|---|---|---|---|---|
| 14 | Kevin Durant (HOU) | 38 | 5 | +0.19 | outside all 5 outside projections: ast 4.8 vs 3.8 to 4.4 (+0.20 z); TO 3.2 vs 2.9 to 3 (-0.26 z); FT% .876 vs .859 to .863 (+0.25 z); age 38: above the outside average in pts, reb, ast (no decline in the method) |
| 23 | Dyson Daniels (ATL) | 23 | 5 | +0.05 | outside all 5 outside projections: ast 5.9 vs 4.7 to 5.6 (+0.15 z); 3PM 0.3 vs 0.4 to 0.6 (-0.10 z); every outside rank 25+ places below ours (we are high): Yahoo 62, Hashtag 64, RotoBaller 55, RotoWire 69, Rotoworld 56 |
| 32 | Franz Wagner (ORL) | 25 | 5 | -0.31 | outside all 5 outside projections: reb 6 vs 5.4 to 5.7 (+0.12 z); ast 3.8 vs 4.1 to 4.3 (-0.15 z); FT% .832 vs .845 to .852 (-0.28 z); gp 66 vs three-season average 55 with a season under 60 |
| 42 | Jalen Williams (OKC) | 25 | 5 | +0.02 | outside all 5 outside projections: ast 6 vs 5 to 5.3 (+0.35 z); 3PM 0.8 vs 1.3 to 1.5 (-0.51 z); FT% .828 vs .805 to .815 (+0.18 z); gp 68 vs three-season average 58 with a season under 60 |
| 52 | Naz Reid (CHA) | 27 | 5 | -0.04 | outside all 5 outside projections: FT% .731 vs .737 to .756 (-0.04 z); mpg 31 vs three-season high 27.5 |
| 64 | Tyler Herro (MIL) | 27 | 5 | -0.28 | outside all 5 outside projections: ast 4.1 vs 4.6 to 4.9 (-0.25 z); 3PM 2.5 vs 2.9 to 3.2 (-0.41 z); TO 1.9 vs 2.2 to 2.3 (+0.38 z); gp 70 vs three-season average 51 with a season under 60 |
| 68 | Kristaps Porzingis (GSW) | 31 | 4 | +0.00 | gp 54 vs three-season average 44 with a season under 60; every outside rank 25+ places below ours (we are high): Yahoo 154, Hashtag 96, RotoWire 128, Rotoworld 115 |
| 83 | Neemias Queta (BOS) | 27 | 5 | -0.04 | outside all 5 outside projections: FT% .704 vs .709 to .719 (-0.04 z); gp 68 vs three-season average 55 with a season under 60 |
| 107 | Rudy Gobert (MIN) | 34 | 5 | -0.27 | outside all 5 outside projections: FT% .562 vs .583 to .599 (-0.27 z); age 34: above the outside average in reb, ast (no decline in the method) |
| 110 | Julian Champagnie (SAS) | 25 | 5 | +0.12 | outside all 5 outside projections: reb 5.8 vs 4.4 to 5.4 (+0.16 z); FT% .847 vs .855 to .870 (-0.04 z); every outside rank 25+ places below ours (we are high): Yahoo 173, Hashtag 165, RotoBaller 188, Rotoworld 194 |
| 113 | Zion Williamson (NOP) | 26 | 5 | +0.08 | outside all 5 outside projections: ast 3.2 vs 3.9 to 4.3 (-0.35 z); TO 2 vs 2.2 to 2.5 (+0.26 z); FT% .709 vs .696 to .702 (+0.17 z); every outside rank 25+ places above ours (we are low): Yahoo 81, Hashtag 78, RotoBaller 78, RotoWire 82, Rotoworld 71 |
| 115 | Cam Spencer (MEM) | 26 | 3 | +0.22 | outside all 3 outside projections: ast 5.6 vs 3 to 5.3 (+0.15 z); FG% .471 vs .452 to .465 (+0.07 z); gp 68 vs three-season average 48 with a season under 60 |
| 126 | Kris Dunn (LAC) | 32 | 4 | -0.03 | outside all 4 outside projections: pts 7.1 vs 5.6 to 6.6 (+0.09 z); ast 3.6 vs 2.7 to 3.2 (+0.20 z); TO 1.4 vs 1 to 1.1 (-0.38 z); FT% .757 vs .731 to .739 (+0.06 z); every outside rank 25+ places below ours (we are high): Yahoo 189, Hashtag 193, Rotoworld 184 |
| 133 | Ja Morant (POR) | 27 | 5 | +0.00 | FT% .845 outside his career band .728 to .824; mpg 25.5 vs outside 30.4/29.5/29.5 (Hashtag/FantasyPros/cards) |
| 142 | Coby White (CHA) | 26 | 5 | -0.24 | outside all 5 outside projections: FT% .830 vs .843 to .864 (-0.24 z); every outside rank 25+ places above ours (we are low): Yahoo 86, Hashtag 86, RotoBaller 96, RotoWire 68, Rotoworld 76 |
| 147 | Luke Kornet (SAS) | 31 | 4 | -0.11 | outside all 4 outside projections: reb 6.1 vs 4.1 to 5.8 (+0.12 z); FG% .613 vs .655 to .662 (-0.27 z); FT% .812 vs .765 to .804 (+0.04 z); every outside rank 25+ places below ours (we are high): Yahoo 254, Hashtag 189, RotoBaller 214 |
| 152 | Miles McBride (NYK) | 26 | 2 | +0.40 | outside all 2 outside projections: pts 11.9 vs 9.1 to 10.9 (+0.18 z); 3PM 2.7 vs 2 to 2.3 (+0.41 z); TO 0.8 vs 0.6 to 0.7 (-0.13 z); FT% .785 vs .803 to .803 (-0.06 z); gp 72 vs three-season average 58 with a season under 60; gp 72 vs outside 66 (Yahoo) |
| 160 | Derrick Jones Jr (LAC) | 29 | 4 | +0.15 | outside all 4 outside projections: ast 1.4 vs 1 to 1.1 (+0.15 z); every outside rank 25+ places below ours (we are high): Yahoo 223, Hashtag 199, RotoBaller 187 |
| 163 | Justin Champagnie (WAS) | 25 | 2 | +0.30 | outside all 2 outside projections: pts 8.6 vs 7.6 to 8.1 (+0.09 z); reb 5.6 vs 4.9 to 5.2 (+0.16 z); FT% .776 vs .754 to .766 (+0.05 z); gp 73 vs three-season average 56 with a season under 60; gp 73 vs outside 58 (Yahoo) |
| 167 | Al Horford (GSW) | 40 | 3 | +0.34 | outside all 3 outside projections: pts 8.6 vs 5.8 to 8.1 (+0.09 z); ast 2.6 vs 1.6 to 2.3 (+0.15 z); FG% .453 vs .435 to .438 (+0.17 z); FT% .819 vs .857 to .885 (-0.07 z); age 40: above the outside average in pts, reb, ast (no decline in the method) |
| 174 | T.J. McConnell (IND) | 34 | 4 | +0.04 | outside all 4 outside projections: FT% .836 vs .767 to .814 (+0.04 z); age 34: above the outside average in pts, ast (no decline in the method) |

### UNANCHORED (fewer than two NBA seasons of 25+ games), now with the outside projections that cover them

| rank | player | NBA seasons on file | refs | net z | what the outside projections say |
|---|---|---|---|---|---|
| 41 | Cooper Flagg (DAL) | 2025-26 | 5 | -0.41 | outside all 5 outside projections: pts 21 vs 22.4 to 25.3 (-0.26 z); ast 4.5 vs 4.8 to 5.1 (-0.15 z) |
| 44 | Cameron Boozer (MEM) | none | 5 | +0.00 | inside every outside projection |
| 53 | Zach Edey (MEM) | 2024-25 | 5 | +0.00 | inside every outside projection |
| 59 | VJ Edgecombe (PHI) | 2025-26 | 5 | +0.00 | inside every outside projection |
| 66 | Kon Knueppel (CHA) | 2025-26 | 5 | +0.00 | inside every outside projection |
| 72 | Yaxel Lendeborg (GSW) | none | 5 | +0.00 | inside every outside projection |
| 92 | Caleb Wilson (CHI) | none | 5 | +0.00 | inside every outside projection |
| 109 | Darryn Peterson (UTA) | none | 5 | +0.00 | inside every outside projection |
| 135 | Derik Queen (NOP) | 2025-26 | 5 | +0.00 | inside every outside projection |
| 140 | AJ Dybantsa (WAS) | none | 4 | -0.28 | outside all 4 outside projections: FG% .450 vs .462 to .478 (-0.28 z); every outside rank 25+ places above ours (we are low): Yahoo 93, RotoBaller 104, RotoWire 101, Rotoworld 89 |
| 144 | Ryan Kalkbrenner (CHA) | 2025-26 | 5 | +0.00 | every outside rank 25+ places below ours (we are high): Yahoo 246, Hashtag 188, RotoBaller 185 |
| 145 | Scotty Pippen Jr. (MEM) | 2024-25 | 5 | +0.00 | inside every outside projection |
| 156 | Cedric Coward (MEM) | 2025-26 | 5 | +0.00 | every outside rank 25+ places above ours (we are low): Yahoo 75, Hashtag 117, RotoBaller 98, RotoWire 90, Rotoworld 117 |
| 161 | Maxime Raynaud (SAC) | 2025-26 | 2 | +0.00 | inside every outside projection |
| 170 | Dylan Cardwell (SAC) | 2025-26 | 2 | +0.95 | outside all 2 outside projections: pts 5.4 vs 3.1 to 4.7 (+0.13 z); reb 7.5 vs 4.3 to 6.7 (+0.33 z); ast 1.4 vs 0.8 to 1.2 (+0.10 z); blk 1.5 vs 0.9 to 1.3 (+0.39 z) |
| 171 | Keaton Wagler (LAC) | none | 3 | +0.34 | outside all 3 outside projections: pts 16.5 vs 11.6 to 14.3 (+0.41 z); 3PM 2.3 vs 1.4 to 1.5 (+0.82 z); TO 2.4 vs 1.5 to 2.2 (-0.26 z); FG% .430 vs .462 to .508 (-0.70 z); FT% .820 vs .697 to .814 (+0.07 z) |
| 173 | Darius Acuff (SAC) | none | 5 | +0.00 | inside every outside projection |
| 175 | Collin Murray-Boyles (TOR) | 2025-26 | 5 | +0.00 | every outside rank 25+ places above ours (we are low): Yahoo 102, Hashtag 108, RotoBaller 90, RotoWire 109, Rotoworld 88 |

### LOW (one small flag each; I agree with these lines)

Nikola Jokic (outside all 5 outside projections: TO 3.7 vs 3.3 to 3.5 (-0.26 z); FT% .829 vs .816 to .822 (+0.17 z)); Shai Gilgeous-Alexander (outside all 5 outside projections: FT% .874 vs .883 to .889 (-0.26 z)); Victor Wembanyama (outside all 5 outside projections: ast 3.1 vs 3.3 to 3.6 (-0.10 z); TO 2.4 vs 2.6 to 2.9 (+0.26 z)); Luka Doncic (outside all 5 outside projections: FT% .772 vs .781 to .785 (-0.30 z)); Kawhi Leonard (age 35: above the outside average in reb, ast (no decline in the method)); Donovan Mitchell (outside all 5 outside projections: TO 2.8 vs 2.6 to 2.6 (-0.26 z)); Stephen Curry (outside all 5 outside projections: ast 4.7 vs 5 to 5.3 (-0.15 z); FG% .469 vs .451 to .459 (+0.30 z)); Tyrese Haliburton (outside all 5 outside projections: TO 1.5 vs 1.7 to 1.9 (+0.26 z)); Trey Murphy III (gp 70 vs three-season average 59 with a season under 60); Jalen Johnson (gp 65 vs three-season average 55 with a season under 60); Chet Holmgren (outside all 5 outside projections: FG% .549 vs .533 to .538 (+0.20 z)); Scottie Barnes (outside all 5 outside projections: FG% .496 vs .477 to .486 (+0.23 z); FT% .801 vs .784 to .793 (+0.10 z)); Domantas Sabonis (outside all 5 outside projections: 3PM 0.9 vs 0.6 to 0.7 (+0.21 z)); Lauri Markkanen (gp 66 vs three-season average 48 with a season under 60); Cade Cunningham (outside all 5 outside projections: blk 0.7 vs 0.8 to 0.8 (-0.20 z)); Kel'el Ware (mpg 26.8 vs three-season high 22.2); Derrick White (outside all 5 outside projections: 3PM 2.7 vs 2.9 to 3.1 (-0.21 z)); Michael Porter Jr (outside all 5 outside projections: stl 0.7 vs 0.8 to 1 (-0.32 z)); Evan Mobley (gp 74 vs three-season average 62 with a season under 60); Giannis Antetokounmpo (outside all 5 outside projections: FG% .600 vs .606 to .624 (-0.18 z); FT% .664 vs .628 to .650 (+0.51 z)); Jalen Duren (outside all 5 outside projections: ast 2 vs 2.3 to 2.5 (-0.15 z); stl 0.7 vs 0.8 to 0.9 (-0.32 z)); Ty Jerome (mpg 27.6 vs three-season high 19.9); Nickeil Alexander-Walker (outside all 5 outside projections: 3PM 3.2 vs 2.6 to 3 (+0.21 z); TO 2.1 vs 1.7 to 1.9 (-0.26 z)); Devin Booker (outside all 5 outside projections: FT% .873 vs .879 to .884 (-0.16 z)); Alperen Sengun (outside all 5 outside projections: TO 3.2 vs 2.9 to 3 (-0.26 z)); LeBron James (age 42: above the outside average in pts, ast (no decline in the method)); Darius Garland (gp 70 vs three-season average 59 with a season under 60); De'Aaron Fox (outside all 5 outside projections: FT% .756 vs .772 to .799 (-0.18 z)); Reed Sheppard (every outside rank 25+ places below ours (we are high): Yahoo 141, Hashtag 118, RotoBaller 129, RotoWire 136, Rotoworld 126); Mikal Bridges (outside all 5 outside projections: TO 1 vs 1.2 to 1.3 (+0.26 z)); Jalen Suggs (outside all 5 outside projections: ast 5.5 vs 4 to 5 (+0.25 z)); Brandon Miller (outside all 5 outside projections: 3PM 3.1 vs 3.4 to 3.5 (-0.31 z)); John Collins (outside all 5 outside projections: FG% .550 vs .539 to .542 (+0.14 z); FT% .774 vs .796 to .810 (-0.18 z)); Jarrett Allen (outside all 5 outside projections: FG% .639 vs .656 to .676 (-0.26 z)); Brandon Ingram (outside all 4 outside projections: TO 2.4 vs 2.6 to 2.8 (+0.26 z)); Ivica Zubac (outside all 5 outside projections: TO 1.8 vs 1.5 to 1.6 (-0.26 z); FG% .603 vs .615 to .629 (-0.19 z); FT% .716 vs .678 to .700 (+0.16 z)); Tre Jones (outside all 5 outside projections: pts 13.7 vs 9.3 to 12.3 (+0.26 z)); Saddiq Bey (every outside rank 25+ places below ours (we are high): Yahoo 151, Hashtag 132, RotoBaller 157, RotoWire 131, Rotoworld 169); Jabari Smith Jr (outside all 5 outside projections: ast 1.9 vs 1.5 to 1.7 (+0.10 z)); Tari Eason (outside all 5 outside projections: 3PM 1.6 vs 1.2 to 1.4 (+0.21 z)); Miles Bridges (outside all 5 outside projections: FT% .823 vs .838 to .846 (-0.16 z)); Toumani Camara (outside all 5 outside projections: pts 13.5 vs 10.7 to 12.6 (+0.17 z); 3PM 2.7 vs 1.8 to 2.3 (+0.41 z); TO 1.8 vs 1.4 to 1.6 (-0.26 z)); Alex Sarr (gp 72 vs three-season average 58 with a season under 60); Ajay Mitchell (gp 68 vs three-season average 46 with a season under 60); Jakob Poeltl (outside all 5 outside projections: FG% .679 vs .653 to .668 (+0.12 z); FT% .588 vs .612 to .642 (-0.16 z)); Robert Williams III (outside all 5 outside projections: FG% .712 vs .686 to .697 (+0.10 z); FT% .618 vs .651 to .692 (-0.11 z)); Zach LaVine (gp 64 vs three-season average 46 with a season under 60); Kyshawn George (gp 68 vs three-season average 58 with a season under 60); Christian Braun (outside all 4 outside projections: FG% .522 vs .531 to .560 (-0.13 z); FT% .774 vs .786 to .815 (-0.09 z)); Paolo Banchero (outside all 5 outside projections: pts 22 vs 23.4 to 24.3 (-0.26 z); 3PM 1.2 vs 1.4 to 1.5 (-0.21 z); FT% .764 vs .748 to .756 (+0.21 z)); CJ McCollum (outside all 5 outside projections: FT% .780 vs .749 to .770 (+0.10 z)); Cam Johnson (outside all 5 outside projections: pts 12.1 vs 12.9 to 15.6 (-0.15 z); FT% .843 vs .853 to .875 (-0.07 z)); Aaron Gordon (gp 66 vs three-season average 53 with a season under 60); Jrue Holiday (age 36: above the outside average in pts, reb, ast (no decline in the method)); Wendell Carter Jr (outside all 4 outside projections: FG% .511 vs .490 to .504 (+0.09 z); FT% .775 vs .754 to .768 (+0.07 z)); Nic Claxton (outside all 5 outside projections: ast 3.7 vs 3.1 to 3.5 (+0.10 z)); Tobias Harris (outside all 5 outside projections: FT% .857 vs .863 to .869 (-0.04 z)); Mitchell Robinson (gp 64 vs three-season average 50 with a season under 60); Naji Marshall (outside all 4 outside projections: pts 15 vs 10.7 to 14.1 (+0.17 z); ast 3.3 vs 2.5 to 3.1 (+0.10 z); FG% .497 vs .505 to .508 (-0.14 z); FT% .766 vs .775 to .778 (-0.12 z)); Santi Aldama (gp 68 vs three-season average 56 with a season under 60); Jaylon Tyson (gp 72 vs three-season average 56 with a season under 60); Jordan Goodwin (gp 75 vs three-season average 52 with a season under 60; gp 75 vs outside 65 (Yahoo)); Kyle Filipowski (outside all 4 outside projections: pts 11.4 vs 9.2 to 10.7 (+0.13 z); reb 7.2 vs 5.7 to 6.7 (+0.21 z); ast 2.6 vs 2.1 to 2.4 (+0.10 z)); Kelly Oubre (outside all 4 outside projections: 3PM 1.5 vs 1.1 to 1.3 (+0.21 z)); Quentin Grimes (outside all 5 outside projections: FT% .824 vs .799 to .811 (+0.14 z)); Bennedict Mathurin (outside all 4 outside projections: pts 17.6 vs 11.2 to 16.5 (+0.20 z); reb 5.4 vs 3.5 to 5.1 (+0.12 z); ast 2.4 vs 1.4 to 2.1 (+0.15 z); TO 2.2 vs 1.3 to 2 (-0.26 z); FG% .434 vs .440 to .443 (-0.12 z)); Dillon Brooks (outside all 5 outside projections: pts 20 vs 15.9 to 18.6 (+0.26 z); TO 1.8 vs 1.3 to 1.6 (-0.26 z)); Bilal Coulibaly (outside all 4 outside projections: pts 11.7 vs 9.3 to 10.7 (+0.18 z)); Duncan Robinson (outside all 5 outside projections: TO 0.7 vs 0.8 to 1.4 (+0.13 z)).

## 5. What is still missing

| gap | who | what would close it |
|---|---|---|
| fewer than three outside projections | Miles McBride (2: RotoBaller, Yahoo), Jordan Goodwin (1: Yahoo), Marcus Smart (2: RotoBaller, Yahoo), Maxime Raynaud (2: RotoBaller, Yahoo), Justin Champagnie (2: RotoBaller, Yahoo), Dylan Cardwell (2: RotoBaller, Yahoo) | Hashtag's full-pool sheet (its file stops at 200), or any deep projection that reaches the bench; Goodwin and Smart are the two whose verdicts depend on it |
| age decline | the 7 players 34 and older in T6 | still no source with decline built in; the five projections' average is the only outside view, and it sits below our line for these 7 |
| role and real-life context | every HIGH and MEDIUM line | the Bleacher Report article as a paste, or any dated depth-chart page; used as leads per line, not as edits |
| a projection with a stated date | the RotoBaller re-export | the file carries no date and its lines equal the 9/29 file; a dated export would say whether RotoBaller has updated since camp |
| the team budget per player | Philadelphia first | an outside minutes sheet now exists for 174 of the 180 (FantasyPros and the cards); reading the budget per player against it is a build step, after the draft with D-C2 |

## Range check (D-RN-3, without last season as a reference)

The deck's own range check still reads its three sources (Yahoo, Hashtag, the newest RotoBaller file). Re-run here with the 10/13 RotoBaller file in place of 9/29 (`range_no_actual_rb1013.json`, no deck change): 80 of 139 checkable top-150 lines, 156 cells, against 80 and 154 on the dial pass's after-run (`range_no_actual_v65.json`); the lines are the same, so the only movement is in who has a third reference: Ryan Kalkbrenner now flagged (added to the RotoBaller file), Brandon Ingram no longer (dropped from it). The next build's gate sees the same. Adding FantasyPros and the cards to the deck's range check is a deck change and the owner's call (D-1013-14 below). This is not a projection pass, so the D-RN-3 mechanism rule does not apply to this report.

## Watchlist

- The 7 HIGH lines on five references (§4); none is changed by this report (D-1013-10, re-put).
- Marcus Smart and Deandre Ayton, question marks for the first time now that a second projection covers them (D-1013-13).
- The 7 players aged 34 and older with no decline in the method (D-1013-11).
- The 18 unanchored lines, 1 line beyond 0.5 z: Dylan Cardwell +0.95 (D-1013-12, re-put).
- Philadelphia's pool at 121.4 possessions against 117.7; the usage model is D-C2, after the draft.
- The 10/14 lock paste (D-1013-1) and the publish freeze during the draft (D-1013-5); no RESYNC during the draft (D-1013-2).

## Open-item receipts

| item | query run (2026-10-13) | dated finding |
|---|---|---|
| (this intake) | no web research and no roster pull; the Bleacher Report fetch attempted and refused (ENOTFOUND; proxy CONNECT 403) | the uploads are the owner's files of 2026-10-13; the lines audited are the ones merged in kit PR #109 |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (`after-report-2026-10-13.md`, receipts dated 10/13) | all HELD or unsigned on 2026-10-13 per those receipts; not re-queried here (did not check). The card paste tags Ingram Out and Porzingis Day-To-Day, consistent with those receipts |

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
- No line was changed, built or dry-run. The option, if asked: the HIGH lines clamped to the edge of the five-source range at the lock, the dial method, or a line-by-line review with two dated outlets each.
- The deck's range check was not changed; it still reads three sources (D-1013-14).
- The card paste's 2026 statistics rows and outlook paragraphs were not transcribed; the outlooks were read in-session as role context and are not evidence here.
- Ranks 181 to 200 and the deck-only rows were not audited.

**In scope and unverified.**
- The card paste's origin: `UNVERIFIABLE` from this container (basketballmonster.com ENOTFOUND); recorded as the owner gave it with the observed layout.
- The RotoBaller re-export's date: `UNVERIFIABLE`, the file carries none; its lines equal the 9/29 file, which is the fact that matters for the audit.
- The 6 lines with fewer than three projections: their T1 verdicts rest on a narrow or absent band: `ATTEMPTED-FAILED`, no deeper source on file (Hashtag's file stops at 200, the cards at 200, FantasyPros' projected rows at 265, RotoBaller at 250).
- Whether five sources share a blind spot on a roster: `NOT-ATTEMPTED`; a line inside their range cannot show one.
- Whether the clamped and history-shaped lines are closer to what will happen than the outside projections: `UNVERIFIABLE` until games are played.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-1013-10 (re-put) | The 7 HIGH lines on five references (Jamal Murray, Collin Gillespie, Bradley Beal, Deandre Ayton, Aaron Nesmith, Sandro Mamukelashvili, Marcus Smart): (a) hold for the draft; (b) clamp the ones with three or more references to the edge of the five-source range at the lock; (c) review line by line with two dated outlets each | (a) for tonight; only Jamal Murray and Collin Gillespie sit in the top 100 |
| D-1013-13 | Marcus Smart (+1.95 z net on two references, RotoBaller and Yahoo: both project 7.8 points against our 9.3, and 0.6 to 1.1 steals against our 1.5) and Deandre Ayton (+1.01 on three: our 12.1 points and 8 rebounds against 9.4 to 11.5 and 6.9 to 7.6): (a) hold; (b) clamp to the edge at the lock | (a); both sit past rank 100 |
| D-1013-14 | Add FantasyPros and the cards to the deck's own range check (`scripts/range_check.py` LINE_SOURCES), so the build gate reads five sources | after the draft; the next build already sees the 10/13 RotoBaller file's 12 added names |
| D-1013-11 | Age decline for the 7 players 34 and older: (a) none, as now; (b) a flat per-36 haircut by age band, after the draft with D-C2 | (b) after the draft |
| D-1013-12 (re-put) | The 1 unanchored line beyond 0.5 z net (Dylan Cardwell): (a) hold; (b) move to the outside average at the lock | (a) |
| D-1013-8, D-1013-9 | Murray and Nesmith just past the cut; Ware LINE QUESTIONED | as set in the dial report |
| D-1013-1..7, D-C2, D-SF-1..4 and earlier | carried | carried |

## Provenance

- Inputs: kit `main` 7c44327 (board, lines, the first audit), deck `main` dd6b719 (page sha256 09a889d4baa5, the z frame); the three uploads from the owner's 2026-10-13 message (sha256 b58e2d6d9fca RotoBaller, d1f79284034e FantasyPros; the cards transcribed from the paste).
- Intake: `report/market/third_party_market.py` (two new sources, no-rank handling, percentage scale), `build_market.py` (one alias), `check_derived.py` (three entries; 27 of 27 reproduce at pin d08ac74), `provenance.csv` (three rows).
- Audit: `audit180-2026-10-13/audit180_v2.py` (two runs identical, md5 checked), `audit180_v2.json`, `audit180_v2.txt`, `write_audit_report_v2.py` (this file's writer, which runs the check below before writing). Known-answer check: `reproduce_check_v2.py` recomputes every outside band from the five processed files with its own loader: 161 cells outside the band, 161 reported by the audit, 0 disagreements. The first audit's records untouched.
- No line, tag or placement changed; both planes' hashes equal before and after (e821ec1ddc67 kit, bd2b983876a8 deck).

## In plain language

**What your uploads did.** They doubled the number of outside projections behind most lines: 149 of the 180 now have five, and the band they span is wider than the three-source band, so 43 lines moved down a tier: 29 because every cell that was outside the three-source band sits inside the five-source band, 5 because the band widened and the disagreement shrank, 8 because a minutes, games or age flag no longer fires against the wider set, and 1 (Goodwin) because a reference was lost. The HIGH list goes from 12 to 7: Murray, Gillespie, Beal, Nesmith and Mamukelashvili stay; six come off because the wider band covers most of their cells (Jaylon Tyson (HIGH to LOW, net z +0.74 to +0.00); Kyle Filipowski (HIGH to LOW, net z +0.77 to +0.44); Quentin Grimes (HIGH to LOW, net z -0.69 to +0.14); Al Horford (HIGH to MEDIUM, net z +0.47 to +0.34); Bennedict Mathurin (HIGH to LOW, net z +1.22 to +0.09); T.J. McConnell (HIGH to MEDIUM, net z +0.52 to +0.04)); Goodwin comes off only because he lost a reference. Two new names appear: Marcus Smart, where both outside sources that cover him project 7.8 points against our 9.3, and Deandre Ayton, where all three sit below our 12.1 points and 8 rebounds.

**What the RotoBaller file is.** The same projection as the 9/29 file, re-ranked: every shared player's stat line is identical, 200 ranks moved, 12 names added and 11 dropped. It adds names at the bottom of the board, not a fresh view.

**What is still open.** The age question is unchanged: 7 players 34 and older sit above every projection's average and the method carries no decline. The 6 bench lines with fewer than three projections. And the Bleacher Report piece, which I cannot reach from here; paste it and it becomes a role-context source for the HIGH and MEDIUM lines.

**Your decisions.** D-1013-10 and D-1013-13 tonight or at the lock; D-1013-14, D-1013-11 and D-1013-12 can wait for the draft's aftermath.
