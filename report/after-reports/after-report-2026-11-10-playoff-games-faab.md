# Playoff games on the Board, and the league's winning FAAB bids (owner picks 2026-11-10, "Playoff games column" and "FAAB bid history table")

Pull window: 2026-11-10 → 2026-11-10 (no pull: report/schedule/games-2026-27.csv, data/league_schedule.json, data/managers/transactions.json and data/source/flaim/pull_2026-11-10.json at be859ea on season/daily, read only; kit main 04b8a32, deck main 01483de).

**Method up front.** Order: the owner's card of 2026-11-10 after the P6 and P8 investigation, picks "Playoff games column (Recommended)" and "FAAB bid history table". Method parameters, stated before the build: the playoff weeks are the league schedule's `playoff_weeks` (18, 19, 20); games are counted from the season's game file by its `yahoo_week`; winning bids are the transaction record's `faab_bid` values as Yahoo gives them. Both are display only. Tests were written first and seen failing. No projection line, injury tag, roster or engine constant changes. EVIDENCE marks what a run or a read showed.

**Verdict: the Board tab gains a sortable "PO g" column (each player's NBA team's games in the fantasy playoff weeks), and the League tab gains a card of the league's winning FAAB bids. Neither feeds a number anywhere else.**

## 1. Playoff games (EVIDENCE: the engine source and a run on the game file)

The simulator plays every week, playoffs included, at the same games per player (`arena.py`: g = 3.5 × availability). The real schedule differs by team over weeks 18–20 (2027-03-01 to 2027-03-21):

| team | games in weeks 18 / 19 / 20 | total |
|---|---|---|
| NOP | 4 / 4 / 4 | 12 |
| BKN | 4 / 3 / 4 | 11 |
| DEN | 3 / 4 / 4 | 11 |
| PHX | 3 / 4 / 4 | 11 |
| CHA | 2 / 4 / 3 | 9 |
| MIL | 3 / 3 / 3 | 9 |

All 30 teams are counted; the range is 9 to 12.

| piece | what it does | evidence |
|---|---|---|
| `season_deck.playoff_games` | Counts each NBA team's games in the playoff weeks, in pool team codes; None when a file is absent | tests `test_season_deck.PlayoffGamesColumn` (3) |
| Board tab | Column "PO g", sortable; the hover gives the three weeks' counts and says the simulator does not use them. A team with no listed game shows a dash, never a zero. No files, no column | same |

Scope kept by an earlier ruling: the Free Agents tab is unchanged. The owner's 2026-11-06 instruction made that list "season z only" with no extra notes on its rows; the Board's "free agents only" filter gives the same view with the column.

## 2. Winning FAAB bids (EVIDENCE: a read of the transaction record)

| piece | what it does | evidence |
|---|---|---|
| `season_deck.faab_bids` | The transaction record's adds that carry a bid, newest first, the team named from the day's pull (its key's number when the pull does not name it); count, low, median, high | tests `test_season_deck.FaabBids` (2) |
| League tab | Card "FAAB: winning bids" with the table; the owner's rows are marked. No record or no bid, no card | same |

On the 11-10 record: 7 winning bids, low $10, median $15, high $100. Yahoo shows winning bids only, so losing bids are not on record. Seven bids are too few to advise a bid; the card says it is a record, not advice.

## 3. Checks

- Red first: 5 new tests. Two test fixtures of mine were wrong and were corrected before the build was called green: the pull fixture needed an available-player list, and the League tab draws its cards only when a league record exists.
- Whole suite on this branch: 1,001 tests OK (2 skipped).

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds (season sweep 2026-11-09, engine 01483de). Nothing here touches a title figure.

## 4. Bounds

- Out of scope by design: the simulator still plays flat games in the playoffs; using real playoff games there is an engine change. No bid advice.
- In scope and unverified: the column was read in the test browser, not on a phone (did not check). The game file's playoff-week games were not checked against a second schedule source (did not check).
- A found item, not changed: the deck build raises when a pull exists with no available-player list and there is no ESPN feed for the day (`co_gm.fa_status`). The runs always have one of the two, so it has not fired.

## 5. Next steps (owner decisions)

1. **Merge (Recommended).** Both show on the deck from the next run.
2. Later, with a season of bids on record: a bid-range note per pickup (assessment first, on your go).
3. Real playoff games in the title simulator (an engine change; assessment with its effect on the title share first, on your go).

Runner impact: code-only. The deck reads three more optional inputs (the game file, the league schedule, the transaction record); no prompt change.

## Fired

plan-gate (loaded; compact plan table shown before the first edit) · adversarial-verify (loaded this turn). scope-fence was not loaded; the Free Agents tab was left alone on the owner's 2026-11-06 ruling, named in section 1.

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
