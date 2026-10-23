# System audit at the week-1 reset: data, Season tool, runner operations — 2026-10-23

Window: the kit at `main` `46984bb`; today's records on `season/daily` `b74ed6f` (the 10/23 morning run, 12:02–12:07Z); the deck repo at `048efb6` (the kit's pinned engine) and at its newest commit `483482b` (CLAUDE.md only); the runner session's scheduled tasks as stored at 14:14Z. Draft PRs #175 and #176 are read as built-not-live. No projection line, tag, roster, ledger row, engine constant or stored prompt changed.

Pull window: 2026-10-23 → 2026-10-23. No new pull: every replay below reads records already logged (the morning pull at 12:04Z is the newest).

**Owner's request (2026-10-23).** "With Fable now reset for the week, please audit and conduct validation, integrity, and competitive effectiveness of system data, season tool, and this fantasy session / runner operations. Provide detailed and thorough afterreport in plain language of scope audited, features of system and grades."

**Method (stated before the run).** Static checks re-run fresh on `main` (test suite, provenance, derived, red-team registry/attacks/bands, gates verify). Today's run checked at its source of truth (ledger rows against the morning record; the deck's pinned inputs; the built page's bytes inside the live artifact; the week card replayed from the same records). Data read for shape and cross-checked where two records describe the same thing (Yahoo's week totals against the box-score rebuild; the season-line blend recomputed by hand for one player). Competitive effectiveness judged on what the tool can answer for a week-1 owner, because no week result is gradable before 10/25. Grades: A = checked and clean, B = works with a named gap, C = a defect that reaches the owner, D/F = broken.

## 0. Read this first (plain language)

1. **Today's action.** As of the 5 AM pull, **Kevin Durant (HOU @ SAS) and Derrick White (BOS vs NYK) were on your bench with games today, while Christian Braun and Miles Bridges were starting with no game.** The brief's ideal lineup already starts Durant and White; the alert that would have told you (PR #176) is built but not merged, so nothing pushed it to you. The week card corroborates it from the other side: Yahoo's own games-left count for you is 18 against the kit's best-lineup 21, and the difference is exactly Durant's 2 and White's 1 remaining games on the bench. Replay: `system-audit-2026-10-23/lineup_replay_2026-10-23_seasonpool.json`.
2. **The system is sound.** 385 tests run with the one known, pre-existing failure; every derived artifact reproduces byte-for-byte; the live Season Deck is exactly the page the runner built; the 11 morning steps all PASS and are in the ledger; the season-line blend reproduces by hand.
3. **Three things need your decision** (section 7): the red-team attack records go STALE against the deck repo's newest commit even though the engine is unchanged; two hand-run scripts (including the lineup check in #176) silently use the preseason pool unless an environment variable is set; and the runner session is at 615k of its 1M context after two days.
4. **Week 1 outlook from today's card:** projected 3–6–0 against MAXEY-MUM OVERDRIVE, 3.57 expected categories of 9, 16.8% chance of 5+. The pre-week forecast (recorded 10/15) was 60.6% to win; two of its expected wins (REB, BLK) have gone the other way. The best This Week pickup adds +0.29 categories (Keon Ellis for Queta). The season waiver scan finds nothing worth a move (+0.015 categories/week at best).

## 1. Scope audited

| Area | What was checked | Evidence |
|---|---|---|
| A. System data | league state, box scores, status feed, season lines, the Flaim pull, the week card's to-date | file reads, cross-checks, one hand recomputation |
| B. Engines and arithmetic | test suite, provenance, derived artifacts, red-team registry/attacks/bands, gates | fresh runs on `main` |
| C. Season tool (deck) | the built page vs the live artifact, render at 400 and 1200 px, every tab, the rules (no FantasyBot verdict, no trades card) | bytes compared; Chromium |
| D. Runner operations | the two stored prompts vs what ran, the morning and afternoon records, ledger coverage, session health | task records, reports, session metadata |
| E. This session | the open PRs, the gates' deck pin, the pool default in my own build, hygiene | git, replays |
| F. Competitive effectiveness | what the tool answers today and what it cannot yet | the brief, the week card, the calibration record |

## 2. System data — grade **A−**

**League state (EVIDENCE).** `data/league_state.json` as of 2026-10-23, source Flaim (Yahoo): 12 teams, 168 players, 168 of 168 resolved, every team 13–15 players with 3 BN and 0–2 IL, no empty slots, 0 NBA-team disagreements. The one unpooled IL player (Niederhäuser, seat 6) passes under the Council 10/15 rule.

**Box scores (EVIDENCE).** `data/actuals/2026-10-22.json`: 2 games (CLE@PHI, DEN@OKC), both ESPN events final, two outlets (`single_source` false), 55 players, 35 pooled. 10/20 and 10/21 the same shape (84/58 and 301/204).

**Status feed (EVIDENCE).** ESPN injuries fetched 12:04:34Z, ok; 18 rows, each tiered with a dated receipt; `STATUS GATE: PASS` re-run today. Your roster: Anthony Black out (IL). Opponent: Knueppel out (moved to IL this morning, the only league move), Beal out.

**Season lines (EVIDENCE, hand-checked).** `season_lines_2026-10-23.json`: 5 box-score records, 267 players with games, 212 movers at the 0.25 threshold. The largest on your roster, Ty Jerome pts 17.5→19.7, reproduces by hand from the registered prior weight: (17.5 × 11.7 + 45) / (11.7 + 1) = 19.67. He scored 45 on 10/21 in 32 minutes. The blend is doing what it was fit to do; one big game moves a line about 2 points this early, which is the measured prior, not a bug.

**The Flaim pull (EVIDENCE).** `pull_2026-10-23.json`: 12 rosters, the week-1 matchup, the 100-player available list, 12 dated lineups for 10/22, 27 transactions. All present because this is the morning pull; the 3 PM re-pin still overwrites the matchup and free-agent sections until #175 merges (open).

**Week card to-date (EVIDENCE, explained).** The card uses Yahoo's scoreboard. The box-score rebuild differs on 8 opponent stats, and the difference is exactly one line: Gui Santos's 10/21 game (5/10 FG, 1/2 FT, 1 three, 12 pts, 5 reb, 1 stl, 0 ast/tov/blk), who was on MAXEY-MUM's active roster that day and has since been dropped. The rebuild uses a pinned dated lineup where one exists and today's roster otherwise; 10/22 is pinned (the manager log), 10/20–21 are not under `data/`, so the rebuild cannot see him. Your side matches on all 11. The card says which column is Yahoo's. This heals itself from week 2 (every day pinned).

**Gap (INFERENCE from the records).** Three rostered players with games have no projection line, so every projection treats them as zero: Darius Acuff Jr. (your opponent this week; 35 min and 24 FGA on 10/21), Andre Drummond (seat 9, C slot; `absent_from_sim` in the brief), Mikel Brown Jr. (seat 3). The kit-pool build is paused by your own call until after week 3; Acuff is the one that touches this week's card.

## 3. Engines and arithmetic — grade **A−**

| check | result today (EVIDENCE) |
|---|---|
| test suite on `main` 46984bb | 385 run, 1 failure, 1 skipped. The failure is `test_matchup_live.test_todays_transcript_yields_todays_outlook`, transcript-dependent, failing identically since 10/22 (open on PR #172's list) |
| provenance | PASS, all rows sourced (verified 2026-07-13 .. 2026-10-07) |
| derived artifacts | 29 of 29 reproduce byte-for-byte from their pinned inputs |
| red-team constants | PASS, 32 registered = 32 live (declared_band 5, measured 7, settings 7, structural 4, uncalibrated 9) |
| red-team attacks, deck at `048efb6` | PASS, 9 attacks: CURRENT 5, UNFINGERPRINTED 4 |
| red-team attacks, deck at `483482b` (its newest commit) | **FAIL: A-1, A-5, A-7, A-8, A-9 STALE** — "record made on engine 048efb6, live engine is 483482b" (`system-audit-2026-10-23/attacks_on_deck_483482b.txt`) |
| bands | PASS, both FRAGILE bands quoted, engine 048efb6 |
| gates `--verify` on `main` | PASS, inputs unchanged |

**Finding B1 (the STALE attacks).** `git diff --stat 048efb6 483482b` on the deck touches only `CLAUDE.md` (doctrine text); `arena/`, `hoops.py` and `scripts/` are byte-identical, and the draft-deck page is the same sha256 `6a5cefea4921` at both. The attack runner fingerprints on the repo commit, so a documentation commit invalidates five attack records. This is the 10/19 post-mortem's own rule working as written, and it means: every gates PASS I have quoted since 10/22 was measured against the kit's pinned deck checkout at 048efb6; the runner's sibling checkout, pulled `--ff-only` each morning, is at 483482b, and a gates run there fails the attacks check today. The engine the attacks describe has not changed. Decision D1.

## 4. The Season tool — grade **A−**

**Live = built (EVIDENCE).** The runner published version 35 (`1792757235-fcad`). I read the live artifact: 272,677 bytes; the built `deck_2026-10-23.html` (272,131 bytes, sha256 `88dfeed9ac52…`) is found whole inside it. The deck record pins 9 inputs with sha256s, all present; render record 6 tabs, 0 page errors, Chromium 141.

**Render today (EVIDENCE, `deck_400.png`, `deck_1200.png`).** 0 page errors at both widths; no horizontal scroll (scrollWidth = viewport); six tabs. On the Today tab: the pre-week forecast tile (60.6%, "recorded 2026-10-15"), the live tile (3.57 of 9, 5+ of 9 16.8%), the structural-band line with both FRAGILE constants, the Week 1 categories card with Yahoo's to-date column and per-category chances, the This Week pickups table (81 free agents scored; Ellis +0.29, Simons +0.28, Clowney +0.26 for Queta), the Pickup scan ("no finished low-value player"). Rules: "FantasyBot" appears once in rendered text, in the counts card — "Counts from the FantasyBot matchup pull; the win probability is the kit's own record, not FantasyBot's" — no FantasyBot verdict; no "Trades worth proposing" card. The "Worth a look" card (PR #176) is absent, as expected before merge.

**Gap.** The Lineup card shows the brief's ideal daily fill, not Yahoo's actual slots, so today's bench problem (§0.1) is visible only by comparing the card with your Yahoo page. #176 closes this.

## 5. Runner operations — grade **B+**

**The morning run 10/23 (EVIDENCE).** `morning_report_2026-10-23.md` and `morning_2026-10-23.json`: MORNING PASS, 11 steps, each with a ledger row (11 rows dated 10/23, all PASS). T0 12:02:39Z; `--since T0` path; Flaim 12 of 12 rosters one at a time, no YAHOO_AUTH_UNAVAILABLE, no retries; matchups and the 100-player list; manager log 12 of 12 dated lineups and 27 transactions; FantasyBot outlook only (1 call); deck published and byte-verified; pushed `b74ed6f` = `origin/season/daily`; PR #165 open draft. The stored morning prompt's 7 steps match what the report says ran. Manager log: 0 starts lost league-wide on 10/22.

**The afternoon run 10/22 (EVIDENCE).** Three runs that afternoon: 22:05Z halted on parallel Flaim calls (345d735), a manual re-run at 22:12Z passed (5d4fb7c), and the one-shot I scheduled re-ran at 22:15Z (c283a11 chain) with identical tiers. The prompt fix (one at a time, one retry) was applied at 22:10Z and the 22:15Z run obeyed it. The 3 PM task is enabled, next 22:03Z today; the two old fresh-session tasks are disabled.

**Finding D1 (ledger coverage).** The afternoon runs leave **no rows** in `report/run-ledger.jsonl` (0 rows mention them); `league_live.py` and `status_feed.py` append rows only when `morning.py` drives them. The afternoon record is the commit and `afternoon_report_<date>.md` only. Decision D5.

**Finding D2 (context ceiling).** The runner session (`session_01BsJA4w…`, created 10/21 14:45Z) reports 615,287 of 1,000,000 context tokens used after two morning runs, two afternoon runs and the owner's manual prompts. At that rate the session compacts within about two days. The kit's guards for that case exist (`--since T0`, "earlier turns are not inputs", the hooks' post-compaction protocol) but no post-compaction run has been audited. The session metadata reports the usage "after_boundary", a field that may mean one compaction has already happened; the runner's transcript is another session's and cannot be read from here (UNVERIFIABLE), so whether the 10/23 run was already post-compaction is unknown; if it was, its 11-step PASS is the first evidence the guards work. The runner serves on Opus 5.5 (configured Sonnet 5.5, switched by the owner). Decision D3.

**Finding D3 (the lineup alert).** The 3 PM prompt I handed the owner on 10/22 invokes `python3 scripts/lineup_check.py --date <date>` with no `SEASON_POOL`. See E1: as written, that check would run on the preseason pool.

## 6. This session — grade **B**

**Finding E1 (hidden pool default; my own build).** `week_matchup.py` and `lineup_check.py` read the projection pool from `co_gm.py`, which uses `SEASON_POOL` when set and otherwise the preseason v69 pool. `morning.py` sets it; a hand run does not. Replay on today's records (`system-audit-2026-10-23/week_matchup_pool_check.json`): without the variable, projected 3–5–1 and 3.62 expected categories; with it, 3–6–0 and 3.57, byte-identical to the morning record. So the morning card is right, and my 10/22–10/23 replays in `after-report-2026-10-22-lineup-alert.md` ran on the preseason pool. Today's alerts are the same on both pools (two empty-slot moves; `lineup_replay_2026-10-23_v69pool.json` vs `…_seasonpool.json`), but the matchup bar that now decides a both-play swap (owner 10/23) would be computed on the wrong lines by the runner as prompted. The record does name the pool it used ("v69 preseason pool" in `inputs.pool`), which is how this was caught. Decision D2.

**Open PRs.** #175 (pull carry-forward, 1fbf9be) and #176 (lineup alert + FA notice, 5ed4c79): both open drafts, mergeable, gates PASS on their heads, awaiting the owner's word. Whichever merges second needs `main` merged in and gates re-run (both touch `pull-log.md`, `run-ledger.jsonl`, `gates.json`).

**Hygiene.** 23 worktrees under `/home/user`, 1.2 GB; disk 41% used. The ledger has 650 rows, 627 PASS, 23 FAIL; the 23 are my own gates runs on 10/21–22 that failed before a report section was added, recorded honestly. The `ccd_session` MCP server failed to connect this session (no effect on the audit).

## 7. Competitive effectiveness — grade **B**

What the tool answers today, from records: the ideal daily lineup; each category's chance this week against the actual opponent with Yahoo's live totals; which free agent helps this week by how many categories; the season-value waiver scan with its title-odds effect; title odds 25.1% ± 0.6 (two seeds × 10,000) with the structural band quoted beside it. What it cannot yet: no week has finished, so nothing is graded (week 1 ends 10/25; the calibration file holds week 1 at p=0.606 and week 2 at p=0.576, both unscored); the availability calibration is INSUFFICIENT until about 11/17; three rostered players are invisible (§2 gap); the lineup alert is not live (§5). The one thing that would have changed your result this week, Durant and White on the bench today, the tool computed but could not deliver.

## 8. Decisions for the owner

- **D1 (red-team fingerprint).** (a) Fingerprint the attack records on a content hash of the engine files (`arena/`, `hoops.py`, `scripts/`), red-first, so a doc-only deck commit does not stale them — recommended; (b) re-run the five attacks on 483482b (the sweep is 6,000 seasons × 2 seeds, hours); (c) keep the kit's gates pinned to 048efb6 and say so in every report. Until decided, (c) is the state of affairs and this report says so.
- **D2 (pool default).** (a) On #176, make `lineup_check.py` and `week_matchup.py` default to `data/season/pool_season.csv` when it exists and print the pool's name in their PASS line — recommended, one small change plus a test; (b) prompt-only: prefix the runner's line with `SEASON_POOL=data/season/pool_season.csv`; (c) leave as is.
- **D3 (runner context).** (a) Let the session compact and audit the first post-compaction morning run against this report's checklist — recommended; (b) rotate to a fresh persistent runner each Monday; (c) both.
- **D4 (unpooled rostered players).** (a) Hold the kit-pool pause until after week 3 as you set — default; (b) add lines for Acuff, Drummond and Brown Jr. now, red-first, since one is on this week's opponent.
- **D5 (afternoon ledger rows).** (a) Have `league_live.py` and `status_feed.py` append a ledger row when run standalone — small; (b) leave the commit as the record.
- **D6.** The merge word on #175 and #176.

## 9. Bounds

- **Assumption A1 (confirmed):** the live artifact is byte-for-byte today's built page — confirmed (§4).
- **Assumption A2 (confirmed):** the known `test_matchup_live` failure is the only suite failure on `main` — confirmed (§3).
- **Not checked:** the runner's transcript itself (another session; only its metadata and the records it pushed were read); the Yahoo page directly (Flaim's pull is the source); FantasyBot's outlook content beyond the counts the card shows.
- **INFERENCE:** the ~2-day estimate to the runner's context ceiling assumes the last two days' rate continues.
- **Out of scope by design:** changing any constant, line, tag, roster, stored prompt or gate; the deck repo's own test suite.

**Bands.** No figure in this report runs on either FRAGILE constant: the week card and the lineup replays use the day's status with the shared shock left out. The brief's title odds (25.1% ± 0.6) run on both, and the standing sweep's bands (`redteam-2026-10-19/sweep.json`, engine 048efb6) apply to them:
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

## Watchlist

- **The first post-compaction morning run** of the runner: MORNING PASS with 11 ledger rows, Flaim read from that day's calls only.
- **10/26:** week 1's result scores the 10/15 prediction (p=0.606) — the first calibration point.
- **The next gates run on a deck checkout at 483482b** fails the attacks check until D1 is decided.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| red-team attacks STALE on deck 483482b (engine unchanged) | **OPEN**, D1 | §3, `attacks_on_deck_483482b.txt` |
| hand-run pool default (week_matchup, lineup_check, the runner prompt) | **OPEN**, D2 | §6, `week_matchup_pool_check.json` |
| runner session at 615k of 1M context | **OPEN**, D3 | §5 |
| three rostered players without a line (Acuff, Drummond, Brown Jr.) | **OPEN**, D4 (owner's pause) | §2 |
| afternoon runs leave no ledger rows | **OPEN**, D5 | §5 |
| Durant and White benched with games today | **REPORTED** to the owner | §0, replay files |
| afternoon pull overwrote the morning's matchups/free agents | **OPEN** on draft PR #175 | `after-report-2026-10-22-pull-carry.md` |
| lineup alert and Today-tab notice | **OPEN** on draft PR #176 | `after-report-2026-10-22-lineup-alert.md` |
| `test_matchup_live` transcript dependence | **OPEN**, flagged (PR #172) | §3 |

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
