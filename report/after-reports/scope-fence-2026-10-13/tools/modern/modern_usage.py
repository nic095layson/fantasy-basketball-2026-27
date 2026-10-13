"""Modern-era re-test of new-team usage (owner 2026-10-12). Targets 2019-20..2025-26 only. For season t a team's usage
demand = its players' t-1 usage (FGA + 0.44*FTA + TOV per 36, thin seasons shrunk toward the league with 500 min),
weighted by each player's t-1 minutes per game (rookies: that season's first-year median) — no target-season minutes
used; capacity = the league's t-1 usage (so each season is measured against its own era); k = capacity / demand.
Usage stats (PTS, FGA, FTA, 3PM, TOV per 36) scale by k**alpha. Minutes in t are not predicted here (per-36 errors), so
the test isolates the rate question. alpha is chosen on 2019-20..2022-23 and judged on 2023-24..2025-26; also
leave-one-season-out (alpha chosen on the other six). Player-clustered bootstrap on the judged improvement."""
import csv, json, random, sys, statistics as st
from collections import defaultdict
SRC = "/home/user/fantasy-basketball-2026-27/report/wo5/data/bref_totals_2004-2026.csv"; OUT = sys.argv[1]
MIN_MPG = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0
OPENING = "--opening" in sys.argv   # each player on his first team of the season only (opening-roster proxy; no mid-season trades)
R = list(csv.DictReader(open(SRC, encoding="utf-8")))
seasons = sorted({r["season"] for r in R}); si = {s: i for i, s in enumerate(seasons)}
FIRST, CHOOSE_END, LAST_T = si["2019-20"], si["2022-23"], si["2025-26"]
F = ("g", "mp", "fga", "fta", "tov", "pts", "fg3")
tot = defaultdict(dict); splits = defaultdict(lambda: defaultdict(list))
for r in R:
    d = {k: float(r[k]) for k in F}; d["team"] = r["team"]; t = si[r["season"]]
    (splits[r["pid"]][t].append(d) if r.get("row", "season") == "split" else tot[r["pid"]].__setitem__(t, d))
def teams_in(pid, t): return [(d["team"], d["mp"]) for d in splits[pid][t]] if splits[pid].get(t) else [(tot[pid][t]["team"], tot[pid][t]["mp"])]
if OPENING:
    _ti = teams_in
    def teams_in(pid, t): return _ti(pid, t)[:1]
def U36(d): return (d["fga"] + 0.44 * d["fta"] + d["tov"]) / d["mp"] * 36
league_u, rookie_u, rookie_mpg = {}, {}, {}
for t in range(len(seasons)):
    ds = [tot[p][t] for p in tot if t in tot[p] and tot[p][t]["mp"] > 0]
    league_u[t] = sum(d["fga"] + 0.44 * d["fta"] + d["tov"] for d in ds) / sum(d["mp"] for d in ds) * 36
    fy = [tot[p][t] for p in tot if t in tot[p] and min(tot[p]) == t and t > 0]
    if not fy: continue                      # 2003-04: debut seasons unknown (the file starts there); never used here
    rookie_u[t] = st.median(U36(d) for d in fy if d["mp"] >= 250); rookie_mpg[t] = st.median(d["mp"] / d["g"] for d in fy if d["g"] > 0)
def prior_u(pid, t):
    d = tot[pid].get(t - 1)
    if not d or d["mp"] <= 0: return rookie_u[t - 1]
    return (U36(d) * d["mp"] + league_u[t - 1] * 500) / (d["mp"] + 500)
k_team = {}
for t in range(FIRST, LAST_T + 1):
    dem = defaultdict(lambda: [0.0, 0.0])
    for p in tot:
        if t not in tot[p]: continue
        pd = tot[p].get(t - 1); w = pd["mp"] / pd["g"] if pd and pd["g"] > 0 else rookie_mpg[t - 1]
        tin = teams_in(p, t)
        for team, _ in tin: dem[team][0] += prior_u(p, t) * w / len(tin); dem[team][1] += w / len(tin)
    for team, (um, m) in dem.items(): k_team[(t, team)] = league_u[t - 1] / (um / m)
USAGE = {"pts": "pts", "fga": "fga", "fta": "fta", "tpm": "fg3", "tov": "tov"}
recs = []
for p in tot:
    for t in tot[p]:
        if t < FIRST or (t - 1) not in tot[p]: continue
        a, b = tot[p][t], tot[p][t - 1]
        if a["g"] < 25 or b["g"] < 25 or a["mp"] < 300 or b["mp"] / b["g"] < MIN_MPG: continue
        tin = teams_in(p, t); prev = teams_in(p, t - 1)[-1][0]; prim = max(tin, key=lambda x: x[1])[0]
        k = sum(k_team[(t, tm)] * mp for tm, mp in tin) / sum(mp for _, mp in tin)
        cy = sum(1 for s in tot[p] if s <= t and tot[p][s]["mp"] > 0)
        recs.append(dict(pid=p, t=t, cy=cy, mover=prim != prev, k=k, prior={c: b[s] / b["mp"] * 36 for c, s in USAGE.items()},
                         act={c: a[s] / a["mp"] * 36 for c, s in USAGE.items()}))
def ae(r, alpha, c): return abs(r["prior"][c] * r["k"] ** alpha - r["act"][c])
def mae(sub, alpha, c): return st.mean(ae(r, alpha, c) for r in sub)
GRID = [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]
CH = [r for r in recs if r["t"] <= CHOOSE_END]; JD = [r for r in recs if r["t"] > CHOOSE_END]
fit = {g: round(mae(CH, g, "pts"), 4) for g in GRID}; alpha = min(fit, key=fit.get)
loso = {}
for t in range(FIRST, LAST_T + 1):
    tr = [r for r in recs if r["t"] != t]; f = {g: mae(tr, g, "pts") for g in GRID}; loso[seasons[t]] = min(f, key=f.get)
for r in recs: r["a_loso"] = loso[seasons[r["t"]]]
def boot(sub, alpha_of, c="pts", n=1000, seed=11):
    by = defaultdict(list)
    for r in sub: by[r["pid"]].append(ae(r, alpha_of(r), c) - ae(r, 0, c))
    keys = list(by); rnd = random.Random(seed); m = []
    for _ in range(n):
        s = [x for k in (rnd.choice(keys) for _ in keys) for x in by[k]]; m.append(sum(s) / len(s))
    m.sort(); return round(m[int(.025 * n)], 4), round(m[int(.975 * n)], 4)
GROUPS = {"all": lambda r: True, "stayers": lambda r: not r["mover"], "movers": lambda r: r["mover"],
          "movers to a crowded team (k<0.95)": lambda r: r["mover"] and r["k"] < 0.95, "movers to a thin team (k>1.05)": lambda r: r["mover"] and r["k"] > 1.05,
          "career years 2-8": lambda r: r["cy"] <= 8, "career years 9+": lambda r: r["cy"] >= 9,
          "movers, career years 2-8": lambda r: r["mover"] and r["cy"] <= 8, "movers, career years 9+": lambda r: r["mover"] and r["cy"] >= 9}
out = {"source": SRC, "targets": "2019-20..2025-26", "min_prior_mpg": MIN_MPG, "records": len(recs), "choose": len(CH), "judge": len(JD),
       "alpha_grid_choose_pts_mae": fit, "alpha_chosen": alpha, "alpha_leave_one_season_out": loso,
       "k_spread_2025_26": [round(min(v for (t, _), v in k_team.items() if t == LAST_T), 3), round(max(v for (t, _), v in k_team.items() if t == LAST_T), 3)], "judged": {}, "loso_all_seasons": {}}
for name, f in GROUPS.items():
    sub = [r for r in JD if f(r)]; d = {"n": len(sub), "players": len({r["pid"] for r in sub})}
    for c in USAGE:
        b0, b1 = mae(sub, 0, c), mae(sub, alpha, c); d[c] = {"old_team_rates": round(b0, 4), "usage_fitted": round(b1, 4), "change_pct": round((b1 - b0) / b0 * 100, 2)}
    d["pts_change_ci95"] = boot(sub, lambda r: alpha) if sub else None; out["judged"][name] = d
    sub = [r for r in recs if f(r)]; e = {"n": len(sub)}
    for c in USAGE:
        b0 = st.mean(ae(r, 0, c) for r in sub); b1 = st.mean(ae(r, r["a_loso"], c) for r in sub); e[c] = round((b1 - b0) / b0 * 100, 2)
    e["pts_change_ci95"] = boot(sub, lambda r: r["a_loso"]); out["loso_all_seasons"][name] = e
json.dump(out, open(OUT, "w"), indent=1)
print(f"records {len(recs)} (prior >= {MIN_MPG} min/g; choose {len(CH)}, judge {len(JD)}); 2025-26 team k range {out['k_spread_2025_26']}")
print("alpha by pts/36 error on 2019-23:", fit, "-> alpha", alpha, "| leave-one-season-out alphas:", loso)
print("\nJUDGED on 2023-24..2025-26 (alpha fixed from 2019-23):")
for name, d in out["judged"].items():
    print(f"  {name:36s} n={d['n']:4d}  " + "  ".join(f"{c} {d[c]['change_pct']:+5.1f}%" for c in USAGE) + f"   pts CI {d['pts_change_ci95']}  (pts/36 err {d['pts']['old_team_rates']:.3f}->{d['pts']['usage_fitted']:.3f})")
print("\nLEAVE-ONE-SEASON-OUT, all seven seasons:")
for name, e in out["loso_all_seasons"].items():
    print(f"  {name:36s} n={e['n']:4d}  " + "  ".join(f"{c} {e[c]:+5.1f}%" for c in USAGE) + f"   pts CI {e['pts_change_ci95']}")
