# Red-team attacks fingerprint the engine's content, not the deck's commit — 2026-10-23

Window: the kit at `main` `679fc8b` plus this branch; the deck at its newest commit `483482b` and at the pinned `048efb6`. No projection line, tag, roster, ledger row, engine constant or attack record changed.

Pull window: 2026-10-23 → 2026-10-23. No pull: the change is to a checker and its tests; it reads the deck repo's git history only.

**Owner's decision (2026-10-23, D1 of the system audit).** "Content hash of engine files (Recommended)": an attack record is STALE only when the engine files changed between its commit and the live one, not when any deck commit landed. The audit found that the deck's `483482b` (a CLAUDE.md-only change) staled 5 of 9 attack records and failed the attacks check on a current deck checkout.

**Method (stated before the build).** "The engine" is what the run-ledger already defines it as: `run_ledger.ENGINE_FILES` = `scripts/hoops.py` and `arena/arena.py` in the deck. A revision's engine fingerprint is the last commit at or before it that touched those files (`git log -1 <rev> -- <files>`), so two revisions with the same fingerprint have byte-identical engine files. A record whose commit has the same fingerprint as the live commit is CURRENT; a different fingerprint, or a commit not in the deck's history, is STALE. Records keep their commit field; nothing is re-run.

## 1. What changed (EVIDENCE)

- `scripts/redteam/run_attacks.py`: `engine_commit(deck, rev)` and `_same()`; `check(..., deck=None)` compares engine fingerprints when `deck` is given, the commit alone otherwise (the old behaviour, kept for the existing tests); the record carries `live_engine_files_commit`; the PASS line reads "on engine <commit> (engine files last changed <commit>)".
- `scripts/test_redteam_attacks.py` class `EngineFingerprint`: a temp git repo with three commits (engine v1, docs only, engine v2). Red first: 3 errors on the unchanged code (`check()` took no `deck`, no `engine_commit`); then 10 of 10.

## 2. On the live decks (EVIDENCE)

| deck checkout | before | after |
|---|---|---|
| `048efb6` (the kit's pin) | PASS, CURRENT 5, UNFINGERPRINTED 4 | PASS, CURRENT 5, UNFINGERPRINTED 4, engine files last changed `95ebade` |
| `483482b` (newest) | **FAIL**, A-1, A-5, A-7, A-8, A-9 STALE | PASS, CURRENT 5, UNFINGERPRINTED 4, engine files last changed `95ebade` |

Both checkouts resolve to the same engine fingerprint `95ebade`, which is the last deck commit touching either engine file; `048efb6` and `483482b` differ only by CLAUDE.md.

## 3. Bounds

- **Not changed:** `check_constants.py` and `sweep.py` still record the deck commit in their records; the attacks checker reads those commits and resolves them to fingerprints, so no record format changed. The run-ledger's `live_engine` check already used this definition.
- **Assumption A1 (unconfirmed):** the deck's engine is fully described by `ENGINE_FILES`. A change to another deck file that the engine imports (none today in `arena/` besides `arena.py`; `scripts/hoops.py` is self-contained per the ledger's definition since 10/21) would not stale the records. The same assumption the ledger already carries.
- **Out of scope by design:** the sweep itself, the registry, the attack scripts.

**Bands.** This change computes no figure; the standing sweep's bands (`redteam-2026-10-19/sweep.json`, engine 048efb6, fingerprint 95ebade) are unchanged:
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

## Watchlist

- **The next engine commit in the deck:** the attacks check must go STALE on it (the `EngineFingerprint` test covers the mechanism; the live case is the check).

## Open-item receipts

| item | status | receipt |
|---|---|---|
| attack records STALE on a doc-only deck commit | **FIXED** on this draft PR | §1, §2 |
| `test_matchup_live` transcript dependence | **OPEN**, flagged (PR #172) | — |

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck 048efb6 and at 483482b, checked today, the same page the 10/22 day report replayed. Its table stands, carried here verbatim from the day report.

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
