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
        self.assertTrue(L[1].startswith("- Me: Hali (2026-11-13, wk 4)")); self.assertIn("Naji (no ESPN date, never)", L[2])


if __name__ == "__main__":
    unittest.main()
