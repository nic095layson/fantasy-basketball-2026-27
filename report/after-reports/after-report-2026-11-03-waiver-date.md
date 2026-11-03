# Waiver date and "you dropped him" beside each waiver-scan and streaming pick (owner pick 2026-11-03, display only)

Pull window: 2026-11-01 → 2026-11-03 (no pull: the records on season/daily read only, the 11-01 morning run d9d84c6 and the 11-03 morning run 39b38ee; kit main 0065abc, deck main e14cc42).

**Method up front.** Build order from the owner (option 1 of `after-report-2026-11-03-waiver-readds.md` on season/daily): show Yahoo's waiver date and a "you dropped him <date>" note beside every waiver-scan pair and streaming row; display only; options 2 and 3 not chosen and not built. This supersedes the 11-02 "own-drop fix not built" only for the display. Method stated to the owner before the build: names resolve through the kit's Yahoo-to-pool resolver (`league_intake.resolve`, the one the status gate uses), a date only for `acquisitionState` "waivers", own drops from `league_moves_<date>.json` and its afternoon record for seat 10, never `data/managers/transactions.json`. The look-back window was put to the owner as a clickable choice before the first run: **3 days (today and the two before it), the owner's pick**. EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: the notes show on the brief's pair and streaming lines, in the record (`add_waiver_date`, `add_own_drop_date`, `waiver_notes`) and as a chip on the deck's Free Agents tab and This week's adds; every known answer matches; the 11-03 brief rebuilt with main's code and the new code differs only by the two notes, the JSON identical apart from the new fields; nothing merged.**

## 1. What was built (EVIDENCE: the diff, the suites)

| change | where | test |
|---|---|---|
| `waiver_info(P, yahoo, moves_by_day)`: waiverDate for a pick on waivers in the day's pin, through the resolver; the seat's drops, latest date; a player missing from the 100-row list gets nothing; `WAIVER_DROP_WINDOW = 3` (owner's pick) | `co_gm.py` | `test_waiver_status.WaiverDate` (5): waivers and own drop ("Bobby Portis Jr." to "Bobby Portis"); waivers only (Kris Dunn, dropped by another team); free agent and missing from the list; no pin (no waiver date, no crash, the own drop still shown since it comes from the moves record); a drop outside the window, the afternoon record, missing days named |
| `own_moves(date, window)`: today and the window - 1 days before, morning and `_pm` record each; days with neither named. `waiver_note`, `annotate_waivers`; the pair and streaming lines gain the notes (after an existing status flag with " · ", else " — "); "Waiver dates not read today" with no pin; missing league-moves days named | `daily_brief.py` | `test_daily_brief.WaiverNotes` (2): the exact suffix strings; the two record fields added, nothing else on the row changed |
| The brief's `waiver_notes` map keyed by the brief's spelling and the board's (Cameron / Cam Johnson); a chip beside Free Agents rows and This week's adds | `season_deck.py` | `test_season_deck.WaiverChips` (3, browser read-back); written after the deck code, then checked to fail on main's deck code (1 failure, 2 errors) and pass on the new |

The ranking, the candidate list, d_ecw, the title runs, the status gate, the decision log's matching and every engine constant are untouched. `WAIVER_DROP_WINDOW` is registered in `scripts/redteam/constants_registry.json` as structural: it is the owner's chosen window for a display note and no ranking, candidate or figure reads it (the first gates run failed on it as an unregistered live constant; 46 registered = 46 live after).

## 2. Re-runs on the records (EVIDENCE: scratch worktree at 39b38ee, removed after; the records tree untouched)

| check | result |
|---|---|
| 11-03 brief, main's code vs new code, same records | `diff`: two lines, the notes only; JSON identical apart from `add_waiver_date`, `add_own_drop_date`, `waiver_notes` |
| 11-03 pair 1, Julian Champagnie | "on waivers until 2026-11-04 · you dropped him 2026-11-03" |
| 11-03 pair 2, Tobias Harris | no waiver note; "O today (yahoo), ESPN expects back 2026-11-06, check before claiming" unchanged |
| 11-03 pair 3, Cameron Johnson | "on waivers until 2026-11-04 · you dropped him 2026-11-03" |
| 11-01 (pin and moves of d9d84c6, the 11-01 brief's own pairs) | Bobby Portis: "on waivers until 2026-11-03 · you dropped him 2026-11-01" |
| Negative, 11-01: Kris Dunn (a streaming row that day; dropped by Podz) | "on waivers until 2026-11-02", no own-drop note |
| 11-03 deck on the new brief | SEASON DECK: PASS, 7 tabs, 0 page errors; Free Agents: Champagnie both notes, Bobby Portis "you dropped him 2026-11-01", Jaylen Wells waivers only; Cam Johnson both notes (sorted by season z) |

The 11-01 check ran the helper on the 11-01 records and the 11-01 brief's own pairs, not a full rebuild: the brief reads the current league state, so a rebuilt 11-01 would rank against a later roster.

## 3. Bands quoted

No title share is quoted as a new figure in this report; the 11-03 brief's figures are reproduced unchanged. The standing structural band for any title figure is the season sweep of 2026-11-02 (deck e14cc42): **weekly_availability is FRAGILE:** -2.6 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.2 (healthy players play 0.95 of games) / +0.0 (healthy players play 0.80 of games), mean of the two seeds.

Runner impact: code-only. The morning "daily brief" step reads the league-moves records of the last three days and writes the notes; the deck shows them. No new step, no prompt change.

## 4. Bounds and open items

- Out of scope by design: re-ranking pairs on waivers, a minimum gain (options 2 and 3, not chosen); the afternoon page reads the 5 AM brief's notes, as it does its pairs.
- Flagged, not fixed (adjacent): the Free Agents tab's "this week" sort keys the week-matchup rows by the pool's spelling, so "Cameron Johnson" shows under "not on this board" and his board row ("Cam Johnson") sorts with the unscored players, past the first 60 rows. Pre-existing; the waiver chip is on his row.
- In scope and unverified: the first live morning run after merge.

## Watchlist

- Next morning run after merge: a re-add of a player dropped in the last three days shows both notes in the brief and on the deck.

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
