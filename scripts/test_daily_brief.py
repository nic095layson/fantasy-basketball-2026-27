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


class Band(unittest.TestCase):
    """Post-mortem D-PM-6 / D-RT-2: every title figure carries the structural band from the standing sweep."""
    def test_band_line_names_the_fragile_constant_and_its_figures(self):
        line = DB.band_line()
        self.assertIn("TEAM_WEEK_SHOCK", line); self.assertIn("FRAGILE", line)
        self.assertRegex(line, r"[+-]\d\.\d")


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


class StatusFile(unittest.TestCase):
    """2026-10-20: a status file dated after the brief (a test run of tomorrow's morning) shadowed the day's own
    file, so the brief read yesterday's rosters' letters. The brief reads the newest file dated on or before it."""
    def test_a_later_dated_file_does_not_shadow_the_brief_date(self):
        import json, tempfile
        d = tempfile.mkdtemp()
        os.makedirs(os.path.join(d, "data", "status"))
        for day in ("2026-10-19", "2026-10-20", "2026-10-21"):
            json.dump({"rows": [{"player": day}]}, open(os.path.join(d, "data", "status", f"status_{day}.json"), "w"))
        kit, CG.KIT = CG.KIT, d
        try:
            st, name = DB.newest_status("2026-10-20")
            self.assertEqual(name, "status_2026-10-20.json"); self.assertEqual(st["rows"][0]["player"], "2026-10-20")
            self.assertEqual(DB.newest_status("2026-10-25")[1], "status_2026-10-21.json")
            self.assertIsNone(DB.newest_status("2026-10-18")[1])
        finally:
            CG.KIT = kit


class Transactions(unittest.TestCase):
    """2026-10-20 (owner): Kevin Porter Jr. waived by MIL on 10/19 reaches the brief; yours first, then the opponent."""
    REC = {"window": ["2026-10-18", "2026-10-20"], "items_in_window": 9, "source": {"ok": True}, "hits": [
        {"date": "2026-10-19", "nba_team": "LAL", "description": "Waived F Dalton Knecht.", "player": "Dalton Knecht", "fantasy_team": None, "seat": None},
        {"date": "2026-10-19", "nba_team": "MIL", "description": "Waived G Kevin Porter Jr.", "player": "Kevin Porter Jr.", "fantasy_team": "THEM", "seat": 11},
        {"date": "2026-10-18", "nba_team": "SAS", "description": "Signed F Tobias Harris.", "player": "Tobias Harris", "fantasy_team": "ME", "seat": 10}]}

    def test_order_and_labels(self):
        L = DB.transactions_lines(self.REC, "ME", "THEM")
        self.assertIn("9 moves, 3 naming a board player", L[0])
        self.assertTrue(L[1].startswith("- **Tobias Harris** (yours)"))
        self.assertIn("THEM, your opponent this week", L[2]); self.assertIn("Waived G Kevin Porter Jr.", L[2])
        self.assertIn("on no roster", L[3])

    def test_unread_feed_and_missing_record_say_so(self):
        self.assertIn("NOT read", DB.transactions_lines({**self.REC, "source": {"ok": False, "detail": "timed out"}}, "ME", "THEM")[0])
        self.assertIn("Not read", DB.transactions_lines(None, "ME", "THEM")[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
