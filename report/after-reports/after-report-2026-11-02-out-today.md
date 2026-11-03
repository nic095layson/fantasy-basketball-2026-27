# Out-today banner on the Today tab, with the best bench swap for this week's matchup (owner requests 2026-11-02 and 2026-11-03)

Pull window: 2026-11-02 → 2026-11-02 (no pull: the records on season/daily 00e71b6 read only, the 3 PM run's status file among them; kit main 2831565, deck main e14cc42).

**Method up front.** The owner saw Kyrie Irving Out on the afternoon page and asked for a flag at the top of the Today tab with the best bench player for his spot (11-02), then asked that the pick follow the matchup's categorical needs (11-03). The 3 PM status file reads Kyrie `O`, availability 0.0; the 5 AM file read `Q`, 0.5 (EVIDENCE: `status_2026-11-02_pm.json`, `status_2026-11-02.json`). Method stated to the owner before each run: first the brief's daily-fill value (season-board z total), then, on the second request, the change in this week's expected categories won against the opponent from week_matchup's existing category model (the Week card's normal approximation on projected finals, the model the 3 PM lineup alerts already use), with season value only as a labelled fallback. EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: the Today tab now opens with an "Out today" card naming each starter Out in the live status and the bench player who adds the most expected categories this week, with the categories he helps; on the 11-02 afternoon records it reads "Kyrie Irving (UTIL) is Out today — start PJ Washington at UTIL: +0.09 expected categories this week (helps REB, BLK, ST)"; the season-value rule had named Julian Champagnie; existing week_matchup figures are unchanged; nothing merged.**

## 1. What was built (EVIDENCE: the diff, the suites)

| change | where | test |
|---|---|---|
| `today_swap_cats`: today's swap split by category (change in P(win) per category this week); `today_swap_value` is now its sum, same model | `week_matchup.py` | `LineupToday.test_the_per_category_split_sums_to_the_week_value_of_the_swap` (sum equal to 12 places) |
| `replacement_table`: for each starter with a game today, every bench player with a game who is not Out and fits his Yahoo slot, ranked by that change, never by season value; written each morning as `lineup_today.replacements` | `week_matchup.py` | `LineupToday.test_replacements_rank_by_this_weeks_categories_not_season_value` |
| The owner's late-week case (11-03: "by Friday, if I am significantly up in Rebounds, but need Assists, this should suggest the corresponding player"): already how the model works, since to-date totals are fixed and only today's games vary, so a locked category's chance barely moves and a close one moves most; pinned by a test, not new code | `week_matchup.py` (no change) | `LineupToday.test_late_in_the_week_a_locked_category_yields_to_the_close_one` (REB won by 50, AST 2 behind: the passer outranks a higher-season-value rebounder; green on the built code, and a season-value ranking would fail it) |
| `out_today`: a starter (live Yahoo slot) with a game today and availability 0 in the build's status file (3 PM in the afternoon build) gets the top row of that table still on the bench, with its gain, the categories it helps and the next two; no row for him in that slot: season value, labelled; nobody fits: the re-filled lineup | `season_deck.py` | `OutToday` (4 tests, browser read-back, 0 errors) |
| The card renders first on the Today tab, with the status file and the ranking basis named | `season_deck.py` | same |

Read-only: the card names a swap; it changes no lineup, roster, line, tag or constant.

## 2. Re-runs on the 11-02 records (EVIDENCE: scratch runs, records tree restored)

| check | result |
|---|---|
| week_matchup, old vs new code, same inputs | lineup moves, category chances and expected categories (4.9718) identical; the new record adds `replacements` |
| Kyrie's ranked replacements at UTIL (5 AM model) | PJ Washington +0.092 (REB +0.086, BLK +0.032, ST +0.013), Julian Champagnie +0.072 (REB +0.040, 3PTM +0.036), Cameron Johnson +0.066 (REB +0.037, 3PTM +0.019) |
| afternoon deck (`--phase pm`) on that record | "Kyrie Irving (UTIL) is Out today — start PJ Washington at UTIL: +0.09 expected categories this week (helps REB, BLK, ST). Next: Julian Champagnie +0.07, Cameron Johnson +0.07."; SEASON DECK: PASS, 0 page errors |
| morning deck (Kyrie `Q`) | no card; SEASON DECK: PASS, 0 page errors |

INFERENCE: rebounds is the week's coin-flip category (P(win) 0.51, projected margin +0.7), so a rebounder's one game moves the most; that is why PJ Washington, last of the three by season value, ranks first. The ranking among candidates does not depend on Kyrie's own figure: every candidate's gain is measured against the same baseline.

## 3. Bands quoted

No title share is quoted in this report. The standing structural band for any title figure on the deck is the season sweep of 2026-11-02 (deck e14cc42): **weekly_availability is FRAGILE:** -2.6 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.2 (healthy players play 0.95 of games) / +0.0 (healthy players play 0.80 of games), mean of the two seeds, as the 11-02 brief quotes it.

Runner impact: code-only. The morning "week matchup" step computes the replacement table (about ten swaps per starter set, same model as the lineup alerts); the morning and afternoon "season deck" steps read it. No new step, no prompt change.

## 4. Bounds and open items

- Out of scope by design: Questionable players (the brief's own "check before lock" line covers them); bench players added after the 5 AM run (no ranking row; season value, labelled); games already started.
- In scope and unverified: the first live render (the next run after merge that sees a starter Out).

## Watchlist

- Next run with a starter Out: the card appears on the published page above the matchup board, ranked by the matchup.

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
