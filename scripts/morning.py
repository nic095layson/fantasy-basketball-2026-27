#!/usr/bin/env python3
"""The morning run (in-season tool; Council 2026-10-19 decisions 6 and 7: a fresh session each morning, record and
propose only). The steps, each a gate in the sense of scripts/gates.py (exit 0 AND its PASS line, or FAIL; a
failed step stops the run and later steps are SKIPPED):

  - preflight (fatal)            scripts/independent_audit/preflight.py --spec scripts/independent_audit/morning_preflight.json
                                   (owner 2026-10-21: the run's preconditions — checkout, deck repo, briefs, remote; not playwright,
                                   which only the deck step needs and which fails that step closed)
  0 league live (non-fatal)      scripts/league_live.py --as-of <today>        (FantasyBot rosters from the session transcript;
                                   a failed pull keeps the last league_state.json and the brief says so — owner 2026-10-20)
  1 box scores for yesterday      scripts/box_pull.py --date <yesterday>        (ESPN + Basketball-Reference)
  2 season lines                  scripts/season_lines.py --date <today>        (preseason line + actuals, priors registered)
  3 season board                  scripts/season_board.py --date <today>
  4 status feed                   scripts/status_feed.py --date <today> then --check on that day's file (Yahoo letters + ESPN feed, receipts)
  4b transactions (fetch only)    scripts/transactions.py --date <today>        (ESPN transactions feed, last 3 days; owner 2026-10-20)
  4c matchup live (non-fatal)     scripts/matchup_live.py --date <today>       (FantasyBot matchup pin; owner 2026-10-20 item 2)
  5 daily brief on the season pool  SEASON_POOL=data/season/pool_season.csv scripts/daily_brief.py --date <today>

Writes report/briefs/morning_<date>.json (every step's command, exit, PASS line, tail), appends each step's verdict to
the run-ledger report/run-ledger.jsonl as 'morning: <step>' (scripts/run_ledger.py, 2026-10-21), and prints
'MORNING: PASS — ...' / 'MORNING: FAIL' with the first failing step. Nothing here changes a projection line, a
tag or a roster: the season files are derived, the brief proposes.

    python3 scripts/morning.py [--date YYYY-MM-DD] [--no-fetch] [--seasons 10000] [--since ISO-TIME]
--since (GAUNTLET 2026-10-21 item 7) goes to the two transcript readers, league live and matchup live: the persistent
runner passes its start time so an earlier day's FantasyBot pull in the same transcript never counts as today's.
"""
import argparse
import datetime
import json
import os
import re
import shlex
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run_ledger  # noqa: E402

KIT = os.path.dirname(HERE)
PY = sys.executable
BRIEFS = os.path.join(KIT, "report", "briefs")


PREFLIGHT_SPEC = os.path.join(HERE, "independent_audit", "morning_preflight.json")


def steps(date, fetch=True, seasons=10000, since=None):
    y = (datetime.date.fromisoformat(date) - datetime.timedelta(days=1)).isoformat()
    season_pool = os.path.join(KIT, "data", "season", "pool_season.csv")
    # step 0, fatal (owner 2026-10-21, independent-audit adoption): the run's preconditions first, so a missing deck repo,
    # browser or remote prints one FAIL line instead of a silent half-run (10/21 runner: "deck still missing").
    st = [dict(name="preflight", cmd=[PY, os.path.join(HERE, "independent_audit", "preflight.py"), "--spec", PREFLIGHT_SPEC],
               cwd=KIT, pass_re=r"^PREFLIGHT: PASS", env={})]
    tail = ["--since", since] if since else []
    if fetch:  # owner 2026-10-20: live rosters from FantasyBot; non-fatal, the last paste stands on a failed pull
        st.append(dict(name="league live", cmd=[PY, os.path.join(HERE, "league_live.py"), "--as-of", date] + tail, cwd=KIT,
                       pass_re=r"^LEAGUE LIVE: PASS", env={}, fatal=False))
        st.append(dict(name="matchup live", cmd=[PY, os.path.join(HERE, "matchup_live.py"), "--date", date] + tail, cwd=KIT,
                       pass_re=r"^MATCHUP LIVE: PASS", env={}, fatal=False))
        st.append(dict(name=f"box scores {y}", cmd=[PY, os.path.join(HERE, "box_pull.py"), "--date", y], cwd=KIT, pass_re=r"^BOX PULL: PASS", env={}))
    st += [dict(name="season lines", cmd=[PY, os.path.join(HERE, "season_lines.py"), "--date", date], cwd=KIT, pass_re=r"^SEASON LINES: PASS", env={}),
           dict(name="season board", cmd=[PY, os.path.join(HERE, "season_board.py"), "--date", date], cwd=KIT, pass_re=r"^SEASON BOARD: PASS", env={}),
           dict(name="status feed", cmd=["bash", "-c", f"{shlex.quote(PY)} {shlex.quote(os.path.join(HERE, 'status_feed.py'))} --date {date} && "
                                                  f"{shlex.quote(PY)} {shlex.quote(os.path.join(HERE, 'status_feed.py'))} --check "
                                                  f"{shlex.quote(os.path.join(KIT, 'data', 'status', f'status_{date}.json'))}"],
                cwd=KIT, pass_re=r"^STATUS GATE: PASS", env={})]
    if fetch:  # owner 2026-10-20: waivers and signings (Kevin Porter Jr.) reach the brief; an unreachable feed is recorded, not fatal
        st.append(dict(name="transactions", cmd=[PY, os.path.join(HERE, "transactions.py"), "--date", date], cwd=KIT,
                       pass_re=r"^TRANSACTIONS: PASS", env={}))
    st += [
           dict(name="daily brief", cmd=[PY, os.path.join(HERE, "daily_brief.py"), "--date", date, "--seasons", str(seasons)], cwd=KIT,
                pass_re=r"^wrote report/briefs/brief_", env={"SEASON_POOL": season_pool}),
           dict(name="season deck", cmd=[PY, os.path.join(HERE, "season_deck.py"), "--date", date], cwd=KIT,
                pass_re=r"^SEASON DECK: PASS", env={})]
    return st


def run_steps(st, out, ledger=None):
    """Run the steps in order; with `ledger` (main passes run_ledger.LEDGER) each step's verdict is appended to the
    run-ledger as 'morning: <step>' — non-fatally: a ledger that cannot be written never fails the morning run."""
    rec = dict(ran_at_utc=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), steps=[], verdict="PASS")
    failed = False
    for s in st:
        if failed:
            rec["steps"].append(dict(name=s["name"], verdict="SKIPPED", cmd=" ".join(shlex.quote(c) for c in s["cmd"]))); continue
        env = dict(os.environ); env.update(s.get("env") or {})
        p = subprocess.run(s["cmd"], cwd=s["cwd"], capture_output=True, text=True, env=env)
        lines = (p.stdout + "\n" + p.stderr).splitlines()
        hits = [ln.strip() for ln in lines if re.search(s["pass_re"], ln)]
        verdict = "PASS" if p.returncode == 0 and hits else "FAIL"
        rec["steps"].append(dict(name=s["name"], cmd=" ".join(shlex.quote(c) for c in s["cmd"]), exit=p.returncode,
                                 pass_line=hits[-1] if hits else "", verdict=verdict, tail=[ln for ln in lines if ln.strip()][-6:]))
        if verdict == "FAIL":
            if s.get("fatal", True):
                failed = True; rec["verdict"] = "FAIL"
            else:
                rec["steps"][-1]["verdict"] = "FAIL (non-fatal)"
        if ledger:
            run_ledger.safe_record("morning: " + s["name"], verdict, rec["steps"][-1]["pass_line"], ledger=ledger)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False); f.write("\n")
    return rec


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--no-fetch", action="store_true"); ap.add_argument("--seasons", type=int, default=10000)
    ap.add_argument("--since", help="the run's start (ISO time): league live and matchup live read only later transcript entries")
    a = ap.parse_args()
    rec = run_steps(steps(a.date, not a.no_fetch, a.seasons, a.since), os.path.join(BRIEFS, f"morning_{a.date}.json"),
                    ledger=run_ledger.LEDGER)
    for s in rec["steps"]:
        print(f"- {s['verdict']} · {s['name']}" + (f" · {s['pass_line']}" if s.get("pass_line") else "") +
              ("" if s["verdict"] != "FAIL" else " · " + " | ".join(s["tail"][-2:])))
    if rec["verdict"] == "PASS":
        print(f"MORNING: PASS — {a.date}: {len(rec['steps'])} steps; brief report/briefs/brief_{a.date}.md; record report/briefs/morning_{a.date}.json")
    else:
        first = next(s for s in rec["steps"] if s["verdict"] == "FAIL")
        print(f"MORNING: FAIL — {a.date}: step '{first['name']}' failed (exit {first['exit']}); later steps skipped; record report/briefs/morning_{a.date}.json")
    return 0 if rec["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
