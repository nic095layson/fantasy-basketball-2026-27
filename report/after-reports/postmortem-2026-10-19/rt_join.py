#!/usr/bin/env python3
"""Red team, phase 1b: the kit board (report/projections-2026-27.csv) against the deck pool (players_v69.csv): name
join by exact spelling, then hoops.fold, then the kit's documented ALIASES table (report/market/build_market.py, read
by AST as the deck's repeat_market_check does); the per-game lines compared on every joined row. Writes rt_join.json."""
import ast, csv, json, os, sys
H=os.path.dirname(os.path.abspath(__file__)); DECK="/home/user/yahoo-fantasy-basketball"; KIT=os.path.normpath(os.path.join(H,"..","..",".."))
sys.path.insert(0,DECK+"/scripts"); import hoops
tree=ast.parse(open(f"{KIT}/report/market/build_market.py",encoding="utf-8").read()); AL={}
for node in ast.walk(tree):
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="ALIASES" for t in node.targets): AL=ast.literal_eval(node.value)
deck=list(csv.DictReader(open(f"{DECK}/arena/results/players_v69.csv",encoding="utf-8"))); dby={r["player"]:r for r in deck}; fold_deck={hoops.fold(n):n for n in dby}
kit=list(csv.DictReader(open(f"{KIT}/report/projections-2026-27.csv",encoding="utf-8")))
canon={}
for k,v in AL.items():
    if isinstance(v,str): canon[hoops.fold(k)]=v
    elif isinstance(v,(list,tuple)):
        for s in v: canon[hoops.fold(s)]=k
how={"exact":0,"fold":0,"alias":0}; unmatched=[]; pairs=[]
for r in kit:
    n=r["name"]
    if n in dby: how["exact"]+=1; pairs.append((r,dby[n]))
    elif hoops.fold(n) in fold_deck: how["fold"]+=1; pairs.append((r,dby[fold_deck[hoops.fold(n)]]))
    elif hoops.fold(n) in canon and (canon[hoops.fold(n)] in dby or hoops.fold(canon[hoops.fold(n)]) in fold_deck):
        c=canon[hoops.fold(n)]; how["alias"]+=1; pairs.append((r,dby.get(c) or dby[fold_deck[hoops.fold(c)]]))
    else: unmatched.append(n)
cols={"pts":"pts","reb":"reb","ast":"ast","stl":"stl","blk":"blk","tpm":"tpm","tov":"tov","fga":"fga","fta":"fta","fgp":"fg_pct","ftp":"ft_pct"}
diffs=[(k["name"],c,float(k[c]),float(d[dc])) for k,d in pairs for c,dc in cols.items() if abs(float(k[c])-float(d[dc]))>1e-9]
# the unmatched names once more by surname + a compatible first name (one a prefix of the other: Cam/Cameron,
# Herb/Herbert; a bare initial is NOT enough — the first draft of this rule paired Kris Murray with Keegan Murray)
first=lambda n: hoops.fold(n).split()[0]
sur={}
for n in dby: sur.setdefault(hoops.surname_key(n), []).append(n)
by_initial={}
for n in unmatched:
    c=[d for d in sur.get(hoops.surname_key(n), []) if first(d).startswith(first(n)) or first(n).startswith(first(d))]
    by_initial[n]=c[0] if len(c)==1 else None
variant_pairs=[(next(r for r in kit if r["name"]==n), dby[d]) for n,d in by_initial.items() if d]
vdiffs=[(k["name"],c,float(k[c]),float(d[dc])) for k,d in variant_pairs for c,dc in cols.items() if abs(float(k[c])-float(d[dc]))>1e-9]
out=dict(spelling_variants_resolved_by_surname={n:d for n,d in by_initial.items() if d},
         kit_only_rows=[n for n,d in by_initial.items() if not d],variant_line_differences=len(vdiffs),variant_first_differences=vdiffs[:10],
         kit_rows=len(kit),deck_rows=len(deck),alias_entries=len(AL),joined=len(pairs),how=how,unmatched=unmatched,line_differences=len(diffs),first_differences=diffs[:10])
json.dump(dict(out,engine_commit=__import__("subprocess").check_output(["git","-C",DECK,"rev-parse","--short","HEAD"]).decode().strip()),open(os.path.join(H,"rt_join.json"),"w"),indent=1); print(json.dumps(out,indent=1))
