#!/usr/bin/env python3
"""Red-first tests for scripts/co_gm.py and scripts/daily_brief.py (Session 1 item 6).

    python3 scripts/test_daily_brief.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import co_gm as CG  # noqa: E402
import daily_brief as DB  # noqa: E402


def pl(name, pos, value, avail=1.0):
    return {"player": name, "positions": pos, "value": value, "availability": avail}


class DailyFill(unittest.TestCase):
    def test_every_slot_kind_is_respected(self):
        lineup, bench = CG.daily_lineup([pl("A", ["C"], 9), pl("B", ["C"], 8), pl("D", ["C"], 7), pl("E", ["PG"], 6)])
        slots = {s: p for s, p in lineup}
        self.assertEqual(slots.get("PG"), "E")
        self.assertEqual(sorted(p for s, p in lineup if s in ("C", "Util")), ["A", "B", "D"])
        self.assertEqual(bench, [])

    def test_a_flex_player_moves_aside_so_a_lower_valued_specialist_still_starts(self):
        # slot-order greedy puts the PG,SG star at PG; the four pure PGs then fill G, Util, Util and
        # one sits. The star belongs at SG so all five start.
        roster = [pl("Star", ["PG", "SG"], 10)] + [pl(f"PG{i}", ["PG"], 5 - i) for i in range(4)]
        lineup, bench = CG.daily_lineup(roster)
        self.assertEqual(len(lineup), 5)
        self.assertEqual(bench, [])

    def test_out_players_never_start_and_eleventh_player_sits(self):
        roster = [pl(f"U{i}", ["SF"], 20 - i) for i in range(11)] + [pl("Hurt", ["C"], 99, avail=0.0)]
        lineup, bench = CG.daily_lineup(roster)
        names = [p for _, p in lineup]
        self.assertNotIn("Hurt", names)
        self.assertEqual(len(lineup), 4)  # SF, F, Util, Util are the only slots an SF can take
        self.assertEqual(len(bench), 7)


class Schedule(unittest.TestCase):
    def test_bref_codes_map_to_pool_codes(self):
        self.assertEqual(CG.TEAM_CODE.get("CHO"), "CHA")
        self.assertEqual(CG.TEAM_CODE.get("BRK"), "BKN")
        self.assertEqual(CG.TEAM_CODE.get("PHO"), "PHX")

    def test_games_left_counts_from_the_date_to_the_week_end(self):
        games = [("2026-10-20", "BOS", "DET"), ("2026-10-21", "PHO", "POR"), ("2026-10-23", "POR", "LAL"),
                 ("2026-10-26", "POR", "UTA")]
        left = CG.games_left(games, "2026-10-21", "2026-10-25")
        self.assertEqual(left["POR"], 2)
        self.assertEqual(left["PHX"], 1)
        self.assertEqual(left.get("BOS", 0), 0)


class Streaming(unittest.TestCase):
    def test_ranks_by_value_among_players_with_more_games_than_the_drop(self):
        # 2026-10-15 first run: every candidate's per-game value was negative and the sort clamped
        # them all to zero, so the list came out in arbitrary order
        fa = [{"player": "A", "team": "X", "games_left": 3, "value_per_game": -2.3},
              {"player": "B", "team": "Y", "games_left": 3, "value_per_game": -1.1},
              {"player": "C", "team": "Z", "games_left": 2, "value_per_game": 5.0}]
        out = CG.streaming(fa, drop_games=2)
        self.assertEqual([r["player"] for r in out], ["B", "A"])


class Note(unittest.TestCase):
    def test_odds_line_carries_both_seeds_and_the_error(self):
        line = DB.odds_line(21.81, 21.60, 10000)
        self.assertIn("21.81", line)
        self.assertIn("21.60", line)
        self.assertIn("±", line)


class SeasonPool(unittest.TestCase):
    """In-season tool: SEASON_POOL (a deck-schema CSV path) overrides the preseason v69 pool for the brief, the
    preview and the waiver scan; unset, the preseason pool loads as before."""
    def test_env_override_points_the_pool_at_the_season_file(self):
        import importlib
        season = os.path.join(CG.KIT, "data", "season", "pool_season.csv")
        if not os.path.exists(season):
            self.skipTest("no season pool written")
        os.environ["SEASON_POOL"] = season
        try:
            CG.load_pool()
            self.assertEqual(os.path.abspath(CG.hoops.DATA_PATH), os.path.abspath(season))
        finally:
            del os.environ["SEASON_POOL"]
        CG.load_pool()
        self.assertTrue(CG.hoops.DATA_PATH.endswith(f"players_{CG.LINES_TAG}.csv"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
