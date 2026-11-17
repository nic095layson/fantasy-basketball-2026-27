import json, os, sys, tempfile, multiprocessing as mp
SP=__import__('os').environ.get('OUT','.')   # run from a checkout of the records branch; OUT is where the records beside this script live
Z="Ziaire Williams"
CFG={'plan':(None,["Cameron Johnson","Cam Spencer"]),            # the owner's stated plan
     'keep_spencer':(None,["Cameron Johnson","PJ Washington"]),   # reference: the earlier top pair of drops
     'zw_for_pj':(Z,["Cameron Johnson","Cam Spencer","PJ Washington"]),
     'zw_for_queta':(Z,["Cameron Johnson","Cam Spencer","Neemias Queta"])}
def job(a):
    cfg,pool,seed=a
    os.environ['SEASON_POOL']=pool; sys.path.insert(0,'scripts')
    import co_gm as CG, il_return as IR
    _,by=CG.load_pool(); state=json.load(open(CG.STATE))
    weeks=int(json.load(open(CG.SCHEDULE))['regular_season_weeks'])
    espn_path,rows=IR.newest_espn('2026-11-17'); il=IR.il_players(state,rows,'2026-11-17',weeks,by=by)
    ros=CG.rosters(state,by,include_il=True); others=[s for s in ros if s!=CG.OWNER_SEAT]
    win=IR.windows_for(il,0,ros,weeks,room=True,seats=others)
    add,drops=CFG[cfg]
    w={'Tyrese Haliburton':(6,weeks),'Kawhi Leonard':(6,weeks)}
    for d in drops: w[d]=(1,5)
    if add: ros[CG.OWNER_SEAT].append(by[add]); w[add]=(6,weeks)
    names=[p['player'] for p in ros[CG.OWNER_SEAT]]
    active6=[n for n in names if w.get(n,(1,weeks))[0]<=6<=w.get(n,(1,weeks))[1]]
    win[CG.OWNER_SEAT]=w
    r=CG.run_league_sim(ros,seed,10000,tempfile.mkdtemp(),tag='x',windows=win)
    t=r['teams'][str(CG.OWNER_SEAT)]
    return dict(cfg=cfg,pool=os.path.basename(pool),seed=seed,champ=t['champ'],final=t.get('final'),playoff=t['playoff'],cats=t.get('cat_win_pct'),n_week6=len(active6))
if __name__=='__main__':
    kit=os.path.abspath('data/season/pool_season.csv'); pools=[kit,SP+'/pool_zw_season.csv',SP+'/pool_zw_recent.csv']
    jobs=[(c,kit,s) for c in ('plan','keep_spencer') for s in (2026,2027)]+[(c,p,s) for c in ('zw_for_pj','zw_for_queta') for p in pools for s in (2026,2027)]
    with mp.Pool(4) as pool: res=pool.map(job,jobs,chunksize=1)
    json.dump(res,open(SP+'/zw2.json','w'),indent=1); print('done',len(res))
