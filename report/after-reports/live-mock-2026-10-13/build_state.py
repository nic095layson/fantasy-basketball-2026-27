#!/usr/bin/env python3
"""The room as the deck's state format: Yahoo's recap names, resolved to the pool's spellings by the page itself
(the Chromium RESYNC of the recap as a semicolon list, step G of repro_v63.json), seats by the snake."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
recap = json.load(open(os.path.join(H, "recap.json")))
g = [s for s in json.load(open(os.path.join(H, "repro_v63.json")))["steps"] if s["step"].startswith("G ")][0]
assert g["picks"] == 156 and len(g["mismatches"]) < 40          # the list is capped at 40, so it is complete
sub = {n: page for n, rec, page in g["mismatches"]}
slot_of = lambda n0: (n0 % 12) + 1 if (n0 // 12) % 2 == 0 else 12 - (n0 % 12)
picks = [{"player": sub.get(p["n"], p["name"]), "slot": slot_of(p["n"] - 1)} for p in recap]
assert [i + 1 for i, pk in enumerate(picks) if pk["slot"] == 10] == g["ownerSlot"]
json.dump({"teams": 12, "slot": 10, "size": 13, "punt": [], "picks": picks}, open(os.path.join(H, "draft_state_m76.json"), "w"), ensure_ascii=False, indent=0)
print("state picks", len(picks), "substitutions", sub)
