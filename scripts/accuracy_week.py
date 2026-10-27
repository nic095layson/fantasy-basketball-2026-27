#!/usr/bin/env python3
"""The weekly accuracy card (owner 2026-10-27, "Weekly accuracy card ... build all four parts"): each finished week is
graded and appended to report/accuracy.json (one row per week, never rewritten), report/accuracy.md regenerated.

  1 player lines   the frozen preseason line (the draft lock, deck players_v69.csv) and, from week 3, the in-season
                   line snapshotted the Sunday before the week (report/accuracy/lines_week<N>.csv, weekly_preview
                   --snapshot), each against the week's regular-season box scores: per category the average
                   projection and result, the bias, the mean absolute error and the rank correlation; FG% and FT%
                   pooled as total makes over total attempts. Players with 2+ games in the week (method of the
                   2026-10-27 audit).
  2 availability   the share of his NBA team's games each player played, grouped by the availability the simulator
                   assumes for him (arena.weekly_availability on the frozen line's tag).
  3 your forecasts the owner's pre-week ledger score (report/calibration.json) and the daily card's week
                   (report/calibration_daily.json), carried as they are.
  4 all matchups   every matchup's pre-week forecast (report/calibration_league.json, weekly_preview --league)
                   scored against the week's final category record: Brier of seat a's P(win) (the pairing's first seat).

    python3 scripts/accuracy_week.py --week 1 [--actuals data/actuals] [--out report/accuracy.json]
"""
import argparse
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
DECK = os.path.abspath(os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball"))
FROZEN = os.path.join(DECK, "arena", "results", "players_v69.csv")
ACTUALS = os.path.join(KIT, "data", "actuals")
WEEKS = os.path.join(KIT, "data", "weeks")
OUT = os.path.join(KIT, "report", "accuracy.json")
SNAPSHOTS = os.path.join(KIT, "report", "accuracy")
LEDGER = os.path.join(KIT, "report", "calibration.json")
DAILY = os.path.join(KIT, "report", "calibration_daily.json")
LEAGUE = os.path.join(KIT, "report", "calibration_league.json")
CATS = ("pts", "reb", "ast", "stl", "blk", "tpm", "tov")
MIN_GAMES = 2


class AccuracyError(Exception):
    pass


def _spearman(x, y):
    n = len(x)
    if n < 3:
        return None
    rk = lambda v: {i: r for r, i in enumerate(sorted(range(n), key=lambda i: v[i]))}
    a, b = rk(x), rk(y)
    return 1 - 6 * sum((a[i] - b[i]) ** 2 for i in range(n)) / (n * (n * n - 1))


def grade_lines(lines, games, min_games=MIN_GAMES):
    """lines {name: {cat: per-game, fg_pct, fga, ft_pct, fta}}; games {name: [box rows]}."""
    q = [n for n in games if n in lines and len(games[n]) >= min_games]
    out = dict(players=len(q), cats={}, pct={})
    if not q:
        return out
    for c in CATS:
        pr = [float(lines[n][c]) for n in q]
        ac = [sum(r[c] for r in games[n]) / len(games[n]) for n in q]
        mp, ma = sum(pr) / len(q), sum(ac) / len(q)
        out["cats"][c] = dict(proj=mp, actual=ma, bias_pct=100 * (mp - ma) / ma if ma else None,
                              mae=sum(abs(p - a) for p, a in zip(pr, ac)) / len(q), rank_corr=_spearman(pr, ac))
    for c, m, a in (("fg_pct", "fgm", "fga"), ("ft_pct", "ftm", "fta")):
        att = sum(float(lines[n][a]) for n in q)
        made, tried = sum(r[m] for n in q for r in games[n]), sum(r[a] for n in q for r in games[n])
        out["pct"][c] = dict(proj=sum(float(lines[n][c]) * float(lines[n][a]) for n in q) / att if att else None,
                             actual=made / tried if tried else None, attempts=tried)
    return out


def grade_availability(tier, team, played, team_games):
    """tier {name: assumed availability}; team {name: NBA team}; played {name: games}; team_games {team: games}."""
    out = {}
    for n, t in tier.items():
        tg = team_games.get(team.get(n), 0)
        if not tg:
            continue
        k = f"{t:.2f}"
        r = out.setdefault(k, dict(assumed=round(t, 2), played=0, team_games=0, share=0.0))
        r["played"] += played.get(n, 0); r["team_games"] += tg
    for r in out.values():
        r["share"] = r["played"] / r["team_games"]
    return out


def grade_matchups(forecast, week):
    """forecast {"pairs": [{a, b, p_win (seat a), exp_cats}]} or None; week = data/weeks/week_N.json."""
    if not forecast:
        return dict(n=0, note="no pre-week forecast recorded for this week")
    by_seat = {t["seat"]: t for t in week["teams"].values()}
    rows = []
    for p in forecast["pairs"]:
        s = by_seat[p["a"]]["yahoo_score"]
        won = 1 if s["wins"] >= 5 else 0
        rows.append(dict(a=p["a"], b=p["b"], p_win=p["p_win"], won=won, cats_won=s["wins"], exp_cats=p.get("exp_cats"),
                         brier=(p["p_win"] - won) ** 2))
    return dict(n=len(rows), brier=sum(r["brier"] for r in rows) / len(rows), rows=rows)


def append(path, week, row):
    rec = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {"weeks": {}}
    if str(week) in rec["weeks"]:
        raise AccuracyError(f"week {week} is already graded in {path}; the record is append-only")
    rec["weeks"][str(week)] = row
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False); f.write("\n")
    return rec


def _weeks():
    import importlib.util
    spec = importlib.util.spec_from_file_location("build_schedule", os.path.join(KIT, "report", "schedule", "build_schedule.py"))
    bs = importlib.util.module_from_spec(spec); spec.loader.exec_module(bs)
    return [(n, s.isoformat(), e.isoformat()) for n, s, e in bs.weeks()]


def week_games(week, actuals):
    """{pool name: [box rows]} and {team: games} from the week's regular-season box-score days."""
    import datetime
    s, e = next((s, e) for n, s, e in _weeks() if n == week)
    d, end = datetime.date.fromisoformat(s), datetime.date.fromisoformat(e)
    games, team_games, seen, days = {}, {}, set(), []
    while d <= end:
        p = os.path.join(actuals, f"{d.isoformat()}.json")
        if os.path.exists(p):
            a = json.load(open(p, encoding="utf-8"))
            if all(g.get("season_type") == 2 for g in a.get("games", [])) and a.get("games"):
                days.append(d.isoformat())
                for r in a["players"]:
                    if (r["team"], r["game"]) not in seen:
                        seen.add((r["team"], r["game"])); team_games[r["team"]] = team_games.get(r["team"], 0) + 1
                    if r.get("pool_name") and not r.get("dnp"):
                        games.setdefault(r["pool_name"], []).append(r)
        d += datetime.timedelta(days=1)
    return games, team_games, days


def _lines(path):
    with open(path, encoding="utf-8") as f:
        return {r["player"]: r for r in csv.DictReader(f)}


def grade_snapshots(week, games, snapshots):
    """The in-season line snapshotted the Sunday before the week and, beside it, the minutes-trend candidate
    (owner 2026-10-27, build 2: lines_week<N>_mt.csv); a missing file is named, never substituted."""
    out = {}
    for key, name, what in (("in_season", f"lines_week{week}.csv", "in-season snapshot"),
                            ("candidate_minutes", f"lines_week{week}_mt.csv", "minutes-trend candidate snapshot")):
        p = os.path.join(snapshots, name)
        out[key] = grade_lines(_lines(p), games) if os.path.exists(p) else dict(note=f"no {what} recorded before this week")
    return out


def grade_week_lines(week, actuals, frozen):
    games, _, days = week_games(week, actuals)
    return dict(grade_lines(_lines(frozen), games), days=days)


def run(week, actuals=ACTUALS, out=OUT, frozen=FROZEN, weeks_dir=WEEKS, ledger=LEDGER, daily=DAILY, league=LEAGUE,
        snapshots=SNAPSHOTS):
    games, team_games, days = week_games(week, actuals)
    flines = _lines(frozen)
    row = dict(week=week, days=days, method=dict(min_games=MIN_GAMES, frozen=os.path.basename(frozen)))
    row["lines"] = dict(preseason=grade_lines(flines, games), **grade_snapshots(week, games, snapshots))
    for d in (os.path.join(DECK, "scripts"), os.path.join(DECK, "arena")):
        if d not in sys.path:
            sys.path.insert(0, d)
    import arena
    tier = {n: arena.weekly_availability(p) for n, p in flines.items()}
    row["availability"] = grade_availability(tier, {n: p["team"] for n, p in flines.items()},
                                             {n: len(g) for n, g in games.items()}, team_games)
    led = json.load(open(ledger, encoding="utf-8")) if os.path.exists(ledger) else {"weeks": {}}
    dl = json.load(open(daily, encoding="utf-8")) if os.path.exists(daily) else {"weeks": {}}
    w = led["weeks"].get(str(week)) or {}
    d = dl["weeks"].get(str(week)) or {}
    row["owner"] = dict(p_win=w.get("p_win"), exp_cats=w.get("exp_cats"), score=w.get("score"),
                        daily=dict(n_forecasts=d.get("n_forecasts"), brier=d.get("brier"), baseline_brier=d.get("baseline_brier"),
                                   skill=d.get("skill")) if d else None)
    lg = json.load(open(league, encoding="utf-8")) if os.path.exists(league) else {"weeks": {}}
    with open(os.path.join(weeks_dir, f"week_{week}.json"), encoding="utf-8") as f:
        row["matchups"] = grade_matchups(lg["weeks"].get(str(week)), json.load(f))
    rec = append(out, week, row)
    with open(out[:-5] + ".md", "w", encoding="utf-8") as f:
        f.write(render(rec))
    return row


def render(rec):
    f = lambda v, p=2: "–" if v is None else f"{v:.{p}f}"
    L = ["# Forecast accuracy — week by week", "",
         "Each finished week graded against the box scores and the final scores (`scripts/accuracy_week.py`; "
         "`report/accuracy.json` is the record, one row per week, never rewritten). Players with 2+ games in the week.", ""]
    L += ["## Player lines: points per game (projected / actual, bias, MAE, rank correlation)", "",
          "| week | players | preseason | bias | MAE | rank | in-season | bias | MAE | rank | minutes candidate | bias | MAE | rank |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    cell = lambda s: (f"{f(s.get('proj'))} / {f(s.get('actual'))} | {f(s.get('bias_pct'), 1)}% | {f(s.get('mae'))} | {f(s.get('rank_corr'))}"
                      if s else "no snapshot | | | ")
    for k in sorted(rec["weeks"], key=int):
        r = rec["weeks"][k]["lines"]
        L.append(f"| {k} | {r['preseason']['players']} | " + " | ".join(cell(r[x].get("cats", {}).get("pts", {})) for x in ("preseason", "in_season", "candidate_minutes")) + " |")
    L += ["", "Switch rule (D-ML-1, pre-committed 2026-10-27): the minutes candidate replaces nothing until its MAE beats the "
          "in-season line's on PTS, REB and AST in 3 of 4 consecutive graded weeks, on the owner's word."]
    L += ["", "## Availability: share of team games played, by the tier the simulator assumes", "",
          "| week | tier | assumed | played / team games | share |", "|---|---|---|---|---|"]
    for k in sorted(rec["weeks"], key=int):
        for t, a in sorted(rec["weeks"][k]["availability"].items()):
            L.append(f"| {k} | {t} | {a['assumed']:.2f} | {a['played']} / {a['team_games']} | {a['share']:.2f} |")
    L += ["", "## Forecasts", "", "| week | your P(win) | result | daily card Brier vs lead | league matchups scored | league Brier |",
          "|---|---|---|---|---|---|"]
    for k in sorted(rec["weeks"], key=int):
        r = rec["weeks"][k]; o = r["owner"]; m = r["matchups"]; sc = o.get("score") or {}
        dly = o.get("daily") or {}
        L.append(f"| {k} | {f(o.get('p_win'), 3)} | {sc.get('cats_won', '–')} cats | {f(dly.get('brier'), 3)} vs {f(dly.get('baseline_brier'), 3)} | "
                 f"{m.get('n', 0)} | {f(m.get('brier'), 3)} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--week", type=int, required=True)
    ap.add_argument("--actuals", default=ACTUALS); ap.add_argument("--out", default=OUT)
    ap.add_argument("--weeks-dir", default=WEEKS); ap.add_argument("--league", default=LEAGUE)
    ap.add_argument("--ledger", default=LEDGER); ap.add_argument("--daily", default=DAILY)
    a = ap.parse_args()
    try:
        r = run(a.week, a.actuals, a.out, weeks_dir=a.weeks_dir, ledger=a.ledger, daily=a.daily, league=a.league)
    except (AccuracyError, OSError, ValueError, KeyError, StopIteration) as e:
        print(f"ACCURACY: FAIL — {e}"); return 1
    print(f"ACCURACY: PASS — {summary(r)}")
    return 0


def summary(r):
    p = r["lines"]["preseason"]
    pts = p["cats"].get("pts")
    m = r["matchups"]
    return (f"week {r['week']}: {p['players']} players" + (f", points {pts['proj']:.2f} projected / {pts['actual']:.2f} actual" if pts else "")
            + f"; {m.get('n', 0)} league matchup(s) scored" + (f" (Brier {m['brier']:.3f})" if m.get("n") else ""))


if __name__ == "__main__":
    sys.exit(main())
