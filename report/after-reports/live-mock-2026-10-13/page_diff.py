#!/usr/bin/env python3
"""What differs between the pages the card ran on? The engine, judgment and app blocks by hash (deck git + the unpublished
Version 64 working tree), the owner veto, and per-row prices / values / availability from val_<v>.json."""
import hashlib, json, os, re, subprocess
H = os.path.dirname(os.path.abspath(__file__))
DECK = os.environ.get("DECK_REPO", "/home/user/yahoo-fantasy-basketball")
page = lambda rev: subprocess.run(["git", "-C", DECK, "show", f"{rev}:docs/draft-deck.html"], capture_output=True, text=True, check=True).stdout
block = lambda h, t: (re.search(r'<script id="%s">(.*?)</script>' % t, h, re.S) or [None, ""])[1]
P = {"v58": page("b39838c"), "v59": page("85d778d"), "v60": page("7428778"), "v62": page("81032d7"), "v63": page("d9916ce")}
v64 = os.path.join(DECK, "docs/draft-deck.html")
P["v64"] = open(v64, encoding="utf-8").read()
print("v64 page sha256", hashlib.sha256(P["v64"].encode()).hexdigest()[:12])
for t in ["engine", "judgment", "app"]:
    print(t, {v: hashlib.sha256(block(h, t).encode()).hexdigest()[:10] for v, h in P.items()})
for v, h in P.items():
    print(v, "veto", re.findall(r'"([^"]+)"', re.search(r"doNotDraft:\s*\[(.*?)\]", block(h, "judgment"), re.S).group(1)))
V = {v: {r["n"]: r for r in json.load(open(os.path.join(H, f"val_{v}.json")))} for v in ["v59", "v60", "v63", "v64"]}
same = lambda a, b, k: sum(1 for n in V[a] if n in V[b] and V[a][n][k] == V[b][n][k])
for a, b in [("v59", "v60"), ("v60", "v63"), ("v59", "v63"), ("v63", "v64")]:
    print(f"{a} vs {b}: rows {len(V[a])}/{len(V[b])} · price identical {same(a, b, 'mkt')} · value identical {same(a, b, 'adj')} · availability identical {same(a, b, 'av')}")
