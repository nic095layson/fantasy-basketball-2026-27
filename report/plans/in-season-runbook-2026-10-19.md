# In-season runbook (Council 2026-10-19; owner "proceed")

What runs, what you feed it, and where to look. Everything records and proposes; nothing changes a projection
line, a tag or a roster without your word (RULES.md).

## Every morning, 06:52 Eastern (scheduled task `trig_01YUcivSLv7aWWoSPoFPmhg4`)

A fresh session runs `python3 scripts/morning.py` and pushes the records to branch `season/daily` under a draft
PR "Season: daily records" (never merged by the run). You get a push notification with the summary. The steps,
each a gate (its PASS line or the run stops):

| step | script | writes |
|---|---|---|
| box scores for yesterday | `scripts/box_pull.py --date <yesterday>` | `data/actuals/<date>.json`: ESPN primary, Basketball-Reference reconciled, names resolved or listed as unpooled, receipts |
| season lines | `scripts/season_lines.py --date <today>` | `data/season/projections_season.csv`, `pool_season.csv`, `season_lines_<date>.json` (movers) |
| season board | `scripts/season_board.py --date <today>` | `report/season/board_<date>.md` / `.json` |
| status feed | `scripts/status_feed.py --date <today>` + `--check` | `data/status/status_<date>.json` (Yahoo letters, ESPN feed, receipts) |
| daily brief | `SEASON_POOL=data/season/pool_season.csv scripts/daily_brief.py --date <today>` | `report/briefs/brief_<date>.md` (lineup, waiver pairs with odds, streaming) |

Record of the run: `report/briefs/morning_<date>.json`. Re-run by hand any time: `python3 scripts/morning.py`
(`--no-fetch` reuses the last box-score record; `--date YYYY-MM-DD` for another morning).

## What you feed it

1. **Rosters** (weekly, before your waiver moves, and after any move you make): the text of Yahoo's league
   "Starting Rosters" page. Until the paste parser lands (it is built against your first sample), the input is
   the transcription CSV `data/source/yahoo-starting-rosters-<date>-view.transcribed.csv` (columns
   `fantasy_team,page,slot,player,nba_team,positions,status`) and `python3 scripts/league_intake.py --as-of <date>`,
   which halts on any name it cannot resolve. The brief prints the state's as-of date.
2. **Weekly scoreboard** (after each week closes): copy `data/weeks/TEMPLATE.csv` to `data/weeks/week_<N>.csv`,
   one row per fantasy team with its opponent and the nine category totals (all six matchups), then
   `python3 scripts/scoreboard_intake.py --week <N>`. It halts on any team it cannot resolve, writes
   `data/weeks/week_<N>.json`, appends every team-week to `data/weeks/team_weeks.csv` (the dataset that will
   calibrate the games shock, D-PM-1), and scores the calibration ledger (`report/calibration.md`).
3. **Your lineup choices**: optional. The brief's recommended lineup is the record the week grades.

## The model, in one paragraph

Each player's season line is the preseason line (never edited) blended with the season's regular-season games:
per category, a prior worth k games of the preseason line plus the actual games, k from the measured
year-over-year stability (FG% 26.0, FT% 37.5, 3PM 9.5, PTS 11.7, REB 12.4, AST 11.7, STL 21.7, BLK 14.5, TO 14.0;
`scripts/season_lines.py`, registered in `scripts/redteam/constants_registry.json`). Percentages blend on
attempts. The board, the brief and the weekly preview read the blended pool; the preseason board stays as the
record of the draft.

## When something breaks

`MORNING: FAIL` names the step; its tail is in `report/briefs/morning_<date>.json`. A single-outlet day
(Basketball-Reference missing) is labelled, not fatal. An unresolved name never becomes a guess: it is listed as
unpooled in the box-score record, and the roster intake halts outright.
