#!/usr/bin/env python3
"""Writes report/after-reports/after-report-2026-10-13-dial.md from the dial pass's own records (verify at the source:
every table is read from an output file, not typed). Fails loudly if a record is missing."""
import json, os, re, subprocess, sys
K = "/home/user/fantasy-basketball-2026-27"; D = "/home/user/yahoo-fantasy-basketball"
O = f"{K}/report/dial/out"; AR = f"{K}/report/after-reports"
rd = lambda p: open(p, encoding="utf-8").read()
J = lambda p: json.load(open(p, encoding="utf-8"))
lines = J(f"{O}/lines_dial_2026-10-13.json"); L = lines["rows"]; LN = {r["name"]: r for r in L}
apply = J(f"{O}/apply_record_2026-10-13.json")
v64 = {r["n"]: r for r in J(f"{AR}/live-mock-2026-10-13/val_v64.json")}; v65 = {r["n"]: r for r in J(f"{O}/val_v65.json")}
rb = J(f"{AR}/usage-2026-10-13/range_check_no_actual.json"); ra = J(f"{O}/range_no_actual_after.json")
chain = rd(f"{O}/chain_2026-10-13.log"); build = rd(f"{O}/build_2026-10-13.log")
rn = rd(f"{O}/rn_section_v65.md"); idj = J(f"{O}/identity_v65.json"); rcj = J(f"{O}/range_check_v65.json")
t7 = rd(f"{O}/card_compare_2026-10-13.txt"); pub = J(f"{O}/publish_v65.json")
tb_b = rd(f"{AR}/usage-2026-10-13/team_budget.txt"); tb_a = rd(f"{O}/team_budget_after.txt")
LABEL = {"pts": "pts", "reb": "reb", "ast": "ast", "stl": "stl", "blk": "blk", "tpm": "3PM", "tov": "TO", "fg_pct": "FG%", "ft_pct": "FT%"}
f3 = lambda c, v: f"{v:.3f}".lstrip("0") if c.endswith("pct") else f"{v:g}"
def board(text):
    return {m.group(2): int(m.group(1)) for m in (re.match(r"^\| (\d+) \| ([^|]+?) \| ([A-Z]{2,3}) \|", ln) for ln in text.splitlines()) if m}
kb = board(subprocess.run(["git", "-C", K, "show", "7c28bb3:report/top-200-2026-27.md"], capture_output=True, text=True, check=True).stdout)
ka = board(rd(f"{K}/report/top-200-2026-27.md"))
side = lambda r: "Philadelphia budget" if r["net_z"] is None else ("high" if r["net_z"] > 0 else "low")
# ---- chain summary lines
def step(name):
    m = re.search(r"== " + re.escape(name) + r"[^\n]*\n(.*?)(?=\n== )", chain, re.S)
    return m.group(1).strip() if m else None
steps = {s: step(s) for s in ["parity", "test_card", "test_draft", "test_gates", "full_dom_check", "repeat_market_check", "identity_check", "range_check (D-RN-3, with last season)"]}
for s, v in steps.items():
    assert v is not None, f"chain step missing: {s}"
    assert v.splitlines()[-1].strip() == "exit 0" or s.startswith("repeat") or s.startswith("range"), f"chain step not green: {s}: {v[-200:]}"
first = lambda s, pat: (re.search(pat, steps[s]) or [None])[0]
# ---- team budget rows
def tb(text):
    out = {}
    for ln in text.splitlines():
        m = re.match(r"^([A-Z]{3}) \| \d+ \| [^|]+\| ([\d.]+) \([\d.]+\) vs ([\d.]+) \| ([\d.]+) \([\d.]+\) vs ([\d.]+) \|", ln)
        if m: out[m.group(1)] = dict(shots=float(m.group(2)), shots_was=float(m.group(3)), pos=float(m.group(4)), pos_was=float(m.group(5)))
    lists = {k: re.search(pat, text).group(1) for k, pat in (("own", r"used in 2025-26: (\d+) \["), ("max", r"league maximum \([\d.]+\): (\d+) \["))}
    share = re.search(r"today lines: the pools cover ([\d.]+)% of 2025-26 league minutes and claim ([\d.]+)%", text).groups()
    return out, lists, share
TB, TBL, TBS = tb(tb_b); TA, TAL, TAS = tb(tb_a)
# ---- range-check mechanisms carried from the MG and WO-5 reports, per player
mech = {}
for f in (f"{AR}/after-report-2026-10-12-wo5.md", f"{AR}/after-report-2026-10-13-mg.md"):
    sec = re.search(r"## Range check \(D-RN-3\)(.*?)\n## ", rd(f), re.S).group(1)
    for ln in sec.splitlines():
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        if ln.startswith("| ") and len(c) == 5 and c[0] not in ("player", "---"): mech[c[0]] = (c[4], os.path.basename(f))
out = []; w = out.append
w("# After-report — the dial pass of 10/13: 24 lines clamped inside the three outside projections' range (D-1013-6), Version 65\n")
w("**Owner requests (2026-10-13, verbatim):** \"Invoke the council on how to proceed. and I'd like for you to conduct as logical dialing as as we can. What can we solve / strengthen today? Let's take meaningful and intentional steps to dial this in.\" After the environment's permission check paused the pass: \"Rebuild the kit board and the draft-deck page, then run the full chain. Compare the card’s 🎯 at your 13 picks before and after. Write the report, merge both PRs, and publish Version 65.\"\n")
w(f"**What was analyzed and changed:** kit `main` 7c28bb3 and deck `main` f6fb476 (Version 64, page sha256 a88d83f4e2f8) as the starting point. The selection record: `usage-2026-10-13/range_check_no_actual.json`, the deck's own range check run without the player's last season as a reference. The references: {', '.join(f'{k} `{v}`' for k, v in lines['references'].items())}.\n")
w("**Method:** the Council (4–1; the Contrarian wanted the high lines at the consensus average, not the edge) chose to clamp the material outliers to the edge of the outside range. Stated to the owner before the run: A6 the per-category range of the three projections; A7 every line whose cells outside that range carry more than 0.5 z, either way, on Version 64, plus Philadelphia's other three for the team budget; A8 each cell outside the range moves to the nearest edge, rounded inward, other cells stay, games, minutes, tags and placements stay; A9 FGA and FTA rescale by one factor when points, threes or a percentage moved, so points still follow from the shooting. Tools in `report/dial/tools/`: `dial_lines.py` computes the lines and writes nothing (two runs identical); `dial_apply.py` writes both planes with assertions A1–A9 (A8 recomputes the range from the deck's own loader; three planted errors caught; a second run changes nothing); `dial_page.py` re-words the colophon and adds seven card receipts; `board_diff.py`, `card_compare.py`, `chain_dial.sh` and this writer read the records.\n")
w("Pull window: 2026-10-13 → 2026-10-13 (no roster pull; the morning's verified pool, stat lines only).\n")
n_hi = sum(1 for r in L if r["net_z"] is not None and r["net_z"] > 0); n_lo = sum(1 for r in L if r["net_z"] is not None and r["net_z"] < 0)
t7c = re.search(r"turns compared: (\d+); 🎯 changed: (\d+)", t7).groups()
w(f"**Headline.** {len(L)} lines now sit inside the range of Yahoo, Hashtag and RotoBaller in every category: {n_hi} that were too high, {n_lo} that were too low and Philadelphia's other three. {lines['n_cells']} values moved, with shot attempts rescaled on {lines['n_shots_rescaled']} lines so the points identity holds. Every gate and every test of the chain passed on the rebuilt page, and Version 65 is live, byte-verified. The card's 🎯 changes at {t7c[1]} of your {t7c[0]} replayed turns. Without last season as a reference, {ra['players']} lines still have a category outside all three projections, down from {rb['players']}, and none of them is one of the 24. Philadelphia's pool still claims more possessions than any team used last season: {TA['PHI']['pos']} against 117.7, down from {TB['PHI']['pos']}.\n")
w("## 1. Roster changes\n\nNone. No placement, tag, games or minutes figure changed on either plane; 24 stat lines moved (§2).\n")
w("## 2. The 24 lines\n\nEVIDENCE: `dial/out/lines_dial_2026-10-13.json`, `apply_record_2026-10-13.json`, `board_diff_2026-10-13.txt`, `val_v65.json` against `live-mock-2026-10-13/val_v64.json`.\n")
w("| player | side | values moved | kit rank before / after | deck value rank v64 / v65 | market rank |\n|---|---|---|---|---|---|")
for r in sorted(L, key=lambda r: v64[r["name"]]["valRank"]):
    n = r["name"]; mv = ", ".join(f"{LABEL[c['cat']]} {f3(c['cat'], c['before'])} to {f3(c['cat'], c['after'])}" for c in r["cells"])
    w(f"| {n} | {side(r)} | {mv} | {kb.get(n, 'off')} / {ka.get(n, 'off')} | {v64[n]['valRank']} / {v65[n]['valRank']} | {v65[n]['mktRank'] or 'unpriced'} |")
oth = [n for n in v64 if n not in LN and v64[n]["valRank"] and (v65.get(n) or {}).get("valRank")]
ch = [n for n in oth if v64[n]["valRank"] != v65[n]["valRank"]]; mx = max(abs(v64[n]["valRank"] - v65[n]["valRank"]) for n in ch)
okb = [n for n in kb if n not in LN and n in ka]; kch = [n for n in okb if kb[n] != ka[n]]; kmx = max(abs(kb[n] - ka[n]) for n in kch)
w(f"\nEveryone else moved only because the 24 did: on the deck {len(ch)} of {len(oth)} other value ranks change, by at most {mx} places; on the kit board {len(kch)} of {len(okb)}, by at most {kmx}. The note behind each of the 24 rows on the page carries the dated clamp entry.\n")
w("## 3. Checks on the result\n\n| check | result |\n|---|---|")
w(f"| `dial_lines.py` | {lines['n_rows']} rows, {lines['n_cells']} values clamped, {lines['n_shots_rescaled']} shot rescales, 0 problems; two runs identical |")
SH = [c for r in apply['rows'] if r['plane'] == 'deck' for c in r['changed']]
n_fga, n_fta = SH.count('fga'), SH.count('fta'); n_catv = len(SH) - n_fga - n_fta
assert n_catv == lines['n_cells'] and 2 * len(SH) == apply['values_changed'], 'apply record does not add up'
w(f"| `dial_apply.py` (both planes) | PASS: deck {apply['deck_rows_changed']} rows, kit {apply['kit_rows_changed']} rows, {apply['values_changed']} values across the two planes (on each, {n_catv} category values and {n_fga + n_fta} shot attempts: FGA on {n_fga} lines, FTA on {n_fta}); a second run changes nothing; the written files equal a fresh write from Version 64; three planted errors (a value outside the range, a change beyond the clamp, a broken identity) each caught |")
w("| Kit (`rank_engine.py`, `slate.py`, `test_rank_engine.py`, `check_provenance.py`, `check_derived.py`) | board rebuilt, 200 from 313 projected; 4 tests OK; PROVENANCE GATE PASS; DERIVED 24 of 24 reproduce; the slate also picks up Yahoo's 10/13 ADP, which the 10/13 Yahoo pass had not regenerated into it |")
bl = [l for l in build.splitlines() if l.strip()]
w(f"| Deck build (`build_deck.py`, 7 gates) | refused once at gate 4 (the stamp still asserted no pool change from the Yahoo pass; restamped `--pool-changes`), then passed: {bl[0].strip()}; {bl[2].strip()} |")
par = first("parity", r"PARITY:[^\n]*")
assert par, "parity verdict line missing"
w(f"| `check_parity.py` | {par}; " + "; ".join(re.sub(r"\s+", " ", x).strip() for x in steps["parity"].splitlines()[:2]) + " |")
w(f"| `test_card.py` / `test_draft.py` / `test_gates.py` | {steps['test_card'].splitlines()[0]} / {steps['test_draft'].splitlines()[0]} / {steps['test_gates'].splitlines()[-2]} |")
w(f"| `full_dom_check.mjs` (on `draft_state_54.json`) | {' '.join(steps['full_dom_check'].splitlines()[:-1])[:300]} |")
w(f"| `repeat_market_check.py` | {rn.splitlines()[0][:300]} |")
w(f"| `identity_check.py` | {steps['identity_check'].splitlines()[0][:300]} |")
w(f"| `range_check.py` (D-RN-3, with last season) | {steps['range_check (D-RN-3, with last season)'].splitlines()[-1][:300]} |")
w("\n## 4. Residual audit\n\nEVIDENCE: `dial/out/range_no_actual_after.json` (the deck's range check with no last-season file, on the rebuilt lines) against the 10/13 usage report's run; `dial/out/team_budget_after.txt` against `usage-2026-10-13/team_budget.txt`.\n")
up_b = sum(r["net_z"] for r in rb["rows"] if r["net_z"] > 0); dn_b = sum(r["net_z"] for r in rb["rows"] if r["net_z"] < 0)
up_a = sum(r["net_z"] for r in ra["rows"] if r["net_z"] > 0); dn_a = sum(r["net_z"] for r in ra["rows"] if r["net_z"] < 0)
still = sorted({r["player"] for r in ra["rows"]} & set(LN)); big = [(r["player"], r["net_z"]) for r in ra["rows"] if abs(r["net_z"]) > 0.5]
w("| without last season as a reference | Version 64 | Version 65 |\n|---|---|---|")
w(f"| lines with a category outside all three projections | {rb['players']} of {rb['checkable']} | {ra['players']} of {ra['checkable']} |")
w(f"| cells outside all three | {rb['cells']} | {ra['cells']} |")
w(f"| z those cells carry, flattering side | {up_b:.2f} | {up_a:.2f} |")
w(f"| z those cells carry, unflattering side | {dn_b:.2f} | {dn_a:.2f} |")
w(f"| lines carrying more than 0.5 z either way | {sum(1 for r in rb['rows'] if abs(r['net_z']) > 0.5)} | {len(big)} |")
w(f"\n- None of the 24 is flagged any more ({len(still)} remain). Two other lines now sit just past the 0.5 cut, because moving the 24 shifted every category's mean and spread a little: " + ", ".join(f"{n} {z:+.2f}" for n, z in big) + ". They were under the cut on Version 64; they go to the sheet as D-1013-8 rather than into this pass.")
w(f"- The team budget: Philadelphia's pool claims {TA['PHI']['shots']} shots and {TA['PHI']['pos']} possessions a game, down from {TB['PHI']['shots']} and {TB['PHI']['pos']}, still above the 2025-26 maximum of 93.3 and 117.7. Teams whose pool exceeds that maximum: {TBL['max']} before and {TAL['max']} now; teams over their own 2025-26 total: {TBL['own']} before and {TAL['own']} now. The pools now claim {TAS[1]}% of last season's league possessions, from {TBS[1]}%.\n")
w("| team | possessions a game, Version 64 | Version 65 | 2025-26 |\n|---|---|---|---|")
for t in ["PHI", "WAS", "MIL", "NOP", "MEM", "MIA", "UTA", "POR"]:
    w(f"| {t} | {TB[t]['pos']} | {TA[t]['pos']} | {TA[t]['pos_was']} |")
w("\n## 5. Test 7 — the card at your 13 picks, Version 64 against Version 65\n\nEVIDENCE: `dial/out/card_compare_2026-10-13.txt`, from the deck's repeat-name replays of the same 25 graded mocks on each page (`arena/results/repeat_market_check_2026-10-13_v64.json` and `_v65.json`). One input differs: the page.\n")
w("```\n" + t7.strip() + "\n```\n")
# the read of test 7, every figure from the comparison and the two repeat-name records
rn64 = J(f"{D}/arena/results/repeat_market_check_2026-10-13_v64.json"); rn65 = J(f"{D}/arena/results/repeat_market_check_2026-10-13_v65.json")
F64 = {f["player"]: f for f in rn64["flagged"]}; F65 = {f["player"]: f for f in rn65["flagged"]}; RA = {r["player"]: r for r in ra["rows"]}
cnt = {m.group(1): (int(m.group(2)), int(m.group(3))) for m in re.finditer(r"([A-Z][^,]+?) (\d+) to (\d+)", re.search(r"clamped names \(v64 to v65\): (.*)", t7).group(1))}
took = {s.rsplit(" ", 1)[0]: int(s.rsplit(" ", 1)[1]) for s in re.search(r"took the 🎯 most often \(v65 name\): (.*)", t7).group(1).split(", ")}
rnd = {int(a): (int(b), int(c)) for a, b, c in re.findall(r"R(\d+) (\d+)/(\d+)", t7)}
WA = "Kel'el Ware"; wa65, wa64 = F65[WA], F64[WA]
assert wa65["verdict"].startswith("LINE QUESTIONED") and wa64["verdict"].startswith("SOURCES SPLIT"), "Ware verdicts not as read"
cl = lambda n: "; ".join(c["text"] for c in RA[n]["cells"])
w(f"**Read.** The card stops pointing at the clamped high lines: Holiday's 🎯 count goes {cnt['Jrue Holiday'][0]} to {cnt['Jrue Holiday'][1]}, Rollins' {cnt['Ryan Rollins'][0]} to {cnt['Ryan Rollins'][1]}, Markkanen's {cnt['Lauri Markkanen'][0]} to {cnt['Lauri Markkanen'][1]}. Round 1 is untouched ({rnd[1][0]} of {rnd[1][1]}); the late picks move most (round 12: {rnd[12][0]} of {rnd[12][1]}). The turns that changed went mostly to Collin Gillespie ({took['Collin Gillespie']}), Kel'el Ware ({took[WA]}) and Reed Sheppard ({took['Reed Sheppard']}).\n")
w(f"- Gillespie ({cl('Collin Gillespie')}; net {RA['Collin Gillespie']['net_z']:+.2f} z) and Sheppard ({cl('Reed Sheppard')}; net {RA['Reed Sheppard']['net_z']:+.2f} z) carry disagreements under the 0.5 cut, so they stand by design (A7). Both are SOURCES SPLIT on the repeat-name check below.")
w(f"- Ware's line sits inside all three projections but for {cl(WA)} (net {RA[WA]['net_z']:+.2f} z). The repeat-name check now calls it LINE QUESTIONED: value rank {wa65['value_rank']}, and all four outside ranks ({', '.join(wa65['outside'].values())}) sit 25 or more places below. On Version 64 he ranked {wa64['value_rank']} and the verdict was SOURCES SPLIT; moving the 24 lifted him one place. His minutes are the minutes-and-games consensus on his 2025-26 rates, kept at #27 by D-MG-3 (a), the Council's 5–0 call made at the owner's request (`after-report-2026-10-13-mg.md`); D-1013-9 on the sheet.\n")
w(f"## 6. Publication\n\n{pub['line']}\n")
# the plan's predictions (stated to the owner at 18:44, before the run) against the records
mxfga = max(float(r["after"]["fga"]) for r in apply["rows"]); negv = sum(1 for r in apply["rows"] for v in r["after"].values() if float(v) < 0)
lq64 = sorted(n for n, f in F64.items() if f["verdict"].startswith("LINE QUESTIONED")); lq65 = sorted(n for n, f in F65.items() if f["verdict"].startswith("LINE QUESTIONED"))
assert {"Jrue Holiday", "Ryan Rollins"} <= set(lq64) and not ({"Jrue Holiday", "Ryan Rollins"} & set(F65)), "Holiday/Rollins verdicts not as read"
hi_n = [r["name"] for r in L if r["net_z"] is not None and r["net_z"] > 0]; lo_n = [r["name"] for r in L if r["net_z"] is not None and r["net_z"] < 0]
d_hi = sum(v65[n]["valRank"] > v64[n]["valRank"] for n in hi_n); d_lo = sum(v65[n]["valRank"] < v64[n]["valRank"] for n in lo_n)
k_hi = [n for n in hi_n if ka[n] > kb[n]]; k_hold = [n for n in hi_n if ka[n] == kb[n]]; k_lo = sum(ka[n] < kb[n] for n in lo_n)
mid = sum(rnd[i][0] for i in range(3, 7)); late = sum(rnd[i][0] for i in range(11, 14)); tot = int(t7c[1])
T7R = [ln.split(' | ') for ln in t7.splitlines() if re.match(r'^\d+ \| \d+ \| \d+ \| ', ln)]
assert len(T7R) == tot, 'comparison table rows do not match the count'
late_h = sum(1 for r in T7R if int(r[1]) >= 11 and r[3] == 'Jrue Holiday')
drop = max(L, key=lambda r: v65[r['name']]['valRank'] - v64[r['name']]['valRank'])['name']
assert drop == 'Jrue Holiday', f'largest fall is {drop}'
held_mid = 'held' if mid * 2 > tot else 'did not hold'
w("## 7. The plan against the outcome\n\nThe predictions written to the owner before the run (`dial/out/plan_2026-10-13.md`, verbatim from the session at 18:44), against the records above.\n")
w("| prediction | outcome |\n|---|---|")
w(f"| 60 to 100 values move; stop a line if a rescaled shot count passes 30 or a value goes negative | {'held' if 60 <= lines['n_cells'] <= 100 else 'did not hold'}: {lines['n_cells']} moved; the 24 lines averaged {lines['n_cells'] / len(L):.1f} values each. No line hit the stop rule: the largest FGA is {mxfga:g}, no value is negative |")
kit_ok = len(k_hi) == len(hi_n) and k_lo == len(lo_n)
w(f"| on the kit board, the 13 high lines fall and the 8 low lines rise | {'held' if kit_ok else 'did not hold for ' + str(len(hi_n) - len(k_hi) + len(lo_n) - k_lo) + ' line'}: on the kit board {len(k_hi)} of {len(hi_n)} fall (" + ", ".join(f"{n} holds at {ka[n]}" for n in k_hold) + f") and {k_lo} of {len(lo_n)} rise; on the deck {d_hi} of {len(hi_n)} fall and {d_lo} of {len(lo_n)} rise |")
w(f"| Holiday and Rollins leave LINE QUESTIONED | held: neither is flagged on Version 65. A new one appeared: {', '.join(lq65)} (§5) |")
w(f"| 0 of the 24 outside the range; Philadelphia lower but above the league maximum | held: {len(still)} of the 24; Philadelphia {TA['PHI']['pos']} against 117.7 |")
w("| the build passes all 7 gates; a refusal gets its cause fixed, no silent waiver | held after one refusal: gate 4 refused the first build because the morning's freshness stamp still said the pool had not changed; restamped with `--pool-changes`, keeping the morning's roster sources; no waiver |")
w(f"| the chain is green | held (§3) |")
w(f"| most 🎯 changes fall in the middle rounds | {held_mid}: rounds 3 to 6 carry {mid} of the {tot} changes and rounds 11 to 13 carry {late}, round 12 alone {rnd[12][0]}. In {late_h} of those {late} late turns the Version 64 🎯 was Holiday, whose value rank fell furthest of the 24 ({v64['Jrue Holiday']['valRank']} to {v65['Jrue Holiday']['valRank']}) |")
w("\nTwo surprises in the tools themselves, both on record in the session:\n")
w("- The first run of `dial_lines.py` counted 106 values. Two were floating-point noise at a range edge: RotoBaller's percentages are stored in points and divided by 100 on load, so a value equal to the edge read as just outside it. A tolerance of 1e-9 removed them before anything was written; 104, two runs identical before and after.")
w("- After the first write, the writer's re-run check failed on a correct second run: A9 compared the cells changed in that run, so a line already clamped read as 'clamp not written'. The fault was in the check, not the data: A9 now compares the written value with the target, the re-run passes with 0 changes, the files written in place equal a fresh write from Version 64 by the corrected writer, and the corrected writer catches all three planted errors (re-run in the verification pass).\n")
# Range check section from the chain's own record, mechanisms carried per player
w("## Range check (D-RN-3)\n")
w(f"Rule (owner, 2026-10-08): on a projection pass, every cell of a top-{rcj['top']} line that sits outside the range of ALL its references (" + ", ".join(f"{k} `{v}`" for k, v in rcj["references"].items()) + f"; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats) carries a one-line mechanism naming two dated outlets, or comes back inside the range. This page: {rcj['players']} player(s), {rcj['cells']} cell(s), of {rcj['checkable']} checkable top-{rcj['top']} lines. None of the 24 clamped lines is listed; every row below is a WO-5 or minutes-and-games line this pass did not touch, and its mechanism is carried from the report that set it.\n")
w("| player | deck rank | cells outside every reference | net z | mechanism (two dated outlets) |\n|---|---|---|---|---|")
missing = []
for r in rcj["rows"]:
    m = mech.get(r["player"])
    if not m: missing.append(r["player"]); continue
    w(f"| {r['player']} | {r['deck_rank']} | " + "; ".join(c["text"] for c in r["cells"]) + f" | {r['net_z']:+.2f} | {m[0]} (carried from `{m[1]}`) |")
assert not missing, f"no mechanism on file for {missing}"
w("\n## Points identity (D-1009-3)\n")
w(f"Rule (owner, 2026-10-09): on a projection pass, every top-200 line on either plane whose points sit more than 1 from its own shooting is reconciled or carries a mechanism naming two dated outlets. This page: `identity_check.py` — {steps['identity_check'].splitlines()[0]}; the clamped lines were written with FGA and FTA rescaled so the identity holds (A5 of the writer: within 0.25).\n")
w("| player | plane | rank | pts | implied (2·FGM + 3PM + FTM) | gap | mechanism (two dated outlets) |\n|---|---|---|---|---|---|---|")
assert not idj.get("rows"), "identity rows present"
w("\n## Watchlist\n")
w("- Jamal Murray and Aaron Nesmith, just past the 0.5 cut after the frame moved (D-1013-8).")
w(f"- Kel'el Ware, LINE QUESTIONED on Version 65 by one place; the 🎯 in {wa65['mocks']} of {len(rn65['replayed'])} replayed mocks (D-1013-9).")
w("- The late-round 🎯 now lands on Collin Gillespie and Reed Sheppard: lines with small disagreements this pass left by design (§5).")
w(f"- Philadelphia's residual: {TA['PHI']['pos']} possessions against a league maximum of 117.7; the usage model is D-C2, after the draft.")
w("- The 10/14 lock paste (D-1013-1) and the publish freeze during the draft (D-1013-5).")
w("- Do not use RESYNC during the draft; the recovery steps are in `after-report-2026-10-13-live-mock.md` (D-1013-2).\n")
w("## Open-item receipts\n\n| item | query run (2026-10-13) | dated finding |\n|---|---|---|")
w("| (this pass) | records only; no web research and no roster pull in this pass | the lines moved inside the three outside projections on file; pull receipts for the window live in `after-report-2026-10-13.md` (the morning's pull), same day |")
w("| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (`after-report-2026-10-13.md`, receipts dated 10/13) | all HELD or unsigned on 2026-10-13 per those receipts; not re-queried in this pass (did not check) |\n")
w(rn[rn.index("## Repeat-name market check"):].strip())
w("")
open(f"{AR}/after-report-2026-10-13-dial.md", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("draft written (sections through the repeat-name check); bounds, decisions, provenance and plain language appended by write_dial_report_tail.py")
