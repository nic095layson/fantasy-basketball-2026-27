#!/usr/bin/env python3
"""WO-5 board diff, both planes, by script. Every player who moves three or more places on either board (inside the
top 200 before or after) gets one row with its mechanism, built from the records rather than written by hand:
  basis  — how his new line was made (lines JSON: base season and minutes, a role move with its outlets, the range
           rule's minutes move, a held rookie line, or no change to his line at all)
  driver — the two categories whose z moved most in the deck's own frame (positive = toward him), so a move with an
           unchanged line reads as the pool moving around him
Usage: wo5_boarddiff.py <pre deck players.csv> <post deck players.csv> <pre kit projections.csv> <post kit projections.csv>
                        <lines.json> <out.json> <out.md>"""
import sys, os, json, re, unicodedata, copy
DECK = os.environ.get("DECK_REPO", "/home/user/yahoo-fantasy-basketball"); KIT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, DECK + "/scripts"); sys.path.insert(0, KIT)
import hoops
import rank_engine as RE
pre_d, post_d, pre_k, post_k, LJ, OJ, OM = sys.argv[1:8]
ALI = {"herb jones": "herbert jones", "cam johnson": "cameron johnson", "nic claxton": "nicolas claxton", "alex sarr": "alexandre sarr", "ron holland": "ronald holland"}
def nk(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower(); s = re.sub(r"[.'`,’-]", "", s); s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = " ".join(t for t in s.split() if t not in {"jr", "sr", "ii", "iii", "iv"}); return ALI.get(s, s)
def deck(path):
    hoops.DATA_PATH = path
    P = hoops.zscores(hoops.load_players()); live = [p for p in P if hoops.availability(p) > 0]
    live.sort(key=lambda p: -hoops.adj_value(p, ()))
    return {nk(p["player"]): dict(rank=i + 1, name=p["player"], z=dict(p["z"]), value=hoops.adj_value(p, ())) for i, p in enumerate(live)}
def kit(path):
    rows = RE.load(path); rows, held = RE.exclude_held(rows)
    z1 = RE.zscores(rows, rows); pool = sorted(rows, key=lambda r: -RE.total(z1[r["name"]]))[:RE.POOL_SIZE]; z2 = RE.zscores(rows, pool)
    for r in rows:
        t = RE.total(z2[r["name"]]); av = RE.avail(r["gp"]); r["z_adj"] = t * av if t > 0 else t
    rows.sort(key=lambda r: -r["z_adj"])
    return {nk(r["name"]): dict(rank=i + 1, name=r["name"]) for i, r in enumerate(rows)}
D0, D1, K0, K1 = deck(pre_d), deck(post_d), kit(pre_k), kit(post_k)
L = {r["key"]: r for r in json.load(open(LJ, encoding="utf-8"))["rows"]}
def basis(k):
    x = L.get(k) or {}
    if not x.get("new"): return "line unchanged (no method line: rookie translation held or no qualifying season)"
    m = x["meta"]; g = x.get("range") or {}; src = x.get("minutes_source", "")
    if str(m.get("base", "")).startswith("rookie"):
        bits = []
        if g.get("factor", 1) != 1: bits.append(f"counting line x{g['factor']:.3f} to the outside lines' range")
        if g.get("pct"): bits.append("/".join(sorted(g["pct"])) + " to the range")
        if g.get("cnt"): bits.append("/".join(sorted(g["cnt"])) + (" by identity" if k in ("aj dybantsa", "cameron boozer") else " to the range"))
        if g.get("base_plane"): bits.append("the kit's line (D-R1)")
        return "rookie translation held; " + "; ".join(bits)
    s = f"{m['base']} per-36 at {m['minutes']:.1f} min"
    if g.get("factor", 1) != 1: s += f" (range rule R1 from {m['default_minutes']:.1f}" + (", after a role move" if src.startswith("override") else "") + ")"
    elif src.startswith("override: "): s += " (role: " + src[len("override: "):].split(" -> ")[0] + ")"
    elif "with" in m.get("default_minutes_basis", ""): s += f" ({m['default_minutes_basis']})"
    if g.get("pct"): s += "; " + "/".join(sorted(g["pct"])) + " to the range"
    return s
rows = []
for k in sorted(set(D0) | set(D1) | set(K0) | set(K1)):
    d0, d1, k0, k1 = (X.get(k, {}).get("rank") for X in (D0, D1, K0, K1))
    dm = (d0 - d1) if d0 and d1 else None; km = (k0 - k1) if k0 and k1 else None
    inside = lambda a, b: (a or 999) <= 200 or (b or 999) <= 200
    big = (dm is not None and abs(dm) >= 3 and inside(d0, d1)) or (km is not None and abs(km) >= 3 and inside(k0, k1))
    if not big: continue
    drv = ""
    if k in D0 and k in D1:
        dz = {c: D1[k]["z"][c] - D0[k]["z"][c] for c in D1[k]["z"]}
        top = sorted(dz.items(), key=lambda kv: -abs(kv[1]))[:2]
        drv = ", ".join(f"{c} {v:+.2f}" for c, v in top)
    name = (D1.get(k) or D0.get(k) or K1.get(k) or K0.get(k))["name"]
    rows.append(dict(player=name, deck_before=d0, deck_after=d1, deck_move=dm, kit_before=k0, kit_after=k1, kit_move=km, driver=drv, basis=basis(k)))
rows.sort(key=lambda r: min(r["deck_after"] or 999, r["kit_after"] or 999))
rec = dict(deck_rows=len(D1), kit_rows=len(K1), movers=len(rows),
           deck_movers=sum(1 for r in rows if r["deck_move"] is not None and abs(r["deck_move"]) >= 3),
           kit_movers=sum(1 for r in rows if r["kit_move"] is not None and abs(r["kit_move"]) >= 3), rows=rows)
json.dump(rec, open(OJ, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
f = lambda v: "—" if v is None else str(v)
mv = lambda v: "—" if v is None else (f"+{v}" if v > 0 else str(v))
out = ["| player | deck before → after (move) | kit before → after (move) | z driver (deck frame) | line basis (mechanism) |", "|---|---|---|---|---|"]
for r in rows:
    out.append(f"| {r['player']} | {f(r['deck_before'])} → {f(r['deck_after'])} ({mv(r['deck_move'])}) | {f(r['kit_before'])} → {f(r['kit_after'])} ({mv(r['kit_move'])}) | {r['driver'] or '—'} | {r['basis']} |")
open(OM, "w", encoding="utf-8").write("\n".join(out) + "\n")
print(f"board diff: {rec['movers']} players move 3+ on either board (deck {rec['deck_movers']}, kit {rec['kit_movers']})")
