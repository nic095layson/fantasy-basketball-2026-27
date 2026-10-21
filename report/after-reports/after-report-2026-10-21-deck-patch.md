# The deck's missing-input crash, fixed; #151 merged — 2026-10-21

Pull window: 2026-10-21 → 2026-10-21 (build only; no roster pull, no box scores, no projection line or tag changed).

**Owner's request.** "Merge 151, build patch, and let me know if there is anything outstanding needed from me", 2026-10-21. "Patch" is decision 4 of `after-report-2026-10-21-gauntlet.md`: the season deck crashed on any morning without a matchup pull.

**What was analyzed.**
- Kit `main` `f63daf0` (after #151), branch `claude/market-data-workorder-mnfi2b`.
- The runner's committed 10/21 records, `season/daily` `8ba6534`.
- Deck `80eecdf`, unchanged.

**Method.**
- One assumption, stated in the plan: "build patch" means build it; merging it stays your word.
- A missing optional input is recorded as `present: false`, `sha256: null`. It is kept in the record, not dropped, so an absence stays visible.

**Headline.**
- **#151 is merged** (`f63daf0`). From 10/22 the runner's `morning.py --help` lists `--since`, so its pulls are time-guarded.
- **The deck crash is fixed in this PR and proven on the runner's real 10/21 tree:** the deck now builds there with no matchup file.
- **It reaches the runner only once this PR merges.** Until then, any morning whose FantasyBot pull fails publishes no deck.

---

## 1. Roster changes and the merges

No roster moved and no projection line or tag changed.

| PR | state | commit | note |
|---|---|---|---|
| kit #151 (GAUNTLET fixes) | **MERGED** | `f63daf0` | squash, pinned to head `e54d6e5`; main's tree equals that head's (checked) |
| kit branch | restarted from main | `5286246` | tree = main; fast-forward push |

## 2. The patch

**Cause** (EVIDENCE, from the GAUNTLET report §3, reproduced twice):
- `season_deck.py` loads `matchup_live` only if the file exists (`opt`).
- But its provenance record hashed every path in `paths`.
- The real morning's `default_paths` always names `data/news/matchup_live_<date>.json`.

**Why the suite missed it.** The existing test "missing records render nothing and do not halt" built from a fixture that names no `matchup_live` path at all. So the real morning's case, a path named but absent, was never exercised.

**The fix** (`scripts/season_deck.py`, the record's `inputs`):
- Each input now carries `present`.
- `sha256` is computed only when the file exists, otherwise `null`.
- Required inputs never reach this line missing, because `_load` halts on them first.

**The red-first test.** `test_a_named_but_absent_optional_input_builds_and_is_recorded_absent`:
- It names a nonexistent `matchup_live` path.
- It went red on the same `FileNotFoundError` as the runner, then green.

**Kit suite:** 238/238, twice.

**The behavioral check** (EVIDENCE, a scratch worktree of the runner's commit `8ba6534`, the patched script copied in):
- `season_deck.py --date 2026-10-21` printed `SEASON DECK: PASS — 2026-10-21: report/season/deck_2026-10-21.html (6 panes, 313 board rows, 16 status rows; record deck_record_2026-10-21.json pins 8 inputs)`. Exit 0.
- The record shows `matchup_live: present false, sha256 null`, and all 7 others present.
- The page embeds `"matchup_live":null`, so the Week pane's live card simply does not render.

**Other readers of the record:** two dated 10/19 report writers (`season-deck-2026-10-19/write_seasondeck.py`, `season-deck-audit-2026-10-19/write_audit.py`). They count the inputs and read `join`, and neither uses the hash strings. Unaffected.

**Bands, unchanged:** sweep on `80eecdf`, `redteam-2026-10-19/sweep.json`.
- **TEAM_WEEK_SHOCK is FRAGILE:** +2.7 (no shock) / −3.6 (shock doubled).
- **weekly_availability is FRAGILE:** −2.7 (no in-sim injury discount) / +0.5 (harsher risk tier 0.65) / −1.5 (healthy plays 0.95) / +1.0 (healthy plays 0.80).
- This report quotes no title share.

## Watchlist

- **Until this PR merges,** the runner's deck step still fails on any morning without a matchup pull. On those mornings the live page stays at the previous day's build.
- **The first daily cron fire into the runner is 2026-10-22 12:53Z.** A check-in is armed for 13:10Z.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| kit #151 | **MERGED** | `f63daf0` |
| deck missing-input crash (decision 4) | **BUILT**, this PR; not merged | red-first, then 238/238; builds on `8ba6534` |
| 7 risk rows, calibration date, evening routine, old routine | open, the owner's | GAUNTLET report decisions 2, 3, 5, 6 |

The flagged-name receipts are carried forward from the lock report. This build pulled nothing and researched no player, so they were not re-queried (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this build (did not check) |

## Repeat-name market check

This build did not change the deck page, which is still deck `80eecdf`, page sha256 6a5cefea4921. The GAUNTLET report replayed it today. Its table stands, carried here verbatim.

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

## Decision sheet

1. **Merge this PR**, ideally before 2026-10-22 12:53Z. Merging is your word.
2. The rest are carried from the GAUNTLET report, still open:
   - the 7 risk rows (decision 2);
   - the calibration check date (decision 3);
   - the evening status routine (decision 5);
   - deleting the old routine (decision 6).

## Bounds

**Out of scope by design.**
- Any projection line, tag, roster or engine constant.
- Any other optional-input handling in the kit. `matchup_live` is the only optional input `season_deck.py` names.

**In scope and unverified.**
- **The fix running inside the runner itself:** NOT-ATTEMPTED. It cannot run there before this PR merges. The scratch build on the runner's own committed tree is the stand-in.

## Provenance

- **Session:** Claude Code (cloud), 2026-10-21, about 15:39Z–16:00Z.
- **Governors:** plan-gate, loaded for this request with its block shown before the merge; adversarial-verify, before delivery.
- **Re-verify:**
  - `SEASON_POOL=1 python3 -m unittest discover -s scripts -p 'test_*.py'` (expect 238 OK);
  - on a checkout of `season/daily` `8ba6534` with this script, `python3 scripts/season_deck.py --date 2026-10-21` (expect PASS).
