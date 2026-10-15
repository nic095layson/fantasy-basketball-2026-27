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

**In scope and unverified.**
- Injury news after the 10/14 lock: did not check (no pull tonight); the board's availability multipliers are the lock's.
- The projections themselves: the 10,000 seasons inherit the lock's lines; the integrity audit's projection confidence (97.8%) and its caveat (the lines sit close to the consensus) stand. `UNVERIFIABLE` until games are played.
- The opponents' in-season behavior (who streams, who trades): `UNVERIFIABLE`.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-LD-1 | the log-display defects (§8: undone lines re-rendered under the later occupant; the stale "no longer your pick" line) together with D83-1: fix after the draft, red-first, on the next deck version | fix after the draft |
| D-INT-1 (provenance freshness), D82-1, D83-1, earlier | carried; post-draft items | carried |

## Provenance

- Inputs: the owner's paste (`owner_message.txt`, verbatim); the lock pool (deck `af91b23`, `arena/results/players_v69.csv`); the page `docs/draft-deck.html` (Version 70, deck main `ec070a6`).
- Tools: `build_state.py` (parse, resolve, the typed sequence), the deck's `arena/mocks/league_sim.py` (new: the house simulator with the full season recorded, `--verify` against `arena.simulate_seasons`), `live_retro.py` (the draft registered as key 100 on tag v69: replay, final, hindsight, arms), `live_deckcard.py`, `live_replay_dom.mjs`, `stress.py`, `scripts/repeat_market_check.py` (33 of 33 rooms, 12 flagged; the league draft is room 100 in that count), `write_report.py`.
- No line, tag or placement changed on either plane; nothing was published.

## In plain language

**The headline.** In 10,000 simulated seasons you win the title about 22 percent of the time — more than anyone else in the league; Oblena (Itsy Bitsy Spida) is next at about 17. You make the playoffs about 99 percent of the time and finish as the top seed in about 43 percent. A second, independent 10,000 gave 21.8 percent: the number is stable.

**What kind of team it is.** You win weeks on FT%, BLK, TO, and you are thin in PTS, REB, AST. Protect the first group; the second is where pickups and trades help most.

**The draft itself.** You took the card's 🎯 at 7 of 13 picks and stayed in its Top 5 at 12. The best single change in hindsight was #15: Jalen Johnson instead of Kevin Durant (+2.2 title points on the house arms). Taking the 🎯 every time grades 24.6 percent on the house arms against 21.8 as drafted.

**The risk.** Losing Haliburton or Durant for the whole season would cut the title share to about 11 percent; Kawhi or Kyrie, to about 14 and 16. The board already prices ordinary missed games.

**The tool.** Your corrections all worked: the board matched Yahoo's 156 of 156. The history display has two cosmetic bugs (§8), on the list for after the draft.
