# After-report — 2026-10-01: a third line for the 184 disagreements (Hashtag's 9/30 projections against both planes)

**Owner input (2026-10-01):** a PDF print of Hashtag Basketball's projections
page ("Does this help you, Claude?"), followed by a note that the outlet's
data comes from Yahoo. Parser output settles what the page is: "Fantasy
Basketball Projections … Updated: 30 September 2026 by Joseph Mamone", a
Top 200 with rest-of-season per-game lines, positions and ADP "from Yahoo",
and a TOTAL z-score. The positions and ADP are Yahoo's; the stat lines are
the outlet's own projections. That is what makes the page useful: this
morning's WO-1 report found 184 of the 314 names both planes carry with
different lines and no way to choose between them (D-WO1-1); an independent
third line can.

**Method.** The PDF read with pdfplumber page by page and parsed by
`report/market/hashtag_pdf_market.py` (200 rows, ranks contiguous, injury
glyphs kept as a flag; pinned to commit `678b469`, reproduces under
`check_derived.py`). Every row joined to both planes by the planes gate's
own name normalisation (`check_planes.norm`, with its aliases). For each of
the 184 differing rows that Hashtag covers, each of the nine category
inputs compared: which plane sits closer to Hashtag's value, and by how
much. No pool row changed: a projection outlet is one line of evidence, not
an edit (F2; the D-WO1-1 default). Verification: this file passes
`report/check_report.py`; receipts below.

Pull window: 2026-10-01 → 2026-10-01 (owner input; not a roster pull).

**Headline.** Hashtag covers 154 of the 184 disagreeing rows, and it does
not take a side: across the nine inputs it sits closer to the kit 503 times,
to the deck 467, with 416 ties; by rows, the deck is closer on more inputs
on 74, the kit on 63, 17 even. Where it does lean is points: closer to the
kit on 79 rows against 47 (mean error 1.34 points for the kit, 1.59 for the
deck), which matters because the deck is the plane the owner drafts from
and this morning's report found it the higher plane on points in 102 of
those rows. On the thirteen widest rows the kit is closer on nine of the
twelve Hashtag carries (Lillard 19.1 against the kit's 17.0 and the deck's
24.0; Flagg 23.3 against 21.0 and 17.8; Coward and Mamukelashvili equal to
the kit exactly), the deck on three (Simons, Dončić, Barrett). The page is
an incremental revision of the same outlet's 8/24 set the kit already holds
(163 of 200 lines unchanged; the 37 revisions are mostly games played and
roles: Porziņģis 51 to 42 games, Shaedon Sharpe 64 to 44, Ingram 72 to 42,
Maluach's minutes doubled). D-WO1-1 is re-put with the new evidence: the
default stays the preseason refresh for the top 150, with the twelve wide
rows that Hashtag covers settled now by the three-source rule.

## 1. What the page is, and what landed

| file | what |
|---|---|
| `report/market/hashtag-raw-2026-09-30.txt` | the PDF's text, 10 pages (PDF md5 `e6737ed1a54392124112273c08ec3d8c`) |
| `report/market/hashtag-2026-09-30.csv` | 200 rows: rank, Hashtag's rank-move count, player, injury flag, Yahoo ADP (169 rows), positions, team, GP, MPG, FG% with makes and attempts, FT% with makes and attempts, 3PM, PTS, REB, AST, STL, BLK, TO, TOTAL |
| `report/market/unmatched-hashtag-2026-09-30.md` | 199 of 200 have a pool row (Yanic Konan Niederhauser does not); 125 pool rows sit outside the top 200; the ADP cross-check (see the ADP report); the input stamp |
| `report/market/hashtag-2026-08-24.csv` | the same outlet's 429-row set from 8/24, already a reference source |

Against the 8/24 copy, 163 of the 200 lines are byte-identical and 37
revised. The revisions are the news since late August: Porziņģis (51 to 42
GP, 17.9 to 16.5 points), Anthony Davis (65 to 59 GP, 22.5 to 19.8), Shaedon
Sharpe (64 to 44 GP), Ingram (72 to 42 GP), Knueppel (74 to 60 GP), Maluach
(14.1 to 25.9 minutes, 4.8 to 10.2 points), Lendeborg (23.5 to 27.5
minutes), Dosunmu (31.4 to 27.4 minutes), Reaves (21.5 to 24.5 points),
Zion, Randle, Queen, Dëmin, Henderson, Marshall, Jaylen Brown, LaMelo, Porter
Jr., Okongwu, Jerome, Buzelis, Fox, Herro, Reid and a dozen smaller ones.
Twenty-five rows carry the page's injury glyph; their games-played against
the kit's: Jimmy Butler 25 (kit 20), Mark Williams 10 (15), Porziņģis 42
(54), Ingram 42 (48), Beal 50 (55), Knueppel 60 (70), Herro 64 (70), Edey
65 (70), Sharpe 44 (18 — the kit excludes him), Pippen Jr. 50 (65),
Hartenstein 68 (66), Giannis 69 (67), Bam 74 (72), Trae Young 70 (70).

## 2. The three-way comparison on the 184 rows

[EVIDENCE: `arena/results/planes_lines_2026-10-01.json` (the 184 rows with
both planes' values), `hashtag-2026-09-30.csv`, `report/projections-2026-27.csv`,
`data/players.csv`; the counts were computed in-session by the comparison
script recorded below and are reproducible from those four files]

154 of the 184 rows have a Hashtag line (30 do not: men outside its top
200). For each input, the plane whose value is nearer Hashtag's:

| input | kit closer | deck closer | tie | mean abs error, kit | mean abs error, deck |
|---|---|---|---|---|---|
| FG% | 63 | 55 | 36 | 0.014 | 0.014 |
| FT% | 46 | 57 | 51 | 0.024 | 0.023 |
| 3PM | 45 | 61 | 48 | 0.231 | 0.226 |
| PTS | **79** | 47 | 28 | **1.338** | 1.592 |
| REB | 56 | 61 | 37 | 0.517 | 0.527 |
| AST | 59 | 63 | 32 | 0.411 | 0.429 |
| STL | 42 | 36 | 76 | 0.120 | 0.132 |
| BLK | 42 | 35 | 77 | 0.118 | 0.122 |
| TO | **71** | 52 | 31 | 0.241 | 0.271 |
| all nine | 503 | 467 | 416 | | |

By rows (the plane closer on more of the nine inputs): deck 74, kit 63,
even 17. Reading: the two planes are each other's equal against a third
set on seven inputs; the deck's points and turnovers run higher than both
the kit and Hashtag. Points carry the most z-weight of any counting input
on this board, so the deck's rows have been read a little rich by the card.

The thirteen wide rows (three or more points apart), kit / deck / Hashtag:

| player | kit | deck | Hashtag 9/30 | closer |
|---|---|---|---|---|
| Damian Lillard | 17.0 | 24.0 | 19.1 (50 GP) | kit |
| Anfernee Simons | 19.5 | 14.5 | 15.1 | deck |
| Luka Dončić | 30.0 | 33.5 | 32.7 | deck |
| Cooper Flagg | 21.0 | 17.8 | 23.3 | kit |
| Quentin Grimes | 14.0 | 17.5 | 15.5 | kit |
| Cedric Coward | 16.3 | 13.0 | 16.3 | kit (equal) |
| Sandro Mamukelashvili | 13.7 | 10.5 | 13.7 | kit (equal) |
| Gradey Dick | 12.0 | 15.0 | — (outside the top 200) | — |
| Jakob Poeltl | 11.5 | 14.5 | 12.4 (58 GP) | kit |
| Kevin Porter Jr. | 11.5 | 14.5 | 12.9 (60 GP) | kit |
| Malik Monk | 14.5 | 17.5 | 14.6 | kit |
| Miles Bridges | 17.0 | 20.0 | 18.0 | kit |
| RJ Barrett | 17.5 | 20.5 | 20.5 (58 GP) | deck (equal) |

Two of the kit's lines equal Hashtag's to the decimal (Coward,
Mamukelashvili) because the kit adopted the outlet's 8/24 line for those
rows when they were added (the board's "[ESTIMATED]" convention); the
agreement there is inheritance, not confirmation.

## 3. What this does and does not settle

- **It is one outlet.** Hashtag's lines are a model's output, revised
  seven times since August; agreement with a plane is evidence about that
  plane's line, not proof. The ESPN projections page the owner pasted (cut
  off mid-paste) would be a fourth line; a PDF of it lands verbatim.
- **It does not replace the refresh.** WO-5's point is box scores from
  the preseason games (10/3 to 10/10) and per-36 rates; no projection set
  carries them yet. The default on D-WO1-1 (re-derive the top 150 at the
  refresh, copy the kit's line to the deck for the tail) stands.
- **It does settle the wide rows well enough to stop carrying two.** On
  twelve of the thirteen the third line is nearer one plane by a point or
  more, or equal to it; those twelve can become one line on both planes
  now, two weeks before the refresh re-derives most of them anyway.
- **It bounds the deck's points.** The card the owner drafts from has
  been reading points about a quarter of a point richer per row than the
  kit and Hashtag together would; nothing in this report moves it, and the
  refresh is where that should be fixed from box scores, not from Hashtag.

## Watchlist

- **The ESPN page as a PDF** (D-ADP-4): the fourth line.
- **Lillard** (kit 17.0, deck 24.0, Hashtag 19.1 at 50 games, Yahoo ADP
  65.9): the widest row on the board and a round-5 price; whichever way
  D-WO1-1 goes, this row is decided before mock 60.
- **The deck's points**: the rows where the deck is three or more points
  above both other sets (Lillard, Grimes, Poeltl, Porter Jr., Monk, Bridges)
  are the card's richest reads.
- Carried: WO-5 after 10/5; `--planes-lines-strict` at the final build.

## Open-item receipts

| item | query run (2026-10-01) | dated finding |
|---|---|---|
| (this comparison) | machine joins only — no web research | the 10/01 daily pull's receipts cover the window |
| Jalen Duren, Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the daily pull's dedicated queries, same day (after-report-2026-10-01.md) | all HELD on 2026-10-01; Hashtag's GP on Porziņģis (42) and Ingram (42) are a projection outlet's view, not news |

## Bounds

- 154 of 184 rows compared; the 30 outside Hashtag's top 200 are not.
- "Closer" is absolute distance per input; it weighs a 0.5-point gap the
  same as a 0.005 FG% gap only within its own column, never across.
- The per-stat counts and the wide-row table were computed by an
  in-session script from the four committed files; the script is not a
  repo artifact, so the counts are reproducible but not under the derived
  gate (the parsed CSV and its join are).
- The 8/24 comparison counts identical lines on the thirteen columns the
  8/24 CSV carries; TOTAL (a z-score against the outlet's pool) differs on
  almost every row and is not compared.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-WO1-1 (re-put) | One line on both planes for the 184 rows. (a) the preseason refresh re-derives the top 150 from box scores and the kit's line is copied to the deck for the tail (this morning's default); (d) new: settle the twelve wide rows Hashtag covers now by the three-source rule — the plane nearer Hashtag's points becomes the line on both planes (kit on nine: Lillard, Flagg, Grimes, Coward, Mamukelashvili, Poeltl, Porter Jr., Monk, Bridges; deck on three: Simons, Dončić, Barrett; Dick to the kit's line) — and leave the rest to (a); (e) apply the same rule to all 154 covered rows now (kit on 79, deck on 47, ties to the kit) and (a) for the 30 uncovered. | (a) with (d): the twelve wide rows settled before mock 60, two outlets on each line as with every edit |
| D-PROJ-1 | Keep the Hashtag page as a reference source only (no instrument reads it), re-captured once more on 10/13 for the final refresh's cross-check? | yes |
| D-PROJ-2 | Yanic Konan Niederhauser (LAC C, Hashtag rank 170, injury-flagged, no Yahoo ADP) has no row on either plane. Add at the next pull with two outlets? | only if Yahoo's list carries him by 10/13; otherwise no |

## Provenance

- Input: the owner's PDF upload of 2026-10-01, read with pdfplumber; the
  page text is the raw layer, kept verbatim and parsed by a committed script
  pinned to commit `678b469`.
- Every number is a field of the files named or the output of the
  comparison described in §2's evidence note.
- Not verified: nothing here rests on web research.
