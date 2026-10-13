#!/usr/bin/env python3
"""DRY RUN — the WO-5b candidate the backtests support. Nothing in either repo is written.
Starts from the committed WO-5 lines (same minutes, same role moves, same returnee minutes, same steals/blocks anchor,
rookies untouched) and changes three things, each chosen by the 20-season backtests:
  H1  counting rates (FGA, FTA, 3PM, REB, AST, TOV) = half the base season's per-36 + half the games-weighted 5/4/3
      per-36 of the base season and the two before it, for a player with 3+ seasons on file before 2026-27; a player
      with fewer keeps his base season (history lags a young player's growth: the backtest's 1-2-season band).
  H2  FG% and FT% = the attempt-weighted 5/4/3 of the same three seasons (beat the one-third career shrink).
  U   usage fitted to the 2026-27 team: k = league usage capacity (2025-26, minutes-weighted FGA+0.44FTA+TOV per 36)
      / the team's demand (each rostered player's 2025-26 usage, shrunk toward the league on thin minutes, weighted by
      his projected 2026-27 minutes — ours for pool players, his 2025-26 minutes otherwise, the first-year median for
      rookies); FGA, FTA, 3PM, TOV scale by k**0.75 (alpha fit on 2006-16, judged on 2016-26). Points by the identity."""
import csv, json, sys, unicodedata, statistics as st
from collections import defaultdict
W = "/home/user/fantasy-basketball-2026-27/report/wo5"; D = "/home/user/yahoo-fantasy-basketball/data"
OUT = sys.argv[1]
ALPHA = 0.75
norm = lambda s: " ".join(t for t in unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().replace(".", "").replace("'", "").replace("-", " ").split() if t not in {"jr", "sr", "ii", "iii", "iv"})
B = list(csv.DictReader(open(W + "/data/bref_totals_2004-2026.csv", encoding="utf-8")))
seasons = sorted({r["season"] for r in B}); si = {s: i for i, s in enumerate(seasons)}; T26 = si["2025-26"]
F = ("g", "mp", "fg", "fga", "fg3", "ft", "fta", "trb", "ast", "stl", "blk", "tov", "pts")
tot = defaultdict(dict); name_pid = {}
for r in B:
    if r.get("row", "season") == "split": continue
    tot[r["pid"]][si[r["season"]]] = {k: float(r[k]) for k in F}
    name_pid.setdefault(norm(r["player"]), r["pid"])
def u36(d): return (d["fga"] + 0.44 * d["fta"] + d["tov"]) / d["mp"] * 36
ds26 = [tot[p][T26] for p in tot if T26 in tot[p] and tot[p][T26]["mp"] > 0]
CAP = sum(d["fga"] + 0.44 * d["fta"] + d["tov"] for d in ds26) / sum(d["mp"] for d in ds26) * 36
rook = [tot[p][T26] for p in tot if T26 in tot[p] and min(tot[p]) == T26 and tot[p][T26]["mp"] >= 250]
ROOK_U = st.median(u36(d) for d in rook); ROOK_MPG = st.median(d["mp"] / d["g"] for d in rook)
def usage_2526(pid):
    d = tot.get(pid, {}).get(T26)
    if not d or d["mp"] <= 0:
        prev = [s for s in tot.get(pid, {}) if tot[pid][s]["mp"] > 0]
        if not prev: return ROOK_U
        d = tot[pid][max(prev)]
    return (u36(d) * d["mp"] + CAP * 500) / (d["mp"] + 500)
L = json.load(open(W + "/out/lines_wo5_2026-10-12.json"))["rows"]
Lk = {r["key"]: r for r in L if r.get("new")}
rosters = json.load(open(D + "/rosters_official.json"))["teams"]
ESPN2 = {"BKN": "BKN", "CHA": "CHA", "GSW": "GSW", "NOP": "NOP", "NYK": "NYK", "PHX": "PHX", "SAS": "SAS", "UTA": "UTA", "WAS": "WAS"}
team_dem = {}; unmatched = []; team_rows = {}
for team, names in rosters.items():
    um = m = 0.0; rows = []
    for n in names:
        k = norm(n); line = Lk.get(k); pid = (line or {}).get("pid") or name_pid.get(k)
        if line and line["meta"].get("minutes"): mins = float(line["meta"]["minutes"]); src = "projected"
        elif pid and T26 in tot.get(pid, {}) and tot[pid][T26]["g"] > 0: mins = tot[pid][T26]["mp"] / tot[pid][T26]["g"]; src = "2025-26"
        else: mins = ROOK_MPG; src = "first-year median"
        if not pid and not line: unmatched.append((team, n))
        u = usage_2526(pid) if pid else ROOK_U
        um += u * mins; m += mins; rows.append((n, round(u, 2), round(mins, 1), src))
    team_dem[team] = um / m; team_rows[team] = rows
K = {t: CAP / d for t, d in team_dem.items()}
def m3(pid, base_i, key, att=None):
    """games-weighted 5/4/3 per-36 over base, base-1, base-2 (or attempt-weighted percentage when att is given)."""
    items = [(w, tot[pid][base_i - j]) for j, w in ((0, 5), (1, 4), (2, 3)) if (base_i - j) in tot[pid] and tot[pid][base_i - j]["mp"] > 0]
    if att:
        den = sum(w * d[att] for w, d in items); return sum(w * d[key] for w, d in items) / den if den > 0 else None
    den = sum(w * d["g"] for w, d in items); return sum(w * d["g"] * d[key] / d["mp"] * 36 for w, d in items) / den if den > 0 else None
CNT = {"fga": "fga", "fta": "fta", "tpm": "fg3", "reb": "trb", "ast": "ast", "tov": "tov"}
out = []
for key, r in Lk.items():
    meta = r["meta"]; base = meta.get("base", "")
    new = dict(r["new"])
    rec = dict(key=key, name=r["name"], team=r.get("team"), base=base, wo5=r["new"], changed=False)
    if base in si and r.get("pid") in tot:
        pid = r["pid"]; bi = si[base]; mins = float(meta["minutes"])
        nprior = sum(1 for s in tot[pid] if s <= bi and tot[pid][s]["mp"] > 0)   # seasons on file up to and including the base
        bd = tot[pid][bi]
        for c, col in CNT.items():
            r1 = bd[col] / bd["mp"] * 36
            rate = 0.5 * r1 + 0.5 * m3(pid, bi, col) if nprior >= 3 else r1
            new[c] = rate * mins / 36
        fg = m3(pid, bi, "fg", "fga"); ft = m3(pid, bi, "ft", "fta")
        if fg: new["fg_pct"] = fg
        if ft: new["ft_pct"] = ft
        team = r.get("team"); k = K.get(team)
        f = k ** ALPHA if k else 1.0
        for c in ("fga", "fta", "tpm", "tov"): new[c] *= f
        new["pts"] = 2 * new["fga"] * new["fg_pct"] + new["tpm"] + new["fta"] * new["ft_pct"]
        for c in new: new[c] = round(new[c], 3 if "pct" in c else 1)
        rec.update(changed=True, history="blend" if nprior >= 3 else "base season only", seasons_on_file=nprior, team_k=round(k, 3) if k else None, usage_factor=round(f, 3))
    rec["candidate"] = new; out.append(rec)
summary = dict(capacity_u36=round(CAP, 3), rookie_u36=round(ROOK_U, 2), rookie_mpg=round(ROOK_MPG, 1), alpha=ALPHA,
               team_k={t: round(v, 3) for t, v in sorted(K.items(), key=lambda x: x[1])}, roster_names=sum(len(v) for v in rosters.values()),
               unmatched_roster_names=len(unmatched), lines=len(out), changed=sum(1 for x in out if x["changed"]))
json.dump(dict(summary=summary, rows=out, team_rows=team_rows, unmatched=unmatched), open(OUT, "w"), indent=1, ensure_ascii=False)
print(json.dumps(summary, indent=1))
