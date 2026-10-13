#!/usr/bin/env python3
"""Dial pass 2026-10-13 (D-1013-6), deck page edits before the build: the colophon Data paragraph narrates this refresh
(gate 6 wants "This refresh (10/13"), the two sentences of the morning's account that the clamp makes untrue are
re-worded, and the seven judgment cards whose lines moved get a dated receipt read from the lines file (the MG pass's
precedent, deck_page_mg.py). Exact anchors; all-or-nothing; idempotent."""
import json, os, sys
P = os.environ.get("DECK_PAGE", "/home/user/yahoo-fantasy-basketball/docs/draft-deck.html")
LINES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", "lines_dial_2026-10-13.json")
s = open(P, encoding="utf-8").read(); orig = s
if "This refresh (10/13 evening, the range clamp" in s: print("already applied"); sys.exit(0)
L = {r["name"]: r for r in json.load(open(LINES, encoding="utf-8"))["rows"]}
LABEL = {"pts": "points", "reb": "rebounds", "ast": "assists", "stl": "steals", "blk": "blocks", "tpm": "3PM", "tov": "turnovers", "fg_pct": "FG%", "ft_pct": "FT%"}
fmt = lambda c, v: f"{v:.3f}".lstrip("0") if c.endswith("pct") else f"{v:g}"
high = [n for n, r in L.items() if r["net_z"] is not None and r["net_z"] > 0]
low = [n for n, r in L.items() if r["net_z"] is not None and r["net_z"] < 0]
disp = lambda n: "Kristaps Porziņģis" if n == "Kristaps Porzingis" else n
def sub(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:80]); s = s.replace(old, new)
OLD_HEAD = "This refresh (10/13, the daily pull on top of the morning’s minutes-and-games pass) read"
NEW_HEAD = ("This refresh (10/13 evening, the range clamp the Council recommended 4–1 and the owner approved, D-1013-6) moved "
            f"{len(L)} lines into the range of the three outside projections on file, Yahoo 10/13, Hashtag 10/12 and RotoBaller 9/29, "
            "category by category to the nearest edge: the lines whose cells outside that range carried more than half a z point "
            f"beyond it, {len(high)} high ({', '.join(disp(n) for n in high)}) and {len(low)} low ({', '.join(disp(n) for n in low)}), "
            "plus Philadelphia’s LeBron James, Joel Embiid and VJ Edgecombe for the team budget; shot attempts rescaled so each "
            "line’s points still follow from its shooting; games, minutes, tags and placements unchanged; written to both planes by "
            "one asserted script, every value checked inside the three projections’ range. The smaller disagreements, each under half "
            "a z point, stand. Earlier the same day the daily pull, on top of the morning’s minutes-and-games pass, read")
sub(OLD_HEAD, NEW_HEAD)
sub("No line or placement changed; the minutes-and-games pass", "That pull changed no line or placement; the minutes-and-games pass")
sub("The lines did not move with it: the pool is Version 63’s.", "The lines did not move with that paste; they moved only in this evening’s range clamp, above.")
CARDS = ["Kawhi Leonard", "James Harden", "Tyrese Maxey", "Ryan Rollins", "Zach LaVine", "Joel Embiid", "VJ Edgecombe"]
for name in CARDS:
    r = L[name]
    moved = ", ".join(f"{LABEL[c['cat']]} {fmt(c['cat'], c['before'])} to {fmt(c['cat'], c['after'])}" for c in r["cells"])
    add = (f" 10/13 (range clamp, D-1013-6): {moved}; now inside Yahoo 10/13, Hashtag 10/12 and RotoBaller 9/29. "
           "The card’s adjustment stays: it is a tooltip flag, not a rank input.")
    assert '"' not in add and "\\" not in add and "];" not in add
    key = f'    "{name}": {{ adj: '; i = s.find(key); assert i >= 0 and s.count(key) == 1, name
    j = s.find('" },', i); assert j > i and "range clamp" not in s[i:j], name
    s = s[:j] + add + s[j:]
assert s != orig
open(P, "w", encoding="utf-8").write(s)
print(f"page edited: colophon head ({len(L)} lines, {len(high)} high, {len(low)} low), two sentences re-worded, {len(CARDS)} card receipts")
