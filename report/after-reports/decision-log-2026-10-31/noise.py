#!/usr/bin/env python3
"""Red team of the decision log (owner 2026-10-31): how noisy is a per-game z-score, against the ±0.5 verdict line
the build prompt proposed on summed box-score z? Per-game z per counting category = (stat − pool per-game mean) /
pool per-game sd over the season pool (percentages: FG%/FT% weighted by attempts the same way); a player's game
residual = his game's summed z minus his own mean; the pooled sd of those residuals is the noise. Beside it, the
correlation between each player's mean per-game z over the box scores on file and his z_adj on the season board,
which says whether the board's scale and the box-score scale agree. Writes noise.json beside this script.

    python3 noise.py --pool <pool_season.csv> --actuals <data/actuals> --board <board_<date>.json>
"""
import argparse, csv, glob, json, math, os, statistics as st, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "scripts"))
import box_pull

ap = argparse.ArgumentParser(); ap.add_argument("--pool", required=True); ap.add_argument("--actuals", required=True)
ap.add_argument("--board", required=True); ap.add_argument("--min-games", type=int, default=5); a = ap.parse_args()
pool = list(csv.DictReader(open(a.pool, encoding="utf-8")))
COUNT = {"pts": "pts", "reb": "reb", "ast": "ast", "stl": "stl", "blk": "blk", "tpm": "tpm", "tov": "tov"}
mu, sd = {}, {}
for c in COUNT:
    v = [float(r[c]) for r in pool]; mu[c], sd[c] = st.mean(v), st.pstdev(v)
for c, m, att in (("fg", "fg_pct", "fga"), ("ft", "ft_pct", "fta")):
    att_mu = st.mean(float(r[att]) for r in pool)
    pct_mu = sum(float(r[m]) * float(r[att]) for r in pool) / sum(float(r[att]) for r in pool)
    imp = [(float(r[m]) - pct_mu) * float(r[att]) / att_mu for r in pool]
    mu[c], sd[c] = (pct_mu, att_mu), st.pstdev(imp)
def game_z(p):
    z = 0.0
    for c in COUNT:
        s = (float(p.get(c) or 0) - mu[c]) / sd[c]; z += -s if c == "tov" else s
    for c, made, att in (("fg", "fgm", "fga"), ("ft", "ftm", "fta")):
        pct_mu, att_mu = mu[c]; A = float(p.get(att) or 0)
        z += (((float(p.get(made) or 0) / A) - pct_mu) * A / att_mu / sd[c]) if A else 0.0
    return z
games = {}
files = sorted(glob.glob(os.path.join(a.actuals, "*.json")))
for f in files:
    for p in json.load(open(f)).get("players", []):
        if p.get("pool_name") and not p.get("dnp") and (p.get("min") or 0) > 0:
            games.setdefault(p["pool_name"], []).append(game_z(p))
res, means = [], {}
for n, zs in games.items():
    if len(zs) >= a.min_games:
        m = st.mean(zs); means[n] = m; res += [z - m for z in zs]
board = json.load(open(a.board))
vals = {r["name"]: r["z_adj"] for r in board["board"]}
idx = box_pull.name_index(list(vals), box_pull.load_aliases())
pairs = [(means[n], vals[box_pull.match_name(n, idx)]) for n in means if box_pull.match_name(n, idx) in vals]
mx, my = st.mean(x for x, _ in pairs), st.mean(y for _, y in pairs)
cov = sum((x - mx) * (y - my) for x, y in pairs); corr = cov / math.sqrt(sum((x - mx) ** 2 for x, _ in pairs) * sum((y - my) ** 2 for _, y in pairs))
noise = st.pstdev(res)
out = dict(box_files=[os.path.basename(f) for f in files], players_with_min_games=len(means), game_residuals=len(res),
           per_game_z_noise_sd=round(noise, 3), weekly_sum_sd_3_5_games=round(noise * math.sqrt(3.5), 3),
           games_to_resolve_half_z_at_2se=round((2 * noise / 0.5) ** 2, 1), corr_mean_game_z_vs_board_z_adj=round(corr, 3), pairs=len(pairs),
           board=os.path.basename(a.board), pool=os.path.basename(a.pool))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "noise.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
