import sys, json, os, subprocess, itertools
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, "/home/user/wtsd/scripts"); sys.path.insert(0, "/home/user/wtsd/scripts/redteam")
os.environ["DECK_REPO"] = "/home/user/yahoo-fantasy-basketball"
POOL = os.environ["SEASON_POOL"] = "/home/user/wtsd/data/season/pool_season.csv"
import co_gm as CG
from sweep import variants_from_registry
SEASONS = int(sys.argv[1]); ONLY = sys.argv[2] if len(sys.argv) > 2 else None
reg = json.load(open("/home/user/fantasy-basketball-2026-27/scripts/redteam/constants_registry.json"))
V = [dict(constant="baseline", label="baseline", patch=None)] + variants_from_registry(reg)
state = json.load(open(CG.STATE)); P, by = CG.load_pool()
known = CG.sim_pool_names(POOL)
ros = {t["seat"]: [by[p["player"]] for p in t["players"] if p["slot"] != "IL" and p["player"] in known] for t in state["teams"]}
top = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "f1_pairs.json")))["top"]
R = {"base": ros}
for x in top:
    r2 = {s: list(r) for s, r in ros.items()}
    r2[CG.OWNER_SEAT] = [p for p in r2[CG.OWNER_SEAT] if p["player"] != x["drop"]] + [by[x["add"]]]
    R[f'{x["add"]} for {x["drop"]}'] = r2
def job(a):
    ri, vi, seed = a; tag = f"{ri}_{vi}_{seed}"
    sp, op, pf = f"w/s_{tag}.json", f"w/o_{tag}.json", f"w/p_{tag}.json"
    json.dump(CG.sim_state(list(R.values())[ri]), open(sp, "w"))
    cmd = [sys.executable, os.path.join(CG.DECK, "arena", "mocks", "league_sim.py"), sp, CG.LINES_TAG, str(SEASONS), str(seed), op,
           "--schedule", CG.SCHEDULE, "--season-cv", "--pool", POOL]
    if V[vi]["patch"]: json.dump(V[vi]["patch"], open(pf, "w")); cmd += ["--patch", pf]
    subprocess.run(cmd, check=True, capture_output=True)
    t = json.load(open(op))["teams"][str(CG.OWNER_SEAT)]
    return ri, vi, seed, t["champ"]
os.makedirs("w", exist_ok=True)
jobs = [(r, v, s) for r in range(len(R)) for v in range(len(V)) for s in (2026, 2027)]
if ONLY: jobs = jobs[:int(ONLY)]
with ProcessPoolExecutor(int(os.environ.get("W", "4"))) as ex: res = list(ex.map(job, jobs))
json.dump({"seasons": SEASONS, "rosters": list(R), "variants": V, "results": res, "state_commit": "season/daily 2f80fb0",
           "absent": sorted(p["player"] for t in state["teams"] for p in t["players"] if p["player"] not in known)},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "f1_decisions.json"), "w"), indent=1)
print(res)
