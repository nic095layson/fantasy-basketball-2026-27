#!/usr/bin/env python3
"""Fetch the two external market sources and land them raw + dated under report/market/.

This is the *network* half of the market-data work order (report/market-data-workorder.md,
§3 steps 1-2). It writes only raw snapshots; parsing/normalization is build_market.py's
job (deterministic, offline). Keeping fetch and parse separate means the gate can re-run
offline from the committed raw files even after the egress window closes.

Sources (owner-allowlisted 2026-08-21):
  - Hashtag Basketball projections  (server-rendered ASP.NET GridView; ADP + per-game line)
  - StatMaxers / statdunk categories (JS SPA; data via the site's *same-origin* API route
    /api/statdunk-nba-projections. The SPA's own Supabase backend *.supabase.co is NOT on
    the allowlist and returns proxy 403 — the same-origin route is the reachable channel.)

Usage:  python3 report/market/fetch_market.py [YYYY-MM-DD]
Exit 0 = both raw files written. Exit 2 = a source is blocked/unreachable (STOP, per §0 —
never work around a blocked channel).
"""
import sys
import time
import re
from datetime import date

import requests

HERE = __import__("os").path.dirname(__import__("os").path.abspath(__file__))
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

HASHTAG_URL = "https://hashtagbasketball.com/fantasy-basketball-projections"
STATDUNK_REFERER = "https://statdunk.com/projections/categories?sport=nba&sort=val"
# StatMaxers same-origin API routes (the SPA's Supabase backend *.supabase.co is off the
# allowlist -> proxy 403). We land three snapshots:
#   base = the published category-value artifact (has categories/z/rank/value) but it is a
#          stale 'provisional_lock_in' (asOf 8/11) whose player universe is broken (misses
#          most stars). Kept ONLY as the validation anchor for the reconstruction method.
#   v2   = the freshest full-coverage projection release (V4.10, asOf ~today). No category
#          block (that lives in Supabase) -> build_market.py reconstructs it via statdunk's
#          own stated method, validated to reproduce base exactly.
#   v3   = the lock-in projection variant, landed for provenance.
STATDUNK_ENDPOINTS = {
    "base": "https://statdunk.com/api/statdunk-nba-projections",
    "v2": "https://statdunk.com/api/statdunk-nba-projections-v2",
    "v3": "https://statdunk.com/api/statdunk-nba-projections-v3-lock-in",
}

# Hashtag position/ADP source. 1=Yahoo 3=ESPN 2=Fantrax 0=Depth Chart.
# Client plays on Yahoo (INPUTS.md default) — PROMPT.md Pass E prefers the client's platform.
HASHTAG_POS_FROM = "1"      # Yahoo
HASHTAG_SHOW = "900"        # "All" — guarantees every pool player is available to the join
HASHTAG_DURATION = "0"      # 2026-27 Rest of Season Projections


def _get(session, url, **kw):
    """GET/POST with exponential backoff on network errors (2,4,8,16s)."""
    method = kw.pop("method", "get")
    last = None
    for i, delay in enumerate([0, 2, 4, 8, 16]):
        if delay:
            time.sleep(delay)
        try:
            r = getattr(session, method)(url, timeout=60, **kw)
            if r.status_code == 200 and r.text:
                return r
            last = f"HTTP {r.status_code} (len {len(r.text)})"
        except requests.RequestException as e:
            last = f"{type(e).__name__}: {e}"
    raise SystemExit(f"BLOCKED/UNREACHABLE: {url}\n  last error: {last}\n"
                     "  Per work order §0, do not work around a blocked channel — stop.")


def fetch_statdunk(session, url):
    r = _get(session, url, headers={"Accept": "application/json",
                                    "Referer": STATDUNK_REFERER})
    import json
    data = r.json()
    players = data.get("players") or (data.get("release", {}) or {}).get("players") or []
    pub = data.get("publication") or (data.get("release", {}) or {}).get("publication") or {}
    n = len(players)
    if n == 0:
        raise SystemExit("statdunk returned 0 players — refusing to land an empty snapshot")
    print(f"  {url.rsplit('/', 1)[-1]}: {n} players | label={pub.get('label')} "
          f"asOf={pub.get('asOf')} kind={pub.get('artifactKind')}")
    return r.text, n


def _form_fields(html):
    """Extract every ASP.NET form field (hidden inputs + current select values)."""
    form = {}
    for m in re.finditer(r'<input[^>]*name="([^"]+)"[^>]*>', html):
        tag, name = m.group(0), m.group(1)
        tm = re.search(r'type="([^"]*)"', tag)
        typ = (tm.group(1) if tm else "text").lower()
        vm = re.search(r'value="([^"]*)"', tag)
        if typ in ("checkbox", "radio"):
            # Only checked boxes are submitted, and they must carry value "on" — Hashtag's
            # server reads the literal "on" to decide which stat columns to render, so an
            # empty value silently drops every category column (and zeroes TOTAL).
            if "checked" not in tag:
                continue
            form[name] = vm.group(1) if vm else "on"
            continue
        form[name] = vm.group(1) if vm else ""
    for m in re.finditer(r'<select[^>]*name="([^"]+)"[^>]*>(.*?)</select>', html, re.S):
        name, body = m.group(1), m.group(2)
        sel = (re.search(r'<option[^>]*selected[^>]*value="([^"]*)"', body)
               or re.search(r'<option[^>]*value="([^"]*)"[^>]*selected', body))
        if sel:
            form[name] = sel.group(1)
        else:
            f = re.search(r'<option[^>]*value="([^"]*)"', body)
            form[name] = f.group(1) if f else ""
    return form


def fetch_hashtag(session):
    r0 = _get(session, HASHTAG_URL)
    form = _form_fields(r0.text)
    form["ctl00$ContentPlaceHolder1$DDPOSFROM"] = HASHTAG_POS_FROM
    form["ctl00$ContentPlaceHolder1$DDSHOW"] = HASHTAG_SHOW
    form["ctl00$ContentPlaceHolder1$DDDURATION"] = HASHTAG_DURATION
    form["__EVENTTARGET"] = "ctl00$ContentPlaceHolder1$DDSHOW"
    form["__EVENTARGUMENT"] = ""
    r = _get(session, HASHTAG_URL, method="post", data=form,
             headers={"Referer": HASHTAG_URL})
    n = r.text.count("HyperLink1_")  # one full-name anchor per data row
    print(f"  hashtag: ~{n} player rows | POSFROM={HASHTAG_POS_FROM}(Yahoo) "
          f"SHOW={HASHTAG_SHOW} DURATION={HASHTAG_DURATION}(ROS)")
    if n < 200:
        raise SystemExit(f"hashtag returned only {n} rows — expected the full list; refusing")
    return r.text, n


def main():
    import os
    d = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    s = requests.Session()
    s.headers.update({"User-Agent": UA})

    print("fetching statdunk (same-origin API, 3 endpoints)...")
    counts = {}
    for tag, url in STATDUNK_ENDPOINTS.items():
        text, n = fetch_statdunk(s, url)
        suffix = "" if tag == "base" else f"-{tag}"
        path = os.path.join(HERE, f"statdunk{suffix}-raw-{d}.json")
        open(path, "w", encoding="utf-8").write(text)
        counts[tag] = n
        print(f"    wrote {os.path.basename(path)} ({len(text)} bytes)")
    sd_n = counts.get("v2", 0)

    print("fetching hashtag (ASP.NET postback, full list)...")
    ht_text, ht_n = fetch_hashtag(s)
    ht_path = os.path.join(HERE, f"hashtag-raw-{d}.html")
    open(ht_path, "w", encoding="utf-8").write(ht_text)
    print(f"  wrote {ht_path} ({len(ht_text)} bytes)")

    print(f"\nOK — raw snapshots landed for {d}: statdunk={sd_n} hashtag~={ht_n}")


if __name__ == "__main__":
    main()
