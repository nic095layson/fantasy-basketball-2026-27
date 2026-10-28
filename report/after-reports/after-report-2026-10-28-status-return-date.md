# Status tiers registered, ESPN's return date in the waiver gate, the deck's Free Agents status, and team 5's 10-27 back-fill — 2026-10-28

Pull window: 2026-10-28 → 2026-10-28 (no pull for the kit: the pinned 10-28 inputs at 4559da0 on season/daily; ESPN's injury feed as read 16:15Z; one read-only Flaim get_roster for team 5 at 2026-10-27, pinned on season/daily at 264d0b6; no market pull).

**Method up front.** Owner 2026-10-28: "Merge 216, then proceed with 2-6". #216 merged (8ea9229) after `gates.py --verify` PASSed on its head 108bc19. Item 5 went to the owner as options before any build, and the owner picked "Use ESPN return date (Recommended)". Parameters stated to the owner before the build:
- An Out stays in the waiver scan when ESPN's expected return is at most 7 days after the brief's date. It keeps its full season value and is flagged with the date.
- Streaming counts that player's games on or after the return date.
- An Out with no ESPN return date stays set aside.
- Item 3 registers the tiers `uncalibrated` at their current values, with no value changed.
- Item 4 shows the status the brief's gate reads (`co_gm.fa_status`), as a label only.
- Item 6 is one dated read for team 5, pinned through the kit's own `daily` shape.

EVIDENCE marks what a run or read showed; INFERENCE marks what is derived.

## 1. Why ESPN's return date (EVIDENCE)

- ESPN's injury feed as read at 16:15Z lists 94 players, 73 "Out" and 21 "Day-To-Day". Each entry carries `details.returnDate`.
- ESPN's own status does not separate one game from a season. Tobias Harris (calf, "ruled out for Tuesday's game") and Jalen Williams (ankle surgery) are both "Out".
- The return date does separate them. Counted from 10-28: Harris back in 0 days, Santi Aldama 0, Justin Champagnie 2, Yves Missi 5, Dylan Cardwell 9, Jalen Williams and Cason Wallace 125.
- Of the 73 Out entries, 37 have a return date within 7 days.

## 2. What was built (EVIDENCE)

- **`co_gm.SHORT_OUT_DAYS = 7`.**
  - `fa_status(P, yahoo, espn, date)` attaches ESPN's return date to every listed player. That includes a player whose status comes from a Yahoo letter: Yahoo's letter still wins, and ESPN supplies the date.
  - It marks `short_out` when an Out returns within the line.
  - `free_agents` keeps a short Out and sets aside a long one, naming its return date. An unknown code is set aside whatever its date. Without the day's date, every Out stays set aside.
- **`co_gm.stream_rows`** builds the streaming candidates: a short Out's expected games are its games on or after the return date.
- **The brief** flags a short-Out pair as "O today (yahoo), ESPN expects back <date>, check before claiming". Its set-aside line names each player's return date.
- **`status_feed.espn_rows`** now pins `return_date` (ESPN's `details.returnDate`).
- **D-WS-1, the tiers registered.** `check_constants.py` now reads co_gm and status_feed, with paths, the owner's seat, the lines tag, the team-code map and the category alias ignored by name. Registered:

  | constant | status | decision |
  |---|---|---|
  | `co_gm.ESPN_TIERS` | uncalibrated | D-WS-1 |
  | `status_feed.TIERS` | uncalibrated | D-WS-1, with D-IS-6/7/10 |
  | `co_gm.SHORT_OUT_DAYS` | uncalibrated | D-WS-2 |
  | `co_gm.WAIVER_CANDIDATES` | uncalibrated | D-WS-1 |
  | `co_gm.SLOTS` | settings | data/league_settings.json roster_positions |

  `CONSTANTS CHECK: PASS — 39 registered = 39 live on deck 366d3ca`.
- **The deck's Free Agents tab.**
  - `season_deck` reads the day's Yahoo pull and ESPN pin as optional inputs (hashed in the record).
  - Each unrostered row shows its code, its source and, on an Out, ESPN's return date.
  - A note under the search box names the sources. On a day with neither pin it reads "No status pinned for the day: check each player before claiming."
- **Red first.** On main's code, 13 new waiver tests errored and one changed test failed; 2 registry tests and 5 deck tests failed. All pass now.
  - One test changed its expectation: the pinned ESPN row now carries `return_date`.
  - Kit suite: 681 tests, OK (2 skipped) on two runs. An earlier run, under parallel load, showed 1 failure whose name was lost because the output was cut to its last lines (ATTEMPTED-FAILED: the two re-runs did not reproduce it).

## 3. The 10-28 brief with the return-date rule (EVIDENCE: a re-run from the pinned 10-28 inputs, scratch worktree at 4559da0, `SEASON_POOL` set as the morning run sets it)

A first re-run without `SEASON_POOL` ran on the preseason v69 lines, and its no-move title read 28.9%: that was my setup error, not the change, and it was discarded. The re-run on the season pool reproduces #216's after run on every figure the rule cannot move:

| | #216 (status gate) | this PR (+ return date) |
|---|---|---|
| set aside | 8 | 4: Jalen Williams (Out, ESPN back 2027-03-02), Cason Wallace (O, back 2027-03-02), Kevin Porter Jr. (NA, no ESPN entry), Dylan Cardwell (O, back 2026-11-06) |
| short Outs back in the 40 | — | Tobias Harris (back 10-28), Justin Champagnie (10-30), Yves Missi (11-02), Santi Aldama (10-28) |
| positive pairs | 2 of 520 | 2 of 520 |
| top pairs | Cameron Johnson for Gillespie 32.45 (−0.16); Bobby Portis for Washington 31.48 (−1.13) | Cameron Johnson for Gillespie 32.5 (−0.2), flagged D; Bobby Portis for Washington 31.5 (−1.1) |
| streaming | Mamukelashvili, Melton, Nesmith (P), LaRavia, Horford | the same five |
| title (no move) | 32.6% ± 0.6 | 32.6% ± 0.6 (32.57 / 32.64 by seed) |

The rule changes no engine constant and no simulator input. On 10-28 it brought four short Outs back into the candidates, and none made a positive pair.

Every title share above carries the standing structural band (season sweep of 2026-10-26: current rosters, season pool, real schedule):
- **TEAM_WEEK_SHOCK is FRAGILE:** +2.7 (no shared games shock (0.0)) / -4.2 (shared games shock doubled (0.12)).
- **weekly_availability is FRAGILE:** -5.4 (no in-sim injury discount (risk 0.88 like healthy)) / +3.7 (harsher risk tier (0.65)) / +0.4 (healthy players play 0.95 of games) / -0.5 (healthy players play 0.80 of games).

The deck built from the same 10-28 records with this branch's `season_deck.py` drew itself: `deck_render_check` PASS, both pins read, and 22 free agents carry a status.

## 4. Item 6: team 5's 10-27 lineup (EVIDENCE)

- One read-only Flaim `get_roster` (team_id 5, as_of_date 2026-10-27) returned 14 players, the same as the read earlier today.
- It is pinned verbatim on season/daily as `data/source/flaim/pull_2026-10-28_backfill.json` (the `daily` block only, plus a `backfill` note). It is a separate file because `pull_2026-10-28.json`'s sha256 is cited by league_state.json and four other 10-28 records (league_state_am, status, league, week_matchup).
- Only `manager_log.py` reads the file: its glob is `pull_*.json`, and it reads `daily` and `rosters`, both safe here. week_matchup, form_board and league_table glob `pull_????-??-??.json`, which the back-fill's name does not match.
- `manager_log.py --date 2026-10-27 --no-transactions`: `MANAGER LOG: PASS — 2026-10-27: 12 lineups, 0 start(s) lost league-wide; profile 2026-10-22..2026-10-27 (6 day(s))`.
- Pushed fast-forward as 264d0b6 on season/daily.

## 5. Item 2: the retry rule (not applied here)

`RUNNER-ASK-v4.md` asks the runner conversation to set its two stored prompts byte-identical to the drafts:
- `morning_v4.txt`: 14,764 bytes, sha256 0f80b767…
- `pm_v2.txt`: 5,370 bytes, sha256 d7031f07…

The runner then reads both back with get_trigger. Both drafts start from stored texts that have not changed since they were verified this morning: the morning task was last updated 2026-10-27 19:53Z, the afternoon task 2026-10-26 19:28Z. Applying them is the owner's paste: this session's update_trigger was refused for those tasks earlier.

## 6. Bounds

**Out of scope by design.**
- No projection line, injury tag, roster or engine constant changed, and no tier value moved.
- The Trade Analyzer and the Board tab still show no status for the unrostered.
- 10-28's ESPN feed was read at 16:15Z, not by the morning run; tomorrow's run pins it with `return_date`.

**In scope and unverified.**
- **How good ESPN's return dates are** (INFERENCE).
  - Yves Missi's note reads "will miss an extended period of time", yet his return date is 11-02. The rule trusts the date, so on 10-28 it kept him in the candidates.
  - Nothing yet grades ESPN's dates against the games players actually returned for. The tag-outcomes ledger records what tagged players did, but not ESPN's dates.
  - This is new decision D-WS-2: calibrate the 7-day line, or grade the dates, once the pins carry a few weeks of `return_date`.
- **The 7-day line, `ESPN_TIERS` and the Yahoo letter tiers** are stated defaults, now registered `uncalibrated`. None has a sweep band. They gate which adds are scanned and do not enter the title simulation, so the season sweep does not cover them.

## 7. Next steps (owner decisions)

1. Merge this PR. From tomorrow's morning brief, the waiver scan reads ESPN's return date and the deck's Free Agents tab shows the status.
2. Paste `RUNNER-ASK-v4.md` (with its two files) into the runner conversation, before 22:03Z if the afternoon run should carry it today.
3. D-WS-2: when the pins hold about two weeks of `return_date`, grade ESPN's dates against the box scores and decide whether 7 days stays.

## Watchlist

- **Tomorrow's brief:** set-aside names carry "ESPN expects back <date>". A short-Out add, if one makes the top three, reads "ESPN expects back".
- **data/status/espn_injuries_2026-10-29.json** rows carry `return_date`.
- **Tomorrow's MANAGER LOG** profile window starts 2026-10-22 and includes 10-27.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| one-game Out treated as a season Out (item 5) | **FIXED** on the owner's pick | §1, §2, §3 |
| status tiers unregistered (D-WS-1) | **REGISTERED** uncalibrated; calibration open | §2 |
| deck Free Agents tab without status (item 4) | **FIXED** | §2, §3 |
| team 5's 10-27 lineup missing (item 6) | **BACK-FILLED**, manager log PASS | §4 |
| Flaim retry rule (item 2) | **DRAFTED**, awaits the owner's paste | §5 |
| ESPN return-date quality (D-WS-2) | **OPEN**, owner decision | §6 |

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
