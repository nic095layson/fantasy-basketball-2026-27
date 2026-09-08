#!/usr/bin/env python3
"""After-report publication gate (fix F2, adopted 2026-09-08).

Born from Ben Simmons shipping as a Clipper. On 2026-09-08 a garbled search
summary said he signed with the LA Clippers; he signed with Sacramento. The
claim skipped every gate because the two-independent-sources rule fires only
for pool-row edits — Simmons touches no row — yet the after-report, the deck
colophon, and two PR bodies all published it as fact. It was the FIFTH
documented search-summary garble. Verification was gated on row impact;
publication was not. This gate closes that split for the one surface it can
check mechanically: the after-report.

Checks, for a given report (default: the newest report/after-reports/*.md):

  1. Required structure: a "Pull window:" line, a roster-changes section
     (## 1.), a watchlist section, and an "Open-item receipts" section
     (fix F1 — the deck plane's judgment_open_items.py --check-report
     verifies the receipts CONTENT against the flagged list; this gate only
     requires the section to exist on the kit plane).
  2. Publication rule: every TABLE ROW that asserts a transaction (contains
     a transaction trigger word) must either name at least TWO distinct
     outlets from the lexicon below, or carry an explicit [SINGLE-SOURCE]
     label so the reader can apply their own discount. Scope is table rows —
     tables are where this report states transactions as fact; prose remains
     the operator's oath.
  3. The pull-log has a row for the report's date.

Exit 0 = pass. Exit 1 = fail, problems listed on stdout.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(HERE, "after-reports")
PULL_LOG = os.path.join(HERE, "pull-log.md")

# Outlet lexicon — names count once each; add outlets as they enter use.
OUTLETS = [
    "espn", "yahoo", "hoopsrumors", "hoops rumors", "realgm", "spotrac",
    "nba.com", "nba communications", "shams", "charania", "woj",
    "wojnarowski", "athletic", "cbs", "bleacher", "b/r", "hoopshype",
    "nbc", "si.com", "sports illustrated", "rotowire", "cp24", "blogto",
    "globe and mail", "cnn", "deseret", "sportico", "heavy", "yardbarker",
    "daily memphian", "bvm", "kings herald", "ap", "associated press",
    "abc", "tsn", "fischer", "clutchpoints", "rotoballer", "espn la crosse",
]
TRIGGERS = re.compile(
    r"→|->|\b(sign(?:ed|s|ing)?|trade[ds]?|waive[ds]?|acquire[ds]?|"
    r"agree[ds]?|guaranteed|withdrew|withdraw[ns]?|bought out|buyout|"
    r"release[ds]?|retire[ds]?|claimed)\b", re.I)
EXEMPT = re.compile(r"\[SINGLE-SOURCE\]|\*date not stated by source\*|"
                    r"pre-window", re.I)


def outlet_count(text):
    low = text.lower()
    found = set()
    for o in OUTLETS:
        if o in low:
            found.add(o)
    # "ap" alone is too short to substring-match safely; require word-bound
    if "ap" in found and not re.search(r"\bap\b", low):
        found.discard("ap")
    # collapse aliases that would double-count one outlet
    if "hoops rumors" in found:
        found.discard("hoopsrumors")
    if "associated press" in found:
        found.discard("ap")
    if "wojnarowski" in found:
        found.discard("woj")
    if "charania" in found:
        found.discard("shams")
    return len(found)


def check(path):
    problems = []
    text = open(path, encoding="utf-8").read()
    name = os.path.basename(path)

    # 1. structure
    m = re.search(r"Pull window: (\d{4}-\d{2}-\d{2}) → (\d{4}-\d{2}-\d{2})",
                  text)
    if not m:
        problems.append("no 'Pull window: YYYY-MM-DD → YYYY-MM-DD' line")
    for anchor, why in (
        ("## 1.", "roster-changes section (## 1.)"),
        ("Watchlist", "watchlist section"),
        ("Open-item receipts", "'Open-item receipts' section (fix F1 — "
         "also run the deck's judgment_open_items.py --check-report "
         "against this file)"),
    ):
        if anchor not in text:
            problems.append(f"missing {why}")

    # 2. publication rule over table rows. Scoped by table HEADER: a table
    # whose header names a source/evidence/receipts column cites one outlet
    # per row by design (the table is the multi-source), and fix/decision
    # tables discuss transactions without asserting them — both classes are
    # skipped whole. Everything else that asserts a transaction must carry
    # two outlets or the [SINGLE-SOURCE] label.
    SKIP_HEADER = re.compile(
        r"source|evidence|says|receipt|query|fix|decision|mechanism|"
        r"recommendation|kills|unblocks", re.I)
    skip_table = False
    prev_blank = True
    for i, line in enumerate(text.splitlines(), 1):
        row = line.strip()
        if not row.startswith("|"):
            prev_blank = True
            skip_table = False
            continue
        if prev_blank:  # first row of a table = its header
            skip_table = bool(SKIP_HEADER.search(row))
            prev_blank = False
            continue
        if set(row) <= {"|", "-", " ", ":"}:
            continue  # separator
        if skip_table or not TRIGGERS.search(row) or EXEMPT.search(row):
            continue
        n = outlet_count(row)
        if n < 2:
            problems.append(
                f"line {i}: transaction row has {n} outlet source(s) and no "
                f"[SINGLE-SOURCE] label — {row[:90]!r}")

    # 3. pull-log row
    if m:
        date = m.group(2)
        try:
            log = open(PULL_LOG, encoding="utf-8").read()
            if f"| {date} |" not in log:
                problems.append(f"pull-log.md has no row for {date}")
        except OSError:
            problems.append("pull-log.md missing")

    if problems:
        print(f"REPORT GATE: FAIL — {name}")
        for p in problems:
            print(f"  {p}")
        return 1
    print(f"REPORT GATE: PASS — {name} (structure, publication rule, "
          "pull-log row)")
    return 0


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        cands = sorted(glob.glob(os.path.join(REPORT_DIR, "after-report-*.md")))
        if not cands:
            print("REPORT GATE: FAIL — no after-reports found")
            sys.exit(1)
        path = cands[-1]
    sys.exit(check(path))


if __name__ == "__main__":
    main()
