#!/usr/bin/env python3
"""GP reconstruction test (owner 2026-10-22 "Test, then weekly"): pin the 44 week-start Yahoo rosters of 2025-26 that the
reconstruction runs on. Each is a Flaim get_roster response (league 466.l.17544, season_year 2025, as_of_date = the
matchup week's first day) for one team-week of the deck's arena/data/weekly_matchups_2025-26.csv, read from the session
transcript where the connector's answer landed. Writes rosters/t<team>_<date>.json (the response's data object, raw)
and rosters/manifest.json (sha256, the transcript entry's timestamp). Exits non-zero unless all 44 pairs are found.

    python3 extract_rosters.py TRANSCRIPT.jsonl --since 2026-10-22T00:38:15Z"""
import argparse, csv, datetime as dt, hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(KIT, "scripts"))
import league_live as LL  # noqa: E402
from flaim_live import _data  # noqa: E402

LEAGUE = "466.l.17544"
TRUTH = os.path.join(KIT, "..", "yahoo-fantasy-basketball", "arena", "data", "weekly_matchups_2025-26.csv")
# manager first name (the truth file) -> Yahoo team id (Flaim get_league_info for 466.l.17544, 2026-10-22)
TEAM = {"William": 1, "Robert": 2, "Christian Oblena": 3, "JCo": 4, "Kyle": 5, "Martin": 6, "Hegi": 7, "Kevin": 8,
        "Noah": 9, "Justin": 10, "David": 11, "John": 12}


def week_start(dates):
    """'10/21-10/26' -> 2025-10-21; October to December are 2025, January on 2026."""
    m, d = (int(x) for x in dates.split("-")[0].split("/"))
    return dt.date(2025 if m >= 10 else 2026, m, d)


def wanted():
    out = []
    for r in csv.DictReader(open(TRUTH, encoding="utf-8")):
        out.append((r["week"], str(TEAM[r["manager"]]), week_start(r["dates"]).isoformat()))
    return out


def extract(transcript, since):
    since = LL.since_instant(since)
    found = {}
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
                        tid = d["teamKey"].rsplit(".t.", 1)[1]
                        found[(tid, d["snapshot"]["date"])] = (d, o.get("timestamp"))
            elif isinstance(x, dict):
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
        walk(o.get("message", {}).get("content"))
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("transcript")
    ap.add_argument("--since", required=True)
    a = ap.parse_args()
    found = extract(a.transcript, a.since)
    want = wanted()
    missing = [(w, t, d) for w, t, d in want if (t, d) not in found]
    if missing:
        sys.exit(f"ROSTERS: FAIL — {len(missing)} of {len(want)} team-weeks have no roster: {missing}")
    os.makedirs(os.path.join(HERE, "rosters"), exist_ok=True)
    files = []
    for w, t, d in want:
        data, ts = found[(t, d)]
        name = f"t{int(t):02d}_{d}.json"
        body = (json.dumps(data, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
        open(os.path.join(HERE, "rosters", name), "wb").write(body)
        files.append(dict(week=int(w), team_id=int(t), date=d, file=name, players=len(data["players"]),
                          response_utc=ts, sha256=hashlib.sha256(body).hexdigest()))
    man = dict(source="Flaim get_roster (platform yahoo, league 466.l.17544, season_year 2025, as_of_date = week start)",
               transcript=os.path.basename(a.transcript), since=a.since, team_weeks=len(files), files=files)
    with open(os.path.join(HERE, "rosters", "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(man, f, indent=1); f.write("\n")
    print(f"ROSTERS: PASS — {len(files)} of {len(want)} team-weeks pinned, "
          f"{len({p['name'] for t, d in found for p in found[(t, d)][0]['players'] if (t, d) in {(x[1], x[2]) for x in want}})} players")


if __name__ == "__main__":
    main()
