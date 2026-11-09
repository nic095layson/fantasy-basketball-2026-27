# The decision log matches alternative pairs (owner pick C1, 2026-11-09)

Pull window: 2026-11-09 → 2026-11-09 (no pull: data/decisions/recommendations.jsonl, session.jsonl and moves.jsonl on season/daily read only at 85556cc; kit main 8f252a2, deck main e14cc42).

**Method up front.** Order: runner after-report `after-report-2026-11-09-runner-window.md`, pick C1. `decision_log.join` compared a move only against each recommendation's top pair, so the owner's 11-08 move (+Cameron Johnson −Ziaire Williams), which was alternative 2 of the 11-07 brief, matched the 10-30 session row as a partial. Method parameters, stated before the build: the join reads the top pair and every alternative (`top`, `alt1`, `alt2`, … in the order the row lists them). The newest row in the horizon wins; within a row an exact pair beats a partial one; the add-then-drop tiering and the horizon are unchanged. The move row records `matched_pair`, and the grader grades against that pair's add, drop and d_title. Committed `moves.jsonl` rows are not rewritten. EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: built and tested. The known answer holds on the real ledgers: M-2026-11-08-01 → R-2026-11-07-01, alt2, exact (it was S-2026-10-30-01, add_match_drop_differs). M-2026-10-31-01 stays on S-2026-10-30-01 but becomes exact through alt5. Two older moves would also re-match. No committed row was changed; how to bring the old rows in line is an owner decision (§4).**

## 1. What changed (EVIDENCE: the diff, the suite)

- `scripts/decision_log.py` — `_pairs(rec)`, `join_pair(move, recs)` → (id, kind, pair). `join()` keeps its two-field form. `moves_rows` writes `matched_pair` on new rows.
- `scripts/decision_grade.py` — `grade()` finds the matching move first and takes `kit_add`, `kit_drop` and `d_title_at_rec` from the matched pair. A row with no `matched_pair` (every row logged before this change) is graded on the top pair, as before. The grade row carries `matched_pair`, and the scorecard's "kit said" cell names the pair when it is an alternative.
- `scripts/test_decision_log.py` — class `AlternativePairs` (6 tests): the 11-08 known answer on the two rows copied from the ledgers, alt5 exact beats top partial within one row, newest row first, top-only rows unchanged, `moves_rows` records the pair, and the grader grades the matched pair.

Red first (EVIDENCE): before the change, `AlternativePairs` gave 6 errors (`AttributeError: module 'decision_log' has no attribute 'join_pair'` ×4, `KeyError: 'matched_pair'` ×2). After, `test_decision_log` passes 19 tests.

Readers of the match fields (EVIDENCE: grep of `match_kind`, `"matches"`): only `decision_grade.py` reads them. Nothing depends on top-only matches.

## 2. Every logged move re-joined (EVIDENCE: `join_pair` over the real ledgers, read only)

| move | +add −drop | committed | re-joined |
|---|---|---|---|
| M-2026-10-24-01 | +Collin Gillespie −Anthony Black,Christian Braun | R-2026-10-22-01 drop_match_add_differs | same, top |
| M-2026-10-25-01 | +Noah Clowney | unrelated | same |
| M-2026-10-26-01 | +Julian Champagnie −Noah Clowney | R-2026-10-22-01 add_match_drop_differs | **R-2026-10-25-01 exact alt1** |
| M-2026-10-28-01 | +Bobby Portis | R-2026-10-27-01 add_match_drop_differs | **R-2026-10-28-01 add_match_drop_differs alt2** |
| M-2026-10-31-01 | +Cameron Johnson −Julian Champagnie | S-2026-10-30-01 add_match_drop_differs | **S-2026-10-30-01 exact alt5** |
| M-2026-11-01-01 | +Julian Champagnie −Bobby Portis | R-2026-10-31-01 add_match_drop_differs | same, top |
| M-2026-11-03-01 | +Karlo Matkovic,Kris Dunn −Cameron Johnson,Julian Champagnie | R-2026-11-02-01 drop_match_add_differs | same, top |
| M-2026-11-05-01 | +Ziaire Williams −Karlo Matkovic | S-2026-11-05-01 exact | same, top |
| M-2026-11-08-01 | +Cameron Johnson −Ziaire Williams | S-2026-10-30-01 add_match_drop_differs | **R-2026-11-07-01 exact alt2** |

M-2026-10-28-01 is an afternoon move (`league_moves_2026-10-28_pm.json`), so the 10-28 morning brief came before it. EVIDENCE: the phase on the row. INFERENCE: matching that brief is sound.

M-2026-10-31-01 (the question in the order): the row stays S-2026-10-30-01, and the kind moves from add_match_drop_differs to exact. Julian Champagnie was the session row's fifth alternative (Johnson for Champagnie, d_title −0.45). Graded under the new rule, that move would be scored as the kit's alt5 pair (Johnson vs Champagnie) and not as the kit's top pair against the owner's drop. In other words, the owner's drop would be graded as one the kit had listed, at −0.45, not as a deviation.

## 3. What this does and does not change today (INFERENCE)

New moves logged after merge carry `matched_pair` and are graded on it. The nine committed rows keep their `matches`/`match_kind` and carry no `matched_pair`, so the grader treats them as before. As it stands, the four re-joins above do not reach the scorecard. No grade has reached a final verdict yet (EVIDENCE: `report/decisions/grades.jsonl` on season/daily is empty); the first window closes on 11-17 (R-2026-10-20-01, which no re-join touches).

Windows the re-join would move (EVIDENCE: `decision_grade.grade` over the real ledgers, committed moves vs re-joined, as of 11-09):

| rec | committed rows: window end, pair | re-joined: window end, pair |
|---|---|---|
| R-2026-10-22-01 | 2026-11-23 (opened by M-2026-10-26-01), top | 2026-11-19 (no matched move: opens on the rec date), top |
| R-2026-10-25-01 | 2026-11-22 (no matched move), top | 2026-11-23 (opened by M-2026-10-26-01), alt1 |

## 4. Open decision for the owner: the nine committed rows

1. **Append a re-join record (Recommended).** Add a new append-only file, `data/decisions/moves_rejoin.jsonl`, with one row per changed move: id, old match, new match, pair, rule date. The grader reads a move's newest re-join over its logged match. `moves.jsonl` stays as written. This has to be in place before 11-19, when R-2026-10-22-01's window would close under the re-join.
2. **Leave them.** Moves logged before 11-09 are graded under the top-only rule, and the scorecard says so in one line. Nothing to build.
3. **Rewrite the four rows in place.** This is simplest for the grader, but it breaks the append-only rule the ledger was built on. Not recommended.

## 5. Bands quoted

This report quotes no new title share. The standing structural band for any title figure is the season sweep of 2026-11-02 (deck e14cc42): **weekly_availability is FRAGILE:** -2.6 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.2 (healthy players play 0.95 of games) / +0.0 (healthy players play 0.80 of games), mean of the two seeds.

Runner impact: code-only. The Monday decision step and the morning moves step run the same commands; new move rows gain one field. No step or prompt change.

## 6. Bounds

- Out of scope by design: the committed ledger rows (§4); the lineup ledger (`lineup.jsonl`), which has its own join.
- In scope and unverified: the first move logged after merge.
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
