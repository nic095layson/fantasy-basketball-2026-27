# Team-update path: a pooled player's club changes when Yahoo and ESPN agree (runner pick D3, owner 2026-11-11)

Pull window: 2026-11-08 → 2026-11-11 (one fetch: ESPN's public NBA teams list, 2026-11-11, HTTP 200, pinned at `data/reference/nba_teams_espn.json` with its sha256; else no pull: `report/after-reports/after-report-2026-11-11-runner-window.md`, `data/league_state.json`, the 11-11 Flaim roster transcription, `data/news/transactions_2026-11-10.json` and the season files at 5d72328 on season/daily, read only, plus one trial on a scratch copy; kit main 3604772).

**Method up front.** Order: the Runner's after-report of 2026-11-11, section "Owner picks", D3 "Team-update path (Recommended)". D1 and D2 were picked as no build and are not built. Tests were written first and seen failing. The plan, shown to the owner before the first edit, named every reader of the pool team and said the change lives in the season files' team column. One hand-set number: a 14-day lookback on ESPN items. EVIDENCE marks what a run or a read showed.

**Verdict: a pooled player's NBA team now changes only when Yahoo's roster pull and an ESPN transactions item agree on the move. Each change is an append-only ledger row with both receipts and can be reversed. On a scratch copy of today's records, Nique Clifford becomes OKC and the disagreement list is empty. The real change lands on the first morning run after this merges; season/daily was not touched.**

## 1. The rule

A change is made when both hold:

1. Yahoo's roster shows the player on a club other than the pool's (today's flagged disagreement).
2. An ESPN transactions item from the last 14 days names that player moving to that same club: "Traded … to the <club>", or an "Acquired", "Signed" or "Claimed" item listed under the arriving club. In a trade item the player's name must stand before "to the": a player named after the club is the piece that came back, and that wording does not say where he went.

Yahoo alone stays a flagged disagreement. ESPN alone is not a disagreement and changes nothing. Wording that names no arrival (waived, recalled, a club ESPN's list does not carry) changes nothing. Club names are read against ESPN's own team list, pinned with its receipt; the kit had no team-name table.

## 2. Where the team is read, and what the change reaches

| reader | source of the team | reached |
|---|---|---|
| roster intake (`league_intake.py`, the disagreement flag) | pool row | yes: reads the ledger, decides, clears the flag |
| `season_lines.py` (writes `pool_season.csv` and `projections_season.csv`) | preseason base files | yes: the ledger's club in the team column only |
| real-games forecast, waiver pairs and streaming games-left, accuracy card, minutes-line files, season board, deck Board and playoff-games column | the two season files | yes, through those files |
| week card and lineup check, rostered players | Yahoo's team | already correct; unchanged |
| title simulator (`league_sim`) | does not read a player's club; games per week are flat | not affected |

The Runner's report inferred that the simulator schedules Clifford on SAC's games. EVIDENCE (read of the deck repo's `arena`): the simulator reads no team schedule; the club matters to the real-games forecast and the games-left counts.

**The change lives in the season files' team column.** The preseason files (`report/projections-2026-27.csv`, the deck's `players_v69.csv` and `data/players.csv`) are not edited. No projection line, injury tag or engine constant changes.

## 3. Records and reversal

`data/team_changes.jsonl`, one row per change: id, date, player, from, to; `yahoo` (the pull file, its sha256, the team shown); `espn` (the item's date, text, listing club and the transactions file it was read from); the rule. The Runner's morning commit carries it with the other records.

`python3 scripts/team_updates.py --revert "<player>" --note "<why>"` appends a revert row. The pool team applies again, the disagreement is flagged again, and that same change is not made a second time. `--list` prints every row.

## 4. Known answers

| case | expected | result |
|---|---|---|
| Nique Clifford: Yahoo OKC, ESPN "Traded G Nique Clifford to the Oklahoma City Thunder." (2026-11-08) | pool team OKC; disagreements `[]` | PASS (test, and the scratch trial below) |
| Yahoo-only mismatch, no ESPN trade item | stays a disagreement, no ledger row | PASS |
| ESPN trade item, Yahoo still on the old club | no change, no ledger row | PASS |

EVIDENCE (scratch copy of season/daily 5d72328, the 11-11 roster transcription): before, `[{'player': 'Nique Clifford', 'yahoo': 'OKC', 'pool': 'SAC'}]`; the intake printed "0 NBA-team disagreement(s) with the pool; 1 team update (Nique Clifford SAC to OKC)"; the ledger row carries pull_2026-11-11.json with sha 8027ed5d… and the ESPN item from transactions_2026-11-10.json. Season lines then differed from the committed files in exactly one row of each file, the team cell: `Nique Clifford,SAC,…` to `Nique Clifford,OKC,…`.

## 5. Checks

- Red first: `test_team_updates` (28 tests; the module did not exist; three wording tests were added, each seen failing, after the review pass found a trade that names the player as the return piece). They cover the names list, the wording rules, the three known answers, a second run writing no second row, the ledger, reversal, the season files and the wiring.
- Whole suite on this branch: 1102 tests OK (2 skipped).

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds (season sweep 2026-11-09, engine 01483de). This change touches no title figure: the simulator does not read a player's club.

## 6. Bounds

- Out of scope by design: D1 (box scores when one outlet is late) and D2 (two deck publishers): owner picked no build.
- Out of scope by design: a free agent's club. The rule starts from a roster disagreement, so only rostered players are covered; a traded free agent keeps his pool club until someone rosters him.
- In scope and unverified: the change inside a real Runner morning (did not check: the next run is 2026-11-12). The ESPN item must still be in a transactions file within 14 days; `transactions_2026-11-10.json` carries it.
- In scope and unverified: how much the SAC club skewed Clifford's games-left and real-games figures (did not check).
- ESPN wording other than the three forms above is not recognised; such a trade stays a flagged disagreement until the wording is added.
- Watch only (F5, nothing changed): the decision card has now appeared in a published deck. EVIDENCE: `deck_record_2026-11-11.json` pins `decision_card_2026-11-11.json` as present, and that deck was published as Version 73 at 16:2xZ on 2026-11-11 by the session re-run. Whether the 2026-11-12 morning deck shows it is not known until that run; a check is scheduled.

## 7. Next steps (owner decisions)

1. **Merge (Recommended).** Clifford's club is corrected on the next morning run, with its ledger row.
2. Hold.

Runner impact: code-only. The live roster step and the season-lines step read the ledger; no prompt changes. The Runner's commit will include one new record file, `data/team_changes.jsonl`.

## Fired

plan-gate (loaded; plan table and the reader list shown before the first edit) · adversarial-verify (loaded before the PR) · scope-fence: not loaded (the work stayed inside D3).

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
