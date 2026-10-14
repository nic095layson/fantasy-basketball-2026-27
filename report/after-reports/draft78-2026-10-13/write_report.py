#!/usr/bin/env python3
"""Writes report/after-reports/after-report-2026-10-13-draft78.md and the pull-log row from the records: the deck's
m78_final / m78_arms / m78_hindsight / m78_deckcard_v65 (the true board) / m78_deckcard_v65_toolstate (the board the tool
held, #88 still UNKNOWN) / m78_tool_vs_truth_dom (the tool log replayed through the v65 page) / m78_replay, this folder's
state_check.txt, yahoo_standings, yahoo_compare.json, six_lines.json and six_cards.json (the owner's question of 10/14),
and rn_section_m78.md (the repeat-name check on 27 mocks). No figure is typed by hand."""
import csv, glob, json, os, re
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.normpath(os.path.join(H, "..", "..", ".."))
D = "/home/user/yahoo-fantasy-basketball/arena/results"
J = lambda p: json.load(open(p, encoding="utf-8")); rd = lambda p: open(p, encoding="utf-8").read()
A = J(f"{D}/m78_arms.json"); HS = J(f"{D}/m78_hindsight.json"); PG = J(f"{D}/m78_deckcard_v65.json")
TS = J(f"{D}/m78_deckcard_v65_toolstate.json"); DOM = J(f"{D}/m78_tool_vs_truth_dom.json"); RP = J(f"{D}/m78_replay.json")["v65"]
F = J(f"{D}/m78_final.json")["v65"]
recap = J(os.path.join(H, "recap.json")); sc = rd(os.path.join(H, "state_check.txt"))
YS = list(csv.DictReader(open(os.path.join(H, "yahoo_standings_2026-10-13.csv"))))
YC = {o["seat"]: o for o in J(os.path.join(H, "yahoo_compare.json"))}
SL = J(os.path.join(H, "six_lines.json")); SC = J(os.path.join(H, "six_cards.json"))
rn = rd(os.path.join(H, "rn_section_m78.md")); rn = rn[rn.index("## Repeat-name market check"):].strip()
msg = rd(os.path.join(H, "owner_message.txt"))
mgr = {p["slot"]: p["manager"] for p in recap}
# ---- the card at each owner turn: true board (recap) and the board the tool held (#88 UNKNOWN)
turns = sorted(PG, key=lambda t: t["pick"]); tturns = sorted(TS, key=lambda t: t["pick"])
own = {p["n"]: p["player"] for p in recap if p["slot"] == 10}
assert [t["pick"] for t in turns] == sorted(own) == [t["pick"] for t in tturns]
assert all(t["actual"] == own[t["pick"]] for t in turns) and all(t["actual"] == own[t["pick"]] for t in tturns)
tgt = lambda t: next(r["n"] for r in t["rows"] if r["target"])
followed = [t for t in turns if t["actualCardRank"] == 1]; top5 = [t for t in turns if t["actualCardRank"] <= 5]
tfollowed = [t for t in tturns if t["actualCardRank"] == 1]; ttop5 = [t for t in tturns if t["actualCardRank"] <= 5]
differ = [(a, b) for a, b in zip(turns, tturns) if [r["n"] for r in a["rows"]] != [r["n"] for r in b["rows"]] or a["actualCardRank"] != b["actualCardRank"]]
assert [a["pick"] for a, _ in differ] == [135, 154], [a["pick"] for a, _ in differ]
tdiff = [(a, b) for a, b in differ if tgt(a) != tgt(b)]
assert [a["pick"] for a, _ in tdiff] == [154] and tgt(tdiff[0][1]) == own[154] and tgt(tdiff[0][0]) == "Tari Eason"
# ---- the echoes: the paste's eight lines = the v65 page replaying the owner's tool log, byte for byte
echo_lines = [l.strip() for l in msg.split("\n") if l.startswith("⚠ off the card")]
dom_echo = [l.strip() for r in DOM["rows"] for l in r["fresh"] if "off the card" in l]
assert len(echo_lines) == 8 and dom_echo == echo_lines
S = DOM["summary"]; assert S["echoMisses"] == 0 and S["clockMismatches"] == 0 and S["pageErrors"] == 0 and S["finalPicks"] == 156
ev = J("/home/user/yahoo-fantasy-basketball/arena/data/events/m78_tool_events.json")
nfeed = sum(1 for e in ev if e["op"] == "feed"); nunk = sum(1 for e in ev if e.get("expect") == "UNKNOWN")
nfix = sum(1 for e in ev if e["op"] == "feed" and re.match(r"\d+- ", e["text"])); nins = sum(1 for e in ev if e["op"] == "insert"); nundo = sum(1 for e in ev if e["op"] == "undo")
# the seven echoes about picks the owner kept agree with the tool-state card (rank and 🎯)
E = re.findall(r"⚠ off the card: (.+?) ranks #(\d+) \(([\d.]+) behind 🎯 (.+?)\)", msg)
kept = [e for e in E if e[0] in own.values()]
assert len(kept) == 7 and all(int(rk) == next(t for t in tturns if t["actual"] == nm)["actualCardRank"] and tg == tgt(next(t for t in tturns if t["actual"] == nm)) for nm, rk, g, tg in kept)
port_diff = [(r["pick"], r["actual_ds_rank"], next(t for t in turns if t["pick"] == r["pick"])["actualCardRank"]) for r in RP
             if r["actual_ds_rank"] != next(t for t in turns if t["pick"] == r["pick"])["actualCardRank"]]
# ---- grades
ad = A["as_drafted"]; fc = A["follow_card_selfconsistent"]
swaps = sorted(((k.split(":", 1)[1], int(k.split(":")[0][5:]), v["champ"]) for k, v in A.items() if k.startswith("swap#")), key=lambda x: -x[2])
ECW = F["ecw"]["T10"] if "T10" in F["ecw"] else F["ecw"]["10"]; ECWR = F["ecw_rank"]; WW = F["exp_winning_weeks"]
ecw_by = {int(str(k).lstrip("T")): v for k, v in F["ecw"].items()}
lead = max(ecw_by, key=ecw_by.get); assert lead == 1 and ECWR == 2, (lead, ECWR)
best = swaps[0]; assert best[1] == 10 and best[0] == "Jalen Johnson", best
hb = {t["pick"]: t for t in HS["turns"]}
assert hb[10]["top"][0]["n"] == "Jalen Johnson"
JJ = A["swap#10:Jalen Johnson"]
assert next(t for t in turns if t["pick"] == 10)["rows"][1]["n"] == "Jalen Johnson"
ALL = {}
for f in glob.glob(f"{D}/m*_arms.json"):
    mm = re.fullmatch(r"m(\d+)_arms\.json", os.path.basename(f))
    if mm and int(mm.group(1)) != 78:
        a = J(f).get("as_drafted")
        if a: ALL[int(mm.group(1))] = a["champ"]
live10 = {m: ALL[m] for m in (67, 68, 73, 74, 75, 77) if m in ALL}
reldiff = max(abs(YC[s]["yahoo_file_sum"]["pts"] - YC[s]["screenshot"]["pts"]) / YC[s]["screenshot"]["pts"] for s in YC)
# ---- Yahoo standings: roto points recomputed reproduce the printed ranks; head to head on the same totals
cats = [("fg_pct", 1), ("ft_pct", 1), ("tpm", 1), ("pts", 1), ("reb", 1), ("ast", 1), ("stl", 1), ("blk", 1), ("tov", -1)]
pts = {r["manager"]: 0.0 for r in YS}
for c, s in cats:
    v = [(float(r[c]) * s, r["manager"]) for r in YS]
    for x, m in v: pts[m] += sum(1 for y, _ in v if y < x) + 1 + (sum(1 for y, _ in v if y == x) - 1) / 2
for r in YS:
    m = r["manager"]; rk = sum(1 for x in pts.values() if x > pts[m]) + 1 + (sum(1 for x in pts.values() if x == pts[m]) - 1) / 2
    assert rk == float(r["rank"]), (m, rk, r["rank"])
me = next(r for r in YS if r["manager"] == "David"); y1 = next(r for r in YS if r["rank"] == "1")
assert me["rank"] == "2" and y1["manager"] == mgr[1]
def h2h(r):
    wn = ls = 0
    for c, s in cats:
        a, b = float(me[c]) * s, float(r[c]) * s
        wn += a > b; ls += a < b
    return wn, ls
rows = [(r["manager"], *h2h(r)) for r in YS if r["manager"] != "David"]
fav = sum(1 for _, a, b in rows if a > b); lost = [(m, a, b) for m, a, b in rows if a <= b]
s1, s10 = YC[1]["yahoo_file_sum"], YC[10]["yahoo_file_sum"]
pg = lambda t, c: t[c] / t["gp"]
ordn = lambda k: f"{k}{'th' if 10 <= k % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(k % 10, 'th')}"
lead_cats = [c for c in ("pts", "reb", "ast", "tpm", "stl", "blk") if pg(s1, c) > pg(s10, c)]
mine_cats = [c for c in ("pts", "reb", "ast", "tpm", "stl", "blk") if pg(s10, c) > pg(s1, c)]
CN = {"pts": "points", "reb": "rebounds", "ast": "assists", "tpm": "threes", "stl": "steals", "blk": "blocks"}
# ---- the owner's question: the six
SIX = ["Jalen Williams", "Payton Pritchard", "OG Anunoby", "Chet Holmgren", "Anthony Davis", "Karl-Anthony Towns"]
before, wo5, mgp, v64, v65 = SL[0], SL[2], SL[3], SL[5], SL[6]
assert before["rev"] == "df1c754" and wo5["rev"] == "8ec736b" and mgp["rev"] == "73e832c" and v64["rev"] == "f6fb476" and v65["rev"] == "dd6b719"
line = lambda v, n: v["players"][n]["line"]
moved_at = {n: [v["label"] for v, w in zip(SL, SL[1:]) if line(v, n) != line(w, n)] for n in SIX}
assert all(moved_at[n] == ["v59 ADP 10/12"] for n in SIX if n != "Jalen Williams"), moved_at  # label of the version BEFORE the change
assert moved_at["Jalen Williams"] == ["v59 ADP 10/12", "v60 WO-5 re-derive"], moved_at
assert all(line(v64, n) == line(v65, n) for n in SIX)  # the dial pass (v65) wrote none of the six
assert wo5["lines_changed_vs_previous"] == 326
YQ = {r["player"]: r for r in csv.DictReader(open(os.path.join(K, "report", "market", "yahoo-proj-2026-10-13.csv"), encoding="utf-8-sig"))}
SV = SC["versions"]; v59c, v60c, v65c = SV["v59"], SV["v60 WO-5"], SV["v65"]
assert v65c["top5"]["Chet Holmgren"] + v65c["top5"]["Anthony Davis"] > v65c["six_top5_total"] / 2
assert v60c["six_target_total"] <= 5 and all(v["six_target_total"] <= 5 for k, v in SV.items() if k != "v59") and v59c["six_target_total"] > 100
T10, P58 = v59c["target_by_pick"]["Karl-Anthony Towns #10"], v59c["target_by_pick"]["Payton Pritchard #58"]
assert v59c["owner_turns"] == v65c["owner_turns"]
NT = v59c["owner_turns"]
import hashlib, subprocess
def blocks(rev):
    h = subprocess.run(["git", "-C", "/home/user/yahoo-fantasy-basketball", "show", f"{rev}:docs/draft-deck.html"], capture_output=True, text=True, check=True).stdout
    g = lambda tag: hashlib.sha256(re.search(r'<script id="%s">(.*?)</script>' % tag, h, re.S).group(1).encode()).hexdigest()[:12]
    return g("engine"), g("data")
BL = {lab: blocks(v["rev"]) for lab, v in SV.items()}
ENG = {e for e, _ in BL.values()}; assert len(ENG) == 1 and len({d for _, d in BL.values()}) == len(BL); ENG = ENG.pop()
o = []; w = o.append
w("# After-report — draft_78: the second 10/13 late live room from slot 10, on deck Version 65; Yahoo's projected standings beside ours; why six players left the card\n")
w("**Owner request (2026-10-13 late, verbatim):** \"Another live mock:\" — the deck tool's LIVE feed, a screenshot of Yahoo's 2026-27 projected standings for the room, the owner's 13-man roster and Yahoo's round-by-round recap. **Follow-up while it was graded (2026-10-14, verbatim):** \"I also have a question. Prior to our work today in stat projections, almost the same players were suggested at a heavy clip, which aren't even on the card now. Curious of what changed in the logic/arithmetic where they are no longer being suggested? Jalen Williams, Pritchard, OG, Chet Holmgren, Anthony Davis, Towns\"\n")
w(f"**Room:** public Yahoo mock, 12 × 13, owner seat 10 (random humans; a practice rep, not opponent intel; display names: " + ", ".join(f"{s} {mgr[s]}" for s in range(1, 13)) + "). **Deck used:** Version 65 (rev `dd6b719`, the dial pass; Porziņģis veto live). Replaying the owner's tool log through the v65 page reproduces all eight \"off the card\" lines of the paste character for character.\n")
w("Pull window: 2026-10-13 → 2026-10-13 (analysis only, written after midnight on 10/14; no roster pull; the planes are held for this morning's final pull by the owner's decision).\n")
w(f"**Headline.** As drafted **{ad['champ']:.2f} percent** for the title on the real eight-team bracket, rank {ad['champ_rank']} of 12, playoffs {ad['playoff']:.2f} percent. Expected weekly category wins {ECW:.3f}, rank {ECWR} of 12 behind seat 1 ({mgr[1]}, {ecw_by[1]:.3f}), favored in {WW} of 11 head-to-heads. Yahoo's projected standings agree on the order: this roster second, {mgr[1]} first. Following the card's 🎯 from the same seat (the self-consistent chain) grades {fc['champ']:.2f} percent. The costly turn was the first one: #10 Tyrese Haliburton, card #9; Jalen Johnson (card #2, gone at #12) grades {JJ['champ']:.2f} percent as a single swap, {JJ['champ'] - ad['champ']:+.2f} points. One pick was never fixed in the tool: #88 stayed UNKNOWN (\"Chite\" = Coby White), so the tool's card at #135 and #154 was computed on a board that still listed him; it changed one 🎯 (#154: Vassell shown, Tari Eason on the true board, worth {hb[154]['card1_gain']:+.4f} weekly category wins). **The six players:** none of their lines changed in the dial pass of 10/13; all six fell on 10/12 when WO-5 rebuilt every line on the 2025-26 season — Davis #{before['players']['Anthony Davis']['adj_rank']} → #{v65['players']['Anthony Davis']['adj_rank']}, Towns #{before['players']['Karl-Anthony Towns']['adj_rank']} → #{v65['players']['Karl-Anthony Towns']['adj_rank']}, Holmgren #{before['players']['Chet Holmgren']['adj_rank']} → #{v65['players']['Chet Holmgren']['adj_rank']}, Jalen Williams #{before['players']['Jalen Williams']['adj_rank']} → #{v65['players']['Jalen Williams']['adj_rank']}, Anunoby #{before['players']['OG Anunoby']['adj_rank']} → #{v65['players']['OG Anunoby']['adj_rank']}, Pritchard #{before['players']['Payton Pritchard']['adj_rank']} → #{v65['players']['Payton Pritchard']['adj_rank']} (§6). On the same {NT} owner turns of 27 graded rooms, the six were the card's 🎯 {v59c['six_target_total']} times on the last page before WO-5 and {v65c['six_target_total']} times on Version 65.\n")
w("## 1. Roster changes\n\nNone. No line, tag, placement or price changed on either plane; this is a grade of a practice room and an answer to a question.\n")
w("## 2. The team, graded\n\nEVIDENCE: `arena/results/m78_final.json`, `m78_arms.json` (18,000 seasons per arm, seeds 11/23/47, the real eight-team bracket), pool tag v65 = `players_v65.csv` (data/players.csv at `dd6b719`, sha256 bd2b983876a8).\n")
w("| arm | title % | playoffs % | rank |\n|---|---|---|---|")
w(f"| as drafted | {ad['champ']:.2f} | {ad['playoff']:.2f} | {ad['champ_rank']} |")
w(f"| follow the card's 🎯 at every turn (self-consistent chain: " + ", ".join(f"#{n} {p}" for n, p in fc["swaps"]) + f") | {fc['champ']:.2f} | {fc['playoff']:.2f} | {fc['champ_rank']} |")
for nm, n, c in swaps: w(f"| single swap at #{n}: {nm} | {c:.2f} | {A[f'swap#{n}:{nm}']['playoff']:.2f} | {A[f'swap#{n}:{nm}']['champ_rank']} |")
CR = F["cat_rank_weekly"]; assert CR["FT%"] == CR["BLK"] == CR["TO"] == 1 and CR["PTS"] == 12 and CR["REB"] == CR["AST"] == 10, CR
w("\nCategory shape (weekly model, rank of 12): " + ", ".join(f"{c} {r}" for c, r in CR.items()) + ". A defensive, efficient build: first in free throws, blocks and turnovers; last in points, tenth in rebounds and assists.\n")
w("For scale, the other live public rooms graded on this bracket: " + ", ".join(f"mock {m} {c:.2f}" for m, c in sorted(live10.items())) + ".\n")
w("## 3. Pick by pick: the page's card, the owner, hindsight\n\nEVIDENCE: `m78_deckcard_v65.json` (the v65 page's own engine on the true board, Yahoo's recap), `m78_deckcard_v65_toolstate.json` (the same engine on the board the tool held: #88 UNKNOWN, Aaron Gordon inserted at #119 after #123 was fed), `m78_hindsight.json` (every single-swap alternative scored by weekly category wins against the final rosters).\n")
w("| pick | owner took | card rank (true board) | the page's 🎯 | what the tool showed, if different | hindsight's best alternative (Δ weekly cat wins) |\n|---|---|---|---|---|---|")
tsb = {t["pick"]: t for t in tturns}
for t in turns:
    h = hb[t["pick"]]["top"][0]; u = tsb[t["pick"]]
    shown = "" if ([r["n"] for r in t["rows"]] == [r["n"] for r in u["rows"]] and t["actualCardRank"] == u["actualCardRank"]) else f"rank {u['actualCardRank']}, 🎯 {tgt(u)}"
    w(f"| #{t['pick']} | {t['actual']} | {t['actualCardRank']} | {tgt(t)} | {shown} | {h['n']} ({h['gain']:+.3f}) |")
wide = [(t["pick"], t["actualCardRank"]) for t in turns if t["actualCardRank"] > 5]
assert wide == [(10, 9), (58, 27), (82, 11), (87, 6)], wide
assert tgt(next(t for t in turns if t["pick"] == 58)) == "Kel'el Ware" == own[63]
d54 = [l for l in echo_lines if "round-9+ rule" in l]; assert len(d54) == 3 and "Anthony Black" in d54[-1] and tgt(tsb[154]) == own[154]
w(f"\nOn the true board the owner took the 🎯 at {len(followed)} of 13 turns and stayed in the Top 5 at {len(top5)}; on the card the tool actually showed, {len(tfollowed)} and {len(ttop5)}. The turns outside the Top 5 were " + ", ".join(f"#{p} {own[p]} (card #{r})" for p, r in wide) + "; at #58 the 🎯 Kel'el Ware lasted to #63 and was taken there. From round 9 on, the D54-1 line (\"take the 🎯\") fired three times; the owner followed it once, at #154 after undoing Anthony Black.\n")
w("## 4. Yahoo's projected standings against ours\n\nEVIDENCE: `yahoo_standings_2026-10-13.csv` (the screenshot transcribed; recomputing roto points from its 12 rows reproduces Yahoo's printed ranks, the 7.5 tie included), `yahoo_compare.json` (each roster summed on Yahoo's per-player file of 10/13), `m78_final.json`.\n")
w(f"| view | where this roster lands |\n|---|---|\n| Yahoo, season-total roto points | {me['rank']} of 12 (behind {y1['manager']}, seat 1) |\n| Yahoo totals, head to head category by category | favored against {fav} of 11; loses to " + ", ".join(f"{m} ({a}-{b})" for m, a, b in lost) + " |\n" + f"| the deck, weekly category model | rank {ECWR} of 12 behind seat 1, favored against {WW} of 11 |")
wins1 = [c for c, s_ in cats if float(me[c]) * s_ > float(y1[c]) * s_]; assert wins1 == ["fg_pct", "ft_pct", "blk", "tov"], wins1
w(f"\nBoth views put seat 1 ({mgr[1]}) first and this roster second. Unlike mock 77, games played explain little of the gap: summed from Yahoo's per-player file seat 1 carries {s1['gp']:.0f} projected games against this roster's {s10['gp']:.0f}. Per player-game seat 1 leads in " + ", ".join(CN[c] for c in lead_cats) + (("; this roster in " + ", ".join(CN[c] for c in mine_cats)) if mine_cats else "") + f". Against seat 1 on Yahoo's totals this roster wins both percentages, blocks and turnovers and loses the other five: the shape §2 shows. Summing Yahoo's 10/13 per-player file comes within {100*reldiff:.1f} percent of the screenshot's points for every team but does not equal it (the deck pool's \"Cameron Johnson\" is \"Cam Johnson\" in Yahoo's file, aliased), so the screenshot rests on a slightly newer Yahoo projection than the file on hand.\n")
w(f"## 5. Tool-state integrity\n\n" + sc.strip().replace("\n", "; ") + f". The owner's tool log as pinned in `arena/data/events/m78_tool_events.json` ({len(ev)} events: {nfeed} feeds, {nunk} of them raw texts that resolved to UNKNOWN (\"Tati,\", \"<axeu\", \"Chite\") and {nfix} numbered fixes (#7 Tatum, #8 Maxey); {nins} insert (Aaron Gordon at #119, sent after #123); {nundo} undo (Anthony Black at #154)) replayed through the v65 page in headless Chromium: {S['echoMisses']} echo misses, {S['clockMismatches']} clock mismatches, {S['pageErrors']} page errors, {S['finalPicks']} picks; the eight \"off the card\" lines equal the paste's. Its final board differs from Yahoo's recap at #88 only (`UNKNOWN #88` vs Coby White), the one fix never sent; the tool warned once (\"#88 is still UNKNOWN\").\n")
w(f"What the open UNKNOWN did: with Coby White still listed and seat 9's roster one guard short, the card from #88 on was computed on a slightly different board. It matched the true board's card at {13 - len(differ)} of 13 owner turns; at #135 Tre Jones showed as #3 (true board #5) and at #154 the 🎯 was Vassell (true board: Tari Eason, Vassell #3). The grade above uses the true board. The grading pipeline's Python port, which keeps the pre-v24 name tie-break and does not apply the page's priced-only rule from round 11, differs from the page record at {len(port_diff)} turns ({', '.join(f'#{p}: port {a}, page {b}' for p, a, b in port_diff)}); the page record is the authority for what the card said.\n")
# ---- §6
w("## 6. The owner's question: why Jalen Williams, Pritchard, Anunoby, Holmgren, Davis and Towns left the card\n")
w("EVIDENCE: `six_lines.py` → `six_lines.json` (the six per-game lines as shipped in the deck's data/players.csv at each version on main from the 10/12 morning pull to Version 65, and the deck's own value math run on each version's pool; two runs identical), `six_cards.py` → `six_cards.json` (per-run cards in the deck at `arena/results/six_cards_2026-10-14/`; the same 27 graded draft states replayed through five page versions with each page's own engine, so the rooms are held fixed and only the page changes), `after-report-2026-10-12-wo5.md` (the method), `report/market/yahoo-proj-2026-10-13.csv` (Yahoo's ranks and ADP of 10/13).\n")
w(f"**What changed.** Not the engine and not the card's arithmetic: the page's engine block (the z-scores, the weekly category model, the card's ordering) is byte-identical on all five pages in the card table below (sha256 {ENG}); only the data block differs." + " What changed is the input: on 10/12 the WO-5 pass rebuilt " + f"{wo5['lines_changed_vs_previous']}" + " deck lines on each player's 2025-26 production rate at his 2025-26 minutes (shooting pulled a third of the way to career, steals and blocks averaged over three seasons, points from the shooting identity; returnees' minutes from the outside projections). Before it, most of the board's stars carried 2024-25-shaped lines. The six are players whose 2025-26 season ran below the line they carried. The minutes-and-games pass that night changed only Jalen Williams among them (his minutes up); the dial pass of 10/13 (Version 65) changed none of them.\n")
w("| player | line before WO-5 (pts / reb / ast / stl / blk / 3pm / to, FG% / FT%) | line now | value rank before → after WO-5 → Version 65 | Yahoo rank / ADP (source: `yahoo-proj-2026-10-13.csv`; lines: the deck's data/players.csv) |\n|---|---|---|---|---|")
fl = lambda L: f"{L['pts']:.1f} / {L['reb']:.1f} / {L['ast']:.1f} / {L['stl']:.1f} / {L['blk']:.1f} / {L['tpm']:.1f} / {L['tov']:.1f}, {L['fg_pct']:.3f} / {L['ft_pct']:.3f}"
for n in SIX:
    y = YQ[n]
    w(f"| {n} | {fl(line(before, n))} | {fl(line(v65, n))} | {before['players'][n]['adj_rank']} → {wo5['players'][n]['adj_rank']} → {v65['players'][n]['adj_rank']} | {y['xrank']} / {float(y['adp']):.1f} |")
w("\nWhere each one's value went (z-score change, before WO-5 → Version 65, the three largest):\n")
for n in SIX:
    za, zb = before["players"][n]["z"], v65["players"][n]["z"]
    d = sorted(((k, zb[k] - za[k]) for k in za), key=lambda x: abs(x[1]), reverse=True)[:3]
    w(f"- {n}: " + ", ".join(f"{k} {v:+.2f}" for k, v in d) + f" (total {sum(zb.values()) - sum(za.values()):+.2f}).")
w(f"\n**On the card, rooms held fixed.** The same {NT} owner turns of 27 graded rooms (mocks {SC['mocks'][0]}–{SC['mocks'][-1]} with a state on file), each turn's card computed by each page's own engine:\n")
w("| page | " + " | ".join(SIX) + " | all six |\n|---|" + "---|" * (len(SIX) + 1))
for lab, v in SV.items():
    w(f"| {lab} (`{v['rev']}`) | " + " | ".join(f"🎯 {v['target'][n]}, Top 5 {v['top5'][n]}" for n in SIX) + f" | 🎯 {v['six_target_total']}, Top 5 {v['six_top5_total']} |")
w(f"\nThe drop happens at one step, v59 → v60 (WO-5): the six go from 🎯 {v59c['six_target_total']} and Top 5 {v59c['six_top5_total']} to 🎯 {v60c['six_target_total']} and Top 5 {v60c['six_top5_total']}; the later pages move them by little. They have not vanished: on Version 65 they still reach the Top 5 {v65c['six_top5_total']} times, {v65c['top5']['Chet Holmgren'] + v65c['top5']['Anthony Davis']} of them Holmgren and Davis, whose new value still sits above where Yahoo ranks and drafts them. The old page's heaviest habit was Towns as the 🎯 at #10 ({T10} of 27 rooms) and Pritchard at #58 ({P58} of 27).\n")
FIVE = ["Anthony Davis", "Chet Holmgren", "Jalen Williams", "OG Anunoby", "Payton Pritchard"]
br = lambda n: before["players"][n]["adj_rank"]; nr = lambda n: v65["players"][n]["adj_rank"]; xr = lambda n: int(YQ[n]["xrank"]); ap = lambda n: float(YQ[n]["adp"])
assert all(br(n) < min(xr(n), ap(n)) - 5 for n in FIVE)  # the old board ran well ahead of the market on all five
near = [n for n in FIVE if abs(nr(n) - min(xr(n), ap(n))) <= 5]; above = [n for n in FIVE if nr(n) < min(xr(n), ap(n)) - 5]
assert near == ["Jalen Williams", "Payton Pritchard"] and above == ["Anthony Davis", "Chet Holmgren", "OG Anunoby"], (near, above)
T_ = "Karl-Anthony Towns"; assert nr(T_) > max(xr(T_), ap(T_))
w("**Was the old board or the new one right?** Against the market, the old board was the outlier: before WO-5 it valued " + ", ".join(f"{n.split()[-1]} {ordn(br(n))}" for n in FIVE) + ", where Yahoo's 10/13 projected rank has them " + ", ".join(f"{xr(n)}" for n in FIVE) + " and the market drafts them around " + ", ".join(f"{ap(n):.0f}" for n in FIVE) + f" (ADP). Now Jalen Williams and Pritchard sit at the market, Davis, Holmgren and Anunoby still above it, and Towns below it ({ordn(nr(T_))} against Yahoo's {ordn(xr(T_))}, ADP {ap(T_):.1f}). Towns is the one where our line is lower than the market's: his 2025-26 season (20.2 points in 31 minutes) is the basis; the 10/12 Towns report and WO-5 §4 carry the full derivation. The one out-of-sample season on record cuts the other way for the method as a whole: a copy of the prior season had more error than pre-season projections in 8 of 9 categories (`after-report-2026-10-09-market.md` §4, cited in the dial report), which is why D-C2 (a blend with a usage model) is set for after the draft.\n")
w("## Watchlist\n")
w("- An UNKNOWN left open changes the board the card computes on. In the real draft, send the `N- Name` fix as soon as the warning shows; here it moved one 🎯 by a small margin.")
w("- Haliburton at #10: card #9 in this room; Jalen Johnson, card #2, was the better pick by a full grade.")
w("- The 10/14 lock paste (D-1013-1), the publish freeze during the draft (D-1013-5), no RESYNC during the draft (D-1013-2).\n")
w("## Open-item receipts\n\n| item | query run (2026-10-13/14) | dated finding |\n|---|---|---|")
w("| (this room) | records only; no web research and no roster pull | the room's names resolve to the v65 pool 156 of 156; the lines are the ones merged in kit PR #109 |")
w("| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull (`after-report-2026-10-13.md`, receipts dated 10/13) | all HELD or unsigned on 2026-10-13 per those receipts; not re-queried here (did not check) |\n")
w(rn + "\n")
w("\n## Bounds\n\n**Out of scope by design.**\n- No line, price or engine change: the owner holds every decision until this morning's final pull. §6 is an assessment; it builds no candidate line.\n- The punt test and the advice line were not re-run: no punt was declared and no advisor click is in the feed.\n- This is a room of random humans, not the league's managers.\n")
NEAR = sum(1 for n in SIX if abs(v65["players"][n]["adj_rank"] - int(YQ[n]["xrank"])) < abs(before["players"][n]["adj_rank"] - int(YQ[n]["xrank"])))
assert NEAR == 6, NEAR
w(f"**In scope and unverified.**\n- The exact Yahoo projection behind the screenshot: `UNVERIFIABLE` from here; the 10/13 per-player file on hand sums to within {100*reldiff:.1f} percent of it but not exactly.\n- The raw text the owner typed for picks the tool resolved by surname (\"assumed over\" lines) is not in the paste; the pinned events feed the resolved names. The echoes and the final board match, so the state is the same; the typed strings are `UNVERIFIABLE`.\n- Whether the season arms' title share holds against the league's real managers: `UNVERIFIABLE` until the draft.\n- Whether WO-5's 2025-26 basis or the pre-WO-5 lines are closer to the 2026-27 outcome for these six: `UNVERIFIABLE` until the season; Yahoo's projected rank sits nearer the new board than the old for all {NEAR} (§6).\n")
w("## Decision sheet (owner disposes)\n\n| id | decision question | default if silent |\n|---|---|---|")
w("| D-1013-10..14 | carried as set; the owner's hold until this morning's final pull | hold |")
w("| D-1013-1..9, D-C2, D-SF-1..4 and earlier | carried | carried |\n")
w("## Provenance\n")
w("- Inputs: the owner's paste (`draft78-2026-10-13/owner_message.txt`, verbatim) and the screenshot (`yahoo_standings_screenshot.webp`, transcribed to `yahoo_standings_2026-10-13.csv`); deck rev `dd6b719` (Version 65, page sha256 09a889d4baa5); deck revs `df1c754`, `f918062`, `8ec736b`, `73e832c`, `3bd8311`, `f6fb476` for §6.")
w("- Tools: `build_state.py` (state and feed check; handles the UNKNOWN and `✎ #N corrected` lines), the deck's `arena/mocks/live_retro.py` (mock 78 registered: replay, final, hindsight, arms), `live_deckcard.py` (the page's engine; the tool-state run reads the DOM replay's final board through a copy whose only change is the state path), `live_replay_dom.mjs` (the tool log through the real page), `scripts/repeat_market_check.py` (27 mocks), `yahoo_compare.py`, `six_lines.py`, `six_cards.py`, `write_report.py` (this file's writer). Records in `arena/results/m78_*.json` and this folder.")
w("- No line, tag or placement changed; both planes' hashes equal before and after (e821ec1ddc67 kit, bd2b983876a8 deck).\n")
w("## In plain language\n")
w(f"**How the room went.** A good room, not your best: about a {ad['champ']:.0f} percent title share, second of 12, favored against {WW} of the other 11 week to week. Yahoo agrees: second, behind {mgr[1]}.")
w(f"\n**The pick to learn from.** The first one. At #10 you took Haliburton, ninth on the card; Jalen Johnson, second on it, went two picks later, and with him the roster grades about {JJ['champ'] - ad['champ']:.0f} title points better.")
w("\n**The UNKNOWN.** #88 never got fixed, so late in the draft the tool still thought Coby White was available. It changed one late suggestion slightly. In the real draft, fix an UNKNOWN as soon as the warning shows.")
w("\n**Your question.** The engine didn't change; the numbers it is fed did. On 10/12 every player's line was rebuilt from last season (2025-26). These six had weaker 2025-26 seasons than the older lines assumed, so their values fell: " + f"Towns from {ordn(br(T_))} to {ordn(nr(T_))}, Davis {ordn(br('Anthony Davis'))} to {ordn(nr('Anthony Davis'))}, Jalen Williams {ordn(br('Jalen Williams'))} to {ordn(nr('Jalen Williams'))}" + ". Before that, the card was pushing them well ahead of where Yahoo and the market rank them (replaying your 27 graded practice rooms on the last page before the rebuild, one of the six was the card's pick at " + f"{v59c['six_target_total']} of your {NT} turns; on today's page, at {v65c['six_target_total']}" + "). Holmgren and Davis still show up on the card when they're available.")
w("\n**Your decisions.** Nothing new; everything holds until this morning's final pull.")
P = os.path.join(K, "report", "after-reports", "after-report-2026-10-13-draft78.md")
open(P, "w", encoding="utf-8").write("\n".join(x for x in o if x is not None) + "\n")
PL = os.path.join(K, "report", "pull-log.md"); pl = rd(PL)
if "after-report-2026-10-13-draft78.md" not in pl:
    row = (f"| 2026-10-13 | mock 78 grade (public room, LIVE mode, deck Version 65) + Yahoo's projected standings + the owner's six-player question | 0 | 0 | 0 | "
           f"after-reports/after-report-2026-10-13-draft78.md — as drafted {ad['champ']:.2f}% (rank {ad['champ_rank']}), ECW {ECW:.3f} rank {ECWR} behind seat 1, favored {WW} of 11; "
           f"card followed {len(followed)} of 13 on the true board ({len(tfollowed)} on the tool's), Top-5 at {len(top5)}; follow-card chain {fc['champ']:.2f}%; the costly turn #10 Haliburton (Jalen Johnson swap {JJ['champ']:.2f}%); "
           f"feed = recap 155 of 156 (#88 left UNKNOWN), eight echoes reproduced by the page; Yahoo standings rank 2 behind seat 1, favored head to head against {fav} of 11 on Yahoo's totals; "
           f"six players: all fell at WO-5 (10/12), none touched by the dial; 🎯 {v59c['six_target_total']} → {v65c['six_target_total']} on {NT} fixed turns; repeat-name check 27 of 27; no plane change |")
    open(PL, "w", encoding="utf-8").write(pl.rstrip("\n") + "\n" + row + "\n")
print("written", P)
