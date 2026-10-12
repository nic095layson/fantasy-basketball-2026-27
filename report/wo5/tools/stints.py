"""Print every season / team-split stint (G >= 15) since 2019-20 for the named players, newest first, with starts share and mpg."""
import csv, sys, unicodedata, re
TOT = sys.argv[1]; want = [w.lower() for w in sys.argv[2:]]
fold = lambda s: unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
rows = [r for r in csv.DictReader(open(TOT, encoding="utf-8")) if r["season"] >= "2019-20"]
for w in want:
    rs = [r for r in rows if w in fold(r["player"])]
    print("==", w)
    for r in sorted(rs, key=lambda r: (r["season"], r["row"] == "split"), reverse=True):
        g = float(r["g"]); gs = float(r["gs"])
        if g < 15: continue
        print(f"   {r['season']} {r['team']:4s} {r['row']:6s} G{int(g):3d} GS{int(gs):3d} share {gs/g:.2f} mpg {float(r['mp'])/g:.1f}")
