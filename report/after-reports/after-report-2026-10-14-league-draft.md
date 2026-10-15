# After-report — the league draft, 2026-10-14: the owner's real 12-team league from seat 10, graded and simulated over 10,000 seasons

**Owner request (2026-10-14, verbatim):** "Alright. Final draft is completed- here we go! Proceed with full analysis and simulate 10000 seasons", with the deck tool's LIVE feed, Yahoo's pick list and the draft order (`draft-league-2026-10-14/owner_message.txt`, pinned verbatim).

**League:** 12 teams × 13 rounds, head-to-head nine categories, 18 regular-season weeks, eight teams to an eight-team bracket with no byes. Seats by the draft order: 1 Oblena (Itsy Bitsy Spida); 2 Noah (Devin Minutes in Heaven); 3 Will (The Konclave); 4 Robby (Gotta Be Bamonte); 5 Kyle (ur my only hope Anti-wan); 6 Martin (HalleLuka Amen); 7 John (John's Cool Team); 8 JCo (Wing Chun Wemby); 9 Kevin (All guards no defense); 10 you (Your Team); 11 Cayas (IM SO HORT); 12 Hegi (Not hurt just SARR). **Board:** the locked lines (pool tag v69 = data/players.csv at deck `af91b23`, byte-identical to the current main's); the page in the room was Version 70, whose engine output equals Version 69's.

Pull window: 2026-10-14 → 2026-10-14 (analysis only; no roster pull, no line change).

**Headline.** Over 10,000 simulated seasons your team wins the title **22.50 percent** of the time, the most in the league (rank 1 of 12; the second run of 10,000 on another seed: 21.84 percent, rank 1). Playoffs 98.87 percent, the top seed 43.33 percent, mean seed 2.47, 5.161 categories a week. The nearest rival is Oblena (Itsy Bitsy Spida) at 16.73 percent. Expected weekly category wins 5.144, rank 1 of 12, favored in 11 of 11 head-to-heads. The card's 🎯 was taken at 7 of 13 turns, the Top 5 at 12. The tool's board equals Yahoo's 156 of 156 after 4 undone entries, 3 Insert-at-# and 1 halted name.

## 1. Roster changes

None. No line, tag, placement or price changed on either plane.

## 2. The league over 10,000 seasons

EVIDENCE: `arena/results/m100_league_sim_10k_s2026.json` and `_s2027.json`, written by `arena/mocks/league_sim.py` — the house simulator (`arena.simulate_seasons`: weekly category draws from each roster's daily-fill model, a shared games shock, the category record as the standings, the 1v8/4v5/2v7/3v6 bracket) with each season's seeds and rounds recorded. Before writing, each run re-ran `arena.simulate_seasons` on its seed and asserted equal champion and playoff counts for all 12 teams. Largest difference between the two runs on any team's title or playoff share: 0.88 points.

| seat | manager (team) | title % | title %, 2nd run | final % | playoffs % | top seed % | mean seed | cats a week |
|---|---|---|---|---|---|---|---|---|
| 10 | you (Your Team) | **22.50** | 21.84 | 38.01 | 98.87 | 43.33 | 2.47 | 5.161 |
| 1 | Oblena (Itsy Bitsy Spida) | **16.73** | 15.93 | 30.81 | 95.12 | 15.14 | 3.92 | 4.883 |
| 6 | Martin (HalleLuka Amen) | **14.87** | 15.70 | 29.37 | 94.25 | 15.82 | 4.02 | 4.873 |
| 3 | Will (The Konclave) | **12.92** | 13.17 | 25.52 | 91.75 | 10.97 | 4.49 | 4.796 |
| 2 | Noah (Devin Minutes in Heaven) | **10.46** | 10.49 | 21.07 | 86.87 | 7.03 | 5.24 | 4.684 |
| 11 | Cayas (IM SO HORT) | **9.96** | 10.53 | 21.06 | 87.91 | 3.86 | 5.46 | 4.645 |
| 5 | Kyle (ur my only hope Anti-wan) | **4.09** | 4.28 | 10.89 | 64.50 | 1.53 | 7.25 | 4.396 |
| 4 | Robby (Gotta Be Bamonte) | **3.86** | 3.58 | 10.01 | 62.21 | 1.47 | 7.41 | 4.371 |
| 8 | JCo (Wing Chun Wemby) | **2.29** | 2.19 | 6.31 | 48.22 | 0.61 | 8.26 | 4.245 |
| 7 | John (John's Cool Team) | **1.62** | 1.56 | 4.48 | 38.38 | 0.16 | 8.85 | 4.158 |
| 9 | Kevin (All guards no defense) | **0.39** | 0.44 | 1.41 | 16.11 | 0.02 | 10.34 | 3.879 |
| 12 | Hegi (Not hurt just SARR) | **0.31** | 0.29 | 1.06 | 15.81 | 0.06 | 10.28 | 3.908 |

Your finishing seed over the 10,000 seasons: #1 43.3%, #2 21.4%, #3 12.7%, #4 8.2%, #5 5.8%, #6 3.8%, #7 2.3%, #8 1.5%, #9 0.6%, #10 0.4%, #11 0.1%.

## 3. Your team

EVIDENCE: `recap.json` (Yahoo's listing: positions and status as Yahoo printed them), the pool's availability multiplier (`hoops.availability`), the page's card record.

| pick | player | NBA team | Yahoo positions | Yahoo status | availability on the board | card rank at the pick |
|---|---|---|---|---|---|---|
| #10 | Tyrese Haliburton | IND | PG,SG | — | 1.00 | 2 |
| #15 | Kevin Durant | HOU | SG,SF,PF | Q | 1.00 | 1 |
| #34 | Kawhi Leonard | TOR | SG,SF,PF | — | 0.78 | 1 |
| #39 | Derrick White | BOS | PG,SG | — | 1.00 | 1 |
| #58 | Kyrie Irving | DAL | PG | Q | 0.85 | 1 |
| #63 | Kel'el Ware | MIL | C | — | 1.00 | 2 |
| #82 | Ty Jerome | MEM | PG,SG | — | 1.00 | 1 |
| #87 | Jaden McDaniels | MIN | SF | — | 1.00 | 1 |
| #106 | Miles Bridges | PHX | PF | Q | 1.00 | 1 |
| #111 | Yaxel Lendeborg | GSW | PF | — | 1.00 | 3 |
| #130 | Neemias Queta | BOS | C | — | 1.00 | 2 |
| #135 | PJ Washington | DAL | PF,C | — | 1.00 | 9 |
| #154 | Christian Braun | DEN | SG,SF,PF | — | 1.00 | 3 |

Category profile — the share of weeks your team wins each category, and its rank among the 12 (10,000 seasons, seed 2026):

| FG% | FT% | 3PTM | PTS | REB | AST | ST | BLK | TO |
|---|---|---|---|---|---|---|---|---|
| 58.1% (#4) | 73.7% (#2) | 60.4% (#5) | 41.2% (#9) | 40.8% (#9) | 32.7% (#12) | 51.4% (#6) | 70.3% (#3) | 87.4% (#1) |

Strongest: FT%, BLK, TO; weakest: PTS, REB, AST. The weekly model's category ranks (`m100_final.json`): FG% 4, FT% 2, 3PTM 5, PTS 9, REB 9, AST 12, ST 6, BLK 3, TO 1.

Expected categories a week against each opponent (`m100_final.json`, the weekly model; 4.5 is even):

| opponent | expected cats | your categories above 50% |
|---|---|---|
| Oblena (Itsy Bitsy Spida) | 4.621 | FG%, FT%, ST, BLK, TO |
| Martin (HalleLuka Amen) | 4.711 | FG%, FT%, 3PTM, BLK, TO |
| Noah (Devin Minutes in Heaven) | 4.758 | FG%, FT%, TO |
| Will (The Konclave) | 4.770 | FG%, FT%, ST, BLK, TO |
| Cayas (IM SO HORT) | 4.893 | FG%, REB, BLK, TO |
| Kyle (ur my only hope Anti-wan) | 5.259 | FT%, 3PTM, PTS, REB, BLK, TO |
| Robby (Gotta Be Bamonte) | 5.313 | FG%, FT%, 3PTM, ST, BLK, TO |
| John (John's Cool Team) | 5.398 | FG%, FT%, 3PTM, ST, BLK, TO |
| JCo (Wing Chun Wemby) | 5.446 | FT%, 3PTM, REB, ST, BLK, TO |
| Kevin (All guards no defense) | 5.652 | FG%, FT%, 3PTM, PTS, ST, TO |
| Hegi (Not hurt just SARR) | 5.761 | FT%, 3PTM, PTS, BLK, TO |

## 4. Pick by pick: the page's card, your pick, hindsight

EVIDENCE: `m100_deckcard_v69.json` (the page's own engine on Yahoo's board before each of your turns), `m100_hindsight.json` (every single-swap alternative scored by weekly category wins against the final rosters).

| pick | you took | card rank | the page's 🎯 | gap to 🎯 | hindsight's best alternative (Δ weekly cat wins) |
|---|---|---|---|---|---|
| #10 | Tyrese Haliburton | 2 | Tyrese Maxey | 0.005 | Tyrese Maxey (+0.007) |
| #15 | Kevin Durant | 1 | Kevin Durant | — | Jalen Johnson (+0.132) |
| #34 | Kawhi Leonard | 1 | Kawhi Leonard | — | Domantas Sabonis (+0.087) |
| #39 | Derrick White | 1 | Derrick White | — | James Harden (+0.021) |
| #58 | Kyrie Irving | 1 | Kyrie Irving | — | Michael Porter Jr. (+0.024) |
| #63 | Kel'el Ware | 2 | Dyson Daniels | 0.002 | Michael Porter Jr. (+0.060) |
| #82 | Ty Jerome | 1 | Ty Jerome | — | none better (closest Immanuel Quickley, -0.019) |
| #87 | Jaden McDaniels | 1 | Jaden McDaniels | — | Josh Hart (+0.055) |
| #106 | Miles Bridges | 1 | Miles Bridges | — | none better (closest Kyshawn George, -0.045) |
| #111 | Yaxel Lendeborg | 3 | Jakob Poeltl | 0.015 | Kyshawn George (+0.058) |
| #130 | Neemias Queta | 2 | Jakob Poeltl | 0.012 | Kyshawn George (+0.037) |
| #135 | PJ Washington | 9 | Jakob Poeltl | off the Top 5 | Kyshawn George (+0.045) |
| #154 | Christian Braun | 3 | Tobias Harris | 0.004 | Draymond Green (+0.061) |

The turns off the 🎯 and where the 🎯 went: #10 Tyrese Haliburton (🎯 Tyrese Maxey, taken #11 by Cayas (IM SO HORT)); #63 Kel'el Ware (🎯 Dyson Daniels, taken #67 by Martin (HalleLuka Amen)); #111 Yaxel Lendeborg (🎯 Jakob Poeltl, taken #151 by John (John's Cool Team)); #130 Neemias Queta (🎯 Jakob Poeltl, taken #151 by John (John's Cool Team)); #135 PJ Washington (🎯 Jakob Poeltl, taken #151 by John (John's Cool Team)); #154 Christian Braun (🎯 Tobias Harris, undrafted).

### 4b. Were your picks better than the card's?

EVIDENCE: `card_vs_owner.py` → `card_vs_owner.json`. At each of your six turns off the 🎯, the 🎯 was swapped in for your pick on Yahoo's final board — pairwise, as the house arms do: the seat that took the 🎯 later gets your player instead (an undrafted 🎯 leaves your player undrafted). Each swap scored by expected weekly category wins and by title share over 10,000 seasons on both seeds (the baselines' seeds, so the dice line up). Negative = your pick was better.

| pick | you took | the card's 🎯 (where it went) | Δ cats a week if 🎯 | Δ title % if 🎯 (seed 2026 / 2027) | verdict |
|---|---|---|---|---|---|
| #10 | Tyrese Haliburton | Tyrese Maxey (#11 seat 11) | +0.0069 | +0.79 / +0.78 | the card's pick was better |
| #63 | Kel'el Ware | Dyson Daniels (#67 seat 6) | +0.0074 | -0.29 / -0.11 | your pick was better (inside the noise) |
| #111 | Yaxel Lendeborg | Jakob Poeltl (#151 seat 7) | +0.0002 | -0.69 / -0.20 | your pick was better |
| #130 | Neemias Queta | Jakob Poeltl (#151 seat 7) | +0.0105 | -0.48 / -0.41 | your pick was better (inside the noise) |
| #135 | PJ Washington | Jakob Poeltl (#151 seat 7) | -0.0171 | -1.20 / -0.57 | your pick was better |
| #154 | Christian Braun | Tobias Harris (undrafted) | +0.0086 | +0.13 / +0.41 | the card's pick was better (inside the noise) |

On title share your pick beat the 🎯 at 4 of 6 turns (#63 Kel'el Ware, #111 Yaxel Lendeborg, #130 Neemias Queta, #135 PJ Washington) and the 🎯 beat yours at 2 (#10 Tyrese Maxey over Tyrese Haliburton, #154 Tobias Harris over Christian Braun). On the card's own measure (cats a week against the final rosters) the 🎯 edges five of the six by 0.011 or less — differences that small sit inside projection error. The two measures can disagree because a pairwise swap also hands a rival your player: the three Poeltl turns would have given John's team Lendeborg, Queta or Washington. The three Poeltl rows are alternatives, not a sum — Poeltl could be taken once.

## 5. What-ifs (the house arms: 18,000 seasons each, seeds 11/23/47 — the method every mock was graded on)

EVIDENCE: `m100_arms.json`. These use the house seeds, not the 10,000-season runs above, so the as-drafted line differs from §2 by Monte-Carlo noise.

| arm | title % | playoffs % | rank |
|---|---|---|---|
| as drafted | 21.78 | 98.85 | 1 |
| follow the card's 🎯 at every turn (#10 Tyrese Maxey, #15 Jalen Johnson, #87 Josh Hart, #111 Jakob Poeltl, #135 Reed Sheppard) | 24.55 | 99.33 | 1 |
| single swap at #15: Jalen Johnson | 23.97 | 99.35 | 1 |
| single swap at #63: Michael Porter Jr. | 23.83 | 99.22 | 1 |
| single swap at #111: Kyshawn George | 23.77 | 99.23 | 1 |
| single swap at #130: Kyshawn George | 23.48 | 99.09 | 1 |
| single swap at #154: Draymond Green | 23.45 | 99.21 | 1 |
| single swap at #135: Kyshawn George | 23.24 | 99.22 | 1 |
| single swap at #34: Domantas Sabonis | 23.02 | 99.26 | 1 |
| single swap at #58: Michael Porter Jr. | 22.70 | 99.06 | 1 |
| single swap at #10: Tyrese Maxey | 22.68 | 99.03 | 1 |
| single swap at #87: Josh Hart | 22.46 | 98.98 | 1 |
| single swap at #39: James Harden | 21.61 | 98.80 | 1 |

## 6. Injury stress: one headline name misses the whole season (10,000 seasons, seed 2026)

EVIDENCE: `stress.json` (`stress.py`): the player's slot is filled by the best undrafted player on the board (Tobias Harris), the pickup a manager would make; the rest of the league unchanged. The board's availability multipliers already price ordinary missed games; this is the tail case.

| out for the season | title % | rank | playoffs % | mean seed | league leader then |
|---|---|---|---|---|---|
| nobody (as drafted) | 22.50 | 1 | 98.87 | 2.47 | you |
| Tyrese Haliburton | 11.43 | 5 | 89.87 | 4.77 | Oblena (Itsy Bitsy Spida) (17.63) |
| Kevin Durant | 11.25 | 5 | 90.35 | 4.55 | Oblena (Itsy Bitsy Spida) (18.71) |
| Kawhi Leonard | 14.23 | 4 | 94.18 | 3.88 | Oblena (Itsy Bitsy Spida) (17.99) |
| Kyrie Irving | 15.66 | 3 | 95.45 | 3.62 | Oblena (Itsy Bitsy Spida) (17.59) |

## 7. The waiver wire at the draft's end

EVIDENCE: `waiver.json` — the undrafted players by the board's value (availability > 0).

| # | player | team | positions | availability |
|---|---|---|---|---|
| 1 | Tobias Harris | SAS | PF | 1.00 |
| 2 | Tre Jones | CHI | PG,SG | 1.00 |
| 3 | Robert Williams III | POR | C | 0.78 |
| 4 | Bobby Portis | MIA | PF,C | 1.00 |
| 5 | Alex Caruso | OKC | SG,SF | 1.00 |
| 6 | Aaron Nesmith | IND | SG,SF | 1.00 |
| 7 | Paul Reed | DET | C,PF | 1.00 |
| 8 | Jrue Holiday | POR | PG,SG | 1.00 |
| 9 | Scotty Pippen Jr. | MEM | PG | 1.00 |
| 10 | Wendell Carter Jr. | ORL | C | 1.00 |

## 7b. Pickups tested: every add/drop pair

EVIDENCE: `waiver_moves.py` → `waiver_moves.json`: the 40 best undrafted players (availability > 0, the owner's veto off) × your 13 = 520 pairs, each scored by expected weekly category wins against the eleven final rosters (the card's own measure; your baseline 5.1439). **8 of 520 pairs improve the team**, and every one drops Braun, Queta, Washington or Lendeborg; no undrafted player improves on any of your top nine. The best pairs then ran 10,000 seasons each through the verified simulator, on the baseline's seed 2026 and again on seed 2027 (`waiver_moves_s2027.json`).

| add | drop | Δ cats a week | title %, seed 2026 (Δ) | title %, seed 2027 (Δ) | categories that move most |
|---|---|---|---|---|---|
| Draymond Green (GSW) | Christian Braun | +0.0606 | 24.04 (+1.54) | 23.56 (+1.72) | AST +0.15, TO -0.11, FG% -0.06 |
| Bobby Portis (MIA) | Christian Braun | +0.0288 | 23.39 (+0.89) | 22.99 (+1.15) | REB +0.08, 3PTM +0.06, AST -0.04 |
| Jrue Holiday (POR) | Christian Braun | +0.0124 | 23.19 (+0.69) | 22.00 (+0.16) | AST +0.09, 3PTM +0.07, TO -0.05 |
| Tobias Harris (SAS) | Christian Braun | +0.0086 | 22.63 (+0.13) | — | FG% -0.04, FT% +0.02, 3PTM +0.02 |
| Aaron Nesmith (IND) | Christian Braun | +0.0039 | 22.96 (+0.46) | — | 3PTM +0.10, FG% -0.05, AST -0.04 |
| Draymond Green (GSW) | Neemias Queta | +0.0253 | 23.00 (+0.50) | 22.60 (+0.76) | AST +0.20, 3PTM +0.10, TO -0.10 |

**The availability test (the critical one).** Draymond Green's line on the board carries full availability (1.00). Run again with Green at the board's risk tier (0.78 ranking / 0.75 weekly — `waiver_draymond_risk.json`), the same Green-for-Braun swap grades 21.25 and 20.54 percent: **below** the as-drafted 22.50 / 21.84. The move's whole gain rests on Green playing a normal schedule. Web check 2026-10-15 (`web_receipts_2026-10-15.md`, leads not box scores): ESPN lists him day-to-day (rest) with a return estimate of Oct 16; RotoWire and Fox Sports report preseason rest games and limited minutes ahead of the Oct 21 opener.

Monte-Carlo error on a single 10,000-season title share is about ±0.4 points (one standard error at 22%); the paired runs share their dice, so a difference that keeps its sign on both seeds is the signal. Green-for-Braun (+1.54 / +1.72) and Portis-for-Braun (+0.89 / +1.15) keep their sign; Holiday (+0.69 / +0.16) is inside the noise.


## 8. Tool-state integrity

recap picks 156; seats 12; managers 1 Oblena (Itsy Bitsy Spida), 2 Noah (Devin Minutes in Heaven), 3 Will (The Konclave), 4 Robby (Gotta Be Bamonte), 5 Kyle (ur my only hope Anti-wan), 6 Martin (HalleLuka Amen), 7 John (John's Cool Team), 8 JCo (Wing Chun Wemby), 9 Kevin (All guards no defense), 10 Me (Your Team), 11 Cayas (IM SO HORT), 12 Hegi (Not hurt just SARR); name resolution: initial+surname, unique 143; initial+surname+team 12; initial+surname, tool log as tie-break 1; tie-breaks by the tool log: #38 J. Williams (OKC): candidates Jalen Williams (OKC), Jaylin Williams (OKC); the tool log has Jalen Williams; Yahoo team differs from the pool's team: 0 []; feed vs recap: 156 of 156 agree on name and seat; differences []; owner picks: #10 Tyrese Haliburton, #15 Kevin Durant, #34 Kawhi Leonard, #39 Derrick White, #58 Kyrie Irving, #63 Kel'el Ware, #82 Ty Jerome, #87 Jaden McDaniels, #106 Miles Bridges, #111 Yaxel Lendeborg, #130 Neemias Queta, #135 PJ Washington, #154 Christian Braun; events 165: feed 157, undo 4, insert 3, HALTED 1; feeds later undone 4: Tyrese Maxey, Derrick White, Deni Avdija, Keyonte George.

EVIDENCE: the typed sequence rebuilt in `arena/data/events/m100_tool_events.json` (165 events) replayed through the page in headless Chromium (`replay_v70.json`): 0 echo misses, 0 clock mismatches, 0 page errors, 156 picks; the final board equals Yahoo's at all 156 picks; every "off the card" line of the paste (8) and every shift line (2) is reproduced character for character.

| what happened | the log | what the tool did |
|---|---|---|
| entries undone and re-entered | 4 undo lines: Tyrese Maxey, Derrick White, Deni Avdija, Keyonte George | each removed and the board re-entered; the board after equals Yahoo's |
| a missed pick restored at #55 | "inserted Ivica Zubac at #55" (to seat 7) | the later picks shifted one place and were re-seated by the snake |
| a missed pick restored at #98 | "inserted AJ Dybantsa at #98" (to seat 2) | the later picks shifted one place and were re-seated by the snake |
| a missed pick restored at #120 | "inserted Ja Morant at #120" (to seat 1) | the later picks shifted one place and were re-seated by the snake |
| a bare "Allen" with the best namesake already taken | "HALTED at \"Allen\"" | nothing logged; the fuller name was then entered |

**Two log-display defects, neither touching the board or the card.** (a) The paste's history shows each undone entry under the name of the pick's later occupant ("#10 Tyrese Haliburton" above "undid: Tyrese Maxey"; "#38 Jalen Williams" and "#39 Derrick White" above the undos of Avdija and White): an Insert-at-# re-renders the history from the state (D59-1), undone lines included; the undo lines name what was removed, and the replay rebuilt from them reproduces the paste. (b) At the #98 insert the log said "#59 Keyonte George is no longer your pick after the shift": George was never your pick on the final board; `relabelLog` (`docs/draft-deck.html`, ~line 1050) maps every history line that carries a pick index — undone entries included — to the state's current pick there, and calls a line "moved off" when its old text had "(YOU)" and the current occupant is not yours; the undone George entry (typed when the tool was one pick short, so it sat on your seat) was re-mapped to #59, where the re-entered George sits for seat 11. The shift line at #58 (D83-1's message) said "Kyrie Irving is the 🎯" — on this board it was true: the card had Kyrie #1 at #58.

The 2 "off the card" lines for entries later undone (Deni Avdija, Keyonte George) were the card's verdicts on mis-seated entries, not on your picks.

## 10. Your opponents against their own history

EVIDENCE: `opponents_vs_history.py` → `opponents_vs_history.json`; history from `arena/draft_boards.json` (three seasons, 156 picks each) and `arena/profiles.json` (the E18 manager profiles). **Value reach** = pick − 9-cat value rank (room_model.py's formula; positive = took fallers, negative = reached past value), 2025-26 on that season's frozen pool and 2026 on the lock pool — two different pools, so the levels compare loosely and the order of managers is the firmer test. **Market reach** = pick − Yahoo ADP (2026 only; there is no earlier ADP file). **Guard share** = picks eligible at PG or SG. Rank agreement of early value reach, 2025-26 against 2026, across the eleven: Spearman +0.40 (n = 11) — a weak link; with eleven managers it is not distinguishable from chance.

| manager (team) | early value reach, 2025-26 to 2026 | whole-draft value reach, 2025-26 to 2026 | market reach 2026 (early) | guard share 2026 (2025-26 / 24-25 / 23-24) | took again from his own past drafts | the profile's loyalty names: taken / gone elsewhere |
|---|---|---|---|---|---|---|
| Oblena (Itsy Bitsy Spida) | +9.3 to +0.5 | -5.5 to -7.8 | +7.1 (-1.2) | 0.54 (0.46 / 0.54 / 0.62) | Chet Holmgren, Darius Garland, Ja Morant | — / Donovan Mitchell #19 Martin |
| Noah (Devin Minutes in Heaven) | -43.5 to -4.0 | -30.9 to -6.4 | +2.5 (-3.4) | 0.46 (0.62 / 0.54 / 0.58) | LaMelo Ball | LaMelo Ball / — |
| Will (The Konclave) | -16.5 to -1.0 | -7.4 to -15.2 | +2.2 (-5.7) | 0.46 (0.54 / 0.58 / 0.45) | Mikal Bridges, Onyeka Okongwu | Onyeka Okongwu / Jaden Ivey undrafted |
| Robby (Gotta Be Bamonte) | -25.7 to -20.7 | -18.8 to -2.2 | +7.7 (+4.5) | 0.62 (0.54 / 0.54 / 0.54) | Bam Adebayo, Devin Booker, Fred VanVleet, Jaylen Brown | Devin Booker / Jarrett Allen #56 JCo; Collin Sexton #152 JCo; Devin Vassell #131 Cayas |
| Kyle (ur my only hope Anti-wan) | -7.0 to -9.5 | -1.0 to +3.8 | -1.7 (-9.0) | 0.54 (0.54 / 0.42 / 0.62) | Rudy Gobert | — / — |
| Martin (HalleLuka Amen) | -14.8 to +2.0 | -4.4 to +8.6 | +11.9 (+4.4) | 0.62 (0.54 / 0.54 / 0.55) | Donovan Mitchell, Jalen Brunson, Jalen Duren, Kyshawn George, Pascal Siakam | — / Luka Doncic #3 Will; Brandon Ingram #79 John; Jalen Suggs #92 Kyle |
| John (John's Cool Team) | -8.0 to -20.5 | -1.3 to -17.9 | +3.1 (+0.1) | 0.31 (0.31 / 0.38 / 0.67) | Aaron Gordon, Cameron Johnson, Jakob Poeltl, Julius Randle, Zach LaVine | Jakob Poeltl / Tyrese Maxey #11 Cayas; Jeremy Sochan undrafted |
| JCo (Wing Chun Wemby) | +4.3 to +7.3 | -15.0 to -3.8 | +5.8 (-0.3) | 0.54 (0.46 / 0.46 / 0.25) | DeMar DeRozan, Zion Williamson | — / Tyrese Haliburton #10 Me; Jimmy Butler III #156 Hegi; Nic Claxton #129 Kevin |
| Kevin (All guards no defense) | -15.8 to -37.5 | +10.0 to -28.1 | +3.7 (-2.1) | 0.46 (0.46 / 0.33 / 0.46) | Quentin Grimes | — / Pascal Siakam #54 Martin |
| Cayas (IM SO HORT) | +5.5 to -3.8 | +8.7 to +3.4 | +4.7 (-0.4) | 0.62 (0.46 / 0.54 / 0.33) | Franz Wagner, Jalen Williams, Joel Embiid | — / — |
| Hegi (Not hurt just SARR) | -26.0 to -6.3 | -17.2 to -13.2 | -0.6 (-7.2) | 0.54 (0.5 / 0.46 / 0.5) | — | — / Immanuel Quickley #86 Cayas; Andrew Wiggins #102 Martin |

**What held, what broke.**

- **Loyalty is weak.** Of the 20 manager–player pairs the profiles list as repeat picks, 4 repeated (Booker to Robby, Okongwu to Will, Poeltl to John, LaMelo Ball to Noah). The profile's own note says league-wide repetition runs at chance; tonight agrees.
- **The model's named prediction missed.** The profile gave Robby drafting Jarrett Allen a 0.77 chance; Robby took Banchero at #52 and Allen went to JCo at #56.
- **Held to type:** Robby (early reach -25.7 → -20.7; at or after Yahoo's ADP early, +4.5 — the market-anchored, name-brand drafter the profile describes); Kyle (mild reacher, -7.0 → -9.5); JCo (value-anchored, +4.3 → +7.3); Oblena's shape (better early than late in both years); John's light guard share (0.31, against 0.31 a year ago).
- **Changed:** Martin — the reigning champion and the profile's apex threat — drafted value this time (early -14.8 → +2.0; on average he took players +11.9 places after their ADP), and he is third in the 10,000 seasons. Kevin reached far harder against the board (-15.8 → -37.5) while staying near ADP (-2.1): he drafted the market, and our board disagrees with the market on his players. His guard-heavy label did not show (0.46). John reached more than before (-8.0 → -20.5). Hegi and Will reached less early than their histories. Noah's −43.5 was 2025-26's autodraft geometry (the profile's own correction); drafting by hand he sat near value (-4.0).
- **Caution on the measure:** value reach is measured against our own board. A manager who drafts the market looks like a reacher wherever our board and the market disagree (Kevin is the clearest case). The market column is the neutral one.
- **What the sim does not see:** the in-season grinders. Will (83 moves last season), Martin (50, and the title), Oblena (69) and Cayas (61) streamed and churned heavily; the 10,000 seasons freeze every roster at the draft, so their real chances are likely higher than modelled, and the gap to you likely smaller.

## 11. Retro: who else was on the board at each of your picks, and what each would have done to your title odds

EVIDENCE: `retro_picks.py` → `retro_picks.json`. At each of your 13 turns, `m100_hindsight.json` scores every legal alternative by expected weekly category wins (ECW) against the final rosters. The three alternatives with the largest positive gain at each turn (or, where nobody beat your pick, the single closest) were swapped in for your pick on Yahoo's final board, pairwise as in §4b: the seat that drafted the alternative later gets your player instead; an undrafted alternative leaves your player undrafted. Each of the 27 swaps ran 10,000 seasons through the verified simulator on seeds 2026 and 2027, the baselines' seeds (22.50 / 21.84 percent), so each swap and its baseline share their random draws. The script ran twice with identical results, and its #10 Maxey row equals §4b's. **Verdict rule:** better than yours only when both seeds exceed +0.5 title points; yours was better when both fall below −0.5; anything else is inside the noise (the two seeds differ by 0.30 points on average across these rows). **Cross-check:** 11 of these swaps also exist in the house arms (§5: 18,000 seasons on seeds 11/23/47, a different set of dice); the direction agrees at 11 of 11.

| pick | you took | alternative (drafted at, by) | ECW gain | title shift, seed 2026 / 2027 | mean | players with an ECW gain over yours | verdict |
|---|---|---|---|---|---|---|---|
| #10 | Tyrese Haliburton | Tyrese Maxey (#11, Cayas) | +0.007 | +0.79 / +0.78 | +0.79 | 1 of 295 | better than yours |
| #15 | Kevin Durant | Jalen Johnson (#18, John) | +0.132 | +2.17 / +1.81 | +1.99 | 7 of 291 | better than yours |
| #15 | Kevin Durant | Donovan Mitchell (#19, Martin) | +0.046 | +0.97 / +1.12 | +1.04 | 7 of 291 | better than yours |
| #15 | Kevin Durant | Jamal Murray (#20, Kyle) | +0.038 | +0.62 / +0.18 | +0.40 | 7 of 291 | inside the noise |
| #34 | Kawhi Leonard | Domantas Sabonis (#36, Hegi) | +0.087 | +0.79 / +1.37 | +1.08 | 2 of 273 | better than yours |
| #34 | Kawhi Leonard | James Harden (#46, Will) | +0.080 | +1.81 / +1.90 | +1.85 | 2 of 273 | better than yours |
| #39 | Derrick White | James Harden (#46, Will) | +0.021 | -0.47 / -0.76 | -0.61 | 1 of 269 | inside the noise |
| #58 | Kyrie Irving | Michael Porter Jr. (#72, Oblena) | +0.024 | +0.55 / +1.02 | +0.79 | 2 of 251 | better than yours |
| #58 | Kyrie Irving | Franz Wagner (#62, Cayas) | +0.018 | -0.41 / -0.02 | -0.21 | 2 of 251 | inside the noise |
| #63 | Kel'el Ware | Michael Porter Jr. (#72, Oblena) | +0.060 | +1.57 / +1.31 | +1.44 | 3 of 247 | better than yours |
| #63 | Kel'el Ware | Naz Reid (#78, Martin) | +0.034 | +1.52 / +1.25 | +1.39 | 3 of 247 | better than yours |
| #63 | Kel'el Ware | Dyson Daniels (#67, Martin) | +0.007 | -0.29 / -0.11 | -0.20 | 3 of 247 | inside the noise |
| #82 | Ty Jerome | Immanuel Quickley (#86, Cayas) | -0.019 | -1.33 / -1.11 | -1.22 | 0 of 229 | yours was better |
| #87 | Jaden McDaniels | Josh Hart (#99, Will) | +0.055 | +0.33 / +0.66 | +0.49 | 2 of 225 | inside the noise |
| #87 | Jaden McDaniels | Caleb Wilson (#91, Martin) | +0.035 | +0.65 / +0.84 | +0.74 | 2 of 225 | better than yours |
| #106 | Miles Bridges | Kyshawn George (#150, Martin) | -0.045 | -1.54 / -0.68 | -1.11 | 0 of 207 | yours was better |
| #111 | Yaxel Lendeborg | Kyshawn George (#150, Martin) | +0.058 | +1.84 / +1.57 | +1.71 | 6 of 203 | better than yours |
| #111 | Yaxel Lendeborg | Cedric Coward (#115, Martin) | +0.035 | +0.49 / +0.63 | +0.56 | 6 of 203 | inside the noise |
| #111 | Yaxel Lendeborg | Draymond Green (undrafted) | +0.026 | +0.79 / +0.36 | +0.57 | 6 of 203 | inside the noise |
| #130 | Neemias Queta | Kyshawn George (#150, Martin) | +0.037 | +1.40 / +0.75 | +1.07 | 3 of 162 | better than yours |
| #130 | Neemias Queta | Draymond Green (undrafted) | +0.025 | +0.50 / +0.76 | +0.63 | 3 of 162 | inside the noise |
| #130 | Neemias Queta | Jakob Poeltl (#151, John) | +0.011 | -0.48 / -0.41 | -0.44 | 3 of 162 | inside the noise |
| #135 | PJ Washington | Kyshawn George (#150, Martin) | +0.045 | +0.68 / +0.86 | +0.77 | 2 of 158 | better than yours |
| #135 | PJ Washington | Draymond Green (undrafted) | +0.022 | +0.41 / +0.42 | +0.41 | 2 of 158 | inside the noise |
| #154 | Christian Braun | Draymond Green (undrafted) | +0.061 | +1.54 / +1.72 | +1.63 | 5 of 141 | better than yours |
| #154 | Christian Braun | Bobby Portis (undrafted) | +0.029 | +0.89 / +1.15 | +1.02 | 5 of 141 | better than yours |
| #154 | Christian Braun | Jrue Holiday (undrafted) | +0.012 | +0.69 / +0.16 | +0.42 | 5 of 141 | inside the noise |

**Reading it.**

- **Turns where a clearly better player was on the board (10 of 13):** #10 Tyrese Maxey over Tyrese Haliburton (+0.79); #15 Jalen Johnson over Kevin Durant (+1.99); #34 James Harden over Kawhi Leonard (+1.85); #58 Michael Porter Jr. over Kyrie Irving (+0.79); #63 Michael Porter Jr. over Kel'el Ware (+1.44); #87 Caleb Wilson over Jaden McDaniels (+0.74); #111 Kyshawn George over Yaxel Lendeborg (+1.71); #130 Kyshawn George over Neemias Queta (+1.07); #135 Kyshawn George over PJ Washington (+0.77); #154 Draymond Green over Christian Braun (+1.63).
- **Turns where your pick stands (3 of 13):** #39 Derrick White, #82 Ty Jerome, #106 Miles Bridges. At #82 and #106 no legal alternative beat your pick even by ECW; at #39 Harden's small ECW gain turns into a loss in the seasons.
- **The largest single miss is #15:** Jalen Johnson, taken three picks later by John, instead of Durant. The second tier is the same shape: Harden at #34, MPJ or Naz Reid at #63, Kyshawn George at #111 (still on the board until #150), and Draymond at #154 (never drafted).
- **The same player recurs.** Kyshawn George is the top alternative at #111, #130 and #135, and Draymond at four turns; you could have had each once. MPJ is the top alternative at both #58 and #63.
- **Where the alternative went matters.** Harden instead of Kawhi at #34 is +1.85; Harden instead of White at #39 is −0.61. In the first swap Will (seat 3) receives Kawhi at #46, in the second White. Every shift includes what the displaced player does on the seat that receives that player; it is not a pure measure of the two players.
- **Hindsight's ceiling.** All the better picks at once, each player used once (#10 Tyrese Maxey, #15 Jalen Johnson, #34 James Harden, #58 Michael Porter Jr., #63 Naz Reid, #87 Caleb Wilson, #111 Kyshawn George, #130 Draymond Green, #154 Bobby Portis), give a title share of 28.58 / 28.67 percent: +6.08 / +6.83 points. That is far below the sum of the single shifts (+10.9): gains overlap, and each swap also strengthens a rival. For scale, following the card at every turn graded 24.55 percent against 21.78 as drafted on the house arms (different seeds). The ceiling is perfect hindsight, not an attainable draft: it knows who every opponent took later.

## 9. Critical review: what this analysis can and cannot tell you

1. **The title share is model-relative.** Every season is simulated on the lock's projection lines. The integrity audit put projection confidence at 97.8%, but that figure mostly measures agreement with consensus (the lines sit about five-sixths of the way to it): if the consensus is wrong about a player, so is this. Real projection error is the largest uncertainty here, larger than the ±0.4-point Monte-Carlo error or the 0.88-point spread between two runs.
2. **The grader and the card are the same engine.** "Following the 🎯 would have graded higher" and "hindsight's best alternative" are measured by the model that produced the card. They show internal consistency, not that the card is right about basketball.
3. **Hindsight uses information you did not have.** §4's alternatives are scored against the final rosters; at the pick, the later picks were unknown. Hindsight gains of 0.1 cats a week or less are small against projection error.
4. **The schedule is average, not yours.** Pairings are drawn at random each week; the league's real schedule (not in either repository) decides any one season's luck.
5. **Opponents stand still.** No trades, streaming or waiver moves by anyone after the draft; the eleven rosters are frozen. Active managers will move the table; the stress test (§6) and the pickup test (§7b) are the only in-season changes modelled.
6. **Availability is the lock's.** Yahoo flags Durant, Kyrie and Miles Bridges questionable; the board carries Durant and Bridges at full availability. Injury news since the lock was not pulled (did not check), apart from the three pickup-relevant names in `web_receipts_2026-10-15.md`. §6 shows what a full-season loss costs: about half the title share for Haliburton or Durant.
7. **The simulator was verified against the house simulator, not against reality.** `league_sim.py` equals `arena.simulate_seasons` draw for draw; that proves the extension is faithful, not that the season model is calibrated. The model's last calibration evidence is in earlier reports (the 2025-26 what-if and survival work), not re-run tonight.
8. **Your team's shape is a real exposure.** Last in assists and ninth in points and rebounds: you win weeks through efficiency and defense (FT%, BLK, TO). A team built that way can drop weeks when one shooter goes cold or one center misses time; the category win shares in §3 are averages over 10,000 seasons, not a promise for any given week.
9. **The pickup test is narrow.** It tries one add for one drop against frozen rosters, using undrafted players by the board's value (top 40). It does not test two-for-one moves, trades, or streaming for games.

## Watchlist

- The two injury-tail names that move the title share most: Kevin Durant (11.2% if out), Tyrese Haliburton (11.4% if out). Their status is the first thing to watch in the season's first weeks.
- The weak categories (PTS, REB, AST) are where waiver and trade moves pay; the strong ones (FT%, BLK, TO) are what to protect.
- Yahoo's status column at the draft flags Kevin Durant (Q), Kyrie Irving (Q), Miles Bridges (Q); the board carries them at availability 1.00, 0.85, 1.00. What the flags mean today was not checked (no pull tonight): the first in-season pull should read them.
- The log-display defects (§8) and D83-1 wait for after the draft; nothing in them changed a pick or the card.

## Open-item receipts

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| (this draft) | records only; no web research and no roster pull | Yahoo's 156 names resolve to the lock pool 156 of 156; Yahoo's NBA team agrees with the pool's at all 156 |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this grade (did not check) |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 beb243ef57af), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 33 of 33 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 32 of 33 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 23 of 33 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 14 of 33 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 33 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| John Collins | 12 of 33 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 11 of 33 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 10 of 33 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 10 of 33 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 7 of 33 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 6 of 33 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 33 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 33 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (17 mocks, value 27, market 45); Lauri Markkanen (15 mocks, value 21, market 37); Tyrese Haliburton (13 mocks, value 7, market 12); Tyrese Maxey (11 mocks, value 5, market 9); Kel'el Ware (10 mocks, value 57, market 77); Tyler Herro (9 mocks, value 51, market 69); Karl-Anthony Towns (8 mocks, value 12, market 15); Miles Bridges (5 mocks, value 96, market 98).


## Bounds

**Out of scope by design.**
- No line, price or engine change; the lines are the lock's.
- The league's real weekly schedule is not in either repository: the simulation draws the pairings at random each week, so each team meets an average schedule. A real schedule moves an individual season, not the 10,000-season shares much.
- In-season management (streaming, trades, waiver moves) is not modelled beyond the daily-fill start rates; §6 is the only replacement modelled.
- §11 simulates only the top three alternatives by ECW at each turn; a player lower on ECW whose title shift would have been larger is not tested. The swaps are single changes on the final board: they do not model how the rest of the draft would have unfolded after a different pick.

**In scope and unverified.**
- Injury news after the 10/14 lock: did not check (no pull tonight); the board's availability multipliers are the lock's.
- The projections themselves: the 10,000 seasons inherit the lock's lines; the integrity audit's projection confidence (97.8%) and its caveat (the lines sit close to the consensus) stand. `UNVERIFIABLE` until games are played.
- The opponents' in-season behavior (who streams, who trades): `UNVERIFIABLE`.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-LD-2 | waiver move after the draft: (a) Draymond Green for Christian Braun now, accepting the rest-day risk; (b) watch Green's first week of games, then decide; (c) Bobby Portis for Braun now, the smaller but sturdier gain; (d) stand pat | (b) |
| D-LD-1 | the log-display defects (§8: undone lines re-rendered under the later occupant; the stale "no longer your pick" line) together with D83-1: fix after the draft, red-first, on the next deck version | fix after the draft |
| D-INT-1 (provenance freshness), D82-1, D83-1, earlier | carried; post-draft items | carried |

## Provenance

- Inputs: the owner's paste (`owner_message.txt`, verbatim); the lock pool (deck `af91b23`, `arena/results/players_v69.csv`); the page `docs/draft-deck.html` (Version 70, deck main `ec070a6`).
- Tools: `build_state.py` (parse, resolve, the typed sequence), the deck's `arena/mocks/league_sim.py` (new: the house simulator with the full season recorded, `--verify` against `arena.simulate_seasons`), `live_retro.py` (the draft registered as key 100 on tag v69: replay, final, hindsight, arms), `live_deckcard.py`, `live_replay_dom.mjs`, `stress.py`, `retro_picks.py` (§11), `scripts/repeat_market_check.py` (33 of 33 rooms, 12 flagged; the league draft is room 100 in that count), `write_report.py`.
- No line, tag or placement changed on either plane; nothing was published.

## In plain language

**The headline.** In 10,000 simulated seasons you win the title about 22 percent of the time — more than anyone else in the league; Oblena (Itsy Bitsy Spida) is next at about 17. You make the playoffs about 99 percent of the time and finish as the top seed in about 43 percent. A second, independent 10,000 gave 21.8 percent: the number is stable.

**What kind of team it is.** You win weeks on FT%, BLK, TO, and you are thin in PTS, REB, AST. Protect the first group; the second is where pickups and trades help most.

**The draft itself.** You took the card's 🎯 at 7 of 13 picks and stayed in its Top 5 at 12. The best single change in hindsight was #15: Jalen Johnson instead of Kevin Durant (+2.2 title points on the house arms). Taking the 🎯 every time grades 24.6 percent on the house arms against 21.8 as drafted.

**The risk.** Losing Haliburton or Durant for the whole season would cut the title share to about 11 percent; Kawhi or Kyrie, to about 14 and 16. The board already prices ordinary missed games.

**Pickups.** Of 520 add/drop pairs, only 8 help, all by dropping one of Braun, Queta, Washington or Lendeborg. The best is **Draymond Green for Christian Braun** (about +1.5 to +1.7 title points), but only if Green plays a normal schedule: at reduced availability the same move costs about 1.3 points, and he has been resting in the preseason. The safer, smaller move is **Bobby Portis for Braun** (about +0.9 to +1.2). Nobody on the wire beats any of your top nine.

**Your picks against the card.** Of your six picks off the card's 🎯, yours came out better on title share at 4 (#63 Kel'el Ware, #111 Yaxel Lendeborg, #130 Neemias Queta, #135 PJ Washington); the card was better at 2 (#10 Tyrese Maxey over Tyrese Haliburton, #154 Tobias Harris over Christian Braun). Every difference is under about 1.2 title points; the clearest wins for you were PJ Washington over Poeltl at #135, and for the card, Maxey over Haliburton at #10.

**Your opponents.** Most drafted roughly as before, but the history predicts less than it seems: only 4 of 20 "loyalty" repeats happened, and the reach ranking barely carried over year to year. The notable change is Martin, last year's champion, who drafted for value this time and sits third in the simulation. The managers who churn the waiver wire hardest (Will, Martin, Oblena, Cayas) are probably stronger than the frozen simulation shows.

**Looking back at every pick (§11).** At 10 of your 13 picks a clearly better player was still on the board; the biggest was Jalen Johnson instead of Durant at #15 (about +2.0 title points). At the other 3 picks your choice holds up. Fixing all of them at once with perfect hindsight would have lifted the title share from about 22 to about 29 percent, but that needs knowing every later pick in advance; following the card would have recovered part of it.

**The tool.** Your corrections all worked: the board matched Yahoo's 156 of 156. The history display has two cosmetic bugs (§8), on the list for after the draft.
