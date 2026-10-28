#!/usr/bin/env python3
"""Red-first tests for the waiver scan's status gate (owner 2026-10-28, "Status gate (Recommended)").

Candidates stay every pool player no league roster holds (that is what can be claimed: a free agent or on waivers);
the day's injury status now gates them:
  - Out (Yahoo O or NA, or ESPN "Out") is set aside from the waiver scan and the streaming list, and named;
  - D, Q, P and ESPN Day-To-Day stay in the waiver scan at full season value, flagged; streaming scales this
    week's games by their tier;
  - Yahoo's letter wins where the player is on the pinned available list; ESPN's feed covers the rest;
  - with no status source read for the day, the scan stops (StatusMissing) and never falls back to the pool.
The 2026-10-28 case: Jalen Williams, unrostered, not on Yahoo's ranked list, ESPN "Out", was the brief's top add.

Owner 2026-10-28 (item 5, "Use ESPN return date (Recommended)"): an Out whose ESPN expected return is at most
SHORT_OUT_DAYS (7) days after the brief's date stays in the waiver scan at full season value, flagged with the date;
streaming counts only the games on or after it. An Out with no ESPN return date (Yahoo O/NA with no ESPN entry, or an
ESPN entry without one) stays set aside.

    python3 scripts/test_waiver_status.py
"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import co_gm as CG  # noqa: E402
import status_feed as SF  # noqa: E402

P, BY = CG.load_pool()          # the frozen pool: real names and lines, no season file needed
STATE = {"teams": []}           # nobody rostered: every pool player is a candidate


def names(fa):
    return [p["player"] for p in fa]


def top_healthy(k):
    """The k best pool players by the scan's own order, so the tests use players that matter."""
    fa, _ = CG.free_agents(P, STATE, CG.fa_status(P, [], []), n=len(P))
    return names(fa)[:k]


class StatusGate(unittest.TestCase):
    def setUp(self):
        self.a, self.b, self.c, self.d = top_healthy(4)

    def test_a_yahoo_out_unrostered_player_is_never_a_candidate(self):
        st = CG.fa_status(P, [{"name": self.a, "status": "O"}], [])
        fa, aside = CG.free_agents(P, STATE, st)
        self.assertNotIn(self.a, names(fa))
        self.assertIn(self.a, [x["player"] for x in aside])

    def test_not_active_is_out_too(self):
        st = CG.fa_status(P, [{"name": self.a, "status": "NA"}], [])
        self.assertNotIn(self.a, names(CG.free_agents(P, STATE, st)[0]))

    def test_a_player_off_yahoos_list_with_espn_out_is_never_a_candidate(self):
        # the 10-28 case: not on the ranked list, so only ESPN carries his status
        st = CG.fa_status(P, [{"name": self.b, "status": None}], [{"player": self.a, "status": "Out"}])
        fa, aside = CG.free_agents(P, STATE, st)
        self.assertNotIn(self.a, names(fa))
        self.assertEqual([x["source"] for x in aside if x["player"] == self.a], ["espn"])

    def test_an_off_list_healthy_player_stays_a_candidate(self):
        # unrostered in the league is claimable (free agent or waivers); Yahoo's ranked list omits some of them
        st = CG.fa_status(P, [{"name": self.b, "status": None}], [])
        self.assertIn(self.a, names(CG.free_agents(P, STATE, st)[0]))

    def test_yahoo_wins_over_espn_where_the_player_is_listed(self):
        st = CG.fa_status(P, [{"name": self.a, "status": "Q"}], [{"player": self.a, "status": "Out"}])
        fa, _ = CG.free_agents(P, STATE, st)
        self.assertIn(self.a, names(fa))
        self.assertEqual(st["by"][self.a]["source"], "yahoo")

    def test_doubtful_and_questionable_stay_in_the_scan_flagged(self):
        st = CG.fa_status(P, [{"name": self.a, "status": "D"}, {"name": self.b, "status": "Q"}],
                          [{"player": self.c, "status": "Day-To-Day"}])
        fa, aside = CG.free_agents(P, STATE, st)
        self.assertTrue({self.a, self.b, self.c} <= set(names(fa)))
        self.assertEqual(aside, [])
        self.assertEqual((st["by"][self.a]["code"], st["by"][self.a]["availability"]), ("D", SF.TIERS["D"][1]))
        self.assertEqual(st["by"][self.c]["availability"], CG.ESPN_TIERS["Day-To-Day"][1])

    def test_an_unknown_letter_is_set_aside_never_guessed(self):
        st = CG.fa_status(P, [{"name": self.a, "status": "SUSP"}], [])
        fa, aside = CG.free_agents(P, STATE, st)
        self.assertNotIn(self.a, names(fa))
        self.assertIn("unknown", [x["reason"] for x in aside if x["player"] == self.a][0])

    def test_no_status_source_halts_loudly(self):
        with self.assertRaises(CG.StatusMissing):
            CG.fa_status(P, None, None)

    def test_one_source_missing_runs_and_names_it(self):
        st = CG.fa_status(P, None, [{"player": self.a, "status": "Out"}])
        self.assertEqual(st["sources"], {"yahoo": False, "espn": True})
        self.assertNotIn(self.a, names(CG.free_agents(P, STATE, st)[0]))

    def test_the_candidate_count_is_filled_after_the_gate(self):
        st = CG.fa_status(P, [{"name": self.a, "status": "O"}], [])
        self.assertEqual(len(CG.free_agents(P, STATE, st, n=10)[0]), 10)


class BriefInputs(unittest.TestCase):
    def test_a_day_with_no_pins_halts_the_scan_instead_of_using_the_pool(self):
        import tempfile
        import daily_brief as DB
        d = tempfile.mkdtemp()
        yahoo, espn = DB.status_inputs("2026-10-28", pull_dir=d, status_dir=d)
        self.assertEqual((yahoo, espn), (None, None))
        with self.assertRaises(CG.StatusMissing):
            CG.fa_status(P, yahoo, espn)

    def test_the_pins_are_read_when_present(self):
        import json
        import tempfile
        import daily_brief as DB
        d = tempfile.mkdtemp()
        json.dump({"free_agents": {"freeAgents": [{"name": "A", "status": "O"}]}}, open(os.path.join(d, "pull_2026-10-28.json"), "w"))
        json.dump({"rows": [{"player": "B", "status": "Out"}]}, open(os.path.join(d, "espn_injuries_2026-10-28.json"), "w"))
        self.assertEqual(DB.status_inputs("2026-10-28", pull_dir=d, status_dir=d),
                         ([{"name": "A", "status": "O"}], [{"player": "B", "status": "Out"}]))


class StreamingGate(unittest.TestCase):
    def test_streaming_scales_games_by_the_tier_and_drops_out_players(self):
        cands = [{"player": "Q-man", "team": "X", "games_left": 3, "value_per_game": 2.0, "availability": 0.5},
                 {"player": "Healthy", "team": "Y", "games_left": 3, "value_per_game": 1.0, "availability": 1.0},
                 {"player": "Out-man", "team": "Z", "games_left": 4, "value_per_game": 9.0, "availability": 0.0}]
        out = CG.streaming(cands, drop_games=2)
        self.assertEqual([r["player"] for r in out], ["Healthy"])           # 3 x 0.5 = 1.5 games is not more than 2
        self.assertEqual(out[0]["exp_games"], 3.0)

    def test_streaming_without_availability_reads_as_healthy(self):
        out = CG.streaming([{"player": "A", "team": "X", "games_left": 3, "value_per_game": 1.0}], drop_games=2)
        self.assertEqual(out[0]["exp_games"], 3.0)


class EspnPin(unittest.TestCase):
    def test_the_feed_is_trimmed_to_one_row_per_player(self):
        feed = {"injuries": [{"displayName": "Oklahoma City Thunder", "injuries": [
            {"status": "Out", "date": "2026-10-26T22:07Z", "shortComment": "surgery",
             "athlete": {"displayName": "Jalen Williams", "team": {"abbreviation": "OKC"}}}]}]}
        rows = SF.espn_rows(feed)
        self.assertEqual(rows, [{"player": "Jalen Williams", "team": "OKC", "status": "Out",
                                 "date": "2026-10-26T22:07Z", "comment": "surgery", "return_date": None}])


class ShortOut(unittest.TestCase):
    """Item 5: ESPN's expected return date splits a one-game Out from a long one."""
    DAY = "2026-10-28"

    def setUp(self):
        self.a, self.b, self.c, self.d = top_healthy(4)

    def gate(self, yahoo, espn):
        st = CG.fa_status(P, yahoo, espn, date=self.DAY)
        return st, CG.free_agents(P, STATE, st)

    def test_the_line_is_seven_days(self):
        self.assertEqual(CG.SHORT_OUT_DAYS, 7)

    def test_an_espn_out_back_within_the_line_stays_in_the_scan_flagged_with_the_date(self):
        st, (fa, aside) = self.gate([], [{"player": self.a, "status": "Out", "return_date": "2026-10-30"}])
        self.assertIn(self.a, names(fa))
        self.assertEqual(aside, [])
        self.assertEqual((st["by"][self.a]["code"], st["by"][self.a]["return_date"], st["by"][self.a]["short_out"]),
                         ("Out", "2026-10-30", True))

    def test_exactly_seven_days_is_inside_the_line_and_eight_is_out(self):
        _, (fa, _) = self.gate([], [{"player": self.a, "status": "Out", "return_date": "2026-11-04"},
                                    {"player": self.b, "status": "Out", "return_date": "2026-11-05"}])
        self.assertIn(self.a, names(fa))
        self.assertNotIn(self.b, names(fa))

    def test_a_long_out_is_set_aside_and_names_its_return_date(self):
        _, (fa, aside) = self.gate([], [{"player": self.a, "status": "Out", "return_date": "2027-03-02"}])
        self.assertNotIn(self.a, names(fa))
        self.assertEqual([(x["player"], x["return_date"]) for x in aside], [(self.a, "2027-03-02")])

    def test_an_espn_out_without_a_return_date_stays_set_aside(self):
        _, (fa, _) = self.gate([], [{"player": self.a, "status": "Out", "return_date": None},
                                    {"player": self.b, "status": "Out"}])
        self.assertFalse({self.a, self.b} & set(names(fa)))

    def test_a_yahoo_out_reads_espns_return_date(self):
        # Tobias Harris on 10-28: Yahoo O, ESPN Out (calf) expected back the same day
        st, (fa, _) = self.gate([{"name": self.a, "status": "O"}],
                                [{"player": self.a, "status": "Out", "return_date": "2026-10-28"}])
        self.assertIn(self.a, names(fa))
        self.assertEqual((st["by"][self.a]["source"], st["by"][self.a]["return_date"]), ("yahoo", "2026-10-28"))

    def test_a_yahoo_out_or_not_active_with_no_espn_entry_stays_set_aside(self):
        _, (fa, aside) = self.gate([{"name": self.a, "status": "O"}, {"name": self.b, "status": "NA"}], [])
        self.assertFalse({self.a, self.b} & set(names(fa)))
        self.assertEqual({x["player"] for x in aside}, {self.a, self.b})

    def test_a_past_return_date_counts_as_back(self):
        _, (fa, _) = self.gate([], [{"player": self.a, "status": "Out", "return_date": "2026-10-20"}])
        self.assertIn(self.a, names(fa))

    def test_without_the_days_date_every_out_stays_set_aside(self):
        st = CG.fa_status(P, [], [{"player": self.a, "status": "Out", "return_date": "2026-10-28"}])
        self.assertNotIn(self.a, names(CG.free_agents(P, STATE, st)[0]))

    def test_an_unknown_code_is_set_aside_whatever_its_return_date(self):
        _, (fa, _) = self.gate([{"name": self.a, "status": "SUSP"}],
                               [{"player": self.a, "status": "Out", "return_date": "2026-10-29"}])
        self.assertNotIn(self.a, names(fa))


class StreamRows(unittest.TestCase):
    """Streaming counts a short Out's games on or after ESPN's return date, at full availability."""
    GAMES = [("2026-10-28", "AAA", "BBB"), ("2026-10-30", "AAA", "CCC"), ("2026-11-01", "DDD", "AAA"),
             ("2026-11-02", "AAA", "BBB")]

    def test_a_short_out_counts_the_games_from_its_return(self):
        fa = [{"player": "Short", "team": "AAA"}, {"player": "Fine", "team": "AAA"}]
        st = {"by": {"Short": {"code": "Out", "source": "espn", "availability": 0.0, "return_date": "2026-10-30",
                               "short_out": True}}}
        rows = {r["player"]: r for r in CG.stream_rows(fa, st, self.GAMES, "2026-10-28", "2026-11-01", value=lambda p: 1.0)}
        self.assertEqual((rows["Fine"]["games_left"], rows["Short"]["games_left"]), (3, 3))
        self.assertEqual(rows["Short"]["games_from_return"], 2)
        out = {r["player"]: r for r in CG.streaming(list(rows.values()), drop_games=0)}
        self.assertEqual((out["Short"]["exp_games"], out["Fine"]["exp_games"]), (2, 3.0))

    def test_a_flagged_player_keeps_scaling_by_the_tier(self):
        st = {"by": {"Q": {"code": "Q", "source": "yahoo", "availability": 0.5, "return_date": None, "short_out": False}}}
        r = CG.stream_rows([{"player": "Q", "team": "AAA"}], st, self.GAMES, "2026-10-28", "2026-11-01", value=lambda p: 1.0)[0]
        self.assertNotIn("games_from_return", r)
        self.assertEqual(CG.streaming([r], drop_games=0)[0]["exp_games"], 1.5)


class EspnReturnDate(unittest.TestCase):
    def test_the_pin_keeps_espns_expected_return_date(self):
        feed = {"injuries": [{"injuries": [
            {"status": "Out", "date": "2026-10-26T21:48Z", "shortComment": "calf",
             "details": {"returnDate": "2026-10-28", "fantasyStatus": {"abbreviation": "GTD"}},
             "athlete": {"displayName": "Tobias Harris", "team": {"abbreviation": "DET"}}}]}]}
        self.assertEqual(SF.espn_rows(feed)[0]["return_date"], "2026-10-28")

    def test_a_row_without_details_has_no_return_date(self):
        feed = {"injuries": [{"injuries": [{"status": "Out", "athlete": {"displayName": "X"}}]}]}
        self.assertIsNone(SF.espn_rows(feed)[0]["return_date"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
