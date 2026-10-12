#!/usr/bin/env python3
"""2026-10-12 (WO-5 find): the Your-roster panel lists every pick — a man no open slot can hold shows in an EXTRA
row and the open slot stays open. Exact anchors; all-or-nothing."""
P = "/home/user/yahoo-fantasy-basketball/docs/draft-deck.html"
s = open(P, encoding="utf-8").read(); orig = s
OLD = '''    for (let si = 0; si < slots.length && leftovers.length; si++)
      if (!slots[si].elig && !assigned[si]) assigned[si] = leftovers.shift();

    const ul = $("myRoster");
    ul.innerHTML = "";
    slots.forEach((slot, si) => {
      const m = assigned[si];
      const li = el("li", m ? "" : "empty");
      li.append(el("span", "slot", slot.label));'''
NEW = '''    for (let si = 0; si < slots.length && leftovers.length; si++)
      if (!slots[si].elig && !assigned[si]) assigned[si] = leftovers.shift();
    /* A man no open slot can hold (bench and Utils full, a positional slot
       still open — e.g. one C among 13) shows in an EXTRA row below the
       template, and the open slot stays shown as open; before 2026-10-12
       (WO-5 find) he was left off the panel. */
    const rows = slots.map((slot, si) => ({ label: slot.label, m: assigned[si] }))
      .concat(leftovers.map(m => ({ label: "EXTRA", m })));

    const ul = $("myRoster");
    ul.innerHTML = "";
    rows.forEach(({ label, m }) => {
      const li = el("li", m ? "" : "empty");
      li.append(el("span", "slot", label));'''
assert s.count(OLD) == 1
s = s.replace(OLD, NEW, 1)
A = " Draft state autosaves in this browser; export <code>draft_state.json</code> for post-draft analysis.</p>"
assert s.count(A) == 1
s = s.replace(A, " Your roster lists every pick: a player no open slot can hold (say, one C among 13 with the bench full) shows in an EXTRA row, and the open slot stays shown as open (2026-10-12)." + A, 1)
assert s != orig
open(P, "w", encoding="utf-8").write(s)
print("roster panel fix applied; Logic sentence added")
