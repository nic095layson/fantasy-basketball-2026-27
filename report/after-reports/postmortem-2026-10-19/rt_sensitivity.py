#!/usr/bin/env python3
"""Red team, phase 3: the owner's title share under each assumption the simulator makes, one at a time, on the final
rosters. arena.simulate_seasons (the house simulator league_sim.py is verified equal to) with the constant patched:
regular-season weeks 17 (shipped) / 18 / 20; the playoff bracket fixed instead of reseeded (shipped); standings by weekly wins instead of the category record; the in-sim availability
tiers (healthy 0.88, risk 0.75) moved; the shared games shock at 0 / 0.06 / 0.12; per-game variance scaled 0.8 / 1.2;
category independence broken by a second shared shock on the percentages. 6,000 seasons on seeds 2026 and 2027 per
variant (Monte-Carlo SE about 0.53 points at 22%). Writes rt_sensitivity.json."""
import json, math, os, random, subprocess, sys
from concurrent.futures import ProcessPoolExecutor
H=os.path.dirname(os.path.abspath(__file__)); DECK="/home/user/yahoo-fantasy-basketball"
sys.path.insert(0,DECK+"/scripts"); sys.path.insert(0,DECK+"/arena")
SEASONS=6000; SEEDS=(2026,2027)
def run(args):
    name,patch,sd=args
    import importlib, hoops, arena
    importlib.reload(arena)  # a fresh module per job: patches must not leak between jobs sharing a worker process
    hoops.DATA_PATH=f"{DECK}/arena/results/players_v69.csv"; P=hoops.zscores(hoops.load_players()); by={p["player"]:p for p in P}
    st=json.load(open(f"{DECK}/arena/data/states/draft_state_100.json"))
    ros={s:[] for s in range(1,13)}
    for pk in st["picks"]: ros[pk["slot"]].append(by[pk["player"]])
    for k,v in patch.get("const",{}).items(): setattr(arena,k,v)
    if "avail" in patch:
        h,r=patch["avail"]; orig=arena.weekly_availability
        arena.weekly_availability=lambda p,h=h,r=r,orig=orig: (r if orig(p)==0.75 else h if orig(p)==0.88 else orig(p))
    if patch.get("fixed_bracket"):
        def fixed_champion(top, week_result):  # the bracket that shipped until 2026-10-15: no reseed after round 1
            qf=[(top[0],top[7]),(top[3],top[4]),(top[1],top[6]),(top[2],top[5])]
            w1=[a if week_result(a,b)>=5 else b for a,b in qf]
            sf=[(w1[0],w1[1]),(w1[2],w1[3])]
            w2=[a if week_result(a,b)>=5 else b for a,b in sf]
            return w2[0] if week_result(*w2)>=5 else w2[1]
        arena.playoff_champion=fixed_champion
    if "cv" in patch:
        arena.CV={c:v*patch["cv"] for c,v in arena.CV.items()}
    rng=random.Random(sd)
    if patch.get("weekly_win") or patch.get("pct_shock"):
        # re-implementation of simulate_seasons with the one rule changed (same draw order otherwise)
        models={i:arena.team_week_model(r) for i,r in ros.items()}; CATS=hoops.CATS; counting=set(hoops.COUNT_COLS)
        sig={i:{c:math.sqrt(models[i][1][c]) or 1e-6 for c in CATS} for i in ros}
        def week(a,b):
            sa=rng.gauss(1,arena.TEAM_WEEK_SHOCK); sb=rng.gauss(1,arena.TEAM_WEEK_SHOCK)
            pa=rng.gauss(0,1) if patch.get("pct_shock") else 0; pb=rng.gauss(0,1) if patch.get("pct_shock") else 0
            w=0
            for c in CATS:
                ma=models[a][0][c]*(sa if c in counting else 1); mb=models[b][0][c]*(sb if c in counting else 1)
                xa=rng.gauss(ma,sig[a][c]); xb=rng.gauss(mb,sig[b][c])
                if c in ("FG%","FT%") and patch.get("pct_shock"):
                    xa+=patch["pct_shock"]*sig[a][c]*pa; xb+=patch["pct_shock"]*sig[b][c]*pb
                w+=1 if ((xa<xb) if c=="TO" else (xa>xb)) else 0
            return w
        ids=list(ros); champ={i:0 for i in ids}; po={i:0 for i in ids}
        for _ in range(SEASONS):
            rec={i:0.0 for i in ids}
            for _w in range(arena.WEEKS):
                pr=ids[:]; rng.shuffle(pr)
                for k in range(0,12,2):
                    a,b=pr[k],pr[k+1]; wa=week(a,b)
                    if patch.get("weekly_win"): rec[a]+=1 if wa>=5 else 0; rec[b]+=1 if wa<5 else 0
                    else: rec[a]+=wa; rec[b]+=9-wa
            seeds=sorted(ids,key=lambda i:(-rec[i],rng.random())); top=seeds[:8]
            for i in top: po[i]+=1
            champ[arena.playoff_champion(top,week)]+=1
    else:
        champ,po=arena.simulate_seasons(ros,SEASONS,rng)
    return name,sd,100*champ[10]/SEASONS,100*po[10]/SEASONS,{i:100*champ[i]/SEASONS for i in champ}
VARIANTS={
 "baseline (shipped: 17 weeks, reseeded bracket, category record, 0.88/0.75, shock 0.06)":{},
 "18 regular-season weeks (the engine of the draft grade)":{"const":{"WEEKS":18}},
 "20 regular-season weeks":{"const":{"WEEKS":20}},
 "fixed bracket, no reseed after round 1 (the engine of the draft grade)":{"fixed_bracket":True},
 "standings by weekly wins (not the category record)":{"weekly_win":True},
 "no in-sim injury discount (risk 0.88 like healthy)":{"avail":(0.88,0.88)},
 "harsher risk tier (0.65)":{"avail":(0.88,0.65)},
 "healthy players play 0.95 of games":{"avail":(0.95,0.75)},
 "healthy players play 0.80 of games":{"avail":(0.80,0.75)},
 "no shared games shock":{"const":{"TEAM_WEEK_SHOCK":0.0}},
 "shared games shock doubled (0.12)":{"const":{"TEAM_WEEK_SHOCK":0.12}},
 "per-game variance x0.8":{"cv":0.8},
 "per-game variance x1.2":{"cv":1.2},
 "percentages share a hot/cold shock (0.5 sd)":{"pct_shock":0.5},
}
if __name__=="__main__":
    jobs=[(n,p,sd) for n,p in VARIANTS.items() for sd in SEEDS]
    with ProcessPoolExecutor(4) as ex: R=list(ex.map(run,jobs))
    # harness self-check: the baseline must reproduce league_sim's 10,000-season figures within 3 SE on both seeds
    ref={sd:json.load(open(f"{DECK}/arena/results/m100_league_sim_10k_s{sd}_w17r_av0.json"))["teams"]["10"]["champ"] for sd in SEEDS}  # the live engine's reference (_av0: recovery/out 0.0, 2026-10-21)
    ref_old={sd:json.load(open(f"{DECK}/arena/results/m100_league_sim_10k_s{sd}.json"))["teams"]["10"]["champ"] for sd in SEEDS}
    out={}
    for n,sd,c,p,allc in R: out.setdefault(n,{})[sd]=dict(title=round(c,2),playoff=round(p,2),all=allc)
    base_key=next(k for k in out if k.startswith("baseline")); base={sd:out[base_key][sd]["title"] for sd in SEEDS}
    se=math.sqrt(0.22*0.78/SEASONS)*100; base_ok={sd:abs(base[sd]-ref[sd])<3*se for sd in SEEDS}
    json.dump(dict(seasons=SEASONS,seeds=list(SEEDS),mc_se_points=round(se,3),reference_10k=ref,reference_10k_draft_grade_engine=ref_old,engine_commit=subprocess.check_output(["git","-C",DECK,"rev-parse","--short","HEAD"]).decode().strip(),baseline_within_3se=base_ok,variants=out),open(os.path.join(H,"rt_sensitivity.json"),"w"),indent=1)
    print("MC SE",round(se,2),"reference 10k",ref,"baseline within 3 SE:",base_ok)
    for n in VARIANTS: print(f"{n:<60} title {out[n][2026]['title']:6.2f} / {out[n][2027]['title']:6.2f}   d {out[n][2026]['title']-base[2026]:+.2f} / {out[n][2027]['title']-base[2027]:+.2f}   playoffs {out[n][2026]['playoff']:.1f}")
