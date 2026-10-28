# The 3 PM run refreshes the Season Deck — 2026-10-28

Pull window: 2026-10-28 → 2026-10-28 (no pull for the kit: the 10-28 afternoon records on season/daily at 2f80fb0, read only).

**Method up front.** Owner 2026-10-28 asked whether the afternoon run updates the Season Tool with roster moves and injury updates. The assessment found that it does not: the afternoon prompt reads "no deck build or publish". The owner then picked "Rebuild, flag morning parts (Recommended)".

EVIDENCE marks what a run showed.

## 1. What was built (EVIDENCE)

| | before | after |
|---|---|---|
| 3 PM run | rosters + status saved, page untouched | also runs `season_deck.py --phase pm` and republishes |
| page file | `deck_<date>.html` (5 AM) | 5 AM file kept; `deck_<date>_pm.html` written beside it |
| Today tab | no time label | the afternoon page says rosters and status are 3 PM's, and the lineup, waiver pairs and odds are 5 AM's |
| a player pooled after 5 AM | n/a | the morning build still halts; the afternoon build names him "added since the 5 AM board" |

**Red first.** 7 tests in `test_season_deck.AfternoonRefresh`:
- 3 errored before the phase existed;
- 2 more errored before the off-board handling;
- the 2 morning guards passed throughout;
- all 7 pass now.

Kit suite: 693 tests OK (2 skipped).

**A real afternoon build on today's records** (season/daily 2f80fb0) gave `SEASON DECK: PASS — 2026-10-28 (afternoon refresh)`: 7 tabs, 0 page errors. Its note names Mo Bamba, pooled after the 5 AM board.

**Surprise found on the way.** The first real build failed: "rostered player(s) with no season-board or held row: ['Mo Bamba']". The deck takes its rows from the 5 AM season board, and Bamba was pooled after it. Rebuilding the board in the afternoon would have overwritten morning files that the morning deck record fingerprints. So the afternoon page names such a player instead, and the morning rule stands.

## 2. Bounds

**Out of scope by design.** The afternoon refresh does not rerun the brief or its title simulations; the page says so.

**In scope and unverified.** The first live afternoon refresh is on 10-29, after the prompt paste.

Runner impact: prompt edit — the afternoon prompt (pm_v3, 6,231 bytes) gains the deck-refresh step; the paste is the owner's (RUNNER-ASK-v6), and the read-back is pending.

## Watchlist

- **10-29 afternoon report:** a SEASON DECK line "(afternoon refresh)" and the publish result.
- **The live page after 3 PM:** shows the afternoon note.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| afternoon deck refresh | **BUILT** (kit) | §1 |
| afternoon prompt edit | **DRAFTED**, paste and read-back pending | Runner impact line |

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
