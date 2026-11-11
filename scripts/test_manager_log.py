#!/usr/bin/env python3
"""Red-first tests for manager_log.py: each manager's locked lineup against who played (starts lost), adds/drops and
IL use, recorded per day and rolled up per team. Record only: nothing here feeds the engine."""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import manager_log as ML  # noqa: E402

ACTIVE = ["PG", "SG", "G", "SF", "PF", "F", "C", "C", "Util", "Util"]


def lineup(team_key, date, players):
    """players: [(name, positions, slot)]"""
    return {"teamKey": team_key, "teamName": "Team " + team_key[-1], "ownerName": "O" + team_key[-1],
            "snapshot": {"type": "date", "date": date},
            "players": [{"name": n, "position": pos, "selectedPosition": s} for n, pos, s in players]}


def box(*rows):
    """rows: (name, team, minutes) — minutes 0 is a DNP line."""
    return {"players": [{"name": n, "pool_name": None, "team": t, "dnp": m == 0, "min": m} for n, t, m in rows]}


class Day(unittest.TestCase):
    def test_a_full_lineup_of_players_who_played_loses_nothing(self):
        players = [(f"P{i}", "PG,SG,SF,PF,C", s) for i, s in enumerate(ACTIVE)] + [("B1", "C", "BN")]
        rec = ML.team_day(lineup("x.t.1", "2026-10-21", players), box(*[(f"P{i}", "ATL", 30) for i in range(10)]), {})
        self.assertEqual((rec["starts"], rec["best_starts"], rec["starts_lost"]), (10, 10, 0))

    def test_a_benched_player_who_played_over_an_idle_eligible_slot_is_a_lost_start(self):
        players = [("Idle C", "C", "C"), ("Bench C", "C", "BN"), ("Guard", "PG", "PG")]
        rec = ML.team_day(lineup("x.t.1", "2026-10-21", players), box(("Bench C", "ATL", 25), ("Guard", "ATL", 30)), {})
        self.assertEqual((rec["starts"], rec["best_starts"], rec["starts_lost"]), (1, 2, 1))
        self.assertEqual(rec["benched_played"], ["Bench C"])

    def test_position_eligibility_decides_whether_a_bench_game_was_lost(self):
        # every active slot holds a player who played except one C; a benched PG who played cannot fill it, and no
        # starter can move into it, so nothing was lost (an empty slot, by contrast, is a real chance: G or Util)
        fill = {"PG": "PG", "SG": "SG", "G": "PG", "SF": "SF", "PF": "PF", "F": "SF", "C": "C", "Util": "SF"}
        players = [(f"S{i}", fill[s], s) for i, s in enumerate(ACTIVE) if i != 7] + [("Idle C", "C", "C"),
                                                                                    ("Bench PG", "PG", "BN")]
        played = [(f"S{i}", "ATL", 30) for i in range(10) if i != 7] + [("Bench PG", "ATL", 25)]
        rec = ML.team_day(lineup("x.t.1", "2026-10-21", players), box(*played), {})
        self.assertEqual((rec["starts"], rec["best_starts"], rec["starts_lost"]), (9, 9, 0))
        self.assertEqual(rec["benched_played"], ["Bench PG"])

    def test_a_reshuffle_counts_when_only_moving_a_starter_frees_the_slot(self):
        # Util holds a non-player; the benched C who played needs C, which a flexible starter occupies
        players = [("Flex", "PF,C", "C"), ("Idle", "PG", "Util"), ("Bench C", "C", "BN")]
        rec = ML.team_day(lineup("x.t.1", "2026-10-21", players), box(("Flex", "ATL", 30), ("Bench C", "ATL", 20)), {})
        self.assertEqual((rec["starts"], rec["best_starts"], rec["starts_lost"]), (1, 2, 1))

    def test_il_slot_players_never_count_as_startable(self):
        players = [("Guard", "PG", "PG"), ("Hurt", "C", "IL")]
        rec = ML.team_day(lineup("x.t.1", "2026-10-21", players), box(("Guard", "ATL", 30), ("Hurt", "ATL", 10)), {})
        self.assertEqual((rec["starts"], rec["best_starts"], rec["starts_lost"]), (1, 1, 0))
        self.assertEqual((rec["il_slots_used"], rec["il_played"]), (1, ["Hurt"]))

    def test_a_dnp_line_is_not_a_game_played(self):
        players = [("Idle C", "C", "C"), ("Bench C", "C", "BN")]
        rec = ML.team_day(lineup("x.t.1", "2026-10-21", players), box(("Bench C", "ATL", 0)), {})
        self.assertEqual(rec["starts_lost"], 0)

    def test_names_fold_across_accents_and_suffixes(self):
        players = [("Idle C", "C", "C"), ("Nikola Jokić", "C", "BN")]
        rec = ML.team_day(lineup("x.t.1", "2026-10-21", players), box(("Nikola Jokic", "DEN", 35)), {})
        self.assertEqual(rec["starts_lost"], 1)

    def test_a_player_whose_team_played_but_who_has_no_box_line_is_named_not_guessed(self):
        players = [("Ghost", "SF", "SF"), ("Rested", "PF", "PF")]
        rec = ML.team_day(lineup("x.t.1", "2026-10-21", players), box(("Someone", "ATL", 20)),
                          {"Ghost": "ATL", "Rested": "BOS"})
        self.assertEqual(rec["no_box_line"], [{"name": "Ghost", "slot": "SF"}])  # BOS did not play: no game, no flag


class Transactions(unittest.TestCase):
    def test_moves_union_by_id_and_count_per_team(self):
        a = [{"transaction_id": "L.tr.1", "type": "add", "date": "2026-10-20", "team_ids": ["L.t.1"],
              "players_added": [{"name": "A"}], "players_dropped": [{"name": "B"}]}]
        b = a + [{"transaction_id": "L.tr.2", "type": "drop", "date": "2026-10-21", "team_ids": ["L.t.2"],
                  "players_added": [], "players_dropped": [{"name": "C"}]}]
        merged, new = ML.union_moves(a, b)
        self.assertEqual((len(merged), new), (2, 1))
        counts = ML.move_counts(merged)
        self.assertEqual(counts["L.t.1"], {"adds": 1, "drops": 1, "moves": 1})
        self.assertEqual(counts["L.t.2"], {"adds": 0, "drops": 1, "moves": 1})


class Rollup(unittest.TestCase):
    def test_profile_sums_days_and_states_the_rate_with_its_sample(self):
        days = [{"date": "2026-10-20", "teams": {"L.t.1": {"team": "T", "owner": "O", "starts": 9, "best_starts": 10,
                                                            "starts_lost": 1, "il_slots_used": 1}}},
                {"date": "2026-10-21", "teams": {"L.t.1": {"team": "T", "owner": "O", "starts": 8, "best_starts": 8,
                                                            "starts_lost": 0, "il_slots_used": 2}}}]
        prof = ML.rollup(days, {"L.t.1": {"adds": 2, "drops": 1, "moves": 2}})
        t = prof["teams"]["L.t.1"]
        self.assertEqual((t["days"], t["starts"], t["best_starts"], t["starts_lost"]), (2, 17, 18, 1))
        self.assertAlmostEqual(t["start_rate"], 17 / 18)
        self.assertEqual((t["il_player_days"], t["adds"], t["drops"]), (3, 2, 1))
        self.assertEqual(prof["window"], {"first": "2026-10-20", "last": "2026-10-21", "days": 2})

    def test_each_team_carries_the_owners_name_for_its_manager_and_an_unknown_team_is_none(self):
        # owner 2026-10-28: the profiles name each league mate as the league state does (the owner's names), not by
        # Yahoo's account name; a team the state does not hold gets None, never a guess
        days = [{"date": "2026-10-20", "teams": {
            "L.t.1": {"team": "Lauri\u2019s Prime Rib", "owner": "William", "starts": 9, "best_starts": 9, "starts_lost": 0, "il_slots_used": 0},
            "L.t.2": {"team": "Nobody's Team", "owner": "X", "starts": 9, "best_starts": 9, "starts_lost": 0, "il_slots_used": 0}}}]
        state = {"teams": [{"name": "Lauri\u2019s Prime Rib", "manager": "Will"}, {"name": "Other", "manager": "Kyle"}]}
        prof = ML.rollup(days, {}, ML.managers_by_team(state))
        self.assertEqual(prof["teams"]["L.t.1"]["manager"], "Will")
        self.assertEqual(prof["teams"]["L.t.1"]["owner"], "William")
        self.assertIsNone(prof["teams"]["L.t.2"]["manager"])

    def test_the_team_name_match_ignores_case_and_apostrophe_style(self):
        m = ML.managers_by_team({"teams": [{"name": "Lauri\u2019s Prime Rib", "manager": "Will"}]})
        self.assertEqual(ML.team_manager(m, "LAURI'S PRIME RIB"), "Will")


class Pins(unittest.TestCase):
    def test_the_days_lineups_come_from_the_pinned_pulls_latest_pin_winning(self):
        with tempfile.TemporaryDirectory() as d:
            for name, slot in (("pull_2026-10-22.json", "BN"), ("pull_2026-10-23.json", "C")):
                with open(os.path.join(d, name), "w") as f:
                    json.dump({"daily": {"x.t.1": {"2026-10-21": lineup("x.t.1", "2026-10-21", [("A", "C", slot)])}}}, f)
            got = ML.pinned_lineups(d, "2026-10-21")
        self.assertEqual(got["x.t.1"]["players"][0]["selectedPosition"], "C")


class FeedShortfall(unittest.TestCase):
    """Owner 2026-11-11 (council pick: "the manager log prints how many rows Flaim could not read"): Flaim's
    get_transactions response says when Yahoo's page carried entries it could not interpret, or rows it dropped for a
    bad timestamp. The log keeps that count beside the moves, so the adds counter says when it may be short."""
    WARN = ("Yahoo returned 6 entries Flaim could not interpret (an unrecognized transaction type or a malformed entry). "
            "This count covers the whole page Flaim fetched.")

    def transcript(self, *datas):
        import json, tempfile
        f = tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False)
        for i, d in enumerate(datas):
            body = json.dumps(dict(success=True, data=dict(d, league_id=ML.LEAGUE_KEY)))
            f.write(json.dumps(dict(timestamp=f"2026-11-11T13:0{i}:00Z", message=dict(content=[dict(type="tool_result", content=body)]))) + "\n")
        f.close()
        return f.name

    def test_the_count_is_read_from_the_warning_and_the_dropped_field(self):
        t = self.transcript(dict(transactions=[], warning=self.WARN, dropped_invalid_timestamp_count=2))
        self.assertEqual(ML.feed_shortfall(t), dict(uninterpreted=6, dropped_invalid_timestamp=2, warning=self.WARN))

    def test_a_clean_response_reads_zero_and_no_response_reads_none(self):
        t = self.transcript(dict(transactions=[], dropped_invalid_timestamp_count=0))
        self.assertEqual(ML.feed_shortfall(t), dict(uninterpreted=0, dropped_invalid_timestamp=0, warning=None))
        self.assertIsNone(ML.feed_shortfall(self.transcript()))

    def test_the_newest_response_wins(self):
        t = self.transcript(dict(transactions=[], warning=self.WARN, dropped_invalid_timestamp_count=0),
                            dict(transactions=[], warning=self.WARN.replace("6 entries", "1 entry"), dropped_invalid_timestamp_count=0))
        self.assertEqual(ML.feed_shortfall(t)["uninterpreted"], 1)

    def test_a_warning_of_another_kind_is_kept_but_counts_nothing(self):
        t = self.transcript(dict(transactions=[], warning="Yahoo was slow today.", dropped_invalid_timestamp_count=0))
        self.assertEqual(ML.feed_shortfall(t), dict(uninterpreted=0, dropped_invalid_timestamp=0, warning="Yahoo was slow today."))

    def test_the_note_names_the_shortfall_and_is_silent_when_there_is_none(self):
        self.assertEqual(ML.shortfall_note(dict(uninterpreted=6, dropped_invalid_timestamp=0, warning=self.WARN)),
                         "Flaim could not read 6 row(s) on Yahoo's page (the moves on record may be short)")
        self.assertEqual(ML.shortfall_note(dict(uninterpreted=1, dropped_invalid_timestamp=2, warning=self.WARN)),
                         "Flaim could not read 3 row(s) on Yahoo's page (the moves on record may be short)")
        self.assertIsNone(ML.shortfall_note(dict(uninterpreted=0, dropped_invalid_timestamp=0, warning=None)))
        self.assertIsNone(ML.shortfall_note(None))


if __name__ == "__main__":
    unittest.main()
