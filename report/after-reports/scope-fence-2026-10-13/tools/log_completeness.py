#!/usr/bin/env python3
"""How complete is the session log as a record of what the owner saw? For each window, count the assistant messages
(by message id), how many carry a tool call, and how many carry a logged text block. Tool calls are logged entry by entry;
text written beside tool calls is often not (the after-report turn's own messages are the control: text was written in
most of them). Usage: log_completeness.py <session.jsonl> <out.json> <end_index_of_after_report_turn>"""
import json, sys
from collections import OrderedDict
LOG, OUT, END = sys.argv[1], sys.argv[2], int(sys.argv[3])
L = [json.loads(l) for l in open(LOG, encoding="utf-8")][:END + 1]
def text_of(e):
    c = e.get("message", {}).get("content")
    return c if isinstance(c, str) else "\n".join(b.get("text", "") for b in (c or []) if isinstance(b, dict) and b.get("type") == "text")
q = next(i for i, e in enumerate(L) if e.get("type") == "user" and "career averages are being taken" in text_of(e) and "Summary:" not in text_of(e))
intr = next(i for i, e in enumerate(L) if i > q and e.get("type") == "user" and text_of(e).strip() == "[Request interrupted by user]")
req = next(i for i, e in enumerate(L) if i > intr and e.get("type") == "user" and text_of(e).startswith("Can you please provide an after-report of this scope-fence breach"))
def count(a, b):
    M = OrderedDict()
    for i in range(a, b):
        e = L[i]
        if e.get("type") != "assistant": continue
        M.setdefault(e["message"].get("id"), set()).update(x.get("type") for x in e["message"]["content"])
    return dict(entries=f"{a}..{b - 1}", assistant_messages=len(M), with_tool_call=sum("tool_use" in k for k in M.values()),
                with_logged_text=sum("text" in k for k in M.values()))
out = {"10/12 window, question to interrupt": count(q, intr), "after-report turn, request to entry %d" % END: count(req, END + 1)}
json.dump(out, open(OUT, "w"), indent=1); print(json.dumps(out, indent=1))
