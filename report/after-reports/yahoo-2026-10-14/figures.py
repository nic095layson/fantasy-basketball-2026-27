"""Figures for the 10/14 Yahoo after-report, from pinned files only. Writes figures_2026-10-14.json.
  - paste shape (rows, ADP, letters) from yahoo-proj-2026-10-14.csv
  - paste vs paste (10/13 -> 10/14) on the shared names: XRank, Rank, ADP, GP, per-game line, letters
  - the re-blend size: for each blended row (report/blend/out/lines_blend_2026-10-14.json), the change each cell would
    take if Yahoo's 10/14 per-game value replaced its 10/13 value as one of the row's equal-weight references
    (cell moves by (new - old) / (n_refs + 1): ours counts one). Measurement only; no line is written."""
import csv, json, os, collections
K = "/home/user/fantasy-basketball-2026-27/report"
M = K + "/market/"
def load(f): return {r["player"]: r for r in csv.DictReader(open(M + f, encoding="utf-8"))}
a, b = load("yahoo-proj-2026-10-13.csv"), load("yahoo-proj-2026-10-14.csv")
pa, pb = load("yahoo-2026-10-13.csv"), load("yahoo-2026-10-14.csv")
pool = {r["name"] for r in csv.DictReader(open(K + "/projections-2026-27.csv", encoding="utf-8"))}
out = {}
rows = list(csv.DictReader(open(M + "yahoo-proj-2026-10-14.csv", encoding="utf-8")))
out["rows"] = len(rows); out["adp"] = sum(1 for r in rows if r["adp"])
out["letters"] = dict(collections.Counter(r["status"] for r in rows if r["status"]))
out["pool_rows_in_paste"] = sum(1 for r in rows if r["player"] in pool)
shared = [n for n in b if n in a]
out["shared"] = len(shared); out["new_names"] = [n for n in b if n not in a]
out["new_pool_names"] = [(n, b[n]["xrank"]) for n in out["new_names"] if n in pool]
out["xrank_changed"] = sum(1 for n in shared if a[n]["xrank"] != b[n]["xrank"])
yr = [(n, int(a[n]["yrank"]), int(b[n]["yrank"])) for n in shared if a[n]["yrank"] != b[n]["yrank"]]
out["yrank_changed"] = len(yr); out["yrank_maxshift"] = max(abs(x - y) for _, x, y in yr) if yr else 0
adp = [(n, a[n]["adp"], b[n]["adp"]) for n in shared if a[n]["adp"] != b[n]["adp"]]
both = [(n, float(x), float(y)) for n, x, y in adp if x and y]
out["adp_changed_both"] = len(both); out["adp_maxshift"] = round(max(abs(x - y) for _, x, y in both), 1)
out["adp_mean_shift"] = round(sum(abs(x - y) for _, x, y in both) / len(both), 2)
out["adp_lost"] = [(n, x) for n, x, y in adp if x and not y]; out["adp_gained"] = [(n, y) for n, x, y in adp if y and not x]
out["adp_up_1"] = sorted([(n, x, y) for n, x, y in both if y - x <= -0.8], key=lambda t: t[2] - t[1])
out["adp_down_1"] = sorted([(n, x, y) for n, x, y in both if y - x >= 0.7], key=lambda t: t[1] - t[2])
CATS = ["pts", "reb", "ast", "stl", "blk", "tpm", "tov", "fg_pct", "ft_pct"]
letters = [(n, a[n]["status"], b[n]["status"]) for n in shared if a[n]["status"] != b[n]["status"]]
out["letters_changed"] = letters
line = []
for n in shared:
    d = {c: (float(a[n][c]), float(b[n][c])) for c in CATS if a[n][c] != b[n][c]}
    gp = (int(a[n]["gp"]), int(b[n]["gp"])) if a[n]["gp"] != b[n]["gp"] else None
    if d or gp: line.append(dict(n=n, gp=gp, cells=d, pool=n in pool))
out["line_changed"] = len(line); out["line_changed_pool"] = sum(1 for x in line if x["pool"])
out["gp_changed"] = sorted([(x["n"], *x["gp"]) for x in line if x["gp"]], key=lambda t: t[2] - t[1])
out["pts_big"] = sorted([(x["n"], *x["cells"]["pts"]) for x in line if "pts" in x["cells"] and abs(x["cells"]["pts"][1] - x["cells"]["pts"][0]) >= 1.5], key=lambda t: t[2] - t[1])
# re-blend size
bl = json.load(open(K + "/blend/out/lines_blend_2026-10-14.json"))["rows"]
by = {r["name"]: r for r in bl}
moves = []
for x in line:
    r = by.get(x["n"])
    if not r: continue
    yref = {c["cat"]: c for c in r["cells"] if "Yahoo" in c["refs"]}
    if not yref: continue
    k = r["n_refs"] + 1
    dc = {c: round((x["cells"][c][1] - x["cells"][c][0]) / k, 4) for c in x["cells"] if c in yref}
    if dc: moves.append(dict(n=x["n"], n_refs=r["n_refs"], d=dc))
out["blend_rows_touched"] = len(moves)
def big(m):
    return any((abs(v) >= 0.3 if c in ("pts", "reb", "ast") else abs(v) >= 0.1 if c in ("stl", "blk", "tpm", "tov") else abs(v) >= 0.005) for c, v in m["d"].items())
out["blend_rows_material"] = [m for m in moves if big(m)]
out["blend_max_pts"] = max((abs(m["d"].get("pts", 0)), m["n"]) for m in moves) if moves else None
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures_2026-10-14.json"), "w"), indent=1, ensure_ascii=False)
for k, v in out.items():
    print(k, ":", json.dumps(v, ensure_ascii=False)[:600])
