#!/usr/bin/env python3
"""Did Yahoo's 10/13 paste change any projection? Join Yahoo's 10/06 and 10/13 projected-stats files (both pinned in the kit,
report/market/yahoo-proj-2026-10-06.csv and -2026-10-13.csv) on the kit's resolved player name and count changes per field."""
import csv, os
H = os.path.dirname(os.path.abspath(__file__))
M = os.path.normpath(os.path.join(H, "..", "..", "market"))
a = {r["player"]: r for r in csv.DictReader(open(os.path.join(M, "yahoo-proj-2026-10-06.csv")))}
b = {r["player"]: r for r in csv.DictReader(open(os.path.join(M, "yahoo-proj-2026-10-13.csv")))}
shared = sorted(set(a) & set(b))
print(f"names: 10/06 {len(a)} · 10/13 {len(b)} · shared {len(shared)} · 10/13 only {len(set(b) - set(a))} · 10/06 only {sorted(set(a) - set(b))}")
LINE = ["gp", "fg_pct", "ft_pct", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]
for f in LINE:
    ch = [n for n in shared if (a[n][f] or "") != (b[n][f] or "")]
    print(f"  {f:<7} changed on {len(ch)} of {len(shared)}" + (f" e.g. {ch[:3]}" if ch else ""))
anyline = [n for n in shared if any((a[n][f] or "") != (b[n][f] or "") for f in LINE)]
print(f"any projection field changed: {len(anyline)} of {len(shared)}")
for f in ["xrank", "yrank", "adp", "status"]:
    ch = [n for n in shared if (a[n].get(f) or "") != (b[n].get(f) or "")]
    mx = max((abs(float(a[n][f]) - float(b[n][f])) for n in ch if a[n].get(f) and b[n].get(f) and f != "status"), default=None)
    print(f"  {f:<7} changed on {len(ch)} of {len(shared)}" + (f" · largest move {mx:g}" if mx is not None else ""))
