# Morning run 2026-10-29

**MORNING:** PASS — 2026-10-29: 16 steps; brief report/briefs/brief_2026-10-29.md; record report/briefs/morning_2026-10-29.json

- **T0:** 2026-10-29T12:04:06Z. Step 4 ran `morning.py --since 2026-10-29T12:04:06Z` (`--help` lists `--since`).
- **Repos:** the kit was already attached (origin nic095layson/fantasy-basketball-2026-27); the deck repo was pulled fast-forward. Tree clean, no stash. season/daily merged origin/main cleanly (#224, #225 came in).
- **Flaim:** tools present. 12 of 12 roster calls returned data; matchups (week 2), the 100-player available list and standings came back. No retries were needed. league_id 478.l.36464 as expected.
- **FantasyBot:** tools present. The outlook alone (1 of 1) returned; the 13 roster calls were not needed.
- **LEAGUE LIVE:** PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-10-29.json; 1 not in the pool, not simulated: Matisse Thybulle (MAXEY-MUM OVERDRIVE, F)
- **WEEK MATCHUP:** PASS — 2026-10-29: week 2 vs Looking Cool Joker!; to date from Yahoo (rebuild agrees); to date 3 day(s), 0 missing; projected 7-2-0
- **Live matchup:** week 2, games left 18 mine / 19 Looking Cool Joker! (data/news/matchup_live_2026-10-29.json).

## League moves (data/news/league_moves_2026-10-29.json, 2026-10-28 → 2026-10-29)

- **KEL'EL YAXEL HALQUETA (yours)** — added Bobby Portis; to IL: Tyrese Haliburton
- **Looking Cool Joker!** — added Keldon Johnson, Mo Bamba; dropped Precious Achiuwa
- **ROOKS FTW** — to IL: Naji Marshall; off IL: AJ Dybantsa
- **Splash Mountain** — added Robert Williams III; to IL: Ziaire Williams

## Step lines

- **TAG OUTCOMES:** PASS — 2026-10-28: 33 flagged player(s) 3 no game, 7 played, 22 sat, 1 unresolved; data/status/tag_outcomes.jsonl
- **MINUTES LINE (candidate only):** PASS — 2026-10-29: 338 players, 284 with games; ratio >= 1.10 for 12, <= 0.90 for 25; 33 unscaled (no preseason mpg); candidate only, wrote pool_season_mt.csv, projections_season_mt.csv
- **STATUS GATE:** PASS — status_2026-10-29.json: 26 flagged row(s), each tiered with a dated receipt
- **MANAGER LOG:** PASS — 2026-10-28: 12 lineups, 1 start(s) lost league-wide; outside IL, team played but no box line (inactive or unmatched name): Alex Caruso, Lauri Markkanen; profile 2026-10-22..2026-10-28 (7 day(s)); 4 new move(s), 73 on record. All 12 dated lineups and the transactions (73 rows; Flaim notes 6 entries it could not interpret) came back.
- **SEASON DECK:** PASS — 7 panes, 315 board rows, 26 status rows; 7 tabs, 0 page errors.
- **Two non-fatal FAILs:**
  - LEAGUE PAIRINGS: FAIL — week 1: team 'Giavaris Jamal Javarison-Lamar' is not in the league state
  - LEAGUE TABLE: FAIL — week_1.json has no yahoo_score for ['ANONG NANGIANNIS?!']
  - Cause (EVIDENCE): team 5 is now named "ANONG NANGIANNIS?!" on Yahoo. The committed 10-28 league_state.json still names it "Giavaris Jamal Javarison-Lamar". Both steps match teams by name. Nothing was changed.

## Deck

Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 42 (1793275736-dde7).
- The 499,167 built bytes are contained in the live page (499,713 bytes).
- The page shows 7 tabs.

## Brief

- **Lineup today:** PG Ty Jerome. He is the only player with a game today; the other 12 are idle.
- **Waiver scan:** "Status from Yahoo and ESPN."
  - Set aside as Out: Jalen Williams (Out, espn, back 2027-03-02), Cason Wallace (O, yahoo, back 2027-03-02), Kevin Porter Jr. (NA, yahoo), Justin Champagnie (O, yahoo, back 2027-02-25), Dylan Cardwell (O, yahoo, back 2026-11-06).
  - Top pair: add Cameron Johnson, drop Collin Gillespie. +0.030 cats/week; title 16.6% (+0.9). He is O today (yahoo) and ESPN expects him back 2026-10-30, so check before claiming.
- **Title:** 15.6% ± 0.5 (avg of 2 runs × 10,000 seasons); playoffs 96.1%.
  - Structural band (season sweep of 2026-10-26): TEAM_WEEK_SHOCK FRAGILE +2.7 / −4.2; weekly_availability FRAGILE −5.4 / +3.7 / +0.4 / −0.5.
- **Movers:** 287 lines moved by 0.25+ (data/season/season_lines_2026-10-29.json). On your roster the moves are small and go both ways: Ty Jerome pts 17.5→20.6, Yaxel Lendeborg pts 11.7→15.0, Derrick White pts 16.8→15.7, Kyrie Irving pts 22.7→21.5.
- **Unpooled with games:** 123 (SEASON LINES); Matisse Thybulle is the one rostered unpooled player.

## Surprise: title share 32.6% → 15.6% in one day (not root-caused)

- EVIDENCE:
  - The brief's title went from 32.57/32.64 (10-28) to 15.0/16.27 (10-29), and playoffs from 99.9% to 96.1%.
  - The base expected weekly category wins went from 5.57 to 5.03.
  - My Yahoo record is unchanged, 3-6, in both days' pinned standings.
  - The code merged from main (#224, #225) touches no engine file; it touches scripts/season_deck.py, status_feed.py, redteam/attacks.json and tests.
  - Haliburton and Kawhi were already tagged Out on 10-28.
  - The roster's summed board z fell from 11.53 to 9.12 after the 10-28 box scores. Looking Cool Joker!'s total fell more, from −2.41 to −10.31; Cade n em and Booker T Floppers rose.
- NOT-ATTEMPTED: decomposing which input moved the title share. That needs re-running the simulator on mixed inputs, which this run does not do.
- Until it is explained, treat today's title figure as candidate.

## Records

- WROTE: 28 path(s) (morning.py).

## Decisions for David

1. **Title drop (Recommended: have the main session root-cause it).** Re-run the 10-29 brief with yesterday's lines and today's rosters, and the reverse, to see which input halved the title share.
   - Alternative: wait one day and see whether it persists.
2. **Team-name keying.**
   - (Recommended) Have the main session key league_pairings and league_table on Yahoo team id instead of name. A rename then can't break them.
   - Alternatively, add a one-time alias for team 5's rename.
   - Or accept both steps failing until week 1's files are regenerated.
3. **Afternoon run:** #225 is now on main, so today's 3 PM run should write status_2026-10-29_pm.json for the first time. No action needed.
