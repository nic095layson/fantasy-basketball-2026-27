# Yahoo's standings on the League tab, and the power card's actual record — 2026-10-26

Pull window: 2026-10-26 → 2026-10-26 (no new pull: Yahoo's standings come from the get_standings response already pinned today with the schedule, `data/source/flaim/pairings/478.l.36464/standings.json`, used only for the scratch check below; everything else from the records branch `season/daily` at 1c24b0d; no web search, no market pull).

**Method up front.** Owner 2026-10-26, from the options card: "Standings card + fix records (Recommended)" over "standings card only", "fix records only" and "wait a few days". The method choices, stated before the build: M1 the standings come from the latest pull on or before the date that carries them, nothing else; M2 "vs line" is category games, ((W − W') + (L' − L)) / 2, against 9th for the top eight and against 8th for the rest (8 of 12 make the playoffs, `arena.PLAYOFF_TEAMS`); M3 a finished week the kit rebuilt from box scores takes its matchup score from the verified week record `data/weeks/week_N.json`; M4 each team's Yahoo W–L–T is checked against the kit's summed finished-week scores. EVIDENCE marks what a run or file showed; INFERENCE what is derived.

## 1. What was wrong (EVIDENCE)

- **The power card's "actual" and "luck" columns were blank for all twelve teams** on today's League tab (`season/daily` `report/league/league_2026-10-26.json`: `actual: null` in every power row). `league_table.build` took a finished week's score only from a Yahoo block in a pull dated after the week ended. Today's first morning run did pin one (`season/daily` a221c73: `pull_2026-10-26.json` carries matchups for weeks 1 and 2), but the "Morning re-run" at 15:12Z (5f95841, another session) re-pinned the same file with week 2 only, so the League record built after it found no week-1 block, rebuilt the week from box scores, and a rebuild carries no score. INFERENCE: a re-run that re-pins the day's pull can drop the previous week's finals; that overwrite is flagged here, not fixed (§5).
- **The verified score existed and was not read.** `data/weeks/week_1.json` (Monday's scoreboard intake, checked 6 of 6 against the owner's screenshot) carries every team's `yahoo_score`.
- **Yahoo's standings were nowhere on the page.** The daily pin of `get_standings` starts with tomorrow's 05:00 PT run (#199 and the runner prompt).

## 2. What was built (EVIDENCE)

- `league_table.py`: a `standings` block (pull, date, playoff_teams, rows with rank, W–L–T, win %, seed, waiver priority, FAAB, `vs_line`, and a `check` naming any team whose Yahoo record differs from the kit's); a rebuilt week reads `week_N.json` for its score and says so (`score_source`); `--weeks` (default `data/weeks`). A standings name not in the league state, or a week record lacking a rebuilt team's score, halts the build.
- `season_deck.py`: a **Standings** card at the top of the League tab, with a dashed line under 8th, your row marked, the check's verdict under the table, and "No Yahoo standings pinned …" when none is.
- Tests, red first: `test_league_table.Standings` (7; failed 6 errors + 1 failure before the code), `test_season_deck.LeagueTab` (3 new; failed before the card). Full kit suite: every file OK.

## 3. On today's data (EVIDENCE, scratch run, not published)

`league_table.py --date 2026-10-26` on the records branch: week 1 `source: rebuild`, `score_source: week_1.json`; `actual` is filled for all 12 teams and equals each team's `yahoo_score` in `week_1.json` (12 of 12, script check). With today's pinned standings response added to a scratch copy of the day's pull: **Yahoo's W–L–T matches the kit's finished weeks for all 12 teams** (`mismatches: []`). The owner's row: **11th, 3–6–0, win % .333, 1 category game behind 8th** (Giavaris Jamal Javarison-Lamar, 4–5–0), waiver priority 3. The deck built on those records renders with 0 page errors and no page overflow at 420 px (`standings-2026-10-26/standings_phone.png`).

**A correction.** In the assessment before this build I told the owner "you're 7th, 4–5, seed 7, waiver priority 12". That was the row of Looking Cool Joker!, the week-2 opponent, misread as the owner's. The record above is the correct one.

## 4. Bounds

**Out of scope by design.** No projection line, injury tag, roster or engine constant changed. The rebuilt week's category totals still come from box scores (the week record carries percentages, not makes and attempts); only its score now comes from the record.

**In scope and unverified.** The card has not yet run on a real daily pin: the first will be tomorrow's 05:00 PT pull. Until then the published card shows "No Yahoo standings pinned". At phone width the waiver column sits behind the table's own sideways scroll (67 px), as the power card's columns do. Yahoo's tiebreak order among equal records (7th–9th today, all 4–5–0) is taken as Yahoo gives it.

## 5. Next steps (owner decisions)

1. Merge this PR; tomorrow's deck carries the card.
2. Whether a same-day re-run should keep the earlier pull's finished-week blocks instead of replacing the file (today it dropped week 1's finals; the week-record fallback built here covers the League tab, not the other readers of the pull).
3. Whether the waiver column should also show FAAB (the response carries it; every team has 500 today).

## Watchlist

- **Tomorrow's morning report:** `LEAGUE TABLE: PASS … standings pull_2026-10-27.json, Yahoo W-L-T matches the kit's finished weeks for 12 teams`. A "DIFFERS" there is a finding to look at the same day.
- **Next Monday:** week 2's score arrives in a post-week pull (source yahoo); the check then covers two weeks.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| power card actual / luck blank | **FIXED** (week records, M3) | §2, §3 |
| Yahoo standings on the League tab | **FIXED**, first daily pin tomorrow | §2, §4 |
| kit record vs Yahoo W–L–T | **CHECKED, 12 of 12 match** | §3 |
| the brief header "lines v69" | **OPEN**, owner decision (from #201) | — |

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck e0722cf (this change's deck commit), checked today, the same page the 10/22 day report replayed. Its table stands, carried here verbatim from the day report.

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
