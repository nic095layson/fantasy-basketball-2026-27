#!/usr/bin/env python3
"""Every figure the 10/13 Yahoo after-report states as typed text (not computed by its writer) checked against the pinned
files: the raw paste, yahoo-2026-10-13.csv, yahoo-proj-2026-10-0{1,6}/13.csv, the disagreements report, the kit's
projections, and the deck's Version 64 page (values / availability). One line per claim, PASS or FAIL."""
import csv, json, os, re, subprocess, unicodedata
H = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.normpath(os.path.join(H, "..", "..", ".."))
M = os.path.join(KIT, "report", "market")
DECK = os.environ.get("DECK_REPO", "/home/user/yahoo-fantasy-basketball")
fold = lambda s: re.sub(r"[^a-z ]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip()
raw = open(os.path.join(M, "yahoo-raw-2026-10-13.txt"), encoding="utf-8").read()
price = list(csv.DictReader(open(os.path.join(M, "yahoo-2026-10-13.csv"))))
p13 = {fold(r["player"]): r for r in csv.DictReader(open(os.path.join(M, "yahoo-proj-2026-10-13.csv")))}
pr = {fold(r["player"]): r for r in price}
dis = open(os.path.join(M, "disagreements-yahoo-2026-10-13.md"), encoding="utf-8").read()
kit = {fold(r["name"]): r for r in csv.DictReader(open(os.path.join(KIT, "report", "projections-2026-27.csv")))}
res = []
def chk(claim, ok, got=""): res.append((ok, claim, got)); print(("PASS " if ok else "FAIL ") + claim + (f"  [{got}]" if got else ""))
# line 55 / 56 / 61
marks = [int(x) for x in re.findall(r"Your Turn - (\d+)(?:st|nd|rd|th) Pick", raw)]
chk("13 turn markers at 10,15,34,39,58,63,82,87,106,111,130,135,154", marks == [10,15,34,39,58,63,82,87,106,111,130,135,154], marks)
chk("raw paste 1,910 lines", raw.count("\n") + (0 if raw.endswith("\n") else 1) == 1910, raw.count("\n"))
xr = sorted(int(r["xrank"]) for r in price)
chk("price file 300 names, XRank 1..300 with no gap", xr == list(range(1, 301)), len(xr))
chk("187 names carry an ADP", sum(1 for r in price if r["adp"]) == 187, sum(1 for r in price if r["adp"]))
chk("the 10/01 list was 300 deep", sum(1 for _ in csv.DictReader(open(os.path.join(M, "yahoo-2026-10-01.csv")))) == 300)
yonly = re.search(r"## E\. Coverage gaps — Yahoo names not in our pool \((\d+)", dis)
chk("I7 297 of 300 resolved (3 Yahoo-only names)", yonly and yonly.group(1) == "3", yonly and yonly.group(1))
# line 57 / 108 / 123
s = p13.get(fold("Ben Simmons"), {})
chk("Ben Simmons ADP 111.1 with 15 projected games", s.get("adp") == "111.1" and s.get("gp") == "15", (s.get("adp"), s.get("gp")))
chk("Tre Jones keeps XRank 138, no ADP", pr[fold("Tre Jones")]["xrank"] == "138" and not pr[fold("Tre Jones")]["adp"], pr[fold("Tre Jones")])
chk("Yves Missi ADP 114.9", pr[fold("Yves Missi")]["adp"] == "114.9", pr[fold("Yves Missi")]["adp"])
k = kit.get(fold("Ben Simmons"), {})
chk("kit: Ben Simmons GP 55 (corrected 2026-10-13 from a typed 15, which was Yahoo's figure)", k.get("gp") == "55", k.get("gp"))
board = open(os.path.join(KIT, "report", "top-200-2026-27.md"), encoding="utf-8").read()
chk("kit: Ben Simmons outside the top-200 board", "Ben Simmons" not in board)
v64 = {fold(r["n"]): r for r in json.load(open(os.path.join(KIT, "report/after-reports/live-mock-2026-10-13/val_v64.json")))}
bs = v64[fold("Ben Simmons")]
chk("deck: Ben Simmons availability 0.78, negative value", bs["av"] == 0.78 and bs["adj"] < 0, (bs["av"], bs["adj"]))
# line 86
O = [n for n, r in p13.items() if r["status"] == "O"]
chk("O letters on 10 rows", len(O) == 10, len(O))
for n, a in [("Jusuf Nurkic", "113.9"), ("Jimmy Butler", "115.8"), ("Mark Williams", "109.3"), ("Maxime Raynaud", "117.7"), ("Isaiah Stewart", "113.0"), ("Brandon Ingram", "72.5")]:
    chk(f"{n} ADP {a}", pr[fold(n)]["adp"] == a, pr[fold(n)]["adp"])
excl_adp = [n for n in ["Jusuf Nurkic", "Jimmy Butler", "Mark Williams", "Shaedon Sharpe", "Max Strus", "Donte DiVincenzo", "Moses Moody"] if pr.get(fold(n), {}).get("adp")]
chk("of the seven excluded O rows, three carry an ADP (Nurkić, Butler, Mark Williams; corrected from a typed four)", sorted(excl_adp) == sorted(["Jusuf Nurkic", "Jimmy Butler", "Mark Williams"]), excl_adp)
d = re.search(r"## D\. Availability disagreements \((\d+)\)", dis)
chk("disagreements §D lists 9 rows", d and d.group(1) == "9", d and d.group(1))
for n, g in [("Alex Caruso", "58"), ("Al Horford", "53"), ("Jaylin Williams", "60"), ("Khris Middleton", "53"), ("Zach Collins", "55"), ("Ziaire Williams", "38"), ("Dominick Barlow", "53"), ("Dru Smith", "60"), ("Luka Garza", "52")]:
    r = p13.get(fold(n), {}); chk(f"{n} Q, Yahoo GP {g}", r.get("status") == "Q" and r.get("gp") == g, (r.get("status"), r.get("gp")))
top150 = [n for n in ["Alex Caruso", "Al Horford", "Jaylin Williams", "Khris Middleton", "Zach Collins", "Ziaire Williams", "Dominick Barlow", "Dru Smith", "Luka Garza"]
          if int(pr[fold(n)]["xrank"]) <= 150 or (v64.get(fold(n), {}).get("valRank") or 999) <= 150]
chk("none of those nine is a top-150 row (Yahoo XRank or our value rank)", not top150, top150)
# line 111
for n, st, a in [("Brandon Ingram", "O", "72.5"), ("Kristaps Porzingis", "Q", "104.2"), ("Kawhi Leonard", "", "34.2"), ("Ryan Rollins", "", "74.3"), ("Bennedict Mathurin", "", "115.9")]:
    r = p13.get(fold(n), {}); chk(f"{n} letter '{st}' ADP {a}", r.get("status", None) == st and r.get("adp") == a, (r.get("status"), r.get("adp")))
for n in ["Jeremy Sochan", "Cam Thomas", "Jaden Ivey", "Lonzo Ball", "Rob Dillingham"]:
    chk(f"{n} absent from the 300", fold(n) not in pr)
# line 123: names among §F risers / fallers
F = dis[dis.index("## F."):]
ris = F[F.index("### Risers"):F.index("### Fallers")]; fal = F[F.index("### Fallers"):F.index("### Newly")]
for n in ["Ty Jerome", "Kevin Porter", "Darius Acuff", "Ajay Mitchell", "Keegan Murray", "John Collins"]:
    chk(f"{n} among §F risers", n in ris)
for n in ["DeRozan", "Herb", "Claxton", "Bey", "Ingram", "Turner"]:
    chk(f"{n} among §F fallers", n in fal)
print(f"\n{sum(ok for ok, *_ in res)} of {len(res)} claims PASS")
