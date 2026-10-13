#!/usr/bin/env python3
"""Real-life context on file for the two cases the owner named: every recorded preseason game of Portland's four guards
and two incumbent forwards, and of Philadelphia's five, from the ESPN box scores the WO-5 pass pinned
(report/wo5/data/preseason_roles_2026-10-12.json, games through 10/12 morning) and the 10/12 Portland game the 10/13
morning pull recorded (report/after-reports/after-report-2026-10-13.md, its box-score table)."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.normpath(os.path.join(H, "..", "..", ".."))
P = {r["name"]: r for r in json.load(open(os.path.join(KIT, "report/wo5/data/preseason_roles_2026-10-12.json"), encoding="utf-8"))["players"]}
MORNING = open(os.path.join(KIT, "report/after-reports/after-report-2026-10-13.md"), encoding="utf-8").read().splitlines()
TEAMS = {"POR": ["Damian Lillard", "Ja Morant", "Jrue Holiday", "Scoot Henderson", "Deni Avdija", "Toumani Camara"],
         "PHI": ["Tyrese Maxey", "VJ Edgecombe", "Jaylen Brown", "LeBron James", "Joel Embiid"]}
for team, names in TEAMS.items():
    print(f"== {team}: ESPN box scores pinned by WO-5 (preseason_roles_2026-10-12.json)")
    for n in names:
        r = P.get(n)
        if not r: print(f"  {n}: no recorded game"); continue
        for g in sorted(r["games"], key=lambda g: g["date"]):
            role = "did not play (" + g["reason"].lower() + ")" if g["dnp"] else ("starter" if g["starter"] else "bench") + f", {g['min']:.0f} min"
            print(f"  {g['date']} {g['team']} vs {g['opp']} | {n} | {role}")
print("== POR: the 10/12 game as the 10/13 morning pull recorded it (after-report-2026-10-13.md)")
for ln in MORNING:
    if ln.startswith("| Trail Blazers 119, London Lions 66 |") and any(f"| {n} |" in ln for n in TEAMS["POR"]):
        c = [x.strip() for x in ln.strip("|").split("|")]
        print(f"  2026-10-12 POR vs London Lions | {c[1]} | {c[4]}, {c[5]}")
