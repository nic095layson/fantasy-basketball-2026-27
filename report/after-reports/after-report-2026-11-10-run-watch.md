# Run watch: one line saying whether the day's run left its records (owner pick 2026-11-10, "Decision card + watchdog", P4)

Pull window: 2026-11-09 → 2026-11-10 (no pull: report/briefs/morning_2026-11-09.json and morning_2026-11-10.json, the two days' morning and afternoon reports, decks and afternoon status files at be859ea on season/daily, read only; the account's scheduled-task list, read 2026-11-10; kit main a1c91ca, deck main 01483de).

**Method up front.** Order: the owner's card pick "Decision card + watchdog (Recommended)"; this report covers the watchdog. Tests were written first and seen failing. The script reads records and prints one line; it changes nothing. EVIDENCE marks what a run or a read showed.

**Verdict: `scripts/run_watch.py` says PASS or ALERT for a day's morning or afternoon run, from the records on a git ref or in a directory. The two scheduled checks that would run it and push to the owner on ALERT are not created yet: that happens only after this merges, on the owner's word.**

## 1. Why (EVIDENCE: the scheduled-task list)

The morning and afternoon Runner tasks show `last_run: SUCCEEDED`. For a task that wakes an existing session, that status records that the wake was delivered, not how the run went. No other scheduled task reads the run's result. A run that halts, or never starts, reaches the owner only if he opens the Runner's session.

## 2. What it checks

| phase | PASS needs | ALERT says |
|---|---|---|
| am | `report/briefs/morning_<date>.json` exists, reads, has verdict PASS and no failed step; the morning report and the deck exist | which of these is missing; the verdict; the failed steps by name (a non-fatal failure too: the run went on without that record) |
| pm | the afternoon report, `data/status/status_<date>_pm.json` and the afternoon deck exist | which is missing |

## 3. Behavioral check (EVIDENCE: runs on season/daily be859ea)

| run | line |
|---|---|
| am 2026-11-09 | RUN WATCH: ALERT — morning PASS but 1 step failed: league table (the team-rename failure of that day) |
| pm 2026-11-09 | RUN WATCH: PASS |
| am 2026-11-10 | RUN WATCH: PASS — morning PASS, 20 steps, no step failed (the same from `--ref origin/season/daily`) |
| pm 2026-11-10 | RUN WATCH: PASS |
| am 2026-11-11 (not run yet) | RUN WATCH: ALERT — no morning record; no morning report; no deck |

## 4. Checks

- Red first: `test_run_watch` (9 tests; the module did not exist).
- Whole suite on this branch: 919 tests OK (2 skipped).

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds (season sweep 2026-11-09, engine 01483de). This script touches no title figure.

## 5. Bounds

- Out of scope by design: the script does not judge the content of a run (a PASS run with a wrong number passes); gates and the audit do that. It does not re-run anything.
- In scope and unverified: the push notification itself, which exists only once the scheduled tasks do (did not check).
- Runs are dated by UTC. The afternoon run fires at 3 PM Pacific (23:00 UTC in winter), so its check must fire before midnight UTC of the same date.

## 6. Next steps (owner decisions)

1. **Merge, then two scheduled checks (Recommended):** 06:30 Pacific for the morning run and 15:45 Pacific for the afternoon run (15:45, not the 16:30 first proposed: 16:30 Pacific is past midnight UTC, the next run date). Each starts a fresh session, fetches season/daily, runs this script, and sends one push only when the line says ALERT.
2. Morning check only.
3. Merge the script and create no scheduled task (run it by hand).

Runner impact: none. The Runner's runs and prompts are untouched; the checks would be separate scheduled tasks.

## Fired

plan-gate (loaded; compact plan table shown before the first edit) · council (loaded; ruling 4–1) · adversarial-verify (loaded this turn).

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
