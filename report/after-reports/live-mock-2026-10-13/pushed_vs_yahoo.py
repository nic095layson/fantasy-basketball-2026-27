#!/usr/bin/env python3
"""The names the card pushed in this room (its 🎯s on Version 59 and on Version 63, and the owner's picks): our value rank
per page (val_<v>.json), Yahoo's own projected-line Rank / XRank / ADP (kit report/market/yahoo-proj-2026-10-13.csv),
the per-game line change v59 -> v63 (the deck's data/players.csv at 85d778d and d9916ce) and our v63 line minus Yahoo's."""
import json, csv, io, os, subprocess, unicodedata, re, statistics as st
H = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.normpath(os.path.join(H, "..", "..", ".."))
DECK = os.environ.get("DECK_REPO", "/home/user/yahoo-fantasy-basketball")
fold = lambda s: re.sub(r"[^a-z ]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip()
V = {v: {fold(r["n"]): r for r in json.load(open(os.path.join(H, f"val_{v}.json")))} for v in ["v59", "v60", "v63", "v64"]}
yp = {fold(r["player"]): r for r in csv.DictReader(open(os.path.join(KIT, "report/market/yahoo-proj-2026-10-13.csv")))}
def pc(rev):
    t = subprocess.run(["git", "-C", DECK, "show", f"{rev}:data/players.csv"], capture_output=True, text=True, check=True).stdout
    return {fold(r["player"]): r for r in csv.DictReader(io.StringIO(t))}
L59, L63 = pc("85d778d"), pc("d9916ce")
state = json.load(open(os.path.join(H, "draft_state_m76.json")))
went = {fold(p["player"]): i + 1 for i, p in enumerate(state["picks"])}
card = {v: {t["pick"]: t for t in json.load(open(os.path.join(H, f"card_{v}.json")))} for v in ["v59", "v60", "v63"]}
t63 = sorted({t["targetName"] for t in card["v63"].values()}, key=lambda n: V["v63"][fold(n)]["valRank"])
t59 = sorted({t["targetName"] for t in card["v59"].values()}, key=lambda n: V["v59"][fold(n)]["valRank"])
mine = [t["actual"] for t in card["v63"].values()]
def row(n):
    k = fold(n); y = yp.get(k, {}); a, b = L59.get(k), L63.get(k)
    cats = ["pts", "reb", "ast", "stl", "blk", "tpm", "tov"]
    d = " ".join(f"{c}{float(b[c]) - float(a[c]):+.1f}" for c in cats if a and b and abs(float(b[c]) - float(a[c])) >= 0.3) if a and b else "-"
    vy = " ".join(f"{c}{float(b[c]) - float(y[c]):+.1f}" for c in cats if b and y.get(c) and abs(float(b[c]) - float(y[c])) >= 0.5) if b and y else "-"
    return (f"{n:<24} val v59 {V['v59'][k]['valRank']!s:>4} v60 {V['v60'][k]['valRank']!s:>4} v63 {V['v63'][k]['valRank']!s:>4} | "
            f"Yahoo rank {y.get('yrank','-'):>4} xrank {y.get('xrank','-'):>4} adp {y.get('adp','-'):>6} | went #{went.get(k,'-')} | "
            f"line v59→v63: {d or 'unchanged'} | v63 minus Yahoo: {vy or 'within 0.5'}")
print("== 🎯s on today's page (Versions 62/63) in this room")
for n in t63: print(row(n))
print("== 🎯s on the practice page (Version 59) in this room")
for n in t59: print(row(n))
print("== the owner's own picks")
for n in mine: print(row(n))
def gap(names, v):
    return [V[v][fold(n)]["valRank"] - int(yp[fold(n)]["yrank"]) for n in names if fold(n) in yp and yp[fold(n)]["yrank"]]
for lab, names, v in [("today's 🎯s, value rank on v63 minus Yahoo rank", t63, "v63"), ("practice 🎯s, value rank on v59 minus Yahoo rank", t59, "v59")]:
    g = gap(names, v); print(f"{lab}: {g} median {st.median(g)}")
