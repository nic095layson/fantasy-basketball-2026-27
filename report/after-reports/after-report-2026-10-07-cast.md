# After-report — 2026-10-07, second report: the three MOCK rooms on the real seating (63, 64, 65), the owner's challenge on the late card, the four decisions applied (D-CAST-1..4), and the Hashtag 10/6 page

**Owner request (2026-10-07, verbatim, three uploads):** three exported draft states (`draft_state_52/53/54.json` → mocks 63, 64, 65), then: "I do want to raise concern, as, Cam Thomas and Saddiq Bey would not be drafted in real life over the likes of Stephon Castle, Davion Mitchell, RJ Barrett, Rui Hachimura, and Keaton Wagner still available. Please provide a dissertation defense, however, I strongly believe this will need some fine tuning. I do believe the tool is very helpful when used in Live Mock drafts (against other humans), but when simulating the 11 personalities (and I'm sure it helps in your Monte Carlo, forecasting and computation). Please let me know your thoughts. As a starting point, would you want to take LAST season 2025-2026 stats for Thomas and Bey, vs. Castle, Mitchell, Barrett and let me know who provided more 9Cat Fantasy production?" — answered in chat with four proposed decisions; then, with the Hashtag projections page `FBall_10.6.pdf`: "Proceed with your decisions, logically, as you suggested and ensure accuracy, system integrity and integration testing."

**Rooms:** the deck's own MOCK mode, 12 × 13, owner seat 10, the eleven opponents the E18 behavioral models of the real league-mates in the league's real 2026-27 order (1 Oblena, 2 Noah, 3 Will, 4 Robby, 5 Kyle, 6 Martin, 7 John, 8 JCo, 9 Kevin, 11 Cayas, 12 Hegi). Not public rooms: LEDGER-eligible. **Deck used:** v47 for all three (rev `fca8f7c`, the 10/7 daily-pull build; the 10/6 Yahoo prices baked; Porziņģis veto live) — identified by the `cast` field each export carries and by the per-turn card echo (every 🎯 the owner took in mocks 63 and 65 is the v47 card's #1). **Method:** each state is the deck's own export (no Yahoo recap and no tool log exist for a MOCK), checked snake-consistent with every name in the pool; the grades are the deck plane's machine-derived retro (`yahoo-fantasy-basketball` `arena/results/m63_*.json`, `m64_*.json`, `m65_*.json`; deck card replayed from the v47 page; title odds on the league's real eight-team bracket). The defense in §2 is built from the same records plus a noise-free replay of the bots, Basketball-Reference's 2025-26 lines read on 10/7, and the Hashtag pages. Every figure below is read from a file named in Provenance; none is eyeballed. Verification: this file passes `report/check_report.py` and the deck's `judgment_open_items.py --check-report`; the gates table is §6.

Pull window: 2026-10-07 → 2026-10-07 (the second report of the day; the morning's `after-report-2026-10-07.md` is the roster pull — this one is analysis, two decisions that touched pool rows on both planes, one engine change, and one market intake).

**Headline.** Three practice rooms against the eleven modeled league-mates in their real seats, all on v47. Mock 63 — the card followed at 13 of 13 turns — grades **23.33 percent** on the real bracket (rank 2 of 12), expected weekly category wins 5.169, rank 1 of 12 (next 5.121). Mock 65 — also 13 of 13 — grades **23.19 percent** (rank 2), ECW 5.174 rank 1 (next 5.099). Mock 64 is the room the owner drafted the way a human would — the card's 🎯 at 2 of 13 turns, Tatum at #10, Durant, Adebayo, Irving, Banchero, Castle at #154 — and grades **7.63 percent** (rank 3), ECW 4.555 rank 3; the self-consistent follow-card chain from the same seat grades 18.97 percent (rank 2). The owner's challenge is upheld on the record (§2): human rooms draft Castle, Mitchell and Barrett in every one of the ten rooms on file and the cast never does, and the late card had offered men Yahoo does not list. Four decisions were applied and tested (§3): unsigned free agents are off every board on both planes (D-CAST-1), the round-11+ card draws only from priced rows (D-CAST-4, red-first 95 of 95, parity EXACT, DOM 130/130), the pre-registered bot experiment ran at N=30 (D-CAST-3: no variant ships — V2 (Yahoo XRank as the value axis) has the best M1 (7.39 picks against 12.07) and the better M2 (7.5 consensus names left undrafted per room against 10.43) but fails the M3 regression guard (Spearman 0.30 against the shipped early-round reach ordering; the eleven collapse to within ±3 of the market in rounds 1–6); V1 and V3 do not improve M2), and the Castle/Barrett lines are logged for WO-5 (D-CAST-2). Hashtag's 10/6 page is parsed and pinned (§5): it prices Bey 132, Castle 151, Barrett 153, Mitchell 172, Hachimura 182 and does not list Thomas, Goodwin or Ellis. Deck v48 is built and published.

## 1. Roster changes

No team label moved. Two decisions changed pool rows on both planes; the rows are listed because the planes gate, the board and the card all moved on them.

| plane | row | change | mechanism | outlets |
|---|---|---|---|---|
| both | Cam Thomas → out-unsigned (D-CAST-1) | deck tag `out-unsigned` (availability 0.0; was a plain note); kit GP 62 → 25 (the exclusion class) and off the board by the engine's unsigned-FA rule | unsigned free agent after camp opened; the pool row is his 2024-25 Brooklyn line (24.0 pts), on his 2025-26 line he grades 318th of 323 draftable | unsigned per Spotrac and the NBC Sports free-agent list, 2026-10-07; 2025-26 line read from Basketball-Reference 2026-10-07 |
| both | Jaden Ivey → out-unsigned (D-CAST-1) | deck tag `out-unsigned`; kit GP 64 → 25, off the board | waived by Chicago 2026-03-30, unsigned since | unsigned per Spotrac and the NBC Sports free-agent list, 2026-10-07 |
| deck | Lonzo Ball → out-unsigned (D-CAST-1; was `inj-risk`) | availability 0.78 → 0.0 | unsigned free agent; not a kit row | unsigned per Spotrac and his ESPN player page, 2026-10-07 |
| both | Rob Dillingham → out-unsigned (D-CAST-1) | deck tag `out-unsigned`; kit GP 50 → 25, off the board (he was outside the top 200 already) | waived by Charlotte 2026-09-28, cleared, unsigned | unsigned per RotoBaller, Saturday Down South and the Basketball-Reference transactions ledger, 2026-10-07 |
| kit | John Konchar (FA) held off the board | the engine's new unsigned-FA rule drops every team-FA row from the board and the z-score pool; his GP (30) is untouched and he was outside the top 200 | waived by New York 2026-09-30 | Hoops Rumors, RealGM (the provenance rows of 2026-09-30) |

Kit board after regeneration (`rank_engine.py`, 321 projected after the 4 unsigned are held): left the board — Cam Thomas (was 133), Jaden Ivey (was 154); entered — Taylor Hendricks (now 198), Isaiah Joe (now 200); 98 other rows moved by 1 to 5 places as the z-score pool lost four rows (no row moved more than five). Deck pool: draftable rows 323 → 319; the planes gate reports the three shared rows as the same decision on both planes (`--planes-waive` ×3, recorded in the build manifest; propagation 0, drift 0, team 0, exclusion 0).

## 2. The dissertation defense — why the late card and the cast offered Thomas and Bey, and what each part of it is worth

The owner's claim has two halves: (a) real managers would not draft Cam Thomas or Saddiq Bey over Castle, Mitchell, Barrett, Hachimura and Wagler (the deck's spelling of the Illinois guard; the page carries no Wagner at that position) while those five sat on the board; (b) the eleven personalities are drafting unlike their human selves. Both are tested against the record, not argued.

### 2a. The record — where humans and the cast actually took these men

Ten human rooms on file from seat 10 (mocks 51–54, 56–61) against the five cast rooms (55, 62–65). Pick numbers are the recorded draft positions; a dash is undrafted through 156.

| player | human rooms drafted (of 10) | human range | cast rooms drafted (of 5) | cast positions |
|---|---|---|---|---|
| Stephon Castle | 10 | 62–84 | 1 | #154 (m64) |
| Davion Mitchell | 10 | 102–129 | 1 | #156 (m64) |
| RJ Barrett | 10 | 117–140 | 0 | — |
| Rui Hachimura | 3 | 123–129 | 1 | #155 (m55) |
| Keaton Wagler | 1 | 153–153 | 0 | — |
| Dillon Brooks | 8 | 120–153 | 1 | #156 (m65) |
| Saddiq Bey | 8 | 136–149 | 5 | #153 (m55), #111 (m62), #136 (m63), #149 (m64), #135 (m65) |
| Cam Thomas | 0 | — | 3 | #154 (m62), #154 (m63), #154 (m65) |
| Jordan Goodwin | 0 | — | 0 | — |
| Keon Ellis | 0 | — | 0 | — |

Castle, Mitchell and Barrett go in every human room, between 62 and 140; the cast took Castle and Mitchell once each — both in mock 64, Castle by the owner at #154 and Mitchell with the last pick of the draft — and Barrett never. Cam Thomas has never been drafted by a human and was taken three times in cast rooms, all three by the owner at #154 following the card. Bey is drafted by humans in 8 of 10 rooms (136–149) and in every cast room (111–153): the owner's instinct on Bey is not supported by the record, and §2d says why.

### 2b. The mechanism in the bots — a noise-free replay of mock 63's last 66 opponent picks

Each personality scores a candidate as `adp_w × market rank + val_w × value rank` (plus the family bias, loyalty, the availability multiplier and a seeded noise term), with `adp_w` between 0.35 (Oblena) and 0.75 (Noah). The market rank is Yahoo's price (ADP, else XRank); the value rank is the deck's own 9-cat value on the committed lines. On the v47 page:

| player | market rank (Yahoo price) | deck value rank | blended rank, market-heaviest seat (Noah, 0.75 market) | blended rank, value-heaviest seat (Oblena, 0.35 market) |
|---|---|---|---|---|
| Stephon Castle | 53 | 251 | 102 | 182 |
| Davion Mitchell | 161 | 170 | 163 | 167 |
| RJ Barrett | 127 | 241 | 156 | 201 |
| Rui Hachimura | 162 | 186 | 168 | 178 |
| Keaton Wagler | 153 | 177 | 159 | 169 |
| Dillon Brooks | 134 | 210 | 153 | 183 |
| Saddiq Bey | 175 | 95 | 155 | 123 |
| Cam Thomas | 242 | 121 | 212 | 163 |
| Jordan Goodwin | 246 | 110 | 212 | 158 |
| Keon Ellis | 250 | 123 | 218 | 167 |

Replaying mock 63's opponent picks #85–#156 (66 picks) with the noise term removed, every bot took its own noise-free #1–#3 candidate 58 of 66 times — the room is doing what its formula says. At those turns the named men ranked, among the available candidates on the bot's own scale (median / best): Stephon Castle 60 / 13; Davion Mitchell 40 / 4; RJ Barrett 62 / 23; Rui Hachimura 56 / 8; Saddiq Bey 24 / 1; Cam Thomas 66 / 26. Castle sits 53rd on the market and 251st on value; even Noah at 0.75 market weight scores him around the 100th candidate in round 8, behind a dozen men the formula prices higher on both axes. The value term is doing it, and the value term is the committed line (§2d), not the engine.

### 2c. The card's own late rows — what D-CAST-4 changes, measured on the four cast rooms

The card's #1 is the blend50 score (half marginal weekly wins, half balanced value), price-blind by design. In round 13 of every cast room it had offered Cam Thomas and Jordan Goodwin, neither listed by Yahoo. The rule (§3b): from round 11 the candidates are the priced rows; an asterisk marks a row Yahoo does not price. 'Was' is the v47 card; 'now' is the same engine with the rule, on the v47 data (D-CAST-1 then removes Thomas everywhere).

| room | pick (round) | owner took | pool rows, then candidates | card was | card now |
|---|---|---|---|---|---|
| m62 | #130 (r11) | Collin Gillespie | 194 then 112 | Collin Gillespie, Herbert Jones, Daniel Gafford, Reed Sheppard, Christian Braun | Collin Gillespie, Herbert Jones, Daniel Gafford, Reed Sheppard, Christian Braun |
| m62 | #135 (r12) | Daniel Gafford | 189 then 107 | Daniel Gafford, Herbert Jones, Christian Braun, Cam Thomas*, Reed Sheppard | Daniel Gafford, Herbert Jones, Christian Braun, Jakob Poeltl, Reed Sheppard |
| m62 | #154 (r13) | Cam Thomas | 170 then 88 | Cam Thomas*, Jordan Goodwin*, Bilal Coulibaly, Santi Aldama, Scotty Pippen Jr. | Bilal Coulibaly, Santi Aldama, Scotty Pippen Jr., Wendell Carter Jr., Malik Monk |
| m63 | #130 (r11) | Collin Gillespie | 194 then 112 | Collin Gillespie, Saddiq Bey, Reed Sheppard, Daniel Gafford, Jerami Grant | Collin Gillespie, Saddiq Bey, Reed Sheppard, Daniel Gafford, Jerami Grant |
| m63 | #135 (r12) | Daniel Gafford | 189 then 107 | Daniel Gafford, Saddiq Bey, Jakob Poeltl, Keegan Murray, Santi Aldama | Daniel Gafford, Saddiq Bey, Jakob Poeltl, Santi Aldama, Keegan Murray |
| m63 | #154 (r13) | Cam Thomas | 170 then 88 | Cam Thomas*, Jordan Goodwin*, Santi Aldama, Bilal Coulibaly, Keon Ellis* | Santi Aldama, Bilal Coulibaly, Scotty Pippen Jr., Luguentz Dort, Quentin Grimes |
| m64 | #130 (r11) | Daniel Gafford | 194 then 112 | Daniel Gafford, Sandro Mamukelashvili, Cason Wallace, Saddiq Bey, Christian Braun | Daniel Gafford, Sandro Mamukelashvili, Cason Wallace, Saddiq Bey, Jakob Poeltl |
| m64 | #135 (r12) | Cason Wallace | 189 then 107 | Saddiq Bey, Cason Wallace, Christian Braun, Reed Sheppard, Cam Thomas* | Saddiq Bey, Cason Wallace, Christian Braun, Reed Sheppard, Santi Aldama |
| m64 | #154 (r13) | Stephon Castle | 170 then 88 | Cam Thomas*, Jordan Goodwin*, Santi Aldama, Wendell Carter Jr., Bilal Coulibaly | Santi Aldama, Wendell Carter Jr., Bilal Coulibaly, Scotty Pippen Jr., Malik Monk |
| m65 | #130 (r11) | Collin Gillespie | 194 then 112 | Collin Gillespie, Saddiq Bey, Reed Sheppard, Christian Braun, Cam Thomas* | Collin Gillespie, Saddiq Bey, Christian Braun, Reed Sheppard, Andrew Nembhard |
| m65 | #135 (r12) | Saddiq Bey | 189 then 107 | Saddiq Bey, Daniel Gafford, Christian Braun, Cam Thomas*, Reed Sheppard | Saddiq Bey, Daniel Gafford, Christian Braun, Santi Aldama, Jakob Poeltl |
| m65 | #154 (r13) | Cam Thomas | 170 then 88 | Cam Thomas*, Jordan Goodwin*, Santi Aldama, Bilal Coulibaly, Keon Ellis* | Bilal Coulibaly, Santi Aldama, Scotty Pippen Jr., Neemias Queta, Malik Monk |

Rounds 11 and 12 move by at most one row (an unpriced Thomas drops off the fifth slot); round 13 changes entirely in all four rooms. Bey stays on the round-11/12 card where he was: he is priced (Yahoo 119.9) and he is the value.

### 2d. Last season's production — the owner's starting question, answered on both engines

Basketball-Reference 2025-26 per-game lines (read 2026-10-07) scored through each engine's own z-score standardization against the current pool; 'committed' is the pool row each plane carries today.

| player | 2025-26 line (GP · pts · reb · ast · stl · blk · 3PM · FG% · FT% · TO) | deck rank on the 2025-26 line | deck rank on the committed line | kit rank on the 2025-26 line | kit rank on the committed line |
|---|---|---|---|---|---|
| Saddiq Bey | 72 · 17.7 · 5.6 · 2.5 · 0.9 · 0.1 · 2.1 · 0.451 · 0.841 · 0.9 | 85 | 95 | 86 | 102 |
| Davion Mitchell | 70 · 9.3 · 2.7 · 6.5 · 1.0 · 0.2 · 1.3 · 0.490 · 0.646 · 1.5 | 164 | 170 | 174 | 182 |
| RJ Barrett | 57 · 19.3 · 5.3 · 3.3 · 0.7 · 0.3 · 1.7 · 0.491 · 0.717 · 1.7 | 165 | 241 | 175 | outside 200 |
| Stephon Castle | 68 · 16.7 · 5.3 · 7.4 · 1.1 · 0.3 · 1.2 · 0.471 · 0.734 · 3.2 | 167 | 251 | 172 | 98 |
| Rui Hachimura | 68 · 11.5 · 3.3 · 0.8 · 0.6 · 0.3 · 1.7 · 0.514 · 0.694 · 0.6 | 228 | 186 | outside 200 | 166 |
| Cam Thomas | 42 · 13.5 · 1.7 · 2.6 · 0.2 · 0.1 · 1.2 · 0.410 · 0.811 · 1.8 | 318 | 121 | outside 200 | 133 |

Kit ranks in this table are on the morning's board (the one the question was asked against); the regenerated board in §1 moves them by at most a few places (Bey 102 → 101). Bey out-produced the three guards last season on both engines (85th on the deck, 86th on the kit, against 164–175 for Mitchell, Barrett and Castle); Hachimura trails them; Thomas, on 42 games of 13.5 points at .410 for Brooklyn, is 318th. So the owner's instinct is right about Thomas and wrong about Bey — and the committed lines carry a different problem: the deck prices Castle 251st and Barrett 241st on their committed lines (Castle 4.8 ast on .440, Barrett .630 FT), far below what either did last season; the kit prices Castle 98th. That is a projection-plane divergence, the WO-5 class of problem, and it is logged there (D-CAST-2) rather than patched in the card.

### 2e. Hashtag's view (the page uploaded with the directive)

Hashtag's 10/6 top-200 ranks Bey 132, Castle 151, Barrett 153, Mitchell 172, Hachimura 182; it does not list Thomas, Goodwin, Ellis or Wagler. Yahoo's 10/6 ADP has Castle 53.8, Barrett 112.4, Mitchell 117.6, Hachimura 117.9, Wagler 116.8, Bey 119.9, Brooks 113.7. Two independent markets agree with the human rooms and with the owner: these are draft picks in the 110–150 band, and a man neither market lists is not.

### 2f. The verdict

Three distinct mechanisms produced the picture the owner saw, and they get three distinct remedies. (1) An unsigned man with a stale line sat in the draftable pool with full availability — a data rule, fixed on both planes (D-CAST-1). (2) The late card was price-blind, so men no market lists could top it once the priced men who fit the roster were gone — a card rule, fixed with a red-first test and twins on every grading path (D-CAST-4). (3) The committed lines on Castle and Barrett are harsher than their 2025-26 production, so both the bots' value term and the card's value half rank them below their market — a projection question, which belongs to WO-5 with the two-outlet role rule (D-CAST-2). The bots' formula itself was tested at N=30 (D-CAST-3, §3c) against the human record and ships only if it passes the pre-registered bar. The tool is more trustworthy against humans because humans supply the market half of the room; the cast supplies it from the same prices but weighs the deck's value more, which is exactly where a stale or harsh line hurts twice.

## 3. The decisions applied, with their tests

### 3a. D-CAST-1 — unsigned free agents off every board, both planes

Rule: an unsigned free agent after camp opened is tagged `out-unsigned` on the deck (availability 0.0, so the pool, the card, the mock bots, the matrix and the z-score standardization all exclude him) and held at the exclusion class on the kit (GP 25, the planes-gate twin) and off the kit board by a new engine rule (`rank_engine.py`: team-FA rows leave the board and the z-score pool; the board's own caveat had stated this rule since Westbrook and the engine now enforces it). Exit condition: two independent dated outlets report a signing; the row is then re-derived on the new team and role. Applied to Thomas, Ivey, Ball, Dillingham (deck) and Thomas, Ivey, Dillingham, Konchar (kit). Each JUDGMENT card carries the decision and the exit condition. Build: gate 7 waivers ×3 as the same decision on both planes; drift 0, propagation 0.

### 3b. D-CAST-4 — the round-11+ card draws from the priced rows

Engine: `CARD_PRICED_FROM = 11` and `cardPool(pool, round)` in the deck's engine block; from that round the council shortlist, the blend50 scores and the sixth-row pin see only rows with a baked Yahoo price (ADP, else XRank); fewer than five priced rows left returns the whole pool; ranks, the matrix, the shelf count, the trap line and the advisor keep the whole pool. Red-first: six cases added to `scripts/test_card.py`, five failed on the unchanged engine (`CARD: 5 of 95 cases FAILED`), all 95 pass after. Twins: `full_dom_check.mjs` engineTop5, `check_parity.py` (the JS export and the Python replay — the Python side filters on `data/market-snapshot.csv`, the same price set parity item 6 already holds identical to the baked prices — and the constant is read from the page source and must equal the engine's export), `live_retro.py card_pool()` on all three card sites, gated on the constant's presence in the page at the revision each mock was drafted on, so every earlier mock replays byte-identically (mocks 63–65 at `fca8f7c`: rule absent, results unchanged). Effect: §2c.

### 3c. D-CAST-3 — the pre-registered bot-fidelity experiment at N=30

Design (`arena/results/castsim_design_2026-10-07.md`, written before the run): simulate 30 MOCK rooms per variant with the page's own engine (owner at 10 on the card's #1, the eleven on `managerScores` under the variant), score against the ten human rooms on file — M1 mean |cast mean pick − human mean pick| over players drafted in at least 5 human rooms; M2 human-consensus names (drafted in at least 8 of 10 human rooms) left undrafted per room; M3 a regression guard on the shipped bots' early-round reach ordering (Spearman ≥ 0.7 against V0 and mean absolute per-manager change ≤ 8). Variants: V0 shipped; V1 late market mode (from round 9 half of `val_w` moves to `adp_w`); V2 XRank value axis (the value rank is Yahoo's XRank where present); V3 both. Ship rule: the best M1 that also improves M2 over V0 and passes M3; none improving both → ship nothing. Three amendments were made before the N=30 run and are disclosed: M3's reference changed from the deck's value rank to the market rank, then to the V0 regression guard (a Yahoo-rank variant fails a value-rank reference by construction); and the engine module was rebuilt from the v48 page so V0 is the shipped bots on the shipped data (the four unsigned excluded, the owner's card on `cardPool`).

| variant | M1 mean abs gap (picks) | players scored | M2 consensus names left undrafted per room (mean) | M3 guard: Spearman vs V0 / mean abs change | guard | never drafted by the cast (of the human-reference set) |
|---|---|---|---|---|---|---|
| V0 | 12.07 | 147 | 10.43 of 143 | 1 / 0 | pass | 12 |
| V1 | 12.09 | 152 | 11.53 of 143 | 1 / 0 | pass | 7 |
| V2 | 7.39 | 153 | 7.5 of 143 | 0.3 / 4.48 | FAIL | 6 |
| V3 | 8.11 | 150 | 11.4 of 143 | 0.3 / 4.48 | FAIL | 9 |

Verdict by the pre-registered rule: **no variant ships — V2 (Yahoo XRank as the value axis) has the best M1 (7.39 picks against 12.07) and the better M2 (7.5 consensus names left undrafted per room against 10.43) but fails the M3 regression guard (Spearman 0.30 against the shipped early-round reach ordering; the eleven collapse to within ±3 of the market in rounds 1–6); V1 and V3 do not improve M2.** The shipped bots stay (V0). What V2 shows is worth keeping: with Yahoo's own rank as the value axis the cast drafts Castle, Barrett and Brooks and leaves only six human-reference names undrafted — but it does so by erasing the personalities the guard protects. The next candidate, to be pre-registered before any run: the XRank value axis from round 7 only, which leaves rounds 1–6 (the guard's window) on the shipped formula.

### 3d. D-CAST-2 — logged for WO-5

Castle (deck committed 4.8 ast on .440 FG, kit 98th) and Barrett (deck .630 FT) are re-derived at WO-5 from their 2025-26 per-36 lines scaled to the projected role, with two dated outlets for every role claim that moves a line, on both planes in one script with assertions, and the board diffed — the WO-5 procedure as written on 10/01. Not patched today: a line moved to fit a draft position is the error the two-plane design exists to catch.

## 4. The three rooms, graded

| room | card's 🎯 taken | as drafted (title odds, rank) | follow-card chain | ECW (rank; next) | favored of 11 | hindsight: turns with a better pick | largest single swap | survival chips (rows, predicted, realized, Brier) |
|---|---|---|---|---|---|---|---|---|
| mock 62 (10/6, v46) | 13 of 13 | 18.05% (rank 2) | 18.22% (rank 2) | 4.987 (rank 2; next 5.284) | 10 | 5 of 13 | Chet Holmgren at #15 (+0.103 cats/wk) | 48, 0.577, 0.521, 0.196 |
| mock 63 (10/7, v47) | 13 of 13 | 23.33% (rank 2) | 23.33% (rank 2) | 5.169 (rank 1; next 5.121) | 10 | 7 of 13 | Chet Holmgren at #15 (+0.060 cats/wk) | 48, 0.608, 0.521, 0.213 |
| mock 64 (10/7, v47) | 2 of 13 | 7.63% (rank 3) | 18.97% (rank 2) | 4.555 (rank 3; next 5.357) | 7 | 10 of 13 | Jalen Johnson at #10 (+0.154 cats/wk) | 53, 0.575, 0.509, 0.196 |
| mock 65 (10/7, v47) | 13 of 13 | 23.19% (rank 2) | 23.19% (rank 2) | 5.174 (rank 1; next 5.099) | 10 | 8 of 13 | Chet Holmgren at #15 (+0.117 cats/wk) | 48, 0.617, 0.542, 0.207 |

### Mock 63

| pick | deck 🎯 (Top-5) | owner took | card rank · gap (blend) | hindsight best single swap (ΔECW vs final rosters) |
|---|---|---|---|---|
| #10 | Jalen Johnson (Jalen Johnson, Jalen Williams, Kevin Durant, Donovan Mitchell, Anthony Davis) | Jalen Johnson | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #15 | Jamal Murray (Jamal Murray, Jalen Williams, Derrick White, Desmond Bane, James Harden) | Jamal Murray | #1 · +0.000 | Chet Holmgren +0.060 |
| #34 | Derrick White (Derrick White, Desmond Bane, OG Anunoby, Franz Wagner, Dyson Daniels) | Derrick White | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #39 | Onyeka Okongwu (Onyeka Okongwu, OG Anunoby, Dyson Daniels, Ivica Zubac, Cameron Boozer) | Onyeka Okongwu | #1 · +0.000 | OG Anunoby +0.041 |
| #58 | Payton Pritchard (Payton Pritchard, Tyler Herro, De'Aaron Fox, Jalen Suggs, Coby White) | Payton Pritchard | #1 · +0.000 | Tyler Herro +0.005 |
| #63 | De'Aaron Fox (De'Aaron Fox, Josh Hart, Isaiah Hartenstein, Jalen Suggs, Rudy Gobert) | De'Aaron Fox | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #82 | Isaiah Hartenstein (Isaiah Hartenstein, Zach LaVine, Yaxel Lendeborg, Myles Turner, Sandro Mamukelashvili) | Isaiah Hartenstein | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #87 | Yaxel Lendeborg (Yaxel Lendeborg, Sandro Mamukelashvili, PJ Washington, Jaden McDaniels, Herbert Jones) | Yaxel Lendeborg | #1 · +0.000 | PJ Washington +0.005 |
| #106 | Sandro Mamukelashvili (Sandro Mamukelashvili, Herbert Jones, Cason Wallace, Devin Vassell, Saddiq Bey) | Sandro Mamukelashvili | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #111 | Herbert Jones (Herbert Jones, Cason Wallace, Devin Vassell, Saddiq Bey, Daniel Gafford) | Herbert Jones | #1 · +0.000 | Saddiq Bey +0.023 |
| #130 | Collin Gillespie (Collin Gillespie, Saddiq Bey, Reed Sheppard, Daniel Gafford, Jerami Grant) | Collin Gillespie | #1 · +0.000 | Saddiq Bey +0.045 |
| #135 | Daniel Gafford (Daniel Gafford, Saddiq Bey, Jakob Poeltl, Keegan Murray, Santi Aldama) | Daniel Gafford | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #154 | Cam Thomas (Cam Thomas, Jordan Goodwin, Santi Aldama, Bilal Coulibaly, Keon Ellis) | Cam Thomas | #1 · +0.000 | Santi Aldama +0.013 |

Counterfactual rosters (`m63_followcard_grade.json`; 18,000 CRN seasons, the real bracket):

| arm | ECW (rank; next) | favored | title odds (rank) |
|---|---|---|---|
| as drafted (the card's 🎯 at 13 of 13 turns) | 5.169 (rank 1; next 5.121) | 10 of 11 | 23.33% (rank 2) |
| follow-card, self-consistent (arms stage) | 5.169 (rank 1; next 5.121) | 10 of 11 | 23.33% (rank 2) |
| advice at #58: Tyler Herro for Payton Pritchard (the 'now' man; Tyler Herro went #61) | 5.173 (rank 1; next 5.122) | 10 of 11 | 23.71% (rank 2) |
| hindsight single swap Chet Holmgren at #15 | 5.229 (rank 1; next 5.106) | 10 of 11 | 25.74% (rank 1) |
| hindsight single swap OG Anunoby at #39 | 5.209 (rank 1; next 5.031) | 11 of 11 | 25.46% (rank 1) |
| hindsight single swap Tyler Herro at #58 | 5.173 (rank 1; next 5.122) | 10 of 11 | 23.71% (rank 2) |
| hindsight single swap PJ Washington at #87 | 5.174 (rank 1; next 5.099) | 10 of 11 | 23.91% (rank 1) |
| hindsight single swap Saddiq Bey at #111 | 5.191 (rank 1; next 5.120) | 10 of 11 | 24.23% (rank 2) |
| hindsight single swap Saddiq Bey at #130 | 5.214 (rank 1; next 5.112) | 10 of 11 | 24.39% (rank 1) |
| hindsight single swap Santi Aldama at #154 | 5.182 (rank 1; next 5.123) | 10 of 11 | 23.87% (rank 2) |

Advice line (page reading): fired at #58 (Tyler Herro now, Jalen Suggs next turn (92% to survive): +0.012 cats/wk over the pair).

### Mock 64

| pick | deck 🎯 (Top-5) | owner took | card rank · gap (blend) | hindsight best single swap (ΔECW vs final rosters) |
|---|---|---|---|---|
| #10 | Jalen Johnson (Jalen Johnson, Jalen Williams, Kevin Durant, Donovan Mitchell, Anthony Davis) | Jayson Tatum | #18 · +0.045 | Jalen Johnson +0.154 |
| #15 | Jalen Williams (Jalen Williams, Chet Holmgren, Kevin Durant, Derrick White, Evan Mobley) | Kevin Durant | #3 · +0.005 | Chet Holmgren +0.064 |
| #34 | Dyson Daniels (Dyson Daniels, OG Anunoby, Franz Wagner, Kyrie Irving, Onyeka Okongwu) | Bam Adebayo | #11 · +0.040 | Franz Wagner +0.052 |
| #39 | OG Anunoby (OG Anunoby, Franz Wagner, Dyson Daniels, Payton Pritchard, Kyrie Irving) | Kyrie Irving | #5 · +0.012 | Franz Wagner +0.071 |
| #58 | Payton Pritchard (Payton Pritchard, De'Aaron Fox, Jalen Suggs, Zach LaVine, Alperen Sengun) | Payton Pritchard | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #63 | Jalen Suggs (Jalen Suggs, Josh Hart, Isaiah Hartenstein, Mikal Bridges, Rudy Gobert) | Paolo Banchero | #21 · +0.089 | none positive (the pick was hindsight-best) |
| #82 | Isaiah Hartenstein (Isaiah Hartenstein, Day'Ron Sharpe, Myles Turner, Yaxel Lendeborg, Zach LaVine) | Jaden McDaniels | #6 · +0.019 | Isaiah Hartenstein +0.058 |
| #87 | Myles Turner (Myles Turner, Yaxel Lendeborg, Day'Ron Sharpe, Herbert Jones, Cason Wallace) | Jabari Smith Jr. | #13 · +0.044 | Julius Randle +0.017 |
| #106 | PJ Washington (PJ Washington, Yaxel Lendeborg, Sandro Mamukelashvili, Herbert Jones, Cason Wallace) | Herbert Jones | #4 · +0.000 | PJ Washington +0.044 |
| #111 | Yaxel Lendeborg (Yaxel Lendeborg, Sandro Mamukelashvili, Cason Wallace, Collin Gillespie, Devin Vassell) | Collin Gillespie | #4 · +0.009 | Sandro Mamukelashvili +0.041 |
| #130 | Daniel Gafford (Daniel Gafford, Sandro Mamukelashvili, Cason Wallace, Saddiq Bey, Christian Braun) | Daniel Gafford | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #135 | Saddiq Bey (Saddiq Bey, Cason Wallace, Christian Braun, Reed Sheppard, Cam Thomas) | Cason Wallace | #2 · +0.000 | Saddiq Bey +0.037 |
| #154 | Cam Thomas (Cam Thomas, Jordan Goodwin, Santi Aldama, Wendell Carter Jr., Bilal Coulibaly) | Stephon Castle | #80 · +0.426 | Wendell Carter Jr. +0.149 |

Counterfactual rosters (`m64_followcard_grade.json`; 18,000 CRN seasons, the real bracket):

| arm | ECW (rank; next) | favored | title odds (rank) |
|---|---|---|---|
| as drafted (the card's 🎯 at 2 of 13 turns) | 4.555 (rank 3; next 5.357) | 7 of 11 | 7.63% (rank 3) |
| follow-card, self-consistent (arms stage) | 4.987 (rank 2; next 5.255) | 10 of 11 | 18.97% (rank 2) |
| 🎯 at #10: Jalen Johnson for Jayson Tatum (card #18; Jalen Johnson went #11) | 4.708 (rank 2; next 5.356) | 10 of 11 | 10.67% (rank 2) |
| 🎯 at #15: Jalen Williams for Kevin Durant (card #3; Jalen Williams went #25) | 4.536 (rank 4; next 5.304) | 6 of 11 | 7.46% (rank 4) |
| 🎯 at #34: Dyson Daniels for Bam Adebayo (card #11; Dyson Daniels went #40) | 4.546 (rank 4; next 5.358) | 7 of 11 | 7.88% (rank 3) |
| 🎯 at #39: OG Anunoby for Kyrie Irving (card #5; OG Anunoby went #49) | 4.612 (rank 3; next 5.265) | 8 of 11 | 9.17% (rank 3) |
| 🎯 at #63: Jalen Suggs for Paolo Banchero (card #21; Jalen Suggs went #78) | 4.477 (rank 6; next 5.358) | 6 of 11 | 6.56% (rank 8) |
| 🎯 at #82: Isaiah Hartenstein for Jaden McDaniels (card #6; Isaiah Hartenstein went #86) | 4.613 (rank 3; next 5.354) | 9 of 11 | 8.14% (rank 3) |
| 🎯 at #87: Myles Turner for Jabari Smith Jr. (card #13; Myles Turner went #89) | 4.563 (rank 3; next 5.352) | 8 of 11 | 7.83% (rank 3) |
| 🎯 at #106: PJ Washington for Herbert Jones (card #4; PJ Washington went #110) | 4.599 (rank 3; next 5.352) | 7 of 11 | 8.47% (rank 3) |
| 🎯 at #111: Yaxel Lendeborg for Collin Gillespie (card #4; Yaxel Lendeborg went #121) | 4.569 (rank 3; next 5.256) | 8 of 11 | 8.13% (rank 3) |
| 🎯 at #135: Saddiq Bey for Cason Wallace (card #2; Saddiq Bey went #149) | 4.592 (rank 3; next 5.352) | 7 of 11 | 7.97% (rank 3) |
| 🎯 at #154: Cam Thomas for Stephon Castle (card #80; Cam Thomas went #undrafted) | 4.696 (rank 3; next 5.340) | 9 of 11 | 10.73% (rank 3) |
| advice at #15: Kevin Durant for Jalen Williams (the 'now' man; Kevin Durant went #15) | 4.555 (rank 3; next 5.357) | 7 of 11 | 7.63% (rank 3) |
| advice at #34: Franz Wagner for Dyson Daniels (the 'now' man; Franz Wagner went #41) | 4.607 (rank 3; next 5.357) | 8 of 11 | 9.07% (rank 3) |
| advice at #39: Franz Wagner for OG Anunoby (the 'now' man; Franz Wagner went #41) | 4.626 (rank 3; next 5.353) | 9 of 11 | 9.17% (rank 3) |
| advice at #58: Alperen Sengun for Payton Pritchard (the 'now' man; Alperen Sengun went #59) | 4.498 (rank 5; next 5.349) | 7 of 11 | 6.26% (rank 6) |
| the 4 advice 'now' men together (#15 Durant, #34 Wagner, #39 Wagner, #58 Sengun) | 4.562 (rank 3; next 5.351) | 8 of 11 | 7.52% (rank 4) |
| hindsight single swap Jalen Johnson at #10 | 4.708 (rank 2; next 5.356) | 10 of 11 | 10.67% (rank 2) |
| hindsight single swap Chet Holmgren at #15 | 4.619 (rank 3; next 5.338) | 9 of 11 | 9.11% (rank 3) |
| hindsight single swap Franz Wagner at #34 | 4.607 (rank 3; next 5.357) | 8 of 11 | 9.07% (rank 3) |
| hindsight single swap Franz Wagner at #39 | 4.626 (rank 3; next 5.353) | 9 of 11 | 9.17% (rank 3) |
| hindsight single swap Isaiah Hartenstein at #82 | 4.613 (rank 3; next 5.354) | 9 of 11 | 8.14% (rank 3) |
| hindsight single swap Julius Randle at #87 | 4.572 (rank 3; next 5.369) | 7 of 11 | 7.84% (rank 4) |
| hindsight single swap PJ Washington at #106 | 4.599 (rank 3; next 5.352) | 7 of 11 | 8.47% (rank 3) |
| hindsight single swap Sandro Mamukelashvili at #111 | 4.596 (rank 3; next 5.349) | 8 of 11 | 8.38% (rank 3) |
| hindsight single swap Saddiq Bey at #135 | 4.592 (rank 3; next 5.352) | 7 of 11 | 7.97% (rank 3) |
| hindsight single swap Wendell Carter Jr. at #154 | 4.704 (rank 3; next 5.339) | 9 of 11 | 11.07% (rank 3) |

Two of these arms need §2d beside them. The #10 arm (Jalen Johnson for Tatum) is the room's largest single cost and is a real one on any line. The #154 arm (Cam Thomas in for Castle) grades higher only because the arms run on the COMMITTED lines — the pool prices Castle 251st and Thomas's row is his 2024-25 Brooklyn line — which is the projection-plane divergence logged as D-CAST-2, not a reason to draft an unsigned man; both planes now hold him out (D-CAST-1), and on his 2025-26 line he grades 318th.

Advice line (page reading): fired at #15 (Kevin Durant now, Jalen Williams next turn (70% to survive): +0.042 cats/wk over the pair); #34 (Franz Wagner now, OG Anunoby next turn (92% to survive): +0.016 cats/wk over the pair); #39 (Franz Wagner now, OG Anunoby next turn (68% to survive): +0.021 cats/wk over the pair); #58 (Alperen Sengun now, Payton Pritchard next turn (77% to survive): +0.052 cats/wk over the pair).

### Mock 65

| pick | deck 🎯 (Top-5) | owner took | card rank · gap (blend) | hindsight best single swap (ΔECW vs final rosters) |
|---|---|---|---|---|
| #10 | Jalen Johnson (Jalen Johnson, Jalen Williams, Kevin Durant, Donovan Mitchell, Anthony Davis) | Jalen Johnson | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #15 | Jamal Murray (Jamal Murray, Jalen Williams, Derrick White, Desmond Bane, James Harden) | Jamal Murray | #1 · +0.000 | Chet Holmgren +0.117 |
| #34 | Derrick White (Derrick White, OG Anunoby, Desmond Bane, Jaren Jackson Jr., Franz Wagner) | Derrick White | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #39 | OG Anunoby (OG Anunoby, Franz Wagner, Jaren Jackson Jr., Dyson Daniels, Cameron Boozer) | OG Anunoby | #1 · +0.000 | Franz Wagner +0.031 |
| #58 | Payton Pritchard (Payton Pritchard, De'Aaron Fox, Coby White, Zach LaVine, Mikal Bridges) | Payton Pritchard | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #63 | Mikal Bridges (Mikal Bridges, Isaiah Hartenstein, Josh Hart, Rudy Gobert, Jalen Suggs) | Mikal Bridges | #1 · +0.000 | Rudy Gobert +0.028 |
| #82 | Isaiah Hartenstein (Isaiah Hartenstein, Yaxel Lendeborg, Day'Ron Sharpe, Herbert Jones, Cason Wallace) | Isaiah Hartenstein | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #87 | Yaxel Lendeborg (Yaxel Lendeborg, Sandro Mamukelashvili, PJ Washington, Cason Wallace, Myles Turner) | Yaxel Lendeborg | #1 · +0.000 | Daniel Gafford +0.020 |
| #106 | PJ Washington (PJ Washington, Sandro Mamukelashvili, Devin Vassell, Herbert Jones, Saddiq Bey) | PJ Washington | #1 · +0.000 | Daniel Gafford +0.018 |
| #111 | Sandro Mamukelashvili (Sandro Mamukelashvili, Devin Vassell, Herbert Jones, Saddiq Bey, Collin Gillespie) | Sandro Mamukelashvili | #1 · +0.000 | Daniel Gafford +0.054 |
| #130 | Collin Gillespie (Collin Gillespie, Saddiq Bey, Reed Sheppard, Christian Braun, Cam Thomas) | Collin Gillespie | #1 · +0.000 | Daniel Gafford +0.039 |
| #135 | Saddiq Bey (Saddiq Bey, Daniel Gafford, Christian Braun, Cam Thomas, Reed Sheppard) | Saddiq Bey | #1 · +0.000 | Daniel Gafford +0.041 |
| #154 | Cam Thomas (Cam Thomas, Jordan Goodwin, Santi Aldama, Bilal Coulibaly, Keon Ellis) | Cam Thomas | #1 · +0.000 | none positive (the pick was hindsight-best) |

Counterfactual rosters (`m65_followcard_grade.json`; 18,000 CRN seasons, the real bracket):

| arm | ECW (rank; next) | favored | title odds (rank) |
|---|---|---|---|
| as drafted (the card's 🎯 at 13 of 13 turns) | 5.174 (rank 1; next 5.099) | 10 of 11 | 23.19% (rank 2) |
| follow-card, self-consistent (arms stage) | 5.174 (rank 1; next 5.099) | 10 of 11 | 23.19% (rank 2) |
| advice at #39: Franz Wagner for OG Anunoby (the 'now' man; Franz Wagner went #44) | 5.204 (rank 1; next 5.102) | 10 of 11 | 24.59% (rank 1) |
| hindsight single swap Chet Holmgren at #15 | 5.290 (rank 1; next 5.091) | 11 of 11 | 27.87% (rank 1) |
| hindsight single swap Franz Wagner at #39 | 5.204 (rank 1; next 5.102) | 10 of 11 | 24.59% (rank 1) |
| hindsight single swap Rudy Gobert at #63 | 5.202 (rank 1; next 5.169) | 11 of 11 | 24.92% (rank 2) |
| hindsight single swap Daniel Gafford at #87 | 5.194 (rank 1; next 5.093) | 10 of 11 | 23.82% (rank 2) |
| hindsight single swap Daniel Gafford at #106 | 5.192 (rank 1; next 5.090) | 10 of 11 | 23.95% (rank 2) |
| hindsight single swap Daniel Gafford at #111 | 5.228 (rank 1; next 5.086) | 11 of 11 | 25.09% (rank 1) |
| hindsight single swap Daniel Gafford at #130 | 5.213 (rank 1; next 5.085) | 11 of 11 | 24.98% (rank 1) |
| hindsight single swap Daniel Gafford at #135 | 5.214 (rank 1; next 5.086) | 11 of 11 | 25.27% (rank 1) |

Advice line (page reading): fired at #39 (Franz Wagner now, OG Anunoby next turn (68% to survive): +0.017 cats/wk over the pair).

Cast fidelity, each room (`m6x_cast_fidelity.json`; the same readout as mock 62):

**Mock 63.**

| seat | manager | profile lean (market / value) | mean market rank minus pick | mean value rank minus pick | guards / centers | loyalty names on the board | taken by them |
|---|---|---|---|---|---|---|---|
| 1 | Oblena | 0.35 / 0.65 | +4.6 | -12.0 | 4 / 6 | Donovan Mitchell (seat 11) | 0 of 1 |
| 2 | Noah | 0.75 / 0.25 | -18.5 | +20.9 | 4 / 5 | LaMelo Ball (seat 2) | 1 of 1 |
| 3 | Will | 0.55 / 0.45 | -10.2 | +9.3 | 6 / 5 | Onyeka Okongwu (seat 10), Jaden Ivey (undrafted) | 0 of 1 |
| 4 | Robby | 0.70 / 0.30 | -14.8 | +22.3 | 7 / 3 | Jarrett Allen (seat 4), Collin Sexton (seat 4), Devin Booker (seat 4), Devin Vassell (seat 7) | 3 of 4 |
| 5 | Kyle | 0.45 / 0.55 | -3.6 | +2.3 | 5 / 4 | none | 0 of 0 |
| 6 | Martin | 0.45 / 0.55 | -0.3 | +2.8 | 5 / 5 | Luka Doncic (seat 4), Brandon Ingram (seat 12), Jalen Suggs (seat 6) | 1 of 3 |
| 7 | John | 0.50 / 0.50 | -5.3 | +6.0 | 9 / 3 | Tyrese Maxey (seat 7), Jakob Poeltl (seat 1), Jeremy Sochan (undrafted) | 1 of 2 |
| 8 | JCo | 0.45 / 0.55 | -2.4 | -0.7 | 6 / 4 | Tyrese Haliburton (seat 8), Jimmy Butler (undrafted), Nic Claxton (seat 8) | 2 of 2 |
| 9 | Kevin | 0.45 / 0.55 | -1.9 | +2.1 | 8 / 4 | Pascal Siakam (seat 9) | 1 of 1 |
| 10 | David | owner | +11.9 | -16.4 | 7 / 4 | none | — |
| 11 | Cayas | 0.40 / 0.60 | -1.0 | +1.9 | 8 / 3 | none | 0 of 0 |
| 12 | Hegi | 0.65 / 0.35 | -7.0 | +10.5 | 7 / 4 | Immanuel Quickley (seat 12), Andrew Wiggins (seat 3) | 1 of 2 |

loyalty fired on 10 of the 17 loyalty names that were drafted by anyone (undrafted names excluded)

**Mock 64.**

| seat | manager | profile lean (market / value) | mean market rank minus pick | mean value rank minus pick | guards / centers | loyalty names on the board | taken by them |
|---|---|---|---|---|---|---|---|
| 1 | Oblena | 0.35 / 0.65 | +4.5 | -13.5 | 6 / 3 | Donovan Mitchell (seat 12) | 0 of 1 |
| 2 | Noah | 0.75 / 0.25 | -14.7 | +21.8 | 4 / 5 | LaMelo Ball (seat 2) | 1 of 1 |
| 3 | Will | 0.55 / 0.45 | -8.6 | +14.5 | 5 / 6 | Onyeka Okongwu (seat 6), Jaden Ivey (undrafted) | 0 of 1 |
| 4 | Robby | 0.70 / 0.30 | -12.2 | +21.8 | 9 / 2 | Jarrett Allen (seat 4), Collin Sexton (seat 4), Devin Booker (seat 4), Devin Vassell (seat 6) | 3 of 4 |
| 5 | Kyle | 0.45 / 0.55 | -2.4 | +1.7 | 7 / 4 | none | 0 of 0 |
| 6 | Martin | 0.45 / 0.55 | +0.9 | -1.3 | 8 / 4 | Luka Doncic (seat 4), Brandon Ingram (seat 2), Jalen Suggs (seat 6) | 1 of 3 |
| 7 | John | 0.50 / 0.50 | -8.4 | +8.6 | 6 / 3 | Tyrese Maxey (seat 6), Jakob Poeltl (seat 7), Jeremy Sochan (undrafted) | 1 of 2 |
| 8 | JCo | 0.45 / 0.55 | -0.3 | -5.2 | 3 / 5 | Tyrese Haliburton (seat 8), Jimmy Butler (undrafted), Nic Claxton (seat 8) | 2 of 2 |
| 9 | Kevin | 0.45 / 0.55 | +0.9 | -1.3 | 9 / 4 | Pascal Siakam (seat 9) | 1 of 1 |
| 10 | David | owner | -5.1 | +0.7 | 7 / 3 | none | — |
| 11 | Cayas | 0.40 / 0.60 | +1.1 | -5.2 | 7 / 5 | none | 0 of 0 |
| 12 | Hegi | 0.65 / 0.35 | -7.4 | +15.5 | 7 / 4 | Immanuel Quickley (seat 12), Andrew Wiggins (seat 12) | 2 of 2 |

loyalty fired on 11 of the 17 loyalty names that were drafted by anyone (undrafted names excluded)

**Mock 65.**

| seat | manager | profile lean (market / value) | mean market rank minus pick | mean value rank minus pick | guards / centers | loyalty names on the board | taken by them |
|---|---|---|---|---|---|---|---|
| 1 | Oblena | 0.35 / 0.65 | +1.4 | -11.3 | 5 / 3 | Donovan Mitchell (seat 11) | 0 of 1 |
| 2 | Noah | 0.75 / 0.25 | -18.0 | +23.8 | 6 / 5 | LaMelo Ball (seat 2) | 1 of 1 |
| 3 | Will | 0.55 / 0.45 | -5.0 | +11.7 | 3 / 7 | Onyeka Okongwu (seat 11), Jaden Ivey (undrafted) | 0 of 1 |
| 4 | Robby | 0.70 / 0.30 | -14.2 | +24.0 | 6 / 3 | Jarrett Allen (seat 4), Collin Sexton (seat 4), Devin Booker (seat 4), Devin Vassell (seat 6) | 3 of 4 |
| 5 | Kyle | 0.45 / 0.55 | -4.8 | +7.8 | 7 / 3 | none | 0 of 0 |
| 6 | Martin | 0.45 / 0.55 | -3.0 | -1.2 | 6 / 4 | Luka Doncic (seat 3), Brandon Ingram (seat 6), Jalen Suggs (seat 6) | 2 of 3 |
| 7 | John | 0.50 / 0.50 | -5.6 | +5.2 | 7 / 5 | Tyrese Maxey (seat 6), Jakob Poeltl (seat 7), Jeremy Sochan (undrafted) | 1 of 2 |
| 8 | JCo | 0.45 / 0.55 | -3.2 | -1.1 | 6 / 5 | Tyrese Haliburton (seat 8), Jimmy Butler (undrafted), Nic Claxton (seat 8) | 2 of 2 |
| 9 | Kevin | 0.45 / 0.55 | -1.2 | -8.8 | 9 / 4 | Pascal Siakam (seat 9) | 1 of 1 |
| 10 | David | owner | +11.3 | -14.9 | 5 / 3 | none | — |
| 11 | Cayas | 0.40 / 0.60 | +0.8 | +0.6 | 8 / 5 | none | 0 of 0 |
| 12 | Hegi | 0.65 / 0.35 | -7.4 | +17.1 | 7 / 3 | Immanuel Quickley (seat 12), Andrew Wiggins (seat 12) | 2 of 2 |

loyalty fired on 12 of the 17 loyalty names that were drafted by anyone (undrafted names excluded)

Target-wait with the three rooms added (`target_wait_2026-10-07c.json`, 10 rooms): deep (mkt − pick ≥ 24) — 🎯s passed on 17, still there at the next owner turn 9, at the turn after 3 of 15; mid (12–23) — 🎯s passed on 6, still there at the next owner turn 2, at the turn after 1 of 5; near (< 12) — 🎯s passed on 12, still there at the next owner turn 5, at the turn after 0 of 11. In mocks 63 and 65 no 🎯 was passed; in mock 64 the #10 🎯 (Jalen Johnson, +1 on the market) went at #11.

## 5. Hashtag 10/6 projections page — parsed, pinned, compared

`FBall_10.6.pdf` (Hashtag Basketball projections, updated 06 Oct 2026; the projections page alone — no ADP page in this upload) read with pdfplumber to `report/market/hashtag-raw-2026-10-06.txt`, parsed by `hashtag_pdf_market.py` (patched to accept a projections-only upload) to `hashtag-2026-10-06.csv` (200 rows) and `unmatched-hashtag-2026-10-06.md`, registered in `check_derived.py` and pinned at `d8a2c0d`; the derived gate reproduces all 17 dated artifacts. Join: 199 of 200 rows have a pool row; the one Hashtag-only name is Yanic Konan Niederhauser (LAC, rank 181). Against the 9/30 page: 198 names on both; new on 10/6 — Isaiah Jackson, Jalen Smith; dropped — Jerami Grant, Shaedon Sharpe; 10 names moved ten or more places: Jimmy Butler III 59→75; Damian Lillard 57→72; Scotty Pippen Jr. 177→191; Max Strus 180→194; Kristaps Porzingis 84→96; Dejounte Murray 30→42; Brandon Ingram 70→82; Yanic Konan Niederhauser 170→181; Bradley Beal 166→176; Rui Hachimura 192→182.

| player | Hashtag 9/30 | Hashtag 10/6 | Yahoo ADP 10/6 | kit board (v48 regeneration) |
|---|---|---|---|---|
| Saddiq Bey | 132 | 132 | 119.9 | 101 |
| Stephon Castle | 152 | 151 | 53.8 | 98 |
| RJ Barrett | 153 | 153 | 112.4 | — |
| Davion Mitchell | 172 | 172 | 117.6 | 180 |
| Rui Hachimura | 192 | 182 | 117.9 | 164 |
| Dillon Brooks | 174 | 174 | 113.7 | — |
| Yaxel Lendeborg | 121 | 121 | 115.7 | 81 |
| Cam Thomas | — | — | — | held off |
| Jordan Goodwin | — | — | — | 108 |
| Keon Ellis | — | — | — | 132 |

## 6. Gates

| gate | result |
|---|---|
| deck build (gates 1–7) | safe to publish; gate 7 waivers ×3 (D-CAST-1, the same decision on both planes), team 0, exclusion 0, drift 0, propagation 0; 171 shared rows carry a differing stat line (WARNING, the standing WO-5 divergence; unchanged) |
| roster lock | direct-complete, 334 of 335 rows on an official roster (Broome allowed, signed by Milwaukee 10/6 per NBA.com, RotoWire, Hoops Rumors; not on ESPN's feed at the 10/7 check) |
| scripts/check_parity.py | EXACT MATCH — 286 owner turns across 22 committed states (the three new rooms included), 335 pool rows, 3015 z-score cells, 319 market ranks (241 priced), survival and clock reads bit-identical |
| scripts/test_card.py | 95 of 95 (six D-CAST-4 cases added; 5 of 95 failed on the unchanged engine, all pass after) |
| scripts/test_gates.py / test_draft.py | 37 of 37 / 65 of 65 |
| arena/mocks/full_dom_check.mjs (state 54) | 130/130 assertions, no page errors (`full_dom_check_2026-10-07_v48.json`) |
| full_dom_check.mjs on mock 63's state (informational) | 130/130, pass True |
| D-CAST-3 experiment | ran at N=30 as pre-registered; no variant ships (§3c) |
| kit rank_engine.py | board regenerated, 321 projected after 4 unsigned held; provenance gate PASS |
| kit check_derived.py | 17 of 17 dated artifacts reproduce from their pinned inputs (the 10/6 Hashtag artifact pinned at d8a2c0d) |
| kit check_provenance.py | PASS — all rows sourced, verified 2026-07-13 .. 2026-10-07 |
| kit check_report.py / deck judgment_open_items.py --check-report | PASS on this file (run after it was written; the PR records the run) |

## Watchlist

- The four unsigned rows: a signing reported by two outlets re-derives the row on both planes (team, role, line) and lifts the tag; until then they are off every board.
- WO-5 (after two preseason games per team): Castle and Barrett first (D-CAST-2), then the 25 Rotoworld divergences (D-RW-1) and the Hashtag 10/6 rows where the kit sits 25+ places away.
- The survival chips against the cast: optimistic in all four cast rooms (predicted above realized each time); still logged, not refit (D62-2 default).
- The round-11+ card rule is measured on four rooms; the first live human room on v48 is its out-of-sample test.

## Open-item receipts

| item | query run (2026-10-07) | dated finding |
|---|---|---|
| (this analysis) | machine replay, Basketball-Reference player pages for the six named men (read 2026-10-07), the Hashtag PDF; no other web research | pull receipts for the window live in `after-report-2026-10-07.md` (the morning's pull, same day) |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (after-report-2026-10-07.md, ten receipts dated 10/7) | all HELD or unsigned on 2026-10-07; Thomas, Ivey, Ball and Dillingham re-tagged out-unsigned today by D-CAST-1 (the receipts named Spotrac, the NBC Sports free-agent list, the ESPN player page, RotoBaller, Saturday Down South and the Basketball-Reference ledger); the other six unchanged |

## Bounds

- The grades are on the committed lines (v44 pool + the 10/6 prices); the WO-5 refresh will move them.
- A MOCK has no second record: the exported board is the engine's own output, so §4 grades the engine against itself at every opponent turn; only the owner's picks are an outside input.
- The bot replay in §2b removes the noise term, so it explains the formula, not the particular pick each seat made.
- The last-season ranks in §2d standardize a 2025-26 line against a pool of 2026-27 projections — a like-for-like production comparison between the six, not a projection.
- D-CAST-3's human reference is ten rooms from one seat; its M1 counts only players drafted in at least five of them.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-CAST-1 | Applied: unsigned free agents (Thomas, Ivey, Ball, Dillingham; Konchar on the kit — unsigned per Spotrac and the NBC Sports free-agent list, 2026-10-07) are off every board on both planes until two outlets report a signing. Keep the rule as a standing pool rule for any future unsigned row? | yes |
| D-CAST-2 | Castle and Barrett (and any committed line that sits 60+ places below its 2025-26 production on the deck) re-derived first at WO-5 with the two-outlet role rule, both planes, board diffed. Confirm the order of work? | yes |
| D-CAST-3 | The N=30 run: no variant passes the pre-registered rule (V2 wins M1 and M2 but fails the M3 personality guard, Spearman 0.30; V1 and V3 do not improve M2). Keep the shipped bots, and pre-register a round-7+ XRank value axis as the next variant? | yes — the bots stay; the follow-up is pre-registered before any run |
| D-CAST-4 | Applied: from round 11 the card's candidates are the priced rows (CARD_PRICED_FROM = 11; whole pool returns under five priced rows). Keep 11, or move the boundary (9 or 10 would also change the §2c rounds-11/12 rows by one name each)? | keep 11 |
| D-C64-1 | Mock 64 drafted like a human (Tatum #10, Castle #154) grades 7.63 percent against 18.97 for the card chain from the same seat; the human-style picks cost most at #10 and #154. Keep logging deliberate off-card rooms as a calibration series? | yes |
| D62-1..3, D61-1..4, D60-1..4, D-1007-1, D-1006-1..4, D-1005-1/3/4, D-Y1..4, D-RW-1..4 | carried | carried |

## Provenance

- Inputs: the owner's three exported draft states (uploaded 2026-10-07), copied verbatim to `arena/data/states/draft_state_63/64/65.json`; the owner's `FBall_10.6.pdf`; Basketball-Reference player pages for Thomas, Bey, Castle, Mitchell, Barrett, Hachimura (read 2026-10-07; the raw tables kept in the session scratchpad and the parsed lines in the deck's `arena/results/dcast_lastseason_2026-10-07.json`).
- Every room figure is read from `arena/results/m63_*.json`, `m64_*.json`, `m65_*.json` (replay, final, hindsight, forecast, arms, pairarms, deckcard, advisor, survival, cast_fidelity, followcard_grade, advice_reads, repeat_names_audit) and `target_wait_2026-10-07.json`; the arms use 18,000 CRN seasons (seeds 11/23/47) on the real eight-team bracket; the deck card and the audit ran the v47 page's own engine under node.
- The defense: `arena/results/dcast_botdiag_m63_2026-10-07.json` (noise-free replay), `dcast_realism_picks_2026-10-07.json` (draft positions by room), `dcast_lastseason_2026-10-07.json`, `dcast_card_effect_v48.json` (§2c); the experiment: `arena/results/castsim_design_2026-10-07.md` and `castsim_n30_2026-10-07.json`.
- Kit: `report/market/hashtag-2026-10-06.csv` and `unmatched-hashtag-2026-10-06.md` (pinned `d8a2c0d`), the board diff in this report computed from the regenerated `top-200-2026-27.md` against the morning's.
- Not verified by web research: nothing in this report rests on a search summary; the signing status of the four unsigned men is the morning's receipts plus Spotrac read directly.

## In plain language

**What you asked.** Whether the late picks the card and the practice rooms were producing — Cam Thomas, Saddiq Bey — are believable when Castle, Mitchell, Barrett, Hachimura and Wagler are still on the board, and whether last season's numbers back your instinct.

**What the record says.** You are right about Thomas and about the three guards, and the record is unanimous: every one of your ten human rooms drafted Castle (62nd to 84th), Mitchell and Barrett, and the eleven bots never did; nobody human has ever drafted Thomas, and the three times he went in a practice room it was the card at #154. You are not right about Bey: humans take him in eight of ten rooms around 140, both Yahoo and Hashtag price him there, and last season he out-produced all three guards in 9-cat by a wide margin (85th against 164th–175th). Thomas on last season's numbers was 318th.

**Why it happened.** Three separate things. Thomas was sitting in the pool on his old Brooklyn line with full availability even though he has no team — a data problem. The late card never looked at prices, so once the priced men who fit your roster were gone, men no market lists could top it — a card problem. And the lines the pool carries for Castle and Barrett are harsher than what they did last year, which drags them down for both the card's value half and the bots' value half — a projection problem.

**What was done.** Each got its own fix. Unsigned free agents are now off every board on both planes until two outlets say they signed (Thomas, Ivey, Ball, Dillingham). From round 11 the card only considers men Yahoo prices; it was tested red-first, every suite and the parity check pass, and on the four practice rooms it changes the round-13 card completely and rounds 11–12 by at most one name. The bots were put through the pre-registered 30-room experiment: nothing shipped. The one variant that drafted like the humans (Yahoo's own ranks as the bots' value axis) also erased the eleven personalities in the early rounds, which the pre-registered guard forbids, so the bots stay as they are; a version that uses Yahoo's ranks only from round 7 is the next thing to test, and it will be written down before it is run. Castle's and Barrett's lines go to the projection refresh (WO-5) to be rebuilt from last season's per-36 with sourced roles — not bent to fit a draft slot today. Hashtag's new page is parsed and on file; it agrees with Yahoo and with your rooms.

**The three rooms.** Mocks 63 and 65, where you took the card's name every time, grade 23.3 and 23.2 percent on the real bracket (both second of twelve). Mock 64, where you drafted like a human would, grades 7.6 percent against 19.0 for the card from the same seat; the two expensive turns were Tatum over Jalen Johnson at #10 and Castle at #154, and the two cheap ones were Durant at #15 and Wallace at #135, which cost almost nothing.

**Your decisions.** D-CAST-1 keep the unsigned rule standing (default yes). D-CAST-2 Castle and Barrett first at WO-5 (default yes). D-CAST-3 the bot experiment's verdict (see the sheet). D-CAST-4 keep the round-11 boundary (default keep). D-C64-1 keep logging deliberate off-card rooms (default yes). Everything earlier is carried.
