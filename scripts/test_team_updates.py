#!/usr/bin/env python3
"""Red-first tests for scripts/team_updates.py (owner 2026-11-11, runner after-report pick D3, "Team-update path"):
a pooled player's NBA team changes only when Yahoo's roster pull and an ESPN transactions item agree on the move.
Known answers: Nique Clifford SAC -> OKC (ESPN item of 2026-11-08); a Yahoo-only mismatch stays a disagreement; an
ESPN item alone changes nothing.

    python3 scripts/test_team_updates.py
"""
import contextlib
import csv
import io
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import team_updates as TU  # noqa: E402
import league_intake as LI  # noqa: E402
import season_lines as SL  # noqa: E402

TRADE = dict(date="2026-11-08", nba_team="SAC", description="Traded G Nique Clifford to the Oklahoma City Thunder.", player="Nique Clifford")
DIS = [dict(player="Nique Clifford", yahoo="OKC", pool="SAC")]
NAMES = TU.team_names()


class Names(unittest.TestCase):
    def test_the_pinned_espn_list_gives_thirty_clubs_in_pool_codes(self):
        self.assertEqual(len(NAMES), 30)
        self.assertEqual(NAMES["oklahoma city thunder"], "OKC")
        self.assertEqual(NAMES["golden state warriors"], "GSW")     # ESPN says GS
        self.assertEqual(NAMES["utah jazz"], "UTA"); self.assertEqual(NAMES["la clippers"], "LAC")


class Destination(unittest.TestCase):
    def test_a_trade_names_its_destination_in_words(self):
        self.assertEqual(TU.destination(TRADE, NAMES), "OKC")

    def test_an_acquiring_clubs_item_is_that_club(self):
        self.assertEqual(TU.destination(dict(nba_team="OKC", description="Acquired G Nique Clifford from the Sacramento Kings."), NAMES), "OKC")
        self.assertEqual(TU.destination(dict(nba_team="GS", description="Signed F Some Player."), NAMES), "GSW")
        self.assertEqual(TU.destination(dict(nba_team="OKC", description="Claimed G Some Player off waivers."), NAMES), "OKC")

    def test_a_trade_with_a_return_named_after_the_club_still_reads_the_club(self):
        t = dict(nba_team="SAC", description="Traded G Nique Clifford to the Oklahoma City Thunder for a 2028 second-round pick.")
        self.assertEqual(TU.destination(t, NAMES, player="Nique Clifford"), "OKC")
        t = dict(nba_team="SAC", description="Traded G Nique Clifford to the Oklahoma City Thunder in exchange for F Some Player.")
        self.assertEqual(TU.destination(t, NAMES, player="Nique Clifford"), "OKC")

    def test_a_player_named_as_the_return_is_not_read_as_leaving(self):
        # he is what the listing club got back: the "to the <club>" is where the other piece went
        t = dict(nba_team="OKC", description="Traded F Some Player to the Sacramento Kings for G Nique Clifford.")
        self.assertIsNone(TU.destination(t, NAMES, player="Nique Clifford"))
        self.assertEqual(TU.destination(t, NAMES, player="Some Player"), "SAC")

    def test_an_accented_or_punctuated_name_still_matches(self):
        t = dict(nba_team="DAL", description="Traded G Luka Dončić to the Los Angeles Lakers.")
        self.assertEqual(TU.destination(t, NAMES, player="Luka Doncic"), "LAL")
        t = dict(nba_team="SAC", description="Traded F P.J. Washington Jr. to the Utah Jazz.")
        self.assertEqual(TU.destination(t, NAMES, player="PJ Washington"), "UTA")

    def test_wording_that_names_no_arrival_gives_none(self):
        for text in ("Waived G Nique Clifford.", "Recalled G Nique Clifford from the Oklahoma City Blue.",
                     "Traded G Nique Clifford to the Springfield Isotopes.", "Placed G Nique Clifford on the injured list.", ""):
            self.assertIsNone(TU.destination(dict(nba_team="SAC", description=text), NAMES), text)


class Decide(unittest.TestCase):
    def test_both_sources_agree_the_team_changes(self):
        c = TU.decide(DIS, [TRADE], NAMES)
        self.assertEqual(len(c), 1)
        self.assertEqual((c[0]["player"], c[0]["from"], c[0]["to"]), ("Nique Clifford", "SAC", "OKC"))
        self.assertEqual(c[0]["espn"]["date"], "2026-11-08"); self.assertIn("Oklahoma City Thunder", c[0]["espn"]["description"])

    def test_yahoo_alone_changes_nothing(self):
        self.assertEqual(TU.decide(DIS, [], NAMES), [])
        other = dict(TRADE, player="Somebody Else", description="Traded G Somebody Else to the Oklahoma City Thunder.")
        self.assertEqual(TU.decide(DIS, [other], NAMES), [])

    def test_espn_alone_changes_nothing(self):
        self.assertEqual(TU.decide([], [TRADE], NAMES), [])                       # Yahoo still shows the old club: no disagreement

    def test_the_two_must_name_the_same_club(self):
        self.assertEqual(TU.decide([dict(player="Nique Clifford", yahoo="DAL", pool="SAC")], [TRADE], NAMES), [])

    def test_a_reverted_change_is_not_made_again(self):
        self.assertEqual(TU.decide(DIS, [TRADE], NAMES, held={("Nique Clifford", "OKC")}), [])

    def test_the_newest_item_is_the_receipt(self):
        old = dict(TRADE, date="2026-11-01", description="Traded G Nique Clifford to the Oklahoma City Thunder. (earlier)")
        self.assertEqual(TU.decide(DIS, [old, TRADE], NAMES)[0]["espn"]["date"], "2026-11-08")


class Ledger(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.p = os.path.join(self.d, "team_changes.jsonl")

    def test_no_file_is_no_change(self):
        self.assertEqual(TU.current(TU.read(self.p)), {}); self.assertEqual(TU.held(TU.read(self.p)), set())

    def test_rows_append_and_the_newest_wins(self):
        c = TU.decide(DIS, [TRADE], NAMES)[0]
        r1 = TU.append(self.p, [TU.row(c, "2026-11-11", dict(file="pull.json", sha256="abc"), TU.read(self.p))])
        self.assertEqual(r1[0]["id"], "T-2026-11-11-01")
        self.assertEqual(TU.current(TU.read(self.p)), {"Nique Clifford": "OKC"})
        row = TU.read(self.p)[0]
        self.assertEqual(row["yahoo"], dict(file="pull.json", sha256="abc", team="OKC"))
        self.assertEqual(row["rule"], TU.RULE)

    def test_a_revert_restores_the_pool_team_and_holds_the_change(self):
        c = TU.decide(DIS, [TRADE], NAMES)[0]
        TU.append(self.p, [TU.row(c, "2026-11-11", dict(file="pull.json", sha256="abc"), [])])
        rv = TU.revert_row(TU.read(self.p), "Nique Clifford", "2026-11-12", "owner: wrong player matched")
        TU.append(self.p, [rv])
        self.assertEqual(TU.current(TU.read(self.p)), {})
        self.assertEqual(TU.held(TU.read(self.p)), {("Nique Clifford", "OKC")})
        self.assertEqual(len(TU.read(self.p)), 2)                                  # append-only: both rows stay
        with self.assertRaises(TU.TeamUpdateError):
            TU.revert_row(TU.read(self.p), "Nobody", "2026-11-12", "x")

    def test_overlay_changes_only_the_named_players(self):
        self.assertEqual(TU.overlay({"Nique Clifford": "SAC", "Other": "DAL"}, {"Nique Clifford": "OKC"}),
                         {"Nique Clifford": "OKC", "Other": "DAL"})


class EspnItems(unittest.TestCase):
    def test_items_come_from_the_transactions_files_in_the_lookback(self):
        d = tempfile.mkdtemp()
        def tx(date, hits):
            json.dump(dict(date=date, hits=hits), open(os.path.join(d, f"transactions_{date}.json"), "w"))
        tx("2026-11-10", [TRADE]); tx("2026-11-09", [TRADE]); tx("2026-10-20", [dict(TRADE, player="Old News")]); tx("2026-11-12", [dict(TRADE, player="Tomorrow")])
        items = TU.espn_items(d, "2026-11-11")
        self.assertEqual([i["player"] for i in items], ["Nique Clifford"])          # one item, not one per file
        self.assertEqual(items[0]["file"], "transactions_2026-11-10.json")          # the newest file that carries it
        self.assertEqual(TU.LOOKBACK_DAYS, 14)
        self.assertEqual(TU.espn_items(os.path.join(d, "none"), "2026-11-11"), [])


POOL = [{"player": "Nique Clifford", "team": "SAC"}, {"player": "Nikola Jokic", "team": "DEN"}, {"player": "Tyrese Haliburton", "team": "IND"}]
HEAD = ["fantasy_team", "page", "slot", "player", "nba_team", "positions", "status"]


class Intake(unittest.TestCase):
    """The roster intake makes the change and clears the flag, with receipts, and never twice."""
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.news = os.path.join(self.d, "news"); os.makedirs(self.news)
        self.ledger = os.path.join(self.d, "team_changes.jsonl"); self.out = os.path.join(self.d, "state.json")

    def roster(self, clifford_team):
        p = os.path.join(self.d, "t.csv")
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(HEAD)
            w.writerows([["A", 1, "PG", "Tyrese Haliburton", "IND", "PG", ""], ["B", 1, "C", "Nikola Jokic", "DEN", "C", ""],
                         ["B", 1, "G", "Nique Clifford", clifford_team, "SG", ""]])
        return p

    def espn(self, hits, date="2026-11-10"):
        json.dump(dict(date=date, hits=hits), open(os.path.join(self.news, f"transactions_{date}.json"), "w"))

    def run_intake(self, team, as_of="2026-11-11"):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = LI.run(self.roster(team), self.out, POOL, {}, draft={10: ["Tyrese Haliburton"], 1: ["Nikola Jokic"]}, as_of=as_of,
                        sources={"flaim": {"pull_file": "data/source/flaim/pull_2026-11-11.json", "pull_sha256": "f" * 64}},
                        team_ledger=self.ledger, news_dir=self.news)
        self.assertEqual(rc, 0, buf.getvalue())
        return json.load(open(self.out)), buf.getvalue()

    def clifford(self, st):
        return next(p for t in st["teams"] for p in t["players"] if p["player"] == "Nique Clifford")

    def test_clifford_becomes_okc_and_the_flag_clears(self):
        self.espn([TRADE])
        st, out = self.run_intake("OKC")
        self.assertEqual(st["nba_team_disagreements"], [])
        self.assertEqual(self.clifford(st)["pool_team"], "OKC")
        self.assertEqual([(u["player"], u["from"], u["to"]) for u in st["team_updates"]], [("Nique Clifford", "SAC", "OKC")])
        row = TU.read(self.ledger)[0]
        self.assertEqual(row["yahoo"], dict(file="data/source/flaim/pull_2026-11-11.json", sha256="f" * 64, team="OKC"))
        self.assertEqual((row["espn"]["date"], row["espn"]["file"]), ("2026-11-08", "transactions_2026-11-10.json"))
        self.assertIn("Traded G Nique Clifford to the Oklahoma City Thunder", row["espn"]["description"])
        self.assertIn("1 team update (Nique Clifford SAC to OKC)", out)

    def test_a_second_run_keeps_the_team_and_writes_no_second_row(self):
        self.espn([TRADE])
        self.run_intake("OKC"); st, out = self.run_intake("OKC", as_of="2026-11-12")
        self.assertEqual(st["nba_team_disagreements"], []); self.assertEqual(self.clifford(st)["pool_team"], "OKC")
        self.assertEqual(len(TU.read(self.ledger)), 1); self.assertEqual(st["team_updates"], [])

    def test_yahoo_only_stays_a_disagreement(self):
        st, _ = self.run_intake("OKC")
        self.assertEqual(st["nba_team_disagreements"], DIS); self.assertEqual(self.clifford(st)["pool_team"], "SAC")
        self.assertFalse(os.path.exists(self.ledger))

    def test_espn_only_makes_no_change(self):
        self.espn([TRADE])
        st, _ = self.run_intake("SAC")
        self.assertEqual(st["nba_team_disagreements"], []); self.assertEqual(self.clifford(st)["pool_team"], "SAC")
        self.assertFalse(os.path.exists(self.ledger))

    def test_without_a_ledger_path_the_intake_is_as_before(self):
        self.espn([TRADE])
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            LI.run(self.roster("OKC"), self.out, POOL, {}, draft={10: ["Tyrese Haliburton"], 1: ["Nikola Jokic"]}, as_of="2026-11-11")
        st = json.load(open(self.out))
        self.assertEqual(st["nba_team_disagreements"], DIS); self.assertNotIn("team_updates", st)

    def test_a_reverted_change_is_flagged_again_and_not_remade(self):
        self.espn([TRADE]); self.run_intake("OKC")
        TU.append(self.ledger, [TU.revert_row(TU.read(self.ledger), "Nique Clifford", "2026-11-12", "owner")])
        st, _ = self.run_intake("OKC", as_of="2026-11-12")
        self.assertEqual(st["nba_team_disagreements"], DIS); self.assertEqual(len(TU.read(self.ledger)), 2)


class SeasonFiles(unittest.TestCase):
    """The season pool and projections files carry the changed team; no stat cell moves."""
    def run_lines(self, ledger):
        d = tempfile.mkdtemp()
        kit = os.path.join(d, "kit.csv"); deck = os.path.join(d, "deck.csv")
        kf = ["name", "team", "pos", "gp", "mpg", "fgp", "fga", "ftp", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]
        df = ["player", "team", "pos", "fg_pct", "fga", "ft_pct", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov", "note"]
        with open(kit, "w", newline="") as f:
            w = csv.writer(f); w.writerow(kf)
            w.writerow(["Nique Clifford", "SAC", "SF,SG", 74, 25.1, 0.418, 7.9, 0.722, 1.3, 1.0, 8.6, 3.8, 2.4, 0.9, 0.3, 1.5])
            w.writerow(["Nikola Jokic", "DEN", "C", 70, 34, 0.55, 17, 0.83, 6, 1.4, 26, 12, 10, 1.6, 1.0, 3.3])
        with open(deck, "w", newline="") as f:
            w = csv.writer(f); w.writerow(df)
            w.writerow(["Nique Clifford", "SAC", "SG,SF", 0.418, 7.9, 0.722, 1.3, 1.0, 8.6, 3.8, 2.4, 0.9, 0.3, 1.5, ""])
            w.writerow(["Nikola Jokic", "DEN", "C", 0.55, 17, 0.83, 6, 1.4, 26, 12, 10, 1.6, 1.0, 3.3, ""])
        out = os.path.join(d, "out")
        rec = SL.run("2026-11-11", [], kit_csv=kit, deck_csv=deck, out_dir=out, team_ledger=ledger)
        rd = lambda n: list(csv.DictReader(open(os.path.join(out, n))))
        return rec, rd("projections_season.csv"), rd("pool_season.csv")

    def test_the_team_column_follows_the_ledger_and_nothing_else_moves(self):
        d = tempfile.mkdtemp(); ledger = os.path.join(d, "team_changes.jsonl")
        rec0, kit0, deck0 = self.run_lines(ledger)                    # no ledger file yet
        self.assertEqual((kit0[0]["team"], deck0[0]["team"]), ("SAC", "SAC")); self.assertEqual(rec0["team_updates"], [])
        TU.append(ledger, [TU.row(TU.decide(DIS, [TRADE], NAMES)[0], "2026-11-11", dict(file="p", sha256="s"), [])])
        rec, kit, deck = self.run_lines(ledger)
        self.assertEqual((kit[0]["team"], deck[0]["team"]), ("OKC", "OKC"))
        self.assertEqual((kit[1]["team"], deck[1]["team"]), ("DEN", "DEN"))
        strip = lambda rows: [{k: v for k, v in r.items() if k != "team"} for r in rows]
        self.assertEqual(strip(kit), strip(kit0)); self.assertEqual(strip(deck), strip(deck0))
        self.assertEqual(rec["team_updates"], [dict(player="Nique Clifford", team="OKC")])

    def test_the_command_line_default_is_the_kits_ledger(self):
        import inspect
        self.assertEqual(inspect.signature(SL.run).parameters["team_ledger"].default, None)
        self.assertTrue(TU.LEDGER.endswith(os.path.join("data", "team_changes.jsonl")))


class Wiring(unittest.TestCase):
    def test_the_live_roster_step_and_the_intake_command_pass_the_ledger(self):
        for fn in ("league_live.py", "league_intake.py", "season_lines.py"):
            src = open(os.path.join(HERE, fn), encoding="utf-8").read()
            self.assertIn("team_updates.LEDGER", src, fn)

    def test_the_command_lists_and_reverts(self):
        d = tempfile.mkdtemp(); p = os.path.join(d, "team_changes.jsonl")
        TU.append(p, [TU.row(TU.decide(DIS, [TRADE], NAMES)[0], "2026-11-11", dict(file="p", sha256="s"), [])])
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(TU.main(["--ledger", p, "--list"]), 0)
            self.assertEqual(TU.main(["--ledger", p, "--revert", "Nique Clifford", "--note", "test", "--date", "2026-11-12"]), 0)
            self.assertEqual(TU.main(["--ledger", p, "--revert", "Nobody", "--note", "test"]), 1)
        self.assertIn("Nique Clifford: SAC to OKC", buf.getvalue()); self.assertIn("TEAM UPDATES: HALT", buf.getvalue())
        self.assertEqual(TU.current(TU.read(p)), {})


if __name__ == "__main__":
    unittest.main()
