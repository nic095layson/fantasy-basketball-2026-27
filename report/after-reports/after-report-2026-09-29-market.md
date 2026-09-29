# After-Report — 2026-09-29 market intake: four sources in one day — the expert consensus top 50, Yahoo's 9/28 top 250 with official position eligibility, a projected top 150 with last season's lines, and RotoBaller's 250 projected lines

**Owner requests (2026-09-29, verbatim):** "Here is a TOP 50 Consensus
combination of experts' individual rankings. Please aggregate into your
memory" (a CSV upload), then: "This is dated 9/28, Yahoo's Top 250 Cat
players and OFFICIAL POSITION ELIGIBILITY" (a paste of the rankings page);
then "Here is more data for you to aggregate, research, consider and
synthesize. Please note this is a little outdated from 9/26/26, however, you
can still utilize the player context that it provides for your real life
synthesizing" (a pasted article: "Projected Top 150 for 2026-27", with each
player's 2025-26 line, a VALUE score, Yahoo ADP and pre-rank snapshots and
role notes); then "One final 250 player database for you to analyze and
consider for today. This is from Rotoballer" (a CSV of projected 9-cat
lines). "Memory" here is the repo — a chat memory is invisible to the next session
(DATA-PULL §0) — so both land in the kit's market layer under the work
order's rules: raw kept verbatim, every name joined to the pool under the
hard gate, a provenance row, a comparison against the board, and no board
row changed by either (owner decision 2026-08-21; fix F2).

**Method:** `report/market/third_party_market.py` (new, one intake for the
three third-party ranking files: parse, join under the hard gate, agreement,
disagreements, team mismatches, and — where the file carries a per-game line —
the kit's projection against it, row by row) and `report/market/yahoo_market.py
2026-09-28 rankings`; all stamped with their inputs and registered in
`report/check_derived.py`, which reproduces every dated artifact byte-for-byte
(10 of 10). Every number below is
read from the generated files; the position diff was computed in this
session against the committed pool and the deck's `data/players.csv`
(sha `c0bf82bf4d39`). Verification: this file passes `report/check_report.py`.

Pull window: 2026-09-29 → 2026-09-29 (a market intake, not a roster pull;
the 9/29 pull-log rows cover the window).

**Headline.** Four external views of the same pool landed today and the
board sits inside the pack, not outside it: rank agreement with the kit runs
0.62 (experts, 50 names), 0.76 (the projected 150), 0.82 (RotoBaller, 242
names) and 0.83 (Yahoo's 9/28 list). The projected 150 agrees with the
kit's roster ledger on every one of its 150 teams; RotoBaller disagrees on
one (Claxton, whom the kit and the article both have in Chicago). Yahoo's
official eligibility gives **82 of 244 players at least one position the
pool does not list, never fewer** — 40 of them in the draftable top 156 —
a change the deck's positional reads should carry before the draft (D-M1).
Against RotoBaller's projected lines the kit runs high on volume across the
league (points +0.85, rebounds +0.50, assists +0.21 per player on average;
percentages, threes and stocks neutral), but against last season's actual
lines it does not (points −0.42): RotoBaller projects a regression the kit
does not, and a league-wide tilt cancels in a relative board. What does
not cancel is the handful of rows where the kit is high on its own —
**Poole, Turner, Ware, Ingram, Trae Young, Herro, Cameron Johnson, Braun,
Eason** — and Mobley's free-throw assumption. Those are the re-derivation
list (D-M4), and one of them, Poole, sits under the draft-56 report's
follow-the-card arm (§7).

---

## 1. What landed

| source | file | rows | joined | gate |
|---|---|---|---|---|
| expert consensus (owner upload) | `report/market/experts-raw-2026-09-29.csv` (verbatim, UTF-8 BOM tolerated) → `experts-2026-09-29.csv`, `unmatched-experts-2026-09-29.md`, `disagreements-experts-2026-09-29.md` | 50 | 50 of 50, no alias needed | PASS |
| Yahoo 9-cat rankings page, 9/28 (pasted 9/29) | `report/market/yahoo-9cat-rankings-raw-2026-09-28.txt` (verbatim) → `yahoo-9cat-rankings-2026-09-28.csv`, `unmatched-yahoo-9cat-rankings-2026-09-28.md` | 250 | 244 pool rows matched; 74 pool rows beyond Yahoo's 250, accepted by the mechanical absence check (0 possible spelling variants); 6 Yahoo names not in the pool | PASS (I1, I4–I6; no XRank gaps) |
| projected top 150 (owner paste, dated 9/26) | `report/market/projected150-raw-2026-09-26.csv` (the structured fields transcribed under invariants: ranks contiguous, stats in range; the prose read in-session, not stored) → `projected150-2026-09-26.csv`, `unmatched-…`, `disagreements-…` | 150 | 150 of 150; 3 rows with no 2025-26 games (Haliburton, Kyrie, Lillard) | PASS |
| RotoBaller overall 9-cat projected rankings (owner upload) | `report/market/rotoballer-raw-2026-09-29.csv` (verbatim) → `rotoballer-2026-09-29.csv`, `unmatched-…`, `disagreements-…` | 250 | 242 of 250; 8 names without a pool row (Clifford, Ament, De Larrea, Riley, Cissé, González, Bryant, Wolf), 0 spelling variants | PASS |
| provenance | `report/market/provenance.csv` | +4 rows (9 total), merged by (source, fetched_on) | — |
| derived gate | `report/check_derived.py` | 4 new entries, 10 of 10 reproduce | PASS |

## 2. The expert consensus against the board

| measure | value |
|---|---|
| Spearman rho, our rank vs expert average rank (50) | 0.620 |
| Spearman rho, our rank vs Fantrax ADP (50) | 0.567 |
| Spearman rho, our rank vs Yahoo 9/22 XRank, same 50 | 0.515 |
| median absolute gap, our rank vs expert rank | 8 places |
| experts' top 50 inside our top 50 | 43 of 50 |
| our top-50 names the experts leave out | Embiid, Kel'el Ware, Myles Turner, Tyler Herro, Cameron Boozer, Michael Porter Jr, Ty Jerome |

Where the board is higher by 10 or more places (8): Dyson Daniels (+39; ours
9, theirs 48 — steals and turnovers), Kyrie Irving (+25; 16 vs 41, with the
0.78 availability already applied), Darius Garland (+22), Devin Booker
(+20), Domantas Sabonis (+18), Anthony Davis (+15), Karl-Anthony Towns (+13),
Chet Holmgren (+10). Where the experts are higher by 10 or more (13):
Donovan Clingan (−75; ours 119, theirs 44), Giannis (−51; 59 vs 8 — the
FT%/TO drag of a 9-cat z-sum), Matas Buzelis (−32), Alperen Sengun (−26),
Dejounte Murray (−26), Jalen Duren (−24), Scottie Barnes (−22), Lauri
Markkanen (−22), Tyrese Haliburton (−17; the kit's 27 against the deck's 7 —
the two planes' standardizations differ on him, as on Poeltl in the draft-56
report), Kevin Durant (−17), Brandon Miller (−17), LaMelo Ball (−16), Jalen
Johnson (−12). Full tables with the board's z-lean per row:
`disagreements-experts-2026-09-29.md`. The three names the draft-56 audit
asked about (Cameron Johnson, Braun, Eason) are outside the experts' top 50,
consistent with that report's finding; OG Anunoby is their 50th (ours 44).

## 3. Yahoo's 9/28 top 250

Six names inside Yahoo's top 250 have no kit row: Bradley Beal (XRank 177,
LAC), Nique Clifford (217), Ben Simmons (230), Will Riley (234), Kingston
Flemings (247), Zach Collins (250). The deck plane carries Beal already
(planes check: 22 deck-only rows); the other five are pool-completeness
items for the next pull, each needing a sourced projection row (two
outlets, fix F2). Movement since the 9/22 rankings page is not computed
here — the rankings path writes no moves section — and the deck's Mkt rank
stays on the 9/22 draft-analysis paste (ADP, else XRank; F8).

## 4. Official position eligibility — the diff that matters

Of the 244 matched players, the pool's positions equal Yahoo's on 162.
On **82** Yahoo lists at least one position the pool does not (the pool's
set is a strict subset in 81 cases; one row differs outright); Yahoo never
lists fewer. The deck's `data/players.csv` differs from Yahoo on 103 rows
and, on some rows, from the kit as well — the two planes were never
reconciled on positions. In a Yahoo league eligibility is the platform's
rule, not a news fact: it needs no second outlet, and the deck's positional
slots (PG/SG/G/SF/PF/F/C/C), its family reads and the mock opponents'
positional need all read this column.

### The 40 inside the draftable top 156

| kit # | player | pool positions | Yahoo official | Yahoo XRank |
|---|---|---|---|---|
| 5 | Tyrese Maxey | PG | **PG,SG** | 6 |
| 8 | Anthony Edwards | PG,SG | **PG,SF,SG** | 7 |
| 9 | Dyson Daniels | SF,SG | **PG,SF,SG** | 69 |
| 21 | Trey Murphy III | SF,SG | **PF,SF,SG** | 24 |
| 29 | Jalen Williams | PF,SF | **PF,SF,SG** | 37 |
| 30 | Amen Thompson | PG,SG | **PG,SF,SG** | 28 |
| 32 | Josh Giddey | PG,SG | **PG,SF,SG** | 19 |
| 35 | Scottie Barnes | C,PF,SF | **C,PF,SF,SG** | 17 |
| 52 | Kristaps Porzingis | C | **C,PF** | 137 |
| 54 | Jaden McDaniels | SF | **PF,SF** | 80 |
| 55 | De'Aaron Fox | PG | **PG,SG** | 71 |
| 56 | Mikal Bridges | PF,SF | **PF,SF,SG** | 63 |
| 60 | Brandon Miller | PF,SF | **PF,SF,SG** | 32 |
| 64 | Herb Jones | SF,SG | **PF,SF,SG** | 122 |
| 65 | Payton Pritchard | PG | **PG,SG** | 73 |
| 66 | Jimmy Butler | PF,SF | **PF,SF,SG** | 138 |
| 75 | Dejounte Murray | PG | **PG,SG** | 59 |
| 76 | Fred VanVleet | PG | **PG,SG** | 139 |
| 78 | PJ Washington | C,PF | **C,PF,SF** | 164 |
| 80 | Alex Sarr | C | **C,PF** | 72 |
| 81 | Jordan Poole | SG | **PG,SG** | 211 |
| 84 | Anfernee Simons | SG | **PG,SG** | 197 |
| 89 | Pascal Siakam | C,PF | **C,PF,SF** | 55 |
| 92 | Cason Wallace | PG | **PG,SF,SG** | 124 |
| 98 | Aaron Nesmith | SF | **PF,SF,SG** | 167 |
| 114 | Draymond Green | PF | **C,PF** | 157 |
| 122 | Yaxel Lendeborg | PF | **PF,SF** | 129 |
| 123 | Bilal Coulibaly | SF | **SF,SG** | 210 |
| 124 | Miles Bridges | PF | **PF,SF** | 95 |
| 126 | Devin Vassell | SG | **SF,SG** | 143 |
| 127 | Kyle Filipowski | C | **C,PF** | 216 |
| 131 | Alex Caruso | PG | **PG,SF,SG** | 202 |
| 133 | Paolo Banchero | PF | **PF,SF** | 61 |
| 137 | Shaedon Sharpe | PG,SG | **PG,SF,SG** | 203 |
| 138 | Scotty Pippen Jr. | PG | **PG,SG** | 169 |
| 147 | Collin Sexton | PG | **PG,SG** | 190 |
| 150 | Caleb Wilson | PF | **PF,SF** | 94 |
| 151 | De'Anthony Melton | PG | **PG,SG** | 241 |
| 154 | Marcus Smart | PG | **PG,SG** | 229 |
| 156 | Jared McCain | SG | **PG,SG** | 222 |

### The other 42

| kit # | player | pool positions | Yahoo official | Yahoo XRank |
|---|---|---|---|---|
| 157 | Santi Aldama | PF | **PF,SF** | 183 |
| 158 | Ayo Dosunmu | PG,SG | **PG,SF,SG** | 110 |
| 159 | Tobias Harris | PF | **PF,SF** | 140 |
| 162 | Luguentz Dort | SG | **SF,SG** | 212 |
| 164 | Kelly Oubre | SF | **PF,SF,SG** | 147 |
| 165 | Malik Monk | SG | **PG,SG** | 223 |
| 166 | Rui Hachimura | PF | **PF,SF** | 121 |
| 170 | De'Andre Hunter | SF | **PF,SF** | 187 |
| 176 | Darryn Peterson | SG | **PG,SG** | 130 |
| 178 | Julian Champagnie | PF,SF | **PF,SF,SG** | 181 |
| 183 | Moussa Diabate | C | **C,PF** | 153 |
| 185 | Ace Bailey | SF | **PF,SF** | 160 |
| 187 | Naji Marshall | PF,SF | **PF,SF,SG** | 191 |
| 189 | GG Jackson | PF | **C,PF,SF** | 184 |
| 190 | Keaton Wagler | SG | **PG,SG** | 238 |
| 191 | Grayson Allen | SG | **PG,SF,SG** | 178 |
| 192 | Derrick Jones Jr | SF | **PF,SF** | 207 |
| 195 | Klay Thompson | SG | **SF,SG** | 168 |
| 197 | Royce O'Neale | SF | **PF,SF** | 219 |
| 204 | Rob Dillingham | PG | **PG,SG** | 245 |
| 205 | Bennedict Mathurin | SG | **SF,SG** | 151 |
| 207 | Terrence Shannon Jr | SG | **SF,SG** | 232 |
| 209 | Jaylen Wells | SG | **SF,SG** | 218 |
| 210 | Tre Johnson | SG | **PG,SF,SG** | 227 |
| 213 | Bub Carrington | PG | **PG,SG** | 240 |
| 215 | Khris Middleton | SF | **PF,SF,SG** | 242 |
| 216 | Dillon Brooks | SF | **PF,SF,SG** | 163 |
| 218 | Max Strus | SG | **PF,SF** | 149 |
| 223 | Keldon Johnson | SF | **PF,SF** | 221 |
| 230 | Kyle Kuzma | PF | **PF,SF** | 174 |
| 234 | Sam Hauser | SF | **PF,SF** | 199 |
| 235 | Nikola Jovic | PF | **C,PF** | 235 |
| 245 | Jonathan Kuminga | PF | **PF,SF** | 155 |
| 248 | Gradey Dick | SG | **SF,SG** | 246 |
| 256 | Isaiah Collier | PG | **PG,SG** | 224 |
| 260 | Allen Graves | PF | **PF,SF** | 248 |
| 262 | Scoot Henderson | PG | **PG,SG** | 186 |
| 265 | Tristan da Silva | SF | **PF,SF** | 226 |
| 267 | Brice Sensabaugh | SF | **PF,SF,SG** | 233 |
| 268 | Joan Beringer | C | **C,PF** | 180 |
| 288 | Oso Ighodaro | C | **C,PF** | 165 |
| 302 | Morez Johnson Jr. | PF | **C,PF** | 204 |

## 5. The projected top 150 (9/26) — last season as the baseline

Rank agreement with the kit 0.756; 124 of its 150 inside our top 150; team
notes match the kit's verified ledger on all 150 (Kawhi to Toronto for
Ingram, LeBron and Brown to Philadelphia, George to Boston, Giannis to Miami
with Herro, Ware and Jaquez to Milwaukee, Harden to Cleveland for Garland,
Randle and Claxton in the four-team deal, Trae Young to Washington, Zubac
to Indiana, Kessler to the Lakers, Porziņģis to Golden State — every one
already in `roster-provenance.csv`). The article's value is its 2025-26
actual lines: the kit's 2026-27 projection against them, over 147 rows, is
neutral on points (−0.42 per player), threes, assists and stocks, slightly
above on rebounds (+0.30) and slightly below on free throws (−0.52). Seventy-
five rows cross a category threshold, as a projection should where the role
changed; the ones that matter to this owner's picks are in §7. The three
guards the owner built around have no 2025-26 games; the article discounts
them to 21 (Haliburton), 65 (Kyrie) and 99 (Lillard) [EVIDENCE:
`disagreements-projected150-2026-09-26.md` §A, §D, §E].

## 6. RotoBaller — projection against projection

The closest external ranking to the board (0.815; 218 of its 250 inside our
top 250) and, with Yahoo, the source the market itself follows most (0.941
against Yahoo XRank). Its projected per-game lines let the kit's be compared
like for like over 241 players [EVIDENCE: `disagreements-rotoballer-2026-09-29.md`
§E; `report/validation-2026-09-29/`-style direction table computed in-session]:

| category | kit minus RotoBaller, mean per player | rows kit higher : lower |
|---|---|---|
| PTS | +0.85 | 159 : 71 |
| REB | +0.50 | 177 : 51 |
| AST | +0.21 | 153 : 71 |
| TOV | +0.11 | 151 : 62 |
| 3PM, STL, BLK, FG% | within ±0.3 | near even |
| FT% | −0.35 | 105 : 131 |

Read with §5: the kit sits close to last season's actual volume while
RotoBaller projects a regression from it, so the tilt is RotoBaller's
conservatism as much as the kit's optimism, and a tilt every row shares
cancels in a relative board (the rank agreement is the highest of the four
sources). The rows that do not cancel — where the kit is high on its own —
are the ones to re-derive. Seventy-nine rows cross a threshold; the ones
that touch this owner's card:

| player | kit # / RotoBaller # / Yahoo # | kit line vs RotoBaller line (per game) | reading (evidence: `disagreements-rotoballer-2026-09-29.md` §E/§F, `yahoo-9cat-rankings-2026-09-28.csv`) |
|---|---|---|---|
| Jordan Poole | 81 / 230 / 211 | 19.5 pts, 3.0 threes, 4.5 ast, 1.2 stl vs 10.1 / 1.8 / 2.3 / 0.5 | the kit projects a starter, both sources a bench role — the largest disagreement of any name that reached the owner's card (§7) |
| Myles Turner | 40 / 104 / 108 | 15.0 pts, 7.0 reb, 2.0 blk vs 12.7 / 5.4 / 1.6 (last season 11.9 / 5.3 / 1.6) | the kit projects a bounce with Giannis gone; both sources and last season say no |
| Kel'el Ware | 39 / 65 / 77 | 14.5 / 10.5 / 1.8 blk vs 9.5 / 7.5 / 1.0 | a Milwaukee role the kit assumes and RotoBaller does not |
| Brandon Ingram | 88 / 202 / 67 | 20.0 pts, 4.5 ast vs 15.0 / 2.0 | the Achilles absence sits in the kit's GP, not its line; RotoBaller cut the line |
| Cameron Johnson | 61 / 105 / 158 | 17.0 / 2.7 threes vs 14.2 / 2.1 | below the row threshold but the same direction as every source (D56-1) |
| Christian Braun | 83 / 168 / 173 | 15.0 / 5.0 reb / 2.8 ast / 1.1 stl vs 12.0 / 4.5 / 2.4 / 0.7 | the kit is high across the whole line (D56-1) |
| Tari Eason | 67 / 140 / 150 | 12.0 pts, 1.6 stl, 0.8 blk, FG% 48 vs 9.6 / 1.2 / 0.5 / 44.1; last season 10.4 / 1.2 / 0.5 / 41.6 | the FG% assumption is 6 points above both; the stocks +0.4 (D56-1) |
| Evan Mobley | 19 / 24 / 29 | FT% 74 vs 70; last season 60.6 | the free-throw assumption is the owner's #1 FT% column's soft spot |
| Karl-Anthony Towns | 6 / 15 / 16 | 24.0 pts vs 20.9; last season 20.1 | a New York usage bet |
| Tyrese Haliburton | 27 / 12 / 9 | 18.5 pts, 8.5 ast, GP 60 vs 17.4 / 9.3 | the kit is the most cautious source on him |
| Kyrie Irving | 16 / 43 / 36 | 23.0 / 5.0 ast, GP 60 vs 21.8 / 4.4 | lines agree; the kit's availability discount is the lightest of the four |
| Damian Lillard | 91 / 84 / 57 | 17.0 / 5.5, GP 45 vs 16.6 / 5.0 | agreement |
| OG Anunoby | 44 / 44 / 52 | 16.5 / 2.1 / 1.4 stl vs 17.0 / 2.3 / 1.5 | agreement — the deck's #27 is its standardization, not the line |
| Brook Lopez | 96 / 144 / 156 | 12.0 / 1.8 blk / FG 51 vs 9.9 / 1.4 / 46.2 | the kit is high on the Clippers role |
| Jakob Poeltl | 128 / 160 / 123 | 11.5 / 9.0 reb vs 11.8 / 7.7 | agreement on the line; the deck's #47 is its standardization (D56-2) |

Team mismatch: one — RotoBaller lists Claxton in Brooklyn; the kit's
ledger and the article have the July trade to Chicago. Eight RotoBaller
names have no pool row; two (Clifford, Riley) are also inside Yahoo's 250.

## 7. What it means for the draft — the synthesis

- **The board is not an outlier.** Four sources, four agreements between
  0.62 and 0.83, and the highest with the one that carries full projected
  lines. The first-principles engine and the market read the same league.
- **The point-guard trio, read against the world.** Haliburton: every
  source ranks him higher than the kit (Yahoo 9, experts 10, RotoBaller 12,
  the article 21, the kit 27) — the kit's GP 60 is the most cautious
  Achilles read on the table. Lillard: agreement everywhere (kit 91,
  RotoBaller 84, the article 99). Kyrie: the kit's #16 is the outlier
  (RotoBaller 43, experts 41, Yahoo 36, the article 65) — not on the line,
  which every source writes the same, but on the availability discount;
  the card had White over him at #39 anyway. Net: the plan's risk is
  concentrated in Kyrie's games played, not in the guards' production.
- **The #130 counterfactual needs a caveat.** The draft-56 report priced
  following the card at #130 (Poole for Sheppard) at +3.7 points of
  championship and hindsight named Poole the best alternative there. Both
  rest on the kit's Poole line — 19.5 points as a starter — which
  RotoBaller (230), Yahoo (211) and the projected 150 (absent from its 150)
  all reject. Until that line is re-derived, treat the #130 leg as
  unproven; the other two legs (White, Pritchard) stand on lines every
  source agrees with. A bounds note now says so in the draft-56 report.
- **The repeat-name audit, completed.** The draft-56 report found the
  card's late-round set warranted by the arithmetic and questioned three
  projection rows. Two more sources now say the same about the same three
  rows (Cameron Johnson, Braun, Eason), and add Poole, Turner, Ware and
  Ingram. That is the re-derivation list, ranked by how often the card
  reaches them: Turner and Eason (card #1 at #106 and #111 in mock 56),
  Cameron Johnson (#87), Braun (#130/#135), Lopez (#154), Poole (the
  hindsight alternative), then Ware and Ingram.
- **Positions.** Unchanged from §4: the platform's eligibility is the
  league's rule; 40 draftable players are under-counted on the deck.

## Watchlist

- D-M1 position sync: until it lands, the deck under-counts roster
  flexibility for 40 draftable players (Daniels, Maxey, Edwards and Giddey
  among them).
- Pool completeness: five Yahoo-top-250 names without a kit row (Clifford,
  Simmons, Riley, Flemings, Collins) — next pull, sourced rows.
- Clingan (ours 119, experts 44, Yahoo 54, RotoBaller 61): the largest
  disagreement in the expert file; re-read the Portland role at the next pull.
- Poole (ours 81, RotoBaller 230, Yahoo 211): the largest disagreement that
  touched the owner's analysis; first on the re-derivation list with Turner
  and Eason.
- Yahoo market paste: the 9/22 ADP file still prices the deck; a fresh
  draft-analysis paste in early October re-prices it.

## Open-item receipts

| item | query run (2026-09-29) | dated finding |
|---|---|---|
| (this intake) | machine join and diff only — no web research in this report | pull receipts for the window live in `after-report-2026-09-29.md` §8 (11 flagged names) |

## Bounds

- The expert file is a top 50 with no source URL; provenance records it as
  the owner's upload with its columns. Fantrax ADP is a different room
  population from Yahoo's.
- The rankings page carries no ADP; agreement with the room's price is
  measured on the 9/22 draft-analysis paste.
- The kit-vs-source line comparison uses the kit's projection row as
  committed on 2026-09-29 and each source's file as uploaded; RotoBaller's
  file carries no games-played column, so its availability view is only in
  its rank. The direction table in §6 was computed in-session from the
  joined CSVs, not by a committed script.
- The position diff treats order as irrelevant (`PG,SG` equals `SG,PG`) and
  the deck's `p` column as the deck's truth; the deck-vs-Yahoo count (103)
  was computed in this session, not by a committed script.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-M1 | Sync position eligibility to Yahoo's official list on both planes (82 kit rows, 103 deck rows), rebuild and republish the deck? | sync before the next mock: the platform's eligibility is the league's rule |
| D-M2 | Add the five missing Yahoo-top-250 names to the pool at the next pull (sourced rows, two outlets each)? | add at the next pull |
| D-M3 | Should the expert average enter the consensus column the Yahoo intake averages (our rank, XRank, ADP)? | no — reference only, as the work order's gated step 5 stands |
| D-M4 | Re-derive the projection lines the kit holds high on its own — Poole, Turner, Eason, Cameron Johnson, Braun, Lopez, Ware, Ingram, and Mobley's FT% — from current role research before the next mock (the 9/16 ritual; two outlets per line)? Supersedes D56-1. | re-derive before the next mock, Poole / Turner / Eason first |
| D-M5 | Add the eight RotoBaller names without a pool row with the five from Yahoo (D-M2)? Clifford and Riley are on both lists. | add the two shared names at the next pull; the six rookies only if Yahoo's list carries them |

## Provenance

- Inputs: the owner's CSV upload and rankings paste (this session,
  2026-09-29), kept verbatim in `report/market/`; stamps name every input
  file, its sha256 and row count, and the commit it was read from.
- Not verified: nothing here rests on web research.
