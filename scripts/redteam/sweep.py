#!/usr/bin/env python3
"""Assumption sweep: the owner's title share under each hand-set engine constant, one at a time, on the league's
final rosters (post-mortem 2026-10-19 D-PM-1; the 10/19 red team's rt_sensitivity.py made standing).

The variants come from scripts/redteam/constants_registry.json: every constant with status declared_band carries
a 'band', the patches this script runs one at a time. A declared_band constant with no band is an error, never
a silent skip. The simulator is the deck's arena.simulate_seasons on the final rosters of the 10/14 league draft
(deck arena/data/states/draft_state_100.json, pool v69). Each job reloads arena so a patch cannot leak between
jobs sharing a worker; the baseline must land within 3 SE of the 10,000-season reference runs on both seeds.

Tiers (the post-mortem rule): mean shift over the seeds, ROBUST under 1 point, SENSITIVE 1 to 2, FRAGILE 2 or
more. A FRAGILE constant's band must be quoted by any report that quotes a title share (check_bands.py).

    python3 scripts/redteam/sweep.py --out report/.../sweep.json [--seasons 6000] [--seeds 2026 2027] [--workers 4]
"""
import argparse
import hashlib
import importlib
import inspect
import json
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(HERE))
DECK = os.path.abspath(os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball"))
REGISTRY = os.path.join(HERE, "constants_registry.json")
STATE = "arena/data/states/draft_state_100.json"
POOL = "arena/results/players_v69.csv"
# The 10k reference of the engine the sweep runs on (league_sim.py --verify, 17 weeks, reseeded). Regenerated when the
# engine moves the reference: _av0 = recovery and out-* at 0.0 (2026-10-21); _scv = the same on arena.SEASON_CV, the
# season tools' per-game variation fitted to the 2025-26 game logs (D-ZS-3, 2026-10-21); the _w17r and _av0 files keep
# the figures that earlier reports cite.
REFERENCE = "arena/results/m100_league_sim_10k_s{seed}_w17r_av0_scv.json"
OWNER_SEAT = 10
TIERS = ((1.0, "ROBUST"), (2.0, "SENSITIVE"))


def tier(shift):
    a = abs(shift)
    for bound, name in TIERS:
        if a < bound:
            return name
    return "FRAGILE"


def variants_from_registry(reg):
    out = []
    for e in reg["constants"]:
        if e.get("status") != "declared_band":
            continue
        if not e.get("band"):
            raise ValueError(f"{e['module']}.{e['name']} is declared_band with no band")
        for b in e["band"]:
            patch = {k: v for k, v in b.items() if k != "label"}
            out.append(dict(constant=f"{e['module']}.{e['name']}", label=b["label"], patch=patch))
    return out


def _job(args):
    # owner 2026-10-26: an optional state and pool (absolute paths) run the season configuration; absent, the draft one
    label, patch, seed, seasons, deck = args[:5]
    state_path, pool_path = (tuple(args[5:7]) + (None, None))[:2]
    for d in (os.path.join(deck, "scripts"), os.path.join(deck, "arena")):
        if d not in sys.path:
            sys.path.insert(0, d)
    hoops = importlib.import_module("hoops")
    arena = importlib.import_module("arena")
    importlib.reload(arena)  # a fresh module per job: patches must not leak between jobs sharing a worker
    hoops.DATA_PATH = pool_path or os.path.join(deck, POOL)
    by = {p["player"]: p for p in hoops.zscores(hoops.load_players())}
    with open(state_path or os.path.join(deck, STATE), encoding="utf-8") as f:
        st = json.load(f)
    ros = {s: [] for s in range(1, arena.TEAMS + 1)}
    for pk in st["picks"]:
        ros[pk["slot"]].append(by[pk["player"]])
    # the patch kinds live in the deck's arena/patches.py since 2026-10-26, shared with league_sim --patch
    importlib.import_module("patches").apply(arena, patch)
    rng = random.Random(seed)
    champ, po = arena.simulate_seasons(ros, seasons, rng, cv=arena.SEASON_CV)
    return label, seed, 100 * champ[OWNER_SEAT] / seasons, 100 * po[OWNER_SEAT] / seasons


def summarize(titles, variants, seeds):
    """titles: {label: {seed: title%}} incl. 'baseline'; variants: [{constant,label}]. Tiers per constant."""
    seeds = [str(s) for s in seeds]
    base = {s: titles["baseline"][s] for s in seeds}
    consts = {}
    for v in variants:
        shifts = {s: round(titles[v["label"]][s] - base[s], 2) for s in seeds}
        mean = round(sum(shifts.values()) / len(seeds), 2)
        c = consts.setdefault(v["constant"], {"variants": [], "tier": "ROBUST", "max_abs_shift": 0.0})
        c["variants"].append(dict(label=v["label"], shift=shifts, shift_mean=mean, tier=tier(mean)))
        if abs(mean) > c["max_abs_shift"]:
            c["max_abs_shift"] = abs(mean)
            c["tier"] = tier(mean)
    return {"constants": consts,
            "fragile": [k for k, c in consts.items() if c["tier"] == "FRAGILE"],
            "sensitive": [k for k, c in consts.items() if c["tier"] == "SENSITIVE"]}


def _sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def _job_sim(args):
    """One variant through the deck's league_sim (owner 2026-10-26, the real-schedule re-measurement): the season
    configuration's state and pool, the league's real pairings and the weeks already final, the patch by --patch."""
    label, patch, seed, seasons, deck, state, pool, schedule, work = args
    tag = "".join(ch if ch.isalnum() else "_" for ch in label)[:40]
    out = os.path.join(work, f"sim_{tag}_{seed}.json")
    cmd = [sys.executable, os.path.join(deck, "arena", "mocks", "league_sim.py"), state, "v69", str(seasons), str(seed), out,
           "--schedule", schedule, "--season-cv", "--pool", pool]
    if patch:
        pf = os.path.join(work, f"patch_{tag}_{seed}.json")
        with open(pf, "w", encoding="utf-8") as f:
            json.dump(patch, f)
        cmd += ["--patch", pf]
    subprocess.run(cmd, check=True, capture_output=True)
    with open(out, encoding="utf-8") as f:
        t = json.load(f)["teams"][str(OWNER_SEAT)]
    return label, seed, t["champ"], t["playoff"]


def season_inputs(out_dir, league_state, pool, seeds, ref_seasons=10000, deck=DECK, schedule=None):
    """Owner 2026-10-26: the season configuration the title odds run on — the league state's rosters (IL excluded,
    D-IS-8, as the brief builds them) on the season pool — written as a picks file in out_dir, and each seed's 10k
    reference from league_sim --verify --pool on it. Returns (state_path, {seed: reference_path})."""
    kit_scripts = os.path.dirname(HERE)
    if kit_scripts not in sys.path:
        sys.path.insert(0, kit_scripts)
    # the inputs are pinned beside the record, and the run reads the pinned copies (owner 2026-10-26)
    os.makedirs(out_dir, exist_ok=True)
    pinned = {}
    for name, src in (("league_state.json", league_state), ("pool_season.csv", pool), ("league_schedule.json", schedule)):
        if src:
            dst = os.path.join(out_dir, name)
            if os.path.abspath(src) != os.path.abspath(dst):
                shutil.copyfile(src, dst)
            pinned[name] = dst
    league_state, pool, schedule = pinned["league_state.json"], pinned["pool_season.csv"], pinned.get("league_schedule.json")
    os.environ["SEASON_POOL"] = pool
    import co_gm as CG
    _, by = CG.load_pool()
    with open(league_state, encoding="utf-8") as f:
        ros = CG.rosters(json.load(f), by)
    os.makedirs(out_dir, exist_ok=True)
    state_path = os.path.join(out_dir, "state_season.json")
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(CG.sim_state(ros), f, indent=1, ensure_ascii=False)
    refs = {}
    for sd in seeds:
        refs[sd] = os.path.join(out_dir, f"reference_10k_s{sd}.json")
        # with the real schedule --verify cannot run (it changes the draw order): the reference is the plain run
        mode = ["--schedule", schedule] if schedule else ["--verify"]
        subprocess.run([sys.executable, os.path.join(deck, "arena", "mocks", "league_sim.py"), state_path, "v69",
                        str(ref_seasons), str(sd), refs[sd], "--season-cv", "--pool", pool] + mode,
                       check=True, capture_output=True)
    return state_path, refs, pool, schedule


def run_sweep(seasons, seeds, out, workers=4, registry=None, deck=DECK, registry_path=REGISTRY, state=None, pool=None,
              references=None, schedule=None):
    """state/pool: absolute paths of a draft-state-shaped picks file and a deck-schema pool (the season configuration,
    owner 2026-10-26); references: {seed: path} of that configuration's 10k league_sim --verify records, each required.
    All three absent: the draft configuration and its standing references, as before."""
    if registry is None:
        with open(registry_path, encoding="utf-8") as f:
            registry = json.load(f)
    variants = variants_from_registry(registry)
    labels = [v["label"] for v in variants]
    if len(set(labels)) != len(labels):
        raise ValueError("two band variants share a label")
    if references:
        for sd in seeds:
            if not os.path.exists(references[sd]):
                raise FileNotFoundError(f"no 10k reference for seed {sd}: {references[sd]}")
    if schedule:
        # owner 2026-10-26: every variant through league_sim on the real pairings and the weeks already final
        if not (state and pool):
            raise ValueError("the real-schedule sweep needs the season configuration's state and pool")
        work = tempfile.mkdtemp()
        jobs = [("baseline", {}, sd, seasons, deck, state, pool, schedule, work) for sd in seeds]
        jobs += [(v["label"], v["patch"], sd, seasons, deck, state, pool, schedule, work) for v in variants for sd in seeds]
        fn = _job_sim
    else:
        jobs = [("baseline", {}, sd, seasons, deck, state, pool) for sd in seeds]
        jobs += [(v["label"], v["patch"], sd, seasons, deck, state, pool) for v in variants for sd in seeds]
        fn = _job
    with ProcessPoolExecutor(workers) as ex:
        res = list(ex.map(fn, jobs))
    titles, playoffs = {}, {}
    for label, sd, c, p in res:
        titles.setdefault(label, {})[str(sd)] = round(c, 2)
        playoffs.setdefault(label, {})[str(sd)] = round(p, 2)
    se = math.sqrt(0.22 * 0.78 / seasons) * 100
    ref, within = {}, {}
    for sd in seeds:
        rp = references[sd] if references else os.path.join(deck, REFERENCE.format(seed=sd))
        if os.path.exists(rp):
            with open(rp, encoding="utf-8") as f:
                ref[str(sd)] = json.load(f)["teams"][str(OWNER_SEAT)]["champ"]
            within[str(sd)] = abs(titles["baseline"][str(sd)] - ref[str(sd)]) < 3 * se
    try:
        commit = subprocess.run(["git", "-C", deck, "rev-parse", "--short", "HEAD"], capture_output=True,
                                text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        commit = ""
    rec = dict(seasons=seasons, seeds=list(seeds), workers=workers, mc_se_points=round(se, 3),
               engine_commit=commit, state=state or STATE, pool=pool or POOL, owner_seat=OWNER_SEAT,
               registry_sha256=hashlib.sha256(json.dumps(registry, sort_keys=True).encode()).hexdigest()[:12],
               reference_10k=ref, baseline_within_3se=within,
               tier_rule="mean shift over seeds: ROBUST < 1, SENSITIVE 1-2, FRAGILE >= 2 title points",
               variants={lb: dict(title=titles[lb], playoff=playoffs[lb]) for lb in ["baseline"] + labels})
    if state or pool:
        rec.update(state_sha256=_sha(state or os.path.join(deck, STATE)), pool_sha256=_sha(pool or os.path.join(deck, POOL)),
                   references={str(sd): references[sd] for sd in seeds} if references else None)
    if schedule:
        rec.update(schedule=schedule, schedule_sha256=_sha(schedule), simulator="league_sim (real pairings, weeks already final)")
    rec.update(summarize(titles, variants, seeds))
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return rec


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seasons", type=int, default=6000)
    ap.add_argument("--seeds", type=int, nargs="+", default=[2026, 2027])
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--deck", default=DECK)
    ap.add_argument("--registry", default=REGISTRY)
    ap.add_argument("--real-schedule", metavar="SCHEDULE",
                    help="with --season: every variant through league_sim on this schedule file (the real pairings and "
                         "the weeks already final), the reference the plain league_sim run (owner 2026-10-26)")
    ap.add_argument("--season", nargs=2, metavar=("LEAGUE_STATE", "POOL"),
                    help="the season configuration (owner 2026-10-26): rosters from the league state on the named pool; "
                         "the picks file and each seed's 10k reference are written beside --out")
    a = ap.parse_args()
    state = pool = refs = sched = None
    if a.real_schedule and not a.season:
        ap.error("--real-schedule needs --season")
    if a.season:
        state, refs, pool, sched = season_inputs(os.path.dirname(os.path.abspath(a.out)), os.path.abspath(a.season[0]),
                                                 os.path.abspath(a.season[1]), tuple(a.seeds), deck=os.path.abspath(a.deck),
                                                 schedule=os.path.abspath(a.real_schedule) if a.real_schedule else None)
    rec = run_sweep(a.seasons, tuple(a.seeds), a.out, a.workers, deck=os.path.abspath(a.deck),
                    registry_path=a.registry, state=state, pool=pool, references=refs, schedule=sched)
    print(f"SWEEP: {rec['seasons']:,} seasons x seeds {rec['seeds']} on deck {rec['engine_commit']}; "
          f"MC SE {rec['mc_se_points']:.2f}; baseline within 3 SE of the 10k reference: {rec['baseline_within_3se']}")
    b = rec["variants"]["baseline"]["title"]
    print(f"{'baseline':<52} " + " / ".join(f"{b[str(s)]:6.2f}" for s in rec["seeds"]))
    for name, c in rec["constants"].items():
        for v in c["variants"]:
            t = rec["variants"][v["label"]]["title"]
            print(f"{v['label']:<52} " + " / ".join(f"{t[str(s)]:6.2f}" for s in rec["seeds"])
                  + f"   shift {v['shift_mean']:+.2f}  {v['tier']:<9} [{name}]")
    print("FRAGILE:", rec["fragile"] or "none", "  SENSITIVE:", rec["sensitive"] or "none")


if __name__ == "__main__":
    main()
