# After-report — 2026-10-08 (standing checks): the repeat-name market check, Flagg on the WO-5 queue, and what else is worth tuning

**Owner request (2026-10-08).** After the answer on "beating the card" (the card does not learn from the mocks; the mocks are graded on the card's own lines, so only outside evidence can show a line is wrong), the owner said yes to both offered options: (1) add Cooper Flagg to the WO-5 review — check his projection against the outside sources and his preseason minutes, and settle the two boards (kit 14, deck 22); (2) make it a standing check — any player who is the card's top pick in 5 or more mocks while sitting 25+ places from the market gets an outside-source check at every refresh. And asked: "Is there any additional, logical and effective, fine tuning to the system and calculations that you suggest?" Items 1 and 2 are applied below (D-RN-2, D-RN-1); the question gets measured evidence and a recommendation, with every change left to the owner (§5, decision sheet).

**Method.** Every figure is read from a committed file: the deck plane's `arena/results/repeat_market_check_2026-10-08.json` (the check's first run) and `arena/results/tuning_2026-10-08/*.json` (the read-only tests, scripts in `arena/mocks/tuning_1008/`), the kit's `report/market/` files and `top-200-2026-27.md`, and the follow-card grades `arena/results/m5[6-9]_*`, `m6*_*`, `m70_*`. Verification: this file passes `report/check_report.py`, the deck's `judgment_open_items.py --check-report` and `repeat_market_check.py --check-report`.

Pull window: 2026-10-08 → 2026-10-08 (no data pull; two owner decisions applied and one question answered; the fifth report of the day).

**Headline.** The standing check is live: on the current page (v51) the card's 🎯 at your 260 owner turns across the 20 graded mocks is one of 41 players, and twelve of them take 72% of those turns. Ten players meet the owner's rule; three of their lines are questioned by all four outside rank sources (PJ Washington, Daniel Gafford, Devin Vassell) and join WO-5 by name, with Flagg. Flagg's 14-versus-22 gap is not his own line (identical on both planes since 10/01): every one of the nine players ranked between his two places carries a richer line on the deck than on the kit, which the WO-5 merge settles. Of the further tuning tested, one is worth doing before the draft — a per-category range check at WO-5 (131 of the 145 checkable top-150 rows carry a cell outside every outside reference) — and two common ideas are measured and rejected (blending Yahoo's ranks into value; a youth adjustment).

## 1. Roster changes

None — no pull ran for this report; the day's sweep and its roster changes are in `after-report-2026-10-08.md`. No pool row moved on either plane.

## 2. Flagg on the WO-5 queue (D-RN-2, applied)

**Recorded in** `report/pre-draft-workorder-2026-10-01.md`, WO-5 "Queue additions (owner, 2026-10-08)". Nothing on his line moves before WO-5: a line moves only on the two-outlet rule with the Dallas box scores for the role.

**His line against every outside line on file** (per game):

| line | GP | PTS | REB | AST | STL | BLK | 3PM | FG% (FGA) | FT% (FTA) | TO | rank in that list |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ours, both planes | 74 | 21.0 | 8.5 | 4.5 | 1.4 | 1.2 | 1.7 | .480 (16.5) | .780 (5.0) | 2.6 | kit 14, deck 22 |
| Yahoo 10/06 | 75 | 23.0 | 7.7 | 5.0 | 1.3 | 1.0 | 1.3 | .474 | .840 | 2.6 | Yahoo Rank 7 (XRank 13, ADP 10.4) |
| Hashtag 10/06 | 72 | 23.3 | 7.3 | 4.9 | 1.3 | 1.0 | 1.3 | .475 (18.5) | .836 (5.3) | 2.2 | 17 |
| RotoBaller 9/29 | — | 22.4 | 6.5 | 5.1 | 1.2 | 0.9 | 1.1 | .468 | .828 | 2.3 | 13 |
| Statdunk 8/24 | 67 | 24.0 | 7.2 | 5.2 | 1.36 | 1.02 | 1.26 | .486 (18.7) | .836 (5.5) | 2.46 | 11 |
| his 2025-26 (Rotoworld profile) | 70 | 21.0 | 6.7 | 4.5 | 1.2 | 0.9 | 1.0 | .468 (17.1) | .827 (4.9) | 2.3 | Rotoworld 9-cat 10 |

Our line has a different shape from every other: free-throw percentage .780 against .827–.840 (his own rookie season .827), points at the bottom of the range, and threes, rebounds and blocks above every source. On the deck's own engine (`flagg_sensitivity.json`) his rank is 22 on our line, 45 on his rookie line as it stands, and 19 on the mean of the four outside lines — so even the outside consensus line does not lift him near the market's 10.

**The two boards** (`flagg_planes.json`). His line is the same on both planes (D-WO1-1(d) adopted the kit's line on 10/01). The kit's games-based availability rule applied to the deck moves him one place (22 to 21). The gap is the players around him: all nine who rank above him on the deck but below him on the kit carry a different, richer line on the deck — Haliburton +2.79 in the deck's z-sum, Jalen Johnson +1.23, Mobley +1.24, Jalen Williams +1.15, Tatum +0.73, Kyrie Irving +0.62, Jamal Murray +0.55, Durant +0.51, Mitchell +0.49. Across the deck's top 150, 35 of 148 comparable rows carry the same line on both planes; WO-5's one-line merge of the top 150 (D-WO1-1(a)) is what settles Flagg's rank, and the WO-5 entry asks for his rank on both boards after it.

**Where rooms took him** (rooms 51–70, the draft states): #6 to #21, median #13; on the board at 25 of your turns (19 at #10, 6 at #15); in the card's Top-5 at none of them as drafted. Replayed on today's page, the card would have shown him 2nd at #15 in mock 55. Your one pick of him, mock 70 #15 (card #8), graded +2.37 title points over the card's Jalen Williams.

## 3. Is the card siloed? The record

**No memory.** The card reads the player pool and the current draft only: the page's engine code (comments stripped) contains no read of the network, browser storage, past draft states or arena results (checked 2026-10-08), and the 9/29 repeat-name audit's mechanism finding stands.

**It reacts to the roster.** The repeat-name audit, run on every room since 56, re-ranks each owner turn with the other rooms' rosters swapped in. In mock 70 the #1 changed under most of the 19 other rosters at 9 of the 12 turns after #10 (`m70_repeat_names_audit.json`). At #10 the roster is empty and the pool nearly identical room to room: the #1 there was Towns in 15 rooms and Jalen Johnson in 5 (as drafted).

**But it recycles names.** Replayed on today's page, the 🎯 at the 260 owner turns of the 20 graded mocks is one of 41 players; the twelve most frequent take 186 of the 260 (Mamukelashvili 27 turns, PJ Washington 25, Towns 21, Pritchard 18, Jalen Williams 16, Anunoby 16, Suggs 15, White 11, Gafford 11, Lendeborg 10, LaVine 9, Hartenstein 7). The cause is structural — the same seat means the same pick numbers, the rooms draft alike, and the value half of the card is fixed between data pulls — so a player the lines like more than the market is on the board at every turn and looks good every time. If one of those lines is wrong, the card repeats the mistake every draft and no mock can show it, because every mock is graded on the same lines. That is the gap D-RN-1 closes.

**Your picks off the card** (single-turn swaps in the follow-card grades, rooms 56–61, 64, 66–70, 52 turns): your pick graded above the card's 🎯 10 times (+9.73 title points in all), below 33 times (−92.61), equal 9 times; the largest wins Flagg #15 in mock 70 (+2.37) and Banchero #63 in mocks 66 and 64 (+1.81, +1.07), the largest loss Irving #39 in mock 57 (−7.40). Following the card all the way graded higher than the draft as made in 11 of the 12 rooms with an off-card turn; mock 69 (one off-card pick, Harden at #15) is the exception, 27.51% against 26.58%. All of these grades use the card's own lines, so they measure fit and path, not whether a line is right; a single swap also keeps your later picks, which were built around the man you took.

## 4. Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 3e594b9dc16b), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 20 of 20 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-06.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-06.csv`, `hashtag-2026-10-06.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| PJ Washington | 16 of 20 | 87 | 149 | 178 | 144 | 141 | 121 | ast 2.4 vs 1.9-2; tov 1.5 vs 1.7-1.8; fg_pct .470 vs .448-.451; ft_pct .750 vs .698-.703 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Sandro Mamukelashvili | 16 of 20 | 81 | 170 | 138 | 105 | 153 | 120 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 15 of 20 | 28 | 65 | 60 | 56 | 43 | 44 | pts 18.5 vs 16.4-17; ast 2.3 vs 2.1-2.1; ft_pct .805 vs .813-.819 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Payton Pritchard | 15 of 20 | 37 | 82 | 33 | 90 | 92 | 72 | stl 1 vs 0.7-0.8; tpm 3.8 vs 3-3.2; tov 2 vs 1.3-1.3; ft_pct .850 vs .873-.875 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Daniel Gafford | 9 of 20 | 90 | 181 | 188 | 180 | 161 | 155 | pts 10.5 vs 9.1-9.8; reb 7.5 vs 5.8-6.5; ast 1.5 vs 1.1-1.2; blk 1.7 vs 1.2-1.4; fg_pct .700 vs .648-.689; ft_pct .700 vs .671-.687 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Jalen Suggs | 9 of 20 | 59 | 108 | 89 | 54 | 84 | 99 | pts 17 vs 14.1-15.1; ast 4 vs 4.8-5 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 8 of 20 | 82 | 144 | 94 | 121 | 137 | 98 | reb 7.5 vs 5.5-6.9; tpm 0.9 vs 1.2-1.3; fg_pct .520 vs .447-.498; ft_pct .740 vs .765-.828 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Isaiah Hartenstein | 7 of 20 | 75 | 104 | 141 | 92 | 100 | 102 | pts 11.5 vs 9.1-10.5; reb 11 vs 9.2-10.3; fg_pct .585 vs .597-.611; ft_pct .680 vs .642-.656 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Zach LaVine | 6 of 20 | 56 | 101 | 162 | 68 | 77 | 118 | pts 22.5 vs 17-21.1; reb 4.5 vs 3.1-3.6; ast 4 vs 2.8-3.4; tov 2.6 vs 2-2.4 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 5 of 20 | 89 | 142 | 122 | 131 | 125 | 123 | pts 16.8 vs 13.4-15.1; tov 1.5 vs 1-1.2; fg_pct .465 vs .432-.443 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |

Near misses (the 🎯 in 5+ mocks, under 25 places): Karl-Anthony Towns (15 mocks, value 6, market 15); Jalen Williams (14 mocks, value 16, market 39); Derrick White (11 mocks, value 24, market 45); Jalen Johnson (6 mocks, value 13, market 11); Mikal Bridges (6 mocks, value 61, market 83).


**Built (D-RN-1, applied).** `scripts/repeat_market_check.py` on the deck plane: it replays every graded mock on the page with the deck's own engine (`live_deckcard.py`, the priced-only late card included), counts the mocks in which each player is the 🎯, and flags the owner's rule; the section above is its output for v51, pasted as printed (only the heading numbered). `--check-report` refuses a report that lacks a row for a flagged name; this kit's `check_report.py` now requires the section heading in every after-report; `DATA-PULL.md` (§1 item 4b, §2, §5 item 6) and the work order (WO-5, WO-7) carry the step. Red-first: the five new `test_gates.py` cases failed with the script absent (5 of 42 failed, the 37 existing passed) and pass with it; the kit gate passed `after-report-2026-10-08-draft70.md` before the change and refuses it after, for the missing section alone. Two full runs wrote identical records from byte-identical replays (49 seconds each). One design correction before the record was written: the first run also read the kit's `consensus-*.csv` as an outside rank, but that file averages our own board rank with Yahoo's, and it alone was holding PJ Washington's line; it is out, leaving the four independent lists the 10/06 cross-check used.

**What the first run says.** Every flagged name sits inside WO-5's top-150 re-derivation already; the check adds two things. It names the three lines all four outside lists question — PJ Washington (the 🎯 in 16 of 20 mocks), Gafford (9) and Vassell (5) — for an explicit mechanism at WO-5 (they join the queue by name). And it prints the cells to look at: Gafford's line is above every outside projection in six of nine categories; PJ Washington's percentages and assists; Pritchard's threes and steals. The near misses carry the other half of the card's early picks — Towns (value 6, market 15), Jalen Williams (16 against 39, 23 places), White (24 against 45, 21 places) — under the 25-place bar by design.

## 5. Further tuning — tested before suggesting (owner question)

Three read-only tests on records (`arena/mocks/tuning_1008/tuning_tests.py`, output `arena/results/tuning_2026-10-08/tuning_tests.json`; actuals are Basketball-Reference's 2025-26 and 2024-25 per-game tables, the what-if's 10/07 downloads, extracted to the CSVs beside the output). Two runs agreed to the third decimal.

**A. Blend the market into our values? No.** Last season, lines built from the prior season's production (`arena/data/players_2025-10-21.csv`, the arena's opening-night pool, priced by the deck engine) against Yahoo's pre-draft ranks of 10/16/2025 (the league's own list), scored by Spearman correlation with actual 2025-26 nine-category value:

| players (Yahoo's list) | actual value | n | entering-season lines | Yahoo pre-draft rank | 50/50 rank blend |
|---|---|---|---|---|---|
| top 60 | season (games count) | 60 | 0.640 | 0.451 | 0.592 |
| top 120 | season | 120 | 0.651 | 0.552 | 0.629 |
| top 200 | season | 173 | 0.769 | 0.713 | 0.766 |
| top 60 | per game | 59 | 0.644 | 0.448 | 0.594 |

The lines beat the market's ranking at every depth, most in the early rounds, and the blend is worse than the lines alone. The system's independence from the market is worth keeping; the defence against a wrong line is the outside check per line (D-RN-1), not averaging toward ADP. Bound: that pool is a reconstruction (2024-25 production, hindsight breakouts dampened), the same family of method as ours, not our current lines.

**B. A youth adjustment for players like Flagg? No.** The same lines' misses by 2025-26 age (non-rookies, 25+ games; actual minus projected nine-category z-sum on one frame): 22 and under −0.60 (n 28, se 0.39), 23–25 −1.15 (53), 26–29 −1.05 (58), 30–33 −0.68 (33), 34 and over −0.28 (16), all players −0.88. The youngest group missed by 0.28 less than average — under one standard error, and the oldest groups did as well. No age curve worth a term; Flagg's case is his line's shape, not his age.

**C. A per-category range check at WO-5? Yes — the one change worth making before the draft.** For each of the card's top-150 lines, every category was set against the range of Yahoo 10/06, Hashtag 10/06, RotoBaller 9/29 and the player's own 2025-26 line (three or more present; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). 131 of the 145 checkable rows carry at least one cell outside every reference — 436 cells (273 on 116 rows at double the tolerance); by category FT% 84, FG% 73, TO 52, PTS 49, AST 44, REB 40, 3PM 39, STL 29, BLK 26. The cells lean flattering: 252 lift the player (+89.4 in z) against 184 that hold him down (−69.0). Largest net: Dyson Daniels (deck 11) +2.61, Ja Morant +1.81, Wembanyama +1.80, Anthony Davis +1.71, Filipowski +1.70; Knueppel −1.67, Dylan Harper −1.50, Buzelis −1.37, Kawhi Leonard −1.35. As a sensitivity only — pulling every such cell to the nearest reference — 71 of the top 150 move ten places or more: Daniels 11 to 42, PJ Washington 87 to 123, Gafford 90 to 134, Jalen Williams 16 to 25, Pritchard 37 to 45; Knueppel 94 to 52, Harden 31 to 21, White 24 to 15, Flagg 22 to 20. That is an upper bound, not a forecast: a line can sit outside every source for a real reason (a role change the sources have not priced). The proposal (D-RN-3) does not assume the sources are right; it asks WO-5 to give every re-derived cell that still sits outside all four references a one-line mechanism with two dated outlets, or bring it inside the range — mechanically listed by the same arithmetic, gated like the receipts.

**Considered and not recommended.** *A mirror check* (players the market prices a round or more above our value whom the card never shows): 98 players qualify on today's page (`mirror_check.json`), too many to act on, and the range check already catches the cells that hold such players down; Flagg himself would be shown 2nd at #15 in mock 55 on today's lines. *Re-tuning the card's 50/50 blend:* swept in August (α 0.4 and 0.6 each failed a room; `findings_2026-08-04_decw_round2.md`), and any re-tune graded on the card's own lines would favour the ΔECW half by construction. *A fairer grade for off-card picks* (replay the card from the swapped turn on, instead of keeping the later picks) is a measurement improvement, not a card change — worth building after the draft (D-RN-4).

## Watchlist

- WO-5 (10/11, 10/13): Flagg (D-RN-2) and the three LINE QUESTIONED names join the queue (Castle/Barrett, the D-RW-1 divergences, the Hashtag 10/6 rows); the standing check runs on the WO-5 page and its section goes in that report.
- The 3-of-4 lines (Mamukelashvili, Pritchard, Suggs, Hartenstein — three of the four outside lists 25+ places below ours) are a whisker under the questioned bar; WO-5 re-derives them anyway as top-150 rows.
- Flagg's free throws: .780 against .827–.840 everywhere else is the single largest cell in his line; the Dallas box scores give the minutes, not the rate.

## Open-item receipts

| item | query run (2026-10-08) | dated finding |
|---|---|---|
| (this analysis) | machine replay and records only — no web research in this report | pull receipts for the window live in `after-report-2026-10-08.md` (the morning's pull, same day) |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (after-report-2026-10-08.md, receipts dated 10/8) | all HELD or unsigned on 2026-10-08; nothing changed since |

## Bounds

- The check counts the card on the current page, replayed on the 20 graded states: a different page (WO-5's) can flag different names, which is the point of running it at every refresh.
- Test A and B rest on a reconstructed opening-night pool, not on our own 2025-26 lines (none exist); test C's references are three projections and one season of actuals, not truth. The clamp ranks are a sensitivity, not a board.
- The outside rank lists are the newest on file (Yahoo 10/06, Hashtag 10/06, Rotoworld 10/05, RotoBaller 9/29); RotoBaller's is nine days old.

## Decision sheet (owner disposes)

| # | decision | default |
|---|---|---|
| D-RN-1 | Standing repeat-name market check at every refresh (rule: 🎯 in 5+ mocks, 25+ places from the market or no Yahoo price; outside-source verdict per name) | applied 2026-10-08 (owner yes) |
| D-RN-2 | Flagg on the WO-5 queue with the line comparison and the two-board diagnosis above | applied 2026-10-08 (owner yes) |
| D-RN-3 | At WO-5, require a one-line mechanism with two dated outlets for every re-derived cell outside all four references (Yahoo, Hashtag, RotoBaller, own 2025-26), or pull it inside the range; a script lists the cells and the WO-5 report gate checks the rows | applied 2026-10-08 (owner yes, same evening; see the addendum) |
| D-RN-4 | Build the fairer off-card grade (replay the card from the swapped turn on) for post-draft retros | after the draft (owner ok, 2026-10-08) |
| D-RN-5 | Mirror check (never-shown, market a round+ ahead) as a standing rule | no — 98 names today; covered by D-RN-3 |

## Addendum — D-RN-3 applied (owner, 2026-10-08, same evening)

The owner said yes to D-RN-3 and to the schedule (WO-5 on 10/11 and 10/13, the final check on 10/13, the 10/14 lock with a fresh Yahoo paste). Built: the deck plane's `scripts/range_check.py` — the arithmetic of §5 C as a standing tool for projection passes. On today's lines it lists 131 players and 436 cells (145 of the top 150 checkable), cell for cell the same as `tuning_tests.json`; two runs wrote identical records. Its `--check-report` refuses a WO-5 report unless every listed player has a row in a "Range check" section whose text names two outlets, counted with this kit's own lexicon (`report/check_report.py`, which gains "basketball-reference", the WO-5 method's source). Red-first: five new `test_gates.py` cases failed with the script absent and pass with it. Wired into WO-5's acceptance and the 10/14 lock's projection leg (`pre-draft-workorder-2026-10-01.md`) and `DATA-PULL.md` §2; daily pulls that move no line skip it. Flagg's four cells (rebounds 8.5 against 6.5–7.7, blocks 1.2 against 0.9–1.0, threes 1.7 against 1.0–1.3, FT% .780 against .827–.840) are on the list, so WO-5 must either explain them with two dated outlets or bring them inside.

## Provenance

- Deck plane: `scripts/repeat_market_check.py`, `scripts/test_gates.py` (cases D-RN-1), `arena/results/repeat_market_check_2026-10-08.json` (page sha256 `3e594b9dc16b…`, v51 = rev `d4cc066`), `arena/mocks/tuning_1008/*.py`, `arena/results/tuning_2026-10-08/*`.
- Kit plane: `report/check_report.py` (the section anchor), `DATA-PULL.md`, `report/pre-draft-workorder-2026-10-01.md` (WO-5 queue additions, WO-7), the market files named in §2 and §4.
- Not verified: nothing here rests on web research; Basketball-Reference figures are the what-if's 10/07 downloads.

## In plain language

The card does not learn from your mock drafts, and the mocks cannot tell it a player is mis-valued, because every mock is graded with the card's own numbers. So the check against tunnel vision has to come from outside. As of today it does, on every refresh: any player the card keeps recommending — top pick in 5 or more of your mocks — while the market sits 25+ places away gets checked against four outside rankings, and against three outside stat projections category by category. The first run flags ten players; for three of them (PJ Washington, Gafford, Vassell) all four outside rankings disagree with us, so their lines get a hard look at the preseason refresh on 10/11 and 10/13, with Flagg. Flagg's lower rank on the draft tool is mostly about the players around him, whose lines on the tool are richer than on the kit; the refresh merges those lines. The one further change worth making is the category-by-category check at that refresh — many of our lines have at least one number more extreme than every outside source, and each of those should either have a reason or come back in range. Two popular ideas were tested on last season and failed: mixing Yahoo's rankings into our values made predictions worse, and young players did not beat their projections by enough to justify a youth boost.
