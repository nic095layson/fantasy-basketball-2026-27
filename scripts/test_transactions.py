#!/usr/bin/env python3
"""Red-first tests for scripts/transactions.py (owner 2026-10-20: Kevin Porter Jr. waived by Milwaukee on 10/19;
the morning run reads ESPN's transactions feed and lists every move that names a pool player).

    python3 scripts/test_transactions.py
"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import transactions as TX  # noqa: E402

ITEMS = [
    {"date": "2026-10-19T07:00Z", "team": {"abbreviation": "MIL"}, "description": "Waived G Kevin Porter Jr."},
    {"date": "2026-10-19T07:00Z", "team": {"abbreviation": "LAL"}, "description": "Waived F Dalton Knecht."},
    {"date": "2026-10-17T07:00Z", "team": {"abbreviation": "NY"}, "description": "Waived Gs Bruce Brown and Dink Pate."},
    {"date": "2026-10-12T07:00Z", "team": {"abbreviation": "POR"}, "description": "Waived G Jalen Williamson."},
]
OWNERS = {"Kevin Porter Jr.": {"team": "KEVIN ELEVEN DOUBLES", "seat": 11}}


class Match(unittest.TestCase):
    def test_a_rostered_waiver_is_listed_with_its_fantasy_team(self):
        hits = TX.match(ITEMS, "2026-10-18", "2026-10-20", ["Kevin Porter Jr.", "Dalton Knecht", "Jalen Williams"], OWNERS)
        self.assertEqual([h["player"] for h in hits], ["Kevin Porter Jr.", "Dalton Knecht"])
        self.assertEqual(hits[0]["fantasy_team"], "KEVIN ELEVEN DOUBLES"); self.assertEqual(hits[0]["seat"], 11)
        self.assertIsNone(hits[1]["fantasy_team"])

    def test_the_window_bounds_and_whole_words(self):
        # Bruce Brown (10/17) is outside a 10/18-10/20 window; "Jalen Williams" must not match "Jalen Williamson"
        hits = TX.match(ITEMS, "2026-10-10", "2026-10-20", ["Bruce Brown", "Jalen Williams"], {})
        self.assertEqual([h["player"] for h in hits], ["Bruce Brown"])
        self.assertEqual(TX.match(ITEMS, "2026-10-18", "2026-10-20", ["Bruce Brown"], {}), [])

    def test_window_is_inclusive_days_ending_on_the_date(self):
        self.assertEqual(TX.window("2026-10-20", 3), ("2026-10-18", "2026-10-20"))


class Feed(unittest.TestCase):
    def test_pages_until_the_window_start_and_an_outage_is_recorded_not_raised(self):
        pages = {1: ITEMS[:2], 2: ITEMS[2:], 3: []}
        calls = []

        def fake(url):
            calls.append(url); n = int(url.rsplit("=", 1)[1])
            return json.dumps({"transactions": pages[n]}), 200, "live"
        items, at = TX.fetch_feed("2026-10-18", fetch=fake)
        self.assertTrue(at["ok"]); self.assertEqual(len(calls), 2); self.assertEqual(len(items), 4)
        items, at = TX.fetch_feed("2026-10-18", fetch=lambda url: (None, 0, "timed out (3 attempts)"))
        self.assertFalse(at["ok"]); self.assertEqual(items, []); self.assertIn("timed out", at["detail"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
