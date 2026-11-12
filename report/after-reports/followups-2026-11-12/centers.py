import copy, json, os, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
W='/home/user/wtsd'; sys.path.insert(0, W+'/scripts')
import co_gm as CG, il_return as IR
DATE="2026-11-12"; RETURNS={"Tyrese Haliburton":"2026-11-21","Kawhi Leonard":"2026-11-23"}; SEASONS=10000
PAIRS={"Queta, then Washington (rule)":["Neemias Queta","PJ Washington"],
       "Queta, then Cam Johnson":["Neemias Queta","Cameron Johnson"],
       "Champagnie, then Queta":["Julian Champagnie","Neemias Queta"],
       "Champagnie, then Cam Johnson":["Julian Champagnie","Cameron Johnson"],
       "Cam Johnson, then Washington":["Cameron Johnson","PJ Washington"],
       "Champagnie, then Washington":["Julian Champagnie","PJ Washington"],
       "Queta, then Ware":["Neemias Queta","Kel'el Ware"]}
state=json.load(open(CG.STATE)); weeks=int(json.load(open(CG.SCHEDULE))["regular_season_weeks"])
P,by=CG.load_pool()
path,rows=IR.newest_espn(DATE, W+'/data/status'); il=IR.il_players(state,rows,DATE,weeks,by=by)
for x in il:
    if x["player"] in RETURNS: x["return_date"]=RETURNS[x["player"]]; x["week"]=IR.return_week(RETURNS[x["player"]],DATE,weeks)
ros=CG.rosters(state,by,include_il=True); rule=IR.windows_for(il,0,ros,weeks,room=True)
me=[t for t in state["teams"] if t["seat"]==CG.OWNER_SEAT][0]
elig={p["player"]:p.get("positions") for p in me["players"]}; print('C-eligible on the roster:',[n for n,e in elig.items() if e and 'C' in e])
def custom(drops):
    win=copy.deepcopy(rule); w10={}
    for x,d in zip(sorted([x for x in il if x["seat"]==CG.OWNER_SEAT],key=lambda x:x["week"]),drops):
        w10[x["player"]]=(x["week"],weeks); w10[d]=(1,x["week"]-1)
    win[CG.OWNER_SEAT]=w10; return win
cfg={k:custom(v) for k,v in PAIRS.items()}
print('rule windows seat 10:',rule[CG.OWNER_SEAT]); print('check: custom rule pair equals the rule:',cfg["Queta, then Washington (rule)"][CG.OWNER_SEAT]=={k:tuple(v) for k,v in rule[CG.OWNER_SEAT].items()})
work=tempfile.mkdtemp(); jobs=[(c,s) for c in cfg for s in IR.SEEDS]
def run(j):
    c,s=j; tag="".join(ch if ch.isalnum() else "_" for ch in c)[:60]
    r=CG.run_league_sim(ros,s,SEASONS,work,tag=tag,windows=cfg[c]); t=r["teams"][str(CG.OWNER_SEAT)]
    return c,s,t["champ"],t["playoff"]
res={}
with ThreadPoolExecutor(4) as ex:
    for c,s,t,po in ex.map(run,jobs): res.setdefault(c,{})[str(s)]=(t,po); print(c,s,round(t,2),flush=True)
json.dump(res,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'centers.json'),'w'),indent=1)
print('---')
for c,d in sorted(res.items(),key=lambda kv:-sum(v[0] for v in kv[1].values())):
    print(f"{c:32s} title {sum(v[0] for v in d.values())/2:5.2f}  by seed {d['2026'][0]:5.2f} / {d['2027'][0]:5.2f}  playoffs {sum(v[1] for v in d.values())/2:5.2f}")
