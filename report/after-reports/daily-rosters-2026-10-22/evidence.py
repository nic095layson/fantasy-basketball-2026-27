#!/usr/bin/env python3
"""Evidence for the daily-roster rebuild (owner 2026-10-22, "Read daily rosters"): the 10/22 week card rebuilt on the
season/daily e7b69bb records, once as that run's pull has it (no lineups) and once with Yahoo's 10/20 and 10/21 lineups
for both teams added — the dated get_roster responses this session made through Flaim (as_of_date), extracted from
the session transcript by flaim_live.extract_pull and pinned beside this file (lineups_2026-10-20_21.json).

    python3 report/after-reports/daily-rosters-2026-10-22/evidence.py --records <kit worktree at e7b69bb> \
        [--transcript <session transcript>]   # without --transcript, the pinned lineups are read

Writes evidence.json beside itself.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(KIT, "scripts"))
import flaim_live as FL  # noqa: E402
import week_matchup as WM  # noqa: E402

RECORDS_COMMIT = "e7b69bb"
DATE = "2026-10-22"
PINNED = os.path.join(HERE, "lineups_2026-10-20_21.json")


def card(records, pull_path):
    paths = dict(state=os.path.join(records, "data", "league_state.json"),
                 schedule=os.path.join(records, "data", "league_schedule.json"),
                 games=os.path.join(records, "report", "schedule", "games-2026-27.csv"),
                 actuals=os.path.join(records, "data", "actuals"), status=os.path.join(records, "data", "status"),
                 yahoo_pull=pull_path)
    rec = WM.build(DATE, paths)
    return dict(to_date_source=rec["to_date_source"], rebuild_rosters=rec["rebuild_rosters"],
                rebuild=dict(me=rec["totals"]["me"]["rebuild_to_date"], opp=rec["totals"]["opp"]["rebuild_to_date"]),
                yahoo=dict(me=rec["totals"]["me"]["to_date"], opp=rec["totals"]["opp"]["to_date"]),
                benched={s: rec["games"][s]["to_date_benched"] for s in ("me", "opp")})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", required=True)
    ap.add_argument("--transcript")
    a = ap.parse_args()
    head = subprocess.run(["git", "-C", a.records, "rev-parse", "--short=7", "HEAD"], capture_output=True, text=True,
                          check=True).stdout.strip()
    assert head == RECORDS_COMMIT, f"records worktree is at {head}, not {RECORDS_COMMIT}"
    os.environ["SEASON_POOL"] = os.path.join(a.records, "data", "season", "pool_season.csv")
    if a.transcript:
        daily = FL.extract_pull(a.transcript)["daily"]
        json.dump(daily, open(PINNED, "w", encoding="utf-8"), indent=1, ensure_ascii=False, sort_keys=True)
    daily = json.load(open(PINNED, encoding="utf-8"))
    run_pull = os.path.join(a.records, "data", "source", "flaim", f"pull_{DATE}.json")
    with tempfile.TemporaryDirectory() as d:
        p = json.load(open(run_pull, encoding="utf-8"))
        p["daily"] = daily
        with_lineups = os.path.join(d, f"pull_{DATE}.json")
        json.dump(p, open(with_lineups, "w", encoding="utf-8"))
        out = dict(records_commit=head, date=DATE, run_pull=os.path.relpath(run_pull, a.records),
                   lineups={k: sorted(v) for k, v in daily.items()},
                   without_lineups=card(a.records, run_pull), with_lineups=card(a.records, with_lineups))
    json.dump(out, open(os.path.join(HERE, "evidence.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    w = out["with_lineups"]["to_date_source"]
    print(f"EVIDENCE: with lineups, rebuild agrees with Yahoo: {w['rebuild_agrees']} ({len(w['differences'])} differences); "
          f"without: {len(out['without_lineups']['to_date_source']['differences'])} differences")


if __name__ == "__main__":
    main()
