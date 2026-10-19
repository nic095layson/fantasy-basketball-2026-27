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
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(HERE))
DECK = os.path.abspath(os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball"))
REGISTRY = os.path.join(HERE, "constants_registry.json")
STATE = "arena/data/states/draft_state_100.json"
POOL = "arena/results/players_v69.csv"
REFERENCE = "arena/results/m100_league_sim_10k_s{seed}_w17r.json"
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
    label, patch, seed, seasons, deck = args
    for d in (os.path.join(deck, "scripts"), os.path.join(deck, "arena")):
        if d not in sys.path:
            sys.path.insert(0, d)
    hoops = importlib.import_module("hoops")
    arena = importlib.import_module("arena")
    importlib.reload(arena)  # a fresh module per job: patches must not leak between jobs sharing a worker
    hoops.DATA_PATH = os.path.join(deck, POOL)
    by = {p["player"]: p for p in hoops.zscores(hoops.load_players())}
    with open(os.path.join(deck, STATE), encoding="utf-8") as f:
        st = json.load(f)
    ros = {s: [] for s in range(1, arena.TEAMS + 1)}
    for pk in st["picks"]:
        ros[pk["slot"]].append(by[pk["player"]])
    for k, v in patch.get("const", {}).items():
        if not hasattr(arena, k):
            raise AttributeError(f"patch names arena.{k}, which the live engine does not have")
        setattr(arena, k, v)
    if "avail" in patch:
        h, r = patch["avail"]
        orig = arena.weekly_availability
        arena.weekly_availability = lambda p, h=h, r=r, orig=orig: (
            r if orig(p) == 0.75 else h if orig(p) == 0.88 else orig(p))
    if "cv" in patch:
        arena.CV = {c: v * patch["cv"] for c, v in arena.CV.items()}
    if "games" in patch:
        # the 3.5 games/week is a literal inside team_week_model, not a module constant: re-compile the
        # function with the literal replaced, in arena's own namespace
        src = inspect.getsource(arena.team_week_model)
        g = patch["games"]
        new = src.replace("g = 3.5 * a", f"g = {g} * a").replace("g_var = 3.5 * a", f"g_var = {g} * a")
        if new == src:
            raise RuntimeError("games patch found no 3.5 literal in team_week_model")
        ns = vars(arena)
        exec(compile(new, arena.__file__, "exec"), ns)
    rng = random.Random(seed)
    champ, po = arena.simulate_seasons(ros, seasons, rng)
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


def run_sweep(seasons, seeds, out, workers=4, registry=None, deck=DECK, registry_path=REGISTRY):
    if registry is None:
        with open(registry_path, encoding="utf-8") as f:
            registry = json.load(f)
    variants = variants_from_registry(registry)
    labels = [v["label"] for v in variants]
    if len(set(labels)) != len(labels):
        raise ValueError("two band variants share a label")
    jobs = [("baseline", {}, sd, seasons, deck) for sd in seeds]
    jobs += [(v["label"], v["patch"], sd, seasons, deck) for v in variants for sd in seeds]
    with ProcessPoolExecutor(workers) as ex:
        res = list(ex.map(_job, jobs))
    titles, playoffs = {}, {}
    for label, sd, c, p in res:
        titles.setdefault(label, {})[str(sd)] = round(c, 2)
        playoffs.setdefault(label, {})[str(sd)] = round(p, 2)
    se = math.sqrt(0.22 * 0.78 / seasons) * 100
    ref, within = {}, {}
    for sd in seeds:
        rp = os.path.join(deck, REFERENCE.format(seed=sd))
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
               engine_commit=commit, state=STATE, pool=POOL, owner_seat=OWNER_SEAT,
               registry_sha256=hashlib.sha256(json.dumps(registry, sort_keys=True).encode()).hexdigest()[:12],
               reference_10k=ref, baseline_within_3se=within,
               tier_rule="mean shift over seeds: ROBUST < 1, SENSITIVE 1-2, FRAGILE >= 2 title points",
               variants={lb: dict(title=titles[lb], playoff=playoffs[lb]) for lb in ["baseline"] + labels})
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
    a = ap.parse_args()
    rec = run_sweep(a.seasons, tuple(a.seeds), a.out, a.workers, deck=os.path.abspath(a.deck),
                    registry_path=a.registry)
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
