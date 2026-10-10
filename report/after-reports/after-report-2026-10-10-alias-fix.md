# After-report — 2026-10-10: the repeat-name check read two outside lists under the wrong spelling (D-RN-6), fixed red-first

**Owner request (2026-10-10, verbatim):** "Fix the alias defect." — the defect surfaced the same morning while answering the owner's Eason-versus-Herbert-Jones question: the standing repeat-name market check (D-RN-1) printed Jones as absent from Yahoo's and Rotoworld's lists (`>490`, `>200`) when both list him under the kit's documented spelling, Herb Jones. **Method:** the fix is a loader that reads the kit's spelling-alias table (`report/market/build_market.py` ALIASES) as a literal and resolves every name on both sides of the join through it; two red-first gate cases fail on the old script and pass on the new; the check re-ran on the live v54 page and its record was diffed mechanically against the mock 73 run. Verification: this file passes `report/check_report.py`, the deck's `repeat_market_check.py --check-report` and `judgment_open_items.py --check-report`.

Pull window: 2026-10-10 → 2026-10-10 (no roster pull; a gate fix on the deck plane and its receipts on this one).

**Headline.** Herbert Jones's outside receipts are Yahoo 147 and Rotoworld 134, not `>490` and `>200`; his verdict (LINE QUESTIONED, all four outside ranks 25+ places below our 74) and the flagged set (14 names on 23 of 23 mocks) are unchanged. The check now resolves spellings through the kit's alias table (10 spellings, 5 players); the deck's gate suite carries two new cases (2 of 54 red on the old script, 54 of 54 green on the final files, twice); the two 10/09 reports that printed the wrong receipts carry a dated correction paragraph under their table.

## 1. Roster changes

None — no pull, no row moved on either plane.

## 2. The defect

| item | what the record shows |
|---|---|
| where | deck `scripts/repeat_market_check.py`: `fold()` lowercases, strips diacritics, periods, apostrophes and suffixes, and nothing else; our pool spells him Herbert Jones, the kit's Yahoo projection file (`yahoo-proj-2026-10-06.csv`) and Rotoworld 9-cat file (`rotoworld-9cat-2026-10-05.csv`) spell him Herb Jones, so the lookup missed and printed one place past each list's end |
| printed (10/09, mocks 72 and 73) | Yahoo Rank `>490`, Hashtag 169, Rotoworld `>200`, RotoBaller `>250`; cells `—` |
| on file | Yahoo projected rank 147 (yrank; XRank 134 in the same file is the card's market column), Hashtag 169 (spelled Herbert there), Rotoworld 134, RotoBaller: not in its 250 (`>250` is real) |
| verdict | unchanged: 147, 169, 134 and >250 all sit 25+ places below our 74, so LINE QUESTIONED stands and Jones stays on Sunday's WO-5 re-derivation |
| cells | still `—`: the cell check needs all three outside per-game lines (Yahoo, Hashtag, RotoBaller) and RotoBaller has no Jones line |
| scope | the only affected name: of the 14 flagged and 5 near-miss names, Jones alone had a not-found receipt whose file carries a same-surname row under another first name (measured over the m73 record and the four files) |
| the kit's intake | unaffected: `build_market.py`, `yahoo_market.py`, `third_party_market.py`, `hashtag_pdf_market.py` and `adp_refresh.py` all resolve through ALIASES (Herb/Herbert Jones, Cam/Cameron Johnson, Nic/Nicolas Claxton, Alex/Alexandre Sarr, Egor Demin/Dёmin); the deck's check had its own fold with no table |

## 3. The fix (deck plane)

- `kit_aliases(kit)` parses `report/market/build_market.py` with `ast` and reads the `ALIASES` assignment as a literal — never an import, since the module is a script (the fixture's copy exits if imported). Every spelling, canonical or variant, keys to the canonical fold; a kit without the table (the suite's fixture kits) yields an empty map and the old behaviour.
- `canon(name, idx)` = `fold` then the table. Applied to our pool names, to every outside rank and line file, to the flagged lookup, and to the report gate's table rows — so a report may write either documented spelling.
- The run record carries `aliases` (players with an alias: 5 on the live kit, 10 spellings) and `alias_file`; the printed section says which.
- Rule going forward (DATA-PULL.md): a new spelling goes into the kit's table, never into the deck script.

## 4. Gates (2026-10-10)

| check | evidence |
|---|---|
| `test_gates.py` against the OLD script, the two new cases in place | 2 of 54 cases FAILED — exactly the two D-RN-6 cases (the flagged row printed `>490`/`>200` and no alias count; the report gate refused the kit's spelling Herb Jones) |
| `test_gates.py` against the new script, first run | 1 of 54 FAILED: the first RN-6 case expected the section to count the fixture's two alias players as "2 entries" while the record counted the four spellings; the record now counts players (`aliases` 5 on the live kit) and the case expects "2 players" — a wording mismatch in the new case, not a resolution failure (the row printed 147 / 169 / 134 / >250 on that run) |
| `test_gates.py` on the final files, run 1 and run 2 | all 54 cases passed, both runs |
| `test_card.py` / `test_draft.py` | 99 / 65 passed (the page and engine are untouched; parity and the DOM drive were not re-run — nothing they measure changed) |
| live re-run on the v54 page (`arena/results/repeat_market_check_2026-10-10_alias.json`) | 23 of 23 mocks replayed, 14 flagged, 5 near misses; page sha256 a771018d8dd3 (same as the m73 run) |
| mechanical diff against `repeat_market_check_2026-10-09_m73.json` | mocks, replayed, failed, thresholds, rank files, line files, every mock's 🎯 list, counts, near misses: identical; flagged names identical (14); one field differs — Herbert Jones `outside`: Yahoo Rank `>490` → 147, Rotoworld `>200` → 134; the new keys `aliases` 5 / `alias_file` |
| `repeat_market_check.py --check-report` on `after-report-2026-10-09-draft73.md` and on this file | PASS (14 flagged names, each with a row) |
| `report/check_report.py` on the two annotated 10/09 reports and on this file | PASS |

## 5. What changes for Sunday

Nothing in the queue: Jones was already on the WO-5 re-derivation as a LINE QUESTIONED name, and the four other alias players (Cameron Johnson, Nicolas Claxton, Alexandre Sarr, Egor Demin) are not flagged today. The corrected receipts replace the wrong ones in the record: the mock 72 and mock 73 reports keep their tables as printed on 10/09 and carry a dated correction paragraph beneath them pointing here.

## Watchlist

- Herbert Jones: LINE QUESTIONED on four outside ranks (147 / 169 / 134 / >250 against our 74); Sunday's pass re-derives him with two dated outlets. The engine re-runs of 2026-10-10 (scratch copies, nothing committed) put him at rank 97 on his three-full-season steal rate and behind Tari Eason on Yahoo's line.
- The other four alias players: covered by the loader the day any of them is flagged.

## Open-item receipts

| item | query run (2026-10-10) | dated finding |
|---|---|---|
| (this fix) | machine replay only — no web research in this report | the day's roster receipts are the 2026-10-09 pull's (`after-report-2026-10-09.md`) and research pass's (`after-report-2026-10-09-research.md`); nothing pulled today |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the 2026-10-09 pull and research pass, the previous day (after-report-2026-10-09.md, after-report-2026-10-09-research.md, receipts dated 10/9) | all HELD or unsigned on 2026-10-09; no pull today, nothing changed on the record since |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 a771018d8dd3), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 23 of 23 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-09.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-06.csv`, `hashtag-2026-10-09.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 5 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| PJ Washington | 19 of 23 | 87 | 151 | 178 | 144 | 141 | 121 | ast 2.4 vs 1.9-2; tov 1.5 vs 1.7-1.8; fg_pct .470 vs .448-.451; ft_pct .750 vs .698-.703 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Payton Pritchard | 18 of 23 | 37 | 83 | 33 | 90 | 92 | 72 | stl 1 vs 0.7-0.8; tpm 3.8 vs 3-3.2; tov 2 vs 1.3-1.3; ft_pct .850 vs .873-.875 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 17 of 23 | 28 | 65 | 60 | 56 | 43 | 44 | pts 18.5 vs 16.4-17; ast 2.3 vs 2.1-2.1; ft_pct .805 vs .813-.819 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Sandro Mamukelashvili | 17 of 23 | 81 | 169 | 138 | 105 | 153 | 120 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Daniel Gafford | 11 of 23 | 90 | 181 | 188 | 180 | 161 | 155 | pts 10.5 vs 9.1-9.8; reb 7.5 vs 5.8-6.5; ast 1.5 vs 1.1-1.2; blk 1.7 vs 1.2-1.4; fg_pct .700 vs .648-.689; ft_pct .700 vs .671-.687 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Jalen Suggs | 11 of 23 | 59 | 105 | 89 | 54 | 84 | 99 | pts 17 vs 14.1-15.1; ast 4 vs 4.8-5 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 10 of 23 | 82 | 144 | 94 | 121 | 137 | 98 | reb 7.5 vs 5.5-6.9; tpm 0.9 vs 1.2-1.3; fg_pct .520 vs .447-.498; ft_pct .740 vs .765-.828 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Isaiah Hartenstein | 7 of 23 | 75 | 104 | 141 | 92 | 100 | 102 | pts 11.5 vs 9.1-10.5; reb 11 vs 9.2-10.3; fg_pct .585 vs .597-.611; ft_pct .680 vs .642-.656 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Zach LaVine | 7 of 23 | 56 | 100 | 162 | 68 | 77 | 118 | pts 22.5 vs 17-21.1; reb 4.5 vs 3.1-3.6; ast 4 vs 2.8-3.4; tov 2.6 vs 2-2.4 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 5 of 23 | 89 | 142 | 122 | 131 | 125 | 123 | pts 16.8 vs 13.4-15.1; tov 1.5 vs 1-1.2; fg_pct .465 vs .432-.443 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Dyson Daniels | 5 of 23 | 11 | 62 | 20 | 64 | 56 | 53 | pts 14.5 vs 11.3-11.8; stl 3 vs 2-2.4; tpm 1.1 vs 0.5-0.6; fg_pct .495 vs .501-.513 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Herbert Jones | 5 of 23 | 74 | 182 | 147 | 169 | 134 | >250 | — | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Josh Hart | 5 of 23 | 67 | 96 | 68 | 84 | 91 | 94 | pts 13.5 vs 11.9-12.2; tpm 1 vs 1.2-1.5; fg_pct .520 vs .498-.503; ft_pct .780 vs .751-.759 | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Saddiq Bey | 5 of 23 | 95 | 176 | 109 | 132 | 169 | 143 | blk 0.4 vs 0.1-0.1; tpm 2.4 vs 1.8-2; tov 1.5 vs 0.8-0.9 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Karl-Anthony Towns (18 mocks, value 6, market 15); Jalen Williams (15 mocks, value 16, market 39); Derrick White (12 mocks, value 24, market 44); Jalen Johnson (6 mocks, value 13, market 11); Mikal Bridges (6 mocks, value 61, market 82).

## Bounds

- The alias table is the kit's; a spelling absent from it still reads as absent, by D-RN-1's rule (one place past the list's end). That is the designed behaviour, now with the documented spellings honoured.
- The cell check for Jones cannot run until a RotoBaller line exists for him; the `—` is a real absence, not the defect.
- Grades, lines and the page did not change; v54 stays published.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-RN-6 | The check resolves spellings through the kit's alias table (applied, red-first, 54 of 54). Keep it, with new spellings added only in the kit's table? | keep it |
| D-1010-1 | The owner's 2026-10-10 note: a contending team's player (Eason, Houston) has more to play for than one on a rebuilding team (Jones, New Orleans), who is more likely to lose minutes or sit once his team is out of the race — a late-season availability effect the season-average line cannot carry. Fold a team-context term into the post-draft expected-games model (WO-7, the per-player expected-games replacement for the flat 0.78), evidence-gated by last season's game logs: did rotation players on the bottom teams lose games or minutes in the fantasy playoff weeks relative to their first twenty weeks? | no model change before the 10/14 lock; the premise is the owner's and is not verified from sources this session; the experiment joins the post-draft expected-games item |
| D73-1, D72-1, D71-1, D70-1, D69-1, D68-1..3, D61-4, D-RN-1..5, D67-1..6, D66-1, D-V4-1, D-CAST-1..4, D62-1..3, D-1008-1..3, D-1009-1..13 and earlier | carried | carried |

## Provenance

- Deck: `scripts/repeat_market_check.py` (loader + canon), `scripts/test_gates.py` (two D-RN-6 cases), `arena/results/repeat_market_check_2026-10-10_alias.json` (the corrected run; the m73 run `repeat_market_check_2026-10-09_m73.json` stays as the 10/09 record).
- Kit: this file; correction paragraphs under §8 of `after-report-2026-10-09-draft72.md` and `after-report-2026-10-09-draft73.md`; `DATA-PULL.md` (the alias rule); `report/pull-log.md`.
- The outside receipts quoted here are read from `report/market/yahoo-proj-2026-10-06.csv` (yrank 147, xrank 134), `hashtag-2026-10-09.csv` (169), `rotoworld-9cat-2026-10-05.csv` (134) and `rotoballer-2026-09-29.csv` (no row).
- Not verified: nothing here rests on web research.

## In plain language

**What was wrong.** The check that guards against the card recommending the same flattering line draft after draft looked up "Herbert Jones" in two lists that call him "Herb Jones", and told you those lists had never heard of him. They rank him 147 and 134.

**What it changes.** Nothing in the verdict: every outside list still has him far below our 74, so he stays on Sunday's re-derivation. The receipts are now right, the check reads the kit's spelling table, and two new gate cases keep it that way.

**Your decisions.** D-RN-6 keep the fix (default yes). D-1010-1 your team-context point goes on the post-draft expected-games work as an experiment (default: nothing moves before Wednesday's draft).
