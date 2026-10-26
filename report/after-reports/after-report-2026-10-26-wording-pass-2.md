# Wording pass on Board, Movers, Week and League — 2026-10-26

Pull window: 2026-10-26 → 2026-10-26 (no new pull: the measurement uses the deck built from the records branch `season/daily` at 1c24b0d with today's league record; no web search, no market pull).

**Method up front.** Owner 2026-10-26, from the options card: "Build all 13 lines (Recommended)" over "fix the two wrong lines only" and "build all, keep Week as is". The assessment measured every visible note on the five tabs in a browser (innerText, tables excluded); the Trade Analyzer's text is player labels and one 10-word note, so it was left alone. Twelve lines change; the thirteenth the card counted (the standings check line, 14 words) was already short and stays — the label's "13" was one too many. EVIDENCE marks what a run showed; INFERENCE what is derived.

## 1. What changed (EVIDENCE)

| tab | before (words) | after (visible) | what moved to the ⓘ hover |
|---|---|---|---|
| Board | held-off list (38) | "Season lines blended with games so far (287 players) · 12 held off the board" (16) | the twelve names |
| Movers | unpooled list (215) | "103 players with games aren't in the pool" (9) | the 103 names |
| Movers | season-line method (44) | "Season line = preseason line blended with games played (287 players)" (12) | the per-category prior games |
| Movers | box-score window (21) | 17 words, "6 days" and "rates" dropped | — |
| Week | FantasyBot counts (17) | 11 | the full sentence |
| Week | ledger line (19) | "Recorded before each week, never rewritten; results from Monday's scoreboard intake (Yahoo's finals)." (13) | — (**corrected**) |
| Week | Brier and skill (59) | 20 | the full definition |
| Week | reliability (17) | 10 | the full sentence |
| League | standings note (38) | 19 | the full definition |
| League | power and luck (50) | 17 | the full definition |
| League | sort and badge (39) | 21 (the week status stays visible) | percentages, turnover sort, badge |
| League | rebuilt week (30) | "Week 1 totals rebuilt from box scores; score from the week record" (13) | how the totals are rebuilt (**corrected**) |

**Measured on the 2026-10-26 deck (browser, notes only):** Board 51 → 29, Movers 280 → 38, Week 112 → 54, League 171 → 84; **614 → 205** words. Page errors 0 before and after.

**Two corrections.** The Week ledger line said results land "when you paste the scoreboard"; since 2026-10-24 they come from Monday's scoreboard intake of Yahoo's pull (`scoreboard_intake.py`, which also grades the scorecard). The League rebuild note said "no Yahoo result for those weeks"; since #202 a rebuilt week takes its score from `data/weeks/week_N.json`, and the note now says which (and stays red only when no week record scored it).

**Tests, red first.** `test_season_deck.WordingPassTwo` (4: one per tab — the long text gone from view, kept in a hover, the short line shown, the wrong phrases nowhere); all four failed before the edit. Full `test_season_deck`: OK.

## 2. Bounds

**Out of scope by design.** No figure, threshold or record changes; the Trade Analyzer is untouched. **In scope and unverified.** Hovers need a pointer or a tap-and-hold on a phone (the ⓘ carries `tabindex` and `aria-label`, as on Today and Free Agents).

## Watchlist

- **Tomorrow's deck:** the four tabs carry the short lines; a hover shows each definition.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| Week ledger line "paste the scoreboard" | **FIXED** | §1 |
| League rebuild note "no Yahoo result" | **FIXED** | §1 |
| wording pass, Board/Movers/Week/League | **DONE**, 614 → 205 | §1 |
| brief header "lines v69" | **OPEN**, owner decision (from #201) | — |

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
