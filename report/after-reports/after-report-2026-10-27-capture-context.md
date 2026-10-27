# Capture now: game context on every box line, and the injury-tag outcomes ledger — 2026-10-27

Pull window: 2026-10-27 → 2026-10-27 (ESPN summaries re-fetched for the 52 regular-season games of 2026-10-20..26 to back-fill context; no Flaim or FantasyBot pull; no web search, no market pull).

**Method up front.** Owner 2026-10-27, from the options card: builds 1 and 4 of the five proposed ("capture now"), ahead of 2, 3 and 5. Stated before the run: context comes from ESPN's summary header (home/away, score, tip time), checked against the boxscore block's own home flag — a disagreement leaves home/away null and says so; days of rest are counted from the kit's own box records, so a team's first recorded game reads null, never a guess; the tag ledger grades a day's status file against that day's box record, a flagged player whose team had no game is "no game", not a miss. Capture only: no projection line, injury tag, roster or engine constant changes. EVIDENCE marks what a run showed.

## 1. What was built (EVIDENCE)

- `box_pull.py`: `game_context(summary)` and `rest_days`/`prior_game_dates`; every game record gains `context` {home, away, home_score, away_score, margin (home − away), tip_utc, neutral, note?}, every player row `rest_days`. `ACTUALS_DIR` names the records read for rest. Tests: `test_box_pull.GameContext` (5, red first; the 10-16 fixture had been trimmed to its stat tables, so a second fixture was trimmed from a live 10-25 summary, LAL at UTA 132-123, and the known margin −9 is asserted by hand).
- `tag_outcomes.py` (new): one line per flagged player per day in `data/status/tag_outcomes.jsonl` — played (minutes, minutes vs season mpg), sat, no game, or unresolved (no team on file); a day already in the ledger is refused. Tests: `test_tag_outcomes` (4, red first).
- `morning.py`: a non-fatal `tag outcomes` step for yesterday, after the box scores and before the status feed; the two exact-order tests gained the step (`test_morning.TagOutcomes`, 2, red first). Kit suite: every file OK; no stray writes.
- **Back-fill, staged on `season/daily` (not pushed):** the seven regular-season records 10-20..10-26 re-fetched for context and given rest days; each stripped of the new keys and compared to its pinned copy byte for byte before writing — no existing cell changed; no context notes on any of the 52 games. Rest-day spread by day (null / 1 / 2+): 10-20 84/0/0, 10-21 301/0/0, 10-22 28/0/27, 10-23 0/0/336, 10-24 0/150/69, 10-25 0/27/169, 10-26 0/69/182 — the opening nights null, then 1s and 2+s as the schedule thickens.

## 2. Bounds

**Out of scope by design.** Nothing reads the new fields yet: the week model, the season line and the accuracy card are unchanged; builds 2, 3 and 5 are what will read them. **In scope and unverified.** The tag ledger has no rows until tomorrow's morning (it needs a status file and the next day's box record; 10-26's status file exists and 10-27's record lands tomorrow, so the first graded day is 10-26, written 10-28). The status feed's P/D tiers were added after some early files, so early days carry fewer tiers.

## 3. Next steps (owner decisions)

1. Merge this PR and push the staged back-fill to `season/daily`.
2. Build 2 (minutes-trend candidate line), then 3 (fit the two fragile constants), then 5 (opponent-aware matchup) — each a separate PR on your word, as chosen.

## Watchlist

- **Tomorrow's morning (10-28):** `TAG OUTCOMES: PASS — 2026-10-27: N flagged player(s) … played/sat/no game`, and `data/actuals/2026-10-27.json` games carrying `context` with no `note`.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| game context on box lines (build 1) | **BUILT**, back-fill staged | §1 |
| injury-tag outcomes ledger (build 4) | **BUILT**, first rows 10-28 | §1, §2 |
| builds 2, 3, 5 | **OPEN**, owner-ordered next | §3 |

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
