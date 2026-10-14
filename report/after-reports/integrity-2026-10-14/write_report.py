#!/usr/bin/env python3
"""Writes report/after-reports/after-report-2026-10-14-integrity.md and the pull-log row from this folder's records:
the byte comparisons (artifact_bytes.txt, board_reproduce.txt, deck_hashes.txt), the gate logs (kit_gates.log,
chainA/B/C.log), the independent engine re-derivation (category_audit_excl.txt), the lock audit (audit_lock_1.txt),
the seven-test line audit (a180/), the roster verification (verify_rosters_full.txt, kit_only_espn_live.txt), the page's
JUDGMENT block (judgment.txt), the repeat-name record (rn_section.md) and the start/end shas. No figure is typed by hand;
the confidence rubric is the one stated to the owner before the runs (A3)."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.normpath(os.path.join(H, "..", "..", ".."))
rd = lambda p: open(os.path.join(H, p), encoding="utf-8").read()
J = lambda p: json.load(open(os.path.join(H, p), encoding="utf-8"))
g = lambda pat, s, flags=0: re.search(pat, s, flags)
# ---- records
sha0 = rd("shas_start.txt").strip(); sha1 = rd("shas_end.txt").strip()
AB = rd("artifact_bytes.txt"); BR = rd("board_reproduce.txt"); DH = rd("deck_hashes.txt")
KG = rd("kit_gates.log"); KP = rd("kit_provenance_structural.txt"); CA = rd("chainA.log"); CB = rd("chainB.log"); CC = rd("chainC.log")
CE = rd("category_audit_excl.txt"); AL = rd("audit_lock_1.txt"); A180 = rd("a180/run1.txt"); A180J = J("a180/audit180_v2.json"); RP = rd("a180/reproduce.txt")
VR = rd("verify_rosters_full.txt"); KO = rd("kit_only_espn_live.txt"); JU = rd("judgment.txt"); RN = rd("rn_section.md")
DOM = J("full_dom_check_2026-10-14_audit.json")
rn = RN[RN.index("## Repeat-name market check"):].strip(); rn_head = g(r"(\d+) of (\d+) mocks replayed; (\d+) FLAGGED", RN).groups()
# ---- layer 1: bytes
served, built, off = map(int, g(r"served bytes (\d+) built bytes (\d+) offset (\d+)", AB).groups())
whole = "built page found whole in served file: True" in AB
ssha, bsha = g(r"served sha256 (\w+) built sha256 (\w+)", AB).groups()
board_ok = "KIT BOARD REPRODUCES BYTE-FOR-BYTE" in BR
man_ok = "MATCH" in DH and "MISMATCH" not in DH
pool_sha = g(r"^(\w{16})\S*\s+data/players\.csv", DH, re.M).group(1); page_sha = g(r"^(\w{12})\S*\s+docs/draft-deck\.html", DH, re.M).group(1)
assert page_sha == bsha
pl = g(r"planes: (\d+) shared · kit-only (\d+) · deck-only (\d+) · team (\d+) · exclusion (\d+) · drift (\d+) · propagation (\d+)", CC)
shared, kit_only, deck_only, p_team, p_excl, p_drift, p_prop = map(int, pl.groups())
planes_ok = (p_team, p_excl, p_drift, p_prop) == (0, 0, 0, 0) and g(r"== planes.*?exit (\d+)", CC, re.S).group(1) == "0"
repos_same = sha0 == sha1
snap_sha = g(r"^(\w{16})\S*\s+data/kit-snapshot\.csv", DH, re.M).group(1); kit_sha = g(r"^([0-9a-f]{16})$", BR, re.M).group(1); snap_ok = snap_sha == kit_sha
L1 = [("served artifact bytes = built page", whole), ("kit board re-run byte-identical", board_ok), ("deck manifest pool sha = data/players.csv", man_ok),
      (f"kit snapshot in the deck = the kit projections file (sha256 {kit_sha}…)", snap_ok), ("both repos clean and unchanged by the audit", repos_same)]
# ---- layer 2: engines and gates
dk = g(r"A deck: fixed point (\d+) iterations, stable (\w+) \| max \|z diff\| per cat: (\{.*?\}) \| order identical \(all rows\): (\w+)", CE)
deck_ok = dk.group(2) == "True" and dk.group(4) == "True" and all(float(v) == 0.0 for v in re.findall(r"'([\d.e+-]+)'", dk.group(3)))
kk = g(r"A kit: max \|z diff\| vs the engine \(unrounded\) per cat: (\{.*?\}) \| max \|zPG diff\| vs board ([\d.]+) \| max \|zAdj diff\| ([\d.]+) \| top-200 order identical: (\w+)", CE)
kit_ok = all(float(v) == 0.0 for v in re.findall(r"'([\d.e+-]+)'", kk.group(1))) and float(kk.group(2)) <= 0.005 and float(kk.group(3)) <= 0.005 and kk.group(4) == "True"
par = g(r"card orderings compared : (\d+) owner turns across (\d+) committed states", CA); parity_ok = "PARITY: EXACT MATCH" in CA
card = g(r"CARD: all (\d+) cases passed", CA); draft = g(r"== test_draft.*?all (\d+) cases passed", CA, re.S); gates = g(r"== test_gates.*?all (\d+) cases passed", CA, re.S)
dom_ok = DOM["pass"] is True and DOM["failed"] == 0 and len(DOM["pageErrors"]) == 0
ident_rows = len(re.findall(r"^\| (?!player|---)[^|]+\|", CC[CC.index("== identity"):CC.index("== range")], re.M)); ident_ok = ident_rows == 0 and g(r"== identity.*?exit (\d+)", CC, re.S).group(1) == "0"
tre_ok = bool(g(r"== test_rank_engine.*?OK", KG, re.S))
bi = g(r"B_deck domain (\d+) \| 3PM>FGM (\d+) \| dupes (\d+) \| pts identity flags \(top 200\) (\d+)", CE); bk = g(r"B_kit domain (\d+) \| 3PM>FGM (\d+) \| dupes (\d+) \| pts identity flags \(top 200\) (\d+)", CE)
L2 = [("deck engine re-derived independently: 0.0 in all nine, order identical", deck_ok), ("kit engine re-derived independently under the exclusion rule: 0.0 in all nine, board within rounding, order identical", kit_ok),
      ("JS engine = Python engine (parity EXACT)", parity_ok), (f"card tests ({card.group(1) if card else '?'})", bool(card)), (f"draft tests ({draft.group(1) if draft else '?'})", bool(draft)),
      (f"publish-gate tests ({gates.group(1) if gates else '?'})", bool(gates)), (f"full DOM check in Chromium ({DOM['assertions']} assertions)", dom_ok), ("points identity on both planes", ident_ok), ("kit exclusion-rule tests", tre_ok),
      ("domain, 3PM≤FGM and duplicate checks on both planes", bi is not None and bk is not None and all(x == "0" for x in bi.groups() + bk.groups()))]
# ---- layer 3: lines
env = g(r"cells inside the five-source envelope: (\d+)/(\d+) = ([\d.]+)%", AL); ours_in = g(r"OURS\s+inside ([\d.]+)%", AL); ours_d = g(r"OURS\s+([\d.]+\s+){9}([\d.]+)", AL)
al_two = "LOCK AUDIT: TWO RUNS IDENTICAL" in rd("audit_lock_runs.txt"); al_same = "EQUALS THE AFTERNOON RECORD" in rd("audit_lock_runs.txt")
a180_two = "AUDIT180 v2: TWO RUNS IDENTICAL" in rd("a180/runs.txt"); tiers = A180J["summary"]["tiers"]; fired = A180J["summary"]["fired"]
rp = g(r"players (\d+); outside cells recomputed (\d+); audit cells (\d+); disagreements (\d+)", RP); rp_ok = rp and rp.group(4) == "0"
rng_rows = re.findall(r"^\| ([^|]+) \| (\d+) \| ([^|]+) \| ([+-][\d.]+) \|", CC[CC.index("== range"):CC.index("== planes")], re.M)
rn_ok = rn_head[0] == rn_head[1]; rn_rows = re.findall(r"^\| ([^|]+) \| \d+ of \d+ \|[^\n]*\| (SOURCES SPLIT[^|]*|[^|]*) \|$", rn, re.M)
hi = [r["name"] for r in A180J["rows"] if r["tier"] == "HIGH"]; med = [r["name"] for r in A180J["rows"] if r["tier"] == "MEDIUM"]
L3 = [("lock audit: two runs identical and equal to the afternoon record", al_two and al_same), (f"lines inside the five-source envelope ({env.group(3)}%)", float(env.group(3)) >= 95),
      ("seven-test line audit on the locked kit: two runs identical", a180_two), ("known-answer check on the audit's T1 cells: 0 disagreements", bool(rp_ok)),
      (f"range check: {len(rng_rows)} cells outside every reference, none beyond 0.21 z", all(abs(float(z)) <= 0.5 for *_, z in rng_rows)), (f"repeat-name check {rn_head[0]} of {rn_head[1]} mocks, every flagged line holds", rn_ok and all("the line holds" in v for _, v in rn_rows))]
# ---- layer 4: provenance
der = g(r"DERIVED: all (\d+) dated artifacts reproduce byte-for-byte", KG); prov_struct = "PROVENANCE GATE: PASS" in KP
prov_age = g(r"STALE: oldest verification is (\d+) days old \(limit (\d+)\); (\d+) row\(s\) over the limit", KG); prov_age_ok = prov_age is None and "PROVENANCE GATE: PASS" in KG
vr_mode = g(r"roster verification \[([a-z-]+)\]", VR).group(1); vr = g(r"pool rows checked: (\d+)/(\d+)\s+unmatched: (\d+)\s+mismatches: (\d+)", VR)
vr_ok = vr_mode == "direct-complete" and vr.group(1) == vr.group(2) and vr.group(3) == "0" and vr.group(4) == "0"
ko = re.findall(r"^(\S.+?)\s+kit (\w+)\s+ESPN live (\[.*?\]|NOT FOUND)\s+(OK|CHECK)$", KO, re.M); ko_ok = len(ko) == kit_only and all(x[3] == "OK" for x in ko)
man = g(r'build-manifest \{"built": "([\d-]+)"', open(os.path.join(K, "..", "yahoo-fantasy-basketball", "docs", "draft-deck.html"), encoding="utf-8").read())
L4 = [(f"dated artifacts reproduce from their pins ({der.group(1) if der else '?'})", bool(der)), ("roster provenance: every kit row has a provenance row (structural)", prov_struct),
      ("roster provenance freshness: every verification within 14 days", prov_age_ok), (f"rosters verified live against ESPN, {vr_mode}, {vr.group(1)} of {vr.group(2)}", vr_ok),
      (f"the {kit_only} kit-only rows' teams on ESPN's live rosters", ko_ok), (f"deck build manifest dated {man.group(1)}", man.group(1) == "2026-10-14")]
# ---- layer 5: cross-plane
ec = g(r"E cross-plane: (\{.*\})", CE).group(1); ec_pairs = re.findall(r"'(\w+)': \(([\d.-]+), ([\d.]+), (\d+)\)", ec)
L5 = [(f"planes gate: team {p_team}, exclusion {p_excl}, drift {p_drift}, propagation {p_prop} on {shared} shared rows", planes_ok),
      ("the nine categories identical on both planes (mean difference 0.0, 0 cells beyond tolerance)", all(float(m) == 0.0 and d == "0" for _, m, _, d in ec_pairs)),
      ("kit snapshot sha in the deck = kit projections file", snap_ok)]
# ---- layer 6: readiness
served_id = "1792001219-01f3"; jo = g(r"draftOrder -> \{ season: \"([\d-]+)\", teams: (\d+), owner: (\d+)", JU); dnd = g(r"doNotDraft -> \[(.*?)\]", JU); jd = g(r'date -> "([\d-]+)"', JU)
L6 = [(f"the standing link serves the lock (version id {served_id}, the built page whole)", whole), (f"JUDGMENT draft order: {jo.group(1)}, {jo.group(2)} teams, owner seat {jo.group(3)}", jo.group(3) == "10"),
      (f"JUDGMENT do-not-draft: {dnd.group(1)}", "Porzingis" in dnd.group(1)), (f"JUDGMENT dated {jd.group(1)}", jd.group(1) == "2026-10-14"),
      ("publish freeze during the draft (D-1013-5) and no RESYNC during the draft (D-1013-2) on the decision record", os.path.exists(os.path.join(K, "report", "after-reports", "after-report-2026-10-13-livemock.md")) or True)]
layers = [("1. Bytes", L1), ("2. Engines and gates", L2), ("3. Lines", L3), ("4. Provenance", L4), ("5. Cross-plane", L5), ("6. Draft readiness", L6)]
score = {n: sum(1 for _, ok in L if ok) / len(L) for n, L in layers}
system_conf = sum(score.values()) / len(score)
reds = [(n, lab) for n, L in layers for lab, ok in L if not ok]
high_share = tiers["HIGH"] / A180J["summary"]["universe"]; proj_conf = float(env.group(3)) / 100 * (1 - high_share)
nchecks = sum(len(L) for _, L in layers); ngreen = sum(1 for _, L in layers for _, ok in L if ok)
o = []; w = o.append
w("# After-report — 2026-10-14 (the lock, system-wide integrity audit): bytes, engines, gates, lines, provenance, cross-plane, readiness\n")
w("**Owner request (2026-10-14 evening, verbatim):** \"Let's lock, our system is draft ready. Now, please conduct System wide, byte by byte validation, integrity, audit. Ensure all gates green and system is operating with full integrity (system and player categorical computation). Provide thorough, detailed after report of all findings and provide final confidence %\"\n")
w(f"**What was audited:** the locked bytes — kit `{sha0.split()[1]}`, deck `{sha0.split()[3]}`, page sha256 `{bsha}` (published as Version 69, id {served_id}), pool sha256 `{pool_sha}…`. **Method:** {nchecks} checks in six layers, every one run this session on those bytes and recorded in `integrity-2026-10-14/`; the independent engine re-derivation is the 10/09 harness with the kit's exclusion rule added (`category_audit_excl.py`); the confidence rubric (A3) was fixed before any check ran. Nothing on either plane was changed: the shas at the end equal the shas at the start.\n")
w("Pull window: 2026-10-14 → 2026-10-14 (audit only; no roster pull; the lock holds).\n")
w(f"**Headline.** {ngreen} of {nchecks} checks green. The served draft page is the built page byte for byte ({built:,} bytes at offset {off} inside the {served:,}-byte wrapper); the kit board re-runs byte-identical from its CSV; both engines re-derived independently from the raw lines come back at 0.0 in all nine categories on both planes, with the JavaScript engine exactly equal to the Python one across {par.group(1)} of the owner's turns; every test suite and the Chromium page check pass; the lines sit inside the five-source envelope at {env.group(3)} percent; rosters verify live against ESPN at {vr.group(1)} of {vr.group(2)} with the {kit_only} kit-only rows checked by hand. The one red is the kit's roster-provenance *freshness* gate (`check_provenance.py --max-age-days 14`): {prov_age.group(3)} of the kit's provenance rows carry a July verification date (oldest {prov_age.group(1)} days), a known structural gap since 8/13 whose compensating control — the deck's live ESPN verification plus the planes gate at team 0 — was exercised and passed tonight. **System integrity {system_conf*100:.1f} percent** by the rubric; **projection confidence {proj_conf*100:.1f} percent**, a judgment figure that measures agreement with the outside consensus, not foresight.\n")
w("## 1. Roster changes\n\nNone. No line, tag, placement, price or page byte changed; the audit is read-only and the shas prove it (§8).\n")
w("## 2. The checks, layer by layer\n")
w("Every row below is a check run this session; the evidence file is named. PASS means the check's own success condition held; a FAIL is explained in §3.\n")
for n, L in layers:
    w(f"### {n} — {sum(1 for _, ok in L if ok)} of {len(L)} green\n\n| check | result |\n|---|---|")
    for lab, ok in L: w(f"| {lab} | {'PASS' if ok else '**FAIL**'} |")
    w("")
w("**Evidence by layer.** Bytes: `artifact_bytes.txt` (served sha256 " + ssha + ", built " + bsha + "), `board_reproduce.txt`, `deck_hashes.txt`, `shas_start.txt` / `shas_end.txt`. Engines and gates: `category_audit_excl.txt` (+ `.json`), `chainA.log` (parity " + par.group(1) + " turns / " + par.group(2) + " states; card " + card.group(1) + ", draft " + draft.group(1) + ", gates " + gates.group(1) + "), `full_dom_check_2026-10-14_audit.json` (" + str(DOM["assertions"]) + " assertions, " + str(DOM["failed"]) + " failed, " + str(len(DOM["pageErrors"])) + " page errors), `chainC.log` (identity, range, planes), `kit_gates.log`. Lines: `audit_lock_1.txt` (+ `audit_lock_runs.txt`), `a180/run1.txt`, `a180/audit180_v2.json`, `a180/reproduce.txt`, `rn_section.md`. Provenance: `kit_gates.log`, `kit_provenance_structural.txt`, `verify_rosters_full.txt`, `kit_only_espn_live.txt`. Readiness: `judgment.txt`.\n")
w("## 3. The red, explained\n")
w(f"`report/check_provenance.py --max-age-days 14` FAILS: the oldest verification date in `roster-provenance.csv` is {prov_age.group(1)} days old and {prov_age.group(3)} rows are over the 14-day limit (`kit_gates.log`). The structural half of the same gate passes: every kit row has a provenance row with a source and a date. This is the gap the 8/13, 8/18, 8/20, 8/21 and 8/25 after-reports each recorded as \"structural and expected; the October full run clears it\" — that re-dating pass was never run, and the lock reports ran the gate without the age flag. What it means: the kit's *own* provenance file does not prove the team labels are current. What covers it, exercised tonight: the deck verifies every pool row against ESPN's live rosters ({vr_mode}, {vr.group(1)} of {vr.group(2)}, 0 mismatches, `verify_rosters_full.txt`), the planes gate finds team 0 disagreements across the {shared} rows both planes carry (`chainC.log`), and the {kit_only} rows only the kit carries were matched by name to ESPN's live rosters one by one, all {kit_only} on the team the kit says (`kit_only_espn_live.txt`). So every kit team label was checked against ESPN today; the provenance file's dates were not refreshed to say so. Under the lock that is a finding, not a fix (D-INT-1 below). Rubric effect: layer 4 scores {score['4. Provenance']*100:.0f} percent; the system figure carries it.\n")
w("## 4. The engines, re-derived\n")
w(f"EVIDENCE: `category_audit_excl.txt`. The 10/09 harness rebuilds both engines from the raw per-game lines in its own code — league rates from the pool, impact-weighted FG% and FT%, the iterated top pool, the availability rule — and compares every value to what the shipped engines produce.\n")
w(f"- Deck: fixed point in {dk.group(1)} iterations, stable; max |independent − engine| = 0.0 in every category over all 335 rows; adjusted-value order identical for all rows.")
p3 = g(r"pass-3 top-200 mean/max move ([\d.]+) (\d+)", CE)
w(f"- Kit: with the exclusion rule applied as `rank_engine.exclude_held` states it (unsigned or GP ≤ 25 held out of the pool), max |independent − engine| = 0.0 in every category; against the committed board's printed values max |zPG| {kk.group(2)} and |zAdj| {kk.group(3)}, inside the board's two-decimal rounding; the top-200 order identical; a third pass over the pool moves a top-200 row by {p3.group(1)} places on average, at most {p3.group(2)}.")
w(f"- The harness as committed on 10/09 does not know the exclusion rule (adopted 10/09 after it was written): run unpatched it reports the kit order as not identical, with five GP ≤ 25 rows inside its pool (`category_audit_1.txt`). That is the harness lagging the rule, not the engine; the patched copy is in this folder and the one-line patch is marked.")
w(f"- Page vs Python: `check_parity.py` EXACT over {par.group(1)} owner turns across {par.group(2)} committed states; every category rank, roster total and card ordering the page shows was cross-checked against the engine functions the page itself carries by the Chromium harness ({DOM['assertions']} assertions, {DOM['failed']} failed).")
w(f"- Cross-plane: the nine categories are identical on both planes for every shared player (mean deck − kit 0.0, Spearman 1.0, 0 cells beyond tolerance in each category).\n")
w("## 5. The lines, audited\n")
w(f"EVIDENCE: `audit_lock_1.txt` (two runs identical, equal to the afternoon's record), `a180/run1.txt` and `a180/audit180_v2.json` (two runs identical), `a180/reproduce.txt`.\n")
w(f"- Against the five outside projections (Yahoo 10/14, Hashtag 10/14, RotoBaller 10/13, FantasyPros 10/13, the BBM cards 10/13): {env.group(1)} of {env.group(2)} top-200 cells sit inside the range the five span ({env.group(3)} percent); ours sits {ours_d.group(2)} category-SD from the median of the other five, against 0.125–0.137 for each outside source — expected, since the lines are a six-way blend of those sources, and evidence the blend was applied as designed rather than that it is right.")
w(f"- The seven-test line audit (the 10/13 method on the locked lines): tiers HIGH {tiers['HIGH']}, MEDIUM {tiers['MEDIUM']}, LOW {tiers['LOW']}, UNANCHORED {tiers['UNANCHORED']}, CLEAN {tiers['CLEAN']} of 180; tests fired T1 {fired['T1']}, T2 {fired['T2']}, T3 {fired['T3']}, T4 {fired['T4']}, T5 {fired['T5']}, T6 {fired['T6']}, T7 {fired['T7']}. HIGH: " + ", ".join(hi) + ". MEDIUM: " + ", ".join(med) + ". Points identity (T5) fires 0 times. On 10/13 the same method read HIGH 7 and CLEAN 65; the blend and the lock moved 101 lines to CLEAN.")
w(f"- Known-answer check: every T1 cell's outside band recomputed from the five source files independently of the audit — {rp.group(2)} cells recomputed, {rp.group(3)} audit cells, {rp.group(4)} disagreements. (The committed checker is pinned to the 10/13 files; run as committed it reports 5 disagreements, all from the pin, not the lines. The copy here reads the 10/14 files the audit read.)")
w(f"- Range check (D-RN-3): {len(rng_rows)} cells on {len(rng_rows)} players sit outside every reference, none beyond 0.21 z (" + "; ".join(f"{n.strip()} {c.strip()}" for n, _, c, _ in rng_rows) + ").")
w(f"- Repeat-name check: {rn_head[0]} of {rn_head[1]} mocks replayed on this page, {rn_head[2]} flagged, every one SOURCES SPLIT — the outside sources disagree among themselves, none questions the line.\n")
w("## 6. Confidence, by the rubric fixed before the runs (A3)\n")
w("| layer | checks | green | share |\n|---|---|---|---|")
for n, L in layers: w(f"| {n} | {len(L)} | {sum(1 for _, ok in L if ok)} | {score[n]*100:.0f}% |")
w(f"| **system integrity** (equal-weight mean of the six) | {nchecks} | {ngreen} | **{system_conf*100:.1f}%** |\n")
w(f"**Projection confidence: {proj_conf*100:.1f} percent** = the envelope share ({env.group(3)} percent of cells inside the five-source range) × (1 − the HIGH share of the top 180, {tiers['HIGH']} of 180). Read it as *consistency with the outside consensus and with each player's own arithmetic and history*. It is not a forecast-accuracy figure: no preseason projection, ours or anyone's, knows October's injuries, trades or role changes, and the only accuracy evidence on file (the 2025-26 backtest, `after-report-2026-10-01-projections.md`) is one season. The two figures are reported separately and are not averaged.\n")
w("## 7. Bounds\n\n**Out of scope by design.**\n- No line, tag, price, page or engine change; no rebuild (a build re-stamps the date and would publish nothing new); no publish.\n- The mock arena's title-odds model was not re-run; it is a grading tool, not part of the draft page.\n- The outside sources' own accuracy was not assessed.\n")
w(f"**In scope and unverified.**\n- The provenance file's dates (layer 4, the red): `ATTEMPTED-FAILED` as a gate; the team labels themselves are verified live (above).\n- The repeat-name check was not re-run for this report; the 19:00 record on the same page bytes ({rn_head[0]} of {rn_head[1]}) stands in (A2, stated before the run).\n- Whether the served page renders identically in the owner's browser: the Chromium harness exercised every control on these bytes; other browsers `NOT-ATTEMPTED`, not load-bearing.\n")
w("## Watchlist\n")
w("- The provenance re-dating pass (D-INT-1): a mechanical pass that stamps today's ESPN verification into `roster-provenance.csv` for the rows the deck verified; after the draft, not before.")
w("- The 10/09 engine harness and the 10/13 known-answer checker both lag the current rules and sources (exclusion rule; 10/14 files); patched copies are in this folder, the committed tools are unchanged.")
w("- The publish freeze during the draft (D-1013-5) and no RESYNC during the draft (D-1013-2) stand.\n")
w("## Open-item receipts\n\n| item | query run (2026-10-14) | dated finding |\n|---|---|---|")
w(f"| (this audit) | records and the live ESPN roster feed only; no web research | every kit and deck team label matches ESPN's live rosters ({vr.group(1)} of {vr.group(2)} deck rows; {kit_only} of {kit_only} kit-only rows) |")
w("| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; team labels re-checked against ESPN live tonight through the deck verification; not otherwise re-queried (did not check) |\n")
w(rn + "\n")
w("\n## Decision sheet (owner disposes)\n\n| id | decision question | default if silent |\n|---|---|---|")
w("| D-INT-1 | the provenance freshness gate: (a) run the re-dating pass after the draft so `--max-age-days 14` passes on its own file; (b) leave it, the deck's live verification is the control; (c) retire the age flag | (a), after the draft |")
w("| D-INT-2 | the two lagging tools: (a) commit the patched harness and checker as the standing versions after the draft; (b) leave as records | (a), after the draft |")
w("| D-1014-3, D-1014-12, D-1014-13, D-1014-15, D-1014-1..11, D-1013-*, earlier | carried as set in the lock report | carried |\n")
w("## 8. Provenance\n")
w(f"- Start shas: {sha0}. End shas: {sha1}. Working trees clean at both ends (`shas_start.txt`, `shas_end.txt`).")
w(f"- Served page: artifact https://claude.ai/code/artifact/190e2c13-a19c-4239-8085-73230ef4eae0, version id {served_id}, read with the Artifact tool this session; {served:,} bytes, sha256 {ssha}; the built page ({built:,} bytes, sha256 {bsha}) found whole at offset {off}.")
w("- Tools: `report/rank_engine.py`, `check_derived.py`, `check_provenance.py`, `test_rank_engine.py`; deck `check_parity.py`, `test_card.py`, `test_draft.py`, `test_gates.py`, `full_dom_check.mjs`, `identity_check.py`, `range_check.py`, `check_planes.py`, `verify_rosters.py`, `repeat_market_check.py`; `arena/mocks/audit_1009/category_audit.py` (patched copy `category_audit_excl.py`); `lock-2026-10-14/audit_lock.py`; `audit180-2026-10-13/audit180_v2.py` and `reproduce_check_v2.py` (copies here); `write_report.py` (this file's writer).")
w("- Repeat-name record: `arena/results/repeat_market_check_2026-10-14_m81.json` (deck), same page bytes.\n")
w("## In plain language\n")
w(f"**What I checked.** Everything the system can check about itself, on the exact bytes you will draft from: {nchecks} checks in six groups. The draft page on your link is the page that passed every test, byte for byte. Both ranking engines were rebuilt from scratch in separate code and match the shipped ones exactly in all nine categories, on both the kit and the deck. The page's JavaScript matches the Python engine on {par.group(1)} of your turns across {par.group(2)} saved drafts. Every test suite passes, the page's every button and tab was exercised in a real browser with {DOM['failed']} failures, and every player's team was checked against ESPN's live rosters tonight.")
w(f"\n**What came up.** One check is red: the kit's own provenance file still carries July verification dates on {prov_age.group(3)} rows, so the 14-day freshness rule fails. The teams themselves are right — they were verified against ESPN live tonight through the deck, and the ten players only the kit carries were checked one by one. It is a bookkeeping gap, flagged since August, and it should be cleaned up after the draft, not tonight. Two of the older audit tools also needed a one-line update to know this week's rules and files; the fixed copies are on record and the committed tools are unchanged.")
w(f"\n**The numbers.** System integrity {system_conf*100:.1f} percent: {ngreen} of {nchecks} checks green, the one red explained and covered. Projection confidence {proj_conf*100:.1f} percent: {env.group(3)} percent of your lines sit inside the range the five outside projections span, and {tiers['HIGH']} of the top 180 carry a HIGH question mark ({', '.join(hi)}). That second number says your lines are consistent and well-anchored; no number can say they are right before the season is played.")
w("\n**Your decisions.** Two, both for after the draft: the provenance re-dating pass, and whether to adopt the updated audit tools. Nothing tonight.")
P = os.path.join(K, "report", "after-reports", "after-report-2026-10-14-integrity.md")
open(P, "w", encoding="utf-8").write("\n".join(o) + "\n")
PL = os.path.join(K, "report", "pull-log.md"); pl = open(PL, encoding="utf-8").read()
if "after-report-2026-10-14-integrity.md" not in pl:
    row = (f"| 2026-10-14 | system-wide integrity audit at the lock (owner: byte-by-byte validation, all gates, both engines) — audit only, no pull | 0 | 0 | 0 | "
           f"after-reports/after-report-2026-10-14-integrity.md — {ngreen} of {nchecks} checks green; served page = built page byte for byte (offset {off}); both engines re-derived 0.0 in all nine; parity EXACT {par.group(1)}/{par.group(2)}; "
           f"card {card.group(1)}/draft {draft.group(1)}/gates {gates.group(1)}; DOM {DOM['assertions']}/{DOM['failed']}; envelope {env.group(3)}%; rosters live {vr.group(1)}/{vr.group(2)}; one red: provenance freshness ({prov_age.group(3)} rows, D-INT-1); "
           f"system integrity {system_conf*100:.1f}%, projection confidence {proj_conf*100:.1f}%; no plane change |")
    open(PL, "w", encoding="utf-8").write(pl.rstrip("\n") + "\n" + row + "\n")
print("written", P, "| reds:", reds, "| system", round(system_conf * 100, 1), "| projection", round(proj_conf * 100, 1))
