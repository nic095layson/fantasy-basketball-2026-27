#!/usr/bin/env python3
"""Title odds if IL players return (owner 2026-10-31: "keep main title odds with current roster as is, but take espn
injury return as a variable title odds in a separate section ... I want to keep caution in keeping them as a
constant when in reality it is a variable").

The headline (daily_brief.py, D-IS-8) drops every IL-slot player for the whole season and is not touched here. This
script runs the same simulator with each IL player league-wide counted from the Yahoo week of ESPN's expected return
date, slipped by 0, 2 and 4 weeks, and never (= the headline). A scenario range, never a forecast, never averaged
into the headline.

Method parameters (stated to the owner before the first run; registered in scripts/redteam/constants_registry.json):
  SLIPS         the grid, weeks after ESPN's date: 0, 2, 4 and never
  ROOM_RULE     on a return the team's lowest-value active player (hoops.adj_value, the brief's own "weakest" rule)
                leaves for the rest of the season, so the active roster stays its size; --no-room switches it off
  BLEND_WEIGHTS hand-set weights for the optional blended figure (UNCALIBRATED); the record carries it, the brief
                does not show it unless the owner says so
Dates: ESPN's return date maps to the Yahoo week containing it (co_gm.week_of); a date before the run's date returns
in the run's week; no ESPN row, no date, "out for season" or a week past the regular season = never. Day-To-Day on
IL: ESPN's date as given. A player the simulator's pool lacks stays absent, as the headline leaves him (absent_from_sim).

    SEASON_POOL=data/season/pool_season.csv python3 scripts/il_return.py --date 2026-10-31 [--seasons 10000] [--checks]
"""
import argparse
import datetime as dt
import glob
import json
import math
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import box_pull  # noqa: E402
import co_gm as CG  # noqa: E402

# owner 2026-11-11 (card: "Cancel the two late worlds"): the +2 week and +4 week worlds read the same as on time
# within sampling error (25.81 and 25.86 beside 25.95 on 11-11), so the grid is on time only; never = the headline
SLIPS = {"on_time": 0}
ROOM_RULE = "lowest adj_value active player leaves from the return week"
ROOM_RULE_ON = True   # the rule's default; --no-room switches it off for a run (sweep 2026-10-31: off adds +13.4 title points)
BLEND_WEIGHTS = {"on_time": 0.4, "late_2": 0.3, "late_4": 0.2, "never": 0.1}
SEEDS = (2026, 2027)
STATUS_DIR = os.path.join(KIT, "data", "status")
OUTDIR = os.path.join(KIT, "report", "il_return")


def newest_espn(date, status_dir=STATUS_DIR):
    """The morning ESPN pin for `date`, else the newest pin dated on or before it: (path, rows) or (None, [])."""
    cands = sorted(p for p in glob.glob(os.path.join(status_dir, "espn_injuries_*.json"))
                   if os.path.basename(p)[14:24] <= date and not os.path.basename(p).endswith("_pm.json"))
    if not cands:
        return None, []
    p = cands[-1]
    return p, json.load(open(p, encoding="utf-8")).get("rows", [])


def return_week(ret_date, run_date, weeks, week_of=CG.week_of):
    """The Yahoo week a return date lands in, or None for never (no date, or past the regular season)."""
    if not ret_date:
        return None
    try:
        d = dt.date.fromisoformat(ret_date[:10])
    except ValueError:
        return None
    d = max(d, dt.date.fromisoformat(run_date))
    try:
        w = week_of(d.isoformat())[0]
    except ValueError:
        return None
    return w if w <= weeks else None


def il_players(state, espn_rows, run_date, weeks, aliases=None, by=None):
    """Every IL-slot player league-wide with his ESPN row and base return week: [{seat, team, player, espn, status,
    return_date, week}] (week None = never). With `by` (the pool in use, {name: row}), a team's unpooled IL-slot
    players that the pool has a row for are IL players too (owner pick 2026-11-12, the A-10 re-run's finding: since
    2026-11-09 co_gm.team_roster(include_il=True) simulates them, and off this list they played every week in every
    return world, with no return week and no roster-room drop)."""
    index = box_pull.name_index([r["player"] for r in espn_rows], aliases if aliases is not None else box_pull.load_aliases())
    espn = {r["player"]: r for r in espn_rows}
    out = []
    for t in state["teams"]:
        listed = {p["player"] for p in t["players"]}
        extra = [u for u in t.get("unpooled") or [] if by is not None and u.get("player") in by and u["player"] not in listed]
        for p in list(t["players"]) + extra:
            if p.get("slot") != "IL":
                continue
            hit = box_pull.match_name(p["player"], index)
            r = espn.get(hit) if hit else None
            out.append(dict(seat=t["seat"], team=t["name"], player=p["player"], espn=hit, status=r and r.get("status"),
                            return_date=r and r.get("return_date"), week=return_week(r.get("return_date"), run_date, weeks) if r else None))
    return out


def windows_for(il, slip, ros_all, weeks, room=True, seats=None, value=None):
    """{seat: {player: (from, to)}} for one slip: each IL player from week+slip (never when that passes the season or
    the base week is None); with room, the seat's lowest-value active player leaves from that week (to = week-1)."""
    value = value or (lambda p: CG.hoops.adj_value(p, ()))
    win = {}
    il_names = {(x["seat"], x["player"]) for x in il}
    removed = set()
    for x in sorted(il, key=lambda x: (x["week"] is None, x["week"] or 0, x["player"])):
        s = x["seat"]
        if seats is not None and s not in seats:
            win.setdefault(s, {})[x["player"]] = (weeks + 1, weeks)
            continue
        w = None if x["week"] is None else x["week"] + slip
        if w is None or w > weeks:
            win.setdefault(s, {})[x["player"]] = (weeks + 1, weeks)
            continue
        win.setdefault(s, {})[x["player"]] = (w, weeks)
        if room:
            active = [p for p in ros_all.get(s, []) if (s, p["player"]) not in il_names and (s, p["player"]) not in removed]
            if active:
                weak = min(active, key=value)
                removed.add((s, weak["player"]))
                win[s][weak["player"]] = (1, w - 1)
    return win


def odds(sims):
    t = {str(s): sims[s]["teams"][str(CG.OWNER_SEAT)]["champ"] for s in SEEDS}
    m = sum(t.values()) / len(t)
    return dict(title_by_seed={k: round(v, 2) for k, v in t.items()}, title=round(m, 2),
                playoffs=round(sum(sims[s]["teams"][str(CG.OWNER_SEAT)]["playoff"] for s in SEEDS) / len(SEEDS), 2),
                seed_spread=round(abs(t[str(SEEDS[0])] - t[str(SEEDS[1])]), 2))


def err(m, n):
    return round(196 * math.sqrt(max(m, 0.01) / 100 * (1 - m / 100) / (2 * n)), 2)


def run_scenarios(state, by, il, weeks, seasons, work, room=True, checks=False, seats_only=None):
    ros_head = CG.rosters(state, by)                 # the headline's roster (D-IS-8)
    ros_all = CG.rosters(state, by, include_il=True)
    out = {}
    out["never"] = odds({s: CG.run_league_sim(ros_head, s, seasons, work, tag="h") for s in SEEDS})
    for name, slip in SLIPS.items():
        win = windows_for(il, slip, ros_all, weeks, room=room)
        out[name] = odds({s: CG.run_league_sim(ros_all, s, seasons, work, tag=name, windows=win) for s in SEEDS})
        out[name]["windows"] = {str(k): {p: list(v) for p, v in d.items()} for k, d in sorted(win.items())}
    win = windows_for(il, 0, ros_all, weeks, room=room, seats=[CG.OWNER_SEAT])
    out["seat10_only_on_time"] = odds({s: CG.run_league_sim(ros_all, s, seasons, work, tag="s10", windows=win) for s in SEEDS})
    # owner 2026-11-02 (runner finding 3): the room rule's band, measured on today's inputs so the section can quote it
    win = windows_for(il, 0, ros_all, weeks, room=not room)
    out["on_time_rule_flipped"] = odds({s: CG.run_league_sim(ros_all, s, seasons, work, tag="rf", windows=win) for s in SEEDS})
    if checks:
        # known answers: every IL player back in week 1 with the room rule off = include_il (within sampling error);
        # every IL player back after the last week = the headline exactly
        wk1 = {x["seat"]: {} for x in il}
        for x in il:
            wk1[x["seat"]][x["player"]] = (1, weeks)
        out["check_week1_no_room"] = odds({s: CG.run_league_sim(ros_all, s, seasons, work, tag="c1", windows=wk1) for s in SEEDS})
        out["check_include_il"] = odds({s: CG.run_league_sim(ros_all, s, seasons, work, tag="c2") for s in SEEDS})
        after = {x["seat"]: {} for x in il}
        for x in il:
            after[x["seat"]][x["player"]] = (weeks + 1, weeks)
        out["check_after_last_week"] = odds({s: CG.run_league_sim(ros_all, s, seasons, work, tag="c3", windows=after) for s in SEEDS})
    return out


def known_answers(sc, brief_title, error):
    """Attack A-10's checks on a --checks run (the 2026-10-31 record's, less the one that needed the late worlds retired
    on 2026-11-11). Exact checks compare the two seeds' figures to two decimals: identical rosters, windows and seeds
    must give identical draws. brief_title is the day's brief headline by seed ({seed: title}), or None."""
    by = lambda k: sc[k]["title_by_seed"]
    ch = {}
    if brief_title is not None:
        b = {str(k): round(float(v), 2) for k, v in brief_title.items()}
        ch["never_equals_brief_headline"] = dict(ok=by("never") == b, never=by("never"), brief=b)
    ch["week1_no_room_equals_include_il"] = dict(ok=by("check_week1_no_room") == by("check_include_il"),
                                                 a=by("check_week1_no_room"), b=by("check_include_il"),
                                                 note="exact: identical windows give identical models and draws")
    ch["after_last_week_equals_headline"] = dict(ok=by("check_after_last_week") == by("never"),
                                                 a=by("check_after_last_week"), b=by("never"))
    ch["seat10_only_within_error_of_never_or_above"] = dict(
        ok=sc["seat10_only_on_time"]["title"] >= sc["never"]["title"] - error,
        seat10_only_on_time=sc["seat10_only_on_time"]["title"], never=sc["never"]["title"], error=error,
        note="the owner's own IL players returning must not lower his title odds beyond sampling error")
    ch["seat10_monotonic_within_error"] = dict(ok=None, retired="2026-11-11: the +2 wk and +4 wk worlds are no longer run")
    ch["two_seeds_spread"] = {k: v["seed_spread"] for k, v in sc.items() if isinstance(v, dict) and "seed_spread" in v}
    return ch


def attack_record(rec, checks, deck_head, kit_sha256):
    return dict(attack="A-10 IL-return scenario known answers", date=rec["date"],
                inputs=dict(state=rec["state"], state_as_of=rec["state_as_of"], espn=rec["espn"], pool=rec["pool"],
                            seasons=rec["seasons"], seeds=rec["seeds"], n_il=rec["n_il"]),
                fingerprint=dict(deck_head=deck_head, kit_sha256=kit_sha256),
                checks=checks, verdict="PASS" if all(c.get("ok") is not False for c in checks.values() if isinstance(c, dict) and "ok" in c) else "FAIL")


def room_band(sc, room=True):
    """The room rule's structural band on the on-time title: the figure with the rule flipped minus the figure as run,
    tiered by the kit's thresholds (1 / 2 title points: ROBUST / SENSITIVE / FRAGILE)."""
    if "on_time_rule_flipped" not in sc:
        return None
    shift = round(sc["on_time_rule_flipped"]["title"] - sc["on_time"]["title"], 1)
    tier = "FRAGILE" if abs(shift) >= 2 else "SENSITIVE" if abs(shift) >= 1 else "ROBUST"
    return dict(constant="il_return.ROOM_RULE_ON", shift=shift, label="rule off" if room else "rule on", tier=tier)


def slip_range(sc):
    vals = [sc[k]["title"] for k in ("on_time", "late_2", "late_4") if k in sc]   # a record from before 2026-11-11 carries all three
    return (round(min(vals), 1), round(max(vals), 1)) if vals else None


def blend(sc, weights=BLEND_WEIGHTS):
    """The hand-weighted figure, or None when a weighted world was not run (the late worlds, since 2026-11-11)."""
    if any(k not in sc for k in weights):
        return None
    return round(sum(weights[k] * sc[k]["title"] for k in weights), 2)


def lines(rec):
    """The brief's section, after "Title odds"."""
    sc, e = rec["scenarios"], rec["error"]
    il = rec["il_players"]
    lo, hi = slip_range(sc)
    band = rec.get("room_band") or room_band(sc)
    # owner 2026-11-02 (runner finding 3; council): one range line, since the three slip rows sit within one error bar
    # of each other, and the room rule's band beside it, the two error bars the red-team rule asks for
    L = [f"**If IL players return** (scenario range, not a forecast; ESPN's earliest-return dates of {rec['espn_date']}, all 12 teams, {rec['n_il']} IL players): "
         + (f"if they return ≈{(lo + hi) / 2:.0f}% ({lo:.1f} to {hi:.1f} across on time / +2 wk / +4 wk)" if any(k in sc for k in ("late_2", "late_4"))
            else f"if they return on ESPN's dates ≈{sc['on_time']['title']:.1f}%") + f" · never = headline {sc['never']['title']:.1f}%. "
         f"Error ± {e} each (2 runs × {rec['seasons']:,} seasons). Returns are uncertain; the headline counts the current roster. "
         f"Room rule ({rec['room_rule']}): "
         + (f"**ROOM_RULE_ON is {band['tier']}: {band['shift']:+.1f} ({band['label']})**." if band else "band not measured this run.")]
    by_seat = {}
    for x in il:
        by_seat.setdefault(x["seat"], []).append(x)
    order = sorted(by_seat, key=lambda s: (s != CG.OWNER_SEAT, s))
    for s in order:
        xs = by_seat[s]
        L.append(f"- {xs[0]['team']}: " + "; ".join(f"{x['player']} ({('earliest ' + x['return_date']) if x['return_date'] else 'no ESPN date'}"
                                                    + (f", wk {x['week']}" if x['week'] else ", never") + ")" for x in xs))
    return L


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--seasons", type=int, default=10000)
    ap.add_argument("--no-room", action="store_true", default=not ROOM_RULE_ON, help="switch the roster-room rule off")
    ap.add_argument("--checks", action="store_true", help="also run the known-answer checks (4 more runs)")
    ap.add_argument("--state", default=CG.STATE); ap.add_argument("--status-dir", default=STATUS_DIR); ap.add_argument("--out", default=OUTDIR)
    ap.add_argument("--attack-record", help="with --checks: write attack A-10's known-answer record here (audit F3, 2026-11-12: "
                                            "it carries this script's sha256, so a later change marks the record STALE)")
    ap.add_argument("--brief", help="the day's brief record for the headline check (default report/briefs/brief_<date>.json)")
    a = ap.parse_args(argv)
    if a.attack_record and not a.checks:
        ap.error("--attack-record needs --checks")
    state = json.load(open(a.state, encoding="utf-8"))
    sched = json.load(open(CG.SCHEDULE, encoding="utf-8"))
    weeks = int(sched["regular_season_weeks"])
    espn_path, rows = newest_espn(a.date, a.status_dir)
    if not espn_path:
        print(f"IL RETURN: HALT no ESPN injury pin on or before {a.date} in {os.path.relpath(a.status_dir, KIT)}")
        return 2
    P, by = CG.load_pool()
    il = il_players(state, rows, a.date, weeks, by=by)
    work = tempfile.mkdtemp()
    sc = run_scenarios(state, by, il, weeks, a.seasons, work, room=not a.no_room, checks=a.checks)
    rec = dict(date=a.date, week=CG.week_of(a.date)[0], weeks=weeks, seasons=a.seasons, seeds=list(SEEDS),
               state=os.path.relpath(a.state, KIT), state_as_of=state.get("as_of"), espn=os.path.relpath(espn_path, KIT),
               espn_date=os.path.basename(espn_path)[14:24], pool=os.environ.get("SEASON_POOL"),
               room_rule=ROOM_RULE if not a.no_room else "off (returning players join a larger active roster)",
               slips=SLIPS, n_il=len(il), il_players=il, scenarios=sc, error=err(sc["never"]["title"], a.seasons),
               blend=dict(weights=BLEND_WEIGHTS, title=blend(sc), status="UNCALIBRATED; not shown in the brief; not computed "
                          "since 2026-11-11 (its late worlds are no longer run)"),
               room_band=room_band(sc, room=not a.no_room), slip_range=slip_range(sc),
               label="scenario range, not a forecast; never replaces or averages into the headline")
    rec["lines"] = lines(rec)
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, f"il_return_{a.date}.json")
    json.dump(rec, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("\n".join(rec["lines"]))
    if a.attack_record:
        sys.path.insert(0, os.path.join(HERE, "redteam"))
        import run_attacks as RA
        bp = a.brief or os.path.join(KIT, "report", "briefs", f"brief_{a.date}.json")
        brief_title = json.load(open(bp, encoding="utf-8")).get("title") if os.path.exists(bp) else None
        ar = attack_record(rec, known_answers(sc, brief_title, rec["error"]), RA.live_commit(os.path.abspath(CG.DECK)),
                           RA.kit_fingerprint(["scripts/il_return.py"]))
        os.makedirs(os.path.dirname(os.path.abspath(a.attack_record)), exist_ok=True)
        json.dump(ar, open(a.attack_record, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(f"IL RETURN CHECKS: {ar['verdict']} — " + ", ".join(f"{k} {'ok' if c.get('ok') else 'retired' if c.get('ok') is None else 'FAILED'}"
                                                                 for k, c in ar["checks"].items() if isinstance(c, dict) and "ok" in c)
              + f"; wrote {os.path.relpath(os.path.abspath(a.attack_record), KIT)}")
        if ar["verdict"] != "PASS":
            return 1
    print(f"IL RETURN: PASS wrote {os.path.relpath(path, KIT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
