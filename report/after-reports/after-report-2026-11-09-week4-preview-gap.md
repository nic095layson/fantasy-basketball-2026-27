# Why the week-4 preview and the 11-09 week card disagree (owner pick D1, 2026-11-09; after-report only, no code)

Pull window: 2026-11-08 → 2026-11-09 (no pull: report/previews/week_04.md and data/league_state.json + data/season/pool_season.csv at e0fb268 (11-08 morning); report/briefs/week_matchup_2026-11-09.json, data/news/league_moves_2026-11-09.json, data/league_state.json and pool_season.csv at 85556cc; all on season/daily, read only; kit main 8f252a2, deck main e14cc42).

**Method up front.** Order: runner after-report `after-report-2026-11-09-runner-window.md`, pick D1. The two week-4 numbers are the preview (`report/previews/week_04.md`: P(win) 41.0%, 4.22 expected categories, PTS 23%, "Q/O statuses not applied", no band) and the 11-09 week card (`week_matchup_2026-11-09.json`: Σp 5.53, P(5+) 0.784, PTS 0.874). Method parameters, stated before the run: the decomposition changes one input at a time on the preview's own engine (`weekly_preview.simulate` on `arena.team_week_model`, season CV, seeds 2026/2027, 10,000 matchups each). The steps are: (S0) the published inputs; (S1) the 11-09 rosters; (S2) the 11-09 season pool; (S3) each NBA team's real week-4 games (`real_games.team_week_model_games`); (S4) every player's availability set to 1.0. Each step is also run with the shared weekly shock at 0. Scratch worktree at 85556cc, removed after; nothing written to the records. Two runs agree (fixed seeds). EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: the two numbers answer different questions on different inputs. The largest single cause is the opponent's roster: seat 3 moved Luka Dončić and Lauri Markkanen to IL on 11-09, after the preview's 11-08 rosters were taken. That alone moves the preview from 41.0% to 67.5%. The rest comes from the preview's season-long availability discount (every healthy player counted at 0.88 of his games) and the week card leaving out the shared weekly shock. Neither engine is wrong. The preview is stale by Monday, and it carries no band.**

## 1. The decomposition (EVIDENCE: the runs)

| step | P(win) | exp. cats | P(win), no shock | exp. cats, no shock | my PTS | opp PTS | P(PTS) |
|---|---|---|---|---|---|---|---|
| S0 preview as published (11-08 rosters, 11-08 pool, flat 3.5 games) | 0.410 | 4.22 | 0.386 | 4.12 | 593.7 | 665.3 | 0.23 |
| S1 + 11-09 rosters (seat 3: −Dončić, −Markkanen to IL, −Dort; +LaRavia, +Hayes, Hart off IL; mine unchanged) | 0.675 | 5.18 | 0.696 | 5.20 | 593.7 | 540.2 | 0.74 |
| S2 + 11-09 season pool | 0.655 | 5.10 | 0.676 | 5.12 | 591.5 | 541.8 | 0.72 |
| S3 + real week-4 games | 0.612 | 4.94 | 0.628 | 4.94 | 594.7 | 553.8 | 0.68 |
| S4 + availability 1.0 for every player | 0.642 | 5.06 | 0.668 | 5.07 | 683.1 | 627.6 | 0.76 |
| week card 11-09 (its own engine) | P(5+) 0.784 | Σp 5.53 | — | — | 667.7 | 600.7 | 0.874 |

S0 reproduces the published preview exactly (41.0%, 4.22, 593.7 / 665.3, 23%), so the decomposition runs on the preview's real engine.

## 2. The candidate causes, one by one

| candidate (from the order) | finding | evidence |
|---|---|---|
| Seat 3 moved Dončić and Markkanen to IL | **The largest cause.** Opponent PTS 665.3 → 540.2, P(win) 0.410 → 0.675 (S0 → S1). The preview read the 11-08 morning rosters, and the move landed in the 11-09 record (`league_moves_2026-11-09.json`). | EVIDENCE |
| The preview ignores Q/O | It does, but that is not the main gap. The preview applies a **season-long** availability tier to every player (`arena.weekly_availability`: healthy 0.88, mild 0.79, risk 0.75), not today's status. Setting it to 1.0 lifts my PTS 594.7 → 683.1 (S3 → S4). The week card uses today's status (Q/O, Out), which lands it between the two (667.7). | EVIDENCE (S4); INFERENCE (the split between S4 and the card) |
| Flat vs real-games schedule | Small this week, and it cuts the other way: −0.04 P(win) (S2 → S3); the opponent has 46 games to my 45. | EVIDENCE |
| Different engines | Yes. The preview is a joint simulation with a shared weekly shock (`TEAM_WEEK_SHOCK` 0.06) and a game-count variance. The week card is a per-category normal approximation without the shock, a ten-slot daily fill, and today's status. Removing the shock alone moves P(win) +0.02 to +0.03 at every step. The rest of the S4 → card gap (exp. cats 5.07 → 5.53; P(PTS) 0.76 → 0.874) comes from the card's narrower spread and its status-based games. | EVIDENCE (shock column); INFERENCE (the remainder, not decomposed further) |

Not decomposed further: the S4 → week-card step mixes three differences (status availability, daily fill, variance formula). Splitting it needs the week card's engine run variant by variant. That was not done here (did not check).

## 3. Should the preview carry a structural band? (assessment)

The preview's figure rests on two declared-band constants: `weekly_availability` (FRAGILE on title share, sweep 2026-11-02) and `TEAM_WEEK_SHOCK` (D-PM-1). EVIDENCE: the healthy tier alone moves my weekly PTS by about 13% (S3 → S4), and the shock moves P(win) by 2–3 points. The preview prints "±0.7 points", which is the seed spread only. A reader takes that as the whole error bar, but the structural spread is several times larger (INFERENCE from the S3/S4 and shock columns, not a full sweep). The preview also goes stale the moment a Monday move lands, and nothing on it says so.

**Options for the owner:**

1. **A weekly band line on the preview, plus a staleness line (Recommended).** The preview re-runs its matchup under each declared-band variant of `weekly_availability` and `TEAM_WEEK_SHOCK` (six variants, both seeds) and prints the range in the same shape as the deck's band sentence. It also names the rosters' date and, on Monday, any move since. Code, a test and an after-report, on your go.
2. **Staleness only.** The preview names its rosters' date and the moves since (from `league_moves_<Monday>.json`), with no band. Smallest change.
3. **Retire the preview's P(win) once the Monday week card exists.** The week card becomes the week's number; the preview stays as Sunday's look-ahead, marked as such.

## 4. Bands quoted

The standing structural band for any title figure is the season sweep of 2026-11-02 (deck e14cc42): **weekly_availability is FRAGILE:** -2.6 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.2 (healthy players play 0.95 of games) / +0.0 (healthy players play 0.80 of games), mean of the two seeds. That band is on title share. This report's weekly figures carry no published weekly band yet (option 1).

Runner impact: none. Report only.

## 5. Bounds

- Out of scope by design: any change to either engine (report only, per the order).
- In scope and unverified: the S4 → week-card remainder (§2, did not check).
## Watchlist

- 2026-11-09: week 3 on the accuracy card, the candidate's second graded week under D-ML-1.
- 2026-11-16: the week-5 confidence re-run; re-run `backtest.py` on about 20 games per player.

## Open-item receipts

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

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
