#!/usr/bin/env python3
"""Validation and integrity audit of the top-180 kit lines, second run (owner uploads, 2026-10-13 evening).

The same seven tests as audit180.py, with the outside-projection set widened from three to five:
Yahoo 10/13, Hashtag 10/12, RotoBaller (the owner's 10/13 re-export: the 9/29 lines, 12 names added),
FantasyPros 10/13 and the owner's 10/13 card paste. The last three carry projected games (FantasyPros,
the cards) and minutes (FantasyPros, the cards), so T4 now reads every outside minutes and games
projection on file instead of Hashtag's alone:
  T4 minutes  MPG above the three-season high by 2+, or 4+ beyond every outside minutes projection on the same side;
              GP 10+ above the three-season average when any of those seasons was under 60 games, or 6+ above every
              outside games projection.
Everything else is audit180.py verbatim (thresholds A2-A5, tiers A6). Reads only; writes audit180_v2.json and
audit180_v2.txt beside itself. Nothing on either plane changes.
"""
import ast, csv, json, os, re, sys, unicodedata
H = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.normpath(os.path.join(H, "..", "..", ".."))
DECK = os.path.normpath(os.path.join(KIT, "..", "yahoo-fantasy-basketball"))
sys.path.insert(0, os.path.join(DECK, "scripts"))
import hoops, range_check as rc
TOP = 180
CATS = ["pts", "reb", "ast", "stl", "blk", "tpm", "tov", "fg_pct", "ft_pct"]
COUNT = ["pts", "reb", "ast", "stl", "blk", "tpm", "tov"]
KITCOL = {"fg_pct": "fgp", "ft_pct": "ftp"}
BREFCOL = {"pts": "pts", "reb": "trb", "ast": "ast", "stl": "stl", "blk": "blk", "tpm": "fg3", "tov": "tov"}
# label, file pattern, column prefix, percentage scale, games column, minutes column
LINE_SOURCES = [
    ("Yahoo", r"yahoo-proj-\d{4}-\d{2}-\d{2}\.csv", "", 1.0, "gp", None),
    ("Hashtag", r"hashtag-\d{4}-\d{2}-\d{2}\.csv", "", 1.0, "gp", "mpg"),
    ("RotoBaller", r"rotoballer-\d{4}-\d{2}-\d{2}\.csv", "src_", 100.0, None, None),
    ("FantasyPros", r"fantasypros-\d{4}-\d{2}-\d{2}\.csv", "src_", 100.0, "gp", "mpg"),
    ("cards", r"cards-\d{4}-\d{2}-\d{2}\.csv", "src_", 100.0, "gp", "mpg"),
]

fold = rc.fold

def aliases():
    tree = ast.parse(open(os.path.join(KIT, "report", "market", "build_market.py"), encoding="utf-8").read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "ALIASES" for t in node.targets):
            table = ast.literal_eval(node.value)
            return {fold(v): fold(k) for k, vs in table.items() for v in vs}
    return {}
AL = aliases()
canon = lambda s: AL.get(fold(s), fold(s))
f = lambda x: float(x) if x not in ("", None) else None

board = []
for ln in open(os.path.join(KIT, "report", "top-200-2026-27.md"), encoding="utf-8"):
    m = re.match(r"^\| (\d+) \| ([^|]+?) \| ([A-Z]{2,3}) \|", ln)
    if m and int(m.group(1)) <= TOP: board.append((int(m.group(1)), m.group(2).strip(), m.group(3)))
assert len(board) == TOP, len(board)
_rows = list(csv.DictReader(open(os.path.join(KIT, "report", "projections-2026-27.csv"), encoding="utf-8")))
kit = {canon(r["name"]): r for r in _rows}
assert len(kit) == len(_rows), "two kit rows fold to one key"
line = lambda r: {c: float(r[KITCOL.get(c, c)]) for c in CATS} | {"fga": float(r["fga"]), "fta": float(r["fta"]), "gp": float(r["gp"]), "mpg": float(r["mpg"])}

# ---- the five outside projections, their games and their minutes
refs, used, ogp, ompg = {}, {}, {}, {}
for label, pat, pre, scale, gcol, mcol in LINE_SOURCES:
    path = rc.newest(KIT, pat); assert path, label
    used[label] = os.path.basename(path)
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        k = canon(r["player"])
        try:
            d = {c: float(r[pre + c]) / (scale if c.endswith("pct") else 1.0) for c in CATS}
        except (KeyError, TypeError, ValueError):
            continue
        refs.setdefault(k, {})[label] = d
        if gcol and f(r.get(gcol)): ogp.setdefault(k, {})[label] = f(r[gcol])
        if mcol and f(r.get(mcol)): ompg.setdefault(k, {})[label] = f(r[mcol])
assert len(used) == 5, used
P = hoops.zscores(hoops.load_players())
import math
live = [p for p in P if hoops.availability(p) > 0]
fp = sorted(live, key=lambda p: -hoops.total_value(p))[:hoops.DRAFTABLE]
lg_fg = sum(p["fg_pct"] * p["fga"] for p in fp) / sum(p["fga"] for p in fp)
lg_ft = sum(p["ft_pct"] * p["fta"] for p in fp) / sum(p["fta"] for p in fp)
def ms(vals):
    m = sum(vals) / len(vals); return m, (math.sqrt(sum((v - m) ** 2 for v in vals) / len(vals)) or 1.0)
PRM = {"fg_pct": ms([(p["fg_pct"] - lg_fg) * p["fga"] for p in fp]), "ft_pct": ms([(p["ft_pct"] - lg_ft) * p["fta"] for p in fp])}
for c in COUNT: PRM[c] = ms([p[c] for p in fp])
def zcell(L, c, v):
    if c == "fg_pct": return ((v - lg_fg) * L["fga"] - PRM[c][0]) / PRM[c][1]
    if c == "ft_pct": return ((v - lg_ft) * L["fta"] - PRM[c][0]) / PRM[c][1]
    z = (v - PRM[c][0]) / PRM[c][1]; return -z if c == "tov" else z

hist = {}
for r in csv.DictReader(open(os.path.join(KIT, "report", "wo5", "data", "bref_totals_2004-2026.csv"), encoding="utf-8")):
    if r["row"] != "season": continue
    hist.setdefault(canon(r["player"]), []).append(r)
pid_of = {}
for r in json.load(open(os.path.join(KIT, "report", "wo5", "out", "lines_wo5_2026-10-12.json"), encoding="utf-8"))["rows"]:
    if r.get("pid"): pid_of[canon(r["name"])] = r["pid"]
by_pid = {}
for rows in hist.values():
    for r in rows: by_pid.setdefault(r["pid"], []).append(r)
ages = {}
for fn in ("bref_pergame_2025-26.csv", "bref_pergame_2024-25.csv"):
    yr = int(fn[-11:-7])
    for r in csv.DictReader(open(os.path.join(DECK, "arena", "results", "tuning_2026-10-08", fn), encoding="utf-8-sig")):
        if r.get("age", "").strip().isdigit(): ages.setdefault(canon(r["player"]), int(r["age"]) + (2026 - yr))
def seasons(key):
    rows = by_pid.get(pid_of.get(key)) or hist.get(key) or []
    rows = sorted(rows, key=lambda r: r["season"])
    return [r for r in rows if float(r["g"]) >= 25][-3:], rows
def per36(r):
    mp = float(r["mp"]); g = float(r["g"])
    return {c: 36 * float(r[BREFCOL[c]]) / mp for c in COUNT} | {"fga36": 36 * float(r["fga"]) / mp, "fta36": 36 * float(r["fta"]) / mp,
            "mpg": mp / g, "g": g, "fg_pct": float(r["fg"]) / float(r["fga"]) if float(r["fga"]) else None,
            "ft_pct": float(r["ft"]) / float(r["fta"]) if float(r["fta"]) else None, "season": r["season"]}

ranks = {}
def add_rank(label, path, name_col, rank_col):
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        if r.get(rank_col): ranks.setdefault(canon(r[name_col]), {})[label] = int(float(r[rank_col]))
add_rank("Yahoo", rc.newest(KIT, r"yahoo-proj-\d{4}-\d{2}-\d{2}\.csv"), "player", "xrank")
add_rank("Hashtag", rc.newest(KIT, r"hashtag-\d{4}-\d{2}-\d{2}\.csv"), "player", "rank")
add_rank("RotoBaller", rc.newest(KIT, r"rotoballer-\d{4}-\d{2}-\d{2}\.csv"), "player", "src_rank")
add_rank("RotoWire", rc.newest(KIT, r"rotowire-\d{4}-\d{2}-\d{2}\.csv"), "player", "src_rank")
add_rank("Rotoworld", rc.newest(KIT, r"rotoworld-9cat-\d{4}-\d{2}-\d{2}\.csv"), "Player", "Rank")
fmtd = lambda d: "/".join(f"{v:g}" for v in d.values()) + " (" + "/".join(d) + ")"

def t4_outside(L, key):
    notes = []
    om, og = ompg.get(key, {}), ogp.get(key, {})
    if om and (L["mpg"] >= max(om.values()) + 4 or L["mpg"] <= min(om.values()) - 4): notes.append(f"mpg {L['mpg']:g} vs outside {fmtd(om)}")
    if og and L["gp"] >= max(og.values()) + 6: notes.append(f"gp {L['gp']:g} vs outside {fmtd(og)}")
    return notes, om, og

out = []
for rank, name, team in board:
    key = canon(name); r = kit[key]; L = line(r); rec = {"rank": rank, "name": name, "team": team, "gp": L["gp"], "mpg": L["mpg"], "tests": {}, "flags": []}
    R = refs.get(key, {})
    cells = []
    for c in CATS:
        vals = [v[c] for v in R.values()]
        if len(vals) < 2: continue
        lo, hi = min(vals), max(vals); tol = 0.005 if c.endswith("pct") else max(0.1, 0.05 * hi)
        if L[c] > hi + tol or L[c] < lo - tol:
            bound = lo if L[c] < lo else hi
            z = zcell(L, c, L[c]) - zcell(L, c, bound)
            cells.append({"cat": c, "line": L[c], "lo": round(lo, 3), "hi": round(hi, 3), "beyond": round(L[c] - bound, 3), "z": round(z, 2)})
    netz = round(sum(x["z"] for x in cells), 2)
    rec["tests"]["T1"] = {"refs": len(R), "sources": sorted(R), "cells": cells, "net_z": netz}
    if cells: rec["flags"].append("T1")
    hs, allrows = seasons(key); rec["history_seasons"] = [h["season"] for h in hs]; rec["age"] = ages.get(key)
    unanchored = len(hs) < 2
    rec["unanchored"] = unanchored
    if not unanchored:
        P36 = [per36(h) for h in hs]
        l36 = {c: 36 * L[c] / L["mpg"] for c in COUNT}
        hits = []
        for c in COUNT:
            lo, hi = min(p[c] for p in P36), max(p[c] for p in P36); tol = max(0.1, 0.10 * max(abs(lo), abs(hi)))
            if l36[c] > hi + tol or l36[c] < lo - tol:
                hits.append({"cat": c, "line_per36": round(l36[c], 2), "band": [round(lo, 2), round(hi, 2)]})
        rec["tests"]["T2"] = {"cells": hits}
        if hits: rec["flags"].append("T2")
        car = [per36(h) for h in allrows if float(h["g"]) >= 25]
        sh = []
        for c in ("fg_pct", "ft_pct"):
            v = [p[c] for p in car if p[c] is not None]
            if not v: continue
            lo, hi = min(v), max(v)
            if L[c] > hi + 0.010 or L[c] < lo - 0.010: sh.append({"cat": c, "line": L[c], "band": [round(lo, 3), round(hi, 3)]})
        rec["tests"]["T3"] = {"cells": sh}
        if sh: rec["flags"].append("T3")
        mx = max(p["mpg"] for p in P36); avg_g = sum(p["g"] for p in P36) / len(P36); low = any(p["g"] < 60 for p in P36)
        t4 = []
        if L["mpg"] >= mx + 2: t4.append(f"mpg {L['mpg']:g} vs three-season high {mx:.1f}")
        if low and L["gp"] >= avg_g + 10: t4.append(f"gp {L['gp']:g} vs three-season average {avg_g:.0f} with a season under 60")
        n4, om, og = t4_outside(L, key); t4 += n4
        rec["tests"]["T4"] = {"notes": t4, "three_season_high_mpg": round(mx, 1), "avg_gp": round(avg_g, 1), "outside_mpg": om, "outside_gp": og}
        if t4: rec["flags"].append("T4")
        last = per36(hs[-1]); a = rec["age"]; t6 = []
        if a is not None and a >= 32:
            up = [c for c in ("pts", "reb", "ast") if l36[c] > last[c] * 1.05]
            if up: t6.append(f"age {a}: per-36 above 2025-26 in {', '.join(up)}")
        if a is not None and a <= 23:
            if all(l36[c] < last[c] * 0.95 for c in ("pts", "reb", "ast")): t6.append(f"age {a}: per-36 below {last['season']} in pts, reb and ast")
        if a is not None and a >= 34 and len(R) >= 2:
            over = [c for c in ("pts", "reb", "ast") if L[c] > sum(v[c] for v in R.values()) / len(R)]
            if len(over) >= 2: t6.append(f"age {a}: above the outside average in {', '.join(over)} (no decline in the method)")
        rec["tests"]["T6"] = {"notes": t6}
        if t6: rec["flags"].append("T6")
    else:
        n4, om, og = t4_outside(L, key)
        rec["tests"]["T4"] = {"notes": n4, "outside_mpg": om, "outside_gp": og}
        if n4: rec["flags"].append("T4")
    imp = 2 * L["fg_pct"] * L["fga"] + L["tpm"] + L["ft_pct"] * L["fta"]; gap = round(imp - L["pts"], 2)
    rec["tests"]["T5"] = {"implied": round(imp, 2), "gap": gap}
    if abs(gap) > 1: rec["flags"].append("T5")
    rk = ranks.get(key, {}); t7 = None
    if len(rk) >= 3:
        above = [k for k, v in rk.items() if v <= rank - 25]; below = [k for k, v in rk.items() if v >= rank + 25]
        if len(above) == len(rk): t7 = "every outside rank 25+ places above ours (we are low)"
        elif len(below) == len(rk): t7 = "every outside rank 25+ places below ours (we are high)"
    rec["tests"]["T7"] = {"ours": rank, "outside": rk, "note": t7}
    if t7: rec["flags"].append("T7")
    big = abs(netz) > 0.5
    n = len(rec["flags"])
    rec["tier"] = "UNANCHORED" if unanchored else ("HIGH" if n >= 3 or big else "MEDIUM" if n == 2 else "LOW" if n == 1 else "CLEAN")
    out.append(rec)

summary = {"universe": TOP, "refs": used, "tiers": {t: sum(1 for r in out if r["tier"] == t) for t in ("HIGH", "MEDIUM", "LOW", "UNANCHORED", "CLEAN")},
           "fired": {t: sum(1 for r in out if t in r["flags"]) for t in ("T1", "T2", "T3", "T4", "T5", "T6", "T7")},
           "refs_per_line": {str(n): sum(1 for r in out if r["tests"]["T1"]["refs"] == n) for n in range(6)},
           "t1_cells": sum(len(r["tests"]["T1"]["cells"]) for r in out),
           "t1_z_up": round(sum(x["z"] for r in out for x in r["tests"]["T1"]["cells"] if x["z"] > 0), 2),
           "t1_z_down": round(sum(x["z"] for r in out for x in r["tests"]["T1"]["cells"] if x["z"] < 0), 2),
           "over_half": [(r["name"], r["tests"]["T1"]["net_z"]) for r in out if abs(r["tests"]["T1"]["net_z"]) > 0.5],
           "unanchored_with_flags": sum(1 for r in out if r["tier"] == "UNANCHORED" and r["flags"]),
           "unanchored_largest": [r["name"] for r in sorted((r for r in out if r["tier"] == "UNANCHORED"), key=lambda r: -sum(abs(x["z"]) for x in r["tests"]["T1"]["cells"]))[:5]],
           "ranks_sources": sorted({k for v in ranks.values() for k in v})}
json.dump({"summary": summary, "rows": out}, open(os.path.join(H, "audit180_v2.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
w = []
w.append(f"AUDIT 180 v2: tiers {summary['tiers']}; tests fired {summary['fired']}; references {used}; refs per line {summary['refs_per_line']}")
for r in out:
    if r["tier"] == "CLEAN": continue
    bits = []
    for x in r["tests"]["T1"]["cells"]: bits.append(f"T1 {x['cat']} {x['line']:g} vs {x['lo']:g}-{x['hi']:g} ({x['z']:+.2f} z)")
    for x in r["tests"].get("T2", {}).get("cells", []): bits.append(f"T2 {x['cat']} per36 {x['line_per36']} vs {x['band'][0]}-{x['band'][1]}")
    for x in r["tests"].get("T3", {}).get("cells", []): bits.append(f"T3 {x['cat']} {x['line']:.3f} vs career {x['band'][0]:.3f}-{x['band'][1]:.3f}")
    for x in r["tests"]["T4"]["notes"]: bits.append("T4 " + x)
    if abs(r["tests"]["T5"]["gap"]) > 1: bits.append(f"T5 identity gap {r['tests']['T5']['gap']:+.2f}")
    for x in r["tests"].get("T6", {}).get("notes", []): bits.append("T6 " + x)
    if r["tests"]["T7"]["note"]: bits.append("T7 " + r["tests"]["T7"]["note"] + " " + json.dumps(r["tests"]["T7"]["outside"]))
    w.append(f"{r['rank']:>3} {r['name']} ({r['team']}) [{r['tier']}] refs {r['tests']['T1']['refs']} net_z {r['tests']['T1']['net_z']:+.2f} age {r['age']} seasons {r['history_seasons']} | " + "; ".join(bits))
open(os.path.join(H, "audit180_v2.txt"), "w", encoding="utf-8").write("\n".join(w) + "\n")
print(w[0])
