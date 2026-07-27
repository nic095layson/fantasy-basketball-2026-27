# Draft Kit Data Pull — After Report

**Run date:** 2026-07-27 · **Window swept:** 2026-07-13 → 2026-07-27 (last full verification was the 7/13 roster audit, commit `5c75e98`)
**Scope:** delta pull — news since 7/13, not the full October Pass A–F re-verification (that run is still owed in October per PROMPT.md §7).

```
📋 Freshness Check — 2026-07-27
✓ Verified: all 5 team changes, 2 pool removals, 2 pool additions, 9 FA statuses,
  16 targeted injury checks, Kawhi trade status — every claim below carries a dated source
⚠ Changes since 7/13: 10 rows edited/added/removed in projections CSV (detail below)
✗ Cannot verify: Mark Williams' current foot status; Trey Alexander SL injury severity;
  Kuminga's GSW-vs-ATL rights discrepancy (single source)
```

---

## 1. Roster changes applied to the CSV (all [CONFIRMED], 2+ sources unless noted)

| Player | Change | Date | Sources |
|---|---|---|---|
| **LeBron James** | Signed PHI, 2yr/$8M — **added to pool** at rank #121 | 7/24 (official 7/26) | [ESPN](https://www.espn.com/nba/story/_/id/49440164/lebron-chooses-76ers-sign-2-year-8-million-contract), [Yahoo](https://sports.yahoo.com/nba/breaking-news/article/lebron-james-signing-2-year-8m-deal-to-join-76ers-for-his-24th-nba-season-153616566.html), [NBC Philly (official)](https://www.nbcsportsphiladelphia.com/nba/philadelphia-76ers/lebron-james-sixers-official-signing-mike-gansey/743927/) |
| **Lu Dort** | OKC → ATL (3-team trade) — team label only, stats unchanged, role-staleness flag | 7/19 | [ESPN](https://www.espn.com/nba/story/_/id/49400155/thunder-send-dort-hawks-three-team-trade-sources-say), [Yahoo](https://sports.yahoo.com/nba/breaking-news/article/thunder-trade-lu-dort-to-hawks-former-no-1-pick-zaccharie-risacher-heads-to-mavericks-in-3-team-deal-160558826.html) |
| **Zaccharie Risacher** | ATL → DAL (same trade) — team label only, role-staleness flag | 7/19 | same two |
| **Jonas Valanciunas** | Signed Zalgiris Kaunas (EuroLeague, 2yr) — **removed from pool** | 7/15 | [NBC Sports](https://www.nbcsports.com/fantasy/basketball/player-news/2026-07-15/jonas-valanciunas-leaves-nba-signs-with-zalgiris), [ESPN](https://www.espn.com/nba/story/_/id/49369108/jonas-valanciunas-joins-zalgiris-14-seasons-nba) |
| **Chris Paul** | Retired 2026-02-13 — **removed from pool.** Pre-existing defect: the 7/13 board ranked a retired player #150 with a 55-GP projection; his own provenance row cited the retirement announcement | 2/13 | [NBA.com](https://www.nba.com/news/chris-paul-announces-nba-retirement), [HoopsRumors](https://www.hoopsrumors.com/2026/02/chris-paul-announces-retirement.html) |
| **Miles Bridges** | CHA → PHX trade official 7/13 — **added to pool** at #125 (see A3 below: he was missing from the 220 entirely) | 7/13 | [ESPN](https://www.espn.com/nba/story/_/id/49208142/sources-hornets-trade-veteran-miles-bridges-suns), [AZFamily](https://www.azfamily.com/video/2026/07/13/phoenix-suns-trade-miles-bridges-becomes-official/) |
| **Jalen Wilson** | Signed ATL **two-way** — projection slashed (30 GP / 12 mpg); two-ways are barely draftable | 7/20 | [Hawks official](https://www.nba.com/hawks/news/atlanta-hawks-sign-forward-jalen-wilson-to-two-way-contract), [RealGM](https://basketball.realgm.com/wiretap/286764/Jalen-Wilson-Hawks-Agree-To-Two-Way-Deal) |

FA rows re-verified unsigned and provenance-refreshed (team label stays FA): **DeMar DeRozan** (7/24, GSW/DET/TOR named suitors), **Draymond Green** (7/25 — "expected to re-sign GSW ~$28M," not yet done, so still FA), **Jonathan Kuminga** (7/24, LAL sign-and-trade talks), **Cam Thomas** (unsigned since MIL waived him 3/23), **Jaden Ivey** (unsigned since CHI waiver 3/31; no market), **Jeremy Sochan** (7/16, NYK reunion "open").

## 2. Projection changes (labeled per Operating Principle 3)

- **LeBron James (new row)** — [ESTIMATED]. Base rates pulled from Basketball-Reference today (2025-26: 60 GP, 33.2 mpg, 20.9/6.1/7.2 on .515/.737): projected down to 55 GP, 29 mpg, 16.0/5.5/6.0/0.9/0.5, 1.2 3PM, 2.6 TO. Mechanism (>20% swing, §4.4): age-42 season + fourth-option role behind Embiid/Maxey/Brown + certain load management. My numbers, not a computation — argue with them.
- **Miles Bridges (new row)** — [ESTIMATED]. Near carry-over of his verified 2025-26 line (77 GP, 31 mpg, 17.1/5.8/3.2, .460/.822): projected 72 GP, 17.0/6.0/3.0. Similar starting-forward role expected in PHX; no mechanism for a bigger move.
- **Anfernee Simons** — [ESTIMATED, my judgment]. Trimmed 32→30 mpg, 21.5→19.5 pts, 3.3→3.0 3PM, 4.5→4.2 ast. Mechanism: usage squeeze from two named arrivals (LeBron 7/24, Kentavious Caldwell-Pope via Grizzlies buyout 7/25-26, [ESPN](https://www.espn.com/nba/story/_/id/49449509/sources-caldwell-pope-join-76ers-grizzlies-buyout)). The direction is [LIKELY]; the magnitude is [SPECULATIVE] — Simons could also just get traded from that crowded backcourt.
- **Jalen Wilson** — [ESTIMATED]. Slashed to two-way scale. Mechanism: two-way contract.
- **No change** (news checked, projection already consistent): DiVincenzo 15 GP (Achilles, ~Feb 2027 return), Lillard 45 GP ("on track for opening night" but single-outlet in-window — hold), Haliburton 60 GP (rehab on track, 7/21), Embiid 45 GP (Rich Paul: "first healthy summer, no surgery," 7/25 — agent-speak, not moving GP on it), Brunson 72 GP (wrist surgery 7/7, ready for camp), Kawhi 35 GP placeholder (see §4).

## 3. Board movement (computed — engine re-run, baseline diffed by script)

Gate status: `check_provenance.py --max-age-days 14` **PASS** (verified span 2026-07-13..27; note the 7/13 rows hit the 14-day limit tomorrow — expected, the full re-verify is October's job).

- **In:** LeBron James #121, Miles Bridges #125, Jalen Wilson #193 (tail).
- **Out:** Chris Paul (was #150 — retired), Jonathan Kuminga (was #199, displaced by additions), Ron Holland (was #200, displaced).
- **Moves ≥3:** Anfernee Simons #64 → #83 (−19, the usage-squeeze trim); Keon Ellis #125 → #129 (−4, pool-composition side effect, not a projection change).
- **Everything else stable** — spot-checked: Kawhi #34→#34, Cam Thomas #119→#119. Top 12 unchanged.
- **Engine header fix:** `rank_engine.py`'s hard-coded caveats still claimed "LeBron James excluded as unsigned FA" while the board now ranks him — fixed the two stale bullets so the artifact doesn't contradict itself. This file needs committing too.

## 4. Kawhi Leonard — still in limbo [CONFIRMED, 3 sources]

Toronto trade remains **on hold, not completed, not voided**. Investigation fact-finding is reportedly complete and the NBA is reviewing the law firm's findings (7/24, [Yahoo](https://sports.yahoo.com/articles/raptors-major-kawhi-leonard-trade-025241373.html)); Silver said 7/15 it must wrap "before the beginning of next season" ([ESPN](https://www.espn.com/nba/story/_/id/49364590/silver-kawhi-leonard-probe-finish-season-starts)); suspension or contract-void scenarios remain live, and the probe expanded 7/14 to a second endorsement deal. Toronto reportedly still intends to complete the deal. His 35-GP LAC placeholder row stands. Side effect: Bennedict Mathurin's RFA is frozen by the same investigation (7/26) — his LAC row stands.

## 5. Watchlist — flagged, no row edits (scope-fence)

- **PHI logjam** is now the biggest projection-uncertainty cluster on the board: Embiid/Maxey/Brown/LeBron/Simons/KCP/Edgecombe. Edgecombe's row is untouched but he's the next candidate for a trim if the rotation news firms up in camp.
- **OKC post-Dort:** Cason Wallace / Alex Caruso minutes should tick up — watchlist, not edited (no minutes reporting yet).
- **MEM post-KCP-buyout:** wing minutes open for Jaylen Wells / GG Jackson — watchlist.
- **RFAs still unsigned 7/26:** Jalen Duren, Mathurin, Peyton Watson — holdout risk if unresolved by camp.
- **Trey Alexander (UTA)** stretchered at Summer League 7/13, severity never disclosed — not in pool, but a UTA depth note.
- **Draymond → GSW** at ~$28M is [LIKELY] per 7/25 reporting; when it signs, his FA row gets a team and a real projection.

## 6. Assumptions & open items

- **A1** — Delta-pull scope (news since 7/13), not full re-verification. All 7/13 verifications trusted for rows with no news.
- **A2** — Deliverable = complete updated files for you to commit via GitHub Desktop (claude.ai cannot push — reads only).
- **A3** — **Miles Bridges was absent from the original 220-row pool.** I could not determine whether that was an oversight or a deliberate exclusion (he has an off-court history you may not want to roster). I added him because he's fantasy-relevant (#125); **delete the row if the exclusion was intentional** — the board regenerates cleanly without him.
- **Open** — Kuminga discrepancy: Bleacher Report (7/24) describes his declined option as Atlanta's, while the kit had him as a GSW FA. Single source; his row says FA either way, but worth reconciling in October.
- **Open** — Mark Williams' foot: no update found in window; his 58-GP discount stands unexamined.

## 7. Verification report (adversarial-verify)

**Criteria** — C1 every change source-dated ≤14 days, 2+ sources for tier-movers: PASS (table above). · C2 `check_provenance.py` passes locally, including `--max-age-days 14`: PASS (output quoted in §3). · C3 rank movement computed, not eyeballed: PASS (script diff, both runs agree). · C4 computed/estimated/speculative labeled: PASS (§2).
**Refutation** — found and fixed one real defect (stale engine header contradicting the board); found one pre-existing defect (retired Chris Paul ranked #150) and removed it; A3 (Bridges) survives as a flagged assumption, not silently absorbed.
**Regressions** — none: unchanged players' ranks stable across baseline diff; gate passes; second engine run identical.
**Status** — delivered. Projection magnitudes in §2 remain estimates by nature and are labeled as such.

---

**Commit handoff (GitHub Desktop):** replace `report/projections-2026-27.csv`, `report/roster-provenance.csv`, `report/rank_engine.py`, `report/top-200-2026-27.md` in `fantasy-basketball-2026-27`, commit as "Data pull 2026-07-27: LeBron→PHI, Dort/Risacher trade, CP3/JV removed, Bridges added, Simons trimmed". Or hand this file to Claude Code and it can apply + push.
