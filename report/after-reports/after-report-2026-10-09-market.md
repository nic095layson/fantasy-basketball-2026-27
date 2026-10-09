# After-report — 2026-10-09 (market and data): the Hashtag ADP of 10/9 and four seasons of verified actual lines

**Owner request (2026-10-09, verbatim):** "Finish the chain. Before merging and publishing PRs, is there any missing or
supplemental data that you need to complete this fine tuning? Whether it be from the past 3 seasons, or any data — please
pull from internet to ensure you have the more pristine and dialed in computation. If you search and pull from the
internet, ensure that data is accurate and you have at least 2, preferably 3 corresponding data sets before implementing
to your system and record." And, with the upload `Hashtag_ADP_10.9.26.pdf`: "I verified that Hashtag compiles the most
up-to-date ADP from Yahoo system, for 9-cat rankings for 26-27 season."

Pull window: 2026-10-09 → 2026-10-09 — not a roster pull: the day's pull is `after-report-2026-10-09.md` (deck v52) and
the audit's fixes are `after-report-2026-10-09-fixes.md`. This report records (a) the data-gap assessment and the
four-season actuals intake it led to, (b) what that record says about the computation, and (c) the 10/9 ADP refresh
and the deck it rebuilt (v53, the published page). No projection line moved; Sunday's WO-5 pass keeps that work.
Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07`, exit 0.

**Method.** Internet pulls into a fresh untrusted directory, parsed as data with `python3 -I`; every number below is a
script's output on a committed record; two independent outlets per row or the row is not recorded; two runs of every
derivation, byte-identical; the owner's upload read with pdfplumber (parser output is the raw layer).

## 1. Roster changes

None — not a pull. The pool on both planes is byte-identical to the morning's (deck pool `dc9a6d9fd75a`).

## 2. The data-gap assessment

What the fine-tuning lacked before today: the backtest behind D-1009-1..4 rested on one out-of-sample season whose
actual lines came from a single outlet (Basketball-Reference, 2024-25 and 2025-26, raw pages never pinned), and the
range check reads that same single-source file. Nothing recorded whether steals' unpredictability is structural, and the
post-draft availability model had no games record to fit on.

What the network allows: 25 hosts probed. Two serve season stat lines — Basketball-Reference (per-game pages, 2022-23 to
2025-26) and ESPN (the per-athlete season statistics API, unrounded per-game lines with games, attempts, makes and
turnovers). nba.com's page and StatDunk answer with no stat table (both render their tables in the browser from an
origin the gateway refuses); hashtagbasketball.com answers but carries no historical lines. Seventeen hosts refuse at
the gateway with 403 CONNECT: stats.nba.com, cdn.nba.com, data.nba.com, basketball.realgm.com, nbastuffer, CBS,
landofbasketball, Fox, StatMuse, FantasyPros, Proballers, sports.yahoo.com, HoopsHype, RotoWire, Sofascore, Wikipedia,
NBC. So the record below is **two corresponding outlets, not three**; the third the owner preferred is reported as not
reachable, with that receipt. The owner's Rotoworld kit carries 2025-26 columns but is a derivative of the same league
data and was not counted as an outlet.

Other data judged and not pulled: the 2026-27 schedule (a weekly-games model would change the card's ΔECW half — a
method change for the owner's sheet, not a data fill); third-party projections (five sets already on file; Hashtag's
10/9 page shows no line moved since 10/6 — §5); injury feeds (the daily pull's work).

## 3. The actuals intake (two outlets, four seasons)

| step | result |
|---|---|
| fetch | 4 Basketball-Reference pages + 48 ESPN pages, all HTTP 200, each pinned by sha256, bytes and UTC time in `raw_manifest.tsv` (the raw pages stay out of the repo; `arena/mocks/actuals_1009/fetch_all.sh` re-pulls into a fresh directory) |
| extract | Basketball-Reference 541 / 572 / 569 / 582 players (2022-23 … 2025-26; the first row per player is the season total, the League Average row dropped); ESPN 539 / 572 / 569 / 582 (athlete count equals each season's `pagination.count`, ids unique) |
| name join | every ESPN name matched (fold; then surname + first three letters for 2 / 1 / 3 names; one token-order case, Cui Yongxi); the two Basketball-Reference-only names are 2022-23 stints of 2 and 6 games ESPN omits |
| cross-check | games exact; counting fields within 0.05 per game; percentages within 0.0005; minutes informational; a blank percentage with zero attempts equals ESPN's zero |
| recorded | 536 / 570 / 569 / 582 players (`actuals_<season>.csv`, ESPN's unrounded values, Basketball-Reference's spelling and team) — clean 533 / 568 / 567 / 581, noted 3 / 2 / 2 / 1 (one cell off by 0.1 or less, named in the row: 2025-26 Jabari Smith Jr. FGA 12.6 vs 12.66) |
| conflicts (excluded, listed) | 2022-23: Brandon Clarke FT% .723 vs .719 and FTA 2.4 vs 2.48, LaMelo Ball FT% .836 vs .843, Tyus Jones FT% .800 vs .806 and FTA 1.3 vs 1.23; 2023-24: Isaiah Jackson games 59 vs 60, Tristan Thompson FG% .608 vs .614; 2024-25 and 2025-26: none |
| the 10/08 files | the fresh Basketball-Reference pull reproduces `tuning_2026-10-08/bref_pergame_2024-25.csv` and `_2025-26.csv` field for field (569 and 582 rows; only the League Average row differs), so the range check's reference and the backtest's inputs are now two-outlet verified |
| reproducibility | `extract_actuals.py`, `crosscheck.py`, `analyze_actuals.py` re-run from the raw pages into a temporary directory: 24 files byte-identical to the record |

## 4. What the record says

**Year-over-year stability** (Spearman ρ of a player's per-game value across consecutive seasons, 25+ games in both):

| category | 2022-23 to 2023-24 (n 336) | 2023-24 to 2024-25 (n 332) | 2024-25 to 2025-26 (n 335) | mean |
|---|---|---|---|---|
| FG% | .746 | .736 | .659 | .714 |
| FT% | .654 | .651 | .598 | .634 |
| 3PM | .885 | .899 | .831 | .872 |
| PTS | .868 | .882 | .795 | .848 |
| REB | .852 | .876 | .792 | .840 |
| AST | .870 | .860 | .810 | .847 |
| STL | .803 | .765 | .681 | .750 |
| BLK | .834 | .828 | .793 | .818 |
| TO | .845 | .855 | .768 | .823 |

Steals are the least stable counting category in each of the three transitions, blocks the next; the finding behind
D-1009-4 is structural, not a one-season effect. Last season's transition was the noisiest of the three in every
category.

**The three-season line as a forecast** (the 2025-26 entering pool, 189 of 220 rows scored against the verified actual
with 25+ games; 11 rows had no prior line). Arms: ENTERING = our line entering 2025-26; PRIOR = the 2024-25 actual;
M3 = games-weighted 5/4/3 over 2024-25, 2023-24, 2022-23; BLEND = half ENTERING, half M3.

| category | ENTERING mae / ρ | PRIOR mae / ρ | M3 mae / ρ | BLEND mae / ρ |
|---|---|---|---|---|
| FG% | .0272 / .790 | .0279 / .751 | .0274 / .770 | .0256 / .792 |
| FT% | .0435 / .733 | .0496 / .692 | .0402 / .765 | .0401 / .775 |
| 3PM | .368 / .803 | .418 / .771 | .401 / .762 | .363 / .793 |
| PTS | 2.78 / .836 | 3.11 / .778 | 3.07 / .766 | 2.74 / .811 |
| REB | .848 / .911 | .884 / .875 | .897 / .874 | .794 / .902 |
| AST | .724 / .884 | .755 / .853 | .809 / .835 | .717 / .876 |
| STL | .224 / .720 | .232 / .666 | .206 / .684 | .205 / .734 |
| BLK | .174 / .856 | .172 / .842 | .166 / .867 | .163 / .874 |
| TO | .406 / .814 | .422 / .757 | .416 / .748 | .384 / .799 |

PRIOR beats ENTERING in 1 category of 9 on error, M3 in 3 (FT%, steals, blocks), BLEND in 9 of 9 on error but with
lower rank correlation in 3PM, points, rebounds, assists and turnovers — the blend trims big misses by pulling toward
the past and pays for it in ordering where our lines already order well. **Departures** (where ENTERING sat half a
category SD or more from PRIOR): steals n 39 — ENTERING closer than PRIOR 21, M3 closer than ENTERING 24, BLEND 27;
blocks n 13 — 3 / 9 / 9; points n 20 — 13 / 8 / 9; rebounds n 18 — 11 / 7 / 12; assists n 15 — 9 / 7 / 10. Where we
depart from a player's history in steals and blocks, the history was right more often; in points, rebounds and assists
our departures were right. That is the rule WO-5 item (8) now carries (D-1009-6).

**Games history** (`gp_history_2026-27.csv`): 252 of the 335 deck rows carry three seasons, 46 two, 24 one, 13 none
(rookies); the three-season players' mean fraction of 82 games is .738 (the flat multiplier is .78), and 108 of the 252
average under 60 games — the spread the post-draft per-player model is for.

**The points identity on actual lines:** on ESPN's unrounded lines pts = 2·FGM + 3PM + FTM to 0.0002; pushed through
the check's own formula on Basketball-Reference's rounded cells (FG% × FGA, FT% × FTA) the largest gap among 432
players with 25+ games is 0.164 (p95 0.108, none above 0.5). A gap above the 1.0 threshold is never rounding
(D-1009-5, evidence).

## 5. The 10/9 ADP (owner upload) and the deck it rebuilt

| item | result |
|---|---|
| the page | Hashtag "Fantasy Basketball Projections", updated 09 October 2026, Top 200, positions and ADP from Yahoo; ten pages, 238 lines, 200 projection rows, parsed by `hashtag_pdf_market.py 2026-10-09` (TRANSCRIPTION GATE PASS; two runs identical); 199 of 200 names join the pool (Yanic Konan Niederhauser, LAC rookie, is Hashtag-only) |
| ADP vs the 10/6 Yahoo paste | 169 comparable names: mean move 0.42 places, median 0.3, largest 2.1 (Brandon Ingram 67.1 to 69.2, Cam Johnson 112.5 to 114.5, Ausar Thompson 83.7 to 82.0); none of 5 or more; 30 page names carry no ADP; positions identical on all 199 |
| Hashtag's lines vs 10/6 | no per-game cell moved on any of the 200 rows; 195 rows' TOTAL recalculated by ±0.02 and one games cell changed — Sunday's outside median is unchanged |
| the price file | `yahoo-2026-10-09.csv` by `report/market/adp_refresh.py` (registered; derived gate 19 of 19): the 10/6 paste's 250 rows with 170 ADPs replaced from the page, 80 keeping the 10/6 ADP (65 of them XRank-only), XRank unchanged; one row gains an ADP it lacked (Scotty Pippen Jr.) |
| the deck | rebuilt on the new file: priced 246 of 335 (same count; 184 by ADP, 62 by XRank — before 183 / 63), prices changed on 151 rows, market-rank order changed for 126 rows; Pippen Jr. moves from XRank 197 to ADP rank 140 (the largest shift, 57 places), every other shift 11 places or fewer (Cam Johnson 130 to 141, Ingram 64 to 70); no pool row, line or placement changed; the colophon's market sentence names the 10/9 file |

## 6. Gates (2026-10-09, market and data)

| gate | result |
|---|---|
| kit `report/check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07; exit 0 |
| kit `report/check_derived.py` | DERIVED: all 19 dated artifacts reproduce byte-for-byte from their pinned inputs (the two new ones at pins 710f7f1 and 73a5572); exit 0 |
| deck `scripts/build_deck.py` | gates 1–7 + F8 pass, no waiver; market `yahoo-2026-10-09.csv` priced 246/335, 0 days old; pool `dc9a6d9fd75a` identical to v52; freshness restamped `--no-pool-changes`; injection round-trip OK; "safe to publish" |
| deck `scripts/check_parity.py` | PARITY: EXACT MATCH — 364 owner turns across 28 committed states; market ranks 318 (priced 240); exit 0 |
| deck `test_card.py` / `test_gates.py` / `test_draft.py` | CARD: all 99 cases passed; all 52 cases passed; all 65 cases passed; exit 0 each |
| deck `arena/mocks/full_dom_check.mjs` | 143 assertions, 0 failed, 0 page errors, pass: true (`arena/results/full_dom_check_2026-10-09_v53.json`) |
| deck `scripts/repeat_market_check.py` | 21 of 21 mocks replayed; 12 FLAGGED, 5 near misses — the v52 set, verdicts unchanged, eight market ranks moved one to three places; the 🎯 identical at all 273 owner turns (`arena/results/repeat_market_check_2026-10-09_v53.json`) |
| deck actuals record | second run from the raw pages byte-identical (24 files); cross-check summary and analysis summary committed |
| kit `report/check_report.py` | REPORT GATE: PASS (structure, publication rule, pull-log row); exit 0 |
| deck `judgment_open_items.py --check-report` | receipts check PASS — all 10 flagged names carry a receipts row; exit 0 |
| deck `repeat_market_check.py --check-report` | REPEAT-NAME CHECK: PASS — 12 flagged names, each with a row (21 of 21 mocks replayed on the v53 page); exit 0 |
| artifact publish | Version 53 (version id 1791570495-d551) at the standing URL after a fresh read of the live version (1791555525-2e7a, the v52 publish); the page's sha256 8978f6cde216, the file committed as deck 1c97b7e |

## 7. Watchlist / open items

- **WO-5, 10/11 pass** — item (8) applies: steals and blocks anchored to the three-season line, departing only with two
  outlets on the departing side; items (5)–(7) as written; `range_check.py` and `identity_check.py --check-report`.
- **10/14 lock** — the owner's fresh Yahoo paste replaces `yahoo-2026-10-09.csv` as the price file (WO-4); until then
  this file stands (D-1009-8).
- **After the draft** — the per-player expected-games model now has its games record; D-RN-4; the BLEND finding (D-1009-7)
  is a candidate for that pass, not a rule.
- Everything carried from `after-report-2026-10-09.md` §10 and the fixes report §7 stands.

## 8. Before and after on the last 15 rooms (owner's request)

**Instrument.** `arena/mocks/live_retro.py` gained a `regrade` stage (two arms, 6,000 seasons × 3 seeds each: the roster as
drafted; the roster the card would have built, self-consistent) with `--rev` choosing the page whose prices the card
sees. Each of mocks 57–71 was graded on today's pool (`players_v53.csv`, byte-identical to v52's) twice — with the v52
page's prices (rev 4024ddb) and with the v53 page's (rev 1c97b7e) — and the card's 🎯 at every owner turn recorded under
both. Beside them, the room's own record (`m<NN>_arms.json`, the page and pool it was drafted on). The real page was also
replayed in the browser for the 21 recorded rooms by the repeat-name check on both versions.

**Result.** Title odds are identical to the third decimal in all 15 rooms under the two price pages; the card's 🎯 is the
same name at all 195 owner turns of the 15 rooms and at all 273 owner turns of the 21 rooms on the real pages
(v52 `d44734abf093` vs v53 `8978f6cde216`); no follow-card chain changed; the mean follow-card title odds are 31.6% on both.
The "recorded" column differs from "today's pool" in most rooms — that is the two weeks of pool work since those rooms
were drafted (the WO-1/WO-2 re-derivation, the exclusions, the role passes), not today's. Today's changes to the deck are
words, a check, and prices that moved the market order by a few places for 126 names; none of it reaches the engine's
valuation of any player, and the market moves were too small to change a single recommendation in 15 rooms.

| room | recorded (its own page, its pool): as drafted / follow the card | today's pool, v52 prices: as drafted / follow the card | today's pool, v53 prices: as drafted / follow the card | 🎯 turns that differ (v52 vs v53) | follow-card chain |
|---|---|---|---|---|---|
| mock 57 | 27.44% / 41.43% | 13.21% / 38.18% | 13.21% / 38.18% | 0 of 13 | identical |
| mock 58 | 36.75% / 40.89% | 22.63% / 38.51% | 22.63% / 38.51% | 0 of 13 | identical |
| mock 59 | 20.38% / 39.18% | 14.95% / 36.67% | 14.95% / 36.67% | 0 of 13 | identical |
| mock 60 | 33.02% / 43.14% | 33.73% / 41.39% | 33.73% / 41.39% | 0 of 13 | identical |
| mock 61 | 16.66% / 34.49% | 16.60% / 34.99% | 16.60% / 34.99% | 0 of 13 | identical |
| mock 62 | 18.05% / 18.22% | 18.29% / 17.44% | 18.29% / 17.44% | 0 of 13 | identical |
| mock 63 | 23.33% / 23.33% | 24.06% / 25.04% | 24.06% / 25.04% | 0 of 13 | identical |
| mock 64 | 7.63% / 18.97% | 9.71% / 22.51% | 9.71% / 22.51% | 0 of 13 | identical |
| mock 65 | 23.19% / 23.19% | 25.29% / 25.29% | 25.29% / 25.29% | 0 of 13 | identical |
| mock 66 | 20.16% / 34.93% | 20.34% / 34.43% | 20.34% / 34.43% | 0 of 13 | identical |
| mock 67 | 17.51% / 37.51% | 18.48% / 38.86% | 18.48% / 38.86% | 0 of 13 | identical |
| mock 68 | 28.36% / 35.00% | 29.39% / 36.39% | 29.39% / 36.39% | 0 of 13 | identical |
| mock 69 | 27.51% / 26.58% | 27.69% / 26.70% | 27.69% / 26.70% | 0 of 13 | identical |
| mock 70 | 20.68% / 30.77% | 20.46% / 30.64% | 20.46% / 30.64% | 0 of 13 | identical |
| mock 71 | 3.48% / 27.13% | 3.58% / 26.96% | 3.58% / 26.96% | 0 of 13 | identical |

Record: `arena/results/regrade_2026-10-09.json` and the 30 `m<NN>_regrade_v52prices.json` / `_v53prices.json` files
(deck). The kit board's own before/after is §4 of the fixes report: six rows left the top 200, the top 60 unmoved.

## Open-item receipts

| player | query run (2026-10-09) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (`after-report-2026-10-09.md`, receipts dated 10/9) | all HELD or unsigned on 2026-10-09; this report did no roster research |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 8978f6cde216), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 21 of 21 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-09.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-06.csv`, `hashtag-2026-10-09.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| PJ Washington | 17 of 21 | 87 | 151 | 178 | 144 | 141 | 121 | ast 2.4 vs 1.9-2; tov 1.5 vs 1.7-1.8; fg_pct .470 vs .448-.451; ft_pct .750 vs .698-.703 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Payton Pritchard | 16 of 21 | 37 | 83 | 33 | 90 | 92 | 72 | stl 1 vs 0.7-0.8; tpm 3.8 vs 3-3.2; tov 2 vs 1.3-1.3; ft_pct .850 vs .873-.875 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 15 of 21 | 28 | 65 | 60 | 56 | 43 | 44 | pts 18.5 vs 16.4-17; ast 2.3 vs 2.1-2.1; ft_pct .805 vs .813-.819 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Sandro Mamukelashvili | 15 of 21 | 81 | 169 | 138 | 105 | 153 | 120 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Daniel Gafford | 10 of 21 | 90 | 181 | 188 | 180 | 161 | 155 | pts 10.5 vs 9.1-9.8; reb 7.5 vs 5.8-6.5; ast 1.5 vs 1.1-1.2; blk 1.7 vs 1.2-1.4; fg_pct .700 vs .648-.689; ft_pct .700 vs .671-.687 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Jalen Suggs | 10 of 21 | 59 | 105 | 89 | 54 | 84 | 99 | pts 17 vs 14.1-15.1; ast 4 vs 4.8-5 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 9 of 21 | 82 | 144 | 94 | 121 | 137 | 98 | reb 7.5 vs 5.5-6.9; tpm 0.9 vs 1.2-1.3; fg_pct .520 vs .447-.498; ft_pct .740 vs .765-.828 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Isaiah Hartenstein | 7 of 21 | 75 | 104 | 141 | 92 | 100 | 102 | pts 11.5 vs 9.1-10.5; reb 11 vs 9.2-10.3; fg_pct .585 vs .597-.611; ft_pct .680 vs .642-.656 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Zach LaVine | 6 of 21 | 56 | 100 | 162 | 68 | 77 | 118 | pts 22.5 vs 17-21.1; reb 4.5 vs 3.1-3.6; ast 4 vs 2.8-3.4; tov 2.6 vs 2-2.4 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 5 of 21 | 89 | 142 | 122 | 131 | 125 | 123 | pts 16.8 vs 13.4-15.1; tov 1.5 vs 1-1.2; fg_pct .465 vs .432-.443 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Dyson Daniels | 5 of 21 | 11 | 62 | 20 | 64 | 56 | 53 | pts 14.5 vs 11.3-11.8; stl 3 vs 2-2.4; tpm 1.1 vs 0.5-0.6; fg_pct .495 vs .501-.513 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Saddiq Bey | 5 of 21 | 95 | 176 | 109 | 132 | 169 | 143 | blk 0.4 vs 0.1-0.1; tpm 2.4 vs 1.8-2; tov 1.5 vs 0.8-0.9 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Karl-Anthony Towns (16 mocks, value 6, market 15); Jalen Williams (15 mocks, value 16, market 39); Derrick White (11 mocks, value 24, market 44); Jalen Johnson (6 mocks, value 13, market 11); Mikal Bridges (6 mocks, value 61, market 82).

On the re-priced page the twelve flagged names and their verdicts are the v52 set; eight market ranks moved by one to three places (Suggs 108 to 105, Washington 148 to 151, Bey 174 to 176, LaVine 101 to 100, Gafford, Vassell, Pritchard, Lendeborg by one), none across the 25-place rule. The card's 🎯 at all 273 owner turns of the 21 rooms is the same name on both pages (`arena/results/repeat_market_check_2026-10-09.json` vs `_v53.json`).

## Bounds

- Two outlets, not three: every stat site beyond Basketball-Reference and ESPN is refused at this environment's
  gateway (§2). Where the two disagree the row is excluded (5 players) or noted (8 cells); nothing was adjudicated.
- One out-of-sample season still carries the forecasting comparison (§4's second table); the stability table is three
  transitions and is the stronger claim.
- The three-season line is games-weighted 5/4/3; other weightings were not tried.
- The 10/9 ADP is Yahoo's as compiled by Hashtag (the owner's verification); 80 of the 250 priced names keep a 10/6 ADP.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-1009-6 | WO-5 anchor for steals and blocks: (a) the player's three-season line (`baseline3_2026-27.csv`), departures only with two outlets on the departing side — written into item (8); (b) keep the outside-median method for every category | (a) — the record (§4: M3 closer 24 of 39 in steals, 9 of 13 in blocks) |
| D-1009-7 | the half-and-half blend of our line and the three-season line, which cut error in 9 of 9 categories last season but ordered worse in five: (a) a candidate for the post-draft pass, measured on a second season first; (b) apply on Sunday to FT%, steals and blocks only; (c) apply to every category | (a) — not applied |
| D-1009-8 | the price file until the lock: (a) `yahoo-2026-10-09.csv` (the 10/6 paste re-priced from the page) stands until the owner's 10/14 Yahoo paste; (b) revert to the 10/6 paste | (a) |
| D-1009-5 (evidence) | the identity threshold: rounding on actual lines reaches 0.164 at most, so 1.0 is six times the noise floor; the default (keep 1.0) stands | (a) 1.0 |

## Provenance and bounds

- Inputs: the owner's `Hashtag_ADP_10.9.26.pdf` (raw layer `report/market/hashtag-raw-2026-10-09.txt`); the 52 fetched pages
  (pinned in `arena/results/actuals_2026-10-09/raw_manifest.tsv`); `arena/data/players_2025-10-21.csv`; `data/players.csv`;
  `report/market/yahoo-2026-10-06.csv`.
- Records: `arena/results/actuals_2026-10-09/` (24 files), `report/market/hashtag-2026-10-09.csv`, `yahoo-2026-10-09.csv`,
  `adp-refresh-2026-10-09.md`, `unmatched-hashtag-2026-10-09.md`; the market-rank comparison `arena/results/market_rank_moves_2026-10-09.json`.
- Every number in §3, §4 and §5 is a script's output; every gate line is the command's own output.

## In plain language

**What you asked.** Whether any data was missing for the fine-tuning, and to pull it from the internet with at least two
matching sources before it touches the system. Plus your Hashtag upload with the current Yahoo ADP.

**What was missing, and what I pulled.** The system's view of "what actually happened last season" came from one website,
for two seasons, never cross-checked. I pulled four seasons (2022-23 through 2025-26) from two independent sites —
Basketball-Reference and ESPN — and compared every player, every stat. They match for essentially everyone: 2,257 player-
seasons recorded, five excluded because the two sites disagree (small free-throw and games differences on older seasons),
eight more carrying a note about a single cell. Every other stat site I tried is blocked by this environment's network
policy, so it is two sources, not three; I'm saying that plainly rather than papering over it.

**What the data changed.** Three things, all on the record: (1) steals really are the hardest category to project — not a
one-year fluke; blocks are next. (2) When our projections departed from a player's own multi-year history in steals and
blocks, the history was right more often than we were; in points, rebounds and assists, we were right. So Sunday's
refresh anchors steals and blocks to each player's three-season line and only departs with two sources behind the
departure. (3) The per-player games history is now on file for the post-draft availability model.

**The ADP.** Your Hashtag page carries Yahoo's ADP as of 10/9. It is the 10/6 prices with small drift (the biggest move
is two places). I rebuilt the draft board on it; the market ranks shift by a few places for about 126 players, and one
(Scotty Pippen Jr.) gains a real ADP where he had only a rank before. The 10/14 lock paste replaces it.

**Did the dialing-in change anything in the last 15 drafts?** No — and that is the right answer. I re-graded all 15 rooms
(mocks 57 to 71) on today's board twice, once with last week's prices and once with the 10/9 prices: identical title odds in
every room, the same recommended pick at every one of the 195 turns you had, and the same pick at all 273 turns across the
21 recorded rooms when the real page is replayed in a browser. Today's work was never meant to move the board: the audit
proved the math exact, the fixes were a kit-board cleanup, honest wording, a new check, and a price refresh that shifted
most names by a place or two. What will move numbers is Sunday's projection pass — and it now has four seasons of verified
history, the steals-and-blocks rule, and the identity check to keep it honest.

**Verification.** The four seasons of actual lines were accepted only where two independent sites match row by row (the differences are listed, not hidden), and every derived file reproduces byte-for-byte on a second run from the raw pages; the Hashtag page was parsed by the same registered script as the 9/30 and 10/6 pages (two runs identical) and both new price artifacts carry commit pins (derived gate 19 of 19); the re-priced deck passed the full chain — parity exact at 364 turns, 99/52/65 cases, 143 browser assertions, the 21-mock replay with the card's pick unchanged at every one of 273 owner turns — and was published after a fresh read of the live version. The before/after re-grade of the last 15 rooms is in §8.

**Your decisions.** D-1009-6 (steals/blocks anchor — default yes), D-1009-7 (the blend — default: not yet), D-1009-8
(this price file until the lock — default yes).
