#!/usr/bin/env python3
"""Known-answer cases for the GP reconstruction (written before the first scored run).
    python3 test_reconstruct.py [RAW_DIR]   (RAW_DIR adds the parser-agreement case against a page #159 parsed)"""
import csv, datetime as dt, os, sys, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import reconstruct as R  # noqa: E402
from extract_rosters import week_start  # noqa: E402
RAW = sys.argv.pop(1) if len(sys.argv) > 1 else None
ALL = {"PG", "SG", "SF", "PF", "C"}


class Seat(unittest.TestCase):
    def test_eleven_players_fill_ten_slots(self):
        self.assertEqual(R.seat([ALL] * 11), 10)

    def test_centers_take_c_c_util_util(self):
        self.assertEqual(R.seat([{"C"}] * 3), 3)
        self.assertEqual(R.seat([{"C"}] * 4), 4)
        self.assertEqual(R.seat([{"C"}] * 5), 4)

    def test_point_guard_cannot_take_a_c_slot(self):
        self.assertEqual(R.seat([{"PG"}] * 5), 4)  # PG, G, Util, Util

    def test_rearranges_where_greedy_would_not(self):
        # first-come would put the dual-eligible man at PG and leave the PG-only man out
        self.assertEqual(R.seat([{"PG", "SG"}, {"PG"}], slots=["PG", "SG"]), 2)

    def test_nobody_played(self):
        self.assertEqual(R.seat([]), 0)


class Weeks(unittest.TestCase):
    def test_year_turn_and_two_week_span(self):
        self.assertEqual((week_start("12/29-1/4"), R.week_end("12/29-1/4")), (dt.date(2025, 12, 29), dt.date(2026, 1, 4)))
        self.assertEqual((R.week_end("2/9-2/22") - week_start("2/9-2/22")).days + 1, 14)

    def test_il_players_count_nothing_and_bench_counts(self):
        roster = {"players": [dict(name="A", position="C", selectedPosition="BN"),
                              dict(name="B", position="C", selectedPosition="IL+")]}
        days = {"a": {"2025-11-03"}, "b": {"2025-11-03"}}
        tw = R.team_week(roster, dt.date(2025, 11, 3), dt.date(2025, 11, 9), {"A": "a", "B": "b"}, days)
        self.assertEqual((tw["gp"], tw["il"], tw["active"]), (1, 1, 1))


@unittest.skipUnless(RAW, "needs RAW_DIR")
class Parser(unittest.TestCase):
    def test_carried_parser_agrees_with_159(self):
        import pull_logs as P
        rows = [r for r in csv.DictReader(open(R.PRIOR, encoding="utf-8")) if r["bref_id"] == "jokicni01"]
        mine = P.parse(open(os.path.join(RAW, "jokicni01.html"), encoding="utf-8", errors="replace").read())
        self.assertEqual([{k: r[k] for k in P.COLS} for r in rows], mine)


if __name__ == "__main__":
    unittest.main(verbosity=2)
