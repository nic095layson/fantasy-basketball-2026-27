# After-report — draft_66: the first MOCK on v49 — the round-11 card rule, the new bots and the Castle/Barrett lines in one room

**Owner request (2026-10-07 evening):** an exported draft state (`draft_state_55.json`) uploaded without comment after the fixes shipped — graded as mock 66, the standing practice-room protocol.

**Room:** the deck's own MOCK mode, 12 × 13, owner seat 10, the eleven opponents the E18 behavioral models of the real league-mates in the league's real order (1 Oblena, 2 Noah, 3 Will, 4 Robby, 5 Kyle, 6 Martin, 7 John, 8 JCo, 9 Kevin, 11 Cayas, 12 Hegi). Not a public room: LEDGER-eligible. **Deck used:** v49 (rev `269c522`; the first build carrying the round-11 priced-only card, the bots' round-7+ XRank value axis and the re-derived Castle/Barrett lines; the four unsigned men excluded; Porziņģis veto live) — the state's `cast` field and the per-turn card echo identify it. **Method:** the state is the deck's own export (no Yahoo recap and no tool log exist for a MOCK), checked snake-consistent with every name in the pool; the grade is the deck plane's machine-derived retro (`arena/results/m66_*.json`; deck card replayed from the v49 page; title odds on the league's real eight-team bracket). Every figure below is read from those files. Verification: this file passes `report/check_report.py` and the deck's `judgment_open_items.py --check-report`.

Pull window: 2026-10-07 → 2026-10-07 (analysis only, the fourth report of the day; no roster pull).

**Headline.** As drafted **20.16 percent** on the real bracket (rank 1 of 12), expected weekly category wins 5.013, rank 1 of 12 (next 4.887), favored in 11 of 11 head-to-heads; the card's 🎯 taken at 5 of 13 turns, a Top-5 row at 6 of 13; the self-consistent follow-card chain from the same seat grades 34.93 percent. The three fixes behaved as built: the late card carried 0 unpriced rows in rounds 11–13; the cast drafted Castle (#78, Martin), Barrett (#112, Kevin), Hachimura (#121), Brooks (#133) and Mitchell (#137) — all five inside or near the human ranges on file — and none of the four unsigned men appeared anywhere. Saddiq Bey went undrafted (watchlist).

## 1. Roster changes

None — a MOCK room; no pull, no row moved on either plane.

## 2. The team, replayed

| arm | ECW (rank; next) | favored | title odds (rank) |
|---|---|---|---|
| as drafted (the card's 🎯 at 5 of 13 turns) | 5.013 (rank 1; next 4.887) | 11 of 11 | 20.16% (rank 1) |
| follow-card, self-consistent (arms stage) | 5.507 (rank 1; next 4.894) | 11 of 11 | 34.93% (rank 1) |
| 🎯 at #10: Jalen Johnson for Giannis Antetokounmpo (card #17; Jalen Johnson went #11) | 5.055 (rank 1; next 4.893) | 10 of 11 | 22.24% (rank 1) |
| 🎯 at #15: Derrick White for Scottie Barnes (card #25; Derrick White went #35) | 4.990 (rank 1; next 4.909) | 9 of 11 | 19.10% (rank 1) |
| 🎯 at #34: Dyson Daniels for Trae Young (card #16; Dyson Daniels went #39) | 5.013 (rank 1; next 4.887) | 11 of 11 | 20.16% (rank 1) |
| 🎯 at #39: OG Anunoby for Dyson Daniels (card #4; OG Anunoby went #51) | 5.027 (rank 1; next 4.887) | 11 of 11 | 19.75% (rank 1) |
| 🎯 at #63: Zach LaVine for Paolo Banchero (card #13; Zach LaVine went #67) | 4.949 (rank 1; next 4.898) | 9 of 11 | 18.35% (rank 1) |
| 🎯 at #82: Coby White for VJ Edgecombe (card #19; Coby White went #87) | 5.013 (rank 1; next 4.887) | 11 of 11 | 20.16% (rank 1) |
| 🎯 at #106: PJ Washington for Jalen Green (card #16; PJ Washington went #111) | 5.013 (rank 1; next 4.887) | 11 of 11 | 20.16% (rank 1) |
| 🎯 at #135: Daniel Gafford for Fred VanVleet (card #19; Daniel Gafford went #154) | 5.013 (rank 1; next 4.887) | 11 of 11 | 20.16% (rank 1) |
| advice at #34: Derrick White for Dyson Daniels (the 'now' man; Derrick White went #35) | 5.236 (rank 1; next 4.893) | 11 of 11 | 26.63% (rank 1) |
| advice at #39: Onyeka Okongwu for OG Anunoby (the 'now' man; Onyeka Okongwu went #43) | 5.041 (rank 1; next 4.894) | 11 of 11 | 20.03% (rank 1) |
| advice at #63: Kel'el Ware for Zach LaVine (the 'now' man; Kel'el Ware went #81) | 4.995 (rank 1; next 4.882) | 11 of 11 | 18.87% (rank 1) |
| the 3 advice 'now' men together (#34 White, #39 Okongwu, #63 Ware) | 5.124 (rank 1; next 4.894) | 11 of 11 | 22.21% (rank 1) |
| hindsight single swap Chet Holmgren at #10 | 5.086 (rank 1; next 4.894) | 11 of 11 | 22.74% (rank 1) |
| hindsight single swap Chet Holmgren at #15 | 5.194 (rank 1; next 4.890) | 11 of 11 | 25.88% (rank 1) |
| hindsight single swap Derrick White at #34 | 5.236 (rank 1; next 4.893) | 11 of 11 | 26.63% (rank 1) |
| hindsight single swap Onyeka Okongwu at #39 | 5.041 (rank 1; next 4.894) | 11 of 11 | 20.03% (rank 1) |
| hindsight single swap Myles Turner at #63 | 5.017 (rank 1; next 4.892) | 11 of 11 | 20.01% (rank 1) |
| hindsight single swap Myles Turner at #82 | 5.150 (rank 1; next 4.874) | 11 of 11 | 24.26% (rank 1) |
| hindsight single swap Myles Turner at #87 | 5.058 (rank 1; next 4.879) | 11 of 11 | 21.73% (rank 1) |
| hindsight single swap Sandro Mamukelashvili at #106 | 5.060 (rank 1; next 4.894) | 11 of 11 | 21.31% (rank 1) |
| hindsight single swap Sandro Mamukelashvili at #130 | 5.020 (rank 1; next 4.893) | 11 of 11 | 20.76% (rank 1) |
| hindsight single swap Sandro Mamukelashvili at #135 | 5.155 (rank 1; next 4.874) | 11 of 11 | 24.65% (rank 1) |

Category ranks (weekly model): FG% 11 · FT% 12 · 3PTM 3 · PTS 1 · REB 7 · AST 1 · ST 1 · BLK 7 · TO 12.

## 3. Pick by pick — card vs owner vs hindsight

| pick | deck 🎯 (Top-5) | owner took | card rank · gap (blend) | hindsight best single swap (ΔECW vs final rosters) |
|---|---|---|---|---|
| #10 | Jalen Johnson (Jalen Johnson, Jalen Williams, Kevin Durant, Donovan Mitchell, Anthony Davis) | Giannis Antetokounmpo | #17 · +0.047 | Chet Holmgren +0.073 |
| #15 | Derrick White (Derrick White, Jamal Murray, Jalen Williams, Stephen Curry, James Harden) | Scottie Barnes | #25 · +0.073 | Chet Holmgren +0.181 |
| #34 | Dyson Daniels (Dyson Daniels, Derrick White, OG Anunoby, Franz Wagner, Desmond Bane) | Trae Young | #16 · +0.065 | Derrick White +0.224 |
| #39 | OG Anunoby (OG Anunoby, Desmond Bane, Payton Pritchard, Dyson Daniels, Onyeka Okongwu) | Dyson Daniels | #4 · +0.009 | Onyeka Okongwu +0.028 |
| #58 | Payton Pritchard (Payton Pritchard, Zach LaVine, De'Aaron Fox, Rudy Gobert, Isaiah Hartenstein) | Payton Pritchard | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #63 | Zach LaVine (Zach LaVine, Coby White, Jalen Suggs, Mikal Bridges, Kel'el Ware) | Paolo Banchero | #13 · +0.071 | Myles Turner +0.004 |
| #82 | Coby White (Coby White, Jalen Suggs, Isaiah Hartenstein, Sandro Mamukelashvili, Myles Turner) | VJ Edgecombe | #19 · +0.102 | Myles Turner +0.138 |
| #87 | Coby White (Coby White, Jalen Suggs, Sandro Mamukelashvili, Myles Turner, PJ Washington) | Coby White | #1 · +0.000 | Myles Turner +0.045 |
| #106 | PJ Washington (PJ Washington, Sandro Mamukelashvili, Daniel Gafford, Yaxel Lendeborg, Saddiq Bey) | Jalen Green | #16 · +0.075 | Sandro Mamukelashvili +0.047 |
| #111 | PJ Washington (PJ Washington, Yaxel Lendeborg, Daniel Gafford, Sandro Mamukelashvili, Aaron Gordon) | PJ Washington | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #130 | Yaxel Lendeborg (Yaxel Lendeborg, Daniel Gafford, Sandro Mamukelashvili, Devin Vassell, Saddiq Bey) | Yaxel Lendeborg | #1 · +0.000 | Sandro Mamukelashvili +0.008 |
| #135 | Daniel Gafford (Daniel Gafford, Sandro Mamukelashvili, Kyle Filipowski, Saddiq Bey, Nikola Vucevic) | Fred VanVleet | #19 · +0.165 | Sandro Mamukelashvili +0.142 |
| #154 | Daniel Gafford (Daniel Gafford, Kyle Filipowski, Nikola Vucevic, Saddiq Bey, Herbert Jones) | Daniel Gafford | #1 · +0.000 | none positive (the pick was hindsight-best) |

Advice line (page reading): fired at #34 (Derrick White now, Desmond Bane next turn (81% to survive): +0.143 cats/wk over the pair); #39 (Onyeka Okongwu now, Payton Pritchard next turn (83% to survive): +0.021 cats/wk over the pair); #63 (Kel'el Ware now, Zach LaVine next turn (74% to survive): +0.064 cats/wk over the pair).

## 4. The fixes, out of sample

| player | human rooms (of 10) and range | this room | rule in play |
|---|---|---|---|
| Stephon Castle | 10 · 62–84 | #78 (Martin) | V4 bots + re-derived line |
| RJ Barrett | 10 · 117–140 | #112 (Kevin) | V4 bots + re-derived line |
| Davion Mitchell | 10 · 102–129 | #137 (JCo) | V4 bots |
| Rui Hachimura | 3 · 123–129 | #121 (Oblena) | V4 bots |
| Dillon Brooks | 8 · 120–153 | #133 (Hegi) | V4 bots |
| Saddiq Bey | 8 · 136–149 | undrafted | priced; on the value axis only |
| Cam Thomas | 0 · — | undrafted | D-CAST-1 (unsigned, excluded) |
| Keaton Wagler | 1 · 153–153 | undrafted | V4 bots |

Late card: 0 unpriced rows across the owner's three turns in rounds 11–13 (the v49 rule). Repeat-name audit (`m66_repeat_names_audit.json`): the #1 changes at 12 of 13 turns under other rooms' rosters (7 of 13 against an empty roster); Gafford on the Top-5 at 5, Braun 0, Poeltl 0.

## 5. Survival chips and the cast

Survival (`m66_survival.json`): this room 55 rows, predicted 0.551 vs realized 0.691, Brier 0.218; BUY NOW 3 of 6 survived, TOSS-UP 7 of 11, quiet 28 of 38. Pooled 51–66: 807 rows, Brier 0.251. (Corrected 2026-10-07 with the deck-card replayer's cardPool fix found grading mock 67 — the first write-up read 0.673 / 0.205 / 2 of 6 and card #24 at #135; see after-report-2026-10-07-draft67.md §10.)

| seat | manager | profile lean (market / value) | mean market rank minus pick | mean value rank minus pick | guards / centers | loyalty names on the board | taken by them |
|---|---|---|---|---|---|---|---|
| 1 | Oblena | 0.35 / 0.65 | -2.6 | +10.0 | 7 / 5 | Donovan Mitchell (seat 12) | 0 of 1 |
| 2 | Noah | 0.75 / 0.25 | -10.7 | +26.4 | 4 / 7 | LaMelo Ball (seat 2) | 1 of 1 |
| 3 | Will | 0.55 / 0.45 | -4.8 | +7.6 | 6 / 4 | Onyeka Okongwu (seat 6), Jaden Ivey (undrafted) | 0 of 1 |
| 4 | Robby | 0.70 / 0.30 | -8.7 | +15.5 | 7 / 3 | Jarrett Allen (seat 4), Collin Sexton (undrafted), Devin Booker (seat 4), Devin Vassell (seat 4) | 3 of 3 |
| 5 | Kyle | 0.45 / 0.55 | -2.8 | -5.2 | 3 / 4 | none | 0 of 0 |
| 6 | Martin | 0.45 / 0.55 | +0.3 | +11.2 | 7 / 4 | Luka Doncic (seat 4), Brandon Ingram (seat 3), Jalen Suggs (seat 6) | 1 of 3 |
| 7 | John | 0.50 / 0.50 | -4.0 | +19.8 | 6 / 2 | Tyrese Maxey (seat 6), Jakob Poeltl (seat 7), Jeremy Sochan (undrafted) | 1 of 2 |
| 8 | JCo | 0.45 / 0.55 | -3.9 | +18.9 | 9 / 3 | Tyrese Haliburton (seat 8), Jimmy Butler (undrafted), Nic Claxton (seat 8) | 2 of 2 |
| 9 | Kevin | 0.45 / 0.55 | -2.0 | +21.5 | 9 / 4 | Pascal Siakam (seat 9) | 1 of 1 |
| 10 | David | owner | -4.5 | -8.8 | 7 / 4 | none | — |
| 11 | Cayas | 0.40 / 0.60 | -2.9 | +6.6 | 7 / 4 | none | 0 of 0 |
| 12 | Hegi | 0.65 / 0.35 | -10.7 | +27.8 | 3 / 7 | Immanuel Quickley (seat 12), Andrew Wiggins (seat 3) | 1 of 2 |

loyalty fired on 10 of the 16 loyalty names that were drafted by anyone (undrafted names excluded)

Target-wait (`target_wait_2026-10-07d.json`, 11 rooms): deep (mkt − pick ≥ 24) — 🎯s passed on 23, still there at the next owner turn 13, at the turn after 3 of 20; mid (12–23) — 🎯s passed on 6, still there at the next owner turn 2, at the turn after 1 of 5; near (< 12) — 🎯s passed on 14, still there at the next owner turn 6, at the turn after 0 of 13.

## Watchlist

- Saddiq Bey undrafted in this room: the V4 bots weigh his XRank (~120) from round 7, so a room that leaves him is a room that found more XRank elsewhere; one room, logged, not a rule.
- Castle's and Barrett's minutes at WO-5 after two preseason games per team (D-CAST-2a).
- The survival chips against the cast (D62-2: leave, log).

## Open-item receipts

| item | query run (2026-10-07) | dated finding |
|---|---|---|
| (this analysis) | machine replay only — no web research in this report | pull receipts for the window live in `after-report-2026-10-07.md` (the morning's pull, same day) |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (after-report-2026-10-07.md, ten receipts dated 10/7) | all HELD or unsigned on 2026-10-07; nothing changed this evening |

## Bounds

- Grades are on the v49 lines (the two re-derived rows included); the WO-5 refresh will move them.
- A MOCK has no second record; only the owner's picks are an outside input.
- One room is one draw of the bots' seeded noise; the fidelity read is a single sample.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D66-1 | The first room on v49 grades 20.16 percent with the three fixes behaving as built (late card all priced; Castle, Barrett, Hachimura, Brooks, Mitchell drafted by the cast inside the human ranges; no unsigned man anywhere). Keep practice rooms on v49 as the baseline through the 14th? | yes |
| D-V4-1, D-CAST-2a/2b, D-CAST-1/3/4, D-C64-1, D62-1..3 and earlier | carried | carried |

## Provenance

- Inputs: the owner's exported draft state (uploaded 2026-10-07 evening), copied verbatim to `arena/data/states/draft_state_66.json` (md5 `8f2ee9dd30cc72e87ea4f6b98299e0d8`); the pool frozen from main `269c522` as `arena/results/m66_players_v49.csv`.
- Every figure from `arena/results/m66_*.json` and `target_wait_2026-10-07d.json`; the arms use 18,000 CRN seasons (seeds 11/23/47) on the real eight-team bracket; the deck card and the audit ran the v49 page's own engine under node; the human ranges from `dcast_realism_picks_2026-10-07.json`.
- Not verified: nothing here rests on web research.

## In plain language

**What this was.** Your first practice room on the page with all of today's fixes. It grades 20.2 percent on the real bracket, first of twelve, first in expected weekly category wins, and you took the card's name at 5 of 13 turns.

**Did the fixes hold up?** Yes, on this one room. The late card showed only men Yahoo prices. The eleven drafted Castle at 78, Barrett at 112, Hachimura at 121, Brooks at 133 and Mitchell at 137 — the men you said real people draft, now drafted — and no unsigned man appeared. Bey went undrafted this time; that is one room and it is on the watchlist, not a rule.

**What the card left on the table.** Hindsight's best single swap is Derrick White at #34, worth about 0.22 categories a week. The advice line spoke at 3 turn(s).

**Your decision.** D66-1 keep v49 as the practice baseline (default yes). Everything earlier is carried.
