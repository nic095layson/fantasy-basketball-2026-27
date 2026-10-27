#!/usr/bin/env python3
"""Red-first tests for weekly_preview.py's league-wide record (owner 2026-10-27, the weekly accuracy card): every
matchup's pre-week forecast, recorded before the week starts, append-only; a repeat is reported, not an error, so
the Sunday morning step can run every week whether or not a session already recorded the owner's matchup.

    python3 scripts/test_weekly_preview.py
"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import weekly_preview as WP  # noqa: E402

PAIRS = [dict(a=1, b=2, p_win=0.6, exp_cats=5.0), dict(a=3, b=4, p_win=0.4, exp_cats=4.0)]


class LeagueRecord(unittest.TestCase):
    def setUp(self):
        self.p = os.path.join(tempfile.mkdtemp(), "calibration_league.json")

    def test_recorded_before_the_week(self):
        self.assertTrue(WP.record_league(self.p, 3, PAIRS, "2026-11-01T12:00:00Z", "2026-11-02"))
        w = json.load(open(self.p))["weeks"]["3"]
        self.assertEqual(w["pairs"], PAIRS); self.assertEqual(w["recorded_at"], "2026-11-01T12:00:00Z")

    def test_too_late_is_an_error(self):
        with self.assertRaises(WP.LedgerError):
            WP.record_league(self.p, 3, PAIRS, "2026-11-02T12:00:00Z", "2026-11-02")

    def test_a_repeat_is_reported_and_nothing_is_rewritten(self):
        WP.record_league(self.p, 3, PAIRS, "2026-11-01T12:00:00Z", "2026-11-02")
        self.assertFalse(WP.record_league(self.p, 3, [dict(PAIRS[0], p_win=0.99)], "2026-11-01T13:00:00Z", "2026-11-02"))
        self.assertEqual(json.load(open(self.p))["weeks"]["3"]["pairs"][0]["p_win"], 0.6)

    def test_the_owner_record_reports_a_repeat_when_asked(self):
        p = os.path.join(tempfile.mkdtemp(), "calibration.json")
        pred = dict(week=3, p_win=0.5)
        WP.record(p, pred, "2026-11-01T12:00:00Z", "2026-11-02")
        self.assertIsNone(WP.record(p, pred, "2026-11-01T13:00:00Z", "2026-11-02", if_absent=True))


class RealGamesLedger(unittest.TestCase):
    """Owner 2026-10-27 (build 5, first slice): the league forecast on each NBA team's real games is recorded in its
    own append-only ledger beside the flat one, by the same rules."""
    def test_the_real_games_ledger_is_a_separate_file_with_the_same_rules(self):
        d = tempfile.mkdtemp(); flat = os.path.join(d, "calibration_league.json"); real = os.path.join(d, "calibration_league_real.json")
        self.assertTrue(WP.record_league(flat, 3, PAIRS, "2026-11-01T12:00:00Z", "2026-11-02"))
        self.assertTrue(WP.record_league(real, 3, [dict(PAIRS[0], p_win=0.65)], "2026-11-01T12:00:00Z", "2026-11-02", method="real games"))
        self.assertEqual(json.load(open(real))["weeks"]["3"]["pairs"][0]["p_win"], 0.65)
        self.assertEqual(json.load(open(real))["weeks"]["3"]["method"], "real games")
        self.assertEqual(json.load(open(flat))["weeks"]["3"]["pairs"][0]["p_win"], 0.6)
        self.assertTrue(WP.LEAGUE_REAL.endswith("calibration_league_real.json"))

    def test_preview_league_takes_a_real_games_switch(self):
        import inspect
        self.assertIn("real_games", inspect.signature(WP.preview_league).parameters)

class Snapshot(unittest.TestCase):
    """Owner 2026-10-27 (build 2): the Sunday snapshot copies the live pool and, beside it, the minutes-trend
    candidate pool when it exists; neither is ever overwritten."""
    def setUp(self):
        self.src = tempfile.mkdtemp(); self.dst = tempfile.mkdtemp()
        open(os.path.join(self.src, "pool_season.csv"), "w").write("player,pts\nA,10.0\n")

    def test_live_and_candidate_are_both_snapshotted(self):
        open(os.path.join(self.src, "pool_season_mt.csv"), "w").write("player,pts\nA,11.0\n")
        out = WP.snapshot(3, os.path.join(self.src, "pool_season.csv"), self.dst)
        self.assertEqual(sorted(os.path.basename(x) for x in out), ["lines_week3.csv", "lines_week3_mt.csv"])
        self.assertEqual(open(os.path.join(self.dst, "lines_week3_mt.csv")).read(), "player,pts\nA,11.0\n")

    def test_the_league_state_and_the_days_status_file_are_snapshotted_too(self):
        # owner 2026-10-27 (build 3): the Monday fit models each week on the rosters and tags true before it
        st = os.path.join(self.src, "league_state.json"); open(st, "w").write('{"as_of": "2026-11-01", "teams": []}')
        sd = os.path.join(self.src, "status"); os.makedirs(sd); open(os.path.join(sd, "status_2026-11-01.json"), "w").write("{}")
        out = WP.snapshot(3, os.path.join(self.src, "pool_season.csv"), self.dst, state=st, status=os.path.join(sd, "status_2026-11-01.json"))
        self.assertEqual(sorted(os.path.basename(x) for x in out), ["lines_week3.csv", "state_week3.json", "status_week3.json"])
        self.assertEqual(open(os.path.join(self.dst, "state_week3.json")).read(), '{"as_of": "2026-11-01", "teams": []}')

    def test_a_missing_state_or_status_file_is_skipped_not_fatal(self):
        out = WP.snapshot(3, os.path.join(self.src, "pool_season.csv"), self.dst, state=os.path.join(self.src, "nope.json"), status=None)
        self.assertEqual([os.path.basename(x) for x in out], ["lines_week3.csv"])

    def test_no_candidate_file_snapshots_the_live_pool_alone(self):
        out = WP.snapshot(3, os.path.join(self.src, "pool_season.csv"), self.dst)
        self.assertEqual([os.path.basename(x) for x in out], ["lines_week3.csv"])

    def test_an_existing_snapshot_is_not_overwritten(self):
        WP.snapshot(3, os.path.join(self.src, "pool_season.csv"), self.dst)
        open(os.path.join(self.src, "pool_season.csv"), "w").write("player,pts\nA,99.0\n")
        self.assertEqual(WP.snapshot(3, os.path.join(self.src, "pool_season.csv"), self.dst), [])
        self.assertEqual(open(os.path.join(self.dst, "lines_week3.csv")).read(), "player,pts\nA,10.0\n")

class LinesLabel(unittest.TestCase):
    """Owner 2026-10-27 ("Relabel future rows"): a new ledger row names the lines it ran on, by the brief's rule:
    the season pool when SEASON_POOL is set (the Sunday step sets it), else the frozen tag. Rows already written
    are never rewritten."""
    def _preview(self, pool):
        old = os.environ.pop("SEASON_POOL", None)
        if pool:
            os.environ["SEASON_POOL"] = pool
        try:
            return WP.preview(3, n=20)
        finally:
            os.environ.pop("SEASON_POOL", None)
            if old is not None:
                os.environ["SEASON_POOL"] = old

    def test_on_the_season_pool_the_row_says_so(self):
        pool = os.path.join(os.path.dirname(HERE), "data", "season", "pool_season.csv")
        self.assertEqual(self._preview(pool)["lines"], "season pool")

    def test_without_it_the_row_keeps_the_frozen_tag(self):
        self.assertEqual(self._preview(None)["lines"], WP.CG.LINES_TAG)


if __name__ == "__main__":
    unittest.main(verbosity=2)
