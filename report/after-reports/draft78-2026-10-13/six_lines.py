#!/usr/bin/env python3
"""Owner question 2026-10-14: Jalen Williams, Pritchard, Anunoby, Holmgren, Davis and Towns were on the card at a heavy
clip before 10/12-10/13's projection work and are not now; what changed? For each deck version on main from the 10/12
morning pull (df1c754, before WO-5) to Version 65 (dd6b719): the six per-game lines as shipped in data/players.csv, and
the deck's own value math (hoops.zscores over that version's pool, total_value, adj_value) for rank and per-category z.
Also counts how many pool lines each version changed. Writes six_lines.json."""
import csv, io, json, os, subprocess, sys
DECK = "/home/user/yahoo-fantasy-basketball"
sys.path.insert(0, os.path.join(DECK, "scripts"))
import hoops
REVS = [("v58 10/12 pull (before WO-5)", "df1c754"), ("v59 ADP 10/12", "f918062"), ("v60 WO-5 re-derive", "8ec736b"),
        ("v62 minutes-and-games", "73e832c"), ("v63 pull 10/13", "3bd8311"), ("v64 Yahoo 10/13", "f6fb476"), ("v65 dial", "dd6b719")]
SIX = ["Jalen Williams", "Payton Pritchard", "OG Anunoby", "Chet Holmgren", "Anthony Davis", "Karl-Anthony Towns"]
COLS = ["fg_pct", "fga", "ft_pct", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]
out, prev = [], None
for label, rev in REVS:
    txt = subprocess.run(["git", "-C", DECK, "show", f"{rev}:data/players.csv"], capture_output=True, text=True, check=True).stdout
    tmp = f"/tmp/six_{rev}.csv"; open(tmp, "w").write(txt)
    hoops.DATA_PATH = tmp
    P = hoops.zscores(hoops.load_players())
    board = sorted([p for p in P if hoops.availability(p) > 0], key=lambda p: -hoops.adj_value(p))
    rank = {p["player"]: i + 1 for i, p in enumerate(board)}
    lines = {p["player"]: [p[c] for c in COLS] for p in P}
    changed = None if prev is None else sum(1 for k, v in lines.items() if k in prev and prev[k] != v)
    row = dict(label=label, rev=rev, lines_changed_vs_previous=changed, players={})
    for n in SIX:
        p = next(x for x in P if x["player"] == n)
        row["players"][n] = dict(line=dict(zip(COLS, lines[n])), adj_rank=rank.get(n), adj_value=round(hoops.adj_value(p), 3),
                                 availability=hoops.availability(p), z={k: round(v, 2) for k, v in p["z"].items()})
    out.append(row); prev = lines
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "six_lines.json"), "w"), indent=1)
for r in out:
    print(f"{r['label']:<30} {r['rev']} lines changed {r['lines_changed_vs_previous']}  " +
          "  ".join(f"{n.split()[-1]} #{v['adj_rank']} ({v['adj_value']})" for n, v in r["players"].items()))
