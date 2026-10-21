# Week categories on the Today tab: to date, projected (faded), and a pickup scan — 2026-10-21

Pull window: 2026-10-21 → 2026-10-21 (build only: no roster pull, no market source, no projection line, tag or constant changed. Read-only fetches of ESPN's public scoreboard for 2026-10-20 to 2026-10-25, to check the schedule.)

**Owner's request** (2026-10-21, verbatim): "Can you build a function for the tool? After each morning refresh pull, I'd like the "Today" tab to show a Week 1 Categories against my opponent, updated from the game results the day prior. Then, using the data and projections you have for the games remaining in the matchup this week, show a "faded" color which are the projections you make through the rest of the matchup. Even Better, if, one of my lower valued players on my team - IF they have completed their games for the week, this tool can forecast what free agent player pickups could contribute to me winning the categories I am deficient in to win"

"Build" means build. Merging stays the owner's word.

**What was analyzed.**
- Kit `main` `55f950c`, on branch `claude/market-data-workorder-mnfi2b`.
- The real records on `main`:
  - box scores `data/actuals/2026-10-20.json`;
  - rosters `data/league_state.json` (as of 2026-10-20);
  - statuses `data/status/status_2026-10-21.json`;
  - season lines `data/season/pool_season.csv`;
  - schedule `report/schedule/games-2026-27.csv`.

**Method.** Each choice below was stated to the owner before the first run.
- **M1 Window.** The Yahoo week from the kit calendar. "To date" means box scores from the week's first day through yesterday. "Remaining" means NBA games from today through the week's last day.
- **M2 To date.** A rebuild from box scores, not Yahoo's own figure; no record carries Yahoo's daily lineups.
  - A game counts for every non-IL player on the current roster who played.
  - On a day when more than ten of a team's players played, the ten counted come from the brief's daily lineup rule (positions, then board value).
- **M3 Projection.** Each player's season-pool per-game line × each remaining game × today's availability from the status file (1.0 with no row). The same ten-slot rule applies each day, and IL counts as zero.
- **M4 Percentages.** Total makes ÷ total attempts, actual plus projected.
- **M5 Leader.** The higher final wins; for turnovers, the lower one wins; equal is a tie. These are single estimates with no probability.
- **M6 Drop.**
  - "Finished" means 0 NBA games from today through the week's end.
  - "Lower valued" means a board value (`adj_value`) below the active roster's median.
- **M7 Pickups.**
  - **Pool:** every pooled free agent (not rostered, not out, not on the do-not-draft list), added in place of the finished player from today on.
  - **Ranking:** by projected category wins gained (a tie counts half), then by how much of each losing category's gap he closes.
  - **Flag:** stated at the phase boundary, before the real run. A free agent who sat out his team's latest game in the past 7 days of box scores is flagged, not removed.

**Headline.**
- **Today's card, on the real records:**
  - To date (10/20 only): you 20 PTS, 5 REB, 10 AST; them 79, 37, 15.
  - Projected through 10/25, you win FG% (.493 vs .455), FT% (.833 vs .825, a near tie) and TO (59.5 vs 80.6), and lose the other six: **3–6–0**.
- **Why this is worse than the pre-week card (60.6% to win):** that card gives every player 3.5 games. The real schedule gives the opponent 41 player-games against your 35, and on 10/20 five of their players had played to two of yours.
- **No pickup scan today:** none of your lower-valued players has finished his week. Queta (Boston, 10th of 13 by value) finishes after the 10/23 game, so the scan first runs on the 10/24 morning.
- **Timing:** this reaches the morning runner only once this PR merges, before 2026-10-22 12:53Z for tomorrow's run.

---

## 1. Merges

Nothing was merged, and no roster, projection line, tag or engine constant changed. This PR is open for the owner's word.

## 2. What was built

- **`scripts/week_matchup.py`** (new) writes `report/briefs/week_matchup_<date>.json`. The record holds, for each category:
  - to-date and projected-final totals for both teams;
  - the leader and the margin.

  It also carries games left (scheduled, and started under the ten-slot rule), any missing box-score days, any unpooled active players, and the pickup block. It prints `WEEK MATCHUP: PASS — …`, or FAIL with the reason. It runs in about 0.2 s.
- **Season Deck, Today tab** (`scripts/season_deck.py`). A new first card, "Week N categories", shows nine rows: you to date, your projection, them to date, their projection, and a W/L/T chip.
  - **Faded projections** use their own colour token and italics: #6A7680 light, #838E97 dark, 4.65:1 and 4.81:1 on the card surface.
  - **Status lines:** the projected W–L–T, games left, and in red any missing box-score days or uncounted players.
  - **Pickup section:** either the scan (drop, top five adds, games, starts, categories gained, flips, gaps closed, season value) or "next to finish".
  - **Method note:** how the totals are built.

  The record is an optional input. With no record the card says so in one line. If the record can't be drawn, the card shows the error and the other five tabs still draw. The record is pinned by sha256 in `deck_record_<date>.json`.
- **`scripts/morning.py`.** A new non-fatal step, "week matchup", on the season pool, after the daily brief and before the deck. A failure costs the card, never the deck.

## 3. Evidence

**Red-first** (EVIDENCE):

| what | before the code | after |
|---|---|---|
| `test_week_matchup.py` | 15 of 15 failing against a stub of the functions (14 errors, 1 failure) | 15 of 15 pass |
| deck card tests | 7 failing (4 failures, 3 errors); the unpooled-row test failed alone before its line | 8 of 8 pass |
| morning step test | 1 failure, 1 error | pass |
| kit suite | 250 on `main` `55f950c` | **274 of 274, twice** |

**Hand-computed known answers** (in the tests):
- the window;
- missed games (DNP) and preseason games excluded;
- IL excluded;
- the ten-slot cap on actual and projected days;
- line × games × availability;
- makes projected from attempts;
- percentages pooled across actual and projected;
- turnovers lower-wins, and a tie with no attempts;
- finished and below the median;
- pickup ranking, where a free agent who flips one category beats one who flips one and loses one, and both beat one with no games left.

**Real run, 2026-10-21** (EVIDENCE, `SEASON_POOL=data/season/pool_season.csv python3 scripts/week_matchup.py --date 2026-10-21`):

| cat | you to date | you projected | them to date | them projected | projected |
|---|---|---|---|---|---|
| FG% | .500 | .493 | .388 | .455 | W |
| FT% | .500 | .833 | .750 | .825 | W |
| 3PTM | 3 | 62.6 | 9 | 73.6 | L |
| PTS | 20 | 572.7 | 79 | 696.2 | L |
| REB | 5 | 180.7 | 37 | 223.8 | L |
| AST | 10 | 131.0 | 15 | 160.5 | L |
| ST | 2 | 36.9 | 7 | 43.6 | L |
| BLK | 2 | 25.3 | 9 | 30.5 | L |
| TO | 5 | 59.5 | 10 | 80.6 | W |

- **Independent re-sum of 10/20.** It was computed separately from the raw box-score file and shares no code with the module. It matches all 11 stat totals for both teams:
  - **You (Queta and White):** 8/16 FG, 1/2 FT, 3 3PM, 20 PTS, 5 REB, 10 AST, 2 ST, 2 BLK, 5 TO.
  - **Them (Maxey, Vassell, Jalen Williams, Towns, Embiid):** 26/67, 18/24, 9, 79, 37, 15, 7, 9, 10.
  - No IL player played that day.
- **Projection trace.** Your remaining REB with no cap is 182.5. The ten-slot rule benches PJ Washington once (6.8 REB) on the day 11 of your players play, giving 175.7, and 5 + 175.7 = 180.7. Your games: 32 started of 33 scheduled. Theirs: 36 of 36.
- **The schedule checked against ESPN.** ESPN's scoreboard, fetched 2026-10-21, matches the kit's schedule on all six days of week 1: 43 games, 0 differences. That includes NY @ BOS on 10/23.
  - FantasyBot's 10/20 pull gave White and Queta 1 game left. Its per-player figure isn't a schedule count: on the same team, PJ Washington got 2 and Kyrie Irving 3.
- **The full morning run.** `morning.py --date 2026-10-21 --no-fetch --seasons 200` ran in a throwaway copy of the repo. All 6 steps passed, including "week matchup", and the deck rendered 6 tabs with 0 page errors and the card drawn. Its nine category rows are identical to the standalone run (two runs agree).
- **The deck.** `season_deck.py --date 2026-10-21` passes with and without the record: 6 tabs, 0 page errors.
  - At 400 px wide the category table fits (334 of 334 px, no sideways scroll).
  - The phone and desktop screenshots, in light and dark, were looked at.
- **A pickup dry run** on today's records, dated 10/24:
  - The record names 10/21–10/23 as missing days; their box scores don't exist yet.
  - It drops Queta (10th of 13) and scores 154 free agents.
  - All of the top five flip FT%: the projected FT% gap is under .0005, so almost any good shooter flips it. That is the weak point of single estimates (decision 3).
- **Edge cases.**
  - A preseason date fails loudly (`outside the 2026-27 fantasy calendar`).
  - A playoff week fails loudly (`no opponent for week 19`); `league_schedule.json` lists opponents through week 17 (decision 4).
  - The last day of a week drops the lowest-valued finished player (PJ Washington, 10/25).
  - A Monday shows "no games played yet this week".

## 4. A surprise, and what it was

**The two figures.** The pre-week card (`report/calibration.json`, recorded 2026-10-15 on 10/15 rosters) gives you 60.6% to win the week, with REB at 75% and BLK at 95%. The new card projects 3–6, losing REB by 43 and BLK by 5.

**Diagnosed before building further** (EVIDENCE):
- **The pre-week model's weekly figure** (`arena.team_week_model`) gives every player `g = 3.5 × availability` games. On today's rosters and lines that puts you ahead: REB 253 to 242, BLK 35 to 27.
- **On the real schedule from 10/21:** REB 182.5 to 186.8, BLK 24.3 to 21.5. Adding 10/20's actual totals (REB 5–37, BLK 2–9) gives the losses.
- **FantasyBot's 10/20 pull leans the same way:** 37 games left to play for them, 30 for you.

Nothing was changed in the simulator; decision 5 holds the option.

**The 60.6% is a simulator figure, so it carries the standing sweep's structural bands.** These come from `report/after-reports/redteam-2026-10-19/sweep.json`, engine `80eecdf`. The sweep measured them on title share in points, not on the weekly win figure, which no sweep has measured.
- **TEAM_WEEK_SHOCK is FRAGILE:** +2.7 (no shock) / −3.6 (shock doubled).
- **weekly_availability is FRAGILE:** −2.7 (no in-sim injury discount) / +0.5 (harsher risk tier 0.65) / −1.5 (healthy plays 0.95) / +1.0 (healthy plays 0.80).

The new card's projections are single estimates from the season lines and the schedule. They don't use the simulator, so these bands don't apply to them; their own limit is decision 3.

## Watchlist

- **First live card:** the 2026-10-22 05:53 PT run, if this PR has merged. Its to-date column will cover 10/20–10/21.
- **First live pickup scan:** the 2026-10-24 morning (Queta finishes after BOS 10/23).
- **The card's to-date totals against Yahoo's scoreboard:** not yet compared (decision 2).

## Open-item receipts

| item | status | receipt |
|---|---|---|
| week categories on the Today tab, faded projections, pickup scan | **BUILT**, this PR; not merged | red-first 24 tests; 274/274 twice; real 10/21 run plus an independent re-sum of 10/20; deck 6 tabs, 0 errors |
| `season_deck.py --out` prints the default path in its PASS line | flagged, not fixed (adjacent; my #154 code) | with `--out <dir>` the files land in `<dir>`, but the line reads `report/season/deck_<date>.html`; production runs pass no `--out` |
| 7 risk rows, calibration date, evening routine, old routine | open, the owner's | GAUNTLET report decisions 2, 3, 5, 6 |

The flagged-name receipts are carried forward from the lock report. This build pulled nothing and researched no player, so they were not re-queried (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this build (did not check) |

## Repeat-name market check

This build did not change the draft-room deck page, which is still deck `80eecdf` (checked `git -C ../yahoo-fantasy-basketball log -1`, clean tree, 2026-10-21), page sha256 6a5cefea4921. The GAUNTLET report replayed it today. Its table stands, carried here verbatim.

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

1. **Merge this PR** before 2026-10-22 12:53Z for the card to appear in tomorrow's run. Merging is your word.
2. **A one-time check against Yahoo.** Send a screenshot or paste of Yahoo's week 1 matchup page after a few days, and I'll compare it with the card's to-date column.
   - If they differ, the cause is M2: a manager benched someone who played, or made a roster move mid-week.
   - Options then: **(a)** keep the rebuild and its label; **(b)** add an owner paste of Yahoo's totals as an override.
3. **Thin margins.** A category decided by a hair flips with almost any pickup; on the 10/24 dry run, FT% did.
   - **(a)** Keep single estimates (shipped).
   - **(b)** Add a per-category win probability from the simulator's weekly variance (`team_week_model` already carries it) and rank pickups by expected categories won. That's a build, on your go.
4. **Playoff weeks 18–20.** No opponent is recorded past week 17, so the card will read "no record" in the playoffs.
   - **(a)** Leave it.
   - **(b)** Add the playoff opponent as an input once the bracket is set.
5. **The pre-week card's flat 3.5 games per player** ignores the real schedule. Week 1 is 41 games against 35. Changing the weekly model touches title odds, so it's a separate work order on your go. Flagged, not changed.
6. **Slamdex.** The link didn't resolve from here (`getaddrinfo ENOTFOUND slamdex.com`), and a web search found nothing by that name.
   - If you connect any Yahoo integration that exposes weekly category totals and daily lineups, M2 can switch to Yahoo's real numbers.
   - Connectors are added in claude.ai Settings → Connectors.
7. **Adjacent:** the `--out` path in the deck's PASS line (receipts table). It's a one-line fix, on your word.
8. **Carried, still open:**
   - the 7 risk rows;
   - the calibration check date (2026-11-17);
   - the evening routine (a/b/c);
   - deleting the old routine (keep until 10/28).

## Bounds

**Out of scope by design.**
- Any projection line, tag, roster or engine constant.
- The simulator's weekly model (decision 5).
- The draft-room deck (deck repo).
- Yahoo's daily lineups.

**In scope and unverified.**
- **The card's to-date totals against Yahoo's scoreboard: UNVERIFIABLE in this session.**
  - FantasyBot's stored 10/20 matchup pull has no category totals (its keys: week, teams, left to play, starters, live flags).
  - The kit has no Yahoo access.
  - Decision 2 resolves it. The card labels the column as a rebuild.
- **A live pickup scan on a real finished-player day with complete box scores: UNVERIFIABLE until 2026-10-24,** because those box scores don't exist yet. The known-answer tests and the 10/24 dry run on today's records cover the logic. **Candidate** until the first live run.
- **Free agents' injury status beyond pool tags and the sat-out flag: NOT-ATTEMPTED.**
  - The status file covers rostered players only, and ESPN's injury feed isn't stored in full.
  - Not load-bearing for the build. It is load-bearing for any single add, so check the player before adding.
- **Waiver players vs free agents: UNVERIFIABLE from the kit's records.** The league puts dropped players on 1-day waivers.
- **The render check inside the runner's own container:** as in #154. The 2026-10-22 13:10Z check-in reports it.

## Provenance

- **Session:** Claude Code (cloud), 2026-10-21.
- **Governors:**
  - plan-gate, loaded for this request with its full block shown before the first write;
  - adversarial-verify, loaded before delivery.
- **Re-verify:**
  - `SEASON_POOL=1 python3 -m unittest discover -s scripts -p 'test_*.py'` (expect 274 OK);
  - `SEASON_POOL=data/season/pool_season.csv python3 scripts/week_matchup.py --date 2026-10-21 --out-dir /tmp/wm` (expect `WEEK MATCHUP: PASS … projected 3-6-0; pickups: no finished low-value player`);
  - `python3 scripts/season_deck.py --date 2026-10-21 --out /tmp/deck` (expect `SEASON DECK: PASS … render: 6 tabs, 0 page errors`).
