#!/usr/bin/env python3
"""From the owner's 2026-10-13 message (owner_message.txt): the RESYNC paste as the page's history stood
(lines 'Draft started:' .. 'RESYNC refused: ...'), the page's seven UNKNOWN lines, and Yahoo's round-by-round
recap as 156 picks (recap.json). Line numbers are asserted, not assumed."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
L = open(os.path.join(H, "owner_message.txt"), encoding="utf-8").read().split("\n")
line = lambda i: L[i - 1]
assert line(6).startswith("Draft started:"), line(6)
assert line(162).startswith("RESYNC refused: paste is empty"), line(162)
assert line(163).startswith("RESYNC: cleared 141 pick(s); rebuilt 7"), line(163)
assert line(171).startswith("— resumed: 7 picks logged"), line(171)
paste_lines = L[5:162]
json.dump(paste_lines, open(os.path.join(H, "owner_paste_lines.json"), "w"), ensure_ascii=False)
echo = L[163:170]
assert all(e.startswith("⚠ (R1) #") for e in echo), echo
json.dump(echo, open(os.path.join(H, "owner_unknown_echo.json"), "w"), ensure_ascii=False)
paste = " ".join(paste_lines)
print("paste semicolons", paste.count(";"), "segments", len([s for s in paste.split(";") if s.strip()]))
picks = []; rnd = None
i = L.index("Round by Round results")
for s in L[i + 1:]:
    m = re.fullmatch(r"Round (\d+)", s.strip())
    if m: rnd = int(m.group(1)); continue
    m = re.fullmatch(r"\((\d+)\) (.+?) - (.+?), (.+?) \(([A-Z]{2,4}) - ([A-Z,]+)\)", s.strip())
    if m:
        k = int(m.group(1)); last, first = m.group(3), m.group(4)
        picks.append(dict(n=(rnd - 1) * 12 + k, round=rnd, k=k, manager=m.group(2), name=f"{first} {last}", team=m.group(5), pos=m.group(6)))
    elif s.strip(): raise SystemExit("UNPARSED: " + s)
picks.sort(key=lambda p: p["n"])
assert [p["n"] for p in picks] == list(range(1, 157)), len(picks)
json.dump(picks, open(os.path.join(H, "recap.json"), "w"), ensure_ascii=False, indent=0)
seat = {}
for p in picks:
    r, pos = divmod(p["n"] - 1, 12); seat.setdefault(p["manager"], set()).add(pos + 1 if r % 2 == 0 else 12 - pos)
assert all(len(v) == 1 for v in seat.values()), seat
print("recap picks", len(picks), "· every manager in one seat (snake)", sorted((min(v), m) for m, v in seat.items())[9])
