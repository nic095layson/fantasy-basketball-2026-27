#!/usr/bin/env python3
"""WO-5 acceptance: the top 60 of both boards, name by name, against the five outside rank files in report/market/
(the newest of each: Yahoo projected rank, Hashtag 9-cat, Rotoworld 9-cat, RotoBaller, RotoWire's expert panel —
the repeat-name check's four plus RotoWire; Yahoo ADP is shown as the price, not counted). Every source 25+ places
away is a divergence; each divergent player gets one line built from the records: the side, the categories that
carry his value in the deck's frame (largest z first, the sign that explains the side), and how his line was made.
Usage: wo5_top60.py <lines.json> <out.json> <out.md>"""
import sys, os, json, csv, re, glob, unicodedata
DECK = os.environ.get("DECK_REPO", "/home/user/yahoo-fantasy-basketball"); KIT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, DECK + "/scripts"); sys.path.insert(0, os.path.join(KIT, "report"))
import hoops, repeat_market_check as RMC
import rank_engine as RE
LJ, OJ, OM = sys.argv[1:4]
idx = RMC.kit_aliases(KIT)
canon = lambda s: RMC.canon(s, idx)
SRC = list(RMC.RANK_SOURCES) + [("RotoWire", r"rotowire-\d{4}-\d{2}-\d{2}\.csv", "player", "src_rank")]
lists = {}
for label, pat, ncol, rcol in SRC:
    f = RMC.newest(KIT, pat)
    ranks = {}
    for r in csv.DictReader(open(f, encoding="utf-8-sig")):
        try: ranks.setdefault(canon(r[ncol]), int(float(r[rcol])))
        except (KeyError, TypeError, ValueError): continue
    lists[label] = (os.path.basename(f), ranks, max(ranks.values()))
yf = sorted(glob.glob(os.path.join(KIT, "report", "market", "yahoo-2026-*.csv")))
yf = [f for f in yf if re.fullmatch(r"yahoo-\d{4}-\d{2}-\d{2}\.csv", os.path.basename(f))][-1]
adp = {canon(r["player"]): r["adp"] for r in csv.DictReader(open(yf, encoding="utf-8-sig"))}
P = hoops.zscores(hoops.load_players()); live = sorted([p for p in P if hoops.availability(p) > 0], key=lambda p: -hoops.adj_value(p, ()))
deck = {canon(p["player"]): (i + 1, p) for i, p in enumerate(live)}
rows = RE.load(os.path.join(KIT, "report", "projections-2026-27.csv")); rows, held = RE.exclude_held(rows)
z1 = RE.zscores(rows, rows); pool = sorted(rows, key=lambda r: -RE.total(z1[r["name"]]))[:RE.POOL_SIZE]; z2 = RE.zscores(rows, pool)
for r in rows:
    t = RE.total(z2[r["name"]]); av = RE.avail(r["gp"]); r["z_adj"] = t * av if t > 0 else t
kitr = {canon(r["name"]): i + 1 for i, r in enumerate(sorted(rows, key=lambda r: -r["z_adj"]))}
L = {}
for r in json.load(open(LJ, encoding="utf-8"))["rows"]:
    L[canon(r["name"])] = r
def basis(k):
    x = L.get(k) or {}
    if not x.get("new"): return "line held (rookie translation)"
    m = x["meta"]
    if str(m.get("base", "")).startswith("rookie"): return "rookie translation (range rule)"
    g = x.get("range") or {}
    s = f"{m['base']} line at {m['minutes']:.1f} min"
    if g.get("factor", 1) != 1: s += " (minutes to the outside range)"
    elif str(x.get("minutes_source", "")).startswith("override"): s += " (role move)"
    return s
names = {k for k, (r, p) in deck.items() if r <= 60} | {k for k, r in kitr.items() if r <= 60}
out = []
for k in sorted(names, key=lambda k: min(deck.get(k, (999,))[0], kitr.get(k, 999))):
    dr, p = deck.get(k, (None, None)); kr = kitr.get(k)
    ours = min(x for x in (dr, kr) if x)
    src = {}
    for label, (fn, ranks, mx) in lists.items():
        src[label] = ranks.get(k)
    div = {}
    for label, v in src.items():
        theirs = v if v is not None else lists[label][2] + 1
        for side, mine in (("deck", dr), ("kit", kr)):
            if mine is not None and mine <= 60 and abs(mine - theirs) >= 25:
                div.setdefault(label, theirs if v is not None else f">{lists[label][2]}")
    line = ""
    if div and p is not None:
        vals = [x if isinstance(x, int) else lists[l][2] + 1 for l, x in div.items()]
        higher = sum(1 for v in vals if v > ours) >= sum(1 for v in vals if v < ours)
        z = p["z"]
        top = sorted(z.items(), key=lambda kv: (-kv[1] if higher else kv[1]))[:3]
        line = (("we rank him higher: " if higher else "we rank him lower: ") +
                ", ".join(f"{c} {v:+.2f}" for c, v in top) + " z carry it; " + basis(k))
        if hoops.availability(p) < 1: line += "; availability x0.78 already applied"
    out.append(dict(player=(p["player"] if p else k), deck=dr, kit=kr, adp=adp.get(k), sources=src, divergent=div, explanation=line))
json.dump(dict(sources={l: v[0] for l, v in lists.items()}, adp_file=os.path.basename(yf), rows=out), open(OJ, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
labels = list(lists)
md = ["| player | deck | kit | ADP | " + " | ".join(labels) + " | divergence (25+) — why |", "|---|---|---|---|" + "---|" * len(labels) + "---|"]
for r in out:
    cells = []
    for l in labels:
        v = r["sources"][l]; c = "—" if v is None else str(v)
        if l in r["divergent"]: c = f"**{c}**"
        cells.append(c)
    md.append(f"| {r['player']} | {r['deck'] or '—'} | {r['kit'] or '—'} | {r['adp'] or '—'} | " + " | ".join(cells) + f" | {r['explanation'] or 'none'} |")
open(OM, "w", encoding="utf-8").write("\n".join(md) + "\n")
print(f"top-60 review: {len(out)} names (union of both boards' top 60); {sum(1 for r in out if r['divergent'])} with a 25+ divergence; "
      f"{sum(len(r['divergent']) for r in out)} source divergences; sources {', '.join(f'{l} {v[0]}' for l, v in lists.items())}")
