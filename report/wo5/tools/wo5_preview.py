#!/usr/bin/env python3
"""Preview a candidate write before it lands: deck ranks (hoops adj_value, availability > 0) and kit ranks
(rank_engine passes) on the current files vs the candidate files; the deck's range check on the candidate deck
file; a points-identity scan of the candidate lines.
Usage: wo5_preview.py <candidate dir with players.csv + projections-2026-27.csv> [--json out.json]"""
import sys, os, json, copy, argparse, re, unicodedata
DECK = "/home/user/yahoo-fantasy-basketball"; KIT = "/home/user/fantasy-basketball-2026-27/report"
sys.path.insert(0, DECK + "/scripts"); sys.path.insert(0, KIT)
import hoops, range_check
import rank_engine as RE
ap = argparse.ArgumentParser(); ap.add_argument("cand"); ap.add_argument("--json"); a = ap.parse_args()
ALI = {"herb jones": "herbert jones", "cam johnson": "cameron johnson", "nic claxton": "nicolas claxton", "alex sarr": "alexandre sarr", "ron holland": "ronald holland"}
def nk(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower(); s = re.sub(r"[.'`,’-]", "", s); s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = " ".join(t for t in s.split() if t not in {"jr", "sr", "ii", "iii", "iv"}); return ALI.get(s, s)
def deck_order(path):
    hoops.DATA_PATH = path
    P = hoops.zscores(hoops.load_players()); P = [p for p in P if hoops.availability(p) > 0]
    P.sort(key=lambda p: -hoops.adj_value(p, ()))
    return [(p["player"], round(hoops.adj_value(p, ()), 3)) for p in P]
def kit_order(path):
    rows = RE.load(path); rows, held = RE.exclude_held(rows)
    z1 = RE.zscores(rows, rows); pool = sorted(rows, key=lambda r: -RE.total(z1[r["name"]]))[:RE.POOL_SIZE]; z2 = RE.zscores(rows, pool)
    for r in rows:
        t = RE.total(z2[r["name"]]); av = RE.avail(r["gp"]); r["z_adj"] = t * av if t > 0 else t
    return [(r["name"], round(r["z_adj"], 3)) for r in sorted(rows, key=lambda r: -r["z_adj"])]
d0 = deck_order(DECK + "/data/players.csv"); d1 = deck_order(os.path.join(a.cand, "players.csv"))
k0 = kit_order(KIT + "/projections-2026-27.csv"); k1 = kit_order(os.path.join(a.cand, "projections-2026-27.csv"))
rk = lambda o: {nk(n): i + 1 for i, (n, _) in enumerate(o)}
D0, D1, K0, K1 = rk(d0), rk(d1), rk(k0), rk(k1)
hoops.DATA_PATH = os.path.join(a.cand, "players.csv")
rc = range_check.compute(argparse.Namespace(kit=os.path.dirname(KIT), actual=range_check.ACTUAL_DEFAULT, top=150))
out = dict(deck_top=[dict(rank=i + 1, player=n, value=v, was=D0.get(nk(n))) for i, (n, v) in enumerate(d1[:200])],
           kit_top=[dict(rank=i + 1, player=n, value=v, was=K0.get(nk(n))) for i, (n, v) in enumerate(k1[:200])],
           range=rc)
moves_d = [(n, D0.get(nk(n)), i + 1) for i, (n, _) in enumerate(d1) if D0.get(nk(n)) and abs(D0[nk(n)] - (i + 1)) >= 3 and min(D0[nk(n)], i + 1) <= 200]
moves_k = [(n, K0.get(nk(n)), i + 1) for i, (n, _) in enumerate(k1) if K0.get(nk(n)) and abs(K0[nk(n)] - (i + 1)) >= 3 and min(K0[nk(n)], i + 1) <= 200]
print(f"deck: {len(d1)} live rows; moves of 3+ places inside the top 200 (either side): {len(moves_d)}")
print(f"kit:  {len(k1)} rows; moves of 3+: {len(moves_k)}")
print(f"range check on the candidate deck: {rc['players']} players, {rc['cells']} cells ({rc['checkable']} checkable)")
if a.json: json.dump(out, open(a.json, "w"), indent=1, ensure_ascii=False)
