# Yahoo through Flaim: real week totals (A), every status letter (B), rosters (C), the real free-agent list (D), and five past seasons — 2026-10-21

Pull window: 2026-10-21 → 2026-10-21. Read-only Yahoo reads through the Flaim connector:
- today's league: 12 current rosters, the week-1 matchup, and 100 available players;
- five past seasons: 32 calls.

No projection line, tag, roster record or engine constant changed. `data/league_state.json` is untouched: today's intake halted (section 1).

**Owner's request** (2026-10-21, verbatim): "Build A, B, C, D. Can you also pull previous season data that you were looking for now?" A–D are the four options offered in the Flaim inventory the same day:
- **A:** Yahoo's real totals for the card's to-date column;
- **B:** every rostered player's Yahoo status letter;
- **C:** rosters from Flaim instead of FantasyBot;
- **D:** Yahoo's real free-agent list in the pickup scan.

"Build" means build. Merging stays the owner's word.

**What was analyzed.** Kit branch `claude/market-data-workorder-mnfi2b` on top of PR #155 (`0710554`).
- Today's Flaim responses are pinned at `data/source/flaim/pull_2026-10-21.json`: 12 rosters, the week-1 matchup, and 100 available players.
- The past seasons are pinned under `data/source/flaim/history/`.
- The kit's own records: box scores, `data/league_state.json` as of 10/20, the season pool, and the schedule.

**Method.** Each choice below was stated before the run that used it.
- **A, to date.**
  - The card's to-date column is Yahoo's own week totals: `get_matchups`, read at the morning pull, so through yesterday's games.
  - The box-score rebuild still runs as a cross-check, and every stat where it differs from Yahoo's figure is listed on the card.
  - The card falls back to the rebuild, and says why, when the pull is missing or unreadable, has no week, or names neither team. A team renamed since the league state was written is found by its roster in the pull.
- **B, status letters.** Every rostered player's letter comes from Yahoo through Flaim and is tiered by `status_feed.TIERS`. A letter the kit does not tier halts the Flaim intake and is never guessed.
- **C, rosters.** Flaim is read first, with every team's real Yahoo slot. FantasyBot is the fallback when the Flaim pull is missing or incomplete. The Flaim matchup and free-agent list are pinned even when its rosters are not used.
- **D, pickup pool.**
  - **What the list is.** Yahoo's available-player list. Flaim returns at most 100, ordered by Yahoo-wide ownership, so pooled players outside that 100 are not scored; the card says how many.
  - **Letters.** A player's letter sets his availability. O and NA are out. A letter the kit does not tier is set aside and named.
  - **Names.** A name the season pool cannot resolve is named as not projected.
  - **Skips.** A player the league state still shows as rostered, or who is on the do-not-draft list or out in the kit pool, is skipped and named.
  - **Fallback.** With no list, the pool is every pooled free agent, as before.
- **History.**
  - All five past seasons: league info and standings.
  - 2025-26 also gets the draft and every week's matchups, weeks 1–21 (Yahoo's `endWeek`).
  - The responses are pinned raw, with no analysis.

**Headline.**
- **A works on the real 10/21 pull.**
  - Yahoo's week-1 totals through 10/20 equal the box-score rebuild on all 11 stats, for both teams, so the card now shows Yahoo's figures with "the box-score rebuild agrees on all 11 stats".
  - The projection is unchanged: **3–6–0** (you win FG%, FT% and TO).
  - Yahoo's own count of games left reads you 32, them 33.
- **D works on the real list.** In an exercise run, 100 listed = 86 scored + 10 out (8 O, 2 NA) + 1 letter the kit does not tier (Isaiah Stewart, "D") + 3 with no season-pool line. 67 pooled free agents outside Yahoo's top 100 go unscored.
- **C and B halt today, on purpose.** Today's Flaim rosters halt the intake on one name, Andre Drummond (rostered on the bench by Podz save the league), who has no pool row. This is the same halt the FantasyBot path would hit. Adding him or carrying him as not counted is decision 3.
- **The morning runner was not changed.** Its prompt can be edited only from inside its own conversation, and the update from here was refused. Until the new prompt is in place, the runner makes no Flaim calls, so A, C and D fall back each morning exactly as before. The new text is ready (decision 2).
- **Five past seasons pinned:** 32 files for 32 calls.

---

## 1. Merges

None. PR #155 stays a draft, now carrying the week card and this build. Merging is your word.

Roster changes Flaim's 10/21 rosters show against the 10/20 league state [SINGLE-SOURCE: Yahoo via Flaim]. These moves are not in `league_state.json`, because today's intake halted:
- Bailey for Sexton at Splash Mountain;
- Missi to John's Cool Team;
- Drummond added at Podz save the league;
- Podziemski moved to IL.

## 2. What was built

- **`scripts/flaim_live.py` (new).** Reads this league's Flaim responses mechanically from the session transcript, as `league_live` does for FantasyBot. Nothing is retyped.
  - **Recognizing responses.** By shape:
    - a roster carries `teamKey` under this league, `snapshot.type == "current"` and `players`; a dated snapshot is never read as today's;
    - a matchup response carries `matchups`;
    - the available-player list carries `freeAgents`.
  - **`check_pull`.** Halts unless all 12 rosters are present and every status letter is one `status_feed.TIERS` knows.
  - **`to_rows`.** Writes the transcription schema `league_intake` reads, with real Yahoo slots for every team.
  - **`side_totals` / `find_sides`.** Read a matchup side's category values into the kit's stat totals.
  - **`--history`.** Pins past seasons' responses, one file per response kind and week.
- **`scripts/league_live.py`.** Flaim first; FantasyBot when the Flaim pull is missing or incomplete; `--source flaim|fantasybot` forces one. Its PASS line names the source. A Flaim pull that is not used for rosters still has its matchup and list pinned for the week card.
- **`scripts/status_feed.py`.** Receipts name the roster source the letters came from: Flaim, FantasyBot, or the owner's upload.
- **`scripts/week_matchup.py`.** A and D as stated in the method. New record fields:
  - `to_date_source`: source, reason, `rebuild_agrees`, `differences`, Yahoo's games left, Yahoo team names;
  - `totals.*.rebuild_to_date`;
  - `pickups.pool`: source, listed, ordering, out, `unknown_status`, `not_projected`, skipped, `kit_pool_not_listed`;
  - each pickup's Yahoo letter.

  New flag: `--yahoo-pull`, defaulting to `data/source/flaim/pull_<date>.json`.
- **`scripts/season_deck.py`, week card.** The to-date source line comes in three forms:
  - Yahoo's scoreboard, with "rebuild agrees on all 11";
  - Yahoo's scoreboard, with each differing stat named;
  - "rebuilt from box scores", with the reason.

  The games line adds "Yahoo's own count of games left". The pickup table shows each add's Yahoo letter. Under the table, the pool line names every player not scored and why.
- **`scripts/morning.py`.** Docstring only; no step changed.
- **Records committed:**
  - `data/source/flaim/pull_2026-10-21.json` and `rosters_2026-10-21.transcribed.csv`;
  - `data/source/flaim/history/` (32 files);
  - evidence beside this report in `report/after-reports/flaim-2026-10-21/`: three week records, plus the runner prompt as it stands and as proposed.

## 3. Evidence

| check | evidence |
|---|---|
| red first | `week_matchup` A/D: 8 of 22 failed before the code (7 new + the CLI test needing `--yahoo-pull`); the rename-by-roster test, then the unreadable-pull test, each failed alone before its fix. Deck card: 4 new tests failed, 5 old passed. `league_live` partial-pin test failed before its fix. |
| kit suite | **302 of 302, twice** (274 on `0710554`; new: `test_flaim_live` 10, `test_week_matchup` +9, `test_league_live` +4, `test_season_deck` +4, `test_status_feed` +1 — counted per file against HEAD) |
| A on the real pull | `week_matchup.py --date 2026-10-21` with the Flaim-built state: `to date from Yahoo (rebuild agrees)`; `to_date_source` = yahoo, differences [], Yahoo games left 32 / 33. With the committed 10/20 state (old team names): Yahoo's totals still found; the opponent was matched by roster (`yahoo_names`). Both runs byte-identical twice. |
| A's figures | 10/20 to date, Yahoo = rebuild: you FG 8/16, FT 1/2, 3PTM 3, PTS 20, REB 5, AST 10, ST 2, BLK 2, TO 5; them FG 26/67, FT 18/24, 9, 79, 37, 15, 7, 9, 10. Final projection unchanged at 3–6–0. |
| D on the real list | the pool exercise (`--date 2026-10-24 --yahoo-pull pull_2026-10-21.json`, scratch): `pickups ran (drop Neemias Queta, 86 free agents scored from the Yahoo list)`; out 10, unknown letter 1 (Isaiah Stewart "D"), not projected 3 (Hugo González, Morez Johnson Jr., Brice Sensabaugh), skipped 0, kit pool not listed 67; byte-identical twice. Its to-date column is the 10/21 pull's, so its ranking means nothing; only the pool mechanics are under test. |
| name resolution | 97 of 100 Yahoo names resolve through `league_intake.resolve` (accents and suffixes, e.g. Nikola Vučević → Nikola Vucevic, Ronald Holland II → Ron Holland) |
| deck, real record | Chromium, real 10/21 record: 0 page errors, 18 faded cells; text has "Yahoo's scoreboard", "rebuild agrees on all 11", "Yahoo's own count of games left"; "rebuilt from box scores" absent. Pool-exercise record: the pool line lists all 14 players it did not score. At 400 px: page 400/400, card 366/366 (no sideways scroll). |
| C on the real pull | 12 teams, real rival slots, Porter's NA read (test on a copy without Drummond's row); the real pull halts naming Drummond and writes nothing (test). Seat mapping PASS for 12 teams (earlier this session). |
| fallbacks | no pull, an unreadable pull, a matchup naming neither team, no list: each falls back and records why (tests) |
| history | 32 calls, 32 files: 2025-26 has 24 (league info, standings, draft of 156 picks, matchups weeks 1–21); the other four seasons have 2 each |
| runner prompt | `update_trigger` refused: "a routine's instructions (its prompt) can be changed only from the conversation or thread the routine posts into … Nothing was changed." |

**Past seasons, as pinned.** The rank column is Yahoo's standings rank, passed through by Flaim. Flaim marks it as not a verified postseason finish, and its `finalRank` and `championshipWon` fields are empty for Yahoo.

| season | league | teams | format | your team | record | playoff seed | Yahoo rank | pinned |
|---|---|---|---|---|---|---|---|---|
| 2025-26 | ANTI ROBBY B2B ROBBY CLUB | 12 | categories | JAMAL AL-QUETA | 103-58-1 | 1 | 6 | league info, standings, draft 156 picks, matchups weeks 1–21 |
| 2024-25 | ANTI ROBBY ROBBY CLUB | 12 | categories | David's Demure Team | 81-79-2 | 8 | 3 | league info, standings |
| 2023-24 | ANTI MARTIN MARTIN CLUB | 12 | categories | LayBron | 94-83-3 | 3 | 7 | league info, standings |
| 2022-23 | Anti Justin Justin League | 12 | categories | WALKER KESSLER RANGER | 80-80-2 | 7 | 3 | league info, standings |
| 2021-22 | Ultimate Fantasy BBall League | 10 | **points** | HUM DIDDLY DAVID | 10-8-0 | 4 | 7 | league info, standings |

The 2021-22 league was a 10-team points league, not 9-category. Any multi-season analysis that leans on it needs the era and format check first (CLAUDE.md).

**Structural bands, carried for the gate.** This report quotes no simulator figure. The standing sweep's bands are carried verbatim:
- TEAM_WEEK_SHOCK is FRAGILE: +2.7 (no shock) / −3.6 (shock doubled).
- weekly_availability is FRAGILE: −2.7 (no in-sim injury discount) / +0.5 (harsher risk tier 0.65) / −1.5 (healthy plays 0.95) / +1.0 (healthy plays 0.80).

## 4. Errors in this build, stated plainly

- **An accidental morning run (18:10Z).**
  - **What happened.** While building the new runner prompt I passed text into Python through an unquoted shell heredoc. The shell executed the backtick-quoted `python3 scripts/morning.py` inside that text, which started a real morning run against the repo.
  - **What it wrote.** I stopped it about two minutes in, once the command hung. By then it had rewritten:
    - box scores, transactions and the status file (fetch timestamps and re-tiered rows);
    - 7 run-ledger rows;
    - two new files (`data/news/matchup_live_2026-10-21.json`, `data/source/fantasybot/outlook_2026-10-21.json`);
    - five season files, with byte-identical content.
  - **What stayed safe.** Its league-live step halted on Drummond, so `data/league_state.json` was not touched. It never reached the brief, the deck, a publish or a push.
  - **Restored.** The four changed tracked files came back from HEAD and the two new files were removed, after each was inspected; `git status` then showed only this build. The Flaim pin it rewrote came from the same transcript responses: its roster rows match the earlier copy exactly (Drummond's row aside), with 12 rosters, week 1 and 100 free agents with the same letters.
  - **The fix.** Scripts carrying prompt text now go through a quoted heredoc, written to a file and then run.
- **The runner prompt could not be applied from here.** The refusal is in the evidence table; decision 2.
- **A gap found in my own C during the build.** As first written, a Flaim pull with too few rosters lost its matchup and free-agent list, so A and D would silently have had no input. Fixed red-first; it is now pinned anyway.

## Watchlist

- **The 2026-10-22 05:53 PT run.**
  - If PR #155 has merged *and* the new prompt is in place, it makes the Flaim calls. The intake will halt on Drummond unless decision 3 is made first.
  - The week card then reads Yahoo's 10/20–10/21 totals, finding the renamed teams by roster.
  - If the prompt is not in place, the run is as today's: FantasyBot rosters, rebuild to date, kit pool.
- **First live pickup scan on Yahoo's list:** the 10/24 morning (Queta finishes after BOS 10/23). This needs the new prompt.
- **Isaiah Stewart's "D".** He is set aside until the letter is tiered (decision 4).

## Open-item receipts

| item | status | receipt |
|---|---|---|
| A: Yahoo's totals as the to-date column, rebuild as cross-check | **BUILT**, this PR; not merged | real 10/21 pull: rebuild agrees 11/11 both teams; tests |
| B: every rostered player's Yahoo letter | **BUILT**; halts on an untiered letter | `check_pull`; receipts name Flaim; tests |
| C: rosters from Flaim, FantasyBot fallback | **BUILT**; halts today on Drummond (decision 3) | pinned-pull tests (halt, and built without his row) |
| D: Yahoo's free-agent list in the pickup scan | **BUILT** | pool exercise 100 = 86 + 10 + 1 + 3; deck pool line |
| runner prompt to make the Flaim calls | **NOT APPLIED** — refused from this session | decision 2; text in `flaim-2026-10-21/runner-prompt-proposed.txt` |
| past seasons | **PINNED**, raw | 32 files under `data/source/flaim/history/` |
| `season_deck.py --out` prints the default path in its PASS line | flagged, not fixed (adjacent) | carried from the week-card report |

The flagged-name receipts are carried forward from the lock report. This build researched no player, so they were not re-queried (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this build (did not check) |

## Repeat-name market check

This build did not change the draft-room deck page, which is still deck `80eecdf` (checked with `git -C ../yahoo-fantasy-basketball log -1`, clean tree, 2026-10-21), page sha256 6a5cefea4921. The GAUNTLET report replayed it today. Its table stands, carried here verbatim.

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

1. **Merge PR #155** (the week card plus this build) before 2026-10-22 12:53Z to have it in tomorrow's run. Merging is your word.
2. **The runner's prompt.** The new text is in `report/after-reports/flaim-2026-10-21/runner-prompt-proposed.txt`. It changes:
   - step 3: Flaim first, with 16 calls (session, league info, 12 rosters, matchups, 100 free agents). FantasyBot's outlook is always called; its 13 roster calls only when Flaim is incomplete or `flaim_live.py` is absent.
   - the "complete" rule;
   - the commit list (adds `data/source/flaim`);
   - two report lines.

   Options:
   - **(a)** Paste it into the runner's own conversation yourself.
   - **(b)** Tell me to send it to the runner session as a message, so it updates its own task.
   - **(c)** Leave it. A, C and D then stay idle every morning, which is today's behavior.

   Whether the runner's session can see Flaim at all is unknown: its task stores no connectors. The prompt's FantasyBot fallback covers that case.
3. **Andre Drummond**, rostered on the bench by Podz save the league, with no pool row. He halts the intake through either source.
   - **(a)** Add a pool line for him. That is a projection-line change, on your word.
   - **(b)** Change the intake to carry unpooled active players as "not counted" instead of halting. That's a build, on your go.
   - **(c)** Leave it. The intake halts and `league_state.json` stays at 10/20 until he is dropped. The week card still finds Yahoo's totals by roster overlap.
4. **Yahoo letters the kit does not tier.** Today one free agent carries "D" (Isaiah Stewart).
   - The kit sets it aside on the card. If a *rostered* player ever carries such a letter, the Flaim intake halts (rule B) and the runner reports it.
   - **(a)** Leave it set aside (shipped).
   - **(b)** Tier "D" on the record. The letter's meaning was not looked up (did not check), so this needs your value.
5. **Pool scope.** Flaim caps the list at 100, and today 67 pooled free agents fall outside it.
   - **(a)** Keep 100 (shipped).
   - **(b)** Add per-position calls (5 × 100) in the runner prompt to widen it.
6. **Carried, still open:**
   - thin margins;
   - playoff weeks 18–20;
   - the pre-week card's flat 3.5 games;
   - the `--out` path line;
   - the 7 risk rows;
   - the calibration date (2026-11-17);
   - the evening routine;
   - the old routine (keep until 10/28).

   The week-card report's decision 2 (compare with Yahoo) is **resolved**: Yahoo's 10/20 totals equal the rebuild, and the card now uses Yahoo's.

## Bounds

**Out of scope by design.**
- Any projection line, tag, roster record or engine constant.
- The draft-room deck.
- Any analysis of the past seasons: they are pinned, not read for conclusions.
- Flaim writes (`refresh_leagues` was not called).

**In scope and unverified.**
- **The new prompt in a live runner: NOT-ATTEMPTED.** It cannot be applied from here (refused); decision 2.
- **Whether the runner's session has the Flaim tools: UNVERIFIABLE from this session.** The task's stored connectors list is empty, and only a run in that session shows it. The prompt falls back to FantasyBot.
- **A1, the pull time.** Assumed: the 05:53 PT pull reflects all of yesterday's games and none of today's. Basis: the 10/20 totals matched the rebuild exactly. A pull taken during today's games would count today twice: once in Yahoo's to-date, once in the projection. The runner's schedule avoids this, but nothing checks it.
- **Yahoo's ranking of the 100 free agents** is Yahoo-wide ownership, not this league's. Players outside it are unscored and counted on the card.
- **The letter "D": NOT-ATTEMPTED.** Its meaning was not looked up; decision 4.
- **Waiver players vs free agents:** Yahoo's list carries no acquisition state (`capabilities.acquisitionState` false), so the card cannot tell them apart.

## Provenance

- **Session:** Claude Code (cloud), 2026-10-21; Flaim connector, read-only.
- **Governors:**
  - plan-gate, reloaded after the compaction, with the remaining plan shown before the next write;
  - adversarial-verify, loaded before delivery.
- **Calls:**
  - today's league: 12 `get_roster`, 1 `get_matchups`, 1 `get_free_agents` (earlier this session);
  - history: 5 `get_league_info`, 5 `get_standings`, 1 `get_draft`, 21 `get_matchups`, from T0 2026-10-21T18:14:57Z;
  - 1 refused `update_trigger`.
- **Re-verify:**
  - `python3 -m unittest discover -s scripts -p 'test_*.py'` (expect 302 OK);
  - `SEASON_POOL=data/season/pool_season.csv python3 scripts/week_matchup.py --date 2026-10-21 --out-dir /tmp/wm` (expect `to date from Yahoo (rebuild agrees)` … `projected 3-6-0`);
  - `python3 scripts/flaim_live.py --history 466.l.17544 --transcript <this session's transcript> --since 2026-10-21T18:14:57Z --out-dir /tmp/h` (expect 24 files);
  - `python3 scripts/league_live.py --as-of 2026-10-21 --out /tmp/s.json --pin-dir /tmp/p --flaim-pin-dir /tmp/p --source flaim --pull data/source/flaim/pull_2026-10-21.json` (expect the HALT naming Drummond).
