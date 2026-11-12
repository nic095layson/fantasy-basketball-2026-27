# Owner playbook, corrections log and a Monday review (owner's card 2026-11-12)

Pull window: 2026-10-17 → 2026-11-12 (no pull: this session's conversation with the owner on 11-11 and 11-12, and the kit's files at main 383bb07, read only).

**Method up front.** The owner asked how the system's standards, integrity and effectiveness are upheld between working sessions. The assessment named four gaps: findings wait for a conversation, the owner's judgment is not on record, a session's corrected errors are not tracked, and winning is not measured directly. Four options went to him on a card; he picked "Weekly review + playbook (Recommended)". Parameters: the playbook holds only what the owner said, quoted with its date, and a session's interpretation is labelled as one; the corrections log holds only statements this session made and then corrected against a record. EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: the owner's operating rules and his read of the league are now on file, this session's six corrected errors are on file, and a read-only review is scheduled for Mondays. No code, projection, roster, constant or engine file changed.**

Runner impact: none — three documents and one pointer line in `CLAUDE.md`; no script the Runner calls is touched and no prompt edit is needed.

## 1. What was added

| File | What it holds |
|---|---|
| `OWNER-PLAYBOOK.md` | The 2-for-1 method, the monthly free-agent budget, weekly adds, core players, how this league prices three players, how the owner wants to work, and the upkeep arrangement. Verbatim quotes with dates. |
| `report/corrections-log.md` | Six rows: what the session said, what the records showed, how it was caught, the check that prevents it. Append-only. |
| `CLAUDE.md` | Three lines, above the doctrine block and outside it, pointing sessions to the two files. The block itself is unchanged. |

## 2. The Monday review

A scheduled task bound to the owner's working conversation, Mondays 16:13 UTC, after the morning run. It reads the week's accuracy card, Draft Check record, run ledger, decision grades and the corrections log, and reports what was wrong, what it cost and fixes as options. It writes nothing and merges nothing. It lives in the scheduler, not in this repository.

## 3. Checks

EVIDENCE: `git diff --stat` shows four files, all documents. The doctrine block in `CLAUDE.md` is byte-identical before and after (checked by extracting the text between the BEGIN and END markers at 383bb07 and at this commit). No test was run, because no code changed; the gates were run on this report and their result is in `gates.json`.

## 4. Bounds

- Out of scope by design: any change to how the kit computes; recording the owner's statements from sessions before 11-11; a direct weekly measure of whether following the kit's advice beat the owner's own moves (named as a gap, not built).
- In scope and unverified: the Monday review has not yet fired; its first run is 2026-11-16.
- One open item is recorded in the playbook as open: whether an unspent month's budget carries over.

**weekly_availability is FRAGILE:** -4.8 (no in-sim injury discount (risk 0.88 like healthy)) / +2.9 (harsher risk tier (0.65)) / -0.9 (healthy players play 0.95 of games) / -0.4 (healthy players play 0.80 of games), mean of the two seeds. No title figure is computed in this change; the last one on record is the 11-11 morning's 16.06%, 10,000 seasons on two seeds.

## 5. Next steps (owner decisions)

1. Merge on your word.
2. Answer the budget carry-over question when convenient.
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
