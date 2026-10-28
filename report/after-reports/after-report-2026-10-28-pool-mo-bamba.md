# Mo Bamba added to the pool on FantasyBot's projection, and this week's card re-run — 2026-10-28

Pull window: 2026-10-28 → 2026-10-28 (no pull for the kit: read-only Flaim get_players and get_roster for teams 3 and 11, and FantasyBot get_player_value, pinned or read this session; the 10-28 records on season/daily at 264d0b6; no market pull).

**Method up front.** Owner 2026-10-28: "Add Mo Bamba to pool and rerun".
- His line was a method decision, offered as options before the build. The owner picked "Pool: FantasyBot; week: both (Recommended)":
  - the pool row is FantasyBot's projection as-is, labelled, following the Brazile precedent of 10-26;
  - this week's card is shown twice: on that line, and on a 29-minute role line (FantasyBot's per-minute rates × 29) while Jaren Jackson Jr. is out.
- The role line is this week's sensitivity only. It is not written to any file the kit reads.

EVIDENCE marks what a run or read showed; INFERENCE marks what is derived.

## 1. The sources (EVIDENCE)

- **Flaim get_players (10-28 18:25Z):** Mo Bamba, UTA C, rostered by Looking Cool Joker! (Christian Oblena), 16% Yahoo-wide. Pinned at `data/source/flaim/players_mo-bamba_2026-10-28.json`.
- **FantasyBot get_player_value (10-28 18:25Z):** projected 3.4 pts, 2.7 reb, 0.5 ast, 0.1 stl, 0.5 blk, 0.3 3PM, 0.5 TO, 62.2% FG, 67.4% FT, 8.6 min; expectedGames 51.6. Pinned at `data/source/fantasybot/player_value_mo-bamba_2026-10-28.json`.
- **His season so far** (`data/actuals`): did not play 10-21, 10-23 or 10-25; on 10-26, 29 min off the bench, 14 pts, 7 reb, 4 blk, 7-8 FG. Jaren Jackson Jr. started the first three games (28–33 min) and played 10 min on 10-26. Yahoo now lists Jackson as O. ESPN's 17:44Z feed lists no Utah injury.

## 2. What was built (EVIDENCE)

- **`data/pool_additions.csv`** gets a Mo Bamba row on FantasyBot's line. FantasyBot gives no attempts, so FGA 2.5 is solved from its points, threes and FG%: 2 × 2.5 × 0.622 + 0.3 = 3.41. Free throws use his season rate (0 FTA).
- **`report/projections-2026-27.csv`** gets the same line as the kit-plane row: games 52 (rounded from expectedGames 51.6) and 8.6 mpg. `test_every_addition_equals_its_kit_plane_twin` holds.
- **Red first:** `test_mo_bamba_is_pooled_on_fantasybots_projection_with_his_sources_pinned` errored on main and passes. Kit suite: 682 tests OK (2 skipped).
- **Season pool rebuilt in scratch** (`season_lines.py --date 2026-10-28` on the 10-28 records): SEASON LINES PASS. 337 rows are unchanged and Mo Bamba is added. His season line blends in his one game: 4.2 pts, 3.0 reb, 0.7 blk, 2.7 FGA at 65.0%.

## 3. This week's card, re-run (EVIDENCE: `week_matchup.py --date 2026-10-28`)

The run uses the 10-28 records with two live rosters: the owner's (Portis added, Haliburton IL) and Looking Cool Joker!'s (Keldon Johnson and Mo Bamba added, Achiuwa dropped). To date is Yahoo's through 10-27, and the rebuild agrees. Bamba has 2 Utah games left.

| | before Bamba was pooled | pool line | 29-minute role line |
|---|---|---|---|
| projected | 6-2-1 | 5-4-0 | 5-4-0 |
| expected categories | 5.54 | 5.42 | 5.14 |
| P(5+ categories) | 0.807 | 0.777 | 0.701 |
| PTS (them; P you win) | 590.6; 0.564 | 599.0; 0.499 | 613.6; 0.390 |
| FG% (them; P) | .483; 0.498 | .485; 0.473 | .488; 0.435 |
| BLK (them; P) | 18.3; 0.984 | 19.7; 0.968 | 21.7; 0.916 |
| REB (them; P) | 183.4; 0.983 | 189.4; 0.966 | 201.6; 0.882 |
| TO (them; P) | 69.5; 0.579 | 70.5; 0.616 | 72.9; 0.699 |

The owner's side is unchanged across the three runs: 599.0 pts, .482 FG%, 30.1 blk, 226.8 reb.

## 4. Bounds

**Out of scope by design.**
- No projection line other than Bamba's, no injury tag, no roster and no engine constant changed.
- The 29-minute role line is written to no file the kit reads.

**In scope and unverified.**
- **Bamba's role** (INFERENCE). His minutes depend on Jaren Jackson Jr.'s absence, and no source gives a timeline: ESPN's feed lists no Utah injury, and Yahoo shows O. The two cards bracket it.
- **The season line rests on one source** and a one-game blend, below the 10-14 blend rule's three-reference floor, on the owner's order.

## 5. Next steps (owner decisions)

1. Merge this PR to carry Bamba's row into the morning run's pool.
2. When Jackson's status is reported, decide whether Bamba's row should change.

## Watchlist

- **Tomorrow's morning brief:** Bamba projected on Looking Cool Joker! (not listed under "Not in the pool").
- **Jaren Jackson Jr.'s status** on ESPN's feed.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| Mo Bamba unpooled on a rival roster | **POOLED** on FantasyBot's line | §1, §2 |
| this week's card with both teams' moves | **RE-RUN**, two lines | §3 |
| Bamba's role while Jackson is out | **OPEN** | §4 |

This report touched no pool row of the frozen snapshot (Bamba is a kit addition, not a snapshot row). The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

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
