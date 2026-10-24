#!/usr/bin/env python3
"""Red-first tests for the kit's .gitattributes merge drivers (owner 2026-10-24, incident decision 1: the morning
merge of 2026-10-24 conflicted on report/pull-log.md because two same-day PRs on two branches each appended a row).
Each test builds a throwaway git repository carrying the kit's .gitattributes, appends a different row to the file
on two branches, merges, and reads the result. Every expectation is about git's behaviour, not the kit's code.

    python3 scripts/test_merge_drivers.py
"""
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
ATTR = open(os.path.join(KIT, ".gitattributes"), encoding="utf-8").read()


def git(cwd, *args):
    return subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "-c", "commit.gpgsign=false", *args],
                          cwd=cwd, capture_output=True, text=True)


def two_branch_append(path, base_text, ours_row, theirs_row):
    """A repo with the kit's .gitattributes and `path` holding base_text; ours and theirs each append one row; merge theirs
    into ours. Returns (merge returncode, the merged file text or None, conflicted paths)."""
    d = tempfile.mkdtemp()
    git(d, "init", "-q", "-b", "main")
    open(os.path.join(d, ".gitattributes"), "w").write(ATTR)
    os.makedirs(os.path.dirname(os.path.join(d, path)), exist_ok=True)
    open(os.path.join(d, path), "w").write(base_text)
    git(d, "add", "-A"); git(d, "commit", "-q", "-m", "base")
    git(d, "checkout", "-q", "-b", "theirs")
    open(os.path.join(d, path), "a").write(theirs_row); git(d, "commit", "-q", "-am", "theirs")
    git(d, "checkout", "-q", "main")
    open(os.path.join(d, path), "a").write(ours_row); git(d, "commit", "-q", "-am", "ours")
    m = git(d, "merge", "--no-edit", "theirs")
    conflicted = git(d, "diff", "--name-only", "--diff-filter=U").stdout.split()
    text = open(os.path.join(d, path), encoding="utf-8").read()
    return m.returncode, text, conflicted


class PullLog(unittest.TestCase):
    BASE = "| date | request | a | b | c | result |\n|---|---|---|---|---|---|\n| 2026-10-23 | earlier row | 0 | 0 | 0 | x |\n"

    def test_two_rows_appended_on_two_branches_merge_without_conflict_and_both_survive(self):
        rc, text, conflicted = two_branch_append("report/pull-log.md", self.BASE,
                                                 "| 2026-10-24 | ours, 00:20Z | 0 | 0 | 0 | box re-pull |\n",
                                                 "| 2026-10-24 | theirs, 00:40Z | 0 | 0 | 0 | scoring loop |\n")
        self.assertEqual((rc, conflicted), (0, []), text)
        self.assertIn("ours, 00:20Z", text); self.assertIn("theirs, 00:40Z", text)
        self.assertNotIn("<<<<<<<", text)
        self.assertEqual(text.count("| 2026-10-24 |"), 2)


class RunLedger(unittest.TestCase):
    def test_the_existing_union_driver_still_merges_two_appended_rows(self):
        rc, text, conflicted = two_branch_append("report/run-ledger.jsonl", '{"name": "a"}\n', '{"name": "ours"}\n', '{"name": "theirs"}\n')
        self.assertEqual((rc, conflicted), (0, []), text)
        self.assertEqual(text.count("\n"), 3)


class NoDriver(unittest.TestCase):
    def test_a_file_without_a_driver_conflicts_the_same_way_the_morning_merge_did(self):
        rc, text, conflicted = two_branch_append("gates.json", '{"verdict": "PASS", "run": 0}\n',
                                                 '{"verdict": "PASS", "run": 1}\n', '{"verdict": "PASS", "run": 2}\n')
        self.assertNotEqual(rc, 0); self.assertEqual(conflicted, ["gates.json"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
