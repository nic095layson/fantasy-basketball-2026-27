#!/usr/bin/env python3
"""Owner question 2026-10-14, the card half: the same 27 graded draft states (mocks 51-78 with a state on file) replayed
through five page versions with each page's own engine (arena/mocks/live_deckcard.py, rev:<sha>:docs/draft-deck.html) —
v59 (f918062, the last page before the 10/12 re-derive), v60 (8ec736b, WO-5), v62 (73e832c, minutes and games),
v64 (f6fb476), v65 (dd6b719, the dial). Holding the rooms fixed isolates what the page itself changed. For each of the six
players: owner turns where he was the 🎯, turns where he was in the Top 5, and the turns he was still available (on any
card row or in the pool). Inputs: the 135 per-run JSONs (argv[1], committed in the deck at arena/results/six_cards_2026-10-14/); writes six_cards.json."""
import json, os, sys, glob, collections
SRC = sys.argv[1]
REVS = [("v59", "f918062"), ("v60 WO-5", "8ec736b"), ("v62 MG", "73e832c"), ("v64", "f6fb476"), ("v65", "dd6b719")]
SIX = ["Jalen Williams", "Payton Pritchard", "OG Anunoby", "Chet Holmgren", "Anthony Davis", "Karl-Anthony Towns"]
MOCKS = sorted({int(os.path.basename(f).split("_")[0][1:]) for f in glob.glob(os.path.join(SRC, "m*_*.json"))})
out = {"mocks": MOCKS, "versions": {}}
for label, rev in REVS:
    tgt = collections.Counter(); top5 = collections.Counter(); by_pick = collections.Counter(); turns = 0
    for m in MOCKS:
        T = json.load(open(os.path.join(SRC, f"m{m}_{rev}.json")))
        for t in T:
            turns += 1
            names = [r["n"] for r in t["rows"]]
            t5 = names[:5]
            tg = [r["n"] for r in t["rows"] if r.get("target")]
            for n in SIX:
                if n in t5: top5[n] += 1
                if n in tg: tgt[n] += 1; by_pick[f"{n} #{t['pick']}"] += 1
    out["versions"][label] = dict(rev=rev, owner_turns=turns, target={n: tgt[n] for n in SIX}, top5={n: top5[n] for n in SIX},
                                  six_target_total=sum(tgt.values()), six_top5_total=sum(top5.values()),
                                  target_by_pick=dict(sorted(by_pick.items())))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "six_cards.json"), "w"), indent=1)
print("mocks", len(MOCKS), MOCKS)
print(f"{'version':<10} {'turns':>5}  " + "  ".join(f"{n.split()[-1][:9]:>9} 🎯/T5" for n in SIX) + "   all six 🎯/T5")
for label, v in out["versions"].items():
    print(f"{label:<10} {v['owner_turns']:>5}  " + "  ".join(f"{v['target'][n]:>6}/{v['top5'][n]:<4}" for n in SIX) + f"   {v['six_target_total']}/{v['six_top5_total']}")
