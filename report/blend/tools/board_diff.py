#!/usr/bin/env python3
"""Six-way blend 2026-10-14: the kit board before (top-200-2026-27.md at REV, default HEAD) and after (the working tree),
and the deck's value ranks before (Version 66's players.csv at DECK_REV) and after (the working tree). Read-only."""
import csv, io, json, os, re, subprocess, sys
KIT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
DECK = os.environ.get("DECK_REPO", "/home/user/yahoo-fantasy-basketball")
REV = sys.argv[1] if len(sys.argv) > 1 else "HEAD"; DECK_REV = sys.argv[2] if len(sys.argv) > 2 else "origin/main"
def board(text):
    out = {}
    for ln in text.splitlines():
        m = re.match(r"^\| (\d+) \| ([^|]+?) \| ([A-Z]{2,3}) \|", ln)
        if m: out[m.group(2)] = int(m.group(1))
    return out
git = lambda repo, rev, path: subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
kb, ka = board(git(KIT, REV, "report/top-200-2026-27.md")), board(open(os.path.join(KIT, "report/top-200-2026-27.md")).read())
sys.path.insert(0, os.path.join(DECK, "scripts")); import hoops, tempfile
def vranks(text):
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as t: t.write(text)
    hoops.DATA_PATH = t.name
    P = hoops.zscores(hoops.load_players()); live = [p for p in P if hoops.availability(p) > 0]
    os.unlink(t.name)
    return {p["player"]: i + 1 for i, p in enumerate(sorted(live, key=lambda p: -hoops.total_value(p)))}
db, da = vranks(git(DECK, DECK_REV, "data/players.csv")), vranks(open(os.path.join(DECK, "data/players.csv"), encoding="utf-8").read())
def summary(label, b, a, top):
    both = [n for n in b if n in a and b[n] <= top]
    mv = sorted(((n, b[n], a[n]) for n in both), key=lambda x: -abs(x[2] - x[1]))
    moved = [m for m in mv if m[1] != m[2]]
    print(f"{label}: {len(both)} players ranked 1-{top} before; {len(moved)} changed rank; mean |move| "
          f"{sum(abs(m[2]-m[1]) for m in mv)/len(mv):.2f}; |move| > 20: {sum(abs(m[2]-m[1]) > 20 for m in mv)}; "
          f"left the top {top}: {sum(1 for n in b if b[n] <= top and a.get(n, 999) > top)}")
    print("  largest: " + "; ".join(f"{n} {x}→{y}" for n, x, y in mv[:15]))
    return mv
print("top 12 kit before:", [n for n, _ in sorted(kb.items(), key=lambda x: x[1])[:12]])
print("top 12 kit after: ", [n for n, _ in sorted(ka.items(), key=lambda x: x[1])[:12]])
summary("kit board top 100", kb, ka, 100); summary("kit board top 200", kb, ka, 200)
print("top 12 deck before:", [n for n, _ in sorted(db.items(), key=lambda x: x[1])[:12]])
print("top 12 deck after: ", [n for n, _ in sorted(da.items(), key=lambda x: x[1])[:12]])
summary("deck value top 100", db, da, 100); summary("deck value top 156", db, da, 156)
for n in ("Kawhi Leonard", "Tyrese Haliburton", "Walker Kessler", "Kyrie Irving", "Anthony Davis", "Damian Lillard", "Chet Holmgren", "Yaxel Lendeborg",
          "Kel'el Ware", "Jalen Duren", "Donovan Clingan", "Zach Edey"):
    print(f"  {n}: kit {kb.get(n, '-')}→{ka.get(n, '-')}, deck value {db.get(n, '-')}→{da.get(n, '-')}")
