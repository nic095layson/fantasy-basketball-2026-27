#!/usr/bin/env python3
"""Owner research 2026-10-14: "Assuming I take Haliburton at 10, build a roster with my remaining picks, using players who
are historically available at each pick (based on the average of the previous live mock drafts we have conducted)."

Rooms: every live public Yahoo room on file drafted from seat 10 (arena/data/states/draft_state_<m>.json for the mocks
below; cast rooms against the modeled league-mates are excluded — bots, not people). Lines: Version 68
(arena/results/players_v68.csv). Stated to the owner before the run.

  availability(p, N) = share of rooms in which no OPPONENT (seat != 10) took p before overall pick N. The owner's own
                       earlier picks in a room do not remove a player: the plan picks differently.
  gain(p | my, N)    = the deck's own weekly model (arena.team_week_model; live_retro.pwins): expected categories won per
                       week by my roster + p against that room's opponent rosters at pick N, minus the same without p,
                       averaged over the rooms where p is still there.
  tiers              = likely (there in >= 65% of rooms), coin flip (35-65%), reach (< 35%).
  plan               = Haliburton at #10, then at each owner pick the likely-tier player with the largest gain whose
                       addition leaves the eight positional slots fillable with the picks left (hoops.POSITIONAL_SLOTS).
  replay             = the plan dropped into every room in the owner's seat where Haliburton was there at #10 (a room where
                       an opponent took him earlier is counted, not graded): at each turn the plan player if an opponent
                       has not taken him, else the next name on that turn's list (likely, then coin flip, then reach) that
                       is still there; a player the plan takes that an opponent drafted later in that room goes to that
                       opponent's slot swapped for the owner's real pick (live_retro.apply_swaps logic). Graded on the real
                       eight-team bracket (live_retro.run_arm, 3 seeds x 6000 seasons) against the owner's real roster in
                       the same room, both on Version 68 lines.
Writes plan_2026-10-14.json beside this script. Deterministic (fixed seeds)."""
import json, math, os, sys
H = os.path.dirname(os.path.abspath(__file__))
DECK = "/home/user/yahoo-fantasy-basketball"
sys.path.insert(0, os.path.join(DECK, "scripts")); sys.path.insert(0, os.path.join(DECK, "arena"))
import hoops, arena, random
ROOMS = [52, 53, 54, 56, 57, 58, 59, 60, 61, 67, 68, 73, 74, 75, 77, 78, 79, 80]
RECENT = [74, 75, 77, 78, 79, 80]          # drafted 10/12 and later (Yahoo's prices moved through September)
SLOT, TEAMS = 10, 12
TURNS = [10, 15, 34, 39, 58, 63, 82, 87, 106, 111, 130, 135, 154]
LIKELY, COIN = 0.65, 0.35
SHOW = 6
NO_TITLE = "--no-title" in sys.argv

hoops.DATA_PATH = os.path.join(DECK, "arena", "results", "players_v68.csv")
POOL = hoops.zscores(hoops.load_players())
BY = {hoops.fold(p["player"]): p for p in POOL}
VETO = hoops.do_not_draft()   # the owner's DO NOT DRAFT list, read from the deck page (2026-09-28: Porzingis)
assert "Kristaps Porzingis" in VETO
LIVE = [p for p in POOL if hoops.availability(p) > 0 and p["player"] not in VETO]

def resolve(name):
    p = BY.get(hoops.fold(name))
    if p: return p["player"]
    c = hoops.match_candidates(POOL, name)
    return c[0]["player"] if len(c) == 1 else None

rooms, unmatched = {}, {}
for m in ROOMS:
    st = json.load(open(os.path.join(DECK, "arena", "data", "states", f"draft_state_{m}.json")))
    assert st["teams"] == TEAMS and st["slot"] == SLOT and len(st["picks"]) == 156, m
    picks = []
    for pk in st["picks"]:
        nm = resolve(pk["player"])
        if nm is None: unmatched.setdefault(m, []).append(pk["player"])
        picks.append({"player": nm or pk["player"], "slot": pk["slot"], "pool": nm is not None})
    rooms[m] = picks

def model(ros): return arena.team_week_model(ros)
def pwin_cats(my, om):
    out = {}
    for c in hoops.CATS:
        d = (my[0][c] - om[0][c]) / (math.sqrt(my[1][c] + om[1][c]) or 1e-9)
        pr = 0.5 * (1 + math.erf(d / math.sqrt(2)))
        out[c] = (1 - pr) if c == "TO" else pr
    return out
def pwins(my, opps): return sum(sum(pwin_cats(my, om).values()) for om in opps) / len(opps) if opps else 0.0

def room_state(m, n):
    """Opponent-taken names before overall pick n (1-based) and the opponent rosters' week models at that point."""
    taken, ros = set(), {s: [] for s in range(1, TEAMS + 1) if s != SLOT}
    for i, pk in enumerate(rooms[m][: n - 1]):
        if pk["slot"] != SLOT:
            taken.add(pk["player"])
            if pk["pool"]: ros[pk["slot"]].append(BY[hoops.fold(pk["player"])])
    return taken, [model(r) for r in ros.values() if r]

def fillable(ros, picks_left):
    match = {}
    def aug(si, seen):
        for pi, p in enumerate(ros):
            if pi in seen or not any(e in hoops.positions_of(p) for e in hoops.POSITIONAL_SLOTS[si][1]): continue
            seen.add(pi)
            if pi not in match or aug(match[pi], seen):
                match[pi] = si; return True
        return False
    open_ = sum(1 for si in range(len(hoops.POSITIONAL_SLOTS)) if not aug(si, set()))
    return open_ <= picks_left

STATES = {(m, n): room_state(m, n) for m in ROOMS for n in TURNS}

def build_plan(rset):
    """The plan and each turn's ranked lists from the rooms in `rset` only."""
    me = [BY[hoops.fold("Tyrese Haliburton")]]
    turns_out, plan = [], [(10, "Tyrese Haliburton")]
    rec_set = [m for m in RECENT if m in rset]
    for k, n in enumerate(TURNS[1:], start=1):
        left = len(TURNS) - k - 1
        base = {m: pwins(model(me), STATES[(m, n)][1]) for m in rset}
        rows = []
        for p in LIVE:
            if p in me: continue
            there = [m for m in rset if p["player"] not in STATES[(m, n)][0]]
            if not there: continue
            a = len(there) / len(rset)
            rec = [m for m in rec_set if p["player"] not in STATES[(m, n)][0]]
            mm = model(me + [p])
            g = sum(pwins(mm, STATES[(m, n)][1]) - base[m] for m in there) / len(there)
            rows.append(dict(n=p["player"], team=p["team"], pos="/".join(hoops.positions_of(p)), avail=round(a, 3),
                             avail_recent=round(len(rec) / len(rec_set), 3) if rec_set else None, gain=round(g, 4),
                             tier="likely" if a >= LIKELY else ("coin" if a >= COIN else "reach"),
                             fits=fillable(me + [p], left)))
        rows.sort(key=lambda r: (-r["gain"], r["n"]))
        pick = next(r for r in rows if r["tier"] == "likely" and r["fits"])
        order = [r["n"] for t in ("likely", "coin", "reach") for r in rows if r["tier"] == t and r["fits"]]
        turns_out.append(dict(pick=n, plan=pick["n"], order=order,
                              likely=[r for r in rows if r["tier"] == "likely"][:SHOW],
                              coin=[r for r in rows if r["tier"] == "coin"][:SHOW],
                              reach=[r for r in rows if r["tier"] == "reach"][:SHOW]))
        me.append(BY[hoops.fold(pick["n"])]); plan.append((n, pick["n"]))
    return plan, turns_out

plan, turns_out = build_plan(ROOMS)
print("plan:", "; ".join(f"#{n} {p}" for n, p in plan), flush=True)

# ---- replay the plan in every room, and grade it against the owner's real roster there (Version 68 lines)
def run_arm(rosters, seeds=(11, 23, 47), seasons=6000):
    champs = {s: 0 for s in rosters}; plays = {s: 0 for s in rosters}
    for sd in seeds:
        c, p = arena.simulate_seasons(rosters, seasons, random.Random(sd))
        for s in rosters: champs[s] += c[s]; plays[s] += p[s]
    tot = seasons * len(seeds)
    return {s: (100 * champs[s] / tot, 100 * plays[s] / tot) for s in rosters}

def finals(picks):
    ros = {s: [] for s in range(1, TEAMS + 1)}
    for pk in picks:
        if pk["pool"]: ros[pk["slot"]].append(BY[hoops.fold(pk["player"])])
    return ros

# the premise: Haliburton at #10. A room where an opponent took him before #10 cannot host the plan; it is counted, not graded.
hali_gone = [m for m in ROOMS if "Tyrese Haliburton" in STATES[(m, 10)][0]]
replay = []
for m in [r for r in ROOMS if r not in hali_gone]:
    # leave-one-out: the plan graded in room m is built from the other rooms only (an in-sample plan would be graded on
    # the rooms it was fitted to)
    lplan, lturns = build_plan([r for r in ROOMS if r != m])
    lists = {t["pick"]: t["order"] for t in lturns}; lists[10] = ["Tyrese Haliburton"]
    picks = [dict(pk) for pk in rooms[m]]
    mine, subs = [], []
    for n in TURNS:
        i = n - 1; assert picks[i]["slot"] == SLOT
        taken = {pk["player"] for pk in picks[:i] if pk["slot"] != SLOT}
        want = lplan[TURNS.index(n)][1]
        alt = next(x for x in [want] + lists[n] if x not in taken and x not in mine)
        if alt != want: subs.append((n, want, alt))
        actual, apool = picks[i]["player"], picks[i]["pool"]
        if alt != actual:
            # where alt sits on the running board now (never earlier than i: earlier opponents are excluded, earlier
            # owner slots hold plan picks); a later opponent who drafted him gets the displaced player instead
            j = next((k for k, pk in enumerate(picks) if pk["player"] == alt), None)
            assert j is None or j > i
            picks[i] = {"player": alt, "slot": SLOT, "pool": True}
            if j is not None:
                picks[j] = {"player": actual, "slot": picks[j]["slot"], "pool": apool}
        mine.append(alt)
    real, pl = finals(rooms[m]), finals(picks)
    ecw = lambda ros: pwins(model(ros[SLOT]), [model(r) for s, r in ros.items() if s != SLOT and r])
    rec = dict(mock=m, loo_plan=[p for _, p in lplan], plan_roster=mine, substitutions=subs, ecw_real=round(ecw(real), 3), ecw_plan=round(ecw(pl), 3),
               real_roster=[pk["player"] for pk in rooms[m] if pk["slot"] == SLOT])
    if not NO_TITLE:
        a, b = run_arm(real), run_arm(pl)
        rk = lambda res: 1 + sum(1 for s in res if s != SLOT and res[s][0] > res[SLOT][0])
        rec.update(title_real=round(a[SLOT][0], 2), title_plan=round(b[SLOT][0], 2), rank_real=rk(a), rank_plan=rk(b))
    replay.append(rec)
    print(m, rec["ecw_real"], rec["ecw_plan"], rec.get("title_real"), rec.get("title_plan"), len(subs), flush=True)

out = dict(rooms=ROOMS, recent=RECENT, haliburton_gone_before_10=hali_gone, pool="players_v68.csv", thresholds=dict(likely=LIKELY, coin=COIN),
           unmatched=unmatched, plan=plan, turns=turns_out, replay=replay)
json.dump(out, open(os.path.join(H, "plan_2026-10-14.json"), "w"), indent=1, ensure_ascii=False)
print("full-sample plan:", "; ".join(f"#{n} {p}" for n, p in plan))
