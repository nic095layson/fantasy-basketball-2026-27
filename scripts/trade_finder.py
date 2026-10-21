#!/usr/bin/env python3
"""Trade Finder (owner 2026-10-20: "1, 2, 5 build", item 1). Sweeps every 1-for-1 trade between
the owner's active roster and each rival's active roster on the live league state, re-modeling
BOTH teams, and surfaces only trades where the owner's expected weekly category wins rise AND
the rival's do not fall (the acceptability proxy, plan-gate A2: our engine standing in for their
judgment, not a model of what they would actually accept). The top trades by the owner's gain
are then checked in the season simulator (both seeds, plan-gate A3). IL players sit out of both
sides (D-IS-8). 2-for-2 is deferred (plan-gate A1).

Record and propose only: nothing here touches a roster, a line or a tag.

    SEASON_POOL=data/season/pool_season.csv python3 scripts/trade_finder.py --date 2026-10-20 \
        [--seasons 10000] [--top 5] [--no-sim]
Writes data/news/trades_<date>.json; the deck's Trade pane and the brief read it.
"""
import argparse
import datetime
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import co_gm as CG  # noqa: E402

OUTDIR = os.path.join(KIT, "data", "news")
SEEDS = (2026, 2027)


def _models(ros):
    return {s: CG.arena.team_week_model(r) for s, r in ros.items()}


def _ecw(models, seat):
    return CG.pwins(models[seat], [m for s, m in models.items() if s != seat])


def apply_trade(ros, t):
    """The two post-trade rosters for a trade record {seat, i_send, i_get}."""
    me, them = ros[CG.OWNER_SEAT], ros[t["seat"]]
    d = next(p for p in me if p["player"] == t["i_send"])
    a = next(p for p in them if p["player"] == t["i_get"])
    return [x for x in me if x is not d] + [a], [x for x in them if x is not a] + [d]


def deltas(ros, seat, me2, them2):
    """Post-trade ECW minus pre-trade ECW for the owner and the rival, the whole league re-modeled."""
    base = _models(ros)
    new = dict(base)
    new[CG.OWNER_SEAT] = CG.arena.team_week_model(me2)
    new[seat] = CG.arena.team_week_model(them2)
    return (_ecw(new, CG.OWNER_SEAT) - _ecw(base, CG.OWNER_SEAT),
            _ecw(new, seat) - _ecw(base, seat))


def sweep(ros, return_count=False):
    """All 1-for-1 trades; keeps d_ecw_me > 0 and d_ecw_them >= 0, sorted by my gain."""
    base = _models(ros)
    base_ecw = {s: _ecw(base, s) for s in ros}
    mine = ros[CG.OWNER_SEAT]
    out, n = [], 0
    for seat, theirs in ros.items():
        if seat == CG.OWNER_SEAT:
            continue
        for d in mine:
            m_wo_d = [x for x in mine if x is not d]
            for a in theirs:
                n += 1
                new = dict(base)
                new[CG.OWNER_SEAT] = CG.arena.team_week_model(m_wo_d + [a])
                new[seat] = CG.arena.team_week_model([x for x in theirs if x is not a] + [d])
                d_me = _ecw(new, CG.OWNER_SEAT) - base_ecw[CG.OWNER_SEAT]
                if d_me <= 0:
                    continue
                d_them = _ecw(new, seat) - base_ecw[seat]
                if d_them < 0:
                    continue
                out.append({"seat": seat, "i_send": d["player"], "i_get": a["player"],
                            "d_ecw_me": round(d_me, 4), "d_ecw_them": round(d_them, 4)})
    out.sort(key=lambda t: -t["d_ecw_me"])
    return (out, n) if return_count else out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--seasons", type=int, default=10000)
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--no-sim", action="store_true")
    a = ap.parse_args()
    state = json.load(open(CG.STATE, encoding="utf-8"))
    P, by = CG.load_pool()
    ros = CG.rosters(state, by)
    team_of = {t["seat"]: t["name"] for t in state["teams"]}
    trades, n = sweep(ros, return_count=True)
    # the simulator check on the top trades, against the brief's base title (same state, same seeds)
    brief_path = os.path.join(KIT, "report", "briefs", f"brief_{a.date}.json")
    base_title = None
    if os.path.exists(brief_path):
        b = json.load(open(brief_path, encoding="utf-8"))["title"]
        base_title = sum(b[str(s)] for s in SEEDS) / len(SEEDS)
    if not a.no_sim and trades and base_title is not None:
        with tempfile.TemporaryDirectory() as work:
            for t in trades[:a.top]:
                me2, them2 = apply_trade(ros, t)
                r2 = dict(ros); r2[CG.OWNER_SEAT] = me2; r2[t["seat"]] = them2
                by_seed = {s: CG.run_league_sim(r2, s, a.seasons, work, tag="t")["teams"][str(CG.OWNER_SEAT)]["champ"]
                           for s in SEEDS}
                t["title_by_seed"] = {str(s): by_seed[s] for s in SEEDS}
                t["title"] = round(sum(by_seed.values()) / len(by_seed), 2)
                t["d_title"] = round(t["title"] - base_title, 2)
    rec = {"date": a.date, "league_state_as_of": state["as_of"], "pairs_swept": n,
           "proposable": len(trades), "base_title": base_title, "seasons": a.seasons,
           "method": "1-for-1, both teams re-modeled; keep d_ecw_me>0 and d_ecw_them>=0 (acceptability proxy)",
           "trades": [dict(t, team=team_of.get(t["seat"])) for t in trades[:max(a.top, 10)]]}
    os.makedirs(OUTDIR, exist_ok=True)
    out = os.path.join(OUTDIR, f"trades_{a.date}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False)
        f.write("\n")
    best = rec["trades"][0] if rec["trades"] else None
    tail = (f"best: send {best['i_send']} to {best['team']} for {best['i_get']} "
            f"({best['d_ecw_me']:+.3f} cats/wk me, {best['d_ecw_them']:+.3f} them"
            + (f", title {best['title']:.1f}% ({best['d_title']:+.1f})" if "title" in best else "") + ")"
            ) if best else "none clears the bar"
    print(f"TRADE FINDER: PASS — {n} pairs swept, {len(trades)} proposable; {tail}; wrote {os.path.relpath(out, KIT)}")


if __name__ == "__main__":
    main()
