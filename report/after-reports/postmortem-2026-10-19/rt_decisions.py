#!/usr/bin/env python3
"""Red team, phase 3b: do the draft's two headline single-swap verdicts survive the structural variants that move the
title level most? Draymond Green for Braun (the pickup) and Jalen Johnson for Durant (the retro's largest miss), each
measured as a title-share difference against the baseline under the same variant, so the structural parameter moves
both sides. Variants: shock 0 / 0.06 / 0.12, no in-sim injury discount. 6,000 seasons, seeds 2026 and 2027. Writes
rt_decisions.json."""
import json, math, os, random, subprocess, sys
from concurrent.futures import ProcessPoolExecutor
H=os.path.dirname(os.path.abspath(__file__)); DECK="/home/user/yahoo-fantasy-basketball"
sys.path.insert(0,DECK+"/scripts"); sys.path.insert(0,DECK+"/arena")
SEASONS=6000; SEEDS=(2026,2027)
SWAPS={"as drafted":[], "Draymond Green for Braun":[("Christian Braun","Draymond Green")], "Jalen Johnson for Durant (#15)":[("Kevin Durant","Jalen Johnson")]}
VARIANTS={"shock 0.06 (shipped)":{}, "shock 0":{"const":{"TEAM_WEEK_SHOCK":0.0}}, "shock 0.12":{"const":{"TEAM_WEEK_SHOCK":0.12}}, "no in-sim injury discount":{"avail":True}}
def run(args):
    swap,var,sd=args
    import importlib, hoops, arena; importlib.reload(arena)
    hoops.DATA_PATH=f"{DECK}/arena/results/players_v69.csv"; P=hoops.zscores(hoops.load_players()); by={p["player"]:p for p in P}
    st=json.load(open(f"{DECK}/arena/data/states/draft_state_100.json")); picks=[dict(p) for p in st["picks"]]
    for drop,add in SWAPS[swap]:
        i=next(k for k,p in enumerate(picks) if p["player"]==drop); j=next((k for k,p in enumerate(picks) if p["player"]==add),None)
        picks[i]["player"]=add
        if j is not None: picks[j]["player"]=drop
    ros={s:[] for s in range(1,13)}
    for pk in picks: ros[pk["slot"]].append(by[pk["player"]])
    patch=VARIANTS[var]
    for k,v in patch.get("const",{}).items(): setattr(arena,k,v)
    if patch.get("avail"):
        orig=arena.weekly_availability; arena.weekly_availability=lambda p,orig=orig:(0.88 if orig(p)==0.75 else orig(p))
    champ,po=arena.simulate_seasons(ros,SEASONS,random.Random(sd))
    return swap,var,sd,100*champ[10]/SEASONS
if __name__=="__main__":
    jobs=[(s,v,sd) for v in VARIANTS for s in SWAPS for sd in SEEDS]
    with ProcessPoolExecutor(4) as ex: R=list(ex.map(run,jobs))
    g={(s,v,sd):c for s,v,sd,c in R}; out={}
    for v in VARIANTS:
        out[v]={}
        for s in SWAPS:
            out[v][s]={sd:dict(title=round(g[(s,v,sd)],2),d_title=round(g[(s,v,sd)]-g[("as drafted",v,sd)],2)) for sd in SEEDS}
    json.dump(dict(engine_commit=subprocess.check_output(["git","-C",DECK,"rev-parse","--short","HEAD"]).decode().strip(),seasons=SEASONS,seeds=list(SEEDS),mc_se_diff_points=round(100*math.sqrt(2*0.22*0.78/SEASONS),2),results=out),open(os.path.join(H,"rt_decisions.json"),"w"),indent=1)
    for v in VARIANTS:
        print(v); 
        for s in SWAPS: print(f"   {s:<32} {out[v][s][2026]['title']:6.2f} / {out[v][s][2027]['title']:6.2f}   d {out[v][s][2026]['d_title']:+.2f} / {out[v][s][2027]['d_title']:+.2f}")
