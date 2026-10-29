#!/usr/bin/env python3
"""Red team, phase 4: the simulator draws continuous normals, so no category ever ties. Real weekly counting stats are
integers, and Yahoo scores a tie as a T for both. This discretizes the same draws (round to integers; percentages to
three decimals, Yahoo's display) for the owner's 11 matchups and counts the tied categories per matchup, 20,000 weeks
per opponent on two seeds. Writes rt_ties.json."""
import json, math, os, random, sys
H=os.path.dirname(os.path.abspath(__file__)); DECK="/home/user/yahoo-fantasy-basketball"
sys.path.insert(0,DECK+"/scripts"); sys.path.insert(0,DECK+"/arena"); import hoops, arena
hoops.DATA_PATH=f"{DECK}/arena/results/players_v69.csv"; P=hoops.zscores(hoops.load_players()); by={p["player"]:p for p in P}
st=json.load(open(f"{DECK}/arena/data/states/draft_state_100.json")); CATS=hoops.CATS; COUNT=set(hoops.COUNT_COLS)
ros={s:[] for s in range(1,13)}
for pk in st["picks"]: ros[pk["slot"]].append(by[pk["player"]])
M={s:arena.team_week_model(r) for s,r in ros.items()}; SG={s:{c:math.sqrt(M[s][1][c]) for c in CATS} for s in ros}
out={}
for sd in (2026,2027):
    rng=random.Random(sd); N=20000; ties={c:0 for c in CATS}; tot=0; owner_delta=0.0
    for o in ros:
        if o==10: continue
        for _ in range(N):
            sa=rng.gauss(1,arena.TEAM_WEEK_SHOCK); sb=rng.gauss(1,arena.TEAM_WEEK_SHOCK)
            for c in CATS:
                ma=M[10][0][c]*(sa if c in COUNT else 1); mb=M[o][0][c]*(sb if c in COUNT else 1)
                xa=rng.gauss(ma,SG[10][c]); xb=rng.gauss(mb,SG[o][c])
                if c in COUNT: xa,xb=round(xa),round(xb)
                else: xa,xb=round(xa,3),round(xb,3)
                if xa==xb: ties[c]+=1
            tot+=1
    out[sd]=dict(matchups=tot,tie_rate_by_cat={c:ties[c]/tot for c in CATS},tied_cats_per_matchup=sum(ties.values())/tot)
json.dump(dict(out,engine_commit=__import__("subprocess").check_output(["git","-C",DECK,"rev-parse","--short","HEAD"]).decode().strip()),open(os.path.join(H,"rt_ties.json"),"w"),indent=1)
for sd in out: print(sd,{c:round(v,4) for c,v in out[sd]["tie_rate_by_cat"].items()},"per matchup",round(out[sd]["tied_cats_per_matchup"],3))
