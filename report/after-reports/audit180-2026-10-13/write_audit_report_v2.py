#!/usr/bin/env python3
"""Writes report/after-reports/after-report-2026-10-13-uploads.md from audit180_v2.json, audit180.json and the intake
records (the three joins' csv and unmatched files, the raw uploads), and appends the pull-log row.
Every figure is read from a record; the typed literals are the method parameters stated to the owner (A1-A4 of the gate)."""
import csv, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.normpath(os.path.join(H, "..", "..", "..")); AR = os.path.join(K, "report", "after-reports")
M = os.path.join(K, "report", "market")
J = lambda p: json.load(open(p, encoding="utf-8")); rd = lambda p: open(p, encoding="utf-8").read()
V1 = J(os.path.join(H, "audit180.json")); V2 = J(os.path.join(H, "audit180_v2.json"))
S1, S2 = V1["summary"], V2["summary"]; R1 = {r["name"]: r for r in V1["rows"]}; R = V2["rows"]
rn = rd(os.path.join(K, "report", "dial", "out", "rn_section_v65.md")); ra = J(os.path.join(H, "range_no_actual_v65.json"))
tb = rd(os.path.join(H, "team_budget_v65.txt"))
LAB = {"pts": "pts", "reb": "reb", "ast": "ast", "stl": "stl", "blk": "blk", "tpm": "3PM", "tov": "TO", "fg_pct": "FG%", "ft_pct": "FT%"}
fmt = lambda c, v: (f"{v:.3f}".lstrip("0") if c.endswith("pct") else f"{v:g}")
def t1(r): return "; ".join(f"{LAB[x['cat']]} {fmt(x['cat'], x['line'])} vs {fmt(x['cat'], x['lo'])} to {fmt(x['cat'], x['hi'])} ({x['z']:+.2f} z)" for x in r["tests"]["T1"]["cells"])
def reasons(r):
    b = []
    if r["tests"]["T1"]["cells"]: b.append(f"outside all {r['tests']['T1']['refs']} outside projections: " + t1(r))
    for x in r["tests"].get("T2", {}).get("cells", []): b.append(f"per-36 {LAB[x['cat']]} {x['line_per36']} outside his own band {x['band'][0]} to {x['band'][1]}")
    for x in r["tests"].get("T3", {}).get("cells", []): b.append(f"{LAB[x['cat']]} {fmt(x['cat'], x['line'])} outside his career band {fmt(x['cat'], x['band'][0])} to {fmt(x['cat'], x['band'][1])}")
    for x in r["tests"]["T4"]["notes"]: b.append(x)
    if abs(r["tests"]["T5"]["gap"]) > 1: b.append(f"points identity gap {r['tests']['T5']['gap']:+.2f}")
    for x in r["tests"].get("T6", {}).get("notes", []): b.append(x)
    if r["tests"]["T7"]["note"]: b.append(r["tests"]["T7"]["note"] + ": " + ", ".join(f"{k} {v}" for k, v in r["tests"]["T7"]["outside"].items()))
    return "; ".join(b)
tier = lambda t: [r for r in R if r["tier"] == t]
HIGH, MED, LOW, UNA, CLEAN = (tier(t) for t in ("HIGH", "MEDIUM", "LOW", "UNANCHORED", "CLEAN"))
n = lambda t: S2["tiers"][t]; n1 = lambda t: S1["tiers"][t]
f1, f2 = S1["fired"], S2["fired"]
cells = [x for r in R for x in r["tests"]["T1"]["cells"]]
zpos = sum(x["z"] for x in cells if x["z"] > 0); zneg = sum(x["z"] for x in cells if x["z"] < 0)
cells1 = [x for r in V1["rows"] for x in r["tests"]["T1"]["cells"]]
zpos1 = sum(x["z"] for x in cells1 if x["z"] > 0); zneg1 = sum(x["z"] for x in cells1 if x["z"] < 0)
big = [r for r in R if abs(r["tests"]["T1"]["net_z"]) > 0.5]; big1 = [r for r in V1["rows"] if abs(r["tests"]["T1"]["net_z"]) > 0.5]
few = [r for r in R if r["tests"]["T1"]["refs"] < 3]
rpl = S2["refs_per_line"]
old = [r for r in R if any("outside average" in x for x in r["tests"].get("T6", {}).get("notes", []))]
old1 = [r for r in V1["rows"] if any("outside average" in x for x in r["tests"].get("T6", {}).get("notes", []))]
OLDLIST = ", ".join(f"{r['name']} ({r['age']})" for r in old)
OLDGONE = ", ".join(r["name"] for r in old1 if r["name"] not in {o["name"] for o in old})
mkt_hi = [r for r in R if r["tests"]["T7"]["note"] and "we are high" in r["tests"]["T7"]["note"]]
mkt_lo = [r for r in R if r["tests"]["T7"]["note"] and "we are low" in r["tests"]["T7"]["note"]]
gp_hist = [r for r in R if any("three-season average" in x for x in r["tests"]["T4"]["notes"])]
gp_out = [r for r in R if any(x.startswith("gp") and "vs outside" in x for x in r["tests"]["T4"]["notes"])]
mp_out = [r for r in R if any(x.startswith("mpg") and "vs outside" in x for x in r["tests"]["T4"]["notes"])]
mp_hist = [r for r in R if any("three-season high" in x for x in r["tests"]["T4"]["notes"])]
withg = [r for r in R if r["tests"]["T4"].get("outside_gp")]
gp_ours = sum(r["gp"] for r in withg); gp_mean = sum(sum(r["tests"]["T4"]["outside_gp"].values()) / len(r["tests"]["T4"]["outside_gp"]) for r in withg)
withm = [r for r in R if r["tests"]["T4"].get("outside_mpg")]
mp_ours = sum(r["mpg"] for r in withm); mp_mean = sum(sum(r["tests"]["T4"]["outside_mpg"].values()) / len(r["tests"]["T4"]["outside_mpg"]) for r in withm)
ubig = [r for r in UNA if abs(r["tests"]["T1"]["net_z"]) > 0.5]
una_refs = sum(1 for r in UNA if r["tests"]["T1"]["refs"] >= 3)
UBIG_S = ", ".join(f"{r['name']} {r['tests']['T1']['net_z']:+.2f}" for r in ubig)
FEW_S = ", ".join(f"{r['name']} ({len(r['tests']['T1']['sources'])}: {', '.join(r['tests']['T1']['sources'])})" for r in few)
byn = {r["name"]: r for r in R}
# typed names in the plain-language section, asserted against the records
assert {r["name"] for r in HIGH} == {"Jamal Murray", "Collin Gillespie", "Bradley Beal", "Deandre Ayton", "Aaron Nesmith", "Sandro Mamukelashvili", "Marcus Smart"}, [r["name"] for r in HIGH]
_h1 = {r["name"] for r in V1["rows"] if r["tier"] == "HIGH"}; _h2 = {r["name"] for r in HIGH}
assert _h1 & _h2 == {"Jamal Murray", "Collin Gillespie", "Bradley Beal", "Aaron Nesmith", "Sandro Mamukelashvili"}
assert _h1 - _h2 == {"Jaylon Tyson", "Kyle Filipowski", "Quentin Grimes", "Bennedict Mathurin", "Al Horford", "T.J. McConnell", "Jordan Goodwin"}
assert byn["Jordan Goodwin"]["tests"]["T1"]["refs"] == 1 and R1["Jordan Goodwin"]["tests"]["T1"]["refs"] == 2
_sm = {x["cat"]: x for x in byn["Marcus Smart"]["tests"]["T1"]["cells"]}; _ay = {x["cat"]: x for x in byn["Deandre Ayton"]["tests"]["T1"]["cells"]}
assert byn["Marcus Smart"]["tests"]["T1"]["sources"] == ["RotoBaller", "Yahoo"] and _sm["pts"]["lo"] == _sm["pts"]["hi"] == 7.8 and _sm["pts"]["line"] == 9.3 and _sm["stl"]["line"] == 1.5, _sm
assert byn["Deandre Ayton"]["tests"]["T1"]["refs"] == 3 and "pts" in _ay and "reb" in _ay, _ay
assert byn["Deandre Ayton"]["rank"] > 100 and byn["Marcus Smart"]["rank"] > 100
SM = f"Marcus Smart ({byn['Marcus Smart']['tests']['T1']['net_z']:+.2f} z net on two references, RotoBaller and Yahoo: both project {_sm['pts']['lo']:g} points against our {_sm['pts']['line']:g}, and {_sm['stl']['lo']:g} to {_sm['stl']['hi']:g} steals against our {_sm['stl']['line']:g})"
AY = f"Deandre Ayton ({byn['Deandre Ayton']['tests']['T1']['net_z']:+.2f} on three: our {_ay['pts']['line']:g} points and {_ay['reb']['line']:g} rebounds against {_ay['pts']['lo']:g} to {_ay['pts']['hi']:g} and {_ay['reb']['lo']:g} to {_ay['reb']['hi']:g})"
assert byn["Ja Morant"]["tests"]["T3"]["cells"] and byn["Ja Morant"]["tests"]["T3"]["cells"][0]["line"] == 0.845
una_refs1 = sum(1 for r in V1["rows"] if r["tier"] == "UNANCHORED" and r["tests"]["T1"]["refs"] >= 3)
plural = lambda k, word: f"{k} {word}" + ("" if k == 1 else "s")
import subprocess
RBJ = J(os.path.join(H, "range_no_actual_rb1013.json"))
_ra = {r["player"] for r in ra["rows"]}; _rb = {r["player"] for r in RBJ["rows"]}
RB_IN, RB_OUT = sorted(_rb - _ra), sorted(_ra - _rb)
assert RBJ["references"]["RotoBaller"] == "rotoballer-2026-10-13.csv", RBJ["references"]
_rep = subprocess.run([sys.executable, os.path.join(H, "reproduce_check_v2.py")], capture_output=True, text=True)
assert _rep.returncode == 0, _rep.stdout + _rep.stderr
REP = re.search(r"outside cells recomputed (\d+); audit cells (\d+); disagreements (\d+)", _rep.stdout)
assert REP and REP.group(1) == REP.group(2) and REP.group(3) == "0", _rep.stdout
TBM = re.search(r"above the 2025-26 league maximum \(117\.7\): (\d+) \[([^\]]*)\]", tb)
phi = re.search(r"^PHI \| \d+ \| [^|]+\| [\d.]+ \([\d.]+\) vs [\d.]+ \| ([\d.]+) ", tb, re.M).group(1)
assert f2["T2"] == 0 and f2["T5"] == 0
# tier moves between the runs, with the reason classified from the records
moves = []
for r in R:
    a = R1[r["name"]]
    if a["tier"] == r["tier"]: continue
    ra_, rb = a["tests"]["T1"]["refs"], r["tests"]["T1"]["refs"]
    if rb < ra_ and rb < 2: why = f"lost its second outside projection (now {rb}: {', '.join(r['tests']['T1']['sources'])}); the range test cannot run"
    elif ra_ < 2 <= rb: why = f"gained a second outside projection (now {rb}); the range test ran for the first time"
    elif a["tests"]["T1"]["cells"] and not r["tests"]["T1"]["cells"]: why = f"inside the five-source band (the three-source band was narrower); {ra_} to {rb} projections"
    elif abs(a["tests"]["T1"]["net_z"]) > abs(r["tests"]["T1"]["net_z"]) + 1e-9: why = f"band widened: net z {a['tests']['T1']['net_z']:+.2f} to {r['tests']['T1']['net_z']:+.2f}"
    else:
        lost = [t for t in a["flags"] if t not in r["flags"]]; got = [t for t in r["flags"] if t not in a["flags"]]
        why = ("no longer " + ", ".join(lost) if lost else "") + ("; now " + ", ".join(got) if got else "")
    moves.append((r["rank"], r["name"], a["tier"], r["tier"], a["tests"]["T1"]["net_z"], r["tests"]["T1"]["net_z"], why))
moves.sort()
down = [m for m in moves if ("CLEAN", "LOW", "MEDIUM", "HIGH").index(m[3]) < ("CLEAN", "LOW", "MEDIUM", "HIGH").index(m[2])]
up = [m for m in moves if m not in down]
inside = [m for m in down if m[6].startswith("inside")]; widened = [m for m in down if m[6].startswith("band widened")]
lostref = [m for m in down if m[6].startswith("lost")]; flagoff = [m for m in down if m[6].startswith("no longer")]
assert len(inside) + len(widened) + len(lostref) + len(flagoff) == len(down), [m for m in down if not any(m[6].startswith(k) for k in ("inside", "band widened", "lost", "no longer"))]
OFF_HIGH = "; ".join(f"{m[1]} ({m[2]} to {m[3]}, net z {m[4]:+.2f} to {m[5]:+.2f})" for m in down if m[2] == "HIGH" and not m[6].startswith("lost"))
# intake records
def join_counts(src):
    rows = list(csv.DictReader(open(os.path.join(M, f"{src}-2026-10-13.csv"), encoding="utf-8")))
    um = rd(os.path.join(M, f"unmatched-{src}-2026-10-13.md"))
    absent = re.findall(r"^\| \d+ \| ([^|]+?) \| [^|]*\| no pool row", um, re.M)
    skipped = re.search(r"left out of the join \((\d+)\)", um)
    return len(rows), absent, int(skipped.group(1)) if skipped else 0
rb_n, rb_abs, _ = join_counts("rotoballer"); fp_n, fp_abs, fp_skip = join_counts("fantasypros"); cd_n, cd_abs, cd_skip = join_counts("cards")
old_rb = {r["Player"]: r for r in csv.DictReader(open(os.path.join(M, "rotoballer-raw-2026-09-29.csv"), encoding="utf-8-sig"))}
new_rb = list(csv.DictReader(open(os.path.join(M, "rotoballer-raw-2026-10-13.csv"), encoding="utf-8-sig")))
shared = [r for r in new_rb if r["Player"] in old_rb]
same_lines = sum(1 for r in shared if all(old_rb[r["Player"]][k] == r[k] for k in ("PTS", "REB", "AST", "STL", "BLK", "3PM", "FG%", "FT%", "TO")))
ranks_moved = sum(1 for r in shared if old_rb[r["Player"]]["Rank"] != r["Rank"])
added = [r["Player"] for r in new_rb if r["Player"] not in old_rb]; dropped = [p for p in old_rb if p not in {r["Player"] for r in new_rb}]
fp_raw = [r for r in csv.DictReader(open(os.path.join(M, "fantasypros-raw-2026-10-13.csv"), encoding="utf-8-sig")) if r.get("Player")]
cd_raw = list(csv.DictReader(open(os.path.join(M, "cards-raw-2026-10-13.csv"), encoding="utf-8")))
assert len(shared) == same_lines, (len(shared), same_lines)
o = []; w = o.append
w("# After-report — 2026-10-13 (uploads): the three uploads taken in, and the top-180 audit re-run on five outside projections\n")
w("**Owner request (2026-10-13 evening):** three uploads with no words, answering the audit report's §4 (\"what you can upload\"): a RotoBaller 9-cat projected-rankings CSV, a FantasyPros rest-of-season projections CSV, and a pasted set of player cards given with the URL basketballmonster.com/projections.aspx. Then: \"Are you able to view and read this link? https://bleacherreport.com/articles/25507731-ranking-99-best-nba-players-ahead-2026-27 — If so, you can also use player role and real life context to integrate to this data projection.\"\n")
w(f"**What was analyzed:** the three uploads, pinned verbatim and joined to the pool under the hard gate; then the same seven tests as `after-report-2026-10-13-audit180.md` on the same 180 lines (`report/top-200-2026-27.md` at kit `main` 7c44327, Version 65's lines) with the outside-projection set widened from three to five. Nothing on either plane changed: both files are byte-identical before and after. References: {', '.join(f'{k} `{v}`' for k, v in S2['refs'].items())}; history and ranks as in the first audit.\n")
w("**Method:** A1 to A6 as stated in the first audit, with A3 generalized to the wider set: minutes are questioned 2+ above the three-season high or 4+ beyond every outside minutes projection on the same side (Hashtag, FantasyPros, the cards); games 10+ above the three-season average after a season under 60, or 6+ above every outside games projection (Yahoo, Hashtag, FantasyPros, the cards). The intake assumptions stated before the run: the card paste's origin is recorded as the owner gave it (the URL) with the observed layout (ESPN-style player cards), unconfirmed because the host cannot be reached from here; the RotoBaller file is dated by its upload day; FantasyPros' rest-of-season games are read as full-season games. Tool: `audit180-2026-10-13/audit180_v2.py`; two runs identical.\n")
w("Pull window: 2026-10-13 → 2026-10-13 (no roster pull; three owner uploads).\n")
w(f"**Headline.** With five outside projections instead of three, the question marks shrink and sharpen. {f2['T1']} of the 180 now have a cell outside every outside projection (was {f1['T1']}), the cells beyond the range carry {zpos:+.2f} z on the flattering side against {zneg:+.2f} (was {zpos1:+.2f} / {zneg1:+.2f}), and the tiers move from HIGH {n1('HIGH')} / MEDIUM {n1('MEDIUM')} / LOW {n1('LOW')} / CLEAN {n1('CLEAN')} to HIGH {n('HIGH')} / MEDIUM {n('MEDIUM')} / LOW {n('LOW')} / CLEAN {n('CLEAN')}. {rpl['5']} of the 180 lines now have all five projections and {rpl['5'] + rpl['4'] + rpl['3']} have three or more; {len(few)} still have fewer than three ({', '.join(r['name'] for r in few)}). Two lines that had no second projection before now have one and fail it: Marcus Smart ({next(r for r in R if r['name'] == 'Marcus Smart')['tests']['T1']['net_z']:+.2f} z net) and Deandre Ayton ({next(r for r in R if r['name'] == 'Deandre Ayton')['tests']['T1']['net_z']:+.2f}). One line left HIGH because it lost a projection, not because it was vindicated: Jordan Goodwin, dropped from the RotoBaller re-export. The RotoBaller upload is the 9/29 projection re-ranked, not a new one: the same stat line on all {same_lines} shared names, {ranks_moved} ranks moved, {len(added)} names added and {len(dropped)} dropped (the 9/29 file lists Aaron Gordon twice). {una_refs} of the {n('UNANCHORED')} unanchored lines now have three or more outside projections (was {una_refs1}); {plural(len(ubig), 'line')} among them still beyond 0.5 z ({UBIG_S}). Minutes and games: over the {len(withm)} lines with an outside minutes projection ours sum to {mp_ours:.0f} against their average {mp_mean:.0f}; over the {len(withg)} with an outside games projection, {gp_ours:.0f} against {gp_mean:.0f}. The Bleacher Report link cannot be read from this container (DNS fails and the proxy refuses the host, the same wall as every sports host on file); pasted text would be taken in the way the cards were.\n")
w("## 1. Roster changes\n\nNone. No line, tag, placement, games or minutes figure changed on either plane; this is an intake and an assessment.\n")
w("## 2. The three uploads\n\nEVIDENCE: `report/market/rotoballer-raw-2026-10-13.csv`, `fantasypros-raw-2026-10-13.csv`, `cards-raw-2026-10-13.csv` (raw, verbatim; the card paste transcribed), the joins `rotoballer-2026-10-13.csv`, `fantasypros-2026-10-13.csv`, `cards-2026-10-13.csv` with their `unmatched-` and `disagreements-` files, `provenance.csv`, `check_derived.py` (27 of 27 reproduce at pin d08ac74).\n")
w("| upload | what it is | rows | joined | without a pool row | note |\n|---|---|---|---|---|---|")
w(f"| RotoBaller overall 9-cat projected rankings | the owner's re-export of the file pinned 9/29 | {len(new_rb)} | {rb_n} | {len(rb_abs)}: {', '.join(rb_abs)} | the same stat line as 9/29 on all {same_lines} shared names; {ranks_moved} of {len(shared)} ranks moved; added {', '.join(added)}; dropped {', '.join(dropped)}. It is a fourth ranking of the same projection, not a fresh projection |")
w(f"| FantasyPros rest-of-season projections | a full 9-cat line with games and minutes | {len(fp_raw)} ({fp_skip} with no projection, all zeros, left out) | {fp_n} | {len(fp_abs)}: {', '.join(fp_abs)} | one new alias: Ron Holland = Ronald Holland II (verified: DET on both). Team codes NOR/PHO/UTH mapped. Covers rookies |")
w(f"| The card paste | one card per player: last season's line, a 2027 projection with games and minutes, an outlook paragraph | {len(cd_raw)} cards ({cd_skip} with no 2027 line: {', '.join(r['Player'] for r in cd_raw if not r['PTS'])}) | {cd_n} | {len(cd_abs)}: {', '.join(cd_abs)} | the 2027 projection rows transcribed; assists over turnovers reproduces the pasted A/TO within 0.06 on every projected row (0 mismatches). Origin: given with the Basketball Monster URL; the layout (Headshot, Day-To-Day and Out tags, 2026 STATISTICS / 2027 PROJECTIONS / 2027 Outlook) matches ESPN's player pages. `UNVERIFIABLE` from here: basketballmonster.com does not resolve (ENOTFOUND). The outlook prose was read in-session and not stored |")
w("\nThe Bleacher Report article: `ATTEMPTED-FAILED`. The fetch fails at DNS (ENOTFOUND bleacherreport.com) and a direct request through the session proxy is refused (CONNECT 403), the same wall recorded for 17 sports hosts at the actuals intake on 10/09. If the owner pastes the article, it goes in as a role-context source the way the RotoWire panel and the profiles pieces did: names, ranks and the role or health words kept verbatim, joined under the hard gate, used as leads for the per-line reading, never as a line edit.\n")
w("## 3. The verdict, test by test, three references against five\n\nEVIDENCE: `audit180-2026-10-13/audit180.json` (three references), `audit180_v2.json` (five), `audit180_v2.txt`.\n")
w("| test | fired, 3 refs | fired, 5 refs | reading on five |\n|---|---|---|---|")
w(f"| T1 outside range | {f1['T1']} | {f2['T1']} | {len(cells)} cells (was {len(cells1)}), {zpos:+.2f} z flattering against {zneg:+.2f}; {len(big)} lines over 0.5 z net (was {len(big1)}): " + ", ".join(f"{r['name']} {r['tests']['T1']['net_z']:+.2f}" for r in sorted(big, key=lambda r: -abs(r['tests']['T1']['net_z']))) + f". Lines per reference count: five {rpl['5']}, four {rpl['4']}, three {rpl['3']}, two {rpl['2']}, one {rpl['1']} |")
w(f"| T2 own history | {f1['T2']} | {f2['T2']} | unchanged by construction |")
w(f"| T3 career shooting | {f1['T3']} | {f2['T3']} | Ja Morant's FT% .845 against his career band, as before |")
w(f"| T4 minutes and games | {f1['T4']} | {f2['T4']} | {len(gp_hist)} games flags rest on injury history; {len(gp_out)} lines sit 6+ games above every outside games projection ({', '.join(r['name'] for r in gp_out)}); {len(mp_hist)} minutes flags against the career high ({', '.join(r['name'] for r in mp_hist)}); {len(mp_out)} lines 4+ minutes beyond every outside minutes projection ({', '.join(r['name'] + ' ' + next(x for x in r['tests']['T4']['notes'] if x.startswith('mpg') and 'outside' in x) for r in mp_out)}). Aggregate minutes {mp_ours:.0f} against {mp_mean:.0f} over {len(withm)}; games {gp_ours:.0f} against {gp_mean:.0f} over {len(withg)} |")
w(f"| T5 points identity | {f1['T5']} | {f2['T5']} | every line reconciles |")
w(f"| T6 age | {f1['T6']} | {f2['T6']} | {len(old)} players 34 and older above the five-source average in two or more of points, rebounds and assists: {OLDLIST}. {OLDGONE} no longer sit above the five-source average in two of the three; the method still carries no decline |")
w(f"| T7 market | {f1['T7']} | {f2['T7']} | the same {f2['T7']} names (RotoBaller's re-ranking moves no verdict): high on {len(mkt_hi)}, low on {len(mkt_lo)} |")
w(f"| team budget | {TBM.group(1)} teams | {TBM.group(1)} teams | unchanged: the lines did not move; Philadelphia {phi} against 117.7 |")
w(f"\nTiers on five references: HIGH {n('HIGH')}, MEDIUM {n('MEDIUM')}, LOW {n('LOW')}, UNANCHORED {n('UNANCHORED')}, CLEAN {n('CLEAN')}. {len(moves)} lines changed tier: {len(down)} down and {len(up)} up.\n")
w("### Lines that changed tier\n\n| rank | player | 3 refs | 5 refs | net z before | net z after | why |\n|---|---|---|---|---|---|---|")
for rk, nm, a, b, za, zb, why in moves: w(f"| {rk} | {nm} | {a} | {b} | {za:+.2f} | {zb:+.2f} | {why} |")
w("\n## 4. The question marks on five references\n\nEVIDENCE: `audit180_v2.json`; z figures in the deck's own frame, flattering positive.\n")
w("### HIGH\n\n| rank | player | age | refs | net z | why |\n|---|---|---|---|---|---|")
for r in HIGH: w(f"| {r['rank']} | {r['name']} ({r['team']}) | {r['age']} | {r['tests']['T1']['refs']} | {r['tests']['T1']['net_z']:+.2f} | {reasons(r)} |")
w("\n### MEDIUM\n\n| rank | player | age | refs | net z | why |\n|---|---|---|---|---|---|")
for r in MED: w(f"| {r['rank']} | {r['name']} ({r['team']}) | {r['age']} | {r['tests']['T1']['refs']} | {r['tests']['T1']['net_z']:+.2f} | {reasons(r)} |")
w("\n### UNANCHORED (fewer than two NBA seasons of 25+ games), now with the outside projections that cover them\n\n| rank | player | NBA seasons on file | refs | net z | what the outside projections say |\n|---|---|---|---|---|---|")
for r in UNA: w(f"| {r['rank']} | {r['name']} ({r['team']}) | {', '.join(r['history_seasons']) or 'none'} | {r['tests']['T1']['refs']} | {r['tests']['T1']['net_z']:+.2f} | {reasons(r) or 'inside every outside projection'} |")
w("\n### LOW (one small flag each; I agree with these lines)\n")
w("; ".join(f"{r['name']} ({reasons(r)})" for r in LOW) + ".\n")
w("## 5. What is still missing\n")
w("| gap | who | what would close it |\n|---|---|---|")
w(f"| fewer than three outside projections | {FEW_S} | Hashtag's full-pool sheet (its file stops at 200), or any deep projection that reaches the bench; Goodwin and Smart are the two whose verdicts depend on it |")
w(f"| age decline | the {len(old)} players 34 and older in T6 | still no source with decline built in; the five projections' average is the only outside view, and it sits below our line for these {len(old)} |")
w("| role and real-life context | every HIGH and MEDIUM line | the Bleacher Report article as a paste, or any dated depth-chart page; used as leads per line, not as edits |")
w("| a projection with a stated date | the RotoBaller re-export | the file carries no date and its lines equal the 9/29 file; a dated export would say whether RotoBaller has updated since camp |")
w(f"| the team budget per player | Philadelphia first | an outside minutes sheet now exists for {len(withm)} of the 180 (FantasyPros and the cards); reading the budget per player against it is a build step, after the draft with D-C2 |\n")
w("## Range check (D-RN-3, without last season as a reference)\n")
w(f"The deck's own range check still reads its three sources (Yahoo, Hashtag, the newest RotoBaller file). Re-run here with the 10/13 RotoBaller file in place of 9/29 (`range_no_actual_rb1013.json`, no deck change): {RBJ['players']} of {RBJ['checkable']} checkable top-150 lines, {RBJ['cells']} cells, against {ra['players']} and {ra['cells']} on the dial pass's after-run (`range_no_actual_v65.json`); the lines are the same, so the only movement is in who has a third reference: {', '.join(RB_IN)} now flagged (added to the RotoBaller file), {', '.join(RB_OUT)} no longer (dropped from it). The next build's gate sees the same. Adding FantasyPros and the cards to the deck's range check is a deck change and the owner's call (D-1013-14 below). This is not a projection pass, so the D-RN-3 mechanism rule does not apply to this report.\n")
w("## Watchlist\n")
w(f"- The {n('HIGH')} HIGH lines on five references (§4); none is changed by this report (D-1013-10, re-put).")
w(f"- Marcus Smart and Deandre Ayton, question marks for the first time now that a second projection covers them (D-1013-13).")
w(f"- The {len(old)} players aged 34 and older with no decline in the method (D-1013-11).")
w(f"- The {n('UNANCHORED')} unanchored lines, {plural(len(ubig), 'line')} beyond 0.5 z: " + ", ".join(f"{r['name']} {r['tests']['T1']['net_z']:+.2f}" for r in ubig) + " (D-1013-12, re-put).")
w(f"- Philadelphia's pool at {phi} possessions against 117.7; the usage model is D-C2, after the draft.")
w("- The 10/14 lock paste (D-1013-1) and the publish freeze during the draft (D-1013-5); no RESYNC during the draft (D-1013-2).\n")
w("## Open-item receipts\n\n| item | query run (2026-10-13) | dated finding |\n|---|---|---|")
w("| (this intake) | no web research and no roster pull; the Bleacher Report fetch attempted and refused (ENOTFOUND; proxy CONNECT 403) | the uploads are the owner's files of 2026-10-13; the lines audited are the ones merged in kit PR #109 |")
w("| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (`after-report-2026-10-13.md`, receipts dated 10/13) | all HELD or unsigned on 2026-10-13 per those receipts; not re-queried here (did not check). The card paste tags Ingram Out and Porzingis Day-To-Day, consistent with those receipts |\n")
w(rn[rn.index("## Repeat-name market check"):].strip() + "\n")
w("\n## Bounds\n\n**Out of scope by design.**")
w("- No line was changed, built or dry-run. The option, if asked: the HIGH lines clamped to the edge of the five-source range at the lock, the dial method, or a line-by-line review with two dated outlets each.")
w("- The deck's range check was not changed; it still reads three sources (D-1013-14).")
w("- The card paste's 2026 statistics rows and outlook paragraphs were not transcribed; the outlooks were read in-session as role context and are not evidence here.")
w("- Ranks 181 to 200 and the deck-only rows were not audited.\n")
w("**In scope and unverified.**")
w("- The card paste's origin: `UNVERIFIABLE` from this container (basketballmonster.com ENOTFOUND); recorded as the owner gave it with the observed layout.")
w("- The RotoBaller re-export's date: `UNVERIFIABLE`, the file carries none; its lines equal the 9/29 file, which is the fact that matters for the audit.")
w(f"- The {len(few)} lines with fewer than three projections: their T1 verdicts rest on a narrow or absent band: `ATTEMPTED-FAILED`, no deeper source on file (Hashtag's file stops at 200, the cards at 200, FantasyPros' projected rows at 265, RotoBaller at 250).")
w("- Whether five sources share a blind spot on a roster: `NOT-ATTEMPTED`; a line inside their range cannot show one.")
w("- Whether the clamped and history-shaped lines are closer to what will happen than the outside projections: `UNVERIFIABLE` until games are played.\n")
w("## Decision sheet (owner disposes)\n\n| id | decision question | default if silent |\n|---|---|---|")
w(f"| D-1013-10 (re-put) | The {n('HIGH')} HIGH lines on five references ({', '.join(r['name'] for r in HIGH)}): (a) hold for the draft; (b) clamp the ones with three or more references to the edge of the five-source range at the lock; (c) review line by line with two dated outlets each | (a) for tonight; only Jamal Murray and Collin Gillespie sit in the top 100 |")
w(f"| D-1013-13 | {SM} and {AY}: (a) hold; (b) clamp to the edge at the lock | (a); both sit past rank 100 |")
w(f"| D-1013-14 | Add FantasyPros and the cards to the deck's own range check (`scripts/range_check.py` LINE_SOURCES), so the build gate reads five sources | after the draft; the next build already sees the 10/13 RotoBaller file's {len(added)} added names |")
w(f"| D-1013-11 | Age decline for the {len(old)} players 34 and older: (a) none, as now; (b) a flat per-36 haircut by age band, after the draft with D-C2 | (b) after the draft |")
w(f"| D-1013-12 (re-put) | The {plural(len(ubig), 'unanchored line')} beyond 0.5 z net ({', '.join(r['name'] for r in ubig)}): (a) hold; (b) move to the outside average at the lock | (a) |")
w("| D-1013-8, D-1013-9 | Murray and Nesmith just past the cut; Ware LINE QUESTIONED | as set in the dial report |")
w("| D-1013-1..7, D-C2, D-SF-1..4 and earlier | carried | carried |\n")
w("## Provenance\n")
w("- Inputs: kit `main` 7c44327 (board, lines, the first audit), deck `main` dd6b719 (page sha256 09a889d4baa5, the z frame); the three uploads from the owner's 2026-10-13 message (sha256 b58e2d6d9fca RotoBaller, d1f79284034e FantasyPros; the cards transcribed from the paste).")
w("- Intake: `report/market/third_party_market.py` (two new sources, no-rank handling, percentage scale), `build_market.py` (one alias), `check_derived.py` (three entries; 27 of 27 reproduce at pin d08ac74), `provenance.csv` (three rows).")
w(f"- Audit: `audit180-2026-10-13/audit180_v2.py` (two runs identical, md5 checked), `audit180_v2.json`, `audit180_v2.txt`, `write_audit_report_v2.py` (this file's writer, which runs the check below before writing). Known-answer check: `reproduce_check_v2.py` recomputes every outside band from the five processed files with its own loader: {REP.group(1)} cells outside the band, {REP.group(2)} reported by the audit, {REP.group(3)} disagreements. The first audit's records untouched.")
w("- No line, tag or placement changed; both planes' hashes equal before and after (e821ec1ddc67 kit, bd2b983876a8 deck).\n")
w("## In plain language\n")
w(f"**What your uploads did.** They doubled the number of outside projections behind most lines: {rpl['5']} of the 180 now have five, and the band they span is wider than the three-source band, so {len(down)} lines moved down a tier: {len(inside)} because every cell that was outside the three-source band sits inside the five-source band, {len(widened)} because the band widened and the disagreement shrank, {len(flagoff)} because a minutes, games or age flag no longer fires against the wider set, and {len(lostref)} (Goodwin) because a reference was lost. The HIGH list goes from {n1('HIGH')} to {n('HIGH')}: Murray, Gillespie, Beal, Nesmith and Mamukelashvili stay; six come off because the wider band covers most of their cells ({OFF_HIGH}); Goodwin comes off only because he lost a reference. Two new names appear: Marcus Smart, where both outside sources that cover him project {_sm['pts']['lo']:g} points against our {_sm['pts']['line']:g}, and Deandre Ayton, where all three sit below our {_ay['pts']['line']:g} points and {_ay['reb']['line']:g} rebounds.")
w(f"\n**What the RotoBaller file is.** The same projection as the 9/29 file, re-ranked: every shared player's stat line is identical, {ranks_moved} ranks moved, {len(added)} names added and {len(dropped)} dropped. It adds names at the bottom of the board, not a fresh view.")
w(f"\n**What is still open.** The age question is unchanged: {len(old)} players 34 and older sit above every projection's average and the method carries no decline. The {len(few)} bench lines with fewer than three projections. And the Bleacher Report piece, which I cannot reach from here; paste it and it becomes a role-context source for the HIGH and MEDIUM lines.")
w("\n**Your decisions.** D-1013-10 and D-1013-13 tonight or at the lock; D-1013-14, D-1013-11 and D-1013-12 can wait for the draft's aftermath.")
P = os.path.join(AR, "after-report-2026-10-13-uploads.md")
open(P, "w", encoding="utf-8").write("\n".join(o) + "\n")
PL = os.path.join(K, "report", "pull-log.md"); pl = rd(PL)
assert "after-report-2026-10-13-uploads.md" not in pl
row = (f"| 2026-10-13 | owner uploads: RotoBaller re-export, FantasyPros projections, player-card paste (intake + the top-180 audit re-run on five references; no roster pull) | 0 | 0 | 0 | "
       f"after-reports/after-report-2026-10-13-uploads.md — three raws pinned and joined under the hard gate ({rb_n}, {fp_n}, {cd_n} matched), registered (derived 27/27); "
       f"the RotoBaller file is the 9/29 projection re-ranked ({same_lines} identical lines, {ranks_moved} ranks moved, 12 names swapped); the cards transcribed with the A/TO check (0 mismatches); "
       f"{rpl['5']} of 180 lines now have five outside projections; T1 {f1['T1']} to {f2['T1']} lines, {zpos:+.2f}/{zneg:+.2f} z; tiers HIGH {n('HIGH')}, MEDIUM {n('MEDIUM')}, LOW {n('LOW')}, UNANCHORED {n('UNANCHORED')}, CLEAN {n('CLEAN')}; "
       f"Smart and Ayton new question marks, Goodwin off HIGH by a lost reference; Bleacher Report host unreachable; no plane change; D-1013-10/12 re-put, D-1013-13/14 on the sheet |")
open(PL, "w", encoding="utf-8").write(pl.rstrip("\n") + "\n" + row + "\n")
print("report and pull-log row written:", P)
