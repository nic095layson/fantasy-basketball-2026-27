#!/usr/bin/env python3
"""The 🎯 at each owner turn on each page, how often two pages agree, and the Top-5 overlap (card_<v>.json)."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
V = ["v59", "v60", "v62", "v63", "v64"]
R = {v: {t["pick"]: t for t in json.load(open(os.path.join(H, f"card_{v}.json")))} for v in V}
turns = sorted(R["v63"])
print("🎯 by page at each owner turn (actual pick in brackets)")
print("pick | actual | " + " | ".join(V))
for n in turns:
    print(f"#{n} | {R['v63'][n]['actual']} | " + " | ".join(R[v][n]["targetName"] for v in V))
same = lambda a, b: sum(R[a][n]["targetName"] == R[b][n]["targetName"] for n in turns)
for a, b in [("v59","v60"),("v60","v62"),("v59","v63"),("v62","v63"),("v63","v64")]:
    print(f"🎯 same {a} vs {b}: {same(a,b)} of {len(turns)}")
def top5(v, n): return [r["n"] for r in R[v][n]["rows"]]
for a, b in [("v59","v63"),("v63","v64")]:
    ov = [len(set(top5(a,n)) & set(top5(b,n))) for n in turns]
    print(f"top-5 overlap {a} vs {b} per turn: {ov} (mean {sum(ov)/len(ov):.2f} of 5)")
print()
for n in turns:
    print(f"#{n} actual {R['v63'][n]['actual']}: v59 top5 {top5('v59',n)}")
    print(f"      v63 top5 {top5('v63',n)}")
    a = R["v59"][n]; b = R["v63"][n]
    print(f"      actual's card rank v59 #{a['actualCardRank']} / v63 #{b['actualCardRank']}")
