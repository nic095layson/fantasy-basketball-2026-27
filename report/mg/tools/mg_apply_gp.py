#!/usr/bin/env python3
"""MG-2: write the games moves to the kit's projections CSV, with assertions (any failure writes nothing):
  G1 header, row count and order unchanged; G2 only the gp cell of a listed row changes; G3 every listed row found once
  and its old gp matches the list; G4 a second run changes nothing. Usage: mg_apply_gp.py <gp_moves.csv> <projections.csv>"""
import csv, io, sys
MOVES, KIT = sys.argv[1:3]
moves = {r["player"]: r for r in csv.DictReader(open(MOVES, encoding="utf-8"))}
raw = open(KIT, encoding="utf-8").read(); rows = list(csv.DictReader(io.StringIO(raw))); head = rows[0].keys()
seen = set(); changed = 0
for r in rows:
    m = moves.get(r["name"])
    if not m: continue
    assert r["name"] not in seen, f"G3 duplicate {r['name']}"; seen.add(r["name"])
    old = int(float(r["gp"]))
    if old == int(m["gp_new"]): continue            # G4: already applied
    assert old == int(m["gp_old"]), f"G3 {r['name']}: kit gp {old} != list gp_old {m['gp_old']}"
    r["gp"] = m["gp_new"]; changed += 1
assert seen == set(moves), f"G3 missing rows: {sorted(set(moves) - seen)}"
buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=list(head), lineterminator="\n"); w.writeheader(); w.writerows(rows); out = buf.getvalue()
a, b = raw.splitlines(), out.splitlines(); assert len(a) == len(b) and a[0] == b[0], "G1"
for x, y in zip(a, b):
    if x != y:
        xa, ya = next(csv.reader([x])), next(csv.reader([y])); diff = [i for i in range(len(xa)) if xa[i] != ya[i]]
        assert diff == [list(head).index("gp")] and xa[0] in moves, f"G2 unexpected change in {xa[0]}: cols {diff}"
open(KIT, "w", encoding="utf-8").write(out)
print(f"MG-2 APPLY: PASS — {changed} gp cell(s) changed of {len(moves)} listed; file {'changed' if out != raw else 'unchanged'}")
