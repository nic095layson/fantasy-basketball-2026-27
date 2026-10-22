#!/usr/bin/env python3
"""D-ZS-1 step 2 (owner 2026-10-21 "Run it"): 2025-26 regular-season game logs from Basketball-Reference for the
kit season board's top 180 (10/21) that have a 2025-26 Basketball-Reference id (q_ids.json). Paced ~3.5 s per page;
a 429 or error pauses 60 s and retries once. Raw pages are kept outside the repo (scratch) with their sha256 in the
manifest; the parsed rows (date, team, opponent, mp, fg, fga, ft, fta, fg3, pts, trb, ast, stl, blk, tov) are written
to gamelogs_2025-26.csv. Prints 'GAMELOGS: PASS — n of m' when at least 150 players parsed.

    python3 pull_gamelogs.py RAW_DIR            fetch every page, then parse
    python3 pull_gamelogs.py RAW_DIR --reparse  parse the saved pages again (each page's sha256 must equal the manifest's)

2026-10-21: the first parse kept Basketball-Reference's repeated in-table header rows (date "Date", points "PTS":
1,183 rows, about seven per player). A game row now needs an ISO date; --reparse rebuilt the CSV from the same bytes."""
import csv, hashlib, html, json, os, re, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = sys.argv[1]
REPARSE = "--reparse" in sys.argv[2:]
os.makedirs(RAW, exist_ok=True)
q = json.load(open(os.path.join(HERE, "q_ids.json"), encoding="utf-8"))
COLS = ["date", "team_name_abbr", "opp_name_abbr", "mp", "fg", "fga", "ft", "fta", "fg3", "pts", "trb", "ast", "stl", "blk", "tov"]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.status, r.read()


def parse(page):
    m = re.search(r'<table[^>]*id="player_game_log_reg".*?</table>', page, re.S)
    if not m:
        return None
    out = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(0), re.S):
        cells = dict(re.findall(r'data-stat="([a-z_0-9]+)"[^>]*>(.*?)</t[dh]>', tr, re.S))
        cells = {k: html.unescape(re.sub(r"<[^>]+>", "", v)).strip() for k, v in cells.items()}
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", cells.get("date", "")) or not cells.get("pts"):
            continue  # the repeated header rows (date "Date") and did-not-play rows (no points cell)
        out.append({c: cells.get(c, "") for c in COLS})
    return out


manifest, rows, failed = [], [], []
if REPARSE:
    old = json.load(open(os.path.join(HERE, "pull_manifest.json"), encoding="utf-8"))
    for pg in old["pages"]:
        body = open(os.path.join(RAW, f"{pg['bref_id']}.html"), "rb").read() if pg["sha256"] else b""
        if body and hashlib.sha256(body).hexdigest() != pg["sha256"]:
            sys.exit(f"GAMELOGS: FAIL — {pg['bref_id']}.html differs from the manifest's sha256")
        games = parse(body.decode("utf-8", "replace")) if body else None
        pg["games"] = len(games) if games is not None else None
        if games is None:
            failed.append(pg["player"])
        else:
            rows += [dict(player=pg["player"], bref_id=pg["bref_id"], **g) for g in games]
    manifest = old["pages"]
for name, pid in ({} if REPARSE else q["bref_ids"]).items():
    url = f"https://www.basketball-reference.com/players/{pid[0]}/{pid}/gamelog/2026"
    for attempt in (1, 2):
        try:
            st, body = get(url)
            break
        except Exception as e:  # noqa: BLE001
            st, body = getattr(e, "code", None) or str(e), b""
            if attempt == 1:
                time.sleep(60)
    raw = os.path.join(RAW, f"{pid}.html")
    if body:
        open(raw, "wb").write(body)
    games = parse(body.decode("utf-8", "replace")) if body else None
    manifest.append(dict(player=name, bref_id=pid, url=url, status=st, sha256=hashlib.sha256(body).hexdigest() if body else None,
                         games=len(games) if games is not None else None))
    if games is None:
        failed.append(name)
    else:
        rows += [dict(player=name, bref_id=pid, **g) for g in games]
    time.sleep(3.5)
with open(os.path.join(HERE, "gamelogs_2025-26.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["player", "bref_id"] + COLS, lineterminator="\n"); w.writeheader(); w.writerows(rows)
rec = dict(fetched_utc=old["fetched_utc"], reparsed_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())) if REPARSE \
    else dict(fetched_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
json.dump(dict(rec, pages=manifest, failed=failed), open(os.path.join(HERE, "pull_manifest.json"), "w"), indent=1, ensure_ascii=False)
ok = len(q["bref_ids"]) - len(failed)
print(f"GAMELOGS: {'PASS' if ok >= 150 else 'FAIL'} — {ok} of {len(q['bref_ids'])} players parsed, {len(rows)} game rows; failed: {failed}")
