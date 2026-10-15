#!/usr/bin/env python3
"""Red-first tests for scripts/league_intake.py (Session 1 item 5).

The intake must resolve every rostered name to the pool or halt without writing:
a league state with one unresolved player would silently drop that player from every
lineup, waiver scan and simulation downstream.

    python3 scripts/test_league_intake.py
"""
import csv
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import league_intake as LI  # noqa: E402

HEAD = ["fantasy_team", "page", "slot", "player", "nba_team", "positions", "status"]
POOL = [{"player": "Tyrese Haliburton", "team": "IND"}, {"player": "Nickeil Alexander-Walker", "team": "ATL"},
        {"player": "Nikola Jokic", "team": "DEN"}]
ABBR = {"N. Alexander-Walker": "Nickeil Alexander-Walker"}


def write(rows, d):
    p = os.path.join(d, "t.csv")
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEAD)
        w.writerows(rows)
    return p


class Resolve(unittest.TestCase):
    def test_exact_accent_and_abbreviation(self):
        res, miss = LI.resolve(["Tyrese Haliburton", "Nikola Jokić", "N. Alexander-Walker"], POOL, ABBR)
        self.assertEqual(miss, [])
        self.assertEqual(res["Nikola Jokić"], "Nikola Jokic")
        self.assertEqual(res["N. Alexander-Walker"], "Nickeil Alexander-Walker")

    def test_unknown_name_is_a_miss_not_a_guess(self):
        res, miss = LI.resolve(["Y. Konan Niederhäuser", "T. Haliburton"], POOL, ABBR)
        self.assertEqual(miss, ["Y. Konan Niederhäuser", "T. Haliburton"])


class Intake(unittest.TestCase):
    def test_halts_and_writes_nothing_on_a_miss(self):
        with tempfile.TemporaryDirectory() as d:
            src = write([["A", 1, "PG", "Tyrese Haliburton", "IND", "PG", ""],
                         ["A", 1, "IL", "Nobody Atall", "LAC", "C", "O"]], d)
            out = os.path.join(d, "state.json")
            rc = LI.run(src, out, POOL, ABBR, draft={}, as_of="2026-10-15")
            self.assertEqual(rc, 1)
            self.assertFalse(os.path.exists(out))

    def test_writes_dated_state_when_all_resolve(self):
        with tempfile.TemporaryDirectory() as d:
            src = write([["A", 1, "PG", "Tyrese Haliburton", "IND", "PG", ""],
                         ["A", 1, "C", "(Empty)", "", "", ""]], d)
            out = os.path.join(d, "state.json")
            rc = LI.run(src, out, POOL, ABBR, draft={10: ["Tyrese Haliburton"]}, as_of="2026-10-15")
            self.assertEqual(rc, 0)
            st = json.load(open(out))
            self.assertEqual(st["as_of"], "2026-10-15")
            team = st["teams"][0]
            self.assertEqual(team["seat"], 10)
            self.assertEqual([p["player"] for p in team["players"]], ["Tyrese Haliburton"])
            self.assertEqual(team["empty_slots"], ["C"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
