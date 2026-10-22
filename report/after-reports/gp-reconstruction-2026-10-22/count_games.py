#!/usr/bin/env python3
"""D-GP-1 stage 1 (owner 2026-10-22, "Count real games, 2025-26 first"): the player-games actually behind each of the 44
known 2025-26 team-weeks, and whether they reproduce Yahoo's own totals. The method was stated to the owner before the run:

  lineup       the players in an active slot (not BN, IL, IL+) of each day's Yahoo roster: the week-start roster pinned in
               rosters/, then one Flaim get_roster snapshot per later day, pinned to daily/ (daily/manifest_all.json)
  player-game  a Basketball-Reference game-log row for that player on that date (#159's logs plus gamelogs_extra)
  totals       the lineup's makes and attempts, threes, points, rebounds, assists, steals, blocks and turnovers (11
               numbers) against Yahoo's own week totals in the pinned Flaim matchups
               (data/source/flaim/history/466.l.17544/matchups_weekNN.json)
  status       ACCEPTED all 11 exact; NEAR every total within 2 and at least one off (count kept, flagged);
               REJECTED otherwise (no count published for that week)
  stop rule    9 or more of the 44 REJECTED: the series is not published (the CSV carries no counts) and the misses are
               diagnosed instead

Each later-day roster is read from the session transcript where the connector's answer landed; a team-day answered twice
with different content stops the run. The 28 days the diagnosis pinned (daily/manifest.json) must come out byte-identical.
2025-26 only; nothing here feeds a model or the deck. Writes player_games_2025-26.csv and player_games_2025-26.json.

    python3 count_games.py TRANSCRIPT.jsonl --since 2026-10-22T00:38:15Z   pin the daily rosters from the transcript, then count
    python3 count_games.py --pinned                                         count from the pinned daily/ files (each sha256
                                                                            must equal daily/manifest_all.json's); no transcript"""
import argparse, csv, datetime as dt, hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import reconstruct as R  # noqa: E402
from extract_rosters import LEAGUE, TEAM, LL, _data, week_start  # noqa: E402

MATCHUPS = os.path.join(R.KIT, "data", "source", "flaim", "history", LEAGUE, "matchups_week{:02d}.json")
# (game-log column, Yahoo total / truth-file column)
TOTALS = [("fg", "fgm"), ("fga", "fga"), ("ft", "ftm"), ("fta", "fta"), ("fg3", "tpm"), ("pts", "pts"), ("trb", "reb"),
          ("ast", "ast"), ("stl", "stl"), ("blk", "blk"), ("tov", "tov")]
STOP_AT = 9


def status(diffs):
    """ACCEPTED / NEAR / REJECTED from the 11 differences (lineup minus Yahoo)."""
    worst = max(abs(v) for v in diffs.values())
    return "ACCEPTED" if worst == 0 else "NEAR" if worst <= 2 else "REJECTED"


def yahoo_totals(week, tid):
    """The team's 11 totals as Yahoo scored them that week (the pinned Flaim matchups file)."""
    for m in json.load(open(MATCHUPS.format(week), encoding="utf-8"))["matchups"]:
        for side in ("away", "home"):
            if m[side]["teamId"] == str(tid):
                c = {x["displayName"]: x["value"] for x in m[side]["categories"]}
                fgm, fga = c["FGM/A"].split("/")
                ftm, fta = c["FTM/A"].split("/")
                return dict(fgm=int(fgm), fga=int(fga), ftm=int(ftm), fta=int(fta), tpm=int(c["3PTM"]), pts=int(c["PTS"]),
                            reb=int(c["REB"]), ast=int(c["AST"]), stl=int(c["ST"]), blk=int(c["BLK"]), tov=int(c["TO"]))
    sys.exit(f"GAMES: FAIL — team {tid} is in no matchup of week {week}")


def snapshots(transcript, since):
    """Every distinct dated roster answer for the league in the transcript: {(team id, date): [(data, timestamp), ...]}."""
    since = LL.since_instant(since)
    seen = {}
    for line in open(transcript, encoding="utf-8"):
        o = LL._loads(line)
        if not isinstance(o, dict) or not LL.recent(o, since):
            continue

        def walk(x):
            if isinstance(x, str):
                if '"teamKey"' in x:
                    d = _data(x)
                    if d is not None and str(d.get("teamKey", "")).startswith(LEAGUE + ".t.") \
                            and (d.get("snapshot") or {}).get("type") == "date":
                        key = (d["teamKey"].rsplit(".t.", 1)[1], d["snapshot"]["date"])
                        body = json.dumps(d, sort_keys=True)
                        if body not in {json.dumps(v, sort_keys=True) for v, _ in seen.get(key, [])}:
                            seen.setdefault(key, []).append((d, o.get("timestamp")))
            elif isinstance(x, dict):
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
        walk(o.get("message", {}).get("content"))
    return seen


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("transcript", nargs="?")
    ap.add_argument("--since")
    ap.add_argument("--pinned", action="store_true")
    a = ap.parse_args()
    if not a.pinned and not (a.transcript and a.since):
        ap.error("give TRANSCRIPT and --since, or --pinned")
    weeks = []
    for r in csv.DictReader(open(R.TRUTH, encoding="utf-8")):
        weeks.append(dict(week=int(r["week"]), dates=r["dates"], manager=r["manager"], team_id=TEAM[r["manager"]],
                          start=week_start(r["dates"]), end=R.week_end(r["dates"]), counter=int(r["gp"]),
                          truth={t: int(r[t]) for _, t in TOTALS}))
    if a.pinned:
        seen = {}
        pinned = json.load(open(os.path.join(HERE, "daily", "manifest_all.json"), encoding="utf-8"))
        a.since = pinned["since"]
        for f in pinned["files"]:
            body = open(os.path.join(HERE, "daily", f["file"]), "rb").read()
            if hashlib.sha256(body).hexdigest() != f["sha256"]:
                sys.exit(f"GAMES: FAIL — daily/{f['file']} differs from daily/manifest_all.json's sha256")
            seen[(str(f["team_id"]), f["date"])] = [(json.loads(body), f["response_utc"])]
    else:
        seen = snapshots(a.transcript, a.since)
    os.makedirs(os.path.join(HERE, "daily"), exist_ok=True)
    diag = {f["file"]: f["sha256"] for f in json.load(open(os.path.join(HERE, "daily", "manifest.json"), encoding="utf-8"))["files"]}
    files, rosters, missing, conflicts = [], {}, [], []
    for w in weeks:
        tid = w["team_id"]
        for k in range((w["end"] - w["start"]).days + 1):
            iso = (w["start"] + dt.timedelta(days=k)).isoformat()
            if k == 0:
                rosters[(tid, iso)] = json.load(open(os.path.join(HERE, "rosters", f"t{tid:02d}_{iso}.json"), encoding="utf-8"))
                continue
            got = seen.get((str(tid), iso), [])
            if not got:
                missing.append(f"t{tid}/{iso}"); continue
            if len(got) > 1:
                conflicts.append(f"t{tid}/{iso}"); continue
            data, ts = got[0]
            name = f"t{tid:02d}_{iso}.json"
            body = (json.dumps(data, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
            sha = hashlib.sha256(body).hexdigest()
            if name in diag and diag[name] != sha:
                sys.exit(f"GAMES: FAIL — {name} differs from the copy the diagnosis pinned")
            open(os.path.join(HERE, "daily", name), "wb").write(body)
            files.append(dict(team_id=tid, date=iso, file=name, response_utc=ts, sha256=sha))
            rosters[(tid, iso)] = data
    if missing or conflicts:
        sys.exit(f"GAMES: FAIL — {len(missing)} team-days with no roster {missing[:8]}, "
                 f"{len(conflicts)} answered twice differently {conflicts[:8]}")
    with open(os.path.join(HERE, "daily", "manifest_all.json"), "w", encoding="utf-8") as f:
        json.dump(dict(source="Flaim get_roster (yahoo, 466.l.17544, season_year 2025), one per day after each week's first",
                       since=a.since, team_days=len(files), matches_diagnosis=sum(1 for x in files if x["file"] in diag),
                       files=files), f, indent=1); f.write("\n")

    man, _ = R.load_days()
    ids, no_games = man["resolved"], set(man["no_games"])
    names = {p["name"] for ro in rosters.values() for p in ro["players"]}
    unknown = sorted(n for n in names if n not in ids and n not in no_games)
    if unknown:
        sys.exit(f"GAMES: FAIL — {len(unknown)} rostered names have no game log resolved (rerun pull_logs.py): {unknown}")
    lines = {}
    for path in (R.PRIOR, R.EXTRA):
        for r in csv.DictReader(open(path, encoding="utf-8")):
            lines[(r["bref_id"], r["date"])] = r

    rows = []
    for w in weeks:
        tid, games, stat = w["team_id"], 0, {c: 0 for c, _ in TOTALS}
        for k in range((w["end"] - w["start"]).days + 1):
            iso = (w["start"] + dt.timedelta(days=k)).isoformat()
            for p in rosters[(tid, iso)]["players"]:
                if p["selectedPosition"] in R.IL | {"BN"}:
                    continue
                ln = lines.get((ids.get(p["name"]), iso))
                if ln:
                    games += 1
                    for c, _ in TOTALS:
                        stat[c] += int(float(ln[c] or 0))
        yahoo = yahoo_totals(w["week"], tid)
        diffs = {t: stat[c] - yahoo[t] for c, t in TOTALS}
        rows.append(dict(week=w["week"], dates=w["dates"], manager=w["manager"], team_id=tid, start=w["start"].isoformat(),
                         end=w["end"].isoformat(), days=(w["end"] - w["start"]).days + 1, player_games=games,
                         yahoo_games_counter=w["counter"], status=status(diffs),
                         off={t: v for t, v in diffs.items() if v}, lineup_totals={t: stat[c] for c, t in TOTALS},
                         yahoo_totals=yahoo, truth_file_equals_yahoo=w["truth"] == yahoo))
    count = {s: sum(1 for r in rows if r["status"] == s) for s in ("ACCEPTED", "NEAR", "REJECTED")}
    publish = count["REJECTED"] < STOP_AT
    with open(os.path.join(HERE, "player_games_2025-26.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["season", "week", "dates", "manager", "team_id", "days", "player_games", "yahoo_games_counter", "status",
                     "totals_off"])
        for r in rows:
            shown = r["player_games"] if publish and r["status"] != "REJECTED" else ""
            wr.writerow(["2025-26", r["week"], r["dates"], r["manager"], r["team_id"], r["days"], shown,
                         r["yahoo_games_counter"], r["status"], "; ".join(f"{t} {v:+d}" for t, v in r["off"].items())])
    with open(os.path.join(HERE, "player_games_2025-26.json"), "w", encoding="utf-8") as f:
        json.dump(dict(method="count_games.py docstring (stated to the owner before the run)", stop_at=STOP_AT,
                       counts=count, published=publish, team_days_pinned=len(files), rows=rows), f, indent=1); f.write("\n")
    gap = [r["player_games"] - r["yahoo_games_counter"] for r in rows]
    print(f"GAMES: {'PUBLISHED' if publish else 'NOT PUBLISHED (stop rule)'} — {len(rows)} team-weeks: "
          f"{count['ACCEPTED']} ACCEPTED, {count['NEAR']} NEAR, {count['REJECTED']} REJECTED (stop at {STOP_AT}); "
          f"{len(files)} later-day rosters pinned, {sum(1 for x in files if x['file'] in diag)} equal to the diagnosis copies")
    print(f"  player-games minus Yahoo's counter: min {min(gap):+d}, max {max(gap):+d}, "
          f"equal in {sum(1 for g in gap if g == 0)} of {len(gap)}")
    for r in rows:
        if r["status"] != "ACCEPTED":
            print(f"  wk{r['week']} {r['manager']}: {r['status']} {r['off']}")


if __name__ == "__main__":
    main()
