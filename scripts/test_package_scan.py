#!/usr/bin/env python3
"""Red-first tests for scripts/package_scan.py (owner 2026-11-11, audit pick C): score packages of one or two moves
for this week and for the title, on demand. On 2026-11-10 this took hand-written scratch scripts.

    python3 scripts/test_package_scan.py
"""
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import package_scan as PS  # noqa: E402

V = {"Star": 9.0, "Mid": 3.0, "Low1": 1.0, "Low2": 0.5, "Low3": 0.2, "FA1": 4.0, "FA2": 2.0, "FA3": 0.1, "Hurt": 8.0}
BY = {n: {"player": n, "adj": v} for n, v in V.items()}
MINE = [dict(player=n, value=V[n]) for n in ("Star", "Mid", "Low1", "Low2", "Low3")]
FAS = [dict(player=n, value=V[n]) for n in ("FA1", "FA2", "FA3")]
IL = [{"seat": 10, "player": "Hurt", "return_date": "2026-11-13", "week": 4}]


def week_fn(names):          # P(5+) rises with the roster's value; FA2 is worth extra this week
    return min(0.99, sum(V[n] for n in names) / 40 + (0.2 if "FA2" in names else 0)), 4.5


def ecw_fn(names):
    return sum(V[n] for n in names) / 10


def fake_sim(calls):
    def sim(ros, seed, seasons, work, tag="cur", windows=None, patch=None):
        names = sorted(p["player"] for p in ros[10])
        calls.append(names)
        return {"teams": {"10": {"champ": sum(V[n] for n in names) + (0.1 if seed == 2027 else 0)}}}
    return sim


class Scan(unittest.TestCase):
    def scan(self, **kw):
        self.calls = []
        a = dict(mine=MINE, fas=FAS, by=BY, avail={}, rosters={10: [BY[r["player"]] for r in MINE], 3: [BY["Mid"]]},
                 k=2, must_add=None, drop_pool=3, shortlist=1, named=[], seasons=100, sim=fake_sim(self.calls),
                 work=tempfile.mkdtemp(), week_fn=week_fn, ecw_fn=ecw_fn, il=IL, value=lambda p: p["adj"])
        a.update(kw)
        return PS.scan(**a)

    def test_every_package_from_the_pool_is_scored_for_week_and_season(self):
        r = self.scan()
        self.assertEqual(r["n_packages"], 3 * 3)                    # C(3 adds, 2) x C(3 drops, 2)
        self.assertEqual(r["drop_pool"], ["Low3", "Low2", "Low1"])  # the lowest three by value; Star and Mid never
        self.assertTrue(all(set(x["drops"]) <= {"Low1", "Low2", "Low3"} for x in r["rows"]))
        x = next(x for x in r["rows"] if x["adds"] == ["FA1", "FA2"] and x["drops"] == ["Low2", "Low3"])
        self.assertAlmostEqual(x["week"]["p5"], (9 + 3 + 1 + 4 + 2) / 40 + 0.2)
        self.assertAlmostEqual(x["week"]["d_p5"], x["week"]["p5"] - r["base"]["week_p5"])
        self.assertAlmostEqual(x["season_d_ecw"], (4 + 2 - 0.5 - 0.2) / 10)

    def test_must_add_fixes_one_of_the_adds(self):
        r = self.scan(must_add="FA3")
        self.assertEqual(r["n_packages"], 2 * 3)
        self.assertTrue(all("FA3" in x["adds"] for x in r["rows"]))

    def test_single_moves_are_packages_of_one(self):
        r = self.scan(k=1)
        self.assertEqual(r["n_packages"], 3 * 3)
        self.assertEqual(len(r["rows"][0]["adds"]), 1)

    def test_only_the_shortlist_and_named_packages_are_simulated(self):
        named = [dict(adds=["FA3", "FA2"], drops=["Low1", "Low2"])]
        r = self.scan(named=named)
        sim = [x for x in r["rows"] if x["title"]]
        # top 1 by season (FA1+FA2 for Low2+Low3), top 1 by week (the same), and the named one
        self.assertEqual(sorted((x["adds"], x["drops"]) for x in sim), [(["FA1", "FA2"], ["Low2", "Low3"]), (["FA2", "FA3"], ["Low1", "Low2"])])
        self.assertEqual(len(self.calls), 2 * (1 + 2))                # base + 2 packages, two seeds each
        n = next(x for x in r["rows"] if x.get("named"))
        self.assertEqual(n["adds"], ["FA2", "FA3"])
        self.assertAlmostEqual(n["title"]["d"], (2 + 0.1) - (1 + 0.5))
        self.assertEqual(n["rank_week"], [x["week"]["p5"] for x in sorted(r["rows"], key=lambda x: -x["week"]["p5"])].index(n["week"]["p5"]) + 1)

    def test_an_add_that_would_be_the_next_cut_is_flagged(self):
        r = self.scan()
        x = next(x for x in r["rows"] if x["adds"] == ["FA1", "FA3"] and x["drops"] == ["Low2", "Low3"])
        self.assertEqual(x["first_cut"], dict(player="FA3", when="Hurt", return_date="2026-11-13"))   # FA3 0.1 is the lowest left
        y = next(x for x in r["rows"] if x["adds"] == ["FA1", "FA2"] and x["drops"] == ["Low2", "Low3"])
        self.assertIsNone(y["first_cut"])                                                               # Low1 goes first
        self.assertIsNone(next(x for x in self.scan(il=[])["rows"] if x["adds"] == ["FA1", "FA3"])["first_cut"])

    def test_a_named_player_who_is_not_available_or_not_mine_is_refused(self):
        with self.assertRaises(PS.PackageError):
            self.scan(named=[dict(adds=["Nobody", "FA1"], drops=["Low1", "Low2"])])
        with self.assertRaises(PS.PackageError):
            self.scan(named=[dict(adds=["FA2", "FA1"], drops=["Low1", "Elsewhere"])])
        with self.assertRaises(PS.PackageError):
            self.scan(must_add="Nobody")

    def test_an_unavailable_free_agent_is_not_a_candidate(self):
        r = self.scan(avail={"FA1": 0.0})
        self.assertTrue(all("FA1" not in x["adds"] for x in r["rows"]))

    def test_render_and_pass_line(self):
        r = self.scan(named=[dict(adds=["FA3", "FA2"], drops=["Low1", "Low2"])]); r["date"] = "2026-11-11"
        md = "\n".join(PS.render(r))
        self.assertIn("| FA1 + FA2 | Low2 + Low3 |", md)
        self.assertIn("your package", md); self.assertIn("of 9", md)
        self.assertIn("would be the next cut when Hurt returns", "\n".join(PS.render(self.scan(shortlist=9) | {"date": "d"})))
        self.assertTrue(PS.pass_line(r, "x.json").startswith("PACKAGE SCAN: PASS — 2026-11-11: 9 packages"))

    def test_named_parses_from_the_command_line_form(self):
        self.assertEqual(PS.parse_named("FA1+FA2/Low1+Low2"), dict(adds=["FA1", "FA2"], drops=["Low1", "Low2"]))
        self.assertEqual(PS.parse_named("FA1/Low1"), dict(adds=["FA1"], drops=["Low1"]))
        with self.assertRaises(PS.PackageError):
            PS.parse_named("FA1+FA2/Low1")


if __name__ == "__main__":
    unittest.main()
