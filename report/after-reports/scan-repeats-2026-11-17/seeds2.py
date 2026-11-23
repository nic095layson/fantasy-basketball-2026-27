import json, os, sys, csv, glob, tempfile, multiprocessing as mp
SP=__import__('os').environ.get('OUT','.')   # run from a checkout of the records branch
WHO={"Cam Spencer":"Cam Spencer","PJ Washington":"PJ Washington"}
CFG={'plan':["Cameron Johnson","Cam Spencer"],'keep_spencer':["Cameron Johnson","PJ Washington"]}
def line(name):
    gs=[]
    for f in sorted(glob.glob('data/actuals/*.json')):
        r=json.load(open(f))
        if not('2026-10-20'<=r['date']<='2026-11-16'): continue
        reg={g['espn_id'] for g in r.get('games',[]) if g.get('season_type')==2}
        gs+=[p for p in r['players'] if (p.get('pool_name') or p['name'])==name and not p.get('dnp') and (p.get('min') or 0)>0 and p.get('game') in reg]
    n=len(gs); s=lambda c: sum(g.get(c) or 0 for g in gs)
    return dict(n=n,fg_pct=s('fgm')/s('fga'),fga=s('fga')/n,ft_pct=s('ftm')/s('fta'),fta=s('fta')/n,tpm=s('tpm')/n,pts=s('pts')/n,reb=s('reb')/n,ast=s('ast')/n,stl=s('stl')/n,blk=s('blk')/n,tov=s('tov')/n,min=s('min')/n)
def job(a):
    cfg,seed,pool=a
    os.environ['SEASON_POOL']=pool; sys.path.insert(0,'scripts')
    import co_gm as CG, il_return as IR
    _,by=CG.load_pool(); state=json.load(open(CG.STATE))
    weeks=int(json.load(open(CG.SCHEDULE))['regular_season_weeks'])
    espn_path,rows=IR.newest_espn('2026-11-17'); il=IR.il_players(state,rows,'2026-11-17',weeks,by=by)
    ros=CG.rosters(state,by,include_il=True); others=[s for s in ros if s!=CG.OWNER_SEAT]
    win=IR.windows_for(il,0,ros,weeks,room=True,seats=others)
    w={'Tyrese Haliburton':(6,weeks),'Kawhi Leonard':(6,weeks)}
    for d in CFG[cfg]: w[d]=(1,5)
    win[CG.OWNER_SEAT]=w
    t=CG.run_league_sim(ros,seed,10000,tempfile.mkdtemp(),tag='x',windows=win)['teams'][str(CG.OWNER_SEAT)]
    return dict(cfg=cfg,seed=seed,champ=t['champ'],final=t.get('final'))
if __name__=='__main__':
    L={n:line(n) for n in WHO}
    rows=list(csv.DictReader(open('data/season/pool_season.csv',encoding='utf-8'))); f=list(rows[0].keys())
    kit={r['player']:{k:r[k] for k in ('pts','reb','ast','stl','blk','tpm','tov','fg_pct','fga','ft_pct','fta')} for r in rows if r['player'] in WHO}
    for r in rows:
        if r['player'] in L:
            l=L[r['player']]; r.update(fg_pct=f"{l['fg_pct']:.3f}",ft_pct=f"{l['ft_pct']:.3f}",**{c:f"{l[c]:.1f}" for c in ('fga','fta','tpm','pts','reb','ast','stl','blk','tov')})
    pool=SP+'/pool_sp_pj_season.csv'
    with open(pool,'w',encoding='utf-8',newline='') as fh:   # closed before the workers read it
        w=csv.DictWriter(fh,fieldnames=f); w.writeheader(); w.writerows(rows)
    for n in WHO: print(n,'kit',kit[n]); print(n,'season',{k:round(v,2) for k,v in L[n].items()})
    jobs=[(c,s,pool) for s in (2026,2027) for c in CFG]
    with mp.Pool(4) as p: res=p.map(job,jobs,chunksize=1)
    json.dump(dict(lines=L,kit=kit,runs=res),open(SP+'/seeds2.json','w'),indent=1)
    by={(x['cfg'],x['seed']):x for x in res}
    for s in (2026,2027): print(s,'plan',by[('plan',s)]['champ'],by[('plan',s)]['final'],'| keep',by[('keep_spencer',s)]['champ'],by[('keep_spencer',s)]['final'],'| diff',round(by[('keep_spencer',s)]['champ']-by[('plan',s)]['champ'],2),round(by[('keep_spencer',s)]['final']-by[('plan',s)]['final'],2))
