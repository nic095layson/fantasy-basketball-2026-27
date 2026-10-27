#!/usr/bin/env python3
"""The minutes-trend candidate line (owner 2026-10-27, build 2: "let's build"): the live season line scaled, per
player, by a recency-weighted minutes forecast over his blended season minutes. It isolates one signal the week-1
audit named (half the projection miss was minutes) and leaves the blend's per-minute rates as they are.

    forecast minutes  = (MIN_PRIOR_GAMES * preseason mpg + n_eff * recent) / (MIN_PRIOR_GAMES + n_eff)
                        recent = the regular-season minutes weighted 0.5 ** (age / HALF_LIFE), newest first;
                        n_eff = the sum of those weights
    implicit minutes  = (STATS_PRIOR * preseason mpg + total minutes) / (STATS_PRIOR + games)
                        STATS_PRIOR = the blend's own points prior (season_lines.PRIOR_GAMES["PTS"]): the minutes
                        the blended line already "believes", at the speed the blend moves
    candidate line    = the live line x (forecast / implicit) on counting stats and attempts; FG% and FT% untouched

Why two priors (2026-10-27, found by the red test and a smoke run): with one prior in both places the ratio is 1.0
by construction and the candidate grades the blend against itself. Minutes stabilise faster than stats, so the
forecast trusts them at MIN_PRIOR_GAMES while the blend keeps trusting stats at its own ~12-game prior; the ratio
carries exactly that difference. A player with no regular-season game has ratio 1.0; a player with no preseason mpg
on file is left unscaled and named. HALF_LIFE and MIN_PRIOR_GAMES are hand-set and registered uncalibrated
(scripts/redteam/constants_registry.json, module minutes_line); the weekly accuracy card is the decision that
calibrates them.

CANDIDATE ONLY: nothing on the board, in the brief or in the simulator reads these files. The Sunday step snapshots
them (report/accuracy/lines_week<N>_mt.csv) and the Monday accuracy card grades them beside the blend; the owner
decides any switch on that record (pre-committed rule: lower MAE than the blend on PTS, REB and AST in at least 3
of 4 consecutive graded weeks).

    python3 scripts/minutes_line.py --date 2026-10-27 [--actuals data/actuals] [--out-dir data/season]
Writes data/season/pool_season_mt.csv (deck schema), projections_season_mt.csv (kit schema) and
data/season/minutes_line_<date>.json (ratios, forecasts, the unscaled). Prints 'MINUTES LINE: PASS — ...'.
"""
import argparse
import csv
import datetime
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
SEASON = os.path.join(KIT, "data", "season")
ACTUALS = os.path.join(KIT, "data", "actuals")
POOL = os.path.join(SEASON, "pool_season.csv")
KIT_CSV = os.path.join(SEASON, "projections_season.csv")
PRE_KIT = os.path.join(KIT, "report", "projections-2026-27.csv")   # the preseason mpg (never edited in season)

HALF_LIFE = 5.0        # games; the recency weight halves every HALF_LIFE games (hand-set, uncalibrated: D-ML-1)
MIN_PRIOR_GAMES = 3.0  # games the preseason mpg is worth in the minutes forecast (hand-set, uncalibrated: D-ML-1)


def stats_prior():
    """The blend's points prior, read live so the denominator tracks the blend (season_lines.PRIOR_GAMES['PTS'])."""
    import season_lines as SL
    return float(SL.PRIOR_GAMES["PTS"])
SCALED = ("fga", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov")
DEC = {c: 1 for c in SCALED}


def forecast_minutes(minutes, pre_mpg, half_life=HALF_LIFE, prior_games=MIN_PRIOR_GAMES):
    """minutes: the player's regular-season minutes, oldest first. None when there is no preseason mpg."""
    if pre_mpg is None:
        return None
    if not minutes:
        return float(pre_mpg)
    n = len(minutes)
    w = [0.5 ** ((n - 1 - i) / half_life) for i in range(n)]
    n_eff = sum(w)
    recent = sum(m * x for m, x in zip(minutes, w)) / n_eff
    return (prior_games * float(pre_mpg) + n_eff * recent) / (prior_games + n_eff)


def implicit_minutes(minutes, pre_mpg, prior_games=None):
    """The minutes the blended line already carries: the preseason mpg moved at the blend's own points prior."""
    if pre_mpg is None:
        return None
    k = stats_prior() if prior_games is None else prior_games
    return (k * float(pre_mpg) + sum(minutes)) / (k + len(minutes))


def scale_row(row, ratio):
    if ratio == 1.0:
        return dict(row)
    out = dict(row)
    for c in SCALED:
        if c in out and out[c] not in ("", None):
            out[c] = f"{float(out[c]) * ratio:.{DEC[c]}f}"
    return out


def season_minutes(actuals_dir, through=None):
    """{pool name: [minutes, oldest first]} from the regular-season box records dated on or before `through`."""
    out = {}
    for f in sorted(glob.glob(os.path.join(actuals_dir, "????-??-??.json"))):
        d = os.path.basename(f)[:10]
        if through and d > through:
            continue
        with open(f, encoding="utf-8") as fh:
            a = json.load(fh)
        if not a.get("games") or not all(g.get("season_type") == 2 for g in a["games"]):
            continue
        for r in a.get("players", []):
            if r.get("pool_name") and not r.get("dnp") and r.get("min", 0) > 0:
                out.setdefault(r["pool_name"], []).append(r["min"])
    return out


def preseason_mpg(path=PRE_KIT):
    with open(path, encoding="utf-8", newline="") as f:
        out = {}
        for r in csv.DictReader(f):
            try:
                out[r["name"]] = float(r["mpg"]) if r.get("mpg") not in ("", None) else None
            except ValueError:
                out[r["name"]] = None
        return out


def build(pool_csv, kit_csv, minutes, half_life=HALF_LIFE, prior_games=MIN_PRIOR_GAMES, stats_prior_games=None, name_col="player"):
    """Scale the pool (deck schema, `player`) and return rows, ratios, forecasts and the unscaled names; the kit-schema
    file (`name`, carries mpg) supplies the preseason minutes."""
    with open(kit_csv, encoding="utf-8", newline="") as f:
        mpg = {}
        for r in csv.DictReader(f):
            try:
                mpg[r["name"]] = float(r["mpg"]) if r.get("mpg") not in ("", None) else None
            except ValueError:
                mpg[r["name"]] = None
    with open(pool_csv, encoding="utf-8", newline="") as f:
        rd = csv.DictReader(f); fields = rd.fieldnames; rows = list(rd)
    out, ratios, fcs, unscaled = [], {}, {}, []
    for r in rows:
        name = r[name_col]; mins = minutes.get(name, []); pre = mpg.get(name)
        fc = forecast_minutes(mins, pre, half_life, prior_games)
        bl = implicit_minutes(mins, pre, stats_prior_games)
        if fc is None or not bl:
            unscaled.append(name); ratios[name] = 1.0; out.append(dict(r)); continue
        ratio = fc / bl
        ratios[name] = ratio; fcs[name] = fc
        out.append(scale_row(r, ratio))
    return dict(rows=out, fields=fields, ratios=ratios, forecasts=fcs, unscaled=sorted(unscaled),
                method=dict(half_life=half_life, min_prior_games=prior_games,
                            stats_prior_games=stats_prior() if stats_prior_games is None else stats_prior_games,
                            rule="live line x forecast/implicit minutes on " + ",".join(SCALED) + "; FG%/FT% untouched"))


def write_csv(path, rows, fields):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); w.writeheader(); w.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--actuals", default=ACTUALS); ap.add_argument("--out-dir", default=SEASON)
    ap.add_argument("--pool", default=POOL); ap.add_argument("--kit", default=KIT_CSV); ap.add_argument("--pre-kit", default=PRE_KIT)
    ap.add_argument("--through", default=None, help="use box records dated on or before this (default: all on disk)")
    a = ap.parse_args()
    try:
        minutes = season_minutes(a.actuals, a.through)
        rec = build(a.pool, a.pre_kit, minutes)                       # preseason mpg from the never-edited file
        kit = build(a.kit, a.pre_kit, minutes, name_col="name")
    except (OSError, ValueError, KeyError) as e:
        print(f"MINUTES LINE: FAIL — {e}"); return 1
    os.makedirs(a.out_dir, exist_ok=True)
    write_csv(os.path.join(a.out_dir, "pool_season_mt.csv"), rec["rows"], rec["fields"])
    write_csv(os.path.join(a.out_dir, "projections_season_mt.csv"), kit["rows"], kit["fields"])
    moved = sorted(((n, r) for n, r in rec["ratios"].items() if abs(r - 1) >= 0.10), key=lambda x: -abs(x[1] - 1))
    out = dict(date=a.date, through=a.through, players=len(rec["rows"]), with_games=sum(1 for n in rec["ratios"] if minutes.get(n)),
               unscaled=rec["unscaled"], method=rec["method"], ratios={n: round(r, 4) for n, r in rec["ratios"].items()},
               forecast_minutes={n: round(v, 2) for n, v in rec["forecasts"].items()},
               biggest_moves=[dict(player=n, ratio=round(r, 3)) for n, r in moved[:20]],
               inputs=dict(pool=os.path.relpath(a.pool, KIT), kit=os.path.relpath(a.kit, KIT), pre_kit=os.path.relpath(a.pre_kit, KIT)))
    with open(os.path.join(a.out_dir, f"minutes_line_{a.date}.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False); f.write("\n")
    up = sum(1 for r in rec["ratios"].values() if r >= 1.10); down = sum(1 for r in rec["ratios"].values() if r <= 0.90)
    print(f"MINUTES LINE: PASS — {a.date}: {out['players']} players, {out['with_games']} with games; ratio >= 1.10 for {up}, <= 0.90 for {down}; "
          f"{len(rec['unscaled'])} unscaled (no preseason mpg); candidate only, wrote pool_season_mt.csv, projections_season_mt.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
