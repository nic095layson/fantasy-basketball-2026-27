#!/usr/bin/env python3
"""Every figure typed into the usage report's Holiday follow-up (headline paragraph, §4 tables, §6 table and counts)
checked against the script outputs it came from: por_lines.txt, context_check.txt and preseason_roles.txt (the two
"Real-life context" tables of §3 and §4); and the first answer's tables (§3 Maxey and Philadelphia, §5 team budget, the
headline's Philadelphia figures) against phi_lines.txt, team_budget.txt and ../live-mock-2026-10-13/val_v59.json and
val_v63.json. Prints one line per literal
and a PASS count; exits 1 on any mismatch."""
import os, re, sys
H = os.path.dirname(os.path.abspath(__file__))
R = open(os.path.join(H, "..", "after-report-2026-10-13-usage.md"), encoding="utf-8").read()
P = open(os.path.join(H, "por_lines.txt"), encoding="utf-8").read()
C = open(os.path.join(H, "context_check.txt"), encoding="utf-8").read()
ok = bad = 0
def check(label, want, got):
    global ok, bad
    good = (abs(float(want) - float(got)) < 1e-9) if isinstance(want, (int, float)) or re.fullmatch(r"-?[\d.]+", str(want)) else str(want) == str(got)
    ok += good; bad += not good
    print(f"{'PASS' if good else 'FAIL'} | {label} | report {got} | record {want}")
def section(head, nxt):
    return R[R.index(head):R.index(nxt)]
def table(text, first):
    rows = [ln for ln in text.splitlines() if ln.startswith("| ") and not ln.startswith("|---")]
    return [[c.strip() for c in ln.strip("|").split("|")] for ln in rows if ln.split("|")[1].strip() != first]
# por_lines blocks
blocks = {m.group(1): m.group(2) for m in re.finditer(r"== (.+?)\n(.*?)(?=\n== |\Z)", P, re.S)}
def prow(name, prefix):
    for ln in blocks[name].splitlines():
        if ln.strip().startswith(prefix): return [c.strip() for c in ln.split("|")]
    return None
num = lambda x: float(x.replace("**", "").strip())
# §4 Holiday per-game table: GP | min | shots | points | threes | assists | turnovers
s4 = section("## 4. Holiday", "## 5. ")
src = {"2023-24 actual (BOS)": "2023-24 actual (BOS)", "2024-25 actual (BOS)": "2024-25 actual (BOS)", "2025-26 actual (POR)": "2025-26 actual (POR)",
       "practice-era line": "practice-era kit line", "**shipped today**": "today's shipped line", "Yahoo 10/13 projection": "Yahoo 10/13 projection",
       "Hashtag 10/12 projection": "Hashtag 10/12 projection", "RotoBaller 9/29 projection": "RotoBaller 9/29 projection"}
cols = {"GP": 1, "min": 2, "shots": 3, "points": 4, "threes": 5, "assists": 6, "turnovers": 8}
for row in table(s4.split("RotoWire's panel")[0], "Holiday"):
    rec = prow("Jrue Holiday", src[row[0]])
    for i, (cname, j) in enumerate(cols.items(), start=1):
        if row[i] in ("—", "-"): check(f"Holiday {row[0]} {cname}", "-", rec[j]); continue
        check(f"Holiday {row[0]} {cname}", rec[j], num(row[i]))
# §4 points table
pts = table(s4.split("| points per game |")[1].split("How each line was built")[0], "---")
for row in pts:
    n = row[0]
    a = prow(n, "2025-26 actual (")
    if row[1] == "no games": check(f"{n} 2025-26", "no row", "no row" if prow(n, "2025-26 actual |") else "row")
    else:
        m = re.fullmatch(r"(\d+(?:\.\d+)?) \((\w+), (\d+) games\)", row[1])
        check(f"{n} 2025-26 points", a[4], m.group(1)); check(f"{n} 2025-26 games", a[1], m.group(3)); check(f"{n} 2025-26 team", a[0].split("(")[1].rstrip(")"), m.group(2))
    shipped = prow(n, "today's shipped line")
    check(f"{n} minutes in how-built", shipped[2], re.search(r"(\d+(?:\.\d+)?)$", row[2]).group(1))
    check(f"{n} practice-era points", prow(n, "practice-era kit line")[4], row[3])
    check(f"{n} shipped points", shipped[4], row[4])
    outs = [float(prow(n, k)[4]) for k in ("Yahoo 10/13 projection", "Hashtag 10/12 projection", "RotoBaller 9/29 projection")]
    lo, hi = [float(x) for x in row[5].split("–")]
    check(f"{n} outside low", min(outs), lo); check(f"{n} outside high", max(outs), hi)
    rk = re.search(r"Version 59\) (\d+) / (\d+); live page \(Version 64\) (\d+) / (\d+)", blocks[n]).groups()
    check(f"{n} practice ranks", f"{rk[0]} / {rk[1]}", row[6]); check(f"{n} live ranks", f"{rk[2]} / {rk[3]}", row[7])
# §6 table against context_check rows
s6 = section("## 6. Board-wide", "## 7. ")
crow = {ln.split(" | ")[0]: ln.split(" | ") for ln in C.splitlines() if ln.count(" | ") > 8 and not ln.startswith("player |")}
TEAM = {"BKN": "BRK", "PHX": "PHO"}; BUD = {"over the league max": "over league max", "over its own total": "over own total", "under both": "under"}
six = table(s6, "player")
check("§6 table rows", 18, len(six))
for row in six:
    c = crow[row[0]]
    check(f"{row[0]} team", c[3], row[1])
    t, g = row[2].rsplit(", ", 1); t = "/".join(TEAM.get(x, x) for x in t.split(" and "))
    check(f"{row[0]} 2025-26", c[4], f"{t} {g} g")
    check(f"{row[0]} our points", c[5], row[3])
    lo, hi = [float(x) for x in row[4].split("–")]; clo, chi = [float(x) for x in c[6].split("-")]
    check(f"{row[0]} outside low", clo, lo); check(f"{row[0]} outside high", chi, hi)
    check(f"{row[0]} value / market", c[2], row[5])
    check(f"{row[0]} budget", c[8], BUD[row[6]])
# counts
g = lambda pat: re.search(pat, C).groups()
a, b, cells = g(r"have a cell outside all three projections \((\d+) cells\)")[0], *g(r"(\d+) of (\d+) checkable")
check("lines with a cell outside", a if False else g(r"projections only|: (\d+) of \d+ checkable")[0] if False else re.search(r"reference: (\d+) of (\d+) checkable", C).group(1), re.search(r"(\d+) of the (\d+) checkable top-150 lines", R).group(1))
check("checkable", re.search(r"reference: (\d+) of (\d+) checkable", C).group(2), re.search(r"(\d+) of the (\d+) checkable top-150 lines", R).group(2))
check("cells", g(r"\((\d+) cells\)")[0], re.search(r"projections, (\d+) cells in all", R).group(1))
ab = g(r"points above all three: (\d+); points below all three: (\d+)")
check("points above", ab[0], re.search(r"(\d+) lines score above all three projections and (\d+) below", R).group(1))
check("points below", ab[1], re.search(r"(\d+) lines score above all three projections and (\d+) below", R).group(2))
bud = g(r"over the league max (\d+), over its own total (\d+), under both (\d+)")
m = re.search(r"(\d+) of the 18 sit on teams over the league maximum and (\d+) on teams over their own 2025-26 total; (\d+) are on teams under both", R)
for i, lab in enumerate(("over max", "over own", "under both")): check(f"budget count {lab}", bud[i], m.group(i + 1))
mk = g(r"ranked above their market price on the live page: (\d+); by 25 or more places: (\d+); below it: (\d+)")
m = re.search(r"On the live page (\d+) of the 18 rank above their market price, (\d+) of them by 25", R)
check("above market", mk[0], m.group(1)); check("above market by 25+", mk[1], m.group(2))
check("headline above market", mk[0], re.search(r"and (\d+) rank above their market price on the live page", R).group(1))
check("headline over max", bud[0], re.search(r"Only (\d+) of the 18 sit on the teams over the league maximum", R).group(1))
by = dict((k, int(v)) for k, v in re.findall(r"(\w{3}) (\d+)", C.split("by team today: ")[1].splitlines()[0]))
m = re.search(r"Cleveland (\d+), Portland (\d+), Dallas (\d+), Philadelphia (\d+), Utah (\d+), and one each on (\w+) other teams", R)
for i, t in enumerate(("CLE", "POR", "DAL", "PHI", "UTA")): check(f"by team {t}", by[t], m.group(i + 1))
check("single teams", sum(v == 1 for v in by.values()), {"six": 6}.get(m.group(6), m.group(6)))
t20 = g(r"arrival or return at 20\+ minutes: (\d+) of (\d+)"); t25 = g(r"arrival or return at 25\+ minutes: (\d+) of (\d+)")
m = re.search(r"Every team in the pool has one \((\d+) of (\d+) teams; (\d+) of (\d+) at 25\+ minutes\)", R)
check("teams 20+", f"{t20[0]} of {t20[1]}", f"{m.group(1)} of {m.group(2)}"); check("teams 25+", f"{t25[0]} of {t25[1]}", f"{m.group(3)} of {m.group(4)}")
# headline Holiday literals against por_lines
hl = R[R.index("**Headline, the Holiday follow-up.**"):R.index("## 1. Roster changes")]
sh = prow("Jrue Holiday", "today's shipped line")
m = re.search(r"own 2025-26 line, (\d+(?:\.\d+)?) points, (\d+(?:\.\d+)?) assists and (\d+(?:\.\d+)?) shots", hl)
check("headline Holiday points", sh[4], m.group(1)); check("headline Holiday assists", sh[6], m.group(2)); check("headline Holiday shots", sh[3], m.group(3))
check("headline Henderson games", prow("Scoot Henderson", "2025-26 actual (")[1], re.search(r"Henderson limited to (\d+) games", hl).group(1))
bos = [float(prow("Jrue Holiday", f"{y} actual (BOS)")[3]) for y in ("2023-24", "2024-25")]
m = re.search(r"he took (\d+) to (\d+) shots", hl); check("headline Boston shots low", round(min(bos)), m.group(1)); check("headline Boston shots high", round(max(bos)), m.group(2))
rk = re.search(r"Version 59\) (\d+) / (\d+); live page \(Version 64\) (\d+) / (\d+)", blocks["Jrue Holiday"]).groups()
m = re.search(r"value rank (\d+) to (\d+) against a market rank of (\d+)", hl)
check("headline rank practice", rk[0], m.group(1)); check("headline rank live", rk[2], m.group(2)); check("headline market", rk[3], m.group(3))
m = re.search(r"minutes, (\d+(?:\.\d+)?) and (\d+(?:\.\d+)?), and left", hl)
check("headline Lillard minutes", prow("Damian Lillard", "today's shipped line")[2], m.group(1)); check("headline Morant minutes", prow("Ja Morant", "today's shipped line")[2], m.group(2))
pool = {ln.split(" | ")[0].strip(): ln for ln in blocks["Portland's pool today (kit projections-2026-27.csv), by projected minutes x games"].splitlines()[0:0]} if False else P.split("== Portland's pool today")[1]
check("headline Lillard GP", re.search(r"Damian Lillard \| PG \| GP (\d+)", pool).group(1), re.search(r"Lillard's (\d+) projected games", hl).group(1))
check("headline Sharpe GP", re.search(r"Shaedon Sharpe \| [A-Z,]+ \| GP (\d+)", pool).group(1), re.search(r"Sharpe's (\d+) leave room", hl).group(1))
# real-life tables against preseason_roles.txt
PR = open(os.path.join(H, "preseason_roles.txt"), encoding="utf-8").read()
GAMES = {"10/05 vs New York": ("2026-10-05", "PHI", "NY"), "10/08 vs Brooklyn": ("2026-10-08", "PHI", "BKN"),
         "10/10 vs Boston": ("2026-10-10", "PHI", "BOS"), "10/07 vs Golden State": ("2026-10-07", "POR", "GS")}
FULL = {"Maxey": "Tyrese Maxey", "Edgecombe": "VJ Edgecombe", "Brown": "Jaylen Brown", "LeBron": "LeBron James", "Embiid": "Joel Embiid",
        "Lillard": "Damian Lillard", "Morant": "Ja Morant", "Holiday": "Jrue Holiday", "Henderson": "Scoot Henderson"}
def recorded(game, name):
    if game == "10/12 vs London Lions":
        m = re.search(r"2026-10-12 POR vs London Lions \| " + re.escape(name) + r" \| (.+)", PR).group(1)
        if "did not play" in m: return "did not play, coach's decision" if "coach's decision" in m else m
        role, mins = re.match(r"(starter|bench), (\d+) min", m).groups()
        return f"{'started' if role == 'starter' else 'bench'}, {mins} min"
    d, t, o = GAMES[game]
    m = re.search(re.escape(f"{d} {t} vs {o} | {name} | ") + r"(.+)", PR).group(1)
    if m.startswith("did not play"):
        why = re.search(r"\((.+)\)", m).group(1)
        return "did not dress" if why == "did not dress" else f"did not play, {why}"
    return m.replace("starter,", "started,")
for head in ("## 3. Maxey", "## 4. Holiday"):
    sec = R[R.index(head):]; sec = sec[sec.index("**Real-life context, checked 10/13.**"):]
    lines = [ln for ln in sec.splitlines() if ln.startswith("| ")]
    hdr = [c.strip() for c in lines[0].strip("|").split("|")]
    body = []
    for ln in lines[1:]:
        if ln.startswith("|---"): continue
        if not ln.startswith("| 10/"): break
        body.append([c.strip() for c in ln.strip("|").split("|")])
    for row in body:
        for col, cell in zip(hdr[1:], row[1:]):
            check(f"{row[0]} {col}", recorded(row[0], FULL[col]), cell)
# §3 Maxey per-game table and the Philadelphia points table against phi_lines.txt
import json
PH = open(os.path.join(H, "phi_lines.txt"), encoding="utf-8").read()
pblocks = {m.group(1): m.group(2) for m in re.finditer(r"== (.+?)\n(.*?)(?=\n== |\Z)", PH, re.S)}
def phrow(name, prefix):
    for ln in pblocks[name].splitlines():
        if ln.strip().startswith(prefix): return [c.strip() for c in ln.split("|")]
s3 = section("## 3. Maxey", "## 4. Holiday")
msrc = {"2023-24 actual": "2023-24 actual", "2024-25 actual": "2024-25 actual", "2025-26 actual": "2025-26 actual",
        "practice-era line": "practice-era kit line", "**shipped today**": "today's shipped line", "Yahoo 10/13 projection": "Yahoo 10/13 projection",
        "Hashtag 10/12 projection": "Hashtag 10/12 projection", "RotoBaller 9/29 projection": "RotoBaller 9/29 projection"}
for row in table(s3.split("RotoWire's panel")[0], "Maxey"):
    rec = phrow("Tyrese Maxey", msrc[row[0]])
    for i, cname in enumerate(("GP", "min", "shots", "points", "threes", "assists"), start=1):
        if row[i] in ("—", "-"): check(f"Maxey {row[0]} {cname}", "-", rec[i]); continue
        check(f"Maxey {row[0]} {cname}", rec[i], num(row[i]))
V59 = {r["n"]: r for r in json.load(open(os.path.join(H, "..", "live-mock-2026-10-13", "val_v59.json"), encoding="utf-8"))}
V63 = {r["n"]: r for r in json.load(open(os.path.join(H, "..", "live-mock-2026-10-13", "val_v63.json"), encoding="utf-8"))}
ptab = s3.split("| points per game | practice-era line |")[1].split("Value ranks from")[0]
for row in table(ptab, "---"):
    n = row[0]
    check(f"{n} practice-era points", phrow(n, "practice-era kit line")[4], row[1])
    check(f"{n} shipped points", phrow(n, "today's shipped line")[4], row[2])
    outs = [float(phrow(n, k)[4]) for k in ("Yahoo 10/13 projection", "Hashtag 10/12 projection", "RotoBaller 9/29 projection")]
    lo, hi = [float(x) for x in row[3].split("–")]
    check(f"{n} outside low", min(outs), lo); check(f"{n} outside high", max(outs), hi)
    a = phrow(n, "2025-26 actual")
    m = re.match(r"(\d+(?:\.\d+)?) \((\w+)(?:, (\d+) games)?\)", row[4])
    check(f"{n} 2025-26 points", a[4], m.group(1)); check(f"{n} 2025-26 team", a[0].split("(")[1].rstrip(")"), m.group(2))
    if m.group(3): check(f"{n} 2025-26 games", a[1], m.group(3))
    check(f"{n} value rank practice / today", f"{V59[n]['valRank']} / {V63[n]['valRank']}", row[5])
# §5 team budget table and board-wide table against team_budget.txt
TB = open(os.path.join(H, "team_budget.txt"), encoding="utf-8").read()
trow = {ln.split(" | ")[0]: ln.split(" | ") for ln in TB.splitlines() if re.match(r"^[A-Z]{3} \| \d+ \|", ln)}
s5 = section("## 5. The team usage budget", "## 6. ")
for row in table(s5.split("The 2025-26 league range")[0], "team"):
    t = trow[row[0]]
    check(f"{row[0]} minutes", t[2], row[1])
    shots_now, shots_was = t[3].split(" vs ")
    check(f"{row[0]} shots", shots_now, row[2]); check(f"{row[0]} 2025-26 shots", shots_was, row[3])
    pos_now, pos_was = t[4].split(" vs ")
    check(f"{row[0]} possessions", pos_now, row[4]); check(f"{row[0]} 2025-26 possessions", pos_was, row[5])
rng = re.search(r"possessions used per game: (\d+(?:\.\d+)?)-(\d+(?:\.\d+)?); shots \(FGA\) (\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)", TB).groups()
m = re.search(r"league range was (\d+(?:\.\d+)?)–(\d+(?:\.\d+)?) shots and (\d+(?:\.\d+)?)–(\d+(?:\.\d+)?) possessions", s5).groups()
for lab, want, got in (("shots low", rng[2], m[0]), ("shots high", rng[3], m[1]), ("possessions low", rng[0], m[2]), ("possessions high", rng[1], m[3])):
    check(f"league range {lab}", want, got)
oo = re.search(r"2025-26: (\d+) \[", TB).group(1); om = re.search(r"league maximum \([\d.]+\): (\d+) \[", TB).group(1)
po, pm = re.search(r"practice-era lines: (\d+) over own, (\d+) over the league max", TB).groups()
cov = re.findall(r"cover (\d+(?:\.\d+)?)% of 2025-26 league minutes and claim (\d+(?:\.\d+)?)% of its possessions", TB)
bw = {r[0]: r[1:] for r in table(s5.split("| board-wide |")[1].split("- **Philadelphia")[0], "---")}
check("over own today", oo, bw["teams whose pool alone exceeds the team's own 2025-26 possessions"][0]); check("over own practice", po, bw["teams whose pool alone exceeds the team's own 2025-26 possessions"][1])
check("over max today", om, bw["teams whose pool alone exceeds the 2025-26 league maximum"][0]); check("over max practice", pm, bw["teams whose pool alone exceeds the 2025-26 league maximum"][1])
check("minutes covered today", cov[0][0] + "%", bw["share of league minutes the pools cover"][0]); check("minutes covered practice", cov[1][0] + "%", bw["share of league minutes the pools cover"][1])
check("possessions claimed today", cov[0][1] + "%", bw["share of league possessions the pools claim"][0]); check("possessions claimed practice", cov[1][1] + "%", bw["share of league possessions the pools claim"][1])
ph = {m.group(1).strip(): (float(m.group(2)), float(m.group(3))) for m in re.finditer(r"^  (.+?)\s+\d+\s+[\d.]+\s+[\d.]+ \|\s+(\d+(?:\.\d+)?) \((\d+(?:\.\d+)?)\)$", TB.split("PHI: player")[1].split("\n\n")[0], re.M)}
for n, d in re.findall(r"(Brown|Caldwell-Pope|LeBron|Edgecombe|Maxey) \+(\d+(?:\.\d+)?)", s5):
    full = {"Brown": "Jaylen Brown", "Caldwell-Pope": "Kentavious Caldwell-Pope", "LeBron": "LeBron James", "Edgecombe": "VJ Edgecombe", "Maxey": "Tyrese Maxey"}[n]
    check(f"PHI added possessions {n}", round(ph[full][0] - ph[full][1], 1), d)
hl1 = R[R.index("**Headline.**"):R.index("**Headline, the Holiday follow-up.**")]
m = re.search(r"claim (\d+(?:\.\d+)?) shots and (\d+(?:\.\d+)?) possessions a game", hl1)
check("headline PHI shots", trow["PHI"][3].split(" vs ")[0].split(" ")[0], m.group(1)); check("headline PHI possessions", trow["PHI"][4].split(" vs ")[0].split(" ")[0], m.group(2))
m = re.search(r"was (\d+(?:\.\d+)?) shots and (\d+(?:\.\d+)?) possessions; Philadelphia itself used (\d+(?:\.\d+)?)", hl1)
check("headline max shots", rng[3], m.group(1)); check("headline max possessions", rng[1], m.group(2)); check("headline PHI own", trow["PHI"][4].split(" vs ")[1], m.group(3))
print(f"\n{ok} of {ok + bad} literals PASS")
sys.exit(1 if bad else 0)
