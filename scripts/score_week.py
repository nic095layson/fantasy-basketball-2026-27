#!/usr/bin/env python3
"""The scoring loop (owner 2026-10-24, Council order step 2): every morning's per-category P(win) for a finished week,
graded against the week's finals.

Inputs: data/weeks/week_N.json (scoreboard_intake.py: the owner's won / lost / tied categories) and each morning's
report/briefs/week_matchup_<date>.json for the dates of that week (week_matchup.py: cats[].p_win, the chance that
morning of winning the category, and leader_to_date). Output: report/calibration_daily.json, append-only per week,
plus a regenerated report/calibration_daily.md.

Scoring: outcome 1 (won), 0.5 (tied), 0 (lost); Brier = (p - outcome)^2, 0 perfect, 0.25 a coin flip. The weekly
ledger (weekly_preview.py) scores the PRE-WEEK prediction and counts a tie as a loss by its pre-registered rule of
2026-10-15; this record scores the DAILY card and uses 0.5 for a tie (proper for a Brier score) — stated 2026-10-24.
Baseline: the lead to date as a forecast (1 if I led the category that morning, 0 if behind, 0.5 if level); skill =
baseline Brier - card Brier, positive when the card beats the scoreboard. Reliability: five bins of width 0.2 over
every day x category forecast, with the count, mean P and hit rate (ties half) in each.

A week is scored once: a rerun with identical inputs is a no-op; with different inputs it halts and leaves the file.
A morning without a record is listed under days_missing, never filled. Red-first tests: test_score_week.py.

    python3 scripts/score_week.py --week 1 [--weeks-dir DIR] [--briefs-dir DIR] [--out FILE] [--ledger PATH]
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import co_gm as CG  # noqa: E402
import run_ledger  # noqa: E402

KIT = CG.KIT
WEEKS = os.path.join(KIT, "data", "weeks")
BRIEFS = os.path.join(KIT, "report", "briefs")
OUT = os.path.join(KIT, "report", "calibration_daily.json")
CATS = ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]
BINS = [(0.0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0)]


class ScoreError(Exception):
    pass


def outcomes(week):
    o = week["owner"]
    out = {c: 1.0 for c in o.get("won", [])}
    out.update({c: 0.5 for c in o.get("tied", [])})
    out.update({c: 0.0 for c in o.get("lost", [])})
    missing = [c for c in CATS if c not in out]
    if missing:
        raise ScoreError(f"week {week.get('week')}: no result for {missing}")
    return out


def _bin(p):
    for lo, hi in BINS:
        if p < hi or (hi == 1.0 and p <= 1.0):
            return f"{lo:.1f}-{hi:.1f}"
    return None


def _days(window):
    s, e = (datetime.date.fromisoformat(x) for x in window)
    return [(s + datetime.timedelta(days=i)).isoformat() for i in range((e - s).days + 1)]


def score(week, cards, window=None):
    """The scorecard for one week from its finals and the morning cards that exist (any order; keyed by date)."""
    res = outcomes(week)
    cards = sorted(cards, key=lambda c: c["date"])
    window = window or (cards[0]["window"] if cards else None)
    days, by_cat, bins = {}, {c: dict(n=0, brier=0.0, baseline=0.0) for c in CATS}, {f"{lo:.1f}-{hi:.1f}": dict(n=0, p=0.0, hits=0.0) for lo, hi in BINS}
    tot = dict(n=0, brier=0.0, baseline=0.0)
    for card in cards:
        d = {}
        for row in card.get("cats", []):
            c = row.get("cat")
            if c not in res or row.get("p_win") is None:
                continue
            p, y = float(row["p_win"]), res[c]
            lead = row.get("leader_to_date")
            base = 1.0 if lead == "me" else 0.0 if lead == "opp" else 0.5
            d[c] = dict(p=p, outcome=y, brier=(p - y) ** 2, lead=lead, baseline_brier=(base - y) ** 2)
            by_cat[c]["n"] += 1; by_cat[c]["brier"] += d[c]["brier"]; by_cat[c]["baseline"] += d[c]["baseline_brier"]
            tot["n"] += 1; tot["brier"] += d[c]["brier"]; tot["baseline"] += d[c]["baseline_brier"]
            b = bins[_bin(p)]; b["n"] += 1; b["p"] += p; b["hits"] += y
        if d:
            days[card["date"]] = d
    if not tot["n"]:
        raise ScoreError(f"week {week.get('week')}: no morning card carries a P(win)")
    by_day = {dt: dict(n=len(d), brier=sum(x["brier"] for x in d.values()) / len(d),
                       baseline_brier=sum(x["baseline_brier"] for x in d.values()) / len(d)) for dt, d in days.items()}
    nm = lambda x: x.get("name") if isinstance(x, dict) else x          # a week_matchup-style {name, seat} reads as its name
    rec = dict(week=week.get("week"), window=window, team=nm(week["owner"].get("team")), opponent=nm(week["owner"].get("opponent")),
               result=dict(won=sorted(week["owner"].get("won", [])), lost=sorted(week["owner"].get("lost", [])),
                           tied=sorted(week["owner"].get("tied", []))),
               days=days, by_day=by_day,
               by_cat={c: dict(n=v["n"], brier=v["brier"] / v["n"] if v["n"] else None,
                               baseline_brier=v["baseline"] / v["n"] if v["n"] else None, outcome=res[c]) for c, v in by_cat.items()},
               reliability=[dict(bin=k, n=v["n"], mean_p=v["p"] / v["n"] if v["n"] else None, hit_rate=v["hits"] / v["n"] if v["n"] else None)
                            for k, v in bins.items()],
               n_forecasts=tot["n"], brier=tot["brier"] / tot["n"], baseline_brier=tot["baseline"] / tot["n"],
               days_scored=sorted(days), days_missing=[dt for dt in (_days(window) if window else []) if dt not in days],
               method=dict(outcome="won 1, tied 0.5, lost 0", brier="(p - outcome)^2; 0 perfect, 0.25 a coin flip",
                           baseline="the lead to date as a forecast: 1 led, 0 behind, 0.5 level", skill="baseline Brier - card Brier",
                           bins="five bins of width 0.2 over every morning x category forecast",
                           note="the weekly ledger (weekly_preview.py) scores the pre-week prediction and counts a tie as a loss, its 2026-10-15 rule; this record scores the daily card"))
    rec["skill"] = rec["baseline_brier"] - rec["brier"]
    return rec


def _fp(path):
    try:
        return hashlib.sha256(open(path, "rb").read()).hexdigest()[:12]
    except OSError:
        return None


def load_cards(briefs_dir, week, window):
    cards, files = [], {}
    for f in sorted(glob.glob(os.path.join(briefs_dir, "week_matchup_????-??-??.json"))):
        try:
            c = json.load(open(f, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if c.get("week") == week or (window and window[0] <= c.get("date", "") <= window[1]):
            cards.append(c); files[os.path.basename(f)] = _fp(f)
    return cards, files


def render(led):
    L = ["# Daily calibration — the morning card's P(win) against the finals", "",
         "Each morning the Today card states, per category, the chance of winning it; at the week's intake every stated chance is",
         "scored against the final (won 1, tied 0.5, lost 0; Brier = (p − outcome)², 0 perfect, 0.25 a coin flip). Baseline = the",
         "lead to date as a forecast; skill = baseline − card, positive when the card beats the scoreboard. `scripts/score_week.py`;",
         "`report/calibration_daily.json` is the record and is append-only.", "",
         "| week | opponent | result | mornings | forecasts | Brier (card) | Brier (lead to date) | skill |", "|---|---|---|---|---|---|---|---|"]
    for k in sorted(led["weeks"], key=int):
        w = led["weeks"][k]; r = w["result"]
        L.append(f"| {k} | {w.get('opponent') or '?'} | {len(r['won'])}-{len(r['lost'])}-{len(r['tied'])} | {len(w['days_scored'])}"
                 f"{' (+' + str(len(w['days_missing'])) + ' missing)' if w['days_missing'] else ''} | {w['n_forecasts']} | "
                 f"{w['brier']:.3f} | {w['baseline_brier']:.3f} | {w['skill']:+.3f} |")
    allb = [x for w in led["weeks"].values() for x in w["reliability"]]
    if allb:
        agg = {}
        for x in allb:
            a = agg.setdefault(x["bin"], dict(n=0, p=0.0, hits=0.0))
            if x["n"]:
                a["n"] += x["n"]; a["p"] += x["mean_p"] * x["n"]; a["hits"] += x["hit_rate"] * x["n"]
        L += ["", "Reliability, all weeks (a calibrated card has hit rate ≈ mean P in every bin):", "",
              "| stated P | forecasts | mean P | hit rate |", "|---|---|---|---|"]
        for k in [f"{lo:.1f}-{hi:.1f}" for lo, hi in BINS]:
            a = agg.get(k, dict(n=0))
            L.append(f"| {k} | {a['n']} | {(a['p'] / a['n']):.2f} | {(a['hits'] / a['n']):.2f} |" if a["n"] else f"| {k} | 0 | — | — |")
    return "\n".join(L) + "\n"


def run(week, weeks_dir=WEEKS, briefs_dir=BRIEFS, out=OUT):
    wp = os.path.join(weeks_dir, f"week_{week}.json")
    if not os.path.exists(wp):
        raise ScoreError(f"no finals for week {week} ({os.path.relpath(wp, KIT) if wp.startswith(KIT) else wp}); run scoreboard_intake first")
    wk = json.load(open(wp, encoding="utf-8"))
    window = wk.get("window")
    cards, files = load_cards(briefs_dir, week, window)
    if cards and not window:
        window = cards[0].get("window")
    rec = score(wk, cards, window)
    rec["inputs"] = dict(week_file=_fp(wp), cards=files)
    rec["scored_at"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    led = json.load(open(out, encoding="utf-8")) if os.path.exists(out) else {"weeks": {}}
    key = str(week)
    if key in led["weeks"]:
        if led["weeks"][key]["inputs"] == rec["inputs"]:
            return dict(status="unchanged", week=led["weeks"][key])
        raise ScoreError(f"week {key} is already scored ({led['weeks'][key]['scored_at']}) on different inputs; the record is append-only")
    led["weeks"][key] = rec
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(led, f, indent=1, ensure_ascii=False); f.write("\n")
    with open(out[:-5] + ".md" if out.endswith(".json") else out + ".md", "w", encoding="utf-8") as f:
        f.write(render(led))
    return dict(status="scored", week=rec)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--week", type=int, required=True)
    ap.add_argument("--weeks-dir", default=WEEKS); ap.add_argument("--briefs-dir", default=BRIEFS); ap.add_argument("--out", default=OUT)
    ap.add_argument("--ledger", default=run_ledger.LEDGER, help="run-ledger path; '' records no row")
    a = ap.parse_args()
    led = lambda v, d: run_ledger.standalone_record("score_week", v, d, ledger=a.ledger) if a.ledger else None
    try:
        r = run(a.week, a.weeks_dir, a.briefs_dir, a.out)
    except (ScoreError, OSError, ValueError, KeyError) as e:
        print(f"WEEK SCORE: FAIL — {e}"); led("FAIL", str(e)[:200]); return 1
    w = r["week"]
    msg = (f"week {a.week} {r['status']}: {len(w['days_scored'])} mornings, {w['n_forecasts']} forecasts; Brier {w['brier']:.3f} "
           f"vs lead-to-date {w['baseline_brier']:.3f} (skill {w['skill']:+.3f})"
           f"{'; missing ' + ', '.join(w['days_missing']) if w['days_missing'] else ''}")
    print(f"WEEK SCORE: PASS — {msg}"); led("PASS", msg[:200])
    return 0


if __name__ == "__main__":
    sys.exit(main())
