# The 10/26 morning failures fixed: Brazile pooled, one unknown pickup no longer freezes the league, a blank week no longer fails the table — 2026-10-26

Window: the kit at `main` `ec6264c` plus this branch; the 10/26 morning record on `season/daily` (`a221c73`: `report/briefs/morning_report_2026-10-26.md`, `morning_2026-10-26.json`, the pinned `data/source/flaim/pull_2026-10-26.json`). No engine constant, injury tag or existing projection line changed; one in-season pool row added by the owner's order.

Pull window: 2026-10-26 → 2026-10-26. Two live reads at 14:42Z: Flaim `get_players("Trevon Brazile")` (Yahoo, league 478.l.36464) and FantasyBot `get_player_value("Trevon Brazile", nba)`, both pinned from this session's transcript.

**The failures (EVIDENCE, the 10/26 run report).** (1) `LEAGUE INTAKE: HALT — 1 name(s) not in the pool; nothing written: Trevon Brazile (Podz save the league, PF, DEN, status -)`; `league_state.json` stayed at 10/25, so the brief, the waiver scan, the title odds and the deck ran on a stale roster (the owner's Champagnie-for-Clowney move and the Kyrie/Kawhi IL swap were invisible, and all three waiver pairs dropped a player already dropped). (2) `LEAGUE TABLE: FAIL — unreadable makes/attempts value '/'`: on day one of a week Yahoo's FGM/A and FTM/A read "/" and the counting cells "", and `league_table` turned `flaim_live`'s `PullError` into a fatal error.

**Owner's decisions (2026-10-26, clicked).** Work item 2: "(a) Partial intake + loud flag". Brazile's line: "FantasyBot's line alone, labelled" — the Drummond precedent blends the kit line with FantasyBot's projection, but Brazile has no kit line (he is in neither `report/projections-2026-27.csv` nor the deck pool) and FantasyBot's projection equals his 2-game season line, so the precedent could not be followed as written; this session stopped and asked, per the owner's instruction.

## 1. Trevon Brazile's pool row (EVIDENCE)

- Sources: `data/source/flaim/players_trevon-brazile_2026-10-26.json` (DEN, PF, rostered by Podz save the league, no status) and `data/source/fantasybot/player_value_trevon-brazile_2026-10-26.json` (projected 10.5 pts, 10.5 reb, 0 ast, 0.5 stl, 1.0 blk, 1.5 3PM, 1.5 TO, 41.2% FG, 66.7% FT, 23.4 min; season 2 games: 7/17 FG, 4/6 FT; expectedGames 63).
- Row (deck schema, `data/pool_additions.csv`): `Trevon Brazile,DEN,PF,0.412,8.5,0.667,3.0,1.5,10.5,10.5,0.0,0.5,1.0,1.5` with the note naming both files, the dates, "one source, a 2-game sample, no kit line, below the 10/14 blend rule's two-line precedent by the owner's order", and "owner 2026-10-26". Shots are his season makes/attempts per game; the points identity holds exactly (2 × 3.5 + 1.5 + 2.0 = 10.5).
- Kit-plane twin (`report/projections-2026-27.csv`, as Drummond has, so `test_every_addition_equals_its_kit_plane_twin` holds and the box puller pools his games): `Trevon Brazile,DEN,PF,63,23.4,0.412,8.5,0.667,3.0,1.5,10.5,10.5,0.0,0.5,1.0,1.5`.
- Simulator: left out the way Drummond is — he is not in the frozen `players_v69.csv` (0 rows), so `co_gm.run_league_sim` drops him and names him in `absent_from_sim` (D-IS-8).

## 2. Option (a): partial intake with a loud flag (EVIDENCE)

- `league_intake.run`: a rostered name the pool lacks is carried as `unpooled` (per team, and in the state's top-level `unpooled` with team, seat, slot, NBA team, status) with no projection line; `LEAGUE INTAKE: WARN — N name(s) not in the pool, carried as unpooled (no line, not simulated): …`; the PASS line counts them.
- `league_live`: the PASS line names them ("; N not in the pool, not simulated: name (team, slot)").
- `daily_brief`: "**Not in the pool, not simulated (N):** …" under the roster line, and `unpooled` in the brief record. `season_deck`: the Today tab leads with a red note naming each one.
- `league_moves` and `transactions` see the carried names, so a pickup is still a move.
- The simulator reads only `players` (`co_gm.rosters`), so it never sees an unpooled name and never invents a line (test).
- **Relation to the Council 2026-10-15 rule:** the IL path is unchanged — a name listed in `data/unpooled_il.json` in an IL slot is still carried as `unpooled_il`. What widens: a name off the pool on any other slot (or an IL slot without a listing) no longer halts the league; it rides as `unpooled`, named in the LEAGUE LIVE line, the brief and the deck every day until a `pool_additions.csv` row lands. The test that asserted the old halt (`test_league_live`, an invented bench name) now asserts the new behaviour; it was rewritten, not removed.

## 3. A week with no stats yet (EVIDENCE)

- `league_table._not_started(side)`: true only when FGM/A and FTM/A read "/" (or "") and every other cell is empty. Such a side carries `totals None`, `not_started True`, Yahoo's score (0-0-9). A week whose every side is blank is recorded `status: not_started` and left out of the cumulative totals and the all-play; if some sides played, the idle ones carry zero totals. `flaim_live._pair` is unchanged, so "12/" and "abc" still fail (test), and `scoreboard_intake` and `week_matchup` keep their strictness.
- The PASS line says "wkN not started (Yahoo shows no stats yet)". The deck's League tab says "week N not started" and its "this week only" view shows "no stats yet" instead of throwing on the missing totals (test).

## 4. Proof (EVIDENCE)

Replay on a scratch copy of `season/daily` at `a221c73` with the run's pinned `pull_2026-10-26.json` (nothing committed there):

| step | before (old code) | after (this branch) |
|---|---|---|
| league live | `LEAGUE INTAKE: HALT — 1 name(s) not in the pool; nothing written:` / `LEAGUE LIVE: HALT — intake refused the pull; league_state.json not touched (last paste stands)` | `LEAGUE INTAKE: PASS — 12 teams, 171 players, 171 of 171 resolved; 0 unpooled; …` / `LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-10-26.json` |
| league table | `LEAGUE TABLE: FAIL — unreadable makes/attempts value '/'` | `LEAGUE TABLE: PASS — 2026-10-26: week 2; wk1 finished (yahoo), wk2 not started (Yahoo shows no stats yet); power #1 Booker T Floppers (0.692), you #5 (0.540)` |

The replayed state sees the owner's roster as Yahoo has it: Julian Champagnie on the bench, Noah Clowney gone, Kyrie Irving on the bench, Kawhi Leonard on IL. Option (a) on the same pull with Brazile's row removed: `LEAGUE INTAKE: WARN — 1 name(s) not in the pool, carried as unpooled (no line, not simulated): Trevon Brazile (Podz save the league, PF, DEN)` then `LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), …; 1 not in the pool, not simulated: Trevon Brazile (Podz save the league, PF)`.

- Red first: the new intake, table, brief and deck tests failed before the code (3 + 2 + 1 + 2), then passed.
- Full suite: 33 files, 488 tests run; the only files not OK are the two pre-existing transcript-dependent ones (`test_league_live` 1, `test_matchup_live` 1; PR #172). `report/run-ledger.jsonl` unchanged across the suite (862 lines).
- `python3 scripts/morning.py --help` still lists `--since`.
- The `--since <now>` form of league live was not used: this session's transcript carries no twelve-roster pull; the owner allowed the pinned 10/26 pull instead.

## 5. Bounds

- **Out of scope by design (flagged, not fixed):** the afternoon run overwriting the morning's `data/news/league_moves_<date>.json`; the morning prompt's commit list lacking `report/league`, `report/form`, `report/calibration*`; anything in the deck repo's engine.
- **Brazile's line is weak by construction:** one source, two games. The season blend (`season_lines`) will weight it as a prior of `PRIOR_GAMES` games while the same two games also arrive as actuals — over-confident, not biased; replaced the day a second source carries him.
- **Assumption A1:** a side with "/" makes/attempts and empty cells means no games yet (seen on 10/26 for all 24 sides); a side with "/" and a non-empty count is treated as malformed and fails.

**Bands.** This change computes no engine figure; the standing sweep's bands (`redteam-2026-10-19/sweep.json`, engine 048efb6) are unchanged:
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

## Watchlist

- **Every LEAGUE LIVE line:** "N not in the pool, not simulated" names the gap; each name is a pool-row decision for the owner.
- **Each Monday:** "wkN not started" in the LEAGUE TABLE line is the day-one case; a FAIL there now means a genuinely malformed cell.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| league live halt on an unpooled pickup (10/26) | **FIXED** on this draft PR (option a + Brazile's row) | §1, §2, §4 |
| league table FAIL on day one of a week | **FIXED** on this draft PR | §3, §4 |
| afternoon run overwrites the morning's league-moves file | **OPEN**, flagged | §5 |
| morning prompt commit list (report/league, report/form, report/calibration*) | **OPEN**, owner's prompt | §5 |
| `test_matchup_live` and `test_league_live` transcript dependence | **OPEN**, flagged (PR #172) | §4 |

This report adds one in-season row to the kit's pool additions (Trevon Brazile, §1) and touches no row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

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
