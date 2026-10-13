#!/usr/bin/env python3
"""2026-10-13 MG pass, deck page edits: JUDGMENT date re-authored to the pull; dated receipts on the two judgment cards
whose lines the pass moved (Embiid, DeRozan — numbers read from the apply record); the colophon Data paragraph's head
rewritten for this refresh (the tail from 'Rookie lines' kept verbatim). Exact anchors; all-or-nothing; idempotent."""
import json, re, sys
P = "/home/user/yahoo-fantasy-basketball/docs/draft-deck.html"; K = "/home/user/fantasy-basketball-2026-27/report/mg"
s = open(P, encoding="utf-8").read(); orig = s
STALE = "No tag, games-played figure or placement changed."   # 10/12's tail sentence; false for this pass on the kit plane (five games moves)
FIXED = "No tag or placement changed on this page; the five games moves live on the kit plane (above)."
if STALE in s:   # second step (found on the served v61 read-back, 2026-10-13): the carried tail contradicted the new head
    assert s.count(STALE) == 1; open(P, "w", encoding="utf-8").write(s.replace(STALE, FIXED)); print("tail sentence corrected:", FIXED); s = s.replace(STALE, FIXED)
if 'const JUDGMENT = {\n  date: "2026-10-13",' in s and "This refresh (10/13" in s: print("already applied"); sys.exit(0)
assert s.count('const JUDGMENT = {\n  date: "2026-10-12",') == 1
s = s.replace('const JUDGMENT = {\n  date: "2026-10-12",', 'const JUDGMENT = {\n  date: "2026-10-13",')
rec = {(x["plane"], x["player"]): x for x in json.load(open(K + "/out/apply_record_2026-10-13.json", encoding="utf-8"))["rows"]}
C = {c["player"]: c for c in json.load(open(K + "/out/candidates_2026-10-13.json", encoding="utf-8"))["candidates"]}
def nums(name):
    k = rec[("kit", name)]; c = C[name]
    return dict(m0=float(k["before"]["mpg"]), m1=float(k["after"]["mpg"]), p0=float(k["before"]["pts"]), p1=float(k["after"]["pts"]), h=c["hashtag_mpg"], y=c["yahoo_implied_minutes"])
e, d = nums("Joel Embiid"), nums("DeMar DeRozan")
RECEIPTS = {
    "Joel Embiid": f" 10/13 (MG pass): minutes {e['m0']:.1f} -> {e['m1']:.1f} on the Yahoo 10/06 and Hashtag 10/12 consensus (Hashtag {e['h']:.1f}, Yahoo implied {e['y']:.1f}, both below the WO-5 figure by 1.5+), points {e['p0']:.1f} -> {e['p1']:.1f}; +0.10 stays — the card's reason is the healthy offseason, not the minutes.",
    "DeMar DeRozan": f" 10/13 (MG pass): minutes {d['m0']:.1f} -> {d['m1']:.1f} on the consensus (Hashtag {d['h']:.1f}, Yahoo implied {d['y']:.1f}), points {d['p0']:.1f} -> {d['p1']:.1f} — the third-option role this card described; -0.05 stays.",
}
for name, add in RECEIPTS.items():
    key = f'    "{name}": {{ adj: '; i = s.find(key); assert i >= 0 and s.count(key) == 1, name
    j = s.find('" },', i); assert j > i and "10/13 (MG pass)" not in s[i:j], name
    s = s[:j] + add + s[j:]
m = re.search(r"<p><strong>Data\.</strong>(.*?)</p>", s, re.S); assert m
body = m.group(1); t = body.find("Rookie lines"); assert t > 0 and body.count("Rookie lines") == 1
tail = body[t:]
HEAD = (" Pool refreshed 2026-10-13 under the roster validation lock — 335 rows, every placement cross-checked against ESPN’s live "
        "rosters (direct-complete, all 30 teams, zero mismatches, 335/335 on the feed, no exemption). This refresh (10/13, the "
        "minutes-and-games pass the Council recommended and the owner approved) reviewed the top-150 players on a new team or with a "
        "base season under 50 games — 47 candidates — against the two October projection outlets, Yahoo 10/6 and Hashtag 10/12, and "
        "moved minutes only where both sat on the same side of the WO-5 figure by 1.5 or more: fifteen lines re-scaled to the two "
        "outlets’ mean minutes, rates unchanged, steals and blocks riding along, points by the shooting identity, written to both "
        "planes by the same asserted script as WO-5 — up for Giannis Antetokounmpo, Kel’el Ware, Franz Wagner, Jalen Williams, Darius "
        "Garland, John Collins, Alex Sarr and Dejounte Murray; down for Joel Embiid, DeMar DeRozan, Grayson Allen, Kelly Oubre Jr., "
        "Royce O’Neale, Tobias Harris and Jerami Grant. The range rule (D-RN-3) then re-ran on the result and re-fixed two of them "
        "inside its references (Dejounte Murray at 29.2 minutes, Alex Sarr at 26.8); the other 32 candidates hold (outlets split, "
        "within tolerance, or one outlet only — Deandre Ayton). Games played moved for five players on the kit plane only (this page’s "
        "availability is tag-based, and tags come from injury news); WO-5’s lines, role moves and the rest of its range resolution "
        "stand as published on 10/12. ")
s = s[:m.start(1)] + HEAD + tail + s[m.end(1):]
assert s != orig and "];" not in s[m.start(1):m.start(1) + len(HEAD) + len(tail)]
open(P, "w", encoding="utf-8").write(s); print("page edited: JUDGMENT date 2026-10-13; receipts Embiid, DeRozan; Data paragraph head (tail kept)")
