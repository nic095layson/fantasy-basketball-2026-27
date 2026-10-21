#!/usr/bin/env python3
"""Red-first tests for league_live.py (owner 2026-10-20: "Build all 3"): the FantasyBot pull
to league_state.json, through league_intake's name checks, with a halt instead of a bad write."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import league_live  # noqa: E402


def team(name, players):
    """A minimal get_league_team response: players is [(name, nba, positions, starter, reserve, injury)]."""
    return {"linked": True, "leagueName": league_live.LEAGUE, "mode": "team", "found": True, "teamName": name,
            "positions": [{"position": "PG", "players": [
                {"name": n, "team": t, "positions": pos, "starter": st, "reserve": rv, "injury": inj,
                 "status": None, "value": 0, "boardRank": None, "expertRank": None, "why": "", "gamesLeft": 0}
                for (n, t, pos, st, rv, inj) in players]}]}


def mine(starters, bench, ir):
    def P(n, t, pos, inj):
        return {"name": n, "team": t, "positions": pos.split("/"), "position": pos, "injury": inj, "statusLine": None}
    return {"linked": True, "leagueName": league_live.LEAGUE,
            "starters": [{"slot": s, "player": P(n, t, pos, inj)} for (s, n, t, pos, inj) in starters],
            "bench": [P(n, t, pos, inj) for (n, t, pos, inj) in bench],
            "ir": [P(n, t, pos, inj) for (n, t, pos, inj) in ir]}


class RowsFromPull(unittest.TestCase):
    def test_rival_reserve_ir_goes_to_il_and_the_rest_to_bn(self):
        pull = {"mine": None, "teams": {"T": team("T", [
            ("A Player", "BOS", "PG/SG", True, None, None),
            ("Hurt Guy", "LAL", "C", False, "ir", "Out")])}}
        rows = league_live.to_rows(pull)
        by = {r["player"]: r for r in rows}
        self.assertEqual(by["A Player"]["slot"], "BN")
        self.assertEqual(by["A Player"]["positions"], "PG,SG")
        self.assertEqual(by["Hurt Guy"]["slot"], "IL")
        self.assertEqual(by["Hurt Guy"]["status"], "O")

    def test_my_team_keeps_its_yahoo_slots(self):
        pull = {"teams": {}, "mine": mine([("PG", "My Guard", "IND", "PG/SG", None)],
                                          [("Bench Man", "NYK", "SF", "Day-to-day")],
                                          [("IL Man", "MIA", "C", "Out")])}
        rows = league_live.to_rows(pull)
        by = {r["player"]: r for r in rows}
        self.assertEqual(by["My Guard"]["slot"], "PG")
        self.assertEqual(by["My Guard"]["fantasy_team"], league_live.MY_TEAM)
        self.assertEqual(by["Bench Man"]["slot"], "BN")
        self.assertEqual(by["Bench Man"]["status"], "Q")
        self.assertEqual(by["IL Man"]["slot"], "IL")

    def test_an_unknown_injury_label_halts_rather_than_guesses(self):
        pull = {"mine": None, "teams": {"T": team("T", [("A Player", "BOS", "PG", True, None, "Suspended")])}}
        with self.assertRaises(league_live.PullError):
            league_live.to_rows(pull)

    def test_the_niederhauser_alias_lands_on_the_unpooled_key(self):
        pull = {"mine": None, "teams": {"T": team("T", [
            ("Yanic Konan Niederhäuser", "PHI", "C", False, "ir", "Out")])}}
        rows = league_live.to_rows(pull)
        self.assertEqual(rows[0]["player"], "Y. Konan Niederhäuser")


def transcript_line(ts, payload):
    """One transcript jsonl line carrying a FantasyBot tool result; ts None leaves the timestamp off."""
    d = {"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "content": [{"type": "text", "text": json.dumps(payload)}]}]}}
    if ts is not None:
        d["timestamp"] = ts
    return json.dumps(d) + "\n"


class SinceGuard(unittest.TestCase):
    """GAUNTLET 2026-10-21 item 7: a persistent runner session keeps every day's pulls in one transcript. With
    --since, only entries at or after the run's start count, so a skipped or partial pull halts instead of
    passing yesterday's rosters off as today's. Without --since, nothing changes."""

    def setUp(self):
        fd, self.tr = tempfile.mkstemp(suffix=".jsonl")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(transcript_line("2026-10-21T12:55:00.250Z", mine([("PG", "Old Guy", "BOS", "PG", None)], [], [])))
            f.write(transcript_line("2026-10-21T12:55:01Z", team("Rival A", [("Old Rival", "BOS", "PG", True, None, None)])))
            f.write(transcript_line("2026-10-22T12:55:00.250Z", mine([("PG", "New Guy", "NYK", "PG", None)], [], [])))
            f.write(transcript_line(None, mine([("PG", "Untimed Guy", "MIA", "PG", None)], [], [])))

    def tearDown(self):
        os.remove(self.tr)

    def names(self, pull):
        return [s["player"]["name"] for s in (pull["mine"] or {}).get("starters", [])]

    def test_without_since_the_latest_in_file_order_wins_as_before(self):
        pull = league_live.extract_pull(self.tr)
        self.assertEqual(self.names(pull), ["Untimed Guy"])
        self.assertIn("Rival A", pull["teams"])

    def test_since_keeps_only_entries_at_or_after_the_run_start(self):
        pull = league_live.extract_pull(self.tr, since="2026-10-22T12:53:00Z")
        self.assertEqual(self.names(pull), ["New Guy"])
        self.assertEqual(pull["teams"], {})  # yesterday's rival pull does not count today

    def test_sub_second_timestamps_compare_as_instants_not_strings(self):
        pull = league_live.extract_pull(self.tr, since="2026-10-22T12:55:00Z")
        self.assertEqual(self.names(pull), ["New Guy"])

    def test_since_after_every_pull_finds_nothing_and_the_check_halts(self):
        pull = league_live.extract_pull(self.tr, since="2026-10-23T00:00:00Z")
        self.assertIsNone(pull["mine"])
        with self.assertRaises(league_live.PullError):
            league_live.check_pull(pull)

    def test_an_unreadable_since_halts(self):
        with self.assertRaises(league_live.PullError):
            league_live.extract_pull(self.tr, since="yesterday")

    def test_the_cli_halts_on_a_stale_only_transcript_and_writes_nothing(self):
        out = os.path.join(tempfile.mkdtemp(), "state.json")
        r = subprocess.run([sys.executable, os.path.join(HERE, "league_live.py"), "--as-of", "2026-10-23",
                            "--transcript", self.tr, "--since", "2026-10-23T00:00:00Z", "--out", out,
                            "--pin-dir", tempfile.mkdtemp()], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("LEAGUE LIVE: HALT", r.stdout)
        self.assertFalse(os.path.exists(out))


class PullChecks(unittest.TestCase):
    def test_a_wrong_league_name_halts(self):
        bad = team("T", [])
        bad["leagueName"] = "SOME OTHER LEAGUE"
        with self.assertRaises(league_live.PullError):
            league_live.check_pull({"mine": None, "teams": {"T": bad}})

    def test_fewer_than_twelve_teams_halts(self):
        pull = {"mine": mine([], [], []), "teams": {f"T{i}": team(f"T{i}", []) for i in range(5)}}
        with self.assertRaises(league_live.PullError):
            league_live.check_pull(pull)


class EndToEnd(unittest.TestCase):
    def test_todays_transcript_builds_a_passing_state_without_overwriting(self):
        """The real pull from this session's transcript resolves 12 teams; written to a scratch path."""
        tdir = tempfile.mkdtemp()
        out = os.path.join(tdir, "league_state.json")
        p = subprocess.run([sys.executable, os.path.join(HERE, "league_live.py"),
                            "--as-of", "2026-10-20", "--out", out,
                            "--pin-dir", tdir], capture_output=True, text=True)
        self.assertIn("LEAGUE INTAKE: PASS", p.stdout, p.stdout + p.stderr)
        self.assertIn("LEAGUE LIVE: PASS", p.stdout, p.stdout + p.stderr)
        state = json.load(open(out, encoding="utf-8"))
        self.assertEqual(len(state["teams"]), 12)
        self.assertIn("fantasybot", state["sources"])
        pin = os.path.join(tdir, "pull_2026-10-20.json")
        self.assertTrue(os.path.exists(pin), "raw pull not pinned")


if __name__ == "__main__":
    unittest.main()
