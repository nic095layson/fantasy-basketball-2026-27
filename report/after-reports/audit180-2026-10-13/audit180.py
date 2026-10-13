#!/usr/bin/env python3
"""Validation and integrity audit of the top-180 lines on the kit board (owner question, 2026-10-13 evening).

Reads only; writes audit180.json and audit180.txt beside itself. Nothing on either plane changes.

Universe (A1): ranks 1-180 of report/top-200-2026-27.md, the kit plane's line for each (report/projections-2026-27.csv).
Tests, each a record per player:
  T1 range    the line's cells against the three outside projections on file (Yahoo 10/13, Hashtag 10/12,
              RotoBaller 9/29): a cell outside all three, with its z beyond the range in the deck's own frame
              (hoops.zscores over the deck pool; net z = sum over cells, flattering positive).
  T2 history  per-36 rates against the player's own band over his last three seasons of 25+ games
              (Basketball-Reference totals pinned at WO-5): outside the band by more than 10% (0.1 floor).
  T3 shooting FG% and FT% against the career band of seasons with 25+ games: outside by more than .010.
  T4 minutes  MPG above the three-season high by 2+, or 4+ from Hashtag's minutes; GP 10+ above the three-season
              average when any of those seasons was under 60 games, or 6+ above both Yahoo's and Hashtag's projected games.
  T5 identity points against 2*FG%*FGA + 3PM + FT%*FTA (gap over 1 is a fail; over 0.25 noted).
  T6 age      32+ projecting more per 36 than 2025-26 in pts, reb or ast; 23 and under projecting less in all three.
  T7 market   our kit rank against every outside rank on file (Yahoo, Hashtag, Rotoworld 9-cat, RotoBaller, RotoWire):
              all available ranks 25+ places on one side.
Tiers (A6): HIGH = three or more tests fire, or a T1 cell beyond 0.5 z; MEDIUM = two; LOW = one; UNANCHORED = fewer
than two qualifying NBA seasons (T2/T3/T6 cannot run); CLEAN = none.
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
ZCAT = {"pts": "PTS", "reb": "REB", "ast": "AST", "stl": "STL", "blk": "BLK", "tpm": "3PM", "tov": "TO", "fg_pct": "FG%", "ft_pct": "FT%"}
BREFCOL = {"pts": "pts", "reb": "trb", "ast": "ast", "stl": "stl", "blk": "blk", "tpm": "fg3", "tov": "tov"}

fold = rc.fold  # the deck's own fold (diacritics, periods, apostrophes and Jr/Sr/II/III/IV suffixes removed)

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

# ---- the universe: the kit board's top 180 and their kit lines
board = []
for ln in open(os.path.join(KIT, "report", "top-200-2026-27.md"), encoding="utf-8"):
    m = re.match(r"^\| (\d+) \| ([^|]+?) \| ([A-Z]{2,3}) \|", ln)
    if m and int(m.group(1)) <= TOP: board.append((int(m.group(1)), m.group(2).strip(), m.group(3)))
assert len(board) == TOP, len(board)
_rows = list(csv.DictReader(open(os.path.join(KIT, "report", "projections-2026-27.csv"), encoding="utf-8")))
kit = {canon(r["name"]): r for r in _rows}
assert len(kit) == len(_rows), "two kit rows fold to one key"
line = lambda r: {c: float(r[KITCOL.get(c, c)]) for c in CATS} | {"fga": float(r["fga"]), "fta": float(r["fta"]), "gp": float(r["gp"]), "mpg": float(r["mpg"])}

# ---- T1: the deck's z frame and the three outside projections (range_check's own loader, no last season)
refs, used = rc.references(KIT, None)
assert len(used) == 3, used
P = hoops.zscores(hoops.load_players())
# the deck's own z frame, the same arithmetic as scripts/range_check.py: parameters over the top-156 fixed point
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

# ---- history: Basketball-Reference season totals (row == season; the summary row for traded players)
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

# ---- outside sources
hashtag = {canon(r["player"]): r for r in csv.DictReader(open(rc.newest(KIT, r"hashtag-\d{4}-\d{2}-\d{2}\.csv"), encoding="utf-8-sig"))}
yahoo = {canon(r["player"]): r for r in csv.DictReader(open(rc.newest(KIT, r"yahoo-proj-\d{4}-\d{2}-\d{2}\.csv"), encoding="utf-8-sig"))}
def outside_gp(key):
    v = [f(yahoo.get(key, {}).get("gp")), f(hashtag.get(key, {}).get("gp"))]
    return [x for x in v if x]
ranks = {}
def add_rank(label, path, name_col, rank_col):
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        if r.get(rank_col): ranks.setdefault(canon(r[name_col]), {})[label] = int(float(r[rank_col]))
add_rank("Yahoo", rc.newest(KIT, r"yahoo-proj-\d{4}-\d{2}-\d{2}\.csv"), "player", "xrank")
add_rank("Hashtag", rc.newest(KIT, r"hashtag-\d{4}-\d{2}-\d{2}\.csv"), "player", "rank")
add_rank("RotoBaller", rc.newest(KIT, r"rotoballer-\d{4}-\d{2}-\d{2}\.csv"), "player", "src_rank")
add_rank("RotoWire", rc.newest(KIT, r"rotowire-\d{4}-\d{2}-\d{2}\.csv"), "player", "src_rank")
add_rank("Rotoworld", rc.newest(KIT, r"rotoworld-9cat-\d{4}-\d{2}-\d{2}\.csv"), "Player", "Rank")

out = []
for rank, name, team in board:
    key = canon(name); r = kit[key]; L = line(r); rec = {"rank": rank, "name": name, "team": team, "gp": L["gp"], "mpg": L["mpg"], "tests": {}, "flags": []}
    # T1
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
    rec["tests"]["T1"] = {"refs": len(R), "cells": cells, "net_z": netz}
    if cells: rec["flags"].append("T1")
    # history
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
        # T3 career shooting band over seasons with 25+ games
        car = [per36(h) for h in allrows if float(h["g"]) >= 25]
        sh = []
        for c in ("fg_pct", "ft_pct"):
            v = [p[c] for p in car if p[c] is not None]
            if not v: continue
            lo, hi = min(v), max(v)
            if L[c] > hi + 0.010 or L[c] < lo - 0.010: sh.append({"cat": c, "line": L[c], "band": [round(lo, 3), round(hi, 3)]})
        rec["tests"]["T3"] = {"cells": sh}
        if sh: rec["flags"].append("T3")
        # T4 minutes and games
        mx = max(p["mpg"] for p in P36); avg_g = sum(p["g"] for p in P36) / len(P36); low = any(p["g"] < 60 for p in P36)
        hm = f(hashtag.get(key, {}).get("mpg"))
        t4 = []
        if L["mpg"] >= mx + 2: t4.append(f"mpg {L['mpg']:g} vs three-season high {mx:.1f}")
        if hm is not None and abs(L["mpg"] - hm) >= 4: t4.append(f"mpg {L['mpg']:g} vs Hashtag {hm:g}")
        if low and L["gp"] >= avg_g + 10: t4.append(f"gp {L['gp']:g} vs three-season average {avg_g:.0f} with a season under 60")
        og = outside_gp(key)
        if og and L["gp"] >= max(og) + 6: t4.append(f"gp {L['gp']:g} vs outside {'/'.join(f'{x:g}' for x in og)} (Yahoo/Hashtag)")
        rec["tests"]["T4"] = {"notes": t4, "three_season_high_mpg": round(mx, 1), "avg_gp": round(avg_g, 1), "hashtag_mpg": hm, "outside_gp": og}
        if t4: rec["flags"].append("T4")
        # T6 age
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
        hm = f(hashtag.get(key, {}).get("mpg"))
        og = outside_gp(key); notes = [f"mpg {L['mpg']:g} vs Hashtag {hm:g}"] if hm is not None and abs(L["mpg"] - hm) >= 4 else []
        if og and L["gp"] >= max(og) + 6: notes.append(f"gp {L['gp']:g} vs outside {'/'.join(f'{x:g}' for x in og)} (Yahoo/Hashtag)")
        rec["tests"]["T4"] = {"notes": notes, "hashtag_mpg": hm, "outside_gp": og}
        if rec["tests"]["T4"]["notes"]: rec["flags"].append("T4")
    # T5 identity
    imp = 2 * L["fg_pct"] * L["fga"] + L["tpm"] + L["ft_pct"] * L["fta"]; gap = round(imp - L["pts"], 2)
    rec["tests"]["T5"] = {"implied": round(imp, 2), "gap": gap}
    if abs(gap) > 1: rec["flags"].append("T5")
    # T7 market
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
           "unanchored_with_flags": sum(1 for r in out if r["tier"] == "UNANCHORED" and r["flags"]),
           "unanchored_largest": [r["name"] for r in sorted((r for r in out if r["tier"] == "UNANCHORED"), key=lambda r: -sum(abs(x["z"]) for x in r["tests"]["T1"]["cells"]))[:5]],
           "ranks_sources": sorted({k for v in ranks.values() for k in v})}
json.dump({"summary": summary, "rows": out}, open(os.path.join(H, "audit180.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
w = []
w.append(f"AUDIT 180: tiers {summary['tiers']}; tests fired {summary['fired']}; references {used}")
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
    w.append(f"{r['rank']:>3} {r['name']} ({r['team']}) [{r['tier']}] net_z {r['tests']['T1']['net_z']:+.2f} age {r['age']} seasons {r['history_seasons']} | " + "; ".join(bits))
open(os.path.join(H, "audit180.txt"), "w", encoding="utf-8").write("\n".join(w) + "\n")
print(w[0])
