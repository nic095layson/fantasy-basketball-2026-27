# After-report — 2026-10-09 (confidence): the system going into the 10/14 draft, before and after today's exercise

**Owner request (2026-10-09, verbatim):** "a few weeks ago I asked you your confidence % in this system and going into
the draft next wednesday. Please provide an updated report, with before and after from this last exercised. Provide
reasons in change of percentages, and any data related evidence."

Pull window: 2026-10-09 → 2026-10-09 — not a pull. **What was analyzed:** the two earlier confidence tables (chat,
2026-10-01 18:53 UTC and 2026-10-02 00:39 UTC, recovered verbatim from the session transcript), against the state of
both planes after today's work: kit main `5b35f53` (PR #85), deck main `2ed1305` (PR #92), deck v53 (version id
1791570495-d551). **Method:** every "now" figure is a judgment (INFERENCE) anchored to a dated record named beside it
(EVIDENCE); the records are today's three after-reports and the committed results they cite. No new computation ran
for this report. Gate: `check_provenance.py` → PASS (verified 2026-07-13 .. 2026-10-07), exit 0.

**Headline.** The tool and the process moved from about 90% to about 92%: the audit reproduced both engines to the
last digit from an independent implementation, every change since was red-first and gated, and the card's advice proved
insensitive to market noise at 273 of 273 recorded turns. The data the draft will run on moved from about 65% to about
70%: for the first time the projection method has out-of-sample evidence (last season's entering lines beat the prior
season in 8 of 9 categories and a three-season average in 6 of 9), but 41 top-200 lines still fail the points identity
and 131 of 145 checkable rows carry a cell outside every outside reference, and both wait on Sunday's pass. The
absolute title odds stay at 40%: identical to the third decimal under price changes, soft under pool changes.

## 1. Roster changes

None — not a pull.

## 2. Confidence by layer, before and after

The rule from 10/01 stands: the system is internally consistent to a very high standard and externally unproven, and
those two are not averaged into one number. Columns 10/01 and 10/02 are the earlier tables as given; "now" is today.

| layer | 10/01 | 10/02 | now | what moved it, with the record |
|---|---|---|---|---|
| Engine math (page = code = Python) | 99% | 99% | 99% | EVIDENCE: an independent re-implementation of each plane's method reproduces the deck engine (all 335 rows) and the kit engine (321 rows) to **0.0** in all nine categories (`category_audit_2026-10-09.json`, 2026-10-09); parity EXACT MATCH at 364 owner turns across 28 recorded drafts, twice today; suites 99 / 52 / 65; browser harness 143 assertions, 0 failed; pts = 2·FGM + 3PM + FTM holds to 0.0002 on 432 actual lines. INFERENCE: nothing honest goes above 99. |
| Placements (who is on which team) | 97% | 98% | 98% | EVIDENCE: direct ESPN roster verification, all 30 teams, 335 of 335 rows, zero mismatches, every pull since 10/02 (`data/freshness.json`, 2026-10-09). INFERENCE: held at 98 because a placement can change on the feed between pulls (Hawkins MEM to CHI appeared on 10/08 and was caught by the pull, not before it). |
| Availability tags (right in kind) | 85% | 87% | 88% | EVIDENCE: the mechanical injury sweep (118 feed rows against 49 tags, no untagged Out row, 2026-10-08/09); Nurkić re-tagged by the D-1008-1 default on 10/09; eight GP ≤ 25 rows now off both boards (kit exclusion, 2026-10-09). INFERENCE: one point up; the tags are mechanical and current. |
| Availability discount as a ranking input (new row) | not scored | not scored | 60% | EVIDENCE: the flat ×0.78 applies only above the pool-mean zero, so 19 of the 29 risk rows in the deck top 200 carry no discount; on the 2025-26 entering pool the 20 risk rows finished 6.3 places worse than forecast under every anchor, and the anchor change did not help (ρ .604 vs .639) — `fix_backtest_2026-10-09.json`. The per-player games model is post-draft (owner 2026-10-09) and now has its three-season games record (252 of 335 rows). INFERENCE: this is the one measured leak left in the valuation; 60 says the tag is right in kind and weak in size. |
| Market column (Mkt rank) | 70%, decaying | 85%, decaying | 92%, decaying slowly | EVIDENCE: Yahoo ADP as of 10/09 (Hashtag's page, owner-verified), 0 days old, 246 of 335 rows priced; 169 names compared with the 10/06 paste moved 0.42 places on average, 2.1 at most (`adp-refresh-2026-10-09.md`). INFERENCE: a market that moved under a place in three days is stable; the 10/14 lock paste is the last refresh. |
| Projection lines (the stats) | 60 to 65% | 65 to 68% | 70% | EVIDENCE for the method: on the 2025-26 entering pool (189 rows scored against the verified actual) our lines beat the prior season in 8 of 9 categories (FG% a tie) and a 5/4/3 three-season line in 6 of 9 (losing FT%, steals, blocks) — `actuals_2026-10-09/analysis_summary.json`; correlation with the actual season .72 to .91 by category. EVIDENCE against the lines as they stand: 41 top-200 players (49 lines) fail the points identity at 1.0 (`identity_check_2026-10-09.json`); 131 of 145 checkable top-150 rows carry a cell outside every outside reference (`range_check`, 2026-10-08); no line has moved on a preseason box score yet. INFERENCE: the method is now shown to have skill; the current lines still carry the July shape. Sunday's pass is the mover; a clean pass with the identity and range checks green would read 75 to 78. |
| Board order, top 60 within ten places | 75% | 78% | 82% | EVIDENCE: the league's own 2025-26 draft redrafted by the card from seat 4 against the real opponents, graded on the actual 2025-26 lines — 54.05% title median against the real roster's 42.10%, 19 of 20 rooms above (`what-if`, 2026-10-07); Rotoworld's 9-cat sheet ρ .830 against the board and .950 against Yahoo (2026-10-06); today's kit exclusion left the top 60 unmoved; the card's pick identical at 273 of 273 recorded turns under the 10/06 and 10/09 prices. INFERENCE: the ordering has out-of-sample support now; four points. |
| Survival chips as a ranking of risk | not scored | 70% | 70% | EVIDENCE unchanged: the league's own draft realizes above the prediction at every band, in order (2026-10-01). No new calibration today. |
| Survival chips as probabilities | not scored | 40% | 40% | EVIDENCE: too pessimistic at every band in the league (2026-10-01); against the cast rooms the Brier runs .196 to .222 and reads optimistic (mocks 62–71). INFERENCE: two biases in two kinds of room; unchanged. |
| Arena title odds as absolute numbers | 40% | 40% | 40% | EVIDENCE: the 15-room re-grade reproduces every room's odds to the third decimal under a price change (`regrade_2026-10-09.json`), while the same rooms moved with the pool over two weeks (mock 57 as drafted 27.4% on its own pool, 13.2% on today's). INFERENCE: stable to noise, soft to lines; relative comparisons remain the use. |
| Card advice under market noise (new row) | not scored | not scored | 95% | EVIDENCE: 126 market ranks changed and the 🎯 stayed the same name at all 195 owner turns of the 15 rooms and all 273 of the 21 rooms on the real pages (2026-10-09). INFERENCE: the card is not knife-edge on prices. |
| Record integrity (new row) | not scored | not scored | 95% | EVIDENCE: every derived artifact pinned to a commit and reproduced byte-for-byte (19 of 19, 2026-10-09); four seasons of actuals accepted only where two outlets match within rounding, conflicts listed; every report gate passing. INFERENCE: the numbers the draft uses can be traced to their source. |

**One number each, as on 10/02.** The tool and the process: about 92% (was about 90). The data the draft will actually
run on: about 70% (was about 65) until Sunday's pass, which is the only thing that moves it further before the lock.
The forecast of winning the league as an absolute figure: 40%, unchanged; the ordering of who to take over whom: about
82%.

## 3. Why the numbers moved — the evidence behind each change

- **Process (+2).** EVIDENCE: the audit (2026-10-09) found no arithmetic error on either plane; every change today
  failed its test first (kit 2 of 4, deck 5 of 52) and then passed; the one defect of the day — the morning pull's
  note-date bug that wrote "Macao" on 33 notes — was caught on the built page before any gate passed and rolled back
  (`after-report-2026-10-09.md`). INFERENCE: a process that catches its own defect before publishing earns the two
  points; it does not earn more, because the defect existed.
- **Data (+5).** EVIDENCE: the backtest and stability records above; the verified actuals replacing a single-outlet
  file; the identity and range flags now counted rather than suspected. INFERENCE: the gain is the method's measured
  skill; the ceiling is the 41 and 131 unresolved flags.
- **Market (+7).** EVIDENCE: the price file went from one day old (10/02) to zero days old on an owner-verified source,
  and the 10/06-to-10/09 drift is under a place for 169 names. INFERENCE: the market is quiet and current.
- **Board order (+4).** EVIDENCE: the what-if on realized lines is the first test of the ordering against what
  actually happened in this league.
- **Two rows unchanged at 40.** No new calibration evidence for the survival probabilities or the absolute odds; the
  re-grade showed the odds' stability to noise, not their accuracy.

## 4. What did not move, and why it is honest

The projection lines are still the layer that decides the draft and still the one with the least evidence. Today
proved the method beat naive baselines last season and proved steals are structurally the noisiest category; it did
not touch a single line. The 70 is the method's credit; the lines earn their own number on Sunday.

## 5. Gates (2026-10-09, this report)

| gate | result |
|---|---|
| kit `report/check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07; exit 0 |
| kit `report/check_report.py` | REPORT GATE: PASS (structure, publication rule, pull-log row); exit 0 |
| deck `judgment_open_items.py --check-report` | receipts check PASS — all 10 flagged names carry a receipts row; exit 0 |
| deck `repeat_market_check.py --check-report` | REPEAT-NAME CHECK: PASS — 12 flagged names, each with a row (21 of 21 mocks replayed on the v53 page); exit 0 |

## 6. Watchlist / open items

- **Sunday 10/11, WO-5** — items (5)–(8): steals and blocks to the three-season anchor, the identity rows, the range
  check; this is what moves the data number.
- **Tuesday 10/13** — the second pass and final check.
- **Wednesday 10/14 morning** — the lock on your fresh Yahoo ADP paste; the league settings screenshot and the
  draft-room positions are still owner-side inputs (D-G5, D-G3).
- **After the draft** — the per-player expected-games model (the 60% row), D-RN-4, D-1009-7.

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

Reproduced from `after-report-2026-10-09-market.md` (the v53 page); this report ran no replay of its own.

## Bounds

**Out of scope by design:** no new computation; the percentages are judgments anchored to records, not measured
probabilities; the earlier tables are quoted as given and not re-derived.

**In scope and unverified:** the survival probabilities' calibration against a public room this week (NOT-ATTEMPTED —
the last public-room Brier is mock 68, 2026-10-08); whether the Macao game changes any role (UNVERIFIABLE until
Sunday's two-outlet read; ESPN's box score is single-source today); the owner-side inputs (league settings, draft-room
positions, the lock paste) — owner's to supply.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-1009-9 | the confidence report cadence: (a) re-issue after Sunday's pass and again at the 10/14 lock, with the same layers; (b) only at the lock | (a) |
| D-1009-6..8 | as on the market report's sheet (steals/blocks anchor; the blend; the price file until the lock) | as there |

## Provenance and bounds

- Sources: the session transcript for the 10/01 and 10/02 tables (quoted verbatim); `after-report-2026-10-09.md`,
  `-fixes.md`, `-market.md`; deck records `category_audit_2026-10-09.json`, `fix_backtest_2026-10-09.json`,
  `actuals_2026-10-09/analysis_summary.json`, `identity_check_2026-10-09.json`, `regrade_2026-10-09.json`,
  `market_rank_moves_2026-10-09.json`; `after-report-2026-10-08-standing-checks.md` (range check);
  `after-report-2026-10-07-whatif.md` and `after-report-2026-10-01-league-survival.md` as cited on their dates.
- Every "now" percentage is INFERENCE; every cited number is a script's output on a committed record.

## In plain language

Three weeks ago I told you the tool was about 90% and the data about 65%. Today the tool is about 92% and the data
about 70%. The tool went up because an independent check reproduced every number to the last digit, every change
since was tested before it was trusted, and the card gives the same advice whether the market moves a little or not.
The data went up because, for the first time, the projection method was scored on a real season and beat the simple
alternatives in most categories. It did not go up more because the current lines still carry 41 internal
inconsistencies and 131 cells no outside source supports, and nothing fixes those except Sunday's pass. The odds of
winning the league as a single number are still 40%: the model is stable, not proven. The order of who to take over
whom is about 82%, and that is the number the draft actually uses.
