# After-report — 2026-10-14 (research): a Haliburton-at-10 roster plan from the live rooms on file

**Owner request (2026-10-14, verbatim):** "Once this is complete and you provide projects report, I'd like for you to conduct a research exercise. Assuming I take Haliburton at 10, I'd like for you to build a roster with my remaining picks, using players who are historically available at each pick (based on the average of the previous live mock drats we have conducted). I'd like to see who I can scope to target at around each round pick I have. I understand this system calculates based on my opponent's roster builds, but If I am building around my top 1 and 2 picks, this in theory should be helpful right?"

Pull window: 2026-10-14 → 2026-10-14 (research on records; no pull, no line or price change on either plane).

**What was analyzed.** The 18 live public rooms on file drafted from seat 10 (mocks 52, 53, 54, 56, 57, 58, 59, 60, 61, 67, 68, 73, 74, 75, 77, 78, 79, 80; the bot-cast rooms are excluded — bots, not people), each a full 156-pick record in `arena/data/states/`. Lines: Version 68 (`arena/results/players_v68.csv`), the lines the draft page carried this morning. Your 13 turns: #10, 15, 34, 39, 58, 63, 82, 87, 106, 111, 130, 135, 154.

**Method (stated before the run).**
- *Availability* of a player at your pick N = the share of rooms in which no opponent had taken him before pick N. Your own earlier picks in a room do not count against him (the plan picks differently from what you did).
- *Fit* = the gain in the deck's own weekly model (expected categories won per week against that room's opponent rosters at that moment), averaged over the rooms where he was still there. This is where your top picks matter: every gain is measured on top of Haliburton and the plan's earlier picks.
- *Tiers*: likely = there in 65%+ of rooms; coin flip = 35%–65%; reach = under 35%. The plan takes the best-fitting *likely* player at each turn whose addition still leaves your eight positional slots fillable; the DO NOT DRAFT list (Porziņģis) is excluded.
- *Check*: the plan dropped into each room in your seat and graded on title odds (8-team bracket, 3 seeds × 6000 seasons) against your real roster in that same room, both on Version 68 lines. Leave-one-out: the plan graded in a room is built from the other rooms only, so no room grades a plan it helped build. When the planned player was gone, the next name on that turn's list took his place.

**Headline.** Haliburton himself was there at #10 in 16 of 18 rooms (gone in mocks 54, 68). Building around him, the most reliable path the rooms support is: #10 Tyrese Haliburton; #15 Karl-Anthony Towns; #34 Derrick White; #39 Franz Wagner; #58 Naz Reid; #63 OG Anunoby; #82 Ty Jerome; #87 Josh Hart; #106 Neemias Queta; #111 Yaxel Lendeborg; #130 Draymond Green; #135 Cameron Johnson; #154 Bobby Portis. Dropped into the 16 rooms where Haliburton was there, the leave-one-out plan beat your real roster on title odds in 15 of 16 (median 20.7% vs 12.0%), and on weekly categories in 15 of 16. That gap is real but overstated — see §3: the plan is graded on the same lines it was chosen with, while your real picks were made on earlier versions of the page.

## 1. Roster changes

None — research only. Neither plane changed.

## 2. The plan, turn by turn — who to scope at each of your picks

Each turn lists the top names by fit in each tier. *There* = share of the rooms where he was available at that pick; *recent* = the same over the six rooms drafted 10/12 or later (mocks 74, 75, 77, 78, 79, 80), since Yahoo's prices moved through September. *Fit* = weekly categories gained (on top of the plan so far).

### Pick #15 — plan: **Karl-Anthony Towns**

| tier | player | team | pos | there | recent | fit |
|---|---|---|---|---|---|---|
| likely | Karl-Anthony Towns | NYK | C/PF | 94% | 83% | +2.021 |
| likely | Lauri Markkanen | UTA | SF/PF | 100% | 100% | +1.990 |
| likely | Chet Holmgren | OKC | PF/C | 100% | 100% | +1.958 |
| likely | Kevin Durant | HOU | PF/SF/SG | 78% | 83% | +1.920 |
| coin | Donovan Mitchell | CLE | PG/SG | 61% | 67% | +1.761 |
| reach | Cooper Flagg | DAL | PF/SF/SG | 11% | 0% | +1.933 |
| reach | Jalen Johnson | ATL | SF/PF | 17% | 17% | +1.916 |
| reach | Tyrese Maxey | PHI | PG | 17% | 0% | +1.902 |
| reach | Scottie Barnes | TOR | SF/PF/C | 28% | 50% | +1.848 |

### Pick #34 — plan: **Derrick White**

| tier | player | team | pos | there | recent | fit |
|---|---|---|---|---|---|---|
| likely | Derrick White | BOS | PG/SG | 100% | 100% | +1.596 |
| likely | Onyeka Okongwu | ATL | C | 100% | 100% | +1.462 |
| likely | OG Anunoby | NYK | SF/PF | 100% | 100% | +1.417 |
| likely | Desmond Bane | ORL | SG/SF | 100% | 100% | +1.402 |
| coin | Kawhi Leonard | TOR | PF/SF/SG | 50% | 67% | +1.540 |
| coin | Lauri Markkanen | UTA | SF/PF | 39% | 33% | +1.491 |
| coin | Anthony Davis | WAS | PF/C | 56% | 33% | +1.471 |
| coin | James Harden | CLE | PG/SG | 39% | 67% | +1.431 |
| reach | Tyrese Maxey | PHI | PG | 6% | 0% | +1.733 |
| reach | Donovan Mitchell | CLE | PG/SG | 28% | 33% | +1.653 |
| reach | Jalen Johnson | ATL | SF/PF | 6% | 0% | +1.567 |
| reach | Scottie Barnes | TOR | SF/PF/C | 6% | 17% | +1.565 |

### Pick #39 — plan: **Franz Wagner**

| tier | player | team | pos | there | recent | fit |
|---|---|---|---|---|---|---|
| likely | Franz Wagner | ORL | SF/PF | 89% | 83% | +1.298 |
| likely | Onyeka Okongwu | ATL | C | 100% | 100% | +1.293 |
| likely | Desmond Bane | ORL | SG/SF | 100% | 100% | +1.284 |
| likely | Kyrie Irving | DAL | PG | 83% | 83% | +1.273 |
| coin | Jalen Duren | DET | C | 56% | 33% | +1.200 |
| coin | Walker Kessler | LAL | C | 50% | 50% | +1.146 |
| reach | Tyrese Maxey | PHI | PG | 6% | 0% | +1.556 |
| reach | Donovan Mitchell | CLE | PG/SG | 28% | 33% | +1.445 |
| reach | Kawhi Leonard | TOR | PF/SF/SG | 28% | 67% | +1.414 |
| reach | Lauri Markkanen | UTA | SF/PF | 17% | 17% | +1.387 |

### Pick #58 — plan: **Naz Reid**

| tier | player | team | pos | there | recent | fit |
|---|---|---|---|---|---|---|
| likely | Naz Reid | CHA | PF/C | 89% | 100% | +1.201 |
| likely | OG Anunoby | NYK | SF/PF | 100% | 100% | +1.196 |
| likely | Kel'el Ware | MIL | C | 94% | 100% | +1.155 |
| likely | Tyler Herro | MIL | PG/SG | 100% | 100% | +1.150 |
| coin | Jalen Williams | OKC | SF/PF | 50% | 17% | +1.202 |
| coin | Michael Porter Jr. | BKN | SF/PF | 56% | 67% | +1.175 |
| coin | Dyson Daniels | ATL | SG/SF | 44% | 33% | +1.157 |
| coin | Cameron Boozer | MEM | PF | 61% | 67% | +1.131 |
| reach | Tyrese Maxey | PHI | PG | 6% | 0% | +1.488 |
| reach | Donovan Mitchell | CLE | PG/SG | 28% | 33% | +1.404 |
| reach | Evan Mobley | CLE | PF/C | 11% | 0% | +1.375 |
| reach | Jalen Johnson | ATL | SF/PF | 6% | 0% | +1.371 |

### Pick #63 — plan: **OG Anunoby**

| tier | player | team | pos | there | recent | fit |
|---|---|---|---|---|---|---|
| likely | OG Anunoby | NYK | SF/PF | 100% | 100% | +1.092 |
| likely | Tyler Herro | MIL | PG/SG | 72% | 67% | +1.085 |
| likely | Ty Jerome | MEM | SG/PG | 100% | 100% | +1.062 |
| likely | VJ Edgecombe | PHI | PG/SG | 100% | 100% | +1.056 |
| coin | Jalen Williams | OKC | SF/PF | 50% | 17% | +1.141 |
| coin | Michael Porter Jr. | BKN | SF/PF | 39% | 33% | +1.069 |
| coin | Matas Buzelis | CHI | SF/PF | 50% | 67% | +1.005 |
| coin | Alex Sarr | WAS | C | 61% | 17% | +0.877 |
| reach | Tyrese Maxey | PHI | PG | 6% | 0% | +1.354 |
| reach | Evan Mobley | CLE | PF/C | 11% | 0% | +1.288 |
| reach | Donovan Mitchell | CLE | PG/SG | 28% | 33% | +1.270 |
| reach | Kawhi Leonard | TOR | PF/SF/SG | 17% | 50% | +1.229 |

### Pick #82 — plan: **Ty Jerome**

| tier | player | team | pos | there | recent | fit |
|---|---|---|---|---|---|---|
| likely | Ty Jerome | MEM | SG/PG | 100% | 100% | +0.988 |
| likely | VJ Edgecombe | PHI | PG/SG | 78% | 83% | +0.973 |
| likely | Josh Hart | NYK | SG/SF | 89% | 100% | +0.962 |
| likely | Caleb Wilson | CHI | PF | 78% | 100% | +0.959 |
| coin | Jalen Williams | OKC | SF/PF | 50% | 17% | +1.049 |
| coin | Mikal Bridges | NYK | SF/PF | 44% | 33% | +0.956 |
| coin | Damian Lillard | POR | PG | 39% | 17% | +0.904 |
| coin | Cedric Coward | MEM | SG/SF | 56% | 17% | +0.839 |
| reach | Tyrese Maxey | PHI | PG | 6% | 0% | +1.323 |
| reach | Donovan Mitchell | CLE | PG/SG | 28% | 33% | +1.212 |
| reach | Evan Mobley | CLE | PF/C | 11% | 0% | +1.184 |
| reach | Jalen Johnson | ATL | SF/PF | 6% | 0% | +1.178 |

### Pick #87 — plan: **Josh Hart**

| tier | player | team | pos | there | recent | fit |
|---|---|---|---|---|---|---|
| likely | Josh Hart | NYK | SG/SF | 78% | 67% | +0.875 |
| likely | Jaden McDaniels | MIN | SF | 72% | 83% | +0.874 |
| likely | John Collins | DET | PF/C | 94% | 83% | +0.874 |
| likely | Andrew Wiggins | MIA | PF/SF/SG | 94% | 100% | +0.861 |
| coin | Jalen Williams | OKC | SF/PF | 50% | 17% | +0.950 |
| coin | VJ Edgecombe | PHI | PG/SG | 61% | 67% | +0.881 |
| coin | Damian Lillard | POR | PG | 39% | 17% | +0.801 |
| coin | Dylan Harper | SAS | PG/SG | 61% | 33% | +0.788 |
| reach | Evan Mobley | CLE | PF/C | 11% | 0% | +1.187 |
| reach | Anthony Davis | WAS | PF/C | 22% | 17% | +1.131 |
| reach | Tyrese Maxey | PHI | PG | 6% | 0% | +1.122 |
| reach | Jalen Johnson | ATL | SF/PF | 6% | 0% | +1.080 |

### Pick #106 — plan: **Neemias Queta**

| tier | player | team | pos | there | recent | fit |
|---|---|---|---|---|---|---|
| likely | Neemias Queta | BOS | C | 67% | 50% | +0.794 |
| likely | Jakob Poeltl | TOR | C | 100% | 100% | +0.768 |
| likely | Yaxel Lendeborg | GSW | PF | 100% | 100% | +0.760 |
| likely | Reed Sheppard | HOU | PG/SG | 94% | 83% | +0.745 |
| coin | Jalen Williams | OKC | SF/PF | 50% | 17% | +0.911 |
| coin | Myles Turner | MIL | C | 61% | 100% | +0.836 |
| coin | John Collins | DET | PF/C | 61% | 0% | +0.833 |
| coin | Isaiah Hartenstein | OKC | C | 50% | 100% | +0.809 |
| reach | Tyrese Maxey | PHI | PG | 6% | 0% | +1.108 |
| reach | Evan Mobley | CLE | PF/C | 11% | 0% | +1.103 |
| reach | Anthony Davis | WAS | PF/C | 22% | 17% | +1.098 |
| reach | Scottie Barnes | TOR | SF/PF/C | 6% | 17% | +1.094 |

### Pick #111 — plan: **Yaxel Lendeborg**

| tier | player | team | pos | there | recent | fit |
|---|---|---|---|---|---|---|
| likely | Yaxel Lendeborg | GSW | PF | 100% | 100% | +0.757 |
| likely | Reed Sheppard | HOU | PG/SG | 94% | 83% | +0.756 |
| likely | Kyshawn George | WAS | PF/SF/SG | 100% | 100% | +0.752 |
| likely | Jakob Poeltl | TOR | C | 100% | 100% | +0.746 |
| coin | Jalen Williams | OKC | SF/PF | 50% | 17% | +0.927 |
| coin | John Collins | DET | PF/C | 39% | 0% | +0.848 |
| coin | Myles Turner | MIL | C | 50% | 67% | +0.818 |
| coin | Damian Lillard | POR | PG | 39% | 17% | +0.816 |
| reach | Tyrese Maxey | PHI | PG | 6% | 0% | +1.165 |
| reach | Donovan Mitchell | CLE | PG/SG | 28% | 33% | +1.099 |
| reach | Evan Mobley | CLE | PF/C | 11% | 0% | +1.092 |
| reach | Anthony Davis | WAS | PF/C | 22% | 17% | +1.057 |

### Pick #130 — plan: **Draymond Green**

| tier | player | team | pos | there | recent | fit |
|---|---|---|---|---|---|---|
| likely | Draymond Green | GSW | PF/C | 100% | 100% | +0.730 |
| likely | PJ Washington | DAL | PF/C | 94% | 83% | +0.723 |
| likely | Cameron Johnson | DEN | PF/SF | 100% | 100% | +0.721 |
| likely | Devin Vassell | SAS | SG/SF | 78% | 100% | +0.717 |
| coin | Jalen Williams | OKC | SF/PF | 50% | 17% | +0.914 |
| coin | Damian Lillard | POR | PG | 39% | 17% | +0.815 |
| coin | Reed Sheppard | HOU | PG/SG | 61% | 67% | +0.768 |
| coin | Collin Gillespie | PHX | PG/SG | 61% | 33% | +0.742 |
| reach | Tyrese Maxey | PHI | PG | 6% | 0% | +1.188 |
| reach | Donovan Mitchell | CLE | PG/SG | 28% | 33% | +1.117 |
| reach | Jalen Johnson | ATL | SF/PF | 6% | 0% | +1.068 |
| reach | Kevin Durant | HOU | PF/SF/SG | 17% | 33% | +1.063 |

### Pick #135 — plan: **Cameron Johnson**

| tier | player | team | pos | there | recent | fit |
|---|---|---|---|---|---|---|
| likely | Cameron Johnson | DEN | PF/SF | 94% | 83% | +0.647 |
| likely | Devin Vassell | SAS | SG/SF | 78% | 100% | +0.647 |
| likely | Saddiq Bey | NOP | PF/SF | 94% | 83% | +0.642 |
| likely | Tobias Harris | SAS | PF | 100% | 100% | +0.634 |
| coin | Jalen Williams | OKC | SF/PF | 50% | 17% | +0.800 |
| coin | Damian Lillard | POR | PG | 39% | 17% | +0.731 |
| coin | Reed Sheppard | HOU | PG/SG | 50% | 50% | +0.669 |
| coin | Collin Gillespie | PHX | PG/SG | 50% | 33% | +0.654 |
| reach | Tyrese Maxey | PHI | PG | 6% | 0% | +1.060 |
| reach | Donovan Mitchell | CLE | PG/SG | 28% | 33% | +1.004 |
| reach | Kawhi Leonard | TOR | PF/SF/SG | 17% | 50% | +0.921 |
| reach | Kevin Durant | HOU | PF/SF/SG | 17% | 33% | +0.917 |

### Pick #154 — plan: **Bobby Portis**

| tier | player | team | pos | there | recent | fit |
|---|---|---|---|---|---|---|
| likely | Bobby Portis | MIA | PF/C | 67% | 83% | +0.634 |
| likely | Tari Eason | HOU | PF/SF/SG | 72% | 83% | +0.619 |
| likely | Christian Braun | DEN | PF/SF/SG | 72% | 83% | +0.614 |
| likely | Tobias Harris | SAS | PF | 72% | 100% | +0.614 |
| coin | Jalen Williams | OKC | SF/PF | 50% | 17% | +0.813 |
| coin | Damian Lillard | POR | PG | 39% | 17% | +0.731 |
| coin | PJ Washington | DAL | PF/C | 61% | 0% | +0.638 |
| coin | Devin Vassell | SAS | SG/SF | 61% | 83% | +0.620 |
| reach | Tyrese Maxey | PHI | PG | 6% | 0% | +1.043 |
| reach | Donovan Mitchell | CLE | PG/SG | 28% | 33% | +1.005 |
| reach | Jalen Johnson | ATL | SF/PF | 6% | 0% | +0.960 |
| reach | Evan Mobley | CLE | PF/C | 11% | 0% | +0.948 |

## 3. The check: the plan dropped into the rooms

| mock | your real roster: title / weekly cats | the plan (built without this room): title / weekly cats | planned players already gone |
|---|---|---|---|
| 52 | 6.92% / 4.536 | 19.17% / 5.037 | 2 of 12 |
| 53 | 11.77% / 4.718 | 20.64% / 5.022 | 2 of 12 |
| 56 | 12.81% / 4.681 | 21.99% / 4.999 | 6 of 12 |
| 57 | 6.01% / 4.473 | 17.39% / 4.963 | 2 of 12 |
| 58 | 6.71% / 4.477 | 21.05% / 5.023 | 3 of 12 |
| 59 | 16.72% / 4.914 | 24.08% / 5.182 | 0 of 12 |
| 60 | 14.89% / 4.841 | 20.47% / 4.973 | 2 of 12 |
| 61 | 7.54% / 4.549 | 17.68% / 4.978 | 4 of 12 |
| 67 | 10.29% / 4.673 | 23.53% / 5.094 | 0 of 12 |
| 73 | 14.10% / 4.853 | 16.63% / 4.976 | 1 of 12 |
| 74 | 8.77% / 4.597 | 16.73% / 4.950 | 4 of 12 |
| 75 | 12.23% / 4.749 | 20.71% / 5.028 | 0 of 12 |
| 77 | 20.91% / 5.015 | 24.34% / 5.078 | 2 of 12 |
| 78 | 10.83% / 4.695 | 17.98% / 4.968 | 3 of 12 |
| 79 | 20.17% / 5.000 | 26.09% / 5.177 | 3 of 12 |
| 80 | 23.84% / 5.054 | 21.80% / 5.022 | 3 of 12 |

Median title odds 12.00% real vs 20.68% plan; mean 12.78% vs 20.64%. The plan beat the real roster in 15 of 16 rooms. Planned players already gone when the turn came: median 2 of 12 per room (max 6).

**Why the gap is overstated (read before trusting it):**
- *Same lines.* The plan was chosen on Version 68's lines and graded on them; your real picks in mocks 52–79 were made on Versions 3x–6x, whose lines differed (the WO-5, MG, dial and blend passes all came after many of these rooms). A roster picked with yesterday's numbers always looks worse under today's.
- *Haliburton is forced.* The real rosters did not all start with Haliburton; the plan's value includes whatever Version 68 thinks of him versus your real #10.
- *Leave-one-out* removes the room-fitting bias only; it cannot remove the two above.
So read the replay as *the plan is not a trap* — it holds up in every kind of room on file — not as a promise of the size of the edge.

**How stable the plan is.** How often each full-sample pick was also the leave-one-out plan's pick, and how often he actually landed on the replayed roster:

| turn | plan | same pick in leave-one-out plans | landed on the roster |
|---|---|---|---|
| #10 | Tyrese Haliburton | 16 of 16 | 16 of 16 |
| #15 | Karl-Anthony Towns | 16 of 16 | 11 of 16 |
| #34 | Derrick White | 16 of 16 | 16 of 16 |
| #39 | Franz Wagner | 16 of 16 | 14 of 16 |
| #58 | Naz Reid | 16 of 16 | 14 of 16 |
| #63 | OG Anunoby | 16 of 16 | 14 of 16 |
| #82 | Ty Jerome | 16 of 16 | 16 of 16 |
| #87 | Josh Hart | 9 of 16 | 9 of 16 |
| #106 | Neemias Queta | 5 of 16 | 0 of 16 |
| #111 | Yaxel Lendeborg | 16 of 16 | 13 of 16 |
| #130 | Draymond Green | 5 of 16 | 5 of 16 |
| #135 | Cameron Johnson | 5 of 16 | 6 of 16 |
| #154 | Bobby Portis | 6 of 16 | 4 of 16 |

## 4. Your question: is building around picks 1 and 2 helpful?

Yes, with one adjustment to how to use it. The fit numbers above already *are* built around your first two picks — every turn's gain is measured on top of Haliburton and the plan's #15 — so the plan leans toward what that core lacks rather than toward the best player in a vacuum. Where it helps most is preparation: knowing that the names in the *likely* column are usually there means you can plan the pair at #34/#39, #58/#63 and so on instead of reacting.

The adjustment: the draft page still adapts to the actual room (who your opponents took, what your roster already has). The plan is fixed in advance; the card is not. When they disagree at a turn, it usually means the room has run differently from the rooms on file — the card has seen that, the plan has not. Use the plan as the scouting map and the card as the live call.

## Watchlist

- Haliburton was gone before #10 in 2 of 18 rooms; if he is gone tonight, this plan's later turns no longer apply as built (the card adapts).
- The plan's late turns (#130 onward) rest on few distinctions — fits there are small and close together.

## Open-item receipts

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| (research) | records only; no web research and no roster pull | the lines are Version 68's (`players_v68.csv`) |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | this morning's final pull (`after-report-2026-10-14.md`, receipts dated 10/14) and the lock report (`after-report-2026-10-14-lock.md`) | as recorded there; not re-queried for this research (did not check) |

The standing check below is the one run on the locked page (Version 70) for the lock report; this research built no page.

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 e68a85a5305f), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 29 of 29 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 29 of 29 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 21 of 29 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 29 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 11 of 29 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 11 of 29 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| John Collins | 11 of 29 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 8 of 29 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 7 of 29 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 6 of 29 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 5 of 29 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 29 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 29 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (14 mocks, value 27, market 45); Lauri Markkanen (14 mocks, value 21, market 37); Tyrese Haliburton (12 mocks, value 7, market 12); Kel'el Ware (8 mocks, value 57, market 77); Tyler Herro (8 mocks, value 51, market 69); Tyrese Maxey (8 mocks, value 5, market 9); Karl-Anthony Towns (5 mocks, value 12, market 15).

## Bounds

- Out of scope by design: bot-cast rooms; the real draft's eleven league-mates (the rooms are public strangers, so tonight's opponents may draft differently); any line or price change.
- In scope and stated: availability is measured on 18 rooms (6 recent) — a player at 70% is a measured rate on a small sample, not a guarantee. The bias in §3 is named, not removed.
- Did not check: a market-only baseline (best available by ADP at each turn) graded the same way — it would separate how much of the gap is planning and how much is the lines.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-1014-14 | Use this plan as a scouting map beside the card (no change to the page), or ask for a second version (e.g. a different #15 or a punt build)? | scouting map only; the page is unchanged |

## Provenance

- Script: `plan.py` (this folder); record: `plan_2026-10-14.json`; run log `plan_run.log`. Engine: the deck's `arena.team_week_model`, `simulate_seasons` (seeds 11, 23, 47; 6000 seasons each), `hoops.POSITIONAL_SLOTS`, `hoops.do_not_draft()`.
- Rooms: `arena/data/states/draft_state_<mock>.json` in the deck repo (mock 80 from branch `claude/mock80-2026-10-14`).

## In plain language

I looked at the 18 live mock rooms you drafted from the 10th seat and asked, for each of your picks, which players were usually still there. Then I built the roster that fits best around Haliburton using only players who were there in at least two out of three rooms:

- **#10** Tyrese Haliburton
- **#15** Karl-Anthony Towns
- **#34** Derrick White
- **#39** Franz Wagner
- **#58** Naz Reid
- **#63** OG Anunoby
- **#82** Ty Jerome
- **#87** Josh Hart
- **#106** Neemias Queta
- **#111** Yaxel Lendeborg
- **#130** Draymond Green
- **#135** Cameron Johnson
- **#154** Bobby Portis

When I dropped that plan into the rooms (each time building it without looking at that room), it beat the roster you actually drafted there in 15 of 16 rooms. Part of that is real, and part of it is that the plan was picked with today's numbers while your real picks used older versions of the page — so treat the size of the edge with caution. Section 2 lists, for every pick, the names that are usually there, the coin flips, and the reaches, so you have backups if the room goes differently. And yes — building around your first two picks is exactly what the fit numbers do; just let the card make the final call at each turn, because it sees the room you are actually in.
