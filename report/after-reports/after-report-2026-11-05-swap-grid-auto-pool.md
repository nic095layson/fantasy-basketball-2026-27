# Today's start/sit heat map by this week's needs, and auto pool rows for rostered players the pool lacked (owner 2026-11-05)

Pull window: 2026-10-22 → 2026-11-05 (no pull: the records on season/daily read only at a6688ad — week-matchup briefs, status files, league state, box scores; kit main 2c5c2cf, deck main e14cc42).

**Method up front.** Owner's asks: (1) "recommend roster moves for daily matchups (especially after the 3PM run) replacing the 'Not in the pool....' content ... dynamic based on the categorical needs of the matchup ... start (Player) for (player) to bench --> [stat category] projected gains, in heat map display (blue in varying projection)"; (2) "This 'Not in the pool' callout — is this not something the tool can pull during the morning runner? For example, pulling Thybulle's stats to build his projection in the pool". Owner's picks on the card: **build the heat map for both runs** and **auto season line** for unpooled rostered players. Method parameters, stated before the build: the grid's pairs and cells are `week_matchup`'s replacement table from the 5 AM run (every bench player with a game today who fits a starter's Yahoo slot; the cell is the change in P(win) for the category this week by the Week card's model, `today_swap_cats`); the deck computes nothing new — it filters the table by its own status file (the 3 PM one in the afternoon) and ranks by the change in expected categories, top 6. The auto pool row's prior is the replacement-level line — the mean of the deck plane's rows ranked 146–166 by the engine's own z (the band around the 156th draftable row), percentages attempt-weighted — blended with the player's games by the same `PRIOR_GAMES` as every row; a rostered player the pool lacks needs 3+ box-score games. Both numbers are hand-set: registered `uncalibrated`, decision D-AP-1. EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: both built, tested and run clean on the live records (suite 798 OK, 2 pre-existing skips); on 11-04 the grid names Kyrie Irving for Collin Gillespie (+0.145 expected categories; PTS +8.9 points of P(win), FT% +2.5, FG% +1.9) as the top swap, with Matkovic unreachable by a direct slot swap; the auto rule gives all four rostered unpooled players a row (Meleek Thomas 5 games, Nolan Traore 8, Matisse Thybulle 9, Quenton Jackson 9) — and the prior is strong: Thybulle's line reads 10.6 points against 8.0 in his box scores. Nothing merged.**

## 1. What was built (EVIDENCE: the diff, the suites)

- `scripts/season_deck.py` — `swap_grid(today_rows, me, avail, repl, moves, top=6)`: flattens the replacement table into (bench, starter) pairs, drops any pair whose starter or bench player has no game or is Out by this build's status, ranks by `d_exp`, marks `kit` when the morning's lineup moves named the pair. `D.swap_grid` in the page data; Today-tab card "Start/sit for today — by this week's needs": start · for · slot · nine cells shaded blue by the cell's share of the grid's largest gain (red tint for a loss; white text on the darkest blue) · Δ cats; ★ on a kit-named pair. A grid with rows leads the tab after the Out-today card; an empty grid's card ("nothing to swap" / "No game for your players today") sits under the Week card so the matchup board keeps the lead. The "Not in the pool" card is now a one-line footer under it. CSS: `.heatmap td.heat`.
- `scripts/season_lines.py` — `replacement_prior(deck_rows)` and `auto_rows(...)`; `run(..., state_json=)` appends an auto row per rostered unpooled player with `AUTO_MIN_GAMES`+ games (name, NBA team, positions from the team's own unpooled entry, note "auto: …"), then blends it like every row; the record gains `auto_rows` and `auto_rule`, and `unpooled_with_games` drops those names. `main()` passes `data/league_state.json`. Constants `AUTO_MIN_GAMES` 3, `AUTO_PRIOR_LO` 146, `AUTO_PRIOR_HI` 166 registered `uncalibrated` (D-AP-1); `STATE` added to the checker's path ignore list.
- Tests: `test_season_deck.SwapGrid` (2: ranking, filters, kit mark, top; the rendered card and the empty state), `test_season_lines.AutoRows` (3: the band mean and a short plane's tail; three games make a blended row and two do not; a name on the plane or no state file makes none). Whole suite 798 OK.

## 2. Re-runs on the records (EVIDENCE: scratch worktree at a6688ad, removed after; the records tree untouched)

- `season_lines.py --date 2026-11-05`: `SEASON LINES: PASS — … 4 auto row(s) for rostered players the pool lacked (Meleek Thomas 5g, Nolan Traore 8g, Matisse Thybulle 9g, Quenton Jackson 9g); 140 unpooled players with games`. Replacement prior (deck rows 146–166): 12.6 pts, 4.6 reb, 3.5 ast, 1.4 3PM, 1.0 stl, 0.5 blk, 1.7 tov, FG% .460, FT% .770. Thybulle's row: 10.6 pts / 3.4 reb / 2.6 ast / 1.2 stl / 0.7 blk on 9 games whose box average is 8.0 / 1.7 / 1.3 / 1.7 / 1.0 (24.2 min). INFERENCE: with k ≈ 12 games on points, the prior still carries more than half the line at 9 games; D-AP-1 should look at a lower band or a lower k for auto rows once four weeks have graded them.
- `season_deck.py --date 2026-11-04` and `2026-11-05` with the new code: `SEASON DECK: PASS … pins 16 inputs; 0 page errors` both days. 11-04 grid (six rows): Kyrie Irving for Gillespie +0.145, for PJ Washington +0.121, for Derrick White +0.086, for McDaniels +0.082, for Ty Jerome +0.042; Kris Dunn for Gillespie −0.033. 11-05: no bench player with a game fits a starter's slot — the empty card sits under the Week card. Phone width (390 px): no horizontal overflow.

INFERENCE: the grid shows direct slot swaps; the morning's "Kyrie for Matkovic" was a reshuffle (Kyrie cannot take the F slot), so it does not appear as a pair and the ★ does not mark it. The Out-today card still covers a starter the status calls Out.

## 3. Bands quoted

No title share is quoted as a new figure in this report. The standing structural band for any title figure is the season sweep of 2026-11-02 (deck e14cc42): **weekly_availability is FRAGILE:** -2.6 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.2 (healthy players play 0.95 of games) / +0.0 (healthy players play 0.80 of games), mean of the two seeds. The auto rows enter the simulator's pool from the next morning's intake; the sweep re-runs on the engine's schedule, not per row.

Runner impact: code-only. The morning "season lines" step gains the auto rows from its own default; "season deck" and the 3 PM rebuild read the grid from the week-matchup record they already read. No new step, no prompt change.

## 4. Bounds and open items

- Out of scope by design: a 3 PM recompute of the swap figures with the afternoon's injuries (the afternoon build filters who plays and who is Out; the Δ figures are the 5 AM model's, said on the card); auto rows for unrostered unpooled players (no positions on record for them; they stay in `unpooled_with_games`); reshuffle pairs (two moves at once).
- Flagged, not fixed (adjacent): the replacement prior's strength on auto rows (above, D-AP-1).
- In scope and unverified: the first live morning run after merge — the auto rows reach `pool_season.csv` and, the morning after, the intake carries those four as pooled and the "Not in the pool" footer empties.

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
