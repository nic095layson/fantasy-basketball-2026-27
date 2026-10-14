#!/usr/bin/env python3
"""Test 7 for the six-way blend (2026-10-14; the dial pass's test 7, same method): the card's 🎯 at the owner's 13 picks in each of the 25 graded mocks, replayed by the
deck's own repeat-name check on Version 66 (arena/results/repeat_market_check_2026-10-14_v66.json) and on the blended page
(…_v67.json). The two records come from the same script on the same 25 mocks; the only input that differs is the page."""
import json, os, sys
from collections import Counter
D = os.environ.get("DECK_REPO", "/home/user/yahoo-fantasy-basketball")
a = json.load(open(os.path.join(D, "arena/results/repeat_market_check_2026-10-14_v66.json"), encoding="utf-8"))
b = json.load(open(os.path.join(D, "arena/results/repeat_market_check_2026-10-14_v67.json"), encoding="utf-8"))
L = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", "lines_blend_2026-10-14.json"), encoding="utf-8"))["rows"]
blended = {r["name"] for r in L}
print(f"pages: v66 {a['page_sha256'][:12]} ({a['replayed']} of {a['mocks'] if isinstance(a['mocks'], int) else len(a['mocks'])} mocks) / v67 {b['page_sha256'][:12]} ({b['replayed']} replayed)")
assert set(a["targets"]) == set(b["targets"]), "different mocks"
turns = changed = 0; rows = []; by_round = Counter(); tot_round = Counter()
for m in sorted(a["targets"], key=int):
    ta = dict((p, n) for p, n in a["targets"][m]); tb = dict((p, n) for p, n in b["targets"][m])
    assert ta.keys() == tb.keys(), f"mock {m}: different turns"
    for rd, p in enumerate(sorted(ta, key=int), 1):
        turns += 1; tot_round[rd] += 1
        if ta[p] != tb[p]:
            changed += 1; by_round[rd] += 1; rows.append((m, rd, p, ta[p], tb[p]))
print(f"turns compared: {turns}; 🎯 changed: {changed}")
print("by round (changed / turns): " + ", ".join(f"R{r} {by_round[r]}/{tot_round[r]}" for r in sorted(tot_round)))
out_v66 = Counter(x[3] for x in rows); in_v67 = Counter(x[4] for x in rows)
print("left the 🎯 most often (v66 name): " + ", ".join(f"{n} {c}" + (" *" if n in blended else "") for n, c in out_v66.most_common(10)))
print("took the 🎯 most often (v67 name): " + ", ".join(f"{n} {c}" + (" *" if n in blended else "") for n, c in in_v67.most_common(10)))
ca = Counter(n for m in a["targets"] for p, n in a["targets"][m]); cb = Counter(n for m in b["targets"] for p, n in b["targets"][m])
print("🎯 counts across all turns, the 15 names with the largest change (v66 to v67): " + ", ".join(f"{n} {ca[n]} to {cb[n]}" for n in sorted(set(ca) | set(cb), key=lambda n: -abs(cb[n] - ca[n]))[:15]))
print("(* = one of the 241 blended lines)")
print("\nmock | round | pick | v66 🎯 | v67 🎯")
for m, rd, p, x, y in rows: print(f"{m} | {rd} | {p} | {x} | {y}")
