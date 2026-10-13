# After-report — the MG pass: minutes and games for the top-150 players on a new team or with a short base season, to the two October outlets' consensus

> **DRAFT** — written while the deck chain was still running: the verification rows marked pending, the repeat-name section and the pull-log row are filled when the chain is green. Not yet gated by `check_report.py`.

**Owner request (2026-10-13, verbatim):** "Proceed with council recommendations" — after the Council's 4–1 verdict earlier the same day: keep WO-5 as the basis, do not switch to expert projections, run a minutes-and-games pass on every top-150 player on a new team or with a base season under 50 games, reviewed against the expert consensus, moves on two dated outlets, the injury modifier untouched.

**What was analyzed:** kit `main` 2df5b22 and deck `main` 8ec736b as the starting point; the WO-5 lines (`wo5/out/lines_wo5_2026-10-12.json`) and range resolution; the two October projection outlets on file, Yahoo 10/06 (`market/yahoo-proj-2026-10-06.csv`) and Hashtag 10/12 (`market/hashtag-2026-10-12.csv`); the kit board as `rank_engine.py` ranks it.

**Method:** rules fixed before the pass ran (§2), applied by committed scripts (`report/mg/tools/`), through the WO-5 pipeline (`wo5_lines.py --minutes` → `wo5_apply.py` → the range rule to a fixed point), seeded with the committed 10/12 range resolution; every figure below comes from the files in `report/mg/out/`.

**Verification:** two controls before any change (§6); the change set guarded before the in-place write (15 rows, 0 unexpected); every tool run twice (second run changes nothing); kit gates; the deck build (gates 1–7 + F8) and the full chain (§7); publish after a fresh read, bytes verified.

Pull window: 2026-10-13 → 2026-10-13 (projection pass; today's roster verification 335/335, no roster change in the pool).

**Headline.** 47 candidates; 15 minutes moves (8 up, 7 down) and 5 games moves; 32 holds. The eight minutes-up players climb on both boards (Kel'el Ware 67 → 27, Giannis Antetokounmpo 58 → 35 on the deck and 39 on the kit, Franz Wagner 68 → 31/34, Darius Garland 103 → 63/62, John Collins 122 → 71, Jalen Williams 57 → 41/42); the seven minutes-down players fall (DeMar DeRozan 88 → 146/147, Grayson Allen 81 → 134/136, Royce O'Neale 125 → 180/179, Kelly Oubre Jr. 121 → 162/164, Joel Embiid 23 → 32 on the deck and 27 → 36 on the kit). The standing range rule re-ran on the result and re-fixed two of the fifteen (Dejounte Murray 29.1 → 29.2 minutes, Alex Sarr 27.2 → 26.8), so those two are holds in effect. The 17 movers' average distance to the expert consensus fell from 35.9 to 18.6 places, and the whole top-150's agreement with the experts rose from .847 to .860. The card at #10 is unchanged: no top-30 slot changed hands except Ware in and Embiid down (§5). Two things did not go to plan and are stated plainly: the deck build needed two named waivers for the games-only rows (§8), and the 10/12 claim that the pipeline rebuilds from scratch is only partly true (§6).

## 1. Roster changes

None. `verify_rosters.py` direct-complete ran today: 335/335 on ESPN's feed, 0 mismatches; the build's gate 7 found 0 team differences between the planes. (The live feed re-authored 12 lines of the evidence file `rosters_official.json`, none of them a pool row's team.)

## 2. The rules, fixed before the pass

- **Candidates:** the kit's top 150 (as `rank_engine.py` ranks them), players on a new team for 2026-27 (team on the line vs the last 2025-26 team on Basketball-Reference) or whose base season has under 50 games: **47** (30 on a new team, 21 with a short base; some both). Rookies have no base season and are not candidates.
- **MG-1 minutes.** References: Hashtag 10/12's stated minutes, and Yahoo 10/06's implied minutes (WO-5 minutes × the median across pts/reb/ast/tpm/tov of Yahoo's cell ÷ ours — the median so one rate difference cannot pose as minutes). Trigger: both references on the same side of the WO-5 minutes, each by 1.5+. New minutes = their mean, rounded to 0.1. Rates unchanged; steals and blocks ride along; points by the shooting identity. Applied as an override row naming both outlets; a 10/12 role move stands unless the same trigger fires against it (none did).
- **MG-2 games.** References: Yahoo and Hashtag games played. Trigger: both on the same side of the kit GP, each by 5+. New GP = their rounded mean. Kit column only — the deck's availability is tag-based, and tags come from injury news (D-MG-2).
- One reference only → hold, listed single-source (Deandre Ayton). The owner's Porziņģis veto is untouched (his minutes held anyway).
- **Disclosure:** the 1.5-minute and 5-game thresholds (about 5%, the range check's own tolerance) were chosen with the candidate table in view, before any file was written. That is a weaker pre-commitment than choosing them blind, and it is on the record.
- **Why the two outlets alone:** the range check's references include the player's own 2025-26 line, so a line that copies last season is never "outside the range" by construction — the check cannot catch the cases this pass exists for.

## 3. The moves

### MG-1 minutes — the 15 triggered moves (both outlets on the same side by 1.5+)

| player | why a candidate | WO-5 min | Hashtag 10/12 | Yahoo 10/06 implied | new min | pts before → after | deck rank | kit rank | range rule after |
|---|---|---|---|---|---|---|---|---|---|
| Joel Embiid | base under 50 games (2025-26, 38 G) | 31.6 | 29.4 | 29.4 | 29.4 | 26.9 → 25.1 | 23 → 32 | 27 → 36 | — |
| Jalen Williams | base under 50 games (2025-26, 33 G) | 28.4 | 31.2 | 31.3 | 31.2 | 17.2 → 19.0 | 57 → 41 | 56 → 42 | new cell(s) kept on the method: ast |
| Giannis Antetokounmpo | new team, base under 50 games (2025-26, 36 G) | 28.9 | 34.2 | 30.9 | 32.5 | 26.9 → 30.3 | 58 → 35 | 58 → 39 | new cell(s) kept on the method: tov |
| Kel'el Ware | new team (2025-26, 77 G) | 22.1 | 27.9 | 25.7 | 26.8 | 11.1 → 13.4 | 67 → 27 | 66 → 27 | — |
| Franz Wagner | base under 50 games (2025-26, 34 G) | 30.0 | 32.5 | 36.4 | 34.5 | 20.6 → 23.7 | 68 → 31 | 68 → 34 | new cell(s) kept on the method: reb |
| Grayson Allen | new team (2025-26, 51 G) | 28.8 | 24.0 | 25.2 | 24.6 | 16.8 → 14.4 | 81 → 134 | 82 → 136 | — |
| Dejounte Murray | base under 50 games (2024-25, 31 G) | 29.1 | 30.7 | 33.1 | 29.2 | 16.7 → 16.7 | 87 → 91 | 87 → 91 | re-fixed by R1 at 29.2 (factor 0.916) |
| DeMar DeRozan | new team (2025-26, 77 G) | 31.2 | 27.8 | 24.6 | 26.2 | 18.2 → 15.2 | 88 → 146 | 88 → 147 | — |
| Alex Sarr | base under 50 games (2025-26, 48 G) | 27.2 | 28.8 | 28.7 | 26.8 | 15.9 → 15.6 | 99 → 103 | 97 → 101 | re-fixed by R1 at 26.8 (factor 0.931) |
| Darius Garland | base under 50 games (2025-26, 45 G) | 29.1 | 31.4 | 32.4 | 31.9 | 18.2 → 20.0 | 103 → 63 | 102 → 62 | — |
| Tobias Harris | new team (2025-26, 63 G) | 27.7 | 26.2 | 23.8 | 25.0 | 13.3 → 12.0 | 111 → 140 | 111 → 138 | — |
| John Collins | new team (2025-26, 69 G) | 27.1 | 28.9 | 32.9 | 30.9 | 13.5 → 15.4 | 122 → 71 | 121 → 71 | — |
| Kelly Oubre | new team (2025-26, 50 G) | 31.5 | 28.2 | 26.7 | 27.4 | 13.9 → 12.1 | 121 → 162 | 123 → 164 | — |
| Royce O'Neale | new team (2025-26, 78 G) | 28.4 | 24.6 | 24.0 | 24.3 | 9.8 → 8.4 | 125 → 180 | 126 → 179 | — |
| Jerami Grant | new team (2025-26, 57 G) | 29.7 | 27.5 | 28.0 | 27.8 | 18.5 → 17.3 | 150 → 193 | 150 → 192 | — |

### MG-2 games — the 5 triggered moves (both outlets on the same side by 5+; kit column only)

| player | kit GP before → after | Yahoo 10/06 | Hashtag 10/12 | kit rank | deck plane |
|---|---|---|---|---|---|
| Jalen Williams | 74 → 68 | 69 | 68 | 56 → 42 | dated note only (availability is tag-based) |
| Franz Wagner | 74 → 66 | 67 | 64 | 68 → 34 | dated note only (availability is tag-based) |
| Jakob Poeltl | 66 → 58 | 58 | 58 | under 3 → under 3 | dated note only (availability is tag-based) |
| Mitchell Robinson | 58 → 64 | 63 | 65 | under 3 → under 3 | dated note only (availability is tag-based) |
| Jerami Grant | 64 → 54 | 59 | 50 | 150 → 192 | dated note only (availability is tag-based) |

### The 32 holds

| player | why a candidate | WO-5 min | Hashtag | Yahoo implied | minutes verdict | kit GP | Yahoo GP | Hashtag GP | games verdict |
|---|---|---|---|---|---|---|---|---|---|
| Kawhi Leonard | new team | 32.1 | 31.1 | 29.4 | hold: references split or within 1.5 min | 60 | 59 | 58 | hold: references split or within 5 games |
| Stephen Curry | base under 50 games | 30.9 | 31.6 | 32.9 | hold: references split or within 1.5 min | 62 | 67 | 60 | hold: references split or within 5 games |
| Lauri Markkanen | base under 50 games | 34.4 | 34.1 | 34.4 | hold: references split or within 1.5 min | 66 | 68 | 65 | hold: references split or within 5 games |
| Anthony Davis | new team | 29.6 | 31.1 | 29.6 | hold: references split or within 1.5 min | 55 | 58 | 59 | hold: references split or within 5 games |
| Walker Kessler | new team | 30.0 | 30.2 | 34 | hold: references split or within 1.5 min | 72 | 67 | 68 | hold: references split or within 5 games |
| Joel Embiid | base under 50 games | 31.6 | 29.4 | 29.4 | moved | 45 | 49 | 52 | hold: references split or within 5 games |
| Paul George | new team, base under 50 games | 30.7 | 31.2 | 26.6 | hold: references split or within 1.5 min | 60 | 59 | 58 | hold: references split or within 5 games |
| Jaren Jackson Jr | base under 50 games | 30.3 | 30.7 | 30.3 | hold: references split or within 1.5 min | 68 | 66 | 67 | hold: references split or within 5 games |
| LaMelo Ball | new team | 28.0 | 29.2 | 31.2 | hold: references split or within 1.5 min | 58 | 60 | 65 | hold: references split or within 5 games |
| Naz Reid | new team | 31.0 | 30.8 | 27.6 | hold: references split or within 1.5 min | 74 | 76 | 74 | hold: references split or within 5 games |
| Jaylen Brown | new team | 34.4 | 33.1 | 29.9 | hold: references split or within 1.5 min | 68 | 69 | 70 | hold: references split or within 5 games |
| LeBron James | new team | 33.1 | 32.1 | 30.9 | hold: references split or within 1.5 min | 55 | 66 | 54 | hold: references split or within 5 games |
| Giannis Antetokounmpo | new team, base under 50 games | 28.9 | 34.2 | 30.9 | moved | 67 | 68 | 69 | hold: references split or within 5 games |
| Tyler Herro | new team, base under 50 games | 31.3 | 31.8 | 37.4 | hold: references split or within 1.5 min | 70 | 66 | 64 | hold: references split or within 5 games |
| Kel'el Ware | new team | 22.1 | 27.9 | 25.7 | moved | 74 | 72 | 74 | hold: references split or within 5 games |
| Kristaps Porzingis | base under 50 games | 23.7 | 24.2 | 22.8 | hold: references split or within 1.5 min | 54 | 55 | 42 | hold: references split or within 5 games |
| Ivica Zubac | base under 50 games | 30.1 | 30.4 | 30.4 | hold: references split or within 1.5 min | 72 | 72 | 72 | hold: references split or within 5 games |
| Grayson Allen | new team | 28.8 | 24 | 25.2 | moved | 64 | 68 | 64 | hold: references split or within 5 games |
| Norman Powell | new team | 29.6 | 29.6 | 27 | hold: references split or within 1.5 min | 66 | 66 | 65 | hold: references split or within 5 games |
| Brandon Ingram | new team | 33.8 | 34.1 | 34.6 | hold: references split or within 1.5 min | 48 | 68 | 42 | hold: references split or within 5 games |
| Dejounte Murray | base under 50 games | 29.1 | 30.7 | 33.1 | moved | 62 | 65 | 64 | hold: references split or within 5 games |
| DeMar DeRozan | new team | 31.2 | 27.8 | 24.6 | moved | 70 | 74 | 72 | hold: references split or within 5 games |
| Alex Sarr | base under 50 games | 27.2 | 28.8 | 28.7 | moved | 72 | 69 | 68 | hold: references split or within 5 games |
| Miles Bridges | new team | 31.0 | 30.1 | 32.9 | hold: references split or within 1.5 min | 72 | 71 | 72 | hold: references split or within 5 games |
| Darius Garland | base under 50 games | 29.1 | 31.4 | 32.4 | moved | 70 | 68 | 68 | hold: references split or within 5 games |
| Peyton Watson | new team | 29.6 | 30.1 | 25.6 | hold: references split or within 1.5 min | 70 | 71 | 70 | hold: references split or within 5 games |
| Tobias Harris | new team | 27.7 | 26.2 | 23.8 | moved | 68 | 71 | 65 | hold: references split or within 5 games |
| Julius Randle | new team | 33.0 | 32.6 | 34.3 | hold: references split or within 1.5 min | 68 | 72 | 75 | hold: references split or within 5 games |
| Isaiah Hartenstein | base under 50 games | 24.2 | 26.4 | 22.9 | hold: references split or within 1.5 min | 66 | 63 | 68 | hold: references split or within 5 games |
| Deandre Ayton | new team | 27.2 | — | 24.2 | hold: single source (no Hashtag line) [SINGLE-SOURCE] | 62 | 66 | — | hold: single source [SINGLE-SOURCE] |
| Jakob Poeltl | base under 50 games | 25.0 | 26.5 | 24.9 | hold: references split or within 1.5 min | 66 | 58 | 58 | moved |
| John Collins | new team | 27.1 | 28.9 | 32.9 | moved | 64 | 65 | 70 | hold: references split or within 5 games |
| Kelly Oubre | new team | 31.5 | 28.2 | 26.7 | moved | 68 | 68 | 64 | hold: references split or within 5 games |
| Christian Braun | base under 50 games | 31.8 | 31.8 | 33.8 | hold: references split or within 1.5 min | 72 | 74 | 72 | hold: references split or within 5 games |
| Kyshawn George | base under 50 games | 29.0 | 29 | 25.1 | hold: references split or within 1.5 min | 68 | 68 | 68 | hold: references split or within 5 games |
| Royce O'Neale | new team | 28.4 | 24.6 | 24 | moved | 70 | 76 | 70 | hold: references split or within 5 games |
| Santi Aldama | new team, base under 50 games | 27.9 | 26.5 | 22.9 | hold: references split or within 1.5 min | 68 | 68 | 64 | hold: references split or within 5 games |
| Nic Claxton | new team | 27.8 | 28.4 | 28.3 | hold: references split or within 1.5 min | 68 | 70 | 67 | hold: references split or within 5 games |
| Bobby Portis | new team | 24.2 | 25.1 | 24.2 | hold: references split or within 1.5 min | 68 | 64 | 68 | hold: references split or within 5 games |
| Zach LaVine | base under 50 games | 31.4 | 32.4 | 33 | hold: references split or within 1.5 min | 64 | 67 | 68 | hold: references split or within 5 games |
| Ja Morant | new team | 25.5 | 30.4 | 23.8 | hold: references split or within 1.5 min | 60 | 58 | 62 | hold: references split or within 5 games |
| Aaron Gordon | base under 50 games | 27.9 | 27.9 | 27.4 | hold: references split or within 1.5 min | 66 | 65 | 58 | hold: references split or within 5 games |
| Jaime Jaquez Jr | new team | 28.3 | 29.2 | 28.3 | hold: references split or within 1.5 min | 68 | 71 | 72 | hold: references split or within 5 games |
| Mitchell Robinson | new team | 19.6 | 22.8 | 18.9 | hold: references split or within 1.5 min | 58 | 63 | 65 | moved |

### Collateral — players outside the pass who moved 3+ places (the pool's frame shifting)

- deck: 72 players moved 3+, 16 moved 5+, 0 moved 8+; the largest 7 places; median 4.0.
- kit: 66 players moved 3+, 15 moved 5+, 2 moved 8+; the largest 10 places; median 4.0.
- The largest: CJ McCollum deck 132→125, kit 133→123; Cameron Johnson deck 134→128, kit 134→126; Kris Dunn deck 127→122, kit 131→124; Anthony Black deck 142→135, kit 144→140; Brandin Podziemski deck 136→130, kit 136→131; Ja Morant deck 143→139, kit 140→134.


## 4. The range rule on the result

The pass went through the standing D-RN-3 range rule, seeded with the committed 10/12 resolution (only Dejounte Murray's R1 minutes were released, since MG-1 triggered against them; `mg_seed_range.py`). It re-fired on two MG players and settled inside its references: **Dejounte Murray** at 29.2 minutes (factor .916; MG-1 had said 31.9) and **Alex Sarr** at 26.8 (factor .931; MG-1 had said 28.8). Three MG lines gained a cell kept on the method (R2): Giannis's turnovers, Jalen Williams's assists, Franz Wagner's rebounds. Naji Marshall's entry gained an R3-keep on FG% with no line change. Range check on the built page: **pending — filled from the chain record**.

## 5. What the boards did

- Both planes: 98 players moved 3+ places on either board (87 deck, 81 kit); 17 of them are the pass's players, the rest the pool's frame shifting by small amounts (§3, Collateral).
- Top-30 slots: Ware enters (67 → 27 on both), Embiid leaves the deck's top 30 (23 → 32). The first round and the #10 card are unchanged.
- Against the expert consensus (mean of Yahoo XRank, Hashtag and Rotoworld ranks): the 17 movers' mean distance 35.9 → 18.6 places; the kit top-150's Spearman with that consensus .847 → .860.
- **Ware is the outlier to watch:** 26.8 minutes on his 2025-26 rates rank him #27 on both boards, while the experts' lines put him near #62 — their per-minute rates for him are lower than last season's. The rule moved his minutes, not his rates; D-MG-3 on the sheet.
- Giannis sits #35/#39 at 32.5 minutes and 67 games (experts #5–9, 34.2 minutes on Hashtag): the rest of the gap is his 36-game 2025-26 rates and the kit's availability factor.

## 6. Controls and integrity

| check | result |
|---|---|
| Control 1 — the 10/12 pipeline on today's inputs, from scratch (`wo5_iterate.sh`) | both data files byte-identical to main; the intermediate lines file differs on the 5 rookie rows (their "new" entries come from the input plane files, so they are empty when the inputs already carry WO-5's values) |
| Control 2 — the same from the pre-WO-5 inputs, from scratch | a different fixed point (36 range entries, 11 shooting clamps, 6 rookie cell moves vs the committed 38 / 11 / 8); files differ. The committed resolution carries rookie identity entries from a separate 10/12 step, so the iteration is path-dependent. The 10/12 after-report's "reaches the same fixed point from the committed inputs" holds only seeded with the committed range (control 3); as a from-scratch claim it is PARTIAL. |
| Control 3 — seeded with the committed range file | lines from totals + overrides + range → apply: 0 values changed, both files byte-identical to main; one more range round changes 0 entries (fixed point) — the recipe this pass used |
| `wo5_apply.py --keep-unchanged-notes` (added today; a blocking dependency) | with the flag, re-applying the committed lines returns both files byte-identical; without it, 326 deck notes are re-dated with no value change — the flag keeps the diff to the rows that moved |
| The change-set guard before the in-place write | deck rows with a stat change 15, notes changed 15, kit rows changed 15; unexpected 0; note-only changes 0 |
| `wo5_apply.py` in place | deck 326 written (15 changed), kit 311 written (15 changed), 255 values; second run: 0 changed, files unchanged |
| `mg_apply_gp.py` (G1–G4) | 5 gp cells changed; second run 0, file unchanged |
| `mg_deck_games_notes.py` | 5 notes added (inserted before each row's WO-5 entry, so apply re-runs keep them); second run 0 |
| Kit gates | `test_rank_engine` OK (4); `check_provenance` PASS; `check_derived` 23/23; `rank_engine.py` rebuilt top-200; `slate.py` rebuilt the slate |

## 7. Verification — the deck chain on the shipped page

| step | result |
|---|---|
| `scripts/verify_rosters.py` | direct-complete 2026-10-13, 335/335, 0 mismatches |
| `scripts/build_deck.py --planes-lines-strict` + two `--planes-waive` | **pending — filled from the chain record** |
| `scripts/check_planes.py --lines-strict` | **pending — filled from the chain record** |
| `scripts/identity_check.py` | **pending — filled from the chain record** |
| `scripts/range_check.py` | **pending — filled from the chain record** |
| `scripts/check_parity.py` | **pending — filled from the chain record** |
| `scripts/test_card.py` / `test_draft.py` / `test_gates.py` | **pending — filled from the chain record** |
| `arena/mocks/full_dom_check.mjs` | **pending — filled from the chain record** |
| `scripts/repeat_market_check.py` | **pending — filled from the chain record** |
| artifact publish | **pending — filled from the chain record** |

## 8. What did not go to plan

1. **Two named waivers on gate 7.** The build's propagation check compares stat columns, so a kit games move with no deck stat change (Poeltl 66 → 58, Robinson 58 → 64) reads as "not carried to the other plane". The deck has no games column; carrying it as a stat change would be wrong, and reverting the games moves would depart from the approved recommendation. The build was run with two waivers by name, reasons recorded in the page's manifest, and each deck row carries a dated games note. My own success criterion "nothing waived" therefore FAILS for this pass, by design and on the record; D-MG-2 lets the owner mirror the games as tags, keep the kit-only moves, or revert them.
2. **The pipeline is path-dependent** (§6, control 2). The pass used the committed resolution as its seed; the 10/12 report's wording is corrected here.
3. **47 candidates, not "about 40"** as the Council estimated (the short-base rule reached 21).
4. **Two of fifteen MG moves were re-decided by the range rule** (Murray, Sarr) — pre-committed, and reported as holds in effect.
5. **`test_card.py`:** **pending**

## Watchlist

- Kel'el Ware at #27 on both boards (D-MG-3).
- Giannis at #35/#39: 32.5 minutes on a 36-game base; the experts carry him at #5–9.
- The five games movers on the deck: tag-based availability unchanged (D-MG-2).
- Joel Embiid 23 → 32 (deck): both outlets at 29.4 minutes; his +0.10 card stands with a dated receipt.
- D-C2 (after the draft): the new-team usage adjustment and the half-and-half history blend.

## Open-item receipts

| item | query run (2026-10-13) | dated finding |
|---|---|---|
| Ryan Rollins | WO-5 role pass; the 10/11 box score (ESPN) | started at point guard 10/11 (RotoWire, Brew Hoop/Yahoo — the day's pull); WO-5 line on his 2025-26 32.1 minutes; card receipt added; HELD −0.05, retiring the flag on the sheet (D-WO5-3) | — MG pass 10/13: no candidate (outside the pass); line unchanged |
| Bennedict Mathurin | WO-5 universe (outside the top 150 on every board) | no role search ran; line on his 2025-26 season at 30.0 minutes; card receipt added; HELD −0.05 | — MG pass 10/13: no candidate (outside the pass); line unchanged |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham | the day's pull, same day (after-report-2026-10-12.md, receipts dated 10/12) | unchanged since this morning's receipts; HELD or unsigned | — MG pass 10/13: a candidate (new team or short base); both verdicts hold, line unchanged |
| Joel Embiid, DeMar DeRozan | the MG pass (this report) | judgment cards carry a dated 10/13 receipt (minutes and points before → after); +0.10 and −0.05 stay |

## Range check (D-RN-3)

Rule (owner, 2026-10-08): on a projection pass, every cell of a top-150 line that sits outside the range of ALL its references (three or more of: Yahoo `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-12.csv`, RotoBaller `rotoballer-2026-09-29.csv`, 2025-26 actual `arena/results/tuning_2026-10-08/bref_pergame_2025-26.csv`; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats) carries a one-line mechanism naming two dated outlets, or comes back inside the range. This page: 26 player(s), 28 cell(s), of 145 checkable top-150 lines (23 / 25 on 10/12; the new cells are MG lines' cells kept on the method by the range rule's R2/R3). Net z is what the cells carry beyond the nearest reference in the deck's frame (positive flatters the player).

| player | deck rank | cells outside every reference | net z | mechanism (two dated outlets) |
|---|---|---|---|---|
| Ryan Rollins | 28 | stl 1.7 vs 1.3-1.5 | 0.64 | stl: steals/blocks on the item-8 three-season anchor (5/4/3 by games, per-36 at his minutes) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Dejounte Murray | 91 | stl 1.4 vs 1.6-1.7 | -0.64 | fg_pct: the percentage moved to the nearest end of the references' range; ft_pct: the percentage moved to the nearest end of the references' range; stl: steals/blocks on the item-8 three-season anchor (5/4/3 by games, per-36 at his minutes); minutes: minutes set by the range rule to the outside lines' range (Hashtag, RotoBaller, Yahoo) |
| Ausar Thompson | 104 | stl 1.8 vs 2-2.2 | -0.64 | stl: steals/blocks on the item-8 three-season anchor (5/4/3 by games, per-36 at his minutes) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Daniel Gafford | 117 | blk 1.6 vs 1.2-1.4 | 0.39 | blk: steals/blocks on the item-8 three-season anchor (5/4/3 by games, per-36 at his minutes) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Michael Porter Jr. | 34 | stl 0.7 vs 0.8-1.1 | -0.32 | stl: steals/blocks on the item-8 three-season anchor (5/4/3 by games, per-36 at his minutes) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Jalen Duren | 43 | stl 0.7 vs 0.8-0.8 | -0.32 | stl: steals/blocks on the item-8 three-season anchor (5/4/3 by games, per-36 at his minutes) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Luka Doncic | 5 | ft_pct .772 vs .780-.782 | -0.26 | ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Tyrese Haliburton | 12 | tov 1.5 vs 1.7-1.7 | 0.25 | minutes: minutes set by the range rule to the outside lines' range (Hashtag, RotoBaller, Yahoo); tov: R2 keep: 2024-25 per-36 rates (Basketball-Reference; ESPN) |
| Naz Reid | 52 | tov 1.9 vs 1.6-1.7 | -0.25 | tov: the 2025-26 per-36 rate at his minutes (the method) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Jalen Williams | 41 | ast 6 vs 5-5.5 | 0.24 | ast: the 2025-26 per-36 rate at his minutes (the method) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Joel Embiid | 32 | ft_pct .846 vs .854-.867 | -0.21 | ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range); stl: steals/blocks on the item-8 three-season anchor (5/4/3 by games, per-36 at his minutes) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Domantas Sabonis | 21 | tpm 0.9 vs 0.6-0.7 | 0.2 | tpm: R2 keep: 2024-25 per-36 rates (Basketball-Reference; ESPN) |
| Cade Cunningham | 24 | blk 0.7 vs 0.8-0.8 | -0.2 | blk: steals/blocks on the item-8 three-season anchor (5/4/3 by games, per-36 at his minutes) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Luke Kornet | 150 | fg_pct .613 vs .643-.657 | -0.19 | fg_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Keegan Murray | 74 | pts 12.4 vs 13.3-16.1 | -0.16 | pts: R2 keep: 2024-25 per-36 rates (Basketball-Reference; ESPN) |
| Naji Marshall | 148 | fg_pct .497 vs .505-.510 | -0.14 | fg_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Aaron Gordon | 136 | ft_pct .744 vs .753-.789 | -0.13 | ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Franz Wagner | 31 | reb 6 vs 5.2-5.7 | 0.12 | reb: the 2025-26 per-36 rate at his minutes (the method) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Giannis Antetokounmpo | 35 | tov 3.6 vs 3.1-3.3; fg_pct .600 vs .608-.624; ft_pct .664 vs .628-.650 | -0.12 | fg_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range); ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range); tov: the 2025-26 per-36 rate at his minutes (the method) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Brandon Ingram | 84 | ft_pct .811 vs .819-.826 | -0.12 | ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Jrue Holiday | 88 | ft_pct .822 vs .838-.867 | -0.1 | ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Jakob Poeltl | 115 | ft_pct .588 vs .602-.642 | -0.09 | ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Jalen Suggs | 64 | ft_pct .834 vs .846-.866 | -0.08 | ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| CJ McCollum | 125 | ft_pct .780 vs .749-.772 | 0.08 | ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Christian Braun | 120 | ft_pct .774 vs .782-.815 | -0.06 | ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |
| Tobias Harris | 140 | ft_pct .857 vs .863-.869 | -0.04 | ft_pct: the percentage shrunk one-third toward his career rate (his 2025-26 rate alone sits inside the range) — Basketball-Reference season totals pulled 2026-10-12, cross-checked against ESPN's verified actuals of 10/9 |

## Points identity (D-1009-3)

Rule (owner, 2026-10-09): on a projection pass, every top-200 line on either plane whose points sit more than 1 from its own shooting (2·FGM + 3PM + FTM) is reconciled or carries a mechanism naming two dated outlets. This page: `identity_check.py` — 0 player(s), 0 line(s) more than 1 from their own shooting (200 deck and 200 kit lines checked); the MG lines were written with points by the identity.

| player | plane | rank | pts | implied (2·FGM + 3PM + FTM) | gap | mechanism (two dated outlets) |
|---|---|---|---|---|---|---|

## Repeat-name market check

**pending — the check runs on the built page; its output is pasted here and gated by `repeat_market_check.py --check-report`**

## Bounds

**Out of scope by design**
- Rates, the new-team usage adjustment and the half-and-half history blend (D-C2, after the draft).
- Deck tags (D-MG-2): tags come from injury news, not projections.
- Candidates outside the kit's top 150, and any player with one reference only.

**In scope and unverified**
- Whether Yahoo's implied minutes (A1) measure minutes rather than a rate view: INFERENCE; the median across five cells damps a single-cell rate difference but cannot separate the two. Ware (§5) is the case where it matters most.
- The thresholds (A3): not tuned; chosen with the table visible (§2).

## Decisions (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-MG-1 | The pass as published (v61): (a) stands; (b) revert to v60 (one command: the before-files are in `report/mg/out/before/`) | (a) |
| D-MG-2 | The five games moves on the deck plane: (a) kit-only, deck rows carry the note (as built, two named waivers); (b) mirror as deck risk tags where the consensus GP is 60 or under (Poeltl 58, Grant 54); (c) revert the games moves on the kit | (a) |
| D-MG-3 | Ware at #27: (a) hold the rule's result; (b) a judgment card (the owner's adjustment, tooltip only — D-1011-4 showed cards do not move ranks); (c) hold his minutes at 22.1 (revert his MG-1 row) | (a) |
| D-C2, D-SF-1..4 | carried | carried |

## Confidence, in plain language

- The process (scripted, asserted, guarded, run twice at every step, two controls before any change): about 92%. The waivers are recorded, not hidden.
- The fifteen minutes moves: about 75% that each is closer to the truth than the line it replaced — two dated October outlets agree on direction and size, and the recent-era evidence says minutes and games were the board's weakest layer. The remaining doubt is Ware-shaped: an outlet's implied minutes can carry a rate view.
- The five games moves: about 65%; games played are the least predictable input, and the kit's availability factor is mild by design.
- The board as a whole: 78% (was 76% after WO-5) — closer to the experts where it most disagreed, on the two inputs they are best at, with the rate engine untouched.

## In plain language

The Council said: keep the projection method, but fix the two things it copies forward from last season — minutes and games — for the players whose situation changed. You said proceed. For the 47 players in the top 150 who changed teams or had a short last season, I looked at the two October projection sources we have on file and moved a player's minutes only when both said the same thing by a clear margin; the same for games. Fifteen players' minutes moved (eight up, seven down) and five players' games moved. The engine then re-ran. Giannis, Ware, Franz Wagner, Garland, Collins and Jalen Williams climb; DeRozan, Grayson Allen, O'Neale, Oubre and Embiid fall. Our board now agrees more with the experts exactly where it disagreed most, and the rest of the board barely moved. Two things to know: the deck page cannot hold a games number, so two rows needed a recorded exception in the build (your call on D-MG-2), and Ware's jump to #27 is the one result the rule produced that the experts would not sign.

## Appendix A — every move of three or more places (both boards, inside the top 200)

Built by `wo5_boarddiff.py` from the before-files and the published files (`report/mg/out/boarddiff_2026-10-13.md`); the basis column names the mechanism behind each line, and the driver column the two categories whose z moved most in the deck's own frame. A player whose line did not change moves because the pool's frame moved around him.

| player | deck before → after (move) | kit before → after (move) | z driver (deck frame) | line basis (mechanism) |
|---|---|---|---|---|
| Kel'el Ware | 67 → 27 (+40) | 66 → 27 (+39) | REB +0.75, ST +0.66 | 2025-26 per-36 at 26.8 min (role: MG-1: Hashtag 10/12 27.9 min and Yahoo 10/06 implied 25.7 min (median of five cells) both above the WO-5 22.1 by 1.5+) |
| Franz Wagner | 68 → 31 (+37) | 68 → 34 (+34) | ST +0.65, PTS +0.55 | 2025-26 per-36 at 34.5 min (role: MG-1: Hashtag 10/12 32.5 min and Yahoo 10/06 implied 36.4 min (median of five cells) both above the WO-5 30.0 by 1.5+) |
| Joel Embiid | 23 → 32 (-9) | 27 → 36 (-9) | PTS -0.34, ST -0.31 | 2025-26 per-36 at 29.4 min (role: MG-1: Hashtag 10/12 29.4 min and Yahoo 10/06 implied 29.4 min (median of five cells) both below the WO-5 31.6 by 1.5+) |
| Onyeka Okongwu | 33 → 36 (-3) | 33 → 33 (0) | REB -0.02, FG% -0.02 | 2025-26 per-36 at 31.0 min |
| Donovan Clingan | 34 → 37 (-3) | 34 → 35 (-1) | REB -0.05, TO -0.02 | 2025-26 per-36 at 27.2 min |
| Giannis Antetokounmpo | 58 → 35 (+23) | 58 → 39 (+19) | PTS +0.59, TO -0.48 | 2025-26 per-36 at 32.5 min (role: MG-1: Hashtag 10/12 34.2 min and Yahoo 10/06 implied 30.9 min (median of five cells) both above the WO-5 28.9 by 1.5+) |
| Kyrie Irving | 37 → 40 (-3) | 35 → 37 (-2) | FG% -0.01, FT% -0.01 | 2024-25 per-36 at 31.1 min (range rule R1 from 36.1) |
| Desmond Bane | 36 → 39 (-3) | 36 → 38 (-2) | FG% -0.02, FT% -0.01 | 2025-26 per-36 at 33.6 min |
| Ty Jerome | 35 → 38 (-3) | 41 → 45 (-4) | FG% -0.02, REB +0.01 | 2024-25 per-36 at 27.6 min (range rule R1 from 19.9, after a role move); ft_pct to the range |
| Paul George | 38 → 42 (-4) | 38 → 40 (-2) | TO -0.01, BLK +0.01 | 2025-26 per-36 at 30.7 min |
| Jalen Duren | 39 → 43 (-4) | 37 → 41 (-4) | FG% -0.04, REB -0.04 | 2025-26 per-36 at 28.2 min |
| Jalen Williams | 57 → 41 (+16) | 56 → 42 (+14) | ST +0.33, PTS +0.32 | 2025-26 per-36 at 31.2 min (role: MG-1: Hashtag 10/12 31.2 min and Yahoo 10/06 implied 31.3 min (median of five cells) both above the WO-5 28.4 by 1.5+) |
| Cooper Flagg | 40 → 44 (-4) | 39 → 43 (-4) | FG% -0.01, REB -0.01 | 2025-26 per-36 at 33.5 min |
| Cameron Boozer | 41 → 45 (-4) | 40 → 44 (-4) | REB -0.03, FG% -0.02 | rookie translation held; pts by identity |
| Jaren Jackson Jr. | 45 → 49 (-4) | 42 → 46 (-4) | FG% -0.01, FT% +0.01 | 2025-26 per-36 at 30.3 min |
| LaMelo Ball | 42 → 46 (-4) | 47 → 51 (-4) | TO +0.02, AST -0.01 | 2025-26 per-36 at 28.0 min |
| Nickeil Alexander-Walker | 44 → 47 (-3) | 43 → 47 (-4) | REB +0.01, FG% -0.01 | 2025-26 per-36 at 33.4 min |
| OG Anunoby | 43 → 48 (-5) | 44 → 48 (-4) | FG% -0.01, TO -0.01 | 2025-26 per-36 at 33.2 min |
| Jalen Brunson | 47 → 51 (-4) | 46 → 49 (-3) | FG% -0.02, PTS -0.01 | 2025-26 per-36 at 35.0 min |
| Evan Mobley | 46 → 50 (-4) | 45 → 50 (-5) | FT% +0.05, REB -0.03 | 2025-26 per-36 at 31.9 min |
| Naz Reid | 48 → 52 (-4) | 48 → 52 (-4) | REB -0.02, FG% -0.01 | 2025-26 per-36 at 31.0 min (role: starter in Bridges' former spot (ESPN box 10/6 and 10/11 ET; Roundtable 10/7)) |
| Damian Lillard | 50 → 53 (-3) | 52 → 56 (-4) | FT% -0.02, REB +0.01 | 2024-25 per-36 at 27.8 min (range rule R1 from 36.1) |
| Zach Edey | 49 → 54 (-5) | 49 → 53 (-4) | REB -0.04, FG% -0.02 | 2024-25 per-36 at 26.6 min (range rule R1 from 21.4); fg_pct/ft_pct to the range |
| Alperen Sengun | 51 → 55 (-4) | 50 → 54 (-4) | FT% +0.04, REB -0.03 | 2025-26 per-36 at 33.3 min |
| Devin Booker | 53 → 57 (-4) | 51 → 55 (-4) | TO +0.02, FT% -0.02 | 2025-26 per-36 at 33.5 min |
| VJ Edgecombe | 52 → 56 (-4) | 54 → 58 (-4) | TO -0.01, BLK +0.01 | 2025-26 per-36 at 35.0 min |
| Josh Giddey | 54 → 58 (-4) | 53 → 57 (-4) | TO +0.04, REB -0.02 | 2025-26 per-36 at 32.1 min |
| Jaylen Brown | 55 → 59 (-4) | 55 → 59 (-4) | TO +0.04, FG% -0.02 | 2025-26 per-36 at 34.4 min |
| LeBron James | 56 → 60 (-4) | 57 → 60 (-3) | FT% +0.02, FG% -0.02 | 2025-26 per-36 at 33.1 min |
| Darius Garland | 103 → 63 (+40) | 102 → 62 (+40) | TO -0.36, ST +0.33 | 2025-26 per-36 at 31.9 min (role: MG-1: Hashtag 10/12 31.4 min and Yahoo 10/06 implied 32.4 min (median of five cells) both above the WO-5 29.1 by 1.5+) |
| Reed Sheppard | 60 → 62 (-2) | 61 → 64 (-3) | TO -0.02, REB +0.02 | 2025-26 per-36 at 26.2 min |
| Trae Young | 63 → 65 (-2) | 60 → 63 (-3) | TO +0.05, AST -0.02 | 2024-25 per-36 at 32.9 min (range rule R1 from 36.0); ft_pct to the range |
| Jalen Suggs | 61 → 64 (-3) | 64 → 66 (-2) | TO +0.01, REB +0.01 | 2025-26 per-36 at 27.6 min |
| Mikal Bridges | 62 → 66 (-4) | 62 → 65 (-3) | TO -0.03, FG% -0.01 | 2025-26 per-36 at 32.8 min |
| Immanuel Quickley | 64 → 67 (-3) | 67 → 69 (-2) | TO -0.02, BLK +0.01 | 2025-26 per-36 at 31.9 min |
| Tyler Herro | 65 → 68 (-3) | 63 → 67 (-4) | FG% -0.01, FT% -0.01 | 2025-26 per-36 at 31.3 min |
| Kon Knueppel | 66 → 69 (-3) | 65 → 68 (-3) | FG% -0.01, ST +0.01 | 2025-26 per-36 at 31.5 min |
| Yaxel Lendeborg | 69 → 70 (-1) | 69 → 72 (-3) | TO -0.02, REB -0.01 | rookie translation held; fg_pct/ft_pct to the range; reb/tpm to the range |
| John Collins | 122 → 71 (+51) | 121 → 71 (+50) | PTS +0.35, ST +0.33 | 2025-26 per-36 at 30.9 min (role: MG-1: Hashtag 10/12 28.9 min and Yahoo 10/06 implied 32.9 min (median of five cells) both above the WO-5 27.1 by 1.5+) |
| Keegan Murray | 72 → 74 (-2) | 73 → 77 (-4) | TO -0.04, REB -0.01 | 2024-25 per-36 at 34.3 min |
| Jarrett Allen | 73 → 78 (-5) | 76 → 78 (-2) | FG% -0.03, FT% +0.03 | 2025-26 per-36 at 27.1 min |
| Payton Pritchard | 77 → 80 (-3) | 77 → 79 (-2) | TO -0.02, BLK +0.01 | 2025-26 per-36 at 32.4 min |
| Neemias Queta | 80 → 82 (-2) | 78 → 82 (-4) | TO -0.03, REB -0.03 | 2025-26 per-36 at 25.3 min |
| Ivica Zubac | 83 → 85 (-2) | 81 → 84 (-3) | REB -0.04, FG% -0.03 | 2025-26 per-36 at 30.1 min |
| Jrue Holiday | 91 → 88 (+3) | 89 → 88 (+1) | TO +0.02, FG% -0.01 | 2025-26 per-36 at 29.4 min |
| Dejounte Murray | 87 → 91 (-4) | 87 → 91 (-4) | TO -0.11, FG% -0.01 | 2024-25 per-36 at 29.2 min (range rule R1 from 32.6, after a role move); fg_pct/ft_pct to the range |
| Alex Sarr | 99 → 103 (-4) | 97 → 101 (-4) | REB -0.06, PTS -0.05 | 2025-26 per-36 at 26.8 min (range rule R1 from 27.2, after a role move) |
| Andrew Nembhard | 104 → 101 (+3) | 104 → 103 (+1) | REB +0.02, AST -0.01 | 2025-26 per-36 at 31.3 min |
| Darryn Peterson | 112 → 110 (+2) | 114 → 111 (+3) | REB +0.01, BLK +0.01 | rookie translation held; pts/tov to the range |
| Zion Williamson | 118 → 114 (+4) | 119 → 117 (+2) | FT% +0.05, FG% -0.04 | 2025-26 per-36 at 29.7 min |
| Cam Spencer | 123 → 118 (+5) | 122 → 119 (+3) | TO -0.02, REB +0.02 | 2025-26 per-36 at 23.8 min |
| Christian Braun | 124 → 120 (+4) | 124 → 121 (+3) | TO -0.03, FG% -0.01 | 2025-26 per-36 at 31.8 min |
| Kyshawn George | 126 → 121 (+5) | 125 → 120 (+5) | TO +0.01, ST +0.01 | 2025-26 per-36 at 29.0 min |
| Kris Dunn | 127 → 122 (+5) | 131 → 124 (+7) | TO -0.02, PTS +0.02 | 2025-26 per-36 at 27.2 min |
| Paolo Banchero | 128 → 123 (+5) | 127 → 122 (+5) | FT% +0.03, REB -0.03 | 2025-26 per-36 at 34.8 min |
| CJ McCollum | 132 → 125 (+7) | 133 → 123 (+10) | REB +0.01, TO -0.01 | 2025-26 per-36 at 28.8 min (2025-26 minutes with ATL (41 of 76 games)) |
| Santi Aldama | 129 → 124 (+5) | 130 → 125 (+5) | TO -0.02, FT% +0.02 | 2025-26 per-36 at 27.9 min |
| Cameron Johnson | 134 → 128 (+6) | 134 → 126 (+8) | TO -0.03, ST +0.01 | 2025-26 per-36 at 30.5 min |
| Nic Claxton | 131 → 126 (+5) | 132 → 127 (+5) | FT% +0.04, FG% -0.02 | 2025-26 per-36 at 27.8 min |
| Moussa Diabate | 130 → 127 (+3) | 128 → 129 (-1) | TO -0.03, REB -0.03 | 2025-26 per-36 at 26.0 min |
| Wendell Carter Jr. | 133 → 129 (+4) | 129 → 128 (+1) | TO -0.02, REB -0.02 | 2025-26 per-36 at 29.3 min |
| Bobby Portis | 135 → 131 (+4) | 135 → 130 (+5) | TO -0.03, FG% -0.01 | 2025-26 per-36 at 24.2 min |
| Brandin Podziemski | 136 → 130 (+6) | 136 → 131 (+5) | TO -0.01, BLK +0.01 | 2025-26 per-36 at 28.4 min |
| Herbert Jones | 137 → 132 (+5) | 137 → 132 (+5) | TO -0.02, PTS +0.01 | 2025-26 per-36 at 28.4 min |
| Zach LaVine | 138 → 133 (+5) | 138 → 133 (+5) | REB +0.02, FG% -0.01 | 2025-26 per-36 at 31.4 min |
| Grayson Allen | 81 → 134 (-53) | 82 → 136 (-54) | ST -0.64, PTS -0.43 | 2025-26 per-36 at 24.6 min (role: MG-1: Hashtag 10/12 24.0 min and Yahoo 10/06 implied 25.2 min (median of five cells) both below the WO-5 28.8 by 1.5+) |
| Ja Morant | 143 → 139 (+4) | 140 → 134 (+6) | TO +0.02, REB +0.01 | 2024-25 per-36 at 25.5 min (range rule R1 from 30.4); ft_pct to the range |
| Anthony Black | 142 → 135 (+7) | 144 → 140 (+4) | FT% +0.02, REB +0.01 | 2025-26 per-36 at 29.8 min |
| Derik Queen | 140 → 137 (+3) | 139 → 135 (+4) | REB -0.02, PTS +0.01 | 2025-26 per-36 at 25.0 min |
| Aaron Gordon | 139 → 136 (+3) | 141 → 137 (+4) | TO -0.03, FT% +0.02 | 2025-26 per-36 at 27.9 min |
| PJ Washington | 141 → 138 (+3) | 142 → 139 (+3) | FT% +0.02, REB -0.01 | 2025-26 per-36 at 31.0 min |
| Tobias Harris | 111 → 140 (-29) | 111 → 138 (-27) | ST -0.31, PTS -0.22 | 2025-26 per-36 at 25.0 min (role: MG-1: Hashtag 10/12 26.2 min and Yahoo 10/06 implied 23.8 min (median of five cells) both below the WO-5 27.7 by 1.5+) |
| Jaime Jaquez Jr. | 144 → 141 (+3) | 143 → 141 (+2) | FG% -0.02, FT% +0.01 | 2025-26 per-36 at 28.3 min |
| Sam Merrill | 146 → 142 (+4) | 145 → 142 (+3) | TO -0.04, REB +0.02 | 2025-26 per-36 at 26.5 min |
| AJ Dybantsa | 148 → 145 (+3) | 148 → 143 (+5) | FT% +0.01, TO +0.01 | rookie translation held; pts by identity; the kit's line (D-R1) |
| Scotty Pippen Jr. | 147 → 143 (+4) | 149 → 146 (+3) | PTS +0.01, REB +0.01 | 2024-25 per-36 at 21.3 min |
| DeMar DeRozan | 88 → 146 (-58) | 88 → 147 (-59) | PTS -0.54, AST -0.35 | 2025-26 per-36 at 26.2 min (role: MG-1: Hashtag 10/12 27.8 min and Yahoo 10/06 implied 24.6 min (median of five cells) both below the WO-5 31.2 by 1.5+) |
| Coby White | 153 → 149 (+4) | 152 → 148 (+4) | TO +0.02, ST +0.01 | 2025-26 per-36 at 29.1 min (role: starting PG when healthy (NBA.com/AP 10/6; Roundtable 10/7)) |
| Naji Marshall | 151 → 148 (+3) | 153 → 150 (+3) | TO -0.01, FG% -0.01 | 2025-26 per-36 at 29.5 min |
| Aaron Nesmith | 154 → 151 (+3) | 154 → 151 (+3) | TO -0.02, ST +0.01 | 2025-26 per-36 at 29.7 min |
| Draymond Green | 155 → 152 (+3) | 155 → 152 (+3) | PTS +0.02, TO +0.01 | 2025-26 per-36 at 27.5 min |
| Jaylon Tyson | 158 → 155 (+3) | 156 → 153 (+3) | TO -0.02, FG% -0.01 | 2025-26 per-36 at 26.9 min |
| Miles McBride | 157 → 153 (+4) | 158 → 154 (+4) | TO -0.04, REB +0.02 | 2025-26 per-36 at 26.3 min |
| Jordan Goodwin | 156 → 154 (+2) | 159 → 156 (+3) | TO -0.03, PTS +0.02 | 2025-26 per-36 at 22.5 min |
| Sandro Mamukelashvili | 159 → 156 (+3) | 157 → 155 (+2) | TO -0.04, FG% -0.01 | 2025-26 per-36 at 21.9 min |
| Marcus Smart | 160 → 157 (+3) | 166 → 160 (+6) | TO -0.02, REB +0.02 | 2025-26 per-36 at 28.5 min |
| Nikola Vucevic | 163 → 160 (+3) | 160 → 157 (+3) | TO -0.03, ST +0.01 | 2025-26 per-36 at 21.1 min (role: bench (ESPN box 10/7 and 10/11 ET; Roundtable 10/8)) |
| Cedric Coward | 165 → 163 (+2) | 161 → 158 (+3) | ST +0.01, TO -0.01 | 2025-26 per-36 at 25.8 min |
| Kyle Filipowski | 161 → 158 (+3) | 162 → 159 (+3) | REB -0.02, TO -0.01 | 2025-26 per-36 at 23.4 min |
| Derrick Jones Jr | 162 → 159 (+3) | 164 → 161 (+3) | TO -0.04, PTS +0.01 | 2025-26 per-36 at 27.0 min |
| Stephon Castle | 167 → 161 (+6) | 167 → 165 (+2) | FT% +0.03, TO +0.03 | 2025-26 per-36 at 30.0 min |
| Kelly Oubre Jr. | 121 → 162 (-41) | 123 → 164 (-41) | ST -0.64, PTS -0.32 | 2025-26 per-36 at 27.4 min (role: MG-1: Hashtag 10/12 28.2 min and Yahoo 10/06 implied 26.7 min (median of five cells) both below the WO-5 31.5 by 1.5+) |
| Al Horford | 171 → 169 (+2) | 171 → 168 (+3) | TO -0.03, PTS +0.02 | 2025-26 per-36 at 21.5 min |
| De'Anthony Melton | 173 → 170 (+3) | 174 → 171 (+3) | REB +0.01, PTS +0.01 | 2025-26 per-36 at 23.0 min |
| Darius Acuff Jr. | 179 → 175 (+4) | 177 → 174 (+3) | REB +0.01, TO +0.01 | line unchanged (no method line: rookie translation held or no qualifying season) |
| Royce O'Neale | 125 → 180 (-55) | 126 → 179 (-53) | 3PTM -0.40, ST -0.32 | 2025-26 per-36 at 24.3 min (role: MG-1: Hashtag 10/12 24.6 min and Yahoo 10/06 implied 24.0 min (median of five cells) both below the WO-5 28.4 by 1.5+) |
| Taylor Hendricks | 190 → 189 (+1) | 191 → 188 (+3) | TO -0.03, PTS +0.01 | 2025-26 per-36 at 24.1 min (2025-26 minutes with MEM (26 of 59 games)) |
| Jerami Grant | 150 → 193 (-43) | 150 → 192 (-42) | ST -0.31, PTS -0.22 | 2025-26 per-36 at 27.8 min (role: MG-1: Hashtag 10/12 27.5 min and Yahoo 10/06 implied 28.0 min (median of five cells) both below the WO-5 29.7 by 1.5+) |


## Provenance

- Session https://claude.ai/code/session_01QjgeRdpDaWgSJmGKRG8fTU, 2026-10-13. Governors: council, plan-gate and scope-fence loaded through the Skill tool before the Council; the full plan block went out before the first write; adversarial-verify loaded before delivery (the PR records its pass).
- Scripts: `report/mg/tools/` (`mg_moves.py`, `mg_seed_range.py`, `mg_apply_gp.py`, `mg_deck_games_notes.py`, `deck_page_mg.py`, `mg_report_tables.py`, `mg_gen_report.py`); `report/wo5/tools/wo5_apply.py` gained `--keep-unchanged-notes`.
- Records: `report/mg/out/` (candidates, seed and final range files, lines, apply record, board diff, iteration logs, before-files) and `report/mg/data/` (the overrides file, the games list).
- Re-verify: rerun `mg_moves.py` on the before-files (same outputs); rerun the seeded iteration from `report/mg/out/iter_logs/`; `python3 -I report/mg/tools/mg_report_tables.py report/mg out.md` and diff.
