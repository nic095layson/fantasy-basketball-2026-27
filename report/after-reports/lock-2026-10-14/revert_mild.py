#!/usr/bin/env python3
"""Owner call 2026-10-14 (lock): "for Kawhi and Anthony Davis, revert their health multiplier to 0.78". Version 66 moved
both from `inj-risk` to `inj-risk-mild` (0.85) as a deck tag only — the kit's games were not touched — so the revert is the
deck tag alone: the leading token back to `inj-risk`, with a dated reason inside the tag's parenthesis (hoops.note_tag
reads the token before the first space or "("). Asserts: exactly the two rows change, only their note, the new leading
tag is `inj-risk` and hoops.availability gives 0.78. A second run changes nothing.
  revert_mild.py <players.csv>"""
import csv, io, sys
sys.path.insert(0, "/home/user/yahoo-fantasy-basketball/scripts")
import hoops
NAMES = {"Kawhi Leonard", "Anthony Davis"}
REASON = "inj-risk (owner lock call 10/14: back from -mild to the full risk tier, 0.78);"
p = sys.argv[1]; raw = open(p, encoding="utf-8", newline="").read()
head = raw.splitlines()[0].split(","); rows = list(csv.DictReader(io.StringIO(raw))); rows0 = [dict(r) for r in rows]
for r in rows:
    if r["player"] in NAMES and r["note"].startswith("inj-risk-mild;"):
        r["note"] = REASON + r["note"][len("inj-risk-mild;"):]
changed = [r0["player"] for r, r0 in zip(rows, rows0) if r != r0]
for r, r0 in zip(rows, rows0):
    assert {k for k in r if r[k] != r0[k]} <= {"note"}, r["player"]
for r in rows:
    if r["player"] in NAMES:
        assert hoops.note_tag(r["note"]) == "inj-risk", (r["player"], hoops.note_tag(r["note"]))
        assert abs(hoops.availability(r) - 0.78) < 1e-9, (r["player"], hoops.availability(r))
buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=head, lineterminator="\r\n" if "\r\n" in raw else "\n"); w.writeheader(); w.writerows(rows)
open(p, "w", encoding="utf-8", newline="").write(buf.getvalue())
print(f"REVERT: {len(changed)} rows changed ({', '.join(changed) or 'none — already reverted'}); both at availability 0.78")
