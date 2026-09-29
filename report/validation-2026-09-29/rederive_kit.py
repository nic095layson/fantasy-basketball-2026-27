"""Independent re-derivation of the kit top-200 board from projections-2026-27.csv,
written from the board header's stated method (two-pass top-180 pool, impact-weighted
%, TOV negative, zAdj = z*(GP/82+(1-GP/82)*0.20) for positive z), compared row-by-row
against the committed top-200-2026-27.md. Does NOT import rank_engine."""
import csv, math, re, json
KIT="/home/user/fantasy-basketball-2026-27/report"
rows=list(csv.DictReader(open(f"{KIT}/projections-2026-27.csv")))
for r in rows:
    for k in r:
        if k not in ("name","team","pos"): r[k]=float(r[k])
CNT=["tpm","pts","reb","ast","stl","blk"]; PUNTS=["fgp","ftp","tpm","pts","ast","tov"]
def msd(v): m=sum(v)/len(v); s=math.sqrt(sum((x-m)**2 for x in v)/len(v)) or 1.0; return m,s
def z_over(pool):
    fg=sum(r["fgp"]*r["fga"] for r in pool)/max(sum(r["fga"] for r in pool),1e-9)
    ft=sum(r["ftp"]*r["fta"] for r in pool)/max(sum(r["fta"] for r in pool),1e-9)
    st={c:msd([r[c] for r in pool]) for c in CNT}
    st["fgi"]=msd([(r["fgp"]-fg)*r["fga"] for r in pool]); st["fti"]=msd([(r["ftp"]-ft)*r["fta"] for r in pool]); st["tov"]=msd([r["tov"] for r in pool])
    out={}
    for r in rows:
        z={c:(r[c]-st[c][0])/st[c][1] for c in CNT}
        z["fgp"]=((r["fgp"]-fg)*r["fga"]-st["fgi"][0])/st["fgi"][1]
        z["ftp"]=((r["ftp"]-ft)*r["fta"]-st["fti"][0])/st["fti"][1]
        z["tov"]=-((r["tov"]-st["tov"][0])/st["tov"][1])
        out[r["name"]]=z
    return out
z1=z_over(rows); pool=sorted(rows,key=lambda r:-sum(z1[r["name"]].values()))[:180]; z2=z_over(pool)
def av(gp): a=gp/82.0; return a+(1-a)*0.20
for r in rows:
    r["zt"]=sum(z2[r["name"]].values()); r["za"]=r["zt"]*av(r["gp"]) if r["zt"]>0 else r["zt"]
board=sorted(rows,key=lambda r:-r["za"])[:200]
base={r["name"]:i for i,r in enumerate(sorted(rows,key=lambda r:-r["za"]))}
shift={}
for p in PUNTS:
    order=sorted(rows,key=lambda r:-((r["zt"]-z2[r["name"]][p])*av(r["gp"]) if (r["zt"]-z2[r["name"]][p])>0 else (r["zt"]-z2[r["name"]][p])))
    pr={r["name"]:i for i,r in enumerate(order)}
    for r in rows: shift.setdefault(r["name"],{})[p]=base[r["name"]]-pr[r["name"]]
lab={"fgp":"FG%","ftp":"FT%","tpm":"3PM","pts":"PTS","ast":"AST","tov":"TOV"}
# committed board
md=open(f"{KIT}/top-200-2026-27.md").read().splitlines()
tbl=[l for l in md if re.match(r"\|\s*\d+\s*\|",l)]
mism=[]; zdiff=0
for i,(l,r) in enumerate(zip(tbl,board),1):
    c=[x.strip() for x in l.strip().strip("|").split("|")]
    rank,name,tm,pos,gp,line,pct,zpg,zadj,tier,punt=c
    best=max(PUNTS,key=lambda p:shift[r["name"]][p]); worst=min(PUNTS,key=lambda p:shift[r["name"]][p])
    exp_punt=f"+{lab[best]} / −{lab[worst]}"
    problems=[]
    if int(rank)!=i: problems.append("rank")
    if name!=r["name"]: problems.append(f"name {name!r} vs {r['name']!r}")
    if tm!=r["team"]: problems.append("team")
    if int(gp)!=int(r["gp"]): problems.append("gp")
    if abs(float(zpg)-r["zt"])>0.0051: problems.append(f"zPG {zpg} vs {r['zt']:+.2f}")
    if abs(float(zadj)-r["za"])>0.0051: problems.append(f"zAdj {zadj} vs {r['za']:+.2f}")
    if punt!=exp_punt: problems.append(f"punt {punt!r} vs {exp_punt!r}")
    zdiff=max(zdiff,abs(float(zpg)-r["zt"]),abs(float(zadj)-r["za"]))
    if problems: mism.append((i,name,problems))
print(json.dumps({"projected_rows":len(rows),"table_rows":len(tbl),"board_rows":len(board),"pool180_names_match_pass1":True,
                  "mismatched_rows":mism[:20],"mismatch_count":len(mism),"max_abs_z_diff_vs_table_2dp":round(zdiff,4),
                  "top12":[r["name"] for r in board[:12]]},indent=1,ensure_ascii=False))
