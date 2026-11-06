# Afternoon page: a morning line whose player has left the roster says so (owner 2026-11-06, "Please build it")

Pull window: 2026-11-05 → 2026-11-05 (no pull: the records on season/daily read only at 1e6652a — brief_2026-11-05.json, week_matchup_2026-11-05.json, league_state.json (PM), deck_2026-11-05_pm.html; kit main 02c26d6, deck main e14cc42).

**Method up front.** Owner's question: "why my Today page still shows Matkovic on my roster?" Assessment from the records: the afternoon page's roster already had Ziaire Williams and not Matković (PM league state), but the Today tab's today-rows, lineup, start/sit slots and this-week drop names are the 5 AM brief's and week-matchup record's, which named Matković (the move came at 17:53Z) — the owner's 2026-10-28 "Rebuild, flag morning parts" design, the runner's Finding 4 of 11-05, and the owner's B1 pick. The owner then chose the runner's option 2: mark, do not recompute. Method parameters, stated before the build: on an afternoon build only, `gone` = names the morning brief and week-matchup record put on the owner's side (today rows, lineup, bench, start/sit slots and moves, the drop side of this week's adds) that the afternoon roster lacks, matched by the kit's accent-and-punctuation name fold (Matkovic = Matković); the page appends a "no longer on your roster" chip to those lines and lists the names in the afternoon note. Nothing is recomputed; the morning page is unchanged. EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: built and tested (suite 802 OK, 2 pre-existing skips); on an afternoon build the chip appears on each morning line of a player who has left the roster and the afternoon note names him; the morning build carries nothing new. Nothing merged.**

## 1. What was built (EVIDENCE: the diff, the suites)

- `scripts/season_deck.py` — `gone_since_morning(brief, week_matchup, roster)`; `build()` adds `refresh.gone` on a pm build; JS `goneChip(name)` on: the Lineup rows, the Today's games rows, the start/sit grid (start and sit), the Out-today line, the "for <drop>" line of This week's adds; the afternoon note gains "No longer on your roster since the 5 AM run (their morning lines are marked): …". CSS `.chip.warn.gone`.
- Tests: `AfternoonRefresh` — a pm build whose roster lost Bench Guy marks his today row and lineup row and names him in the note (3 occurrences), the morning build none; `gone_since_morning` folds accents (Matković on the roster clears Matkovic from the brief) and reads every morning list; empty inputs give an empty list. Whole suite 802 OK.

## 2. Re-runs on the records (EVIDENCE: records read, no scratch build)

`brief_2026-11-05.json`: today row `["Karlo Matkovic","NOP",null,…]`, `waiver_top[*].drop` = Karlo Matkovic ×3, `streaming_vs` Matkovic; `week_matchup_2026-11-05.json` `lineup_today.slots` carries Karlo Matkovic (F); PM `league_state.json` seat 10: Ziaire Williams on, Matković off; the 11-05 pm deck's roster: Ziaire on, Matković off. INFERENCE: with this build the 11-05 pm page would mark the Matkovic today row and the start/sit slot line, and name him in the note; the waiver pairs and streaming line of the brief Markdown are not on the deck (the deck's "This week's adds" rows drop Kris Dunn), so they get no chip because they are not rendered.

## 3. Bands quoted

No title share is quoted as a new figure in this report. The standing structural band for any title figure is the season sweep of 2026-11-02 (deck e14cc42): **weekly_availability is FRAGILE:** -2.6 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.2 (healthy players play 0.95 of games) / +0.0 (healthy players play 0.80 of games), mean of the two seeds.

Runner impact: code-only. The 3 PM run's deck step reads the morning records and the live state as it does now; no step or prompt change.

## 4. Bounds and open items

- Out of scope by design: recomputing the lineup, pairs or odds in the afternoon (the owner's 10-28 and 11-05 picks stand); the brief Markdown's own lines.
- In scope and unverified: the first live afternoon run after a same-day roster move.

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
