# The G-score column on the season board — 2026-10-21 (night)

Pull window: 2026-10-21 → 2026-10-21. No league or market pull. Inputs:
- the 10/21 season lines, `data/season/projections_season.csv`;
- the week-to-week variance measured from the 2025-26 game logs in the z-score assessment (`after-report-2026-10-21-zscore-assessment.md` §4, Measurement 3), pinned here as `data/season/gscore_tau.json`.

**Owner's request** (2026-10-21, clicked on D-ZS-2): **"Build it"**. The option read: "The paper's exact formula (Table 5), shown beside the z-score on the season board for comparison. Changes no ranking. Test-first, on its own PR."

**What was analyzed.**
- Kit at `83851de`, the z-score assessment's head, which carries the game logs and the weights script.
- `scripts/season_board.py` and `report/rank_engine.py`.
- The paper, arXiv 2307.02188v5, pinned in `data/source/papers/`, Table 5 (p. 5).
- Deck `80eecdf`, for the morning chain's end-to-end run.

**Method, stated to you before the build.** The board's own 10/21 projections over its own 180-player pool give each player's mean, the pool mean μ and the spread σ, exactly as the z uses them. τ comes from the 2025-26 weekly logs. A weekly τ is put on the board's per-game scale by dividing by the logs' mean games per counted week (3.0065). κ = 26/25 (13 non-IL roster spots). The G total takes the same availability factor as z. The board stays ordered by z.

**Headline.**
- **Built, test-first, and the board's order cannot move.** Eight new tests failed against the old code and pass now, 11 of 11. The full suite passes 323 of 323, three runs. Without the τ file the board is byte-identical to the committed 10/21 board. With it, the order, every z and every z total are unchanged; two new columns appear: G (adj) and G #, the rank G alone would give.
- **On 10/21 the G rank mostly agrees with z, with a pattern.**
  - Rank correlation 0.98 over the z top 156; 44 of those 156 move 10 or more places, and 11 of the top 12 are the same.
  - The largest falls are steals specialists, as the paper predicts: Dyson Daniels 34 → 64, Cason Wallace 89 → 121, Alex Caruso 124 → 157, Herb Jones 147 → 179, Scotty Pippen Jr. 148 → 181.
  - The largest rises: Paolo Banchero 122 → 94, CJ McCollum 116 → 100, Julius Randle 119 → 103.
- **The morning chain runs with it.** End to end on a copy with the τ file in place, the morning passes 6 of 6. The season deck renders 6 tabs with 0 page errors and carries the new fields, but its Board tab does not show them; adding them there is a separate choice.

## 1. What changed

- **`scripts/season_board.py`.**
  - `load_pin(path)` reads `data/season/gscore_tau.json`. It returns nothing when the file is absent, and refuses a file missing any of the nine categories, κ or the games-per-week figure.
  - `gscores(rows, pool, pin)` computes Table 5 over the same pool as `rank_engine.zscores`, with population SDs:
    - counting: G = (x − μ) / √(σ² + κ·(τ/g)²), turnovers negated;
    - FG%/FT%: G = (a/μ_A)·(r − μ_R) / √(σ_R² + κ·τ_R²).
  - `build()` adds `g_total`, `g_adj` (G total × the same availability factor as z, when positive), per-category `g` and `g_rank`, all from the same rows and pool. The board's sort key is untouched: `z_adj`.
  - `render()` adds a note naming the paper and the τ file, and the two columns.
  - `write()` adds the G fields and a `gscore` block to the json. With no τ file the json and md are written exactly as before.
- **`data/season/gscore_tau.json`.** Written by `report/after-reports/zscore-assessment-2026-10-21/gamelogs/gscore_weights.py --pin`, and reproduced byte for byte by a second run. It holds 157 players, 22 weeks, κ 1.04, 3.0065 games a week, the weekly τ for the seven counting categories, and τ_R for FG% and FT%.
- **`scripts/test_season_board.py`.** Eight new tests (§2).

## 2. Tests, red first

| test | what it pins | red (old code) | green |
|---|---|---|---|
| known answer on a hand-built pool | Table 5 worked by hand on three players: PTS 1.18823, FG% 0.77911, TOV 1.03882, the middle shooter 0 | error | pass |
| counting G at zero τ is the board's z | every counting category, every row, to 9 places | error | pass |
| week-to-week variance only shrinks a category | \|G\| ≤ \|G at τ = 0\| | error | pass |
| the G column never moves the board | same order and same z (adj) with and without the τ file | error | pass |
| G (adj) takes the same availability as z | G total × avail(GP) when positive; G ranks 1..n | error | pass |
| no τ file, no column | no G fields, no G header, no `gscore` block | error | pass |
| a pinned board shows G beside z | the header, the paper's id, "ranked by z", the json fields | error | pass |
| a τ file missing a category is refused | a loud error, not a silent zero | error | pass |

Records: `gscore-column-2026-10-21/red.txt` (8 errors, the new tests against the old `season_board.py`) and `green.txt` (11 of 11).

## 3. The column on the 10/21 board

Record: `gscore-column-2026-10-21/compare.py` / `.json`, two runs byte-identical.

| measure | z top 156 | z top 180 |
|---|---|---|
| rank correlation, G rank vs z rank | 0.9808 | 0.9812 |
| players moving 10+ places | 44 | 58 |
| top 12 shared | 11 of 12; the one swap: Anthony Davis (z 12, G 15) and Jayson Tatum (z 15, G 10) | same |

**The weight each category carries on the board.** That is G / z for counting categories, and the median G / z over the pool for FG%/FT%, which also carries Table 5b's definition:

| STL | FG% | FT% | TOV | PTS | BLK | 3PM | REB | AST |
|---|---|---|---|---|---|---|---|---|
| 0.40 | 0.49 | 0.54 | 0.60 | 0.62 | 0.66 | 0.67 | 0.68 | 0.72 |

- **Steals weigh less here than on 2025-26 alone** (0.40 against 0.47). The board's projected lines spread less across players than last season's actual weeks did, so the same week-to-week variance takes a bigger share. EVIDENCE: the board's own σ against the logs' τ, in `compare.json`.
- **FG% carries two changes, and they are separable.**
  - The paper's Table 5b uses the spread of players' raw shooting rates, while the kit's z uses the spread of impact. At zero weekly variance that definition alone scales FG% to 0.78 of the kit's z (FT% 1.06).
  - Week-to-week variance then scales it by 0.62 (FT% 0.51).
  - Both are in `compare.json` under `percentage_definition`.
- **The games-per-week divisor barely matters.** With the arena's 3.5 games a week in place of the logs' 3.0065, the G ranks of the z top 156 correlate 0.9991 with the shipped ones, and no rank moves more than 8 places.

## 4. Errors and surprises, stated plainly

- **One end-to-end check first ran in the wrong folder.** My copy command used `rsync`, which is not installed here. The commands after it were joined with `;`, so the morning chain ran in the main checkout (the z-score assessment's branch, without the τ file) instead of the copy.
  - It rewrote eleven 10/21 records there and wrote one new file.
  - All were restored from that branch's commit, and the new file deleted, before its commit. `git status` showed only the intended files. The deck repo was untouched.
  - The check was then run in a proper copy (`cp -a`, git link removed, run only if the copy exists): 6 of 6 PASS.
- **The Season Deck does not show the column.** Its Board tab reads `z_adj` and the nine z values; the G fields ride along in its data unused. I did not change it: your option named the season board.

## Watchlist

- **G is a comparison, not a ranking.** The board, lineup, streaming and waiver shortlist still sort by z. A G rank far from the z rank says that player's value leans on a category that swings week to week (steals most of all).
- **τ is last season's.** It assumes 2025-26's week-to-week swings carry into 2026-27. It is re-measurable from this season's logs once enough weeks accrue (several weeks at least).

## Open-item receipts

| item | status | receipt |
|---|---|---|
| G-score board (D-ZS-2, owner "Build it") | **BUILT** as a comparison column; no ranking changed | §1–§3 |
| per-game variation fit (D-ZS-3) | **OPEN**: your choice; nothing changed | `after-report-2026-10-21-zscore-assessment.md` §4 |

The flagged-name receipts are carried forward from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21 (`after-report-2026-10-21-pickups-file.md` §1). The rest were not re-queried for this build (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this build (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (§1, `roster_drift_2026-10-21.json`) |

## Repeat-name market check

This build did not change the draft-room deck page, which is still deck `80eecdf` (checked with `git -C ../yahoo-fantasy-basketball log -1`, clean tree, 2026-10-21), page sha256 6a5cefea4921. The GAUNTLET report replayed it today. Its table stands, carried here verbatim.

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

**Structural bands, carried for the gate.** This report quotes no simulator figure. The standing sweep's bands are carried verbatim:
- TEAM_WEEK_SHOCK is FRAGILE: +2.7 (no shock) / −3.6 (shock doubled).
- weekly_availability is FRAGILE: −2.7 (no in-sim injury discount) / +0.5 (harsher risk tier 0.65) / −1.5 (healthy plays 0.95) / +1.0 (healthy plays 0.80).

## Decision sheet

1. **How this ships** (it is built for its own PR; this session may push only to its one branch):
   - (a) merge the z-score assessment (#159) first, after which this goes up as a new PR from that branch;
   - (b) allow a second branch now;
   - (c) add it to #159.
2. **The Season Deck's Board tab**: show G (adj) and G # there too, or leave the deck as it is. Default: leave it.
3. **D-ZS-3** (unchanged, in the assessment): the per-game variation fit.

## Bounds

**Out of scope by design.**
- Any change to how the board, lineup, streaming or waivers rank.
- The Season Deck page.
- The draft-room deck page.
- H-scoring (the paper's later companion).

**In scope and unverified.**
- That 2025-26's week-to-week variance carries into 2026-27 (an assumption): UNVERIFIABLE until this season's weeks accrue.
- Whether G picks better than z in this league: did not check. The paper's simulation is the only evidence, and it is for drafting from a static list, not in-season pickups.

## Provenance

- **Produced by** session `session_01QjgeRdpDaWgSJmGKRG8fTU` on 2026-10-21, about 21:40–22:20Z.
- **Governors.**
  - plan-gate was loaded after a context compaction. Its block was emitted before any of this was written, with the method line above.
  - adversarial-verify was loaded before delivery. Its pass found the wrong-folder run (§4), and checked the τ file by regenerating it.
- **Sources.**
  - The code at the commits above.
  - The paper, Table 5 (p. 5), read from the pinned parser text.
  - The z-score assessment's game-log record.
- **Re-verify.**
  - `python3 scripts/test_season_board.py`
  - `python3 report/after-reports/gscore-column-2026-10-21/compare.py`
  - `python3 report/after-reports/zscore-assessment-2026-10-21/gamelogs/gscore_weights.py --pin <file>`, then `cmp` it with `data/season/gscore_tau.json`.

## In plain language

The season board now shows a second number beside each player's z-score: his G-score, the version the paper you uploaded recommends for head-to-head leagues. G counts a category for less when it swings a lot from week to week. The board still sorts by z, so nothing about your rankings, lineup or pickups changes.

On today's board the two mostly agree. The biggest differences are steals specialists: Dyson Daniels drops from 34th to 64th by G, because steals are the swingiest category. Paolo Banchero climbs from 122nd to 94th. The column appears on the board each morning from now on. Whether it should also show in the Season Deck, and whether we should ever rank by it, are your calls.
