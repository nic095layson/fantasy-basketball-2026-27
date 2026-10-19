"""Owner's predicted weekly H2H vs the real schedule, on the league state (rosters as of the 10/20 Yahoo view).
Model: arena.team_week_model (daily-fill weekly model) on each team's non-IL players, v69 lines; one week = the
house simulator's week_result (shared games shock + per-category normal draws). 10,000 matchups per week per seed."""
import json, math, os, random, sys
DECK = "/home/user/yahoo-fantasy-basketball"; KIT = "/home/user/fantasy-basketball-2026-27"
sys.path.insert(0, DECK + "/scripts"); sys.path.insert(0, DECK + "/arena")
import hoops, arena
hoops.DATA_PATH = os.path.join(DECK, "arena", "results", "players_v69.csv")
players = hoops.zscores(hoops.load_players()); by = {p["player"]: p for p in players}
st = json.load(open(KIT + "/data/league_state.json")); sch = json.load(open(KIT + "/data/league_schedule.json"))
ros, miss = {}, []
for t in st["teams"]:
    ros[t["seat"]] = [by[p["player"]] for p in t["players"] if p["slot"] != "IL" and p["player"] in by]
    miss += [p["player"] for p in t["players"] if p["slot"] != "IL" and p["player"] not in by]
assert not miss, miss
CATS = hoops.CATS; counting = set(hoops.COUNT_COLS)
models = {s: arena.team_week_model(r) for s, r in ros.items()}
sig = {s: {c: math.sqrt(models[s][1][c]) or 1e-6 for c in CATS} for s in ros}
def week(a, b, rng):
    sa, sb = rng.gauss(1, arena.TEAM_WEEK_SHOCK), rng.gauss(1, arena.TEAM_WEEK_SHOCK); won = {}
    for c in CATS:
        ma = models[a][0][c] * (sa if c in counting else 1); mb = models[b][0][c] * (sb if c in counting else 1)
        xa, xb = rng.gauss(ma, sig[a][c]), rng.gauss(mb, sig[b][c])
        won[c] = xa < xb if c == "TO" else xa > xb
    return won
N = int(sys.argv[1]); out = {"n_per_week": N, "seeds": [2026, 2027], "rows": []}
team_name = {t["seat"]: t["name"] for t in st["teams"]}
for o in sch["owner_opponents"]:
    r = {"week": o["week"], "manager": o["manager"], "seat": o["seat"], "team": team_name[o["seat"]]}
    for seed in (2026, 2027):
        rng = random.Random(seed * 100 + o["week"]); wins = 0; cats = 0; per = {c: 0 for c in CATS}
        for _ in range(N):
            w = week(10, o["seat"], rng); k = sum(w.values()); cats += k; wins += k >= 5
            for c in CATS: per[c] += w[c]
        r[f"s{seed}"] = {"p_win": wins / N, "exp_cats": cats / N, "cat_p": {c: per[c] / N for c in CATS}}
    out["rows"].append(r)
json.dump(out, open(sys.argv[2], "w"), indent=1)
for r in out["rows"]:
    a, b = r["s2026"], r["s2027"]; p = (a["p_win"] + b["p_win"]) / 2; se = 1.96 * math.sqrt(p * (1 - p) / (2 * N))
    print(f"wk {r['week']:2d} {r['manager']:7s} {r['team'][:30]:30s} P(win) {a['p_win']:.3f}/{b['p_win']:.3f} ±{se:.3f}  cats {a['exp_cats']:.2f}/{b['exp_cats']:.2f}")
