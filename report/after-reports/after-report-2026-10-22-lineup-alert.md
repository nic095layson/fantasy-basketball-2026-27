# The 3 PM lineup check and the Today tab's free-agent notice — 2026-10-22

Window: the kit at `main` `46984bb` plus this branch. The replays read the `season/daily` records at `c283a11` (the 10/22 morning run and its restored pull). No projection line, tag, roster, ledger row or engine constant changed.

Pull window: 2026-10-22 → 2026-10-22. There was no new pull: both replays read records already logged.

**Owner's request (2026-10-22).** "Can you please integrate at the 3PM pull, if I have any players that are eligible to play but are on my Bench, can you please send me a notification through Claude? Additionally, if there is a player on my starting lineup who is much worse (Let's say Washington, and Durant on my bench), please notify me to make this roster change as well. I'd like for you to scan also - if there is a valuable player available in the free agent pull, to make this notice to me on the 'Today' tab of the Season tool."

**Method (stated to the owner before the build, owner answers in quotes).**
- **Swap rule.** "I like option 1, but also want to build and integrate option 3 where it is dynamic and matchup-up aware."
  - A move is notified when the slot is **empty**: the bench player has a game today, and the starter he would replace has none, is Out, or the slot is open.
  - **Changed 2026-10-23 (owner):** "In this case, I'd rather start Queta for Washington if it would better help me win this week's matchup." When both players have a game, the move is notified only when starting the bench player today adds `LINEUP_D_EXP` 0.05 or more expected categories won this week. This uses the week card's model: today's swap only, the rest of the week unchanged. The season-value gap is shown in the message, but it is no longer a bar. The first build also alerted on a season gap of 1.0 or more (`LINEUP_GAP`); that constant is removed.
  - The best lineup is the kit's ten-slot fill (`CG.daily_lineup`, by value) over the players who play today and are not Out.
- **Notify.** "Push only when needed." The script prints a `PUSH:` line only when there is an alert.
- **Free-agent notice.** "Beats my weakest by 1.0+." A free agent is listed when his season value per game beats your weakest non-IL player's by `FA_NOTICE_GAP` 1.0 or more. The top `FA_NOTICE_TOP` 3 are listed. Beside them is the week card's best This Week move, when it adds `FA_NOTICE_D_EXP` 0.10 or more expected categories.

**Changed 2026-10-23 (owner, D2 of the system audit: "Default to the season pool on #176").** `week_matchup.py` and `lineup_check.py` read their lines through `co_gm.load_pool`, which used the preseason v69 pool unless `SEASON_POOL` was set; `morning.py` sets it, a hand run did not, and the runner prompt handed over on 10/22 did not. Now `week_matchup.build` sets `SEASON_POOL` to `data/season/pool_season.csv` when the variable is unset and that file exists (`SEASON_POOL_DEFAULT`), and both PASS lines name the pool ("pool pool_season.csv"). Red first: 2 failures on the unchanged code (`inputs.pool` = "v69 preseason pool"; no pool in the lineup line), then 77 of 77. On today's records a hand run of `week_matchup.py` with no variable now reproduces the morning record exactly (3–6–0, 3.5655), and a hand run of `lineup_check.py` gives the same moves and alerts as the `SEASON_POOL` run (`system-audit-2026-10-23/lineup_replay_2026-10-23_seasonpool.json`). The 10/22 replays quoted in §3 below ran on the preseason pool (the record said so in `inputs.pool`); their alerts are unchanged on the season pool.

## 1. What changed (EVIDENCE)

- `scripts/week_matchup.py`:
  - The four constants are at line 84 (`LINEUP_GAP` removed 2026-10-23). `lineup_moves` is at line 304, `today_swap_value` at 325, `lineup_alerts` at 337 and `fa_notice` at 344.
  - The record carries `lineup_today` and `fa_notice` (line 710).
- `scripts/lineup_check.py` (new):
  - It runs the week card's build with the same inputs.
  - It writes `data/news/lineup_<date>.json`.
  - It prints one line: `LINEUP CHECK: ALERT`, `OK` or `FAIL`. On an alert, a `PUSH: Lineup — …` line follows with the text for the notification.
  - It changes no value.
- `scripts/season_deck.py`: `faNotice` (line 385) draws a "Worth a look" card at the top of the Today tab, only when a free agent passes a bar (line 425).
- Tests:
  - `test_week_matchup.py` classes `LineupToday` (line 293) and `FreeAgentNotice` (line 364).
  - Two record tests run `lineup_check.py` end to end (lines 430 and 446).
  - `test_season_deck.py` lines 591 and 602.

## 2. Tests

- The deck card's test was written first and failed on the unchanged page ("Worth a look" absent). It passes with the card. The red-first counts for the week_matchup tests are not recorded here (did not check).
- `test_week_matchup.py` 55 OK; `test_season_deck.py` 74 OK.
- 2026-10-23 change: the alert test was rewritten to the owner's rule. Its Queta case (gap 1.13, this week −0.02) must not alert. It failed on the first build's code (1 failure), then passed.
- Full suite: 399 run, 1 failure, 1 skipped. The failure is `test_matchup_live.test_todays_transcript_yields_todays_outlook`, the known transcript-dependent test that fails identically on main.

## 3. On real records (EVIDENCE; `lineup-alert-2026-10-22/`)

- **2026-10-22:** `LINEUP CHECK: OK — no move`. Only CLE, DEN, OKC and PHI play, and Yahoo's lineup already starts the best of yours who do (`lineup_2026-10-22.json`).
- **2026-10-23 (rosters as of the 10/22 morning pull):** `LINEUP CHECK: ALERT`; 3 moves in the first build, 2 after the 2026-10-23 change (`lineup_2026-10-23.json`):
  - Start Kevin Durant (HOU) for Christian Braun, who has no game: +0.39 expected categories this week.
  - Start Derrick White (BOS) for Miles Bridges, who has no game: +0.43.
  - Start Neemias Queta (BOS) for PJ Washington: season value **+1.13**, this week **−0.02**. In the first build the season bar fired and the move was notified. **After the 2026-10-23 change it is not notified**: the replay alerts on 2 moves (Durant, White), and Queta stays in the record's `moves` but not in `alerts`. Two runs were byte-identical. The evidence files are the post-change run.
- **The Today card on today's records:**
  - Collin Gillespie (PHX) for PJ Washington, season gap +1.03.
  - This week: Anfernee Simons (PHI) for Neemias Queta, +0.38 expected categories.
  - It renders at 400 px with no page error (`today_400.png`).

## 4. Bounds

- **Assumption A1 (unconfirmed):** the afternoon league state carries Yahoo's slots as they stand at 3 PM. The check reads the slots from `data/league_state.json`, which the 3 PM run re-pulls. It is confirmed by the first afternoon run whose slots match Yahoo's page.
- **The runner wiring is not in this PR.** The 3 PM scheduled task's prompt is the owner's to change. The text for it was given to the owner beside this report. Until the prompt changes, nothing runs `lineup_check.py` and no push is sent.
- **Push delivery depends on the runner session's tools.** A Claude push notification needs the PushNotification tool in that session. The prompt tells the runner to say so at the top of its report when the tool is missing. This was not tested from the runner (did not check).
- **INFERENCE:** the matchup bar values one day's games, so its figures are small (the Queta move reads −0.02), and 0.05 is a low bar. A swap that helps this week by less than 0.05 is not notified.
- **Out of scope by design:** making the move (Flaim is read-only), and changing any value or constant.

**Bands.** The lineup check and the notice use neither FRAGILE constant of the standing sweep (`redteam-2026-10-19/sweep.json`, engine 048efb6). The shared shock is left out, and availability is the day's status, as on the week card. The sweep's bands for those constants, quoted:
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

## Watchlist

- **The first 3 PM run after the owner merges and pastes the prompt:** the `LINEUP CHECK` line is at the top of the report, and a push arrives on an alert. That run also confirms A1.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| bench player playing while a starter sits, no notification | **BUILT** on this draft PR; live after merge + runner prompt | §1, §3 |
| valuable free agent not surfaced on the Today tab | **BUILT** on this draft PR | §1, §3 |
| `test_matchup_live` transcript dependence | **OPEN**, flagged (PR #172) | §2 |
| afternoon pull overwrote the morning's matchups/free agents | **OPEN** on draft PR #175 | `after-report-2026-10-22-pull-carry.md` |

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck 048efb6, the same page the 10/22 day report and the odds-tiles report replayed. Its table stands, carried here verbatim from the day report.

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
