# After-Report — 2026-09-29 market intake, fifth source: an unnamed outlet's 9-cat top 144 with player profiles, and its sleepers / breakouts / busts

**Owner requests (2026-09-29, verbatim):** "Here is another player ranking
and real life situation profile for you to synthesize into your rankings:"
(a paste of a 9-cat top 144 with prose profiles on the top 50), then the
companion piece ("Sleepers … Breakouts … Busts"), then two questions
answered in the session and summarized in §6: "does the 'real life
basketball' narrative help you at all? Or are you mainly interested in
statistical category data" and "Do you use the live mock drafts that I
conduct (which are within Yahoo) to aggregate player draft positions and
for your data?"

**Source:** the outlet is not named in either paste (image credits and a
"SEE ALSO" line survive; no byline or masthead). It is recorded as an owner
paste and, under fix F2, cannot count as an independent outlet for any
pool-row edit until it is named (D-P1). **Method:**
`report/market/third_party_market.py profiles 2026-09-29` — the ranking
transcribed to `profiles-raw-2026-09-29.csv` (145 rows: the article numbers
126 twice, so `Rank` is the list position and `Printed` the article's
number; teams given as nicknames, mapped to codes; a short `Claim` in the
analyst's own words for each of the 50 profiled players — the prose itself
was read in-session and not stored, the 9/26 precedent), the two lists to
`profiles-tags-raw-2026-09-29.csv` (38 rows), both joined to the pool under
the hard gate, outputs generated `--as-of 30e968d` and registered in
`report/check_derived.py` (11 of 11 dated artifacts reproduce byte-for-byte).
Every number below is read from the generated files. Verification: this file
passes `report/check_report.py`.

Pull window: 2026-09-29 → 2026-09-29 (a market intake, not a roster pull;
the 9/29 pull-log rows cover the window).

**Headline.** The source tracks Yahoo's own list almost exactly (rho 0.946
against the 9/28 XRank) and agrees with the board about as well as the other
outside views do (rho 0.735; the four 9/29 sources ran 0.62–0.83)
[EVIDENCE: `disagreements-profiles-2026-09-29.md` §A]. Where it splits from
the board, the split is the same one every source makes, and it falls into
three clusters (§3): stars the board fades on availability or 9-cat shape
(Tatum, Haliburton, Giannis, Barnes, LeBron, Jaylen Brown, Banchero);
role-dependent young or bench men every source puts 60–130 places above the
board (Rollins, Harper, Dybantsa, Nurkić, Kevin Porter Jr, Queta, Dёmin);
and steals-and-blocks profiles the board alone holds high (Dyson Daniels,
Anthony Davis, Embiid, Ty Jerome, Kyrie, Garland, Day'Ron Sharpe). The
profiles carry the useful part: dated, checkable situation claims (§4), of
which Tatum's is the one that reaches the card — every outside view has him
top-13 while the kit's 65-game line and the deck's Achilles tag put him 17th
on the board and 16th on the card at your #10 in mock 57 (D-P2). No pool row
changed; the decisions are on the sheet.

## 1. What landed

| item | result |
|---|---|
| ranking rows | 145 (printed 1–144, with 126 twice: Portis and Davion Mitchell); joined to the pool 145 of 145 — 0 without a pool row, 0 spelling-variant trips |
| tag rows | 38 (sleepers 6 named + 6 other; breakouts 6 + 6; busts 6 + 8); joined 38 of 38 |
| alias added | `Egor Demin` ← `Egor Dёmin` (Cyrillic ё, which NFKD does not fold) |
| provenance | `provenance.csv` row `profiles / 2026-09-29 / 145` |
| reproducibility | `check_derived.py`: 11 of 11 (the new intake pinned at 30e968d) |
| board rows changed | none (fix F2; a single unnamed outlet) |

## 2. Agreement with the board

| measure | value |
|---|---|
| Spearman rho, board vs source | 0.735 |
| Spearman rho, board vs Yahoo 9/28 XRank, same 145 rows | 0.791 |
| Spearman rho, source vs Yahoo 9/28 XRank | 0.946 |
| median absolute gap | 25 places |
| source's 145 inside the board's top 145 | 121 |
| board 20+ places higher | 31 rows |
| source 20+ places higher | 55 rows |
| team mismatches vs the kit ledger | 3 — the article predates the moves: Kawhi (article LAC; kit TOR, executed 2026-09-14), Ingram (article TOR; kit LAC), Peyton Watson (article DEN; kit CLE) |

The 0.946 against Yahoo is the number to read first: this ranking is, for
practical purposes, Yahoo's list with prose attached. Its disagreements with
the board are therefore the market's disagreements with the board, which
the 9/29 intake already measured, and §3 reads them that way.

## 3. Where the board stands alone — the cross-source check

Our rank, then this source, RotoBaller (9/29), the projected top 150
(9/26), the expert consensus top 50 (9/29), and Yahoo's 9/28 XRank / 9/22
ADP [EVIDENCE: the five joined CSVs in `report/market/`]:

| player | board | this source | RotoBaller | proj. 150 | experts | Yahoo XRank / ADP | reading |
|---|---|---|---|---|---|---|---|
| Jayson Tatum | 17 | 7 | 5 | 13 | 9 | 8 / 10.4 | every view top-13; the kit's 65 GP and the deck's Achilles tag are the whole gap (D-P2) |
| Tyrese Haliburton | 26 | 12 | 12 | 21 | 10 | 9 / 17.8 | same mechanism, 60 GP and the Achilles tag (D-P2) |
| Giannis Antetokounmpo | 57 | 10 | 7 | 8 | 8 | 10 / 8.5 | the board's 9-cat shape (FT% and turnovers), a stance, not a data gap (D-P4) |
| Scottie Barnes | 35 | 11 | 11 | 15 | 13 | 17 / 13.9 | shape (FT%, turnovers); stance (D-P4) |
| LeBron James | 141 | 44 | 47 | 46 | — | 44 / 39.6 | the board's rest-and-age line; stance (D-P4) |
| Jaylen Brown | 132 | 40 | 62 | 42 | — | 45 / 28.5 | the source's own bust call; the board is lower than the bust-caller (D-P4) |
| Paolo Banchero | 129 | 45 | 60 | 51 | — | 61 / 34.3 | turnovers and FT%; stance (D-P4) |
| Ryan Rollins | 175 | 48 | 83 | 61 | — | 60 / 76.0 | every source 48–83: the post-Giannis role is not in the kit's line (D-P3) |
| Dylan Harper | 168 | 65 | 76 | — | — | 97 / 84.0 | role (D-P3) |
| AJ Dybantsa | 173 | 72 | 103 | — | — | 96 / 77.3 | rookie role (D-P3) |
| Jusuf Nurkić | 283 | 122 | 136 | 91 | — | 114 / 113.8 | the board's largest gap in the file, 161 places (D-P3) |
| Kevin Porter Jr | 231 | 89 | 126 | 80 | — | 131 / 117.3 | role (D-P3) |
| Neemias Queta | 248 | 113 | 96 | 138 | — | 103 / 112.6 | role (D-P3) |
| Egor Dёmin | 206 | 115 | 115 | — | — | 162 / 120.5 | role (D-P3) |
| Dyson Daniels | 9 | 60 | 53 | 33 | 48 | 69 / 61.6 | the board alone: steals and turnovers carry him; kept as first-principles |
| Anthony Davis | 7 | 52 | 31 | 58 | 22 | 43 / 37.2 | blocks and rebounds at 0.78 availability still rank 7th here |
| Joel Embiid | 21 | 68 | 49 | 47 | — | 46 / 50.7 | 45 GP on the kit line; the source lists him among busts |
| Kristaps Porziņģis | 48 | 121 | 189 | 117 | — | 137 / 101.1 | moot: owner veto (DO NOT DRAFT) and out indefinitely pre-camp |
| Jimmy Butler | 65 | 136 | 237 | 79 | — | 138 / 117.4 | the kit prices 20 GP; the deck excludes him outright (ACL recovery) — the two planes already disagree with each other |
| Ty Jerome | 50 | 114 | 71 | 74 | — | 89 / 107.4 | steals and FT%; the source lists him among breakouts while ranking him 114th |
| Kyrie Irving | 16 | 53 | 43 | 65 | 41 | 36 / 52.1 | the board's 0.78 (ACL) still leaves him 16th; mock 57's #39 pick |
| Darius Garland | 23 | 55 | 56 | 89 | 45 | 56 / 64.2 | assists and threes; first-principles |
| Day'Ron Sharpe | 68 | 105 | 86 | 120 | — | 90 / 94.3 | the board made the sleeper call before the source did |

Three clusters, then. The first is availability the board prices and the
market does not (Tatum, Haliburton): that is a fact question and the only
one here that changes what the card shows. The second is 9-cat shape the
board penalizes and points-league habits forgive (Giannis, Barnes, LeBron,
Brown, Banchero): the board's stance, measured and deliberate, and the Mkt
column already tells the drafter where the room will take them. The third is
role: seven names every outside source puts 60–160 places above the board,
all of them men whose 2026-27 role changed this summer (Rollins and Porter
in the post-Giannis Bucks, Harper behind a declining Fox, Nurkić and Queta
as presumed starters, two rookies). Those are re-derivation candidates in
the ordinary sense — two dated outlets on the role, then the line — and the
mock record says why they matter: rooms take exactly these names 30–80
slots before the board would.

## 4. The profiles' situation claims against the kit

The kit encodes availability as games played on the projection line; the
deck as a note tag (`*-risk` 0.78, `*-recovery` and `out-*` excluded). The
source's claim is the short form recorded in `profiles-raw-2026-09-29.csv`
[EVIDENCE: that file; `projections-2026-27.csv`; the deck's `data/players.csv`].

| player | source # | board # | kit GP | deck tag | the source's claim | reading |
|---|---|---|---|---|---|---|
| Jayson Tatum | 7 | 17 | 65 | inj-achilles-risk | Brown gone, Tatum runs the offense; 28/10/6 possible; no injury caveat | the source treats the Achilles as history; the kit and deck do not — D-P2 |
| Tyrese Haliburton | 12 | 26 | 60 | inj-achilles-risk | first-round value when healthy | "when healthy" is the whole question; D-P2 |
| Kyrie Irving | 53 | 16 | 60 | inj-acl-risk | (not profiled; "Kyrie Irving set to return" in Flagg's profile) | consistent with the kit's 60 GP |
| Kawhi Leonard | 9 | 25 | 35 | inj-risk | in limbo at press time; suspension risk; top-10 if he plays | the kit's 35 GP already prices the risk the source names; article predates the Toronto move |
| Jalen Duren | 38 | 56 | 72 | — | no contract at press time | the standing 10/1 qualifying-offer item; kit HELD |
| Lauri Markkanen | 36 | 47 | 66 | — | top-10 per game but 42 games (hip), 47 the year before | the kit's 66 GP is more optimistic than the source's own caution — watch |
| Domantas Sabonis | 39 | 18 | 70 | — | February meniscus surgery, expected ready; age 30 | consistent |
| Josh Giddey | 18 | 30 | 72 | — | May ankle arthroscopy, expected full go | consistent |
| Evan Mobley | 31 | 34 | 74 | — | missed 60 games over three seasons; healthy now | the kit's 74 GP is the optimistic end — watch |
| Ivica Zubac | 46 | 79 | 72 | — | recovered from the rib injury | consistent on availability; the gap is the line |
| Trae Young | 22 | 39 | 70 | — | 15 games last season; boom-bust | the kit's 70 GP is the optimistic end — watch |
| Cade Cunningham | 5 | 11 | 72 | — | missed 11 games late (collapsed lung) | consistent |
| Jalen Williams | 35 | 29 | 74 | — | injury-plagued season; bounce-back expected | consistent |
| Walker Kessler | 37 | 37 | 72 | inj-shoulder-risk | some injury issues | consistent; both planes carry the risk |
| Zion Williamson | 81 | 96 | 50 | inj-risk | bust: missed 20 games; career-low scoring | the board is lower than the bust-caller |
| Joel Embiid | 68 | 21 | 45 | inj-risk | listed among busts | the kit's 45 GP is the stricter view; the per-game line carries him |
| Stephen Curry | 25 | 12 | 62 | inj-risk | still elite when active | consistent |
| Trey Murphy III | 28 | 20 | 70 | inj-shoulder-risk | a trade out of New Orleans possible | trade chatter only; no row action |

Reading the table as a whole: on eighteen availability claims the kit is
stricter than the source on four (Kawhi, Zion, Embiid, Butler), looser on
three (Markkanen, Mobley, Trae Young — watch items, not edits), and the two
that matter for the draft are Tatum and Haliburton, where the source's
silence on the Achilles is itself the claim.

## 5. Sleepers, breakouts and busts against the board

[EVIDENCE: `disagreements-profiles-2026-09-29.md` §G]

| section | names | board already agrees | board disagrees |
|---|---|---|---|
| sleepers (12) | White, Kessler, Coby White, Ware, Coward, Sharpe; Sarr, Zubac, Anunoby, George, Powell, Champagnie | 6 — the board ranks Derrick White 22 (source 27), Sharpe 68 (105), Anunoby 44 (59), Paul George 49 (67), Kessler 37 (37), Powell 85 (78) | 6 — Coby White 98 (56), Coward 140 (96), Zubac 79 (46), Sarr 75 (57), Ware 82 (90), Champagnie 176 (129) |
| breakouts (12) | Flagg, Reaves, Miller, Rollins, Harper, Black; Dybantsa, Camara, Dёmin, C. Wilson, Jerome, Murray-Boyles | 5 — Flagg 13 (14), Reaves 19 (19), Jerome 50 (114), Camara 81 (117), Murray-Boyles 86 (125) | 7 — Rollins 175 (48), Harper 168 (65), Dybantsa 173 (72), Dёmin 206 (115), C. Wilson 145 (80), Miller 60 (43), Black 181 (139) |
| busts (14) | J. Brown, Fox, Morant, Zion, Brooks, Vučević; Herro, F. Wagner, Porter Jr, Randle, Embiid, Hart, Turner, Queen | 8 — Brown 132 (40), Zion 96 (81), Morant 138 (100), Brooks 216 (unranked), Vučević 130 (unranked), Randle 110 (83), F. Wagner 66 (62), Queen 162 (unranked) | 6 — Fox 53 (87), Hart 51 (91), Turner 87 (118), Herro 43 (63), Porter Jr 45 (70), Embiid 21 (68) |

Two of the source's sleeper calls (Sharpe, Anunoby) and two of its breakout
calls (Jerome, Camara) are names the board has carried above the market for
weeks; the six busts the board disagrees on are all steals-or-blocks
profiles (Fox, Hart, Turner, Embiid) or scorers the board rates on threes
and FT% (Herro, Porter). The breakout list is where the two views part
company most, and it is the same role cluster as §3.

## 6. What the narrative is for (the owner's questions, on the record)

- An outside ranking never moves a row (fix F2, owner decision 2026-08-21);
  it lands as the reference layer and the tables above. The only outside
  number that changes the card's behavior is Yahoo's ADP (the Mkt column and
  the survival chips).
- A checkable situation claim — a role, a return date, a contract, a games
  expectation — is what can reach a row, through the re-derivation ritual
  and its two-dated-outlets rule. The evidence-shaped claims in these pastes
  (Reaves' 28.8/5.8/6.8 without LeBron in October–November, Coby White's
  18.3/5.3/4.0 without Ball and Bridges, Sharpe's per-36 line, Giddey's May
  arthroscopy, Kawhi's investigation) are the useful part; "still a bucket"
  is not.
- The owner's six live rooms from seat 10 are used as a test set (the card
  graded pick by pick; the survival chips calibrated on rooms 51–52 and
  tested out of sample on 53–57; the repeat-name audit), never as a price:
  six observations per player cannot replace Yahoo's ADP, but they can test
  it, which is what the chips' Brier score does.

## Watchlist

- Tatum and Haliburton: five outside views against the kit's 65 / 60 games
  and the deck's Achilles tags; the next named report on either return
  timeline settles D-P2.
- The role cluster (Rollins, Harper, Dybantsa, Nurkić, Kevin Porter Jr,
  Queta, Dёmin): two dated outlets each on the 2026-27 role before the next
  pull (D-P3).
- Markkanen (66 GP), Mobley (74), Trae Young (70): the kit's optimistic end
  against the source's caution; no edit, re-check at the first preseason
  report.
- Kawhi: the kit's 35 GP carries the suspension risk; a ruling either way
  moves the line.
- Duren: qualifying-offer deadline Thursday 10/1 (standing).
- The outlet's name (D-P1): once named, its claims can pair with a second
  outlet.

## Open-item receipts

| item | query run (2026-09-29) | dated finding |
|---|---|---|
| (this analysis) | file joins and the five committed market snapshots only — no web research in this report | pull receipts for the window live in `after-report-2026-09-29.md` §8 |

## Bounds

- The outlet is unnamed; nothing in it can satisfy fix F2 on its own, and
  its 0.946 agreement with Yahoo means it adds little independent signal on
  ranks. Its value is the situation claims, which are dated only by the
  paste (2026-09-29) and by internal evidence (Kawhi "at press time" in
  limbo; Duren unsigned) placing the writing before 9/14.
- The `Claim` column is the analyst's paraphrase, not the article's text.
- The ranking carries a numbering error (126 twice); list position is used
  as the source rank, so every printed number after 126 is one higher than
  the position.
- The board's ranks in §3 are the kit's first-principles ranks
  (`projections-2026-27.csv` at 30e968d); the deck's card rank for the same
  player can differ by a place or two (Tatum: board 17, card 16 in mock 57).
- No projection line was compared category by category: the source carries
  no stat line (RotoBaller and the projected 150 did; see the 9/29 report).

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-P1 | Name the outlet behind the two pastes so its claims can count toward the two-outlet rule; until then it is an owner paste | stays an owner paste; claims are watch items only |
| D-P2 | Tatum (kit 65 GP, deck 0.78) and Haliburton (60 GP, 0.78): every outside view has them top-13 and top-21; re-derive the availability from named return-date reporting now, or hold the tags until camp reporting settles? | hold; re-derive on the first named report of full participation or a return date — the card already shows the gap under the feed when the owner overrides it, as at #10 in mock 57 |
| D-P3 | The role cluster the board fades 60–160 places below every source (Rollins, Harper, Dybantsa, Nurkić, Kevin Porter Jr, Queta, Dёmin): run the role re-derivation (two dated outlets each) before the next pull? | yes — batch them into the next pull's ritual; the six live rooms show these names going 30–80 slots ahead of the board |
| D-P4 | The board's deliberate 9-cat fades (Giannis 57, Barnes 35, LeBron 141, Jaylen Brown 132, Banchero 129): keep the first-principles stance, or add a "market says" marker on the card? | keep; the Mkt column already carries the market's number and the survival chips read it |

## Provenance

- Inputs: the two owner pastes (this session, 2026-09-29), transcribed to
  `profiles-raw-2026-09-29.csv` (145 rows) and `profiles-tags-raw-2026-09-29.csv`
  (38 rows); joined by `third_party_market.py` at commit 30e968d against
  `projections-2026-27.csv` (324 rows), `yahoo-9cat-rankings-2026-09-28.csv`
  and `consensus-2026-09-22.csv`.
- Every number is read from `profiles-2026-09-29.csv`, `profiles-tags-2026-09-29.csv`,
  `disagreements-profiles-2026-09-29.md`, the four earlier joined CSVs and
  the deck's `data/players.csv` (tags).
- Not verified: nothing here rests on web research; the outlet, the article
  date and the roster moves it predates are inferred from the text itself.
