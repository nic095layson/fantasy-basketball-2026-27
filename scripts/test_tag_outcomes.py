#!/usr/bin/env python3
"""Red-first tests for scripts/tag_outcomes.py (owner 2026-10-27, build 4, "capture now"): what every player
flagged in a day's status file then did in that day's games — played (minutes against his season norm), sat, or his
team had no game — appended to data/status/tag_outcomes.jsonl, one line per flagged player per day, never rewritten.

    python3 scripts/test_tag_outcomes.py
"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tag_outcomes as TO  # noqa: E402


def status(rows):
    return dict(date="2026-10-25", tiers={}, rows=[dict(player=p, yahoo_status=s, tier=t, availability=a, fantasy_team="T", seat=1)
                                                   for p, s, t, a in rows])


def actuals(players, teams_with_games):
    rows = [dict(pool_name=p, team=t, min=m, dnp=m == 0, game=f"g{t}") for p, t, m in players]
    rows += [dict(pool_name=None, team=t, min=1, dnp=False, game=f"g{t}") for t in teams_with_games]
    return dict(date="2026-10-25", games=[dict(season_type=2)], players=rows)


class Outcomes(unittest.TestCase):
    def test_played_sat_and_no_game_are_told_apart(self):
        st = status([("Q Guy", "Q", "questionable", 0.5), ("O Guy", "O", "out", 0.0), ("Idle Guy", "Q", "questionable", 0.5)])
        ac = actuals([("Q Guy", "BOS", 28), ("O Guy", "LAL", 0)], ["BOS", "LAL"])
        team = {"Q Guy": "BOS", "O Guy": "LAL", "Idle Guy": "MIA"}
        norm = {"Q Guy": 32.0, "O Guy": 30.0, "Idle Guy": 20.0}
        out = {r["player"]: r for r in TO.outcomes(st, ac, team, norm)}
        self.assertEqual(out["Q Guy"]["outcome"], "played"); self.assertEqual(out["Q Guy"]["minutes"], 28)
        self.assertAlmostEqual(out["Q Guy"]["minutes_vs_norm"], 28 / 32.0)
        self.assertEqual(out["O Guy"]["outcome"], "sat")
        self.assertEqual(out["Idle Guy"]["outcome"], "no game")
        self.assertEqual(out["Q Guy"]["yahoo_status"], "Q"); self.assertEqual(out["Q Guy"]["availability"], 0.5)

    def test_a_flagged_player_with_no_known_team_is_recorded_as_unresolved(self):
        st = status([("Ghost", "Q", "questionable", 0.5)])
        out = TO.outcomes(st, actuals([], ["BOS"]), {}, {})
        self.assertEqual(out[0]["outcome"], "unresolved")

    def test_the_ledger_appends_one_line_per_player_per_day_and_refuses_a_repeat_day(self):
        p = os.path.join(tempfile.mkdtemp(), "tag_outcomes.jsonl")
        rows = [dict(date="2026-10-25", player="A", outcome="played"), dict(date="2026-10-25", player="B", outcome="sat")]
        self.assertEqual(TO.append(p, "2026-10-25", rows), 2)
        self.assertEqual(len(open(p).read().strip().splitlines()), 2)
        with self.assertRaises(TO.OutcomeError):
            TO.append(p, "2026-10-25", rows)

    def test_a_day_with_no_flagged_players_appends_nothing_and_is_not_an_error(self):
        p = os.path.join(tempfile.mkdtemp(), "tag_outcomes.jsonl")
        self.assertEqual(TO.append(p, "2026-10-25", []), 0)
        self.assertFalse(os.path.exists(p))


if __name__ == "__main__":
    unittest.main(verbosity=2)
