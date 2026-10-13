#!/usr/bin/env python3
"""Dial pass 2026-10-13: the kit board before (top-200-2026-27.md at 7c28bb3, the pass's base) and after (the working tree), rank by rank,
for the 24 clamped players and for everyone else."""
import json, os, re, subprocess, sys
KIT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
REV = sys.argv[1] if len(sys.argv) > 1 else "7c28bb3"  # the kit main the pass started from
def board(text):
    out = {}
    for ln in text.splitlines():
        m = re.match(r"^\| (\d+) \| ([^|]+?) \| ([A-Z]{2,3}) \|", ln)
        if m: out[m.group(2)] = int(m.group(1))
    return out
before = board(subprocess.run(["git", "-C", KIT, "show", f"{REV}:report/top-200-2026-27.md"], capture_output=True, text=True, check=True).stdout)
after = board(open(os.path.join(KIT, "report/top-200-2026-27.md"), encoding="utf-8").read())
L = json.load(open(os.path.join(KIT, "report/dial/out/lines_dial_2026-10-13.json"), encoding="utf-8"))["rows"]
names = {r["name"] for r in L}
print(f"kit board: {len(before)} rows before ({REV}), {len(after)} after")
print("player | side | kit rank before | kit rank after | move")
for r in sorted(L, key=lambda r: before.get(r["name"], 999)):
    b, a = before.get(r["name"]), after.get(r["name"])
    side = "PHI budget" if r["net_z"] is None else ("high" if r["net_z"] > 0 else "low")
    mv = "-" if b is None or a is None else f"{b - a:+d}"
    print(f"{r['name']} | {side} | {b if b else 'off'} | {a if a else 'off'} | {mv}")
others = [(n, before[n], after.get(n)) for n in before if n not in names]
moved = [(n, b, a) for n, b, a in others if a is not None and a != b]
gone = [n for n, b, a in others if a is None]
new = [n for n in after if n not in before]
print(f"others: {len(moved)} of {len(others)} change rank; largest moves: " + ", ".join(f"{n} {b} to {a}" for n, b, a in sorted(moved, key=lambda x: -abs(x[1] - x[2]))[:6]))
print(f"left the top 200: {gone}; entered: {new}")
