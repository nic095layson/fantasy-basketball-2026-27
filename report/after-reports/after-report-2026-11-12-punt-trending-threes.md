# Punt-aware board view, trending-up free agents, and a threes-split candidate line (owner's card, 2026-11-12)

Pull window: 2026-10-17 → 2026-11-12 (one fetch: Basketball-Reference's 2025-26 season totals table, parsed to `data/reference/threes_prior_2025-26.csv` with its manifest; else no pull: the kit's files at main 797df7f and the records at db51bfb on season/daily, read only).

**Method up front.** The owner sent a list of fifteen valuation formulas and asked which the kit already has, which are useful, and how they would be used. The assessment (read from the code) found nine present, four absent and two partial, and put four options on a card. He picked three: "Punt-aware build view", "Trending-up screen", "Split threes into attempts and %". Parameters, stated to him before the build: (1) a category switched off leaves every player's sum, with the board's own availability rule, and a "My build" button switches off the categories where his team ranks 10th or worse of 12; (2) last 3 games against the games before them from 4 games played, flagged at minutes up 6 or usage up 4 points, usage = (FGA + 0.44 FTA + TOV) as a share of the team's while he is on the floor; (3) prior percentage = the player's 2025-26 three-point percentage, attempts settling at the blend's own threes prior (9.5 games) and the percentage at 750 attempts, the owner-supplied figure. EVIDENCE marks what a run showed; INFERENCE what is derived.

**Verdict: all three are built and run on today's records. The Board has nine category chips and a fit column that appears when one is off; the Free Agents tab has a Trending Up card; a third line (`pool_season_3s.csv`) is written each morning, snapshotted on Sundays and graded on Mondays on threes made. Nothing changes the board's order, the live line, the brief or the simulator.**

Runner impact: code-only — the morning run gains one non-fatal step, "threes line" (23 steps, was 22); `form_board.py` adds usage fields to its record; the deck draws one new control row and one new card. No prompt edit.

## 1. Two changes of plan, both told to the owner before the work that used them

- **The prior's source.** The plan named the 2025-26 game logs on file. They carry threes made and no attempts, so they cannot give a percentage. The prior comes instead from Basketball-Reference's 2025-26 season totals (one fetch, 582 players, checksum in the manifest; the first row per player, which is the combined row for the 71 who were traded).
- **The Trade Analyzer.** The card's wording included it. Its net figure and tier verdict rest on all nine categories and are covered by existing tests; the punt chips are on the Board only. A trade read with categories off is done by sorting the Board by fit. Left for the owner to ask for.

One rule was tightened after the first real run: a free agent whose usage is up while his minutes are down by the threshold is left off the list (Jarace Walker read 24.0 to 12.3 minutes with usage up; that is not a rise).

## 2. Punt-aware view

`scripts/season_deck.py`: chips `#bd-punt` (one per category), `#bd-mybuild`, `#bd-allcats`; a `fit` column drawn only when a category is off, value = the sum of the categories still on, times GP/82 + (1 − GP/82) × `STREAM_R` when that sum is positive (the board's z adj rule, constant read from the board's module). `PUNT_WEAK_FROM = 3` (display, hand-set).

EVIDENCE, today's records with the owner's weak categories off (assists and steals, his 12th and 11th of 12):

| player | board # | z adj | fit |
|---|---|---|---|
| Kawhi Leonard | 5 | 4.88 | 2.93 |
| Kevin Durant | 29 | 1.92 | 2.53 |
| Kyrie Irving | 15 | 2.97 | 2.17 |
| John Collins | 81 | −0.39 | 1.30 |
| Miles Bridges | 50 | 0.77 | 1.28 |
| Tyrese Haliburton | 11 | 4.11 | 1.06 |
| Derrick White | 46 | 0.95 | −0.37 |

INFERENCE: his rank in assists is read with Haliburton on the IL, where he counts zero. When Haliburton is active the "My build" button may no longer switch assists off; the view follows the roster as it stands.

## 3. Trending-up screen

`scripts/form_board.py`: per game, the team's possessions and minutes over everyone who played; `usage()` pooled over a set of games; `usg`, `last3_usg`, `prior_usg`, `usg_trend` on every row; `USG_TREND_MIN = 4.0` (display, hand-set, like `TREND_MIN`). `scripts/season_deck.py`: card `#fa-trending` on the Free Agents tab, free agents only, by minutes gained.

EVIDENCE, today: 99 free agents in the record; the card's rule lists those up in minutes, or up in usage without a fall in minutes. Examples: Kevin Huerter 20.4 → 29.3 minutes and 14.8% → 18.8% usage; Bennett Stirtz 16.8 → 24.0 and 13.8% → 20.4%; Dylan Cardwell 13.0 → 20.7 and 9.2% → 16.5% (4 games).

## 4. Threes-split candidate

`scripts/threes_line.py` (new), `PCT_PRIOR_ATT = 750.0` and `MIN_PRIOR_ATT = 100`, both registered uncalibrated under D-TS-1. Only `tpm` changes; points and percentages are the live line's. `weekly_preview.snapshot` copies `pool_season_3s.csv` to `lines_week<N>_3s.csv`; `accuracy_week.py` grades it as `candidate_threes` and the card prints a threes table with the switch rule.

EVIDENCE, today's records: 342 players, 233 split, 109 unsplit (no 2025-26 row with 100+ attempts, or no preseason threes: rookies, last season's long absences, non-shooters). Candidate above the live line by 0.2 or more for 30, below for 16.

| player | live | candidate | this season | prior % |
|---|---|---|---|---|
| Brandon Miller | 3.0 | 3.55 | — | — |
| Grayson Allen | 3.1 | 2.67 | — | — |
| Derrick White | 2.3 | 2.29 | 21 of 63 | .327 |
| Julian Champagnie | 2.6 | 2.39 | 34 of 78 | .381 |
| Ty Jerome | 2.5 | 2.67 | 26 of 71 | .420 |

INFERENCE: for Derrick White the two lines agree, because his 2025-26 percentage (.327) and this season's (.333) are the same; the split does not predict a recovery for him.

## 5. Checks

| check | result |
|---|---|
| `test_season_deck.PuntView` (3), hand-worked sums | OK; the chip test first failed on a real fault (the chips rendered as text), fixed |
| `test_form_board.Usage` (4), hand-worked | OK; written after the code, so not seen failing first |
| `test_season_deck.TrendingUp` (2) | OK |
| `test_threes_line` (9), hand-worked | OK; written after the code, so not seen failing first |
| `test_weekly_preview` snapshot, `test_accuracy_week.ThreesCandidate` (2), `test_morning` step list | OK |
| Constants registry | 51 registered = 51 live (was 49) |
| All three on the 11-12 records in a scratch copy of season/daily | FORM BOARD, THREES LINE, SEASON DECK each PASS; page: 0 errors |
| Full suite | 1,169 tests; the first run had 7 errors, all from this change (a new test helper reused the name of an existing one, `board_dom`); renamed, and the suite in `gates.json` is the re-run |
| Gates | in `gates.json` |

A fault caught before anything was written to the kit: the first parse of the totals table dropped eight players whose cells are printed in bold as league leaders (Julian Champagnie among them). The parser now strips markup; 582 rows, none unparsed.

## 6. Bounds

- Out of scope by design: the scarcity multiplier and position-based replacement value (assessed, not recommended); playoff-games weighting (a column today; worth applying near the trade deadline); the Trade Analyzer's verdict.
- In scope and unverified: the threes candidate has no graded week yet; its first snapshot is Sunday 11-15 and its first grade Monday 11-23. The 750-attempt figure is the owner's, with no source; the grade is the test of it.
- The candidate changes threes only. A full version would move points and FG% with it; not built.

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds. No title figure is computed in this change; the last one on record is the 11-11 morning's 16.06%, 10,000 seasons on two seeds.

## 7. Next steps (owner decisions)

1. Merge on your word; the next morning run writes the candidate and the next deck build shows the chips and the card.
2. Whether the punt chips should also drive the Trade Analyzer.
3. D-TS-1: the threes candidate replaces nothing until it beats the in-season line on threes made in 3 of 4 consecutive graded weeks, and then only on your word.
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
