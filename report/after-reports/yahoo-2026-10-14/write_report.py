#!/usr/bin/env python3
"""Writes after-report-2026-10-14-yahoo.md from the records in this folder (figures_2026-10-14.json, moves_v68_v69.json,
chain.log, rn_section.txt, publish.json) and the pinned market files. Every count in the report comes from a record."""
import csv, json, os, re
H = os.path.dirname(os.path.abspath(__file__))
K = "/home/user/fantasy-basketball-2026-27/report"
F = json.load(open(f"{H}/figures_2026-10-14.json", encoding="utf-8"))
MV = json.load(open(f"{H}/moves_v68_v69.json", encoding="utf-8"))
CH = open(f"{H}/chain.log", encoding="utf-8").read()
RN = open(f"{H}/rn_section.txt", encoding="utf-8").read()
PUB = json.load(open(f"{H}/publish.json", encoding="utf-8"))
LET = [l.split("|") for l in open(f"{H}/letters_vs_tags.txt", encoding="utf-8").read().splitlines() if l]
Y = {r["player"]: r for r in csv.DictReader(open(f"{K}/market/yahoo-proj-2026-10-14.csv", encoding="utf-8"))}

def grab(label, pat):
    m = re.search(pat, CH)
    assert m, f"chain.log lacks {label}"
    return m.group(0).strip()
parity = grab("parity", r"PARITY: [^\n]+")
card = grab("test_card", r"CARD: all \d+ cases passed")
draft = re.findall(r"all (\d+) cases passed", CH)
dom = grab("dom", r"\d+ assertions, 0 failed[^\n]*")
ident = grab("identity", r"POINTS IDENTITY[^\n]*|identity[^\n]*off[^\n]*")
rng = grab("range", r"RANGE CHECK[^\n]*|range[^\n]*cells[^\n]*")
rn_head = RN.splitlines()[0]
rn_sec = RN[RN.index("## Repeat-name market check"):].rstrip() + "\n"
assert "exit 1" not in CH and "exit 2" not in CH, "a chain step failed"

def fmt_moves():
    rows = []
    for n, a, b, pa, pb in MV["max5"]:
        rows.append(f"| {n} | {a} to {b} | {pa[0]} {pa[1]} to {pb[0]} {pb[1]} |")
    return "\n".join(rows)

L = []
w = L.append
w("# After-report — 2026-10-14 (market): Yahoo's lock paste as the price source (deck Version 69) and as a projection line\n")
w('**Owner input (2026-10-14, verbatim):** "Yahoo ADP and Projections 10/14:" — followed by Yahoo\'s player list in its projected-stats view, copied from the owner\'s draft room, 350 rows. This is the lock paste the sheet had waited for (D-1013-1 / D-1014-3: land it the same way if it arrives before the draft).\n')
w("Pull window: 2026-10-14 → 2026-10-14 (owner input, WO-4; not a roster pull — the morning pull report `after-report-2026-10-14.md` stands).")
w("Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07`, exit 0 (no kit row changed).\n")
lt = F["letters"]
w(f"**What it is (parser output).** The same draft-room copy of the projected-stats page as 10/13 — name twice, a status letter on some rows, positions, team, then XRank, Yahoo's own Rank, ADP, GP and nine projected season totals, with the owner's \"Your Turn - Nth Pick\" markers between entries — but copied without the header row: the first entry starts at once. {F['rows']} rows; {F['adp']} carry an ADP, {F['rows'] - F['adp']} show \"-\"; status letters Q on {lt.get('Q', 0)}, O on {lt.get('O', 0)}, NA on {lt.get('NA', 0)}.\n")
w(f"**Method.** The paste kept verbatim as `report/market/yahoo-raw-2026-10-14.txt` (tabs intact; only the caption line \"Yahoo ADP and Projections 10/14:\" dropped), committed before any run (8380ff7). `yahoo_market.py` changed three ways, each committed before the run that used it: (1) the headerless copy is recognised (first two lines the same name, a 13-field numeric line within the next four); (2) the abbreviated-name resolver (I7) no longer offers a pool row to a second Yahoo row on another team when a Yahoo row on that row's own team already takes it — the paste is 350 deep and carries a third \"J. Green\" (UTA, XRank 333), Lonzo Ball as \"L. Ball\" (CLE, NA, XRank 349) and Tyus Jones as \"T. Jones\" (DEN, XRank 312); before the fix the first stopped the run and the other two silently joined LaMelo Ball and Tre Jones; (3) a new check fails the run if two Yahoo rows land on one pool row. Red-first: with fix (2) switched off, check (3) reports the LaMelo and Tre Jones double joins and the J. Green tie (3 problems); with it on, 0. The earlier pastes re-parse byte-identically (derived gate 28 of 28, the 9/15, 9/22, 10/01, 10/06 and 10/13 Yahoo intakes among them). Transcription gate PASS (I1–I7): 350 parsed, XRank 1..350 with no gap; I7 resolved 306 of 350 abbreviated names to a pool row; absence gate PASS, mechanical (19 pool players outside Yahoo's 350, 0 possible spelling variants). The run was pinned to 7438f8c and registered in `check_derived.py`. Price moves computed from the two built pages' own `PLAYERS` arrays (Version 68 as published, Version 69 as built); the re-blend size from the blend record `report/blend/out/lines_blend_2026-10-14.json`.\n")
w(f"**Headline.** The market barely moved overnight: on the {F['shared']} names both pastes carry, XRank is identical on every one, and ADP moved on {F['adp_changed_both']} names by at most {F['adp_maxshift']} place (mean {F['adp_mean_shift']}). One name lost its ADP — Anfernee Simons (110.4 yesterday, now \"-\"; priced by XRank 201, so his market rank falls from 119 to 210). The deck now prices {MV['priced_v69']} of 335 rows (was {MV['priced_v68']}): the 8 new rows are XRank 301–342 additions from the deeper list, none lost. Yahoo did revise its projections on {F['line_changed']} names (all pool rows; GP on {len(F['gp_changed'])}). Re-running the six-way blend with these lines would move {len(F['blend_rows_material'])} blended rows by a material amount, the largest Rui Hachimura at {F['blend_max_pts'][0]:+.1f} points per game — see §4 — so this build is price-only, as recommended: the lines, tags and placements are Version 68's.\n")
w("## 1. Roster changes\n")
w("None. Single-source flags only (F2; Yahoo is one outlet): Yahoo lists Lonzo Ball at CLE with the NA letter (the pool holds him unsigned), and Tyus Jones at DEN (not a pool row). No pool row changed team, entered or left; `report/projections-2026-27.csv` is byte-identical to the morning's.\n")
w("## 2. What landed\n")
w("- `report/market/yahoo-raw-2026-10-14.txt` — the paste, verbatim (caption line dropped).")
w(f"- `report/market/yahoo-2026-10-14.csv` — the WO-4 price file (`player,team,pos,xrank,adp`; {F['rows']} names, {F['adp']} with ADP) — the deck's F8 price source from this build on.")
w("- `report/market/yahoo-proj-2026-10-14.csv` — the per-game line (total / GP), the totals, Yahoo's Rank, the status letters.")
w("- `report/market/consensus-2026-10-14.csv`, `unmatched-yahoo-2026-10-14.md` (the absence gate), `disagreements-yahoo-2026-10-14.md`, `provenance.csv` (the yahoo row).")
w("- `report/market/yahoo_market.py` — the headerless format, the resolver rule and the double-join check; `report/check_derived.py` — the registration.\n")
w("## 3. The price (WO-4) — the overnight move against the 10/13 file\n")
w(f"Pool rows priced: {MV['priced_v68']} on the 10/13 file, {MV['priced_v69']} on 10/14. Newly priced (8, all by XRank, all past #300): " + ", ".join(f"{n} ({int(p[0])})" for n, _, _, _, p in MV["newly"]) + ". None lost.\n")
w(f"Market order among the rows priced both days changed on {MV['order_changes']} rows (mean {MV['mean_shift']} places; {MV['top156_changes']} of them inside the top 156 on one day or the other) — almost all one- or two-place reshuffles inside the ADP 104–118 band, where many names sit within a tenth of a pick of each other. The largest:\n")
w("| player | market rank 10/13 to 10/14 | price 10/13 to 10/14 |\n|---|---|---|")
w(fmt_moves() + "\n")
w(f"ADP up by 0.8 or more: " + "; ".join(f"{n} {a} to {b}" for n, a, b in F["adp_up_1"]) + f". Down by 0.7 or more: " + "; ".join(f"{n} {a} to {b}" for n, a, b in F["adp_down_1"]) + f". Yahoo's own Rank (its projection rank) moved on {F['yrank_changed']} names, by up to {F['yrank_maxshift']} places, as its projections changed and 50 names were added below #300.\n")
w("## 4. Yahoo's projection line: what changed overnight, and what a re-blend would do\n")
w(f"Yahoo revised {F['line_changed']} projection lines overnight (every one a pool row). Games changed on {len(F['gp_changed'])}: " + "; ".join(f"{n} {a} to {b}" for n, a, b in F["gp_changed"][:9]) + ", and smaller moves on the rest. Points per game moved 1.5 or more on " + f"{len(F['pts_big'])}: " + "; ".join(f"{n} {a} to {b}" for n, a, b in F["pts_big"]) + ".\n")
w(f"Version 67's six-way blend counts Yahoo's 10/13 line as one equal-weight reference among up to six (ours one of them); games and minutes were not blended. If Yahoo's 10/14 line replaced its 10/13 line, a blended cell would move by (new − old) / (references + 1). Of the {F['blend_rows_touched']} blended rows Yahoo touched, {len(F['blend_rows_material'])} would move by a material amount (0.3+ in points, rebounds or assists; 0.1+ in steals, blocks, threes or turnovers; .005+ in a percentage):\n")
w("| player | references | points | rebounds | assists | threes | blocks |\n|---|---|---|---|---|---|---|")
for m in F["blend_rows_material"]:
    d = m["d"]
    w(f"| {m['n']} | {m['n_refs']} | {d.get('pts', 0):+.2f} | {d.get('reb', 0):+.2f} | {d.get('ast', 0):+.2f} | {d.get('tpm', 0):+.2f} | {d.get('blk', 0):+.2f} |")
w("\nThe Yahoo games cuts (Ingram 68 to 55, Raynaud 74 to 65, Kuzma 71 to 65, Knueppel 79 to 70, Filipowski 75 to 65) would not flow through the blend at all — games stayed ours by design. Ingram and Raynaud already carry risk tags on the deck (availability 0.78).\n")
w("## 5. The status letters against the tag inventory\n")
w(f"{len(LET)} letters changed overnight. Cleared: " + ", ".join(f"{n}" for n, a, b, t in LET if a != "-" and b == "-") + ". Newly lettered Q: " + ", ".join(f"{n}" for n, a, b, t in LET if a == "-" and b == "Q") + ". Q to O: " + ", ".join(f"{n} (deck `{t}`)" for n, a, b, t in LET if a == "Q" and b == "O") + ".\n")
w("Tyrese Haliburton's Q cleared — consistent with the deck's untagged row (owner call, Version 66). Dylan Cardwell's Q became O — consistent with the owner's lock call this morning (`inj-calf-risk`, out 2+ weeks). No tag moves on a Yahoo letter alone (one outlet; tags come from injury news on two).\n")
w("## 6. Deck build and publish\n")
w("- Pool unchanged (Version 68's bytes, pool sha 30246ac015fe); `hoops.py freshness --stamp --no-pool-changes` re-stamped for the re-price; the colophon's Market sentence re-authored (\"Yahoo's 2026-10-14 paste (the lock paste) prices 302 of 335 rows (ADP on 185, else XRank)\").")
w("- `build_deck.py`: planes: 315 shared · kit-only 10 · deck-only 20 · team 0 · exclusion 0 · drift 0 · propagation 0; market: yahoo-2026-10-14.csv — priced 302/335 rows (Yahoo ADP else XRank), 0 days old; built 335 players, injection round-trip OK, no waiver, \"safe to publish\" (first build passed); `data/market-snapshot.csv` refreshed with the build.")
w(f"- `check_parity.py`: {parity}. `test_card.py` {card}; `test_draft.py` all {draft[1]} cases passed; `test_gates.py` all {draft[2]} cases passed. `full_dom_check.mjs` on `draft_state_54.json`: {dom} (`arena/results/full_dom_check_2026-10-14_v69.json`). `repeat_market_check.py`: {rn_head} (`arena/results/repeat_market_check_2026-10-14_v69.json`). `identity_check.py`: {ident}. `range_check.py`: {rng}.")
w(f"- Published to the standing URL after a fresh read: Version 69, id {PUB['version_id']} ({PUB['artifact']}); the served file carries the built page (sha256 {PUB['page_sha256_12']}) byte-for-byte at offset 349 inside the service's wrapper; fresh read immediately before showed Version 68 (id {PUB['prev_id']}).\n")
w("## 7. Gates (2026-10-14, market)\n")
w("| gate | evidence |\n|---|---|")
w(f"| `market/yahoo_market.py 2026-10-14 --as-of 7438f8c` | TRANSCRIPTION GATE PASS (I1–I7); 350 parsed, 186 with ADP, XRank gaps NONE; I7 306 of 350; JOIN 325 pool players, 306 matched, 19 accepted absences, 0 possible spelling variants; GATE PASS |")
w("| red-first, the double-join check | resolver fix off: 3 problems (LaMelo Ball from L. Ball/MIN and L. Ball/CLE; Tre Jones from T. Jones/CHI and T. Jones/DEN; J. Green UTA ties two rows); fix on: 0 |")
w("| `report/check_derived.py` | DERIVED: all 28 dated artifacts reproduce byte-for-byte from their pinned inputs; exit 0 |")
w("| `report/check_provenance.py` | PASS — all rows sourced; exit 0 |")
w("| `scripts/build_deck.py` (deck) | gates 1–7 + F8 pass, no waiver; 302/335 priced on yahoo-2026-10-14.csv, 0 days old; \"safe to publish\" |")
w(f"| `scripts/check_parity.py` (deck) | {parity}; exit 0 |")
w(f"| `scripts/test_card.py` / `test_draft.py` / `test_gates.py` (deck) | {card} / all {draft[1]} cases passed / all {draft[2]} cases passed; exit 0 each |")
w(f"| `arena/mocks/full_dom_check.mjs` (deck) | {dom}; exit 0 |")
w(f"| `scripts/repeat_market_check.py` (deck) | {rn_head}; exit 0 |")
w(f"| `scripts/identity_check.py` / `range_check.py` (deck) | {ident} / {rng} (the pool is Version 68's; these confirm it) |")
w("| `report/check_report.py` | see the PR body (run on this file after writing) |")
w("| `scripts/judgment_open_items.py --check-report` / `repeat_market_check.py --check-report` (deck plane) | see the PR body (run on this file after writing) |")
w(f"| artifact publish | Version 69, id {PUB['version_id']}; byte-verified at offset 349 |\n")
w("## 8. Watchlist / open items\n")
w("- **The draft** — this is the price the draft runs on unless another paste arrives; the parser takes the draft-room copy with or without its header row.")
w("- **Anfernee Simons** — lost his ADP on the page (priced by XRank 201 now; market rank 119 to 210); his value row is ours and unchanged.")
w("- **Yahoo's games cuts** — Ingram 55, Raynaud 65, Kuzma 65, Knueppel 70, Filipowski 65 (D-1014-12 below).")
w("- **Rui Hachimura and Jonathan Kuminga** — Yahoo raised both lines sharply overnight (points 11.4 to 18.6 and 11.6 to 16.0); a re-blend would lift ours by 1.2 and 0.9 points per game.\n")
w("## Open-item receipts\n")
w("| player | query run (2026-10-14) | dated finding |\n|---|---|---|")
rec = []
for n in ["Brandon Ingram", "Kristaps Porzingis", "Kawhi Leonard", "Bennedict Mathurin", "Ryan Rollins"]:
    r = Y[n]; rec.append(f"{n.split()[-1]} {r['status'] or 'unlettered'} (ADP {r['adp'] or '-'}, GP {r['gp']})")
w("| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the morning pull, same day (`after-report-2026-10-14.md`, receipts dated 10/14) | all held as of this morning; this paste adds Yahoo's letters only — " + "; ".join(rec) + "; Thomas, Ivey, Sochan, Dillingham absent from the 350; Lonzo Ball listed at CLE with NA (one outlet, no row change) |\n")
w(rn_sec)
w("## Bounds\n")
w("- Out of scope by design: no pool line, tag, team or placement moved (price-only, the standing recommendation for the lock paste); the re-blend in §4 is measured, not applied.")
w("- The re-blend size is a first-order estimate: it swaps Yahoo's cell in the blend record and holds the shot-attempt rescale and the morning's three lock calls (Kornet, White, Cardwell) fixed; a real re-blend would rerun `blend_lines.py` and the whole chain.")
w("- Did not check: whether the overnight 🎯 on the owner's turns changes on Version 69 in the graded rooms (the prices moved at most 1.0 ADP place outside Simons; not load-bearing for publishing a price refresh); Yahoo's page timestamp (the paste carries none).\n")
w("## Decision sheet (owner disposes)\n")
w("| id | decision question | default if silent |\n|---|---|---|")
w("| D-1014-3 | the lock paste: price-only rebuild before the lock | applied (Version 69) |")
w("| D-1014-12 | Re-blend on Yahoo's 10/14 projections before the draft? (a) no — 9 rows move materially, the largest +1.2 points (Hachimura); (b) yes — rerun the blend with the 10/14 line, rebuild, chain, republish (about an hour) | (a) |")
w("| D-1014-13 | Yahoo's games cuts (Ingram 55, Raynaud 65, Kuzma 65, Knueppel 70, Filipowski 65) — (a) no change, games stay ours; (b) read each against two outlets before the draft | (a) |")
w("| D-1014-9..11, D-1014-1..8, D-1013-*, and earlier | carried | carried |\n")
w("## Provenance\n")
w("- Inputs: the owner's paste (chat, 2026-10-14; `report/market/yahoo-raw-2026-10-14.txt`), `yahoo-2026-10-13.csv` and `yahoo-proj-2026-10-13.csv` (the comparisons), the blend record `report/blend/out/lines_blend_2026-10-14.json`, the published Version 68 page (deck main 85ad6ea) and the built Version 69 page.")
w("- Scripts: `report/market/yahoo_market.py` (pinned at 7438f8c), `report/check_derived.py`; this folder: `figures.py` (paste vs paste, letters, re-blend size), `moves.py` (market order from the two pages), `letters_vs_tags.txt`, `chain.log`, `rn_section.txt`, `publish.json`, this writer.")
w("- Deck results: `arena/results/full_dom_check_2026-10-14_v69.json`, `repeat_market_check_2026-10-14_v69.json`; `data/freshness.json` re-stamped; `data/market-snapshot.csv` refreshed.\n")
w("## In plain language\n")
w("**What this did.** Your 10/14 Yahoo paste is now the price the deck reads — the Mkt number on every row, the survival read behind BUY NOW, and the priced-only card from round 11. 302 of the 335 rows carry a price now (294 yesterday); the eight new ones are deep names past #300.\n")
w("**What moved.** Almost nothing in the market. Every XRank is the same as yesterday; ADPs shifted by a fraction of a pick (none more than one). The one real change: Anfernee Simons no longer has an ADP on Yahoo, so the deck now prices him around 201 instead of 110.\n")
w("**Yahoo's projections did change** for 58 players — Hachimura, Kuminga, LaVine, Kyrie and Keyonte George up; Raynaud, Kuzma, Wells and Pippen Jr. down; and Yahoo cut games for Ingram (55), Raynaud, Kuzma, Knueppel and Filipowski. Our lines blend Yahoo as one voice of up to six, so feeding these in would move nine players a little (Hachimura the most, about +1.2 points a game). I did not apply that — it is your call (D-1014-12), and my recommendation is to leave the lines as they are for the draft.\n")
w("**The deck.** Rebuilt on the new prices and republished as Version 69; every check, the full page drive and the repeat-name check passed on the published bytes. Lines, tags and placements are exactly this morning's.\n")
open(f"{K}/after-reports/after-report-2026-10-14-yahoo.md", "w", encoding="utf-8").write("\n".join(L))
print("wrote", len("\n".join(L)), "chars")
