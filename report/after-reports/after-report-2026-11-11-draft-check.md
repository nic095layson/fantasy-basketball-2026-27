# Draft Check: the draft-day system beside the season so far, every Monday, on the tab where Movers stood (owner 2026-11-11)

Pull window: 2026-10-20 → 2026-11-10 (no pull: the box scores, weekly finals, league state and the pinned Yahoo pulls at e5bd361 on season/daily, read only; the locked draft-day lines `arena/results/players_v69.csv`, the draft card `m100_deckcard_v69.json` and the two 10,000-season draft-day simulations in the deck repository at 01483de, read only; kit main 47a094e).

**Method up front.** Owner request, verbatim: "I like this data, a lot. Can you please implement this with updating tables every monday, and include this on the season deck REPLACING the 'Movers' tab?" It follows the assessment given in chat the same day (the pre-draft system against 22 days of box scores). Three owner picks on cards before the build: "Keep minutes, drop movers", the name "Draft Check", and "Seed for Monday 11-09". Parameters, stated in the plan before the first edit: value is the engine's nine-category z-score sum, fitted once on the draft-day lines (top-156 fixed point) and applied unchanged to each player's per-game line so far; the window is every box-score day from 2026-10-20 to the day before the record's date; a player needs 5 games to enter the scatter and the actual ranks; standings are the record date's Yahoo pull. Two hand-set numbers, both display thresholds: 5 games, and 0.5 value points for "even" on the disagreement table. EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: a new Monday step writes one dated record with five tables, and the deck's fifth tab, now "Draft Check", draws the newest one, with the minutes board below it, collapsed. The season-line movers list has left the page. Suite 1132 OK. Nothing in the engine reads the record; no line, tag, roster or constant changed.**

Runner impact: prompt edit — the morning prompt's step 5 lists the seven tab names and must read "Draft Check" where it reads "Movers". The Monday step itself needs no prompt change: `morning.py` runs it, and the commit step already takes every new path under `report/`.

## 1. What was built

| piece | what it does |
|---|---|
| `scripts/draft_check.py` | Builds the record `report/draft_check/draft_check_<date>.json`: picks, preferred, teams, cats, scatter. A record is never rewritten (`--force` excepted). Prints one `DRAFT CHECK: PASS` or `HALT` line. |
| `scripts/morning.py` | A non-fatal "draft check" step on Mondays, after the preview staleness step and before the deck. |
| `scripts/season_deck.py` | Optional input `draft_check` = the newest record on or before the date. Pane `pane-draft`, tab "Draft Check". The minutes board moves into a closed section at the bottom. The season-line movers card is removed. |
| `scripts/deck_render_check.py` | The pinned tab and pane names follow. |

The five tables:

1. **Picks.** Each of the 13 draft picks: draft-day value, per-game value so far, the change, games played of team games.
2. **Disagreements.** The turns where the draft card's first choice was another player (6 of 13), both sides graded the same way. A side with fewer than 5 games is named, not graded.
3. **League.** Each team's draft-day title share and rank beside its Yahoo rank and record, with the rank agreement.
4. **Categories.** The owner's draft-day chance to win each category in a week (mean of the two seeds) beside the weeks won, lost and tied.
5. **All players.** Draft-day value against value so far for every pool player with 5+ games, the owner's picks marked, with the rank agreement.

## 2. Known answers

EVIDENCE: `scripts/test_draft_check.py` (25 tests) and `DraftCheckTab` in `scripts/test_season_deck.py` (5 tests).

| check | result |
|---|---|
| Value on a three-player pool differing only in points (10, 20, 30) | −1.2247, 0, +1.2247; an outside line of 28.165 scores +1.0 |
| The scale against the engine's own `hoops.zscores` on the draft-day lines (5 players) | within 0.15 on each |
| Per-game lines: a DNP is no game for the player and a game for his team | 1 of 2 games |
| Window: preseason days and the record's own date are not counted | 1 day of 3 |
| Disagreements list only turns where the card's first choice differs | 1 of 2 turns |
| A pull with no standings, a missing draft file, no box-score day, an unknown standings team | HALT, each named |
| A second run for the same date | the record is not rewritten |
| The deck with a record | 7 tabs, 0 page errors; all five tables read from the record |
| The deck with no record | 7 tabs, 0 page errors; "No draft check on record yet" |
| The Monday step | present on 2026-11-09, absent on 2026-11-10, non-fatal, before the deck |

On a scratch copy of season/daily, the 11-09 record reads: 19 box-score days, 263 players with 5+ games, rank agreement 0.704; Miles Bridges −1.33 → +4.49; Kel'el Ware +0.34 → −6.55; the owner ranked 1 on draft day and stands 2 (17-10-0). The 11-11 afternoon deck rebuilt there with this code: PASS, 7 tabs, 0 page errors, no sideways scroll at 400 px.

## 3. Checks

- Full suite: 1132 tests OK, 2 skipped.
- Constants check: PASS, 49 registered = 49 live (the two display thresholds are not engine constants).
- Tests that pinned the old tab were changed with the owner's order behind them: `RealMoversRender` now asserts the movers list is off the page; `WordingPassTwo.test_movers` checks the new tab; the render check's known-answer test names the new tab.

## 4. Bounds

Out of scope by design:
- The record changes nothing in the engine and no figure the brief or the simulator reads.
- `season_lines.py` still records movers and the morning report still names them; only the deck card is gone.
- The post-mortem's hindsight alternatives (the best legal player at each turn) are not on the tab; the tab shows the card's own first choices, which the draft record holds turn by turn.

In scope and not verified:
- `draft_check.py` was written before its tests; only the deck's tests were seen red first (16 failures and 7 errors on the old tab's assertions, then green).
- The step has not run inside the Runner's session. NOT-ATTEMPTED: it first runs there on Monday 2026-11-16.
- A player traded mid-season is counted against his latest club's games.
- The plan named today's 11-11 figures as known answers; the tests use hand-worked fixtures and the engine-parity check instead, because the real records live on season/daily, not on main.

## 5. Next steps (owner decisions)

1. Merge this PR, or hold.
2. Paste the one-line prompt edit into the Runner's conversation: in step 5, "Today, Trade Analyzer, Free Agents, Board, Draft Check, Week, League". Until then the Runner's own tab-name sentence is out of date; the build's render check already enforces the new names.
3. The 11-09 seed record is committed to season/daily on the owner's pick; the tab shows it from the first deck built after the merge.

## Fired

plan-gate (loaded; compact plan table shown before the first edit, as CLAUDE.md accepts) · adversarial-verify (loaded before the commit) · scope-fence not loaded: the work stayed inside the order.

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds. This report quotes no title share of its own; the draft-day shares in the league table are the 10-14 simulation's.

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
