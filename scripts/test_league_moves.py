#!/usr/bin/env python3
"""Red-first tests for league_moves.py: the adds/drops/IL diff between two league states."""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import league_moves  # noqa: E402


def state(as_of, teams):
    """teams: {name: {seat, players: [(player, slot)]}}"""
    return {"as_of": as_of, "teams": [
        {"name": n, "seat": t["seat"],
         "players": [{"player": p, "slot": s} for p, s in t["players"]],
         "unpooled_il": t.get("unpooled_il", [])}
        for n, t in teams.items()]}


class Diff(unittest.TestCase):
    def test_adds_drops_and_il_moves_are_named_per_team(self):
        old = state("2026-10-19", {"T": {"seat": 1, "players": [("A", "BN"), ("B", "PG"), ("C", "BN")]}})
        new = state("2026-10-20", {"T": {"seat": 1, "players": [("B", "PG"), ("C", "IL"), ("D", "BN")]}})
        moves = league_moves.diff(old, new)
        self.assertEqual(len(moves), 1)
        m = moves[0]
        self.assertEqual(m["team"], "T")
        self.assertEqual(m["added"], ["D"])
        self.assertEqual(m["dropped"], ["A"])
        self.assertEqual(m["to_il"], ["C"])
        self.assertEqual(m["from_il"], [])

    def test_a_team_with_no_change_is_not_listed(self):
        old = state("2026-10-19", {"T": {"seat": 1, "players": [("A", "BN")]}})
        new = state("2026-10-20", {"T": {"seat": 1, "players": [("A", "BN")]}})
        self.assertEqual(league_moves.diff(old, new), [])

    def test_teams_match_by_seat_so_a_rename_is_not_a_roster_move(self):
        old = state("2026-10-19", {"DEVIN": {"seat": 2, "players": [("A", "BN")]}})
        new = state("2026-10-20", {"KEVIN": {"seat": 2, "players": [("A", "BN")]}})
        self.assertEqual(league_moves.diff(old, new), [])

    def test_unpooled_il_counts_as_rostered(self):
        old = state("2026-10-19", {"T": {"seat": 1, "players": [], "unpooled_il": ["U. Man"]}})
        new = state("2026-10-20", {"T": {"seat": 1, "players": [], "unpooled_il": ["U. Man"]}})
        self.assertEqual(league_moves.diff(old, new), [])



class Phase(unittest.TestCase):
    """Owner 2026-10-26, option 1A: the afternoon run writes its own record and never touches the morning's."""
    def test_pm_path_is_suffixed_and_am_is_not(self):
        self.assertTrue(league_moves.record_path("2026-10-26", "am").endswith(os.path.join("data", "news", "league_moves_2026-10-26.json")))
        self.assertTrue(league_moves.record_path("2026-10-26", "pm").endswith(os.path.join("data", "news", "league_moves_2026-10-26_pm.json")))

    def test_write_record_takes_a_phase_and_records_it(self):
        import json, tempfile
        d = tempfile.mkdtemp()
        old = {"as_of": "2026-10-25", "teams": []}; new = {"as_of": "2026-10-26", "teams": []}
        rec, out = league_moves.write_record(old, new, "2026-10-26", out=os.path.join(d, "x.json"), phase="pm")
        self.assertEqual(rec["phase"], "pm")
        self.assertEqual(json.load(open(out))["phase"], "pm")
        rec2, _ = league_moves.write_record(old, new, "2026-10-26", out=os.path.join(d, "y.json"))
        self.assertEqual(rec2["phase"], "am")       # the default never changes today's behaviour

if __name__ == "__main__":
    unittest.main()
