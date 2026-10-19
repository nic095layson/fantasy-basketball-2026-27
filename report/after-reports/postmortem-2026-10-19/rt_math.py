#!/usr/bin/env python3
"""Red team, phase 1: known-answer re-implementation of the engine's category math, written from the formulas and not
from the engine, then compared to hoops.zscores and arena.team_week_model on the lock pool (players_v69.csv).
Also the kit engine's board (report/projections-2026-27.csv) against the deck's. Writes rt_math.json."""
import csv, json, math, os, sys
H=os.path.dirname(os.path.abspath(__file__)); DECK="/home/user/yahoo-fantasy-basketball"; KIT=os.path.normpath(os.path.join(H,"..","..",".."))
sys.path.insert(0,DECK+"/scripts"); sys.path.insert(0,DECK+"/arena"); import hoops, arena
POOL=f"{DECK}/arena/results/players_v69.csv"; hoops.DATA_PATH=POOL
rows=list(csv.DictReader(open(POOL,encoding="utf-8")))
NUM=("fg_pct","fga","ft_pct","fta","tpm","pts","reb","ast","stl","blk","tov")
for r in rows:
    for k in NUM: r[k]=float(r[k])
COUNT={"3PTM":"tpm","PTS":"pts","REB":"reb","AST":"ast","ST":"stl","BLK":"blk","TO":"tov"}
def avail(note):
    tag=(note or "").split(" ")[0].split("(")[0]
    if tag.startswith("out-"): return 0.0
    if "mild" in tag: return 0.85
    if "recovery" in tag: return 0.0
    if "risk" in tag: return 0.78
    return 1.0
def params(pool):
    lg_fg=sum(p["fg_pct"]*p["fga"] for p in pool)/sum(p["fga"] for p in pool)
    lg_ft=sum(p["ft_pct"]*p["fta"] for p in pool)/sum(p["fta"] for p in pool)
    vals={"FG%":[(p["fg_pct"]-lg_fg)*p["fga"] for p in pool],"FT%":[(p["ft_pct"]-lg_ft)*p["fta"] for p in pool]}
    for c,col in COUNT.items(): vals[c]=[p[col] for p in pool]
    prm={}
    for c,v in vals.items():
        m=sum(v)/len(v); s=math.sqrt(sum((x-m)**2 for x in v)/len(v)); prm[c]=(m,s)
    return lg_fg,lg_ft,prm
def apply(pool_all,lg_fg,lg_ft,prm):
    for p in pool_all:
        v={"FG%":(p["fg_pct"]-lg_fg)*p["fga"],"FT%":(p["ft_pct"]-lg_ft)*p["fta"]}
        for c,col in COUNT.items(): v[c]=p[col]
        p["z2"]={c:((v[c]-prm[c][0])/prm[c][1])*(-1 if c=="TO" else 1) for c in v}
        p["tv2"]=sum(p["z2"].values())
# fixed point exactly as documented: pass 0 full pool, then top-156 by total value among availability>0, iterate to a fixed set
apply(rows,*params(rows)); seen=set(); iters=0
for _ in range(5):
    top=sorted([p for p in rows if avail(p["note"])>0],key=lambda p:-p["tv2"])[:156]
    key=frozenset(p["player"] for p in top)
    if key in seen: break
    seen.add(key); apply(rows,*params(top)); iters+=1
E=hoops.zscores(hoops.load_players()); eby={p["player"]:p for p in E}
maxdz=max(abs(p["z2"][c]-eby[p["player"]]["z"][c]) for p in rows for c in p["z2"])
maxda=max(abs(avail(p["note"])-hoops.availability(eby[p["player"]])) for p in rows)
# independent adj_value and board order
for p in rows: p["adj2"]=p["tv2"]*avail(p["note"]) if p["tv2"]>0 else p["tv2"]
ord2=[p["player"] for p in sorted([p for p in rows if avail(p["note"])>0],key=lambda p:-p["adj2"])]
ord1=[p["player"] for p in sorted([p for p in E if hoops.availability(p)>0],key=lambda p:-hoops.adj_value(p))]
first_diff=next((i for i,(a,b) in enumerate(zip(ord1,ord2)) if a!=b),None)
# weekly percentage known-answer on the owner's roster: team FG% must be makes/attempts, never a mean of percentages
st=json.load(open(f"{DECK}/arena/data/states/draft_state_100.json")); mine=[eby[pk["player"]] for pk in st["picks"] if pk["slot"]==10]
mu,var=arena.team_week_model(mine); w=arena.daily_fill_weights(mine)
def wa(p):
    t=hoops.note_tag(p.get("note"));
    return 0.79 if "mild" in t else 0.60 if "recovery" in t else 0.75 if "risk" in t else 0.88
mk=sum(w[id(p)]*p["fg_pct"]*p["fga"]*3.5*wa(p) for p in mine); at=sum(w[id(p)]*p["fga"]*3.5*wa(p) for p in mine)
naive=sum(p["fg_pct"] for p in mine)/len(mine)
pts=sum(w[id(p)]*p["pts"]*3.5*wa(p) for p in mine)
pts_var=sum(w[id(p)]*((p["pts"]*0.30)**2*3.5*wa(p)+p["pts"]**2*3.5*wa(p)*(1-wa(p))) for p in mine)
# kit board vs deck board
kit=list(csv.DictReader(open(f"{KIT}/report/projections-2026-27.csv",encoding="utf-8")))
kcols=kit[0].keys(); kname=next(c for c in kcols if c.lower() in ("player","name"))
kby={r[kname]:r for r in kit}
common=[p for p in rows if p["player"] in kby]
numeric_cols=[c for c in ("pts","reb","ast","stl","blk","tpm","tov","fga","fta","fg_pct","ft_pct") if c in kcols]
line_diff=max(abs(float(kby[p["player"]][c])-p[c]) for p in common for c in numeric_cols) if numeric_cols else None
# the pinned league settings (kit data/league_settings.json, Session 1 item 2) against the engine's constants
LS=json.load(open(f"{KIT}/data/league_settings.json",encoding="utf-8"))
active=[x for x in LS["roster_positions"]["value"] if x not in ("BN","IL")]
slot_of=lambda sl: "Util" if sl is None else ("G" if sl==("PG","SG") else "F" if sl==("SF","PF") else sl[0])
engine_slots=[slot_of(sl) for sl in arena.LINEUP_SLOTS]
settings_check=dict(scoring_type=LS["scoring_type"]["value"],standings_rule_engine="cumulative category record (arena.simulate_seasons)",
    regular_season_weeks=dict(settings=LS["regular_season_weeks"]["value"],engine=arena.WEEKS,agree=LS["regular_season_weeks"]["value"]==arena.WEEKS),
    playoff_teams=dict(settings=LS["playoffs"]["value"]["teams"],engine=arena.PLAYOFF_TEAMS,agree=LS["playoffs"]["value"]["teams"]==arena.PLAYOFF_TEAMS),
    active_slots=dict(settings=active,engine=engine_slots,agree=active==engine_slots),
    categories_agree=LS["categories"]["value"]==list(hoops.CATS),
    playoff_reseeding=dict(settings=LS["playoff_reseeding"]["value"],semantics_note=LS["playoff_reseeding"].get("semantics"),engine="reseed() after round 1" if hasattr(arena,"reseed") else "fixed"),
    lineup_deadline=LS["lineup_deadline"]["value"],source=LS["_source"]["file"],received=LS["_source"]["received"],
    engine_commit=__import__("subprocess").check_output(["git","-C",DECK,"rev-parse","--short","HEAD"]).decode().strip())
out=dict(pool=os.path.relpath(POOL,DECK),rows=len(rows),fixed_point_iterations=iters,settings_check=settings_check,
 z_max_abs_diff=maxdz,availability_max_abs_diff=maxda,board_first_order_difference=first_diff,board_len=len(ord1),
 owner_week_fg=dict(engine=mu["FG%"],known_answer=mk/at,naive_mean_of_pcts=naive,abs_diff=abs(mu["FG%"]-mk/at)),
 owner_week_fg_var=dict(engine=var["FG%"],known_answer=(1.15**2)*(mk/at)*(1-mk/at)/at),
 owner_week_pts=dict(engine_mu=mu["PTS"],known_answer_mu=pts,engine_var=var["PTS"],known_answer_var=pts_var),
 kit_vs_deck=dict(kit_rows=len(kit),common=len(common),columns=numeric_cols,max_abs_line_diff=line_diff))
json.dump(out,open(os.path.join(H,"rt_math.json"),"w"),indent=1)
print(json.dumps(out,indent=1))
