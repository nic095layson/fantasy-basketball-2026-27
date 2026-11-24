"""Owner 2026-11-24 ("Fix the simulator first"): the league simulator plays whatever roster it is handed, and the title
share moves about 12 points per extra active player; a hand-built trade arm with 14 (or 11) active players read as a
huge gain (or loss). run_league_sim(active_limit=N) refuses a roster with more than N players active in any week."""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import co_gm as CG


def P(name):
    return {"player": name}


class ActiveLimit(unittest.TestCase):
    def test_the_limit_is_the_leagues_non_il_slots(self):
        self.assertEqual(CG.active_limit(), 13)    # PG, SG, G, SF, PF, F, C, C, Util, Util, BN, BN, BN (+ IL, IL)

    def test_thirteen_pass_and_fourteen_are_named_by_seat_and_week(self):
        ros = {10: [P(f"p{i}") for i in range(13)], 1: [P(f"q{i}") for i in range(13)]}
        self.assertEqual(CG.over_active_limit(ros, None, 17, 13), [])
        ros[10].append(P("extra"))
        bad = CG.over_active_limit(ros, None, 17, 13)
        self.assertEqual(bad[0], dict(seat=10, week=1, active=14)); self.assertEqual(len(bad), 17)

    def test_a_player_outside_his_window_does_not_count(self):
        ros = {10: [P(f"p{i}") for i in range(12)] + [P("returns"), P("leaves")]}
        win = {10: {"returns": (7, 17), "leaves": (1, 6)}}
        self.assertEqual(CG.over_active_limit(ros, win, 17, 13), [])   # 12 + one of the two in every week
        win[10]["returns"] = (6, 17)                                      # week 6: both
        self.assertEqual(CG.over_active_limit(ros, win, 17, 13), [dict(seat=10, week=6, active=14)])

    def test_run_league_sim_refuses_before_simulating_and_is_unchanged_without_the_limit(self):
        ros = {10: [P(f"p{i}") for i in range(14)]}
        called = []
        real = CG.subprocess.run, CG.sim_pool_names, CG.pool_guard
        try:
            CG.subprocess.run = lambda *a, **k: called.append(1) or (_ for _ in ()).throw(RuntimeError("simulated"))
            CG.sim_pool_names = lambda pool=None: {p["player"] for r in ros.values() for p in r}
            CG.pool_guard = lambda: None
            with self.assertRaises(CG.RosterLimitError) as e:
                CG.run_league_sim(ros, 2026, 10, "/tmp", active_limit=13)
            self.assertIn("seat 10", str(e.exception)); self.assertEqual(called, [])
            with self.assertRaises(RuntimeError):                          # no limit: straight to the simulator, as before
                CG.run_league_sim(ros, 2026, 10, "/tmp")
            self.assertEqual(called, [1])
        finally:
            CG.subprocess.run, CG.sim_pool_names, CG.pool_guard = real


if __name__ == "__main__":
    unittest.main()
