#!/usr/bin/env python3
"""Is Version 59 a fair stand-in for 'how we've been practicing'? The 🎯 at the owner's 13 turns on older practice pages
(v44 10/06, v50 10/08, v54 10/09, v59 10/12) against the page drafted on (v63), and against each other."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
V = ["v44", "v50", "v54", "v59", "v63"]
R = {v: {t["pick"]: t["targetName"] for t in json.load(open(os.path.join(H, f"card_{v}.json")))} for v in V}
turns = sorted(R["v63"])
print("pick | " + " | ".join(V))
for n in turns: print(f"#{n} | " + " | ".join(R[v][n] for v in V))
for a in V:
    print(a, " ".join(f"{b}:{sum(R[a][n] == R[b][n] for n in turns)}" for b in V if b != a))
