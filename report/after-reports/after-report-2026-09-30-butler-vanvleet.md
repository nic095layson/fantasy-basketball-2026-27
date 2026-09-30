# After-report — Jimmy Butler's re-inclusion and Fred VanVleet's price, researched (2026-09-30)

**Owner request (2026-09-30, verbatim):** "Also, can you please re-include
Jimmy Butler? News is saying of his return to on court work. Additionally,
may I ask where Fred VanVleet's value lies in your database? He is healthy
and set to return to his starting role for Houston as well. Please internet
research for both value pricing for these players."

**Scope.** Two players, both planes, the market file, and three dated
WebSearch passes on 2026-09-30. **What changed: nothing in the pool** — Butler's
re-inclusion is put back to the owner with the evidence (it conflicts with
two of the owner's own standing rules), and VanVleet's rows already price
what the news says; both carry a decision below.

Pull window: 2026-09-30 → 2026-09-30 (same-evening research; not a roster
pull — the 9/30 pull-log rows cover the window).

**Headline.** Butler's news is real and does not clear the bar the pool sets
for re-entry: he is in "very light on-court activities" eight months after
ACL surgery, the Warriors say he stays in that stage "for a chunk of time to
open the season", and the only return date in print is Slater's "January or
February, optimistic". Re-including him tonight would put him at **deck rank
24** (the deck's only available multiplier is the 0.78 risk tier, which
assumes about four games in five) for a man who cannot play before the
league's week 12 at best, and it would draft for an IL+ stash, which the
owner ruled out on 2026-08-04. The kit already prices him honestly at 20
games (rank 66, the streaming-credit model); the room prices him at ADP 117.
**VanVleet is priced where the news says**: fully cleared, scrimmaging,
starting, but no back-to-backs early and cautious minutes — the kit's 55
games (rank 75) and the deck's first-season-back risk tag (rank 69) carry
exactly that; the room has him at ADP 120 and XRank 136, roughly 45 places
below the board, and he went at #132 in tonight's live room.

## 1. Jimmy Butler

| source (2026-09-30) | finding |
|---|---|
| NBC Sports Bay Area | "light on-court work", can dunk, three-quarter speed; the team is cautious; "no timeline for his return"; January or February "an optimistic target" |
| Warriors' own update via Yahoo, Heavy | Butler and Moody "progressed to very light on-court activities" and remain in that stage "for a chunk of time to open the season" |
| Slater via Yahoo, Bleacher Report | a January or February 2027 return is "optimistic"; he will not be available when the season opens |
| Hoops Rumors (June, September notes) | ACL surgery in February after the January 19 tear against Miami |

What the planes carry: kit 20 games, 29 minutes, 15.5 / 5.5 / 4.5 on .470 —
rank 66 (the streaming-credit availability model gives a 20-game man
roughly 40 percent of his per-game value); deck `acl-recovery-jan26`, which
excludes him from every board and card (the resolver still logs him when an
opponent takes him, as it did at #141 tonight). Market: consensus 106, Yahoo
XRank 134, ADP 117.4.

Why not tonight: (1) the pool's re-entry rule (`data/RESEARCH.md`, owner
ruling 2026-07-12) re-tags a recovery to `-risk` "once news confirms a full
return"; this news confirms light drills and no date. (2) The deck's risk
tier is 0.78 — four games in five. A February return is 25 to 35 games of
the league's 21-week season, a third at most; the tag would price him at
rank 24 and the card would show him in round 2 territory with a ▲. (3) The
owner's own answer 6 of 2026-08-04: "the owner drafts ONLY for active
roster + bench, never for IL+ stashes"; a January return is a stash by
definition. The honest instrument for Butler is the kit's games line, and
the honest deck treatment is a finer availability tier than the tag system
has — which is decision D-BV1's second branch.

## 2. Fred VanVleet

| source (2026-09-30) | finding |
|---|---|
| SI Rockets (two pieces) | fully cleared for all basketball activities after the torn right ACL and meniscus; "the Rockets will be cautious"; Udoka on the rehab and the mentality |
| Yahoo (Rockets camp day one, "first look", "remains on course") | five-on-five scrimmages "at a high level"; starting point guard with Durant, Amen Thompson, Jabari Smith Jr. and Şengün |
| ClutchPoints | the clearance "comes with one important caveat": no back-to-backs to open the season |
| The Dream Shake | camp day-one report, same lineup |

What the planes carry: kit 55 games, 28 minutes, 13.5 / 3.5 / 5.5 with 2.4
threes on .400 / .850 — rank 75; deck `inj-acl-risk (first season back)`,
line 14.1 / 3.7 / 5.6 with 2.5 threes on .374 / .810 (his 2024-25
Basketball-Reference season) — rank 69, and because his 9-cat total is
slightly negative the 0.78 multiplier does not move him (negatives are never
shrunk). Market: consensus 110, Yahoo XRank 136, ADP 119.5; #132 in mock 58.

Where the value lies: the board says round 6 to 7 (69 to 75), the room says
round 10 to 11 (120 to 136). The gap is the usual one for a returning
starter the market discounts twice — once for the injury, once for the age
(32) — while the board prices only the games. The no-back-to-backs rule is
already inside 55 games (82 minus the second nights of about 14 back-to-backs
minus rest). He is exactly what the round-9 rule is for: a starting point
guard with threes and assists at a two-round discount, and the card put him
in the owner's Top-5 at #130 tonight. No edit is warranted; the deck note
gets today's outlets at the next pull (D-BV2), and the kit's .400 field-goal
line is the one number to re-check against his career .400 and 2024-25
.374 at the final pre-draft refresh.

## Watchlist

- **Butler**: the first sourced return date, or a Warriors update moving him
  past "very light" work — either re-opens D-BV1.
- **VanVleet**: the first preseason box score (minutes, back-to-back
  handling).

## Open-item receipts

| item | query run (2026-09-30) | dated finding |
|---|---|---|
| Butler status | WebSearch ×2 (return timeline; injury and surgery) | NBC Sports Bay Area, Yahoo/Heavy (the Warriors' update), Slater via Yahoo and Bleacher Report, Hoops Rumors — very light on-court work, no timeline, January or February optimistic |
| VanVleet status | WebSearch ×1 (camp, clearance, role) | SI Rockets, Yahoo Rockets coverage, ClutchPoints, The Dream Shake — cleared, scrimmaging, starting, no early back-to-backs, cautious minutes |
| both, market | `report/market/consensus-2026-09-22.csv` | Butler XRank 134 / ADP 117.4; VanVleet XRank 136 / ADP 119.5 |

## Bounds

- All outlets read through search summaries (the sports domains are
  egress-blocked for direct fetch).
- The deck's availability tiers are 0.0, 0.78 and 1.0; nothing in between
  exists tonight, which is the whole Butler problem.
- No pool row changed; both planes' ranks quoted are tonight's v36 and
  the kit board at `13af53b`.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-BV1 | Butler: (a) keep excluded until a sourced return date, with the kit's 20 games as the only price; or (b) re-include as an owner override at the 0.78 tier (deck rank 24, a ▲ on the card, and a judgment card saying the multiplier overstates him); or (c) add a finer deck availability tier (a games-based multiplier twinned from the kit, so a 20-game man shows at roughly 0.40) — a red-first engine change with parity, sized for the final pre-draft build. | (a) now; (c) at the final pre-draft refresh if the owner wants recovery stars visible at an honest price |
| D-BV2 | VanVleet: append today's outlets to the deck note (cleared, starting, no early back-to-backs) at the next pull; re-check the kit's .400 field-goal line against his .374 last season at the final refresh. | yes |

## Provenance

- Inputs: three dated WebSearch summaries (2026-09-30); both planes' rows and
  ranks computed by `hoops.py` on the v36 pool and the kit board as merged.
- No claim here rests on a direct read of a blocked sports domain.
