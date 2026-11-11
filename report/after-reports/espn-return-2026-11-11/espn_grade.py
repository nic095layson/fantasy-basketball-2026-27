import json,glob,os,sys,datetime as dt,collections,statistics as st
KIT="KIT_RECORDS"; sys.path.insert(0,KIT+"/scripts")
import box_pull
D=dt.date.fromisoformat
fold=box_pull.fold if hasattr(box_pull,'fold') else (lambda s:s.lower())
# games played: name -> sorted dates with minutes; team game dates
played=collections.defaultdict(set); team_games=collections.defaultdict(set)
for p in sorted(glob.glob(KIT+'/data/actuals/2026-1*.json')):
    d=os.path.basename(p)[:10]; a=json.load(open(p))
    if d<'2026-10-20': continue
    for x in a['players']:
        team_games[x['team']].add(d)
        if not x.get('dnp') and (x.get('min') or 0)>0:
            played[fold(x['name'])].add(d)
            if x.get('pool_name'): played[fold(x['pool_name'])].add(d)
LAST=max(d for s in team_games.values() for d in s)
pins=sorted(glob.glob(KIT+'/data/status/espn_injuries_2026-1?-??.json'))
quotes=[]  # (pin, player, team, return_date)
for p in pins:
    r=json.load(open(p)); pin=r['date'] if len(r.get('date',''))==10 else os.path.basename(p)[14:24]
    for x in r['rows']:
        if x['status']=='Out' and x.get('return_date'): quotes.append((pin,x['player'],x['team'],x['return_date']))
print("pins",len(pins),os.path.basename(pins[0])[14:24],"to",os.path.basename(pins[-1])[14:24],"| box scores through",LAST,"| Out quotes with a date:",len(quotes),"| players:",len({q[1] for q in quotes}))
def first_game_after(name,pin):
    g=sorted(d for d in played.get(fold(name),()) if d>=pin)   # a morning pin: a game that same day counts
    return g[0] if g else None
rows=[]
for pin,name,team,ret in quotes:
    act=first_game_after(name,pin)
    rows.append(dict(pin=pin,player=name,team=team,quoted=ret,actual=act,lead=(D(ret)-D(pin)).days))
# name-match sanity: how many quoted players ever appear in box scores at all
ever={q[1] for q in quotes if played.get(fold(q[1]))}
print("quoted players with any box line this season:",len(ever),"of",len({q[1] for q in quotes}))
# A. accuracy of the quoted date, for quotes whose player has returned
ret=[r for r in rows if r['actual']]
for r in ret: r['err']=(D(r['actual'])-D(r['quoted'])).days
def summ(rs,label):
    if not rs: print(label,"n=0"); return
    e=[r['err'] for r in rs]
    right=sum(abs(x)<=1 for x in e); early=sum(x<-1 for x in e); late=sum(x>1 for x in e)
    print(f"{label}: n={len(e)} right(±1d) {right} ({100*right/len(e):.0f}%) | back earlier than quoted {early} ({100*early/len(e):.0f}%) | later {late} ({100*late/len(e):.0f}%) | median error {st.median(e):+.0f}d, mean {st.mean(e):+.1f}d")
print("\nA. Quotes for players who have since played (error = actual return minus quoted date):")
summ(ret,"  all quote-days")
# one row per player-episode: the FIRST quote seen for each (player, actual return)
first={}
for r in sorted(ret,key=lambda r:r['pin']): first.setdefault((r['player'],r['actual']),r)
summ(list(first.values()),"  first quote per return (one per player-return)")
last={}
for r in sorted(ret,key=lambda r:r['pin']): last[(r['player'],r['actual'])]=r
summ(list(last.values()),"  last quote before the return")
# censored: quoted date passed (by >1 day) and player has not played since pin
cens=[r for r in rows if not r['actual'] and (D(LAST)-D(r['quoted'])).days>1]
cp={r['player'] for r in cens}
print(f"\n   quotes whose date has passed by 2+ days with no game since: {len(cens)} quote-days, {len(cp)} players (these are 'late', size unknown)")
# how the quote moves: per player, number of distinct quoted dates
dates=collections.defaultdict(set)
for r in rows: dates[r['player']].add(r['quoted'])
c=collections.Counter(len(v) for v in dates.values()); print("   distinct quoted dates per player:",dict(sorted(c.items())))
# B. the 7-day line: kept (lead<=7) vs set aside; truth = played within 7 days of the pin
print("\nB. The 7-day line, graded only on pins with 7 days of box scores after them (pin <= %s):"%(D(LAST)-dt.timedelta(days=7)).isoformat())
cut=(D(LAST)-dt.timedelta(days=7)).isoformat()
tab=collections.Counter(); ex=collections.defaultdict(list)
for r in rows:
    if r['pin']>cut: continue
    kept=r['lead']<=7
    back=bool(r['actual']) and (D(r['actual'])-D(r['pin'])).days<=7
    tab[(kept,back)]+=1; ex[(kept,back)].append(r)
n=sum(tab.values()); print("   quote-days graded:",n)
for k,lab in (((True,True),"kept in the scan, was back within 7 days (right)"),((True,False),"kept in the scan, NOT back within 7 days (wrong keep)"),((False,True),"set aside, but was back within 7 days (wrong set-aside)"),((False,False),"set aside, not back within 7 days (right)")):
    print(f"   {lab}: {tab[k]} ({100*tab[k]/n:.0f}%)")
# per-player version (first quote per player in the gradable window)
fp={}
for r in sorted(rows,key=lambda r:r['pin']):
    if r['pin']<=cut: fp.setdefault(r['player'],r)
t2=collections.Counter(((r['lead']<=7), bool(r['actual']) and (D(r['actual'])-D(r['pin'])).days<=7) for r in fp.values())
print("   per player (first quote):",{f"kept={k[0]},back={k[1]}":v for k,v in sorted(t2.items())}, "n",len(fp))
# alternative lines
print("\n   other lines, same quote-days (share classified right):")
for L in (3,5,7,10,14):
    ok=sum(1 for r in rows if r['pin']<=cut and ((r['lead']<=L)==(bool(r['actual']) and (D(r['actual'])-D(r['pin'])).days<=7)))
    keep=sum(1 for r in rows if r['pin']<=cut and r['lead']<=L)
    print(f"     line {L:>2}d: right {100*ok/n:.0f}%  (kept {keep} of {n})")
print("\n   wrong keeps (first 12, pin / player / quoted / actual):")
seen=set()
for r in ex[(True,False)]:
    if r['player'] in seen: continue
    seen.add(r['player']); print("    ",r['pin'],r['player'],r['team'],r['quoted'],r['actual'])
    if len(seen)>=12: break
print("   wrong set-asides:")
seen=set()
for r in ex[(False,True)]:
    if r['player'] in seen: continue
    seen.add(r['player']); print("    ",r['pin'],r['player'],r['team'],r['quoted'],r['actual'])
json.dump(rows,open(os.path.dirname(os.path.abspath(__file__))+"/espn_grade_rows.json","w"))
