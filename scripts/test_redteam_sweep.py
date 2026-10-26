#!/usr/bin/env python3
"""Red-first tests for scripts/redteam/sweep.py and check_bands.py (post-mortem 2026-10-19 D-PM-1; RULES.md 5, 6).

The sweep must build its variants from the registry (a declared_band constant with no band is an error, not
a silent skip), tier a shift by the post-mortem rule, and the bands check must refuse a report that does not
quote every FRAGILE band.

    python3 scripts/test_redteam_sweep.py
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "redteam"))
import sweep as S  # noqa: E402
import check_bands as B  # noqa: E402


def registry(*entries):
    return {"constants": list(entries)}


SHOCK = {"module": "arena", "name": "TEAM_WEEK_SHOCK", "value": 0.06, "status": "declared_band",
         "band": [{"label": "no shock", "const": {"TEAM_WEEK_SHOCK": 0.0}},
                  {"label": "shock doubled", "const": {"TEAM_WEEK_SHOCK": 0.12}}]}
FIXED = {"module": "arena", "name": "WEEKS", "value": 17, "status": "settings"}


class Variants(unittest.TestCase):
    def test_variants_come_from_declared_bands_only(self):
        v = S.variants_from_registry(registry(SHOCK, FIXED))
        self.assertEqual([x["constant"] for x in v], ["arena.TEAM_WEEK_SHOCK"] * 2)
        self.assertEqual(v[0]["label"], "no shock")

    def test_declared_band_without_band_is_an_error(self):
        bare = dict(SHOCK)
        bare.pop("band")
        with self.assertRaises(ValueError):
            S.variants_from_registry(registry(bare))


class Tiers(unittest.TestCase):
    def test_tier_thresholds(self):
        self.assertEqual(S.tier(0.99), "ROBUST")
        self.assertEqual(S.tier(-1.0), "SENSITIVE")
        self.assertEqual(S.tier(1.99), "SENSITIVE")
        self.assertEqual(S.tier(2.0), "FRAGILE")
        self.assertEqual(S.tier(-3.4), "FRAGILE")

    def test_constant_tier_is_its_worst_variant(self):
        rec = S.summarize({"baseline": {"2026": 20.0, "2027": 20.0},
                           "no shock": {"2026": 23.0, "2027": 23.8},
                           "shock doubled": {"2026": 19.5, "2027": 19.7}},
                          [dict(constant="arena.TEAM_WEEK_SHOCK", label="no shock"),
                           dict(constant="arena.TEAM_WEEK_SHOCK", label="shock doubled")], ["2026", "2027"])
        c = rec["constants"]["arena.TEAM_WEEK_SHOCK"]
        self.assertEqual(c["tier"], "FRAGILE")
        self.assertEqual([v["shift_mean"] for v in c["variants"]], [3.4, -0.4])
        self.assertEqual(rec["fragile"], ["arena.TEAM_WEEK_SHOCK"])


class Bands(unittest.TestCase):
    SWEEP = {"constants": {"arena.TEAM_WEEK_SHOCK": {"tier": "FRAGILE", "variants": [
        {"label": "no shock", "shift_mean": 3.4}, {"label": "shock doubled", "shift_mean": -2.3}]},
        "arena.CV": {"tier": "ROBUST", "variants": [{"label": "x0.8", "shift_mean": 0.1}]}},
        "fragile": ["arena.TEAM_WEEK_SHOCK"]}

    def run_check(self, text):
        with tempfile.TemporaryDirectory() as d:
            r = os.path.join(d, "r.md")
            s = os.path.join(d, "s.json")
            with open(r, "w") as f:
                f.write(text)
            with open(s, "w") as f:
                json.dump(self.SWEEP, f)
            return B.check(r, s)

    def test_report_without_the_band_fails(self):
        ok, problems = self.run_check("# report\nthe title share is 21.4 percent.\n")
        self.assertFalse(ok)
        self.assertTrue(any("TEAM_WEEK_SHOCK" in p for p in problems), problems)

    def test_report_with_half_the_band_fails(self):
        ok, _ = self.run_check("TEAM_WEEK_SHOCK is FRAGILE: +3.4 without the shock.\n")
        self.assertFalse(ok)

    def test_report_quoting_the_band_passes(self):
        ok, problems = self.run_check("TEAM_WEEK_SHOCK is FRAGILE: +3.4 with no shock, -2.3 doubled.\n")
        self.assertTrue(ok, problems)

    def test_unicode_minus_is_accepted(self):
        ok, _ = self.run_check("TEAM_WEEK_SHOCK FRAGILE: +3.4 / −2.3\n")
        self.assertTrue(ok)

    def test_no_fragile_constant_passes_without_quotes(self):
        with tempfile.TemporaryDirectory() as d:
            r = os.path.join(d, "r.md")
            s = os.path.join(d, "s.json")
            with open(r, "w") as f:
                f.write("nothing here\n")
            with open(s, "w") as f:
                json.dump({"constants": {"arena.CV": {"tier": "ROBUST", "variants": []}}, "fragile": []}, f)
            ok, _ = B.check(r, s)
            self.assertTrue(ok)


class Smoke(unittest.TestCase):
    def test_sweep_runs_on_the_live_engine_at_test_size(self):
        if not os.path.isdir(S.DECK):
            self.skipTest("deck not present")
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "sweep.json")
            rec = S.run_sweep(seasons=10, seeds=(1, 2), out=out, workers=2,
                             registry=registry(SHOCK, FIXED))
            self.assertEqual(sorted(rec["variants"]), sorted(["baseline", "no shock", "shock doubled"]))
            self.assertEqual(rec["seasons"], 10)
            self.assertIn("engine_commit", rec)
            self.assertTrue(os.path.exists(out))



class SeasonConfiguration(unittest.TestCase):
    """Owner 2026-10-26 ("re-measure the uncertainty ranges ... now that they use the updated stats"): the sweep runs
    on a named state and pool (the season configuration the title odds use) and records both with their sha256; the
    draft configuration stays the default."""
    def setUp(self):
        if not os.path.isdir(S.DECK):
            self.skipTest("deck not present")
        import csv
        self.d = tempfile.mkdtemp()
        st = json.load(open(os.path.join(S.DECK, S.STATE), encoding="utf-8"))
        first = st["picks"][0]["player"]; st["picks"][0]["player"] = "Season Pickup Zzz"
        self.state = os.path.join(self.d, "state.json"); json.dump(st, open(self.state, "w"))
        with open(os.path.join(S.DECK, S.POOL), encoding="utf-8") as f:
            r = csv.DictReader(f); fields = r.fieldnames; rows = list(r)
        rows.append(dict(next(x for x in rows if x["player"] == first), player="Season Pickup Zzz"))
        self.pool = os.path.join(self.d, "pool.csv")
        with open(self.pool, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

    def test_a_job_plays_the_named_state_and_pool(self):
        label, seed, title, playoff = S._job(("baseline", {}, 1, 20, S.DECK, self.state, self.pool))
        self.assertEqual((label, seed), ("baseline", 1))
        self.assertGreaterEqual(title, 0.0)

    def test_the_record_names_the_configuration_with_hashes_and_its_own_references(self):
        import hashlib
        refs = {}
        for sd in (1, 2):
            refs[sd] = os.path.join(self.d, f"ref_{sd}.json")
            json.dump({"teams": {str(S.OWNER_SEAT): {"champ": 50.0}}}, open(refs[sd], "w"))
        rec = S.run_sweep(seasons=10, seeds=(1, 2), out=os.path.join(self.d, "sweep.json"), workers=2,
                          registry=registry(SHOCK, FIXED), state=self.state, pool=self.pool, references=refs)
        self.assertEqual(rec["state"], self.state); self.assertEqual(rec["pool"], self.pool)
        self.assertEqual(rec["state_sha256"], hashlib.sha256(open(self.state, "rb").read()).hexdigest())
        self.assertEqual(rec["pool_sha256"], hashlib.sha256(open(self.pool, "rb").read()).hexdigest())
        self.assertEqual(rec["reference_10k"], {"1": 50.0, "2": 50.0})

    def test_a_missing_reference_is_an_error_not_a_silent_skip(self):
        with self.assertRaises(FileNotFoundError):
            S.run_sweep(seasons=10, seeds=(1,), out=os.path.join(self.d, "sweep.json"), workers=1,
                        registry=registry(SHOCK, FIXED), state=self.state, pool=self.pool,
                        references={1: os.path.join(self.d, "nope.json")})


class RealSchedule(unittest.TestCase):
    """Owner 2026-10-26 ("build the real-schedule re-measurement"): every variant through league_sim on the league's
    real pairings and the weeks already final; the inputs pinned beside the record; the reference the plain run."""
    SCHED = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "league_schedule.json")

    def setUp(self):
        if not os.path.isdir(S.DECK):
            self.skipTest("deck not present")
        sc = SeasonConfiguration(); sc.setUp(); self.d, self.state, self.pool = sc.d, sc.state, sc.pool
        st = json.load(open(self.state))
        self.ls = os.path.join(self.d, "ls.json")
        json.dump(dict(as_of="2026-10-26", teams=[dict(name=f"T{s}", seat=s, players=[dict(player=pk["player"], slot="BN")
                  for pk in st["picks"] if pk["slot"] == s]) for s in range(1, 13)]), open(self.ls, "w"))

    def test_inputs_are_pinned_and_the_reference_is_the_plain_real_schedule_run(self):
        out = os.path.join(self.d, "rec")
        state, refs, pool, sched = S.season_inputs(out, self.ls, self.pool, (1,), ref_seasons=20, schedule=self.SCHED)
        for f in ("league_state.json", "pool_season.csv", "league_schedule.json", "state_season.json"):
            self.assertTrue(os.path.exists(os.path.join(out, f)), f)
        self.assertEqual((os.path.dirname(pool), os.path.dirname(sched)), (out, out))
        ref = json.load(open(refs[1]))
        self.assertFalse(ref["verified_against_arena"])
        self.assertIn("schedule", ref)

    def test_every_variant_runs_through_league_sim_and_the_record_says_so(self):
        out = os.path.join(self.d, "rec")
        state, refs, pool, sched = S.season_inputs(out, self.ls, self.pool, (1,), ref_seasons=20, schedule=self.SCHED)
        rec = S.run_sweep(seasons=10, seeds=(1,), out=os.path.join(out, "sweep.json"), workers=2, registry=registry(SHOCK, FIXED),
                          state=state, pool=pool, references=refs, schedule=sched)
        self.assertEqual(rec["simulator"], "league_sim (real pairings, weeks already final)")
        self.assertEqual(rec["schedule"], sched)
        self.assertEqual(sorted(rec["variants"]), sorted(["baseline", "no shock", "shock doubled"]))

    def test_the_real_schedule_needs_the_season_configuration(self):
        with self.assertRaises(ValueError):
            S.run_sweep(seasons=10, seeds=(1,), out=os.path.join(self.d, "x.json"), workers=1, registry=registry(SHOCK, FIXED),
                        schedule=self.SCHED)

if __name__ == "__main__":
    unittest.main(verbosity=2)
