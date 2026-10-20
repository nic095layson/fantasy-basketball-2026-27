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
Writes report/season/deck_<date>.html and deck_record_<date>.json (sha256 of every input).
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
                calibration=os.path.join(KIT, "report", "calibration.json"))


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
    shock = sweep["constants"]["arena.TEAM_WEEK_SHOCK"]
    band = dict(name="arena.TEAM_WEEK_SHOCK", tier=shock["tier"], engine=sweep.get("engine_commit") or sweep.get("engine"),
                variants=[dict(label=v.get("label"), shift=v.get("shift_mean_1dp", f"{v['shift_mean']:+.1f}"))
                          for v in shock["variants"]])
    if shock["tier"] == "FRAGILE" and not band["variants"]: raise DeckError("FRAGILE band with no variants")
    wk = calib.get("weeks", {}).get(str(brief.get("week"))) or {}
    data = dict(date=date, generated_utc=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                my_team=my_team, my_seat=my_seat, brief=brief, board=board, status=status,
                league=dict(as_of=league["as_of"], rosters=rosters, managers={t["name"]: t.get("manager") for t in league["teams"]}), season_lines=lines, matchup=wk,
                ledger=calib.get("weeks", {}), band=band,
                config=dict(cats=["FG%", "FT%", "3PM", "PTS", "REB", "AST", "STL", "BLK", "TOV"],
                            tier_low=0.3, tier_high=1.0, verdict_edge=0.5, verdict_strong=1.5,
                            thresholds_note="stated defaults, D-SD-1 (owner re-tunes); z screen only, not the simulator"))
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = SHELL.replace("__DATA__", payload)
    record = dict(date=date, out=f"report/season/deck_{date}.html",
                  inputs={k: dict(path=os.path.relpath(p, KIT) if p.startswith(KIT) else p,
                                  sha256=hashlib.sha256(open(p, "rb").read()).hexdigest()) for k, p in paths.items()},
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
  --ok:#2E7D4F; --warn:#B26A00; --crit:#B3261E;
  --disp:"Barlow Condensed","Arial Narrow",system-ui,sans-serif;
  --body:"IBM Plex Sans","Segoe UI",system-ui,sans-serif;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#11161B; --surface:#1A222A; --ink:#E7EAEC; --ink2:#9AA4AD; --line:#2A343D; --chip:#232D36;
  --accent:#D06B2A; --mine:#1E97AD; --pos:#4484C8; --neg:#CE5240; --negtx:#E2735F;
  --ok:#5BB77F; --warn:#D9A04C; --crit:#E07069; color-scheme:dark } }
:root[data-theme="dark"]{
  --bg:#11161B; --surface:#1A222A; --ink:#E7EAEC; --ink2:#9AA4AD; --line:#2A343D; --chip:#232D36;
  --accent:#D06B2A; --mine:#1E97AD; --pos:#4484C8; --neg:#CE5240; --negtx:#E2735F;
  --ok:#5BB77F; --warn:#D9A04C; --crit:#E07069; color-scheme:dark }
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
function bandLine(){ return D.band.name.replace("arena.","")+" is "+D.band.tier+": "+D.band.variants.map(v=>v.shift+" (shock "+v.label+")").join(" / ")+" title points — engine "+(D.band.engine||"?"); }
function T(t){ if(t===D.my_team) return t+" (you)"; const m=(D.league.managers||{})[t]; return m? t+" ("+m+")" : t; }
function ownChip(r){ return r.mine? h("span",{class:"chip mine"},"mine") : r.fa? h("span",{class:"chip fa"},"FA") : h("span",{class:"chip"},T(r.owner)); }
function statusChip(letter){ if(!letter) return null; const cls=letter==="O"?"crit":(letter==="Q"?"warn":"ok"); return h("span",{class:"chip "+cls},letter); }

// ---- Today ----
(function(){ const b=D.brief, p=$("#pane-today");
  $("#hdate").textContent=D.date;
  $("#hsub").textContent=T(D.my_team)+" · week "+b.week+" vs "+T(b.opponent)+" · lines "+b.lines+" · rosters as-of "+D.league.as_of;
  const seeds=Object.keys(b.title);
  const tiles=h("div",{class:"tiles"},
    h("div",{class:"tile"},h("div",{class:"v"},pct((D.matchup.by_seed?D.matchup.by_seed[seeds[0]].p_win:null))),h("div",{class:"l"},"win week "+b.week),h("div",{class:"e"},D.matchup.by_seed?("seed "+seeds[1]+": "+pct(D.matchup.by_seed[seeds[1]].p_win)):"")),
    h("div",{class:"tile"},h("div",{class:"v"},f1(b.title[seeds[0]])+"%"),h("div",{class:"l"},"title odds"),h("div",{class:"e"},"seed "+seeds[1]+": "+f1(b.title[seeds[1]])+"% · "+b.seasons.toLocaleString()+" seasons")),
    h("div",{class:"tile"},h("div",{class:"v"},f1(b.playoffs[seeds[0]])+"%"),h("div",{class:"l"},"playoffs"),h("div",{class:"e"},"seed "+seeds[1]+": "+f1(b.playoffs[seeds[1]])+"%")));
  const catRows = D.matchup.by_seed? Object.entries(D.matchup.by_seed[seeds[0]].cat_p) : [];
  const catTbl = catRows.length? h("div",{class:"tablebox"},h("table",{},
      h("tr",{},h("th",{},"category"),h("th",{class:"num"},"P(win cat)"),h("th",{},"")),
      catRows.map(([c,v])=>h("tr",{},h("td",{},c),h("td",{class:"num"},pct(v)),
        h("td",{},h("span",{class:"bar "+(v>=0.5?"pos":"neg")},h("i",{style:"width:"+Math.round(Math.abs(v-0.5)*160)+"px"}))))))) : h("div",{class:"zero"},"No matchup record yet.");
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
function myField(){ return h("div",{class:"field static",title:T(D.my_team)},T(D.my_team)+" · "+MINE.length+" on the board"); }
function pickList(rows, set, rerender, empty){ return h("div",{class:"plist"}, rows.length? rows.map(r=>h("label",{},
  h("input",{type:"checkbox",...(set.has(r.name)?{checked:""}:{}),onchange:(e)=>{e.target.checked?set.add(r.name):set.delete(r.name);rerender();}}),
  r.name+" · "+r.pos+" · "+r.team+" · z ",zv(r.z_adj))) : h("div",{class:"zero"},empty)); }
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
        h("div",{},h("h2",{},"I send"),myField(),pickList(MINE,out,render,"No players of yours on the board.")),
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
  function render(){ const pool=BOARD.filter(r=>r.fa && (!search || r.name.toLowerCase().includes(search.toLowerCase())))
      .sort((a,b)=>b.z_adj-a.z_adj).slice(0,60);  // owner 2026-10-20: free agents by z, descending
    root.replaceChildren(
      h("div",{class:"h2row"},h("h2",{},"Free-Agent Adder"),
        h("button",{id:"fa-reset",class:"resetbtn",onclick:()=>{drop.clear();add.clear();search="";inp.value="";render();}},"Reset")),
      h("p",{class:"note"},nfa+" unrostered players on today's board, matched to all 12 rosters as of "+D.league.as_of+"."),
      h("div",{class:"pick"},
        h("div",{},h("h2",{},"I drop"),myField(),pickList(MINE,drop,render,"No players of yours on the board.")),
        h("div",{},h("h2",{},"I add"),
          inp,
          pickList(pool,add,render,"No free agents match."))),
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
  p.append(h("div",{class:"card"},h("h2",{},"Season-line movers (±"+L.threshold+" z and over)"),
    h("p",{class:"note"},L.players_with_games+" pool players with regular-season games; each category's season line = the preseason line carried as a per-category prior (games: "+CATS.map(c=>{const k=(c==="TOV"?"TO":(c==="STL"?"STL":c)); return k+" "+(L.prior_games[k]!=null?L.prior_games[k]:"—");}).join(", ")+") blended with what the games show."),
    L.movers.length? h("div",{class:"tablebox"},h("table",{},
      h("tr",{},h("th",{},"player"),h("th",{class:"num"},"games"),h("th",{},"moved")),
      L.movers.map(m=>h("tr",{},h("td",{},m.name),h("td",{class:"num"},String(m.games)),
        h("td",{},Object.entries(m.moved).map(([c,v])=>h("span",{class:"chip",style:"margin-right:4px"},c+" ",zv(v,true))))))))
      : h("div",{class:"zero"},"No movers yet — the first regular-season games land 2026-10-21."),
    L.unpooled_with_games.length? h("p",{class:"note"},"Unpooled with games: "+L.unpooled_with_games.join(", ")):null));
})();

// ---- Week / ledger ----
(function(){ const p=$("#pane-week"); const b=D.brief; const weeks=Object.values(D.ledger).sort((a,z)=>a.week-z.week);
  p.append(h("div",{class:"card"},h("h2",{},"Week "+b.week+" — "+(b.week_window?b.week_window.join(" to "):"")),
    h("p",{class:"note"},"Each week's prediction is recorded before the week starts and never rewritten; results land when you paste the scoreboard."),
    weeks.length? h("div",{class:"tablebox"},h("table",{},
      h("tr",{},h("th",{class:"num"},"wk"),h("th",{},"opponent"),h("th",{class:"num"},"P(win)"),h("th",{class:"num"},"exp cats"),h("th",{},"recorded on rosters"),h("th",{},"result")),
      weeks.map(w=>{ const sd=Object.keys(w.by_seed||{}); const pw=sd.length?w.by_seed[sd[0]].p_win:null, ec=sd.length?w.by_seed[sd[0]].exp_cats:null;
        return h("tr",{},h("td",{class:"num"},String(w.week)),h("td",{},w.opponent_team+" ("+(w.opponent_manager||"?")+")"),
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
  $("#foot").textContent="Built "+D.generated_utc+" from the morning records — lines "+D.brief.lines+", league state as-of "+D.league.as_of+", engine "+(D.band.engine||"?")+". The page proposes; it changes nothing. Record: report/season/deck_record_"+D.date+".json";
})();
</script>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args()
    paths = default_paths(a.date)
    try:
        html, data, record = build(paths, a.date)
    except DeckError as e:
        print(f"SEASON DECK: FAIL — {a.date}: {e}"); sys.exit(1)
    outdir = os.path.join(KIT, "report", "season"); os.makedirs(outdir, exist_ok=True)
    op = os.path.join(outdir, f"deck_{a.date}.html"); open(op, "w", encoding="utf-8").write(html)
    rp = os.path.join(outdir, f"deck_record_{a.date}.json"); json.dump(record, open(rp, "w", encoding="utf-8"), indent=1)
    print(f"SEASON DECK: PASS — {a.date}: report/season/deck_{a.date}.html ({record['panes']} panes, {record['board_rows']} board rows, "
          f"{record['status_rows']} status rows; record deck_record_{a.date}.json pins {len(record['inputs'])} inputs)")


if __name__ == "__main__":
    main()
