#!/usr/bin/env python3
"""Waiver pickups for the owner's league roster (owner 2026-10-15: "Were there any players undrafted that you recommend
I pick up?"). Every add/drop pair — the 40 best undrafted players by the board's value (availability > 0, owner veto
off) × the owner's 13 — scored by expected weekly category wins against the eleven final rosters (live_retro's pwins
on arena.team_week_model, the card's own ΔECW measure). The best pairs, plus the best AST pair (the weakest category),
then run through the verified league simulator: 10,000 seasons, seed 2026 — the baseline's seed, so the weekly draws
line up and the difference is mostly the move, not the dice. Writes waiver_moves.json."""
import json, math, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); DECK = "/home/user/yahoo-fantasy-basketball"
sys.path.insert(0, DECK + "/scripts"); sys.path.insert(0, DECK + "/arena")
import hoops, arena
hoops.DATA_PATH = f"{DECK}/arena/results/players_v69.csv"
P = hoops.zscores(hoops.load_players()); by = {p["player"]: p for p in P}
st = json.load(open(f"{DECK}/arena/data/states/draft_state_100.json", encoding="utf-8"))
ros = {s: [] for s in range(1, 13)}
for pk in st["picks"]: ros[pk["slot"]].append(by[pk["player"]])
taken = {pk["player"] for pk in st["picks"]}; veto = hoops.do_not_draft()
CATS = hoops.CATS
def pwins(my, opps):
    tot = 0.0
    for om in opps:
        for c in CATS:
            d = (my[0][c] - om[0][c]) / (math.sqrt(my[1][c] + om[1][c]) or 1e-9)
            pr = 0.5 * (1 + math.erf(d / math.sqrt(2))); tot += (1 - pr) if c == "TO" else pr
    return tot / len(opps)
opp = [arena.team_week_model(r) for s, r in ros.items() if s != 10]
mine = ros[10]; base = pwins(arena.team_week_model(mine), opp)
fa = sorted((p for p in P if p["player"] not in taken and hoops.availability(p) > 0 and p["player"] not in veto), key=lambda p: -hoops.adj_value(p, ()))[:40]
pairs = []
for a in fa:
    for d in mine:
        new = [x for x in mine if x is not d] + [a]
        m = arena.team_week_model(new)
        cats = {c: sum(((1 - x) if c == "TO" else x) for x in [0.5 * (1 + math.erf(((m[0][c] - om[0][c]) / (math.sqrt(m[1][c] + om[1][c]) or 1e-9)) / math.sqrt(2))) for om in opp]) / len(opp) for c in CATS}
        pairs.append(dict(add=a["player"], add_team=a["team"], add_pos=a.get("pos"), add_avail=hoops.availability(a), drop=d["player"],
                          d_ecw=round(pwins(m, opp) - base, 4), cats=cats))
pairs.sort(key=lambda x: -x["d_ecw"])
best_by_drop = {}
for x in pairs: best_by_drop.setdefault(x["drop"], x)
base_m = arena.team_week_model(mine)
base_cats = {c: sum(((1 - x) if c == "TO" else x) for x in [0.5 * (1 + math.erf(((base_m[0][c] - om[0][c]) / (math.sqrt(base_m[1][c] + om[1][c]) or 1e-9)) / math.sqrt(2))) for om in opp]) / len(opp) for c in CATS}
for x in pairs: x["d_cats"] = {c: round(x["cats"][c] - base_cats[c], 4) for c in CATS}; del x["cats"]
# who to sim: the top 6 distinct adds (each with its best drop), and the best AST-gaining positive pair
seen, sim = set(), []
for x in pairs:
    if x["add"] not in seen and x["d_ecw"] > 0:
        seen.add(x["add"]); sim.append(x)
    if len(sim) == 6: break
ast = max((x for x in pairs if x["d_ecw"] > 0), key=lambda x: x["d_cats"]["AST"], default=None)
if ast and all(not (ast["add"] == s["add"] and ast["drop"] == s["drop"]) for s in sim): sim.append(ast)
base_sim = json.load(open(f"{DECK}/arena/results/m100_league_sim_10k_s2026.json"))["teams"]["10"]
for x in sim:
    s2 = json.loads(json.dumps(st)); k = next(i for i, pk in enumerate(s2["picks"]) if pk["player"] == x["drop"] and pk["slot"] == 10)
    s2["picks"][k]["player"] = x["add"]; sp = os.path.join(H, "_w_state.json"); op = os.path.join(H, "_w_out.json")
    json.dump(s2, open(sp, "w"), ensure_ascii=False)
    subprocess.run([sys.executable, f"{DECK}/arena/mocks/league_sim.py", sp, "v69", "10000", "2026", op], check=True, capture_output=True)
    r = json.load(open(op))["teams"]["10"]; os.remove(sp); os.remove(op)
    x["sim"] = dict(champ=r["champ"], playoff=r["playoff"], mean_seed=r["mean_seed"], d_champ=round(r["champ"] - base_sim["champ"], 2))
    print(f"+{x['add']:<22} -{x['drop']:<20} dECW {x['d_ecw']:+.4f}  title {r['champ']:.2f}% ({x['sim']['d_champ']:+.2f})  AST {x['d_cats']['AST']:+.3f}")
out = dict(base_ecw=round(base, 4), base_title=base_sim["champ"], candidates=len(fa), pairs=len(pairs), simulated=sim,
           best_by_drop={k: dict(add=v["add"], d_ecw=v["d_ecw"]) for k, v in best_by_drop.items()},
           top20=[{k: v for k, v in x.items()} for x in pairs[:20]],
           positive_pairs=sum(1 for x in pairs if x["d_ecw"] > 0))
json.dump(out, open(os.path.join(H, "waiver_moves.json"), "w"), indent=1, ensure_ascii=False)
print("base ECW", round(base, 4), "| positive pairs", out["positive_pairs"], "of", len(pairs))
print("best add per drop:", {k: (v["add"], v["d_ecw"]) for k, v in best_by_drop.items()})
