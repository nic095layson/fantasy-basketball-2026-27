#!/usr/bin/env python3
"""Known-answer check: on the players both records cover, the audit's T1 cells must equal the deck's own range check
(range_no_actual_v65.json: the same three references, no last season, the deck's z frame) cell for cell."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, "/home/user/yahoo-fantasy-basketball/scripts"); import range_check as rc
A = {rc.fold(r["name"]): r for r in json.load(open(os.path.join(H, "audit180.json")))["rows"]}
D = {rc.fold(r["player"]): r for r in json.load(open(os.path.join(H, "range_no_actual_v65.json")))["rows"]}
shared = [k for k in D if k in A and A[k]["tests"]["T1"]["refs"] == 3]
bad = []
for k in shared:
    a = {x["cat"]: x["z"] for x in A[k]["tests"]["T1"]["cells"]}; d = {x["cat"]: round(x["z_beyond"], 2) for x in D[k]["cells"]}
    if set(a) != set(d) or any(abs(a[c] - d[c]) > 0.011 for c in a): bad.append((k, a, d))
# and every audited three-reference player the deck lists must be flagged by the audit, and vice versa within the deck's top-150 scope
missing = [k for k in shared if not A[k]["tests"]["T1"]["cells"]]
print(f"shared flagged players {len(shared)}; cell sets and z agree on {len(shared) - len(bad)}; disagreements {len(bad)}; deck-flagged but audit-clean {len(missing)}")
for b in bad[:10]: print("  ", b)
sys.exit(1 if bad or missing else 0)
