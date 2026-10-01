# After-report — 2026-10-01 WO-1 and WO-2: the planes stat-line drift gate, and the verifier's suffix fold and live-feed re-author

**Owner request (2026-10-01):** the pre-draft work order (`report/
pre-draft-workorder-2026-10-01.md`) pasted back as the session's standing
instruction, §3 blank so the defaults apply: WO-1 (D-30-4, "build it first")
and WO-2 (D-1001-2, "yes") are the two work orders runnable before the
preseason games; the rest wait on the owner's inputs or on box scores.

Pull window: 2026-10-01 → 2026-10-01 (code and verification only; no news
sweep, no pool-row edit on either plane; the 10/01 pull-log rows cover the
window). Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows
sourced; verified 2026-07-13 .. 2026-09-30`, exit 0.

**Method.** Red-first on the deck plane. WO-1: three cases added to the
gate suite and run first (3 of 37 failed, the strict flag unknown to the
build — `scratchpad pull1001/test_gates_wo1_red.log`), then
`scripts/check_planes.py` gained a per-row stat-line comparison on every
shared name, reported as a warning by default and counted as a refusal
under `--lines-strict`, with `--lines-report PATH` writing the full list;
`scripts/build_deck.py` gained `--planes-lines-strict` and the manifest a
`lines` count. WO-2: a scratch case showed `verify_rosters.py` failing to
match `Jimmy Butler III` and `Ronald Holland II` and leaving the evidence
file untouched in direct mode (`red_reauthor.py`, RED), then the name fold
dropped generational suffixes and took the planes gate's aliases, and a
direct-mode run now re-authors `data/rosters_official.json`'s teams from
ESPN's feed. Every number below is a command's own output or a field of
`arena/results/planes_lines_2026-10-01.json`.

**Headline.** The gate exists and it has something to say: 184 of the 314
names both planes carry have different per-game lines, 57 of them inside
the kit's top 60, and the deck — the surface the owner drafts from — is the
higher plane on points in 102 of those rows against 55 for the kit.
Seventeen rows differ by three or more points, Lillard the widest (kit
17.0, deck 24.0), with Simons (19.5 vs 14.5), Shaedon Sharpe (19.0 vs
15.0), Dončić (30.0 vs 33.5), Grimes, Coward, Flagg (21.0 vs 17.8) behind
him; only two of the 184 carry a dated reprice on the deck side (Mobley,
Sochan), so the rest is the two planes' July baselines never having been
one line. Nothing was reconciled today: that is a projection decision, not
a side effect of a gate, and it is on the sheet (D-WO1-1). The verifier now
matches 333 of 334 pool rows against ESPN's thirty live rosters with only
Tony Bradley's day-old camp deal unmatched, and the fallback evidence file
mirrors the feed (605 names) instead of only what the pulls wrote — the
mechanism that let Vincent ride on Atlanta for three months is closed.

## 1. What shipped

| plane | change | evidence |
|---|---|---|
| deck | `check_planes.py`: stat-line comparison on shared rows (11 columns, exact); `lines N` warning with the first eight rows; `--lines-strict` counts them as mismatches; `--lines-report PATH` writes the full JSON list; `pool_sha256` in the result | real-repo run: `lines 184: shared row(s) carry a differing stat line (WARNING; --lines-strict refuses)`, exit 0; strict run exit 1 |
| deck | `build_deck.py`: `--planes-lines-strict` flag; manifest `planes.lines` and `planes.lines_strict` | suite cases below |
| deck | `test_gates.py`: three WO-1 cases (warning reported and the build passes; the manifest count; strict refuses by name); prime walks the `--allow-unmatched` path when a verify run shows unmatched rows and zero mismatches; the R4-F05 case asserts the unmatched row by name, not by count | red run 3 of 37 FAIL; green run all 37 cases passed (the three WO-1 cases green; the prime's exemption path and the R4-F05 by-name assertion hold) |
| deck | `verify_rosters.py`: `norm()` drops II / III / IV / Jr / Sr and applies the planes gate's aliases; direct mode writes the feed's teams, today's date and a `reauthored` block into `data/rosters_official.json`, the `source` narrative untouched | scratch RED → PASS on both checks; real run 333/334, 0 mismatches, unmatched Tony Bradley only; evidence 605 names, `reauthored` 2026-10-01 |
| deck | `arena/results/planes_lines_2026-10-01.json` — the first run's list: date, kit sha `2a0ace719ab1`, pool sha `09fe6d433264`, 314 shared, 184 rows with every differing column and both values | committed |
| kit | nothing but this report and the pull-log row | — |

## 2. The drift, measured

| readout | value |
|---|---|
| shared names | 314 |
| rows whose line differs on at least one column | 184 |
| rows differing by 3+ points | 17 |
| rows differing by 1.5 to 3 points | 61 |
| differing rows inside the kit top 60 / top 150 | 57 / 126 |
| points: deck higher / kit higher | 102 / 55 |
| columns most often different (rows) | fga 163, fta 163, pts 157, tov 155, ast 153, reb 148, fg% 137, 3PM 130, ft% 122, stl 105, blk 96 |
| differing rows with a dated reprice note on the deck | 2 (Mobley, Sochan) |

The seventeen wide rows, kit vs deck points: Lillard 17.0 / 24.0, Simons
19.5 / 14.5, Shaedon Sharpe 19.0 / 15.0, Dončić 30.0 / 33.5, Grimes 14.0 /
17.5, Coward 16.3 / 13.0, Flagg 21.0 / 17.8, Mamukelashvili 13.7 / 10.5,
DiVincenzo 11.5 / 14.5, Dick 12.0 / 15.0, Poeltl 11.5 / 14.5, Butler 15.5 /
18.5, Kevin Porter Jr. 11.5 / 14.5, Monk 14.5 / 17.5, Mark Williams 12.5 /
15.5, Miles Bridges 17.0 / 20.0, Barrett 17.5 / 20.5. Three of them (Sharpe,
DiVincenzo, Mark Williams) are excluded on both planes and never reach a
card; Butler is excluded on the deck; the other thirteen are live draft
rows.

## 3. Why nothing was reconciled today

Rule 3 of the work order: a projection changes only with a named mechanism.
A gate that discovers two baselines can report them; choosing one line for
184 rows is a projection decision for the owner, and the preseason refresh
(WO-5) is the mechanism that will write one line to both planes for the
top 150 from box scores and per-36 rates. The gate is what keeps them one
line afterward, and `--planes-lines-strict` at the final build is what
proves it. The thirteen live wide rows are the ones worth deciding before
WO-5 if the owner wants (D-WO1-1).

## 4. Verification

| gate | result (evidence: the command's own output line) |
|---|---|
| deck `test_gates.py` (red, before the change) | 3 of 37 cases FAILED — the three new WO-1 cases; `BUILD REFUSED — unknown argument '--planes-lines-strict'` |
| deck `test_gates.py` (green, after) | all 37 cases passed (the three WO-1 cases green; the prime's exemption path and the R4-F05 by-name assertion hold) |
| deck `test_draft.py` / `test_card.py` | all 62 cases passed / CARD: all 68 cases passed |
| deck `check_parity.py` (page unchanged) | PARITY: EXACT MATCH |
| deck `check_planes.py --kit <kit>` | planes 314 shared · team 0 · exclusion 0 · drift 0 · propagation 0; lines 184 (warning), exit 0 |
| deck `check_planes.py --lines-strict` | same counts; `REFUSED by --lines-strict`, exit 1 |
| deck `verify_rosters.py` (direct) | 333/334, 0 mismatches, UNMATCHED (1): Tony Bradley; re-run `--allow-unmatched` for the artifact |
| scratch `red_reauthor.py` | before: unmatched ['Ron Holland', 'Jimmy Butler'], evidence unchanged (RED); after: unmatched [], evidence teams = the feed, date today (PASS) |
| kit `check_provenance.py` / `check_derived.py` / `check_report.py` on this file / `judgment_open_items.py --check-report` | PROVENANCE GATE: PASS; DERIVED: all 11 dated artifacts reproduce byte-for-byte; REPORT GATE: PASS; receipts check PASS |

The page was not rebuilt: no pool row changed and the scripts are not
embedded in it, so `main` and the live artifact (Version 37) stay
byte-identical. The committed verification artifact now reads 333/334 with
one exemption while the page's build manifest still carries this morning's
331/334 with three; the next pull's build re-syncs them.

## Watchlist

- **D-WO1-1** decides when and how the 184 lines become one; until then
  every deck build prints the warning and the count sits in the manifest.
- **`--planes-lines-strict`** is for the final build on 10/14; it refuses
  today, by design.
- **Tony Bradley** — ESPN's feed should post him within a day; the
  exemption drops when it does.
- **The evidence file** now changes with every direct-mode run (sorted
  names, so the diffs are small); a day ESPN times out falls back to the
  last live mirror, which is the intended behavior.

## Open-item receipts

| item | query run (2026-10-01) | dated finding |
|---|---|---|
| (no news sweep) | none — a code and verification work order | the 10/01 daily pull's receipts stand (after-report-2026-10-01.md) |
| Jalen Duren, Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the daily pull's dedicated queries, same day | all HELD on 2026-10-01; nothing here touches them |
| Tony Bradley | ESPN roster API NYK (fetched by the verifier) | not on the feed; the 9/30 camp deal (RealGM, Hoops Wire, BVM) stands; exempted by name |

## Bounds

- Out of scope by design: reconciling the lines (D-WO1-1); the kit side
  has no line-diff tool of its own (the gate lives on the deck and reads the
  kit checkout).
- In scope and unverified: none — every claim above is a command output or
  a field of the committed JSON.
- The exact-match comparison counts a 0.005 rounding difference the same
  as a 7-point one; the report's magnitude buckets, not the count, say what
  matters.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-WO1-1 | One line on both planes: (a) let WO-5 re-derive the top 150 from preseason box scores and per-36 rates (one script, both planes) and copy the kit's line to the deck for the tail at the final refresh so `--planes-lines-strict` passes; (b) copy the kit's line to the deck now for all 184 (a mass projection change with no per-row mechanism); (c) copy the deck's line to the kit now. The thirteen live wide rows (Lillard, Simons, Dončić, Flagg, Grimes, Coward, Mamukelashvili, Dick, Poeltl, Porter, Monk, Bridges, Barrett) can be decided ahead of the rest. | (a); the thirteen wide rows re-derived first when WO-5 starts |
| D-WO1-2 | Which plane is the reference where no dated mechanism exists? The work order says the kit; the deck is the surface drafted from and runs 3 points higher on 102 rows. | the kit, with the deck's higher line kept only where a dated outlet backs it |
| D-WO2-1 | The evidence file now rewrites itself from the live feed on every direct run (605 names). Keep, or write it only when the feed's content changed? | keep; the diffs are sorted and small |

## Provenance

- Inputs: the two repositories as merged this morning (kit main db21cfd, deck main b3986f8), ESPN's roster API (fetched 2026-10-01 by the verifier), no web research.
- Every number is a command's output or a field of `arena/results/planes_lines_2026-10-01.json`; the scratch cases and the red suite log are in `scratchpad pull1001/`.
