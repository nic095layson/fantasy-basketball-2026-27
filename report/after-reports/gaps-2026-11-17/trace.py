import json, os, sys, tempfile, csv
sys.path.insert(0, 'scripts')
state_p, pool_p, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.environ['SEASON_POOL'] = pool_p
import co_gm as CG
_, by = CG.load_pool()
state = json.load(open(state_p))
ros = CG.rosters(state, by)
work = tempfile.mkdtemp()
sims = {s: CG.run_league_sim(ros, s, 10000, work, tag='tr') for s in (2026, 2027)}
t = {s: sims[s]['teams'] for s in sims}
res = {seat: round((t[2026][seat]['champ'] + t[2027][seat]['champ']) / 2, 2) for seat in t[2026]}
me = [t[2026]['10']['champ'], t[2027]['10']['champ']]
json.dump(dict(state=state_p, pool=pool_p, title=res, me=me, n=len(ros[10]), absent=sims[2026].get('absent_from_sim'),
               played=sims[2026]['schedule']['played_weeks']), open(out, 'w'))
print(os.path.basename(state_p), os.path.basename(pool_p), 'me', res['10'], me, 'roster', len(ros[10]), 'played', sims[2026]['schedule']['played_weeks'])
