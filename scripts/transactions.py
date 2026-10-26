#!/usr/bin/env python3
"""Morning transactions check (in-season tool; owner 2026-10-20: "KPJ was waived by his team. Please include this in
the daily refresh routine").

Source, measured reachable from this container on 2026-10-20: ESPN's public NBA transactions feed (structured JSON,
newest first; 423 items for 2026-27 that day). For a date, every transaction dated in the window ending on that date
(default 3 days, so a missed morning or a weekend is not lost) is read, and each one naming a pool player is listed,
with the fantasy team that rosters him from data/league_state.json (or none: a board player). Names match by the
deck's fold (verify_rosters.norm: accents, punctuation, suffixes) on whole words of the description.

Record and propose only: nothing here changes a line, a tag, a roster or a status tier. An unreachable feed is
recorded as such (ok: false) and the morning goes on; the brief says the feed was not read.

    python3 scripts/transactions.py --date 2026-10-20 [--days 3] [--feed FILE]
Prints 'TRANSACTIONS: PASS — ...' and writes data/news/transactions_<date>.json.
"""
import argparse
import csv
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
DECK = os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball")
sys.path.insert(0, os.path.join(DECK, "scripts"))
sys.path.insert(0, HERE)
from verify_rosters import norm  # noqa: E402
import box_pull  # noqa: E402

FEED = "https://site.web.api.espn.com/apis/site/v2/sports/basketball/nba/transactions?limit=100&page={page}"
STATE = os.path.join(KIT, "data", "league_state.json")
POOL = os.path.join(DECK, "data", "players.csv")
OUTDIR = os.path.join(KIT, "data", "news")
MAX_PAGES = 10


def window(date, days):
    end = datetime.date.fromisoformat(date)
    return (end - datetime.timedelta(days=days - 1)).isoformat(), end.isoformat()


def fetch_feed(start, fetch=box_pull.fetch):
    """Pages of the feed, newest first, until one reaches back past `start`. Returns (items, attempt)."""
    items, pages = [], []
    at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for page in range(1, MAX_PAGES + 1):
        url = FEED.format(page=page)
        text, code, how = fetch(url)
        pages.append({"url": url, "http": code})
        if text is None:
            return items, {"attempted": at, "ok": False, "pages": pages, "detail": how}
        tx = json.loads(text).get("transactions", [])
        items += tx
        if not tx or min(t["date"][:10] for t in tx) < start:
            break
    return items, {"attempted": at, "ok": True, "pages": pages}


def match(items, start, end, pool_names, owners):
    keys = {}
    for n in pool_names:
        k = norm(n)
        if k:
            keys.setdefault(k, n)
    pats = [(re.compile(r"(?<![a-z])" + re.escape(k) + r"(?![a-z])"), n) for k, n in keys.items()]
    hits = []
    for t in items:
        d = t.get("date", "")[:10]
        if not (start <= d <= end):
            continue
        text = norm(t.get("description", ""))
        for pat, n in pats:
            if pat.search(text):
                o = owners.get(n)
                hits.append({"date": d, "nba_team": (t.get("team") or {}).get("abbreviation"), "description": t.get("description"),
                             "player": n, "fantasy_team": o["team"] if o else None, "seat": o["seat"] if o else None})
    hits.sort(key=lambda h: (h["fantasy_team"] is None, h["date"]), reverse=False)
    return hits


def owners_of(state):
    out = {}
    for t in state["teams"]:
        for p in t["players"]:
            out[p["player"]] = {"team": t["name"], "seat": t.get("seat")}
        for n in t.get("unpooled_il", []) + [u["player"] for u in t.get("unpooled") or []]:
            out[n] = {"team": t["name"], "seat": t.get("seat")}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--days", type=int, default=3)
    ap.add_argument("--feed", help="a saved feed page (JSON) in place of the live feed")
    a = ap.parse_args()
    start, end = window(a.date, a.days)
    if a.feed:
        items, attempt = json.load(open(a.feed, encoding="utf-8")).get("transactions", []), {"ok": True, "file": a.feed}
    else:
        items, attempt = fetch_feed(start)
    state = json.load(open(STATE, encoding="utf-8"))
    owners = owners_of(state)
    pool_names = sorted({r["player"] for r in csv.DictReader(open(POOL, encoding="utf-8"))} | set(owners))
    in_window = [t for t in items if start <= t.get("date", "")[:10] <= end]
    hits = match(items, start, end, pool_names, owners)
    rec = {"date": a.date, "window": [start, end], "league_state_as_of": state["as_of"], "source": attempt,
           "items_in_window": len(in_window), "hits": hits}
    os.makedirs(OUTDIR, exist_ok=True)
    out = os.path.join(OUTDIR, f"transactions_{a.date}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False); f.write("\n")
    rostered = [h for h in hits if h["fantasy_team"]]
    feed = f"{len(in_window)} feed item(s) {start} to {end}" if attempt["ok"] else f"feed NOT READ ({attempt.get('detail')})"
    print(f"TRANSACTIONS: PASS — {a.date}: {feed}; {len(hits)} name a pool player, {len(rostered)} rostered"
          + (": " + "; ".join(f"{h['player']} ({h['fantasy_team']}): {h['description']}" for h in rostered) if rostered else "")
          + f"; wrote {os.path.relpath(out, KIT)}")


if __name__ == "__main__":
    main()
