# Fitting the 750-attempt threes prior, and re-centring the candidate line (owner 2026-11-12)

Pull window: 2026-10-17 → 2026-11-12 (no pull: `data/reference/threes_prior_2025-26.csv` in the kit at main cf331cf and the box scores through 2026-11-11 on the records branch at db51bfb, read only; nothing written to the records).

**Owner's request, verbatim:** "Fit the 750 figure against the 2025-26 data". Then, on a card: "Re-centre it (Recommended)".

**What was analyzed.** The threes-split candidate line (`scripts/threes_line.py`, merged in #265), which pulled each shooter's percentage toward his raw 2025-26 percentage with a flat weight of 750 attempts, a figure from the owner's list that had not been checked against data.

**Method up front,** stated to the owner before the runs. One season, 2025-26 (Basketball-Reference totals on file: 582 players, 90,970 attempts); a single season by the owner's wording, so no multi-season window is involved. Sample: players with 100+ attempts, the kit's own cut-off, repeated at 50+ and 200+. Fit: beta-binomial maximum likelihood, cross-checked by a moments estimate, with 1,000 player resamples for the range (200 at the two side cut-offs). Because that file has season totals only, the kit's actual rule was tested forward on this season's box scores through 2026-11-11: which prior, fixed before the season, gives this season's makes the highest likelihood.

**Verdict: the weight was defensible and the centre was not. The 2025-26 data puts the figure at 356 (95% 249 to 635); this season's games cannot tell 750 from 400. They can tell that a raw last-season percentage predicts worse than the same percentage first pulled toward the league average. The candidate now does that. It is still a candidate: nothing on the board, in the brief or in the simulator reads it.**

Runner impact: code-only — the "threes line" morning step writes the same three files with one column computed differently; its record gains `prior_weight` per player and the method block names the fitted figures. No prompt edit.

## 1. The fit on 2025-26

| Players included | Players | Attempts | Fitted strength | 95% range | Moments estimate | Fitted mean |
|---|---|---|---|---|---|---|
| 50+ attempts | 379 | 88,077 | 339 | 244 to 544 | 344 | .3567 |
| 100+ attempts | 307 | 82,746 | 356 | 249 to 635 | 360 | .3581 |
| 200+ attempts | 191 | 65,705 | 549 | 372 to 1,050 | 538 | .3690 |

EVIDENCE: `threes-prior-fit-2026-11-12/fit_2025-26.txt`, written by `fit_2025-26.py`. The strength is the number of attempts at which a player's own percentage is as informative as the league's. 750 lies above the range at the kit's cut-off and inside it at 200+. The fitted spread of true talent among the 100+ shooters is about 2.5 percentage points.

## 2. The forward check on 2026-27

179 players with 100+ attempts last season and 20+ this season; 9,253 attempts through 2026-11-11.

| Prior centre | Best flat weight | Log-likelihood at best | at 750 | Miss size (attempt-weighted RMSE) |
|---|---|---|---|---|
| Raw last-season % | 200 | −6032.74 | −6033.59 | .0773 |
| League average only | 300 | −6027.67 | −6028.24 | .0755 |
| Last-season % pulled toward the league | 400 | −6023.73 | −6023.83 | .0739 |
| Pulled, weight 356 + last season's attempts | per player | −6023.61 | | |

EVIDENCE: `forward_2026-27.txt`, written by `forward_2026-27.py`. Pulled against raw, both at 750: a gain of 9.76 log-likelihood, 95% 1.41 to 18.15 over 2,000 player resamples, above zero in 98.9% of them. Within one centre the weights 200 to 750 differ by less than 1: the weight is not identified by four weeks. For the raw centre the best weight over 500 resamples ranged from 100 to 20,000.

INFERENCE: the per-player weight (356 plus last season's attempts) is the form the fitted model implies; the forward data neither prefers it nor rejects it against a flat 400 (−6023.61 against −6023.73).

## 3. What changed in the code

`scripts/threes_line.py`: `PCT_PRIOR_ATT = 750.0` is gone. `PCT_PRIOR_K = 356.0` and `PCT_PRIOR_MU = 0.3581`, both registered as measured with the fit as their record. `prior_centre()` returns each player's pulled percentage and its weight; `build()` takes a weight per player. With no games the candidate still equals the preseason line by construction. `MIN_PRIOR_ATT = 100` is unchanged and still uncalibrated.

One correction made during the build: the first version computed the league average as makes over attempts (.363), which leans toward high-volume shooters and is not the mean the fit produced (.3581). The code uses the fitted mean, so the two fitted figures belong to one model.

EVIDENCE, today's records, old rule against new on the same inputs (233 players split under both):

| Player | Live line | Candidate, 750 and raw | Candidate, re-centred | Centre, raw | Centre, pulled |
|---|---|---|---|---|---|
| Ty Jerome | 2.5 | 2.67 | 2.52 | .420 | .372 |
| Kevin Durant | 1.8 | 1.88 | 1.84 | .413 | .389 |
| Julian Champagnie | 2.6 | 2.39 | 2.35 | .381 | .372 |
| Derrick White | 2.3 | 2.29 | 2.31 | .327 | .338 |
| Brandon Miller | 3.0 | 3.55 | 3.53 | .383 | .373 |
| Grayson Allen | 3.1 | 2.67 | 2.68 | .350 | .353 |

The candidate moved by 0.1 threes or more for 6 of 233 players and by 0.05 or more for 48. Against the live line it is now higher by 0.2 or more for 29 and lower for 17 (was 30 and 16).

## 4. Checks

| Check | Result |
|---|---|
| `test_threes_line` | 11 tests OK: two new (the pulled centre and its weight, hand-worked; a per-player weight reaching the split), one updated for the new record fields |
| Constants registry | 52 registered = 52 live (was 51): measured 9, uncalibrated 24 |
| Full suite | 1,188 tests OK, 2 skipped (was 1,186) |
| Gates | PASS and verified (see the commit) |

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds. That is the 2026-11-09 sweep the brief quotes, for the title odds; this change touches neither the title odds nor any constant in that sweep.

## 5. Bounds

Out of scope by design: the live season line, the board, the brief and the simulator; the attempts half of the split; `MIN_PRIOR_ATT`.

In scope and unverified:
- More than one prior season: NOT-ATTEMPTED; the owner asked for 2025-26, and the kit holds three-point attempts for that season only.
- Whether the candidate beats the live line on threes made: not known until the weekly grading (first snapshot Sunday 2026-11-15, first grade Monday 2026-11-23). The forward check here grades the percentage prior alone, not the finished line.
- Talent change from one season to the next (a player who rebuilt his shot): not modelled; the weight treats last season as fully current.

## 6. Next steps (owner decisions)

1. Nothing is needed for this change beyond the merge. The switch rule D-TS-1 stands: the candidate replaces nothing until it beats the live line on threes in 3 of 4 graded weeks, on the owner's word.
2. If the candidate earns the switch, the same pulled-centre idea could be assessed for free-throw and field-goal percentage. Not built.

## 7. Provenance

Session of 2026-11-12 (session model A) on branch `claude/market-data-workorder-mnfi2b`. Scripts and outputs: `report/after-reports/threes-prior-fit-2026-11-12/`. Re-verify: `python3 report/after-reports/threes-prior-fit-2026-11-12/fit_2025-26.py`; the forward script reads the records checkout's `data/actuals`.

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
