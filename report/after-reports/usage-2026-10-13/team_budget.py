#!/usr/bin/env python3
"""Do the shipped lines claim more of a team's shots and possessions than a team uses?

Benchmark (A1): each team's 2025-26 per-game totals from the kit's pinned Basketball-Reference season totals
(report/wo5/data/bref_totals_2004-2026.csv): every 2025-26 row carrying a real team code (single-team season rows and
the per-team split rows of traded players; the 2TM/3TM/4TM summary rows excluded), summed per team, divided by 82.
Known-answer check first: every team's minutes must come to 240-245 a game, or the script stops.

Projection (A2): for each team, the sum over its rows in a kit projections file of line x projected GP / 82 —
a lower bound on the team's projected total, because the pool omits each team's deep bench.
Usage (A3): possessions used = FGA + 0.44 x FTA + TOV; FGA and PTS shown too.

    python3 team_budget.py                # shipped lines (report/projections-2026-27.csv) vs the practice-era lines
"""
import csv, io, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.normpath(os.path.join(H, "..", "..", ".."))
BREF = os.path.join(KIT, "report", "wo5", "data", "bref_totals_2004-2026.csv")
PRACTICE_REV = "89fe5a5^1"   # kit main just before the WO-5 merge: the lines behind the practice page (deck Version 59)
MAP = {"BKN": "BRK", "CHA": "CHO", "PHX": "PHO"}
MULTI = {"2TM", "3TM", "4TM", "TOT"}
f = lambda x: float(x) if x not in ("", None) else 0.0

def actual_2025_26():
    T = {}
    for r in csv.DictReader(open(BREF)):
        if r["season"] != "2025-26" or r["team"] in MULTI: continue
        t = T.setdefault(r["team"], {"min": 0, "fga": 0, "fta": 0, "tov": 0, "pts": 0, "n": 0})
        for k, c in (("min", "mp"), ("fga", "fga"), ("fta", "fta"), ("tov", "tov"), ("pts", "pts")): t[k] += f(r[c])
        t["n"] += 1
    for t in T.values():
        for k in ("min", "fga", "fta", "tov", "pts"): t[k] /= 82.0
        t["use"] = t["fga"] + 0.44 * t["fta"] + t["tov"]
    return T

def projected(text):
    P, rows = {}, {}
    for r in csv.DictReader(io.StringIO(text)):
        if r["team"] == "FA": continue
        team = MAP.get(r["team"], r["team"]); w = f(r["gp"]) / 82.0
        t = P.setdefault(team, {"min": 0, "fga": 0, "fta": 0, "tov": 0, "pts": 0, "n": 0})
        t["min"] += f(r["mpg"]) * w; t["fga"] += f(r["fga"]) * w; t["fta"] += f(r["fta"]) * w
        t["tov"] += f(r["tov"]) * w; t["pts"] += f(r["pts"]) * w; t["n"] += 1
        rows.setdefault(team, []).append(r)
    for t in P.values(): t["use"] = t["fga"] + 0.44 * t["fta"] + t["tov"]
    return P, rows

A = actual_2025_26()
bad = {k: round(v["min"], 1) for k, v in A.items() if not 240 <= v["min"] <= 245}
assert len(A) == 30 and not bad, ("benchmark failed the known-answer minutes check", len(A), bad)
print(f"benchmark: 30 teams, 2025-26 minutes per game {min(v['min'] for v in A.values()):.1f}-{max(v['min'] for v in A.values()):.1f} (known-answer check passed)")
lg_max = max(v["use"] for v in A.values()); lg_min = min(v["use"] for v in A.values())
lg_fga = (min(v["fga"] for v in A.values()), max(v["fga"] for v in A.values()))
print(f"2025-26 team possessions used per game: {lg_min:.1f}-{lg_max:.1f}; shots (FGA) {lg_fga[0]:.1f}-{lg_fga[1]:.1f}")
now_text = open(os.path.join(KIT, "report", "projections-2026-27.csv"), encoding="utf-8").read()
old_text = subprocess.run(["git", "-C", KIT, "show", f"{PRACTICE_REV}:report/projections-2026-27.csv"], capture_output=True, text=True, check=True).stdout
NOW, NOWROWS = projected(now_text); OLD, OLDROWS = projected(old_text)
print("\nteam | pool rows | pool minutes/g today (practice) | shots/g today (practice) vs 2025-26 | possessions used/g today (practice) vs 2025-26 | today/2025-26 | points/g today vs 2025-26")
order = sorted(NOW, key=lambda k: -NOW[k]["use"] / A[k]["use"])
for k in order:
    n, o, a = NOW[k], OLD.get(k, {}), A[k]
    print(f"{k} | {n['n']} | {n['min']:.0f} ({o.get('min', 0):.0f}) | {n['fga']:.1f} ({o.get('fga', 0):.1f}) vs {a['fga']:.1f} | {n['use']:.1f} ({o.get('use', 0):.1f}) vs {a['use']:.1f} | {n['use'] / a['use']:.3f} | {n['pts']:.1f} vs {a['pts']:.1f}")
over_own = [k for k in order if NOW[k]["use"] > A[k]["use"]]
over_max = [k for k in order if NOW[k]["use"] > lg_max]
print(f"\nteams whose pool alone uses more possessions than the team used in 2025-26: {len(over_own)} {over_own}")
print(f"teams whose pool alone is above the 2025-26 league maximum ({lg_max:.1f}): {len(over_max)} {over_max}")
print(f"same tests on the practice-era lines: {sum(OLD[k]['use'] > A[k]['use'] for k in OLD)} over own, {sum(OLD[k]['use'] > lg_max for k in OLD)} over the league max")
sa = sum(v["use"] for v in A.values()); sm = sum(v["min"] for v in A.values())
for lab, Pp in (("today", NOW), ("practice-era", OLD)):
    su = sum(v["use"] for v in Pp.values()); smin = sum(v["min"] for v in Pp.values())
    print(f"league-wide, {lab} lines: the pools cover {smin / sm:.1%} of 2025-26 league minutes and claim {su / sa:.1%} of its possessions used (per-minute usage {(su / smin) / (sa / sm):.3f} x the league's)")
for team in ["PHI"] + [k for k in over_max if k != "PHI"]:
    print(f"\n{team}: player | GP | min | shots | possessions used/g weighted by GP, today (practice)")
    old = {r["name"]: r for r in OLDROWS.get(team, [])}
    for r in sorted(NOWROWS[team], key=lambda r: -(f(r["fga"]) + 0.44 * f(r["fta"]) + f(r["tov"])) * f(r["gp"])):
        u = (f(r["fga"]) + 0.44 * f(r["fta"]) + f(r["tov"])) * f(r["gp"]) / 82
        q = old.get(r["name"]); uo = (f(q["fga"]) + 0.44 * f(q["fta"]) + f(q["tov"])) * f(q["gp"]) / 82 if q else None
        print(f"  {r['name']:<26} {r['gp']:>3} {r['mpg']:>5} {r['fga']:>5} | {u:5.1f} ({'-' if uo is None else f'{uo:.1f}'})")
