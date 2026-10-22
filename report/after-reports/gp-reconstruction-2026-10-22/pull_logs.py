#!/usr/bin/env python3
"""GP reconstruction test: 2025-26 regular-season game logs for every player on the 44 pinned rosters (rosters/).
A rostered name resolves to a Basketball-Reference id through the 2025-26 per-game page (NBA_2026_per_game.html, the
page #159's q_ids.json came from; its sha256 is checked). Players whose logs #159 already pulled
(../zscore-assessment-2026-10-21/gamelogs/gamelogs_2025-26.csv) are reused; the rest are fetched, paced 3.5 s, a
429 or error pausing 60 s and retrying once. A name absent from the per-game page played no 2025-26 game and is
recorded as such (NO_GAMES, with the receipts named there). Raw pages stay outside the repo with their sha256 here.

    python3 pull_logs.py RAW_DIR            fetch what is missing, then parse
    python3 pull_logs.py RAW_DIR --reparse  parse the saved pages again (each sha256 must equal the manifest's)

Writes gamelogs_extra_2025-26.csv (same columns as #159's file) and logs_manifest.json."""
import csv, glob, hashlib, html, json, os, re, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(KIT, "..", "yahoo-fantasy-basketball", "scripts"))
from verify_rosters import norm  # noqa: E402

PRIOR = os.path.join(HERE, "..", "zscore-assessment-2026-10-21", "gamelogs", "gamelogs_2025-26.csv")
PER_GAME_SHA = "923acee39d1c6a257009bd713707c5d61f6394dd232cae2143cf4a515eb98553"
COLS = ["date", "team_name_abbr", "opp_name_abbr", "mp", "fg", "fga", "ft", "fta", "fg3", "pts", "trb", "ast", "stl", "blk", "tov"]
# absent from the 2025-26 per-game page; receipts: the deck's pinned 2025-26 per-game files from two outlets
# (arena/results/actuals_2026-10-09/bref_pergame_2025-26.csv and espn_pergame_2025-26.csv) carry no row for him,
# while the 2022-23, 2023-24 and 2024-25 files of both outlets do
NO_GAMES = {"Kyrie Irving"}


def parse(page):
    """The parser of ../zscore-assessment-2026-10-21/gamelogs/pull_gamelogs.py (that script runs on import, so it is
    carried here; test_reconstruct.py checks the two agree on a page #159 parsed)."""
    m = re.search(r'<table[^>]*id="player_game_log_reg".*?</table>', page, re.S)
    if not m:
        return None
    out = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(0), re.S):
        cells = dict(re.findall(r'data-stat="([a-z_0-9]+)"[^>]*>(.*?)</t[dh]>', tr, re.S))
        cells = {k: html.unescape(re.sub(r"<[^>]+>", "", v)).strip() for k, v in cells.items()}
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", cells.get("date", "")) or not cells.get("pts"):
            continue
        out.append({c: cells.get(c, "") for c in COLS})
    return out


def rostered():
    """Every name on the pinned week-start rosters and on the diagnosis's daily rosters (daily/, when present)."""
    names = set()
    for f in sorted(glob.glob(os.path.join(HERE, "rosters", "t*.json")) + glob.glob(os.path.join(HERE, "daily", "t*.json"))):
        names |= {p["name"] for p in json.load(open(f, encoding="utf-8"))["players"]}
    return sorted(names)


def bref_ids(raw):
    body = open(os.path.join(raw, "NBA_2026_per_game.html"), "rb").read()
    if hashlib.sha256(body).hexdigest() != PER_GAME_SHA:
        sys.exit("LOGS: FAIL — NBA_2026_per_game.html is not the page #159 resolved its ids from")
    ids = {}
    for m in re.finditer(r'data-append-csv="([a-z0-9]+)"[^>]*>\s*<a href="[^"]+">([^<]+)</a>', body.decode("utf-8", "replace")):
        ids.setdefault(norm(html.unescape(m.group(2))), set()).add(m.group(1))
    return ids


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.status, r.read()


def main():
    raw = sys.argv[1]
    reparse = "--reparse" in sys.argv[2:]
    ids = bref_ids(raw)
    prior = {r["bref_id"] for r in csv.DictReader(open(PRIOR, encoding="utf-8"))}
    resolved, unresolved = {}, []
    for n in rostered():
        s = ids.get(norm(n), set())
        if len(s) > 1:
            sys.exit(f"LOGS: FAIL — {n} matches {len(s)} ids on the per-game page: {sorted(s)}")
        if s:
            resolved[n] = next(iter(s))
        elif n not in NO_GAMES:
            unresolved.append(n)
    if unresolved:
        sys.exit(f"LOGS: FAIL — {len(unresolved)} rostered names resolve to no id and carry no receipt: {unresolved}")
    have = os.path.exists(os.path.join(HERE, "logs_manifest.json"))
    prev = json.load(open(os.path.join(HERE, "logs_manifest.json"), encoding="utf-8")) if have else {}
    old = {p["bref_id"]: p for p in prev.get("pages", [])}
    pages, rows, failed = [], [], []
    for n, pid in sorted(resolved.items()):
        if pid in prior:
            continue
        url = f"https://www.basketball-reference.com/players/{pid[0]}/{pid}/gamelog/2026"
        path = os.path.join(raw, f"{pid}.html")
        if reparse:
            body = open(path, "rb").read() if old[pid]["sha256"] else b""
            if body and hashlib.sha256(body).hexdigest() != old[pid]["sha256"]:
                sys.exit(f"LOGS: FAIL — {pid}.html differs from the manifest's sha256")
            st = old[pid]["status"]
        elif pid in old and old[pid]["sha256"] and os.path.exists(path) \
                and hashlib.sha256(open(path, "rb").read()).hexdigest() == old[pid]["sha256"]:
            body, st = open(path, "rb").read(), old[pid]["status"]  # fetched before and unchanged: not fetched again
        else:
            for attempt in (1, 2):
                try:
                    st, body = get(url)
                    break
                except Exception as e:  # noqa: BLE001
                    st, body = getattr(e, "code", None) or str(e), b""
                    if attempt == 1:
                        time.sleep(60)
            if body:
                open(path, "wb").write(body)
            time.sleep(3.5)
        games = parse(body.decode("utf-8", "replace")) if body else None
        pages.append(dict(player=n, bref_id=pid, url=url, status=st, sha256=hashlib.sha256(body).hexdigest() if body else None,
                          games=len(games) if games is not None else None))
        if games is None:
            failed.append(n)
        else:
            rows += [dict(player=n, bref_id=pid, **g) for g in games]
    with open(os.path.join(HERE, "gamelogs_extra_2025-26.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["player", "bref_id"] + COLS, lineterminator="\n"); w.writeheader(); w.writerows(rows)
    new = [p["bref_id"] for p in pages if p["bref_id"] not in old]
    man = dict(fetched_utc=prev.get("fetched_utc") or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               added_utc=(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) if new and old else prev.get("added_utc")),
               added=sorted(set(prev.get("added", [])) | (set(new) if old else set())),
               per_game_sha256=PER_GAME_SHA, rostered=len(resolved) + len(NO_GAMES & set(rostered())),
               reused_from_159=sum(1 for p in resolved.values() if p in prior), fetched=len(pages),
               no_games=sorted(NO_GAMES & set(rostered())), failed=failed, resolved=dict(sorted(resolved.items())), pages=pages)
    with open(os.path.join(HERE, "logs_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(man, f, indent=1); f.write("\n")
    verdict = "PASS" if not failed else "FAIL"
    print(f"LOGS: {verdict} — {man['rostered']} rostered: {man['reused_from_159']} reused, {len(pages)} fetched "
          f"({len(rows)} game rows), {len(man['no_games'])} with no 2025-26 game, {len(failed)} failed {failed}")


if __name__ == "__main__":
    main()
