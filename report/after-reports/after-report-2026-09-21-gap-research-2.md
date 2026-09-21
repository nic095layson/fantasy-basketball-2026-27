# After-report — Gap research round 2 + system tune-up analysis (2026-09-21)

**Owner request (2026-09-21, verbatim):** "Can you please conduct a full,
internet search player research for the data you were missing this run? Also
conduct a tune-up system analysation, anywhere you see the system can improve
with this most recent run. provide after report."

**Scope.** Part A: the pool gaps draft_51 exposed. The un-researched gap set
was enumerated mechanically — Yahoo-300 names absent from the kit 240-pool,
minus the 13 researched 2026-09-16 — yielding 73 true gaps (74 raw; Ronald
Holland II is an alias artifact, pool has Ron Holland). The eight most
room-draftable (XRank 165–213, rotation-relevant) got dedicated dated
searches; the remaining 65 deep-tail names were deliberately not researched
(decision, not limit — rationale in Bounds). Part B: tune-up proposals from
draft_51's four defect classes plus the cross-plane findings. **Nothing
integrated**; every change below is a proposal.

**Method:** WebSearch summary channel (sports fetches egress-blocked;
summaries garble — cross-outlet agreement per claim, [SINGLE-SOURCE] labels
otherwise). Verification: this file passes `report/check_report.py`.

Pull window: 2026-09-15 → 2026-09-15 (research run 2026-09-21; no roster
state change since the 9/16 integration).

**Headline.** Tre Jones — the name a live room actually drafted while both
planes lacked him — is a genuine MUST-ADD: Chicago's primary backup point
guard (14.1 pts / 5.4 ast / 1.2 stl in 64 games) on a roster with only one
other true ball-handler behind Giddey. Four more gaps earn deep rows (Joan
Beringer is the find: Minnesota's primary backup center now that the Naz Reid
seat is empty), two are watch-only. On the tune-up side, the run's biggest
systemic hole is not any single bug — it is that **the two planes have no
mechanical consistency check**: Butler was right on the deck and wrong on the
kit for months, then Sheppard/Vučević/George/Randle were right on the kit and
wrong on the deck within a week, and the live mock priced two picks off the
stale side. Proposal S3 makes that a gate.

---

## Part A — the missing players: fit, role, opportunity

## 1. Verdict summary

| player | team | XRank | verdict |
|---|---|---|---|
| Tre Jones | CHI PG | 173 | MUST ADD (both planes) — live-drafted at #134 |
| Joan Beringer | MIN C | 169 | ADD (deep) — primary backup C behind Gobert |
| Isaiah Joe | DET SG | 213 | ADD (deep) — elite 3PT, closes games |
| Naji Marshall | DAL F | 203 | ADD (deep) — extended, line real, role crowded |
| Jay Huff | IND C | 165 | ADD (deep) — backup C, stretch-blocker |
| Tim Hardaway Jr. | MIA SG | 184 | OPTIONAL — bench sniper, one-category |
| Will Riley | WAS F | 178 | WATCH — squeezed by a suddenly deep roster |
| Scotty Pippen Jr. | MEM PG | 176 | WATCH — real opportunity, toe-surgery recovery |

**Tre Jones (CHI).** First guard off the bench and, with Rob Dillingham, one
of only two true point guards behind Josh Giddey; 14.1 points, 5.4 assists,
1.2 steals across 64 games last season, with local coverage arguing he opens
with an even larger role (EVIDENCE: SI Bulls, Yahoo depth-chart projection,
RotoWire, searched 2026-09-21). A real 9-cat line (AST/STL, low TO per his
profile) that a live room already drafted. Demote if Chicago adds a veteran
ball-handler in camp.

**Joan Beringer (MIN).** The offseason's LaMelo Ball trade sent Naz Reid out,
and Beringer — 7.9 mpg as a rookie — is now the primary backup center behind
Gobert, a rim-running, shot-blocking archetype with switch ability (EVIDENCE:
SI Timberwolves, Canis Hoopus, Last Word, searched 2026-09-21). BLK-per-minute
profile our engine values; minutes still modest. Demote if MIN adds a veteran
big.

**Isaiah Joe (DET).** Detroit's second elite perimeter threat next to Duncan
Robinson — 42.3% from three on 11.1 points with defensive competence the
coverage explicitly ranks above Robinson's, and a "closes more games than
you'd think" read (EVIDENCE: SI Pistons ×2, Piston Powered, searched
2026-09-21). 3PM specialist row, cross-corroborates the 9/16 Robinson
research (which already named Joe among DET's 40%+ additions).

**Naji Marshall (DAL).** Three-year, $52.2M extension against an explicitly
undetermined role after Dallas took Morez Johnson at No. 9; career-best
15.2/4.7/3.3 with 1.1 steals on 51% last season (EVIDENCE: Yahoo, SI
Mavericks, CBS role note, searched 2026-09-21). The line is pool-worthy; the
crowd is the risk. Demote if camp reporting puts him under ~24 mpg.

**Jay Huff (IND).** Backup center behind Zubac, bulked up, floor-spacing
shot-blocker with analytics appeal — and an explicit career-long
role-stability caveat (EVIDENCE: Yahoo, Fieldhouse Files, RotoWire, searched
2026-09-21). One conflict noted: a January article treats Isaiah Jackson as a
Pacer while Yahoo's 9/15 list has him LAC — the stale-article read, not a
data problem [dated-source conflict, resolved toward the fresher Yahoo list].

**Tim Hardaway Jr. (MIA).** One year, ~$6.5M; primary bench scorer staggered
with Giannis, catch-and-shoot with famously low turnovers (EVIDENCE: NBA.com
×2, SI Heat, searched 2026-09-21). One-category 3PM row — OPTIONAL.

**Will Riley (WAS).** Late-season flashes (20.0 points over his final seven)
but the newly competitive Wizards squeeze him into a bench fight with Khris
Middleton and Bilal Coulibaly (EVIDENCE: Yahoo, Bullets Forever, searched
2026-09-21). WATCH. Side-finding: the projected WAS starting five named again
— Young, Davis, Dybantsa, Kyshawn George, **Sarr** — further evidence Ayton
projects as the backup center, supporting his cautious kit line (62 GP
timeshare) and sharpening his preseason watch item.

**Scotty Pippen Jr. (MEM).** Real floor-general opportunity in the post-Ja
backcourt against Ty Jerome and Cam Spencer — but he missed 72 games with a
toe injury (March surgery), rehabbing toward a full return (EVIDENCE: SI
Grizzlies, Yahoo, RotoWire, searched 2026-09-21). WATCH until camp confirms
health. Cross-corroborates Jerome's lead-guard path (our validated value).
Side-finding: MEM coverage names **Javon Small**, a guard in neither pool nor
Yahoo's 300 — logged to the watchlist as a new-name check.

## Part B — tune-up: where draft_51 says the system can improve

Tiered proposals; every item cites the run evidence that produced it.

- **S1 — MUST FIX (resolver design): opponent picks never require pool
  membership.** Evidence: #134 silently logged the wrong player, #152 was
  then blocked, #154 stuck the owner's own turn — all from ONE out-of-pool
  name. An opponent pick should log verbatim with a not-in-pool marker; only
  owner-side recommendations need pool rows. Cross-language change (deck JS +
  `arena.py` + parity fixtures, driven red first per the house rule).
- **S2 — MUST FIX (data): pool coverage.** Adds per the Part A tiers, applied
  per-plane after S3's first diff produces each plane's exact missing list
  (the kit and deck pools differ — the deck has names the kit lacks and vice
  versa). Coverage policy going forward: the pool should cover Yahoo XRank ≤
  ~180 at minimum — the live room drafted XRank 173.
- **S3 — HIGHLY RECOMMEND (new gate): cross-plane consistency check.** The
  run's biggest lesson. Butler sat correct-on-deck/stale-on-kit for months;
  a week later Sheppard, Vučević, Keyonte George and Randle were
  correct-on-kit/stale-on-deck, and the live tool priced two real picks off
  the stale side (Sheppard at 82, Lillard at 63). A per-pull script diffing
  name sets, team codes, and availability severity (kit GP class vs deck tag
  class) would have caught both directions mechanically. This is the
  F7-shaped protocol addition.
- **S4 — RECOMMEND (advisor stability): punt-detector hysteresis.** It
  retargeted four times (AST+FT% → FT%+TO → TO+FG% → TO+AST) and its final
  call was half wrong — the replay shows TO as the roster's second-best
  category. Require a sustained fit-delta before flipping, and log the
  rationale so the after-report can audit it.
- **S5 — NICE (cosmetic):** the "logged AND skipped: injury-excluded"
  annotation at #140 — reword to "logged; note: this player is
  injury-excluded on our board."
- **S6 — NICE (storage tolerance):** state files should carry verbatim names
  with not-in-pool markers so a state like draft_51 can be stored canonically
  even before pool adds land (today it would break the parity harness's
  auto-ingest).
- **S7 — POLICY (D-I1 generalized):** one shared severity source for
  recovery-class players. Butler is deck 0.0 ("return ~2027") vs kit GP 20
  (board #68) — whichever the owner picks, both planes should derive from it.

## Watchlist

Javon Small (MEM) — new name, neither plane nor Yahoo-300, verify next pull;
Ayton's WAS backup-role evidence (preseason confirms); Pippen Jr. toe rehab;
Riley's bench fight; the standing items unchanged. All Part A adds await
owner approval — nothing enters a pool from this report.

## Open-item receipts

| player / item | query run (2026-09-21) | dated finding + outlets |
|---|---|---|
| Tre Jones | Tre Jones Bulls 2026-27 backup point guard role | primary backup PG, 14.1/5.4/1.2; SI, Yahoo, RotoWire, NBA.com |
| Jay Huff | Jay Huff Pacers 2026-27 center role | backup C behind Zubac; Yahoo, Fieldhouse Files, RotoWire |
| Joan Beringer | Joan Beringer Timberwolves rookie 2026-27 role | primary backup C post-Reid; SI, Canis Hoopus, Last Word |
| Scotty Pippen Jr. | Scotty Pippen Jr Grizzlies 2026-27 guard rotation | floor-general chance, toe rehab; SI, Yahoo, RotoWire |
| Will Riley | Will Riley Wizards 2026-27 rookie role minutes | bench fight vs Middleton/Coulibaly; Yahoo, Bullets Forever |
| Tim Hardaway Jr. | Tim Hardaway Jr Heat 2026-27 role | bench sniper, staggered with Giannis; NBA.com, SI |
| Isaiah Joe | Isaiah Joe Pistons 2026-27 shooting role | 42.3% 3PT, second weapon next to Robinson; SI (x2), Piston Powered |
| Naji Marshall | Naji Marshall Mavericks 2026-27 wing role | 3yr/$52.2M, role undetermined; Yahoo, SI, CBS |
| Gap enumeration | mechanical: Yahoo-300 minus kit-240 minus 9/16 set | 73 true gaps; researched 8; skipped 65 (see Bounds) |
| Publication gate | check_report.py on this file | PASS 2026-09-21 |

## Bounds

**Out of scope by design:** the 65 deeper un-researched gaps (XRank ~180–299
bench/two-way names; evidence for the cutoff: the live room drafted exactly
one of the 73 gaps, at XRank 173, and none deeper — stopped by decision, each
name one search away if the owner wants any); implementation of S1–S7
(proposals only); any pool edit.

**In scope and unverified:** per-plane missing lists differ and the deck-side
list is not enumerated here (S3's first run produces it — the kit-side list
is the one above); all stats are summary-channel relayed (standing garble
bound, mitigated by cross-outlet agreement); the Isaiah Jackson IND-vs-LAC
conflict resolved toward the fresher source, not a primary fetch.

## Decision sheet (owner disposes)

- **D51-1 (refined) — the pre-next-mock work order:** S1 + S2 (with the Part
  A add approvals: Tre Jones MUST; Beringer, Joe, Marshall, Huff deep;
  Hardaway optional) + S5 + S6, then rebuild, parity, artifact republish,
  and canonical storage of draft_state_51.
- **D51-3 — adopt S3** (cross-plane consistency gate) as protocol fix F7?
- **D51-4 — adopt S4** (punt-advisor hysteresis)?
- **D-I1 — Butler severity** (S7 makes it a policy, not a one-off): deck 0.0
  vs kit GP 20 — pick one, both planes inherit.

## Provenance

Produced 2026-09-21 by the operating session
(`https://claude.ai/code/session_01QjgeRdpDaWgSJmGKRG8fTU`) on branch
`claude/draft-51-mock-analysis` (PR #23, with the draft_51 analysis).
8 dated searches, outlets in receipts; gap enumeration from
`yahoo-2026-09-15.csv` vs `projections-2026-27.csv` at main. Companion:
`after-report-2026-09-21-draft51.md` (the run this report tunes against).
