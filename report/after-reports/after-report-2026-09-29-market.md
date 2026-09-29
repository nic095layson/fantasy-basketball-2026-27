# After-Report — 2026-09-29 market intake: expert consensus top 50 and Yahoo's 9/28 top-250 with official position eligibility

**Owner requests (2026-09-29, verbatim):** "Here is a TOP 50 Consensus
combination of experts' individual rankings. Please aggregate into your
memory" (a CSV upload), then: "This is dated 9/28, Yahoo's Top 250 Cat
players and OFFICIAL POSITION ELIGIBILITY" (a paste of the rankings page).
"Memory" here is the repo — a chat memory is invisible to the next session
(DATA-PULL §0) — so both land in the kit's market layer under the work
order's rules: raw kept verbatim, every name joined to the pool under the
hard gate, a provenance row, a comparison against the board, and no board
row changed by either (owner decision 2026-08-21; fix F2).

**Method:** `report/market/experts_market.py` (new, on the Yahoo-intake
pattern) and `report/market/yahoo_market.py 2026-09-28 rankings`; both
stamped with their inputs and registered in `report/check_derived.py`, which
reproduces every dated artifact byte-for-byte (8 of 8). Every number below is
read from the generated files; the position diff was computed in this
session against the committed pool and the deck's `data/players.csv`
(sha `c0bf82bf4d39`). Verification: this file passes `report/check_report.py`.

Pull window: 2026-09-29 → 2026-09-29 (a market intake, not a roster pull;
the 9/29 pull-log rows cover the window).

**Headline.** The experts agree with the board more than Yahoo's room does
(Spearman 0.620 vs 0.515 over the same 50 names), 43 of their top 50 sit in
ours, and the disagreements run in both directions along the board's known
fault lines (FT%/TO drags on Giannis and Sengun; steals and free throws on
Daniels and Kyrie). Yahoo's 9/28 list joined 244 of 318 pool rows with zero
spelling-variant trips and names **six players inside its top 250 the pool
does not carry**. Its official eligibility gives **82 of 244 players at
least one position the pool does not list, never fewer** — 40 of them in
the draftable top 156 — which is a change the deck's positional reads
should carry before the draft (D-M1).

---

## 1. What landed

| source | file | rows | joined | gate |
|---|---|---|---|---|
| expert consensus (owner upload) | `report/market/experts-raw-2026-09-29.csv` (verbatim, UTF-8 BOM tolerated) → `experts-2026-09-29.csv`, `unmatched-experts-2026-09-29.md`, `disagreements-experts-2026-09-29.md` | 50 | 50 of 50, no alias needed | PASS |
| Yahoo 9-cat rankings page, 9/28 (pasted 9/29) | `report/market/yahoo-9cat-rankings-raw-2026-09-28.txt` (verbatim) → `yahoo-9cat-rankings-2026-09-28.csv`, `unmatched-yahoo-9cat-rankings-2026-09-28.md` | 250 | 244 pool rows matched; 74 pool rows beyond Yahoo's 250, accepted by the mechanical absence check (0 possible spelling variants); 6 Yahoo names not in the pool | PASS (I1, I4–I6; no XRank gaps) |
| provenance | `report/market/provenance.csv` | +2 rows (7 total), merged by (source, fetched_on) | — |
| derived gate | `report/check_derived.py` | 2 new entries, 8 of 8 reproduce | PASS |

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

## Watchlist

- D-M1 position sync: until it lands, the deck under-counts roster
  flexibility for 40 draftable players (Daniels, Maxey, Edwards and Giddey
  among them).
- Pool completeness: five Yahoo-top-250 names without a kit row (Clifford,
  Simmons, Riley, Flemings, Collins) — next pull, sourced rows.
- Clingan (ours 119, experts 44, Yahoo 54): the largest disagreement in the
  file; re-read the Portland role at the next pull.
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
- The position diff treats order as irrelevant (`PG,SG` equals `SG,PG`) and
  the deck's `p` column as the deck's truth; the deck-vs-Yahoo count (103)
  was computed in this session, not by a committed script.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-M1 | Sync position eligibility to Yahoo's official list on both planes (82 kit rows, 103 deck rows), rebuild and republish the deck? | sync before the next mock: the platform's eligibility is the league's rule |
| D-M2 | Add the five missing Yahoo-top-250 names to the pool at the next pull (sourced rows, two outlets each)? | add at the next pull |
| D-M3 | Should the expert average enter the consensus column the Yahoo intake averages (our rank, XRank, ADP)? | no — reference only, as the work order's gated step 5 stands |

## Provenance

- Inputs: the owner's CSV upload and rankings paste (this session,
  2026-09-29), kept verbatim in `report/market/`; stamps name every input
  file, its sha256 and row count, and the commit it was read from.
- Not verified: nothing here rests on web research.
