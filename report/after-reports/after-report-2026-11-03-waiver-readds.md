# After-report 2026-11-03: the waiver scan re-proposes the owner's own fresh drops

**For:** the main session. **From:** the persistent runner (records branch season/daily).
**Owner's request (2026-11-03):** "Write an after report on the waiver re-add issue for Main session."
**Analyzed:** the daily briefs `report/briefs/brief_2026-10-28.md` through `brief_2026-11-03.md`; the pinned Flaim pulls `data/source/flaim/pull_<date>.json` for the same days; `data/managers/transactions.json` (96 rows, pulled 2026-11-03); `scripts/co_gm.py` and `scripts/daily_brief.py` at season/daily 39b38ee (= origin/main 0065abc plus the records); main's `after-report-2026-11-02-runner-fixes.md` (in bbb571d).
**Window: 2026-10-28 → 2026-11-03 (7 briefs).** 10-28 is the first day the status gate fed the scan from the pinned Yahoo list (owner 2026-10-28, "Status gate"). The window was chosen for that reason, not inherited.
**Method:** for each day I took every "Add **X**, drop Y" pair the brief printed, looked X up in that day's pinned available-player list (`acquisitionState`, `waiverDate`), and checked whether the owner dropped X in the two days before. I read the scan's candidate filter in code. No code was changed and nothing was re-run. This is an assessment only.

**Headline.** On 4 of the 7 days, the scan's top pair re-added a player the owner had dropped within the previous 2 days. On all 4 days that player was still on waivers (his waiverDate fell on the next day or two), so the move could not be made that morning. The cause is in code. The scan's candidate list is "every pool player not on a roster". It never reads Yahoo's `acquisitionState`/`waiverDate`, and it has no memory of the owner's last move. The scan ranks season-long expected category wins, and the gaps between bench-level players are small (+0.020 to +0.025 cats/week on three of those days). So players the owner swaps between come back up as the top suggestion. **On 11-02 the owner excluded the own-drop fix from main's build ("not built, the owner's word").** Whether to revisit that is the owner's call, not this report's. This report adds 11-03's evidence and the options.

## 1. Evidence

### 1a. Day by day (EVIDENCE: the brief, the same day's pin, the transactions file)

| Brief | Pairs printed | Re-add of an own drop ≤2 days old | That player's Yahoo state in the pin |
|---|---|---|---|
| 10-28 | 3 | none | Jalen Williams not in the 100-row list; the other two free agents |
| 10-29 | 3 | none | all free agents |
| 10-30 | 3 | none | all free agents |
| 10-31 | 3 | **#1 Julian Champagnie** (dropped 10-31, tr.102) | waivers, waiverDate 2026-11-01 |
| 11-01 | 1 | **#1 Bobby Portis** (dropped 11-01, tr.107) | waivers, waiverDate 2026-11-03 |
| 11-02 | 1 | **#1 Bobby Portis** (same drop) | waivers, waiverDate 2026-11-03 |
| 11-03 | 3 | **#1 Julian Champagnie** (dropped 11-03, tr.114); **#3 Cameron Johnson** (dropped 11-03, tr.115) | both waivers, waiverDate 2026-11-04 |

Totals from this table: 17 pairs printed. Every own drop listed happened hours before that day's brief ran (e.g. tr.114 at 2026-11-03T05:02Z, tr.115 at 06:11Z; the run started at 13:03Z). 5 of them re-add an own drop ≤2 days old, and those same 5 are the only pairs whose player was on waivers. 4 of the 7 #1 pairs are re-adds.

### 1b. The owner/scan cycle (EVIDENCE: transactions tr.102, 107, 114, 115; the briefs)

```
10-31 owner  +Cameron Johnson  −Champagnie      → scan 10-31: add Champagnie
11-01 owner  +Champagnie       −Portis          → scan 11-01, 11-02: add Portis, drop Cameron Johnson
11-03 owner  +Matković −Champagnie, +Dunn −Cameron Johnson
                                                → scan 11-03: add Champagnie / add Cameron Johnson, drop Matković
```

Champagnie was re-added 11-01 08:15Z with a 10 FAAB bid (tr.107), the day after the scan proposed him. Whether the scan prompted that move is not recorded (INFERENCE at most). Champagnie was then on the roster from 11-01 to 11-03 and dropped again.

### 1c. The cause in code (EVIDENCE: `scripts/co_gm.py` at 39b38ee)

- `free_agents()` (co_gm.py:191-211) builds candidates as `p["player"] not in rostered` over the kit pool, ranked by `adj_value`, top `WAIVER_CANDIDATES = 40`. The status gate removes long Outs only.
- `daily_brief.status_inputs()` (daily_brief.py:80-93) loads the pin's `freeAgents` as a **status source only**. Nothing in `scripts/*.py` reads `waiverDate` (`grep -rn waiverDate scripts/*.py`: no hits).
- `waiver_pairs()` (co_gm.py:214-228) scores every add/drop pair by the change in expected weekly category wins against the current roster. It has no input for the transaction history and no minimum gain. On 10-31, 11-01 and 11-02 the top pair was worth +0.020 to +0.025 cats/week.

### 1d. 11-03 is different in size (EVIDENCE: brief_2026-11-03.md; INFERENCE in the last bullet)

- The top pair is +0.188 cats/week, title 12.9% (+3.4), against a 9.5% headline. That is about 8× the earlier days' gains.
- The drop it names is Karlo Matković, the owner's own add from that morning. The streaming section rates him the weakest active player (−3.91 per game).
- INFERENCE: on 11-03 the scan disagrees with the owner's pickup, not just tie-breaking between equal players. A display or memory fix would label this pair, not remove the disagreement. Whether the owner's reason for Matković (for example games this week, or a role change) is something the kit can't see: **did not check**.

## 2. Assessment

| Finding | Tier | Basis | What would demote it |
|---|---|---|---|
| The scan proposes adds that can't be made that morning (on waivers) | **HIGHLY RECOMMEND fixing the display** | EVIDENCE §1a: 5 of 17 pairs, 4 of 7 top pairs | A Yahoo waiverDate that turned out not to block a same-day add |
| The scan has no memory of the owner's last move | **Owner's call: excluded 11-02** | EVIDENCE §1c; main's 11-02 report | already decided against; revisit only on the owner's word |
| Small-gain churn (+0.02/week top pairs) | NICE TO HAVE: a minimum-gain line | EVIDENCE §1c; INFERENCE that the gains are inside noise. The scan's own run-to-run error was not measured here (did not check). | A measured scan error well below 0.02 cats/week |
| 11-03's +0.188 disagreement with the owner's add | NOT a bug: report it | INFERENCE §1d | none needed |

## 3. Bounds

**Out of scope by design**
- No fix, candidate or dry run was built (CLAUDE.md rule 1: a question gets an assessment).
- No trade logic (owner veto 2026-10-20).
- The streaming list was not audited beyond one earlier note: on 11-01 its first name, Kris Dunn, was on waivers (`after-report-2026-11-02-runner-window.md` §4).

**In scope and unverified**
- The exact words of the owner's 11-02 exclusion: main's report says "the waiver own-drop fix" / "own-drop logic". Whether that also covers a display-only waiverDate mark is not stated there. NOT-ATTEMPTED: main's session transcript is not visible from this session. **Load-bearing for option 1 below, so main should confirm with the owner before building it.**
- The scan's run-to-run error on d_ecw: NOT-ATTEMPTED (it would need a re-run; this report is read-only).
- Briefs before 10-28: NOT-ATTEMPTED by choice. The pins before the status gate did not feed the scan, so a pre-gate re-add would have the same cause but different inputs.

## 4. Decisions for the owner (main builds only on the owner's go)

1. **Show Yahoo's waiverDate beside every scan and streaming pick, and add a "you dropped him on <date>" note (Recommended).** Display only. The pin already carries both facts (`freeAgents[].waiverDate`, `data/managers/transactions.json`), and no ranking changes. Main should first confirm this is outside the 11-02 exclusion.
2. Option 1, plus moving pairs whose add is on waivers below the ones that can be made today, still listed with their date.
3. Option 1, plus a minimum gain before a pair is printed as the top pick (the line set from a measured scan error, stated before the run).
4. Keep the 11-02 decision as is: nothing built. The runner keeps recording re-adds in its morning report.

**Owner's pick, 2026-11-03 (clickable card in the runner session): option 1, "Show waiver date".** This is the display-only change: Yahoo's waiverDate and a "you dropped him on <date>" note beside each scan and streaming pick, with no ranking change. Options 2 and 3 were not chosen. Main builds this on that word.

## 5. Provenance

- Produced by the persistent runner session (claude.ai/code/session_01BsJA4wttu98TKVNoh6HBz1), 2026-11-03, after the morning run's commit 39b38ee.
- Re-verify:
  - Per-day table: re-run the lookup in §Method over `report/briefs/brief_2026-10-28..11-03.md` and `data/source/flaim/pull_<date>.json`.
  - Code claims: `grep -n "def free_agents\|def waiver_pairs\|WAIVER_CANDIDATES =" scripts/co_gm.py` and `grep -rn waiverDate scripts/*.py`.
  - The exclusion: `git show bbb571d:report/after-reports/after-report-2026-11-02-runner-fixes.md` lines 5, 16, 44.
- Earlier report on the same finding: `report/after-reports/after-report-2026-11-02-runner-window.md` §4 (3 days, 10-31 to 11-02).
