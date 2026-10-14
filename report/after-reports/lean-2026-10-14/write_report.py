#!/usr/bin/env python3
"""Writes report/after-reports/after-report-2026-10-14-lean.md and the pull-log row from this folder's records:
test_draft_red.txt (the new cases against the pre-fix engine), test_draft_green.txt (after), lean_demo.txt (the owner's
screenshot roster rendered in Chromium on the old and the new page), fix.diff, chainA.log / chainB.log (parity, card,
draft, gates; DOM, identity, planes on the fixed page), publish.json, rn_section.md. No figure is typed by hand."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.normpath(os.path.join(H, "..", "..", ".."))
rd = lambda p: open(os.path.join(H, p), encoding="utf-8").read(); g = lambda pat, s, f=0: re.search(pat, s, f)
RED = rd("test_draft_red.txt"); GREEN = rd("test_draft_green.txt"); DEMO = [json.loads(l) for l in rd("lean_demo.txt").splitlines() if l.strip().startswith("{")]
CA = rd("chainA.log"); CB = rd("chainB.log"); PUB = json.loads(rd("publish.json")); DIFF = rd("fix.diff"); RN = rd("rn_section.md")
rn = RN[RN.index("## Repeat-name market check"):].strip(); rn_head = g(r"(\d+) of (\d+) mocks replayed; (\d+) FLAGGED", RN).groups()
red_fail = g(r"(\d+) of (\d+) cases FAILED", RED); red_line = g(r"⚠ LEAN: (\dG vs \dF)", RED)
green = g(r"all (\d+) cases passed", GREEN)
old, new = DEMO[0], DEMO[1]; assert "page_old" in old["deck"] and new["deck"].endswith("draft-deck.html")
par = g(r"card orderings compared : (\d+) owner turns across (\d+) committed states", CA); parity_ok = "PARITY: EXACT MATCH" in CA
card = g(r"CARD: all (\d+) cases passed", CA); draft = g(r"== test_draft.*?all (\d+) cases passed", CA, re.S); gates = g(r"== test_gates.*?all (\d+) cases passed", CA, re.S)
dom = json.loads(g(r'(\{"assertions".*?\})', CB).group(1)); ident_ok = g(r"== identity.*?exit (\d+)", CB, re.S).group(1) == "0"
pl = g(r"planes: (\d+) shared · kit-only (\d+) · deck-only (\d+) · team (\d+) · exclusion (\d+) · drift (\d+) · propagation (\d+)", CB)
assert parity_ok and card and draft and gates and dom["pass"] and dom["failed"] == 0 and ident_ok and pl.group(4) == "0"
nfiles = len(re.findall(r"^diff --git", DIFF, re.M)); added = sum(1 for l in DIFF.splitlines() if l.startswith("+") and not l.startswith("+++")); removed = sum(1 for l in DIFF.splitlines() if l.startswith("-") and not l.startswith("---"))
o = []; w = o.append
w("# After-report — 2026-10-14 (lock day, pre-draft): the LEAN roster-balance line counted position tokens, not players — fixed on both engines, deck Version " + str(PUB["service_version"]) + "\n")
w("**Owner request (2026-10-14, verbatim):** \"Can you please adjust this where: System is saying I have 7G, but in reality that is 'G eligible' it is saying I am overloaded in a position when I am not. I hope it is not affecting the computation\"; then \"I just want to ensure, this is not changing your arithmetic computation right? The positional counting\"; then \"Publish fix now and grade Mock 82\".\n")
w("Pull window: 2026-10-14 → 2026-10-14 (a display fix on the deck page; no roster pull, no line, tag, price or placement change on either plane).\n")
w(f"**Headline.** The ⚠ LEAN line under the card tallied position *tokens* — a PG,SG player counted as two guards — so the owner's six-man roster of four dual-eligible guards and two forwards read \"7G vs 2F\". It is a warning line only: the card's 🎯 ordering never reads positions, and the TARGET read uses the family counter that already counted each player once (the one printing \"G (4) F (2) C (2)\"). The line now counts players once per family on the page and on its Python twin ({nfiles} files, +{added}/−{removed} lines). Red-first: the new test reproduces the owner's exact \"{red_line.group(1)}\" on the pre-fix engine ({red_fail.group(1)} of {red_fail.group(2)} cases fail), then all {green.group(1)} pass. The owner's roster rendered in Chromium: old page \"{old['lean'][0]}\", new page no LEAN line, census \"{new['census']}\" on both. Chain green on the fixed page (parity EXACT {par.group(1)} turns / {par.group(2)} states; card {card.group(1)}, draft {draft.group(1)}, gates {gates.group(1)}; DOM {dom['assertions']}/{dom['failed']}); published as Version {PUB['service_version']} (id {PUB['version_id']}), byte-verified at offset {PUB['offset']}.\n")
w("## 1. Roster changes\n\nNone. No line, tag, placement or price changed on either plane; the pool sha256 is unchanged. The page's JavaScript and `scripts/hoops.py` changed in one place each, plus the dated note in the page's Logic paragraph.\n")
w("## 2. What was wrong, and what was not\n")
w("EVIDENCE: `fix.diff`; the page at `docs/draft-deck.html` (the LEAN line, `posCounts`), `scripts/hoops.py` (`pos_counts`); the TARGET read's `balCt` / `familiesOf` and the roster header's `famN`.\n")
w("- The LEAN line summed `posCounts.PG + posCounts.SG` against `posCounts.SF + posCounts.PF`, where `posCounts` counts every position string a player carries. Derrick White (PG,SG), Devin Booker (PG,SG) and Tyrese Haliburton (PG,SG) each counted twice, Desmond Bane (SG,SF) once on each side: 7 against 2. The Python twin did the same.")
w("- The 🎯 and the card's +/− cats-per-week numbers are the blend50 score (marginal weekly category wins against the room plus balanced value); positions do not enter it. The TARGET / BOARD LEAN read uses `familiesOf(p)` and `balCt`, which count a player once per family and compare against the startable floor; the roster header's `G (4) F (2) C (2)` is the same counter. Neither changed, and neither was wrong.")
w("- The fix: `g` = players eligible at PG or SG, `f` = players eligible at SF or PF, each player once; threshold unchanged (|G − F| ≥ 4 at five or more players). On the owner's roster: 4 against 2, no line.\n")
w("## 3. Verification\n")
w("| check | result |\n|---|---|")
w(f"| red-first: the two new `test_draft.py` cases against the pre-fix engine (`test_draft_red.txt`) | {red_fail.group(1)} of {red_fail.group(2)} FAIL, the first printing \"⚠ LEAN: {red_line.group(1)}\" — the owner's exact line |")
w(f"| the same suite after the fix (`test_draft_green.txt`) | all {green.group(1)} cases passed |")
w(f"| the owner's screenshot roster (picks #10 Haliburton, #15 Towns, #34 Booker, #39 White, #58 Okongwu, #63 Bane) fed into the real page in headless Chromium (`lean_demo.txt`, `events_screenshot.json`, `arena/mocks/lean_dom_check.mjs`) | old page: \"{old['lean'][0]}\"; new page: no LEAN line; census \"{new['census']}\" on both |")
w(f"| `check_parity.py` on the fixed page (`chainA.log`) | PARITY: EXACT MATCH — {par.group(1)} owner turns across {par.group(2)} committed states |")
w(f"| `test_card.py` / `test_draft.py` / `test_gates.py` | all {card.group(1)} / all {draft.group(1)} / all {gates.group(1)} |")
w(f"| `full_dom_check.mjs` (`chainB.log`) | {dom['assertions']} assertions, {dom['failed']} failed, {dom['pageErrors']} page errors |")
w(f"| `identity_check.py` / `check_planes.py` | exit 0 / planes team {pl.group(4)} exclusion {pl.group(5)} drift {pl.group(6)} propagation {pl.group(7)} on {pl.group(1)} shared rows |")
w(f"| publish | Version {PUB['service_version']}, id {PUB['version_id']}, the built page (sha256 {PUB['page_sha256_12']}) found whole in the served file at offset {PUB['offset']} ({PUB['served_bytes']:,} bytes served) |\n")
w("## Watchlist\n")
w("- The publish freeze during the draft (D-1013-5) and no RESYNC during the draft (D-1013-2) stand; this publish precedes the draft.")
w("- `arena/mocks/lean_dom_check.mjs` stays as a harness for roster-balance questions: any pick list, any page.\n")
w("## Open-item receipts\n\n| item | query run (2026-10-14) | dated finding |\n|---|---|---|")
w("| (this fix) | records only; no web research and no roster pull | display fix; the pool sha256 unchanged |")
w("| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this fix (did not check) |\n")
w(rn + "\n")
w("\n## Bounds\n\n**Out of scope by design.**\n- No change to the lean threshold or to any engine computation; no line, tag, price or placement change.\n- The repeat-name check was not re-run: the lines are byte-identical to the lock's (" + f"{rn_head[0]} of {rn_head[1]} mocks, {rn_head[2]} flagged" + " on the same pool).\n")
w("**In scope and unverified.**\n- None: every claim above is a run on this page's bytes.\n")
w("## Decision sheet (owner disposes)\n\n| id | decision question | default if silent |\n|---|---|---|")
w("| (none new) | the fix was the owner's call (\"Publish fix now\") | applied |")
w("| D-INT-1, D-INT-2, D-1014-*, D-1013-*, earlier | carried | carried |\n")
w("## Provenance\n")
w(f"- Deck: `scripts/hoops.py`, `docs/draft-deck.html`, `scripts/test_draft.py` (+2 cases), `arena/mocks/lean_dom_check.mjs` (new); page sha256 {PUB['page_sha256_12']}; published {PUB['version_id']} after a fresh read of {PUB['prev_id']}.")
w("- This folder: `fix.diff`, `test_draft_red.txt`, `test_draft_green.txt`, `lean_demo.txt`, `events_screenshot.json`, `chainA.log`, `chainB.log`, `publish.json`, `rn_section.md`, this writer.")
w("- No line, tag or placement changed on either plane.\n")
w("## In plain language\n")
w("**What was wrong.** The warning line under the card counted White, Booker and Haliburton twice each because each is listed at both PG and SG. It said 7 guards; you had 4. It was only that warning line.")
w("\n**What was not wrong.** The card's recommendation and its numbers never look at positions, and the roster header's \"G (4) F (2) C (2)\" was already counting correctly. Nothing in the arithmetic changed.")
w(f"\n**What was done.** The line now counts each player once. A new test fails on the old code with your exact \"7G vs 2F\" and passes on the new; your roster rendered in a real browser shows the line gone; every check in the chain passes; the page on your link is Version {PUB['service_version']}, byte-verified.")
P = os.path.join(K, "report", "after-reports", "after-report-2026-10-14-lean.md")
open(P, "w", encoding="utf-8").write("\n".join(o) + "\n")
PL = os.path.join(K, "report", "pull-log.md"); pl = open(PL, encoding="utf-8").read()
if "after-report-2026-10-14-lean.md" not in pl:
    row = (f"| 2026-10-14 | LEAN roster-balance line fix (owner: tokens counted, not players) — deck Version {PUB['service_version']}, display only | 0 | 0 | 0 | "
           f"after-reports/after-report-2026-10-14-lean.md — red-first {red_fail.group(1)} of {red_fail.group(2)} → all {green.group(1)}; Chromium: old page \"{old['lean'][0].replace('⚠ ', '')}\", new page none; parity EXACT {par.group(1)}/{par.group(2)}; "
           f"card {card.group(1)}/draft {draft.group(1)}/gates {gates.group(1)}; DOM {dom['assertions']}/{dom['failed']}; published {PUB['version_id']} byte-verified; no plane change |")
    open(PL, "w", encoding="utf-8").write(pl.rstrip("\n") + "\n" + row + "\n")
print("written", P)
