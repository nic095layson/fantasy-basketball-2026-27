# The simulator refuses an over-limit roster on request; the Holmgren trade re-priced (2026-11-24)

Pull window: 2026-11-24 → 2026-11-24 (no pull: kit main ce3bb13, deck main 4fcd92b, the records branch season/daily at 6f2058be, read only; simulations in a throwaway worktree).

**Owner's request, verbatim (2026-11-24).** Card pick "Fix the simulator first", after the session reported that its simulator runs of his composed trade (Derrick White + Yaxel Lendeborg for Chet Holmgren) swung 10 to 14 title points on one bench player.

**Method up front.** Stated to the owner before the change: diagnose with five controlled runs (2 seeds), then fix tests-first. Records of 2026-11-24 (rosters, kit lines), 10,000 seasons per seed, every team's IL players back on ESPN's dates by the kit's room rule; the trade from week 7, Holmgren from week 12 (ESPN 2027-01-02).

**Verdict. The simulator was right; its inputs were illegal. It plays any roster it is handed, and one extra active player moved the owner's title share about 12.5 points, so trade arms with 11 or 14 active players read as huge losses or gains. `run_league_sim(active_limit=13)` now refuses such a roster before simulating; on legal rosters the trade reads +1.8 title points.**

Runner impact: code-only (`co_gm.run_league_sim` gains an optional `active_limit`, off by default; the package scan passes the league's 13; no morning step, record or prompt changes).

Pool rows touched: none

## 1. Diagnosis (2 seeds, title share)

| run | title | reading |
|---|---|---|
| base (13 active) | 21.6 / 22.0 | |
| base + Cameron Johnson as a 14th active player | 34.3 / 34.2 | one extra body, no drop: +12.5 |
| swap, Johnson on the roster with no active week | identical to the swap without him | the code paths match |

Real records never exceed the limit: every seat peaks at exactly 13 active in the brief's world and in the IL-return world with the room rule; the IL-return step's deliberate "room rule flipped" band plays 15 for every team, which is why the guard is opt-in.

## 2. The guard

`co_gm.active_limit()` reads the league's settings record (every roster position but IL: 13). `co_gm.over_active_limit()` lists each seat-week over it (a windowed player counts only inside his window). `run_league_sim(..., active_limit=N)` raises `RosterLimitError` naming the seat and week before any simulation. Tests (`scripts/test_sim_active_limit.py`, 4) written first: 4 errors before, all pass after. On its first live use it caught a second error in the session's own trade arm: the partner, taking two for one, kept 14 (he now cuts his lowest-value player, Jaime Jaquez Jr.).

## 3. The owner's trade on legal rosters (6 seeds, 2026-2031)

| arm | title vs no swap | final | partner's title |
|---|---|---|---|
| White + Lendeborg for Holmgren (Holmgren from week 12) | **+1.8** (seeds +1.2 to +2.3) | +1.5 | +0.9 |
| the same, Johnson in the open spot weeks 7-11 | +2.3 (+1.4 to +3.1) | +2.6 | +0.9 |
| Holmgren two weeks late (week 14), 4 seeds | +1.4 (+1.1 to +1.7) | +0.9 | |
| Holmgren never back and held all season, 4 seeds | -13.6 | -18.9 | |

Read: the trade costs regular-season categories while Holmgren is out (the session's phase model: about -0.9 categories over weeks 7 to 17) and gains in the playoffs, which the title share weighs; the verdict is conditional on his return (positive at week 12 or 14, sharply negative if he never plays and is held). Structural band (today's sweep): weekly_availability SENSITIVE, about -1.5 / +1.2 title points.

## 4. Correction

The session told the owner on 2026-11-24 "I wouldn't do White + Yaxel for Holmgren at this price", from a regular-season phase model, with no title figure. On legal rosters the title figure is +1.8, conditional on Holmgren's return. Logged in `report/corrections-log.md`.

## 5. Bounds

Out of scope by design: other trades (standing owner veto: only trades he composes are priced); turning the guard on in the morning steps.

In scope and unverified: whether the partner would cut Jaquez (the kit's lowest-value rule, not his choice).

## 6. Provenance

Session of 2026-11-24 (session model B, continuing the Main session; branch `claude/sim-active-limit`). Re-verify: `python3 -m unittest scripts.test_sim_active_limit`.
