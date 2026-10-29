import sys, json, os
sys.path.insert(0, "/home/user/wtsd/scripts")
os.environ["DECK_REPO"] = "/home/user/yahoo-fantasy-basketball"
os.environ["SEASON_POOL"] = "/home/user/wtsd/data/season/pool_season.csv"
import co_gm as CG
from concurrent.futures import ProcessPoolExecutor
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "w"), exist_ok=True)
state = json.load(open("/home/user/wtsd/data/news/league_state_am_2026-10-29.json")); P, by = CG.load_pool()
il = CG.rosters(state, by)
act = {s: list(r) for s, r in il.items()}
act[CG.OWNER_SEAT] = act[CG.OWNER_SEAT] + [by["Tyrese Haliburton"]]
def job(a):
    tag, seed = a; r = il if tag == "il" else act
    rec = CG.run_league_sim(r, seed, 10000, os.path.join(os.path.dirname(os.path.abspath(__file__)), "w"), tag=f"{tag}{seed}")
    t = rec["teams"][str(CG.OWNER_SEAT)]; return tag, seed, t["champ"], t["playoff"], rec["absent_from_sim"]
with ProcessPoolExecutor(4) as ex: res = list(ex.map(job, [(t, s) for t in ("il", "active") for s in (2026, 2027)]))
for r in res: print(r[:4], "absent", r[4])
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dis8.json"), "w"), indent=1)
