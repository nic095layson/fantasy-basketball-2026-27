"""Opponent-gap assessment (2026-10-22): rebuild Yahoo's week-1 to-date totals from the actual daily lineups.
Lineups: Flaim get_roster as_of_date results, extracted mechanically from the session transcript.
Boxes: data/actuals/{date}.json in the kit worktree. Yahoo totals: the 14:15Z Flaim pin."""
import json, sys, unicodedata, re
T, KIT = sys.argv[1], sys.argv[2]
STATS = ["fgm","fga","ftm","fta","tpm","pts","reb","ast","stl","blk","tov"]
def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode().lower()
    s = re.sub(r"[.'’]", "", s); s = re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", s)
    return " ".join(s.split())
# 1) daily rosters from the transcript (date snapshots), last occurrence wins
lineups = {}
for line in open(T, encoding="utf-8"):
    if '"type\\":\\"date\\"' not in line and '"type":"date"' not in line: continue
    try: ev = json.loads(line)
    except Exception: continue
    msg = ev.get("message") or {}
    for c in (msg.get("content") or []) if isinstance(msg.get("content"), list) else []:
        if c.get("type") != "tool_result": continue
        body = c.get("content")
        texts = [x.get("text","") for x in body] if isinstance(body, list) else [body or ""]
        for t in texts:
            try: r = json.loads(t)
            except Exception: continue
            d = (r.get("data") or {})
            snap = d.get("snapshot") or {}
            if snap.get("type") == "date" and str(d.get("teamKey","")).startswith("478.l.36464.t."):
                lineups[(d["teamKey"].split(".t.")[1], snap["date"])] = d["players"]
print("lineups found:", sorted(lineups))
pin = json.load(open(f"{KIT}/data/source/flaim/pull_2026-10-22.json"))
def yahoo_tot(team_id):
    for m in pin["matchups"]["1"]["matchups"]:
        for side in ("home","away"):
            s = m[side]
            if s["teamId"] == team_id:
                c = {x["displayName"]: x["value"] for x in s["categories"]}
                fgm, fga = map(int, c["FGM/A"].split("/")); ftm, fta = map(int, c["FTM/A"].split("/"))
                return dict(fgm=fgm, fga=fga, ftm=ftm, fta=fta, tpm=int(c["3PTM"]), pts=int(c["PTS"]), reb=int(c["REB"]),
                            ast=int(c["AST"]), stl=int(c["ST"]), blk=int(c["BLK"]), tov=int(c["TO"]))
out = {}
for team in ("10","11"):
    tot = {k:0 for k in STATS}; rows = []
    for d in ("2026-10-20","2026-10-21"):
        box = json.load(open(f"{KIT}/data/actuals/{d}.json"))
        regular = {g["espn_id"] for g in box["games"] if g.get("season_type") == 2}
        byname = {norm(p["name"]): p for p in box["players"] if p.get("game") in regular}
        for pl in lineups[(team, d)]:
            slot = pl["selectedPosition"]; b = byname.get(norm(pl["name"]))
            played = bool(b) and not b.get("dnp")
            line = {k: (b.get(k) or 0) for k in STATS} if played else None
            rows.append(dict(date=d, player=pl["name"], slot=slot, played=played, pool_name=(b or {}).get("pool_name"), line=line))
            if played and slot not in ("BN","IL","IL+"):
                for k in STATS: tot[k] += line[k]
    y = yahoo_tot(team)
    out[team] = dict(actual_lineup_total=tot, yahoo=y, equal=(tot == y), rows=rows)
    print(team, "lineup sum == Yahoo:", tot == y); print("  lineup", tot); print("  yahoo ", y)
json.dump(out, open(sys.argv[3], "w"), indent=1)
