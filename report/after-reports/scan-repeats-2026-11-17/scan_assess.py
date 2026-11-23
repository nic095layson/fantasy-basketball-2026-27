import sys, json, collections, statistics as st, datetime as dt, io, contextlib
SP=__import__('os').environ.get('OUT','.')   # run from a checkout of the records branch; OUT is where the records beside this script live
sys.argv=['audit.py','--records','.']
src=open('report/after-reports/missed-pickups-2026-11-17/audit.py').read().replace("json.dump(out,open(os.path.join(HERE,'audit.json'),'w'),indent=1,default=str)","pass")
with contextlib.redirect_stdout(io.StringIO()): exec(src)
slots=json.load(open(SP+'/slots.json'))
# 1. within-day spread among picks sharing a drop
byday=collections.defaultdict(list)
for s in slots: byday[s['date']].append(s)
same=[v for v in byday.values() if len(v)>=2 and len({x['drop'] for x in v})==1]
spreads=[max(x['d_title'] for x in v)-min(x['d_title'] for x in v) for v in same]
print('days with 2+ picks sharing one drop',len(same),'spread median',round(st.median(spreads),2),'spread<1.0:',sum(x<1.0 for x in spreads))
drops=collections.Counter(s['drop'] for s in slots); print('drops named',drops.most_common())
big=[s for s in slots if s['d_title']>2]; print('d_title>2:',len(big),collections.Counter(s['drop'] for s in big))
# 2. line vs actual for the repeated names, from first listing
print('\nline at first listing vs box average from first listing to 11-16')
for name in ['Tobias Harris','Julian Champagnie','Bobby Portis','Cameron Johnson','Jrue Holiday']:
    k=norm(name); d0=min(s['date'] for s in slots if s['add']==name); r=POOLS[d0].get(k) or POOLS[d0].get(norm(name.replace('Cameron','Cam')))
    gs=games(k,d0,W1); a=avg(gs) if gs else None
    free=sorted(((poolval(kk,d0),kk) for kk in POOLS[d0] if poolval(kk,d0) is not None and not rostered_on(kk,d0)),reverse=True)
    rk=next((i+1 for i,(v,kk) in enumerate(free) if kk==k),None)
    print(f"{name:18} first {d0[5:]} kit line {r['pts']}/{r['reb']}/{r['ast']} {r['stl']}s {r['blk']}b {r['tpm']}3 fg{r['fg_pct']} | actual n{len(gs)} "+(line_str(a) if a else 'no games')+f" | kit rank among free {rk} of {len(free)} | actual val {round(val(a),2) if a else None} (roster line {LINE:.2f})")
# 3. owner add/drop history of the repeated names, and listings within 7 days after an owner drop
own=collections.defaultdict(list)
for x in tx:
    if x['team_ids'][0]!=OWNER or x['type']=='trade': continue
    for p in x['players_added']: own[norm(p['name'])].append((x['date'],'add'))
    for p in x['players_dropped']: own[norm(p['name'])].append((x['date'],'drop'))
after_drop=0
for s in slots:
    ev=[e for e in own.get(norm(s['add']),[]) if e[1]=='drop' and 0<=(dt.date.fromisoformat(s['date'])-dt.date.fromisoformat(e[0])).days<=7]
    s['after_own_drop']=bool(ev); after_drop+=bool(ev)
print('\nlistings of a player the owner had dropped in the previous 7 days:',after_drop,'of',len(slots))
for name in ['Tobias Harris','Julian Champagnie','Bobby Portis','Cameron Johnson','Jrue Holiday']: print(name, own.get(norm(name)))
# 4. the rank-1 pick against the free field over the next 7 days
print('\nrank-1 pick vs free players over the next 7 days (free that morning, 2+ games, 18+ min)')
res=[]
for d,v in sorted(byday.items()):
    s=[x for x in v if x['rank']==1][0]; k=norm(s['add']); hi=(dt.date.fromisoformat(d)+dt.timedelta(6)).isoformat()
    if hi>W1: continue
    field=[]
    for c in logs:
        if rostered_on(c,d): continue
        g=games(c,d,hi)
        if len(g)>=2 and st.mean(x['min'] for x in g)>=18: field.append((vg(g),c))
    field.sort(reverse=True); g=games(k,d,hi)
    mine=vg(g) if len(g)>=2 else None
    pct=None if mine is None else round(100*sum(1 for v_,c in field if v_<mine)/len(field))
    res.append((d,s['add'],len(g),None if mine is None else round(mine,2),pct,len(field),disp[field[0][1]],round(field[0][0],1)))
    print(d[5:],f"{s['add']:18} games {len(g)} val {None if mine is None else round(mine,2)} percentile among {len(field)} free: {pct} | best free: {disp[field[0][1]]} {round(field[0][0],1)}")
ok=[r for r in res if r[4] is not None]
print('graded days',len(ok),'of',len(res),'median percentile',st.median(r[4] for r in ok),'top quarter',sum(r[4]>=75 for r in ok),'bottom half',sum(r[4]<50 for r in ok),'no games',sum(r[3] is None for r in res))
