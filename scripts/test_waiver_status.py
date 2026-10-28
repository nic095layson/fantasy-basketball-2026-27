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
                                 "date": "2026-10-26T22:07Z", "comment": "surgery"}])


if __name__ == "__main__":
    unittest.main(verbosity=2)
