# Morning run 2026-11-28

**MORNING: PASS — 2026-11-28: 24 steps; brief report/briefs/brief_2026-11-28.md; record report/briefs/morning_2026-11-28.json**

- **Schedule:** T0 2026-11-28T12:41:13Z. Path: `morning.py --since <T0>`. Saturday: no sweep, no forecasts, no scoreboard intake.
- **Repos:** kit already attached; deck repo pulled. season/daily at dba6729, merge "Already up to date". Tree clean, no stash.
- **Flaim:** league 478.l.36464.
  - Returned: 12 of 12 rosters (one call at a time), matchups for week 6, 100 available players, standings, 12 of 12 dated lineups for 2026-11-27, transactions (99 rows).
  - Flaim again could not interpret 1 Yahoo entry. No errors, no retries.
- **FantasyBot:** outlook only (1 call; Flaim was complete).
- **Session note:** the session context was compacted during the Flaim reads. The governors were reloaded before the scripted run. No owner objections were open.

## Step lines

- LEAGUE LIVE: PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-11-28.json; 3 not in the deck pool (Charles Bassey, Kenrich Williams, Matisse Thybulle)
- MATCHUP LIVE: PASS — week 6, games left 11 mine / 10 Booker T Floppers
- BOX PULL: PASS — 2026-11-27: 11 games, 284 player lines, 200 in the pool; two outlets: 284 matched, 0 cells differ
- MANAGER LOG: PASS — 2026-11-27: 12 lineups, 0 start(s) lost league-wide; outside IL, team played but no box line: Cade Cunningham, Jaylen Brown, Kyrie Irving, LaMelo Ball; 3 new move(s), 229 on record; Flaim could not read 1 row
- TAG OUTCOMES: PASS — 2026-11-27: 36 flagged player(s) 10 no game, 7 played, 17 sat, 2 unresolved
- LINEUP LOG: PASS — 2026-11-27: 2 pair(s), start followed 0; ledger 22 days, start followed 1/3
- SEASON LINES: PASS — 306 lines moved by 0.25+; 3 auto rows (Bassey 17g, Kenrich Williams 19g, Thybulle 19g)
- MINUTES LINE: PASS — 341 players, 303 with games; ratio >= 1.10 for 5, <= 0.90 for 25; 36 unscaled
- THREES LINE: PASS — above the live line by 0.2+ for 24, below for 12; candidate only
- STATUS GATE: PASS — status_2026-11-28.json: 34 flagged rows
- TRANSACTIONS: PASS — 1 feed item 2026-11-26 to 2026-11-28; 0 name a pool player
- DECISION LOG: PASS — R-2026-11-28-01 add_drop Julian Champagnie for PJ Washington; moves: nothing new
- TITLE WATCH: PASS — title 19.0% (was 14.7%), +4.3 against a band of ±0.7: **MOVED**
- WEEK MATCHUP: PASS — week 6 vs Booker T Floppers; to date from Yahoo (rebuild agrees); 5 days, 0 missing; projected 7-2-0
- DECISION CARD: PASS — 2 pairs; order changes between the worlds; top pair holds in 4 of 4
- LEAGUE TABLE: PASS — power #1 SNOWTIME WHITE WALKERS (0.570), you #4 (0.554); Yahoo W-L-T matches the kit's finished weeks
- SEASON DECK: PASS — report/season/deck_2026-11-28.html (7 panes, 317 board rows, 34 status rows; render: 7 tabs, 0 page errors)

## League moves (league_moves_2026-11-28.json, since the 11-27 morning state)

- **SNOWTIME WHITE WALKERS** — added Alex Caruso, dropped Julian Champagnie; RJ Barrett to IL, Dylan Harper off IL.
- **Cade n em** — added Mikel Brown Jr., dropped Sandro Mamukelashvili.
- **Thompson Telepathy** — dropped Kevin Porter Jr.; LeBron James to IL, Austin Reaves off IL.
- **ROOKS FTW** — Cameron Boozer to IL, Jusuf Nurkic off IL.
- Yesterday's waiver pair (Caruso for Gillespie) is gone: SNOWTIME WHITE WALKERS added Caruso (Yahoo, 2026-11-28).

## Brief

- **Week 6 (Yahoo):** you lead Booker T Floppers 7-1-1 after 5 days; games left 11 / 10. Standings 27-18-0, 3rd.
- **Status:** Kyrie Irving is now O on Yahoo (he was Q yesterday afternoon); he had no box line on 11-27.
- **Lineup today (daily-fill rule):** SG Durant, C Ware. Everyone else has no game today.
- **Waiver scan:** 4 of 520 pairs positive; top 2 checked in the simulator (±0.8 sampling error):
  - Add **Julian Champagnie** (SAS), drop PJ Washington: +0.044 cats/week; title 20.3% (+1.3). On waivers until 2026-11-29.
  - Add Kevin Porter Jr., drop PJ Washington: +0.010 cats/week; title 18.8% (−0.3), no gain. He is O and on waivers.
  - Decision card: Champagnie holds in 4 of 4 availability variants (+0.5 to +1.35). In the IL-return world the order flips and the gain is about 0 (−0.04).
- **Title:** 19.0% ± 0.5 (2 runs × 10,000 seasons). Playoffs 99.4%.
  - **Moved +4.3 from yesterday, outside the ±0.7 band.** Title watch lists no method change. Four rival teams changed rosters (above), and the 11-28 season lines moved 306 players. This run does not separate the two causes: no attribution was computed.
  - Structural band (sweep of 2026-11-23, 5 days old): no FRAGILE constant in the headline; weekly_availability SENSITIVE −1.1 / +0.5 (healthy), −1.5 / +1.2 (risk).
  - If IL players return on ESPN's dates: ≈22.7% (scenario, not a forecast; ± 0.54). **ROOM_RULE_ON is FRAGILE in that scenario: +5.1 with the rule off.**

## Deck

- Read before publishing: the live page was Version 112 (1795821326-73d6), this session's 11-27 afternoon publish.
- Published to https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe as Version 113 (1795870084-d7fe).
- The 780,060 built bytes are contained in the 780,606-byte live page, which renders 7 tabs with 0 page errors.
- **WROTE:** 46 path(s) (morning.py).

## Decision for David

The Champagnie pair is the first this week whose title gain (+1.3) clears the sampling error (±0.8). The gain only holds if injured players stay out. Context: 1 of 4 weekly adds used (Gillespie, 11-23); FAAB balance $430.
1. **Claim Champagnie, drop PJ Washington (Recommended)** — Washington has 0 games left this week. The gain holds in 4 of 4 availability variants. FAAB: $70 spent all season ($500 − $430); bids on record since 11-08 total $50 ($15 Caruso 11-10, $35 Collins 11-11).
2. **Hold** — the gain is near the noise line and vanishes in the IL-return world (Haliburton back 12-13 forces a cut). It also keeps the week's last add open for an emergency, per your Saturday/Sunday rule.
3. **Hold until the afternoon check** — see whether Irving's O changes before using an add.
