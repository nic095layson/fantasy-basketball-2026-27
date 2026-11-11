# ESPN's return dates graded, and the date reworded as the earliest return (D-WS-2; owner card 2026-11-11)

Pull window: 2026-10-28 → 2026-11-11 (no pull: the 15 ESPN morning pins `data/status/espn_injuries_<date>.json`, the box scores `data/actuals` through 2026-11-10 and `data/season/pool_season.csv` at 6f40cf6 on season/daily, read only; kit main 6ad1f09).

**Method up front.** Order: the owner's check-in of 2026-10-28 (D-WS-2, "Check-in Nov 11"), then the card pick of 2026-11-11, "Keep 7 days, relabel, re-grade (Recommended)". The window and sample were stated to the owner before the run. One graded item is one player's first quoted return date while listed Out. "Back" is his first game with minutes on or after that morning. "On time" is within one day of the quote. Players in the kit's pool only. The grading scripts are in `report/after-reports/espn-return-2026-11-11/` (paths point at a records checkout). EVIDENCE marks what a run showed.

**Verdict: ESPN's date behaves as the earliest a player could be back. The 7-day line is unchanged. The brief, the IL-return section and the deck now say "earliest return". A re-grade on a month of data is scheduled for 2026-11-25.**

## 1. How good is the date (EVIDENCE: espn_grade2.py)

1,085 Out quotes with a date across 15 mornings, 140 players; 724 quote-days and 101 players in the kit's pool.

| first date quoted for a player | players | share |
|---|---|---|
| back within one day of it | 29 | 44% |
| back later (median 3 days late) | 16 | 24% |
| date passed by 2+ days, not back by 11-10 | 19 | 29% |
| back earlier | 2 | 3% |

- The last quote before a return was within one day for 44 of 47 returns: ESPN rolls the date forward, so it is reliable only when close.
- By lead time, first quotes of players who returned: 1 to 3 days out, 27 of 39 on time; 4 to 7 days out, 2 of 5.

## 2. The 7-day line (EVIDENCE: the same run; pins through 2026-11-03, so each has 7 days of box scores after it)

| first quote per player | players | back within 7 days |
|---|---|---|
| kept in the scan (date within 7 days) | 34 | 20 (59%) |
| set aside (date further out) | 28 | 2 (7%) |

By quote-day (319, repeated measures of the same players): a 3-day line classifies 82% right, 5 days 78%, 7 days 75%, 10 days 70%.

## 3. What changed

| where | before | after |
|---|---|---|
| brief, waiver pair flag | "ESPN expects back 2026-11-13" | "ESPN's earliest return 2026-11-13" |
| brief, set-aside list and streaming notes | "ESPN expects back …", "back …" | "ESPN's earliest return …" |
| IL-return section (brief and deck) | "ESPN dates of …", "Hali (2026-11-13, wk 4)" | "ESPN's earliest-return dates of …", "Hali (earliest 2026-11-13, wk 4)" |
| deck, free-agent status chip | "Out (ESPN), back 2026-10-23" | "Out (ESPN), earliest return 2026-10-23" |

`co_gm.SHORT_OUT_DAYS` stays 7; a test pins it.

## 4. Checks

- Red first: `EarliestReturnWording` (4 tests, 3 failing and 1 erroring before the change); the two existing tests that pinned the old words were updated to the new ones.
- Name matching checked: the 37 quoted players with no box line under a stricter name key are season-long absences or deep-bench players, not mismatches (15 of them are in the pool and counted as not back).
- Whole suite on this branch: 1061 tests OK (2 skipped).

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds (season sweep 2026-11-09, engine 01483de). This change touches no title figure.

## 5. Bounds

- Two weeks at the start of a season, 62 to 66 players per table: the direction is clear, the percentages are not settled.
- "Back" means he played minutes; a healthy player who sat for another reason counts as not back.
- The 19 players whose date passed are late by an unknown amount.
- INFERENCE: the IL-return blend's weight on "on time" (0.4) sits beside the 44% measured here; that weight was not fitted to this and is not changed.
- Out of scope by design: no change to the line, to any tier, or to the IL-return scenarios.

## 6. Next steps (owner decisions)

1. **Merge the wording (Recommended).** The re-grade on 2026-11-25 then brings the line itself back as options (keep 7, 5 or 3).
2. Hold the wording until the re-grade.

Runner impact: code-only. The brief and deck read differently in four places; no step, record or prompt changes.

## Fired

plan-gate (loaded for the grading and again for the wording; window and sample stated before the run; plan table shown before the first edit) · adversarial-verify (loaded before the assessment and before the push) · scope-fence: not loaded.

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
