#!/usr/bin/env python3
"""Figures the 2026-10-13 scope-fence after-report quotes, computed from out/timeline.json (no hand counts).
Usage: timeline_stats.py <timeline.json> <out.json>"""
import json, sys
from datetime import datetime
T = json.load(open(sys.argv[1], encoding="utf-8")); ev = T["events"]
ts = lambda e: datetime.fromisoformat(e["ts"].replace("Z", "+00:00"))
def first(pred): return next(e for e in ev if pred(e))
q = ev[0]
interrupt = first(lambda e: e["kind"] == "owner interrupt")
objection = first(lambda e: "owner message" in e["kind"] and "20 year test" in str(e["text"]))
last_text_before = [e for e in ev if e["kind"] == "assistant text" and e["i"] < interrupt["i"]][-1]
label_20 = [e for e in ev if e["kind"] == "tool call" and "20 season" in e["text"]]
cand_write = first(lambda e: e["kind"] == "tool call" and e.get("tool") == "Write" and "candidate" in e["text"])
usage_req = first(lambda e: "owner message" in e["kind"] and "Usage on new team" in str(e["text"]))
scope_q = first(lambda e: "owner message" in e["kind"] and "scope-fence" in str(e["text"]))
scope_ans = first(lambda e: e["kind"] == "assistant text" and "scope question first" in e["text"])
calls_silent = [e for e in ev if e["kind"] == "tool call" and last_text_before["i"] < e["i"] < interrupt["i"]]
texts_before = [e for e in ev if e["kind"] == "assistant text" and e["i"] < interrupt["i"]]
mention = lambda words: [e["i"] for e in texts_before if any(w in e["text"].lower() for w in words)]
out = dict(
    question=dict(i=q["i"], ts=q["ts"]),
    usage_requirement_mid_turn=dict(i=usage_req["i"], ts=usage_req["ts"], text=usage_req["text"]),
    owner_visible_texts_before_interrupt=[dict(i=e["i"], ts=e["ts"], text=e["text"]) for e in texts_before],
    texts_before_interrupt_mentioning_window_or_seasons=mention(["season", "2006", "window", "20-", "years"]),
    texts_before_interrupt_mentioning_candidate_or_fix=mention(["candidate", "wo-5b", "fix", "build", "dry run"]),
    tool_labels_naming_the_window=[dict(i=e["i"], ts=e["ts"], text=e["text"]) for e in label_20],
    candidate_write=dict(i=cand_write["i"], ts=cand_write["ts"]),
    tool_calls_after_last_text_before_interrupt=len(calls_silent),
    tool_call_labels_in_that_stretch=[e["text"] for e in calls_silent],
    minutes_last_text_to_interrupt=round((ts(interrupt) - ts(last_text_before)).total_seconds() / 60, 1),
    minutes_question_to_interrupt=round((ts(interrupt) - ts(q)).total_seconds() / 60, 1),
    minutes_question_to_candidate_write=round((ts(cand_write) - ts(q)).total_seconds() / 60, 1),
    objection=dict(i=objection["i"], ts=objection["ts"]), interrupt=dict(i=interrupt["i"], ts=interrupt["ts"]),
    scope_question=dict(i=scope_q["i"], ts=scope_q["ts"]), scope_answer=dict(i=scope_ans["i"], ts=scope_ans["ts"]),
    minutes_scope_question_to_answer=round((ts(scope_ans) - ts(scope_q)).total_seconds() / 60, 1),
    compaction_lines=[e["text"] for e in ev if e["kind"].startswith("compaction")][0],
)
json.dump(out, open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
for k, v in out.items():
    if k not in ("owner_visible_texts_before_interrupt", "compaction_lines", "tool_call_labels_in_that_stretch"): print(k, "=", v)
print("tool_call_labels_in_that_stretch =", out["tool_call_labels_in_that_stretch"])
print("compaction lines:"); [print("  ", l[:230]) for l in out["compaction_lines"]]
