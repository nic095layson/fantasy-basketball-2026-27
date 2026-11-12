#!/usr/bin/env python3
"""The threes-split candidate line (owner 2026-11-12, card: "Split threes into attempts and %"): the live season line
with one column rebuilt. The blend treats threes made as a count with a prior worth season_lines.PRIOR_GAMES["3PM"]
games, so a cold fortnight pulls a shooter's line down as fast as a real change of role would. This candidate separates
the part that settles quickly (attempts) from the part that settles slowly (the percentage):

    prior percentage  = (PCT_PRIOR_K x PCT_PRIOR_MU + his 2025-26 makes) / (PCT_PRIOR_K + his 2025-26 attempts)
                        (data/reference/threes_prior_2025-26.csv, Basketball-Reference season totals; used only at
                        MIN_PRIOR_ATT attempts or more). One season of threes is itself a small sample, so last
                        season's mark is pulled toward the league before it is used (owner pick 2026-11-12,
                        "Re-centre it").
    prior weight      = PCT_PRIOR_K + his 2025-26 attempts   (what that pulled percentage is worth, in attempts)
    prior attempts    = the preseason line's threes made / the prior percentage   (the projection's own volume)
    attempts per game = (ATT_PRIOR_GAMES x prior attempts + this season's attempts) / (ATT_PRIOR_GAMES + games)
    percentage        = (prior weight x prior percentage + this season's makes) / (prior weight + this season's attempts)
    candidate threes  = attempts per game x percentage

With no games the candidate equals the preseason line (the prior attempts times the prior percentage is the preseason
threes by construction). Only `tpm` changes; points, FG% and every other column are the live line's. A player with no
2025-26 row, under MIN_PRIOR_ATT attempts, or no preseason threes keeps the live line and is listed as unsplit.

ATT_PRIOR_GAMES is read live from the blend (its own threes prior), so attempts move at the speed threes move today.
PCT_PRIOR_K and PCT_PRIOR_MU are fitted together (report/after-reports/threes-prior-fit-2026-11-12/): the beta-binomial
strength and mean of three-point talent among the 307 players with 100+ attempts in 2025-26, 356 (95% 249 to 635) and
.3581. The mean is the fit's, not makes over attempts (.363), which leans toward the high-volume shooters. It replaces the owner-supplied flat
750 of the first version; on this season's first four weeks the flat weight could not be told from 400, and the
pulled centre beat the raw one. The line is still a graded candidate (D-TS-1).

CANDIDATE ONLY: nothing on the board, in the brief or in the simulator reads these files. The Sunday step snapshots
them (report/accuracy/lines_week<N>_3s.csv) and the Monday accuracy card grades them beside the blend on threes made.

Writes data/season/pool_season_3s.csv (deck schema), projections_season_3s.csv (kit schema) and
data/season/threes_line_<date>.json. Red-first tests: test_threes_line.py.

    python3 scripts/threes_line.py --date 2026-11-12 [--through DATE] [--actuals DIR] [--out-dir DIR]
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
import box_pull  # noqa: E402

SEASON = os.path.join(KIT, "data", "season")
ACTUALS = os.path.join(KIT, "data", "actuals")
POOL = os.path.join(SEASON, "pool_season.csv")
KIT_CSV = os.path.join(SEASON, "projections_season.csv")
PRE_KIT = os.path.join(KIT, "report", "projections-2026-27.csv")   # the preseason threes (never edited in season)
PRIOR = os.path.join(KIT, "data", "reference", "threes_prior_2025-26.csv")

PCT_PRIOR_K = 356.0     # attempts of league-average shooting a 2025-26 percentage is pulled toward (fitted, see the docstring)
PCT_PRIOR_MU = 0.3581   # that league average: the fitted mean of three-point talent, 2025-26, 100+ attempts
MIN_PRIOR_ATT = 100     # a 2025-26 percentage on fewer attempts than this is not used (hand-set, uncalibrated: D-TS-1)


def att_prior_games():
    """The blend's own threes prior, read live (season_lines.PRIOR_GAMES['3PM'])."""
    import season_lines as SL
    return float(SL.PRIOR_GAMES["3PM"])


def season_threes(actuals_dir=ACTUALS, through=None):
    """{pool name: (games, makes, attempts)} over regular-season box scores, DNPs excluded (season_lines' rules)."""
    out = {}
    for path in sorted(glob.glob(os.path.join(actuals_dir, "*.json"))):
        a = json.load(open(path, encoding="utf-8"))
        if through and (a.get("date") or "") > through:
            continue
        if not a.get("games") or not all(g.get("season_type") == 2 for g in a["games"]):
            continue
        for r in a.get("players", []):
            if r.get("pool_name") and not r.get("dnp") and r.get("min", 0) > 0:
                t = out.setdefault(r["pool_name"], [0, 0, 0])
                t[0] += 1; t[1] += r.get("tpm", 0) or 0; t[2] += r.get("tpa", 0) or 0
    return {k: tuple(v) for k, v in out.items()}


def read_prior(path=PRIOR):
    with open(path, encoding="utf-8", newline="") as f:
        return [dict(player=r["player"], games=int(r["games"]), fg3=int(r["fg3"]), fg3a=int(r["fg3a"])) for r in csv.DictReader(f)]


def prior_pct(names, prior_rows, aliases=None, min_att=MIN_PRIOR_ATT):
    """{line name: 2025-26 percentage} for the names that resolve to a prior row with min_att attempts or more."""
    index = box_pull.name_index([r["player"] for r in prior_rows], aliases if aliases is not None else box_pull.load_aliases())
    by = {r["player"]: r for r in prior_rows}
    out = {}
    for n in names:
        hit = box_pull.match_name(n, index)
        r = by.get(hit) if hit else None
        if r and r["fg3a"] >= min_att:
            out[n] = r["fg3"] / r["fg3a"]
    return out


def prior_centre(names, prior_rows, aliases=None, min_att=MIN_PRIOR_ATT, k=PCT_PRIOR_K, mu=PCT_PRIOR_MU):
    """({line name: pulled 2025-26 percentage}, {line name: its weight in attempts}, league percentage) for the names
    that resolve to a prior row with min_att attempts or more."""
    index = box_pull.name_index([r["player"] for r in prior_rows], aliases if aliases is not None else box_pull.load_aliases())
    by = {r["player"]: r for r in prior_rows}
    pct, weight = {}, {}
    for n in names:
        hit = box_pull.match_name(n, index)
        r = by.get(hit) if hit else None
        if r and r["fg3a"] >= min_att:
            pct[n] = (k * mu + r["fg3"]) / (k + r["fg3a"])
            weight[n] = k + r["fg3a"]
    return pct, weight, mu


def preseason_tpm(path=PRE_KIT):
    with open(path, encoding="utf-8", newline="") as f:
        out = {}
        for r in csv.DictReader(f):
            try:
                out[r["name"]] = float(r["tpm"])
            except (ValueError, KeyError, TypeError):
                out[r["name"]] = None
        return out


def line_names(*paths_cols):
    out = []
    for path, col in paths_cols:
        with open(path, encoding="utf-8", newline="") as f:
            out += [r[col] for r in csv.DictReader(f)]
    return sorted(set(out))


def resolve_pre(names, pre_raw, aliases=None):
    """{line name: preseason threes}: the deck plane and the kit plane spell some names differently ("Cameron Johnson" /
    "Cam Johnson"), so each line name is looked up in the preseason file through the box puller's alias index."""
    index = box_pull.name_index(list(pre_raw), aliases if aliases is not None else box_pull.load_aliases())
    out = {}
    for n in names:
        hit = n if n in pre_raw else box_pull.match_name(n, index)
        if hit is not None:
            out[n] = pre_raw.get(hit)
    return out


def split(pre_tpm, pct0, games, makes, attempts, att_prior, pct_prior=PCT_PRIOR_K):
    """(threes per game, attempts per game, percentage) for one player, or None when he cannot be split."""
    if pre_tpm is None or not pct0 or pre_tpm <= 0:
        return None
    att0 = pre_tpm / pct0
    att = (att_prior * att0 + attempts) / (att_prior + games)
    pct = (pct_prior * pct0 + makes) / (pct_prior + attempts)
    return att * pct, att, pct


def build(lines_csv, pre, pct0, threes, att_prior=None, pct_prior=PCT_PRIOR_K, name_col="player", league=None):
    """pct_prior: the prior percentage's weight in attempts, one number for everyone or {name: weight}."""
    att_prior = att_prior_games() if att_prior is None else att_prior
    weight = (lambda n: pct_prior.get(n, PCT_PRIOR_K)) if isinstance(pct_prior, dict) else (lambda n: pct_prior)
    with open(lines_csv, encoding="utf-8", newline="") as f:
        rd = csv.DictReader(f); fields = rd.fieldnames; rows = list(rd)
    out, detail, unsplit = [], {}, []
    for r in rows:
        name = r[name_col]; g, m, a = threes.get(name, (0, 0, 0))
        s = split(pre.get(name), pct0.get(name), g, m, a, att_prior, weight(name))
        if s is None:
            unsplit.append(name); out.append(dict(r)); continue
        new = dict(r); new["tpm"] = f"{s[0]:.1f}"
        try:
            live = float(r["tpm"])
        except (ValueError, TypeError):
            live = None
        detail[name] = dict(live=live, candidate=round(s[0], 2), attempts=round(s[1], 2), pct=round(s[2], 4),
                            prior_pct=round(pct0[name], 4), prior_weight=round(weight(name), 1), games=g, makes=m, att=a)
        out.append(new)
    return dict(rows=out, fields=fields, detail=detail, unsplit=sorted(unsplit),
                method=dict(att_prior_games=att_prior, pct_prior_k=PCT_PRIOR_K if isinstance(pct_prior, dict) else None,
                            pct_prior_weight="PCT_PRIOR_K + 2025-26 attempts, per player" if isinstance(pct_prior, dict) else pct_prior,
                            league_pct=None if league is None else round(league, 4), min_prior_att=MIN_PRIOR_ATT,
                            rule="tpm = blended attempts x shrunk percentage; the prior percentage is last season's pulled "
                                 "toward the league; every other column is the live line's"))


def write_csv(path, rows, fields):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); w.writeheader(); w.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--actuals", default=ACTUALS); ap.add_argument("--out-dir", default=SEASON)
    ap.add_argument("--pool", default=POOL); ap.add_argument("--kit", default=KIT_CSV); ap.add_argument("--pre-kit", default=PRE_KIT)
    ap.add_argument("--prior", default=PRIOR)
    ap.add_argument("--through", default=None, help="use box records dated on or before this (default: all on disk)")
    a = ap.parse_args()
    try:
        threes = season_threes(a.actuals, a.through); prior = read_prior(a.prior)
        names = line_names((a.pool, "player"), (a.kit, "name"))
        pre = resolve_pre(names, preseason_tpm(a.pre_kit)); pct0, wt, mu = prior_centre(names, prior)
        threes = dict(threes, **{n: v for n, v in resolve_pre(names, threes).items() if v is not None})   # the box scores' spelling
        rec = build(a.pool, pre, pct0, threes, pct_prior=wt, league=mu)
        kit = build(a.kit, pre, pct0, threes, pct_prior=wt, name_col="name", league=mu)
    except (OSError, ValueError, KeyError) as e:
        print(f"THREES LINE: FAIL — {e}"); return 1
    os.makedirs(a.out_dir, exist_ok=True)
    write_csv(os.path.join(a.out_dir, "pool_season_3s.csv"), rec["rows"], rec["fields"])
    write_csv(os.path.join(a.out_dir, "projections_season_3s.csv"), kit["rows"], kit["fields"])
    moved = sorted(((n, d) for n, d in rec["detail"].items() if d["live"] is not None), key=lambda x: -abs(x[1]["candidate"] - x[1]["live"]))
    out = dict(date=a.date, through=a.through, players=len(rec["rows"]), split=len(rec["detail"]), unsplit=rec["unsplit"],
               method=rec["method"], detail=rec["detail"],
               biggest_moves=[dict(player=n, live=d["live"], candidate=d["candidate"]) for n, d in moved[:20]],
               inputs=dict(pool=os.path.relpath(a.pool, KIT), kit=os.path.relpath(a.kit, KIT), pre_kit=os.path.relpath(a.pre_kit, KIT),
                           prior=os.path.relpath(a.prior, KIT)))
    with open(os.path.join(a.out_dir, f"threes_line_{a.date}.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False); f.write("\n")
    up = sum(1 for _, d in moved if d["candidate"] - d["live"] >= 0.2); down = sum(1 for _, d in moved if d["candidate"] - d["live"] <= -0.2)
    print(f"THREES LINE: PASS — {a.date}: {out['players']} players, {out['split']} split, {len(rec['unsplit'])} unsplit (no 2025-26 percentage "
          f"on {MIN_PRIOR_ATT}+ attempts or no preseason threes); candidate above the live line by 0.2+ for {up}, below for {down}; "
          f"candidate only, wrote pool_season_3s.csv, projections_season_3s.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
