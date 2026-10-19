#!/usr/bin/env python3
"""The simulators' league constants must equal the league's own settings page
(plan 2026-10-15 §4 B1; lesson L2: league mechanics are read from the league, never assumed).

Source of truth: data/league_settings.json, transcribed from the owner's pinned settings PDF
(data/source/yahoo-league-settings-2026-10-15.pdf). Checked against the deck's arena/arena.py
and scripts/hoops.py (found through DECK_REPO or the sibling checkout) and the kit's
report/schedule/build_schedule.py. Any divergence fails.

    python3 scripts/test_settings.py
"""
import collections
import importlib.util
import json
import os
import sys
import unittest

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK = os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball")
for p in (os.path.join(DECK, "scripts"), os.path.join(DECK, "arena")):
    sys.path.insert(0, p)
import hoops  # noqa: E402
import arena  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "build_schedule", os.path.join(KIT, "report", "schedule", "build_schedule.py"))
build_schedule = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build_schedule)

S = {k: (v["value"] if isinstance(v, dict) and "value" in v else v)
     for k, v in json.load(open(os.path.join(KIT, "data", "league_settings.json"), encoding="utf-8")).items()}

# Yahoo slot -> eligible base positions (None = Util, any position)
SLOT = {"PG": ("PG",), "SG": ("SG",), "G": ("PG", "SG"), "SF": ("SF",), "PF": ("PF",),
        "F": ("SF", "PF"), "C": ("C",), "Util": None}
STARTING = [s for s in S["roster_positions"] if s not in ("BN", "IL")]


class Settings(unittest.TestCase):
    def test_teams(self):
        self.assertEqual(arena.TEAMS, S["teams"])

    def test_regular_season_weeks(self):
        self.assertEqual(arena.WEEKS, S["regular_season_weeks"],
                         "arena.WEEKS is the regular-season matchup count")

    def test_playoff_teams(self):
        self.assertEqual(arena.PLAYOFF_TEAMS, S["playoffs"]["teams"])

    def test_playoff_weeks_in_the_schedule_builder(self):
        self.assertEqual(tuple(build_schedule.OWNER_PLAYOFF_WEEKS), tuple(S["playoffs"]["weeks"]))

    def test_categories(self):
        self.assertEqual(list(hoops.CATS), S["categories"])

    def test_starting_slots(self):
        want = collections.Counter(SLOT[s] for s in STARTING)
        self.assertEqual(collections.Counter(arena.LINEUP_SLOTS), want)
        non_util = collections.Counter(elig for _, elig in hoops.POSITIONAL_SLOTS)
        self.assertEqual(non_util, collections.Counter(SLOT[s] for s in STARTING if s != "Util"))

    def test_roster_size_and_draft(self):
        active = sum(1 for s in S["roster_positions"] if s != "IL")
        self.assertEqual(arena.ROUNDS, active)
        self.assertEqual(hoops.DRAFTABLE, S["teams"] * active)

    def test_playoff_reseeding(self):
        """Reseeded: after round 1 the best remaining seed meets the worst remaining seed.
        Upsets 8 over 1 and 7 over 2 leave seeds {3, 4, 7, 8}: semis 3 v 8 and 4 v 7."""
        self.assertTrue(S["playoff_reseeding"])
        played = []
        upsets = {(1, 8), (2, 7)}

        def week_result(a, b):
            played.append(tuple(sorted((a, b))))
            lo = min(a, b)
            winner = max(a, b) if tuple(sorted((a, b))) in upsets else lo
            return 9 if winner == a else 0

        arena.playoff_champion(list(range(1, 9)), week_result)
        self.assertEqual(set(played[4:6]), {(3, 8), (4, 7)}, f"semifinals played: {played[4:6]}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
