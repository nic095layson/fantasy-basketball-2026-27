#!/usr/bin/env python3
"""Matchup live (owner 2026-10-20: "1, 2, 5 build", item 2). Extracts the newest FantasyBot
get_matchup_outlook response from the session transcript, pins it under data/source/fantasybot/,
and records the NEUTRAL facts for the Week tab: games left both sides, games-in-progress flag,
and each side's starter games-left. FantasyBot's own verdict ("Projected 2-7-0, 7% to win") is
kept in the pinned raw JSON as data but is never shown on the deck and never evaluates anything
(owner rule 2026-10-20; the kit's simulator owns p(win)). Verified 2026-10-20: the pre-game
response carries NO per-category live score (plan-gate A6) — if in-game pins later show real
tallies, wiring them is a separate, flagged step.

    python3 scripts/matchup_live.py --date 2026-10-20 [--transcript FILE | --pull FILE]
Writes data/news/matchup_live_<date>.json; non-fatal in the morning run.
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from league_live import LEAGUE, TRANSCRIPTS, PullError, _loads, newest_transcript  # noqa: E402

PIN_DIR = os.path.join(KIT, "data", "source", "fantasybot")
OUTDIR = os.path.join(KIT, "data", "news")


def extract_outlook(transcript):
    """The LAST get_matchup_outlook response naming this league in the transcript."""
    found = None

    def walk(x):
        nonlocal found
        if isinstance(x, str):
            if '"leagueName"' in x and LEAGUE in x and '"myLeftToPlay"' in x:
                j = _loads(x)
                if isinstance(j, dict) and "myLeftToPlay" in j:
                    found = j
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    with open(transcript, encoding="utf-8") as f:
        for line in f:
            if LEAGUE not in line or "myLeftToPlay" not in line:
                continue
            o = _loads(line)
            if o is not None:
                walk(o)
    return found


def record(outlook):
    """The neutral facts only; the FantasyBot verdict stays in the pin, not here."""
    if outlook.get("leagueName") != LEAGUE:
        raise PullError(f"league name {outlook.get('leagueName')!r} is not {LEAGUE!r}")
    g = lambda side: [{"player": p["name"], "team": p.get("team"), "games_left": p.get("gamesLeft"),
                       "state": p.get("gameState")} for p in outlook.get(side) or []]
    return {"week": outlook.get("week"), "my_team": outlook.get("myTeamName"), "opp_team": outlook.get("oppTeamName"),
            "my_left_to_play": outlook.get("myLeftToPlay"), "opp_left_to_play": outlook.get("oppLeftToPlay"),
            "games_in_progress": bool(outlook.get("gamesInProgress")), "final": bool(outlook.get("final")),
            "live_scoring": bool(outlook.get("liveScoring")),
            "my_starters": g("myStarters"), "opp_starters": g("oppStarters")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--transcript")
    ap.add_argument("--pull", help="a saved outlook JSON instead of a transcript")
    ap.add_argument("--out-dir", default=OUTDIR)
    ap.add_argument("--pin-dir", default=PIN_DIR)
    a = ap.parse_args()
    try:
        if a.pull:
            outlook = json.load(open(a.pull, encoding="utf-8"))
        else:
            outlook = extract_outlook(a.transcript or newest_transcript())
        if outlook is None:
            raise PullError("no get_matchup_outlook response in the transcript")
        rec = record(outlook)
    except (PullError, OSError, KeyError) as e:
        print(f"MATCHUP LIVE: HALT — {e}; no record written")
        return 1
    os.makedirs(a.pin_dir, exist_ok=True)
    pin = os.path.join(a.pin_dir, f"outlook_{a.date}.json")
    with open(pin, "w", encoding="utf-8") as f:
        json.dump(outlook, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    rec["date"] = a.date
    rec["pin"] = {"file": os.path.relpath(pin, KIT),
                  "sha256": hashlib.sha256(open(pin, "rb").read()).hexdigest()}
    os.makedirs(a.out_dir, exist_ok=True)
    out = os.path.join(a.out_dir, f"matchup_live_{a.date}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"MATCHUP LIVE: PASS — week {rec['week']}, games left {rec['my_left_to_play']} mine / "
          f"{rec['opp_left_to_play']} {rec['opp_team']}; wrote {os.path.relpath(out, KIT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
