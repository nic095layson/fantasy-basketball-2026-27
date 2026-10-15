#!/usr/bin/env python3
"""Writer for after-report-2026-10-15-co-gm-weekly.md — figures read from records."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(KIT, "report", "after-reports", "after-report-2026-10-15-co-gm-weekly.md")
rd = lambda n: open(os.path.join(HERE, n), encoding="utf-8").read()
g = re.search(r"Ran (\d+) tests", rd("test_weekly_green.txt")).group(1)
assert "ModuleNotFoundError" in rd("test_weekly_red.txt") and "OK" in rd("test_weekly_green.txt")
refused = [l for l in rd("record_week1_again_refused.txt").splitlines() if "LedgerError" in l][0]
w = json.load(open(os.path.join(KIT, "report", "calibration.json"), encoding="utf-8"))["weeks"]["1"]
prev = open(os.path.join(KIT, "report", "previews", "week_01.md"), encoding="utf-8").read()
h = json.load(open(os.path.join(KIT, "report", "after-reports", "co-gm-s1-league-state-2026-10-15", "h2h_assessment_2026-10-15.json")))["rows"][0]
same = abs(h["s2026"]["p_win"] - w["by_seed"]["2026"]["p_win"]) < 1e-12 and abs(h["s2027"]["p_win"] - w["by_seed"]["2027"]["p_win"]) < 1e-12
rn = rd("rn_section.md").rstrip() + "\n"
text = f"""# After-report — 2026-10-15: Session 1 item 7 — the weekly preview and the calibration ledger, week 1 recorded before the week

**Owner request:** Session 1 item 7: "scripts/weekly_preview.py (the real opponent, category by category) and calibration.md/calibration.json with week 1's predicted category-win probabilities recorded before the week." The owner said "Proceed".

**What changed.**
- Kit: `scripts/weekly_preview.py`, `scripts/test_weekly.py`, `report/previews/week_01.md`, `report/calibration.json`, `report/calibration.md`.
- No line, tag, team, price or placement changed. Nothing published.

**Method (stated to the owner before the run, as the 2026-10-15 assessment).**
- Non-IL rosters from the league state, on lines {w['lines']}.
- `arena.team_week_model` with the house simulator's weekly draw.
- {w['n_per_seed']:,} matchups × seeds {w['seeds'][0]} / {w['seeds'][1]}.

Pull window: 2026-10-15 → 2026-10-15 (records only; no web research).

## 1. Roster changes

None.

## 2. Week 1, recorded {w['recorded_at']} (the week starts {w['week_start']})

{prev}

## 3. Verification

- **Tests, red first:** `test_weekly_red.txt` (module missing), then `test_weekly_green.txt` ({g} tests, OK).
- **What the tests prove:** a recorded week cannot be rewritten; a prediction dated on or after the week's start is refused; the Brier arithmetic is checked against a hand-written formula.
- **The real ledger, driven red:** recording week 1 a second time returns `{refused}` (`record_week1_again_refused.txt`).
- **Agreement with the owner's earlier assessment:** week 1's per-seed P(win) equals `h2h_assessment_2026-10-15.json` exactly: {same}. Same method, same seeds.

## Watchlist

- **Score week 1 after Sunday 10/25:** `weekly_preview.py --score 1 --won "<the categories won>"` from the owner's scoreboard paste.
- **Week 1 is six days (Oct 20–25), but the model's weekly means are a standard week.** Category win probabilities depend on both sides alike, so the effect is second-order. The ledger will show it.

## Open-item receipts

| item | query run (2026-10-15) | dated finding |
|---|---|---|
| (this item) | records only | week 1 recorded |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried (network blocked) |

{rn}
The section above is carried from item 1's run today; the page is unchanged, and the gate replays it.

## Bounds

**Out of scope by design.**
- Player-level projected-vs-actual lines (plan B6's second half, P1).
- Monthly reports.

**In scope and unverified.**
- Q/O statuses are not applied to the weekly model.
- The short week 1 is modelled as a full week.

**What this cannot see.**
- Lineup moves.
- Streaming.
- Injuries during the week.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-S1-10 | Paste week 1's final scoreboard on 10/26 so the ledger can score it | requested |
| D-S1-11 | Apply status tiers to the weekly model (P1, with B3) | P1 |
| earlier rows | carried in `OPEN.md` | carried |

## Provenance

This folder: `test_weekly_red.txt`, `test_weekly_green.txt`, `record_week1.txt`, `record_week1_again_refused.txt`, `rn_section.md`, this writer.

## In plain language

Before week 1 begins, the system has written down its prediction: a {w['p_win']:.0%} chance you beat Cayas, winning blocks, turnovers, field-goal % and rebounds and losing assists, points and threes. That record is locked, so it can't be changed after the fact.

When you send the final scoreboard, it grades itself. That's the first test of the model against real games rather than against itself.
"""
open(OUT, "w", encoding="utf-8").write(text); print("wrote", os.path.relpath(OUT, KIT))
