#!/usr/bin/env python3
"""Start/sit ledger (owner 2026-11-05: "when you suggest me to START a player instead of having him on my bench ...
track these on a ledger (system daily play suggested vs. actual played), and provide the hit/miss rate").
For one game day Y (the morning run grades yesterday) it reads three records and writes one row, never computing a
suggestion of its own:
  - the kit's suggestions for Y: report/briefs/week_matchup_Y.json → lineup_today.moves (week_matchup.lineup_moves:
    each {start, sit, kind, gap}; an empty list means the best daily fill was the lineup as it stood);
  - the owner's locked lineup for Y: the "daily" block of the pinned Flaim pulls (data/source/flaim/pull_*.json,
    get_roster as of Y; the latest pin holding the owner's team and Y wins — the morning pull of Y+1 normally holds it);
  - who did what on Y: data/actuals/Y.json (box_pull), scored with the engine's own zscores over that day's box lines
    (hoops.zscores: top-156 fixed point, the engine's rule, no constant of this script's).
Per pair it records whether the START was followed (the named bench player in an active slot at lock), whether the SIT
was followed (the named starter not in an active slot at lock), and how the night went: the start's box-line z minus
the sit's ("night": kit | against | no grade when either had no box line). The night is the outcome, not a verdict —
the red team measured per-game z noise at sd 3.65 against a 0.5 line (decision_grade.py), so one box score cannot
judge a pair; the rates that carry meaning are the followed rates and the season-z gap, tallied over weeks.
Ledger: data/decisions/lineup.jsonl, one row per day (id L-<Y>), append-only — a day already there is left as it is
and reported. Scorecard: report/decisions/lineup_scorecard.json and .md, regenerated from the ledger every run.
    python3 scripts/lineup_log.py --date 2026-11-05            # grades 2026-11-04
    python3 scripts/lineup_log.py --day 2026-11-04             # grades that day
    python3 scripts/lineup_log.py --backfill                   # every day with a week_matchup brief, oldest first
Prints 'LINEUP LOG: PASS — ...' (a missing brief, lineup or box record is named in the row, never guessed) or HALT.
"""
import argparse
import datetime as dt
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
DECK = os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball")
for _p in (os.path.join(DECK, "scripts"), HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import box_pull  # noqa: E402
import decision_log as DL  # noqa: E402

BRIEFS = os.path.join(KIT, "report", "briefs")
PIN_DIR = os.path.join(KIT, "data", "source", "flaim")
ACTUALS = os.path.join(KIT, "data", "actuals")
LEDGER = os.path.join(KIT, "data", "decisions", "lineup.jsonl")
SCORECARD = os.path.join(KIT, "report", "decisions", "lineup_scorecard.json")
OWNER_SEAT = DL.OWNER_SEAT
BENCH = {"BN", "IL", "IL+"}  # data/league_settings.json: every other roster slot is active


class LogError(Exception):
    pass


def fold(name, aliases=None):
    aliases = aliases or {}
    return box_pull.fold(aliases.get(name, name) or "")


def _alias_map():
    """variant → canonical, from the kit alias table (box_pull.load_aliases: canonical → variants)."""
    out = {}
    for canon, variants in (box_pull.load_aliases() or {}).items():
        for v in (variants if isinstance(variants, (list, tuple, set, frozenset)) else [variants]):
            out[v] = canon
    return out


def locked_lineup(day, team_name, pin_dir=PIN_DIR):
    """{player name: slot} the owner locked on `day`, from the pinned pulls' daily block; None when no pin holds it.
    Audit item F3 (owner 2026-11-10): the team is followed by its Yahoo team key, read from the newest pin that
    carries `team_name`, so a day pinned before a rename is still found; with no key, by name as before."""
    blocks = []
    for path in sorted(glob.glob(os.path.join(pin_dir, "pull_*.json"))):
        try:
            with open(path, encoding="utf-8") as f:
                daily = json.load(f).get("daily") or {}
        except (OSError, ValueError):
            continue
        blocks.append({k: v for k, v in daily.items() if isinstance(v, dict)})
    my_key = None
    for daily in blocks:
        for key, days in daily.items():
            if any(isinstance(r, dict) and r.get("teamName") == team_name for r in days.values()):
                my_key = key
    found = None
    for daily in blocks:
        for key, days in daily.items():
            rec = days.get(day)
            if rec and (key == my_key if my_key else rec.get("teamName") == team_name):
                found = rec
    if not found:
        return None
    return {p["name"]: (p.get("selectedPosition") or "BN") for p in found.get("players") or []}


def night_z(actuals_path):
    """{folded name: (box line, z)} for every player with minutes on the day, z by the engine's zscores over the day."""
    import hoops
    with open(actuals_path, encoding="utf-8") as f:
        act = json.load(f)
    rows = []
    for p in act.get("players") or []:
        if p.get("dnp") or not p.get("min"):
            continue
        r = dict(p, player=p["name"], availability=1.0,
                 fg_pct=(p["fgm"] / p["fga"]) if p.get("fga") else 0.0,
                 ft_pct=(p["ftm"] / p["fta"]) if p.get("fta") else 0.0)
        rows.append(r)
    if not rows:
        return {}
    keep = hoops.availability
    hoops.availability = lambda p: 1.0  # a box line has no note column; every line is in the day's pool
    try:
        hoops.zscores(rows)
    finally:
        hoops.availability = keep
    out = {}
    for r in rows:
        line = dict(min=r["min"], pts=r["pts"], reb=r["reb"], ast=r["ast"], tpm=r["tpm"], stl=r["stl"], blk=r["blk"],
                    tov=r["tov"], fg=f"{r['fgm']}/{r['fga']}", ft=f"{r['ftm']}/{r['fta']}", z=round(hoops.total_value(r), 2))
        for name in {r.get("pool_name") or r["name"], r["name"]}:
            out[fold(name)] = line
    return out


def grade_day(day, briefs=BRIEFS, pin_dir=PIN_DIR, actuals=ACTUALS, aliases=None):
    """One ledger row for `day`; the inputs it lacked are named in the row."""
    aliases = _alias_map() if aliases is None else aliases
    bp = os.path.join(briefs, f"week_matchup_{day}.json")
    row = dict(id=f"L-{day}", date=day, made_at=DL.now(), brief=os.path.relpath(bp, KIT), pairs=[])
    if not os.path.exists(bp):
        row.update(status="no brief", team=None)
        return row
    with open(bp, encoding="utf-8") as f:
        wm = json.load(f)
    me = wm.get("me") or {}
    row["team"] = me.get("name")
    row["games"] = (wm.get("lineup_today") or {}).get("games_today")
    moves = ((wm.get("lineup_today") or {}).get("moves")) or []
    locked = locked_lineup(day, me.get("name"), pin_dir) if me.get("name") else None
    row["lineup_record"] = locked is not None
    ap = os.path.join(actuals, f"{day}.json")
    nz = night_z(ap) if os.path.exists(ap) else None
    row["box_record"] = nz is not None
    if not moves:
        row["status"] = "agreed"  # the best fill was the lineup as it stood: nothing to follow
        return row
    row["status"] = "graded"
    lf = {fold(n, aliases): s for n, s in (locked or {}).items()}
    for m in moves:
        s, t = m.get("start"), m.get("sit")
        pr = dict(start=s, sit=t, kind=m.get("kind"), gap=m.get("gap"), d_exp=m.get("d_exp"))
        fs, ft = fold(s, aliases), fold(t, aliases) if t else None
        if locked is None:
            pr.update(locked=None, start_followed=None, sit_followed=None)
        else:
            pr["locked"] = {s: lf.get(fs, "not on roster"), **({t: lf.get(ft, "not on roster")} if t else {})}
            pr["start_followed"] = (fs in lf) and lf[fs] not in BENCH
            pr["sit_followed"] = None if not t else ((ft in lf) and lf[ft] in BENCH)
        if nz is None:
            pr.update(night=None, box=None)
        else:
            bs, bt = nz.get(fs), (nz.get(ft) if ft else None)
            pr["box"] = {s: bs, **({t: bt} if t else {})}
            if bs and bt:
                pr["z_gap"] = round(bs["z"] - bt["z"], 2)
                pr["night"] = "kit" if pr["z_gap"] > 0 else "against"
            else:
                pr["night"] = "no grade"
        row["pairs"].append(pr)
    return row


def scorecard(rows):
    days = sorted(rows, key=lambda r: r["date"])
    pairs = [p for r in days for p in r.get("pairs") or []]
    n = lambda key, val=True: sum(1 for p in pairs if p.get(key) == val)
    graded = [p for p in pairs if p.get("start_followed") is not None]
    both = sum(1 for p in graded if p["start_followed"] and (p["sit_followed"] in (True, None)))
    out = dict(as_of=days[-1]["date"] if days else None, days=len(days),
               days_agreed=sum(1 for r in days if r.get("status") == "agreed"),
               days_graded=sum(1 for r in days if r.get("status") == "graded"),
               days_no_brief=sum(1 for r in days if r.get("status") == "no brief"),
               pairs=len(pairs), pairs_with_lineup=len(graded),
               start_followed=n("start_followed"), sit_followed=n("sit_followed"), both_followed=both,
               night_kit=n("night", "kit"), night_against=n("night", "against"), night_no_grade=n("night", "no grade"),
               night_no_box=sum(1 for p in pairs if p.get("night") is None),
               gap_sum_followed=round(sum(p.get("gap") or 0 for p in graded if p["start_followed"]), 2),
               gap_sum_ignored=round(sum(p.get("gap") or 0 for p in graded if not p["start_followed"]), 2),
               rows=[dict(date=r["date"], status=r.get("status"), lineup_record=r.get("lineup_record"),
                          pairs=[{k: p.get(k) for k in ("start", "sit", "kind", "gap", "start_followed", "sit_followed",
                                                        "night", "z_gap")} for p in r.get("pairs") or []]) for r in days],
               method=dict(suggested="week_matchup_<day>.json lineup_today.moves", locked="pinned Flaim daily block (get_roster as of the day)",
                           night="start's box-line z minus the sit's, hoops.zscores over the day's box lines (engine rule)",
                           caveat="the night is the outcome, not a verdict: per-game z noise sd 3.65 vs a 0.5 line (red team, decision_grade.py)"))
    out["start_followed_rate"] = round(out["start_followed"] / len(graded), 3) if graded else None
    out["sit_followed_rate"] = round(out["sit_followed"] / len(graded), 3) if graded else None
    return out


def render_md(sc):
    L = ["# Start/sit calls — followed, and how the night went", "",
         f"As of {sc['as_of']}: {sc['days']} days on the ledger — {sc['days_agreed']} agreed (no move suggested), "
         f"{sc['days_graded']} with a suggestion, {sc['days_no_brief']} without a brief.", "",
         f"Pairs {sc['pairs']} (lineup on record for {sc['pairs_with_lineup']}): start followed {sc['start_followed']}, "
         f"sit followed {sc['sit_followed']}, both {sc['both_followed']}; night went the kit's way {sc['night_kit']}, "
         f"against {sc['night_against']}, no grade {sc['night_no_grade']}.", "",
         "| day | start | sit | gap | start followed | sit followed | night | z gap |", "|---|---|---|---|---|---|---|---|"]
    y = lambda v: "–" if v is None else ("yes" if v else "no")
    for r in sc["rows"]:
        if not r["pairs"]:
            L.append(f"| {r['date']} | — | — | — | {r['status']} | | | |")
        for p in r["pairs"]:
            L.append(f"| {r['date']} | {p['start']} | {p['sit'] or '—'} | {p['gap'] if p['gap'] is not None else '–'} | "
                     f"{y(p['start_followed'])} | {y(p['sit_followed'])} | {p['night'] or 'no box'} | "
                     f"{p['z_gap'] if p.get('z_gap') is not None else '–'} |")
    L += ["", f"Method: {sc['method']['suggested']}; locked = {sc['method']['locked']}; night = {sc['method']['night']}.",
          f"Caveat: {sc['method']['caveat']}.", ""]
    return "\n".join(L)


def write_scorecard(rows, path=SCORECARD):
    sc = scorecard(rows)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sc, f, indent=1, ensure_ascii=False)
    with open(path[:-5] + ".md", "w", encoding="utf-8") as f:
        f.write(render_md(sc))
    return sc


def run(days, ledger=LEDGER, briefs=BRIEFS, pin_dir=PIN_DIR, actuals=ACTUALS, scorecard_path=SCORECARD, dry_run=False):
    have = DL.read(ledger)
    ids = {r["id"] for r in have}
    new, skipped = [], []
    pending, missing = [], []
    for d in days:
        if f"L-{d}" in ids:
            skipped.append(d)
            continue
        row = grade_day(d, briefs, pin_dir, actuals)
        if row["status"] == "no brief":
            missing.append(d)  # no morning brief for the day: nothing was suggested or declined; reported, never a row
            continue
        if not row["box_record"] and row.get("games") is not False:
            pending.append(d)  # the night is not in yet; the row waits (append-only: a row written now would never be graded)
            continue
        new.append(row)
    if not dry_run and new:
        DL.append(ledger, new)
    sc = scorecard(have + new) if dry_run else write_scorecard(DL.read(ledger), scorecard_path)
    return new, skipped, sc, pending, missing


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="the morning run's date; grades the day before")
    ap.add_argument("--day", help="the game day to grade")
    ap.add_argument("--backfill", action="store_true", help="every day with a week_matchup brief, oldest first")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    if a.backfill:
        days = sorted(os.path.basename(p)[len("week_matchup_"):-5] for p in glob.glob(os.path.join(BRIEFS, "week_matchup_*.json")))
    elif a.day:
        days = [a.day]
    elif a.date:
        days = [(dt.date.fromisoformat(a.date) - dt.timedelta(days=1)).isoformat()]
    else:
        print("LINEUP LOG: HALT — give --date, --day or --backfill")
        return 2
    try:
        new, skipped, sc, pending, missing = run(days, ledger=LEDGER, briefs=BRIEFS, pin_dir=PIN_DIR, actuals=ACTUALS,
                                                 scorecard_path=SCORECARD, dry_run=a.dry_run)
    except (LogError, DL.LogError, OSError, ValueError) as e:
        print(f"LINEUP LOG: HALT — {e}")
        return 1
    parts = []
    for r in new:
        if r["status"] == "graded":
            f = [p for p in r["pairs"] if p.get("start_followed")]
            parts.append(f"{r['date']}: {len(r['pairs'])} pair(s), start followed {len(f)}"
                         + ("" if r["lineup_record"] else " (no lineup record)") + ("" if r["box_record"] else " (no box record)"))
        else:
            parts.append(f"{r['date']}: {r['status']}")
    if pending:
        parts.append(f"waiting for box scores: {', '.join(pending)}")
    if missing:
        parts.append(f"no brief: {', '.join(missing)}")
    if skipped:
        parts.append(f"already logged: {', '.join(skipped)}")
    print(f"LINEUP LOG: PASS — {'; '.join(parts) or 'nothing to grade'}; ledger {sc['days']} days, {sc['pairs']} pairs, "
          f"start followed {sc['start_followed']}/{sc['pairs_with_lineup']}, night kit {sc['night_kit']} / against {sc['night_against']}"
          + (" (dry run)" if a.dry_run else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
