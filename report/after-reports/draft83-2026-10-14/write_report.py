#!/usr/bin/env python3
"""Writes report/after-reports/after-report-2026-10-14-draft83.md and the pull-log row from the records: the deck's
m83_final / m83_arms / m83_hindsight / m83_deckcard_v69 / m83_replay, this folder's state_check.txt, rn_section_m83.md,
and the replay of the owner's tool log through the current page (Version 70; its engine is the lock page's — the
Version 70 change is one warning line's count, so the log cannot tell Version 69 from Version 70). No figure is typed by hand."""
import glob, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.normpath(os.path.join(H, "..", "..", ".."))
DK = "/home/user/yahoo-fantasy-basketball"; D = f"{DK}/arena/results"
J = lambda p: json.load(open(p, encoding="utf-8")); rd = lambda p: open(p, encoding="utf-8").read()
A = J(f"{D}/m83_arms.json"); HS = J(f"{D}/m83_hindsight.json"); PG = J(f"{D}/m83_deckcard_v69.json")
RP = J(f"{D}/m83_replay.json")["v69"]; F = J(f"{D}/m83_final.json")["v69"]
recap = J(os.path.join(H, "recap.json")); sc = rd(os.path.join(H, "state_check.txt")); msg = rd(os.path.join(H, "owner_message.txt"))
rn = rd(os.path.join(H, "rn_section_m83.md")); rn = rn[rn.index("## Repeat-name market check"):].strip()
rn_head = re.search(r"(\d+) of (\d+) mocks replayed; (\d+) FLAGGED", rd(os.path.join(H, "rn_section_m83.md"))).groups()
mgr = {p["slot"]: p["manager"] for p in recap}
turns = sorted(PG, key=lambda t: t["pick"]); own = {p["n"]: p["player"] for p in recap if p["slot"] == 10}
assert [t["pick"] for t in turns] == sorted(own) and all(t["actual"] == own[t["pick"]] for t in turns)
tgt = lambda t: next(r["n"] for r in t["rows"] if r["target"])
followed = [t for t in turns if t["actualCardRank"] == 1]; top5 = [t for t in turns if t["actualCardRank"] <= 5]
echo_lines = [l.strip() for l in msg.split("\n") if l.startswith("⚠ off the card")]
echo_of = lambda rec: [l.strip() for r in rec["rows"] for l in r["fresh"] if "off the card" in l]
RV = J(os.path.join(H, "replay_v70.json")); S = RV["summary"]
assert len(echo_lines) == 1 and echo_of(RV) == echo_lines
assert S["echoMisses"] == 0 and S["clockMismatches"] == 0 and S["pageErrors"] == 0 and S["finalPicks"] == 156
E = re.findall(r"⚠ off the card: (.+?) ranks #(\d+) \(([\d.]+) behind 🎯 (.+?)\)", msg); tb = {t["actual"]: t for t in turns}
assert all(int(rk) == tb[nm]["actualCardRank"] and tg == tgt(tb[nm]) for nm, rk, g, tg in E)
# the shift line after the #6 insert: the paste's text, reproduced by the page, against the page's own card at #10
shift_paste = [l.strip() for l in msg.split("\n") if "is YOUR pick after the shift" in l]
shift_page = [l.strip() for r in RV["rows"] for l in r["fresh"] if "is YOUR pick after the shift" in l]
assert len(shift_paste) == 1 and shift_page == shift_paste
t10 = tb[own[10]]; assert t10["pick"] == 10
ev = J(f"{DK}/arena/data/events/m83_tool_events.json")
nfeed = sum(1 for e in ev if e["op"] == "feed"); nins = sum(1 for e in ev if e["op"] == "insert"); nundo = sum(1 for e in ev if e["op"] == "undo")
nskip = sum(1 for e in ev if e.get("expect") == "skipped")
ins = re.findall(r"✎ inserted (.+?) at #(\d+) → Seat (\d+)", msg); undos = re.findall(r"↶ undid: (.+?) \(Seat (\d+)\)", msg)
skips = re.findall(r'⚠ skipped "(.+?)": already off the board', msg)
assumed = re.findall(r"#(\d+): (.+?) → Seat \d+(?: \(YOU\))?\s+\(assumed over ([^)]+)\)", msg)
injskip = re.findall(r"#(\d+): (.+?) → Seat \d+\s+\((.+?) skipped: injury-excluded\)", msg)
heads = re.findall(r"#(\d+): (.+?) → Seat (\d+)(?: \(YOU\))?\s+\(heads-up: (.+?) is injury-excluded on this board\)", msg)
nres = [int(x) for x in re.findall(r"— resumed: (\d+) picks logged —", msg)]
assert nins == len(ins) == 2 and nundo == len(undos) == 2 and nskip == len(skips) == 1
sys.path.insert(0, f"{DK}/scripts"); import hoops
fs = RV["finalState"]["picks"]; board_diff = [i + 1 for i, (p, r) in enumerate(zip(fs, recap)) if hoops.fold(p["player"]) != hoops.fold(r["player"]) or p["slot"] != r["slot"]]
assert board_diff == [] and len(fs) == 156
assumed_ok = all(hoops.fold(recap[int(n) - 1]["player"]) == hoops.fold(nm) for n, nm, _ in assumed)
port_diff = [(r["pick"], r["actual_ds_rank"], tb[r["actual"]]["actualCardRank"]) for r in RP if r["actual_ds_rank"] != tb[r["actual"]]["actualCardRank"]]
ad = A["as_drafted"]; fc = A["follow_card_selfconsistent"]
swaps = sorted(((k.split(":", 1)[1], int(k.split(":")[0][5:]), v["champ"]) for k, v in A.items() if k.startswith("swap#")), key=lambda x: -x[2])
ecw_by = {int(str(k).lstrip("T")): v for k, v in F["ecw"].items()}; ECW = ecw_by[10]; ECWR = F["ecw_rank"]; WW = F["exp_winning_weeks"]
lead = max(ecw_by, key=ecw_by.get); hb = {t["pick"]: t for t in HS["turns"]}; best = swaps[0]
ALL = {}
for f in glob.glob(f"{D}/m*_arms.json"):
    mm = re.fullmatch(r"m(\d+)_arms\.json", os.path.basename(f))
    if mm and int(mm.group(1)) != 83:
        a = J(f).get("as_drafted")
        if a: ALL[int(mm.group(1))] = a["champ"]
live = {m: ALL[m] for m in (67, 68, 73, 74, 75, 77, 78, 79, 80, 81, 82) if m in ALL}
CR = F["cat_rank_weekly"]; taken = {p["player"]: (p["n"], p["slot"]) for p in recap}
o = []; w = o.append
w("# After-report — draft_83: the 10/14 evening live room from slot 10, on the locked lines\n")
w("**Owner request (2026-10-14, verbatim):** the deck tool's LIVE feed, the owner's 13-man roster and Yahoo's round-by-round recap, pasted with no other text (`draft83-2026-10-14/owner_message.txt`). Read as the standing request for these pastes: grade the room with the deck pipeline and report; no line, tag or price changes.\n")
w(f"**Room:** public Yahoo mock, 12 × 13, owner seat 10 (random humans; a practice rep, not opponent intel; display names: " + ", ".join(f"{s} {mgr[s]}" for s in range(1, 13)) + "). **Deck used:** the locked lines (pool tag v69 = data/players.csv at `af91b23`). The page was Version 69 or Version 70 — the log cannot tell which: Version 70 changed only the ⚠ LEAN warning line's count, which this paste does not carry, and the one \"off the card\" line of the paste is reproduced character for character by the current page.\n")
w("Pull window: 2026-10-14 → 2026-10-14 (analysis only; no roster pull).\n")
w(f"**Headline.** As drafted **{ad['champ']:.2f} percent** for the title on the real eight-team bracket, rank {ad['champ_rank']} of 12, playoffs {ad['playoff']:.2f} percent. Expected weekly category wins {ECW:.3f}, rank {ECWR} of 12" + ("" if lead == 10 else f" behind seat {lead} ({mgr[lead]}, {ecw_by[lead]:.3f})") + f", favored in {WW} of 11 head-to-heads. Following the card's 🎯 from the same seat (the self-consistent chain) grades {fc['champ']:.2f} percent. The owner took the 🎯 at {len(followed)} of 13 turns and stayed in the Top 5 at {len(top5)}; the largest single swap is #{best[1]} {best[0]} ({best[2]:.2f} percent, {best[2] - ad['champ']:+.2f} points). The tool log carried two Insert-at-# corrections (" + ", ".join(f"#{n} {nm}" for nm, n, s in ins) + "), a double undo at the last round, and one refused repeat entry; the board the tool ended on equals Yahoo's recap at 156 of 156 picks. One display defect found: after the #6 insert moved Haliburton onto the owner's seat, the log line said \"Haliburton is the 🎯\" while the card at #10 had " + f"{tgt(t10)} as 🎯 and Haliburton #{t10['actualCardRank']} (D83-1).\n")
w("## 1. Roster changes\n\nNone. No line, tag, placement or price changed on either plane; this is a grade of a practice room.\n")
w("## 2. The team, graded\n\nEVIDENCE: `arena/results/m83_final.json`, `m83_arms.json` (18,000 seasons per arm, seeds 11/23/47, the real eight-team bracket), pool tag v69 = `players_v69.csv` (data/players.csv at `af91b23`, the lock's pool). The grade runs on Yahoo's recap (the true board), not the tool's.\n")
w("| arm | title % | playoffs % | rank |\n|---|---|---|---|")
w(f"| as drafted | {ad['champ']:.2f} | {ad['playoff']:.2f} | {ad['champ_rank']} |")
w(f"| follow the card's 🎯 at every turn (self-consistent chain: " + ", ".join(f"#{n} {p}" for n, p in fc["swaps"]) + f") | {fc['champ']:.2f} | {fc['playoff']:.2f} | {fc['champ_rank']} |")
for nm, n, c in swaps: w(f"| single swap at #{n}: {nm} | {c:.2f} | {A[f'swap#{n}:{nm}']['playoff']:.2f} | {A[f'swap#{n}:{nm}']['champ_rank']} |")
w("\nCategory shape (weekly model, rank of 12): " + ", ".join(f"{c} {r}" for c, r in CR.items()) + ".\n")
w("For scale, the other live public rooms graded on this bracket: " + ", ".join(f"mock {m} {c:.2f}" for m, c in sorted(live.items())) + ".\n")
w("## 3. Pick by pick: the page's card, the owner, hindsight\n\nEVIDENCE: `m83_deckcard_v69.json` (the page's own engine on the true board before each owner turn), `m83_hindsight.json` (every single-swap alternative scored by weekly category wins against the final rosters).\n")
w("| pick | owner took | card rank | the page's 🎯 | hindsight's best alternative (Δ weekly cat wins) |\n|---|---|---|---|---|")
for t in turns:
    h = hb[t["pick"]]["top"][0]
    w(f"| #{t['pick']} | {t['actual']} | {t['actualCardRank']} | {tgt(t)} | {h['n']} ({h['gain']:+.3f}) |")
off = [t for t in turns if t["actualCardRank"] > 1]
gap = lambda t: next(r["ds"] for r in t["rows"] if r["target"]) - next(r["ds"] for r in t["rows"] if r["n"] == t["actual"])
w(f"\nThe turns off the 🎯: " + ", ".join(f"#{t['pick']} {t['actual']} (card #{t['actualCardRank']}, {gap(t):.3f} behind 🎯 {tgt(t)}, taken " + (f"#{taken[tgt(t)][0]} by seat {taken[tgt(t)][1]}" if tgt(t) in taken else "never") + ")" for t in off) + ".\n")
w(f"## 4. Tool-state integrity\n\n" + sc.strip().replace("\n", "; ") + f".\n")
w(f"EVIDENCE: the owner's tool log as pinned in `arena/data/events/m83_tool_events.json` ({len(ev)} events: {nfeed} feeds, of them {nskip} refused repeat; {nins} inserts; {nundo} undos; the closing \"resumed: {nres[-1]} picks logged\" line carries no event) replayed through the current page in headless Chromium (`draft83-2026-10-14/replay_v70.json`): {S['echoMisses']} echo misses, {S['clockMismatches']} clock mismatches, {S['pageErrors']} page errors, {S['finalPicks']} picks; the final state equals Yahoo's recap name and seat at all 156 picks.\n")
w("| what happened in the room | the log line | what the tool did |\n|---|---|---|")
for nm, n, s in ins:
    w(f"| a missed pick restored at #{n} | \"inserted {nm} at #{n} → Seat {s}\" | the later picks shifted one place and re-seated by the snake; replay echo matched |")
w(f"| \"{skips[0]}\" typed again after #{taken[next(p['player'] for p in recap if p['player'].endswith(skips[0]))][0]} was logged | \"skipped \\\"{skips[0]}\\\": already off the board (no pick logged)\" | refused; nothing logged, the board unchanged |")
w(f"| the last round entered out of order (#{int(heads[0][0])} {heads[0][1]} logged to the owner's seat) | " + "; ".join(f"\"undid: {u} (Seat {s})\"" for u, s in undos) + " | both picks removed in reverse order, then #154 Devin Vassell (owner), #155 Jimmy Butler (seat 11), #156 Maxime Raynaud (seat 12) re-logged |")
w(f"\nThe resolver's choices on shared surnames (\"assumed over\" lines, {len(assumed)}): every one agrees with Yahoo's recap — {'yes' if assumed_ok else 'NO'}. Injury-excluded namesakes skipped by rule: " + ", ".join(f"#{n} {nm} ({x} skipped)" for n, nm, x in injskip) + f". The heads-up on Jimmy Butler (\"injury-excluded on this board\") printed both times he was logged; he was taken at #155 by seat 11.\n")
w(f"**The shift line (D83-1).** After the Tatum insert, the paste and the replayed page both print: \"{shift_paste[0]}\". The page builds that line from the card as last rendered (`cardGapText`, `docs/draft-deck.html`); Haliburton was already logged and so was not on that card, the lookup found no row, and the fallback text — written for the case \"the pick is the 🎯\" — printed instead. The card on the true board at #10 (`m83_deckcard_v69.json`) had {tgt(t10)} as 🎯 and Haliburton #{t10['actualCardRank']}, {gap(t10):.3f} behind. The line is a log message only; nothing the card computes reads it. Not fixed tonight (publish freeze, D-1013-5).\n")
w(f"The grading pipeline's Python port differs from the page record at {len(port_diff)} turns" + (f" ({', '.join(f'#{p}: port {a}, page {b}' for p, a, b in port_diff)})" if port_diff else "") + "; the page record is the authority for what the card said.\n")
w("## Watchlist\n")
T10 = {}
for m in (75, 77, 78, 79, 80, 81, 82, 83):
    f = sorted(glob.glob(f"{D}/m{m}_deckcard_v*.json")); f = [x for x in f if "toolstate" not in x][-1]
    t = next(x for x in J(f) if x["pick"] == 10); T10[m] = (t["actual"], t["actualCardRank"], tgt(t))
w("- #10 across the recent live rooms (page records): " + "; ".join(f"mock {m} {a} (card #{r}, 🎯 {g})" for m, (a, r, g) in T10.items()) + ".")
w("- A missed pick in the first round (Tatum at #6) moved the owner's own pick: the tool caught it with Insert-at-#, and the shift line printed the wrong 🎯 claim (D83-1). In the real draft, check the pick counter against Yahoo's before the owner's turn.")
w("- The publish freeze during the draft (D-1013-5) and no RESYNC during the draft (D-1013-2) stand.\n")
w("## Open-item receipts\n\n| item | query run (2026-10-14) | dated finding |\n|---|---|---|")
w("| (this room) | records only; no web research and no roster pull | the room's names resolve to the lock pool 156 of 156 |")
w("| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this grade (did not check) |\n")
w(rn + "\n")
w("\n## Bounds\n\n**Out of scope by design.**\n- No line, price or engine change; the D83-1 line is flagged, not fixed.\n- No Yahoo standings comparison: no screenshot came with this paste.\n- The punt test and the advice line were not re-run: no punt was declared and no advisor click is in the feed.\n- This is a room of random humans, not the league's managers.\n")
w("**In scope and unverified.**\n- Which page, Version 69 or Version 70: `UNVERIFIABLE` from the paste (no LEAN line in it); the engines are identical, so no figure here depends on it.\n- The card the owner saw at the moment of the #10 pick: the tool was one pick short then (Tatum not yet logged), so the screen showed the card for the tool's pick #9 with Tatum available. This report grades the card on the true board, as for every room with an insert; the on-screen card at that moment was not reconstructed (did not check).\n- Whether the season arms' title share holds against the league's real managers: `UNVERIFIABLE` until the draft.\n")
w("## Decision sheet (owner disposes)\n\n| id | decision question | default if silent |\n|---|---|---|")
w("| D83-1 | the shift line after an Insert-at-# says \"X is the 🎯\" when X is simply not on the current card: (a) leave it until after the draft (publish freeze) and read the card, not that line; (b) after the draft, make the line say the card rank on the board before the pick, or say nothing | (a), then (b) after the draft |")
w("| D82-1, D-INT-1, D-INT-2, D-1014-*, D-1013-*, earlier | carried | carried |\n")
w("## Provenance\n")
w("- Inputs: the owner's paste (`draft83-2026-10-14/owner_message.txt`, verbatim); the current page `docs/draft-deck.html` (Version 70, deck main `0fdb485`); pool tag v69 (rev `af91b23`).")
w(f"- Tools: `build_state.py`, the deck's `arena/mocks/live_retro.py` (mock 83 registered on tag v69: replay, final, hindsight, arms), `live_deckcard.py`, `live_replay_dom.mjs`, `scripts/repeat_market_check.py` ({rn_head[0]} of {rn_head[1]} mocks, {rn_head[2]} flagged), `write_report.py`. Records in `arena/results/m83_*.json` and this folder.")
w("- No line, tag or placement changed on either plane.\n")
w("## In plain language\n")
w(f"**How the room went.** About a {ad['champ']:.0f} percent title share, {ad['champ_rank']} of 12 by title odds and {ECWR} of 12 week to week, favored against {WW} of the other 11. You followed the card at {len(followed)} of 13 picks and stayed in its Top 5 at all {len(top5)}.")
w(f"\n**The pick to learn from.** The best single change would have been #{best[1]}: {best[0]} instead of {own[best[1]]}, worth about {best[2] - ad['champ']:+.1f} title points. Following the 🎯 at every turn would have graded {fc['champ']:.1f} percent, {fc['champ'] - ad['champ']:+.1f} points against as drafted.")
w(f"\n**The tool.** Your corrections all worked: the two inserts (Tatum at #6, Ingram at #92), the double undo at the end, and the refused repeat of Lendeborg left the tool's board identical to Yahoo's, 156 of 156. One line misled: after the Tatum insert it said \"Haliburton is the 🎯\". At #10 the card actually had {tgt(t10)} first and Haliburton second, {gap(t10):.3f} behind — a near tie. That line is a message only and doesn't change the card; trust the card itself.")
w("\n**Your decisions.** D83-1, that message; the default leaves it until after the draft.")
P = os.path.join(K, "report", "after-reports", "after-report-2026-10-14-draft83.md")
open(P, "w", encoding="utf-8").write("\n".join(o) + "\n")
PL = os.path.join(K, "report", "pull-log.md"); pl = rd(PL)
if "after-report-2026-10-14-draft83.md" not in pl:
    row = (f"| 2026-10-14 | mock 83 grade (public room, LIVE mode, locked lines, page Version 69 or 70) | 0 | 0 | 0 | "
           f"after-reports/after-report-2026-10-14-draft83.md — as drafted {ad['champ']:.2f}% (rank {ad['champ_rank']}), ECW {ECW:.3f} rank {ECWR}, favored {WW} of 11; "
           f"card followed {len(followed)} of 13, Top-5 at {len(top5)}; follow-card chain {fc['champ']:.2f}%; largest swap #{best[1]} {best[0]} {best[2]:.2f}%; "
           f"tool board = recap 156 of 156 after 2 inserts, 2 undos, 1 refused repeat; the one echo reproduced; shift line misstates the 🎯 at #10 (D83-1); no plane change |")
    open(PL, "w", encoding="utf-8").write(pl.rstrip("\n") + "\n" + row + "\n")
print("written", P)
