#!/usr/bin/env python3
"""Co-GM library (Session 1 items 6-7): the league state as simulator rosters, the daily lineup,
games left this week, and the waiver scan. The waiver scoring is lifted, not rewritten, from
report/after-reports/draft-league-2026-10-14/waiver_moves.py (pwins on arena.team_week_model,
the 40 best undrafted by board value, every add x drop pair) and now reads the league state
instead of the draft board."""
import csv
import datetime
import json
import math
import os
import subprocess
import sys

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK = os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball")
for _p in (os.path.join(DECK, "scripts"), os.path.join(DECK, "arena")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import hoops  # noqa: E402
import arena  # noqa: E402

LINES_TAG = "v69"
STATE = os.path.join(KIT, "data", "league_state.json")
SCHEDULE = os.path.join(KIT, "data", "league_schedule.json")
GAMES = os.path.join(KIT, "report", "schedule", "games-2026-27.csv")
OWNER_SEAT = 10
TEAM_CODE = {"CHO": "CHA", "BRK": "BKN", "PHO": "PHX"}  # Basketball-Reference -> pool/Yahoo codes
SLOTS = [("PG", ("PG",)), ("SG", ("SG",)), ("G", ("PG", "SG")), ("SF", ("SF",)), ("PF", ("PF",)),
         ("F", ("SF", "PF")), ("C", ("C",)), ("C", ("C",)), ("Util", None), ("Util", None)]
WAIVER_CANDIDATES = 40  # inherited from waiver_moves.py; stated to the owner before the first run


def load_pool():
    """The preseason v69 pool, or the season pool when SEASON_POOL names a deck-schema CSV (in-season tool,
    2026-10-19: data/season/pool_season.csv from season_lines.py; the brief, preview and waiver scan then run on the
    blended lines and say so)."""
    hoops.DATA_PATH = os.environ.get("SEASON_POOL") or os.path.join(DECK, "arena", "results", f"players_{LINES_TAG}.csv")
    P = hoops.zscores(hoops.load_players())
    return P, {p["player"]: p for p in P}


def rosters(state, by, include_il=False):
    # owner 2026-10-20 (D-IS-8): an IL player counts as zero (absent from the simulation) until he is on the active roster
    out = {}
    for t in state["teams"]:
        out[t["seat"]] = [by[p["player"]] for p in t["players"] if include_il or p["slot"] != "IL"]
    return out


# ---------------------------------------------------------------- daily lineup
def daily_lineup(players):
    """Players: dicts with player, positions (Yahoo eligibility), value, availability.
    Starts as many as the ten slots allow, preferring higher value: players are added in value
    order and each may displace a lower-valued assignment only along an augmenting path
    (Kuhn's matching), so a flex star moves aside rather than strand a specialist. Out
    (availability 0) never starts. Returns ([(slot, player)], [benched])."""
    cand = sorted((p for p in players if p["availability"] > 0), key=lambda p: -p["value"])
    owner = [None] * len(SLOTS)

    def fits(p, i):
        el = SLOTS[i][1]
        return el is None or any(x in el for x in p["positions"])

    def place(k, seen):
        for i in range(len(SLOTS)):
            if i in seen or not fits(cand[k], i):
                continue
            seen.add(i)
            if owner[i] is None or place(owner[i], seen):
                owner[i] = k
                return True
        return False

    started = set()
    for k in range(len(cand)):
        if place(k, set()):
            started.add(k)
    lineup = [(SLOTS[i][0], cand[k]["player"]) for i, k in enumerate(owner) if k is not None]
    bench = [cand[k]["player"] for k in range(len(cand)) if k not in started]
    return lineup, bench


# ---------------------------------------------------------------- schedule
def load_games(path=GAMES):
    return [(r["date"], r["visitor"], r["home"]) for r in csv.DictReader(open(path, encoding="utf-8"))]


def games_left(games, start, end):
    left = {}
    for d, v, h in games:
        if start <= d <= end:
            for t in (v, h):
                t = TEAM_CODE.get(t, t)
                left[t] = left.get(t, 0) + 1
    return left


def week_of(date):
    """The Yahoo week containing `date` from the kit's calendar (build_schedule.weeks)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("build_schedule", os.path.join(KIT, "report", "schedule", "build_schedule.py"))
    bs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bs)
    d = datetime.date.fromisoformat(date)
    for n, s, e in bs.weeks():
        if s <= d <= e:
            return n, s.isoformat(), e.isoformat()
    raise ValueError(f"{date} is outside the 2026-27 fantasy calendar")


# ---------------------------------------------------------------- waiver scan (waiver_moves.py, lifted)
CATS = hoops.CATS


def _pcat(m, om, c):
    d = (m[0][c] - om[0][c]) / (math.sqrt(m[1][c] + om[1][c]) or 1e-9)
    pr = 0.5 * (1 + math.erf(d / math.sqrt(2)))
    return (1 - pr) if c == "TO" else pr


def pwins(my, opps):
    return sum(_pcat(my, om, c) for om in opps for c in CATS) / len(opps)


def free_agents(P, state, n=WAIVER_CANDIDATES):
    rostered = {p["player"] for t in state["teams"] for p in t["players"]}
    veto = hoops.do_not_draft()
    fa = [p for p in P if p["player"] not in rostered and hoops.availability(p) > 0 and p["player"] not in veto]
    return sorted(fa, key=lambda p: -hoops.adj_value(p, ()))[:n]


def waiver_pairs(ros, fa, owner=OWNER_SEAT):
    # the season tools run on arena.SEASON_CV, the per-game variation fitted to the 2025-26 game logs (D-ZS-3, owner
    # 2026-10-21 "Season tools only"); the draft engine's arena.CV stays frozen with the draft page
    cv = arena.SEASON_CV
    opp = [arena.team_week_model(r, cv) for s, r in ros.items() if s != owner]
    mine = ros[owner]
    base = pwins(arena.team_week_model(mine, cv), opp)
    pairs = []
    for a in fa:
        for d in mine:
            m = arena.team_week_model([x for x in mine if x is not d] + [a], cv)
            pairs.append({"add": a["player"], "add_team": a["team"], "drop": d["player"],
                          "d_ecw": round(pwins(m, opp) - base, 4)})
    pairs.sort(key=lambda x: -x["d_ecw"])
    return base, pairs


def streaming(candidates, drop_games, n=5):
    """Free agents worth a stream: more games left this week than the player they would replace,
    ranked by per-game board value (negative values rank too: below the pool mean is not zero)."""
    ok = [r for r in candidates if r["games_left"] > drop_games]
    return sorted(ok, key=lambda r: (-r["value_per_game"], -r["games_left"]))[:n]


# ---------------------------------------------------------------- simulator bridge
def sim_state(ros):
    return {"teams": len(ros), "picks": [{"slot": s, "player": p["player"]} for s, r in sorted(ros.items()) for p in r]}


def sim_pool_names(path=None):
    """The names the deck's season simulator can play: the pool it is given (SEASON_POOL, owner 2026-10-26), else its
    frozen players_<LINES_TAG>.csv."""
    with open(path or os.path.join(DECK, "arena", "results", f"players_{LINES_TAG}.csv"), encoding="utf-8") as f:
        return {r["player"] for r in csv.DictReader(f)}


def run_league_sim(ros, seed, seasons, workdir, tag="cur"):
    # 2026-10-21 (owner option (b), data/pool_additions.csv): a rostered pickup the simulator's frozen pool lacks is left
    # out of the simulation, as an IL player is (D-IS-8), and named in the record's absent_from_sim
    # 2026-10-26 (owner, "use the season pool"): with SEASON_POOL set the simulator plays that pool (league_sim --pool),
    # the lines the board plays with the pickups in them; unset, the frozen v69 pool as before
    pool = os.path.abspath(os.environ["SEASON_POOL"]) if os.environ.get("SEASON_POOL") else None
    known = sim_pool_names(pool)
    absent = sorted(p["player"] for r in ros.values() for p in r if p["player"] not in known)
    ros = {s: [p for p in r if p["player"] in known] for s, r in ros.items()}
    sp = os.path.join(workdir, f"_state_{tag}_{seed}.json")
    op = os.path.join(workdir, f"_sim_{tag}_{seed}.json")
    json.dump(sim_state(ros), open(sp, "w", encoding="utf-8"), ensure_ascii=False)
    subprocess.run([sys.executable, os.path.join(DECK, "arena", "mocks", "league_sim.py"), sp, LINES_TAG,
                    str(seasons), str(seed), op, "--schedule", SCHEDULE, "--season-cv"] + (["--pool", pool] if pool else []),
                   check=True, capture_output=True)
    rec = json.load(open(op, encoding="utf-8"))
    os.remove(sp)
    os.remove(op)
    rec["absent_from_sim"] = absent
    return rec
