#!/usr/bin/env python3
"""The 24 (Council 4-1, 10/14 morning): kit top-200 players whose projected minutes differ by 3+ from the average of the
outside minutes projections on file (Hashtag 10/12, FantasyPros 10/13, BBM cards 10/13; two or more required).
Read-only; writes disputed_minutes.json beside itself."""
import csv, json, os, re, sys, statistics as st
H = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.normpath(os.path.join(H, "..", "..", ".."))
sys.path.insert(0, os.path.join(KIT, "report", "blend", "tools")); from common import canon
SRC = [("Hashtag", "hashtag-2026-10-12.csv"), ("FantasyPros", "fantasypros-2026-10-13.csv"), ("BBM cards", "cards-2026-10-13.csv")]
mp = {}
for lab, fn in SRC:
    for r in csv.DictReader(open(os.path.join(KIT, "report", "market", fn), encoding="utf-8-sig")):
        try: mp.setdefault(canon(r["player"]), {})[lab] = float(r["mpg"])
        except (KeyError, ValueError): pass
kit = {canon(r["name"]): r for r in csv.DictReader(open(os.path.join(KIT, "report", "projections-2026-27.csv"), encoding="utf-8"))}
board = []
for ln in open(os.path.join(KIT, "report", "top-200-2026-27.md"), encoding="utf-8"):
    m = re.match(r"^\| (\d+) \| ([^|]+?) \| ([A-Z]{2,3}) \|", ln)
    if m: board.append((int(m.group(1)), m.group(2).strip(), m.group(3)))
board = board[:200]
rows, undisputed = [], []
for rank, name, team in board:
    k = canon(name); o = mp.get(k, {})
    if len(o) < 2: continue
    ours = float(kit[k]["mpg"]); out = st.mean(o.values())
    rec = dict(rank=rank, name=name, team=team, ours=ours, outside=round(out, 2), sources=o, diff=round(ours - out, 2))
    (rows if abs(ours - out) >= 3 else undisputed).append(rec)
json.dump(dict(rule="|ours - outside avg| >= 3, two or more outside minutes", n_checked=len(rows) + len(undisputed),
               disputed=sorted(rows, key=lambda r: r["diff"]), undisputed=undisputed), open(os.path.join(H, "disputed_minutes.json"), "w"), indent=1)
print(f"checked {len(rows) + len(undisputed)}; disputed {len(rows)} (ours lower {sum(r['diff'] < 0 for r in rows)}, higher {sum(r['diff'] > 0 for r in rows)})")
for r in sorted(rows, key=lambda r: r["diff"]): print(f"  #{r['rank']:<3} {r['name']:<24} {r['team']} ours {r['ours']:.1f} outside {r['outside']:.1f} ({r['diff']:+.1f})")
