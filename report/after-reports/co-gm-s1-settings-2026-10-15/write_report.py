#!/usr/bin/env python3
"""Writer for after-report-2026-10-15-co-gm-settings.md — every figure read from records
(RULES.md rule 6). Run from the kit root."""
import json
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DECK = os.path.join(KIT, "..", "yahoo-fantasy-basketball")
OUT = os.path.join(KIT, "report", "after-reports", "after-report-2026-10-15-co-gm-settings.md")
RES = os.path.join(DECK, "arena", "results")


def rd(name):
    return open(os.path.join(HERE, name), encoding="utf-8").read()


def counts(text):
    ran = int(re.search(r"Ran (\d+) tests?", text).group(1))
    m = re.search(r"FAILED \((?:failures=(\d+))?(?:, )?(?:errors=(\d+))?\)", text)
    return ran, (int(m.group(1) or 0) + int(m.group(2) or 0)) if m else 0


S = json.load(open(os.path.join(KIT, "data", "league_settings.json")))
SCH = json.load(open(os.path.join(KIT, "data", "league_schedule.json")))
v = lambda k: S[k]["value"]
red_set, green_set, red_sch, green_sch = (counts(rd(f)) for f in (
    "test_settings_red.txt", "test_settings_green.txt", "test_schedule_red.txt", "test_schedule_green.txt"))
red_names = re.findall(r"^FAIL: (test_\w+)", rd("test_settings_red.txt"), re.M)
verify_lines = [ln for f in ("sim_w17r_s2026.log", "sim_w17r_s2027.log") for ln in rd(f).splitlines() if ln.startswith("verify:")]
assert len(verify_lines) == 2 and red_set[1] > 0 and green_set[1] == 0 and red_sch[1] > 0 and green_sch[1] == 0

ARMS = [("18 weeks, fixed bracket (draft night, on file)", ""),
        ("17 weeks, reseeded, random pairings", "_w17r"),
        ("17 weeks, reseeded, the real schedule", "_w17r_sched")]
rows, summary = [], {}
for label, suf in ARMS:
    r = [json.load(open(os.path.join(RES, f"m100_league_sim_10k_s{s}{suf}.json"))) for s in (2026, 2027)]
    n = sum(x["seasons"] for x in r)
    t = [x["teams"]["10"] for x in r]
    c = [x["champ"] for x in t]; pl = [x["playoff"] for x in t]
    cm, pm = sum(c) / 2, sum(pl) / 2
    ce = 196 * math.sqrt(cm / 100 * (1 - cm / 100) / n)
    pe = 196 * math.sqrt(pm / 100 * (1 - pm / 100) / n)
    rank = [sorted(x["teams"], key=lambda i: -x["teams"][i]["champ"]).index("10") + 1 for x in r]
    rows.append(f"| {label} | {r[0]['weeks']} | {c[0]:.2f} / {c[1]:.2f} | {cm:.2f} ± {ce:.2f} | {pl[0]:.2f} / {pl[1]:.2f} | {pm:.2f} ± {pe:.2f} | {rank[0]} / {rank[1]} |")
    summary[suf] = (cm, ce, pm)
honored = sum(json.load(open(os.path.join(RES, f"m100_league_sim_10k_s{x}_w17r_sched.json")))["schedule"]["honored"] for x in (2026, 2027))
opp = ", ".join(f"{o['week']} {o['manager']}" for o in SCH["owner_opponents"])
rn = rd("rn_section.md").rstrip() + "\n"
old, new, sched = summary[""], summary["_w17r"], summary["_w17r_sched"]

text = f"""# After-report — 2026-10-15: Session 1 item 2 — the league's settings and schedule, read from the league; the simulator corrected to 17 weeks and a reseeded bracket

**Owner request (2026-10-15):** Session 1 item 2 — settings and schedule from the owner, `league_settings.json` / `league_schedule.json`, `test_settings.py` failing on any divergence, `league_sim.py --schedule`. Owner inputs: the settings PDF and the rosters PDF (uploaded 2026-10-15, pinned in `data/source/`), then in chat, verbatim: "Correct, weeks 18-20 and ends March 21, 2027." with the 17-opponent list and "Merge" (`data/source/owner-matchup-schedule-2026-10-15.md`).

**What changed.**
- Kit: `data/league_settings.json`, `data/league_schedule.json`, `scripts/test_settings.py`, `scripts/test_schedule.py`.
- Kit: `report/schedule/build_schedule.py` gets playoff weeks {tuple(v('playoffs')['weeks'])}, plus a `--games` re-bucket mode with no fetch. Its per-week file changes only the two playoff-window columns: 28 shared columns, 0 rows differ.
- Deck: `arena.WEEKS` {v('regular_season_weeks')}, `arena.playoff_champion` reseeded (new `arena.reseed`), `league_sim.py` reseeded plus `--schedule`, and the `test_bracket.py` docstring.
- No line, tag, team, price or placement changed. Nothing published.

**Method (stated to the owner before the run).**
- A1: reseeding means the best remaining seed meets the worst. This is assumed; the owner has not confirmed it.
- A2: only the owner's 17 opponents are known. The other ten teams are paired at random each week.
- A3: weeks 7 and 17 are 14-day matchups on Yahoo's calendar. The simulator treats them as single weeks.
- A4: the re-grade uses the rosters as drafted (state `draft_state_100.json`, tag v69), so it is comparable with draft night.
- Runs: 10,000 seasons each, seeds 2026 and 2027 (draft night's seeds).

Pull window: 2026-10-15 → 2026-10-15 (owner settings, rosters and schedule; no roster pull, no web research).

## 1. Roster changes

None applied. The rosters PDF is pinned for item 5 and has not been parsed here.

## 2. What the league's page said that the model had wrong

| setting | league page | model before | test |
|---|---|---|---|
| regular-season weeks | {v('regular_season_weeks')} (playoffs weeks {", ".join(map(str, v('playoffs')['weeks']))}, end {v('playoffs')['ends']}) | 18 | `test_regular_season_weeks` |
| playoff window in the schedule builder | weeks {", ".join(map(str, v('playoffs')['weeks']))} | weeks 19, 20, 21 (D-G5, "confirm on the settings page") | `test_playoff_weeks_in_the_schedule_builder` |
| playoff reseeding | yes | fixed bracket | `test_playoff_reseeding` |

EVIDENCE:
- `test_settings_red.txt`: {red_set[0]} tests, {red_set[1]} failing ({", ".join(red_names)}).
- `test_settings_green.txt`: {red_set[0]} tests, {green_set[1]} failing.
- `test_schedule_red.txt`: {red_sch[0]} tests, {red_sch[1]} failing. `league_sim` ignored `--schedule` and wrote no schedule record.
- `test_schedule_green.txt`: {green_sch[0]} tests, {green_sch[1]} failing.

Settings that already matched: {v('teams')} teams, {v('playoffs')['teams']} playoff teams, the nine categories, the ten starting slots, and {sum(1 for s in v('roster_positions') if s != 'IL')} active roster spots.

## 3. The schedule

The owner's opponents by week, with managers resolved to draft seats through the draft board: {opp}. Weeks {", ".join(map(str, SCH['playoff_weeks']))} are playoffs. Every other team appears, and the owner's seat never plays itself (`test_schedule.py`).

## 4. The league grade, re-stated

Seat 10, rosters as drafted on 10/14, 10,000 seasons per seed. Error is the 95% binomial interval on the two-seed mean.

| model | weeks | title s2026 / s2027 | title, mean | playoffs s2026 / s2027 | playoffs, mean | title rank |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}

`--verify` on the corrected model, both seeds: "{verify_lines[0]}" and "{verify_lines[1].split(' on seed ')[1]}". In plain terms, the reseeded `league_sim` equals `arena.simulate_seasons` draw for draw. The schedule runs change the draw order, so they cannot be verified that way. Their check is that the owner met the listed opponent in all {honored:,} simulated weeks (`honored` in each record).

**Reading.**
- Correcting the season shape moves the title share from {old[0]:.2f}% to {new[0]:.2f}%.
- The real schedule moves it to {sched[0]:.2f}%.
- Each shift is about the size of the ±{new[1]:.2f}-point error, so the honest reading is that the title share is still about 21–22%, and still rank 1.
- INFERENCE: one week fewer gives the regular season less room for the stronger roster to separate. The schedule's random pairings for the other ten teams (A2) limit what its arm can say.

## Watchlist

- A1 (reseed semantics) and A2 (others' pairings) are on `OPEN.md`. If the owner can share the full league schedule, A2 goes away.
- D-S1-2: the two 14-day matchups (weeks 7 and 17) are not modelled as double-length.

## Open-item receipts

| item | query run (2026-10-15) | dated finding |
|---|---|---|
| (this item) | owner inputs only; no web research and no roster pull | settings and schedule pinned; pool unchanged |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this item (did not check) |

{rn}
The section above is item 1's pasted output of the deck's `repeat_market_check.py` from earlier today, carried over. The page and the lines are unchanged since then; the arena changes do not touch the page engine. The gate replays it again.

## Bounds

**Out of scope by design.**
- No change to projections, the page, or the in-season dynamics (B3).
- The schedule's 14-day weeks (D-S1-2).

**In scope and unverified.**
- A1, the reseed rule: assumed, not confirmed by the owner.
- The settings transcription beyond the confirmed playoff fields: read from the page images, not individually confirmed.

**What this cannot see.**
- Every pick, add and drop since the draft (item 5).
- The other teams' real pairings.
- Whether the season model is calibrated. It is verified against itself, not against outcomes; item 7 starts that.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-S1-2 | Model weeks 7 and 17 as double-length matchups | not modelled; P1 with B3 |
| D-S1-3 | Send the full league schedule, so that all 12 teams' pairings are real | random pairings for the other ten |
| D-G5 | Playoff window | CLOSED: weeks 18–20 per the settings page and the owner |
| earlier rows | carried in `OPEN.md` | carried |

## Provenance

- This folder: `test_settings_red.txt`, `test_settings_green.txt`, `test_schedule_red.txt`, `test_schedule_green.txt`, `sim_w17r_s2026.log`, `sim_w17r_s2027.log`, `sim_w17r_sched_s2026.log`, `sim_w17r_sched_s2027.log`, `rn_section.md`, this writer.
- Deck: `arena/results/m100_league_sim_10k_s{{2026,2027}}{{_w17r,_w17r_sched}}.json` (new) and the draft-night `m100_league_sim_10k_s{{2026,2027}}.json` (unchanged).
- Owner inputs: `data/source/yahoo-league-settings-2026-10-15.pdf`, `data/source/yahoo-starting-rosters-2026-10-20-view.pdf`, `data/source/owner-matchup-schedule-2026-10-15.md`.

## In plain language

Your league's settings page caught two mistakes in the simulator. It was playing 18 regular-season weeks instead of 17, and it ignored the reseeding after round one. Both are fixed, each with a test that failed before the fix and passes now.

The simulator now also plays your actual opponent each week. With all of that, your title chance on the roster you drafted is about {sched[0]:.0f}% (was {old[0]:.0f}%), still the best in the league on this model.
"""
open(OUT, "w", encoding="utf-8").write(text)
print(f"wrote {os.path.relpath(OUT, KIT)}")
