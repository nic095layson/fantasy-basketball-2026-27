#!/usr/bin/env python3
"""Writer for after-report-2026-10-15-co-gm-daily-brief.md — figures read from records."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(KIT, "report", "after-reports", "after-report-2026-10-15-co-gm-daily-brief.md")
rd = lambda n: open(os.path.join(HERE, n), encoding="utf-8").read()
def counts(t):
    ran = int(re.search(r"Ran (\d+) tests?", t).group(1)); m = re.search(r"FAILED \((?:failures=(\d+))?(?:, )?(?:errors=(\d+))?\)", t)
    return ran, (int(m.group(1) or 0) + int(m.group(2) or 0)) if m else 0
b = json.load(open(os.path.join(KIT, "report", "briefs", "brief_2026-10-21.json"), encoding="utf-8"))
assert "ModuleNotFoundError" in rd("test_daily_brief_red.txt")
sr, g = counts(rd("test_streaming_red.txt")), counts(rd("test_daily_brief_green.txt"))
t = b["title"]; n = b["seasons"]; m = (t["2026"] + t["2027"]) / 2; e = 196 * (m / 100 * (1 - m / 100) / (2 * n)) ** 0.5
playing = sum(1 for r in b["today"] if r[2]); started = len(b["lineup"])
note = open(os.path.join(KIT, "report", "briefs", "brief_2026-10-21.md"), encoding="utf-8").read()
top = b["waiver_top"]
rn = rd("rn_section.md").rstrip() + "\n"
text = f"""# After-report — 2026-10-15: Session 1 item 6 — the daily brief, run for {b['date']}

**Owner request:** Session 1 item 6: "scripts/daily_brief.py: for today — the owner's players with games, the lineup by the daily-fill rule, the waiver scan (waiver_moves.py against league_state.json), streaming candidates by games remaining this week, title odds on the real schedule (10,000 seasons, two seeds, error stated). One markdown note. Run it for 10/21 and show the owner the note." The owner set the date as 10/21.

**What changed.**
- Kit: `scripts/co_gm.py` (the library: league-state rosters, the daily lineup, games left, the waiver scan lifted from `waiver_moves.py`, the simulator bridge), `scripts/daily_brief.py`, `scripts/test_daily_brief.py`, `report/briefs/brief_{b['date']}.md` and `.json`.
- No line, tag, team, price or placement changed. Nothing published.

**Method (stated to the owner before the run).**
- **Inputs:** NBA games from `games-2026-27.csv` (Basketball-Reference, built 9/30); lines {b['lines']}; availability from `{b['status_file']}`.
- **Waiver scan:** the top 40 free agents by board value (inherited from `waiver_moves.py`, stated) × the owner's non-IL players. The top 3 distinct adds go to the simulator on seed 2026, {n:,} seasons, real schedule.
- **Title odds:** {n:,} seasons × seeds 2026 / 2027.

Pull window: 2026-10-15 → 2026-10-15 (the brief for {b['date']}, built on the 2026-10-15 records; no web research — the sports hosts are denied).

## 1. Roster changes

None.

## 2. The note

{note}

## 3. Verification

- **Tests, red first:**
  - `test_daily_brief_red.txt`: the module was missing.
  - `test_streaming_red.txt`: {sr[0]} tests, {sr[1]} error.
  - `test_daily_brief_green.txt`: {g[0]} tests, {g[1]} failing.
- **The lineup test was sharpened before any code existed:** the case is one that slot-order greedy loses (a PG/SG star plus four pure PGs: greedy starts 4, the matching starts 5).
- **Caught in my own review of the first run** (`brief_2026-10-21_first_run.md`):
  - **What was wrong:** the streaming list ranked by a value clamped at zero. Every free agent sits below the pool mean, so the list was in arbitrary order.
  - **Fix:** rank free agents with more games left than the owner's weakest active player by per-game value. Red-first.
  - **Result for 10/21:** no free agent has more games left this week than the weakest player, so the section correctly says "none".
- **Lineup:** {playing} of the owner's non-IL players play on {b['date']}, and {started} start.
- **Title odds:** {m:.1f}% ± {e:.1f} (seeds {t['2026']:.2f}% / {t['2027']:.2f}%).

## Watchlist

- **The waiver result is the brief's one actionable item:**
  - **The pairs:** {', '.join(f"add {x['add']} for {x['drop']} ({x['d_ecw']:+.3f} cats/week; title {x['d_title_seed2026']:+.2f} points on one seed)" for x in top)}.
  - **This is an open decision:** draft-night D-LD-2, defaulting to watching Green's first week.
  - **The +2.57-point figure is one seed;** a second seed confirms or shrinks it before anyone acts.
- The schedule file predates the Cup knockout dating (week 7); week 1 is unaffected.

## Open-item receipts

| item | query run (2026-10-15) | dated finding |
|---|---|---|
| (this item) | records only (league state, status file, schedule file); no web research (network-denied) | brief written |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried (network blocked) |

{rn}
The section above is carried from item 1's run today; the page is unchanged, and the gate replays it.

## Bounds

**Out of scope by design.**
- Automating the run at 9am ET (P1).
- Trades.

**In scope and unverified.**
- The brief runs on the 10/15 rosters and statuses. On 10/21 itself it needs a fresh paste to be current.

**What this cannot see.**
- News after the paste.
- ESPN injuries.
- Minutes limits.
- Other managers' pending claims.
- FAB budgets.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-LD-2 (carried) | Add Draymond Green for Christian Braun now, or watch week 1 | watch week 1; the brief re-scores it daily |
| D-S1-9 | Re-run the brief on 10/21 morning after a fresh rosters/status paste | yes, if you paste |
| earlier rows | carried in `OPEN.md` | carried |

## Provenance

This folder: `test_daily_brief_red.txt`, `test_streaming_red.txt`, `test_daily_brief_green.txt`, `brief_2026-10-21_first_run.md`, `rn_section.md`, this writer. Kit: `report/briefs/brief_{b['date']}.md`, `.json`.

## In plain language

The daily note works. For 10/21 it starts your ten players who have games. It flags Durant, Irving and Bridges as questionable to check before tip-off.

The waiver scan's best move is Draymond Green in for Christian Braun, worth about +2.6 points of title odds on one simulation run. That's still your call from draft night.

Your title odds on today's rosters are about {m:.0f}%.
"""
open(OUT, "w", encoding="utf-8").write(text); print("wrote", os.path.relpath(OUT, KIT))
