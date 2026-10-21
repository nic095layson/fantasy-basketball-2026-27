#!/usr/bin/env python3
"""Owner 2026-10-19: "retro-run our draft again. Knowing what the red team found, would the card's suggested players
have changed? What would've been the draft changes? Try and stay as close to the real draft as drafted, but I want
to know how much better % we could have been in championship probability."

Red-team findings applied (post-mortem 2026-10-19): the card's ECW ignores the shared games shock, overstating
counting-category edges (here: a shock-aware ECW inflates the counting-cat variance by shock^2 (mu_a^2 + mu_b^2),
exactly what the simulator draws); the judge is the shipped engine (17 weeks, reseeded bracket), not the draft-grade
engine; every title figure carries its Monte-Carlo SE and the shock band (0 / 0.12).

Stages (all from the deck's records; the card is live_retro.card(), an exact port of the page's decwScores):
  screen   per owner turn, the card both ways (plain / shock-aware), and every legal alternative scored against the
           final rosters both ways (pairwise swap when a later seat took the alternative)
  sim      the union of the top-3 alternatives by each screen, swapped in pairwise, 10,000 seasons x seeds 2026/2027
  band     the swaps that clear the noise line on both seeds, re-run at shock 0 and 0.12 (6,000 seasons x 2 seeds)
  board    the close-to-real board (your pick kept unless one alternative clears +NL on both seeds and stays positive
           across the band), the §11 ceiling board, and the as-drafted baseline, all on the shipped engine
Writes retro_redteam.json."""
import importlib, json, math, os, random, statistics, subprocess, sys
from concurrent.futures import ProcessPoolExecutor
H = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(os.path.dirname(os.path.dirname(H)))
DECK = os.path.abspath(os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball"))
sys.path.insert(0, DECK + "/scripts"); sys.path.insert(0, DECK + "/arena"); sys.path.insert(0, DECK + "/arena/mocks")
import hoops, arena
SEEDS = (2026, 2027); SEASONS = 10000; BAND_SEASONS = 6000; NL = 0.5; TOPK = 3; SLOT = 10; BAND = (0.0, 0.12)
POOL = f"{DECK}/arena/results/players_v69.csv"; STATE = f"{DECK}/arena/data/states/draft_state_100.json"
# 2026-10-21 (owner "implement fixes", decision 5 (a)): pinned by design to the _w17r references of the 0.60-recovery
# engine this retro studied; the live engine's references are the _w17r_av0 files (deck #128).
REF = {sd: f"{DECK}/arena/results/m100_league_sim_10k_s{sd}_w17r.json" for sd in SEEDS}
hoops.DATA_PATH = POOL
P = hoops.zscores(hoops.load_players()); BY = {p["player"]: p for p in P}
ST = json.load(open(STATE, encoding="utf-8")); PICKS = ST["picks"]
OWNER_IDX = [i for i, pk in enumerate(PICKS) if pk["slot"] == SLOT]
CATS = hoops.CATS; COUNTING = set(hoops.COUNT_COLS); SHOCK = arena.TEAM_WEEK_SHOCK
ENGINE = subprocess.check_output(["git", "-C", DECK, "rev-parse", "--short", "HEAD"]).decode().strip()
HIND = json.load(open(f"{DECK}/arena/results/m100_hindsight.json", encoding="utf-8"))
RETRO11 = json.load(open(f"{KIT}/report/after-reports/draft-league-2026-10-14/retro_picks.json", encoding="utf-8"))
# the deck's card, byte-for-byte the page's rule (D-CAST-4 priced-only card from round CARD_PRICED_FROM)
import live_retro as LR  # noqa: E402  (module-level constants: MOCK etc. are read from its CLI defaults)


def pwin_cats(my, om, shock):
    out = {}
    for c in CATS:
        var = my[1][c] + om[1][c]
        if shock and c in COUNTING:
            var += shock * shock * (my[0][c] ** 2 + om[0][c] ** 2)
        d = (my[0][c] - om[0][c]) / (math.sqrt(var) or 1e-9)
        pr = 0.5 * (1 + math.erf(d / math.sqrt(2)))
        out[c] = (1 - pr) if c == "TO" else pr
    return out


def pwins(my, opps, shock):
    return sum(sum(pwin_cats(my, om, shock).values()) for om in opps) / len(opps)


def rosters_upto(upto):
    ros, taken = {s: [] for s in range(1, arena.TEAMS + 1)}, set()
    for pk in PICKS[:upto]:
        taken.add(pk["player"]); ros[pk["slot"]].append(BY[pk["player"]])
    return ros, taken


VETO = hoops.do_not_draft()  # JUDGMENT.doNotDraft on the lock page (owner 2026-09-28): off the owner's candidate pool


def avail_pool(taken):
    return [p for p in P if p["player"] not in taken and hoops.availability(p) > 0 and p["player"] not in VETO]


def card(upto):
    """live_retro.card() with the ECW leg scored both ways (plain and shock-aware) from the same models; same pool
    rule (card_pool), same ds blend. Returns ((top5, ranks) plain, (top5, ranks) shock-aware)."""
    ros, taken = rosters_upto(upto)
    mine = ros[SLOT]; opp = [r for s, r in ros.items() if s != SLOT and r]
    pool = LR.card_pool(avail_pool(taken), upto)
    vals = [hoops.adj_value(p, ()) for p in pool]
    models = [arena.team_week_model(r) for r in opp]
    mym = arena.team_week_model(mine) if mine else None
    cand = [arena.team_week_model(mine + [p]) for p in pool]
    out = []
    for shock in (0.0, SHOCK):
        base = pwins(mym, models, shock) if mine else 0.0
        decw = [pwins(m, models, shock) - base for m in cand]
        pd, pv = LR.pct(decw), LR.pct(vals)
        ds = [0.5 * pd[i] + 0.5 * pv[i] for i in range(len(pool))]
        order = sorted(range(len(pool)), key=lambda i: (-ds[i], [-ord(ch) for ch in pool[i]["player"]]))
        out.append(([dict(n=pool[i]["player"], pos=pool[i]["pos"], ds=round(ds[i], 4), decw=round(decw[i], 4), val=round(vals[i], 3))
                     for i in order[:5]], {pool[i]["player"]: k + 1 for k, i in enumerate(order)}))
    return out[0], out[1]


def swap_models(ros_final, opp_models, order_idx, n, alt, actual):
    """Models for the owner's final roster with `alt` in place of `actual`, and the opponents' models with the one seat
    that drafted `alt` (if any) re-modelled holding `actual`. One or two team_week_model calls per alternative."""
    mine = [p for p in ros_final[SLOT] if p["player"] != actual] + [BY[alt]]
    j = order_idx.get(alt); opp = dict(opp_models)
    if j is not None and PICKS[j]["slot"] != SLOT:
        o = PICKS[j]["slot"]
        opp[o] = arena.team_week_model([p for p in ros_final[o] if p["player"] != alt] + [BY[actual]])
    return arena.team_week_model(mine), list(opp.values())


def screen():
    ros_final, _ = rosters_upto(len(PICKS)); order_idx = {pk["player"]: i for i, pk in enumerate(PICKS)}
    opp_models = {s: arena.team_week_model(r) for s, r in ros_final.items() if s != SLOT}
    opp0 = list(opp_models.values()); my0 = arena.team_week_model(ros_final[SLOT])
    base = {"plain": pwins(my0, opp0, 0.0), "shock": pwins(my0, opp0, SHOCK)}
    assert abs(base["plain"] - HIND["base_ecw"]) < 1e-6, (base, HIND["base_ecw"])
    turns = []
    for n in OWNER_IDX:
        actual = PICKS[n]["player"]
        later = {PICKS[m]["player"] for m in OWNER_IDX if m > n}
        (card_plain, rank_plain), (card_shock, rank_shock) = card(n)
        _, taken = rosters_upto(n)
        legal = [p["player"] for p in LR.card_pool(avail_pool(taken), n) if p["player"] != actual and p["player"] not in later]
        rows = []
        for nm in legal:
            my, opp = swap_models(ros_final, opp_models, order_idx, n, nm, actual)
            ep = pwins(my, opp, 0.0); es = pwins(my, opp, SHOCK)
            j = order_idx.get(nm)
            rows.append(dict(n=nm, pos=BY[nm]["pos"], team=BY[nm]["team"], gain_plain=round(ep - base["plain"], 4),
                             gain_shock=round(es - base["shock"], 4), drafted_at=(None if j is None else j + 1),
                             drafted_by_slot=(None if j is None else PICKS[j]["slot"]),
                             card_rank_plain=rank_plain.get(nm), card_rank_shock=rank_shock.get(nm)))
        top_plain = sorted(rows, key=lambda r: -r["gain_plain"])[:TOPK]
        top_shock = sorted(rows, key=lambda r: -r["gain_shock"])[:TOPK]
        hind_top = [a["n"] for a in next(t for t in HIND["turns"] if t["pick"] == n + 1)["top"][:TOPK]]
        assert [r["n"] for r in top_plain] == hind_top, (n + 1, [r["n"] for r in top_plain], hind_top)
        turns.append(dict(pick=n + 1, actual=actual, card_plain=card_plain, card_shock=card_shock,
                          actual_card_rank_plain=rank_plain.get(actual), actual_card_rank_shock=rank_shock.get(actual),
                          n_legal=len(rows), n_better_plain=sum(r["gain_plain"] > 0 for r in rows),
                          n_better_shock=sum(r["gain_shock"] > 0 for r in rows),
                          top_plain=top_plain, top_shock=top_shock,
                          candidates=sorted({r["n"] for r in top_plain + top_shock if r["gain_plain"] > 0 or r["gain_shock"] > 0})))
        print(f"  screened #{n + 1} ({len(rows)} legal)", flush=True)
    return base, turns


def swap_picks(picks, n, alt):
    picks = [dict(pk) for pk in picks]; mine = picks[n]["player"]
    j = next((i for i, pk in enumerate(picks) if pk["player"] == alt), None)
    picks[n]["player"] = alt
    if j is not None: picks[j]["player"] = mine
    return picks


def sim_job(args):
    """One season run on the shipped engine (arena.simulate_seasons; league_sim.py is verified equal to it), with the
    shock patched for band runs. Each job reloads arena so a patch cannot leak between jobs sharing a worker."""
    key, picks, sd, seasons, shock = args
    import importlib as il, arena as ar
    il.reload(ar)
    if shock is not None: ar.TEAM_WEEK_SHOCK = shock
    ros = {s: [] for s in range(1, ar.TEAMS + 1)}
    for pk in picks: ros[pk["slot"]].append(BY[pk["player"]])
    champ, po = ar.simulate_seasons(ros, seasons, random.Random(sd))
    return key, sd, shock, 100 * champ[SLOT] / seasons, 100 * po[SLOT] / seasons


if __name__ == "__main__":
    base_ecw, turns = screen()
    print(f"base ECW plain {base_ecw['plain']:.4f} shock-aware {base_ecw['shock']:.4f}")
    for t in turns:
        print(f"#{t['pick']:>3} {t['actual']:<22} card plain #1 {t['card_plain'][0]['n']:<22} shock #1 {t['card_shock'][0]['n']:<22} "
              f"better {t['n_better_plain']:>3}/{t['n_better_shock']:>3} of {t['n_legal']}  cands {t['candidates']}")
    # --- sim: baseline + every candidate swap, 10k x 2 seeds
    jobs = [("base", PICKS, sd, SEASONS, None) for sd in SEEDS]
    for t in turns:
        for alt in t["candidates"]:
            for sd in SEEDS:
                jobs.append((f"{t['pick']}::{alt}", swap_picks(PICKS, t["pick"] - 1, alt), sd, SEASONS, None))
    print(f"sim jobs {len(jobs)} ({len(jobs)//2} boards x 2 seeds, {SEASONS:,} seasons)")
    with ProcessPoolExecutor(4) as ex: R = list(ex.map(sim_job, jobs))
    got = {}
    for key, sd, _, c, p in R: got.setdefault(key, {})[sd] = dict(title=round(c, 2), playoff=round(p, 2))
    ref = {sd: json.load(open(REF[sd]))["teams"][str(SLOT)]["champ"] for sd in SEEDS}
    se = math.sqrt(0.21 * 0.79 / SEASONS) * 100
    base_ok = {sd: abs(got["base"][sd]["title"] - ref[sd]) < 3 * se for sd in SEEDS}
    assert all(base_ok.values()), (got["base"], ref, se)
    base = {sd: got["base"][sd]["title"] for sd in SEEDS}
    swaps = []
    for t in turns:
        for alt in t["candidates"]:
            r = got[f"{t['pick']}::{alt}"]; d = {sd: round(r[sd]["title"] - base[sd], 2) for sd in SEEDS}
            row = next(x for x in t["top_plain"] + t["top_shock"] if x["n"] == alt)
            swaps.append(dict(pick=t["pick"], owner=t["actual"], alt=alt, pos=row["pos"], drafted_at=row["drafted_at"],
                              drafted_by_slot=row["drafted_by_slot"], gain_plain=row["gain_plain"], gain_shock=row["gain_shock"],
                              in_top_plain=alt in [x["n"] for x in t["top_plain"]], in_top_shock=alt in [x["n"] for x in t["top_shock"]],
                              card_rank_plain=row["card_rank_plain"], card_rank_shock=row["card_rank_shock"],
                              title={sd: r[sd]["title"] for sd in SEEDS}, d_title=d, d_title_mean=round(sum(d.values()) / 2, 2),
                              clears_nl=all(v > NL for v in d.values())))
    # --- band: swaps clearing the noise line, at shock 0 and 0.12
    cand = [s for s in swaps if s["clears_nl"]]
    bjobs = [("base", PICKS, sd, BAND_SEASONS, sh) for sd in SEEDS for sh in BAND]
    for s in cand:
        for sd in SEEDS:
            for sh in BAND:
                bjobs.append((f"{s['pick']}::{s['alt']}", swap_picks(PICKS, s["pick"] - 1, s["alt"]), sd, BAND_SEASONS, sh))
    print(f"band jobs {len(bjobs)}")
    with ProcessPoolExecutor(4) as ex: RB = list(ex.map(sim_job, bjobs))
    bgot = {}
    for key, sd, sh, c, p in RB: bgot.setdefault(key, {}).setdefault(str(sh), {})[sd] = round(c, 2)
    for s in cand:
        s["band"] = {sh: {sd: round(bgot[f"{s['pick']}::{s['alt']}"][sh][sd] - bgot["base"][sh][sd], 2) for sd in SEEDS} for sh in bgot["base"]}
        s["robust"] = all(v > 0 for sh in s["band"] for v in s["band"][sh].values())
    # --- boards: close-to-real (best robust swap per turn, in pick order, each alternative used once), §11 ceiling, baseline
    used, close, picks = set(), [], [dict(pk) for pk in PICKS]
    for t in turns:
        c = [s for s in cand if s["pick"] == t["pick"] and s.get("robust") and s["alt"] not in used]
        if not c: continue
        b = max(c, key=lambda s: s["d_title_mean"]); used.add(b["alt"])
        picks = swap_picks(picks, t["pick"] - 1, b["alt"]); close.append(dict(pick=t["pick"], owner=b["owner"], alt=b["alt"], d_title_mean=b["d_title_mean"]))
    c11 = [dict(pk) for pk in PICKS]
    for s in RETRO11["ceiling"]["swaps"]: c11 = swap_picks(c11, s["pick"] - 1, s["alt"])
    boards = {"close_to_real": picks, "ceiling_s11_on_shipped_engine": c11}
    jobs = [(k, b, sd, SEASONS, None) for k, b in boards.items() for sd in SEEDS]
    jobs += [(k, b, sd, BAND_SEASONS, sh) for k, b in boards.items() for sd in SEEDS for sh in BAND]
    with ProcessPoolExecutor(4) as ex: RR = list(ex.map(sim_job, jobs))
    bres = {}
    for key, sd, sh, c, p in RR: bres.setdefault(key, {}).setdefault("shipped" if sh is None else str(sh), {})[sd] = dict(title=round(c, 2), playoff=round(p, 2))
    out = dict(engine_commit=ENGINE, pool="players_v69.csv", state="draft_state_100.json", seat=SLOT, seeds=list(SEEDS), seasons=SEASONS,
               band_seasons=BAND_SEASONS, band_shocks=list(BAND), shock_shipped=SHOCK, noise_line=NL, topk=TOPK, mc_se_points=round(se, 3),
               reference_10k=ref, baseline=got["base"], baseline_within_3se=base_ok, base_ecw=base_ecw,
               base_band={sh: bgot["base"][sh] for sh in bgot["base"]}, turns=turns, swaps=swaps,
               close_to_real=dict(swaps=close, result=bres["close_to_real"]),
               ceiling_s11=dict(swaps=RETRO11["ceiling"]["swaps"], old_engine_title=RETRO11["ceiling"]["title"], result=bres["ceiling_s11_on_shipped_engine"]),
               retro11_base_title=RETRO11["base_title"])
    json.dump(out, open(os.path.join(H, "retro_redteam.json"), "w"), indent=1, ensure_ascii=False)
    print("baseline", got["base"], "ref", ref, "within 3 SE", base_ok)
    for s in swaps:
        print(f"#{s['pick']:>3} {s['owner']:<20} -> {s['alt']:<22} dECW plain {s['gain_plain']:+.3f} shock {s['gain_shock']:+.3f}  dTitle {s['d_title'][2026]:+.2f}/{s['d_title'][2027]:+.2f}  band {s.get('band')}  robust {s.get('robust')}")
    print("close-to-real:", close, bres["close_to_real"])
    print("ceiling §11 on shipped engine:", bres["ceiling_s11_on_shipped_engine"])
