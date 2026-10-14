#!/usr/bin/env python3
"""Morning pull 2026-10-14: append dated notes to the deck's players.csv (note column only), with assertions.
Notes come from the records: verdicts.json (the 24 against preseason) and the ESPN injuries feed items dated 2026-10-14 UTC
for pool rows (feed.json, the downloaded feed), plus the one new in-window item since the 10/13 pull (Dylan Cardwell).
No tag, line, team or placement changes. A1 every named player exists once; A2 only the note column changes; A3 no '];';
A4 a second run changes nothing (notes carry a '10/14 pull:' marker and are replaced in place)."""
import csv, io, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__))
DECK = sys.argv[1]; FEED = sys.argv[2]
MARK = "10/14 pull:"
V = json.load(open(os.path.join(H, "verdicts.json")))
cal = V["calibration"]
def g(games): return ", ".join(f"{d[5:]} {o} {'start' if s == 'S' else 'bench'} {int(m)}" for d, o, s, m in games)
notes = {}
for r in V["rows"]:
    if r["pre_gp"] == 0:
        txt = (f"{MARK} no preseason game through 10/13 on ESPN's box scores; ours {r['ours']:.1f} min against the outside "
               f"average {r['outside']:.1f} (Hashtag 10/12, FantasyPros 10/13, BBM cards 10/13) stays unread by preseason")
    elif r["verdict"] == "TOO LITTLE DATA":
        txt = (f"{MARK} one preseason game ({g(r['games'])}); too little to read against ours {r['ours']:.1f} min and the "
               f"outside average {r['outside']:.1f} [SINGLE-SOURCE: box score] (ESPN box scores)")
    else:
        txt = (f"{MARK} preseason {r['pre_gp']} games, {r['starts']} starts, {r['pre_mpg']} min a game ({g(r['games'])}); "
               f"calibrated on {cal['n']} undisputed players it reads {r['adj_shift']}/{r['adj_scale']}/{r['adj_team']} against ours "
               f"{r['ours']:.1f} and the outside average {r['outside']:.1f}: {r['verdict'].lower()} "
               f"[SINGLE-SOURCE: box score] (ESPN box scores)")
    notes[r["name"]] = [txt]
feed = json.load(open(FEED))
fold = lambda s: re.sub(r"\s+", " ", re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", re.sub(r"[.'’]", "", s.lower()))).strip()
raw = open(DECK, encoding="utf-8", newline="").read()
head = raw.splitlines()[0].split(","); rows = list(csv.DictReader(io.StringIO(raw)))
byf = {fold(r["player"]): r["player"] for r in rows}
for t in feed["injuries"]:
    for i in t["injuries"]:
        n = byf.get(fold(i["athlete"]["displayName"]))
        if not n or (i.get("date") or "") < "2026-10-14": continue
        sc = (i.get("shortComment") or "").replace(";", ",").replace("]", ")")
        notes.setdefault(n, []).append(f"{MARK} {i.get('status')} on ESPN's injuries feed (item {i['date'][:16]}Z, "
                                       f"{(i.get('details') or {}).get('returnDate') or 'no'} estimate): {sc} [SINGLE-SOURCE: ESPN feed] (ESPN injuries feed)")
notes.setdefault("Dylan Cardwell", []).append(
    f"{MARK} Out, at least two weeks with a left calf strain per Anthony Slater of ESPN.com via ESPN's injuries feed (item 2026-10-13 20:57Z, "
    "10/29 estimate) — new since the 10/13 pull, untagged, on the decision sheet (D-1014-5) [SINGLE-SOURCE: ESPN feed] (ESPN injuries feed)")
notes.setdefault("Coby White", []).append(
    f"{MARK} the left calf strain of camp (announced 10/5, out the whole preseason, 10/21 estimate on ESPN's feed) is his third calf strain "
    "in about a year per the 10/5 reports (TSN, NBA.com, RotoBaller) — the role tag stands, on the decision sheet (D-1014-6)")
ENTRY = re.compile(r"(; |\. )?" + re.escape(MARK) + r".*$")
d0 = [dict(r) for r in rows]; changed = 0; fails = []
names = {r["player"] for r in rows}
resolved = {}; skipped = []
for n, v in notes.items():
    k = byf.get(fold(n))
    if not k and n in {r["name"] for r in V["rows"]}: skipped.append(n); continue   # kit-only rows (no deck twin)
    if not k: fails.append(f"A1 {n} not in the pool")
    else: resolved.setdefault(k, []).extend(v)
notes = resolved
for r in rows:
    if r["player"] in notes:
        base = ENTRY.sub("", r["note"]).rstrip()
        sep = ". " if base.endswith("]") else "; "
        r["note"] = (base + sep if base else "") + "; ".join(notes[r["player"]])
for r, r0 in zip(rows, d0):
    if any(r[c] != r0[c] for c in head if c != "note"): fails.append(f"A2 {r0['player']}")
    if "];" in r["note"]: fails.append(f"A3 {r['player']}")
    changed += r != r0
if fails: print("NOTES: FAIL", fails[:10]); sys.exit(1)
buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=head, lineterminator="\r\n" if "\r\n" in raw else "\n"); w.writeheader(); w.writerows(rows)
open(DECK, "w", encoding="utf-8", newline="").write(buf.getvalue())
json.dump(notes, open(os.path.join(H, "deck_notes_2026-10-14.json"), "w"), indent=1, ensure_ascii=False)
print(f"NOTES: PASS — {len(notes)} players, {changed} rows changed; kit-only, no deck row: {skipped}")
