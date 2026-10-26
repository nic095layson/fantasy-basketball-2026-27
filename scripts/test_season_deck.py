#!/usr/bin/env python3
"""season_deck.py red-first tests: the deck page is rendered solely from named records, embeds them verbatim,
halts on a missing record, joins ownership mechanically, and shows the structural band and zero-states."""
import json, os, re, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import season_deck as SD
import deck_render_check as DRC

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
        dict(name="MY TEAM", seat=10, manager="David", players=[dict(player="Alpha Man", slot="PG", status="P", positions=["PG"]),
                                                                dict(player="Bench Guy", slot="BN", status=None, positions=["PF"])],
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

    def test_every_fragile_band_is_on_the_page(self):
        # 2026-10-21 (owner "implement fixes", decision 2): the sweep on deck 80eecdf tiers two constants FRAGILE;
        # the page must carry every one the record names, not a hardcoded TEAM_WEEK_SHOCK (daily_brief's rule).
        two = dict(engine_commit="80eecdf", fragile=["arena.TEAM_WEEK_SHOCK", "arena.weekly_availability"],
                   constants={"arena.TEAM_WEEK_SHOCK": dict(tier="FRAGILE", variants=[
                                  dict(label="no shared games shock (0.0)", shift_mean=2.71),
                                  dict(label="shared games shock doubled (0.12)", shift_mean=-3.62)]),
                              "arena.weekly_availability": dict(tier="FRAGILE", variants=[
                                  dict(label="no in-sim injury discount", shift_mean=-2.68),
                                  dict(label="harsher risk tier (0.65)", shift_mean=0.47)]),
                              "arena.PCT_MIX_INFL": dict(tier="SENSITIVE", variants=[
                                  dict(label="inflation 1.30", shift_mean=-1.06)])})
        json.dump(two, open(self.fx["sweep"], "w"))
        html, data, rec = self.build()
        m = re.search(r'<script id="deck-data" type="application/json">(.*?)</script>', html, re.S)
        emb = json.loads(m.group(1))
        self.assertEqual([b["name"] for b in emb["bands"]], ["arena.TEAM_WEEK_SHOCK", "arena.weekly_availability"])
        self.assertEqual([v["shift"] for v in emb["bands"][1]["variants"]], ["-2.7", "+0.5"])
        self.assertNotIn("PCT_MIX_INFL", json.dumps(emb["bands"]))
        self.assertIn("D.bands", html)

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

    def test_board_search_box_survives_rerender_and_board_has_reset(self):
        # owner 2026-10-20: typing in the Board search lost focus on every character, because render() rebuilt the
        # input; it is now built once, outside render(), and only the table holder is replaced. Plus a Reset button.
        html, data, rec = self.build()
        board = html.split('$("#pane-board")')[1].split("// ---- Movers")[0]
        before_render = board.split("function render(){")[0]
        self.assertIn('id:"bd-q"', before_render)
        self.assertIn('id:"bd-fa"', before_render)
        self.assertNotIn("box.replaceChildren", board)
        self.assertIn('id:"bd-reset"', board)
        self.assertNotIn("tbl.replaceChildren(\n      h(", board)  # a bare null child prints "null" (Chromium-checked)

    def test_my_positional_breakdown_counts_eligibility_and_families_by_hand(self):
        # owner 2026-10-26: the Free Agents tab shows my roster's positional breakdown as the Draft Deck does —
        # the top row counts every position a player is eligible for, the bottom row counts each player once per
        # family (G = PG or SG, F = SF or PF; the deck's rule, test_draft.py "G (4) F (2) C (2)"). IL players count.
        players = [dict(player="A", slot="PG", positions=["PG", "SG"]), dict(player="B", slot="SG", positions=["SG", "SF", "PF"]),
                   dict(player="C", slot="C", positions=["C"]), dict(player="D", slot="IL", positions=["PF", "C"]),
                   dict(player="E", slot="BN", positions=["SF"])]
        bd = SD.positional_breakdown(players)
        self.assertEqual(bd["positions"], dict(PG=1, SG=2, SF=2, PF=2, C=2))   # by hand from the five rows
        self.assertEqual(bd["families"], dict(G=2, F=3, C=2))                 # A,B guards; B,D,E forwards; C,D centers
        self.assertEqual((bd["rostered"], bd["il"]), (5, 1))
        with self.assertRaises(SD.DeckError):                                   # a token the kit does not know is never a silent 0
            SD.positional_breakdown([dict(player="X", slot="BN", positions=["G"])])

    def test_the_fa_tab_carries_my_positional_breakdown(self):
        html, data, rec = self.build()
        bd = data["league"]["my_positions"]
        self.assertEqual(bd["positions"], dict(PG=1, SG=0, SF=0, PF=1, C=0))   # fixture: Alpha Man PG, Bench Guy PF
        self.assertEqual(bd["families"], dict(G=1, F=1, C=0))
        self.assertIn('id:"fa-positions"', html)                                    # the page builds the block in script
        self.assertIn("my_positions", html)

    def test_my_held_players_are_named_on_trade_and_fa(self):
        # owner 2026-10-20: "I have Max Strus on my IL but he is not showing up" -> option (b): my side of the Trade
        # and FA panes names my rostered players held off the board (display only; the line already exists for theirs)
        html, data, rec = self.build()
        self.assertIn("function myHeld(", html)
        trade = html.split('$("#pane-trade")')[1].split('$("#pane-fa")')[0]
        fa = html.split('$("#pane-fa")')[1].split("// ---- Board")[0]
        self.assertIn("myHeld()", trade); self.assertIn("myHeld()", fa)

    def test_odds_tiles_show_the_two_run_average_not_seed_labels(self):
        # owner 2026-10-20: "Please relabel them, or just provide the average"
        html, data, rec = self.build()
        shell = re.sub(r'<script id="deck-data".*?</script>', "", html, flags=re.S)
        self.assertNotIn('"seed "', shell)
        self.assertIn("const avg2=", shell)

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



class WeekTabCurrentNames(Deck):
    """Owner 2026-10-20 ("Merge 145 to correct to KEVIN", option a): the Week tab shows each
    opponent's CURRENT team name (by seat, from the live board), while the ledger record itself
    stays frozen as written."""

    def test_week_rows_resolve_the_opponent_name_by_seat(self):
        html, data, rec = self.build()
        self.assertIn("seatName", html)
        # the row no longer prints the frozen name directly
        self.assertNotIn('h("td",{},w.opponent_team+" ("', html)


class FantasyBotCards(Deck):
    """Owner 2026-10-20 ("1, 2, 5 build"): the Trades-worth-proposing card and the This-week-live
    card render from data/news records when present, and FantasyBot's verdict text never appears."""

    def test_live_card_renders_from_the_optional_record(self):
        import json as J
        self.fx["matchup_live"] = os.path.join(self.d, "ml.json")
        J.dump({"date": "2026-10-21", "week": 1, "my_left_to_play": 30, "opp_left_to_play": 37,
                "games_in_progress": False, "opp_team": "OPP", "my_team": "ME",
                "my_starters": [], "opp_starters": []}, open(self.fx["matchup_live"], "w"))
        html, data, rec = self.build()
        self.assertIn("This week", html)
        self.assertEqual(data["matchup_live"]["opp_left_to_play"], 37)
        # owner veto 2026-10-20: no hypothetical-trade card, ever
        self.assertNotIn("Trades worth proposing", html)
        self.assertNotIn("7% to win", html)

    def test_missing_records_render_nothing_and_do_not_halt(self):
        html, data, rec = self.build()
        self.assertIsNone(data["matchup_live"])

    def test_a_named_but_absent_optional_input_builds_and_is_recorded_absent(self):
        # GAUNTLET 2026-10-21 decision 4: the real morning names data/news/matchup_live_<date>.json via
        # default_paths even when no matchup pull ran; the record hashed every path and the build crashed
        self.fx["matchup_live"] = os.path.join(self.d, "no_matchup_live_today.json")
        html, data, rec = self.build()
        self.assertIsNone(data["matchup_live"])
        self.assertIs(rec["inputs"]["matchup_live"]["present"], False)
        self.assertIsNone(rec["inputs"]["matchup_live"]["sha256"])
        self.assertIs(rec["inputs"]["board"]["present"], True)
        self.assertEqual(len(rec["inputs"]["board"]["sha256"]), 64)

def real_movers_lines(d):
    """The movers record as season_lines.py writes it, not a hand-typed copy: one pooled player, three big
    regular-season games, run through season_lines.run. Each mover's `moved` is {stat: [preseason, season]} strings.
    The 10/21 crash came from a fixture that never had a mover (after-report-2026-10-21-board-test.md §3)."""
    import csv
    import season_lines as SL
    kit, deck = os.path.join(d, "kit.csv"), os.path.join(d, "deck.csv")
    for path, row in ((kit, dict(name="Alpha Man", team="DEN", pos="C", gp="72", mpg="34.0", fgp="0.550", fga="16.0",
                                  ftp="0.800", fta="5.0", tpm="1.0", pts="25.0", reb="12.0", ast="9.0", stl="1.5",
                                  blk="0.8", tov="3.0")),
                      (deck, dict(player="Alpha Man", team="DEN", pos="C", fg_pct="0.550", fga="16.0", ft_pct="0.800",
                                  fta="5.0", tpm="1.0", pts="25.0", reb="12.0", ast="9.0", stl="1.5", blk="0.8",
                                  tov="3.0", note=""))):
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(row)); w.writeheader(); w.writerow(row)
    game = dict(min=36, pts=40, fgm=15, fga=22, tpm=3, tpa=6, ftm=7, fta=8, reb=16, ast=12, tov=6, stl=3, blk=2)
    rec = dict(date="2026-10-21", games=[dict(espn_id=str(i), season_type=2) for i in range(3)],
               players=[dict(game, name="Alpha Man", pool_name="Alpha Man", team="DEN", dnp=False, game=str(i))
                        for i in range(3)])
    out = SL.run(date="2026-10-21", actuals=[rec], kit_csv=kit, deck_csv=deck, out_dir=d)
    return os.path.join(d, "season_lines_2026-10-21.json"), out


RENDER_OK, RENDER_WHY = DRC.available()


@unittest.skipUnless(RENDER_OK, RENDER_WHY)
class RealMoversRender(unittest.TestCase):
    """Decision A (owner 2026-10-21): with real movers the page draws all six tabs and each moved stat reads
    preseason → season under its category name."""
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.fx = fixtures(self.d)
        self.fx["season_lines"], self.lines = real_movers_lines(self.d)
        self.assertTrue(self.lines["movers"])  # the producer really wrote movers

    def test_the_page_draws_itself_with_real_movers(self):
        html, data, rec = SD.build(self.fx, date="2026-10-21")
        p = os.path.join(self.d, "deck.html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(html)
        res = DRC.check(p)
        self.assertEqual(res["status"], "PASS", res["reasons"])
        movers = res["panes"]["movers"]
        self.assertIn("Alpha Man", movers)
        moved = self.lines["movers"][0]["moved"]
        labels = {"pts": "PTS", "fgp": "FG%", "reb": "REB", "ast": "AST", "tov": "TOV"}
        for col, label in labels.items():
            self.assertIn(col, moved)
            x, y = moved[col]
            self.assertIn(f"{label} {x} → {y}", movers)
        self.assertNotIn(" z and over", movers)


@unittest.skipUnless(RENDER_OK, RENDER_WHY)
class PublishOnlyWhatDraws(unittest.TestCase):
    """Decision B (owner 2026-10-21): main() writes deck_<date>.html only after the page drew itself; a page that fails
    is kept as deck_<date>.failed.html and the step FAILs, so the morning run has nothing broken to publish."""
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.fx = fixtures(self.d); self.out = os.path.join(self.d, "out")
        self._build = SD.build

    def tearDown(self):
        SD.build = self._build

    def run_main(self):
        argv = sys.argv
        sys.argv = ["season_deck.py", "--date", "2026-10-21", "--out", self.out]
        try:
            SD.main()
        finally:
            sys.argv = argv

    def test_a_page_that_cannot_draw_itself_is_never_written_as_the_deck(self):
        html, data, rec = self._build(self.fx, date="2026-10-21")
        broken = html.replace("// ---- tabs, footer ----", "null.toFixed(); // ---- tabs, footer ----")
        self.assertNotEqual(broken, html)
        SD.build = lambda paths, date: (broken, data, rec)
        with self.assertRaises(SystemExit) as cm:
            self.run_main()
        self.assertEqual(cm.exception.code, 1)
        self.assertFalse(os.path.exists(os.path.join(self.out, "deck_2026-10-21.html")))
        self.assertTrue(os.path.exists(os.path.join(self.out, "deck_2026-10-21.failed.html")))
        self.assertFalse(os.path.exists(os.path.join(self.out, "deck_2026-10-21.check.html")))

    def test_a_page_that_draws_itself_is_written_and_its_render_recorded(self):
        built = self._build(self.fx, date="2026-10-21")
        SD.build = lambda paths, date: built
        self.run_main()
        self.assertTrue(os.path.exists(os.path.join(self.out, "deck_2026-10-21.html")))
        rec = json.load(open(os.path.join(self.out, "deck_record_2026-10-21.json")))
        self.assertEqual(rec["render"]["status"], "PASS")
        self.assertEqual(rec["render"]["tabs"], DRC.TABS)
        self.assertEqual(rec["render"]["page_errors"], 0)


WM_CATS = ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]


def week_matchup_record(pickups=None):
    """A week_matchup.py-shaped record (owner 2026-10-21): to-date actuals, projected finals, leaders, pickups."""
    cats = [dict(cat=c, me_to_date=(0.5 if "%" in c else 20 + i), opp_to_date=(0.388 if "%" in c else 30 + i),
                 me_final=(0.493 if "%" in c else 500.5 + i), opp_final=(0.455 if "%" in c else 600.5 + i),
                 leader_to_date="opp", leader=("me" if c in ("FG%", "TO") else "opp"), margin=1.0)
            for i, c in enumerate(WM_CATS)]
    return dict(date="2026-10-21", week=1, window=["2026-10-20", "2026-10-25"], me=dict(name="MY TEAM", seat=10),
                opponent=dict(name="THEM", seat=11), to_date_days=["2026-10-20"], missing_days=[],
                remaining_days=["2026-10-21", "2026-10-22"], status_file="status_2026-10-21.json", cats=cats,
                projected=dict(wins=2, losses=7, ties=0),
                games=dict(me=dict(to_date_counted=2, remaining_started=32, remaining_uncapped=33),
                           opp=dict(to_date_counted=5, remaining_started=36, remaining_uncapped=36)),
                pickups=pickups or dict(status="no finished low-value player", drop_candidates=[], top=[], pool_size=0,
                                        drop=None, next_finish=[dict(player="Bench Guy", team="BOS", last_game="2026-10-23", value=-1.49)]),
                method=dict(to_date="reconstructed from box scores"))


RAN = dict(status="ran", pool_size=154, next_finish=[],
           drop=dict(player="Bench Guy", team="BOS", value=-1.49, value_rank=10, of=13),
           drop_candidates=[dict(player="Bench Guy", team="BOS", value=-1.49, value_rank=10, of=13)],
           top=[dict(add="Free Agent", team="GSW", value=0.4, games_left=3, starts=3, net=1.0, flips_to_win=["BLK"],
                     flips_to_loss=[], gap_closed=1.0, missed=None),
                dict(add="Hurt Guy", team="DEN", value=0.1, games_left=2, starts=2, net=0.0, flips_to_win=[],
                     flips_to_loss=[], gap_closed=0.4, missed="2026-10-20")])


TW = dict(status="ran", drops=["Bench Guy"], pool_size=2, no_games=["Idle Man"], drop_alone={"Bench Guy": -0.03},
          rows=[dict(add="Free Agent", team="GSW", drop="Bench Guy", d_exp=0.54, d_exp_drop=-0.03, d_exp_add=0.57,
                     d_cat={"FG%": 0.01, "FT%": 0.0, "3PTM": 0.0, "PTS": -0.02, "REB": 0.12, "AST": 0.0, "ST": 0.0,
                            "BLK": 0.43, "TO": 0.0}, games=3, games_left=3, value=0.4, status=None, missed=None,
                     season_d_ecw=0.0123),
                dict(add="Other FA", team="LAL", drop="Bench Guy", d_exp=0.1, d_exp_drop=-0.03, d_exp_add=0.13,
                     d_cat={"FG%": 0.0, "FT%": 0.0, "3PTM": 0.0, "PTS": 0.1, "REB": 0.0, "AST": 0.0, "ST": 0.0,
                            "BLK": 0.0, "TO": 0.0}, games=2, games_left=2, value=1.1, status=None, missed=None,
                     season_d_ecw=0.031)])


def fa_positions_dom(html_path, tick=()):
    """The Free Agents pane's positions block in the browser, after ticking the named players' boxes in order."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b, exe, tried = DRC._launch(p)
        try:
            pg = b.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.route(re.compile(r"^https?://"), lambda r: r.abort())
            pg.goto("file://" + os.path.abspath(html_path), wait_until="load")
            for name in tick:
                pg.evaluate("(n) => { const l=[...document.querySelectorAll('#pane-fa .plist label')].find(x => x.textContent.startsWith(n+' ')); l.querySelector('input').click(); }", name)
            return dict(errors=errs, text=pg.evaluate("() => document.getElementById('fa-positions').textContent"))
        finally:
            b.close()


def fa_dom(html_path, sort=None):
    """The Free Agents pane read in the browser; sort, if given, is chosen in the pane's sort control first."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b, exe, tried = DRC._launch(p)
        try:
            pg = b.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.route(re.compile(r"^https?://"), lambda r: r.abort())
            pg.goto("file://" + os.path.abspath(html_path), wait_until="load")
            if sort:
                pg.select_option("#fa-sort", sort)
            return dict(errors=errs, text=pg.evaluate("() => document.getElementById('pane-fa').textContent"),
                        labels=pg.evaluate("() => { const l=[...document.querySelectorAll('#pane-fa .plist')]; return [...l[l.length-1].querySelectorAll('label')].map(x => x.textContent) }"))  # the "I add" list
        finally:
            b.close()


def today_dom(html_path):
    """The Today pane's faded cells and text, read in the browser (the card is drawn by the page's script)."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b, exe, tried = DRC._launch(p)
        try:
            pg = b.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.route(re.compile(r"^https?://"), lambda r: r.abort())
            pg.goto("file://" + os.path.abspath(html_path), wait_until="load")
            return dict(errors=errs, text=pg.evaluate("() => document.getElementById('pane-today').textContent"),
                        proj=pg.evaluate("() => document.querySelectorAll('#pane-today td.proj').length"),
                        first=pg.evaluate("() => { const c=document.querySelector('#pane-today .card'); return c? c.querySelector('h2').textContent : null }"),
                        proj_color=pg.evaluate("() => { const t=document.querySelector('#pane-today td.proj'); return t? getComputedStyle(t).color : null }"),
                        ink_color=pg.evaluate("() => { const t=document.querySelector('#pane-today td.actual'); return t? getComputedStyle(t).color : null }"))
        finally:
            b.close()


def _row(slot, player, team, today, td=None, games=0, status=None):
    return dict(slot=slot, player=player, team=team, positions=["PG"], status=status, today=today, games=games,
                to_date=None if td is None else dict(dict(fgm=0, fga=0, ftm=0, fta=0, tpm=0, pts=0, reb=0, ast=0, stl=0,
                                                          blk=0, tov=0), **td))


def board_record(match_opp=False):
    """week_matchup_record() with the owner's 2026-10-23 matchup board: two sides by slot, Yahoo's totals, the score."""
    r = week_matchup_record()
    me_tot = dict(fgm=11, fga=24, ftm=4, fta=4, tpm=3, pts=29, reb=10, ast=9, stl=2, blk=1, tov=3)
    opp_tot = dict(fgm=9, fga=20, ftm=5, fta=6, tpm=2, pts=30, reb=12, ast=4, stl=1, blk=2, tov=2)
    r["board"] = dict(score=dict(me=3, opp=6, tie=0),
        me=dict(name="MY TEAM", seat=10, manager="Me", departed=dict(names=[], to_date={k: 0 for k in me_tot}, games=0),
                totals=me_tot, rows_match_totals=True, rows=[
                    _row("PG", "Alpha Man", "DEN", "vs DAL", dict(fgm=8, fga=15, ftm=4, fta=4, tpm=2, pts=22, reb=2, ast=8, stl=1, blk=0, tov=2), 1),
                    _row("C", "Big Guy", "MIL", None, dict(fgm=3, fga=9, tpm=1, pts=7, reb=8, ast=1, stl=1, blk=1, tov=1), 1),
                    _row("BN", "Bench Guy", "BOS", "@ NYK"),
                    _row("IL", "Hurt Guy", "ORL", "vs MIN", status="O")]),
        opp=dict(name="THEM", seat=11, manager="Cayas", departed=dict(names=[], to_date={k: 0 for k in opp_tot}, games=0),
                 totals=opp_tot, rows_match_totals=match_opp, rows=[
                    _row("PG", "Their Guard", "PHI", None, dict(fgm=9, fga=20, ftm=5, fta=6, tpm=2, pts=25, reb=7, ast=4, stl=1, blk=0, tov=2), 1),
                    _row("SF", "Their Wing", "TOR", "@ WAS", dict(reb=5, blk=2), 1),
                    _row("C", "Their Center", "CHI", "@ MIL")]))
    return r


def board_dom(html_path, width=1280):
    """The matchup board read in the browser at a given viewport width."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b, exe, tried = DRC._launch(p)
        try:
            pg = b.new_page(viewport=dict(width=width, height=900)); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.route(re.compile(r"^https?://"), lambda r: r.abort())
            pg.goto("file://" + os.path.abspath(html_path), wait_until="load")
            q = lambda js: pg.evaluate(js)
            return dict(errors=errs,
                first=q("() => { const c=document.querySelector('#pane-today .card'); return c? c.id : null }"),
                text=q("() => { const m=document.getElementById('mboard'); return m? m.textContent : null }"),
                score=q("() => [...document.querySelectorAll('#mboard .mb-score b')].map(x=>x.textContent)"),
                lead=q("() => [...document.querySelectorAll('#mboard .mb-cats td.lead')].map(x=>x.dataset.cat+':'+x.dataset.side)"),
                slots=q("() => [...document.querySelectorAll('#mboard .mb-players td.slot')].map(x=>x.textContent)"),
                cells=q("() => [...document.querySelectorAll('#mboard .mb-players tr')].map(tr=>[...tr.children].map(td=>td.textContent))"),
                page_overflow=q("() => document.documentElement.scrollWidth - window.innerWidth"))
        finally:
            b.close()


class MatchupBoard(unittest.TestCase):
    """Owner 2026-10-23: "take this inspiration [Yahoo's matchup page] ... make this the today page, which should
    update with each morning refresh. Same data being pulled, just build differently visually"."""
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.fx = fixtures(self.d)

    def page(self, record):
        self.fx["week_matchup"] = os.path.join(self.d, "wm.json")
        with open(self.fx["week_matchup"], "w") as f:
            json.dump(record, f)
        html, data, rec = SD.build(self.fx, date="2026-10-21")
        p = os.path.join(self.d, "deck.html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(html)
        return p

    def test_the_board_leads_today_with_both_teams_their_managers_and_the_score(self):
        p = self.page(board_record())
        self.assertEqual(DRC.check(p)["status"], "PASS")
        dom = board_dom(p)
        self.assertEqual(dom["errors"], [])
        self.assertEqual(dom["first"], "mboard")
        self.assertEqual(dom["score"], ["3", "6"])
        for s in ("MY TEAM", "THEM", "Cayas", "Week 1"):
            self.assertIn(s, dom["text"])

    def test_the_category_row_shows_each_sides_totals_and_marks_the_leader(self):
        dom = board_dom(self.page(board_record()))
        # the record's leader_to_date is "opp" in every category (week_matchup_record), so every lead mark is theirs
        self.assertEqual(len(dom["lead"]), 9)
        self.assertTrue(all(x.endswith(":opp") for x in dom["lead"]))
        self.assertIn(".458", dom["text"])            # 11/24, Yahoo-style three places with no leading zero
        self.assertIn("29", dom["text"])

    def test_players_pair_by_slot_with_their_week_line_and_todays_game(self):
        dom = board_dom(self.page(board_record()))
        self.assertEqual(dom["slots"], ["PG", "SF", "C", "BN", "IL"])
        rows = {r[len(r) // 2]: r for r in dom["cells"] if len(r) > 3}   # keyed by the middle (slot) cell
        pg = " ".join(rows["PG"])
        for s in ("Alpha Man", "vs DAL", ".533", "22", "Their Guard", "No game", ".450", "25"):
            self.assertIn(s, pg)
        sf = " ".join(rows["SF"])
        self.assertIn("Their Wing", sf); self.assertIn("Empty", sf)       # no SF on my side
        il = " ".join(rows["IL"])
        self.assertIn("Hurt Guy", il); self.assertIn("O", il)

    def test_a_player_who_has_not_counted_shows_dashes_and_totals_are_yahoos(self):
        dom = board_dom(self.page(board_record()))
        bn = [r for r in dom["cells"] if len(r) > 3 and r[len(r) // 2] == "BN"][0]
        self.assertIn("Bench Guy", " ".join(bn)); self.assertIn("–", " ".join(bn))
        tot = [r for r in dom["cells"] if r and "TOTAL" in r[0]][0]
        self.assertIn("29", tot); self.assertIn("30", tot)

    def test_a_side_whose_rows_do_not_add_to_yahoo_is_named_and_one_that_does_is_not(self):
        text = board_dom(self.page(board_record(match_opp=False)))["text"]
        self.assertIn("THEM: Yahoo's totals differ from the sum of the player rows", text)
        self.assertNotIn("MY TEAM: Yahoo's totals differ", text)
        text = board_dom(self.page(board_record(match_opp=True)))["text"]
        self.assertNotIn("Yahoo's totals differ", text)

    def test_the_board_never_scrolls_the_page_sideways_on_a_phone(self):
        dom = board_dom(self.page(board_record()), width=400)
        self.assertEqual(dom["errors"], [])
        self.assertLessEqual(dom["page_overflow"], 0)

    def test_a_record_without_a_board_draws_no_board(self):
        self.assertIsNone(board_dom(self.page(week_matchup_record()))["text"])


def league_record():
    """league_table.py-shaped record (owner 2026-10-23, Build 1): twelve teams, cumulative totals, ranks, all-play power."""
    import league_table as LT
    teams = [f"Team {i}" for i in range(1, 13)]
    def tot(k):  # Team k: k-shaped so every column orders differently from the power order
        return dict(fgm=40 + k, fga=100 + k, ftm=10 + k, fta=20, tpm=k, pts=100 + 10 * k, reb=50 + (13 - k), ast=20 + k, stl=5 + k % 3, blk=3 + k % 2, tov=20 - k)
    totals = {t: tot(i + 1) for i, t in enumerate(teams)}
    ap = LT.allplay(totals)
    cats = {t: LT.cat_values(x) for t, x in totals.items()}
    rk = LT.ranks(cats)
    cum = {t: dict(seat=i + 1, manager=f"M{i + 1}", mine=(i + 1 == 10), totals=totals[t], weeks=1, cats=cats[t], ranks=rk[t]) for i, t in enumerate(teams)}
    power = sorted([dict(team=t, seat=i + 1, manager=f"M{i + 1}", mine=(i + 1 == 10), allplay=ap[t], actual=dict(w=5, l=4, t=0), actual_pct=5 / 9,
                         luck=5 / 9 - ap[t]["pct"]) for i, t in enumerate(teams)], key=lambda x: -x["allplay"]["pct"])
    for i, x in enumerate(power): x["rank"] = i + 1
    wk = dict(week=1, window=["2026-10-20", "2026-10-25"], status="in_progress", source="yahoo", pull="pull_2026-10-21.json",
              teams={t: dict(seat=i + 1, totals=totals[t], opponent=teams[(i + 1) % 12], score=dict(wins=5, losses=4, ties=0), games_remaining=20)
                     for i, t in enumerate(teams)}, allplay=ap)
    return dict(date="2026-10-21", week=1, window=["2026-10-20", "2026-10-25"], league_state_as_of="2026-10-21", weeks=[wk],
                cumulative=cum, power=power, method=dict(power="all-play"), inputs=dict(pulls={}, state={}))


def league_dom(html_path, clicks=(), width=1280):
    """The League pane read in the browser; clicks = column header labels to click in order."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b, exe, tried = DRC._launch(p)
        try:
            pg = b.new_page(viewport=dict(width=width, height=900)); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.route(re.compile(r"^https?://"), lambda r: r.abort())
            pg.goto("file://" + os.path.abspath(html_path), wait_until="load")
            pg.evaluate("() => document.querySelector('nav.tabs button[data-tab=league]') && document.querySelector('nav.tabs button[data-tab=league]').click()")
            for c in clicks:
                pg.evaluate("(c) => { const th=[...document.querySelectorAll('#lg-table th')].find(x=>x.textContent.replace(/[ ↑↓]/g,'')===c); th.click(); }", c)
            q = lambda js: pg.evaluate(js)
            return dict(errors=errs,
                text=q("() => { const m=document.getElementById('pane-league'); return m? m.textContent : null }"),
                teams=q("() => [...document.querySelectorAll('#lg-table tr td.team')].map(x=>x.dataset.team)"),
                mine=q("() => [...document.querySelectorAll('#lg-table tr.mine td.team')].map(x=>x.dataset.team)"),
                badges=q("() => [...document.querySelectorAll('#lg-table tr.mine .rk')].map(x=>x.textContent)"),
                power=q("() => [...document.querySelectorAll('#lg-power tr td.team')].map(x=>x.dataset.team)"),
                page_overflow=q("() => document.documentElement.scrollWidth - window.innerWidth"))
        finally:
            b.close()


class LeagueTab(unittest.TestCase):
    """Owner 2026-10-23, Build 1: the League tab — every team's cumulative categories, sortable, with a computed power ranking."""
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.fx = fixtures(self.d)

    def page(self, record):
        if record is not None:
            self.fx["league"] = os.path.join(self.d, "league_table.json")
            with open(self.fx["league"], "w") as f:
                json.dump(record, f)
        html, data, rec = SD.build(self.fx, date="2026-10-21")
        p = os.path.join(self.d, "deck.html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(html)
        return p

    def test_default_paths_name_the_days_league_record_and_an_absent_one_builds(self):
        self.assertTrue(SD.default_paths("2026-10-22")["league"].endswith(os.path.join("report", "league", "league_2026-10-22.json")))
        html, data, rec = SD.build(self.fx, date="2026-10-21")
        self.assertIsNone(data["league_table"])
        self.assertEqual(rec["panes"], 7)

    def test_the_tab_lists_twelve_teams_in_power_order_with_my_row_marked_and_rank_badges(self):
        p = self.page(league_record())
        self.assertEqual(DRC.check(p)["status"], "PASS")
        dom = league_dom(p)
        self.assertEqual(dom["errors"], [])
        self.assertEqual(len(dom["teams"]), 12)
        self.assertEqual(dom["teams"], [x["team"] for x in league_record()["power"]])   # default order: power rank
        self.assertEqual(dom["mine"], ["Team 10"])
        self.assertEqual(len(dom["badges"]), 9)
        self.assertEqual(dom["badges"][8], "3")      # Team 10's TO rank: tov 20-k, fewest first -> Team 12 1st, 11 2nd, 10 3rd
        for s in ("Power", "all-play", "M10", "week 1", "to date"):
            self.assertIn(s, dom["text"])

    def test_every_category_column_sorts_on_a_click_turnovers_ascending(self):
        p = self.page(league_record())
        self.assertEqual(league_dom(p, clicks=("TO",))["teams"][0], "Team 12")     # fewest turnovers first
        self.assertEqual(league_dom(p, clicks=("PTS",))["teams"][0], "Team 12")    # most points first
        self.assertEqual(league_dom(p, clicks=("PTS", "PTS"))["teams"][0], "Team 1")
        self.assertEqual(league_dom(p, clicks=("REB",))["teams"][0], "Team 1")     # reb = 50 + (13 - k)
        self.assertEqual(league_dom(p, clicks=("FG%",))["teams"][0], "Team 12")    # (40+k)/(100+k) rises with k

    def test_the_power_card_orders_by_all_play_and_the_page_fits_a_phone(self):
        p = self.page(league_record())
        dom = league_dom(p, width=400)
        self.assertEqual(dom["errors"], [])
        self.assertEqual(dom["power"], [x["team"] for x in league_record()["power"]])
        self.assertLessEqual(dom["page_overflow"], 0)

    def test_no_record_draws_the_tab_with_a_zero_state(self):
        dom = league_dom(self.page(None))
        self.assertEqual(dom["errors"], [])
        self.assertIn("No league record", dom["text"])


class WeekMatchupData(unittest.TestCase):
    """Owner 2026-10-21: the Today tab carries the week's categories; the record is an optional input."""
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.fx = fixtures(self.d)

    def build(self):
        return SD.build(self.fx, date="2026-10-21")

    def test_default_paths_name_the_days_week_matchup_record(self):
        self.assertTrue(SD.default_paths("2026-10-22")["week_matchup"].endswith(
            os.path.join("report", "briefs", "week_matchup_2026-10-22.json")))

    def test_the_record_is_embedded_verbatim(self):
        self.fx["week_matchup"] = os.path.join(self.d, "wm.json")
        with open(self.fx["week_matchup"], "w") as f:
            json.dump(week_matchup_record(), f)
        html, data, rec = self.build()
        self.assertEqual(data["week_matchup"]["cats"][3]["me_final"], 503.5)
        self.assertIs(rec["inputs"]["week_matchup"]["present"], True)

    def test_absent_record_builds_with_none(self):
        self.fx["week_matchup"] = os.path.join(self.d, "none.json")
        html, data, rec = self.build()
        self.assertIsNone(data["week_matchup"])


@unittest.skipUnless(RENDER_OK, RENDER_WHY)
class WeekMatchupCard(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.fx = fixtures(self.d)

    def page(self, record):
        if record is not None:
            self.fx["week_matchup"] = os.path.join(self.d, "wm.json")
            with open(self.fx["week_matchup"], "w") as f:
                json.dump(record, f)
        html, data, rec = SD.build(self.fx, date="2026-10-21")
        p = os.path.join(self.d, "deck.html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(html)
        return p

    def test_the_card_leads_today_with_actuals_and_faded_projections(self):
        p = self.page(week_matchup_record())
        self.assertEqual(DRC.check(p)["status"], "PASS")
        dom = today_dom(p)
        self.assertEqual(dom["errors"], [])
        self.assertIn("Week 1 categories", dom["first"])
        self.assertEqual(dom["proj"], 18)                       # my final and their final, nine categories
        self.assertNotEqual(dom["proj_color"], dom["ink_color"])  # faded: the projection wears its own color
        for s in ("FG%", "BLK", "TO", "0.493", "503.5", "THEM", "2–7–0", "through 2026-10-20"):
            self.assertIn(s, dom["text"])
        self.assertIn("Bench Guy", dom["text"])                 # who finishes next, while nobody has
        self.assertIn("2026-10-23", dom["text"])

    def test_pickups_name_the_drop_the_adds_their_flips_and_a_missed_game(self):
        dom = today_dom(self.page(week_matchup_record(RAN)))
        self.assertEqual(dom["errors"], [])
        for s in ("Bench Guy", "Free Agent", "BLK", "Hurt Guy", "2026-10-20", "154"):
            self.assertIn(s, dom["text"])

    def test_an_active_player_with_no_pool_row_is_named_as_not_counted(self):
        r = week_matchup_record(); r["unpooled_active"] = ["Nobody Pooled"]
        dom = today_dom(self.page(r))
        self.assertIn("Not counted", dom["text"]); self.assertIn("Nobody Pooled", dom["text"])

    def test_no_record_says_so_and_the_page_still_draws(self):
        p = self.page(None)
        self.assertEqual(DRC.check(p)["status"], "PASS")
        self.assertIn("No week-to-date record", today_dom(p)["text"])

    # ---- A and D (owner 2026-10-21): the card says where its to-date column and its pickup pool came from
    def test_yahoos_totals_are_named_as_the_source_and_the_rebuild_agreement_is_stated(self):
        r = week_matchup_record()
        r["to_date_source"] = dict(source="yahoo", reason=None, rebuild_agrees=True, differences=[],
                                   yahoo_games_remaining=dict(me=32, opp=33))
        dom = today_dom(self.page(r))
        self.assertEqual(dom["errors"], [])
        self.assertIn("Yahoo's scoreboard", dom["text"])
        self.assertIn("rebuild agrees on all 11", dom["text"])
        self.assertIn("Yahoo's own count of games left: you 32, them 33", dom["text"])
        self.assertNotIn("rebuilt from box scores", dom["text"])

    def test_a_rebuild_difference_is_named_stat_by_stat(self):
        r = week_matchup_record()
        r["to_date_source"] = dict(source="yahoo", reason=None, rebuild_agrees=False,
                                   differences=[dict(side="me", stat="pts", yahoo=15, rebuild=13)],
                                   yahoo_games_remaining=dict(me=32, opp=33))
        self.assertIn("you PTS Yahoo 15, rebuild 13", today_dom(self.page(r))["text"])

    def test_a_rebuild_fallback_says_why(self):
        r = week_matchup_record()
        r["to_date_source"] = dict(source="rebuild", reason="no Yahoo pull file (pull_2026-10-21.json)",
                                   rebuild_agrees=None, differences=[], yahoo_games_remaining=None)
        text = today_dom(self.page(r))["text"]
        self.assertIn("rebuilt from box scores", text); self.assertIn("no Yahoo pull file", text)

    def test_the_yahoo_pool_names_every_player_it_did_not_score(self):
        k = dict(RAN, pool=dict(source="yahoo", listed=100, ordering="platform_rostered_rate_desc",
                                out=[dict(name="Out Man", team="ORL", status="O")],
                                unknown_status=[dict(name="Letter Man", team="MEM", status="D")],
                                not_projected=[dict(name="New Guy", team="BOS", status=None)],
                                skipped=[dict(name="Held Man", team="BOS", status=None, reason="rostered in the league state")],
                                kit_pool_not_listed=67))
        k["top"] = [dict(k["top"][0], status="Q")] + k["top"][1:]
        text = today_dom(self.page(week_matchup_record(k)))["text"]
        for s in ("Yahoo's available-player list", "100 listed", "Out Man", "Letter Man (D)", "not tiered",
                  "New Guy", "Held Man", "67", "Free Agent (GSW) · Q"):
            self.assertIn(s, text)

    # ---- P1 (owner 2026-10-22, "Full build"): each category's chance, and free agents judged on this week's matchup
    def test_the_card_shows_each_categorys_chance_and_the_expected_categories(self):
        r = week_matchup_record()
        for i, c in enumerate(r["cats"]):
            c["p_win"] = 0.86 if c["cat"] == "BLK" else 0.5
        r["exp_cats"] = 4.86
        dom = today_dom(self.page(r))
        self.assertEqual(dom["errors"], [])
        for s in ("chance", "86%", "4.86"):
            self.assertIn(s, dom["text"])

    def test_the_this_week_scan_names_the_move_its_change_the_drops_share_and_the_season_cost(self):
        k = dict(week_matchup_record()["pickups"], this_week=TW)
        dom = today_dom(self.page(week_matchup_record(k)))
        self.assertEqual(dom["errors"], [])
        for s in ("Free Agent", "for Bench Guy", "+0.54", "BLK +0.43", "REB +0.12", "−0.03", "+0.012", "Idle Man"):
            self.assertIn(s, dom["text"])

    def test_the_free_agent_notice_names_the_add_the_drop_and_the_gap(self):
        # owner 2026-10-22: "if there is a valuable player available in the free agent pull, make this notice to me on
        # the Today tab"
        r = week_matchup_record()
        r["fa_notice"] = dict(rows=[dict(add="Big Pickup", team="LAL", drop="Bench Guy", gap=2.4)],
                              this_week=dict(add="Week Rental", drop="Bench Guy", d_exp=0.34), gap=1.0, d_exp=0.1)
        dom = today_dom(self.page(r))
        self.assertEqual(dom["errors"], [])
        for s in ("Worth a look", "Big Pickup (LAL)", "for Bench Guy", "+2.40", "Week Rental", "+0.34"):
            self.assertIn(s, dom["text"])

    def test_no_notice_card_when_nothing_passes_either_bar(self):
        r = week_matchup_record()
        r["fa_notice"] = dict(rows=[], this_week=None, gap=1.0, d_exp=0.1)
        dom = today_dom(self.page(r))
        self.assertEqual(dom["errors"], [])
        self.assertNotIn("Worth a look", dom["text"])

    def test_the_positions_recount_as_drops_and_adds_are_ticked(self):
        # owner 2026-10-26 (item 3): the header counts follow the picked move. The board row's pos is Yahoo's
        # eligibility (equal for 14/14 rostered and 87/87 board free agents on 10/26). Fixture: Alpha Man PG and
        # Bench Guy PF are mine; Other FA is an SF. Drop Bench Guy, add Other FA -> PF 1->0, SF 0->1, F stays 1.
        b = json.load(open(self.fx["board"]))
        b["board"].append(dict(rank=4, name="Other FA", team="LAL", pos="SF", gp=70.0, z_adj=5.0, z_total=5.0,
                               z={c: 0.5 for c in ["FG%", "FT%", "3PM", "PTS", "REB", "AST", "STL", "BLK", "TOV"]}))
        json.dump(b, open(self.fx["board"], "w"))
        p = self.page(week_matchup_record())
        before = fa_positions_dom(p)
        self.assertEqual(before["errors"], [])
        self.assertIn("PF(1)", before["text"].replace(" ", ""))
        after = fa_positions_dom(p, tick=("Bench Guy", "Other FA"))
        self.assertEqual(after["errors"], [])
        t = after["text"].replace(" ", "")
        self.assertIn("PF(1→0)", t); self.assertIn("SF(0→1)", t)
        self.assertIn("PG(1)", t)                    # untouched counts stay plain
        self.assertIn("F(1)", t)                     # a forward out, a forward in: the family count holds

    def test_free_agents_sort_by_this_week_and_back_to_season_z(self):
        b = json.load(open(self.fx["board"]))
        b["board"].append(dict(rank=4, name="Other FA", team="LAL", pos="SF", gp=70.0, z_adj=5.0, z_total=5.0,
                               z={c: 0.5 for c in ["FG%", "FT%", "3PM", "PTS", "REB", "AST", "STL", "BLK", "TOV"]}))
        json.dump(b, open(self.fx["board"], "w"))
        k = dict(week_matchup_record()["pickups"], this_week=TW)
        p = self.page(week_matchup_record(k))
        week = fa_dom(p)
        self.assertEqual(week["errors"], [])
        self.assertIn("Free Agent", week["labels"][0])       # +0.54 this week, though Other FA has the higher z
        self.assertIn("+0.54", week["labels"][0])
        season = fa_dom(p, sort="z")
        self.assertIn("Other FA", season["labels"][0])

    # ---- owner 2026-10-22 ("Live + pre-week"): the frozen forecast is labelled as such; a live tile sits beside it
    def test_the_odds_card_labels_the_frozen_forecast_and_adds_the_live_tile(self):
        c = json.load(open(self.fx["calibration"])); c["weeks"]["1"]["recorded_at"] = "2026-10-15T20:26:51Z"
        json.dump(c, open(self.fx["calibration"], "w"))
        r = week_matchup_record()
        for x in r["cats"]:
            x["p_win"] = 0.5
        r["exp_cats"], r["p_5plus"] = 4.5, 0.5
        dom = today_dom(self.page(r))
        self.assertEqual(dom["errors"], [])
        for s in ("pre-week forecast", "recorded 2026-10-15", "60.7%", "4.50", "now", "5+ of 9: 50.0%", "independent"):
            self.assertIn(s, dom["text"])
        self.assertNotIn("win week 1", dom["text"].lower().replace("pre-week", ""))

    def test_without_a_live_record_the_live_tile_says_so(self):
        dom = today_dom(self.page(None))
        self.assertEqual(dom["errors"], [])
        self.assertIn("no live record this morning", dom["text"])
        self.assertIn("pre-week forecast", dom["text"])

    def test_the_fantasybot_card_no_longer_calls_the_frozen_figure_live(self):
        html, _, _ = SD.build(self.fx, date="2026-10-21")
        self.assertNotIn("P(win week) — our simulator", html)

    def test_a_malformed_record_shows_its_error_on_the_card_and_every_tab_still_draws(self):
        bad = week_matchup_record(); bad["cats"] = None
        p = self.page(bad)
        res = DRC.check(p)
        self.assertEqual(res["status"], "PASS", res["reasons"])
        self.assertIn("could not be drawn", today_dom(p)["text"])



def form_record():
    """form_board.py-shaped record (owner 2026-10-23): minutes, starts, role and per-36 rates per player from the box scores."""
    def row(name, nba, owner, seat, mine, fa, slot, games, mpg, starts, role, pts36, trend=None):
        return dict(name=name, yahoo_name=name, owner=owner, seat=seat, mine=mine, fa=fa, slot=slot, status=None, nba=nba,
                    games=games, mpg=mpg, starts=starts, role=role, minutes=[mpg] * games if games else [],
                    per36=dict(pts=pts36, reb=5.0, ast=3.0, stl=1.0, blk=0.5, tpm=2.0, tov=2.0) if games else {},
                    per_game={}, fg=dict(made=5, att=10, pct=0.5 if games else None), ft=dict(made=2, att=2, pct=1.0 if games else None),
                    last3_mpg=None, prior_mpg=None, trend=trend)
    rows = [row("Their Star", "NYK", "THEM", 11, False, False, "C", 1, 40.0, 1, "starter", 27.0),
            row("Alpha Man", "DEN", "MY TEAM", 10, True, False, "PG", 2, 33.0, 2, "starter", 19.6),
            row("Free Agent", "GSW", None, None, False, True, None, 1, 20.0, 0, "bench", 18.0),
            row("Bench Guy", "DAL", "MY TEAM", 10, True, False, "BN", 1, 12.0, 0, "bench", 12.0),
            row("Hurt FA", "MIA", None, None, False, True, None, 0, None, 0, None, None)]
    return dict(date="2026-10-21", window=["2026-10-20", "2026-10-21"], league_state_as_of="2026-10-19", pull="pull_2026-10-21.json",
                rows=rows, fa_unresolved=["Nobody Known"], unpooled_with_games=["Mystery Man"],
                counts=dict(rostered=3, free_agents=2, with_games=4, no_game=1, days=2),
                method=dict(source="box scores", rate_base=36, trend_min_games=4, trend_min=6.0, role="starter flag",
                            not_a_projection="the season line stays the per-game line"),
                inputs=dict(actuals={}, state=None, pull=None, pool=None))


def form_dom(html_path, clicks=(), view=None, width=1280):
    """The minutes card on the Movers pane read in the browser; clicks = header labels to click in order; view = the filter."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b, exe, tried = DRC._launch(p)
        try:
            pg = b.new_page(viewport=dict(width=width, height=900)); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.route(re.compile(r"^https?://"), lambda r: r.abort())
            pg.goto("file://" + os.path.abspath(html_path), wait_until="load")
            pg.evaluate("() => document.querySelector('nav.tabs button[data-tab=movers]').click()")
            if view:
                pg.evaluate("(v) => { const s=document.getElementById('fm-view'); s.value=v; s.dispatchEvent(new Event('change')); }", view)
            for c in clicks:
                pg.evaluate("(c) => { const th=[...document.querySelectorAll('#fm-table th')].find(x=>x.textContent.replace(/[ ↑↓]/g,'')===c); th.click(); }", c)
            q = lambda js: pg.evaluate(js)
            return dict(errors=errs,
                text=q("() => { const m=document.getElementById('pane-movers'); return m? m.textContent : null }"),
                names=q("() => [...document.querySelectorAll('#fm-table tr td.name')].map(x=>x.dataset.name)"),
                mine=q("() => [...document.querySelectorAll('#fm-table tr.mine td.name')].map(x=>x.dataset.name)"),
                fa_text=q("() => { const m=document.getElementById('pane-fa'); return m? m.textContent : null }"),
                stamp=q("() => { const e=document.getElementById('hstamp'); return e? e.textContent+' | '+e.title : null }"),
                page_overflow=q("() => document.documentElement.scrollWidth - window.innerWidth"))
        finally:
            b.close()


class FormCard(unittest.TestCase):
    """Owner 2026-10-23: the minutes & role board on the Movers tab, my rows marked, sortable, with a view filter; the
    Free Agents list shows each free agent's minutes per game."""
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.fx = fixtures(self.d)

    def page(self, record):
        if record is not None:
            self.fx["form"] = os.path.join(self.d, "form.json")
            with open(self.fx["form"], "w") as f:
                json.dump(record, f)
        html, data, rec = SD.build(self.fx, date="2026-10-21")
        p = os.path.join(self.d, "deck.html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(html)
        return p

    def test_default_paths_name_the_days_form_record_and_an_absent_one_builds(self):
        self.assertTrue(SD.default_paths("2026-10-22")["form"].endswith(os.path.join("report", "form", "form_2026-10-22.json")))
        html, data, rec = SD.build(self.fx, date="2026-10-21")
        self.assertIsNone(data["form"])
        p = self.page(None)
        self.assertEqual(DRC.check(p)["status"], "PASS")
        self.assertIn("No minutes record", form_dom(p)["text"])

    def test_the_card_lists_players_by_minutes_with_my_rows_marked(self):
        p = self.page(form_record())
        self.assertEqual(DRC.check(p)["status"], "PASS")
        dom = form_dom(p)
        self.assertEqual(dom["errors"], [])
        self.assertEqual(dom["names"], ["Their Star", "Alpha Man", "Free Agent", "Bench Guy", "Hurt FA"])   # mpg desc, no-game last
        self.assertEqual(dom["mine"], ["Alpha Man", "Bench Guy"])
        for s in ("Minutes & role", "33.0", "S 2/2", "B 0/1", "2026-10-20", "per-36", "Nobody Known", "Mystery Man"):
            self.assertIn(s, dom["text"])
        self.assertIn("Updated ", dom["stamp"]); self.assertIn("generated 20", dom["stamp"])   # the build time, top right
        self.assertLessEqual(dom["page_overflow"], 0)

    def test_headers_sort_and_the_view_filters_to_mine_or_free_agents(self):
        p = self.page(form_record())
        self.assertEqual(form_dom(p, clicks=("g",))["names"][0], "Alpha Man")                 # games desc: 2 first
        self.assertEqual(form_dom(p, clicks=("PTS",))["names"][0], "Their Star")              # per-36 pts desc: 27.0
        self.assertEqual(form_dom(p, clicks=("player",))["names"][0], "Alpha Man")           # name asc
        self.assertEqual(form_dom(p, view="mine")["names"], ["Alpha Man", "Bench Guy"])
        self.assertEqual(form_dom(p, view="fa")["names"], ["Free Agent", "Hurt FA"])

    def test_the_free_agent_list_shows_minutes_per_game(self):
        p = self.page(form_record())
        self.assertIn("20.0 min/g (1 g, bench)", form_dom(p)["fa_text"])



def score_record():
    """score_week.py-shaped record (owner 2026-10-24): week 1's morning P(win) graded against the finals."""
    cats = ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]
    day = {c: dict(p=0.7, outcome=1.0, brier=0.09, lead="me", baseline_brier=0.0) for c in cats}
    wk = dict(week=1, window=["2026-10-20", "2026-10-25"], team="MY TEAM", opponent="KEVIN ELEVEN DOUBLES",
              result=dict(won=cats[:5], lost=cats[5:8], tied=cats[8:]), days={"2026-10-22": day, "2026-10-23": day},
              by_day={"2026-10-22": dict(n=9, brier=0.09, baseline_brier=0.0), "2026-10-23": dict(n=9, brier=0.09, baseline_brier=0.0)},
              by_cat={c: dict(n=2, brier=0.09, baseline_brier=0.0, outcome=1.0) for c in cats},
              reliability=[dict(bin="0.6-0.8", n=18, mean_p=0.7, hit_rate=1.0)] + [dict(bin=b, n=0, mean_p=None, hit_rate=None) for b in ("0.0-0.2", "0.2-0.4", "0.4-0.6", "0.8-1.0")],
              n_forecasts=18, brier=0.09, baseline_brier=0.0, skill=-0.09, days_scored=["2026-10-22", "2026-10-23"],
              days_missing=["2026-10-20", "2026-10-21", "2026-10-24", "2026-10-25"], method=dict(outcome="won 1, tied 0.5, lost 0"),
              inputs=dict(week_file="abc", cards={}), scored_at="2026-10-26T12:05:00Z")
    return dict(weeks={"1": wk})


def week_dom(html_path, width=1280):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b, exe, tried = DRC._launch(p)
        try:
            pg = b.new_page(viewport=dict(width=width, height=900)); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.route(re.compile(r"^https?://"), lambda r: r.abort())
            pg.goto("file://" + os.path.abspath(html_path), wait_until="load")
            pg.evaluate("() => document.querySelector('nav.tabs button[data-tab=week]').click()")
            q = lambda js: pg.evaluate(js)
            return dict(errors=errs, text=q("() => document.getElementById('pane-week').textContent"),
                        rows=q("() => [...document.querySelectorAll('#sc-table tr td.wk')].map(x=>x.textContent)"),
                        page_overflow=q("() => document.documentElement.scrollWidth - window.innerWidth"))
        finally:
            b.close()


class Scorecard(unittest.TestCase):
    """Owner 2026-10-24: the Week tab shows how the morning card's P(win) scored against each finished week."""
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.fx = fixtures(self.d)

    def page(self, record):
        if record is not None:
            self.fx["scores"] = os.path.join(self.d, "calibration_daily.json")
            with open(self.fx["scores"], "w") as f:
                json.dump(record, f)
        html, data, rec = SD.build(self.fx, date="2026-10-21")
        p = os.path.join(self.d, "deck.html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(html)
        return p

    def test_default_paths_name_the_record_and_an_absent_one_builds_with_a_pending_line(self):
        self.assertTrue(SD.default_paths("2026-10-22")["scores"].endswith(os.path.join("report", "calibration_daily.json")))
        p = self.page(None)
        self.assertEqual(DRC.check(p)["status"], "PASS")
        dom = week_dom(p)
        self.assertEqual(dom["errors"], [])
        self.assertIn("Scorecard", dom["text"]); self.assertIn("first finals", dom["text"])

    def test_a_scored_week_shows_brier_baseline_skill_and_missing_mornings(self):
        p = self.page(score_record())
        self.assertEqual(DRC.check(p)["status"], "PASS")
        dom = week_dom(p)
        self.assertEqual(dom["errors"], []); self.assertEqual(dom["rows"], ["1"])
        for s in ("0.090", "0.000", "−0.090", "2 of 6 mornings", "5-3-1", "0.6-0.8", "18"):
            self.assertIn(s, dom["text"])
        self.assertLessEqual(dom["page_overflow"], 0)



class UnpooledAndNotStarted(unittest.TestCase):
    """Owner 2026-10-26: the Today tab names unpooled players; the League tab survives a week with no stats yet."""
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.fx = fixtures(self.d)

    def build(self, league_patch=None, league_rec=None):
        if league_patch:
            st = json.load(open(self.fx["league_state"])); st.update(league_patch)
            json.dump(st, open(self.fx["league_state"], "w"))
        if league_rec is not None:
            self.fx["league"] = os.path.join(self.d, "league_table.json"); json.dump(league_rec, open(self.fx["league"], "w"))
        html, data, rec = SD.build(self.fx, date="2026-10-21")
        p = os.path.join(self.d, "deck.html"); open(p, "w", encoding="utf-8").write(html)
        return p, data

    def test_today_names_each_unpooled_player(self):
        p, data = self.build(dict(unpooled=[dict(player="Trevon Brazile", fantasy_team="THEM", seat=11, slot="BN", nba_team="DEN", status=None)]))
        self.assertEqual(data["league"]["unpooled"][0]["player"], "Trevon Brazile")
        self.assertEqual(DRC.check(p)["status"], "PASS")
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b, exe, tried = DRC._launch(pw)
            try:
                pg = b.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.route(re.compile(r"^https?://"), lambda r: r.abort())
                pg.goto("file://" + os.path.abspath(p), wait_until="load")
                txt = pg.evaluate("() => document.getElementById('pane-today').textContent")
            finally:
                b.close()
        self.assertEqual(errs, [])
        self.assertIn("Not in the pool, not simulated: Trevon Brazile (THEM, BN)", txt)

    def test_league_tab_draws_a_not_started_week_without_error(self):
        rec = league_record()
        teams = {t: dict(x, totals=None, not_started=True, score=dict(wins=0, losses=0, ties=9)) for t, x in rec["weeks"][0]["teams"].items()}
        rec["weeks"].append(dict(week=2, window=["2026-10-26", "2026-11-01"], status="not_started", source="yahoo", pull="pull_2026-10-26.json", teams=teams))
        p, data = self.build(league_rec=rec)
        self.assertEqual(DRC.check(p)["status"], "PASS")
        dom = league_dom(p)
        self.assertEqual(dom["errors"], [])
        self.assertIn("week 2 not started", dom["text"])
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b, exe, tried = DRC._launch(pw)
            try:
                pg = b.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.route(re.compile(r"^https?://"), lambda r: r.abort())
                pg.goto("file://" + os.path.abspath(p), wait_until="load")
                pg.evaluate("() => document.querySelector('nav.tabs button[data-tab=league]').click()")
                pg.evaluate("() => { const s=document.querySelector('#pane-league select'); s.value='week'; s.dispatchEvent(new Event('change')); }")
                txt = pg.evaluate("() => document.getElementById('pane-league').textContent")
            finally:
                b.close()
        self.assertEqual(errs, []); self.assertIn("no stats yet", txt)

if __name__ == "__main__":
    unittest.main()
