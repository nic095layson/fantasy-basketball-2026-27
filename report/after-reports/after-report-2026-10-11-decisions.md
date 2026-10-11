# After-report — 2026-10-11: the owner's three decisions applied to the deck (LaVine a, Lendeborg c, Fox same as LaVine); deck v57

**Owner request (2026-10-11, verbatim):** "Proceed with: LaVine - a / Lendeborg - c / Fox - same as LaVine" — the answers to D-1011-1 and D-1011-2 from the morning's pull report, plus Fox by direct instruction.

Pull window: 2026-10-11 → 2026-10-11 (no roster pull; the judgment layer on the deck plane and its record on this one).
Gate: `check_provenance.py` → PASS (no kit row changed); the deck chain is green on the v57 page (§4).

**Headline.** All three decisions are applied exactly as given — LaVine −0.10, Lendeborg +0.10 (Lendeborg only; Acuff unchanged), Fox −0.10 — and every one of them is a **label, not a demotion**: since the 2026-08-04 blend50 ship the decision card's order is `rankCard` (blend50, then ΔECW, then name) and the judgment adjustment rides the row as metadata (`fs` for tooltips, the "· judgment −0.10" suffix and the owner's words behind it). The morning sheet said (a) "moves him a few card places" — that was wrong and is corrected in the 10/11 report. Measured, not assumed: the 🎯 is the same name at 299 of 299 owner turns across the 23 replayed rooms under the v56 and v57 pages; the per-player 🎯 counts are identical; the real page rendered in Chromium at the turns where each man was the system pick shows the same Top-5 order on both pages (all demo turns), with the judgment value and the owner’s words now in that row’s tooltips (the score tooltip reads “· judgment −0.10”, the † tooltip carries the OWNER NOTE / OWNER DECISION text; the visible row text is unchanged since the 2026-08-05 concision pass); parity stays EXACT because the ordering key never read the judgment value. The lever that does move a man off the card is the veto (`doNotDraft`), and the lever that moves him on it is the line — D-1011-4 puts that choice to the owner.

## 1. Roster changes

None — no pull, no row moved on either plane; `data/players.csv` is byte-identical to the v56 build (gate 4's quiet-day path, `--no-pool-changes`).

## 2. What was applied (deck plane, `docs/draft-deck.html` JUDGMENT block)

| card | before (v56, this morning) | after (v57) | decision |
|---|---|---|---|
| Zach LaVine | adj 0, the owner's note verbatim, D-1011-1 pending | **adj −0.10**, the decision appended ("OWNER DECISION 2026-10-11 (verbatim: 'LaVine - a')") | D-1011-1 (a) |
| Yaxel Lendeborg | adj 0, the owner's note verbatim | **adj +0.10**, the decision appended ("'Lendeborg - c'": Lendeborg only; the committed line untouched, WO-5 owns it) | D-1011-2 (c) |
| Darius Acuff Jr. | adj 0, the owner's note verbatim | adj 0, the decision recorded ("(c) — Lendeborg only; no adjustment on Acuff") | D-1011-2 (c) |
| De'Aaron Fox | no card | **new card, adj −0.10** ("OWNER DECISION 2026-10-11 (verbatim): 'Fox - same as LaVine'"), no rationale attributed beyond the owner's words; the two missed preseason games noted from the feed | D-1011-3 (decided by the owner, applied) |

The colophon's owner-notes sentence now states the decisions. JUDGMENT date 2026-10-11 (gate 5 satisfied); freshness re-stamped with `--no-pool-changes`; `build_deck.py`: planes 315 shared · team 0 · exclusion 0 · drift 0 · propagation 0 · waived 0 (no waiver needed — the kit snapshot is unchanged since v56); pool 3294e3cb7512 (= v56); "safe to publish".

## 3. What the adjustments do — and do not do (measured)

**The code.** The card's rows are built at `app` lines 3281–3287: `adj: j ? j.adj : 0, why: j ? j.why : "", … fs: r.s + adj + bonus`; the order is `rankCard(...)` — `sort((a, b) => b.ds - a.ds || b.decw - a.decw || name)`, the engine's blend50 key, which never reads `adj` or `fs`. The comment at the call site (E9 ship, 2026-08-04) says it outright: "the Top-5 ORDER is the validated blend50 score at every seat — replacing the composite fs sort … Council/judgment/slide stay as metadata; fs is retained on rows for tooltips and REVERT-MAP rollback." The only renders of `adj` are the score tooltip’s suffix (“· judgment −0.10”, line 3446, `sc.dataset.tip`) and the `jdg` bit of the breakdown line, which the 2026-08-05 concision pass moved into the † tooltip (line 3451) — nothing in the visible row text. The engine block (`adjValue`, `decwScores`, `rankCard`) never references `JUDGMENT`; the parity harness exports exactly those, which is why parity has been EXACT with non-zero cards (Tatum +0.35, Maxey −0.10) all along.

**The replays (engine-level, the standing repeat-name instrument).** `repeat_market_check.py` on the v57 page: 23 of 23 mocks replayed, 14 flagged (4 LINE QUESTIONED, 10 SOURCES SPLIT), 5 near misses. The 🎯 per owner turn against the v56 run: 299 of 299 turns identical across 23 rooms; per-player 🎯 counts identical (42 names).

**The real page in Chromium (`card_dom_demo.mjs`, both pages, the same truncated committed states, sequential runs).** The turns chosen are ones where the repeat-name record has each man as the 🎯:

| turn | row on v57 | v56 page | v57 page | order |
|---|---|---|---|---|
| mock 51, pick 82 | 1 🎯 Zach LaVine | none | judgment -0.10 in the score tooltip; the † tooltip carries “OWNER NOTE 2026-10-11 (verbatim): 'not a fan of LaVine. Has let me down before in fantasy …” | same order; 0 page errors |
| mock 55, pick 63 | 1 🎯 De'Aaron Fox | none | judgment -0.10 in the score tooltip; the † tooltip carries “OWNER DECISION 2026-10-11 (verbatim): 'Fox - same as LaVine' — the LaVine treatment (D-101…” | same order; 0 page errors |
| mock 55, pick 63 | 5 Zach LaVine | none | judgment -0.10 in the score tooltip; the † tooltip carries “OWNER NOTE 2026-10-11 (verbatim): 'not a fan of LaVine. Has let me down before in fantasy …” | same order; 0 page errors |
| mock 67, pick 82 | 1 🎯 De'Aaron Fox | none | judgment -0.10 in the score tooltip; the † tooltip carries “OWNER DECISION 2026-10-11 (verbatim): 'Fox - same as LaVine' — the LaVine treatment (D-101…” | same order; 0 page errors |
| mock 67, pick 82 | 4 Zach LaVine | none | judgment -0.10 in the score tooltip; the † tooltip carries “OWNER NOTE 2026-10-11 (verbatim): 'not a fan of LaVine. Has let me down before in fantasy …” | same order; 0 page errors |
| mock 59, pick 106 | 1 🎯 Yaxel Lendeborg | none | judgment +0.10 in the score tooltip; the † tooltip carries “OWNER NOTE 2026-10-11 (verbatim): 'I'm bullish on Acuff, but especially Lendeborg. I reall…” | same order; 0 page errors |
| mock 62, pick 82 | 1 🎯 Yaxel Lendeborg | none | judgment +0.10 in the score tooltip; the † tooltip carries “OWNER NOTE 2026-10-11 (verbatim): 'I'm bullish on Acuff, but especially Lendeborg. I reall…” | same order; 0 page errors |

Every Top-5 order is the same on both pages at every demo turn; the judgment value and the owner’s words appear in the adjusted man’s row tooltips on v57 (hover the score for “· judgment −0.10”, the † for the words) and nowhere on v56; the visible row text (name, ΔECW, Mkt, plus-cats) is identical on both pages. The owner sees the flag on hover at the moment of the pick; the pick order has not changed.

## 4. Gates (2026-10-11, the v57 page)

| gate | evidence |
|---|---|
| `hoops.py freshness --stamp --no-pool-changes` | 2026-10-11, no pool change asserted; gate 4 agreed (pool hash = v56's) |
| `scripts/build_deck.py` | gates 1–7 + F8 pass, no waiver; round-trip OK; "safe to publish" |
| `scripts/check_parity.py` | PARITY: EXACT MATCH; exit 0 |
| `scripts/test_card.py` / `test_gates.py` / `test_draft.py` | CARD: all 99 cases passed / all 54 cases passed / all 65 cases passed; exit 0 each |
| `arena/mocks/full_dom_check.mjs` (draft_state_54) | 143 assertions, 0 failed, [] page errors, pass true (`arena/results/full_dom_check_2026-10-11_v57.json`); exit 0 |
| `scripts/repeat_market_check.py` | 23 of 23 mocks replayed, 14 flagged (4 LINE QUESTIONED, 10 SOURCES SPLIT), 5 near misses (`arena/results/repeat_market_check_2026-10-11_v57.json`); exit 0 |
| `card_dom_demo.mjs` (v56 page vs v57 page) | 5 owner turns rendered on each; page errors 0 / 0; orders identical |
| `report/check_provenance.py` | PASS — no kit row changed |
| `report/check_report.py` | REPORT GATE: PASS — after-report-2026-10-11-decisions.md (structure, publication rule, pull-log row); exit 0 |
| `report/check_derived.py` | DERIVED: all 21 dated artifacts reproduce byte-for-byte from their pinned inputs; exit 0 |
| artifact publish | Version 57, id 1791705161-a5b1, the standing URL; the served file carries the built page byte-for-byte inside the service's 364-byte wrapper; manifest built 2026-10-11 |

## 5. What this means for Wednesday

- LaVine and Fox: when either is on your Top-5, his score tooltip carries “· judgment −0.10” and the † tooltip your words; the 🎯 can still be him if the blend puts him first. If the intent is that the card never offers him, that is the veto (D-1011-4 (a)).
- Lendeborg: his score tooltip carries “· judgment +0.10” and the † tooltip your note; he reaches the card where the blend puts him (value rank 82 on the committed line). If the intent is that he climbs the card, that is the line — the WO-5 pass today re-derives it from the three starts (D-1007-1), and the engine ranks him from there.
- Acuff: unchanged, the line on today's WO-5 pass (D-1006-1).

## Watchlist

- **D-1011-4** (below) — the owner's call on whether the judgment layer should move the card, and for whom.
- The Sunday WO-5 projection pass (Lendeborg, Acuff, Mathurin, Rollins, Daniels' steals, Flagg, the four questioned lines).
- The next pull: the Macao rematch, Magic–Cavaliers, Bucks–Hornets, Bulls–Nuggets.

## Open-item receipts

| item | query run (2026-10-11) | dated finding |
|---|---|---|
| (these decisions) | machine replay only — no web research in this report | the day's receipts are the morning pull's (`after-report-2026-10-11.md`); nothing pulled here |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the 2026-10-11 early pull, the same morning (`after-report-2026-10-11.md`, §3 and its Open-item receipts table) | HELD, all ten; the JUDGMENT receipts on the page are dated 2026-10-11 |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 5e2c86b0fa23), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 23 of 23 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-09.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-06.csv`, `hashtag-2026-10-09.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 5 players).

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

- The "no rank moves" finding rests on the page's own code (cited by line), the engine-level replays (273 owner turns) and the Chromium renders at the chosen turns; it is not a claim about every possible state, but the ordering key is the same function at every state.
- The DOM demo renders truncated committed states through the page's import path; the on-the-clock turn is the one the record names, and only the card rows and the status strip are read.
- Fox's −0.10 is applied on the owner's words alone ("same as LaVine"); no rationale is attributed to him beyond that.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-1011-4 | The judgment adjustment is a label, not a rank change (§3). If the intent behind LaVine (a) and Fox was to keep them off YOUR card, the lever is the veto; if the intent behind Lendeborg (c) was to move him up, the lever is the line. Options: (a) add LaVine and/or Fox to `doNotDraft` (they leave your candidate pool only; the room, rosters and matrix still see them) — name which; (b) keep the labels as they are (the card flags them at the pick, order unchanged); (c) make the judgment adjustment a term in the card order — an engine change against the 2026-08-04 measurement that retired the composite sort, so it would ship only through a pre-registered replay of the live rooms on file (the D58-3 bar), not by fiat. | (b) — the decisions as given are applied and visible; a veto or an engine change is the owner's to say in so many words |
| D-1011-1 | LaVine — (a) applied as a −0.10 label (the morning sheet's "moves him a few card places" was wrong; corrected in that report) | closed by the owner |
| D-1011-2 | Lendeborg/Acuff — (c) applied: Lendeborg +0.10 label, Acuff unchanged | closed by the owner |
| D-1011-3 | Fox — −0.10 label by the owner's direct call ("same as LaVine") | closed by the owner |
| D-1010-2 and earlier | carried | carried |

## Provenance

- Inputs: the owner's message (2026-10-11, verbatim above); `docs/draft-deck.html` at v56 (`scratchpad pull1011/decisions/page_v56.html`) and the v57 build; `arena/results/repeat_market_check_2026-10-11.json` (v56) and `_v57.json`; the 30 committed states in `arena/data/states/`.
- Scripts: `judgment_decisions.py` (the three cards and the colophon sentence, exact anchors), `chain.sh` (`chain.log`), `card_dom_demo.mjs` (committed to the deck as `arena/mocks/card_dom_demo.mjs`; results `arena/results/card_dom_demo_2026-10-11_v56.json`, `_v57.json`), `write_report.py` (this file).
- Code cited: `docs/draft-deck.html` app block lines 3262–3296 (the card assembly and the E9 comment), 3446 and 3451 (the only renders of `adj`), engine block `rankCard` (the ordering key); `scripts/check_parity.py` (exports `rankCard`, `decwScores`, `adjValue` — never `JUDGMENT`).

## In plain language

**What I did.** Exactly what you said: LaVine −0.10, Lendeborg +0.10 (Acuff untouched), Fox −0.10. The deck is rebuilt and republished as v57 with every gate green.

**What I found while doing it.** A judgment adjustment on this deck is a flag in the card row’s hover tooltips, not a demotion or a promotion. The card's order has been the pure blend50 score since August 4, when the composite sort was retired because the tested card beat it; the adjustment and your words ride along on the row for you to see at the pick. I checked it three ways: the code, the replays of all 23 rooms on file (the system pick is the same name at every one of the 273 owner turns under both pages), and the real page rendered in a browser at the turns where each man was the pick (same order, the suffix now on his row). My sheet yesterday said (a) would move LaVine a few places. That was wrong, and the report says so.

**What you can still do.** If you want LaVine or Fox never offered to you, that is the veto, the same switch as Porziņģis; say the names. If you want Lendeborg higher on the card, that comes from his line, which today's projection pass re-derives from his three starts. If you want the judgment layer to actually move the card, that is an engine change and I would run it as a pre-registered replay first, not ship it on a Sunday.
