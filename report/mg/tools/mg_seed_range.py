#!/usr/bin/env python3
"""Seed range file for the MG pass. The 10/12 range resolution is the committed starting point (the iteration is
path-dependent: its rookie identity entries came from a separate 10/12 step and are not re-derived from scratch).
An MG-1 mover whose committed entry carries R1 minutes has that entry's minutes/factor released, so the override can
apply; the range rule re-runs on the result and wins if it fires again (the standing D-RN-3 rule).
Usage: mg_seed_range.py <committed range.json> <candidates.json> <out seed.json>"""
import json, re, sys, unicodedata
R, C, OUT = sys.argv[1:4]
norm = lambda s: " ".join(t for t in re.sub(r"[^a-z0-9 ]", " ", re.sub(r"[.'`,’-]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower())).split() if t not in {"jr", "sr", "ii", "iii", "iv"})
rng = json.load(open(R, encoding="utf-8")); cands = json.load(open(C, encoding="utf-8"))["candidates"]
released = []
for c in cands:
    if c.get("mg1") != "MOVE": continue
    e = rng.get(norm(c["player"]))
    if e and (e.get("minutes") is not None or e.get("factor", 1.0) != 1.0):
        released.append(dict(player=c["player"], r1_minutes=e.get("minutes"), factor=e.get("factor"), mechanism=(e.get("mechanisms") or {}).get("minutes")))
        e.pop("minutes", None); e.pop("factor", None); (e.get("mechanisms") or {}).pop("minutes", None)
        e["mg_note"] = "R1 minutes released for the MG-1 override (2026-10-13); the range rule re-runs on the result"
json.dump(rng, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(json.dumps(dict(entries=len(rng), released=released), indent=1))
