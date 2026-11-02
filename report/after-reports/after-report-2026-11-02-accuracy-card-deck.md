# The weekly accuracy card on the Season Deck's Week tab (owner pick 2026-10-27 "after week 2 grades"; built 2026-11-02)

Pull window: 2026-11-02 → 2026-11-02 (no pull: the records on season/daily 463e84f read only; kit main e19970c, deck main e14cc42).

**Method up front.** The one-shot task of 10-27 fired at 20:00Z: `report/accuracy.json` holds weeks 1 and 2 (EVIDENCE: the record's `weeks` keys). The deck's Week tab carried the daily-card Brier scorecard but not the weekly card (EVIDENCE: 0 "MAE" hits in `deck_2026-11-02.html`; `season_deck.py` never read `accuracy.json`). This session had said the card was already on the deck; that was wrong and is corrected here. The owner picked "Build now". Plan-gate's criteria were stated before the build; adversarial-verify graded the result against them. EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: the Week tab now renders the weekly accuracy card from `accuracy.json`, read-only, beside the daily-card scorecard; 3 red-first tests green, the deck suite green (167), both real builds PASS with 0 page errors; nothing merged.**

## 1. What was built (EVIDENCE: the diff, the suite)

| change | where | test |
|---|---|---|
| `accuracy=report/accuracy.json` is an optional deck input, pinned in the record (15 inputs today, sha256 recorded; absent reads as absent, never hashed) | `season_deck.default_paths`, `build` | `AccuracyCard.test_record_pins_the_accuracy_input` |
| The card: three tables under "Forecast accuracy — week by week": player lines (preseason, in-season, minutes candidate: projected / actual PTS, bias, MAE, rank correlation; a week without a snapshot column reads "no snapshot"), availability by tier (assumed vs played share, a share more than 0.05 under the assumption in the negative colour), forecasts (your P(win), result, daily-card Brier vs the lead-only Brier, league matchups scored). The two switch rules D-ML-1 and D-RG-1 are quoted as pre-committed, not decided | the Week pane, after the scorecard block | `AccuracyCard.test_two_graded_weeks_render_lines_availability_and_forecasts` (browser read-back, 0 errors, 0 overflow) |
| Zero state: "No week graded yet — the card fills at Monday's intake." | same | `AccuracyCard.test_default_paths_name_the_record_and_an_absent_one_builds_with_a_pending_line` |

Nothing on the deck computes accuracy; every figure is the Monday intake's record (`accuracy_week.py`). No engine, constant, line or roster changed.

## 2. Re-runs on the 11-02 records (EVIDENCE: two builds in scratch)

| build | result |
|---|---|
| with `accuracy.json` (weeks 1 and 2) | SEASON DECK: PASS, 7 panes, 315 board rows, 15 inputs pinned, 0 page errors; the browser read-back shows week 1 "no snapshot" in the in-season and minutes columns, week 2 preseason 13.14 / 11.88, 10.6%, 3.60, 0.77; in-season 8.7%, 3.46, 0.79; minutes candidate 7.6%, 3.34, 0.81; availability 0.88 tier 727 / 918 = 0.79 |
| without `accuracy.json` | SEASON DECK: PASS, 15 inputs (accuracy absent), zero state rendered, 0 page errors |

The figures match `report/accuracy.md` line for line (EVIDENCE: the markdown card of the same record).

## 3. Bands quoted

No title share is quoted in this report. The standing structural band for any title figure on the deck is the season sweep of 2026-11-02 (deck e14cc42): **weekly_availability is FRAGILE:** -2.6 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.2 (healthy players play 0.95 of games) / +0.0 (healthy players play 0.80 of games), mean of the two seeds, as the 11-02 brief quotes it from the morning run's sweep record (`report/after-reports/redteam-2026-11-02-season/sweep.json` on season/daily).

Runner impact: none. The morning run's "season deck" step picks the card up from `report/accuracy.json` on the next build after merge; no new step, no prompt change.

## 4. Bounds and open items

- Out of scope by design: the per-category line tables (REB, AST and the rest stay in the record and the markdown card; the deck shows PTS, the card's headline); the league-matchup Brier columns (0 scored weeks so far, the ledgers began 10-27).
- In scope and unverified: the first live render on the records branch (the 11-03 morning run after merge); the 10-27 one-shot task has fired and is closed by this build.

## Watchlist

- 2026-11-03 morning (after merge): the Week tab shows the card from the records branch's `accuracy.json`; the deck record pins 15 inputs.
- 2026-11-09 Monday: week 3 lands as the third row with all three line columns; the D-ML-1 count starts reading.

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
