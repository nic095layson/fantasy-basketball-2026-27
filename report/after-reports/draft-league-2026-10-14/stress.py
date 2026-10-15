#!/usr/bin/env python3
"""Injury stress arms for the owner's league roster, through the verified league simulator (league_sim.py,
10,000 seasons, seed 2026): each of the owner's four headline names in turn misses the WHOLE season and his slot is
filled by the best undrafted player on the board (the waiver pickup a manager would make). Also writes the
undrafted top 15 by the board's value (the waiver wire at the draft's end). Writes stress.json and waiver.json."""
import json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); DECK = "/home/user/yahoo-fantasy-basketball"
sys.path.insert(0, DECK + "/scripts"); import hoops
hoops.DATA_PATH = f"{DECK}/arena/results/players_v69.csv"
P = hoops.zscores(hoops.load_players())
st = json.load(open(f"{DECK}/arena/data/states/draft_state_100.json", encoding="utf-8"))
taken = {pk["player"] for pk in st["picks"]}
veto = hoops.do_not_draft()
fa = sorted((p for p in P if p["player"] not in taken and hoops.availability(p) > 0), key=lambda p: -hoops.adj_value(p, ()))
waiver = [dict(player=p["player"], team=p["team"], pos=p.get("pos"), value=round(hoops.adj_value(p, ()), 3),
               availability=hoops.availability(p), note=hoops.note_tag(p.get("note")), owner_veto=p["player"] in veto) for p in fa[:15]]
json.dump(waiver, open(os.path.join(H, "waiver.json"), "w"), indent=1, ensure_ascii=False)
repl = next(p["player"] for p in fa if p["player"] not in veto)
out = dict(replacement=repl, seasons=10000, seed=2026, arms={})
for nm in ("Tyrese Haliburton", "Kevin Durant", "Kawhi Leonard", "Kyrie Irving"):
    s2 = json.loads(json.dumps(st))
    k = next(i for i, pk in enumerate(s2["picks"]) if pk["player"] == nm and pk["slot"] == 10)
    s2["picks"][k]["player"] = repl
    sp = os.path.join(H, f"stress_state_{nm.split()[-1].lower()}.json"); json.dump(s2, open(sp, "w"), ensure_ascii=False, indent=0)
    op = os.path.join(H, f"stress_{nm.split()[-1].lower()}.json")
    subprocess.run([sys.executable, f"{DECK}/arena/mocks/league_sim.py", sp, "v69", "10000", "2026", op], check=True, capture_output=True)
    r = json.load(open(op))["teams"]
    best_other = max((s for s in r if s != "10"), key=lambda s: r[s]["champ"])
    out["arms"][nm] = dict(champ=r["10"]["champ"], playoff=r["10"]["playoff"], mean_seed=r["10"]["mean_seed"],
                           cats_per_week=r["10"]["cats_per_week"],
                           champ_rank=1 + sum(1 for s in r if s != "10" and r[s]["champ"] > r["10"]["champ"]),
                           top_rival=(int(best_other), r[best_other]["champ"]))
    os.remove(sp)
    print(nm, "->", repl, out["arms"][nm])
json.dump(out, open(os.path.join(H, "stress.json"), "w"), indent=1, ensure_ascii=False)
print("waiver top 5:", [(w["player"], w["value"]) for w in waiver[:5]])
