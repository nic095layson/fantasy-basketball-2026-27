# The level gap and the card's shock term: Council, measurements, and what was built

Pull window: 2026-11-16 → 2026-11-16 (no pull: kit main 19d0eb5, deck main 1a47f81; the records branch season/daily at b35ad98, read only; measurements and the week-4 refit in throwaway worktrees and scratch).

**Owner's order, verbatim (2026-11-16):** "Have council deliberate the two open decisions and proceed." The two decisions are section 8 of `after-report-2026-11-16-shock-fit.md`: the model's weekly level running 10% low, and the card's category edges carrying no shock term.

**Method up front.** The facts were measured before the Council deliberated:
- NBA games per team per Yahoo week, from the box-score records in `data/actuals/`.
- Yahoo's counted totals against everything each Sunday roster produced in the week's box scores.
- How much managers differ in that ratio (one-way ANOVA).
- What a uniform 10% level error does to the title share.

The verdict and the plan were shown to the owner before any file was written. One owner card was answered mid-build (section 5). Tests were written first and seen failing.

**Verdict: the level gap is left in the engine and now measured every Monday. The card's season edges now carry the shock's variance, and the card agrees with the simulator to within 0.004 per category (it was 0.08). One correction: my earlier "bench backfill" reading of the gap is withdrawn, and so is my own first measurement of streaming, which a name-join error inflated.**

Runner impact: code-only — the Monday fit (`scoreboard_intake` → `fit_constants.run`) also writes `level`, `in_week` and the shock's level-relative value; the brief's waiver pairs, the package scan and the week card's season edges read the shock term through `co_gm.pwins`. No step, prompt or schedule changes.

Pool rows touched: none

## 1. The measurements (weeks 1-4, 48 team-weeks)

| Measure | Value | Source |
|---|---|---|
| Model level: actual / model, counting categories | 1.103 (3PTM 1.12, PTS 1.08, REB 1.09, AST 1.10, ST 1.11, BLK 1.06, TO 1.16) | refit on season/daily b35ad98 |
| NBA games per team per Yahoo week | 3.28 (week 1: 2.87, 2: 3.27, 3: 3.60, 4: 3.40); the model assumes 3.5 | `data/actuals/` |
| Per-game lines vs actual, PTS | Run high: preseason +5.7% to +13.0%, in-season +1.7% to +9.1% | `report/accuracy.json` |
| Yahoo totals / the Sunday roster's whole box-score production | 1.04 on PTS (league mean); seats 0.98 to 1.07 | `data/actuals/` and the accuracy snapshots |
| Do managers differ in that ratio? | No: F = 0.50 (df 11, 36) on PTS; 1.31 on the seven counting categories (the fit's measure); the 95% line is about 2.07 | one-way ANOVA |
| A uniform 10% level change, owner's title share | 15.45 / 15.52 → 15.58 / 15.15 (6,000 seasons, season rosters, random pairings) | scratch run |

What they mean (INFERENCE):
- Two inputs push the model's level up: fewer real games than 3.5, and per-game lines that run high.
- In-week adds lift Yahoo's totals by about 4%. So the model's own count of started games, the daily-fill weights times availability, is the most likely remaining cause.
- A uniform level error leaves the order of teams, and so the title share, unchanged. The shock is measured relative to the level (`after-report-2026-11-16-shock-fit.md`, section 4).

## 2. The Council

| Decision | Vote | Verdict |
|---|---|---|
| The level gap | 4-1 | Leave the engine. Record the level and the per-team in-week factor (with the between-team F) in every Monday fit. Re-open per-team streaming in the simulator when F clears its 95% line |
| The card's shock term | 5-0 | The card's season edge carries the shock's variance (shock² × mu² per team on the counting categories), so it is the simulator's own marginal |

Dissent on the level gap (Contrarian): fix the model's game count now, since the absolute numbers in the brief are off. That vote flips if the weekly P(win) calibration shows a bias.

## 3. What changed

| Where | Change |
|---|---|
| `scripts/co_gm.py` | `_pcat(m, om, c, shock=0.0)`; `pwins` passes `arena.TEAM_WEEK_SHOCK`. The week card's in-week chances (`week_matchup`, on totals partly already played) call `_pcat` without it and are unchanged |
| `scripts/fit_constants.py` | `level(rows)`, `in_week_factors(week, …)` (names joined through `box_pull`'s fold, suffix key and alias table), `between_team_f`, `level_relative`. The Monday record and summary carry all four |
| `scripts/test_fit_constants.py` | 5 tests, seen failing first |
| `postmortem-2026-10-19/rt_consistency.py` (A-3) | The card's ECW mirrors the shock term; record re-made; old record `rt_consistency_pre-2026-11-16-card.json` |
| `scripts/redteam/attacks.json` | A-3 history row |

## 4. Checks

| Check | Result |
|---|---|
| New tests first | 1 failure and 4 errors, then OK |
| Full kit suite | 1,259 OK. The first full run failed 2 week-card tests: I had put the shock into `_pcat` itself, which the week card also uses for this week's partly played totals. I moved it into `pwins` only, and the week card's tests pass unchanged |
| A-3 on the live references | Max gap 0.0029 / 0.0036 (was 0.084 / 0.086), mean 0.0009 / 0.0010, rank agreement 1.0 / 1.0 |
| Week-4 refit with the new fields | Level 1.103; in-week F 1.31 (df 11, 36); shock 0.1177, level-relative 0.1067 (live 0.11) |
| Standing attacks / claims | 11 of 11 CURRENT; claim gate PASS |

## 5. The decision ledger under the new card (branch rule fired; owner card)

Every logged add/drop recommendation was re-scored on the records of its own date (season/daily at that day's last commit), with the current engine, with and without the shock term:
- 17 could be re-scored. 16 keep their sign. Their edges shrink by 6% to 86%, and the smallest edges shrink most (R-2026-11-11-01: +0.026 → +0.004; R-2026-11-16-01, Champagnie for Hezonja: +0.092 → +0.081). The owner card stated "about 10-40%", which the table does not support (corrections log).
- One flips: R-2026-10-22-01, Champagnie for Braun, from −0.0021 to +0.0018. Both are about zero, the value recorded at the time was +0.001, and the new formula keeps that recorded sign.
- 4 could not be re-scored: the dropped player was already off that day's end-of-day roster.

Owner card (2026-11-16, verbatim pick): **"Proceed, flip recorded (Recommended)"**. Nothing in the ledger is rewritten.

## 6. Corrections to what I told the owner today

- The shock report (`after-report-2026-11-16-shock-fit.md`, section 4) gave "bench backfill" as the likely cause of the level gap. It was labelled an untested inference, and the measurement does not support it (section 1). Withdrawn.
- During this deliberation I first measured in-week streaming with a plain name match. Box-score spellings ("Jaime Jaquez Jr", "Herb Jones", "Darius Acuff") missed their roster rows, so the Sunday rosters looked smaller and streaming looked large: seat 1 +41%. A what-if built on that number cut the owner's title share from 15.5% to about 1.3%. With the folded join, streaming is about +4%, and managers do not differ (F 0.50). Both numbers were withdrawn before the Council voted. Rows are in `report/corrections-log.md`.

## 7. Bounds

Out of scope by design: any engine change for the level gap (the vote); the draft deck's own card in `docs/draft-deck.html`, which the draft used and the season tools do not read.

In scope and unverified: none.

Limit: the remaining level gap is attributed by elimination (section 1). The model's started-games count was not measured directly (NOT-ATTEMPTED). I did not check whether the records hold every team's daily lineups (`data/decisions/lineup.jsonl` holds the owner's). Not load-bearing for the vote: a uniform level leaves the order of teams unchanged (section 1).

## 8. Decisions for the owner

1. **Merge the kit PR on your word.** No deck change.
2. **Nothing else is pending from this Council.** The Monday fit now carries the level and the in-week F, and re-opens the question when F clears about 2.07.

## 9. Provenance

One Claude Code session on 2026-11-16 (session model A), on the owner's order above. The Council's deliberation stayed internal; its condensed verdict was shown before the build. Re-verify: `python3 -m unittest scripts.test_fit_constants`; `python3 report/after-reports/postmortem-2026-10-19/rt_consistency.py`; the refit with `FC.run(4, …, actuals_dir=<records>/data/actuals)` on season/daily.
