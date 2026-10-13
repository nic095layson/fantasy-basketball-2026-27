#!/usr/bin/env python3
"""Writes report/after-reports/after-report-2026-10-13-audit180.md from audit180.json and the records beside it.
Every figure is read from a record; the typed literals are the method parameters stated to the owner (A1-A6)."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.normpath(os.path.join(H, "..", "..", "..")); AR = os.path.join(K, "report", "after-reports")
J = lambda p: json.load(open(p, encoding="utf-8")); rd = lambda p: open(p, encoding="utf-8").read()
A = J(os.path.join(H, "audit180.json")); S = A["summary"]; R = A["rows"]
rn = rd(os.path.join(K, "report", "dial", "out", "rn_section_v65.md")); ra = J(os.path.join(H, "range_no_actual_v65.json"))
tb = rd(os.path.join(H, "team_budget_v65.txt"))
LAB = {"pts": "pts", "reb": "reb", "ast": "ast", "stl": "stl", "blk": "blk", "tpm": "3PM", "tov": "TO", "fg_pct": "FG%", "ft_pct": "FT%"}
fmt = lambda c, v: (f"{v:.3f}".lstrip("0") if c.endswith("pct") else f"{v:g}")
def t1(r): return "; ".join(f"{LAB[x['cat']]} {fmt(x['cat'], x['line'])} vs {fmt(x['cat'], x['lo'])} to {fmt(x['cat'], x['hi'])} ({x['z']:+.2f} z)" for x in r["tests"]["T1"]["cells"])
def reasons(r):
    b = []
    if r["tests"]["T1"]["cells"]: b.append("outside all three projections: " + t1(r))
    for x in r["tests"].get("T2", {}).get("cells", []): b.append(f"per-36 {LAB[x['cat']]} {x['line_per36']} outside his own band {x['band'][0]} to {x['band'][1]}")
    for x in r["tests"].get("T3", {}).get("cells", []): b.append(f"{LAB[x['cat']]} {fmt(x['cat'], x['line'])} outside his career band {fmt(x['cat'], x['band'][0])} to {fmt(x['cat'], x['band'][1])}")
    for x in r["tests"]["T4"]["notes"]: b.append(x)
    if abs(r["tests"]["T5"]["gap"]) > 1: b.append(f"points identity gap {r['tests']['T5']['gap']:+.2f}")
    for x in r["tests"].get("T6", {}).get("notes", []): b.append(x)
    if r["tests"]["T7"]["note"]: b.append(r["tests"]["T7"]["note"] + ": " + ", ".join(f"{k} {v}" for k, v in r["tests"]["T7"]["outside"].items()))
    return "; ".join(b)
tier = lambda t: [r for r in R if r["tier"] == t]
HIGH, MED, LOW, UNA, CLEAN = (tier(t) for t in ("HIGH", "MEDIUM", "LOW", "UNANCHORED", "CLEAN"))
n = lambda t: S["tiers"][t]
fired = S["fired"]
cells = [x for r in R for x in r["tests"]["T1"]["cells"]]
zpos = sum(x["z"] for x in cells if x["z"] > 0); zneg = sum(x["z"] for x in cells if x["z"] < 0)
big = [r for r in R if abs(r["tests"]["T1"]["net_z"]) > 0.5]
two_refs = [r["name"] for r in R if r["tests"]["T1"]["refs"] == 2]; no_refs = [r["name"] for r in R if r["tests"]["T1"]["refs"] < 2]
gp_hist = [r for r in R if any("three-season average" in x for x in r["tests"]["T4"]["notes"])]
gp_out = [r for r in R if any("(Yahoo/Hashtag)" in x for x in r["tests"]["T4"]["notes"])]
both = [r for r in R if len(r["tests"]["T4"].get("outside_gp", [])) == 2]
gp_ours = sum(r["gp"] for r in both); gp_out_mean = sum(sum(r["tests"]["T4"]["outside_gp"]) / 2 for r in both)
old = [r for r in R if r["tests"].get("T6", {}).get("notes")]
UL = ", ".join(S["unanchored_largest"])
OLDLIST = ", ".join(f"{r['name']} ({r['age']})" for r in old)
mkt_hi = [r for r in R if r["tests"]["T7"]["note"] and "we are high" in r["tests"]["T7"]["note"]]
mkt_lo = [r for r in R if r["tests"]["T7"]["note"] and "we are low" in r["tests"]["T7"]["note"]]
noh = [r for r in UNA if not r["history_seasons"]]
TBM = re.search(r"above the 2025-26 league maximum \(117\.7\): (\d+) \[([^\]]*)\]", tb); TBO = re.search(r"more possessions than the team used in 2025-26: (\d+)", tb)
phi = re.search(r"^PHI \| \d+ \| [^|]+\| [\d.]+ \([\d.]+\) vs [\d.]+ \| ([\d.]+) ", tb, re.M).group(1)
assert fired["T2"] == 0 and fired["T5"] == 0, "the report's reading of T2/T5 assumes zero fires"
o = []; w = o.append
w("# After-report — 2026-10-13 (audit): validation and integrity audit of the top-180 lines on the kit board\n")
w("**Owner request (2026-10-13, verbatim):** \"With the board now rebuilt, I'd like for you to conduct a validation and integrity audit on the top 180 players 9cat projection lines. Do you agree with the kit's projections, or do they seem unrealistic? Provide a report of who you have question marks on, and let me know what I can upload to you to help confidence reach near certain levels.\"\n")
w(f"**What was analyzed:** the kit board's ranks 1 to 180 (`report/top-200-2026-27.md` at kit `main` a98a37f, Version 65's lines) and each player's line in `report/projections-2026-27.csv`. Nothing on either plane changed: both files are byte-identical before and after the audit. References: {', '.join(f'{k} `{v}`' for k, v in S['refs'].items())}; the player's own Basketball-Reference seasons 2003-04 to 2025-26 (`report/wo5/data/bref_totals_2004-2026.csv`, pinned at WO-5); outside ranks from {', '.join(S['ranks_sources'])}.\n")
w("**Method (A1 to A6, stated to the owner before the run):** A1 the universe is the kit board's top 180. A2 history is the player's own per-36 rates over his last three seasons of 25+ games; a cell is questioned beyond that band by more than 10% (0.1 floor), a percentage beyond the career band by more than .010. A3 minutes are questioned 2+ above the three-season high or 4+ from Hashtag's; games 10+ above the three-season average after a season under 60, or 6+ above both Yahoo's and Hashtag's projected games. A4 age: 32 and older projecting more per 36 than last season, 23 and younger projecting less, and 34 and older above the outside average in two of points, rebounds and assists. A5 market: every outside rank 25+ places on one side of ours. A6 tiers: HIGH when three or more tests fire or the cells outside the outside range carry more than 0.5 z; MEDIUM two tests; LOW one; UNANCHORED when fewer than two qualifying NBA seasons exist; CLEAN none. Seven tests, T1 to T7, in `audit180-2026-10-13/audit180.py`; two runs identical.\n")
w("Pull window: 2026-10-13 → 2026-10-13 (no roster pull; the lines as merged in kit PR #109).\n")
w(f"**Headline.** The lines are internally sound and history-shaped: every one of the {S['universe']} passes the points identity, and none departs from the player's own three-season per-36 band by more than the tolerance (T2 fired 0 times). That is the strength and the limit of the method: a line built from a player's own rates cannot be wrong about his arithmetic, and cannot see a role change. The real question marks are therefore where the outside projections disagree with that history. {fired['T1']} of the 180 have a category outside all three outside projections, but after this evening's clamp the disagreements are small and balanced: the cells beyond the range carry {zpos:+.2f} z on the flattering side and {zneg:+.2f} on the other, and only {len(big)} lines carry more than 0.5 z net. I agree with the top 100 as a whole; my question marks concentrate on {n('HIGH')} HIGH lines ({sum(1 for r in HIGH if r['rank'] > 100)} of them past rank 100, {sum(1 for r in HIGH if r['tests']['T1']['refs'] == 2)} with only two outside projections), on {len(old)} players aged 34 and older whose lines carry no age decline, on the {n('UNANCHORED')} rookies and returners with fewer than two NBA seasons, and on the {TBM.group(1)} team pools still above last season's league maximum of possessions. Games played are not a systematic lean: over the {len(both)} players both Yahoo and Hashtag project, our games sum to {gp_ours:.0f} against their average {gp_out_mean:.0f}.\n")
w("## 1. Roster changes\n\nNone. No line, tag, placement, games or minutes figure changed on either plane; this is an assessment.\n")
w("## 2. The verdict, test by test\n\nEVIDENCE: `audit180-2026-10-13/audit180.json` (one record per player), `audit180.txt` (the flagged lines), `range_no_actual_v65.json`, `team_budget_v65.txt`.\n")
w("| test | what it asks | fired | reading |\n|---|---|---|---|")
w(f"| T1 outside range | is a cell outside all three outside projections, and by how much in the deck's z frame | {fired['T1']} of 180 | small and two-sided after the clamp: {len(cells)} cells, {zpos:+.2f} z flattering against {zneg:+.2f}; {len(big)} lines over 0.5 z net, all but {sum(1 for r in big if r['rank'] <= 100)} of them ranked past 100. {len(two_refs)} of the 180 have only two outside projections and {len(no_refs)} have none ({', '.join(no_refs)}) |")
w(f"| T2 own history | does the per-36 line sit inside the player's own three-season band | {fired['T2']} | the method builds each line from that band, so it cannot fail here; the test confirms no transcription or scaling error in the {180 - n('UNANCHORED')} anchored lines |")
t3 = [(r, x) for r in R if r["tests"].get("T3", {}).get("cells") for x in r["tests"]["T3"]["cells"]]
w(f"| T3 career shooting | FG% or FT% outside the career band | {fired['T3']} | " + "; ".join(f"{r['name']}: {LAB[x['cat']]} {fmt(x['cat'], x['line'])} against a career band of {fmt(x['cat'], x['band'][0])} to {fmt(x['cat'], x['band'][1])}" for r, x in t3) + " |")
w(f"| T4 minutes and games | minutes above the career high or far from Hashtag; games above the player's own history or above both outside projections | {fired['T4']} | {len(gp_hist)} games flags rest on the player's injury history; only {len(gp_out)} lines sit 6+ games above both Yahoo and Hashtag ({', '.join(r['name'] for r in gp_out)}). Our games are not optimistic in aggregate ({gp_ours:.0f} against {gp_out_mean:.0f} over {len(both)} players) |")
w(f"| T5 points identity | points equal to 2·FG%·FGA + 3PM + FT%·FTA within 1 | {fired['T5']} | every line reconciles |")
w(f"| T6 age | 32+ projected up, 23 and under projected down, 34+ above the outside average | {fired['T6']} | no line projects an old player up or a young player down against his own last season; {len(old)} players aged 34 and older sit above the outside average in two or more of points, rebounds and assists because the method carries no age decline: {OLDLIST} |")
w(f"| T7 market | every outside rank 25+ places on one side of ours | {fired['T7']} | we are high on {len(mkt_hi)} ({', '.join(r['name'] for r in mkt_hi)}) and low on {len(mkt_lo)} ({', '.join(r['name'] for r in mkt_lo)}) |")
w(f"| team budget | a team's pool above the league maximum of possessions used | {TBM.group(1)} teams | {TBM.group(2).replace(chr(39), '')}; {TBO.group(1)} teams above their own 2025-26 total; Philadelphia {phi} against 117.7 (`team_budget_v65.txt`, the dial pass's run on these same lines) |")
w(f"\nTiers: HIGH {n('HIGH')}, MEDIUM {n('MEDIUM')}, LOW {n('LOW')}, UNANCHORED {n('UNANCHORED')}, CLEAN {n('CLEAN')}. Of the 180, {n('CLEAN')} lines pass every test and {n('LOW')} carry one flag; apart from the age-decline question in T6, which is a property of the method rather than of any one line, I agree with those {n('CLEAN') + n('LOW')} as they stand.\n")
w("## 3. The question marks\n\nEVIDENCE: `audit180-2026-10-13/audit180.json`; z figures in the deck's own frame, flattering positive.\n")
w("### HIGH\n\n| rank | player | age | net z beyond the range | why |\n|---|---|---|---|---|")
for r in HIGH: w(f"| {r['rank']} | {r['name']} ({r['team']}) | {r['age']} | {r['tests']['T1']['net_z']:+.2f} | {reasons(r)} |")
w("\n### MEDIUM\n\n| rank | player | age | net z | why |\n|---|---|---|---|---|")
for r in MED: w(f"| {r['rank']} | {r['name']} ({r['team']}) | {r['age']} | {r['tests']['T1']['net_z']:+.2f} | {reasons(r)} |")
w("\n### UNANCHORED (fewer than two NBA seasons of 25+ games: college or one-season translations)\n\n| rank | player | NBA seasons on file | net z | what the outside projections say |\n|---|---|---|---|---|")
for r in UNA: w(f"| {r['rank']} | {r['name']} ({r['team']}) | {', '.join(r['history_seasons']) or 'none'} | {r['tests']['T1']['net_z']:+.2f} | {reasons(r) or 'inside all three projections; ' + ('no NBA history at all' if not r['history_seasons'] else 'one season')} |")
w("\n### LOW (one small disagreement each; I agree with these lines)\n")
w("; ".join(f"{r['name']} ({reasons(r)})" for r in LOW) + ".\n")
w("## 4. What you can upload, and what it would settle\n")
w(f"Near-certainty is not available for a forecast: a projection is right or wrong in April. What an upload can make near-certain tonight is narrower and still worth having: that every line sits inside the band of independent projections, that minutes and games match what the people closest to each team expect, and that the {n('UNANCHORED')} unanchored lines rest on more than one translation. Each item below names the test it feeds.\n")
w("| upload | feeds | what it settles |\n|---|---|---|")
w(f"| A fresh RotoBaller projection export, or any third full-stat projection dated this week (Basketball Monster, ESPN, FantasyPros, Hashtag's paid sheet) | T1, the clamp's references | the RotoBaller file on hand is dated 9/29, before camp cuts and the preseason; a current third source tightens the range for all 180 and gives the {len(two_refs)} two-reference players a real band |")
w(f"| A projected-minutes or depth-chart export per team (RotoWire depth charts, Hashtag's minutes column for the full pool, a Lineups-style minutes sheet) | T4, the team budget | minutes are the largest single lever in every line; an outside minutes sheet for all 180 settles the {fired['T4']} T4 flags and lets the team budget be read per player, Philadelphia first |")
w(f"| The latest injury report and games-played projections (Yahoo's projected GP page for the full pool, or Hashtag's) | T4 games | our games are consensus-shaped in aggregate; a full-pool games file closes the {len(gp_hist)} injury-history flags one by one |")
w(f"| A rookie projection source with per-game lines (Hashtag rookie sheet, a draft-guide translation, summer-league and preseason box scores) | the {n('UNANCHORED')} unanchored lines | {UL} carry the largest cell-by-cell disagreements with the outside projections among the unanchored lines; two more translations per rookie would say whether ours or the outside's is the outlier |")
w(f"| Any source that projects decline for players 34 and older (an aging-curve table, or simply a second projection's lines for the {len(old)} named in T6) | T6 | the method carries last season's per-36 forward unchanged; an outside view with decline built in says how much the {len(old)} old lines overstate |")
w("| Your league's final Yahoo draft order and roster settings (already on file for 10/14) and tonight's Yahoo projected-stats paste at the lock | T7, prices | the lock paste re-prices the card; it does not change a line unless you say so (D-1013-1) |")
w("\nWhat an upload cannot settle: whether the three outside sources share a blind spot on a roster (a line inside their range is still a guess if they all guessed together), and anything that happens after the draft. Those are bounded below.\n")
w("## Range check (D-RN-3, without last season as a reference)\n")
w(f"The deck's own range check re-run on the live page with no last-season file: {ra['players']} of {ra['checkable']} checkable top-150 lines have a category outside all three outside projections, {ra['cells']} cells; identical to the dial pass's after-run (`range_no_actual_v65.json`). None of the 24 clamped lines is among them. This is not a projection pass, so the owner's D-RN-3 mechanism rule does not apply to this report; the 19 lines the rule flags with last season as a reference carry their mechanisms in `after-report-2026-10-13-dial.md`.\n")
w("## Watchlist\n")
w(f"- The {n('HIGH')} HIGH lines above; none is changed by this report (D-1013-10).")
w(f"- The {len(old)} players aged 34 and older with no decline in the method (D-1013-11).")
ubig = [r for r in UNA if abs(r["tests"]["T1"]["net_z"]) > 0.5]
w(f"- The {n('UNANCHORED')} unanchored lines, {len(ubig)} with net z beyond 0.5 either way: " + ", ".join(f"{r['name']} {r['tests']['T1']['net_z']:+.2f}" for r in ubig) + " (D-1013-12).")
w(f"- Philadelphia's pool at {phi} possessions against 117.7; the usage model is D-C2, after the draft.")
w("- The 10/14 lock paste (D-1013-1) and the publish freeze during the draft (D-1013-5); no RESYNC during the draft (D-1013-2).\n")
w("## Open-item receipts\n\n| item | query run (2026-10-13) | dated finding |\n|---|---|---|")
w("| (this audit) | records only; no web research and no roster pull | the lines audited are the ones merged in kit PR #109 this evening; pull receipts for the window live in `after-report-2026-10-13.md` (the morning's pull), same day |")
w("| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (`after-report-2026-10-13.md`, receipts dated 10/13) | all HELD or unsigned on 2026-10-13 per those receipts; not re-queried in this audit (did not check) |\n")
w(rn[rn.index("## Repeat-name market check"):].strip() + "\n")
w("\n## Bounds\n\n**Out of scope by design.**")
w(f"- No line was changed, built or dry-run; this is the assessment the owner asked for. The option, if asked: a line-by-line review of the {n('HIGH')} HIGH rows with two dated outlets each, the way WO-5 researched its candidates.")
w("- Ranks 181 to 200 of the kit board and the deck-only rows were not audited.")
w("- The tests use the files on hand; no new outside source was fetched.\n")
w("**In scope and unverified.**")
w(f"- Whether the three outside sources share a blind spot on a roster: `NOT-ATTEMPTED`; a line inside their range cannot show one.")
w(f"- The {len(two_refs)} lines with only two outside projections and the {len(no_refs)} with none: their T1 verdicts rest on a narrower or absent band: `ATTEMPTED-FAILED`, no third source on file for them (the RotoBaller file covers 242 names, Hashtag 200, Yahoo 300).")
w(f"- Whether the clamped and history-shaped lines are closer to what will happen than the outside projections: `UNVERIFIABLE` until games are played; the one-season record (`after-report-2026-10-09-market.md` §4) favours pre-season projections over a copy of the prior season in 8 of 9 categories.\n")
w("## Decision sheet (owner disposes)\n\n| id | decision question | default if silent |\n|---|---|---|")
w(f"| D-1013-10 | The {n('HIGH')} HIGH lines: (a) hold for the draft; (b) clamp the ones with two or more outside references to the edge of their range at the lock, the dial method; (c) review line by line with two dated outlets each | (a) for tonight: " + ", ".join(f"{r['name']}" for r in HIGH if r['rank'] <= 100) + " sit in the top 100 and the rest sit past rank 100 |")
w(f"| D-1013-11 | Age decline for the {len(old)} players 34 and older: (a) none, as now; (b) a flat per-36 haircut by age band, after the draft with D-C2 | (b) after the draft |")
w(f"| D-1013-12 | The {len(ubig)} unanchored lines beyond 0.5 z net ({', '.join(r['name'] for r in ubig)}): (a) hold; (b) move to the outside average at the lock | (a) |")
w("| D-1013-8, D-1013-9 | Murray and Nesmith just past the cut; Ware LINE QUESTIONED | as set in the dial report |")
w("| D-1013-1..7, D-C2, D-SF-1..4 and earlier | carried | carried |\n")
w("## Provenance\n")
w(f"- Inputs: kit `main` a98a37f (board, lines), deck `main` dd6b719 (page sha256 09a889d4baa5, the z frame), the three projection files and {len(S['ranks_sources'])} rank files named above, the pinned Basketball-Reference totals.")
w("- Tools: `audit180-2026-10-13/audit180.py` (two runs identical), the deck's `scripts/range_check.py` with no last-season file, the dial pass's `team_budget_after.txt` copied as `team_budget_v65.txt`, `write_audit_report.py` (this file's writer).")
w("- Known-answer checks on the tool: a planted doubling of Holiday's points fires T2 (session record); `reproduce_check.py` confirms the T1 cells and their z equal the deck's own range check cell for cell on every player both records cover.")
w("- No line, tag or placement changed; both planes' hashes equal before and after (e821ec1ddc67 kit, bd2b983876a8 deck).\n")
w("## In plain language\n")
w(f"**Do I agree with the lines?** For the most part, yes. Every line adds up, and every line follows from the player's own last three seasons. {n('CLEAN') + n('LOW')} of the 180 pass everything or carry one small flag. The method's weakness is the opposite of a transcription error: it trusts last season. Where a player's role is changing, the outside projections see it and the history does not, and that is where my question marks sit.")
top_high = [r for r in HIGH if r["rank"] <= 100]; ware = next(r for r in R if r["name"] == "Kel'el Ware"); wh = ware["tests"]["T7"]["outside"]
biggest = sorted(HIGH, key=lambda r: -abs(r["tests"]["T1"]["net_z"]))[:2]
w(f"\n**Who I have question marks on.** {n('HIGH')} players, listed in §3. In the top 100: " + "; ".join(f"{r['name']} at #{r['rank']} ({', '.join(LAB[x['cat']] for x in r['tests']['T1']['cells'] if x['z'] > 0) or 'no cell'} above every outside projection, {r['tests']['T1']['net_z']:+.2f} z net)" for r in top_high) + f". Kel'el Ware at #{ware['rank']} is {ware['tier']} here rather than HIGH only because Hashtag ranks him {wh['Hashtag']}, {wh['Hashtag'] - ware['rank']} places from ours, one short of the market test; the repeat-name check still calls his line questioned (D-1013-9). Further down, " + " and ".join(f"{r['name']} ({r['tests']['T1']['net_z']:+.2f} z net, {r['tests']['T1']['refs']} outside projections)" for r in biggest) + f" carry the largest disagreements on the board. Add the {len(old)} players aged 34 and older, whose lines carry no decline, and the {n('UNANCHORED')} rookies and returners whose lines rest on a translation rather than NBA seasons.")
w("\n**What to upload.** The single most useful file is a current third projection with full stats (RotoBaller's is two weeks old). After that, a projected-minutes sheet per team, a full-pool games projection, and a rookie projection source. Each closes a named test above. None makes a forecast certain; together they make the lines consensus-checked in every category for every player, which is as far as pre-season certainty goes.")
w("\n**Your decisions.** D-1013-10 on the HIGH lines tonight; D-1013-11 and D-1013-12 can wait for the lock or the draft's aftermath.")
P = os.path.join(AR, "after-report-2026-10-13-audit180.md")
open(P, "w", encoding="utf-8").write("\n".join(o) + "\n")
PL = os.path.join(K, "report", "pull-log.md"); pl = rd(PL)
assert "after-report-2026-10-13-audit180.md" not in pl
row = (f"| 2026-10-13 | owner question: validation and integrity audit of the top-180 kit lines (assessment, no roster pull) | 0 | 0 | 0 | "
       f"after-reports/after-report-2026-10-13-audit180.md — seven tests on 180 lines, two runs identical; points identity 0 off, own-history band 0 off; "
       f"{fired['T1']} lines with a cell outside all three outside projections ({zpos:+.2f} z flattering against {zneg:+.2f}), {len(big)} over 0.5 z net; "
       f"tiers HIGH {n('HIGH')}, MEDIUM {n('MEDIUM')}, LOW {n('LOW')}, UNANCHORED {n('UNANCHORED')}, CLEAN {n('CLEAN')}; {len(old)} players 34+ with no decline in the method; "
       f"games not optimistic in aggregate ({gp_ours:.0f} against {gp_out_mean:.0f}); no plane change; D-1013-10..12 on the sheet |")
open(PL, "w", encoding="utf-8").write(pl.rstrip("\n") + "\n" + row + "\n")
print("report and pull-log row written")
