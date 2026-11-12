"""Forward check of the threes prior on this season's box scores (owner 2026-11-12).
    python3 forward_2026-27.py <records checkout> > forward_2026-27.txt"""
import os, sys, math, random, statistics
KIT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from math import lgamma
sys.path.insert(0,os.path.join(KIT,'scripts'))
import threes_line as TL, box_pull
W=sys.argv[1]   # a checkout of the records branch (data/actuals)
threes=TL.season_threes(W+'/data/actuals')            # this season: name -> (games, makes, attempts)
prior=TL.read_prior()
idx=box_pull.name_index([r['player'] for r in prior], box_pull.load_aliases()); by={r['player']:r for r in prior}
MU,K=0.3581,356.0
rows=[]
for name,(g,m,a) in threes.items():
    hit=box_pull.match_name(name,idx); r=by.get(hit) if hit else None
    if r and r['fg3a']>=100 and a>=20:
        rows.append((name,m,a,r['fg3'],r['fg3a']))
print('players',len(rows),'this-season attempts',sum(r[2] for r in rows),'makes',sum(r[1] for r in rows), 'pct %.4f'%(sum(r[1] for r in rows)/sum(r[2] for r in rows)),
      'last-season pct of same players %.4f'%(sum(r[3] for r in rows)/sum(r[4] for r in rows)), 'median last-season attempts',statistics.median(r[4] for r in rows))
def bb(m,n,p,w):
    a=p*w;b=(1-p)*w
    return lgamma(a+m)+lgamma(b+n-m)-lgamma(w+n)-(lgamma(a)+lgamma(b)-lgamma(w))
centers={'raw last-season %':lambda m0,n0:m0/n0, 'last-season % pulled toward league (K=356)':lambda m0,n0:(K*MU+m0)/(K+n0), 'league average only':lambda m0,n0:MU}
grid=[100,150,200,300,400,500,750,1000,1500,2500,5000,20000]
def best(rs,c):
    f=centers[c]; L={w:sum(bb(m,a,f(m0,n0),w) for _,m,a,m0,n0 in rs) for w in grid}
    return max(L,key=L.get),L
for c in centers:
    w,L=best(rows,c)
    print(c,'| best flat weight',w,'| logL at best %.2f'%L[w],'| at 750 %.2f'%L[750],'| at 356 ~400 %.2f'%L[400])
# variable weight K+n0 with shrunk centre (the textbook posterior)
f=centers['last-season % pulled toward league (K=356)']
print('textbook: centre pulled, weight K+n0: logL %.2f'%sum(bb(m,a,f(m0,n0),K+n0) for _,m,a,m0,n0 in rows))
# bootstrap the best flat weight for the raw centre
random.seed(2026); bw=[]
for i in range(500):
    s=[random.choice(rows) for _ in rows]; bw.append(best(s,'raw last-season %')[0])
bw.sort(); from collections import Counter
print('raw centre, best weight over 500 resamples:',sorted(Counter(bw).items()))
# plain prediction error of this season's % (attempt-weighted squared error), prior only
for c,f in centers.items():
    print(c,'weighted RMSE of this-season pct %.4f'%math.sqrt(sum(a*((m/a)-f(m0,n0))**2 for _,m,a,m0,n0 in rows)/sum(r[2] for r in rows)))
print('---')
raw=centers['raw last-season %']; pul=centers['last-season % pulled toward league (K=356)']
d=[bb(m,a,pul(m0,n0),750)-bb(m,a,raw(m0,n0),750) for _,m,a,m0,n0 in rows]
random.seed(7); tot=[]
for i in range(2000):
    tot.append(sum(random.choice(d) for _ in d))
tot.sort(); print('pulled minus raw at weight 750: logL gain %.2f, 95%% %.2f to %.2f, share of resamples above 0: %.3f'%(sum(d),tot[50],tot[1949],sum(1 for t in tot if t>0)/2000))
# what the candidate line would change for a few names (percentage centre only)
for n in ('Derrick White','Julian Champagnie','Ty Jerome','Cameron Johnson','Kevin Durant'):
    for r in rows:
        if r[0]==n: print(n,'last season %d of %d = %.3f; pulled centre %.3f; this season %d of %d'%(r[3],r[4],r[3]/r[4],pul(r[3],r[4]),r[1],r[2]))
