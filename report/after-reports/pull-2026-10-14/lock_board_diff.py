"""Board effect of the three lock calls (lock_calls.py): the kit board at HEAD against the working tree, and the deck's
value ranks (hoops.total_value over live rows, the page's own order) for players.csv at DECK_REV against the working
tree. Before the lock calls the two planes differed from these revisions by notes only, which move no value. Read-only;
writes lock_board_diff_2026-10-14.json."""
import csv, io, json, os, re, subprocess, sys, tempfile
H = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.normpath(os.path.join(H, "..", "..", ".."))
DECK = "/home/user/yahoo-fantasy-basketball"; REV = "HEAD"; DECK_REV = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
git = lambda repo, rev, path: subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
def board(text):
    out = {}
    for ln in text.splitlines():
        m = re.match(r"^\| (\d+) \| ([^|]+?) \| ([A-Z]{2,3}) \|(?:[^|]*\|){1}\s*(\d+)\s*\|(?:[^|]*\|){3}\s*([+-][\d.]+)\s*\|", ln)
        if m: out[m.group(2)] = {"rank": int(m.group(1)), "gp": int(m.group(4)), "zadj": float(m.group(5))}
    return out
sys.path.insert(0, os.path.join(DECK, "scripts")); import hoops
def vranks(text):
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as t: t.write(text)
    hoops.DATA_PATH = t.name
    P = hoops.zscores(hoops.load_players()); live = [p for p in P if hoops.availability(p) > 0]
    os.unlink(t.name)
    return {p["player"]: i + 1 for i, p in enumerate(sorted(live, key=lambda p: -hoops.total_value(p)))}
kb, ka = board(git(KIT, REV, "report/top-200-2026-27.md")), board(open(os.path.join(KIT, "report/top-200-2026-27.md")).read())
db, da = vranks(git(DECK, DECK_REV, "data/players.csv")), vranks(open(os.path.join(DECK, "data/players.csv"), encoding="utf-8").read())
assert len(kb) == len(ka) == 200
def summary(b, a, top):
    names = [n for n in b if b[n] <= top]
    mv = [(n, b[n], a.get(n)) for n in names if a.get(n) != b[n]]
    entered = sorted((n for n in a if a[n] <= top and (n not in b or b[n] > top)), key=lambda n: a[n])
    left = sorted((n for n in names if a.get(n) is None or a[n] > top), key=lambda n: b[n])
    return {"top": top, "changed": len(mv), "mean_abs_move": round(sum(abs((a.get(n) or top + 1) - b[n]) for n in names) / len(names), 2),
            "largest": sorted(mv, key=lambda x: (-abs((x[2] or 999) - x[1]), x[1]))[:10], "entered": entered, "left": left}
kr = lambda d: {n: v["rank"] for n, v in d.items()}
out = {"kit_rev": subprocess.run(["git", "-C", KIT, "rev-parse", "--short", REV], capture_output=True, text=True).stdout.strip(),
       "deck_rev": subprocess.run(["git", "-C", DECK, "rev-parse", "--short", DECK_REV], capture_output=True, text=True).stdout.strip(),
       "named": {n: {"kit_before": kb.get(n), "kit_after": ka.get(n), "deck_before": db.get(n), "deck_after": da.get(n)}
                 for n in ("Luke Kornet", "Coby White", "Dylan Cardwell")},
       "kit_top12": {"before": sorted(kr(kb), key=kr(kb).get)[:12], "after": sorted(kr(ka), key=kr(ka).get)[:12]},
       "kit_top200": summary(kr(kb), kr(ka), 200), "kit_top100": summary(kr(kb), kr(ka), 100),
       "deck_top156": summary(db, da, 156), "deck_top12": {"before": sorted(db, key=db.get)[:12], "after": sorted(da, key=da.get)[:12]}}
json.dump(out, open(os.path.join(H, "lock_board_diff_2026-10-14.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps(out["named"]), out["kit_top200"]["changed"], out["deck_top156"]["changed"], out["deck_top156"]["entered"], out["deck_top156"]["left"])
