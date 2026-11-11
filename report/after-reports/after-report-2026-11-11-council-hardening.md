# Council on today's fixes: one small build, one drill, one correction, one step flagged for the owner's cancel (owner 2026-11-11)

Pull window: 2026-10-17 → 2026-11-11 (one fetch in scratch: ESPN and Basketball-Reference box scores for 2026-11-10, twice, by the kit's own `box_pull.py`, written only to the scratchpad; else no pull: the morning records, run ledger and manager-log files at 61b05c1 on season/daily, read only; kit main c1cb150).

**Method up front.** Owner's card answer, verbatim: "Have council deliberate, and proceed with recommendations. Any that prove 'theatrical' and non-fruitful, flag to me for final cancel of run." It followed a diagnostic the same day that rated each function and proposed four fixes. The council (five roles, one vote) was run on those four; its verdict was shown to the owner before the first edit, with the plan. Parameters: step times are the gaps between consecutive run-ledger rows over the mornings of 11-06 to 11-10 (the ledger stamps a step when it ends, so each gap is charged to the later step); the drill used the 11-11 morning's committed records with the box-score step marked failed and its file removed. EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: the manager log now reports how many rows Flaim could not read (6 on the newest response on file). The resume path was drilled on a real morning and works. The team-rename fix the diagnostic proposed already existed, so nothing was built for it and the diagnostic's "it will recur" was wrong. The IL-return step's two "late" worlds are flagged for the owner's cancel; nothing was cut.**

Runner impact: code-only — `manager_log.py` adds one clause to its MANAGER LOG line and one key to `data/managers/transactions.json`. No prompt edit.

## 1. Council verdict (4–1)

Build the team-rename fix and run the recovery drill; from the small hardening keep only the unreadable-row count and drop the extra transactions tests (a step that has passed 22 of 22 does not need them today); do not cut the IL-return worlds without the owner's word; leave tag outcomes, the lineup log and decision grades running. The dissent wanted no hardening at all.

## 2. The correction: the rename fix was already built

EVIDENCE: `git log -S` on `scripts/league_table.py` and `scripts/league_pairings.py` shows the team-key matching landed on 2026-10-29 (95cf5a3) and 2026-11-09 (7a974cf), each with a rename test. Replayed today on the records branch with current code, into a scratch folder: `league_table.py --date 2026-10-29` PASS, `--date 2026-11-09` PASS, `--date 2026-11-11` PASS. The three recorded step failures were each fixed the day they happened. The diagnostic rated the two steps "Watch" correctly by its 14-day rule, but its line "it will recur whenever a manager renames" was not checked against the code and was wrong.

## 3. The build: rows Flaim could not read

Flaim's `get_transactions` response carries a warning when Yahoo's page held entries it could not interpret, and a count of rows dropped for a bad timestamp. The manager log read only the rows. It now reads both figures from the newest response, writes them under `feed` in `data/managers/transactions.json`, and adds "Flaim could not read N row(s) on Yahoo's page (the moves on record may be short)" to its line when N is above zero. No row and no count of moves changes.

| check | result |
|---|---|
| 5 new tests, seen failing first (5 errors), then passing | `FeedShortfall` in `scripts/test_manager_log.py` |
| The newest real response in this session's transcript | 6 uninterpreted, 0 dropped |

## 4. The drill: resume on a real morning

EVIDENCE: a scratch worktree of season/daily at 61b05c1. The 11-11 morning record was rewritten to the state a failed fetch leaves (preflight, league live and matchup live PASS; box scores FAIL; the other 18 steps absent) and `data/actuals/2026-11-10.json` was deleted. Then `morning.py --date 2026-11-11 --since 2026-11-11T13:00:00Z --resume`.

| check | result |
|---|---|
| Exit and line | exit 0; `MORNING: PASS — 2026-11-11: 22 steps (after 1 earlier attempt(s))` |
| The three passed steps | kept byte-for-byte as recorded; not run again |
| The record | first run's time kept, `resumed_at_utc` set, one entry under `attempts` naming the box-score step |
| Box scores | re-fetched: 6 games, 154 player lines, every stat cell equal to the committed file; the one difference is Jamal Cain, who has since gained a pool row |
| Brief | title 15.56 / 16.56 on the two seeds, the same as the committed brief; same lineup; same top pair |

Two steps printed FAIL (non-fatal) in the drill: tag outcomes and decision log. Both ledgers already held the day's rows, because the drill started from the finished morning's files, and both refuse a second append. INFERENCE: on a real failed fetch those steps have not run yet and will not refuse. The same refusal is what the two recorded 11-02 failures were.

## 5. Flagged for the owner's cancel (nothing cut)

| step | cost | what it yields | reading |
|---|---|---|---|
| IL return: the "2 weeks late" and "4 weeks late" worlds | about half of the step's ~132 s; the step is 41% of a ~5.4-minute morning | 25.81% and 25.86% beside "on time" 25.95% on 11-11 | The three are the same within sampling error; the "slip range" line carries no information |
| IL return: the "on time" world itself | the other half | 25.95% against 16.06% with no returns | One comparison worth having, though it moves 11.5 points on the hand-set room rule |
| Tag outcomes | under 1 s | 459 rows; no script reads them | Idle until the season-end review; not wasteful |
| Lineup log | under 1 s | 6 days, 1 pair, 0 nights graded | Low yield so far |
| Decision grades | about 1 s on Mondays | 0 verdicts | By design until the first 28-day window closes on 11-17 |

## 6. Checks

- Full suite: 1137 tests OK, 2 skipped.
- The three league-table replays and the drill, above.

## 7. Bounds

Out of scope by design: no projection line, injury tag, roster or engine constant changed; season/daily was not written; the IL-return step was not changed.

In scope and not verified:
- The resume path inside the Runner's own session. NOT-ATTEMPTED: it needs a real failed morning there.
- Step times are read from ledger gaps over 5 mornings, not from a timer inside each step.
- Whether an append-only step that refuses a duplicate should print PASS instead of FAIL was not decided; it is an owner decision below.

## 8. Next steps (owner decisions)

1. Merge this PR, or hold.
2. IL return: cancel the two "late" worlds (recommended), cancel the whole step, or keep all four.
3. Append-only refusals: leave as FAIL (non-fatal), or have a duplicate append read as "already recorded" so a re-run does not raise a watchdog alert.

## Fired

council (loaded on the owner's word) · plan-gate (loaded; compact plan table shown before the first edit) · adversarial-verify (loaded before the commit) · scope-fence not loaded: one adjacent question (the append-only refusals) was flagged above, not fixed.

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds. The title figures quoted here (16.06% and the IL-return worlds) are the 11-11 morning's, 10,000 seasons on two seeds.

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
