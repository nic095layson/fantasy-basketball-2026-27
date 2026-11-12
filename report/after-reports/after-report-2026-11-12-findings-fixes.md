# Fixes for audit findings F1 to F4 (owner 2026-11-12)

Pull window: 2026-10-17 → 2026-11-12 (no pull: kit main 94117d8 plus this branch; the records branch season/daily at c14c1ec (this morning's run) and db51bfb (afternoon), read only, in a scratch copy; the scheduler's task list read once; two simulation runs in scratch, nothing written to the records).

**Owner's request, verbatim:** "Conduct effective, logical and meaningful fixes for Findings 1-4, provide afterreport."

**What was changed.** `scripts/morning.py`, `scripts/sweep_record.py`, `scripts/daily_brief.py`, `scripts/season_deck.py`, `scripts/redteam/run_attacks.py`, `scripts/redteam/attacks.json`, `scripts/il_return.py`, their tests, and one analysis folder, `report/after-reports/findings-fix-2026-11-12/`. The findings are those of `after-report-2026-11-12-system-audit.md`, section 6.

**Method up front.** Each fix's parameters were shown to the owner in one plan table before any file was written. Tests first for F1, F2 and F3. F1 and F2 were then replayed on a scratch copy of this morning's records (commit c14c1ec with this branch's scripts). F3's exemplar, attack A-10, was re-run with its known-answer checks at the script's default (10,000 seasons, seeds 2026 and 2027). F4 ran four drop pairs under the baseline and the ten sweep variants whose shift on 2026-11-12 was not zero, at the sweep's own setting (6,000 seasons, seeds 2026 and 2027), on the afternoon state and season pool, real schedule, returns Tyrese Haliburton 2026-11-21 and Kawhi Leonard 2026-11-23 (reported dates, not confirmed; the same as the 2026-11-11 run).

**Verdict: F1, F2 and F4 are fixed and verified. F3's mechanism is built and tested and is live on the new drop-order attack, but its exemplar could not be switched over: re-running A-10 failed one known-answer check, which exposed a real defect in the "if IL players return" figure (two rivals' IL players are counted as playing every week). That defect is reported here and left for the owner's pick, not fixed.**

Runner impact: code-only — the morning sequence gains one step ("manager log", 24 steps on a fetch morning, was 23). The Runner's prompt already calls get_transactions and the dated rosters before `morning.py`, so nothing in the prompt has to change; its later standalone manager-log call finds the same rows and writes the same bytes. One visible change: a manager-log HALT now appears in the morning record as a failed non-fatal step, so the run watch will alert on it, as it does for every other step.

## 1. What each fix does

| Finding | Before | After | Evidence |
|---|---|---|---|
| F1 moves file rewritten after the deck pinned it | `manager_log.py` ran after `morning.py`; no ledger row. This morning's deck pinned yesterday's file (146 moves) while the commit carried 156 | A non-fatal step "manager log <yesterday>" right after the box scores, on fetch mornings, with the run's `--since`; it precedes the brief, the week card and the deck | Replay on c14c1ec with yesterday's moves file restored: step PASS; a second run left all 22 files under `data/managers/` byte-identical; the rebuilt deck's `league_tx` pin equals the file (3883cedc839c79dc both) |
| F2 sweep labelled "current rosters" at three days old | "season sweep of 2026-11-09 (current rosters, season pool, real schedule)" | "season sweep of 2026-11-09 (3 days old; rosters of that date, season pool, real schedule)" on the brief and the deck; "made today" on a Monday | The rebuilt deck of 2026-11-12 prints the new label; four label tests |
| F3 attack fingerprint ignored kit scripts | A record read CURRENT whenever the deck engine was unchanged | An attack may list `kit_files`; its record carries their sha256 (`fingerprint.kit_sha256`); a changed file, or a record with no hash, reads STALE and fails the gate | Four tests (one changed byte flips CURRENT to STALE); live on A-11. A-10 not switched: see section 2 |
| F4 drop order had sampling error only | Four figures from 2026-11-11, each ± 0.5 | The four pairs under 11 configurations; record and script on the attack list as A-11 | Section 3 |

`il_return.py` also gains `--checks --attack-record PATH`, which writes A-10's known-answer record with the script's own hash, so the record no longer depends on a hand-assembled file.

## 2. What the A-10 re-run found (new, not fixed)

| Check | Result |
|---|---|
| "never" world equals the brief's headline, both seeds | ok (20.56 / 19.92 both) |
| every return in week 1 with the room rule off equals IL included, both seeds | ok (34.60 / 33.62 both) |
| every return after the last week equals the headline, both seeds | **FAILED: 18.68 / 18.45 against 20.56 / 19.92** |
| the owner's own returns do not lower his title odds | ok (36.11 against 20.24, ± 0.56) |
| title falls with the slip (+2 wk, +4 wk) | not run since 2026-11-11, when those worlds ended |

EVIDENCE for the cause, read from the code and today's state: since PR #246 (2026-11-09) `co_gm.team_roster(include_il=True)` adds a team's unpooled players that have an auto season line, IL slot included; `il_return.il_players` reads only the pooled list. Two IL-slot players are in the first and not the second: Nolan Traore (seat 5) and Morez Johnson Jr. (seat 9). They get no return week and no roster-room drop, so they play every week in every return world. The headline (20.2%) is not affected: it excludes IL slots on both lists.

INFERENCE: the brief's "if IL players return" figure, and every figure this session quoted from that scenario on 2026-11-11 and 11-12, is too low for the owner by about the size of the failed check's gap, 1.7 points at 10,000 seasons × 2 seeds (± 0.56). The size on the on-time world itself was not measured.

The standing A-10 row still names the 2026-10-31 record and reads CURRENT by the deck fingerprint; the row carries a `kit_files_pending` note, and the failed record is at `findings-fix-2026-11-12/rt_il_return_2026-11-12_FAILED.json`.

## 3. F4: the drop order under the sweep's variants

Title odds, mean of two seeds, 6,000 seasons each. Sampling error about ± 0.8 on each figure and about ± 1.1 on a difference between two columns.

| Configuration | Rule's pick (Queta, then Washington) | Queta + Cam Johnson | Champagnie + Queta | Champagnie + Cam Johnson |
|---|---|---|---|---|
| baseline | 25.12 | 27.09 | 26.49 | 26.23 |
| binomial floor only (1.0) | 25.79 | 28.58 | 27.70 | 27.32 |
| inflation 1.30 | 23.68 | 26.24 | 25.53 | 24.96 |
| no shared games shock (0.0) | 27.70 | 30.55 | 29.77 | 29.33 |
| shared games shock doubled (0.12) | 20.58 | 22.93 | 22.78 | 22.37 |
| no in-sim injury discount | 23.88 | 26.26 | 25.58 | 25.83 |
| harsher risk tier (0.65) | 24.24 | 26.73 | 26.50 | 26.05 |
| healthy players play 0.95 of games | 22.63 | 25.87 | 25.58 | 24.87 |
| healthy players play 0.80 of games | 26.75 | 28.04 | 27.96 | 27.75 |
| 3.0 games per healthy week | 24.45 | 25.96 | 25.27 | 25.02 |
| 4.0 games per healthy week | 24.95 | 27.77 | 26.76 | 27.03 |

| Reading | Result |
|---|---|
| Cutting PJ Washington (the rule's pick) | last in 11 of 11 configurations; behind Queta + Cam Johnson by 1.3 to 3.2 points |
| Queta + Cam Johnson | first in 11 of 11; ahead of Champagnie + Queta by 0.1 to 1.0 and of Champagnie + Cam Johnson by 0.3 to 1.3 |
| Champagnie + Queta against Champagnie + Cam Johnson | −0.3 to +0.7; the order flips in 2 of 11 |
| Each column's own level | moves about −4.5 to +3.5 across the variants |

**What holds:** do not cut Washington. **What does not separate:** the three pairs without him sit within one sampling error of each other in most configurations; the model does not choose among Queta, Champagnie and Cam Johnson, so that choice is the owner's read (his 2026-11-12 instinct: Queta first).

Caveat that applies to every cell: the defect in section 2 is in these runs too. It gives seats 5 and 9 one extra player each in all four columns alike, so the levels are low and the differences between columns should be little affected; that last clause is inference, not measured.

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds. That is the 2026-11-09 sweep the brief quotes, for the headline title odds; the table above is the same variants applied to the drop pairs.

## 4. Verification

| Check | Result |
|---|---|
| Full suite | 1,185 tests OK, 2 skipped (was 1,174), 159 s |
| New tests | morning sequence 2, sweep label 1, attack fingerprint 4, A-10 known answers 4; two existing morning tests updated for the new step |
| Attack list | 11 attacks: CURRENT 10, UNFINGERPRINTED 1; 1 carries a kit fingerprint (A-11) |
| Gates | PASS and verified (see the commit) |

## 5. Bounds

Out of scope by design: the sweep's Monday cadence (owner's 2026-10-26 pick) is unchanged; no projection line, tag, roster or engine constant was touched; kit fingerprints were not added to attacks A-1 to A-9 (their scripts are frozen post-mortem files beside their records, or are re-run by every gate).

In scope and unverified:
- F1 with the Runner's own transcript: NOT-ATTEMPTED here, because that transcript is not on this machine. The replay used this session's transcript, whose transactions response is older and added no new moves. The first live proof is the 2026-11-13 morning run: its record should show "manager log 2026-11-12" PASS and the deck's `league_tx` pin should equal the committed file.
- The size of the section 2 defect on the on-time figure: NOT-ATTEMPTED, by choice; it is measured by the fix's own before-and-after.
- F4 differences under that defect: inference, as stated.

## 6. Next steps (owner decisions)

1. The IL-return defect: count unpooled IL-slot players as IL players in `il_return.il_players` (recommended; small, with a test, then A-10 is re-run and switched to the kit fingerprint), or leave the scenario as is and note the bias on the brief.
2. Sweep cadence: keep Mondays (recommended; the label now tells the age) or re-run on a mid-week day as well.
3. The cuts for Haliburton and Kawhi: the owner's call among Queta, Champagnie and Cam Johnson; the model only says not Washington.

## 7. Provenance

Session of 2026-11-12 (session model A) on branch `claude/market-data-workorder-mnfi2b`. Records: `findings-fix-2026-11-12/drop_band.json` (deck 01483de, records db51bfb, state, pool and schedule hashes inside), `drop_band.py`, `rt_il_return_2026-11-12_FAILED.json`. Re-verify: `python3 scripts/redteam/run_attacks.py --check`; `python3 -m unittest test_morning test_sweep_record test_redteam_attacks test_il_return` in `scripts/`.

## Watchlist

- 2026-11-09: week 3 on the accuracy card, the candidate's second graded week under D-ML-1.
- 2026-11-16: the week-5 confidence re-run; re-run `backtest.py` on about 20 games per player.

## Open-item receipts

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck 366d3ca (this PR changes no deck file), checked today, the same page the 10/22 day report replayed. Its table stands, carried here verbatim from the day report.

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
