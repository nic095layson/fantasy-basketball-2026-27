"""Does a player's longer history predict next season better than last season alone?
Source: report/wo5/data/bref_totals_2004-2026.csv (Basketball-Reference regular-season totals, pinned by sha256).
Targets: every player-season t from 2006-07 to 2025-26 with 25+ games in t and in t-1. Arms predict t's per-game line."""
import csv, json, math, sys, statistics as st
from collections import defaultdict
SRC = "/home/user/fantasy-basketball-2026-27/report/wo5/data/bref_totals_2004-2026.csv"
OUT = sys.argv[1]
rows = [r for r in csv.DictReader(open(SRC, encoding="utf-8")) if r.get("row", "season") != "split"]
seasons = sorted({r["season"] for r in rows}); si = {s: i for i, s in enumerate(seasons)}
P = defaultdict(dict)
for r in rows:
    d = {k: float(r[k]) for k in ("g", "mp", "fg", "fga", "fg3", "ft", "fta", "trb", "ast", "stl", "blk", "tov", "pts")}
    P[r["pid"]][si[r["season"]]] = d
CNT = {"pts": "pts", "reb": "trb", "ast": "ast", "tpm": "fg3", "stl": "stl", "blk": "blk", "tov": "tov"}
CATS = list(CNT) + ["fg_pct", "ft_pct"]
def per36(d, k): return d[k] / d["mp"] * 36 if d["mp"] > 0 else 0.0
def wavg(items):  # [(weight, value)]
    w = sum(a for a, _ in items); return sum(a * b for a, b in items) / w if w > 0 else None
def predict(hist, t):
    """hist: {season_idx: totals}. Returns {arm: {cat: per-game}} using only seasons < t."""
    p1 = hist[t - 1]; mpg1 = p1["mp"] / p1["g"]
    prior3 = [(w, hist[t - k]) for k, w in ((1, 5), (2, 4), (3, 3)) if (t - k) in hist and hist[t - k]["mp"] > 0]
    allp = [hist[s] for s in hist if s < t and hist[s]["mp"] > 0]
    out = {}
    def rate_m3(k): return wavg([(w * d["g"], per36(d, k)) for w, d in prior3])
    def rate_car(k): return sum(d[k] for d in allp) / sum(d["mp"] for d in allp) * 36
    mpg_m3 = wavg([(w * d["g"], d["mp"] / d["g"]) for w, d in prior3])
    for arm in ("PRIOR", "M3_RATES", "CAREER_RATES", "BLEND_RATES", "M3_RATES_M3_MIN"):
        o = {}
        for c, k in CNT.items():
            r1 = per36(p1, k); rm = rate_m3(k); rc = rate_car(k)
            rate = {"PRIOR": r1, "M3_RATES": rm, "CAREER_RATES": rc, "BLEND_RATES": 0.5 * r1 + 0.5 * rm, "M3_RATES_M3_MIN": rm}[arm]
            mins = mpg_m3 if arm == "M3_RATES_M3_MIN" else mpg1
            o[c] = rate * mins / 36
        out[arm] = o
    def pct(made, att, ds): a = sum(d[att] for d in ds); return sum(d[made] for d in ds) / a if a > 0 else None
    fg1 = pct("fg", "fga", [p1]); ft1 = pct("ft", "fta", [p1])
    fgc = pct("fg", "fga", allp); ftc = pct("ft", "fta", allp)
    fgm3 = wavg([(w * d["fga"], d["fg"] / d["fga"]) for w, d in prior3 if d["fga"] > 0]); ftm3 = wavg([(w * d["fta"], d["ft"] / d["fta"]) for w, d in prior3 if d["fta"] > 0])
    P_ = {"PRIOR": (fg1, ft1), "M3_RATES": (fgm3, ftm3), "CAREER_RATES": (fgc, ftc), "BLEND_RATES": ((fg1 + fgm3) / 2 if fg1 and fgm3 else fg1, (ft1 + ftm3) / 2 if ft1 and ftm3 else ft1),
          "M3_RATES_M3_MIN": (fgm3, ftm3)}
    for arm in out: out[arm]["fg_pct"], out[arm]["ft_pct"] = P_[arm]
    out["WO5_SHRINK"] = dict(out["PRIOR"]); out["WO5_SHRINK"]["fg_pct"] = fg1 + (fgc - fg1) / 3 if fg1 and fgc else fg1
    out["WO5_SHRINK"]["ft_pct"] = ft1 + (ftc - ft1) / 3 if ft1 and ftc else ft1
    return out
ARMS = ["PRIOR", "WO5_SHRINK", "M3_RATES", "BLEND_RATES", "CAREER_RATES", "M3_RATES_M3_MIN"]
err = {a: defaultdict(list) for a in ARMS}; per_season = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
strata = defaultdict(lambda: {a: defaultdict(list) for a in ARMS})
n = 0
for pid, hist in P.items():
    first = min(hist)
    for t in hist:
        if t < 3 or (t - 1) not in hist: continue
        a, p1 = hist[t], hist[t - 1]
        if a["g"] < 25 or p1["g"] < 25 or a["mp"] <= 0 or p1["mp"] <= 0: continue
        pred = predict(hist, t)
        act = {c: a[k] / a["g"] for c, k in CNT.items()}
        act["fg_pct"] = a["fg"] / a["fga"] if a["fga"] >= 50 else None; act["ft_pct"] = a["ft"] / a["fta"] if a["fta"] >= 25 else None
        exp = (t - first) if first >= 1 else None          # seasons of history before t (debut known only from 2004-05 on)
        band = None if exp is None else ("1-2 prior seasons" if exp <= 2 else "3-5" if exp <= 5 else "6+")
        n += 1
        for arm in ARMS:
            for c in CATS:
                if act[c] is None or pred[arm][c] is None: continue
                e = abs(pred[arm][c] - act[c])
                if c in ("fg_pct", "ft_pct"):
                    att = a["fga"] / a["g"] if c == "fg_pct" else a["fta"] / a["g"]
                    e = e * att   # error in made-shots terms, so low-volume shooters do not dominate the percentage error
                err[arm][c].append(e)
                per_season[t][arm][c].append((pred[arm][c], act[c]))
                if band: strata[band][arm][c].append(e)
def spearman(pairs):
    def rk(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v)
        for p, i in enumerate(o): r[i] = p + 1
        return r
    a, b = rk([x for x, _ in pairs]), rk([y for _, y in pairs]); n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
res = {"source": SRC, "player_seasons": n, "targets": f"{seasons[3]}..{seasons[-1]}", "arms": {}, "strata": {}}
for arm in ARMS:
    res["arms"][arm] = {c: {"mae": round(st.mean(err[arm][c]), 4), "n": len(err[arm][c]),
                            "mean_season_spearman": round(st.mean(spearman(per_season[t][arm][c]) for t in per_season if len(per_season[t][arm][c]) > 30), 4)} for c in CATS}
for band, d in strata.items():
    res["strata"][band] = {arm: {c: round(st.mean(d[arm][c]), 4) for c in CATS if d[arm][c]} for arm in ARMS}
    res["strata"][band]["n"] = len(d["PRIOR"]["pts"])
json.dump(res, open(OUT, "w"), indent=1)
print("player-seasons:", n, res["targets"])
hdr = "arm".ljust(17) + "".join(c.rjust(9) for c in CATS); print(hdr)
for arm in ARMS: print(arm.ljust(17) + "".join(f"{res['arms'][arm][c]['mae']:9.4f}" for c in CATS))
print("mean within-season Spearman (ordering):")
for arm in ARMS: print(arm.ljust(17) + "".join(f"{res['arms'][arm][c]['mean_season_spearman']:9.4f}" for c in CATS))
for band in sorted(res["strata"]):
    print(f"-- {band} (n={res['strata'][band]['n']}) MAE"); 
    for arm in ARMS: print("  " + arm.ljust(15) + "".join(f"{res['strata'][band][arm].get(c, float('nan')):9.4f}" for c in CATS))
