#!/usr/bin/env python3
"""Morning box-score pull (in-season tool; Council 2026-10-19 decision 5, owner "proceed").

Sources, measured reachable from this container on 2026-10-19 with a browser user-agent: ESPN's public
scoreboard and summary API (primary, structured JSON) and Basketball-Reference's box-score pages (second
outlet, HTML tables). stats.nba.com does not resolve; NBA.com's pages are JavaScript shells. A date on which
only one outlet has games (preseason is absent from Basketball-Reference) is labelled single_source.

For a date: every FINAL event on ESPN's scoreboard, each summary's box score (per player: minutes, points,
FGM/FGA, 3PM/3PA, FTM/FTA, REB, AST, TOV, STL, BLK, starter, DNP), the same from each Basketball-Reference game
page, the two reconciled player by player (a differing cell is listed, never averaged), names resolved to the
kit's pool by the deck's fold plus the kit alias table, then by the suffix-free key when exactly one pool name
shares it (owner 2026-10-22; a miss is recorded as unpooled with its line kept, never guessed), and one dated JSON
record with the receipts (URLs, fetch times, HTTP codes).

    python3 scripts/box_pull.py --date 2026-10-16 [--out data/actuals/2026-10-16.json] [--cache DIR] [--no-bref]
Prints 'BOX PULL: PASS — ...' (exit 0) when every FINAL ESPN event yielded a box score and the record was written;
'BOX PULL: FAIL' (exit 1) when a fetch failed or an event has no box score, in which case nothing is written.
"""
import argparse
import ast
import datetime
import json
import os
import re
import ssl
import sys
import time
import unicodedata
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
DECK = os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball")
UA = "Mozilla/5.0 (X11; Linux x86_64) fantasy-basketball-kit box_pull"
CA = "/root/.ccr/ca-bundle.crt"
ESPN_SB = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={ymd}"
ESPN_SUM = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={eid}"
BREF_IDX = "https://www.basketball-reference.com/boxscores/?month={m}&day={d}&year={y}"
BREF_GAME = "https://www.basketball-reference.com{path}"
TEAM_CODE = {"CHO": "CHA", "BRK": "BKN", "PHO": "PHX"}  # Basketball-Reference -> pool/Yahoo codes (co_gm.TEAM_CODE)
ESPN_CODE = {"GS": "GSW", "NY": "NYK", "NO": "NOP", "SA": "SAS", "UTAH": "UTA", "WSH": "WAS"}  # ESPN -> pool codes
STATS = ("min", "pts", "fgm", "fga", "tpm", "tpa", "ftm", "fta", "reb", "ast", "tov", "stl", "blk")
ALIAS_FILE = os.path.join(KIT, "report", "market", "build_market.py")
POOL_CSV = os.path.join(KIT, "report", "projections-2026-27.csv")


# ---------------------------------------------------------------- fetching
def fetch(url, cache=None, binary=False, timeout=30):
    """GET with the browser agent through the session proxy; cached by URL when `cache` is a directory."""
    key = re.sub(r"[^A-Za-z0-9._-]+", "_", url)[-150:]
    if cache:
        p = os.path.join(cache, key)
        if os.path.exists(p):
            return open(p, "rb").read() if binary else open(p, encoding="utf-8").read(), 200, "cache"
    ctx = ssl.create_default_context(cafile=CA if os.path.exists(CA) else None)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    raw, code, err = None, 0, ""
    for attempt in range(3):  # a handshake timeout on one page must not sink the morning (seen live 2026-10-19)
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                raw = r.read(); code = r.status
            break
        except urllib.error.HTTPError as e:
            return None, e.code, str(e)
        except (urllib.error.URLError, OSError) as e:
            err = str(e); time.sleep(2 * (attempt + 1))
    if raw is None:
        return None, 0, f"{err} (3 attempts)"
    text = raw if binary else raw.decode("utf-8", "replace")
    if cache:
        os.makedirs(cache, exist_ok=True)
        with open(os.path.join(cache, key), "wb" if binary else "w", **({} if binary else {"encoding": "utf-8"})) as f:
            f.write(text)
    return text, code, "live"


# ---------------------------------------------------------------- ESPN
def espn_events(scoreboard):
    out = []
    for e in scoreboard.get("events", []):
        st = e.get("status", {}).get("type", {})
        out.append(dict(id=e["id"], name=e.get("name"), date=e.get("date"), final=st.get("name") == "STATUS_FINAL",
                        status=st.get("name"), season_type=(e.get("season") or {}).get("type")))
    return out


def _int(s):
    """A box cell to int; ESPN prints '--' for a listed player who did not play."""
    try:
        return int(float(str(s).strip()))
    except (TypeError, ValueError):
        return 0


def _split(s):
    a, b = (str(s).split("-") + ["0"])[:2]
    return _int(a), _int(b)


def parse_espn_summary(summary):
    """Per-player rows from an ESPN summary's boxscore.players (keys: minutes, points, FGM-FGA, 3PM-3PA, FTM-FTA,
    rebounds, assists, turnovers, steals, blocks, ...)."""
    rows = []
    for t in summary["boxscore"]["players"]:
        team = t["team"]["abbreviation"]; team = ESPN_CODE.get(team, team)
        for block in t["statistics"]:
            keys = block["keys"]
            for a in block["athletes"]:
                st = dict(zip(keys, a.get("stats") or []))
                dnp = bool(a.get("didNotPlay")) or not a.get("stats") or _int(st.get("minutes")) == 0 and str(st.get("minutes", "")).strip() in ("", "--", "0")
                mn = 0 if dnp else _int(st.get("minutes"))
                fgm, fga = _split(st.get("fieldGoalsMade-fieldGoalsAttempted", "0-0")) if not dnp else (0, 0)
                tpm, tpa = _split(st.get("threePointFieldGoalsMade-threePointFieldGoalsAttempted", "0-0")) if not dnp else (0, 0)
                ftm, fta = _split(st.get("freeThrowsMade-freeThrowsAttempted", "0-0")) if not dnp else (0, 0)
                g = lambda k: 0 if dnp else _int(st.get(k))
                rows.append(dict(name=a["athlete"]["displayName"], espn_id=str(a["athlete"].get("id")), team=team,
                                 starter=bool(a.get("starter")), dnp=dnp, min=mn, pts=g("points"), fgm=fgm, fga=fga,
                                 tpm=tpm, tpa=tpa, ftm=ftm, fta=fta, reb=g("rebounds"), ast=g("assists"),
                                 tov=g("turnovers"), stl=g("steals"), blk=g("blocks")))
    return rows


# ---------------------------------------------------------------- Basketball-Reference
def pool_team(code):
    return TEAM_CODE.get(code, code)


def bref_game_paths(index_text, date):
    y, m, d = date.split("-")
    return sorted(set(re.findall(rf"/boxscores/{y}{m}{d}0[A-Z]{{3}}\.html", index_text)))


def _cell(row, stat):
    m = re.search(rf'data-stat="{stat}"[^>]*>(.*?)</t[dh]>', row, re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""


def parse_bref_tables(html):
    rows = []
    for m in re.finditer(r'<table[^>]*id="box-([A-Z]{3})-game-basic".*?</table>', html, re.S):
        team = pool_team(m.group(1))
        for tr in re.findall(r"<tr[^>]*>.*?</tr>", m.group(0), re.S):
            if 'data-stat="player"' not in tr or "<th" not in tr.split("</th>")[0]:
                continue
            pid = re.search(r'data-append-csv="([^"]+)"', tr)
            if not pid:
                continue  # header or Team Totals row
            name = _cell(tr, "player")
            mp = _cell(tr, "mp")
            dnp = ":" not in mp
            mn = 0 if dnp else int(mp.split(":")[0]) + (1 if int(mp.split(":")[1]) >= 30 else 0)
            g = lambda k: 0 if dnp else int(_cell(tr, k) or 0)
            rows.append(dict(name=name, bref_id=pid.group(1), team=team, dnp=dnp, min=mn, pts=g("pts"), fgm=g("fg"),
                             fga=g("fga"), tpm=g("fg3"), tpa=g("fg3a"), ftm=g("ft"), fta=g("fta"), reb=g("trb"),
                             ast=g("ast"), tov=g("tov"), stl=g("stl"), blk=g("blk")))
    return rows


# ---------------------------------------------------------------- names, reconciliation, record
def fold(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c) and c not in "'’`.").strip()


def load_aliases(path=ALIAS_FILE):
    """The kit alias table (report/market/build_market.py ALIASES: canonical -> variants), read by AST, never executed."""
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except OSError:
        return {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "ALIASES" for t in node.targets):
            return ast.literal_eval(node.value)
    return {}


def load_pool_names(path=POOL_CSV):
    import csv
    with open(path, encoding="utf-8") as f:
        return [r["name"] for r in csv.DictReader(f)]


def resolve_names(rows, pool_names, aliases):
    index = name_index(pool_names, aliases)
    out = []
    for r in rows:
        r = dict(r); r["pool_name"] = match_name(r["name"], index)
        out.append(r)
    return out


SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v"}


def name_key(name):
    """Folded name with generational suffixes dropped (Robert Williams III -> robert williams)."""
    toks = [t for t in fold(name).split() if t not in SUFFIXES]
    return " ".join(toks)


def name_index(names, aliases=None):
    """The lookup match_name reads: each folded spelling (the alias table's variants folded to their canonical name)
    and each suffix-free key with the names that share it."""
    by = {fold(n): n for n in names}
    for canon, variants in (aliases or {}).items():
        for v in variants:
            by.setdefault(fold(v), canon)
    keyed = {}
    for n in names:
        keyed.setdefault(name_key(n), set()).add(n)
    return by, keyed


def match_name(name, index):
    """The name `name` folds to; failing that, the one name sharing its suffix-free key (owner 2026-10-22: ESPN's
    "Darius Acuff Jr." is the kit's "Darius Acuff"); otherwise None. A key two names share matches neither."""
    by, keyed = index
    hit = by.get(fold(name))
    if hit is None:
        cands = keyed.get(name_key(name), ())
        hit = next(iter(cands)) if len(cands) == 1 else None
    return hit


def _compatible(a, b):
    """Same surname and prefix-compatible first names (Ron / Ronald, Tre / Trevon); Keegan / Kris Murray are not."""
    ta, tb = name_key(a).split(), name_key(b).split()
    if not ta or not tb or ta[-1] != tb[-1]:
        return False
    fa, fb = ta[0], tb[0]
    return fa.startswith(fb) or fb.startswith(fa)


def reconcile(espn_rows, bref_rows):
    """Join on suffix-free folded name + team, then on team + surname + a prefix-compatible first name (the two
    outlets' nickname and suffix habits differ); compare the box cells (minutes to within 1); list every difference."""
    key = lambda r: (name_key(r["name"]), r["team"])
    e = {key(r): r for r in espn_rows}; b = {key(r): r for r in bref_rows}
    pairs = [(k, k) for k in sorted(set(e) & set(b))]
    left_e = sorted(set(e) - set(b)); left_b = sorted(set(b) - set(e))
    for ke in left_e:
        cands = [kb for kb in left_b if kb[1] == ke[1] and _compatible(e[ke]["name"], b[kb]["name"])]
        if len(cands) == 1:
            pairs.append((ke, cands[0])); left_b.remove(cands[0])
    used_e = {p[0] for p in pairs}
    matched, mism = 0, []
    for ke, kb in pairs:
        k = ke
        b_row = b[kb]
        cells = {}
        for s in STATS:
            x, y = e[k][s], b_row[s]
            if (abs(x - y) > 1) if s == "min" else (x != y):
                cells[s] = [x, y]
        if cells:
            mism.append(dict(name=e[k]["name"], team=e[k]["team"], cells=cells))
        else:
            matched += 1
    return dict(matched=matched, mismatched=mism,
                espn_only=[f"{e[k]['name']} ({e[k]['team']})" for k in sorted(set(e) - used_e)],
                bref_only=[f"{b[k]['name']} ({b[k]['team']})" for k in left_b])


def build_record(date, players, games, single_source, sources, reconciliation=None):
    return dict(date=date, fetched_at_utc=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                sources=sources, single_source=single_source, games=games, players=players,
                reconciliation=reconciliation or {}, unpooled=[p["name"] for p in players if p.get("pool_name") is None],
                n_players=len(players), n_pooled=sum(1 for p in players if p.get("pool_name")))


# ---------------------------------------------------------------- main
def pull(date, cache=None, use_bref=True, log=print):
    ymd = date.replace("-", "")
    receipts = {"espn": {"scoreboard": ESPN_SB.format(ymd=ymd), "summaries": [], "fetched_at_utc": None},
                "bref": {"index": None, "pages": [], "fetched_at_utc": None}}
    text, code, how = fetch(ESPN_SB.format(ymd=ymd), cache)
    if text is None:
        return None, [f"ESPN scoreboard HTTP {code}: {how}"]
    receipts["espn"]["fetched_at_utc"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    events = espn_events(json.loads(text)); finals = [e for e in events if e["final"]]
    problems, espn_rows, games = [], [], []
    for e in finals:
        url = ESPN_SUM.format(eid=e["id"]); t2, c2, h2 = fetch(url, cache)
        receipts["espn"]["summaries"].append(dict(event=e["id"], url=url, http=c2, how=h2))
        if t2 is None:
            problems.append(f"ESPN summary {e['id']} HTTP {c2}: {h2}"); continue
        rows = parse_espn_summary(json.loads(t2))
        if not rows:
            problems.append(f"ESPN summary {e['id']} has no box score"); continue
        for r in rows:
            r["game"] = e["id"]
        espn_rows += rows; games.append(dict(espn_id=e["id"], name=e["name"], date=e["date"], season_type=e["season_type"]))
        time.sleep(0.3)
    bref_rows, bref_games = [], []
    if use_bref:
        y, m, d = date.split("-"); idx_url = BREF_IDX.format(m=int(m), d=int(d), y=y)
        receipts["bref"]["index"] = idx_url
        t3, c3, h3 = fetch(idx_url, cache)
        receipts["bref"]["fetched_at_utc"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if t3 is None:
            problems.append(f"Basketball-Reference index HTTP {c3}: {h3}")
        else:
            for path in bref_game_paths(t3, date):
                url = BREF_GAME.format(path=path); t4, c4, h4 = fetch(url, cache)
                receipts["bref"]["pages"].append(dict(path=path, http=c4, how=h4))
                if t4 is None:
                    problems.append(f"Basketball-Reference {path} HTTP {c4}: {h4}"); continue
                rows = parse_bref_tables(t4); bref_rows += rows; bref_games.append(path)
                time.sleep(1.0)  # the site's crawl courtesy; a morning slate is at most 15 pages
    if problems:
        return None, problems
    single = not bref_rows
    rec = reconcile(espn_rows, bref_rows) if bref_rows else {}
    players = resolve_names(espn_rows, load_pool_names(), load_aliases())
    sources = dict(espn=dict(events=len(events), final=len(finals), **receipts["espn"]),
                   bref=dict(games=len(bref_games), **receipts["bref"]))
    return build_record(date, players, games, single, sources, rec), []


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", required=True)
    ap.add_argument("--out")
    ap.add_argument("--cache")
    ap.add_argument("--no-bref", action="store_true")
    a = ap.parse_args()
    rec, problems = pull(a.date, a.cache, not a.no_bref)
    if problems:
        print("BOX PULL: FAIL")
        for p in problems:
            print("  " + p)
        return 1
    out = a.out or os.path.join(KIT, "data", "actuals", f"{a.date}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False); f.write("\n")
    r = rec["reconciliation"]
    print(f"BOX PULL: PASS — {a.date}: {len(rec['games'])} games, {rec['n_players']} player lines, {rec['n_pooled']} in the pool, "
          f"{len(rec['unpooled'])} unpooled; " + ("single-source (ESPN only)" if rec["single_source"] else
          f"two outlets: {r['matched']} matched, {len(r['mismatched'])} cells differ, {len(r['espn_only'])} ESPN-only, {len(r['bref_only'])} bref-only")
          + f"; written {os.path.relpath(out, KIT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
