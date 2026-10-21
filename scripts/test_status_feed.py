#!/usr/bin/env python3
"""Red-first tests for scripts/status_feed.py (Session 1 item 4; plan §4 A3).

The gate the plan asks for: a Q/O-flagged row at availability 1.00 with no receipt fails
the build (Durant and Bridges sat Q on draft night with nothing reading it).

    python3 scripts/test_status_feed.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import status_feed as SF  # noqa: E402

RECEIPT = {"source": "yahoo rosters page", "file": "x.pdf", "captured": "2026-10-15", "text": "Q"}


class Tiers(unittest.TestCase):
    def test_letters_map_to_the_stated_tiers(self):
        self.assertEqual(SF.tier(None), ("healthy", 1.00))
        self.assertEqual(SF.tier("Q"), ("questionable", 0.50))
        self.assertEqual(SF.tier("O"), ("out", 0.00))

    def test_unknown_letter_is_refused_not_guessed(self):
        with self.assertRaises(ValueError):
            SF.tier("GTD?")


class Gate(unittest.TestCase):
    def row(self, status, avail, receipts):
        return {"player": "Kevin Durant", "yahoo_status": status, "availability": avail, "receipts": receipts}

    def test_flagged_row_at_full_availability_without_receipt_fails(self):
        problems = SF.check([self.row("Q", 1.00, [])])
        self.assertTrue(problems and "Kevin Durant" in problems[0], problems)

    def test_flagged_row_at_full_availability_with_receipt_passes(self):
        # an owner override back to 1.00 is allowed when it carries its dated receipt
        self.assertEqual(SF.check([self.row("Q", 1.00, [RECEIPT])]), [])

    def test_flagged_row_discounted_needs_a_receipt_too(self):
        self.assertTrue(SF.check([self.row("O", 0.00, [])]))

    def test_receipt_must_carry_a_date(self):
        self.assertTrue(SF.check([self.row("Q", 0.50, [{"source": "yahoo", "text": "Q"}])]))

    def test_build_records_the_owners_flagged_players_first(self):
        state = {"as_of": "2026-10-15", "sources": {"pdf": {"file": "p.pdf", "sha256": "ab" * 32}},
                 "teams": [{"seat": 10, "name": "Me", "players": [
                     {"player": "Tyrese Haliburton", "status": None, "slot": "PG"},
                     {"player": "Kevin Durant", "status": "Q", "slot": "SG"}]},
                     {"seat": 1, "name": "Other", "players": [{"player": "Nikola Jokic", "status": "Q", "slot": "C"}]}]}
        rows = SF.build(state, espn=None, espn_attempt={"ok": False, "detail": "denied"})
        self.assertEqual(rows[0]["player"], "Kevin Durant")
        self.assertEqual(rows[0]["availability"], 0.50)
        self.assertEqual(rows[0]["receipts"][0]["captured"], "2026-10-15")
        self.assertEqual(SF.check(rows), [])


class Probable(unittest.TestCase):
    """2026-10-19: Yahoo's P (probable) letter appeared on the owner's rosters paste (Stephen Curry); tiered 0.75 as
    a stated default (D-IS-6), between Q (0.50) and healthy (1.00). An unknown letter still refuses."""
    def test_p_is_tiered_and_unknown_still_refuses(self):
        self.assertEqual(SF.tier("P"), ("probable", 0.75))
        with self.assertRaises(ValueError):
            SF.tier("ZZ")


class NotActive(unittest.TestCase):
    """2026-10-20: Yahoo's NA (not active) letter appeared on the owner's rosters paste (Kevin Porter Jr.); tiered
    0.00 like O, a stated default (D-IS-7). It is a flagged letter, so the dated-receipt check covers it."""
    def test_na_is_tiered_out_and_needs_a_dated_receipt(self):
        self.assertEqual(SF.tier("NA"), ("not active", 0.00))
        self.assertEqual(len(SF.check([{"player": "X", "yahoo_status": "NA", "availability": 0.0, "receipts": []}])), 1)


class FlaimReceipts(unittest.TestCase):
    """Owner 2026-10-21 ("Build A, B, C, D"): when the rosters came from Flaim, every flagged player's receipt names
    the Yahoo read through Flaim and the pinned pull, with its sha256 — not an owner upload that never happened."""
    def test_a_flaim_state_receipts_name_flaim_and_the_pull(self):
        state = {"as_of": "2026-10-21", "sources": {"flaim": {"pull_file": "data/source/flaim/pull_2026-10-21.json",
                                                              "pull_sha256": "cd" * 32}},
                 "teams": [{"name": "MAXEY-MUM OVERDRIVE", "seat": 11, "players": [
                     {"player": "Kevin Porter Jr.", "slot": "PG", "status": "NA"}]}]}
        rows = SF.build(state)
        r = rows[0]["receipts"][0]
        self.assertIn("Flaim", r["source"])
        self.assertEqual((r["file"], r["sha256"], r["captured"]), ("data/source/flaim/pull_2026-10-21.json", "cd" * 32, "2026-10-21"))
        self.assertEqual(rows[0]["availability"], 0.0)
        self.assertEqual(SF.check(rows), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
