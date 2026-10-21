#!/usr/bin/env python3
"""Does one in-season addition move anyone else's z-scores? The deck engine (hoops.zscores) seeds over the full pool,
then standardizes over its top-156 by total value. This runs it on the frozen v69 snapshot alone and on the snapshot
followed by the kit's data/pool_additions.csv (what season_lines writes on a no-games day), and records the largest
change in any snapshot player's z per category, whether the top-156 set changed, and the additions' own rank.
Writes zscore_effect.json beside itself."""
import csv, importlib, json, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DECK = os.path.join(KIT, "..", "yahoo-fantasy-basketball")
sys.path.insert(0, os.path.join(DECK, "scripts"))
import hoops  # noqa: E402
SNAP = os.path.join(DECK, "arena", "results", "players_v69.csv")
ADDS = os.path.join(KIT, "data", "pool_additions.csv")


def board(path):
    hoops.DATA_PATH = path
    ps = hoops.zscores(hoops.load_players())
    avail = [p for p in ps if hoops.availability(p) > 0]
    order = sorted(avail, key=lambda p: -hoops.total_value(p))
    return {p["player"]: p for p in ps}, [p["player"] for p in order]


with tempfile.TemporaryDirectory() as d:
    both = os.path.join(d, "both.csv")
    rows = list(csv.reader(open(SNAP, encoding="utf-8"))) + list(csv.reader(open(ADDS, encoding="utf-8")))[1:]
    with open(both, "w", newline="", encoding="utf-8") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)
    a, ra = board(SNAP)
    b, rb = board(both)
added = [n for n in b if n not in a]
cats = list(next(iter(a.values()))["z"])
maxd = {c: max(abs(a[n]["z"][c] - b[n]["z"][c]) for n in a) for c in cats}
rec = dict(snapshot=os.path.relpath(SNAP, KIT), additions=os.path.relpath(ADDS, KIT),
           deck_commit=os.popen(f"git -C {DECK} rev-parse --short HEAD").read().strip(),
           snapshot_rows=len(a), with_additions_rows=len(b), added=added,
           added_rank={n: rb.index(n) + 1 if n in rb else None for n in added},
           added_total_value={n: round(hoops.total_value(b[n]), 3) for n in added},
           top156_same=set(ra[:hoops.DRAFTABLE]) == set(rb[:hoops.DRAFTABLE]),
           max_abs_z_change_other_players=maxd,
           rank_order_same_for_snapshot_players=[n for n in rb if n in a] == ra)
json.dump(rec, open(os.path.join(HERE, "zscore_effect.json"), "w"), indent=1); print(json.dumps(rec, indent=1))
