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


if __name__ == "__main__":
    unittest.main()
