#!/usr/bin/env python3
"""The league draft (2026-10-14 night, the owner's real 12-team league, seat 10): Yahoo's pick list from
owner_message.txt as 156 picks (recap.json) — each abbreviated name ("J. Butler III") resolved to the lock pool
(players_v69.csv) by first initial + surname, the recap's NBA team as the tie-break, and the tool's own log as the
last tie-break (every such use is recorded); seats by the snake, managers from the owner's draft order. The tool's
LIVE feed compared pick for pick with the recap. Writes recap.json, feed.json, state_check.txt, the deck state
arena/data/states/draft_state_100.json and the replay events arena/data/events/m100_tool_events.json.

The paste's history is the page's log as rendered at the end: an Insert-at-# re-renders earlier lines from the
state (D59-1), so a line for a pick that was later undone shows the pick's CURRENT occupant. The typed sequence is
rebuilt from the undo lines: each "undid: X" names the pick it removed, which is the most recent feed not yet undone."""
import json, os, re, sys
from collections import Counter
H = os.path.dirname(os.path.abspath(__file__))
DECK = "/home/user/yahoo-fantasy-basketball"
sys.path.insert(0, os.path.join(DECK, "scripts"))
import hoops
L = open(os.path.join(H, "owner_message.txt"), encoding="utf-8").read().split("\n")
f = hoops.fold
# ---- managers by seat (the owner's draft order)
i0 = L.index("Draft order:")
mgr = {}
for s in L[i0 + 1:]:
    m = re.fullmatch(r"(\d+)\. (.+)", s.strip())
    if m: mgr[int(m.group(1))] = m.group(2).strip()
assert sorted(mgr) == list(range(1, 13)) and mgr[10] == "Me", mgr
# ---- Yahoo's pick list: blocks of [number] name name [status] positions team team-name
i1 = next(j for j, s in enumerate(L) if s.startswith("Pick\tPlayer\tTeam"))
i2 = next(j for j in range(i1, len(L)) if L[j].strip() == "__")
blocks, cur = [], None
for s in L[i1 + 1:i2]:
    t = s.strip()
    if not t or re.fullmatch(r"Round \d+", t): continue
    if re.fullmatch(r"\d+", t):
        cur = [int(t)]; blocks.append(cur); continue
    cur.append(t)
picks = []
for b in blocks:
    n, rest = b[0], b[1:]
    assert rest[0] == rest[1], b
    status = rest[2] if len(rest) == 6 else ""
    assert len(rest) in (5, 6) and (not status or re.fullmatch(r"[A-Z]{1,4}", status)), b
    pos, team, tname = rest[-3], rest[-2], rest[-1]
    assert re.fullmatch(r"(PG|SG|SF|PF|C)(,(PG|SG|SF|PF|C))*", pos), b
    picks.append(dict(n=n, abbr=rest[0], status=status, pos=pos, team=team, team_name=tname))
picks.sort(key=lambda p: p["n"])
assert [p["n"] for p in picks] == list(range(1, 157)), len(picks)
slot_of = lambda n0: (n0 % 12) + 1 if (n0 // 12) % 2 == 0 else 12 - (n0 % 12)
tname_of = {}
for p in picks:
    p["slot"] = slot_of(p["n"] - 1); p["manager"] = mgr[p["slot"]]
    tname_of.setdefault(p["slot"], set()).add(p["team_name"])
assert all(len(v) == 1 for v in tname_of.values()) and tname_of[10] == {"Your Team"}, tname_of
# ---- the tool's feed: ✓ lines (final numbering), inserts; plus the typed event sequence
start = next(j for j, s in enumerate(L) if s.startswith("Draft started:"))
end = next(j for j, s in enumerate(L) if s.strip() == "___")
feed, ev, stack = {}, [], []
for s in L[start:end]:
    m = re.match(r"\s*✓ \(R\d+\) #(\d+): (.+?) → Seat (\d+)", s)
    if m:
        feed[int(m.group(1))] = (m.group(2).strip(), int(m.group(3)))
        ev.append({"op": "feed", "text": m.group(2).strip(), "expect": m.group(2).strip()}); stack.append(len(ev) - 1); continue
    m = re.match(r"\s*✎ inserted (.+?) at #(\d+) → Seat (\d+)", s)
    if m:
        feed[int(m.group(2))] = (m.group(1).strip(), int(m.group(3)))
        ev.append({"op": "insert", "P": int(m.group(2)), "text": m.group(1).strip(), "expect": f"inserted {m.group(1).strip()}"}); continue
    m = re.match(r"\s*↶ undid: (.+?) \(Seat (\d+)\)", s)
    if m:
        k = stack.pop(); ev[k]["text"] = ev[k]["expect"] = m.group(1).strip(); ev[k]["undone"] = True
        ev.append({"op": "undo", "expect": "undid"}); continue
    m = re.match(r'⚠ HALTED at "(.+?)"', s)
    if m: ev.append({"op": "feed", "text": m.group(1), "expect": "HALTED"}); continue
    m = re.match(r'⚠ skipped "(.+?)": already off the board', s)
    if m: ev.append({"op": "feed", "text": m.group(1), "expect": "skipped"}); continue
assert sorted(feed) == list(range(1, 157)), sorted(set(range(1, 157)) - set(feed))
json.dump({str(k): v for k, v in sorted(feed.items())}, open(os.path.join(H, "feed.json"), "w"), ensure_ascii=False, indent=0)
# ---- resolve each recap name to the pool
hoops.DATA_PATH = os.path.join(DECK, "arena", "results", "players_v69.csv")
P = hoops.load_players()
SUF = {"jr", "sr", "ii", "iii", "iv"}
TEAMFIX = {"PHX": {"PHX", "PHO"}, "SAS": {"SAS", "SA"}, "NOP": {"NOP", "NO"}, "GSW": {"GSW", "GS"}, "NYK": {"NYK", "NY"}, "WAS": {"WAS", "WSH"}, "UTA": {"UTA", "UTH"}, "BKN": {"BKN", "BRK"}}
strip_suf = lambda toks: [t for t in toks if t.rstrip(".") not in SUF]
how = Counter(); notes = []
for p in picks:
    a = re.sub(r"[.'’]", " ", f(p["abbr"])).split()
    ini, sur = a[0], strip_suf(a[1:])
    def ok(x):
        t = strip_suf(re.sub(r"[.'’]", " ", f(x["player"])).split())
        return t and t[0].startswith(ini) and t[-len(sur):] == sur
    c = [x for x in P if ok(x)]
    if len(c) > 1:
        ct = [x for x in c if x["team"] in TEAMFIX.get(p["team"], {p["team"]})]
        if len(ct) == 1: c = ct; how["initial+surname+team"] += 1
        else:
            fd = [x for x in c if f(x["player"]) == f(feed[p["n"]][0])]
            assert len(fd) == 1, (p, [x["player"] for x in c]); c = fd; how["initial+surname, tool log as tie-break"] += 1
            notes.append(f"#{p['n']} {p['abbr']} ({p['team']}): candidates " + ", ".join(f"{x['player']} ({x['team']})" for x in (ct or [x for x in P if ok(x)])) + f"; the tool log has {feed[p['n']][0]}")
    elif len(c) == 1: how["initial+surname, unique"] += 1
    assert len(c) == 1, (p, [x["player"] for x in c])
    p["player"] = c[0]["player"]; p["pool_team"] = c[0]["team"]
assert len({p["player"] for p in picks}) == 156, "a name resolved twice"
json.dump(picks, open(os.path.join(H, "recap.json"), "w"), ensure_ascii=False, indent=0)
diff = [(n, feed[n], picks[n - 1]["player"], picks[n - 1]["slot"]) for n in range(1, 157)
        if f(feed[n][0]) != f(picks[n - 1]["player"]) or feed[n][1] != picks[n - 1]["slot"]]
team_diff = [(p["n"], p["player"], p["team"], p["pool_team"]) for p in picks if p["pool_team"] not in TEAMFIX.get(p["team"], {p["team"]})]
state = {"teams": 12, "slot": 10, "size": 13, "punt": [], "picks": [{"player": p["player"], "slot": p["slot"]} for p in picks]}
json.dump(state, open(os.path.join(DECK, "arena", "data", "states", "draft_state_100.json"), "w"), ensure_ascii=False, indent=0)
json.dump(ev, open(os.path.join(DECK, "arena", "data", "events", "m100_tool_events.json"), "w"), ensure_ascii=False, indent=0)
out = [f"recap picks {len(picks)}; seats 12; managers " + ", ".join(f"{s} {mgr[s]} ({next(iter(tname_of[s]))})" for s in range(1, 13)),
       "name resolution: " + "; ".join(f"{k} {v}" for k, v in how.items()),
       "tie-breaks by the tool log: " + (" | ".join(notes) if notes else "none"),
       f"Yahoo team differs from the pool's team: {len(team_diff)} {team_diff}",
       f"feed vs recap: {156 - len(diff)} of 156 agree on name and seat; differences {diff}",
       "owner picks: " + ", ".join(f"#{p['n']} {p['player']}" for p in picks if p["slot"] == 10),
       "events " + str(len(ev)) + ": " + ", ".join(f"{k} {v}" for k, v in Counter(e["op"] if e["op"] != "feed" or e["expect"] not in ("HALTED", "skipped") else e["expect"] for e in ev).items())
       + f"; feeds later undone {sum(1 for e in ev if e.get('undone'))}: " + ", ".join(e["text"] for e in ev if e.get("undone"))]
open(os.path.join(H, "state_check.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
