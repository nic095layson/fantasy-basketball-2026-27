# After-report — the dial pass of 10/13: 24 lines clamped inside the three outside projections' range (D-1013-6), Version 65

**Owner requests (2026-10-13, verbatim):** "Invoke the council on how to proceed. and I'd like for you to conduct as logical dialing as as we can. What can we solve / strengthen today? Let's take meaningful and intentional steps to dial this in." After the environment's permission check paused the pass: "Rebuild the kit board and the draft-deck page, then run the full chain. Compare the card’s 🎯 at your 13 picks before and after. Write the report, merge both PRs, and publish Version 65."

**What was analyzed and changed:** kit `main` 7c28bb3 and deck `main` f6fb476 (Version 64, page sha256 a88d83f4e2f8) as the starting point. The selection record: `usage-2026-10-13/range_check_no_actual.json`, the deck's own range check run without the player's last season as a reference. The references: Yahoo `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, RotoBaller `rotoballer-2026-09-29.csv`.

**Method:** the Council (4–1; the Contrarian wanted the high lines at the consensus average, not the edge) chose to clamp the material outliers to the edge of the outside range. Stated to the owner before the run: A6 the per-category range of the three projections; A7 every line whose cells outside that range carry more than 0.5 z, either way, on Version 64, plus Philadelphia's other three for the team budget; A8 each cell outside the range moves to the nearest edge, rounded inward, other cells stay, games, minutes, tags and placements stay; A9 FGA and FTA rescale by one factor when points, threes or a percentage moved, so points still follow from the shooting. Tools in `report/dial/tools/`: `dial_lines.py` computes the lines and writes nothing (two runs identical); `dial_apply.py` writes both planes with assertions A1–A9 (A8 recomputes the range from the deck's own loader; three planted errors caught; a second run changes nothing); `dial_page.py` re-words the colophon and adds seven card receipts; `board_diff.py`, `card_compare.py`, `chain_dial.sh` and this writer read the records.

Pull window: 2026-10-13 → 2026-10-13 (no roster pull; the morning's verified pool, stat lines only).

**Headline.** 24 lines now sit inside the range of Yahoo, Hashtag and RotoBaller in every category: 13 that were too high, 8 that were too low and Philadelphia's other three. 104 values moved, with shot attempts rescaled on 22 lines so the points identity holds. Every gate and every test of the chain passed on the rebuilt page, and Version 65 is live, byte-verified. The card's 🎯 changes at 51 of your 325 replayed turns. Without last season as a reference, 80 lines still have a category outside all three projections, down from 102, and none of them is one of the 24. Philadelphia's pool still claims more possessions than any team used last season: 121.4 against 117.7, down from 127.6.

## 1. Roster changes

None. No placement, tag, games or minutes figure changed on either plane; 24 stat lines moved (§2).

## 2. The 24 lines

EVIDENCE: `dial/out/lines_dial_2026-10-13.json`, `apply_record_2026-10-13.json`, `board_diff_2026-10-13.txt`, `val_v65.json` against `live-mock-2026-10-13/val_v64.json`.

| player | side | values moved | kit rank before / after | deck value rank v64 / v65 | market rank |
|---|---|---|---|---|---|
| Tyrese Maxey | high | pts 28.2 to 26.1, reb 4.1 to 3.8, ast 6.6 to 6, TO 2.4 to 2.3 | 5 / 5 | 4 / 5 | 9 |
| Kawhi Leonard | high | pts 27.8 to 24.3, reb 6.4 to 6.1, 3PM 2.6 to 2.3, FT% .882 to .881 | 4 / 6 | 6 / 7 | 32 |
| Lauri Markkanen | high | pts 26.4 to 23.8, ast 2.1 to 1.9, FG% .471 to .463 | 14 / 21 | 11 / 21 | 37 |
| James Harden | high | pts 22.9 to 20.8, blk 0.6 to 0.5, 3PM 3 to 2.7, FG% .435 to .426, FT% .877 to .878 | 18 / 28 | 17 / 28 | 33 |
| Anthony Edwards | low | reb 5 to 5.5, ast 3.7 to 3.6, 3PM 3.4 to 3.5, FT% .798 to .813 | 23 / 15 | 23 / 13 | 7 |
| Ryan Rollins | high | ast 5.6 to 5.5, stl 1.7 to 1.5, blk 0.6 to 0.5, FG% .473 to .475 | 29 / 46 | 28 / 46 | 74 |
| Joel Embiid | Philadelphia budget | pts 25.1 to 24.6, stl 0.7 to 0.6, FG% .493 to .490, FT% .846 to .857 | 36 / 40 | 32 / 35 | 50 |
| Evan Mobley | low | reb 9 to 9.2, TO 1.9 to 2, FG% .546 to .552, FT% .629 to .661 | 50 / 37 | 50 / 38 | 29 |
| VJ Edgecombe | Philadelphia budget | pts 16 to 15.9, FT% .818 to .817 | 58 / 59 | 56 / 58 | 75 |
| Jaylen Brown | high | pts 28.6 to 24, reb 6.9 to 6, ast 5.1 to 4.6, 3PM 2 to 1.9, TO 3.6 to 3.4 | 59 / 91 | 59 / 93 | 30 |
| LeBron James | Philadelphia budget | pts 20.9 to 20.3, 3PM 1.3 to 1.4, FG% .512 to .513, FT% .737 to .752 | 60 / 57 | 60 / 55 | 38 |
| Keyonte George | high | pts 23.1 to 20.3, stl 0.8 to 0.9, FT% .880 to .871 | 70 / 85 | 73 / 86 | 53 |
| Deni Avdija | high | pts 24.1 to 20.7, ast 6.7 to 5.5, TO 3.8 to 3.5, FG% .462 to .469 | 75 / 90 | 76 / 91 | 39 |
| Kristaps Porzingis | low | ast 2.5 to 2.4, blk 1.3 to 1.2, 3PM 1.7 to 1.9, FG% .451 to .467 | 76 / 68 | 77 / 68 | 103 |
| Jrue Holiday | high | pts 16.4 to 12.8, reb 4.6 to 4.2, ast 6.1 to 4.6, blk 0.4 to 0.3, 3PM 2.6 to 2, TO 2.8 to 2.1, FT% .822 to .855 | 88 / 124 | 88 / 127 | 149 |
| Dejounte Murray | low | stl 1.4 to 1.6 | 91 / 74 | 91 / 72 | 64 |
| Andrew Nembhard | high | pts 17.1 to 14.7, reb 2.8 to 2.9, ast 7.7 to 6.8, 3PM 1.9 to 1.5, TO 2.4 to 2.2, FG% .447 to .449, FT% .820 to .819 | 103 / 129 | 101 / 131 | 152 |
| Ausar Thompson | low | pts 9.8 to 10.4, reb 5.7 to 6, stl 1.8 to 2, blk 0.9 to 1, TO 1.5 to 1.6, FT% .580 to .592 | 109 / 78 | 104 / 77 | 81 |
| Pascal Siakam | low | pts 24.2 to 23.2, stl 0.9 to 1, TO 2.2 to 1.9, FG% .488 to .499 | 108 / 77 | 109 / 75 | 49 |
| Daniel Gafford | high | reb 6.9 to 6.5, stl 0.7 to 0.6, blk 1.6 to 1.4 | 115 / 143 | 117 / 143 | 182 |
| Santi Aldama | high | pts 13.9 to 13.2, reb 6.7 to 5.5, blk 0.7 to 0.6, TO 1.3 to 1.2 | 125 / 150 | 124 / 149 | 228 |
| Zach LaVine | low | reb 2.8 to 3.1, ast 2.3 to 2.8, TO 1.9 to 2, FG% .476 to .487, FT% .865 to .859 | 133 / 117 | 133 / 117 | 99 |
| Aaron Gordon | low | pts 16 to 15.7, reb 5.8 to 5.7, ast 2.7 to 2.8, 3PM 1.7 to 1.6, TO 1.1 to 1.2, FG% .493 to .516, FT% .744 to .753 | 137 / 123 | 136 / 124 | 126 |
| Sam Merrill | high | pts 12.5 to 10.8, ast 2.4 to 2.2, 3PM 3 to 2.7, TO 0.8 to 0.7, FG% .449 to .440, FT% .867 to .885 | 142 / 169 | 142 / 168 | 258 |

Everyone else moved only because the 24 did: on the deck 183 of 294 other value ranks change, by at most 6 places; on the kit board 126 of 176, by at most 6. The note behind each of the 24 rows on the page carries the dated clamp entry.

## 3. Checks on the result

| check | result |
|---|---|
| `dial_lines.py` | 24 rows, 104 values clamped, 22 shot rescales, 0 problems; two runs identical |
| `dial_apply.py` (both planes) | PASS: deck 24 rows, kit 24 rows, 290 values across the two planes (on each, 104 category values and 41 shot attempts: FGA on 22 lines, FTA on 19); a second run changes nothing; the written files equal a fresh write from Version 64; three planted errors (a value outside the range, a change beyond the clamp, a broken identity) each caught |
| Kit (`rank_engine.py`, `slate.py`, `test_rank_engine.py`, `check_provenance.py`, `check_derived.py`) | board rebuilt, 200 from 313 projected; 4 tests OK; PROVENANCE GATE PASS; DERIVED 24 of 24 reproduce; the slate also picks up Yahoo's 10/13 ADP, which the 10/13 Yahoo pass had not regenerated into it |
| Deck build (`build_deck.py`, 7 gates) | refused once at gate 4 (the stamp still asserted no pool change from the Yahoo pass; restamped `--pool-changes`), then passed: planes: 315 shared · kit-only 10 · deck-only 20 · team 0 · exclusion 0 · drift 0 · propagation 0; deck built: 335 players · pull 2026-10-13 · pool bd2b983876a8 · injection round-trip OK |
| `check_parity.py` | PARITY: EXACT MATCH; card orderings compared : 416 owner turns across 32 committed states; market ranks compared : 318 (priced 286) |
| `test_card.py` / `test_draft.py` / `test_gates.py` | CARD: all 99 cases passed / all 65 cases passed / all 54 cases passed |
| `full_dom_check.mjs` (on `draft_state_54.json`) | {"assertions":145,"failed":0,"pageErrors":0,"crash":false,"pass":true,"failures":[]} |
| `repeat_market_check.py` | 25 of 25 mocks replayed; 8 FLAGGED, 5 near miss(es) |
| `identity_check.py` | POINTS IDENTITY: 0 player(s), 0 line(s) more than 1 from their own shooting (200 deck and 200 kit lines checked) |
| `range_check.py` (D-RN-3, with last season) | RANGE CHECK: 19 player(s) with 21 cell(s) outside every reference (145 of the top 150 checkable) |

## 4. Residual audit

EVIDENCE: `dial/out/range_no_actual_after.json` (the deck's range check with no last-season file, on the rebuilt lines) against the 10/13 usage report's run; `dial/out/team_budget_after.txt` against `usage-2026-10-13/team_budget.txt`.

| without last season as a reference | Version 64 | Version 65 |
|---|---|---|
| lines with a category outside all three projections | 102 of 139 | 80 of 139 |
| cells outside all three | 214 | 154 |
| z those cells carry, flattering side | 16.55 | 6.22 |
| z those cells carry, unflattering side | -14.04 | -9.20 |
| lines carrying more than 0.5 z either way | 21 | 2 |

- None of the 24 is flagged any more (0 remain). Two other lines now sit just past the 0.5 cut, because moving the 24 shifted every category's mean and spread a little: Aaron Nesmith -0.54, Jamal Murray +0.51. They were under the cut on Version 64; they go to the sheet as D-1013-8 rather than into this pass.
- The team budget: Philadelphia's pool claims 95.1 shots and 121.4 possessions a game, down from 100.3 and 127.6, still above the 2025-26 maximum of 93.3 and 117.7. Teams whose pool exceeds that maximum: 7 before and 6 now; teams over their own 2025-26 total: 10 before and 8 now. The pools now claim 96.4% of last season's league possessions, from 97.2%.

| team | possessions a game, Version 64 | Version 65 | 2025-26 |
|---|---|---|---|
| PHI | 127.6 | 121.4 | 114.2 |
| WAS | 142.2 | 142.2 | 114.8 |
| MIL | 119.1 | 119.0 | 108.4 |
| NOP | 122.2 | 122.2 | 115.2 |
| MEM | 121.5 | 121.5 | 115.3 |
| MIA | 118.1 | 118.1 | 117.4 |
| UTA | 119.7 | 115.7 | 117.2 |
| POR | 111.0 | 104.9 | 117.7 |

## 5. Test 7 — the card at your 13 picks, Version 64 against Version 65

EVIDENCE: `dial/out/card_compare_2026-10-13.txt`, from the deck's repeat-name replays of the same 25 graded mocks on each page (`arena/results/repeat_market_check_2026-10-13_v64.json` and `_v65.json`). One input differs: the page.

```
pages: v64 a88d83f4e2f8 ([51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75] of 25 mocks) / v65 09a889d4baa5 ([51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75] replayed)
turns compared: 325; 🎯 changed: 51
by round (changed / turns): R1 0/25, R2 2/25, R3 6/25, R4 7/25, R5 6/25, R6 6/25, R7 1/25, R8 1/25, R9 2/25, R10 0/25, R11 5/25, R12 14/25, R13 1/25
left the 🎯 most often (v64 name): Jrue Holiday 20 *, Ryan Rollins 15 *, Lauri Markkanen 8 *, Kawhi Leonard 2 *, Yaxel Lendeborg 2, Kel'el Ware 1, Kevin Durant 1, Jalen Suggs 1, James Harden 1 *
took the 🎯 most often (v65 name): Collin Gillespie 9, Kel'el Ware 9, Reed Sheppard 7, Derrick White 4, Saddiq Bey 4, Dyson Daniels 3, Bam Adebayo 3, Michael Porter Jr. 2, Ty Jerome 2, Yaxel Lendeborg 2
🎯 counts across all turns for the clamped names (v64 to v65): Lauri Markkanen 28 to 20, Jrue Holiday 20 to 0, VJ Edgecombe 18 to 18, Ryan Rollins 17 to 2, Tyrese Maxey 10 to 10, Kawhi Leonard 7 to 5, James Harden 1 to 0
(* = one of the 24 clamped lines)

mock | round | pick | v64 🎯 | v65 🎯
51 | 4 | 39 | Ryan Rollins | Derrick White
51 | 5 | 58 | Ryan Rollins | Michael Porter Jr.
51 | 12 | 135 | Jrue Holiday | Saddiq Bey
52 | 4 | 39 | Kel'el Ware | Derrick White
52 | 11 | 130 | Jrue Holiday | Collin Gillespie
52 | 12 | 135 | Jrue Holiday | Collin Gillespie
53 | 2 | 15 | Kevin Durant | Jamal Murray
53 | 5 | 58 | Ryan Rollins | Dyson Daniels
53 | 6 | 63 | Ryan Rollins | Ty Jerome
53 | 11 | 130 | Jrue Holiday | Collin Gillespie
53 | 12 | 135 | Jrue Holiday | Collin Gillespie
54 | 5 | 58 | Ryan Rollins | Kel'el Ware
54 | 6 | 63 | Ryan Rollins | Naz Reid
54 | 11 | 130 | Jrue Holiday | Collin Gillespie
54 | 12 | 135 | Jrue Holiday | Collin Gillespie
55 | 6 | 63 | Ryan Rollins | Ty Jerome
55 | 7 | 82 | Ryan Rollins | Cameron Boozer
56 | 4 | 39 | Ryan Rollins | Derrick White
56 | 5 | 58 | Ryan Rollins | Kel'el Ware
56 | 8 | 87 | Jalen Suggs | Reed Sheppard
56 | 12 | 135 | Jrue Holiday | Collin Gillespie
57 | 12 | 135 | Jrue Holiday | Yaxel Lendeborg
58 | 2 | 15 | Lauri Markkanen | Kevin Durant
58 | 5 | 58 | Ryan Rollins | Kel'el Ware
58 | 12 | 135 | Jrue Holiday | Tari Eason
60 | 12 | 135 | Jrue Holiday | Yaxel Lendeborg
61 | 12 | 135 | Jrue Holiday | Reed Sheppard
64 | 3 | 34 | Lauri Markkanen | Bam Adebayo
64 | 4 | 39 | Lauri Markkanen | Dyson Daniels
66 | 3 | 34 | Lauri Markkanen | Bam Adebayo
67 | 12 | 135 | Jrue Holiday | Saddiq Bey
68 | 3 | 34 | Kawhi Leonard | Kel'el Ware
68 | 11 | 130 | Jrue Holiday | Reed Sheppard
68 | 12 | 135 | Jrue Holiday | Reed Sheppard
69 | 6 | 63 | Ryan Rollins | Kel'el Ware
70 | 3 | 34 | Lauri Markkanen | Dyson Daniels
71 | 3 | 34 | Lauri Markkanen | Bam Adebayo
71 | 4 | 39 | Lauri Markkanen | Kel'el Ware
72 | 4 | 39 | Lauri Markkanen | Kel'el Ware
73 | 6 | 63 | Ryan Rollins | Nickeil Alexander-Walker
73 | 9 | 106 | Yaxel Lendeborg | Reed Sheppard
73 | 11 | 130 | Jrue Holiday | Reed Sheppard
73 | 12 | 135 | Jrue Holiday | Reed Sheppard
74 | 3 | 34 | James Harden | Kel'el Ware
74 | 4 | 39 | Kawhi Leonard | Derrick White
74 | 12 | 135 | Jrue Holiday | Saddiq Bey
75 | 5 | 58 | Ryan Rollins | Michael Porter Jr.
75 | 6 | 63 | Ryan Rollins | Kel'el Ware
75 | 9 | 106 | Yaxel Lendeborg | Collin Gillespie
75 | 12 | 135 | Jrue Holiday | Collin Gillespie
75 | 13 | 154 | Jrue Holiday | Saddiq Bey
```

**Read.** The card stops pointing at the clamped high lines: Holiday's 🎯 count goes 20 to 0, Rollins' 17 to 2, Markkanen's 28 to 20. Round 1 is untouched (0 of 25); the late picks move most (round 12: 14 of 25). The turns that changed went mostly to Collin Gillespie (9), Kel'el Ware (9) and Reed Sheppard (7).

- Gillespie (pts 12.7 vs 9.5-11.9; reb 4.1 vs 3.3-3.9; tpm 2.9 vs 2.1-2.7; tov 1.6 vs 1.1-1.4; net +0.18 z) and Sheppard (tpm 2.8 vs 2.2-2.6; net +0.21 z) carry disagreements under the 0.5 cut, so they stand by design (A7). Both are SOURCES SPLIT on the repeat-name check below.
- Ware's line sits inside all three projections but for ft_pct .732 vs .714-.723 (net +0.04 z). The repeat-name check now calls it LINE QUESTIONED: value rank 26, and all four outside ranks (51, 51, 63, 65) sit 25 or more places below. On Version 64 he ranked 27 and the verdict was SOURCES SPLIT; moving the 24 lifted him one place. His minutes are the minutes-and-games consensus on his 2025-26 rates, kept at #27 by D-MG-3 (a), the Council's 5–0 call made at the owner's request (`after-report-2026-10-13-mg.md`); D-1013-9 on the sheet.

## 6. Publication

Version 65, id 1791920608-6e9c, the standing URL (fresh read of Version 64, id 1791911410-a85b, immediately before, its served file of 610226 bytes carrying the deck main f6fb476 page, sha256 a88d83f4e2f8, at offset 349); the served file (618381 bytes) carries the built page (618017 bytes, sha256 09a889d4baa5) byte-for-byte inside the service's 364-byte wrapper at offset 349; manifest built 2026-10-13, kit plane sha256 e821ec1ddc67 (the clamped projections file), market yahoo-2026-10-13.csv priced 294/335, no waiver

## 7. The plan against the outcome

The predictions written to the owner before the run (`dial/out/plan_2026-10-13.md`, verbatim from the session at 18:44), against the records above.

| prediction | outcome |
|---|---|
| 60 to 100 values move; stop a line if a rescaled shot count passes 30 or a value goes negative | did not hold: 104 moved; the 24 lines averaged 4.3 values each. No line hit the stop rule: the largest FGA is 19.9, no value is negative |
| on the kit board, the 13 high lines fall and the 8 low lines rise | did not hold for 1 line: on the kit board 12 of 13 fall (Tyrese Maxey holds at 5) and 8 of 8 rise; on the deck 13 of 13 fall and 8 of 8 rise |
| Holiday and Rollins leave LINE QUESTIONED | held: neither is flagged on Version 65. A new one appeared: Kel'el Ware (§5) |
| 0 of the 24 outside the range; Philadelphia lower but above the league maximum | held: 0 of the 24; Philadelphia 121.4 against 117.7 |
| the build passes all 7 gates; a refusal gets its cause fixed, no silent waiver | held after one refusal: gate 4 refused the first build because the morning's freshness stamp still said the pool had not changed; restamped with `--pool-changes`, keeping the morning's roster sources; no waiver |
| the chain is green | held (§3) |
| most 🎯 changes fall in the middle rounds | did not hold: rounds 3 to 6 carry 25 of the 51 changes and rounds 11 to 13 carry 20, round 12 alone 14. In 20 of those 20 late turns the Version 64 🎯 was Holiday, whose value rank fell furthest of the 24 (88 to 127) |

Two surprises in the tools themselves, both on record in the session:

- The first run of `dial_lines.py` counted 106 values. Two were floating-point noise at a range edge: RotoBaller's percentages are stored in points and divided by 100 on load, so a value equal to the edge read as just outside it. A tolerance of 1e-9 removed them before anything was written; 104, two runs identical before and after.
- After the first write, the writer's re-run check failed on a correct second run: A9 compared the cells changed in that run, so a line already clamped read as 'clamp not written'. The fault was in the check, not the data: A9 now compares the written value with the target, the re-run passes with 0 changes, the files written in place equal a fresh write from Version 64 by the corrected writer, and the corrected writer catches all three planted errors (re-run in the verification pass).

## Range check (D-RN-3)

Rule (owner, 2026-10-08): on a projection pass, every cell of a top-150 line that sits outside the range of ALL its references (Yahoo `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, RotoBaller `rotoballer-2026-09-29.csv`, 2025-26 actual `arena/results/tuning_2026-10-08/bref_pergame_2025-26.csv`; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats) carries a one-line mechanism naming two dated outlets, or comes back inside the range. This page: 19 player(s), 21 cell(s), of 145 checkable top-150 lines. None of the 24 clamped lines is listed; every row below is a WO-5 or minutes-and-games line this pass did not touch, and its mechanism is carried from the report that set it.

| player | deck rank | cells outside every reference | net z | mechanism (two dated outlets) |
|---|---|---|---|---|
| Michael Porter Jr. | 32 | stl 0.7 vs 0.8-1.1 | -0.32 | stl: steals/blocks on the item-8 three-season anchor (5/4/3 by games, per-36 at his minutes) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 (carried from `after-report-2026-10-13-mg.md`) |
| Jalen Duren | 43 | stl 0.7 vs 0.8-0.8 | -0.32 | stl: steals/blocks on the item-8 three-season anchor (5/4/3 by games, per-36 at his minutes) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 (carried from `after-report-2026-10-13-mg.md`) |
| Luka Doncic | 4 | ft_pct .772 vs .780-.782 | -0.26 | ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 (carried from `after-report-2026-10-13-mg.md`) |
| Tyrese Haliburton | 11 | tov 1.5 vs 1.7-1.7 | +0.26 | minutes: minutes set by the range rule to the outside lines' range (Hashtag, RotoBaller, Yahoo); tov: R2 keep: 2024-25 per-36 rates (Basketball-Reference; ESPN) (carried from `after-report-2026-10-13-mg.md`) |
| Naz Reid | 52 | tov 1.9 vs 1.6-1.7 | -0.26 | tov: the 2025-26 per-36 rate at his minutes (the method) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 (carried from `after-report-2026-10-13-mg.md`) |
| Jalen Williams | 41 | ast 6 vs 5-5.5 | +0.25 | ast: the 2025-26 per-36 rate at his minutes (the method) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 (carried from `after-report-2026-10-13-mg.md`) |
| Domantas Sabonis | 20 | tpm 0.9 vs 0.6-0.7 | +0.21 | tpm: R2 keep: 2024-25 per-36 rates (Basketball-Reference; ESPN) (carried from `after-report-2026-10-13-mg.md`) |
| Cade Cunningham | 23 | blk 0.7 vs 0.8-0.8 | -0.20 | blk: steals/blocks on the item-8 three-season anchor (5/4/3 by games, per-36 at his minutes) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 (carried from `after-report-2026-10-13-mg.md`) |
| Luke Kornet | 148 | fg_pct .613 vs .643-.662 | -0.19 | fg_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 (carried from `after-report-2026-10-13-mg.md`) |
| Keegan Murray | 76 | pts 12.4 vs 13.3-16.1 | -0.17 | pts: R2 keep: 2024-25 per-36 rates (Basketball-Reference; ESPN) (carried from `after-report-2026-10-13-mg.md`) |
| Naji Marshall | 147 | fg_pct .497 vs .505-.510 | -0.14 | fg_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 (carried from `after-report-2026-10-13-mg.md`) |
| Franz Wagner | 30 | reb 6 vs 5.2-5.7 | +0.12 | reb: the 2025-26 per-36 rate at his minutes (the method) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 (carried from `after-report-2026-10-13-mg.md`) |
| Brandon Ingram | 84 | ft_pct .811 vs .819-.826 | -0.12 | ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 (carried from `after-report-2026-10-13-mg.md`) |
| Giannis Antetokounmpo | 34 | tov 3.6 vs 3.1-3.3; fg_pct .600 vs .608-.624; ft_pct .664 vs .628-.650 | -0.11 | fg_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range); ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range); tov: the 2025-26 per-36 rate at his minutes (the method) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 (carried from `after-report-2026-10-13-mg.md`) |
| Jakob Poeltl | 114 | ft_pct .588 vs .602-.642 | -0.10 | ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 (carried from `after-report-2026-10-13-mg.md`) |
| Jalen Suggs | 65 | ft_pct .834 vs .846-.866 | -0.08 | ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 (carried from `after-report-2026-10-13-mg.md`) |
| CJ McCollum | 121 | ft_pct .780 vs .749-.772 | +0.08 | ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 (carried from `after-report-2026-10-13-mg.md`) |
| Christian Braun | 118 | ft_pct .774 vs .782-.815 | -0.06 | ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 (carried from `after-report-2026-10-13-mg.md`) |
| Tobias Harris | 135 | ft_pct .857 vs .863-.869 | -0.04 | ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 (carried from `after-report-2026-10-13-mg.md`) |

## Points identity (D-1009-3)

Rule (owner, 2026-10-09): on a projection pass, every top-200 line on either plane whose points sit more than 1 from its own shooting is reconciled or carries a mechanism naming two dated outlets. This page: `identity_check.py` — POINTS IDENTITY: 0 player(s), 0 line(s) more than 1 from their own shooting (200 deck and 200 kit lines checked); the clamped lines were written with FGA and FTA rescaled so the identity holds (A5 of the writer: within 0.25).

| player | plane | rank | pts | implied (2·FGM + 3PM + FTM) | gap | mechanism (two dated outlets) |
|---|---|---|---|---|---|---|

## Watchlist

- Jamal Murray and Aaron Nesmith, just past the 0.5 cut after the frame moved (D-1013-8).
- Kel'el Ware, LINE QUESTIONED on Version 65 by one place; the 🎯 in 21 of 25 replayed mocks (D-1013-9).
- The late-round 🎯 now lands on Collin Gillespie and Reed Sheppard: lines with small disagreements this pass left by design (§5).
- Philadelphia's residual: 121.4 possessions against a league maximum of 117.7; the usage model is D-C2, after the draft.
- The 10/14 lock paste (D-1013-1) and the publish freeze during the draft (D-1013-5).
- Do not use RESYNC during the draft; the recovery steps are in `after-report-2026-10-13-live-mock.md` (D-1013-2).

## Open-item receipts

| item | query run (2026-10-13) | dated finding |
|---|---|---|
| (this pass) | records only; no web research and no roster pull in this pass | the lines moved inside the three outside projections on file; pull receipts for the window live in `after-report-2026-10-13.md` (the morning's pull), same day |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (`after-report-2026-10-13.md`, receipts dated 10/13) | all HELD or unsigned on 2026-10-13 per those receipts; not re-queried in this pass (did not check) |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 09a889d4baa5), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 25 of 25 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-13.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 5 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Kel'el Ware | 21 of 25 | 26 | 77 | 51 | 51 | 63 | 65 | ft_pct .732 vs .714-.723 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Reed Sheppard | 20 of 25 | 63 | 180 | 56 | 118 | 126 | 129 | tpm 2.8 vs 2.2-2.6 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Ty Jerome | 20 of 25 | 39 | 117 | 48 | 60 | 101 | 71 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 11 of 25 | 70 | 143 | 93 | 121 | 137 | 98 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 7 of 25 | 79 | 183 | 100 | 126 | 148 | 156 | pts 12.7 vs 9.5-11.9; reb 4.1 vs 3.3-3.9; tpm 2.9 vs 2.1-2.7; tov 1.6 vs 1.1-1.4 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Saddiq Bey | 7 of 25 | 90 | 177 | 108 | 132 | 169 | 143 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Dyson Daniels | 6 of 25 | 22 | 62 | 20 | 64 | 56 | 53 | reb 6.8 vs 5.8-6.4; ast 5.9 vs 4.7-5.5; tpm 0.3 vs 0.5-0.6 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Michael Porter Jr. | 5 of 25 | 32 | 60 | 55 | 62 | 70 | 59 | pts 24.5 vs 18.7-21.8; ast 3 vs 2.4-2.6; stl 0.7 vs 0.8-1; tpm 3.4 vs 2.9-3.1; tov 2.3 vs 1.9-2 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (21 mocks, value 6, market 18); Lauri Markkanen (14 mocks, value 21, market 37); VJ Edgecombe (12 mocks, value 58, market 75); Derrick White (10 mocks, value 29, market 45); Tyrese Maxey (7 mocks, value 5, market 9).

## Bounds

**Out of scope by design.**
- The 80 lines that still disagree with the three projections were not touched: 78 carry half a z point or less each (A7), and the 2 now just past it are D-1013-8.
- No blend of seasons, no usage model and no team scaling: those are D-C2, after the draft. Philadelphia's residual is measured (§4), not modeled.
- No engine, card, survival or price change; the market file is Yahoo's 10/13 paste, as on Version 64.

**In scope and unverified.**
- Whether the clamped lines are closer to what will happen — `UNVERIFIABLE` until games are played. The record behind the choice is one out-of-sample season (`after-report-2026-10-09-market.md` §4), where a copy of the prior season had more error than pre-season projections in 8 of 9 categories.
- Whether the three outside sources share a blind spot on some roster — `NOT-ATTEMPTED`; a line inside their range cannot show one.
- The edge of the range is the most optimistic outside view on the high side and the most pessimistic on the low side; the Contrarian's average would have moved the 13 high lines further. How much further, and what that would do to the card: `NOT-ATTEMPTED`, by the Council's choice of the edge.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-1013-6 | Decided 2026-10-13: the Council's sharpened option, the material lines clamped to the edge of the outside range, owner go ("Write the report, merge both PRs, and publish Version 65") | applied in this pass |
| D-1013-8 | Aaron Nesmith (-0.54) and Jamal Murray (+0.51) sit just past the 0.5 cut after the 24 moved the category frame. Clamp them too at the 10/14 lock pass? | no: both within 0.05 of the cut |
| D-1013-9 | Kel'el Ware is LINE QUESTIONED on Version 65 (value rank 26; Yahoo 51, Hashtag 51, Rotoworld 63, RotoBaller 65), one place past the bar after the 24 moved. His minutes are the consensus D-MG-3 (a) kept; his rates are his 2025-26 rates. Re-derive his rates with two dated outlets before the draft, or keep D-MG-3 (a)? | keep D-MG-3 (a) for the draft; the standing rule re-derives the line at the next projection pass |
| D-1013-7 | Two build checks: the team budget, and the range check without last season as a reference | after the draft, with D-C2 |
| D-C2 | The blend of seasons and the new-team usage model, including Philadelphia's residual | after the draft |
| D-1013-1..5, D-SF-1..4 and earlier | carried | carried |

## Provenance

- Starting point: kit `main` 7c28bb3, deck `main` f6fb476 (Version 64, page sha256 a88d83f4e2f8). Selection: `usage-2026-10-13/range_check_no_actual.json`. References: `report/market/yahoo-proj-2026-10-13.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-09-29.csv`.
- Tools: `report/dial/tools/` (`dial_lines.py`, `dial_apply.py`, `dial_page.py`, `board_diff.py`, `card_compare.py`, `chain_dial.sh`, `write_dial_report.py`, `write_dial_report_tail.py`). Outputs: `report/dial/out/` (the plan as written before the run, lines, apply record, build log, chain log, board diff, team budget after, range checks before and after, value ranks, identity and range records, repeat-name section, card comparison, publish record). Deck records: `arena/results/full_dom_check_2026-10-13_v65.json`, `repeat_market_check_2026-10-13_v65.json`.
- The pass paused once: the environment's permission check refused commands mid-pass; the unverified changes were backed up to the scratchpad and both repositories restored, then reapplied on the owner's go and checked byte-identical to the backup.
- Publication: Version 65, id 1791920608-6e9c, the standing URL (fresh read of Version 64, id 1791911410-a85b, immediately before, its served file of 610226 bytes carrying the deck main f6fb476 page, sha256 a88d83f4e2f8, at offset 349); the served file (618381 bytes) carries the built page (618017 bytes, sha256 09a889d4baa5) byte-for-byte inside the service's 364-byte wrapper at offset 349; manifest built 2026-10-13, kit plane sha256 e821ec1ddc67 (the clamped projections file), market yahoo-2026-10-13.csv priced 294/335, no waiver

## In plain language

**What changed.** 24 players' projections were pulled back inside what Yahoo, Hashtag and RotoBaller project for them. Thirteen were too high: Holiday's value rank goes 88 to 127, Brown's 59 to 93, Markkanen's 11 to 21, Kawhi's 6 to 7. Eight were too low and come up: Edwards 23 to 13, Mobley 50 to 38, Siakam 109 to 75. Philadelphia's LeBron, Embiid and Edgecombe were brought inside the same range: their points come down a little (Embiid 25.1 to 24.6, LeBron 20.9 to 20.3, Edgecombe 16 to 15.9), and the other moved values go to the nearer edge, so some go up, such as free throws (LeBron .737 to .752, Embiid .846 to .857). No other player's value rank on the page moved more than 6 places.

**What it does to your card.** Across the 25 practice drafts replayed on both versions, the 🎯 at your picks changes at 51 of 325 turns, none in round 1. Holiday and Rollins mostly stop being the pick. Late in the draft the 🎯 now often lands on Gillespie, Ware or Sheppard instead; the details are in §5.

**What is left.** Philadelphia's players, added up, still claim more of the ball than any team used last season, 121.4 possessions against 117.7. That needs a usage model, which waits until after the draft. Two players now sit right at the edge of the cut, and their call is D-1013-8. Ware's line is now questioned by the repeat-name check, by one place, and his call is D-1013-9.

**Your decisions.** D-1013-8 and D-1013-9 tonight or at the lock; D-1013-7 and D-C2 after the draft.
