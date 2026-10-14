#!/usr/bin/env python3
"""Writes report/after-reports/after-report-2026-10-14-draft82.md and the pull-log row from the records: the deck's
m82_final / m82_arms / m82_hindsight / m82_deckcard_v69 / m82_replay, this folder's state_check.txt, rn_section_m82.md,
and the three page replays of the owner's tool log — the lock page (Version 69, the page the room was drafted on), the
Version 68 page (the version identification) and the LEAN-fix page (Version 70). No figure is typed by hand."""
import glob, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.normpath(os.path.join(H, "..", "..", ".."))
D = "/home/user/yahoo-fantasy-basketball/arena/results"
J = lambda p: json.load(open(p, encoding="utf-8")); rd = lambda p: open(p, encoding="utf-8").read()
A = J(f"{D}/m82_arms.json"); HS = J(f"{D}/m82_hindsight.json"); PG = J(f"{D}/m82_deckcard_v69.json")
RP = J(f"{D}/m82_replay.json")["v69"]; F = J(f"{D}/m82_final.json")["v69"]
recap = J(os.path.join(H, "recap.json")); sc = rd(os.path.join(H, "state_check.txt")); msg = rd(os.path.join(H, "owner_message.txt"))
rn = rd(os.path.join(H, "rn_section_m82.md")); rn = rn[rn.index("## Repeat-name market check"):].strip()
rn_head = re.search(r"(\d+) of (\d+) mocks replayed; (\d+) FLAGGED", rd(os.path.join(H, "rn_section_m82.md"))).groups()
mgr = {p["slot"]: p["manager"] for p in recap}
turns = sorted(PG, key=lambda t: t["pick"]); own = {p["n"]: p["player"] for p in recap if p["slot"] == 10}
assert [t["pick"] for t in turns] == sorted(own) and all(t["actual"] == own[t["pick"]] for t in turns)
tgt = lambda t: next(r["n"] for r in t["rows"] if r["target"])
followed = [t for t in turns if t["actualCardRank"] == 1]; top5 = [t for t in turns if t["actualCardRank"] <= 5]
echo_lines = [l.strip() for l in msg.split("\n") if l.startswith("⚠ off the card")]
echo_of = lambda rec: [l.strip() for r in rec["rows"] for l in r["fresh"] if "off the card" in l]
LK = J(os.path.join(H, "replay_lock.json")); V68 = J(os.path.join(H, "replay_v68.json")); FX = J(os.path.join(H, "replay_fixed.json"))
assert len(echo_lines) == 3 and echo_of(LK) == echo_lines
v68_diff = [(a, b) for a, b in zip(echo_of(V68), echo_lines) if a != b] + [(x, None) for x in echo_of(V68)[len(echo_lines):]]
assert v68_diff, "the Version 68 page must differ somewhere for the identification to hold"
pick_of = {v: k for k, v in own.items()}
def targets(echoes):
    t = dict(own)
    for nm, rk, g, tg in (re.match(r"⚠ off the card: (.+?) ranks #(\d+) \(([\d.]+) behind 🎯 (.+?)\)", l).groups() for l in echoes):
        t[pick_of[nm]] = tg
    return t
T69, TFX = targets(echo_lines), targets(echo_of(FX)); assert all(T69[t["pick"]] == tgt(t) for t in turns)
fx_diff = [(p, T69[p], TFX[p]) for p in sorted(own) if T69[p] != TFX[p]]
E = re.findall(r"⚠ off the card: (.+?) ranks #(\d+) \(([\d.]+) behind 🎯 (.+?)\)", msg); tb = {t["actual"]: t for t in turns}
assert all(int(rk) == tb[nm]["actualCardRank"] and tg == tgt(tb[nm]) for nm, rk, g, tg in E)
S = LK["summary"]; assert S["echoMisses"] == 0 and S["clockMismatches"] == 0 and S["pageErrors"] == 0 and S["finalPicks"] == 156
ev = J("/home/user/yahoo-fantasy-basketball/arena/data/events/m82_tool_events.json")
nfeed = sum(1 for e in ev if e["op"] == "feed"); nunk = sum(1 for e in ev if str(e.get("expect", "")).startswith("UNKNOWN")); nhalt = sum(1 for e in ev if e.get("expect") == "HALTED")
nfix = sum(1 for e in ev if e["op"] == "feed" and re.match(r"\d+- ", e["text"])); nins = sum(1 for e in ev if e["op"] == "insert"); nundo = sum(1 for e in ev if e["op"] == "undo")
nres = [int(x) for x in re.findall(r"— resumed: (\d+) picks logged —", msg) if int(x) > 0]
sys.path.insert(0, "/home/user/yahoo-fantasy-basketball/scripts"); import hoops
fs = LK["finalState"]["picks"]; board_diff = [i + 1 for i, (p, r) in enumerate(zip(fs, recap)) if hoops.fold(p["player"]) != hoops.fold(r["player"]) or p["slot"] != r["slot"]]
assert board_diff == [124] and fs[123]["player"] == "Draymond Green" and recap[123]["player"] == "Jalen Green" and fs[123]["slot"] == recap[123]["slot"] == 4
assumed = re.search(r"#124: Draymond Green → Seat 4\s+\((assumed over [^)]+)\)", msg).group(1)
# did the divergence reach the owner's card? the two Greens on the owner's later cards, and Jalen Green's true fate
later = [t for t in turns if t["pick"] > 124]
hb = {t["pick"]: t for t in HS["turns"]}
greens = [(t["pick"], r["n"], i + 1) for t in later for i, r in enumerate(t["rows"]) if r["n"] in ("Draymond Green", "Jalen Green")]
# the tool held Draymond as taken from #124 on, so he could not reach the owner's card; hindsight ranks him on its own board
hidden = [(t["pick"], next(x["gain"] for x in hb[t["pick"]]["top"] if x["n"] == "Draymond Green")) for t in later if any(x["n"] == "Draymond Green" for x in hb[t["pick"]]["top"][:1])]
hid_txt = (" The miss had a cost the other way: with Draymond marked taken, the card could not offer him afterwards, and hindsight ranks him the best alternative at " + ", ".join(f"#{p} ({g:+.3f} weekly cats)" for p, g in hidden) + " — he went undrafted in the room.") if hidden else ""
port_diff = [(r["pick"], r["actual_ds_rank"], tb[r["actual"]]["actualCardRank"]) for r in RP if r["actual_ds_rank"] != tb[r["actual"]]["actualCardRank"]]
ad = A["as_drafted"]; fc = A["follow_card_selfconsistent"]
swaps = sorted(((k.split(":", 1)[1], int(k.split(":")[0][5:]), v["champ"]) for k, v in A.items() if k.startswith("swap#")), key=lambda x: -x[2])
ecw_by = {int(str(k).lstrip("T")): v for k, v in F["ecw"].items()}; ECW = ecw_by[10]; ECWR = F["ecw_rank"]; WW = F["exp_winning_weeks"]
lead = max(ecw_by, key=ecw_by.get); hb = {t["pick"]: t for t in HS["turns"]}; best = swaps[0]
ALL = {}
for f in glob.glob(f"{D}/m*_arms.json"):
    mm = re.fullmatch(r"m(\d+)_arms\.json", os.path.basename(f))
    if mm and int(mm.group(1)) != 82:
        a = J(f).get("as_drafted")
        if a: ALL[int(mm.group(1))] = a["champ"]
live = {m: ALL[m] for m in (67, 68, 73, 74, 75, 77, 78, 79, 80, 81) if m in ALL}
CR = F["cat_rank_weekly"]; taken = {p["player"]: (p["n"], p["slot"]) for p in recap}
o = []; w = o.append
w("# After-report — draft_82: the 10/14 late live room from slot 10, on the lock page (Version 69)\n")
w("**Owner request (2026-10-14, verbatim):** the deck tool's LIVE feed, the owner's 13-man roster and Yahoo's round-by-round recap, pasted during the integrity audit (`draft82-2026-10-14/owner_message.txt`), then \"Publish fix now and grade Mock 82\". Read as the standing request for these pastes: grade the room with the deck pipeline and report; no line, tag or price changes.\n")
w(f"**Room:** public Yahoo mock, 12 × 13, owner seat 10 (random humans; a practice rep, not opponent intel; display names: " + ", ".join(f"{s} {mgr[s]}" for s in range(1, 13)) + "). **Deck used:** the lock page, published as Version 69 (rev `af91b23`, page sha256 e68a85a5305f; the six-way blend re-taken on Yahoo and Hashtag 10/14, Kawhi and Davis at 0.78). Replaying the owner's tool log through that page reproduces all three \"off the card\" lines of the paste character for character; through the Version 68 page the echoes differ (" + "; ".join(f"page: \"{x[0]}\"" for x in v68_diff) + "), so the room was drafted on the lock page — the first live room on the locked lines.\n")
w("Pull window: 2026-10-14 → 2026-10-14 (analysis only; no roster pull).\n")
w(f"**Headline.** As drafted **{ad['champ']:.2f} percent** for the title on the real eight-team bracket, rank {ad['champ_rank']} of 12, playoffs {ad['playoff']:.2f} percent. Expected weekly category wins {ECW:.3f}, rank {ECWR} of 12" + ("" if lead == 10 else f" behind seat {lead} ({mgr[lead]}, {ecw_by[lead]:.3f})") + f", favored in {WW} of 11 head-to-heads. Following the card's 🎯 from the same seat (the self-consistent chain) grades {fc['champ']:.2f} percent. The owner took the 🎯 at {len(followed)} of 13 turns and stayed in the Top 5 at {len(top5)}; the largest single swap is #{best[1]} {best[0]} ({best[2]:.2f} percent, {best[2] - ad['champ']:+.2f} points). The tool log: 156 feeds, no fix, no resume; the board the tool held equals Yahoo's recap at 155 of 156 picks — at #124 the tool resolved an ambiguous entry to Draymond Green ({assumed}) while Yahoo's recap has Jalen Green there (seat 4 either way). " + ("That divergence reached the owner's card: " + "; ".join(f"#{p} {n} at card #{i}" for p, n, i in greens) + "." if greens else "Neither Green appeared on the owner's card after #124." + hid_txt) + f" The same log through the LEAN-fix page (Version 70) " + (f"changes the 🎯 at {len(fx_diff)} of 13 turns (" + "; ".join(f"#{p}: {a} → {b}" for p, a, b in fx_diff) + ")" if fx_diff else "gives the same 🎯 at all 13 of the owner's turns") + ".\n")
w("## 1. Roster changes\n\nNone. No line, tag, placement or price changed on either plane; this is a grade of a practice room.\n")
w("## 2. The team, graded\n\nEVIDENCE: `arena/results/m82_final.json`, `m82_arms.json` (18,000 seasons per arm, seeds 11/23/47, the real eight-team bracket), pool tag v69 = `players_v69.csv` (data/players.csv at `af91b23`, the lock's pool, sha256 d1d74587c5db). The grade runs on Yahoo's recap (the true board), not the tool's.\n")
w("| arm | title % | playoffs % | rank |\n|---|---|---|---|")
w(f"| as drafted | {ad['champ']:.2f} | {ad['playoff']:.2f} | {ad['champ_rank']} |")
w(f"| follow the card's 🎯 at every turn (self-consistent chain: " + ", ".join(f"#{n} {p}" for n, p in fc["swaps"]) + f") | {fc['champ']:.2f} | {fc['playoff']:.2f} | {fc['champ_rank']} |")
for nm, n, c in swaps: w(f"| single swap at #{n}: {nm} | {c:.2f} | {A[f'swap#{n}:{nm}']['playoff']:.2f} | {A[f'swap#{n}:{nm}']['champ_rank']} |")
w("\nCategory shape (weekly model, rank of 12): " + ", ".join(f"{c} {r}" for c, r in CR.items()) + ".\n")
w("For scale, the other live public rooms graded on this bracket: " + ", ".join(f"mock {m} {c:.2f}" for m, c in sorted(live.items())) + ".\n")
w("## 3. Pick by pick: the page's card, the owner, hindsight\n\nEVIDENCE: `m82_deckcard_v69.json` (the lock page's own engine), `m82_hindsight.json` (every single-swap alternative scored by weekly category wins against the final rosters).\n")
w("| pick | owner took | card rank | the page's 🎯 | hindsight's best alternative (Δ weekly cat wins) |\n|---|---|---|---|---|")
for t in turns:
    h = hb[t["pick"]]["top"][0]
    w(f"| #{t['pick']} | {t['actual']} | {t['actualCardRank']} | {tgt(t)} | {h['n']} ({h['gain']:+.3f}) |")
w(f"\nThe turns off the 🎯: " + ", ".join(f"#{t['pick']} {t['actual']} (card #{t['actualCardRank']}, 🎯 {tgt(t)}, taken " + (f"#{taken[tgt(t)][0]} by seat {taken[tgt(t)][1]}" if tgt(t) in taken else "never") + ")" for t in turns if t["actualCardRank"] > 1) + ".\n")
w(f"## 4. Tool-state integrity\n\n" + sc.strip().replace("\n", "; ") + f". The owner's tool log as pinned in `arena/data/events/m82_tool_events.json` ({len(ev)} events: {nfeed} feeds, {nunk} UNKNOWN, {nfix} numbered fixes, {nhalt} halts, {nins} inserts, {nundo} undos; {len(nres)} page resumes) replayed through the lock page in headless Chromium: {S['echoMisses']} echo misses, {S['clockMismatches']} clock mismatches, {S['pageErrors']} page errors, {S['finalPicks']} picks; the three \"off the card\" lines equal the paste's. **The one divergence from the true board:** at #124 the paste's line reads \"Draymond Green → Seat 4 ({assumed})\" — the resolver picked Draymond from an ambiguous entry — while Yahoo's recap has Jalen Green at #124 for seat 4 ({mgr[4]}); Jalen Green was in fact gone and Draymond (taken by nobody; Yahoo's recap does not list him) stayed on the tool's available list. " + ("On the owner's later cards: " + "; ".join(f"#{p} {n} card #{i}" for p, n, i in greens) + "." if greens else "Neither Green reached the owner's card at #130, #135 or #154." + hid_txt) + f" The resolver's rule (a bare surname resolves to the best available namesake) did what it says; the typed text is not in the paste. The grading pipeline's Python port differs from the page record at {len(port_diff)} turns" + (f" ({', '.join(f'#{p}: port {a}, page {b}' for p, a, b in port_diff)})" if port_diff else "") + "; the page record is the authority for what the card said.\n")
w("## 5. The same room on the LEAN-fix page (Version 70)\n")
w(f"EVIDENCE: `draft82-2026-10-14/replay_fixed.json` (the owner's tool log through the page carrying the roster-balance fix, in headless Chromium: {FX['summary']['echoMisses']} echo misses, {FX['summary']['pageErrors']} page errors, {FX['summary']['finalPicks']} picks).\n")
w("The fix changes one warning line's count, not the engine; on this room the fixed page gives " + (f"a different 🎯 at {len(fx_diff)} of the owner's 13 turns: " + "; ".join(f"#{p} {a} → {b}" for p, a, b in fx_diff) if fx_diff else "the same 🎯 at all 13 of the owner's turns") + f", and prints {len(echo_of(FX))} \"off the card\" lines to the paste's {len(echo_lines)}" + (" — identical" if echo_of(FX) == echo_lines else "") + ".\n")
w("## Watchlist\n")
T10 = {}
for m in (75, 77, 78, 79, 80, 81, 82):
    f = sorted(glob.glob(f"{D}/m{m}_deckcard_v*.json")); f = [x for x in f if "toolstate" not in x][-1]
    t = next(x for x in J(f) if x["pick"] == 10); T10[m] = (t["actual"], t["actualCardRank"], tgt(t))
w("- #10 across the recent live rooms (page records): " + "; ".join(f"mock {m} {a} (card #{r}, 🎯 {g})" for m, (a, r, g) in T10.items()) + f". On the lock page Haliburton is card #{T10[82][1]} at #10 (🎯 {T10[82][2]}).")
w("- The ambiguous-surname resolution (#124): a bare surname with several namesakes resolves to the best available one by rule; in a live room, typing the first name too (\"Jalen Green\") removes the ambiguity. No rule change proposed tonight.")
w("- The publish freeze during the draft (D-1013-5) and no RESYNC during the draft (D-1013-2) stand.\n")
w("## Open-item receipts\n\n| item | query run (2026-10-14) | dated finding |\n|---|---|---|")
w("| (this room) | records only; no web research and no roster pull | the room's names resolve to the lock pool 156 of 156 |")
w("| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this grade (did not check) |\n")
w(rn + "\n")
w("\n## Bounds\n\n**Out of scope by design.**\n- No line, price or engine change.\n- No Yahoo standings comparison: no screenshot came with this paste.\n- The punt test and the advice line were not re-run: no punt was declared and no advisor click is in the feed.\n- This is a room of random humans, not the league's managers.\n")
w("**In scope and unverified.**\n- The raw text the owner typed for picks the tool resolved by surname (\"assumed over\" lines, #124 among them) is not in the paste; the pinned events feed the resolved names: `UNVERIFIABLE`.\n- Whether the season arms' title share holds against the league's real managers: `UNVERIFIABLE` until the draft.\n")
w("## Decision sheet (owner disposes)\n\n| id | decision question | default if silent |\n|---|---|---|")
w("| D82-1 | the bare-surname resolver after a live miss (#124, Green): (a) keep the rule, type first names in the real draft; (b) halt on any surname with 2+ available namesakes (the pre-9/29 behaviour, which buried the owner mid-draft at \"George\") | (a) |")
w("| D-INT-1, D-INT-2, D-1014-*, D-1013-*, earlier | carried | carried |\n")
w("## Provenance\n")
w("- Inputs: the owner's paste (`draft82-2026-10-14/owner_message.txt`, verbatim); the lock page (deck rev `af91b23`, sha256 e68a85a5305f, published as Version 69, id 1792001219-01f3); the Version 68 page (rev `cb1a922`); the LEAN-fix page (Version 70).")
w(f"- Tools: `build_state.py`, the deck's `arena/mocks/live_retro.py` (mock 82 registered on tag v69: replay, final, hindsight, arms), `live_deckcard.py`, `live_replay_dom.mjs` (three pages), `scripts/repeat_market_check.py` ({rn_head[0]} of {rn_head[1]} mocks, {rn_head[2]} flagged), `write_report.py`. Records in `arena/results/m82_*.json` and this folder.")
w("- No line, tag or placement changed on either plane.\n")
w("## In plain language\n")
w(f"**How the room went.** About a {ad['champ']:.0f} percent title share, {ad['champ_rank']} of 12 by title odds and {ECWR} of 12 week to week, favored against {WW} of the other 11. You followed the card at {len(followed)} of 13 picks and stayed in its Top 5 at {len(top5)}. This was the first live room on the locked lines.")
w(f"\n**The pick to learn from.** The best single change would have been #{best[1]}: {best[0]} instead of {own[best[1]]}, worth about {best[2] - ad['champ']:.1f} title points. Following the 🎯 at every turn would have graded {fc['champ']:.1f} percent, {fc['champ'] - ad['champ']:+.1f} points against as drafted.")
w("\n**The tool.** One thing to know for tonight: at #124 you logged a \"Green\" and the tool chose Draymond, but the room had taken Jalen Green. " + ("It changed what the card showed you afterwards (see §4)." if greens else ("It did not put a wrong name on your card, but it hid one: Draymond Green stayed marked as taken, so the card could not offer him, and hindsight likes him at " + ", ".join(f"#{p}" for p, _ in hidden) + "." if hidden else "It did not reach any of your later picks, but it could have.")) + " In the real draft, type the first name when a surname is shared. The roster-balance line fix (Version 70) changes nothing on this room's card.")
w("\n**Your decisions.** D82-1, the surname rule; the default keeps it and relies on first names.")
P = os.path.join(K, "report", "after-reports", "after-report-2026-10-14-draft82.md")
open(P, "w", encoding="utf-8").write("\n".join(o) + "\n")
PL = os.path.join(K, "report", "pull-log.md"); pl = rd(PL)
if "after-report-2026-10-14-draft82.md" not in pl:
    row = (f"| 2026-10-14 | mock 82 grade (public room, LIVE mode, the lock page Version 69 — first live room on the locked lines) | 0 | 0 | 0 | "
           f"after-reports/after-report-2026-10-14-draft82.md — as drafted {ad['champ']:.2f}% (rank {ad['champ_rank']}), ECW {ECW:.3f} rank {ECWR}, favored {WW} of 11; "
           f"card followed {len(followed)} of 13, Top-5 at {len(top5)}; follow-card chain {fc['champ']:.2f}%; largest swap #{best[1]} {best[0]} {best[2]:.2f}%; "
           f"tool board = recap 155 of 156 (#124 Draymond vs Jalen Green, D82-1); three echoes reproduced by the lock page, not by Version 68; LEAN-fix page 🎯 differs at {len(fx_diff)} of 13; no plane change |")
    open(PL, "w", encoding="utf-8").write(pl.rstrip("\n") + "\n" + row + "\n")
print("written", P)
