#!/usr/bin/env python3
"""Board-wide context check (owner question 2026-10-13, Holiday and Portland's four point guards): which top-150 lines
score more points than ALL THREE outside projections, and what changed around each of them.

Input: range_check_no_actual.json, the deck's own range check (scripts/range_check.py at deck f6fb476, owner rule
D-RN-3) run with --actual pointing at no file, so the references are the three outside projections only (Yahoo 10/13,
Hashtag 10/12, RotoBaller 9/29) and the player's own 2025-26 line is NOT a reference. Its rule: top 150 by the deck's
value, a cell is outside when it misses [min, max] of the references by more than max(0.1, 5% of the max).

Each line whose points cell sits ABOVE all three gets one label (A5, stated to the owner before the run):
  moved             today's team is not among his 2025-26 teams (Basketball-Reference season and split rows)
  no 2025-26 games  no 2025-26 row (a rookie, or a season missed)
  stayed, arrivals  same team, and the kit pool on that team holds a teammate projected for MIN+ minutes a game who
                    arrived (was not on the team in 2025-26, or had no 2025-26 games) or returns (fewer than 41 games
                    in 2025-26)
  stayed, none      same team, no such teammate
and a budget flag from team_budget.txt (over the 2025-26 league maximum / over the team's own 2025-26 total), and the
value rank and market rank the live page (Version 64, sha256 a88d83f4e2f8) gives him (../live-mock-2026-10-13/val_v64.json).
The last block counts, for each threshold, the teams whose kit pool holds such an arrival or return at all: a label
every team earns cannot separate a context miss from a career year that will not repeat.
MIN is 20 (a rotation player); the class counts are also printed at 25 (a starter's share) as a sensitivity line."""
import ast, csv, json, os, re, unicodedata
H = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.normpath(os.path.join(H, "..", "..", ".."))
MAP = {"BKN": "BRK", "CHA": "CHO", "PHX": "PHO"}
MULTI = {"2TM", "3TM", "4TM", "TOT"}
def fold(s):  # the range check's own name fold
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'’]", "", s); s = re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()
rec = json.load(open(os.path.join(H, "range_check_no_actual.json"), encoding="utf-8"))
kit = {fold(r["name"]): r for r in csv.DictReader(open(os.path.join(KIT, "report/projections-2026-27.csv"), encoding="utf-8"))}
last = {}  # fold(name) -> {"teams": set, "g": games}
for r in csv.DictReader(open(os.path.join(KIT, "report/wo5/data/bref_totals_2004-2026.csv"))):
    if r["season"] != "2025-26": continue
    d = last.setdefault(fold(r["player"]), {"teams": set(), "g": 0.0})
    if r["row"] == "season":
        d["g"] = float(r["g"])
        if r["team"] not in MULTI: d["teams"].add(r["team"])
    else:
        d["teams"].add(r["team"])
V = {fold(r["n"]): r for r in json.load(open(os.path.join(H, "..", "live-mock-2026-10-13", "val_v64.json"), encoding="utf-8"))}
txt = open(os.path.join(H, "team_budget.txt"), encoding="utf-8").read()
over_max = ast.literal_eval(re.search(r"above the 2025-26 league maximum \([\d.]+\): \d+ (\[.*?\])", txt).group(1))
over_own = ast.literal_eval(re.search(r"used in 2025-26: \d+ (\[.*?\])", txt).group(1))
team = lambda k: MAP.get(kit[k]["team"], kit[k]["team"])
def arrivals(k, MIN):
    t = team(k); out = []
    for j, r in kit.items():
        if j == k or team(j) != t or float(r["mpg"]) < MIN: continue
        L = last.get(j)
        if L is None: out.append(f"{r['name']} {r['mpg']} min, no 2025-26 games")
        elif t not in L["teams"]: out.append(f"{r['name']} {r['mpg']} min, from {'/'.join(sorted(L['teams']))}")
        elif L["g"] < 41: out.append(f"{r['name']} {r['mpg']} min, returns ({L['g']:.0f} games)")
    return out
def label(k, MIN):
    L = last.get(k)
    if L is None: return "no 2025-26 games"
    if team(k) not in L["teams"]: return "moved"
    return "stayed, arrivals" if arrivals(k, MIN) else "stayed, none"
above, below, missing = [], [], []
for row in rec["rows"]:
    c = next((c for c in row["cells"] if c["cat"] == "pts"), None)
    if not c: continue
    k = fold(row["player"])
    if k not in kit: missing.append(row["player"]); continue
    (above if c["ours"] > c["hi"] else below).append((row, c, k))
print(f"range check without the own-season reference: {rec['players']} of {rec['checkable']} checkable top-{rec['top']} lines "
      f"have a cell outside all three projections ({rec['cells']} cells); references {rec['references']}")
print(f"points above all three: {len(above)}; points below all three: {len(below)}; names not matched to the kit: {len(missing)} {missing}")
print(f"over the 2025-26 league maximum: {over_max}; over their own 2025-26 total: {over_own}")
print()
print("player | deck rank | value / market rank (Version 64) | team today | 2025-26 | our points | outside | label | budget | arrivals and returns on his team (20+ min) | other cells outside all three")
for row, c, k in sorted(above, key=lambda x: x[0]["deck_rank"]):
    L = last.get(k); prev = "no games" if L is None else f"{'/'.join(sorted(L['teams']))} {L['g']:.0f} g"
    b = "over league max" if team(k) in over_max else ("over own total" if team(k) in over_own else "under")
    others = "; ".join(x["text"] for x in row["cells"] if x["cat"] != "pts") or "none"
    v = V.get(k, {}); vm = f"{v.get('valRank')} / {v.get('mktRank') or 'unpriced'}"
    print(f"{row['player']} | {row['deck_rank']} | {vm} | {kit[k]['team']} | {prev} | {c['ours']:g} | {c['lo']:g}-{c['hi']:g} | {label(k, 20)} | {b} | "
          f"{'; '.join(arrivals(k, 20)) or '-'} | {others}")
print()
for MIN in (20, 25):
    for lab, S in (("above", above), ("below", below)):
        cnt = {}
        for row, c, k in S: cnt[label(k, MIN)] = cnt.get(label(k, MIN), 0) + 1
        ob = sum(team(k) in over_max for row, c, k in S)
        print(f"labels at {MIN}+ minutes, points {lab} all three ({len(S)}): " + ", ".join(f"{a} {cnt.get(a, 0)}" for a in ("moved", "no 2025-26 games", "stayed, arrivals", "stayed, none")) + f"; on the seven over-max teams {ob}")
print()
print("points below all three (deck rank, team, label at 20+):")
print("; ".join(f"{row['player']} ({row['deck_rank']}, {kit[k]['team']}, {label(k, 20)}, {c['ours']:g} vs {c['lo']:g}-{c['hi']:g})" for row, c, k in sorted(below, key=lambda x: x[0]["deck_rank"])))
by_team = {}
for row, c, k in above: by_team[kit[k]["team"]] = by_team.get(kit[k]["team"], 0) + 1
print("points above all three, by team today: " + ", ".join(f"{t} {n}" for t, n in sorted(by_team.items(), key=lambda x: (-x[1], x[0]))))
bud = [("over the league max" if team(k) in over_max else "over its own total" if team(k) in over_own else "under both") for row, c, k in above]
print("points above all three, by team budget: " + ", ".join(f"{b} {bud.count(b)}" for b in ("over the league max", "over its own total", "under both")))
gap = [(V[k]["mktRank"] or 999) - V[k]["valRank"] for row, c, k in above]
print(f"of the {len(above)}, ranked above their market price on the live page: {sum(g > 0 for g in gap)}; by 25 or more places: {sum(g >= 25 for g in gap)}; below it: {sum(g < 0 for g in gap)}")
print()
teams = sorted({team(k) for k in kit if kit[k]["team"] != "FA"})
for MIN in (20, 25, 30):
    have = [t for t in teams if any(arrivals(k, MIN) for k in kit if team(k) == t)]
    print(f"teams whose kit pool holds an arrival or return at {MIN}+ minutes: {len(have)} of {len(teams)}; without: {sorted(set(teams) - set(have))}")
