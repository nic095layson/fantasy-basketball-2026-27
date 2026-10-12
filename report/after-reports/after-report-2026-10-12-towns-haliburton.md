# After-report — Towns at #10, or Haliburton at #10 and Towns at #15: the card's arithmetic, 13 rooms re-graded three ways, and the 2025-26 lines

**Owner request (2026-10-12, verbatim):** "Can you please explain to me from your arithmetic perspective why Towns is suggested as my first round pick, when potentially Maxey, Edwards, Haliburton may still be on the board? Also.. Can you please review on previous mock / live draft records? What if I were to select Haliburton at 10, and KAT at 15?" Then, with the owner's PDF `9Cat_Final_Rankings_2025-2026.pdf`: "If this helps you, here are the final stats at the end of last season 2025-2026".

**Method:** the deck card's own score at #10 (blend50: half the percentile of ΔECW, the expected weekly categories a player adds against the room's rosters, half the percentile of balanced value) read from the saved card replays of 30 rooms; three sensitivities on mock 75's #10 board (Haliburton's availability, 2025-26 lines); the 13 slot-10 rooms where both men were on the board at #10 re-graded with the owner's other eleven picks held, strict pairwise swaps, 18,000 CRN seasons on the league's real eight-team bracket, three ways (shipped lines, Haliburton fully healthy, last season's lines). The PDF was read with pdfplumber (10 pages, md5 `c4b313cfcda34071ece4cefe99e9049a`), raw text pinned; every 2025-26 figure is checked against the deck's verified actuals (`arena/results/actuals_2026-10-09/actuals_2025-26.csv`, Basketball-Reference and ESPN). Verification: this file passes `report/check_report.py` and the deck's `judgment_open_items.py --check-report` and `repeat_market_check.py --check-report`.

Pull window: 2026-10-12 → 2026-10-12 (analysis only, the fifth report of the day; no roster pull).

**Headline.** On the shipped lines the card takes Towns at #10 because he is second on both halves of its score and the only man near the top of both (value 4.15 behind Davis's 4.38, ΔECW 4.327 behind Jalen Johnson's 4.365, on mock 75's board) — but his line is his 2024-25 season; on his 2025-26 line (two sources) the same card ranks him #26 at #10 and Maxey #1. Haliburton at #10 and Towns at #15, graded in the 13 rooms where both were on the board: on the shipped lines Towns-first is better under every survival read (by 1.44, 2.18, 3.37 title points); with Haliburton fully healthy it flips when Towns lasts (Haliburton first ahead by 1.92 on the public-room record, behind by 0.89 if Towns goes at #11 as in the cast); on last season's lines taking both is the weakest outcome (6.62 against 9.20 and 8.68).

## 1. Roster changes

None — analysis only; no row moved on either plane.

## 2. Why the card says Towns at #10

The card's score is half the ΔECW percentile and half the balanced-value percentile. At #10 Towns is second on each half (Davis has more value, Jalen Johnson more ΔECW) and the only player near the top of both. Mock 75's board (v59):

| player | value (z-sum after availability) | ΔECW (cats/week) | card rank | survival to #15 | Yahoo ADP 10/12 |
|---|---|---|---|---|---|
| Karl-Anthony Towns | 4.15 | 4.327 | 1 | 0.53 | 15.6 |
| Tyrese Maxey | 3.63 | 4.185 | 2 | 0.25 | 9.7 |
| Jalen Johnson | 3.15 | 4.365 | 3 | 0.36 | — |
| Tyrese Haliburton | 3.87 (4.96 raw × 0.78) | 4.146 | 4 | 0.43 | 13.5 |
| Anthony Edwards (mock 74's board; gone at #9 in mock 75) | 3.66 | 4.211 | 2 | 0.18 | 7.8 |

Towns' line on the board (24.8 points, 12.5 rebounds, 2.1 threes, .525 / .830) makes him a center who adds field-goal percentage (+1.02), free throws (+0.61) and threes (+0.36) on top of rebounds (+2.49) and points (+1.38); bigs usually cost the first three. Maxey's and Edwards' scoring is offset by field-goal percentage on volume (−1.10, −0.91) and turnovers (−0.35, −1.69). Haliburton has the best raw line of the four (+4.96, assists +2.69, threes +1.32) and loses it to the first-season-back Achilles tag (value ×0.78, weekly availability 0.75); he passes Towns once he is rated at about 84 percent of a healthy season (`breakeven.txt`).

**The line under the pick.** Towns' board line is his 2024-25 season (24.4 / 12.8 / 2.0 threes / .526 / .829 in 35.0 minutes). In 2025-26 he played 75 games at 31.0 minutes: 20.1 points, 11.9 rebounds, 1.5 threes, .501 / .858 — the deck's verified actuals and the owner's PDF give the same totals (1,504 points, 889 rebounds, 113 threes in 75 games). On that line his value is 1.93 (29th on the board, against 4.15 and 6th) and the same #10 card ranks him #26, Maxey #1 and Haliburton #2. With every row that played 40+ games in 2025-26 on its 2025-26 per-game line, the #10 card reads Maxey #1, Haliburton #8, Towns #23. The staleness is board-wide: 44 of the 52 top-60 rows with a 2025-26 season of 20+ games sit closer to their 2024-25 line than to 2025-26. The owed WO-5 refresh rebuilds every top-150 line from the 2025-26 per-36 rates scaled to projected minutes; it has not run.

The owner's PDF (Hashtag Basketball, 2025-26 season totals, Top 200, turnovers weighted ×0.25):

| player | 2025-26 9-cat rank | games |
|---|---|---|
| Tyrese Maxey | 5 | 70 |
| Donovan Mitchell | 10 | 70 |
| Karl-Anthony Towns | 12 | 75 |
| Jalen Johnson | 13 | 72 |
| Chet Holmgren | 19 | 69 |
| Anthony Edwards | 27 | 61 |
| Tyrese Haliburton | not in the Top 200 | — |
| Anthony Davis | not in the Top 200 | — |

Haliburton missed 2025-26 with the Achilles tear; Davis played 20 games (the deck's actuals), too few for the page's season-total Top 200.
[EVIDENCE: `arena/results/whatif_hk_2026-10-12/card_lines_2025-26.json`, `breakeven.txt`; the saved card replays `arena/results/m*_deckcard_*.json`; `report/market/hashtag-final-9cat-2025-26-raw-2026-10-12.txt`]

## 3. Who lasted from #10 to #15 on the record

| rooms | Towns left at #10 by the owner | lasted to #15 | Haliburton left at #10 | lasted to #15 |
|---|---|---|---|---|
| public Yahoo rooms (15) | 6 | 6 | 11 | 3 |
| the deck's league-mate cast (10) | 3 | 0 | 0 (gone before #10 in all 10) | — |

Haliburton went at #11–#14 in mocks 51 (#14), 52 (#14), 53 (#14), 57 (#13), 60 (#14), 61 (#11), 73 (#12), 74 (#14). In the cast rooms Towns went at #11 every time he was left (mock 55 to Noah, mock 70 to Cayas, mock 71 to Cayas); Cayas holds seat 11 in the real order. In the league's real 2025-26 draft Towns went #7 against a pre-draft rank of 14 (`arena/data/league_draft_2025-26_raw_2026-10-01.txt`, `league_predraft_ranks_2025-26_raw_2026-10-01.txt`).

## 4. Haliburton at #10, Towns at #15 — the 13 rooms graded

**The shipped lines (v58 = v59 values).** Means: Towns + Haliburton 19.27%; Towns + the card's #15 21.24%; Haliburton + the card's #15 17.03%. Losing Towns costs more than losing Haliburton in 12 of 13 rooms. Haliburton first wins at no Towns survival rate.

| survival read | Towns first | Haliburton first | Haliburton first minus Towns first |
|---|---|---|---|
| public rooms on record (Towns 6 of 6, Haliburton 3 of 11) | 20.70% | 19.27% | -1.44 |
| the deck's survival read at #10 (v59 prices) (Towns 0.53, Haliburton 0.43) | 20.39% | 18.21% | -2.18 |
| the league cast on the real seating (Towns taken at #11 in 3 of 3 cast rooms; Haliburton 0.43 from the model) | 20.39% | 17.03% | -3.37 |

**Haliburton fully healthy (his first-season-back tag cleared).** Means: Towns + Haliburton 23.71%; Towns + the card's #15 21.07%; Haliburton + the card's #15 21.31%. Losing Towns costs more than losing Haliburton in 7 of 13 rooms. Haliburton first wins once Towns lasts to #15 with probability 0.37 or more.

| survival read | Towns first | Haliburton first | Haliburton first minus Towns first |
|---|---|---|---|
| public rooms on record (Towns 6 of 6, Haliburton 3 of 11) | 21.79% | 23.71% | +1.92 |
| the deck's survival read at #10 (v59 prices) (Towns 0.53, Haliburton 0.43) | 22.20% | 22.58% | +0.38 |
| the league cast on the real seating (Towns taken at #11 in 3 of 3 cast rooms; Haliburton 0.43 from the model) | 22.20% | 21.31% | -0.89 |

**Last season's lines (every row with 2025-26 GP 40+ on its 2025-26 per-game).** Means: Towns + Haliburton 6.62%; Towns + the card's #15 9.20%; Haliburton + the card's #15 8.68%. Losing Towns costs more than losing Haliburton in 9 of 13 rooms. Haliburton first wins at no Towns survival rate.

| survival read | Towns first | Haliburton first | Haliburton first minus Towns first |
|---|---|---|---|
| public rooms on record (Towns 6 of 6, Haliburton 3 of 11) | 8.50% | 6.62% | -1.88 |
| the deck's survival read at #10 (v59 prices) (Towns 0.53, Haliburton 0.43) | 8.09% | 7.59% | -0.50 |
| the league cast on the real seating (Towns taken at #11 in 3 of 3 cast rooms; Haliburton 0.43 from the model) | 8.09% | 8.68% | +0.59 |

Per-room figures for the shipped lines:

| room | owner #10 / #15 as drafted | as drafted | Towns + Haliburton | Towns + the card's #15 (Haliburton gone) | Haliburton + the card's #15 (Towns gone) | the card's #15 on each path |
|---|---|---|---|---|---|---|
| mock 51 | Anthony Edwards / Karl-Anthony Towns | 19.04% | 10.92% | 19.04% | 8.54% | Towns path: Anthony Edwards; Haliburton path: Chet Holmgren |
| mock 52 | Jayson Tatum / Donovan Mitchell | 11.15% | 15.89% | 17.59% | 13.75% | Towns path: Donovan Mitchell; Haliburton path: Chet Holmgren |
| mock 53 | Jayson Tatum / Karl-Anthony Towns | 12.96% | 15.43% | 12.96% | 14.58% | Towns path: Jalen Williams; Haliburton path: Chet Holmgren |
| mock 56 | Karl-Anthony Towns / Tyrese Haliburton | 9.63% | 9.63% | 13.74% | 5.73% | Towns path: Tyrese Maxey; Haliburton path: Chet Holmgren |
| mock 57 | Jayson Tatum / Karl-Anthony Towns | 13.21% | 15.16% | 18.23% | 13.83% | Towns path: Jalen Johnson; Haliburton path: Chet Holmgren |
| mock 58 | Tyrese Haliburton / Karl-Anthony Towns | 22.63% | 22.63% | 24.92% | 19.30% | Towns path: Tyrese Maxey; Haliburton path: Chet Holmgren |
| mock 59 | Tyrese Haliburton / Karl-Anthony Towns | 14.95% | 14.95% | 15.75% | 12.71% | Towns path: Tyrese Maxey; Haliburton path: Chet Holmgren |
| mock 60 | Karl-Anthony Towns / Kevin Durant | 33.73% | 33.22% | 33.73% | 32.27% | Towns path: Jalen Williams; Haliburton path: Chet Holmgren |
| mock 61 | Karl-Anthony Towns / Donovan Mitchell | 16.60% | 15.42% | 16.60% | 14.54% | Towns path: Donovan Mitchell; Haliburton path: Chet Holmgren |
| mock 67 | Karl-Anthony Towns / Tyrese Haliburton | 18.48% | 18.48% | 21.14% | 19.73% | Towns path: Jalen Johnson; Haliburton path: Chet Holmgren |
| mock 73 | Karl-Anthony Towns / Donovan Mitchell | 34.17% | 33.22% | 34.89% | 28.19% | Towns path: Donovan Mitchell; Haliburton path: Chet Holmgren |
| mock 74 | Karl-Anthony Towns / Donovan Mitchell | 17.91% | 16.10% | 17.91% | 12.29% | Towns path: Jalen Williams; Haliburton path: Chet Holmgren |
| mock 75 | Karl-Anthony Towns / Tyrese Haliburton | 29.39% | 29.39% | 29.66% | 25.86% | Towns path: Donovan Mitchell; Haliburton path: Chet Holmgren |

[EVIDENCE: `arena/results/whatif_hk_2026-10-12/{shipped,haliburton_healthy,lines_2025-26}/`, `survival_records.json`, README there]

**Reading.** On the shipped lines the order the card gives is the better one under every survival read: when Haliburton is gone at #15 the card's #15 man (Mitchell, Maxey, Jalen Williams or Jalen Johnson) grades better beside Towns in 12 of 13 rooms, while when Towns is gone the card's #15 is Holmgren and the roster loses about two title points. If Haliburton is rated fully healthy, Haliburton first is better whenever Towns is likely to last (the public rooms: 6 of 6), and worse if Towns goes at #11 as he did against the cast. On last season's lines neither man belongs in the first two picks: taking both is the weakest outcome, and the #10 card is Maxey.

## Watchlist

- The WO-5 refresh: the first-round pick rests on it (§2).
- Haliburton's ankle (day-to-day, a 10/13 estimate on ESPN's feed) and the first-season-back tag.
- Seat 11 (Cayas) and seat 12 (Hegi) between your #10 and #15.

## Open-item receipts

| item | query run (2026-10-12) | dated finding |
|---|---|---|
| (this analysis) | machine replay only — no web research in this report | pull receipts for the window live in `after-report-2026-10-12.md` (the morning's pull), same day |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (after-report-2026-10-12.md, receipts dated 10/12) | all HELD or unsigned on 2026-10-12; nothing changed since |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 ca032b2697c5), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 25 of 25 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-12.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-06.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 5 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| PJ Washington | 20 of 25 | 87 | 155 | 178 | 144 | 141 | 121 | ast 2.4 vs 1.9-2; tov 1.5 vs 1.7-1.8; fg_pct .470 vs .448-.451; ft_pct .750 vs .698-.703 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Payton Pritchard | 19 of 25 | 37 | 85 | 33 | 90 | 92 | 72 | stl 1 vs 0.7-0.8; tpm 3.8 vs 3-3.2; tov 2 vs 1.3-1.3; ft_pct .850 vs .873-.875 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 18 of 25 | 28 | 64 | 60 | 56 | 43 | 44 | pts 18.5 vs 16.4-17; ast 2.3 vs 2.1-2.1; ft_pct .805 vs .813-.819 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Sandro Mamukelashvili | 17 of 25 | 81 | 169 | 138 | 105 | 153 | 120 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Daniel Gafford | 11 of 25 | 90 | 180 | 188 | 181 | 161 | 155 | pts 10.5 vs 9.1-9.8; reb 7.5 vs 5.8-6.5; ast 1.5 vs 1.1-1.2; blk 1.7 vs 1.2-1.4; fg_pct .700 vs .648-.689; ft_pct .700 vs .671-.687 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Jalen Suggs | 11 of 25 | 59 | 105 | 89 | 54 | 84 | 99 | pts 17 vs 14.1-15.1; ast 4 vs 4.8-5 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 11 of 25 | 82 | 141 | 94 | 121 | 137 | 98 | reb 7.5 vs 5.5-6.9; tpm 0.9 vs 1.2-1.3; fg_pct .520 vs .447-.498; ft_pct .740 vs .765-.828 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Isaiah Hartenstein | 9 of 25 | 75 | 104 | 141 | 92 | 100 | 102 | pts 11.5 vs 9.1-10.5; reb 11 vs 9.2-10.3; fg_pct .585 vs .597-.611; ft_pct .680 vs .642-.656 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 7 of 25 | 89 | 138 | 122 | 131 | 125 | 123 | pts 16.8 vs 13.4-15.1; tov 1.5 vs 1-1.2; fg_pct .465 vs .432-.443 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Zach LaVine | 7 of 25 | 56 | 99 | 162 | 68 | 77 | 118 | pts 22.5 vs 17-21.1; reb 4.5 vs 3.1-3.6; ast 4 vs 2.8-3.4; tov 2.6 vs 2-2.4 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Josh Hart | 6 of 25 | 67 | 95 | 68 | 84 | 91 | 94 | pts 13.5 vs 11.9-12.2; tpm 1 vs 1.2-1.5; fg_pct .520 vs .498-.503; ft_pct .780 vs .751-.759 | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Anthony Davis | 5 of 25 | 5 | 42 | 36 | 26 | 28 | 31 | pts 24 vs 19.8-22; reb 11.8 vs 9.8-10.6; ast 3.4 vs 2.8-3.1; blk 2.1 vs 1.7-1.9; tpm 0.9 vs 0.5-0.6 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Coby White | 5 of 25 | 58 | 89 | 106 | 86 | 76 | 77 | ft_pct .900 vs .843-.864 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Dyson Daniels | 5 of 25 | 11 | 62 | 20 | 64 | 56 | 53 | pts 14.5 vs 11.3-11.8; stl 3 vs 2-2.4; tpm 1.1 vs 0.5-0.6; fg_pct .495 vs .501-.513 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Herbert Jones | 5 of 25 | 74 | 182 | 147 | 169 | 134 | >250 | — | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Saddiq Bey | 5 of 25 | 95 | 175 | 109 | 132 | 169 | 143 | blk 0.4 vs 0.1-0.1; tpm 2.4 vs 1.8-2; tov 1.5 vs 0.8-0.9 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Karl-Anthony Towns (20 mocks, value 6, market 15); Jalen Williams (16 mocks, value 16, market 40); Derrick White (14 mocks, value 24, market 45); Jalen Johnson (6 mocks, value 13, market 11); Mikal Bridges (6 mocks, value 61, market 84).

Unchanged since the mock-75 report: the same page (v59) and the same 25 mocks; the gate re-runs the check on this file.

## Bounds

- Pairwise swaps hold every other seat's picks; in mock 51 the Towns path's #15 is the owner's own #10 (Edwards), who would likely not last (the README gives the means without it).
- The 2025-26 sensitivity is last season's per-game line, not a projection: no minutes forecast, no shrinkage toward career. It bounds how far the first round moves; WO-5 sets where it lands.
- The cast's early Towns picks lean on the deck's own value axis in rounds 1–6 (Towns rank 6); the real seat 11 drafts on its own board.
- Title odds are against the league's real bracket with each room's twelve rosters, practice rooms against strangers or the cast — not a forecast of Wednesday.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-1012-3 | The #10 pick rests on a 2024-25 Towns line; on his 2025-26 line the card's #1 at #10 is Maxey. Options: (a) draft from the card as shipped; (b) run the owed WO-5 refresh before Wednesday (every top-150 line from 2025-26 per-36 and the preseason role, both planes, rebuild, chain, publish); (c) the same method on the rounds-1-to-3 band only (the top 40 of either board) Tuesday | (a) — WO-5 needs your go; my recommendation is (c) at least |
| D-1012-4 | Haliburton at #10 and Towns at #15. Options: (a) no — follow the card at #10; (b) yes; (c) clear Haliburton's first-season-back tag (he becomes the card's #1 at #10 on the shipped lines) | (a) |
| D75-1, D-1012-2, D-1012-1, D-1011-4, D74-1, D-1011-1..3, D-1010-2, D-1010-1, D-RN-6, D73-1 and earlier | carried | carried |

## Provenance

- Inputs: the saved card replays (`arena/results/m*_deckcard_*.json`), the committed room states 51–75, `arena/results/actuals_2026-10-09/actuals_2025-26.csv` and `actuals_2024-25.csv`, the owner's PDF (md5 `c4b313cfcda34071ece4cefe99e9049a`, raw text `report/market/hashtag-final-9cat-2025-26-raw-2026-10-12.txt`), the league's 2025-26 draft and pre-draft ranks in the deck repo.
- Scripts: `arena/mocks/whatif_hk*.py` (deck); every figure from `arena/results/whatif_hk_2026-10-12/`.
- Not verified: nothing here rests on web research.

## In plain language

**Why Towns.** The card picks the man who leads on both of its halves: what he is worth over a season and how many categories he adds to your week. On the board's numbers that is Towns, a center who also hits threes and free throws: second on each measure, and nobody else is near the top of both. Haliburton's line is actually the best of the four, but the board discounts him for his first season back from the Achilles tear.

**The catch.** The board's Towns numbers are his 2024-25 season. Last season he played fewer minutes and scored about four points a game less. Your PDF and our own records show the same numbers. On last season's numbers the card would not take Towns at #10. It would take Maxey, and Towns would be 26th on that card. Most of the top of the board has the same problem. The refresh that fixes it, the WO-5 pass, has not run.

**Haliburton first, Towns at #15.** On the current numbers, no: the card's order is better in all three survival readings, because if Haliburton is gone at #15 the card has a guard nearly as good, while if Towns is gone there is no second Towns. If you trust Haliburton's health fully, it becomes a good move as long as Towns lasts to #15, which he did in all six human rooms where you passed on him. On last season's numbers, though, neither of them should be your first two picks.

**Your decisions.** D-1012-3: let me run the refresh before Wednesday (default: draft from the card as it is; I recommend at least the top-40 version). D-1012-4: Haliburton first (default no). Everything earlier is carried.
