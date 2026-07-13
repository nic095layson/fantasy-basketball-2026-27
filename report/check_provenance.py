#!/usr/bin/env python3
"""Roster-provenance gate — enforces PROMPT.md §0.6.

Every row of projections-2026-27.csv must have a matching row in
roster-provenance.csv (same player, same team, with a source URL and a
verification date). This exists because the 2026-07-12 CSV shipped 39 stale
team values sourced from memory instead of research — see
postmortem-2026-07-13-roster-audit.md. A team edit without a provenance edit
is exactly the failure mode this file blocks.

Usage:
  python3 check_provenance.py                  # structural check
  python3 check_provenance.py --max-age-days 14  # + freshness gate (October runs)

Exit 0 = pass. Exit 1 = fail, problems listed on stdout.
rank_engine.py imports check() and refuses to build a board that fails it.
"""
import csv
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECTIONS = os.path.join(HERE, "projections-2026-27.csv")
PROVENANCE = os.path.join(HERE, "roster-provenance.csv")


def check(projections_path=PROJECTIONS, provenance_path=PROVENANCE, max_age_days=None):
    """Return (problems, newest, oldest) where problems is a list of strings
    and newest/oldest are the min/max verified_on dates across all rows."""
    problems = []
    if not os.path.exists(provenance_path):
        return ([f"{os.path.basename(provenance_path)} is missing — every "
                 "player-team claim needs a source (PROMPT.md §0.6)"], None, None)

    proj = list(csv.DictReader(open(projections_path)))
    prov_rows = list(csv.DictReader(open(provenance_path)))
    prov = {}
    for p in prov_rows:
        if p["name"] in prov:
            problems.append(f"duplicate provenance row: {p['name']}")
        prov[p["name"]] = p

    dates = []
    for r in proj:
        p = prov.get(r["name"])
        if p is None:
            problems.append(f"NO PROVENANCE: {r['name']} ({r['team']}) — team "
                            "asserted without a source")
            continue
        if p["team"] != r["team"]:
            problems.append(f"TEAM MISMATCH: {r['name']} is {r['team']} in "
                            f"projections but {p['team']} in provenance — one "
                            "of them was edited without the other")
        if not p["source_url"].strip():
            problems.append(f"EMPTY SOURCE: {r['name']}")
        try:
            dates.append(date.fromisoformat(p["verified_on"]))
        except ValueError:
            problems.append(f"BAD verified_on DATE: {r['name']} "
                            f"({p['verified_on']!r} — must be YYYY-MM-DD)")

    proj_names = {r["name"] for r in proj}
    for name in prov:
        if name not in proj_names:
            problems.append(f"ORPHAN provenance row (player not in projections): {name}")

    newest = max(dates) if dates else None
    oldest = min(dates) if dates else None
    if max_age_days is not None and oldest is not None:
        age = (date.today() - oldest).days
        if age > max_age_days:
            stale = sorted(n for n, p in prov.items()
                           if n in proj_names
                           and _age_ok(p) and
                           (date.today() - date.fromisoformat(p["verified_on"])).days > max_age_days)
            problems.append(f"STALE: oldest verification is {age} days old "
                            f"(limit {max_age_days}); {len(stale)} row(s) over "
                            f"the limit, e.g. {', '.join(stale[:5])}")
    return problems, newest, oldest


def _age_ok(p):
    try:
        date.fromisoformat(p["verified_on"])
        return True
    except ValueError:
        return False


def main():
    max_age = None
    if "--max-age-days" in sys.argv:
        max_age = int(sys.argv[sys.argv.index("--max-age-days") + 1])
    problems, newest, oldest = check(max_age_days=max_age)
    if problems:
        print(f"PROVENANCE GATE: FAIL ({len(problems)} problem(s))")
        for p in problems:
            print(" -", p)
        sys.exit(1)
    span = oldest.isoformat() if oldest == newest else f"{oldest} .. {newest}"
    print(f"PROVENANCE GATE: PASS — all rows sourced; verified {span}")


if __name__ == "__main__":
    main()
