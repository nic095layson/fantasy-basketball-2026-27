"""The daily brief's title-odds headline (daily_brief.py section 5: CG.rosters(state, by) then CG.run_league_sim per
seed, 10,000 seasons) on the live engine, for il_return's never_equals_brief_headline check. Writes {"title": {...}}."""
import json, os, sys, tempfile
W, out = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(W, "scripts"))
import co_gm as CG, il_return as IR
state = json.load(open(CG.STATE, encoding="utf-8"))
P, by = CG.load_pool()
ros = CG.rosters(state, by)
work = tempfile.mkdtemp()
t = {str(s): CG.run_league_sim(ros, s, 10000, work)["teams"][str(CG.OWNER_SEAT)]["champ"] for s in IR.SEEDS}
json.dump({"title": t, "as_of": state.get("as_of"), "how": "daily_brief section 5 code path, live engine"}, open(out, "w"))
print(t)
