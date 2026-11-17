"""Replay of the short-Out rule on the pinned ESPN feeds, 2026-10-28 to 2026-11-12 (run 2026-11-17 from a checkout of the
records branch with the working copy's co_gm.py and daily_brief.py; SEASON_POOL=data/season/pool_season.csv).

For every day and every player today's rule keeps in the scan as a "short Out" (Out, ESPN return date within 7 days):
did he play on or before that day's quoted return date? Three rules are compared on those instances:
  R0  today's: keep all
  RA  the rule built: keep only when the first day of the unbroken run of Out listings (7-day look-back) to the return
      date is at most 7 days
  RB  the alternative tried and rejected: keep only when the return date has not been pushed back within that run
Output of the run: rule_replay.txt beside this file."""
import sys, json, glob, os, datetime as dt, collections
sys.path.insert(0, 'scripts')
import co_gm as CG, daily_brief as DB, league_intake as LI
P, by = CG.load_pool()
logs = collections.defaultdict(list)
for f in sorted(glob.glob('data/actuals/*.json')):
    a = json.load(open(f))
    for p in a['players']:
        if not p.get('dnp') and (p.get('min') or 0) > 0:
            logs[LI.norm(p.get('pool_name') or p['name'])].append(a['date'])
days = sorted(os.path.basename(f)[14:24] for f in glob.glob('data/status/espn_injuries_2026-??-??.json'))
D = lambda s: dt.date.fromisoformat(s[:10])
esp = {}
for d in days:
    rows = json.load(open(f'data/status/espn_injuries_{d}.json'))['rows']
    res, _ = LI.resolve([r['player'] for r in rows], P, {})
    esp[d] = {res[r['player']]: r for r in rows if r['player'] in res}
inst = []
for d in days:
    if d > '2026-11-12':
        continue        # leave four or more days of box scores after the day
    yahoo, espn = DB.status_inputs(d)
    st = CG.fa_status(P, yahoo, espn, date=d)
    for n, s in st['by'].items():
        if not s['short_out']:
            continue
        ret = s['return_date'][:10]
        run = []
        for k in range(1, 8):
            day = (D(d) - dt.timedelta(days=k)).isoformat()
            r = esp.get(day, {}).get(n)
            if day not in esp or r is None or r['status'] != 'Out':
                break
            run.append((day, r.get('return_date') and r['return_date'][:10]))
        played = any(d <= x <= ret for x in logs.get(LI.norm(n), []))
        first = run[-1][0] if run else d
        q = [x for _, x in run if x]
        inst.append(dict(d=d, n=n, ret=ret, played=played, R0=True, RA=(D(ret) - D(first)).days <= 7, RB=(not q) or ret <= min(q)))
print('instances', len(inst), 'players', len({i['n'] for i in inst}), 'played by the quoted date', sum(i['played'] for i in inst))
for rule in ('R0', 'RA', 'RB'):
    keep = [i for i in inst if i[rule]]; aside = [i for i in inst if not i[rule]]
    print(rule, 'keeps', len(keep), 'played', sum(i['played'] for i in keep), '| sets aside', len(aside), 'played', sum(i['played'] for i in aside),
          sorted({i['n'] for i in aside if i['played']}))
