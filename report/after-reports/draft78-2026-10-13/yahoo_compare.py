#!/usr/bin/env python3
"""Yahoo's projected standings (screenshot, yahoo_standings_2026-10-13.csv) against each roster summed from Yahoo's own
per-player projection file on hand (report/market/yahoo-proj-2026-10-13.csv: games x per-game line), and the same
rosters on the deck's Version 65 lines (data/players.csv: projected games x per-game line). Tells whether the
screenshot is Yahoo's per-player file summed, and where Yahoo's view and ours part for seat 10 and seat 9."""
import csv, json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.normpath(os.path.join(H, "..", "..", ".."))
sys.path.insert(0, "/home/user/yahoo-fantasy-basketball/scripts"); import hoops, range_check as rc
recap = json.load(open(os.path.join(H, "recap.json"), encoding="utf-8"))
mgr = {p["slot"]: p["manager"] for p in recap}
ros = {}
for p in recap: ros.setdefault(p["slot"], []).append(p["player"])
Y = {rc.fold(r["player"]): r for r in csv.DictReader(open(os.path.join(K, "report", "market", "yahoo-proj-2026-10-13.csv"), encoding="utf-8-sig"))}
hoops.DATA_PATH = "/home/user/yahoo-fantasy-basketball/data/players.csv"
D = {rc.fold(p["player"]): p for p in hoops.load_players()}
S = {r["manager"]: r for r in csv.DictReader(open(os.path.join(H, "yahoo_standings_2026-10-13.csv")))}
ALIAS = {"Cameron Johnson": "Cam Johnson"}  # mock 78: the deck pool spells him Cameron, Yahoo's 10/13 file Cam
C = ["tpm", "pts", "reb", "ast", "stl", "blk", "tov"]
def tot(names, src, gpk, ck):
    t = {c: 0.0 for c in C}; fgm = fga = ftm = fta = 0.0; miss = []; g = 0
    for n in names:
        r = src.get(rc.fold(n)) or src.get(rc.fold(ALIAS.get(n, n)))
        if not r: miss.append(n); continue
        gp = float(r[gpk] or 0); g += gp
        for c in C: t[c] += gp * float(r[ck(c)] or 0)
        fga += gp * float(r.get("fga") or 0); fta += gp * float(r.get("fta") or 0)
        fgm += gp * float(r.get("fga") or 0) * float(r[ck("fg_pct")] or 0); ftm += gp * float(r.get("fta") or 0) * float(r[ck("ft_pct")] or 0)
    t["fg_pct"] = fgm / fga if fga else None; t["ft_pct"] = ftm / fta if fta else None; t["gp"] = g
    return t, miss
out = []
ycols = lambda c: c
for s in range(1, 13):
    yt, ym = tot(ros[s], Y, "gp", ycols)
    sc = S[mgr[s]]
    out.append({"seat": s, "manager": mgr[s], "yahoo_file_sum": {k: round(v, 3) if isinstance(v, float) else v for k, v in yt.items()}, "missing_in_yahoo_file": ym,
                "screenshot": {c: float(sc[c]) for c in C}, "diff_pts": round(yt["pts"] - float(sc["pts"]), 1), "diff_reb": round(yt["reb"] - float(sc["reb"]), 1)})
json.dump(out, open(os.path.join(H, "yahoo_compare.json"), "w"), indent=1, ensure_ascii=False)
for o in out:
    print(f"seat {o['seat']:>2} {o['manager']:<15} games {o['yahoo_file_sum']['gp']:>5.0f}  pts file {o['yahoo_file_sum']['pts']:>7.0f} vs shot {o['screenshot']['pts']:>6.0f} ({o['diff_pts']:+.0f})  reb {o['diff_reb']:+.0f}  missing {o['missing_in_yahoo_file']}")
