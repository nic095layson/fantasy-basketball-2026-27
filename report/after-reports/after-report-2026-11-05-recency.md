# Should the tool weight recent form more heavily? A walk-forward test of recency against the season blend (owner question 2026-11-05)

Pull window: 2026-10-16 → 2026-11-04 (no pull: the box-score records on season/daily 8408911 read only, 18 game days; the preseason line from the deck's players_v69.csv; kit main 249fade, deck main e14cc42).

**Method up front.** The owner's hypothesis, after the Ziaire Williams and Julian Champagnie case: lines that weight recent games should predict better than the tool's season blend, and if so the whole tool should move that way. The blend today (`season_lines.py`): a prior worth 9.5 to 37.5 games of the preseason line, by category, derived from year-over-year stability, plus every game this season at full weight; no recency weighting inside the season. Method and parameters were stated to the owner before the run (the plan table of 2026-11-05): every pooled player with 6 or more games (243 players), a walk-forward test that predicts each player's next game from his earlier games only, from his 5th game on (1,029 player-games); ten estimators; mean absolute error per game and signed bias per category; each estimator paired against the current blend with a bootstrap over players (2,000 draws, 95% interval). Minutes are scored the same way as the role signal. Robustness: 8 or more games (189 players, 884 player-games); a split by whether a player's minutes moved 6 or more between his first four and last four games. A1: the next single game is the target, since the brief re-runs daily; weekly totals were not scored. A2: ten games is a short season; every reading here is a first reading, and the report says when the sample grows. EVIDENCE marks what a run showed; INFERENCE what is derived; MEMORY marks background knowledge not checked against a source in this session.

**Verdict: recency on the stats themselves does not hold. Every recent-form estimator (last 4 games, exponentially weighted means) is worse than the current blend on steals, turnovers, FG% and FT%, worse or no different on the rest, and never better on a 9-cat category. What does hold is weaker and more specific: the blend's prior is somewhat too strong for points, rebounds and assists at this point of the season (halving it improves all three, intervals excluding zero), and recent form predicts minutes far better than any blend (a role signal). The kit already carries the build that uses exactly that signal, the minutes-trend candidate line, and its first graded week beat the blend on all three categories. Recommendation: no engine change now; let the candidate's pre-committed switch rule run, and re-measure the prior strength each Monday.**

## 1. The question, made falsifiable

H1 (the owner's): a line built from a player's recent games predicts his next game better than the blend, on the categories the league scores. Falsified if no recent-form estimator beats the blend with a bootstrap interval excluding zero on any category.
H2 (weaker): the blend trusts the preseason line too much this early; a weaker prior predicts better. Falsified if halving the prior does not beat the blend.
H3 (mechanism): recent form carries information mainly through minutes (role), not through per-minute production. Supported if recent-form estimators beat the blend on minutes and not on stats, and if the gain concentrates in players whose minutes moved.

## 2. Results, all players with 6+ games (EVIDENCE: `recency-2026-11-05/backtest_min6.json`)

Mean absolute error per game, next-game target; in brackets the difference from the current blend, "better" or "worse" only when the bootstrap interval excludes zero, "(ns)" otherwise. FG% and FT% are scored as made shots against expected made on the game's own attempts. MIN has no preseason column in the pool, so its "preseason" row is the mean of the player's first four games.

| estimator | PTS | REB | AST | STL | BLK | 3PM | TO | FG% | FT% | MIN |
|---|---|---|---|---|---|---|---|---|---|---|
| preseason | 5.307 (+0.277 worse) | 2.014 (+0.075 worse) | 1.505 (+0.054 worse) | 0.759 (+0.007 worse) | 0.578 (+0.010 worse) | 1.022 (+0.039 worse) | 1.003 (+0.014 worse) | 1.200 (-0.003 (ns)) | 0.632 (-0.002 (ns)) | 4.797 (+0.117 worse) |
| blend (current) | 5.030 | 1.939 | 1.452 | 0.752 | 0.567 | 0.983 | 0.988 | 1.203 | 0.634 | 4.680 |
| season mean | 5.035 (+0.005 (ns)) | 1.964 (+0.025 (ns)) | 1.478 (+0.026 (ns)) | 0.785 (+0.034 worse) | 0.570 (+0.002 (ns)) | 1.002 (+0.019 (ns)) | 1.053 (+0.065 worse) | 1.312 (+0.109 worse) | 0.716 (+0.082 worse) | 4.538 (-0.141 better) |
| last 4 | 5.114 (+0.084 (ns)) | 2.036 (+0.097 worse) | 1.518 (+0.067 worse) | 0.808 (+0.056 worse) | 0.571 (+0.003 (ns)) | 1.026 (+0.043 worse) | 1.068 (+0.080 worse) | 1.359 (+0.156 worse) | 0.767 (+0.133 worse) | 4.475 (-0.204 better) |
| ewma hl3 | 5.044 (+0.014 (ns)) | 1.992 (+0.053 (ns)) | 1.493 (+0.042 worse) | 0.794 (+0.042 worse) | 0.571 (+0.004 (ns)) | 1.006 (+0.023 (ns)) | 1.062 (+0.074 worse) | 1.328 (+0.125 worse) | 0.731 (+0.097 worse) | 4.446 (-0.233 better) |
| ewma hl6 | 5.031 (+0.001 (ns)) | 1.974 (+0.035 (ns)) | 1.483 (+0.032 (ns)) | 0.788 (+0.036 worse) | 0.570 (+0.002 (ns)) | 1.003 (+0.020 (ns)) | 1.056 (+0.067 worse) | 1.317 (+0.114 worse) | 0.722 (+0.088 worse) | 4.474 (-0.206 better) |
| blend, prior /2 | 4.955 (-0.074 better) | 1.918 (-0.021 better) | 1.437 (-0.015 better) | 0.752 (-0.000 (ns)) | 0.566 (-0.002 (ns)) | 0.977 (-0.006 (ns)) | 0.991 (+0.003 (ns)) | 1.207 (+0.004 (ns)) | 0.637 (+0.003 (ns)) | 4.633 (-0.047 better) |
| blend, prior x2 | 5.120 (+0.091 worse) | 1.965 (+0.026 worse) | 1.470 (+0.018 worse) | 0.754 (+0.002 (ns)) | 0.571 (+0.003 (ns)) | 0.994 (+0.011 worse) | 0.991 (+0.003 (ns)) | 1.201 (-0.002 (ns)) | 0.633 (-0.001 (ns)) | 4.722 (+0.043 worse) |
| blend + ewma hl3 actuals | 5.025 (-0.005 (ns)) | 1.936 (-0.004 (ns)) | 1.449 (-0.002 (ns)) | 0.753 (+0.001 (ns)) | 0.566 (-0.001 (ns)) | 0.980 (-0.003 (ns)) | 0.991 (+0.003 (ns)) | 1.203 (+0.000 (ns)) | 0.634 (+0.000 (ns)) | 4.609 (-0.071 better) |
| blend + ewma hl6 actuals | 5.026 (-0.004 (ns)) | 1.937 (-0.002 (ns)) | 1.450 (-0.001 (ns)) | 0.752 (+0.001 (ns)) | 0.567 (-0.001 (ns)) | 0.981 (-0.002 (ns)) | 0.990 (+0.001 (ns)) | 1.203 (-0.000 (ns)) | 0.634 (+0.000 (ns)) | 4.642 (-0.037 better) |

Reading the table:

- **H1 is falsified.** "Last 4" and both exponentially weighted means are worse than the blend on REB, AST, STL, 3PM, TO, FG% and FT%, and no different on PTS and BLK. Not one 9-cat category improves. The percentages suffer most (FG% +0.13 to +0.16 made shots per game of error, FT% +0.09 to +0.13): a hot or cold shooting stretch over a handful of attempts is noise that the blend's 26- and 37.5-game priors correctly damp.
- **H2 holds, narrowly.** Halving the prior beats the blend on PTS (−0.074), REB (−0.021) and AST (−0.015), all intervals excluding zero, and is no different elsewhere; doubling it is worse on those three and on 3PM. INFERENCE: at 10 games the blend under-reacts to real level changes in the three volume categories, while its percentage and steal priors are about right. Recency-weighting the actuals inside the blend ("blend + ewma") changes nothing, so the issue is the prior's weight, not the order of the games.
- **H3 holds.** On minutes, every recent-form estimator beats the blend by 0.14 to 0.23 minutes with intervals excluding zero, and the blend-style minutes carry a bias of +1.2 minutes (players are playing more than their early games implied). Role moves first and shows in minutes; the stats follow with noise on top.

## 3. Robustness (EVIDENCE: `backtest_min8.json`, `backtest_min6_moved.json`, `backtest_min6_stable.json`)

| check | finding |
|---|---|
| 8+ games only (189 players, 884 player-games) | same shape: last 4 worse on PTS, REB, AST, STL, 3PM, TO, FG%, FT%; prior /2 better on PTS (−0.065, interval excluding zero), no different on REB and AST; recency better on minutes (−0.20) |
| players whose minutes moved 6+ (35 players, 153 player-games) | recency does not rescue the stats even here: last 4 worse on REB, AST, STL, 3PM, FG%, FT%, no different on PTS; on minutes it is far better (−1.5 minutes, 67% to 81% of games closer) and the blend's minutes bias is +3.0 |
| players with stable minutes (208 players, 876 player-games) | last 4 worse on REB, AST, STL, 3PM, TO, FG%, FT%; prior /2 better on PTS, REB, AST; recency no different on minutes |

INFERENCE: the role signal is real and large, and it is almost entirely a minutes signal. Scaling a player's rates by his recent minutes is the right place for recency; weighting his recent box scores is not.

## 4. The build the kit already has (EVIDENCE: `scripts/minutes_line.py`, `report/accuracy.md`)

Build 2 of 2026-10-27, the minutes-trend candidate line, does what section 3 points to: the blend's per-minute rates scaled by a recency-weighted minutes forecast (half-life 5 games, a 3-game preseason prior on minutes, both registered uncalibrated under D-ML-1). It is a candidate: nothing on the board, in the brief or in the simulator reads it; the Monday accuracy card grades it beside the blend. Week 2, the first graded week with all three lines:

| line | PTS MAE | PTS bias | REB MAE | AST MAE |
|---|---|---|---|---|
| preseason | 3.60 | +10.6% | 1.41 | 1.06 |
| in-season blend | 3.46 | +8.7% | 1.35 | 1.02 |
| minutes candidate | 3.34 | +7.6% | 1.31 | 1.00 |

The pre-committed switch rule (D-ML-1): the candidate replaces nothing until its MAE beats the blend's on PTS, REB and AST in 3 of 4 consecutive graded weeks, on the owner's word. Week 2 is one of the three. Week 3 grades on Monday 2026-11-09.

## 5. The case that started this, re-read (EVIDENCE: the 11-05 what-if runs; the lines below)

| per game | Ziaire Williams: preseason | blend (7 games) | blend with prior halved | actual, 7 games |
|---|---|---|---|---|
| FG% | .424 | .453 | .472 | .574 |
| points | 10.2 | 10.6 | 10.7 | 11.1 |
| turnovers | 1.1 | 0.88 | 0.76 | 0.43 |
| minutes | preseason mpg on file | blend trusts stats at a ~12-game prior | | 23.3, 5 starts of 7, rising |

The owner's read of Ziaire was right, and section 2 says why the tool lagged it: his FG% and turnover gains sit in the two slowest-moving priors (26 and 14 games), and his role change is a minutes signal the blend does not read at all. Champagnie's blend line matched his season average, but one 26-point game carried that average; on his last four games he is below his line. INFERENCE: both cases are the H3 mechanism, not a case for weighting recent box scores, which section 2 shows would have hurt on the percentages for the pool as a whole. A small discrepancy, not chased and not load-bearing: the pool's blended Ziaire line (10.4 points, .443) differs by a few tenths from the recomputation here (10.6, .453); the game set is the same, so the difference is in the preseason source or a rounding step.

## 6. Background (MEMORY, not checked against a source in this session)

Projection systems that pool past data with a prior and regress toward it are standard (the Marcel family for baseball; in basketball, the stabilization-point literature that measures how many attempts a rate needs before it carries more signal than noise). Two of their results match what the table shows: rates on few attempts (shooting percentages, steals, blocks) stabilise slowly and need strong priors; volume per game stabilises faster and is driven by minutes, which change with role. The derived-prior design in `season_lines.py` is a one-parameter version of that idea. None of this was verified here, and the figures in this report rest on the kit's records alone.

## 7. What this means for the whole tool

- The blend is the right structure. The evidence argues for re-measuring its prior strength on the counting categories as games accumulate, not for replacing it with recency.
- Recency belongs in minutes. The candidate line is that build, already graded weekly.
- The daily brief and the title simulator read the blend. Any change to the prior or the candidate's promotion changes every pick, every title share and every band, so each is an engine change: red-team sweep, registry update, owner go.
- The percentages should not move. On FG% and FT% every alternative is worse or no different.

## 8. Bands quoted

No title share is quoted as a new figure. The what-if title shares of the 11-05 Ziaire assessment (8.7% baseline; 12.5% on his season line) carry the standing structural band of the season sweep of 2026-11-02 (deck e14cc42): **weekly_availability is FRAGILE:** -2.6 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.2 (healthy players play 0.95 of games) / +0.0 (healthy players play 0.80 of games).

Runner impact: none. Research only; no code, step or prompt changed.

## 9. Decisions for the owner (assessment only; a build waits for the owner's pick)

1. **Stay the course (Recommended).** No engine change. The minutes candidate keeps grading under D-ML-1; its promotion, if it earns it, is the recency change the evidence supports. Re-run this backtest at week 5 (2026-11-16, with the confidence re-run) when players have about 20 games, to see whether the prior-strength finding holds and in which direction it is moving.
2. **Make the backtest a Monday step.** `backtest.py` (in `recency-2026-11-05/`) runs beside the accuracy card each Monday and writes the prior-strength table to the record; the card quotes "prior /2 vs blend" per category. No engine change; a small build on its own PR.
3. **Halve the counting priors now.** PTS, REB and AST priors to about 6 games. An engine change on week-3 evidence: every title share moves; needs the red-team sweep and a registry update; the percentages and steals stay as they are.
4. **Show form beside each pick, display only.** The last-4 line beside the blend on waiver and streaming picks, so the owner sees what the table shows without the tool acting on it.

## 10. Bounds and open items

- Out of scope by design: weekly totals as a target (A1); the league's own game-to-game scoring weights; news on roles.
- In scope and unverified: whether the prior-strength finding survives 20 games (the week-5 re-run); the pool-line discrepancy in section 5.
- Not attempted: a per-player prior (strong for established players, weak for rookies and role changers), which the role split suggests and the sample cannot yet fit.

## Watchlist

- 2026-11-09: week 3 on the accuracy card, the candidate's second graded week under D-ML-1.
- 2026-11-16: the week-5 confidence re-run; re-run `backtest.py` on about 20 games per player.

## Open-item receipts

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck 366d3ca (this PR changes no deck file), checked today, the same page the 10/22 day report replayed. Its table stands, carried here verbatim from the day report.

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 6a5cefea4921), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 33 of 33 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 32 of 33 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 23 of 33 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 14 of 33 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 33 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| John Collins | 11 of 33 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 10 of 33 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 10 of 33 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 9 of 33 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 7 of 33 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 7 of 33 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 33 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 33 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (17 mocks, value 27, market 45); Lauri Markkanen (15 mocks, value 21, market 37); Tyrese Haliburton (13 mocks, value 7, market 12); Tyrese Maxey (11 mocks, value 5, market 9); Kel'el Ware (10 mocks, value 57, market 77); Tyler Herro (9 mocks, value 51, market 69); Karl-Anthony Towns (8 mocks, value 12, market 15); Miles Bridges (5 mocks, value 96, market 98).
