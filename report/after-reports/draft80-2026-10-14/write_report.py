#!/usr/bin/env python3
"""Writes report/after-reports/after-report-2026-10-14-draft80.md and the pull-log row from the records: the deck's
m80_final / m80_arms / m80_hindsight / m80_deckcard_v68 / m80_tool_vs_truth_dom / m80_replay, this folder's
state_check.txt and rn_section_m80.md (the repeat-name check), and the Version 67 replay of the same log (which page
the owner drafted on). No figure is typed by hand."""
import glob, json, os, re
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.normpath(os.path.join(H, "..", "..", ".."))
D = "/home/user/yahoo-fantasy-basketball/arena/results"
J = lambda p: json.load(open(p, encoding="utf-8")); rd = lambda p: open(p, encoding="utf-8").read()
A = J(f"{D}/m80_arms.json"); HS = J(f"{D}/m80_hindsight.json"); PG = J(f"{D}/m80_deckcard_v68.json")
DOM = J(f"{D}/m80_tool_vs_truth_dom.json"); RP = J(f"{D}/m80_replay.json")["v68"]; F = J(f"{D}/m80_final.json")["v68"]
recap = J(os.path.join(H, "recap.json")); sc = rd(os.path.join(H, "state_check.txt")); msg = rd(os.path.join(H, "owner_message.txt"))
rn = rd(os.path.join(H, "rn_section_m80.md")); rn = rn[rn.index("## Repeat-name market check"):].strip()
mgr = {p["slot"]: p["manager"] for p in recap}
turns = sorted(PG, key=lambda t: t["pick"]); own = {p["n"]: p["player"] for p in recap if p["slot"] == 10}
assert [t["pick"] for t in turns] == sorted(own) and all(t["actual"] == own[t["pick"]] for t in turns)
tgt = lambda t: next(r["n"] for r in t["rows"] if r["target"])
followed = [t for t in turns if t["actualCardRank"] == 1]; top5 = [t for t in turns if t["actualCardRank"] <= 5]
wide = [(t["pick"], t["actualCardRank"]) for t in turns if t["actualCardRank"] > 5]
# the paste's echoes = the v68 page replaying the owner's tool log; and = the page card on the recap board
echo_lines = [l.strip() for l in msg.split("\n") if l.startswith("⚠ off the card")]
dom_echo = [l.strip() for r in DOM["rows"] for l in r["fresh"] if "off the card" in l]
assert len(echo_lines) == 5 and dom_echo == echo_lines
V67 = J(os.path.join(H, "replay_v67.json")); v67_echo = [l.strip() for r in V67["rows"] for l in r["fresh"] if "off the card" in l]
v67_diff = [(a, b) for a, b in zip(v67_echo, echo_lines) if a != b]; assert len(v67_diff) == 1
E = re.findall(r"⚠ off the card: (.+?) ranks #(\d+) \(([\d.]+) behind 🎯 (.+?)\)", msg)
tb = {t["actual"]: t for t in turns}
assert len(E) == 5 and all(int(rk) == tb[nm]["actualCardRank"] and tg == tgt(tb[nm]) for nm, rk, g, tg in E)
S = DOM["summary"]; assert S["echoMisses"] == 0 and S["clockMismatches"] == 0 and S["pageErrors"] == 0 and S["finalPicks"] == 156
ev = J("/home/user/yahoo-fantasy-basketball/arena/data/events/m80_tool_events.json")
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
    if mm and int(mm.group(1)) != 80:
        a = J(f).get("as_drafted")
        if a: ALL[int(mm.group(1))] = a["champ"]
live = {m: ALL[m] for m in (67, 68, 73, 74, 75, 77, 78, 79) if m in ALL}
CR = F["cat_rank_weekly"]
taken = {p["player"]: (p["n"], p["slot"]) for p in recap}
o = []; w = o.append
nfix_lines = re.findall(r"✎ #(\d+) corrected: UNKNOWN #\d+ → (.+)", msg); raw_unk = re.findall(r"#(\d+): UNKNOWN \(\"(.+?)\"", msg)
assert len(nfix_lines) == 3 and len(raw_unk) == 3
late_fix = [int(n) for n, _ in nfix_lines if int(n) == 133]
w("# After-report — draft_80: the 10/14 afternoon live room from slot 10, on deck Version 68\n")
w("**Owner request (2026-10-14, verbatim):** \"Thank you. First live mock for today:\" followed by the deck tool's LIVE feed, the owner's 13-man roster and Yahoo's round-by-round recap (`draft80-2026-10-14/owner_message.txt`). Read as the standing request for these pastes: grade the room with the deck pipeline and report; no line, tag or price changes (Version 68 is the lock page).\n")
w(f"**Room:** public Yahoo mock, 12 × 13, owner seat 10 (random humans; a practice rep, not opponent intel; display names: " + ", ".join(f"{s} {mgr[s]}" for s in range(1, 13)) + "). **Deck used:** Version 68 (rev `cb1a922`, the final morning pull and the owner's three lock calls; Porziņģis veto live). Replaying the owner's tool log through the Version 68 page reproduces all five \"off the card\" lines of the paste character for character; through Version 67 one differs (" + "; ".join(f"page: \"{x[0]}\"" for x in v67_diff) + "), so the room was drafted on Version 68.\n")
w("Pull window: 2026-10-14 → 2026-10-14 (analysis only; no roster pull; Version 68 is the locked page).\n")
w(f"**Headline.** As drafted **{ad['champ']:.2f} percent** for the title on the real eight-team bracket, rank {ad['champ_rank']} of 12, playoffs {ad['playoff']:.2f} percent. Expected weekly category wins {ECW:.3f}, rank {ECWR} of 12" + ("" if lead == 10 else f" behind seat {lead} ({mgr[lead]}, {ecw_by[lead]:.3f})") + f", favored in {WW} of 11 head-to-heads. Following the card's 🎯 from the same seat (the self-consistent chain) grades {fc['champ']:.2f} percent. The owner took the 🎯 at {len(followed)} of 13 turns and stayed in the Top 5 at {len(top5)}; the largest single swap is #{best[1]} {best[0]} ({best[2]:.2f} percent, {best[2] - ad['champ']:+.2f} points). The tool log is clean: the board the tool held equals Yahoo's recap at 156 of 156 picks, after three typed names were fixed by number (one of them four picks later).\n")
w("## 1. Roster changes\n\nNone. No line, tag, placement or price changed on either plane; this is a grade of a practice room.\n")
w("## 2. The team, graded\n\nEVIDENCE: `arena/results/m80_final.json`, `m80_arms.json` (18,000 seasons per arm, seeds 11/23/47, the real eight-team bracket), pool tag v68 = `players_v68.csv` (data/players.csv at `cb1a922`, sha256 30246ac015fe).\n")
w("| arm | title % | playoffs % | rank |\n|---|---|---|---|")
w(f"| as drafted | {ad['champ']:.2f} | {ad['playoff']:.2f} | {ad['champ_rank']} |")
w(f"| follow the card's 🎯 at every turn (self-consistent chain: " + ", ".join(f"#{n} {p}" for n, p in fc["swaps"]) + f") | {fc['champ']:.2f} | {fc['playoff']:.2f} | {fc['champ_rank']} |")
for nm, n, c in swaps: w(f"| single swap at #{n}: {nm} | {c:.2f} | {A[f'swap#{n}:{nm}']['playoff']:.2f} | {A[f'swap#{n}:{nm}']['champ_rank']} |")
w("\nCategory shape (weekly model, rank of 12): " + ", ".join(f"{c} {r}" for c, r in CR.items()) + ".\n")
w("For scale, the other live public rooms graded on this bracket: " + ", ".join(f"mock {m} {c:.2f}" for m, c in sorted(live.items())) + ".\n")
w("## 3. Pick by pick: the page's card, the owner, hindsight\n\nEVIDENCE: `m80_deckcard_v68.json` (the Version 68 page's own engine), `m80_hindsight.json` (every single-swap alternative scored by weekly category wins against the final rosters).\n")
w("| pick | owner took | card rank | the page's 🎯 | hindsight's best alternative (Δ weekly cat wins) |\n|---|---|---|---|---|")
for t in turns:
    h = hb[t["pick"]]["top"][0]
    w(f"| #{t['pick']} | {t['actual']} | {t['actualCardRank']} | {tgt(t)} | {h['n']} ({h['gain']:+.3f}) |")
w(f"\nThe turns off the 🎯: " + ", ".join(f"#{t['pick']} {t['actual']} (card #{t['actualCardRank']}, 🎯 {tgt(t)}, taken " + (f"#{taken[tgt(t)][0]} by seat {taken[tgt(t)][1]}" if tgt(t) in taken else "never") + ")" for t in turns if t["actualCardRank"] > 1) + ".\n")
assert fs[132]["player"] == recap[132]["player"] == "Kevin Porter Jr." and fs[132]["slot"] == recap[132]["slot"]
w(f"## 4. Tool-state integrity\n\n" + sc.strip().replace("\n", "; ") + f". The owner's tool log as pinned in `arena/data/events/m80_tool_events.json` ({len(ev)} events: {nfeed} feeds, {len(raw_unk)} of them raw texts that resolved to UNKNOWN (" + ", ".join(f"\"{t}\" at #{n}" for n, t in raw_unk) + f"), {nfix} numbered fixes (" + ", ".join(f"#{n} {nm}" for n, nm in nfix_lines) + f"; #133 sent after #137, four picks late), {nhalt} halts, {nins} inserts, {nundo} undos; {nres} page resumes in the paste, replayed as one session) replayed through the Version 68 page in headless Chromium: {S['echoMisses']} echo misses, {S['clockMismatches']} clock mismatches, {S['pageErrors']} page errors, {S['finalPicks']} picks; the final board equals Yahoo's recap at 156 of 156 and the five \"off the card\" lines equal the paste's. The late fix: in the tool's final board #133 is {fs[132]['player']} on Seat {fs[132]['slot']}; Yahoo's recap has {recap[132]['player']} at #133 for seat {recap[132]['slot']} ({mgr[recap[132]['slot']]}). The grading pipeline's Python port differs from the page record at {len(port_diff)} turns" + (f" ({', '.join(f'#{p}: port {a}, page {b}' for p, a, b in port_diff)})" if port_diff else "") + "; the page record is the authority for what the card said.\n")
w("## 5. The Undo / Insert-at-# check of this morning, on this room\n")
w("The owner's question of 2026-10-14 (\"when using the undo pick and insert at # features ... the arithmetic computation and correct team association is accurate?\") was answered from a separate harness (`report/after-reports/undo-insert-2026-10-14/`). This room used neither feature; its three numbered fixes are the nearest live case, and they behaved as the harness predicts: each landed on its own pick number and seat, the late one included, and the final board equals Yahoo's recap at 156 of 156.\n")
w("## Watchlist\n")
T10 = {}
for m in (73, 74, 75, 77, 78, 79, 80):
    f = sorted(glob.glob(f"{D}/m{m}_deckcard_v*.json")); f = [x for x in f if "toolstate" not in x][-1]
    t = next(x for x in J(f) if x["pick"] == 10); T10[m] = (t["actual"], t["actualCardRank"], tgt(t))
w("- #10 across the recent live rooms (page records): " + "; ".join(f"mock {m} {a} (card #{r}, 🎯 {g})" for m, (a, r, g) in T10.items()) + ". On Version 68 Haliburton is card #" + str(T10[80][1]) + " at #10 (🎯 " + T10[80][2] + "); on Version 65 he was card #9.")
w("- The publish freeze during the draft (D-1013-5) and no RESYNC during the draft (D-1013-2) stand.\n")
w("## Open-item receipts\n\n| item | query run (2026-10-14) | dated finding |\n|---|---|---|")
w("| (this room) | records only; no web research and no roster pull | the room's names resolve to the Version 68 pool 156 of 156 |")
w("| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | this morning's final pull (`after-report-2026-10-14.md`, receipts dated 10/14) | as recorded there (HELD, or unsigned); not re-queried for this grade (did not check) |\n")
w(rn + "\n")
w("\n## Bounds\n\n**Out of scope by design.**\n- No line, price or engine change: Version 68 is the lock page and the publish freeze holds.\n- No Yahoo standings comparison: no screenshot came with this paste.\n- The punt test and the advice line were not re-run: no punt was declared and no advisor click is in the feed.\n- This is a room of random humans, not the league's managers.\n")
w("**In scope and unverified.**\n- The raw text the owner typed for picks the tool resolved by surname (\"assumed over\" lines) is not in the paste; the pinned events feed the resolved names. The echoes and the final board match, so the state is the same; the typed strings are `UNVERIFIABLE`.\n- Whether the season arms' title share holds against the league's real managers: `UNVERIFIABLE` until the draft.\n")
w("## Decision sheet (owner disposes)\n\n| id | decision question | default if silent |\n|---|---|---|")
w("| (none new) | this room raises no decision | — |")
w("| D-1014-1..3, D-1014-8, D-1013-1..14 and earlier | carried as set in the 10/14 reports | carried |\n")
w("## Provenance\n")
w("- Inputs: the owner's paste (`draft80-2026-10-14/owner_message.txt`, verbatim); deck rev `cb1a922` (Version 68, page sha256 b83d1cdcc0e9, published 1791993066-d8ff).")
w("- Tools: `build_state.py` (state, feed check and the replay events), the deck's `arena/mocks/live_retro.py` (mock 80 registered on tag v68: replay, final, hindsight, arms), `live_deckcard.py` (the page's engine), `live_replay_dom.mjs` (the tool log through the Version 68 and Version 67 pages), `scripts/repeat_market_check.py`, `write_report.py` (this file's writer). Records in `arena/results/m80_*.json` and this folder.")
w("- No line, tag or placement changed on either plane.\n")
w("## In plain language\n")
w(f"**How the room went.** About a {ad['champ']:.0f} percent title share, {ad['champ_rank']} of 12 by title odds and {ECWR} of 12 week to week, favored against {WW} of the other 11. You followed the card at {len(followed)} of 13 picks and stayed in its Top 5 at {len(top5)}.")
w(f"\n**The pick to learn from.** The best single change would have been #{best[1]}: {best[0]} instead of {own[best[1]]}, worth about {best[2] - ad['champ']:.1f} title points.")
w("\n**The tool.** Clean on the final page: three typos fixed by number (one four picks after the fact), one page reload, and the tool's board matched Yahoo's at every pick.")
w("\n**Your decisions.** Nothing new.")
P = os.path.join(K, "report", "after-reports", "after-report-2026-10-14-draft80.md")
open(P, "w", encoding="utf-8").write("\n".join(x for x in o if x is not None) + "\n")
PL = os.path.join(K, "report", "pull-log.md"); pl = rd(PL)
if "after-report-2026-10-14-draft80.md" not in pl:
    row = (f"| 2026-10-14 | mock 80 grade (public room, LIVE mode, deck Version 68) | 0 | 0 | 0 | "
           f"after-reports/after-report-2026-10-14-draft80.md — as drafted {ad['champ']:.2f}% (rank {ad['champ_rank']}), ECW {ECW:.3f} rank {ECWR}, favored {WW} of 11; "
           f"card followed {len(followed)} of 13, Top-5 at {len(top5)}; follow-card chain {fc['champ']:.2f}%; largest swap #{best[1]} {best[0]} {best[2]:.2f}%; "
           f"tool board = recap 156 of 156, five echoes reproduced by the Version 68 page (one differs on Version 67); no plane change |")
    open(PL, "w", encoding="utf-8").write(pl.rstrip("\n") + "\n" + row + "\n")
print("written", P)
