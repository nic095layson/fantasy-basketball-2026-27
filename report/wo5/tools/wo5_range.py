#!/usr/bin/env python3
"""WO-5 range resolution (D-RN-3 on the projection pass). Rules fixed before they were run (2026-10-12):
  R1 minutes  — for a listed player with two or more of pts/reb/ast/tpm/tov outside on the same side (the signature
                of a minutes difference; one such cell alone is a rate and goes to R2), one factor f on his counting line (= his minutes x f; rates unchanged; points
                by identity), chosen to bring every listed cell among pts/reb/ast/tpm/tov inside [min, max] of his
                references while keeping every other counting cell inside the check's tolerance; the f nearest 1 among
                those with the fewest cells left outside; applied only if it leaves fewer such cells outside. STL/BLK
                ride along (rate form) but never choose f — they are the item-8 anchor.
  R2 rates    — a pts/reb/ast/tpm/tov cell still outside after R1 stays, with the mechanism "base-season per-36
                rates (Basketball-Reference; ESPN)"; a STL/BLK cell stays with "item-8 three-season anchor
                (Basketball-Reference; ESPN)".
  R3 shooting — a FG%/FT% cell outside: stays with "one-third shrink to career (Basketball-Reference; ESPN)" when
                his unshrunk base-season value is itself inside the tolerance band (the shrink put it outside);
                otherwise (no 2025-26 season of 25+ games, or a rookie translation) it moves to the nearest end of
                [min, max] and points follow by identity.
  Rookies     — held lines (no NBA season) take R1 and R3 the same way; a counting cell left outside after R1 moves
                to the nearest end (no NBA rates to cite) — points by scaling his shot volume (FGA and FTA together) so
                the identity holds.
Usage: wo5_range.py <candidate players.csv> <lines.json> <out range.json> [--prev range.json]"""
import sys, os, json, argparse, csv, re, unicodedata
DECK = "/home/user/yahoo-fantasy-basketball"; KIT = "/home/user/fantasy-basketball-2026-27"
sys.path.insert(0, DECK + "/scripts")
import hoops, range_check as RC
ap = argparse.ArgumentParser(); ap.add_argument("cand"); ap.add_argument("lines"); ap.add_argument("out"); ap.add_argument("--prev")
a = ap.parse_args()
ALI = {"herb jones": "herbert jones", "cam johnson": "cameron johnson", "nic claxton": "nicolas claxton", "alex sarr": "alexandre sarr", "ron holland": "ronald holland"}
def nk(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower(); s = re.sub(r"[.'`,’-]", "", s); s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = " ".join(t for t in s.split() if t not in {"jr", "sr", "ii", "iii", "iv"}); return ALI.get(s, s)
L = {r["key"]: r for r in json.load(open(a.lines))["rows"]}
prev = json.load(open(a.prev)) if a.prev else {}
hoops.DATA_PATH = a.cand
rec = RC.compute(argparse.Namespace(kit=KIT, actual=RC.ACTUAL_DEFAULT, top=150))
refs, used = RC.references(KIT, RC.ACTUAL_DEFAULT)
deck = {nk(r["player"]): r for r in csv.DictReader(open(a.cand, encoding="utf-8"))}
CNT = ["pts", "reb", "ast", "tpm", "tov", "stl", "blk"]; DRIVE = ["pts", "reb", "ast", "tpm", "tov"]
tol = lambda c, hi: 0.005 if c.endswith("pct") else max(0.1, 0.05 * hi)
out = dict(prev)
for row in rec["rows"]:
    k = nk(row["player"]); ref = refs[RC.fold(row["player"])]; p = deck[k]
    lo = {c: min(d[c] for d in ref.values()) for c in RC.CATS}; hi = {c: max(d[c] for d in ref.values()) for c in RC.CATS}
    flagged = {c["cat"] for c in row["cells"]}
    v = {c: float(p[c]) for c in RC.CATS + ["fga", "fta"]}
    x = L.get(k) or {}
    rookie = not str((x.get("meta") or {}).get("base") or "").startswith("20")   # no NBA base season: a held line
    e = dict(out.get(k, {})); e.setdefault("player", row["player"]); e.setdefault("cells_seen", [])
    e["cells_seen"] = sorted(set(e["cells_seen"]) | {c["text"] for c in row["cells"]})
    # R1
    def bad(f):
        n = 0
        for c in DRIVE:
            val = v[c] * f
            if c in flagged:
                n += not (lo[c] <= val <= hi[c])
            else:
                n += not (lo[c] - tol(c, hi[c]) <= val <= hi[c] + tol(c, hi[c]))
        return n
    base_bad = bad(1.0)
    # the minutes signature: two or more of pts/reb/ast/tpm/tov outside on the same side (one cell alone is a rate)
    hi_n = sum(1 for c in DRIVE if c in flagged and v[c] > hi[c]); lo_n = sum(1 for c in DRIVE if c in flagged and v[c] < lo[c])
    if max(hi_n, lo_n) >= 2:
        best = min((bad(f / 1000), abs(f / 1000 - 1), f / 1000) for f in range(500, 1701))
        f = best[2] if best[0] < base_bad else 1.0
    else:
        f = 1.0
    mech = {}
    if f != 1.0:
        f0 = e.get("factor", 1.0); e["factor"] = round(f0 * f, 4)
        if not rookie:
            e["minutes"] = round(x["meta"]["minutes"] * f, 1)
        mech["minutes"] = f"R1 minutes to the outside lines' range ({', '.join(sorted(k2 for k2 in ref))})"
    # cells after R1
    after = {c: (v[c] * f if c in CNT else v[c]) for c in RC.CATS}
    pct = dict(e.get("pct", {}))
    for c in ["fg_pct", "ft_pct"]:
        if lo[c] - tol(c, hi[c]) <= after[c] <= hi[c] + tol(c, hi[c]): continue
        season = None if rookie else (x["meta"]["season_fg"] if c == "fg_pct" else x["meta"]["season_ft"])
        if season is not None and x["meta"]["base"] == "2025-26" and lo[c] - tol(c, hi[c]) <= season <= hi[c] + tol(c, hi[c]):
            mech[c] = "R3 keep: one-third shrink to career (Basketball-Reference; ESPN)"
        else:
            pct[c] = round(min(max(after[c], lo[c]), hi[c]), 3)
            mech[c] = f"R3 to the range ({'rookie translation' if rookie else x['meta']['base'] + ' base'})"
    if pct: e["pct"] = pct
    left = []
    for c in CNT:
        if lo[c] - tol(c, hi[c]) <= after[c] <= hi[c] + tol(c, hi[c]): continue
        if rookie:   # no NBA rates and no three-season anchor to cite: every counting cell to the range
            e.setdefault("cnt", {})[c] = round(min(max(after[c], lo[c]), hi[c]), 1); mech[c] = "R1b rookie cell to the range"
        elif c in ("stl", "blk"):
            mech[c] = "R2 keep: item-8 three-season anchor (Basketball-Reference; ESPN)"; left.append(c)
        else:
            mech[c] = f"R2 keep: {'' if rookie else x['meta']['base'] + ' '}per-36 rates (Basketball-Reference; ESPN)"; left.append(c)
    e["rookie"] = rookie
    e.setdefault("mechanisms", {}).update(mech)
    out[k] = e
json.dump(out, open(a.out, "w"), indent=1, ensure_ascii=False)
print(f"range rows {rec['players']} ({rec['cells']} cells); entries now {len(out)}; "
      f"R1 moves {sum(1 for e in out.values() if e.get('factor', 1) != 1)}; R3 clamps {sum(len(e.get('pct', {})) for e in out.values())}; "
      f"rookie cell moves {sum(len(e.get('cnt', {})) for e in out.values())}")
