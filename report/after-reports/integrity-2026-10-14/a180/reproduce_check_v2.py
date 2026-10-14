#!/usr/bin/env python3
"""Known-answer check on audit180_v2.json: for every T1 cell, recompute the outside band from the five processed
reference files with an independent loader (no shared code with audit180_v2.py except the deck's name fold), and
confirm lo, hi and the direction; also confirm that every line's reference count equals the number of files that
carry the player, and that no in-band cell was reported. Prints the tallies; exits 1 on any disagreement."""
import csv, json, os, sys, unicodedata, re
H = os.path.dirname(os.path.abspath(__file__)); K = "/home/user/fantasy-basketball-2026-27"; M = os.path.join(K, "report", "market")
sys.path.insert(0, os.path.join(K, "..", "yahoo-fantasy-basketball", "scripts")); import range_check as rc
fold = rc.fold
import ast
tree = ast.parse(open(os.path.join(M, "build_market.py"), encoding="utf-8").read())
AL = next({fold(v): fold(k) for k, vs in ast.literal_eval(n.value).items() for v in vs} for n in tree.body if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "ALIASES" for t in n.targets))
canon = lambda s: AL.get(fold(s), fold(s))
CATS = ["pts", "reb", "ast", "stl", "blk", "tpm", "tov", "fg_pct", "ft_pct"]
FILES = {"Yahoo": ("yahoo-proj-2026-10-14.csv", "", 1), "Hashtag": ("hashtag-2026-10-14.csv", "", 1), "RotoBaller": ("rotoballer-2026-10-13.csv", "src_", 100),
         "FantasyPros": ("fantasypros-2026-10-13.csv", "src_", 100), "cards": ("cards-2026-10-13.csv", "src_", 100)}
refs = {}
for label, (fn, pre, sc) in FILES.items():
    for r in csv.DictReader(open(os.path.join(M, fn), encoding="utf-8-sig")):
        try: d = {c: float(r[pre + c]) / (sc if c.endswith("pct") else 1) for c in CATS}
        except (KeyError, ValueError): continue
        refs.setdefault(canon(r["player"]), {})[label] = d
kit = {canon(r["name"]): r for r in csv.DictReader(open(os.path.join(K, "report", "projections-2026-27.csv"), encoding="utf-8"))}
KC = {"fg_pct": "fgp", "ft_pct": "ftp"}
A = json.load(open(os.path.join(H, "audit180_v2.json"), encoding="utf-8"))
bad = []; cells = 0; inband_missing = 0
for r in A["rows"]:
    k = canon(r["name"]); R = refs.get(k, {}); L = {c: float(kit[k][KC.get(c, c)]) for c in CATS}
    if r["tests"]["T1"]["refs"] != len(R) or sorted(R) != r["tests"]["T1"]["sources"]: bad.append((r["name"], "refs", r["tests"]["T1"]["sources"], sorted(R)))
    got = {x["cat"]: x for x in r["tests"]["T1"]["cells"]}
    for c in CATS:
        vals = [v[c] for v in R.values()]
        if len(vals) < 2: continue
        lo, hi = min(vals), max(vals); tol = 0.005 if c.endswith("pct") else max(0.1, 0.05 * hi)
        out = L[c] > hi + tol or L[c] < lo - tol
        if out:
            cells += 1
            x = got.get(c)
            if not x or abs(x["lo"] - lo) > 1e-6 or abs(x["hi"] - hi) > 1e-6 or (x["beyond"] > 0) != (L[c] > hi): bad.append((r["name"], c, x, (lo, hi, L[c])))
        elif c in got: bad.append((r["name"], c, "reported but inside the band", (lo, hi, L[c])))
print(f"players {len(A['rows'])}; outside cells recomputed {cells}; audit cells {sum(len(r['tests']['T1']['cells']) for r in A['rows'])}; disagreements {len(bad)}")
for b in bad[:20]: print(b)
sys.exit(1 if bad else 0)
