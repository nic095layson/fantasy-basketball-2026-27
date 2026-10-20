#!/usr/bin/env python3
"""League moves (owner 2026-10-20, item 2 of the FantasyBot build): who added, dropped, or moved
whom to or from IL since the previous league state. Teams match by seat, so a team rename (KEVIN
ELEVEN DOUBLES) is not a roster move. Record only: nothing here changes a line, a tag, or a roster.

    python3 scripts/league_moves.py --old OLD.json --new NEW.json --date YYYY-MM-DD
Writes data/news/league_moves_<date>.json; the daily brief reads it.
"""
import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
OUTDIR = os.path.join(KIT, "data", "news")


def _team(t):
    """(rostered names incl. unpooled IL, names in an IL slot)."""
    names = {p["player"] for p in t["players"]} | set(t.get("unpooled_il") or [])
    il = {p["player"] for p in t["players"] if p["slot"] == "IL"} | set(t.get("unpooled_il") or [])
    return names, il


def diff(old, new):
    """Per-seat moves between two league states; a team appears only if something changed."""
    old_by = {t["seat"]: t for t in old["teams"]}
    moves = []
    for t in new["teams"]:
        o = old_by.get(t["seat"])
        if o is None:
            continue
        on, oil = _team(o)
        nn, nil_ = _team(t)
        m = {"team": t["name"], "seat": t["seat"],
             "added": sorted(nn - on), "dropped": sorted(on - nn),
             "to_il": sorted((nil_ - oil) & on & nn), "from_il": sorted((oil - nil_) & on & nn)}
        if any(m[k] for k in ("added", "dropped", "to_il", "from_il")):
            moves.append(m)
    return moves


def write_record(old, new, date, out=None):
    rec = {"date": date, "old_as_of": old["as_of"], "new_as_of": new["as_of"], "moves": diff(old, new)}
    out = out or os.path.join(OUTDIR, f"league_moves_{date}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return rec, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--old", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--date", required=True)
    a = ap.parse_args()
    old = json.load(open(a.old, encoding="utf-8"))
    new = json.load(open(a.new, encoding="utf-8"))
    rec, out = write_record(old, new, a.date)
    n = sum(len(m["added"]) + len(m["dropped"]) + len(m["to_il"]) + len(m["from_il"]) for m in rec["moves"])
    print(f"LEAGUE MOVES: PASS — {len(rec['moves'])} team(s) changed, {n} move(s), "
          f"{old['as_of']} to {new['as_of']}; wrote {os.path.relpath(out, KIT)}")


if __name__ == "__main__":
    main()
