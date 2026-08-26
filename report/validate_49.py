#!/usr/bin/env python3
"""draft_state_49 validation vs the Yahoo recap + post-draft roster analysis.

Ground truth: the Yahoo round-by-round recap the owner pasted (transcribed
below, mojibake restored to proper accents). The state file is the system's
record. Every comparison in the report comes from THIS script's output.
"""
import json, sys, os
sys.path.insert(0, "/home/user/yahoo-fantasy-basketball/scripts")
import hoops

STATE = "/root/.claude/uploads/3cdbbd9b-02dd-585e-8d00-b8a370128fae/90017b8c-draft_state_49.json"

SEATS = {1: "Brandon", 2: "Ethan", 3: "Team 3", 4: "Andy", 5: "Scott", 6: "??",
         7: "Chase", 8: "David", 9: "Yizan", 10: "John", 11: "Jay C.", 12: "Peter"}

# Yahoo recap, rounds in printed order (round-local pick 1..12). Names converted
# "Last, First" -> "First Last"; mojibake restored (Joki?->Jokić etc.).
RECAP = [
 ["Nikola Jokić","Victor Wembanyama","Luka Dončić","Shai Gilgeous-Alexander",
  "Giannis Antetokounmpo","Cooper Flagg","Cade Cunningham","Karl-Anthony Towns",
  "Tyrese Maxey","Anthony Edwards","Jayson Tatum","Jalen Johnson"],
 ["Donovan Mitchell","Tyrese Haliburton","Kevin Durant","Stephen Curry",
  "Anthony Davis","Scottie Barnes","Alperen Şengün","LaMelo Ball",
  "Austin Reaves","Jamal Murray","Jalen Brunson","Trey Murphy III"],
 ["Kawhi Leonard","Trae Young","Chet Holmgren","Evan Mobley","Paolo Banchero",
  "Rudy Gobert","Walker Kessler","Kyrie Irving","Derrick White","Pascal Siakam",
  "Josh Giddey","Jalen Duren"],
 ["Amen Thompson","Devin Booker","Darius Garland","Lauri Markkanen",
  "Jalen Williams","Domantas Sabonis","Isaiah Collier","Jaylen Brown",
  "Kon Knueppel","James Harden","Deni Avdija","Brandon Miller"],
 ["Alex Sarr","Bam Adebayo","Donovan Clingan","Onyeka Okongwu","LeBron James",
  "Keyonte George","Joel Embiid","Jaren Jackson Jr.","Dejounte Murray",
  "Franz Wagner","Desmond Bane","Nickeil Alexander-Walker"],
 ["Tyler Herro","OG Anunoby","Michael Porter Jr.","Cameron Boozer",
  "Dyson Daniels","Naz Reid","Zach Edey","Stephon Castle","Matas Buzelis",
  "Julius Randle","Ivica Zubac","Kel'el Ware"],
 ["Ryan Rollins","Jaden McDaniels","Damian Lillard","Coby White",
  "Zion Williamson","VJ Edgecombe","Mikal Bridges","Payton Pritchard",
  "Day'Ron Sharpe","Jalen Green","Paul George","Jarrett Allen"],
 ["Brandon Ingram","Dylan Harper","CJ McCollum","Caleb Wilson","Reed Sheppard",
  "De'Aaron Fox","AJ Dybantsa","Ja Morant","Neemias Queta","Norman Powell",
  "Ty Jerome","Miles Bridges"],
 ["Immanuel Quickley","Isaiah Hartenstein","Ausar Thompson","Cedric Coward",
  "Myles Turner","Darryn Peterson","Derik Queen","Jakob Poeltl",
  "Kristaps Porziņģis","Zach LaVine","Mark Williams","Josh Hart"],
 ["Nic Claxton","Wendell Carter Jr.","Fred VanVleet","Jaime Jaquez Jr.",
  "Cameron Johnson","Ayo Dosunmu","Kyshawn George","Andrew Wiggins",
  "John Collins","Jabari Smith Jr.","Darius Acuff Jr.","Cason Wallace"],
 ["Jalen Suggs","Brandin Podziemski","Kevin Porter Jr.","Moussa Diabaté",
  "DeMar DeRozan","Sandro Mamukelashvili","Peyton Watson","Brook Lopez",
  "Yaxel Lendeborg","Aaron Gordon","Jusuf Nurkić","Keegan Murray"],
 ["Toumani Camara","RJ Barrett","Devin Vassell","Jimmy Butler III",
  "Christian Braun","Saddiq Bey","Maxime Raynaud","Anthony Black",
  "Quentin Grimes","Collin Murray-Boyles","Andrew Nembhard","Davion Mitchell"],
 ["Egor Dëmin","Collin Gillespie","Jrue Holiday","Tim Hardaway Jr.",
  "Klay Thompson","Daniel Gafford","Paul Reed","Tari Eason","Isaiah Stewart",
  "Kyle Kuzma","Ajay Mitchell","PJ Washington"],
]

players = hoops.zscores(hoops.load_players())
state = json.load(open(STATE))
assert (state["teams"], state["slot"], state["size"]) == (12, 8, 13)

# ---- 1. canonicalize every recap name through the ACTUAL resolver ----------
canon, resolver_notes = [], []
for r, rd in enumerate(RECAP, 1):
    for k, nm in enumerate(rd, 1):
        overall = (r - 1) * 12 + k
        seat = k if r % 2 == 1 else 13 - k
        subs = hoops.match_candidates(players, nm)
        if len(subs) == 1:
            canon.append((overall, seat, nm, subs[0]["player"], "resolved"))
        elif len(subs) == 0:
            canon.append((overall, seat, nm, None, "NO-MATCH"))
            resolver_notes.append((overall, nm, "no match in pool"))
        else:
            names = [p["player"] for p in subs]
            canon.append((overall, seat, nm, None, f"AMBIG:{names}"))
            resolver_notes.append((overall, nm, f"ambiguous: {names}"))

print("== A. Yahoo-name -> pool resolver pass (156 recap names) ==")
n_res = sum(1 for c in canon if c[4] == "resolved")
print(f"resolved 1:1 : {n_res}/156")
for o, nm, why in resolver_notes:
    print(f"  pick {o:>3}  {nm!r:<26} {why}")

# ---- 2. state-vs-recap pick-by-pick validation ------------------------------
print("\n== B. draft_state_49 vs Yahoo recap, all 156 picks ==")
mism, unk = [], []
for (overall, seat, yname, cname, status), pk in zip(canon, state["picks"]):
    st_name, st_slot = pk["player"], pk["slot"]
    if st_slot != seat:
        mism.append((overall, f"SEAT: state {st_slot} vs snake {seat}"))
    if st_name.startswith("UNKNOWN"):
        unk.append((overall, seat, yname))
    elif cname is not None and st_name != cname:
        mism.append((overall, f"NAME: state {st_name!r} vs recap {cname!r}"))
    elif cname is None and status == "NO-MATCH":
        pass  # pool-missing player; state can't have matched either
exact = 156 - len(unk) - len([m for m in mism if m[1].startswith("NAME")])
print(f"picks compared        : 156")
print(f"name matches          : {exact}")
print(f"UNKNOWN in state      : {len(unk)}")
for o, s, y in unk:
    print(f"  pick {o:>3} (seat {s} {SEATS[s]}): recap says {y!r}")
print(f"seat/name mismatches  : {len(mism)}")
for o, m in mism:
    print(f"  pick {o:>3}: {m}")

# ---- 3. ground-truth rosters + z analysis ----------------------------------
# Rosters from the RECAP (truth), pool players only; note who drops out.
print("\n== C. roster z-analysis (ground truth = recap; pool players only) ==")
byname = {p["player"]: p for p in players}
rosters = {s: [] for s in SEATS}
missing = []
for overall, seat, yname, cname, status in canon:
    if cname:
        rosters[seat].append(byname[cname])
    else:
        missing.append((seat, yname))
print("players excluded from totals (not in pool):",
      ", ".join(f"{n} (seat {s} {SEATS[s]})" for s, n in missing) or "none")

CATS = hoops.CATS
totals = {s: {c: sum(p["z"][c] for p in ros) for c in CATS}
          for s, ros in rosters.items()}
comp = {s: sum(t.values()) for s, t in totals.items()}
comp_no_ast = {s: sum(v for c, v in t.items() if c != "AST")
               for s, t in totals.items()}

print("\n9-cat composite (sum of category z-totals), ranked:")
for rk, (s, v) in enumerate(sorted(comp.items(), key=lambda kv: -kv[1]), 1):
    tag = "  <-- DAVID" if s == 8 else ""
    print(f"  {rk:>2}. seat {s:<2} {SEATS[s]:<8} {v:+7.2f}{tag}")

print("\npunt-AST composite (8 cats, AST removed for ALL teams), ranked:")
for rk, (s, v) in enumerate(sorted(comp_no_ast.items(), key=lambda kv: -kv[1]), 1):
    tag = "  <-- DAVID" if s == 8 else ""
    print(f"  {rk:>2}. seat {s:<2} {SEATS[s]:<8} {v:+7.2f}{tag}")

print("\nDavid's category ranks (of 12):")
for c in CATS:
    order = sorted(SEATS, key=lambda s: -totals[s][c])
    rk = order.index(8) + 1
    print(f"  {c:<5} total {totals[8][c]:+6.2f}  rank {rk:>2}"
          + ("   (declared punt)" if c == "AST" else ""))

print("\nH2H: categories David leads vs each opponent (of 9 / of 8 ex-AST):")
for s in SEATS:
    if s == 8: continue
    w9 = sum(1 for c in CATS if totals[8][c] > totals[s][c])
    w8 = sum(1 for c in CATS if c != "AST" and totals[8][c] > totals[s][c])
    print(f"  vs seat {s:<2} {SEATS[s]:<8} {w9}/9   {w8}/8")

# ---- 4. value / reach for David's picks ------------------------------------
print("\n== D. David's picks vs board rank (composite adj_value order) ==")
board = sorted((p for p in players if hoops.availability(p) > 0),
               key=lambda p: -hoops.adj_value(p))
brank = {p["player"]: i + 1 for i, p in enumerate(board)}
for overall, seat, yname, cname, status in canon:
    if seat != 8 or not cname: continue
    br = brank.get(cname)
    rnd = (overall - 1) // 12 + 1
    if br is None:
        flag = "(unranked: availability 0)"
    elif br < overall - 15: flag = f"VALUE (+{overall - br})"
    elif br > overall + 8:  flag = f"reach (-{br - overall})"
    else: flag = "fair"
    print(f"  R{rnd:>2} pick {overall:>3}: {cname:<26} board #{br}  {flag}")
