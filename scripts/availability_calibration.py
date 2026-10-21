#!/usr/bin/env python3
"""Availability calibration (D-PM-4 option d; owner "implement fixes for all these", 2026-10-21). Measures, from the
season's own box scores, the share of his team's games a rostered player actually played, by injury tier, and sets
the realized risk/healthy and mild/healthy ratios beside the three numbers the system uses for the same thing:

  deck board   hoops.availability          risk 0.78, mild 0.85 (healthy 1.00)
  simulator    arena.weekly_availability   risk 0.75 / 0.88 = 0.852, mild 0.79 / 0.88 = 0.898
  kit board    rank_engine.avail(gp)       per player; the tier's mean relative to the healthy median

It changes no value. Until the sample is large enough it says INSUFFICIENT and why; after that, MEASURED, with the
realized ratios and how far each instrument sits from them. Which number to adopt stays the owner's decision.

Method (stated to the owner 2026-10-21 before the first run):
  - regular season only: games whose record says season_type 2 (preseason and DNPs never count)
  - population: players on league rosters in a non-IL slot (data/league_state.json; D-IS-8 zeroes IL anyway)
  - tier: today's pool note (data/season/pool_season.csv), leading tag only, the deck's own rule
  - share: games played (not DNP, minutes > 0) / games his current pool team has played
  - verdict MEASURED only when the median team has played MIN_TEAM_GAMES and MIN_RISK risk-tagged players are in
    the population; the defaults put the first possible verdict near CHECK_DATE

    python3 scripts/availability_calibration.py [--min-team-games 15] [--min-risk 10] [--out PATH]
Prints 'AVAILABILITY CALIBRATION: INSUFFICIENT — ...' or 'AVAILABILITY CALIBRATION: MEASURED — ...'; exit 0 either way.
"""
import argparse
import csv
import glob
import json
import os
import statistics
import sys

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK = os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball")
ACTUALS = os.path.join(KIT, "data", "actuals")
STATE = os.path.join(KIT, "data", "league_state.json")
POOL = os.path.join(KIT, "data", "season", "pool_season.csv")
LINES = os.path.join(KIT, "data", "season", "projections_season.csv")
MIN_TEAM_GAMES = 15
MIN_RISK = 10
CHECK_DATE = "2026-11-17"  # about four weeks of games at MIN_TEAM_GAMES
SIM_HEALTHY = 0.88


def calibrate(records, population, tiers, team_of, min_team_games=MIN_TEAM_GAMES, min_risk=MIN_RISK):
    """records: box-score records (data/actuals schema); population: player names; tiers: {name: tier};
    team_of: {name: current pool team}. Returns the measurement as a dict."""
    team_games, played = {}, {}
    for rec in records:
        regular = {g["espn_id"] for g in rec.get("games", []) if g.get("season_type") == 2}
        seen = set()
        for p in rec.get("players", []):
            if p.get("game") not in regular:
                continue
            if (p["team"], p["game"]) not in seen:
                seen.add((p["team"], p["game"]))
                team_games[p["team"]] = team_games.get(p["team"], 0) + 1
            if p.get("pool_name") and not p.get("dnp") and (p.get("min") or 0) > 0:
                played.setdefault(p["pool_name"], set()).add(p["game"])
    by_tier = {}
    for name in population:
        tg = team_games.get(team_of.get(name))
        share = len(played.get(name, ())) / tg if tg else None
        by_tier.setdefault(tiers.get(name, "healthy"), []).append(share)
    out_tiers = {}
    for t, shares in by_tier.items():
        known = [s for s in shares if s is not None]
        out_tiers[t] = dict(n=len(shares), n_measured=len(known),
                            mean_share=statistics.mean(known) if known else None)
    healthy = (out_tiers.get("healthy") or {}).get("mean_share")
    ratio = {t: out_tiers[t]["mean_share"] / healthy for t in ("risk", "mild")
             if healthy and (out_tiers.get(t) or {}).get("mean_share") is not None}
    median_tg = statistics.median(team_games.values()) if team_games else 0
    n_risk = (out_tiers.get("risk") or {}).get("n_measured", 0)
    why = []
    if median_tg < min_team_games:
        why.append(f"median team games {median_tg:g} < {min_team_games}")
    if n_risk < min_risk:
        why.append(f"{n_risk} risk-tagged with games < {min_risk}")
    if not ratio:
        why.append("no realized ratio (no healthy or tagged player has team games on file)")
    return dict(team_games=team_games, median_team_games=median_tg, tiers=out_tiers, ratio=ratio,
                verdict="INSUFFICIENT" if why else "MEASURED", why="; ".join(why),
                min_team_games=min_team_games, min_risk=min_risk)


def _engine():
    for p in (os.path.join(DECK, "scripts"), os.path.join(DECK, "arena"), os.path.join(KIT, "report")):
        if p not in sys.path:
            sys.path.insert(0, p)
    import hoops, arena, check_planes, rank_engine  # noqa: E401
    return hoops, arena, check_planes, rank_engine


def tier_of(hoops, note):
    tag = hoops.note_tag(note)
    if tag.startswith("out-"):
        return "out"
    return {1.0: "healthy", 0.85: "mild", 0.78: "risk", 0.0: "recovery"}[hoops.availability({"note": note})]


def instruments(hoops, arena, check_planes, rank_engine, pool_rows, population, tiers):
    """The three relative numbers for risk and mild, on the instruments' own scales (same definitions as the
    2026-10-21 D-PM-4 measurement, report/after-reports/proceed-2026-10-21/dpm4_compare.py)."""
    kit = {check_planes.norm(r["name"]): float(r["gp"]) for r in csv.DictReader(open(LINES, encoding="utf-8"))}
    avail = {n: rank_engine.avail(kit[check_planes.norm(n)]) for n in population if check_planes.norm(n) in kit}
    healthy = [a for n, a in avail.items() if tiers.get(n) == "healthy"]
    ref = statistics.median(healthy) if healthy else None
    out = {}
    for t, note in (("risk", "inj-knee-risk"), ("mild", "inj-acl-mild")):
        vals = [a / ref for n, a in avail.items() if tiers.get(n) == t] if ref else []
        out[t] = dict(deck=hoops.availability({"note": note}),
                      simulator=round(arena.weekly_availability({"note": note}) / SIM_HEALTHY, 4),
                      kit_mean=round(statistics.mean(vals), 4) if vals else None)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--min-team-games", type=int, default=MIN_TEAM_GAMES)
    ap.add_argument("--min-risk", type=int, default=MIN_RISK)
    ap.add_argument("--out")
    a = ap.parse_args()
    hoops, arena, check_planes, rank_engine = _engine()
    pool = list(csv.DictReader(open(POOL, encoding="utf-8")))
    note = {r["player"]: r["note"] for r in pool}
    team_of = {r["player"]: r["team"] for r in pool}
    state = json.load(open(STATE, encoding="utf-8"))
    population = [p["player"] for t in state["teams"] for p in t["players"]
                  if not (p.get("slot") or "").startswith("IL") and p["player"] in note]
    tiers = {n: tier_of(hoops, note[n]) for n in population}
    records = [json.load(open(p, encoding="utf-8")) for p in sorted(glob.glob(os.path.join(ACTUALS, "*.json")))]
    r = calibrate(records, population, tiers, team_of, a.min_team_games, a.min_risk)
    r["instruments"] = instruments(hoops, arena, check_planes, rank_engine, pool, population, tiers)
    r.update(check_date=CHECK_DATE, population=len(population), actuals_files=len(records),
             league_state_as_of=state.get("as_of"))
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(r, f, indent=1, sort_keys=True)
            f.write("\n")
    counts = ", ".join(f"{t} {v['n']}" for t, v in sorted(r["tiers"].items()))
    if r["verdict"] == "INSUFFICIENT":
        print(f"AVAILABILITY CALIBRATION: INSUFFICIENT — {r['why']} (population {len(population)}: {counts}; "
              f"regular-season team-games on file {sum(r['team_games'].values())}); first verdict expected near "
              f"{CHECK_DATE}. No value changed.")
    else:
        parts = []
        for t in ("risk", "mild"):
            if t in r["ratio"]:
                i = r["instruments"][t]
                parts.append(f"{t}/healthy realized {r['ratio'][t]:.3f} vs deck {i['deck']:.3f}, simulator "
                             f"{i['simulator']:.3f}, kit {i['kit_mean'] if i['kit_mean'] is not None else '?'}")
        print(f"AVAILABILITY CALIBRATION: MEASURED — {'; '.join(parts)} (median team games "
              f"{r['median_team_games']:g}; population {len(population)}: {counts}). No value changed; "
              f"which number to adopt is the owner's decision (D-PM-4).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
