import sys, json, os
sys.path.insert(0, "/home/user/wtsd/scripts")
os.environ["DECK_REPO"] = "/home/user/yahoo-fantasy-basketball"
os.environ["SEASON_POOL"] = "/home/user/wtsd/data/season/pool_season.csv"
import co_gm as CG, daily_brief as DB
date = "2026-10-28"
state = json.load(open(CG.STATE)); P, by = CG.load_pool(); ros = {t["seat"]: [by[p["player"]] for p in t["players"] if p["slot"] != "IL" and p["player"] in by] for t in state["teams"]}; print("dropped", [p["player"] for t in state["teams"] for p in t["players"] if p["player"] not in by])
y, e = DB.status_inputs(date); st = CG.fa_status(P, y, e, date=date)
fa, aside = CG.free_agents(P, state, st)
base, pairs = CG.waiver_pairs(ros, fa)
pos = [x for x in pairs if x["d_ecw"] > 0]; top, seen = [], set()
for x in pos:
    if x["add"] not in seen: seen.add(x["add"]); top.append(x)
    if len(top) == 3: break
mine = [p["player"] for p in ros[CG.OWNER_SEAT]]
print("pool", CG.lines_label() if hasattr(CG,"lines_label") else "", "mine", len(mine), "Portis" in " ".join(mine), "Haliburton" in " ".join(mine))
print("aside", [a["player"] for a in aside]); print("base", base, "pos", len(pos), "of", len(pairs))
for x in top: print(x, st["by"].get(x["add"],{}).get("code"))
json.dump({"base_ecw": base, "top": top, "n_pos": len(pos), "n": len(pairs)}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "f1_pairs.json"),"w"), indent=1)
