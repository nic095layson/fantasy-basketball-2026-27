#!/usr/bin/env python3
"""2026-10-12 WO-5: receipts on the two judgment cards that waited on this pass (Rollins, Mathurin); colophon Data
paragraph rewritten for the WO-5 refresh. JUDGMENT date already 2026-10-12. Exact anchors; all-or-nothing."""
import re, sys
sys.path.insert(0, "/home/user/yahoo-fantasy-basketball/scripts")
import hoops, market_prices
P = "/home/user/yahoo-fantasy-basketball/docs/draft-deck.html"
s = open(P, encoding="utf-8").read(); orig = s
assert s.count('const JUDGMENT = {\n  date: "2026-10-12",') == 1
RECEIPTS = {
    "Ryan Rollins": " 10/12 (WO-5): line re-derived by the method — 2025-26 base at 32.1 minutes (17.3 / 4.6 / 5.6; steals 1.7 on the item-8 three-season anchor, outside Yahoo, Hashtag and RotoBaller and kept with that mechanism) (Basketball-Reference; ESPN); the starting role is on the 10/11 box score, so no minutes move; HELD -0.05 — retiring the flag is on the owner's sheet.",
    "Bennedict Mathurin": " 10/12 (WO-5): line re-derived by the method — 2025-26 base (Indiana 28 games, Clippers 26) at 30.0 minutes (Basketball-Reference); outside the top-150 universe, so no role search ran and no minutes moved; HELD -0.05, re-check.",
}
for name, add in RECEIPTS.items():
    key = f'    "{name}": {{ adj: '
    i = s.find(key); assert i >= 0 and s.count(key) == 1, name
    j = s.find('" },', i); assert j > i, name
    s = s[:j] + add + s[j:]
players = hoops.load_players(); n_pool = len(players)
yfile = market_prices.newest_yahoo_file(); prices = market_prices.load_yahoo(yfile)
n_priced, n_unpriced = market_prices.join(players, prices); mdate = market_prices.file_date(yfile)
m = re.search(r"<p><strong>Data\.</strong>.*?</p>", s, re.S); assert m
NEW = (
    f"<p><strong>Data.</strong> Pool refreshed 2026-10-12 under the roster validation lock — {n_pool} rows, every placement "
    f"cross-checked against ESPN’s live rosters (direct-complete, all 30 teams, zero mismatches, {n_pool}/{n_pool} on the feed, no exemption). "
    "This refresh (10/12, the WO-5 projection pass) re-derived every line with an NBA season of 25 or more games by the work order’s method and wrote it to both planes in one asserted script: "
    "rates from the player’s 2025-26 per-36 line on Basketball-Reference (else his latest season of 25+ games), scaled to that season’s minutes unless two dated outlets moved his role "
    "(seven moves — Kevin Porter Jr., Nikola Vučević and Jay Huff to the bench; Naz Reid, Coby White, Ty Jerome and Rui Hachimura to starting roles); FG% and FT% shrunk one-third toward career; "
    "steals and blocks on the three-season anchor; points from the shooting identity. Preseason box scores counted as evidence of role only, never of minutes or rates. "
    "The range rule then brought every top-150 cell that sat outside all of its references (Yahoo 10/6, Hashtag 10/12, RotoBaller 9/29, the player’s own 2025-26 line) back inside or onto a stated mechanism: "
    "ten players’ minutes moved to the outside lines’ range (the returnees Lillard, Davis, Irving, VanVleet, Morant, Young, Haliburton, Dejounte Murray and Edey, and Ty Jerome), with eleven shooting cells and six rookie counting cells; "
    "25 cells stay on the method with their mechanism (the steals/blocks anchor, the career shrink, a season’s per-36 rates). "
    "Rookie lines stay the college translation except where that rule moved them; AJ Dybantsa’s two planes now carry the kit’s line (D-R1), with his and Cameron Boozer’s shot volume set by the points identity. "
    "No tag, games-played figure or placement changed. "
    f"Market: Yahoo’s {mdate} paste prices {n_priced} of {n_pool} rows (ADP, else XRank); the rest ride the internal model.</p>"
)
s = s[:m.start()] + NEW + s[m.end():]
assert s != orig
open(P, "w", encoding="utf-8").write(s)
print("receipts:", len(RECEIPTS), "; colophon Data paragraph rewritten; pool", n_pool, "priced", n_priced, "yahoo", mdate)
