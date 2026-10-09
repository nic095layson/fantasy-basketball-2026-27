# After-report — 2026-10-09 (RotoWire): the expert panel's 9-cat rankings and notes, taken in as the other side of the arithmetic

**Owner request (2026-10-09, verbatim):** "On the topic of real life analysis (role, health, situation and opportunity).
Here is an article written today, 10/9 by RotoWire panel of NBA experts. Please implement or consider as you see fit, I
just want to give you the other side of things in supplement to your arithmetic expertise."

Pull window: 2026-10-09 → 2026-10-09 — not a pull: a third-party intake. The article is pinned verbatim
(`report/market/rotowire-raw-2026-10-09.txt`), transcribed deterministically (`rotowire_text.py`, 150 rows; the note per
player kept verbatim, the health and role words it carries named), joined to the pool and compared with the kit board and
Yahoo's market (`third_party_market.py rotowire`), and registered (derived gate 21 of 21). No pool row changed: a single
outlet never moves a row (fix F2); every health or role claim is a lead for Sunday's two-outlet verification.
Gate: `check_provenance.py` → PASS (verified 2026-07-13 .. 2026-10-07), exit 0.

## 1. Roster changes

None — an intake.

## 2. The intake

| measure | value |
|---|---|
| rows | 150 (rounds 1–13), every line parsed, every team mapped to a kit code; ranks contiguous |
| join | 150 of 150 names have a pool row; no spelling variant; 0 team mismatches against the kit |
| agreement with the kit board | Spearman ρ .779; median gap 22 places; 128 of the panel's 150 sit inside our top 150 |
| agreement with Yahoo's market | the panel vs Yahoo's XRank ρ .949 (our board vs XRank .787) — the panel ranks the room more than it ranks the categories |
| notes | 36 rows carry a health word, 35 a role word (`rotowire-parse-2026-10-09.md`) |
| our top-150 names the panel leaves out | 22, nine of them off our boards already (Butler, Lively, Mark Williams, Sharpe, Thomas, Konchar-class exclusions) or deep-bench names (Goodwin, Ellis, Pippen Jr.); the rest are the late-round steals men the board likes (Herb Jones, Coulibaly, Tre Jones, Caruso, Nesmith, Filipowski, Vucevic) |

## 3. Where the panel and the board disagree by 20 or more places

The disagreements are the board's known values and fades, with the same nine-column reasons as the owner's gap
explanation earlier today (the board column is the kit's; the deck orders the same players the same way).

**The board is higher (32 names; the largest):**

| player | our # | panel # | the panel says | the board's nine-column reason |
|---|---|---|---|---|
| Kristaps Porziņģis | 48 | 128 | "cleared 65 games twice in his career … not at Warriors training camp" | blocks +1.49, turnovers +0.59; vetoed by the owner on 9/28, the card never shows him |
| Dyson Daniels | 9 | 69 | "the steals are still the point … no 3s and a weak free-throw line" | steals +5.44, the largest single category score on the board; the line is first on Sunday's anchor |
| Joel Embiid | 22 | 66 | "when he plays he wins categories outright … high-variance swing" | FT% and points elite; the 0.78 haircut already applied |
| Zach LaVine | 72 | 122 | "missed 108 games in three years and could be traded into a smaller role" | threes +1.32, points +0.96, nothing below −1.03 |
| Fred VanVleet | 75 | 125 | "32-year-old guard coming off a torn ACL into a crowded backcourt" | steals +1.44, assists +0.82, turnovers +0.59; haircut applied |
| Kyrie Irving | 17 | 42 | "a strong category-league riser … coming off an ACL tear at 34" | FT% +1.67, threes +1.00, points +1.36, nothing negative; haircut applied |
| Kawhi Leonard | 12 | 37 | "a clean bill of health last season cuts against a decade of evidence" | steals and points; haircut applied |
| Chet Holmgren | 10 | 30 | "a category-league player … the raw counting totals are ordinary" | blocks +3.23, turnovers +0.73 — the panel's own reason, priced |
| Darius Garland | 24 | 47 | "recent injury issues create some downside risk" | assists and threes; no health note on his row — a lead (§4) |
| Nic Claxton, Jrue Holiday, Mamukelashvili, Lendeborg, P.J. Washington, Braun, Reed, Gordon, Hart, Jerome, Gillespie, Sheppard, Wallace, Allen, Bey, Cam Johnson, George, Mitchell, Bridges, Powell, Camara, Sharpe, Collins | 48–115 | 80–147 | role or minutes doubts in most notes | low-usage efficiency with steals or blocks and no leak; the late-round profile the board prefers |

**The panel is higher (52 names; the largest):**

| player | our # | panel # | the panel says | the board's nine-column reason |
|---|---|---|---|---|
| Stephon Castle | 181 | 63 | "a category-league faller … shooting efficiency and turnovers" | the panel agrees on the categories and still ranks him 118 places higher; our line is the 10/7 re-derivation |
| Jaylen Brown | 135 | 44 | "better in points leagues" | FG% −0.53, FT% −0.41, blocks −0.64, turnovers −1.02 |
| LeBron James | 141 | 54 | "what will his minutes, role and games played actually look like?" | haircut applied; FT% and turnovers negative |
| Paolo Banchero | 130 | 49 | "field-goal percentage mediocre, free-throw line inconsistent, turnovers heavy" | the panel's reasons, priced: FT% −1.47, turnovers −1.56 |
| Giannis Antetokounmpo | 59 | 10 | "force you to punt or pair carefully … build the roster around the punt" | FT% −5.42, threes −1.56, turnovers −1.56 against four elite columns |
| Alperen Sengun | 57 | 22 | "the turnovers are heavy and he gives you nothing from 3" | the panel's reasons, priced: FT% −1.82, threes −1.35, turnovers −1.02 |
| Scottie Barnes | 35 | 11 | "the free-throw percentage and the low 3-point volume are the drags" | FG% −0.87, FT% −0.59, turnovers −1.15, nothing elite |
| Kon Knueppel | 105 | 51 | "unclear if he'll be ready to start the season due to a hamstring issue" | a modest projected line; the hamstring is on his row since 9/25 |
| Matas Buzelis | 79 | 43 | "potential for both more minutes and development" | the ceiling priced, not the line; assists −1.04, steals −0.84 |
| Dylan Harper, Acuff, Dybantsa, Queen, Fears, Dëmin, Maluach, Mikel Brown, Caleb Wilson, Peterson | 119–254 | 76–149 | rookies and sophomores, "rookie inefficiency and turnovers are charged at full price" | the panel says it and ranks them anyway; the board prices the line |
| Isaiah Jackson, Jaquez Jr., Queta, Porter Jr., Dosunmu, Black, DeRozan, Davion Mitchell, Hachimura | 156–289 | 87–146 | role claims: a starting job, a sixth-man role, an open rotation | low per-game lines on our rows; the role claims are leads (§4) |

## 4. The health and role notes against the pool (leads, not facts)

Thirty-six rows carry a health word and 35 a role word. Nearly all are already on the pool rows with dated receipts:
Knueppel's hamstring (9/25), Claxton's hamstring (10/4–5, CBS), Coby White's calf (10/6), Porziņģis out pre-camp, Ingram's
partially torn Achilles (kit GP 48, haircut), Mikel Brown's ankle sprain, Maluach's preseason minutes, Isaiah Jackson on
the Clippers' first unit in camp, Hartenstein and Jalen Williams held out on 10/6, Markkanen's neck, and every
Achilles-return tag (Tatum, Haliburton, Lillard, Dejounte Murray, Irving's ACL, VanVleet's ACL). Mark Williams and
Lively are already excluded.

New leads written into WO-5 item (9) for Sunday's two-outlet check: Garland's "recent injury issues" (no note on his
row); Poeltl's back (46 games last season) against our 66; Gafford as Dallas's starting center with Lively out (our
10.5 / 7.5 / 1.7 line is a backup's); Hachimura as the Clippers' second option with Ingram out; Durant's rest days
against our 62 games. None of these moves a row today.

## 5. What the panel says about the owner's own notes

| player | our # (kit / deck) | panel # | the panel says | read |
|---|---|---|---|---|
| Anthony Davis | 5 / 5 | 23 | "Twenty games last year … pair him with durable pieces and take the swing" | the same view as the owner's: a first-round line when he plays; the panel discounts harder than the 0.78 |
| Kyrie Irving | 17 / 15 | 42 | "a strong category-league riser … elite percentages, 3s, steals, low turnovers" | agrees with the board on the profile, prices the ACL |
| Cooper Flagg | 14 / 22 | 8 | "Kyrie Irving's return should raise the quality of his shots without eating many of them" | the owner's synergy view, in the panel's words; our FT% and points are on Sunday's review |
| Dyson Daniels | 9 / 11 | 69 | "the steals are still the point … no 3s and a weak free-throw line" | the panel prices the two leaks the owner saw (threes, FT%) and the Alexander-Walker / Dort usage question by rank, not by note |
| Chet Holmgren | 10 / 10 | 30 | "blocks and 3s from a center … the raw counting totals are ordinary" | no regression or Mara note; the panel's rank is the points-league reflex the owner named |
| Jaren Jackson Jr. | 23 / 23 | 36 | "blocks and 3s … the field-goal percentage and the foul trouble are the recurring problems" | no shutdown note; the owner's playoff-weeks risk stays his |
| Kristaps Porziņģis | 48 / 39 | 128 | "not at Warriors training camp as he deals with health issues" | the owner's veto, confirmed by the panel's rank |
| Desmond Bane | — / 27 | 57 | "high-volume 3-point shooting … steals and low turnovers. Role cemented as Orlando's No. 3 option" | the panel sees the peripherals the owner doubted: steals and low turnovers, not only scoring |
| Tyler Herro | — / 43 | 60 | "the most turnovers of his career, and he gives you nothing defensively" | the panel's doubt matches the owner's; the board still prices the threes and free throws |
| Zach LaVine | 72 / 56 | 122 | "missed 108 games in three years and could be traded into a smaller role" | the owner's health and age doubt, in the panel's words |
| Alperen Sengun | 57 / 69 | 22 | "the turnovers are heavy and he gives you nothing from 3" | the panel names the leaks and ranks him 22nd anyway; the board does not |

## 6. Gates (2026-10-09, the RotoWire intake)

| gate | result |
|---|---|
| kit `report/market/rotowire_text.py` | TRANSCRIPTION GATE: PASS — 150 rows, ranks contiguous, every line parsed; stamped at e06087c |
| kit `report/market/third_party_market.py rotowire` | GATE PASS — 150 of 150 matched, 0 spelling variants, 0 team mismatches; stamped at 6098459 |
| kit `report/check_derived.py` | DERIVED: all 21 dated artifacts reproduce byte-for-byte; exit 0 |
| kit `report/check_provenance.py` | PASS — all rows sourced; exit 0 |
| kit `report/check_report.py` | REPORT GATE: PASS (structure, publication rule, pull-log row); exit 0 |
| deck `judgment_open_items.py --check-report` | receipts check PASS — all 10 flagged names carry a receipts row; exit 0 |
| deck `repeat_market_check.py --check-report` | REPEAT-NAME CHECK: PASS — 12 flagged names, each with a row (21 of 21 mocks replayed on the v53 page); exit 0 |

## 7. Watchlist / open items

- **Sunday 10/11** — WO-5 item (9): the five new leads on two outlets; the rows already carrying a note re-dated with
  the day's receipts.
- **10/13** — the panel's rank beside each of the owner's named players in the bigger-picture assessment (§5 is the
  first cut).
- Everything carried from the day's three earlier reports stands.

## Open-item receipts

| player | query run (2026-10-09) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (`after-report-2026-10-09.md`, receipts dated 10/9); the panel's notes on Ingram (Achilles, "return timetable is unclear"), Porziņģis (not at camp), Leonard (health history), Mathurin (NOP arrival), Rollins (role murky) are single-outlet leads consistent with the rows | all HELD or unsigned on 2026-10-09; this intake did no roster research |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 8978f6cde216), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 21 of 21 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-09.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-06.csv`, `hashtag-2026-10-09.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| PJ Washington | 17 of 21 | 87 | 151 | 178 | 144 | 141 | 121 | ast 2.4 vs 1.9-2; tov 1.5 vs 1.7-1.8; fg_pct .470 vs .448-.451; ft_pct .750 vs .698-.703 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Payton Pritchard | 16 of 21 | 37 | 83 | 33 | 90 | 92 | 72 | stl 1 vs 0.7-0.8; tpm 3.8 vs 3-3.2; tov 2 vs 1.3-1.3; ft_pct .850 vs .873-.875 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 15 of 21 | 28 | 65 | 60 | 56 | 43 | 44 | pts 18.5 vs 16.4-17; ast 2.3 vs 2.1-2.1; ft_pct .805 vs .813-.819 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Sandro Mamukelashvili | 15 of 21 | 81 | 169 | 138 | 105 | 153 | 120 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Daniel Gafford | 10 of 21 | 90 | 181 | 188 | 180 | 161 | 155 | pts 10.5 vs 9.1-9.8; reb 7.5 vs 5.8-6.5; ast 1.5 vs 1.1-1.2; blk 1.7 vs 1.2-1.4; fg_pct .700 vs .648-.689; ft_pct .700 vs .671-.687 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Jalen Suggs | 10 of 21 | 59 | 105 | 89 | 54 | 84 | 99 | pts 17 vs 14.1-15.1; ast 4 vs 4.8-5 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 9 of 21 | 82 | 144 | 94 | 121 | 137 | 98 | reb 7.5 vs 5.5-6.9; tpm 0.9 vs 1.2-1.3; fg_pct .520 vs .447-.498; ft_pct .740 vs .765-.828 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Isaiah Hartenstein | 7 of 21 | 75 | 104 | 141 | 92 | 100 | 102 | pts 11.5 vs 9.1-10.5; reb 11 vs 9.2-10.3; fg_pct .585 vs .597-.611; ft_pct .680 vs .642-.656 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Zach LaVine | 6 of 21 | 56 | 100 | 162 | 68 | 77 | 118 | pts 22.5 vs 17-21.1; reb 4.5 vs 3.1-3.6; ast 4 vs 2.8-3.4; tov 2.6 vs 2-2.4 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 5 of 21 | 89 | 142 | 122 | 131 | 125 | 123 | pts 16.8 vs 13.4-15.1; tov 1.5 vs 1-1.2; fg_pct .465 vs .432-.443 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Dyson Daniels | 5 of 21 | 11 | 62 | 20 | 64 | 56 | 53 | pts 14.5 vs 11.3-11.8; stl 3 vs 2-2.4; tpm 1.1 vs 0.5-0.6; fg_pct .495 vs .501-.513 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Saddiq Bey | 5 of 21 | 95 | 176 | 109 | 132 | 169 | 143 | blk 0.4 vs 0.1-0.1; tpm 2.4 vs 1.8-2; tov 1.5 vs 0.8-0.9 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Karl-Anthony Towns (16 mocks, value 6, market 15); Jalen Williams (15 mocks, value 16, market 39); Derrick White (11 mocks, value 24, market 44); Jalen Johnson (6 mocks, value 13, market 11); Mikal Bridges (6 mocks, value 61, market 82).

Reproduced from `after-report-2026-10-09-market.md` (the v53 page); this intake ran no replay of its own.

## Bounds

**Out of scope by design:** the panel's prose was not fact-checked claim by claim today (each claim is a lead for the
pull's two-outlet rule, not a fact in the record); the panel's ranks are not blended into the board (a single outlet;
the market-blend test of 10/08 rejected rank blending on evidence).

**In scope and unverified:** the five new leads (NOT-ATTEMPTED today, scheduled Sunday); whether the panel's "faller"
and "riser" calls add signal beyond Yahoo's market (its .949 correlation with XRank says most of its ordering is the
room's; NOT-ATTEMPTED as a measurement).

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-1009-10 | the repeat-name check's outside ranks: (a) add the RotoWire panel as a fifth outside rank at the 10/13 pass (a flagged line then needs 25+ places on four of five); (b) keep the four | (a) at 10/13 — one more named outlet with a 9-cat view |

## Provenance and bounds

- Inputs: the owner's paste (`report/market/rotowire-raw-2026-10-09.txt`); the kit board and pool; `yahoo-2026-10-09.csv`.
- Records: `rotowire-raw-2026-10-09.csv`, `rotowire-parse-2026-10-09.md`, `rotowire-2026-10-09.csv`,
  `unmatched-rotowire-2026-10-09.md`, `disagreements-rotowire-2026-10-09.md`, `provenance.csv` (row merged).
- Every number in §2 and §3 is the intake scripts' output; the quotations in §3 and §5 are the panel's words from the
  pinned text.

## In plain language

**What this is.** A panel of RotoWire's experts ranked 150 players for nine-category leagues with a sentence on each
about role, health and situation. I pinned the article, read every line by script, matched all 150 names to our pool,
and compared their order with ours and with Yahoo's room.

**What it says about us.** Their list agrees with Yahoo's draft room far more than with our board (.95 against .78), so
it is mostly a well-reasoned market list. Where they differ from us, they differ for the reasons we already know and
have priced: they rank Giannis, Sengun, Barnes and Banchero high while naming the free-throw, three-point and turnover
leaks that hold them down on our board; they rank Daniels, Porziņģis, Irving, Holmgren and the late-round steals men
low while naming the very categories that lift them for us. On your own notes, they side with you on Davis's swing,
Irving's profile, Flagg-with-Irving, Herro's defensive hole and LaVine's health, and they see in Bane the steals and
low turnovers the board sees.

**What changes.** No ranking. Five of their health and role remarks were not yet on our rows (Garland, Poeltl, Gafford,
Hachimura, Durant's rest days) and are now on Sunday's checklist to be confirmed by two sources before anything moves.
One decision for you: whether their ranks join the four outside sources the repeat-name check uses from 10/13 (default
yes).
