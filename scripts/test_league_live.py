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
                            "--as-of", "2026-10-20", "--out", out, "--source", "fantasybot",
                            "--pin-dir", tdir], capture_output=True, text=True)
        self.assertIn("LEAGUE INTAKE: PASS", p.stdout, p.stdout + p.stderr)
        self.assertIn("LEAGUE LIVE: PASS", p.stdout, p.stdout + p.stderr)
        state = json.load(open(out, encoding="utf-8"))
        self.assertEqual(len(state["teams"]), 12)
        self.assertIn("fantasybot", state["sources"])
        pin = os.path.join(tdir, "pull_2026-10-20.json")
        self.assertTrue(os.path.exists(pin), "raw pull not pinned")


class FlaimFirst(unittest.TestCase):
    """Owner 2026-10-21 ("Build A, B, C, D"): rosters come from Flaim (every team's Yahoo slot and status letter);
    FantasyBot is the fallback when the Flaim pull is missing or incomplete."""
    PIN = os.path.join(os.path.dirname(HERE), "data", "source", "flaim", "pull_2026-10-21.json")

    def run_live(self, *args):
        tdir = tempfile.mkdtemp()
        out = os.path.join(tdir, "league_state.json")
        p = subprocess.run([sys.executable, os.path.join(HERE, "league_live.py"), "--as-of", "2026-10-21", "--out", out,
                            "--pin-dir", tdir, "--flaim-pin-dir", tdir] + list(args), capture_output=True, text=True)
        return p, out, tdir

    @unittest.skipUnless(os.path.exists(PIN), "no pinned Flaim pull")
    def test_the_pinned_pull_halts_on_the_one_unpooled_active_player_and_writes_nothing(self):
        # 2026-10-21: Andre Drummond (Podz save the league, BN) has no pool row; whether to add one or carry him as
        # not counted is the owner's decision, so the intake's existing halt stands
        p, out, tdir = self.run_live("--source", "flaim", "--pull", self.PIN)
        self.assertIn("Andre Drummond", p.stdout)
        self.assertIn("LEAGUE LIVE: HALT", p.stdout)
        self.assertFalse(os.path.exists(out))

    @unittest.skipUnless(os.path.exists(PIN), "no pinned Flaim pull")
    def test_the_pinned_flaim_pull_builds_every_team_with_yahoo_slots_and_letters(self):
        pull = json.load(open(self.PIN, encoding="utf-8"))
        for r in pull["rosters"].values():
            r["players"] = [pl for pl in r["players"] if pl["name"] != "Andre Drummond"]
        fd, pin = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(pull, f)
        p, out, tdir = self.run_live("--source", "flaim", "--pull", pin)
        self.assertIn("LEAGUE LIVE: PASS — rosters from Flaim", p.stdout, p.stdout + p.stderr)
        state = json.load(open(out, encoding="utf-8"))
        self.assertEqual(len(state["teams"]), 12)
        self.assertIn("flaim", state["sources"])
        slots = {pl["slot"] for t in state["teams"] if t["seat"] != 10 for pl in t["players"]}
        self.assertTrue(slots - {"BN", "IL"}, "rival teams carry only BN/IL: Yahoo slots were lost")
        porter = [pl for t in state["teams"] for pl in t["players"] if pl["player"] == "Kevin Porter Jr."]
        self.assertEqual([pl["status"] for pl in porter], ["NA"])

    def test_an_incomplete_flaim_pull_falls_back_to_fantasybot_and_says_so(self):
        fd, tr = tempfile.mkstemp(suffix=".jsonl")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(transcript_line("2026-10-22T12:55:00Z", mine([("PG", "Old Guy", "BOS", "PG", None)], [], [])))
        p, out, tdir = self.run_live("--transcript", tr)
        self.assertIn("Flaim pull not used", p.stdout, p.stdout)
        self.assertIn("LEAGUE LIVE: HALT", p.stdout, p.stdout)  # the FantasyBot fallback is incomplete too
        self.assertFalse(os.path.exists(out))

    def test_a_flaim_pull_without_twelve_rosters_still_pins_its_matchup_and_list_for_the_week_card(self):
        import test_flaim_live as TFL
        fd, tr = tempfile.mkstemp(suffix=".jsonl")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            for i in range(1, 12):
                f.write(TFL.line("2026-10-22T12:55:00Z", TFL.roster(i, f"T{i}", [("A", "BOS", "PG", "PG", None)])))
            f.write(TFL.line("2026-10-22T12:55:30Z", TFL.matchups(1, [(TFL.side(1, "T1", 1, 1, 1, 1, (0,) * 7, 1),
                                                                        TFL.side(2, "T2", 1, 1, 1, 1, (0,) * 7, 1))])))
        p, out, tdir = self.run_live("--transcript", tr)
        self.assertIn("Flaim pull not used", p.stdout, p.stdout)
        pinned = json.load(open(os.path.join(tdir, "pull_2026-10-21.json"), encoding="utf-8"))
        self.assertEqual((pinned["source"], sorted(pinned["matchups"])), ("flaim", ["1"]))


if __name__ == "__main__":
    unittest.main()
