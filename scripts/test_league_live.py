#!/usr/bin/env python3
"""Red-first tests for league_live.py (owner 2026-10-20: "Build all 3"): the FantasyBot pull
to league_state.json, through league_intake's name checks, with a halt instead of a bad write."""
import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import league_live  # noqa: E402
import league_intake as LI  # noqa: E402


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

    def test_questionable_maps_to_q(self):
        # the runner's 10/21 re-run (owner go, #157): FantasyBot's 'Questionable' on Deni Avdija, Yahoo's 'Q' via Flaim
        # the same day. The mapping shipped in #157 without a test; this one pins it (green from the start).
        pull = {"mine": None, "teams": {"T": team("T", [("A Player", "POR", "SF", True, None, "Questionable")])}}
        self.assertEqual(league_live.to_rows(pull)[0]["status"], "Q")

    def test_doubtful_maps_to_d(self):
        # owner 2026-10-21: "Stewart's 'D' means 'Doubtful'" (status_feed.TIERS D, 0.25, D-IS-10) and, clicked the same
        # evening, "0.25 + add mapping": FantasyBot's spelling of the same status lands on Yahoo's letter
        pull = {"mine": None, "teams": {"T": team("T", [("A Player", "DET", "PF", True, None, "Doubtful")])}}
        self.assertEqual(league_live.to_rows(pull)[0]["status"], "D")

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
                            "--pin-dir", tempfile.mkdtemp(), "--ledger", ""], capture_output=True, text=True)
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
    """The whole path from a transcript to a passing state, on a fixture transcript (2026-10-26: until now this read
    this session's live transcript through newest_transcript(), so it failed in every checkout but the one it was
    written in). The pinned 10/21 Flaim pull is carried as the tool results of a transcript line each."""
    PIN = os.path.join(os.path.dirname(HERE), "data", "source", "flaim", "pull_2026-10-21.json")

    @unittest.skipUnless(os.path.exists(PIN), "no pinned Flaim pull")
    def test_a_fixture_transcript_builds_a_passing_state_and_pins_the_pull(self):
        import test_flaim_live as TFL
        pull = json.load(open(self.PIN, encoding="utf-8"))
        fd, tr = tempfile.mkstemp(suffix=".jsonl")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            for r in pull["rosters"].values():
                f.write(TFL.line("2026-10-21T12:55:00Z", {"success": True, "data": r}))
            for m in pull["matchups"].values():
                f.write(TFL.line("2026-10-21T12:55:30Z", {"success": True, "data": m}))
            if pull.get("free_agents"):
                f.write(TFL.line("2026-10-21T12:55:40Z", {"success": True, "data": pull["free_agents"]}))
        tdir = tempfile.mkdtemp()
        out = os.path.join(tdir, "league_state.json")
        p = subprocess.run([sys.executable, os.path.join(HERE, "league_live.py"), "--as-of", "2026-10-21", "--out", out,
                            "--transcript", tr, "--since", "2026-10-21T12:50:00Z", "--pin-dir", tdir, "--flaim-pin-dir", tdir,
                            "--ledger", ""], capture_output=True, text=True)
        self.assertIn("LEAGUE LIVE: PASS — rosters from Flaim", p.stdout, p.stdout + p.stderr)
        state = json.load(open(out, encoding="utf-8"))
        self.assertEqual(len(state["teams"]), 12)
        self.assertIn("flaim", state["sources"])
        self.assertTrue(os.path.exists(os.path.join(tdir, "pull_2026-10-21.json")), "raw pull not pinned")
        os.remove(tr)


class FlaimFirst(unittest.TestCase):
    """Owner 2026-10-21 ("Build A, B, C, D"): rosters come from Flaim (every team's Yahoo slot and status letter);
    FantasyBot is the fallback when the Flaim pull is missing or incomplete."""
    PIN = os.path.join(os.path.dirname(HERE), "data", "source", "flaim", "pull_2026-10-21.json")

    def run_live(self, *args, tdir=None):
        tdir = tdir or tempfile.mkdtemp()
        out = os.path.join(tdir, "league_state.json")
        # --ledger '' : a test run leaves no row in the kit's run-ledger (2026-10-23; standalone runs record by default
        # since D5, and the suite was appending a league_live row to report/run-ledger.jsonl on every run)
        p = subprocess.run([sys.executable, os.path.join(HERE, "league_live.py"), "--as-of", "2026-10-21", "--out", out,
                            "--pin-dir", tdir, "--flaim-pin-dir", tdir, "--ledger", ""] + list(args), capture_output=True, text=True)
        return p, out, tdir

    @unittest.skipUnless(os.path.exists(PIN), "no pinned Flaim pull")
    def test_the_pinned_pull_builds_every_team_with_yahoo_slots_letters_and_drummond(self):
        # owner 2026-10-21 option (b): Drummond's row lives in the kit's data/pool_additions.csv, so the real 10/21 pull
        # builds all twelve teams with him on Podz save the league's bench whatever the deck pool beside the kit carries
        # (before the additions file it halted on his name against deck main)
        p, out, tdir = self.run_live("--source", "flaim", "--pull", self.PIN)
        self.assertIn("LEAGUE LIVE: PASS — rosters from Flaim", p.stdout, p.stdout + p.stderr)
        state = json.load(open(out, encoding="utf-8"))
        self.assertEqual(len(state["teams"]), 12)
        self.assertIn("flaim", state["sources"])
        slots = {pl["slot"] for t in state["teams"] if t["seat"] != 10 for pl in t["players"]}
        self.assertTrue(slots - {"BN", "IL"}, "rival teams carry only BN/IL: Yahoo slots were lost")
        porter = [pl for t in state["teams"] for pl in t["players"] if pl["player"] == "Kevin Porter Jr."]
        self.assertEqual([pl["status"] for pl in porter], ["NA"])
        drummond = [(t["name"], pl["slot"]) for t in state["teams"] for pl in t["players"] if pl["player"] == "Andre Drummond"]
        self.assertEqual(drummond, [("Podz save the league", "BN")])

    @unittest.skipUnless(os.path.exists(PIN), "no pinned Flaim pull")
    def test_a_second_run_for_the_same_date_keeps_the_dated_lineups_the_first_pinned(self):
        # owner 2026-10-22 ("Read daily rosters"): the afternoon check runs league live for the morning's date with no
        # dated lineup in its pull; the week card reads the morning's lineups from this file on later days
        tdir = tempfile.mkdtemp()
        morning = json.load(open(self.PIN, encoding="utf-8"))
        team = sorted(morning["rosters"])[0]
        morning["daily"] = {team: {"2026-10-20": dict(morning["rosters"][team], snapshot={"type": "date", "date": "2026-10-20"})}}
        with open(os.path.join(tdir, "pull_2026-10-21.json"), "w", encoding="utf-8") as f:
            json.dump(morning, f)
        p, out, _ = self.run_live("--source", "flaim", "--pull", self.PIN, tdir=tdir)
        self.assertIn("LEAGUE LIVE: PASS", p.stdout, p.stdout + p.stderr)
        pinned = json.load(open(os.path.join(tdir, "pull_2026-10-21.json"), encoding="utf-8"))
        self.assertEqual({t: sorted(d) for t, d in (pinned.get("daily") or {}).items()}, {team: ["2026-10-20"]})

    @unittest.skipUnless(os.path.exists(PIN), "no pinned Flaim pull")
    def test_an_active_player_with_no_pool_row_is_carried_unpooled_and_named(self):
        # owner 2026-10-26, option (a) (replaces the halt this test asserted until then): a rostered, non-IL name the
        # pool lacks is carried as `unpooled`, named on the LEAGUE LIVE line, and the state is written
        pull = json.load(open(self.PIN, encoding="utf-8"))
        team = sorted(pull["rosters"])[7]
        pull["rosters"][team]["players"].append(dict(name="Not A Pool Player", playerKey="478.p.999999", team="NYK",
                                                     position="C", selectedPosition="BN"))
        fd, pin = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(pull, f)
        p, out, tdir = self.run_live("--source", "flaim", "--pull", pin)
        self.assertIn("LEAGUE INTAKE: WARN", p.stdout)
        self.assertIn("LEAGUE LIVE: PASS", p.stdout)
        self.assertIn("1 not in the pool, not simulated: Not A Pool Player", p.stdout)
        st = json.load(open(out, encoding="utf-8"))
        self.assertEqual([u["player"] for u in st["unpooled"]], ["Not A Pool Player"])
        self.assertNotIn("Not A Pool Player", [q["player"] for t in st["teams"] for q in t["players"]])

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

    def test_a_flaim_pull_without_twelve_rosters_still_pins_its_dated_lineups_for_the_week_card(self):
        # owner 2026-10-22 ("Read daily rosters"): a past day's lineup is pinned even when today's rosters fall short
        import test_flaim_live as TFL
        fd, tr = tempfile.mkstemp(suffix=".jsonl")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            for i in range(1, 12):
                f.write(TFL.line("2026-10-22T12:55:00Z", TFL.roster(i, f"T{i}", [("A", "BOS", "PG", "PG", None)])))
            f.write(TFL.line("2026-10-22T12:55:30Z", TFL.roster(11, "T11", [("A", "BOS", "PG", "PG", None)], snapshot="2026-10-20")))
        p, out, tdir = self.run_live("--transcript", tr)
        self.assertIn("Flaim pull not used", p.stdout, p.stdout)
        pinned = json.load(open(os.path.join(tdir, "pull_2026-10-21.json"), encoding="utf-8"))
        self.assertEqual({t: sorted(d) for t, d in pinned["daily"].items()}, {f"{TFL.KEY}.t.11": ["2026-10-20"]})



class Phases(unittest.TestCase):
    """Owner 2026-10-26, option 1A with the am baseline: the afternoon never overwrites the morning's record, and a
    morning re-run after an afternoon run still diffs overnight (the 10/25 defect: d887553 then 13597a2)."""
    PIN = os.path.join(HERE, "..", "data", "source", "flaim", "pull_2026-10-26.json")

    def state(self, as_of, teams):
        return {"as_of": as_of, "sources": {}, "unpooled_il": {}, "unpooled": [], "standings": None, "scoreboard": None,
                "teams": teams, "nba_team_disagreements": []}

    def team(self, name, seat, players):
        return {"name": name, "seat": seat, "manager": "M", "players": [dict(player=p, yahoo_name=p, slot="BN",
                yahoo_nba_team="DEN", pool_team="DEN", positions=["PF"], status=None) for p in players],
                "empty_slots": [], "unpooled_il": [], "unpooled": []}

    def test_am_writes_the_baseline_copy_and_pm_writes_only_its_own_record(self):
        import json, tempfile
        d = tempfile.mkdtemp(); news = os.path.join(d, "news"); os.makedirs(news)
        st = os.path.join(d, "league_state.json")
        yday = self.state("2026-10-25", [self.team("A", 1, ["X"])])
        json.dump(yday, open(st, "w"))
        morning = self.state("2026-10-26", [self.team("A", 1, ["Y"])])
        rec, out = league_live.record_moves(yday, morning, "2026-10-26", "am", news)
        self.assertTrue(out.endswith("league_moves_2026-10-26.json"))
        self.assertTrue(os.path.exists(os.path.join(news, "league_state_am_2026-10-26.json")))
        before = open(out, "rb").read()
        afternoon = self.state("2026-10-26", [self.team("A", 1, ["Z"])])
        rec2, out2 = league_live.record_moves(morning, afternoon, "2026-10-26", "pm", news)
        self.assertTrue(out2.endswith("league_moves_2026-10-26_pm.json"))
        self.assertEqual(open(out, "rb").read(), before)                 # the morning record is untouched
        self.assertFalse(os.path.exists(os.path.join(news, "league_state_am_2026-10-26_pm.json")))

    def test_a_morning_rerun_after_the_afternoon_still_diffs_overnight(self):
        import json, tempfile
        d = tempfile.mkdtemp(); news = os.path.join(d, "news"); os.makedirs(news)
        yday = self.state("2026-10-25", [self.team("A", 1, ["X"])])
        league_live.record_moves(self.state("2026-10-24", [self.team("A", 1, ["W"])]), yday, "2026-10-25", "am", news)
        morning = self.state("2026-10-26", [self.team("A", 1, ["Y"])])
        league_live.record_moves(yday, morning, "2026-10-26", "am", news)
        afternoon = self.state("2026-10-26", [self.team("A", 1, ["Z"])])
        league_live.record_moves(morning, afternoon, "2026-10-26", "pm", news)
        # the re-run's "old" state on disk is now the afternoon's; the am baseline must win
        base = league_live.am_baseline("2026-10-26", news, afternoon)
        self.assertEqual(base["as_of"], "2026-10-25")
        self.assertEqual([p["player"] for p in base["teams"][0]["players"]], ["X"])
        rec, out = league_live.record_moves(base, morning, "2026-10-26", "am", news)
        self.assertEqual((rec["old_as_of"], rec["new_as_of"]), ("2026-10-25", "2026-10-26"))

    def test_no_baseline_falls_back_to_the_state_on_disk(self):
        import tempfile
        d = tempfile.mkdtemp(); news = os.path.join(d, "news"); os.makedirs(news)
        cur = self.state("2026-10-26", [self.team("A", 1, ["Y"])])
        self.assertIs(league_live.am_baseline("2026-10-26", news, cur), cur)

class AfternoonPin(unittest.TestCase):
    """Owner 2026-10-29 ("Fix like #225"): the 3 PM run pins its pull and roster transcription under _pm names, so the
    morning's pull_<date>.json stays as the morning records hashed it; the afternoon pin starts from the morning's."""
    def test_the_morning_and_afternoon_pin_to_different_files(self):
        am = league_live.pin_paths("/p", "2026-10-29", "am")
        pm = league_live.pin_paths("/p", "2026-10-29", "pm")
        self.assertEqual(am, (os.path.join("/p", "pull_2026-10-29.json"), os.path.join("/p", "rosters_2026-10-29.transcribed.csv"),
                              os.path.join("/p", "pull_2026-10-29.json")))
        self.assertEqual(pm, (os.path.join("/p", "pull_2026-10-29_pm.json"), os.path.join("/p", "rosters_2026-10-29_pm.transcribed.csv"),
                              os.path.join("/p", "pull_2026-10-29.json")))


if __name__ == "__main__":
    unittest.main()


class LedgerRow(unittest.TestCase):
    """Owner 2026-10-23 (D5): a standalone league_live.py run records its verdict (here a HALT on a missing pull)."""
    def test_a_halt_run_alone_records_a_fail_row(self):
        d = tempfile.mkdtemp(); led = os.path.join(d, "ledger.jsonl")
        env = {k: v for k, v in os.environ.items() if k != "KIT_LEDGER_PARENT"}
        p = subprocess.run([sys.executable, os.path.join(HERE, "league_live.py"), "--as-of", "2026-10-23", "--pull",
                            os.path.join(d, "missing.json"), "--out", os.path.join(d, "state.json"), "--ledger", led],
                           capture_output=True, text=True, env=env)
        self.assertNotEqual(p.returncode, 0)
        rows = [json.loads(l) for l in open(led)]
        self.assertEqual([(r["name"], r["verdict"]) for r in rows], [("league_live", "FAIL")])
