#!/usr/bin/env python3
"""Board-wide: our value order per page (val_<v>.json) against Yahoo's own projected-line Rank and ADP (yahoo-proj-2026-10-13.csv)."""
import json, csv, os, unicodedata, re, statistics as st
H = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.normpath(os.path.join(H, "..", "..", ".."))
fold = lambda s: re.sub(r"[^a-z ]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).replace(" jr", "").replace(" iii", "").replace(" ii", "").strip()
yp = [r for r in csv.DictReader(open(os.path.join(KIT, "report/market/yahoo-proj-2026-10-13.csv"))) if r["yrank"]]
def spearman(a, b):
    n = len(a)
    ra = {v: i for i, v in enumerate(sorted(range(n), key=lambda i: a[i]))}
    rb = {v: i for i, v in enumerate(sorted(range(n), key=lambda i: b[i]))}
    d2 = sum((ra[i] - rb[i]) ** 2 for i in range(n))
    return 1 - 6 * d2 / (n * (n * n - 1))
for v in ["v59", "v60", "v63", "v64"]:
    V = {fold(r["n"]): r for r in json.load(open(os.path.join(H, f"val_{v}.json"))) if r["valRank"]}
    for top in (60, 150):
        rows = [r for r in yp if int(r["yrank"]) <= top and fold(r["player"]) in V]
        a = [V[fold(r["player"])]["valRank"] for r in rows]; b = [int(r["yrank"]) for r in rows]
        mad = st.mean(abs(x - y) for x, y in zip(a, b))
        w25 = sum(abs(x - y) > 25 for x, y in zip(a, b))
        rowsA = [r for r in rows if r["adp"] not in ("", None)]
        rho_adp = spearman([V[fold(r["player"])]["valRank"] for r in rowsA], [float(r["adp"]) for r in rowsA])
        print(f"{v}: Yahoo projection top {top}: joined {len(rows)} · rho vs Yahoo Rank {spearman(a, b):.3f} · mean |rank gap| {mad:.1f} · gaps over 25 places {w25} · rho vs ADP {rho_adp:.3f} (n={len(rowsA)})")
    miss = [r["player"] for r in yp if int(r["yrank"]) <= 150 and fold(r["player"]) not in V]
    print(f"   not joined in Yahoo's top 150: {miss}")
