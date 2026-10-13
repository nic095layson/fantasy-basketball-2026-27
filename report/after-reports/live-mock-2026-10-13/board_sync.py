#!/usr/bin/env python3
"""Was the board right before the wipe? The page's history (picks 1-141, with inserts and the #141 fix) against Yahoo's recap."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
msg = open(os.path.join(H, "owner_message.txt"), encoding="utf-8").read().split("\n")[:162]
state = json.load(open(os.path.join(H, "draft_state_m76.json")))
logged = {}
for l in msg:
    m = re.match(r"\s*✓ \(R\d+\) #(\d+): (.+?) → Seat (\d+)", l)
    if m: logged[int(m.group(1))] = (m.group(2), int(m.group(3)))
    m = re.match(r"\s*✎ inserted (.+?) at #(\d+) → Seat (\d+)", l)
    if m: logged[int(m.group(2))] = (m.group(1), int(m.group(3)))
    m = re.match(r"\s*✎ #(\d+) corrected: UNKNOWN #\d+ → (.+)$", l)
    if m: logged[int(m.group(1))] = (m.group(2).strip(), None)
print("history entries for picks 1-141:", len([n for n in logged if n <= 141]), "missing:", [n for n in range(1, 142) if n not in logged])
bad = [(n, logged[n][0], state["picks"][n-1]["player"]) for n in range(1, 142) if n in logged and logged[n][0] != state["picks"][n-1]["player"]]
seat = [(n, logged[n][1], state["picks"][n-1]["slot"]) for n in range(1, 142) if n in logged and logged[n][1] is not None and logged[n][1] != state["picks"][n-1]["slot"]]
print("name differences vs Yahoo's recap:", bad)
print("seat differences vs snake order:", seat)
