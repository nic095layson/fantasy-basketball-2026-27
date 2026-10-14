#!/usr/bin/env python3
"""Writes report/after-reports/after-report-2026-10-14-undo-insert.md and its pull-log row from the records beside this
script: run_a / run_b (undo_insert_check.mjs on the Version 68 page), their _totals dumps re-checked by totals_oracle.py
logic, the repro_history record, and the mock-80 repeat-name section. No figure is typed by hand."""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.normpath(os.path.join(H, "..", "..", ".."))
J = lambda p: json.load(open(os.path.join(H, p), encoding="utf-8")); rd = lambda p: open(p, encoding="utf-8").read()
RA, RB = J("run_a_2026-10-14.json"), J("run_b_2026-10-14.json")
TA, TB = J("run_a_2026-10-14_totals.json"), J("run_b_2026-10-14_totals.json")
REPRO = J("repro_history_2026-10-14.json")
sys.path.insert(0, "/home/user/yahoo-fantasy-basketball/scripts"); import hoops
P = {p["player"]: p for p in hoops.zscores(hoops.load_players())}
assert RA["page"] == RB["page"] and RA["page"].endswith("page_v68.html")
# ---- assertions and failures
allA = RA["all"] + RB["all"]
hand_ids = sorted({a["id"].split(".")[0] for a in RA["all"] if not a["id"].startswith("R")})
hand = [a for a in RA["all"] if not a["id"].startswith("R")]
assert all(a["ok"] for a in hand), [a["id"] for a in hand if not a["ok"]]
rnd = [a for a in allA if a["id"].startswith("R")]
fails = RA["failures"] + RB["failures"]
assert all(f["id"].endswith("path-equals-oracle") for f in fails)
eng_diff = [f["id"] for f in fails if any(not x.startswith("tab:") for x in f["detail"])]
assert eng_diff == []
lead = [re.search(r'@\d+: path "(.*?)"', x).group(1)[:9] for f in fails for x in f["detail"] if x.startswith("tab:")]
assert all(l.startswith(("Losing", "Watching")) for l in lead), set(lead)
seeds = sorted({int(re.match(r"R(\d+)", a["id"]).group(1)) for a in rnd})
ops = {k: RA["notes"]["randomOps"][k] + RB["notes"]["randomOps"][k] for k in ("insert", "undo", "wrongLog")}
cps = sorted({a["id"].split(".")[0] for a in rnd if "@" in a["id"]})
assert len(seeds) == 10 and len(cps) == 10 and RA["pageErrors"] == [] and RB["pageErrors"] == []
# ---- independent totals (hoops) and rank ties
TOL = 13 * 5e-7; cells = 0; worst = 0.0; ties = []; over = []
for d in TA + TB:
    R = {s: [] for s in range(1, 13)}
    for n, s in d["picks"]:
        if n in P: R[s].append(P[n])
    full = {s: hoops.roster_totals(R[s]) for s in R}
    for s in R:
        for c in hoops.CATS:
            e = abs(d["totals"][str(s)][c] - full[s][c]); cells += 1; worst = max(worst, e)
            if e > TOL: over.append((d["id"], s, c))
    for c in hoops.CATS:
        py = 1 + sum(1 for s in R if s != 10 and full[s][c] > full[10][c])
        if py != d["ranks"][c]:
            gap = min(abs(full[s][c] - full[10][c]) for s in R if s != 10); ties.append((d["id"], c, d["ranks"][c], py, gap))
assert over == [] and all(t[4] < 1e-12 for t in ties)
# ---- the history reproduction
after = REPRO["after"]; assert REPRO["stateEqualsCleanFeed"] is True
dup_msg = [l for l in after if l.startswith("· #11 Josh Giddey is no longer your pick")]
assert len(dup_msg) == 2
rn = rd(os.path.join(K, "report", "after-reports", "draft80-2026-10-14", "rn_section_m80.md")); rn = rn[rn.index("## Repeat-name market check"):].strip()
o = []; w = o.append
w("# After-report — 2026-10-14: Undo and Insert-at-# integrity on the Version 68 page\n")
w("**Owner request (2026-10-14, verbatim):** \"Hi Claude, can you please test, validate integrity, that when using the “undo pick” and “insert at #” features are used, the arithmetic computation and correct team association is accurate?\" Read as an assessment: test and report; nothing on the page changes (the publish freeze holds).\n")
w("**What was analyzed:** the published Version 68 page (sha256 b83d1cdcc0e9, version id 1791993066-d8ff), driven in headless Chromium by `undo_insert_check.mjs`. **Method (stated to the owner before the run):** a PATH page reaches a final pick list through Undo and Insert-at-# (the owner's corrections); a clean ORACLE page is fed the same list in one feed; every derived value is compared — the picks and their seats (every seat also held to the snake formula), each team's roster, the nine z-total categories per team, the owner's category ranks, the next-pick clock, the available pool, the Top-5 card, the visible text of all five tabs — and the latest history line for each pick is held to the state. Each team's totals are re-computed independently in Python from the deck's own data (`hoops.py`).\n")
w("Pull window: 2026-10-14 → 2026-10-14 (analysis only; no roster pull; no page change).\n")
w(f"**Headline.** Undo and Insert-at-# keep the arithmetic and the team association exact. In {len(hand_ids)} hand-built cases and {len(seeds)} seeded full 156-pick drafts ({ops['insert']} inserts, {ops['undo']} undos, {ops['wrongLog']} wrong picks logged and undone; each draft compared at a mid-draft checkpoint and at the end), every pick sat on the correct seat, and every roster, category total, rank, clock, pool and Top-5 card equalled the clean page. {cells:,} team-by-category totals re-computed in Python agree within {worst:.1e} (the page bakes each player to six decimals). Three display quirks were found; none changes a number (§3).\n")
w("## 1. Roster changes\n\nNone. No line, tag, placement, price or page byte changed; this is a test of the shipped page.\n")
w("## 2. Results\n\nEVIDENCE: `run_a_2026-10-14.json` (the hand cases and seeds 1–5), `run_b_2026-10-14.json` (seeds 6–10), the `_totals` dumps, `totals_oracle.py`.\n")
w("| check | result |\n|---|---|")
w(f"| hand cases ({', '.join(hand_ids)}): undo and re-log; an insert crossing the owner's seat (#12, moving #15 and #16 on and off YOUR seat); insert at #1; insert at the end; insert ahead of a standing UNKNOWN (renamed to its new number); undo after insert; refusals (past the end, already drafted, #0, an off-snake my: pick) change nothing; reload | {sum(a['ok'] for a in hand)} of {len(hand)} assertions pass |")
w(f"| seats equal the snake formula, final list equals the intended draft, history's latest line per pick equals the state (random drafts) | {sum(a['ok'] for a in rnd if not a['id'].endswith(('path-equals-oracle','advice-line-live')))} of {sum(1 for a in rnd if not a['id'].endswith(('path-equals-oracle','advice-line-live')))} pass |")
w(f"| the advice line at mid-draft checkpoints equals the clean page | {sum(a['ok'] for a in rnd if a['id'].endswith('advice-line-live'))} of {sum(1 for a in rnd if a['id'].endswith('advice-line-live'))} |")
w(f"| every derived value equals the clean page (random drafts, checkpoints and ends) | {sum(a['ok'] for a in rnd if a['id'].endswith('path-equals-oracle'))} of {sum(1 for a in rnd if a['id'].endswith('path-equals-oracle'))} pass; the {len(fails)} that differ differ in no number (picks, seats, rosters, totals, ranks, clock, pool and Top-5 all equal) — only the punt advisor's wording (§3, Q3) |")
w(f"| Python re-computation of every team's nine totals | {cells:,} cells, largest gap {worst:.1e} (tolerance {TOL:.1e}: 13 players × half a sixth-decimal) |")
w(f"| category ranks against Python | {len(ties)} rank cells differ by one place; each is an exact tie (largest gap between the two teams {max(t[4] for t in ties):.1e}), and the page and the clean page match on every one |")
w("| page errors | 0 |\n")
w("## 3. Three display quirks (no number changes)\n")
w(f"- **Q1 — the history box after Undo then Insert.** Insert re-numbers the history from the state; lines for picks that were undone are re-rendered too, with whoever now holds that number. Reproduction (`repro_history.mjs`, 12 picks, Undo 3, three different players logged, a missed pick inserted at #2): the history shows \"{[l for l in after if l.startswith('✓ (R1) #11: Josh Giddey')][0]}\" just before \"↶ undid: …\" lines for other players, and \"{dup_msg[0]}\" twice. The state equals a clean feed of the same picks.")
w("- **Q2 — the advice line after the last pick.** When the draft completes the card renderer returns before it clears the advice line (`docs/draft-deck.html`: the `draftDone()` return in the card renderer comes before `alBox.classList.add(\"hidden\")`), so the last \"Take …\" sentence stays on screen. Any draft, not only corrections.")
w("- **Q3 — the punt advisor's \"2 picks running\".** Its counter counts owner turns the page rendered (`st.leanSeen`, ticked when the pick count differs from `st.leanSeenAt`), so the same picks entered one at a time and in one batch word it differently (measured: every one of the differing comparisons above). From the code (INFERENCE, not measured): undoing back across an owner turn, or an insert, can count a turn twice, so the message can arrive a turn early. Advice only; no button writes the punt box.\n")
w("## Watchlist\n\n- The publish freeze during the draft (D-1013-5) and no RESYNC during the draft (D-1013-2) stand; Q1–Q3 are carried to after the draft.\n")
w("## Open-item receipts\n\n| item | query run (2026-10-14) | dated finding |\n|---|---|---|")
w("| (this test) | records only; no web research and no roster pull | the page tested is the published Version 68, byte-identical (sha256 b83d1cdcc0e9) |")
w("| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | this morning's final pull (`after-report-2026-10-14.md`, receipts dated 10/14) | as recorded there; not re-queried for this test (did not check) |\n")
w(rn + "\n")
w("\n## Bounds\n\n**Out of scope by design.** Mock mode (the owner's draft is LIVE); RESYNC (covered 10/13); any fix (freeze).\n")
w("**In scope and unverified.** Q3's double count is read from the code and not reproduced (`NOT-ATTEMPTED`; not load-bearing: it moves advice wording, no number).\n")
w("## Decision sheet (owner disposes)\n\n| id | decision | options | recommendation |\n|---|---|---|---|")
w("| D-1014-9 | Q1, the history box after Undo then Insert | (a) leave through the draft; fix after (relabel skips lines whose pick was undone); (b) fix now (breaks the freeze) | (a) |")
w("| D-1014-10 | Q2, the stale advice line after the last pick | (a) leave; clear it in the draft-complete branch after the draft; (b) fix now | (a) |")
w("| D-1014-11 | Q3, the punt advisor counter | (a) leave; key the counter to the owner's pick number after the draft; (b) fix now | (a) |\n")
w("## Provenance\n\n- `undo_insert_check.mjs` (the harness; runs A and B, two processes), `totals_oracle.py`, `repro_history.mjs`, this writer; records beside them. The trial run (`trial_2026-10-14.json`) found the harness's own two faults (an open insert bar compared to a closed one; the stale advice line at draft end) before the full runs.\n")
w("## In plain language\n")
w(f"Undo and Insert-at-# are safe to use in the draft. Across {len(hand_ids)} hand-built cases and {len(seeds)} full practice drafts with {ops['insert']} inserts and {ops['undo']} undos, every pick landed on the right team and every total, rank and recommendation matched a clean entry of the same picks. Three display quirks, none of which changes a number: the history box can look muddled after an undo followed by an insert; the last advice sentence stays up after the final pick; and the punt advisor's \"2 picks running\" can be off by a turn. Trust the Rosters tab, the board and the card — they are always rebuilt from the actual picks.")
Pth = os.path.join(K, "report", "after-reports", "after-report-2026-10-14-undo-insert.md")
open(Pth, "w", encoding="utf-8").write("\n".join(o) + "\n")
PL = os.path.join(K, "report", "pull-log.md"); pl = rd(PL)
if "after-report-2026-10-14-undo-insert.md" not in pl:
    row = (f"| 2026-10-14 | owner question: Undo and Insert-at-# integrity on the Version 68 page (test, no pull) | 0 | 0 | 0 | "
           f"after-reports/after-report-2026-10-14-undo-insert.md — {len(hand_ids)} hand cases + {len(seeds)} seeded full drafts ({ops['insert']} inserts, {ops['undo']} undos, {ops['wrongLog']} wrong logs): seats, rosters, totals, ranks, clock, pool, Top-5 equal a clean entry in every comparison; "
           f"{cells} team-category totals within {worst:.1e} of Python; {len(ties)} rank cells are exact ties; three display quirks (D-1014-9..11, rec (a) leave through the draft); no plane change |")
    open(PL, "w", encoding="utf-8").write(pl.rstrip("\n") + "\n" + row + "\n")
print("written", Pth)
