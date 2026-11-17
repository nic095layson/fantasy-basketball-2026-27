"""Swap scores for the missed-pickup report (2026-11-17): each of three free players for each of the owner's bottom four,
on the kit's line and on the player's own 2026-11-03..11-16 box-score line. Scratch analysis, kept for the record;
run from a checkout of the records branch with the deck beside it. Writes score2.json and score2_lines.json to $OUT."""
import json, os, sys, csv, glob, tempfile, multiprocessing as mp
SP=os.environ.get('OUT','.')   # run from a checkout of the records branch: OUT=<dir> python3 swap_scores.py
ADDS=["Kelly Oubre Jr.","Ziaire Williams","Jerami Grant"]; BOX={"Kelly Oubre Jr.":"Kelly Oubre"}
DROPS=["Kel'el Ware","Neemias Queta","PJ Washington","Cameron Johnson"]
L0,L1='2026-11-03','2026-11-16'
def recent_lines():
    out={}
    for a in ADDS:
        gs=[]
        for f in sorted(glob.glob('data/actuals/*.json')):
            r=json.load(open(f))
            if not(L0<=r['date']<=L1): continue
            for p in r['players']:
                if (p.get('pool_name') or p['name'])==BOX.get(a,a) and not p.get('dnp') and (p.get('min') or 0)>0: gs.append(p)
        n=len(gs); s=lambda c: sum(g.get(c) or 0 for g in gs)
        out[a]=dict(n=n,fg_pct=s('fgm')/s('fga'),fga=s('fga')/n,ft_pct=(s('ftm')/s('fta')) if s('fta') else 0.0,fta=s('fta')/n,tpm=s('tpm')/n,pts=s('pts')/n,reb=s('reb')/n,ast=s('ast')/n,stl=s('stl')/n,blk=s('blk')/n,tov=s('tov')/n,min=s('min')/n)
    return out
def make_pool(path, lines):
    rows=list(csv.DictReader(open('data/season/pool_season.csv',encoding='utf-8'))); f=list(rows[0].keys())
    for r in rows:
        if r['player'] in lines:
            l=lines[r['player']]
            r.update(fg_pct=f"{l['fg_pct']:.3f}",ft_pct=f"{l['ft_pct']:.3f}",**{c:f"{l[c]:.1f}" for c in ('fga','fta','tpm','pts','reb','ast','stl','blk','tov')})
    w=csv.DictWriter(open(path,'w',encoding='utf-8',newline=''),fieldnames=f); w.writeheader(); w.writerows(rows)
def job(args):
    pool,add,drop,seed=args
    os.environ['SEASON_POOL']=pool
    sys.path.insert(0,'scripts')
    import co_gm as CG
    _,by=CG.load_pool(); state=json.load(open(CG.STATE)); ros=CG.rosters(state,by)
    if add:
        ros[CG.OWNER_SEAT]=[p for p in ros[CG.OWNER_SEAT] if p['player']!=drop]+[by[add]]
        assert len(ros[CG.OWNER_SEAT])==len(CG.rosters(state,by)[CG.OWNER_SEAT])
    r=CG.run_league_sim(ros,seed,10000,tempfile.mkdtemp(),tag='x')
    t=r['teams'][str(CG.OWNER_SEAT)]
    return dict(pool=os.path.basename(pool),add=add,drop=drop,seed=seed,champ=t['champ'],final=t.get('final'),semi=t.get('semi'),playoff=t['playoff'])
if __name__=='__main__':
    lines=recent_lines(); json.dump(lines,open(SP+'/score2_lines.json','w'),indent=1)
    hi=SP+'/pool_recent.csv'; make_pool(hi,lines); kit=os.path.abspath('data/season/pool_season.csv')
    jobs=[(kit,None,None,s) for s in (2026,2027)]+[(p,a,d,s) for p in (kit,hi) for a in ADDS for d in DROPS for s in (2026,2027)]
    with mp.Pool(4) as pool: res=pool.map(job,jobs,chunksize=1)
    json.dump(res,open(SP+'/score2.json','w'),indent=1); print('done',len(res))
