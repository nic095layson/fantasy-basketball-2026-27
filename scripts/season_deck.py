#!/usr/bin/env python3
"""Season Deck: one HTML page rendered solely from the morning run's records (owner 2026-10-19 evening: "Proceed,
let's build it"; scope full dashboard, interactive board, auto-publish each morning, phone and desktop equally).

Inputs (all must exist; a missing or malformed record halts the build):
  brief         report/briefs/brief_<date>.json         (daily_brief.py)
  board         report/season/board_<date>.json         (season_board.py)
  status        data/status/status_<date>.json          (status_feed.py)
  league_state  data/league_state.json                  (league_intake.py)
  season_lines  data/season/season_lines_<date>.json    (season_lines.py)
  sweep         report/after-reports/redteam-2026-10-19/sweep.json  (standing red-team sweep)
  calibration   report/calibration.json                 (weekly_preview.py)

The page embeds those records verbatim as JSON and renders every figure from them in the browser; the static shell
carries no figure. The one derivation here is a mechanical join: each board row gains its fantasy owner (or FA).
The Trade Analyzer and Free-Agent Adder tabs (owner pitch 2026-10-19 evening; split into two tabs and the Waivers tab
removed on the owner's audit the same night) do z-score arithmetic on the board's own vectors in the page; its tier thresholds are stated defaults (D-SD-1), carried in the embedded config,
and the pane labels itself a screen — the sim-graded verdict (title odds) stays a session ask.
Writes report/season/deck_<date>.html and deck_record_<date>.json (sha256 of every input), but only after the page
drew itself in a headless browser (deck_render_check.py, owner 2026-10-21 decision B); otherwise it keeps the page as
deck_<date>.failed.html and prints SEASON DECK: FAIL.
"""
import argparse, datetime, hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

class DeckError(Exception): pass


def _load(path, what):
    if not os.path.exists(path): raise DeckError(f"{what} record missing: {path}")
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception as e:
        raise DeckError(f"{what} record unreadable: {path}: {e}")


def default_paths(date):
    return dict(brief=os.path.join(KIT, "report", "briefs", f"brief_{date}.json"),
                board=os.path.join(KIT, "report", "season", f"board_{date}.json"),
                status=os.path.join(KIT, "data", "status", f"status_{date}.json"),
                league_state=os.path.join(KIT, "data", "league_state.json"),
                season_lines=os.path.join(KIT, "data", "season", f"season_lines_{date}.json"),
                sweep=os.path.join(KIT, "report", "after-reports", "redteam-2026-10-19", "sweep.json"),
                calibration=os.path.join(KIT, "report", "calibration.json"),
                # optional (owner 2026-10-20; trade finder removed on the owner's veto 2026-10-20): absent renders nothing
                matchup_live=os.path.join(KIT, "data", "news", f"matchup_live_{date}.json"),
                # optional (owner 2026-10-21): the week's categories to date and projected (week_matchup.py)
                week_matchup=os.path.join(KIT, "report", "briefs", f"week_matchup_{date}.json"))


def resolve_rostered(rostered, board_names, held_names, aliases):
    """Map each rostered name (the league paste's spelling) to its season-board row or held name (the kit's spelling).
    Owner audit 2026-10-19: Jaren Jackson Jr. / Cameron Johnson showed as free agents under an exact-string join.
    Order: exact; accent-and-punctuation fold; the kit alias table (report/market/build_market.py); suffix-dropped
    name only when unique. Anything unresolved, or two rostered names on one row, halts the build."""
    import box_pull as BP
    targets = list(board_names) + [h for h in held_names if h not in board_names]
    exact = set(targets)
    by_fold = {}
    for t in targets: by_fold.setdefault(BP.fold(t), []).append(t)
    alias = {}
    for canon, variants in (aliases or {}).items():
        for v in variants:
            alias.setdefault(BP.fold(v), canon); alias.setdefault(BP.fold(canon), v)
    by_key = {}
    for t in targets: by_key.setdefault(BP.name_key(t), []).append(t)
    out, unresolved = {}, []
    for n in rostered:
        hit = None
        if n in exact: hit = n
        elif len(by_fold.get(BP.fold(n), [])) == 1: hit = by_fold[BP.fold(n)][0]
        else:
            a = alias.get(BP.fold(n))
            if a is not None and len(by_fold.get(BP.fold(a), [])) == 1: hit = by_fold[BP.fold(a)][0]
            elif len(by_key.get(BP.name_key(n), [])) == 1: hit = by_key[BP.name_key(n)][0]
        (unresolved.append(n) if hit is None else out.__setitem__(n, hit))
    if unresolved: raise DeckError(f"rostered player(s) with no season-board or held row: {sorted(unresolved)}")
    seen = {}
    for n, t in out.items():
        if t in seen: raise DeckError(f"two rostered names resolve to one row {t!r}: {seen[t]!r} and {n!r}")
        seen[t] = n
    return out


def build(paths, date):
    import co_gm
    import box_pull as BP
    my_seat = co_gm.OWNER_SEAT
    brief = _load(paths["brief"], "brief"); board = _load(paths["board"], "board")
    status = _load(paths["status"], "status"); league = _load(paths["league_state"], "league state")
    lines = _load(paths["season_lines"], "season lines"); sweep = _load(paths["sweep"], "sweep")
    calib = _load(paths["calibration"], "calibration")
    opt = lambda k: (json.load(open(paths[k], encoding="utf-8"))
                     if paths.get(k) and os.path.exists(paths[k]) else None)
    matchup_live = opt("matchup_live"); week_matchup = opt("week_matchup")
    for k in ("date", "opponent", "title", "lineup"):
        if k not in brief: raise DeckError(f"brief lacks {k}")
    if brief["date"] != date: raise DeckError(f"brief is for {brief['date']}, not {date}")
    # mechanical join: each board row gains its fantasy owner
    board_names = [r["name"] for r in board["board"]]
    rostered = [p["player"] for t in league["teams"] for p in t["players"]]
    rmap = resolve_rostered(rostered, board_names, board.get("held") or [], BP.load_aliases())
    on_board = set(board_names)
    own = {}
    my_team = None
    for t in league["teams"]:
        if t["seat"] == my_seat: my_team = t["name"]
        for p in t["players"]: own[rmap[p["player"]]] = (t["name"], t["seat"])
    if my_team is None: raise DeckError(f"league state has no seat {my_seat}")
    for r in board["board"]:
        o = own.get(r["name"])
        r["owner"] = o[0] if o else None; r["seat"] = o[1] if o else None
        r["fa"] = o is None; r["mine"] = bool(o and o[1] == my_seat)
    rosters = {t["name"]: dict(seat=t["seat"], manager=t.get("manager"),
                               players=[rmap[p["player"]] for p in t["players"] if rmap[p["player"]] in on_board],
                               off_board=[rmap[p["player"]] for p in t["players"] if rmap[p["player"]] not in on_board],
                               # owner 2026-10-20 (D-IS-8): IL players count 0 in the build strip; the page needs their names
                               il=[rmap[p["player"]] for p in t["players"]
                                   if (p.get("slot") or "").startswith("IL") and rmap[p["player"]] in on_board],
                               added=t.get("added_since_draft") or [], dropped=t.get("dropped_since_draft") or [],
                               unpooled_il=t.get("unpooled_il") or []) for t in league["teams"]}
    respelled = sorted((n, m) for n, m in rmap.items() if n != m)
    # every constant the standing sweep tiers FRAGILE, as daily_brief.band_line quotes them (2026-10-21: two since
    # deck 80eecdf, TEAM_WEEK_SHOCK and weekly_availability); a record without the list falls back to the tiers
    fragile = sweep.get("fragile") or [k for k, c in sweep["constants"].items() if c.get("tier") == "FRAGILE"]
    bands = []
    for key in fragile:
        c = sweep["constants"][key]
        bands.append(dict(name=key, tier=c["tier"], variants=[
            dict(label=v.get("label"), shift=v.get("shift_mean_1dp", f"{v['shift_mean']:+.1f}")) for v in c["variants"]]))
        if not bands[-1]["variants"]: raise DeckError(f"FRAGILE band {key} with no variants")
    band_engine = sweep.get("engine_commit") or sweep.get("engine")
    wk = calib.get("weeks", {}).get(str(brief.get("week"))) or {}
    data = dict(date=date, generated_utc=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                my_team=my_team, my_seat=my_seat, brief=brief, board=board, status=status,
                league=dict(as_of=league["as_of"], rosters=rosters, managers={t["name"]: t.get("manager") for t in league["teams"]}), season_lines=lines, matchup=wk,
                ledger=calib.get("weeks", {}), bands=bands, band_engine=band_engine, matchup_live=matchup_live,
                week_matchup=week_matchup,
                config=dict(cats=["FG%", "FT%", "3PM", "PTS", "REB", "AST", "STL", "BLK", "TOV"],
                            tier_low=0.3, tier_high=1.0, verdict_edge=0.5, verdict_strong=1.5,
                            thresholds_note="stated defaults, D-SD-1 (owner re-tunes); z screen only, not the simulator"))
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = SHELL.replace("__DATA__", payload)
    record = dict(date=date, out=f"report/season/deck_{date}.html",
                  # an optional input named but absent today (matchup_live on a morning with no matchup pull) is
                  # recorded as absent, not hashed: hashing it crashed the 10/21 runner (GAUNTLET decision 4).
                  # Required inputs never reach here missing; _load halts on them above.
                  inputs={k: dict(path=os.path.relpath(p, KIT) if p and p.startswith(KIT) else p,
                                  present=bool(p) and os.path.exists(p),
                                  sha256=hashlib.sha256(open(p, "rb").read()).hexdigest()
                                  if p and os.path.exists(p) else None) for k, p in paths.items()},
                  board_rows=len(board["board"]), status_rows=len(status["rows"]), panes=6,
                  join=dict(rostered=len(rostered), unresolved=0, on_board=sum(1 for n in rostered if rmap[n] in on_board),
                            off_board=sum(1 for n in rostered if rmap[n] not in on_board), respelled=respelled,
                            free_agents_on_board=sum(1 for r in board["board"] if r["fa"])))
    return html, data, record


SHELL = r"""<title>Season Deck 2026-27</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
/* layout: sticky scoreboard header with a scrollable tab rail; one column on phones, two for the Today pane on desktop */
:root{
  --bg:#F4F5F3; --surface:#FFFFFF; --ink:#1B2630; --ink2:#5B6670; --line:#DEE2E0; --chip:#ECEEEC;
  --accent:#C45A21; --mine:#077FA6; --pos:#2766A8; --neg:#C13F2E; --negtx:#B83A2A;
  --ok:#2E7D4F; --warn:#B26A00; --crit:#B3261E; --fade:#6A7680; --lead:#DCEAF4;
  --disp:"Barlow Condensed","Arial Narrow",system-ui,sans-serif;
  --body:"IBM Plex Sans","Segoe UI",system-ui,sans-serif;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#11161B; --surface:#1A222A; --ink:#E7EAEC; --ink2:#9AA4AD; --line:#2A343D; --chip:#232D36;
  --accent:#D06B2A; --mine:#1E97AD; --pos:#4484C8; --neg:#CE5240; --negtx:#E2735F;
  --ok:#5BB77F; --warn:#D9A04C; --crit:#E07069; --fade:#838E97; --lead:#1D3646; color-scheme:dark } }
:root[data-theme="dark"]{
  --bg:#11161B; --surface:#1A222A; --ink:#E7EAEC; --ink2:#9AA4AD; --line:#2A343D; --chip:#232D36;
  --accent:#D06B2A; --mine:#1E97AD; --pos:#4484C8; --neg:#CE5240; --negtx:#E2735F;
  --ok:#5BB77F; --warn:#D9A04C; --crit:#E07069; --fade:#838E97; --lead:#1D3646; color-scheme:dark }
body{background:var(--bg); color:var(--ink); font-family:var(--body); margin:0; font-size:15px; line-height:1.45}
.wrap{max-width:1060px; margin:0 auto; padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:0 48px}
body::before{content:""; position:fixed; inset:0 0 auto; height:env(safe-area-inset-top,0px); z-index:10; background:var(--bg)}
header.deck{position:sticky; top:env(safe-area-inset-top,0px); z-index:9; background:var(--bg); border-bottom:1px solid var(--line)}
header.deck .wrap{padding-block:10px 0}
h1{font-family:var(--disp); font-weight:700; font-size:28px; letter-spacing:.02em; margin:0; text-wrap:balance}
h1 .dt{color:var(--accent)}
.sub{color:var(--ink2); font-size:13px; margin:2px 0 8px}
nav.tabs{display:flex; gap:4px; overflow-x:auto; -webkit-overflow-scrolling:touch; padding-bottom:0}
nav.tabs button{appearance:none; border:0; background:none; color:var(--ink2); font-family:var(--disp); font-weight:600; font-size:17px; letter-spacing:.04em; text-transform:uppercase; padding:8px 12px 10px; cursor:pointer; border-bottom:3px solid transparent; white-space:nowrap; min-height:44px}
nav.tabs button[aria-selected="true"]{color:var(--ink); border-bottom-color:var(--accent)}
nav.tabs button:focus-visible{outline:2px solid var(--mine); outline-offset:-2px}
main .wrap{padding-top:16px}
section.pane{display:flex; flex-direction:column; gap:16px}
.card{background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:14px 16px; min-width:0}
.card h2{font-family:var(--disp); font-weight:600; font-size:19px; letter-spacing:.05em; text-transform:uppercase; margin:0 0 8px; color:var(--ink)}
.cols{display:grid; gap:16px; grid-template-columns:1fr}
@media (min-width:760px){ .cols{grid-template-columns:1fr 1fr} .cols .span2{grid-column:1/-1} }
.tiles{display:grid; gap:10px; grid-template-columns:repeat(auto-fit,minmax(130px,1fr))}
.tile{background:var(--chip); border-radius:6px; padding:10px 12px}
.tile .v{font-family:var(--disp); font-weight:700; font-size:26px; font-variant-numeric:tabular-nums}
.tile .l{font-size:12px; color:var(--ink2); text-transform:uppercase; letter-spacing:.06em}
.tile .e{font-size:12px; color:var(--ink2); font-variant-numeric:tabular-nums}
table{border-collapse:collapse; width:100%; font-variant-numeric:tabular-nums}
.tablebox{overflow-x:auto}
th,td{text-align:left; padding:5px 8px; border-bottom:1px solid var(--line); font-size:13.5px; white-space:nowrap}
th{color:var(--ink2); font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:.05em; cursor:default}
th.sort{cursor:pointer; text-decoration:underline dotted}
td.num,th.num{text-align:right}
.chip{display:inline-block; background:var(--chip); border-radius:999px; padding:1px 8px; font-size:12px; color:var(--ink2)}
.chip.mine{background:var(--mine); color:#fff}
.chip.fa{border:1px solid var(--line); background:none}
.chip.ok{color:var(--ok)} .chip.warn{color:var(--warn)} .chip.crit{color:var(--crit)}
.bar{display:flex; align-items:center; gap:6px; min-width:120px}
.bar i{display:block; height:10px; border-radius:4px; min-width:2px}
.bar.pos i{background:var(--pos)} .bar.neg i{background:var(--neg)}
.bar b{font-weight:500; font-size:12.5px; font-variant-numeric:tabular-nums}
.note{color:var(--ink2); font-size:12.5px}
.zero{color:var(--ink2); padding:14px 0}
select,input[type=search],input[type=text]{background:var(--surface); color:var(--ink); border:1px solid var(--line); border-radius:6px; padding:8px 10px; font-family:var(--body); font-size:14px; max-width:100%}
.pick{display:grid; grid-template-columns:1fr; gap:16px}
@media (min-width:640px){ .pick{grid-template-columns:1fr 1fr} }
.pick>div{min-width:0; display:flex; flex-direction:column; gap:8px}
.pick h2{margin:0}
.field{width:100%; height:40px; box-sizing:border-box}
.field.static{display:flex; align-items:center; border:1px solid var(--line); border-radius:6px; padding:0 10px; background:var(--chip); color:var(--ink2); font-size:14px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis}
.plist{border:1px solid var(--line); border-radius:6px; height:230px; overflow-y:auto; padding:4px; box-sizing:border-box}
.plist label{display:flex; gap:8px; align-items:center; padding:6px 8px; border-radius:4px; font-size:13.5px; min-height:32px}
.plist label:hover{background:var(--chip)}
.plist input{accent-color:var(--accent)}
.build{display:flex; flex-wrap:wrap; gap:6px; margin:10px 0 2px}
.bchip{display:flex; align-items:center; gap:5px; border:1px solid var(--line); border-radius:6px; padding:3px 8px; background:var(--chip)}
.bchip .bn{color:var(--ink2); font-size:11px; text-transform:uppercase; letter-spacing:.04em}
.bchip .br{font-weight:600; font-size:13px; font-variant-numeric:tabular-nums}
.bchip.up .br{color:var(--pos)} .bchip.down .br{color:var(--neg)}
.verdict{font-family:var(--disp); font-weight:700; font-size:22px; letter-spacing:.03em}
.verdict.pos{color:var(--pos)} .verdict.neg{color:var(--neg)} .verdict.even{color:var(--ink2)}
/* week card (owner 2026-10-21): projections faded — their own token (4.6:1+ on surface in both themes) and italic */
.proj{color:var(--fade); font-style:italic} .wk td.actual{color:var(--ink)} .wk th.projh{color:var(--fade); font-style:italic}
.wk th,.wk td{padding:5px 6px}  /* six columns fit a 400px phone without a sideways scroll */
/* the matchup board (owner 2026-10-23, after Yahoo's matchup page): header, category row, players side by side by slot */
.mb-head{display:grid; grid-template-columns:1fr auto 1fr; gap:12px; align-items:center; margin:2px 0 12px}
.mb-team{min-width:0} .mb-team.r{text-align:right}
.mb-name{font-family:var(--disp); font-size:26px; font-weight:600; line-height:1.1; color:var(--mine); overflow-wrap:anywhere}
.mb-team.r .mb-name{color:var(--accent)}
.mb-mgr{color:var(--ink2); font-size:13px}
.mb-score{font-family:var(--disp); font-size:36px; font-weight:600; display:flex; gap:10px; align-items:baseline; color:var(--ink)}
.mb-score span{font-size:14px; font-weight:400; color:var(--ink2)}
@media (max-width:560px){ .mb-name{font-size:19px} .mb-score{font-size:28px} .mb-head{gap:8px} }
.mb-cats td.lead,.mb-cats th.lead{background:var(--lead); font-weight:700}
.mb-cats td:first-child{white-space:normal; min-width:8em}
.mb-players th,.mb-players td{padding:4px 5px; font-size:12.5px}
@media (min-width:1100px){ .mb-players th,.mb-players td{padding:4px 4px} }
.mb-players td.slot,.mb-players th.slot,.mb-players td.mid{text-align:center; background:var(--chip); color:var(--ink2); font-weight:600}
.mb-pl{white-space:normal; min-width:8.5em}
.mb-pl b{font-weight:600; color:var(--ink)} .mb-pl .chip{margin-left:4px; padding:0 6px}
.mb-pl small{display:block; color:var(--ink2); font-size:11.5px}
.mb-players td.dash{color:var(--fade)}
.mb-players tr.mb-total td{font-weight:700; border-top:2px solid var(--line)}
.mb-empty{color:var(--fade)}
.zneg{color:var(--negtx)}  /* text red: 4.5:1+ on surface, bg and chip in both themes (--neg is for fills) */
.h2row{display:flex; justify-content:space-between; align-items:center; gap:10px; margin:0 0 8px}
.h2row h2{margin:0}
.resetbtn{border:1px solid var(--line); background:var(--surface); color:var(--ink2); border-radius:999px; padding:5px 14px; cursor:pointer; font-size:13px; min-height:32px}
.resetbtn:hover{background:var(--chip); color:var(--ink)}
.mode{display:flex; gap:8px; margin-bottom:10px}
.mode button{border:1px solid var(--line); background:var(--surface); color:var(--ink2); border-radius:999px; padding:7px 14px; cursor:pointer; font-size:13.5px; min-height:38px}
.mode button[aria-pressed="true"]{background:var(--ink); color:var(--bg); border-color:var(--ink)}
.cmp{display:grid; gap:4px; grid-template-columns:1fr auto 1fr; align-items:center; font-size:13px}
.cmp .cl{display:flex; justify-content:flex-end} .cmp .cr{display:flex}
.cmp i{display:block; height:9px; border-radius:4px; min-width:1px}
.cmp .cl i{background:var(--mine)} .cmp .cr i{background:var(--accent)}
.cmp .cc{color:var(--ink2); text-transform:uppercase; font-size:11px; letter-spacing:.05em; width:40px; text-align:center}
footer{color:var(--ink2); font-size:12px; margin-top:28px; border-top:1px solid var(--line); padding-top:10px}
@media (prefers-reduced-motion: no-preference){ nav.tabs button{transition:color .12s} }
</style>
<script id="deck-data" type="application/json">__DATA__</script>
<header class="deck"><div class="wrap">
  <h1>Season Deck <span class="dt" id="hdate"></span></h1>
  <div class="sub" id="hsub"></div>
  <nav class="tabs" id="tabs" role="tablist"></nav>
</div></header>
<main><div class="wrap">
  <section class="pane" id="pane-today" role="tabpanel"></section>
  <section class="pane" id="pane-trade" role="tabpanel" hidden></section>
  <section class="pane" id="pane-fa" role="tabpanel" hidden></section>
  <section class="pane" id="pane-board" role="tabpanel" hidden></section>
  <section class="pane" id="pane-movers" role="tabpanel" hidden></section>
  <section class="pane" id="pane-week" role="tabpanel" hidden></section>
  <footer id="foot"></footer>
</div></main>
<script>
"use strict";
const D = JSON.parse(document.getElementById("deck-data").textContent);
const C = D.config, CATS = C.cats;
const $ = (s)=>document.querySelector(s);
function h(tag, attrs, ...kids){ const el=document.createElement(tag);
  for(const [k,v] of Object.entries(attrs||{})){ if(k==="class") el.className=v; else if(k.startsWith("on")) el.addEventListener(k.slice(2),v); else el.setAttribute(k,v); }
  for(const k of kids.flat()){ if(k==null) continue; el.append(k.nodeType?k:document.createTextNode(k)); } return el; }
const f1=(x)=>(x==null?"—":(Math.round(x*10)/10).toFixed(1)), f2=(x)=>(x==null?"—":x.toFixed(2)), pct=(x)=>(x==null?"—":(x*100).toFixed(1)+"%");
const sgn=(x,d)=>((x>=0?"+":"")+x.toFixed(d==null?2:d));
// owner 2026-10-20: odds shown as the average of the two seeded runs (the seed labels read as years)
const avg2=(xs)=>{ const v=xs.filter(x=>x!=null); return v.length? v.reduce((a,b)=>a+b,0)/v.length : null; };
// owner 2026-10-20: negative z-scores in red font; a value that rounds to 0.00 stays uncolored
function zv(x, signed){ const t=signed? sgn(x) : f2(x); return h("span",(x!=null && Math.round(x*100)<0)?{class:"zneg"}:{},t); }
/*SWAP_MATH_BEGIN*/
function swapMath(inRows, outRows, cats){
  const d={}; let net=0;
  for(const c of cats){ let s=0;
    for(const r of inRows) s+=r.z[c]; for(const r of outRows) s-=r.z[c];
    d[c]=s; net+=s; }
  return {d:d, net:net};
}
/*SWAP_MATH_END*/
function tier(x, lo, hi){ const a=Math.abs(x); return a<lo?"low":(a<hi?"medium":"high"); }
function bandLine(){ if(!D.bands.length) return "no FRAGILE constant — engine "+(D.band_engine||"?"); return D.bands.map(b=>b.name.replace("arena.","")+" is "+b.tier+": "+b.variants.map(v=>v.shift+" ("+v.label+")").join(" / ")).join("; ")+" title points — engine "+(D.band_engine||"?"); }
function T(t){ if(t===D.my_team) return t+" (you)"; const m=(D.league.managers||{})[t]; return m? t+" ("+m+")" : t; }
function ownChip(r){ return r.mine? h("span",{class:"chip mine"},"mine") : r.fa? h("span",{class:"chip fa"},"FA") : h("span",{class:"chip"},T(r.owner)); }
function statusChip(letter){ if(!letter) return null; const cls=letter==="O"?"crit":(letter==="Q"?"warn":"ok"); return h("span",{class:"chip "+cls},letter); }

const swk=(x,d)=>{ const r=Number(x.toFixed(d)); return (r>0?"+":r<0?"−":"")+Math.abs(r).toFixed(d); };  // a true minus; 0 unsigned
// ---- This week's adds (owner 2026-10-22, P1): free agents by the change in expected categories won this week ----
function thisWeek(W){ const K=W.pickups, TW=K&&K.this_week; if(!TW) return null;
  if(TW.status!=="ran") return h("p",{class:"note"},"This week's adds: "+(TW.status==="no drop candidate"?"no lower-valued player to drop.":"no free agent to score."));
  const moved=(dc)=>Object.keys(dc).filter(c=>Math.abs(dc[c])>=0.005).sort((a,b)=>Math.abs(dc[b])-Math.abs(dc[a])).map(c=>c+" "+swk(dc[c],2)).join(", ")||"none";
  const da=TW.drop_alone||{}, das=Object.keys(da).map(d=>d+" "+swk(da[d],2));
  return [h("p",{},h("b",{},"This week's adds. "),"Each free agent from tomorrow in place of the lower-valued player whose drop helps most, by the change in expected categories won against "+W.opponent.name+" ("+TW.pool_size+" scored; best "+Math.min(8,TW.rows.length)+" shown):"),
    TW.rows.length? h("div",{class:"tablebox"},h("table",{},
      h("tr",{},h("th",{},"move"),h("th",{class:"num"},"Δ cats"),h("th",{class:"num"},"games"),h("th",{class:"num"},"drop's part"),h("th",{class:"num"},"season"),h("th",{},"categories moved")),
      TW.rows.slice(0,8).map(r=>h("tr",{},h("td",{style:"white-space:normal;min-width:9em"},r.add+" ("+r.team+")"+(r.status?" · "+r.status:"")+(r.missed?" · sat out "+r.missed:""),
          h("div",{class:"note"},"for "+r.drop)),
        h("td",{class:"num"},swk(r.d_exp,2)),h("td",{class:"num"},String(r.games)),h("td",{class:"num"},swk(r.d_exp_drop,2)),
        h("td",{class:"num"},r.season_d_ecw==null?"—":swk(r.season_d_ecw,3)),h("td",{style:"white-space:normal;min-width:10em"},moved(r.d_cat)))))) : h("div",{class:"zero"},"No free agent has a playable game after today."),
    das.length? h("p",{class:"note"},"Dropping with nobody added (from tomorrow): "+das.join("; ")+". A positive figure means that player's remaining games cost you categories this week; it is part of every move that drops him.") : null,
    (TW.no_games||[]).length? h("p",{class:"note"},"No playable game after today, so not ranked: "+TW.no_games.join(", ")+".") : null,
    h("p",{class:"note"},"Δ cats = the change in expected categories won this week (the sum of the nine changes in each category's chance); categories moved = those changes, largest first; season = the change in expected weekly categories over the season against the other eleven teams, the cost or gain beyond this week. Chances are normal approximations on the projected finals, with the variation of each remaining game (season per-game CV); the league allows 4 adds a week.")];
}

// ---- Week categories card (owner 2026-10-21): to date from box scores in full ink, projected final faded ----
function weekCard(){ const W=D.week_matchup, wk=D.brief.week;
  if(!W) return h("div",{class:"card wk"},h("h2",{},"Week "+wk+" categories"),
    h("div",{class:"zero"},"No week-to-date record for "+D.date+" (week_matchup.py did not run, or failed, this morning)."));
  try{
    const isPct=(c)=>c.indexOf("%")>=0;
    const fv=(c,x,fin)=>x==null?"—":(isPct(c)? x.toFixed(3) : (fin? (Math.round(x*10)/10).toFixed(1) : String(Math.round(x))));
    const chip=(l)=>l==="me"?h("span",{class:"chip ok"},"W"):(l==="opp"?h("span",{class:"chip crit"},"L"):h("span",{class:"chip"},"T"));
    const P=W.projected, G=W.games, last=(a)=>a[a.length-1];
    const S=W.to_date_source||{source:"rebuild",reason:null}, yahoo=S.source==="yahoo";
    const SL={fgm:"FGM",fga:"FGA",ftm:"FTM",fta:"FTA",tpm:"3PTM",pts:"PTS",reb:"REB",ast:"AST",stl:"ST",blk:"BLK",tov:"TO"};
    const through=yahoo? "Yahoo's scoreboard at this morning's pull" : (W.to_date_days.length? "box scores through "+last(W.to_date_days) : "no games played yet this week");
    const rebuilt="To date is rebuilt from box scores"+(S.reason?" ("+S.reason+")":" because Yahoo's daily lineups are not in any record")+
      ": every non-IL player who played, at most ten a day, so it can differ from Yahoo's scoreboard. ";
    const srcLine=yahoo? h("p",{class:"note"+(S.rebuild_agrees?"":" zneg")},"To date is Yahoo's scoreboard (read through Flaim at the morning pull); "+
      (S.rebuild_agrees? "the box-score rebuild agrees on all 11 stats." :
        "the box-score rebuild differs: "+(S.differences||[]).map(x=>(x.side==="me"?"you ":"them ")+(SL[x.stat]||x.stat)+" Yahoo "+x.yahoo+", rebuild "+x.rebuild).join("; ")+". Yahoo's figure is the column.")) : null;
    const tbl=h("div",{class:"tablebox"},h("table",{},
      h("tr",{},h("th",{},"cat"),h("th",{class:"num"},"you"),h("th",{class:"num projh"},"proj"),h("th",{class:"num"},"them"),h("th",{class:"num projh"},"proj"),h("th",{},""),h("th",{class:"num"},"chance")),
      W.cats.map(r=>h("tr",{},h("td",{},r.cat),
        h("td",{class:"num actual"},fv(r.cat,r.me_to_date,false)),h("td",{class:"num proj"},fv(r.cat,r.me_final,true)),
        h("td",{class:"num actual"},fv(r.cat,r.opp_to_date,false)),h("td",{class:"num proj"},fv(r.cat,r.opp_final,true)),
        h("td",{},chip(r.leader)),h("td",{class:"num"},r.p_win==null?"—":Math.round(r.p_win*100)+"%")))));
    const sat=(g)=>g.remaining_uncapped-g.remaining_started;
    const games="Games left: you "+G.me.remaining_started+" of "+G.me.remaining_uncapped+" scheduled"+(sat(G.me)?" (the daily ten-slot fill sits "+sat(G.me)+")":"")+
      ", them "+G.opp.remaining_started+" of "+G.opp.remaining_uncapped+(sat(G.opp)?" (fill sits "+sat(G.opp)+")":"")+"."+
      (yahoo&&S.yahoo_games_remaining? " Yahoo's own count of games left: you "+S.yahoo_games_remaining.me+", them "+S.yahoo_games_remaining.opp+".":"");
    const poolLine=(PO,n)=>{ if(!PO) return null;
      if(PO.source!=="yahoo") return h("p",{class:"note"},"Pool: every pooled free agent in the kit ("+(PO.reason||"no Yahoo list")+").");
      const nm=(a)=>a.map(x=>x.name+(x.status?" ("+x.status+")":"")).join(", "), parts=["Pool: Yahoo's available-player list ("+PO.listed+" listed, most-owned across Yahoo first); "+n+" scored."];
      if(PO.out.length) parts.push("Out (O or NA): "+nm(PO.out)+".");
      if(PO.unknown_status.length) parts.push("Status letter not tiered by the kit, so not scored: "+nm(PO.unknown_status)+".");
      if(PO.not_projected.length) parts.push("No season-pool line, so not projected: "+nm(PO.not_projected)+".");
      if(PO.skipped.length) parts.push("Skipped: "+PO.skipped.map(x=>x.name+" ("+x.reason+")").join(", ")+".");
      if(PO.kit_pool_not_listed) parts.push(PO.kit_pool_not_listed+" pooled free agents outside Yahoo's list are not scored.");
      return h("p",{class:"note"},parts.join(" ")); };
    const K=W.pickups; let pk;
    if(K.status==="ran"){ const d=K.drop;
      pk=[h("p",{},h("b",{},"Pickup scan. "),d.player+" ("+d.team+") has no games left this week and ranks "+d.value_rank+" of "+d.of+" by board value ("+f2(d.value)+"). Free agents in his place from today, by projected category wins gained ("+K.pool_size+" scored):"),
        K.top.length? h("div",{class:"tablebox"},h("table",{},
          h("tr",{},h("th",{},"add"),h("th",{class:"num"},"games"),h("th",{class:"num"},"starts"),h("th",{class:"num"},"cats"),h("th",{},"flips"),h("th",{class:"num"},"gaps closed"),h("th",{class:"num"},"value")),
          K.top.map(r=>h("tr",{},h("td",{},r.add+" ("+r.team+")"+(r.status?" · "+r.status:"")+(r.missed?" · sat out "+r.missed:"")),
            h("td",{class:"num"},String(r.games_left)),h("td",{class:"num"},String(r.starts)),h("td",{class:"num"},sgn(r.net,1)),
            h("td",{},(r.flips_to_win.length?"+"+r.flips_to_win.join(", "):"")+(r.flips_to_loss.length?" −"+r.flips_to_loss.join(", "):"")||"none"),
            h("td",{class:"num"},f2(r.gap_closed)),h("td",{class:"num"},zv(r.value)))))) : h("div",{class:"zero"},"No free agent changes a projected category."),
        poolLine(K.pool, K.pool_size),
        h("p",{class:"note"},"cats = projected category wins gained (a tie counts half); gaps closed = over the categories you are projected to lose, the share of each gap he closes, summed (1.00 = one whole gap); value = his season board value, the rest-of-season cost of the move. The league allows 4 adds a week. Projections are single estimates: a category won or lost by a hair flips with almost anyone.")];
    } else {
      const nx=(K.next_finish||[]).slice(0,3).map(x=>x.player+" ("+x.team+") after "+x.last_game).join("; ");
      pk=[h("p",{class:"note"},"Pickup scan: none of your lower-valued players has finished his games this week."+(nx?" Next to finish: "+nx+".":""))];
    }
    return h("div",{class:"card wk"},h("h2",{},"Week "+W.week+" categories"),
      h("p",{class:"note"},"You vs "+T(W.opponent.name)+" · to date: "+through+" · ",
        h("span",{class:"proj"},"faded = projected final through "+W.window[1])),
      tbl, srcLine,
      h("p",{},"Projected "+P.wins+"–"+P.losses+"–"+P.ties+" (W–L–T)."+(W.exp_cats!=null?" Expected categories this week: "+W.exp_cats.toFixed(2)+" of 9.":"")+" "+games),
      W.missing_days.length? h("p",{class:"note zneg"},"No box scores on file for "+W.missing_days.join(", ")+(yahoo? ": the rebuild cross-check lacks those days." : ": those days are not in the to-date totals.")):null,
      (W.unpooled_active||[]).length? h("p",{class:"note zneg"},"Not counted (no pool row, so no box-score join or projection): "+W.unpooled_active.join(", ")+"."):null,
      pk, thisWeek(W),
      h("p",{class:"note"},(yahoo?"":rebuilt)+"Projected = each player's season line × his games left × today's availability, ten a day. The card further down, recorded before the week, assumes 3.5 games per player; this one uses the real schedule."));
  } catch(e){
    return h("div",{class:"card wk"},h("h2",{},"Week "+wk+" categories"),h("div",{class:"zero"},"Week categories could not be drawn: "+e.message));
  }
}

// ---- Worth a look (owner 2026-10-22): "if there is a valuable player available in the free agent pull, make this
// notice to me on the 'Today' tab"; drawn only when a free agent passes a bar ----
function faNotice(){ const W=D.week_matchup, N=W&&W.fa_notice; if(!N || (!(N.rows||[]).length && !N.this_week)) return null;
  const tw=N.this_week;
  return h("div",{class:"card"},h("h2",{},"Worth a look"),
    N.rows.length? h("div",{class:"tablebox"},h("table",{},
      h("tr",{},h("th",{},"add"),h("th",{class:"num"},"season gap")),
      N.rows.map(r=>h("tr",{},h("td",{style:"white-space:normal;min-width:9em"},r.add+" ("+r.team+")",h("div",{class:"note"},"for "+r.drop)),
        h("td",{class:"num"},swk(r.gap,2)))))) : null,
    tw? h("p",{},h("b",{},"This week: "),tw.add+(tw.team?" ("+tw.team+")":"")+" for "+tw.drop+", "+swk(tw.d_exp,2)+" expected categories won this week.") : null,
    h("p",{class:"note"},"Season gap = the free agent's season value per game minus that of your weakest non-IL player (listed only at "+
      N.gap.toFixed(1)+" or more, best "+N.rows.length+" shown). This week = the best move in the week card's scan, shown when it adds "+
      N.d_exp.toFixed(2)+" or more expected categories. A notice, not a move: the league allows 4 adds a week."));
}

// ---- the live week tile (owner 2026-10-22): expected categories now and the chance of 5+ of 9, from the week card ----
function liveTile(W, wk){
  if(!W || W.week!==wk || W.exp_cats==null) return h("div",{class:"tile"},h("div",{class:"v"},"—"),h("div",{class:"l"},"week "+wk+" now"),
    h("div",{class:"e"},"no live record this morning"));
  return h("div",{class:"tile"},h("div",{class:"v"},W.exp_cats.toFixed(2)),h("div",{class:"l"},"week "+W.week+" now: expected categories of 9"),
    h("div",{class:"e"},(W.p_5plus!=null?"5+ of 9: "+pct(W.p_5plus)+" (categories taken as independent) · ":"")+"from this morning's week card"));
}

// ---- the matchup board (owner 2026-10-23: "take this inspiration [Yahoo's matchup page] ... make this the today page";
// week_matchup.py's board block: Yahoo's totals, the categories each side leads to date, every player by today's slot) ----
function matchupBoard(){ const W=D.week_matchup, B=W&&W.board; if(!B) return null;
  const SLOTS=["PG","SG","G","SF","PF","F","C","UTIL","BN","IL","IL+"];
  const CAT=[["FG%","fgm","fga"],["FT%","ftm","fta"],["3PTM","tpm"],["PTS","pts"],["REB","reb"],["AST","ast"],["ST","stl"],["BLK","blk"],["TO","tov"]];
  const pv=(m,a)=>a? (m/a).toFixed(3).replace(/^0/,"") : "–";
  const vals=(t)=>CAT.map(([c,m,a])=>t==null? "–" : (a? pv(t[m],t[a]) : String(t[m])));
  const lead={}; (W.cats||[]).forEach(r=>lead[r.cat]=r.leader_to_date);
  const side=(k)=>B[k], me=side("me"), op=side("opp");
  const head=h("div",{class:"mb-head"},
    h("div",{class:"mb-team"},h("div",{class:"mb-name"},me.name),h("div",{class:"mb-mgr"},(me.manager&&me.manager!=="Me"?me.manager+" · ":"")+"you")),
    h("div",{class:"mb-score"},h("b",{},String(B.score.me)),h("span",{},"vs"),h("b",{},String(B.score.opp))),
    h("div",{class:"mb-team r"},h("div",{class:"mb-name"},op.name),h("div",{class:"mb-mgr"},op.manager||"")));
  const catRow=(k,s)=>h("tr",{},h("td",{},s.name),
    vals(s.totals).map((v,i)=>h("td",lead[CAT[i][0]]===k?{class:"num lead","data-cat":CAT[i][0],"data-side":k}:{class:"num"},v)),
    h("td",{class:"num"},h("b",{},String(B.score[k]))));
  const cats=h("div",{class:"tablebox"},h("table",{class:"mb-cats"},
    h("tr",{},h("th",{},"Team"),CAT.map(([c])=>h("th",{class:"num"},c)),h("th",{class:"num"},"Score")),
    catRow("me",me), catRow("opp",op)));
  const slotName=(x)=>x==="UTIL"?"Util":x;
  const plCell=(r)=> r? h("td",{class:"mb-pl"},h("b",{},r.player),statusChip(r.status),
      h("small",{},(r.team||"")+(r.positions&&r.positions.length?" · "+r.positions.join(","):"")),
      h("small",{},r.today||"No game")) : h("td",{class:"mb-pl mb-empty"},"Empty");
  const statCells=(r)=>vals(r&&r.to_date).map(v=>h("td",{class:"num"+(v==="–"?" dash":"")},v));
  const by=(s)=>{ const m={}; s.rows.forEach(r=>{ const k=(r.slot||"").toUpperCase(); (m[k]=m[k]||[]).push(r); }); return m; };
  const A=by(me), O=by(op), order=SLOTS.concat(Object.keys(A).concat(Object.keys(O)).filter(k=>SLOTS.indexOf(k)<0));
  const rows=[];
  order.forEach(k=>{ const n=Math.max((A[k]||[]).length,(O[k]||[]).length);
    for(let i=0;i<n;i++){ const a=(A[k]||[])[i], o=(O[k]||[])[i];
      rows.push(h("tr",{},plCell(a),statCells(a),h("td",{class:"slot"},slotName(k)),plCell(o),statCells(o))); } });
  const total=h("tr",{class:"mb-total"},h("td",{},"TOTAL"),vals(me.totals).map(v=>h("td",{class:"num"},v)),h("td",{class:"mid"},""),
    h("td",{},"TOTAL"),vals(op.totals).map(v=>h("td",{class:"num"},v)));
  const hdr=h("tr",{},h("th",{},me.name),CAT.map(([c])=>h("th",{class:"num"},c)),h("th",{class:"slot"},"Pos"),h("th",{},op.name),CAT.map(([c])=>h("th",{class:"num"},c)));
  const players=h("div",{class:"tablebox"},h("table",{class:"mb-players"},hdr,rows,total));
  const STAT=["fgm","fga","ftm","fta","tpm","pts","reb","ast","stl","blk","tov"], SL={fgm:"FGM",fga:"FGA",ftm:"FTM",fta:"FTA",tpm:"3PTM",pts:"PTS",reb:"REB",ast:"AST",stl:"ST",blk:"BLK",tov:"TO"};
  const diffNote=(s)=>{ if(s.rows_match_totals) return null;
    const sum={}; STAT.forEach(k=>{ sum[k]=s.rows.reduce((a,r)=>a+((r.to_date||{})[k]||0),0)+((s.departed||{}).to_date||{})[k]||0; });
    const d=STAT.filter(k=>sum[k]!==s.totals[k]).map(k=>SL[k]+" Yahoo "+s.totals[k]+", rows "+sum[k]);
    return h("p",{class:"note zneg"},s.name+": Yahoo's totals differ from the sum of the player rows ("+d.join("; ")+"). The rows are rebuilt from box scores; a day with no Yahoo lineup on file is read from this morning's roster, so a player dropped since, or a game Yahoo counted from a different slot, is not on the rows."); };
  const gone=(s)=>(s.departed&&s.departed.names.length)? h("p",{class:"note"},s.name+": counted this week but no longer on the roster: "+s.departed.names.join(", ")+".") : null;
  const S=W.to_date_source||{};
  return h("div",{class:"card",id:"mboard"},h("h2",{},"Week "+W.week+" matchup"),
    h("p",{class:"note"},W.window[0]+" to "+W.window[1]+" · totals "+(S.source==="yahoo"?"from Yahoo's scoreboard at the morning pull":"rebuilt from box scores")+
      " · player rows rebuilt from box scores through "+((W.to_date_days||[]).slice(-1)[0]||"—")+" · rosters and slots as of "+(W.league_state_as_of||D.league.as_of)),
    head, cats, players, diffNote(me), diffNote(op), gone(me), gone(op),
    h("p",{class:"note"},"Score = categories each side leads to date. A dash: no game counted in an active slot this week. Today's game has no tip-off time: the kit's schedule file carries dates only."));
}

// ---- Today ----
(function(){ const b=D.brief, p=$("#pane-today");
  $("#hdate").textContent=D.date;
  $("#hsub").textContent=T(D.my_team)+" · week "+b.week+" vs "+T(b.opponent)+" · lines "+b.lines+" · rosters as-of "+D.league.as_of;
  const runs="avg of 2 runs × "+b.seasons.toLocaleString()+" seasons", BS=D.matchup.by_seed;
  const tiles=h("div",{class:"tiles"},
    // owner 2026-10-22 ("Live + pre-week"): the ledger's figure is frozen before the week (so it can be graded) and is
    // labelled so; the live tile beside it reads this morning's week card
    h("div",{class:"tile"},h("div",{class:"v"},pct(BS?avg2(Object.values(BS).map(x=>x.p_win)):null)),
      h("div",{class:"l"},"week "+b.week+" pre-week forecast"),
      h("div",{class:"e"},BS?(D.matchup.recorded_at?"recorded "+D.matchup.recorded_at.slice(0,10)+" · ":"recorded before the week · ")+"avg of 2 runs":"")),
    liveTile(D.week_matchup, b.week),
    h("div",{class:"tile"},h("div",{class:"v"},f1(avg2(Object.values(b.title)))+"%"),h("div",{class:"l"},"title odds"),h("div",{class:"e"},runs)),
    h("div",{class:"tile"},h("div",{class:"v"},f1(avg2(Object.values(b.playoffs)))+"%"),h("div",{class:"l"},"playoffs"),h("div",{class:"e"},runs)));
  const catRows = BS? Object.keys(Object.values(BS)[0].cat_p).map(c=>[c, avg2(Object.values(BS).map(x=>x.cat_p[c]))]) : [];
  const catTbl = catRows.length? h("div",{class:"tablebox"},h("table",{},
      h("tr",{},h("th",{},"category"),h("th",{class:"num"},"P(win cat)"),h("th",{},"")),
      catRows.map(([c,v])=>h("tr",{},h("td",{},c),h("td",{class:"num"},pct(v)),
        h("td",{},h("span",{class:"bar "+(v>=0.5?"pos":"neg")},h("i",{style:"width:"+Math.round(Math.abs(v-0.5)*160)+"px"}))))))) : h("div",{class:"zero"},"No matchup record yet.");
  const mb=matchupBoard(); if(mb) p.append(mb);
  const fn=faNotice(); if(fn) p.append(fn);
  p.append(weekCard());
  p.append(
    h("div",{class:"cols"},
      h("div",{class:"card span2"},h("h2",{},"Odds"),tiles,h("p",{class:"note"},"Structural band (standing sweep): "+bandLine())),
      h("div",{class:"card"},h("h2",{},"Lineup"),h("div",{class:"tablebox"},h("table",{},
        b.lineup.map(([slot,name])=>h("tr",{},h("td",{},h("span",{class:"chip"},slot)),h("td",{},name))))),
        b.bench.length?h("p",{class:"note"},"Bench: "+b.bench.join(", ")):null),
      h("div",{class:"card"},h("h2",{},"Today's games"),
        b.today.length? h("div",{class:"tablebox"},h("table",{},
          h("tr",{},h("th",{},"player"),h("th",{},"game"),h("th",{},"status"),h("th",{class:"num"},"avail"),h("th",{class:"num"},"left/wk")),
          b.today.map(([pl,tm,g,st,av,left])=>h("tr",{},h("td",{},pl+" ("+tm+")"),h("td",{},g),h("td",{},statusChip(st)||"—"),h("td",{class:"num"},f2(av)),h("td",{class:"num"},String(left)))))) : h("div",{class:"zero"},"No games today."),
        ),
      h("div",{class:"card span2"},h("h2",{},"Week "+b.week+" categories (recorded before the week)"),catTbl)));
})();

// ---- Trade Analyzer + Free-Agent Adder (owner 2026-10-19: two tabs; z screen, stated defaults D-SD-1) ----
const BOARD=D.board.board, BYNAME={}; BOARD.forEach(r=>BYNAME[r.name]=r);
const MINE=BOARD.filter(r=>r.mine);
function howItWorks(){ return h("div",{class:"card"},h("h2",{},"How this screen works"),
  h("p",{class:"note"},"Per-category z-scores come from today's board (the same vectors the rankings sum; the turnover column already credits low turnovers). Gains are the incoming players' z minus the outgoing players' z, tiered low (<"+C.tier_low+"), medium (<"+C.tier_high+"), high (≥"+C.tier_high+"). The verdict is the net z against ±"+C.verdict_edge+" (strong at ±"+C.verdict_strong+") — "+C.thresholds_note+". For the 10,000-season title-odds verdict on a specific move, ask Claude in session.")); }
function keepTyping(inp, rerender){ const had=document.activeElement===inp, a=inp.selectionStart, b=inp.selectionEnd; rerender();
  if(had){ inp.focus(); try{ inp.setSelectionRange(a,b); }catch(e){} } }
/* Build strip (owner 2026-10-20): each team's per-category z totals over its ACTIVE on-board roster (IL counts 0,
   owner rule D-IS-8); your rank = 1 + teams strictly higher. A picked move re-totals the rosters it touches. */
function activeNames(team, delta){ const R=D.league.rosters[team]||{players:[],il:[]}; const il=new Set(R.il||[]);
  let ns=R.players.filter(n=>!il.has(n));
  if(delta){ ns=ns.filter(n=>!delta.out.has(n)); delta.inc.forEach(n=>{ if(ns.indexOf(n)<0) ns.push(n); }); }
  return ns; }
function catTotals(names){ const t={}; CATS.forEach(c=>t[c]=0);
  names.forEach(n=>{ const r=BYNAME[n]; if(r) CATS.forEach(c=>{ t[c]+=r.z[c]; }); }); return t; }
function leagueRanks(deltas){ const teams=Object.keys(D.league.rosters); const tot={};
  teams.forEach(t=>{ tot[t]=catTotals(activeNames(t, deltas&&deltas[t])); });
  const mine=tot[D.my_team], ranks={};
  CATS.forEach(c=>{ ranks[c]=1; teams.forEach(t=>{ if(t!==D.my_team && tot[t][c]>mine[c]) ranks[c]++; }); });
  return ranks; }
const RANKS0=leagueRanks(null), NTEAMS=Object.keys(D.league.rosters).length;
function buildStrip(id, deltas, active){ const after=active? leagueRanks(deltas) : null;
  return h("div",{id:id},h("h2",{},"Your build — rank 1–"+NTEAMS+" vs the league"),
    h("div",{class:"build"},CATS.map(c=>{ const b=RANKS0[c], a=after? after[c] : null, moved=(a!==null&&a!==b);
      /* owner 2026-10-20: heat by rank — blue excellent, grey mid-pack, red worst (Draft Deck's grading);
         colored by the after-rank when a move is picked */
      const shown=(a===null? b : a), mid=(NTEAMS+1)/2, hi=Math.round(Math.abs(mid-shown)/(mid-1)*45);
      return h("span",{class:"bchip"+(moved?(a<b?" up":" down"):""),
        style:"background:color-mix(in srgb, var(--"+(shown<mid?"pos":"neg")+") "+hi+"%, var(--chip))",
        title:c+": rank "+shown+" of "+NTEAMS+(moved?" (was "+b+")":"")},
        h("span",{class:"bn"},c==="TOV"?"TO↑":c),
        h("span",{class:"br"},moved? b+"→"+a : String(a===null?b:a))); })),
    h("p",{class:"note"},(active? "Before → after the picked move; summed board z per category, ranked against the other "+(NTEAMS-1)+" teams. "
      : "Current build; picking a move shows before → after. ")
      +"IL players count 0 (owner rule D-IS-8) · z screen only — not the simulator."));
}
// owner 2026-10-20 (Strus on IL "not showing up"): my rostered players held off the board, named under my list
function myHeld(){ const ob=(D.league.rosters[D.my_team]||{}).off_board||[];
  return ob.length? h("p",{class:"note"},"You also roster, off the board (held, no z line): "+ob.join(", ")) : null; }
function myField(){ return h("div",{class:"field static",title:T(D.my_team)},T(D.my_team)+" · "+MINE.length+" on the board"); }
function pickList(rows, set, rerender, empty, extra){ return h("div",{class:"plist"}, rows.length? rows.map(r=>h("label",{},
  h("input",{type:"checkbox",...(set.has(r.name)?{checked:""}:{}),onchange:(e)=>{e.target.checked?set.add(r.name):set.delete(r.name);rerender();}}),
  r.name+" · "+r.pos+" · "+r.team+" · z ",zv(r.z_adj),extra?extra(r):null)) : h("div",{class:"zero"},empty)); }
function scoreBlock(inRows, outRows, noun){ noun=noun||"SCREEN";
  if(!(inRows.length||outRows.length)) return h("p",{class:"zero"},"Pick players on both sides to score a move.");
  const m=swapMath(inRows,outRows,CATS);
  return h("div",{},
    h("div",{class:"tablebox"},h("table",{},
      h("tr",{},h("th",{},"category"),h("th",{class:"num"},"Δz"),h("th",{},"size"),h("th",{},"")),
      CATS.map(c=>h("tr",{},h("td",{},c),h("td",{class:"num"},zv(m.d[c],true)),h("td",{},tier(m.d[c],C.tier_low,C.tier_high)),
        h("td",{},h("span",{class:"bar "+(m.d[c]>=0?"pos":"neg")},h("i",{style:"width:"+Math.min(120,Math.round(Math.abs(m.d[c])*40))+"px"}))))))),
    h("p",{},h("span",{class:"verdict "+(m.net>=C.verdict_edge?"pos":(m.net<=-C.verdict_edge?"neg":"even"))},
      (m.net>=C.verdict_strong?"STRONG FAVORABLE "+noun:m.net>=C.verdict_edge?"FAVORABLE "+noun:m.net<=-C.verdict_strong?"STRONG UNFAVORABLE "+noun:m.net<=-C.verdict_edge?"UNFAVORABLE "+noun:"ABOUT EVEN")),
      " ",h("span",{class:"note"},"net Δz ",zv(m.net,true)," · in "+inRows.length+" / out "+outRows.length+" · z screen only — not the simulator")),
    (inRows.length!==outRows.length)? h("p",{class:"note"},"Unequal player counts: the net also prices the empty or extra roster spot at z 0; judge accordingly."):null);
}
(function(){ const p=$("#pane-trade"); const teams=Object.keys(D.league.rosters).filter(t=>t!==D.my_team).sort();
  let team=teams[0]; const out=new Set(), inc=new Set(); const root=h("div",{class:"card"}); p.append(root, howItWorks());
  function render(){ const R=D.league.rosters[team]||{players:[],off_board:[]};
    const theirs=R.players.map(n=>BYNAME[n]).filter(Boolean).sort((a,b)=>a.rank-b.rank);
    inc.forEach(n=>{ if(!R.players.includes(n)) inc.delete(n); });
    root.replaceChildren(
      h("div",{class:"h2row"},h("h2",{},"Trade Analyzer"),
        h("button",{id:"tr-reset",class:"resetbtn",onclick:()=>{out.clear();inc.clear();render();}},"Reset")),
      h("div",{class:"pick"},
        h("div",{},h("h2",{},"I send"),myField(),pickList(MINE,out,render,"No players of yours on the board."),myHeld()),
        h("div",{},h("h2",{},"I receive"),
          h("select",{id:"tr-team",class:"field",onchange:(e)=>{team=e.target.value;inc.clear();render();}},teams.map(t=>h("option",{value:t,...(t===team?{selected:""}:{})},T(t)))),
          pickList(theirs,inc,render,"No board rows on this roster."))),
      ...(R.off_board.length? [h("p",{class:"note"},T(team)+" also rosters, off the board (held, no z line): "+R.off_board.join(", "))] : []),
      buildStrip("tr-build",{[D.my_team]:{out:out,inc:inc},[team]:{out:inc,inc:out}},inc.size||out.size),
      scoreBlock([...inc].map(n=>BYNAME[n]),[...out].map(n=>BYNAME[n]),"TRADE"));
  }
  render();
})();
(function(){ const p=$("#pane-fa"); let search=""; const drop=new Set(), add=new Set(); const root=h("div",{class:"card"}); p.append(root, howItWorks());
  const nfa=BOARD.filter(r=>r.fa).length;
  const inp=h("input",{type:"search",id:"fa-search",class:"field",placeholder:"Search free agents",oninput:()=>{search=inp.value; keepTyping(inp,render);}});
  // owner 2026-10-22 (P1): this week's matchup value beside z; the sort defaults to it when the morning's scan ran
  const W=D.week_matchup, TWR=((W&&W.pickups&&W.pickups.this_week&&W.pickups.this_week.rows)||[]), TWM={};
  TWR.forEach(r=>{TWM[r.add]=r;});
  const onBoard=new Set(BOARD.filter(r=>r.fa).map(r=>r.name)), offBoard=TWR.filter(r=>!onBoard.has(r.add)).map(r=>r.add);
  let sortBy=TWR.length?"week":"z";
  const sortSel=h("select",{id:"fa-sort",class:"field",onchange:(e)=>{sortBy=e.target.value;render();}},
    h("option",{value:"week",...(sortBy==="week"?{selected:""}:{})},"Sort: this week"+(W?" vs "+W.opponent.name:"")),
    h("option",{value:"z",...(sortBy==="z"?{selected:""}:{})},"Sort: season z"));
  const wk=(r)=>{ const t=TWM[r.name]; return t? h("span",{class:"note"}," · this week "+swk(t.d_exp,2)+" ("+t.games+" g, for "+t.drop+")") : null; };
  function render(){ let pool=BOARD.filter(r=>r.fa && (!search || r.name.toLowerCase().includes(search.toLowerCase())))
      .sort((a,b)=>b.z_adj-a.z_adj);  // owner 2026-10-20: free agents by z, descending
    if(sortBy==="week") pool=pool.sort((a,b)=>{ const x=TWM[a.name], y=TWM[b.name];  // 2026-10-22: scored ones first, by this week
      return (x&&y)? y.d_exp-x.d_exp : x? -1 : y? 1 : 0; });                         // the rest keep their z order (stable sort)
    pool=pool.slice(0,60);
    root.replaceChildren(
      h("div",{class:"h2row"},h("h2",{},"Free-Agent Adder"),
        h("button",{id:"fa-reset",class:"resetbtn",onclick:()=>{drop.clear();add.clear();search="";inp.value="";render();}},"Reset")),
      h("p",{class:"note"},nfa+" unrostered players on today's board, matched to all 12 rosters as of "+D.league.as_of+"."),
      h("div",{class:"pick"},
        h("div",{},h("h2",{},"I drop"),myField(),pickList(MINE,drop,render,"No players of yours on the board."),myHeld()),
        h("div",{},h("h2",{},"I add"),
          inp, sortSel,
          TWR.length? h("p",{class:"note"},"This week = the change in expected categories won against "+W.opponent.name+" if you add him from tomorrow in place of the lower-valued player named (Today tab, \"This week's adds\")."+
            (offBoard.length? " Scored this week but not on this board: "+offBoard.join(", ")+".":"")) : null,
          pickList(pool,add,render,"No free agents match.",wk))),
      buildStrip("fa-build",{[D.my_team]:{out:drop,inc:add}},add.size||drop.size),
      scoreBlock([...add].map(n=>BYNAME[n]),[...drop].map(n=>BYNAME[n])));
  }
  render();
})();

// ---- Board ----
(function(){ const p=$("#pane-board"); const rows=D.board.board.slice();
  let key="rank", asc=true, q="", fa=false;
  let ca=null, cb=null;
  const box=h("div",{class:"card"}), cmp=h("div",{class:"card"});
  p.append(box,cmp);
  // owner 2026-10-20: the search box and filter are built once (rebuilding them on each keystroke dropped focus);
  // render() replaces only the table holder
  const inp=h("input",{type:"search",id:"bd-q",placeholder:"Search player or team",oninput:(e)=>{q=e.target.value;render();}});
  const faBox=h("input",{type:"checkbox",id:"bd-fa",onchange:(e)=>{fa=e.target.checked;render();}});
  const tbl=h("div",{});
  box.append(h("div",{class:"h2row"},h("h2",{},"Season board — "+rows.length+" ranked players"),
      h("button",{id:"bd-reset",class:"resetbtn",onclick:()=>{q="";inp.value="";fa=false;faBox.checked=false;key="rank";asc=true;ca=null;cb=null;render();}},"Reset")),
    h("p",{class:"note"},"Blended season lines ("+D.season_lines.players_with_games+" players with regular-season games so far). Held off the board: "+(D.board.held.length?D.board.held.join(", "):"none")+"."),
    h("div",{class:"pick"},inp,h("label",{style:"display:flex;align-items:center;gap:6px"},faBox,"free agents only")),
    tbl);
  function cmpRender(){ const a=ca&&rows.find(r=>r.name===ca), b=cb&&rows.find(r=>r.name===cb);
    const sel=(id,val,on)=>h("select",{id:id,onchange:(e)=>on(e.target.value)},h("option",{value:""},"pick a player"),
      rows.map(r=>h("option",{value:r.name,...(r.name===val?{selected:""}:{})},r.rank+". "+r.name)));
    cmp.replaceChildren(h("h2",{},"Compare"),
      h("div",{class:"pick"},h("div",{},sel("cmp-a",ca,v=>{ca=v;cmpRender();})),h("div",{},sel("cmp-b",cb,v=>{cb=v;cmpRender();}))),
      (a&&b)? h("div",{},
        h("p",{class:"note"},a.name+" (z ",zv(a.z_adj),", left bars) vs "+b.name+" (z ",zv(b.z_adj),", right bars)"),
        h("div",{class:"cmp"},CATS.map(c=>[
          h("div",{class:"cl"},h("i",{style:"width:"+Math.min(110,Math.round(Math.max(0,a.z[c]+2)*22))+"px"}),h("b",{style:"font-size:11px;margin-left:4px"},zv(a.z[c]))),
          h("div",{class:"cc"},c),
          h("div",{class:"cr"},h("b",{style:"font-size:11px;margin-right:4px"},zv(b.z[c])),h("i",{style:"width:"+Math.min(110,Math.round(Math.max(0,b.z[c]+2)*22))+"px"}))]).flat())
      ) : h("p",{class:"zero"},"Pick two players."));
  }
  function render(){ let rs=rows.filter(r=>(!q||r.name.toLowerCase().includes(q.toLowerCase())||(r.owner||"FA").toLowerCase().includes(q.toLowerCase()))&&(!fa||r.fa));
    rs.sort((x,y)=>{ const a=key==="name"?x.name:(key==="owner"?(x.owner||"zzFA"):(key in x? x[key] : x.z[key])); const b=key==="name"?y.name:(key==="owner"?(y.owner||"zzFA"):(key in y? y[key] : y.z[key]));
      return (a<b?-1:a>b?1:0)*(asc?1:-1); });
    const hd=(label,k,num)=>h("th",{class:"sort"+(num?" num":""),onclick:()=>{asc=(key===k)?!asc:(k==="rank"||k==="name"||k==="owner"); key=k; render();}},label+(key===k?(asc?" ↑":" ↓"):""));
    tbl.replaceChildren(h("div",{},  // h() skips the null note; replaceChildren alone would print "null"
      h("div",{class:"tablebox"},h("table",{},
        h("tr",{},hd("#","rank",true),hd("player","name"),h("th",{},"pos"),hd("owner","owner"),hd("z adj","z_adj",true),CATS.map(c=>hd(c,c,true))),
        rs.slice(0,200).map(r=>h("tr",{},h("td",{class:"num"},String(r.rank)),h("td",{},r.name+" · "+r.team),h("td",{},r.pos),
          h("td",{},ownChip(r)),h("td",{class:"num"},zv(r.z_adj)),CATS.map(c=>h("td",{class:"num"},zv(r.z[c]))))))),
      rs.length>200?h("p",{class:"note"},"Showing the first 200 of "+rs.length+" rows; narrow with search."):null));
    cmpRender();
  }
  render();
})();

// ---- Movers ----
(function(){ const p=$("#pane-movers"); const L=D.season_lines;
  // season_lines.py records each moved stat as [preseason, season] per-game strings under its kit column (owner
  // 2026-10-21, decision A: shown as "PTS 25.6 → 24.5"; formatting the pair as a number threw and took the tab bar down)
  const ML={fgp:"FG%",ftp:"FT%",fga:"FGA",fta:"FTA",tpm:"3PM",pts:"PTS",reb:"REB",ast:"AST",stl:"STL",blk:"BLK",tov:"TOV"};
  const mv=(c,v)=>(ML[c]||c)+" "+(Array.isArray(v)?v[0]+" → "+v[1]:String(v));
  p.append(h("div",{class:"card"},h("h2",{},"Season-line movers (per-game line moved "+L.threshold+"+; FG%/FT% 0.01+)"),
    h("p",{class:"note"},L.players_with_games+" pool players with regular-season games; each category's season line = the preseason line carried as a per-category prior (games: "+CATS.map(c=>{const k=(c==="TOV"?"TO":(c==="STL"?"STL":c)); return k+" "+(L.prior_games[k]!=null?L.prior_games[k]:"—");}).join(", ")+") blended with what the games show."),
    L.movers.length? h("div",{class:"tablebox"},h("table",{},
      h("tr",{},h("th",{},"player"),h("th",{class:"num"},"games"),h("th",{},"moved")),
      L.movers.map(m=>h("tr",{},h("td",{},m.name),h("td",{class:"num"},String(m.games)),
        h("td",{},Object.entries(m.moved).map(([c,v])=>h("span",{class:"chip",style:"margin-right:4px"},mv(c,v))))))))
      : h("div",{class:"zero"},"No movers yet — the first regular-season games land 2026-10-21."),
    L.unpooled_with_games.length? h("p",{class:"note"},"Unpooled with games: "+L.unpooled_with_games.join(", ")):null));
})();

// ---- Week / ledger ----
(function(){ const p=$("#pane-week"); const b=D.brief; const weeks=Object.values(D.ledger).sort((a,z)=>a.week-z.week);
  // owner 2026-10-20 item 2: neutral live-matchup facts from the FantasyBot pin; p(win) stays OURS
  // (the ledger's simulator record) — FantasyBot's verdict never renders (owner rule)
  if(D.matchup_live){ const L=D.matchup_live, BS2=(D.matchup&&D.matchup.by_seed)?Object.values(D.matchup.by_seed):[];
    const pw2=BS2.length?avg2(BS2.map(x=>x.p_win)):null;
    p.append(h("div",{class:"card"},h("h2",{},"This week — live"),
      h("div",{class:"tiles"},
        h("div",{class:"tile"},h("div",{class:"v"},String(L.my_left_to_play)),h("div",{class:"l"},"my player-games left")),
        h("div",{class:"tile"},h("div",{class:"v"},String(L.opp_left_to_play)),h("div",{class:"l"},(L.opp_team||"opponent")+" left")),
        pw2!=null?h("div",{class:"tile"},h("div",{class:"v"},pct(pw2)),h("div",{class:"l"},"P(win week) — pre-week forecast")):null),
      h("p",{class:"note"},"Counts from the FantasyBot matchup pull ("+L.date+(L.games_in_progress?", games in progress":"")+"); the win probability is the kit's own record, not FantasyBot's.")));
  }
  // owner 2026-10-20 (option a): show each opponent's CURRENT team name by seat; the ledger record stays frozen
  const seatName={}; for(const r of D.board.board){ if(r.seat!=null) seatName[r.seat]=r.owner; }
  p.append(h("div",{class:"card"},h("h2",{},"Week "+b.week+" — "+(b.week_window?b.week_window.join(" to "):"")),
    h("p",{class:"note"},"Each week's prediction is recorded before the week starts and never rewritten; results land when you paste the scoreboard."),
    weeks.length? h("div",{class:"tablebox"},h("table",{},
      h("tr",{},h("th",{class:"num"},"wk"),h("th",{},"opponent"),h("th",{class:"num"},"P(win)"),h("th",{class:"num"},"exp cats"),h("th",{},"recorded on rosters"),h("th",{},"result")),
      weeks.map(w=>{ const sd=Object.values(w.by_seed||{}); const pw=sd.length?avg2(sd.map(x=>x.p_win)):null, ec=sd.length?avg2(sd.map(x=>x.exp_cats)):null;
        const oname=seatName[w.opponent_seat]||w.opponent_team;
        return h("tr",{},h("td",{class:"num"},String(w.week)),h("td",{},oname+" ("+(w.opponent_manager||"?")+")"),
          h("td",{class:"num"},pct(pw)),h("td",{class:"num"},f2(ec)),h("td",{},w.rosters_as_of||"—"),h("td",{},w.result||"pending"));})))
      : h("div",{class:"zero"},"No weeks recorded yet.")));
})();

// ---- tabs, footer ----
(function(){ const defs=[["today","Today"],["trade","Trade Analyzer"],["fa","Free Agents"],["board","Board"],["movers","Movers"],["week","Week"]];
  const tabs=$("#tabs"); let cur="today";
  try{ const s=localStorage.getItem("deck-tab"); if(s&&defs.some(d=>d[0]===s)) cur=s; }catch(e){}
  const hash=(location.hash||"").replace("#",""); if(defs.some(d=>d[0]===hash)) cur=hash;
  function show(id){ cur=id;
    for(const [k] of defs){ document.getElementById("pane-"+k).hidden = k!==id; }
    [...tabs.children].forEach((b,i)=>b.setAttribute("aria-selected",String(defs[i][0]===id)));
    try{ localStorage.setItem("deck-tab",id); }catch(e){}
  }
  for(const [id,label] of defs) tabs.append(h("button",{role:"tab","aria-selected":"false",onclick:()=>show(id)},label));
  show(cur);
  $("#foot").textContent="Built "+D.generated_utc+" from the morning records — lines "+D.brief.lines+", league state as-of "+D.league.as_of+", engine "+(D.band_engine||"?")+". The page proposes; it changes nothing. Record: report/season/deck_record_"+D.date+".json";
})();
</script>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--out", default=os.path.join(KIT, "report", "season"), help="output folder (default report/season)")
    a = ap.parse_args()
    paths = default_paths(a.date)
    try:
        html, data, record = build(paths, a.date)
    except DeckError as e:
        print(f"SEASON DECK: FAIL — {a.date}: {e}"); sys.exit(1)
    outdir = a.out; os.makedirs(outdir, exist_ok=True)
    # owner 2026-10-21, decision B: the page takes its published name only after it drew itself in a headless browser
    # (deck_render_check.py). On 10/21 a page whose script threw was published with no tabs; a page that fails, or
    # that no browser could check, is kept as deck_<date>.failed.html and the step FAILs, leaving nothing to publish.
    import deck_render_check as DRC
    op = os.path.join(outdir, f"deck_{a.date}.html"); tmp = os.path.join(outdir, f"deck_{a.date}.check.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)
    res = DRC.check(tmp)
    if res["status"] != "PASS":
        failed = os.path.join(outdir, f"deck_{a.date}.failed.html"); os.replace(tmp, failed)
        print(f"SEASON DECK: FAIL — {a.date}: render {res['status']}: {'; '.join(res['reasons'])} "
              f"(page kept as deck_{a.date}.failed.html; deck_{a.date}.html not written)")
        sys.exit(1)
    os.replace(tmp, op)
    record["render"] = dict(status="PASS", tabs=res["tabs"], page_errors=0, browser=res["browser"])
    rp = os.path.join(outdir, f"deck_record_{a.date}.json"); json.dump(record, open(rp, "w", encoding="utf-8"), indent=1)
    print(f"SEASON DECK: PASS — {a.date}: report/season/deck_{a.date}.html ({record['panes']} panes, {record['board_rows']} board rows, "
          f"{record['status_rows']} status rows; record deck_record_{a.date}.json pins {len(record['inputs'])} inputs; "
          f"render: {len(res['tabs'])} tabs, 0 page errors)")


if __name__ == "__main__":
    main()
