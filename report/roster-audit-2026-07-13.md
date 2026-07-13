# Roster-Accuracy Audit — Tm Field — 2026-07-13

**Trigger:** a three-player spot check of the Lakers cluster (Grimes, Hachimura,
Sexton) found all three `Tm` values wrong — treated as a signal of systemic
staleness, not an exhaustive list. **Scope:** verify the `team` field for all
220 rows of `projections-2026-27.csv` against live web sources; fix `Tm` only.
GP, stat lines, and percentages untouched (re-projection is October's job).
INPUTS.md untouched.

**Method:** every row verified against live research run 2026-07-13 —
current roster pages / team offseason trackers for unchanged players, dated
news articles (official team news, ESPN, beat writers preferred) required for
every correction, two sources wherever available. The most surprising
correction (Trae Young) was independently re-verified before applying.
No verdicts from training-data memory.

## Result summary

| | |
|---|---|
| Rows verified | 220 / 220 |
| Confirmed correct | 181 |
| **Corrected** | **39** (17.7% of the file) |
| Unconfirmed | 0 |
| Now team-less (FA/retired) | 9 |
| Tier moves after re-rank | **0** (see below) |

The corruption was not confined to one team cluster or one vintage: the file
missed **February-deadline trades** (McCain, Hunter, Mathurin, Hendricks,
Dillingham/Dosunmu, Trae Young from January), **June/July trades** (LaMelo
four-teamer, Claxton, Aldama, Stewart, O'Neale/Allen), **July free agency**
(Grimes, Sexton, Hachimura, Smart, Powell, Simons, Vučević, Robinson, Harris,
Collins, Bogdanović, Drummond), **waivers/option declines** (DeRozan,
Valančiūnas, Ivey, Kuminga, Draymond, Cam Thomas, Jalen Wilson, Sochan), and
one **retirement** (Chris Paul). Two rows were doubly stale — wrong even for
where the player finished 2025-26 (Sexton finished in CHI, not CHA; Drummond
in PHI, not LAC).

## Corrections applied (old → new)

| Player | Tm | Move | Source |
|---|---|---|---|
| Trae Young | ATL → **WAS** | Traded 2026-01-09 for CJ McCollum + Corey Kispert; re-signed 4yr/$212M July | [NBA.com](https://www.nba.com/news/hawks-trade-trae-young-to-wizards-for-cj-mccollum-corey-kispert) · [ESPN](https://www.espn.com/nba/story/_/id/49145221/sources-trae-young-sign-4-year-212m-deal-wizards) |
| LaMelo Ball | CHA → **MIN** | 4-team trade w/ Josh Green for Naz Reid + picks, official 2026-07-10 | [HoopsRumors](https://www.hoopsrumors.com/2026/07/wolves-hornets-nets-bulls-finalize-four-team-trade.html) |
| Julius Randle | MIN → **BKN** | Salary dump in the LaMelo four-teamer, 2026-07-10 | [ESPN](https://www.espn.com/nba/story/_/id/49175343/hornets-trade-ball-timberwolves-reid-picks) |
| Naz Reid | MIN → **CHA** | To Charlotte in the LaMelo four-teamer, 2026-07-10 | [ESPN](https://www.espn.com/nba/story/_/id/49175343/hornets-trade-ball-timberwolves-reid-picks) |
| Nic Claxton | BKN → **CHI** | To Bulls in the Randle/LaMelo deal (agreed draft eve, official 7/10) | [ESPN](https://www.espn.com/nba/story/_/id/49149223/sources-wolves-trade-randle-nets-claxton-bulls) |
| Kawhi Leonard | TOR → **LAC** | June 30 LAC→TOR trade **on hold** since 2026-07-09 pending NBA probe; Clipper of record | [NBA.com](https://www.nba.com/news/raptors-clippers-kawhi-leonard-trade-on-hold) |
| Anfernee Simons | CHI → **PHI** | UFA after deadline stint; 2yr/$12.3M with PHI, agreed 2026-07-02 | [ESPN](https://www.espn.com/nba/story/_/id/49250070/sources-anfernee-simons-agrees-deal-revamped-76ers) |
| Coby White | CHI → **CHA** | Deadline trade to CHA, then re-signed 3yr/$74M (2026-06-25) | [At The Hive](https://atthehive.com/2026/06/25/charlotte-hornets-to-re-sign-coby-white-to-three-year-deal/) · [hornets.com](https://hornets.com/news/after-seamless-adjustment-and-magic-moment-coby-white-signs-up-for-more-in-charlotte) |
| Ayo Dosunmu | CHI → **MIN** | Deadline trade (for Dillingham); re-signed 5yr/$112M, official 2026-07-10 | [ESPN](https://www.espn.com/nba/story/_/id/49150075/dosunmu-gets-5-year-112m-deal-timberwolves) |
| Rob Dillingham | MIN → **CHI** | Feb 2026 deadline, the other side of the Dosunmu swap | [NBA.com](https://www.nba.com/news/ayo-dosunumu-trade-wolves-bulls) |
| Norman Powell | MIA → **CHI** | 2yr/$45M with Bulls ~2026-07-01 (Giannis hard cap squeezed MIA) | [NBC Miami](https://www.nbcmiami.com/news/sports/miami-heat/heat-all-star-norman-powell-reportedly-agrees-to-2-year-deal-with-bulls/3828136/) |
| Rui Hachimura | LAL → **LAC** | 2yr/$28M with Clippers, official 2026-07-06 | [ESPN](https://www.espn.com/nba/story/_/id/49286926/rui-hachimura-clippers-agree-2-year-28m-deal) |
| Quentin Grimes | PHI → **LAL** | 4yr/$60M, agreed 2026-07-01, official 7/7 | [HoopsRumors](https://www.hoopsrumors.com/2026/07/lakers-to-sign-quentin-grimes-to-four-year-contract.html) |
| Collin Sexton | CHA → **LAL** | 2yr/$19M room exception, official 2026-07-12 (finished 2025-26 in CHI — row was doubly stale) | [HoopsRumors](https://www.hoopsrumors.com/2026/07/lakers-collin-sexton-agree-to-two-year-deal.html) |
| Marcus Smart | LAL → **HOU** | Opted out; 2yr/$13M with Rockets, 2026-07-01 | [HoopsRumors](https://www.hoopsrumors.com/2026/07/rockets-marcus-smart-agree-to-two-year-deal.html) |
| Bogdan Bogdanović | LAC → **HOU** | Option declined by LAC; 1yr minimum with HOU, official 7/8 | [ESPN](https://www.espn.com/nba/story/_/id/49233123/sources-rockets-agree-1-year-deal-bogdan-bogdanovic) |
| John Collins | LAC → **DET** | Sign-and-trade, 3yr/$51M, announced 2026-07-01 | [ESPN](https://www.espn.com/nba/story/_/id/49235613/sources-pistons-land-potential-starting-pf-john-collins) |
| Andre Drummond | LAC → **NYK** | 1yr/$3.9M agreed 2026-07-03 (spent 2025-26 in PHI — row was doubly stale) | [ESPN](https://www.espn.com/nba/story/_/id/49262566/andre-drummond-reaches-1-year-deal-new-york-knicks) |
| Mitchell Robinson | NYK → **BOS** | 3yr/$47.4M with Celtics, official 2026-07-06 | [NBA.com](https://www.nba.com/news/mitchell-robinson-celtics-free-agency-2026) |
| Nikola Vučević | BOS → **ORL** | 1yr/$3.9M vet-min reunion with Magic, 2026-07-01 | [ESPN](https://www.espn.com/nba/story/_/id/49236864/sources-nikola-vucevic-reuniting-magic-1-year-deal) |
| Santi Aldama | MEM → **DAL** | Traded 2026-07-01 for AJ Johnson + picks | [ESPN](https://www.espn.com/nba/story/_/id/49243066/sources-mavericks-add-7-footer-aldama-trade-grizzlies) |
| Isaiah Stewart | DET → **MEM** | Traded 2026-07-08 for three future seconds (within the 6-team Middleton S&T) | [ESPN](https://www.espn.com/nba/story/_/id/49170745/sources-pistons-trading-isaiah-stewart-grizzlies) |
| Taylor Hendricks | UTA → **MEM** | Feb 2026 deadline, part of the Jaren Jackson Jr package to UTA | [CBS](https://www.cbssports.com/fantasy/basketball/news/grizzlies-taylor-hendricks-traded-to-memphis/) · [NBA.com](https://www.nba.com/news/jaren-jackson-jr-trade-jazz-2026) |
| Tobias Harris | DET → **SAS** | 2yr/$31M with Spurs, 2026-07-01 | [Detroit News](https://www.detroitnews.com/story/sports/nba/pistons/2026/07/01/tobias-harris-signs-san-antonio-spurs/90773880007/) |
| Jared McCain | PHI → **OKC** | Feb 2026 deadline (for the pick that became Philon + three seconds) | [NBA.com](https://www.nba.com/news/thunder-sixers-jared-mccain-trade) |
| De'Andre Hunter | CLE → **SAC** | Feb 2026 three-team deal (Schröder, Ellis, Miller to CLE) | [ESPN](https://www.espn.com/nba/story/_/id/47793616/sources-cavs-trade-hunter-kings-schroder-ellis) |
| Bennedict Mathurin | IND → **LAC** | Feb 2026 Zubac deal; LAC tendered $8.77M QO — unsigned RFA, LAC of record | [HoopsRumors](https://www.hoopsrumors.com/2026/06/clippers-make-mathurin-miller-sanders-rfas.html) |
| Keon Ellis | SAC → **BKN** | Deadline trade to CLE, then 2yr/$18M with BKN, 2026-07-01 | [ESPN](https://www.espn.com/nba/story/_/id/49231668/sources-keon-ellis-agrees-2-year-18m-deal-nets) |
| Royce O'Neale | PHX → **CHA** | Traded w/ Allen + 2033 1st for Miles Bridges, agreed 2026-06-26 | [Arizona Sports](https://arizonasports.com/nba/phoenix-suns/suns-trade-grayson-allen-royce-oneale-miles-bridges-future-draft-picks) |
| Grayson Allen | PHX → **CHA** | Same Miles Bridges trade, 2026-06-26/28 | [NBA.com](https://www.nba.com/news/miles-bridges-trade-hornets-suns) |
| DeMar DeRozan | SAC → **FA** | Waived 2026-07-06 ($10M of $25.7M guaranteed); unsigned, LAC/MIA/DEN linked | [ESPN](https://www.espn.com/nba/story/_/id/49288211/sources-demar-derozan-cut-kings-hits-free-agency) |
| Jonas Valančiūnas | DEN → **FA** | Waived 2026-07-08 ahead of guarantee date; unsigned (EuroLeague possible) | [HoopsHype](https://www.hoopshype.com/story/sports/nba/rumors/2026/07/08/nuggets-waive-veteran-center-jonas-valanciunas/90854603007/) |
| Draymond Green | GSW → **FA** | Declined $27.7M option 2026-06-29; unsigned, expected to re-sign GSW | [SF Standard](https://sfstandard.com/2026/06/29/draymond-green-warriors-free-agent-options/) |
| Jonathan Kuminga | GSW → **FA** | Traded to ATL Feb 2026 (Porziņģis deal); ATL declined $24.3M option June — UFA | [NBC Bay Area](https://www.nbcbayarea.com/nba/golden-state-warriors/jonathan-kuminga-lakers-free-agency/4110207/) |
| Jaden Ivey | DET → **FA** | Traded to CHI 2026-02-03; waived by CHI 2026-03-30; unsigned | [Detroit News](https://www.detroitnews.com/story/sports/nba/pistons/2026/02/03/detroit-pistons-trade-jaden-ivey-in-three-team-deal-acquire-two-players/88494251007/) |
| Cam Thomas | BKN → **FA** | Waived by BKN Feb 2026; MIL rest-of-season deal ended; unsigned | [ESPN](https://www.espn.com/nba/story/_/id/47841532/sources-nets-waive-cam-thomas-making-free-agent) |
| Jalen Wilson | BKN → **FA** | BKN declined $3M qualifying offer (~2026-06-29) — UFA | [HoopsRumors](https://www.hoopsrumors.com/2026/06/2026-nba-qualifying-offer-recap.html) |
| Jeremy Sochan | SAS → **FA** | Waived by SAS 2026-02-11; NYK rest-of-season deal expired; unsigned | [ESPN](https://www.espn.com/nba/story/_/id/47901149/jeremy-sochan-waived-spurs-becomes-free-agent) |
| Chris Paul | LAC → **FA** | Traded to TOR 2026-02-04, waived, **announced retirement** Feb 2026 | [NBA.com](https://www.nba.com/news/chris-paul-announces-nba-retirement) |

## Needs manual review (step-4 flags)

**Priority 1 — projection void, row-level decision needed (9).** These players
have no team; their GP/stat rows describe a context that no longer exists.
Recommend deciding per row before October: re-project on signing, or zero out.

1. **Chris Paul — RETIRED.** Remove the row entirely.
2. **DeMar DeRozan (FA)** — waived by SAC; 20.5 ppg projection is teamless.
3. **Jonas Valančiūnas (FA)** — may not play in the NBA at all (EuroLeague reports).
4. **Jaden Ivey (FA)** — waived in March, unsigned; DET-context row void.
5. **Jonathan Kuminga (FA)** — GSW-context row doubly void (ATL stint + option decline).
6. **Draymond Green (FA)** — likely re-signs GSW, but not under contract today.
7. **Cam Thomas (FA)** — waived twice since Feb; 24 ppg row is fiction until he signs.
8. **Jalen Wilson (FA)** — QO declined.
9. **Jeremy Sochan (FA)** — off SAS since February.

**Priority 2 — team corrected, role/minutes context stale (30).** The stat
lines still assume the OLD situation; October's re-projection should treat
these as role-changed players (per-36 rebuild), not blends:

- **Upgraded/expanded roles:** Naz Reid (6th man → likely CHA starter),
  Mitchell Robinson (NYK backup → BOS frontcourt), John Collins (starting PF
  DET), Coby White (CHA starting PG post-LaMelo), Taylor Hendricks (career-best
  run in MEM), Isaiah Stewart (MEM frontcourt), Tobias Harris (SAS).
- **Squeezed/downgraded roles:** Marcus Smart (LAL starter → HOU reserve),
  Bogdan Bogdanović (crowded HOU backcourt), Andre Drummond (backup behind
  KAT), Jared McCain (bench on loaded OKC), Vučević (backup behind Wendell
  Carter), Julius Randle (rebuilding BKN), Grimes/Sexton (LAL backcourt
  shares), Hachimura (LAC frontcourt), Aldama (DAL), O'Neale + Allen (CHA),
  Powell (CHI), Simons (PHI third-guard), Keon Ellis (BKN), Dosunmu (MIN),
  Dillingham (CHI, plus reported minor offseason surgery), Claxton (CHI).
- **Usage re-anchored:** Trae Young (WAS lead guard — arguably up),
  LaMelo Ball (shares MIN backcourt with Edwards — likely down).
- **Unresolved:** Kawhi Leonard (LAC of record; TOR trade on hold pending NBA
  probe — 35-GP placeholder stays placeholder), Bennedict Mathurin (unsigned
  LAC RFA), De'Andre Hunter (returning from season-ending eye surgery, SAC
  crowded by Acuff).

## Tier movement after re-running rank_engine.py

**0 players moved tiers; 0 entered or left the top 200.** This is by
construction, not an anomaly: the engine's z-scores are computed from the
per-game stat columns and GP only — `team` is a display label in the output
table. Since this pass corrected `Tm` and nothing else (per scope), the
rankings are numerically identical; only the Tm column of the board changed.
The real ranking impact of these 39 moves arrives when October's re-projection
updates minutes/usage for the flagged rows above.

## Baseline prose corrections applied

Per the task, only sentences in `baseline-2026-07.md` stating a team
affiliation corrected above were touched: Trae Young (§3 tier list, §7 ATL
capsule), LaMelo Ball (§3 tier list, §7 CHA capsule), Anfernee Simons (§4
breakout table, §7 CHI capsule), Vučević (§7 BOS + CHI capsules), Randle/
LaMelo (§7 MIN capsule), Ivey (§7 DET capsule), Mathurin (§7 IND capsule),
Powell (§7 MIA capsule), McCain (§7 PHI capsule), O'Neale (§7 PHX capsule),
DeRozan (§7 SAC capsule). Historical ledger rows describing February-deadline
events as events (e.g., "Vučević → BOS for Simons → CHI") were left intact —
they were true when they happened; only current-affiliation statements were
corrected.

## Observations (not acted on — flagged for the October run)

- **The July baseline itself missed the January Trae Young trade** — its §3
  tiers and ATL capsule had him in Atlanta while also listing McCollum (the
  trade return) as a Hawk. Mixed-vintage data, same failure mode as the CSV.
- **Baseline CHA capsule lists Mark Williams as CHA** with a `[VERIFY roster]`
  tag; verified today he is PHX (CSV already said PHX, so no CSV correction —
  and per scope the capsule sentence was left, flagged here instead).
- **James Harden** declined his $42.3M option 6/29; a new multiyear CLE deal
  is agreed-but-unsigned as of 7/13. Kept CLE (team of record by agreement);
  watch for the signing.
- **Fred VanVleet** missed all of 2025-26 (ACL) and **Jimmy Butler** is
  reportedly out until ~Dec 2026 (Jan ACL tear) — their GP columns (55 each)
  are re-projection matters, out of scope here but load-bearing for the board.
- **JJJ → UTA held up** — the baseline's `[VERIFY destination]` resolved as
  the CSV had it (deadline deal: JJJ/Konchar/Landale/V. Williams for Clayton,
  Anderson, Hendricks, Niang, 3 FRPs).

## Source-dating note

All 39 corrections cite dated articles; 30 are dated within the 30-day window
(≥ 2026-06-13). The remaining 9 concern February–March events (deadline
trades, waivers, the Paul retirement) whose *event* coverage is older by
nature — each was corroborated with a within-window or accessed-today source
confirming the player's current status (July roster pages, QO recaps, July
free-agency coverage). Confirmed-OK rows cite current roster pages/offseason
trackers accessed 2026-07-13 or dated June–July articles.

---

*Audit run 2026-07-13 (Claude Code). Verification fleet: 10 parallel research
agents, 3 teams each; every row required a source, corrections required dated
articles; results validated for 220/220 coverage and cross-agent consistency
(both sides of every multi-team trade corrected independently) before apply.*
