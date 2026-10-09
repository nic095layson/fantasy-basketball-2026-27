# After-report — 2026-10-09 (fixes): the category audit's recommendations applied

**Owner request (2026-10-09, verbatim):** "Proceed with all your recommendations. Thank you Claude!" — on the
assessment that followed "Knowing what you do now, such as re-simulating last year's fantasy season — would this
proposed fixes help 'sharpen' and fine tune the calculations …? I need this as dialed in as we can. Can't have
gaps or differences in counting categories, unless it is actually benefitting a competitive advantage."

Pull window: 2026-10-09 → 2026-10-09 — not a pull: the day's pull is `after-report-2026-10-09.md` (window
10/8 → 10/9, deck v52). This report records the code, governance and page changes that apply decisions
D-1009-1..4, the backtest they rest on, and the board effects. No projection line moved; the projection work
those decisions queue is the WO-5 pass of 10/11, as recommended.
Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07`,
exit 0 (no CSV row changed).

**Method.** Machine work on records only; no web research. The backtest (`arena/mocks/audit_1009/fix_backtest.py`,
record `arena/results/fix_backtest_2026-10-09.json`, deck PR #91, two runs byte-identical) scored each proposed
fix on the 2025-26 entering pool (`arena/data/players_2025-10-21.csv`, 220 rows, 20 risk tags) against the
actual 2025-26 lines (Basketball-Reference, 25+ games). Every change below was made red-first where it is
code, by exact-anchor script where it is prose, and verified by the repos' own gates.

## 1. Roster changes

None — not a pull. The pool on both planes is byte-identical to the morning's.

## 2. What was applied

| decision | what changed | where | verified by |
|---|---|---|---|
| **D-1009-1** kit exclusion class | `rank_engine.py` now holds every row at GP ≤ 25 (`EXCLUSION_GP`, the deck's out-*/recovery twin) off the board and out of the 180-row z-score pool, as it already held team-`FA` rows; the rule lives in `exclude_held()`, the board header names both held groups | kit `report/rank_engine.py`, `report/test_rank_engine.py` (new), `report/top-200-2026-27.md` | red-first: the FA rule was first moved into `exclude_held()` with the board byte-identical, then four tests written — the GP case and the pool case **failed** (2 of 4), the FA case passed; the rule implemented — **4 of 4** pass; board regenerated and diffed (§4) |
| **D-1009-2** the discount's zero | wording only, the engine untouched: `hoops.zscores`' docstring no longer calls the z-sum's zero "replacement level" (it is the top-156 pool's mean, about the 58th playable row; the haircut applies above it); the page's Logic paragraph ("replacement-anchored") and legend ("applied only when value is positive" → "… positive, i.e. above the draftable average") and the gradient-model comment say the same | deck `scripts/hoops.py`, `docs/draft-deck.html` | parity EXACT on the rebuilt page (§6): the arithmetic did not move |
| **D-1009-3** the points identity | new `scripts/identity_check.py`: every top-200 line on either plane whose points sit more than 1.0 from 2·FGM + 3PM + FTM is listed; `--check-report` refuses a projection-pass report unless each listed player's row names two outlets (the kit's lexicon); WO-5 acceptance item (7); DATA-PULL §2 bullet | deck `scripts/identity_check.py`, `scripts/test_gates.py` (+5 cases); kit `DATA-PULL.md`, the work order | red-first: the five PI cases were added with `scripts/identity_check.py` absent — **5 of 52 cases FAILED** (exactly the five; the other 47 green); the script placed — **all 52 cases passed** |
| **D-1009-4** WO-5's order of work | queue addition (5): the 10/11 pass starts with the audit's largest departures, steals and blocks first, each named with ours / the outside median / the 2025-26 actual; (6) the fifteen identity rows the audit named plus the check's full listing (§5) | kit `report/pre-draft-workorder-2026-10-01.md` | the text names the record it rests on |
| after the draft | the fairer off-card grade (D-RN-4) and the availability model: replace the flat 0.78 with a per-player expected-games estimate, re-fit, then review the haircut's anchor (T1 below) | the work order's new "After the draft" paragraph | — |

Not changed, by the evidence: the place the injury discount starts (D-1009-2 option (b) is withdrawn — T1 below).

## 3. The backtest the decisions rest on (2025-26 entering pool vs the actual season)

| test | result | what it decided |
|---|---|---|
| T1 the discount anchor | Spearman vs realized season value at the top 120 / 156 / 200: shipped rule .639 / .700 / .796; anchored at replacement .604 / .693 / .792; no discount at all .641 / .701 / .796; discount on every row .633 / .692 / .790. The 20 risk rows finished 6.3 places worse than forecast under every rule (11 of 20 too high); 12 of the 20 sat below zero and were never discounted | the anchor does not help and the flat tag barely matters; what leaked is the flatness (Davis #5 to 20 games, Curry #9 to 43, Porziņģis #36 to 32, Fox #54 to 72, all at 0.78) — a per-player games estimate is the post-draft fix |
| T2 the points identity | 30 entering lines off by 1+; points set to the implied value cut their error from 2.42 to 1.98 (20 of 30 improved) but Embiid from −2.9 to −5.8 — his shooting half was wrong; |residual| does not predict |points error| (ρ .03) | the identity flags inconsistency, not which side is wrong: reconcile by evidence, never by formula alone |
| T3 per category | the entering lines beat the prior season's actual in 8 of 9 categories (FG% a tie); steals the least predictable (ρ .673; the prior season .584); mean bias +0.68 pts, +0.51 reb, +0.20 ast | the richer counting lines are a measured edge; steals are noise for everyone |
| T4 departures | where a line departed 0.5+ z from the prior actual, it beat the prior season in 7 of 9 categories (pts 9/12, reb 6/7, ast 7/9, tpm 8/11) — steals 13 of 24, blocks 2 of 4 | steal and block departures go first on Sunday, to two-source numbers |

## 4. Board effects (computed, never eyeballed)

- **Kit** (`scratchpad fix1009/kit_board_diff.json`): 12 rows held off — unsigned Thomas, Ivey, Konchar,
  Dillingham; GP ≤ 25 Lively, DiVincenzo, Butler, Nurkić, Mark Williams, Strus, Moody, Sharpe. Exits from the
  top 200: Butler (was 68), Lively (107), Mark Williams (121), Shaedon Sharpe (136), Nurkić (172), DiVincenzo
  (176) — the six the audit named. Entries at 195–200: Barrett, Kennard, Champagnie, Fears, Toppin, Mathurin.
  143 of the 200 rows shift, 3.0 places on average, 8 at most (Trent Jr. 183 to 175, Simons 177 to 170, Mitchell
  Robinson 181 to 174); the top 60 is unchanged. The audit's A5 counterfactual predicted the same six exits and
  the same ceiling.
- **Deck:** no row moved — the changes are wording. Parity on the rebuilt page: EXACT MATCH, 364 owner turns across 28 committed states, 318 market ranks (240 priced) — the arithmetic did not move.

## 5. The points identity today (the check's first run; mechanisms are Sunday's work)

At the 1.0 threshold the check lists **41 players, 49 lines** (deck 200 and kit 200 checked) — the audit's 15 at
its looser max(1.0, 8%) rule plus 26 more whose gap is between 1.0 and 8% of their points (Jokić +1.8, Tatum +2.0,
Durant +1.7, Giannis +1.5, Dončić +1.4 on both planes, Wembanyama −1.4 on the kit). This report is not a
projection pass, so `--check-report` is not applied to it; the section below is the queue for the 10/11 pass,
where every row either comes back inside by evidence or names two outlets. The threshold is on the sheet
(D-1009-5).

## Points identity (D-1009-3)

Rule (owner, 2026-10-09): on a projection pass, every top-200 line on either plane whose points sit more than 1 from its own shooting (2·FGM + 3PM + FTM, with FGM = FG% × FGA and FTM = FT% × FTA) is reconciled by evidence — either side may be the wrong half — or carries a one-line mechanism naming two dated outlets. This pass: 41 player(s), 49 line(s), of 200 deck and 200 kit lines checked.

| player | plane | rank | pts | implied (2·FGM + 3PM + FTM) | gap | mechanism (two dated outlets) |
|---|---|---|---|---|---|---|
| Joel Embiid | deck | 71 | 24 | 21.1 | +2.9 | — |
| Kyrie Irving | deck | 15 | 24.7 | 22.2 | +2.5 | — |
| Karl-Anthony Towns | deck | 6 | 24.8 | 22.5 | +2.3 | — |
| Jayson Tatum | deck | 21 | 26.8 | 24.8 | +2.0 | — |
| Zion Williamson | deck | 105 | 24.8 | 23.0 | +1.8 | — |
| Amen Thompson | kit | 28 | 16.5 | 18.3 | -1.8 | — |
| Bam Adebayo | kit | 32 | 17.5 | 19.3 | -1.8 | — |
| Tyrese Haliburton | deck | 7 | 18.6 | 20.4 | -1.8 | — |
| Nikola Jokic | deck | 2 | 29 | 27.2 | +1.8 | — |
| Onyeka Okongwu | deck | 36 | 15 | 16.8 | -1.8 | — |
| Kevin Durant | deck | 18 | 26 | 24.3 | +1.7 | — |
| Trae Young | deck | 57 | 23.5 | 21.9 | +1.6 | — |
| Walker Kessler | kit | 35 | 11.5 | 13.1 | -1.6 | — |
| Jalen Duren | deck | 60 | 12.5 | 14.0 | -1.5 | — |
| Josh Giddey | deck | 32 | 16.5 | 18.0 | -1.5 | — |
| Rudy Gobert | kit | 85 | 11 | 12.5 | -1.5 | — |
| Giannis Antetokounmpo | deck | 42 | 30.8 | 29.3 | +1.5 | — |
| Jalen Duren | kit | 57 | 13.5 | 15.0 | -1.5 | — |
| AJ Dybantsa | deck | 139 | 20.5 | 22.0 | -1.5 | — |
| James Harden | kit | 37 | 20.5 | 21.9 | -1.4 | — |
| Paolo Banchero | deck | 102 | 26.5 | 25.1 | +1.4 | — |
| Victor Wembanyama | kit | 2 | 26.5 | 27.9 | -1.4 | — |
| Luka Doncic | deck | 4 | 33.5 | 32.1 | +1.4 | — |
| Luka Doncic | kit | 4 | 33.5 | 32.1 | +1.4 | — |
| Donovan Mitchell | deck | 14 | 24.5 | 25.8 | -1.3 | — |
| Stephen Curry | kit | 13 | 23.5 | 24.7 | -1.2 | — |
| OG Anunoby | deck | 28 | 18.5 | 17.3 | +1.2 | — |
| Kristaps Porzingis | deck | 39 | 19.8 | 18.6 | +1.2 | — |
| Evan Mobley | deck | 19 | 19.5 | 20.7 | -1.2 | — |
| Trey Murphy III | deck | 33 | 22 | 20.8 | +1.2 | — |
| Aaron Gordon | kit | 93 | 15.5 | 16.7 | -1.2 | — |
| Derrick White | kit | 23 | 17.5 | 18.7 | -1.2 | — |
| Nikola Jokic | kit | 3 | 28 | 29.2 | -1.2 | — |
| Daniel Gafford | kit | 130 | 9.5 | 10.7 | -1.2 | — |
| Desmond Bane | deck | 27 | 19.8 | 21.0 | -1.2 | — |
| OG Anunoby | kit | 44 | 16.5 | 17.7 | -1.2 | — |
| Zach Edey | deck | 84 | 12.5 | 13.6 | -1.1 | — |
| Shai Gilgeous-Alexander | kit | 1 | 31 | 32.1 | -1.1 | — |
| Cameron Boozer | deck | 48 | 18.5 | 19.6 | -1.1 | — |
| Cameron Boozer | kit | 41 | 18.5 | 19.6 | -1.1 | — |
| Paul George | kit | 51 | 17.5 | 18.6 | -1.1 | — |
| AJ Dybantsa | kit | 166 | 18 | 19.1 | -1.1 | — |
| Andrew Nembhard | deck | 124 | 12.5 | 13.6 | -1.1 | — |
| Jamal Murray | deck | 20 | 21.8 | 22.9 | -1.1 | — |
| Amen Thompson | deck | 30 | 16.5 | 17.6 | -1.1 | — |
| Jamal Murray | kit | 26 | 22 | 23.1 | -1.1 | — |
| Austin Reaves | deck | 26 | 23 | 24.0 | -1.0 | — |
| Jalen Suggs | deck | 59 | 17 | 16.0 | +1.0 | — |
| Tyrese Maxey | deck | 9 | 25 | 24.0 | +1.0 | — |

## 6. Gates (2026-10-09, the fixes)

| gate | result |
|---|---|
| kit `report/test_rank_engine.py` | red first: 2 of 4 failed (the GP case, the pool case) with the FA-only rule; then 4 of 4 OK |
| kit `report/check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07; exit 0 |
| kit `report/rank_engine.py` | exit 0; 200 of 313 projected, 12 held off (named above) |
| kit `report/check_derived.py` | PASS — all 17 dated artifacts reproduce byte-for-byte; exit 0 (the engine change touches no pinned artifact) |
| deck `scripts/test_gates.py`, red run | 5 of 52 cases FAILED — exactly the five new PI cases (`scripts/identity_check.py` absent: "No such file or directory"), the other 47 green |
| deck `scripts/build_deck.py` | gates 1–7 + F8 pass on the first run, no waiver needed (the kit CSV is unchanged since v52, so no propagation item): planes 315 shared · team 0 · exclusion 0 · drift 0 · propagation 0; pool `dc9a6d9fd75a`, identical to v52; freshness restamped `--no-pool-changes` for the wording rebuild; injection round-trip OK; "safe to publish" |
| deck `scripts/check_parity.py` | PARITY: EXACT MATCH — 364 owner turns across 28 committed states; market ranks 318 (priced 240); exit 0 |
| deck `test_card.py` / `test_gates.py` / `test_draft.py` | CARD: all 99 cases passed; all 52 cases passed (the five PI cases among them); all 65 cases passed; exit 0 each |
| deck `arena/mocks/full_dom_check.mjs` | 143 assertions, 0 failed, 0 page errors, pass: true on the wording build; the published v53 (the same wording plus the 10/9 ADP refresh) carries its own run in `arena/results/full_dom_check_2026-10-09_v53.json` (`after-report-2026-10-09-market.md` §6) |
| deck `scripts/repeat_market_check.py` | 21 of 21 mocks replayed on the wording build; 12 FLAGGED, 5 near misses — the v52 set with the same verdicts; the published v53's run is `arena/results/repeat_market_check_2026-10-09_v53.json` (the market report) |
| deck `scripts/identity_check.py` | exit 0; 41 players, 49 lines (§5) |
| kit `report/check_report.py` | REPORT GATE: PASS (structure, publication rule, pull-log row); exit 0 |
| deck `judgment_open_items.py --check-report` | receipts check PASS — all 10 flagged names carry a receipts row; exit 0 |
| deck `repeat_market_check.py --check-report` | REPEAT-NAME CHECK: PASS — 12 flagged names, each with a row (21 of 21 mocks replayed on the wording build); exit 0 |
| artifact publish | Version 53 (version id 1791570495-d551) at the standing URL after a fresh read of the live version (1791555525-2e7a, the v52 publish); the page's sha256 8978f6cde216, the file committed as deck 1c97b7e |

## 7. Watchlist / open items

- **WO-5, 10/11 pass** — the queue in its new order: (5) steal and block departures (Daniels first), then
  Okongwu FG%, Gobert FT%, Fox and Duren points, Filipowski; (6) the identity listing (§5); then the
  standing items (Flagg, the LINE QUESTIONED names, Acuff, Mathurin, Rollins/Jerome, Castle, Lendeborg);
  `range_check.py --check-report` and `identity_check.py --check-report` on the report.
- **After the draft** — D-RN-4; the per-player expected-games model and the anchor review (D-1009-2).
- **The Macao game** — its box score is the 10/11 pull's, with the 10/10 slate.
- Everything carried from `after-report-2026-10-09.md` §10 stands.

## Open-item receipts

| player | query run (2026-10-09) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (`after-report-2026-10-09.md`, receipts dated 10/9) | all HELD or unsigned on 2026-10-09; nothing changed since — this report did no research |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 0bffe01c043f), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 21 of 21 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-06.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-06.csv`, `hashtag-2026-10-06.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| PJ Washington | 17 of 21 | 87 | 148 | 178 | 144 | 141 | 121 | ast 2.4 vs 1.9-2; tov 1.5 vs 1.7-1.8; fg_pct .470 vs .448-.451; ft_pct .750 vs .698-.703 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Payton Pritchard | 16 of 21 | 37 | 82 | 33 | 90 | 92 | 72 | stl 1 vs 0.7-0.8; tpm 3.8 vs 3-3.2; tov 2 vs 1.3-1.3; ft_pct .850 vs .873-.875 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 15 of 21 | 28 | 65 | 60 | 56 | 43 | 44 | pts 18.5 vs 16.4-17; ast 2.3 vs 2.1-2.1; ft_pct .805 vs .813-.819 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Sandro Mamukelashvili | 15 of 21 | 81 | 169 | 138 | 105 | 153 | 120 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Daniel Gafford | 10 of 21 | 90 | 180 | 188 | 180 | 161 | 155 | pts 10.5 vs 9.1-9.8; reb 7.5 vs 5.8-6.5; ast 1.5 vs 1.1-1.2; blk 1.7 vs 1.2-1.4; fg_pct .700 vs .648-.689; ft_pct .700 vs .671-.687 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Jalen Suggs | 10 of 21 | 59 | 108 | 89 | 54 | 84 | 99 | pts 17 vs 14.1-15.1; ast 4 vs 4.8-5 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 9 of 21 | 82 | 143 | 94 | 121 | 137 | 98 | reb 7.5 vs 5.5-6.9; tpm 0.9 vs 1.2-1.3; fg_pct .520 vs .447-.498; ft_pct .740 vs .765-.828 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Isaiah Hartenstein | 7 of 21 | 75 | 104 | 141 | 92 | 100 | 102 | pts 11.5 vs 9.1-10.5; reb 11 vs 9.2-10.3; fg_pct .585 vs .597-.611; ft_pct .680 vs .642-.656 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Zach LaVine | 6 of 21 | 56 | 101 | 162 | 68 | 77 | 118 | pts 22.5 vs 17-21.1; reb 4.5 vs 3.1-3.6; ast 4 vs 2.8-3.4; tov 2.6 vs 2-2.4 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 5 of 21 | 89 | 141 | 122 | 131 | 125 | 123 | pts 16.8 vs 13.4-15.1; tov 1.5 vs 1-1.2; fg_pct .465 vs .432-.443 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Dyson Daniels | 5 of 21 | 11 | 62 | 20 | 65 | 56 | 53 | pts 14.5 vs 11.3-11.8; stl 3 vs 2-2.4; tpm 1.1 vs 0.5-0.6; fg_pct .495 vs .501-.513 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Saddiq Bey | 5 of 21 | 95 | 174 | 109 | 132 | 169 | 143 | blk 0.4 vs 0.1-0.1; tpm 2.4 vs 1.8-2; tov 1.5 vs 0.8-0.9 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Karl-Anthony Towns (16 mocks, value 6, market 15); Jalen Williams (15 mocks, value 16, market 39); Derrick White (11 mocks, value 24, market 45); Jalen Johnson (6 mocks, value 13, market 11); Mikal Bridges (6 mocks, value 61, market 83).

The twelve flagged names and their verdicts are the v52 set (the pool is byte-identical to the morning's); the market rank each row prints is the 10/6 price. The 10/9 ADP refresh that follows this report re-runs the check on its own page (`after-report-2026-10-09-market.md`).

## Bounds

- One season of backtest (2025-26) is the only out-of-sample record; whether steals' unpredictability is
  structural or a one-year effect is not knowable from it.
- The backtest's "shipped rule" reproduces today's engine over last season's pool; the 0.78 itself was
  arena-calibrated under that rule, which is why the anchor stays and the flatness is the post-draft target.
- The identity threshold (1.0) is a choice; the listing is 41 players at 1.0 and 15 at max(1.0, 8%). Measured on the
  verified 2025-26 actual lines (`after-report-2026-10-09-market.md` §4), rounding alone moves the identity by at most 0.164
  (p95 0.108; 432 players with 25+ games), so a gap above 1.0 is never rounding.
- The kit board's new exclusions change nothing the owner sees on draft night (the deck already excluded them);
  they keep the two planes' boards honest with each other.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-1009-1 | kit exclusion class — **applied** (owner yes): GP ≤ 25 rows off the board and pool | — |
| D-1009-2 | the discount's zero — **wording applied**, the rule **kept** by the backtest (owner yes to the recommendation); the anchor review and the per-player games model are post-draft | — |
| D-1009-3 | points identity — **the check and the acceptance item applied**; the reconciliation is Sunday's | — |
| D-1009-4 | WO-5's order of work — **applied** to the work order | — |
| D-1009-5 | the identity threshold for Sunday's pass: (a) keep 1.0 — 41 players, 49 lines, every one reconciled or carrying two outlets; (b) widen to max(1.0, 8% of points) — the audit's 15, the high scorers' rounding tolerated | (a) 1.0 — the owner asked for no unexplained gaps |

## Provenance and bounds

- Inputs: `arena/results/category_audit_2026-10-09.json` (the morning's audit), `arena/results/fix_backtest_2026-10-09.json`
  (the backtest, deck PR #91), `arena/data/players_2025-10-21.csv`, `arena/results/tuning_2026-10-08/bref_pergame_2025-26.csv`
  and `bref_pergame_2024-25.csv`; the committed 10/09 boards as the pre-change snapshots.
- Every number in §3, §4 and §5 is a script's output (`scratchpad fix1009/`, the two records); every gate line is the
  command's own output.

## In plain language

**What I did.** Everything from this afternoon's recommendations that can be done before Sunday, in both repos:

1. **The kit board now drops injured-out players the way it drops unsigned ones.** Butler, Lively, Mark Williams,
   Shaedon Sharpe, Nurkić and DiVincenzo are off it (Strus and Moody too, who were already below 200). I wrote the
   test before the fix and watched it fail, then pass. 143 players shuffle by a few spots at most; your top 60 is
   untouched. The deck — your draft-night board — already did this, so nothing changes on 10/14.
2. **The injury-discount rule stays as it is, and the code now says what it actually does.** The deck's
   documentation and the page's fine print called the zero line "replacement"; it's the average draftable player.
   Last season's replay showed that moving it would have made the rankings slightly worse, so only the words
   changed. The real fix — a per-player games estimate instead of one flat 0.78 — is on the post-draft list.
3. **There's now a mechanical check for projections whose points don't match their shooting**, with its own
   tests (written first, failing first), and Sunday's refresh can't be accepted until every flagged line is either
   reconciled or explained by two sources. Today's first run flags 41 players at the strict ±1.0 you asked for
   (D-1009-5 lets you loosen it to 15 if you'd rather).
4. **Sunday's refresh has its marching order written down:** steals and blocks first — Daniels at the top —
   because last season our departures from a player's prior season were right about three times out of four in
   points, rebounds and assists, but only half the time in steals and blocks. Then the identity list, then the
   standing items.

**What I did not do.** I did not touch any projection today. That's Sunday's pass, when every team has two
games on the record; doing it twice would double the churn for no gain.

**Verification.** Each change was tested before it was trusted: the kit's new engine test failed first (2 of 4) and then passed (4 of 4) and the board regenerates byte-identical on a second run; the deck's five new gate cases failed first (5 of 52) and then passed (52 of 52); the deck's arithmetic was re-checked against its independent Python twin at 364 owner turns across 28 recorded drafts (exact match, so the wording change moved no number); the page passed its 143-assertion browser check and the repeat-name replay of 21 mocks; every report gate passed; the published page is the committed file. Nothing here is a projection change — those are Sunday's.

**Your one new decision.** D-1009-5, the identity threshold (default: keep the strict 1.0).
