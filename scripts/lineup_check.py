#!/usr/bin/env python3
"""The 3 PM lineup check (owner 2026-10-22): "if I have any players that are eligible to play but are on my Bench,
send me a notification ... if there is a player on my starting lineup who is much worse, notify me to make this
roster change."

Reads the same records as week_matchup.py (the afternoon league state with Yahoo's slots, today's schedule, the status
file, the season pool, the week's to-date) and compares Yahoo's slots with the best ten-slot fill of today's games.
A move is notified when:
  - a slot is empty: a bench player has a game today and the starter he replaces has none, is Out, or the slot is open;
  - a starter is worse: both play today, and the bench player's season value per game beats his by LINEUP_GAP (1.0)
    or more, or starting the bench player today adds LINEUP_D_EXP (0.05) or more expected categories won this week
    against the opponent (the week card's model, today's swap only, the rest of the week unchanged).

Prints one LINEUP CHECK line (ALERT with each move, or OK) and the push text on the next line when there is an alert;
writes data/news/lineup_<date>.json. Changes no value.

    python3 scripts/lineup_check.py --date <UTC date> [--state ...] [--yahoo-pull ...]
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import co_gm as CG  # noqa: E402
import week_matchup as WM  # noqa: E402

NEWS = os.path.join(CG.KIT, "data", "news")


def describe(m, teams):
    who = f"Start {m['start']} ({teams.get(m['start'], '?')})"
    if m["sit"] is None:
        return f"{who} in an open slot"
    if m["kind"] == "empty":
        return f"{who} for {m['sit']}, who has no game today or is Out"
    return (f"{who} for {m['sit']}: season value {'+' if m['gap'] >= 0 else '−'}{abs(m['gap']):.2f}, "
            f"this week {'+' if m['d_exp'] >= 0 else '−'}{abs(m['d_exp']):.2f} expected categories")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", required=True)
    ap.add_argument("--out-dir", default=NEWS)
    ap.add_argument("--state", default=CG.STATE); ap.add_argument("--schedule", default=CG.SCHEDULE)
    ap.add_argument("--games", default=CG.GAMES); ap.add_argument("--actuals", default=WM.ACTUALS)
    ap.add_argument("--status-dir", default=WM.STATUS)
    ap.add_argument("--yahoo-pull", help="the Flaim pull (default data/source/flaim/pull_<date>.json)")
    a = ap.parse_args()
    pull = a.yahoo_pull or os.path.join(WM.PULLS, f"pull_{a.date}.json")
    try:
        rec = WM.build(a.date, dict(state=a.state, schedule=a.schedule, games=a.games, actuals=a.actuals,
                                    status=a.status_dir, yahoo_pull=pull))
    except Exception as e:  # noqa: BLE001 — one FAIL line; the runner reports it and goes on
        print(f"LINEUP CHECK: FAIL — {a.date}: {type(e).__name__}: {e}")
        return 1
    L = rec["lineup_today"]
    state = json.load(open(a.state, encoding="utf-8"))
    me = next(t for t in state["teams"] if t["seat"] == CG.OWNER_SEAT)
    teams = {p["player"]: p["yahoo_nba_team"] for p in me["players"]}
    out = dict(date=a.date, opponent=rec["opponent"]["name"], league_state_as_of=rec["league_state_as_of"],
               status_file=rec["status_file"], games_today=L["games_today"], moves=L["moves"], alerts=L["alerts"],
               slots=L["slots"], gap=L["gap"], d_exp=L["d_exp"], exp_cats=rec["exp_cats"])
    os.makedirs(a.out_dir, exist_ok=True)
    path = os.path.join(a.out_dir, f"lineup_{a.date}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False); f.write("\n")
    rel = os.path.relpath(path, CG.KIT) if path.startswith(CG.KIT) else path
    if L["alerts"]:
        lines = [describe(m, teams) for m in L["alerts"]]
        print(f"LINEUP CHECK: ALERT — {a.date}: {len(lines)} move(s): " + "; ".join(lines) + f"; wrote {rel}")
        print("PUSH: Lineup — " + "; ".join(lines))
    else:
        why = ("no bench player of yours plays today, or Yahoo's lineup already starts the best who do" if not L["moves"]
               else f"{len(L['moves'])} swap(s) under both bars")
        print(f"LINEUP CHECK: OK — {a.date}: no move ({why}); wrote {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
