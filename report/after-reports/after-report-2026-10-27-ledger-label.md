# Forecast-ledger label and OPEN.md tidy — 2026-10-27

Pull window: 2026-10-27 → 2026-10-27 (no pull: code and OPEN.md only; no web search, no market pull).

**Method up front.** Owner 2026-10-27, from the open-decisions list: "Relabel future rows (Recommended)" and "Close both, flag D-LD-2 (Recommended)". Two changes, nothing else: (1) each new row of the pre-week forecast ledger names the lines it ran on, by the same rule the brief has used since 10-26; (2) OPEN.md drops two rows whose PRs are merged and flags one stale default without deciding it. Rows already in any ledger are never rewritten. EVIDENCE marks what a run showed; INFERENCE what is derived.

## 1. The ledger label (EVIDENCE)

`weekly_preview.preview` stamped `lines: v69` (`co_gm.LINES_TAG`) on every forecast row, though the Sunday step runs it with `SEASON_POOL` set, so the forecast is made on the season pool. The rule now lives once, in `co_gm.lines_label()`: "season pool" when `SEASON_POOL` is set, else the frozen tag. The brief's `daily_brief.lines_label()` calls it, so the brief and the ledger cannot disagree. The "no line for" error in the preview names the same label.

Red first: `test_weekly_preview.LinesLabel` runs the real `preview` for week 3 (20 draws per seed, nothing recorded) on main's code and failed `'v69' != 'season pool'`; the frozen-tag case passed. After the change both pass, and so do the brief's two label tests. Full kit suite: 644 tests OK (2 skipped), no stray writes.

Rows already written keep `v69`: the ledger is append-only, and the owner chose future rows only. INFERENCE: a reader of `calibration.json` sees `v69` on weeks recorded before this merge and `season pool` after it; both are true of the run that wrote them.

## 2. OPEN.md (EVIDENCE)

- D-RR-1 (Hunter season override) and D-GP-3 (2022-23 to 2024-25 weekly totals) said "merge is the owner's"; both PRs are merged (#166 at d4cde27 and #164 at 46984bb, both 2026-10-22). They move to a new Closed table that names each merge.
- D-LD-2 (the waiver move, default "watch week 1") is marked STALE: week 1 ended 10-25. The default is not changed and no move is proposed here.

The deck repo's mirror of OPEN.md was not edited (this kit copy is the master); it can be synced on the owner's word.

## 3. Bounds

**Out of scope by design.** No projection line, injury tag, roster or engine constant changed. The draft page, the deck and the title-odds simulator are untouched. The availability-check assessment the owner asked for ("Assess first") is reported in chat, not built here. **In scope and unverified.** None.

## 4. Next steps (owner decisions)

1. Merge this PR; the first `season pool` row is week 3's, recorded Sunday 2026-11-01.
2. D-LD-2 needs a fresh look when the owner wants one.

## Watchlist

- **Sunday 2026-11-01:** `report/calibration.json` week 3 carries `"lines": "season pool"`.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| calibration ledger rows labelled v69 | **FIXED** for future rows; past rows unchanged by design | §1 |
| D-RR-1, D-GP-3 | **CLOSED** (merged) | §2 |
| D-LD-2 | **OPEN**, flagged stale | §2 |

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck e0722cf (this change's deck commit), checked today, the same page the 10/22 day report replayed. Its table stands, carried here verbatim from the day report.

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
