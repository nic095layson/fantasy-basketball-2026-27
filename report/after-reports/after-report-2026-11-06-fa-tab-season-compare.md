# Free Agents tab: season z only, equal rows; season totals side by side on the Trade Analyzer and Free Agents tabs (owner 2026-11-06)

Pull window: 2026-11-04 → 2026-11-05 (no pull: the records on season/daily read only at 1e6652a — board, form and status records of 11-05; kit main 3fbf640, deck main e14cc42).

**Method up front.** Two owner asks on 2026-11-06, with a screenshot of the tab: (1) "remove this [the sort selector and its two notes] and make it zscore season outlook ... so that the player fields are equal"; pick on the card: **season z only** — no sort control, rows in the I-drop shape, the status and waiver chips stay, this-week and minutes notes leave the rows. (2) "when I select 2 players (both in Trade Analyzer and Free Agent tabs), have their SEASON TOTAL stats displayed side by side. Also add FG%, FT%, and 3PM." Method parameters, stated before the build: the totals are the form record's (`form_board.py`: regular-season box scores in `data/actuals`, DNPs excluded — the same games the season lines blend in); the record gains a `totals` block (sums per player), and the deck falls back to `per_game × games` on a record written before this build; FG%/FT% are season made/attempted; "better" = the higher figure, except turnovers (fewer); equal figures mark nobody. EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: both built, tested (suite 800 OK, 2 pre-existing skips) and run on the live 11-05 records; nothing merged. One thing to see: with the week sort gone, the season-z list now leads with injured players (Jalen Williams, Out to 2027-03-02; Porziņģis; Cason Wallace) — their chips say so, but you may want them filtered or sunk; not built, decision below.**

## 1. What was built (EVIDENCE: the diff, the suites)

- `scripts/season_deck.py`, Free Agents pane: the `fa-sort` select and the "This week = …" and "Status today …" notes removed; the pool is season z, descending (the 2026-10-20 order); rows are `name · pos · team · z` + status chip + waiver chip (the this-week figure and the min/g note no longer on this tab — the Today tab's "This week's adds" and the Movers tab keep them). Supersedes the 2026-10-22 week sort and the 2026-10-23 minutes note on this tab.
- `seasonCompare(names)`: with exactly two players ticked across a pane's two lists, a card "Season totals — A vs B": games · min/g, FG% (made/att), FT% (made/att), 3PM, PTS, REB, AST, ST, BLK, TO; the better figure marked (`td.best`, a filled pill); a player with no box line yet → "No box scores yet for …". Placed above the z screen on both the Trade Analyzer and the Free Agents panes.
- `scripts/form_board.py` `summarize()`: `totals` = the summed box cells per player (pts, reb, ast, stl, blk, tpm, tov).
- Tests: `test_season_deck` — the week-sort test rewritten as season-z-only (no `#fa-sort`, no notes, row text exactly `Other FA · SF · LAL · z 5.00`); the status-note and no-pins tests assert the notes are gone; the FA minutes test asserts min/g left the rows; the this-week-note one-line test removed with the note; `SeasonCompare` (3: totals and marks on the FA tab, one pick shows nothing + the trade tab, a player without box scores). Fixture `form_record()` gains `per_game` and `totals`. Whole suite 800 OK.

## 2. Re-runs on the records (EVIDENCE: scratch worktree at 1e6652a, removed after; the records tree untouched)

`form_board.py --date 2026-11-05`: PASS; Julian Champagnie `totals` {pts 78, reb 30, ast 11, stl 8, blk 6, tpm 22, tov 3} over 8 games. `season_deck.py --date 2026-11-05`: PASS, 0 page errors; `#fa-sort` absent; first four I-add rows: Jalen Williams · SF,PF · OKC · z 1.12 · Out (ESPN), back 2027-03-02 / Kristaps Porzingis · C · GSW · z 0.84 · O (Yahoo), back 2026-12-01 / Cason Wallace … / Tobias Harris … back 2026-11-09. Ticking Ty Jerome and Julian Champagnie: "Season totals — Ty Jerome vs Julian Champagnie: games · min/g 7 · 30.9 | 8 · 26.1; FG% 50.4% (67/133) | 43.1% (25/58); FT% 87.0% (40/46) | 85.7% (6/7); 3PM 18 | 22; PTS 192 | 78; REB 25 | 30; AST 36 | 11; ST 7 | 8; BLK 2 | 6; TO 18 | 3".

INFERENCE: the injured-first ordering is the season z doing what it says; the week sort used to push scored, available players up. Decision for the owner (not built): sink players Out beyond N days to the bottom, or leave the chips to say it.

## 3. Bands quoted

No title share is quoted as a new figure in this report. The standing structural band for any title figure is the season sweep of 2026-11-02 (deck e14cc42): **weekly_availability is FRAGILE:** -2.6 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.2 (healthy players play 0.95 of games) / +0.0 (healthy players play 0.80 of games), mean of the two seeds.

Runner impact: code-only. The morning "form board" step writes the totals from its own code; "season deck" reads them; no step, flag or prompt change.

## 4. Bounds and open items

- Out of scope by design: a filter or sort penalty for injured free agents (decision above); per-game or per-36 columns on the compare card (the Movers tab has them); the Today tab's "This week's adds" card, untouched.
- In scope and unverified: the first live morning run after merge (the form record carries `totals`; the deck reads them rather than the fallback).

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
