import sys,json,glob,statistics as st,random,collections
sys.path.insert(0,'/home/user/wtsd/scripts'); import form_board as FB
recs=[json.load(open(p)) for p in sorted(glob.glob('/home/user/wtsd/data/actuals/2026-1*.json'))]
recs=[r for r in recs if r.get('games') and all(g.get('season_type')==2 for g in r['games'])]
log=FB.game_log(recs); mean=lambda x: sum(x)/len(x) if x else float('nan')
# every regular-season date each NBA team played
team_dates=collections.defaultdict(set)
for r in recs:
    day=r['date']
    for g in r['games']:
        c=g.get('context') or {}
        for t in (c.get('home'),c.get('away')):
            if t: team_dates[t].add(day)
team_dates={t:sorted(v) for t,v in team_dates.items()}
rows=[]
for pl,g in log.items():
    played={x['date']:x for x in g}; prev=False
    for t in range(FB.TREND_MIN_GAMES, len(g)+1):
        s=FB.summarize(g[:t]); last=g[t-1]
        up_m=s['trend']=='up'; up_u=(s.get('usg_trend')=='up' and s['trend']!='down'); flag=up_m or up_u
        kind='minutes' if up_m else 'usage only' if up_u else 'none'
        nxt_dates=[d for d in team_dates.get(last['team'],[]) if d>last['date']][:3]
        if len(nxt_dates)==3:                           # the TEAM has three later games; he may or may not appear
            app=[played.get(d) for d in nxt_dates]
            mins=[(x['min'] if x else 0) for x in app]; pts=[(x['pts'] if x else 0) for x in app]
            pg=[x for x in app if x]
            rows.append(dict(p=pl,flag=flag,onset=flag and not prev,kind=kind,prior=s['prior_mpg'],last3=s['last3_mpg'],season=s['mpg'],
                             appear=len(pg)/3, team3_min=mean(mins), team3_pts=mean(pts), pts_season=s['per_game']['pts'],
                             pts36_before=s['per36']['pts'], pts36_next=(36*sum(x['pts'] for x in pg)/sum(x['min'] for x in pg)) if pg and sum(x['min'] for x in pg) else None,
                             played_min=mean([x['min'] for x in pg]) if pg else None))
        prev=flag
print('player-dates with three later TEAM games:',len(rows),'| players',len({r['p'] for r in rows}))
def show(lab,rs):
    p36=[(r['pts36_next']-r['pts36_before']) for r in rs if r['pts36_next'] is not None]
    print(f"{lab:30s} n={len(rs):4d} | appeared in {100*mean([r['appear'] for r in rs]):3.0f}% of the team's next 3 | minutes per TEAM game (missed = 0): before {mean([r['season'] for r in rs]):5.1f} next {mean([r['team3_min'] for r in rs]):5.1f} ({mean([r['team3_min']-r['season'] for r in rs]):+.1f}) | points per team game: before {mean([r['pts_season'] for r in rs]):5.1f} next {mean([r['team3_pts'] for r in rs]):5.1f} ({mean([r['team3_pts']-r['pts_season'] for r in rs]):+.1f}) | points per 36 change {mean(p36):+.1f}")
on=[r for r in rows if r['onset']]
show('minutes up 6+ (onsets)',[r for r in on if r['kind']=='minutes'])
show('usage up 4+ only (onsets)',[r for r in on if r['kind']=='usage only'])
show('not flagged',[r for r in rows if not r['flag']])
show('minutes, under 26 mpg',[r for r in on if r['kind']=='minutes' and r['season']<26])
show('usage only, under 26 mpg',[r for r in on if r['kind']=='usage only' and r['season']<26])
show('not flagged, under 26 mpg',[r for r in rows if not r['flag'] and r['season']<26])
random.seed(3); P=sorted({r['p'] for r in rows}); byp=collections.defaultdict(list)
for r in rows: byp[r['p']].append(r)
res=collections.defaultdict(list)
for i in range(1000):
    s=[r for p in random.choices(P,k=len(P)) for r in byp[p]]
    base=[r for r in s if not r['flag']]
    for k in ('minutes','usage only'):
        f=[r for r in s if r['onset'] and r['kind']==k]
        if f and base:
            res[k,'min'].append(mean([r['team3_min']-r['season'] for r in f])-mean([r['team3_min']-r['season'] for r in base]))
            res[k,'pts'].append(mean([r['team3_pts']-r['pts_season'] for r in f])-mean([r['team3_pts']-r['pts_season'] for r in base]))
            res[k,'app'].append(100*(mean([r['appear'] for r in f])-mean([r['appear'] for r in base])))
for k,v in res.items():
    v=sorted(v); print(k,'edge over unflagged: median %.2f, 95%% %.2f to %.2f'%(v[len(v)//2],v[25],v[-26]))
# longer horizon for the minutes trigger: next 5 games he played
r5=[]
for pl,g in log.items():
    prev=False
    for t in range(FB.TREND_MIN_GAMES, len(g)-4):
        s=FB.summarize(g[:t]); up=s['trend']=='up'
        if up and not prev: r5.append((s['prior_mpg'],s['last3_mpg'],mean([x['min'] for x in g[t:t+3]]),mean([x['min'] for x in g[t+3:t+5]])))
        prev=up or (s.get('usg_trend')=='up' and s['trend']!='down')
print('minutes trigger with 5 later games: n=%d | prior %.1f last3 %.1f games 1-3 after %.1f games 4-5 after %.1f'%(len(r5),*[mean([x[i] for x in r5]) for i in range(4)]))
