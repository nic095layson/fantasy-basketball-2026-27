"""Modern-era re-test (owner 2026-10-12: the 20-season window is the wrong era). Does history beyond last season help?
Targets 2019-20..2025-26 only (the data's own plateau: league 3PM/36 1.82-2.02, usage/36 16.5-16.9). Inputs reach back
at most three seasons (to 2016-17) except the CAREER arm and the shipped FG%/FT% career pull, which are career by
definition. Choose on 2019-20..2022-23, judge on 2023-24..2025-26; per-season wins; player-clustered bootstrap.
Fantasy-relevant = 20+ min/g and 25+ games the season before, 25+ games in the target season."""
import csv, json, math, random, sys, statistics as st
from collections import defaultdict
SRC = "/home/user/fantasy-basketball-2026-27/report/wo5/data/bref_totals_2004-2026.csv"; OUT = sys.argv[1]
MIN_MPG = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0
rows = [r for r in csv.DictReader(open(SRC, encoding="utf-8")) if r.get("row", "season") != "split"]
seasons = sorted({r["season"] for r in rows}); si = {s: i for i, s in enumerate(seasons)}
FIRST, CHOOSE_END, LAST_T = si["2019-20"], si["2022-23"], si["2025-26"]
P = defaultdict(dict)
for r in rows:
    P[r["pid"]][si[r["season"]]] = {k: float(r[k]) for k in ("g", "mp", "fg", "fga", "fg3", "ft", "fta", "trb", "ast", "stl", "blk", "tov", "pts")}
CNT = {"pts": "pts", "reb": "trb", "ast": "ast", "tpm": "fg3", "stl": "stl", "blk": "blk", "tov": "tov"}
CATS = list(CNT) + ["fg_pct", "ft_pct"]
def r36(d, k): return d[k] / d["mp"] * 36
def three(hist, t):  # games-weighted 5/4/3 over t-1, t-2, t-3 (the shipped steals/blocks anchor)
    return [(w, hist[t - j]) for j, w in ((1, 5), (2, 4), (3, 3)) if (t - j) in hist and hist[t - j]["mp"] > 0]
def rate3(items, k): return sum(w * d["g"] * r36(d, k) for w, d in items) / sum(w * d["g"] for w, d in items)
def pct3(items, m, a):
    den = sum(w * d[a] for w, d in items); return sum(w * d[m] for w, d in items) / den if den > 0 else None
def pct(ds, m, a):
    den = sum(d[a] for d in ds); return sum(d[m] for d in ds) / den if den > 0 else None
def predict(hist, t):
    p1 = hist[t - 1]; mpg = p1["mp"] / p1["g"]; it = three(hist, t); car = [hist[s] for s in hist if s < t and hist[s]["mp"] > 0]
    rate = {"last": {c: r36(p1, k) for c, k in CNT.items()}, "three": {c: rate3(it, k) for c, k in CNT.items()},
            "career": {c: sum(d[k] for d in car) / sum(d["mp"] for d in car) * 36 for c, k in CNT.items()}}
    rate["blend"] = {c: 0.5 * rate["last"][c] + 0.5 * rate["three"][c] for c in CNT}
    fg = {"last": pct([p1], "fg", "fga"), "three": pct3(it, "fg", "fga"), "career": pct(car, "fg", "fga")}
    ft = {"last": pct([p1], "ft", "fta"), "three": pct3(it, "ft", "fta"), "career": pct(car, "ft", "fta")}
    def mix(d, a, b, w):  # w of the way from a toward b
        return d[a] + w * (d[b] - d[a]) if d[a] is not None and d[b] is not None else d[a]
    arms = {
        "LAST (last season only)":            ("last", None, ("last",)),
        "SHIPPED (WO-5 as on the board)":      ("last", "three", ("shrink", "career")),
        "SHIPPED, pct pull to 3 seasons":      ("last", "three", ("shrink", "three")),
        "THREE (5/4/3 three seasons)":         ("three", None, ("pure", "three")),
        "BLEND (half last, half three)":       ("blend", None, ("half", "three")),
        "CAREER (career averages)":            ("career", None, ("pure", "career")),
    }
    out = {}
    for name, (cnt, sb, pr) in arms.items():
        o = {c: rate[cnt][c] * mpg / 36 for c in CNT}
        if sb: o["stl"], o["blk"] = rate[sb]["stl"] * mpg / 36, rate[sb]["blk"] * mpg / 36
        for key, d in (("fg_pct", fg), ("ft_pct", ft)):
            if pr == ("last",): o[key] = d["last"]
            elif pr[0] == "shrink": o[key] = mix(d, "last", pr[1], 1 / 3)
            elif pr[0] == "half": o[key] = mix(d, "last", pr[1], 0.5)
            else: o[key] = d[pr[1]] if d[pr[1]] is not None else d["last"]
        out[name] = o
    return out
ARMS = list(predict({0: P["garneke01"][0], 1: P["garneke01"][1], 2: P["garneke01"][2]}, 2))
recs = []
for pid, hist in P.items():
    for t in hist:
        if t < FIRST or (t - 1) not in hist: continue
        a, p1 = hist[t], hist[t - 1]
        if a["g"] < 25 or p1["g"] < 25 or a["mp"] <= 0 or p1["mp"] / p1["g"] < MIN_MPG: continue
        cy = sum(1 for s in hist if s <= t and hist[s]["mp"] > 0)          # career year of the target season
        act = {c: a[k] / a["g"] for c, k in CNT.items()}
        act["fg_pct"] = a["fg"] / a["fga"] if a["fga"] >= 50 else None; act["ft_pct"] = a["ft"] / a["fta"] if a["fta"] >= 25 else None
        recs.append(dict(pid=pid, t=t, cy=cy, act=act, att={"fg_pct": a["fga"] / a["g"], "ft_pct": a["fta"] / a["g"]}, pred=predict(hist, t)))
# category scale: the spread of the actual values among these player-seasons (percentages in made-shot impact terms)
lg = {"fg_pct": st.mean(r["act"]["fg_pct"] for r in recs if r["act"]["fg_pct"]), "ft_pct": st.mean(r["act"]["ft_pct"] for r in recs if r["act"]["ft_pct"])}
SD = {c: st.pstdev([r["act"][c] for r in recs]) for c in CNT}
for c in ("fg_pct", "ft_pct"): SD[c] = st.pstdev([(r["act"][c] - lg[c]) * r["att"][c] for r in recs if r["act"][c]])
def errs(r, arm):
    e = {}
    for c in CATS:
        if r["act"][c] is None or r["pred"][arm][c] is None: continue
        x = abs(r["pred"][arm][c] - r["act"][c]); e[c] = x * r["att"][c] if c.endswith("pct") else x
    return e
for r in recs:
    r["e"] = {arm: errs(r, arm) for arm in ARMS}
    r["comp"] = {arm: st.mean(r["e"][arm][c] / SD[c] for c in r["e"][arm]) for arm in ARMS}
STRATA = {"all fantasy-relevant": lambda r: True, "career years 2-8": lambda r: r["cy"] <= 8, "  years 2-3": lambda r: r["cy"] <= 3,
          "  years 4-8": lambda r: 4 <= r["cy"] <= 8, "career years 9+": lambda r: r["cy"] >= 9}
def boot(sub, arm, ref, n=1000, seed=7):
    by = defaultdict(list)
    for r in sub: by[r["pid"]].append(r["comp"][arm] - r["comp"][ref])
    keys = list(by); rnd = random.Random(seed); m = []
    for _ in range(n):
        s = [x for k in (rnd.choice(keys) for _ in keys) for x in by[k]]; m.append(sum(s) / len(s))
    m.sort(); return round(m[int(.025 * n)], 4), round(m[int(.975 * n)], 4)
res = {"source": SRC, "targets": "2019-20..2025-26", "min_prior_mpg": MIN_MPG, "n": len(recs), "scale_sd": {c: round(v, 4) for c, v in SD.items()}, "strata": {}}
for sname, f in STRATA.items():
    sub = [r for r in recs if f(r)]; ch = [r for r in sub if r["t"] <= CHOOSE_END]; jd = [r for r in sub if r["t"] > CHOOSE_END]
    d = {"n": len(sub), "players": len({r["pid"] for r in sub}), "n_choose": len(ch), "n_judge": len(jd), "arms": {}}
    for arm in ARMS:
        cat = {c: round(st.mean(r["e"][arm][c] for r in sub if c in r["e"][arm]), 4) for c in CATS}
        seas = [t for t in range(FIRST, LAST_T + 1) if any(r["t"] == t for r in sub)]
        wins = sum(1 for t in seas if st.mean(r["comp"][arm] for r in sub if r["t"] == t) < st.mean(r["comp"][ARMS[0]] for r in sub if r["t"] == t))
        d["arms"][arm] = {"composite": round(st.mean(r["comp"][arm] for r in sub), 4), "composite_choose": round(st.mean(r["comp"][arm] for r in ch), 4),
                          "composite_judge": round(st.mean(r["comp"][arm] for r in jd), 4), "per_cat_mae": cat,
                          "seasons_better_than_LAST": f"{wins}/{len(seas)}",
                          "diff_vs_LAST_ci95": boot(sub, arm, ARMS[0]) if arm != ARMS[0] else None,
                          "diff_vs_SHIPPED_ci95": boot(sub, arm, ARMS[1]) if arm != ARMS[1] else None}
    best = min(ARMS, key=lambda a: d["arms"][a]["composite_choose"]); d["chosen_on_2019_23"] = best
    d["judged_2023_26"] = {a: d["arms"][a]["composite_judge"] for a in (best, ARMS[0], ARMS[1])}
    res["strata"][sname] = d
json.dump(res, open(OUT, "w"), indent=1)
print(f"player-seasons {len(recs)} (targets 2019-20..2025-26, prior >= {MIN_MPG} min/g)  scale SD:", res["scale_sd"])
for sname, d in res["strata"].items():
    print(f"\n== {sname}: n={d['n']} ({d['players']} players; choose {d['n_choose']}, judge {d['n_judge']})  chosen on 2019-23: {d['chosen_on_2019_23']}  judged 2023-26: {d['judged_2023_26']}")
    print("   arm".ljust(36) + "comp".rjust(7) + "".join(c.rjust(8) for c in CATS) + "  wins  diff-vs-LAST CI      diff-vs-SHIPPED CI")
    for arm, a in d["arms"].items():
        print("   " + arm.ljust(33) + f"{a['composite']:7.4f}" + "".join(f"{a['per_cat_mae'][c]:8.4f}" for c in CATS) + f"  {a['seasons_better_than_LAST']:>4}  {str(a['diff_vs_LAST_ci95']):18s} {a['diff_vs_SHIPPED_ci95']}")
