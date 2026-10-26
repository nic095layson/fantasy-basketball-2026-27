# Title odds on the league's full real schedule and the weeks already final — 2026-10-26

Pull window: 2026-10-26 → 2026-10-26 (Flaim get_matchups weeks 1–17, get_league_info, get_standings, pulled ~16:50–17:05Z; no web search, no market pull).

**Method up front.** Owner 2026-10-26, from the options card: "Full pairings + results so far". Two repos: the kit (this PR, #196) pins and compiles the inputs; the deck (yahoo-fantasy-basketball PR #133) teaches the season simulator to use them. Every figure below is read from a record or a run made this session; nothing is typed from memory. Dated evidence is marked EVIDENCE; anything derived is marked INFERENCE.

**Owner's decision (2026-10-26, clicked).** "Full pairings + results so far (Recommended)" over "pairings only", "results only" and "assess first".

## 1. What was wrong (EVIDENCE, re-verified this session)

- **Ten of twelve teams played a random schedule.** `arena/mocks/league_sim.py:77-84` (deck 483482b) fixed the owner's seat against `OPP[_w]` and shuffled the other ten every week. `data/league_schedule.json` carried only `owner_opponents` (17 rows from the owner's 2026-10-15 message; `_source.scope`: "the other ten teams' pairings were not supplied").
- **Every simulated season started 0-0.** `record = {i: 0 for i in ids}` at `league_sim.py:75`; Week 1 is final (`data/weeks/week_1.json`, intake 2026-10-26 morning) and nothing read it.
- **Yahoo publishes the pairings.** `get_matchups(week=N)` for N = 3..17 returned six `upcoming` matchups each on 2026-10-26 (EVIDENCE: the pinned responses below).

## 2. What was built (EVIDENCE)

**Inputs, pinned mechanically.** `flaim_live.py --history 478.l.36464 --out-dir data/source/flaim/pairings --since 2026-10-26T14:28:16Z` pinned 19 responses from this session's transcript: `matchups_week01.json` … `matchups_week17.json`, `league_info.json`, `standings.json`. Each week file carries 6 matchups covering team ids 1..12 exactly once (checked by script, all 17 OK; week 1 `final`, week 2 `in_progress`, weeks 3–17 `upcoming`).

**`scripts/league_pairings.py` (new).** Reads the pins, maps Yahoo team ids to draft seats by team name through `data/league_state.json` (12 of 12 names resolve), and writes into `data/league_schedule.json`:
- `pairings`: `{week: [[seatA, seatB] × 6]}` for weeks 1–17;
- `played`: `{week: {seat: [wins, losses, ties]}}` from `data/weeks/week_N.json` (`yahoo_score` per team) — today week 1 only;
- `pairings_source` (files, weeks, seat-map rule) and `owner_opponents_check`.
The owner's 17 listed opponents are checked week for week against Yahoo: **they match exactly** (seats 11, 1, 9, 3, 12, 4, 2, 7, 6, 8, 5, 11, 1, 9, 3, 12, 4). A contradiction raises `PairingsError`; a week whose matchups do not cover every team, or a played week missing a seat, likewise. Nothing else in the schedule file changes (`_source`, `owner_seat`, `regular_season_weeks`, `playoff_weeks`, `owner_opponents` untouched).

**`morning.py`.** A non-fatal `league pairings` step before `daily brief`, so the played block is recompiled every morning from the Monday intake's week records; a failed compile leaves the last schedule file standing.

**Deck `league_sim.py --schedule` (PR #133, 8877468).** With `pairings` present every team plays its listed pairing every week (`honored` counts them); with `played` present those weeks are not drawn — each season starts from the recorded category record, a tie counting half a win (Yahoo's standings rule, `get_standings` percentage), and only the remaining weeks and the playoffs are simulated. Pairings not covering every team once, or a played week not covering every seat, fail before any record is written. Without the keys the file behaves exactly as before; `--verify` is untouched. The record names what ran (`honored`, `weeks_played`, `played_weeks`, `played_rule`, `pairings`).

**Tests, red first.** Kit: `test_league_pairings.py` (5), `test_morning.Pairings` (1), the step-order test updated. Deck: `arena/test_schedule.py` (6: pairings honored and said so; the owner-only file unchanged; a fully played season reproduces the recorded standings exactly — mean = recorded wins, sd 0; one played week counts once; ties count half; an incomplete played week halts with no record). All failed before the code. Deck `test_season_cv` (6) and `test_bracket` (5) still OK. Kit suite: 35 files; the only failures are the two live-transcript tests PR #195 replaces.

**Headline (EVIDENCE, scratch run, not published).** The owner's current roster (league state 2026-10-26, the season pool the brief uses), the new simulator, 10,000 seasons × seeds 2026/2027, before = the old schedule file (owner-only pairings, 0-0 start), after = the new one (all pairings, week 1 played):

| | title % (2026 / 2027) | playoffs % (2026 / 2027) |
|---|---|---|
| before | 23.16 / 22.05 | 99.14 / 99.12 |
| after | 22.17 / 22.31 | 98.38 / 98.48 |

Mean title share 22.6 → 22.2, a move of −0.4 points, inside the two-seed spread of the before run itself (1.1 points) — INFERENCE: the real schedule and the 3-6 Week 1 move the owner's odds little today, because one played week of 17 and a near-uniform pairing draw leave the roster strength as the dominant term. The top three title shares by seat (seed 2026) were 10, 1, 2 before and after.

## 3. Bounds

- **Out of scope by design:** no projection line, injury tag, roster or engine constant changed; the deck's draft engine (`arena.CV`, `--verify`) untouched; nothing published to the live page.
- **In scope and unverified:** the morning runner's path end to end (clone deck main → `league pairings` → brief) runs tomorrow at 5 AM Pacific only if PR #133 is on deck `main` and #196 on kit `main`; until #133 merges the kit's simulator ignores the new keys and the odds are the "before" column.
- **The played block carries totals only.** A played week's per-category wins are not in `week_N.json`'s `yahoo_score`, so the record's `cat_win_pct` covers simulated weeks only; the record says so (`played_rule`).
- **Ties.** Half a win in the record (Yahoo's percentage rule). The simulator's own draws produce no ties (continuous), so this touches played weeks only.
- **Playoff weeks 18–20** are still simulated by the fixed bracket; Yahoo's playoff pairings do not exist yet.
- **Assumption A1 (held):** team names in the pins equal `data/league_state.json` names — 12 of 12 resolved. A renamed team breaks the map and halts (named in the error), never mis-seats.

**Bands.** The standing sweep (`redteam-2026-10-19/sweep.json`, engine 048efb6) runs `league_sim.py` without `--schedule` on the draft state, so its bands are unchanged by this input; they are quoted as they stand:
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).
Once PR #133 is on deck `main` the engine file `league_sim.py` differs from the fingerprint the attack records carry; the red-team rule (an engine change → full pass) calls for the sweep and attacks to rerun on the new commit. Listed in §4, not done.

## 4. Open for the owner

- **Merge PR #133 (deck) then PR #196 (kit)**, in that order: the kit side is inert until the deck has the simulator change.
- **Rerun the standing sweep and attacks on the new deck commit** after #133 merges (6,000 seasons × 2 seeds; the bands should reproduce within sampling error since the sweep does not pass `--schedule`).
- **Merge PR #195** (the two live-transcript tests on fixtures); independent.

## Watchlist

- **Tomorrow's morning report:** a `LEAGUE PAIRINGS: PASS — 17 weeks … 1 week(s) played` line before the brief; the brief's title line should carry the new simulator's `weeks_played` in its record.
- **Next Monday:** after `SCOREBOARD INTAKE` records week 2, `played` should read 2 weeks.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| the other ten teams paired at random | **FIXED** (deck PR #133 + kit PR #196) | §2 |
| every simulated season starting 0-0 | **FIXED** (played weeks from the records) | §2 |
| owner's 10/15 opponent list vs Yahoo | **CHECKED, match** | §2 |
| sweep and attacks on the new engine commit | **OPEN**, after #133 merges | §3, §4 |
| `test_matchup_live` and `test_league_live` transcript dependence | **FIXED** on PR #195 | §2 |

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck 048efb6 and at 483482b, checked today, the same page the 10/22 day report replayed. Its table stands, carried here verbatim from the day report.

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
