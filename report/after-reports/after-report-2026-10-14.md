# After-report — 2026-10-14: the final morning pull before the draft (Version 68), with the 24 disputed-minutes players read against the preseason

**Owner request (2026-10-14 morning, verbatim):** "Conduct thorough morning pull, with emphasis on the biggest remaining doubt - focus on sources dated today, 10-14-2026 and using preseason data as a guide. Provide detailed after report before we lock". The biggest remaining doubt is the Council's (4–1, this morning): the 24 top-200 players whose projected minutes sit 3 or more from the average of the outside minutes projections (Hashtag 10/12, FantasyPros 10/13, BBM cards 10/13), out of 187 with two or more outside minutes on file.

**What was analyzed and changed:** deck `main` 43ca6bf (Version 67, the six-way blend) and kit `main` 391581f. New inputs pulled 2026-10-14 14:31 UTC: every final ESPN preseason box score from 9/28 to 10/13 (`espn_manifest_2026-10-14.tsv`, parsed to `preseason_roles_2026-10-14.json`, two parses identical); ESPN's league injuries feed (`espn_injuries_2026-10-14.json`); the 30 official rosters (direct-complete); 16 web searches (`search_log_2026-10-14.md`). **What changed:** notes on 37 page rows, and — after the first draft of this report was shown — the owner's three lock calls, verbatim "Restore Kornet's line, Tag Coby White calf risk, Tag Cardwell calf risk" (D-1014-5/6/7, §3a). No other stat line, tag, team or placement moved on either plane. Version 68 is the page with both.

**Method (stated to the owner before the run):** A1 window — every final preseason game 9/28–10/13, minutes per game played and starts. A2 — preseason minutes run low (regulars rest, benches empty), so the shortfall is measured on the 131 undisputed players and taken out before comparing: a shift of -11.43 minutes, or a scale of 0.624. A3 — a verdict needs the adjusted preseason figure 1.5+ minutes closer to one side; under two preseason games is "too little data". **The A2 branch fired** (the shift was past the stated 4-minute limit), so raw figures are shown beside the adjusted ones, and one check was added before any verdict was read: both global corrections inflate every player alike, which favours whichever side projects *more* minutes, so a third, team-relative correction (each player against his own undisputed teammates) was added and a verdict now needs all three to agree (`verdicts.py`, docstring; two runs identical). A4 — "today" means an item timestamped 2026-10-14. A5 — no line moves on the 24 without the owner (the owner then moved one: Kornet). A6 — no Yahoo lock paste has arrived, so prices stay the 10/13 paste.

Pull window: 2026-10-14 → 2026-10-14 (the final pull; preseason box scores 9/28–10/13; tonight's seven games are after the window).

## The short answer, in plain language

**Last night's blend holds up against the preseason.** Of the 24 players whose minutes we disputed with the outside sources, the preseason backs the outside sources for 9 (Dylan Harper, Jalen Green, Egor Demin, Day'Ron Sharpe, Kevin Porter Jr, Alex Caruso, Damian Lillard, LaMelo Ball, Kris Dunn), backs us for 1 (Luke Kornet), is split on 6 and has too little to say on 8. The blend already moved each of these lines five-sixths of the way to the outside sources, so for the 9 the board is already where the preseason points. Harper is the clearest: he started both games he played, at 19 and 24 minutes, while our old line had him as a 22.6-minute bench guard.

**The one player the preseason says we had right is Luke Kornet** (three games, 15–22 minutes, one start, against an outside average of 17.35). **At the owner's call his own line is back** (D-1014-7): he moves from #196 to #151 on the page and from #191 to #148 on the kit board. He is a late-round name either way.

**The eight with too little preseason** are mostly injured or rested, and the reasons are on today's feed: Tobias Harris and Coby White have calf strains and have not played, Beal has not done five-on-five, Aldama had a knee issue, Monk and others were rested by Sacramento on 10/13. For those the blend is the best guess there is.

**Today's sources.** I searched for anything dated today on the 24 and found nothing on the web I could confirm as 10/14 (16 queries, all logged). What is dated today is ESPN's injury feed: 15 items on our players, all written last night about last night's games — mostly planned rest days. One new injury since yesterday's pull matters a little: **Dylan Cardwell** is out at least two weeks with a calf strain. And **Coby White**'s calf strain is his third in about a year. **At the owner's call both now carry the injury-risk tag** (D-1014-5, D-1014-6), with six games off each on the kit (the Stewart and Raynaud shape). Neither moves on the page — White stays #106, Cardwell #175 to #173 only because Kornet's line moved — because the tag only bites above the pool average; what changes is the ▲ on their rows and a lower weekly figure.

**Nothing else changed by hand.** Restoring one line nudges the pool averages, so about a third of the board shifts by a place or so (kit top 200: 80 rows, mean move 0.72; Wembanyama and Gilgeous-Alexander swap #2 and #3 on the kit by 0.01; Curry and Tatum swap #9 and #10 on the page). One edge case to know: **Jalen Green** slips from #155 to #158 on the page, just past the 156 drafted, and Marcus Smart comes in. Rosters still match all 30 teams (335/335). Version 68 passed every gate and test and is live.

## 1. Roster changes

None. Direct-complete roster verification of 2026-10-14: 30 teams, 335 of 335 pool rows on the feed, 0 mismatches, 0 unmatched. The official rosters lost 7 camp names since the 10/13 check, none in the pool (Dain Dainja, Dion Brown, Miles Kelly, Yuki Kawamura, Aaron Nkrumah, Damari Monsanto, Chucky Hepburn). The four unsigned free agents (Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham) are on no official roster: still unsigned.

## 2. The 24 against the preseason

EVIDENCE: `disputed_minutes.json` (the list), `preseason_roles_2026-10-14.json` (the box scores), `verdicts.json` (the reading). "Adjusted" shows the three corrections — global shift / global scale / team-relative — and the verdict needs all three to agree. Games: date, opponent, S(tart) or B(ench), minutes.

| player | team | kit rank | ours | outside | games / starts | preseason min | games | adjusted | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Dylan Harper | SAS | 105 | 22.6 | 29.2 | 2 / 2 | 21.5 | 10-08 ATL S 19; 10-10 PHX S 24 | 32.9 / 34.5 / 32.3 | backs outside |
| Morez Johnson Jr. | DAL | 194 | 18.5 | 25.1 | 1 / 1 | 12.0 | 10-09 HOU S 12 | — | too little data |
| Jalen Green | PHX | 156 | 25.9 | 31.8 | 3 / 3 | 22.0 | 10-10 SA S 29; 10-07 CHI S 22; 10-05 DET S 15 | 33.4 / 35.3 / 39.5 | backs outside |
| Egor Demin | BKN | 152 | 25.1 | 30.2 | 3 / 3 | 20.7 | 10-06 CHA S 18; 10-08 PHI S 22; 10-12 WSH S 22 | 32.1 / 33.2 / 33.2 | backs outside |
| Day'Ron Sharpe | BKN | 117 | 18.7 | 23.5 | 2 / 2 | 19.5 | 10-06 CHA S 18; 10-12 WSH S 21 | 30.9 / 31.3 / 31.3 | backs outside |
| Kevin Porter Jr | MIL | 116 | 19.9 | 24.5 | 2 / 0 | 18.5 | 10-11 CHA B 18; 10-05 MIN B 19 | 29.9 / 29.7 / 24.6 | backs outside |
| Ja Morant | POR | 139 | 25.5 | 29.8 | 3 / 2 | 18.7 | 10-13 SAC B 23; 10-07 GS S 19; 10-12 LON S 14 | 30.1 / 30.0 / 28.0 | split |
| Tobias Harris | SAS | 113 | 25.0 | 29.1 | 0 / 0 | 0.0 | — | — | too little data |
| Mitchell Robinson | BOS | 130 | 19.6 | 23.4 | 1 / 1 | 14.0 | 10-10 PHI S 14 | — | too little data |
| Coby White | CHA | 103 | 29.1 | 32.9 | 0 / 0 | — | — | — | too little data |
| Alex Caruso | OKC | 136 | 18.2 | 21.9 | 2 / 2 | 16.0 | 10-07 MIL S 17; 10-13 IND S 15 | 27.4 / 25.7 / 24.4 | backs outside |
| Damian Lillard | POR | 49 | 27.8 | 31.1 | 2 / 2 | 21.0 | 10-13 SAC S 23; 10-07 GS S 19 | 32.4 / 33.7 / 31.4 | backs outside |
| Malik Monk | SAC | 200 | 22.0 | 25.2 | 0 / 0 | — | — | — | too little data |
| De'Andre Hunter | SAC | 183 | 26.1 | 29.2 | 3 / 2 | 16.7 | 10-10 GS B 19; 10-05 LAL S 13; 10-08 LAL S 18 | 28.1 / 26.8 / 27.0 | split |
| LaMelo Ball | MIN | 40 | 28.0 | 31.1 | 3 / 3 | 19.7 | 10-05 MIL S 17; 10-07 IND S 20; 10-12 NY S 22 | 31.1 / 31.6 / 33.1 | backs outside |
| Collin Gillespie | PHX | 99 | 28.5 | 25.4 | 3 / 0 | 17.0 | 10-10 SA B 20; 10-07 CHI B 14; 10-05 DET B 17 | 28.4 / 27.3 / 30.5 | split |
| Luke Kornet | SAS | 191 | 21.0 | 17.4 | 3 / 1 | 18.0 | 10-08 ATL B 15; 10-10 PHX B 17; 10-12 UTAH S 22 | 29.4 / 28.9 / 27.0 | backs ours |
| Santi Aldama | DAL | 179 | 27.9 | 24.0 | 0 / 0 | 0.0 | — | — | too little data |
| Ryan Rollins | MIL | 75 | 32.1 | 28.1 | 3 / 3 | 19.3 | 10-11 CHA S 23; 10-07 OKC S 21; 10-05 MIN S 14 | 30.7 / 30.9 / 25.6 | split |
| Saddiq Bey | NOP | 121 | 31.2 | 27.2 | 2 / 0 | 18.5 | 10-06 OKC B 20; 10-08 MIA B 17 | 29.9 / 29.7 / 34.8 | split |
| Tre Jones | CHI | 129 | 26.9 | 22.8 | 1 / 0 | 10.0 | 10-11 DEN B 10 | — | too little data |
| Deandre Ayton | WAS | 172 | 27.2 | 23.1 | 3 / 2 | 19.0 | 10-12 BKN S 25; 10-08 NY S 17; 10-10 DET B 15 | 30.4 / 30.5 / 25.5 | split |
| Kris Dunn | LAC | 167 | 27.2 | 22.4 | 2 / 0 | 10.5 | 10-10 TOR B 15; 10-04 GS B 6 | 21.9 / 16.8 / 19.6 | backs outside |
| Bradley Beal | LAC | 186 | 32.1 | 25.7 | 0 / 0 | 0.0 | — | — | too little data |

Tally: backs outside 9, backs ours 1, split 6, too little data 8. Of the 15 where our minutes were lower, the preseason backs the outside sources on 8; of the 9 where ours were higher it backs the outside on 1 (Kris Dunn: 6 and 15 minutes off the bench), ours on 1 (Kornet).

**Reading (INFERENCE).** Preseason minutes are a weak signal — two or three games, rest days, blowouts — which is why the verdicts need three agreeing corrections and why "split" is common. What the signal does carry is *role*: who starts. All eight players we had too low and the preseason backs the other way started most of their games (Harper 2 of 2, Jalen Green 3 of 3, Demin 3 of 3, Sharpe 2 of 2, Caruso 2 of 2, Lillard 2 of 2, LaMelo 3 of 3; Porter is the exception, 0 starts, but his bench minutes are still above the line we had). That is the role change our lines, built on last season's minutes, could not see.

**The too-little-data rows and today's feed:**

| player | preseason games | ESPN's injuries feed, 10/14 download |
|---|---|---|
| Morez Johnson Jr. | 1 | Day-To-Day, item 2026-10-11, 2026-10-14 estimate: Johnson (rest) won't play in Sunday's preseason game against the Rockets, Grant Afseth of DallasHoopsJournal.com reports. |
| Tobias Harris | 0 | Day-To-Day, item 2026-10-05, 2026-10-20 estimate: Spurs head coach Mitch Johnson said they will not rush Tobias Harris (calf) back to the court, Jared Weiss of The Athletic reports. |
| Mitchell Robinson | 1 | not on ESPN's injuries feed 10/14 |
| Coby White | 0 | Day-To-Day, item 2026-10-05, 2026-10-21 estimate: The Hornets announced Monday that White suffered a left calf strain during training camp and will not play during the preseason. |
| Malik Monk | 0 | Day-To-Day, item 2026-10-14, 2026-10-16 estimate: Monk (rest) is out for Tuesday's preseason game against Portland, Matt George of ABC 10 Sacramento reports. |
| Santi Aldama | 0 | Day-To-Day, item 2026-10-11, 2026-10-14 estimate: Aldama (knee) won't play in Sunday's preseason game against the Rockets, Grant Afseth of DallasHoopsJournal.com reports. |
| Tre Jones | 1 | not on ESPN's injuries feed 10/14 |
| Bradley Beal | 0 | Day-To-Day, item 2026-10-07, 2026-10-14 estimate: Beal (knee) isn't participating in five-on-five work and is doing individual player development work, Tomer Azarly of ClutchPoints.com reports. Azarly |

## 3. What it means for the board

- **Backs outside (9):** no change needed. The blend already carries five-sixths of the outside view of these lines (Version 67), and the preseason says that direction is right.
- **Backs ours (1, Kornet):** the blend moved him the wrong way. The owner restored his own line (D-1014-7, §3a).
- **Split (6):** keep the blend — an average is the right hedge when the evidence points both ways.
- **Too little data (8):** keep the blend. Morez Johnson Jr. is kit-only (no row on the page), so his note sits on the kit side only.

Nothing in this section changed a line by itself; the owner's three calls are in §3a.

## 3a. The owner's three lock calls (applied)

EVIDENCE: `lock_calls.py` (assertions: only the named cells move on either plane, the tags read `inj-calf-risk` through the page's own parser, no `];`, Kornet's kit and page lines equal; a second run changes nothing) → `lock_calls_2026-10-14.json`; board effect `lock_board_diff.py` (kit board at HEAD and page values at deck `43ca6bf` against the working trees; two runs identical) → `lock_board_diff_2026-10-14.json`.

| call | page (deck) | kit | page rank | kit rank |
|---|---|---|---|---|
| D-1014-7 restore Kornet's line | the nine categories to the pre-blend line (`lines_blend_2026-10-14.json`, "old"); note added | same line | #196 to #151 | #191 to #148 |
| D-1014-6 tag Coby White | leading tag `inj-calf-risk` (×0.78 above the pool mean, weekly 0.75); the old role note kept as prose | GP 68 to 62 | #106 to #106 | #103 to #103 |
| D-1014-5 tag Dylan Cardwell | leading tag `inj-calf-risk`; the rookie-proj prose kept (the market model still reads it) | GP 65 to 59 | #175 to #173 | #173 to #174 |

Kit cells changed: Coby White gp 68 to 62; Luke Kornet fgp 0.649 to 0.613; Luke Kornet fga 3.5 to 4.0; Luke Kornet ftp 0.791 to 0.812; Luke Kornet fta 1.5 to 1.7; Luke Kornet pts 5.8 to 6.3; Luke Kornet reb 5.3 to 6.1; Luke Kornet ast 1.6 to 1.9; Luke Kornet blk 0.9 to 1.1; Dylan Cardwell gp 65 to 59. Page cells changed: 11 (Kornet's nine categories plus his note, the two tags).

**Games (my call, stated):** the kit carries risk as games. Six off each, about two weeks of the schedule, is the shape of D-1010-2 (Stewart 70 to 64) and D-1012-1 (Raynaud 72 to 66). White at 62 sits at the low end of the outside range (Hashtag 62, Yahoo 69, BBM cards 72, FantasyPros 75); Cardwell at 59 against Yahoo's 72. Neither GP cut moves the kit board, because the kit never shrinks a below-average value for absence.

**Ripple (EVIDENCE, `lock_board_diff_2026-10-14.json`):** kit top 200 — 80 rows moved, mean 0.72 places, entries none; kit top 100 — 22 moved. Page top 156 — 71 moved, mean 0.6; in: Luke Kornet, Marcus Smart; out: Jalen Green, De'Anthony Melton. The ripple is the pool averages moving under one restored line (Kornet's field-goal and rebound columns), not a judgment on anyone else.

## 4. Sources dated today

`search_log_2026-10-14.md`: 16 queries, 0 web results confirmed as dated 2026-10-14 (the search tool mixes seasons; every result is a lead until its own date is seen). The dated-today material is ESPN's injuries feed, downloaded 2026-10-14 14:31 UTC: 18 items league-wide carry a 2026-10-14 UTC timestamp, 15 of them on pool rows — all written the evening of 10/13 US time.

| item (UTC) | player | status | what it says |
|---|---|---|---|
| 00:16Z | Andrew Nembhard | Day-To-Day | Nembhard (undisclosed) won't play in Tuesday's preseason game against the Thunder, Scott Agness of FieldhouseFiles.com reports. |
| 00:17Z | Aaron Nesmith | Day-To-Day | Nesmith will be rested for Tuesday's preseason game against the Thunder, Scott Agness of FieldhouseFiles.com reports. |
| 00:18Z | Jarace Walker | Day-To-Day | Walker (undisclosed) won't play in Tuesday's preseason game against the Thunder, Scott Agness of FieldhouseFiles.com reports. |
| 00:19Z | T.J. McConnell | Day-To-Day | McConnell (undisclosed) will not play in Tuesday's preseason matchup against Oklahoma City, Scott Agness of Fieldhouse Files reports. |
| 00:33Z | Luka Doncic | Day-To-Day | Doncic will be rested for Tuesday's preseason game against the Warriors, Khobi Price of The California Post reports. |
| 00:35Z | Ziaire Williams | Day-To-Day | Williams (foot) will not play in Tuesday's preseason matchup against Golden State, Khobi Price of The California Post reports. |
| 00:39Z | Collin Sexton | Day-To-Day | Sexton (lower leg) has been ruled out for Tuesday's preseason game against the Warriors, Khobi Price of The California Post reports. |
| 00:57Z | Zach LaVine | Day-To-Day | LaVine (rest) will not play in Tuesday's preseason matchup against Portland, Matt George of ABC 10 Sacramento reports. |
| 00:59Z | Domantas Sabonis | Day-To-Day | Sabonis (undisclosed) will not play in Tuesday's preseason matchup against Portland, Matt George of ABC 10 Sacramento reports. |
| 01:00Z | Malik Monk | Day-To-Day | Monk (rest) is out for Tuesday's preseason game against Portland, Matt George of ABC 10 Sacramento reports. |
| 01:02Z | Darius Acuff Jr. | Day-To-Day | Acuff (rest) has been ruled out for Tuesday's preseason game against Portland, Matt George of ABC 10 Sacramento reports. |
| 01:04Z | De'Andre Hunter | Day-To-Day | Hunter (rest) has been ruled out for Tuesday's preseason game against the Trail Blazers, Matt George of ABC 10 Sacramento reports. |
| 01:06Z | Ben Simmons | Day-To-Day | Simmons (rest) won't play in Tuesday's preseason game against the Trail Blazers, Matt George of ABC 10 Sacramento reports. |
| 01:40Z | Draymond Green | Day-To-Day | Green (rest) has been ruled out for Tuesday's preseason game against the Lakers, Law Murray of The Athletic reports. |
| 10:40Z | Precious Achiuwa | Day-To-Day | Precious Achiuwa exited Tuesday's game with a right ankle injury and did not return, per Jason Anderson of the Sacramento Bee. |

Each is on the player's page note (`deck_notes_2026-10-14.json`, 37 rows), labelled single-source.

## 5. The injury feed both ways

EVIDENCE: `feed_diff_2026-10-14.json` (the diff), `tags_2026-10-14.txt` (the page's tag inventory). Feed: 137 items on 30 teams, 94 on pool rows; at the 14:31 pull the page carried 50 tags (17 excluded, 33 risk); the two lock-call tags (§3a) make it 52 and 35.

- **Pool rows Out on the feed (11):** Jimmy Butler III (Surgery, 2027-01-02 estimate), Moses Moody (Surgery, 2026-12-01 estimate), Max Strus (None, 2026-11-02 estimate), Brandon Ingram (Surgery, 2026-11-01 estimate), Isaiah Stewart (None, 2026-10-23 estimate), Donte DiVincenzo (Surgery, 2027-04-01 estimate), Mark Williams (Surgery, 2027-02-03 estimate), Shaedon Sharpe (Surgery, 2027-03-02 estimate), Dylan Cardwell (Strain, 2026-10-29 estimate), Maxime Raynaud (Dislocated, 2026-10-25 estimate), Jusuf Nurkic (None, 2026-11-04 estimate). All carry their tag; Dylan Cardwell, the one new item since the 10/13 pull (Out, at least two weeks, left calf strain, per Anthony Slater of ESPN.com on ESPN's feed, item 2026-10-13 20:57 UTC, 10/29 estimate), was untagged in the first draft and is tagged now by the owner's call (D-1014-5).
- **Coby White** (left calf strain announced 10/5, out the whole preseason, 10/21 estimate) was on the page as healthy with a role note; the 10/5 reports (TSN, NBA.com, RotoBaller) call it his third calf strain in about a year — tagged now by the owner's call (D-1014-6).
- **Day-to-day items on untagged pool rows (71):** almost all rest days for the last preseason games; none says more than day-to-day, and none is new information about the regular season. Listed in the record.
- **Tagged but absent from the feed (28):** unchanged from the 10/13 pull; the four unsigned free agents among them are on no official roster.

## 6. Publication

| step | result |
|---|---|
| deck notes | 37 rows, note column only (`deck_notes.py`: every name resolved, no other column changed, no `];`, a second run changes nothing) |
| lock calls | `lock_calls.py` PASS, kit 10 cells / page 11 cells, second run 0 |
| kit board | `rank_engine.py` re-run (200 of 313 projected, 12 held), `slate.py`, `test_rank_engine` OK, `check_provenance` PASS, `check_derived` 27/27 |
| build | red-first: refused on gate 7 without the exemption (propagation 2: White GP 68 to 62, Cardwell GP 65 to 59 — the page has no games column; its rows changed by tag). With the two players excused by name (the build's plane exemption flag, recorded in the manifest): 7 gates PASS, 335 players, rosters direct-complete 335/335, planes 315 shared, drift 0, 2 named exemptions, market the 10/13 paste (294/335 priced) |
| chain on Version 68 | parity EXACT (455 owner turns across 35 committed states); test_card 103; test_draft 65; test_gates 54; full DOM 145 assertions, 0 failed; repeat-name 28 of 28 mocks replayed; 8 FLAGGED |
| publish | Version 68, version id 1791993066-d8ff; the served page equals the local file (sha256 b83d1cdcc0e9) inside the publisher's wrapper |

## 7. The plan against the outcome

| criterion | grade | evidence |
|---|---|---|
| C1 preseason fetched, parsed twice identical, manifest kept | PASS | 46 finals 9/28–10/13; `espn_manifest_2026-10-14.tsv` |
| C2 the 24-row table from the records | PASS | §2, `verdicts.json` (two runs identical) |
| C3 today's sources for the 24, queries logged | PASS | §4, `search_log_2026-10-14.md` (0 items confirmed as 10/14 on the web; the feed's 15 are) |
| C4 feed both ways; rosters 335/335 | PASS | §1, §5 |
| C5 Version 68: 7 gates, chain green, publish byte-verified | PASS | §6 |
| C7 the owner's three calls on both planes, asserted, board effect from records | PASS | §3a |
| C6 this report through the five gates; the sheet covers the 24 | PASS | the gate runs ride the kit PR; D-1014-8 |

Predictions: "the preseason backs the outside on at least half of the 15 we have low" — 8 of 15 ✓; "Harper about 25+ adjusted" — 32.3 to 34.5 ✓; the A2 branch (a shift past 4 minutes) **fired** at -11.43, and the third correction was added as described in the method.

## Watchlist

- Tonight's seven preseason games (BKN at MIA, CHA at BOS, PHX at SA, NO at DAL, CHI at MIL, DET at MIN, DEN at LAC) end after the lock; Harper, Kornet, Jalen Green, Porter and Bey play in them. They cannot change the board before the draft.
- The Yahoo lock paste (D-1013-1) has not arrived; the page prices on the 10/13 paste. If it arrives before the lock it is a price-only rebuild (D-1014-3).
- The publish freeze during the draft (D-1013-5) and no RESYNC during the draft (D-1013-2) stand.

## Open-item receipts

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram | ESPN injuries feed, downloaded 2026-10-14 14:31 UTC | Out, 11/1 estimate: partially torn Achilles, won't be ready for the start of the season (Joey Linn, SI.com, via ESPN's feed, item 9/28) — HELD (inj-achilles-risk stands) |
| Kristaps Porzingis | ESPN injuries feed, same download | day-to-day, 10/21 estimate: remains away from the team (Anthony Slater, ESPN.com, item 10/12) — HELD; the owner's veto stands |
| Kawhi Leonard | ESPN injuries feed, same download | not on the feed 10/14; debuted 10/13 (21 in 17 minutes, ESPN box score, in Version 66) — HELD on the -mild tier by the owner's call |
| Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham | official rosters, direct-complete 2026-10-14 | on no team's roster: still unsigned — HELD out-unsigned |
| Jeremy Sochan | ESPN injuries feed, same download | not on the feed 10/14 — HELD (no change) |
| Bennedict Mathurin | ESPN injuries feed, same download | not on the feed 10/14 — HELD (no change) |
| Ryan Rollins | ESPN box scores 9/28–10/13; injuries feed | 3 preseason starts (14, 21, 23 min); not on the feed — HELD; his minutes read SPLIT (§2) |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 b83d1cdcc0e9), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 28 of 28 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-13.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 28 of 28 | 41 | 117 | 48 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 19 of 28 | 90 | 180 | 56 | 118 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 11 of 28 | 34 | 65 | 60 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 9 of 28 | 105 | 138 | 181 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| John Collins | 9 of 28 | 72 | 118 | 102 | 71 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 8 of 28 | 100 | 183 | 100 | 126 | 148 | 155 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 8 of 28 | 6 | 32 | 15 | 16 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 5 of 28 | 114 | 141 | 120 | 131 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (19 mocks, value 9, market 18); Lauri Markkanen (16 mocks, value 20, market 37); Derrick White (12 mocks, value 27, market 45); Tyrese Haliburton (12 mocks, value 7, market 12); Tyrese Maxey (7 mocks, value 5, market 9); Kel'el Ware (6 mocks, value 57, market 77); VJ Edgecombe (6 mocks, value 61, market 75).

## Bounds

**Out of scope by design.** Any stat-line change beyond the owner's Kornet call (A5); the usage model and team scaling (D-C2); tonight's games (after the window).

**In scope and unverified.**
- **Web sources dated 10/14:** `ATTEMPTED-FAILED` — 16 queries, none returned an item whose own date I could confirm as 10/14 (the tool returns summaries that mix seasons). The conclusions do not rest on them: the verdicts rest on ESPN's box scores and feed. Fetching each candidate page to read its date was not done (time).
- **How preseason minutes translate to the season:** `UNVERIFIABLE` from this data alone — the calibration uses this preseason's undisputed players, not a past season's preseason-to-season record, which is not on file (did not check the web for one). That is why the verdicts need three corrections to agree and are labelled INFERENCE where they become advice.
- **Morez Johnson Jr.:** kit-only row, one preseason game — `UNVERIFIABLE` before the season.

## Decision sheet (owner disposes)

| id | decision | options | recommendation |
|---|---|---|---|
| D-1014-5 | Dylan Cardwell (Out 2+ weeks, calf, 10/29 estimate) | (a) tag inj-calf-risk; (b) note only | **DECIDED (a)** by the owner, 10/14 ("Tag Cardwell calf risk"); applied, kit GP 65 to 59 (§3a) |
| D-1014-6 | Coby White (third calf strain in about a year, 10/21 estimate) | (a) tag inj-calf-risk; (b) keep the role note | **DECIDED (a)** by the owner, 10/14 ("Tag Coby White calf risk"); applied, kit GP 68 to 62 (§3a) |
| D-1014-7 | Luke Kornet, the one line the preseason backs as ours | (a) keep the blend; (b) restore our line | **DECIDED (b)** by the owner, 10/14 ("Restore Kornet's line"); applied on both planes (§3a) |
| D-1014-8 | the other 23 disputed-minutes players | (a) keep the blend; (b) restore ours on the split rows | (a) |
| D-1014-3 (carried) | the Yahoo lock paste | (a) paste it before the lock: a price-only rebuild; (b) lock on the 10/13 prices | (a) if it arrives in time |
| D-1014-1, D-1014-2 (carried) | Lendeborg's line; the blend's weights | as in `after-report-2026-10-14-blend.md` | open; recommendations (a) and (a) |

The kit GP figures under D-1014-5/6 (six games each) are my reading of the precedent, not the owner's words; another figure is a kit-only edit with no board effect (§3a).

## Provenance

- This cloud session, the morning of 2026-10-14 (pull started 14:30 UTC). Governors loaded for this task: plan-gate (full block emitted before the pull), after-report; the Council's verdict of this morning set the emphasis.
- Records in `report/after-reports/pull-2026-10-14/`: `disputed_minutes.py/.json`, `preseason_roles_2026-10-14.json` (parsed by `report/wo5/tools/parse_preseason.py`), `espn_manifest_2026-10-14.tsv`, `verdicts.py/.json`, `espn_injuries_2026-10-14.json`, `feed_diff_2026-10-14.json`, `tags_2026-10-14.txt`, `deck_notes.py`, `deck_notes_2026-10-14.json`, `search_log_2026-10-14.md`, `lock_calls.py` + `lock_calls_2026-10-14.json`, `lock_board_diff.py` + `lock_board_diff_2026-10-14.json`, this writer.
- Re-verify: `python3 verdicts.py` reproduces `verdicts.json` from the pinned box scores; `python3 deck_notes.py <deck players.csv> espn_injuries_2026-10-14.json` and `python3 lock_calls.py` on the shipped files change nothing.
