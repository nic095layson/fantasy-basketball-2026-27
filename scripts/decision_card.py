#!/usr/bin/env python3
"""The decision card (owner 2026-11-10, pick "Decision card + watchdog"; council 4-1): the brief's top pickup pairs
looked at three more ways before the owner acts. Display only: the brief's figures, its ranking and the headline
title share are never changed, and nothing here feeds a graded record.

1. Two worlds. The brief scores a pair with every IL player absent for the season (D-IS-8, "never return"). The card
   scores the same pairs with every team's IL players back on ESPN's dates (il_return.py's on-time scenario and its
   room rule), and says when the order of the pairs differs between the two. On 2026-11-10 it did: Collins for Dunn
   led the never-return world (+3.44 against +1.57) and trailed the return world (+1.52 against +2.52).
2. The band. The top pair is re-scored under each declared variant of weekly_availability (the FRAGILE constant), in
   the never-return world, and the card says in how many it keeps its sign.
3. This week beside the season. Each pair's effect on this week's matchup, read from the week card's pair_checks.

    SEASON_POOL=data/season/pool_season.csv python3 scripts/decision_card.py --date 2026-11-10 [--seasons 10000]
Prints 'DECISION CARD: PASS — ...' (a hold day is a PASS with no pairs) or 'DECISION CARD: HALT — <why>'. Exit 0 / 1.
"""
import argparse
import json
import os
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import co_gm as CG  # noqa: E402
import il_return as IR  # noqa: E402

KIT = CG.KIT
SEEDS = IR.SEEDS
OUTDIR = os.path.join(KIT, "report", "briefs")
REGISTRY = os.path.join(HERE, "redteam", "constants_registry.json")
BAND_CONSTANT = "weekly_availability"
LABEL = ("Display only: the brief's ranking and the headline title share are unchanged. The return world rests on "
         "ESPN's dates and the room rule (the lowest-value active player leaves), which is itself FRAGILE.")


def band_variants(registry_path=REGISTRY, name=BAND_CONSTANT):
    """[(label, patch)] for the declared band of one constant, as the sweep reads the registry."""
    with open(registry_path, encoding="utf-8") as f:
        reg = json.load(f)
    return [(b["label"], {k: v for k, v in b.items() if k != "label"})
            for e in reg["constants"] if e.get("status") == "declared_band" and e["name"] == name for b in e.get("band") or []]


def _swap(ros, add, drop, by):
    r = {s: list(x) for s, x in ros.items()}
    r[CG.OWNER_SEAT] = [p for p in r[CG.OWNER_SEAT] if p["player"] != drop] + [by[add]]
    return r


def _mean(sims):
    return sum(s["teams"][str(CG.OWNER_SEAT)]["champ"] for s in sims) / len(sims)


def build(brief, ilr, week, state, by, variants, seasons, sim, work, value=None, seeds=SEEDS, workers=1):
    """The card for one day. sim: co_gm.run_league_sim (or a stand-in with its signature). Each missing input leaves
    its own part None and adds one note; nothing is guessed."""
    top = [dict(add=x["add"], drop=x["drop"], title=x.get("title"), d_title=x.get("d_title"), d_ecw=x.get("d_ecw"))
           for x in (brief.get("waiver_top") or [])]
    notes = []
    bt = brief.get("title") or {}
    base_never = sum(bt.values()) / len(bt) if bt else None
    card = dict(date=brief.get("date"), seasons=seasons, seeds=list(seeds), base=dict(never=base_never, on_time=None),
                pairs=[], order=None, rank_flip=None, robust=None, notes=notes, label=LABEL)
    if not top:
        notes.append("no positive pair in the brief today: nothing to check")
        return card

    ros_head = CG.rosters(state, by)
    jobs = {}   # key -> (roster, windows, patch)
    il = (ilr or {}).get("il_players")
    if il and ilr.get("weeks"):
        weeks = int(ilr["weeks"])
        ros_all = CG.rosters(state, by, include_il=True)
        kw = {"value": value} if value else {}
        jobs[("on", None)] = (ros_all, IR.windows_for(il, 0, ros_all, weeks, room=True, **kw), None)
        for i, x in enumerate(top):
            r = _swap(ros_all, x["add"], x["drop"], by)
            jobs[("on", i)] = (r, IR.windows_for(il, 0, r, weeks, room=True, **kw), None)
    else:
        notes.append("no il_return record for the day: the return world is not scored")
    for label, patch in variants or []:
        jobs[("band", label, "base")] = (ros_head, None, patch)
        jobs[("band", label, "pair")] = (_swap(ros_head, top[0]["add"], top[0]["drop"], by), None, patch)

    def run(item):
        n, (key, (ros, win, patch)) = item
        return key, [sim(ros, s, seasons, work, tag=f"dc{n}", windows=win, patch=patch) for s in seeds]
    items = list(enumerate(jobs.items()))
    if workers > 1 and len(items) > 1:
        with ThreadPoolExecutor(workers) as ex:
            res = dict(ex.map(run, items))
    else:
        res = dict(run(it) for it in items)

    base_on = _mean(res[("on", None)]) if ("on", None) in res else None
    card["base"]["on_time"] = base_on
    checks = {(c.get("add"), c.get("drop")): c for c in ((week or {}).get("pair_checks") or [])}
    if not (week or {}).get("pair_checks"):
        notes.append("no pair_checks on the week card: this week's effect is not shown")
    for i, x in enumerate(top):
        wk = checks.get((x["add"], x["drop"]))
        if wk and wk.get("skipped"):
            notes.append(f"{x['add']} for {x['drop']}: this week is not shown ({wk['skipped']})")
        card["pairs"].append(dict(
            add=x["add"], drop=x["drop"], never=dict(title=x["title"], d_title=x["d_title"]),
            on_time=dict(title=_mean(res[("on", i)]), d_title=_mean(res[("on", i)]) - base_on) if base_on is not None else None,
            week=({k: wk[k] for k in ("d_exp", "p_5plus", "d_p_5plus")} if wk and wk.get("d_exp") is not None else None)))
    if base_on is not None:
        key = lambda world: [[p["add"], p["drop"]] for p in sorted(card["pairs"], key=lambda p: -p[world]["d_title"])]
        card["order"] = dict(never=key("never"), on_time=key("on_time"))
        card["rank_flip"] = card["order"]["never"] != card["order"]["on_time"]
    if variants:
        head = top[0]["d_title"] or 0.0
        rows = [dict(label=label, d_title=_mean(res[("band", label, "pair")]) - _mean(res[("band", label, "base")]))
                for label, _ in variants]
        held = sum(1 for r in rows if (r["d_title"] > 0) == (head > 0))
        card["robust"] = dict(add=top[0]["add"], drop=top[0]["drop"], constant=BAND_CONSTANT, variants=rows, held=held,
                              holds=held == len(rows), low=min(r["d_title"] for r in rows), high=max(r["d_title"] for r in rows))
    return card


def render(card):
    L = [f"## Decision card — {card['date']}", ""]
    if not card["pairs"]:
        return L + ["No pair to check today. " + " ".join(card["notes"]), "", card["label"]]
    on = card["base"]["on_time"] is not None
    L += ["| add | drop | season, IL players never return | season, IL players return on time | this week (5+ of 9) |", "|---|---|---|---|---|"]
    for p in card["pairs"]:
        wk = p["week"]
        L.append(f"| {p['add']} | {p['drop']} | {p['never']['d_title']:+.1f} | "
                 + (f"{p['on_time']['d_title']:+.1f}" if p["on_time"] else "not scored") + " | "
                 + (f"{100 * wk['d_p_5plus']:+.1f} points ({wk['d_exp']:+.2f} categories)" if wk else "not shown") + " |")
    L.append("")
    if on:
        L.append(f"Title share with no move: {card['base']['never']:.1f}% (never return), {card['base']['on_time']:.1f}% (return on time).")
        L.append("**The order changes between the two worlds.** Check the return-on-time column before acting."
                 if card["rank_flip"] else "The order is the same in both worlds.")
    r = card["robust"]
    if r:
        L.append(f"Top pair ({r['add']} for {r['drop']}) under the {r['constant']} band: holds in {r['held']} of {len(r['variants'])} "
                 f"settings ({r['low']:+.1f} to {r['high']:+.1f}).")
    L += [n[0].upper() + n[1:] + "." for n in card["notes"]]
    return L + ["", card["label"]]


def pass_line(card, out):
    n = len(card["pairs"])
    if not n:
        return f"DECISION CARD: PASS — {card['date']}: no pair today; wrote {out}"
    flip = ("order changes between the worlds" if card["rank_flip"] else "same order in both worlds") if card["rank_flip"] is not None else "return world not scored"
    r = card["robust"]
    rob = f"top pair holds in {r['held']} of {len(r['variants'])}" if r else "band not run"
    return f"DECISION CARD: PASS — {card['date']}: {n} pair(s); {flip}; {rob}; wrote {out}"


def _load(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", required=True)
    ap.add_argument("--seasons", type=int, help="default: the brief's")
    ap.add_argument("--state", default=CG.STATE)
    ap.add_argument("--out-dir", default=OUTDIR)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    brief = _load(os.path.join(a.out_dir, f"brief_{a.date}.json"))
    if brief is None:
        print(f"DECISION CARD: HALT — no brief for {a.date}"); return 1
    state = _load(a.state)
    ilr = _load(os.path.join(KIT, "report", "il_return", f"il_return_{a.date}.json"))
    week = _load(os.path.join(a.out_dir, f"week_matchup_{a.date}.json"))
    _, by = CG.load_pool()
    missing = [x[k] for x in brief.get("waiver_top") or [] for k in ("add",) if x[k] not in by]
    if missing:
        print(f"DECISION CARD: HALT — no line in the pool for {', '.join(missing)}"); return 1
    seasons = a.seasons or int(brief.get("seasons") or 10000)
    card = build(brief, ilr, week, state, by, band_variants(), seasons, CG.run_league_sim, tempfile.mkdtemp(), workers=a.workers)
    card["inputs"] = dict(brief=f"brief_{a.date}.json", il_return=bool(ilr), week_card=bool(week), pool=os.environ.get("SEASON_POOL"),
                          state_as_of=state.get("as_of"))
    out = os.path.join(a.out_dir, f"decision_card_{a.date}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(card, f, indent=1, ensure_ascii=False); f.write("\n")
    with open(os.path.join(a.out_dir, f"decision_card_{a.date}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(render(card)) + "\n")
    print(pass_line(card, os.path.relpath(out, KIT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
