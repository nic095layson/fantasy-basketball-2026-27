# After-report — 2026-10-01 owner inputs (WO-4): the fresh Yahoo list, the draft room's positions, two Hashtag pages, last year's draft

**Owner inputs (2026-10-01, in order):** Yahoo's draft-analysis list pasted
into chat (300 names, 188 with ADP; "the fresh Yahoo ADP paste" asked for
this morning); last year's league draft pasted ("LAST YEARS DRAFT RESULTS",
13 rounds with the team-name to manager map); two PDFs printed from Hashtag
Basketball — its projections page ("Does this help you, Claude?") and its
ADP page ("Joseph Mamone pulls this data directly from Yahoo"). This report
lands the first, second and fourth under the work order's WO-4 rule (the
owner's inputs, the day they land); the projections page is the next
report, because it is a projection question (D-WO1-1), not a market one.

**Method.** The paste transcribed verbatim and run through
`report/market/yahoo_market.py` (transcription invariants, the hard unmatched
gate, consensus and disagreements, provenance; outputs pinned to the inputs
commit so `check_derived.py` reproduces them). Positions set on both planes
by a script with exact-match assertions and a before/after record. The PDFs
read with pdfplumber page by page (no eyeballing); the ADP page parsed into
per-platform columns and cross-checked against the paste. The deck rebuilt
through its seven gates with the new price file (F8), then parity, the
three suites and the 128-assertion browser drive; published to the standing
artifact URL. Verification: this file passes `report/check_report.py`;
receipts below.

Pull window: 2026-10-01 → 2026-10-01 (owner inputs; not a roster pull — the
10/01 daily-pull row covers the window).

**Headline.** The market column is current again (Yahoo ADP as of
2026-10-01 on 186 deck rows, XRank on 111 more; the 9/22 paste retired), and
the pool's positions now match what the draft room shows: 51 kit rows and
54 deck rows changed, every one of them because the pool had been set from
Yahoo's 9-cat *rankings* page (9/28), which lists wider eligibility than
Yahoo's *draft-analysis* page, the one the draft room displays (mocks 57, 58
and 59 had shown the gap on 28 to 29 men each). Hashtag's ADP page, which
carries Yahoo's ADP alongside ESPN's and Fantrax's, agrees with the paste on
every position and on every ADP to within two picks (a day's drift). Last
year's draft re-paste matches the room model ingested on 8/04 pick for pick.
Yahoo moved little in nine days (the biggest ADP moves under five picks);
what moved most was its expert XRank — Porziņģis down 55, Kuminga from the
placeholder tier to 129 — and the room now prices thirteen more men (Poole,
Tre Jones with ADPs; Beal, Clarkson and eleven others with an XRank) while
twelve fell off the top 300. Four Yahoo team placements disagree with the
deck's free-agent rows (Westbrook SAC, Konchar NYK, Valančiūnas DEN, Batum
LAC) and two priced men have no deck row (Drummond, Morez Johnson): flags
for the next pull, not edits (F2).

## 1. What landed

| plane | file | what |
|---|---|---|
| kit | `report/market/yahoo-raw-2026-10-01.txt` | the paste, verbatim (2,774 lines; 300 blocks, duplicate name lines as the transcription check) |
| kit | `report/market/yahoo-2026-10-01.csv` | 300 rows (player, team, pos, xrank, adp); transcription gate I1–I5 PASS, XRank gaps none |
| kit | `report/market/consensus-2026-10-01.csv`, `unmatched-yahoo-2026-10-01.md`, `disagreements-yahoo-2026-10-01.md` | join 296 of 324 pool rows; 28 accepted absences (14 outside Yahoo's top 300 by the mechanical check, 4 unsigned free agents, Sochan and Whitmore on standing watch items, the rest camp bodies); 4 Yahoo-only names; pinned to commit `020771c` |
| kit | `report/market/positions_sync_2026-10-01.json` | every position change on both planes, before and after |
| kit | `report/projections-2026-27.csv` | `pos` on 51 rows; no line changed |
| kit | `report/top-200-2026-27.md`, `report/seat-10-slate.md` | regenerated (positions; the slate's ADP column from the 10/01 consensus) |
| kit | `report/market/hashtag-adp-raw-2026-09-30.txt`, `hashtag-raw-2026-09-30.txt` | the two PDFs' text, page by page (PDF md5 `bb77a74f…`, `e6737ed1…`); parsed by `hashtag_pdf_market.py` into `hashtag-2026-09-30.csv` (200 rows) and `hashtag-adp-2026-09-30.csv` (418) with `unmatched-hashtag-2026-09-30.md`, pinned and registered under `check_derived.py` |
| deck | `data/players.csv` | `pos` on 54 rows; no line changed |
| deck | `docs/draft-deck.html` (v38) | Mkt from `yahoo-2026-10-01.csv` — 297 of 334 rows priced (186 ADP, 111 XRank); colophon re-worded; pool sha `ebb38ca7be4f` |
| deck | `arena/data/league_draft_2025-26_raw_2026-10-01.txt`, `arena/results/league_intel_2025-26.md` §5 | last year's draft re-paste as the audit copy, with the 156-of-156 check |

## 2. Positions: two Yahoo pages, and the room shows the narrower one

[EVIDENCE: `positions_sync_2026-10-01.json`; `yahoo-2026-09-22.csv` and
`yahoo-2026-10-01.csv` (draft-analysis page) against
`yahoo-9cat-rankings-2026-09-28.csv` (rankings page); the mock-57, 58 and 59
reports' §7; the Hashtag ADP page's Yahoo position column]

| | rankings page (9/28) | draft-analysis page (9/22, 10/01) |
|---|---|---|
| Jalen Williams | PF,SF,SG | SF,PF |
| Anthony Edwards | PG,SF,SG | PG,SG |
| Scottie Barnes | C,PF,SF,SG | SF,PF,C |
| Tyrese Maxey | PG,SG | PG |
| Mikal Bridges | PF,SF,SG | SF,PF |

The 9/29 re-derivation set both planes from the rankings page (D-M1, "Yahoo
official"). Three live rooms since then showed 28 to 29 drafted men with
fewer positions than the pool, and in every case the room's set was the
draft-analysis page's. Hashtag's ADP page, which takes its Yahoo positions
from the same feed, agrees with the 10/01 paste on all 189 names it carries a
Yahoo column for. The rule from the gap audit (D-G3: the positions the room
shows win) is applied: 51 kit rows and 54 deck rows re-set, 48 of them
narrower, 6 wider (men the 9/28 page did not carry: AJ Green, DiVincenzo,
Isaiah Joe, Keon Ellis, Moody, Westbrook, Merrill, Ziaire Williams,
Risacher — the 10/01 page lists them). The 28 kit and 37 deck rows Yahoo's
top 300 does not carry keep their positions. The deck's slot logic
(PG/SG/G/SF/PF/F/C/C), its family reads and the mock opponents' positional
need all read this column; the card's lineup eligibility now matches the
room's.

## 3. The market: nine days of Yahoo

[EVIDENCE: `disagreements-yahoo-2026-10-01.md` §F (Yahoo vs
`yahoo-2026-09-22.csv`); `data/market-snapshot.csv` v37 vs v38]

- **ADP barely moved.** 186 rows carry an ADP on both dates; the largest
  moves are Caruso later by 8.9, Simons 7.8, AJ Green 7.5, Lopez 7.3; Paul
  Reed earlier by 6.2, LaVine 4.6, Draymond 4.5, Sabonis 4.1. No top-60 man
  moved more than five picks (Anthony Davis later by 5.0, Sabonis earlier by
  4.1).
- **XRank moved more.** Fallers: Porziņģis 97 to 152, Kevin Porter Jr. 121
  to 158, Vassell 122 to 157, Vučević 144 to 177, Sheppard 117 to 149, Braun
  143 to 173, Knueppel 45 to 64, Sabonis 22 to 35, Jaylen Brown 31 to 44.
  Risers: DeRozan 251 to 102, Larsson 273 to 147, Santos 250 to 141,
  Hachimura 186 to 121, Gafford 170 to 120, Cameron Johnson 172 to 135,
  Dëmin 164 to 131, Grimes 158 to 126. Newly expert-ranked: Kuminga 129 (was
  the placeholder tier), Mara 250, Bronny James 467.
- **Who entered and left the priced set.** With ADP now and none on 9/22:
  Poole 111.8, Tre Jones 118.2. On the 10/01 list and not the 9/22 one:
  Beringer, Beal, GG Jackson, Will Riley, Shannon, Clifford, Simmons, Jović,
  Dick, Zach Collins, Flemings, Clarkson, Graves. Off the list: Broome,
  Toppin, Bradley, Isaiah Jackson, Steinbach, Moritz Wagner, Kobe Sanders,
  Hendricks, LeVert, Sion James, Conley, Ben Sheppard — the deck's internal
  model orders these twelve now.
- **The deck's Mkt column.** 297 priced (296 before); the rank changed on
  255 of 284 shared priced rows, 92 of them by ten or more places, almost
  all in the XRank-only tail where Yahoo's expert re-ordering landed: Adem
  Bona 107 to 283, Duncan Robinson 117 to 218, Burries 151 to 244, Cameron
  Johnson 137 to 188, Shaedon Sharpe 165 to 217; Poole 200 to 128, Paul
  Reed 181 to 139, Collier 281 to 202. The survival chips read this column,
  so the chips moved with it; the card's ordering did not (price-blind).
- **Our board against the room** (§B of the disagreements file, 43 values
  and 88 fades at 15+ picks): the values are the known shape — Ty Jerome
  (our 51, ADP 114), Dyson Daniels (9 vs 64), Porziņģis (48 vs 99, vetoed),
  Butler (68 vs 116), Ajay Mitchell, Hart, VanVleet, Garland, Collins,
  Washington; the deep fades are mechanical (a man we rank past 140 shows a
  fade merely by having an ADP), the real ones being Bronny James (ADP
  103.5, our 324), Mara, Morez Johnson, Drummond, Poole, AJ Green, Mikel
  Brown, Kuminga, Queta, Jaquez.

## 4. Hashtag's ADP page as the cross-check

[EVIDENCE: `hashtag-adp-raw-2026-09-30.txt` (18 pages); parsed
`hashtag-adp-2026-09-30.csv`, 418 rows, blend order contiguous 1 to 418]

The page lists, per player, Yahoo / ESPN / Fantrax positions, ADP and
order, and a blended ADP (189 with a Yahoo ADP, 344 ESPN, 293 Fantrax). Its
Yahoo column against the owner's paste: 186 comparable rows, 130 differ,
none by more than 2.0 (Bronny James 103.5 in the paste vs 101.5; AJ Green
106.8 vs 105.4) — the page was captured a day earlier (30 September) and
Yahoo's ADP moves a few tenths a day in the deep rounds. Positions: 0 of 189
differ. The owner's description ("Joseph Mamone pulls this data directly
from Yahoo") holds for this page. ESPN's and Fantrax's columns are a
reference for how other rooms price the same men (Flagg ESPN 17.3 vs Yahoo
10.3; Brunson ESPN 12.9 vs Yahoo 21.4; Sabonis ESPN 16.9 vs Fantrax 38.1);
the league is a Yahoo league and the deck prices from Yahoo alone.

## 5. Last year's draft: the re-paste against the room model

[EVIDENCE: `arena/data/league_draft_2025-26_raw_2026-10-01.txt` (md5
`195e819bed615b1a088e8b3b25e24d0a`) against `arena/draft_boards.json`
["2025-26"] and `league_intel_2025-26.md` §12]

156 of 156 picks agree on pick number, seat and team name; one spelling
differs (#128 "Bobby Portis Jr." vs the stored "Bobby Portis"); the
manager map agrees on all twelve teams ("Robert" for the stored "Robby").
The snake is consistent with the round-one order (the owner picked 4th). The
8/04 ingestion stands; the E18 profiles, the room model and the arena's
opponents do not re-derive. The paste is kept as the audit copy.

## 6. Deck v38 — what changed on the page

- Mkt rank: from `yahoo-2026-10-01.csv` (F8), 297 priced; the colophon's
  Data paragraph re-worded for the 10/01 source and the positions change.
- Positions on 54 rows; no stat line, tag, placement or judgment card
  changed (the judgment layer keeps today's date from the morning build).
- Planes gate: 314 shared, team 0, exclusion 0, drift 0, propagation 0;
  lines 184 (warning; D-WO1-1, the next report).
- Roster verification: this morning's direct-complete ESPN run (333 of 334,
  one exemption, Tony Bradley) stands; freshness re-stamped with the
  pool-changes assertion for this build.

## 7. Gates (2026-10-01)

| gate | result |
|---|---|
| kit `yahoo_market.py` transcription gate (I1–I5) | PASS — 300 blocks, 188 with ADP, XRank gaps none |
| kit `yahoo_market.py` hard unmatched gate | PASS — 296 of 324 matched, 28 accepted absences, 0 possible spelling variants |
| kit `sync_positions.py` (scratch, assertions on every row) | kit 51 changed / 245 unchanged / 28 unmatched; deck 54 / 243 / 37; a second run changes 0 |
| kit `rank_engine.py` provenance gate | PASS — board regenerated, 200 of 324; no rank moved, positions only |
| kit `check_report.py` | PASS (this file) |
| kit `check_provenance.py` | PASS — all rows sourced |
| kit `check_derived.py` | PASS — all 13 dated artifacts reproduce byte-for-byte at their pins (the 10/01 Yahoo intake and the 9/30 Hashtag pages registered) |
| deck `build_deck.py` gates 1–7 + F8 | all pass; planes 314 shared · team 0 · exclusion 0 · drift 0 · propagation 0; lines 184 (warning); market `yahoo-2026-10-01.csv` priced 297/334, 0 days old; pool `ebb38ca7be4f`; injection round-trip OK (gate 6 refused the first colophon wording — "54 rows" read as a pool count — and passed the reworded one) |
| deck `check_parity.py` | PARITY: EXACT MATCH (324 market ranks compared, 289 priced in the parity pool) |
| deck `test_card.py` / `test_draft.py` / `test_gates.py` | CARD all 68 cases passed / all 62 cases passed / all 37 cases passed |
| deck `full_dom_check.mjs` on the built page | 128 assertions, 0 failed, 0 page errors, pass (`arena/results/full_dom_check_2026-10-01_v38.json`) |
| artifact publish | Version 38 (id `1790888734-8b44`) at the standing URL after a fresh read of Version 37; page 366,330 bytes, sha256 `2cb28de98b35401f…` |

## Watchlist

- **The four Yahoo team placements** the deck carries as free agents
  (Westbrook SAC, Konchar NYK, Valančiūnas DEN, Batum LAC) and Clarkson
  (NYK on both): ESPN's roster feed at the next pull is the second outlet
  (the verifier skips FA rows, so it did not flag them).
- **Drummond (ADP 105.4) and Morez Johnson (116.6)** are priced inside
  the draftable 156 with kit rows but no deck rows; **Yang Hansen** has no
  row anywhere and went #126 in mock 59 (D59-3).
- **The ESPN projections page** the owner pasted into chat (interrupted
  mid-paste): a PDF print of it, like the two Hashtag pages, lands verbatim
  and parses the same way; the chat paste cannot be transcribed to the
  verbatim standard at that length.
- **The deck's survival chips** now run on the 10/01 prices; mock 60 is
  their first room on it.
- Carried: D59-1 (insert re-numbering), D59-2 (the advice line), the
  league settings screenshot (D-G5), WO-5.

## Open-item receipts

| item | query run (2026-10-01) | dated finding |
|---|---|---|
| (this intake) | machine joins and parses only — no web research | the 10/01 daily pull's receipts cover the window |
| Westbrook, Konchar, Valančiūnas, Batum, Clarkson | none this report — Yahoo's team column is one outlet (F2) | flagged for the next pull's ESPN check |
| Jalen Duren, Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the daily pull's dedicated queries, same day (after-report-2026-10-01.md) | all HELD on 2026-10-01; Yahoo's ADP for Porziņģis 99 (XRank 152), Ingram 62.8, Kawhi 30.4 are prices, not news |

## Bounds

- The ADP cross-check compares two captures a day apart; it bounds
  transcription error at two picks, it does not prove the paste exact.
- Positions were set from the page the room displays; if Yahoo widens
  eligibility in-season, the pool lags until the next paste.
- The Hashtag ADP page's platform columns were assigned by group order
  (Yahoo, ESPN, Fantrax); one row (Jakucionis, two groups, no Yahoo ADP)
  could not be assigned and is left unlabelled in the CSV.
- The ESPN and Fantrax columns are not used by any instrument.
- The deck's Mkt movement counts compare the two builds' price snapshots;
  the rank among priced rows is by price only (ties by name).

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-ADP-1 | Westbrook (SAC), Konchar (NYK), Valančiūnas (DEN), Batum (LAC): Yahoo lists them on teams; the deck carries FA. Resolve at the next pull against ESPN's roster feed and a second outlet, and move the rows if confirmed? | yes, next pull, two outlets |
| D-ADP-2 | Andre Drummond and Morez Johnson Jr.: priced inside the draftable 156 (ADP 105.4, 116.6), kit rows exist, no deck rows. Twin the kit rows onto the deck at the next pull (placement check, line, tag) so the card can price them? | yes, next pull |
| D-ADP-3 | Positions: both planes now carry the draft-analysis page's set (the room's). Keep syncing positions from each Yahoo draft-analysis paste and stop using the rankings page for eligibility? | yes; D-G3 closed |
| D-ADP-4 | ESPN's projections page: the owner prints it to PDF (as with the Hashtag pages) so it lands verbatim and becomes a fourth projection line next to Hashtag's? | yes, when convenient; the chat paste is not transcribed |
| D-ADP-5 | Hashtag's ADP page: keep as a reference capture only (no instrument reads ESPN/Fantrax ADP), or add the blend as a second price column on the card? | reference only until the draft; revisit for 2027 |

## Provenance

- Inputs: the owner's paste and uploads of 2026-10-01, kept verbatim
  (`yahoo-raw-2026-10-01.txt`; the two Hashtag extractions; the draft
  re-paste in the deck repo). The Yahoo outputs are pinned to commit
  `020771c` and reproduce under `check_derived.py`.
- Every number is a command's output or a field of the files named.
- Not verified: Yahoo's team column for the four flagged men (F2).
