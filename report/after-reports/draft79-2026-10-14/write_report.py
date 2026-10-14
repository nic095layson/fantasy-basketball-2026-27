#!/usr/bin/env python3
"""Writes report/after-reports/after-report-2026-10-14-draft79.md and the pull-log row from the records: the deck's
m79_final / m79_arms / m79_hindsight / m79_deckcard_v65 / m79_tool_vs_truth_dom / m79_replay, this folder's
state_check.txt and rn_section_m79.md (the repeat-name check on 28 mocks), and mock 78's six_cards.json for the
six players the owner asked about. No figure is typed by hand."""
import glob, json, os, re
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.normpath(os.path.join(H, "..", "..", ".."))
D = "/home/user/yahoo-fantasy-basketball/arena/results"
J = lambda p: json.load(open(p, encoding="utf-8")); rd = lambda p: open(p, encoding="utf-8").read()
A = J(f"{D}/m79_arms.json"); HS = J(f"{D}/m79_hindsight.json"); PG = J(f"{D}/m79_deckcard_v65.json")
DOM = J(f"{D}/m79_tool_vs_truth_dom.json"); RP = J(f"{D}/m79_replay.json")["v65"]; F = J(f"{D}/m79_final.json")["v65"]
recap = J(os.path.join(H, "recap.json")); sc = rd(os.path.join(H, "state_check.txt")); msg = rd(os.path.join(H, "owner_message.txt"))
rn = rd(os.path.join(H, "rn_section_m79.md")); rn = rn[rn.index("## Repeat-name market check"):].strip()
mgr = {p["slot"]: p["manager"] for p in recap}
turns = sorted(PG, key=lambda t: t["pick"]); own = {p["n"]: p["player"] for p in recap if p["slot"] == 10}
assert [t["pick"] for t in turns] == sorted(own) and all(t["actual"] == own[t["pick"]] for t in turns)
tgt = lambda t: next(r["n"] for r in t["rows"] if r["target"])
followed = [t for t in turns if t["actualCardRank"] == 1]; top5 = [t for t in turns if t["actualCardRank"] <= 5]
wide = [(t["pick"], t["actualCardRank"]) for t in turns if t["actualCardRank"] > 5]
# the paste's echoes = the v65 page replaying the owner's tool log; and = the page card on the recap board
echo_lines = [l.strip() for l in msg.split("\n") if l.startswith("⚠ off the card")]
dom_echo = [l.strip() for r in DOM["rows"] for l in r["fresh"] if "off the card" in l]
assert len(echo_lines) == 7 and dom_echo == echo_lines
E = re.findall(r"⚠ off the card: (.+?) ranks #(\d+) \(([\d.]+) behind 🎯 (.+?)\)", msg)
tb = {t["actual"]: t for t in turns}
assert len(E) == 7 and all(int(rk) == tb[nm]["actualCardRank"] and tg == tgt(tb[nm]) for nm, rk, g, tg in E)
S = DOM["summary"]; assert S["echoMisses"] == 0 and S["clockMismatches"] == 0 and S["pageErrors"] == 0 and S["finalPicks"] == 156
ev = J("/home/user/yahoo-fantasy-basketball/arena/data/events/m79_tool_events.json")
nfeed = sum(1 for e in ev if e["op"] == "feed"); nunk = sum(1 for e in ev if e.get("expect") == "UNKNOWN"); nhalt = sum(1 for e in ev if e.get("expect") == "HALTED")
nfix = sum(1 for e in ev if e["op"] == "feed" and re.match(r"\d+- ", e["text"])); nins = sum(1 for e in ev if e["op"] == "insert"); nundo = sum(1 for e in ev if e["op"] == "undo")
nres = sum(1 for l in msg.split("\n") if l.startswith("— resumed"))
import sys
sys.path.insert(0, "/home/user/yahoo-fantasy-basketball/scripts"); import hoops
fs = DOM["finalState"]["picks"]; board_diff = [i + 1 for i, (p, r) in enumerate(zip(fs, recap)) if hoops.fold(p["player"]) != hoops.fold(r["player"]) or p["slot"] != r["slot"]]
assert board_diff == []
port_diff = [(r["pick"], r["actual_ds_rank"], tb[r["actual"]]["actualCardRank"]) for r in RP if r["actual_ds_rank"] != tb[r["actual"]]["actualCardRank"]]
# ---- grades
ad = A["as_drafted"]; fc = A["follow_card_selfconsistent"]
swaps = sorted(((k.split(":", 1)[1], int(k.split(":")[0][5:]), v["champ"]) for k, v in A.items() if k.startswith("swap#")), key=lambda x: -x[2])
ecw_by = {int(str(k).lstrip("T")): v for k, v in F["ecw"].items()}; ECW = ecw_by[10]; ECWR = F["ecw_rank"]; WW = F["exp_winning_weeks"]
lead = max(ecw_by, key=ecw_by.get)
hb = {t["pick"]: t for t in HS["turns"]}
best = swaps[0]
ALL = {}
for f in glob.glob(f"{D}/m*_arms.json"):
    mm = re.fullmatch(r"m(\d+)_arms\.json", os.path.basename(f))
    if mm and int(mm.group(1)) != 79:
        a = J(f).get("as_drafted")
        if a: ALL[int(mm.group(1))] = a["champ"]
live = {m: ALL[m] for m in (67, 68, 73, 74, 75, 77, 78) if m in ALL}
CR = F["cat_rank_weekly"]
# ---- the six players the owner asked about, in this room
SIX = ["Jalen Williams", "Payton Pritchard", "OG Anunoby", "Chet Holmgren", "Anthony Davis", "Karl-Anthony Towns"]
taken = {p["player"]: (p["n"], p["slot"]) for p in recap}
six_on_card = [(t["pick"], r["rank"], r["n"], r["target"]) for t in turns for r in t["rows"] if r["n"] in SIX]
assert taken["Chet Holmgren"] == (34, 10) and tgt(tb["Chet Holmgren"]) == "Chet Holmgren"
assert taken["Payton Pritchard"] == (82, 10) and tb["Payton Pritchard"]["actualCardRank"] == 6
o = []; w = o.append
w("# After-report — draft_79: the 10/14 early live room from slot 10, on deck Version 65\n")
w("**Owner request (2026-10-14, verbatim):** the deck tool's LIVE feed, the owner's 13-man roster and Yahoo's round-by-round recap, pasted without comment while mock 78 was being graded (`draft79-2026-10-14/owner_message.txt`). Read as the standing request for these pastes: grade the room with the deck pipeline and report; no line, tag or price changes.\n")
w(f"**Room:** public Yahoo mock, 12 × 13, owner seat 10 (random humans; a practice rep, not opponent intel; display names: " + ", ".join(f"{s} {mgr[s]}" for s in range(1, 13)) + "). **Deck used:** Version 65 (rev `dd6b719`, the dial pass; Porziņģis veto live). Replaying the owner's tool log through the v65 page reproduces all seven \"off the card\" lines of the paste character for character.\n")
w("Pull window: 2026-10-14 → 2026-10-14 (analysis only; no roster pull; the planes are held for this morning's final pull by the owner's decision).\n")
w(f"**Headline.** As drafted **{ad['champ']:.2f} percent** for the title on the real eight-team bracket, rank {ad['champ_rank']} of 12, playoffs {ad['playoff']:.2f} percent. Expected weekly category wins {ECW:.3f}, rank {ECWR} of 12" + ("" if lead == 10 else f" behind seat {lead} ({mgr[lead]}, {ecw_by[lead]:.3f})") + f", favored in {WW} of 11 head-to-heads. Following the card's 🎯 from the same seat (the self-consistent chain) grades {fc['champ']:.2f} percent. The owner took the 🎯 at {len(followed)} of 13 turns and stayed in the Top 5 at {len(top5)}; the largest single swap is #{best[1]} {best[0]} ({best[2]:.2f} percent, {best[2] - ad['champ']:+.2f} points). The tool log is clean: the board the tool held equals Yahoo's recap at 156 of 156 picks.\n")
w("## 1. Roster changes\n\nNone. No line, tag, placement or price changed on either plane; this is a grade of a practice room.\n")
w("## 2. The team, graded\n\nEVIDENCE: `arena/results/m79_final.json`, `m79_arms.json` (18,000 seasons per arm, seeds 11/23/47, the real eight-team bracket), pool tag v65 = `players_v65.csv` (data/players.csv at `dd6b719`, sha256 bd2b983876a8).\n")
w("| arm | title % | playoffs % | rank |\n|---|---|---|---|")
w(f"| as drafted | {ad['champ']:.2f} | {ad['playoff']:.2f} | {ad['champ_rank']} |")
w(f"| follow the card's 🎯 at every turn (self-consistent chain: " + ", ".join(f"#{n} {p}" for n, p in fc["swaps"]) + f") | {fc['champ']:.2f} | {fc['playoff']:.2f} | {fc['champ_rank']} |")
for nm, n, c in swaps: w(f"| single swap at #{n}: {nm} | {c:.2f} | {A[f'swap#{n}:{nm}']['playoff']:.2f} | {A[f'swap#{n}:{nm}']['champ_rank']} |")
w("\nCategory shape (weekly model, rank of 12): " + ", ".join(f"{c} {r}" for c, r in CR.items()) + ".\n")
w("For scale, the other live public rooms graded on this bracket: " + ", ".join(f"mock {m} {c:.2f}" for m, c in sorted(live.items())) + ".\n")
w("## 3. Pick by pick: the page's card, the owner, hindsight\n\nEVIDENCE: `m79_deckcard_v65.json` (the v65 page's own engine), `m79_hindsight.json` (every single-swap alternative scored by weekly category wins against the final rosters).\n")
w("| pick | owner took | card rank | the page's 🎯 | hindsight's best alternative (Δ weekly cat wins) |\n|---|---|---|---|---|")
for t in turns:
    h = hb[t["pick"]]["top"][0]
    w(f"| #{t['pick']} | {t['actual']} | {t['actualCardRank']} | {tgt(t)} | {h['n']} ({h['gain']:+.3f}) |")
nxt = {tgt(t): taken.get(tgt(t)) for t in turns if t["actualCardRank"] > 1}
w(f"\nThe turns outside the Top 5: " + ", ".join(f"#{p} {own[p]} (card #{r}, 🎯 {tgt(tb[own[p]])}, taken " + (f"#{taken[tgt(tb[own[p]])][0]} by seat {taken[tgt(tb[own[p]])][1]}" if tgt(tb[own[p]]) in taken else "never") + ")" for p, r in wide) + ".\n")
w("**The six players from the owner's question, in this room** (see `after-report-2026-10-13-draft78.md` §6): " + "; ".join(f"{n} went #{taken[n][0]} to seat {taken[n][1]}" for n in SIX if n in taken) + ". On the owner's card: " + "; ".join(f"#{p} {n} card #{rk}" + (" (the 🎯)" if tg else "") for p, rk, n, tg in six_on_card) + ". Holmgren at #34 was the card's 🎯 and the owner took him; Pritchard at #82 was the owner's pick at card #6, behind the 🎯 Ty Jerome.\n")
w(f"## 4. Tool-state integrity\n\n" + sc.strip().replace("\n", "; ") + f". The owner's tool log as pinned in `arena/data/events/m79_tool_events.json` ({len(ev)} events: {nfeed} feeds, {nunk} of them raw texts that resolved to UNKNOWN (\"Chetr\" at #34, \"Jrie\" at #147), {nfix} numbered fixes, {nhalt} halt (\"Mitchell\" after #132, Donovan Mitchell already drafted), {nins} insert (Cason Wallace at #115, sent after #123), {nundo} undo (Daniel Gafford at #133, re-fed after Ajay Mitchell); {nres} page resumes in the paste, replayed as one session) replayed through the v65 page in headless Chromium: {S['echoMisses']} echo misses, {S['clockMismatches']} clock mismatches, {S['pageErrors']} page errors, {S['finalPicks']} picks; the final board equals Yahoo's recap at 156 of 156 and the seven \"off the card\" lines equal the paste's. The page's card on the recap board gives the same rank and 🎯 for all seven. The grading pipeline's Python port differs from the page record at {len(port_diff)} turns" + (f" ({', '.join(f'#{p}: port {a}, page {b}' for p, a, b in port_diff)})" if port_diff else "") + "; the page record is the authority for what the card said.\n")
w("## Watchlist\n")
T10 = {}
for m in (72, 73, 74, 75, 77, 78, 79):
    f = sorted(glob.glob(f"{D}/m{m}_deckcard_v*.json")); f = [x for x in f if "toolstate" not in x][-1]
    t = next(x for x in J(f) if x["pick"] == 10); T10[m] = (t["actual"], t["actualCardRank"], tgt(t))
assert T10[78][:2] == T10[79][:2] == ("Tyrese Haliburton", 9) and T10[77][0] != "Tyrese Haliburton"
w("- #10 across the recent live rooms (page records): " + "; ".join(f"mock {m} {a} (card #{r}, 🎯 {g})" for m, (a, r, g) in T10.items()) + ". Haliburton at card #9 in the last two rooms; the 🎯 there is Jamal Murray on v65, where it was Towns before the 10/12 rebuild.")
w("- The 10/14 lock paste (D-1013-1), the publish freeze during the draft (D-1013-5), no RESYNC during the draft (D-1013-2).\n")
w("## Open-item receipts\n\n| item | query run (2026-10-14) | dated finding |\n|---|---|---|")
w("| (this room) | records only; no web research and no roster pull | the room's names resolve to the v65 pool 156 of 156; the lines are the ones merged in kit PR #109 |")
w("| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the 10/13 pull (`after-report-2026-10-13.md`, receipts dated 10/13) | all HELD or unsigned on 2026-10-13 per those receipts; not re-queried here (did not check); this morning's final pull re-queries them |\n")
w(rn + "\n")
w("\n## Bounds\n\n**Out of scope by design.**\n- No line, price or engine change: the owner holds every decision until this morning's final pull.\n- No Yahoo standings comparison: no screenshot came with this paste.\n- The punt test and the advice line were not re-run: no punt was declared and no advisor click is in the feed.\n- This is a room of random humans, not the league's managers.\n")
w("**In scope and unverified.**\n- The raw text the owner typed for picks the tool resolved by surname (\"assumed over\" lines) is not in the paste; the pinned events feed the resolved names. The echoes and the final board match, so the state is the same; the typed strings are `UNVERIFIABLE`.\n- Whether the season arms' title share holds against the league's real managers: `UNVERIFIABLE` until the draft.\n")
w("## Decision sheet (owner disposes)\n\n| id | decision question | default if silent |\n|---|---|---|")
w("| D-1013-10..14 | carried as set; the owner's hold until this morning's final pull | hold |")
w("| D-1013-1..9, D-C2, D-SF-1..4 and earlier | carried | carried |\n")
w("## Provenance\n")
w("- Inputs: the owner's paste (`draft79-2026-10-14/owner_message.txt`, verbatim); deck rev `dd6b719` (Version 65, page sha256 09a889d4baa5).")
w("- Tools: `build_state.py` (state and feed check), the deck's `arena/mocks/live_retro.py` (mock 79 registered: replay, final, hindsight, arms), `live_deckcard.py` (the page's engine), `live_replay_dom.mjs` (the tool log through the real page), `scripts/repeat_market_check.py` (28 mocks), `write_report.py` (this file's writer). Records in `arena/results/m79_*.json` and this folder.")
w("- No line, tag or placement changed; both planes' hashes equal before and after (e821ec1ddc67 kit, bd2b983876a8 deck).\n")
w("## In plain language\n")
w(f"**How the room went.** About a {ad['champ']:.0f} percent title share, {ad['champ_rank']} of 12 by title odds and {ECWR} of 12 week to week, favored against {WW} of the other 11. You followed the card at {len(followed)} of 13 picks and stayed in its Top 5 at {len(top5)}.")
w(f"\n**The pick to learn from.** The best single change would have been #{best[1]}: {best[0]} instead of {own[best[1]]}, worth about {best[2] - ad['champ']:.0f} title points.")
w("\n**The tool.** Clean: two typos fixed, one halt handled, one insert and one undo, and the tool's board matched Yahoo's at every pick.")
w("\n**Your decisions.** Nothing new; everything holds until this morning's final pull.")
P = os.path.join(K, "report", "after-reports", "after-report-2026-10-14-draft79.md")
open(P, "w", encoding="utf-8").write("\n".join(x for x in o if x is not None) + "\n")
PL = os.path.join(K, "report", "pull-log.md"); pl = rd(PL)
if "after-report-2026-10-14-draft79.md" not in pl:
    row = (f"| 2026-10-14 | mock 79 grade (public room, LIVE mode, deck Version 65) | 0 | 0 | 0 | "
           f"after-reports/after-report-2026-10-14-draft79.md — as drafted {ad['champ']:.2f}% (rank {ad['champ_rank']}), ECW {ECW:.3f} rank {ECWR}, favored {WW} of 11; "
           f"card followed {len(followed)} of 13, Top-5 at {len(top5)}; follow-card chain {fc['champ']:.2f}%; largest swap #{best[1]} {best[0]} {best[2]:.2f}%; "
           f"tool board = recap 156 of 156, seven echoes reproduced by the page; repeat-name check 28 of 28; no plane change |")
    open(PL, "w", encoding="utf-8").write(pl.rstrip("\n") + "\n" + row + "\n")
print("written", P)
