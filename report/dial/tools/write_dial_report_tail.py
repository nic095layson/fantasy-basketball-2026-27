#!/usr/bin/env python3
"""Appends Bounds, the decision sheet, Provenance and the plain-language section to after-report-2026-10-13-dial.md,
reading every figure from the same records as write_dial_report.py."""
import json, re
K = "/home/user/fantasy-basketball-2026-27"; O = f"{K}/report/dial/out"; AR = f"{K}/report/after-reports"
P = f"{AR}/after-report-2026-10-13-dial.md"
J = lambda p: json.load(open(p, encoding="utf-8")); rd = lambda p: open(p, encoding="utf-8").read()
s = rd(P); assert "## Bounds" not in s, "tail already appended"
L = J(f"{O}/lines_dial_2026-10-13.json")["rows"]; ra = J(f"{O}/range_no_actual_after.json"); pub = J(f"{O}/publish_v65.json")
t7 = rd(f"{O}/card_compare_2026-10-13.txt"); turns, changed = re.search(r"turns compared: (\d+); 🎯 changed: (\d+)", t7).groups()
v64 = {r["n"]: r for r in J(f"{AR}/live-mock-2026-10-13/val_v64.json")}; v65 = {r["n"]: r for r in J(f"{O}/val_v65.json")}
big = [(r["player"], r["net_z"]) for r in ra["rows"] if abs(r["net_z"]) > 0.5]
tb_a = rd(f"{O}/team_budget_after.txt"); phi = re.search(r"^PHI \| \d+ \| [^|]+\| [\d.]+ \([\d.]+\) vs [\d.]+ \| ([\d.]+) ", tb_a, re.M).group(1)
vr = lambda n: f"{v64[n]['valRank']} to {v65[n]['valRank']}"
LN = {r["name"]: r for r in L}
nm = lambda n: {"LeBron James": "LeBron"}.get(n, n.split()[-1])
pp = lambda n, c="pts": f"{nm(n)} {float(LN[n]['before'][c]):g} to {float(LN[n]['new'][c]):g}"
pf = lambda n, c="ft_pct": f"{nm(n)} {float(LN[n]['before'][c]):.3f} to {float(LN[n]['new'][c]):.3f}".replace(" 0.", " .")
assert all(float(LN[n]["new"]["ft_pct"]) > float(LN[n]["before"]["ft_pct"]) for n in ("LeBron James", "Joel Embiid")), "PHI free throws not up as read"
oth = [n for n in v64 if n not in LN and v64[n]["valRank"] and (v65.get(n) or {}).get("valRank")]
mx = max(abs(v64[n]["valRank"] - v65[n]["valRank"]) for n in oth)
out = []; w = out.append
w("## Bounds\n\n**Out of scope by design.**")
small = [r for r in ra["rows"] if abs(r["net_z"]) <= 0.5]
w(f"- The {ra['players']} lines that still disagree with the three projections were not touched: {len(small)} carry half a z point or less each (A7), and the {len(big)} now just past it are D-1013-8.")
w("- No blend of seasons, no usage model and no team scaling: those are D-C2, after the draft. Philadelphia's residual is measured (§4), not modeled.")
w("- No engine, card, survival or price change; the market file is Yahoo's 10/13 paste, as on Version 64.\n")
w("**In scope and unverified.**")
w("- Whether the clamped lines are closer to what will happen — `UNVERIFIABLE` until games are played. The record behind the choice is one out-of-sample season (`after-report-2026-10-09-market.md` §4), where a copy of the prior season had more error than pre-season projections in 8 of 9 categories.")
w("- Whether the three outside sources share a blind spot on some roster — `NOT-ATTEMPTED`; a line inside their range cannot show one.")
w("- The edge of the range is the most optimistic outside view on the high side and the most pessimistic on the low side; the Contrarian's average would have moved the 13 high lines further. How much further, and what that would do to the card: `NOT-ATTEMPTED`, by the Council's choice of the edge.\n")
w("## Decision sheet (owner disposes)\n\n| id | decision question | default if silent |\n|---|---|---|")
w("| D-1013-6 | Decided 2026-10-13: the Council's sharpened option, the material lines clamped to the edge of the outside range, owner go (\"Write the report, merge both PRs, and publish Version 65\") | applied in this pass |")
w("| D-1013-8 | " + " and ".join(f"{n} ({z:+.2f})" for n, z in big) + " sit just past the 0.5 cut after the 24 moved the category frame. Clamp them too at the 10/14 lock pass? | no: both within 0.05 of the cut |")
rn65 = J("/home/user/yahoo-fantasy-basketball/arena/results/repeat_market_check_2026-10-13_v65.json"); wa = {f["player"]: f for f in rn65["flagged"]}["Kel'el Ware"]
assert wa["verdict"].startswith("LINE QUESTIONED"), "Ware verdict not as read"
w(f"| D-1013-9 | Kel'el Ware is LINE QUESTIONED on Version 65 (value rank {wa['value_rank']}; Yahoo {wa['outside']['Yahoo Rank']}, Hashtag {wa['outside']['Hashtag']}, Rotoworld {wa['outside']['Rotoworld']}, RotoBaller {wa['outside']['RotoBaller']}), one place past the bar after the 24 moved. His minutes are the consensus D-MG-3 (a) kept; his rates are his 2025-26 rates. Re-derive his rates with two dated outlets before the draft, or keep D-MG-3 (a)? | keep D-MG-3 (a) for the draft; the standing rule re-derives the line at the next projection pass |")
w("| D-1013-7 | Two build checks: the team budget, and the range check without last season as a reference | after the draft, with D-C2 |")
w("| D-C2 | The blend of seasons and the new-team usage model, including Philadelphia's residual | after the draft |")
w("| D-1013-1..5, D-SF-1..4 and earlier | carried | carried |\n")
w("## Provenance\n")
w("- Starting point: kit `main` 7c28bb3, deck `main` f6fb476 (Version 64, page sha256 a88d83f4e2f8). Selection: `usage-2026-10-13/range_check_no_actual.json`. References: `report/market/yahoo-proj-2026-10-13.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-09-29.csv`.")
w("- Tools: `report/dial/tools/` (`dial_lines.py`, `dial_apply.py`, `dial_page.py`, `board_diff.py`, `card_compare.py`, `chain_dial.sh`, `write_dial_report.py`, `write_dial_report_tail.py`). Outputs: `report/dial/out/` (the plan as written before the run, lines, apply record, build log, chain log, board diff, team budget after, range checks before and after, value ranks, identity and range records, repeat-name section, card comparison, publish record). Deck records: `arena/results/full_dom_check_2026-10-13_v65.json`, `repeat_market_check_2026-10-13_v65.json`.")
w("- The pass paused once: the environment's permission check refused commands mid-pass; the unverified changes were backed up to the scratchpad and both repositories restored, then reapplied on the owner's go and checked byte-identical to the backup.")
w(f"- Publication: {pub['line']}\n")
w("## In plain language\n")
w(f"**What changed.** 24 players' projections were pulled back inside what Yahoo, Hashtag and RotoBaller project for them. Thirteen were too high: Holiday's value rank goes {vr('Jrue Holiday')}, Brown's {vr('Jaylen Brown')}, Markkanen's {vr('Lauri Markkanen')}, Kawhi's {vr('Kawhi Leonard')}. Eight were too low and come up: Edwards {vr('Anthony Edwards')}, Mobley {vr('Evan Mobley')}, Siakam {vr('Pascal Siakam')}. Philadelphia's LeBron, Embiid and Edgecombe were brought inside the same range: their points come down a little ({pp('Joel Embiid')}, {pp('LeBron James')}, {pp('VJ Edgecombe')}), and the other moved values go to the nearer edge, so some go up, such as free throws ({pf('LeBron James')}, {pf('Joel Embiid')}). No other player's value rank on the page moved more than {mx} places.")
w(f"\n**What it does to your card.** Across the 25 practice drafts replayed on both versions, the 🎯 at your picks changes at {changed} of {turns} turns, none in round 1. Holiday and Rollins mostly stop being the pick. Late in the draft the 🎯 now often lands on Gillespie, Ware or Sheppard instead; the details are in §5.")
w(f"\n**What is left.** Philadelphia's players, added up, still claim more of the ball than any team used last season, {phi} possessions against 117.7. That needs a usage model, which waits until after the draft. Two players now sit right at the edge of the cut, and their call is D-1013-8. Ware's line is now questioned by the repeat-name check, by one place, and his call is D-1013-9.")
w("\n**Your decisions.** D-1013-8 and D-1013-9 tonight or at the lock; D-1013-7 and D-C2 after the draft.")
open(P, "a", encoding="utf-8").write("\n".join(out) + "\n")
print("tail appended")
# the pull-log row, same records
PL = f"{K}/report/pull-log.md"; pl = rd(PL)
assert "after-report-2026-10-13-dial.md" not in pl, "pull-log row already present"
row = ("| 2026-10-13 | owner go: the dial pass (D-1013-6, Council 4–1), no roster pull | 24 (both planes, stat lines only) | 0 | 0 | "
       f"after-reports/after-report-2026-10-13-dial.md — {len(L)} lines clamped category by category to the nearest edge of the Yahoo 10/13, Hashtag 10/12 and RotoBaller 9/29 range "
       f"(the 21 carrying more than 0.5 z beyond it, 13 high and 8 low, plus Philadelphia's LeBron James, Joel Embiid and VJ Edgecombe); {J(f'{O}/lines_dial_2026-10-13.json')['n_cells']} values, "
       f"shot attempts rescaled on {J(f'{O}/lines_dial_2026-10-13.json')['n_shots_rescaled']} lines; written by an asserted two-plane script; kit board, slate and gates rebuilt; deck build 7 gates; chain green; "
       f"lines outside all three projections without last season {J(f'{AR}/usage-2026-10-13/range_check_no_actual.json')['players']} to {ra['players']}, none of the 24; Philadelphia possessions {phi} against 117.7; "
       f"the card's 🎯 changes at {changed} of {turns} replayed turns; Version 65 published and byte-verified; D-1013-8 and D-1013-9 on the sheet |")
open(PL, "w", encoding="utf-8").write(pl.rstrip("\n") + "\n" + row + "\n")
print("pull-log row appended")
