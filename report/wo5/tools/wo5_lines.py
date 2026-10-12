#!/usr/bin/env python3
"""WO-5 default lines (P3-P4). For every row on either plane: the Basketball-Reference id, the base season, and the method line
at the base season's minutes. Method (pre-draft-workorder WO-5 + queue item 8 + the 10/7 Castle precedent):
  minutes   = base-season minutes per game (overrides from the role-evidence file only, each with two dated outlets)
  base      = 2025-26 if G >= 25, else the latest of 2024-25 / 2023-24 with G >= 25, else none (line held)
  FGA, FTA, 3PM, REB, AST, TOV = base-season per-36 x minutes / 36
  FG%, FT%  = base-season percentage shrunk one-third toward career (all regular seasons on file through 2025-26)
  STL, BLK  = per-36 of the three-season line (2025-26 / 2024-25 / 2023-24 weighted 5/4/3 by games), x minutes / 36
  PTS       = 2 * FGA * FG% + 3PM + FTA * FT%  (the points identity)
Range resolution (wo5_range.py, D-RN-3): --range range.json replaces a listed player's minutes (R1) and shooting
percentages (R3); a rookie's held line takes the R1 factor and the R3/R1b cells; points follow by identity.
Usage: wo5_lines.py <bref_totals.csv> <deck players.csv> <kit projections.csv> <out.json> [--minutes overrides.csv] [--range range.json]"""
import csv, json, sys, re, unicodedata, statistics as st, os
TOT, DECK, KIT, OUT = sys.argv[1:5]
OVR = sys.argv[sys.argv.index("--minutes") + 1] if "--minutes" in sys.argv else None
RNG = json.load(open(sys.argv[sys.argv.index("--range") + 1])) if "--range" in sys.argv else {}
ALIASES = {"herb jones": "herbert jones", "cam johnson": "cameron johnson", "nic claxton": "nicolas claxton",
           "alex sarr": "alexandre sarr", "ron holland": "ronald holland"}
def norm(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'`,’-]", "", s); s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = " ".join(t for t in s.split() if t not in {"jr", "sr", "ii", "iii", "iv"})
    return ALIASES.get(s, s)
TEAMFIX = {"BRK": "BKN", "PHO": "PHX", "CHO": "CHA", "GSW": "GS", "NOP": "NO", "SAS": "SA", "NYK": "NY", "UTA": "UTAH", "WAS": "WSH"}
CANON = {"BRK": "BKN", "BKN": "BKN", "PHO": "PHX", "PHX": "PHX", "CHO": "CHA", "CHA": "CHA", "GS": "GSW", "GSW": "GSW", "NO": "NOP", "NOP": "NOP",
         "SA": "SAS", "SAS": "SAS", "NY": "NYK", "NYK": "NYK", "UTAH": "UTA", "UTA": "UTA", "WSH": "WAS", "WAS": "WAS"}
canon = lambda t: CANON.get(t, t) if t else t
seasons = {}; bypid = {}; names = {}; splits = {}
for r in csv.DictReader(open(TOT, encoding="utf-8")):
    for k in ("g", "gs", "mp", "fg", "fga", "fg3", "ft", "fta", "trb", "ast", "stl", "blk", "tov", "pts"): r[k] = float(r[k])
    if r.get("row", "season") == "split":
        splits.setdefault(r["pid"], {}).setdefault(r["season"], []).append(r); continue
    bypid.setdefault(r["pid"], {})[r["season"]] = r
    names.setdefault(norm(r["player"]), set()).add(r["pid"])
def career(pid):
    s = bypid[pid].values(); fg = sum(x["fg"] for x in s); fga = sum(x["fga"] for x in s); ft = sum(x["ft"] for x in s); fta = sum(x["fta"] for x in s)
    return (fg / fga if fga else None, ft / fta if fta else None, fga, fta)
def base_season(pid):
    for s in ("2025-26", "2024-25", "2023-24"):
        r = bypid[pid].get(s)
        if r and r["g"] >= 25 and r["mp"] > 0: return s
    return None
def anchor36(pid, stat):
    num = den = 0.0; used = []
    for s, w in (("2025-26", 5), ("2024-25", 4), ("2023-24", 3)):
        r = bypid[pid].get(s)
        if not r or r["g"] == 0 or r["mp"] == 0: continue
        ww = w * r["g"]; num += ww * r[stat] / r["mp"] * 36; den += ww; used.append(f"{s}:{int(r['g'])}")
    return (num / den if den else None), used
def default_minutes(pid, s, team):
    """The base season's minutes; for a player traded during it, his minutes with his current team when that is his last
    split of 15+ games (Basketball-Reference team rows, chronological)."""
    r = bypid[pid][s]; mpg = r["mp"] / r["g"]
    sp = splits.get(pid, {}).get(s, [])
    if r["team"].endswith("TM") and sp:
        last = sp[-1]
        if canon(last["team"]) == canon(team) and last["g"] >= 15:
            return last["mp"] / last["g"], f"{s} minutes with {last['team']} ({int(last['g'])} of {int(r['g'])} games)"
    return mpg, f"{s} minutes"
def line(pid, minutes=None, team=None, pct=None):
    s = base_season(pid)
    if not s: return None
    r = bypid[pid][s]; mpg = r["mp"] / r["g"]
    dm, dsrc = default_minutes(pid, s, team)
    M = minutes if minutes is not None else dm
    k = M / r["mp"]   # per-minute scale on season totals
    cfg, cft, cfga, cfta = career(pid)
    sfg = r["fg"] / r["fga"] if r["fga"] else 0.0; sft = r["ft"] / r["fta"] if r["fta"] else 0.0
    fgp = sfg + ((cfg - sfg) / 3 if cfg is not None and r["fga"] else 0.0)
    ftp = sft + ((cft - sft) / 3 if cft is not None and r["fta"] else 0.0)
    stl36, su = anchor36(pid, "stl"); blk36, _ = anchor36(pid, "blk")
    L = dict(fga=r["fga"] * k, fta=r["fta"] * k, tpm=r["fg3"] * k, reb=r["trb"] * k, ast=r["ast"] * k, tov=r["tov"] * k,
             stl=stl36 * M / 36, blk=blk36 * M / 36, fg_pct=fgp, ft_pct=ftp)
    if pct:
        L["fg_pct"] = pct.get("fg_pct", L["fg_pct"]); L["ft_pct"] = pct.get("ft_pct", L["ft_pct"])
    L["pts"] = 2 * L["fga"] * L["fg_pct"] + L["tpm"] + L["fta"] * L["ft_pct"]
    meta = dict(base=s, base_g=int(r["g"]), base_gs=int(r["gs"]), base_mpg=round(mpg, 2), minutes=round(M, 2), base_team=r["team"],
                default_minutes=round(dm, 2), default_minutes_basis=dsrc,
                splits=[(x["team"], int(x["g"]), int(x["gs"]), round(x["mp"] / x["g"], 1)) for x in splits.get(pid, {}).get(s, [])],
                season_fg=round(sfg, 4), season_ft=round(sft, 4), career_fg=round(cfg, 4) if cfg else None, career_ft=round(cft, 4) if cft else None,
                career_fga=int(cfga), career_fta=int(cfta), anchor_seasons=su,
                season_pg={c: round(r[t] / r["g"], 2) for c, t in (("pts", "pts"), ("reb", "trb"), ("ast", "ast"), ("stl", "stl"), ("blk", "blk"), ("tpm", "fg3"), ("tov", "tov"), ("fga", "fga"), ("fta", "fta"))})
    return L, meta
def rnd(L):
    out = {c: round(L[c], 1) for c in ("fga", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov")}
    out["fg_pct"] = round(L["fg_pct"], 3); out["ft_pct"] = round(L["ft_pct"], 3)
    return out
deck = list(csv.DictReader(open(DECK, encoding="utf-8"))); kit = list(csv.DictReader(open(KIT, encoding="utf-8")))
ovr = {}
if OVR:
    for r in csv.DictReader(open(OVR, encoding="utf-8")): ovr[norm(r["player"])] = r
def match(name, team):
    n = norm(name); c = names.get(n, set())
    if len(c) == 1: return next(iter(c)), "name"
    if len(c) > 1:
        t = TEAMFIX.get(team, team)
        hits = [p for p in c if any(TEAMFIX.get(x["team"], x["team"]) == t for x in bypid[p].values() if x["season"] >= "2023-24")]
        if len(hits) == 1: return hits[0], "name+team"
        recent = [p for p in c if "2025-26" in bypid[p]]
        if len(recent) == 1: return recent[0], "name+2025-26"
        return None, f"ambiguous {sorted(c)}"
    return None, "no bref row"
rows = {}
for plane, P, nk in (("deck", deck, "player"), ("kit", kit, "name")):
    for r in P:
        n = norm(r[nk]); e = rows.setdefault(n, dict(name=r[nk]))
        e[plane] = r
out = []
for n, e in rows.items():
    team = (e.get("deck") or e.get("kit"))["team"]
    pid, how = match(e["name"], team)
    rec = dict(name=e["name"], key=n, on_deck="deck" in e, on_kit="kit" in e, team=team, pid=pid, match=how,
               tag=(e.get("deck") or {}).get("note", "").split(" ")[0].split("(")[0] if e.get("deck") else None,
               kit_gp=(e.get("kit") or {}).get("gp"), kit_mpg=(e.get("kit") or {}).get("mpg"))
    g = RNG.get(n)
    if pid:
        o = ovr.get(n)
        M = float(g["minutes"]) if g and g.get("minutes") is not None else (float(o["minutes"]) if o else None)
        res = line(pid, M, team, (g or {}).get("pct"))
        if res:
            L, meta = res; rec["new"] = rnd(L); rec["meta"] = meta; rec["minutes_source"] = ("override: " + o["mechanism"]) if o else meta["default_minutes_basis"]
            if g: rec["range"] = g
        else:
            rec["new"] = None; rec["meta"] = {"seasons": sorted(bypid[pid].keys())[-3:]}
    if g and g.get("rookie") and not rec.get("new"):
        bp = g.get("base_plane") or ("deck" if e.get("deck") else "kit")   # D-R1: a row whose planes differ names the plane it keeps
        src = e[bp]; f = float(g.get("factor", 1.0)); kc = {"fg_pct": "fgp", "ft_pct": "ftp"}
        get = (lambda c: float(src[c])) if bp == "deck" else (lambda c: float(src[kc.get(c, c)]))
        Lr = {c: get(c) * f for c in ("fga", "fta", "tpm", "reb", "ast", "stl", "blk", "tov")}
        Lr["fg_pct"] = g.get("pct", {}).get("fg_pct", get("fg_pct")); Lr["ft_pct"] = g.get("pct", {}).get("ft_pct", get("ft_pct"))
        for c, val in g.get("cnt", {}).items():
            if c != "pts": Lr[c] = val
        if "pts" in g.get("cnt", {}):   # points to the range through shot volume, so the identity holds
            sv = (g["cnt"]["pts"] - Lr["tpm"]) / (2 * Lr["fga"] * Lr["fg_pct"] + Lr["fta"] * Lr["ft_pct"])
            Lr["fga"] *= sv; Lr["fta"] *= sv
        Lr["pts"] = 2 * Lr["fga"] * Lr["fg_pct"] + Lr["tpm"] + Lr["fta"] * Lr["ft_pct"]
        km = float((e.get("kit") or {}).get("mpg") or 0) * f
        rec["new"] = rnd(Lr); rec["meta"] = dict(base="rookie translation (held)", minutes=round(km, 2), factor=f)
        rec["minutes_source"] = "rookie translation x R1 factor"; rec["range"] = g
    if e.get("deck"):
        d = e["deck"]; rec["deck_line"] = {c: d[c] for c in ("fg_pct", "fga", "ft_pct", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov")}
    if e.get("kit"):
        k = e["kit"]; rec["kit_line"] = {"fg_pct": k["fgp"], "fga": k["fga"], "ft_pct": k["ftp"], "fta": k["fta"], **{c: k[c] for c in ("tpm", "pts", "reb", "ast", "stl", "blk", "tov")}}
    out.append(rec)
used = {r["key"] for r in out if str(r.get("minutes_source", "")).startswith("override")}
assert used == set(ovr), f"overrides not applied: {sorted(set(ovr) - used)}"
summ = dict(rows=len(out), matched=sum(1 for r in out if r["pid"]), with_line=sum(1 for r in out if r.get("new")),
            held_no_qualifying_season=sorted(r["name"] for r in out if r["pid"] and not r.get("new")),
            unmatched=sorted((r["name"], r["match"]) for r in out if not r["pid"]),
            base_not_2526=sorted((r["name"], r["meta"]["base"]) for r in out if r.get("new") and r["meta"]["base"] != "2025-26"))
json.dump(dict(summary=summ, rows=out), open(OUT, "w", encoding="utf-8"), indent=1)
print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in summ.items()}))
print("unmatched:", summ["unmatched"])
print("held (no season with 25+ G in 2023-24..2025-26):", summ["held_no_qualifying_season"])
print("base season not 2025-26:", summ["base_not_2526"])
