#!/usr/bin/env python3
"""The draft check (owner 2026-11-11: "implement this with updating tables every Monday, and include this on the
season deck replacing the Movers tab"). One dated record per Monday that sets the draft-day system beside the season
so far, in five tables:

  picks      the owner's 13 draft picks: draft-day value against per-game value so far, with games played
  preferred  the turns where the draft card's first choice was another player, both graded the same way
  teams      the draft-day simulation's title share and rank beside Yahoo's standings
  cats       the owner's draft-day chance of winning each category in a week beside the weeks actually won
  scatter    every pool player with MIN_GAMES+ games: draft-day value against value so far, with the rank agreement

Display only. It reads the locked draft-day lines and the draft's own records in the deck repository, the kit's box
scores, weekly finals and the pinned Yahoo pull; it changes no line, tag, roster or constant, and nothing in the
engine reads it. A record is never rewritten (a second run for the same Monday is refused unless --force).

Value: the nine-category z-score sum of hoops.py (league percentage baselines weighted by attempts, percentage
impact = (rate - league rate) x attempts, population standard deviation, turnovers sign-flipped, the top-TOP_N fixed
point), fitted once on the draft-day lines and then applied unchanged to each player's per-game line so far, so the
two columns are on one scale. Window: every box-score day from SEASON_START to the day before --date.

    python3 scripts/draft_check.py --date 2026-11-09
Prints 'DRAFT CHECK: PASS — ...' (exit 0) or 'DRAFT CHECK: HALT — <why>' (exit 1).
"""
import argparse
import collections
import csv
import datetime as dt
import glob
import hashlib
import json
import os
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
DECK = os.path.abspath(os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball"))
OUT_DIR = os.path.join(KIT, "report", "draft_check")
OWNER_SEAT = 10
SEASON_START = "2026-10-20"
TOP_N = 156          # hoops.py's fixed point: 12 teams x 13 roster spots
MIN_GAMES = 5        # a player needs this many games to enter the scatter and the actual ranks
SIM_SEEDS = (2026, 2027)
STATS = ("fg_pct", "fga", "ft_pct", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov")
CATS = ("FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO")


class DraftCheckError(Exception):
    pass


def fold(s):
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).lower()
    for a in (".", "'", "’"):
        s = s.replace(a, "")
    for suf in (" jr", " sr", " iii", " ii", " iv"):
        if s.endswith(suf):
            s = s[: -len(suf)]
    return " ".join(s.split())


def default_paths(date):
    res = os.path.join(DECK, "arena", "results")
    return dict(lines=os.path.join(res, "players_v69.csv"),
                card=os.path.join(res, "m100_deckcard_v69.json"),
                sims=[os.path.join(res, f"m100_league_sim_10k_s{s}_w17r.json") for s in SIM_SEEDS],
                actuals=os.path.join(KIT, "data", "actuals"),
                weeks=os.path.join(KIT, "data", "weeks"),
                league_state=os.path.join(KIT, "data", "league_state.json"),
                pull=os.path.join(KIT, "data", "source", "flaim", f"pull_{date}.json"))


def read_lines(path):
    out = {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out[fold(r["player"])] = dict({k: float(r[k]) for k in STATS}, name=r["player"])
    return out


def _raw(p, lf, lt):
    return [(p["fg_pct"] - lf) * p["fga"], (p["ft_pct"] - lt) * p["fta"], p["tpm"], p["pts"], p["reb"], p["ast"],
            p["stl"], p["blk"], -p["tov"]]


def fit_scale(pool, top_n=TOP_N, rounds=8):
    """The value function fitted on the draft-day pool: returns value(line) -> float."""
    pool = list(pool)
    if len(pool) < 2:
        raise DraftCheckError("the draft-day pool has fewer than 2 players")
    cur = pool
    for _ in range(rounds):
        fga, fta = sum(p["fga"] for p in cur), sum(p["fta"] for p in cur)
        lf = sum(p["fg_pct"] * p["fga"] for p in cur) / fga
        lt = sum(p["ft_pct"] * p["fta"] for p in cur) / fta
        rows = [_raw(p, lf, lt) for p in cur]
        mu = [statistics.mean(c) for c in zip(*rows)]
        sd = [statistics.pstdev(c) or 1.0 for c in zip(*rows)]

        def value(p, lf=lf, lt=lt, mu=mu, sd=sd):
            return sum((x - m) / s for x, m, s in zip(_raw(p, lf, lt), mu, sd))
        nxt = sorted(pool, key=lambda p: -value(p))[:top_n]
        if {id(p) for p in nxt} == {id(p) for p in cur}:
            break
        cur = nxt
    return value


def season_lines(actuals_dir, as_of, start=SEASON_START):
    """Per-game lines from the box scores, start <= day < as_of: {folded name: (line, games, team games)}, days."""
    tot = collections.defaultdict(collections.Counter)
    team_games, team_of, days = collections.Counter(), {}, []
    for f in sorted(glob.glob(os.path.join(actuals_dir, "20??-??-??.json"))):
        day = os.path.basename(f)[:10]
        if not (start <= day < as_of):
            continue
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        seen = set()
        for p in d.get("players", []):
            seen.add((p["team"], p["game"]))
            if p.get("dnp") or not p.get("min"):
                continue
            k = fold(p.get("pool_name") or p["name"])
            c = tot[k]
            c["g"] += 1
            team_of[k] = p["team"]
            for s in ("pts", "fgm", "fga", "ftm", "fta", "tpm", "reb", "ast", "stl", "blk", "tov"):
                c[s] += p.get(s) or 0
        for t, _ in seen:
            team_games[t] += 1
        if seen:
            days.append(day)
    out = {}
    for k, c in tot.items():
        g = c["g"]
        line = dict(fg_pct=c["fgm"] / c["fga"] if c["fga"] else 0.0, fga=c["fga"] / g,
                    ft_pct=c["ftm"] / c["fta"] if c["fta"] else 0.0, fta=c["fta"] / g,
                    **{s: c[s] / g for s in ("tpm", "pts", "reb", "ast", "stl", "blk", "tov")})
        out[k] = (line, g, team_games[team_of[k]])
    return out, days


def spearman(xs, ys):
    n = len(xs)
    if n < 3:
        return None

    def ranks(v):
        order = sorted(range(n), key=lambda i: v[i])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2.0
            i = j + 1
        return r
    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return round(sum((a - mx) * (b - my) for a, b in zip(rx, ry)) / den, 3) if den else None


def build(date, paths):
    for k in ("lines", "card", "league_state", "pull"):
        if not os.path.exists(paths[k]):
            raise DraftCheckError(f"missing {k}: {os.path.relpath(paths[k], KIT)}")
    for p in paths["sims"]:
        if not os.path.exists(p):
            raise DraftCheckError(f"missing draft-day simulation: {os.path.relpath(p, KIT)}")
    pre = read_lines(paths["lines"])
    value = fit_scale(pre.values())
    actual, days = season_lines(paths["actuals"], date)
    if not days:
        raise DraftCheckError(f"no box-score day between {SEASON_START} and {date}")
    pre_val = {k: value(p) for k, p in pre.items()}
    pre_rank = {k: i + 1 for i, (k, _) in enumerate(sorted(pre_val.items(), key=lambda kv: -kv[1]))}
    act_val = {k: value(line) for k, (line, g, tg) in actual.items() if k in pre}
    ranked = sorted(((k, v) for k, v in act_val.items() if actual[k][1] >= MIN_GAMES), key=lambda kv: -kv[1])
    act_rank = {k: i + 1 for i, (k, _) in enumerate(ranked)}

    def row(name):
        k = fold(name)
        line, g, tg = actual.get(k, (None, 0, None))
        return dict(name=name, pre=round(pre_val[k], 2) if k in pre_val else None, pre_rank=pre_rank.get(k),
                    act=round(act_val[k], 2) if k in act_val else None, act_rank=act_rank.get(k), games=g,
                    team_games=tg)

    card = json.load(open(paths["card"], encoding="utf-8"))
    picks, preferred = [], []
    for turn in card:
        mine = dict(row(turn["actual"]), pick=turn["pick"])
        picks.append(mine)
        target = next((r["n"] for r in turn.get("rows", []) if r.get("target")), None)
        if target and fold(target) != fold(turn["actual"]):
            preferred.append(dict(pick=turn["pick"], mine=row(turn["actual"]), card=row(target)))
    if not picks:
        raise DraftCheckError("the draft card lists no turn")

    # teams: the draft-day simulation beside Yahoo's standings
    state = json.load(open(paths["league_state"], encoding="utf-8"))
    seat_of = {t["name"]: t["seat"] for t in state["teams"]}
    sims = [json.load(open(p, encoding="utf-8"))["teams"] for p in paths["sims"]]
    title = {int(s): round(sum(sim[s]["champ"] for sim in sims) / len(sims), 1) for s in sims[0]}
    title_rank = {s: i + 1 for i, (s, _) in enumerate(sorted(title.items(), key=lambda kv: (-kv[1], kv[0])))}
    pull = json.load(open(paths["pull"], encoding="utf-8"))
    table = ((pull.get("standings") or {}).get("standings")) or []
    if not table:
        raise DraftCheckError(f"{os.path.relpath(paths['pull'], KIT)} carries no standings")
    teams = []
    for t in table:
        if t["name"] not in seat_of:
            raise DraftCheckError(f"standings team not in the league state: {t['name']}")
        s = seat_of[t["name"]]
        teams.append(dict(name=t["name"], seat=s, mine=s == OWNER_SEAT, rank=int(t["rank"]), wins=int(t["wins"]),
                          losses=int(t["losses"]), ties=int(t["ties"]), pre_title=title[s], pre_rank=title_rank[s]))
    teams.sort(key=lambda t: t["rank"])
    team_rho = spearman([t["pre_rank"] for t in teams], [t["rank"] for t in teams])

    # cats: the owner's planned weekly win chance beside the weeks won
    plan = {c: round(sum(sim[str(OWNER_SEAT)]["cat_win_pct"][c] for sim in sims) / len(sims), 1) for c in CATS}
    rec = {c: [0, 0, 0] for c in CATS}
    weeks = []
    for f in sorted(glob.glob(os.path.join(paths["weeks"], "week_*.json"))):
        w = json.load(open(f, encoding="utf-8"))
        o = w.get("owner") or {}
        if "won" not in o:
            continue
        weeks.append(w["week"])
        for i, key in enumerate(("won", "lost", "tied")):
            for c in o.get(key, []):
                rec[c][i] += 1
    cats = [dict(cat=c, plan=plan[c], won=rec[c][0], lost=rec[c][1], tied=rec[c][2]) for c in CATS]

    mine = {fold(p["name"]) for p in picks}
    scatter = [dict(name=pre[k]["name"], pre=round(pre_val[k], 2), act=round(v, 2), games=actual[k][1],
                    mine=k in mine) for k, v in ranked]
    sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
    return dict(date=date, window=[days[0], days[-1]], days=len(days), min_games=MIN_GAMES, top_n=TOP_N,
                weeks_graded=sorted(weeks), picks=picks, preferred=preferred, teams=teams, team_rank_agreement=team_rho,
                cats=cats, scatter=scatter, rank_agreement=spearman([d["pre"] for d in scatter],
                                                                    [d["act"] for d in scatter]),
                sources={k: dict(path=os.path.relpath(p, KIT), sha256=sha(p))
                         for k, p in [("lines", paths["lines"]), ("card", paths["card"]), ("pull", paths["pull"])]
                         + [(f"sim_{s}", p) for s, p in zip(SIM_SEEDS, paths["sims"])]},
                method="value = nine-category z-score sum fitted on the draft-day lines (top %d fixed point) and "
                       "applied unchanged to the per-game line so far; display only" % TOP_N)


def pass_line(rec):
    me = next((t for t in rec["teams"] if t["mine"]), None)
    return (f"DRAFT CHECK: PASS — {rec['date']}: box scores {rec['window'][0]} to {rec['window'][1]} ({rec['days']} days), "
            f"{len(rec['picks'])} picks, {len(rec['scatter'])} players with {rec['min_games']}+ games, rank agreement "
            f"{rec['rank_agreement']}"
            + (f"; you were ranked {me['pre_rank']} on draft day and stand {me['rank']} ({me['wins']}-{me['losses']}-{me['ties']})" if me else ""))


def latest(date, out_dir=None):
    """The newest record dated on or before `date`, or None (the deck reads this)."""
    out_dir = out_dir or OUT_DIR
    best = None
    for f in sorted(glob.glob(os.path.join(out_dir, "draft_check_20??-??-??.json"))):
        if os.path.basename(f)[12:22] <= date:
            best = f
    return best


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=dt.datetime.utcnow().strftime("%Y-%m-%d"),
                    help="the record's date (a Monday in the morning run); box scores before it are counted")
    ap.add_argument("--out", default=OUT_DIR)
    ap.add_argument("--force", action="store_true", help="rewrite an existing record for this date")
    a = ap.parse_args()
    out = os.path.join(a.out, f"draft_check_{a.date}.json")
    if os.path.exists(out) and not a.force:
        print(f"DRAFT CHECK: PASS — {a.date}: the record exists and is not rewritten ({os.path.relpath(out, KIT)})")
        return 0
    try:
        rec = build(a.date, default_paths(a.date))
    except DraftCheckError as e:
        print(f"DRAFT CHECK: HALT — {e}")
        return 1
    os.makedirs(a.out, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(pass_line(rec))
    return 0


if __name__ == "__main__":
    sys.exit(main())
