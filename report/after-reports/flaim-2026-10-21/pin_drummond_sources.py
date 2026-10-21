#!/usr/bin/env python3
"""Pin the two 10/21 records behind Andre Drummond's pool line (owner 2026-10-21: "Drummond, pull data from both sources
to add a projection for him"), read mechanically from this session's transcript, never retyped:
  FantasyBot get_player_value (per-game projection)  -> data/source/fantasybot/player_value_andre-drummond_2026-10-21.json
  Flaim get_players (Yahoo identity and ownership)   -> data/source/flaim/players_andre-drummond_2026-10-21.json

    python3 pin_drummond_sources.py TRANSCRIPT.jsonl
Prints 'PIN: PASS — ...' or exits 1 naming what it could not find."""
import hashlib, json, os, sys

KIT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
WANT = {"mcp__FantasyBot__get_player_value": ("data/source/fantasybot/player_value_andre-drummond_2026-10-21.json",
                                              lambda d: d.get("player", {}).get("name") == "Andre Drummond"),
        "mcp__Flaim_Fantasy__get_players": ("data/source/flaim/players_andre-drummond_2026-10-21.json",
                                            lambda d: any(p.get("name") == "Andre Drummond" for p in d.get("data", {}).get("players", [])))}


def main(path):
    calls, found = {}, {}
    for line in open(path, encoding="utf-8"):
        e = json.loads(line)
        msg = e.get("message") or {}
        for c in msg.get("content") or [] if isinstance(msg.get("content"), list) else []:
            if c.get("type") == "tool_use" and c.get("name") in WANT:
                calls[c["id"]] = (c["name"], c.get("input"))
            if c.get("type") == "tool_result" and c.get("tool_use_id") in calls:
                name, inp = calls[c["tool_use_id"]]
                body = c.get("content")
                text = body if isinstance(body, str) else "".join(x.get("text", "") for x in body if isinstance(x, dict))
                data = json.loads(text)
                if WANT[name][1](data):
                    found[name] = dict(tool=name, input=inp, captured_utc=e.get("timestamp"), response=data)
    missing = [n for n in WANT if n not in found]
    if missing:
        print("PIN: FAIL — no transcript response for " + ", ".join(missing)); sys.exit(1)
    for name, rec in found.items():
        out = os.path.join(KIT, WANT[name][0])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        rec["source_transcript_sha256"] = hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]
        json.dump(rec, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False, sort_keys=True)
        print(f"  {WANT[name][0]}  captured {rec['captured_utc']}  sha256 {hashlib.sha256(open(out, 'rb').read()).hexdigest()[:12]}")
    print(f"PIN: PASS — {len(found)} of {len(WANT)} records pinned from the transcript")


if __name__ == "__main__":
    main(sys.argv[1])
