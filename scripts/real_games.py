#!/usr/bin/env python3
"""The week model on each NBA team's real games (owner 2026-10-27, build 5, first slice): arena.team_week_model line
for line, with one substitution — a player's expected games are his NBA team's games in the fantasy week's window
(report/schedule/games-2026-27.csv) times his availability, not a flat 3.5 x availability. The engine's daily-fill
weights, availability tiers, category list and percentage-mix constant are IMPORTED, never copied, so the only thing
that can differ is the games count; test_real_games.DriftCheck proves the two models agree to the last digit at 3.5.

A team the window lists no games for (a code the schedule does not carry) gets the flat 3.5 and is named; it is
never silently dropped. A two-week matchup (weeks 7 and 17) takes the real count over its whole window, where the
flat 3.5 was known to be wrong.

CANDIDATE ONLY: the pre-week league forecast on this model is recorded in report/calibration_league_real.json beside
the flat one and graded by the Monday accuracy card (column matchups_real); nothing live reads it. Switch rule,
pre-committed (D-RG-1): lower Brier than the flat forecast over at least 4 consecutive graded weeks, on the owner's word.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import co_gm as CG  # noqa: E402

FLAT = 3.5


def team_week_model_games(roster, cv, games, report=False):
    """Per-category weekly (mu, var) as arena.team_week_model, with g = games[team] * a. games: {NBA code: games in
    the window}. With report=True also returns the sorted list of NBA codes that fell back to the flat count."""
    arena, hoops = CG.arena, CG.hoops
    cv = arena.CV if cv is None else cv
    mu = {c: 0.0 for c in arena.CATS}
    var = {c: 0.0 for c in arena.CATS}
    lw = arena.daily_fill_weights(roster)
    fg_mk = fg_at = ft_mk = ft_at = 0.0
    unscheduled = set()
    for p in roster:
        w = lw.get(id(p), 1.0)
        a = arena.weekly_availability(p)
        n = games.get(p["team"])
        if n is None:
            unscheduled.add(p["team"]); n = FLAT
        g = n * a
        g_var = n * a * (1 - a)
        for c, col in hoops.COUNT_COLS.items():
            x = p[col]
            mu[c] += w * x * g
            var[c] += w * ((x * cv[c]) ** 2 * g + x ** 2 * g_var)
        fg_mk += w * p["fg_pct"] * p["fga"] * g
        fg_at += w * p["fga"] * g
        ft_mk += w * p["ft_pct"] * p["fta"] * g
        ft_at += w * p["fta"] * g
    p_fg = fg_mk / (fg_at or 1)
    p_ft = ft_mk / (ft_at or 1)
    mu["FG%"] = p_fg
    var["FG%"] = (arena.PCT_MIX_INFL ** 2) * max(p_fg * (1 - p_fg), 1e-4) / (fg_at or 1)
    mu["FT%"] = p_ft
    var["FT%"] = (arena.PCT_MIX_INFL ** 2) * max(p_ft * (1 - p_ft), 1e-4) / (ft_at or 1)
    return (mu, var, sorted(unscheduled)) if report else (mu, var)


def week_window(week):
    import importlib.util
    spec = importlib.util.spec_from_file_location("build_schedule", os.path.join(CG.KIT, "report", "schedule", "build_schedule.py"))
    bs = importlib.util.module_from_spec(spec); spec.loader.exec_module(bs)
    for n, s, e in bs.weeks():
        if n == week:
            return s.isoformat(), e.isoformat()
    raise ValueError(f"week {week} is not in the calendar")


def week_games(week, games=None):
    """{NBA code: games in the fantasy week's window} from the schedule file."""
    s, e = week_window(week)
    return CG.games_left(games if games is not None else CG.load_games(), s, e)
