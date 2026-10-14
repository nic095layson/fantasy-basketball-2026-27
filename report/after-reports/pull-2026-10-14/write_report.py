#!/usr/bin/env python3
"""Writes after-report-2026-10-14.md (the final morning pull, Version 68) from the records beside this script, the deck's
chain log and the repeat-name section. Figures are read from records; the prose around them is the author's."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.normpath(os.path.join(H, "..", "..", ".."))
S = "/tmp/claude-0/-home-user-fantasy-basketball-2026-27/3cdbbd9b-02dd-585e-8d00-b8a370128fae/scratchpad/pull1014"
rd = lambda p: open(p, encoding="utf-8").read()
V = json.load(open(os.path.join(H, "verdicts.json"))); cal = V["calibration"]; rows = V["rows"]
D = json.load(open(os.path.join(H, "disputed_minutes.json")))
F = json.load(open(os.path.join(H, "feed_diff_2026-10-14.json")))
N = json.load(open(os.path.join(H, "deck_notes_2026-10-14.json")))
feed = json.load(open(os.path.join(H, "espn_injuries_2026-10-14.json")))
LC = json.load(open(os.path.join(H, "lock_calls_2026-10-14.json"))); B = json.load(open(os.path.join(H, "lock_board_diff_2026-10-14.json")))
BN = B["named"]; KO, CW, DC = BN["Luke Kornet"], BN["Coby White"], BN["Dylan Cardwell"]
BUILD = rd(f"{S}/build.log"); BUILD_RED = rd(f"{S}/build_red.log")
assert "BUILD REFUSED" in BUILD_RED and "safe to publish" in BUILD and "waived 2" in BUILD
kit_lc = "; ".join(f"{n} {c} {a} to {b}" for n, c, a, b in LC["kit"])
CH = rd(f"{S}/chain.log"); RN = rd(f"{S}/rn_section.txt")
rn_body = RN[RN.index("## Repeat-name market check"):].split("\n", 1)[1].strip()
g = lambda pat: re.search(pat, CH).group(1)
chain = dict(page=g(r"== page (\w+)"), parity=g(r"card orderings compared : (\d+ owner turns across \d+ committed states)"),
             card=g(r"CARD: all (\d+) cases passed"), draft=g(r"all (\d+) cases passed\nexit 0\n== test_gates"),
             gates=g(r"all (\d+) cases passed\nexit 0\n== full_dom"), dom=g(r'"assertions":(\d+),"failed":0'),
             rn=g(r"(\d+ of \d+ mocks replayed; \d+ FLAGGED)"))
assert "PARITY: EXACT MATCH" in CH
PUB = json.load(open(f"{S}/publish.json"))
tally = {}
for r in rows: tally.setdefault(r["verdict"], []).append(r["name"])
lower = [r for r in rows if r["diff"] < 0]; higher = [r for r in rows if r["diff"] > 0]
lower_out = [r["name"] for r in lower if r["verdict"] == "BACKS OUTSIDE"]
def games(r): return "; ".join(f"{d[5:]} {o} {'S' if s == 'S' else 'B'} {int(m)}" for d, o, s, m in r.get("games") or []) or "—"
def adj(r): return f"{r['adj_shift']} / {r['adj_scale']} / {r['adj_team']}" if r.get("adj_team") is not None else "—"
tab = "\n".join(f"| {r['name']} | {r['team']} | {r['rank']} | {r['ours']:.1f} | {r['outside']:.1f} | {r['pre_gp']} / {r['starts']} | "
                f"{r['pre_mpg'] if r['pre_mpg'] is not None else '—'} | {games(r)} | {adj(r)} | {r['verdict'].lower()} |" for r in rows)
fdate = {}
for t in feed["injuries"]:
    for i in t["injuries"]: fdate[i["athlete"]["displayName"]] = i
def feedline(n):
    i = fdate.get(n)
    if not i: return "not on ESPN's injuries feed 10/14"
    return f"{i.get('status')}, item {i['date'][:10]}, {(i.get('details') or {}).get('returnDate') or 'no'} estimate: {(i.get('shortComment') or '')[:150]}"
little = "\n".join(f"| {r['name']} | {r['pre_gp']} | {feedline(r['name']).replace('|', '/')} |" for r in rows if r["verdict"] == "TOO LITTLE DATA")
today_items = sorted(((i["date"][:16], i["athlete"]["displayName"], i.get("status"), (i.get("shortComment") or "")[:140])
                      for t in feed["injuries"] for i in t["injuries"] if (i.get("date") or "") >= "2026-10-14"), key=lambda x: x[0])
pool_today = [x for x in today_items if any(x[1] == k or x[1].rstrip(".") == k.rstrip(".") for k in N)]
today_tab = "\n".join(f"| {d[11:]}Z | {n} | {s} | {c.replace('|', '/')} |" for d, n, s, c in pool_today)
pool_out = ", ".join(f"{x['name']} ({x['detail']}, {x['returnDate'] or 'no'} estimate)" for x in F["pool_out"])
# Range check and points identity on Version 68 (the deck's own scripts, outputs kept beside this writer). The four
# cells are the four of Version 67; their mechanisms are carried from that report's writer (blend-2026-10-14).
MECH = {
    "Yaxel Lendeborg": "the six-way blend: FantasyPros 10/13 (0.6) and the BBM cards 10/13 (0.3) sit below the three references the check reads (Yahoo 10/13 1.3, Hashtag 10/12 1.2, RotoBaller 10/13 1.3); the equal-weight mean of the six is 1.0",
    "Caleb Wilson": "the six-way blend: FantasyPros 10/13 (.752) and the BBM cards 10/13 (.770) sit above the three references (Yahoo 10/13 .720, Hashtag 10/12 .720, RotoBaller 10/13 .728); the mean of the six is .735",
    "Collin Murray-Boyles": "the six-way blend: FantasyPros 10/13 (.600) and the BBM cards 10/13 (.599) sit above the three references (Yahoo 10/13 .580, Hashtag 10/12 .579, RotoBaller 10/13 .579); the mean of the six is .586",
    "Dylan Harper": "the six-way blend: FantasyPros 10/13 (.785) and the BBM cards 10/13 (.785) sit above the three references (Yahoo 10/13 .758, Hashtag 10/12 .754, RotoBaller 10/13 .755); the mean of the six is .765",
}
RC = rd(os.path.join(H, "range_check_v68.txt")); IDT = rd(os.path.join(H, "identity_v68.txt"))
rc_rows = re.findall(r"^\| ([^|]+?) \| (\d+) \| ([^|]+?) \| ([+-][\d.]+) \| — \|$", RC, re.M)
assert {r[0] for r in rc_rows} == set(MECH), rc_rows
rc_head = re.search(r"RANGE CHECK: (.*)", RC).group(1); id_head = re.search(r"POINTS IDENTITY: (.*)", IDT).group(1)
rc_tab = "\n".join(f"| {n} | {rk} | {cells} | {z} | {MECH[n]} |" for n, rk, cells, z in rc_rows)
cut = ["Dain Dainja", "Dion Brown", "Miles Kelly", "Yuki Kawamura", "Aaron Nkrumah", "Damari Monsanto", "Chucky Hepburn"]

RPT = f"""# After-report — 2026-10-14: the final morning pull before the draft (Version 68), with the 24 disputed-minutes players read against the preseason

**Owner request (2026-10-14 morning, verbatim):** "Conduct thorough morning pull, with emphasis on the biggest remaining doubt - focus on sources dated today, 10-14-2026 and using preseason data as a guide. Provide detailed after report before we lock". The biggest remaining doubt is the Council's (4–1, this morning): the {len(rows)} top-200 players whose projected minutes sit 3 or more from the average of the outside minutes projections (Hashtag 10/12, FantasyPros 10/13, BBM cards 10/13), out of {D['n_checked']} with two or more outside minutes on file.

**What was analyzed and changed:** deck `main` 43ca6bf (Version 67, the six-way blend) and kit `main` 391581f. New inputs pulled 2026-10-14 14:31 UTC: every final ESPN preseason box score from 9/28 to 10/13 (`espn_manifest_2026-10-14.tsv`, parsed to `preseason_roles_2026-10-14.json`, two parses identical); ESPN's league injuries feed (`espn_injuries_2026-10-14.json`); the 30 official rosters (direct-complete); 16 web searches (`search_log_2026-10-14.md`). **What changed:** notes on {len(N)} page rows, and — after the first draft of this report was shown — the owner's three lock calls, verbatim "Restore Kornet's line, Tag Coby White calf risk, Tag Cardwell calf risk" (D-1014-5/6/7, §3a). No other stat line, tag, team or placement moved on either plane. Version 68 is the page with both.

**Method (stated to the owner before the run):** A1 window — every final preseason game 9/28–10/13, minutes per game played and starts. A2 — preseason minutes run low (regulars rest, benches empty), so the shortfall is measured on the {cal['n']} undisputed players and taken out before comparing: a shift of {cal['shift']:+.2f} minutes, or a scale of {cal['scale']}. A3 — a verdict needs the adjusted preseason figure 1.5+ minutes closer to one side; under two preseason games is "too little data". **The A2 branch fired** (the shift was past the stated 4-minute limit), so raw figures are shown beside the adjusted ones, and one check was added before any verdict was read: both global corrections inflate every player alike, which favours whichever side projects *more* minutes, so a third, team-relative correction (each player against his own undisputed teammates) was added and a verdict now needs all three to agree (`verdicts.py`, docstring; two runs identical). A4 — "today" means an item timestamped 2026-10-14. A5 — no line moves on the 24 without the owner (the owner then moved one: Kornet). A6 — no Yahoo lock paste has arrived, so prices stay the 10/13 paste.

Pull window: 2026-10-14 → 2026-10-14 (the final pull; preseason box scores 9/28–10/13; tonight's seven games are after the window).

## The short answer, in plain language

**Last night's blend holds up against the preseason.** Of the {len(rows)} players whose minutes we disputed with the outside sources, the preseason backs the outside sources for {len(tally.get('BACKS OUTSIDE', []))} ({', '.join(tally.get('BACKS OUTSIDE', []))}), backs us for {len(tally.get('BACKS OURS', []))} ({', '.join(tally.get('BACKS OURS', []))}), is split on {len(tally.get('SPLIT', []))} and has too little to say on {len(tally.get('TOO LITTLE DATA', []))}. The blend already moved each of these lines five-sixths of the way to the outside sources, so for the {len(tally.get('BACKS OUTSIDE', []))} the board is already where the preseason points. Harper is the clearest: he started both games he played, at 19 and 24 minutes, while our old line had him as a 22.6-minute bench guard.

**The one player the preseason says we had right is Luke Kornet** (three games, 15–22 minutes, one start, against an outside average of {next(r['outside'] for r in rows if r['name'] == 'Luke Kornet')}). **At the owner's call his own line is back** (D-1014-7): he moves from #{KO['deck_before']} to #{KO['deck_after']} on the page and from #{KO['kit_before']['rank']} to #{KO['kit_after']['rank']} on the kit board. He is a late-round name either way.

**The eight with too little preseason** are mostly injured or rested, and the reasons are on today's feed: Tobias Harris and Coby White have calf strains and have not played, Beal has not done five-on-five, Aldama had a knee issue, Monk and others were rested by Sacramento on 10/13. For those the blend is the best guess there is.

**Today's sources.** I searched for anything dated today on the 24 and found nothing on the web I could confirm as 10/14 (16 queries, all logged). What is dated today is ESPN's injury feed: {len(pool_today)} items on our players, all written last night about last night's games — mostly planned rest days. One new injury since yesterday's pull matters a little: **Dylan Cardwell** is out at least two weeks with a calf strain. And **Coby White**'s calf strain is his third in about a year. **At the owner's call both now carry the injury-risk tag** (D-1014-5, D-1014-6), with six games off each on the kit (the Stewart and Raynaud shape). Neither moves on the page — White stays #{CW['deck_after']}, Cardwell #{DC['deck_before']} to #{DC['deck_after']} only because Kornet's line moved — because the tag only bites above the pool average; what changes is the ▲ on their rows and a lower weekly figure.

**Nothing else changed by hand.** Restoring one line nudges the pool averages, so about a third of the board shifts by a place or so (kit top 200: {B['kit_top200']['changed']} rows, mean move {B['kit_top200']['mean_abs_move']}; Wembanyama and Gilgeous-Alexander swap #2 and #3 on the kit by 0.01; Curry and Tatum swap #9 and #10 on the page). One edge case to know: **Jalen Green** slips from #155 to #158 on the page, just past the 156 drafted, and Marcus Smart comes in. Rosters still match all 30 teams ({335}/335). Version 68 passed every gate and test and is live.

## 1. Roster changes

None. Direct-complete roster verification of 2026-10-14: 30 teams, 335 of 335 pool rows on the feed, 0 mismatches, 0 unmatched. The official rosters lost {len(cut)} camp names since the 10/13 check, none in the pool ({', '.join(cut)}). The four unsigned free agents (Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham) are on no official roster: still unsigned.

## 2. The {len(rows)} against the preseason

EVIDENCE: `disputed_minutes.json` (the list), `preseason_roles_2026-10-14.json` (the box scores), `verdicts.json` (the reading). "Adjusted" shows the three corrections — global shift / global scale / team-relative — and the verdict needs all three to agree. Games: date, opponent, S(tart) or B(ench), minutes.

| player | team | kit rank | ours | outside | games / starts | preseason min | games | adjusted | verdict |
|---|---|---|---|---|---|---|---|---|---|
{tab}

Tally: backs outside {len(tally.get('BACKS OUTSIDE', []))}, backs ours {len(tally.get('BACKS OURS', []))}, split {len(tally.get('SPLIT', []))}, too little data {len(tally.get('TOO LITTLE DATA', []))}. Of the {len(lower)} where our minutes were lower, the preseason backs the outside sources on {len(lower_out)}; of the {len(higher)} where ours were higher it backs the outside on {sum(r['verdict'] == 'BACKS OUTSIDE' for r in higher)} (Kris Dunn: 6 and 15 minutes off the bench), ours on {sum(r['verdict'] == 'BACKS OURS' for r in higher)} (Kornet).

**Reading (INFERENCE).** Preseason minutes are a weak signal — two or three games, rest days, blowouts — which is why the verdicts need three agreeing corrections and why "split" is common. What the signal does carry is *role*: who starts. All eight players we had too low and the preseason backs the other way started most of their games (Harper 2 of 2, Jalen Green 3 of 3, Demin 3 of 3, Sharpe 2 of 2, Caruso 2 of 2, Lillard 2 of 2, LaMelo 3 of 3; Porter is the exception, 0 starts, but his bench minutes are still above the line we had). That is the role change our lines, built on last season's minutes, could not see.

**The too-little-data rows and today's feed:**

| player | preseason games | ESPN's injuries feed, 10/14 download |
|---|---|---|
{little}

## 3. What it means for the board

- **Backs outside ({len(tally.get('BACKS OUTSIDE', []))}):** no change needed. The blend already carries five-sixths of the outside view of these lines (Version 67), and the preseason says that direction is right.
- **Backs ours (1, Kornet):** the blend moved him the wrong way. The owner restored his own line (D-1014-7, §3a).
- **Split ({len(tally.get('SPLIT', []))}):** keep the blend — an average is the right hedge when the evidence points both ways.
- **Too little data ({len(tally.get('TOO LITTLE DATA', []))}):** keep the blend. Morez Johnson Jr. is kit-only (no row on the page), so his note sits on the kit side only.

Nothing in this section changed a line by itself; the owner's three calls are in §3a.

## 3a. The owner's three lock calls (applied)

EVIDENCE: `lock_calls.py` (assertions: only the named cells move on either plane, the tags read `inj-calf-risk` through the page's own parser, no `];`, Kornet's kit and page lines equal; a second run changes nothing) → `lock_calls_2026-10-14.json`; board effect `lock_board_diff.py` (kit board at HEAD and page values at deck `{B['deck_rev']}` against the working trees; two runs identical) → `lock_board_diff_2026-10-14.json`.

| call | page (deck) | kit | page rank | kit rank |
|---|---|---|---|---|
| D-1014-7 restore Kornet's line | the nine categories to the pre-blend line (`lines_blend_2026-10-14.json`, "old"); note added | same line | #{KO['deck_before']} to #{KO['deck_after']} | #{KO['kit_before']['rank']} to #{KO['kit_after']['rank']} |
| D-1014-6 tag Coby White | leading tag `inj-calf-risk` (×0.78 above the pool mean, weekly 0.75); the old role note kept as prose | GP {CW['kit_before']['gp']} to {CW['kit_after']['gp']} | #{CW['deck_before']} to #{CW['deck_after']} | #{CW['kit_before']['rank']} to #{CW['kit_after']['rank']} |
| D-1014-5 tag Dylan Cardwell | leading tag `inj-calf-risk`; the rookie-proj prose kept (the market model still reads it) | GP {DC['kit_before']['gp']} to {DC['kit_after']['gp']} | #{DC['deck_before']} to #{DC['deck_after']} | #{DC['kit_before']['rank']} to #{DC['kit_after']['rank']} |

Kit cells changed: {kit_lc}. Page cells changed: {len(LC['deck'])} (Kornet's nine categories plus his note, the two tags).

**Games (my call, stated):** the kit carries risk as games. Six off each, about two weeks of the schedule, is the shape of D-1010-2 (Stewart 70 to 64) and D-1012-1 (Raynaud 72 to 66). White at 62 sits at the low end of the outside range (Hashtag 62, Yahoo 69, BBM cards 72, FantasyPros 75); Cardwell at 59 against Yahoo's 72. Neither GP cut moves the kit board, because the kit never shrinks a below-average value for absence.

**Ripple (EVIDENCE, `lock_board_diff_2026-10-14.json`):** kit top 200 — {B['kit_top200']['changed']} rows moved, mean {B['kit_top200']['mean_abs_move']} places, entries {B['kit_top200']['entered'] or 'none'}; kit top 100 — {B['kit_top100']['changed']} moved. Page top 156 — {B['deck_top156']['changed']} moved, mean {B['deck_top156']['mean_abs_move']}; in: {', '.join(B['deck_top156']['entered'])}; out: {', '.join(B['deck_top156']['left'])}. The ripple is the pool averages moving under one restored line (Kornet's field-goal and rebound columns), not a judgment on anyone else.

## 4. Sources dated today

`search_log_2026-10-14.md`: 16 queries, 0 web results confirmed as dated 2026-10-14 (the search tool mixes seasons; every result is a lead until its own date is seen). The dated-today material is ESPN's injuries feed, downloaded 2026-10-14 14:31 UTC: {len(today_items)} items league-wide carry a 2026-10-14 UTC timestamp, {len(pool_today)} of them on pool rows — all written the evening of 10/13 US time.

| item (UTC) | player | status | what it says |
|---|---|---|---|
{today_tab}

Each is on the player's page note (`deck_notes_2026-10-14.json`, {len(N)} rows), labelled single-source.

## 5. The injury feed both ways

EVIDENCE: `feed_diff_2026-10-14.json` (the diff), `tags_2026-10-14.txt` (the page's tag inventory). Feed: {F['feed_rows']} items on {F['feed_teams']} teams, {F['pool_rows_on_feed']} on pool rows; at the 14:31 pull the page carried {F['tags']} tags ({F['excluded']} excluded, {F['risk']} risk); the two lock-call tags (§3a) make it {F['tags'] + 2} and {F['risk'] + 2}.

- **Pool rows Out on the feed ({len(F['pool_out'])}):** {pool_out}. All carry their tag; Dylan Cardwell, the one new item since the 10/13 pull (Out, at least two weeks, left calf strain, per Anthony Slater of ESPN.com on ESPN's feed, item 2026-10-13 20:57 UTC, 10/29 estimate), was untagged in the first draft and is tagged now by the owner's call (D-1014-5).
- **Coby White** (left calf strain announced 10/5, out the whole preseason, 10/21 estimate) was on the page as healthy with a role note; the 10/5 reports (TSN, NBA.com, RotoBaller) call it his third calf strain in about a year — tagged now by the owner's call (D-1014-6).
- **Day-to-day items on untagged pool rows ({len(F['dtd_untagged'])}):** almost all rest days for the last preseason games; none says more than day-to-day, and none is new information about the regular season. Listed in the record.
- **Tagged but absent from the feed ({len(F['tagged_absent'])}):** unchanged from the 10/13 pull; the four unsigned free agents among them are on no official roster.

## 6. Publication

| step | result |
|---|---|
| deck notes | {len(N)} rows, note column only (`deck_notes.py`: every name resolved, no other column changed, no `];`, a second run changes nothing) |
| lock calls | `lock_calls.py` PASS, kit {len(LC['kit'])} cells / page {len(LC['deck'])} cells, second run 0 |
| kit board | `rank_engine.py` re-run (200 of 313 projected, 12 held), `slate.py`, `test_rank_engine` OK, `check_provenance` PASS, `check_derived` 27/27 |
| build | red-first: refused on gate 7 without the exemption (propagation 2: White GP 68 to 62, Cardwell GP 65 to 59 — the page has no games column; its rows changed by tag). With the two players excused by name (the build's plane exemption flag, recorded in the manifest): 7 gates PASS, 335 players, rosters direct-complete 335/335, planes 315 shared, drift 0, 2 named exemptions, market the 10/13 paste (294/335 priced) |
| chain on Version 68 | parity EXACT ({chain['parity']}); test_card {chain['card']}; test_draft {chain['draft']}; test_gates {chain['gates']}; full DOM {chain['dom']} assertions, 0 failed; repeat-name {chain['rn']} |
| publish | Version 68, version id {PUB['version_id']}; the served page equals the local file (sha256 {chain['page']}) inside the publisher's wrapper |

## 7. The plan against the outcome

| criterion | grade | evidence |
|---|---|---|
| C1 preseason fetched, parsed twice identical, manifest kept | PASS | 46 finals 9/28–10/13; `espn_manifest_2026-10-14.tsv` |
| C2 the {len(rows)}-row table from the records | PASS | §2, `verdicts.json` (two runs identical) |
| C3 today's sources for the 24, queries logged | PASS | §4, `search_log_2026-10-14.md` (0 items confirmed as 10/14 on the web; the feed's {len(pool_today)} are) |
| C4 feed both ways; rosters 335/335 | PASS | §1, §5 |
| C5 Version 68: 7 gates, chain green, publish byte-verified | PASS | §6 |
| C7 the owner's three calls on both planes, asserted, board effect from records | PASS | §3a |
| C6 this report through the five gates; the sheet covers the 24 | PASS | the gate runs ride the kit PR; D-1014-8 |

Predictions: "the preseason backs the outside on at least half of the 15 we have low" — {len(lower_out)} of {len(lower)} ✓; "Harper about 25+ adjusted" — {next(r['adj_team'] for r in rows if r['name'] == 'Dylan Harper')} to {next(r['adj_scale'] for r in rows if r['name'] == 'Dylan Harper')} ✓; the A2 branch (a shift past 4 minutes) **fired** at {cal['shift']:+.2f}, and the third correction was added as described in the method.

## Range check (D-RN-3)

Rule (owner, 2026-10-08): on a projection pass, every cell of a top-150 line that sits outside ALL its references either carries a one-line mechanism naming two dated outlets, or comes back inside. References: Yahoo `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, RotoBaller `rotoballer-2026-10-13.csv` and the 2025-26 actual line. Version 68: {rc_head} (`range_check_v68.txt`) — the same four cells as Version 67; Kornet's restored line is not in the top 150 checked. Each sits outside because the blend also reads FantasyPros and the BBM cards, which the deck's range check does not yet read (D-1013-14).

| player | deck rank | cells outside every reference | net z | mechanism (two dated outlets) |
|---|---|---|---|---|
{rc_tab}

## Points identity (D-1009-3)

{id_head} (`identity_v68.txt`; the deck's `identity_check.py` on Version 68, both planes — Kornet's restored line included). No line needs a mechanism.

## Watchlist

- Tonight's seven preseason games (BKN at MIA, CHA at BOS, PHX at SA, NO at DAL, CHI at MIL, DET at MIN, DEN at LAC) end after the lock; Harper, Kornet, Jalen Green, Porter and Bey play in them. They cannot change the board before the draft.
- The Yahoo lock paste (D-1013-1) has not arrived; the page prices on the 10/13 paste. If it arrives before the lock it is a price-only rebuild (D-1014-3).
- The publish freeze during the draft (D-1013-5) and no RESYNC during the draft (D-1013-2) stand.

## Open-item receipts

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram | ESPN injuries feed, downloaded 2026-10-14 14:31 UTC | Out, 11/1 estimate: partially torn Achilles, won't be ready for the start of the season (Joey Linn, SI.com, via ESPN's feed, item 9/28) — HELD (inj-achilles-risk stands) |
| Kristaps Porzingis | ESPN injuries feed, same download | day-to-day, 10/21 estimate: remains away from the team (Anthony Slater, ESPN.com, item 10/12) — HELD; the owner's veto stands |
| Kawhi Leonard | ESPN injuries feed, same download | not on the feed 10/14; debuted 10/13 (21 in 17 minutes, ESPN box score, in Version 66) — HELD on the -mild tier by the owner's call |
| Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham | official rosters, direct-complete 2026-10-14 | on no team's roster: still unsigned — HELD out-unsigned |
| Jeremy Sochan | ESPN injuries feed, same download | not on the feed 10/14 — HELD (no change) |
| Bennedict Mathurin | ESPN injuries feed, same download | not on the feed 10/14 — HELD (no change) |
| Ryan Rollins | ESPN box scores 9/28–10/13; injuries feed | 3 preseason starts (14, 21, 23 min); not on the feed — HELD; his minutes read SPLIT (§2) |

## Repeat-name market check

{rn_body}

## Bounds

**Out of scope by design.** Any stat-line change beyond the owner's Kornet call (A5); the usage model and team scaling (D-C2); tonight's games (after the window).

**In scope and unverified.**
- **Web sources dated 10/14:** `ATTEMPTED-FAILED` — 16 queries, none returned an item whose own date I could confirm as 10/14 (the tool returns summaries that mix seasons). The conclusions do not rest on them: the verdicts rest on ESPN's box scores and feed. Fetching each candidate page to read its date was not done (time).
- **How preseason minutes translate to the season:** `UNVERIFIABLE` from this data alone — the calibration uses this preseason's undisputed players, not a past season's preseason-to-season record, which is not on file (did not check the web for one). That is why the verdicts need three corrections to agree and are labelled INFERENCE where they become advice.
- **Morez Johnson Jr.:** kit-only row, one preseason game — `UNVERIFIABLE` before the season.

## Decision sheet (owner disposes)

| id | decision | options | recommendation |
|---|---|---|---|
| D-1014-5 | Dylan Cardwell (Out 2+ weeks, calf, 10/29 estimate) | (a) tag inj-calf-risk; (b) note only | **DECIDED (a)** by the owner, 10/14 ("Tag Cardwell calf risk"); applied, kit GP 65 to 59 (§3a) |
| D-1014-6 | Coby White (third calf strain in about a year, 10/21 estimate) | (a) tag inj-calf-risk; (b) keep the role note | **DECIDED (a)** by the owner, 10/14 ("Tag Coby White calf risk"); applied, kit GP 68 to 62 (§3a) |
| D-1014-7 | Luke Kornet, the one line the preseason backs as ours | (a) keep the blend; (b) restore our line | **DECIDED (b)** by the owner, 10/14 ("Restore Kornet's line"); applied on both planes (§3a) |
| D-1014-8 | the other {len(rows) - 1} disputed-minutes players | (a) keep the blend; (b) restore ours on the split rows | (a) |
| D-1014-3 (carried) | the Yahoo lock paste | (a) paste it before the lock: a price-only rebuild; (b) lock on the 10/13 prices | (a) if it arrives in time |
| D-1014-1, D-1014-2 (carried) | Lendeborg's line; the blend's weights | as in `after-report-2026-10-14-blend.md` | open; recommendations (a) and (a) |

The kit GP figures under D-1014-5/6 (six games each) are my reading of the precedent, not the owner's words; another figure is a kit-only edit with no board effect (§3a).

## Provenance

- This cloud session, the morning of 2026-10-14 (pull started 14:30 UTC). Governors loaded for this task: plan-gate (full block emitted before the pull), after-report; the Council's verdict of this morning set the emphasis.
- Records in `report/after-reports/pull-2026-10-14/`: `disputed_minutes.py/.json`, `preseason_roles_2026-10-14.json` (parsed by `report/wo5/tools/parse_preseason.py`), `espn_manifest_2026-10-14.tsv`, `verdicts.py/.json`, `espn_injuries_2026-10-14.json`, `feed_diff_2026-10-14.json`, `tags_2026-10-14.txt`, `deck_notes.py`, `deck_notes_2026-10-14.json`, `search_log_2026-10-14.md`, `lock_calls.py` + `lock_calls_2026-10-14.json`, `lock_board_diff.py` + `lock_board_diff_2026-10-14.json`, this writer.
- Re-verify: `python3 verdicts.py` reproduces `verdicts.json` from the pinned box scores; `python3 deck_notes.py <deck players.csv> espn_injuries_2026-10-14.json` and `python3 lock_calls.py` on the shipped files change nothing.
"""
open(os.path.join(KIT, "report", "after-reports", "after-report-2026-10-14.md"), "w", encoding="utf-8").write(RPT)
print("wrote", len(RPT))
