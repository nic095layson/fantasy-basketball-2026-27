#!/usr/bin/env python3
"""Trace every figure in after-report-2026-10-22-day-findings.md to a cited source (owner 2026-10-22: "Provide
thorough, detailed report of findings from today ... in plain language"; criterion R2 of the plan: every figure traced
to a source line, checked mechanically).

Sources, all committed or pinned:
  - the 20 after-reports: 18 on main under report/after-reports/, two on their draft branches (git show of 7f455ca
    for #164 and 7ee73f0 for #166);
  - the records beside the report (git histories, commit times, the runner's 10/22 records, the stored-prompt read);
  - the code the report quotes: scripts/co_gm.py on main and the deck's arena/mocks/league_sim.py and
    arena/data/weekly_matchups_2025-26_README.md on deck main (DECK_REPO, default ../yahoo-fantasy-basketball).

Checks:
  1. every number, date, clock time, commit hash and PR number in the report appears in a source (signs folded:
     the report's "−" is the sources' "−" or "-");
  2. the counts the report makes itself are recomputed from the same files: reports in the window, PRs merged on
     10/21 PT, rows and labels of the §2 table, the four errors this report adds, the seven that reached the owner,
     the runner's box and week-card figures, and the code lines it cites.

Writes trace.json beside itself; exit 1 if any figure is unmatched or any count disagrees."""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DECK = os.environ.get("DECK_REPO") or os.path.join(os.path.dirname(KIT), "yahoo-fantasy-basketball")
REPORT = os.environ.get("TRACE_REPORT") or os.path.join(KIT, "report", "after-reports", "after-report-2026-10-22-day-findings.md")
RUNNER = os.path.join(HERE, "runner-2026-10-22")

ON_MAIN = ["2026-10-21-" + n for n in ("board-test", "corrections", "council-fixes", "deck-patch", "deck-render",
                                       "flaim", "gauntlet", "gscore-column", "independent-audit", "merge-check",
                                       "pickups-file", "proceed", "redteam-audit", "week-matchup",
                                       "zscore-assessment")] + \
          ["2026-10-22-" + n for n in ("gp-reconstruction", "risk-rows", "season-cv")]
ON_DRAFTS = {"2026-10-22-flaim-history-totals": "7f455ca", "2026-10-22-hunter-override": "7ee73f0"}


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout


def sources():
    out = {}
    for n in ON_MAIN:
        p = os.path.join(KIT, "report", "after-reports", f"after-report-{n}.md")
        out[f"after-report-{n}.md"] = open(p, encoding="utf-8").read()
    for n, c in ON_DRAFTS.items():
        out[f"after-report-{n}.md@{c}"] = git(KIT, "show", f"{c}:report/after-reports/after-report-{n}.md")
    for root, _, files in os.walk(HERE):
        for f in files:
            if f.endswith((".txt", ".json", ".md", ".csv")) and f not in ("trace.json", "plants.txt"):  # plants.txt records planted wrong values; never a source
                out[os.path.relpath(os.path.join(root, f), HERE)] = open(os.path.join(root, f), encoding="utf-8").read()
    out["scripts/co_gm.py"] = git(KIT, "show", "origin/main:scripts/co_gm.py")
    out["deck arena/mocks/league_sim.py"] = git(DECK, "show", "origin/main:arena/mocks/league_sim.py")
    out["deck weekly_matchups README"] = git(DECK, "show", "origin/main:arena/data/weekly_matchups_2025-26_README.md")
    return out


TOKEN = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?Z)?)"
    r"|(?P<pr>#\d+)"
    r"|(?P<hash>\b[0-9a-f]{7,12}\b(?=[^0-9a-z]))"
    r"|(?P<clock>\b\d{1,2}:\d{2}\b)"
    r"|(?P<num>[−+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)")

# figures that are code line numbers, verified by a count check below rather than by a text match
VERIFIED_BY_CHECK = {"177": "co_gm.py lines 162-177 pass LINES_TAG to league_sim.py",
                     "162": "co_gm.py line 162 defines sim_pool_names",
                     "33": "league_sim.py line 33 loads players_<tag>.csv"}


def body(text):
    """The report minus the two sections carried verbatim from earlier reports (checked by their own deck gates)."""
    a = text.index("This report touched no pool row of the frozen snapshot.")
    b = text.index("## Decision sheet")
    return text[:a] + text[b:]


def found(tok, kind, src):
    variants = {tok}
    if kind == "pr":  # open_prs.json carries PR numbers as JSON fields
        variants.add(f'"number": {tok[1:]},')
    if kind == "clock":  # a 12-hour clock in the plain-language section is the same time as the 24-hour record
        h, mm = tok.split(":")
        variants |= {f"{int(h):02d}:{mm}"} | ({f"{int(h) + 12}:{mm}"} if int(h) < 12 else set())
    if kind == "num":
        bare = tok.replace("−", "-")
        variants |= {bare, bare.lstrip("+-"), tok.replace("−", "−")}
        if bare.lstrip("+-").startswith("0."):
            variants.add(bare.lstrip("+-")[1:])  # .493 written as 0.493 or the reverse
    for v in sorted(variants):  # sorted: set order varies with hash randomization (two runs differed, 2026-10-22)
        if not v:
            continue
        pat = re.escape(v)
        if kind == "num" or (kind == "pr" and v.startswith("#")):
            pat = r"(?<![\d.])" + pat + r"(?![\d])"
        for name, s in src.items():
            if re.search(pat, s):
                return name
    return None


def counts(text, src):
    checks = []

    def check(what, claimed, actual):
        checks.append(dict(check=what, claimed=claimed, actual=actual, ok=claimed == actual))

    times = [l.split(" | ") for l in src["report_commit_times.txt"].splitlines() if l.strip()]
    day = [t for t in times if t[1].startswith("10-21")]
    check("after-reports committed 10/21 PT", 17, len(day))
    check("after-reports committed 10/20 PT (background)", 3, len(times) - len(day))
    check("after-reports in all", 20, len(times))

    kit = [l for l in src["git_kit_first_parent.txt"].splitlines() if l.startswith("10-21")]
    kit_prs = [re.search(r"#(\d+)", l).group(1) for l in kit if re.search(r"#\d+", l)
               and not l.split(" ", 4)[-1].startswith(("Restart", "Merge prior"))]
    check("kit PRs merged 10/21 PT", 15, len(set(kit_prs)))
    deck = [l for l in src["git_deck_first_parent.txt"].splitlines() if l.startswith("10-21")]
    check("deck PRs merged 10/21 PT", 2, len(deck))

    s2 = text[text.index("## 2. Did the data model improve?"):text.index("**Verdict, item by item.**")]
    rows = [l for l in s2.splitlines() if l.startswith("| ") and not l.startswith("| change") and "---" not in l]
    labels = [l.split(" | ")[2] for l in rows]
    check("§2 rows", 13, len(rows))
    check("§2 rows labelled IN USE", 6, sum(x.startswith("IN USE") for x in labels))
    check("§2 rows labelled PARTLY IN USE", 2, sum(x.startswith("PARTLY") for x in labels))
    check("§2 rows labelled BUILT, NOT IN USE", 4, sum(x.startswith("BUILT") for x in labels))
    check("§2 rows labelled UNPROVEN", 1, sum(x.startswith("UNPROVEN") for x in labels))

    s6 = text[text.index("## 6. Errors"):text.index("## Watchlist")]
    erows = [l for l in s6.splitlines() if re.match(r"\| [ABCDS]\d ", l)]
    mine = [l.split(" | ")[0].strip("| ") for l in erows if "this report" in l.split(" | ")[3]]
    check("errors this report adds", ["A7", "A8", "A9", "S1"], mine)
    reached = re.findall(r"^  - ([AS]\d(?:, [AS]\d)*(?: and [AS]\d)?)", s6, re.M)
    ids = sorted({i for r in reached for i in re.findall(r"[AS]\d", r)})
    check("errors that reached the owner, a live page or a merged file", 7, len(ids))

    box = json.loads(src[os.path.join("runner-2026-10-22", "box_2026-10-21_sources.json")])
    check("ESPN events on 10/21", 11, box["espn_events"])
    check("ESPN final on 10/21", 8, box["espn_final"])
    sched = src[os.path.join("runner-2026-10-22", "schedule_2026-10-21.csv")].strip().splitlines()
    check("scheduled games on 10/21", 11, len(sched))
    west = {"GSW,LAL", "PHO,POR", "SAC,LAC"}
    sched_pairs = {",".join(r.split(",")[2:4]) for r in sched}
    check("the three named games are on the 10/21 schedule", True, west <= sched_pairs)
    wk = json.loads(src[os.path.join("runner-2026-10-22", "week_card_to_date.json")])
    check("week-card stats where Yahoo differs from the rebuild", 21, wk["n_differences"])
    check("Yahoo higher on every differing stat", True, wk["yahoo_higher_in_all"])
    prompt = json.loads(src[os.path.join("runner-2026-10-22", "stored_prompt_read.json")])
    check("stored prompt names Flaim", False, prompt["prompt_mentions_flaim"])

    co = src["scripts/co_gm.py"].splitlines()
    check("co_gm.py line 162 defines sim_pool_names", True, co[161].startswith("def sim_pool_names"))
    check("co_gm.py lines 162-177 pass LINES_TAG to league_sim.py", True,
          any("league_sim.py" in l and "LINES_TAG" in l for l in co[161:177]))
    check("co_gm.py LINES_TAG is v69", True, 'LINES_TAG = "v69"' in src["scripts/co_gm.py"])
    ls = src["deck arena/mocks/league_sim.py"].splitlines()
    check("league_sim.py line 33 loads players_<tag>.csv", True, "players_{tag}.csv" in ls[32])
    readme = src["deck weekly_matchups README"]
    check("README schema line says player-games actually played", True,
          "player-games actually played" in readme)
    check("README correction says gp does not equal the player-games", True, "does **not** equal" in readme)
    # the prose that states each count must state the computed value (a planted "9 final" or "7 of the 13" fails here;
    # a bare number search alone cannot catch it, because small numbers appear somewhere in the sources)
    words = "zero one two three four five six seven eight nine ten eleven twelve thirteen".split()

    def says(what, phrase):
        check(f"prose states: {what}", True, phrase in text)

    says("reports in the window", f"{len(day)} after-reports were committed in that window")
    says("background reports", f"{words[len(times) - len(day)].capitalize()} more were committed on Monday evening")
    says("kit PR count", f"#163 ({len(set(kit_prs))})")
    says("deck PR count", f"#130 ({len(deck)})")
    n_in = sum(x.startswith("IN USE") for x in labels)
    says("IN USE share", f"That is {n_in} of the {len(rows)} rows")
    says("box events and finals (§3)", f"ESPN listed {box['espn_events']} events and {box['espn_final']} final")
    says("box events and finals (A9)", f"ESPN listed {box['espn_events']} events, {box['espn_final']} final")
    says("headline finals", f"only {box['espn_final']} of Tuesday's {len(sched)} games were final")
    says("schedule games", f"The schedule has {len(sched)} games that day")
    says("Yahoo differs", f"It differs from the box-score rebuild on {wk['n_differences']} stats")
    says("errors this report adds", f"plus {words[len(mine)]} found while writing this one")
    says("errors that reached", f"{words[len(ids)].capitalize()} reached you, a live page or a merged file")
    # the three named games are absent from the box record (so they are the 11 - 8 not final)
    named = {"Golden State", "Phoenix", "Sacramento"}
    check("the three named games are absent from the 10/21 box record", True,
          not any(n in g for g in box["games_in_record"] for n in named))

    # the 2026-10-22 correction (§3): the opponent-side gap was Acuff's unmatched 10/21 line, bound to its pins
    C = "correction-2026-10-22"
    STATS = ["fgm", "fga", "ftm", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]
    rec = json.loads(src[os.path.join(C, "recon.json")])
    cards = json.loads(src[os.path.join(C, "week_cards.json")])
    fixed = json.loads(src[os.path.join(C, "name_fix_week_card.json")])
    moves = json.loads(src[os.path.join(C, "league_moves.json")])
    pr = json.loads(src[os.path.join(C, "pr_168.json")])
    row = lambda who: next(r for r in rec["10"]["rows"] if r["date"] == "2026-10-21" and r["player"] == who)
    acuff, santos = row("Darius Acuff Jr."), row("Gui Santos")
    c0554, c1415 = cards["51cf6b3"], cards["2f2aea8"]
    complete = c1415["yahoo"]["opp"]
    check("correction: Acuff played on 10/21 and the box pull left him unmatched", (True, None),
          (acuff["played"], acuff["pool_name"]))
    a = acuff["line"]
    says("correction: Acuff's line", f"{a['fgm']}-{a['fga']} FG, {a['ftm']}-{a['fta']} FT, {a['tpm']} 3PM, {a['pts']} PTS, "
                                     f"{a['reb']} REB, {a['ast']} AST, {a['stl']} STL, {a['blk']} BLK, {a['tov']} TO")
    check("correction: the reconciliation read the 14:15Z card's Yahoo totals", (complete, c1415["yahoo"]["me"]),
          (rec["10"]["yahoo"], rec["11"]["yahoo"]))
    check("correction: 05:54 PT rebuild + Acuff's line = complete Yahoo, all 11", True,
          all(c0554["rebuild"]["opp"][k] + a[k] == complete[k] for k in STATS))
    says("correction: the FGA sum", f"FGA {c0554['rebuild']['opp']['fga']} + {a['fga']} = {complete['fga']}")
    opp = sorted(d["stat"] for d in c1415["differences"] if d["side"] == "opp")
    check("correction: the 14:15Z card differs on Acuff's nonzero stats only", sorted(k for k in STATS if a[k]), opp)
    check("correction: the 14:15Z card agrees on your side", 0, sum(d["side"] == "me" for d in c1415["differences"]))
    says("correction: the 14:15Z count", f"differs from Yahoo on {len(opp)} of the {len(STATS)} stats")
    check("correction: actual lineups reproduce Yahoo, both teams", (True, True), (rec["10"]["equal"], rec["11"]["equal"]))
    check("correction: no benched or IL player played", 0,
          sum(r["played"] and r["slot"] in ("BN", "IL", "IL+") for t in rec.values() for r in t["rows"]))
    dropped = lambda c: [m for m in moves[c]["moves"] if "Gui Santos" in m["dropped"]]
    check("correction: Santos's drop first shows at e7b69bb, not 21d815d", (0, 1), (len(dropped("21d815d")), len(dropped("e7b69bb"))))
    check("correction: the run times named", ("2026-10-22T14:15:13Z", "2026-10-22T14:31:49Z", "2026-10-22T14:44:17Z"),
          (c1415["t0"], cards["21d815d"]["t0"], cards["e7b69bb"]["t0"]))
    s = santos["line"]
    # records_from is a worktree path, so the fixed card is tied to the 14:44Z records by its numbers: e7b69bb's
    # rebuild plus Acuff's line, the one row the fix adds
    check("correction: the fixed card is e7b69bb's rebuild plus Acuff's line", True,
          all(cards["e7b69bb"]["rebuild"]["opp"][k] + a[k] == fixed["week_card"]["rebuild"]["opp"][k] for k in STATS))
    check("correction: with the fix, the opponent's gap is exactly Santos's line", True,
          {d["stat"]: d["yahoo"] - d["rebuild"] for d in fixed["week_card"]["differences"] if d["side"] == "opp"}
          == {k: s[k] for k in STATS if s[k]})
    says("correction: Santos's line", f"{s['fgm']}-{s['fga']} FG, {s['pts']} PTS, {s['reb']} REB")
    check("correction: #168 is an open draft, not merged", (168, "open", True, False),
          (pr["number"], pr["state"], pr["draft"], pr["merged"]))

    # the 05:54 PT update (§3): the scheduled run's record, bound to the prose
    wk2 = json.loads(src[os.path.join("runner-2026-10-22", "week_card_to_date_0554PT.json")])
    box2 = json.loads(src[os.path.join("runner-2026-10-22", "box_2026-10-21_sources_0554PT.json")])
    c2 = src[os.path.join("runner-2026-10-22", "commit_0554PT.txt")]
    check("05:54 run: ESPN events and finals", (11, 11), (box2["espn_events"], box2["espn_final"]))
    says("05:54 run box line", f"ESPN listed {box2['espn_events']} events and {box2['espn_final']} final")
    says("05:54 run split", f"the {wk2['n_differences']} differences split {wk2['n_me']} and {wk2['n_opp']}")
    check("05:54 run: rebuild higher on every one of yours", True, wk2["me_rebuild_higher_in_all"])
    check("05:54 run: Yahoo higher on every one of theirs", True, wk2["opp_yahoo_higher_in_all"])
    sha = wk2["yahoo_pull_input"]["sha256"]
    check("both runs read the same Yahoo pin", True, f"847748e (20:46 PT run): {sha}" in c2)
    says("the shared pin's sha256 prefix", sha[:12])

    # R1: each of the 20 reports is cited outside the commit-time table
    table_start = text.index("**The 20 reports, by commit time**")
    table_end = text.index("## 2. Did the data model improve?")
    rest = text[:table_start] + text[table_end:]
    short = ["proceed", "gauntlet", "deck-patch", "board-test", "deck-render", "week-matchup", "independent-audit",
             "flaim", "merge-check", "pickups-file", "zscore-assessment", "gscore-column", "risk-rows",
             "gp-reconstruction", "season-cv", "flaim-history-totals", "hunter-override", "corrections",
             "redteam-audit", "council-fixes"]
    cited = [n for n in short if re.search(r"(?<![\w-])" + re.escape(n) + r"(?![\w-])", rest)]
    check("R1: reports cited outside the commit-time table", short, cited)

    # context pins: a headline figure appears, in the same wording, in the source the report names beside it
    pins = [
        ("2026-10-22-season-cv", "5.2996 before, 5.2251 after"),
        ("2026-10-22-season-cv", "+0.0304 before, +0.0257 after"),
        ("2026-10-22-season-cv", "goes from +0.0047 to −0.0042"),
        ("2026-10-22-season-cv", "24.48 / 23.72 before and 24.69 / 22.94 after"),
        ("2026-10-22-season-cv", "about 0.43 points per seed"),
        ("2026-10-22-season-cv", "1.24–1.43 times the old ones"),
        ("2026-10-21-zscore-assessment", "10,332 rows"),
        ("2026-10-21-zscore-assessment", "1.53 to 2.46 times"),
        ("2026-10-21-zscore-assessment", "−0.36 and −0.61 points"),
        ("2026-10-21-zscore-assessment", "won 21.4% of each-category seasons, against an 8.33% baseline"),
        ("2026-10-21-proceed", "**21.1 % → 23.3 %** and **21.3 % → 24.1 %**"),
        ("2026-10-21-proceed", "deck ×0.78, simulator ×0.852, kit ×0.918"),
        ("2026-10-21-week-matchup", "60.6% to win"),
        ("2026-10-21-week-matchup", "41 player-games against your 35"),
        ("2026-10-21-week-matchup", "**3–6–0**"),
        ("2026-10-22-risk-rows", "8 of 200 rows change"),
        ("2026-10-22-gp-reconstruction", "only 3 of 44 team-weeks"),
        ("2026-10-22-gp-reconstruction", "runs from −7 to +8"),
        ("2026-10-21-gscore-column", "Rank correlation 0.98"),
        ("2026-10-21-gscore-column", "Dyson Daniels 34 → 64"),
        ("2026-10-21-pickups-file", "Drummond lands at #227"),
        ("2026-10-21-merge-check", "100 listed = 87 scored + 10 out + 0 unknown + 3 not projected"),
        ("2026-10-21-redteam-audit", "1,800 of 1,800"),
        ("2026-10-21-council-fixes", "2,174 of them"),
        ("2026-10-22-flaim-history-totals@7f455ca", "3,348 of 3,348"),
        ("2026-10-22-hunter-override@7ee73f0", "exactly 1 of 336 rows"),
        ("2026-10-22-hunter-override@7ee73f0", "−4.21"),
        (os.path.join("runner-2026-10-22", "morning_report_2026-10-22.md"), "Title 23.8% ± 0.6"),
        (os.path.join("runner-2026-10-22", "morning_report_2026-10-22.md"), "4 of 12 roster calls returned data"),
        (os.path.join("runner-2026-10-22", "morning_report_2026-10-22.md"), "152 lines moved by 0.25+"),
        (os.path.join("runner-2026-10-22", "morning_report_2026-10-22.md"), "version 1792640745-5b2e"),
    ]
    for key, phrase in pins:
        name = key if key.startswith("runner") else f"after-report-{key}.md" if "@" not in key else \
            f"after-report-{key.split('@')[0]}.md@{key.split('@')[1]}"
        check(f"pin: {phrase!r} in {name}", True, phrase in src.get(name, ""))
    return checks


def main():
    text = open(REPORT, encoding="utf-8").read()
    src = sources()
    tokens, unmatched = [], []
    for m in TOKEN.finditer(body(text)):
        kind = m.lastgroup
        tok = m.group(kind)
        if kind == "hash" and not re.search(r"[a-f]", tok):
            kind = "num"
        where = found(tok, kind, src)
        if where is None and tok in VERIFIED_BY_CHECK:
            where = "count check: " + VERIFIED_BY_CHECK[tok]
        if kind == "hash" and where is None:
            for repo in (KIT, DECK):
                if subprocess.run(["git", "-C", repo, "cat-file", "-e", tok + "^{commit}"],
                                  capture_output=True).returncode == 0:
                    where = f"git commit in {os.path.basename(repo)}"
        tokens.append(dict(token=tok, kind=kind, source=where))
        if where is None:
            unmatched.append(tok)
    checks = counts(text, src)
    bad = [c for c in checks if not c["ok"]]
    ok_checks = {c["check"] for c in checks if c["ok"]}
    for t in tokens:  # a figure verified only by a count check stands only if that check passed
        if t["source"] and t["source"].startswith("count check: ") and t["source"][13:] not in ok_checks:
            t["source"] = None
            unmatched.append(t["token"])
    rec = dict(report=os.path.relpath(REPORT, KIT), sources=sorted(src), tokens=len(tokens),
               unmatched=sorted(set(unmatched)), count_checks=checks, verdict="PASS" if not unmatched and not bad
               else "FAIL", figures=tokens)
    with open(os.path.join(HERE, "trace.json"), "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"TRACE: {rec['verdict']} — {len(tokens)} figures, {len(set(unmatched))} unmatched "
          f"{sorted(set(unmatched))}; {len(checks) - len(bad)} of {len(checks)} counts agree"
          + ("" if not bad else f"; disagree: {[(c['check'], c['claimed'], c['actual']) for c in bad]}"))
    sys.exit(0 if rec["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
