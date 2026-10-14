#!/usr/bin/env python3
"""Mock 82 (2026-10-14 evening, LIVE public room, slot 10): Yahoo's round-by-round recap from
owner_message.txt as 156 picks (recap.json), each name resolved to the deck pool's spelling by the deck's own
resolver (hoops.match_candidates, first-name + surname with the recap's team as the tie-break), seats by the snake;
the tool's LIVE feed (the ✓ lines, after undos and inserts) compared pick for pick with the recap. Writes recap.json,
feed.json, the deck state arena/data/states/draft_state_82.json, and state_check.txt."""
import json, os, re, sys, unicodedata
H = os.path.dirname(os.path.abspath(__file__))
DECK = "/home/user/yahoo-fantasy-basketball"
sys.path.insert(0, os.path.join(DECK, "scripts"))
import hoops
L = open(os.path.join(H, "owner_message.txt"), encoding="utf-8").read().split("\n")
# ---- recap
picks = []; rnd = None
i = L.index("Round by Round results")
for s in L[i + 1:]:
    m = re.fullmatch(r"Round (\d+)", s.strip())
    if m: rnd = int(m.group(1)); continue
    m = re.fullmatch(r"\((\d+)\) (.+?) - (.+?), (.+?) \(([A-Z]{2,4}) - ([A-Z,]+)\)", s.strip())
    if m:
        k = int(m.group(1))
        picks.append(dict(n=(rnd - 1) * 12 + k, round=rnd, k=k, manager=m.group(2), name=f"{m.group(4)} {m.group(3)}", team=m.group(5), pos=m.group(6)))
    elif s.strip() and not s.startswith("* your team"): raise SystemExit("UNPARSED: " + s)
picks.sort(key=lambda p: p["n"])
assert [p["n"] for p in picks] == list(range(1, 157)), len(picks)
slot_of = lambda n0: (n0 % 12) + 1 if (n0 // 12) % 2 == 0 else 12 - (n0 % 12)
seat = {}
for p in picks:
    p["slot"] = slot_of(p["n"] - 1); seat.setdefault(p["manager"], set()).add(p["slot"])
assert all(len(v) == 1 for v in seat.values()) and seat["David"] == {10}, seat
# ---- resolve to the pool
hoops.DATA_PATH = os.path.join(DECK, "data", "players.csv")
P = hoops.load_players()
TEAMFIX = {"PHX": {"PHX", "PHO"}, "SAS": {"SAS", "SA"}, "NOP": {"NOP", "NO"}, "GSW": {"GSW", "GS"}, "NYK": {"NYK", "NY"}, "WAS": {"WAS", "WSH"}, "UTA": {"UTA", "UTH"}}
pool_less, resolved = [], {}
for p in picks:
    c = hoops.match_candidates(P, p["name"])
    if len(c) > 1:
        c = [x for x in c if x["team"] in TEAMFIX.get(p["team"], {p["team"]})] or c
    if len(c) == 1:
        p["player"] = c[0]["player"]
    else:
        p["player"] = p["name"]; pool_less.append((p["n"], p["name"], [x["player"] for x in c][:4]))
assert len({p["player"] for p in picks}) == 156, "a name resolved twice"
json.dump(picks, open(os.path.join(H, "recap.json"), "w"), ensure_ascii=False, indent=0)
# ---- the tool's feed: ✓ lines replayed with undo and insert
start = next(j for j, s in enumerate(L) if s.startswith("Draft started:"))
end = next(j for j, s in enumerate(L) if s.strip() in ("____", "___", "__", "My Team"))  # mock 82: no separator line; the feed ends at "My Team"
feed = {}
for s in L[start:end]:
    m = re.match(r"\s*✓ \(R\d+\) #(\d+): (.+?) → Seat (\d+)", s)
    if m: feed[int(m.group(1))] = (m.group(2).strip(), int(m.group(3))); continue
    m = re.match(r"\s*✎ inserted (.+?) at #(\d+) → Seat (\d+)", s)
    if m: feed[int(m.group(2))] = (m.group(1).strip(), int(m.group(3))); continue
    # mock 78: an unmatched typed name leaves the pick UNKNOWN (seat by the snake) until a "✎ #N corrected" line names it
    m = re.match(r"⚠ \(R\d+\) #(\d+): UNKNOWN \(\"(.+?)\"", s)
    if m: feed[int(m.group(1))] = (f"UNKNOWN ({m.group(2)})", slot_of(int(m.group(1)) - 1)); continue
    m = re.match(r"\s*✎ #(\d+) corrected: UNKNOWN #\d+ → (.+)", s)
    if m: feed[int(m.group(1))] = (m.group(2).strip(), slot_of(int(m.group(1)) - 1))
assert sorted(feed) == list(range(1, 157)), sorted(set(range(1, 157)) - set(feed))
unknown_left = [(n, v[0]) for n, v in sorted(feed.items()) if v[0].startswith("UNKNOWN")]
json.dump({str(k): v for k, v in sorted(feed.items())}, open(os.path.join(H, "feed.json"), "w"), ensure_ascii=False, indent=0)
f = lambda s: hoops.fold(s)
diff = [(n, feed[n], picks[n - 1]["player"], picks[n - 1]["slot"]) for n in range(1, 157)
        if f(feed[n][0]) != f(picks[n - 1]["player"]) or feed[n][1] != picks[n - 1]["slot"]]
state = {"teams": 12, "slot": 10, "size": 13, "punt": [], "picks": [{"player": p["player"], "slot": p["slot"]} for p in picks]}
json.dump(state, open(os.path.join(DECK, "arena", "data", "states", "draft_state_82.json"), "w"), ensure_ascii=False, indent=0)
out = [f"recap picks {len(picks)}; seats {len(seat)} (David = 10); pool-less {len(pool_less)}: {pool_less}",
       f"feed vs recap: {156 - len(diff)} of 156 agree on name and seat; differences {diff}",
       f"feed picks still UNKNOWN at the end: {unknown_left}",
       "owner picks: " + ", ".join(f"#{p['n']} {p['player']}" for p in picks if p["slot"] == 10)]
open(os.path.join(H, "state_check.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
# ---- mock 82: the tool log as replay events (arena/data/events/m82_tool_events.json), in the order the paste shows.
# A ✓ line is a feed of the resolved name (the typed short form is not in the paste — the "assumed over" lines);
# an UNKNOWN line is a feed of the raw text; a "✎ #N corrected" line is the numbered fix "N- Name"; "still UNKNOWN"
# warnings and "— resumed" lines carry no event (the resume is one session in the replay).
ev = []
for s in L[start:end]:
    m = re.match(r"\s*✓ \(R\d+\) #(\d+): (.+?) → Seat (\d+)", s)
    if m: ev.append({"op": "feed", "text": m.group(2).strip(), "expect": m.group(2).strip()}); continue
    m = re.match(r"⚠ \(R\d+\) #(\d+): UNKNOWN \(\"(.+?)\"", s)
    if m: ev.append({"op": "feed", "text": m.group(2), "expect": f'UNKNOWN ("{m.group(2)}"'}); continue
    m = re.match(r"\s*✎ #(\d+) corrected: UNKNOWN #\d+ → (.+)", s)
    if m: ev.append({"op": "feed", "text": f"{m.group(1)}- {m.group(2).strip()}", "expect": f"#{m.group(1)} corrected"}); continue
json.dump(ev, open(os.path.join(DECK, "arena", "data", "events", "m82_tool_events.json"), "w"), ensure_ascii=False, indent=0)
print(f"events {len(ev)}: feeds {sum(1 for e in ev if not e['text'][0].isdigit())}, numbered fixes {sum(1 for e in ev if e['text'][0].isdigit())}")
