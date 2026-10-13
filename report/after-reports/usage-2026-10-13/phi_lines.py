#!/usr/bin/env python3
"""Maxey and Philadelphia's other stars: their last three seasons (Basketball-Reference totals, kit-pinned), the kit line
behind the practice page (git 89fe5a5^1) and today's shipped line, and the outside PROJECTIONS on file (Yahoo 10/13,
Hashtag 10/12, RotoBaller 9/29). Rotoworld's sheet and the 9/26 projected-150 carry last season's actuals, not
projections, so only their ranks appear; RotoWire carries a rank and a note. Per-game figures; minutes where a source has them."""
import csv, io, os, subprocess
H = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.normpath(os.path.join(H, "..", "..", ".."))
M = os.path.join(KIT, "report", "market")
NAMES = ["Tyrese Maxey", "Jaylen Brown", "LeBron James", "Joel Embiid", "VJ Edgecombe"]
f = lambda x: float(x) if x not in ("", None, "-") else None
def rows(text): return {r.get("name") or r.get("player"): r for r in csv.DictReader(io.StringIO(text))}
bref = [r for r in csv.DictReader(open(os.path.join(KIT, "report/wo5/data/bref_totals_2004-2026.csv"))) if r["row"] == "season"]
now = rows(open(os.path.join(KIT, "report/projections-2026-27.csv"), encoding="utf-8").read())
old = rows(subprocess.run(["git", "-C", KIT, "show", "89fe5a5^1:report/projections-2026-27.csv"], capture_output=True, text=True, check=True).stdout)
yp = rows(open(os.path.join(M, "yahoo-proj-2026-10-13.csv"), encoding="utf-8").read())
ht = rows(open(os.path.join(M, "hashtag-2026-10-12.csv"), encoding="utf-8").read())
rb = rows(open(os.path.join(M, "rotoballer-2026-09-29.csv"), encoding="utf-8").read())
rw = rows(open(os.path.join(M, "rotoworld-2026-10-05.csv"), encoding="utf-8").read())
rt = rows(open(os.path.join(M, "rotowire-2026-10-09.csv"), encoding="utf-8").read())
fmt = lambda v, d=1: "-" if v is None else f"{v:.{d}f}"
for n in NAMES:
    print(f"== {n}")
    print("  source | GP | min | shots | points | threes | assists | rebounds")
    for b in sorted((r for r in bref if r["player"] == n and r["season"] in ("2023-24", "2024-25", "2025-26")), key=lambda r: r["season"]):
        g = float(b["g"]); pg = lambda c: float(b[c]) / g
        print(f"  {b['season']} actual ({b['team']}) | {g:.0f} | {pg('mp'):.1f} | {pg('fga'):.1f} | {pg('pts'):.1f} | {pg('fg3'):.1f} | {pg('ast'):.1f} | {pg('trb'):.1f}")
    for lab, src in (("practice-era kit line", old), ("today's shipped line", now)):
        r = src.get(n)
        if r: print(f"  {lab} | {r['gp']} | {r['mpg']} | {r['fga']} | {r['pts']} | {r['tpm']} | {r['ast']} | {r['reb']}")
    r = yp.get(n); print(f"  Yahoo 10/13 projection | {r['gp']} | - | - | {r['pts']} | {r['tpm']} | {r['ast']} | {r['reb']}" if r else "  Yahoo 10/13: not on file")
    r = ht.get(n); print(f"  Hashtag 10/12 projection | {r['gp']} | {r['mpg']} | {r['fga']} | {r['pts']} | {r['tpm']} | {r['ast']} | {r['reb']}" if r else "  Hashtag 10/12: not on file")
    r = rb.get(n); print(f"  RotoBaller 9/29 projection | - | - | - | {r['src_pts']} | {r['src_tpm']} | {r['src_ast']} | {r['src_reb']}" if r else "  RotoBaller 9/29: not on file")
    r = rw.get(n); print(f"  Rotoworld 10/05 9-cat rank {r['src_rank']}" if r else "  Rotoworld: not on file")
    r = rt.get(n); print(f"  RotoWire 10/09 rank {r['src_rank']} — {r['flag']}: {r['claim'][:240]}" if r else "  RotoWire: not on file")
