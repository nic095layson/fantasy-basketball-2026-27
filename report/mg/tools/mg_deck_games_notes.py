#!/usr/bin/env python3
"""MG-2 on the deck plane: the deck has no games column (its availability is tag-based, and tags come from injury news),
so each kit games move is recorded on the player's deck row as a dated note entry — the plane's evidence trail — with
no stat, tag or placement change. The entry is inserted BEFORE the row's WO-5 entry so wo5_apply.py re-runs (which
replace the WO-5 entry) leave it intact; a second run of this script changes nothing.
Usage: mg_deck_games_notes.py <gp_moves.csv> <deck players.csv> <candidates.json>"""
import csv, io, json, sys
MOVES, DECK, CAND = sys.argv[1:4]
moves = {r["player"]: r for r in csv.DictReader(open(MOVES, encoding="utf-8"))}
C = {c["player"]: c for c in json.load(open(CAND, encoding="utf-8"))["candidates"]}
raw = open(DECK, encoding="utf-8").read(); rows = list(csv.DictReader(io.StringIO(raw))); head = list(rows[0].keys())
seen = set(); changed = 0; MARK = ": WO-5 line — "
for r in rows:
    m = moves.get(r["player"])
    if not m: continue
    seen.add(r["player"]); note = r["note"]
    if "MG-2 games" in note: continue
    c = C[r["player"]]
    entry = (f"10/13: MG-2 games {m['gp_old']} -> {m['gp_new']} on the kit plane (Yahoo 10/06 {int(c['yahoo_gp'])} GP and Hashtag 10/12 "
             f"{int(c['hashtag_gp'])} GP both on the same side by 5+; the mean); this plane's availability is tag-based and tags come from injury news — no tag change")
    assert "]" not in entry
    i = note.find(MARK)
    if i >= 0:
        j = note.rfind("; ", 0, i); j = j if j >= 0 else note.rfind(". ", 0, i)   # the separator before the WO-5 entry's date
        k = j + 2 if j >= 0 else 0
        r["note"] = note[:k] + entry + "; " + note[k:]
    else:
        sep = ". " if note.rstrip().endswith("]") else "; "
        r["note"] = (note + sep if note else "") + entry
    assert "];" not in r["note"]; changed += 1
assert seen == set(moves), sorted(set(moves) - seen)
buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=head, lineterminator="\n"); w.writeheader(); w.writerows(rows); out = buf.getvalue()
a, b = raw.splitlines(), out.splitlines(); assert len(a) == len(b) and a[0] == b[0]
for x, y in zip(a, b):
    if x != y:
        xa, ya = next(csv.reader([x])), next(csv.reader([y])); d = [i for i in range(len(xa)) if xa[i] != ya[i]]
        assert d == [head.index("note")] and xa[0] in moves, (xa[0], d)
open(DECK, "w", encoding="utf-8").write(out)
print(f"MG-2 DECK NOTES: PASS — {changed} note(s) added of {len(moves)} listed; file {'changed' if out != raw else 'unchanged'}")
