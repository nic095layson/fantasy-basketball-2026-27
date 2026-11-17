import json, os, sys, tempfile, multiprocessing as mp
SP=__import__('os').environ.get('OUT','.')   # run from a checkout of the records branch
CFG={'plan':["Cameron Johnson","Cam Spencer"],'keep_spencer':["Cameron Johnson","PJ Washington"]}
def job(a):
    cfg,seed=a
    os.environ['SEASON_POOL']=os.path.abspath('data/season/pool_season.csv'); sys.path.insert(0,'scripts')
    import co_gm as CG, il_return as IR
    _,by=CG.load_pool(); state=json.load(open(CG.STATE))
    weeks=int(json.load(open(CG.SCHEDULE))['regular_season_weeks'])
    espn_path,rows=IR.newest_espn('2026-11-17'); il=IR.il_players(state,rows,'2026-11-17',weeks,by=by)
    ros=CG.rosters(state,by,include_il=True); others=[s for s in ros if s!=CG.OWNER_SEAT]
    win=IR.windows_for(il,0,ros,weeks,room=True,seats=others)
    w={'Tyrese Haliburton':(6,weeks),'Kawhi Leonard':(6,weeks)}
    for d in CFG[cfg]: w[d]=(1,5)
    win[CG.OWNER_SEAT]=w
    r=CG.run_league_sim(ros,seed,10000,tempfile.mkdtemp(),tag='x',windows=win)
    t=r['teams'][str(CG.OWNER_SEAT)]
    return dict(cfg=cfg,seed=seed,champ=t['champ'],final=t.get('final'),playoff=t['playoff'],cats=t.get('cat_win_pct'))
if __name__=='__main__':
    jobs=[(c,s) for s in (2026,2027,2028,2029,2030,2031) for c in CFG]
    with mp.Pool(4) as pool: res=pool.map(job,jobs,chunksize=1)
    json.dump(res,open(SP+'/seeds.json','w'),indent=1)
    import statistics as st
    by={(x['cfg'],x['seed']):x for x in res}
    dt=[by[('keep_spencer',s)]['champ']-by[('plan',s)]['champ'] for s in (2026,2027,2028,2029,2030,2031)]
    df=[by[('keep_spencer',s)]['final']-by[('plan',s)]['final'] for s in (2026,2027,2028,2029,2030,2031)]
    for s in (2026,2027,2028,2029,2030,2031): print(s,'plan',by[('plan',s)]['champ'],by[('plan',s)]['final'],'| keep',by[('keep_spencer',s)]['champ'],by[('keep_spencer',s)]['final'])
    print('title diff by seed',[round(x,2) for x in dt],'mean',round(st.mean(dt),2),'se',round(st.stdev(dt)/len(dt)**0.5,2),'positive seeds',sum(x>0 for x in dt))
    print('final diff by seed',[round(x,2) for x in df],'mean',round(st.mean(df),2),'se',round(st.stdev(df)/len(df)**0.5,2),'positive seeds',sum(x>0 for x in df))
    print('plan mean title',round(st.mean(by[('plan',s)]['champ'] for s in (2026,2027,2028,2029,2030,2031)),2),'final',round(st.mean(by[('plan',s)]['final'] for s in (2026,2027,2028,2029,2030,2031)),2))
    c=by[('plan',2026)]['cats']; print('cat change (6-seed mean)',{k:round(st.mean(by[('keep_spencer',s)]['cats'][k]-by[('plan',s)]['cats'][k] for s in (2026,2027,2028,2029,2030,2031)),1) for k in c})
