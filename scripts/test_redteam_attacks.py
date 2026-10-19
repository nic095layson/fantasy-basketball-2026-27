#!/usr/bin/env python3
"""Red-first tests for scripts/redteam/run_attacks.py (post-mortem 2026-10-19, finding 2: the engine changed
under the report and nothing said so).

    python3 scripts/test_redteam_attacks.py
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "redteam"))
import run_attacks as A  # noqa: E402


class Check(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.d, "s"))
        with open(os.path.join(self.d, "s", "attack.py"), "w") as f:
            f.write("print('x')\n")
        with open(os.path.join(self.d, "rec.json"), "w") as f:
            json.dump({"engine_commit": "abc1234", "nested": {"engine_commit": "abc1234"}}, f)

    def attacks(self, **over):
        row = {"id": "A-1", "name": "n", "question": "q", "script": "s/attack.py", "record": "rec.json",
               "commit_field": "engine_commit", "added": "2026-10-19"}
        row.update(over)
        return {"attacks": [row]}

    def test_present_record_on_the_live_commit_passes(self):
        rec = A.check(self.attacks(), root=self.d, live_commit="abc1234")
        self.assertEqual(rec["verdict"], "PASS", rec)
        self.assertEqual(rec["attacks"][0]["status"], "CURRENT")

    def test_missing_record_fails(self):
        rec = A.check(self.attacks(record="nope.json"), root=self.d, live_commit="abc1234")
        self.assertEqual(rec["verdict"], "FAIL")
        self.assertEqual(rec["attacks"][0]["status"], "MISSING")

    def test_missing_script_fails(self):
        rec = A.check(self.attacks(script="s/gone.py"), root=self.d, live_commit="abc1234")
        self.assertEqual(rec["verdict"], "FAIL")

    def test_record_on_another_engine_is_stale(self):
        rec = A.check(self.attacks(), root=self.d, live_commit="def5678")
        self.assertEqual(rec["verdict"], "FAIL")
        self.assertEqual(rec["attacks"][0]["status"], "STALE")
        self.assertIn("abc1234", rec["attacks"][0]["why"])

    def test_nested_commit_field_is_read(self):
        rec = A.check(self.attacks(commit_field="nested.engine_commit"), root=self.d, live_commit="abc1234")
        self.assertEqual(rec["attacks"][0]["status"], "CURRENT")

    def test_record_without_a_commit_field_is_unfingerprinted_not_stale(self):
        rec = A.check(self.attacks(commit_field=None), root=self.d, live_commit="zzz")
        self.assertEqual(rec["verdict"], "PASS")
        self.assertEqual(rec["attacks"][0]["status"], "UNFINGERPRINTED")

    def test_duplicate_ids_fail(self):
        a = self.attacks()
        a["attacks"].append(dict(a["attacks"][0]))
        rec = A.check(a, root=self.d, live_commit="abc1234")
        self.assertEqual(rec["verdict"], "FAIL")
        self.assertTrue(any("duplicate" in p for p in rec["problems"]), rec["problems"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
