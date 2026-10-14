#!/usr/bin/env python3
"""Kit board before (Version 68) and after the lock, from the two top-200 files the engine wrote. Writes
board_diff_lock_2026-10-14.json beside this script: moves inside the final 180, entries and exits.
  board_diff.py <before top-200.md> <after top-200.md>"""
import json, os, re, sys
def board(p):
    out = {}
    for l in open(p, encoding="utf-8"):
        m = re.match(r"^\| (\d+) \| ([^|]+?) \| (\w+) \|", l)
        if m: out[m.group(2)] = int(m.group(1))
    return out
a, b = board(sys.argv[1]), board(sys.argv[2])
top = 180
moves = sorted([(n, a.get(n), r) for n, r in b.items() if r <= top and a.get(n) != r], key=lambda x: -abs((x[1] or 999) - x[2]))
out = dict(before=len(a), after=len(b), moved_in_180=len(moves), moves=moves,
           entered_180=[(n, a.get(n), r) for n, r in b.items() if r <= top and (a.get(n) or 999) > top],
           left_180=[(n, r, b.get(n)) for n, r in a.items() if r <= top and (b.get(n) or 999) > top])
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "board_diff_lock_2026-10-14.json"), "w"), indent=1, ensure_ascii=False)
print(f"moved inside the 180: {len(moves)}; entered {out['entered_180']}; left {out['left_180']}")
for n, x, y in moves[:20]: print(f"  {n}: {x} -> {y}")
