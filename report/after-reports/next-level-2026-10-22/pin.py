#!/usr/bin/env python3
"""Pin the Flaim responses the next-level proposal cites (owner 2026-10-22, GAUNTLET: "research and propose how we can
take the tool to the next level"), extracted mechanically from the session transcript, as flaim_live.extract_pull does:
nothing is retyped. Three read-only calls made at 2026-10-22T16:19Z: get_standings, get_transactions (count 25) and
get_matchups for week 2 (the first week-2 call returned YAHOO_AUTH_UNAVAILABLE, a token refresh in progress; the retry
returned data).

    python3 report/after-reports/next-level-2026-10-22/pin.py --transcript <session transcript> [--since 2026-10-22T16:19:00Z]

Writes flaim_samples.json beside itself: the three data objects, raw.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(KIT, "scripts"))
import flaim_live as FL  # noqa: E402
import league_live as LL  # noqa: E402


def kind(d):
    if "standings" in d and d.get("leagueKey") == FL.LEAGUE_KEY:
        return "standings"
    if "transactions" in d and d.get("league_id") == FL.LEAGUE_KEY:
        return "transactions"
    if "matchups" in d and d.get("leagueKey") == FL.LEAGUE_KEY and d.get("matchupWeek") == 2:
        return "matchups_week2"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", required=True)
    ap.add_argument("--since", default="2026-10-22T16:19:00Z")
    a = ap.parse_args()
    since = LL.since_instant(a.since)
    found = {}

    def walk(x):
        if isinstance(x, str):
            if '"success"' in x and FL.LEAGUE_KEY in x:
                d = FL._data(x)
                if d is not None and kind(d):
                    found[kind(d)] = d
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    with open(a.transcript, encoding="utf-8") as f:
        for ln in f:
            if FL.LEAGUE_KEY not in ln:
                continue
            o = LL._loads(ln)
            if o is not None and LL.recent(o, since):
                walk(o.get("message") if isinstance(o, dict) and "message" in o else o)
    missing = sorted({"standings", "transactions", "matchups_week2"} - set(found))
    assert not missing, f"not in the transcript since {a.since}: {missing}"
    out = os.path.join(HERE, "flaim_samples.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(dict(since=a.since, **found), f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    print(f"PIN: PASS — {', '.join(sorted(found))} pinned to {os.path.relpath(out, KIT)}")


if __name__ == "__main__":
    main()
