#!/usr/bin/env python3
"""The owner's logged turns (the history in owner_message.txt) against each page's replayed card (card_<v>.json)."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
msg = open(os.path.join(H, "owner_message.txt"), encoding="utf-8").read().split("\n")
echo = {}
for i, l in enumerate(msg[:163]):
    m = re.search(r"#(\d+): (.+?) → Seat 10 \(YOU\)", l)
    if not m: continue
    n = int(m.group(1))
    tail = l + " " + (msg[i + 1] if i + 1 < len(msg) and msg[i + 1].startswith("⚠ off the card") else "")
    e = re.search(r"off the card: (.+?) ranks #(\d+) \(([\d.]+) behind 🎯 (.+?)\)", tail)
    echo[n] = (m.group(2), int(e.group(2)), e.group(3), e.group(4)) if e else (m.group(2), None, None, None)
print("owner turns logged:", sorted(echo), "echo lines:", sum(1 for v in echo.values() if v[1]))
for ver in ["v63", "v62", "v59", "v58", "v64"]:
    res = json.load(open(os.path.join(H, f"card_{ver}.json")))
    agree = 0; rows = []
    for t in res:
        n = t["pick"]
        if n not in echo: rows.append(f"  #{n} {t['actual']}: no live line (board wiped) — replay 🎯 {t['targetName']}, {t['actual']} ranks #{t['actualCardRank']} gap {t['echoGap']}"); continue
        name, r, gap, tgt = echo[n]
        if r is None:
            ok = t["targetName"] == t["actual"]
            rows.append(f"  #{n} {name}: live = took the 🎯 · replay 🎯 {t['targetName']} {'MATCH' if ok else 'DIFFERS'}")
        else:
            ok = (t["actualCardRank"] == r and t["echoGap"] == gap and t["targetName"] == tgt)
            rows.append(f"  #{n} {name}: live #{r} {gap} behind {tgt} · replay #{t['actualCardRank']} {t['echoGap']} behind {t['targetName']} {'MATCH' if ok else 'DIFFERS'}")
        agree += ok
    print(f"{ver}: {agree} of {len(echo)} logged owner turns reproduced")
    for r_ in rows: print(r_)
