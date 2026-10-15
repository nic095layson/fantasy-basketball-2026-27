#!/usr/bin/env python3
"""Owner 2026-10-15: "Were any of my picks better than the card's?" At each of the owner's six turns off the card's 🎯,
the 🎯 is swapped in for the owner's pick on Yahoo's final board — pairwise, as the house arms do: if another seat took
the 🎯 later, that seat gets the owner's player instead; if nobody took the 🎯, the owner's player goes undrafted. Each
swap is scored two ways: expected weekly category wins against the (swap-adjusted) final rosters, and title share over
10,000 seasons through the verified league simulator on seeds 2026 and 2027 (the baselines' seeds). Writes
card_vs_owner.json."""
import json, math, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); DECK = "/home/user/yahoo-fantasy-basketball"
sys.path.insert(0, DECK + "/scripts"); sys.path.insert(0, DECK + "/arena")
import hoops, arena
hoops.DATA_PATH = f"{DECK}/arena/results/players_v69.csv"
P = hoops.zscores(hoops.load_players()); by = {p["player"]: p for p in P}
st = json.load(open(f"{DECK}/arena/data/states/draft_state_100.json", encoding="utf-8"))
card = json.load(open(f"{DECK}/arena/results/m100_deckcard_v69.json"))
CATS = hoops.CATS
def ecw(picks):
    ros = {s: [] for s in range(1, 13)}
    for pk in picks: ros[pk["slot"]].append(by[pk["player"]])
    my = arena.team_week_model(ros[10]); tot = 0.0; cats = {c: 0.0 for c in CATS}
    for s, r in ros.items():
        if s == 10: continue
        om = arena.team_week_model(r)
        for c in CATS:
            d = (my[0][c] - om[0][c]) / (math.sqrt(my[1][c] + om[1][c]) or 1e-9)
            pr = 0.5 * (1 + math.erf(d / math.sqrt(2))); v = (1 - pr) if c == "TO" else pr
            tot += v; cats[c] += v / 11
    return tot / 11, cats
base_e, base_c = ecw(st["picks"])
base = {sd: json.load(open(f"{DECK}/arena/results/m100_league_sim_10k_s{sd}.json"))["teams"]["10"]["champ"] for sd in (2026, 2027)}
out = dict(base_ecw=round(base_e, 4), base_title=base, turns=[])
for t in sorted(card, key=lambda t: t["pick"]):
    if t["actualCardRank"] == 1: continue
    tg = next(r["n"] for r in t["rows"] if r["target"]); n = t["pick"] - 1
    picks = [dict(pk) for pk in st["picks"]]; mine = picks[n]["player"]
    j = next((i for i, pk in enumerate(picks) if pk["player"] == tg), None)
    picks[n]["player"] = tg
    if j is not None: picks[j]["player"] = mine
    e, c = ecw(picks)
    s2 = dict(st, picks=picks); sp = os.path.join(H, "_cvo_state.json"); json.dump(s2, open(sp, "w"), ensure_ascii=False)
    titles = {}
    for sd in (2026, 2027):
        op = os.path.join(H, "_cvo_out.json")
        subprocess.run([sys.executable, f"{DECK}/arena/mocks/league_sim.py", sp, "v69", "10000", str(sd), op], check=True, capture_output=True)
        titles[sd] = json.load(open(op))["teams"]["10"]["champ"]; os.remove(op)
    os.remove(sp)
    rec = dict(pick=t["pick"], owner=mine, target=tg, card_rank=t["actualCardRank"],
               target_went=(f"#{j + 1} seat {st['picks'][j]['slot']}" if j is not None else "undrafted"),
               d_ecw_if_target=round(e - base_e, 4), d_title_if_target={sd: round(titles[sd] - base[sd], 2) for sd in titles},
               d_cats_if_target={k: round(c[k] - base_c[k], 3) for k in CATS})
    out["turns"].append(rec)
    print(f"#{rec['pick']:>3} you {mine:<20} 🎯 {tg:<18} ({rec['target_went']:>14})  ΔECW if 🎯 {rec['d_ecw_if_target']:+.4f}  Δtitle {rec['d_title_if_target'][2026]:+.2f} / {rec['d_title_if_target'][2027]:+.2f}")
json.dump(out, open(os.path.join(H, "card_vs_owner.json"), "w"), indent=1, ensure_ascii=False)
