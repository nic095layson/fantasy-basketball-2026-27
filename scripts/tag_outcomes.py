#!/usr/bin/env python3
"""Injury-tag outcomes (owner 2026-10-27, build 4, "capture now"): what every player flagged in a day's status file
then did in that day's games — played (with his minutes against his season norm), sat, or his NBA team had no game —
appended to data/status/tag_outcomes.jsonl, one line per flagged player per day, a day never rewritten. Capture only:
nothing here changes a tier, a line or a constant. The weekly accuracy card and a later fit read it.

The status file is the day's (data/status/status_<date>.json, built that morning); the games are that date's box
record (data/actuals/<date>.json, pulled the next morning); the NBA team and the season minutes norm come from the
season projections (data/season/projections_season.csv: team, mpg). A flagged player with no team on file is
recorded as unresolved, never guessed.

    python3 scripts/tag_outcomes.py --date 2026-10-25 [--out data/status/tag_outcomes.jsonl]
"""
import argparse
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
STATUS = os.path.join(KIT, "data", "status")
ACTUALS = os.path.join(KIT, "data", "actuals")
PROJ = os.path.join(KIT, "data", "season", "projections_season.csv")
OUT = os.path.join(STATUS, "tag_outcomes.jsonl")


class OutcomeError(Exception):
    pass


def outcomes(status, actuals, team_of, norm_mpg):
    """One row per flagged player: outcome in {played, sat, no game, unresolved}."""
    played = {r["pool_name"]: r for r in actuals.get("players", []) if r.get("pool_name")}
    teams_with_games = {r["team"] for r in actuals.get("players", [])}
    out = []
    for r in status.get("rows", []):
        name = r["player"]; t = team_of.get(name)
        row = dict(date=status["date"], player=name, fantasy_team=r.get("fantasy_team"), seat=r.get("seat"),
                   yahoo_status=r.get("yahoo_status"), tier=r.get("tier"), availability=r.get("availability"), nba_team=t)
        if t is None:
            row["outcome"] = "unresolved"
        elif t not in teams_with_games:
            row["outcome"] = "no game"
        elif name in played and not played[name].get("dnp") and played[name].get("min", 0) > 0:
            m = played[name]["min"]; n = norm_mpg.get(name)
            row.update(outcome="played", minutes=m, minutes_vs_norm=(m / n) if n else None, norm_mpg=n)
        else:
            row["outcome"] = "sat"
        out.append(row)
    return out


def append(path, date, rows):
    """Append the day's rows; a day already in the ledger is refused (append-only). Returns the rows written."""
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for ln in f:
                if ln.strip() and json.loads(ln).get("date") == date:
                    raise OutcomeError(f"{date} is already in {path}; the ledger is append-only")
    if not rows:
        return 0
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return len(rows)


def load_norms(path=PROJ):
    team, mpg = {}, {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            team[r["name"]] = r.get("team")
            try:
                mpg[r["name"]] = float(r.get("mpg") or 0) or None
            except ValueError:
                mpg[r["name"]] = None
    return team, mpg


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", required=True); ap.add_argument("--out", default=OUT)
    ap.add_argument("--status-dir", default=STATUS); ap.add_argument("--actuals", default=ACTUALS); ap.add_argument("--proj", default=PROJ)
    a = ap.parse_args()
    sp = os.path.join(a.status_dir, f"status_{a.date}.json"); bp = os.path.join(a.actuals, f"{a.date}.json")
    try:
        with open(sp, encoding="utf-8") as f:
            st = json.load(f)
        with open(bp, encoding="utf-8") as f:
            ac = json.load(f)
        team, mpg = load_norms(a.proj)
        rows = outcomes(st, ac, team, mpg)
        n = append(a.out, a.date, rows)
    except (OutcomeError, OSError, ValueError, KeyError) as e:
        print(f"TAG OUTCOMES: FAIL — {e}"); return 1
    c = {}
    for r in rows:
        c[r["outcome"]] = c.get(r["outcome"], 0) + 1
    print(f"TAG OUTCOMES: PASS — {a.date}: {n} flagged player(s) " + ", ".join(f"{v} {k}" for k, v in sorted(c.items())) + f"; {os.path.relpath(a.out, KIT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
