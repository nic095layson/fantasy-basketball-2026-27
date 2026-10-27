# Fitting the two fragile constants from the finished weeks — 2026-10-27

Pull window: 2026-10-27 → 2026-10-27 (no pull: `data/weeks/week_1.json`, the Sunday snapshots of weeks 1–2 back-filled from the records branch's 10-19 and 10-25 morning commits, and `report/accuracy.json`; no web search, no market pull).

**Method up front.** Owner 2026-10-27: build 3 of the five chosen ("let's build"). The fit **proposes only**: it writes a record and a table; the registry and the engine change on the owner's word, never by the script. Stated before the run: the shared weekly games swing (`TEAM_WEEK_SHOCK`) is measured as the excess of the variance, across team-weeks, of the mean actual÷expected ratio over the seven counting categories beyond what the simulator's own `team_week_model` predicts with no shock (the categories treated as independent under no shock, A2), expected totals from the lines and rosters snapshotted the Sunday before each week; the error is a bootstrap over team-weeks; a shock is reported only when the excess stands two SE clear of zero, otherwise "not detectable" (never a small number read off noise — a no-shock synthetic set came out slightly positive by chance and the red test caught it). The availability tiers are the pooled share of team games played per assumed tier from the accuracy card, binomial SE. A proposal needs four finished weeks. EVIDENCE marks what a run showed; INFERENCE what is derived.

## 1. What one week says (EVIDENCE, `report/fits/fit_week1.json`)

- **Shock:** 12 team-weeks; variance of the factor 0.0074, model term 0.0030, excess 0.00438 ± 0.00226 — not two SE clear of zero, so **no shock proposed**. INFERENCE: the point value would be √excess ≈ 0.066, near the live 0.06; one week cannot say more. Every team's factor but one sat below 1 (0.74–1.03): the league scored about 11% under the model's expectation in week 1, the same shortfall the week-1 audit measured in minutes and per-minute output.
- **Availability:** tier 0.88 measured 0.828 ± 0.013 (n 809, live outside 2 SE); tier 0.75 measured 0.573 ± 0.050 (n 96, live outside 2 SE); tier 0.00 measured 0.000 ± 0.000 (n 22, live inside 2 SE); tier 0.79 measured 0.800 ± 0.179 (n 5, live inside 2 SE). The two tiers with real samples both sit outside two SE of their live values, in the direction the audit found; the proposal line waits for week 4.
- Status: too few weeks to propose (1 of 4); the record says so rather than proposing.

## 2. What was built (EVIDENCE)

- `fit_constants.py` (new): the estimator, the pooling, the sample gate, an append-only `report/fits/fit_week<N>.json` and a regenerated `report/fits.md`. `test_fit_constants` (8, red first): a known 0.06 shock recovered within error at 1,200 and at 144 team-weeks, a zero shock reported as not detectable, the factor and model term by hand, the availability pooling by hand, the gate, the append-only record.
- `weekly_preview.snapshot`: the Sunday step now also keeps the league state and the day's status file (`state_week<N>.json`, `status_week<N>.json`), so each week is modelled on the rosters and tags true before it (`test_weekly_preview`, 2 new). `scoreboard_intake.py`: the Monday intake runs the fit after the accuracy card, non-fatal, named on its PASS line (`test_scoreboard_intake`, 1 new).
- **Back-fill (this PR, `report/accuracy/`):** week 1's state from the 10-19 morning (the draft-night rosters, as of 10-15 — the same rosters the week-1 ledger used) and its nearest prior status file (10-17); week 2's from the 10-25 morning. Named here because week 1 had no Sunday snapshot step yet.
- **A defect caught, same class as build 1's:** two pre-existing intake tests ran the new hook against the kit's real `report/fits/` and wrote a record mixing the fixture week with the real snapshots. Both tests now pass `--fits-dir`/`--snapshots-dir` to scratch, the stray was removed, and the suite leaves `report/fits` untouched (checked). Kit suite: every file OK.

## 3. Bounds

**Out of scope by design.** No constant, line, tag or roster changed; the registry is untouched. **In scope and unverified.** A2 (independence of the seven categories under no shock) makes the model term a floor; a positive within-team correlation at zero shock would be read as shock. With four or more weeks the per-category residual correlations can be reported beside the fit to test A2 — proposed for the week-4 record, not built. The week-1 snapshot predates the status feed's P/D tiers.

## 4. Next steps (owner decisions)

1. Merge this PR; the first proposal line appears on 2026-11-16 (after week 4's intake).
2. Build 5 (opponent-aware matchup), as ordered, once a few weeks of context and fits have accrued.

## Watchlist

- **Monday 2026-11-02:** `… fit through week 2, weeks [1, 2], 24 team-weeks; shock …; too few weeks to propose (2 of 4)`.
- **Sunday 2026-11-01:** `snapshot: … state_week3.json, status_week3.json` beside the lines.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| fit of the two fragile constants (build 3) | **BUILT**, proposes from week 4 | §1, §2 |
| intake tests leaking into report/ | **FIXED** (both), leak-checked | §2 |
| build 5 | **OPEN**, owner-ordered next | §4 |

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck e0722cf (this change's deck commit), checked today, the same page the 10/22 day report replayed. Its table stands, carried here verbatim from the day report.

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
