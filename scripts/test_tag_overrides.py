#!/usr/bin/env python3
"""Red-first tests for the kit's in-season tag overrides in scripts/season_lines.py (owner 2026-10-22, D-RR-1:
"Remove it", then the route "Kit season override"). The frozen Version 69 snapshot (deck players_v69.csv) is never
edited; data/tag_overrides.csv replaces one player's leading note tag in the season pool the brief, week matchup and
availability calibration read, and refuses an override whose expected tag no longer matches the snapshot.

    python3 scripts/test_tag_overrides.py
"""
import csv
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import season_lines as S  # noqa: E402
import co_gm  # noqa: E402  (imports the deck's hoops and arena from the sibling checkout)

KIT_ROW = dict(name="Test Wing", team="SAC", pos="SF", gp="70", mpg="26.0", fgp="0.440", fga="10.0", ftp="0.850",
               fta="3.0", tpm="1.9", pts="13.8", reb="3.9", ast="1.7", stl="0.7", blk="0.2", tov="1.5")
DECK_ROW = dict(player="Test Wing", team="SAC", pos="SF", fg_pct="0.440", fga="10.0", ft_pct="0.850", fta="3.0",
                tpm="1.9", pts="13.8", reb="3.9", ast="1.7", stl="0.7", blk="0.2", tov="1.5",
                note="inj-eye-risk (retinal surgery Feb); 10/9: started the 10/8 game")
OTHER_ROW = dict(DECK_ROW, player="Other Guard", pos="PG", note="inj-knee-risk (first season back)")
OVERRIDE = dict(player="Test Wing", tag_from="inj-eye-risk", tag_to="tag-cleared", decided="2026-10-22 owner D-RR-1",
                receipt="after-report-2026-10-22-risk-rows.md §4")


def write(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)


def inputs(d, deck_rows=(DECK_ROW, OTHER_ROW), overrides=(OVERRIDE,), override_fields=None):
    kit, deck, ov = (os.path.join(d, n) for n in ("kit.csv", "deck.csv", "overrides.csv"))
    write(kit, [KIT_ROW], list(KIT_ROW))
    write(deck, list(deck_rows), list(DECK_ROW))
    write(ov, list(overrides), override_fields or list(OVERRIDE))
    return kit, deck, ov


def pool(d):
    return list(csv.DictReader(open(os.path.join(d, "pool_season.csv"), encoding="utf-8")))


class Override(unittest.TestCase):
    def test_the_leading_tag_is_replaced_and_the_prose_kept(self):
        with tempfile.TemporaryDirectory() as d:
            kit, deck, ov = inputs(d)
            S.run(date="2026-10-22", actuals=[], kit_csv=kit, deck_csv=deck, out_dir=d, overrides_csv=ov)
            note = pool(d)[0]["note"]
            self.assertEqual(S.note_tag(note), "tag-cleared")
            self.assertTrue(note.endswith(" (retinal surgery Feb); 10/9: started the 10/8 game"), note)

    def test_only_the_named_players_note_changes(self):
        with tempfile.TemporaryDirectory() as d:
            kit, deck, ov = inputs(d)
            S.run(date="2026-10-22", actuals=[], kit_csv=kit, deck_csv=deck, out_dir=d, overrides_csv=ov)
            out = pool(d)
            self.assertEqual(out[1], OTHER_ROW)
            self.assertEqual({k: v for k, v in out[0].items() if k != "note"}, {k: v for k, v in DECK_ROW.items() if k != "note"})

    def test_the_consumers_read_the_override_as_healthy(self):
        # the deck's own leading-tag rules: the board's availability and the season simulator's weekly availability
        with tempfile.TemporaryDirectory() as d:
            kit, deck, ov = inputs(d)
            S.run(date="2026-10-22", actuals=[], kit_csv=kit, deck_csv=deck, out_dir=d, overrides_csv=ov)
            row = pool(d)[0]
            self.assertEqual(co_gm.hoops.availability(row), 1.0)
            self.assertEqual(co_gm.arena.weekly_availability(row), 0.88)
            self.assertEqual(co_gm.hoops.availability(DECK_ROW), 0.78)

    def test_a_stale_override_is_refused_and_nothing_is_written(self):
        with tempfile.TemporaryDirectory() as d:
            kit, deck, ov = inputs(d, overrides=(dict(OVERRIDE, tag_from="inj-knee-risk"),))
            with self.assertRaisesRegex(ValueError, "Test Wing.*inj-eye-risk.*inj-knee-risk"):
                S.run(date="2026-10-22", actuals=[], kit_csv=kit, deck_csv=deck, out_dir=d, overrides_csv=ov)
            self.assertFalse(os.path.exists(os.path.join(d, "pool_season.csv")))

    def test_a_player_outside_the_deck_plane_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            kit, deck, ov = inputs(d, overrides=(dict(OVERRIDE, player="Nobody Here"),))
            with self.assertRaisesRegex(ValueError, "Nobody Here"):
                S.run(date="2026-10-22", actuals=[], kit_csv=kit, deck_csv=deck, out_dir=d, overrides_csv=ov)

    def test_a_file_with_other_columns_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            kit, deck, ov = inputs(d, overrides=({"player": "Test Wing", "tag": "tag-cleared"},),
                                   override_fields=["player", "tag"])
            with self.assertRaisesRegex(ValueError, "columns"):
                S.run(date="2026-10-22", actuals=[], kit_csv=kit, deck_csv=deck, out_dir=d, overrides_csv=ov)

    def test_a_replacement_must_be_one_tag_token(self):
        with tempfile.TemporaryDirectory() as d:
            kit, deck, ov = inputs(d, overrides=(dict(OVERRIDE, tag_to="healthy now"),))
            with self.assertRaisesRegex(ValueError, "one tag"):
                S.run(date="2026-10-22", actuals=[], kit_csv=kit, deck_csv=deck, out_dir=d, overrides_csv=ov)

    def test_an_override_without_a_decision_is_refused(self):
        # found by the delivery check (2026-10-22): an empty "decided" cell raised IndexError, not the FAIL line
        with tempfile.TemporaryDirectory() as d:
            kit, deck, ov = inputs(d, overrides=(dict(OVERRIDE, decided=" "),))
            with self.assertRaisesRegex(ValueError, "decided"):
                S.run(date="2026-10-22", actuals=[], kit_csv=kit, deck_csv=deck, out_dir=d, overrides_csv=ov)

    def test_no_overrides_file_leaves_the_pool_byte_equal(self):
        with tempfile.TemporaryDirectory() as d:
            kit, deck, _ = inputs(d)
            S.run(date="2026-10-22", actuals=[], kit_csv=kit, deck_csv=deck, out_dir=d,
                  overrides_csv=os.path.join(d, "absent.csv"))
            self.assertEqual(open(os.path.join(d, "pool_season.csv"), encoding="utf-8").read().replace("\r", ""),
                             open(deck, encoding="utf-8").read().replace("\r", ""))

    def test_the_record_names_each_override_applied(self):
        with tempfile.TemporaryDirectory() as d:
            kit, deck, ov = inputs(d)
            rec = S.run(date="2026-10-22", actuals=[], kit_csv=kit, deck_csv=deck, out_dir=d, overrides_csv=ov)
            self.assertEqual(rec["tag_overrides"], [dict(player="Test Wing", tag_from="inj-eye-risk", tag_to="tag-cleared")])

    def test_the_command_line_run_reads_the_kits_overrides_file(self):
        # end to end on the real inputs, written to a scratch folder: Hunter's eye tag is cleared in the season pool only
        with tempfile.TemporaryDirectory() as d:
            p = subprocess.run([sys.executable, os.path.join(HERE, "season_lines.py"), "--date", "2026-10-22", "--out", d],
                               capture_output=True, text=True)
            self.assertIn("SEASON LINES: PASS", p.stdout, p.stdout + p.stderr)
            hunter = next(r for r in pool(d) if r["player"] == "De'Andre Hunter")
            self.assertEqual(S.note_tag(hunter["note"]), "tag-cleared")
            with open(S.DECK_CSV, encoding="utf-8") as f:
                snap = next(r for r in csv.DictReader(f) if r["player"] == "De'Andre Hunter")
            self.assertEqual(S.note_tag(snap["note"]), "inj-eye-risk")


if __name__ == "__main__":
    unittest.main(verbosity=2)
