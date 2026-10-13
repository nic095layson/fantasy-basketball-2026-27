#!/usr/bin/env python3
"""League-wide per-36 rates by season from the WO-5 Basketball-Reference totals (season rows only) — the era check the
20-season window skipped. Usage: league_per36.py <bref_totals.csv> <out.json>"""
import csv, json, sys
from collections import defaultdict
by = defaultdict(lambda: defaultdict(float))
for r in csv.DictReader(open(sys.argv[1], encoding="utf-8")):
    if r.get("row", "season") == "split": continue
    for k in ("mp", "fga", "fg3", "fta", "tov", "pts"): by[r["season"]][k] += float(r[k])
out = {s: {"3pm_36": round(c["fg3"] / c["mp"] * 36, 2), "fga_36": round(c["fga"] / c["mp"] * 36, 2), "fta_36": round(c["fta"] / c["mp"] * 36, 2),
           "pts_36": round(c["pts"] / c["mp"] * 36, 2), "usage_36": round((c["fga"] + 0.44 * c["fta"] + c["tov"]) / c["mp"] * 36, 2)} for s, c in sorted(by.items())}
json.dump(out, open(sys.argv[2], "w"), indent=1)
for s, v in out.items(): print(s, v)
