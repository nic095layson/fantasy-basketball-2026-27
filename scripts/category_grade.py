#!/usr/bin/env python3
"""Category grades (owner 2026-11-10, pick "P5 + P7"): every pre-week category forecast the kit recorded for every
matchup, graded against the week's final lines, by category. The owner's own matchup gives nine graded forecasts a
week; the six league matchups give fifty-four, so a category the model reads badly shows weeks sooner.

Inputs, all written before or at the week's end and never rewritten:
  report/calibration_league.json        the flat-schedule forecast of every matchup (weekly_preview --league)
  report/calibration_league_real.json   the same on each NBA team's real games (the D-RG-1 candidate)
  data/weeks/week_N.json                the week's final lines (scoreboard_intake.py)
For a pair (a, b) and a category, p = the recorded chance that seat a wins it. Outcome: 1 a won, 0 b won, 0.5 a tie
(turnovers: fewer wins). Brier = (p - outcome)^2; 0.25 is a coin flip's score. A "call" is a forecast that favours a
side (p != 0.5) in a category that was not tied; a hit is a call the favoured side won; confidence is the mean stated
chance of the favoured side over the calls (hit rate below confidence = too sure).

The record report/category_grades.json is rebuilt from those inputs on every run (derived, never hand-edited).
Proposes nothing and changes nothing: no line, tag, roster or constant reads it.

    python3 scripts/category_grade.py
Prints 'CATEGORY GRADE: PASS — <summary>'.
"""
import argparse
import glob
import json
import os
import re
import sys

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATS = ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]
WEEKS = os.path.join(KIT, "data", "weeks")
SOURCES = {"flat": os.path.join(KIT, "report", "calibration_league.json"),
           "real_games": os.path.join(KIT, "report", "calibration_league_real.json")}
OUT = os.path.join(KIT, "report", "category_grades.json")
NAMES = {"flat": "flat", "real_games": "real games"}


def outcome(cat, a, b):
    if a == b:
        return 0.5
    return 1.0 if ((a < b) if cat == "TO" else (a > b)) else 0.0


def _blank():
    return dict(n=0, sq=0.0, calls=0, hits=0, conf=0.0)


def _close(x):
    return dict(n=x["n"], brier=(x["sq"] / x["n"]) if x["n"] else None, calls=x["calls"], hits=x["hits"],
                hit_rate=(x["hits"] / x["calls"]) if x["calls"] else None,
                confidence=(x["conf"] / x["calls"]) if x["calls"] else None)


def finals(weeks_dir):
    """{week: {seat: line}} for every week_N.json on disk."""
    out = {}
    for p in glob.glob(os.path.join(weeks_dir, "week_*.json")):
        m = re.search(r"week_(\d+)\.json$", p)
        if not m:
            continue
        with open(p, encoding="utf-8") as f:
            wk = json.load(f)
        out[int(m.group(1))] = {int(t["seat"]): t["line"] for t in wk["teams"].values()}
    return out


def grade_one(path, lines):
    by, total, weeks, notes = {c: _blank() for c in CATS}, _blank(), [], []
    if not os.path.exists(path):
        return dict(weeks=[], by_cat={c: _close(by[c]) for c in CATS}, all=_close(total),
                    note=f"no forecast record ({os.path.relpath(path, KIT) if path.startswith(KIT) else os.path.basename(path)})")
    with open(path, encoding="utf-8") as f:
        rec = json.load(f)
    for w in sorted(rec.get("weeks") or {}, key=int):
        wk = int(w)
        if wk not in lines:
            continue                                    # forecasts recorded, the week not final yet
        used = False
        for pr in rec["weeks"][w].get("pairs") or []:
            a, b = int(pr["a"]), int(pr["b"])
            miss = [s for s in (a, b) if s not in lines[wk]]
            if miss or not pr.get("cat_p"):
                notes.append(f"week {wk}: seat {miss[0]} has no final line" if miss else f"week {wk}: pair {a}-{b} has no category forecast")
                continue
            used = True
            for c in CATS:
                p, o = float(pr["cat_p"][c]), outcome(c, lines[wk][a][c], lines[wk][b][c])
                for x in (by[c], total):
                    x["n"] += 1; x["sq"] += (p - o) ** 2
                    if p != 0.5 and o != 0.5:
                        x["calls"] += 1; x["hits"] += int((p > 0.5) == (o == 1.0)); x["conf"] += max(p, 1 - p)
        if used:
            weeks.append(wk)
    return dict(weeks=weeks, by_cat={c: _close(by[c]) for c in CATS}, all=_close(total), note="; ".join(notes) or None)


def grade(weeks_dir=WEEKS, sources=None):
    lines = finals(weeks_dir)
    return dict(weeks_final=sorted(lines), methods={k: grade_one(p, lines) for k, p in (sources or SOURCES).items()},
                method="p = recorded pre-week chance that seat a wins the category; outcome 1 / 0 / 0.5 (tie), TO low wins; "
                       "Brier (p - outcome)^2, 0.25 = coin flip; calls exclude 50% forecasts and tied categories")


def _f(x, nd=3):
    return "–" if x is None else f"{x:.{nd}f}"


def render(rec):
    L = ["# Category grades — every matchup's pre-week category forecast against the finals", "",
         "Each recorded chance that a team wins a category, scored on the week's final line (`scripts/category_grade.py`; "
         "rebuilt from the forecast records and `data/weeks` on every run). Brier: 0 is perfect, 0.25 is a coin flip. "
         "Favourite right: of the forecasts that favoured a side in an untied category, how many that side won, beside the "
         "mean chance the kit gave it.", ""]
    ms = [k for k in rec["methods"]]
    L.append("| category | " + " | ".join(f"{NAMES.get(k, k)}: n | Brier | favourite right | stated" for k in ms) + " |")
    L.append("|---|" + "---|---|---|---|" * len(ms))
    for c in CATS + ["all"]:
        row = []
        for k in ms:
            x = rec["methods"][k]["all"] if c == "all" else rec["methods"][k]["by_cat"][c]
            row.append(f"{x['n']} | {_f(x['brier'])} | " + (f"{x['hits']} of {x['calls']}" if x["calls"] else "–") + f" | {_f(x['confidence'], 2)}")
        L.append(f"| {'**all**' if c == 'all' else c} | " + " | ".join(row) + " |")
    L.append("")
    for k in ms:
        m = rec["methods"][k]
        L.append(f"{NAMES.get(k, k)}: weeks {', '.join(map(str, m['weeks'])) or 'none yet'}" + (f"; {m['note']}" if m["note"] else "") + ".")
    L += ["", "Small samples: one week is 54 forecasts, 6 per category. Read a category as weak only when it stays above the "
              "coin flip over several weeks."]
    return L


def summary(rec):
    parts = []
    for i, (k, m) in enumerate(rec["methods"].items()):
        a = m["all"]
        if not a["n"]:
            parts.append(f"{NAMES.get(k, k)} none graded" + (f" ({m['note']})" if m["note"] else "")); continue
        parts.append(f"{NAMES.get(k, k)} {a['n']}" + (f" forecasts over {len(m['weeks'])} week(s)" if i == 0 else "") + f", Brier {a['brier']:.3f}"
                     + (f", favourite right {a['hits']} of {a['calls']}" if i == 0 and a["calls"] else ""))
    return "; ".join(parts)


def run(weeks_dir=WEEKS, sources=None, out=OUT):
    rec = grade(weeks_dir, sources)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False); f.write("\n")
    with open(os.path.splitext(out)[0] + ".md", "w", encoding="utf-8") as f:
        f.write("\n".join(render(rec)) + "\n")
    return rec


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--weeks-dir", default=WEEKS); ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    print(f"CATEGORY GRADE: PASS — {summary(run(a.weeks_dir, None, a.out))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
