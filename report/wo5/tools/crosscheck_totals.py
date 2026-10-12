"""P2: the 2025-26 bref totals divided by games must reproduce the recorded, two-outlet-verified per-game file
(arena/results/actuals_2026-10-09/actuals_2025-26.csv) within rounding (0.051 on counts, 0.0006 on percentages).
Also 2024-25 and 2023-24 against their recorded files."""
import csv, sys, unicodedata, re
T, D = sys.argv[1], sys.argv[2]
def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'`,’-]", "", s); s = re.sub(r"[^a-z0-9 ]", " ", s)
    return " ".join(x for x in s.split() if x not in {"jr", "sr", "ii", "iii", "iv"})
tot = {}
for r in csv.DictReader(open(T, encoding="utf-8")):
    tot.setdefault(r["season"], {}).setdefault(norm(r["player"]), []).append(r)
bad = 0; n = 0; amb = 0
for season in ("2025-26", "2024-25", "2023-24"):
    rec = list(csv.DictReader(open(f"{D}/actuals_{season}.csv", encoding="utf-8")))
    sb = 0; sn = 0
    for r in rec:
        c = tot.get(season, {}).get(norm(r["player"]))
        if not c: continue
        if len(c) > 1: amb += 1; continue
        t = c[0]; g = float(t["g"]); sn += 1
        if g == 0: continue
        chk = {"gp": (g, float(r["gp"]), 0.0), "mpg": (float(t["mp"]) / g, float(r["mpg"]), 0.051), "pts": (float(t["pts"]) / g, float(r["pts"]), 0.051),
               "reb": (float(t["trb"]) / g, float(r["reb"]), 0.051), "ast": (float(t["ast"]) / g, float(r["ast"]), 0.051),
               "stl": (float(t["stl"]) / g, float(r["stl"]), 0.051), "blk": (float(t["blk"]) / g, float(r["blk"]), 0.051),
               "tov": (float(t["tov"]) / g, float(r["tov"]), 0.051), "tpm": (float(t["fg3"]) / g, float(r["tpm"]), 0.051),
               "fga": (float(t["fga"]) / g, float(r["fga"]), 0.051), "fta": (float(t["fta"]) / g, float(r["fta"]), 0.051)}
        if float(t["fga"]): chk["fg_pct"] = (float(t["fg"]) / float(t["fga"]), float(r["fg_pct"]), 0.0006)
        if float(t["fta"]): chk["ft_pct"] = (float(t["ft"]) / float(t["fta"]), float(r["ft_pct"]), 0.0006)
        errs = [(k, round(a, 4), b) for k, (a, b, tol) in chk.items() if abs(a - b) > tol]
        if errs:
            sb += 1
            if sb <= 6: print(season, r["player"], errs)
    print(f"{season}: {sn} matched rows, {sb} with any cell outside rounding")
    bad += sb; n += sn
print(f"total matched {n}, mismatched {bad}, ambiguous names skipped {amb}")
