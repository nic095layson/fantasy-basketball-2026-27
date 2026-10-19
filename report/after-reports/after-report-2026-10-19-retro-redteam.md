# After-report — the draft retro re-run with the red team's findings: would the card's picks have changed, what the draft changes would have been, and how much title share a close-to-real draft gains

**Owner request (2026-10-19, verbatim):** "retro-run our draft again. Knowing what the red team found, would the card's suggested players have changed? What would've been the draft changes? Try and stay as close to the real draft as drafted, but I want to know how much better % we could have been in championship probability".

**What was analyzed.** The 10/14 league draft (`draft_state_100.json`, pool v69, seat 10) on the shipped engine (deck `259c630`: 17 regular-season weeks, reseeded bracket), with three red-team findings applied. (1) The card's measure ignores the shared games shock and overstates counting-category edges: every alternative is scored both ways, by the card's plain ECW and by a shock-aware ECW that inflates the counting-category variance by shock² (μa² + μb²), which is what the simulator draws. (2) The engine changed under the §11 retro: every swap is re-judged on the shipped engine (10,000 seasons on seeds 2026 and 2027, Monte-Carlo SE 0.41 points), and the §11 ceiling board is re-run on it. (3) The shock is FRAGILE: every swap that clears the noise line is re-run at shock 0 and 0.12 (6,000 seasons per seed), and only a swap that stays positive across the band is called robust. The card at each turn is the deck's exact port of the page's rule (`live_retro.card()`: half ΔECW against the opponents' rosters at the time, half adjusted value, priced-only from the late rounds, Porzingis vetoed). Screens: the top 3 alternatives by each measure against the final rosters, pairwise-swapped (a later seat that took the alternative gets your player); the union of both screens is simulated. Noise line 0.5 title points on both seeds, as in §11.

**Headline.** Knowing what the red team found changes the odds, not the names. The card's 🎯 is the same player under the shock-aware measure at 12 of 13 turns (the one change: #111, Jakob Poeltl to Neemias Queta), its top five identical at 6 of 13; the hindsight top three differ at one turn (#154 Tobias Harris enters, Jrue Holiday leaves). What the findings do change: 4 of the 23 swaps that clear the noise line on the shipped engine do not survive the shock band (#58 Franz Wagner, #63 Dyson Daniels, #87 Caleb Wilson, #87 Josh Hart), one of them the card's own 🎯 at that turn. The baseline reproduces the 10,000-season reference exactly (21.10 / 21.33). Staying close to the real draft: two changes, Jalen Johnson for Kevin Durant at #15 and James Harden for Kawhi Leonard at #34, move the title share from 21.10 / 21.33 to 28.25 / 28.26 (+7.04 mean); the best close-to-real board is 6 changes at 29.12 / 29.06 (+7.88); the §11 ceiling board (9 changes) re-run on the shipped engine is 28.83 / 28.65. Every figure here carries the structural band: TEAM_WEEK_SHOCK is FRAGILE: +3.4 (no shared games shock (0.0)) / -2.3 (shared games shock doubled (0.12)) on the as-drafted title share; the as-drafted share runs 24.42 / 25.43 with no shock and 19.40 / 19.02 with it doubled, and the boards' gains at shock 0.12 are 52% and 47% of their shipped-engine gains (§4).

Pull window: 2026-10-19 → 2026-10-19 (analysis only; no roster pull, no line change).

## 1. Roster changes

None. No pull, no line, tag, price or engine constant changed; the retro swaps live only inside the simulation records.

## 2. Would the card's suggested players have changed?

EVIDENCE: `retro_redteam.py` → `retro_redteam.json` (`turns[].card_plain`, `card_shock`). The card at each of your turns, recomputed on the shipped engine the way the page computes it, with the ECW leg plain (as shipped) and shock-aware (the red team's correction). The ΔECW column is the alternative's gain in expected weekly category wins against the opponents' rosters at that moment.

| pick | you took | your pick's card rank (plain / shock-aware) | card 🎯 plain | card 🎯 shock-aware | top five identical |
|---|---|---|---|---|---|
| #10 | Tyrese Haliburton | 2 / 2 | Tyrese Maxey (ΔECW +4.467) | Tyrese Maxey (ΔECW +4.468) | yes |
| #15 | Kevin Durant | 1 / 1 | Kevin Durant (ΔECW +1.935) | Kevin Durant (ΔECW +1.918) | yes |
| #34 | Kawhi Leonard | 1 / 1 | Kawhi Leonard (ΔECW +1.424) | Kawhi Leonard (ΔECW +1.406) | yes |
| #39 | Derrick White | 1 / 1 | Derrick White (ΔECW +1.353) | Derrick White (ΔECW +1.318) | yes |
| #58 | Kyrie Irving | 1 / 1 | Kyrie Irving (ΔECW +1.032) | Kyrie Irving (ΔECW +0.998) | yes |
| #63 | Kel'el Ware | 2 / 2 | Dyson Daniels (ΔECW +0.815) | Dyson Daniels (ΔECW +0.793) | no: Dyson Daniels, Kel'el Ware, Naz Reid, Jaden McDaniels, Mikal Bridges |
| #82 | Ty Jerome | 1 / 1 | Ty Jerome (ΔECW +0.983) | Ty Jerome (ΔECW +0.933) | no: Ty Jerome, Immanuel Quickley, Jaden McDaniels, Josh Hart, Joel Embiid |
| #87 | Jaden McDaniels | 1 / 1 | Jaden McDaniels (ΔECW +0.867) | Jaden McDaniels (ΔECW +0.822) | no: Jaden McDaniels, Caleb Wilson, Josh Hart, John Collins, Andrew Wiggins |
| #106 | Miles Bridges | 1 / 1 | Miles Bridges (ΔECW +0.752) | Miles Bridges (ΔECW +0.707) | no: Miles Bridges, Cason Wallace, Myles Turner, Reed Sheppard, Collin Gillespie |
| #111 | Yaxel Lendeborg | 3 / 3 | Jakob Poeltl (ΔECW +0.794) | Neemias Queta (ΔECW +0.741) | no: Neemias Queta, Jakob Poeltl, Yaxel Lendeborg, Nic Claxton, Christian Braun |
| #130 | Neemias Queta | 3 / 2 | Jakob Poeltl (ΔECW +0.718) | Jakob Poeltl (ΔECW +0.672) | no: Jakob Poeltl, Neemias Queta, Reed Sheppard, Kyshawn George, Ayo Dosunmu |
| #135 | PJ Washington | 9 / 9 | Jakob Poeltl (ΔECW +0.797) | Jakob Poeltl (ΔECW +0.708) | no: Jakob Poeltl, Kyshawn George, Reed Sheppard, Christian Braun, Tobias Harris |
| #154 | Christian Braun | 2 / 2 | Tobias Harris (ΔECW +0.693) | Tobias Harris (ΔECW +0.625) | yes |

The shock-aware measure compresses every counting-category edge toward a coin flip, the ones you lead and the ones you trail alike (the as-drafted ECW barely moves, 5.144 to 5.157 of 9, while the gain of every alternative shrinks, by a median 41%), but it compresses them for every candidate at once, so the order the card shows you barely moves. The one 🎯 that changes is at #111: Jakob Poeltl and Neemias Queta sit within 0.005 of each other on the card's blended score either way; the red team's correction tips it, nothing more. INFERENCE: a shock-aware card would have shown you the same names at the same turns; the finding's effect on draft-day advice is nil, its effect on the odds quoted beside the advice is the subject of §4.

## 3. The hindsight swaps on the shipped engine, both screens, with the band

EVIDENCE: `retro_redteam.json` (`swaps`): every alternative in the union of the two top-3 screens, swapped in pairwise, 10,000 seasons on each seed; the band columns re-run the swap and the baseline at shock 0 and 0.12 (6,000 seasons per seed) for every swap that clears the noise line on both seeds. 'went' is where the alternative was actually drafted (pick / seat; undrafted = a free agent at the end of the draft). The screens agree on 24 of 26 candidates.

| pick | you took | alternative | went | card rank at the turn (plain / shock) | ΔECW plain / shock-aware | title shift (2026 / 2027) | clears 0.5 | shift at shock 0 | shift at shock 0.12 | robust |
|---|---|---|---|---|---|---|---|---|---|---|
| #10 | Tyrese Haliburton | Tyrese Maxey | #11 seat 11 | 1 / 1 | +0.007 / -0.007 | +1.75 / +2.54 | yes | +1.41 / +1.97 | +0.02 / +0.68 | yes |
| #15 | Kevin Durant | Donovan Mitchell | #19 seat 6 | 11 / 11 | +0.046 / +0.035 | +2.38 / +2.45 | yes | +3.10 / +0.87 | +0.22 / +1.76 | yes |
| #15 | Kevin Durant | Jalen Johnson | #18 seat 7 | 3 / 3 | +0.132 / +0.095 | +2.55 / +3.63 | yes | +4.53 / +3.42 | +1.63 / +1.48 | yes |
| #15 | Kevin Durant | Jamal Murray | #20 seat 5 | 6 / 6 | +0.038 / +0.036 | +1.40 / +2.25 | yes | +2.15 / +0.39 | +0.57 / +1.08 | yes |
| #34 | Kawhi Leonard | Domantas Sabonis | #36 seat 12 | 6 / 7 | +0.087 / +0.051 | +2.07 / +2.29 | yes | +0.88 / +0.37 | +1.57 / +0.50 | yes |
| #34 | Kawhi Leonard | James Harden | #46 seat 3 | 5 / 5 | +0.080 / +0.054 | +2.60 / +2.59 | yes | +3.95 / +2.42 | +1.32 / +1.73 | yes |
| #39 | Derrick White | James Harden | #46 seat 3 | 7 / 7 | +0.021 / +0.000 | +0.09 / +0.38 | no | — | — |  |
| #58 | Kyrie Irving | Franz Wagner | #62 seat 11 | 2 / 2 | +0.018 / +0.007 | +0.97 / +1.20 | yes | +0.71 / -0.50 | +0.42 / +0.10 | **no** |
| #58 | Kyrie Irving | Michael Porter Jr. | #72 seat 1 | 6 / 6 | +0.024 / +0.010 | +2.22 / +1.63 | yes | +2.46 / +1.14 | +0.73 / +1.43 | yes |
| #63 | Kel'el Ware | Dyson Daniels | #67 seat 6 | 1 / 1 | +0.007 / -0.012 | +1.09 / +1.85 | yes | +1.53 / -1.05 | +0.00 / +0.15 | **no** |
| #63 | Kel'el Ware | Michael Porter Jr. | #72 seat 1 | 7 / 8 | +0.060 / +0.032 | +2.34 / +3.22 | yes | +3.16 / +2.74 | +1.00 / +2.08 | yes |
| #63 | Kel'el Ware | Naz Reid | #78 seat 6 | 3 / 3 | +0.034 / +0.018 | +1.78 / +2.31 | yes | +2.36 / +1.67 | +0.25 / +1.31 | yes |
| #87 | Jaden McDaniels | Caleb Wilson | #91 seat 6 | 3 / 2 | +0.035 / +0.017 | +1.19 / +1.84 | yes | +0.70 / +1.14 | -0.10 / +0.96 | **no** |
| #87 | Jaden McDaniels | Josh Hart | #99 seat 3 | 2 / 3 | +0.055 / +0.034 | +1.84 / +1.24 | yes | +2.11 / +0.40 | +0.23 / -0.09 | **no** |
| #111 | Yaxel Lendeborg | Cedric Coward | #115 seat 6 | 7 / 7 | +0.035 / +0.022 | +1.12 / +1.33 | yes | +0.50 / +0.77 | +0.65 / +1.25 | yes |
| #111 | Yaxel Lendeborg | Draymond Green | undrafted | 27 / 25 | +0.026 / +0.010 | +0.61 / +0.64 | yes | +1.50 / +0.07 | +1.05 / +0.35 | yes |
| #111 | Yaxel Lendeborg | Kyshawn George | #150 seat 6 | 13 / 13 | +0.058 / +0.039 | +2.33 / +2.40 | yes | +2.81 / +2.09 | +1.07 / +1.61 | yes |
| #130 | Neemias Queta | Draymond Green | undrafted | 18 / 19 | +0.025 / +0.003 | +1.73 / +2.11 | yes | +2.66 / +0.80 | +0.63 / +1.31 | yes |
| #130 | Neemias Queta | Jakob Poeltl | #151 seat 7 | 1 / 1 | +0.011 / +0.001 | +0.42 / +1.14 | no | — | — |  |
| #130 | Neemias Queta | Kyshawn George | #150 seat 6 | 4 / 4 | +0.037 / +0.011 | +1.52 / +2.16 | yes | +2.28 / +1.74 | +0.18 / +1.31 | yes |
| #135 | PJ Washington | Draymond Green | undrafted | 14 / 14 | +0.022 / +0.015 | +0.21 / +0.71 | no | — | — |  |
| #135 | PJ Washington | Kyshawn George | #150 seat 6 | 2 / 2 | +0.045 / +0.036 | +1.35 / +1.96 | yes | +2.56 / +1.20 | +0.45 / +0.95 | yes |
| #154 | Christian Braun | Bobby Portis | undrafted | 3 / 3 | +0.029 / +0.019 | +1.21 / +2.30 | yes | +1.81 / +1.57 | +0.22 / +0.88 | yes |
| #154 | Christian Braun | Draymond Green | undrafted | 8 / 8 | +0.061 / +0.040 | +2.03 / +2.52 | yes | +3.00 / +1.20 | +2.05 / +0.98 | yes |
| #154 | Christian Braun | Jrue Holiday | undrafted | 4 / 4 | +0.012 / +0.001 | +0.79 / +1.27 | yes | +1.30 / +0.37 | +0.20 / +1.18 | yes |
| #154 | Christian Braun | Tobias Harris | undrafted | 1 / 1 | +0.009 / +0.006 | +0.96 / +0.86 | yes | +0.48 / +0.79 | +0.05 / +0.16 | yes |

Of the 23 swaps that clear the noise line on the shipped engine, 19 stay positive on both seeds at both ends of the band and 4 do not: #58 Franz Wagner for Kyrie Irving (shock 0: +0.71 / -0.50; 0.12: +0.42 / +0.10); #63 Dyson Daniels for Kel'el Ware (shock 0: +1.53 / -1.05; 0.12: +0.00 / +0.15); #87 Caleb Wilson for Jaden McDaniels (shock 0: +0.70 / +1.14; 0.12: -0.10 / +0.96); #87 Josh Hart for Jaden McDaniels (shock 0: +2.11 / +0.40; 0.12: +0.23 / -0.09). The §11 retro, run before the red team, would have counted all of them as misses; with the band, they are swaps whose sign depends on a constant nobody has measured. One is the card's own 🎯 at that turn.

## 4. How much better, staying as close to the real draft as possible

EVIDENCE: `cumulative.py` → `cumulative.json`: the 8 swaps of the close-to-real board (at each turn that has one, the robust alternative with the largest single-swap gain, each alternative used once; 19 robust swaps in all, several naming the same player at different turns) taken one at a time in order of their single-swap gain, each cumulative board run 10,000 seasons on both seeds on the shipped engine; `retro_redteam.json` (`close_to_real`, `ceiling_s11`) for the full board and the §11 board with their bands. Swaps interact (an alternative taken at one turn hands your player to the seat that drafted it, and the roster's category balance moves), so the curve is not the sum of the single shifts.

| changes | the change added | title share (2026 / 2027) | shift vs as drafted | mean |
|---|---|---|---|---|
| 0 | as drafted | 21.10 / 21.33 | — | — |
| 1 | Jalen Johnson for Kevin Durant at #15 | 23.65 / 24.96 | +2.55 / +3.63 | +3.09 |
| 2 | James Harden for Kawhi Leonard at #34 | 28.25 / 28.26 | +7.15 / +6.93 | +7.04 |
| 3 | Kyshawn George for Yaxel Lendeborg at #111 | 28.91 / 28.12 | +7.81 / +6.79 | +7.30 |
| 4 | Tyrese Maxey for Tyrese Haliburton at #10 | 29.04 / 29.09 | +7.94 / +7.76 | +7.85 |
| 5 | Naz Reid for Kel'el Ware at #63 | 28.75 / 27.72 | +7.65 / +6.39 | +7.02 |
| 6 | Michael Porter Jr. for Kyrie Irving at #58 | 29.12 / 29.06 | +8.02 / +7.73 | +7.88 |
| 7 | Draymond Green for Neemias Queta at #130 | 27.17 / 27.13 | +6.07 / +5.80 | +5.94 |
| 8 | Bobby Portis for Christian Braun at #154 | 27.06 / 27.05 | +5.96 / +5.72 | +5.84 |

Two changes carry 89% of the best close-to-real board's gain. The curve peaks at 6 changes (29.12 / 29.06, +7.88); the last 2 robust swaps lower it, because by then the roster they were measured against no longer exists. The full 8-change board and the §11 ceiling board, with the band:

| board | changes | shipped engine (2026 / 2027) | at shock 0 | at shock 0.12 | gain vs as drafted at shock 0.06 / 0 / 0.12 (mean) |
|---|---|---|---|---|---|
| as drafted | 0 | 21.10 / 21.33 | 24.42 / 25.43 | 19.40 / 19.02 | — |
| close-to-real, all 8 changes | 8 | 27.06 / 27.05 | 29.73 / 30.13 | 22.12 / 22.37 | +5.84 / +5.00 / +3.04 |
| §11 ceiling (old engine 28.58 / 28.67) | 9 | 28.83 / 28.65 | 33.05 / 33.13 | 22.85 / 22.68 | +7.52 / +8.16 / +3.56 |

Read with both error bars: Monte-Carlo SE 0.41 points per figure, and the structural band (TEAM_WEEK_SHOCK is FRAGILE: +3.4 (no shared games shock (0.0)) / -2.3 (shared games shock doubled (0.12)) on the as-drafted title share). The §11 board's gain is +7.52 on the shipped engine, +8.16 with no shock and +3.56 with it doubled; the sign holds across the band for every board above, the size does not. The §11 ceiling on the shipped engine (28.83 / 28.65) is within noise of its old-engine figure (28.58 / 28.67), while the as-drafted share moved from 22.50 / 21.84 to 21.10 / 21.33: the engine change (finding 2) moved the level and left the retro's conclusions standing.

## 5. The three questions, answered

- **Would the card's suggested players have changed?** No, in practice: the 🎯 at 12 of 13 turns and the top five at 6 of 13 are the same players under the shock-aware measure; the hindsight top three differ at one late turn. The red team's finding moves the odds beside the advice, not the advice.
- **What would the draft changes have been?** The two that matter most, in order of gain: Jalen Johnson instead of Kevin Durant at #15 (card rank 3 at the turn) and James Harden instead of Kawhi Leonard at #34 (card rank 5). The next 4 (Kyshawn George at #111, Tyrese Maxey at #10, Naz Reid at #63, Michael Porter Jr. at #58) add +0.84 together. Both of the big two were on your card that turn, below the pick you made; neither was the 🎯.
- **How much better?** From 21.10 / 21.33 to 28.25 / 28.26 with two changes and 29.12 / 29.06 at best with 6, on the shipped engine; the full close-to-real board's gain is +5.84 on the shipped engine, +5.00 at shock 0 and +3.04 at 0.12. Hindsight, not foresight: every alternative is judged against the final rosters, which no card could see at the turn.

## Watchlist

- Franz Wagner (#58), Dyson Daniels (#63), Caleb Wilson (#87), Josh Hart (#87): positive on the shipped engine, sign not robust to the shock. The next in-season report that quotes a swap should carry its band the same way.
- The card's 🎯 at #63 (Dyson Daniels) is one of the non-robust swaps: the card's measure and the simulator's realized rates still disagree on him by the counting-category compression the red team measured.
- Draymond Green and Bobby Portis were undrafted and appear as robust late alternatives; both are already on this week's free-agent recommendations (Draymond for Braun, Portis for Braun).

## Open-item receipts

Carried from the post-mortem report of the same day (no pull today; the rows are that report's):

Carried verbatim from the 10/14 league report (gated there on 10/15); not re-queried for this post-mortem (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| (this draft) | records only; no web research and no roster pull | Yahoo's 156 names resolve to the lock pool 156 of 156; Yahoo's NBA team agrees with the pool's at all 156 |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this grade (did not check) |

## Repeat-name market check

Carried from the post-mortem report of the same day (no refresh today):

Carried verbatim from the 10/14 league report; the same 33 rooms, not replayed again here (did not check).

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
- The availability-scale mismatch (D-PM-4: ranking 0.78 for risk, simulation 0.75 of 0.88) stays as shipped on both the card and the simulator; reconciling it is an engine change you have not decided.
- Ties (D-PM-2) are not modelled; symmetric, judged non-load-bearing.
- Alternatives are single swaps of your pick; the other eleven seats draft as they did (a later seat that took the alternative gets your player). A different pick by you would have changed what the room did next; that is not modelled here or in §11.
- The card is screened, not re-drafted: the shock-aware measure is applied to the page's rule at each real turn, not to a replayed draft.

**In scope and unverified.**
- Joint moves in the shock band: the cumulative boards were run at shock 0 and 0.12 only for the full close-to-real board and the §11 board, not for every step of the curve; `NOT-ATTEMPTED` for the intermediate steps, judged non-load-bearing because the two-change and best boards sit between those two.
- The screens keep the top three by each measure; an alternative outside both top threes with a larger simulated gain would be missed. `NOT-ATTEMPTED` as a full simulation of every legal alternative (about 3,000 boards); the §11 retro had the same bound.

## Decision sheet (owner disposes)

| id | decision | recommended |
|---|---|---|
| D-RR-1 | the card's ECW leg: (a) make it shock-aware on the page (same names, honest edges; a deck change, red-first, own PR); (b) leave, since the order does not move | (b) until D-PM-1 lands a measured shock |
| D-RR-2 | every swap, pickup or trade verdict from here on carries its shock band (the two band runs add about a minute): (a) adopt as the standing rule; (b) only for verdicts within 2 points of the noise line | (a) |
| D-RR-3 | the two big misses (#15 and #34) were card ranks 3 and 5 at their turns, below your pick: (a) record both on the lessons ledger as the pattern to test next draft (the card's own first choice taken 7 of 13 times, the misses sat on the card either way); (b) no action | (a) |

## Provenance

- Session: Claude Code (claude.ai/code), 2026-10-19, kit branch `claude/market-data-workorder-mnfi2b`; deck `259c630` read-only; pool `players_v69.csv`; rosters `draft_state_100.json`.
- Records: `retro_redteam.json` (screens, swaps, bands, boards), `cumulative.json` (the curve), this folder; the standing sweep record `redteam-2026-10-19/sweep.json` for the band sentence; `draft-league-2026-10-14/retro_picks.json` for the §11 ceiling board.
- Runs: screens 13 turns × every legal alternative both ways; swaps 26 boards + baseline × 2 seeds × 10,000 seasons; band 23 swaps + baseline × 2 shocks × 2 seeds × 6,000; boards 2 × (2 seeds × 10,000 + 2 shocks × 2 seeds × 6,000); curve 8 boards × 2 seeds × 10,000. Baseline within 3 SE of the 10,000-season reference on both seeds (exactly equal: same simulator, same seeds).
- Re-verify: `python3 report/after-reports/retro-redteam-2026-10-19/retro_redteam.py` then `cumulative.py` then `write_retro_redteam.py`; `python3 scripts/gates.py --verify --report report/after-reports/after-report-2026-10-19-retro-redteam.md`.

## In plain language

You asked whether the red team's findings would have changed what the card told you on draft night. They would not: with the games shock accounted for, the card's first choice is the same player at twelve of thirteen turns and its top five is the same at 6. What the findings change is how sure we are of the odds. Re-running every hindsight swap on the engine we actually ship, and then again with the shock at zero and at double, 4 of the 23 swaps that looked like clear misses turn out to depend on that one unmeasured number, including the card's own first choice at #63. The robust ones say this: had you taken Jalen Johnson at #15 instead of Kevin Durant and James Harden at #34 instead of Kawhi Leonard, your title odds would be about 28 percent instead of about 21, and the best version of a draft that stays close to yours is about 29 percent with 6 changes. Those numbers come with two uncertainties: about half a point from the dice, and a band on the gain that runs from +5.0 with no games shock to +3.0 with it doubled, for the full close-to-real board. Both big changes were on your card at the turn, a few rows below the pick you made.
