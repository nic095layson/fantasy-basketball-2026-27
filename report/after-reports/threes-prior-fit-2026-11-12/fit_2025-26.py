"""Audit of the 750-attempt threes prior (owner 2026-11-12): beta-binomial fit of three-point talent on the 2025-26 totals.
    python3 fit_2025-26.py > fit_2025-26.txt"""
import csv, math, os, random
from math import lgamma
K=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))   # the kit
rows=[(r['player'],int(r['fg3']),int(r['fg3a'])) for r in csv.DictReader(open(K+'/data/reference/threes_prior_2025-26.csv'))]
def ll(data,mu,k):
    a=mu*k;b=(1-mu)*k
    return sum(lgamma(a+m)+lgamma(b+n-m)-lgamma(k+n)-(lgamma(a)+lgamma(b)-lgamma(k)) for m,n in data)
def mle(data):
    mu=sum(m for m,n in data)/sum(n for m,n in data)
    best=None
    # golden search over log k, with mu refined on a small grid
    for mu_ in [mu+d for d in (-0.01,-0.005,0,0.005,0.01)]:
        lo,hi=math.log(20),math.log(20000)
        for _ in range(60):
            a=lo+(hi-lo)*0.382; b=lo+(hi-lo)*0.618
            if ll(data,mu_,math.exp(a))>ll(data,mu_,math.exp(b)): hi=b
            else: lo=a
        k=math.exp((lo+hi)/2); v=ll(data,mu_,k)
        if best is None or v>best[0]: best=(v,mu_,k)
    return best[1],best[2]
def mom(data):
    N=sum(n for m,n in data); mu=sum(m for m,n in data)/N
    # attempts-weighted: observed var of p minus mean binomial var
    w=[n for m,n in data]; W=sum(w)
    obs=sum(n*((m/n)-mu)**2 for m,n in data)/W
    samp=sum(n*(mu*(1-mu)/n) for m,n in data)/W
    tv=obs-samp
    return mu,(mu*(1-mu)/tv-1) if tv>0 else float('inf'),obs,samp
random.seed(2026)
for cut in (50,100,200):
    d=[(m,n) for _,m,n in rows if n>=cut]
    mu,k=mle(d); mm=mom(d)
    bs=[]
    for i in range(1000 if cut==100 else 200):
        s=[random.choice(d) for _ in d]; bs.append(mle(s)[1])
    bs.sort()
    print(f"cut {cut}+: players {len(d)}, attempts {sum(n for m,n in d)}, mean {mu:.4f}, MLE K {k:.0f}, 95% {bs[int(.025*len(bs))]:.0f}-{bs[int(.975*len(bs))]:.0f} ({len(bs)} resamples), moments K {mm[1]:.0f}, true sd of talent {math.sqrt(mu*(1-mu)/(k+1)):.4f}")
