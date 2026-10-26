#!/usr/bin/env python3
"""The league's real schedule for all 12 teams, and the weeks already final, compiled into data/league_schedule.json
for the deck's season simulator (owner 2026-10-26, "full pairings + results so far").

Until now the schedule file carried only the owner's 17 opponents (owner message 2026-10-15) and the simulator paired
the other ten teams at random each week, and every simulated season started 0-0. Yahoo publishes every week's
pairings in advance; the morning runner's Flaim get_matchups responses for weeks 1..17 are pinned raw by
`flaim_live.py --history` under data/source/flaim/pairings/<league>/matchups_weekNN.json. This script reads those pins,
maps Yahoo team ids to the kit's draft seats by team name through data/league_state.json, and writes:

  pairings   {week: [[seatA, seatB] x 6]}   every regular-season week, every team once
  played     {week: {seat: [wins, losses, ties]}}   from data/weeks/week_N.json (scoreboard_intake), the weeks final

and checks the owner's listed opponents against Yahoo week for week: a contradiction is a PairingsError, never a
silent overwrite. Nothing is typed in; nothing else in the schedule file changes.

    python3 scripts/league_pairings.py [--schedule PATH] [--pins DIR] [--weeks DIR] [--state PATH] [--ledger PATH|'']
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
KIT = os.path.dirname(HERE)
SCHEDULE = os.path.join(KIT, "data", "league_schedule.json")
PINS = os.path.join(KIT, "data", "source", "flaim", "pairings", "478.l.36464")
WEEKS = os.path.join(KIT, "data", "weeks")
STATE = os.path.join(KIT, "data", "league_state.json")


class PairingsError(Exception):
    pass


def seat_map(state):
    """Yahoo team name -> draft seat, from the league state the intake builds every morning."""
    return {t["name"]: t["seat"] for t in state["teams"]}


def week_pairs(resp, seats):
    """One week's matchups as seat pairs; every team exactly once or PairingsError."""
    pairs, seen = [], []
    for m in resp.get("matchups") or []:
        try:
            a, b = seats[m["home"]["teamName"]], seats[m["away"]["teamName"]]
        except KeyError as e:
            raise PairingsError(f"week {resp.get('matchupWeek')}: team {e} is not in the league state")
        pairs.append([a, b]); seen += [a, b]
    if sorted(seen) != sorted(seats.values()):
        raise PairingsError(f"week {resp.get('matchupWeek')}: {len(pairs)} matchup(s) cover seats {sorted(seen)}, "
                            f"not all of {sorted(seats.values())}")
    return pairs


def compile(sched, pins, weeks_dir, state):
    """The schedule with pairings and played weeks added; the owner's listed opponents checked against the pins."""
    seats = seat_map(state)
    n_weeks = int(sched["regular_season_weeks"])
    pairings, srcs = {}, []
    for p in sorted(glob.glob(os.path.join(pins, "matchups_week*.json"))):
        resp = json.load(open(p, encoding="utf-8"))
        w = int(resp.get("matchupWeek") or 0)
        if not 1 <= w <= n_weeks:
            continue
        pairings[str(w)] = week_pairs(resp, seats); srcs.append(os.path.relpath(p, KIT) if p.startswith(KIT) else p)
    missing = [w for w in range(1, n_weeks + 1) if str(w) not in pairings]
    if missing:
        raise PairingsError(f"no pinned matchups for week(s) {missing}")
    owner = sched["owner_seat"]
    for o in sched.get("owner_opponents") or []:
        w = str(o["week"])
        opp = next((b if a == owner else a for a, b in pairings[w] if owner in (a, b)), None)
        if opp != o["seat"]:
            raise PairingsError(f"week {w}: the schedule lists seat {o['seat']} as the owner's opponent, Yahoo pairs seat {opp}")
    played = {}
    for p in sorted(glob.glob(os.path.join(weeks_dir, "week_*.json"))):
        m = re.fullmatch(r"week_(\d+)\.json", os.path.basename(p))
        if not m:
            continue
        rec = json.load(open(p, encoding="utf-8"))
        w = str(int(m.group(1)))
        played[w] = {}
        for name, t in (rec.get("teams") or {}).items():
            ys = t.get("yahoo_score") or {}
            if not all(k in ys for k in ("wins", "losses", "ties")):
                raise PairingsError(f"week {w}: {name} carries no yahoo_score")
            played[w][str(t["seat"])] = [int(ys["wins"]), int(ys["losses"]), int(ys["ties"])]
        if sorted(int(s) for s in played[w]) != sorted(seats.values()):
            raise PairingsError(f"week {w}: played records cover seats {sorted(played[w])}, not every team")
    out = dict(sched)
    out["pairings"] = dict(sorted(pairings.items(), key=lambda kv: int(kv[0])))
    out["pairings_source"] = dict(files=srcs, weeks=len(pairings), seat_map="team name -> seat through data/league_state.json")
    out["owner_opponents_check"] = "match"
    out["played"] = dict(sorted(played.items(), key=lambda kv: int(kv[0])))
    return out


def main():
    import argparse
    import run_ledger
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--schedule", default=SCHEDULE); ap.add_argument("--pins", default=PINS)
    ap.add_argument("--weeks", default=WEEKS); ap.add_argument("--state", default=STATE)
    ap.add_argument("--ledger", default=run_ledger.LEDGER, help="run-ledger for the row ('' to skip)")
    a = ap.parse_args()
    try:
        sched = json.load(open(a.schedule, encoding="utf-8"))
        out = compile(sched, a.pins, a.weeks, json.load(open(a.state, encoding="utf-8")))
    except (PairingsError, OSError, ValueError, KeyError) as e:
        msg = f"LEAGUE PAIRINGS: FAIL — {e}"
        print(msg)
        if a.ledger:
            run_ledger.record("league pairings", "FAIL", msg, ledger=a.ledger)
        return 1
    with open(a.schedule, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False); f.write("\n")
    msg = (f"LEAGUE PAIRINGS: PASS — {out['pairings_source']['weeks']} weeks of pairings for all {len(seat_map(json.load(open(a.state, encoding='utf-8'))))} teams, "
           f"owner opponents {out['owner_opponents_check']}, {len(out['played'])} week(s) played; wrote {os.path.relpath(a.schedule, KIT) if a.schedule.startswith(KIT) else a.schedule}")
    print(msg)
    if a.ledger:
        run_ledger.record("league pairings", "PASS", msg, ledger=a.ledger)
    return 0


if __name__ == "__main__":
    sys.exit(main())
