# After-report — draft_78: the second 10/13 late live room from slot 10, on deck Version 65; Yahoo's projected standings beside ours; why six players left the card

**Owner request (2026-10-13 late, verbatim):** "Another live mock:" — the deck tool's LIVE feed, a screenshot of Yahoo's 2026-27 projected standings for the room, the owner's 13-man roster and Yahoo's round-by-round recap. **Follow-up while it was graded (2026-10-14, verbatim):** "I also have a question. Prior to our work today in stat projections, almost the same players were suggested at a heavy clip, which aren't even on the card now. Curious of what changed in the logic/arithmetic where they are no longer being suggested? Jalen Williams, Pritchard, OG, Chet Holmgren, Anthony Davis, Towns"

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (random humans; a practice rep, not opponent intel; display names: 1 Mathieu, 2 Tanner, 3 Joe, 4 victor, 5 Ryan, 6 Calvin, 7 SWON, 8 Mike Walsh, 9 Mamba Out!, 10 David, 11 Phillip, 12 Invisible Bully). **Deck used:** Version 65 (rev `dd6b719`, the dial pass; Porziņģis veto live). Replaying the owner's tool log through the v65 page reproduces all eight "off the card" lines of the paste character for character.

Pull window: 2026-10-13 → 2026-10-13 (analysis only, written after midnight on 10/14; no roster pull; the planes are held for this morning's final pull by the owner's decision).

**Headline.** As drafted **19.48 percent** for the title on the real eight-team bracket, rank 2 of 12, playoffs 98.89 percent. Expected weekly category wins 5.054, rank 2 of 12 behind seat 1 (Mathieu, 5.099), favored in 10 of 11 head-to-heads. Yahoo's projected standings agree on the order: this roster second, Mathieu first. Following the card's 🎯 from the same seat (the self-consistent chain) grades 35.96 percent. The costly turn was the first one: #10 Tyrese Haliburton, card #9; Jalen Johnson (card #2, gone at #12) grades 26.65 percent as a single swap, +7.17 points. One pick was never fixed in the tool: #88 stayed UNKNOWN ("Chite" = Coby White), so the tool's card at #135 and #154 was computed on a board that still listed him; it changed one 🎯 (#154: Vassell shown, Tari Eason on the true board, worth +0.0073 weekly category wins). **The six players:** none of their lines changed in the dial pass of 10/13; all six fell on 10/12 when WO-5 rebuilt every line on the 2025-26 season — Davis #5 → #14, Towns #6 → #24, Holmgren #10 → #15, Jalen Williams #16 → #41, Anunoby #28 → #50, Pritchard #37 → #78 (§6). On the same 351 owner turns of 27 graded rooms, the six were the card's 🎯 104 times on the last page before WO-5 and 4 times on Version 65.

## 1. Roster changes

None. No line, tag, placement or price changed on either plane; this is a grade of a practice room and an answer to a question.

## 2. The team, graded

EVIDENCE: `arena/results/m78_final.json`, `m78_arms.json` (18,000 seasons per arm, seeds 11/23/47, the real eight-team bracket), pool tag v65 = `players_v65.csv` (data/players.csv at `dd6b719`, sha256 bd2b983876a8).

| arm | title % | playoffs % | rank |
|---|---|---|---|
| as drafted | 19.48 | 98.89 | 2 |
| follow the card's 🎯 at every turn (self-consistent chain: #10 Jamal Murray, #34 Chet Holmgren, #39 Dyson Daniels, #58 Derrick White, #82 Ty Jerome, #87 Immanuel Quickley, #135 Bobby Portis) | 35.96 | 99.98 | 1 |
| single swap at #10: Jalen Johnson | 26.65 | 99.76 | 1 |
| single swap at #58: Cameron Boozer | 24.63 | 99.72 | 1 |
| single swap at #135: Tari Eason | 22.83 | 99.39 | 1 |
| single swap at #15: Jamal Murray | 21.68 | 99.42 | 1 |
| single swap at #82: Josh Hart | 21.36 | 99.15 | 1 |
| single swap at #106: Myles Turner | 21.08 | 99.29 | 2 |
| single swap at #34: James Harden | 20.88 | 99.14 | 2 |
| single swap at #154: Tari Eason | 20.43 | 99.00 | 2 |
| single swap at #39: Michael Porter Jr. | 20.31 | 99.06 | 1 |

Category shape (weekly model, rank of 12): FG% 4, FT% 1, 3PTM 6, PTS 12, REB 10, AST 10, ST 3, BLK 1, TO 1. A defensive, efficient build: first in free throws, blocks and turnovers; last in points, tenth in rebounds and assists.

For scale, the other live public rooms graded on this bracket: mock 67 17.51, mock 68 28.36, mock 73 34.17, mock 74 17.91, mock 75 29.39, mock 77 35.98.

## 3. Pick by pick: the page's card, the owner, hindsight

EVIDENCE: `m78_deckcard_v65.json` (the v65 page's own engine on the true board, Yahoo's recap), `m78_deckcard_v65_toolstate.json` (the same engine on the board the tool held: #88 UNKNOWN, Aaron Gordon inserted at #119 after #123 was fed), `m78_hindsight.json` (every single-swap alternative scored by weekly category wins against the final rosters).

| pick | owner took | card rank (true board) | the page's 🎯 | what the tool showed, if different | hindsight's best alternative (Δ weekly cat wins) |
|---|---|---|---|---|---|
| #10 | Tyrese Haliburton | 9 | Jamal Murray |  | Jalen Johnson (+0.248) |
| #15 | Kevin Durant | 2 | Jamal Murray |  | Jamal Murray (+0.086) |
| #34 | Kawhi Leonard | 1 | Kawhi Leonard |  | James Harden (+0.056) |
| #39 | Derrick White | 1 | Derrick White |  | Michael Porter Jr. (+0.050) |
| #58 | Zach Edey | 27 | Kel'el Ware |  | Cameron Boozer (+0.207) |
| #63 | Kel'el Ware | 1 | Kel'el Ware |  | Naz Reid (-0.031) |
| #82 | Jaden McDaniels | 11 | Ty Jerome |  | Josh Hart (+0.067) |
| #87 | Yaxel Lendeborg | 6 | Ty Jerome |  | Josh Hart (-0.011) |
| #106 | Neemias Queta | 5 | Collin Gillespie |  | Myles Turner (+0.023) |
| #111 | Collin Gillespie | 1 | Collin Gillespie |  | Toumani Camara (-0.032) |
| #130 | Reed Sheppard | 1 | Reed Sheppard |  | Draymond Green (-0.007) |
| #135 | Tre Jones | 5 | Devin Vassell | rank 3, 🎯 Devin Vassell | Tari Eason (+0.058) |
| #154 | Devin Vassell | 3 | Tari Eason | rank 1, 🎯 Devin Vassell | Tari Eason (+0.007) |

On the true board the owner took the 🎯 at 5 of 13 turns and stayed in the Top 5 at 9; on the card the tool actually showed, 6 and 9. The turns outside the Top 5 were #10 Tyrese Haliburton (card #9), #58 Zach Edey (card #27), #82 Jaden McDaniels (card #11), #87 Yaxel Lendeborg (card #6); at #58 the 🎯 Kel'el Ware lasted to #63 and was taken there. From round 9 on, the D54-1 line ("take the 🎯") fired three times; the owner followed it once, at #154 after undoing Anthony Black.

## 4. Yahoo's projected standings against ours

EVIDENCE: `yahoo_standings_2026-10-13.csv` (the screenshot transcribed; recomputing roto points from its 12 rows reproduces Yahoo's printed ranks, the 7.5 tie included), `yahoo_compare.json` (each roster summed on Yahoo's per-player file of 10/13), `m78_final.json`.

| view | where this roster lands |
|---|---|
| Yahoo, season-total roto points | 2 of 12 (behind Mathieu, seat 1) |
| Yahoo totals, head to head category by category | favored against 9 of 11; loses to Mathieu (4-5), victor (4-5) |
| the deck, weekly category model | rank 2 of 12 behind seat 1, favored against 10 of 11 |

Both views put seat 1 (Mathieu) first and this roster second. Unlike mock 77, games played explain little of the gap: summed from Yahoo's per-player file seat 1 carries 911 projected games against this roster's 891. Per player-game seat 1 leads in points, rebounds, assists, threes, steals; this roster in blocks. Against seat 1 on Yahoo's totals this roster wins both percentages, blocks and turnovers and loses the other five: the shape §2 shows. Summing Yahoo's 10/13 per-player file comes within 3.4 percent of the screenshot's points for every team but does not equal it (the deck pool's "Cameron Johnson" is "Cam Johnson" in Yahoo's file, aliased), so the screenshot rests on a slightly newer Yahoo projection than the file on hand.

## 5. Tool-state integrity

recap picks 156; seats 12 (David = 10); pool-less 0: []; feed vs recap: 155 of 156 agree on name and seat; differences [(88, ('UNKNOWN (Chite)', 9), 'Coby White', 9)]; feed picks still UNKNOWN at the end: [(88, 'UNKNOWN (Chite)')]; owner picks: #10 Tyrese Haliburton, #15 Kevin Durant, #34 Kawhi Leonard, #39 Derrick White, #58 Zach Edey, #63 Kel'el Ware, #82 Jaden McDaniels, #87 Yaxel Lendeborg, #106 Neemias Queta, #111 Collin Gillespie, #130 Reed Sheppard, #135 Tre Jones, #154 Devin Vassell. The owner's tool log as pinned in `arena/data/events/m78_tool_events.json` (160 events: 158 feeds, 3 of them raw texts that resolved to UNKNOWN ("Tati,", "<axeu", "Chite") and 2 numbered fixes (#7 Tatum, #8 Maxey); 1 insert (Aaron Gordon at #119, sent after #123); 1 undo (Anthony Black at #154)) replayed through the v65 page in headless Chromium: 0 echo misses, 0 clock mismatches, 0 page errors, 156 picks; the eight "off the card" lines equal the paste's. Its final board differs from Yahoo's recap at #88 only (`UNKNOWN #88` vs Coby White), the one fix never sent; the tool warned once ("#88 is still UNKNOWN").

What the open UNKNOWN did: with Coby White still listed and seat 9's roster one guard short, the card from #88 on was computed on a slightly different board. It matched the true board's card at 11 of 13 owner turns; at #135 Tre Jones showed as #3 (true board #5) and at #154 the 🎯 was Vassell (true board: Tari Eason, Vassell #3). The grade above uses the true board. The grading pipeline's Python port, which keeps the pre-v24 name tie-break and does not apply the page's priced-only rule from round 11, differs from the page record at 2 turns (#39: port 2, page 1, #111: port 2, page 1); the page record is the authority for what the card said.

## 6. The owner's question: why Jalen Williams, Pritchard, Anunoby, Holmgren, Davis and Towns left the card

EVIDENCE: `six_lines.py` → `six_lines.json` (the six per-game lines as shipped in the deck's data/players.csv at each version on main from the 10/12 morning pull to Version 65, and the deck's own value math run on each version's pool; two runs identical), `six_cards.py` → `six_cards.json` (per-run cards in the deck at `arena/results/six_cards_2026-10-14/`; the same 27 graded draft states replayed through five page versions with each page's own engine, so the rooms are held fixed and only the page changes), `after-report-2026-10-12-wo5.md` (the method), `report/market/yahoo-proj-2026-10-13.csv` (Yahoo's ranks and ADP of 10/13).

**What changed.** Not the engine and not the card's arithmetic: the page's engine block (the z-scores, the weekly category model, the card's ordering) is byte-identical on all five pages in the card table below (sha256 af51c3becbd4); only the data block differs. What changed is the input: on 10/12 the WO-5 pass rebuilt 326 deck lines on each player's 2025-26 production rate at his 2025-26 minutes (shooting pulled a third of the way to career, steals and blocks averaged over three seasons, points from the shooting identity; returnees' minutes from the outside projections). Before it, most of the board's stars carried 2024-25-shaped lines. The six are players whose 2025-26 season ran below the line they carried. The minutes-and-games pass that night changed only Jalen Williams among them (his minutes up); the dial pass of 10/13 (Version 65) changed none of them.

| player | line before WO-5 (pts / reb / ast / stl / blk / 3pm / to, FG% / FT%) | line now | value rank before → after WO-5 → Version 65 | Yahoo rank / ADP (source: `yahoo-proj-2026-10-13.csv`; lines: the deck's data/players.csv) |
|---|---|---|---|---|
| Jalen Williams | 22.5 / 5.5 / 5.4 / 1.7 / 0.7 / 2.0 / 2.6, 0.488 / 0.795 | 19.0 / 5.1 / 6.0 / 1.3 / 0.6 / 0.8 / 2.1, 0.493 / 0.828 | 16 → 57 → 41 | 37 / 40.5 |
| Payton Pritchard | 19.0 / 4.2 / 5.5 / 1.0 / 0.2 / 3.8 / 2.0, 0.465 / 0.850 | 16.9 / 3.9 / 5.2 / 0.8 / 0.1 / 2.7 / 1.4, 0.461 / 0.883 | 37 → 77 → 78 | 80 / 82.4 |
| OG Anunoby | 18.5 / 5.0 / 2.3 / 1.6 / 0.9 / 2.3 / 1.4, 0.480 / 0.805 | 16.6 / 5.2 / 2.2 / 1.4 / 0.7 / 2.3 / 1.8, 0.481 / 0.810 | 28 → 43 → 50 | 69 / 67.7 |
| Chet Holmgren | 17.5 / 8.8 / 2.4 / 0.9 / 2.4 / 1.7 / 1.5, 0.500 / 0.760 | 16.9 / 8.9 / 1.7 / 0.7 / 2.1 / 1.3 / 1.6, 0.549 / 0.790 | 10 → 16 → 15 | 31 / 30.6 |
| Anthony Davis | 24.0 / 11.8 / 3.4 / 1.2 / 2.1 / 0.9 / 2.0, 0.515 / 0.775 | 22.0 / 10.2 / 3.1 / 1.0 / 1.9 / 0.6 / 2.0, 0.518 / 0.781 | 5 → 14 → 14 | 45 / 42.6 |
| Karl-Anthony Towns | 24.8 / 12.5 / 3.2 / 1.0 / 0.8 / 2.1 / 2.9, 0.525 / 0.830 | 20.2 / 11.9 / 3.0 / 0.8 / 0.6 / 1.5 / 2.5, 0.508 / 0.852 | 6 → 25 → 24 | 16 / 15.6 |

Where each one's value went (z-score change, before WO-5 → Version 65, the three largest):

- Jalen Williams: 3PTM -1.18, ST -0.88, PTS -0.57 (total -1.52).
- Payton Pritchard: 3PTM -1.14, TO +0.64, ST -0.46 (total -1.69).
- OG Anunoby: TO -0.67, BLK -0.35, ST -0.28 (total -1.31).
- Chet Holmgren: FG% +0.80, ST -0.50, BLK -0.48 (total -0.53).
- Anthony Davis: REB -0.46, ST -0.40, BLK -0.30 (total -1.75).
- Karl-Anthony Towns: PTS -0.77, 3PTM -0.57, FG% -0.52 (total -1.90).

**On the card, rooms held fixed.** The same 351 owner turns of 27 graded rooms (mocks 51–78 with a state on file), each turn's card computed by each page's own engine:

| page | Jalen Williams | Payton Pritchard | OG Anunoby | Chet Holmgren | Anthony Davis | Karl-Anthony Towns | all six |
|---|---|---|---|---|---|---|---|
| v59 (`f918062`) | 🎯 19, Top 5 52 | 🎯 24, Top 5 57 | 🎯 22, Top 5 65 | 🎯 4, Top 5 25 | 🎯 6, Top 5 47 | 🎯 29, Top 5 29 | 🎯 104, Top 5 275 |
| v60 WO-5 (`8ec736b`) | 🎯 0, Top 5 0 | 🎯 0, Top 5 1 | 🎯 0, Top 5 9 | 🎯 3, Top 5 6 | 🎯 1, Top 5 9 | 🎯 0, Top 5 0 | 🎯 4, Top 5 25 |
| v62 MG (`73e832c`) | 🎯 0, Top 5 0 | 🎯 0, Top 5 1 | 🎯 0, Top 5 6 | 🎯 3, Top 5 6 | 🎯 1, Top 5 5 | 🎯 0, Top 5 0 | 🎯 4, Top 5 18 |
| v64 (`f6fb476`) | 🎯 0, Top 5 0 | 🎯 0, Top 5 1 | 🎯 0, Top 5 6 | 🎯 3, Top 5 6 | 🎯 1, Top 5 5 | 🎯 0, Top 5 0 | 🎯 4, Top 5 18 |
| v65 (`dd6b719`) | 🎯 0, Top 5 1 | 🎯 0, Top 5 1 | 🎯 0, Top 5 5 | 🎯 3, Top 5 11 | 🎯 1, Top 5 9 | 🎯 0, Top 5 0 | 🎯 4, Top 5 27 |

The drop happens at one step, v59 → v60 (WO-5): the six go from 🎯 104 and Top 5 275 to 🎯 4 and Top 5 25; the later pages move them by little. They have not vanished: on Version 65 they still reach the Top 5 27 times, 20 of them Holmgren and Davis, whose new value still sits above where Yahoo ranks and drafts them. The old page's heaviest habit was Towns as the 🎯 at #10 (22 of 27 rooms) and Pritchard at #58 (14 of 27).

**Was the old board or the new one right?** Against the market, the old board was the outlier: before WO-5 it valued Davis 5th, Holmgren 10th, Williams 16th, Anunoby 28th, Pritchard 37th, where Yahoo's 10/13 projected rank has them 45, 31, 37, 69, 80 and the market drafts them around 43, 31, 40, 68, 82 (ADP). Now Jalen Williams and Pritchard sit at the market, Davis, Holmgren and Anunoby still above it, and Towns below it (24th against Yahoo's 16th, ADP 15.6). Towns is the one where our line is lower than the market's: his 2025-26 season (20.2 points in 31 minutes) is the basis; the 10/12 Towns report and WO-5 §4 carry the full derivation. The one out-of-sample season on record cuts the other way for the method as a whole: a copy of the prior season had more error than pre-season projections in 8 of 9 categories (`after-report-2026-10-09-market.md` §4, cited in the dial report), which is why D-C2 (a blend with a usage model) is set for after the draft.

## Watchlist

- An UNKNOWN left open changes the board the card computes on. In the real draft, send the `N- Name` fix as soon as the warning shows; here it moved one 🎯 by a small margin.
- Haliburton at #10: card #9 in this room; Jalen Johnson, card #2, was the better pick by a full grade.
- The 10/14 lock paste (D-1013-1), the publish freeze during the draft (D-1013-5), no RESYNC during the draft (D-1013-2).

## Open-item receipts

| item | query run (2026-10-13/14) | dated finding |
|---|---|---|
| (this room) | records only; no web research and no roster pull | the room's names resolve to the v65 pool 156 of 156; the lines are the ones merged in kit PR #109 |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull (`after-report-2026-10-13.md`, receipts dated 10/13) | all HELD or unsigned on 2026-10-13 per those receipts; not re-queried here (did not check) |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 09a889d4baa5), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 27 of 27 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-13.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Kel'el Ware | 23 of 27 | 26 | 77 | 51 | 51 | 63 | 61 | ft_pct .732 vs .714-.723 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Reed Sheppard | 22 of 27 | 63 | 180 | 56 | 118 | 126 | 129 | tpm 2.8 vs 2.2-2.6 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Ty Jerome | 22 of 27 | 39 | 117 | 48 | 60 | 101 | 65 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 11 of 27 | 70 | 143 | 93 | 121 | 137 | 91 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 8 of 27 | 79 | 183 | 100 | 126 | 148 | 155 | pts 12.7 vs 9.5-11.9; reb 4.1 vs 3.3-3.9; tpm 2.9 vs 2.1-2.7; tov 1.6 vs 1.1-1.4 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Saddiq Bey | 8 of 27 | 90 | 177 | 108 | 132 | 169 | 157 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Dyson Daniels | 6 of 27 | 22 | 62 | 20 | 64 | 56 | 55 | reb 6.8 vs 5.8-6.4; ast 5.9 vs 4.7-5.5; tpm 0.3 vs 0.5-0.6 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Michael Porter Jr. | 6 of 27 | 32 | 60 | 55 | 62 | 70 | 57 | pts 24.5 vs 18.7-21.8; ast 3 vs 2.4-2.6; stl 0.7 vs 0.8-1; tpm 3.4 vs 2.9-3.1; tov 2.3 vs 1.9-2 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 5 of 27 | 7 | 32 | 15 | 16 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (23 mocks, value 6, market 18); Lauri Markkanen (15 mocks, value 21, market 37); VJ Edgecombe (13 mocks, value 58, market 75); Derrick White (11 mocks, value 29, market 45); Tyrese Maxey (7 mocks, value 5, market 9).


## Bounds

**Out of scope by design.**
- No line, price or engine change: the owner holds every decision until this morning's final pull. §6 is an assessment; it builds no candidate line.
- The punt test and the advice line were not re-run: no punt was declared and no advisor click is in the feed.
- This is a room of random humans, not the league's managers.

**In scope and unverified.**
- The exact Yahoo projection behind the screenshot: `UNVERIFIABLE` from here; the 10/13 per-player file on hand sums to within 3.4 percent of it but not exactly.
- The raw text the owner typed for picks the tool resolved by surname ("assumed over" lines) is not in the paste; the pinned events feed the resolved names. The echoes and the final board match, so the state is the same; the typed strings are `UNVERIFIABLE`.
- Whether the season arms' title share holds against the league's real managers: `UNVERIFIABLE` until the draft.
- Whether WO-5's 2025-26 basis or the pre-WO-5 lines are closer to the 2026-27 outcome for these six: `UNVERIFIABLE` until the season; Yahoo's projected rank sits nearer the new board than the old for all 6 (§6).

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-1013-10..14 | carried as set; the owner's hold until this morning's final pull | hold |
| D-1013-1..9, D-C2, D-SF-1..4 and earlier | carried | carried |

## Provenance

- Inputs: the owner's paste (`draft78-2026-10-13/owner_message.txt`, verbatim) and the screenshot (`yahoo_standings_screenshot.webp`, transcribed to `yahoo_standings_2026-10-13.csv`); deck rev `dd6b719` (Version 65, page sha256 09a889d4baa5); deck revs `df1c754`, `f918062`, `8ec736b`, `73e832c`, `3bd8311`, `f6fb476` for §6.
- Tools: `build_state.py` (state and feed check; handles the UNKNOWN and `✎ #N corrected` lines), the deck's `arena/mocks/live_retro.py` (mock 78 registered: replay, final, hindsight, arms), `live_deckcard.py` (the page's engine; the tool-state run reads the DOM replay's final board through a copy whose only change is the state path), `live_replay_dom.mjs` (the tool log through the real page), `scripts/repeat_market_check.py` (27 mocks), `yahoo_compare.py`, `six_lines.py`, `six_cards.py`, `write_report.py` (this file's writer). Records in `arena/results/m78_*.json` and this folder.
- No line, tag or placement changed; both planes' hashes equal before and after (e821ec1ddc67 kit, bd2b983876a8 deck).

## In plain language

**How the room went.** A good room, not your best: about a 19 percent title share, second of 12, favored against 10 of the other 11 week to week. Yahoo agrees: second, behind Mathieu.

**The pick to learn from.** The first one. At #10 you took Haliburton, ninth on the card; Jalen Johnson, second on it, went two picks later, and with him the roster grades about 7 title points better.

**The UNKNOWN.** #88 never got fixed, so late in the draft the tool still thought Coby White was available. It changed one late suggestion slightly. In the real draft, fix an UNKNOWN as soon as the warning shows.

**Your question.** The engine didn't change; the numbers it is fed did. On 10/12 every player's line was rebuilt from last season (2025-26). These six had weaker 2025-26 seasons than the older lines assumed, so their values fell: Towns from 6th to 24th, Davis 5th to 14th, Jalen Williams 16th to 41st. Before that, the card was pushing them well ahead of where Yahoo and the market rank them (replaying your 27 graded practice rooms on the last page before the rebuild, one of the six was the card's pick at 104 of your 351 turns; on today's page, at 4). Holmgren and Davis still show up on the card when they're available.

**Your decisions.** Nothing new; everything holds until this morning's final pull.
