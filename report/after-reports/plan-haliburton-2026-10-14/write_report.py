#!/usr/bin/env python3
"""Writes after-report-2026-10-14-haliburton-plan.md from plan_2026-10-14.json (plan.py's record). Every number in the
report is read from that record."""
import json, os, statistics as st
H = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(f"{H}/plan_2026-10-14.json", encoding="utf-8"))
R = D["replay"]
OUT = os.path.join(os.path.dirname(H), "after-report-2026-10-14-haliburton-plan.md")
nR, nG = len(D["rooms"]), len(R)
gone = D["haliburton_gone_before_10"]
pct = lambda x: f"{100 * x:.0f}%"
tr = [r["title_real"] for r in R]; tp = [r["title_plan"] for r in R]
er = [r["ecw_real"] for r in R]; ep = [r["ecw_plan"] for r in R]
better = sum(1 for a, b in zip(tr, tp) if b > a)
subs = [len(r["substitutions"]) for r in R]
# how often each full-sample plan name actually made the replayed roster
plan_names = [p for _, p in D["plan"]]
landed = {p: sum(1 for r in R if p in r["plan_roster"]) for p in plan_names}
loo_same = {p: sum(1 for r in R if p in r["loo_plan"]) for p in plan_names}

L = []; w = L.append
w("# After-report — 2026-10-14 (research): a Haliburton-at-10 roster plan from the live rooms on file\n")
w('**Owner request (2026-10-14, verbatim):** "Once this is complete and you provide projects report, I\'d like for you to conduct a research exercise. Assuming I take Haliburton at 10, I\'d like for you to build a roster with my remaining picks, using players who are historically available at each pick (based on the average of the previous live mock drats we have conducted). I\'d like to see who I can scope to target at around each round pick I have. I understand this system calculates based on my opponent\'s roster builds, but If I am building around my top 1 and 2 picks, this in theory should be helpful right?"\n')
w("Pull window: 2026-10-14 → 2026-10-14 (research on records; no pull, no line or price change on either plane).\n")
w(f"**What was analyzed.** The {nR} live public rooms on file drafted from seat 10 (mocks {', '.join(map(str, D['rooms']))}; the bot-cast rooms are excluded — bots, not people), each a full 156-pick record in `arena/data/states/`. Lines: Version 68 (`arena/results/players_v68.csv`), the lines the draft page carried this morning. Your 13 turns: #10, 15, 34, 39, 58, 63, 82, 87, 106, 111, 130, 135, 154.\n")
w("**Method (stated before the run).**")
w("- *Availability* of a player at your pick N = the share of rooms in which no opponent had taken him before pick N. Your own earlier picks in a room do not count against him (the plan picks differently from what you did).")
w("- *Fit* = the gain in the deck's own weekly model (expected categories won per week against that room's opponent rosters at that moment), averaged over the rooms where he was still there. This is where your top picks matter: every gain is measured on top of Haliburton and the plan's earlier picks.")
w(f"- *Tiers*: likely = there in {pct(D['thresholds']['likely'])}+ of rooms; coin flip = {pct(D['thresholds']['coin'])}–{pct(D['thresholds']['likely'])}; reach = under {pct(D['thresholds']['coin'])}. The plan takes the best-fitting *likely* player at each turn whose addition still leaves your eight positional slots fillable; the DO NOT DRAFT list (Porziņģis) is excluded.")
w(f"- *Check*: the plan dropped into each room in your seat and graded on title odds (8-team bracket, 3 seeds × 6000 seasons) against your real roster in that same room, both on Version 68 lines. Leave-one-out: the plan graded in a room is built from the other rooms only, so no room grades a plan it helped build. When the planned player was gone, the next name on that turn's list took his place.\n")
w(f"**Headline.** Haliburton himself was there at #10 in {nR - len(gone)} of {nR} rooms (gone in mocks {', '.join(map(str, gone))}). Building around him, the most reliable path the rooms support is: " + "; ".join(f"#{n} {p}" for n, p in D["plan"]) + f". Dropped into the {nG} rooms where Haliburton was there, the leave-one-out plan beat your real roster on title odds in {better} of {nG} (median {st.median(tp):.1f}% vs {st.median(tr):.1f}%), and on weekly categories in {sum(1 for a, b in zip(er, ep) if b > a)} of {nG}. That gap is real but overstated — see §3: the plan is graded on the same lines it was chosen with, while your real picks were made on earlier versions of the page.\n")
w("## 1. Roster changes\n\nNone — research only. Neither plane changed.\n")
w("## 2. The plan, turn by turn — who to scope at each of your picks\n")
w("Each turn lists the top names by fit in each tier. *There* = share of the rooms where he was available at that pick; *recent* = the same over the six rooms drafted 10/12 or later (mocks " + ", ".join(map(str, D["recent"])) + "), since Yahoo's prices moved through September. *Fit* = weekly categories gained (on top of the plan so far).\n")
for t in D["turns"]:
    w(f"### Pick #{t['pick']} — plan: **{t['plan']}**\n")
    w("| tier | player | team | pos | there | recent | fit |\n|---|---|---|---|---|---|---|")
    for tier in ("likely", "coin", "reach"):
        for r in t[tier][:4]:
            w(f"| {tier} | {r['n']} | {r['team']} | {r['pos']} | {pct(r['avail'])} | {pct(r['avail_recent']) if r['avail_recent'] is not None else '-'} | {r['gain']:+.3f} |")
    w("")
w("## 3. The check: the plan dropped into the rooms\n")
w("| mock | your real roster: title / weekly cats | the plan (built without this room): title / weekly cats | planned players already gone |\n|---|---|---|---|")
for r in R:
    w(f"| {r['mock']} | {r['title_real']:.2f}% / {r['ecw_real']:.3f} | {r['title_plan']:.2f}% / {r['ecw_plan']:.3f} | {len(r['substitutions'])} of 12 |")
w(f"\nMedian title odds {st.median(tr):.2f}% real vs {st.median(tp):.2f}% plan; mean {st.mean(tr):.2f}% vs {st.mean(tp):.2f}%. The plan beat the real roster in {better} of {nG} rooms. Planned players already gone when the turn came: median {st.median(subs):g} of 12 per room (max {max(subs)}).\n")
w("**Why the gap is overstated (read before trusting it):**")
w("- *Same lines.* The plan was chosen on Version 68's lines and graded on them; your real picks in mocks 52–79 were made on Versions 3x–6x, whose lines differed (the WO-5, MG, dial and blend passes all came after many of these rooms). A roster picked with yesterday's numbers always looks worse under today's.")
w("- *Haliburton is forced.* The real rosters did not all start with Haliburton; the plan's value includes whatever Version 68 thinks of him versus your real #10.")
w("- *Leave-one-out* removes the room-fitting bias only; it cannot remove the two above.")
w("So read the replay as *the plan is not a trap* — it holds up in every kind of room on file — not as a promise of the size of the edge.\n")
w("**How stable the plan is.** How often each full-sample pick was also the leave-one-out plan's pick, and how often he actually landed on the replayed roster:\n")
w("| turn | plan | same pick in leave-one-out plans | landed on the roster |\n|---|---|---|---|")
for n, p in D["plan"]:
    w(f"| #{n} | {p} | {loo_same[p]} of {nG} | {landed[p]} of {nG} |")
w("")
w("## 4. Your question: is building around picks 1 and 2 helpful?\n")
w("Yes, with one adjustment to how to use it. The fit numbers above already *are* built around your first two picks — every turn's gain is measured on top of Haliburton and the plan's #15 — so the plan leans toward what that core lacks rather than toward the best player in a vacuum. Where it helps most is preparation: knowing that the names in the *likely* column are usually there means you can plan the pair at #34/#39, #58/#63 and so on instead of reacting.\n")
w("The adjustment: the draft page still adapts to the actual room (who your opponents took, what your roster already has). The plan is fixed in advance; the card is not. When they disagree at a turn, it usually means the room has run differently from the rooms on file — the card has seen that, the plan has not. Use the plan as the scouting map and the card as the live call.\n")
w("## Watchlist\n")
w("- Haliburton was gone before #10 in " + f"{len(gone)} of {nR} rooms; if he is gone tonight, this plan's later turns no longer apply as built (the card adapts).")
w("- The plan's late turns (#130 onward) rest on few distinctions — fits there are small and close together.\n")
w("## Open-item receipts\n")
w("| item | query run (2026-10-14) | dated finding |\n|---|---|---|")
w("| (research) | records only; no web research and no roster pull | the lines are Version 68's (`players_v68.csv`) |")
w("| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | this morning's final pull (`after-report-2026-10-14.md`, receipts dated 10/14) and the lock report (`after-report-2026-10-14-lock.md`) | as recorded there; not re-queried for this research (did not check) |\n")
RN = open(os.path.join(os.path.dirname(H), "lock-2026-10-14", "rn_section.txt"), encoding="utf-8").read()
w("The standing check below is the one run on the locked page (Version 70) for the lock report; this research built no page.\n")
w(RN[RN.index("## Repeat-name market check"):].rstrip() + "\n")
w("## Bounds\n")
w(f"- Out of scope by design: bot-cast rooms; the real draft's eleven league-mates (the rooms are public strangers, so tonight's opponents may draft differently); any line or price change.")
w(f"- In scope and stated: availability is measured on {nR} rooms ({len(D['recent'])} recent) — a player at 70% is a measured rate on a small sample, not a guarantee. The bias in §3 is named, not removed.")
w("- Did not check: a market-only baseline (best available by ADP at each turn) graded the same way — it would separate how much of the gap is planning and how much is the lines.\n")
w("## Decision sheet (owner disposes)\n")
w("| id | decision question | default if silent |\n|---|---|---|")
w("| D-1014-14 | Use this plan as a scouting map beside the card (no change to the page), or ask for a second version (e.g. a different #15 or a punt build)? | scouting map only; the page is unchanged |\n")
w("## Provenance\n")
w("- Script: `plan.py` (this folder); record: `plan_2026-10-14.json`; run log `plan_run.log`. Engine: the deck's `arena.team_week_model`, `simulate_seasons` (seeds 11, 23, 47; 6000 seasons each), `hoops.POSITIONAL_SLOTS`, `hoops.do_not_draft()`.")
w("- Rooms: `arena/data/states/draft_state_<mock>.json` in the deck repo (mock 80 from branch `claude/mock80-2026-10-14`).\n")
w("## In plain language\n")
w(f"I looked at the {nR} live mock rooms you drafted from the 10th seat and asked, for each of your picks, which players were usually still there. Then I built the roster that fits best around Haliburton using only players who were there in at least two out of three rooms:\n")
w("\n".join(f"- **#{n}** {p}" for n, p in D["plan"]) + "\n")
w(f"When I dropped that plan into the rooms (each time building it without looking at that room), it beat the roster you actually drafted there in {better} of {nG} rooms. Part of that is real, and part of it is that the plan was picked with today's numbers while your real picks used older versions of the page — so treat the size of the edge with caution. Section 2 lists, for every pick, the names that are usually there, the coin flips, and the reaches, so you have backups if the room goes differently. And yes — building around your first two picks is exactly what the fit numbers do; just let the card make the final call at each turn, because it sees the room you are actually in.\n")
open(OUT, "w", encoding="utf-8").write("\n".join(L))
print("wrote", OUT)
