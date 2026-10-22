# Three older seasons' weekly totals from Yahoo (D-GP-3) — 2026-10-22

Pull window: 2026-10-22 → 2026-10-22. The data read covers three past seasons of the league:
- 2024-25, Yahoo league 454.l.115080, weeks 1-21;
- 2023-24, Yahoo league 428.l.39018, weeks 1-23;
- 2022-23, Yahoo league 418.l.131270, weeks 1-21.

What was pulled:
- **Yahoo, through Flaim (read-only).** 68 calls, 02:15:58-02:42:23Z, no errors:
  - `get_league_info` once per season (3 calls);
  - `get_matchups` once per week (21 + 23 + 21 = 65 calls).

  2024-25 week 1 was also read once last night (2026-10-21 23:54Z), as the probe behind yesterday's answer. Today's response is the one pinned.
- Nothing else: no rosters, no game logs, no web search.

No pool row, tag, line or constant changed. Nothing in the engine, the board or the brief reads these files yet.

**Your decision** (2026-10-22, about 02:25Z, clicked):
- **D-GP-3, "Weekly totals only (Recommended)".** The option read: pin the 2024-25, 2023-24 and 2022-23 weekly totals, about 65 Flaim calls, with no daily rosters, on a draft PR. Merging it is yours.

**Method, stated to you before the run** (02:25Z):
- `get_league_info` once each for 2023-24 and 2022-23, then `get_matchups` for every week of the three seasons.
- The raw responses are pinned by the existing path, `scripts/flaim_live.py --history`. It writes to a scratch folder first; the league_info and standings files are compared with the 10/21 pins before anything is copied in.
- Checks: every matchup final; 11 categories; both team ids inside the league's 12; the category score recomputed from the totals equals Yahoo's.
- One check was added after the plan and before any result was read: each team's regular-season record, summed from its matchups, must equal Yahoo's standings file for that season. It is a second instrument for the same totals.

## 1. What is pinned

65 files, one per week, under `data/source/flaim/history/<league>/matchups_weekNN.json`. Each is Flaim's response as returned: sorted keys, nothing retyped.

| Season | Yahoo league | Weeks on file | Matchups | Regular-season weeks | Playoff weeks |
|---|---|---|---|---|---|
| 2024-25 | 454.l.115080 | 21 | 120 | 1-18, six matchups each | 19-21, four matchups each |
| 2023-24 | 428.l.39018 | 23 | 132 | 1-20, six matchups each | 21-23, four matchups each |
| 2022-23 | 418.l.131270 | 21 | 120 | 1-18, six matchups each | 19-21, four matchups each |

Each matchup gives both teams' eleven totals for the week:
- FGM/A, FG%, FTM/A, FT%, 3PTM, PTS, REB, AST, ST, BLK, TO;
- Yahoo's result in each of the nine scored categories, and the week's category score.

The league_info and standings files these seasons already had (pinned 10/21) were re-pinned to scratch and are byte-identical. They were not touched.

## 2. The checks, and what they found

| Check | Result |
|---|---|
| Every week of each season on disk, header names the league and the week, categories scoring | 65 of 65 |
| Every matchup final, no games remaining | 372 of 372 |
| Both teams inside the league's 12, no team twice in a week | 372 of 372 |
| Same 11 categories in Yahoo's order on every side | 744 of 744 sides |
| Each scored category decided again from the totals (FG% and FT% from makes and attempts, TO lower wins) equals Yahoo's result on both sides | 3,348 of 3,348 |
| Displayed FG% and FT% round from the makes and attempts shown | 1,488 of 1,488 |
| Each side's wins-losses-ties equals Yahoo's category score | 744 of 744 |
| Each team's regular-season record, summed from its matchups, equals Yahoo's standings | 36 of 36 teams (12 per season) |

**The checker was tested on a known wrong answer first.** One copy of the files had one turnover total changed by one: 2023-24 week 19, the 61-61 tie between teams 2 and 9. The checker failed that copy with three named lines: the category, and both teams' scores. On the real files it passes. Two runs gave the same record.

Re-verify: `python3 report/after-reports/flaim-history-2026-10-22/verify_history_totals.py`. It reads only the pinned files and writes `verify_record.json` beside itself.

## 3. What this gives, and what it does not

**It gives** every week's eleven totals for both teams in every matchup of three seasons, checked against Yahoo's own verdicts and standings.

**It does not give games played.** Flaim's matchup response has no games counter. The 2025-26 count (D-GP-1, PR #162) needed every team's daily roster plus each player's game log. These seasons have neither on file; that was your choice ("no daily rosters").

**No conclusion rests on these files yet.** Per the project rule, any analysis across these seasons states its seasons and runs the era check (`league_per36.py`) before a conclusion. Nothing here compares seasons, so no era check ran. The window is the three seasons you named, not a file's extent.

## 4. Errors and surprises, stated plainly

- **Playoff ties still name a winner.** Three playoff weeks ended 4-4-1 in categories, yet Yahoo names a winner:
  - 2023-24 week 21, teams 3 and 7;
  - 2023-24 week 23, teams 2 and 4;
  - 2022-23 week 21, teams 4 and 12.

  All three went to the away side. The seven regular-season 4-4-1 weeks all return "tie" (2024-25 weeks 12 and 16; 2023-24 weeks 13, 14 and 16; 2022-23 weeks 1 and 2). The playoff case is presumably Yahoo's tiebreak, whose rule is not in the response. The checks compare category results and scores, never the winner field, so no check depends on it.
- **2023-24 is longer.** It has 23 weeks, 20 of them regular season, against 21 and 18 in the other two. Its standings records sum to 180 category results per team, not 162. Any per-week or per-season comparison has to say so.
- **Team ids are per season.** Team 4 in 2022-23 is not necessarily team 4 in 2024-25, and the owners of 2022-23 teams 9 and 12 show as "--hidden--" (league_info, 10/21). No owner mapping was made.
- **Week 1 of 2024-25 was read twice** (last night's probe and today). The pinning keeps the latest response. The checks pass on it.

## Watchlist

No player is named in this report and no player's line was read, so there is nothing new to watch.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| older seasons' weekly totals (D-GP-3, your "Weekly totals only") | **DONE on this draft PR**: 65 weeks pinned and checked; merging is your call | §1–§2 |
| season variation (D-ZS-3, your "Season variance") | **DONE**: deck #130 and the kit season-variation PR merged on your word | `after-report-2026-10-22-season-cv.md` |
| Hunter's tag (D-RR-1) | **OPEN**: you chose "Remove it"; the route is the open question (the deck's frozen-pool stamp) | `after-report-2026-10-22-risk-rows.md` §4 |

This pull touched no pool row and read no player's line. The flagged-name receipts are carried forward from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21 (`after-report-2026-10-21-pickups-file.md` §1). The rest were not re-queried for this pull (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this change (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (§1, `roster_drift_2026-10-21.json`) |

## Repeat-name market check

No player is ranked, priced or recommended here. This pull did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck 048efb6, the page the GAUNTLET report replayed on 10/21. Its table stands, carried here verbatim.

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

## Decision sheet

| ID | Question | Default if you say nothing | Where |
|---|---|---|---|
| D-GP-3 | Older seasons: decided 10/22 about 02:25Z, "Weekly totals only". Done: 65 weeks pinned and checked (§1-§2), on this draft PR | merge is yours | this report |

## Bounds

**Out of scope by design:**
- daily rosters and games played for these seasons;
- any analysis across seasons;
- any change to a line, tag, constant or the board;
- 2021-22 (league 410.l.129140), a points league.

**In scope and unverified:** none. Every figure above comes from the pinned files through the checker.

**Red-team bands** (the standing sweep record, engine 048efb6; no title share is quoted in this report):
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared shock) / −3.4 (shock doubled).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy plays 0.95) / +0.9 (healthy plays 0.80).

## Provenance

- Raw responses: `data/source/flaim/history/{454.l.115080,428.l.39018,418.l.131270}/matchups_week*.json`, written by `python3 scripts/flaim_live.py --history 454.l.115080 428.l.39018 418.l.131270 --since 2026-10-21T00:00:00Z --out-dir <scratch>` from this session's transcript. Then the 65 matchup files were copied in, after the league_info and standings files were found byte-identical to the 10/21 pins.
- Checker: `report/after-reports/flaim-history-2026-10-22/verify_history_totals.py`; record `verify_record.json`.
- The governors for this run were loaded with the Skill tool at 02:41Z, after a context compaction (plan-gate). Adversarial-verify is loaded before the delivery.

## In plain language

You asked for the weekly scoreboards of the three seasons before last, without the daily lineups. They are now saved: every week, every matchup, both teams' eleven numbers.

I didn't take Yahoo's word for who won. I recomputed every category of every matchup from the raw numbers, 3,348 of them, and every one matched. Then I added up each team's season from those weeks and checked it against Yahoo's final standings: all 36 teams matched. I also planted one wrong number to make sure the checker would catch it, and it did.

What these files can't tell you is how many games each team played, because the weekly scoreboard doesn't include that. Getting it would take the daily lineups, which you chose to skip. Nothing in the tool uses these files yet, and the PR waits for your word.
