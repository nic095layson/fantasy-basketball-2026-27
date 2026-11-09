# Week tab in plain language (owner pick 2026-11-09, "Build it as shown")

Pull window: 2026-11-09 → 2026-11-09 (no pull: wording only; kit main 25b9a9a, deck main 01483de).

**Method up front.** The owner asked for "ELI5 / plain language" on the Week tab: Scorecard (Brier card, Brier lead, Skill), Forecast accuracy (Bias, MAE, Rank), Availability and Forecasts. The before→after table was shown in chat and the owner picked "Build it as shown". The change is wording only. No figure, record or grader changes. The technical terms and the switch-rule codes (D-ML-1, D-RG-1) move into the ⓘ hovers. EVIDENCE marks what a run or read showed.

**Verdict: built and tested. The Week tab's visible text now uses the plain labels, the hovers keep the technical definitions, and every number renders unchanged.**

## 1. What changed (EVIDENCE: the diff, the suite)

| Before | After |
|---|---|
| Scorecard — the morning card's P(win) against the finals | How good were our daily win chances? |
| Brier card / Brier lead / skill | Our miss score / Scoreboard miss score / Beat the scoreboard by |
| Reliability: stated P / forecasts / mean P / hit rate | When we said X%, did it happen X% of the time? We said / Times / Average we said / It happened |
| Forecast accuracy — week by week | How close were our player projections? |
| preseason / in-season / minutes candidate | Draft-day line / Current line / Test line (minutes trend) |
| bias / MAE / rank | Too high / too low by / Typical miss / Got the order right? |
| Availability … tier / assumed / played / team games / share | Do players actually play as often as we assume? Health group (Healthy, Minor knock, Injury risk, Out) / We assume they play / Games played / team's games / Actually played |
| Forecasts: your P(win) / result / daily card Brier / lead-only Brier / league matchups scored | Did our weekly win chance hold up? Our pre-week win chance / Categories you won / Daily miss score: ours / scoreboard / Other matchups checked |
| Switch rules D-ML-1, D-RG-1 (visible) | "…only on your OK" (visible); the codes and exact rules in the hovers |

- `scripts/season_deck.py`: the Scorecard and Forecast accuracy cards (labels, notes, hovers, tier names).
- `scripts/test_season_deck.py`: new `PlainLanguageWeek`. The page uppercases headings, so the comparison ignores case; the test checks that the jargon is gone from the visible text, that it is still in the hovers, that the plain labels are shown, and that the numbers are unchanged. Four older tests that pinned the old wording were updated to the new labels, with their number checks unchanged.

Red first (EVIDENCE): `PlainLanguageWeek` failed on the old page (`'brier card' unexpectedly found` in the visible text) and passes now. Deck tests: 190 OK.

## 2. Bands quoted

This report quotes no title share. The standing structural band for any title figure is the season sweep of 2026-11-02 (deck e14cc42): **weekly_availability is FRAGILE:** -2.6 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.2 (healthy players play 0.95 of games) / +0.0 (healthy players play 0.80 of games), mean of the two seeds.

Runner impact: code-only. The deck step is unchanged; the page shows the new wording from the next build.

## 3. Bounds

- Out of scope by design: other tabs; the after-report and brief Markdown.
- In scope and unverified: the first live build after merge.
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
