# Taking the tool to the next level: what exists, what is missing, what to build — 2026-10-22

Window: the kit at `main` `d2f2f0f`, the morning records of `season/daily` `e7b69bb` (the 14:44Z run of 10/22), the deck at `048efb6`, the 2026-27 NBA schedule file, and three read-only Flaim responses pinned beside this report. Nothing was built; no projection line, tag, roster or engine constant changed.

Pull window: 2026-10-22 → 2026-10-22. The pull is three read-only Flaim calls made at 16:19Z (`get_standings`, `get_transactions` with count 25, `get_matchups` for week 2; the first week-2 call returned `YAHOO_AUTH_UNAVAILABLE`, a token refresh in progress, and the retry returned data), pinned as `next-level-2026-10-22/flaim_samples.json` by `pin.py`. No market pull and no web search.

**Owner's request (2026-10-22, GAUNTLET).** "Research and propose how we can take the tool to the next level — meaningful, competitive winning additions with the data you have and the access you have with the connectors; propose what is missing and what we can build to boost data projections and forecasting." Examples: (1) streamers at the start of each matchup from the opponent's categorical makeup and free agents with more than 2 games that week; (2) the trend of all 11 opponents against yours, a weekly championship-% update, and player rankings on the previous week's cumulative stats; (3) stronger forecasting for this season and for the future Draft Deck. Added mid-run: (4) "the goal, as well, is for what data we acquire this season and feed into the Draft tool to further improve and build out accuracy, integrity, and strength of forecasting"; (5) the priority: "For the Today tab and Free Agents tab — instead of solely relying on zscore gscore, can this tool also analyze what categorical contributions the free agents can provide (plus remaining games for the week) to help win my weekly matchup? Please let me know if this is a logically sound tool to build, and how we would correctly and intellectually go about it."

**What was analyzed.**
- Every in-season script's own description and the code lines cited below (receipts in `next-level-2026-10-22/facts.json`, written by `facts.py`).
- The morning records of `e7b69bb`: the 10/22 brief, the week card, the calibration ledger, `data/weeks/`.
- The red-team constants registry (`scripts/redteam/constants_registry.json`, 32 constants).
- Three Flaim responses (standings, the last 25 league transactions, week 2's matchups).

**Method.** Read-only inventory, then a gap list, then proposals. Every count below is written by `facts.py` from a record (two runs, identical `facts.json`); the worked example in §2 is computed by `worked_example.py` with the kit's own probability function on illustrative inputs (two runs, identical). Each claim is marked EVIDENCE (measured from a named record) or INFERENCE (judgment). Method parameters stated to the owner before use: a "streamer" is a free agent with 3+ games in the Yahoo week (the owner's ">2"); weeks are the schedule file's `yahoo_week`.

**Headline.**
- **The free-agent idea is sound, and it is the right objective for weekly moves.** This league scores each category as its own win (EVIDENCE: `scoringTypeRaw` `"head"` in the pinned week-2 response; Flaim distinguishes `"headone"`, Most Categories). So the value of an add this week is the change in expected categories won — a sum, one term per category, that can be shown category by category. Z and G scores are season measures and do not see the opponent, the score so far, or the remaining schedule. §2.
- **Three forecasting gaps change the numbers you see today** (EVIDENCE, §1): the title odds run on the frozen preseason lines (`co_gm.py:23`), never use results to date (the simulator takes no standings input, `league_sim.py:25-27`), and pair your ten rivals at random; the weekly model assumes 3.5 games a player instead of the real schedule (`arena.py:506`).
- **The league's whole weekly scoreboard is one Flaim call away, and nothing reads it yet.** `get_matchups` returns all six matchups' category totals and the next week's real pairings (EVIDENCE, pinned week 2). The scoreboard intake still waits for a hand-filled CSV (`data/weeks/` holds only the template), so the weekly prediction ledger has never been scored. This one intake feeds the opponent trend, the title-odds update, and most of the Draft Deck calibration (§3, §4).
- **Do not use Yahoo's "games remaining" as a number** (EVIDENCE, §1): across the 12 teams of week 2 it matches active-slot games for the two teams of your own matchup and rostered non-IL games for three others; no one definition fits. The kit should count playable games itself.

---

## 1. What the tool does now, and the gaps (EVIDENCE unless marked)

| Your ask | What exists | The gap |
|---|---|---|
| Streamers vs the opponent's category makeup | The week card's pickup scan ranks Yahoo's available players by projected category wins gained against the opponent (`week_matchup.py` M7). The brief's streaming list ranks by games left and season board value (`co_gm.py:150`), not by the opponent. | The week card uses point estimates with no probabilities (M5, `week_matchup.py:27`) and scans only when one of your players has finished his week (M6, line 28). Nothing runs at the start of the week. |
| The 11 opponents' trend and weekly title % | The house simulator computes every team's title, final and playoff odds each morning (`league_sim.py:125`). | The brief keeps only your team's. The run uses the frozen v69 lines (`co_gm.py:23`, `league_sim.py:33`), takes no results to date (`league_sim.py:25-27`), and pairs the ten other teams at random ("the owner's own 17 opponents only", `data/league_schedule.json`). |
| Player rankings on last week's cumulative stats | The season board blends preseason lines with actuals (`season_board.py`, `season_lines.py`); the Movers tab lists season-line movers. | No last-7 or last-14-day form view, and no comparison of form against the season line. |
| Stronger forecasting | The weekly prediction ledger is append-only and pre-registered: week 1 was recorded 2026-10-15T20:26:51Z (`report/calibration.json`). | Never scored: the scoreboard intake waits for a hand-filled CSV (`scoreboard_intake.py:5`; `data/weeks/` holds only `TEMPLATE.csv`). Neither `weekly_preview` nor `scoreboard_intake` is a morning step (`morning.py`, only `week_matchup.py` at lines 19 and 81), so week 2's prediction is not recorded unless someone runs it. |

**Yahoo's "games remaining" has no single definition** (`facts.json`, `week2_games_check`). Week-2 counts were pinned at 16:19Z and compared with each roster's NBA games that week (morning pull, the schedule file, the kit's team-code map `co_gm.TEAM_CODE`):
- active-slot players' games equal Yahoo's count for the two teams of your own matchup (yours 32, Looking Cool Joker! 29);
- rostered non-IL players' games equal it for three others (Booker T Floppers, John's Cool Team, Thompson Telepathy);
- neither fits all 12.

Your 32 counts only your ten active slots: the three on your bench have 12 more games that week. Rosters can also change between the morning pull and 16:19Z (MAXEY-MUM OVERDRIVE added and dropped at 15:31Z, transaction tr.43 in the pinned feed). The kit should count playable games itself (§2) and never quote Yahoo's field.

**What the schedule says** (EVIDENCE, `facts.json`, `schedule`):
- Week 2 (10/26–11/01): 9 NBA teams play 4 games, 20 play 3, 1 plays 2.
- The playoffs: week 18 (3/01–3/07) has 10 four-game teams and 2 two-game teams; week 19 has 16 four-game teams; week 20 has 15.
- Week 7 (11/30–12/13) and week 17 (2/15–2/28) each span two calendar weeks. Week 17 gives 7 teams 5 games.

## 2. Priority 1 — matchup-aware free-agent analysis (the owner's question)

**Verdict: logically sound, and the correct objective for a weekly add.** (INFERENCE from the league's scoring, which is EVIDENCE.)
- Every category is its own win in the standings, so a week is worth the expected number of categories won: the sum over the nine categories of P(win) plus half P(tie).
- Expected values add whatever the correlations between categories, so the per-category contributions add up exactly to the total. The tool can show each category's share and the shares add up.
- Z and G scores rank season-long value against the player pool. They are blind to three things that decide a week:
  - the score so far;
  - how close each category is;
  - how many games each player has left.

**The arithmetic.**
1. **State.** For each category, the final total = Yahoo's total to date (fixed, already read by the week card) + the projected remaining total (season-pool per-game line × playable games × availability, the week card's M3). Only the remaining games are uncertain. Their variance comes from the measured per-game spread `arena.SEASON_CV` (EVIDENCE: registry status `measured`). For FG% and FT% it is the binomial spread on remaining attempts × `PCT_MIX_INFL`, as in `arena.team_week_model`.
2. **Probability.** P(win c) = Φ(margin / √(variance mine + variance theirs)), the kit's existing `co_gm._pcat` (`co_gm.py:116`); TO is reversed.
3. **Playable games, not team games.** A game counts only if the daily-fill rule (the week card's ten-slot fill) gives the player an active slot that day. Your "3+ games" becomes a display filter, not a hard cutoff: a 2-game player can still be the best add if he flips a close category.
4. **The swap.** For each available player and each drop candidate: add his line for his playable games and remove the dropped player's remaining games. The score is the change in expected categories won, shown per category. Beside it goes the drop's season cost, the brief's existing season-long add/drop scan (`co_gm.waiver_pairs`).
5. **League rules.** The 4 acquisitions per week (`league_settings.json`) are shown as a budget. A player dropped within the last day is flagged as probably on waivers (waiver time 1 day; Flaim's transaction feed shows recent drops), and a claim loses that day's game. A name the projections cannot resolve is named, never guessed (the week card's existing rule).

**Worked example** (`worked_example.txt`; ILLUSTRATIVE made-up numbers, real arithmetic). You lead PTS 560–500 and trail BLK 22–24, with FG% 170/360 to date and 60 attempts left. Two available players, 3 playable games each:

| Add | PTS P(win) | BLK P(win) | FG% P(win) | Expected categories, these three |
|---|---|---|---|---|
| (none) | 0.856 | 0.319 | 0.568 | — |
| S, a scorer (18 pts, 0.3 blk, 15 FGA at 42%) | 0.976 (+0.120) | 0.399 (+0.080) | 0.441 (−0.127) | **+0.073** |
| R, a rim protector (7 pts, 2 blk, 5 FGA at 60%) | 0.923 (+0.068) | 0.761 (+0.442) | 0.671 (+0.103) | **+0.613** |

R is worth +0.540 categories more this week, although S has the bigger counting line. Points is already likely won, blocks is a close loss R can flip, and S's misses cost field-goal percentage. A season ranking cannot see any of that.

**Where it shows.**
- **Today tab:** a "Best adds this week vs <opponent>" panel, with each candidate's per-category bars and his playable games day by day.
- **Free Agents tab:** a "This week" sort beside the z and G columns, which keep their season meaning (`season_deck.py:473` sorts by z today).

**Validation (red-first, then calibrated).**
- Known-answer tests written first, each failing on today's code:
  - a tied category is 0.5;
  - a player whose games all fall on full-lineup days adds 0;
  - a high-volume, low-percentage shooter lowers FG%;
  - more games raise TO;
  - the per-category changes sum to the total.
- **The formula against simulation:** on the same inputs, the house simulator's weekly draw must agree within its own error.
- **Calibration:** each morning's P(win) per category is recorded before the games, append-only like `calibration.json`, and scored at the week's end (Brier score and a reliability table). After 4 to 6 weeks this says whether the stated uncertainty is right.

**Bounds.**
- In the playoffs (weeks 18–20) the stake is the matchup itself. That Yahoo decides a playoff matchup by categories won is INFERENCE: the settings carry a "higher seed wins" tiebreak, but this was not verified. If so, correlations between categories matter, and the simulator's draw (with its games shock) should replace the sum there.
- The opponent's own adds cannot be known in advance. The tool can show sensitivity to them but not predict them.

**Options.** (a) Upgrade the week card's pickup scan and add the "This week" view to Free Agents, on its own draft PR, red-first (recommended); (b) probabilities only on the week card, with M6 loosened, and no Free Agents change; (c) defer.

## 3. Proposals for winning this season (ranked; effort is INFERENCE)

| # | Proposal | Data (verified to exist) | Effort | Why it wins |
|---|---|---|---|---|
| P1 | Matchup-aware free agents (§2) | week card inputs, Yahoo list, `SEASON_CV`, `_pcat` | M | Every weekly add judged on the categories it can actually swing |
| P2 | **Weekly league intake from Flaim**: each Monday, last week's six matchups (all 12 teams' category totals) into `data/weeks/team_weeks.csv` and the ledger score; the next week's real pairings; the standings with each team's FAB balance (500 each today) | `get_matchups(week)`, `get_standings` (pinned) | S–M | Replaces the never-filled CSV; scores the prediction ledger; the foundation for P3, P5 and §4 |
| P3 | **Title odds that move**: the simulator on the blended season lines, starting from the real standings, with the real pairings for all 12 teams; all 12 teams' odds stored each morning as a trend line | P2's records, `season_lines` pool, the simulator's existing 12-team output | M (deck + kit) | Your ask (2): the 11-opponent trend and a weekly title % that reflects what has happened |
| P4 | **Monday week plan**: P1 run at the start of each week with the 3+ games filter and the 4-add budget, day by day | P1 + schedule | S on top of P1 | Your ask (1): streamers chosen against this opponent's category profile |
| P5 | **Form board**: each player's last-7 and last-14-day z (and G) on actual box scores, beside the season line, with a rostered/free flag | `data/actuals` (morning box pull) | S | Your ask (2), player rankings on recent stats, shown beside the season line, never replacing it (small samples) |
| P6 | **Playoff-schedule view**: games in weeks 18–20 for your roster and for free agents, ahead of the league's last day for deals (2027-03-04, `league_settings.json`) | schedule file | S | Weeks 18–20 range from 2 to 4 games per NBA team (§1) |
| P7 | **League activity record**: pin the transaction feed daily (Flaim returns a rolling 30 days, flagged `possibly_truncated` in the pinned sample, so rows are lost unless pinned) | `get_transactions` (pinned) | S | Each manager's streaming habits, for the opponent model and for §4 |

**How each is checked, and its risk** (each ships red-first on its own PR):
- **P2.** A week's six matchups must parse to 12 team rows; a missing team or a non-numeric cell halts, as `scoreboard_intake.py` already does. For your own matchup, the intake's totals must equal the week card's Yahoo column for that week. Risk: Flaim's sign-in can hiccup (the 16:19Z call failed once and the retry worked), so it retries once, then halts and says so, and never fills from memory.
- **P3.** An identity test: given the preseason lines, no results and random pairings, the new run must reproduce today's odds within simulation error. Both seeds must agree within error, and the standings input must equal Yahoo's W-L-T. Risk: it changes the deck's simulator script (not the frozen draft page), and the title figures must keep carrying the sweep's bands.
- **P4.** P1's tests, plus the adds counted against the weekly 4 from the transaction feed. Risk: a Monday plan is stale by midweek, so it reruns each morning.
- **P5.** With the window set to the whole season, the form z must equal the board's z on the same actuals. Risk: 7 days is 3 to 4 games, so a small sample can overreact. The form view shows the games count beside the season line and never orders the board.
- **P6.** The counts must equal the schedule file's (`facts.py` already computes them). Risk: postponed NBA games, so the schedule is reread each week.
- **P7.** The record is append-only and de-duplicated by transaction id; rerunning a day adds nothing. Risk: a gap of more than 30 days loses rows, because the feed is a rolling window, so the morning run pins it daily.

Fenced out: no trade sweep (owner veto 2026-10-20); no FantasyBot or Yahoo win projection quoted (Flaim documents a Yahoo `winProbability` field on matchups; it is absent from the pinned week-2 response, and if it appears it is data only, never quoted).

## 4. The season's data feeding the Draft Deck (owner's addition)

The red-team registry lists 32 judgment constants (EVIDENCE: 9 uncalibrated, 5 with a declared band, 7 measured, 7 from settings, 4 structural). This season's data can calibrate the ones that move title odds most. Each row below names the data, the constant or source it would calibrate (registry decision id), and when there is enough of it (INFERENCE).

| Data captured this season | Calibrates | Registry status / decision | Enough by |
|---|---|---|---|
| All 12 teams' weekly category totals (P2) | `TEAM_WEEK_SHOCK`, the games shock behind the largest structural band on title odds | declared band, FRAGILE; D-PM-1 | ~8–10 weeks (96–120 team-weeks) |
| Weekly FG%/FT% spreads (P2) | `PCT_MIX_INFL` | declared band; deck N1 refit | ~8–10 weeks |
| Games played by injury tier (`availability_calibration.py`, already running) | `weekly_availability`, `availability` | declared band, FRAGILE / uncalibrated; D-PM-4 | its own check date, 2026-11-17 (`availability_calibration.py:40`; INSUFFICIENT in the 10/22 record) |
| The real schedule by week (already pinned) | `GAMES_PER_WEEK` (3.5) | declared band; deck N1 refit | now |
| Daily lineups (PR #169, once the runner step is stored) | `BENCH_WEIGHT`: how often bench games count | declared band; D-PM-4 / N1 | ~6 weeks |
| Actual games per player this season | `SEASON_GAMES` (65) and so the in-season prior strength | uncalibrated; D-IS-1 | season end |
| Actual per-game lines vs every pinned preseason source (Yahoo, Hashtag, Rotoworld, RotoBaller, FantasyPros, RotoWire ranks, the kit's own) | a **projection-source scorecard**: per-category error by source, for next year's blend weights | new (the sources are pinned; their accuracy against this season's actuals has never been measured) | mid-season and season end |
| The league's category totals needed to win a week | a **winning-threshold profile** for this league: draft targets by category | new | ~8 weeks |
| This draft + 2025-26's, and each manager's moves (P7) | the draft room's manager profiles and the survival curve (`SURV_K`, `SURV_FLOOR`, measured) | measured; refit with a second season | season end |

**Integrity rules for the pipeline** (house rules applied):
- every input is pinned with its sha256 and is append-only;
- a recalibrated constant ships red-first, with the assumption sweep re-run and the bands re-quoted;
- the draft page's frozen engine (`CV`, the v69 lines) is never rewritten mid-season;
- a source that cannot be reproduced (like Yahoo's "games remaining") is never used as a number.

## 5. Bounds

**Out of scope by design:**
- Nothing in this report was built. Each proposal waits for your word, on its own PR.
- No web research on other tools: you asked about the data and access the kit already has.

**In scope and unverified:**
- Effort sizes and "enough by" dates are judgment (INFERENCE).
- Playoff matchups decided by categories won is INFERENCE (§2).
- Why Yahoo's "games remaining" differs by team was not resolved. Three definitions were tested (§1); the recommendation does not depend on the answer.

**Bands.** This report quotes no title share and moves none. The title odds in the morning brief carry the standing sweep's bands (`redteam-2026-10-19/sweep.json`, engine 048efb6):
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared games shock) / −3.4 (shock doubled to 0.12).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy players play 0.95 of games) / +0.9 (healthy players play 0.80 of games).

P2 and §4 would calibrate both from this season's data.

## 6. Decisions for the owner

1. **Priority 1, matchup-aware free agents (§2):**
   - (a) upgrade the week card's pickup scan and add the "This week" view to Free Agents, red-first, on its own draft PR (recommended);
   - (b) probabilities on the week card only;
   - (c) defer.
2. **P2, the weekly league intake from Flaim:**
   - (a) build it next, since it unlocks P3, the ledger scoring and §4 (recommended);
   - (b) keep the hand-filled CSV.
3. **P3, title odds that move:**
   - (a) after P2, on the blended lines, results to date and real pairings (recommended);
   - (b) keep the preseason-line odds.
4. **P4 to P7:**
   - (a) one at a time after P1 to P3, in the order P4, P5, P6, P7 (recommended);
   - (b) pick others first.
5. **Week 2's prediction:**
   - (a) record it with `weekly_preview.py --week 2 --record` before Monday 10/26, so the ledger has no hole (recommended);
   - (b) wait for P2.

## Watchlist

- **Week 2 starts Monday 10/26:** its prediction is recorded only if someone runs it (decision 5).
- **The availability calibration** reports INSUFFICIENT until its check date, 2026-11-17 (`availability_calibration.py:40`).
- **The transaction feed** is a rolling 30 days: rows older than that are gone unless pinned (P7).
- **Week 1's final standings (after 10/25):** each team's W + L + T should be 9, one decision per category. That confirms from results the each-category scoring that §2 rests on (today's evidence is the response's `scoringTypeRaw` `"head"`).

## Open-item receipts

| item | status | receipt |
|---|---|---|
| the week card's daily-lineup rebuild (#169) | **MERGED** 2026-10-22 (`d2f2f0f`); storing the runner step is yours | `after-report-2026-10-22-daily-rosters.md` |
| the afternoon check's rewrite of the morning pull file (#169 decision 3) | **CLOSED**: owner chose "Leave it", 2026-10-22 | `after-report-2026-10-22-daily-rosters.md` §4 |
| the weekly prediction ledger | **OPEN**: week 1 recorded 2026-10-15, never scored | §1; decisions 2 and 5 |
| `availability_calibration.py` name mismatch | **OPEN**, recorded on #168 | `after-report-2026-10-22-name-fix.md` §3 |

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward as the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck 048efb6, checked today, the same page the 10/22 day report and the GAUNTLET report replayed. Its table stands, carried here verbatim from the day report.

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
