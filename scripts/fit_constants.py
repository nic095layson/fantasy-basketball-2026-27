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
  board comparison     (owner 2026-10-27, "Fold into the week-4 fit"; replaces availability_calibration.py) the
                       realized risk/healthy and mild/healthy ratios from those pooled shares, with a delta-method
                       standard error, beside the same ratios on the three instruments that discount injury risk:
                       the deck board (hoops.availability), the simulator (arena.weekly_availability over its
                       healthy share) and the kit board (rank_engine.avail(gp) over the frozen pool's players in each
                       tier, divided by the healthy median; gp from data/season/projections_season.csv). Tiers are the
                       frozen preseason tags, as on the accuracy card, so no tag is set with hindsight.

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
SEASON_PROJ = os.path.join(KIT, "data", "season", "projections_season.csv")
TAG_NOTES = {"risk": "inj-knee-risk", "mild": "inj-acl-mild"}   # one representative tag per tier, as D-PM-4 measured


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


# Every value each tier has been assumed at (constants_registry.json weekly_availability record): the accuracy
# card keys its rows by the assumed value, so a tier's weeks before a value change carry the old key.
VALUE_TIER = {"0.88": "healthy", "0.80": "healthy", "0.75": "risk", "0.65": "risk", "0.79": "mild"}


def availability_pool(weeks, live=None):
    """weeks: the accuracy card's availability dicts, {tier: {assumed, played, team_games}}. live: {tier name: live
    key} (tier_keys()); with it, a tier's rows under an earlier value pool with its live-value rows, keyed and judged
    by the live value, with the team games per recorded value under pooled_from (Council 2026-11-16, owner "proceed
    with their vote": the share played is the players', not the assumption's). Without it, pooled by value only."""
    acc = {}
    for w in weeks:
        for t, a in w.items():
            k = live.get(VALUE_TIER.get(t), t) if live else t
            r = acc.setdefault(k, dict(assumed=float(k) if k != t else a["assumed"], played=0, team_games=0, by={}))
            r["played"] += a["played"]; r["team_games"] += a["team_games"]
            r["by"][t] = r["by"].get(t, 0) + a["team_games"]
    out = {}
    for t, r in acc.items():
        n = r["team_games"]
        if not n:
            continue
        p = r["played"] / n; se = math.sqrt(p * (1 - p) / n) if 0 < p < 1 else 0.0
        out[t] = dict(live=r["assumed"], measured=p, se=se, n=n, played=r["played"],
                      live_within_2se=abs(r["assumed"] - p) <= 2 * se)
        if live and set(r["by"]) != {t}:
            out[t]["pooled_from"] = r["by"]
    return out


def tier_keys():
    """The accuracy card's availability keys for healthy, risk and mild: the simulator's assumed shares, as strings."""
    import co_gm as CG
    k = lambda note: f"{CG.arena.weekly_availability({'note': note}):.2f}"
    return dict(healthy=k(""), **{t: k(n) for t, n in TAG_NOTES.items()})


def board_comparison(avail, instruments, keys=None):
    """avail: availability_pool's output; instruments: {tier: {deck, simulator, kit}} relative to healthy. Returns
    {tier: {measured, se, n, deck, simulator, kit, within_2se: {instrument: bool | None}}}; a tier or a healthy pool
    with no team games carries measured None and a note, never a guess."""
    keys = keys or tier_keys()
    h = avail.get(keys["healthy"]); out = {}
    for t in ("risk", "mild"):
        a = avail.get(keys[t]); inst = instruments.get(t, {})
        row = dict(measured=None, se=None, n=a["n"] if a else 0, **{i: inst.get(i) for i in ("deck", "simulator", "kit")})
        if not a or not h or not h["measured"] or not a["measured"]:
            row["note"] = f"no {t} share yet" if not a else "no healthy share yet"
            row["within_2se"] = {i: None for i in ("deck", "simulator", "kit")}
            out[t] = row; continue
        r = a["measured"] / h["measured"]
        se = r * math.sqrt((a["se"] / a["measured"]) ** 2 + (h["se"] / h["measured"]) ** 2)
        row.update(measured=r, se=se)
        row["within_2se"] = {i: (None if row[i] is None else abs(row[i] - r) <= 2 * se) for i in ("deck", "simulator", "kit")}
        out[t] = row
    return out


def board_instruments(frozen=None, season_proj=SEASON_PROJ):
    """The three instruments' risk/healthy and mild/healthy ratios, read from the engines (never typed)."""
    import co_gm as CG
    import accuracy_week as AW
    sys.path.insert(0, os.path.join(KIT, "report"))
    import rank_engine as RE
    hs = CG.arena.weekly_availability({"note": ""})
    out = {t: dict(deck=CG.hoops.availability({"note": n}),
                   simulator=round(CG.arena.weekly_availability({"note": n}) / hs, 4)) for t, n in TAG_NOTES.items()}
    try:
        with open(frozen or AW.FROZEN, encoding="utf-8") as f:
            share = {r["player"]: CG.arena.weekly_availability(r) for r in csv.DictReader(f)}
        with open(season_proj, encoding="utf-8") as f:
            gp = {r["name"]: float(r["gp"]) for r in csv.DictReader(f) if r.get("gp")}
    except (OSError, KeyError, ValueError) as e:
        for t in out:
            out[t].update(kit=None, kit_note=f"kit board not computed: {e}")
        return out
    by = {}
    for n, s in share.items():
        if n in gp:
            by.setdefault(f"{s:.2f}", []).append(RE.avail(gp[n]))
    healthy = sorted(by.get(f"{hs:.2f}", []))
    ref = healthy[len(healthy) // 2] if healthy else None
    for t, n in TAG_NOTES.items():
        vals = by.get(f"{CG.arena.weekly_availability({'note': n}):.2f}", [])
        out[t]["kit"] = round(sum(vals) / len(vals) / ref, 4) if vals and ref else None
        out[t]["kit_n"] = len(vals)
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
        ros = CG.team_roster(team, by, strict=False)  # the simulator's build: auto-row players count (2026-11-10)
        missing = [p["player"] for p in team["players"] if p.get("slot") != "IL" and p["player"] not in by]
        if not ros:
            skipped.append(f"{name}: no lined players"); continue
        mu, var = CG.arena.team_week_model(ros, CG.arena.SEASON_CV)
        row = {c: dict(actual=float(t["line"][c]), mu=float(mu[c]), var=float(var[c])) for c in COUNTING}
        row["_team"] = name; row["_missing_lines"] = missing
        rows.append(row)
    note = f"{len(rows)} team-weeks" + (f"; skipped: {'; '.join(skipped)}" if skipped else "")
    return rows, note


ACTUALS = os.path.join(KIT, "data", "actuals")
BOX_COLS = {"3PTM": "tpm", "PTS": "pts", "REB": "reb", "AST": "ast", "ST": "stl", "BLK": "blk", "TO": "tov"}


def level(rows):
    """Council 2026-11-16 (4-1): the model's level, the mean of actual / model per counting category over the
    team-weeks and over the seven. 1.0 is a model whose weekly means are right; the shock fit is read relative to it."""
    by = {c: sum(r[c]["actual"] / r[c]["mu"] for r in rows) / len(rows) for c in COUNTING} if rows else {}
    return dict(n=len(rows), by_cat=by, overall=(sum(by.values()) / len(by)) if by else None)


def level_relative(shock, lv):
    """The shock relative to the model's level (raw shock / level overall): the value the Council of 2026-11-16 set
    TEAM_WEEK_SHOCK from (0.107 on both the 0.88/0.75 and the 0.80/0.65 tiers, where the raw fit read 0.107 / 0.118)."""
    if shock.get("shock") is None or not (lv or {}).get("overall"):
        return None
    return shock["shock"] / lv["overall"]


def in_week_factors(week, weeks_dir=WEEKS, snapshots=SNAPSHOTS, actuals_dir=ACTUALS):
    """Council 2026-11-16 (4-1): each team's in-week roster factor for `week`, {seat: factor}: Yahoo's counted total
    over everything its Sunday roster (non-IL, the accuracy snapshot) produced in the week's box scores, benched games
    included, per counting category, averaged over the categories with a non-zero roster total. Above 1 is production
    from players added during the week. Names join through box_pull's fold, suffix key and alias table (a bare string
    match lost every Jr./Herb-Herbert spelling in the first measurement of 2026-11-16)."""
    import co_gm as CG
    import box_pull as BP
    import glob
    wk_path = os.path.join(weeks_dir, f"week_{week}.json"); state_p = os.path.join(snapshots, f"state_week{week}.json")
    if not (os.path.exists(wk_path) and os.path.exists(state_p) and os.path.isdir(actuals_dir)):
        return {}
    wk = json.load(open(wk_path, encoding="utf-8")); state = json.load(open(state_p, encoding="utf-8"))
    aliases = BP.load_aliases()
    out = {}
    rosters = {}
    for t in state["teams"]:
        names = [p["player"] for p in t["players"] if p.get("slot") != "IL"]
        names += [u if isinstance(u, str) else u.get("player") for u in (t.get("unpooled") or []) if (u if isinstance(u, str) else u.get("slot")) != "IL"]
        rosters[t["seat"]] = (BP.name_index(names, aliases), {c: 0.0 for c in COUNTING})
    for f in sorted(glob.glob(os.path.join(actuals_dir, "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        try:
            if CG.week_of(d["date"])[0] != week:
                continue
        except (ValueError, KeyError):
            continue
        for p in d.get("players", []):
            if p.get("dnp") or not p.get("min"):
                continue
            for seat, (index, tot) in rosters.items():
                if BP.match_name(p["name"], index) or (p.get("pool_name") and BP.match_name(p["pool_name"], index)):
                    for c, k in BOX_COLS.items():
                        tot[c] += float(p.get(k) or 0)
                    break
    for t in wk["teams"].values():
        if t["seat"] not in rosters:
            continue
        tot = rosters[t["seat"]][1]
        r = [float(t["line"][c]) / tot[c] for c in COUNTING if tot[c]]
        if r:
            out[str(t["seat"])] = sum(r) / len(r)
    return out


def between_team_f(by_team):
    """One-way ANOVA of the weekly in-week factors by team ({seat: [factor per week]}): F, its degrees of freedom and
    the 95% line. F near or below 1 means the teams differ no more than week-to-week noise."""
    groups = [v for v in by_team.values() if len(v) >= 2]
    k = len(groups); n = sum(len(v) for v in groups)
    if k < 2 or n <= k:
        return dict(F=None, df_between=k - 1, df_within=n - k, note="too few team-weeks")
    grand = sum(sum(v) for v in groups) / n
    msb = sum(len(v) * (sum(v) / len(v) - grand) ** 2 for v in groups) / (k - 1)
    msw = sum((x - sum(v) / len(v)) ** 2 for v in groups for x in v) / (n - k)
    return dict(F=(msb / msw) if msw else None, df_between=k - 1, df_within=n - k,
                means={s: sum(v) / len(v) for s, v in by_team.items() if v})


def run(week, weeks_dir=WEEKS, snapshots=SNAPSHOTS, accuracy=ACCURACY, out_dir=OUT, boots=500, actuals_dir=ACTUALS):
    """Fit on every finished week up to and including `week` that has its inputs; write the week's record."""
    rows, notes, weeks_used = [], [], []
    in_week = {}
    for w in range(1, week + 1):
        r, n = team_week_rows(w, weeks_dir, snapshots)
        notes.append(f"week {w}: {n}")
        if r:
            rows += r; weeks_used.append(w)
            for seat, fct in in_week_factors(w, weeks_dir, snapshots, actuals_dir).items():
                in_week.setdefault(seat, []).append(fct)
    shock = shock_estimate([{c: r[c] for c in COUNTING} for r in rows], boots=boots, seed=week) if rows else dict(n=0, shock=None, se=None, note="no team-weeks")
    acc = json.load(open(accuracy, encoding="utf-8"))["weeks"] if os.path.exists(accuracy) else {}
    avail = availability_pool([acc[k]["availability"] for k in sorted(acc, key=int) if int(k) <= week and acc[k].get("availability")],
                              live=tier_keys())
    import co_gm as CG
    rec = dict(week=week, weeks_used=weeks_used, status=proposal_status(len(weeks_used)), notes=notes,
               team_week_shock=dict(live=CG.arena.TEAM_WEEK_SHOCK, **shock, level_relative=level_relative(shock, level(rows))),
               level=level(rows),
               in_week=dict(by_team=in_week, **between_team_f(in_week),
                            reopen="Council 2026-11-16: re-open per-team streaming in the simulator when F clears its 95% line"),
               weekly_availability=avail,
               board_comparison=board_comparison(avail, board_instruments()),
               method=dict(shock="f = mean over 7 counting cats of actual/mu per team-week; Var(f) = shock^2 + mean(mean_c var/mu^2)/7 "
                                 "(cats independent under no shock, A2); shock = sqrt(excess); bootstrap SE over team-weeks",
                           availability="pooled share of team games played per tier, binomial SE, keyed and judged by the tier's live "
                                        "value; weeks under an earlier value pool in (pooled_from, Council 2026-11-16); from report/accuracy.json",
                           board_comparison="realized tier/healthy ratio, delta-method SE, beside deck, simulator and kit-board ratios; frozen preseason tags",
                           inputs="data/weeks/week_N.json actuals; report/accuracy/lines_weekN.csv + state_weekN.json for the model",
                           rosters="co_gm.team_roster since 2026-11-10: active players plus the team's unpooled players the week's "
                                   "lines carry (auto season lines). Weeks 1-3 have no such player, so their rows are as first fitted"),
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
    L += ["", "## board comparison (realized ratio to healthy, beside each instrument's discount)", "",
          "| through week | tier | measured | SE | n | deck board | simulator | kit board | within 2 SE (deck / sim / kit) |",
          "|---|---|---|---|---|---|---|---|---|"]
    yn = lambda v: "–" if v is None else ("yes" if v else "no")
    for r in recs:
        for t, c in sorted((r.get("board_comparison") or {}).items()):
            w = c["within_2se"]
            L.append(f"| {r['week']} | {t} | {f(c['measured'], 3)} | {f(c['se'], 3)} | {c['n']} | {f(c['deck'], 2)} | "
                     f"{f(c['simulator'], 3)} | {f(c['kit'], 3)} | {yn(w['deck'])} / {yn(w['simulator'])} / {yn(w['kit'])} |")
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
    sh = (f"shock {s['shock']:.4f} ± {s['se']:.4f}" + (f", level-relative {s['level_relative']:.4f}" if s.get("level_relative") else "")
          + f" (live {s['live']})") if s.get("shock") is not None else f"shock: {s.get('note')}"
    tiers = ", ".join(f"{t}: {a['measured']:.2f} ± {a['se']:.2f} (n {a['n']})" for t, a in sorted(av.items()))
    bc = r.get("board_comparison") or {}
    cmp = ", ".join(f"{t} {c['measured']:.2f} ± {c['se']:.2f} vs deck {c['deck']} / sim {c['simulator']} / kit {c['kit']}"
                    for t, c in sorted(bc.items()) if c.get("measured") is not None)
    lv, iw = r.get("level") or {}, r.get("in_week") or {}
    lvl = f"level (actual/model) {lv['overall']:.3f}" if lv.get("overall") is not None else "level: none"
    iwk = f"in-week factor F {iw['F']:.2f} (df {iw['df_between']}, {iw['df_within']})" if iw.get("F") is not None else "in-week factor: none"
    return (f"through week {r['week']}, weeks {r['weeks_used']}, {s.get('n', 0)} team-weeks; {sh}; {lvl}; {iwk}; availability {tiers or 'none'}; "
            f"board comparison {cmp or 'none'}; {r['status']}; proposes only")


if __name__ == "__main__":
    sys.exit(main())
