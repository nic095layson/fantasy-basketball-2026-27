import json,glob,os,sys,datetime as dt,collections,statistics as st,unicodedata,re,csv
KIT="KIT_RECORDS"
D=dt.date.fromisoformat
def key(s):
    s="".join(c for c in unicodedata.normalize("NFKD",s) if not unicodedata.combining(c)).lower()
    s=re.sub(r"[.'’`-]"," ",s); s=re.sub(r"\b(jr|sr|ii|iii|iv)\b","",s); return " ".join(s.split())
played=collections.defaultdict(dict); allnames=set()
for p in sorted(glob.glob(KIT+'/data/actuals/2026-1*.json')):
    d=os.path.basename(p)[:10]
    if d<'2026-10-20': continue
    for x in json.load(open(p))['players']:
        allnames.add(key(x['name']))
        if not x.get('dnp') and (x.get('min') or 0)>0: played[key(x['name'])][d]=x['min']
LAST='2026-11-10'
rows=json.load(open(sys.argv[1]))
names={r['player'] for r in rows}
nob=[n for n in names if key(n) not in allnames]
print("quoted players never in any box file (played or DNP), after a stricter name key:",len(nob),"of",len(names)); print("  ",sorted(nob)[:45])
pool={key(r['player']) for r in csv.DictReader(open(KIT+'/data/season/pool_season.csv'))}
print("of those, in the kit pool:",[n for n in nob if key(n) in pool])
for r in rows:
    g=sorted(d for d in played.get(key(r['player']),{}) if d>=r['pin']); r['actual']=g[0] if g else None
def rot(n,pin):   # a rotation player: in the kit pool
    return key(n) in pool
R=[r for r in rows if rot(r['player'],r['pin'])]
print("\nPOOL PLAYERS ONLY: quote-days",len(R),"players",len({r['player'] for r in R}))
ret=[r for r in R if r['actual']]
for r in ret: r['err']=(D(r['actual'])-D(r['quoted'])).days
def summ(rs,label):
    e=[r['err'] for r in rs]; n=len(e)
    if not n: print(label,"n=0"); return
    print(f"{label}: n={n} right(±1d) {sum(abs(x)<=1 for x in e)} ({100*sum(abs(x)<=1 for x in e)/n:.0f}%) | earlier {sum(x<-1 for x in e)} | later {sum(x>1 for x in e)} ({100*sum(x>1 for x in e)/n:.0f}%) | median {st.median(e):+.0f}d mean {st.mean(e):+.1f}d | late ones: median {st.median([x for x in e if x>1] or [0]):+.0f}d")
first={}; last={}
for r in sorted(ret,key=lambda r:r['pin']): first.setdefault((r['player'],r['actual']),r); last[(r['player'],r['actual'])]=r
summ(list(first.values()),"A. first quote per return"); summ(list(last.values()),"A. last quote before the return")
bylead=collections.defaultdict(list)
for r in first.values(): bylead["1-3d" if r['lead']<=3 else "4-7d" if r['lead']<=7 else "8d+"].append(r)
for k in ("1-3d","4-7d","8d+"): summ(bylead[k],f"   first quote, return quoted {k} out")
cens={r['player'] for r in R if not r['actual'] and (D(LAST)-D(r['quoted'])).days>1}
print("   quoted date passed by 2+ days, still no game:",len(cens),"players:",sorted(cens)[:20])
cut='2026-11-03'; G=[r for r in R if r['pin']<=cut]; n=len(G)
tab=collections.Counter(((r['lead']<=7), bool(r['actual']) and (D(r['actual'])-D(r['pin'])).days<=7) for r in G)
print(f"\nB. 7-day line, pool players, pins <= {cut}: quote-days {n}")
for k,lab in (((True,True),"kept, back within 7d (right)"),((True,False),"kept, not back within 7d (wrong keep)"),((False,True),"set aside, back within 7d (wrong set-aside)"),((False,False),"set aside, not back (right)")):
    print(f"   {lab}: {tab[k]} ({100*tab[k]/n:.0f}%)")
fp={}
for r in sorted(G,key=lambda r:r['pin']): fp.setdefault(r['player'],r)
t2=collections.Counter(((r['lead']<=7), bool(r['actual']) and (D(r['actual'])-D(r['pin'])).days<=7) for r in fp.values())
print("   per player, first quote:",{f"kept={a},back={b}":v for (a,b),v in sorted(t2.items())},"n",len(fp))
print("   other lines (quote-days right / kept, and of those kept how many were back within 7d):")
for L in (2,3,5,7,10):
    ok=sum(1 for r in G if (r['lead']<=L)==(bool(r['actual']) and (D(r['actual'])-D(r['pin'])).days<=7))
    kept=[r for r in G if r['lead']<=L]; kb=sum(1 for r in kept if r['actual'] and (D(r['actual'])-D(r['pin'])).days<=7)
    print(f"     {L:>2}d: right {100*ok/n:.0f}% | kept {len(kept)}, of which back in 7d {kb} ({100*kb/max(len(kept),1):.0f}%)")
print("   wrong keeps, pool players (pin, player, quoted, actual):")
seen=set()
for r in sorted(G,key=lambda r:r['pin']):
    if r['lead']<=7 and not (r['actual'] and (D(r['actual'])-D(r['pin'])).days<=7) and r['player'] not in seen:
        seen.add(r['player']); print("    ",r['pin'],r['player'],r['quoted'],r['actual'])
