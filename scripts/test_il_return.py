#!/usr/bin/env python3
"""Red-first tests for scripts/il_return.py (owner 2026-10-31: ESPN's injury return as a variable in a separate title-odds
section; the headline keeps D-IS-8). The headline path must stay byte-identical: sim_state without windows is the
state it always was; the brief draws the section only from a record on disk and simulates nothing for it.

    python3 scripts/test_il_return.py
"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import co_gm as CG  # noqa: E402
import daily_brief as DB  # noqa: E402
import il_return as IR  # noqa: E402

WEEKS = 17


def week_of(date):
    """A toy calendar: week 1 = 2026-10-19..25, then 7-day weeks."""
    import datetime as dt
    d = dt.date.fromisoformat(date); n = (d - dt.date(2026, 10, 19)).days // 7 + 1
    if n < 1 or n > 20:
        raise ValueError(date)
    return n, None, None


class Dates(unittest.TestCase):
    def test_return_date_maps_to_its_week_and_the_edges_are_never(self):
        rw = lambda d: IR.return_week(d, "2026-10-31", WEEKS, week_of)
        self.assertEqual(rw("2026-11-13"), 4)
        self.assertEqual(rw("2026-10-20"), 2)           # before the run's date: the run's week
        self.assertEqual(rw("2026-10-31"), 2)           # today
        self.assertIsNone(rw(None)); self.assertIsNone(rw("")); self.assertIsNone(rw("TBD"))
        self.assertIsNone(rw("2027-03-01"))             # past the regular season
        self.assertIsNone(rw("2027-06-01"))             # outside the calendar

    def test_il_players_come_from_the_state_with_espn_rows_matched_by_name(self):
        state = {"teams": [{"seat": 10, "name": "Me", "players": [{"player": "Tyrese Haliburton", "slot": "IL"}, {"player": "A", "slot": "PG"}]},
                           {"seat": 2, "name": "T2", "players": [{"player": "Naji Marshall", "slot": "IL"}, {"player": "Cameron Johnson", "slot": "IL"}]}]}
        rows = [{"player": "Tyrese Haliburton", "status": "Out", "return_date": "2026-11-13"},
                {"player": "Cam Johnson", "status": "Day-To-Day", "return_date": "2026-10-31"}]
        with __import__("unittest.mock").mock.patch.object(IR.CG, "week_of", week_of):
            il = IR.il_players(state, rows, "2026-10-31", WEEKS, aliases={"Cam Johnson": ["Cameron Johnson"]})
        got = {x["player"]: (x["espn"], x["week"]) for x in il}
        self.assertEqual(got, {"Tyrese Haliburton": ("Tyrese Haliburton", 4), "Naji Marshall": (None, None), "Cameron Johnson": ("Cam Johnson", 2)})
        self.assertNotIn("A", got)

    def test_an_unpooled_il_slot_player_the_pool_has_a_row_for_is_an_il_player(self):
        # owner pick 2026-11-12 (the A-10 re-run): off this list he played every week in every return world
        state = {"teams": [{"seat": 5, "name": "T5", "players": [{"player": "Jalen Suggs", "slot": "IL"}, {"player": "A", "slot": "PG"}],
                            "unpooled": [{"player": "Nolan Traore", "slot": "IL"}, {"player": "Bench Rookie", "slot": "BN"},
                                         {"player": "No Row", "slot": "IL"}]}]}
        rows = [{"player": "Nolan Traore", "status": "Out", "return_date": "2026-11-13"}]
        with __import__("unittest.mock").mock.patch.object(IR.CG, "week_of", week_of):
            il = IR.il_players(state, rows, "2026-10-31", WEEKS, aliases={}, by={"Nolan Traore": {}, "Bench Rookie": {}, "Jalen Suggs": {}})
            old = IR.il_players(state, rows, "2026-10-31", WEEKS, aliases={})
        self.assertEqual({x["player"]: x["week"] for x in il}, {"Jalen Suggs": None, "Nolan Traore": 4})
        self.assertEqual([x["player"] for x in old], ["Jalen Suggs"])     # without the pool, the list as before


class Windows(unittest.TestCase):
    def setUp(self):
        self.il = [dict(seat=10, team="Me", player="Hali", week=4), dict(seat=10, team="Me", player="Kawhi", week=6),
                   dict(seat=2, team="T2", player="Naji", week=None), dict(seat=2, team="T2", player="Nurk", week=3)]
        mk = lambda n, v: {"player": n, "v": v}
        self.ros = {10: [mk("Hali", 9), mk("Kawhi", 9), mk("A", 3), mk("B", 1), mk("C", 2)], 2: [mk("Naji", 2), mk("Nurk", 5), mk("X", 1), mk("Y", 4)]}
        self.value = lambda p: p["v"]

    def test_on_time_returns_open_at_the_week_and_the_weakest_active_leaves(self):
        w = IR.windows_for(self.il, 0, self.ros, WEEKS, room=True, value=self.value)
        self.assertEqual(w[10], {"Hali": (4, WEEKS), "B": (1, 3), "Kawhi": (6, WEEKS), "C": (1, 5)})
        self.assertEqual(w[2], {"Nurk": (3, WEEKS), "X": (1, 2), "Naji": (WEEKS + 1, WEEKS)})

    def test_a_slip_past_the_season_is_never_and_frees_no_room(self):
        w = IR.windows_for(self.il, 12, self.ros, WEEKS, room=True, value=self.value)
        self.assertEqual(w[10], {"Hali": (16, WEEKS), "B": (1, 15), "Kawhi": (WEEKS + 1, WEEKS)})

    def test_room_off_removes_nobody_and_seats_only_keeps_other_teams_absent(self):
        w = IR.windows_for(self.il, 0, self.ros, WEEKS, room=False, value=self.value)
        self.assertEqual(w[10], {"Hali": (4, WEEKS), "Kawhi": (6, WEEKS)})
        w = IR.windows_for(self.il, 0, self.ros, WEEKS, room=True, seats=[10], value=self.value)
        self.assertEqual(w[2], {"Naji": (WEEKS + 1, WEEKS), "Nurk": (WEEKS + 1, WEEKS)})
        self.assertEqual(w[10]["Hali"], (4, WEEKS))


class Headline(unittest.TestCase):
    def test_sim_state_without_windows_is_the_state_it_always_was(self):
        ros = {1: [{"player": "A"}, {"player": "B"}], 10: [{"player": "C"}]}
        self.assertEqual(CG.sim_state(ros), {"teams": 2, "picks": [{"slot": 1, "player": "A"}, {"slot": 1, "player": "B"}, {"slot": 10, "player": "C"}]})
        self.assertEqual(json.dumps(CG.sim_state(ros)), json.dumps(CG.sim_state(ros, None)))
        st = CG.sim_state(ros, {10: {"C": (4, 17)}})
        self.assertEqual(st["picks"][2], {"slot": 10, "player": "C", "from_week": 4, "to_week": 17})
        self.assertEqual(st["picks"][0], {"slot": 1, "player": "A"})

    def test_the_brief_reads_the_section_from_a_record_only(self):
        d = tempfile.mkdtemp()
        self.assertIsNone(DB.il_return_for("2026-10-31", d))
        rec = dict(espn_date="2026-10-31", n_il=22, room_rule="r", error=0.7, seasons=10000, label="l", lines=["x"],
                   scenarios={k: dict(title=t, playoffs=90.0) for k, t in (("never", 15.0), ("on_time", 25.0), ("late_2", 22.0), ("late_4", 20.0))})
        json.dump(rec, open(os.path.join(d, "il_return_2026-10-31.json"), "w"))
        self.assertEqual(DB.il_return_for("2026-10-31", d)["n_il"], 22)
        open(os.path.join(d, "il_return_2026-11-01.json"), "w").write("{broken")
        self.assertIsNone(DB.il_return_for("2026-11-01", d))

    def test_the_section_lines_name_every_il_player_seat_10_first(self):
        rec = dict(espn_date="2026-10-31", n_il=3, room_rule="r", error=0.7, seasons=10000,
                   scenarios={k: dict(title=t) for k, t in (("never", 15.0), ("on_time", 25.0), ("late_2", 22.0), ("late_4", 20.0))},
                   il_players=[dict(seat=2, team="T2", player="Naji", return_date=None, week=None), dict(seat=10, team="Me", player="Hali", return_date="2026-11-13", week=4)])
        rec["scenarios"]["on_time_rule_flipped"] = dict(title=38.4)
        L = IR.lines(rec)
        self.assertIn("if they return ≈22% (20.0 to 25.0 across on time / +2 wk / +4 wk) · never = headline 15.0%", L[0])
        self.assertIn("ROOM_RULE_ON is FRAGILE: +13.4 (rule off)", L[0])
        self.assertIn("not a forecast", L[0])
        self.assertEqual(IR.room_band(rec["scenarios"]), dict(constant="il_return.ROOM_RULE_ON", shift=13.4, label="rule off", tier="FRAGILE"))
        self.assertEqual(IR.room_band(dict(on_time=dict(title=25.0), on_time_rule_flipped=dict(title=25.6)))["tier"], "ROBUST")
        del rec["scenarios"]["on_time_rule_flipped"]
        self.assertIn("band not measured this run", IR.lines(rec)[0])
        self.assertIn("ESPN's earliest-return dates of", IR.lines(rec)[0])    # owner 2026-11-11: the date is a floor
        self.assertTrue(L[1].startswith("- Me: Hali (earliest 2026-11-13, wk 4)")); self.assertIn("Naji (no ESPN date, never)", L[2])


class TwoWorlds(unittest.TestCase):
    """Owner 2026-11-11 (card: "Cancel the two late worlds"): the +2 week and +4 week worlds read the same as on time
    within sampling error (25.81 and 25.86 beside 25.95 on 11-11), so the step runs never and on time only."""
    def test_the_grid_is_on_time_only(self):
        self.assertEqual(IR.SLIPS, {"on_time": 0})

    def test_the_scenarios_run_carry_no_late_world(self):
        calls = []
        real = IR.CG.run_league_sim, IR.CG.rosters, IR.odds
        try:
            IR.CG.rosters = lambda state, by, include_il=False: {}
            IR.CG.run_league_sim = lambda ros, seed, seasons, work, tag=None, windows=None: calls.append(tag) or {}
            IR.odds = lambda runs: dict(title=20.0, playoffs=90.0)
            sc = IR.run_scenarios({}, {}, [], 17, 100, "/tmp")
        finally:
            IR.CG.run_league_sim, IR.CG.rosters, IR.odds = real
        self.assertEqual(sorted(sc), ["never", "on_time", "on_time_rule_flipped", "seat10_only_on_time"])
        self.assertEqual(len(calls), 8)   # four worlds on two seeds; six worlds before

    def test_the_section_line_states_one_figure_not_a_range(self):
        rec = dict(espn_date="2026-11-11", n_il=1, room_rule="r", error=0.7, seasons=10000,
                   scenarios=dict(never=dict(title=16.1), on_time=dict(title=25.9), on_time_rule_flipped=dict(title=37.4)),
                   il_players=[dict(seat=10, team="Me", player="Hali", return_date="2026-11-13", week=4)])
        line = IR.lines(rec)[0]
        self.assertIn("if they return on ESPN's dates ≈25.9% · never = headline 16.1%", line)
        self.assertNotIn("+2 wk", line); self.assertNotIn(" to ", line.split("never")[0])

    def test_the_blend_is_not_computed_without_its_worlds_and_an_old_record_still_blends(self):
        self.assertIsNone(IR.blend(dict(never=dict(title=16.0), on_time=dict(title=26.0))))
        old = {k: dict(title=t) for k, t in (("never", 10.0), ("on_time", 20.0), ("late_2", 20.0), ("late_4", 20.0))}
        self.assertEqual(IR.blend(old), 19.0)



class KnownAnswers(unittest.TestCase):
    """Audit finding F3 (2026-11-12): attack A-10's record is written by the script (--checks --attack-record) with
    the script's own sha256, so the checks are reproducible and a changed script stales the record."""
    def sc(self, **over):
        o = lambda a, b: dict(title_by_seed={"2026": a, "2027": b}, title=round((a + b) / 2, 2), seed_spread=round(abs(a - b), 2))
        sc = dict(never=o(20.0, 20.4), on_time=o(25.0, 25.2), seat10_only_on_time=o(29.0, 29.4),
                  check_week1_no_room=o(40.0, 41.0), check_include_il=o(40.0, 41.0), check_after_last_week=o(20.0, 20.4))
        sc.update({k: o(*v) for k, v in over.items()})
        return sc

    def test_every_check_passes_on_consistent_runs(self):
        ch = IR.known_answers(self.sc(), {"2026": 20.0, "2027": 20.4}, 0.5)
        rec = IR.attack_record(dict(date="d", state="s", state_as_of="d", espn="e", pool="p", seasons=1, seeds=[1], n_il=2), ch, "abc1234", {"scripts/il_return.py": "x"})
        self.assertEqual(rec["verdict"], "PASS", ch)
        self.assertEqual(rec["fingerprint"], {"deck_head": "abc1234", "kit_sha256": {"scripts/il_return.py": "x"}})
        self.assertIsNone(ch["seat10_monotonic_within_error"]["ok"])

    def test_a_headline_that_differs_from_the_brief_fails(self):
        ch = IR.known_answers(self.sc(), {"2026": 20.1, "2027": 20.4}, 0.5)
        self.assertFalse(ch["never_equals_brief_headline"]["ok"])
        self.assertEqual(IR.attack_record(dict(date="d", state="s", state_as_of="d", espn="e", pool="p", seasons=1, seeds=[1], n_il=2), ch, "a", {})["verdict"], "FAIL")

    def test_the_exact_checks_fail_on_a_one_hundredth_difference(self):
        ch = IR.known_answers(self.sc(check_include_il=(40.01, 41.0)), None, 0.5)
        self.assertFalse(ch["week1_no_room_equals_include_il"]["ok"])
        self.assertNotIn("never_equals_brief_headline", ch)
        ch = IR.known_answers(self.sc(check_after_last_week=(20.0, 20.41)), None, 0.5)
        self.assertFalse(ch["after_last_week_equals_headline"]["ok"])

    def test_own_returns_lowering_the_title_beyond_error_fails(self):
        ch = IR.known_answers(self.sc(seat10_only_on_time=(19.0, 19.2)), None, 0.5)
        self.assertFalse(ch["seat10_only_within_error_of_never_or_above"]["ok"])


if __name__ == "__main__":
    unittest.main()
