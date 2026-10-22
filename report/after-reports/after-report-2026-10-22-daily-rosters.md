# The week card's rebuild reads Yahoo's daily lineups — 2026-10-22

Window: the week-1 box-score records 2026-10-20 and 10-21 and the 10/22 week card, on `season/daily` `e7b69bb`; Yahoo's lineups for both teams on those two days. No projection line, tag, roster or engine constant changed.

Pull window: 2026-10-20 → 2026-10-22. The pull is four Flaim `get_roster` calls with `as_of_date` (your team and MAXEY-MUM OVERDRIVE, 10/20 and 10/21), made in this session at 2026-10-22T14:32:44Z during the opponent-gap assessment and pinned here as `daily-rosters-2026-10-22/lineups_2026-10-20_21.json`. No market pull and no web search.

**Owner's request.** Asked how the week card's cross-check should treat a player dropped after playing (Gui Santos), the owner chose "Read daily rosters (Recommended)", 2026-10-22 ~15:30Z: build it on its own draft PR, with the rebuild reading Yahoo's roster for each day through Flaim, at most 14 extra calls a week.

**What was analyzed.**
- Kit `main` `16d0113` (with #168's name fix), merged forward to `03069b5` (#167); this branch `claude/week-card-daily-rosters`.
- The committed records of `season/daily` `e7b69bb` (the 14:44Z morning run of 10/22).

**Method, stated to the owner before the build.**
- For each past day of the week, the rebuild counts the box lines of the players Yahoo had **in an active slot that day** (not BN, IL or IL+), read from Flaim `get_roster` with `as_of_date`.
- Each day's lineup is pinned once per team. A morning fetches only yesterday's lineup, for you and the opponent: 2 calls a day, 14 a week. Lineups pinned by earlier runs that week are read too, and the latest pin of a day wins. A later run for the same date (the afternoon check) keeps the lineups already pinned in that day's file; for the same team and day its own response wins (stated to the owner before the fix, 2026-10-22).
- A day with no pinned lineup falls back to today's roster and the ten-slot rule, and the card's record names those days (`rebuild_rosters` in `week_matchup_<date>.json`; the Season Deck page does not show it).
- Basis: the 10/20–10/21 reconciliation of the opponent-gap assessment (actual lineups reproduced Yahoo on all 11 stats for both teams). That is two days, not yet a season.
- Red-first: the seven new tests were run on `main`'s code first and all seven failed (4 errors, 3 failures; `daily-rosters-2026-10-22/red_first.txt`). Then the code was written (`green.txt`).

**Headline.**
- **With Yahoo's daily lineups, the 10/22 card's rebuild equals Yahoo on all 11 stats for both teams.** All four team-days read Yahoo's lineup, and no benched player scored.
- **Without them** (today's rule, on `main` with the name fix), the opponent's rebuild differs from Yahoo on 8 stats, exactly Gui Santos's 10/21 line (5-10 FG, 1-2 FT, 1 3PM, 12 PTS, 5 REB, 1 STL): he was dropped this morning after playing.
- **The runner does not fetch the lineups yet.** The two morning calls are proposed text (`daily-rosters-2026-10-22/runner-step-proposed.txt`), not applied. Until they are, every day falls back to today's rule, as before this change.
- **A second run for the same date keeps the lineups already pinned.** The afternoon check runs `league_live.py` for the morning's date and rewrote that day's pull file, which would have erased the morning's lineups: the card would have read only yesterday's, never an earlier day's. Found by the verify pass and fixed on this branch (§2, "The afternoon check").

---

## 1. The change

| File | Change |
|---|---|
| `scripts/flaim_live.py` | `extract_pull` keeps dated `get_roster` responses under `daily`, by team and date (the latest response wins); a dated response is still never read as today's roster. `keep_daily()` carries an earlier pin's lineups into a later pin for the same date. |
| `scripts/league_live.py` | Both places that write the Flaim pin call `keep_daily()`, so a second run for the same date keeps the lineups already pinned; a Flaim pull short of twelve rosters still pins its dated lineups for the card, as it already did its matchup and available-player list. |
| `scripts/week_matchup.py` | `to_date()` counts a day's active Yahoo slots when that day's lineup is given, reading box lines under the lineup's spelling; `week_lineups()` gathers the week's pinned lineups (earlier pulls first, the run's own last); `build()` passes each team's lineups and records each day's source in `rebuild_rosters`; the method text says which rule ran. |
| tests | 12 new: 6 in `test_flaim_live.py` (`Extract`), 4 in `test_week_matchup.py` (`Record`), 2 in `test_league_live.py` (`FlaimFirst`). |

## 2. Evidence (all EVIDENCE: measured on this branch, records named)

**Tests.**
- New tests on `main`'s code: 7 of 7 fail (`red_first.txt`). With the change, all 45 tests in the two files pass (`green.txt`).
- The five tests of the afternoon fix on the code before it (`99b24e9`): 5 of 5 fail, 3 errors (`keep_daily` absent), 1 error (a lineup-only pull pinned nothing) and 1 failure (the second run's pin had lost the first run's lineup: `{}`) (`red_pin_fix.txt`). With the fix, `test_flaim_live.py` 17, `test_league_live.py` 21 and `test_week_matchup.py` 31 all pass (`green_pin_fix.txt`).
- Full suite on the fix: 354 tests, two runs, identical results (`suite_pin_fix.txt`, which names the command). 352 pass, 1 is skipped, and 1 fails: `test_matchup_live.Record.test_todays_transcript_yields_todays_outlook`. Before the fix: 349, the same one failure (`suite.txt`).
- That failure is pre-existing. It fails identically on `main` (the name-fix after-report recorded it on `af625a8`). It reads today's live session transcript and expects a fixed opponent name from an earlier date. It is unrelated to this change and was left untouched.

**The 10/22 card on the `e7b69bb` records** (`daily-rosters-2026-10-22/evidence.py`, two runs, identical `evidence.json`):

| | rebuild vs Yahoo | days on Yahoo's lineup |
|---|---|---|
| without lineups (the run's own pull) | 8 opponent stats differ: FGM 62/67, FGA 153/163, FTM 39/40, FTA 55/57, 3PM 21/22, PTS 184/196, REB 66/71, STL 14/15 | 0 of 4 |
| with the 10/20–10/21 lineups | 0 differ, both sides | 4 of 4 |

**The afternoon check** (found by the verify pass, 2026-10-22 ~15:48Z, while the gates ran on `0d8e1d2`).
- The cause: `league_live.py` writes `data/source/flaim/pull_<date>.json` afresh on every run. The afternoon check (stored at 3:00 PM Pacific, first run 22:04Z today) runs it for the morning's UTC date with a pull that has no dated lineup, so each afternoon would have erased the lineup the morning pinned. The next morning's card reads earlier days from those files: it would have found only yesterday's lineup, and every earlier day would have fallen back to today's roster. The record would have said so (`today` in `rebuild_rosters`), but the build would not have done what you chose.
- The test on real data (`daily-rosters-2026-10-22/afternoon.py`, output `afternoon.txt`): the morning of 10/22 pins the four 10/20–10/21 lineups; the afternoon check runs on the `e7b69bb` run's own pull; the 10/23 card then gathers the week's lineups. Code before the fix: 0 lineups, twice. With the fix: 4 (both teams, 10/20 and 10/21), twice.
- What the fix keeps: only the dated lineups. Today's rosters, the matchup and the available-player list in that file are still the latest run's, as before.

## 3. Bounds

**Out of scope by design:**
- **The runner's stored prompt is not changed.** The proposed step is `runner-step-proposed.txt`; storing it is yours. Until then no morning pins a lineup, and the card behaves as before.
- **The remaining-days projection** still uses today's roster, which is correct for days not yet played.
- `scripts/availability_calibration.py`'s name mismatch (recorded on #168) is unchanged.

**In scope and unverified:**
- **Two days, two teams.** The rule is shown on 10/20–10/21 only. A later day where a benched player scores, or where more than ten play, has not occurred in the records yet; the tests exercise the bench case (`Record.test_a_days_yahoo_lineup_counts_its_active_slots_and_not_its_bench`).
- **Spellings.** A lineup name is matched to its box line by spelling, then by the suffix-free key (#168). A Yahoo spelling that differs from ESPN's in any other way would leave that line uncounted, and it would show as a cross-check difference, not silently.
- **Whether a missed morning is recovered.** A day whose lineup was never pinned stays on the fallback for the rest of the week; the record names it, the Season Deck page does not.

**Bands.** This change quotes no title share and moves none. The title odds in the morning brief carry the standing sweep's bands (`redteam-2026-10-19/sweep.json`, engine 048efb6):
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

## 4. Decisions for the owner

1. **Merge this PR?** It is a draft; gates are run on it before any merge (RULES 7).
2. **Store the runner step?** The two morning calls in `runner-step-proposed.txt`, in the runner's own conversation. Without them the change does nothing on its own.
3. **The afternoon rewrite of the morning's pull file (older than this PR, not changed here).** The afternoon check replaces the morning's matchup and available-player list in `pull_<date>.json`. The week card records that file's sha256, so after 3 PM the recorded hash no longer matches the file on `season/daily`; the morning's bytes stay in git at the morning commit. Options: (a) leave it, the morning commit is the record; (b) have the afternoon check pin under its own name, a separate PR on your word. Recommended: (a); the morning commit keeps the card's inputs exact, and nothing reads that file after 3 PM today.

## Watchlist

- **The first morning after both merge and the runner step is stored:** its record's `rebuild_rosters` should read `yahoo` for yesterday, both teams, and the cross-check should agree with Yahoo unless a game was still in progress at the pull.
- **A day the runner misses** shows as `today` in the record's `rebuild_rosters` for the rest of the week (the page does not show it).
- **The first afternoon check after the merge:** `pull_<date>.json` on `season/daily` should still carry the morning's lineups under `daily`.
- **Monday's two calls fetch Sunday's lineups, which no card reads** (Sunday is never a past day of the current week, and the old week's card is done). 12 of the 14 weekly calls are used.
- **Week 1 ends 10/25**, the first week a whole set of lineups could be pinned.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| the card's today's-roster rule (Santos) | **BUILT on this draft PR**; merging and the runner step are yours | §1, §2 |
| `availability_calibration.py` name mismatch | **OPEN**, recorded on #168 | `after-report-2026-10-22-name-fix.md` §3 |

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
