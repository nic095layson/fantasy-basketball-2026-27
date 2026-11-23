import json, os, sys, csv, glob, tempfile, multiprocessing as mp
SP=__import__('os').environ.get('OUT','.')   # run from a checkout of the records branch; OUT is where the records beside this script live
Z="Ziaire Williams"
def box(lo,hi):
    gs=[]
    for f in sorted(glob.glob('data/actuals/*.json')):
        r=json.load(open(f))
        if not(lo<=r['date']<=hi): continue
        reg={g['espn_id'] for g in r.get('games',[]) if g.get('season_type')==2}
        for p in r['players']:
            if (p.get('pool_name') or p['name'])==Z and not p.get('dnp') and (p.get('min') or 0)>0 and p.get('game') in reg: gs.append(dict(p,date=r['date']))
    return gs
def line(gs):
    n=len(gs); s=lambda c: sum(g.get(c) or 0 for g in gs)
    return dict(n=n,fg_pct=s('fgm')/s('fga'),fga=s('fga')/n,ft_pct=(s('ftm')/s('fta')) if s('fta') else 0.0,fta=s('fta')/n,tpm=s('tpm')/n,pts=s('pts')/n,reb=s('reb')/n,ast=s('ast')/n,stl=s('stl')/n,blk=s('blk')/n,tov=s('tov')/n,min=s('min')/n,starts=sum(1 for g in gs if g.get('starter')))
def make_pool(path, l):
    rows=list(csv.DictReader(open('data/season/pool_season.csv',encoding='utf-8'))); f=list(rows[0].keys())
    for r in rows:
        if r['player']==Z:
            r.update(fg_pct=f"{l['fg_pct']:.3f}",ft_pct=f"{l['ft_pct']:.3f}",**{c:f"{l[c]:.1f}" for c in ('fga','fta','tpm','pts','reb','ast','stl','blk','tov')})
    w=csv.DictWriter(open(path,'w',encoding='utf-8',newline=''),fieldnames=f); w.writeheader(); w.writerows(rows)
def job(a):
    world,pool,drop,seed=a
    os.environ['SEASON_POOL']=pool; sys.path.insert(0,'scripts')
    import co_gm as CG, il_return as IR
    _,by=CG.load_pool(); state=json.load(open(CG.STATE))
    if world=='never':
        ros=CG.rosters(state,by)
        if drop: ros[CG.OWNER_SEAT]=[p for p in ros[CG.OWNER_SEAT] if p['player']!=drop]+[by[Z]]
        r=CG.run_league_sim(ros,seed,10000,tempfile.mkdtemp(),tag='x')
    else:
        weeks=int(json.load(open(CG.SCHEDULE))['regular_season_weeks'])
        espn_path,rows=IR.newest_espn('2026-11-17'); il=IR.il_players(state,rows,'2026-11-17',weeks,by=by)
        ros=CG.rosters(state,by,include_il=True); others=[s for s in ros if s!=CG.OWNER_SEAT]
        win=IR.windows_for(il,0,ros,weeks,room=True,seats=others)
        w={'Tyrese Haliburton':(5,weeks),'Kawhi Leonard':(6,weeks),'Cameron Johnson':(1,4),'Cam Spencer':(1,5)}
        if drop:
            ros[CG.OWNER_SEAT].append(by[Z]); w[Z]=(6,weeks); w[drop]=(1,5)
        win[CG.OWNER_SEAT]=w
        r=CG.run_league_sim(ros,seed,10000,tempfile.mkdtemp(),tag='x',windows=win)
    t=r['teams'][str(CG.OWNER_SEAT)]
    return dict(world=world,pool=os.path.basename(pool),drop=drop,seed=seed,champ=t['champ'],final=t.get('final'),playoff=t['playoff'],cats=t.get('cat_win_pct'))
if __name__=='__main__':
    L=dict(season=line(box('2026-10-20','2026-11-16')),recent=line(box('2026-11-03','2026-11-16')))
    log=[(g['date'],g['min'],bool(g.get('starter')),g['pts'],g['reb'],g['ast'],g['stl'],g['blk'],g['tpm'],g['tov'],g['fgm'],g['fga']) for g in box('2026-10-20','2026-11-16')]
    json.dump(dict(lines=L,log=log),open(SP+'/zw_lines.json','w'),indent=1)
    kit=os.path.abspath('data/season/pool_season.csv'); pools={'kit':kit}
    for k in ('season','recent'):
        pools[k]=SP+f'/pool_zw_{k}.csv'; make_pool(pools[k],L[k])
    jobs=[(wd,kit,None,s) for wd in ('never','return') for s in (2026,2027)]
    jobs+=[('never',p,d,s) for p in pools.values() for d in ("Neemias Queta","Cameron Johnson") for s in (2026,2027)]
    jobs+=[('return',p,"Neemias Queta",s) for p in pools.values() for s in (2026,2027)]
    with mp.Pool(4) as pool: res=pool.map(job,jobs,chunksize=1)
    json.dump(res,open(SP+'/zw.json','w'),indent=1); print('done',len(res))
