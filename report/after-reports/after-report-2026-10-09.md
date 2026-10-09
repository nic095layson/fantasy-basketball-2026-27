# After-report — 2026-10-09 data pull + deck v52 + the category integrity audit

**Owner request (2026-10-09, verbatim):** "Please conduct daily refresh pull, provide after report.
Additionally conduct full categorical research to ensure data computation is operating with integrity
and accuracy" — WO-3's daily pull, plus a full audit of the nine categories on both planes (§8).

Pull window: 2026-10-08 → 2026-10-09 (from Thursday's pull, 14:17 UTC on 10/8, to 13:35 UTC on 10/9: six
preseason games played in it — Celtics–Cavaliers, Pelicans–Heat, 76ers–Nets, Wizards–Knicks,
Hawks–Spurs and Kings–Lakers, all 10/8. The Rockets–Mavericks game in Macao tipped at 12:00 UTC on 10/9
and was still in progress at the window's end (Houston led 85-69 in the third on ESPN's scoreboard at
13:47 UTC); its box score is the next pull's, its pregame rulings are this one's.)
Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13 ..
2026-10-07`, exit 0 (no provenance row changed today — Nurkić's change is games, not team).

**Method.** The six box scores read from ESPN's own feed (scoreboard and summary endpoints) before any
search — starters, minutes, lines, DNP reasons and the summaries' injury blocks — cross-referenced to both
planes by script, run under `python3 -I` on the downloaded JSON (`scratchpad pull1009/boxscores.txt`,
`box.json`). ESPN's league-wide injuries feed (118 rows) diffed against the deck's 49-row tag inventory
in both directions by script (`injuries.txt`). Then one sweep of 42 dated queries (33 standard, 9
extended for the six recaps and three injury items): the ledger check (Basketball-Reference's 2026-27
transactions page read directly, 85 date blocks, newest 10/7, plus one search ledger), a dedicated query
for each of the ten flagged receipts, one team-shaped query for each of the seven teams in the watch set
(CHI, GSW, LAC, MIL, NOP, POR, TOR), the injury sweep, and the carried items. Direct fetches: NBA.com's
news index and its 10/8 LeBron James debut story (AP), ESPN's roster API for all 30 teams (the verifier),
ESPN's scoreboards 10/8–10/13. NBA.com's 10/9 Starting 5 column was not yet published (404). Egress-blocked
as on every pull: Yahoo, SI, CBS, RotoWire and the other sports domains (their items rest on dated search
summaries, labeled where they stand alone).

## 1. Roster changes

No placement moved on either plane. One tier moved, by the owner's sheet default.

| player | change | date | sources | applied? |
|---|---|---|---|---|
| Jusuf Nurkić | **re-tagged `foot-recovery`** on the deck (excluded, availability 0) and **kit GP 62 → 25** (the exclusion twin) — D-1008-1 default (a), the owner silent: a partial plantar plate tear of the right second toe from the 10/4 opener, re-evaluated in four weeks, the start of the season missed | 2026-10-09 (default applied) | the Jazz's release on NBA.com (10/8), CBS Sports, SI Jazz, Bleacher Report, ClutchPoints; ESPN's league feed: Out, 2026-11-04 estimate | **Yes** — he leaves the deck's board (was 165 of 319, outside any 156-pick room). On the kit the board did **not** move: he stays #172, because the kit engine holds only team-`FA` rows off the board — the audit's finding A5 (§8, D-1009-1). The planes gate's propagation check flagged the kit-only GP move and was waived by name, recorded in the manifest (the Strus/Lively mechanism) |

Zero trades in the window. The ledger's newest block is 10/7: the Kings signed and waived Trhae Mitchell
(Exhibit 10) and the Trail Blazers waived Jaylen Martin — no pool row; the search ledger carries nothing
dated 10/8 or 10/9. ESPN's roster feed shows camp churn on names that are on no pool row: Miami lists
Gabe Madsen and Kylor Kelley and no longer lists J'Vonne Hadley (who played 12 minutes on 10/8) or Lester
Quinones, and Washington lists Skal Labissiere (his 10/5 Exhibit 10, per the ledger) [SINGLE-SOURCE: ESPN
roster feed] — no row on either plane, nothing applied.

## 2. The six box scores (ESPN's feed; lines rest on the box score where no outlet named them)

**Celtics 124, Cavaliers 113 (Cleveland; Boston's opener).** Boston rested Tatum, George, White, Queta,
Robinson, Hauser and Pritchard (rest or undisclosed on the feed, 10/10 estimates; most regulars expected
Saturday vs Philadelphia — CelticsBlog, NBC Sports Boston, Boston Globe). Luka Garza started at C — 27
min, 22 / 10 / 3 blk on 6-17, 3-10 from three — with Conley (18 min, 3 / 4 ast), Scheierman (23 min, 16,
4-7 from three), Walsh (26 min, 16) and Hugo González (not a pool row). Cleveland played its starters
the first half only (17 min each): Allen 6 / 4, Mobley 8, Mitchell 11 on 4-8, Watson 7 / 4 / 4 / 2 blk,
Tyson 14 on 6-8; Craig Porter Jr. 16 min / 5 / 10 ast off the bench. **James Harden** did not play —
right ankle soreness, "just caution" per Atkinson (RotoWire, Fear The Sword/Yahoo, CelticsBlog),
day-to-day with a 10/11 estimate.

**Heat 128, Pelicans 118 (Miami).** New Orleans started Zion (16 min, 8 on 3-9), Murphy III (14 min, 11),
Missi (19 min, 11 / 9), **Mathurin** (14 min, 8 on 3-7 — his first start, game two) and Fears (19 min,
11), with **Dejounte Murray** held out (right toe contusion, precautionary per Mosley — RotoWire, CBS
Sports; 10/14 on the feed); Poole 14 on 4-5 in 13 min, Bey 12 / 5, Queen 16 min with 5 to. Miami started
**Giannis** (18 min, 18 on 8-13, 2-5 FT), Wiggins 13, Adebayo 9, Klay Thompson 5 with 3 blk, Davion
Mitchell 9 / 7 ast (WSVN, Yahoo, TalkBasket); Larsson (illness) and Dru Smith (right calf strain, 10/16)
DNP.

**Nets 114, 76ers 108 (Brooklyn).** Philadelphia's new five played together for the first time:
**LeBron James** (18 min, 10 / 4 / 5 with one field-goal attempt and 8-8 at the line — NBA.com/AP),
Embiid (24 min, 6 on 1-5, 8 to), Jaylen Brown (24 min, 18 on 5-9, 7-7 FT), Maxey (19 min, 14),
Edgecombe (23 min, 11); Barlow (back), Simons (hamstring per the feed's ESPN note) and Bona (left foot)
out with 10/16 estimates. Brooklyn held out **Porter Jr.** (left wrist soreness) and **Sharpe** (left
shoulder soreness), both described as precautionary after playing the opener, and Mikel Brown Jr.
(ankle) — NBC Sports, NetsDaily, Yahoo; Clowney (11 in 20 min) and Wagner (6 / 4 stl) started in their
places, Randle 14 / 6, Demin 13 / 5 ast, Ellis 12.

**Wizards 111, Knicks 109 (New York).** Washington started Davis (17 min, 16 on 6-11, 7 reb), **AJ
Dybantsa** in his debut (23 min, 11 / 4 stl on 5-11), Kyshawn George (22 min, 12 / 7 / 5, 4 to), Ayton
at C with **Sarr** out (right foot) (17 min, 4 / 10) and Trae Young (17 min, 15, 3-6 from three) —
Bullets Forever/Yahoo, Sportando, TalkBasket, Fox Sports; Champagnie 12 / 2 blk, Carrington 11,
Coulibaly 2 on 1-7; Middleton rested. New York's starters played about 20 minutes: Brunson 13 on 6-12,
Hart 13 / 6, Anunoby 10, Towns 8 / 7 on 2-7, Bridges 2 on 1-6; Shamet 13 off the bench (Sofascore,
Yahoo); Bradley and Agbaji coach's decisions.

**Hawks 123, Spurs 116 (San Antonio; the Spurs' opener).** San Antonio started Champagnie (18 min, 10),
**Wembanyama** (17 min, 9 / 6 / 1 blk), Vassell (18 min, 12), **Castle** (18 min, 14 on 5-8 / 4 / 3) and
**Harper** (19 min, 16 on 5-7 / 4 / 4) — Yahoo, News 4 San Antonio, Eurohoops; **Fox** was a late
scratch with soreness after a demanding morning practice (Yahoo; the feed), Harris out (left calf).
Atlanta started Okongwu (22 min, 13 / 4 / 5), McCollum (19 min, 14, 4-6 from three), Alexander-Walker
(23 min, 7 on 2-8), Aaron Wiggins (24 min, 10) and **Daniels** (21 min, 13 / 11 reb on 6-16, 1 stl);
Flemings 15 / 5 ast / 3 stl in 20 min off the bench; Jalen Johnson (rest), Dort (right knee bruise) and
Gueye (foot) out.

**Lakers 114, Kings 110 (Los Angeles).** Sacramento sat **Sabonis, Keegan Murray, Monk and Simmons**
again (the Kings' availability report via James Ham; Yahoo, Sactown Sports) and started Hunter (18 min,
3 / 5 to), Achiuwa (24 min, 18 on 9-13), Raynaud (24 min, 13 / 10 / 2 blk), LaVine (23 min, 11 / 4 stl)
and **Acuff Jr.** (23 min, 12 on 4-15, 2-7 from three — two starts in two games; Yahoo, Sactown Sports).
The Lakers started Looney and Thiero (not pool rows), **Dončić** (25 min, 23 on 6-16, 9-9 FT, 5 to),
Reaves (25 min, 8 / 5 / 8 ast) and Grimes (29 min, 12, 6 to); Mamukelashvili 19 on 7-10 and LaRavia 17
off the bench; Kessler (finger), Sexton (lower body), Knecht and Ziaire Williams out with 10/13 estimates.

**Macao (in progress at the window's end).** Pregame: **P.J. Washington** ruled out with a left ankle
sprain, severity unclear, next chance the 10/11 rematch (ESPN's feed; RotoWire, CBS Sports, Athlon);
Irving out (left knee rest; May says he plays one of the two games), Aldama (right knee) out or a
game-time decision, Lively out (Athlon, China Daily, the feed). The box score is the 10/11 pull's.

## 3. Flagged-item receipts (F1) — verdicts

| card | 10/9 finding | verdict |
|---|---|---|
| Brandon Ingram | no new item; the 9/28 timeline stands; the feed's 2026-11-01 estimate | HELD −0.15 |
| Kristaps Porziņģis | no new item; out indefinitely on the feed (Slater); Kerr "definitely concerning" ~10/6 | HELD, veto unchanged |
| Kawhi Leonard | sits the 10/10 Vancouver game (TSN, Sportsnet via Daily Hive); 10/13 vs the Knicks the earliest named first game | HELD |
| Cam Thomas | unsigned; the ledger's newest block (10/7) carries no signing (Basketball-Reference, Spotrac) | HELD |
| Jaden Ivey | unsigned; no signing in the ledger (Basketball-Reference, Spotrac) | HELD |
| Jeremy Sochan | no new item; Portland's next game 10/12 vs the London Lions | HELD −0.2 |
| Lonzo Ball | unsigned; no signing in the ledger (Basketball-Reference, RotoWire) | HELD |
| Rob Dillingham | unsigned; no signing in the ledger (Basketball-Reference, Spotrac) | HELD |
| Bennedict Mathurin | **started** game two at Miami (14 min, 8 on 3-7) with Murray out; one start in two games | HELD, WO-5's 10/11 pass |
| Ryan Rollins | no new item; Milwaukee's next game 10/11 at Charlotte | HELD, WO-5 |

`judgment_open_items.py` on the re-authored page: 10 flagged, the same ten.

## 4. The carried items

- **Nurkić** — applied (§1). Re-entry when two outlets report him cleared and playing.
- **Harden** — right ankle soreness, held out for caution; next chance 10/11 vs Orlando. Untagged (deck
  31; one of the card's repeat names, §Repeat-name). Not a tier question on one precautionary absence.
- **P.J. Washington** — left ankle sprain, ruled out pregame in Macao; next chance 10/11. Untagged; he is
  also LINE QUESTIONED on the repeat-name check (WO-5).
- **Porter Jr., Sharpe, Mikel Brown Jr.** — precautionary absences in Brooklyn; 10/12 estimates.
- **Dejounte Murray** — right toe contusion, precautionary; 10/14 estimate; already tagged risk.
- **Fox** — late scratch, soreness; 10/10 estimate.
- **Sabonis, Keegan Murray, Monk, Simmons** — out again (two preseason games each for Murray and
  Simmons; Sabonis played 10 minutes in the opener). No tier change; re-check after 10/10 at Golden State.
- **Acuff Jr.** — two starts in two games; D-1006-1 (a) puts his line on WO-5's 10/11 pass.
- **Mathurin** — one start in two games (§3); WO-5.
- **Castle** — 18 minutes in San Antonio's opener; the minutes re-check (D-CAST-2a) follows 10/10 at
  Phoenix.
- **Hartenstein, Holmgren** — no new item; 10/12 at Atlanta (D-1008-2 holds).
- **Bridges** — no new item; Saturday vs San Antonio the named chance.
- **Claxton, Harris, Knueppel, Coby White** — no new item; the opener in question for all four
  (re-evaluations about 10/19–10/20).
- **Strus, Lively** — exclusions stand; Lively out of Macao.
- **Beal, Duren, Bona, Brown Jr., Suggs, Black** — no new item beyond the feed's estimates.
- **Lendeborg** — Golden State's next game 10/10 vs Sacramento (D-1007-1 holds until WO-5).

## 5. Window sweep, team shadows, injury sweep

**Team shadows (7):** CHI — Claxton's two-week re-evaluation (about 10/19), Memphis tonight; GSW —
Porziņģis out indefinitely, Sacramento 10/10; LAC — Vancouver 10/10, Ingram's timeline; MIL — Charlotte
10/11; NOP — Murray's toe, Mathurin's start; POR — no dated item (London Lions 10/12); TOR — Kawhi sits
10/10. No trade or signing touches a pool row.

**Injury sweep, both directions (mechanical).** ESPN's league injuries feed (118 rows, fetched 10/9)
against the 49-row tag inventory (16 excluded, 33 risk) before today's edit:

| direction | result |
|---|---|
| pool rows with status Out on the feed | 8: Ingram (risk), Strus, Moody, Butler, Mark Williams, Shaedon Sharpe, DiVincenzo (excluded) — and Nurkić, the one untagged Out row, now excluded by the D-1008-1 default (§1) |
| tagged rows absent from the feed (candidates for "cleared") | 26: the nine `out-*` free agents and retirees and 17 risk rows (Davis, Lillard, Morant, Haliburton, Edey, Zion, Embiid, LeBron and the rest), all playing or practicing under their tags; none re-tagged (first-season-back convention) |
| untagged rows on the feed with Out or a return date after 10/21 | 1 before the edit (Nurkić), 0 after |

Day-to-day items on the feed for untagged rows (not tier questions today): Harden, P.J. Washington,
Aldama (10/11); Porter Jr., Sharpe, Mikel Brown Jr., Hartenstein, Holmgren, Filipowski, Markkanen
(10/12); Sexton, Knecht, Ziaire Williams (10/13); Simons, Bona, Barlow, Dru Smith (10/16); Harris (10/20);
Claxton, Knueppel, Coby White (10/21); Fox, Sabonis, Monk, Dort, Bridges and the rested Celtics (10/10).

**Garbles caught (search summaries, logged, not used):** Acuff "19 points on 8-of-17 in a 127-103 loss"
(the 10/5 game, not 10/8); a summary asserting the Lakers and Kings did not meet on 10/8 (the box score
says they did, 114-110); Harden's February 2026 thumb fracture returned for the ankle query; the 2022
Nurkić plantar fasciitis; Sabonis' October 2025 hamstring; Hartenstein's 2025 soleus strain; Bridges'
2025 Hornets ankle; Dejounte Murray's 2024 hand and 2025 Achilles; the 2025 Celtics–Cavaliers preseason
story; Fox's 2026 conference-finals ankle; Lively's 2025 stress fracture; Strus' 2024 Cleveland injuries;
Duren's spring 2026 knee and ankle.

## 6. Board effects (computed, never eyeballed)

- **Kit:** `rank_engine.py` re-run, 200 of 321 projected (four unsigned rows held off); the diff against
  the morning snapshot is Nurkić's GP cell and the generation-date line. **No rank moved** — Nurkić stays
  #172 at his per-game value (negative totals are never discounted, and GP-25 rows are not held off the
  board; §8 A4/A5, D-1009-1).
- **Deck:** the draftable ordering recomputed before and after (`scratchpad pull1009/deck_board_diff.json`):
  319 → 318 draftable, 1 exit (Nurkić, from 165), 0 entries, 0 moves of three or more places, 0 value
  changes — he sat outside the top-156 fixed point, so no z-score moved; the order after equals the order
  before with him removed (checked by script).

## 7. Deck build and publish

- `data/players.csv`: 139 notes appended and one re-tag (Nurkić); no line, team or other tag change; CRLF
  preserved, every other byte untouched (140 lines in the diff). Dylan Cardwell's note was skipped — it
  still ends in `]` (the build regex trap, D-1006-3).
- **A defect in my own note generator, caught before anything shipped:** the first run dated the two late
  10/8 games (Hawks–Spurs, 00:00 UTC; Kings–Lakers, 02:45 UTC) by their UTC date and wrote "the 10/9 game
  in Macao" into 33 notes, Wembanyama's and Dončić's among them. Found by reading the built page; the
  verification chain was stopped, the pool and page restored to their committed bytes (md5 match), the
  generator fixed (Eastern date; Macao by venue), the edits re-applied and every appended fragment checked
  by script — 0 notes with a 10/9 game date outside the three Dallas pregame rulings. The page was rebuilt
  and every gate re-run from the start on the corrected pool.
- `scripts/verify_rosters.py` (no exemption): direct-complete, all 30 rosters, 335/335 matched, 0
  mismatches, 0 unmatched.
- `hoops.py freshness --stamp` with `--pool-changes` (gate 4): 2026-10-09; one tier, 139 notes.
- `JUDGMENT` re-dated 2026-10-09 with the ten receipts; colophon Data paragraph rewritten for 10/9 (gate 6
  accepted it).
- `build_deck.py --planes-waive "Jusuf Nurkic: the exclusion twin …"`: planes 315 shared · team 0 ·
  exclusion 0 · drift 0 · propagation 0 · waived 1; 170 line differences by design; market
  `yahoo-2026-10-06.csv`, 246/335 priced, 3 days old; built 335 players, pull 2026-10-09, injection
  round-trip OK, "safe to publish".
- `check_parity.py`: PARITY: EXACT MATCH (364 owner turns across 28 committed states; 318 market ranks compared, 240 priced). `test_card.py` 99/99, `test_gates.py` 47/47, `test_draft.py` 65/65. `full_dom_check.mjs` on `draft_state_54.json`: 143 assertions, 0 failed, 0 page errors, pass true (`arena/results/full_dom_check_2026-10-09_v52.json`). `repeat_market_check.py`: 21 of 21 mocks replayed, 12 flagged (the section below). Every result file before the chain was checksummed: 504 files unchanged, three new (the audit, the DOM check, the repeat-name record).

## 8. Category integrity audit (owner request, 2026-10-09)

**Question.** Is the nine-category computation operating with integrity and accuracy — on both planes,
in every category?

**Method.** A new read-only harness, `arena/mocks/audit_1009/category_audit.py` (deck repo), record
`arena/results/category_audit_2026-10-09.json`, run twice on today's final pool with byte-identical
output. Five parts: **A** an independent re-implementation of each plane's z-score method written from
its spec (deck: the `hoops.zscores` docstring — top-156 fixed point over playable rows, volume-weighted
FG%/FT% impact, TO negated, availability on positive totals; kit: PROMPT.md §4.2 — pass 1 over all signed
rows, pass 2 over the top 180, GP/82 + (1 − GP/82)·0.20 on positive totals), compared cell by cell with
each engine's own output; **B** data integrity per category; **C** each category's agreement with the
outside per-game lines (Yahoo 10/6, Hashtag 10/6, RotoBaller 9/29) and with the 2025-26 actual line
(Basketball-Reference, 25+ games, 432 players); **D** ranking sensitivity per category; **E** cross-plane
agreement. Outside lines enter as the median of those present (two or more).

### 8.1 Verdicts

| check | result | verdict |
|---|---|---|
| Deck engine reproduced (all 335 rows × 9 categories) | max \|independent − engine\| **0.0** in every category; the top-156 fixed point found in 2 iterations and stable; adjusted-value order identical for all rows | **PASS** |
| Kit engine reproduced (321 rows with a team × 9) | max \|independent − engine (unrounded)\| **0.0** in every category; the committed board prints exactly the engine's values (0 formatting mismatches, largest raw gap 0.00499 inside the 2-decimal rounding); top-200 order identical | **PASS** |
| Page engine (JS) vs Python | `check_parity.py` PARITY: EXACT MATCH — 364 owner turns across 28 committed states; 318 market ranks compared (240 priced); exit 0 | **PASS** |
| Direction of every category | Spearman(raw stat, z) = +1.000 in eight categories and −1.000 in TO; FG%/FT% z monotone in volume-weighted impact | **PASS** |
| Domains, 3PM ≤ FGM, duplicates | 0 / 0 / 0 on both planes; every percentage in (0, 1) | **PASS** |
| Kit pool convergence | the spec says "iterated once"; a third pass would keep 177 of the 180 pool names and move top-200 ranks 0.74 places on average, 4 at most | **PASS** (information) |
| Points identity (pts = 2·FGM + 3PM + FTM) | deck top 200: residual sd **0.725**, 9 rows beyond max(1.0, 8%) — Embiid +2.91, Irving +2.54, Towns +2.27, Haliburton −1.79, Okongwu −1.76, Duren −1.54, Giddey −1.52, Edey −1.12, Nembhard −1.06; kit top 200: mean **−0.27**, sd 0.488, 6 rows — Amen Thompson −1.80, Adebayo −1.79, Kessler −1.58, Gobert −1.50, Duren −1.49, Gafford −1.17. For scale, Hashtag's lines (sd 0.056) and the 2025-26 actual lines (sd 0.055) hold the identity to rounding | **FINDING** — D-1009-3 |
| Availability discount's reach (both planes) | adj = total × availability **only when the total is positive**, and the zero sits at the **mean** of the pool, not at replacement: the deck's last positive playable row is #58, so **19 of the 29 risk-tagged rows in the deck's top 200 carry no discount** (LeBron 62, Dejounte Murray 63, Morant 65, George 66, VanVleet 68, Embiid 71, Edey 84, Lillard 88, Keegan Murray 100, Zion 105, Sarr 110, Ingram 117, Mitchell Robinson 133 and six more); the kit's zero is at #69 and 74 of its top 200 with GP under 70 carry none. The deck docstring says the zero "sits at replacement level" — measured, it sits at the pool mean (mean total of the 156 = 0.000). Counterfactual (discount measured from the rank-156 total, −2.84): 121 of the top 200 move, at most 14 places; 24 of the 29 risk rows fall 1–14 places (Haliburton 7 to 12, Irving 15 to 24, Curry 17 to 26, Tatum 21 to 29, Embiid 71 to 83, Lillard 88 to 101). The card's ΔECW half is **not** affected — the weekly model prices every player's games as 3.5 × his weekly availability whether his value is positive or negative (`teamWeekModel`); the gap reaches the adjusted-value half of the card's blend, the board order and the mock bots' value axis (which share the rule) | **FINDING** — D-1009-2 |
| Kit exclusion class on the board | the kit engine holds only team-`FA` rows off the board; GP ≤ 25 rows (the deck's exclusion twin) stay on it at their per-game value: **Butler #68** (GP 20 — the zero line again), Lively #107, Mark Williams #121, Shaedon Sharpe #136, **Nurkić #172** (today's default), DiVincenzo #176; five of them sit inside the kit's 180-player z-pool. Holding them off as FA rows are held: 143 of the top 200 move, 2.2 places on average, 8 at most | **FINDING** — D-1009-1 |
| Kit per-36 rates vs last season's league max | 3 cells marginally above: Jokić AST 11.12 vs 11.07, Trae Young AST 11.11 vs 11.07 and TO 4.63 vs 4.53 per 36 | noted (within a hair; not defects) |
| Category agreement with the outside lines | §8.2 | no computation defect; WO-5 inputs (D-1009-4) |
| Cross-plane (309 shared names) | per-category Spearman 0.970–0.990; mean deck − kit within ±0.15 pts and ±0.04 elsewhere; lines differ by design (the planes gate's 170 warnings) | by design |

### 8.2 The nine categories against the outside lines and last season (deck top 146 with two or more outside lines)

| category | ours − outside median (mean) | share above | net z vs median | ρ vs Hashtag | ρ ours vs 2025-26 actual | outside sources vs 2025-26 actual | range-check cells (generous / low, z) | rank move if replaced by the median (mean / max) |
|---|---|---|---|---|---|---|---|---|
| FG% | +.0002 | .49 | −1.5 | .884 | **.778** | .949–.955 | 38 (+10.5) / 35 (−13.0) | 7.3 / 39 |
| FT% | −.0032 | .40 | −7.0 | .921 | **.857** | .957–.975 | 31 (+10.1) / 53 (−15.0) | 5.9 / 47 |
| 3PM | +0.06 | .48 | +8.6 | .949 | .876 | .942–.952 | 26 (+9.5) / 13 (−5.3) | 5.7 / 35 |
| PTS | +0.58 | .62 | +15.6 | .939 | .894 | .927–.943 | 39 (+13.2) / 10 (−3.9) | 6.8 / 30 |
| REB | +0.32 | .65 | +18.2 | .968 | .943 | .953–.960 | 34 (+9.9) / 6 (−1.1) | 4.7 / 24 |
| AST | +0.18 | .59 | +13.6 | .966 | .912 | .952–.961 | 35 (+10.3) / 9 (−2.4) | 4.5 / 25 |
| STL | +0.04 | .47 | +18.1 | .893 | **.782** | .903–.918 | 19 (+12.3) / 10 (−5.1) | **8.6** / 41 |
| BLK | +0.05 | .48 | +13.6 | .940 | .858 | .935–.962 | 19 (+9.3) / 7 (−2.9) | 5.3 / 35 |
| TO | +0.10 | .54 | −20.1 | .915 | .854 | .938–.947 | 11 (+4.3) / 41 (−20.2) | 7.5 / 38 |

How to read it. (1) **Level:** our counting lines run above the outside median — +0.58 points, +0.32
rebounds, +0.18 assists a game on average — and so do our turnovers (+0.10, which counts against), with
FT% a little below (−.003). That is the signature of more minutes and usage than the outside sources
assume, not of an engine error; a uniform level shift moves nobody in a z-frame. (2) **Ordering:** in
every category our lines agree with last season's actual line less than each outside source does — most
in FG% (.778 vs .95), steals (.782 vs .91), FT% (.857 vs .96–.98) and blocks (.858 vs .94). That is
partly by design (the outside sources lean on last season; our lines carry role changes — Giannis to
Miami, LeBron and Brown to Philadelphia), and last season's preseason backtest favored our method over
Yahoo's (top-60 ρ .640 vs .451; after-report-2026-10-08-standing-checks.md §5). It is not proof of error.
FT% is the exception worth naming: it is the most stable category year to year, and the outside sources
track last season's FT% at .96–.98 while ours sit at .857 — the 53 low FT% cells are the largest single
block in the range check. (3) **Consequence:** replacing one category at a time with the outside median
moves the top 150 by 4.5–8.6 places on average; steals move it most (8.6), then TO (7.5) and FG% (7.3).

### 8.3 The largest departures, by category (deck top 150; z beyond the outside median in the deck's frame)

| category | player (deck rank): ours vs outside median vs 2025-26 actual, z |
|---|---|
| STL | **Dyson Daniels (11): 3.0 vs 2.2 vs 2.0, +2.28** — the single largest cell in the audit; Fred VanVleet (68): 1.6 vs 1.2 (no 2025-26 line), +1.14; Ausar Thompson (109): 1.7 vs 2.1 vs 2.0, −1.14; Jalen Williams (16): 1.7 vs 1.4 vs 1.2, +0.86 |
| BLK | Wembanyama (1): 4.0 vs 3.2 vs 3.1, +1.55; Gafford (90): 1.7 vs 1.2 vs 1.3, +0.97; Buzelis (125): 1.1 vs 1.6 vs 1.5, −0.97; Jalen Johnson (13): 1.0 vs 0.6 vs 0.4, +0.77 |
| FG% | Okongwu (36): .560 vs .481 vs .480, +1.42; Tre Jones (143): .475 vs .543 vs .553, −1.06; Harper (146): .455 vs .505 vs .505, −0.98; Barnes (38): .450 vs .482 vs .507, −0.85 |
| FT% | Gobert (78): .680 vs .596 vs .526, +1.15; Embiid (71): .825 vs .866 vs .854, −1.06; **Flagg (22): .780 vs .836 vs .827, −0.96** (already on WO-5, D-RN-2); Amen Thompson (30): .700 vs .760 vs .779, −0.93 |
| PTS | Duren (60): 12.5 vs 17.7 vs 19.5, −0.96; Fox (51): 24.0 vs 18.9 vs 18.6, +0.94; Filipowski (123): 15.0 vs 10.0 vs 11.4, +0.93; Dybantsa (139, rookie): 20.5 vs 15.5, +0.93 |
| REB | Filipowski (123): 8.5 vs 6.3 vs 7.2, +0.89; Davis (5): 11.8 vs 10.1, +0.67; Aldama (130): 6.8 vs 5.1 vs 6.7, +0.67; Hartenstein (75): 11.0 vs 9.4 vs 9.4, +0.63 |
| AST | Franz Wagner (29): 5.8 vs 4.2 vs 3.3, +0.83; Zion (105): 5.4 vs 3.9 vs 3.2, +0.78; Herro (43): 6.2 vs 4.8 vs 4.1, +0.72; Coulibaly (131): 3.8 vs 2.5 vs 2.6, +0.70 |
| 3PM | Knueppel (94): 2.6 vs 3.5 vs 3.4, −0.96; Pritchard (37): 3.8 vs 3.0 vs 2.7, +0.85; Buzelis (125): 1.5 vs 2.3 vs 2.2, −0.85; Edwards (8): 4.2 vs 3.5 vs 3.4, +0.75 |
| TO | Franz Wagner (29): 3.0 vs 2.1 vs 1.7, −1.21; Harden (31): 4.2 vs 3.3 vs 3.5, −1.21; Zion (105): 3.3 vs 2.4 vs 2.0, −1.21; Herro (43): 3.1 vs 2.3 vs 1.9, −1.08 |

Every one of these is a line question for WO-5 under the two-outlet rule, not a computation defect; the
range check (D-RN-3) already requires each to come back inside the range or carry a mechanism.

### 8.4 Corrections made during the audit (recorded, not hidden)

- **Rotoworld is not a projection source.** The first run counted Rotoworld's 9-cat sheet as an outside
  line; its Spearman against the 2025-26 actual line came back 1.000 in eight categories. The repo's own
  parse note says it plainly ("The kit carries no projected stat lines"): those columns are last season's
  stats. Excluded from every line comparison, as `range_check.py` already does; no shipped check used it
  as a line.
- **Scope.** The first run's top-150 lists included the excluded rows (adjusted value 0, which lands at
  the zero line, about #58). Corrected to playable rows only, as the board and `range_check.py` use.
- **Kit reproduction strength.** The first run compared the kit to its printed board (2 decimals); a direct
  comparison with the engine's unrounded values was added and returns 0.0.

### 8.5 What this means for the draft

The arithmetic is sound: both engines reproduce exactly from an independent implementation, the page
agrees with the Python, every category points the right way and no value is out of domain. What the audit
found is three method gaps, none of which the mocks could have caught because they are graded on the same
engine: (1) the injury discount does not reach players below the zero line — about half the draftable
pool (D-1009-2); (2) the kit board still lists the injured players the deck excludes, Butler at #68
(D-1009-1); (3) 15 lines whose points do not follow from their own shooting, Embiid's by almost three
points (D-1009-3). And in the data, the categories where our lines stand furthest from both the market and
last season are steals (Daniels above all), FT% and FG% — which is where WO-5's two passes should start
(D-1009-4).

## 9. Gates (2026-10-09)

| gate | result |
|---|---|
| `report/check_provenance.py` | PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07; exit 0 |
| `report/rank_engine.py` | exit 0; 200 of 321 projected (4 unsigned held off); board diff = Nurkić's GP cell + the date line |
| `scripts/verify_rosters.py` (deck, no exemption) | direct-complete, all 30 rosters, 335/335, 0 mismatches, 0 unmatched; exit 0 |
| `hoops.py freshness --stamp --pool-changes` (deck) | 2026-10-09, one tier and 139 notes asserted |
| `scripts/build_deck.py` (deck) | gates 1–7 + F8 pass with one named waiver (Nurkić, the exclusion twin); round-trip OK; "safe to publish" |
| `scripts/check_parity.py` (deck) | PARITY: EXACT MATCH — 364 owner turns across 28 committed states; 318 market ranks compared (240 priced); exit 0 |
| `scripts/test_card.py` / `test_gates.py` / `test_draft.py` (deck) | 99 / 47 / 65 cases passed; exit 0 each |
| `arena/mocks/full_dom_check.mjs` (deck) | 143 assertions, 0 failed, 0 page errors, pass true; exit 0 |
| `scripts/repeat_market_check.py` (deck) | 21 of 21 mocks replayed, 12 flagged (3 LINE QUESTIONED, 9 SOURCES SPLIT), 5 near misses; exit 0 |
| `arena/mocks/audit_1009/category_audit.py` (deck) | exit 0; two runs byte-identical; record `arena/results/category_audit_2026-10-09.json` |
| `report/check_report.py` | PASS — structure, publication rule, pull-log row; exit 0 (seven rows reworded first: the gate's transaction heuristic matched the four free-agent verdict rows, which now name their outlets, two audit rows' wording, and the rank arrows in the availability row) |
| `report/check_derived.py` | PASS — all 17 dated artifacts reproduce byte-for-byte; exit 0 |
| `scripts/judgment_open_items.py --check-report` (deck plane) | PASS — all 10 flagged names carry a receipts row; exit 0 |
| `scripts/repeat_market_check.py --check-report` (deck plane) | PASS — 12 flagged names, each with a row (21 of 21 mocks replayed); exit 0 |
| artifact publish | Version 52, id 1791555525-2e7a, the standing URL; the served file carries the built page byte-for-byte inside the service's 364-byte wrapper; manifest built 2026-10-09 |

## 10. Watchlist / open items

- **Macao** — Rockets–Mavericks 10/9 box score and the 10/11 rematch (P.J. Washington's ankle, Irving's
  one game, Aldama, VanVleet, Adams, Smart, Sengun) at the 10/11 pull.
- **WO-5, first pass (10/11)** — the 24 teams with two games after Saturday; the queue: Flagg (D-RN-2), the
  LINE QUESTIONED names, Daniels and Bey, Acuff Jr. (D-1006-1), Mathurin, Rollins and Jerome (D-1002-3),
  Castle (D-CAST-2a after 10/10), Lendeborg (D-1007-1), and — if the owner agrees — the audit's largest
  departures and the 15 points-identity rows (D-1009-3/4). `range_check.py --check-report` on the pass.
- **Harden** — ankle; 10/11 vs Orlando.
- **Brooklyn's three** — Porter Jr., Sharpe, Mikel Brown Jr.; 10/12.
- **Sacramento's four** — Sabonis, Keegan Murray, Monk, Simmons; 10/10 at Golden State.
- **Hartenstein, Holmgren** — 10/12 at Atlanta (D-1008-2).
- **Kawhi** — sits 10/10; the 10/13 Knicks game.
- **Claxton, Harris, Knueppel, Coby White** — re-evaluations about 10/19–10/20.
- **Nurkić, Strus, Lively** — exclusions stand; re-entry on two outlets reporting a cleared return.
- **The build regex trap** — D-1006-3; Cardwell's note still ends in `]`.
- **Market** — the Yahoo paste is three days old; the next is the owner's input on the 10/14 morning.
- **Owner decisions carried:** D-1008-2, D-1008-3 (approved 10/8: two passes), D-1007-1, D-1006-1..4,
  D-1005-1/3, D-1002-1, D-1002-3, D-CAST-2a/2b, D-RN-4 (after the draft), D71-1, and the sheets before them.

## Open-item receipts

| player | query run | dated finding |
|---|---|---|
| Brandon Ingram | Brandon Ingram Clippers Achilles update October 9 2026 · ESPN league injuries feed (fetched) | no new item; the 9/28 timeline (abc30, TSN, NBC Sports); the feed's 2026-11-01 estimate; HELD |
| Kristaps Porzingis | Kristaps Porzingis Warriors status update October 9 2026 · ESPN league injuries feed (fetched) | no new item; out indefinitely on the feed (Slater); Kerr "definitely concerning" ~10/6 — Bleacher Report, Newsweek, NBA.com 9/28; HELD |
| Kawhi Leonard | Kawhi Leonard Raptors Vancouver preseason status October 9 2026 · Toronto Raptors news October 9 2026 | sits 10/10 in Vancouver; 10/13 vs the Knicks the earliest — TSN, Daily Hive (Sportsnet's Grange), NBC Sports 10/3; HELD |
| Cam Thomas | Cam Thomas OR Jaden Ivey OR Lonzo Ball OR Rob Dillingham signs contract October 2026 · basketball-reference.com NBA_2027_transactions (fetched, 85 date blocks) · NBA transactions October 8 2026 | unsigned; no signing in the ledger's newest block (10/7) — Basketball-Reference, Spotrac |
| Jaden Ivey | (same queries) | unsigned — Basketball-Reference, Spotrac |
| Jeremy Sochan | Jeremy Sochan Trail Blazers roster spot October 9 2026 · Portland Trail Blazers news October 9 2026 | no new item; the camp battle stands — Roundtable 9/28, NBC Sports, Bleacher Report; next game 10/12; HELD |
| Lonzo Ball | (same free-agent queries) | unsigned — Basketball-Reference, RotoWire |
| Rob Dillingham | (same free-agent queries) · ledger (fetched) | unsigned — Basketball-Reference, Spotrac |
| Bennedict Mathurin | Bennedict Mathurin starts Pelicans Heat preseason October 8 2026 starting lineup · Heat beat Pelicans 128-118 … (extended) · ESPN box score 10/8 (fetched) | started at Miami, 14 min / 8 on 3-7, Murray held out — box score, Yahoo, Roundtable, Crescent City Sports; HELD, WO-5 |
| Ryan Rollins | Ryan Rollins Kevin Porter Jr Bucks starting point guard October 9 2026 · Milwaukee Bucks news October 9 2026 | no new item; next game 10/11 at Charlotte — Roundtable, Brew Hoop, Fox Sports; HELD |
| Jusuf Nurkić | Jusuf Nurkic Jazz foot plantar plate update October 9 2026 · ESPN league injuries feed (fetched) | no new item since the 10/8 release; Out on the feed, 2026-11-04 — NBA.com, CBS Sports; D-1008-1 default applied |
| James Harden | James Harden ankle Cavaliers Celtics preseason October 8 2026 · Cavaliers James Harden ankle soreness ruled out … (extended) · ESPN game feed (fetched) | right ankle soreness, "just caution" — RotoWire, Fear The Sword/Yahoo, CelticsBlog; 10/11 |
| P.J. Washington / Kyrie Irving / Santi Aldama | P.J. Washington ankle sprain Mavericks Rockets Macao October 9 2026 · Mavericks Rockets Macao … (extended) · ESPN injuries feed (fetched) | Washington left ankle sprain, out; Irving rest; Aldama knee — RotoWire, CBS Sports, Athlon, China Daily, the feed |
| Dejounte Murray | New Orleans Pelicans news October 9 2026 Dejounte Murray toe · Pelicans Dejounte Murray toe bruise ruled out Heat preseason (extended) | right toe contusion, precautionary per Mosley — RotoWire, CBS Sports, Yahoo; 10/14 |
| Michael Porter Jr. / Day'Ron Sharpe / Mikel Brown Jr. | Nets beat 76ers 114-108 preseason Porter Jr wrist Sharpe shoulder … (extended) · ESPN game feed (fetched) | wrist / shoulder soreness, precautionary; Brown's ankle non-contact — NBC Sports, NetsDaily, Yahoo; 10/12 |
| De'Aaron Fox / Stephon Castle / Tobias Harris | De'Aaron Fox soreness late scratch Spurs Hawks … · Hawks beat Spurs 123-116 … (extended) · Tobias Harris calf Spurs opener update … | Fox late scratch (soreness); Castle 14 in 18 min; Harris out for the preseason — Yahoo, News 4 San Antonio, KSAT 10/5, Spectrum News |
| Domantas Sabonis / Keegan Murray / Malik Monk / Ben Simmons / Darius Acuff Jr. | Lakers beat Kings 114-110 … (extended) · Domantas Sabonis ruled out again … · Darius Acuff Jr. Kings preseason Lakers … | the four ruled out (the Kings' report via James Ham); Acuff 12 on 4-15 — Yahoo, Sactown Sports, RotoWire |
| LeBron James / Joel Embiid / Jaylen Brown | nba.com/news/lebron-james-sixers-preseason-debut (fetched) · Nets beat 76ers … (extended) | LeBron 10 / 5 / 4 in the first half, one shot, 8-8 FT — NBA.com/AP, NetsDaily, Yahoo |
| AJ Dybantsa / Alex Sarr / Trae Young / Anthony Davis | Wizards beat Knicks 111-109 … (extended) · Alex Sarr foot Wizards ruled out Knicks … | Dybantsa 11 / 4 stl in his debut; Sarr out (foot), Ayton started — Bullets Forever/Yahoo, Sportando, TalkBasket, Fox Sports, Eurohoops |
| Luka Garza / Jayson Tatum / Derrick White / Neemias Queta | Celtics beat Cavaliers 124-113 … (extended) · Celtics Cavaliers preseason October 8 2026 … | Garza 22 / 10 starting at C; seven regulars rested — CelticsBlog, NBC Sports Boston, Boston Globe, BVM Sports |
| Giannis Antetokounmpo / Jeremiah Fears | Heat beat Pelicans 128-118 … (extended) | Giannis 18 on 8-13 in 18 min — WSVN, Yahoo, TalkBasket, SI Heat |
| Isaiah Hartenstein / Chet Holmgren | Isaiah Hartenstein ankle Thunder update October 9 2026 Holmgren | no new item (the search returned 2025 items) — the feed's 10/12 estimates; D-1008-2 holds |
| Miles Bridges | Miles Bridges ankle Suns Spurs Saturday update October 2026 | no new item (2025 Hornets items returned, logged) — the feed's 10/10 estimate |
| Kon Knueppel / Coby White / Brandon Miller | Hornets Knueppel hamstring Coby White calf Brandon Miller update October 9 2026 | no new item; White out for the preseason, the opener unclear — NBC Sports, ClutchPoints, RotoBaller, TSN 10/5-6 |
| Dereck Lively / Max Strus / Bradley Beal / Jalen Duren | Dereck Lively Max Strus Bradley Beal Jalen Duren injury update October 9 2026 | no new item (older items returned, logged); Lively out of Macao on the feed; exclusions stand |
| Adem Bona / Anfernee Simons / Dominick Barlow | 76ers Anfernee Simons hamstring Adem Bona foot Dominick Barlow back October 2026 | out for the two Boston games per ESPN's McMenamin on the feed; Bona's foot sprain — Eurohoops, NBC Sports Philadelphia |
| Walker Kessler / Collin Sexton | Lakers Walker Kessler finger Collin Sexton lower body Kings preseason October 8 2026 | out again 10/8, 10/13 estimates [SINGLE-SOURCE: ESPN feed on today's status] |
| (window ledger) | NBA transactions October 8 2026 signed waived traded · basketball-reference.com NBA_2027_transactions (fetched) | 10/7: SAC Trhae Mitchell signed and waived, POR waived Jaylen Martin; zero trades since 9/27 — Basketball-Reference, ESPN team pages |
| (injury sweep) | NBA injury news October 9 2026 preseason · NBA "cleared" OR "returns to practice" … October 9 2026 · ESPN league injuries feed (fetched, 118 rows) | §5; both searches returned older seasons (logged); the feed diff found the one untagged Out row (Nurkić) |
| (team watch, 7) | "<Team> news October 9 2026" one each: CHI, GSW, LAC, MIL, NOP, POR, TOR | §5 |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 d44734abf093), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 21 of 21 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-06.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-06.csv`, `hashtag-2026-10-06.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| PJ Washington | 17 of 21 | 87 | 148 | 178 | 144 | 141 | 121 | ast 2.4 vs 1.9-2; tov 1.5 vs 1.7-1.8; fg_pct .470 vs .448-.451; ft_pct .750 vs .698-.703 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Payton Pritchard | 16 of 21 | 37 | 82 | 33 | 90 | 92 | 72 | stl 1 vs 0.7-0.8; tpm 3.8 vs 3-3.2; tov 2 vs 1.3-1.3; ft_pct .850 vs .873-.875 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 15 of 21 | 28 | 65 | 60 | 56 | 43 | 44 | pts 18.5 vs 16.4-17; ast 2.3 vs 2.1-2.1; ft_pct .805 vs .813-.819 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Sandro Mamukelashvili | 15 of 21 | 81 | 169 | 138 | 105 | 153 | 120 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Daniel Gafford | 10 of 21 | 90 | 180 | 188 | 180 | 161 | 155 | pts 10.5 vs 9.1-9.8; reb 7.5 vs 5.8-6.5; ast 1.5 vs 1.1-1.2; blk 1.7 vs 1.2-1.4; fg_pct .700 vs .648-.689; ft_pct .700 vs .671-.687 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Jalen Suggs | 10 of 21 | 59 | 108 | 89 | 54 | 84 | 99 | pts 17 vs 14.1-15.1; ast 4 vs 4.8-5 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 9 of 21 | 82 | 143 | 94 | 121 | 137 | 98 | reb 7.5 vs 5.5-6.9; tpm 0.9 vs 1.2-1.3; fg_pct .520 vs .447-.498; ft_pct .740 vs .765-.828 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Isaiah Hartenstein | 7 of 21 | 75 | 104 | 141 | 92 | 100 | 102 | pts 11.5 vs 9.1-10.5; reb 11 vs 9.2-10.3; fg_pct .585 vs .597-.611; ft_pct .680 vs .642-.656 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Zach LaVine | 6 of 21 | 56 | 101 | 162 | 68 | 77 | 118 | pts 22.5 vs 17-21.1; reb 4.5 vs 3.1-3.6; ast 4 vs 2.8-3.4; tov 2.6 vs 2-2.4 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 5 of 21 | 89 | 141 | 122 | 131 | 125 | 123 | pts 16.8 vs 13.4-15.1; tov 1.5 vs 1-1.2; fg_pct .465 vs .432-.443 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Dyson Daniels | 5 of 21 | 11 | 62 | 20 | 65 | 56 | 53 | pts 14.5 vs 11.3-11.8; stl 3 vs 2-2.4; tpm 1.1 vs 0.5-0.6; fg_pct .495 vs .501-.513 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Saddiq Bey | 5 of 21 | 95 | 174 | 109 | 132 | 169 | 143 | blk 0.4 vs 0.1-0.1; tpm 2.4 vs 1.8-2; tov 1.5 vs 0.8-0.9 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Karl-Anthony Towns (16 mocks, value 6, market 15); Jalen Williams (15 mocks, value 16, market 39); Derrick White (11 mocks, value 24, market 45); Jalen Johnson (6 mocks, value 13, market 11); Mikal Bridges (6 mocks, value 61, market 83).

The same twelve names as the 10/8 run on 21 mocks — the flags are stable on today's page (the pool's lines did not move). P.J. Washington, Gafford and Vassell stay LINE QUESTIONED for WO-5's 10/11 pass; Washington's ankle sprain (§4) is availability, not the line question. Record `arena/results/repeat_market_check_2026-10-09.json`.

## Bounds

- Direct-complete roster verification proves membership, not role (335/335 today, no exemption).
- A preseason box score is a dated primary record, not a reprice mechanism; lines move at WO-5 (two passes,
  10/11 and 10/13).
- The Macao game was in progress at the window's end; its box score is the next pull's.
- The audit's outside comparison rests on three outside line sets (Yahoo 10/6, Hashtag 10/6, RotoBaller
  9/29) and last season's actual line; agreement with last season is not accuracy for next season (§8.2).
- The availability counterfactual (D-1009-2) is a board-order measurement only; the arena-calibrated 0.78
  was fit with today's rule, so any change would need that calibration re-run before it could be trusted.
- Yahoo, SI, CBS, RotoWire and most sports domains are egress-blocked; their items rest on dated search
  summaries. Thirteen garbles were caught (§5).

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-1009-1 | **Kit exclusion class.** The kit engine holds only team-`FA` rows off the board; GP ≤ 25 rows (the twin of the deck's exclusion) stay on it at their per-game value — Butler #68, Lively #107, Mark Williams #121, Shaedon Sharpe #136, Nurkić #172, DiVincenzo #176 — and five sit inside its 180-player z-pool. D-1008-1's option (a) said "set the kit's GP to 25 (the exclusion twin, off the board)", and the board did not follow (nor for Strus or Lively before it). (a) The engine holds GP ≤ 25 rows off the board and out of the pool as it does FA rows — one rule, a red-first test, the board diff in the report (143 of the top 200 move, mean 2.2, max 8); (b) keep, and say in the header that GP-25 rows remain listed | (a), at the 10/11 pull |
| D-1009-2 | **Where the injury discount starts.** Both planes multiply by availability only when the total is positive, and the zero is the pool mean (deck #58, kit #69), so 19 of the 29 risk-tagged rows in the deck's top 200 carry no discount; the deck docstring calls the zero "replacement level" and the page's colophon says the z-scores are "replacement-anchored", which they are not; the page's legend does say "×0.78 applied only when value is positive", but not that positive means above the average draftable player (about #58). The card's ΔECW half already prices games for everyone; the gap is in the adjusted-value half, the board order and the bots' value axis. (a) No method change before the draft (the 0.78 was arena-calibrated with this rule); correct the docstring and the colophon's wording at the next code-touching pull; review the anchor after the draft with D-RN-4; (b) anchor the discount at replacement now (the rank-156 total) — 121 of the top 200 move, max 14; needs the 0.78 refit, parity twins and the mock regrades before 10/14 | (a) |
| D-1009-3 | **Points identity.** 9 deck and 6 kit top-200 lines carry points that do not follow from their own shooting by more than max(1.0, 8%) (Embiid +2.9, Irving +2.5, Towns +2.3 on the deck; Amen Thompson −1.8, Adebayo −1.8 on the kit). (a) Add the identity to WO-5's acceptance — every top-200 line within ±1.0 of its implied points or a named mechanism — and reconcile the 15 rows on the 10/11 pass, both planes; (b) leave | (a) |
| D-1009-4 | **WO-5's order of work.** Start the 10/11 pass with the audit's largest departures (§8.3) — Daniels' steals first (+2.28 z, the largest cell), then Wembanyama's blocks, Okongwu's FG%, Gobert's FT%, Fox's and Duren's points — under the two-outlet rule, as the range check already requires | yes |
| D-1008-1 | Nurkić — **closed**: default (a) applied (§1) | — |
| carried | D-1008-2 (Hartenstein: hold until 10/12), D-1007-1, D-1006-1..4, D-1005-1/3, D-1002-1, D-1002-3, D-CAST-2a/2b, D-RN-4, D71-1 | as before |

## Provenance and bounds

- Inputs: ESPN's scoreboards (10/8–10/13), six summary feeds and the league injuries feed (fetched
  2026-10-09 13:35 UTC), ESPN's roster API for all 30 teams (the verifier); Basketball-Reference's 2026-27
  transactions page (85 date blocks); NBA.com's news index and the 10/8 LeBron James debut story; 42 dated
  web-search summaries; the committed 10/08 pools and boards as the pre-pull snapshots; for the audit, the
  kit's `report/market/` line files named in §8 and the deck's `bref_pergame_2025-26.csv`.
- Every number in §2, §5, §6 and §8 is a script run or a box-score read (`scratchpad pull1009/`,
  `arena/results/category_audit_2026-10-09.json`); every gate line is the command's own output.
- Not verified: the Yahoo, SI, CBS, RotoWire and Athlon articles (egress-blocked; headlines and search
  summaries only).

## In plain language

**What this pull did.** One day since Thursday's pull and six more preseason games in it. I read all six
box scores straight from ESPN's feed before searching, swept the news, checked every player's team against
ESPN's live rosters for all 30 clubs (all 335 matched), and rebuilt and republished the deck. A seventh
game — Houston and Dallas in Macao — was still being played when I finished, so it goes into Sunday's
refresh.

**The one data change.** Jusuf Nurkić comes off the board. You didn't answer yesterday's question about his
torn toe ligament, so the default applied, the same rule as Max Strus last week. He was 165th on the deck,
so no draft board moves.

**What the games said.** LeBron played his first game for Philadelphia and took one shot in 18 minutes —
10 points, all but two from the line, and five assists. James Harden sat Cleveland's opener with a sore
right ankle ("just caution"). P.J. Washington sprained his left ankle before the Macao game. Brooklyn held
out Michael Porter Jr. and Day'Ron Sharpe as a precaution. Mathurin started for New Orleans for the first
time, Acuff started again for Sacramento, and Sacramento sat Sabonis, Keegan Murray, Monk and Simmons
again. Boston rested seven regulars and Luka Garza scored 22. None of it moves a projection today; it all
feeds the refresh on Sunday.

**The category audit you asked for.** I rebuilt both scoring engines from scratch from their written rules
and compared them, number by number, with the real engines. They match exactly in all nine categories on
both the deck and the kit, every category points the right way (turnovers count against you), and no
number is out of range. The math is doing what it says. What I found is three places where the rules
themselves have gaps:

1. **The injury discount stops halfway down the board.** A player's value is only cut for injury risk if
   his total is above zero — and zero is the *average* draftable player, not the last one. So LeBron,
   Embiid, Morant, Lillard, Zion and Ingram, all ranked below about 58th, carry no injury discount at all
   on the board. The card's head-to-head half does account for their missed games; the value half does
   not. My suggestion (D-1009-2): don't change this five days before the draft — the 0.78 risk factor was
   tuned with this rule — and review it after.
2. **The kit board still lists players the deck has excluded.** Jimmy Butler, out until 2027, sits 68th on
   the kit board; Nurkić stays at 172. The deck, which is your draft-night board, excludes them correctly.
   Suggested fix (D-1009-1): make the kit hold them off the way it holds unsigned free agents.
3. **Fifteen projections don't add up.** For Embiid, Irving and Towns on the deck, the points line is two
   to three points higher than their own shooting numbers produce. Other sources' lines add up to within a
   tenth of a point. Suggested fix (D-1009-3): reconcile them in Sunday's refresh.

And one pattern in the data: compared with Yahoo, Hashtag and RotoBaller, our lines give players more
points, rebounds and assists — and more turnovers — which looks like more minutes than the market expects.
The biggest single gap anywhere is Dyson Daniels' steals: we project 3.0 a game, the market about 2.2, and
he averaged 2.0 last season. That is worth roughly two and a quarter category-points of value, and it is
first on my list for Sunday's refresh (D-1009-4).

**What broke and what I fixed.** My own note writer dated the two late Thursday games by UTC and labelled
33 players' notes as "the 10/9 game in Macao". I caught it reading the built page, rolled everything back,
fixed the dates, and rebuilt and re-ran every check from the start.

**Verification.** The rebuilt deck passed every check: the page and the Python agree exactly across 364 owner turns in 28 saved rooms, all 211 test cases pass, the browser robot drafted a full room with 143 checks and zero failures, the roster check matched all 335 players with no exception, the repeat-name check replayed all 21 mocks, and Version 52 is live at the usual link. The audit itself ran twice with identical output.

**Your decisions.** D-1009-1 (kit board: hold the injured off — default yes, Sunday), D-1009-2 (injury
discount: no change before the draft — default), D-1009-3 (reconcile the 15 lines Sunday — default yes),
D-1009-4 (start Sunday's refresh with Daniels' steals and the other biggest gaps — default yes).

**Next.** Sunday the 11th: the first projection refresh pass (WO-5), with the Macao game, the audit's
queue and the range check.
