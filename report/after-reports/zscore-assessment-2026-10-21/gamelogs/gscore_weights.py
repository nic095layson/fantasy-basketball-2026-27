#!/usr/bin/env python3
"""D-ZS-1 step 2 + D-ZS-2 input (owner 2026-10-21): week-to-week variance from the 2025-26 game logs, turned into the
G-score weights of Rosenof, arXiv 2307.02188v5 (data/source/papers/, p. 4: G-scores are Z-scores whose
"denominators are modified to add period-to-period variance"; Table 5), plus the per-game CV fit for arena.CV.

Method, stated to the owner before the run (2026-10-21):
  Q        the kit season board's top 180 of 10/21 (rank_engine.POOL_SIZE) that played 2025-26; sensitivity at 156
  weeks    Monday-Sunday from 2025-10-27; the two All-Star-break weeks (2026-02-09 to 02-22) excluded; only weeks
           wholly inside the logs' date range; a player's week counts if he played; 10+ counted weeks to enter
  counting per category: mu(q) = mean weekly total, tau(q) = SD of weekly totals (population, as Table 5a);
           sigma = SD across Q of mu(q); tau_M = RMS across Q of tau(q)
  percent  Table 5b exactly: mu_A(q) mean weekly attempts, mu_A their mean over Q, mu_R(q) the player's composite
           rate, mu_R = sum a_q mu_R(q) / sum a_q (a_q = mu_A(q)), sigma_R = SD across Q of mu_R(q),
           tau_R(q) = SD across W of theta_A(q,w)/mu_A * (theta_R(q,w) - mu_R), tau_R = RMS across Q
  weight   w = sigma / sqrt(sigma^2 + kappa * tau^2) on 2025-26 alone (the paper's Table 8 "G-score as fraction of
           Z-score"); kappa = 2N/(2N-1), N = the league's non-IL roster spots (data/league_settings.json) = 13 -> 1.04
  pin      --pin PATH writes what the season board needs for Table 5 on its own projections: kappa, the weekly
           tau_M per counting category, tau_R per percentage, and the mean games per counted player-week (g) that
           puts a weekly tau on the board's per-game scale (tau / g)
  CV fit   per counting category: sqrt(sum n_i var_i / sum n_i mean_i^2) over Q players with 20+ games (per-game)
  check    each player's per-game means from the logs vs the pinned ESPN 2025-26 per-game file (deck
           arena/results/actuals_2026-10-09/espn_pergame_2025-26.csv), 0.15 per stat per game
Writes gscore_weights_2025-26.json beside itself (and, with --pin, the season board's input file). Analysis only."""
import argparse, csv, datetime as dt, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
DECK = os.path.join(KIT, "..", "yahoo-fantasy-basketball")
sys.path.insert(0, os.path.join(DECK, "scripts")); sys.path.insert(0, os.path.join(DECK, "arena"))
from verify_rosters import norm  # noqa: E402
import arena  # noqa: E402

START = dt.date(2025, 10, 27)
ASB = (dt.date(2026, 2, 9), dt.date(2026, 2, 22))
N_ROSTER = sum(1 for p in json.load(open(os.path.join(KIT, "data", "league_settings.json"), encoding="utf-8"))["roster_positions"]["value"] if p != "IL")
KAPPA = 2 * N_ROSTER / (2 * N_ROSTER - 1)
COUNT = {"PTS": "pts", "REB": "trb", "AST": "ast", "3PTM": "fg3", "ST": "stl", "BLK": "blk", "TO": "tov"}
PCT = {"FG%": ("fg", "fga"), "FT%": ("ft", "fta")}
KIT_KEY = {"PTS": "pts", "REB": "reb", "AST": "ast", "3PTM": "tpm", "ST": "stl", "BLK": "blk", "TO": "tov", "FG%": "fgp", "FT%": "ftp"}
num = lambda v: float(v) if v not in ("", None) else 0.0


def sd(xs):
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


def load():
    q = json.load(open(os.path.join(HERE, "q_ids.json"), encoding="utf-8"))
    games = {}
    for r in csv.DictReader(open(os.path.join(HERE, "gamelogs_2025-26.csv"), encoding="utf-8")):
        games.setdefault(r["player"], []).append(r)
    return q, games


def weeks_of(games):
    last = max(dt.date.fromisoformat(r["date"]) for gs in games.values() for r in gs)
    out = {}
    for name, gs in games.items():
        for r in gs:
            d = dt.date.fromisoformat(r["date"])
            if d < START or ASB[0] <= d <= ASB[1]:
                continue
            k = (d - START).days // 7
            if START + dt.timedelta(days=7 * k + 6) > last:
                continue  # a week the logs do not wholly cover
            out.setdefault(name, {}).setdefault(k, []).append(r)
    return out


def weights(q_names, wk):
    players = [n for n in q_names if n in wk and len(wk[n]) >= 10]
    res = {"players": len(players)}
    for cat, col in COUNT.items():
        mus, taus = [], []
        for n in players:
            tot = [sum(num(r[col]) for r in rs) for rs in wk[n].values()]
            mus.append(sum(tot) / len(tot)); taus.append(sd(tot))
        sigma, tau = sd(mus), math.sqrt(sum(t * t for t in taus) / len(taus))
        res[cat] = dict(sigma=round(sigma, 4), tau=round(tau, 4), w=round(sigma / math.sqrt(sigma ** 2 + KAPPA * tau ** 2), 4))
    for cat, (mk, at) in PCT.items():
        att = {n: [sum(num(r[at]) for r in rs) for rs in wk[n].values()] for n in players}
        mk_ = {n: [sum(num(r[mk]) for r in rs) for rs in wk[n].values()] for n in players}
        mu_aq = {n: sum(att[n]) / len(att[n]) for n in players}
        mu_a = sum(mu_aq.values()) / len(players)
        mu_rq = {n: sum(mk_[n]) / sum(att[n]) for n in players if sum(att[n]) > 0}
        mu_r = sum(mu_aq[n] * mu_rq[n] for n in mu_rq) / sum(mu_aq[n] for n in mu_rq)
        sigma = sd(list(mu_rq.values()))
        # theta_A/mu_A * (theta_R - mu_R) = (makes - mu_R * attempts) / mu_A; a week with no attempts contributes 0
        taus = [sd([(m - mu_r * x) / mu_a for m, x in zip(mk_[n], att[n])]) for n in players]
        tau = math.sqrt(sum(t * t for t in taus) / len(taus))
        res[cat] = dict(mu_A=round(mu_a, 4), mu_R=round(mu_r, 4), sigma=round(sigma, 5), tau=round(tau, 5),
                        w=round(sigma / math.sqrt(sigma ** 2 + KAPPA * tau ** 2), 4), rate_players=len(mu_rq))
    gw = [len(rs) for n in players for rs in wk[n].values()]
    res["games_per_week"] = dict(mean=round(sum(gw) / len(gw), 4), sd=round(sd(gw), 4), player_weeks=len(gw))
    return res


def cv_fit(q_names, games):
    out = {}
    for cat, col in COUNT.items():
        a = b = 0.0
        for n in q_names:
            gs = games.get(n, [])
            if len(gs) < 20:
                continue
            xs = [num(r[col]) for r in gs]
            m = sum(xs) / len(xs)
            a += len(xs) * sd(xs) ** 2; b += len(xs) * m * m
        out[cat] = dict(fitted=round(math.sqrt(a / b), 3), hand_set=arena.CV[cat], ratio=round(math.sqrt(a / b) / arena.CV[cat], 2))
    return out


def espn_check(games):
    espn = {norm(r["player"]): r for r in csv.DictReader(open(os.path.join(DECK, "arena", "results", "actuals_2026-10-09", "espn_pergame_2025-26.csv"), encoding="utf-8"))}
    pairs = dict(pts="pts", trb="reb", ast="ast", stl="stl", blk="blk", tov="tov", fg3="tpm", fga="fga", fta="fta")
    joined, bad = 0, []
    for n, gs in games.items():
        e = espn.get(norm(n))
        if not e:
            continue
        joined += 1
        off = {}
        if int(float(e["gp"])) != len(gs):
            off["gp"] = (len(gs), e["gp"])
        for bc, ec in pairs.items():
            mine = sum(num(r[bc]) for r in gs) / len(gs)
            if abs(mine - float(e[ec])) > 0.15:
                off[bc] = (round(mine, 2), round(float(e[ec]), 2))
        if off:
            bad.append(dict(player=n, off=off))
    return dict(joined=joined, agree=joined - len(bad), disagree=bad)


def pin(rec, path):
    """What scripts/season_board.py reads for the G column (Table 5 on the board's own projections)."""
    w = rec["q180"]
    out = dict(paper=rec["paper"], source=rec["source"], written_by=os.path.relpath(os.path.abspath(__file__), KIT),
               q="kit season board top 180 of 2026-10-21 with 10+ counted 2025-26 weeks", players=w["players"],
               weeks=rec["weeks_counted"], n_roster=N_ROSTER, kappa=round(KAPPA, 6), games_per_week=w["games_per_week"]["mean"],
               tau={KIT_KEY[c]: w[c]["tau"] for c in COUNT}, tau_r={KIT_KEY[c]: w[c]["tau"] for c in PCT})
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1); f.write("\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pin", help="also write the season board's G-column input file here")
    a = ap.parse_args()
    q, games = load()
    wk = weeks_of(games)
    names180 = [n for n in q["q_names"] if n in games]
    names156 = [n for n in q["q_names"][:156] if n in games]
    nweeks = sorted({k for v in wk.values() for k in v})
    rec = dict(source="Basketball-Reference 2025-26 regular-season game logs (pull_manifest.json)", paper="arXiv 2307.02188v5 (data/source/papers/)",
               kappa=round(KAPPA, 4), weeks_counted=len(nweeks),
               week_starts=[str(START + dt.timedelta(days=7 * k)) for k in nweeks],
               q180=weights(names180, wk), q156=weights(names156, wk), cv_fit=cv_fit(names180, games), espn_check=espn_check(games))
    json.dump(rec, open(os.path.join(HERE, "gscore_weights_2025-26.json"), "w"), indent=1, ensure_ascii=False)
    w = rec["q180"]
    print(f"weeks {len(nweeks)}, Q180 players {w['players']}, Q156 players {rec['q156']['players']}, kappa {KAPPA:.3f}")
    print("weights (Q180): " + ", ".join(f"{c} {w[c]['w']:.2f}" for c in list(COUNT) + list(PCT)))
    print("weights (Q156): " + ", ".join(f"{c} {rec['q156'][c]['w']:.2f}" for c in list(COUNT) + list(PCT)))
    print("CV fit: " + ", ".join(f"{c} {v['fitted']} (hand {v['hand_set']}, x{v['ratio']})" for c, v in rec["cv_fit"].items()))
    print(f"games per counted player-week (Q180): {w['games_per_week']['mean']}")
    e = rec["espn_check"]; print(f"ESPN check: {e['agree']} of {e['joined']} agree; disagree {len(e['disagree'])}")
    if a.pin:
        pin(rec, a.pin); print(f"pinned: {a.pin}")


if __name__ == "__main__":
    main()
