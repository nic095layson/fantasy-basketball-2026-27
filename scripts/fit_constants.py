#!/usr/bin/env python3
"""Fit the two FRAGILE hand-set constants from the finished weeks (owner 2026-10-27, build 3): propose only.

  TEAM_WEEK_SHOCK      the shared games-played swing the simulator draws once per team-week (gauss(1, shock)) on
                       every counting category. For each finished team-week the simulator's own team_week_model, on
                       the lines and rosters snapshotted the Sunday before (report/accuracy/lines_week<N>.csv,
                       state_week<N>.json), gives each counting category's expected total mu and variance var; the
                       factor f = mean over the 7 counting categories of actual/mu. Across team-weeks
                       Var(f) = shock^2 + model term, the model term = mean over team-weeks of mean_c(var_c/mu_c^2)/7
                       (the categories treated as independent under no shock, A2). shock = sqrt(Var(f) - model term);
                       a bootstrap over team-weeks gives the standard error. A non-positive excess reports
                       "no shock detectable at this sample", never a clamped number.
  weekly_availability  the share of his NBA team's games a player plays by the tier the simulator assumes, pooled
                       over the finished weeks from the accuracy card's availability rows (report/accuracy.json),
                       with the binomial standard error and whether the live value sits within 2 SE.

Sample gate: with fewer than MIN_WEEKS finished weeks the fit runs and reports "too few weeks to propose". The
registry and the engine are never written by this script; the owner decides any swap on the record it writes:
report/fits/fit_week<N>.json (never rewritten) and report/fits.md (regenerated).

    python3 scripts/fit_constants.py --week 2 [--out-dir report/fits]
"""
import argparse
import csv
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
WEEKS = os.path.join(KIT, "data", "weeks")
SNAPSHOTS = os.path.join(KIT, "report", "accuracy")
ACCURACY = os.path.join(KIT, "report", "accuracy.json")
OUT = os.path.join(KIT, "report", "fits")
COUNTING = ("3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO")
MIN_WEEKS = 4


class FitError(Exception):
    pass


def factor(row):
    return sum(row[c]["actual"] / row[c]["mu"] for c in COUNTING) / len(COUNTING)


def model_term(row):
    return sum(row[c]["var"] / row[c]["mu"] ** 2 for c in COUNTING) / len(COUNTING) / len(COUNTING)


def _estimate(rows):
    f = [factor(r) for r in rows]; m = sum(f) / len(f)
    var_f = sum((x - m) ** 2 for x in f) / (len(f) - 1)
    term = sum(model_term(r) for r in rows) / len(rows)
    return var_f, term, var_f - term


def shock_estimate(rows, boots=500, seed=0):
    """rows: per team-week {cat: {actual, mu, var}} for the counting cats."""
    if len(rows) < 3:
        return dict(n=len(rows), shock=None, se=None, note="fewer than 3 team-weeks")
    var_f, term, excess = _estimate(rows)
    rng = random.Random(seed); bs = []
    for _ in range(boots):
        sample = [rows[rng.randrange(len(rows))] for _ in rows]
        bs.append(_estimate(sample)[2])
    mean_b = sum(bs) / len(bs)
    se_excess = math.sqrt(sum((b - mean_b) ** 2 for b in bs) / (len(bs) - 1))
    out = dict(n=len(rows), var_factor=var_f, model_term=term, excess=excess, se_excess=se_excess, bootstrap=boots)
    # a shock is reported only when the excess variance stands 2 SE clear of zero; otherwise "not detectable",
    # never a small number read off noise (2026-10-27: a no-shock synthetic set came out slightly positive by chance)
    if excess <= 2 * se_excess:
        out.update(shock=None, se=None, note=f"no shock detectable at this sample (excess variance {excess:.5f} ± {se_excess:.5f}, not 2 SE clear of 0)")
    else:
        shock = math.sqrt(excess)
        out.update(shock=shock, se=se_excess / (2 * shock))     # delta method: d sqrt(x) = dx / (2 sqrt x)
    return out


def availability_pool(weeks):
    """weeks: the accuracy card's availability dicts, {tier: {assumed, played, team_games}}."""
    acc = {}
    for w in weeks:
        for t, a in w.items():
            r = acc.setdefault(t, dict(assumed=a["assumed"], played=0, team_games=0))
            r["played"] += a["played"]; r["team_games"] += a["team_games"]
    out = {}
    for t, r in acc.items():
        n = r["team_games"]
        if not n:
            continue
        p = r["played"] / n; se = math.sqrt(p * (1 - p) / n) if 0 < p < 1 else 0.0
        out[t] = dict(live=r["assumed"], measured=p, se=se, n=n, played=r["played"],
                      live_within_2se=abs(r["assumed"] - p) <= 2 * se)
    return out


def proposal_status(n_weeks):
    return "proposal" if n_weeks >= MIN_WEEKS else f"too few weeks to propose ({n_weeks} of {MIN_WEEKS})"


def write_fit(path, rec):
    if os.path.exists(path):
        raise FitError(f"{path} exists; a week's fit is never rewritten")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False); f.write("\n")


# ---------------------------------------------------------------- the real inputs
def team_week_rows(week, weeks_dir=WEEKS, snapshots=SNAPSHOTS):
    """Each team's {cat: {actual, mu, var}} for the week: actuals from data/weeks/week_N.json, mu/var from the
    simulator's team_week_model on the Sunday snapshot (lines + state). Returns (rows, note)."""
    import co_gm as CG
    wk_path = os.path.join(weeks_dir, f"week_{week}.json")
    lines = os.path.join(snapshots, f"lines_week{week}.csv"); state_p = os.path.join(snapshots, f"state_week{week}.json")
    for p in (wk_path, lines, state_p):
        if not os.path.exists(p):
            return [], f"week {week}: missing {os.path.relpath(p, KIT)}"
    with open(wk_path, encoding="utf-8") as f:
        wk = json.load(f)
    with open(state_p, encoding="utf-8") as f:
        state = json.load(f)
    CG.hoops.DATA_PATH = lines
    P = CG.hoops.zscores(CG.hoops.load_players()); by = {p["player"]: p for p in P}
    rows, skipped = [], []
    for name, t in wk["teams"].items():
        seat = t["seat"]
        team = next((x for x in state["teams"] if x["seat"] == seat), None)
        if team is None:
            skipped.append(f"seat {seat} not in the state snapshot"); continue
        ros = [by[p["player"]] for p in team["players"] if p.get("slot") != "IL" and p["player"] in by]
        missing = [p["player"] for p in team["players"] if p.get("slot") != "IL" and p["player"] not in by]
        if not ros:
            skipped.append(f"{name}: no lined players"); continue
        mu, var = CG.arena.team_week_model(ros, CG.arena.SEASON_CV)
        row = {c: dict(actual=float(t["line"][c]), mu=float(mu[c]), var=float(var[c])) for c in COUNTING}
        row["_team"] = name; row["_missing_lines"] = missing
        rows.append(row)
    note = f"{len(rows)} team-weeks" + (f"; skipped: {'; '.join(skipped)}" if skipped else "")
    return rows, note


def run(week, weeks_dir=WEEKS, snapshots=SNAPSHOTS, accuracy=ACCURACY, out_dir=OUT, boots=500):
    """Fit on every finished week up to and including `week` that has its inputs; write the week's record."""
    rows, notes, weeks_used = [], [], []
    for w in range(1, week + 1):
        r, n = team_week_rows(w, weeks_dir, snapshots)
        notes.append(f"week {w}: {n}")
        if r:
            rows += r; weeks_used.append(w)
    shock = shock_estimate([{c: r[c] for c in COUNTING} for r in rows], boots=boots, seed=week) if rows else dict(n=0, shock=None, se=None, note="no team-weeks")
    acc = json.load(open(accuracy, encoding="utf-8"))["weeks"] if os.path.exists(accuracy) else {}
    avail = availability_pool([acc[k]["availability"] for k in sorted(acc, key=int) if int(k) <= week and acc[k].get("availability")])
    import co_gm as CG
    rec = dict(week=week, weeks_used=weeks_used, status=proposal_status(len(weeks_used)), notes=notes,
               team_week_shock=dict(live=CG.arena.TEAM_WEEK_SHOCK, **shock),
               weekly_availability=avail,
               method=dict(shock="f = mean over 7 counting cats of actual/mu per team-week; Var(f) = shock^2 + mean(mean_c var/mu^2)/7 "
                                 "(cats independent under no shock, A2); shock = sqrt(excess); bootstrap SE over team-weeks",
                           availability="pooled share of team games played per assumed tier, binomial SE; from report/accuracy.json",
                           inputs="data/weeks/week_N.json actuals; report/accuracy/lines_weekN.csv + state_weekN.json for the model"),
               proposes_only=True)
    write_fit(os.path.join(out_dir, f"fit_week{week}.json"), rec)
    with open(os.path.join(os.path.dirname(out_dir.rstrip("/")), "fits.md"), "w", encoding="utf-8") as f:
        f.write(render(out_dir))
    return rec


def render(out_dir):
    import glob
    recs = [json.load(open(p, encoding="utf-8")) for p in sorted(glob.glob(os.path.join(out_dir, "fit_week*.json")), key=lambda p: int(p.rsplit("week", 1)[1][:-5]))]
    f = lambda v, p=4: "–" if v is None else f"{v:.{p}f}"
    L = ["# Fits of the hand-set constants — proposals only", "",
         "Each Monday the finished weeks are fitted (`scripts/fit_constants.py`); a record is never rewritten. "
         f"A proposal needs {MIN_WEEKS} finished weeks. Nothing here changes the engine or the registry: the owner decides any swap.", "",
         "## TEAM_WEEK_SHOCK (shared weekly games swing)", "",
         "| through week | weeks | team-weeks | live | measured | SE | status |", "|---|---|---|---|---|---|---|"]
    for r in recs:
        s = r["team_week_shock"]
        L.append(f"| {r['week']} | {','.join(map(str, r['weeks_used'])) or '–'} | {s.get('n', 0)} | {s['live']} | "
                 + (f(s["shock"]) if s.get("shock") is not None else s.get("note", "–")) + f" | {f(s.get('se'))} | {r['status']} |")
    L += ["", "## weekly_availability (share of team games played, by assumed tier)", "",
          "| through week | tier (live) | measured | SE | n | live within 2 SE |", "|---|---|---|---|---|---|"]
    for r in recs:
        for t, a in sorted(r["weekly_availability"].items()):
            L.append(f"| {r['week']} | {a['live']:.2f} | {a['measured']:.3f} | {a['se']:.3f} | {a['n']} | {'yes' if a['live_within_2se'] else 'no'} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--week", type=int, required=True)
    ap.add_argument("--weeks-dir", default=WEEKS); ap.add_argument("--snapshots", default=SNAPSHOTS)
    ap.add_argument("--accuracy", default=ACCURACY); ap.add_argument("--out-dir", default=OUT); ap.add_argument("--boots", type=int, default=500)
    a = ap.parse_args()
    try:
        r = run(a.week, a.weeks_dir, a.snapshots, a.accuracy, a.out_dir, a.boots)
    except (FitError, OSError, ValueError, KeyError) as e:
        print(f"FIT CONSTANTS: FAIL — {e}"); return 1
    print(f"FIT CONSTANTS: PASS — {summary(r)}")
    return 0


def summary(r):
    s = r["team_week_shock"]; av = r["weekly_availability"]
    sh = f"shock {s['shock']:.4f} ± {s['se']:.4f} (live {s['live']})" if s.get("shock") is not None else f"shock: {s.get('note')}"
    tiers = ", ".join(f"{t}: {a['measured']:.2f} ± {a['se']:.2f} (n {a['n']})" for t, a in sorted(av.items()))
    return f"through week {r['week']}, weeks {r['weeks_used']}, {s.get('n', 0)} team-weeks; {sh}; availability {tiers or 'none'}; {r['status']}; proposes only"


if __name__ == "__main__":
    sys.exit(main())
