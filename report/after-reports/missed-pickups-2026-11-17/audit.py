#!/usr/bin/env python3
"""Missed-pickup audit (owner 2026-11-17: "continue auditing and finding cases where there was a missed-pick up player
that was in my blind spot"). Read-only: it reads a checkout of the records branch and writes one JSON beside itself.

    python3 report/after-reports/missed-pickups-2026-11-17/audit.py --records <checkout of season/daily>

Method (stated to the owner before the run, 2026-11-17):
  window      2026-10-20 (the first brief) to 2026-11-16 (the last box score): the session's choice
  adds        data/managers/transactions.json (Yahoo's feed through Flaim), every team but the owner's
  owner       Yahoo team 11 (KEL'EL YAXEL HALQUETA). The first pass used team 10 (MISSI ELLIOTT) by mistake; the
              owner's own roster in the state file was the known answer that caught it
  flagged     named in a brief's waiver_top (or, separately, streaming) on or before the add date
  value       a plain nine-category per-game z-sum from the window's box scores (percentages as makes above the
              league rate), base = players with 8+ games at 20+ minutes. NOT the kit's value: no category fit,
              no positions, no opponent. "Roster level" = the 156th best of the window; "top 100" = the 100th
  rostered    walked from the transaction feed and the newest league state, by day
  signals     checked on the morning of each day from games before it: R1 30+ min in 3 straight, R2 30+ in 2 of
              the last 3, JUMP last-2 minutes 6+ over his earlier average (and 24+), START2 started the last two,
              VAL3 / VAL3+ last-3 value at roster level / top-100 level with 20+ minutes
"""
import argparse, json, glob, csv, unicodedata, re, collections, subprocess, os, statistics as st, datetime as dt
ap = argparse.ArgumentParser(); ap.add_argument("--records", required=True); A = ap.parse_args()
R = A.records.rstrip("/") + "/"; HERE = os.path.dirname(os.path.abspath(__file__))
W0,W1='2026-10-20','2026-11-16'; OWNER='478.l.36464.t.11'
_m = json.load(open(sorted(glob.glob(R + "data/managers/day_*.json"))[-1]))
TN = {k.split(".")[-1]: (v.get("name") or v.get("team")) if isinstance(v, dict) else v for k, v in _m["teams"].items()}
def norm(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    s=re.sub(r"[.'`]", '', s); s=re.sub(r'\b(jr|sr|ii|iii|iv)\b','',s); s=re.sub(r'\s+',' ',s).strip()
    return {'cameron johnson':'cam johnson'}.get(s,s)
def nxt(d,n=1): return (dt.date.fromisoformat(d)+dt.timedelta(n)).isoformat()
def days(a,b):
    while a<=b: yield a; a=nxt(a)
state=json.load(open(R+'data/league_state.json'))
tx=sorted(json.load(open(R+'data/managers/transactions.json'))['rows'],key=lambda x:x['timestamp'])
logs=collections.defaultdict(list); disp={}
for f in sorted(glob.glob(R+'data/actuals/*.json')):
    a=json.load(open(f)); d=a['date']
    for p in a['players']:
        k=norm(p.get('pool_name') or p['name']); disp.setdefault(k,p.get('pool_name') or p['name']); logs[k].append(dict(p,date=d))
cur={}
for t in state['teams']:
    for p in t['players']:
        cur[norm(p.get('yahoo_name') or p['player'])]=t['name']; cur[norm(p['player'])]=t['name']
for u in state.get('unpooled') or []: cur[norm(u['player'])]=u['fantasy_team']
events=collections.defaultdict(list)
for x in tx:
    if x['type']=='trade': continue
    for p in x['players_added']: events[norm(p['name'])].append((x['date'],'add',x['team_ids'][0]))
    for p in x['players_dropped']: events[norm(p['name'])].append((x['date'],'drop',x['team_ids'][0]))
def rostered_on(k,d):
    ev=[e for e in events.get(k,[]) if e[0]<d]
    if ev:
        if ev[-1][1]=='add' and k not in cur and not [e for e in events[k] if e[0]>=d]: return d<='2026-11-16'  # end-inconsistent: held until the state says otherwise
        return ev[-1][1]=='add'
    later=[e for e in events.get(k,[]) if e[0]>=d]
    if later: return later[0][1]=='drop'
    return k in cur
def games(k,lo=None,hi=None):
    return [g for g in logs.get(k,[]) if not g.get('dnp') and (g.get('min') or 0)>0 and (lo is None or g['date']>=lo) and (hi is None or g['date']<=hi)]
CATS=['pts','reb','ast','stl','blk','tpm','tov']
def avg(gs):
    n=len(gs); a={c:sum(g.get(c) or 0 for g in gs)/n for c in CATS+['fgm','fga','ftm','fta','min']}; a['n']=n; return a
full={k:avg(games(k,W0,W1)) for k in logs if len(games(k,W0,W1))>=5}
base=[a for a in full.values() if a['min']>=20 and a['n']>=8]
lg_fg=sum(a['fgm']*a['n'] for a in base)/sum(a['fga']*a['n'] for a in base); lg_ft=sum(a['ftm']*a['n'] for a in base)/sum(a['fta']*a['n'] for a in base)
def feats(a): return dict({c:a[c] for c in CATS}, fg=a['fgm']-lg_fg*a['fga'], ft=a['ftm']-lg_ft*a['fta'])
F=[feats(a) for a in base]; mu={c:st.mean(f[c] for f in F) for c in F[0]}; sd={c:st.pstdev(f[c] for f in F) for c in F[0]}
def val(a):
    f=feats(a); return sum((-1 if c=='tov' else 1)*(f[c]-mu[c])/sd[c] for c in f)
def catz(a):
    f=feats(a); return {c:round((-1 if c=='tov' else 1)*(f[c]-mu[c])/sd[c],1) for c in f}
def vg(gs): return val(avg(gs)) if gs else None
vals=sorted(((val(a),k) for k,a in full.items()),reverse=True)
LINE=vals[155][0]; L100=vals[99][0]; rank={k:i+1 for i,(v,k) in enumerate(vals)}
def line_str(a): return '%.0f/%.0f/%.0f %.1fs %.1fb %.1f3 %.1fto %.0fmin'%(a['pts'],a['reb'],a['ast'],a['stl'],a['blk'],a['tpm'],a['tov'],a['min'])
# flags
flag=collections.defaultdict(lambda:{'waiver_top':[],'streaming':[]})
for f in sorted(glob.glob(R+'report/briefs/brief_2026-*.json')):
    b=json.load(open(f)); d=b['date']
    for w in b.get('waiver_top') or []: flag[norm(w['add'])]['waiver_top'].append(d)
    for s in b.get('streaming') or []: flag[norm(s['player'])]['streaming'].append(d)
def flagged(k,D,kind): return [d for d in flag.get(k,{}).get(kind,[]) if d<=D]
# pool lines by date
def poolval(k,d):
    try: rows=POOLS[d]
    except KeyError: return None
    r=rows.get(k)
    if not r: return None
    a={c:float(r[c] or 0) for c in ['pts','reb','ast','stl','blk','tpm','tov','fga','fta']}
    a['fgm']=float(r['fg_pct'] or 0)*a['fga']; a['ftm']=float(r['ft_pct'] or 0)*a['fta']; a['min']=0
    return val(a)
POOLS={}
for d in days(W0,'2026-11-17'):   # the pool file as the records branch held it at the end of each day
    c=subprocess.run(["git","-C",R,"rev-list","-1",f"--before={d} 23:59:59 +0000","HEAD","--","data/season/pool_season.csv"],capture_output=True,text=True).stdout.strip()
    if c:
        txt=subprocess.run(["git","-C",R,"show",f"{c}:data/season/pool_season.csv"],capture_output=True,text=True).stdout
        POOLS[d]={norm(r['player']):r for r in csv.DictReader(txt.splitlines())}
# signals (evaluated on the morning of d, from games before d)
def sig(k,d,rule):
    gs=[g for g in games(k) if g['date']<d]
    l3=gs[-3:]
    if rule=='R1': return len(l3)==3 and all(g['min']>=30 for g in l3)
    if rule=='R2': return len(l3)==3 and sum(g['min']>=30 for g in l3)>=2
    if rule=='JUMP':
        if len(gs)<5: return False
        return st.mean(g['min'] for g in gs[-2:])>=st.mean(g['min'] for g in gs[:-2])+6 and st.mean(g['min'] for g in gs[-2:])>=24
    if rule=='START2': return len(gs)>=2 and all(g.get('starter') for g in gs[-2:])
    if rule=='VAL3': return len(l3)==3 and st.mean(g['min'] for g in l3)>=20 and vg(l3)>=LINE
    if rule=='VAL3+': return len(l3)==3 and st.mean(g['min'] for g in l3)>=20 and vg(l3)>=L100
RULES=['R1','R2','JUMP','START2','VAL3','VAL3+']
def free_start(k,D):
    s=W0
    for e in events.get(k,[]):
        if e[0]<D and e[1]=='drop': s=max(s,e[0])
    return s
def first_fire(k,D,rule):
    for d in days(free_start(k,D),D):
        if not rostered_on(k,d) and sig(k,d,rule): return d
out={}
# ---------- lens 1: rival adds
rows=[]
for x in tx:
    if x['type']!='add' or x['team_ids'][0]==OWNER or not(W0<=x['date']<=W1): continue
    for p in x['players_added']:
        k=norm(p['name']); D=x['date']; post=games(k,nxt(D),W1)
        a=avg(post) if post else None
        rows.append(dict(player=p['name'],k=k,team=TN[x['team_ids'][0].split('.')[-1]],date=D,wt=flagged(k,D,'waiver_top'),sm=flagged(k,D,'streaming'),
            n=len(post),val=round(val(a),2) if a else None,line=line_str(a) if a else '',pre=[g['min'] for g in games(k) if g['date']<D][-3:],
            poolval=poolval(k,D),fires={r:first_fire(k,D,r) for r in RULES},now=cur.get(k,'FREE'),free_since=free_start(k,D),matched=k in logs))
out['rival']=rows
# ---------- lens 2: owner adds vs best free that morning (hindsight)
own=[]
for x in tx:
    if x['team_ids'][0]!=OWNER or x['type']!='add' or not(W0<=x['date']<=W1): continue
    D=x['date']
    for p in x['players_added']:
        k=norm(p['name']); post=games(k,nxt(D),W1); 
        held_to=next((e[0] for e in events[k] if e[0]>D and e[1]=='drop' and e[2]==OWNER),None)
        held=games(k,nxt(D),held_to or W1)
        cands=[]
        for c in logs:
            if c==k or rostered_on(c,D): continue
            cp=games(c,nxt(D),W1)
            if len(cp)>=4 and st.mean(g['min'] for g in cp)>=18: cands.append((vg(cp),c,len(cp)))
        cands.sort(reverse=True)
        best=[dict(player=disp[c],val=round(v,2),n=n,line=line_str(avg(games(c,nxt(D),W1))),pre=[g['min'] for g in games(c) if g['date']<D][-3:],
                   pre3val=(round(vg([g for g in games(c) if g['date']<D][-3:]),2) if len([g for g in games(c) if g['date']<D])>=3 else None),
                   wt=bool(flagged(c,D,'waiver_top')),sm=bool(flagged(c,D,'streaming')),sig=[r for r in RULES if sig(c,D,r)],poolval=poolval(c,D),
                   taken=next(((e[0],TN[e[2].split('.')[-1]]) for e in events.get(c,[]) if e[0]>=D and e[1]=='add'),None)) for v,c,n in cands[:4]]
        own.append(dict(date=D,add=p['name'],drop=[q['name'] for q in x['players_dropped']],post_n=len(post),post_val=round(vg(post),2) if post else None,
            held_to=held_to,held_n=len(held),held_val=round(vg(held),2) if held else None,line=line_str(avg(post)) if post else '',wt=bool(flagged(k,D,'waiver_top')),best=best,n_free_better=sum(1 for v,c,n in cands if post and v>vg(post))))
out['own']=own
# ---------- lens 3: free today
L0='2026-11-03'
free=[]
for k in logs:
    if k in cur: continue
    g14=games(k,L0,W1)
    if len(g14)>=4 and st.mean(g['min'] for g in g14)>=18:
        g7=games(k,'2026-11-10',W1)
        free.append(dict(player=disp[k],v14=round(vg(g14),2),n14=len(g14),line=line_str(avg(g14)),v7=round(vg(g7),2) if len(g7)>=2 else None,min7=round(st.mean(g['min'] for g in g7),1) if g7 else None,
            last=g14[-1]['date'],full=round(val(full[k]),2) if k in full else None,poolval=poolval(k,'2026-11-17'),cz=catz(avg(g14)),
            wt=[d for d in flag.get(k,{}).get('waiver_top',[]) if d>='2026-11-10'],sm=[d for d in flag.get(k,{}).get('streaming',[]) if d>='2026-11-10'],sig=[r for r in RULES if sig(k,'2026-11-17',r)]))
free.sort(key=lambda r:-r['v14']); out['free']=free
me=[t for t in state['teams'] if 'KEL' in t['name']][0]
mine=[]
for p in me['players']:
    k=norm(p['player']); g14=games(k,L0,W1)
    mine.append(dict(player=p['player'],slot=p['slot'],status=p['status'],v14=round(vg(g14),2) if len(g14)>=2 else None,n14=len(g14),line=line_str(avg(g14)) if g14 else '',full=round(val(full[k]),2) if k in full else None,poolval=poolval(k,'2026-11-17'),cz=catz(avg(g14)) if g14 else None))
out['mine']=mine
# ---------- lens 4: signals, fires over the window among unrostered
sigs={}
for r in RULES:
    fired={}
    for k in logs:
        for d in days(W0,W1):
            if not rostered_on(k,d) and sig(k,d,r): fired.setdefault(k,d)
    graded=[(k,d,vg(games(k,d,W1))) for k,d in fired.items() if len(games(k,d,W1))>=3]
    sigs[r]=dict(fired=len(fired),graded=len(graded),hit=sum(1 for k,d,v in graded if v>=LINE),hit100=sum(1 for k,d,v in graded if v>=L100),names={disp[k]:d for k,d in fired.items()})
out['sigs']=sigs
out['meta']=dict(LINE=LINE,L100=L100,nbase=len(base),lg_fg=lg_fg,lg_ft=lg_ft,nplayers=len(full))
json.dump(out,open(os.path.join(HERE,'audit.json'),'w'),indent=1,default=str)

# kit's own flagged adds: what they did from first flag
kit=[]
for k,f in flag.items():
    if not f['waiver_top']: continue
    d0=min(f['waiver_top']); gs=games(k,d0,W1)
    kit.append(dict(player=disp.get(k,k),first=d0,days=len(f['waiver_top']),n=len(gs),val=round(vg(gs),2) if len(gs)>=3 else None,line=line_str(avg(gs)) if gs else ''))
out['kit']=kit
out['nopool_free']=[disp[k] for k in logs if k not in cur and k not in POOLS['2026-11-17'] and len(games(k,'2026-11-03',W1))>=4 and st.mean(g['min'] for g in games(k,'2026-11-03',W1))>=18]
out['free_n']=len([k for k in logs if k not in cur and len(games(k,'2026-11-03',W1))>=4 and st.mean(g['min'] for g in games(k,'2026-11-03',W1))>=18])
json.dump(out,open(os.path.join(HERE,'audit.json'),'w'),indent=1,default=str)
print('LINE',round(LINE,2),'L100',round(L100,2),'rival adds',len(rows),'unique',len({r['k'] for r in rows}),'unmatched',[r['player'] for r in rows if not r['matched']],'own adds',len(own),'free cands',len(free))
