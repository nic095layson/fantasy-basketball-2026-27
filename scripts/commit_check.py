#!/usr/bin/env python3
"""After the run's commit: nothing the run wrote may still be uncommitted (owner 2026-10-26, option 2A).

The morning and afternoon prompts carry hand-kept commit lists. Three times a script gained an output the lists did
not name (report/league from league_table.py, report/form from form_board.py, report/calibration* from
scoreboard_intake.py and score_week.py), and the run left it behind for the next run to stash as a "leftover".
This check runs after the commit and fails loudly instead: any change still in the tree under data/ or report/ is
named, and `--expected` additionally names a path the run says it wrote that never reached a commit.

    python3 scripts/commit_check.py [--root DIR] [--expected PATH ...]

Exit 0 = clean. Exit 1 = FAIL, with every path listed.
"""
import argparse
import os
import subprocess
import sys

WATCHED = ("data/", "report/")


def dirty(root):
    """Paths still uncommitted under the watched roots, as git reports them."""
    # --untracked-files=all: git otherwise collapses a new directory to "report/", hiding which file was left behind
    p = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=root, capture_output=True, text=True)
    if p.returncode != 0:
        return None
    out = []
    for line in p.stdout.splitlines():
        path = line[3:].strip().strip('"')
        if " -> " in path:          # a rename: the destination is what is uncommitted
            path = path.split(" -> ", 1)[1]
        if path.startswith(WATCHED):
            out.append(path)
    return sorted(out)


def check(root, expected=None):
    left = dirty(root)
    if left is None:
        return 1, "COMMIT CHECK: FAIL — not a git checkout, so nothing could be verified"
    missing = []
    if expected:
        tracked = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True).stdout.splitlines()
        missing = sorted(p for p in expected if p not in tracked)
    if not left and not missing:
        return 0, "COMMIT CHECK: PASS — the tree is clean under " + ", ".join(WATCHED)
    msg = ["COMMIT CHECK: FAIL — the run's outputs are not all committed:"]
    msg += [f"  - uncommitted: {p}" for p in left]
    msg += [f"  - never committed (the run says it wrote this): {p}" for p in missing]
    return 1, "\n".join(msg)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--expected", nargs="*", default=None, help="paths the run reported in its WROTE manifest")
    a = ap.parse_args()
    rc, msg = check(a.root, a.expected)
    print(msg)
    return rc


if __name__ == "__main__":
    sys.exit(main())
