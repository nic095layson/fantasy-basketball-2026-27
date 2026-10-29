import sys, json, os, subprocess
sys.path.insert(0, "/home/user/wtsd/scripts")
os.environ["DECK_REPO"] = "/home/user/yahoo-fantasy-basketball"
POOL = os.environ["SEASON_POOL"] = "/home/user/wtsd/data/season/pool_season.csv"
import co_gm as CG
state = json.load(open("/home/user/wtsd/data/news/league_state_am_2026-10-28.json")); P, by = CG.load_pool()
ros = CG.rosters(state, by)
for s in (2026, 2027):
    print(s, CG.run_league_sim(ros, s, 10000, "w")["teams"][str(CG.OWNER_SEAT)]["champ"])
print([p["player"] for t in state["teams"] if t["seat"]==CG.OWNER_SEAT for p in t["players"] if p["slot"]=="IL"])
