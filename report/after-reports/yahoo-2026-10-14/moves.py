"""Market-order moves V68 -> V69 from the two built pages' PLAYERS arrays (mkt = Yahoo price; unpriced rows ride
the internal order after the priced ones). Writes moves_v68_v69.json."""
import json, re, sys
def players(path):
    s = open(path, encoding="utf-8").read()
    i = s.index("const PLAYERS = ") + len("const PLAYERS = ")
    arr, _ = json.JSONDecoder().raw_decode(s[i:])
    return arr
def order(P):
    pr = sorted([p for p in P if p.get("mkt") is not None], key=lambda p: (p["mkt"], p["n"]))
    return {p["n"]: k + 1 for k, p in enumerate(pr)}, {p["n"]: (p.get("mkt"), p.get("mktsrc")) for p in P}
D = sys.argv[1]
a, pa = order(players(f"{D}/page_v68.html")); b, pb = order(players(f"{D}/page_v69_built.html"))
moves = sorted([(n, a.get(n), b.get(n), pa[n], pb[n]) for n in pb if a.get(n) != b.get(n)], key=lambda x: -abs((x[2] or 999) - (x[1] or 999)))
both = [m for m in moves if m[1] and m[2]]
out = dict(priced_v68=len(a), priced_v69=len(b), order_changes=len(both), newly=[m for m in moves if not m[1]],
           mean_shift=round(sum(abs(m[2]-m[1]) for m in both)/len(both), 2) if both else 0,
           max5=[m for m in both][:8], top156_changes=sum(1 for m in both if min(m[1], m[2]) <= 156))
json.dump(out, open(f"{D}/moves_v68_v69.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, ensure_ascii=False)[:2500])
