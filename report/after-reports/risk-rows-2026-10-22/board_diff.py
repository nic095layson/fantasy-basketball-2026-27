#!/usr/bin/env python3
"""Preseason kit board before/after the six GP changes (owner 2026-10-22): report/top-200-2026-27.md at origin/main
(before) vs the working tree (after), every player whose rank, GP or zAdj changed. Writes board_diff.json beside
itself and prints one line per mover.

    python3 report/after-reports/risk-rows-2026-10-22/board_diff.py [--base REF]"""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
MD = "report/top-200-2026-27.md"


def parse(text):
    out = {}
    for line in text.splitlines():
        m = re.match(r"^\| (\d+) \| ([^|]+?) \| [^|]* \| [^|]* \| (\d+) \|(?:[^|]*\|){3} ([+−-][\d.]+) \|", line)
        if m:
            out[m.group(2)] = dict(rank=int(m.group(1)), gp=int(m.group(3)), zadj=float(m.group(4).replace("−", "-")))
    return out


def main():
    base = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "origin/main"
    before = parse(subprocess.run(["git", "-C", KIT, "show", f"{base}:{MD}"], capture_output=True, text=True, check=True).stdout)
    after = parse(open(os.path.join(KIT, MD), encoding="utf-8").read())
    assert len(before) == 200 and len(after) == 200, (len(before), len(after))
    rows = []
    for n in sorted(set(before) | set(after), key=lambda n: after.get(n, before.get(n))["rank"]):
        b, a = before.get(n), after.get(n)
        if b != a:
            rows.append(dict(player=n, before=b, after=a))
    rec = dict(base=base, base_commit=subprocess.run(["git", "-C", KIT, "rev-parse", base], capture_output=True, text=True).stdout.strip(),
               board_rows=200, changed=len(rows), rows=rows)
    json.dump(rec, open(os.path.join(HERE, "board_diff.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for r in rows:
        b, a = r["before"] or {}, r["after"] or {}
        print(f"{r['player']}: rank {b.get('rank')} -> {a.get('rank')}, GP {b.get('gp')} -> {a.get('gp')}, zAdj {b.get('zadj')} -> {a.get('zadj')}")
    print(f"BOARD DIFF: {len(rows)} of 200 rows changed")


if __name__ == "__main__":
    main()
