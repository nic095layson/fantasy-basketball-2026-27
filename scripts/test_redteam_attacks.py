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


class ShippedList(unittest.TestCase):
    """Owner 2026-10-29 (audit F2): the known-answer, join, consistency and ties attacks carry the engine they ran on;
    A-3 compares against the live engine's references (owner "Repoint to current runs", 2026-10-29)."""

    def test_attacks_a1_to_a4_name_a_commit_field_their_records_carry(self):
        root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
        with open(os.path.join(root, "scripts", "redteam", "attacks.json"), encoding="utf-8") as f:
            attacks = {a["id"]: a for a in json.load(f)["attacks"]}
        for i in ("A-1", "A-2", "A-3", "A-4"):
            a = attacks[i]
            self.assertTrue(a.get("commit_field"), i)
            with open(os.path.join(root, a["record"]), encoding="utf-8") as f:
                self.assertTrue(A._dig(json.load(f), a["commit_field"]), i)



class KitFiles(unittest.TestCase):
    """Audit finding F3 (2026-11-12): A-10's record read CURRENT after scripts/il_return.py had changed, because the
    fingerprint followed the deck engine only. An attack that names kit_files is held to their content."""
    def setUp(self):
        self.d = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.d, "s"))
        with open(os.path.join(self.d, "s", "attack.py"), "w") as f:
            f.write("print('x')\n")
        self.row = {"id": "A-1", "name": "n", "question": "q", "script": "s/attack.py", "record": "rec.json",
                    "commit_field": "fingerprint.deck_head", "kit_files": ["s/attack.py"], "added": "2026-11-12"}

    def record(self, kit=True):
        fp = {"deck_head": "abc1234"}
        if kit:
            fp["kit_sha256"] = A.kit_fingerprint(["s/attack.py"], root=self.d)
        with open(os.path.join(self.d, "rec.json"), "w") as f:
            json.dump({"fingerprint": fp}, f)

    def check(self):
        return A.check({"attacks": [self.row]}, root=self.d, live_commit="abc1234")

    def test_an_unchanged_kit_file_is_current(self):
        self.record()
        rec = self.check()
        self.assertEqual(rec["attacks"][0]["status"], "CURRENT", rec)
        self.assertEqual(rec["kit_fingerprinted"], 1)
        self.assertEqual(rec["verdict"], "PASS")

    def test_one_changed_byte_in_the_kit_file_is_stale(self):
        self.record()
        with open(os.path.join(self.d, "s", "attack.py"), "a") as f:
            f.write("#\n")
        rec = self.check()
        self.assertEqual(rec["attacks"][0]["status"], "STALE")
        self.assertIn("s/attack.py changed since the record was made", rec["attacks"][0]["why"])
        self.assertEqual(rec["verdict"], "FAIL")

    def test_a_record_without_the_hash_is_stale(self):
        self.record(kit=False)
        rec = self.check()
        self.assertEqual(rec["attacks"][0]["status"], "STALE")
        self.assertIn("no hash for kit file s/attack.py", rec["attacks"][0]["why"])

    def test_an_attack_without_kit_files_is_judged_as_before(self):
        self.record(kit=False)
        del self.row["kit_files"]
        rec = self.check()
        self.assertEqual(rec["attacks"][0]["status"], "CURRENT")
        self.assertEqual(rec["kit_fingerprinted"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)


class EngineFingerprint(unittest.TestCase):
    """Owner 2026-10-23 (D1): an attack record is STALE only when the engine files changed between its commit and
    the live one, not when any deck commit landed (the 10/23 audit: a CLAUDE.md-only deck commit staled 5 of 9)."""
    def setUp(self):
        import subprocess
        self.deck = tempfile.mkdtemp()
        def git(*a):
            return subprocess.run(["git", "-C", self.deck] + list(a), capture_output=True, text=True, check=True).stdout.strip()
        git("init", "-q"); git("config", "user.email", "t@t"); git("config", "user.name", "t")
        os.makedirs(os.path.join(self.deck, "arena")); os.makedirs(os.path.join(self.deck, "scripts"))
        for p in ("arena/arena.py", "scripts/hoops.py", "README.md"):
            with open(os.path.join(self.deck, p), "w") as f:
                f.write("v1\n")
        git("add", "-A"); git("commit", "-q", "-m", "engine v1"); self.c_engine = git("rev-parse", "--short", "HEAD")
        with open(os.path.join(self.deck, "README.md"), "w") as f:
            f.write("docs only\n")
        git("add", "-A"); git("commit", "-q", "-m", "docs"); self.c_docs = git("rev-parse", "--short", "HEAD")
        with open(os.path.join(self.deck, "arena/arena.py"), "w") as f:
            f.write("v2\n")
        git("add", "-A"); git("commit", "-q", "-m", "engine v2"); self.c_engine2 = git("rev-parse", "--short", "HEAD")
        self.root = tempfile.mkdtemp(); os.makedirs(os.path.join(self.root, "s"))
        with open(os.path.join(self.root, "s", "attack.py"), "w") as f:
            f.write("print('x')\n")
        with open(os.path.join(self.root, "rec.json"), "w") as f:
            json.dump({"engine_commit": self.c_engine}, f)
        self.attacks = {"attacks": [{"id": "A-1", "name": "n", "question": "q", "script": "s/attack.py", "record": "rec.json",
                                     "commit_field": "engine_commit", "added": "2026-10-19"}]}

    def test_a_docs_only_deck_commit_keeps_the_record_current(self):
        rec = A.check(self.attacks, root=self.root, live_commit=self.c_docs, deck=self.deck)
        self.assertEqual(rec["attacks"][0]["status"], "CURRENT", rec["attacks"][0])
        self.assertEqual(rec["verdict"], "PASS")

    def test_an_engine_change_still_stales_the_record(self):
        rec = A.check(self.attacks, root=self.root, live_commit=self.c_engine2, deck=self.deck)
        self.assertEqual(rec["attacks"][0]["status"], "STALE", rec["attacks"][0])

    def test_the_engine_commit_of_a_revision_is_the_last_commit_touching_the_engine_files(self):
        self.assertEqual(A.engine_commit(self.deck, self.c_docs), self.c_engine)
        self.assertEqual(A.engine_commit(self.deck, self.c_engine2), self.c_engine2)
