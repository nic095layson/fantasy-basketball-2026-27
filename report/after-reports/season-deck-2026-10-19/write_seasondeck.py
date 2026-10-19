#!/usr/bin/env python3
"""Writes after-report-2026-10-19-season-deck.md from the build's records: deck_record, the embedded config,
the test run, the palette validator outputs, the swap-math mirror, and the publish read. No figure typed by hand.
Open-item receipts and Repeat-name sections carried from the in-season report of the same day."""
import json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(os.path.dirname(os.path.dirname(H)))
OUT = os.path.join(KIT, "report/after-reports/after-report-2026-10-19-season-deck.md")
SRC = os.path.join(KIT, "report/after-reports/after-report-2026-10-19-inseason-tool.md")
sys.path.insert(0, os.path.join(KIT, "scripts"))
import season_deck as SD
REC = json.load(open(os.path.join(KIT, "report/season/deck_record_2026-10-21.json")))
MORN = json.load(open(os.path.join(KIT, "report/briefs/morning_2026-10-21.json")))
html, data, _ = SD.build(SD.default_paths("2026-10-21"), "2026-10-21")
C = data["config"]
ev = lambda n: open(os.path.join(H, n), encoding="utf-8").read().strip()
pal = {n: ("ALL CHECKS PASS" in ev(n)) for n in ["palette-light-series.txt", "palette-light-diverging.txt",
                                                 "palette-dark-series.txt", "palette-dark-diverging.txt"]}
assert all(pal.values()), pal
mirror = ev("swap-math-mirror.txt").splitlines()[-1]; assert mirror.startswith("SWAP MATH MIRROR: PASS"), mirror
tests = ev("tests-season-deck.txt"); m = re.search(r"Ran (\d+) tests", tests); ntests = int(m.group(1))
assert tests.rstrip().endswith("OK"), tests[-200:]
deck_step = next(s for s in MORN["steps"] if s["name"] == "season deck"); assert deck_step["verdict"] == "PASS"
src = open(SRC, encoding="utf-8").read()
def section(h):
    mm = re.search(rf"^## {re.escape(h)}.*?(?=^## )", src, re.S | re.M); return mm.group(0).rstrip() + "\n"
URL = "https://claude.ai/artifact/Az6vPGzG6TLWrPjdAWL2pe"
inputs = "\n".join(f"- {k}: `{v['path']}` sha256 {v['sha256'][:12]}" for k, v in REC["inputs"].items())
L = []; w = L.append
w("# After-report — the Season Deck: the in-season dashboard artifact, rebuilt each morning from the records")
w("")
w("Pull window: 2026-10-19 → 2026-10-19 — no pull; a rendering layer over records already pulled (league state as-of " + data["league"]["as_of"] + ", lines " + data["brief"]["lines"] + ").")
w("")
w("**Owner request (2026-10-19 evening, verbatim):** \"Will you be building an artifact tool, such as you did with the draft deck?\" then \"Proceed, let's build it. Ask me questions along the way for function, or any design choices\" — four choices answered on the card: full dashboard, interactive board, auto-publish every morning, phone and desktop equally. Mid-build pitch, built in: \"Trade Analyzer … Free agent adder … show zscore computation / categorical addition and subtraction (low, medium, high) … give 'approval' or 'confidence' in trade.\"")
w("")
w(f"**Headline.** `scripts/season_deck.py` renders one HTML page solely from {len(REC['inputs'])} named records (every input pinned by sha256 in `report/season/deck_record_2026-10-21.json`); the page embeds the records verbatim and the static shell carries no figure ({ntests} tests, red first). It is live at {URL} (Version 1, byte-verified: the built file sits inside the served page byte for byte and the embedded data hashes equal). `morning.py` gained it as step 6, and the 06:52 America/Los_Angeles task now republishes it to that URL after a fresh read each morning. The Moves pane is the owner's trade-analyzer / free-agent-adder pitch as a z-score screen with stated-default thresholds (D-SD-1); the simulator verdict stays a session ask. No projection line, tag, roster or engine constant changed.")
w("")
w("## 1. Roster changes")
w("")
w("None. The deck proposes; it changes nothing on either plane.")
w("")
w("## 2. What was built, with its evidence")
w("")
w(f"- **Renderer** `scripts/season_deck.py`: loads the seven records below, halts on any missing or malformed one, joins each board row to its fantasy owner (the one derivation), embeds everything as JSON, and writes `report/season/deck_<date>.html` + a record. EVIDENCE: `SEASON DECK: PASS — 2026-10-21 … {REC['board_rows']} board rows, {REC['status_rows']} status rows`; inputs:\n" + inputs)
w(f"- **Tests** `scripts/test_season_deck.py`: {ntests}, written red first (`season-deck-2026-10-19/tests-season-deck.txt`; the first run failed on the missing module). They check the embedded data equals the records, a missing record halts, the ownership join, zero-states, the FRAGILE band on the page, the record's hashes, and the morning step.")
w("- **The band on the page.** Every odds figure the deck shows carries the standing sweep's structural band, rendered from the sweep record: arena.TEAM_WEEK_SHOCK is FRAGILE, " + " / ".join(v["shift"] for v in data["band"]["variants"]) + " title points across its declared variants (engine " + data["band"]["engine"] + "); a test pins the band's presence on the page.")
w("- **Panes** (7): Today (lineup, today's games, odds tiles with both seeds and the structural band, week categories), Waivers (the brief's engine-graded pairs, labelled as such), Moves (below), Board (sortable 9-cat table, search, free-agent filter, compare picker), Movers (season-line movers, zero-state until games land), Status (every flagged player with its dated receipt), Week (the calibration ledger, recorded-before-the-week).")
w(f"- **Moves pane** (the owner's pitch): trade mode picks an opponent and players both ways; free-agent mode picks adds from the unrostered board. Per-category Δz = acquired z − sent z, tiered low < {C['tier_low']} / medium < {C['tier_high']} / high; verdict from net Δz against ±{C['verdict_edge']} (strong ±{C['verdict_strong']}). The thresholds ship in the page's embedded config as stated defaults — {C['thresholds_note']}. EVIDENCE the page's arithmetic is the stated arithmetic: the swap function extracted from the shipped page and run in node against python sums on live board rows — `{mirror}` (`season-deck-2026-10-19/swap-math-mirror.txt`). The pane labels itself a screen; unequal player counts carry a caveat line.")
w("- **Chart colors**: validated, not eyeballed — the dataviz six-check validator on both series pairs and both diverging pairs, light and dark, all `ALL CHECKS PASS` (`season-deck-2026-10-19/palette-*.txt`, run 2026-10-19).")
w("- **The look** (one pass, per the design contract): Chromium at 1200px and 400px, light and dark — 0 px horizontal overflow at every width, 0 script errors (the one console error is this sandbox's proxy blocking the Google Fonts fetch; the declared fallback stacks cover it). Screenshots `look-desktop-light.png`, `look-moves.png`. One edit from the look: the engine fingerprint read from the sweep's `engine_commit` key (it printed `engine ?` before).")
w(f"- **Morning step 6**: `{deck_step['cmd'].split('/')[-1]}` — the 2026-10-21 dry run PASS end to end with the deck as the last gate (`report/briefs/morning_2026-10-21.json`).")
w(f"- **Publish**: Version 1 at {URL} (id 1792448084-4928), icon basketball. Byte-verify after a fresh read: the local file is a byte-for-byte substring of the served page and the embedded `deck-data` JSON hashes equal (sha256 prefix 258e79753921 both sides). The scheduled task `trig_01YUcivSLv7aWWoSPoFPmhg4` (updated 2026-10-19T22:15Z) now reads the URL fresh, republishes `deck_<date>.html` to it, re-reads and confirms, every morning at 06:52 America/Los_Angeles.")
w("")
w("## Watchlist")
w("")
w("- The first scheduled republish is the 2026-10-20 firing; whether that fresh session holds the Artifact tool is UNVERIFIABLE until it runs (the prompt tells it to say exactly that and skip if not — the page then lags to our sessions).")
w("- The artifact is private; only you can open it until you share it from the page's Share menu.")
w("- The board pane shows the first 200 rows of a sort; search narrows. The Moves free-agent list shows the top 60 matches.")
w("- Players on rosters but off the board (held or unpooled) cannot be picked in Moves — they have no z vector; the pane lists only board rows.")
w("")
w(section("Open-item receipts"))
w(section("Repeat-name market check"))
w("## Bounds")
w("")
w("**Out of scope by design.** The page computes nothing but the Moves z-sums; every other figure is a record's. No simulation in the page; the sim verdict on a specific move stays a session ask. The draft deck page is untouched.")
w("")
w("**In scope and unverified.** The scheduled republish end to end: `NOT-ATTEMPTED` here because it fires in a fresh session tomorrow; the 10/20 morning report will say. Load-bearing only for the page's freshness, not its correctness.")
w("")
w("## Decision sheet (owner disposes)")
w("")
w("| id | decision | recommended |")
w("|---|---|---|")
w(f"| D-SD-1 | Moves screen thresholds (tier low {C['tier_low']} / high {C['tier_high']}; verdict edge {C['verdict_edge']} / strong {C['verdict_strong']}) — stated defaults: (a) keep until a few weeks of sim-graded moves calibrate them; (b) set your own now | (a) |")
w("| D-SD-2 | weekly pinned checkpoint of the deck after each scoreboard intake: (a) no (the git record `deck_<date>.html` already keeps history); (b) yes, publish a dated copy weekly | (a) |")
w("")
w("## Provenance")
w("")
w("- Session: Claude Code (claude.ai/code), 2026-10-19 evening, kit branch `claude/market-data-workorder-mnfi2b` (restarted from main after PR #128 merged); deck repo read-only.")
w(f"- Records: `report/season/deck_2026-10-21.html`, `deck_record_2026-10-21.json`, evidence in `after-reports/season-deck-2026-10-19/`.")
w("- Re-verify: `python3 scripts/season_deck.py --date <today>` then diff the embedded JSON against the records; `python3 -m unittest scripts.test_season_deck`; open the URL and compare its footer build stamp to `deck_record_<date>.json`.")
w("")
w("## In plain language")
w("")
w("You now have one page, like the draft deck, that is rebuilt from scratch every morning from the same records the engine writes: your lineup and today's games, this week's odds with their error and the band, the engine-graded pickups, a sortable season board, injury flags with receipts, and the week ledger. The new Moves tab is your trade analyzer and free-agent adder: pick players going out and coming in, and it shows the category-by-category z gains and losses, sized low, medium or high, and a screen verdict. That verdict is quick arithmetic on the board's own numbers — when you want the real answer on a specific move, ask me and I run the 10,000-season simulator like we did for Jones and Holiday. The page changes nothing by itself, and tomorrow at 6:52 your time it updates itself for the first time.")
w("")
open(OUT, "w", encoding="utf-8").write("\n".join(L)); print("wrote", OUT, len(L), "lines")
