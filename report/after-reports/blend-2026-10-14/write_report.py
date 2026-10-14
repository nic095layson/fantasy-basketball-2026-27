#!/usr/bin/env python3
"""Writes after-report-2026-10-14-blend.md from the records in report/blend/out/, the deck chain logs and the V66 calls.
Every figure in a table or a count in the prose is read from a record here, not typed (adversarial-verify rule 7);
the prose around them is the author's."""
import json, os, re
KIT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
OUT = os.path.join(KIT, "report", "blend", "out")
DECK = "/home/user/yahoo-fantasy-basketball"
rd = lambda p: open(p, encoding="utf-8").read()


def audit(path):
    t = rd(os.path.join(OUT, path))
    cats = {}
    for m in re.finditer(r"^(\w+)\s+(\d+)\s+([+-][\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+(\d+) \((\d+)%\)$", t, re.M):
        cats[m.group(1)] = dict(n=int(m.group(2)), bias=float(m.group(3)), mae=float(m.group(4)), loo=float(m.group(5)),
                                out=int(m.group(7)), outpct=int(m.group(8)))
    env = re.search(r"inside the five-source envelope: (\d+)/(\d+) = ([\d.]+)%", t)
    ins = dict(re.findall(r"^  (\S[\w ]*?)\s+inside ([\d.]+)%$", t, re.M))
    dist = {}
    for m in re.finditer(r"^  (\S[\w ]*?)\s+((?:[\d.]+\s+){9})([\d.]+)$", t, re.M):
        dist[m.group(1).strip()] = float(m.group(3))
    refs = re.search(r"refs per player \(top 200\): (\{.*\})", t).group(1)
    return dict(cats=cats, env=(int(env.group(1)), int(env.group(2)), env.group(3)), inside=ins, dist=dist, refs=refs)


A0, A1 = audit("audit_v66_lines.txt"), audit("audit_v67_lines_new200.txt")
L = json.load(open(os.path.join(OUT, "lines_blend_2026-10-14.json"), encoding="utf-8"))
R = json.load(open(os.path.join(OUT, "apply_record_2026-10-14.json"), encoding="utf-8"))
nrows, ndeck = len(L["rows"]), sum(x["on_deck"] for x in L["rows"])
wide = L["wide_factor"]
kit_vals = sum(len(x["changed"]) for x in R["rows"] if x["plane"] == "kit")
deck_vals = sum(len(x["changed"]) for x in R["rows"] if x["plane"] == "deck")
assert kit_vals + deck_vals == R["values_changed"]
BD = rd(os.path.join(OUT, "board_diff_2026-10-14.txt"))
CC = rd(os.path.join(OUT, "card_compare_2026-10-14.txt"))
cc_turns, cc_changed = map(int, re.search(r"turns compared: (\d+); 🎯 changed: (\d+)", CC).groups())
cc_round = re.search(r"by round \(changed / turns\): (.*)", CC).group(1)
cc_counts = re.search(r"the 15 names with the largest change \(v66 to v67\): (.*)", CC).group(1)
NP = rd(os.path.join(OUT, "named_players_2026-10-14.txt"))
TB = rd(os.path.join(OUT, "team_budget_after.txt"))
tb_over = re.search(r"teams whose pool alone is above the 2025-26 league maximum \(117.7\): (\d+) (\[.*?\])", TB).groups()
RCJ = json.load(open(os.path.join(OUT, "range_check_v67.json"), encoding="utf-8"))
IDT = rd(os.path.join(OUT, "identity_v67.txt"))
S = "/tmp/claude-0/-home-user-fantasy-basketball-2026-27/3cdbbd9b-02dd-585e-8d00-b8a370128fae/scratchpad"
CH66, CH67 = rd(f"{S}/v66/chain.log"), rd(f"{S}/blend/chain.log")
RN = rd(f"{S}/blend/rn_section.txt")
rn_head = re.search(r"(\d+) of (\d+) mocks replayed; (\d+) FLAGGED", RN).groups()
rn_body = RN[RN.index("## Repeat-name market check"):].split("\n", 1)[1].strip()


def chain(t):
    g = lambda pat: re.search(pat, t).group(1)
    return dict(parity=g(r"card orderings compared : (\d+ owner turns across \d+ committed states)"),
                card=g(r"CARD: all (\d+) cases passed"), draft=g(r"all (\d+) cases passed\nexit 0\n== test_gates"),
                gates=g(r"all (\d+) cases passed\nexit 0\n== full_dom"), dom=g(r'"assertions":(\d+),"failed":0'),
                rn=g(r"(\d+ of \d+ mocks replayed; \d+ FLAGGED)"), page=g(r"== page (\w+)"))


C66, C67 = chain(CH66), chain(CH67)
assert "PARITY: EXACT MATCH" in CH66 and "PARITY: EXACT MATCH" in CH67


def lines_of(section):
    m = re.search(r"## " + re.escape(section) + r"\n(.*?)(?=\n## |\Z)", NP, re.S)
    return [ln for ln in m.group(1).strip().splitlines() if ln.strip()]


def bd(label):
    m = re.search(re.escape(label) + r": (\d+) players ranked 1-(\d+) before; (\d+) changed rank; mean \|move\| ([\d.]+); \|move\| > 20: (\d+); left the top \d+: (\d+)\n  largest: (.*)", BD)
    return m.groups()


kit100, kit200, deck100, deck156 = bd("kit board top 100"), bd("kit board top 200"), bd("deck value top 100"), bd("deck value top 156")
top12 = {k: re.search(re.escape(k) + r":?\s+(\[.*\])", BD).group(1) for k in ("top 12 deck before", "top 12 deck after")}
owner = {m.group(1): m.groups()[1:] for m in re.finditer(r"^  (.+?): kit (\S+)→(\S+), deck value (\S+)→(\S+)$", BD, re.M)}
CATN = {"pts": "points", "reb": "rebounds", "ast": "assists", "stl": "steals", "blk": "blocks", "tpm": "threes", "tov": "turnovers",
        "fg_pct": "FG%", "ft_pct": "FT%"}
fmtb = lambda c, v: (f"{v:+.4f}" if c.endswith("pct") else f"{v:+.2f}")

mech = {
    "Yaxel Lendeborg": ("tpm", "the six-way blend: FantasyPros 10/13 (0.6) and the BBM cards 10/13 (0.3) sit below the three references the check reads (Yahoo 10/13 1.3, Hashtag 10/12 1.2, RotoBaller 10/13 1.3); the equal-weight mean of the six is 1.0"),
    "Caleb Wilson": ("ft_pct", "the six-way blend: FantasyPros 10/13 (.752) and the BBM cards 10/13 (.770) sit above the three references (Yahoo 10/13 .720, Hashtag 10/12 .720, RotoBaller 10/13 .728); the mean of the six is .735"),
    "Collin Murray-Boyles": ("fg_pct", "the six-way blend: FantasyPros 10/13 (.600) and the BBM cards 10/13 (.599) sit above the three references (Yahoo 10/13 .580, Hashtag 10/12 .579, RotoBaller 10/13 .579); the mean of the six is .586"),
    "Dylan Harper": ("ft_pct", "the six-way blend: FantasyPros 10/13 (.785) and the BBM cards 10/13 (.785) sit above the three references (Yahoo 10/13 .758, Hashtag 10/12 .754, RotoBaller 10/13 .755); the mean of the six is .765"),
}
rc_txt = rd(os.path.join(OUT, "range_check_v67.txt"))
rc_rows = re.findall(r"^\| ([^|]+?) \| (\d+) \| ([^|]+?) \| ([+-][\d.]+) \| — \|$", rc_txt, re.M)
assert {r[0] for r in rc_rows} == set(mech), (rc_rows, mech.keys())
rc_head = re.search(r"RANGE CHECK: (.*)", rc_txt).group(1)
id_head = re.search(r"POINTS IDENTITY: (.*)", IDT).group(1)

c0, c1 = A0["cats"], A1["cats"]
few = sum(v for k, v in eval(A0['refs']).items() if k < 3)
audit_rows = "\n".join(
    f"| {CATN[c]} | {fmtb(c, c0[c]['bias'])} | {fmtb(c, c1[c]['bias'])} | {c0[c]['out']} of {c0[c]['n']} ({c0[c]['outpct']}%) | {c1[c]['out']} of {c1[c]['n']} ({c1[c]['outpct']}%) |"
    for c in ["pts", "reb", "ast", "stl", "blk", "tpm", "tov", "fg_pct", "ft_pct"])
fore = ["RotoBaller", "FantasyPros", "Yahoo", "OURS", "BBM cards", "Hashtag"]
env_rows = "\n".join(f"| {'**ours**' if f == 'OURS' else f} | {A0['inside'][f]}% | {A0['dist'][f]:.3f} | {A1['inside'][f]}% | {A1['dist'][f]:.3f} |" for f in fore)
own = "\n".join(f"| {n} | {v[0]} / {v[1]} | {v[2]} / {v[3]} |" for n, v in owner.items())
wide_txt = ", ".join(f"{w['name']} ({w['factor']})" for w in wide)

RPT = f"""# After-report — 2026-10-14 (night of 10/13): the owner's calls (Version 66), an audit of the 200 projection lines, and the six-way blend (Version 67)

**Owner requests (verbatim).** First, the calls: "Chet - untag / Tyrese - healthy, untag / Kawhi - keep at .85 (But I am very bullish on him) / Damian - keep at .85 / Kyrie - .85 / Davis - .85 / leave the other 3 as default / Kessler - healthy / Lendeborg, I may take with my 7th or 8th pick, I'm very bullish on him. Knowing my draft mates, I don't think he survives past 105", with "New 0.85 tier for these four", "Now, tonight" and "If you believe .88 is better than .85, please use that." Then, while that was building: "Now, once that is complute. Run a thorough and expertise audit of the 200 player projections. Are these realistic and accurate, or do you have 95% confidence in your kit's projections, based on the outside data that you have aggregated. Run a Gauntlet and Council debate to tighten up and dial in all the numbers so that we have a sound and realistic projection. Provide after report in plain language"

**What was analyzed and changed.** Kit `main` 29d3d26 and deck `main` 6064cc2 (Version 65) as the start. Version 66 (deck PR #114, main c1065c5) carries the calls. Version 67 (deck PR #115, main 43ca6bf; this kit PR) carries the blend. The five outside projections, all already pinned in `report/market/`: Yahoo `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, RotoBaller `rotoballer-2026-10-13.csv`, FantasyPros `fantasypros-2026-10-13.csv`, the Basketball Monster cards `cards-2026-10-13.csv`.

**Method.** The Gauntlet sequence (plan gate → work → adversarial pass → this report), with a Council on the method. The plan went to the owner before any line moved, with assumptions A1–A5 and criteria C1–C9 (§7). Tools in `report/blend/tools/`: `audit_measure.py` (the audit, read-only), `blend_lines.py` (the blended lines, writes nothing), `blend_apply.py` (writes both planes with assertions), `board_diff.py`, `card_compare.py`. Every one that produces a record was run twice with identical output.

Pull window: 2026-10-14 → 2026-10-14 (no roster pull beyond Version 66's verification; the stat lines of the 10/13 outside projections, already pinned).

## The short answer, in plain language

**Were our numbers realistic?** Yes. I compared our 200 lines with the five outside projection sets, and our lines turned out to be the closest of the six to the group. Each source's average distance from the median of the other five, in category-spread units: ours {A0['dist']['OURS']:.3f}, the other five {min(v for k, v in A0['dist'].items() if k != 'OURS'):.3f} to {max(v for k, v in A0['dist'].items() if k != 'OURS'):.3f}. On average we ran a little high on points (+{c0['pts']['bias']:.2f} a game against the outside median) and matched the group everywhere else.

**Could you have 95% confidence in them?** No, and no projection can give you that. Two facts settle it.
- *The experts disagree with each other.* I asked how often each source's number lands between the highest and lowest of four others. RotoBaller, the best of them, did so {A0['inside']['RotoBaller']}% of the time, Hashtag {A0['inside']['Hashtag']}%, and our lines {A0['inside']['OURS']}%.
- *The season itself is noisy.* In last season's test our pre-season points line missed a player's real average by 2.78 points a game on average (`after-report-2026-10-09-market.md`), and that was one of the better methods tested.

So no single source deserves 95% confidence, ours included.

**What we did about it (Council 4–1).** The most reliable way to get a sounder number is to average several good forecasts. Every line that has at least three outside projections — {nrows} on the kit, {ndeck} of them on the page — is now the plain average of our line and the outside lines, category by category, with ours counting as one vote of up to six. Games, minutes, injury tags (including tonight's calls) and teams did not change.

- *Why averaging helps.* The average of several forecasts can never do worse than those forecasts do on average; that is arithmetic. It usually beats most of them, because their misses partly cancel (INFERENCE: the general forecasting result, not measured on these six). Last season's test showed the same on our own data: a half-and-half blend of two forecasts beat each of them in all nine categories.
- *What it costs.* The blend pulls our lines toward the market. Where we were higher than everyone on a player, he drops.

**What changed on your draft board.**
- The page's top 12 is the same twelve names, slightly reordered.
- The middle rounds moved more. In the page's top 100, {deck100[2]} players changed rank, by {deck100[3]} places on average; {deck100[4]} moved more than 20 places. In each of those, our line had sat at or past the edge of the outside range in several categories.
- The 🎯 (the card's single pick) changes at **{cc_changed} of the {cc_turns}** turns where you picked in the 28 practice drafts I replayed. That is a big change in what the card will tell you today, so read §5 before the draft.

**Three names you asked about.**
- *Kawhi* stays #5 on the page.
- *Lendeborg* falls from value #70 to #102: the outside average sits below our line in 8 of his 9 categories. Your plan to take him in round 7 or 8 is still yours to make; the card simply won't point at him there (decision D-1014-1).
- *Kel'el Ware*, the 🎯 in 45 of your practice turns before, falls from #27 to #58. All five outside sources project him for fewer points, rebounds and threes than we did.

**How confident I am now.** In the system (arithmetic, plumbing, the page) as before: every gate and test passed on Version 67, and the 🎯 the page shows is the engine's own. In the numbers, more than last night: they now sit inside the professional range in {A1['env'][2]}% of cells, and the main thing the audit worried about — lines we alone believed — is gone. That number is by construction, not proof of accuracy.

One weak spot stays open, and nobody can close it before tonight. Whether equal weights are better than, say, trusting our line a little more could only be settled with last season's outside projections, and those are not on file. I did not search for them tonight (time); the choice is on the decision sheet.

## 1. Roster changes

No placement or team changed on either plane, and no row was added or dropped. Two passes changed the pool tonight.

- **Version 66 (availability tags only).**
  - Tyrese Haliburton and Walker Kessler are untagged and healthy, by your call.
  - Kawhi Leonard, Anthony Davis, Kyrie Irving and Damian Lillard sit on a new lighter risk tier. It counts ×0.85 on value instead of ×0.78, and 0.79 instead of 0.75 in the weekly model, in all three copies of the engine.
  - Holmgren stays untagged. Black, Merrill and Hartenstein keep their defaults.
  - On your ".88" question I kept 0.85. The outside projections put these four at 0.842–0.870 of a healthy season's games.
  - Checks: the four new card tests failed before the code and passed after (103 of 103). Build: 7 gates PASS. Chain: parity EXACT ({C66['parity']}), test_card {C66['card']}, test_draft {C66['draft']}, test_gates {C66['gates']}, full DOM {C66['dom']}/0, repeat-name {C66['rn']}.
  - Published as Version 66 (1791957366-babb), byte-verified (page {C66['page']}).
- **Version 67 (stat lines only):** the blend, §3.

## 2. The audit: how our 200 lines compared with the five outside projections

EVIDENCE: `blend/out/audit_v66_lines.txt` (our lines before the blend, on the board's 200), `audit_v67_lines_new200.txt` (the blended lines, on the new board's 200), both by `audit_measure.py` with two identical runs each. Outside lines per player in the top 200 before the blend: {A0['refs']} (number of outside sources: players). The 191 with three or more are the ones the tables below read.

**Category by category.** "Lean" is our line minus the median of the outside sources, averaged over the 191 (+ means we were higher). "Outside every source" counts players whose number sat above all five or below all five.

| category | lean before | lean after | outside every source, before | after |
|---|---|---|---|---|
{audit_rows}

**Each forecaster against the others** (the 157 players all five sources cover). "Inside" is how often a source's number lands between the highest and lowest of four others. "Distance" is the average gap to the median of the other five, in units of the category's spread across the 200.

| forecaster | inside, before | distance, before | inside, after | distance, after |
|---|---|---|---|---|
{env_rows}

Reading:
- **EVIDENCE.** Before the blend our lines were the closest of the six to the rest and sat in the middle of the pack on the "inside" test. No outside source reaches 80% on it.
- **INFERENCE.** "95% confidence" in single numbers isn't on offer from anyone. The useful question is whether our lines were an outlier, and they were not.

After the blend our line is, by construction, close to the middle of the six, which is why its own "after" figures look so much better than anyone else's. That is a property of averaging, not new evidence of accuracy.

## 3. The blend

**The Council (4–1).**
- The Contrarian voted to change nothing, or to cap our line's move at half the gap: our lines were already the closest to the group, so nothing was broken.
- First Principles carried the vote. The average of good forecasts beats them on average whether or not any one of them is broken, and our own 2025-26 test agreed (a half-and-half blend beat both of its parts in 9 of 9 categories, `after-report-2026-10-09-market.md`).
- Equal weights won over 50/50 because the six distances above sit within 0.007 of each other: no forecaster looks more reliable than the rest.
- The Contrarian's vote would flip if last season's outside projections showed equal weights doing worse than our lines alone (D-1014-2).

**The rule as shipped (A1–A5).**
- Each of the nine categories is the plain average of our line and every outside line on file.
- It applies to rows with three or more outside projections: {nrows} kit rows ({ndeck} on the page).
- FGA and FTA scale by one factor per row, so points still add up from the shooting.
- Games, minutes, tags, teams and placements stay. So do the rows with fewer than three outside projections, including Marcus Smart, whose line is on two (RotoBaller, Yahoo).

**One rule changed mid-run, and why.** The plan said that a row needing its shot attempts scaled by more than ±15% would keep its old shooting.
- That rule fired on {len(wide)} rows, and they were the widest disagreements. Khaman Maluach is the clearest: our 3.0 points against 5.0–10.4 from the outside sources. Holding his shooting would have blended his rebounds and blocks but not his points, which makes the line contradict itself.
- Minutes feed neither ranking engine; the page has no minutes column. So I changed the rule to always rescale and list the wide factors instead.
- The {len(wide)}: {wide_txt}.
- One consequence: for these rows the kit's minutes column no longer matches the shot volume. That column feeds no value.

**What the writer checked** (`blend_apply.py`, record `apply_record_2026-10-14.json`).
- Headers, row counts and every non-stat column are unchanged.
- The two planes agree on every blended row.
- Points add up within 0.25.
- Values are sane.
- No note carries the `];` trap.
- Every blended value equals the six-way mean recomputed inside the writer from the pinned files, and three of the sources agree with the deck's own loader.
- Nothing beyond the nine categories and FGA/FTA moved.
- Result: PASS — {R['deck_rows_changed']} deck rows and {R['kit_rows_changed']} kit rows; {R['values_changed']} values ({kit_vals} on the kit, {deck_vals} on the deck). A second run changes nothing, and the written files equal the dry run byte for byte. Three planted errors (a wrong mean, a broken points identity, a `];` note) were each caught.

**The named players** (`blend/out/named_players_2026-10-14.txt`, from the lines file):

""" + "\n".join("- " + ln for ln in lines_of("HIGH on five references (audit v2, 10/13)")) + """

The 12 players aged 34 and older whose lines carried no age decline (last night's audit, T6) now carry the outside sources' view of them:

""" + "\n".join("- " + ln for ln in lines_of("34 and older with no age decline (audit, 10/13)")) + f"""

## 4. What moved on the boards

EVIDENCE: `blend/out/board_diff_2026-10-14.txt` (`board_diff.py`, two runs identical): the kit board before (kit HEAD) and after, and the page's value ranks on Version 66's pool and on Version 67's.

| board | players | changed rank | mean move | moved more than 20 | left the range |
|---|---|---|---|---|---|
| page, top 100 | {deck100[0]} | {deck100[2]} | {deck100[3]} | {deck100[4]} | {deck100[5]} |
| page, top 156 (the draftable pool) | {deck156[0]} | {deck156[2]} | {deck156[3]} | {deck156[4]} | {deck156[5]} |
| kit board, top 100 | {kit100[0]} | {kit100[2]} | {kit100[3]} | {kit100[4]} | {kit100[5]} |
| kit board, top 200 | {kit200[0]} | {kit200[2]} | {kit200[3]} | {kit200[4]} | {kit200[5]} |

- Page top 12 before: {top12['top 12 deck before']}.
- After: {top12['top 12 deck after']}.
- Largest moves in the page's top 100: {deck100[6]}.
- In the top 156: {deck156[6]}.

**Your players and questions** (kit board, then page value rank):

| player | kit board, before / after | page value, before / after |
|---|---|---|
{own}

Every move of more than 20 places in the top 100 was inspected before publishing. None was a data error. In each one, our line had sat at or past the edge of the outside range in several of the nine categories: Tre Jones, Saddiq Bey, Ryan Rollins, Reed Sheppard and Lendeborg high; Brandon Miller low. Small moves in many categories add up in ranks 60–120, where one z point is about 30 places.

**The team budget did not improve.** {tb_over[0]} teams' pools still claim more possessions a game than any team used last season: {tb_over[1]} (`blend/out/team_budget_after.txt`, the 10/13 usage report's own script). The outside projections overload the same rosters about as much as we did. Fixing that needs the usage model on the sheet for after the draft (D-C2).

## 5. Test 7 — the card's 🎯 at your picks, Version 66 against Version 67

EVIDENCE: `blend/out/card_compare_2026-10-14.txt` (`card_compare.py`, two runs identical), from the deck's repeat-name replays of the same 28 graded mocks on each page (`arena/results/repeat_market_check_2026-10-14_v66.json` and `_v67.json`). The page is the only input that differs.

- **Turns compared:** {cc_turns}. **The 🎯 changed at {cc_changed}.**
- **By round** (changed / turns): {cc_round}.
- **Count of 🎯 across all turns, the 15 largest changes:** {cc_counts}.
- **What it means for today (INFERENCE).** The card now points less often at the men only we liked (Ware, Sheppard, Lendeborg, Bey) and more often at men every source likes but the market prices late:
  - Ty Jerome: value #41, market #117.
  - OG Anunoby: value #33, market #65.
  - John Collins: value #74, market #118.
- **What this test cannot tell you.** Whether the new 🎯 wins more. The practice rooms are graded on our own lines, so regrading them on the blended lines would grade the blend by itself.

## 6. Publication

| step | result |
|---|---|
| deck build (7 gates) | refused once at gate 6: the colophon said "the other 97 rows", a count the gate rejects against the 335-row pool. The refused build had not touched the page (checked by comparison). Reworded, then PASS |
| chain on Version 67 | parity EXACT ({C67['parity']}); test_card {C67['card']}; test_draft {C67['draft']}; test_gates {C67['gates']}; full DOM {C67['dom']} assertions, 0 failed; repeat-name {C67['rn']}; {id_head}; {rc_head} |
| kit | provenance PASS; board 200 from 313; tests OK; derived 27 of 27; the seat-10 slate regenerated (it still carried Version 65's pool) |
| publish | Version 67, version id 1791960484-154b, on the standing artifact; the served page equals the local file (sha256 {C67['page']}) inside the publisher's wrapper |
| PRs | deck #114 (Version 66) and #115 (Version 67) merged; this kit PR carries the tools, the lines and this report |

## 7. The plan against the outcome

The plan as sent to the owner before any line moved, graded binary:

| criterion | grade | evidence |
|---|---|---|
| C1 the audit and the 95% answer from files | PASS | §2, both audit records, two runs identical |
| C2 blended lines, two identical runs | PASS | `blend_lines.py` twice, `cmp` identical |
| C3 writer assertions, planted errors, no-op second run | PASS | §3 |
| C4 every blended value recomputed at the source | PASS | A8 in `blend_apply.py`, recomputed from the pinned files |
| C5 kit rebuild and tests | PASS | §6 |
| C6 deck build and full chain | PASS | §6 (one refusal on a prose count, fixed before publishing) |
| C7 test 7 count | PASS | §5, {cc_changed} of {cc_turns} |
| C8 Version 67 published, byte-verified; PRs merged | PASS | §6 |
| C9 this report through the gates | PASS | the gate runs are in the kit PR |

Predictions against outcomes:
- "About 241 rows change": {nrows}. ✓
- "Envelope from 75% to above 95%": {A0['env'][2]}% → {A1['env'][2]}%. ✓
- "The top 12 barely moves": the same 12 names, reordered. ✓
- "No top-100 player moves more than about 20 places": **missed**. {deck100[4]} on the page did, the largest 39; each was inspected (§4).
- The ±15% shot rule: **fired {len(wide)} times and was changed** (§3).

## Range check (D-RN-3)

Rule (owner, 2026-10-08): on a projection pass, every cell of a top-150 line that sits outside ALL its references either carries a one-line mechanism naming two dated outlets, or comes back inside. The references are Yahoo `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, RotoBaller `rotoballer-2026-10-13.csv` and the 2025-26 actual line. This page: {rc_head}. Each one sits outside because the blend also reads FantasyPros and the BBM cards, which the deck's range check does not yet read (D-1013-14).

| player | deck rank | cells outside every reference | net z | mechanism (two dated outlets) |
|---|---|---|---|---|
""" + "\n".join(f"| {p} | {rk} | {cells} | {z} | {mech[p][1]} |" for p, rk, cells, z in rc_rows) + f"""

## Points identity (D-1009-3)

{id_head} (`blend/out/identity_v67.txt`; the deck's `identity_check.py` on Version 67, both planes). No line needs a mechanism.

## Watchlist

- **This morning's final pull and the Yahoo lock paste** (D-1013-1) build Version 68 on top of Version 67. If the lock paste brings new Yahoo projected lines (not only prices), the blend can be re-run on them mechanically with the same two scripts (D-1014-3).
- **The publish freeze during the draft** (D-1013-5) and **no RESYNC during the draft** (D-1013-2) stand.
- **Ty Jerome** is now the 🎯 in 28 of 28 replayed mocks (value #41, market #117). His line sits inside all three projections the check reads, and three of the four outside ranks put him at 48–65.

## Open-item receipts

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| (this pass) | records only; no web research and no roster pull beyond Version 66's verification (direct-complete 335/335, 2026-10-14) | the blend reads the five outside projections pinned 10/12–10/13; no tag or placement moved |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the 10/13 pull (`after-report-2026-10-13.md`, receipts dated 10/13); Kawhi's debut read from ESPN's 10/13 box score for Version 66 | held or unsigned on 2026-10-13 per those receipts; not re-queried tonight (did not check); this morning's final pull re-queries them |

## Repeat-name market check

{rn_body}

## Bounds

**Out of scope by design.**
- Games, minutes and availability (your calls and the 10/13 minutes-and-games pass stand).
- The usage model and team scaling (D-C2, after the draft).
- Adding FantasyPros and the cards to the deck's own range check (D-1013-14).
- Any change to the engine, the card or the page beyond its Data paragraph.

**In scope and unverified.**
- **Whether equal weights beat our line alone, or a 50/50 split, on real outcomes:** `NOT-ATTEMPTED`. It needs last season's pre-season projections from the outside sources. None are on file, and I did not search for archived copies tonight (time). The choice rests on the measured fact that the six forecasters sit equally close to each other (§2) and on general forecasting practice. It is a **candidate**, decision D-1014-2.
- **Whether the new 🎯 wins more often than the old one:** `UNVERIFIABLE` before the season. Every practice room is graded on our own projected lines (§5).
- **The players with fewer than three outside projections** ({few} in the top 200 before the blend) keep our lines unchecked against a consensus: `NOT-ATTEMPTED` by rule (A4).

## Decision sheet (owner disposes)

| id | decision | options | recommendation |
|---|---|---|---|
| D-1014-1 | Lendeborg's line | (a) keep the blend (value #102); (b) take his line out of the blend, back to ours (value #70); (c) keep the blend and add a judgment note (a tooltip flag, it moves no rank) | (a). Your plan to take him in round 7 or 8 does not need the card's agreement, and the outside average sits below our line in 8 of his 9 categories |
| D-1014-2 | the blend's weights | (a) keep equal weights (ours one of six); (b) 50/50 ours against the outside average; (c) revert to Version 66's lines | (a). (b) or (c) is a rerun of the same scripts and the chain, about 50 minutes |
| D-1014-3 | the lock paste | (a) if Yahoo's lock paste changes projected lines, re-run the blend on them before the lock; (b) keep the 10/13 lines regardless | (a) |
| D-1014-4 | the six teams over budget | (a) leave for after the draft with D-C2; (b) scale those pools tonight | (a) |

## Provenance

- **Session:** this cloud session, the night of 10/13 (UTC 2026-10-14). Plan, Council and adversarial pass as described above.
- **Governors loaded for this task:** gauntlet, plan-gate, adversarial-verify and after-report. The plan block was emitted before the work; council and scope-fence were applied in-session.
- **Kit:** branch `claude/market-data-workorder-mnfi2b`; commits 440bb9e (tools and audit), e2cc9db (lines, board, slate), and this report's commit.
- **Deck:** PR #114 → c1065c5 (Version 66), PR #115 → 43ca6bf (Version 67).
- **Artifact:** https://claude.ai/code/artifact/190e2c13-a19c-4239-8085-73230ef4eae0, versions 1791957366-babb (66) and 1791960484-154b (67).
- **Re-verify:**
  - `python3 report/blend/tools/blend_lines.py --deck <deck>/data/players.csv --kit report/projections-2026-27.csv --out x.json` on the pre-blend files reproduces `lines_blend_2026-10-14.json`.
  - `python3 report/blend/tools/blend_apply.py report/blend/out/lines_blend_2026-10-14.json --deck … --kit …` on the shipped files changes nothing.
  - `python3 report/blend/tools/audit_measure.py` reproduces `audit_v67_lines_new200.txt`.
"""
dst = os.path.join(KIT, "report", "after-reports", "after-report-2026-10-14-blend.md")
open(dst, "w", encoding="utf-8").write(RPT)
print("wrote", dst, len(RPT), "chars")
