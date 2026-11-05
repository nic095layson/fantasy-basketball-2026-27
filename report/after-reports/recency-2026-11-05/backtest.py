import json, glob, csv, os, sys, math, random, collections
os.chdir('/home/user/wtsd'); S = sys.argv[1]
PRIOR = {"FG%": 26.0, "FT%": 37.5, "3PM": 9.5, "PTS": 11.7, "REB": 12.4, "AST": 11.7, "STL": 21.7, "BLK": 14.5, "TO": 14.0}
CNT = {"PTS": "pts", "REB": "reb", "AST": "ast", "STL": "stl", "BLK": "blk", "3PM": "tpm", "TO": "tov"}
pre = {r['player']: r for r in csv.DictReader(open('/home/user/yahoo-fantasy-basketball/arena/results/players_v69.csv'))}
games = collections.defaultdict(list)
for f in sorted(glob.glob('data/actuals/2026-1*.json')):
    for r in json.load(open(f))['players']:
        n = r.get('pool_name') or r['name']
        if r.get('dnp') or r.get('min', 0) <= 0 or n not in pre: continue
        games[n].append(r)
MIN_G = int(sys.argv[2]) if len(sys.argv) > 2 else 6
ROLE = os.environ.get("ROLE")
def shift(g):
    return sum(h["min"] for h in g[-4:]) / 4 - sum(h["min"] for h in g[:4]) / 4
players = [n for n, g in games.items() if len(g) >= MIN_G and
           (abs(shift(g)) >= 6 if ROLE == "moved" else abs(shift(g)) < 6 if ROLE == "stable" else True)]
print('players', len(players), 'min games', MIN_G, file=sys.stderr)

def est_counting(hist, p, cat, key, kind, hl=None, kmul=1.0):
    k = PRIOR[cat] * kmul; n = len(hist); vals = [h[key] for h in hist]
    if kind == 'pre': return p
    if kind == 'season': return sum(vals) / n
    if kind == 'last4': v = vals[-4:]; return sum(v) / len(v)
    if kind == 'ewma':
        w = [0.5 ** ((n - 1 - i) / hl) for i in range(n)]; return sum(x * y for x, y in zip(vals, w)) / sum(w)
    if kind == 'blend': return (k * p + sum(vals)) / (k + n)
    if kind == 'blend_ewma':   # the prior as before; the actuals recency-weighted, their total weight kept at n games
        w = [0.5 ** ((n - 1 - i) / hl) for i in range(n)]; sw = sum(w)
        return (k * p + n * sum(x * y for x, y in zip(vals, w)) / sw) / (k + n)
    raise ValueError(kind)

def est_pct(hist, pp, pa, cat, mk, ak, kind, hl=None, kmul=1.0):
    k = PRIOR[cat] * kmul; n = len(hist)
    made = [h[mk] for h in hist]; att = [h[ak] for h in hist]
    if kind == 'pre': return pp
    if kind == 'season': return sum(made) / sum(att) if sum(att) else pp
    if kind == 'last4': m, a = sum(made[-4:]), sum(att[-4:]); return m / a if a else pp
    if kind == 'ewma':
        w = [0.5 ** ((n - 1 - i) / hl) for i in range(n)]
        m, a = sum(x * y for x, y in zip(made, w)), sum(x * y for x, y in zip(att, w)); return m / a if a else pp
    if kind == 'blend': return (k * pa * pp + sum(made)) / (k * pa + sum(att))
    if kind == 'blend_ewma':
        w = [0.5 ** ((n - 1 - i) / hl) for i in range(n)]; sw = sum(w)
        m = n * sum(x * y for x, y in zip(made, w)) / sw; a = n * sum(x * y for x, y in zip(att, w)) / sw
        return (k * pa * pp + m) / (k * pa + a)
    raise ValueError(kind)

EST = [('preseason', 'pre', None, 1), ('blend (current)', 'blend', None, 1), ('season mean', 'season', None, 1),
       ('last 4', 'last4', None, 1), ('ewma hl3', 'ewma', 3, 1), ('ewma hl6', 'ewma', 6, 1),
       ('blend, prior /2', 'blend', None, 0.5), ('blend, prior x2', 'blend', None, 2),
       ('blend + ewma hl3 actuals', 'blend_ewma', 3, 1), ('blend + ewma hl6 actuals', 'blend_ewma', 6, 1)]
# errors[est][cat] = list of (player, abs err, signed err)
err = {e[0]: collections.defaultdict(list) for e in EST}
MINP = 4
for n in players:
    g = games[n]; p = pre[n]
    pre_c = {cat: float(p[CNT[cat]]) for cat in CNT}; pre_min = None
    for t in range(MINP, len(g)):
        hist, nxt = g[:t], g[t]
        for label, kind, hl, km in EST:
            for cat, key in CNT.items():
                e = est_counting(hist, pre_c[cat], cat, key, kind, hl, km); d = nxt[key] - e
                err[label][cat].append((n, abs(d), d))
            for cat, pk, ak_, mk, ak in (("FG%", 'fg_pct', 'fga', 'fgm', 'fga'), ("FT%", 'ft_pct', 'fta', 'ftm', 'fta')):
                if nxt[ak] <= 0: continue
                e = est_pct(hist, float(p[pk]), float(p[ak_]), cat, mk, ak, kind, hl, km)
                d = nxt[mk] - e * nxt[ak]          # made vs expected made on the game's own attempts
                err[label][cat].append((n, abs(d), d))
            # minutes: no preseason minutes column in the pool, so 'pre' uses the season mean of games 1..MINP-1 as a stand-in
            key = 'min'; vals = [h[key] for h in hist]
            if kind == 'pre': e = sum(vals[:MINP]) / MINP
            else: e = est_counting(hist, sum(vals[:MINP]) / MINP, 'PTS', key, kind, hl, km)
            d = nxt[key] - e; err[label]['MIN'].append((n, abs(d), d))

cats = list(CNT) + ['FG%', 'FT%', 'MIN']
base = 'blend (current)'
random.seed(2026)
def boot_diff(a, b, B=2000):
    """bootstrap over players of mean(|err_a|) - mean(|err_b|); returns (mean, lo, hi)"""
    byp = collections.defaultdict(lambda: [0.0, 0.0, 0])
    for (n, ea, _), (_, eb, _) in zip(a, b):
        byp[n][0] += ea; byp[n][1] += eb; byp[n][2] += 1
    names = list(byp); diffs = []
    for _ in range(B):
        samp = [byp[random.choice(names)] for _ in names]
        diffs.append(sum(x[0] - x[1] for x in samp) / sum(x[2] for x in samp))
    diffs.sort(); m = sum(x[0] - x[1] for x in byp.values()) / sum(x[2] for x in byp.values())
    return m, diffs[int(0.025 * B)], diffs[int(0.975 * B)]
out = {'players': len(players), 'min_games': MIN_G, 'player_games': len(err[base]['PTS']), 'cats': {}}
for cat in cats:
    row = {}
    for label, *_ in EST:
        a = err[label][cat]; mae = sum(x[1] for x in a) / len(a); bias = sum(x[2] for x in a) / len(a)
        m, lo, hi = boot_diff(a, err[base][cat]) if label != base else (0, 0, 0)
        wins = sum(1 for x, y in zip(a, err[base][cat]) if x[1] < y[1]) / len(a) if label != base else None
        row[label] = dict(mae=round(mae, 3), bias=round(bias, 3), d_vs_blend=round(m, 3), lo=round(lo, 3), hi=round(hi, 3), beats_blend_share=None if wins is None else round(wins, 3))
    out['cats'][cat] = row
json.dump(out, open(os.path.join(S, f'backtest_min{MIN_G}_{ROLE or "all"}.json'), 'w'), indent=1)
print('player-games', out['player_games'])
for cat in cats:
    print(f'== {cat}')
    for label, r in out['cats'][cat].items():
        print(f"  {label:28s} MAE {r['mae']:7.3f} bias {r['bias']:+7.3f} vs blend {r['d_vs_blend']:+7.3f} [{r['lo']:+.3f},{r['hi']:+.3f}] beats {r['beats_blend_share']}")
