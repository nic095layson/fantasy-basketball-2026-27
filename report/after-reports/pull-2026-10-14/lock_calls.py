"""The owner's three lock calls of 10/14 (D-1014-5/6/7), written to both planes
with assertions. Idempotent: a second run changes nothing.

  Kornet  — the pre-blend line restored (lines_blend_2026-10-14.json "old"),
            kit and deck; games, minutes, tag unchanged.
  White   — deck leading tag inj-calf-risk (availability 0.78); kit GP 68 to 62.
  Cardwell— deck leading tag inj-calf-risk (availability 0.78); kit GP 65 to 59.

GP: the precedent of D-1010-2 (Stewart 70 to 64) and D-1012-1 (Raynaud 72 to
66) — six games, about two weeks of the schedule, for a risk tag.
"""
import csv, io, json, os, sys

KIT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DECK = "/home/user/yahoo-fantasy-basketball"
KIT_CSV = os.path.join(KIT, "report", "projections-2026-27.csv")
DECK_CSV = os.path.join(DECK, "data", "players.csv")
BLEND = os.path.join(KIT, "report", "blend", "out", "lines_blend_2026-10-14.json")
OUT = os.path.join(os.path.dirname(__file__), "lock_calls_2026-10-14.json")

GP = {"Coby White": (68, 62), "Dylan Cardwell": (65, 59)}
TAG = {
    "Coby White": "inj-calf-risk (owner call 10/14, D-1014-6: a left calf strain in camp, "
                  "announced 10/5, out the whole preseason, a 10/21 estimate on ESPN's feed, "
                  "his third calf strain in about a year per the 10/5 reports; availability "
                  "0.78 and the kit's GP 68 to 62 as the twin, the Stewart/Raynaud shape); ",
    "Dylan Cardwell": "inj-calf-risk (owner call 10/14, D-1014-5: Out at least two weeks with "
                      "a left calf strain per Anthony Slater of ESPN.com on ESPN's feed, item "
                      "2026-10-13 20:57Z, a 10/29 estimate; availability 0.78 and the kit's GP "
                      "65 to 59 as the twin, the Stewart/Raynaud shape); ",
}
KORNET_NOTE = ("; 10/14 lock: owner call D-1014-7 — the pre-blend line restored "
               "(FG% .613 on 4.0 FGA, FT% .812 on 1.7 FTA, 6.3 pts, 6.1 reb, 1.9 ast, "
               "0.5 stl, 1.1 blk, 0.4 tov); preseason backed ours (three methods agree), "
               "the blend took his line toward an outside average of 17.4 min")
KIT_MAP = {"fgp": "fg_pct", "fga": "fga", "ftp": "ft_pct", "fta": "fta", "tpm": "tpm",
           "pts": "pts", "reb": "reb", "ast": "ast", "stl": "stl", "blk": "blk", "tov": "tov"}


def fmt(col, v):
    return f"{v:.3f}" if col in ("fgp", "ftp", "fg_pct", "ft_pct") else f"{v:.1f}"


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        raw = f.read()
    rows = list(csv.DictReader(io.StringIO(raw)))
    return raw, list(csv.DictReader(io.StringIO(raw)).fieldnames), rows


def dump(path, fields, rows, raw_before):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n" if "\r\n" not in raw_before else "\r\n")
    w.writeheader()
    w.writerows(rows)
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())


def main():
    old = {r["name"]: r for r in json.load(open(BLEND))["rows"]}["Luke Kornet"]["old"]
    log = {"kit": [], "deck": []}

    # ---- kit
    raw, fields, rows = load(KIT_CSV)
    before = [dict(r) for r in rows]
    for r in rows:
        if r["name"] == "Luke Kornet":
            for kc, dc in KIT_MAP.items():
                nv = fmt(kc, old[dc])
                if r[kc] != nv:
                    log["kit"].append(["Luke Kornet", kc, r[kc], nv]); r[kc] = nv
        if r["name"] in GP:
            a, b = GP[r["name"]]
            if r["gp"] != str(b):
                assert r["gp"] == str(a), (r["name"], r["gp"])
                log["kit"].append([r["name"], "gp", r["gp"], str(b)]); r["gp"] = str(b)
    # A1: only the named cells moved
    for x, y in zip(before, rows):
        for c in fields:
            if x[c] != y[c]:
                assert (x["name"] == "Luke Kornet" and c in KIT_MAP) or (x["name"] in GP and c == "gp"), (x["name"], c)
    assert len(before) == len(rows)
    dump(KIT_CSV, fields, rows, raw)

    # ---- deck
    raw, fields, rows = load(DECK_CSV)
    before = [dict(r) for r in rows]
    for r in rows:
        n = r["player"]
        if n == "Luke Kornet":
            for dc in KIT_MAP.values():
                nv = fmt(dc, old[dc])
                if r[dc] != nv:
                    log["deck"].append([n, dc, r[dc], nv]); r[dc] = nv
            if "10/14 lock:" not in r["note"]:
                r["note"] += KORNET_NOTE; log["deck"].append([n, "note", "", KORNET_NOTE])
        if n in TAG and not r["note"].startswith("inj-calf-risk"):
            r["note"] = TAG[n] + r["note"]; log["deck"].append([n, "note-tag", "", TAG[n]])
    # A2: only the named cells moved; A3: no injection trap; A4: tags read right
    for x, y in zip(before, rows):
        for c in fields:
            if x[c] != y[c]:
                ok = (x["player"] == "Luke Kornet" and (c in KIT_MAP.values() or c == "note")) or \
                     (x["player"] in TAG and c == "note")
                assert ok, (x["player"], c)
    assert len(before) == len(rows)
    sys.path.insert(0, os.path.join(DECK, "scripts"))
    import hoops
    by = {r["player"]: r for r in rows}
    for n in TAG:
        assert hoops.note_tag(by[n]["note"]) == "inj-calf-risk", n
        assert "];" not in by[n]["note"]
    assert "];" not in by["Luke Kornet"]["note"]
    assert hoops.note_tag(by["Luke Kornet"]["note"]) == "rookie-proj"
    # A5: kit and deck Kornet lines agree
    kit = {r["name"]: r for r in csv.DictReader(open(KIT_CSV))}["Luke Kornet"]
    for kc, dc in KIT_MAP.items():
        assert float(kit[kc]) == float(by["Luke Kornet"][dc]), kc
    dump(DECK_CSV, fields, rows, raw)

    if log["kit"] or log["deck"]:  # a re-run leaves the first run's record
        json.dump(log, open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"PASS kit cells changed {len(log['kit'])}, deck cells changed {len(log['deck'])}")


if __name__ == "__main__":
    main()
