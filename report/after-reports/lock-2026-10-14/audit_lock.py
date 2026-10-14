"""Read-only audit: the kit top-200 lines (KITPROJ, default the kit file) against the five outside projections. Prints per-category bias/MAE vs the outside median, the envelope test for every forecaster against four others, and each forecaster's distance to the median of the other five (category SD units). MOUT writes the per-player record."""
import ast, csv, json, os, re, sys, statistics as st
KIT = "/home/user/fantasy-basketball-2026-27"; DECK = "/home/user/yahoo-fantasy-basketball"
sys.path.insert(0, os.path.join(DECK, "scripts"))
import range_check as rc
fold = rc.fold
tree = ast.parse(open(f"{KIT}/report/market/build_market.py").read())
AL = {}
for n in tree.body:
    if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "ALIASES" for t in n.targets):
        AL = {fold(v): fold(k) for k, vs in ast.literal_eval(n.value).items() for v in vs}
canon = lambda s: AL.get(fold(s), fold(s))
CATS = ["pts", "reb", "ast", "stl", "blk", "tpm", "tov", "fg_pct", "ft_pct"]
KC = {"fg_pct": "fgp", "ft_pct": "ftp"}
SRC = [("Yahoo", "yahoo-proj-2026-10-14.csv", "", 1.0), ("Hashtag", "hashtag-2026-10-14.csv", "", 1.0),
       ("RotoBaller", "rotoballer-2026-10-13.csv", "src_", 100.0), ("FantasyPros", "fantasypros-2026-10-13.csv", "src_", 100.0),
       ("BBM cards", "cards-2026-10-13.csv", "src_", 100.0)]
refs = {}
for lab, fn, pre, sc in SRC:
    for r in csv.DictReader(open(f"{KIT}/report/market/{fn}", encoding="utf-8-sig")):
        try: d = {c: float(r[pre + c]) / (sc if c.endswith("pct") else 1) for c in CATS}
        except (KeyError, ValueError, TypeError): continue
        refs.setdefault(canon(r["player"]), {})[lab] = d
board = []
for ln in open(f"{KIT}/report/top-200-2026-27.md"):
    m = re.match(r"^\| (\d+) \| ([^|]+?) \| ([A-Z]{2,3}) \|", ln)
    if m: board.append((int(m.group(1)), m.group(2).strip()))
board = board[:200]; assert len(board) == 200
kit = {canon(r["name"]): r for r in csv.DictReader(open(__import__('os').environ.get('KITPROJ', f'{KIT}/report/projections-2026-27.csv')))}
out = {"rows": [], "nrefs": {}}
per = {c: {"diff": [], "out": 0, "n": 0, "loo": []} for c in CATS}
for rank, name in board:
    k = canon(name); R = refs.get(k, {}); L = kit[k]
    out["nrefs"][len(R)] = out["nrefs"].get(len(R), 0) + 1
    row = {"rank": rank, "name": name, "n": len(R), "cells": {}}
    if len(R) >= 3:
        for c in CATS:
            vals = [R[s][c] for s in R]; ours = float(L[KC.get(c, c)]); med = st.median(vals)
            per[c]["diff"].append(ours - med); per[c]["n"] += 1
            if ours < min(vals) - 1e-9 or ours > max(vals) + 1e-9: per[c]["out"] += 1
            for s in R:  # leave-one-out: each outside source against the median of the others
                others = [R[t][c] for t in R if t != s]; per[c]["loo"].append(abs(R[s][c] - st.median(others)))
            row["cells"][c] = [ours, med, min(vals), max(vals)]
    out["rows"].append(row)
print("refs per player (top 200):", dict(sorted(out["nrefs"].items())))
print(f"{'cat':7} {'n':>4} {'bias ours-med':>13} {'MAE ours':>9} {'MAE src(loo)':>12} {'ratio':>6} {'outside env':>11}")
tot_out = tot_n = 0
for c in CATS:
    d = per[c]; mae = st.mean(abs(x) for x in d["diff"]); loo = st.mean(d["loo"])
    tot_out += d["out"]; tot_n += d["n"]
    print(f"{c:7} {d['n']:>4} {st.mean(d['diff']):>+13.4f} {mae:>9.4f} {loo:>12.4f} {mae/loo:>6.2f} {d['out']:>5} ({d['out']/d['n']:.0%})")
print(f"cells inside the five-source envelope: {tot_n-tot_out}/{tot_n} = {(tot_n-tot_out)/tot_n:.1%}")
json.dump(out, open(__import__("os").environ.get("MOUT", "/dev/null"), "w"), indent=1)
# apples to apples: every forecaster (ours and each outside source) against the range of four others
import itertools
print("\nenvelope test, each forecaster vs the min-max of four others (157 players with all five):")
fc = {}
for rank, name in board:
    k = canon(name); R = refs.get(k, {})
    if len(R) != 5: continue
    ours = {c: float(kit[k][KC.get(c, c)]) for c in CATS}
    allf = dict(R); allf["OURS"] = ours
    for f_ in allf:
        others = [s for s in allf if s != f_]
        for sub in itertools.combinations(others, 4):
            for c in CATS:
                vals = [allf[s][c] for s in sub]
                ins = min(vals) - 1e-9 <= allf[f_][c] <= max(vals) + 1e-9
                a = fc.setdefault(f_, [0, 0]); a[0] += ins; a[1] += 1
for f_, (i, n) in sorted(fc.items(), key=lambda x: -x[1][0] / x[1][1]):
    print(f"  {f_:12} inside {i/n:.1%}")
# distance of each forecaster to the median of the other five, in each category's SD units (157 players)
print("\nmean distance to the median of the other five (category SD units, 157 players):")
sd = {c: st.pstdev([float(kit[canon(n)][KC.get(c, c)]) for _, n in board]) for c in CATS}
dist = {}
for rank, name in board:
    k = canon(name); R = refs.get(k, {})
    if len(R) != 5: continue
    allf = dict(R); allf["OURS"] = {c: float(kit[k][KC.get(c, c)]) for c in CATS}
    for f_ in allf:
        for c in CATS:
            m = st.median([allf[s][c] for s in allf if s != f_])
            dist.setdefault(f_, {}).setdefault(c, []).append(abs(allf[f_][c] - m) / sd[c])
print(f"  {'':12} " + " ".join(f"{c:>6}" for c in CATS) + "    all")
for f_ in dist:
    vals = [st.mean(dist[f_][c]) for c in CATS]
    print(f"  {f_:12} " + " ".join(f"{v:6.3f}" for v in vals) + f"  {st.mean(vals):.3f}")
