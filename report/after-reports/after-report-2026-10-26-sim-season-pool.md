# Title odds on the season pool — 2026-10-26

Pull window: 2026-10-26 → 2026-10-26 (no new pull: every input is a file already in the repos — the records branch `season/daily` at 1c24b0d for `data/league_state.json` and `data/season/pool_season.csv`, kit main ee4dd3a for `data/league_schedule.json`, deck main c11b05b for the frozen pool; no web search, no market pull).

**Method up front.** Owner 2026-10-26, from the options card: "Use the season pool (Recommended)" over "add pickups only" and "leave it as is". Two repos: the deck (yahoo-fantasy-basketball, branch `claude/sim-season-pool-2026-10-26`) teaches the season simulator to read a named pool; the kit (this PR) passes it the season pool whenever `SEASON_POOL` is set, which the morning run sets. Every figure below is read from a run made this session; nothing is typed from memory. EVIDENCE marks what a run or file showed; INFERENCE marks what is derived from it.

## 1. What was wrong (EVIDENCE, read this session)

- **The title odds ran on the draft-day lines.** `arena/mocks/league_sim.py:39` (deck c11b05b) loaded `arena/results/players_v69.csv` unconditionally, and `co_gm.run_league_sim` filtered rostered names by that file (`sim_pool_names`).
- **So pickups counted as zero.** Today `absent_from_sim` = `['Trevon Brazile']`: he is in the season pool (`season/daily` `data/season/pool_season.csv`, 337 rows, from `data/pool_additions.csv`) and not in the frozen one (335 rows).
- **And the board and the odds scored different players.** Of the 335 players both pools carry, 286 have a different line in the season pool (script comparison of every shared column). The board, waiver scan and weekly matchup already read the season pool (`morning.py` steps 5–6, `SEASON_POOL`); only the title odds did not.

## 2. What was built (EVIDENCE)

**Deck `league_sim.py --pool <csv>`.** Loads the player lines from the named deck-schema CSV; the record gains `pool: {file, sha256, players}`. Without the flag nothing changes: on seed 11, 300 seasons, the real schedule, the output file is byte-identical to deck main's (`cmp`, this session).

**Kit `co_gm.run_league_sim`.** With `SEASON_POOL` set it passes `--pool <absolute path>` and filters rostered names by that pool; unset, the frozen v69 pool and no `pool` key, as before. `daily_brief.sim_absent_line` no longer calls the pool frozen.

**Tests, red first.** Deck `arena/test_pool.py` (3): a player only in the named pool is simulated and the record names the pool, its sha256 and 336 players; without the flag that player is missing; naming the frozen file gives the same season as no flag. Kit `test_daily_brief.SimulatorPool` (2 new): with a season pool carrying a pickup, `absent_from_sim` is empty and the record names the pool; without one, no `pool` key. Each new behaviour test failed before the code (deck: `AssertionError: ['Test Pickup Zzz']`; kit: the pickup listed as absent). Deck `arena/test_schedule.py` still 6 OK; kit `test_daily_brief` 21 OK.

**A regression of mine from #196, fixed here (EVIDENCE).** `scripts/test_schedule.py::test_owner_plays_the_listed_opponent_every_week` has failed on kit main since the real schedule merged: week 1 is in `played`, the simulator does not draw a played week, so the owner's opponent is honoured 20 × 16 = 320 times, and the test expected 20 × 17 = 340. It fails identically with both repos at main (run this session), so it is not this change. The #196 after-report said "the only failures are the two live-transcript tests PR #195 replaces"; that was wrong — this one was missed. The expectation now subtracts the played weeks (commit 025400f, separate from the feature).

## 3. Headline (EVIDENCE, scratch run, not published)

Today's rosters (`season/daily` `data/league_state.json`, as of 2026-10-26), built from the season pool in both runs as the brief builds them; the real schedule with week 1 played; seeds 2026 and 2027, 10,000 seasons each (the brief's defaults). The only difference between the runs is the pool the simulator reads.

| owner (seat 10) | title % (2026 / 2027) | mean | playoffs % (2026 / 2027) |
|---|---|---|---|
| before — frozen v69 lines | 22.17 / 22.31 | 22.24 | 98.38 / 98.48 |
| after — season pool | 25.46 / 25.19 | 25.33 | 98.40 / 98.58 |
| season pool, Brazile left out | 25.78 / 25.52 | 25.65 | — |

The "before" row equals the #196 report's "after" row to the hundredth, the same configuration run twice (EVIDENCE).

Every seat's mean title share, before → after: 1 13.91 → 12.84 (−1.07), 2 12.30 → 10.52 (−1.79), 3 11.82 → 11.51 (−0.31), 4 1.84 → 4.53 (+2.69), 5 5.57 → 2.98 (−2.59), 6 9.91 → 10.21 (+0.30), 7 2.75 → 3.83 (+1.08), 8 7.23 → 6.13 (−1.10), 9 0.00 → 0.00, 10 22.24 → 25.33 (+3.09), 11 11.79 → 11.62 (−0.17), 12 0.64 → 0.52 (−0.12).

INFERENCE: the owner's +3.1 points comes from the season-blended lines, not from Brazile — with him left out the season pool gives 25.65, with him 25.33, a −0.3 difference no larger than the two-seed spread (0.27). The seeds agree within 0.3 on both sides, so the +3.1 is not sampling noise. Seats 4 (+2.7) and 5 (−2.6) move as much as the owner does.

## 4. Bounds

**Out of scope by design.** No projection line, injury tag, roster or engine constant changed: the diff touches `league_sim.py` (pool path and record key), `co_gm.run_league_sim`, one caveat string and tests. The red-team sweep was not rerun: it measures the engine on the draft-state roster and the frozen pool against its 10k reference (`scripts/redteam/sweep.py`, `POOL`, `REFERENCE`), and none of those inputs changed. The standing attack check is run as a gate below.

**In scope and unverified.**
- The structural bands quoted beside the brief's title odds were measured on the draft configuration (frozen pool, draft roster). Whether the season-pool configuration has the same bands is unmeasured; that needs a season-pool reference run and is the owner's call.
- The brief still prints "lines v69" in its header and `"lines": "v69"` in its record, although the board has read the season pool since 2026-10-19 and the odds now do too. That label was already wrong before this change; it is flagged, not fixed here.
- The weekly preview (`weekly_preview.py`) and the matchup tool were not touched; they already read `SEASON_POOL` through `co_gm.load_pool`.

## 5. Next steps (owner decisions)

1. Merge the deck PR, then the kit PR (the kit's new test needs the deck's `--pool`). The first morning run after both merges prints the season-pool odds.
2. Whether to fix the brief's "lines v69" label (a one-line wording change).
3. Whether to measure the structural bands on the season-pool configuration.

## Watchlist

- **The first morning run after both merges:** the brief's title-odds record should carry `pool` naming `data/season/pool_season.csv` and an empty `absent_from_sim`; the owner's title share should sit near 25% (today's 25.33 mean), not near 22%.
- **The next in-season pickup:** once his `data/pool_additions.csv` row lands in the season pool, he is simulated the same morning.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| pickups left out of the title odds (Brazile today) | **FIXED** (deck `--pool` + kit wiring, this PR) | §2, §3 |
| title odds and board on different lines (286 of 335) | **FIXED** when `SEASON_POOL` is set | §1, §3 |
| `test_schedule` failing since #196 | **FIXED** (025400f) | §2 |
| brief header "lines v69" | **OPEN**, owner decision | §4, §5 |
| structural bands on the season-pool configuration | **OPEN**, owner decision | §4, §5 |

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
