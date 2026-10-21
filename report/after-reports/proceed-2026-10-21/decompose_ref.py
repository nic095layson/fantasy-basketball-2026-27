"""does the current engine with recovery patched back to 0.60 reproduce the old w17r reference exactly?"""
import json, random, sys
D = "/home/user/yahoo-fantasy-basketball"
sys.path.insert(0, D + "/scripts"); sys.path.insert(0, D + "/arena")
import hoops, arena
hoops.DATA_PATH = D + "/arena/results/players_v69.csv"
by = {p["player"]: p for p in hoops.zscores(hoops.load_players())}
st = json.load(open(D + "/arena/data/states/draft_state_100.json"))
ros = {s: [] for s in range(1, 13)}
for pk in st["picks"]: ros[pk["slot"]].append(by[pk["player"]])
orig = arena.weekly_availability
mode = sys.argv[1]
if mode == "rec060":
    arena.weekly_availability = lambda p: 0.60 if (orig(p) == 0.0 and "recovery" in hoops.note_tag(p.get("note"))) else orig(p)
for sd in (2026, 2027):
    ch, po = arena.simulate_seasons(ros, 10000, random.Random(sd))
    old = json.load(open(f"{D}/arena/results/m100_league_sim_10k_s{sd}_w17r.json"))["teams"]
    new = json.load(open(f"{D}/arena/results/m100_league_sim_10k_s{sd}_w17r_av0.json"))["teams"]
    diff_old = [s for s in range(1, 13) if round(ch[s] / 100, 2) != old[str(s)]["champ"]]
    diff_new = [s for s in range(1, 13) if round(ch[s] / 100, 2) != new[str(s)]["champ"]]
    print(mode, sd, "seat10", ch[10] / 100, "seat2", ch[2] / 100, "| seats differing from OLD ref:", diff_old, "| from NEW ref:", diff_new)
