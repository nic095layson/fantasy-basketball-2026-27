#!/usr/bin/env python3
"""Owner 2026-10-15: "Can you please conduct a retro analysis of the players available at each of my picks, and let me
know who could have been the better pick, and the winning % shift?"

For each of the owner's 13 turns, the hindsight file (deck arena/results/m100_hindsight.json) lists every legal
alternative scored by expected weekly category wins (ECW) against the final rosters. This takes the top three
alternatives with a positive ECW gain at each turn (or, where none beat the owner's pick, the single best alternative,
to show the margin) and swaps each in pairwise, as card_vs_owner.py and the house arms do: if another seat drafted the
alternative later, that seat gets the owner's player; if nobody drafted it, the owner's player goes undrafted. Each swap
runs through the verified league simulator, 10,000 seasons on seeds 2026 and 2027 (the baselines' seeds, so the swap
and the baseline share their random draws). Single swaps: the shifts do not add up across turns; one combined hindsight-ceiling board is run separately.
Writes retro_picks.json."""
import json, math, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
H = os.path.dirname(os.path.abspath(__file__)); DECK = "/home/user/yahoo-fantasy-basketball"
sys.path.insert(0, DECK + "/scripts"); sys.path.insert(0, DECK + "/arena")
import hoops, arena
hoops.DATA_PATH = f"{DECK}/arena/results/players_v69.csv"
P = hoops.zscores(hoops.load_players()); by = {p["player"]: p for p in P}
st = json.load(open(f"{DECK}/arena/data/states/draft_state_100.json", encoding="utf-8"))
hind = json.load(open(f"{DECK}/arena/results/m100_hindsight.json", encoding="utf-8"))
CATS = hoops.CATS; SEEDS = (2026, 2027); TOPK = 3


def ecw(picks):
    ros = {s: [] for s in range(1, 13)}
    for pk in picks: ros[pk["slot"]].append(by[pk["player"]])
    my = arena.team_week_model(ros[10]); tot = 0.0
    for s, r in ros.items():
        if s == 10: continue
        om = arena.team_week_model(r)
        for c in CATS:
            d = (my[0][c] - om[0][c]) / (math.sqrt(my[1][c] + om[1][c]) or 1e-9)
            pr = 0.5 * (1 + math.erf(d / math.sqrt(2))); tot += (1 - pr) if c == "TO" else pr
    return tot / 11


def swap(n, tg):
    picks = [dict(pk) for pk in st["picks"]]; mine = picks[n]["player"]
    j = next((i for i, pk in enumerate(picks) if pk["player"] == tg), None)
    picks[n]["player"] = tg
    if j is not None: picks[j]["player"] = mine
    return picks, j


def sim(job):
    key, picks, sd = job
    sp = os.path.join(H, f"_rp_{key}_{sd}_state.json"); op = os.path.join(H, f"_rp_{key}_{sd}_out.json")
    json.dump(dict(st, picks=picks), open(sp, "w"), ensure_ascii=False)
    subprocess.run([sys.executable, f"{DECK}/arena/mocks/league_sim.py", sp, "v69", "10000", str(sd), op], check=True, capture_output=True)
    r = json.load(open(op))["teams"]["10"]; os.remove(sp); os.remove(op)
    return key, sd, r["champ"], r["playoff"]


base_e = ecw(st["picks"])
bfile = {sd: json.load(open(f"{DECK}/arena/results/m100_league_sim_10k_s{sd}.json"))["teams"]["10"] for sd in SEEDS}
base = {sd: bfile[sd]["champ"] for sd in SEEDS}; base_po = {sd: bfile[sd]["playoff"] for sd in SEEDS}
assert abs(hind["base_ecw"] - base_e) < 1e-6, (hind["base_ecw"], base_e)
rows, jobs = [], []
for t in sorted(hind["turns"], key=lambda t: t["pick"]):
    n = t["pick"] - 1; assert st["picks"][n]["player"] == t["actual"] and st["picks"][n]["slot"] == 10
    pos = [a for a in t["top"] if a["gain"] > 0][:TOPK] or t["top"][:1]
    for a in pos:
        picks, j = swap(n, a["n"]); e = ecw(picks)
        assert abs((e - base_e) - a["gain"]) < 5e-4, (t["pick"], a["n"], e - base_e, a["gain"])
        key = f"{t['pick']}_{len(rows)}"
        rows.append(dict(key=key, pick=t["pick"], owner=t["actual"], alt=a["n"], alt_pos=a["pos"], alt_team=a["t"],
                         alt_went=(f"#{j + 1} seat {st['picks'][j]['slot']}" if j is not None else "undrafted"),
                         d_ecw=round(e - base_e, 4), card_rank=a["card_rank"], beat_owner=a["gain"] > 0,
                         n_better=t["n_better"], n_legal=t["n_legal"]))
        jobs += [(key, picks, sd) for sd in SEEDS]
with ThreadPoolExecutor(4) as ex: res = list(ex.map(sim, jobs))
got = {(k, sd): (c, p) for k, sd, c, p in res}
for r in rows:
    r["d_title"] = {sd: round(got[(r["key"], sd)][0] - base[sd], 2) for sd in SEEDS}
    r["d_playoff"] = {sd: round(got[(r["key"], sd)][1] - base_po[sd], 2) for sd in SEEDS}
    r["d_title_mean"] = round(sum(r["d_title"].values()) / 2, 2); del r["key"]
# Hindsight ceiling: at every turn, in pick order, the alternative with the best mean title shift among players not
# already used at an earlier turn (only shifts above +0.5, the noise line), all swapped pairwise into one board.
used, combo, picks = set(), [], [dict(pk) for pk in st["picks"]]
for pk_no in sorted({r["pick"] for r in rows}):
    c = [r for r in rows if r["pick"] == pk_no and r["alt"] not in used and r["d_title_mean"] > 0.5]
    if not c: continue
    b = max(c, key=lambda r: r["d_title_mean"]); used.add(b["alt"]); n = pk_no - 1; mine = picks[n]["player"]
    j = next((i for i, x in enumerate(picks) if x["player"] == b["alt"]), None)
    picks[n]["player"] = b["alt"]
    if j is not None: picks[j]["player"] = mine
    combo.append(dict(pick=pk_no, owner=b["owner"], alt=b["alt"]))
cres = {sd: sim(("combo", picks, sd)) for sd in SEEDS}
ceiling = dict(swaps=combo, d_ecw=round(ecw(picks) - base_e, 4),
               d_title={sd: round(cres[sd][2] - base[sd], 2) for sd in SEEDS}, title={sd: round(cres[sd][2], 2) for sd in SEEDS},
               d_playoff={sd: round(cres[sd][3] - base_po[sd], 2) for sd in SEEDS})
out = dict(base_ecw=round(base_e, 4), base_title=base, base_playoff=base_po, seasons=10000, seeds=list(SEEDS), rows=rows, ceiling=ceiling)
json.dump(out, open(os.path.join(H, "retro_picks.json"), "w"), indent=1, ensure_ascii=False)
print(f"base title {base[2026]:.2f} / {base[2027]:.2f}   base ECW {base_e:.4f}")
for r in rows:
    print(f"#{r['pick']:>3} {r['owner']:<20} alt {r['alt']:<22} ({r['alt_went']:>14})  dECW {r['d_ecw']:+.4f}  dTitle {r['d_title'][2026]:+.2f} / {r['d_title'][2027]:+.2f}  mean {r['d_title_mean']:+.2f}")
print("ceiling:", [f"#{c['pick']} {c['alt']}" for c in combo], "dECW", ceiling["d_ecw"], "title", ceiling["title"], "dTitle", ceiling["d_title"], "dPlayoff", ceiling["d_playoff"])
