#!/usr/bin/env python3
"""Holiday and Portland's other guards (owner question 2026-10-13: Lillard, Morant, Henderson and Holiday on one roster):
their last three seasons (Basketball-Reference totals, kit-pinned; multi-team seasons print the season row and each
team's split), the kit line behind the practice page (git 89fe5a5^1) and today's shipped line, and the outside
PROJECTIONS on file (Yahoo 10/13, Hashtag 10/12, RotoBaller 9/29). Rotoworld's sheet carries last season's actuals,
not projections, so only its rank appears; RotoWire carries a rank and a note. Per-game figures; minutes where a source
has them. Same sources and columns as phi_lines.py, plus Portland's two incumbent forwards (Avdija, Camara) and each
player's value rank and market rank on the practice page (Version 59) and the live page (Version 64), from
../live-mock-2026-10-13/val_v59.json and val_v64.json."""
import csv, io, json, os, subprocess
H = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.normpath(os.path.join(H, "..", "..", ".."))
M = os.path.join(KIT, "report", "market")
NAMES = ["Jrue Holiday", "Damian Lillard", "Ja Morant", "Scoot Henderson", "Deni Avdija", "Toumani Camara"]
VAL = {v: {r["n"]: r for r in json.load(open(os.path.join(H, "..", "live-mock-2026-10-13", f"val_{v}.json"), encoding="utf-8"))} for v in ("v59", "v64")}
def rows(text): return {r.get("name") or r.get("player"): r for r in csv.DictReader(io.StringIO(text))}
bref = list(csv.DictReader(open(os.path.join(KIT, "report/wo5/data/bref_totals_2004-2026.csv"))))
now = rows(open(os.path.join(KIT, "report/projections-2026-27.csv"), encoding="utf-8").read())
old = rows(subprocess.run(["git", "-C", KIT, "show", "89fe5a5^1:report/projections-2026-27.csv"], capture_output=True, text=True, check=True).stdout)
yp = rows(open(os.path.join(M, "yahoo-proj-2026-10-13.csv"), encoding="utf-8").read())
ht = rows(open(os.path.join(M, "hashtag-2026-10-12.csv"), encoding="utf-8").read())
rb = rows(open(os.path.join(M, "rotoballer-2026-09-29.csv"), encoding="utf-8").read())
rw = rows(open(os.path.join(M, "rotoworld-2026-10-05.csv"), encoding="utf-8").read())
rt = rows(open(os.path.join(M, "rotowire-2026-10-09.csv"), encoding="utf-8").read())
for n in NAMES:
    print(f"== {n}")
    print("  source | GP | min | shots | points | threes | assists | rebounds | turnovers")
    seasons = sorted((r for r in bref if r["player"] == n and r["season"] in ("2023-24", "2024-25", "2025-26")),
                     key=lambda r: (r["season"], r["row"] != "season"))
    for s in ("2023-24", "2024-25", "2025-26"):
        if not any(b["season"] == s for b in seasons): print(f"  {s} actual | no row (no games that season)")
    for b in seasons:
        g = float(b["g"]); pg = lambda c: float(b[c]) / g
        lab = f"{b['season']} actual ({b['team']})" if b["row"] == "season" else f"    {b['season']} split ({b['team']})"
        print(f"  {lab} | {g:.0f} | {pg('mp'):.1f} | {pg('fga'):.1f} | {pg('pts'):.1f} | {pg('fg3'):.1f} | {pg('ast'):.1f} | {pg('trb'):.1f} | {pg('tov'):.1f}")
    for lab, src in (("practice-era kit line", old), ("today's shipped line", now)):
        r = src.get(n)
        print(f"  {lab} ({r['team']}) | {r['gp']} | {r['mpg']} | {r['fga']} | {r['pts']} | {r['tpm']} | {r['ast']} | {r['reb']} | {r['tov']}" if r else f"  {lab}: not in the file")
    r = yp.get(n); print(f"  Yahoo 10/13 projection | {r['gp']} | - | - | {r['pts']} | {r['tpm']} | {r['ast']} | {r['reb']} | {r['tov']}" if r else "  Yahoo 10/13: not on file")
    r = ht.get(n); print(f"  Hashtag 10/12 projection | {r['gp']} | {r['mpg']} | {r['fga']} | {r['pts']} | {r['tpm']} | {r['ast']} | {r['reb']} | {r['tov']}" if r else "  Hashtag 10/12: not on file")
    r = rb.get(n); print(f"  RotoBaller 9/29 projection | - | - | - | {r['src_pts']} | {r['src_tpm']} | {r['src_ast']} | {r['src_reb']} | {r['src_tov']}" if r else "  RotoBaller 9/29: not on file")
    r = rw.get(n); print(f"  Rotoworld 10/05 9-cat rank {r['src_rank']}" if r else "  Rotoworld: not on file")
    r = rt.get(n); print(f"  RotoWire 10/09 rank {r['src_rank']} — {r['flag']}: {r['claim'][:300]}" if r else "  RotoWire: not on file")
    print("  value / market rank: practice page (Version 59) " + " / ".join(str(VAL["v59"][n][k]) for k in ("valRank", "mktRank"))
          + "; live page (Version 64) " + " / ".join(str(VAL["v64"][n][k]) for k in ("valRank", "mktRank")))
# the pool as the kit holds it today, and the team-budget row
print("== Portland's pool today (kit projections-2026-27.csv), by projected minutes x games")
pool = sorted((r for r in now.values() if r["team"] == "POR"), key=lambda r: -float(r["mpg"]) * float(r["gp"]))
for r in pool:
    b = [x for x in bref if x["player"] == r["name"] and x["season"] == "2025-26" and x["row"] == "season"]
    last = f"{b[0]['team']} {float(b[0]['g']):.0f} games" if b else "no 2025-26 games"
    print(f"  {r['name']} | {r['pos']} | GP {r['gp']} | min {r['mpg']} | shots {r['fga']} | points {r['pts']} | assists {r['ast']} | 2025-26: {last}")
