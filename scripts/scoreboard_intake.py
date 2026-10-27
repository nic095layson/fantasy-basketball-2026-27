#!/usr/bin/env python3
"""Weekly scoreboard intake (in-season tool; Council 2026-10-19 decision 3, 5-0).

Input: one CSV per week, data/weeks/week_<N>.csv, one row per fantasy team with its opponent and nine category
totals (the template: week,team,opponent,FG%,FT%,3PTM,PTS,REB,AST,ST,BLK,TO). The owner fills it from Yahoo's
scoreboard (a paste parser is added when the first paste sample arrives). Every team name must resolve to
data/league_state.json; a miss, a missing team, or a non-numeric cell HALTS the intake (RULES.md rule 4).

Outputs: data/weeks/week_<N>.json (the matchups, every team's line, the owner's categories won / lost / tied),
data/weeks/team_weeks.csv (every team-week's nine totals, append-only and idempotent per week: the dataset the
games shock and the variance scales are calibrated on, D-PM-1), and the calibration ledger scored through
scripts/weekly_preview.py --score (skipped with --no-ledger).

    python3 scripts/scoreboard_intake.py --week 1 [--csv data/weeks/week_1.csv] [--no-ledger]
    python3 scripts/scoreboard_intake.py --week 1 --from-pull data/source/flaim/pull_2026-10-26.json   (Build 1: Yahoo's finals)
"""
import argparse
import csv
import json
import os
import subprocess
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
STATE = os.path.join(KIT, "data", "league_state.json")
WEEKS = os.path.join(KIT, "data", "weeks")
CATS = ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]
OWNER_SEAT = 10


class IntakeError(Exception):
    pass


def fold(s):
    return "".join(c for c in unicodedata.normalize("NFKD", str(s).lower()) if not unicodedata.combining(c) and c not in "'’`.").strip()


def parse(path, state):
    seats = {fold(t["name"]): (t["name"], t["seat"]) for t in state["teams"]}
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    missing_cols = [c for c in ["week", "team", "opponent"] + CATS if rows and c not in rows[0]]
    if missing_cols:
        raise IntakeError(f"missing columns: {missing_cols}")
    teams, problems = {}, []
    for i, r in enumerate(rows, 2):
        nm, op = seats.get(fold(r["team"])), seats.get(fold(r["opponent"]))
        if not nm:
            problems.append(f"row {i}: team {r['team']!r} is not in the league state"); continue
        if not op:
            problems.append(f"row {i}: opponent {r['opponent']!r} is not in the league state"); continue
        line = {}
        for c in CATS:
            try:
                line[c] = float(r[c])
            except (TypeError, ValueError):
                problems.append(f"row {i}: {nm[0]} {c} is {r[c]!r}, not a number")
        teams[nm[0]] = dict(seat=nm[1], opponent=op[0], line=line)
    if problems:
        raise IntakeError("; ".join(problems))
    if len(teams) != 12:
        raise IntakeError(f"{len(teams)} teams, not 12")
    weeks = {int(r["week"]) for r in rows}
    if len(weeks) != 1:
        raise IntakeError(f"rows span weeks {sorted(weeks)}")
    matchups, seen = [], set()
    for t, v in teams.items():
        if t in seen:
            continue
        o = v["opponent"]
        if teams.get(o, {}).get("opponent") != t:
            raise IntakeError(f"{t} lists {o} but {o} lists {teams.get(o, {}).get('opponent')}")
        matchups.append([t, o]); seen |= {t, o}
    return dict(week=weeks.pop(), teams=teams, matchups=matchups, source=os.path.relpath(path, KIT))


def from_pull(path, week, state):
    """A finished week's six matchups from a Flaim pull's Yahoo matchup block (owner 2026-10-23, Build 1): the same
    shape parse() returns. Halts when the pull lacks the week, or the week is not final (every matchup's status must
    read "final" — Flaim's get_matchups contract, read 2026-10-23: upcoming, in_progress or final; the Runner session
    flagged the earlier "finished" check the same day), or a team is not in the league state."""
    sys.path.insert(0, HERE)
    import league_table as LT
    pull = json.load(open(path, encoding="utf-8"))
    block = ((pull.get("matchups") or {}).get(str(week)))
    if not block:
        raise IntakeError(f"{os.path.basename(path)} carries no week {week} matchups")
    unfinished = [m.get("matchupId") for m in block.get("matchups") or [] if (m.get("status") or "") != "final"]
    if unfinished:
        raise IntakeError(f"week {week} is not final in {os.path.basename(path)} (matchups {unfinished} are {block['matchups'][0].get('status')!r})")
    try:
        yw = LT.week_from_yahoo(block, state)
    except LT.TableError as e:
        raise IntakeError(str(e))
    teams = {}
    for n, x in yw.items():
        v = LT.cat_values(x["totals"])
        teams[n] = dict(seat=x["seat"], opponent=x["opponent"], line={c: (round(v[c], 4) if c in ("FG%", "FT%") and v[c] is not None else v[c]) for c in CATS},
                        yahoo_score=x["score"])
    matchups, seen = [], set()
    for t, v in teams.items():
        if t not in seen:
            matchups.append([t, v["opponent"]]); seen |= {t, v["opponent"]}
    rel = os.path.relpath(path, KIT) if os.path.abspath(path).startswith(KIT) else path
    return dict(week=week, teams=teams, matchups=matchups, source=rel)


def owner_result(week, owner_seat=OWNER_SEAT):
    me = next(t for t, v in week["teams"].items() if v["seat"] == owner_seat)
    opp = week["teams"][me]["opponent"]
    a, b = week["teams"][me]["line"], week["teams"][opp]["line"]
    won, lost, tied = [], [], []
    for c in CATS:
        x, y = a[c], b[c]
        better = x < y if c == "TO" else x > y
        (tied if x == y else won if better else lost).append(c)
    return dict(team=me, opponent=opp, won=won, lost=lost, tied=tied, cats_won=len(won), cats_tied=len(tied))


def append_team_weeks(week, path):
    fields = ["week", "team", "seat", "opponent"] + CATS
    existing = []
    if os.path.exists(path):
        with open(path, encoding="utf-8", newline="") as f:
            existing = [r for r in csv.DictReader(f) if int(r["week"]) != week["week"]]
    new = [dict(week=week["week"], team=t, seat=v["seat"], opponent=v["opponent"], **{c: v["line"][c] for c in CATS})
           for t, v in sorted(week["teams"].items(), key=lambda kv: kv[1]["seat"])]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); w.writeheader()
        w.writerows(sorted(existing + new, key=lambda r: (int(r["week"]), int(r["seat"]))))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--week", type=int, required=True); ap.add_argument("--csv"); ap.add_argument("--no-ledger", action="store_true")
    ap.add_argument("--from-pull", help="a Flaim pull carrying the final week's matchups (owner 2026-10-23, Build 1)")
    ap.add_argument("--state", default=STATE); ap.add_argument("--weeks-dir", default=WEEKS)
    # owner 2026-10-24 (the scoring loop): after the weekly ledger, every morning card's P(win) is graded (score_week.py)
    ap.add_argument("--calibration", default=None, help="weekly calibration ledger (default: weekly_preview's)")
    ap.add_argument("--briefs-dir", default=None, help="where the morning week_matchup_<date>.json cards are")
    ap.add_argument("--daily-out", default=None, help="the daily calibration record (default: report/calibration_daily.json)")
    # owner 2026-10-27 (the weekly accuracy card): the week graded into report/accuracy.json after the scorers
    ap.add_argument("--accuracy-out", default=None, help="the accuracy record (default: report/accuracy.json)")
    ap.add_argument("--actuals-dir", default=None, help="box-score days (default: data/actuals)")
    ap.add_argument("--league-calibration", default=None, help="every matchup's pre-week forecast (default: report/calibration_league.json)")
    a = ap.parse_args()
    WEEKS_DIR = a.weeks_dir
    path = a.from_pull or a.csv or os.path.join(WEEKS_DIR, f"week_{a.week}.csv")
    with open(a.state, encoding="utf-8") as f:
        state = json.load(f)
    try:
        wk = from_pull(path, a.week, state) if a.from_pull else parse(path, state)
    except (IntakeError, OSError, ValueError) as e:
        print(f"SCOREBOARD INTAKE: FAIL — {e}"); return 1
    if wk["week"] != a.week:
        print(f"SCOREBOARD INTAKE: FAIL — the file says week {wk['week']}, --week {a.week}"); return 1
    res = owner_result(wk); wk["owner"] = res
    os.makedirs(WEEKS_DIR, exist_ok=True)
    with open(os.path.join(WEEKS_DIR, f"week_{a.week}.json"), "w", encoding="utf-8") as f:
        json.dump(wk, f, indent=1, ensure_ascii=False); f.write("\n")
    append_team_weeks(wk, os.path.join(WEEKS_DIR, "team_weeks.csv"))
    ledger = daily = "skipped"
    if not a.no_ledger:
        cmd = [sys.executable, os.path.join(HERE, "weekly_preview.py"), "--score", str(a.week), "--won", ",".join(res["won"])]
        if a.calibration:
            cmd += ["--ledger", a.calibration]
        p = subprocess.run(cmd, capture_output=True, text=True)
        ledger = f"exit {p.returncode}: " + (p.stdout.strip().splitlines() or [p.stderr.strip()[-200:]])[-1]
        # the daily scorer is non-fatal: the intake stands, and a scoring failure is named on this line
        import score_week as SW
        try:
            r = SW.run(a.week, WEEKS_DIR, a.briefs_dir or SW.BRIEFS, a.daily_out or SW.OUT)
            w = r["week"]
            daily = (f"{r['status']}, {len(w['days_scored'])} mornings / {w['n_forecasts']} forecasts, Brier {w['brier']:.3f} "
                     f"vs lead-to-date {w['baseline_brier']:.3f}")
        except (SW.ScoreError, OSError, ValueError, KeyError) as e:
            daily = f"FAIL — {str(e)[:160]}"
    accuracy = "skipped"
    if not a.no_ledger:
        # non-fatal like the daily scorer: the intake stands, and a grading failure is named on the PASS line
        import accuracy_week as AW
        try:
            r = AW.run(a.week, a.actuals_dir or AW.ACTUALS, a.accuracy_out or AW.OUT, weeks_dir=WEEKS_DIR,
                       ledger=a.calibration or AW.LEDGER, daily=a.daily_out or AW.DAILY, league=a.league_calibration or AW.LEAGUE)
            accuracy = AW.summary(r)
        except (AW.AccuracyError, OSError, ValueError, KeyError, StopIteration) as e:
            accuracy = f"FAIL — {str(e)[:160]}"
    print(f"SCOREBOARD INTAKE: PASS — week {a.week}: 6 matchups, 12 team lines; you {res['cats_won']}-{len(res['lost'])}-{res['cats_tied']} "
          f"vs {res['opponent']} (won {', '.join(res['won']) or 'none'}); team_weeks.csv updated; ledger {ledger}; week score {daily}; accuracy {accuracy}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
