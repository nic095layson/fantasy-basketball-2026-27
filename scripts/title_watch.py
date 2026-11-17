#!/usr/bin/env python3
"""The overnight title check (audit item F5, owner 2026-11-10). On 2026-11-10 the title share read 12.3% against
18.0% the morning before, and the reasons (a kit merge that put auto-row players in the simulator, a pool change and
one IL return on another team) had to be traced by hand. This step compares the day's brief with the one before it
and, when the share moved by more than the sampling error of the difference, names what changed between the two
runs: the kit merges that reached this checkout, and the league's roster moves on the day's brief. Owner 2026-11-16
("Mark method changes"): a change of method between the runs (the season line's minutes switch, or a registered
constant added, removed or changed) is named first, as METHOD CHANGE, so it is not read as a league result.

Owner 2026-11-17 (pick F1, after-report-2026-11-17-gaps-and-fixes.md): on a day with a method change the two figures
are also walked like for like, on today's engine and one input at a time: the earlier run's own state, lines and
schedule (read from the commit that added its brief); then today's rosters and results on the earlier lines; then
today's brief. On 2026-11-17 the watch printed "-0.5, within the band" over +1.9 (constants), +1.9 (rosters and
results) and -4.3 (the minutes switch reaching the lines file). Three runs of the simulator, each in its own process,
the brief's seeds and seasons; today's row must reproduce the brief or no walk is shown.

Display only: it reads two briefs, git history and (for the walk) the simulator, and changes neither the brief nor any
figure. Without a method change it names what changed and does not split the move between the causes.

Band: each brief's share is the mean of two runs of n seasons, with sampling error 1.96 * sqrt(p(1-p)/(2n))
(daily_brief.odds_line). The difference of two such shares has error sqrt(e_today^2 + e_before^2). No new constant.

    python3 scripts/title_watch.py --date 2026-11-10 [--no-walk]
Prints 'TITLE WATCH: PASS — ...' (exit 0) or 'TITLE WATCH: HALT — <why>' (exit 1, only when the day has no brief).
"""
import argparse
import datetime as dt
import glob
import json
import math
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
BRIEFS = os.path.join(KIT, "report", "briefs")
OWNER_SEAT = 10


def _share(b):
    t = b.get("title") or {}
    return sum(t.values()) / len(t) if t else None


def _err(p, n):
    return 196 * math.sqrt(p / 100 * (1 - p / 100) / (2 * n))


def prev_brief(date, briefs=BRIEFS):
    """The newest morning brief dated before `date` (afternoon files are never read), or None."""
    days = sorted(m.group(1) for p in glob.glob(os.path.join(briefs, "brief_*.json"))
                  for m in [re.fullmatch(r"brief_(\d{4}-\d{2}-\d{2})\.json", os.path.basename(p))] if m and m.group(1) < date)
    return os.path.join(briefs, f"brief_{days[-1]}.json") if days else None


def kit_merges(root, since):
    """Subjects of the pull-request merges that reached this checkout after `since` (ISO time of the earlier run),
    oldest first. None when it cannot be read (no time, no git history): the caller says so."""
    if not since:
        return None
    def git(*a):
        return subprocess.run(["git", "-C", root] + list(a), capture_output=True, text=True, check=True).stdout
    try:
        base = git("rev-list", "-1", "--first-parent", f"--before={since}", "HEAD").strip()
        if not base:
            return None
        out = git("log", "--merges", "--reverse", "--format=%s", f"{base}..HEAD")
    except (subprocess.CalledProcessError, OSError):
        return None
    return [s for s in out.splitlines() if s.startswith("Merge pull request")]


SEASON = os.path.join(KIT, "data", "season")
REGISTRY = os.path.join("scripts", "redteam", "constants_registry.json")


def line_method_changes(prev_rec, rec):
    """Owner 2026-11-16 ("Mark method changes"): what changed in how the season line is made between two days'
    season-lines records (season_lines_<date>.json). Today: which columns carry the minutes ratio (line_switch)."""
    if prev_rec is None:
        return ["line method: no season-lines record for the earlier run"]
    if rec is None:
        return ["line method: no season-lines record for this run"]
    cats = lambda r: [c.upper() for c in ((r.get("line_switch") or {}).get("cats") or [])]
    a, b = cats(prev_rec), cats(rec)
    if a == b:
        return []
    return [f"line method: the minutes ratio now applies to {', '.join(b) or 'no column'} (before: {', '.join(a) or 'none'})"]


def registry_changes(old, new):
    """Registered constants (scripts/redteam/constants_registry.json rows) changed, added or removed between two runs."""
    key = lambda r: f"{r['module']}.{r['name']}"
    o, n = {key(r): r.get("value") for r in old}, {key(r): r.get("value") for r in new}
    out = [f"constant {k}: {o[k]} to {n[k]}" for k in n if k in o and o[k] != n[k]]
    out += [f"constant {k} added" for k in n if k not in o]
    return out + [f"constant {k} removed" for k in o if k not in n]


def registry_at(root, since):
    """The constants registry as it stood at the newest first-parent commit before `since`, or None when unreadable."""
    if not since:
        return None
    try:
        g = lambda *a: subprocess.run(["git", "-C", root] + list(a), capture_output=True, text=True, check=True).stdout
        base = g("rev-list", "-1", "--first-parent", f"--before={since}", "HEAD").strip()
        return json.loads(g("show", f"{base}:{REGISTRY}"))["constants"] if base else None
    except (subprocess.CalledProcessError, OSError, ValueError, KeyError):
        return None


# owner 2026-11-17 (F1): the three inputs a title share is made from, as paths inside the checkout
INPUT_PATHS = dict(state="data/league_state.json", pool="data/season/pool_season.csv", schedule="data/league_schedule.json")
WALK_STEPS = ("the engine and its constants, on the earlier run's inputs", "rosters and results recorded since",
              "the lines file (line method and the day's games)")


def inputs_at(root, date):
    """The state, lines and schedule files as the morning run of `date` committed them: read from the commit that
    added that day's brief (a later afternoon commit overwrites the state). {name: temp file path}, or None when git
    cannot give all three."""
    try:
        g = lambda *a: subprocess.run(["git", "-C", root] + list(a), capture_output=True, check=True).stdout
        commit = g("log", "--diff-filter=A", "--format=%H", "-n", "1", "--", f"report/briefs/brief_{date}.json").decode().strip()
        if not commit:
            return None
        d, out = tempfile.mkdtemp(prefix="title_watch_"), {}
        for k, rel in INPUT_PATHS.items():
            out[k] = os.path.join(d, os.path.basename(rel))
            with open(out[k], "wb") as f:
                f.write(g("show", f"{commit}:{rel}"))
        return out
    except (subprocess.CalledProcessError, OSError):
        return None


def _sim(state, pool, schedule, seasons):
    """One row of the walk: the owner's title share for a state, a lines file and a schedule, in its own process so
    the pool and the schedule of one row cannot reach the next (co_gm.pool_guard; the 11-10 trace ran two rows on the
    wrong pool that way)."""
    env = dict(os.environ, SEASON_POOL=os.path.abspath(pool))
    out = subprocess.run([sys.executable, os.path.abspath(__file__), "--sim", os.path.abspath(state), os.path.abspath(schedule), str(int(seasons))],
                         capture_output=True, text=True, check=True, env=env).stdout
    t = json.loads(out.strip().splitlines()[-1])
    return sum(t.values()) / len(t)


SIM = _sim   # the tests put a stand-in here


def _sim_main(argv):
    """`title_watch.py --sim STATE SCHEDULE SEASONS` with SEASON_POOL set: prints {seed: owner's title share}."""
    import co_gm as CG
    import daily_brief as DB
    state_p, sched_p, seasons = argv[0], argv[1], int(argv[2])
    CG.SCHEDULE = os.path.abspath(sched_p)
    _, by = CG.load_pool()
    with open(state_p, encoding="utf-8") as f:
        ros = CG.rosters(json.load(f), by)
    work = tempfile.mkdtemp()
    print(json.dumps({str(s): CG.run_league_sim(ros, s, seasons, work, tag="walk")["teams"][str(CG.OWNER_SEAT)]["champ"] for s in DB.SEEDS}))
    return 0


def walk(prev_title, title, rows):
    """The like-for-like walk from the earlier brief to today's. rows: the three re-runs on today's engine
    (prev_inputs: the earlier run's state, lines and schedule; rosters: today's state and schedule on the earlier
    lines; today: today's own inputs). Today's row is the known answer: same inputs, seeds and seasons as the brief, so
    it must equal the brief's share to two decimals, or the walk is not shown."""
    out = dict(rows=dict(rows), steps=[], reproduced=abs(rows["today"] - title) < 0.005, error=None)
    if not out["reproduced"]:
        out["error"] = (f"today's brief did not reproduce on a re-run of its own inputs ({rows['today']:.2f} against "
                        f"{title:.2f}): no walk is shown")
        return out
    stops = (rows["prev_inputs"], rows["rosters"], title)
    out["steps"] = [dict(what=w, delta=to - frm, to=to) for w, frm, to in zip(WALK_STEPS, (prev_title,) + stops[:2], stops)]
    return out


def like_for_like(root, prev_date, prev_title, title, today, seasons, sim=None):
    """Run the walk's three rows. today: {state, pool, schedule} paths of today's run. A walk that cannot be made says
    why and shows no step."""
    old = inputs_at(root, prev_date)
    if old is None:
        return dict(rows={}, steps=[], reproduced=None,
                    error=f"the {prev_date} run's inputs are not readable from git history (the commit that added its brief, "
                          f"with {', '.join(INPUT_PATHS.values())}): no walk is shown")
    sim = sim or SIM
    try:
        rows = dict(prev_inputs=sim(old["state"], old["pool"], old["schedule"], seasons),
                    rosters=sim(today["state"], old["pool"], today["schedule"], seasons),
                    today=sim(today["state"], today["pool"], today["schedule"], seasons))
    except (subprocess.CalledProcessError, OSError, ValueError, KeyError) as e:
        return dict(rows={}, steps=[], reproduced=None, error=f"the simulator did not run for the walk ({type(e).__name__}): no walk is shown")
    return walk(prev_title, title, rows)


def _walk_short(rec):
    w = rec.get("walk") or {}
    if not w.get("steps"):
        return ""
    return "; walk: " + ", ".join(f"{s['delta']:+.1f} {n}" for s, n in zip(w["steps"], ("engine", "rosters and results", "lines")))


def check(brief, prev, merges, owner_seat=OWNER_SEAT, method=None):
    """The record for one day. prev None: no comparison. merges None: git history was not readable. method: the
    method changes between the two runs (line_method_changes + registry_changes), named first among the causes."""
    title, n = _share(brief), int(brief.get("seasons") or 0)
    rec = dict(date=brief.get("date"), title=title, seasons=n, prev_date=None, prev_title=None, delta=None, band=None,
               moved=None, gap_days=None, merges=merges, method_changes=list(method or []),
               moves=[dict(m, owner=m.get("seat") == owner_seat) for m in brief.get("league_moves") or []
                      if any(m.get(k) for k in ("added", "dropped", "to_il", "from_il"))])
    if prev is None or title is None or _share(prev) is None or not n or not prev.get("seasons"):
        return rec
    pt = _share(prev)
    band = math.sqrt(_err(title, n) ** 2 + _err(pt, int(prev["seasons"])) ** 2)
    rec.update(prev_date=prev.get("date"), prev_title=pt, delta=title - pt, band=band, moved=abs(title - pt) > band,
               gap_days=(dt.date.fromisoformat(brief["date"]) - dt.date.fromisoformat(prev["date"])).days)
    return rec


def _move_text(m):
    parts = [("added " + ", ".join(m["added"])) if m.get("added") else "", ("dropped " + ", ".join(m["dropped"])) if m.get("dropped") else "",
             ("to IL " + ", ".join(m["to_il"])) if m.get("to_il") else "", ("off IL " + ", ".join(m["from_il"])) if m.get("from_il") else ""]
    return f"{'your team' if m.get('owner') else m.get('team')}: " + ", ".join(p for p in parts if p)


def _causes(rec):
    out = []
    if rec.get("method_changes"):
        out.append("METHOD CHANGE: " + "; ".join(rec["method_changes"]) + "; part or all of the move is the method, not the league")
    if rec["merges"] is None:
        out.append("kit merges not readable from git history")
    elif rec["merges"]:
        out.append(f"{len(rec['merges'])} kit merge(s): " + "; ".join(re.sub(r"^Merge pull request ", "", s) for s in rec["merges"]))
    if rec["moves"]:
        out.append(f"{len(rec['moves'])} team(s) changed rosters: " + "; ".join(_move_text(m) for m in rec["moves"]))
    if rec["merges"] == [] and not rec["moves"]:
        out.append("no kit merge and no roster move found between the two runs: unexplained, check the pool and the status feed")
    return out


def pass_line(rec, out):
    head = f"TITLE WATCH: PASS — {rec['date']}: "
    if rec["moved"] is None:
        return head + f"no earlier brief to compare with (title {rec['title']:.1f}%); wrote {out}" if rec["title"] is not None \
            else head + f"no title share on the brief; wrote {out}"
    gap = f", {rec['gap_days']} days earlier" if rec["gap_days"] != 1 else ""
    base = (f"title {rec['title']:.1f}% (was {rec['prev_title']:.1f}% on {rec['prev_date']}{gap}), "
            f"{rec['delta']:+.1f} against a band of ±{rec['band']:.1f}")
    if not rec["moved"]:
        meth = (" (METHOD CHANGE between the runs: " + "; ".join(rec["method_changes"]) + ")") if rec.get("method_changes") else ""
        return head + base + f": within the band{meth}{_walk_short(rec)}; wrote {out}"
    return head + base + ": MOVED. " + ". ".join(_causes(rec)) + f"{_walk_short(rec)}; wrote {out}"


def render(rec):
    L = [f"## Title watch — {rec['date']}", ""]
    if rec["moved"] is None:
        return L + ["No earlier brief to compare with."]
    L += ["| | title share |", "|---|---|", f"| {rec['prev_date']} | {rec['prev_title']:.1f}% |", f"| {rec['date']} | {rec['title']:.1f}% |",
          f"| change | {rec['delta']:+.1f} (band ±{rec['band']:.1f}) |", ""]
    if rec.get("method_changes"):
        L += ["**Method change between the two runs.** The two figures were not made the same way:", ""]
        L += [f"- {m}" for m in rec["method_changes"]] + [""]
    w = rec.get("walk") or {}
    if w.get("steps"):
        L += ["**Like for like.** The same change on today's engine, one input at a time (each row is a run of the "
              f"simulator; a step smaller than about ±{rec['band']:.1f} is noise):", "",
              "| step | change | title share after |", "|---|---|---|", f"| the {rec['prev_date']} brief | | {rec['prev_title']:.1f}% |"]
        L += [f"| {s['what']} | {s['delta']:+.1f} | {s['to']:.1f}% |" for s in w["steps"]] + [""]
    elif w.get("error"):
        L += [f"Like for like: {w['error']}.", ""]
    if not rec["moved"]:
        if w.get("steps"):
            return L + ["The net change is within the band; the steps above show what it is made of."]
        return L + ["Within the band: the change is no larger than two runs of the same simulator differ by."]
    L += ["**The title share moved by more than the band.** What changed between the two runs:", ""]
    L += [f"- {c[0].upper() + c[1:]}." for c in _causes(rec)]
    if w.get("steps"):
        return L + ["", "The walk above splits the move between the engine, the rosters and the lines; inside a step it does not split further."]
    return L + ["", "This names what changed; it does not split the move between the causes."]


def _load(path):
    if not path or not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    if argv[:1] == ["--sim"]:
        return _sim_main(argv[1:])
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", required=True)
    ap.add_argument("--briefs", default=BRIEFS)
    ap.add_argument("--root", default=KIT, help="the git checkout whose merges are read")
    ap.add_argument("--season", default=SEASON, help="the folder of season_lines_<date>.json records")
    for k, rel in INPUT_PATHS.items():
        ap.add_argument(f"--{k}", default=os.path.join(KIT, *rel.split("/")), help=f"today's {k} file, for the like-for-like walk")
    ap.add_argument("--no-walk", action="store_true", help="name a method change without the like-for-like walk (no simulator run)")
    a = ap.parse_args(argv)
    brief = _load(os.path.join(a.briefs, f"brief_{a.date}.json"))
    if brief is None:
        print(f"TITLE WATCH: HALT — no brief for {a.date}"); return 1
    pp = prev_brief(a.date, a.briefs)
    prev = _load(pp)
    ran = (_load(os.path.join(a.briefs, f"morning_{prev['date']}.json")) or {}).get("ran_at_utc") if prev else None
    method = None
    if prev:   # owner 2026-11-16 ("Mark method changes")
        method = line_method_changes(_load(os.path.join(a.season, f"season_lines_{prev['date']}.json")),
                                     _load(os.path.join(a.season, f"season_lines_{a.date}.json")))
        old_reg, new_reg = registry_at(a.root, ran), _load(os.path.join(a.root, REGISTRY))
        if old_reg is not None and new_reg is not None:
            method += registry_changes(old_reg, new_reg["constants"])
    rec = check(brief, prev, kit_merges(a.root, ran) if prev else None, method=method)
    # owner 2026-11-17 (F1): a real method change (not a missing record) gets the like-for-like walk
    rec["walk"] = None
    if not a.no_walk and rec["delta"] is not None and any("no season-lines record" not in m for m in method or []):
        rec["walk"] = like_for_like(a.root, prev["date"], rec["prev_title"], rec["title"],
                                    dict(state=a.state, pool=a.pool, schedule=a.schedule), int(brief.get("seasons") or 0))
    rec["inputs"] = dict(brief=f"brief_{a.date}.json", prev_brief=os.path.basename(pp) if pp else None, prev_ran_at_utc=ran)
    out = os.path.join(a.briefs, f"title_watch_{a.date}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False); f.write("\n")
    with open(os.path.join(a.briefs, f"title_watch_{a.date}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(render(rec)) + "\n")
    print(pass_line(rec, os.path.relpath(out, KIT) if out.startswith(KIT) else out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
