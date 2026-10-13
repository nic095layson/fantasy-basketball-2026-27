"""New-team usage: does fitting a player's shot volume to his new team's usage budget predict better than carrying his
old-team rates? Basketball-Reference totals 2004-2026 (pinned). For each season t the team's usage demand is the
minutes-weighted average of its players' PRIOR-season usage (FGA + 0.44*FTA + TOV per 36); the league's average actual
usage in t-1 is the capacity; k = capacity / demand. A player's usage-driven stats (PTS, FGA, FTA, 3PM, TOV) scale by
k**alpha. Minutes in t are taken as known (in practice they are a separate projected input). alpha is fit on
2006-07..2015-16 and judged on 2016-17..2025-26 — nothing from the test seasons chooses it."""
import csv, json, math, sys, statistics as st
from collections import defaultdict
SRC = "/home/user/fantasy-basketball-2026-27/report/wo5/data/bref_totals_2004-2026.csv"; OUT = sys.argv[1]
WEIGHTS = sys.argv[2] if len(sys.argv) > 2 else "actual"; BASE = sys.argv[3] if len(sys.argv) > 3 else "prior"
R = list(csv.DictReader(open(SRC, encoding="utf-8")))
seasons = sorted({r["season"] for r in R}); si = {s: i for i, s in enumerate(seasons)}
F = ("g", "mp", "fga", "fta", "tov", "pts", "fg3", "ast", "fg", "ft")
tot = defaultdict(dict); splits = defaultdict(lambda: defaultdict(list))
for r in R:
    d = {k: float(r[k]) for k in F}; d["team"] = r["team"]; t = si[r["season"]]
    if r.get("row", "season") == "split": splits[r["pid"]][t].append(d)
    else: tot[r["pid"]][t] = d
def teams_in(pid, t):
    """[(team, minutes)] for season t, chronological."""
    if splits[pid].get(t): return [(d["team"], d["mp"]) for d in splits[pid][t]]
    d = tot[pid][t]; return [(d["team"], d["mp"])]
def U36(d): return (d["fga"] + 0.44 * d["fta"] + d["tov"]) / d["mp"] * 36 if d["mp"] > 0 else None
league_u = {}; rookie_u = {}; rookie_mpg = {}
for t in range(len(seasons)):
    ds = [tot[p][t] for p in tot if t in tot[p] and tot[p][t]["mp"] > 0]
    league_u[t] = sum(d["fga"] + 0.44 * d["fta"] + d["tov"] for d in ds) / sum(d["mp"] for d in ds) * 36
    first = [U36(tot[p][t]) for p in tot if t in tot[p] and min(tot[p]) == t and t > 0 and tot[p][t]["mp"] >= 250]
    rookie_u[t] = st.median(first) if first else league_u[t]
    fm = [tot[p][t]["mp"] / tot[p][t]["g"] for p in tot if t in tot[p] and min(tot[p]) == t and t > 0 and tot[p][t]["g"] > 0]
    rookie_mpg[t] = st.median(fm) if fm else 12.0
def prior_u(pid, t):
    d = tot[pid].get(t - 1)
    if not d or d["mp"] <= 0: return rookie_u.get(t - 1, league_u[t - 1])
    u = U36(d); return (u * d["mp"] + league_u[t - 1] * 500) / (d["mp"] + 500)   # shrink thin seasons toward the league
k_team = {}
for t in range(1, len(seasons)):
    dem = defaultdict(lambda: [0.0, 0.0])
    for p in tot:
        if t not in tot[p]: continue
        u = prior_u(p, t)
        tin = teams_in(p, t)
        if WEIGHTS == "prior_mpg":
            # leak-free: the player's prior-season minutes per game (rookies: the league's first-year median), split over the
            # teams he was rostered by in t in proportion to games there would also leak, so only his roster teams are used
            pd = tot[p].get(t - 1); w = (pd["mp"] / pd["g"]) if pd and pd["g"] > 0 else rookie_mpg.get(t - 1, 12.0)
            tin = [(tm, w / len(tin)) for tm, _ in tin]
        for team, mp in tin:
            dem[team][0] += u * mp; dem[team][1] += mp
    for team, (um, m) in dem.items():
        if m > 0: k_team[(t, team)] = league_u[t - 1] / (um / m)
USAGE = {"pts": "pts", "fga": "fga", "fta": "fta", "tpm": "fg3", "tov": "tov"}
recs = []
for p in tot:
    for t in tot[p]:
        if t < 3 or (t - 1) not in tot[p]: continue
        a, b = tot[p][t], tot[p][t - 1]
        if a["g"] < 25 or b["g"] < 25 or a["mp"] < 300 or b["mp"] < 300: continue
        tin = teams_in(p, t); last_prev = teams_in(p, t - 1)[-1][0]
        prim = max(tin, key=lambda x: x[1])[0]
        k = sum(k_team[(t, tm)] * mp for tm, mp in tin) / sum(mp for _, mp in tin)
        k_prev_same = k_team.get((t - 1, last_prev))
        pr = {c: b[s] / b["mp"] * 36 for c, s in USAGE.items()}
        if BASE == "blend":
            # half last season, half the games-weighted 5/4/3 three-season rate (the history test's best counting arm)
            hist = [(w * tot[p][t - kk]["g"], tot[p][t - kk]) for kk, w in ((1, 5), (2, 4), (3, 3)) if (t - kk) in tot[p] and tot[p][t - kk]["mp"] > 0]
            m3 = {c: sum(w * d[s] / d["mp"] * 36 for w, d in hist) / sum(w for w, _ in hist) for c, s in USAGE.items()}
            pr = {c: 0.5 * pr[c] + 0.5 * m3[c] for c in pr}
        recs.append(dict(t=t, mover=prim != last_prev, k=k, prior=pr,
                         act={c: a[s] / a["mp"] * 36 for c, s in USAGE.items()}))
def mae(sub, alpha, c):
    return st.mean(abs(r["prior"][c] * r["k"] ** alpha - r["act"][c]) for r in sub)
TRAIN = [r for r in recs if r["t"] <= si["2015-16"]]; TEST = [r for r in recs if r["t"] > si["2015-16"]]
grid = [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]
fit = {g: mae(TRAIN, g, "pts") for g in grid}; alpha = min(fit, key=fit.get)
out = {"weights": WEIGHTS, "base": BASE, "source": SRC, "records": len(recs), "train": len(TRAIN), "test": len(TEST), "alpha_grid_train_pts_mae": fit, "alpha_chosen": alpha, "test": {}}
for name, sub in (("all", TEST), ("movers", [r for r in TEST if r["mover"]]), ("stayers", [r for r in TEST if not r["mover"]]),
                  ("movers_k<0.95 (crowded new team)", [r for r in TEST if r["mover"] and r["k"] < 0.95]),
                  ("movers_k>1.05 (thin new team)", [r for r in TEST if r["mover"] and r["k"] > 1.05])):
    out["test"][name] = {"n": len(sub)}
    for c in USAGE:
        base, adj = mae(sub, 0, c), mae(sub, alpha, c)
        out["test"][name][c] = {"mae_old_team_rates": round(base, 4), "mae_usage_fitted": round(adj, 4), "change_pct": round((adj - base) / base * 100, 2)}
json.dump(out, open(OUT, "w"), indent=1)
print("records", len(recs), "train", len(TRAIN), "test", len(TEST)); print("alpha fit on train (pts/36 MAE):", {g: round(v, 4) for g, v in fit.items()}, "-> alpha", alpha)
for name, d in out["test"].items():
    print(f"{name:36s} n={d['n']:5d}  " + "  ".join(f"{c}: {d[c]['mae_old_team_rates']:.3f}->{d[c]['mae_usage_fitted']:.3f} ({d[c]['change_pct']:+.1f}%)" for c in USAGE))
