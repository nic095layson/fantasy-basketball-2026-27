#!/usr/bin/env python3
"""Owner 2026-10-15: "How were my opponents' picks compared to their historical tendencies?" Each manager's 2026 picks
measured the same ways their history was, from the records:
  - value reach: pick − 9-cat value rank (room_model.py's formula: hoops.adj_value over the available pool), mean and
    early (R1–6); 2025-26 recomputed with room_model's own pool (players_2025-10-21.csv) and board, 2026 on the lock pool;
    the two pools differ, so levels compare loosely and the ORDER of managers is the firmer comparison;
  - market reach (2026 only; no earlier ADP file exists): pick − Yahoo ADP (kit report/market/yahoo-2026-10-14.csv);
  - guard share: picks eligible at PG/SG (2026 from Yahoo's listing; earlier seasons from the lock pool's positions,
    names that are no longer in the pool skipped);
  - repeats: players the manager also drafted in 2023-24, 2024-25 or 2025-26 (arena/draft_boards.json), and hits on the
    loyalty pairs and model predictions in arena/profiles.json.
Writes opponents_vs_history.json."""
import csv, json, os, sys, unicodedata
H = os.path.dirname(os.path.abspath(__file__)); DECK = "/home/user/yahoo-fantasy-basketball"; KIT = os.path.normpath(os.path.join(H, "..", "..", ".."))
sys.path.insert(0, DECK + "/scripts"); import hoops
def norm(n):
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().replace(".", "").replace("'", "").lower()
    for suf in (" jr", " iii", " ii", " iv"):
        if n.endswith(suf): n = n[: -len(suf)]
    return " ".join(n.split())
def vranks(path):
    hoops.DATA_PATH = path; pl = hoops.zscores(hoops.load_players())
    av = sorted((p for p in pl if hoops.availability(p) > 0), key=lambda p: -hoops.adj_value(p))
    return {norm(p["player"]): i + 1 for i, p in enumerate(av)}, {norm(p["player"]): p for p in pl}
v25, _ = vranks(f"{DECK}/arena/data/players_2025-10-21.csv")
v26, pool26 = vranks(f"{DECK}/arena/results/players_v69.csv")
boards = json.load(open(f"{DECK}/arena/draft_boards.json", encoding="utf-8"))
prof = json.load(open(f"{DECK}/arena/profiles.json", encoding="utf-8"))["managers"]
recap = json.load(open(os.path.join(H, "recap.json"), encoding="utf-8"))
adp = {norm(r["player"]): float(r["adp"]) for r in csv.DictReader(open(f"{KIT}/report/market/yahoo-2026-10-14.csv", encoding="utf-8")) if r.get("adp")}
is_g = lambda pos: any(x in ("PG", "SG") for x in (pos or "").split(","))
def reach(picks, vr):
    d = [(n, n - vr[norm(nm)]) for n, nm in picks if norm(nm) in vr]
    e = [x for n, x in d if n <= 72]
    return dict(n=len(d), mean=round(sum(x for _, x in d) / len(d), 1) if d else None, early=round(sum(e) / len(e), 1) if e else None)
out = {}
for s in range(1, 13):
    m = next(p["manager"] for p in recap if p["slot"] == s)
    if m == "Me": continue
    mine = [(p["n"], p["player"]) for p in recap if p["slot"] == s]
    r26 = reach(mine, v26)
    mk = [(n, n - adp[norm(nm)]) for n, nm in mine if norm(nm) in adp]
    mk_e = [x for n, x in mk if n <= 72]
    g26 = sum(1 for p in recap if p["slot"] == s and is_g(p["pos"]))
    hist = {}
    for season, b in boards.items():
        ps = [(x["pick"], x["player"]) for x in b if x["manager"] == m]
        known = [nm for _, nm in ps if norm(nm) in pool26]
        hist[season] = dict(picks=[nm for _, nm in ps], guard_share=round(sum(1 for nm in known if is_g(pool26[norm(nm)].get("pos"))) / len(known), 2) if known else None, n_pos=len(known))
    r25 = reach([(x["pick"], x["player"]) for x in boards["2025-26"] if x["manager"] == m], v25)
    prior = {norm(nm): season for season in ("2023-24", "2024-25", "2025-26") for nm in hist[season]["picks"]}
    repeats = sorted({nm for _, nm in mine if norm(nm) in prior})
    loy = prof.get(m, {}).get("loyalty", {}); loyal = [x for k in ("3peat", "2peat") for x in loy.get(k, [])]
    loy_hit = [x for x in loyal if norm(x) in {norm(nm) for _, nm in mine}]
    loy_elsewhere = {x: next((f"#{p['n']} {p['manager']}" for p in recap if norm(p["player"]) == norm(x)), "undrafted") for x in loyal if x not in loy_hit}
    out[m] = dict(seat=s, team=next(p["team_name"] for p in recap if p["slot"] == s), picks=[nm for _, nm in mine],
                  reach_2026=r26, reach_2025=r25, profile_reach_early_2526=prof.get(m, {}).get("reach_early_2526"),
                  market_reach_2026=dict(n=len(mk), mean=round(sum(x for _, x in mk) / len(mk), 1) if mk else None, early=round(sum(mk_e) / len(mk_e), 1) if mk_e else None),
                  guard_share_2026=round(g26 / 13, 2), guard_share_hist={k: v["guard_share"] for k, v in hist.items()},
                  repeats=repeats, loyalty_listed=loyal, loyalty_hit=loy_hit, loyalty_went=loy_elsewhere,
                  profile_model=prof.get(m, {}).get("model"), profile_read=prof.get(m, {}).get("read"))
# rank agreement between 2025-26 and 2026 early value reach (Spearman, no ties assumed)
ms = [m for m in out if out[m]["reach_2025"]["early"] is not None and out[m]["reach_2026"]["early"] is not None]
def ranks(v): o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v); [r.__setitem__(i, k) for k, i in enumerate(o)]; return r
a = ranks([out[m]["reach_2025"]["early"] for m in ms]); b = ranks([out[m]["reach_2026"]["early"] for m in ms]); n = len(ms)
rho = 1 - 6 * sum((x - y) ** 2 for x, y in zip(a, b)) / (n * (n * n - 1))
res = dict(managers=out, spearman_early_reach_2025_vs_2026=round(rho, 3), n=n)
json.dump(res, open(os.path.join(H, "opponents_vs_history.json"), "w"), indent=1, ensure_ascii=False)
print(f"{'mgr':<7}{'early25':>8}{'early26':>8}{'mean25':>8}{'mean26':>8}{'mkt26':>7}{'mktE26':>7}  G26  G25/G24/G23   repeats | loyalty hit / went")
for m, x in sorted(out.items(), key=lambda kv: kv[1]["seat"]):
    gh = x["guard_share_hist"]
    print(f"{m:<7}{x['reach_2025']['early']:>8}{x['reach_2026']['early']:>8}{x['reach_2025']['mean']:>8}{x['reach_2026']['mean']:>8}{x['market_reach_2026']['mean']:>7}{x['market_reach_2026']['early']:>7}  {x['guard_share_2026']:.2f} {gh['2025-26']}/{gh['2024-25']}/{gh['2023-24']}  {x['repeats']} | {x['loyalty_hit']} / {x['loyalty_went']}")
print("spearman early reach 2025 vs 2026:", res["spearman_early_reach_2025_vs_2026"], "n", n)
