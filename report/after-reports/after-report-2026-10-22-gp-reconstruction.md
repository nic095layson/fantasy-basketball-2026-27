# Rebuilding past seasons' games played: the 2025-26 test — 2026-10-22

Pull window: 2026-10-22 → 2026-10-22. The data read covers the 2025-26 season (2025-10-21 to 2026-03-22). What was pulled:
- **Yahoo, through Flaim (read-only).** 320 `get_roster` calls for league 466.l.17544, season 2025:
  - 44 week-start rosters, from 00:38Z;
  - 28 daily rosters, from 00:51Z;
  - 248 daily rosters for stage 1 of D-GP-1 (§5), 01:17–01:29Z.

  Two calls hit Yahoo's "token refresh in progress" error and succeeded on retry. Each response is pinned under `gp-reconstruction-2026-10-22/rosters/` and `daily/`, with sha256 in `rosters/manifest.json`, `daily/manifest.json` (the diagnosis's 28) and `daily/manifest_all.json` (all 276 later days).
- **Basketball-Reference.** 90 regular-season game-log pages, 3.5 s apart, with no failures: 68 for the test, then 22 for players who appear only on the stage-1 daily rosters. The other 163 players reuse #159's logs. Raw pages stay outside the repo; their sha256 is in `logs_manifest.json`.
- **One web search** for Yahoo's definition of its games counter. Yahoo's help page itself was unreachable (`getaddrinfo ENOTFOUND help.yahoo.com`).

No pool row, tag, line or constant changed.

**Your decisions** (2026-10-22, about 00:05Z, clicked):
- **"Build the reconstruction"**, on the question of past seasons' games played.
- **"Test, then weekly (Recommended)"**. The option read: "First rebuild your 22 matchups of 2025-26 (both teams, about 42 weekly snapshots plus a few daily ones) and score against the 44 known figures. If it lands within an error bar I state before the run, do the three older seasons with weekly snapshots and a daily-fill model, about 250 calls per season."

**After the test** (2026-10-22, 01:14Z, clicked):
- **D-GP-1, "Count real games, 2025-26 first (Recommended)".** The option read: "Pull the rest of your 2025-26 matchups' daily rosters (248 calls). Count the games actually behind each week's stats, and keep a week only if all 11 recomputed totals match Yahoo's. Older seasons (about 280 calls each) only on your word after." Done in §5.
- **D-GP-2, "Add a README warning (Recommended)".** Done on deck PR #131.

**Method, stated to you before the run.**
- **Truth.** The 44 `gp` values in the deck's `arena/data/weekly_matchups_2025-26.csv`. Its README says 42 of them were never checked against a screenshot; only week 1's two values were.
- **Roster.** Each team-week used the Yahoo roster on the week's first day, held for the whole week. Anyone in an IL or IL+ slot counted for nothing.
- **Played.** A player played on a day when his Basketball-Reference log has a row for it.
- **Lineup.** Each day, the players who played fill the ten active slots (PG SG G SF PF F C C Util Util) by Yahoo eligibility, as many as fit. This is a perfect daily manager, bench included.
- **The bar.** PASS if, across the 44 team-weeks, the mean absolute error is at most 1.5 games and the mean bias is within ±0.75. Nothing was tuned to the 44 values.
- **If it fails.** Pull daily rosters for the three worst team-weeks (21 calls or fewer), split the error into roster changes and lineup choices, and bring it to you. The older seasons do not run.

**Headline.**
- **Stage 1 of D-GP-1 (§5): the real games behind all 44 team-weeks are counted, and the series stands.**
  - 41 team-weeks reproduce all eleven of Yahoo's recorded totals exactly (ACCEPTED). The other 3 are each off by one in a single total (NEAR, kept and flagged). None is REJECTED, against a stop rule of 9.
  - Yahoo's games counter equals those real games in only 3 of 44 team-weeks. The counter minus the real games runs from −7 to +8.
  - The series is in `player_games_2025-26.csv`. It feeds nothing yet, and the older seasons wait for your word (D-GP-3).
- **The test FAILED.**
  - Mean absolute error is 3.93 games against the 1.5 bar.
  - Mean bias is −3.25 against ±0.75. That is the opposite sign to my prediction: I expected the perfect manager to overcount.
  - Two runs were byte-identical.
  - The older seasons did not run.
- **The week-start roster isn't the main problem.** In 31 of 44 team-weeks, even every game by every active rostered player with no slot limit falls short of Yahoo's figure.
- **The daily rosters reproduce Yahoo's scoring exactly, but not its games figure.**
  - For five team-weeks, the players in active slots each day were summed through the game logs. That reproduces all eleven recorded weekly totals in four of them, and ten of eleven in the fifth (assists 88 against 87).
  - Those totals are makes and attempts for field goals and free throws, threes, points, rebounds, assists, steals, blocks and turnovers.
  - Yet the games behind those totals differ from Yahoo's "Games Played" by −7 to +8.
  - That includes the two week-1 values a screenshot verified: 32 against 33, and 28 against 35.
- **So `gp` in the deck file is not the count of player-games behind the scored totals.** What it does count is unsettled.

## 1. Roster changes: none

This test changed no roster, pool row or tag. The section is kept for the report gate.

**The test, all 44 team-weeks** (`reconstruction_2025-26.json`; `reconstruct.py`, two runs md5 cf6a0640):

| set | team-weeks | mean absolute error (games) | mean bias |
|---|---|---|---|
| all (the verdict) | 44 | 3.93 | −3.25 |
| without week 17 (14 days on one snapshot) | 42 | 3.83 | −3.12 |
| your rows | 19 | 4.63 | −4.42 |
| opponents' rows | 25 | 3.40 | −2.36 |

- **Direction:** 32 rows undercount, 7 overcount and 5 are exact.
- **The slot limit hardly mattered:** a player who played went unseated in 8 rows, at most 5 in any one.
- **Worst rows:**
  - your week 13: 32 against 43;
  - Hegi's week 17: 46 against 55;
  - your weeks 5 and 7: 36 against 44, and 38 against 46;
  - Robert's week 8: 19 against 27.

## 2. Why it missed: daily rosters for five team-weeks

**Which weeks.**
- The plan's failure branch picked the three worst 7-day rows: your week 13, Robert's week 8 and your week 5. That took 18 calls; each week's first day was already pinned.
- Week 1, both teams, was added after the first diagnosis as a settling case: it is the one row pair a screenshot verified. That took 10 more calls, past the plan's 21-call cap. I stated it to you before the run.

`diagnose_daily.py`, two runs md5 2dd562f0; the figures are in `diagnosis_daily.json`:

| week, team | Yahoo games | week-start roster, perfect manager | daily roster, perfect manager | daily lineup: active-slot players who played | active-slot players whose team played | 11 weekly totals match |
|---|---|---|---|---|---|---|
| 13, yours | 43 | 32 | 38 | 38 | 45 | all 11 |
| 8, Robert | 27 | 19 | 19 | 19 | 29 | all 11 |
| 5, yours | 44 | 36 | 40 | 40 | 48 | all 11 |
| 1, yours (screenshot 32) | 32 | 33 | 34 | 33 | 33 | all 11 |
| 1, Kyle (screenshot 28) | 28 | 33 | 35 | 35 | 35 | 10 of 11 (assists 88 vs 87) |

**How to read the columns** (EVIDENCE, `diagnosis_daily.json`):
- **Roster change in the week.** The fourth column minus the third: +6, 0, +4, +1 and +2.
- **Lineup choice.** The fifth column minus the fourth: 0, 0, 0, −1 and 0. The managers' actual daily lineups seated almost exactly the players a perfect manager would.
- **The rest.** Yahoo's figure minus the fifth column: +5, +8, +4, −1 and −7. Neither roster nor lineup explains this.
- **The sixth column** counts players in an active slot whose NBA team played, whether or not they played. It brackets Yahoo's figure in the first three weeks, but sits above it in both week-1 rows. So neither simple definition fits.
- **Robert's week 8 is the cleanest case.** The same 15 names sit on his roster all seven days, and no bench player played. His whole active roster played 19 games, which reproduce every weekly total Yahoo recorded. Yahoo's figure is 27.

**Checks that rule out my own errors** (EVIDENCE):
- **Game logs:** each player's count of game rows equals his 2025-26 games played in both pinned per-game files, Basketball-Reference and ESPN, for 225 of 225 resolved players.
- **Team match:** all 44 truth rows name the team I pulled (team name and manager).
- **Snapshot dates:** pairing each day with the roster from the day before collapses the counts to 19, 9 and 19, and the day after to 21, 9 and 22, against 38, 19 and 40 on the same day. The snapshots are dated correctly.
- **Short appearances:** across weeks 1 and 8, one active-slot game ran under 10 minutes (Anthony Edwards, 3:08, 5 points, 10/26). No zero-stat cameo explains the gaps.

**What Yahoo's games figure counts** (ATTEMPTED-FAILED):
- Yahoo's help page was unreachable (`getaddrinfo ENOTFOUND help.yahoo.com`).
- A search summary attributes to that page (SLN6784) the rule that a player counts as "played" with one second of playing time, for position-usage limits.
- That rule would make Yahoo's figure equal the fifth column, which it does not. I can't quote the page, so the counter's definition stays unsettled.

## 3. What this means

- **The method can't rebuild Yahoo's games figure.** Rosters plus game logs reproduce exactly what Yahoo scored, but the number shown as "Games Played" doesn't equal the player-games behind that scoring, in either direction.
- **The older seasons did not run.** The test was the condition for them. Neither did the era check (`league_per36.py`), since no multi-season conclusion was drawn.
- **A cleaner quantity is within reach** (INFERENCE from five team-weeks): the player-games actually behind each team-week's totals.
  - Daily rosters plus logs give it, and every team-week can check itself: its eleven recomputed totals must match the totals Yahoo recorded, which Flaim's `get_matchups` returns for past weeks.
  - In this test, 4 of 5 team-weeks matched on all eleven; the fifth was off by one assist.
- **The deck's `gp` column should not feed a fit until its meaning is settled.** It is the declared fit data for the weekly-model refit (the deck's README). The 2026-10-21 z-score assessment also divided by it. Flagged, not changed (see Watchlist and the decision sheet).

## 4. Errors and surprises, stated plainly

- **My prediction had the wrong sign.** I expected the perfect-manager assumption to overcount. The test undercounted, because rosters change during the week (+0 to +6 in the diagnosed weeks) and Yahoo's figure runs higher still.
- **A checker of mine was broken before the data was.**
  - My first game-count cross-check failed 222 of 222 players because it read a column named `g`; the file's column is `gp`. Fixed, it gives 222 of 222 matching.
  - Recorded per adversarial-verify rule 9: a check that fails everything indicts the checker.
- **Three players were missing logs on the first diagnosis run.** Keldon Johnson, Buddy Hield and Tre Mann appear only on daily rosters. Each run stopped by name, `pull_logs.py` added the three pages, and every earlier result was re-checked unchanged (`reconstruction_2025-26.json` md5 the same).
- **The two diagnostic columns were added after the first output.** These are the "active-slot players whose team played" column and the totals check. Both are labelled that way in `diagnose_daily.py`.
- **The week-1 settling case went past the stated cap** of 21 daily calls by 10, stated before the run.
- **Stage 1 needed 22 more game-log pages than the test.** 28 players appear only on the stage-1 daily rosters; 6 were already in #159's logs. `count_games.py` pinned the daily rosters first and stopped by name, as designed, then `pull_logs.py` added the pages. `logs_manifest.json`'s `added_utc` now dates the latest batch (01:34Z); `added` lists all 25 pages added after the first fetch.

## 5. Stage 1: the real games behind all 44 team-weeks (D-GP-1)

**Method, stated to you before the run and restated after a context compaction** (`count_games.py` docstring):
- **Lineup.** Each day, the players in an active slot (not BN, IL or IL+) on that day's Yahoo roster. That is the week-start roster pinned for the test, then one Flaim snapshot for every later day.
- **Player-game.** A Basketball-Reference game-log row for that player on that date.
- **Totals.** The lineup's makes and attempts for field goals and free throws, threes, points, rebounds, assists, steals, blocks and turnovers: 11 numbers. They are checked against Yahoo's own week totals in the pinned Flaim matchups (`data/source/flaim/history/466.l.17544/matchups_weekNN.json`).
- **Status.**
  - ACCEPTED: all 11 exact.
  - NEAR: every total within 2 and at least one off. The count is kept and flagged.
  - REJECTED: anything else. No count is published for that week.
- **Stop rule.** If 9 or more of the 44 are REJECTED, the series is not published and the misses are diagnosed instead.
- **Scope.** 2025-26 only. This is one season, so the era check (`league_per36.py`) does not apply.
- **Prediction, written before scoring:** 34 or more ACCEPTED and 4 or fewer REJECTED, from the diagnosis's 4 of 5.

**Result** (`player_games_2025-26.csv` and `.json`; `count_games.py`, two runs byte-identical, md5 5b241509 and 2ba03933):

| status | team-weeks | what it means |
|---|---|---|
| ACCEPTED | 41 | all 11 totals equal Yahoo's |
| NEAR | 3 | one total off by one; the count is kept and flagged |
| REJECTED | 0 | the stop rule is at 9 |

**The three NEAR team-weeks.** In each, the game logs carry one more than Yahoo recorded:

| week, team | the total | game logs | Yahoo |
|---|---|---|---|
| 1, Kyle | assists | 88 | 87 |
| 3, yours | rebounds | 240 | 239 |
| 16, yours | blocks | 14 | 13 |

All three point the same way, which fits a stat correction made after Yahoo closed the week (INFERENCE; not checked).

**Real games against Yahoo's games counter** (EVIDENCE, the same file):
- Equal in 3 of 44 team-weeks. Yahoo's counter is above the real games in 27 and below them in 14.
- The counter minus the real games runs from −7 to +8. Those are the same extremes as the five diagnosed weeks.
- On average the counter is 0.68 games above, and the mean absolute gap is 2.55 games.
- On your 19 rows the counter runs 2.00 games above the real games, on average. On the opponents' 25 rows it runs 0.32 below.
- So the deck file's `gp` column is not this quantity in 41 of 44 rows. That bears out D-GP-2.

| week | team | days | real games | Yahoo counter | status |
|---|---|---|---|---|---|
| 1 | yours | 6 | 33 | 32 | ACCEPTED |
| 1 | Kyle | 6 | 35 | 28 | NEAR |
| 2 | yours | 7 | 44 | 44 | ACCEPTED |
| 2 | Christian Oblena | 7 | 43 | 46 | ACCEPTED |
| 3 | yours | 7 | 46 | 46 | NEAR |
| 3 | William | 7 | 45 | 42 | ACCEPTED |
| 4 | yours | 7 | 40 | 43 | ACCEPTED |
| 4 | Justin | 7 | 39 | 40 | ACCEPTED |
| 5 | yours | 7 | 40 | 44 | ACCEPTED |
| 5 | Kevin | 7 | 41 | 38 | ACCEPTED |
| 6 | yours | 7 | 42 | 43 | ACCEPTED |
| 6 | Hegi | 7 | 35 | 37 | ACCEPTED |
| 7 | yours | 7 | 41 | 46 | ACCEPTED |
| 7 | Martin | 7 | 44 | 45 | ACCEPTED |
| 8 | yours | 7 | 19 | 21 | ACCEPTED |
| 8 | Robert | 7 | 19 | 27 | ACCEPTED |
| 9 | yours | 7 | 34 | 38 | ACCEPTED |
| 9 | John | 7 | 34 | 29 | ACCEPTED |
| 10 | yours | 7 | 38 | 41 | ACCEPTED |
| 10 | Noah | 7 | 42 | 39 | ACCEPTED |
| 11 | yours | 7 | 44 | 45 | ACCEPTED |
| 11 | JCo | 7 | 46 | 43 | ACCEPTED |
| 12 | yours | 7 | 46 | 48 | ACCEPTED |
| 12 | Kyle | 7 | 47 | 45 | ACCEPTED |
| 13 | yours | 7 | 38 | 43 | ACCEPTED |
| 13 | Christian Oblena | 7 | 46 | 46 | ACCEPTED |
| 14 | yours | 7 | 41 | 43 | ACCEPTED |
| 14 | William | 7 | 43 | 45 | ACCEPTED |
| 15 | yours | 7 | 48 | 46 | ACCEPTED |
| 15 | Justin | 7 | 40 | 44 | ACCEPTED |
| 16 | yours | 7 | 39 | 45 | NEAR |
| 16 | Kevin | 7 | 43 | 45 | ACCEPTED |
| 17 | yours | 14 | 55 | 56 | ACCEPTED |
| 17 | Hegi | 14 | 53 | 55 | ACCEPTED |
| 18 | yours | 7 | 40 | 41 | ACCEPTED |
| 18 | Martin | 7 | 47 | 48 | ACCEPTED |
| 19 | yours | 7 | 46 | 47 | ACCEPTED |
| 19 | JCo | 7 | 48 | 43 | ACCEPTED |
| 19 | Martin | 7 | 48 | 47 | ACCEPTED |
| 19 | Kevin | 7 | 45 | 41 | ACCEPTED |
| 20 | Martin | 7 | 45 | 44 | ACCEPTED |
| 20 | Justin | 7 | 43 | 45 | ACCEPTED |
| 21 | Martin | 7 | 47 | 46 | ACCEPTED |
| 21 | William | 7 | 47 | 49 | ACCEPTED |

**Checks** (EVIDENCE):
- **Rosters.**
  - All 276 later-day rosters were pinned (`daily/manifest_all.json`, md5 eae37158).
  - The 28 that the diagnosis had already pinned came out byte-identical.
  - No team-day was missing, and none was answered twice with different content.
- **Names.** All 254 rostered names resolve to a Basketball-Reference id, except Kyrie Irving, who played no 2025-26 game (receipted). 22 new pages, 0 failures.
- **Known answer.** The five diagnosed team-weeks give the same counts (38, 19, 40, 33, 35). Each is ACCEPTED exactly where the diagnosis found all 11 totals equal. This is now a test in `test_reconstruct.py`: 10 of 10 pass, with the status rule as a second new case.
- **Every counted game is seen by the check.** None of the 1,839 counted player-games has all 11 of its stats at zero, so each one moves at least one total that is checked against Yahoo's. A game counted or dropped by mistake would therefore show as a total off. Added by the verification pass.
- **Reproducible from the repo alone.** `count_games.py --pinned` recomputes the series from the pinned daily files, each sha-checked against `daily/manifest_all.json`, with no session transcript needed. It gives byte-identical outputs. A file altered by one character stops the run by name.
- **Truth file.** Its totals equal Yahoo's pinned totals in 44 of 44 rows.
- **No drift in earlier results.** After the new logs, `reconstruct.py` and `diagnose_daily.py` reproduce their earlier outputs byte for byte (md5 cf6a0640 and 2dd562f0).

**What it is and isn't.**
- It is the count of games behind what Yahoo scored, per team-week. It does not settle what Yahoo's counter counts.
- It covers 44 team-weeks: your 19 matchups plus the champion's 3 playoff rounds, both teams. That is 2 of 6 league matchups per week, the deck file's own limit.
- Nothing reads it yet. No model, deck file, pool row, tag, line or constant changed.

## Watchlist

- **The deck's `weekly_matchups_2025-26.csv` `gp` column.** It equals the player-games behind the recorded totals in only 3 of 44 rows. The counter minus those games runs from −7 to +8 (§5). That includes both screenshot-verified week-1 values. The README already warns that 42 of 44 values are unchecked; this finding is about what the number means, not transcription. The file is unchanged; the README warning is on deck PR #131 (D-GP-2).
- **The z-score assessment's weekly per-game-rate spread.** It reported 1.53–2.46x the equal-player bound. Its method line reads "against the model's implied spread CV / √gp" (`after-report-2026-10-21-zscore-assessment.md` line 96), so it rests on this `gp` column, and part of that spread may come from this. Not re-derived here (did not check).

## Open-item receipts

| item | status | receipt |
|---|---|---|
| past-season games played (your "Build the reconstruction") | **TEST FAILED**; the older seasons did not run | §1–§3 |
| the real games behind 2025-26 (your D-GP-1 "Count real games, 2025-26 first") | **DONE**: 44 of 44 team-weeks counted, 41 ACCEPTED, 3 NEAR, 0 REJECTED; older seasons are your call (D-GP-3) | §5, `player_games_2025-26.csv` |
| the deck's `gp` column (your D-GP-2 "Add a README warning") | **DONE on deck PR #131**, not merged; merging is your call | Watchlist |
| Hunter's tag (D-RR-1) | **OPEN**, on kit PR #161 | `after-report-2026-10-22-risk-rows.md` §4 |

This test touched no pool row. The flagged-name receipts are carried forward from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21 (`after-report-2026-10-21-pickups-file.md` §1). The rest were not re-queried for this test (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this test (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (§1, `roster_drift_2026-10-21.json`) |

## Repeat-name market check

This test did not touch the draft-room deck page, which is still deck `80eecdf` (checked with `git -C ../yahoo-fantasy-basketball log -1`, clean tree, 2026-10-22), page sha256 6a5cefea4921. The GAUNTLET report replayed it on 10/21. Its table stands, carried here verbatim.

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

1. **D-GP-1: past seasons' games. DECIDED 2026-10-22 01:14Z, (b) first stage.** You clicked "Count real games, 2025-26 first (Recommended)". Done in §5.
2. **D-GP-2: the deck's `gp` column. DECIDED 2026-10-22 01:14Z, (a).** You clicked "Add a README warning (Recommended)". The warning is on deck PR #131, not merged.
   - Its last sentence reads "The player-games behind each 2025-26 row are being counted there (D-GP-1)". That count is now done.
   - I can change the sentence to state the result (3 of 44 rows equal) on your word. It is one line on the same PR.
3. **D-GP-3: the older seasons.**
   - **(a) Stop at 2025-26.** 44 verified team-weeks are on file, and nothing reads them yet.
   - **(b) Add 2024-25 next.** About 280 roster calls (the estimate on your D-GP-1 option) for your matchups, both teams, plus game logs. Each team-week is accepted only on its own 11 totals, the same rule. Before any conclusion spans two seasons, the era check (`league_per36.py`) runs.
   - **(c) All three older seasons**, about 840 calls.
   - Not tested: whether Flaim returns dated rosters for seasons before 2025-26 (did not check).
   - *Default if silent: (a). Recommended: (a) until the weekly refit (deck README, R7) is scoped. The refit is the only reader, and it should say how many team-weeks it needs.*

## Bounds

**Out of scope by design.**
- The three older seasons: conditional on the test, which failed, and now on your word (D-GP-3).
- The weekly-model refit itself, and any use of `player_games_2025-26.csv`.
- Re-deriving the z-score assessment's spread figure.
- Any change to the deck file.

**In scope and unverified.**
- **What Yahoo's games figure counts:** ATTEMPTED-FAILED (Yahoo help unreachable; one search summary, not quotable).
- **Why the three NEAR team-weeks are each one high on the game-log side:** a stat correction after Yahoo closed the week is the likely reading. Not checked against a second box-score source (did not check).
- **Whether the totals check would also pass with a perfect manager's lineup:** not run. The series counts the lineup that was actually set, which is what Yahoo scored.

## Provenance

- **Produced by** session `session_01QjgeRdpDaWgSJmGKRG8fTU` on 2026-10-22: the test and diagnosis about 00:38–01:10Z, stage 1 (§5) about 01:17–01:45Z.
- **Branch:** kit `claude/gp-reconstruction-2026-10-22`, from #159's head `5253a09` (it reuses #159's 2025-26 game logs). Deck sibling `80eecdf`.
- **Governors.**
  - plan-gate was loaded for this test, and its full block was emitted before the first file was written.
  - adversarial-verify was loaded before delivery. Its pass added:
    - the second-outlet game-count check (ESPN, 225 of 225);
    - the off-by-one test;
    - the team-name check (44 of 44);
    - the eleven-totals check, which became the main finding;
    - the week-1 settling case.
  - For stage 1 (§5), after a context compaction, both governors were loaded afresh with the Skill tool. plan-gate's full block was emitted before `count_games.py` was written; adversarial-verify ran before this section was delivered. A second compaction fell during that pass; both were loaded again, and the gate re-emitted, before the last report edits and the commit.
- **Re-verify** (from `report/after-reports/gp-reconstruction-2026-10-22/`):
  - `python3 test_reconstruct.py RAW_DIR` (10 known-answer cases)
  - `python3 pull_logs.py RAW_DIR --reparse` (sha-checked)
  - `python3 reconstruct.py`
  - `python3 diagnose_daily.py TRANSCRIPT --since 2026-10-22T00:51:56Z`
  - `python3 count_games.py --pinned` (from the pinned daily rosters; `count_games.py TRANSCRIPT --since 2026-10-22T00:38:15Z` re-extracts them from the session transcript)

## In plain language

You asked whether past seasons' "games played" could be rebuilt from the connectors. I tested it on last season first, where we know the answer for your 22 matchups.

It didn't pass. Using each week's opening roster, my rebuild was off by about four games a week, usually too low, because rosters change during the week.

When I pulled day-by-day rosters for five weeks, something more useful turned up. Those rosters, run through the game logs, reproduce exactly what Yahoo scored: every point, rebound and shot. But the number Yahoo labels "Games Played" doesn't match the games behind those stats. It's off by up to eight either way, even for week 1, where your screenshot confirms Yahoo's number. So that column isn't measuring what we assumed.

I stopped there; the older seasons didn't run. The useful path is to count the games actually behind each week's stats, which checks itself every week. That's your call.

You chose that path, and it worked. I pulled every day's roster for all 22 of your matchups, 248 more snapshots, and counted the games each lineup actually played. In 41 of the 44 team-weeks, those games add up to exactly what Yahoo scored, in all eleven stats. In the other 3, one stat is off by one. So the count can be trusted, week by week.

Yahoo's "Games Played" number matched the real count in just 3 of the 44, and on your weeks it ran about two games high. Nothing uses the new count yet. Going back to older seasons is your call.
