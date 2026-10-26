#!/usr/bin/env python3
"""Red-first tests for flaim_live.py (owner 2026-10-21: "Build A, B, C, D"): the Yahoo league read through the Flaim
connector, extracted mechanically from the session transcript like FantasyBot's — every team's real Yahoo slots and
status letters (C, B), this week's matchup totals (A) and the available-player list (D).

    python3 scripts/test_flaim_live.py
"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import flaim_live as FL  # noqa: E402

KEY = FL.LEAGUE_KEY


def roster(team_id, name, players, snapshot="current"):
    """A get_roster response; players is [(name, nba, positions, selectedPosition, status or None)]."""
    snap = {"type": snapshot} if snapshot == "current" else {"type": "date", "date": snapshot}
    ps = []
    for n, t, pos, sel, st in players:
        p = {"playerKey": "478.p.1", "playerId": "1", "name": n, "team": t, "position": pos, "selectedPosition": sel}
        if st:
            p["status"] = st
        ps.append(p)
    return {"success": True, "data": {"teamKey": f"{KEY}.t.{team_id}", "teamName": name, "ownerName": "x",
                                      "snapshot": snap, "players": ps}}


def side(team_id, name, fga, fgm, fta, ftm, rest, left):
    tpm, pts, reb, ast, stl, blk, tov = rest
    cats = [("9004003", "FGM/A", f"{fgm}/{fga}"), ("5", "FG%", "x"), ("9007006", "FTM/A", f"{ftm}/{fta}"),
            ("8", "FT%", "x"), ("10", "3PTM", str(tpm)), ("12", "PTS", str(pts)), ("15", "REB", str(reb)),
            ("16", "AST", str(ast)), ("17", "ST", str(stl)), ("18", "BLK", str(blk)), ("19", "TO", str(tov))]
    return {"teamKey": f"{KEY}.t.{team_id}", "teamId": str(team_id), "teamName": name, "gamesRemaining": left,
            "categories": [{"statId": s, "displayName": d, "value": v} for s, d, v in cats]}


def matchups(week, pairs):
    return {"success": True, "data": {"leagueKey": KEY, "currentWeek": week, "matchupWeek": week,
                                      "scoringType": "categories",
                                      "matchups": [{"matchupId": i + 1, "week": week, "home": h, "away": a}
                                                   for i, (h, a) in enumerate(pairs)]}}


def free_agents(players):
    return {"success": True, "data": {"leagueKey": KEY, "position": "ALL", "count": len(players),
                                      "freeAgents": [dict({"name": n, "team": t, "position": pos},
                                                          **({"status": st} if st else {}))
                                                     for n, t, pos, st in players]}}


def standings(rows):
    """A get_standings response: rows = [(team_id, name, wins, losses, ties)]."""
    return {"success": True, "data": {"leagueKey": KEY, "leagueName": "x", "seasonPhase": "regular_season",
                                      "standings": [{"teamKey": f"{KEY}.t.{i}", "teamId": str(i), "name": n,
                                                     "wins": str(w), "losses": str(l), "ties": t, "rank": str(k + 1)}
                                                    for k, (i, n, w, l, t) in enumerate(rows)]}}


def line(ts, payload):
    """One transcript entry carrying a tool result whose text is the JSON response, as the harness writes it."""
    o = {"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": "t", "content": json.dumps(payload)}]}}
    if ts:
        o["timestamp"] = ts
    return json.dumps(o) + "\n"


def twelve(ts, letters=None):
    letters = letters or {}
    return "".join(line(ts, roster(i, f"Team {i}", [(f"P{i}a", "BOS", "PG,SG", "PG", letters.get(i)),
                                                      (f"P{i}b", "DEN", "C", "IL", "O")])) for i in range(1, 13))


class Extract(unittest.TestCase):
    def write(self, text):
        fd, p = tempfile.mkstemp(suffix=".jsonl")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        self.addCleanup(os.remove, p)
        return p

    def test_twelve_current_rosters_a_matchup_and_free_agents_are_read(self):
        tr = self.write(twelve("2026-10-22T12:55:00Z")
                        + line("2026-10-22T12:55:30Z", matchups(1, [(side(10, "Team 10", 67, 26, 24, 18, (9, 79, 37, 15, 7, 9, 10), 33),
                                                                     side(11, "Team 11", 16, 8, 2, 1, (3, 20, 5, 10, 2, 2, 5), 32))]))
                        + line("2026-10-22T12:55:40Z", free_agents([("Jrue Holiday", "POR", "PG,SG", None)])))
        pull = FL.extract_pull(tr)
        self.assertEqual(len(pull["rosters"]), 12)
        self.assertEqual(sorted(pull["matchups"]), ["1"])
        self.assertEqual(pull["free_agents"]["freeAgents"][0]["name"], "Jrue Holiday")
        FL.check_pull(pull)

    def test_the_standings_response_is_read_and_pinned(self):
        # owner 2026-10-26 (item 7): Yahoo's standings pinned daily beside the rosters, for the record
        tr = self.write(twelve("2026-10-27T12:55:00Z") + line("2026-10-27T12:56:00Z", standings([(12, "Team 12", 6, 2, 1), (1, "Team 1", 6, 3, 0)])))
        pull = FL.extract_pull(tr)
        self.assertEqual([r["name"] for r in pull["standings"]["standings"]], ["Team 12", "Team 1"])
        other = self.write(line("2026-10-27T12:56:00Z", {"success": True, "data": dict(standings([])["data"], leagueKey="478.l.1")}))
        self.assertIsNone(FL.extract_pull(other)["standings"])          # another league's standings are ignored

    def test_a_later_pin_with_no_standings_keeps_the_earlier_pins(self):
        path = self.pin({}, standings={"standings": [{"name": "A"}]})
        pull = FL.keep_daily({"source": "flaim", "daily": {}, "matchups": {}, "free_agents": None, "standings": None}, path)
        self.assertEqual(pull["standings"], {"standings": [{"name": "A"}]})
        self.assertIn("standings", pull["carried_forward"])

    def test_a_dated_snapshot_is_never_read_as_todays_roster(self):
        tr = self.write(twelve("2026-10-22T12:55:00Z")
                        + line("2026-10-22T12:56:00Z", roster(3, "Team 3", [("Old Day", "BOS", "PG", "PG", None)], snapshot="2026-10-20")))
        pull = FL.extract_pull(tr)
        self.assertEqual([p["name"] for p in pull["rosters"][f"{KEY}.t.3"]["players"]][0], "P3a")

    def test_a_dated_snapshot_is_kept_as_that_days_lineup(self):
        # owner 2026-10-22 ("Read daily rosters"): the week card's rebuild counts each past day's real Yahoo lineup
        tr = self.write(twelve("2026-10-22T12:55:00Z")
                        + line("2026-10-22T12:56:00Z", roster(3, "Team 3", [("Old Day", "BOS", "PG", "PG", None),
                                                                            ("Sat Out", "DEN", "C", "BN", None)], snapshot="2026-10-20")))
        day = FL.extract_pull(tr)["daily"][f"{KEY}.t.3"]["2026-10-20"]
        self.assertEqual((day["teamName"], [(p["name"], p["selectedPosition"]) for p in day["players"]]),
                         ("Team 3", [("Old Day", "PG"), ("Sat Out", "BN")]))

    def test_the_latest_response_for_a_team_and_day_wins(self):
        first = roster(3, "Team 3", [("First", "BOS", "PG", "PG", None)], snapshot="2026-10-20")
        later = roster(3, "Team 3", [("Later", "BOS", "PG", "PG", None)], snapshot="2026-10-20")
        pull = FL.extract_pull(self.write(line("2026-10-22T12:56:00Z", first) + line("2026-10-22T12:57:00Z", later)))
        self.assertEqual(pull["daily"][f"{KEY}.t.3"]["2026-10-20"]["players"][0]["name"], "Later")

    def test_another_leagues_dated_snapshot_is_ignored(self):
        other = roster(5, "Elsewhere", [("Ghost", "BOS", "PG", "PG", None)], snapshot="2026-10-20")
        other["data"]["teamKey"] = "466.l.17544.t.5"
        self.assertEqual(FL.extract_pull(self.write(line("2026-10-22T12:57:00Z", other)))["daily"], {})

    def test_a_later_pin_for_the_same_date_keeps_an_earlier_pins_lineups(self):
        # the afternoon check rewrites the morning's pull file and fetches no dated lineup; the week card reads the
        # morning's on later days (found by the verify pass, 2026-10-22)
        morning = roster(3, "Team 3", [("Played", "BOS", "PG", "PG", None)], snapshot="2026-10-20")["data"]
        pull = FL.keep_daily({"source": "flaim", "daily": {}}, self.pin({f"{KEY}.t.3": {"2026-10-20": morning}}))
        self.assertEqual(pull["daily"][f"{KEY}.t.3"]["2026-10-20"]["players"][0]["name"], "Played")

    def test_the_later_pin_wins_for_a_team_and_day_and_keeps_the_other_days(self):
        old = roster(3, "Team 3", [("Old", "BOS", "PG", "PG", None)], snapshot="2026-10-20")["data"]
        kept = roster(3, "Team 3", [("Kept", "BOS", "PG", "PG", None)], snapshot="2026-10-21")["data"]
        new = roster(3, "Team 3", [("New", "BOS", "PG", "PG", None)], snapshot="2026-10-20")["data"]
        pull = FL.keep_daily({"source": "flaim", "daily": {f"{KEY}.t.3": {"2026-10-20": new}}},
                             self.pin({f"{KEY}.t.3": {"2026-10-20": old, "2026-10-21": kept}}))
        self.assertEqual({d: r["players"][0]["name"] for d, r in pull["daily"][f"{KEY}.t.3"].items()},
                         {"2026-10-20": "New", "2026-10-21": "Kept"})

    def test_a_later_pin_with_no_matchups_or_free_agents_keeps_the_earlier_pins(self):
        # the 3 PM check pulls rosters only; its re-pin dropped the morning's matchups and available-player list,
        # which the week card reads (owner 2026-10-22, "Carry them forward")
        path = self.pin({}, matchups={"1": {"m": 1}}, free_agents={"freeAgents": [{"name": "A"}]})
        pull = FL.keep_daily({"source": "flaim", "daily": {}, "matchups": {}, "free_agents": None}, path)
        self.assertEqual((pull["matchups"], pull["free_agents"], pull["carried_forward"]),
                         ({"1": {"m": 1}}, {"freeAgents": [{"name": "A"}]}, ["free_agents", "matchups"]))

    def test_a_later_pins_own_matchups_and_free_agents_win(self):
        path = self.pin({}, matchups={"1": {"m": "old"}}, free_agents={"freeAgents": [{"name": "Old"}]})
        later = {"source": "flaim", "daily": {}, "matchups": {"1": {"m": "new"}}, "free_agents": {"freeAgents": []}}
        pull = FL.keep_daily(later, path)
        self.assertEqual((pull["matchups"], pull["free_agents"], "carried_forward" in pull),
                         ({"1": {"m": "new"}}, {"freeAgents": []}, False))

    def test_a_same_day_re_pin_keeps_a_week_the_earlier_pin_had_and_the_new_pull_lacks(self):
        # owner 2026-10-26 ("same-day re-runs keep earlier final results"): the 15:12Z morning re-run re-pinned
        # pull_2026-10-26.json with week 2 only, and week 1's finals, pinned by the first run, were lost
        path = self.pin({}, matchups={"1": {"m": "week 1 finals"}, "2": {"m": "old 2"}})
        pull = FL.keep_daily({"source": "flaim", "daily": {}, "matchups": {"2": {"m": "new 2"}}}, path)
        self.assertEqual(pull["matchups"], {"1": {"m": "week 1 finals"}, "2": {"m": "new 2"}})
        self.assertEqual(pull["carried_forward"], ["matchups week 1"])

    def test_with_no_earlier_pin_the_pull_is_pinned_as_it_is(self):
        pull = {"source": "flaim", "daily": {}}
        self.assertEqual(FL.keep_daily(dict(pull), os.path.join(tempfile.mkdtemp(), "pull_2026-10-22.json")), pull)

    def pin(self, daily, **more):
        fd, p = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(dict({"source": "flaim", "daily": daily}, **more), f)
        return p

    def test_another_leagues_rosters_are_ignored(self):
        other = roster(5, "Elsewhere", [("Ghost", "BOS", "PG", "PG", None)])
        other["data"]["teamKey"] = "466.l.17544.t.5"
        pull = FL.extract_pull(self.write(twelve("2026-10-22T12:55:00Z") + line("2026-10-22T12:57:00Z", other)))
        self.assertEqual(len(pull["rosters"]), 12)
        self.assertNotIn("466.l.17544.t.5", pull["rosters"])

    def test_since_keeps_only_this_runs_entries(self):
        tr = self.write(twelve("2026-10-21T12:55:00Z") + line("2026-10-22T12:55:00Z", roster(1, "Team 1", [("New", "BOS", "PG", "PG", None)])))
        pull = FL.extract_pull(tr, since="2026-10-22T12:53:00Z")
        self.assertEqual(len(pull["rosters"]), 1)
        with self.assertRaises(FL.PullError):
            FL.check_pull(pull)

    def test_eleven_teams_halts(self):
        pull = FL.extract_pull(self.write("".join(line("2026-10-22T12:55:00Z", roster(i, f"T{i}", [("A", "BOS", "PG", "PG", None)]))
                                                  for i in range(1, 12))))
        with self.assertRaisesRegex(FL.PullError, "11 of 12"):
            FL.check_pull(pull)

    def test_d_doubtful_is_a_known_letter_and_does_not_halt(self):
        # owner 2026-10-21: "Stewart's 'D' means 'Doubtful'" (status_feed.TIERS, D-IS-10)
        FL.check_pull(FL.extract_pull(self.write(twelve("2026-10-22T12:55:00Z", letters={4: "D"}))))

    def test_an_unknown_status_letter_halts_and_is_named(self):
        pull = FL.extract_pull(self.write(twelve("2026-10-22T12:55:00Z", letters={4: "ZZZ"})))
        with self.assertRaisesRegex(FL.PullError, "ZZZ"):
            FL.check_pull(pull)


class Rows(unittest.TestCase):
    def test_every_team_keeps_its_yahoo_slot_and_letter(self):
        rows = FL.to_rows({"rosters": {f"{KEY}.t.10": roster(10, "MAXEY-MUM OVERDRIVE", [
            ("Kevin Porter Jr.", "MIL", "PG,SG", "PG", "NA"), ("Tyrese Maxey", "PHI", "PG", "BN", None),
            ("Immanuel Quickley", "TOR", "PG,SG", "Util", None), ("Kon Knueppel", "CHA", "SG,SF", "IL", "O")])["data"]}})
        got = [(r["fantasy_team"], r["slot"], r["player"], r["nba_team"], r["positions"], r["status"]) for r in rows]
        self.assertEqual(got, [("MAXEY-MUM OVERDRIVE", "PG", "Kevin Porter Jr.", "MIL", "PG,SG", "NA"),
                               ("MAXEY-MUM OVERDRIVE", "BN", "Tyrese Maxey", "PHI", "PG", ""),
                               ("MAXEY-MUM OVERDRIVE", "UTIL", "Immanuel Quickley", "TOR", "PG,SG", ""),
                               ("MAXEY-MUM OVERDRIVE", "IL", "Kon Knueppel", "CHA", "SG,SF", "O")])


class Matchup(unittest.TestCase):
    def test_a_sides_category_totals_parse_from_yahoo_values(self):
        s = side(11, "Mine", 16, 8, 2, 1, (3, 20, 5, 10, 2, 2, 5), 32)
        self.assertEqual(FL.side_totals(s), dict(fgm=8, fga=16, ftm=1, fta=2, tpm=3, pts=20, reb=5, ast=10, stl=2, blk=2, tov=5))

    def test_no_free_throws_reads_as_zero_over_zero(self):
        s = side(4, "Splash", 4, 2, 0, 0, (0, 4, 3, 3, 1, 1, 2), 36)
        self.assertEqual((FL.side_totals(s)["ftm"], FL.side_totals(s)["fta"]), (0, 0))

    def test_the_owners_matchup_is_found_by_team_name(self):
        m = matchups(1, [(side(1, "A", 1, 1, 1, 1, (0,) * 7, 1), side(9, "B", 1, 1, 1, 1, (0,) * 7, 1)),
                         (side(10, "Opp", 67, 26, 24, 18, (9, 79, 37, 15, 7, 9, 10), 33),
                          side(11, "Me", 16, 8, 2, 1, (3, 20, 5, 10, 2, 2, 5), 32))])["data"]
        me, opp = FL.find_sides(m, "Me", "Opp")
        self.assertEqual((me["teamId"], opp["teamId"]), ("11", "10"))
        self.assertEqual(FL.find_sides(m, "Me", "Nobody"), (None, None))


if __name__ == "__main__":
    unittest.main(verbosity=2)
