"""Parse ESPN preseason summaries (untrusted JSON, run with python3 -I) into per-player role rows:
team, games, starts, minutes total/avg, per-game list (date, opp, starter, min). Also per-team game counts."""
import json, glob, os, sys, re, datetime
DL, OUT = sys.argv[1], sys.argv[2]
games = []; players = {}; teamgames = {}
for f in sorted(glob.glob(os.path.join(DL, "summary_*.json"))):
    d = json.load(open(f, encoding="utf-8"))
    hdr = d.get("header", {}); comp = (hdr.get("competitions") or [{}])[0]
    utc = comp.get("date") or ""; gid = hdr.get("id")
    # ESPN's timestamp is UTC; the game's local (US Eastern, EDT = UTC-4 until 2026-11-01) date is what outlets print.
    date = (datetime.datetime.strptime(utc[:16], "%Y-%m-%dT%H:%M") - datetime.timedelta(hours=4)).strftime("%Y-%m-%d") if utc else ""
    teams = {c["team"]["id"]: c["team"].get("abbreviation") for c in comp.get("competitors", [])}
    box = d.get("boxscore", {}).get("players", [])
    if not box: games.append(dict(id=gid, date=date, utc=utc, teams=list(teams.values()), box=False)); continue
    games.append(dict(id=gid, date=date, utc=utc, teams=list(teams.values()), box=True))
    for tb in box:
        ab = tb["team"].get("abbreviation"); opp = [a for a in teams.values() if a != ab]
        teamgames.setdefault(ab, set()).add(gid)
        st = tb["statistics"][0]; keys = st.get("keys") or st.get("names") or st.get("labels")
        for a in st.get("athletes", []):
            nm = a["athlete"]["displayName"]; aid = a["athlete"]["id"]
            rec = players.setdefault(aid, dict(name=nm, teams=set(), games=[]))
            rec["teams"].add(ab)
            dnp = a.get("didNotPlay") or not a.get("stats")
            mins = 0.0
            if not dnp:
                s = dict(zip(keys, a["stats"]))
                mv = s.get("minutes", s.get("MIN", "0"))
                try: mins = float(mv)
                except: mins = 0.0
            rec["games"].append(dict(date=date, gid=gid, team=ab, opp=opp[0] if opp else "", starter=bool(a.get("starter")), dnp=bool(dnp), min=mins,
                                     reason=a.get("reason", "")))
out = dict(games=games, team_games={k: len(v) for k, v in sorted(teamgames.items())}, players=[])
for aid, r in players.items():
    played = [g for g in r["games"] if not g["dnp"]]
    out["players"].append(dict(id=aid, name=r["name"], teams=sorted(r["teams"]), gp=len(played), starts=sum(1 for g in played if g["starter"]),
                               min_total=round(sum(g["min"] for g in played), 1), mpg=round(sum(g["min"] for g in played) / len(played), 1) if played else 0.0,
                               dnp=sum(1 for g in r["games"] if g["dnp"]), games=r["games"]))
json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1)
print(len(games), "games;", sum(1 for g in games if g["box"]), "with box;", len(out["players"]), "players")
print("team games:", out["team_games"])
