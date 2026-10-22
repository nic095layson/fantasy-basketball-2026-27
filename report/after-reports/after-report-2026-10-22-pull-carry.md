# The day's pull file keeps the morning's matchups and available players — 2026-10-22

Window: the kit at `main` `46984bb` plus this branch; the 10/22 records on `season/daily` (morning pin `e7b69bb`, afternoon pin `3fab26c`, rosters `ee3f7fe`). No projection line, tag, roster, ledger row or engine constant changed.

Pull window: 2026-10-22 → 2026-10-22. No new pull: the replay reads the 10/22 morning and afternoon pins, already logged.

**Owner's question (2026-10-22).** The runner reported that the 3 PM checks rewrote `data/source/flaim/pull_2026-10-22.json` without this morning's matchups and available-player list. Asked "What option do you recommend": recommendation given (carry them forward, as the file already does for lineups). **Decision: "Carry them forward (Recommended)".**

**Method (stated before the build).** When a later run for the same date re-pins the pull and has no matchups or no available-player list of its own, the earlier pin's are kept and `carried_forward` names them; a later pull with its own wins. No pull time is stamped: the pull file never records one (assumption A1 below), so the mark says only that the section came from the day's earlier pin.

## 1. What changed (EVIDENCE)

- `scripts/flaim_live.py`: `keep_daily` (line 99) now also keeps `matchups` and `free_agents` from the earlier pin when the later pull has none, and writes `carried_forward`; a later pull with its own drops the mark. `league_live.py` already calls it for every same-date re-pin (line 250), so no caller changed.
- Tests: `test_flaim_live.py`, two new (line 133: an afternoon pull with none keeps the morning's; line 141: a later pull's own win).

## 2. Tests

- Red first: the carry-forward test errored on main's code (`KeyError: carried_forward`; the morning's sections were gone); the guard test already passed (existing behaviour). Then 19 of 19 in `test_flaim_live.py`.
- Full suite: 387 run, 1 failure (`test_matchup_live`, the known transcript-dependent test, failing identically on main), 1 skipped.

## 3. On today's real pins (EVIDENCE)

- Replay: this afternoon's pull (`3fab26c`) re-pinned over this morning's (`e7b69bb`): the matchups and the available-player list equal the morning's, the rosters are the afternoon's, `carried_forward` = free_agents, matchups.
- The week card on the replayed file: `WEEK MATCHUP: PASS`, to date from Yahoo, 88 available players in the pool, 83 moves scored (`pull-carry-2026-10-22/week_matchup_replay_2026-10-22.json`). It reads main's records, which lack the 10/21 box scores (they are on `season/daily` only), hence "1 missing" day and 83 moves where the runner's rebuild on `season/daily` had 0 missing and 84; that difference is the records, not this change.

## 4. Bounds

- **Assumption A1 (unconfirmed):** the carried sections are the day's first run's; true while only the morning run pulls matchups and available players (the 3 PM prompt pulls rosters only).
- **Out of scope by design:** today's already-written 10/22 pull file is not repaired (`morning_copy_2026-10-22.json` already holds the morning's); the runner prompts are unchanged.

**Bands.** This change reaches no engine figure: it decides which pinned Yahoo sections the week card reads, and touches neither FRAGILE constant of the standing sweep (`redteam-2026-10-19/sweep.json`, engine 048efb6):
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

## Watchlist

- **Tomorrow's 3 PM check:** its pin should show `carried_forward` and keep the morning's matchups and available players.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| a same-day re-pin dropped the morning's matchups and available players | **FIXED** on this draft PR | §1 |
| `test_matchup_live` transcript dependence | **OPEN**, flagged (PR #172) | §2 |

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward as the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck 048efb6, checked today, the same page the 10/22 day report and the GAUNTLET report replayed. Its table stands, carried here verbatim from the day report.

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
