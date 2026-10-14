#!/usr/bin/env python3
"""The 24 against preseason minutes (owner 10/14: "using preseason data as a guide").
A1 window: every final ESPN preseason game 2026-09-28..10-13 (preseason_roles_2026-10-14.json); measure = minutes per game played, starts.
A2 calibration: preseason minutes run below the season's; measured on the UNDISPUTED players (ours within 3 of the outside average)
   with 2+ preseason games: shift = median(preseason mpg - outside avg); adjusted = preseason mpg - shift.
   Sensitivity (stated beforehand as the branch for a shift above 4): the same with a ratio, scale = median(preseason / outside),
   adjusted = preseason / scale. A verdict counts only where both methods agree; otherwise SPLIT.
   Added after the first run (the shift came out at -11.4, past the stated 4-minute branch, and both global corrections
   inflate every player alike, which favours whichever side projects MORE minutes): a third, team-relative check —
   scale_team = median(preseason / outside) over the player's undisputed teammates with 2+ games (3+ teammates needed,
   else the global scale) — and a verdict now needs all three methods to agree.
A3 verdict: BACKS OURS / BACKS OUTSIDE when the adjusted figure is 1.5+ minutes closer to one side; SPLIT otherwise; TOO LITTLE DATA
   under 2 preseason games. Read-only; writes verdicts.json beside itself."""
import json, os, statistics as st, sys
H = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.normpath(os.path.join(H, "..", "..", ".."))
sys.path.insert(0, os.path.join(KIT, "report", "blend", "tools")); from common import canon
pre = json.load(open(os.path.join(H, "preseason_roles_2026-10-14.json")))
P = {}
for p in pre["players"]:
    k = canon(p["name"])
    if k not in P or p["gp"] > P[k]["gp"]: P[k] = p
D = json.load(open(os.path.join(H, "disputed_minutes.json")))
cal = [(P[canon(r["name"])]["mpg"], r["outside"]) for r in D["undisputed"] if canon(r["name"]) in P and P[canon(r["name"])]["gp"] >= 2]
shift = st.median(a - b for a, b in cal); scale = st.median(a / b for a, b in cal)
tscale = {}
for r in D["undisputed"]:
    p = P.get(canon(r["name"]))
    if p and p["gp"] >= 2: tscale.setdefault(r["team"], []).append(p["mpg"] / r["outside"])
def verdict(adj, ours, out):
    do, dx = abs(adj - ours), abs(adj - out)
    return "BACKS OURS" if dx - do >= 1.5 else "BACKS OUTSIDE" if do - dx >= 1.5 else "SPLIT"
rows = []
for r in D["disputed"]:
    p = P.get(canon(r["name"]))
    rec = dict(r)
    if not p or p["gp"] < 2:
        rec.update(pre_gp=p["gp"] if p else 0, pre_mpg=p["mpg"] if p else None, starts=p["starts"] if p else 0,
                   games=[(g["date"], g["opp"], "S" if g["starter"] else "B", g["min"]) for g in (p["games"] if p else []) if not g["dnp"]],
                   verdict="TOO LITTLE DATA"); rows.append(rec); continue
    a1, a2 = p["mpg"] - shift, p["mpg"] / scale
    ts = tscale.get(r["team"], []); sc3 = st.median(ts) if len(ts) >= 3 else scale; a3 = p["mpg"] / sc3
    v1, v2, v3 = (verdict(a, r["ours"], r["outside"]) for a in (a1, a2, a3))
    rec.update(pre_gp=p["gp"], pre_mpg=p["mpg"], starts=p["starts"], adj_shift=round(a1, 1), adj_scale=round(a2, 1), adj_team=round(a3, 1), team_scale=round(sc3, 3), team_n=len(ts),
               games=[(g["date"], g["opp"], "S" if g["starter"] else "B", g["min"]) for g in p["games"] if not g["dnp"]],
               dnp=[(g["date"], g["reason"]) for g in p["games"] if g["dnp"]],
               verdict=v1 if v1 == v2 == v3 else "SPLIT", methods=[v1, v2, v3])
    rows.append(rec)
out = dict(calibration=dict(n=len(cal), shift=round(shift, 2), scale=round(scale, 3)), rows=rows)
json.dump(out, open(os.path.join(H, "verdicts.json"), "w"), indent=1)
print(f"calibration on {len(cal)} undisputed players: shift {shift:+.2f} min, scale {scale:.3f}")
for r in rows:
    print(f"{r['name']:<24} ours {r['ours']:>4.1f} out {r['outside']:>4.1f} | pre gp {r['pre_gp']} st {r['starts']} mpg {r['pre_mpg']} "
          f"adj {r.get('adj_shift')}/{r.get('adj_scale')}/{r.get('adj_team')} (team n {r.get('team_n')}) -> {r['verdict']}")
