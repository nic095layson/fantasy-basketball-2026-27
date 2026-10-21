#!/usr/bin/env python3
"""Red team, phase 2: the card's measure (ECW, normal approximation, independent categories, 11 opponents) against the
simulator's realized category win rates (shock, random pairings, 17 weeks, reseeded bracket) for all 12 seats; the league totals that must
hold by construction (every category sums to 50% across teams; each seat's category rates equal its cats-per-week);
rank agreement between ECW and title share. Writes rt_consistency.json."""
import json, math, os, sys
H=os.path.dirname(os.path.abspath(__file__)); DECK="/home/user/yahoo-fantasy-basketball"
sys.path.insert(0,DECK+"/scripts"); sys.path.insert(0,DECK+"/arena"); import hoops, arena
hoops.DATA_PATH=f"{DECK}/arena/results/players_v69.csv"; P=hoops.zscores(hoops.load_players()); by={p["player"]:p for p in P}
st=json.load(open(f"{DECK}/arena/data/states/draft_state_100.json")); CATS=hoops.CATS
ros={s:[] for s in range(1,13)}
for pk in st["picks"]: ros[pk["slot"]].append(by[pk["player"]])
M={s:arena.team_week_model(r) for s,r in ros.items()}
def ecw(s):
    tot=0; cats={c:0 for c in CATS}
    for o in ros:
        if o==s: continue
        for c in CATS:
            d=(M[s][0][c]-M[o][0][c])/(math.sqrt(M[s][1][c]+M[o][1][c]) or 1e-9); pr=0.5*(1+math.erf(d/math.sqrt(2))); v=(1-pr) if c=="TO" else pr
            tot+=v; cats[c]+=v/11
    return tot/11,cats
E={s:ecw(s) for s in ros}
# 2026-10-21 (owner "implement fixes", decision 5 (a)): pinned by design to the _w17r references of the 0.60-recovery
# engine this post-mortem studied; the live engine's references are the _w17r_av0 files (deck #128).
S={sd:json.load(open(f"{DECK}/arena/results/m100_league_sim_10k_s{sd}_w17r.json"))["teams"] for sd in (2026,2027)}  # the shipped engine's reference runs (17 weeks, reseeded; Session 1 item 2)
def rank(vals):
    o=sorted(vals,key=lambda k:-vals[k]); return {k:i+1 for i,k in enumerate(o)}
def spearman(a,b):
    ks=list(a); ra,rb=rank(a),rank(b); n=len(ks); return 1-6*sum((ra[k]-rb[k])**2 for k in ks)/(n*(n*n-1))
out={}
for sd,T in S.items():
    cat_sum={c:sum(T[str(s)]["cat_win_pct"][c] for s in ros)/12 for c in CATS}
    per_seat=[]; gaps=[]
    for s in ros:
        t=T[str(s)]; e,cats=E[s]
        d={c:t["cat_win_pct"][c]/100-cats[c] for c in CATS}; gaps+= [abs(x) for x in d.values()]
        per_seat.append(dict(seat=s,ecw=round(e,4),sim_cats_per_week=round(t["cats_per_week"],4),sim_cat_mean=round(sum(t["cat_win_pct"].values())/900,4),max_cat_gap=round(max(abs(x) for x in d.values()),4),d=d))
    out[sd]=dict(cat_mean_across_teams=cat_sum,all_cats_at_50=all(abs(v-50)<1e-6 for v in cat_sum.values()),
        max_abs_gap_ecw_vs_sim=max(gaps),mean_abs_gap=sum(gaps)/len(gaps),
        spearman_ecw_vs_title=round(spearman({s:E[s][0] for s in ros},{s:T[str(s)]["champ"] for s in ros}),3),
        spearman_ecw_vs_cats_per_week=round(spearman({s:E[s][0] for s in ros},{s:T[str(s)]["cats_per_week"] for s in ros}),3),
        per_seat=per_seat)
    # the owner's per-category: ECW vs sim
    out[sd]["owner"]={c:dict(ecw=round(E[10][1][c],3),sim=round(T["10"]["cat_win_pct"][c]/100,3)) for c in CATS}
json.dump(out,open(os.path.join(H,"rt_consistency.json"),"w"),indent=1)
for sd in out:
    o=out[sd]; print(sd,"cats at 50:",o["all_cats_at_50"],"max gap",round(o["max_abs_gap_ecw_vs_sim"],4),"mean gap",round(o["mean_abs_gap"],4),"rho title",o["spearman_ecw_vs_title"],"rho cats/wk",o["spearman_ecw_vs_cats_per_week"])
    print("  owner:",{c:(v["ecw"],v["sim"]) for c,v in o["owner"].items()})
    print("  worst seats:",sorted([(p["seat"],p["max_cat_gap"]) for p in o["per_seat"]],key=lambda x:-x[1])[:3])
