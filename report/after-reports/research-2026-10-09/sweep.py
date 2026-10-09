"""ESPN summaries (untrusted JSON, run with -I) -> target-player lines, team starters, injury rows. Args: out_dir sum_*.json..."""
import json, sys, os, re, unicodedata, collections
def fold(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'’]", "", s); s = re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()
TARGETS = ["Dyson Daniels","Nickeil Alexander-Walker","Luguentz Dort","Onyeka Okongwu","CJ McCollum","Jalen Johnson",
 "Chet Holmgren","Aday Mara","Isaiah Hartenstein","Jalen Williams","Jaylin Williams",
 "Daniel Gafford","Dereck Lively II","Anthony Davis","Kyrie Irving","Cooper Flagg","Naji Marshall","P.J. Washington",
 "Isaiah Jackson","Brook Lopez","Rui Hachimura","Brandon Ingram","Khaman Maluach","Oso Ighodaro","Mark Williams",
 "Kon Knueppel","Coby White","Nic Claxton","Darius Garland","Jakob Poeltl","Kevin Durant","Alperen Sengun",
 "Ryan Rollins","Michael Porter Jr.","Neemias Queta","Mitchell Robinson","DeMar DeRozan","Ty Jerome","Jaren Jackson Jr.",
 "Kristaps Porzingis","Desmond Bane","Tyler Herro","Zach LaVine","Fred VanVleet","Victor Wembanyama","Jabari Smith Jr.","Steven Adams","Clint Capela"]
T = {fold(n): n for n in TARGETS}
TEAMS = {"DAL","PHX","OKC","IND","ATL","LAL","CLE","SA","HOU","BKN","CHI","CHA","NY","BOS","MIL","UTAH","MIA","TOR","MIN","DEN"}
out = sys.argv[1]; rows=[]; starters=[]; inj=[]
for f in sys.argv[2:]:
    d = json.load(open(f)); gid = os.path.basename(f)[4:-5]
    h = d["header"]["competitions"][0]
    comp = {c["team"]["abbreviation"]: c for c in h["competitors"]}
    import datetime as _dt; date = (_dt.datetime.strptime(h["date"][:16], "%Y-%m-%dT%H:%M") - _dt.timedelta(hours=4)).strftime("%Y-%m-%d")  # ET game date
    for tb in d["boxscore"].get("players", []):
        ab = tb["team"]["abbreviation"]; opp = [a for a in comp if a != ab][0]
        st = tb["statistics"][0]; keys = st.get("keys")
        sl=[]
        for a in st["athletes"]:
            nm = a["athlete"]["displayName"]; k = fold(nm)
            if a.get("starter"): sl.append(nm)
            if k not in T: continue
            if a.get("didNotPlay"):
                rows.append([date,gid,ab,opp,T[k],"DNP",a.get("reason",""),"","","","","","","","","",""]); continue
            v = dict(zip(keys, a.get("stats", [])))
            rows.append([date,gid,ab,opp,T[k],"S" if a.get("starter") else "B","",v.get("minutes",""),v.get("points",""),v.get("rebounds",""),v.get("assists",""),v.get("steals",""),v.get("blocks",""),v.get("turnovers",""),v.get("fieldGoalsMade-fieldGoalsAttempted",""),v.get("threePointFieldGoalsMade-threePointFieldGoalsAttempted",""),v.get("freeThrowsMade-freeThrowsAttempted","")])
        if ab in TEAMS: starters.append(f"{date} {gid} {ab} vs {opp}: " + ", ".join(sl))
    for ib in d.get("injuries", []):
        ab = ib.get("team", {}).get("abbreviation", "?")
        for i in ib.get("injuries", []):
            nm = i.get("athlete", {}).get("displayName", "?"); k = fold(nm)
            if k not in T: continue
            det = i.get("details", {}) or {}
            inj.append(f"{date} {gid} {ab} {nm}: {i.get('status','')} | {det.get('side','')} {det.get('location','')} {det.get('type','')} {det.get('detail','')} | return {det.get('returnDate','')} | {(i.get('shortComment') or '')[:200]}")
rows.sort(key=lambda r:(r[4],r[0]))
hdr=["date","game","team","opp","player","role","reason","min","pts","reb","ast","stl","blk","tov","fg","3pt","ft"]
with open(os.path.join(out,"sweep.tsv"),"w") as fh:
    fh.write("\t".join(hdr)+"\n")
    for r in rows: fh.write("\t".join(str(x) for x in r)+"\n")
open(os.path.join(out,"starters.txt"),"w").write("\n".join(sorted(starters))+"\n")
# dedupe injury rows by (team, name, status, body) keeping the latest date
seen={}
for line in sorted(inj):
    key=line.split(" ",2)[2]
    seen[key]=line
open(os.path.join(out,"injuries.txt"),"w").write("\n".join(seen.values())+"\n")
# rollup
roll=collections.OrderedDict()
for r in rows:
    p=r[4]; g=roll.setdefault(p,dict(games=0,played=0,starts=0,mins=[],dnp=[]))
    g["games"]+=1
    if r[5]=="DNP": g["dnp"].append(f"{r[0]} {r[6]}")
    else:
        g["played"]+=1; g["starts"]+= r[5]=="S"; g["mins"].append(int(r[7] or 0))
with open(os.path.join(out,"rollup.txt"),"w") as fh:
    for p,g in roll.items():
        fh.write(f"{p:28s} games {g['games']} played {g['played']} starts {g['starts']} min {g['mins']} dnp {g['dnp']}\n")
print(len(rows),"rows;",len(starters),"starter lines;",len(seen),"injury rows")
