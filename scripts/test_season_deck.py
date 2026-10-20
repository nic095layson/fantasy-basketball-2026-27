#!/usr/bin/env python3
"""season_deck.py red-first tests: the deck page is rendered solely from named records, embeds them verbatim,
halts on a missing record, joins ownership mechanically, and shows the structural band and zero-states."""
import json, os, re, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import season_deck as SD

CATS = ["FG%", "FT%", "3PM", "PTS", "REB", "AST", "STL", "BLK", "TO"]


def fixtures(d):
    j = lambda name, obj: (json.dump(obj, open(os.path.join(d, name), "w")), os.path.join(d, name))[1]
    brief = j("brief.json", dict(date="2026-10-21", week=1, week_window=["2026-10-20", "2026-10-25"],
        league_state_as_of="2026-10-19", status_file="status_2026-10-21.json", lines="v69",
        opponent="KEVIN ELEVEN DOUBLES",
        today=[["Alpha Man", "DEN", "@ LAL", None, 1.0, 3]],
        lineup=[["PG", "Alpha Man"]], bench=[],
        waiver_base_ecw=5.2257, waiver_positive_pairs=8, waiver_pairs_scored=520,
        waiver_top=[dict(add="Free Agent", add_team="GSW", drop="Bench Guy", d_ecw=0.0551,
                         title_seed2026=26.82, d_title_seed2026=1.85)],
        streaming=[], streaming_vs=dict(player="Bench Guy", games_left=3, value_per_game=-2.43),
        title={"2026": 24.97, "2027": 24.56}, playoffs={"2026": 99.26, "2027": 99.4}, seasons=10000))
    board = j("board.json", dict(date="2026-10-21", lines="data/season/projections_season.csv", n_rows=2, held=[],
        board=[dict(rank=1, name="Alpha Man", team="DEN", pos="C", gp=72.0, z_adj=10.19, z_total=11.29,
                    z={c: 1.0 for c in ["FG%", "FT%", "3PM", "PTS", "REB", "AST", "STL", "BLK", "TOV"]}),
               dict(rank=2, name="Free Agent", team="GSW", pos="PF", gp=70.0, z_adj=2.0, z_total=2.5,
                    z={c: 0.2 for c in ["FG%", "FT%", "3PM", "PTS", "REB", "AST", "STL", "BLK", "TOV"]}),
               dict(rank=3, name="Bench Guy", team="DAL", pos="PF", gp=70.0, z_adj=-1.0, z_total=-1.0,
                    z={c: -0.1 for c in ["FG%", "FT%", "3PM", "PTS", "REB", "AST", "STL", "BLK", "TOV"]})]))
    status = j("status.json", dict(date="2026-10-21", league_state_as_of="2026-10-19",
        tiers={"None": ["healthy", 1.0], "Q": ["questionable", 0.5], "O": ["out", 0.0], "P": ["probable", 0.75]},
        espn=dict(ok=False), rows=[dict(player="Alpha Man", fantasy_team="MY TEAM", seat=10, slot="PG",
                                        yahoo_status="P", tier="probable", availability=0.75,
                                        receipts=[dict(source="Yahoo", captured="2026-10-19", text="P beside Alpha Man")])]))
    league = j("league.json", dict(as_of="2026-10-19", teams=[
        dict(name="MY TEAM", seat=10, manager="David", players=[dict(player="Alpha Man", slot="PG", status="P"),
                                                                dict(player="Bench Guy", slot="BN", status=None)],
             empty_slots=[], unpooled_il=[], added_since_draft=[], dropped_since_draft=[]),
        dict(name="THEM", seat=11, manager="Cayas", players=[], empty_slots=[], unpooled_il=[],
             added_since_draft=[], dropped_since_draft=[])]))
    lines = j("season_lines.json", dict(date="2026-10-21", records=1, players_with_games=0,
        prior_games={c: 10.0 for c in CATS}, season_games=65, threshold=0.25, movers=[], unpooled_with_games=[]))
    sweep = j("sweep.json", dict(engine_commit="259c630", constants={"arena.TEAM_WEEK_SHOCK": dict(tier="FRAGILE",
        variants=[dict(label="0", shift_mean=3.4, shift_mean_1dp="+3.4"), dict(label="0.12", shift_mean=-2.3, shift_mean_1dp="-2.3")])}))
    calib = j("calibration.json", dict(weeks={"1": dict(week=1, opponent_seat=11, opponent_manager="Cayas",
        opponent_team="KEVIN ELEVEN DOUBLES", rosters_as_of="2026-10-15", lines="v69", n_per_seed=10000,
        seeds=[2026, 2027], by_seed={"2026": dict(p_win=0.6046, exp_cats=4.9324, cat_p={c: 0.5 for c in ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]}),
                                     "2027": dict(p_win=0.61, exp_cats=4.95, cat_p={c: 0.5 for c in ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]})},
        result="pending")}))
    return dict(brief=brief, board=board, status=status, league_state=league, season_lines=lines,
                sweep=sweep, calibration=calib)


class Deck(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.fx = fixtures(self.d)

    def build(self):
        return SD.build(self.fx, date="2026-10-21")

    def test_embedded_data_equals_the_records(self):
        html, data, rec = self.build()
        m = re.search(r'<script id="deck-data" type="application/json">(.*?)</script>', html, re.S)
        self.assertIsNotNone(m)
        emb = json.loads(m.group(1))
        self.assertEqual(emb["brief"]["title"]["2026"], 24.97)
        self.assertEqual(emb["brief"]["waiver_top"][0]["d_ecw"], 0.0551)
        self.assertEqual(emb["board"]["board"][0]["z"]["REB"], 1.0)
        self.assertEqual(emb["matchup"]["by_seed"]["2026"]["p_win"], 0.6046)

    def test_missing_record_halts(self):
        os.remove(self.fx["board"])
        with self.assertRaises(SD.DeckError): self.build()

    def test_ownership_join_is_mechanical(self):
        html, data, rec = self.build()
        rows = {r["name"]: r for r in data["board"]["board"]}
        self.assertEqual(rows["Alpha Man"]["owner"], "MY TEAM"); self.assertEqual(rows["Alpha Man"]["seat"], 10)
        self.assertIsNone(rows["Free Agent"]["owner"]); self.assertTrue(rows["Free Agent"]["fa"])

    def test_zero_states_and_band(self):
        html, data, rec = self.build()
        self.assertIn("No movers", html)
        self.assertIn("TEAM_WEEK_SHOCK", html); self.assertIn("+3.4", html); self.assertIn("-2.3", html.replace("−", "-"))

    def test_record_pins_every_input(self):
        html, data, rec = self.build()
        for k, p in self.fx.items():
            self.assertIn(k, rec["inputs"]); self.assertEqual(len(rec["inputs"][k]["sha256"]), 64)

    def test_panes_present(self):
        html, data, rec = self.build()
        for pane in ["pane-today", "pane-trade", "pane-fa", "pane-board", "pane-movers", "pane-week"]:
            self.assertIn(f'id="{pane}"', html)
        for gone in ["pane-status", "pane-waivers", "pane-moves"]:  # removed on the owner's calls 2026-10-19
            self.assertNotIn(f'id="{gone}"', html)
        self.assertIn("deck-data", html); self.assertIn("<title>", html)

    def test_managers_embedded_for_every_team(self):
        html, data, rec = self.build()
        self.assertEqual(data["league"]["managers"], {"MY TEAM": "David", "THEM": "Cayas"})
        self.assertEqual(set(data["league"]["managers"]), set(data["league"]["rosters"]))

    def test_build_strips_present_and_il_names_embedded(self):
        # Owner 2026-10-20: BUILD rank strip (1-12 vs the league) on the trade and FA panes; IL players count 0 (D-IS-8),
        # so the page needs each team's IL names in board spelling.
        L = json.load(open(self.fx["league_state"]))
        L["teams"][0]["players"][1]["slot"] = "IL"  # Bench Guy to IL
        json.dump(L, open(self.fx["league_state"], "w"))
        html, data, rec = self.build()
        r = data["league"]["rosters"]["MY TEAM"]
        self.assertEqual(r["il"], ["Bench Guy"])
        self.assertIn("Bench Guy", r["players"])  # pick lists keep him; only the build totals zero him
        self.assertEqual(data["league"]["rosters"]["THEM"]["il"], [])
        # the ids are made at runtime; the shell carries the two buildStrip calls (DOM checked in Chromium)
        self.assertIn('buildStrip("tr-build"', html); self.assertIn('buildStrip("fa-build"', html)
        # owner 2026-10-20: a Reset button clears each pane's picks (and the FA search)
        self.assertIn('id:"tr-reset"', html); self.assertIn('id:"fa-reset"', html)
        # owner 2026-10-20: positions between name and team in the pick lists; FA pool explicitly z-descending
        self.assertIn('r.pos', html.split("pickList(rows")[1][:400])
        self.assertIn('sort((a,b)=>b.z_adj-a.z_adj)', html)

    def test_negative_z_scores_wear_the_negative_color(self):
        # owner 2026-10-20: negative z-scores in red font, so they read apart from positives. Every z render site
        # goes through zv(); a value that rounds to -0.00 is zero and stays uncolored (DOM checked in Chromium).
        html, data, rec = self.build()
        self.assertIn(".zneg{color:var(--negtx)}", html)
        self.assertEqual(html.count("--negtx:"), 3)  # light, dark media, dark toggle
        self.assertIn("function zv(", html)
        for raw in ["f2(r.z_adj)", "f2(a.z_adj)", "f2(b.z_adj)", "f2(r.z[c])", "f2(a.z[c])", "f2(b.z[c])",
                    "sgn(m.d[c])", "sgn(m.net)", "+sgn(v)"]:
            self.assertNotIn(raw, html, raw + " renders a z-score without zv()")

    def test_no_hand_typed_figures_outside_data(self):
        # the static shell (html with the data block stripped) carries no decimal figures from the records
        html, data, rec = self.build()
        shell = re.sub(r'<script id="deck-data".*?</script>', "", html, flags=re.S)
        for lit in ["24.97", "0.0551", "26.82", "5.2257"]:
            self.assertNotIn(lit, shell)


class OwnershipJoin(unittest.TestCase):
    """Owner audit 2026-10-19: rostered players showed as FA because the league state carries the roster's spelling
    (Jaren Jackson Jr., Cameron Johnson) and the season board the kit's (Jaren Jackson Jr, Cam Johnson)."""
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.fx = fixtures(self.d)
        b = json.load(open(self.fx["board"])); L = json.load(open(self.fx["league_state"]))
        z = {c: 0.1 for c in ["FG%", "FT%", "3PM", "PTS", "REB", "AST", "STL", "BLK", "TOV"]}
        for i, n in enumerate(["Jaren Jackson Jr", "Cam Johnson", "Darius Acuff", "Jusuf Nurkic Twin"]):
            b["board"].append(dict(rank=10 + i, name=n, team="UTA", pos="C", gp=70.0, z_adj=0.5, z_total=0.5, z=z))
        b["held"] = ["Jusuf Nurkic"]
        L["teams"][1]["players"] = [dict(player="Jaren Jackson Jr.", slot="C", status=None),
                                    dict(player="Cameron Johnson", slot="SF", status=None),
                                    dict(player="Darius Acuff Jr.", slot="PG", status=None),
                                    dict(player="Jusuf Nurkić", slot="IL", status="O")]
        json.dump(b, open(self.fx["board"], "w")); json.dump(L, open(self.fx["league_state"], "w"))

    def test_spelling_variants_resolve_to_their_board_rows(self):
        html, data, rec = SD.build(self.fx, date="2026-10-21")
        rows = {r["name"]: r for r in data["board"]["board"]}
        for n in ["Jaren Jackson Jr", "Cam Johnson", "Darius Acuff"]:
            self.assertEqual(rows[n]["owner"], "THEM", n); self.assertFalse(rows[n]["fa"], n)
        self.assertTrue(rows["Free Agent"]["fa"])

    def test_rosters_embedded_in_board_spelling_with_off_board_listed(self):
        html, data, rec = SD.build(self.fx, date="2026-10-21")
        r = data["league"]["rosters"]["THEM"]
        self.assertEqual(sorted(r["players"]), ["Cam Johnson", "Darius Acuff", "Jaren Jackson Jr"])
        self.assertEqual(r["off_board"], ["Jusuf Nurkic"])
        self.assertEqual(rec["join"]["rostered"], 6); self.assertEqual(rec["join"]["unresolved"], 0)

    def test_unresolvable_rostered_name_halts(self):
        L = json.load(open(self.fx["league_state"]))
        L["teams"][1]["players"].append(dict(player="Nobody Atall", slot="BN", status=None))
        json.dump(L, open(self.fx["league_state"], "w"))
        with self.assertRaises(SD.DeckError): SD.build(self.fx, date="2026-10-21")

    def test_two_rostered_names_on_one_row_halts(self):
        L = json.load(open(self.fx["league_state"]))
        L["teams"][0]["players"].append(dict(player="Jaren Jackson Jr", slot="BN", status=None))
        json.dump(L, open(self.fx["league_state"], "w"))
        with self.assertRaises(SD.DeckError): SD.build(self.fx, date="2026-10-21")


class Morning(unittest.TestCase):
    def test_morning_has_the_deck_step(self):
        import morning
        st = morning.steps("2026-10-21", fetch=False)
        names = [s["name"] for s in st]
        self.assertIn("season deck", names)
        self.assertEqual(names[-1], "season deck")
        s = next(s for s in st if s["name"] == "season deck")
        self.assertIn("season_deck.py", " ".join(s["cmd"])); self.assertTrue(s["pass_re"].startswith("^SEASON DECK: PASS"))


if __name__ == "__main__":
    unittest.main()
