"""Independent re-derivation of the deck's z-scores / value / availability / market
price from data/players.csv, written from the documented method (hoops.zscores
docstring + adj_value + availability + market_prices header), NOT by calling hoops.
Compares against (a) the PLAYERS array baked into docs/draft-deck.html and (b) hoops.py.
"""
import csv, json, math, re, sys, unicodedata, glob, os
DECK = "/home/user/yahoo-fantasy-basketball"
KIT = "/home/user/fantasy-basketball-2026-27"
CATS = ["FG%","FT%","3PTM","PTS","REB","AST","ST","BLK","TO"]
COL = {"3PTM":"tpm","PTS":"pts","REB":"reb","AST":"ast","ST":"stl","BLK":"blk","TO":"tov"}
rows = list(csv.DictReader(open(f"{DECK}/data/players.csv", encoding="utf-8")))
for r in rows:
    for k in ("fg_pct","fga","ft_pct","fta","tpm","pts","reb","ast","stl","blk","tov"):
        r[k] = float(r[k])
def tag(note): return re.split(r"[\s(]", (note or "").lower(), 1)[0]
def avail(r):
    t = tag(r["note"])
    if t.startswith("out-") or t.endswith("-recovery"): return 0.0
    if t.endswith("-risk") or t in ("risk","inj-risk"): return 0.78
    if "recovery" in t: return 0.0
    if "risk" in t: return 0.78
    return 1.0
def params(pool):
    n = len(pool)
    lg_fg = sum(p["fg_pct"]*p["fga"] for p in pool)/(sum(p["fga"] for p in pool) or 1)
    lg_ft = sum(p["ft_pct"]*p["fta"] for p in pool)/(sum(p["fta"] for p in pool) or 1)
    series = {"FG%":[(p["fg_pct"]-lg_fg)*p["fga"] for p in pool],
              "FT%":[(p["ft_pct"]-lg_ft)*p["fta"] for p in pool]}
    for c,col in COL.items(): series[c] = [p[col] for p in pool]
    prm = {}
    for c,v in series.items():
        m = sum(v)/n; s = math.sqrt(sum((x-m)**2 for x in v)/n) or 1.0
        prm[c] = (m,s)
    return lg_fg, lg_ft, prm
def apply(lg_fg, lg_ft, prm):
    for p in rows:
        vals = {"FG%":(p["fg_pct"]-lg_fg)*p["fga"], "FT%":(p["ft_pct"]-lg_ft)*p["fta"]}
        for c,col in COL.items(): vals[c] = p[col]
        p["z"] = {}
        for c,v in vals.items():
            m,s = prm[c]; z=(v-m)/s
            p["z"][c] = -z if c=="TO" else z
def tv(p): return sum(p["z"].values())
apply(*params(rows))
seen=set(); iters=0
for _ in range(5):
    top = sorted([p for p in rows if avail(p)>0], key=lambda p:-tv(p))[:156]
    key = frozenset(p["player"] for p in top)
    if key in seen: break
    seen.add(key); apply(*params(top)); iters+=1
def adj(p):
    t=tv(p); a=avail(p); return t*a if t>0 else t
# market price: newest kit yahoo file, ADP else XRank
yf = sorted(glob.glob(f"{KIT}/report/market/yahoo-????-??-??.csv"))[-1]
def norm(n):
    s = unicodedata.normalize("NFKD", n).encode("ascii","ignore").decode().lower()
    s = re.sub(r"[^a-z0-9 ]"," ",s)
    return " ".join(t for t in s.split() if t not in {"jr","sr","ii","iii","iv"})
price = {}
for y in csv.DictReader(open(yf, encoding="utf-8")):
    adp = y.get("adp"); xr = y.get("xrank")
    v = None
    try:
        if adp not in (None,"","-"): v = float(adp)
        elif xr not in (None,"","-"): v = float(xr)
    except ValueError: v=None
    price[norm(y["player"])] = v
# baked deck
html = open(f"{DECK}/docs/draft-deck.html", encoding="utf-8").read()
baked = json.loads(re.search(r"const PLAYERS = (\[.*?\]);", html, re.S).group(1))
bk = {p["n"]:p for p in baked}
sys.path.insert(0, f"{DECK}/scripts"); import hoops
hp = {p["player"]:p for p in hoops.zscores(hoops.load_players())}
out = {"csv_rows":len(rows), "baked_rows":len(baked), "fixed_point_iters":iters, "yahoo_file":os.path.basename(yf)}
maxdz_baked=0; maxdz_hoops=0; maxdv=0; av_mismatch=[]; raw_mismatch=[]; mkt_mismatch=[]; missing=[]
for p in rows:
    b = bk.get(p["player"])
    if b is None: missing.append(p["player"]); continue
    for c in CATS:
        maxdz_baked = max(maxdz_baked, abs(p["z"][c]-b["z"][c]))
        maxdz_hoops = max(maxdz_hoops, abs(p["z"][c]-hp[p["player"]]["z"][c]))
    maxdv = max(maxdv, abs(adj(p) - hoops.adj_value(hp[p["player"]])))
    if abs(avail(p)-b["av"])>1e-12: av_mismatch.append((p["player"],avail(p),b["av"]))
    rawcols = ["tpm","pts","reb","ast","stl","blk","tov","fg_pct","fga","ft_pct","fta"]  # build_deck RAW_COLS order
    if any(abs(round(p[c],4)-b["r"][i])>1e-9 for i,c in enumerate(rawcols[:len(b["r"])])): raw_mismatch.append(p["player"])
    if b.get("t")!=p["team"] or b.get("p")!=p["pos"] or (b.get("note") or "")!=(p["note"] or ""): raw_mismatch.append(p["player"]+"(meta)")
    pr = price.get(norm(p["player"]))
    if (pr is None) != (b.get("mkt") is None) or (pr is not None and abs(pr-b["mkt"])>1e-9): mkt_mismatch.append((p["player"],pr,b.get("mkt")))
out.update({"max_abs_dz_vs_baked":maxdz_baked, "max_abs_dz_vs_hoops":maxdz_hoops, "max_abs_dvalue_vs_hoops":maxdv,
            "av_mismatches":av_mismatch, "raw_or_meta_mismatches":raw_mismatch, "mkt_mismatches":mkt_mismatch[:20], "mkt_mismatch_count":len(mkt_mismatch), "missing_from_deck":missing,
            "priced_rows_mine":sum(1 for p in rows if price.get(norm(p["player"])) is not None), "priced_rows_baked":sum(1 for b in baked if b.get("mkt") is not None),
            "top10_mine":[p["player"] for p in sorted(rows,key=lambda p:-adj(p))[:10]],
            "top10_hoops":[p["player"] for p in sorted(hp.values(),key=lambda p:-hoops.adj_value(p))[:10]],
            "top10_baked_by_val":[b["n"] for b in sorted(baked,key=lambda b:-(sum(b["z"].values())*b["av"] if sum(b["z"].values())>0 else sum(b["z"].values())))[:10]]})
print(json.dumps(out, indent=1, ensure_ascii=False))
