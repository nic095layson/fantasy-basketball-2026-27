#!/usr/bin/env python3
"""Red-first tests for scripts/co_gm.py and scripts/daily_brief.py (Session 1 item 6).

    python3 scripts/test_daily_brief.py
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import co_gm as CG  # noqa: E402
import daily_brief as DB  # noqa: E402


def pl(name, pos, value, avail=1.0):
    return {"player": name, "positions": pos, "value": value, "availability": avail}


class DailyFill(unittest.TestCase):
    def test_every_slot_kind_is_respected(self):
        lineup, bench = CG.daily_lineup([pl("A", ["C"], 9), pl("B", ["C"], 8), pl("D", ["C"], 7), pl("E", ["PG"], 6)])
        slots = {s: p for s, p in lineup}
        self.assertEqual(slots.get("PG"), "E")
        self.assertEqual(sorted(p for s, p in lineup if s in ("C", "Util")), ["A", "B", "D"])
        self.assertEqual(bench, [])

    def test_a_flex_player_moves_aside_so_a_lower_valued_specialist_still_starts(self):
        # slot-order greedy puts the PG,SG star at PG; the four pure PGs then fill G, Util, Util and
        # one sits. The star belongs at SG so all five start.
        roster = [pl("Star", ["PG", "SG"], 10)] + [pl(f"PG{i}", ["PG"], 5 - i) for i in range(4)]
        lineup, bench = CG.daily_lineup(roster)
        self.assertEqual(len(lineup), 5)
        self.assertEqual(bench, [])

    def test_out_players_never_start_and_eleventh_player_sits(self):
        roster = [pl(f"U{i}", ["SF"], 20 - i) for i in range(11)] + [pl("Hurt", ["C"], 99, avail=0.0)]
        lineup, bench = CG.daily_lineup(roster)
        names = [p for _, p in lineup]
        self.assertNotIn("Hurt", names)
        self.assertEqual(len(lineup), 4)  # SF, F, Util, Util are the only slots an SF can take
        self.assertEqual(len(bench), 7)


class Schedule(unittest.TestCase):
    def test_bref_codes_map_to_pool_codes(self):
        self.assertEqual(CG.TEAM_CODE.get("CHO"), "CHA")
        self.assertEqual(CG.TEAM_CODE.get("BRK"), "BKN")
        self.assertEqual(CG.TEAM_CODE.get("PHO"), "PHX")

    def test_games_left_counts_from_the_date_to_the_week_end(self):
        games = [("2026-10-20", "BOS", "DET"), ("2026-10-21", "PHO", "POR"), ("2026-10-23", "POR", "LAL"),
                 ("2026-10-26", "POR", "UTA")]
        left = CG.games_left(games, "2026-10-21", "2026-10-25")
        self.assertEqual(left["POR"], 2)
        self.assertEqual(left["PHX"], 1)
        self.assertEqual(left.get("BOS", 0), 0)


class Streaming(unittest.TestCase):
    def test_ranks_by_value_among_players_with_more_games_than_the_drop(self):
        # 2026-10-15 first run: every candidate's per-game value was negative and the sort clamped
        # them all to zero, so the list came out in arbitrary order
        fa = [{"player": "A", "team": "X", "games_left": 3, "value_per_game": -2.3},
              {"player": "B", "team": "Y", "games_left": 3, "value_per_game": -1.1},
              {"player": "C", "team": "Z", "games_left": 2, "value_per_game": 5.0}]
        out = CG.streaming(fa, drop_games=2)
        self.assertEqual([r["player"] for r in out], ["B", "A"])


class Note(unittest.TestCase):
    def test_odds_line_is_the_two_run_average_with_its_error(self):
        # owner 2026-10-20: "just provide the average" — the seed labels read as years; one averaged figure
        line = DB.odds_line(21.81, 21.60, 10000)
        self.assertIn("21.7%", line)
        self.assertIn("±", line)
        self.assertNotIn("seed", line.lower())
        self.assertNotIn("21.81", line)


class Band(unittest.TestCase):
    """Post-mortem D-PM-6 / D-RT-2: every title figure carries the structural band from the standing sweep."""
    def test_band_line_names_the_fragile_constant_and_its_figures(self):
        # a fixture record (2026-11-17): the live sweep may carry no FRAGILE constant, which says nothing about the line
        import json, tempfile
        rec = dict(engine_commit="abc1234", fragile=["arena.TEAM_WEEK_SHOCK"], constants={"arena.TEAM_WEEK_SHOCK": dict(
            tier="FRAGILE", variants=[dict(label="no shock", shift_mean=3.0), dict(label="doubled", shift_mean=-2.5)])})
        p = os.path.join(tempfile.mkdtemp(), "s.json")
        json.dump(rec, open(p, "w"))
        line = DB.band_line(p)
        self.assertIn("TEAM_WEEK_SHOCK", line); self.assertIn("FRAGILE", line)
        self.assertRegex(line, r"[+-]\d\.\d")

    def test_a_band_from_another_engine_says_stale_and_the_record_carries_the_check(self):
        """Owner 2026-11-17 ("Flag it and re-sweep"): the 11-17 brief printed Monday morning's band beside a share on
        the engine changed that afternoon."""
        import json, tempfile
        from unittest import mock
        rec = dict(engine_commit="abc1234", fragile=[], constants={})
        p = os.path.join(tempfile.mkdtemp(), "s.json")
        json.dump(rec, open(p, "w"))
        stale = dict(status="STALE", why="measured on engine aaa1111, the live engine is bbb2222")
        with mock.patch.object(DB.SR, "stale", return_value=stale):
            self.assertIn("deck abc1234; STALE: measured on engine aaa1111, the live engine is bbb2222, so these shifts are not today's)",
                          DB.band_line(p))
            self.assertEqual(DB.band_check(p)["status"], "STALE")
        with mock.patch.object(DB.SR, "stale", return_value=dict(status="CURRENT", why="")):
            self.assertNotIn("STALE", DB.band_line(p)); self.assertIn("no FRAGILE constant", DB.band_line(p))

    def test_with_no_fragile_constant_the_largest_sensitive_band_is_printed(self):
        """Owner 2026-11-17 ("Show the largest band anyway"): the 11-17 sweep had none at 2 points."""
        import json, tempfile
        from unittest import mock
        rec = dict(engine_commit="3551a15", fragile=[], constants={
            "arena.weekly_availability": dict(tier="SENSITIVE", max_abs_shift=1.93, variants=[
                dict(label="risk at the old 0.75", shift_mean=-1.93), dict(label="risk at the unfloored fit (0.56)", shift_mean=1.9)]),
            "arena.TEAM_WEEK_SHOCK": dict(tier="SENSITIVE", max_abs_shift=1.52, variants=[dict(label="no shared games shock (0.0)", shift_mean=1.52)]),
            "arena.BENCH_WEIGHT": dict(tier="ROBUST", max_abs_shift=0.0, variants=[dict(label="bench", shift_mean=0.0)])})
        p = os.path.join(tempfile.mkdtemp(), "s.json")
        json.dump(rec, open(p, "w"))
        with mock.patch.object(DB.SR, "stale", return_value=dict(status="CURRENT", why="")):
            line = DB.band_line(p)
        self.assertIn("): no FRAGILE constant; the largest band, weekly_availability is SENSITIVE: -1.9 (risk at the old 0.75) / +1.9 (risk at the unfloored fit (0.56)).", line)
        self.assertNotIn("TEAM_WEEK_SHOCK", line)
        self.assertEqual(DB.band_check(os.path.join(tempfile.mkdtemp(), "none.json"))["status"], "UNKNOWN")


class SeasonBand(unittest.TestCase):
    """Owner 2026-10-26 ("re-measure the uncertainty ranges shown with the title odds now that they use the updated
    stats"): the brief quotes the sweep run on the season configuration and says which configuration it is."""
    def test_the_brief_reads_the_season_sweep(self):
        self.assertTrue(DB.SR.latest("2026-10-27").endswith(os.path.join("redteam-2026-10-26-season-real", "sweep.json")))

    def test_the_band_line_names_the_configuration(self):
        import json, tempfile
        rec = dict(engine_commit="abc1234", fragile=["arena.TEAM_WEEK_SHOCK"], constants={"arena.TEAM_WEEK_SHOCK": dict(
            tier="FRAGILE", variants=[dict(label="no shock", shift_mean=3.0), dict(label="doubled", shift_mean=-2.5)])})
        d = tempfile.mkdtemp()
        json.dump(rec, open(os.path.join(d, "draft.json"), "w"))
        json.dump(dict(rec, state_sha256="x", pool_sha256="y"), open(os.path.join(d, "season.json"), "w"))
        self.assertIn("draft sweep", DB.band_line(os.path.join(d, "draft.json")))
        self.assertIn("season sweep", DB.band_line(os.path.join(d, "season.json")))


class LinesLabel(unittest.TestCase):
    """Owner 2026-10-26 ("You can change the v69 label"): the brief names the lines it actually ran on."""
    def test_with_the_season_pool_the_label_names_it(self):
        old = os.environ.get("SEASON_POOL")
        os.environ["SEASON_POOL"] = "/x/data/season/pool_season.csv"
        try:
            self.assertEqual(DB.lines_label(), "season pool")
        finally:
            os.environ.pop("SEASON_POOL") if old is None else os.environ.__setitem__("SEASON_POOL", old)

    def test_without_it_the_label_stays_the_frozen_tag(self):
        old = os.environ.pop("SEASON_POOL", None)
        try:
            self.assertEqual(DB.lines_label(), CG.LINES_TAG)
        finally:
            if old is not None:
                os.environ["SEASON_POOL"] = old


class SeasonPool(unittest.TestCase):
    """In-season tool: SEASON_POOL (a deck-schema CSV path) overrides the preseason v69 pool for the brief, the
    preview and the waiver scan; unset, the preseason pool loads as before."""
    def test_env_override_points_the_pool_at_the_season_file(self):
        import importlib
        season = os.path.join(CG.KIT, "data", "season", "pool_season.csv")
        if not os.path.exists(season):
            self.skipTest("no season pool written")
        os.environ["SEASON_POOL"] = season
        try:
            CG.load_pool()
            self.assertEqual(os.path.abspath(CG.hoops.DATA_PATH), os.path.abspath(season))
        finally:
            del os.environ["SEASON_POOL"]
        CG.load_pool()
        self.assertTrue(CG.hoops.DATA_PATH.endswith(f"players_{CG.LINES_TAG}.csv"))


class StatusFile(unittest.TestCase):
    """2026-10-20: a status file dated after the brief (a test run of tomorrow's morning) shadowed the day's own
    file, so the brief read yesterday's rosters' letters. The brief reads the newest file dated on or before it."""
    def test_a_later_dated_file_does_not_shadow_the_brief_date(self):
        import json, tempfile
        d = tempfile.mkdtemp()
        os.makedirs(os.path.join(d, "data", "status"))
        for day in ("2026-10-19", "2026-10-20", "2026-10-21"):
            json.dump({"rows": [{"player": day}]}, open(os.path.join(d, "data", "status", f"status_{day}.json"), "w"))
        kit, CG.KIT = CG.KIT, d
        try:
            st, name = DB.newest_status("2026-10-20")
            self.assertEqual(name, "status_2026-10-20.json"); self.assertEqual(st["rows"][0]["player"], "2026-10-20")
            self.assertEqual(DB.newest_status("2026-10-25")[1], "status_2026-10-21.json")
            self.assertIsNone(DB.newest_status("2026-10-18")[1])
        finally:
            CG.KIT = kit


class Transactions(unittest.TestCase):
    """2026-10-20 (owner): Kevin Porter Jr. waived by MIL on 10/19 reaches the brief; yours first, then the opponent."""
    REC = {"window": ["2026-10-18", "2026-10-20"], "items_in_window": 9, "source": {"ok": True}, "hits": [
        {"date": "2026-10-19", "nba_team": "LAL", "description": "Waived F Dalton Knecht.", "player": "Dalton Knecht", "fantasy_team": None, "seat": None},
        {"date": "2026-10-19", "nba_team": "MIL", "description": "Waived G Kevin Porter Jr.", "player": "Kevin Porter Jr.", "fantasy_team": "THEM", "seat": 11},
        {"date": "2026-10-18", "nba_team": "SAS", "description": "Signed F Tobias Harris.", "player": "Tobias Harris", "fantasy_team": "ME", "seat": 10}]}

    def test_order_and_labels(self):
        L = DB.transactions_lines(self.REC, "ME", "THEM")
        self.assertIn("9 moves, 3 naming a board player", L[0])
        self.assertTrue(L[1].startswith("- **Tobias Harris** (yours)"))
        self.assertIn("THEM, your opponent this week", L[2]); self.assertIn("Waived G Kevin Porter Jr.", L[2])
        self.assertIn("on no roster", L[3])

    def test_unread_feed_and_missing_record_say_so(self):
        self.assertIn("NOT read", DB.transactions_lines({**self.REC, "source": {"ok": False, "detail": "timed out"}}, "ME", "THEM")[0])
        self.assertIn("Not read", DB.transactions_lines(None, "ME", "THEM")[0])


class InjuredList(unittest.TestCase):
    """Owner 2026-10-20 (D-IS-8): "Keep IL players as '0' value unless they are on active roster"."""
    def test_il_players_are_absent_from_the_simulation_rosters_until_moved_to_an_active_slot(self):
        by = {n: {"player": n} for n in ("A", "B", "C")}
        state = {"teams": [{"seat": 10, "players": [{"player": "A", "slot": "PG"}, {"player": "B", "slot": "BN"},
                                                    {"player": "C", "slot": "IL"}]}]}
        self.assertEqual([p["player"] for p in CG.rosters(state, by)[10]], ["A", "B"])
        state["teams"][0]["players"][2]["slot"] = "Util"
        self.assertEqual([p["player"] for p in CG.rosters(state, by)[10]], ["A", "B", "C"])



class LeagueMoves(unittest.TestCase):
    """Owner 2026-10-20 item 2: a league-moves line in the brief — adds/drops/IL since yesterday."""

    def test_moves_render_per_team_with_adds_drops_and_il(self):
        rec = {"old_as_of": "2026-10-19", "new_as_of": "2026-10-20", "moves": [
            {"team": "T", "seat": 1, "added": ["D Man"], "dropped": ["A Man"], "to_il": ["C Man"], "from_il": []}]}
        out = "\n".join(DB.league_moves_lines(rec, "Me"))
        self.assertIn("D Man", out)
        self.assertIn("added", out)
        self.assertIn("A Man", out)
        self.assertIn("dropped", out)
        self.assertIn("C Man", out)
        self.assertIn("IL", out)

    def test_no_record_says_so_instead_of_staying_silent(self):
        out = "\n".join(DB.league_moves_lines(None, "Me"))
        self.assertIn("No league-moves record", out)

    def test_my_team_is_marked_yours(self):
        rec = {"old_as_of": "2026-10-19", "new_as_of": "2026-10-20", "moves": [
            {"team": "Me", "seat": 10, "added": ["X"], "dropped": [], "to_il": [], "from_il": []}]}
        out = "\n".join(DB.league_moves_lines(rec, "Me"))
        self.assertIn("yours", out)

class SimulatorPool(unittest.TestCase):
    """2026-10-21 (owner option (b), the kit's pickups file): the season simulator runs on the frozen v69 pool, so a
    rostered pickup it lacks (Andre Drummond, 10/21) stopped the brief, a fatal morning step. Such a player is left out
    of the simulation, the rule the brief applies to IL players (D-IS-8), and the brief names him."""
    def test_a_rostered_player_the_simulator_pool_lacks_is_left_out_and_named(self):
        import json
        import tempfile
        P, by = CG.load_pool()
        ros = CG.rosters(json.load(open(CG.STATE, encoding="utf-8")), by)
        rival = next(s for s in sorted(ros) if s != CG.OWNER_SEAT)
        ros[rival] = ros[rival] + [dict(ros[rival][0], player="Pickup Nobody")]
        rec = CG.run_league_sim(ros, 2026, 20, tempfile.mkdtemp())
        self.assertEqual(rec["absent_from_sim"], ["Pickup Nobody"])
        self.assertIn(str(CG.OWNER_SEAT), rec["teams"])

    def test_with_a_season_pool_the_simulator_plays_its_pickups_and_names_the_pool(self):
        """Owner 2026-10-26 ("use the season pool"): with SEASON_POOL set, the title odds run on that pool (the lines
        the board plays, pickups included) through league_sim --pool, so a pickup only it carries is not left out."""
        import csv
        import json
        import tempfile
        d = tempfile.mkdtemp()
        frozen = os.path.join(CG.DECK, "arena", "results", f"players_{CG.LINES_TAG}.csv")
        with open(frozen, encoding="utf-8") as f:
            r = csv.DictReader(f); fields = r.fieldnames; rows = list(r)
        pool = os.path.join(d, "pool.csv")
        with open(pool, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows + [dict(rows[0], player="Pickup Nobody")])
        old = os.environ.get("SEASON_POOL")
        os.environ["SEASON_POOL"] = pool
        try:
            P, by = CG.load_pool()
            ros = CG.rosters(json.load(open(CG.STATE, encoding="utf-8")), by)
            rival = next(s for s in sorted(ros) if s != CG.OWNER_SEAT)
            ros[rival] = ros[rival] + [by["Pickup Nobody"]]
            rec = CG.run_league_sim(ros, 2026, 20, d)
        finally:
            if old is None:
                os.environ.pop("SEASON_POOL", None)
            else:
                os.environ["SEASON_POOL"] = old
        self.assertEqual(rec["absent_from_sim"], [])
        self.assertEqual(rec["pool"]["file"], os.path.abspath(pool))

    def test_without_a_season_pool_the_record_names_no_pool(self):
        import json
        import tempfile
        old = os.environ.pop("SEASON_POOL", None)
        try:
            P, by = CG.load_pool()
            rec = CG.run_league_sim(CG.rosters(json.load(open(CG.STATE, encoding="utf-8")), by), 2026, 20, tempfile.mkdtemp())
        finally:
            if old is not None:
                os.environ["SEASON_POOL"] = old
        self.assertNotIn("pool", rec)

    def test_the_brief_names_who_the_simulation_left_out(self):
        self.assertEqual(DB.sim_absent_line([]), None)
        line = DB.sim_absent_line(["Andre Drummond"])
        self.assertIn("Andre Drummond", line)
        self.assertIn("left out of the season simulation", line)



class Unpooled(unittest.TestCase):
    """Owner 2026-10-26, option (a): every name the intake carried without a pool row is named in the brief."""
    def test_named_with_team_and_slot_and_none_says_nothing(self):
        st = {"unpooled": [dict(player="Trevon Brazile", fantasy_team="Podz save the league", seat=4, slot="BN", nba_team="DEN", status=None)]}
        self.assertEqual(DB.unpooled_line(st), "**Not in the pool, not simulated (1):** Trevon Brazile (Podz save the league, BN, DEN). "
                                                "Each needs a data/pool_additions.csv row before the simulator counts him.")
        self.assertIsNone(DB.unpooled_line({"unpooled": []})); self.assertIsNone(DB.unpooled_line({}))


class AutoRowsSimulated(unittest.TestCase):
    """Owner 2026-11-09 (pick "Simulate them"): a rostered player the intake carried as unpooled is simulated when the
    season pool has his row (the auto season line); a name with no row anywhere stays out and keeps the old label."""
    BY = {n: {"player": n} for n in ("A", "Auto Guy")}

    def state(self):
        return {"unpooled": [dict(player="Auto Guy", fantasy_team="T", seat=10, slot="BN", nba_team="CLE", status=None),
                             dict(player="Nobody", fantasy_team="T", seat=10, slot="BN", nba_team="DEN", status=None)],
                "teams": [{"seat": 10, "players": [{"player": "A", "slot": "PG"}],
                           "unpooled": [dict(player="Auto Guy", slot="BN", nba_team="CLE", positions=["SG"], status=None),
                                        dict(player="Nobody", slot="BN", nba_team="DEN", positions=["PF"], status=None),
                                        dict(player="Hurt Auto", slot="IL", nba_team="CLE", positions=["SG"], status="O")]}]}

    def test_an_auto_row_player_is_in_the_simulation_roster(self):
        by = dict(self.BY, **{"Hurt Auto": {"player": "Hurt Auto"}})
        self.assertEqual([p["player"] for p in CG.rosters(self.state(), by)[10]], ["A", "Auto Guy"])   # IL still counts 0
        self.assertEqual([p["player"] for p in CG.rosters(self.state(), by, include_il=True)[10]], ["A", "Auto Guy", "Hurt Auto"])

    def test_an_auto_row_player_is_not_labelled_not_simulated(self):
        line = DB.unpooled_line(self.state(), self.BY)
        self.assertIn("**Not in the pool, not simulated (1):** Nobody (T, BN, DEN).", line)
        self.assertNotIn("Auto Guy (T, BN, CLE). Each", line)
        self.assertIn("Auto row (blended), simulated (1): Auto Guy (T, BN, CLE).", line)
        only_auto = dict(self.state(), unpooled=self.state()["unpooled"][:1])
        self.assertEqual(DB.unpooled_line(only_auto, self.BY), "Auto row (blended), simulated (1): Auto Guy (T, BN, CLE).")


class EarliestReturnWording(unittest.TestCase):
    """Owner 2026-11-11 (card "Keep 7 days, relabel, re-grade"): ESPN's date is the earliest a player could be back.
    Graded 10-28 to 11-11, a first quote was on time for 44% of pool players and early for 3%."""
    def test_the_waiver_flag_calls_it_the_earliest_return(self):
        s = dict(code="Out", source="espn", return_date="2026-11-13", short_out=True)
        self.assertEqual(DB.add_flag(s), "Out today (espn), ESPN's earliest return 2026-11-13")
        self.assertEqual(DB.add_flag(dict(code="Q", source="yahoo", short_out=False)), "Q today (yahoo)")

    def test_a_set_aside_player_and_a_streamer_use_the_same_words(self):
        self.assertEqual(DB.aside_flag(dict(player="A", code="Out", source="espn", return_date="2026-12-01T00:00Z")),
                         "A (Out, espn, ESPN's earliest return 2026-12-01)")
        self.assertEqual(DB.aside_flag(dict(player="A", code="Out", source="yahoo")), "A (Out, yahoo)")
        self.assertEqual(DB.stream_flag(dict(status="Out", return_date="2026-11-13", exp_games=2.0)),
                         " (Out today, ESPN's earliest return 2026-11-13: 2 from then)")
        self.assertEqual(DB.stream_flag(dict(status="Q", exp_games=1.5)), " (Q today: 1.5 expected)")
        self.assertEqual(DB.stream_flag(dict()), "")

    def test_no_line_says_expects_back(self):
        src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "daily_brief.py")).read()
        self.assertNotIn("expects back", src)

    def test_the_seven_day_line_is_unchanged(self):
        self.assertEqual(CG.SHORT_OUT_DAYS, 7)


class LongOutWording(unittest.TestCase):
    """Owner 2026-11-17: a player set aside because his absence is no longer short says so, with the day the feed first
    listed him Out (or "or earlier" when the look-back reached its limit)."""
    def test_the_set_aside_line_names_the_run(self):
        x = dict(player="Tobias Harris", code="O", source="yahoo", return_date="2026-11-09", out_since="2026-10-29", long_out=True, out_capped=True)
        self.assertEqual(DB.aside_flag(x), "Tobias Harris (O, yahoo, ESPN's earliest return 2026-11-09; out since 2026-10-29 or earlier, so not a short absence)")
        self.assertIn("out since 2026-11-03, so", DB.aside_flag(dict(x, out_since="2026-11-03", out_capped=False)))

    def test_an_ordinary_out_reads_as_before(self):
        self.assertEqual(DB.aside_flag(dict(player="A", code="Out", source="espn", return_date=None)), "A (Out, espn)")
        self.assertEqual(DB.aside_flag(dict(player="A", code="O", source="yahoo", return_date="2026-12-03", out_since="2026-11-10", long_out=False, out_capped=True)),
                         "A (O, yahoo, ESPN's earliest return 2026-12-03)")


class ScanRead(unittest.TestCase):
    """Owner 2026-11-17 (card: "Both fixes"): the listed pairs say what their title figures can and cannot tell apart.
    Display only: nothing is reordered."""
    def pair(self, add, drop, d):
        return {"add": add, "drop": drop, "d_title": d, "title": 14.1 + d}

    def test_the_noise_is_the_error_of_a_difference_of_two_shares(self):
        # 14.1% over 2 runs x 10,000 seasons: one share is +/- 0.48 (odds_line), a difference +/- 0.68
        self.assertAlmostEqual(DB.scan_noise(14.1, 10000), 0.68, places=2)
        self.assertAlmostEqual(DB.scan_noise(14.1, 10000) / (196 * (0.141 * 0.859 / 20000) ** 0.5), 2 ** 0.5, places=6)

    def test_each_pair_is_read_against_the_noise(self):
        r = DB.scan_read([self.pair("A", "X", 2.1), self.pair("B", "Y", 0.4), self.pair("C", "Z", -0.5)], 14.1, 10000)
        self.assertEqual([p["read"] for p in r["picks"]], [None, "inside sampling error", "no title gain"])
        self.assertEqual((r["same_drop"], r["tied"]), (None, False))
        self.assertEqual(DB.read_note(r, 0), ""); self.assertEqual(DB.read_note(r, 1), " [inside sampling error]")
        self.assertEqual(DB.read_lines(r), [])

    def test_one_shared_drop_and_a_tie_are_said(self):
        # the 11-03 brief: three adds for Karlo Matkovic at +3.39, +3.12 and +2.55 share the drop but are not tied
        r = DB.scan_read([self.pair("A", "Karlo Matkovic", 3.39), self.pair("B", "Karlo Matkovic", 3.12),
                          self.pair("C", "Karlo Matkovic", 2.55)], 14.1, 10000)
        self.assertEqual((r["same_drop"], r["tied"]), ("Karlo Matkovic", False))
        self.assertEqual(DB.read_lines(r), ["All 3 name Karlo Matkovic as the drop: the title figures say more about that "
                                            "roster spot than about which player you add."])
        r = DB.scan_read([self.pair("A", "X", 3.03), self.pair("B", "X", 3.08), self.pair("C", "X", 2.69)], 14.1, 10000)
        self.assertTrue(r["tied"])
        self.assertIn("The 3 adds are within sampling error of each other (+2.7 to +3.1 title points): the scan cannot rank them.",
                      DB.read_lines(r))

    def test_one_pair_is_never_a_tie_and_no_pair_reads_nothing(self):
        r = DB.scan_read([self.pair("A", "X", 0.75)], 14.1, 10000)
        self.assertEqual((r["same_drop"], r["tied"], r["picks"][0]["read"]), (None, False, None))
        self.assertIsNone(DB.scan_read([], 14.1, 10000)); self.assertEqual(DB.read_lines(None), []); self.assertEqual(DB.read_note(None, 0), "")


class RoleWatch(unittest.TestCase):
    """Owner 2026-11-17 (picks "Starts watch", "Hold check on drops"): both lists reach the brief; a failure is said,
    never raised."""

    def test_the_brief_asks_for_the_days_drops_and_carries_the_record(self):
        seen = {}

        def build(date, state, pool_names, espn=None, drops=()):
            seen.update(date=date, pool=pool_names, espn=espn, drops=list(drops))
            return {"box_scores": ["2026-10-20", "2026-11-16"], "rule": dict(start_run=2, stale_days=7, dropped_days=3, hold_days=7, shown=8),
                    "starts_watch": [], "hold_check": []}
        rw = DB.role_watch_for("2026-11-17", {"teams": []}, ["A"], [{"player": "A"}], ["B", "C"], build=build)
        self.assertEqual(seen, dict(date="2026-11-17", pool=["A"], espn=[{"player": "A"}], drops=["B", "C"]))
        md = DB.role_watch_md(rw)
        self.assertIn("## Starts watch (free players)", md)
        self.assertIn("## Hold check (before you drop)", md)
        self.assertIn("No free player has started his last 2 games.", md)

    def test_a_failure_is_printed_and_the_brief_goes_on(self):
        def build(*a, **k):
            raise KeyError("date")
        rw = DB.role_watch_for("2026-11-17", {}, [], None, [], build=build)
        self.assertEqual(rw, {"error": "KeyError: 'date'"})
        self.assertEqual(DB.role_watch_md(rw).count("Not available today (KeyError: 'date')."), 2)


class MethodStamp(unittest.TestCase):
    """Owner 2026-11-17 (pick F2, after-report-2026-11-17-gaps-and-fixes.md): a title share carries the method it was
    made with. On 2026-11-16 three method changes reached the live figures at three different moments, and a session
    quoted new constants on old lines as "tonight's engine"."""

    def _day(self, rec=None, registry=b'{"constants": []}'):
        import hashlib
        d = tempfile.mkdtemp()
        if rec is not None:
            json.dump(rec, open(os.path.join(d, "season_lines_2026-11-17.json"), "w"))
        r = os.path.join(d, "registry.json"); open(r, "wb").write(registry)
        return d, r, hashlib.sha256(registry).hexdigest()

    def test_the_stamp_names_the_engine_the_line_method_and_the_registry(self):
        d, r, sha = self._day(dict(date="2026-11-17", line_switch=dict(cats=["pts", "reb", "ast"])))
        m = DB.method_stamp("2026-11-17", season_dir=d, registry=r, engine="ecb60cb")
        self.assertEqual(m["line"], f"Method: deck engine ecb60cb; line method: minutes ratio on PTS, REB, AST; constants registry {sha[:12]}")
        self.assertEqual((m["engine"], m["line_switch"], m["registry_sha256"]), ("ecb60cb", ["PTS", "REB", "AST"], sha))

    def test_no_ratio_and_no_record_read_differently(self):
        d, r, _ = self._day(dict(date="2026-11-17"))
        self.assertIn("line method: blend only (no minutes ratio)", DB.method_stamp("2026-11-17", season_dir=d, registry=r, engine="ecb60cb")["line"])
        d, r, _ = self._day(None)
        m = DB.method_stamp("2026-11-17", season_dir=d, registry=r, engine="ecb60cb")
        self.assertIn("line method: no season-lines record for the day", m["line"]); self.assertIsNone(m["line_switch"])

    def test_a_changed_constant_changes_the_stamp_and_nothing_else_does(self):
        rec = dict(date="2026-11-17", line_switch=dict(cats=["pts"]))
        d, r, _ = self._day(rec); a = DB.method_stamp("2026-11-17", season_dir=d, registry=r, engine="ecb60cb")
        d2, r2, _ = self._day(rec); self.assertEqual(a["line"], DB.method_stamp("2026-11-17", season_dir=d2, registry=r2, engine="ecb60cb")["line"])
        d3, r3, _ = self._day(rec, registry=b'{"constants": [{"name": "TEAM_WEEK_SHOCK", "value": 0.11}]}')
        self.assertNotEqual(a["line"], DB.method_stamp("2026-11-17", season_dir=d3, registry=r3, engine="ecb60cb")["line"])

    def test_what_cannot_be_read_is_said(self):
        d, _, _ = self._day(dict(date="2026-11-17"))
        m = DB.method_stamp("2026-11-17", season_dir=d, registry=os.path.join(d, "absent.json"), engine="")
        self.assertIn("deck engine not readable", m["line"]); self.assertIn("constants registry not readable", m["line"])
        self.assertIsNone(m["registry_sha256"])

    def test_the_title_section_prints_the_stamp(self):
        self.assertEqual(DB.method_md(dict(line="Method: deck engine ecb60cb; x")), ["- Method: deck engine ecb60cb; x"])
        self.assertEqual(DB.method_md(None), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)


class WaiverNotes(unittest.TestCase):
    """Owner pick 2026-11-03 (display only): the suffix on a scan pair or streaming line, and the record fields."""
    INFO = {"read": True, "by": {"Julian Champagnie": {"waiver_date": "2026-11-04", "own_drop_date": "2026-11-03"},
                                 "Kris Dunn": {"waiver_date": "2026-11-02", "own_drop_date": None},
                                 "Bobby Portis": {"waiver_date": None, "own_drop_date": "2026-11-01"}}}

    def test_the_suffix_reads_as_the_build_order_says(self):
        self.assertEqual(DB.waiver_note("Julian Champagnie", self.INFO), "on waivers until 2026-11-04 · you dropped him 2026-11-03")
        self.assertEqual(DB.waiver_note("Kris Dunn", self.INFO), "on waivers until 2026-11-02")
        self.assertEqual(DB.waiver_note("Bobby Portis", self.INFO), "you dropped him 2026-11-01")
        self.assertEqual(DB.waiver_note("Tobias Harris", self.INFO), "")
        self.assertEqual(DB.waiver_note("Tobias Harris", None), "")

    def test_the_record_gains_two_fields_and_nothing_else_moves(self):
        rows = [{"add": "Julian Champagnie", "d_ecw": 0.03}, {"add": "Tobias Harris", "d_ecw": 0.02}]
        before = [dict(r) for r in rows]
        DB.annotate_waivers(rows, "add", self.INFO)
        self.assertEqual(rows[0]["add_waiver_date"], "2026-11-04"); self.assertEqual(rows[0]["add_own_drop_date"], "2026-11-03")
        self.assertIsNone(rows[1]["add_waiver_date"]); self.assertIsNone(rows[1]["add_own_drop_date"])
        for r, b in zip(rows, before):
            self.assertEqual({k: v for k, v in r.items() if not k.startswith("add_waiver") and k != "add_own_drop_date"}, b)


class TeamRoster(unittest.TestCase):
    """Owner 2026-11-10 (audit F1): one roster build, co_gm.team_roster, for the simulator, the Monday fit and the
    week card's season cost. strict=False skips a name with no line (the fit and the week card read frozen or older
    lines); strict=True is rosters() as it was."""
    BY = {n: {"player": n} for n in ("A", "Auto Guy", "Hurt Auto")}
    T = {"seat": 10, "players": [{"player": "A", "slot": "PG"}, {"player": "Gone", "slot": "SG"}, {"player": "Hurt", "slot": "IL"}],
         "unpooled": [dict(player="Auto Guy", slot="BN"), dict(player="Nobody", slot="BN"), dict(player="Hurt Auto", slot="IL")]}

    def test_lenient_build_skips_names_without_a_line_and_adds_auto_rows(self):
        self.assertEqual([p["player"] for p in CG.team_roster(self.T, self.BY, strict=False)], ["A", "Auto Guy"])
        self.assertEqual([p["player"] for p in CG.team_roster(self.T, self.BY, include_il=True, strict=False)], ["A", "Auto Guy", "Hurt Auto"])

    def test_strict_build_is_the_simulators_and_refuses_a_missing_line(self):
        ok = dict(self.T, players=[{"player": "A", "slot": "PG"}])
        self.assertEqual(CG.team_roster(ok, self.BY), CG.rosters({"teams": [ok]}, self.BY)[10])
        with self.assertRaises(KeyError):
            CG.team_roster(self.T, self.BY)


class PoolGuard(unittest.TestCase):
    """Owner 2026-11-10 (audit F4, council ruling): the simulator reads SEASON_POOL when it runs, not when the pool
    was loaded; a pool changed in between is refused, never played silently (the 11-10 title-drop trace ran two rows
    on the wrong pool that way)."""
    def setUp(self):
        self.old = os.environ.get("SEASON_POOL")
        self.season = os.path.join(CG.KIT, "data", "season", "pool_season.csv")
        if not os.path.exists(self.season):
            self.skipTest("no season pool written")

    def tearDown(self):
        os.environ.pop("SEASON_POOL", None)
        if self.old is not None:
            os.environ["SEASON_POOL"] = self.old
        CG.load_pool()

    def test_a_pool_changed_after_the_load_is_refused_before_the_simulator_starts(self):
        import shutil, tempfile
        d = tempfile.mkdtemp(); other = os.path.join(d, "pool_other.csv"); shutil.copyfile(self.season, other)
        os.environ["SEASON_POOL"] = self.season
        CG.load_pool()
        os.environ["SEASON_POOL"] = other
        calls = []
        real = CG.subprocess.run
        CG.subprocess.run = lambda *a, **k: calls.append(a) or (_ for _ in ()).throw(AssertionError("simulator started"))
        try:
            with self.assertRaises(RuntimeError) as e:
                CG.run_league_sim({10: []}, 2026, 10, d)
        finally:
            CG.subprocess.run = real
        self.assertEqual(calls, [])
        self.assertIn("pool_season.csv", str(e.exception)); self.assertIn("pool_other.csv", str(e.exception))

    def test_the_same_pool_passes_the_guard(self):
        os.environ["SEASON_POOL"] = self.season
        CG.load_pool()
        self.assertIsNone(CG.pool_guard())

    def test_the_preseason_pool_passes_when_none_is_named(self):
        os.environ.pop("SEASON_POOL", None)
        CG.load_pool()
        self.assertIsNone(CG.pool_guard())


class SimPatch(unittest.TestCase):
    """Owner 2026-11-10 (decision card, P2): run_league_sim can hand the simulator a constants patch (league_sim
    --patch, as the Monday sweep does), so a pair can be re-scored under the declared band. No patch: the command
    is as before."""
    def _cmd(self, **kw):
        import json as J, tempfile
        CG.load_pool()          # the pool guard compares against the last load: load under this test's own environment
        d = tempfile.mkdtemp(); seen = []
        real = CG.subprocess.run
        def fake(cmd, **k):
            seen.append(list(cmd))
            J.dump({"teams": {"10": {"champ": 1.0}}}, open(cmd[6], "w"))
            if "--patch" in cmd:
                seen.append(J.load(open(cmd[cmd.index("--patch") + 1])))
        CG.subprocess.run = fake
        try:
            CG.run_league_sim({10: []}, 2026, 10, d, **kw)
        finally:
            CG.subprocess.run = real
        return seen, d

    def test_a_patch_reaches_the_simulator_and_its_file_is_removed(self):
        seen, d = self._cmd(patch={"weekly_availability": {"risk": 0.65}}, tag="t")
        self.assertIn("--patch", seen[0]); self.assertEqual(seen[1], {"weekly_availability": {"risk": 0.65}})
        self.assertEqual(os.listdir(d), [])

    def test_no_patch_no_flag(self):
        seen, _ = self._cmd()
        self.assertNotIn("--patch", seen[0])
