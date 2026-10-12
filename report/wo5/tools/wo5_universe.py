"""P3 universe + P5 candidates. Ranks: deck value (hoops zscores, adj_value, availability > 0) on the current pool and on the
pool with every default method line swapped in; kit board (rank_engine passes) on the current kit pool. Universe = union of the
three top-150s plus the WO-5 queue names. Candidates for role research inside the universe:
  T  team changed since the base season (bref team vs current team; a 2TM/3TM base counts as changed)
  S  starting role changed: base-season starts share vs preseason starts share differ by 0.5 or more (preseason >= 2 games)
  Q  named in the WO-5 queue for role
Preseason minutes and production are never used: role only (owner, 2026-10-12)."""
import sys, os, csv, json, copy, re, unicodedata
DECK = "/home/user/yahoo-fantasy-basketball"; KIT = "/home/user/fantasy-basketball-2026-27/report"
S = sys.argv[1]
sys.path.insert(0, DECK + "/scripts"); sys.path.insert(0, KIT)
import hoops
import rank_engine as RE
dl = json.load(open(S + "/default_lines.json")); pre = json.load(open(S + "/preseason_roles.json"))
norm = lambda s: " ".join(t for t in re.sub(r"[^a-z0-9 ]", " ", re.sub(r"[.'`,’-]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower())).split() if t not in {"jr", "sr", "ii", "iii", "iv"})
ALI = {"herb jones": "herbert jones", "cam johnson": "cameron johnson", "nic claxton": "nicolas claxton", "alex sarr": "alexandre sarr", "ron holland": "ronald holland"}
nk = lambda s: ALI.get(norm(s), norm(s))
def deck_rank(players):
    P = hoops.zscores(players); P = [p for p in P if hoops.availability(p) > 0]
    P.sort(key=lambda p: -hoops.adj_value(p, ())); return {nk(p["player"]): i + 1 for i, p in enumerate(P)}
hoops.DATA_PATH = DECK + "/data/players.csv"; raw = hoops.load_players()
cur_deck = deck_rank(copy.deepcopy(raw))
new = copy.deepcopy(raw); byk = {r["key"]: r for r in dl["rows"]}
for p in new:
    r = byk.get(nk(p["player"]))
    if r and r.get("new"):
        for c, v in r["new"].items(): p[c] = v
new_deck = deck_rank(new)
rows = RE.load(os.path.join(KIT, "projections-2026-27.csv")); rows, held = RE.exclude_held(rows)
z1 = RE.zscores(rows, rows); pool = sorted(rows, key=lambda r: -RE.total(z1[r["name"]]))[:RE.POOL_SIZE]; z2 = RE.zscores(rows, pool)
for r in rows:
    t = RE.total(z2[r["name"]]); av = RE.avail(r["gp"]); r["z_adj"] = t * av if t > 0 else t
kit_rank = {nk(r["name"]): i + 1 for i, r in enumerate(sorted(rows, key=lambda r: -r["z_adj"]))}
QUEUE = ["Cooper Flagg", "PJ Washington", "Daniel Gafford", "Devin Vassell", "Herbert Jones", "Isaiah Jackson", "Rui Hachimura", "Brook Lopez",
         "Morez Johnson Jr.", "Khaman Maluach", "Oso Ighodaro", "DeMar DeRozan", "Aday Mara", "Jaylin Williams", "Stephon Castle", "Dyson Daniels"]
qk = {nk(q) for q in QUEUE}
U = {k for k, v in cur_deck.items() if v <= 150} | {k for k, v in new_deck.items() if v <= 150} | {k for k, v in kit_rank.items() if v <= 150} | qk
pre_by = {}
for p in pre["players"]: pre_by.setdefault(nk(p["name"]), []).append(p)
CANON = {"BRK": "BKN", "BKN": "BKN", "PHO": "PHX", "PHX": "PHX", "CHO": "CHA", "CHA": "CHA", "GS": "GSW", "GSW": "GSW", "NO": "NOP", "NOP": "NOP",
         "SA": "SAS", "SAS": "SAS", "NY": "NYK", "NYK": "NYK", "UTAH": "UTA", "UTA": "UTA", "WSH": "WAS", "WAS": "WAS"}
canon = lambda t: CANON.get(t, t) if t else t
out = []
for k in sorted(U):
    r = byk.get(k); name = r["name"] if r else k
    team = canon(r["team"]) if r else None
    m = (r or {}).get("meta") or {}
    bt = m.get("base_team"); bt2 = canon(bt) if bt else None
    flags = []
    if bt and (bt.endswith("TM") or bt2 != team): flags.append("T")
    pr = pre_by.get(k, [])
    pgp = sum(p["gp"] for p in pr); pst = sum(p["starts"] for p in pr); pdnp = sum(p["dnp"] for p in pr)
    bshare = (m["base_gs"] / m["base_g"]) if m.get("base_g") else None; pshare = (pst / pgp) if pgp else None
    if bshare is not None and pshare is not None and pgp >= 2 and abs(bshare - pshare) >= 0.5: flags.append("S")
    if k in qk: flags.append("Q")
    out.append(dict(name=name, key=k, team=team, base_team=bt, cur_deck=cur_deck.get(k), new_deck=new_deck.get(k), kit=kit_rank.get(k),
                    base=m.get("base"), base_g=m.get("base_g"), base_gs=m.get("base_gs"), base_mpg=m.get("base_mpg"),
                    pre_gp=pgp, pre_starts=pst, pre_dnp=pdnp, pre_teams=sorted({canon(t) for p in pr for t in p["teams"]}),
                    has_line=bool(r and r.get("new")), flags=flags))
json.dump(dict(universe=out), open(S + "/universe.json", "w"), indent=1)
c = [x for x in out if x["flags"] and x["flags"] != ["Q"] or "Q" in x["flags"]]
print(f"universe {len(out)}; with a method line {sum(1 for x in out if x['has_line'])}; candidates {len(c)} (T {sum(1 for x in out if 'T' in x['flags'])}, S {sum(1 for x in out if 'S' in x['flags'])}, Q {sum(1 for x in out if 'Q' in x['flags'])})")
for x in sorted(c, key=lambda x: (x["new_deck"] or 999)):
    print(f"{x['name']:26} {x['team']:5} base {x['base']} {x['base_team']} G{x['base_g']} GS{x['base_gs']} {x['base_mpg']}m | pre {x['pre_gp']}g {x['pre_starts']}st dnp{x['pre_dnp']} {x['pre_teams']} | ranks deck {x['cur_deck']}->{x['new_deck']} kit {x['kit']} | {''.join(x['flags'])}")
