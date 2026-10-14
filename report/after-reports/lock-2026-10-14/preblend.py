#!/usr/bin/env python3
"""The lock re-blend's starting point: both planes with every Version 67 blended row returned to its pre-blend line (the
lines file's "old"), so the six-way mean is taken once, from our own line, never from an already-blended one.
Assertions (exit 1, nothing written):
  P1 on every row of the Version 67 lines file, the current kit and deck lines equal that file's "new" line, except the rows
     named in HELD, which equal its "old" line (Kornet: the owner's lock call restored it) — i.e. nothing else touched a
     blended line since the blend
  P2 only the eleven stat columns of listed rows change; every other cell and row is byte-identical
  preblend.py <lines_blend_2026-10-14.json> --deck <players.csv> --kit <projections.csv> --out-dir DIR"""
import argparse, csv, io, json, os, sys
sys.path.insert(0, "/home/user/fantasy-basketball-2026-27/report/blend/tools")
from common import STAT, KITCOL, canon, fmt  # noqa: E402
HELD = {"Luke Kornet": "owner lock call 10/14 (D-1014-6): pre-blend line restored on both planes"}

def read(p):
    raw = open(p, encoding="utf-8", newline="").read()
    return raw, raw.splitlines()[0].split(","), list(csv.DictReader(io.StringIO(raw)))

def write(rows, header, raw):
    buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=header, lineterminator="\r\n" if "\r\n" in raw else "\n")
    w.writeheader(); w.writerows(rows); return buf.getvalue()

ap = argparse.ArgumentParser(); ap.add_argument("lines"); ap.add_argument("--deck", required=True); ap.add_argument("--kit", required=True)
ap.add_argument("--out-dir", required=True); a = ap.parse_args()
L = {r["key"]: r for r in json.load(open(a.lines, encoding="utf-8"))["rows"]}
fails, n = [], {"kit": 0, "deck": 0}
out = {}
for plane, path, namecol in (("kit", a.kit, "name"), ("deck", a.deck, "player")):
    raw, head, rows = read(path)
    rows0 = [dict(r) for r in rows]
    for r in rows:
        x = L.get(canon(r[namecol]))
        if not x: continue
        col = (lambda c: KITCOL.get(c, c)) if plane == "kit" else (lambda c: c)
        want = x["old"] if r[namecol] in HELD else x["new"]
        for c in STAT:
            if abs(float(r[col(c)]) - want[c]) > 1e-9:
                fails.append(f"P1 {plane} {r[namecol]} {c}: plane {r[col(c)]} vs lines file {'old' if r[namecol] in HELD else 'new'} {want[c]}")
        for c in STAT: r[col(c)] = fmt(c, x["old"][c])
        n[plane] += 1
    for r, r0 in zip(rows, rows0):
        diff = {k for k in r if r[k] != r0[k]}
        if diff - {KITCOL.get(c, c) if plane == "kit" else c for c in STAT}: fails.append(f"P2 {plane} {r[namecol]} {sorted(diff)}")
    out[plane] = write(rows, head, raw)
    if plane == "kit" and write(rows0, head, raw) != raw: fails.append("P2 kit: the writer does not round-trip the file")
    if plane == "deck" and write(rows0, head, raw) != raw: fails.append("P2 deck: the writer does not round-trip the file")
if fails:
    print("PREBLEND: FAIL"); [print("  " + f) for f in fails[:30]]; sys.exit(1)
os.makedirs(a.out_dir, exist_ok=True)
open(os.path.join(a.out_dir, "projections-2026-27.csv"), "w", encoding="utf-8", newline="").write(out["kit"])
open(os.path.join(a.out_dir, "players.csv"), "w", encoding="utf-8", newline="").write(out["deck"])
print(f"PREBLEND: PASS — {len(L)} blended rows; kit {n['kit']} and deck {n['deck']} rows returned to the pre-blend line; "
      f"held rows matched their restored line: {', '.join(HELD)}")
