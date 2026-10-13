#!/usr/bin/env python3
"""Evidence extractor for the 2026-10-13 scope-fence after-report. Reads the Claude Code session log (JSONL) and writes:
  - the timeline from the owner's 10/12 career-averages question to the end of the log: owner messages (verbatim),
    assistant text (verbatim), tool-call descriptions (verbatim, the line the owner sees), skill loads, compactions,
    and owner messages queued mid-turn;
  - a census of governor loads over the whole log: Skill-tool loads, re-attached skill bodies after compaction
    (which skills, how often, first/last), and catalog listings (names and descriptions only).
The window ends at the owner's after-report request (2026-10-13), and the census counts only entries up to it, so a
rerun on a longer log reproduces the same file.
Usage: extract_timeline.py <session.jsonl> <out.json>"""
import json, re, sys
LOG, OUT = sys.argv[1:3]
L = [json.loads(l) for l in open(LOG, encoding="utf-8")]
def text_of(e):
    c = e.get("message", {}).get("content")
    if isinstance(c, str): return c
    return "\n".join(b.get("text", "") for b in (c or []) if isinstance(b, dict) and b.get("type") == "text")
start = next(i for i, e in enumerate(L) if e.get("type") == "user" and "career averages are being taken" in text_of(e) and "Summary:" not in text_of(e))
end = next(i for i, e in enumerate(L) if i > start and e.get("type") == "user" and text_of(e).startswith("Can you please provide an after-report of this scope-fence breach"))
L = L[:end + 1]
events = []
for i in range(start, len(L)):
    e = L[i]; t = e.get("type"); ts = e.get("timestamp")
    if t == "user":
        s = text_of(e)
        if s.startswith("This session is being continued from a previous conversation"):
            keep = [ln.strip() for ln in s.splitlines() if re.search(r"20-season|20 season|20-year|backtest|candidate", ln, re.I)]
            events.append(dict(i=i, ts=ts, kind="compaction summary (lines that carry the backtests forward)", text=keep)); continue
        if s.startswith("Base directory for this skill:"): events.append(dict(i=i, ts=ts, kind="skill text loaded", text=s.splitlines()[0])); continue
        if s.strip() == "[Request interrupted by user]": events.append(dict(i=i, ts=ts, kind="owner interrupt", text=s)); continue
        if s.strip() and not s.lstrip().startswith("<"): events.append(dict(i=i, ts=ts, kind="owner message", text=s))
        for b in (e.get("message", {}).get("content") or []):
            if isinstance(b, dict) and b.get("type") == "tool_result":
                cs = json.dumps(b.get("content"))
                if "The user sent a new message while you were working" in cs:
                    m = re.search(r"The user sent a new message while you were working:\\n(.*?)\\n\\nThis is how Claude Code surfaces", cs)
                    events.append(dict(i=i, ts=ts, kind="owner message (mid-turn)", text=json.loads('"' + m.group(1) + '"') if m else "(present)"))
    elif t == "queue-operation":
        if e.get("operation") == "enqueue" and e.get("content"):
            events.append(dict(i=i, ts=ts, kind="owner message queued mid-turn", text=e["content"] if isinstance(e["content"], str) else json.dumps(e["content"])))
    elif t == "assistant":
        for b in e.get("message", {}).get("content", []):
            if not isinstance(b, dict): continue
            if b.get("type") == "text" and b["text"].strip(): events.append(dict(i=i, ts=ts, kind="assistant text", text=b["text"]))
            if b.get("type") == "tool_use":
                inp = b.get("input", {})
                if b["name"] == "Skill": events.append(dict(i=i, ts=ts, kind="skill load", text=inp.get("skill")))
                elif b["name"] == "Write": events.append(dict(i=i, ts=ts, kind="tool call", tool="Write", text="write " + inp.get("file_path", "")))
                else: events.append(dict(i=i, ts=ts, kind="tool call", tool=b["name"], text=inp.get("description") or inp.get("file_path") or ""))
census = {"log_entries": len(L), "first_ts": next(e.get("timestamp") for e in L if e.get("timestamp")), "last_ts": L[-1].get("timestamp"),
          "skill_tool_loads": [], "reattached_bodies": {}, "plan_gate_reattached_with_D51R_args": 0, "catalog_listings": 0, "compactions": 0,
          "governor_file_reads_by_tools": []}
GOV = re.compile(r"(plan-gate|scope-fence|adversarial-verify|gauntlet)/SKILL\.md")
for i, e in enumerate(L):
    if e.get("type") == "assistant":
        for b in e.get("message", {}).get("content", []):
            if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Skill":
                census["skill_tool_loads"].append(dict(i=i, ts=e.get("timestamp"), skill=b["input"].get("skill"), args=(b["input"].get("args") or "")[:160]))
    if e.get("type") == "attachment":
        at = e.get("attachment") or {}; sk = at.get("skills")
        if at.get("type") == "skill_listing": census["catalog_listings"] += 1      # names + descriptions only
        if at.get("type") == "invoked_skills" and isinstance(sk, list):            # full bodies re-attached after a compaction
            for s in sk:
                m = re.search(r"/synced/[^/]+/([a-z-]+)", s.get("content", "")); name = m.group(1) if m else "?"
                if name == "plan-gate" and "D51R" in s.get("content", ""): census["plan_gate_reattached_with_D51R_args"] += 1
                r = census["reattached_bodies"].setdefault(name, {"count": 0, "first": None, "last": None})
                r["count"] += 1; r["first"] = r["first"] or e.get("timestamp"); r["last"] = e.get("timestamp")
    if e.get("isCompactSummary"): census["compactions"] += 1
    if e.get("type") == "assistant":
        for b in e.get("message", {}).get("content", []):
            if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") in ("Bash", "Read"):
                g = GOV.search(json.dumps(b.get("input")))
                if g: census["governor_file_reads_by_tools"].append(dict(i=i, ts=e.get("timestamp"), file=g.group(0)))
json.dump(dict(log=LOG, start_index=start, events=events, census=census), open(OUT, "w"), indent=1, ensure_ascii=False)
print("events", len(events), "from index", start, "| census:", json.dumps({k: v for k, v in census.items() if k != "skill_tool_loads"}), "| skill loads:", [(x["ts"][:16], x["skill"]) for x in census["skill_tool_loads"]])
