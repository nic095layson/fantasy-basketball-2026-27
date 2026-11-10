# The decision card: pickup pairs in two worlds, under the band, and on this week (owner pick 2026-11-10, "Decision card + watchdog"; council ruling 4–1)

Pull window: 2026-11-10 → 2026-11-10 (no pull: report/briefs/brief_2026-11-10.json, report/il_return/il_return_2026-11-10.json, data/league_state.json at 6da518c and be859ea, data/season/pool_season.csv, data/status and data/source/flaim at be859ea on season/daily, read only; kit main a1c91ca, deck main 01483de).

**Method up front.** Order: the owner's 11-10 question ("gaps … outside my scope … that Claude/red team/council identifies"), then the card pick "Decision card + watchdog (Recommended)" (this report covers the decision card, proposals P1–P3; the watchdog has its own). Method parameters, stated to the owner before the build: the brief's top 3 pairs; the brief's own seasons and seeds (10,000 × 2); the return world is il_return.py's on-time scenario (ESPN dates, slip 0, the room rule); the band is the registry's declared variants of `weekly_availability`; the week effect counts the add from tomorrow, as the week card's pickup scan does. Tests were written first and seen failing. No projection line, injury tag, roster or engine constant changes; the brief (a graded record) is not touched. EVIDENCE marks what a run or a read showed; INFERENCE what is derived.

**Verdict: the morning run now writes a decision card after the week card, and the deck's Today tab draws it. The card shows each of the brief's top pairs in both worlds, says when their order differs, re-scores the top pair under the availability band, and puts this week's effect beside the season's. It adds about one minute to the run.**

## 1. Why (EVIDENCE: runs on the 11-10 morning records)

The brief scores a pair with every injured-list player absent for the season (owner 2026-10-20, D-IS-8). On 11-10 the owner's two candidate drops for John Collins ranked one way in that world and the other way with injured-list players back on ESPN's dates:

| add Collins, drop | never return (the brief's world) | return on time |
|---|---|---|
| Kris Dunn | +3.44 | +1.52 |
| Cameron Johnson | +1.57 | +2.52 |
| title share with no move | 12.3% | 21.9% |

The gap in the return world is 1.0 point, about 1.4 times the sampling error of a difference. The return world rests on the room rule (`il_return.ROOM_RULE_ON`, FRAGILE, +14.3 with the rule off) and on ESPN dates that had not been graded on 11-10.

## 2. What was built

| piece | what it does | evidence |
|---|---|---|
| `scripts/decision_card.py` (new) | Reads the day's brief, il_return record and week card. Scores each top pair in the return-on-time world; re-scores the top pair under each band variant in the never-return world; reads each pair's week effect. Writes `report/briefs/decision_card_<date>.json` and `.md`. A missing input leaves its own part out with a note. A hold day is a PASS with no pairs | tests `test_decision_card` (9) |
| `co_gm.run_league_sim(patch=…)` | Hands the simulator a constants patch (`league_sim --patch`, as the Monday sweep does); no patch, the command as before; the live constants are untouched | tests `test_daily_brief.SimPatch` |
| `week_matchup.pair_checks` | The week card scores the brief's own pairs on this week's matchup (`pair_checks`), morning and afternoon; a pair it cannot score says why | tests `test_week_matchup.PairChecks` |
| `morning.py` | New step "decision card" after "week matchup", non-fatal | test `test_morning.DecisionCardStep`; the pinned step list in `test_morning.Steps` gained the step |
| `season_deck.py` | Today tab card "Pickup check" from the record; no record or no pair, no card; the input is pinned in the deck record | tests `test_season_deck.DecisionCardDeck` (4) |

## 3. Behavioral check on the 11-10 records (EVIDENCE: runs in a scratch copy; nothing written to season/daily)

| check | result |
|---|---|
| Return-world base on the morning state | 21.95%, equal to il_return's on-time record (21.95) |
| The card on the afternoon state: Collins for Caruso | +3.4 never return · +3.2 return on time · −0.7 points this week |
| Julian Champagnie for Caruso | +1.5 · +1.3 · +1.4 points this week |
| Tobias Harris for Caruso | +1.4 · +1.1 · this week not shown (he is Out, so he is not in the day's free-agent pool) |
| Top pair under the band | holds in 4 of 4 settings (+2.7 to +3.8) |
| Run time | 52 seconds for 24 simulations (4 at a time) |

## 4. Checks

- Red first: `test_decision_card` (9), `SimPatch` (2), `PairChecks` (2), `DecisionCardStep` (1), `DecisionCardDeck` (4, of which 3 failed before the code).
- One existing test changed on purpose: the pinned morning step list now includes "decision card".
- The new pool guard (PR #250) stopped one of the new tests, which ran a simulation after another test had loaded a different pool. The test now loads the pool first.
- Whole suite: 948 tests OK (2 skipped).

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds (season sweep 2026-11-09, engine 01483de). The card changes no title figure.

## 5. Bounds

- Out of scope by design: the brief's ranking rule and its recommendation are unchanged, so the decision log still records the brief's top pair. Two-move packages are not scored. The opponent's side is not varied.
- In scope and unverified: the card was read in the test browser, not on a phone (did not check). The band is run for the top pair only, in the never-return world only.
- The return world's own uncertainty (the room rule, ESPN dates) is named on the card, not measured per pair.

## 6. Next steps (owner decisions)

1. **Merge, and read the card beside the brief (Recommended).** When the card says the order changes, the return-on-time column is the one to weigh, with its caveats.
2. After a few weeks of cards and the ESPN-date grading, decide whether the brief itself should rank by a blend of the two worlds (an engine-rule change; assessment first, on your go).

Runner impact: code-only. The morning run gains one non-fatal step whose line appears in the MORNING block and whose two files are in the WROTE list; the afternoon run's week card gains `pair_checks`. No prompt change.

## Fired

plan-gate (loaded; compact plan table shown before the first edit) · red-team (loaded; decision robustness, step 5) · council (loaded; ruling 4–1) · adversarial-verify (loaded before the proposal; re-run below before delivery).

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
