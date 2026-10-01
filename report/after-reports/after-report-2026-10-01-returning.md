# After-report — 2026-10-01 returning-from-injury intake: NBC Sports' top twelve via Yahoo, checked against the records

**Owner request (2026-10-01, verbatim):** "Here is Injury returning players
profile projections from Yahoo:" — the twelve-player column (games missed,
injury, availability, a role claim each), pasted after the daily pull.

Pull window: 2026-10-01 → 2026-10-01 (intake, not a roster pull; the 10/01
pull-log row covers the window). The piece is NBC Sports' fantasy column
"2026-27 Fantasy Basketball: Kyrie Irving, Tyrese Haliburton among big names
returning from injury", syndicated on Yahoo Sports (the NBC Sports result of
that title surfaced on 10/01; nbcsports.com is egress-blocked, so the byline
and date were not read). One outlet.

**Method.** The piece was transcribed verbatim to
`report/market/returning-raw-2026-10-01.csv` (12 rows) with a provenance
row. Every games-missed figure was checked against Basketball-Reference's
2025-26 game log (eight fetched on 10/01; the four 82-game absences were not
fetched), every price claim against the kit's 9/22 Yahoo file, every injury
label and availability claim against both planes' tags and notes and, where
the piece and the pool disagreed, against two further outlets. Rank effects
of the games-line questions were measured with scratch runs of the kit
engine and the deck's own ranking (`scratchpad pull1001/`). Verification:
this file passes `report/check_report.py`; receipts below.

**Headline.** The column's arithmetic is right and its labels are not all
right. All eight games-missed figures that could be checked reconcile to the
game logs exactly (Morant 20, Giannis 36, Sabonis 19, Tatum 16, Murray 14,
Edey 11, Lively 7, Kessler 5), and every price claim reconciles to the 9/22
Yahoo file (Morant's "eighth round" is ADP 91.8, Murray's "late sixth" 71.1,
Tatum's "top-10" 10.4). Two injury labels fail the claim-check: Giannis's
"Achilles" is a calf-strain-and-knee-hyperextension season with no
structural damage and a full-go camp (ESPN, Yahoo, Hoops Rumors, NBA.com;
RotoWire, CBS Sports), and Sabonis's "Back, Knee" is a torn left meniscus
with season-ending surgery (ESPN, NBC Sports Bay Area, ClutchPoints). The
pool already carries ten of the twelve at the risk tier; the two untagged
names are the two the column mislabels. No pool row changed today: the
games-line questions the column raises move no kit rank (Kessler sits 37th
at 72, 64 or 58 games; Lively 114th at 56 or 25; Giannis 59th at 67 or 60)
and the one deck effect — Giannis 44 → 47 at the risk tier — is the owner's
call (D-RT1). The one standing tension is Lively: not cleared nine months
after a second foot surgery, timeline unclear, which is the state the pool
calls a recovery exclusion (the Steven Adams precedent) while three pulls
have kept him at the risk tier (D-RT3).

## 1. The twelve, claim by claim

Played = Basketball-Reference 2025-26 game-log totals (fetched 10/01) unless
marked; "82 missed" rows were not fetched — both planes already carry them
as first-season-back returnees.

| # | player | piece: missed / injury / availability | played (record) | kit GP · rank | deck tag · rank | piece's price claim vs 9/22 file | verdict |
|---|---|---|---|---|---|---|---|
| 1 | Kyrie Irving | 82 / ACL / full go | 0 (not fetched) | 60 · 17 | `inj-acl-risk` · — | none (ADP 52.1) | consistent |
| 2 | Tyrese Haliburton | 82 / Achilles / full go | 0 (not fetched) | 60 · 26 | `inj-achilles-risk` · — | "first-round upside" (ADP 17.8) | consistent |
| 3 | Damian Lillard | 82 / Achilles / full go | 0 (not fetched) | 45 · 92 | `inj-achilles-risk` · — | "later rounds" (ADP 69.4, sixth round) | consistent on health; the price claim is looser than the file |
| 4 | Ja Morant | 62 / ankle, calf, elbow / full go | 20 | 60 · 139 | `inj-risk` (added 10/01) · 68 | "eighth round, picks 85–100" (ADP 91.8, XRank 103) | SUPPORTED |
| 5 | Fred VanVleet | 82 / ACL / minutes restriction possible | 0 (not fetched) | 55 · 76 | `inj-acl-risk` · 69 | "late-round PG" (ADP 119.5) | consistent; today's note already carries the minutes caveat (D-BV2) |
| 6 | Zach Edey | 71 / ankle / recovering, on track for the opener | 11 | 70 · 66 | `inj-ankle-risk` · — | "mid-round ADP" (74.1) | SUPPORTED; the frontcourt-competition claim is noted (Stewart, Post, Boozer) |
| 7 | Walker Kessler | 77 / shoulder / full go | 5 | 72 · 37 | `inj-shoulder-risk` · 45 | "fourth round range" (ADP 36.2) | SUPPORTED; kit games question D-RT2 |
| 8 | Dereck Lively II | 75 / foot / timeline unclear | 7 | 56 · 114 | `inj-risk` · 132 | "deep leagues only" (no ADP; XRank 175) | SUPPORTED; Ujiri's "patient" quote confirmed (RotoWire, Yardbarker) — exclusion question D-RT3 |
| 9 | Jayson Tatum | 66 / Achilles / full go | 16 | 65 · 18 | `inj-achilles-risk` (+0.35 card) · — | "top-10 pick" (ADP 10.4, XRank 8) | SUPPORTED |
| 10 | Domantas Sabonis | 63 / back, knee / full go | 19 | 70 · 20 | untagged (D-S8) · 24 | none (ADP 29.5) | PARTIAL — the record is a torn left meniscus and season-ending surgery (§2); the "may be moved by the rebuilding Kings" line is the column's alone [SINGLE-SOURCE] |
| 11 | Dejounte Murray | 68 / Achilles / full go | 14 | 62 · 75 | `inj-achilles-risk` · — | "late sixth-round ADP" (71.1) | SUPPORTED |
| 12 | Giannis Antetokounmpo | 46 / Achilles / full go | 36 | 67 · 59 | untagged · 44 | "first-rounder" (ADP 8.5) | UNSUPPORTED on the injury label (§2); availability claim SUPPORTED |

## 2. The two labels that fail the claim-check

- **Giannis — not an Achilles.** The 2025-26 record is repeated right-calf
  strains (NBA.com's calf-injury items; the AOL/AP "questionable for the
  Celtics game as he seeks to return from calf strain") and a left knee
  hyperextension with a bone bruise on March 15 that ended his season at 36
  games, with imaging showing no structural damage (ESPN, Yahoo, Hoops
  Rumors, Yardbarker, Brew Hoop). At Heat camp he is a full go with no
  limitations (RotoWire, CBS Sports, Bleacher Report). The column's 28.9
  minutes and 36 games are right; its injury label is wrong in kind. The
  pool's untagged row is therefore not a missed Achilles returnee under F6;
  whether a 36-game soft-tissue season earns the chronic `inj-risk` tier is
  D-RT1.
- **Sabonis — a knee, with surgery.** Nineteen games; a left-knee meniscus
  tear cost him 27 games from November to January, he returned January 16,
  was in and out with soreness, and had season-ending surgery in
  mid-February (ESPN, NBC Sports Bay Area, ClutchPoints, Blazer's Edge). No
  outlet checked mentions a back injury. His untagged row is owner decision
  D-S8 (2026-09-08: meniscus, a different injury class from the Achilles
  returnees) and yesterday's sweep had him ready for camp after skipping
  Lithuania's qualifiers (Sactown Sports, SI Kings); nothing here reopens it.

## 3. What the pool does with the column

Nothing today. The column is one outlet; its checkable claims either match
the records and the pool, or raise games-line questions whose rank effects
were measured and found nil on the kit:

| question | scratch measurement | owner item |
|---|---|---|
| Kessler's kit games (72) against 5 and 58 played the last two seasons | kit rank 37 at 72, 64 and 58 games | D-RT2 |
| Giannis at the deck's risk tier | deck 44 to 47 (adjusted value 0.77 to 0.60); kit rank 59 at 67 or 60 games | D-RT1 |
| Lively as a recovery exclusion | kit rank 114 at 56 or 25 games (negative composite); deck 132, and an exclusion removes him from the owner's candidate pool | D-RT3 |

Deck notes recording why Giannis is untagged, Lively's twice-repaired foot
and Ujiri's quote, Kessler's five games and Sabonis's nineteen ride the next
daily pull (D-RT5), which rebuilds the deck anyway.

## Watchlist

- **Lively** — a clearance or a ruled-out opener decides D-RT3; the Mavericks
  open 10/21 against Houston.
- **Giannis** — any calf or knee item in preseason reopens D-RT1.
- **Kessler** — first preseason minutes as the Lakers' starting center.
- **Edey** — the Stewart / Post / Boozer frontcourt share in preseason.
- **Sabonis** — a trade would reprice the row; nothing sourced beyond the
  column's speculation.

## Open-item receipts

| item | query run (2026-10-01) | dated finding |
|---|---|---|
| (the column) | Yahoo fantasy basketball top returning from injury players 2026-27 … · nbcsports.com fetch | NBC Sports' column, syndicated on Yahoo; nbcsports.com blocked (one fetch, EGRESS_BLOCKED) |
| Giannis Antetokounmpo | Giannis Antetokounmpo Achilles injury 2025-26 games played status Heat training camp 2026 · Giannis Antetokounmpo calf strain knee hyperextension March 2026 36 games Bucks season · B-Ref game log (fetched) | 36 GP, 28.9 mpg; calf strains; knee hyperextension + bone bruise 3/15, no structural damage — ESPN, Yahoo, Hoops Rumors, NBA.com; full go at camp — RotoWire, CBS Sports, Bleacher Report |
| Domantas Sabonis | Domantas Sabonis 2025-26 back knee injury games played Kings training camp 2026 healthy · B-Ref game log (fetched) | 19 GP; torn left meniscus, season-ending surgery mid-February — ESPN, NBC Sports Bay Area, ClutchPoints |
| Dereck Lively II | Dereck Lively Masai Ujiri "patient" Mavericks foot recovery 2026 · B-Ref game log (fetched) | 7 GP; right foot repaired twice in 14 months; shooting → running; "being patient with D-Live" — RotoWire, Yardbarker; not cleared for camp — ESPN |
| Walker Kessler | B-Ref game log (fetched) | 5 GP, 31.0 mpg, 14.4 / 10.8 / 3.0 / 1.8 blk / 1.2 3PM |
| Zach Edey | B-Ref game log (fetched) | 11 GP, 25.8 mpg, 13.6 / 11.1 / 1.9 blk / .633 |
| Jayson Tatum | B-Ref game log (fetched) | 16 GP, 32.6 mpg, 21.8 / 10.0 / 5.3 / 2.9 3PM |
| Dejounte Murray | B-Ref game log (fetched) | 14 GP, 27.9 mpg, 16.7 / 5.4 / 6.4 / 1.6 stl |
| Ja Morant | (today's pull) B-Ref game log (fetched) | 20 GP, 28.4 mpg, 19.5 / 3.3 / 8.1 |
| (price claims) | report/market/yahoo-2026-09-22.csv (read) | §1, last column |
| Jalen Duren, Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the daily pull's dedicated queries, same day (after-report-2026-10-01.md, Open-item receipts) | all HELD on 2026-10-01; nothing in the column touches them |

## Bounds

- One outlet; its byline and date were not read (nbcsports.com blocked).
- The four 82-game absences were not fetched; both planes carry them as
  first-season-back returnees and the column agrees.
- Lively's "98 of 246 games in three seasons" was not checked beyond the
  2025-26 log (7 of 82).
- The rank sensitivities are the engines' own outputs on scratch copies;
  they say nothing about the weekly model, which does price games through
  the deck's availability tags.
- Whether Sabonis also had a back issue was not found in the outlets
  checked; the label is graded on what was found.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-RT1 | Giannis: 36 games on calf strains and a knee hyperextension, full go now, untagged on both planes (kit 67 GP). Tag `inj-risk` on the deck (44 to 47; the weekly model expects fewer games) and lower the kit line, or hold untagged on one bad soft-tissue season with no structural damage? | hold untagged; note at the next pull |
| D-RT2 | Kessler's kit games, 72 against 5 and 58 played: the board is insensitive (37 at 72, 64, 58). Lower to 64 for honesty? | hold 72 |
| D-RT3 | Lively: not cleared nine months after a second foot surgery, timeline unclear, "patient" — the state the pool calls a recovery exclusion (Adams was `ankle-recovery` until he was a full camp participant), yet three pulls kept `inj-risk`. Re-tag `foot-recovery` (deck excluded, kit GP 25 for the planes gate) at the next pull unless he is cleared, or keep him draftable at the risk tier? | re-tag at the next pull unless cleared |
| D-RT4 | Sabonis (D-S8, 2026-09-08): the column corroborates "full go"; the record is 19 games and a meniscus surgery, not "back, knee". Reopen D-S8? | no |
| D-RT5 | Deck notes for Giannis (why untagged), Lively (Ujiri, the twice-repaired foot), Kessler (five games) and Sabonis (nineteen, surgery) at the next daily pull? | yes |

## Provenance

- Inputs: the owner's paste (transcribed to `report/market/returning-raw-2026-10-01.csv`), eight Basketball-Reference game logs fetched 2026-10-01, four dated WebSearch summaries (2026-10-01), the kit's 9/22 Yahoo file, both planes' pools and boards as merged today.
- Every number in §1 and §3 is a fetched record or a script output (`scratchpad pull1001/sens/`, the deck ranking by `hoops.py`'s own functions).
- Not verified: nothing here rests on a direct read of a blocked sports domain.
