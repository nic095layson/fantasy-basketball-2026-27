#!/usr/bin/env python3
"""Value rank (neutral weights, av>0, the replayer's VAL_RANK) and per-game line for every pool row of one page version."""
import json, re, subprocess, sys, tempfile, os
src, out = sys.argv[1], sys.argv[2]
if src.startswith("rev:"):
    rev, p = src[4:].split(":", 1)
    html = subprocess.run(["git", "-C", "/home/user/yahoo-fantasy-basketball", "show", f"{rev}:{p}"], capture_output=True, text=True, check=True).stdout
else:
    html = open(src, encoding="utf-8").read()
ex = lambda t: re.search(r'<script id="%s">(.*?)</script>' % t, html, re.S).group(1)
tmp = tempfile.mkdtemp(prefix="valrank-")
open(os.path.join(tmp, "deck.mjs"), "w").write(ex("data") + "\n" + ex("engine") + "\nexport const api = { PLAYERS, CATS, fitZ, marketRanks, adjValue };\n")
open(os.path.join(tmp, "run.mjs"), "w").write("""
import { api } from "./deck.mjs";
const { PLAYERS, CATS } = api;
const nw = {}; for (const c of CATS) nw[c] = 1.0;
const live = [...PLAYERS].filter(p => p.av > 0);
const byVal = live.sort((a, b) => api.fitZ(b, nw).adj - api.fitZ(a, nw).adj);
const MKT = api.marketRanks([...PLAYERS].filter(p => p.av > 0));
const out = PLAYERS.map(p => ({ n: p.n, t: p.t, p: p.p, av: p.av, mkt: p.mkt ?? null, mktRank: MKT.get(p.n) ?? null,
  valRank: p.av > 0 ? byVal.indexOf(p) + 1 : null, adj: p.av > 0 ? +api.fitZ(p, nw).adj.toFixed(4) : null,
  keys: Object.keys(p), raw: p.raw ?? p.s ?? null }));
process.stdout.write(JSON.stringify(out));
""")
r = subprocess.run(["node", os.path.join(tmp, "run.mjs")], capture_output=True, text=True)
if r.returncode: sys.exit(r.stderr[:2000])
json.dump(json.loads(r.stdout), open(out, "w"), ensure_ascii=False)
