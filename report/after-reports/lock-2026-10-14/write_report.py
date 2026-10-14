#!/usr/bin/env python3
"""Writes after-report-2026-10-14-lock.md from the records: the Yahoo 10/14 intake figures (../yahoo-2026-10-14/), the
Hashtag 10/14 intake, the two blend records (report/blend/out/), the board diff and the chain/publish records in this folder."""
import csv, json, os, re, statistics as st
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.dirname(H); K = os.path.dirname(A)
Y = json.load(open(f"{A}/yahoo-2026-10-14/figures_2026-10-14.json", encoding="utf-8"))
B67 = {r["key"]: r for r in json.load(open(f"{K}/blend/out/lines_blend_2026-10-14.json", encoding="utf-8"))["rows"]}
BL = json.load(open(f"{K}/blend/out/lines_blend_lock_2026-10-14.json", encoding="utf-8"))
BLK = {r["key"]: r for r in BL["rows"]}
APP = json.load(open(f"{K}/blend/out/apply_record_lock_2026-10-14.json", encoding="utf-8"))
BD = json.load(open(f"{H}/board_diff_lock_2026-10-14.json", encoding="utf-8"))
CH = open(f"{H}/chain.log", encoding="utf-8").read()
RN = open(f"{H}/rn_section.txt", encoding="utf-8").read()
PUB = json.load(open(f"{H}/publish.json", encoding="utf-8"))
LET = [l.split("|") for l in open(f"{A}/yahoo-2026-10-14/letters_vs_tags.txt", encoding="utf-8").read().splitlines() if l]
HT = {r["player"]: r for r in csv.DictReader(open(f"{K}/market/hashtag-2026-10-14.csv", encoding="utf-8"))}
HO = {r["player"]: r for r in csv.DictReader(open(f"{K}/market/hashtag-2026-10-12.csv", encoding="utf-8"))}
YP = {r["player"]: r for r in csv.DictReader(open(f"{K}/market/yahoo-proj-2026-10-14.csv", encoding="utf-8"))}
MV = json.load(open(f"{A}/yahoo-2026-10-14/moves_v68_v69.json", encoding="utf-8"))

def grab(pat):
    m = re.search(pat, CH); assert m, pat; return m.group(0).strip()
parity = grab(r"PARITY: [^\n]+"); card = grab(r"CARD: all \d+ cases passed"); allp = re.findall(r"all (\d+) cases passed", CH)
dom = grab(r"\d+ assertions, 0 failed[^\n]*"); ident = grab(r"POINTS IDENTITY[^\n]*"); rng = grab(r"RANGE CHECK[^\n]*")
assert not re.search(r"^exit [1-9]", CH, re.M), "a chain step failed"
rn_head = RN.splitlines()[0]; rn_sec = RN[RN.index("## Repeat-name market check"):].rstrip() + "\n"

# lines that move against Version 67's blend (the deck/kit lines this morning), Kornet excluded (held)
moves = []
for k, r in BLK.items():
    if r["name"] == "Luke Kornet": continue
    old = B67[k]["new"] if k in B67 else r["old"]
    d = {c: round(r["new"][c] - old[c], 3) for c in r["new"] if abs(r["new"][c] - old[c]) > 1e-9}
    if d: moves.append((r["name"], d, k not in B67))
moves.sort(key=lambda x: -abs(x[1].get("pts", 0)))
ht_changed = [n for n in HT if n in HO and any(HT[n][c] != HO[n][c] for c in ("gp", "mpg", "fg_pct", "ft_pct", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"))]
bm = BD["moves"]

L = []; w = L.append
w("# After-report — 2026-10-14 (the lock): Yahoo and Hashtag 10/14 re-blended into the lines, Kawhi and Davis back to 0.78, deck Version 70\n")
w('**Owner input (2026-10-14, verbatim):** "Yahoo ADP and Projections 10/14:" — Yahoo\'s player list from the draft room, 350 rows; then, with the Hashtag projections page printed to PDF (`Hashtag_Projections_10.14.pdf`): "Take the Yahoo and Hashtag projections dated today, and synergize with kit\'s as you see fit and meaningful. Provide to me the final 180 kit rankings and lock"; and, during the work: "I\'m sorry, but for Kawhi and Anthony Davis, revert their health multiplier to 0.78".\n')
w("Pull window: 2026-10-14 → 2026-10-14 (owner inputs, WO-4 and the lock; not a roster pull — the morning pull report `after-report-2026-10-14.md` stands).")
w("Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07`, exit 0.\n")
w("**Method (stated to the owner before any line moved).** A1: the six-way blend you approved this morning, taken again *from our own pre-blend lines* (re-blending already-blended lines would count our line twice), with Yahoo 10/14 and Hashtag 10/14 in place of Yahoo 10/13 and Hashtag 10/12; RotoBaller, FantasyPros and the Basketball Monster cards (all 10/13) unchanged; each of the nine categories the equal-weight mean, shot attempts rescaled so points add up. A2: games, minutes, tags and teams stay ours — Yahoo's games cuts are listed, not applied. A3: Luke Kornet keeps the line your lock call restored. Then your mid-work call: Kawhi Leonard and Anthony Davis back from the lighter tier to `inj-risk` (×0.78).\n")
w(f"**Headline.** The lock moved little, and only where today's outlets moved. Hashtag's page changed on {len(ht_changed)} rows since 10/12; Yahoo revised {Y['line_changed']} projection lines overnight. Re-blended, {len(moves)} lines move on both planes (Rui Hachimura +1.3 points, De'Andre Hunter −1.0, Jonathan Kuminga +0.9 the largest), and Obi Toppin is newly blended now that three outlets project him. The kit's final top 180 holds the same 180 players as this morning; {BD['moved_in_180']} change place, by {st.mean(abs(a - b) for _, a, b in bm):.2f} places on average and 10+ for {sum(1 for _, a, b in bm if abs(a - b) >= 10)}. Kawhi and Davis are back at ×0.78 on the draft page. The deck is Version 70, priced on Yahoo's lock paste (302 of 335 rows), every gate green, published and byte-verified.\n")
w("## 1. Roster changes\n")
w("None. Single-source flags only (F2; Yahoo is one outlet): Yahoo lists Lonzo Ball at CLE with the NA letter (the pool holds him unsigned) and Tyus Jones at DEN (not a pool row). No pool row changed team, entered or left.\n")
w("## 2. What landed\n")
w("- Kit, market: `yahoo-raw-2026-10-14.txt` (the paste, verbatim) and its outputs (`yahoo-2026-10-14.csv` the price file, `yahoo-proj-2026-10-14.csv`, consensus, unmatched, disagreements); `hashtag-raw-2026-10-14.txt` (the PDF's page text, pdfplumber, 10 pages, 238 lines) and `hashtag-2026-10-14.csv`, `unmatched-hashtag-2026-10-14.md`; both registered (derived 29 of 29).")
w("- Kit, parser: `yahoo_market.py` reads the headerless draft-room copy, and its name resolver no longer joins a second Yahoo row on another team to a pool row a same-team Yahoo row already holds (the paste's third \"J. Green\", Lonzo Ball as \"L. Ball\" and Tyus Jones as \"T. Jones\"); a new check fails the run if two Yahoo rows land on one player (red-first: 3 problems with the rule off, 0 with it on).")
w("- Kit, lines: `report/projections-2026-27.csv` (54 lines), `report/top-200-2026-27.md` (regenerated); `blend/tools/common.py` (`BLEND_SET=lock` selects the 10/14 files; unset, Version 67's sources stand), `blend/out/lines_blend_lock_2026-10-14.json`, `lines_blend_lock_apply_2026-10-14.json` (Kornet held), `apply_record_lock_2026-10-14.json`.")
w("- This folder: `preblend.py` (the starting point), `revert_mild.py` (Kawhi, Davis), `board_diff.py`, `final_180.py` and **`final-180-kit-2026-10-14.md`**, `blend_lock.log`, `chain.log`, `rn_section.txt`, `publish.json`, this writer.")
w("- Deck: `data/players.csv` (54 lines, two tags, 238 notes), `data/freshness.json`, `data/market-snapshot.csv`, `docs/draft-deck.html` (Version 70).\n")
w("## 3. Today's two outlets\n")
w(f"**Yahoo (the lock paste).** {Y['rows']} rows, {Y['adp']} with ADP; Q on {Y['letters'].get('Q', 0)}, O on {Y['letters'].get('O', 0)}, NA on {Y['letters'].get('NA', 0)}. Against the 10/13 paste: XRank identical on all {Y['shared']} shared names; ADP moved on {Y['adp_changed_both']} by at most {Y['adp_maxshift']} (mean {Y['adp_mean_shift']}); Anfernee Simons lost his ADP (110.4; now priced by XRank 201, market rank 119 to 210). Projections revised on {Y['line_changed']} names — games on {len(Y['gp_changed'])} (" + "; ".join(f"{n} {a} to {b}" for n, a, b in Y["gp_changed"][:6]) + ", …), points per game by 1.5+ on " + ", ".join(f"{n} {a} to {b}" for n, a, b in Y["pts_big"]) + ".\n")
w(f"**Hashtag.** The 10/14 page (Updated: 14 October 2026) carries the same 200 names as 10/12; {len(ht_changed)} rows differ: " + "; ".join(f"{n} (points {HO[n]['pts']} to {HT[n]['pts']}, GP {HO[n]['gp']} to {HT[n]['gp']})" for n in ht_changed) + ".\n")
w("## 4. The lock re-blend\n")
w(f"- **Starting point** (`preblend.py`): on all 241 rows of this morning's blend, today's kit and deck lines equal the blend's output (Kornet equals his restored pre-blend line) — nothing else touched a blended line since; each returned to its pre-blend line. PREBLEND: PASS.")
w("- **Control**: the unchanged sources on that starting point reproduce this morning's blend on 241 of 241 rows, value for value — the tool and the starting point are the ones Version 67 used.")
w(f"- **Lock run** (`BLEND_SET=lock`): {len(BL['rows'])} rows reach three or more outside lines (Toppin newly: Yahoo, Hashtag, FantasyPros); Kornet held; {len(BL['wide_factor'])} rows with a shot factor outside 0.85–1.15, listed not held (the morning's rule); 0 problems. `blend_apply.py` PASS on A1–A9 (both planes in one pass; every category recomputed from the pinned files) — deck {APP['deck_rows_changed']} rows, kit {APP['kit_rows_changed']} rows rewritten against the pre-blend start; a second run changes nothing.")
w(f"- **Against this morning's lines**: {len(moves)} rows move on each plane (the same rows on both, suffix spellings aside). The largest:\n")
w("| player | points | rebounds | assists | threes | steals | FG% | FT% |\n|---|---|---|---|---|---|---|---|")
for n, d, new in moves[:14]:
    f = lambda c, p=1: (f"{d[c]:+.{p}f}" if c in d else "")
    w(f"| {n}{' (newly blended)' if new else ''} | {f('pts')} | {f('reb')} | {f('ast')} | {f('tpm')} | {f('stl')} | {f('fg_pct', 3)} | {f('ft_pct', 3)} |")
w("\nGames stayed ours (A2). Yahoo's games cuts — Ingram 55, Raynaud 65, Kuzma 65, Knueppel 70, Filipowski 65 — and Hashtag's (Kawhi 58 to 50, Porziņģis 42 to 30) are not applied; Ingram and Raynaud already carry risk tags, Porziņģis is on the DO NOT DRAFT list.\n")
w("## 5. Kawhi Leonard and Anthony Davis back to ×0.78\n")
w("Version 66 moved both from `inj-risk` to `inj-risk-mild` (×0.85) as a deck tag only — the kit's games were not touched (kit GP 60 and 55 throughout). `revert_mild.py` puts the leading tag back to `inj-risk` with the dated reason inside it; asserted: exactly those two rows change, only their notes, `hoops.availability` = 0.78 for both; a second run changes nothing. Kyrie Irving and Damian Lillard stay on the lighter tier. The kit board is not affected (the kit models health through games).\n")
w("## 6. The kit board — the final 180\n")
w(f"`rank_engine.py` on the lock lines: 200 players from 313 projected; provenance PASS; `test_rank_engine.py` OK. The top 180 holds the same 180 players as this morning's board (none in, none out). {BD['moved_in_180']} change place; mean move {st.mean(abs(a - b) for _, a, b in bm):.2f} places; 10+ for {sum(1 for _, a, b in bm if abs(a - b) >= 10)}:\n")
w("| player | this morning | the lock |\n|---|---|---|")
for n, a, b in bm[:12]:
    w(f"| {n} | {a} | {b} |")
w("\nThe full table is `lock-2026-10-14/final-180-kit-2026-10-14.md` (rank, team, positions, games, line, percentages, value, move).\n")
w("## 7. Deck build and publish\n")
w("- `hoops.py freshness --stamp --pool-changes` (the lock); colophon: a lock paragraph at the head of the Data section, the Kawhi/Davis sentence of 10/13 marked as reverted, the Market sentence on the 10/14 paste.")
w("- `build_deck.py`: planes: 315 shared · kit-only 10 · deck-only 20 · team 0 · exclusion 0 · drift 0 · propagation 0; market: yahoo-2026-10-14.csv — priced 302/335 rows, 0 days old; built 335 players, pool d1d74587c5db, injection round-trip OK, no waiver, \"safe to publish\" (first build passed).")
w(f"- Chain on the built page (sha256 {PUB['page_sha256_12']}): `check_parity.py` {parity}; `test_card.py` {card}; `test_draft.py` all {allp[1]}; `test_gates.py` all {allp[2]}; `full_dom_check.mjs` {dom}; `repeat_market_check.py` {rn_head}; `identity_check.py` {ident}; `range_check.py` {rng}.")
w(f"- Published to the standing URL ({PUB['artifact']}) after a fresh read of Version 68 (id {PUB['prev_id']}): Version 70, id {PUB['version_id']}; the served file carries the built page byte-for-byte at offset 349. (Version 69 — this afternoon's price-only build — was superseded before publishing; its chain was stopped.)\n")
w("## 8. Gates (2026-10-14, the lock)\n")
w("| gate | evidence |\n|---|---|")
w("| `market/yahoo_market.py 2026-10-14 --as-of 7438f8c` | TRANSCRIPTION GATE PASS (I1–I7); 350 parsed, 186 with ADP; I7 306 of 350; JOIN 306 matched, 19 accepted absences; GATE PASS |")
w("| `market/hashtag_pdf_market.py 2026-10-14 --as-of 03a8704` | 200 rows, TRANSCRIPTION GATE PASS; 1 Hashtag-only name, none a spelling variant; GATE PASS |")
w("| `report/check_derived.py` | DERIVED: all 29 dated artifacts reproduce byte-for-byte from their pinned inputs |")
w("| `preblend.py` / control / `blend_lines.py` (lock) / `blend_apply.py` ×2 | PASS / 241 of 241 identical / 0 problems / PASS, second run no change |")
w("| `revert_mild.py` ×2 | 2 rows, both at 0.78 / 0 rows |")
w("| `rank_engine.py`, `check_provenance.py`, `test_rank_engine.py` | 200 from 313; PASS; OK |")
w(f"| `build_deck.py` (deck) | gates 1–7 + F8 pass, no waiver, 302/335 priced |")
w(f"| `check_parity.py` / `test_card.py` / `test_draft.py` / `test_gates.py` (deck) | {parity} / {card} / all {allp[1]} / all {allp[2]}; exit 0 each |")
w(f"| `full_dom_check.mjs` (deck) | {dom} |")
w(f"| `repeat_market_check.py` (deck) | {rn_head} |")
w(f"| `identity_check.py` / `range_check.py` (deck) | {ident} / {rng} |")
w("| `report/check_report.py`, deck `--check-report` gates | run on this file after writing (PR body) |")
w(f"| artifact publish | Version 70, id {PUB['version_id']}, byte-verified at offset 349 |\n")
w("## Watchlist\n")
w("- Yahoo's and Hashtag's games cuts (§4) — not applied; the draft page's tags carry health.")
w("- Anfernee Simons lost his Yahoo ADP (market rank 210 now).")
w("- Lonzo Ball listed by Yahoo at CLE with NA (one outlet; the pool holds him unsigned).\n")
w("## Open-item receipts\n")
w("| player | query run (2026-10-14) | dated finding |\n|---|---|---|")
rec = []
for n in ["Brandon Ingram", "Kristaps Porzingis", "Kawhi Leonard", "Bennedict Mathurin", "Ryan Rollins"]:
    r = YP[n]; rec.append(f"{n.split()[-1]} {r['status'] or 'unlettered'} (Yahoo ADP {r['adp'] or '-'}, GP {r['gp']})")
w("| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the morning pull, same day (`after-report-2026-10-14.md`, receipts dated 10/14) | all held as of this morning; today's pastes add letters and games only — " + "; ".join(rec) + "; Hashtag 10/14 has Kawhi at 50 games and Porziņģis at 30; Thomas, Ivey, Sochan, Dillingham absent from Yahoo's 350; Lonzo Ball listed at CLE with NA (one outlet, no row change) |\n")
w(rn_sec)
w("## Bounds\n")
w("- Out of scope by design: games and minutes (A2) — the outlets' games are listed, not blended; teams and placements; the deck's other injury tags.")
w("- The blend's five outside lines: only Yahoo's and Hashtag's are today's; RotoBaller, FantasyPros and the cards are 10/13 (no newer files were supplied).")
w("- The Haliburton plan research (separate report) was run on Version 68's lines; the lock moves its names by 1–5 places on the kit board (Towns 13 to 14, Derrick White 25 to 26, Wagner 35 to 38, Anunoby 34 to 31, Jerome 43 to 47) — its turn lists stand as scouting, not re-run.")
w("- Did not check: the card's 🎯 at your turns in past rooms on Version 70 (a re-grade); not load-bearing for publishing the lock.\n")
w("## Decision sheet (owner disposes)\n")
w("| id | decision question | default if silent |\n|---|---|---|")
w("| D-1014-3 | the lock paste | applied — Version 70 is priced on it |")
w("| D-1014-12 | re-blend on today's Yahoo and Hashtag | applied at your call (\"synergize … and lock\") |")
w("| D-1014-13 | the outlets' games cuts (Ingram 55, Raynaud 65, Kuzma 65, Knueppel 70, Filipowski 65; Kawhi 50 on Hashtag) — (a) games stay ours; (b) apply | (a) |")
w("| D-1014-15 | Kawhi Leonard and Anthony Davis back to ×0.78 | applied at your call |")
w("| D-1014-1..11, D-1013-*, earlier | carried | carried |\n")
w("## Provenance\n")
w("- Inputs: the owner's Yahoo paste and Hashtag PDF (chat, 2026-10-14), the pinned 10/13 RotoBaller, FantasyPros and cards files, this morning's blend record `blend/out/lines_blend_2026-10-14.json`, the kit at 7bf829d and the deck at main 85ad6ea (Version 68).")
w("- Commits: kit 8380ff7, 023372a, 7438f8c (Yahoo raw and parser), 03a8704 (Hashtag raw), the lock commit; deck af91b23 (Version 70) and the merge of main 462fa1b.")
w("- Re-verify: `BLEND_SET=lock python3 report/blend/tools/blend_lines.py --deck <pre>/players.csv --kit <pre>/projections-2026-27.csv --out x.json` after `preblend.py`; `python3 report/check_derived.py`; read the standing URL and compare at offset 349.\n")
w("## In plain language\n")
w(f"**What I did.** I took Yahoo's and Hashtag's projections from today and folded them into our lines exactly the way you approved this morning — every category is the average of our line and the five outside lines, with today's Yahoo and Hashtag replacing yesterday's. I started from our own lines, not this morning's already-averaged ones, so nothing got counted twice; and I checked that running the old sources through the same steps gives back this morning's lines exactly.\n")
w(f"**What moved.** Not much, because Yahoo and Hashtag barely moved: {len(moves)} players' lines changed, mostly by a few tenths. Hachimura (+1.3 points), Kuminga (+0.9), LaVine, Santos and Kyrie went up; Hunter (−1.0), Pippen Jr. and Wells went down. Games, minutes and injury tags stayed ours; Kornet kept his restored line.\n")
w("**Kawhi and Davis** are back at the full 0.78 injury discount on the draft page, as you asked. Kyrie and Lillard stay at 0.85.\n")
w(f"**Your final 180.** Same 180 players as this morning; {BD['moved_in_180']} shifted a few places, seven by ten or more (Hachimura 168 to 145 the biggest). The full list is in `final-180-kit-2026-10-14.md`.\n")
w("**Locked.** The draft page is Version 70, priced on your 10/14 Yahoo paste, every check passed on the exact bytes that are published.\n")
open(f"{A}/after-report-2026-10-14-lock.md", "w", encoding="utf-8").write("\n".join(L))
print("wrote after-report-2026-10-14-lock.md")
