# After-report — post-mortem of the league draft (2026-10-14): the draft graded from the records, and a red-team pass on the engine's computation and category calculations

**Owner request (2026-10-19, verbatim):** "Please provide a post-mortem for our league's draft. Conduct red team analysis of computation and categorical calculations".

**What was analyzed.** The 10/14 league draft on the locked lines (pool tag v69, deck `arena/results/players_v69.csv`), its grade files (`m100_final`, `m100_deckcard_v69`, `m100_hindsight`, `m100_arms`, the two 10,000-season runs), the kit's follow-up records (`card_vs_owner`, `retro_picks`, `waiver_moves`, `stress`, `opponents_vs_history`), and the engine itself: `scripts/hoops.py` (z-scores over the top-156 fixed point, availability tiers, adjusted value) and `arena/arena.py` (daily-fill weekly model, category-record standings, the 8-team bracket). **Method.** Every red-team check is a script in `postmortem-2026-10-19/` writing a JSON record this report reads: a from-scratch re-implementation of the category math compared to the engine (`rt_math.py`, `rt_join.py`); the card's measure against the simulator's realized rates (`rt_consistency.py`); integer ties the simulator cannot produce (`rt_ties.py`); the title share under each structural assumption, one at a time (`rt_sensitivity.py`, 6,000 seasons on two seeds, the baseline asserted within 3 standard errors of the 10,000-season reference); and whether the two headline swap verdicts survive those variants (`rt_decisions.py`). No line, tag, price or engine constant changed.

**Headline.** The computation is right: an independent re-implementation of the z-scores, the availability tiers, the board order and the weekly percentage and counting math reproduces the engine exactly (largest z-score difference 0.0e+00), and the two planes' boards differ on 0 of 309 joined rows' lines. The card's measure and the simulator agree to a mean 1.1 points per category (rank agreement with title share 0.99). What is **not** right is the precision implied around the title share: the level moves by 2.7 points one way and 3.3 the other under one uncalibrated constant (the shared games shock, 0.06, set to 0 and to 0.12), against the ±0.4 Monte-Carlo error the reports quoted and the ±0.5 noise line the retro used. The draft decisions survive that: Draymond for Braun and Jalen Johnson over Durant stay positive on both seeds under every variant. The draft itself graded 7 of 13 on the card's 🎯, title share 22.50 / 21.84 percent (rank 1 / 1); 10 of the 13 picks had a clearly better player available in hindsight, 4 of them by 1.5 title points or more (#15, #34, #111, #154); 4 of those misses were the card's own first choice, so they are hindsight's disagreement with the projections, not departures from the card.

Pull window: 2026-10-19 → 2026-10-19 (analysis only; no roster pull, no line change).

## 1. Roster changes

None. No line, tag, placement, price or engine constant changed on either plane.

## 2. The draft, graded from the records

EVIDENCE: `m100_deckcard_v69.json` (the page's card before each turn), `m100_hindsight.json` (every legal alternative by weekly category wins against the final rosters), `retro_picks.json` (the top alternatives swapped in pairwise, 10,000 seasons on seeds 2026 and 2027), `m100_arms.json` (house arms, 18,000 seasons). Baselines: title 22.50 / 21.84 percent, ECW 5.144 rank 1, favored in 11 of 11 head-to-heads; the card's 🎯 taken at 7 of 13 turns, its Top 5 at 12; following the 🎯 at every turn grades 24.55 percent against 21.78 as drafted on the house arms. **Tiers:** BEST AVAILABLE = no legal alternative beat the pick even by ECW; HELD = alternatives existed but none clears +0.5 title points on both seeds; MISS = one does; COSTLY MISS = by 1.5 points or more on the mean of the two seeds.

| pick | you took | card rank of your pick | the card's 🎯 | players better by ECW | best alternative (title shift, seed 2026 / 2027) | tier |
|---|---|---|---|---|---|---|
| #10 | Tyrese Haliburton | 2 | Tyrese Maxey | 1 of 295 | Tyrese Maxey (+0.79 / +0.78) | MISS |
| #15 | Kevin Durant | 1 | Kevin Durant | 7 of 291 | Jalen Johnson (+2.17 / +1.81) | COSTLY MISS |
| #34 | Kawhi Leonard | 1 | Kawhi Leonard | 2 of 273 | James Harden (+1.81 / +1.90) | COSTLY MISS |
| #39 | Derrick White | 1 | Derrick White | 1 of 269 | James Harden (-0.47 / -0.76) | HELD |
| #58 | Kyrie Irving | 1 | Kyrie Irving | 2 of 251 | Michael Porter Jr. (+0.55 / +1.02) | MISS |
| #63 | Kel'el Ware | 2 | Dyson Daniels | 3 of 247 | Michael Porter Jr. (+1.57 / +1.31) | MISS |
| #82 | Ty Jerome | 1 | Ty Jerome | 0 of 229 | Immanuel Quickley (-1.33 / -1.11) | BEST AVAILABLE |
| #87 | Jaden McDaniels | 1 | Jaden McDaniels | 2 of 225 | Caleb Wilson (+0.65 / +0.84) | MISS |
| #106 | Miles Bridges | 1 | Miles Bridges | 0 of 207 | Kyshawn George (-1.54 / -0.68) | BEST AVAILABLE |
| #111 | Yaxel Lendeborg | 3 | Jakob Poeltl | 6 of 203 | Kyshawn George (+1.84 / +1.57) | COSTLY MISS |
| #130 | Neemias Queta | 2 | Jakob Poeltl | 3 of 162 | Kyshawn George (+1.40 / +0.75) | MISS |
| #135 | PJ Washington | 9 | Jakob Poeltl | 2 of 158 | Kyshawn George (+0.68 / +0.86) | MISS |
| #154 | Christian Braun | 3 | Tobias Harris | 5 of 141 | Draymond Green (+1.54 / +1.72) | COSTLY MISS |

**Reading it.** 2 picks were the best available by the engine's own measure, 1 held, 6 were misses and 4 costly. The misses split two ways. 4 (#15, #34, #58, #87) were the card's own first choice at the time: hindsight scores them against the final rosters, which the card could not see, so these are the projections' disagreement with the later picks, not yours with the card. 6 (#10, #63, #111, #130, #135, #154) were turns off the card where a better player was on the board. Of the six turns off the 🎯, your pick graded better on title share than the card's on both seeds at 4 (#63, #111, #130, #135), the card's at 2 (#10, #154) (`card_vs_owner.json`). The combined hindsight ceiling (every better pick at once, each player used once) is 28.58 / 28.67 percent; it knows every later pick and is not an attainable draft.

**The pickup scan.** 8 of 520 add/drop pairs improve the team, every one dropping Braun, Queta, Washington or Lendeborg (`waiver_moves.json`); the best, Draymond Green for Braun, is +1.54 / +1.72 title points at full availability and -1.25 / -1.30 at the 0.78 tier (`waiver_draymond_risk.json`). The injury stress (`stress.json`): a full-season loss of Haliburton or Durant leaves 11.2 percent.

## 3. Red team: the computation

EVIDENCE: `rt_math.py` → `rt_math.json`; `rt_join.py` → `rt_join.json`. The category math was re-implemented from the documented formulas without importing the engine's functions (league percentage baselines weighted by attempts; percentage impact = (rate − league rate) × attempts; population standard deviation; turnovers sign-flipped; the top-156 fixed point iterated from the full-pool pass), then compared cell by cell on the 335-row lock pool.

| check | result | verdict |
|---|---|---|
| z-scores, all 9 categories, all 335 rows | max abs difference 0.0e+00; fixed point in 3 iterations | PASS |
| availability tiers from the note tag (1.0 / 0.85 / 0.78 / 0) | max abs difference 0.0e+00 | PASS |
| board order (adjusted value, availability > 0) | 318 rows, first order difference: none | PASS |
| your weekly team FG% = makes ÷ attempts, not a mean of rates | engine 0.4909, known answer 0.4909, the naive mean would be 0.4988 | PASS |
| weekly FG% variance = binomial on attempts × 1.15² | engine 6.81e-04, known answer 6.81e-04 | PASS |
| weekly points mean and variance (daily-fill weights × 3.5 × availability; compound-sum variance) | mean 648.62 vs 648.62; variance 2769.5 vs 2769.5 | PASS |
| kit board vs deck pool, per-game lines | 309 of 325 kit rows join (302 exact, 7 by folding); 0 line differences on 11 columns; 6 more join by surname with 0 differences; 10 rows are kit-only | PASS with a limit: the kit's documented alias table (6 entries) resolves 0 of the 16 unmatched spellings |

The one defect in this table is not in the arithmetic. The kit's alias table does not cover the spellings its own board uses for Cam Johnson, Mikel Brown, Dereck Lively, Kelly Oubre, Herb Jones, Darius Acuff (suffixes and short first names), so any cross-plane check that joins by that table silently drops them. Their lines agree with the deck's; the join does not. D-PM-5.

## 4. Red team: the category model against the simulator, and ties

EVIDENCE: `rt_consistency.py` → `rt_consistency.json`; `rt_ties.py` → `rt_ties.json`. The card scores a roster by expected weekly category wins (ECW): a normal approximation per category, independent categories, averaged over the 11 opponents. The simulator draws the same model but adds the shared games shock (0.06) and random pairings, and the title runs through seeding and a bracket. If the two disagree, the card is advising on something the seasons do not reward.

| check | seed 2026 | seed 2027 | verdict |
|---|---|---|---|
| every category sums to 50% across the 12 teams | True | True | PASS |
| max gap, ECW vs simulated category rate, any seat and category (points) | 4.6 | 4.7 | PASS with a limit |
| mean gap (points) | 1.1 | 1.1 | PASS |
| rank agreement, ECW vs title share (Spearman) | 0.986 | 0.979 | PASS |
| rank agreement, ECW vs cats per week | 0.993 | 0.993 | PASS |

Your own categories, the card's probability against the simulator's rate (seed 2026):

| category | card (ECW) | simulator | gap (points) |
|---|---|---|---|
| FG% | 0.582 | 0.581 | -0.1 |
| FT% | 0.736 | 0.737 | +0.1 |
| 3PTM | 0.609 | 0.604 | -0.5 |
| PTS | 0.392 | 0.412 | +2.0 |
| REB | 0.389 | 0.408 | +1.9 |
| AST | 0.305 | 0.327 | +2.2 |
| ST | 0.514 | 0.514 | +0.0 |
| BLK | 0.712 | 0.703 | -0.9 |
| TO | 0.904 | 0.874 | -3.0 |

The pattern is systematic, not noise: the shared shock adds variance to every counting category, which pulls the simulator's rates toward 50 percent. Your strongest counting edge (turnovers, 0.904 on the card) realizes at 0.874; your weak counting categories realize a little better than the card says. The card overstates its edges in the counting categories by about 2 to 3 points and is exact on the percentages. Ranking is unaffected (0.993 agreement). Limit, not bug.

**Ties.** The simulator draws continuous values, so no category ever ties; Yahoo scores a tie as a T for both sides. Rounding the same draws to integers (percentages to three decimals) across your 11 matchups, 220,000 matchup-weeks per seed: blocks tie 4.5 percent of the time, steals 4.3, threes 2.6, turnovers 1.6, the rest under 1.5; 0.17 tied categories per matchup, about one every six weeks (seed 2027: 0.17). The simulator resolves each as a coin flip, which is unbiased in expectation; the cost is a 5-4 week it calls when the real result is 4-4-1. Limit, not bug. D-PM-2.

## 5. Red team: how much the title share depends on each assumption

EVIDENCE: `rt_sensitivity.py` → `rt_sensitivity.json` (6,000 seasons per variant on seeds 2026 and 2027; Monte-Carlo SE 0.54 points; the baseline reproduced the 10,000-season reference within 3 SE on both seeds: {'2026': True, '2027': True}). One assumption changed per row, the final rosters held fixed. **Tiers:** ROBUST = under 1 point on both seeds; SENSITIVE = 1 to 2; FRAGILE = 2 or more.

| assumption varied | title %, seed 2026 / 2027 | shift vs baseline (mean of the two seeds) | tier |
|---|---|---|---|
| baseline (18 weeks, category record, 0.88/0.75, shock 0.06) | 22.53 / 21.70 | +0.00 / +0.00 (+0.00) | baseline |
| 17 regular-season weeks | 21.78 / 22.20 | -0.75 / +0.50 (-0.12) | ROBUST |
| 20 regular-season weeks | 20.53 / 22.73 | -2.00 / +1.03 (-0.48) | ROBUST |
| standings by weekly wins (not the category record) | 21.88 / 21.97 | -0.65 / +0.27 (-0.19) | ROBUST |
| no in-sim injury discount (risk 0.88 like healthy) | 20.62 / 18.92 | -1.91 / -2.78 (-2.34) | FRAGILE |
| harsher risk tier (0.65) | 23.28 / 21.73 | +0.75 / +0.03 (+0.39) | ROBUST |
| healthy players play 0.95 of games | 20.65 / 20.50 | -1.88 / -1.20 (-1.54) | SENSITIVE |
| healthy players play 0.80 of games | 23.75 / 22.53 | +1.22 / +0.83 (+1.03) | SENSITIVE |
| no shared games shock | 24.77 / 24.78 | +2.24 / +3.08 (+2.66) | FRAGILE |
| shared games shock doubled (0.12) | 18.78 / 18.83 | -3.75 / -2.87 (-3.31) | FRAGILE |
| per-game variance x0.8 | 21.48 / 20.95 | -1.05 / -0.75 (-0.90) | ROBUST |
| per-game variance x1.2 | 22.23 / 21.38 | -0.30 / -0.32 (-0.31) | ROBUST |
| percentages share a hot/cold shock (0.5 sd) | 21.52 / 20.48 | -1.01 / -1.22 (-1.12) | SENSITIVE |

**Reading it.** The league-format assumptions (17 or 20 regular-season weeks, standings by weekly wins) are ROBUST, ROBUST, ROBUST: the title share barely moves, though weekly-win standings cut the playoff share by 2.1 / 2.8 points. FRAGILE: no in-sim injury discount (risk 0.88 like healthy) (-2.3); no shared games shock (+2.7); shared games shock doubled (0.12) (-3.3). SENSITIVE: healthy players play 0.95 of games (-1.5); healthy players play 0.80 of games (+1.0); percentages share a hot/cold shock (0.5 sd) (-1.1). The shared games shock is the one that matters most and is the least grounded: at 0 the title share is 24.8 / 24.8, at 0.12 it is 18.8 / 18.8. That constant (`arena.TEAM_WEEK_SHOCK = 0.06`) has no calibration record I could find in either repository; it was set by judgment. Giving risk-tagged players full games in the simulation costs you 2.3 points because the rivals' risk-tagged players outnumber yours; that tier at least has a calibration record (2025-26 games played). **Every title figure this project has quoted carries roughly ±3 points of structural uncertainty from the shock alone, on top of the ±0.4 Monte-Carlo error the reports stated.** The ±0.5 noise line the retro used for single-swap verdicts covered the Monte-Carlo error only. D-PM-1, D-PM-6.

**Do the decisions survive?** EVIDENCE: `rt_decisions.py` → `rt_decisions.json`. The two headline swaps re-run against the baseline under the same variant, so the structural constant moves both sides.

| variant | Draymond Green for Braun (title shift, 2026 / 2027) | Jalen Johnson over Durant at #15 |
|---|---|---|
| shock 0.06 (shipped) | +1.97 / +1.63 | +2.42 / +1.92 |
| shock 0 | +2.63 / +1.07 | +3.87 / +4.05 |
| shock 0.12 | +1.42 / +0.98 | +1.33 / +1.22 |
| no in-sim injury discount | +1.37 / +1.82 | +1.55 / +3.60 |

Both stay positive on both seeds under every variant (SE of a difference 0.76 points). The verdicts are robust where the level is not: a structural constant shifts every arm together. The size of a gain is not robust (Jalen Johnson's ranges from +1.2 to +4.1), so a gain's magnitude should be read as a band, not a number.

## 6. Process defects found while doing this

1. **A rank read as a games count (chat, 2026-10-16).** The Kyle roster read said the board projected Giannis for 39 games. The MG report's row reads "58 → 39" for the kit rank and "67 | 68 | 69" for games (ours, Yahoo, Hashtag): the 39 was his board rank, his games were held at 67. Corrected in chat on 10/16; it reached no committed report. The lesson is the standing one: a figure quoted in chat from memory of a record is a figure typed by hand.
2. **A harness leak, caught by its own check.** The first sensitivity run patched engine constants inside worker processes that were reused across variants, so later variants inherited earlier patches; the symptom was seed-to-seed gaps of 3 to 4 points where the Monte-Carlo error allowed 1. The fix reloads the engine module per job, and the script now asserts the baseline within 3 SE of the 10,000-season reference (seeds 2026 and 2027: within). The contaminated run was discarded; nothing from it is quoted.
3. **The noise line was too narrow.** The retro's +0.5 rule separated swaps from Monte-Carlo noise only; §5 shows the level's structural band is about six times wider. Verdicts stand (§5), magnitudes do not.
4. **The kit alias table has a gap** (6 entries; 6 of its own board's spellings unresolved). Lines agree; joins do not.
5. **The league's settings are not on file.** The simulator assumes category-record standings, 18 regular-season weeks and Yahoo's ten active slots from the 2025-26 intel; your 10/16 prompt said playoffs are weeks 18 to 20, which implies 17. §5 shows the title share is robust to each, but the assumptions should be a file, not a memory. D-PM-3.

## 7. Verdicts

| item | tier | what would demote it |
|---|---|---|
| the z-score, availability, board-order and weekly-model arithmetic | CORRECT (re-derived to rounding) | any cell of `rt_math.json` above 1e-9 |
| the card's measure as a ranking of rosters | SOUND (0.99 rank agreement with the simulator) | agreement under 0.9 on a future roster set |
| the card's per-category probabilities in counting categories | OVERSTATED by 2 to 3 points | a shock calibration that lands at 0 |
| the title share as a point estimate | OVERPRECISE: ±0.4 stated, about ±3 structural | a calibrated shock within 0.02 of 0.06 |
| the league-format assumptions (weeks, standings rule, slots) | ROBUST but UNVERIFIED | the settings file contradicting them |
| the draft's single-swap verdicts (Draymond, #15) | ROBUST (positive under every variant) | a variant under which either turns negative |
| the draft itself | 2 best-available, 1 held, 6 misses, 4 costly | the projections, once games are played |

## Watchlist

- Draymond Green's status before the 10/21 opener: the one pickup the records support, and the one whose verdict holds under every variant.
- The shared games shock: record real weekly team totals from week 1 so the constant can be calibrated by week 6 (D-PM-1).
- Ties in blocks and steals in your real matchups: the first 4-4-1 week is the model's blind spot, not a surprise.

## Open-item receipts

Carried verbatim from the 10/14 league report (gated there on 10/15); not re-queried for this post-mortem (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| (this draft) | records only; no web research and no roster pull | Yahoo's 156 names resolve to the lock pool 156 of 156; Yahoo's NBA team agrees with the pool's at all 156 |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this grade (did not check) |

## Repeat-name market check

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
- No engine constant, line, tag or price changed; every red-team script reads the engine and writes a record.
- The projections' accuracy against real games: no game has been played; this report tests the computation on the projections, not the projections.
- The daily-fill start-rate model was checked for arithmetic, not for realism against your league's lineup habits.

**In scope and unverified.**
- The league's scoring rule, week count and active slots (A1 to A3): `NOT-ATTEMPTED` as a lookup, because no settings file exists in either repository; tested for sensitivity instead (§5, all ROBUST).
- The shared games shock's true value: `UNVERIFIABLE` until weekly team totals exist; the report treats the title share as a band for that reason.
- The tie rule's effect on standings: measured per matchup (§4), not run through the seasons; `NOT-ATTEMPTED` as a full simulation, judged non-load-bearing because ties are symmetric.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-PM-1 | calibrate the shared games shock (0.06): (a) record weekly team category totals from week 1 and fit it at week 6, red-first, own PR; (b) leave it and quote title shares as a band of about ±3 points; (c) both | (c) |
| D-PM-2 | ties: (a) add a tie rule to the simulator (integer draws, a T scored 0.5), red-first; (b) leave, note the limit in every report | (b) |
| D-PM-3 | league settings: (a) owner pastes the Yahoo settings page and it is pinned as a settings file both engines read; (b) carry A1 to A3 as stated assumptions | (a) |
| D-PM-4 | the two availability scales (ranking 0.78 for risk; simulation 0.75 of 0.88 games, a 0.85 ratio): (a) reconcile after the first month's games, with D-RN-4; (b) leave | (a) |
| D-PM-5 | the kit alias table: (a) add the six board spellings, red-first, own PR; (b) leave | (a) |
| D-PM-6 | reporting rule: every title figure carries both its Monte-Carlo error and the structural band from §5 until D-PM-1 lands | adopt |
| D-LD-2, D-LD-1, D-INT-1, D82-1, D83-1 | carried | carried |

## Provenance

- Inputs: the lock pool (deck `arena/results/players_v69.csv`), the kit board (`report/projections-2026-27.csv`), the league draft state (`arena/data/states/draft_state_100.json`) and its grade files, the kit's 10/14 and 10/13 after-reports and the draft-league folder's JSON records.
- Tools: `rt_math.py`, `rt_join.py`, `rt_consistency.py`, `rt_ties.py`, `rt_sensitivity.py`, `rt_decisions.py`, `write_postmortem.py` (this folder); the deck's `arena.simulate_seasons` for every season run.
- Gates: `report/check_report.py`; the deck's `judgment_open_items.py --check-report` and `repeat_market_check.py --check-report` (exit codes in the PR body).
- No line, tag, price or engine constant changed on either plane; nothing was published.

## In plain language

**The math is right.** I rebuilt the engine's category scoring from the written formulas without using the engine, and it matched to the last decimal: every z-score, every availability tier, the whole board order, and the weekly team percentages and counting totals. The kit and deck boards carry the same lines.

**The precision was wrong.** The title share has been quoted as about 22 percent give or take 0.4. One constant in the simulator, how much a team's categories rise and fall together week to week, was set by judgment and never measured. Turning it off gives about 25 percent; doubling it gives about 19. So read the title share as 22 give or take 3. The league-format assumptions barely matter.

**The advice survives.** Draymond Green for Braun and the retro's Jalen Johnson over Durant stay positive under every version of the model. Their sizes should be read as ranges.

**The card flatters its edges a little.** In counting categories the card's probabilities are 2 to 3 points too confident; it is exact on the percentages, and it ranks rosters the same way the seasons do. The simulator also never ties a category, which real blocks and steals do about once every six weeks.

**The draft.** 2 picks were the best available, 1 held up, and 10 had a clearly better player on the board in hindsight, 4 of them by 1.5 points or more; the largest was #15, Jalen Johnson over Durant. But 4 of those 10 were the card's own first choice, so the bigger lesson is about the projections, not the drafting. Following the card everywhere would have been worth about 2.8 points on the house arms.

**What I got wrong this week.** I read a board rank as a games count for Giannis in chat, and my first sensitivity harness contaminated its own variants; both were caught and neither reached a report. The decisions on the sheet are about measuring the one constant that matters, writing the league settings down, and widening the error bars.
