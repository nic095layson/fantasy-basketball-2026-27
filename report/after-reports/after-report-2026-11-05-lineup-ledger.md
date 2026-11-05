# Start/sit ledger: the kit's daily start/sit calls against the lineup you locked, with the followed rate and how the night went (owner 2026-11-05)

Pull window: 2026-10-22 → 2026-11-05 (no pull: the records on season/daily read only at a6688ad — the week-matchup briefs, the pinned Flaim daily blocks and the box scores; kit main 2c5c2cf, deck main e14cc42).

**Method up front.** Owner's ask: "When you suggest me to START a player, instead of having him on my bench ... track these on a ledger (system daily play suggested vs. actual played), and provide for me the hit/miss rate." Owner's pick on the card: backfill first, then build. Method parameters, stated before the run: **suggested** = each morning's `week_matchup_<day>.json → lineup_today.moves` (the kit's daily fill when it differs from the lineup as it stood; an empty list is a day the kit agreed); **actual** = the lineup the owner locked that day, from the pinned Flaim pulls' daily block (`get_roster` as of the day; the next morning's pull holds it); **followed** = the named bench player in an active slot at lock (start), the named starter not in one (sit); **night** = the start's box-line z minus the sit's, scored with the engine's own `hoops.zscores` over that day's box lines (the top-156 fixed point, the engine's rule; no constant of this build's). Window: every day with a week-matchup brief, 10-22 → 11-05. EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: 15 days on record, 13 with no suggestion (the kit agreed with the lineup), 2 with suggestions (4 pairs): start followed 3 of 4, sit followed 2 of 4, both 1 of 4; the night went the kit's way 2 of 4. The ledger, its grader and a Week-tab card are built, tested (suite 793 OK, 2 pre-existing skips) and run clean on the live records; nothing merged.**

## 1. What was built (EVIDENCE: the diff, the suites)

- `scripts/lineup_log.py` — reads the three records above for one day, writes one row to `data/decisions/lineup.jsonl` (id `L-<day>`, append-only through `decision_log.append`; a logged day is left as it is), and regenerates `report/decisions/lineup_scorecard.json` + `.md` from the whole ledger. A day whose box scores are not in yet waits (a row written early could never be graded); a day with no brief is reported, never a row; a missing lineup pin or box line is named in the row (`locked: null`, `night: "no grade"`), never guessed. `--date D` grades D−1 (the morning form); `--day`; `--backfill`.
- `scripts/morning.py` — step "lineup log" after "tag outcomes", non-fatal (`LINEUP LOG: PASS`); it runs after "box scores" and "league live", which pin what it reads.
- `scripts/season_deck.py` — optional input `lineup` (`report/decisions/lineup_scorecard.json`, pinned in the deck record as the 16th input); Week tab card "Start/sit calls — followed, and how the night went": the day counts, the followed rates, the night tally, and the pairs by day (last 20 days with a suggestion). Nothing on the deck computes.
- Tests: `test_lineup_log.py` (6: followed/ignored with the engine's night score and accent folding; agreed day and missing pin named; no brief and an empty sit; append-only + waiting for box scores + scorecard roll-up + Markdown; no-games day; `main` lines), `test_season_deck.LineupCard` (2: absent record → pending line; record → rates, names, phone width), `test_morning` (step order updated). Whole suite 793 OK.

## 2. Re-runs on the records (EVIDENCE: scratch worktree at a6688ad, removed after; the records tree untouched)

`--backfill`: `LINEUP LOG: PASS — 2026-10-22: agreed; … 2026-10-26: 2 pair(s), start followed 1; … 2026-11-04: 2 pair(s), start followed 2; waiting for box scores: 2026-11-05; ledger 14 days, 4 pairs, start followed 3/4, night kit 2 / against 2`. A second run on the same days: `already logged`. The 11-05 deck rebuilt with the new code: `SEASON DECK: PASS … pins 16 inputs; 0 page errors`; the card reads 14 days · 12 agreed · 2 with a suggestion, start followed 3 / 4 (75%), sit followed 2 / 4 (50%).

| day | kit said | gap (season z) | locked | followed | night (z) | went |
|---|---|---|---|---|---|---|
| 10-26 | start Ty Jerome, sit PJ Washington | 4.48 | Jerome G, PJ Util | start yes · sit no | −0.57 vs 4.55 | against |
| 10-26 | start Miles Bridges, sit Collin Gillespie | 0.36 | both BN | start no · sit yes | −1.02 vs −1.56 | kit |
| 11-04 | start Kyrie Irving, sit Karlo Matkovic | 7.44 | Kyrie Util, Matkovic F | start yes · sit no | 0.41 vs −2.88 | kit |
| 11-04 | start Kris Dunn, sit PJ Washington | 1.44 (Δexp −0.056) | Dunn SG, PJ BN | start yes · sit yes | −1.35 vs 0.39 | against |

INFERENCE: on both days the owner took the kit's start and benched someone other than the kit's sit (a reshuffle); the ledger scores those as start-followed, sit-not. 11-03's locked lineup is not on record (no morning pull on 11-04 held it): the row says so.

The night is the outcome, not a verdict: the red team measured per-game z noise at sd 3.65 against a 0.5 line (`decision_grade.py`), so one box score cannot judge a pair. The rates that carry meaning are the followed rates and the season-z gap (followed pairs 13.36, ignored 0.36), over weeks.

## 3. Bands quoted

No title share is quoted as a new figure in this report. The standing structural band for any title figure is the season sweep of 2026-11-02 (deck e14cc42): **weekly_availability is FRAGILE:** -2.6 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.2 (healthy players play 0.95 of games) / +0.0 (healthy players play 0.80 of games), mean of the two seeds.

Runner impact: code-only. `morning.py` gains the "lineup log" step from its own step list; the Runner prompt's step-4 and commit text already cover any path the run writes under data/ and report/. No prompt change.

## 4. Bounds and open items

- Out of scope by design: the Out-today card's bench swap (a replacement for a starter with no game) is not a `moves` pair and is not graded here; a value verdict per pair (the red team's noise finding rules it out on one night); any change to how the kit suggests.
- Flagged, not fixed (adjacent): `manager_log.py` lives on season/daily only, not on main; this build does not depend on it.
- In scope and unverified: the first live morning run after merge (the step's PASS line in `morning_<date>.json`); the ledger's first rows are written by that run, not by this PR (the backfill ran in a scratch worktree only — the records branch is the Runner's to write).

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
