#!/usr/bin/env python3
"""GP reconstruction test, the FAIL branch stated before the run: daily rosters for the worst 7-day team-weeks (the
plan capped the calls at 21, so week 17's 14 days were out): the owner's week 13 (-11), Robert's week 8 (-8, the
worst opponent row) and the owner's week 5 (-8, the earliest of the tied rows). Each day's Flaim get_roster snapshot
(the first day is the pinned week-start roster) is pinned to daily/, and each team-week's gap is split:

  weekly    reconstruct.py's figure: the week-start roster, a perfect daily manager
  daily     the same perfect manager on each day's actual roster        -> daily - weekly  = roster change in the week
  lineup    the players actually in an active slot (not BN, IL, IL+) who played that day -> lineup - daily = lineup choice
  known     Yahoo's figure in the truth file                            -> known - lineup  = what neither explains
  starts    players in an active slot whose NBA team played that day, whether or not they played (a team's game days
            are the union of every pinned log row under that team; a player's team on a day is the team of his nearest
            log row, or the 2025-26 per-game file's team when he has none). Added AFTER the first run showed a residual
            the other figures could not explain: a hypothesis formed on the output, so a bracket, not a test
  totals    the lineup's game-log stat totals (makes, attempts, threes, points, rebounds, assists, steals, blocks,
            turnovers) against the truth row's eleven totals: equal means the snapshots and logs reproduce exactly what
            Yahoo scored, whatever its games counter counts. Added after the first run, with "starts"
  week 1    both teams of week 1 were added after the first run as the settling case: the one row pair checked against
            a screenshot (README correction of 2026-10-21, "Games Played 32/32" and "28/28"); 6 days, 10 more calls

    python3 diagnose_daily.py TRANSCRIPT.jsonl --since 2026-10-22T00:51:56Z"""
import argparse, collections, csv, datetime as dt, hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import reconstruct as R  # noqa: E402
from extract_rosters import extract  # noqa: E402

CASES = [(13, "David", 11, "2026-01-12"), (8, "Robert", 2, "2025-12-08"), (5, "David", 11, "2025-11-17"),
         (1, "David", 11, "2025-10-21"), (1, "Kyle", 5, "2025-10-21")]
TOTALS = [("fg", "fgm"), ("fga", "fga"), ("ft", "ftm"), ("fta", "fta"), ("fg3", "tpm"), ("pts", "pts"), ("trb", "reb"),
          ("ast", "ast"), ("stl", "stl"), ("blk", "blk"), ("tov", "tov")]


def schedules(ids):
    sys.path.insert(0, os.path.join(R.KIT, "..", "yahoo-fantasy-basketball", "scripts"))
    from verify_rosters import norm
    team_days, rows = collections.defaultdict(set), collections.defaultdict(list)
    for path in (R.PRIOR, R.EXTRA):
        for r in csv.DictReader(open(path, encoding="utf-8")):
            team_days[r["team_name_abbr"]].add(r["date"]); rows[r["bref_id"]].append((r["date"], r["team_name_abbr"]))
    pg = {norm(r["player"]): r["team"] for r in csv.DictReader(open(os.path.join(
        R.KIT, "..", "yahoo-fantasy-basketball", "arena", "results", "actuals_2026-10-09", "bref_pergame_2025-26.csv"), encoding="utf-8"))}

    def team_on(name, iso):
        rs = rows.get(ids.get(name), [])
        if not rs:
            return pg.get(norm(name))
        day = dt.date.fromisoformat(iso)
        return min(rs, key=lambda x: abs((dt.date.fromisoformat(x[0]) - day).days))[1]
    return team_days, team_on


def day_figures(roster, iso, ids, days):
    played = lambda p: iso in days.get(ids.get(p["name"]), ())
    active = [p for p in roster["players"] if p["selectedPosition"] not in R.IL]
    best = R.seat([set(p["position"].split(",")) for p in active if played(p)])
    started = sum(1 for p in active if p["selectedPosition"] != "BN" and played(p))
    benched = sorted(p["name"] for p in active if p["selectedPosition"] == "BN" and played(p))
    return best, started, benched


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("transcript")
    ap.add_argument("--since", required=True)
    a = ap.parse_args()
    found = extract(a.transcript, a.since)
    man, days = R.load_days()
    ids = man["resolved"]
    rec = json.load(open(os.path.join(HERE, "reconstruction_2025-26.json"), encoding="utf-8"))
    weekly = {(r["week"], r["manager"]): r for r in rec["rows"]}
    team_days, team_on = schedules(ids)
    lines = {}
    for path in (R.PRIOR, R.EXTRA):
        for r in csv.DictReader(open(path, encoding="utf-8")):
            lines[(r["bref_id"], r["date"])] = r
    truth = {(int(r["week"]), r["manager"]): r for r in csv.DictReader(open(R.TRUTH, encoding="utf-8"))}
    os.makedirs(os.path.join(HERE, "daily"), exist_ok=True)
    out, files, unknown = [], [], set()
    for week, mgr, tid, start in CASES:
        d0 = dt.date.fromisoformat(start)
        w = weekly[(week, mgr)]
        tot_best = tot_started = tot_starts = 0
        stat = {c: 0 for c, _ in TOTALS}
        per_day = []
        week_names = set()
        for k in range((dt.date.fromisoformat(w["end"]) - d0).days + 1):
            iso = (d0 + dt.timedelta(days=k)).isoformat()
            if k == 0:
                roster = json.load(open(os.path.join(HERE, "rosters", f"t{tid:02d}_{iso}.json"), encoding="utf-8"))
            else:
                if (str(tid), iso) not in found:
                    sys.exit(f"DAILY: FAIL — no roster for team {tid} on {iso}")
                roster = found[(str(tid), iso)][0]
                name = f"t{tid:02d}_{iso}.json"
                body = (json.dumps(roster, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
                open(os.path.join(HERE, "daily", name), "wb").write(body)
                files.append(dict(team_id=tid, date=iso, file=name, response_utc=found[(str(tid), iso)][1],
                                  sha256=hashlib.sha256(body).hexdigest()))
            week_names |= {p["name"] for p in roster["players"]}
            best, started, benched = day_figures(roster, iso, ids, days)
            in_slot = [p for p in roster["players"] if p["selectedPosition"] not in R.IL | {"BN"}]
            starts = sum(1 for p in in_slot if iso in team_days.get(team_on(p["name"], iso), ()))
            sat = sorted(p["name"] for p in in_slot if iso in team_days.get(team_on(p["name"], iso), ())
                         and iso not in days.get(ids.get(p["name"]), ()))
            for p in in_slot:
                ln = lines.get((ids.get(p["name"]), iso))
                for c, _ in TOTALS:
                    stat[c] += int(float(ln[c] or 0)) if ln else 0
            tot_best += best; tot_started += started; tot_starts += starts
            per_day.append(dict(date=iso, perfect=best, actual_lineup=started, starts=starts, benched_who_played=benched,
                                in_slot_did_not_play=sat))
        unknown |= {n for n in week_names if n not in ids and n not in man["no_games"]}
        out.append(dict(week=week, manager=mgr, team_id=tid, known=w["known"], weekly=w["reconstructed"], daily=tot_best,
                        lineup=tot_started, starts=tot_starts, roster_change=tot_best - w["reconstructed"], lineup_choice=tot_started - tot_best,
                        unexplained=w["known"] - tot_started,
                        totals_lineup={t: stat[c] for c, t in TOTALS},
                        totals_truth={t: int(truth[(week, mgr)][t]) for _, t in TOTALS},
                        totals_equal=all(stat[c] == int(truth[(week, mgr)][t]) for c, t in TOTALS), days=per_day))
    if unknown:
        sys.exit(f"DAILY: FAIL — names on the daily rosters with no game log resolved: {sorted(unknown)}")
    with open(os.path.join(HERE, "daily", "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(dict(source="Flaim get_roster (yahoo, 466.l.17544, season_year 2025), one per day", since=a.since,
                       files=files), f, indent=1); f.write("\n")
    with open(os.path.join(HERE, "diagnosis_daily.json"), "w", encoding="utf-8") as f:
        json.dump(dict(cases=out), f, indent=1); f.write("\n")
    for c in out:
        print(f"wk{c['week']} {c['manager']}: known {c['known']} | weekly {c['weekly']} -> daily {c['daily']} "
              f"(roster change {c['roster_change']:+}) -> lineup {c['lineup']} (lineup choice {c['lineup_choice']:+}) "
              f"| unexplained {c['unexplained']:+} | starts {c['starts']} | 11 totals equal: {c['totals_equal']}")
    print(f"DAILY: {len(files)} daily rosters pinned")


if __name__ == "__main__":
    main()
