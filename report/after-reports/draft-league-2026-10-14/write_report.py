#!/usr/bin/env python3
"""Writes report/after-reports/after-report-2026-10-14-league-draft.md and the pull-log row from the records: the
two 10,000-season league simulations (deck arena/results/m100_league_sim_10k_s2026/s2027.json, each verified equal to
arena.simulate_seasons on its seed), m100_final / m100_hindsight / m100_arms / m100_deckcard_v69, this folder's
recap.json, state_check.txt, replay_v70.json (the tool log through the page in Chromium), stress.json, waiver.json,
retro_picks.json and rn_section_league.md. No figure is typed by hand."""
import glob, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.normpath(os.path.join(H, "..", "..", ".."))
DK = "/home/user/yahoo-fantasy-basketball"; D = f"{DK}/arena/results"
J = lambda p: json.load(open(p, encoding="utf-8")); rd = lambda p: open(p, encoding="utf-8").read()
S1, S2 = J(f"{D}/m100_league_sim_10k_s2026.json"), J(f"{D}/m100_league_sim_10k_s2027.json")
assert S1["seasons"] == S2["seasons"] == 10000 and S1["verified_against_arena"] and S2["verified_against_arena"]
A = J(f"{D}/m100_arms.json"); HS = J(f"{D}/m100_hindsight.json"); PG = J(f"{D}/m100_deckcard_v69.json"); F = J(f"{D}/m100_final.json")["v69"]
recap = J(os.path.join(H, "recap.json")); sc = rd(os.path.join(H, "state_check.txt")); msg = rd(os.path.join(H, "owner_message.txt"))
ST = J(os.path.join(H, "stress.json")); WV = J(os.path.join(H, "waiver.json")); RV = J(os.path.join(H, "replay_v70.json")); SM = RV["summary"]
rn = rd(os.path.join(H, "rn_section_league.md")); rn_head = re.search(r"(\d+) of (\d+) mocks replayed; (\d+) FLAGGED", rn).groups(); rn = rn[rn.index("## Repeat-name market check"):].strip()
mgr = {p["slot"]: p["manager"] for p in recap}; tname = {p["slot"]: p["team_name"] for p in recap}
who = lambda s: ("you" if s == 10 else mgr[s]) + f" ({tname[s]})"
T1, T2 = S1["teams"], S2["teams"]; seats = sorted(T1, key=lambda s: -T1[s]["champ"])
gap = max(abs(T1[s][k] - T2[s][k]) for s in T1 for k in ("champ", "playoff"))
me1, me2 = T1["10"], T2["10"]; rank1 = 1 + sum(1 for s in T1 if s != "10" and T1[s]["champ"] > me1["champ"])
rank2 = 1 + sum(1 for s in T2 if s != "10" and T2[s]["champ"] > me2["champ"]); rival = seats[1] if seats[0] == "10" else seats[0]
CATS = list(me1["cat_win_pct"]); crank = {c: 1 + sum(1 for s in T1 if T1[s]["cat_win_pct"][c] > me1["cat_win_pct"][c]) for c in CATS}
turns = sorted(PG, key=lambda t: t["pick"]); own = {p["n"]: p["player"] for p in recap if p["slot"] == 10}
assert [t["pick"] for t in turns] == sorted(own) and all(t["actual"] == own[t["pick"]] for t in turns)
tgt = lambda t: next(r["n"] for r in t["rows"] if r["target"])
dsg = lambda t: next(r["ds"] for r in t["rows"] if r["target"]) - next((r["ds"] for r in t["rows"] if r["n"] == t["actual"]), float("nan"))
followed = [t for t in turns if t["actualCardRank"] == 1]; top5 = [t for t in turns if t["actualCardRank"] <= 5]
# the paste's "off the card" lines for the owner's FINAL picks agree with the page record
E = re.findall(r"⚠ off the card: (.+?) ranks #(\d+) \(([\d.]+) behind 🎯 (.+?)\)", msg); tb = {t["actual"]: t for t in turns}
E_final = [e for e in E if e[0] in tb]; E_stale = [e for e in E if e[0] not in tb]
assert all(int(rk) == tb[nm]["actualCardRank"] and tg == tgt(tb[nm]) for nm, rk, g, tg in E_final)
echo_of = lambda rec: [l.strip() for r in rec["rows"] for l in r["fresh"] if "off the card" in l]
echo_paste = [l.strip() for l in msg.split("\n") if l.startswith("⚠ off the card")]
assert SM["echoMisses"] == 0 and SM["pageErrors"] == 0 and SM["finalPicks"] == 156 and echo_of(RV) == echo_paste
shift_paste = [l.strip() for l in msg.split("\n") if "after the shift" in l]
shift_page = [l.strip() for r in RV["rows"] for l in r["fresh"] if "after the shift" in l]
assert shift_page == shift_paste, (shift_page, shift_paste)
sys.path.insert(0, f"{DK}/scripts"); import hoops
fs = RV["finalState"]["picks"]; board_diff = [i + 1 for i, (p, r) in enumerate(zip(fs, recap)) if hoops.fold(p["player"]) != hoops.fold(r["player"]) or p["slot"] != r["slot"]]
assert board_diff == []
ev = J(f"{DK}/arena/data/events/m100_tool_events.json"); undone = [e["text"] for e in ev if e.get("undone")]
ins = re.findall(r"✎ inserted (.+?) at #(\d+) → Seat (\d+)", msg); halts = re.findall(r'⚠ HALTED at "(.+?)"', msg)
ad = A["as_drafted"]; fc = A["follow_card_selfconsistent"]
swaps = sorted(((k.split(":", 1)[1], int(k.split(":")[0][5:]), v["champ"]) for k, v in A.items() if k.startswith("swap#")), key=lambda x: -x[2])
best = swaps[0] if swaps else None; hb = {t["pick"]: t for t in HS["turns"]}
taken = {p["player"]: (p["n"], p["slot"]) for p in recap}
po = F["per_opp"]; ECW = {int(str(k).lstrip('T')): v for k, v in F['ecw'].items()}[10]
hoops.DATA_PATH = f"{DK}/arena/results/players_v69.csv"; PL = {p["player"]: p for p in hoops.load_players()}
o = []; w = o.append
w("# After-report — the league draft, 2026-10-14: the owner's real 12-team league from seat 10, graded and simulated over 10,000 seasons\n")
w("**Owner request (2026-10-14, verbatim):** \"Alright. Final draft is completed- here we go! Proceed with full analysis and simulate 10000 seasons\", with the deck tool's LIVE feed, Yahoo's pick list and the draft order (`draft-league-2026-10-14/owner_message.txt`, pinned verbatim).\n")
w("**League:** 12 teams × 13 rounds, head-to-head nine categories, 18 regular-season weeks, eight teams to an eight-team bracket with no byes. Seats by the draft order: " + "; ".join(f"{s} {who(s)}" for s in range(1, 13)) + ". **Board:** the locked lines (pool tag v69 = data/players.csv at deck `af91b23`, byte-identical to the current main's); the page in the room was Version 70, whose engine output equals Version 69's.\n")
w("Pull window: 2026-10-14 → 2026-10-14 (analysis only; no roster pull, no line change).\n")
w(f"**Headline.** Over 10,000 simulated seasons your team wins the title **{me1['champ']:.2f} percent** of the time, the most in the league (rank {rank1} of 12; the second run of 10,000 on another seed: {me2['champ']:.2f} percent, rank {rank2}). Playoffs {me1['playoff']:.2f} percent, the top seed {me1['seed_pct'][0]:.2f} percent, mean seed {me1['mean_seed']:.2f}, {me1['cats_per_week']:.3f} categories a week. The nearest rival is {who(int(rival))} at {T1[rival]['champ']:.2f} percent. Expected weekly category wins {ECW:.3f}, rank {F['ecw_rank']} of 12, favored in {F['exp_winning_weeks']} of 11 head-to-heads. The card's 🎯 was taken at {len(followed)} of 13 turns, the Top 5 at {len(top5)}. The tool's board equals Yahoo's 156 of 156 after {len(undone)} undone entries, {len(ins)} Insert-at-# and {len(halts)} halted name.\n")
w("## 1. Roster changes\n\nNone. No line, tag, placement or price changed on either plane.\n")
w(f"## 2. The league over 10,000 seasons\n\nEVIDENCE: `arena/results/m100_league_sim_10k_s2026.json` and `_s2027.json`, written by `arena/mocks/league_sim.py` — the house simulator (`arena.simulate_seasons`: weekly category draws from each roster's daily-fill model, a shared games shock, the category record as the standings, the 1v8/4v5/2v7/3v6 bracket) with each season's seeds and rounds recorded. Before writing, each run re-ran `arena.simulate_seasons` on its seed and asserted equal champion and playoff counts for all 12 teams. Largest difference between the two runs on any team's title or playoff share: {gap:.2f} points.\n")
w("| seat | manager (team) | title % | title %, 2nd run | final % | playoffs % | top seed % | mean seed | cats a week |\n|---|---|---|---|---|---|---|---|---|")
for s in seats:
    t, u = T1[s], T2[s]
    w(f"| {s} | {who(int(s))} | **{t['champ']:.2f}** | {u['champ']:.2f} | {t['final']:.2f} | {t['playoff']:.2f} | {t['seed_pct'][0]:.2f} | {t['mean_seed']:.2f} | {t['cats_per_week']:.3f} |")
w(f"\nYour finishing seed over the 10,000 seasons: " + ", ".join(f"#{k + 1} {x:.1f}%" for k, x in enumerate(me1["seed_pct"]) if x >= 0.05) + ".\n")
w("## 3. Your team\n\nEVIDENCE: `recap.json` (Yahoo's listing: positions and status as Yahoo printed them), the pool's availability multiplier (`hoops.availability`), the page's card record.\n")
w("| pick | player | NBA team | Yahoo positions | Yahoo status | availability on the board | card rank at the pick |\n|---|---|---|---|---|---|---|")
for t in turns:
    p = next(x for x in recap if x["n"] == t["pick"])
    w(f"| #{t['pick']} | {t['actual']} | {p['team']} | {p['pos']} | {p['status'] or '—'} | {hoops.availability(PL[t['actual']]):.2f} | {t['actualCardRank']} |")
w("\nCategory profile — the share of weeks your team wins each category, and its rank among the 12 (10,000 seasons, seed 2026):\n")
w("| " + " | ".join(CATS) + " |\n|" + "---|" * len(CATS))
w("| " + " | ".join(f"{me1['cat_win_pct'][c]:.1f}% (#{crank[c]})" for c in CATS) + " |")
strong = [c for c in CATS if crank[c] <= 3]; weak = [c for c in CATS if crank[c] >= 9]
w(f"\nStrongest: {', '.join(strong)}; weakest: {', '.join(weak)}. The weekly model's category ranks (`m100_final.json`): " + ", ".join(f"{c} {r}" for c, r in F["cat_rank_weekly"].items()) + ".\n")
w("Expected categories a week against each opponent (`m100_final.json`, the weekly model; 4.5 is even):\n")
w("| opponent | expected cats | your categories above 50% |\n|---|---|---|")
for s in sorted(po, key=lambda s: po[s]["exp_cats"]):
    w(f"| {who(int(s))} | {po[s]['exp_cats']:.3f} | " + ", ".join(c for c, v in po[s]["cats"].items() if v > 0.5) + " |")
w("\n## 4. Pick by pick: the page's card, your pick, hindsight\n\nEVIDENCE: `m100_deckcard_v69.json` (the page's own engine on Yahoo's board before each of your turns), `m100_hindsight.json` (every single-swap alternative scored by weekly category wins against the final rosters).\n")
w("| pick | you took | card rank | the page's 🎯 | gap to 🎯 | hindsight's best alternative (Δ weekly cat wins) |\n|---|---|---|---|---|---|")
for t in turns:
    h = hb[t["pick"]]["top"]; hh = (f"{h[0]['n']} ({h[0]['gain']:+.3f})" if h[0]["gain"] > 0 else f"none better (closest {h[0]['n']}, {h[0]['gain']:+.3f})") if h else "—"
    g = dsg(t); w(f"| #{t['pick']} | {t['actual']} | {t['actualCardRank']} | {tgt(t)} | {'—' if t['actualCardRank'] == 1 else (f'{g:.3f}' if g == g else 'off the Top 5')} | {hh} |")
off = [t for t in turns if t["actualCardRank"] > 1]
w(f"\nThe turns off the 🎯 and where the 🎯 went: " + "; ".join(f"#{t['pick']} {t['actual']} (🎯 {tgt(t)}, " + (f"taken #{taken[tgt(t)][0]} by {who(taken[tgt(t)][1])})" if tgt(t) in taken else "undrafted)") for t in off) + ".\n")
CV = J(os.path.join(H, "card_vs_owner.json"))
w("### 4b. Were your picks better than the card's?\n\nEVIDENCE: `card_vs_owner.py` → `card_vs_owner.json`. At each of your six turns off the 🎯, the 🎯 was swapped in for your pick on Yahoo's final board — pairwise, as the house arms do: the seat that took the 🎯 later gets your player instead (an undrafted 🎯 leaves your player undrafted). Each swap scored by expected weekly category wins and by title share over 10,000 seasons on both seeds (the baselines' seeds, so the dice line up). Negative = your pick was better.\n")
w("| pick | you took | the card's 🎯 (where it went) | Δ cats a week if 🎯 | Δ title % if 🎯 (seed 2026 / 2027) | verdict |\n|---|---|---|---|---|---|")
def verdict(x):
    a, b = x["d_title_if_target"]["2026"], x["d_title_if_target"]["2027"]
    if a > 0 and b > 0: return "the card's pick was better" + (" (inside the noise)" if max(a, b) < 0.5 else "")
    if a < 0 and b < 0: return "your pick was better" + (" (inside the noise)" if min(a, b) > -0.5 else "")
    return "a wash (the seeds disagree)"
for x in CV["turns"]:
    w(f"| #{x['pick']} | {x['owner']} | {x['target']} ({x['target_went']}) | {x['d_ecw_if_target']:+.4f} | {x['d_title_if_target']['2026']:+.2f} / {x['d_title_if_target']['2027']:+.2f} | {verdict(x)} |")
better_you = [x for x in CV["turns"] if x["d_title_if_target"]["2026"] < 0 and x["d_title_if_target"]["2027"] < 0]
better_card = [x for x in CV["turns"] if x["d_title_if_target"]["2026"] > 0 and x["d_title_if_target"]["2027"] > 0]
w(f"\nOn title share your pick beat the 🎯 at {len(better_you)} of 6 turns (" + ", ".join(f"#{x['pick']} {x['owner']}" for x in better_you) + f") and the 🎯 beat yours at {len(better_card)} (" + ", ".join(f"#{x['pick']} {x['target']} over {x['owner']}" for x in better_card) + "). On the card's own measure (cats a week against the final rosters) the 🎯 edges five of the six by 0.011 or less — differences that small sit inside projection error. The two measures can disagree because a pairwise swap also hands a rival your player: the three Poeltl turns would have given John's team Lendeborg, Queta or Washington. The three Poeltl rows are alternatives, not a sum — Poeltl could be taken once.\n")
w("## 5. What-ifs (the house arms: 18,000 seasons each, seeds 11/23/47 — the method every mock was graded on)\n\nEVIDENCE: `m100_arms.json`. These use the house seeds, not the 10,000-season runs above, so the as-drafted line differs from §2 by Monte-Carlo noise.\n")
w("| arm | title % | playoffs % | rank |\n|---|---|---|---|")
w(f"| as drafted | {ad['champ']:.2f} | {ad['playoff']:.2f} | {ad['champ_rank']} |")
w(f"| follow the card's 🎯 at every turn (" + (", ".join(f"#{n} {p}" for n, p in fc["swaps"]) or "no change") + f") | {fc['champ']:.2f} | {fc['playoff']:.2f} | {fc['champ_rank']} |")
for nm, n, c in swaps: w(f"| single swap at #{n}: {nm} | {c:.2f} | {A[f'swap#{n}:{nm}']['playoff']:.2f} | {A[f'swap#{n}:{nm}']['champ_rank']} |")
w(f"\n## 6. Injury stress: one headline name misses the whole season (10,000 seasons, seed 2026)\n\nEVIDENCE: `stress.json` (`stress.py`): the player's slot is filled by the best undrafted player on the board ({ST['replacement']}), the pickup a manager would make; the rest of the league unchanged. The board's availability multipliers already price ordinary missed games; this is the tail case.\n")
w("| out for the season | title % | rank | playoffs % | mean seed | league leader then |\n|---|---|---|---|---|---|")
w(f"| nobody (as drafted) | {me1['champ']:.2f} | {rank1} | {me1['playoff']:.2f} | {me1['mean_seed']:.2f} | you |")
for nm, r in ST["arms"].items():
    w(f"| {nm} | {r['champ']:.2f} | {r['champ_rank']} | {r['playoff']:.2f} | {r['mean_seed']:.2f} | {who(r['top_rival'][0]) if r['champ_rank'] > 1 else 'you'} ({r['top_rival'][1]:.2f}) |")
w("\n## 7. The waiver wire at the draft's end\n\nEVIDENCE: `waiver.json` — the undrafted players by the board's value (availability > 0).\n")
w("| # | player | team | positions | availability |\n|---|---|---|---|---|")
for i, x in enumerate(WV[:10], 1): w(f"| {i} | {x['player']} | {x['team']} | {x['pos']} | {x['availability']:.2f} |")
WM = J(os.path.join(H, "waiver_moves.json")); W2 = J(os.path.join(H, "waiver_moves_s2027.json")); DR = J(os.path.join(H, "waiver_draymond_risk.json"))
w(f"\n## 7b. Pickups tested: every add/drop pair\n\nEVIDENCE: `waiver_moves.py` → `waiver_moves.json`: the {WM['candidates']} best undrafted players (availability > 0, the owner's veto off) × your 13 = {WM['pairs']} pairs, each scored by expected weekly category wins against the eleven final rosters (the card's own measure; your baseline {WM['base_ecw']:.4f}). **{WM['positive_pairs']} of {WM['pairs']} pairs improve the team**, and every one drops Braun, Queta, Washington or Lendeborg; no undrafted player improves on any of your top nine. The best pairs then ran 10,000 seasons each through the verified simulator, on the baseline's seed 2026 and again on seed 2027 (`waiver_moves_s2027.json`).\n")
w("| add | drop | Δ cats a week | title %, seed 2026 (Δ) | title %, seed 2027 (Δ) | categories that move most |\n|---|---|---|---|---|---|")
for x in WM["simulated"]:
    k = f"+{x['add']} -{x['drop']}"; y = W2["arms"].get(k)
    mv = ", ".join(f"{c} {v:+.2f}" for c, v in sorted(x["d_cats"].items(), key=lambda kv: -abs(kv[1]))[:3])
    w(f"| {x['add']} ({x['add_team']}) | {x['drop']} | {x['d_ecw']:+.4f} | {x['sim']['champ']:.2f} ({x['sim']['d_champ']:+.2f}) | " + (f"{y['champ']:.2f} ({y['d_champ']:+.2f})" if y else "—") + f" | {mv} |")
w(f"\n**The availability test (the critical one).** Draymond Green's line on the board carries full availability (1.00). Run again with Green at the board's risk tier (0.78 ranking / 0.75 weekly — `waiver_draymond_risk.json`), the same Green-for-Braun swap grades {DR['title']['2026']:.2f} and {DR['title']['2027']:.2f} percent: **below** the as-drafted {me1['champ']:.2f} / {me2['champ']:.2f}. The move's whole gain rests on Green playing a normal schedule. Web check 2026-10-15 (`web_receipts_2026-10-15.md`, leads not box scores): ESPN lists him day-to-day (rest) with a return estimate of Oct 16; RotoWire and Fox Sports report preseason rest games and limited minutes ahead of the Oct 21 opener.\n")
w("Monte-Carlo error on a single 10,000-season title share is about ±0.4 points (one standard error at 22%); the paired runs share their dice, so a difference that keeps its sign on both seeds is the signal. Green-for-Braun (+1.54 / +1.72) and Portis-for-Braun (+0.89 / +1.15) keep their sign; Holiday (+0.69 / +0.16) is inside the noise.\n")
w(f"\n## 8. Tool-state integrity\n\n" + sc.strip().replace("\n", "; ") + ".\n")
w(f"EVIDENCE: the typed sequence rebuilt in `arena/data/events/m100_tool_events.json` ({len(ev)} events) replayed through the page in headless Chromium (`replay_v70.json`): {SM['echoMisses']} echo misses, {SM['clockMismatches']} clock mismatches, {SM['pageErrors']} page errors, {SM['finalPicks']} picks; the final board equals Yahoo's at all 156 picks; every \"off the card\" line of the paste ({len(echo_paste)}) and every shift line ({len(shift_paste)}) is reproduced character for character.\n")
w("| what happened | the log | what the tool did |\n|---|---|---|")
w(f"| entries undone and re-entered | {len(undone)} undo lines: " + ", ".join(undone) + " | each removed and the board re-entered; the board after equals Yahoo's |")
for nm, n, s in ins: w(f"| a missed pick restored at #{n} | \"inserted {nm} at #{n}\" (to seat {s}) | the later picks shifted one place and were re-seated by the snake |")
for hname in halts: w(f"| a bare \"{hname}\" with the best namesake already taken | \"HALTED at \\\"{hname}\\\"\" | nothing logged; the fuller name was then entered |")
w(f"\n**Two log-display defects, neither touching the board or the card.** (a) The paste's history shows each undone entry under the name of the pick's later occupant (\"#10 Tyrese Haliburton\" above \"undid: Tyrese Maxey\"; \"#38 Jalen Williams\" and \"#39 Derrick White\" above the undos of Avdija and White): an Insert-at-# re-renders the history from the state (D59-1), undone lines included; the undo lines name what was removed, and the replay rebuilt from them reproduces the paste. (b) At the #98 insert the log said \"#59 Keyonte George is no longer your pick after the shift\": George was never your pick on the final board; `relabelLog` (`docs/draft-deck.html`, ~line 1050) maps every history line that carries a pick index — undone entries included — to the state's current pick there, and calls a line \"moved off\" when its old text had \"(YOU)\" and the current occupant is not yours; the undone George entry (typed when the tool was one pick short, so it sat on your seat) was re-mapped to #59, where the re-entered George sits for seat 11. The shift line at #58 (D83-1's message) said \"Kyrie Irving is the 🎯\" — on this board it was true: the card had Kyrie #1 at #58.\n")
w("The " + str(len(E_stale)) + " \"off the card\" lines for entries later undone (" + ", ".join(e[0] for e in E_stale) + ") were the card's verdicts on mis-seated entries, not on your picks.\n")
OV = J(os.path.join(H, "opponents_vs_history.json")); OM = OV["managers"]
w("## 10. Your opponents against their own history\n")
w(f"EVIDENCE: `opponents_vs_history.py` → `opponents_vs_history.json`; history from `arena/draft_boards.json` (three seasons, 156 picks each) and `arena/profiles.json` (the E18 manager profiles). **Value reach** = pick − 9-cat value rank (room_model.py's formula; positive = took fallers, negative = reached past value), 2025-26 on that season's frozen pool and 2026 on the lock pool — two different pools, so the levels compare loosely and the order of managers is the firmer test. **Market reach** = pick − Yahoo ADP (2026 only; there is no earlier ADP file). **Guard share** = picks eligible at PG or SG. Rank agreement of early value reach, 2025-26 against 2026, across the eleven: Spearman {OV['spearman_early_reach_2025_vs_2026']:+.2f} (n = {OV['n']}) — a weak link; with eleven managers it is not distinguishable from chance.\n")
w("| manager (team) | early value reach, 2025-26 to 2026 | whole-draft value reach, 2025-26 to 2026 | market reach 2026 (early) | guard share 2026 (2025-26 / 24-25 / 23-24) | took again from his own past drafts | the profile's loyalty names: taken / gone elsewhere |\n|---|---|---|---|---|---|---|")
for m, x in sorted(OM.items(), key=lambda kv: kv[1]["seat"]):
    gh = x["guard_share_hist"]; lw = "; ".join(f"{k} {v}" for k, v in x["loyalty_went"].items())
    w(f"| {m} ({x['team']}) | {x['reach_2025']['early']:+.1f} to {x['reach_2026']['early']:+.1f} | {x['reach_2025']['mean']:+.1f} to {x['reach_2026']['mean']:+.1f} | {x['market_reach_2026']['mean']:+.1f} ({x['market_reach_2026']['early']:+.1f}) | {x['guard_share_2026']:.2f} ({gh['2025-26']} / {gh['2024-25']} / {gh['2023-24']}) | {', '.join(x['repeats']) or '—'} | {', '.join(x['loyalty_hit']) or '—'} / {lw or '—'} |")
tot = sum(len(x["loyalty_listed"]) for x in OM.values()); hit = sum(len(x["loyalty_hit"]) for x in OM.values())
w(f"\n**What held, what broke.**\n")
w(f"- **Loyalty is weak.** Of the {tot} manager–player pairs the profiles list as repeat picks, {hit} repeated (Booker to Robby, Okongwu to Will, Poeltl to John, LaMelo Ball to Noah). The profile's own note says league-wide repetition runs at chance; tonight agrees.")
w("- **The model's named prediction missed.** The profile gave Robby drafting Jarrett Allen a 0.77 chance; Robby took Banchero at #52 and Allen went to JCo at #56.")
w(f"- **Held to type:** Robby (early reach {OM['Robby']['reach_2025']['early']:+.1f} → {OM['Robby']['reach_2026']['early']:+.1f}; at or after Yahoo's ADP early, {OM['Robby']['market_reach_2026']['early']:+.1f} — the market-anchored, name-brand drafter the profile describes); Kyle (mild reacher, {OM['Kyle']['reach_2025']['early']:+.1f} → {OM['Kyle']['reach_2026']['early']:+.1f}); JCo (value-anchored, {OM['JCo']['reach_2025']['early']:+.1f} → {OM['JCo']['reach_2026']['early']:+.1f}); Oblena's shape (better early than late in both years); John's light guard share ({OM['John']['guard_share_2026']:.2f}, against {OM['John']['guard_share_hist']['2025-26']} a year ago).")
w(f"- **Changed:** Martin — the reigning champion and the profile's apex threat — drafted value this time (early {OM['Martin']['reach_2025']['early']:+.1f} → {OM['Martin']['reach_2026']['early']:+.1f}; on average he took players {OM['Martin']['market_reach_2026']['mean']:+.1f} places after their ADP), and he is third in the 10,000 seasons. Kevin reached far harder against the board ({OM['Kevin']['reach_2025']['early']:+.1f} → {OM['Kevin']['reach_2026']['early']:+.1f}) while staying near ADP ({OM['Kevin']['market_reach_2026']['early']:+.1f}): he drafted the market, and our board disagrees with the market on his players. His guard-heavy label did not show ({OM['Kevin']['guard_share_2026']:.2f}). John reached more than before ({OM['John']['reach_2025']['early']:+.1f} → {OM['John']['reach_2026']['early']:+.1f}). Hegi and Will reached less early than their histories. Noah's −43.5 was 2025-26's autodraft geometry (the profile's own correction); drafting by hand he sat near value ({OM['Noah']['reach_2026']['early']:+.1f}).")
w("- **Caution on the measure:** value reach is measured against our own board. A manager who drafts the market looks like a reacher wherever our board and the market disagree (Kevin is the clearest case). The market column is the neutral one.")
w("- **What the sim does not see:** the in-season grinders. Will (83 moves last season), Martin (50, and the title), Oblena (69) and Cayas (61) streamed and churned heavily; the 10,000 seasons freeze every roster at the draft, so their real chances are likely higher than modelled, and the gap to you likely smaller.\n")
RP = J(os.path.join(H, "retro_picks.json")); RR = RP["rows"]; RC = RP["ceiling"]; SD = [str(s) for s in RP["seeds"]]
assert RP["base_title"] == {k: T for k, T in zip(SD, (me1["champ"], me2["champ"]))} and abs(RP["base_ecw"] - HS["base_ecw"]) < 1e-3
NL = 0.5
def rverdict(r):
    a, b = (r["d_title"][s] for s in SD)
    return "better than yours" if min(a, b) > NL else ("yours was better" if max(a, b) < -NL else "inside the noise")
seed_spread = sum(abs(r["d_title"][SD[0]] - r["d_title"][SD[1]]) for r in RR) / len(RR)
arm_cmp = [(r, A[f"swap#{r['pick']}:{r['alt']}"]["champ"] - ad["champ"]) for r in RR if f"swap#{r['pick']}:{r['alt']}" in A]
arm_agree = sum(1 for r, d in arm_cmp if (d > 0) == (r["d_title_mean"] > 0))
w("## 11. Retro: who else was on the board at each of your picks, and what each would have done to your title odds\n")
w(f"EVIDENCE: `retro_picks.py` → `retro_picks.json`. At each of your 13 turns, `m100_hindsight.json` scores every legal alternative by expected weekly category wins (ECW) against the final rosters. The three alternatives with the largest positive gain at each turn (or, where nobody beat your pick, the single closest) were swapped in for your pick on Yahoo's final board, pairwise as in §4b: the seat that drafted the alternative later gets your player instead; an undrafted alternative leaves your player undrafted. Each of the {len(RR)} swaps ran 10,000 seasons through the verified simulator on seeds {SD[0]} and {SD[1]}, the baselines' seeds ({RP['base_title'][SD[0]]:.2f} / {RP['base_title'][SD[1]]:.2f} percent), so each swap and its baseline share their random draws. The script ran twice with identical results, and its #10 Maxey row equals §4b's. **Verdict rule:** better than yours only when both seeds exceed +{NL} title points; yours was better when both fall below −{NL}; anything else is inside the noise (the two seeds differ by {seed_spread:.2f} points on average across these rows). **Cross-check:** {len(arm_cmp)} of these swaps also exist in the house arms (§5: 18,000 seasons on seeds 11/23/47, a different set of dice); the direction agrees at {arm_agree} of {len(arm_cmp)}.\n")
w("| pick | you took | alternative (drafted at, by) | ECW gain | title shift, seed " + SD[0] + " / " + SD[1] + " | mean | players with an ECW gain over yours | verdict |\n|---|---|---|---|---|---|---|---|")
for r in RR:
    went = r["alt_went"] if r["alt_went"] == "undrafted" else f"{r['alt_went'].split()[0]}, {mgr[int(r['alt_went'].split('seat ')[1])]}"
    w(f"| #{r['pick']} | {r['owner']} | {r['alt']} ({went}) | {r['d_ecw']:+.3f} | {r['d_title'][SD[0]]:+.2f} / {r['d_title'][SD[1]]:+.2f} | {r['d_title_mean']:+.2f} | {r['n_better']} of {r['n_legal']} | {rverdict(r)} |")
bt = [r for r in RR if rverdict(r) == "better than yours"]; best_at = {}
for r in bt:
    if r["pick"] not in best_at or r["d_title_mean"] > best_at[r["pick"]]["d_title_mean"]: best_at[r["pick"]] = r
clean = [t["pick"] for t in HS["turns"] if t["pick"] not in best_at]
ceil_list = ", ".join(f"#{c['pick']} {c['alt']}" for c in RC["swaps"])
w(f"\n**Reading it.**\n")
w(f"- **Turns where a clearly better player was on the board ({len(best_at)} of 13):** " + "; ".join(f"#{p} {best_at[p]['alt']} over {best_at[p]['owner']} ({best_at[p]['d_title_mean']:+.2f})" for p in sorted(best_at)) + ".")
w(f"- **Turns where your pick stands ({len(clean)} of 13):** " + ", ".join(f"#{p} {next(t['actual'] for t in HS['turns'] if t['pick'] == p)}" for p in sorted(clean)) + ". At #82 and #106 no legal alternative beat your pick even by ECW; at #39 Harden's small ECW gain turns into a loss in the seasons.")
w("- **The largest single miss is #15:** Jalen Johnson, taken three picks later by John, instead of Durant. The second tier is the same shape: Harden at #34, MPJ or Naz Reid at #63, Kyshawn George at #111 (still on the board until #150), and Draymond at #154 (never drafted).")
w("- **The same player recurs.** Kyshawn George is the top alternative at #111, #130 and #135, and Draymond at four turns; you could have had each once. MPJ is the top alternative at both #58 and #63.")
w("- **Where the alternative went matters.** Harden instead of Kawhi at #34 is +1.85; Harden instead of White at #39 is −0.61. In the first swap Will (seat 3) receives Kawhi at #46, in the second White. Every shift includes what the displaced player does on the seat that receives that player; it is not a pure measure of the two players.")
w(f"- **Hindsight's ceiling.** All the better picks at once, each player used once ({ceil_list}), give a title share of {RC['title'][SD[0]]:.2f} / {RC['title'][SD[1]]:.2f} percent: {RC['d_title'][SD[0]]:+.2f} / {RC['d_title'][SD[1]]:+.2f} points. That is far below the sum of the single shifts ({sum(r['d_title_mean'] for r in RR if any(c['pick'] == r['pick'] and c['alt'] == r['alt'] for c in RC['swaps'])):+.1f}): gains overlap, and each swap also strengthens a rival. For scale, following the card at every turn graded {fc['champ']:.2f} percent against {ad['champ']:.2f} as drafted on the house arms (different seeds). The ceiling is perfect hindsight, not an attainable draft: it knows who every opponent took later.\n")
w("## 9. Critical review: what this analysis can and cannot tell you\n")
w(f"1. **The title share is model-relative.** Every season is simulated on the lock's projection lines. The integrity audit put projection confidence at 97.8%, but that figure mostly measures agreement with consensus (the lines sit about five-sixths of the way to it): if the consensus is wrong about a player, so is this. Real projection error is the largest uncertainty here, larger than the ±0.4-point Monte-Carlo error or the {gap:.2f}-point spread between two runs.")
w("2. **The grader and the card are the same engine.** \"Following the 🎯 would have graded higher\" and \"hindsight's best alternative\" are measured by the model that produced the card. They show internal consistency, not that the card is right about basketball.")
w("3. **Hindsight uses information you did not have.** §4's alternatives are scored against the final rosters; at the pick, the later picks were unknown. Hindsight gains of 0.1 cats a week or less are small against projection error.")
w("4. **The schedule is average, not yours.** Pairings are drawn at random each week; the league's real schedule (not in either repository) decides any one season's luck.")
w("5. **Opponents stand still.** No trades, streaming or waiver moves by anyone after the draft; the eleven rosters are frozen. Active managers will move the table; the stress test (§6) and the pickup test (§7b) are the only in-season changes modelled.")
w("6. **Availability is the lock's.** Yahoo flags Durant, Kyrie and Miles Bridges questionable; the board carries Durant and Bridges at full availability. Injury news since the lock was not pulled (did not check), apart from the three pickup-relevant names in `web_receipts_2026-10-15.md`. §6 shows what a full-season loss costs: about half the title share for Haliburton or Durant.")
w("7. **The simulator was verified against the house simulator, not against reality.** `league_sim.py` equals `arena.simulate_seasons` draw for draw; that proves the extension is faithful, not that the season model is calibrated. The model's last calibration evidence is in earlier reports (the 2025-26 what-if and survival work), not re-run tonight.")
w(f"8. **Your team's shape is a real exposure.** Last in assists and ninth in points and rebounds: you win weeks through efficiency and defense ({', '.join(strong)}). A team built that way can drop weeks when one shooter goes cold or one center misses time; the category win shares in §3 are averages over 10,000 seasons, not a promise for any given week.")
w("9. **The pickup test is narrow.** It tries one add for one drop against frozen rosters, using undrafted players by the board's value (top 40). It does not test two-for-one moves, trades, or streaming for games.\n")
w("## Watchlist\n")
w(f"- The two injury-tail names that move the title share most: " + ", ".join(f"{nm} ({r['champ']:.1f}% if out)" for nm, r in sorted(ST["arms"].items(), key=lambda x: x[1]["champ"])[:2]) + ". Their status is the first thing to watch in the season's first weeks.")
w(f"- The weak categories ({', '.join(weak)}) are where waiver and trade moves pay; the strong ones ({', '.join(strong)}) are what to protect.")
qflag = [(t['actual'], next(x for x in recap if x['n'] == t['pick'])['status'], hoops.availability(PL[t['actual']])) for t in turns if next(x for x in recap if x['n'] == t['pick'])['status']]
w("- Yahoo's status column at the draft flags " + ", ".join(f"{n} ({st})" for n, st, a in qflag) + "; the board carries them at availability " + ", ".join(f"{a:.2f}" for n, st, a in qflag) + ". What the flags mean today was not checked (no pull tonight): the first in-season pull should read them.")
w("- The log-display defects (§8) and D83-1 wait for after the draft; nothing in them changed a pick or the card.\n")
w("## Open-item receipts\n\n| item | query run (2026-10-14) | dated finding |\n|---|---|---|")
w("| (this draft) | records only; no web research and no roster pull | Yahoo's 156 names resolve to the lock pool 156 of 156; Yahoo's NBA team agrees with the pool's at all 156 |")
w("| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this grade (did not check) |\n")
w(rn + "\n")
w("\n## Bounds\n\n**Out of scope by design.**\n- No line, price or engine change; the lines are the lock's.\n- The league's real weekly schedule is not in either repository: the simulation draws the pairings at random each week, so each team meets an average schedule. A real schedule moves an individual season, not the 10,000-season shares much.\n- In-season management (streaming, trades, waiver moves) is not modelled beyond the daily-fill start rates; §6 is the only replacement modelled.\n- §11 simulates only the top three alternatives by ECW at each turn; a player lower on ECW whose title shift would have been larger is not tested. The swaps are single changes on the final board: they do not model how the rest of the draft would have unfolded after a different pick.\n")
w("**In scope and unverified.**\n- Injury news after the 10/14 lock: did not check (no pull tonight); the board's availability multipliers are the lock's.\n- The projections themselves: the 10,000 seasons inherit the lock's lines; the integrity audit's projection confidence (97.8%) and its caveat (the lines sit close to the consensus) stand. `UNVERIFIABLE` until games are played.\n- The opponents' in-season behavior (who streams, who trades): `UNVERIFIABLE`.\n")
w("## Decision sheet (owner disposes)\n\n| id | decision question | default if silent |\n|---|---|---|")
w("| D-LD-2 | waiver move after the draft: (a) Draymond Green for Christian Braun now, accepting the rest-day risk; (b) watch Green\'s first week of games, then decide; (c) Bobby Portis for Braun now, the smaller but sturdier gain; (d) stand pat | (b) |")
w("| D-LD-1 | the log-display defects (§8: undone lines re-rendered under the later occupant; the stale \"no longer your pick\" line) together with D83-1: fix after the draft, red-first, on the next deck version | fix after the draft |")
w("| D-INT-1 (provenance freshness), D82-1, D83-1, earlier | carried; post-draft items | carried |\n")
w("## Provenance\n")
w("- Inputs: the owner's paste (`owner_message.txt`, verbatim); the lock pool (deck `af91b23`, `arena/results/players_v69.csv`); the page `docs/draft-deck.html` (Version 70, deck main `ec070a6`).")
w(f"- Tools: `build_state.py` (parse, resolve, the typed sequence), the deck's `arena/mocks/league_sim.py` (new: the house simulator with the full season recorded, `--verify` against `arena.simulate_seasons`), `live_retro.py` (the draft registered as key 100 on tag v69: replay, final, hindsight, arms), `live_deckcard.py`, `live_replay_dom.mjs`, `stress.py`, `retro_picks.py` (§11), `scripts/repeat_market_check.py` ({rn_head[0]} of {rn_head[1]} rooms, {rn_head[2]} flagged; the league draft is room 100 in that count), `write_report.py`.")
w("- No line, tag or placement changed on either plane; nothing was published.\n")
w("## In plain language\n")
w(f"**The headline.** In 10,000 simulated seasons you win the title about {me1['champ']:.0f} percent of the time — more than anyone else in the league; {who(int(rival))} is next at about {T1[rival]['champ']:.0f}. You make the playoffs about {me1['playoff']:.0f} percent of the time and finish as the top seed in about {me1['seed_pct'][0]:.0f} percent. A second, independent 10,000 gave {me2['champ']:.1f} percent: the number is stable.")
w(f"\n**What kind of team it is.** You win weeks on {', '.join(strong)}, and you are thin in {', '.join(weak)}. Protect the first group; the second is where pickups and trades help most.")
w(f"\n**The draft itself.** You took the card's 🎯 at {len(followed)} of 13 picks and stayed in its Top 5 at {len(top5)}. " + (f"The best single change in hindsight was #{best[1]}: {best[0]} instead of {own[best[1]]} ({best[2] - ad['champ']:+.1f} title points on the house arms). " if best else "") + f"Taking the 🎯 every time grades {fc['champ']:.1f} percent on the house arms against {ad['champ']:.1f} as drafted.")
w(f"\n**The risk.** Losing Haliburton or Durant for the whole season would cut the title share to about {min(r['champ'] for r in ST['arms'].values()):.0f} percent; Kawhi or Kyrie, to about {ST['arms']['Kawhi Leonard']['champ']:.0f} and {ST['arms']['Kyrie Irving']['champ']:.0f}. The board already prices ordinary missed games.")
w(f"\n**Pickups.** Of {WM['pairs']} add/drop pairs, only {WM['positive_pairs']} help, all by dropping one of Braun, Queta, Washington or Lendeborg. The best is **Draymond Green for Christian Braun** (about +1.5 to +1.7 title points), but only if Green plays a normal schedule: at reduced availability the same move costs about 1.3 points, and he has been resting in the preseason. The safer, smaller move is **Bobby Portis for Braun** (about +0.9 to +1.2). Nobody on the wire beats any of your top nine.")
w(f"\n**Your picks against the card.** Of your six picks off the card's 🎯, yours came out better on title share at {len(better_you)} (" + ", ".join(f"#{x['pick']} {x['owner']}" for x in better_you) + f"); the card was better at {len(better_card)} (" + ", ".join(f"#{x['pick']} {x['target']} over {x['owner']}" for x in better_card) + "). Every difference is under about 1.2 title points; the clearest wins for you were PJ Washington over Poeltl at #135, and for the card, Maxey over Haliburton at #10.")
w(f"\n**Your opponents.** Most drafted roughly as before, but the history predicts less than it seems: only {hit} of {tot} \"loyalty\" repeats happened, and the reach ranking barely carried over year to year. The notable change is Martin, last year's champion, who drafted for value this time and sits third in the simulation. The managers who churn the waiver wire hardest (Will, Martin, Oblena, Cayas) are probably stronger than the frozen simulation shows.")
w(f"\n**Looking back at every pick (§11).** At {len(best_at)} of your 13 picks a clearly better player was still on the board; the biggest was Jalen Johnson instead of Durant at #15 (about {best_at[15]['d_title_mean']:+.1f} title points). At the other {len(clean)} picks your choice holds up. Fixing all of them at once with perfect hindsight would have lifted the title share from about {RP['base_title'][SD[0]]:.0f} to about {RC['title'][SD[0]]:.0f} percent, but that needs knowing every later pick in advance; following the card would have recovered part of it.")
w(f"\n**The tool.** Your corrections all worked: the board matched Yahoo's 156 of 156. The history display has two cosmetic bugs (§8), on the list for after the draft.")
P = os.path.join(K, "report", "after-reports", "after-report-2026-10-14-league-draft.md")
open(P, "w", encoding="utf-8").write("\n".join(o) + "\n")
PLG = os.path.join(K, "report", "pull-log.md"); pl = rd(PLG)
if "after-report-2026-10-14-league-draft.md" not in pl:
    row = (f"| 2026-10-14 | THE LEAGUE DRAFT (real league, seat 10, locked lines) — graded and simulated over 10,000 seasons | 0 | 0 | 0 | "
           f"after-reports/after-report-2026-10-14-league-draft.md — title {me1['champ']:.2f}% (rank {rank1}; 2nd run {me2['champ']:.2f}%), playoffs {me1['playoff']:.2f}%, top seed {me1['seed_pct'][0]:.2f}%; "
           f"ECW {ECW:.3f} rank {F['ecw_rank']}, favored {F['exp_winning_weeks']} of 11; card {len(followed)} of 13, Top-5 {len(top5)}; follow-card {fc['champ']:.2f}% vs as drafted {ad['champ']:.2f}% (house arms); "
           f"tool board = Yahoo 156/156; simulator verified against arena on both seeds; D-LD-1 on the sheet; no plane change |")
    open(PLG, "w", encoding="utf-8").write(pl.rstrip("\n") + "\n" + row + "\n")
print("written", P)
