# Audit items F3, F5 and F6: team keys, the overnight title check, package rows (owner card 2026-11-10)

Pull window: 2026-11-09 → 2026-11-10 (no pull: brief_2026-11-09.json, brief_2026-11-10.json and morning_2026-11-09.json at be859ea on season/daily, and that checkout's git history, read only; one trial run of the title check wrote two files there, removed before any commit; kit main 04b8a32).

**Method up front.** Order: the owner's card pick "Audit items F3, F5, F6" of 2026-11-10. Tests were written first and seen failing for each item. Method choices stated to the owner before the build: a package's grade is the sum of its legs' gaps; the title check's threshold is the sampling error of the difference of two briefs (no new constant); team keys first, names only where a record carries no key. No projection line, roster, injury tag or engine constant changes. EVIDENCE marks what a run or a read showed.

**Verdict: three changes, each display or record keeping only. A two-move package is logged and graded as one recommendation; the morning run says when the title share moved by more than sampling error and names what changed between the two runs; the week card and the lineup log follow a team by its Yahoo key, so a rename no longer loses its earlier days.**

## 1. F6: package rows in the decision log

| before | after |
|---|---|
| Two moves advised together were two rows, each carrying the package's value (+1.38 on both rows of 2026-11-09) | `decision_log.py --session --package '[{"add":..,"drop":..},..]'` writes one row, kind `package`, with every leg in `moves` and the package's value once |
| A move matched one row | Each of the owner's moves joins the package by its own leg (`top`, `pkg2`, ...) |
| Each row graded alone | `decision_grade.grade` grades each leg on its own window and reports the package once: gap = the sum of the legs' gaps, against the same verdict line; any leg still pending keeps the whole package pending |

The two rows already on the ledger (S-2026-11-09-01 and -02) are not rewritten: the ledger is append-only. They will each be graded as a single pair.

## 2. F5: the overnight title check

`scripts/title_watch.py`, a non-fatal morning step after the decision log. It reads the day's brief and the newest earlier morning brief.

- Band: each share is the mean of two runs of n seasons, error 1.96·sqrt(p(1−p)/(2n)) as the brief prints it; the difference of two shares has error sqrt(e_today² + e_before²). At 12% and 18% on 10,000 seasons that is ±0.7.
- Inside the band: one line, nothing named.
- Outside the band: it names the pull-request merges that reached the checkout since the earlier run (git history from that run's recorded time) and every team's roster change on the day's brief (the owner's team marked).

EVIDENCE (trial on season/daily be859ea, files removed afterwards): "title 12.3% (was 18.1% on 2026-11-09), -5.8 against a band of ±0.7: MOVED", then six merges (#244 to #249) and six teams' moves, among them "#246: ... auto-row players simulated" and "SNOWTIME WHITE WALKERS: ... off IL Luka Doncic". The hand trace of this morning found those two as the largest causes (−2.69 and −2.64) plus a pool change (−0.42).

## 3. F3: team keys

| script | before | after |
|---|---|---|
| `week_matchup.py`, earlier days' lineups | keyed by Yahoo team name: a team renamed mid-week lost the days pinned under its old name | keyed by team key (`team_key`, `team_lineups`); by name only when the pull has no rosters |
| `week_matchup.py`, adds counter | the owner's key found by the league-state name: a stale name gave no key | found through `team_key` (state name, else the roster holding most of the team's players) |
| `lineup_log.py`, locked lineup | matched by name in each pin | the key is read from the newest pin carrying the name, then every pin is read by key |
| `league_live.py` | unchanged: its input (the FantasyBot transcription) carries no team key |
| `scoreboard_intake.py` | unchanged: its input is a hand-typed CSV of team names with no key |

## 4. Checks

- Red first: `PackageRows`, `PackageGrade` (8 errors before the change), `test_title_watch` (the module did not exist), `TeamKeys`, `LockedLineupByKey` (5 failing before the change).
- An existing test pins the decision log directly after the brief; the title check was placed after the decision log to keep it.
- Whole suite on this branch: 1021 tests OK (2 skipped).

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds (season sweep 2026-11-09, engine 01483de). Nothing here changes a title figure.

## 5. Bounds

- Out of scope by design: the title check names what changed and does not split the move between the causes; that takes simulator runs, one change at a time. It does not read the pool or the status feed, so a pool-only change shows as "unexplained, check the pool and the status feed".
- Out of scope by design: the package verdict uses the same ±line as a single pair. Whether a two-leg sum should face a wider line is an owner decision, not taken here.
- In scope and unverified: the title check inside a real Runner morning (did not check: the next run is 2026-11-11). Its merge list depends on the earlier morning record carrying `ran_at_utc`; without it the line says "kit merges not readable from git history".
- In scope and unverified: no team has been renamed since the 2026-11-09 case, so F3 rests on its tests.
- INFERENCE: on the trial, #249 appears in the merge list because the trial ran this afternoon; the morning step would have run before that merge.

## 6. Next steps (owner decisions)

1. **Merge (Recommended).** The title check starts on the next morning run; package rows are used the next time two moves are advised together.
2. Merge, and also show the title-watch line on the deck's Today tab (a second, small build).
3. Hold: keep the changes on the branch.

Runner impact: code-only. The morning run gains one non-fatal step; no prompt changes.

## Fired

plan-gate (loaded after the compaction; compact plan table shown before the first edit) · adversarial-verify (loaded before delivery) · scope-fence: not loaded.

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
