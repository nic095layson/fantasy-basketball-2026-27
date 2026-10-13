#!/usr/bin/env python3
"""MG pass (Council recommendation, owner 'proceed' 2026-10-13): minutes and games for the top-150 players on a new
team or with a base season under 50 games, moved to the consensus of the two October outlets where both agree.
Rules fixed before this script was run (after-report-2026-10-13-mg.md states they were chosen with the candidate
table in view):
  MG-1 minutes — references: Hashtag 10/12 stated minutes; Yahoo 10/06 implied minutes = WO-5 minutes x the median
       over pts/reb/ast/tpm/tov of (Yahoo cell / WO-5 cell). Trigger: both references on the same side of the WO-5
       minutes, each by >= 1.5. New minutes = mean of the two, rounded to 0.1. Applied as a minutes override row
       (wo5_lines.py --minutes): rates unchanged, steals/blocks ride along, points by identity. A 10/12 override
       stands unless the same trigger fires against it, in which case the MG row replaces it.
  MG-2 games   — references: Yahoo 10/06 and Hashtag 10/12 games played. Trigger: both on the same side of the kit
       GP, each by >= 5. New GP = round(mean). Kit column only (the deck's modifier is tag-based; tags come from
       injury news, not projections — D-MG-2 on the owner's sheet).
  One reference only (no Hashtag line) -> hold, listed single-source. Rookies have no base season and are not candidates.
Usage: mg_moves.py <kit projections.csv> <lines_wo5.json> <bref totals.csv> <yahoo csv> <hashtag csv> <overrides 10/12 csv>
                   <out candidates.json> <out overrides csv> <out gp moves csv>"""
import csv, json, re, sys, unicodedata, statistics as st
KIT, LINES, TOT, YAH, HAS, OVR0, OUT_J, OUT_O, OUT_G = sys.argv[1:10]
sys.path.insert(0, "/home/user/fantasy-basketball-2026-27/report")
import rank_engine as RE
ALIASES = {"herb jones": "herbert jones", "cam johnson": "cameron johnson", "nic claxton": "nicolas claxton",
           "alex sarr": "alexandre sarr", "ron holland": "ronald holland"}
def norm(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'`,’-]", "", s); s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = " ".join(t for t in s.split() if t not in {"jr", "sr", "ii", "iii", "iv"}); return ALIASES.get(s, s)
MIN_TOL, GP_TOL, TOP, SHORT = 1.5, 5, 150, 50
DRIVE = ["pts", "reb", "ast", "tpm", "tov"]
# the kit board, as rank_engine ranks it (pool z-scores, availability on positive totals)
base = RE.load(KIT); kept, held = RE.exclude_held(base)
z1 = RE.zscores(kept, kept); order = sorted(kept, key=lambda r: -RE.total(z1[r["name"]])); pool = order[:RE.POOL_SIZE]; z = RE.zscores(kept, pool)
val = lambda r: (RE.total(z[r["name"]]) * RE.avail(r["gp"])) if RE.total(z[r["name"]]) > 0 else RE.total(z[r["name"]])
board = {norm(r["name"]): (i, r) for i, r in enumerate(sorted(kept, key=lambda r: -val(r)), 1)}
L = {r["key"]: r for r in json.load(open(LINES, encoding="utf-8"))["rows"]}
last = {}
for r in csv.DictReader(open(TOT, encoding="utf-8")):
    if r["season"] != "2025-26": continue
    if r.get("row", "season") == "split": last[r["pid"]] = r["team"]            # splits are chronological; the last wins
for r in csv.DictReader(open(TOT, encoding="utf-8")):
    if r["season"] == "2025-26" and r.get("row", "season") != "split": last.setdefault(r["pid"], r["team"])
BREF = {"BKN": "BRK", "CHA": "CHO", "PHX": "PHO"}
Y = {norm(r["player"]): r for r in csv.DictReader(open(YAH, encoding="utf-8"))}
H = {norm(r["player"]): r for r in csv.DictReader(open(HAS, encoding="utf-8"))}
ovr0 = {norm(r["player"]): r for r in csv.DictReader(open(OVR0, encoding="utf-8"))}
f = lambda x: float(x) if x not in (None, "") else None
cands = []
for n, (rank, k) in sorted(board.items(), key=lambda x: x[1][0]):
    if rank > TOP: continue
    r = L.get(n); m = (r or {}).get("meta") or {}
    if not r or not r.get("new") or not str(m.get("base", "")).startswith("20"): continue   # an NBA base season; held rookie lines are not candidates
    pid = r.get("pid"); moved = bool(pid in last and BREF.get(r.get("team"), r.get("team")) != last[pid])
    short = float(m["base_g"]) < SHORT
    if not (moved or short): continue
    w = r["new"]; wmin = float(m["minutes"]); y = Y.get(n); h = H.get(n)
    c = dict(rank=rank, player=k["name"], why=[x for x, ok in (("new team", moved), ("base under 50 games", short)) if ok],
             base=m["base"], base_g=int(float(m["base_g"])), wo5_minutes=wmin, default_minutes=f(m.get("default_minutes")),
             override_1012=(ovr0.get(n) or {}).get("mechanism"), kit_gp=int(float(k["gp"])),
             prev_team=last.get(pid), team=r.get("team"))
    # MG-1
    ratios = [f(y[cat]) / float(w[cat]) for cat in DRIVE if y and f(y.get(cat)) is not None and float(w[cat]) > 0.05] if y else []
    y_impl = round(wmin * st.median(ratios), 1) if len(ratios) >= 3 else None
    h_mpg = f(h.get("mpg")) if h else None
    c.update(hashtag_mpg=h_mpg, yahoo_implied_minutes=y_impl, yahoo_ratio_cells=len(ratios))
    if h_mpg is None or y_impl is None:
        c["mg1"] = "HOLD — single source (" + ("no Hashtag line" if h_mpg is None else "no Yahoo line") + ") [SINGLE-SOURCE]"
    else:
        dh, dy = h_mpg - wmin, y_impl - wmin
        if dh >= MIN_TOL and dy >= MIN_TOL or dh <= -MIN_TOL and dy <= -MIN_TOL:
            new = round((h_mpg + y_impl) / 2, 1)
            c["mg1"] = "MOVE"; c["new_minutes"] = new
            c["mg1_mechanism"] = (f"MG-1: Hashtag 10/12 {h_mpg:.1f} min and Yahoo 10/06 implied {y_impl:.1f} min (median of five cells) both "
                                  f"{'above' if dh > 0 else 'below'} the {'10/12 override' if ovr0.get(n) else 'WO-5'} {wmin:.1f} by 1.5+ -> mean {new:.1f}")
        else: c["mg1"] = "HOLD — references split or within 1.5 min"
    # MG-2
    yg, hg = (f(y.get("gp")) if y else None), (f(h.get("gp")) if h else None)
    c.update(yahoo_gp=yg, hashtag_gp=hg)
    if yg is None or hg is None: c["mg2"] = "HOLD — single source [SINGLE-SOURCE]"
    else:
        dg1, dg2 = yg - c["kit_gp"], hg - c["kit_gp"]
        if dg1 >= GP_TOL and dg2 >= GP_TOL or dg1 <= -GP_TOL and dg2 <= -GP_TOL:
            c["mg2"] = "MOVE"; c["new_gp"] = int(round((yg + hg) / 2))
            c["mg2_mechanism"] = f"MG-2: Yahoo 10/06 {int(yg)} GP and Hashtag 10/12 {int(hg)} GP both {'above' if dg1 > 0 else 'below'} the kit {c['kit_gp']} by 5+ -> mean {c['new_gp']}"
        else: c["mg2"] = "HOLD — references split or within 5 games"
    cands.append(c)
# outputs
moves1 = [c for c in cands if c["mg1"] == "MOVE"]; moves2 = [c for c in cands if c["mg2"] == "MOVE"]
rows = [dict(r) for r in csv.DictReader(open(OVR0, encoding="utf-8"))]
replaced = []
for c in moves1:
    n = norm(c["player"]); hit = [r for r in rows if norm(r["player"]) == n]
    if hit: hit[0]["minutes"] = f"{c['new_minutes']:.1f}"; hit[0]["mechanism"] = c["mg1_mechanism"]; replaced.append(c["player"])
    else: rows.append(dict(player=c["player"], minutes=f"{c['new_minutes']:.1f}", mechanism=c["mg1_mechanism"]))
for r in rows: assert "]" not in r["mechanism"] and ";" not in r["mechanism"][-2:], r   # A7: never '];' in a note
with open(OUT_O, "w", encoding="utf-8", newline="") as fh:
    wtr = csv.DictWriter(fh, fieldnames=["player", "minutes", "mechanism"]); wtr.writeheader(); [wtr.writerow(r) for r in rows]
with open(OUT_G, "w", encoding="utf-8", newline="") as fh:
    wtr = csv.DictWriter(fh, fieldnames=["player", "gp_old", "gp_new", "mechanism"]); wtr.writeheader()
    for c in moves2: wtr.writerow(dict(player=c["player"], gp_old=c["kit_gp"], gp_new=c["new_gp"], mechanism=c["mg2_mechanism"]))
summ = dict(rules=dict(min_tol=MIN_TOL, gp_tol=GP_TOL, top=TOP, short_base_games=SHORT, references=["Yahoo 10/06 (yahoo-proj-2026-10-06.csv)", "Hashtag 10/12 (hashtag-2026-10-12.csv)"]),
            candidates=len(cands), movers=sum("new team" in c["why"] for c in cands), short_base=sum("base under 50 games" in c["why"] for c in cands),
            mg1_moves=len(moves1), mg1_up=sum(c["new_minutes"] > c["wo5_minutes"] for c in moves1), mg1_replacing_1012_override=replaced,
            mg1_single_source=[c["player"] for c in cands if "SINGLE" in c["mg1"]], mg2_moves=len(moves2), mg2_single_source=[c["player"] for c in cands if "SINGLE" in c["mg2"]],
            overrides_rows=len(rows))
json.dump(dict(summary=summ, candidates=cands), open(OUT_J, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(json.dumps(summ, indent=1))
print(f"{'#':>3} {'player':24} {'WO5':>5} {'Hmpg':>5} {'Yimp':>5} -> {'new':>5} | {'kitGP':>5} {'Ygp':>4} {'Hgp':>4} -> {'new':>4}")
for c in cands:
    print(f"{c['rank']:>3} {c['player']:24} {c['wo5_minutes']:5.1f} {str(c['hashtag_mpg']):>5} {str(c['yahoo_implied_minutes']):>5} -> {str(c.get('new_minutes','—')):>5} | {c['kit_gp']:5d} {str(c['yahoo_gp']):>4} {str(c['hashtag_gp']):>4} -> {str(c.get('new_gp','—')):>4}   {c['mg1'][:22]:22} {c['mg2'][:22]}")
